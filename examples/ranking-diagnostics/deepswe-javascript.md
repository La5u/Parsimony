# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-javascript-26-pooled-80-20-v0.7` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.1 Pro Preview (high) | 0.546 | 2 | 2/2 | 0.589 | 1–2 | 1–2 |
| Gemini 3.5 Flash (high) | 0.792 | 4 | 10/10 | 0.453 | 2–4 | 2–4 |
| Claude Fable 5 (xhigh) | 0.800 | 4 | 14/14 | 0.312 | 1–6 | 1–6 |
| Claude Opus 4.8 (max) | 0.830 | 3 | 8/8 | 0.413 | 3–6 | 3–6 |
| Kimi K2.7 Code | 0.843 | 2 | 5/5 | 0.585 | 3–10 | 2–10 |
| Gemini 3.6 Flash (high) | 0.858 | 4 | 11/11 | 0.312 | 6–8 | 6–8 |
| GPT-5.5 (xhigh) | 0.885 | 4 | 10/10 | 0.459 | 2–17 | 3–17 |
| Kimi K3 (max) | 0.911 | 5 | 13/13 | 0.398 | 5–13 | 5–13 |
| Qwen3.8 Max (xhigh) | 0.927 | 4 | 13/13 | 0.492 | 7–15 | 7–15 |
| GPT-5.6 Terra (max) | 0.931 | 4 | 14/14 | 0.492 | 9–14 | 9–14 |
| GLM-5.2 (max) | 0.932 | 2 | 6/6 | 0.585 | 7–20 | 8–20 |
| Claude Sonnet 5 (max) | 0.942 | 5 | 11/11 | 0.394 | 3–17 | 3–17 |
| GLM-5.3 (max) | 0.958 | 5 | 18/18 | 0.400 | 10–15 | 9–15 |
| DeepSeek V4 Flash (max) | 0.972 | 3 | 7/7 | 0.412 | 10–16 | 10–16 |
| Gemini 3.7 Flash (medium) | 1.018 | 5 | 11/11 | 0.397 | 11–22 | 11–22 |
| GPT-5.6 Luna (max) | 1.024 | 5 | 12/12 | 0.404 | 11–22 | 11–22 |
| GPT-5.6 Sol (max) | 1.026 | 4 | 15/15 | 0.493 | 12–21 | 12–21 |
| GPT-5.4 (xhigh) | 1.027 | 4 | 7/7 | 0.499 | 8–24 | 8–24 |
| Grok 4.5 (high) | 1.051 | 3 | 8/8 | 0.574 | 10–23 | 10–23 |
| GLM-5.3 Flash (max) | 1.063 | 4 | 12/12 | 0.310 | 16–22 | 16–22 |
| DeepSeek V4 Pro (max) | 1.066 | 4 | 13/13 | 0.491 | 18–21 | 18–21 |
| Claude Sonnet 4.6 (high) | 1.073 | 3 | 8/8 | 0.571 | 5–24 | 5–24 |
| Grok 4.6 (medium) | 1.124 | 5 | 16/16 | 0.397 | 18–25 | 18–25 |
| Claude Opus 5 (max) | 1.178 | 4 | 13/13 | 0.309 | 21–26 | 21–26 |
| Muse Spark 1.2 (xhigh) | 1.300 | 5 | 11/11 | 0.409 | 23–26 | 23–26 |
| Muse Spark 1.1 (xhigh) | 1.304 | 5 | 9/9 | 0.409 | 24–26 | 24–25 |

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
