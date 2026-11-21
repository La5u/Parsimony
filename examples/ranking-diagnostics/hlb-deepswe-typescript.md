# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-typescript-65-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.816 | 13 | 21/25 | 0.147 | 1–1 | 1–1 |
| GLM-5.3 Flash (high) · Codex | 0.861 | 22 | 35/36 | 0.091 | 2–2 | 2–2 |
| GLM-5.3 Flash (low) · Qwen Code | 0.877 | 25 | 45/48 | 0.077 | 2–4 | 2–4 |
| GLM-5.3 Flash (low) · Grok Build | 0.892 | 25 | 58/61 | 0.079 | 3–4 | 3–5 |
| DeepSeek V4.1 Flash (low) · fx | 0.907 | 26 | 53/57 | 0.078 | 5–12 | 5–8 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.910 | 29 | 57/61 | 0.070 | 4–11 | 5–9 |
| GLM-5.3 Flash (low) · fx | 0.915 | 26 | 53/57 | 0.075 | 5–12 | 5–12 |
| GLM-5.3 Flash (low) · pi | 0.916 | 24 | 50/55 | 0.078 | 6–12 | 5–12 |
| GLM-5.3 Flash (low) · oh-my-pi | 0.917 | 26 | 48/51 | 0.078 | 5–11 | 4–11 |
| DeepSeek V4.1 Flash (low) · oh-my-pi | 0.918 | 23 | 49/54 | 0.080 | 5–11 | 5–11 |
| GLM-5.3 Flash (low) · Hermes | 0.919 | 23 | 49/53 | 0.086 | 6–12 | 7–14 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.928 | 23 | 51/53 | 0.081 | 9–15 | 9–15 |
| GLM-5.3 Flash (low) · OpenCode | 0.935 | 28 | 54/57 | 0.069 | 12–17 | 12–17 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.937 | 26 | 56/60 | 0.082 | 6–19 | 12–16 |
| GLM-5.3 Flash (low) · Kimi Code | 0.937 | 23 | 46/47 | 0.092 | 7–18 | 7–23 |
| DeepSeek V4.1 Flash (high) · oh-my-pi | 0.941 | 23 | 47/49 | 0.088 | 13–20 | 13–18 |
| GLM-5.3 Flash (low) · Claude Code | 0.944 | 24 | 54/57 | 0.086 | 13–21 | 13–22 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.952 | 24 | 61/65 | 0.078 | 16–21 | 16–21 |
| GLM-5.3 Flash (high) · pi | 0.953 | 22 | 52/54 | 0.085 | 13–24 | 18–21 |
| GLM-5.3 Flash (low) · OpenClaw | 0.955 | 24 | 50/52 | 0.081 | 16–25 | 18–22 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.959 | 24 | 56/60 | 0.084 | 16–25 | 16–24 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.962 | 20 | 45/48 | 0.099 | 9–26 | 8–27 |
| GLM-5.3 Flash (high) · Grok Build | 0.965 | 24 | 59/63 | 0.078 | 20–28 | 20–41 |
| DeepSeek V4.1 Flash (high) · Grok Build | 0.966 | 26 | 60/65 | 0.079 | 20–27 | 22–27 |
| GLM-5.3 Flash (high) · Claude Code | 0.966 | 24 | 51/54 | 0.082 | 19–28 | 19–28 |
| DeepSeek V4.1 Flash (low) · Codex | 0.970 | 29 | 59/64 | 0.070 | 19–36 | 23–30 |
| GLM-5.3 Flash (high) · oh-my-pi | 0.971 | 23 | 49/54 | 0.079 | 21–31 | 21–31 |
| DeepSeek V4.1 Flash (low) · pi | 0.973 | 22 | 51/55 | 0.090 | 21–32 | 21–34 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 0.976 | 26 | 52/54 | 0.078 | 24–36 | 25–37 |
| GLM-5.3 Flash (low) · DeepSeek Harness | 0.979 | 23 | 52/56 | 0.085 | 26–35 | 26–35 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 0.980 | 29 | 59/61 | 0.069 | 28–35 | 27–35 |
| GLM-5.3 Flash (high) · Qwen Code | 0.981 | 23 | 51/54 | 0.084 | 28–36 | 27–36 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.982 | 27 | 63/66 | 0.073 | 26–38 | 26–39 |
| DeepSeek V4.1 Flash (low) · Grok Build | 0.982 | 26 | 56/59 | 0.075 | 27–39 | 27–39 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.991 | 23 | 52/58 | 0.087 | 28–39 | 28–40 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 0.991 | 27 | 52/55 | 0.077 | 25–46 | 30–42 |
| GLM-5.3 Flash (high) · Kimi Code | 0.992 | 24 | 53/56 | 0.077 | 27–42 | 27–43 |
| DeepSeek V4.1 Flash (low) · DeepSeek Harness | 0.993 | 27 | 60/64 | 0.076 | 31–45 | 35–45 |
| Ripple-65B Preview · oh-my-pi | 0.994 | 16 | 26/27 | 0.123 | 30–42 | 30–42 |
| DeepSeek V4.1 Flash (high) · Hermes | 0.996 | 23 | 54/58 | 0.086 | 32–43 | 32–41 |
| DeepSeek V4.1 Flash (high) · pi | 0.999 | 27 | 55/58 | 0.076 | 31–43 | 34–43 |
| DeepSeek V4.1 Flash (high) · fx | 1.007 | 25 | 53/57 | 0.080 | 34–46 | 35–46 |
| DeepSeek V4.1 Flash (high) · DeepSeek Harness | 1.009 | 27 | 64/68 | 0.075 | 39–47 | 41–46 |
| GLM-5.3 Flash (high) · OpenCode | 1.013 | 26 | 52/57 | 0.079 | 41–46 | 33–46 |
| GLM-5.3 Flash (high) · fx | 1.018 | 25 | 50/56 | 0.076 | 42–49 | 42–48 |
| DeepSeek V4.1 Flash (high) · Codex | 1.020 | 28 | 58/61 | 0.071 | 40–49 | 28–49 |
| GLM-5.3 Flash (high) · OpenClaw | 1.028 | 24 | 54/58 | 0.078 | 45–49 | 45–49 |
| GLM-5.3 Flash (high) · Hermes | 1.031 | 29 | 57/60 | 0.069 | 42–50 | 44–50 |
| GLM-5.3 Flash (high) · DeepSeek Harness | 1.033 | 23 | 58/61 | 0.084 | 44–52 | 46–52 |
| Ripple-65B Preview · fx | 1.044 | 21 | 33/37 | 0.103 | 47–52 | 47–53 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.046 | 22 | 43/47 | 0.095 | 47–53 | 50–51 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.063 | 28 | 60/65 | 0.069 | 47–53 | 48–53 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.069 | 25 | 57/63 | 0.079 | 49–54 | 51–54 |
| Ripple-65B Preview · Grok Build | 1.089 | 19 | 36/39 | 0.104 | 53–56 | 54–56 |
| Ripple-65B Preview · OpenClaw | 1.103 | 10 | 13/15 | 0.213 | 53–57 | 53–57 |
| Ripple-65B Preview · Qwen Code | 1.103 | 15 | 23/25 | 0.149 | 54–57 | 54–59 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.124 | 27 | 56/59 | 0.074 | 56–58 | 56–57 |
| Ripple-65B Preview · Kimi Code | 1.164 | 23 | 49/54 | 0.095 | 58–59 | 58–60 |
| Ripple-65B Preview · pi | 1.167 | 22 | 39/44 | 0.085 | 57–60 | 57–59 |
| Ripple-65B Preview · Hermes | 1.184 | 24 | 43/47 | 0.082 | 58–60 | 58–60 |
| Ripple-65B Preview · DeepSeek Harness | 1.229 | 14 | 31/34 | 0.167 | 61–62 | 61–62 |
| Ripple-65B Preview · Codex | 1.261 | 23 | 42/47 | 0.088 | 61–64 | 61–64 |
| Ripple-65B Preview · Claude Code | 1.265 | 17 | 28/32 | 0.117 | 61–64 | 61–64 |
| Ripple-65B Preview · OpenCode | 1.289 | 23 | 40/45 | 0.086 | 61–64 | 61–64 |
| Ripple-65B Preview · mini-SWE-agent | 1.369 | 14 | 23/28 | 0.125 | 65–65 | 65–65 |

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
