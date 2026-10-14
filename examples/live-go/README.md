# SWE-bench Live MultiLang — Go

Website: **[parsimony.lasu.dev/live-go.html](https://parsimony.lasu.dev/live-go.html)**.

Six public submissions to [SWE-bench Live](https://swe-bench-live.github.io) MultiLang, all from the same submitter's **AMI Agent**, on all **138** tasks of its `go` split. One harness, so model differences are less confounded than on the other Live boards, but AMI versions and retry settings differ (below). Pass/fail is the submitter's own evaluation report, not rechecked here. Includes **Qwen3.8-27B**, an open-weight model the submitter self-hosted.

This is separate from the DeepSWE Go board: different tasks and harness. Never pool them.

## Sources

- Tasks: Hugging Face [`SWE-bench-Live/MultiLang` at `62dc074`](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/62dc0745c40f067fc366ae3eb1a26136e5928f85), `data/go-00000-of-00001.parquet`.
- Runs: GitHub [`SWE-bench-Live/submission` at `99bae66`](https://github.com/SWE-bench-Live/submission/tree/99bae66f923b3dfeab2d18366c0593929c5722de/submissions/multilang/go/ami-agent), `submissions/multilang/go/ami-agent/<config>`.
- Before-state checks: [`../live-multilang/*_go.preimages.json`](../live-multilang/) (metadata and hashes only).

## Results (analyzer 0.10.0-beta @ `9dd189a`, `tree-sitter-go-units-v2`, Python 3.14.7)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Claude Haiku 4.5 · AMI Agent 0.7.0 | 0.86× | 0.74–1.02× | 65 | +69.8 | +222.3 | 65.2% | 82/90 |
| 2 | Claude Opus 4.6 · AMI Agent 0.7.0 | 0.88× | 0.75–1.03× | 69 | +123.6 | +125.0 | 74.6% | 97/103 |
| 3 | Gemini 3.6 Flash · AMI Agent 0.7.0 | 0.90× | 0.73–1.10× | 61 | +322.2 | +233.0 | 56.5% | 72/78 |
| 4 | Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 1.03× | 0.85–1.22× | 60 | +333.4 | +221.1 | 52.2% | 64/72 |
| 5 | Claude Sonnet 4.6 · AMI Agent 0.7.0 | 1.23× | 0.93–1.56× | 65 | +114.6 | +114.8 | 71.7% | 91/99 |
| 6 | Qwen3.8-27B · AMI Agent 0.7.2 | 1.48× | 1.12–2.12× | 31 | +81.2 | +69.9 | 29.7% | 39/41 |

| Configuration | Submitted | Measured | Unverified before-state | Empty patch | Retries of failed instances (submitter README) |
|---|---:|---:|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 (2026-07-16) | 138 | 137 | 1 | 0 | 2 |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 (2026-07-23) | 138 | 133 | 5 | 0 | 2 |
| Claude Haiku 4.5 · AMI Agent 0.7.0 (2026-07-29) | 138 | 124 | 4 | 10 | 2 |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 (2026-07-29) | 130 | 124 | 6 | 8 | 15 |
| Gemini 3.6 Flash · AMI Agent 0.7.0 (2026-07-29) | 130 | 128 | 2 | 8 | 5 |
| Qwen3.8-27B (self-hosted, vLLM) · AMI Agent 0.7.2 (2026-09-23) | 138 | 130 | 2 | 6 | not stated |

**Retries differ.** Each submitter README says failed instances were re-run up to the number of times shown. More retries can raise Solved, most for the Gemini runs; the footprint is still that of the submitted patch. Unverified before-states and empty patches are not measured and never count as zero. No analysis errors.

Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md). Records publish scalars and hashes only, not patches; raw-artifact redistribution is not cleared (same terms as the [Live Python review](../../docs/archive/priority-live-provenance.md)).

## Reproduce

Needs the pinned Go grammar: `pip install tree-sitter==0.26.0 "tree-sitter-go @ <URL#sha256 in pyproject.toml>"` (pip, not uv, so the source URL is recorded).

```sh
GO="--cohort ami_claude_opus_4_6_go --cohort ami_claude_sonnet_4_6_go --cohort ami_claude_haiku_4_5_go --cohort ami_gemini_3_1_pro_preview_go --cohort ami_gemini_3_6_flash_go --cohort ami_qwen3_8_27b_go"
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase inventory $GO
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase audit $GO
# from a clean worktree at the analyzer commit:
PYTHONPATH=. python examples/benchmark-discovery/run-live-multilang.py --output-dir /tmp/live-ml --phase measure $GO
M=examples/live-go
python -m parsimony.release freeze $M/population.jsonl --name live-multilang-go-v1 --output $M/population-manifest.json
python -m parsimony.scoring freeze $M/*-ami*.jsonl --name live-multilang-go-v1 --population $M/population-manifest.json --output $M/score-panel.json
python -m parsimony.release audit $M/population-manifest.json $M/*-ami*.jsonl --output $M/coverage.json
python -m parsimony.scoring score $M/score-panel.json $M/*-ami*.jsonl --output $M/scores.json
python -m parsimony.stability $M/score-panel.json $M/*-ami*.jsonl --output $M/stability.json
```
