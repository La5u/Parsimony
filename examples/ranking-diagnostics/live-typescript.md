# Same-task net ratio diagnostics

Panel: `live-multilang-typescript-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 0.701 | 23 | 27/28 | 0.253 | 1–2 | 1–2 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 0.784 | 34 | 66/70 | 0.173 | 1–3 | 1–3 |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 0.801 | 33 | 56/62 | 0.204 | 2–3 | 2–3 |
| GPT-5.5 · Slingshot 3.0.0 | 1.260 | 33 | 51/52 | 0.194 | 4–5 | 4–5 |
| GPT-5.5 · Slingshot 2.6.0 | 1.454 | 34 | 45/46 | 0.154 | 4–5 | 4–5 |

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
