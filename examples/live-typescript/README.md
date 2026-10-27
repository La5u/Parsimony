# SWE-bench Live MultiLang — TypeScript

Website: **[parsimony.lasu.dev/live-typescript.html](https://parsimony.lasu.dev/live-typescript.html)**.

Six public model + agent submissions to [SWE-bench Live](https://swe-bench-live.github.io) MultiLang, on all **111** tasks of its `ts` split. **This compares model + agent setups, not models alone:** each submitter used their own agent (AMI Agent, Sapient Slingshot or Lenovo TianxiCode), and pass/fail is the submitter's own evaluation report, not rechecked here. One attempt per task.

## Sources

- Tasks: Hugging Face [`SWE-bench-Live/MultiLang` at `62dc074`](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/62dc0745c40f067fc366ae3eb1a26136e5928f85), `data/ts-00000-of-00001.parquet` (unchanged at the current revision `3638632`).
- Runs: GitHub [`SWE-bench-Live/submission` at `99bae66`](https://github.com/SWE-bench-Live/submission/tree/99bae66f923b3dfeab2d18366c0593929c5722de/submissions/multilang/js_ts), `submissions/multilang/js_ts/<config>/ts`: AMI Agent 0.7.0 + Claude Opus 4.6 (2026-07-10), Slingshot 2.6.0 + Claude Sonnet 4.5 (2026-06-23), Slingshot 2.6.0 + GPT-5.5 (2026-06-29), Slingshot 3.0.0 + GPT-5.5 (2026-07-30), Slingshot 3.4.0 + GPT-5.6 Sol. GPT-5.6 Sol's predictions and results are byte-identical to the earlier audited pin `cba8a6d`.
- TianxiCode 0.1.486 + DeepSeek V4.1 Flash (2026-10-26): **not merged upstream.** It comes from the open pull request [SWE-bench-Live/submission#64](https://github.com/SWE-bench-Live/submission/pull/64) (by `wei64`), pinned at its head commit [`8275820`](https://github.com/SWE-bench-Live/submission/tree/8275820e4fd36720d5281ce73e8fc5beb16fb404/submissions/multilang/js_ts/tianxi/deepseek-flash), `submissions/multilang/js_ts/tianxi/deepseek-flash`. If the PR changes or is closed, this row stays at that commit. One run covers both JS and TS (one `preds.json` and `results.json`, 219 tasks); this board imports its `ts` tasks and sets the other split aside. Every nonempty patch in `preds.json` is identical to its copy in `trajs/<task>/patch.diff`, so nothing is set aside for diverging copies (unlike its Live Go run).
- Before-state checks: [`../live-multilang/*_ts.preimages.json`](../live-multilang/) (metadata and hashes only). Each touched file's old blob and hunks are matched against the task's base commit; patches that cannot be checked are left unmeasured.

## Results (analyzer 0.10.0-beta @ `4c02b61`, `typescript-compiler-units-v1`, Python 3.14.7)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Claude Sonnet 4.5 · Slingshot 2.6.0 | 0.69× | 0.42–1.00× | 23 | +39.1 | +60.0 | 25.2% | 27/28 |
| 2 | GPT-5.6 Sol · Slingshot 3.4.0 | 0.81× | 0.43–1.13× | 43 | +130.2 | +130.8 | 63.1% | 66/70 |
| 3 | Claude Opus 4.6 · AMI Agent 0.7.0 | 0.86× | 0.52–1.22× | 35 | +24.8 | +33.4 | 55.9% | 56/62 |
| 4 | DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 0.99× | 0.68–1.34× | 37 | +21.7 | +43.7 | 50.5% | 54/56 |
| 5 | GPT-5.5 · Slingshot 3.0.0 | 1.17× | 0.92–1.51× | 42 | +109.0 | +111.5 | 46.8% | 51/52 |
| 6 | GPT-5.5 · Slingshot 2.6.0 | 1.38× | 0.97–1.82× | 41 | +107.7 | +113.2 | 41.4% | 45/46 |

| Configuration | Submitted | Measured | Upstream grader error | Unverified before-state | Analysis error | Empty patch | Not in the run |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 111 | 103 | 0 | 4 | 2 | 2 | 0 |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 107 | 103 | 2 | 1 | 1 | 0 | 4 |
| GPT-5.5 · Slingshot 2.6.0 | 111 | 108 | 1 | 1 | 1 | 0 | 0 |
| GPT-5.5 · Slingshot 3.0.0 | 111 | 108 | 0 | 2 | 1 | 0 | 0 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 111 | 106 | 1 | 2 | 2 | 0 | 0 |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 111 | 106 | 3 | 0 | 2 | 0 | 0 |

Grader errors, unverified before-states, analysis errors, empty patches and unsubmitted tasks are not measured and never count as zero. Grader errors and unsubmitted tasks keep an unknown outcome, never a failure.

**TianxiCode.** Its 3 incomplete tasks are reported by the official harness as `incomplete_ids`; they count as grader errors here (unknown outcome, not failure). **Model name:** the run names only the alias `tianxi-agent-plan/deepseek-flash` (`--variant max --thinking`); it is labelled DeepSeek V4.1 Flash, the submitter's own label in the PR title, and the label of its [Live Go](../live-go/README.md) row. Its retries cover infrastructure or model-transport failures only, never grader verdicts (submitter README).

Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md). Records publish scalars and hashes only, not patches. Raw-artifact redistribution is not cleared; see the [Live Python review](../../docs/archive/priority-live-provenance.md), which applies the same terms.

## Reproduce

```sh
# external storage only: the cache holds upstream patches
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase inventory
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase audit
# from a clean checkout, with the analyzer from a worktree at 4c02b61 (its own npm ci), Python 3.14.7:
PYTHONPATH=/path/to/worktree-at-4c02b61 python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase measure
M=examples/live-typescript
python -m parsimony.release freeze $M/population.jsonl --name live-multilang-typescript-v1 --output $M/population-manifest.json
# the panel was frozen with the five earlier runs; TianxiCode is scored against it
python -m parsimony.scoring freeze $M/{claude,gpt}-*.jsonl --name live-multilang-typescript-v1 --population $M/population-manifest.json --output $M/score-panel.json
python -m parsimony.release audit $M/population-manifest.json $M/*-*.jsonl --output $M/coverage.json
python -m parsimony.scoring score $M/score-panel.json $M/*-*.jsonl --output $M/scores.json
python -m parsimony.stability $M/score-panel.json $M/*-*.jsonl --output $M/stability.json
```
