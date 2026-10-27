# Same-task net ratio diagnostics

Panel: `swe-polybench-verified-python-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.6 Sol · Slingshot 3.4.0 | 0.650 | 60 | 64/64 | 0.434 | 1–1 | 1–2 |
| DeepSeek V4 Flash (max) · Mobile Coder 1.2.4 | 1.013 | 59 | 80/80 | 0.349 | 2–3 | 2–3 |
| Claude Opus 4.8 · HMigBot | 1.034 | 60 | 69/70 | 0.219 | 2–3 | 2–5 |
| Claude Opus 5.5 (high) · AiWork.Code | 1.125 | 64 | 80/80 | 0.345 | 4–5 | 1–4 |
| Claude Opus 5.5 (high) · Jitto Build (Claude Code) | 1.178 | 67 | 97/97 | 0.357 | 4–5 | 4–5 |

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
