# Same-task net ratio diagnostics

Panel: `mini-swe-agent-33-448-solved-80-20-v0.5` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Qwen2.5-Coder 32B | 0.415 | 42 | 43/45 | 0.303 | 1–3 | 1–8 |
| Gemini 2.5 Pro | 0.539 | 264 | 264/268 | 0.034 | 1–2 | 1–2 |
| Claude Opus 4.5 (high) | 0.672 | 378 | 384/384 | 0.053 | 2–3 | 3–4 |
| Gemini 3 Flash (high) | 0.742 | 375 | 379/379 | 0.068 | 4–8 | 3–8 |
| Gemini 3 Pro (preview) | 0.747 | 368 | 370/371 | 0.044 | 4–7 | 4–8 |
| Claude Opus 4.6 | 0.750 | 373 | 378/378 | 0.049 | 4–7 | 4–7 |
| Claude Sonnet 4 | 0.772 | 324 | 324/324 | 0.066 | 4–23 | 2–22 |
| MiniMax M2.5 (high) | 0.829 | 373 | 379/379 | 0.069 | 7–11 | 6–11 |
| Kimi K2.5 (high) | 0.850 | 354 | 354/354 | 0.055 | 8–10 | 8–14 |
| Claude Haiku 4.5 (high) | 0.867 | 333 | 333/333 | 0.085 | 8–14 | 9–14 |
| Devstral 2512 | 0.869 | 268 | 269/269 | 0.109 | 9–19 | 8–19 |
| GLM-5.1 · EvalScope | 0.882 | 358 | 363/363 | 0.055 | 9–13 | 10–14 |
| o4-mini | 0.923 | 222 | 223/225 | 0.045 | 12–15 | 12–18 |
| o3 | 0.932 | 292 | 292/292 | 0.080 | 13–18 | 13–18 |
| Llama 4 Maverick | 0.945 | 104 | 104/105 | 0.160 | 4–20 | 5–26 |
| Kimi K2 Instruct | 0.950 | 216 | 216/219 | 0.037 | 13–18 | 13–20 |
| Claude Sonnet 4.5 (high) | 0.955 | 357 | 357/357 | 0.058 | 14–18 | 15–20 |
| GLM-5 (high) | 0.966 | 360 | 364/364 | 0.021 | 15–19 | 13–20 |
| GPT-5 mini | 0.983 | 281 | 281/281 | 0.105 | 17–24 | 13–24 |
| GPT-5.1 | 1.007 | 327 | 329/330 | 0.026 | 19–21 | 16–21 |
| GPT-5.1 Codex | 1.032 | 330 | 330/330 | 0.039 | 20–22 | 19–23 |
| Qwen3-Coder 480B | 1.048 | 271 | 273/277 | 0.036 | 20–23 | 18–25 |
| GLM-4.6 | 1.060 | 273 | 273/277 | 0.033 | 21–24 | 17–24 |
| Claude Opus 4 | 1.102 | 336 | 337/338 | 0.063 | 24–26 | 23–26 |
| GPT-5 | 1.115 | 318 | 319/325 | 0.028 | 24–27 | 23–26 |
| GPT-5 nano | 1.123 | 173 | 173/174 | 0.065 | 24–28 | 23–29 |
| gpt-oss-120b | 1.163 | 122 | 123/130 | 0.111 | 23–32 | 17–33 |
| Gemini 3.5 Flash | 1.165 | 347 | 359/359 | 0.056 | 27–29 | 24–29 |
| GPT-5.2 | 1.220 | 343 | 345/345 | 0.081 | 29–32 | 23–32 |
| DeepSeek V3.2 (high) | 1.222 | 348 | 350/350 | 0.057 | 28–31 | 28–31 |
| GLM-4.5 | 1.249 | 267 | 267/271 | 0.037 | 14–32 | 16–32 |
| Devstral Small 2512 | 1.305 | 279 | 280/282 | 0.042 | 4–34 | 4–35 |
| Kimi K2 Thinking | 1.380 | 313 | 314/317 | 0.072 | 29–34 | 29–34 |
| MiniMax M2 | 1.430 | 299 | 302/305 | 0.076 | 31–34 | 30–34 |
| GPT-5.2 (high) | 1.671 | 362 | 364/364 | 0.036 | 35–35 | 34–35 |

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
