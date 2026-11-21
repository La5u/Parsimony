"""Import SWE-bench Multilingual tasks and one-attempt runs.

    python -m parsimony.multilingual dataset ml.parquet --language go --output go.jsonl
    python -m parsimony.multilingual analyze ENTRY --dataset go.jsonl --output records.jsonl
    python -m parsimony.multilingual analyze rusta-glm --rusta-dir DIR --dataset go.jsonl --output records.jsonl
"""
import argparse
import hashlib
import http.client
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from .analysis import implementation
from .artifacts import Cache
from .benchmark import analyze_submission, read_jsonl
from .deepswe import blank_context, dataset_rows, fetch_json, fetch_patch
from .languages import SUPPORTED, extension_language

PREFIX = 'multilingual_'
LANGUAGES = tuple(language for language in SUPPORTED if language in {'go', 'javascript', 'typescript', 'php'})
DATASET_COMMIT = '846e647b9f33c0b51b739d005d13d85493c9af09'
DATASET_URL = (f'https://huggingface.co/datasets/SWE-bench/SWE-bench_Multilingual/resolve/{DATASET_COMMIT}'
               '/data/test-00000-of-00001.parquet')
DATASET_SHA256 = '92abca7cb527b41a9f66d03a26ce441ff7319e3a49f985998fd56be4bb9b08b2'
EXPERIMENTS_COMMIT = '40f164d5b8f1d249bf95a6df8b74b577fd8e519d'
EXPERIMENTS_PATH = f'{EXPERIMENTS_COMMIT}/evaluation/multilingual'
EXPERIMENTS = f'https://raw.githubusercontent.com/SWE-bench/experiments/{EXPERIMENTS_PATH}'
BUCKET = 'https://swe-bench-submissions.s3.amazonaws.com/multilingual'
RUSTA_URL = ('https://github.com/vladimirpesic/devscriptor-web/releases/download/swe-bench-multilingual/'
             'rusta-devscriptor-swe-bench-multilingual.tar.gz')
RUSTA_SHA256 = '3adc3cbeed472b3a8d9cf9e633a6dae6a6ff81276ec7f0874135861674473d52'
RUSTA_MODELS = {'rusta-deepseek': ('deepseek-flash', 'DeepSeek V4.1 Flash'),
                'rusta-glm': ('glm-5.3', 'GLM-5.3'), 'rusta-kimi': ('kimi-for-coding', 'Kimi K2.8 Preview')}

# Labels from info.name and mini-swe-agent_version in the pinned metadata.
NAMES = {f'20260213_mini-v2.0.0a0_{model}': f'{name} · mini-SWE-agent 2.0' for model, name in {
    'claude-4-5-haiku': 'Claude Haiku 4.5', 'claude-4-5-opus': 'Claude Opus 4.5',
    'claude-4-5-sonnet': 'Claude Sonnet 4.5', 'claude-4-6-opus': 'Claude Opus 4.6',
    'deepseek-3-2': 'DeepSeek V3.2', 'gemini-3-flash': 'Gemini 3 Flash', 'gemini-3-pro': 'Gemini 3 Pro',
    'glm-5': 'GLM-5', 'gpt-5-2-high': 'GPT-5.2 (high)', 'gpt-5-mini': 'GPT-5 mini', 'kimi-k2-5': 'Kimi K2.5',
}.items()}
NAMES.update({'20260216_mini-v2.0.0a0_minimax-2-5': 'MiniMax M2.5 · mini-SWE-agent 2.0',
              '20260220_mini-v2.0.0_gpt-5-2-codex': 'GPT-5.2 Codex · mini-SWE-agent 2.0',
              '20260902_mini-v2.4.6_gemini-3-5-flash': 'Gemini 3.5 Flash · mini-SWE-agent 2.4.6'})
NAMES.update({entry: f'{name} (max) · Rusta 1.0.0' for entry, (_, name) in RUSTA_MODELS.items()})

EXCLUDED_EXTENSIONS = {'.java': 'java', '.rb': 'ruby',
                       **dict.fromkeys(('.c', '.h', '.cc', '.cpp', '.cxx', '.hh', '.hpp', '.hxx'), 'c/c++')}
DIFF_PATHS = re.compile(r'^diff --git a/(.+?) b/([^\r\n]+)\r?$', re.M)


def display_name(agent):
    entry = agent.removeprefix(PREFIX)
    return NAMES.get(entry, entry)


