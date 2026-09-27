"""Import DeepSWE runs (github.com/datacurve-ai/deep-swe): tasks, reference solutions and per-run patches.

DeepSWE runs every model with mini-swe-agent, four attempts per task, and publishes each run's
final patch and pass/fail. Parsimony treats each attempt as its own item, ``<task>#<attempt>``,
so one model has four items per task. Items of the same task share one reference pool (every
passing patch of the task, any attempt) and are resampled together (``cluster``).

    python -m parsimony.deepswe dataset CHECKOUT --output deepswe.jsonl
    python -m parsimony.deepswe configs --output configs.json
    python -m parsimony.deepswe analyze CONFIG --dataset deepswe.jsonl --output CONFIG.jsonl
    python -m parsimony.deepswe panel RECORDS... --name NAME --output score-panel.json
"""
import argparse
import hashlib
import http.client
import json
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path
from urllib.error import HTTPError

from .artifacts import Cache
from .benchmark import analyze_submission, read_jsonl
from .scoring import freeze, measured, metrics, out_of_scope

SITE = 'https://deepswe.datacurve.ai/artifacts'
RELEASE = 'v1.1'
ATTEMPTS = 4


EFFORTS = ('low', 'medium', 'high', 'xhigh', 'max', 'default')
VENDORS = {'claude': 'Claude', 'gpt': 'GPT', 'gemini': 'Gemini', 'glm': 'GLM', 'kimi': 'Kimi', 'grok': 'Grok',
           'deepseek': 'DeepSeek', 'qwen3': 'Qwen3', 'muse': 'Muse'}


def display_name(agent):
    """'deepswe-v1.1_mini_swe_agent_gpt_5_6_sol_max' -> 'GPT-5.6 Sol (max)'."""
    tokens = re.sub(r'^deepswe-v[\d.]+_mini_swe_agent_', '', agent).split('_')
    effort = tokens.pop() if tokens[-1] in EFFORTS else None
    words = []
    for token in tokens:
        if words and token.isdigit() and words[-1][-1].isdigit():
            words[-1] += '.' + token  # 5_6 -> 5.6, k2_7 -> K2.7, qwen3_8 -> Qwen3.8
        elif not words:
            words.append(VENDORS.get(token, token.capitalize()))
        else:
            words.append(token.upper() if re.fullmatch(r'[a-z]\d+', token) else token.capitalize())
    name = words[0] + ('-' + words[1] if words[0] in ('GPT', 'GLM') and len(words) > 1 else '')
    rest = words[2:] if words[0] in ('GPT', 'GLM') else words[1:]
    name = ' '.join([name, *rest])
    return f'{name} ({effort})' if effort and effort != 'default' else name


def cluster(item):
    """The task an item belongs to: attempts of one task are resampled together."""
    return item.split('#', 1)[0]


def read_tasks(checkout, language='python'):
    """Tasks of one language from a DeepSWE checkout: repository, base commit, reference solution."""
    out = []
    for toml in sorted(Path(checkout, 'tasks').glob('*/task.toml')):
        meta = tomllib.loads(toml.read_text())['metadata']
        if meta['language'] != language:
            continue
        match = re.fullmatch(r'https://github\.com/([^/]+/[^/]+?)(?:\.git)?/?', meta['repository_url'])
        if not match:
            raise ValueError(f'{toml}: repository is not on GitHub')
        solution = toml.parent / 'solution' / 'solution.patch'
        out.append(dict(task=meta['task_id'], repo=match.group(1), base_commit=meta['base_commit_hash'],
                        language=meta['language'], patch=blank_context(solution.read_text())))
    return out


def blank_context(patch):
    """Restore the space of blank context lines stripped from a few reference solutions.

    Within the line counts of a hunk header every line starts with ' ', '+', '-' or '\\'; an empty
    line there is a blank context line whose leading space was lost (git apply accepts it, a strict
    parser does not).
    """
    lines = patch.splitlines(keepends=True)
    old = new = 0
    for i, line in enumerate(lines):
        header = re.match(r'@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@', line)
        if header:
            old, new = (int(n) if n is not None else 1 for n in header.groups())
            continue
        if old <= 0 and new <= 0:
            continue
        if line in ('\n', '\r\n'):
            line = lines[i] = ' ' + line
        if line.startswith('\\'):
            continue
        old -= line[:1] in ' -'
        new -= line[:1] in ' +'
    return ''.join(lines)


