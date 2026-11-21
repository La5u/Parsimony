# SWE-bench Multilingual — PHP

Website: **[parsimony.lasu.dev/multilingual-php.html](https://parsimony.lasu.dev/multilingual-php.html)**. Shared notes: [../multilingual/README.md](../multilingual/README.md).

## Population

All 43 tasks of the PHP repositories in [SWE-bench Multilingual](https://www.swebench.com/multilingual.html) (carbon, laravel/framework, php-cs-fixer, phpspreadsheet). A repository's track is the language most of its reference fixes change, so the rule uses only the reference fixes, never model output or outcomes. One attempt per task.

## Results (analyzer 0.11.0-beta, `tree-sitter-php-units-v1`, commit `3cadbda`)

Same-task ratio as on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count; ranked rows need at least 15.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | DeepSeek V4.1 Flash (max) · Rusta 1.0.0 | 0.49× | 0.14–0.73× | 34 | +43.6 | +38.5 | 81.4% | 35/35 |
| 2 | MiniMax M2.5 · mini-SWE-agent 2.0 | 0.57× | 0.25–0.88× | 27 | +17.4 | +29.4 | 62.8% | 27/27 |
| 3 | Kimi K2.8 Preview (max) · Rusta 1.0.0 | 0.69× | 0.45–1.02× | 30 | +21.3 | +33.4 | 69.8% | 30/30 |
| 4 | Kimi K2.5 · mini-SWE-agent 2.0 | 0.79× | 0.41–1.80× | 29 | +19.7 | +28.6 | 69.8% | 29/30 |
| 5 | GLM-5.3 (max) · Rusta 1.0.0 | 0.80× | 0.53–1.29× | 34 | +25.2 | +27.7 | 83.7% | 36/36 |
| 6 | Claude Opus 4.6 · mini-SWE-agent 2.0 | 0.83× | 0.32–1.19× | 32 | +26.3 | +30.3 | 76.7% | 33/33 |
| 7 | Claude Sonnet 4.5 · mini-SWE-agent 2.0 | 0.96× | 0.49–1.28× | 32 | +28.6 | +38.4 | 74.4% | 32/32 |
| 8 | GLM-5 · mini-SWE-agent 2.0 | 0.98× | 0.57–1.30× | 31 | +32.5 | +44.1 | 79.1% | 33/34 |
| 9 | GPT-5 mini · mini-SWE-agent 2.0 | 1.00× | 0.68–1.55× | 21 | +26.9 | +26.0 | 48.8% | 21/21 |
| 10 | Claude Opus 4.5 · mini-SWE-agent 2.0 | 1.02× | 0.44–1.33× | 30 | +27.4 | +33.3 | 72.1% | 31/31 |
| 11 | Gemini 3.5 Flash · mini-SWE-agent 2.4.6 | 1.03× | 0.37–1.46× | 33 | +26.8 | +50.0 | 76.7% | 33/33 |
| 12 | Gemini 3 Flash · mini-SWE-agent 2.0 | 1.05× | 0.68–1.74× | 30 | +21.5 | +29.7 | 69.8% | 30/30 |
| 13 | Gemini 3 Pro · mini-SWE-agent 2.0 | 1.10× | 0.62–2.08× | 28 | +25.5 | +34.4 | 65.1% | 28/28 |
| 14 | DeepSeek V3.2 · mini-SWE-agent 2.0 | 1.30× | 0.77–2.22× | 30 | +31.7 | +40.0 | 69.8% | 30/30 |
| 15 | Claude Haiku 4.5 · mini-SWE-agent 2.0 | 1.38× | 0.52–3.20× | 31 | +36.8 | +43.0 | 74.4% | 32/32 |
| 16 | GPT-5.2 Codex · mini-SWE-agent 2.0 | 1.48× | 1.02–2.31× | 30 | +41.5 | +44.0 | 72.1% | 31/31 |
| 17 | GPT-5.2 (high) · mini-SWE-agent 2.0 | 2.06× | 1.16–3.12× | 30 | +49.9 | +64.2 | 69.8% | 30/30 |

Of 731 attempts: **712 measured**, 7 analysis errors, 11 missing or empty patches, 1 tasks a run has no result for. 523 solved. Missing measurements are never zero. Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md).