def repo_languages(tasks):
    """One vote per language per reference patch. All tasks inherit the repository's winner."""
    votes = defaultdict(Counter)
    for task in tasks:
        languages = set()
        for paths in DIFF_PATHS.findall(task['patch']):
            for path in paths:
                language = extension_language(path)
                if language and implementation(path, language):
                    languages.add(language)
                elif not language:
                    excluded = EXCLUDED_EXTENSIONS.get(Path(path).suffix.lower())
                    # Apply the same path exclusions to unsupported source extensions.
                    if excluded and implementation(str(Path(path).with_suffix('.go')), 'go'):
                        languages.add(excluded)
        votes[task['repo']].update(languages)
    repos = {}
    for repo, counts in sorted(votes.items()):
        best = counts.most_common(2)
        if not best or (len(best) == 2 and best[0][1] == best[1][1]):
            raise ValueError(f'{repo}: no unique source language ({dict(counts)})')
        repos[repo] = best[0][0]
    return repos


def dataset(parquet_path, language):
    """Read a local Parquet file and make one item per task of the chosen language."""
    if language not in LANGUAGES:
        raise ValueError(f'unsupported Multilingual track: {language}')
    try:
        import pyarrow.parquet as parquet
    except ImportError as exc:
        raise ValueError('reading Parquet requires the optional pyarrow dependency') from exc
    with Path(parquet_path).open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        stream.seek(0)
        tasks = parquet.read_table(stream, columns=['instance_id', 'repo', 'base_commit', 'patch']).to_pylist()
    if len({t['instance_id'] for t in tasks}) != len(tasks):
        raise ValueError('duplicate Multilingual task IDs')
    repos = repo_languages(tasks)
    counts = Counter(repos[t['repo']] for t in tasks)
    for name in sorted(counts.keys() | set(LANGUAGES)):
        members = ', '.join(repo for repo, track in repos.items() if track == name)
        excluded = ' (excluded)' if name not in LANGUAGES else ''
        print(f'{name}{excluded}: {counts[name]} tasks; {members or "no repositories"}')
    rows = dataset_rows([dict(t, task=t['instance_id'], language=language, patch=blank_context(t['patch']))
                         for t in tasks if repos[t['repo']] == language], attempts=1)
    return [dict(row, dataset_file_sha256=digest) for row in rows]


def _mini_metadata(raw):
    """Read the two plain scalars in the pinned metadata's info block."""
    info = re.search(r'^info:\s*\n((?:[ \t].*\n)*)', raw.decode('utf-8-sig') + '\n', re.M)
    fields = dict(re.findall(r'^  (name|mini-swe-agent_version):[ \t]+(.+)$', info[1] if info else '', re.M))
    return fields['name'].strip().strip('\'"'), fields['mini-swe-agent_version'].strip().strip('\'"')


def _official(entry, cache):
    base = f'{EXPERIMENTS}/{entry}'
    metadata_url, results_url = base + '/metadata.yaml', base + '/per_instance_details.json'
    raw = cache.get(metadata_url)
    model, version = _mini_metadata(raw)
    outcomes, digest = fetch_json(cache, results_url)
    patch_base = f'{BUCKET}/{entry}/logs'
    submission_url = f'https://github.com/SWE-bench/experiments/tree/{EXPERIMENTS_PATH}/{entry}'
    provenance = dict(layout='multilingual-mini-v1', submission_url=submission_url, ref=EXPERIMENTS_COMMIT,
                      experiments_commit=EXPERIMENTS_COMMIT, prediction_url=patch_base, prediction_sha256=None,
                      metadata_url=metadata_url, metadata_sha256=hashlib.sha256(raw).hexdigest(),
                      results_url=results_url, results_sha256=digest, model=model, reported_model=model,
                      harness='mini-SWE-agent', harness_version=version)
    return outcomes, provenance


def _rusta(entry, directory, tarball):
    if directory is None:
        raise ValueError(f'{entry} requires --rusta-dir')
    if tarball is not None:
        with Path(tarball).open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != RUSTA_SHA256:
                raise ValueError('Rusta tarball SHA-256 mismatch')
    model_id, model = RUSTA_MODELS[entry]
    folder = entry.removeprefix('rusta-')
    root = Path(directory, folder)
    raw = (root / 'all_preds.jsonl').read_bytes()
    results = (root / 'results.json').read_bytes()
    predictions = {}
    for line in raw.decode('utf-8').split('\n'):
        if line.strip():
            prediction = json.loads(line)
            task = prediction['instance_id']
            if task in predictions:
                raise ValueError(f'{entry}: duplicate prediction for {task}')
            predictions[task] = prediction.get('model_patch')
    provenance = dict(layout='multilingual-rusta-v1', submission_url=RUSTA_URL, ref='swe-bench-multilingual',
                      release_sha256=RUSTA_SHA256, release_sha256_verified=tarball is not None,
                      prediction_url=f'{RUSTA_URL}#{folder}/all_preds.jsonl',
                      results_url=f'{RUSTA_URL}#{folder}/results.json',
                      prediction_sha256=hashlib.sha256(raw).hexdigest(), results_sha256=hashlib.sha256(results).hexdigest(),
                      model=model, reported_model=model_id, reasoning_effort='max', harness='Rusta',
                      harness_version='1.0.0', devscriptor_version='1.0.4')
    return json.loads(results), predictions, provenance