def dataset_rows(tasks, attempts=ATTEMPTS):
    """One metadata row per item; the reference solution plays the role of the human patch."""
    return [dict(instance_id=f"{t['task']}#{k}", repo=t['repo'], base_commit=t['base_commit'],
                 language=t['language'], patch=t['patch'])
            for t in tasks for k in range(1, attempts + 1)]


def choose_configs(leaderboard, trials, available=lambda config: True):
    """Each model's best-scoring configuration among those with a patch for at least 95% of runs.

    ``available(config)`` checks that the configuration's patches can actually be downloaded.
    """
    runs, patched = defaultdict(int), defaultdict(int)
    for r in trials:
        runs[r['config']] += 1
        patched[r['config']] += bool(r['has_model_patch'])
    best = {}
    for row in leaderboard:
        config = row['config']
        if runs[config] and patched[config] >= 0.95 * runs[config]:
            if row['model'] not in best or row['pass_rate'] > best[row['model']]['pass_rate']:
                if available(config):
                    best[row['model']] = row
    return sorted((dict(model=r['model'], reasoning_effort=r['reasoning_effort'], config=r['config'],
                        pass_rate=r['pass_rate']) for r in best.values()), key=lambda r: -r['pass_rate'])


def attempts(trials, config, tasks):
    """{item: run} for one configuration; attempts are numbered by start time within each task."""
    by_task = defaultdict(list)
    for r in trials:
        if r['config'] == config and r['task_name'] in tasks:
            by_task[r['task_name']].append(r)
    items = {}
    for task, runs in by_task.items():
        runs.sort(key=lambda r: (r.get('started_at') or '', r['trial_name']))
        if len(runs) > ATTEMPTS:
            raise ValueError(f'{config}: {len(runs)} runs for {task}')
        for k, run in enumerate(runs, 1):
            items[f'{task}#{k}'] = run
    return items


def load_submission(config, trials, release, cache, task_names):
    """A submission in the shape ``benchmark.analyze_submission`` expects."""
    base = release['artifact_base_url'].rstrip('/')
    pattern = release['artifact_patterns']['model_patch']
    runs = attempts(trials, config, set(task_names))
    predictions, locations, resolved = {}, {}, set()
    unresolved, no_logs, missing = [], [], []
    for item, run in sorted(runs.items()):
        if run['outcome'] == 'pass':
            resolved.add(item)
        elif run['outcome'] == 'fail':
            unresolved.append(item)
        else:  # errored runs are excluded from DeepSWE's own score: outcome unknown
            no_logs.append(item)
            continue
        location = f"{base}/{pattern.replace('{trial_name}', run['trial_name'])}"
        locations[item] = location
        if not run['has_model_patch']:
            missing.append(item)
            continue
        patch = fetch_patch(cache, location)
        if patch is None:
            missing.append(item)
        else:
            predictions[item] = patch
    first = next(iter(runs.values()), {})
    return dict(agent=f'deepswe-{release["release_id"]}_{config}', submission_url=f'{SITE}/{release["release_id"]}',
                predictions=predictions, prediction_locations=locations, resolved=resolved,
                evaluated=set(runs), result_details=dict(resolved=sorted(resolved), unresolved=unresolved,
                                                         no_logs=no_logs, missing_patch=missing),
                provenance=dict(prediction_url=base, results_url=f'{SITE}/{release["release_id"]}/trials.json',
                                layout='deepswe-trials-v1', release_id=release['release_id'], config=config,
                                model=first.get('model'), reasoning_effort=first.get('reasoning_effort'),
                                harness=first.get('harness'), prediction_sha256=None, reported_model=first.get('model', ''),
                                trials_sha256=release.get('trials_sha256'), submission_url=f'{SITE}/{release["release_id"]}',
                                ref=release['release_id']))


def fetch_patch(cache, url, tries=4):
    """Patch text, or None when the file is not published (the CDN answers 403 or 404).

    Network errors are retried; persistent ones propagate so a run never silently loses patches.
    """
    for attempt in range(tries):
        try:
            return cache.get(url).decode('utf-8')
        except HTTPError as exc:
            exc.close()
            if exc.code in (403, 404):
                return None
            if attempt == tries - 1:
                raise
        except (OSError, http.client.HTTPException):
            if attempt == tries - 1:
                raise


