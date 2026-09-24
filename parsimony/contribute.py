"""Export and validate reviewable result bundles.

``export`` and ``validate`` are offline arithmetic/checksum checks. ``verify``
downloads a sample of the recorded patches and re-measures them.
"""
import argparse
import hashlib
import json
import math
import random
from pathlib import Path

from .analysis import measure
from .artifacts import Cache, _bytes, _parse_predictions
from .benchmark import ANALYZER_VERSION, FAILED_CATEGORIES, base_source, leaderboard, read_jsonl


FORMAT = 'successful-footprint-medians-v1'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_records(records, agent):
    require(bool(records), 'no records selected')
    ids = set()
    signatures = set()
    for r in records:
        task = r['task_id']
        require(r['agent'] == agent and task not in ids, 'mixed agents or duplicate task IDs')
        ids.add(task)
        require(type(r['resolved']) is bool, 'resolved must be boolean')
        require(r['benchmark_tasks'] == 500, 'contributed Verified results require the 500-task denominator')
        count = r['published_resolved_count']
        require(type(count) is int and 0 <= count <= 500, 'invalid published resolved count')
        require(math.isclose(r['resolve_rate'], count / 500, abs_tol=1e-12), 'resolve rate/count mismatch')
        signatures.add((r['analyzer_version'], r['python_version'], count))
        provenance = r['provenance']
        for key in ('submission_url', 'results_url', 'patch_location'):
            require(str(provenance.get(key, '')).startswith(('https://', 'http://')), f'public {key} required')
        digest = provenance.get('results_sha256', '')
        require(isinstance(digest, str) and len(digest) == 64
                and all(c in '0123456789abcdef' for c in digest), 'result artifact SHA256 required')
        require(r['analysis_status'] in {'ok', 'not_resolved', 'not_selected', 'limit', 'missing_patch',
                                        'missing_base_metadata', 'error', 'fetch_error'}, 'unknown analysis status')
        if r['analysis_status'] != 'ok':
            require(r['metrics'] is None, 'unavailable analysis must not carry scored metrics')
            continue
        categories = set(r.get('published_result_categories', []))
        # Failed-patch measurements (analyze --include-failed) are allowed only
        # with an explicit evaluated-failure category; summaries use successes only.
        require(r['resolved'] or (categories & FAILED_CATEGORIES and 'no_logs' not in categories),
                'unresolved metrics require an explicit failed category')
        m = r['metrics']
        require(m['mode'] == 'full_file', 'patch-only estimates are not accepted as full-file contributions')
        for key in ('tokens_added', 'tokens_deleted', 'churn', 'files_changed'):
            require(type(m[key]) is int and m[key] >= 0, f'invalid {key}')
        require(m['net_tokens'] == m['tokens_added'] - m['tokens_deleted'], 'net token mismatch')
        require(m['churn'] == m['tokens_added'] + m['tokens_deleted'], 'churn mismatch')
        require(provenance.get('base_commit') and provenance.get('repo') and provenance.get('patch_sha256'),
                'full-file source and patch provenance required')
        human = r.get('human_metrics')
        expected_ratio = m['churn'] / human['churn'] if human and human['churn'] else None
        require(r.get('model_human_ratio') == expected_ratio, 'model/human ratio mismatch')
    require(len(signatures) == 1, 'mixed analyzer/Python versions or resolve totals')
    require(len(ids) <= 500, 'too many Verified tasks')
    count = records[0]['published_resolved_count']
    observed = sum(r['resolved'] for r in records)
    require(observed <= count, 'more resolved records than published total')
    if len(ids) == 500:
        require(observed == count, 'complete record set disagrees with published resolved count')


def export(records_path, agent, destination):
    records = sorted((r for r in read_jsonl(records_path) if r['agent'] == agent), key=lambda r: r['task_id'])
    check_records(records, agent)
    payload = ''.join(json.dumps(r, sort_keys=True, allow_nan=False) + '\n' for r in records).encode()
    manifest = dict(format=FORMAT, agent=agent, benchmark='SWE-bench Verified',
                    coverage='complete-record-set' if len(records) == 500 else 'sample',
                    task_ids=[r['task_id'] for r in records],
                    records_sha256=hashlib.sha256(payload).hexdigest())
    board = leaderboard(records)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'records.jsonl').write_bytes(payload)
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (destination / 'leaderboard.json').write_text(json.dumps(board, indent=2, allow_nan=False) + '\n')
    validate(destination)