def load_submission(entry, cache, items, rusta_dir=None, rusta_tarball=None):
    """Use published evaluation outcomes and omit missing or empty patches from measurement."""
    if entry not in NAMES:
        raise ValueError(f'unknown Multilingual entry {entry!r}')
    rusta = entry in RUSTA_MODELS
    if rusta:
        outcomes, local_patches, provenance = _rusta(entry, rusta_dir, rusta_tarball)
    else:
        outcomes, provenance = _official(entry, cache)
    items = set(items)
    predictions, locations, evaluated, resolved, missing = {}, {}, set(), set(), []
    for item in sorted(items):
        task = item.removesuffix('#1')
        if task not in outcomes:
            continue
        evaluated.add(item)
        if outcomes[task].get('resolved') is True:
            resolved.add(item)
        if rusta:
            locations[item] = f"{provenance['prediction_url']}:instance_id={task}"
            patch = local_patches.get(task)
        else:
            locations[item] = f"{provenance['prediction_url']}/{task}/patch.diff"
            patch = fetch_patch(cache, locations[item])
        if patch and patch.strip():
            predictions[item] = patch
        else:
            missing.append(item)
    return dict(agent=PREFIX + entry, submission_url=provenance['submission_url'], predictions=predictions,
                prediction_locations=locations, resolved=resolved, evaluated=evaluated, provenance=provenance,
                result_details=dict(resolved=sorted(resolved), unresolved=sorted(evaluated - resolved),
                                    no_logs=sorted(items - evaluated), missing_patch=missing))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--cache', default='.parsimony-cache')
    commands = parser.add_subparsers(dest='command', required=True)
    data = commands.add_parser('dataset', help='import one language track from a Multilingual Parquet file')
    data.add_argument('parquet')
    data.add_argument('--language', choices=LANGUAGES, required=True)
    data.add_argument('--output', required=True)
    run = commands.add_parser('analyze', help='measure a Multilingual submission')
    run.add_argument('entry')
    run.add_argument('--dataset', required=True)
    run.add_argument('--output', required=True)
    run.add_argument('--rusta-dir', help='extracted release root containing deepseek/, glm/ and kimi/')
    run.add_argument('--rusta-tarball', help='optional release archive to verify against the pinned SHA-256')
    args = parser.parse_args()
    try:
        if args.command == 'dataset':
            records = dataset(args.parquet, args.language)
        else:
            rows = read_jsonl(args.dataset)
            if not rows or any(row.get('language') not in LANGUAGES for row in rows):
                raise ValueError('expected a nonempty Multilingual dataset of a supported track')
            cache = Cache(args.cache, timeout=90)
            submission = load_submission(args.entry, cache, {r['instance_id'] for r in rows},
                                         args.rusta_dir, args.rusta_tarball)
            digests = {r.get('dataset_file_sha256') for r in rows}
            if len(digests) == 1 and None not in digests:
                digest = next(iter(digests))
                submission['provenance']['dataset_file_sha256'] = digest
                if digest == DATASET_SHA256:
                    submission['provenance'].update(dataset_commit=DATASET_COMMIT, dataset_file_url=DATASET_URL)
            records = list(analyze_submission(submission, cache, rows, include_failed=True))
            for _ in range(3):  # Retry base file downloads for the affected tasks only.
                retry = {r['task_id'] for r in records if r['analysis_status'] == 'fetch_error'}
                if not retry:
                    break
                redone = {r['task_id']: r for r in analyze_submission(submission, cache, rows, task_ids=retry,
                                                                        include_failed=True) if r['task_id'] in retry}
                records = [redone.get(r['task_id'], r) for r in records]
        Path(args.output).write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
        print(f'Wrote {len(records)} {"items" if args.command == "dataset" else "records"} to {args.output}')
    except (OSError, ValueError, KeyError, http.client.HTTPException) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
