# SWE-bench Multilingual — Go

Website: **[parsimony.lasu.dev/multilingual-go.html](https://parsimony.lasu.dev/multilingual-go.html)**. Shared notes: [../multilingual/README.md](../multilingual/README.md).

## Population

All 42 tasks of the Go repositories in [SWE-bench Multilingual](https://www.swebench.com/multilingual.html) (caddy, gin, hugo, terraform, prometheus). A repository's track is the language most of its reference fixes change, so the rule uses only the reference fixes, never model output or outcomes. One attempt per task.

## Results (analyzer 0.11.0-beta, `tree-sitter-go-units-v2`, commit `3cadbda`)

Same-task ratio as on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count; ranked rows need at least 15.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Kimi K2.8 Preview (max) · Rusta 1.0.0 | 0.66× | 0.42–0.87× | 25 | +19.7 | +36.0 | 59.5% | 25/25 |
| 2 | Kimi K2.5 · mini-SWE-agent 2.0 | 0.75× | 0.56–1.00× | 22 | +23.7 | +42.6 | 59.5% | 23/25 |
| 3 | Claude Haiku 4.5 · mini-SWE-agent 2.0 | 0.75× | 0.40–1.15× | 19 | +17.9 | +65.8 | 47.6% | 20/20 |
| 4 | DeepSeek V4.1 Flash (max) · Rusta 1.0.0 | 0.76× | 0.53–0.96× | 26 | +30.4 | +50.1 | 64.3% | 27/27 |
| 5 | MiniMax M2.5 · mini-SWE-agent 2.0 | 0.77× | 0.56–1.01× | 24 | +28.0 | +49.3 | 59.5% | 24/25 |
| 6 | Claude Sonnet 4.5 · mini-SWE-agent 2.0 | 0.81× | 0.53–1.24× | 21 | +20.2 | +69.4 | 54.8% | 22/23 |
| 7 | Gemini 3 Pro · mini-SWE-agent 2.0 | 0.81× | 0.66–0.96× | 22 | +21.4 | +45.2 | 52.4% | 22/22 |
| 8 | Claude Opus 4.5 · mini-SWE-agent 2.0 | 0.82× | 0.47–1.09× | 23 | +29.4 | +35.6 | 57.1% | 23/24 |
| 9 | Claude Opus 4.6 · mini-SWE-agent 2.0 | 0.87× | 0.38–1.31× | 23 | +30.1 | +43.2 | 54.8% | 23/23 |
| 10 | Gemini 3 Flash · mini-SWE-agent 2.0 | 0.94× | 0.52–1.42× | 26 | +34.7 | +43.8 | 61.9% | 26/26 |
| 11 | GLM-5 · mini-SWE-agent 2.0 | 0.94× | 0.65–1.36× | 22 | +28.3 | +44.6 | 57.1% | 23/24 |
| 12 | GLM-5.3 (max) · Rusta 1.0.0 | 1.09× | 0.65–1.94× | 25 | +36.5 | +41.8 | 64.3% | 27/27 |
| 13 | GPT-5.2 Codex · mini-SWE-agent 2.0 | 1.11× | 0.72–1.44× | 20 | +43.1 | +82.7 | 47.6% | 20/20 |
| 14 | GPT-5.2 (high) · mini-SWE-agent 2.0 | 1.35× | 1.05–1.79× | 22 | +49.9 | +76.0 | 52.4% | 22/22 |
| 15 | Gemini 3.5 Flash · mini-SWE-agent 2.4.6 | 1.73× | 1.20–2.60× | 25 | +60.6 | +79.4 | 61.9% | 25/26 |
| 16 | DeepSeek V3.2 · mini-SWE-agent 2.0 | 2.07× | 0.90–4.08× | 19 | +50.6 | +58.7 | 50.0% | 20/21 |
| — | GPT-5 mini · mini-SWE-agent 2.0 | 0.84× | 0.31–1.93× | 13 | +25.3 | +50.6 | 33.3% | 14/14 |

Of 714 attempts: **682 measured**, 6 analysis errors, 26 missing or empty patches, 0 tasks a run has no result for. 394 solved. Missing measurements are never zero. Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md).
