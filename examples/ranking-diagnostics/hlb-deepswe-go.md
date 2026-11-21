# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-go-65-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.872 | 19 | 28/28 | 0.103 | 1–2 | 1–2 |
| GLM-5.3 Flash (low) · oh-my-pi | 0.895 | 25 | 45/45 | 0.078 | 1–2 | 1–2 |
| GLM-5.3 Flash (low) · pi | 0.912 | 25 | 51/51 | 0.082 | 3–5 | 3–5 |
| GLM-5.3 Flash (high) · oh-my-pi | 0.913 | 29 | 63/63 | 0.071 | 3–8 | 3–8 |
| GLM-5.3 Flash (low) · OpenCode | 0.916 | 28 | 60/60 | 0.073 | 3–8 | 3–8 |
| GLM-5.3 Flash (low) · Kimi Code | 0.919 | 27 | 56/56 | 0.078 | 3–9 | 3–9 |
| GLM-5.3 Flash (low) · Grok Build | 0.920 | 28 | 59/59 | 0.072 | 4–14 | 4–13 |
| GLM-5.3 Flash (low) · Hermes | 0.920 | 29 | 58/58 | 0.072 | 4–16 | 4–12 |
| DeepSeek V4.1 Flash (high) · Codex | 0.922 | 29 | 68/68 | 0.072 | 4–13 | 4–13 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.927 | 27 | 60/60 | 0.075 | 8–18 | 8–18 |
| GLM-5.3 Flash (high) · Qwen Code | 0.927 | 27 | 55/55 | 0.080 | 6–17 | 6–17 |
| GLM-5.3 Flash (low) · OpenClaw | 0.927 | 29 | 57/57 | 0.071 | 6–15 | 5–15 |
| GLM-5.3 Flash (low) · Qwen Code | 0.928 | 26 | 52/52 | 0.080 | 5–18 | 5–18 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.930 | 29 | 66/66 | 0.072 | 8–17 | 7–17 |
| DeepSeek V4.1 Flash (low) · oh-my-pi | 0.931 | 29 | 65/65 | 0.072 | 6–18 | 6–18 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 0.934 | 29 | 62/62 | 0.072 | 12–19 | 10–19 |
| GLM-5.3 Flash (low) · fx | 0.936 | 28 | 57/57 | 0.072 | 10–20 | 10–21 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.938 | 32 | 72/72 | 0.066 | 14–23 | 13–24 |
| GLM-5.3 Flash (low) · Claude Code | 0.938 | 27 | 59/59 | 0.075 | 13–20 | 13–20 |
| DeepSeek V4.1 Flash (low) · Codex | 0.944 | 29 | 69/69 | 0.072 | 19–23 | 19–23 |
| GLM-5.3 Flash (high) · Codex | 0.944 | 22 | 40/40 | 0.096 | 18–25 | 18–25 |
| DeepSeek V4.1 Flash (low) · Grok Build | 0.948 | 31 | 72/72 | 0.068 | 20–24 | 20–24 |
| GLM-5.3 Flash (high) · pi | 0.948 | 29 | 68/68 | 0.071 | 19–25 | 19–25 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.954 | 28 | 67/67 | 0.077 | 21–26 | 21–26 |
| DeepSeek V4.1 Flash (low) · pi | 0.955 | 30 | 66/66 | 0.070 | 22–27 | 22–27 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.957 | 30 | 61/61 | 0.069 | 21–27 | 21–27 |
| DeepSeek V4.1 Flash (high) · pi | 0.964 | 27 | 63/63 | 0.076 | 26–30 | 26–30 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.966 | 29 | 70/70 | 0.072 | 27–35 | 27–35 |
| GLM-5.3 Flash (high) · OpenCode | 0.971 | 31 | 65/65 | 0.067 | 26–33 | 26–33 |
| DeepSeek V4.1 Flash (high) · Hermes | 0.973 | 30 | 71/71 | 0.069 | 28–34 | 28–34 |
| DeepSeek V4.1 Flash (low) · fx | 0.973 | 29 | 65/65 | 0.071 | 26–34 | 26–36 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 0.975 | 31 | 62/62 | 0.068 | 29–34 | 28–34 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 0.979 | 32 | 75/75 | 0.066 | 30–36 | 30–36 |
| GLM-5.3 Flash (high) · Grok Build | 0.979 | 27 | 60/60 | 0.080 | 29–35 | 29–35 |
| DeepSeek V4.1 Flash (high) · fx | 0.982 | 29 | 66/66 | 0.072 | 31–40 | 31–40 |
| DeepSeek V4.1 Flash (high) · oh-my-pi | 0.988 | 29 | 69/69 | 0.072 | 31–38 | 31–38 |
| GLM-5.3 Flash (high) · Kimi Code | 0.993 | 30 | 69/69 | 0.070 | 31–41 | 33–40 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.994 | 31 | 75/75 | 0.067 | 36–41 | 36–41 |
| GLM-5.3 Flash (low) · DeepSeek Harness | 0.997 | 28 | 65/65 | 0.072 | 37–42 | 37–42 |
| GLM-5.3 Flash (high) · Claude Code | 1.001 | 30 | 66/66 | 0.070 | 36–43 | 36–43 |
| DeepSeek V4.1 Flash (high) · Grok Build | 1.003 | 29 | 74/74 | 0.072 | 29–43 | 29–43 |
| GLM-5.3 Flash (high) · OpenClaw | 1.003 | 26 | 58/58 | 0.082 | 37–45 | 36–45 |
| GLM-5.3 Flash (high) · fx | 1.009 | 31 | 66/66 | 0.067 | 41–44 | 41–44 |
| DeepSeek V4.1 Flash (low) · OpenCode | 1.011 | 29 | 76/76 | 0.072 | 29–45 | 29–45 |
| DeepSeek V4.1 Flash (high) · DeepSeek Harness | 1.024 | 30 | 73/73 | 0.072 | 45–47 | 45–47 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.025 | 30 | 61/61 | 0.069 | 45–48 | 45–48 |
| Ripple-65B Preview · Qwen Code | 1.030 | 25 | 38/38 | 0.086 | 41–49 | 41–49 |
| GLM-5.3 Flash (high) · Hermes | 1.048 | 29 | 66/66 | 0.070 | 46–49 | 46–49 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.062 | 29 | 70/70 | 0.072 | 48–52 | 48–52 |
| DeepSeek V4.1 Flash (low) · DeepSeek Harness | 1.062 | 31 | 82/82 | 0.067 | 43–52 | 43–52 |
| Ripple-65B Preview · fx | 1.063 | 24 | 42/42 | 0.092 | 48–52 | 48–52 |
| GLM-5.3 Flash (high) · DeepSeek Harness | 1.072 | 28 | 61/61 | 0.074 | 49–53 | 49–53 |
| Ripple-65B Preview · Grok Build | 1.087 | 27 | 51/51 | 0.077 | 52–55 | 52–55 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.089 | 28 | 62/62 | 0.076 | 52–56 | 52–56 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.105 | 30 | 65/65 | 0.068 | 55–59 | 55–59 |
| Ripple-65B Preview · Hermes | 1.109 | 29 | 49/49 | 0.071 | 54–59 | 54–59 |
| Ripple-65B Preview · Kimi Code | 1.111 | 25 | 47/47 | 0.084 | 54–59 | 54–59 |
| Ripple-65B Preview · pi | 1.111 | 26 | 44/44 | 0.083 | 54–59 | 54–59 |
| Ripple-65B Preview · OpenCode | 1.119 | 26 | 52/52 | 0.078 | 55–60 | 56–60 |
| Ripple-65B Preview · oh-my-pi | 1.141 | 28 | 45/45 | 0.076 | 59–61 | 59–61 |
| Ripple-65B Preview · DeepSeek Harness | 1.150 | 24 | 45/45 | 0.084 | 60–62 | 60–62 |
| Ripple-65B Preview · OpenClaw | 1.164 | 19 | 32/32 | 0.129 | 60–62 | 60–62 |
| Ripple-65B Preview · Claude Code | 1.215 | 25 | 46/46 | 0.079 | 63–63 | 63–63 |
| Ripple-65B Preview · Codex | 1.234 | 27 | 54/54 | 0.083 | 63–64 | 63–64 |
| Ripple-65B Preview · mini-SWE-agent | 1.307 | 20 | 40/40 | 0.112 | 65–65 | 65–65 |

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
