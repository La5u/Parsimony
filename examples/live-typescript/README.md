# SWE-bench Live MultiLang — TypeScript

Website: **[parsimony.lasu.dev/live-typescript.html](https://parsimony.lasu.dev/live-typescript.html)**.

Five public model + agent submissions to [SWE-bench Live](https://swe-bench-live.github.io) MultiLang, on all **111** tasks of its `ts` split. **This compares model + agent setups, not models alone:** each submitter used their own agent (AMI Agent or Sapient Slingshot), and pass/fail is the submitter's own evaluation report, not rechecked here. One attempt per task.

## Sources

- Tasks: Hugging Face [`SWE-bench-Live/MultiLang` at `62dc074`](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/62dc0745c40f067fc366ae3eb1a26136e5928f85), `data/ts-00000-of-00001.parquet` (unchanged at the current revision `3638632`).
- Runs: GitHub [`SWE-bench-Live/submission` at `99bae66`](https://github.com/SWE-bench-Live/submission/tree/99bae66f923b3dfeab2d18366c0593929c5722de/submissions/multilang/js_ts), `submissions/multilang/js_ts/<config>/ts`: AMI Agent 0.7.0 + Claude Opus 4.6 (2026-07-10), Slingshot 2.6.0 + Claude Sonnet 4.5 (2026-06-23), Slingshot 2.6.0 + GPT-5.5 (2026-06-29), Slingshot 3.0.0 + GPT-5.5 (2026-07-30), Slingshot 3.4.0 + GPT-5.6 Sol. GPT-5.6 Sol's predictions and results are byte-identical to the earlier audited pin `cba8a6d`.
- Before-state checks: [`../live-multilang/*_ts.preimages.json`](../live-multilang/) (metadata and hashes only). Each touched file's old blob and hunks are matched against the task's base commit; patches that cannot be checked are left unmeasured.

## Results (analyzer 0.10.0-beta @ `4c02b61`, `typescript-compiler-units-v1`, Python 3.14.7)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Claude Sonnet 4.5 · Slingshot 2.6.0 | 0.70× | 0.46–0.95× | 23 | +39.1 | +60.0 | 25.2% | 27/28 |
| 2 | GPT-5.6 Sol · Slingshot 3.4.0 | 0.78× | 0.34–1.08× | 34 | +130.2 | +130.8 | 63.1% | 66/70 |
| 3 | Claude Opus 4.6 · AMI Agent 0.7.0 | 0.80× | 0.51–1.10× | 33 | +24.8 | +33.4 | 55.9% | 56/62 |
| 4 | GPT-5.5 · Slingshot 3.0.0 | 1.26× | 0.95–1.99× | 33 | +109.0 | +111.5 | 46.8% | 51/52 |
| 5 | GPT-5.5 · Slingshot 2.6.0 | 1.45× | 0.90–2.23× | 34 | +107.7 | +113.2 | 41.4% | 45/46 |

| Configuration | Submitted | Measured | Upstream grader error | Unverified before-state | Analysis error | Empty patch | Not in the run |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 111 | 103 | 0 | 4 | 2 | 2 | 0 |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 107 | 103 | 2 | 1 | 1 | 0 | 4 |
| GPT-5.5 · Slingshot 2.6.0 | 111 | 108 | 1 | 1 | 1 | 0 | 0 |
| GPT-5.5 · Slingshot 3.0.0 | 111 | 108 | 0 | 2 | 1 | 0 | 0 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 111 | 106 | 1 | 2 | 2 | 0 | 0 |

Grader errors, unverified before-states, analysis errors, empty patches and unsubmitted tasks are not measured and never count as zero. Grader errors and unsubmitted tasks keep an unknown outcome, never a failure.

Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md). Records publish scalars and hashes only, not patches. Raw-artifact redistribution is not cleared; see the [Live Python review](../../docs/archive/priority-live-provenance.md), which applies the same terms.

## Reproduce

```sh
# external storage only: the cache holds upstream patches
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase inventory
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase audit
# from a clean worktree at the analyzer commit, after npm ci, with Python 3.14.7:
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase measure
M=examples/live-typescript
python -m parsimony.release freeze $M/population.jsonl --name live-multilang-typescript-v1 --output $M/population-manifest.json
python -m parsimony.scoring freeze $M/*-*.jsonl --name live-multilang-typescript-v1 --population $M/population-manifest.json --output $M/score-panel.json
python -m parsimony.release audit $M/population-manifest.json $M/*-*.jsonl --output $M/coverage.json
python -m parsimony.scoring score $M/score-panel.json $M/*-*.jsonl --output $M/scores.json
python -m parsimony.stability $M/score-panel.json $M/*-*.jsonl --output $M/stability.json
```
