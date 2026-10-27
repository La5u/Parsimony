# Same-task net ratio diagnostics

Panel: `live-multilang-typescript-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 0.692 | 23 | 27/28 | 0.250 | 1–1 | 1–1 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 0.815 | 43 | 66/70 | 0.139 | 2–3 | 2–3 |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 0.861 | 35 | 56/62 | 0.201 | 2–4 | 2–4 |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 0.990 | 37 | 54/56 | 0.101 | 2–4 | 2–4 |
| GPT-5.5 · Slingshot 3.0.0 | 1.167 | 42 | 51/52 | 0.150 | 5–5 | 5–5 |
| GPT-5.5 · Slingshot 2.6.0 | 1.379 | 41 | 45/46 | 0.124 | 6–6 | 6–6 |

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
