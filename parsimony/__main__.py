import argparse
import json
import platform
import sys
from pathlib import Path

from .artifacts import Cache, load_manifest, load_submission
from .benchmark import ANALYZER_VERSION, analyze_submission, fetch_dataset, leaderboard, read_jsonl


def main():
    parser = argparse.ArgumentParser(description='Parsimony static SWE-bench footprint benchmark')
    parser.add_argument('--cache', default='.parsimony-cache')
    commands = parser.add_subparsers(dest='command', required=True)
    dataset = commands.add_parser('dataset', help='cache Verified metadata and human patches')
    dataset.add_argument('--output', default='verified.jsonl')
    analyze = commands.add_parser('analyze', help='import and statically analyze published submissions')
    analyze.add_argument('submissions', nargs='*')
    analyze.add_argument('--manifest', action='append', default=[])
    analyze.add_argument('--ref', default='main', help='experiments Git commit/ref')
    analyze.add_argument('--dataset', help='Verified metadata JSONL (required for full-file analysis)')
    analyze.add_argument('--patch-only', action='store_true', help='less reliable hunk estimates, separate leaderboard mode')
    analyze.add_argument('--limit', type=int, help='eligible tasks to attempt per submission, sorted by ID')
    analyze.add_argument('--include-failed', action='store_true', help='also fetch/analyze explicitly failed patches where available')
    analyze.add_argument('--task', action='append', help='analyze this task ID only (repeatable); keeps full resolve-rate denominator')
    analyze.add_argument('--output', default='results.jsonl')
    analyze.add_argument('--resume', action='store_true', help='append missing task records to existing output (one submission, no --limit/--task)')
    board = commands.add_parser('leaderboard')
    board.add_argument('records', nargs='+')
    board.add_argument('--shared', action='store_true')
    board.add_argument('--agent', action='append')
    board.add_argument('--mode', choices=['full_file', 'patch_only'], default='full_file')
    args = parser.parse_args()
    try:
        if args.command == 'leaderboard':
            records = [r for path in args.records for r in read_jsonl(path)]
            print(json.dumps(leaderboard(records, args.shared, args.agent, args.mode), indent=2))
            return
        cache = Cache(args.cache)
        if args.command == 'dataset':
            rows = fetch_dataset(cache)
        else:
            if not args.submissions and not args.manifest:
                parser.error('provide a submission or --manifest')
            if not args.dataset and not args.patch_only:
                parser.error('provide --dataset or explicitly opt into --patch-only')
            if args.limit is not None and args.limit < 1:
                parser.error('--limit must be positive')
            metadata = read_jsonl(args.dataset) if args.dataset else None
            prior = []
            if args.resume:
                if len(args.submissions) != 1 or args.manifest or args.limit or args.task or not metadata:
                    parser.error('--resume requires one submission and full metadata; no --limit, --task or manifest')
                if Path(args.output).exists():
                    prior = read_jsonl(args.output)
                seen = set()
                dataset_ids = {m['instance_id'] for m in metadata}
                for r in prior:
                    key = (r['agent'], r['task_id'])
                    if key in seen or r['task_id'] not in dataset_ids:
                        raise ValueError('resume file has duplicates or out-of-population records')
                    seen.add(key)
                    if r['analyzer_version'] != ANALYZER_VERSION or r['python_version'] != platform.python_version():
                        raise ValueError('resume file uses incompatible analyzer/Python version')
                    if r['provenance'].get('ref') != args.ref:
                        raise ValueError('resume file uses a different experiments ref')
                    if r['analysis_status'] in {'not_selected', 'limit'}:
                        raise ValueError('resume file contains records skipped by --task/--limit')
                    if r.get('metrics') and r['metrics'].get('mode') != ('patch_only' if args.patch_only else 'full_file'):
                        raise ValueError('resume file uses a different analysis mode')
                    categories = set(r.get('published_result_categories', []))
                    if (args.include_failed and not r['resolved'] and
                            categories & {'unresolved', 'failed', 'not_resolved'} and
                            'no_logs' not in categories and r['analysis_status'] == 'not_resolved'):
                        raise ValueError('resume file has failures skipped without --include-failed')
            remaining = ([m['instance_id'] for m in metadata if m['instance_id'] not in {r['task_id'] for r in prior}]
                         if args.resume else args.task)
            submissions = [load_submission(s, cache, args.ref, task_ids=remaining, limit=args.limit,
                                           include_failed=args.include_failed)
                           for s in args.submissions]
            submissions += [load_manifest(s, cache) for s in args.manifest]
            names = [s['agent'] for s in submissions]
            if len(set(names)) != len(names):
                parser.error('agent names collide; use manifests with distinct agent names')
            if args.resume and prior:
                current = submissions[0]
                if any(r['agent'] != current['agent'] or
                       r['provenance'].get('results_sha256') != current['provenance'].get('results_sha256') or
                       r['published_resolved_count'] != len(current['resolved']) or
                       r['resolved'] != (r['task_id'] in current['resolved'])
                       for r in prior):
                    raise ValueError('resume file submission/results differ from existing records')
            wanted = set(remaining or [])
            rows = (r for s in submissions for r in analyze_submission(
                s, cache, metadata, args.limit, args.patch_only, task_ids=remaining,
                include_failed=args.include_failed)
                    if not args.resume or r['task_id'] in wanted)
        with Path(args.output).open('a' if args.command == 'analyze' and args.resume else 'w') as stream:
            count = 0
            for row in rows:
                stream.write(json.dumps(row, sort_keys=True) + '\n')
                if args.command == 'analyze' and args.resume:
                    stream.flush()
                count += 1
        print(f'Wrote {count} records to {args.output}', file=sys.stderr)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
