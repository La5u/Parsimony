# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-typescript-26-pooled-80-20-v0.7` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3 Flash Preview · DeepSWE 1.0 | 0.764 | 4 | 5/5 | 0.482 | 1–6 | 1–6 |
| Gemini 3.1 Pro Preview (high) | 0.811 | 8 | 16/17 | 0.226 | 1–4 | 1–4 |
| Kimi K2.7 Code | 0.821 | 19 | 38/39 | 0.102 | 2–4 | 2–4 |
| Gemini 3.5 Flash (high) | 0.832 | 20 | 47/51 | 0.114 | 3–6 | 3–6 |
| Claude Fable 5 (xhigh) | 0.848 | 29 | 83/89 | 0.069 | 4–6 | 4–6 |
| Claude Opus 4.8 (max) | 0.850 | 22 | 61/64 | 0.092 | 4–6 | 4–6 |
| MiMo V2.5 Pro · DeepSWE 1.0 | 0.887 | 15 | 32/36 | 0.130 | 7–10 | 7–10 |
| GLM-5.2 (max) | 0.894 | 27 | 58/61 | 0.073 | 7–10 | 7–10 |
| Claude Sonnet 4.6 (high) | 0.904 | 16 | 40/44 | 0.122 | 8–11 | 8–11 |
| Claude Sonnet 5 (max) | 0.904 | 25 | 62/69 | 0.086 | 7–12 | 7–13 |
| GLM-5.1 · DeepSWE 1.0 | 0.908 | 13 | 30/32 | 0.163 | 9–12 | 9–12 |
| Kimi K3 (max) | 0.932 | 27 | 77/84 | 0.071 | 11–15 | 11–15 |
| Grok Build 0.1 · DeepSWE 1.0 | 0.948 | 6 | 14/16 | 0.262 | 11–29 | 11–29 |
| Gemini 3.6 Flash (high) | 0.956 | 23 | 55/57 | 0.085 | 12–18 | 12–18 |
| Grok 4.6 (medium) | 0.960 | 24 | 73/81 | 0.090 | 14–18 | 14–17 |
| Qwen3.8 Max (xhigh) | 0.961 | 27 | 68/75 | 0.080 | 13–18 | 13–18 |
| Kimi K2.6 · DeepSWE 1.0 | 0.962 | 12 | 28/28 | 0.165 | 11–20 | 11–20 |
| DeepSeek V4 Flash (max) | 0.974 | 24 | 66/73 | 0.091 | 16–21 | 16–21 |
| Claude Opus 4.6 (max) · DeepSWE 1.0 | 0.981 | 16 | 40/44 | 0.115 | 12–23 | 12–23 |
| GLM-5.3 (max) | 0.981 | 26 | 80/85 | 0.081 | 16–23 | 16–27 |
| Grok 4.5 (high) | 0.987 | 25 | 61/68 | 0.071 | 14–23 | 14–23 |
| GLM-5.3 Flash (max) | 0.991 | 26 | 68/72 | 0.073 | 19–23 | 19–23 |
| Claude Opus 4.7 (max) · DeepSWE 1.0 | 1.004 | 27 | 70/73 | 0.079 | 21–25 | 21–25 |
| GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 1.022 | 9 | 14/17 | 0.239 | 18–30 | 18–30 |
| MiniMax M3 · DeepSWE 1.0 | 1.026 | 18 | 28/32 | 0.107 | 21–30 | 21–30 |
| GPT-5.6 Terra (max) | 1.032 | 29 | 84/91 | 0.074 | 23–28 | 23–28 |
| DeepSeek V4 Pro (max) | 1.033 | 27 | 81/86 | 0.081 | 24–28 | 25–28 |
| GPT-5.6 Sol (max) | 1.048 | 29 | 88/92 | 0.074 | 24–30 | 24–30 |
| Claude Opus 5 (max) | 1.050 | 28 | 82/88 | 0.077 | 26–31 | 26–31 |
| GPT-5.6 Luna (max) | 1.051 | 27 | 77/81 | 0.080 | 27–30 | 27–31 |
| Gemini 3.7 Flash (medium) | 1.091 | 26 | 82/86 | 0.084 | 31–32 | 28–32 |
| GPT-5.5 (xhigh) | 1.106 | 28 | 82/87 | 0.076 | 31–33 | 31–33 |
| GPT-5.4 (xhigh) | 1.126 | 25 | 66/70 | 0.081 | 32–34 | 33–34 |
| Qwen3.6 Plus · DeepSWE 1.0 | 1.255 | 2 | 2/2 | 0.873 | 13–34 | 13–34 |
| Muse Spark 1.2 (xhigh) | 1.305 | 24 | 67/71 | 0.083 | 35–36 | 35–36 |
| Muse Spark 1.1 (xhigh) | 1.371 | 25 | 63/68 | 0.086 | 35–36 | 35–36 |
| Claude Haiku 4.5 · DeepSWE 1.0 | — | 0 | 0/0 | — | — | — |
| MiniMax M2.7 · DeepSWE 1.0 | — | 0 | 0/0 | — | — | — |

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
