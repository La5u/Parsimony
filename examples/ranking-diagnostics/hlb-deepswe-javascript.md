# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-javascript-65-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · OpenClaw | 0.763 | 3 | 5/5 | 0.423 | 1–3 | 1–5 |
| GLM-5.3 Flash (low) · OpenCode | 0.783 | 3 | 7/7 | 0.423 | 2–7 | 2–7 |
| GLM-5.3 Flash (high) · Codex | 0.795 | 4 | 6/6 | 0.303 | 1–15 | 1–15 |
| GLM-5.3 Flash (low) · Kimi Code | 0.801 | 3 | 7/7 | 0.424 | 1–24 | 1–24 |
| GLM-5.3 Flash (low) · Grok Build | 0.805 | 2 | 6/6 | 0.588 | 1–32 | 3–32 |
| GLM-5.3 Flash (low) · Hermes | 0.826 | 3 | 7/7 | 0.378 | 3–22 | 2–22 |
| GLM-5.3 Flash (low) · pi | 0.830 | 4 | 7/7 | 0.302 | 3–9 | 3–9 |
| GLM-5.3 Flash (low) · DeepSeek Harness | 0.850 | 4 | 7/7 | 0.302 | 4–14 | 4–14 |
| GLM-5.3 Flash (low) · Qwen Code | 0.860 | 3 | 5/5 | 0.423 | 8–11 | 8–11 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.869 | 4 | 6/6 | 0.495 | 6–11 | 6–12 |
| DeepSeek V4.1 Flash (low) · oh-my-pi | 0.892 | 4 | 9/9 | 0.495 | 10–14 | 10–14 |
| DeepSeek V4.1 Flash (high) · DeepSeek Harness | 0.896 | 5 | 15/15 | 0.411 | 11–17 | 10–17 |
| DeepSeek V4.1 Flash (high) · Codex | 0.902 | 5 | 11/11 | 0.412 | 12–16 | 13–16 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.908 | 4 | 8/8 | 0.494 | 9–23 | 9–23 |
| DeepSeek V4.1 Flash (low) · Grok Build | 0.917 | 5 | 11/11 | 0.412 | 15–18 | 15–20 |
| Ripple-65B Preview · Qwen Code | 0.918 | 2 | 3/3 | 0.588 | 10–34 | 11–34 |
| DeepSeek V4.1 Flash (high) · Grok Build | 0.924 | 5 | 10/10 | 0.412 | 5–33 | 5–33 |
| DeepSeek V4.1 Flash (low) · DeepSeek Harness | 0.930 | 5 | 11/11 | 0.412 | 14–28 | 15–28 |
| GLM-5.3 Flash (low) · Claude Code | 0.932 | 4 | 7/7 | 0.302 | 11–30 | 11–30 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.937 | 5 | 10/10 | 0.413 | 10–47 | 10–47 |
| DeepSeek V4.1 Flash (high) · fx | 0.938 | 5 | 11/11 | 0.411 | 13–27 | 13–27 |
| DeepSeek V4.1 Flash (high) · Hermes | 0.945 | 4 | 10/10 | 0.495 | 21–26 | 21–26 |
| GLM-5.3 Flash (low) · Codex | 0.945 | 3 | 4/4 | 0.425 | 3–55 | 3–55 |
| GLM-5.3 Flash (low) · fx | 0.947 | 4 | 7/7 | 0.301 | 9–38 | 9–38 |
| DeepSeek V4.1 Flash (low) · fx | 0.951 | 4 | 11/11 | 0.495 | 19–35 | 19–35 |
| GLM-5.3 Flash (high) · fx | 0.955 | 3 | 6/6 | 0.377 | 20–33 | 15–33 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 0.956 | 5 | 12/12 | 0.411 | 23–30 | 23–30 |
| DeepSeek V4.1 Flash (low) · pi | 0.958 | 4 | 9/9 | 0.495 | 16–42 | 16–42 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.962 | 5 | 10/10 | 0.413 | 19–45 | 19–45 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.972 | 5 | 11/11 | 0.412 | 24–38 | 23–38 |
| DeepSeek V4.1 Flash (high) · pi | 0.972 | 5 | 11/11 | 0.412 | 25–39 | 25–39 |
| GLM-5.3 Flash (low) · oh-my-pi | 0.973 | 2 | 3/3 | 0.588 | 24–39 | 22–39 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 0.974 | 4 | 7/7 | 0.301 | 11–38 | 11–46 |
| DeepSeek V4.1 Flash (low) · Codex | 0.980 | 4 | 9/9 | 0.495 | 23–41 | 23–41 |
| GLM-5.3 Flash (high) · oh-my-pi | 0.994 | 2 | 6/6 | 0.587 | 35–37 | 35–37 |
| DeepSeek V4.1 Flash (high) · oh-my-pi | 0.998 | 4 | 9/9 | 0.301 | 24–47 | 24–53 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 0.998 | 5 | 8/8 | 0.411 | 25–41 | 25–41 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.009 | 5 | 12/12 | 0.413 | 30–52 | 30–52 |
| GLM-5.3 Flash (high) · Qwen Code | 1.011 | 4 | 8/8 | 0.465 | 26–46 | 26–46 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.012 | 5 | 10/10 | 0.412 | 28–46 | 28–46 |
| DeepSeek V4.1 Flash (low) · OpenCode | 1.024 | 5 | 13/13 | 0.412 | 34–45 | 34–45 |
| Ripple-65B Preview · Codex | 1.025 | 4 | 7/7 | 0.498 | 7–63 | 7–63 |
| GLM-5.3 Flash (high) · OpenClaw | 1.027 | 3 | 8/8 | 0.423 | 31–46 | 31–46 |
| GLM-5.3 Flash (high) · OpenCode | 1.029 | 4 | 9/9 | 0.493 | 15–49 | 15–49 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 1.031 | 4 | 12/12 | 0.495 | 38–47 | 38–47 |
| GLM-5.3 Flash (high) · Grok Build | 1.032 | 5 | 11/11 | 0.410 | 23–49 | 23–49 |
| GLM-5.3 Flash (high) · Claude Code | 1.035 | 4 | 10/10 | 0.494 | 20–48 | 20–48 |
| GLM-5.3 Flash (high) · Hermes | 1.087 | 4 | 8/8 | 0.494 | 43–52 | 43–52 |
| Ripple-65B Preview · DeepSeek Harness | 1.089 | 3 | 4/4 | 0.577 | 47–55 | 47–55 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.100 | 4 | 9/9 | 0.302 | 43–59 | 43–59 |
| Ripple-65B Preview · Kimi Code | 1.101 | 4 | 8/8 | 0.497 | 35–61 | 35–61 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.102 | 4 | 11/11 | 0.302 | 48–55 | 39–55 |
| GLM-5.3 Flash (high) · Kimi Code | 1.131 | 4 | 8/8 | 0.494 | 48–57 | 48–57 |
| GLM-5.3 Flash (high) · pi | 1.136 | 4 | 9/9 | 0.492 | 21–60 | 21–60 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.138 | 5 | 13/13 | 0.413 | 50–58 | 48–58 |
| GLM-5.3 Flash (high) · DeepSeek Harness | 1.139 | 5 | 10/10 | 0.410 | 49–58 | 49–58 |
| Ripple-65B Preview · OpenCode | 1.142 | 3 | 6/6 | 0.423 | 52–56 | 52–56 |
| Ripple-65B Preview · Grok Build | 1.151 | 4 | 9/9 | 0.494 | 53–58 | 53–58 |
| Ripple-65B Preview · oh-my-pi | 1.188 | 4 | 8/8 | 0.495 | 51–59 | 51–59 |
| Ripple-65B Preview · OpenClaw | 1.256 | 1 | 2/2 | 1.000 | 57–61 | 57–61 |
| Ripple-65B Preview · Claude Code | 1.276 | 2 | 4/4 | 0.602 | 59–62 | 59–62 |
| Ripple-65B Preview · Hermes | 1.282 | 3 | 6/6 | 0.421 | 50–64 | 50–64 |
| Ripple-65B Preview · fx | 1.337 | 1 | 3/3 | 1.000 | 62–63 | 62–63 |
| Ripple-65B Preview · pi | 1.368 | 3 | 6/6 | 0.423 | 60–64 | 60–64 |
| Ripple-65B Preview · mini-SWE-agent | 1.795 | 2 | 3/3 | 0.602 | 63–65 | 63–65 |

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
