# Score sensitivity: 26 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `deepswe-v1.1-javascript-26-pooled-80-20-v0.7`: 20 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (20 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Fable 5 (xhigh) ≈ GLM-5.3 (max) ≈ GPT-5.6 Terra (max) ≈ Kimi K3 (max) ≈ Qwen3.8 Max (xhigh) ≈ Grok 4.6 (medium) ≈ Gemini 3.5 Flash (high) ≈ GPT-5.6 Sol (max) ≈ DeepSeek V4 Pro (max) ≈ Gemini 3.6 Flash (high) ≈ Claude Sonnet 5 (max) ≈ GPT-5.5 (xhigh) ≈ Claude Opus 4.8 (max) ≈ Claude Sonnet 4.6 (high) ≈ Gemini 3.7 Flash (medium) ≈ GPT-5.6 Luna (max) ≈ Grok 4.5 (high) ≈ GLM-5.3 Flash (max) ≈ DeepSeek V4 Flash (max) ≈ Claude Opus 5 (max) ≈ Muse Spark 1.2 (xhigh) ≈ Kimi K2.7 Code ≈ GLM-5.2 (max) ≈ Muse Spark 1.1 (xhigh) ≈ GPT-5.4 (xhigh) ≈ Gemini 3.1 Pro Preview (high) (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (0 of 25 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 25 pairs): Claude Fable 5 (xhigh) vs GLM-5.3 (max), GLM-5.3 (max) vs GPT-5.6 Terra (max), GPT-5.6 Terra (max) vs Kimi K3 (max), Kimi K3 (max) vs Qwen3.8 Max (xhigh), Qwen3.8 Max (xhigh) vs Grok 4.6 (medium), Grok 4.6 (medium) vs Gemini 3.5 Flash (high), Gemini 3.5 Flash (high) vs GPT-5.6 Sol (max), GPT-5.6 Sol (max) vs DeepSeek V4 Pro (max), DeepSeek V4 Pro (max) vs Gemini 3.6 Flash (high), Gemini 3.6 Flash (high) vs Claude Sonnet 5 (max), Claude Sonnet 5 (max) vs GPT-5.5 (xhigh), GPT-5.5 (xhigh) vs Claude Opus 4.8 (max), Claude Opus 4.8 (max) vs Claude Sonnet 4.6 (high), Claude Sonnet 4.6 (high) vs Gemini 3.7 Flash (medium), Gemini 3.7 Flash (medium) vs GPT-5.6 Luna (max), GPT-5.6 Luna (max) vs Grok 4.5 (high), Grok 4.5 (high) vs GLM-5.3 Flash (max), GLM-5.3 Flash (max) vs DeepSeek V4 Flash (max), DeepSeek V4 Flash (max) vs Claude Opus 5 (max), Claude Opus 5 (max) vs Muse Spark 1.2 (xhigh), Muse Spark 1.2 (xhigh) vs Kimi K2.7 Code, Kimi K2.7 Code vs GLM-5.2 (max), GLM-5.2 (max) vs Muse Spark 1.1 (xhigh), Muse Spark 1.1 (xhigh) vs GPT-5.4 (xhigh), GPT-5.4 (xhigh) vs Gemini 3.1 Pro Preview (high).
- **Midpoint rank never changes under any variation**: none.

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 20 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Fable 5 (xhigh) | 48.6 | 15.3–76.9 | 48.6 | 1–3 | 1–18 | 0.51 |
| 2 | GLM-5.3 (max) | 39.7 | 22.7–58.6 | 39.7 | 1–6 | 1–15 | 0.13 |
| 3 | GPT-5.6 Terra (max) | 36.1 | 9.0–62.2 | 36.1 | 2–8 | 1–13 | 0.24 |
| 4 | Kimi K3 (max) | 35.6 | 21.4–49.7 | 35.6 | 2–7 | 3–16 | 0.00 |
| 5 | Qwen3.8 Max (xhigh) | 32.1 | 4.5–57.6 | 32.1 | 5–8 | 2–16 | 0.00 |
| 6 | Grok 4.6 (medium) | 31.9 | 10.4–53.4 | 31.9 | 3–13 | 2–22 | 0.00 |
| 7 | Gemini 3.5 Flash (high) | 30.9 | 4.6–55.8 | 30.9 | 1–13 | 1–20 | 0.11 |
| 8 | GPT-5.6 Sol (max) | 30.3 | 5.4–55.3 | 30.3 | 4–14 | 2–23 | 0.00 |
| 9 | DeepSeek V4 Pro (max) | 24.8 | 4.1–43.8 | 24.8 | 8–16 | 6–20 | 0.00 |
| 10 | Gemini 3.6 Flash (high) | 24.2 | -1.4–49.8 | 24.2 | 7–13 | 2–25 | 0.01 |
| 11 | Claude Sonnet 5 (max) | 24.2 | 12.3–43.9 | 24.2 | 7–12 | 4–19 | 0.00 |
| 12 | GPT-5.5 (xhigh) | 23.3 | -0.2–46.1 | 23.3 | 5–17 | 3–20 | 0.00 |
| 13 | Claude Opus 4.8 (max) | 20.8 | -8.3–49.8 | 20.8 | 9–18 | 4–21 | 0.00 |
| 14 | Claude Sonnet 4.6 (high) | 19.3 | -10.6–53.0 | 19.3 | 11–21 | 2–24 | 0.01 |
| 15 | Gemini 3.7 Flash (medium) | 19.1 | -0.3–41.9 | 19.1 | 11–18 | 6–20 | 0.00 |
| 16 | GPT-5.6 Luna (max) | 16.9 | 4.9–29.1 | 16.9 | 11–22 | 6–23 | 0.00 |
| 17 | Grok 4.5 (high) | 15.8 | -10.9–43.7 | 15.8 | 14–22 | 7–24 | 0.00 |
| 18 | GLM-5.3 Flash (max) | 13.1 | -0.5–26.6 | 13.1 | 16–23 | 9–24 | 0.00 |
| 19 | DeepSeek V4 Flash (max) | 12.5 | -7.1–32.1 | 12.5 | 18–22 | 13–24 | 0.00 |
| 20 | Claude Opus 5 (max) | 11.1 | -2.6–23.4 | 11.1 | 16–25 | 9–26 | 0.00 |
| 21 | Muse Spark 1.2 (xhigh) | 9.7 | -5.6–31.2 | 9.7 | 15–23 | 11–24 | 0.00 |
| 22 | Kimi K2.7 Code | 9.2 | -12.0–39.5 | 9.2 | 17–26 | 7–26 | 0.00 |
| 23 | GLM-5.2 (max) | 8.8 | -12.2–31.0 | 8.8 | 20–24 | 16–26 | 0.00 |
| 24 | Muse Spark 1.1 (xhigh) | 8.1 | -9.8–30.0 | 8.1 | 14–24 | 8–26 | 0.00 |
| 25 | GPT-5.4 (xhigh) | 4.8 | -9.2–22.2 | 4.8 | 21–26 | 13–26 | 0.00 |
| 26 | Gemini 3.1 Pro Preview (high) | 1.4 | -9.1–12.7 | 1.4 | 25–26 | 22–26 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Fable 5 (xhigh) > GLM-5.3 (max) | 8.90 | -24.10 to 40.25 | 0.69 | without testem/testem | yes |
| GLM-5.3 (max) > GPT-5.6 Terra (max) | 3.61 | -32.48 to 38.85 | 0.55 | without KaTeX/KaTeX | yes |
| GPT-5.6 Terra (max) > Kimi K3 (max) | 0.50 | -30.58 to 31.59 | 0.55 | net weight=0.5, net weight=0.6, net weight=0.7, panel without Claude Fable 5 (xhigh), panel without Gemini 3.5 Flash (high), without csstree/csstree, without yjs/yjs | yes |
| Kimi K3 (max) > Qwen3.8 Max (xhigh) | 3.42 | -15.52 to 23.01 | 0.60 | without testem/testem | yes |
| Qwen3.8 Max (xhigh) > Grok 4.6 (medium) | 0.19 | -25.61 to 24.64 | 0.55 | failure cap=50, panel without Claude Fable 5 (xhigh), panel without DeepSeek V4 Pro (max), panel without Gemini 3.5 Flash (high), panel without Gemini 3.6 Flash (high), panel without GPT-5.6 Sol (max), panel without Grok 4.5 (high), panel without Kimi K3 (max), panel without Qwen3.8 Max (xhigh), without csstree/csstree, without yjs/yjs | yes |
| Grok 4.6 (medium) > Gemini 3.5 Flash (high) | 1.00 | -36.50 to 43.75 | 0.51 | failure cap=0, failure cap=10, without KaTeX/KaTeX | yes |
| Gemini 3.5 Flash (high) > GPT-5.6 Sol (max) | 0.59 | -40.58 to 45.17 | 0.51 | net weight=0.9, net weight=1, failure cap=50, panel without GLM-5.3 (max), panel without GPT-5.5 (xhigh), without testem/testem, without yjs/yjs | yes |
| GPT-5.6 Sol (max) > DeepSeek V4 Pro (max) | 5.56 | -14.14 to 28.60 | 0.70 | without csstree/csstree | yes |
| DeepSeek V4 Pro (max) > Gemini 3.6 Flash (high) | 0.54 | -39.34 to 37.07 | 0.55 | net weight=0.5, failure cap=0, failure cap=10, panel without Claude Sonnet 5 (max), panel without Gemini 3.5 Flash (high), without KaTeX/KaTeX, without csstree/csstree | yes |
| Gemini 3.6 Flash (high) > Claude Sonnet 5 (max) | 0.05 | -15.55 to 17.69 | 0.50 | net weight=0.9, net weight=1, failure cap=50, panel without Claude Opus 5 (max), panel without DeepSeek V4 Flash (max), panel without GLM-5.2 (max), panel without GLM-5.3 Flash (max), panel without GLM-5.3 (max), panel without GPT-5.4 (xhigh), panel without GPT-5.5 (xhigh), panel without GPT-5.6 Luna (max), panel without GPT-5.6 Sol (max), panel without GPT-5.6 Terra (max), panel without Grok 4.6 (medium), panel without Kimi K3 (max), panel without Muse Spark 1.1 (xhigh), panel without Muse Spark 1.2 (xhigh), panel without Qwen3.8 Max (xhigh), without testem/testem, without yjs/yjs | yes |
| Claude Sonnet 5 (max) > GPT-5.5 (xhigh) | 0.88 | -20.06 to 21.58 | 0.54 | net weight=1, failure cap=0, failure cap=10, without KaTeX/KaTeX, without yjs/yjs | yes |
| GPT-5.5 (xhigh) > Claude Opus 4.8 (max) | 2.55 | -18.22 to 29.20 | 0.56 | net weight=0.5, without csstree/csstree | yes |
| Claude Opus 4.8 (max) > Claude Sonnet 4.6 (high) | 1.45 | -3.40 to 9.18 | 0.66 | without KaTeX/KaTeX | yes |
| Claude Sonnet 4.6 (high) > Gemini 3.7 Flash (medium) | 0.24 | -15.42 to 24.36 | 0.51 | failure cap=50, panel without Claude Fable 5 (xhigh), panel without Claude Sonnet 5 (max), panel without Gemini 3.5 Flash (high), panel without Grok 4.6 (medium), without testem/testem | yes |
| Gemini 3.7 Flash (medium) > GPT-5.6 Luna (max) | 2.17 | -21.44 to 25.42 | 0.60 | without yjs/yjs | yes |
| GPT-5.6 Luna (max) > Grok 4.5 (high) | 1.09 | -21.68 to 23.43 | 0.57 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, without KaTeX/KaTeX, without csstree/csstree | yes |
| Grok 4.5 (high) > GLM-5.3 Flash (max) | 2.76 | -15.62 to 21.56 | 0.60 | without yjs/yjs | yes |
| GLM-5.3 Flash (max) > DeepSeek V4 Flash (max) | 0.52 | -6.87 to 11.36 | 0.51 | failure cap=0, failure cap=10, panel without Claude Opus 5 (max), panel without Muse Spark 1.2 (xhigh), without testem/testem | yes |
| DeepSeek V4 Flash (max) > Claude Opus 5 (max) | 1.40 | -14.54 to 17.35 | 0.59 | failure cap=50, without testem/testem, without yjs/yjs | yes |
| Claude Opus 5 (max) > Muse Spark 1.2 (xhigh) | 1.46 | -23.36 to 23.50 | 0.56 | failure cap=0, without KaTeX/KaTeX, without testem/testem | yes |
| Muse Spark 1.2 (xhigh) > Kimi K2.7 Code | 0.45 | -10.65 to 12.11 | 0.53 | failure cap=0, failure cap=10, without KaTeX/KaTeX, without csstree/csstree | yes |
| Kimi K2.7 Code > GLM-5.2 (max) | 0.46 | -16.20 to 17.65 | 0.60 | net weight=0.5, net weight=0.6, without yjs/yjs | yes |
| GLM-5.2 (max) > Muse Spark 1.1 (xhigh) | 0.71 | -22.37 to 25.82 | 0.57 | failure cap=50, without testem/testem | yes |
| Muse Spark 1.1 (xhigh) > GPT-5.4 (xhigh) | 3.23 | -24.66 to 29.70 | 0.62 | without yjs/yjs | yes |
| GPT-5.4 (xhigh) > Gemini 3.1 Pro Preview (high) | 3.44 | -10.46 to 17.34 | 0.64 | without csstree/csstree, without testem/testem | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 48.6 (1) | 48.8 (1) | 48.7 (1) | 48.7 (1) | 48.5 (1) | 48.4 (1) | 48.6 (1) | 52.3 (1) | 50.8 (1) | 44.8 (1) |
| GLM-5.3 (max) | 39.7 (2) | 40.1 (2) | 40.0 (2) | 39.8 (2) | 39.5 (2) | 39.4 (2) | 39.7 (2) | 41.0 (2) | 40.5 (2) | 38.3 (2) |
| GPT-5.6 Terra (max) | 36.1 (3) | 33.9 (4) | 34.6 (4) | 35.3 (4) | 36.8 (3) | 37.5 (3) | 36.1 (3) | 40.1 (3) | 38.5 (3) | 32.0 (3) |
| Kimi K3 (max) | 35.6 (4) | 35.6 (3) | 35.6 (3) | 35.6 (3) | 35.5 (4) | 35.5 (4) | 35.6 (4) | 39.8 (4) | 38.1 (4) | 31.3 (4) |
| Qwen3.8 Max (xhigh) | 32.1 (5) | 32.9 (5) | 32.6 (5) | 32.4 (5) | 31.9 (5) | 31.6 (6) | 32.1 (5) | 36.6 (5) | 34.8 (5) | 27.7 (6) |
| Grok 4.6 (medium) | 31.9 (6) | 32.8 (6) | 32.5 (6) | 32.2 (6) | 31.7 (6) | 31.4 (7) | 31.9 (6) | 34.6 (7) | 33.5 (7) | 29.3 (5) |
| Gemini 3.5 Flash (high) | 30.9 (7) | 31.3 (7) | 31.2 (7) | 31.1 (7) | 30.8 (8) | 30.7 (8) | 30.9 (7) | 36.5 (6) | 34.3 (6) | 25.4 (8) |
| GPT-5.6 Sol (max) | 30.3 (8) | 28.0 (8) | 28.8 (8) | 29.6 (8) | 31.1 (7) | 31.9 (5) | 30.3 (8) | 33.8 (8) | 32.4 (8) | 26.9 (7) |
| DeepSeek V4 Pro (max) | 24.8 (9) | 24.3 (10) | 24.5 (9) | 24.6 (9) | 25.0 (9) | 25.1 (9) | 24.8 (9) | 29.0 (11) | 27.3 (10) | 20.5 (9) |
| Gemini 3.6 Flash (high) | 24.2 (10) | 24.4 (9) | 24.4 (10) | 24.3 (10) | 24.2 (11) | 24.1 (12) | 24.2 (10) | 29.8 (9) | 27.6 (9) | 18.6 (11) |
| Claude Sonnet 5 (max) | 24.2 (11) | 24.1 (11) | 24.1 (11) | 24.2 (11) | 24.2 (10) | 24.2 (11) | 24.2 (11) | 28.6 (12) | 26.9 (12) | 19.8 (10) |
| GPT-5.5 (xhigh) | 23.3 (12) | 21.4 (13) | 22.1 (12) | 22.7 (12) | 23.9 (12) | 24.6 (10) | 23.3 (12) | 29.6 (10) | 27.1 (11) | 17.1 (12) |
| Claude Opus 4.8 (max) | 20.8 (13) | 21.7 (12) | 21.4 (13) | 21.1 (13) | 20.5 (13) | 20.1 (13) | 20.8 (13) | 27.6 (13) | 24.9 (13) | 13.9 (13) |
| Claude Sonnet 4.6 (high) | 19.3 (14) | 20.0 (14) | 19.8 (14) | 19.5 (14) | 19.1 (14) | 18.9 (14) | 19.3 (14) | 26.4 (14) | 23.6 (14) | 12.2 (15) |
| Gemini 3.7 Flash (medium) | 19.1 (15) | 19.7 (15) | 19.5 (15) | 19.3 (15) | 18.9 (15) | 18.6 (15) | 19.1 (15) | 24.8 (15) | 22.5 (15) | 13.4 (14) |
| GPT-5.6 Luna (max) | 16.9 (16) | 15.6 (17) | 16.0 (17) | 16.5 (16) | 17.4 (16) | 17.8 (16) | 16.9 (16) | 22.1 (17) | 20.0 (17) | 11.8 (16) |
| Grok 4.5 (high) | 15.8 (17) | 16.2 (16) | 16.1 (16) | 16.0 (17) | 15.7 (17) | 15.5 (17) | 15.8 (17) | 23.3 (16) | 20.3 (16) | 8.3 (17) |
| GLM-5.3 Flash (max) | 13.1 (18) | 13.9 (18) | 13.6 (18) | 13.3 (18) | 12.8 (18) | 12.5 (18) | 13.1 (18) | 18.1 (19) | 16.1 (19) | 8.1 (18) |
| DeepSeek V4 Flash (max) | 12.5 (19) | 12.6 (19) | 12.6 (19) | 12.6 (19) | 12.5 (19) | 12.5 (19) | 12.5 (19) | 20.4 (18) | 17.3 (18) | 4.6 (20) |
| Claude Opus 5 (max) | 11.1 (20) | 11.9 (20) | 11.7 (20) | 11.4 (20) | 10.9 (20) | 10.6 (20) | 11.1 (20) | 15.5 (24) | 13.7 (22) | 6.8 (19) |
| Muse Spark 1.2 (xhigh) | 9.7 (21) | 9.9 (21) | 9.8 (21) | 9.8 (21) | 9.6 (21) | 9.5 (21) | 9.7 (21) | 15.7 (22) | 13.3 (23) | 3.6 (21) |
| Kimi K2.7 Code | 9.2 (22) | 9.2 (23) | 9.2 (23) | 9.2 (22) | 9.3 (22) | 9.3 (22) | 9.2 (22) | 18.0 (20) | 14.5 (20) | 0.5 (22) |
| GLM-5.2 (max) | 8.8 (23) | 9.5 (22) | 9.3 (22) | 9.0 (23) | 8.5 (23) | 8.3 (23) | 8.8 (23) | 17.2 (21) | 13.8 (21) | 0.3 (24) |
| Muse Spark 1.1 (xhigh) | 8.1 (24) | 8.0 (24) | 8.0 (24) | 8.0 (24) | 8.1 (24) | 8.1 (24) | 8.1 (24) | 15.7 (23) | 12.7 (24) | 0.4 (23) |
| GPT-5.4 (xhigh) | 4.8 (25) | 4.1 (25) | 4.3 (25) | 4.6 (25) | 5.1 (25) | 5.3 (25) | 4.8 (25) | 13.5 (25) | 10.0 (25) | -3.9 (25) |
| Gemini 3.1 Pro Preview (high) | 1.4 (26) | 1.2 (26) | 1.3 (26) | 1.3 (26) | 1.5 (26) | 1.5 (26) | 1.4 (26) | 9.4 (26) | 6.2 (26) | -6.7 (26) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (0 of 1108 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Fable 5 (xhigh) | 56 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14 |
| Claude Opus 4.8 (max) | 32 | 0 | none |
| Claude Opus 5 (max) | 52 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10, GLM-5.3 Flash (max) 18→19, DeepSeek V4 Flash (max) 19→18 |
| Claude Sonnet 4.6 (high) | 32 | 0 | none |
| Claude Sonnet 5 (max) | 44 | 0 | DeepSeek V4 Pro (max) 9→10, Gemini 3.6 Flash (high) 10→9, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14 |
| DeepSeek V4 Flash (max) | 28 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| DeepSeek V4 Pro (max) | 52 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5 |
| Gemini 3.1 Pro Preview (high) | 8 | 0 | none |
| Gemini 3.5 Flash (high) | 40 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, DeepSeek V4 Pro (max) 9→10, Gemini 3.6 Flash (high) 10→9, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14 |
| Gemini 3.6 Flash (high) | 44 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5 |
| Gemini 3.7 Flash (medium) | 44 | 0 | none |
| GLM-5.2 (max) | 24 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GLM-5.3 Flash (max) | 48 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GLM-5.3 (max) | 72 | 0 | Gemini 3.5 Flash (high) 7→8, GPT-5.6 Sol (max) 8→7, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.4 (xhigh) | 28 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.5 (xhigh) | 40 | 0 | Gemini 3.5 Flash (high) 7→8, GPT-5.6 Sol (max) 8→7, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.6 Luna (max) | 48 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.6 Sol (max) | 60 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.6 Terra (max) | 56 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| Grok 4.5 (high) | 32 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5 |
| Grok 4.6 (medium) | 64 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14 |
| Kimi K2.7 Code | 20 | 0 | none |
| Kimi K3 (max) | 52 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| Muse Spark 1.1 (xhigh) | 36 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| Muse Spark 1.2 (xhigh) | 44 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10, GLM-5.3 Flash (max) 18→19, DeepSeek V4 Flash (max) 19→18 |
| Qwen3.8 Max (xhigh) | 52 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| (dedup panel) | 0 | 0 | none |

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| KaTeX/KaTeX (4) | Claude Fable 5 (xhigh) 1→3, GLM-5.3 (max) 2→6, GPT-5.6 Terra (max) 3→2, Kimi K3 (max) 4→7, Qwen3.8 Max (xhigh) 5→8, Grok 4.6 (medium) 6→13, Gemini 3.5 Flash (high) 7→1, GPT-5.6 Sol (max) 8→4, DeepSeek V4 Pro (max) 9→16, Gemini 3.6 Flash (high) 10→9, Claude Sonnet 5 (max) 11→10, GPT-5.5 (xhigh) 12→5, Claude Opus 4.8 (max) 13→12, Claude Sonnet 4.6 (high) 14→11, GPT-5.6 Luna (max) 16→17, Grok 4.5 (high) 17→14, GLM-5.3 Flash (max) 18→19, DeepSeek V4 Flash (max) 19→22, Claude Opus 5 (max) 20→25, Kimi K2.7 Code 22→18, GLM-5.2 (max) 23→20, Muse Spark 1.1 (xhigh) 24→23, GPT-5.4 (xhigh) 25→24 |
| csstree/csstree (4) | GPT-5.6 Terra (max) 3→8, Grok 4.6 (medium) 6→3, Gemini 3.5 Flash (high) 7→6, GPT-5.6 Sol (max) 8→14, DeepSeek V4 Pro (max) 9→10, Gemini 3.6 Flash (high) 10→7, GPT-5.5 (xhigh) 12→17, Claude Opus 4.8 (max) 13→9, Claude Sonnet 4.6 (high) 14→12, Gemini 3.7 Flash (medium) 15→13, GPT-5.6 Luna (max) 16→22, Grok 4.5 (high) 17→15, GLM-5.3 Flash (max) 18→16, DeepSeek V4 Flash (max) 19→18, Claude Opus 5 (max) 20→19, Muse Spark 1.2 (xhigh) 21→23, Kimi K2.7 Code 22→20, GLM-5.2 (max) 23→21, GPT-5.4 (xhigh) 25→26, Gemini 3.1 Pro Preview (high) 26→25 |
| testem/testem (8) | Claude Fable 5 (xhigh) 1→3, GLM-5.3 (max) 2→1, GPT-5.6 Terra (max) 3→2, Kimi K3 (max) 4→6, Grok 4.6 (medium) 6→10, Gemini 3.5 Flash (high) 7→13, GPT-5.6 Sol (max) 8→4, DeepSeek V4 Pro (max) 9→8, Gemini 3.6 Flash (high) 10→12, Claude Sonnet 5 (max) 11→7, GPT-5.5 (xhigh) 12→9, Claude Opus 4.8 (max) 13→18, Claude Sonnet 4.6 (high) 14→21, Gemini 3.7 Flash (medium) 15→11, Grok 4.5 (high) 17→22, GLM-5.3 Flash (max) 18→23, DeepSeek V4 Flash (max) 19→20, Claude Opus 5 (max) 20→19, Muse Spark 1.2 (xhigh) 21→15, Kimi K2.7 Code 22→17, GLM-5.2 (max) 23→24, Muse Spark 1.1 (xhigh) 24→14, GPT-5.4 (xhigh) 25→26, Gemini 3.1 Pro Preview (high) 26→25 |
| yjs/yjs (4) | GLM-5.3 (max) 2→4, GPT-5.6 Terra (max) 3→5, Kimi K3 (max) 4→2, Qwen3.8 Max (xhigh) 5→7, Grok 4.6 (medium) 6→3, Gemini 3.5 Flash (high) 7→9, GPT-5.6 Sol (max) 8→6, DeepSeek V4 Pro (max) 9→8, Gemini 3.6 Flash (high) 10→13, Claude Sonnet 5 (max) 11→12, GPT-5.5 (xhigh) 12→10, Claude Opus 4.8 (max) 13→14, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→18, GPT-5.6 Luna (max) 16→11, Grok 4.5 (high) 17→19, GLM-5.3 Flash (max) 18→17, DeepSeek V4 Flash (max) 19→20, Claude Opus 5 (max) 20→16, Muse Spark 1.2 (xhigh) 21→23, Kimi K2.7 Code 22→26, GLM-5.2 (max) 23→22, GPT-5.4 (xhigh) 25→21, Gemini 3.1 Pro Preview (high) 26→25 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (20) | Solved by fewer (20) |
|---|---:|---:|
| Claude Fable 5 (xhigh) | 48.6 (1) | 48.6 (1) |
| GLM-5.3 (max) | 39.7 (2) | 39.7 (2) |
| GPT-5.6 Terra (max) | 36.1 (3) | 36.1 (3) |
| Kimi K3 (max) | 35.6 (4) | 35.6 (4) |
| Qwen3.8 Max (xhigh) | 32.1 (5) | 32.1 (5) |
| Grok 4.6 (medium) | 31.9 (6) | 31.9 (6) |
| Gemini 3.5 Flash (high) | 30.9 (7) | 30.9 (7) |
| GPT-5.6 Sol (max) | 30.3 (8) | 30.3 (8) |
| DeepSeek V4 Pro (max) | 24.8 (9) | 24.8 (9) |
| Gemini 3.6 Flash (high) | 24.2 (10) | 24.2 (10) |
| Claude Sonnet 5 (max) | 24.2 (11) | 24.2 (11) |
| GPT-5.5 (xhigh) | 23.3 (12) | 23.3 (12) |
| Claude Opus 4.8 (max) | 20.8 (13) | 20.8 (13) |
| Claude Sonnet 4.6 (high) | 19.3 (14) | 19.3 (14) |
| Gemini 3.7 Flash (medium) | 19.1 (15) | 19.1 (15) |
| GPT-5.6 Luna (max) | 16.9 (16) | 16.9 (16) |
| Grok 4.5 (high) | 15.8 (17) | 15.8 (17) |
| GLM-5.3 Flash (max) | 13.1 (18) | 13.1 (18) |
| DeepSeek V4 Flash (max) | 12.5 (19) | 12.5 (19) |
| Claude Opus 5 (max) | 11.1 (20) | 11.1 (20) |
| Muse Spark 1.2 (xhigh) | 9.7 (21) | 9.7 (21) |
| Kimi K2.7 Code | 9.2 (22) | 9.2 (22) |
| GLM-5.2 (max) | 8.8 (23) | 8.8 (23) |
| Muse Spark 1.1 (xhigh) | 8.1 (24) | 8.1 (24) |
| GPT-5.4 (xhigh) | 4.8 (25) | 4.8 (25) |
| Gemini 3.1 Pro Preview (high) | 1.4 (26) | 1.4 (26) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **Claude Fable 5 (xhigh) − GLM-5.3 (max) = 8.90**: failed/solved -13.60 (5), solved/failed 5.28 (1), solved/solved 17.22 (13). For Claude Fable 5 (xhigh): `testem-bail-on-test-failure#2` +5.28 (solved/failed), `testem-per-launcher-reports#1` +4.37 (solved/solved), `testem-per-launcher-reports#2` +3.38 (solved/solved). For GLM-5.3 (max): `csstree-shorthand-expansion-compression#2` -3.43 (failed/solved), `csstree-shorthand-expansion-compression#1` -2.85 (failed/solved), `yjs-map-conflict-detection#4` -2.76 (failed/solved).
- **GLM-5.3 (max) − GPT-5.6 Terra (max) = 3.61**: failed/failed -0.06 (1), failed/solved -3.15 (1), solved/failed 16.28 (5), solved/solved -9.45 (13). For GLM-5.3 (max): `katex-multicolumn-array-spans#1` +5.15 (solved/failed), `katex-multicolumn-array-spans#2` +3.27 (solved/failed), `testem-bail-on-test-failure#4` +3.08 (solved/failed). For GPT-5.6 Terra (max): `testem-per-launcher-reports#2` -4.08 (solved/solved), `csstree-shorthand-expansion-compression#3` -3.15 (failed/solved), `testem-per-launcher-reports#1` -2.76 (solved/solved).
- **GPT-5.6 Terra (max) − Kimi K3 (max) = 0.50**: failed/failed -0.14 (2), failed/solved -17.45 (4), solved/failed 18.06 (5), solved/solved 0.03 (9). For GPT-5.6 Terra (max): `testem-per-launcher-reports#2` +4.84 (solved/failed), `csstree-shorthand-expansion-compression#2` +4.50 (solved/failed), `katex-multicolumn-array-spans#3` +3.87 (solved/failed). For Kimi K3 (max): `katex-multicolumn-array-spans#2` -4.66 (failed/solved), `testem-bail-on-test-failure#3` -4.60 (failed/solved), `katex-multicolumn-array-spans#1` -4.22 (failed/solved).
- **Kimi K3 (max) − Qwen3.8 Max (xhigh) = 3.42**: failed/failed 0.16 (4), failed/solved -11.11 (3), solved/failed 11.78 (3), solved/solved 2.60 (10). For Kimi K3 (max): `testem-bail-on-test-failure#3` +4.45 (solved/failed), `testem-bail-on-test-failure#4` +3.97 (solved/failed), `csstree-shorthand-expansion-compression#3` +3.35 (solved/failed). For Qwen3.8 Max (xhigh): `katex-multicolumn-array-spans#3` -4.53 (failed/solved), `testem-per-launcher-reports#2` -3.44 (failed/solved), `yjs-map-conflict-detection#2` -3.13 (failed/solved).
- **Qwen3.8 Max (xhigh) − Grok 4.6 (medium) = 0.19**: failed/failed 0.03 (2), failed/solved -12.12 (5), solved/failed 7.77 (2), solved/solved 4.51 (11). For Qwen3.8 Max (xhigh): `csstree-shorthand-expansion-compression#1` +4.00 (solved/failed), `katex-multicolumn-array-spans#1` +3.77 (solved/failed), `yjs-map-conflict-detection#1` +3.09 (solved/solved). For Grok 4.6 (medium): `katex-multicolumn-array-spans#2` -3.83 (solved/solved), `testem-bail-on-test-failure#2` -3.58 (failed/solved), `testem-bail-on-test-failure#3` -3.36 (failed/solved).
- **Grok 4.6 (medium) − Gemini 3.5 Flash (high) = 1.00**: failed/failed -0.24 (3), failed/solved -4.15 (1), solved/failed 22.11 (7), solved/solved -16.72 (9). For Grok 4.6 (medium): `katex-multicolumn-array-spans#2` +5.21 (solved/failed), `katex-multicolumn-array-spans#3` +5.13 (solved/failed), `katex-multicolumn-array-spans#4` +5.05 (solved/failed). For Gemini 3.5 Flash (high): `yjs-map-conflict-detection#4` -4.78 (solved/solved), `yjs-map-conflict-detection#1` -4.56 (solved/solved), `yjs-map-conflict-detection#3` -4.22 (solved/solved).
- **Gemini 3.5 Flash (high) − GPT-5.6 Sol (max) = 0.59**: failed/failed 0.26 (2), failed/solved -24.37 (8), solved/failed 14.34 (3), solved/solved 10.35 (7). For Gemini 3.5 Flash (high): `testem-bail-on-test-failure#1` +5.10 (solved/failed), `testem-bail-on-test-failure#2` +4.86 (solved/failed), `yjs-map-conflict-detection#4` +4.56 (solved/solved). For GPT-5.6 Sol (max): `csstree-shorthand-expansion-compression#4` -5.21 (failed/solved), `csstree-shorthand-expansion-compression#3` -4.71 (failed/solved), `testem-per-launcher-reports#1` -4.50 (failed/solved).
- **GPT-5.6 Sol (max) − DeepSeek V4 Pro (max) = 5.56**: failed/failed -0.34 (4), failed/solved -1.79 (1), solved/failed 12.42 (3), solved/solved -4.73 (12). For GPT-5.6 Sol (max): `csstree-shorthand-expansion-compression#4` +5.26 (solved/failed), `testem-per-launcher-reports#1` +4.46 (solved/failed), `csstree-shorthand-expansion-compression#1` +2.70 (solved/failed). For DeepSeek V4 Pro (max): `yjs-map-conflict-detection#3` -2.43 (solved/solved), `katex-multicolumn-array-spans#4` -2.11 (solved/solved), `katex-multicolumn-array-spans#3` -1.79 (failed/solved).
- **DeepSeek V4 Pro (max) − Gemini 3.6 Flash (high) = 0.54**: failed/failed 0.11 (4), failed/solved -12.43 (3), solved/failed 16.48 (5), solved/solved -3.61 (8). For DeepSeek V4 Pro (max): `testem-per-launcher-reports#3` +5.05 (solved/failed), `testem-per-launcher-reports#4` +4.09 (solved/solved), `csstree-shorthand-expansion-compression#3` +3.58 (solved/failed). For Gemini 3.6 Flash (high): `testem-bail-on-test-failure#3` -4.46 (failed/solved), `testem-bail-on-test-failure#1` -4.19 (failed/solved), `testem-bail-on-test-failure#2` -3.78 (failed/solved).
- **Gemini 3.6 Flash (high) − Claude Sonnet 5 (max) = 0.05**: failed/failed -0.22 (3), failed/solved -11.94 (6), solved/failed 17.67 (6), solved/solved -5.45 (5). For Gemini 3.6 Flash (high): `testem-bail-on-test-failure#3` +4.47 (solved/failed), `testem-bail-on-test-failure#1` +4.02 (solved/failed), `yjs-map-conflict-detection#3` +3.00 (solved/failed). For Claude Sonnet 5 (max): `katex-multicolumn-array-spans#2` -3.08 (failed/solved), `testem-per-launcher-reports#3` -2.52 (failed/solved), `csstree-shorthand-expansion-compression#2` -2.10 (failed/solved).
- **Claude Sonnet 5 (max) − GPT-5.5 (xhigh) = 0.88**: failed/failed 0.47 (5), failed/solved -11.66 (4), solved/failed 17.17 (5), solved/solved -5.11 (6). For Claude Sonnet 5 (max): `testem-bail-on-test-failure#2` +5.62 (solved/failed), `yjs-map-conflict-detection#2` +4.72 (solved/failed), `katex-multicolumn-array-spans#2` +3.04 (solved/failed). For GPT-5.5 (xhigh): `csstree-shorthand-expansion-compression#1` -4.80 (solved/solved), `testem-per-launcher-reports#1` -4.79 (failed/solved), `yjs-map-conflict-detection#3` -3.79 (failed/solved).
- **GPT-5.5 (xhigh) − Claude Opus 4.8 (max) = 2.55**: failed/failed -0.48 (8), failed/solved -8.32 (2), solved/failed 16.66 (4), solved/solved -5.31 (6). For GPT-5.5 (xhigh): `csstree-shorthand-expansion-compression#1` +5.55 (solved/failed), `csstree-shorthand-expansion-compression#4` +5.09 (solved/failed), `yjs-map-conflict-detection#4` +4.82 (solved/failed). For Claude Opus 4.8 (max): `yjs-map-conflict-detection#2` -4.94 (failed/solved), `testem-per-launcher-reports#4` -3.55 (solved/solved), `katex-multicolumn-array-spans#1` -3.37 (failed/solved).
- **Claude Opus 4.8 (max) − Claude Sonnet 4.6 (high) = 1.45**: failed/failed 0.20 (10), failed/solved -3.28 (2), solved/failed 7.75 (2), solved/solved -3.23 (6). For Claude Opus 4.8 (max): `yjs-map-conflict-detection#3` +4.55 (solved/failed), `katex-multicolumn-array-spans#1` +3.21 (solved/failed), `testem-per-launcher-reports#1` +1.19 (solved/solved). For Claude Sonnet 4.6 (high): `yjs-map-conflict-detection#4` -2.45 (failed/solved), `yjs-map-conflict-detection#1` -1.79 (solved/solved), `testem-per-launcher-reports#3` -1.72 (solved/solved).
- **Claude Sonnet 4.6 (high) − Gemini 3.7 Flash (medium) = 0.24**: failed/failed 0.27 (8), failed/solved -12.59 (4), solved/failed 0.95 (1), solved/solved 11.61 (7). For Claude Sonnet 4.6 (high): `testem-per-launcher-reports#3` +3.73 (solved/solved), `testem-per-launcher-reports#4` +3.48 (solved/solved), `testem-per-launcher-reports#2` +1.60 (solved/solved). For Gemini 3.7 Flash (medium): `yjs-map-conflict-detection#3` -4.38 (failed/solved), `katex-multicolumn-array-spans#2` -4.29 (failed/solved), `testem-bail-on-test-failure#2` -2.22 (failed/solved).
- **Gemini 3.7 Flash (medium) − GPT-5.6 Luna (max) = 2.17**: failed/failed 0.03 (6), failed/solved -9.16 (3), solved/failed 7.11 (2), solved/solved 4.20 (9). For Gemini 3.7 Flash (medium): `katex-multicolumn-array-spans#2` +4.47 (solved/failed), `yjs-map-conflict-detection#1` +3.26 (solved/solved), `yjs-map-conflict-detection#2` +3.04 (solved/solved). For GPT-5.6 Luna (max): `csstree-shorthand-expansion-compression#1` -4.67 (failed/solved), `katex-multicolumn-array-spans#1` -2.90 (failed/solved), `csstree-shorthand-expansion-compression#4` -2.70 (solved/solved).
- **GPT-5.6 Luna (max) − Grok 4.5 (high) = 1.09**: failed/failed -0.22 (7), failed/solved -3.96 (1), solved/failed 12.17 (5), solved/solved -6.90 (7). For GPT-5.6 Luna (max): `csstree-shorthand-expansion-compression#1` +4.70 (solved/failed), `katex-multicolumn-array-spans#1` +2.96 (solved/failed), `csstree-shorthand-expansion-compression#4` +2.85 (solved/solved). For Grok 4.5 (high): `testem-per-launcher-reports#1` -3.96 (failed/solved), `yjs-map-conflict-detection#1` -3.04 (solved/solved), `yjs-map-conflict-detection#2` -2.31 (solved/solved).
- **Grok 4.5 (high) − GLM-5.3 Flash (max) = 2.76**: failed/failed -0.14 (7), failed/solved -11.95 (5), solved/failed 1.48 (1), solved/solved 13.37 (7). For Grok 4.5 (high): `yjs-map-conflict-detection#2` +3.19 (solved/solved), `yjs-map-conflict-detection#1` +2.82 (solved/solved), `testem-per-launcher-reports#3` +2.00 (solved/solved). For GLM-5.3 Flash (max): `yjs-map-conflict-detection#4` -3.23 (failed/solved), `testem-bail-on-test-failure#1` -2.70 (failed/solved), `katex-multicolumn-array-spans#2` -2.17 (failed/solved).
- **GLM-5.3 Flash (max) − DeepSeek V4 Flash (max) = 0.52**: failed/failed -0.15 (7), failed/solved -3.71 (1), solved/failed 12.34 (6), solved/solved -7.97 (6). For GLM-5.3 Flash (max): `testem-bail-on-test-failure#1` +2.68 (solved/failed), `testem-per-launcher-reports#2` +2.55 (solved/failed), `testem-per-launcher-reports#1` +2.04 (solved/failed). For DeepSeek V4 Flash (max): `yjs-map-conflict-detection#2` -3.81 (solved/solved), `katex-multicolumn-array-spans#4` -3.71 (failed/solved), `testem-per-launcher-reports#4` -3.08 (solved/solved).
- **DeepSeek V4 Flash (max) − Claude Opus 5 (max) = 1.40**: failed/failed 0.10 (7), failed/solved -10.93 (6), solved/solved 12.23 (7). For DeepSeek V4 Flash (max): `yjs-map-conflict-detection#2` +4.04 (solved/solved), `testem-per-launcher-reports#3` +3.96 (solved/solved), `testem-per-launcher-reports#4` +3.14 (solved/solved). For Claude Opus 5 (max): `katex-multicolumn-array-spans#1` -3.97 (failed/solved), `testem-bail-on-test-failure#3` -1.78 (failed/solved), `yjs-map-conflict-detection#1` -1.49 (failed/solved).
- **Claude Opus 5 (max) − Muse Spark 1.2 (xhigh) = 1.46**: failed/failed -0.10 (5), failed/solved -4.41 (2), solved/failed 10.06 (4), solved/solved -4.09 (9). For Claude Opus 5 (max): `katex-multicolumn-array-spans#1` +4.10 (solved/failed), `katex-multicolumn-array-spans#4` +2.50 (solved/failed), `testem-bail-on-test-failure#3` +2.02 (solved/failed). For Muse Spark 1.2 (xhigh): `csstree-shorthand-expansion-compression#3` -3.74 (failed/solved), `yjs-map-conflict-detection#3` -3.49 (solved/solved), `yjs-map-conflict-detection#2` -1.84 (solved/solved).
- **Muse Spark 1.2 (xhigh) − Kimi K2.7 Code = 0.45**: failed/failed -0.86 (9), solved/failed 8.58 (6), solved/solved -7.28 (5). For Muse Spark 1.2 (xhigh): `csstree-shorthand-expansion-compression#3` +3.74 (solved/failed), `testem-per-launcher-reports#3` +1.83 (solved/failed), `katex-multicolumn-array-spans#2` +1.08 (solved/failed). For Kimi K2.7 Code: `testem-per-launcher-reports#2` -3.02 (solved/solved), `yjs-map-conflict-detection#2` -1.85 (solved/solved), `yjs-map-conflict-detection#3` -1.07 (solved/solved).
- **Kimi K2.7 Code − GLM-5.2 (max) = 0.46**: failed/failed 0.04 (13), failed/solved -4.99 (2), solved/failed 4.27 (1), solved/solved 1.14 (4). For Kimi K2.7 Code: `yjs-map-conflict-detection#4` +4.27 (solved/failed), `yjs-map-conflict-detection#3` +2.13 (solved/solved), `yjs-map-conflict-detection#2` +1.44 (solved/solved). For GLM-5.2 (max): `testem-per-launcher-reports#4` -3.94 (failed/solved), `yjs-map-conflict-detection#1` -1.96 (solved/solved), `testem-per-launcher-reports#1` -1.05 (failed/solved).
- **GLM-5.2 (max) − Muse Spark 1.1 (xhigh) = 0.71**: failed/failed 1.09 (9), failed/solved -13.29 (5), solved/failed 8.41 (2), solved/solved 4.50 (4). For GLM-5.2 (max): `testem-per-launcher-reports#2` +4.37 (solved/failed), `testem-per-launcher-reports#4` +4.03 (solved/failed), `yjs-map-conflict-detection#1` +2.30 (solved/solved). For Muse Spark 1.1 (xhigh): `yjs-map-conflict-detection#4` -4.38 (failed/solved), `csstree-shorthand-expansion-compression#2` -4.22 (failed/solved), `csstree-shorthand-expansion-compression#4` -3.07 (failed/solved).
- **Muse Spark 1.1 (xhigh) − GPT-5.4 (xhigh) = 3.23**: failed/failed -0.16 (6), failed/solved -15.09 (5), solved/failed 19.48 (7), solved/solved -1.00 (2). For Muse Spark 1.1 (xhigh): `yjs-map-conflict-detection#4` +4.30 (solved/failed), `csstree-shorthand-expansion-compression#2` +4.21 (solved/failed), `yjs-map-conflict-detection#3` +3.38 (solved/failed). For GPT-5.4 (xhigh): `csstree-shorthand-expansion-compression#1` -5.40 (failed/solved), `testem-per-launcher-reports#4` -4.50 (failed/solved), `testem-per-launcher-reports#2` -2.47 (failed/solved).
- **GPT-5.4 (xhigh) − Gemini 3.1 Pro Preview (high) = 3.44**: failed/failed -2.75 (12), failed/solved -5.57 (1), solved/failed 12.36 (6), solved/solved -0.61 (1). For GPT-5.4 (xhigh): `csstree-shorthand-expansion-compression#1` +5.17 (solved/failed), `testem-per-launcher-reports#2` +2.43 (solved/failed), `yjs-map-conflict-detection#2` +1.55 (solved/failed). For Gemini 3.1 Pro Preview (high): `yjs-map-conflict-detection#3` -5.57 (failed/solved), `testem-per-launcher-reports#4` -0.61 (solved/solved), `csstree-shorthand-expansion-compression#2` -0.30 (failed/failed).

## Regenerate

```sh
python -m parsimony.stability examples/deepswe-javascript/score-panel.json examples/deepswe-javascript/*.jsonl --output examples/deepswe-javascript/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
