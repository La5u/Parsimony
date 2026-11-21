# SWE-bench Multilingual — TypeScript

Website: **[parsimony.lasu.dev/multilingual-typescript.html](https://parsimony.lasu.dev/multilingual-typescript.html)**. Shared notes: [../multilingual/README.md](../multilingual/README.md).

## Population

All 15 tasks of the TypeScript repositories in [SWE-bench Multilingual](https://www.swebench.com/multilingual.html) (babel, docusaurus, vuejs/core). A repository's track is the language most of its reference fixes change, so the rule uses only the reference fixes, never model output or outcomes. One attempt per task.

## Results (analyzer 0.11.0-beta, `typescript-compiler-units-v1`, commit `3cadbda`)

Same-task ratio as on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count; ranked rows need at least 15.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5 · mini-SWE-agent 2.0 | 0.26× | -0.32–0.90× | 8 | +12.6 | +18.0 | 66.7% | 9/10 |
| 2 | Claude Opus 4.5 · mini-SWE-agent 2.0 | 0.30× | -0.37–0.96× | 8 | +4.9 | +13.8 | 60.0% | 8/9 |
| 3 | Claude Opus 4.6 · mini-SWE-agent 2.0 | 0.68× | 0.44–0.86× | 8 | +20.6 | +24.5 | 66.7% | 9/10 |
| 4 | GLM-5.3 (max) · Rusta 1.0.0 | 0.74× | 0.46–1.13× | 8 | +12.6 | +23.6 | 66.7% | 9/10 |
| 5 | DeepSeek V4.1 Flash (max) · Rusta 1.0.0 | 0.92× | 0.48–1.48× | 9 | +16.4 | +35.3 | 80.0% | 11/12 |
| 6 | Claude Sonnet 4.5 · mini-SWE-agent 2.0 | 0.95× | 0.51–1.13× | 8 | +14.9 | +19.7 | 60.0% | 8/9 |
| 7 | Kimi K2.8 Preview (max) · Rusta 1.0.0 | 1.04× | 0.73–1.29× | 8 | +22.8 | +29.9 | 66.7% | 9/10 |
| 8 | MiniMax M2.5 · mini-SWE-agent 2.0 | 1.26× | 0.48–2.64× | 8 | +21.5 | +27.6 | 60.0% | 8/9 |
| 9 | GPT-5.2 Codex · mini-SWE-agent 2.0 | 1.69× | 1.14–2.05× | 8 | +28.9 | +36.5 | 60.0% | 8/9 |
| — | GPT-5 mini · mini-SWE-agent 2.0 | 0.62× | — | 4 | +15.0 | +25.8 | 33.3% | 4/5 |
| — | Gemini 3 Flash · mini-SWE-agent 2.0 | 0.81× | 0.34–2.05× | 7 | +14.6 | +19.6 | 53.3% | 7/8 |
| — | GPT-5.2 (high) · mini-SWE-agent 2.0 | 0.99× | 0.64–1.16× | 7 | +14.1 | +32.2 | 53.3% | 7/8 |
| — | Gemini 3 Pro · mini-SWE-agent 2.0 | 1.01× | 0.76–1.18× | 7 | +17.9 | +28.5 | 53.3% | 7/8 |
| — | Gemini 3.5 Flash · mini-SWE-agent 2.4.6 | 1.05× | — | 3 | +13.7 | +34.0 | 26.7% | 3/4 |
| — | Kimi K2.5 · mini-SWE-agent 2.0 | 1.25× | 0.48–2.25× | 5 | +27.8 | +40.8 | 40.0% | 5/6 |
| — | Claude Haiku 4.5 · mini-SWE-agent 2.0 | 1.72× | 0.25–3.24× | 6 | +33.3 | +27.6 | 46.7% | 6/7 |
| — | DeepSeek V3.2 · mini-SWE-agent 2.0 | 2.06× | 1.33–3.20× | 7 | +36.8 | +35.9 | 53.3% | 8/8 |

Of 255 attempts: **214 measured**, 20 analysis errors, 12 missing or empty patches, 9 tasks a run has no result for. 142 solved. Missing measurements are never zero. Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md).
