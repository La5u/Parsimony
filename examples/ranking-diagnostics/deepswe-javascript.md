# Same-task net ratio diagnostics

Panel: `deepswe-v1.1-javascript-26-pooled-80-20-v0.7` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.1 Pro Preview (high) | 0.563 | 2 | 2/2 | 0.570 | 1–2 | 1–2 |
| Kimi K2.6 · DeepSWE 1.0 | 0.628 | 1 | 3/3 | 1.000 | 2–3 | 2–3 |
| Grok Build 0.1 · DeepSWE 1.0 | 0.736 | 2 | 4/4 | 0.573 | 2–30 | 2–30 |
| Gemini 3.5 Flash (high) | 0.799 | 4 | 10/10 | 0.457 | 3–6 | 3–7 |
| Claude Fable 5 (xhigh) | 0.811 | 4 | 14/14 | 0.316 | 1–9 | 1–11 |
| GLM-5.1 · DeepSWE 1.0 | 0.819 | 2 | 3/3 | 0.568 | 4–8 | 4–8 |
| Claude Opus 4.8 (max) | 0.847 | 3 | 8/8 | 0.398 | 3–9 | 3–9 |
| MiMo V2.5 Pro · DeepSWE 1.0 | 0.854 | 1 | 1/1 | 1.000 | 6–11 | 6–10 |
| Kimi K2.7 Code | 0.866 | 2 | 5/5 | 0.567 | 7–11 | 7–11 |
| Gemini 3.6 Flash (high) | 0.870 | 4 | 11/11 | 0.317 | 6–13 | 6–13 |
| GPT-5.5 (xhigh) | 0.893 | 4 | 10/10 | 0.463 | 5–23 | 6–23 |
| GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 0.915 | 2 | 5/5 | 0.569 | 6–26 | 5–26 |
| Kimi K3 (max) | 0.918 | 5 | 13/13 | 0.401 | 5–17 | 5–18 |
| Qwen3.8 Max (xhigh) | 0.936 | 4 | 13/13 | 0.497 | 7–21 | 7–21 |
| GPT-5.6 Terra (max) | 0.941 | 4 | 14/14 | 0.497 | 10–19 | 10–19 |
| Claude Sonnet 5 (max) | 0.950 | 5 | 11/11 | 0.397 | 5–21 | 5–22 |
| GLM-5.2 (max) | 0.957 | 2 | 6/6 | 0.567 | 14–22 | 14–22 |
| Claude Opus 4.7 (max) · DeepSWE 1.0 | 0.959 | 3 | 10/10 | 0.398 | 13–20 | 13–20 |
| GLM-5.3 (max) | 0.965 | 5 | 18/18 | 0.403 | 16–21 | 15–21 |
| DeepSeek V4 Flash (max) | 0.991 | 3 | 7/7 | 0.397 | 13–24 | 13–24 |
| Gemini 3.7 Flash (medium) | 1.026 | 5 | 11/11 | 0.400 | 16–26 | 16–26 |
| GPT-5.6 Luna (max) | 1.031 | 5 | 12/12 | 0.407 | 12–30 | 12–30 |
| GPT-5.4 (xhigh) | 1.035 | 4 | 7/7 | 0.503 | 13–32 | 13–32 |
| GPT-5.6 Sol (max) | 1.035 | 4 | 15/15 | 0.498 | 14–28 | 14–28 |
| Claude Opus 4.6 (max) · DeepSWE 1.0 | 1.038 | 3 | 4/4 | 0.398 | 22–25 | 22–25 |
| Grok 4.5 (high) | 1.063 | 3 | 8/8 | 0.580 | 14–28 | 14–28 |
| DeepSeek V4 Pro (max) | 1.076 | 4 | 13/13 | 0.495 | 20–28 | 20–28 |
| GLM-5.3 Flash (max) | 1.076 | 4 | 12/12 | 0.314 | 17–29 | 17–30 |
| Claude Sonnet 4.6 (high) | 1.086 | 3 | 8/8 | 0.578 | 8–29 | 8–29 |
| MiniMax M3 · DeepSWE 1.0 | 1.132 | 2 | 5/6 | 0.566 | 27–30 | 27–30 |
| Grok 4.6 (medium) | 1.132 | 5 | 16/16 | 0.399 | 21–33 | 21–33 |
| Claude Opus 5 (max) | 1.192 | 4 | 13/13 | 0.312 | 23–34 | 23–34 |
| Muse Spark 1.2 (xhigh) | 1.309 | 5 | 11/11 | 0.412 | 31–34 | 31–34 |
| Muse Spark 1.1 (xhigh) | 1.313 | 5 | 9/9 | 0.412 | 31–34 | 31–33 |
| Claude Haiku 4.5 · DeepSWE 1.0 | — | 0 | 0/0 | — | — | — |
| Gemini 3 Flash Preview · DeepSWE 1.0 | — | 0 | 0/0 | — | — | — |
| MiniMax M2.7 · DeepSWE 1.0 | — | 0 | 0/0 | — | — | — |
| Qwen3.6 Plus · DeepSWE 1.0 | — | 0 | 0/0 | — | — | — |

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
