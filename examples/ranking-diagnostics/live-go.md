# Same-task net ratio diagnostics

Panel: `live-multilang-go-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Claude Haiku 4.5 · AMI Agent 0.7.0 | 0.862 | 65 | 82/90 | 0.229 | 1–3 | 1–3 |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 0.878 | 69 | 97/103 | 0.195 | 1–3 | 1–3 |
| Gemini 3.6 Flash · AMI Agent 0.7.0 | 0.899 | 61 | 72/78 | 0.219 | 1–3 | 1–3 |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 1.029 | 60 | 64/72 | 0.090 | 4–4 | 4–4 |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 | 1.231 | 65 | 91/99 | 0.176 | 5–5 | 5–5 |
| Qwen3.8-27B · AMI Agent 0.7.2 | 1.483 | 31 | 39/41 | 0.217 | 6–6 | 6–6 |

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
