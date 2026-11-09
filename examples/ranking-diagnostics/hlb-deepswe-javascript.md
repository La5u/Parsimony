# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-javascript-40-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (low) · OpenCode 2 | 0.771 | 3 | 7/7 | 0.405 | 1–5 | 1–5 |
| GLM-5.3 Flash (high) · Codex | 0.781 | 4 | 6/6 | 0.291 | 1–11 | 1–11 |
| GLM-5.3 Flash (low) · pi | 0.816 | 4 | 7/7 | 0.289 | 2–9 | 2–9 |
| GLM-5.3 Flash (low) · Qwen Code | 0.847 | 3 | 5/5 | 0.405 | 5–7 | 5–7 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.851 | 4 | 10/10 | 0.511 | 6–7 | 6–8 |
| DeepSeek V4.1 Flash (high) · Codex | 0.864 | 5 | 11/11 | 0.428 | 4–10 | 7–10 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.869 | 4 | 9/9 | 0.487 | 4–13 | 4–13 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.873 | 5 | 11/11 | 0.429 | 3–21 | 3–21 |
| GLM-5.3 Flash (low) · Hermes | 0.873 | 3 | 6/6 | 0.406 | 3–20 | 4–20 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.877 | 4 | 9/9 | 0.510 | 4–17 | 4–17 |
| DeepSeek V4.1 Flash (low) · pi | 0.883 | 5 | 10/10 | 0.430 | 1–28 | 1–28 |
| GLM-5.3 Flash (low) · Kimi Code | 0.883 | 2 | 3/3 | 0.581 | 4–27 | 5–27 |
| DeepSeek V4.1 Flash (high) · pi | 0.887 | 5 | 12/12 | 0.429 | 5–26 | 5–26 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.897 | 5 | 13/13 | 0.429 | 8–27 | 10–27 |
| GLM-5.3 Flash (low) · Claude Code | 0.917 | 4 | 7/7 | 0.288 | 10–21 | 10–21 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.922 | 5 | 10/10 | 0.429 | 9–29 | 9–29 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.929 | 5 | 10/10 | 0.427 | 13–23 | 13–23 |
| DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.931 | 5 | 11/11 | 0.428 | 15–20 | 16–20 |
| GLM-5.3 Flash (low) · Codex | 0.932 | 3 | 4/4 | 0.407 | 2–33 | 2–33 |
| DeepSeek V4.1 Flash (low) · Codex | 0.935 | 4 | 9/9 | 0.512 | 13–24 | 13–24 |
| GLM-5.3 Flash (high) · Kimi Code | 0.953 | 4 | 7/7 | 0.288 | 12–27 | 12–27 |
| GLM-5.3 Flash (high) · Qwen Code | 0.975 | 4 | 8/8 | 0.485 | 16–26 | 16–26 |
| DeepSeek V4.1 Flash (low) · OpenCode 2 | 0.981 | 5 | 13/13 | 0.427 | 21–25 | 20–25 |
| GLM-5.3 Flash (high) · OpenCode 2 | 0.983 | 4 | 9/9 | 0.509 | 9–31 | 9–31 |
| GLM-5.3 Flash (high) · Claude Code | 0.989 | 4 | 10/10 | 0.509 | 11–29 | 11–29 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 0.990 | 5 | 13/13 | 0.430 | 16–35 | 16–35 |
| DeepSeek V4.1 Flash (high) · Hermes | 1.002 | 5 | 11/11 | 0.426 | 23–28 | 23–29 |
| GLM-5.3 Flash (low) · OpenClaw | 1.008 | 3 | 5/5 | 0.404 | 18–33 | 18–33 |
| GLM-5.3 Flash (high) · Hermes | 1.037 | 4 | 9/9 | 0.287 | 22–34 | 22–34 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 1.054 | 5 | 11/11 | 0.429 | 23–36 | 23–36 |
| GLM-5.3 Flash (low) · OpenCode | 1.062 | 2 | 2/2 | 0.578 | 20–35 | 20–35 |
| GLM-5.3 Flash (high) · OpenCode | 1.070 | 1 | 2/2 | 1.000 | 31–34 | 31–34 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.083 | 5 | 14/14 | 0.430 | 26–37 | 26–37 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.083 | 4 | 9/9 | 0.287 | 28–37 | 28–37 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.085 | 4 | 11/11 | 0.289 | 30–36 | 26–36 |
| GLM-5.3 Flash (high) · pi | 1.087 | 4 | 9/9 | 0.507 | 14–36 | 14–36 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.372 | 3 | 6/6 | 0.408 | 31–39 | 31–38 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.452 | 4 | 10/10 | 0.501 | 19–38 | 19–38 |
| GLM-5.3 Flash (high) · OpenClaw | 1.566 | 1 | 1/1 | 1.000 | 38–40 | 37–40 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 2.122 | 4 | 6/6 | 0.495 | 39–40 | 39–40 |

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
