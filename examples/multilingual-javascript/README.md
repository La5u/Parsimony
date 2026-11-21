# SWE-bench Multilingual — JavaScript

Website: **[parsimony.lasu.dev/multilingual-javascript.html](https://parsimony.lasu.dev/multilingual-javascript.html)**. Shared notes: [../multilingual/README.md](../multilingual/README.md).

## Population

All 28 tasks of the JavaScript repositories in [SWE-bench Multilingual](https://www.swebench.com/multilingual.html) (axios, immutable-js, three.js, preact). A repository's track is the language most of its reference fixes change, so the rule uses only the reference fixes, never model output or outcomes. One attempt per task.

## Results (analyzer 0.11.0-beta, `typescript-compiler-units-v1`, commit `3cadbda`)

Same-task ratio as on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count; ranked rows need at least 15.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Claude Opus 4.6 · mini-SWE-agent 2.0 | 0.62× | 0.48–0.77× | 25 | +14.0 | +35.7 | 92.9% | 26/26 |
| 2 | Kimi K2.8 Preview (max) · Rusta 1.0.0 | 0.63× | 0.38–0.86× | 25 | +15.0 | +17.4 | 89.3% | 25/25 |
| 3 | DeepSeek V4.1 Flash (max) · Rusta 1.0.0 | 0.76× | 0.40–1.12× | 25 | +17.4 | +39.5 | 89.3% | 25/25 |
| 4 | Claude Haiku 4.5 · mini-SWE-agent 2.0 | 0.77× | 0.45–1.27× | 19 | +13.3 | +20.2 | 67.9% | 19/19 |
| 5 | MiniMax M2.5 · mini-SWE-agent 2.0 | 0.79× | 0.55–1.08× | 19 | +12.5 | +27.6 | 67.9% | 19/19 |
| 6 | Claude Opus 4.5 · mini-SWE-agent 2.0 | 0.79× | 0.57–1.08× | 23 | +14.7 | +32.8 | 85.7% | 24/24 |
| 7 | GLM-5.3 (max) · Rusta 1.0.0 | 0.80× | 0.57–0.98× | 22 | +15.1 | +27.2 | 78.6% | 22/22 |
| 8 | Gemini 3 Pro · mini-SWE-agent 2.0 | 0.85× | 0.57–1.06× | 23 | +16.4 | +21.3 | 82.1% | 23/23 |
| 9 | Gemini 3 Flash · mini-SWE-agent 2.0 | 0.85× | 0.59–1.28× | 20 | +15.2 | +20.5 | 71.4% | 20/20 |
| 10 | Claude Sonnet 4.5 · mini-SWE-agent 2.0 | 0.91× | 0.69–1.18× | 19 | +12.8 | +21.1 | 67.9% | 19/19 |
| 11 | Kimi K2.5 · mini-SWE-agent 2.0 | 0.96× | 0.46–1.33× | 19 | +18.7 | +20.2 | 71.4% | 19/20 |
| 12 | GLM-5 · mini-SWE-agent 2.0 | 1.09× | 0.76–1.46× | 18 | +15.5 | +21.5 | 64.3% | 18/18 |
| 13 | Gemini 3.5 Flash · mini-SWE-agent 2.4.6 | 1.20× | 0.93–1.40× | 21 | +27.2 | +27.2 | 75.0% | 21/21 |
| 14 | GPT-5.2 (high) · mini-SWE-agent 2.0 | 1.64× | 1.19–2.36× | 22 | +30.2 | +49.4 | 78.6% | 22/22 |
| 15 | GPT-5.2 Codex · mini-SWE-agent 2.0 | 1.72× | 0.99–2.88× | 21 | +30.8 | +59.7 | 75.0% | 21/21 |
| 16 | DeepSeek V3.2 · mini-SWE-agent 2.0 | 2.21× | 0.88–5.73× | 17 | +37.3 | +36.1 | 60.7% | 17/17 |
| — | GPT-5 mini · mini-SWE-agent 2.0 | 1.55× | 1.04–3.26× | 10 | +18.0 | +24.3 | 35.7% | 10/10 |

Of 476 attempts: **462 measured**, 2 analysis errors, 4 missing or empty patches, 8 tasks a run has no result for. 351 solved. Missing measurements are never zero. Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md).
