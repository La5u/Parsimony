# Same-task net ratio diagnostics

Panel: `live-multilang-javascript-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 0.562 | 23 | 54/60 | 0.337 | 1–2 | 1–2 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 0.803 | 27 | 72/79 | 0.239 | 1–2 | 1–2 |
| GPT-5.5 · Slingshot 3.0.0 | 1.109 | 27 | 44/46 | 0.279 | 3–4 | 3–5 |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 1.114 | 15 | 21/23 | 0.332 | 3–4 | 3–4 |
| GPT-5.5 · Slingshot 2.6.0 | 1.556 | 25 | 30/31 | 0.230 | 5–5 | 4–5 |

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
