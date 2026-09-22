import argparse
import json
import sys
from pathlib import Path

from .artifacts import Cache, load_manifest, load_submission
from .benchmark import analyze_submission, fetch_dataset, leaderboard, read_jsonl


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
    analyze.add_argument('--limit', type=int, help='successful tasks to attempt per submission, sorted by ID')
    analyze.add_argument('--task', action='append', help='analyze this task ID only (repeatable); keeps full resolve-rate denominator')
    analyze.add_argument('--output', default='results.jsonl')
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
            submissions = [load_submission(s, cache, args.ref, task_ids=args.task, limit=args.limit)
                           for s in args.submissions]
            submissions += [load_manifest(s, cache) for s in args.manifest]
            names = [s['agent'] for s in submissions]
            if len(set(names)) != len(names):
                parser.error('agent names collide; use manifests with distinct agent names')
            rows = (r for s in submissions for r in analyze_submission(
                s, cache, metadata, args.limit, args.patch_only, task_ids=args.task))
        with Path(args.output).open('w') as stream:
            count = 0
            for row in rows:
                stream.write(json.dumps(row, sort_keys=True) + '\n')
                count += 1
        print(f'Wrote {count} records to {args.output}', file=sys.stderr)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