def validate(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text())
    require(manifest['format'] == FORMAT, 'unknown score format; scalar score bundles are not supported')
    require(manifest['benchmark'] == 'SWE-bench Verified', 'unsupported benchmark')
    payload = (directory / 'records.jsonl').read_bytes()
    require(hashlib.sha256(payload).hexdigest() == manifest['records_sha256'], 'records checksum mismatch')
    records = read_jsonl(directory / 'records.jsonl')
    # Reject non-standard JSON numbers even in auxiliary fields.
    json.dumps(records, allow_nan=False)
    check_records(records, manifest['agent'])
    require(sorted(r['task_id'] for r in records) == manifest['task_ids'], 'task manifest mismatch')
    expected = 'complete-record-set' if len(records) == 500 else 'sample'
    require(manifest['coverage'] == expected, 'coverage label mismatch')
    board = json.loads((directory / 'leaderboard.json').read_text())
    require(board == leaderboard(records), 'leaderboard differs from recomputed results; regenerate it')


def fetch_patch(record, cache):
    """Download the recorded patch from its public location."""
    location = record['provenance']['patch_location']
    url, _, fragment = location.partition('#instance_id=')
    if not fragment:
        return _bytes(url, cache).decode('utf-8')
    _, predictions = _parse_predictions(_bytes(url, cache))
    require(fragment in predictions, f'{fragment} missing from {url}')
    return predictions[fragment]


def verify(records, dataset, cache, sample=None, seed=0):
    """Re-fetch patches, check SHA256 and re-measure them (current analyzer only)."""
    metadata = {row['instance_id']: row for row in dataset}
    measured = [r for r in records if r['analysis_status'] == 'ok']
    if sample is not None and sample < len(measured):
        measured = random.Random(seed).sample(measured, sample)
    results = []
    for r in sorted(measured, key=lambda r: (r['agent'], r['task_id'])):
        row = dict(agent=r['agent'], task_id=r['task_id'])
        try:
            patch = fetch_patch(r, cache)
            row['patch_sha256_matches'] = (hashlib.sha256(patch.encode()).hexdigest()
                                           == r['provenance']['patch_sha256'])
            if r['analyzer_version'] != ANALYZER_VERSION:
                row['metrics_match'] = None
                row['note'] = f"recorded with analyzer {r['analyzer_version']}; hash checked only"
            else:
                meta = metadata[r['task_id']]
                require((meta['repo'], meta['base_commit']) ==
                        (r['provenance']['repo'], r['provenance']['base_commit']), 'base commit differs from dataset')
                source = base_source(cache, meta) if r['metrics']['mode'] == 'full_file' else None
                row['metrics_match'] = measure(patch, source) == r['metrics']
        except Exception as exc:  # report every record rather than stopping at the first failure
            row['error'] = f'{type(exc).__name__}: {exc}'
        results.append(row)
    failures = [row for row in results if row.get('error') or row.get('patch_sha256_matches') is False
                or row.get('metrics_match') is False]
    return dict(checked=len(results), failures=len(failures), analyzer_version=ANALYZER_VERSION,
                sample=sample, seed=seed, results=results)


def bundle_dirs(root):
    root = Path(root)
    require(root.is_dir(), 'submission root does not exist')
    return [root] if (root / 'manifest.json').exists() else sorted(p for p in root.iterdir() if p.is_dir())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('export', help='create/update a bundle from existing JSONL')
    add.add_argument('records')
    add.add_argument('--agent', required=True)
    add.add_argument('--output', required=True)
    check = commands.add_parser('validate', help='check all bundle directories; no network access')
    check.add_argument('root', nargs='?', default='submissions')
    audit = commands.add_parser('verify', help='download recorded patches, check hashes and re-measure')
    audit.add_argument('root', nargs='?', default='submissions', help='bundle directory, bundle root or JSONL file')
    audit.add_argument('--dataset', required=True, help='Verified metadata JSONL')
    audit.add_argument('--sample', type=int, help='random measured records to check (default: all)')
    audit.add_argument('--seed', type=int, default=0)
    audit.add_argument('--cache', default='.parsimony-cache')
    audit.add_argument('--output', help='write the JSON report here')
    args = parser.parse_args()
    try:
        if args.command == 'export':
            export(args.records, args.agent, args.output)
            print(f'Exported and validated {args.output}')
        elif args.command == 'validate':
            bundles = bundle_dirs(args.root)
            for bundle in bundles:
                validate(bundle)
            print(f'Validated {len(bundles)} submission bundles (offline)')
        else:
            root = Path(args.root)
            files = [root] if root.is_file() else [b / 'records.jsonl' for b in bundle_dirs(root)]
            records = [r for path in files for r in read_jsonl(path)]
            report = verify(records, read_jsonl(args.dataset), Cache(args.cache), args.sample, args.seed)
            text = json.dumps(report, indent=2, sort_keys=True) + '\n'
            if args.output:
                Path(args.output).write_text(text)
            print(f"Verified {report['checked']} records: {report['failures']} failures")
            if report['failures']:
                parser.exit(1, text if not args.output else '')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
