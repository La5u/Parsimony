# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-go-v0.8-pooled-archived-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.1 Pro Preview (high) | 0.702 | 11 | 20/20 | 0.173 | 1–1 | 1–1 |
| Claude Fable 5 (xhigh) | 0.820 | 31 | 97/97 | 0.069 | 2–2 | 2–2 |
| Claude Opus 4.8 (max) | 0.858 | 29 | 84/84 | 0.073 | 3–4 | 3–4 |
| Claude Sonnet 5 (max) | 0.865 | 27 | 67/67 | 0.079 | 3–5 | 3–5 |
| Kimi K2.7 Code | 0.874 | 24 | 58/58 | 0.090 | 3–7 | 3–7 |
| Gemini 3.5 Flash (high) | 0.876 | 24 | 54/54 | 0.095 | 5–7 | 5–7 |
| Claude Sonnet 4.6 (high) | 0.883 | 21 | 36/36 | 0.099 | 3–9 | 3–9 |
| GLM-5.2 (max) | 0.887 | 28 | 67/67 | 0.077 | 6–9 | 6–9 |
| Kimi K3 (max) | 0.889 | 32 | 107/107 | 0.068 | 5–9 | 6–9 |
| Gemini 3.6 Flash (high) | 0.914 | 30 | 80/80 | 0.076 | 10–11 | 10–11 |
| Qwen3.8 Max (xhigh) | 0.919 | 28 | 84/84 | 0.074 | 10–11 | 10–11 |
| DeepSeek V4 Flash (max) | 0.975 | 29 | 84/84 | 0.074 | 12–12 | 12–12 |
| GLM-5.3 (max) | 1.001 | 32 | 104/104 | 0.068 | 13–15 | 13–15 |
| GLM-5.3 Flash (max) | 1.004 | 31 | 94/94 | 0.069 | 13–16 | 13–16 |
| Gemini 3.7 Flash (medium) | 1.014 | 29 | 102/102 | 0.073 | 13–16 | 13–16 |
| Grok 4.5 (high) | 1.022 | 25 | 77/77 | 0.082 | 15–17 | 15–17 |
| Grok 4.6 (medium) | 1.027 | 30 | 100/100 | 0.071 | 16–18 | 16–18 |
| Claude Opus 5 (max) | 1.044 | 32 | 108/108 | 0.068 | 16–18 | 16–18 |
| DeepSeek V4 Pro (max) | 1.081 | 32 | 91/91 | 0.068 | 19–20 | 19–20 |
| GPT-5.5 (xhigh) | 1.088 | 32 | 102/102 | 0.068 | 19–21 | 19–21 |
| GPT-5.6 Sol (max) | 1.106 | 30 | 107/107 | 0.072 | 19–22 | 19–22 |
| GPT-5.6 Terra (max) | 1.108 | 32 | 105/105 | 0.070 | 21–22 | 21–22 |
| GPT-5.6 Luna (max) | 1.132 | 33 | 107/107 | 0.066 | 23–24 | 23–24 |
| GPT-5.4 (xhigh) | 1.143 | 28 | 86/86 | 0.077 | 23–24 | 23–24 |
| Muse Spark 1.2 (xhigh) | 1.240 | 29 | 85/85 | 0.075 | 25–25 | 25–25 |
| Muse Spark 1.1 (xhigh) | 1.282 | 28 | 81/81 | 0.079 | 26–26 | 26–26 |

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
