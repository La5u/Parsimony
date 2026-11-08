# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-python-36-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.829 | 19 | 29/30 | 0.087 | 1–1 | 1–1 |
| GLM-5.3 Flash (low) · Qwen Code | 0.851 | 26 | 45/45 | 0.065 | 2–3 | 2–3 |
| GLM-5.3 Flash (high) · Codex | 0.856 | 18 | 30/32 | 0.099 | 1–3 | 1–3 |
| GLM-5.3 Flash (low) · pi | 0.881 | 29 | 54/55 | 0.059 | 4–5 | 4–5 |
| GLM-5.3 Flash (low) · Kimi Code | 0.885 | 28 | 56/57 | 0.062 | 4–5 | 4–5 |
| GLM-5.3 Flash (low) · Claude Code | 0.902 | 25 | 55/55 | 0.067 | 6–7 | 6–7 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.912 | 29 | 60/63 | 0.056 | 6–7 | 5–7 |
| GLM-5.3 Flash (high) · Qwen Code | 0.928 | 27 | 58/59 | 0.061 | 8–8 | 8–9 |
| GLM-5.3 Flash (low) · OpenCode | 0.939 | 18 | 33/35 | 0.092 | 9–12 | 9–10 |
| DeepSeek V4.1 Flash (high) · Codex | 0.944 | 28 | 60/64 | 0.062 | 8–12 | 8–12 |
| GLM-5.3 Flash (low) · Hermes | 0.951 | 27 | 50/51 | 0.066 | 9–13 | 9–15 |
| GLM-5.3 Flash (high) · Kimi Code | 0.953 | 29 | 62/63 | 0.056 | 9–14 | 9–14 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.955 | 29 | 69/72 | 0.059 | 10–14 | 10–14 |
| GLM-5.3 Flash (high) · Claude Code | 0.967 | 27 | 64/65 | 0.064 | 12–15 | 12–15 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.972 | 20 | 42/44 | 0.086 | 14–16 | 13–16 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.986 | 30 | 70/71 | 0.058 | 15–20 | 15–20 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.992 | 29 | 67/69 | 0.058 | 16–21 | 16–21 |
| DeepSeek V4.1 Flash (low) · Codex | 0.992 | 27 | 53/55 | 0.063 | 16–22 | 16–22 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.992 | 30 | 66/69 | 0.058 | 16–22 | 16–22 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.993 | 23 | 44/47 | 0.075 | 10–21 | 10–21 |
| GLM-5.3 Flash (high) · pi | 0.993 | 28 | 63/63 | 0.060 | 16–21 | 16–21 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 1.013 | 27 | 60/62 | 0.062 | 17–24 | 17–24 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.015 | 28 | 59/61 | 0.060 | 22–25 | 22–25 |
| GLM-5.3 Flash (low) · OpenClaw | 1.023 | 16 | 30/33 | 0.106 | 20–26 | 20–26 |
| GLM-5.3 Flash (high) · Hermes | 1.024 | 28 | 59/59 | 0.061 | 22–25 | 22–25 |
| GLM-5.3 Flash (high) · OpenCode | 1.048 | 21 | 35/35 | 0.077 | 24–27 | 24–27 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.055 | 27 | 62/62 | 0.061 | 26–28 | 26–28 |
| DeepSeek V4.1 Flash (high) · pi | 1.075 | 30 | 61/63 | 0.057 | 27–28 | 26–28 |
| DeepSeek V4.1 Flash (low) · pi | 1.090 | 29 | 62/64 | 0.061 | 28–30 | 28–30 |
| GLM-5.3 Flash (high) · OpenClaw | 1.108 | 20 | 39/39 | 0.088 | 29–31 | 29–32 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.119 | 31 | 74/77 | 0.056 | 30–32 | 30–32 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.148 | 28 | 59/61 | 0.062 | 30–33 | 30–33 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.160 | 26 | 67/70 | 0.066 | 30–34 | 30–34 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.184 | 28 | 62/65 | 0.061 | 34–35 | 34–35 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.217 | 13 | 23/23 | 0.127 | 33–36 | 33–36 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 1.258 | 9 | 10/13 | 0.180 | 35–36 | 35–36 |

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
