# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-typescript-40-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.837 | 13 | 21/25 | 0.146 | 1–2 | 1–3 |
| GLM-5.3 Flash (high) · Codex | 0.855 | 22 | 35/36 | 0.092 | 2–3 | 1–3 |
| GLM-5.3 Flash (low) · Qwen Code | 0.862 | 25 | 45/48 | 0.077 | 1–3 | 1–3 |
| GLM-5.3 Flash (low) · Kimi Code | 0.906 | 21 | 42/45 | 0.089 | 4–4 | 4–6 |
| GLM-5.3 Flash (low) · pi | 0.919 | 23 | 49/54 | 0.083 | 5–7 | 5–7 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.928 | 24 | 57/61 | 0.076 | 5–7 | 5–7 |
| GLM-5.3 Flash (low) · OpenCode 2 | 0.930 | 28 | 54/57 | 0.067 | 5–8 | 4–8 |
| GLM-5.3 Flash (low) · Hermes | 0.941 | 19 | 41/45 | 0.094 | 6–10 | 8–11 |
| GLM-5.3 Flash (low) · Claude Code | 0.949 | 24 | 54/57 | 0.088 | 8–12 | 8–12 |
| GLM-5.3 Flash (high) · pi | 0.952 | 22 | 52/54 | 0.087 | 9–12 | 9–12 |
| GLM-5.3 Flash (low) · OpenCode | 0.952 | 18 | 34/37 | 0.116 | 7–12 | 7–15 |
| GLM-5.3 Flash (high) · Claude Code | 0.964 | 24 | 51/54 | 0.082 | 11–14 | 10–14 |
| DeepSeek V4.1 Flash (low) · OpenCode 2 | 0.967 | 24 | 61/65 | 0.076 | 9–17 | 9–17 |
| DeepSeek V4.1 Flash (low) · Codex | 0.971 | 29 | 59/64 | 0.071 | 9–20 | 12–17 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.976 | 30 | 65/68 | 0.063 | 11–20 | 11–20 |
| GLM-5.3 Flash (high) · Qwen Code | 0.976 | 23 | 51/54 | 0.084 | 11–19 | 14–19 |
| DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.983 | 27 | 63/66 | 0.074 | 16–21 | 16–22 |
| GLM-5.3 Flash (high) · OpenCode | 0.986 | 15 | 27/32 | 0.134 | 13–23 | 13–24 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.987 | 24 | 56/60 | 0.086 | 16–22 | 16–22 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.990 | 24 | 54/60 | 0.082 | 15–24 | 17–24 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.995 | 22 | 47/53 | 0.084 | 17–23 | 17–23 |
| GLM-5.3 Flash (low) · OpenClaw | 0.995 | 17 | 27/30 | 0.105 | 15–23 | 16–23 |
| DeepSeek V4.1 Flash (low) · Hermes | 1.004 | 31 | 70/74 | 0.064 | 22–26 | 22–27 |
| DeepSeek V4.1 Flash (high) · Codex | 1.009 | 28 | 58/61 | 0.070 | 18–29 | 14–29 |
| DeepSeek V4.1 Flash (high) · OpenCode | 1.013 | 19 | 43/48 | 0.103 | 22–29 | 22–29 |
| DeepSeek V4.1 Flash (high) · pi | 1.013 | 28 | 58/61 | 0.076 | 17–31 | 15–29 |
| GLM-5.3 Flash (high) · Kimi Code | 1.015 | 26 | 61/65 | 0.076 | 17–29 | 17–30 |
| GLM-5.3 Flash (high) · OpenCode 2 | 1.015 | 26 | 52/57 | 0.080 | 23–29 | 19–30 |
| GLM-5.3 Flash (high) · Hermes | 1.019 | 25 | 53/56 | 0.080 | 23–31 | 23–31 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.027 | 30 | 69/74 | 0.068 | 24–31 | 24–31 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 1.028 | 27 | 56/60 | 0.076 | 11–33 | 11–33 |
| DeepSeek V4.1 Flash (low) · pi | 1.051 | 25 | 55/59 | 0.082 | 24–35 | 24–35 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.053 | 22 | 43/47 | 0.094 | 32–34 | 32–34 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 1.057 | 10 | 18/19 | 0.171 | 24–35 | 24–35 |
| GLM-5.3 Flash (high) · OpenClaw | 1.102 | 22 | 38/42 | 0.088 | 35–39 | 35–39 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.103 | 29 | 67/72 | 0.066 | 35–37 | 34–37 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.105 | 26 | 55/58 | 0.077 | 20–38 | 20–38 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.122 | 26 | 55/58 | 0.076 | 37–38 | 37–38 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.169 | 17 | 22/23 | 0.113 | 32–40 | 32–40 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.183 | 26 | 60/66 | 0.076 | 39–40 | 39–40 |

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
