# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-typescript-40-pooled-80-20-v0.11` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.837 | 13 | 21/25 | 0.146 | 1–1 | 1–2 |
| GLM-5.3 Flash (high) · Codex | 0.855 | 22 | 35/36 | 0.092 | 1–3 | 1–3 |
| GLM-5.3 Flash (low) · Qwen Code | 0.867 | 25 | 45/48 | 0.077 | 2–3 | 2–3 |
| GLM-5.3 Flash (low) · Kimi Code | 0.906 | 21 | 42/45 | 0.089 | 4–4 | 4–5 |
| GLM-5.3 Flash (low) · pi | 0.919 | 23 | 49/54 | 0.083 | 5–7 | 4–7 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.928 | 24 | 57/61 | 0.076 | 5–7 | 5–7 |
| GLM-5.3 Flash (low) · OpenCode 2 | 0.935 | 28 | 54/57 | 0.067 | 5–8 | 6–8 |
| GLM-5.3 Flash (low) · Hermes | 0.948 | 19 | 41/45 | 0.095 | 7–11 | 8–13 |
| GLM-5.3 Flash (low) · Claude Code | 0.949 | 24 | 54/57 | 0.088 | 7–12 | 7–11 |
| GLM-5.3 Flash (high) · pi | 0.952 | 22 | 52/54 | 0.087 | 8–12 | 9–12 |
| GLM-5.3 Flash (low) · OpenCode | 0.952 | 18 | 34/37 | 0.116 | 7–12 | 7–15 |
| DeepSeek V4.1 Flash (low) · OpenCode 2 | 0.967 | 24 | 61/65 | 0.076 | 9–16 | 9–16 |
| GLM-5.3 Flash (high) · Claude Code | 0.969 | 24 | 51/54 | 0.082 | 12–15 | 11–15 |
| DeepSeek V4.1 Flash (low) · Codex | 0.976 | 29 | 59/64 | 0.071 | 10–21 | 12–19 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.981 | 30 | 65/68 | 0.063 | 12–20 | 12–21 |
| GLM-5.3 Flash (high) · Qwen Code | 0.982 | 23 | 51/54 | 0.084 | 12–21 | 14–21 |
| DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.983 | 27 | 63/66 | 0.074 | 14–20 | 14–22 |
| GLM-5.3 Flash (high) · OpenCode | 0.986 | 15 | 27/32 | 0.134 | 12–23 | 12–24 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.987 | 24 | 56/60 | 0.086 | 14–22 | 14–22 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.995 | 24 | 54/60 | 0.083 | 16–24 | 18–24 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.995 | 22 | 47/53 | 0.084 | 17–23 | 15–23 |
| GLM-5.3 Flash (low) · OpenClaw | 0.995 | 17 | 27/30 | 0.105 | 13–23 | 13–22 |
| DeepSeek V4.1 Flash (low) · Hermes | 1.008 | 31 | 70/74 | 0.064 | 23–28 | 23–28 |
| DeepSeek V4.1 Flash (high) · pi | 1.013 | 28 | 58/61 | 0.076 | 14–31 | 14–30 |
| DeepSeek V4.1 Flash (high) · Codex | 1.014 | 28 | 58/61 | 0.071 | 19–30 | 14–30 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.015 | 26 | 55/58 | 0.077 | 20–30 | 20–29 |
| DeepSeek V4.1 Flash (high) · OpenCode | 1.018 | 19 | 43/48 | 0.103 | 23–32 | 23–32 |
| GLM-5.3 Flash (high) · Hermes | 1.019 | 25 | 53/56 | 0.080 | 23–31 | 23–31 |
| GLM-5.3 Flash (high) · Kimi Code | 1.020 | 26 | 61/65 | 0.076 | 17–31 | 17–31 |
| GLM-5.3 Flash (high) · OpenCode 2 | 1.020 | 26 | 52/57 | 0.080 | 23–33 | 20–33 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.032 | 30 | 69/74 | 0.068 | 25–33 | 25–33 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 1.033 | 27 | 56/60 | 0.076 | 11–34 | 11–34 |
| DeepSeek V4.1 Flash (low) · pi | 1.051 | 25 | 55/59 | 0.082 | 23–36 | 23–36 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.053 | 22 | 43/47 | 0.094 | 33–35 | 32–35 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 1.057 | 10 | 18/19 | 0.171 | 23–35 | 23–35 |
| GLM-5.3 Flash (high) · OpenClaw | 1.102 | 22 | 38/42 | 0.088 | 36–39 | 36–39 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.108 | 29 | 67/72 | 0.066 | 36–38 | 36–38 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.122 | 26 | 55/58 | 0.076 | 37–38 | 37–38 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.169 | 17 | 22/23 | 0.113 | 32–40 | 32–40 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.189 | 26 | 60/66 | 0.076 | 39–40 | 39–40 |

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
