# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-go-36-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.874 | 19 | 28/28 | 0.103 | 1–1 | 1–1 |
| GLM-5.3 Flash (low) · Hermes | 0.921 | 30 | 62/62 | 0.069 | 2–6 | 2–6 |
| GLM-5.3 Flash (low) · pi | 0.923 | 25 | 51/51 | 0.082 | 2–5 | 2–5 |
| DeepSeek V4.1 Flash (high) · Codex | 0.925 | 28 | 67/67 | 0.075 | 2–6 | 2–6 |
| GLM-5.3 Flash (low) · Qwen Code | 0.930 | 26 | 52/52 | 0.080 | 2–8 | 2–8 |
| GLM-5.3 Flash (high) · Qwen Code | 0.933 | 27 | 55/55 | 0.080 | 4–7 | 4–7 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.943 | 26 | 55/55 | 0.079 | 5–12 | 5–12 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.944 | 27 | 64/64 | 0.076 | 3–10 | 3–10 |
| GLM-5.3 Flash (low) · Claude Code | 0.946 | 27 | 59/59 | 0.075 | 7–10 | 7–10 |
| GLM-5.3 Flash (low) · OpenCode | 0.948 | 17 | 26/26 | 0.110 | 6–15 | 6–15 |
| DeepSeek V4.1 Flash (low) · Codex | 0.953 | 29 | 69/69 | 0.072 | 8–15 | 8–15 |
| GLM-5.3 Flash (high) · Kimi Code | 0.954 | 27 | 68/68 | 0.077 | 10–15 | 10–15 |
| GLM-5.3 Flash (low) · Kimi Code | 0.954 | 27 | 59/59 | 0.075 | 8–16 | 7–16 |
| GLM-5.3 Flash (high) · pi | 0.957 | 29 | 68/68 | 0.071 | 9–15 | 9–15 |
| GLM-5.3 Flash (high) · Codex | 0.958 | 22 | 40/40 | 0.097 | 11–15 | 11–15 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.971 | 32 | 72/72 | 0.066 | 7–18 | 7–18 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.976 | 32 | 76/76 | 0.066 | 15–19 | 15–19 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.978 | 29 | 70/70 | 0.072 | 17–19 | 17–19 |
| GLM-5.3 Flash (low) · OpenClaw | 0.985 | 21 | 30/30 | 0.096 | 16–21 | 16–21 |
| DeepSeek V4.1 Flash (low) · pi | 0.999 | 30 | 69/69 | 0.070 | 19–21 | 19–21 |
| GLM-5.3 Flash (high) · Claude Code | 1.012 | 30 | 66/66 | 0.070 | 20–22 | 20–22 |
| GLM-5.3 Flash (high) · Hermes | 1.017 | 28 | 64/64 | 0.075 | 21–23 | 21–23 |
| GLM-5.3 Flash (high) · OpenClaw | 1.025 | 24 | 32/32 | 0.085 | 21–27 | 21–27 |
| DeepSeek V4.1 Flash (high) · OpenCode | 1.026 | 26 | 56/56 | 0.081 | 20–26 | 20–26 |
| DeepSeek V4.1 Flash (low) · OpenCode | 1.029 | 26 | 55/55 | 0.079 | 23–29 | 23–29 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.033 | 31 | 78/78 | 0.068 | 23–28 | 23–28 |
| DeepSeek V4.1 Flash (low) · Hermes | 1.034 | 31 | 69/69 | 0.068 | 23–28 | 23–28 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.040 | 30 | 61/61 | 0.069 | 25–29 | 25–29 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.057 | 30 | 66/66 | 0.073 | 25–31 | 25–31 |
| DeepSeek V4.1 Flash (high) · pi | 1.063 | 29 | 65/65 | 0.072 | 29–31 | 29–31 |
| GLM-5.3 Flash (high) · OpenCode | 1.076 | 24 | 39/39 | 0.086 | 28–32 | 28–32 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.082 | 17 | 25/25 | 0.123 | 28–33 | 28–33 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 1.132 | 13 | 21/22 | 0.159 | 31–36 | 31–36 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.132 | 30 | 66/66 | 0.069 | 32–36 | 32–36 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.137 | 30 | 70/70 | 0.069 | 33–36 | 33–36 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.146 | 31 | 67/67 | 0.068 | 33–36 | 33–36 |

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
