#!/usr/bin/env python3
"""Measure GLM-5.1 (EvalScope agentic harness) on SWE-bench Verified from a pinned public replay export.

Source: https://huggingface.co/datasets/fxiao0369/GLM51-swebench-replay (MIT), pinned revision below.
It publishes 500 predictions with a per-instance `resolved` boolean from the uploader's own
SWE-bench run. This is a different harness from every other Verified row (mini-SWE-agent), so the
record agent names the harness. Empty predictions are recorded as `no_generation`, never as zero.

The export strips trailing whitespace from every patch (all copies in the repository agree), which
drops final blank context lines and so breaks the last hunk's line count. Only whitespace-only lines
can be lost that way, so when the final hunk is short by the same number of old and new lines,
exactly that many blank context lines are restored. The analyzer still checks every context line
against the base commit, added and removed lines are untouched, and each record keeps the source
patch hash and the number of restored lines.

Run from the repository root with the 0.5.2-beta analyzer used for the Verified board:

    git worktree add --detach /tmp/parsimony-0aa66df 0aa66df
    PYTHONPATH=/tmp/parsimony-0aa66df python examples/benchmark-discovery/add-glm51-verified.py \
        --external-dir /tmp/glm51-measure --output examples/mini-swe-agent-500/glm-5.1-evalscope.jsonl

Metadata (repo, base commit) comes from an existing 500-record Verified cohort; the human
comparison is intentionally not computed, as for Gemini 3.5 Flash. Raw patches stay external.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[2]
REVISION = '5c03de18c6ef604d8cd95da95c1335b717fc0936'
DATASET = 'fxiao0369/GLM51-swebench-replay'
PREDICTIONS_URL = f'https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/data/verified_agentic/predictions.jsonl'
PREDICTIONS_SHA256 = '3cfd73490b4cefb78fc5f4dca0bb2a0d4bbf2e7a25eb5ceec4933cc426123951'
ANALYZER_COMMIT = '0aa66dfb6dca76893b0f20e22233317965ff0d25'
AGENT = 'glm-5.1-evalscope'
METADATA_SOURCE = 'examples/mini-swe-agent-500/claude-4-6-opus.jsonl'
COUNTS = {'resolved': 363, 'failed': 131, 'no_generation': 6}


def require(condition, message):
    if not condition:
        raise SystemExit(message)


HUNK = re.compile(r'^@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@', re.M)


def restore_trailing_context(patch):
    """Return (patch, restored line count): undo whitespace stripping at the end of the last hunk."""
    hunks = list(HUNK.finditer(patch))
    if not hunks:
        return patch, 0
    last = hunks[-1]
    want_old, want_new = (int(n) if n is not None else 1 for n in last.groups())
    body = patch[last.end():].split('\n')[1:]
    old = sum(line[:1] in (' ', '-', '') for line in body)
    new = sum(line[:1] in (' ', '+', '') for line in body)
    missing = want_old - old
    if missing <= 0 or missing != want_new - new or any(line.startswith('\\') for line in body):
        return patch, 0
    return patch.rstrip('\n') + '\n' + ' \n' * missing, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--external-dir', type=Path, required=True, help='download cache, outside the repository')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=8)
    args = parser.parse_args()

    from parsimony import benchmark
    from parsimony.artifacts import Cache
    commit, source_sha = benchmark.analyzer_identity()
    require(commit == ANALYZER_COMMIT, f'analyzer must be a clean {ANALYZER_COMMIT[:7]} checkout, got {commit}')
    require(REPO not in args.external_dir.resolve().parents, 'keep the cache outside the repository')
    require(not args.output.exists(), f'{args.output} exists; frozen records are never overwritten')

    cache = Cache(args.external_dir / 'cache', timeout=30)
    raw = cache.get(PREDICTIONS_URL)
    require(hashlib.sha256(raw).hexdigest() == PREDICTIONS_SHA256, 'predictions changed at the pinned revision')
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    require(all(type(r['resolved']) is bool and isinstance(r['model_patch'], str) for r in rows), 'unexpected row shape')
    by_id = {r['instance_id']: r for r in rows}

    records = [json.loads(line) for line in (REPO / METADATA_SOURCE).read_text().splitlines() if line.strip()]
    dataset = sorted((dict(instance_id=r['task_id'], repo=r['provenance']['repo'],
                           base_commit=r['provenance']['base_commit']) for r in records),
                     key=lambda r: r['instance_id'])
    population = {r['instance_id'] for r in dataset}
    require(len(rows) == len(by_id) == len(population) == 500 and set(by_id) == population,
            'predictions must cover exactly the 500 Verified tasks')

    resolved = {t for t, r in by_id.items() if r['resolved']}
    empty = {t for t, r in by_id.items() if not r['model_patch'].strip()}
    require(not resolved & empty, 'an empty prediction is marked resolved')
    failed = population - resolved - empty
    require({'resolved': len(resolved), 'failed': len(failed), 'no_generation': len(empty)} == COUNTS,
            'source outcome counts changed')
    restored = {t: restore_trailing_context(r['model_patch']) for t, r in by_id.items() if t not in empty}
    submission = dict(
        agent=AGENT, resolved=resolved, evaluated=population,
        predictions={t: patch for t, (patch, _) in restored.items()},
        result_details=dict(resolved=sorted(resolved), unresolved=sorted(failed), no_generation=sorted(empty)),
        provenance=dict(layout='huggingface-evalscope-predictions-v1', harness='EvalScope swe_bench_verified_agentic',
                        reported_model=rows[0]['model_name_or_path'], ref=REVISION,
                        submission_url=f'https://huggingface.co/datasets/{DATASET}/tree/{REVISION}',
                        prediction_url=PREDICTIONS_URL, prediction_sha256=PREDICTIONS_SHA256,
                        results_url=PREDICTIONS_URL, results_sha256=PREDICTIONS_SHA256,
                        outcome_source='uploader-reported per-instance resolved boolean, not the official leaderboard',
                        license='MIT'))

    def one(task):
        # Pass the full dataset each time so every record keeps the 500-task denominator.
        return next(r for r in benchmark.analyze_submission(submission, cache, dataset=dataset, task_ids=[task],
                                                            include_failed=True) if r['task_id'] == task)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        measured = list(pool.map(one, sorted(population)))
    require(Counter(r['evaluation_result'] for r in measured) == COUNTS, 'measured outcomes changed')
    require(all(r['analyzer_source_sha256'] == source_sha and r['human_metrics'] is None for r in measured),
            'analyzer identity changed during measurement')
    for r in measured:
        if r['task_id'] in restored:
            r['provenance']['source_patch_sha256'] = hashlib.sha256(by_id[r['task_id']]['model_patch'].encode()).hexdigest()
            r['provenance']['trailing_context_lines_restored'] = restored[r['task_id']][1]
    with args.output.open('x') as stream:
        for record in measured:
            stream.write(json.dumps(record, sort_keys=True) + '\n')
    print('Measured 500:', dict(Counter((r['evaluation_result'], r['analysis_status']) for r in measured)))


if __name__ == '__main__':
    main()
