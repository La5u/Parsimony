# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-python-65-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · Codex | 0.834 | 19 | 29/30 | 0.090 | 1–1 | 1–1 |
| GLM-5.3 Flash (low) · Qwen Code | 0.862 | 26 | 45/45 | 0.068 | 2–4 | 2–4 |
| GLM-5.3 Flash (high) · Codex | 0.867 | 18 | 30/32 | 0.103 | 2–4 | 2–4 |
| GLM-5.3 Flash (low) · Grok Build | 0.867 | 29 | 52/52 | 0.061 | 2–4 | 2–4 |
| GLM-5.3 Flash (low) · pi | 0.886 | 29 | 54/55 | 0.061 | 5–5 | 5–5 |
| GLM-5.3 Flash (low) · fx | 0.898 | 25 | 51/51 | 0.067 | 6–9 | 6–9 |
| GLM-5.3 Flash (low) · Hermes | 0.901 | 24 | 48/50 | 0.074 | 6–9 | 6–9 |
| GLM-5.3 Flash (low) · Kimi Code | 0.901 | 27 | 52/54 | 0.065 | 6–9 | 6–9 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.908 | 28 | 59/61 | 0.063 | 7–11 | 7–11 |
| GLM-5.3 Flash (low) · Claude Code | 0.908 | 25 | 55/55 | 0.070 | 8–12 | 8–15 |
| GLM-5.3 Flash (low) · oh-my-pi | 0.912 | 23 | 42/43 | 0.081 | 7–12 | 7–17 |
| GLM-5.3 Flash (low) · OpenClaw | 0.914 | 25 | 51/52 | 0.073 | 10–12 | 10–13 |
| GLM-5.3 Flash (low) · OpenCode | 0.925 | 25 | 51/53 | 0.071 | 12–15 | 10–15 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 0.926 | 29 | 59/61 | 0.058 | 12–17 | 12–15 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.927 | 27 | 55/58 | 0.062 | 13–16 | 11–16 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.937 | 26 | 54/57 | 0.066 | 15–19 | 12–19 |
| DeepSeek V4.1 Flash (high) · oh-my-pi | 0.944 | 28 | 50/51 | 0.063 | 14–22 | 14–22 |
| GLM-5.3 Flash (high) · Qwen Code | 0.944 | 27 | 58/59 | 0.062 | 16–21 | 16–23 |
| GLM-5.3 Flash (high) · oh-my-pi | 0.946 | 27 | 58/59 | 0.067 | 16–21 | 16–21 |
| DeepSeek V4.1 Flash (high) · Codex | 0.947 | 28 | 60/64 | 0.065 | 17–22 | 17–22 |
| DeepSeek V4.1 Flash (high) · Grok Build | 0.948 | 29 | 58/60 | 0.061 | 14–22 | 13–22 |
| DeepSeek V4.1 Flash (low) · fx | 0.956 | 26 | 57/58 | 0.064 | 20–28 | 20–28 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.959 | 26 | 60/62 | 0.066 | 19–27 | 19–27 |
| GLM-5.3 Flash (high) · Hermes | 0.960 | 26 | 53/53 | 0.063 | 18–27 | 18–27 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.961 | 27 | 53/55 | 0.067 | 22–33 | 22–33 |
| GLM-5.3 Flash (high) · Kimi Code | 0.962 | 29 | 61/63 | 0.059 | 22–30 | 22–30 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 0.971 | 27 | 58/61 | 0.063 | 25–34 | 25–34 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.971 | 28 | 65/67 | 0.061 | 22–30 | 20–30 |
| GLM-5.3 Flash (high) · Grok Build | 0.972 | 29 | 68/69 | 0.061 | 24–33 | 24–33 |
| DeepSeek V4.1 Flash (low) · oh-my-pi | 0.974 | 26 | 52/54 | 0.064 | 22–39 | 22–39 |
| DeepSeek V4.1 Flash (low) · Grok Build | 0.975 | 27 | 63/64 | 0.066 | 26–35 | 26–35 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.978 | 30 | 68/69 | 0.060 | 24–35 | 24–35 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 0.978 | 25 | 48/51 | 0.071 | 20–38 | 20–38 |
| GLM-5.3 Flash (high) · Claude Code | 0.981 | 27 | 64/65 | 0.067 | 28–36 | 28–36 |
| DeepSeek V4.1 Flash (high) · Hermes | 0.986 | 27 | 55/58 | 0.065 | 30–40 | 30–40 |
| GLM-5.3 Flash (high) · fx | 0.986 | 29 | 66/67 | 0.061 | 32–38 | 32–39 |
| DeepSeek V4.1 Flash (high) · fx | 0.987 | 26 | 57/60 | 0.066 | 34–39 | 32–39 |
| GLM-5.3 Flash (high) · OpenCode | 0.989 | 28 | 61/62 | 0.062 | 33–41 | 33–40 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.996 | 27 | 60/62 | 0.065 | 35–41 | 35–41 |
| GLM-5.3 Flash (high) · pi | 0.996 | 28 | 63/63 | 0.062 | 35–42 | 35–43 |
| DeepSeek V4.1 Flash (low) · Codex | 0.997 | 27 | 53/55 | 0.064 | 36–43 | 36–43 |
| DeepSeek V4.1 Flash (low) · DeepSeek Harness | 1.007 | 25 | 52/53 | 0.072 | 35–44 | 32–45 |
| GLM-5.3 Flash (high) · OpenClaw | 1.009 | 28 | 61/62 | 0.061 | 38–47 | 38–48 |
| DeepSeek V4.1 Flash (high) · pi | 1.012 | 29 | 55/56 | 0.060 | 42–45 | 42–45 |
| GLM-5.3 Flash (low) · DeepSeek Harness | 1.015 | 27 | 55/55 | 0.066 | 42–47 | 42–47 |
| DeepSeek V4.1 Flash (high) · DeepSeek Harness | 1.024 | 28 | 63/66 | 0.063 | 45–47 | 45–47 |
| DeepSeek V4.1 Flash (low) · pi | 1.029 | 24 | 55/56 | 0.074 | 43–48 | 42–48 |
| Ripple-65B Preview · oh-my-pi | 1.050 | 19 | 35/37 | 0.083 | 45–49 | 45–49 |
| GLM-5.3 Flash (high) · DeepSeek Harness | 1.072 | 29 | 71/71 | 0.059 | 49–52 | 49–53 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.072 | 27 | 62/62 | 0.062 | 49–54 | 49–51 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.073 | 25 | 65/67 | 0.071 | 48–53 | 47–56 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.084 | 26 | 54/55 | 0.067 | 49–54 | 49–54 |
| Ripple-65B Preview · OpenClaw | 1.092 | 22 | 27/28 | 0.080 | 50–55 | 50–55 |
| Ripple-65B Preview · OpenCode | 1.093 | 24 | 43/45 | 0.073 | 52–56 | 52–55 |
| Ripple-65B Preview · fx | 1.097 | 20 | 37/40 | 0.082 | 52–56 | 52–56 |
| Ripple-65B Preview · Qwen Code | 1.105 | 20 | 28/31 | 0.088 | 50–56 | 51–56 |
| Ripple-65B Preview · Grok Build | 1.123 | 21 | 42/45 | 0.080 | 57–58 | 57–59 |
| Ripple-65B Preview · DeepSeek Harness | 1.133 | 18 | 34/36 | 0.087 | 57–60 | 57–60 |
| Ripple-65B Preview · Kimi Code | 1.137 | 23 | 46/48 | 0.069 | 57–60 | 57–60 |
| Ripple-65B Preview · pi | 1.141 | 22 | 41/44 | 0.076 | 57–60 | 57–60 |
| Ripple-65B Preview · Hermes | 1.185 | 23 | 49/51 | 0.068 | 61–62 | 61–63 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.202 | 27 | 61/64 | 0.066 | 61–63 | 61–63 |
| Ripple-65B Preview · Codex | 1.227 | 24 | 46/48 | 0.072 | 63–64 | 62–64 |
| Ripple-65B Preview · Claude Code | 1.231 | 22 | 46/48 | 0.072 | 62–64 | 62–64 |
| Ripple-65B Preview · mini-SWE-agent | 1.500 | 19 | 29/31 | 0.091 | 65–65 | 65–65 |

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
