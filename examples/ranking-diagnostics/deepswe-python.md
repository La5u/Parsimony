# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-python-26-pooled-80-20-v0.5` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.1 Pro Preview (high) | 0.663 | 8 | 11/11 | 0.180 | 1–1 | 1–1 |
| Claude Fable 5 (xhigh) | 0.801 | 28 | 97/101 | 0.063 | 2–3 | 2–3 |
| Claude Sonnet 5 (max) | 0.834 | 25 | 78/81 | 0.067 | 3–4 | 3–5 |
| Claude Opus 4.8 (max) | 0.842 | 29 | 83/86 | 0.061 | 3–7 | 3–7 |
| GLM-5.2 (max) | 0.842 | 24 | 53/57 | 0.068 | 3–6 | 3–6 |
| Kimi K3 (max) | 0.848 | 30 | 89/92 | 0.059 | 3–8 | 3–8 |
| Gemini 3.5 Flash (high) | 0.856 | 17 | 38/40 | 0.103 | 3–8 | 3–8 |
| Claude Sonnet 4.6 (high) | 0.867 | 19 | 36/40 | 0.093 | 2–8 | 2–8 |
| Kimi K2.7 Code | 0.889 | 20 | 32/33 | 0.090 | 9–9 | 9–9 |
| DeepSeek V4 Flash (max) | 0.931 | 27 | 63/66 | 0.063 | 10–11 | 10–11 |
| Qwen3.8 Max (xhigh) | 0.934 | 27 | 74/75 | 0.063 | 10–11 | 10–11 |
| Gemini 3.6 Flash (high) | 0.949 | 22 | 53/57 | 0.085 | 12–12 | 11–12 |
| Grok 4.5 (high) | 0.976 | 28 | 79/80 | 0.064 | 13–13 | 13–13 |
| Grok 4.6 (medium) | 1.004 | 28 | 89/92 | 0.058 | 14–15 | 14–15 |
| GPT-5.4 (xhigh) | 1.032 | 25 | 59/63 | 0.066 | 15–18 | 15–18 |
| Gemini 3.7 Flash (medium) | 1.041 | 27 | 80/82 | 0.067 | 14–19 | 14–19 |
| GLM-5.3 Flash (max) | 1.047 | 29 | 93/95 | 0.062 | 15–18 | 15–18 |
| GPT-5.6 Sol (max) | 1.060 | 29 | 98/101 | 0.062 | 17–19 | 17–19 |
| GPT-5.6 Terra (max) | 1.067 | 29 | 90/93 | 0.060 | 18–21 | 18–21 |
| GPT-5.5 (xhigh) | 1.074 | 28 | 87/91 | 0.062 | 19–22 | 19–22 |
| DeepSeek V4 Pro (max) | 1.075 | 29 | 77/81 | 0.060 | 19–22 | 19–22 |
| GLM-5.3 (max) | 1.075 | 29 | 87/90 | 0.062 | 16–22 | 16–22 |
| GPT-5.6 Luna (max) | 1.143 | 30 | 85/89 | 0.058 | 23–24 | 23–24 |
| Claude Opus 5 (max) | 1.144 | 28 | 97/101 | 0.064 | 23–24 | 23–24 |
| Muse Spark 1.2 (xhigh) | 1.309 | 27 | 66/69 | 0.063 | 25–25 | 25–25 |
| Muse Spark 1.1 (xhigh) | 1.352 | 24 | 68/72 | 0.071 | 26–26 | 26–26 |

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