def pooled_panel(records, name):
    """Freeze a panel whose items share their task's references across attempts.

    Every passing patch of a task, from any attempt, is a reference for each of that task's items.
    A reference is labelled ``<agent>#<attempt>``, so each is unique; the stability analysis strips
    the attempt, so leaving a model out removes all its attempts.
    Tasks without any measured, in-scope passing patch cannot calibrate footprint and are left out.
    """
    usable = {cluster(r['task_id']) for r in records
              if r['resolved'] and measured(r) and not out_of_scope(metrics(r['metrics']))}
    relabeled = [dict(r, agent=f"{r['agent']}#{r['task_id'].rsplit('#', 1)[1]}", task_id=cluster(r['task_id']))
                 for r in records if cluster(r['task_id']) in usable]
    pooled = freeze(relabeled, name)
    items = sorted({r['task_id'] for r in records})
    pooled['tasks'] = {item: pooled['tasks'][cluster(item)] for item in items if cluster(item) in pooled['tasks']}
    pooled['scope'] = 'fixed-cohort-sample-pooled-attempts'
    return pooled


def fetch_json(cache, url, tries=4):
    """Download (or read from the cache) one JSON artifact; large files are retried when cut off."""
    for attempt in range(tries):
        try:
            raw = cache.get(url)
            break
        except http.client.IncompleteRead:
            if attempt == tries - 1:
                raise
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--cache', default='.parsimony-cache')
    parser.add_argument('--release', default=RELEASE)
    commands = parser.add_subparsers(dest='command', required=True)
    data = commands.add_parser('dataset', help='item metadata from a DeepSWE checkout')
    data.add_argument('checkout')
    data.add_argument('--language', default='python')
    data.add_argument('--output', required=True)
    conf = commands.add_parser('configs', help="each model's best configuration with published patches")
    conf.add_argument('--output', required=True)
    run = commands.add_parser('analyze', help='measure one configuration')
    run.add_argument('config')
    run.add_argument('--dataset', required=True)
    run.add_argument('--output', required=True)
    make = commands.add_parser('panel', help='freeze a panel pooling references across attempts')
    make.add_argument('records', nargs='+')
    make.add_argument('--name', required=True)
    make.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        cache = Cache(args.cache, timeout=90)
        if args.command == 'dataset':
            rows = dataset_rows(read_tasks(args.checkout, args.language))
            Path(args.output).write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in rows))
            print(f'Wrote {len(rows)} items ({len(rows) // ATTEMPTS} tasks) to {args.output}')
        elif args.command == 'configs':
            trials, _ = fetch_json(cache, f'{SITE}/{args.release}/trials.json')
            board, _ = fetch_json(cache, f'{SITE}/{args.release}/leaderboard-live.json')
            release, _ = fetch_json(cache, f'{SITE}/{args.release}/release.json')
            base = release['artifact_base_url'].rstrip('/')
            pattern = release['artifact_patterns']['model_patch']
            def available(config):  # probe the first published patch of the configuration
                run = next((r for r in trials['rows'] if r['config'] == config and r['has_model_patch']), None)
                return run is not None and fetch_patch(
                    cache, f"{base}/{pattern.replace('{trial_name}', run['trial_name'])}") is not None
            chosen = choose_configs(board['rows'], trials['rows'], available)
            Path(args.output).write_text(json.dumps(chosen, indent=1) + '\n')
            print(f'Wrote {len(chosen)} configurations to {args.output}')
        elif args.command == 'analyze':
            release, release_sha = fetch_json(cache, f'{SITE}/{args.release}/release.json')
            trials, trials_sha = fetch_json(cache, f'{SITE}/{args.release}/trials.json')
            release = dict(release, trials_sha256=trials_sha, release_sha256=release_sha)
            dataset = read_jsonl(args.dataset)
            submission = load_submission(args.config, trials['rows'], release, cache,
                                         {cluster(r['instance_id']) for r in dataset})
            records = list(analyze_submission(submission, cache, dataset, include_failed=True))
            for _ in range(3):  # base files that failed to download: retry those items only
                retry = {r['task_id'] for r in records if r['analysis_status'] == 'fetch_error'}
                if not retry:
                    break
                redone = {r['task_id']: r for r in analyze_submission(submission, cache, dataset, task_ids=retry,
                                                                        include_failed=True) if r['task_id'] in retry}
                records = [redone.get(r['task_id'], r) for r in records]
            Path(args.output).write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
            print(f'Wrote {len(records)} records to {args.output}')
        else:
            records = [r for path in args.records for r in read_jsonl(path)]
            result = pooled_panel(records, args.name)
            result['source_sha256'] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in args.records}
            with Path(args.output).open('x') as stream:
                stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
            print(f'Wrote {args.output} ({len(result["tasks"])} items)')
    except (OSError, ValueError, KeyError, http.client.HTTPException) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
