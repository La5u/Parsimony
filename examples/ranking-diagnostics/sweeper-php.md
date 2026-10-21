# Same-task net ratio diagnostics

Panel: `sweeper-php-v1` · `same-task-net-diagnostics-v1`

These diagnostics do not change the website ranking. Lower footprint is not better coding quality.

## Coverage and influence

| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3.8 Max (none) · Codex | 0.133 | 38 | 38/40 | 0.101 | 1–1 | 1–1 |
| GLM-5.3 Flash (max) · Codex | 0.297 | 51 | 53/55 | 0.044 | 2–2 | 2–2 |
| DeepSeek V4.1 Flash (xhigh) · DeepSeek harness | 0.573 | 64 | 67/68 | 0.061 | 3–4 | 3–4 |
| Kimi K3 (high) · Kimi Code | 0.592 | 62 | 65/66 | 0.054 | 3–5 | 3–5 |
| GPT-5.6 Terra (xhigh) · Codex | 0.604 | 45 | 45/46 | 0.072 | 3–5 | 3–5 |
| GPT-5.6 Luna (xhigh) · Codex | 0.739 | 54 | 55/57 | 0.061 | 6–6 | 6–6 |
| Muse Spark 1.3 (xhigh) · Muse Code | 0.796 | 61 | 62/65 | 0.068 | 7–8 | 7–8 |
| Claude Opus 5 (xhigh) · Claude Code | 0.829 | 67 | 70/71 | 0.063 | 7–8 | 7–8 |
| GLM-5.3 (max) · Codex | 0.950 | 55 | 55/56 | 0.056 | 9–10 | 9–10 |
| GPT-6 Astra (xhigh) · Codex | 0.989 | 72 | 75/78 | 0.056 | 9–12 | 9–12 |
| DeepSeek V4 Pro (xhigh) · DeepSeek harness | 1.010 | 63 | 64/66 | 0.054 | 10–12 | 10–12 |
| GPT-5.6 Sol (xhigh) · Codex | 1.050 | 60 | 60/63 | 0.060 | 10–12 | 10–12 |
| Claude Fable 5.1 (xhigh) · Claude Code | 1.198 | 67 | 70/73 | 0.050 | 13–13 | 13–13 |
| Qwen3.8 Flash (xhigh) · Codex | 2.167 | 70 | 73/76 | 0.066 | 14–14 | 14–14 |
| Grok 4.6 (xhigh-fast) · Cursor | 2.675 | 64 | 71/78 | 0.055 | 15–15 | 15–15 |

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
