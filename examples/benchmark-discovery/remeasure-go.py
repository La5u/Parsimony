#!/usr/bin/env python3
"""Prepare frozen DeepSWE Go inputs; measure only in an explicitly pinned clean checkout.

prepare --repo REPO --root /tmp/parsimony-go-v2-release
verify  --root ROOT [--download]  # restore only inventory-bound URL bytes
measure --root ROOT --worktree CLEAN --commit FULL_SHA --source-sha256 HASH
        --track-json PINNED_TRACK.json --version VERSION --name NEW_RELEASE_NAME

Run measure with the supplied worktree's Python 3.14.7. No target code is executed.
Raw artifacts and scalar outputs remain external; nothing is published. Preparation
uses pinned trials bytes (not outcome inference) and preserves old unavailable slots.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import subprocess
import sys
import tarfile
import threading
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

TASK_COMMIT = '0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea'
DATASET_SHA = 'ea57379e61ffbe05423d03c829f13b4ae89ebe28c1b0da85c2a48fd29f52413d'
TRIALS_SHA = '310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6'
OLD_COMMIT = '7705e8de13343bbafbfe5bccba665dd2bab8b24a'
OLD_SOURCE = '3c7a31f7b62de1f7b786ed8b20e1f49bc41e85069c0783cde41fc8bfae5cdd93'
TRIALS_URL = 'https://deepswe.datacurve.ai/artifacts/v1.1/trials.json'
TASK_URL = f'https://codeload.github.com/datacurve-ai/deep-swe/tar.gz/{TASK_COMMIT}'
LOCK = threading.Lock()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dump(path, value):
    data = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    immutable(path, data)


def immutable(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        require(path.read_bytes() == data, f'refusing changed input/output: {path}')
    else:
        with path.open('xb') as stream:
            stream.write(data)


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_bytes().splitlines() if line.strip()]


def modules(repo):
    sys.path.insert(0, str(repo))
    from parsimony.artifacts import Cache
    from parsimony.deepswe import read_tasks, dataset_rows, attempts
    return Cache, read_tasks, dataset_rows, attempts


def cache_class(base):
    class BoundCache(base):
        def __init__(self, root, offline=False):
            super().__init__(root / 'cache', timeout=60)
            self.root, self.offline = root, offline

        def get(self, url, expected=None, bound=16 * 1024 * 1024):
            target = self.cache_dir / digest(url.encode())
            if target.exists():
                data = target.read_bytes()
            else:
                require(not self.offline, f'offline cache miss: {url}')
                for attempt in range(3):
                    started = time.monotonic()
                    try:
                        request = Request(url, headers={'User-Agent': 'parsimony-go-release-prep/1'})
                        with urlopen(request, timeout=self.timeout) as response:
                            length = response.headers.get('Content-Length')
                            require(not length or int(length) <= bound, f'oversized response: {url}')
                            chunks, size = [], 0
                            while True:
                                require(time.monotonic() - started < 180, f'download deadline: {url}')
                                chunk = response.read(min(65536, bound + 1 - size))
                                if not chunk:
                                    break
                                size += len(chunk)
                                require(size <= bound, f'download bound: {url}')
                                chunks.append(chunk)
                            data = b''.join(chunks)
                        break
                    except Exception as exc:
                        with LOCK, (self.root / 'download-log.jsonl').open('a') as log:
                            log.write(json.dumps({'url': url, 'attempt': attempt + 1, 'error': str(exc)}) + '\n')
                        if attempt == 2:
                            raise
                        time.sleep(attempt + 1)
                require(expected is None or digest(data) == expected, f'download hash mismatch: {url}')
                immutable(target, data)
                with LOCK, (self.root / 'download-log.jsonl').open('a') as log:
                    log.write(json.dumps({'url': url, 'bytes': len(data), 'sha256': digest(data)}) + '\n')
            require(len(data) <= bound, f'cache exceeds bound: {url}')
            require(expected is None or digest(data) == expected, f'cache hash mismatch: {url}')
            return data
    return BoundCache


def external(root, repo):
    require(not root.is_relative_to(repo), 'cache/output must be outside checkout')


def touched(patch):
    """Inventory all text AND metadata-only paths, independent of analyzer scope."""
    entries = []
    blocks = re.split(r'(?m)^diff --git ', patch)
    for block in blocks[1:] or blocks:
        git = block.splitlines()[0].split() if blocks[1:] else []
        old = re.search(r'(?m)^--- ([^\n]+)', block)
        new = re.search(r'(?m)^\+\+\+ ([^\n]+)', block)
        if old and new:
            paths = [old[1].split('\t')[0].strip(), new[1].split('\t')[0].strip()]
        elif len(git) == 2:
            paths = git
        else:
            require(not block.strip(), 'cannot inventory patch paths')
            continue
        normalized = []
        for path in paths:
            if path.startswith(('a/', 'b/')):
                path = path[2:]
            require(path == '/dev/null' or (not path.startswith('/') and '..' not in PurePosixPath(path).parts
                    and not any(c in path for c in ('"', '\\', ' '))), f'unsafe/unsupported path: {path}')
            normalized.append(path)
        entries.append({'old': normalized[0], 'new': normalized[1]})
    return entries


def old_records(root):
    return {p.name: jsonl(p) for p in sorted((root / 'old').glob('*.jsonl'))}


def prepare(args):
    repo, root = args.repo.resolve(), args.root.resolve()
    external(root, repo)
    root.mkdir(parents=True, exist_ok=True)
    Cache, read_tasks, dataset_rows, attempts = modules(repo)
    cache = cache_class(Cache)(root)
    source = repo / 'examples/deepswe-go'
    for path in sorted(source.iterdir()):
        if path.suffix in {'.json', '.jsonl'}:
            immutable(root / 'old' / path.name, path.read_bytes())
    old = old_records(root)
    pop = json.loads((root / 'old/population.json').read_bytes())
    require(len(old) == 26 and pop['task_count'] == 136 and pop['dataset_sha256'] == DATASET_SHA,
            'wrong frozen cohort')
    bindings = []
    for name, rows in old.items():
        require(len(rows) == 136 and {r['task_id'] for r in rows} == set(pop['tasks']), f'membership: {name}')
        raw_lines = (root / 'old' / name).read_bytes().splitlines(keepends=True)
        for n, (r, line) in enumerate(zip(rows, raw_lines), 1):
            require(r['analyzer_commit'] == OLD_COMMIT and r['analyzer_source_sha256'] == OLD_SOURCE
                    and r['python_version'] == '3.14.7', 'old analyzer identity differs')
            require({k: r['provenance'][k] for k in ('repo', 'base_commit')} == pop['tasks'][r['task_id']], 'old base differs')
            require(r['provenance']['trials_sha256'] == TRIALS_SHA, 'old trials binding differs')
            bindings.append({'file': name, 'line': n, 'line_sha256': digest(line), 'agent': r['agent'],
                             'task_id': r['task_id'], 'provenance': r['provenance'],
                             'resolved': r['resolved'], 'categories': r['published_result_categories'],
                             'evaluation_result': r['evaluation_result']})
    dump(root / 'old-record-bindings.json', bindings)
    with ThreadPoolExecutor(max_workers=2) as pool:
        task_future = pool.submit(cache.get, TASK_URL, None, 128 * 1024 * 1024)
        trial_future = pool.submit(cache.get, TRIALS_URL, TRIALS_SHA, 64 * 1024 * 1024)
        archive, trials_raw = task_future.result(), trial_future.result()
    task_inventory = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
        for member in tar.getmembers():
            relative = PurePosixPath(*PurePosixPath(member.name).parts[1:])
            if not (str(relative).startswith('tasks/') and
                    (relative.name == 'task.toml' or str(relative).endswith('/solution/solution.patch'))):
                continue
            require(member.isfile() and '..' not in relative.parts and not relative.is_absolute()
                    and member.size <= 16 * 1024 * 1024, 'unsafe task archive member')
            data = tar.extractfile(member).read()
            immutable(root / 'upstream-tasks' / str(relative), data)
            task_inventory.append({'path': str(relative), 'sha256': digest(data), 'bytes': len(data)})
    dataset = dataset_rows(read_tasks(root / 'upstream-tasks', 'go'))
    dataset_raw = ''.join(json.dumps(r, sort_keys=True) + '\n' for r in dataset).encode()
    require(digest(dataset_raw) == DATASET_SHA, 'dataset not byte-identical to frozen population')
    immutable(root / 'dataset.jsonl', dataset_raw)
    metadata = {r['instance_id']: r for r in dataset}
    require({k: {field: v[field] for field in ('repo', 'base_commit')} for k, v in metadata.items()} == pop['tasks'],
            'dataset population differs')
    trials = json.loads(trials_raw)['rows']
    patch_jobs, memberships = {}, []
    for name, rows in old.items():
        config = rows[0]['provenance']['config']
        require(all(r['provenance']['config'] == config and r['agent'] == rows[0]['agent'] for r in rows), 'mixed config')
        runs = attempts(trials, config, {k.split('#')[0] for k in metadata})
        for r in rows:
            task, prov = r['task_id'], r['provenance']
            run = runs.get(task)
            if run is None:
                require(r['evaluation_result'] == 'unknown' and not r['published_result_categories']
                        and prov['patch_sha256'] is None, 'absent run not unknown')
            else:
                expected = {'pass': 'resolved', 'fail': 'failed'}.get(run['outcome'], 'no_logs')
                require(r['evaluation_result'] == expected, 'pinned upstream outcome differs')
                for field in ('model', 'reasoning_effort', 'harness'):
                    require(prov[field] == run[field], f'upstream attribution differs: {field}')
                if expected != 'no_logs':
                    require(f"/{run['trial_name']}/artifacts/model.patch" in prov['patch_location'], 'trial/patch URL differs')
                memberships.append({'file': name, 'task_id': task, 'trial': run})
            require(prov['reference_patch_sha256'] == digest(metadata[task]['patch'].encode()), 'reference hash differs')
            if prov['patch_sha256'] is not None:
                require(run and run['has_model_patch'], 'old patch not declared upstream')
                url = prov['patch_location']
                require(url not in patch_jobs or patch_jobs[url] == prov['patch_sha256'], 'URL hash conflict')
                patch_jobs[url] = prov['patch_sha256']
    dump(root / 'pinned-trial-memberships.json', memberships)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(lambda job: cache.get(job[0], job[1]), sorted(patch_jobs.items())))
    print(f'Patches validated: {len(patch_jobs)}', flush=True)
    base_jobs, touched_inventory = {}, []
    for name, rows in old.items():
        for r in rows:
            prov, task = r['provenance'], r['task_id']
            patches = [('reference', metadata[task]['patch'])]
            if prov['patch_sha256'] is not None:
                patches.append(('model', cache.get(prov['patch_location'], prov['patch_sha256']).decode('utf-8')))
            for kind, patch in patches:
                for entry in touched(patch):
                    url = None if entry['old'] == '/dev/null' else (
                        f"https://raw.githubusercontent.com/{prov['repo']}/{prov['base_commit']}/{quote(entry['old'], safe='/')}")
                    if url:
                        base_jobs[url] = True
                    touched_inventory.append({'file': name, 'task_id': task, 'kind': kind, **entry, 'base_url': url})
    dump(root / 'touched-files.json', touched_inventory)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(cache.get, sorted(base_jobs)))
    urls = [(TASK_URL, 128 * 1024 * 1024), (TRIALS_URL, 64 * 1024 * 1024)]
    urls += [(url, 16 * 1024 * 1024) for url in sorted(set(patch_jobs) | set(base_jobs))]
    inventory = [{'url': url, 'sha256': digest(cache.get(url, bound=bound)),
                  'bytes': len(cache.get(url, bound=bound)), 'bound': bound} for url, bound in urls]
    dump(root / 'download-inventory.json', inventory)
    dump(root / 'upstream-task-inventory.json', {'commit': TASK_COMMIT, 'archive_url': TASK_URL,
         'archive_sha256': digest(archive), 'members': task_inventory, 'dataset_sha256': DATASET_SHA})
    summary = {'state': 'prepared-not-measured-not-published', 'outcomes_source': 'exact pinned trials bytes; no reconstruction',
               'configs': len(old), 'records': len(bindings), 'attempts_per_config': 136, 'tasks': 34,
               'patches': len(patch_jobs), 'base_files_all_scopes': len(base_jobs),
               'touched_entries_with_repeated_reference_memberships': len(touched_inventory),
               'absent_before_sides': sum(e['base_url'] is None for e in touched_inventory),
               'statuses': dict(Counter(r['analysis_status'] for rows in old.values() for r in rows)),
               'outcomes': dict(Counter(r['evaluation_result'] for rows in old.values() for r in rows)),
               'inventory_bytes': sum(e['bytes'] for e in inventory), 'dataset_sha256': DATASET_SHA,
               'trial_sha256': TRIALS_SHA, 'upstream_archive_sha256': digest(archive),
               'workers': args.workers, 'request_timeout_seconds': 60, 'request_deadline_seconds': 180,
               'max_attempts': 3, 'artifact_bound_bytes': 16 * 1024 * 1024}
    dump(root / 'preparation-summary.json', summary)
    files = {str(p.relative_to(root)): digest(p.read_bytes()) for directory in ('old', 'upstream-tasks')
             for p in sorted((root / directory).rglob('*')) if p.is_file()}
    for name in ('dataset.jsonl', 'old-record-bindings.json', 'pinned-trial-memberships.json', 'touched-files.json',
                 'download-inventory.json', 'upstream-task-inventory.json', 'preparation-summary.json'):
        files[name] = digest((root / name).read_bytes())
    dump(root / 'prepared.json', {'format': 'parsimony-go-prepared-v1', 'files': files,
         'driver_sha256': digest(Path(__file__).read_bytes())})
    print(json.dumps(summary, indent=2), flush=True)


def verify(args, repo=None):
    root = args.root.resolve()
    manifest = json.loads((root / 'prepared.json').read_bytes())
    require(manifest['format'] == 'parsimony-go-prepared-v1', 'wrong prepared format')
    require(digest(Path(__file__).read_bytes()) == manifest['driver_sha256'], 'driver changed since preparation')
    for name, sha in manifest['files'].items():
        path = root / name
        require(path.resolve().is_relative_to(root) and digest(path.read_bytes()) == sha, f'input hash mismatch: {name}')
    inventory = json.loads((root / 'download-inventory.json').read_bytes())
    if args.download:
        Cache, *_ = modules(repo or args.repo.resolve())
        cache = cache_class(Cache)(root)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(lambda e: cache.get(e['url'], e['sha256'], e['bound']), inventory))
    for entry in inventory:
        data = (root / 'cache' / digest(entry['url'].encode())).read_bytes()
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], f'cached hash mismatch: {entry["url"]}')
    require(digest((root / 'dataset.jsonl').read_bytes()) == DATASET_SHA, 'dataset checksum')
    return manifest


def differences(old, new, prefix=''):
    if isinstance(old, dict) and isinstance(new, dict):
        result = {}
        for key in sorted(set(old) | set(new)):
            path = f'{prefix}.{key}' if prefix else key
            if key not in old or key not in new:
                result[path] = {'old_present': key in old, 'new_present': key in new,
                                'old': old.get(key), 'new': new.get(key)}
            else:
                result.update(differences(old[key], new[key], path))
        return result
    return {} if old == new else {prefix: {'old': old, 'new': new}}


def measure(args):
    require(platform.python_version() == '3.14.7', 'measurement requires Python 3.14.7')
    root, repo = args.root.resolve(), args.worktree.resolve()
    external(root, repo)
    require(re.fullmatch('[0-9a-f]{40}', args.commit) is not None, 'full analyzer commit required')
    def git(*options):
        return subprocess.check_output(['git', '-C', str(repo), *options], text=True).strip()
    require(git('rev-parse', '--show-toplevel') == str(repo), 'worktree must be checkout root')
    require(git('rev-parse', 'HEAD') == args.commit and not git('status', '--porcelain', '--untracked-files=all'),
            'dirty or wrong analyzer checkout; commit analyzer before measuring')
    require(args.commit != OLD_COMMIT and args.source_sha256 != OLD_SOURCE, 'refusing old analyzer relabel')
    Cache, *_ = modules(repo)
    import parsimony.benchmark as benchmark
    from parsimony.languages import track
    from parsimony.release import freeze_dataset, audit
    from parsimony.deepswe import pooled_panel
    require(Path(benchmark.__file__).resolve().is_relative_to(repo), 'imported wrong analyzer')
    require(benchmark.analyzer_identity() == (args.commit, args.source_sha256), 'analyzer source identity differs')
    require(benchmark.ANALYZER_VERSION == args.version and args.version != '0.6.0-beta', 'wrong analyzer version')
    expected_track = json.loads(args.track_json.read_bytes())
    require(expected_track.get('language') == 'go' and track('go') == expected_track, 'wrong Go track/parser pins')
    args.download = False
    prepared = verify(args, repo)
    require(re.fullmatch('[a-zA-Z0-9._-]+', args.name) is not None, 'unsafe versioned release name')
    output = root / 'releases' / args.name
    require(not output.exists(), 'release output already exists; never resume/mix analyzer identities')
    output.mkdir(parents=True)
    cache = cache_class(Cache)(root, offline=True)
    dataset = jsonl(root / 'dataset.jsonl')
    old = old_records(root)
    all_records, comparison = [], []
    invariant_keys = ('agent', 'task_id', 'resolved', 'published_result_categories', 'evaluation_result',
                      'published_resolved_count', 'benchmark_tasks', 'resolve_rate', 'provenance')
    for name, rows in old.items():
        first = rows[0]
        provenance = {k: v for k, v in first['provenance'].items() if k not in
                      {'instance_id', 'patch_location', 'patch_sha256', 'patch_final_newline_restored',
                       'repo', 'base_commit', 'reference_patch_sha256'}}
        predictions, locations = {}, {}
        categories = {}
        for r in rows:
            p = r['provenance']
            locations[r['task_id']] = p['patch_location']
            if p['patch_sha256'] is not None:
                predictions[r['task_id']] = cache.get(p['patch_location'], p['patch_sha256']).decode('utf-8')
            for category in r['published_result_categories']:
                categories.setdefault(category, []).append(r['task_id'])
        submission = dict(agent=first['agent'], submission_url=provenance['submission_url'], predictions=predictions,
                          prediction_locations=locations, resolved={r['task_id'] for r in rows if r['resolved']},
                          evaluated={r['task_id'] for r in rows if r['evaluation_result'] != 'unknown'},
                          result_details=categories, provenance=provenance)
        records = list(benchmark.analyze_submission(submission, cache, dataset, include_failed=True))
        require(len(records) == 136 and {r['task_id'] for r in records} == {r['task_id'] for r in rows}, 'lost slots')
        before = {r['task_id']: r for r in rows}
        for r in records:
            previous = before[r['task_id']]
            for key in invariant_keys:
                # Categories are a membership set; the original order is retained in the new record.
                if key == 'published_result_categories':
                    require(set(previous[key]) == set(r[key]), 'outcome membership changed')
                    r[key] = previous[key]
                else:
                    require(r[key] == previous[key], f'original binding changed: {key} / {name} / {r["task_id"]}')
            require(r['analyzer_commit'] == args.commit and r['analyzer_source_sha256'] == args.source_sha256
                    and r['measurement_track'] == expected_track, 'record identity differs')
            comparison.append({'file': name, 'task_id': r['task_id'], 'agent': r['agent'],
                               'differences': differences(previous, r), 'bindings_unchanged': True})
        immutable(output / name, ''.join(json.dumps(r, sort_keys=True, allow_nan=False) + '\n' for r in records).encode())
        all_records.extend(records)
        print(f'{name}: {dict(Counter(r["analysis_status"] for r in records))}', flush=True)
    population = freeze_dataset(root / 'dataset.jsonl', args.name, args.commit)
    dump(output / 'population.json', population)
    dump(output / 'coverage.json', audit(population, all_records, root / 'dataset.jsonl'))
    panel = pooled_panel(all_records, args.name + '-pooled-archived-80-20')
    panel['source_sha256'] = {name: digest((output / name).read_bytes()) for name in old}
    dump(output / 'score-panel.json', panel)
    dump(output / 'record-comparison.json', comparison)
    from parsimony.scoring import measured, metrics, out_of_scope
    def summary(records):
        eligible = [r for r in records if measured(r) and not out_of_scope(metrics(r['metrics']))]
        solved = [r for r in eligible if r['resolved']]
        return {'statuses': dict(Counter(r['analysis_status'] for r in records)),
                'eligible': len(eligible), 'population': len(records),
                'measured_net_mean': sum(r['metrics']['net_units'] for r in eligible) / len(eligible) if eligible else None,
                'measured_solved_net_mean': sum(r['metrics']['net_units'] for r in solved) / len(solved) if solved else None,
                'outcomes': dict(Counter(r['evaluation_result'] for r in records)),
                'errors': [{'task_id': r['task_id'], 'analysis_error': r.get('analysis_error'),
                            'human_error': r.get('human_error')} for r in records
                           if r.get('analysis_error') or r.get('human_error')]}
    dump(output / 'comparison-summary.json', {name: {'old': summary(rows), 'new': summary(jsonl(output / name))}
                                               for name, rows in old.items()})
    require(not git('status', '--porcelain', '--untracked-files=all') and git('rev-parse', 'HEAD') == args.commit,
            'checkout changed during measurement')
    dump(output / 'release-manifest.json', {'state': 'measured-not-published', 'prepared_sha256': digest((root / 'prepared.json').read_bytes()),
         'prepared': prepared, 'analyzer_commit': args.commit, 'analyzer_source_sha256': args.source_sha256,
         'analyzer_version': args.version, 'python_version': platform.python_version(), 'track': expected_track,
         'python_executable': sys.executable, 'driver_sha256': digest(Path(__file__).read_bytes()),
         'files': {p.name: digest(p.read_bytes()) for p in sorted(output.iterdir()) if p.is_file()}})
    print(f'Complete external versioned release: {output}; publication and archived diagnostics review still required.')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('prepare', 'verify', 'measure'):
        p = sub.add_parser(command)
        p.add_argument('--root', type=Path, default=Path('/tmp/parsimony-go-v2-release'))
        p.add_argument('--workers', type=int, default=8)
        if command in ('prepare', 'verify'):
            p.add_argument('--repo', type=Path, default=Path.cwd())
        if command == 'verify':
            p.add_argument('--download', action='store_true')
        if command == 'measure':
            p.add_argument('--worktree', type=Path, required=True)
            p.add_argument('--commit', required=True)
            p.add_argument('--source-sha256', required=True)
            p.add_argument('--track-json', type=Path, required=True)
            p.add_argument('--version', required=True)
            p.add_argument('--name', required=True)
    args = parser.parse_args()
    require(1 <= args.workers <= 8, 'workers must be between 1 and 8')
    if args.command == 'prepare':
        prepare(args)
    elif args.command == 'verify':
        verify(args)
        print('All prepared file and URL hashes verified.')
    else:
        measure(args)


if __name__ == '__main__':
    main()
