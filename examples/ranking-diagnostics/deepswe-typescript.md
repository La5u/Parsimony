# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-typescript-26-pooled-80-20-v0.7` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Kimi K2.7 Code | 0.812 | 19 | 38/39 | 0.099 | 1–3 | 1–3 |
| Gemini 3.1 Pro Preview (high) | 0.820 | 8 | 16/17 | 0.228 | 1–3 | 1–3 |
| Gemini 3.5 Flash (high) | 0.830 | 20 | 47/51 | 0.115 | 1–5 | 1–5 |
| Claude Fable 5 (xhigh) | 0.844 | 29 | 83/89 | 0.068 | 3–5 | 3–5 |
| Claude Opus 4.8 (max) | 0.848 | 22 | 61/64 | 0.091 | 4–5 | 4–5 |
| GLM-5.2 (max) | 0.887 | 27 | 58/61 | 0.071 | 6–8 | 6–8 |
| Claude Sonnet 4.6 (high) | 0.898 | 16 | 40/44 | 0.119 | 6–8 | 6–8 |
| Claude Sonnet 5 (max) | 0.902 | 25 | 62/69 | 0.087 | 6–9 | 6–9 |
| Kimi K3 (max) | 0.928 | 27 | 77/84 | 0.070 | 8–10 | 8–10 |
| Gemini 3.6 Flash (high) | 0.951 | 23 | 55/57 | 0.084 | 9–13 | 9–13 |
| Qwen3.8 Max (xhigh) | 0.954 | 27 | 68/75 | 0.080 | 10–12 | 10–12 |
| Grok 4.6 (medium) | 0.956 | 24 | 73/81 | 0.091 | 10–13 | 10–13 |
| DeepSeek V4 Flash (max) | 0.969 | 24 | 66/73 | 0.091 | 12–15 | 12–15 |
| GLM-5.3 (max) | 0.978 | 26 | 80/85 | 0.081 | 12–16 | 12–18 |
| Grok 4.5 (high) | 0.980 | 25 | 61/68 | 0.073 | 10–16 | 10–16 |
| GLM-5.3 Flash (max) | 0.990 | 26 | 68/72 | 0.072 | 14–16 | 13–16 |
| GPT-5.6 Terra (max) | 1.025 | 29 | 84/91 | 0.074 | 17–19 | 17–19 |
| DeepSeek V4 Pro (max) | 1.028 | 27 | 81/86 | 0.081 | 17–19 | 16–19 |
| GPT-5.6 Sol (max) | 1.042 | 29 | 88/92 | 0.074 | 18–21 | 17–20 |
| GPT-5.6 Luna (max) | 1.047 | 27 | 77/81 | 0.080 | 18–21 | 18–22 |
| Claude Opus 5 (max) | 1.050 | 28 | 82/88 | 0.078 | 18–21 | 18–21 |
| Gemini 3.7 Flash (medium) | 1.089 | 26 | 82/86 | 0.084 | 22–23 | 19–23 |
| GPT-5.5 (xhigh) | 1.101 | 28 | 82/87 | 0.076 | 22–24 | 22–23 |
| GPT-5.4 (xhigh) | 1.123 | 25 | 66/70 | 0.081 | 23–24 | 24–24 |
| Muse Spark 1.2 (xhigh) | 1.302 | 24 | 67/71 | 0.082 | 25–26 | 25–26 |
| Muse Spark 1.1 (xhigh) | 1.365 | 25 | 63/68 | 0.086 | 25–26 | 25–26 |

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
