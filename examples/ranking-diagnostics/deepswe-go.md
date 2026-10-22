# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-go-v0.8-pooled-archived-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3 Flash Preview · DeepSWE 1.0 | 0.633 | 7 | 10/10 | 0.291 | 1–1 | 1–2 |
| Gemini 3.1 Pro Preview (high) | 0.708 | 11 | 20/20 | 0.175 | 2–2 | 1–2 |
| Grok Build 0.1 · DeepSWE 1.0 | 0.825 | 13 | 19/19 | 0.183 | 3–5 | 3–5 |
| Claude Fable 5 (xhigh) | 0.829 | 31 | 97/97 | 0.070 | 3–5 | 3–5 |
| Kimi K2.6 · DeepSWE 1.0 | 0.850 | 22 | 39/39 | 0.097 | 3–7 | 3–7 |
| GLM-5.1 · DeepSWE 1.0 | 0.861 | 15 | 23/23 | 0.143 | 5–9 | 5–9 |
| Claude Opus 4.8 (max) | 0.867 | 29 | 84/84 | 0.074 | 6–8 | 6–8 |
| Claude Sonnet 5 (max) | 0.874 | 27 | 67/67 | 0.079 | 7–10 | 7–10 |
| MiMo V2.5 Pro · DeepSWE 1.0 | 0.879 | 16 | 23/23 | 0.131 | 5–14 | 5–14 |
| Kimi K2.7 Code | 0.887 | 24 | 58/58 | 0.091 | 7–14 | 8–14 |
| Claude Sonnet 4.6 (high) | 0.891 | 21 | 36/36 | 0.100 | 7–14 | 7–14 |
| Gemini 3.5 Flash (high) | 0.891 | 24 | 54/54 | 0.096 | 9–13 | 9–13 |
| GLM-5.2 (max) | 0.895 | 28 | 67/67 | 0.077 | 10–14 | 10–14 |
| Kimi K3 (max) | 0.898 | 32 | 107/107 | 0.068 | 9–14 | 10–14 |
| Claude Opus 4.6 (max) · DeepSWE 1.0 | 0.918 | 15 | 27/27 | 0.138 | 11–17 | 11–17 |
| Gemini 3.6 Flash (high) | 0.924 | 30 | 80/80 | 0.077 | 15–17 | 15–17 |
| Qwen3.8 Max (xhigh) | 0.928 | 28 | 84/84 | 0.075 | 15–17 | 15–17 |
| DeepSeek V4 Flash (max) | 0.984 | 29 | 84/84 | 0.074 | 18–19 | 18–19 |
| GLM-5.3 (max) | 1.011 | 32 | 104/104 | 0.068 | 19–21 | 19–21 |
| GLM-5.3 Flash (max) | 1.012 | 31 | 94/94 | 0.069 | 19–22 | 19–22 |
| Gemini 3.7 Flash (medium) | 1.021 | 29 | 102/102 | 0.073 | 19–24 | 19–24 |
| MiniMax M3 · DeepSWE 1.0 | 1.025 | 17 | 24/24 | 0.125 | 18–25 | 18–25 |
| Claude Opus 4.7 (max) · DeepSWE 1.0 | 1.029 | 31 | 77/78 | 0.071 | 21–25 | 21–25 |
| Grok 4.5 (high) | 1.030 | 25 | 77/77 | 0.082 | 21–25 | 21–25 |
| Grok 4.6 (medium) | 1.036 | 30 | 100/100 | 0.072 | 22–26 | 22–26 |
| Claude Opus 5 (max) | 1.053 | 32 | 108/108 | 0.069 | 25–26 | 25–26 |
| DeepSeek V4 Pro (max) | 1.092 | 32 | 91/91 | 0.069 | 27–28 | 27–28 |
| GPT-5.5 (xhigh) | 1.099 | 32 | 102/102 | 0.069 | 27–29 | 27–29 |
| Qwen3.6 Plus · DeepSWE 1.0 | 1.117 | 7 | 8/8 | 0.261 | 27–32 | 27–32 |
| GPT-5.6 Sol (max) | 1.117 | 30 | 107/107 | 0.073 | 27–31 | 27–31 |
| GPT-5.6 Terra (max) | 1.122 | 32 | 105/105 | 0.071 | 29–31 | 29–31 |
| GPT-5.6 Luna (max) | 1.143 | 33 | 107/107 | 0.067 | 31–33 | 31–33 |
| GPT-5.4 (xhigh) | 1.157 | 28 | 86/86 | 0.078 | 32–34 | 32–34 |
| GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 1.182 | 21 | 48/48 | 0.112 | 33–34 | 33–34 |
| Muse Spark 1.2 (xhigh) | 1.248 | 29 | 85/85 | 0.076 | 35–35 | 35–35 |
| Muse Spark 1.1 (xhigh) | 1.297 | 28 | 81/81 | 0.080 | 36–36 | 36–36 |
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
