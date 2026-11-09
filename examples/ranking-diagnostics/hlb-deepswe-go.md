# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-go-40-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.875 | 19 | 28/28 | 0.103 | 1–1 | 1–1 |
| GLM-5.3 Flash (low) · Hermes | 0.923 | 30 | 62/62 | 0.069 | 2–7 | 2–7 |
| GLM-5.3 Flash (low) · pi | 0.924 | 25 | 51/51 | 0.082 | 2–5 | 2–5 |
| DeepSeek V4.1 Flash (high) · Codex | 0.927 | 28 | 67/67 | 0.075 | 2–7 | 2–7 |
| GLM-5.3 Flash (low) · OpenCode 2 | 0.927 | 28 | 60/60 | 0.073 | 2–6 | 2–6 |
| GLM-5.3 Flash (low) · Qwen Code | 0.932 | 26 | 52/52 | 0.080 | 2–9 | 2–9 |
| GLM-5.3 Flash (high) · Qwen Code | 0.935 | 27 | 55/55 | 0.080 | 4–8 | 4–8 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.945 | 26 | 55/55 | 0.079 | 5–13 | 5–13 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.946 | 27 | 64/64 | 0.076 | 3–12 | 3–12 |
| GLM-5.3 Flash (low) · Claude Code | 0.947 | 27 | 59/59 | 0.075 | 8–11 | 8–12 |
| GLM-5.3 Flash (low) · OpenCode | 0.952 | 17 | 26/26 | 0.111 | 8–16 | 7–16 |
| GLM-5.3 Flash (low) · Kimi Code | 0.954 | 27 | 59/59 | 0.075 | 8–17 | 8–17 |
| DeepSeek V4.1 Flash (low) · Codex | 0.956 | 29 | 69/69 | 0.073 | 9–16 | 9–16 |
| GLM-5.3 Flash (high) · Kimi Code | 0.957 | 27 | 68/68 | 0.077 | 10–16 | 10–16 |
| GLM-5.3 Flash (high) · pi | 0.959 | 29 | 68/68 | 0.071 | 10–16 | 10–16 |
| GLM-5.3 Flash (high) · Codex | 0.960 | 22 | 40/40 | 0.097 | 11–16 | 11–16 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.973 | 32 | 72/72 | 0.066 | 8–19 | 8–19 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.978 | 32 | 76/76 | 0.067 | 16–21 | 16–21 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.980 | 29 | 70/70 | 0.072 | 18–22 | 18–22 |
| GLM-5.3 Flash (high) · OpenCode 2 | 0.982 | 31 | 65/65 | 0.068 | 17–22 | 17–22 |
| GLM-5.3 Flash (low) · OpenClaw | 0.985 | 21 | 30/30 | 0.096 | 17–23 | 17–23 |
| DeepSeek V4.1 Flash (low) · pi | 1.002 | 30 | 69/69 | 0.071 | 21–24 | 21–24 |
| DeepSeek V4.1 Flash (high) · OpenCode 2 | 1.006 | 31 | 75/75 | 0.067 | 22–24 | 22–24 |
| GLM-5.3 Flash (high) · Claude Code | 1.014 | 30 | 66/66 | 0.070 | 22–25 | 22–25 |
| GLM-5.3 Flash (high) · Hermes | 1.018 | 28 | 64/64 | 0.075 | 24–27 | 24–27 |
| DeepSeek V4.1 Flash (low) · OpenCode 2 | 1.024 | 29 | 76/76 | 0.073 | 18–28 | 18–29 |
| DeepSeek V4.1 Flash (high) · OpenCode | 1.027 | 26 | 56/56 | 0.081 | 22–30 | 22–30 |
| GLM-5.3 Flash (high) · OpenClaw | 1.028 | 24 | 32/32 | 0.085 | 25–32 | 25–32 |
| DeepSeek V4.1 Flash (low) · OpenCode | 1.031 | 26 | 55/55 | 0.079 | 26–33 | 27–33 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.036 | 31 | 78/78 | 0.068 | 27–32 | 27–32 |
| DeepSeek V4.1 Flash (low) · Hermes | 1.036 | 31 | 69/69 | 0.069 | 26–32 | 26–32 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.042 | 30 | 61/61 | 0.069 | 29–33 | 29–33 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.059 | 30 | 66/66 | 0.073 | 29–35 | 29–35 |
| DeepSeek V4.1 Flash (high) · pi | 1.065 | 29 | 65/65 | 0.072 | 33–36 | 33–36 |
| GLM-5.3 Flash (high) · OpenCode | 1.076 | 24 | 39/39 | 0.086 | 32–36 | 32–36 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.085 | 17 | 25/25 | 0.124 | 33–37 | 33–37 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.133 | 30 | 66/66 | 0.069 | 36–40 | 36–40 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 1.135 | 13 | 21/22 | 0.163 | 35–40 | 35–40 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.139 | 30 | 70/70 | 0.069 | 37–40 | 37–40 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.148 | 31 | 67/67 | 0.068 | 37–40 | 37–40 |

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
