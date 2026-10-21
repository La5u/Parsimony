# Same-task net ratio diagnostics

Panel: `live-lite-python-300-80-20-v0.5` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.5 · agav 0.2.0-beta.2 | 0.792 | 73 | 185/186 | 0.240 | 1–3 | 1–3 |
| DeepSeek V4.1 Flash · TianxiCode 0.1.423 | 0.870 | 73 | 202/204 | 0.245 | 1–4 | 1–4 |
| Claude Opus 4.8 · AiWork.Code | 1.163 | 73 | 102/102 | 0.158 | 1–4 | 1–4 |
| GPT-5.6 Sol · Slingshot 3.4.0 | 1.206 | 73 | 205/211 | 0.156 | 2–4 | 2–4 |

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
