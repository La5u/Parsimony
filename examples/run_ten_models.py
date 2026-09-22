"""Reproduce the 10-model/10-shared-task sample without running any agent code.

From the checkout: python -m examples.run_ten_models --dataset verified.jsonl
"""
import argparse
import hashlib
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from parsimony.artifacts import Cache, load_submission
from parsimony.benchmark import analyze_submission, leaderboard, read_jsonl


def analyze_one(job):
    name, plan, metadata, cache_dir = job
    cache = Cache(cache_dir, timeout=90)
    submission = load_submission(name, cache, ref=plan['experiments_ref'], task_ids=plan['tasks'])
    if not set(plan['tasks']) <= submission['resolved']:
        raise ValueError(f'selected tasks not all resolved by {name}')
    records = list(analyze_submission(submission, cache, metadata, task_ids=plan['tasks']))
    selected = [r for r in records if r['task_id'] in plan['tasks']]
    print(name, dict(Counter(r['analysis_status'] for r in selected)), flush=True)
    progress = Path(cache_dir) / 'ten-model-progress'
    progress.mkdir(parents=True, exist_ok=True)
    (progress / (name + '.jsonl')).write_text(
        ''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', default='verified.jsonl')
    parser.add_argument('--cache', default='.parsimony-cache')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    plan = json.loads((directory / 'ten-model-plan.json').read_text())
    digest = hashlib.sha256(Path(args.dataset).read_bytes()).hexdigest()
    if digest != plan['dataset_sha256']:
        raise ValueError('dataset differs from the recorded sample; preserve the original metadata or create a new plan')
    metadata = read_jsonl(args.dataset)
    if len(metadata) != 500:
        raise ValueError('use complete 500-task Verified metadata')
    jobs = [(name, plan, metadata, args.cache) for name in plan['submissions']]
    # Separate processes bypass the GIL for token-sequence alignment; they run
    # only Parsimony's static analyzer, never any submitted code.
    with ProcessPoolExecutor(max_workers=4) as pool:
        records = [r for group in pool.map(analyze_one, jobs) for r in group]
    selected = [r for r in records if r['task_id'] in plan['tasks']]
    for path, rows in [(Path(args.cache) / 'ten-model-all-results.jsonl', records),
                       (directory / 'ten-model-results.jsonl', selected)]:
        path.write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in rows))
    board = leaderboard(records, shared=True)
    (directory / 'ten-model-leaderboard.json').write_text(json.dumps(board, indent=2) + '\n')
    print(json.dumps(board, indent=2))
    if any(r['analysis_status'] != 'ok' or r.get('human_error') for r in selected):
        raise SystemExit('Some selected analyses failed; inspect saved records (no replacement sampling).')


if __name__ == '__main__':
    main()
