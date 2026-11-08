# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-typescript-36-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.834 | 13 | 21/25 | 0.145 | 1–2 | 1–3 |
| GLM-5.3 Flash (high) · Codex | 0.852 | 22 | 35/36 | 0.092 | 2–3 | 2–3 |
| GLM-5.3 Flash (low) · Qwen Code | 0.858 | 25 | 45/48 | 0.076 | 1–3 | 1–3 |
| GLM-5.3 Flash (low) · Kimi Code | 0.901 | 21 | 42/45 | 0.089 | 4–4 | 4–5 |
| GLM-5.3 Flash (low) · pi | 0.916 | 23 | 49/54 | 0.082 | 5–6 | 4–6 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.925 | 24 | 57/61 | 0.076 | 5–7 | 5–6 |
| GLM-5.3 Flash (low) · Hermes | 0.938 | 19 | 41/45 | 0.094 | 6–9 | 7–10 |
| GLM-5.3 Flash (low) · Claude Code | 0.945 | 24 | 54/57 | 0.087 | 7–11 | 7–11 |
| GLM-5.3 Flash (low) · OpenCode | 0.947 | 18 | 34/37 | 0.114 | 7–11 | 7–13 |
| GLM-5.3 Flash (high) · pi | 0.949 | 22 | 52/54 | 0.086 | 8–12 | 8–11 |
| GLM-5.3 Flash (high) · Claude Code | 0.959 | 24 | 51/54 | 0.081 | 9–12 | 9–12 |
| DeepSeek V4.1 Flash (low) · Codex | 0.967 | 29 | 59/64 | 0.070 | 8–17 | 11–15 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.972 | 30 | 65/68 | 0.062 | 10–17 | 10–17 |
| GLM-5.3 Flash (high) · Qwen Code | 0.973 | 23 | 51/54 | 0.083 | 11–16 | 12–16 |
| GLM-5.3 Flash (high) · OpenCode | 0.981 | 15 | 27/32 | 0.133 | 12–20 | 12–20 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.985 | 24 | 56/60 | 0.085 | 14–19 | 14–19 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.986 | 24 | 54/60 | 0.081 | 13–21 | 15–21 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.991 | 22 | 47/53 | 0.084 | 15–20 | 15–20 |
| GLM-5.3 Flash (low) · OpenClaw | 0.992 | 17 | 27/30 | 0.105 | 13–21 | 15–21 |
| DeepSeek V4.1 Flash (low) · Hermes | 1.001 | 31 | 70/74 | 0.064 | 19–23 | 19–23 |
| DeepSeek V4.1 Flash (high) · Codex | 1.005 | 28 | 58/61 | 0.070 | 15–25 | 12–25 |
| DeepSeek V4.1 Flash (high) · OpenCode | 1.008 | 19 | 43/48 | 0.101 | 19–26 | 19–26 |
| DeepSeek V4.1 Flash (high) · pi | 1.010 | 28 | 58/61 | 0.075 | 15–27 | 13–25 |
| GLM-5.3 Flash (high) · Kimi Code | 1.012 | 26 | 61/65 | 0.075 | 14–26 | 14–26 |
| GLM-5.3 Flash (high) · Hermes | 1.016 | 25 | 53/56 | 0.080 | 20–27 | 20–27 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 1.023 | 27 | 56/60 | 0.075 | 9–29 | 9–29 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.024 | 30 | 69/74 | 0.067 | 21–27 | 21–27 |
| DeepSeek V4.1 Flash (low) · pi | 1.049 | 25 | 55/59 | 0.082 | 21–31 | 21–31 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.049 | 22 | 43/47 | 0.092 | 28–30 | 28–30 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 1.052 | 10 | 18/19 | 0.170 | 21–31 | 21–31 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.100 | 29 | 67/72 | 0.065 | 31–33 | 30–33 |
| GLM-5.3 Flash (high) · OpenClaw | 1.101 | 22 | 38/42 | 0.088 | 31–36 | 31–36 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.104 | 26 | 55/58 | 0.077 | 18–34 | 18–34 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.119 | 26 | 55/58 | 0.075 | 33–34 | 33–34 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.166 | 17 | 22/23 | 0.112 | 28–36 | 28–36 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.180 | 26 | 60/66 | 0.075 | 35–36 | 35–36 |

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
