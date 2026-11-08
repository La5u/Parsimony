# Same-task net ratio diagnostics

Panel: `hlb-deepswe-v1.1-javascript-36-pooled-80-20` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.3 Flash (high) · Codex | 0.775 | 4 | 6/6 | 0.292 | 1–10 | 1–10 |
| GLM-5.3 Flash (low) · pi | 0.809 | 4 | 7/7 | 0.290 | 1–8 | 1–8 |
| GLM-5.3 Flash (low) · Qwen Code | 0.834 | 3 | 5/5 | 0.404 | 3–6 | 4–6 |
| DeepSeek V4.1 Flash (low) · Qwen Code | 0.842 | 4 | 10/10 | 0.509 | 3–6 | 3–7 |
| DeepSeek V4.1 Flash (high) · Codex | 0.858 | 5 | 11/11 | 0.427 | 4–9 | 6–8 |
| GLM-5.3 Flash (low) · Hermes | 0.860 | 3 | 6/6 | 0.404 | 2–18 | 3–18 |
| DeepSeek V4.1 Flash (high) · Claude Code | 0.867 | 5 | 11/11 | 0.429 | 2–18 | 2–18 |
| DeepSeek V4.1 Flash (high) · Qwen Code | 0.867 | 4 | 9/9 | 0.508 | 3–16 | 3–16 |
| DeepSeek V4.1 Flash (low) · OpenCode | 0.867 | 4 | 9/9 | 0.489 | 3–12 | 3–12 |
| DeepSeek V4.1 Flash (low) · pi | 0.877 | 5 | 10/10 | 0.430 | 1–24 | 1–24 |
| GLM-5.3 Flash (low) · Kimi Code | 0.878 | 2 | 3/3 | 0.584 | 3–26 | 4–26 |
| DeepSeek V4.1 Flash (high) · pi | 0.880 | 5 | 12/12 | 0.429 | 5–22 | 5–22 |
| DeepSeek V4.1 Flash (low) · Hermes | 0.891 | 5 | 13/13 | 0.429 | 7–23 | 9–23 |
| GLM-5.3 Flash (low) · Claude Code | 0.910 | 4 | 7/7 | 0.289 | 9–19 | 9–19 |
| DeepSeek V4.1 Flash (low) · Claude Code | 0.915 | 5 | 10/10 | 0.429 | 8–25 | 8–25 |
| GLM-5.3 Flash (low) · Codex | 0.918 | 3 | 4/4 | 0.406 | 2–29 | 2–29 |
| DeepSeek V4.1 Flash (high) · OpenCode | 0.923 | 5 | 10/10 | 0.427 | 12–21 | 12–21 |
| DeepSeek V4.1 Flash (low) · Codex | 0.926 | 4 | 9/9 | 0.510 | 13–19 | 13–19 |
| GLM-5.3 Flash (high) · Kimi Code | 0.946 | 4 | 7/7 | 0.288 | 11–24 | 11–24 |
| GLM-5.3 Flash (high) · Qwen Code | 0.973 | 4 | 8/8 | 0.487 | 14–23 | 14–23 |
| GLM-5.3 Flash (high) · Claude Code | 0.979 | 4 | 10/10 | 0.507 | 9–25 | 9–25 |
| DeepSeek V4.1 Flash (low) · mini-SWE-agent | 0.983 | 5 | 13/13 | 0.431 | 15–31 | 15–31 |
| GLM-5.3 Flash (low) · OpenClaw | 0.993 | 3 | 5/5 | 0.402 | 16–29 | 16–29 |
| DeepSeek V4.1 Flash (high) · Hermes | 0.996 | 5 | 11/11 | 0.426 | 20–25 | 20–27 |
| GLM-5.3 Flash (high) · Hermes | 1.029 | 4 | 9/9 | 0.288 | 20–30 | 20–30 |
| DeepSeek V4.1 Flash (low) · Kimi Code | 1.047 | 5 | 11/11 | 0.429 | 21–32 | 21–32 |
| GLM-5.3 Flash (low) · OpenCode | 1.056 | 2 | 2/2 | 0.581 | 18–31 | 18–31 |
| GLM-5.3 Flash (high) · OpenCode | 1.072 | 1 | 2/2 | 1.000 | 27–31 | 27–31 |
| GLM-5.3 Flash (low) · mini-SWE-agent | 1.075 | 4 | 9/9 | 0.288 | 25–33 | 25–33 |
| DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.076 | 5 | 14/14 | 0.430 | 22–33 | 22–33 |
| GLM-5.3 Flash (high) · pi | 1.077 | 4 | 9/9 | 0.504 | 10–32 | 10–32 |
| GLM-5.3 Flash (high) · mini-SWE-agent | 1.078 | 4 | 11/11 | 0.290 | 26–32 | 20–32 |
| DeepSeek V4.1 Flash (low) · OpenClaw | 1.366 | 3 | 6/6 | 0.401 | 28–34 | 28–34 |
| DeepSeek V4.1 Flash (high) · Kimi Code | 1.442 | 4 | 10/10 | 0.497 | 17–34 | 17–34 |
| GLM-5.3 Flash (high) · OpenClaw | 1.552 | 1 | 1/1 | 1.000 | 34–36 | 33–36 |
| DeepSeek V4.1 Flash (high) · OpenClaw | 2.115 | 4 | 6/6 | 0.490 | 35–36 | 35–36 |

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
