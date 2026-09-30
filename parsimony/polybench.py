"""Bounded, declared-candidate SWE-PolyBench Verified imports.

Inventory: python -m parsimony.polybench --cache /tmp/poly inventory \
    --run 20260422_iswe_agent --language python --output /tmp/run.json
Analyze (offline, no target execution): python -m parsimony.polybench \
    --cache /tmp/poly analyze /tmp/run.json --output /tmp/records.jsonl

Only the two audited submission candidates and the pinned Verified CSV are
supported. Inventory downloads all result bodies, including harness placeholders;
analysis retains the entire predefined language population, never a solved-only
subset. Exact joins are candidate bases, NOT historical-input verification.
Rights, historical generation/evaluator inputs and configuration homogeneity
remain unreviewed. This module does not build scores or publication artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError

from .artifacts import Cache
from .live import fetch_hf_rows

SUBMISSION_REVISION = 'e7062f4a848ca7775bc1c1313f7aa419bd6a3ec1'
DATASET_REVISION = 'b3fca77b637379f0c01ad86d18753a7ac1998b53'
REPOSITORY = 'amazon-science/SWE-PolyBench'
DATASET = 'AmazonScience/SWE-PolyBench_Verified'
RAW = f'https://raw.githubusercontent.com/{REPOSITORY}/{SUBMISSION_REVISION}'
COMMIT_URL = f'https://api.github.com/repos/{REPOSITORY}/git/commits/{SUBMISSION_REVISION}'
TREE_URL = f'https://api.github.com/repos/{REPOSITORY}/git/trees/{SUBMISSION_REVISION}?recursive=1'
LANGUAGE_COUNTS = {'python': 113, 'javascript': 100, 'typescript': 100, 'java': 69}
SUPPORTED_TRACKS = ('python', 'javascript', 'typescript')
RUNS = {
    '20260623_migbot_claude-opus-4-8': {
        'agent': 'HMigBot', 'model': 'claude-opus-4-8',
        'declared_languages': list(LANGUAGE_COUNTS),
        'selection_disclosure': (
            'Submitter reports 70 Feature + 312 complementary instances, 29 infrastructure '
            'empty-patch retries, five unconditional temporal-isolation replacements, '
            'then frozen-set re-evaluation after evaluator compatibility repairs. '
            'No independent history-isolation or trajectory audit performed.'),
    },
    '20260422_iswe_agent': {
        'agent': 'iSWE-Agent', 'model': 'iSWE-Agent-GPT-5.4',
        'declared_languages': ['python'],
        'selection_disclosure': (
            'Submitter declares the 113-task Verified Python subset; audited predictions '
            'contain 112 tasks, missing keras-team__keras-20002. README explains the '
            '2110-task full-harness output is not the submitted cohort. Pass@1 and '
            'restricted history access are submitter claims, not independently verified.'),
    },
}
ID = re.compile(r'^[A-Za-z0-9_][A-Za-z0-9_.-]*$')
REPO = re.compile(r'^[A-Za-z0-9_][A-Za-z0-9_.-]*/[A-Za-z0-9_][A-Za-z0-9_.-]*$')
SHA = re.compile(r'^[0-9a-f]{40}$')


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _checksum(value: dict) -> str:
    return _sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode())


def _id(value) -> str:
    if not isinstance(value, str) or not ID.fullmatch(value) or value in ('.', '..'):
        raise ValueError(f'unsafe or missing task ID: {value!r}')
    return value


def _object(raw: bytes) -> dict:
    # Duplicate JSON keys must not silently overwrite IDs/outcomes.
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    value = json.loads(raw, object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError('expected JSON object')
    return value


def _evidence(cache, url: str) -> tuple[bytes, dict]:
    raw = cache.get(url)
    return raw, dict(url=url, sha256=_sha(raw), bytes=len(raw), hash_scope='complete raw body')


def _result(raw: bytes, task_id: str, prediction: dict | None) -> dict:
    value = _object(raw)
    if value.get('instance_id') != task_id:
        raise ValueError(f'{task_id}: result instance_id mismatch')
    for key in ('generation', 'resolved'):
        if type(value.get(key)) is not bool:
            raise ValueError(f'{task_id}: result {key} must be boolean')
    for key in ('patch_applied', 'with_logs', 'all_f2p_passed', 'no_p2p_failed'):
        if key in value and type(value[key]) is not bool:
            raise ValueError(f'{task_id}: result {key} must be boolean')
    if value['resolved'] and any(value.get(key) is False for key in
                                 ('generation', 'patch_applied', 'with_logs',
                                  'all_f2p_passed', 'no_p2p_failed')):
        raise ValueError(f'{task_id}: contradictory resolved outcome')
    if prediction is None and (value['generation'] or value['resolved']):
        raise ValueError(f'{task_id}: generated result absent from predictions')
    if prediction and prediction['model_patch'] and not value['generation']:
        raise ValueError(f'{task_id}: nonempty prediction contradicts generation=false')
    # Test lists are diagnostic only. Even source-resolved rows can contain
    # unrelated failed tests; do not reconstruct correctness from test counts.
    return value


def import_run(cache: Cache, *, run_name: str, language: str = 'python') -> dict:
    """Fetch a complete candidate inventory, including non-submitted results."""
    if run_name not in RUNS:
        raise ValueError('unsupported run; only the two pinned candidates are supported')
    if language not in LANGUAGE_COUNTS:
        raise ValueError(f'unsupported inventory language: {language}')
    declaration = RUNS[run_name]
    prefix = f'evaluation/PBVerified/{run_name}'
    base = f'{RAW}/{prefix}'
    commit_bytes, commit_source = _evidence(cache, COMMIT_URL)
    commit = _object(commit_bytes)
    tree_metadata = commit.get('tree')
    tree_sha = tree_metadata.get('sha') if isinstance(tree_metadata, dict) else None
    if commit.get('sha') != SUBMISSION_REVISION or not isinstance(tree_sha, str) or not SHA.fullmatch(tree_sha):
        raise ValueError('submission commit verification failed')
    tree_bytes, tree_source = _evidence(cache, TREE_URL)
    tree = _object(tree_bytes)
    # GitHub accepts a commit as a tree-ish; the response can echo that commit
    # rather than the underlying tree object SHA. Both are immutable pins.
    if tree.get('sha') not in (tree_sha, SUBMISSION_REVISION) or tree.get('truncated') is not False:
        raise ValueError('submission tree revision mismatch or truncated inventory')
    entries = tree.get('tree')
    if not isinstance(entries, list):
        raise ValueError('submission tree must contain entries')
    paths = set()
    result_paths = {}
    for entry in entries:
        path = entry.get('path') if isinstance(entry, dict) else None
        if not isinstance(path, str) or path in paths:
            raise ValueError('missing or duplicate submission tree path')
        paths.add(path)
        if path.startswith(prefix + '/') and path.endswith('_result.json'):
            relative = path[len(prefix) + 1:]
            match = re.fullmatch(r'logs/([^/]+)_result\.json', relative)
            if not match or entry.get('type') != 'blob':
                raise ValueError(f'unsupported result layout: {path}')
            task_id = _id(match[1])
            if task_id in result_paths:
                raise ValueError(f'duplicate result ID: {task_id}')
            result_paths[task_id] = path
    tasks, dataset_source = fetch_hf_rows(cache, DATASET, DATASET_REVISION, 'test.csv')
    by_id = {}
    for row in tasks:
        task_id = _id(row.get('instance_id'))
        if task_id in by_id:
            raise ValueError(f'duplicate dataset task ID: {task_id}')
        repo, commit = row.get('repo'), row.get('base_commit')
        lang = str(row.get('language', '')).lower()
        if not isinstance(repo, str) or not REPO.fullmatch(repo) or '..' in repo.split('/'):
            raise ValueError(f'{task_id}: unsafe repository')
        if not isinstance(commit, str) or not SHA.fullmatch(commit):
            raise ValueError(f'{task_id}: base_commit must be a full SHA')
        if lang not in LANGUAGE_COUNTS:
            raise ValueError(f'{task_id}: unsupported dataset language')
        by_id[task_id] = dict(task_id=task_id, repo=repo, base_commit=commit, language=lang)
    if dict(Counter(r['language'] for r in by_id.values())) != LANGUAGE_COUNTS:
        raise ValueError('pinned dataset must contain the complete 382-task language population')
    pred_bytes, pred_source = _evidence(cache, base + '/all_preds.jsonl')
    predictions = {}
    for line in pred_bytes.splitlines():
        if not line.strip():
            continue
        value = _object(line)
        task_id = _id(value.get('instance_id'))
        if task_id in predictions:
            raise ValueError(f'duplicate prediction ID: {task_id}')
        if task_id not in by_id:
            raise ValueError(f'{task_id}: prediction absent from pinned dataset')
        if by_id[task_id]['language'] not in declaration['declared_languages']:
            raise ValueError(f'{task_id}: prediction outside declared cohort')
        if not isinstance(value.get('model_patch'), str):
            raise ValueError(f'{task_id}: prediction must contain string model_patch')
        if value.get('model_name_or_path') != declaration['model']:
            raise ValueError(f'{task_id}: prediction model label mismatch')
        for key in ('repo', 'base_commit'):
            if key in value and value[key] != by_id[task_id][key]:
                raise ValueError(f'{task_id}: prediction {key} mismatch')
        predictions[task_id] = value
    documents = {}
    for filename in ('README.md', 'metadata.yaml'):
        raw, source = _evidence(cache, base + '/' + filename)
        documents[filename] = dict(source=source, text=raw.decode('utf-8-sig'))
    if run_name == '20260623_migbot_claude-opus-4-8':
        raw, source = _evidence(cache, base + '/temporal_history_isolation_audit.json')
        documents['temporal_history_isolation_audit.json'] = dict(source=source, data=_object(raw))
    results = {}
    outside = []
    def fetch_result(item):
        task_id, path = item
        url = RAW + '/' + path
        try:
            raw, source = _evidence(cache, url)
        except HTTPError as exc:
            if exc.code != 404:
                raise
            exc.close()
            return task_id, dict(status='missing', source=dict(url=url, sha256=None))
        value = _result(raw, task_id, predictions.get(task_id))
        return task_id, dict(status='present', source=source, data=value)
    with ThreadPoolExecutor(max_workers=8) as pool:
        for task_id, result in pool.map(fetch_result, sorted(result_paths.items())):
            results[task_id] = result
            if task_id not in predictions:
                outside.append(dict(task_id=task_id, classification='non_submitted_placeholder', **result))
    records = []
    for task_id, meta in sorted(by_id.items()):
        prediction = predictions.get(task_id)
        patch = prediction['model_patch'] if prediction is not None else None
        result = results.get(task_id, dict(status='missing', source=dict(
            url=base + f'/logs/{task_id}_result.json', sha256=None)))
        value = result.get('data')
        outcome = 'unknown'
        if prediction is not None and value is not None:
            outcome = ('no_generation' if not value['generation'] else
                       'success' if value['resolved'] else 'failure')
        records.append(dict(
            **meta, submitted=prediction is not None, patch=patch,
            reported_model=prediction.get('model_name_or_path') if prediction else None,
            artifact_status='missing' if patch is None else 'empty_patch' if not patch else 'present',
            published_outcome=outcome, result=result,
            scope_status='supported' if meta['language'] in SUPPORTED_TRACKS else 'unsupported_language',
            provenance=dict(prediction_url=pred_source['url'], prediction_sha256=pred_source['sha256'],
                            prediction_location=pred_source['url'] + '#instance_id=' + task_id,
                            patch_sha256=_sha(patch.encode()) if patch is not None else None,
                            result_url=result['source']['url'], result_sha256=result['source']['sha256'])))
    run = dict(schema_version=1, benchmark='swe-polybench-verified', run_name=run_name,
               submission_revision=SUBMISSION_REVISION, dataset=dataset_source,
               provenance_status='declared-candidate', historical_dataset_match='unverified',
               historical_evaluator_match='unverified', rights_status='unreviewed-do-not-publish',
               configuration_homogeneity='unverified', declaration=dict(declaration),
               commit_source=commit_source, tree_source=tree_source,
               prediction_source=pred_source, documents=documents,
               language=language, population_ids=sorted(k for k, r in by_id.items() if r['language'] == language),
               dataset_task_count=len(by_id), submitted_task_count=len(predictions),
               listed_result_count=len(result_paths),
               non_submitted_results=outside,
               unavailable_result_ids=sorted(k for k, r in results.items() if r['status'] == 'missing'),
               records=records)
    run['inventory_sha256'] = _checksum(run)
    return run


class _OfflineSources:
    """Read existing Cache files directly; never call its network-backed get()."""
    def __init__(self, cache: Cache):
        self.directory = Path(cache.cache_dir)
        self.used = {}

    def get(self, url: str) -> bytes:
        try:
            raw = (self.directory / _sha(url.encode())).read_bytes()
        except OSError:
            self.used[url] = dict(url=url, sha256=None, status='unavailable_offline')
            raise
        self.used[url] = dict(url=url, sha256=_sha(raw), bytes=len(raw))
        return raw


def analyze_run(run: dict, cache: Cache, *, language: str | None = None) -> list[dict]:
    """Static full-file analysis of one whole track using ONLY cached base files.

    Populate exact raw GitHub base-file URLs in Cache beforehand. Cache misses
    remain fetch_error records, never zeros or inferred benchmark failures.
    No historical-verification claim or review override is accepted here.
    """
    language = language or run.get('language')
    if language not in SUPPORTED_TRACKS:
        raise ValueError(f'unsupported analysis track: {language}')
    if language != run.get('language'):
        raise ValueError('analysis track must match the inventoried population')
    if _checksum({k: v for k, v in run.items() if k != 'inventory_sha256'}) != run.get('inventory_sha256'):
        raise ValueError('inventory checksum mismatch; re-import rather than subset or edit records')
    if (run.get('run_name') not in RUNS or run.get('submission_revision') != SUBMISSION_REVISION
            or run.get('dataset', {}).get('revision') != DATASET_REVISION
            or run.get('provenance_status') != 'declared-candidate'
            or run.get('historical_dataset_match') != 'unverified'):
        raise ValueError('analysis requires the pinned declared-candidate inventory')
    selected = [r for r in run['records'] if r['language'] == language]
    if (len(selected) != LANGUAGE_COUNTS[language]
            or sorted(r['task_id'] for r in selected) != run['population_ids']
            or len(set(run['population_ids'])) != len(selected)):
        raise ValueError('analysis requires the complete predefined language population')
    from .benchmark import analyze_submission
    submission = dict(
        agent=run['declaration']['agent'],
        predictions={r['task_id']: r['patch'] for r in selected},
        resolved={r['task_id'] for r in selected if r['published_outcome'] == 'success'},
        evaluated={r['task_id'] for r in selected if r['published_outcome'] in ('success', 'failure')},
        result_details={key: [r['task_id'] for r in selected if r['published_outcome'] == outcome]
                        for key, outcome in (('resolved', 'success'), ('failed', 'failure'),
                                             ('no_generation', 'no_generation'))},
        provenance=dict(prediction_url=run['prediction_source']['url'],
                        benchmark=run['benchmark'], dataset=run['dataset'],
                        submission_revision=SUBMISSION_REVISION,
                        inventory_sha256=run['inventory_sha256'],
                        provenance_status='declared-candidate', historical_dataset_match='unverified',
                        historical_evaluator_match='unverified', rights_status=run['rights_status'],
                        selection_disclosure=run['declaration']['selection_disclosure'],
                        model_identity='submitter-label-not-independent-attestation',
                        failure_semantics='upstream-reported-not-attributed-to-patch',
                        documents={k: v['source'] for k, v in run['documents'].items()}))
    metadata = [dict(instance_id=r['task_id'], repo=r['repo'], base_commit=r['base_commit'],
                     language=language, patch='') for r in selected]
    sources = _OfflineSources(cache)
    by_id = {r['task_id']: r for r in selected}
    records = []
    for record in analyze_submission(submission, sources, metadata, include_failed=True):
        source = by_id[record['task_id']]
        result_data = source['result'].get('data', {})
        record.update(published_outcome=source['published_outcome'], submitted=source['submitted'],
                      artifact_status=source['artifact_status'], result_status=source['result']['status'],
                      harness_result_flags={key: result_data[key] for key in
                                            ('generation', 'resolved', 'patch_applied', 'with_logs',
                                             'all_f2p_passed', 'no_p2p_failed') if key in result_data})
        record['provenance'].update(source['provenance'], reported_model=source['reported_model'],
                                    base_sources=list(sources.used.values()),
                                    base_provenance_status='pinned-candidate-not-historically-verified')
        sources.used.clear()
        if source['artifact_status'] != 'present':
            record.update(metrics=None, analysis_status='missing_patch' if source['patch'] is None else 'empty_patch')
        elif source['published_outcome'] == 'unknown':
            record.update(metrics=None, analysis_status='unknown_outcome')
        records.append(record)
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', default='.parsimony-cache')
    commands = parser.add_subparsers(dest='command', required=True)
    inventory = commands.add_parser('inventory', help='fetch/cache full pinned run inventory')
    inventory.add_argument('--run', required=True, choices=RUNS)
    inventory.add_argument('--language', required=True, choices=LANGUAGE_COUNTS)
    inventory.add_argument('--output', required=True)
    analysis = commands.add_parser('analyze', help='offline static analysis, no scores')
    analysis.add_argument('inventory')
    analysis.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        cache = Cache(args.cache, timeout=90)
        if args.command == 'inventory':
            run = import_run(cache, run_name=args.run, language=args.language)
            text = json.dumps(run, sort_keys=True, indent=2) + '\n'
        else:
            run = json.loads(Path(args.inventory).read_text())
            text = ''.join(json.dumps(r, sort_keys=True) + '\n' for r in analyze_run(run, cache))
        Path(args.output).write_text(text)
        print(f'Wrote {args.output}; declared candidate, not publication-ready')
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
