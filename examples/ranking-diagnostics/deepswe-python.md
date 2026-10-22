# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-python-26-pooled-80-20-v0.5` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3 Flash Preview · DeepSWE 1.0 | 0.499 | 2 | 2/4 | 0.549 | 1–1 | 1–1 |
| Gemini 3.1 Pro Preview (high) | 0.676 | 8 | 11/11 | 0.184 | 2–2 | 2–2 |
| Claude Fable 5 (xhigh) | 0.808 | 28 | 97/101 | 0.063 | 3–5 | 3–5 |
| Kimi K2.6 · DeepSWE 1.0 | 0.814 | 14 | 23/25 | 0.127 | 3–6 | 3–6 |
| Claude Opus 4.6 (max) · DeepSWE 1.0 | 0.830 | 18 | 35/37 | 0.091 | 4–9 | 4–9 |
| Claude Sonnet 5 (max) | 0.845 | 25 | 78/81 | 0.067 | 6–9 | 5–9 |
| Qwen3.6 Plus · DeepSWE 1.0 | 0.848 | 1 | 1/1 | 1.000 | 6–9 | 6–9 |
| Claude Opus 4.8 (max) | 0.850 | 29 | 83/86 | 0.061 | 5–10 | 5–10 |
| GLM-5.2 (max) | 0.854 | 24 | 53/57 | 0.069 | 7–11 | 7–11 |
| Kimi K3 (max) | 0.857 | 30 | 89/92 | 0.059 | 5–12 | 5–12 |
| Gemini 3.5 Flash (high) | 0.864 | 17 | 38/40 | 0.104 | 6–12 | 6–12 |
| Claude Sonnet 4.6 (high) | 0.870 | 19 | 36/40 | 0.093 | 3–13 | 3–13 |
| MiMo V2.5 Pro · DeepSWE 1.0 | 0.884 | 12 | 20/21 | 0.166 | 12–14 | 12–14 |
| Kimi K2.7 Code | 0.898 | 20 | 32/33 | 0.090 | 13–15 | 13–15 |
| DeepSeek V4 Flash (max) | 0.941 | 27 | 63/66 | 0.063 | 14–17 | 14–17 |
| Qwen3.8 Max (xhigh) | 0.945 | 27 | 74/75 | 0.062 | 15–18 | 15–18 |
| Grok Build 0.1 · DeepSWE 1.0 | 0.957 | 8 | 15/15 | 0.188 | 15–20 | 15–20 |
| Gemini 3.6 Flash (high) | 0.958 | 22 | 53/57 | 0.086 | 16–19 | 16–19 |
| Grok 4.5 (high) | 0.986 | 28 | 79/80 | 0.065 | 18–20 | 18–20 |
| Claude Opus 4.7 (max) · DeepSWE 1.0 | 1.005 | 27 | 63/68 | 0.061 | 19–21 | 19–22 |
| Grok 4.6 (medium) | 1.014 | 28 | 89/92 | 0.057 | 19–22 | 19–22 |
| MiniMax M3 · DeepSWE 1.0 | 1.027 | 12 | 22/24 | 0.132 | 21–27 | 21–27 |
| GPT-5.4 (xhigh) | 1.040 | 25 | 59/63 | 0.067 | 21–27 | 21–27 |
| Gemini 3.7 Flash (medium) | 1.046 | 27 | 80/82 | 0.067 | 20–28 | 20–28 |
| GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 1.053 | 14 | 27/29 | 0.118 | 22–29 | 22–28 |
| GLM-5.3 Flash (max) | 1.056 | 29 | 93/95 | 0.062 | 23–27 | 23–27 |
| GPT-5.6 Sol (max) | 1.069 | 29 | 98/101 | 0.062 | 25–29 | 25–29 |
| GPT-5.6 Terra (max) | 1.075 | 29 | 90/93 | 0.061 | 26–30 | 26–30 |
| GPT-5.5 (xhigh) | 1.082 | 28 | 87/91 | 0.062 | 28–31 | 28–31 |
| DeepSeek V4 Pro (max) | 1.084 | 29 | 77/81 | 0.060 | 27–31 | 27–31 |
| GLM-5.3 (max) | 1.085 | 29 | 87/90 | 0.062 | 25–32 | 25–32 |
| GPT-5.6 Luna (max) | 1.152 | 30 | 85/89 | 0.058 | 31–34 | 31–34 |
| Claude Opus 5 (max) | 1.154 | 28 | 97/101 | 0.065 | 32–33 | 32–33 |
| GLM-5.1 · DeepSWE 1.0 | 1.205 | 8 | 11/13 | 0.193 | 3–35 | 3–35 |
| Muse Spark 1.2 (xhigh) | 1.314 | 27 | 66/69 | 0.064 | 34–35 | 34–35 |
| Muse Spark 1.1 (xhigh) | 1.359 | 24 | 68/72 | 0.072 | 35–36 | 35–36 |
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
