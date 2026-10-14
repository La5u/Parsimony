# SWE-bench Live MultiLang — JavaScript

Website: **[parsimony.lasu.dev/live-javascript.html](https://parsimony.lasu.dev/live-javascript.html)**.

Five public model + agent submissions to [SWE-bench Live](https://swe-bench-live.github.io) MultiLang, on all **108** tasks of its `js` split. **This compares model + agent setups, not models alone:** each submitter used their own agent (AMI Agent or Sapient Slingshot), and pass/fail is the submitter's own evaluation report, not rechecked here. One attempt per task.

## Sources

- Tasks: Hugging Face [`SWE-bench-Live/MultiLang` at `62dc074`](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/62dc0745c40f067fc366ae3eb1a26136e5928f85), `data/js-00000-of-00001.parquet` (unchanged at the current revision `3638632`).
- Runs: GitHub [`SWE-bench-Live/submission` at `99bae66`](https://github.com/SWE-bench-Live/submission/tree/99bae66f923b3dfeab2d18366c0593929c5722de/submissions/multilang/js_ts), `submissions/multilang/js_ts/<config>/js`: AMI Agent 0.7.0 + Claude Opus 4.6 (2026-07-10), Slingshot 2.6.0 + Claude Sonnet 4.5 (2026-06-23), Slingshot 2.6.0 + GPT-5.5 (2026-06-29), Slingshot 3.0.0 + GPT-5.5 (2026-07-30), Slingshot 3.4.0 + GPT-5.6 Sol. GPT-5.6 Sol's predictions and results are byte-identical to the earlier audited pin `cba8a6d`.
- Before-state checks: [`../live-multilang/*_js.preimages.json`](../live-multilang/) (metadata and hashes only). Each touched file's old blob and hunks are matched against the task's base commit; patches that cannot be checked are left unmeasured.

## Results (analyzer 0.10.0-beta @ `4c02b61`, `typescript-compiler-units-v1`, Python 3.14.7)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Claude Opus 4.6 · AMI Agent 0.7.0 | 0.56× | 0.24–1.12× | 23 | +30.9 | +33.6 | 55.6% | 54/60 |
| 2 | GPT-5.6 Sol · Slingshot 3.4.0 | 0.80× | 0.43–1.05× | 27 | +82.1 | +94.4 | 73.1% | 72/79 |
| 3 | GPT-5.5 · Slingshot 3.0.0 | 1.11× | 0.80–1.67× | 27 | +47.3 | +56.5 | 42.6% | 44/46 |
| 4 | Claude Sonnet 4.5 · Slingshot 2.6.0 | 1.11× | 0.93–1.45× | 15 | +77.6 | +61.9 | 21.3% | 21/23 |
| 5 | GPT-5.5 · Slingshot 2.6.0 | 1.56× | 1.03–2.06× | 25 | +36.0 | +90.9 | 28.7% | 30/31 |

| Configuration | Submitted | Measured | Upstream grader error | Unverified before-state | Analysis error | Empty patch | Not in the run |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 93 | 80 | 0 | 4 | 2 | 7 | 15 |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 93 | 83 | 8 | 1 | 1 | 0 | 15 |
| GPT-5.5 · Slingshot 2.6.0 | 93 | 86 | 4 | 1 | 2 | 0 | 15 |
| GPT-5.5 · Slingshot 3.0.0 | 93 | 87 | 3 | 1 | 2 | 0 | 15 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 108 | 102 | 3 | 1 | 2 | 0 | 0 |

Grader errors, unverified before-states, analysis errors, empty patches and unsubmitted tasks are not measured and never count as zero. Grader errors and unsubmitted tasks keep an unknown outcome, never a failure. The four older runs report 93 tasks; the other 15 are absent from their results.

Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md). Records publish scalars and hashes only, not patches. Raw-artifact redistribution is not cleared; see the [Live Python review](../../docs/archive/priority-live-provenance.md), which applies the same terms.

## Reproduce

```sh
# external storage only: the cache holds upstream patches
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase inventory
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase audit
# from a clean worktree at the analyzer commit, after npm ci, with Python 3.14.7:
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase measure
M=examples/live-javascript
python -m parsimony.release freeze $M/population.jsonl --name live-multilang-javascript-v1 --output $M/population-manifest.json
python -m parsimony.scoring freeze $M/*-*.jsonl --name live-multilang-javascript-v1 --population $M/population-manifest.json --output $M/score-panel.json
python -m parsimony.release audit $M/population-manifest.json $M/*-*.jsonl --output $M/coverage.json
python -m parsimony.scoring score $M/score-panel.json $M/*-*.jsonl --output $M/scores.json
python -m parsimony.stability $M/score-panel.json $M/*-*.jsonl --output $M/stability.json
```
