# Same-task net ratio diagnostics

Panel: `live-multilang-javascript-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.5 · Slingshot 3.0.0 | 0.789 | 37 | 44/46 | 0.225 | 1–3 | 1–3 |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 0.867 | 34 | 54/60 | 0.278 | 1–5 | 1–4 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 0.975 | 39 | 72/79 | 0.218 | 1–4 | 1–5 |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 1.022 | 18 | 21/23 | 0.309 | 3–5 | 3–5 |
| GPT-5.5 · Slingshot 2.6.0 | 1.230 | 28 | 30/31 | 0.225 | 2–6 | 1–6 |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 1.281 | 36 | 55/58 | 0.214 | 4–6 | 4–6 |

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
