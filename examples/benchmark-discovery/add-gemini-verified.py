#!/usr/bin/env python3
"""Inventory pinned Gemini Verified artifacts, then measure in a clean analyzer checkout.

Run inventory with the current importer; run measure with --analyzer-checkout pointing
at an existing clean 0aa66df checkout, using Python 3.14.7. Use one fresh external
output folder for both phases. Raw predictions/cache stay external; nothing is
published by this script.
Metadata contains only repo/base from the existing 500-record cohort: human
comparison is intentionally not computed (no reference hashes are copied).
Historical evaluator certification and redistribution rights remain unverified.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
SUBMISSION_REVISION = '40f164d5b8f1d249bf95a6df8b74b577fd8e519d'
ARTIFACT_REVISION = '2f6637a2557da1f7b5f2b583ab7090a077bbeed2'
ANALYZER_COMMIT = '0aa66dfb6dca76893b0f20e22233317965ff0d25'
PYTHON_VERSION = '3.14.7'
NAME = '20260901_mini-v2.4.2_gemini-3-5-flash'
BASE = f'https://raw.githubusercontent.com/SWE-bench/experiments/{SUBMISSION_REVISION}/evaluation/verified/{NAME}'
SUBMISSION_URL = f'https://github.com/SWE-bench/experiments/tree/{SUBMISSION_REVISION}/evaluation/verified/{NAME}'
METADATA_SOURCE = 'examples/mini-swe-agent-500/claude-4-6-opus.jsonl'
FILES = ('inventory.json', 'dataset.json', 'evidence.json')
COUNTS = dict(population=500, resolved=359, failed=82, no_generation=59,
              separate_patches_agree=441)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode('utf-8')


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def external_root(path, checkout=None):
    """Resolve symlinks before any mkdir, cache creation, or output write."""
    root = Path(path).resolve()
    protected = [REPO.resolve()]
    if checkout is not None:
        protected.append(Path(checkout).resolve())
    for target in [root, root / 'cache', *(root / f for f in (*FILES, 'manifest.json', 'measurements.jsonl'))]:
        target = target.resolve()
        require(not any(target == p or p in target.parents for p in protected),
                'outputs/cache must be external to source and analyzer checkouts')
        require(target == root or root in target.parents, 'output/cache symlink escapes external folder')
        ancestor = target
        while not ancestor.is_dir() and ancestor != ancestor.parent:
            ancestor = ancestor.parent
        probe = subprocess.run(['git', '-C', str(ancestor), 'rev-parse', '--show-toplevel'],
                               capture_output=True, text=True)
        require(probe.returncode != 0, 'outputs/cache must not be inside a Git checkout')
    # An existing cache could hide a symlink into a checkout behind a URL hash.
    if (root / 'cache').exists():
        require(not any(p.is_symlink() for p in (root / 'cache').rglob('*')),
                'cache must not contain symlinks')
    return root


def id_set(values, label):
    require(isinstance(values, (list, set)), f'{label} must be a list/set of IDs')
    require(all(isinstance(t, str) and t for t in values), f'{label} requires string IDs')
    require(len(values) == len(set(values)), f'{label} has duplicate IDs')
    return set(values)


def dataset_from_records(records):
    require(isinstance(records, list) and len(records) == 500, 'expected 500 metadata records')
    ids = id_set([r['task_id'] for r in records], 'metadata population')
    dataset = []
    for row in records:
        provenance = row['provenance']
        repo, base = provenance['repo'], provenance['base_commit']
        require(isinstance(repo, str) and re.fullmatch(r'[^/\s]+/[^/\s]+', repo), 'invalid repo')
        require(isinstance(base, str) and re.fullmatch(r'[0-9a-f]{40}', base), 'invalid base commit')
        dataset.append(dict(instance_id=row['task_id'], repo=repo, base_commit=base))
    require(len(ids) == 500, 'expected 500 unique metadata IDs')
    return sorted(dataset, key=lambda r: r['instance_id'])


def outcomes(details, aggregate, population):
    require(isinstance(details, dict) and len(details) == 441, 'expected 441 evaluated details')
    require(all(isinstance(t, str) and t and isinstance(r, dict) and
                type(r.get('resolved')) is bool for t, r in details.items()),
            'per-instance resolved must be an exact boolean')
    require(isinstance(aggregate, dict), 'aggregate must be an object')
    resolved = {t for t, r in details.items() if r['resolved']}
    failed = set(details) - resolved
    ng = id_set(aggregate.get('no_generation'), 'no_generation')
    require(len(ng) == 59 and not set(details) & ng and set(details) | ng == population,
            '441 evaluated + 59 disjoint explicit no_generation must cover the 500 IDs')
    require(len(resolved) == 359 and len(failed) == 82 and
            id_set(aggregate.get('resolved'), 'aggregate resolved') == resolved,
            'conflicting aggregate/per-instance resolved outcomes')
    for category in ('unresolved', 'failed', 'not_resolved'):
        if category in aggregate:
            require(id_set(aggregate[category], category) == failed, 'conflicting explicit failures')
    for category in ('no_logs', 'unknown', 'no_submission'):
        if category in aggregate:
            require(not id_set(aggregate[category], category), 'conflicting aggregate outcomes')
    return resolved, failed, ng


def pinned(provenance):
    require(provenance.get('artifact_ref') == ARTIFACT_REVISION and
            provenance.get('metadata_ref') == SUBMISSION_REVISION and
            provenance.get('submission_url') == SUBMISSION_URL, 'submission/artifact pin mismatch')
    logs = provenance.get('failure_logs_url', '')
    require(isinstance(logs, str) and logs.startswith('https://raw.githubusercontent.com/') and
            f'/{ARTIFACT_REVISION}/' in logs, 'separate patches must use pinned GitHub artifacts')


def build_inventory(submission, details_raw, aggregate_raw, dataset, cache, workers, metadata_sha):
    pinned(submission['provenance'])
    ids = {r['instance_id'] for r in dataset}
    resolved, failed, ng = outcomes(json.loads(details_raw), json.loads(aggregate_raw), ids)
    require(id_set(submission['resolved'], 'importer resolved') == resolved,
            'importer resolved conflicts with source outcomes')
    predictions = submission['predictions']
    require(isinstance(predictions, dict) and set(predictions) == resolved | failed and
            all(isinstance(p, str) for p in predictions.values()), 'expected 441 exact predictions')
    logs = submission['provenance']['failure_logs_url']

    def check(task):
        url = f'{logs}/{task}/patch.diff'
        raw = cache.get(url)
        require(raw.decode('utf-8') == predictions[task], f'separate patch differs from prediction: {task}')
        return dict(task_id=task, url=url, sha256=sha(raw), bytes=len(raw), resolved=task in resolved)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        patches = list(pool.map(check, sorted(predictions)))
    submission = dict(submission, resolved=sorted(resolved), evaluated=sorted(ids),
                      result_details=dict(resolved=sorted(resolved), unresolved=sorted(failed),
                                          no_generation=sorted(ng)))
    submission['provenance'] = dict(submission['provenance'],
        per_instance_results_url=BASE + '/per_instance_details.json',
        per_instance_results_sha256=sha(details_raw),
        aggregate_results_url=BASE + '/results/results.json',
        aggregate_results_sha256=sha(aggregate_raw),
        outcome_binding='per-instance-booleans-plus-explicit-aggregate-no-generation-v1')
    evidence = dict(submission_revision=SUBMISSION_REVISION, artifact_revision=ARTIFACT_REVISION,
                    **COUNTS, provenance=submission['provenance'], patches=patches,
                    dataset_metadata_source=METADATA_SOURCE, dataset_source_sha256=metadata_sha,
                    dataset_metadata_sha256=sha(encode(dataset)),
                    human_comparison_status='intentionally-not-computed-repo-base-only',
                    rights_status='numeric-and-hash-reporting-only-no-raw-redistribution',
                    historical_evaluator_status='not-independently-certified')
    return submission, evidence


def manifest_for(payloads, metadata_sha):
    return dict(schema_version=1, submission_revision=SUBMISSION_REVISION,
                artifact_revision=ARTIFACT_REVISION, required_analyzer_commit=ANALYZER_COMMIT,
                required_python_version=PYTHON_VERSION, dataset_metadata_source=METADATA_SOURCE,
                dataset_source_sha256=metadata_sha,
                files={name: sha(raw) for name, raw in payloads.items()})


def load_bound(root):
    manifest = json.loads((root / 'manifest.json').read_bytes())
    payloads = {name: (root / name).read_bytes() for name in FILES}
    require(manifest == manifest_for(payloads, manifest.get('dataset_source_sha256')),
            'manifest binding/pinned identity mismatch')
    require(isinstance(manifest['dataset_source_sha256'], str) and
            re.fullmatch('[0-9a-f]{64}', manifest['dataset_source_sha256']), 'invalid metadata source hash')
    submission, dataset, evidence = (json.loads(payloads[name]) for name in FILES)
    require(isinstance(dataset, list) and len(dataset) == 500 and
            all(isinstance(r, dict) and set(r) == {'instance_id', 'repo', 'base_commit'} for r in dataset),
            'dataset must contain only 500 repo/base records, no human patches or reference hashes')
    # Reuse metadata validation without copying any reference provenance.
    dataset_from_records([dict(task_id=r['instance_id'], provenance=r) for r in dataset])
    ids = id_set([r['instance_id'] for r in dataset], 'dataset population')
    pinned(submission['provenance'])
    require(id_set(submission['evaluated'], 'inventory population') == ids, 'missing inventory population')
    categories = submission['result_details']
    require(set(categories) == {'resolved', 'unresolved', 'no_generation'}, 'unexpected outcome categories')
    patches = evidence['patches']
    require(isinstance(patches, list) and len(patches) == 441 and
            len(id_set([p['task_id'] for p in patches], 'separate patches')) == 441,
            'missing separate patch population')
    details = {p['task_id']: {'resolved': p['resolved']} for p in patches}
    resolved, failed, ng = outcomes(details, dict(resolved=categories['resolved'],
                                                 no_generation=categories['no_generation']), ids)
    require(id_set(categories['unresolved'], 'explicit failures') == failed and
            id_set(submission['resolved'], 'inventory resolved') == resolved, 'inventory outcome conflict')
    predictions = submission['predictions']
    require(set(predictions) == resolved | failed and all(isinstance(p, str) for p in predictions.values()),
            'inventory prediction population/type mismatch')
    for p in patches:
        raw = predictions[p['task_id']].encode('utf-8')
        require(p['sha256'] == sha(raw) and type(p['bytes']) is int and p['bytes'] == len(raw) and
                p['url'] == f"{submission['provenance']['failure_logs_url']}/{p['task_id']}/patch.diff",
                'separate patch hash/length/location binding mismatch')
    require(all(evidence.get(k) == v for k, v in COUNTS.items()) and
            evidence.get('submission_revision') == SUBMISSION_REVISION and
            evidence.get('artifact_revision') == ARTIFACT_REVISION and
            evidence.get('provenance') == submission['provenance'] and
            evidence.get('dataset_metadata_source') == METADATA_SOURCE and
            evidence.get('dataset_source_sha256') == manifest['dataset_source_sha256'] and
            evidence.get('dataset_metadata_sha256') == sha(payloads['dataset.json']),
            'evidence binding mismatch')
    submission['resolved'], submission['evaluated'] = resolved, ids
    return submission, dataset


def inventory(root, workers):
    from parsimony.artifacts import Cache, load_submission
    require(not any((root / name).exists() for name in (*FILES, 'manifest.json')),
            'inventory outputs already exist; use a fresh external folder')
    raw = (REPO / METADATA_SOURCE).read_bytes()
    dataset = dataset_from_records([json.loads(line) for line in raw.splitlines() if line.strip()])
    cache = Cache(root / 'cache', timeout=25)
    submission = load_submission(SUBMISSION_URL, cache, task_ids=[], include_failed=True)
    submission, evidence = build_inventory(submission, cache.get(BASE + '/per_instance_details.json'),
        cache.get(BASE + '/results/results.json'), dataset, cache, workers, sha(raw))
    payloads = dict(zip(FILES, map(encode, (submission, dataset, evidence))))
    for name, content in payloads.items():
        (root / name).write_bytes(content)
    (root / 'manifest.json').write_bytes(encode(manifest_for(payloads, sha(raw))))
    print('Bound 441 agreeing patches and all 500 explicit outcomes', flush=True)


def clean_checkout(checkout):
    require(git(checkout, 'rev-parse', '--show-toplevel') == str(checkout), 'expected analyzer checkout root')
    require(git(checkout, 'rev-parse', 'HEAD') == ANALYZER_COMMIT and
            not git(checkout, 'status', '--porcelain'), 'required analyzer checkout must be clean at 0aa66df')


def measure_worker(root, checkout, workers):
    from parsimony.artifacts import Cache
    from parsimony import benchmark
    require(platform.python_version() == PYTHON_VERSION, 'measurement requires Python ' + PYTHON_VERSION)
    clean_checkout(checkout)
    require(Path(benchmark.__file__).resolve().parent == checkout / 'parsimony', 'analyzer imported from wrong checkout')
    benchmark.analyzer_identity.cache_clear()
    commit, source_sha = benchmark.analyzer_identity()
    require(commit == ANALYZER_COMMIT, 'required clean analyzer identity unavailable')
    submission, dataset = load_bound(root)
    cache = Cache(root / 'cache', timeout=25)

    def one(task):
        # Supply the whole dataset every time: 500 denominator and source outcomes,
        # including no_generation. Do not measure a one-row dataset or relabel records.
        return next(r for r in benchmark.analyze_submission(submission, cache, dataset=dataset,
                    task_ids=[task], include_failed=True) if r['task_id'] == task)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        records = list(pool.map(one, sorted(submission['evaluated'])))
    require(len(records) == 500 and {r['task_id'] for r in records} == submission['evaluated'],
            'measurement population mismatch')
    require(all(r['analyzer_commit'] == commit and r['analyzer_source_sha256'] == source_sha and
                r['python_version'] == PYTHON_VERSION and r['benchmark_tasks'] == 500 and
                r['published_resolved_count'] == 359 and r['resolve_rate'] == 359 / 500 and
                type(r['resolved']) is bool and r['resolved'] == (r['task_id'] in submission['resolved']) and
                r['provenance']['patch_sha256'] == (
                    sha(submission['predictions'][r['task_id']].encode('utf-8'))
                    if r['task_id'] in submission['predictions'] else None) and
                r['human_metrics'] is None and r['model_human_ratio'] is None for r in records),
            'measurement identity/denominator/human comparison mismatch')
    require(Counter(r['evaluation_result'] for r in records) ==
            {'resolved': 359, 'failed': 82, 'no_generation': 59}, 'measurement source outcomes changed')
    clean_checkout(checkout)
    benchmark.analyzer_identity.cache_clear()
    require(benchmark.analyzer_identity() == (commit, source_sha), 'analyzer changed during measurement')
    output = root / 'measurements.jsonl'
    with output.open('x', encoding='utf-8') as stream:
        for record in sorted(records, key=lambda r: r['task_id']):
            stream.write(json.dumps(record, sort_keys=True) + '\n')
    print('Measured 500:', dict(Counter(r['analysis_status'] for r in records)), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('inventory', 'measure'))
    parser.add_argument('--external-dir', required=True)
    parser.add_argument('--analyzer-checkout', type=Path)
    parser.add_argument('--workers', type=int, default=12)
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        require(args.workers > 0, 'workers must be positive')
        require(not args.worker or args.phase == 'measure', 'worker is measurement-only')
        checkout = args.analyzer_checkout.resolve() if args.analyzer_checkout else None
        root = external_root(args.external_dir, checkout)
        if args.phase == 'inventory':
            inventory(root, args.workers)
        else:
            require(checkout is not None, 'measure requires --analyzer-checkout')
            require(not (root / 'measurements.jsonl').exists(), 'measurement output already exists')
            load_bound(root)  # Fail before launching the analyzer or performing HTTP.
            clean_checkout(checkout)
            if args.worker:
                measure_worker(root, checkout, args.workers)
            else:
                env = dict(os.environ, PYTHONPATH=str(checkout), PYTHONDONTWRITEBYTECODE='1')
                subprocess.run([sys.executable, str(Path(__file__).resolve()), 'measure',
                                '--external-dir', str(root), '--analyzer-checkout', str(checkout),
                                '--workers', str(args.workers), '--worker'], cwd=checkout,
                               env=env, check=True)
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
