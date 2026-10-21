# Same-task net ratio diagnostics

Panel: `live-multilang-go-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Claude Haiku 4.5 · AMI Agent 0.7.0 | 0.827 | 73 | 82/90 | 0.218 | 1–2 | 1–2 |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 0.876 | 81 | 97/103 | 0.187 | 1–3 | 1–3 |
| Gemini 3.6 Flash · AMI Agent 0.7.0 | 0.891 | 68 | 72/78 | 0.218 | 2–3 | 2–3 |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 1.013 | 61 | 64/72 | 0.086 | 4–4 | 4–5 |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 | 1.126 | 77 | 91/99 | 0.168 | 5–5 | 4–5 |
| Qwen3.8-27B · AMI Agent 0.7.2 | 1.239 | 33 | 39/41 | 0.191 | 6–7 | 6–7 |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 1.242 | 66 | 82/88 | 0.212 | 6–7 | 6–7 |

Largest task share is the largest absolute per-task peer footprint divided by the total peer footprint; cancellation can make it exceed 1. Unavailable perturbations are counted separately in JSON, not included in rank ranges.

## Interpretation

- Descriptive sensitivity, not confidence intervals or a replacement ranking.
- Successful measured repairs only; missing footprints are not imputed.
- Each task/repository deletion preserves peer eligibility rules; peer deletion recomputes them.
- Peer rank changes exclude the mechanical effect of removing a competing candidate.
- Pairwise comparisons use all shared solved measured base tasks, without the three-peer gate.
- Repository omission tests influence; it is not a repository-cluster bootstrap.
- Harness, retry policy and upstream outcome validity are not inferred from model labels.
- Combined-language ranking is not evaluated; run this separately for each language board.

JSON includes missing-success reasons, top task/repository/peer influences, unavailable scenarios, and pairwise matched-task means. Rank ranges are sensitivity extrema, not 95% intervals.
