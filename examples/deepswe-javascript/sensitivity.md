# Score sensitivity: 26 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `deepswe-v1.1-javascript-26-pooled-80-20-v0.6`: 20 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (19 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Fable 5 (xhigh) ≈ GLM-5.3 (max) ≈ GPT-5.6 Terra (max) ≈ Kimi K3 (max) ≈ Qwen3.8 Max (xhigh) ≈ Grok 4.6 (medium) ≈ GPT-5.6 Sol (max) ≈ Gemini 3.5 Flash (high) ≈ DeepSeek V4 Pro (max) ≈ Claude Sonnet 5 (max) ≈ Gemini 3.6 Flash (high) ≈ GPT-5.5 (xhigh) ≈ Claude Opus 4.8 (max) ≈ Claude Sonnet 4.6 (high) ≈ Gemini 3.7 Flash (medium) ≈ GPT-5.6 Luna (max) ≈ Grok 4.5 (high) ≈ GLM-5.3 Flash (max) ≈ DeepSeek V4 Flash (max) ≈ Claude Opus 5 (max) ≈ Muse Spark 1.1 (xhigh) ≈ Muse Spark 1.2 (xhigh) ≈ Kimi K2.7 Code ≈ GLM-5.2 (max) ≈ GPT-5.4 (xhigh) ≈ Gemini 3.1 Pro Preview (high) (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (0 of 25 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 25 pairs): Claude Fable 5 (xhigh) vs GLM-5.3 (max), GLM-5.3 (max) vs GPT-5.6 Terra (max), GPT-5.6 Terra (max) vs Kimi K3 (max), Kimi K3 (max) vs Qwen3.8 Max (xhigh), Qwen3.8 Max (xhigh) vs Grok 4.6 (medium), Grok 4.6 (medium) vs GPT-5.6 Sol (max), GPT-5.6 Sol (max) vs Gemini 3.5 Flash (high), Gemini 3.5 Flash (high) vs DeepSeek V4 Pro (max), DeepSeek V4 Pro (max) vs Claude Sonnet 5 (max), Claude Sonnet 5 (max) vs Gemini 3.6 Flash (high), Gemini 3.6 Flash (high) vs GPT-5.5 (xhigh), GPT-5.5 (xhigh) vs Claude Opus 4.8 (max), Claude Opus 4.8 (max) vs Claude Sonnet 4.6 (high), Claude Sonnet 4.6 (high) vs Gemini 3.7 Flash (medium), Gemini 3.7 Flash (medium) vs GPT-5.6 Luna (max), GPT-5.6 Luna (max) vs Grok 4.5 (high), Grok 4.5 (high) vs GLM-5.3 Flash (max), GLM-5.3 Flash (max) vs DeepSeek V4 Flash (max), DeepSeek V4 Flash (max) vs Claude Opus 5 (max), Claude Opus 5 (max) vs Muse Spark 1.1 (xhigh), Muse Spark 1.1 (xhigh) vs Muse Spark 1.2 (xhigh), Muse Spark 1.2 (xhigh) vs Kimi K2.7 Code, Kimi K2.7 Code vs GLM-5.2 (max), GLM-5.2 (max) vs GPT-5.4 (xhigh), GPT-5.4 (xhigh) vs Gemini 3.1 Pro Preview (high).
- **Rank never changes under any variation**: none.

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 20 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Fable 5 (xhigh) | 48.5 | 15.3–77.0 | 48.5 | 1–3 | 1–17 | 0.49 |
| 2 | GLM-5.3 (max) | 40.0 | 22.6–58.9 | 40.0 | 1–6 | 1–15 | 0.14 |
| 3 | GPT-5.6 Terra (max) | 36.0 | 8.6–62.5 | 36.0 | 1–8 | 1–14 | 0.26 |
| 4 | Kimi K3 (max) | 35.8 | 21.7–49.9 | 35.8 | 2–7 | 2–17 | 0.00 |
| 5 | Qwen3.8 Max (xhigh) | 32.4 | 4.6–57.7 | 32.4 | 4–8 | 2–16 | 0.00 |
| 6 | Grok 4.6 (medium) | 31.9 | 10.5–53.4 | 31.9 | 3–13 | 2–22 | 0.00 |
| 7 | GPT-5.6 Sol (max) | 30.1 | 4.8–55.4 | 30.1 | 4–14 | 2–23 | 0.00 |
| 8 | Gemini 3.5 Flash (high) | 29.8 | 3.2–55.0 | 29.8 | 2–14 | 1–21 | 0.11 |
| 9 | DeepSeek V4 Pro (max) | 24.9 | 4.7–44.0 | 24.9 | 8–15 | 6–20 | 0.00 |
| 10 | Claude Sonnet 5 (max) | 24.2 | 12.1–43.9 | 24.2 | 7–12 | 4–18 | 0.00 |
| 11 | Gemini 3.6 Flash (high) | 24.0 | -1.3–49.4 | 24.0 | 7–13 | 2–25 | 0.00 |
| 12 | GPT-5.5 (xhigh) | 23.6 | 0.2–46.3 | 23.6 | 5–17 | 3–20 | 0.00 |
| 13 | Claude Opus 4.8 (max) | 20.5 | -8.3–49.2 | 20.5 | 9–18 | 4–21 | 0.00 |
| 14 | Claude Sonnet 4.6 (high) | 19.1 | -10.6–52.2 | 19.1 | 11–20 | 2–24 | 0.01 |
| 15 | Gemini 3.7 Flash (medium) | 18.2 | -0.8–40.5 | 18.2 | 13–19 | 8–21 | 0.00 |
| 16 | GPT-5.6 Luna (max) | 16.3 | 3.9–28.9 | 16.3 | 11–22 | 6–24 | 0.00 |
| 17 | Grok 4.5 (high) | 16.0 | -10.7–44.0 | 16.0 | 14–22 | 7–24 | 0.00 |
| 18 | GLM-5.3 Flash (max) | 13.4 | -0.6–27.1 | 13.4 | 15–23 | 9–24 | 0.00 |
| 19 | DeepSeek V4 Flash (max) | 12.2 | -7.2–31.7 | 12.2 | 18–23 | 13–24 | 0.00 |
| 20 | Claude Opus 5 (max) | 10.9 | -2.6–22.7 | 10.9 | 17–25 | 9–26 | 0.00 |
| 21 | Muse Spark 1.1 (xhigh) | 10.3 | -10.1–30.4 | 7.9–12.8 | 11–24 | 8–26 | 0.00 |
| 22 | Muse Spark 1.2 (xhigh) | 9.7 | -5.9–31.1 | 9.7 | 15–24 | 11–25 | 0.00 |
| 23 | Kimi K2.7 Code | 9.3 | -12.0–39.6 | 9.3 | 17–26 | 6–26 | 0.00 |
| 24 | GLM-5.2 (max) | 8.6 | -12.2–31.1 | 8.6 | 20–24 | 16–26 | 0.00 |
| 25 | GPT-5.4 (xhigh) | 4.9 | -9.4–22.9 | 4.9 | 20–26 | 13–26 | 0.00 |
| 26 | Gemini 3.1 Pro Preview (high) | 1.2 | -9.2–12.5 | 1.2 | 25–26 | 22–26 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Fable 5 (xhigh) > GLM-5.3 (max) | 8.50 | -24.49 to 40.74 | 0.69 | without testem/testem | yes |
| GLM-5.3 (max) > GPT-5.6 Terra (max) | 3.97 | -32.21 to 39.29 | 0.55 | without KaTeX/KaTeX | yes |
| GPT-5.6 Terra (max) > Kimi K3 (max) | 0.25 | -31.34 to 31.85 | 0.54 | net weight=0.5, net weight=0.6, net weight=0.7, panel without Claude Fable 5 (xhigh), panel without Gemini 3.5 Flash (high), panel without Grok 4.6 (medium), panel without Muse Spark 1.2 (xhigh), without csstree/csstree, without yjs/yjs | yes |
| Kimi K3 (max) > Qwen3.8 Max (xhigh) | 3.42 | -15.94 to 23.92 | 0.60 | without testem/testem | yes |
| Qwen3.8 Max (xhigh) > Grok 4.6 (medium) | 0.42 | -25.15 to 24.68 | 0.55 | failure cap=50, panel without Claude Fable 5 (xhigh), panel without DeepSeek V4 Pro (max), panel without Gemini 3.5 Flash (high), panel without Gemini 3.6 Flash (high), without csstree/csstree, without yjs/yjs | yes |
| Grok 4.6 (medium) > GPT-5.6 Sol (max) | 1.84 | -34.44 to 37.94 | 0.56 | net weight=1, without KaTeX/KaTeX, without testem/testem | yes |
| GPT-5.6 Sol (max) > Gemini 3.5 Flash (high) | 0.33 | -43.82 to 42.05 | 0.53 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=0, failure cap=10, panel without Claude Fable 5 (xhigh), panel without Claude Sonnet 5 (max), panel without Gemini 3.5 Flash (high), panel without Muse Spark 1.2 (xhigh), without KaTeX/KaTeX, without csstree/csstree | yes |
| Gemini 3.5 Flash (high) > DeepSeek V4 Pro (max) | 4.82 | -33.00 to 43.61 | 0.59 | without testem/testem, without yjs/yjs | yes |
| DeepSeek V4 Pro (max) > Claude Sonnet 5 (max) | 0.78 | -23.22 to 26.01 | 0.54 | without KaTeX/KaTeX, without testem/testem | yes |
| Claude Sonnet 5 (max) > Gemini 3.6 Flash (high) | 0.13 | -17.68 to 16.16 | 0.55 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, panel without Claude Fable 5 (xhigh), panel without Claude Sonnet 5 (max), panel without Gemini 3.5 Flash (high), panel without Gemini 3.6 Flash (high), panel without Gemini 3.7 Flash (medium), panel without Grok 4.5 (high), without csstree/csstree | yes |
| Gemini 3.6 Flash (high) > GPT-5.5 (xhigh) | 0.38 | -34.72 to 34.91 | 0.51 | net weight=0.9, net weight=1, failure cap=0, panel without GLM-5.3 Flash (max), panel without GPT-5.6 Sol (max), panel without Grok 4.6 (medium), without KaTeX/KaTeX, without testem/testem, without yjs/yjs | yes |
| GPT-5.5 (xhigh) > Claude Opus 4.8 (max) | 3.15 | -17.08 to 29.06 | 0.58 | without csstree/csstree | yes |
| Claude Opus 4.8 (max) > Claude Sonnet 4.6 (high) | 1.37 | -3.43 to 9.21 | 0.66 | without KaTeX/KaTeX | yes |
| Claude Sonnet 4.6 (high) > Gemini 3.7 Flash (medium) | 0.87 | -14.85 to 24.66 | 0.54 | failure cap=50, without testem/testem | yes |
| Gemini 3.7 Flash (medium) > GPT-5.6 Luna (max) | 1.97 | -21.64 to 23.80 | 0.60 | without yjs/yjs | yes |
| GPT-5.6 Luna (max) > Grok 4.5 (high) | 0.32 | -21.89 to 22.09 | 0.53 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=0, failure cap=10, panel without Muse Spark 1.1 (xhigh), panel without Muse Spark 1.2 (xhigh), without KaTeX/KaTeX, without csstree/csstree | yes |
| Grok 4.5 (high) > GLM-5.3 Flash (max) | 2.51 | -15.60 to 21.40 | 0.61 | failure cap=50, without yjs/yjs | yes |
| GLM-5.3 Flash (max) > DeepSeek V4 Flash (max) | 1.22 | -6.33 to 12.29 | 0.60 | failure cap=0, failure cap=10, without testem/testem | yes |
| DeepSeek V4 Flash (max) > Claude Opus 5 (max) | 1.32 | -14.33 to 16.96 | 0.59 | failure cap=50, without testem/testem, without yjs/yjs | yes |
| Claude Opus 5 (max) > Muse Spark 1.1 (xhigh) | 0.58 | -23.81 to 29.77 | 0.39 | failure cap=0, failure cap=10, panel without GPT-5.5 (xhigh), panel without GPT-5.6 Luna (max), panel without Muse Spark 1.2 (xhigh), without KaTeX/KaTeX, without testem/testem | no |
| Muse Spark 1.1 (xhigh) > Muse Spark 1.2 (xhigh) | 0.68 | -8.79 to 13.79 | 0.29 | failure cap=50, without KaTeX/KaTeX, without csstree/csstree | no |
| Muse Spark 1.2 (xhigh) > Kimi K2.7 Code | 0.37 | -10.98 to 12.33 | 0.52 | failure cap=0, failure cap=10, without KaTeX/KaTeX, without csstree/csstree | yes |
| Kimi K2.7 Code > GLM-5.2 (max) | 0.72 | -15.12 to 17.34 | 0.60 | net weight=0.5, without yjs/yjs | yes |
| GLM-5.2 (max) > GPT-5.4 (xhigh) | 3.64 | -16.31 to 27.68 | 0.58 | without yjs/yjs | yes |
| GPT-5.4 (xhigh) > Gemini 3.1 Pro Preview (high) | 3.71 | -10.62 to 18.04 | 0.64 | without csstree/csstree, without testem/testem | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 48.5 (1) | 48.8 (1) | 48.7 (1) | 48.6 (1) | 48.4 (1) | 48.3 (1) | 48.5 (1) | 52.3 (1) | 50.8 (1) | 44.7 (1) |
| GLM-5.3 (max) | 40.0 (2) | 40.5 (2) | 40.4 (2) | 40.2 (2) | 39.8 (2) | 39.6 (2) | 40.0 (2) | 41.4 (2) | 40.8 (2) | 38.6 (2) |
| GPT-5.6 Terra (max) | 36.0 (3) | 33.8 (4) | 34.5 (4) | 35.3 (4) | 36.8 (3) | 37.5 (3) | 36.0 (3) | 40.1 (3) | 38.4 (3) | 32.0 (3) |
| Kimi K3 (max) | 35.8 (4) | 35.9 (3) | 35.9 (3) | 35.8 (3) | 35.7 (4) | 35.7 (4) | 35.8 (4) | 40.0 (4) | 38.3 (4) | 31.6 (4) |
| Qwen3.8 Max (xhigh) | 32.4 (5) | 33.0 (5) | 32.8 (5) | 32.6 (5) | 32.1 (5) | 31.9 (5) | 32.4 (5) | 36.8 (5) | 35.0 (5) | 27.9 (6) |
| Grok 4.6 (medium) | 31.9 (6) | 32.8 (6) | 32.5 (6) | 32.2 (6) | 31.6 (6) | 31.4 (7) | 31.9 (6) | 34.6 (7) | 33.5 (6) | 29.3 (5) |
| GPT-5.6 Sol (max) | 30.1 (7) | 27.6 (8) | 28.5 (8) | 29.3 (8) | 30.9 (7) | 31.7 (6) | 30.1 (7) | 33.5 (8) | 32.2 (8) | 26.6 (7) |
| Gemini 3.5 Flash (high) | 29.8 (8) | 30.3 (7) | 30.1 (7) | 29.9 (7) | 29.6 (8) | 29.4 (8) | 29.8 (8) | 35.3 (6) | 33.1 (7) | 24.2 (8) |
| DeepSeek V4 Pro (max) | 24.9 (9) | 24.4 (9) | 24.6 (9) | 24.8 (9) | 25.1 (9) | 25.3 (9) | 24.9 (9) | 29.2 (11) | 27.5 (9) | 20.7 (9) |
| Claude Sonnet 5 (max) | 24.2 (10) | 24.0 (11) | 24.0 (11) | 24.1 (10) | 24.2 (11) | 24.3 (11) | 24.2 (10) | 28.6 (12) | 26.8 (12) | 19.7 (10) |
| Gemini 3.6 Flash (high) | 24.0 (11) | 24.2 (10) | 24.1 (10) | 24.1 (11) | 24.0 (12) | 23.9 (12) | 24.0 (11) | 29.7 (10) | 27.4 (10) | 18.4 (11) |
| GPT-5.5 (xhigh) | 23.6 (12) | 21.6 (12) | 22.3 (12) | 23.0 (12) | 24.3 (10) | 25.0 (10) | 23.6 (12) | 29.9 (9) | 27.4 (11) | 17.4 (12) |
| Claude Opus 4.8 (max) | 20.5 (13) | 21.5 (13) | 21.1 (13) | 20.8 (13) | 20.2 (13) | 19.8 (13) | 20.5 (13) | 27.4 (13) | 24.6 (13) | 13.6 (13) |
| Claude Sonnet 4.6 (high) | 19.1 (14) | 19.9 (14) | 19.6 (14) | 19.4 (14) | 18.9 (14) | 18.6 (14) | 19.1 (14) | 26.2 (14) | 23.4 (14) | 12.0 (15) |
| Gemini 3.7 Flash (medium) | 18.2 (15) | 18.9 (15) | 18.7 (15) | 18.5 (15) | 18.0 (15) | 17.8 (15) | 18.2 (15) | 24.0 (15) | 21.7 (15) | 12.5 (14) |
| GPT-5.6 Luna (max) | 16.3 (16) | 15.2 (17) | 15.6 (17) | 15.9 (17) | 16.6 (16) | 17.0 (16) | 16.3 (16) | 21.4 (17) | 19.4 (17) | 11.1 (16) |
| Grok 4.5 (high) | 16.0 (17) | 16.4 (16) | 16.2 (16) | 16.1 (16) | 15.8 (17) | 15.7 (17) | 16.0 (17) | 23.5 (16) | 20.5 (16) | 8.4 (18) |
| GLM-5.3 Flash (max) | 13.4 (18) | 14.1 (18) | 13.9 (18) | 13.7 (18) | 13.2 (18) | 13.0 (18) | 13.4 (18) | 18.5 (19) | 16.5 (19) | 8.4 (17) |
| DeepSeek V4 Flash (max) | 12.2 (19) | 12.4 (19) | 12.3 (19) | 12.3 (19) | 12.2 (19) | 12.1 (19) | 12.2 (19) | 20.1 (18) | 17.0 (18) | 4.3 (20) |
| Claude Opus 5 (max) | 10.9 (20) | 11.7 (20) | 11.5 (20) | 11.2 (20) | 10.6 (20) | 10.4 (20) | 10.9 (20) | 15.3 (24) | 13.5 (23) | 6.6 (19) |
| Muse Spark 1.1 (xhigh) | 10.3 (21) | 10.3 (21) | 10.3 (21) | 10.3 (21) | 10.3 (21) | 10.4 (21) | 10.3 (21) | 18.0 (21) | 14.9 (20) | 2.7 (22) |
| Muse Spark 1.2 (xhigh) | 9.7 (22) | 9.9 (22) | 9.8 (22) | 9.7 (22) | 9.6 (22) | 9.5 (22) | 9.7 (22) | 15.7 (23) | 13.3 (24) | 3.6 (21) |
| Kimi K2.7 Code | 9.3 (23) | 9.2 (24) | 9.2 (23) | 9.2 (23) | 9.3 (23) | 9.4 (23) | 9.3 (23) | 18.1 (20) | 14.5 (21) | 0.5 (23) |
| GLM-5.2 (max) | 8.6 (24) | 9.3 (23) | 9.1 (24) | 8.8 (24) | 8.3 (24) | 8.1 (24) | 8.6 (24) | 17.0 (22) | 13.6 (22) | 0.1 (24) |
| GPT-5.4 (xhigh) | 4.9 (25) | 4.0 (25) | 4.3 (25) | 4.6 (25) | 5.2 (25) | 5.5 (25) | 4.9 (25) | 13.6 (25) | 10.2 (25) | -3.8 (25) |
| Gemini 3.1 Pro Preview (high) | 1.2 (26) | 1.0 (26) | 1.1 (26) | 1.2 (26) | 1.3 (26) | 1.3 (26) | 1.2 (26) | 9.4 (26) | 6.1 (26) | -6.9 (26) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (0 of 1104 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Fable 5 (xhigh) | 56 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, GPT-5.6 Sol (max) 7→8, Gemini 3.5 Flash (high) 8→7, Claude Sonnet 5 (max) 10→11, Gemini 3.6 Flash (high) 11→10 |
| Claude Opus 4.8 (max) | 32 | 0 | none |
| Claude Opus 5 (max) | 52 | 0 | none |
| Claude Sonnet 4.6 (high) | 32 | 0 | none |
| Claude Sonnet 5 (max) | 44 | 0 | GPT-5.6 Sol (max) 7→8, Gemini 3.5 Flash (high) 8→7, DeepSeek V4 Pro (max) 9→10, Claude Sonnet 5 (max) 10→12, Gemini 3.6 Flash (high) 11→9, GPT-5.5 (xhigh) 12→11 |
| DeepSeek V4 Flash (max) | 28 | 0 | none |
| DeepSeek V4 Pro (max) | 52 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5 |
| Gemini 3.1 Pro Preview (high) | 8 | 0 | none |
| Gemini 3.5 Flash (high) | 40 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, GPT-5.6 Sol (max) 7→8, Gemini 3.5 Flash (high) 8→7, DeepSeek V4 Pro (max) 9→10, Claude Sonnet 5 (max) 10→11, Gemini 3.6 Flash (high) 11→9 |
| Gemini 3.6 Flash (high) | 44 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Claude Sonnet 5 (max) 10→11, Gemini 3.6 Flash (high) 11→10 |
| Gemini 3.7 Flash (medium) | 44 | 0 | Claude Sonnet 5 (max) 10→11, Gemini 3.6 Flash (high) 11→10 |
| GLM-5.2 (max) | 24 | 0 | none |
| GLM-5.3 Flash (max) | 48 | 0 | Gemini 3.6 Flash (high) 11→12, GPT-5.5 (xhigh) 12→11 |
| GLM-5.3 (max) | 72 | 0 | none |
| GPT-5.4 (xhigh) | 28 | 0 | none |
| GPT-5.5 (xhigh) | 40 | 0 | Claude Opus 5 (max) 20→21, Muse Spark 1.1 (xhigh) 21→20 |
| GPT-5.6 Luna (max) | 48 | 0 | Claude Opus 5 (max) 20→21, Muse Spark 1.1 (xhigh) 21→20 |
| GPT-5.6 Sol (max) | 60 | 0 | Gemini 3.6 Flash (high) 11→12, GPT-5.5 (xhigh) 12→11 |
| GPT-5.6 Terra (max) | 56 | 0 | none |
| Grok 4.5 (high) | 32 | 0 | Claude Sonnet 5 (max) 10→11, Gemini 3.6 Flash (high) 11→10 |
| Grok 4.6 (medium) | 64 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, Gemini 3.6 Flash (high) 11→12, GPT-5.5 (xhigh) 12→11 |
| Kimi K2.7 Code | 20 | 0 | none |
| Kimi K3 (max) | 52 | 0 | none |
| Muse Spark 1.1 (xhigh) | 32 | 0 | GPT-5.6 Luna (max) 16→17, Grok 4.5 (high) 17→16 |
| Muse Spark 1.2 (xhigh) | 44 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, GPT-5.6 Sol (max) 7→8, Gemini 3.5 Flash (high) 8→7, GPT-5.6 Luna (max) 16→17, Grok 4.5 (high) 17→16, Claude Opus 5 (max) 20→21, Muse Spark 1.1 (xhigh) 21→20 |
| Qwen3.8 Max (xhigh) | 52 | 0 | none |
| (dedup panel) | 0 | 0 | none |

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| KaTeX/KaTeX (4) | Claude Fable 5 (xhigh) 1→3, GLM-5.3 (max) 2→6, GPT-5.6 Terra (max) 3→1, Kimi K3 (max) 4→7, Qwen3.8 Max (xhigh) 5→8, Grok 4.6 (medium) 6→13, GPT-5.6 Sol (max) 7→4, Gemini 3.5 Flash (high) 8→2, DeepSeek V4 Pro (max) 9→15, Claude Sonnet 5 (max) 10→9, Gemini 3.6 Flash (high) 11→10, GPT-5.5 (xhigh) 12→5, Claude Opus 4.8 (max) 13→12, Claude Sonnet 4.6 (high) 14→11, Gemini 3.7 Flash (medium) 15→16, GPT-5.6 Luna (max) 16→17, Grok 4.5 (high) 17→14, DeepSeek V4 Flash (max) 19→23, Claude Opus 5 (max) 20→25, Muse Spark 1.1 (xhigh) 21→22, Muse Spark 1.2 (xhigh) 22→21, Kimi K2.7 Code 23→19, GLM-5.2 (max) 24→20, GPT-5.4 (xhigh) 25→24 |
| csstree/csstree (4) | GPT-5.6 Terra (max) 3→8, Kimi K3 (max) 4→3, Grok 4.6 (medium) 6→4, GPT-5.6 Sol (max) 7→14, Gemini 3.5 Flash (high) 8→6, DeepSeek V4 Pro (max) 9→10, Claude Sonnet 5 (max) 10→11, Gemini 3.6 Flash (high) 11→7, GPT-5.5 (xhigh) 12→17, Claude Opus 4.8 (max) 13→9, Claude Sonnet 4.6 (high) 14→12, Gemini 3.7 Flash (medium) 15→13, GPT-5.6 Luna (max) 16→22, Grok 4.5 (high) 17→15, GLM-5.3 Flash (max) 18→16, DeepSeek V4 Flash (max) 19→18, Claude Opus 5 (max) 20→19, Muse Spark 1.1 (xhigh) 21→24, Muse Spark 1.2 (xhigh) 22→23, Kimi K2.7 Code 23→20, GLM-5.2 (max) 24→21, GPT-5.4 (xhigh) 25→26, Gemini 3.1 Pro Preview (high) 26→25 |
| testem/testem (8) | Claude Fable 5 (xhigh) 1→3, GLM-5.3 (max) 2→1, GPT-5.6 Terra (max) 3→2, Kimi K3 (max) 4→6, Qwen3.8 Max (xhigh) 5→4, Grok 4.6 (medium) 6→10, GPT-5.6 Sol (max) 7→5, Gemini 3.5 Flash (high) 8→14, Claude Sonnet 5 (max) 10→7, Gemini 3.6 Flash (high) 11→12, GPT-5.5 (xhigh) 12→8, Claude Opus 4.8 (max) 13→18, Claude Sonnet 4.6 (high) 14→20, Gemini 3.7 Flash (medium) 15→13, Grok 4.5 (high) 17→22, GLM-5.3 Flash (max) 18→23, DeepSeek V4 Flash (max) 19→21, Claude Opus 5 (max) 20→19, Muse Spark 1.1 (xhigh) 21→11, Muse Spark 1.2 (xhigh) 22→15, Kimi K2.7 Code 23→17, GPT-5.4 (xhigh) 25→26, Gemini 3.1 Pro Preview (high) 26→25 |
| yjs/yjs (4) | GLM-5.3 (max) 2→4, GPT-5.6 Terra (max) 3→5, Kimi K3 (max) 4→2, Qwen3.8 Max (xhigh) 5→7, Grok 4.6 (medium) 6→3, GPT-5.6 Sol (max) 7→6, Gemini 3.5 Flash (high) 8→9, DeepSeek V4 Pro (max) 9→8, Claude Sonnet 5 (max) 10→12, Gemini 3.6 Flash (high) 11→13, GPT-5.5 (xhigh) 12→10, Claude Opus 4.8 (max) 13→14, Claude Sonnet 4.6 (high) 14→16, Gemini 3.7 Flash (medium) 15→19, GPT-5.6 Luna (max) 16→11, Grok 4.5 (high) 17→18, GLM-5.3 Flash (max) 18→15, DeepSeek V4 Flash (max) 19→21, Claude Opus 5 (max) 20→17, Muse Spark 1.1 (xhigh) 21→22, Muse Spark 1.2 (xhigh) 22→24, Kimi K2.7 Code 23→26, GLM-5.2 (max) 24→23, GPT-5.4 (xhigh) 25→20, Gemini 3.1 Pro Preview (high) 26→25 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (19) | Solved by fewer (19) |
|---|---:|---:|
| Claude Fable 5 (xhigh) | 48.5 (1) | 48.5 (1) |
| GLM-5.3 (max) | 40.0 (2) | 40.0 (2) |
| GPT-5.6 Terra (max) | 36.0 (3) | 36.0 (3) |
| Kimi K3 (max) | 35.8 (4) | 35.8 (4) |
| Qwen3.8 Max (xhigh) | 32.4 (5) | 32.4 (5) |
| Grok 4.6 (medium) | 31.9 (6) | 31.9 (6) |
| GPT-5.6 Sol (max) | 30.1 (7) | 30.1 (7) |
| Gemini 3.5 Flash (high) | 29.8 (8) | 29.8 (8) |
| DeepSeek V4 Pro (max) | 24.9 (9) | 24.9 (9) |
| Claude Sonnet 5 (max) | 24.2 (10) | 24.2 (10) |
| Gemini 3.6 Flash (high) | 24.0 (11) | 24.0 (11) |
| GPT-5.5 (xhigh) | 23.6 (12) | 23.6 (12) |
| Claude Opus 4.8 (max) | 20.5 (13) | 20.5 (13) |
| Claude Sonnet 4.6 (high) | 19.1 (14) | 19.1 (14) |
| Gemini 3.7 Flash (medium) | 18.2 (15) | 18.2 (15) |
| GPT-5.6 Luna (max) | 16.3 (16) | 16.3 (16) |
| Grok 4.5 (high) | 16.0 (17) | 16.0 (17) |
| GLM-5.3 Flash (max) | 13.4 (18) | 13.4 (18) |
| DeepSeek V4 Flash (max) | 12.2 (19) | 12.2 (19) |
| Claude Opus 5 (max) | 10.9 (20) | 10.9 (20) |
| Muse Spark 1.1 (xhigh) | 10.3 (21) | 10.3 (21) |
| Muse Spark 1.2 (xhigh) | 9.7 (22) | 9.7 (22) |
| Kimi K2.7 Code | 9.3 (23) | 9.3 (23) |
| GLM-5.2 (max) | 8.6 (24) | 8.6 (24) |
| GPT-5.4 (xhigh) | 4.9 (25) | 4.9 (25) |
| Gemini 3.1 Pro Preview (high) | 1.2 (26) | 1.2 (26) |

## What drives each adjacent gap

Difference in mean score split by outcome (a/b), and the tasks that move it most. Contributions are per-task differences divided by the task count, so they sum to the gap.

- **Claude Fable 5 (xhigh) − GLM-5.3 (max) = 8.50**: failed/solved -13.50 (5), solved/failed 5.28 (1), solved/solved 16.72 (13). For Claude Fable 5 (xhigh): `testem-bail-on-test-failure#2` +5.28 (solved/failed), `testem-per-launcher-reports#1` +4.35 (solved/solved), `testem-per-launcher-reports#2` +3.44 (solved/solved). For GLM-5.3 (max): `csstree-shorthand-expansion-compression#2` -3.43 (failed/solved), `csstree-shorthand-expansion-compression#1` -3.01 (failed/solved), `yjs-map-conflict-detection#4` -2.72 (failed/solved).
- **GLM-5.3 (max) − GPT-5.6 Terra (max) = 3.97**: failed/failed -0.06 (1), failed/solved -3.16 (1), solved/failed 16.25 (5), solved/solved -9.06 (13). For GLM-5.3 (max): `katex-multicolumn-array-spans#1` +5.16 (solved/failed), `katex-multicolumn-array-spans#2` +3.37 (solved/failed), `testem-bail-on-test-failure#4` +3.08 (solved/failed). For GPT-5.6 Terra (max): `testem-per-launcher-reports#2` -4.03 (solved/solved), `csstree-shorthand-expansion-compression#3` -3.16 (failed/solved), `testem-per-launcher-reports#1` -2.74 (solved/solved).
- **GPT-5.6 Terra (max) − Kimi K3 (max) = 0.25**: failed/failed -0.14 (2), failed/solved -17.64 (4), solved/failed 18.17 (5), solved/solved -0.13 (9). For GPT-5.6 Terra (max): `testem-per-launcher-reports#2` +4.79 (solved/failed), `csstree-shorthand-expansion-compression#2` +4.65 (solved/failed), `katex-multicolumn-array-spans#3` +3.92 (solved/failed). For Kimi K3 (max): `testem-bail-on-test-failure#3` -4.91 (failed/solved), `katex-multicolumn-array-spans#2` -4.63 (failed/solved), `katex-multicolumn-array-spans#1` -4.12 (failed/solved).
- **Kimi K3 (max) − Qwen3.8 Max (xhigh) = 3.42**: failed/failed 0.16 (4), failed/solved -11.28 (3), solved/failed 12.10 (3), solved/solved 2.44 (10). For Kimi K3 (max): `testem-bail-on-test-failure#3` +4.77 (solved/failed), `testem-bail-on-test-failure#4` +3.97 (solved/failed), `csstree-shorthand-expansion-compression#3` +3.35 (solved/failed). For Qwen3.8 Max (xhigh): `katex-multicolumn-array-spans#3` -4.55 (failed/solved), `testem-per-launcher-reports#2` -3.48 (failed/solved), `yjs-map-conflict-detection#2` -3.25 (failed/solved).
- **Qwen3.8 Max (xhigh) − Grok 4.6 (medium) = 0.42**: failed/failed 0.03 (2), failed/solved -11.97 (5), solved/failed 7.97 (2), solved/solved 4.39 (11). For Qwen3.8 Max (xhigh): `csstree-shorthand-expansion-compression#1` +4.15 (solved/failed), `katex-multicolumn-array-spans#1` +3.82 (solved/failed), `yjs-map-conflict-detection#1` +3.15 (solved/solved). For Grok 4.6 (medium): `katex-multicolumn-array-spans#2` -3.69 (solved/solved), `testem-bail-on-test-failure#2` -3.58 (failed/solved), `testem-bail-on-test-failure#3` -3.34 (failed/solved).
- **Grok 4.6 (medium) − GPT-5.6 Sol (max) = 1.84**: failed/failed 0.05 (1), failed/solved -7.19 (3), solved/failed 15.09 (4), solved/solved -6.11 (12). For Grok 4.6 (medium): `katex-multicolumn-array-spans#3` +5.22 (solved/failed), `katex-multicolumn-array-spans#4` +3.89 (solved/solved), `katex-multicolumn-array-spans#2` +3.73 (solved/solved). For GPT-5.6 Sol (max): `csstree-shorthand-expansion-compression#4` -4.05 (solved/solved), `csstree-shorthand-expansion-compression#3` -3.75 (solved/solved), `csstree-shorthand-expansion-compression#1` -2.80 (failed/solved).
- **GPT-5.6 Sol (max) − Gemini 3.5 Flash (high) = 0.33**: failed/failed -0.26 (2), failed/solved -14.03 (3), solved/failed 24.15 (8), solved/solved -9.53 (7). For GPT-5.6 Sol (max): `csstree-shorthand-expansion-compression#4` +5.22 (solved/failed), `csstree-shorthand-expansion-compression#3` +4.72 (solved/failed), `testem-per-launcher-reports#1` +4.52 (solved/failed). For Gemini 3.5 Flash (high): `testem-bail-on-test-failure#1` -5.10 (failed/solved), `yjs-map-conflict-detection#4` -4.56 (solved/solved), `testem-bail-on-test-failure#2` -4.54 (failed/solved).
- **Gemini 3.5 Flash (high) − DeepSeek V4 Pro (max) = 4.82**: failed/failed 0.02 (3), failed/solved -16.19 (7), solved/failed 17.42 (4), solved/solved 3.57 (6). For Gemini 3.5 Flash (high): `testem-bail-on-test-failure#1` +5.08 (solved/failed), `yjs-map-conflict-detection#1` +4.72 (solved/solved), `testem-bail-on-test-failure#2` +4.52 (solved/failed). For DeepSeek V4 Pro (max): `csstree-shorthand-expansion-compression#3` -3.67 (failed/solved), `testem-per-launcher-reports#3` -3.21 (solved/solved), `katex-multicolumn-array-spans#4` -3.13 (failed/solved).
- **DeepSeek V4 Pro (max) − Claude Sonnet 5 (max) = 0.78**: failed/failed -0.24 (4), failed/solved -7.93 (3), solved/failed 16.01 (5), solved/solved -7.05 (8). For DeepSeek V4 Pro (max): `testem-per-launcher-reports#4` +5.48 (solved/failed), `csstree-shorthand-expansion-compression#3` +3.76 (solved/failed), `yjs-map-conflict-detection#3` +3.17 (solved/failed). For Claude Sonnet 5 (max): `testem-bail-on-test-failure#2` -5.37 (failed/solved), `yjs-map-conflict-detection#1` -3.89 (solved/solved), `yjs-map-conflict-detection#2` -3.19 (solved/solved).
- **Claude Sonnet 5 (max) − Gemini 3.6 Flash (high) = 0.13**: failed/failed 0.23 (3), failed/solved -17.70 (6), solved/failed 11.87 (6), solved/solved 5.74 (5). For Claude Sonnet 5 (max): `katex-multicolumn-array-spans#2` +3.02 (solved/failed), `testem-per-launcher-reports#3` +2.57 (solved/failed), `csstree-shorthand-expansion-compression#2` +2.11 (solved/failed). For Gemini 3.6 Flash (high): `testem-bail-on-test-failure#3` -4.47 (failed/solved), `testem-bail-on-test-failure#1` -4.02 (failed/solved), `yjs-map-conflict-detection#3` -2.96 (failed/solved).
- **Gemini 3.6 Flash (high) − GPT-5.5 (xhigh) = 0.38**: failed/failed -0.15 (5), failed/solved -17.25 (4), solved/failed 18.37 (5), solved/solved -0.58 (6). For Gemini 3.6 Flash (high): `yjs-map-conflict-detection#2` +4.89 (solved/failed), `testem-bail-on-test-failure#3` +4.61 (solved/failed), `testem-bail-on-test-failure#2` +3.85 (solved/failed). For GPT-5.5 (xhigh): `csstree-shorthand-expansion-compression#1` -5.56 (failed/solved), `csstree-shorthand-expansion-compression#4` -4.90 (failed/solved), `testem-per-launcher-reports#1` -4.87 (failed/solved).
- **GPT-5.5 (xhigh) − Claude Opus 4.8 (max) = 3.15**: failed/failed -0.48 (8), failed/solved -8.32 (2), solved/failed 16.81 (4), solved/solved -4.85 (6). For GPT-5.5 (xhigh): `csstree-shorthand-expansion-compression#1` +5.55 (solved/failed), `csstree-shorthand-expansion-compression#4` +4.94 (solved/failed), `yjs-map-conflict-detection#4` +4.82 (solved/failed). For Claude Opus 4.8 (max): `yjs-map-conflict-detection#2` -4.95 (failed/solved), `testem-per-launcher-reports#4` -3.49 (solved/solved), `katex-multicolumn-array-spans#1` -3.38 (failed/solved).
- **Claude Opus 4.8 (max) − Claude Sonnet 4.6 (high) = 1.37**: failed/failed 0.22 (10), failed/solved -3.35 (2), solved/failed 7.87 (2), solved/solved -3.37 (6). For Claude Opus 4.8 (max): `yjs-map-conflict-detection#3` +4.66 (solved/failed), `katex-multicolumn-array-spans#1` +3.21 (solved/failed), `testem-per-launcher-reports#1` +1.42 (solved/solved). For Claude Sonnet 4.6 (high): `yjs-map-conflict-detection#4` -2.52 (failed/solved), `yjs-map-conflict-detection#1` -2.01 (solved/solved), `testem-per-launcher-reports#3` -1.68 (solved/solved).
- **Claude Sonnet 4.6 (high) − Gemini 3.7 Flash (medium) = 0.87**: failed/failed 0.27 (8), failed/solved -12.22 (4), solved/failed 0.95 (1), solved/solved 11.86 (7). For Claude Sonnet 4.6 (high): `testem-per-launcher-reports#3` +3.69 (solved/solved), `testem-per-launcher-reports#4` +3.47 (solved/solved), `testem-per-launcher-reports#2` +1.78 (solved/solved). For Gemini 3.7 Flash (medium): `katex-multicolumn-array-spans#2` -4.24 (failed/solved), `yjs-map-conflict-detection#3` -4.21 (failed/solved), `testem-bail-on-test-failure#2` -2.22 (failed/solved).
- **Gemini 3.7 Flash (medium) − GPT-5.6 Luna (max) = 1.97**: failed/failed 0.02 (6), failed/solved -8.50 (3), solved/failed 7.05 (2), solved/solved 3.41 (9). For Gemini 3.7 Flash (medium): `katex-multicolumn-array-spans#2` +4.41 (solved/failed), `yjs-map-conflict-detection#1` +3.16 (solved/solved), `yjs-map-conflict-detection#2` +3.14 (solved/solved). For GPT-5.6 Luna (max): `csstree-shorthand-expansion-compression#1` -4.53 (failed/solved), `csstree-shorthand-expansion-compression#4` -2.85 (solved/solved), `katex-multicolumn-array-spans#1` -2.66 (failed/solved).
- **GPT-5.6 Luna (max) − Grok 4.5 (high) = 0.32**: failed/failed -0.21 (7), failed/solved -3.96 (1), solved/failed 11.57 (5), solved/solved -7.09 (7). For GPT-5.6 Luna (max): `csstree-shorthand-expansion-compression#1` +4.55 (solved/failed), `katex-multicolumn-array-spans#1` +2.72 (solved/failed), `csstree-shorthand-expansion-compression#4` +2.70 (solved/solved). For Grok 4.5 (high): `testem-per-launcher-reports#1` -3.96 (failed/solved), `yjs-map-conflict-detection#1` -3.04 (solved/solved), `yjs-map-conflict-detection#2` -2.38 (solved/solved).
- **Grok 4.5 (high) − GLM-5.3 Flash (max) = 2.51**: failed/failed -0.16 (7), failed/solved -12.08 (5), solved/failed 1.63 (1), solved/solved 13.12 (7). For Grok 4.5 (high): `yjs-map-conflict-detection#2` +3.17 (solved/solved), `yjs-map-conflict-detection#1` +2.78 (solved/solved), `testem-per-launcher-reports#1` +1.85 (solved/solved). For GLM-5.3 Flash (max): `yjs-map-conflict-detection#4` -3.13 (failed/solved), `testem-bail-on-test-failure#1` -2.84 (failed/solved), `testem-bail-on-test-failure#2` -2.23 (failed/solved).
- **GLM-5.3 Flash (max) − DeepSeek V4 Flash (max) = 1.22**: failed/failed -0.14 (7), failed/solved -3.66 (1), solved/failed 12.69 (6), solved/solved -7.67 (6). For GLM-5.3 Flash (max): `testem-bail-on-test-failure#1` +2.82 (solved/failed), `testem-per-launcher-reports#2` +2.62 (solved/failed), `testem-bail-on-test-failure#2` +2.10 (solved/failed). For DeepSeek V4 Flash (max): `yjs-map-conflict-detection#2` -3.81 (solved/solved), `katex-multicolumn-array-spans#4` -3.66 (failed/solved), `testem-per-launcher-reports#4` -3.03 (solved/solved).
- **DeepSeek V4 Flash (max) − Claude Opus 5 (max) = 1.32**: failed/failed 0.10 (7), failed/solved -10.85 (6), solved/solved 12.06 (7). For DeepSeek V4 Flash (max): `yjs-map-conflict-detection#2` +4.04 (solved/solved), `testem-per-launcher-reports#3` +3.82 (solved/solved), `testem-per-launcher-reports#4` +3.14 (solved/solved). For Claude Opus 5 (max): `katex-multicolumn-array-spans#1` -3.83 (failed/solved), `testem-bail-on-test-failure#3` -1.78 (failed/solved), `yjs-map-conflict-detection#1` -1.54 (failed/solved).
- **Claude Opus 5 (max) − Muse Spark 1.1 (xhigh) = -0.01**: failed/failed 0.16 (4), failed/solved -8.43 (3), solved/failed 14.09 (7), solved/solved -5.83 (5). For Claude Opus 5 (max): `katex-multicolumn-array-spans#2` +2.87 (solved/failed), `katex-multicolumn-array-spans#4` +2.73 (solved/failed), `testem-per-launcher-reports#4` +2.24 (solved/failed). For Muse Spark 1.1 (xhigh): `csstree-shorthand-expansion-compression#2` -4.41 (failed/solved), `csstree-shorthand-expansion-compression#4` -2.99 (failed/solved), `yjs-map-conflict-detection#3` -2.75 (solved/solved).
- **Muse Spark 1.1 (xhigh) − Muse Spark 1.2 (xhigh) = -2.83**: failed/failed -0.16 (4), failed/solved -10.52 (7), solved/failed 9.21 (4), solved/solved -1.36 (4). For Muse Spark 1.1 (xhigh): `csstree-shorthand-expansion-compression#2` +4.33 (solved/failed), `csstree-shorthand-expansion-compression#4` +2.89 (solved/failed), `testem-bail-on-test-failure#1` +1.07 (solved/failed). For Muse Spark 1.2 (xhigh): `csstree-shorthand-expansion-compression#3` -4.07 (failed/solved), `testem-per-launcher-reports#3` -1.91 (failed/solved), `yjs-map-conflict-detection#2` -1.78 (solved/solved).
- **Muse Spark 1.2 (xhigh) − Kimi K2.7 Code = 0.37**: failed/failed -0.86 (9), solved/failed 8.57 (6), solved/solved -7.34 (5). For Muse Spark 1.2 (xhigh): `csstree-shorthand-expansion-compression#3` +3.89 (solved/failed), `testem-per-launcher-reports#3` +1.77 (solved/failed), `katex-multicolumn-array-spans#2` +0.98 (solved/failed). For Kimi K2.7 Code: `testem-per-launcher-reports#2` -3.04 (solved/solved), `yjs-map-conflict-detection#2` -1.85 (solved/solved), `yjs-map-conflict-detection#1` -1.01 (solved/solved).
- **Kimi K2.7 Code − GLM-5.2 (max) = 0.72**: failed/failed 0.05 (13), failed/solved -4.71 (2), solved/failed 4.38 (1), solved/solved 1.00 (4). For Kimi K2.7 Code: `yjs-map-conflict-detection#4` +4.38 (solved/failed), `yjs-map-conflict-detection#3` +2.01 (solved/solved), `yjs-map-conflict-detection#2` +1.34 (solved/solved). For GLM-5.2 (max): `testem-per-launcher-reports#4` -3.68 (failed/solved), `yjs-map-conflict-detection#1` -1.96 (solved/solved), `testem-per-launcher-reports#1` -1.03 (failed/solved).
- **GLM-5.2 (max) − GPT-5.4 (xhigh) = 3.64**: failed/failed 0.87 (11), failed/solved -7.76 (3), solved/failed 8.13 (2), solved/solved 2.40 (4). For GLM-5.2 (max): `yjs-map-conflict-detection#1` +4.91 (solved/failed), `yjs-map-conflict-detection#3` +3.22 (solved/failed), `testem-per-launcher-reports#2` +1.92 (solved/solved). For GPT-5.4 (xhigh): `csstree-shorthand-expansion-compression#1` -5.39 (failed/solved), `testem-per-launcher-reports#3` -1.42 (failed/solved), `testem-per-launcher-reports#4` -1.03 (solved/solved).
- **GPT-5.4 (xhigh) − Gemini 3.1 Pro Preview (high) = 3.71**: failed/failed -2.71 (12), failed/solved -5.57 (1), solved/failed 12.22 (6), solved/solved -0.23 (1). For GPT-5.4 (xhigh): `csstree-shorthand-expansion-compression#1` +5.17 (solved/failed), `testem-per-launcher-reports#2` +2.39 (solved/failed), `yjs-map-conflict-detection#2` +1.50 (solved/failed). For Gemini 3.1 Pro Preview (high): `yjs-map-conflict-detection#3` -5.57 (failed/solved), `csstree-shorthand-expansion-compression#2` -0.30 (failed/failed), `katex-multicolumn-array-spans#2` -0.29 (failed/failed).

## Regenerate

```sh
python -m parsimony.stability examples/deepswe-javascript/score-panel.json examples/deepswe-javascript/*.jsonl --output examples/deepswe-javascript/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
