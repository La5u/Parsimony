"""Export and validate reviewable result bundles; no downloads or patch analysis."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from .benchmark import leaderboard, read_jsonl


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
        require(r['analysis_status'] in {'ok', 'not_resolved', 'not_selected', 'limit',
                                        'missing_patch', 'missing_base_metadata', 'error'}, 'unknown analysis status')
        if r['analysis_status'] != 'ok':
            require(r['metrics'] is None, 'unavailable analysis must not carry scored metrics')
            continue
        require(r['resolved'], 'current format only scores successful patches')
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('export', help='create/update a bundle from existing JSONL')
    add.add_argument('records')
    add.add_argument('--agent', required=True)
    add.add_argument('--output', required=True)
    check = commands.add_parser('validate', help='check all bundle directories; no network access')
    check.add_argument('root', nargs='?', default='submissions')
    args = parser.parse_args()
    try:
        if args.command == 'export':
            export(args.records, args.agent, args.output)
            print(f'Exported and validated {args.output}')
        else:
            root = Path(args.root)
            require(root.is_dir(), 'submission root does not exist')
            bundles = [root] if (root / 'manifest.json').exists() else sorted(p for p in root.iterdir() if p.is_dir())
            for bundle in bundles:
                validate(bundle)
            print(f'Validated {len(bundles)} submission bundles (offline)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
