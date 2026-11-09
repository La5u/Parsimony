# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-python-40-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.832 | 19 | 29/30 | 0.086 | 1–1 | 1–1 |
| GLM-5.3 Flash (low) · Qwen Code | 0.855 | 26 | 45/45 | 0.065 | 2–3 | 2–3 |
| GLM-5.3 Flash (high) · Codex | 0.863 | 18 | 30/32 | 0.098 | 2–3 | 2–3 |
| GLM-5.3 Flash (low) · pi | 0.884 | 29 | 54/55 | 0.059 | 4–5 | 4–5 |
| GLM-5.3 Flash (low) · Kimi Code | 0.889 | 28 | 56/57 | 0.062 | 4–5 | 4–6 |
| GLM-5.3 Flash (low) · Claude Code | 0.906 | 25 | 55/55 | 0.067 | 6–7 | 6–7 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.915 | 29 | 60/63 | 0.057 | 6–7 | 5–7 |
| GLM-5.3 Flash (low) · OpenCode 2 | 0.929 | 25 | 51/53 | 0.068 | 8–10 | 8–10 |
| GLM-5.3 Flash (high) · Qwen Code | 0.931 | 27 | 58/59 | 0.061 | 8–9 | 8–10 |
| GLM-5.3 Flash (low) · OpenCode | 0.944 | 18 | 33/35 | 0.091 | 9–14 | 9–12 |
| DeepSeek V4.1 Flash (high) · Codex | 0.947 | 28 | 60/64 | 0.062 | 9–13 | 9–13 |
| GLM-5.3 Flash (low) · Hermes | 0.955 | 27 | 50/51 | 0.066 | 10–15 | 10–17 |
| GLM-5.3 Flash (high) · Kimi Code | 0.957 | 29 | 62/63 | 0.056 | 10–16 | 10–16 |
| DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.958 | 27 | 53/55 | 0.064 | 12–16 | 11–16 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.958 | 29 | 69/72 | 0.059 | 10–15 | 10–15 |
| GLM-5.3 Flash (high) · Claude Code | 0.971 | 27 | 64/65 | 0.064 | 15–17 | 15–17 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.977 | 20 | 42/44 | 0.085 | 16–19 | 15–19 |
| GLM-5.3 Flash (high) · OpenCode 2 | 0.979 | 28 | 61/62 | 0.061 | 16–21 | 17–19 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.990 | 30 | 70/71 | 0.057 | 17–23 | 18–23 |
| DeepSeek V4.1 Flash (low) · Codex | 0.995 | 27 | 53/55 | 0.063 | 19–26 | 19–26 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.995 | 30 | 66/69 | 0.057 | 17–26 | 17–26 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.996 | 29 | 67/69 | 0.058 | 18–25 | 18–25 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.997 | 23 | 44/47 | 0.075 | 11–25 | 11–25 |
| GLM-5.3 Flash (high) · pi | 0.997 | 28 | 63/63 | 0.059 | 19–25 | 19–25 |
| DeepSeek V4.1 Flash (low) · OpenCode 2 | 1.000 | 27 | 60/62 | 0.063 | 19–25 | 19–25 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 1.016 | 27 | 60/62 | 0.061 | 20–28 | 20–28 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.018 | 28 | 59/61 | 0.059 | 25–29 | 25–29 |
| GLM-5.3 Flash (high) · Hermes | 1.028 | 28 | 59/59 | 0.062 | 26–29 | 26–29 |
| GLM-5.3 Flash (low) · OpenClaw | 1.029 | 16 | 30/33 | 0.105 | 24–31 | 24–31 |
| GLM-5.3 Flash (high) · OpenCode | 1.053 | 21 | 35/35 | 0.077 | 28–31 | 28–32 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.059 | 27 | 62/62 | 0.061 | 30–32 | 29–32 |
| DeepSeek V4.1 Flash (high) · pi | 1.078 | 30 | 61/63 | 0.056 | 30–32 | 30–32 |
| DeepSeek V4.1 Flash (low) · pi | 1.095 | 29 | 62/64 | 0.061 | 32–34 | 32–34 |
| GLM-5.3 Flash (high) · OpenClaw | 1.112 | 20 | 39/39 | 0.087 | 33–35 | 33–36 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.121 | 31 | 74/77 | 0.055 | 34–36 | 34–36 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.153 | 28 | 59/61 | 0.062 | 35–37 | 35–37 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.164 | 26 | 67/70 | 0.065 | 34–38 | 34–38 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.188 | 28 | 62/65 | 0.061 | 38–39 | 38–39 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.219 | 13 | 23/23 | 0.126 | 37–40 | 37–40 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 1.261 | 9 | 10/13 | 0.179 | 39–40 | 39–40 |

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
