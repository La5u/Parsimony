# SWE-bench Live MultiLang — Go

Website: **[parsimony.lasu.dev/live-go.html](https://parsimony.lasu.dev/live-go.html)**.

Seven public submissions to [SWE-bench Live](https://swe-bench-live.github.io) MultiLang on all **138** tasks of its `go` split: six from the same submitter's **AMI Agent**, and **DeepSeek V4.1 Flash · TianxiCode** (Lenovo). The six AMI runs share a harness, so their model differences are less confounded than on the other Live boards, but AMI versions and retry settings differ (below). Pass/fail is the submitter's own evaluation report, not rechecked here. Includes **Qwen3.8-27B**, an open-weight model the submitter self-hosted.

This is separate from the DeepSWE Go board: different tasks and harness. Never pool them.

## Sources

- Tasks: Hugging Face [`SWE-bench-Live/MultiLang` at `62dc074`](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/62dc0745c40f067fc366ae3eb1a26136e5928f85), `data/go-00000-of-00001.parquet`.
- Runs: GitHub [`SWE-bench-Live/submission` at `99bae66`](https://github.com/SWE-bench-Live/submission/tree/99bae66f923b3dfeab2d18366c0593929c5722de/submissions/multilang/go/ami-agent), `submissions/multilang/go/ami-agent/<config>`; TianxiCode at [`641b727`](https://github.com/SWE-bench-Live/submission/tree/641b727c8a5e3e5d0af08a348e632b12c3f11aef/submissions/multilang/go/tianxi/deepseek-flash) (added 2026-10-16), `submissions/multilang/go/tianxi/deepseek-flash`.
- Before-state checks: [`../live-multilang/*_go.preimages.json`](../live-multilang/) (metadata and hashes only).

## Results (analyzer 0.10.0-beta @ `9dd189a`, `tree-sitter-go-units-v2`, Python 3.14.7)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Claude Haiku 4.5 · AMI Agent 0.7.0 | 0.83× | 0.67–1.06× | 73 | +69.8 | +222.3 | 65.2% | 82/90 |
| 2 | Claude Opus 4.6 · AMI Agent 0.7.0 | 0.88× | 0.74–1.07× | 81 | +123.6 | +125.0 | 74.6% | 97/103 |
| 3 | Gemini 3.6 Flash · AMI Agent 0.7.0 | 0.89× | 0.74–1.09× | 68 | +322.2 | +233.0 | 56.5% | 72/78 |
| 4 | Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 1.01× | 0.85–1.19× | 61 | +333.4 | +221.1 | 52.2% | 64/72 |
| 5 | Claude Sonnet 4.6 · AMI Agent 0.7.0 | 1.13× | 0.90–1.34× | 77 | +114.6 | +114.8 | 71.7% | 91/99 |
| 6 | Qwen3.8-27B · AMI Agent 0.7.2 | 1.24× | 0.95–1.64× | 33 | +81.2 | +69.9 | 29.7% | 39/41 |
| 7 | DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 1.24× | 0.81–1.51× | 66 | +100.2 | +103.1 | 63.8% | 82/88 |

| Configuration | Submitted | Measured | Unverified before-state | Empty patch | Retries of failed instances (submitter README) |
|---|---:|---:|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 (2026-07-16) | 138 | 137 | 1 | 0 | 2 |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 (2026-07-23) | 138 | 133 | 5 | 0 | 2 |
| Claude Haiku 4.5 · AMI Agent 0.7.0 (2026-07-29) | 138 | 124 | 4 | 10 | 2 |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 (2026-07-29) | 130 | 124 | 6 | 8 | 15 |
| Gemini 3.6 Flash · AMI Agent 0.7.0 (2026-07-29) | 130 | 128 | 2 | 8 | 5 |
| Qwen3.8-27B (self-hosted, vLLM) · AMI Agent 0.7.2 (2026-09-23) | 138 | 130 | 2 | 6 | not stated |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 (2026-10-13) | 138 | 113 | 0 | 1 | infrastructure/API failures only |

**Retries differ.** Each submitter README says failed instances were re-run up to the number of times shown. More retries can raise Solved, most for the Gemini runs; the footprint is still that of the submitted patch. Unverified before-states and empty patches are not measured and never count as zero. No analysis errors.

**TianxiCode: 24 tasks set aside.** The submission has each patch twice, in `preds.json` and in `trajs/<task>/patch.diff`. They are identical on 113 tasks but differ in content on 24 (23 reported failures, 1 success), and the logs don't show which copy was evaluated. Those 24 are not measured (`not_selected`), never zero; the list is in `examples/benchmark-discovery/run-live-multilang.py`. **Model name:** the run names only the alias `tianxi-agent-plan/deepseek-flash`. It is labelled DeepSeek V4.1 Flash because TianxiCode's September Live Lite README described that alias as DeepSeek V4.1 Flash (see the [Live Python board](../live-python/README.md)); this run's README states no version.

Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md). Records publish scalars and hashes only, not patches; raw-artifact redistribution is not cleared (same terms as the [Live Python review](../../docs/archive/priority-live-provenance.md)).

## Reproduce

Needs the pinned Go grammar: `pip install tree-sitter==0.26.0 "tree-sitter-go @ <URL#sha256 in pyproject.toml>"` (pip, not uv, so the source URL is recorded).

```sh
GO="--cohort ami_claude_opus_4_6_go --cohort ami_claude_sonnet_4_6_go --cohort ami_claude_haiku_4_5_go --cohort ami_gemini_3_1_pro_preview_go --cohort ami_gemini_3_6_flash_go --cohort ami_qwen3_8_27b_go --cohort tianxicode_deepseek_v4_1_flash_go"
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase inventory $GO
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase audit $GO
# from a clean checkout, with the analyzer from a worktree at 9dd189a:
PYTHONPATH=/path/to/worktree-at-9dd189a python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase measure $GO
M=examples/live-go
python -m parsimony.release freeze $M/population.jsonl --name live-multilang-go-v1 --output $M/population-manifest.json
# the panel was frozen with the six AMI runs; TianxiCode is scored against it
python -m parsimony.scoring freeze $M/*-ami*.jsonl --name live-multilang-go-v1 --population $M/population-manifest.json --output $M/score-panel.json
python -m parsimony.release audit $M/population-manifest.json $M/*-*.jsonl --output $M/coverage.json
python -m parsimony.scoring score $M/score-panel.json $M/*-*.jsonl --output $M/scores.json
python -m parsimony.stability $M/score-panel.json $M/*-*.jsonl --output $M/stability.json
```
