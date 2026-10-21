# Score sensitivity: 38 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `deepswe-v1.1-javascript-26-pooled-80-20-v0.7`: 20 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (13 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Fable 5 (xhigh) ≈ GLM-5.3 (max) ≈ GPT-5.6 Terra (max) ≈ Kimi K3 (max) ≈ Qwen3.8 Max (xhigh) ≈ Grok 4.6 (medium) ≈ Gemini 3.5 Flash (high) ≈ GPT-5.6 Sol (max) ≈ DeepSeek V4 Pro (max) ≈ Gemini 3.6 Flash (high) ≈ Claude Sonnet 5 (max) ≈ GPT-5.5 (xhigh) ≈ Claude Opus 4.8 (max) ≈ Claude Sonnet 4.6 (high) ≈ Gemini 3.7 Flash (medium) ≈ GPT-5.6 Luna (max) ≈ Grok 4.5 (high) ≈ Claude Opus 4.7 (max) · DeepSWE 1.0 ≈ GLM-5.3 Flash (max) ≈ DeepSeek V4 Flash (max) ≈ Claude Opus 5 (max) ≈ Muse Spark 1.2 (xhigh) ≈ Kimi K2.7 Code ≈ GLM-5.2 (max) ≈ Muse Spark 1.1 (xhigh) ≈ GPT-5.4 (xhigh) ≈ GPT-5.4 mini (xhigh) · DeepSWE 1.0 ≈ Kimi K2.6 · DeepSWE 1.0 ≈ GLM-5.1 · DeepSWE 1.0 ≈ Gemini 3.1 Pro Preview (high) ≈ MiniMax M3 · DeepSWE 1.0 ≈ Grok Build 0.1 · DeepSWE 1.0 ≈ Claude Opus 4.6 (max) · DeepSWE 1.0 ≈ MiMo V2.5 Pro · DeepSWE 1.0 ≈ Claude Haiku 4.5 · DeepSWE 1.0 ≈ Gemini 3 Flash Preview · DeepSWE 1.0 ≈ MiniMax M2.7 · DeepSWE 1.0 ≈ Qwen3.6 Plus · DeepSWE 1.0 (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (0 of 37 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 37 pairs): Claude Fable 5 (xhigh) vs GLM-5.3 (max), GLM-5.3 (max) vs GPT-5.6 Terra (max), GPT-5.6 Terra (max) vs Kimi K3 (max), Kimi K3 (max) vs Qwen3.8 Max (xhigh), Qwen3.8 Max (xhigh) vs Grok 4.6 (medium), Grok 4.6 (medium) vs Gemini 3.5 Flash (high), Gemini 3.5 Flash (high) vs GPT-5.6 Sol (max), GPT-5.6 Sol (max) vs DeepSeek V4 Pro (max), DeepSeek V4 Pro (max) vs Gemini 3.6 Flash (high), Gemini 3.6 Flash (high) vs Claude Sonnet 5 (max), Claude Sonnet 5 (max) vs GPT-5.5 (xhigh), GPT-5.5 (xhigh) vs Claude Opus 4.8 (max), Claude Opus 4.8 (max) vs Claude Sonnet 4.6 (high), Claude Sonnet 4.6 (high) vs Gemini 3.7 Flash (medium), Gemini 3.7 Flash (medium) vs GPT-5.6 Luna (max), GPT-5.6 Luna (max) vs Grok 4.5 (high), Grok 4.5 (high) vs Claude Opus 4.7 (max) · DeepSWE 1.0, Claude Opus 4.7 (max) · DeepSWE 1.0 vs GLM-5.3 Flash (max), GLM-5.3 Flash (max) vs DeepSeek V4 Flash (max), DeepSeek V4 Flash (max) vs Claude Opus 5 (max), Claude Opus 5 (max) vs Muse Spark 1.2 (xhigh), Muse Spark 1.2 (xhigh) vs Kimi K2.7 Code, Kimi K2.7 Code vs GLM-5.2 (max), GLM-5.2 (max) vs Muse Spark 1.1 (xhigh), Muse Spark 1.1 (xhigh) vs GPT-5.4 (xhigh), GPT-5.4 (xhigh) vs GPT-5.4 mini (xhigh) · DeepSWE 1.0, GPT-5.4 mini (xhigh) · DeepSWE 1.0 vs Kimi K2.6 · DeepSWE 1.0, Kimi K2.6 · DeepSWE 1.0 vs GLM-5.1 · DeepSWE 1.0, GLM-5.1 · DeepSWE 1.0 vs Gemini 3.1 Pro Preview (high), Gemini 3.1 Pro Preview (high) vs MiniMax M3 · DeepSWE 1.0, MiniMax M3 · DeepSWE 1.0 vs Grok Build 0.1 · DeepSWE 1.0, Grok Build 0.1 · DeepSWE 1.0 vs Claude Opus 4.6 (max) · DeepSWE 1.0, Claude Opus 4.6 (max) · DeepSWE 1.0 vs MiMo V2.5 Pro · DeepSWE 1.0, MiMo V2.5 Pro · DeepSWE 1.0 vs Claude Haiku 4.5 · DeepSWE 1.0, Claude Haiku 4.5 · DeepSWE 1.0 vs Gemini 3 Flash Preview · DeepSWE 1.0, Gemini 3 Flash Preview · DeepSWE 1.0 vs MiniMax M2.7 · DeepSWE 1.0, MiniMax M2.7 · DeepSWE 1.0 vs Qwen3.6 Plus · DeepSWE 1.0.
- **Midpoint rank never changes under any variation**: none.

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 20 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Fable 5 (xhigh) | 48.6 | 15.3–76.9 | 48.6 | 1–3 | 1.0–18.0 | 0.51 |
| 2 | GLM-5.3 (max) | 39.7 | 22.7–58.6 | 39.7 | 1–6 | 1.0–16.0 | 0.13 |
| 3 | GPT-5.6 Terra (max) | 36.1 | 9.0–62.2 | 36.1 | 2–8 | 1.0–15.0 | 0.24 |
| 4 | Kimi K3 (max) | 35.6 | 21.4–49.7 | 35.6 | 2–7 | 3.0–19.0 | 0.00 |
| 5 | Qwen3.8 Max (xhigh) | 32.1 | 4.5–57.7 | 32.1 | 5–8 | 2.0–17.0 | 0.00 |
| 6 | Grok 4.6 (medium) | 31.9 | 10.4–53.4 | 31.9 | 3–13 | 2.0–26.0 | 0.00 |
| 7 | Gemini 3.5 Flash (high) | 30.9 | 4.6–55.8 | 30.9 | 1–13 | 1.0–21.0 | 0.11 |
| 8 | GPT-5.6 Sol (max) | 30.3 | 5.4–55.3 | 30.3 | 4–15 | 2.0–26.0 | 0.00 |
| 9 | DeepSeek V4 Pro (max) | 24.8 | 4.1–43.8 | 24.8 | 8–16 | 6.0–23.0 | 0.00 |
| 10 | Gemini 3.6 Flash (high) | 24.2 | -1.4–49.8 | 24.2 | 7–13 | 2.0–28.0 | 0.01 |
| 11 | Claude Sonnet 5 (max) | 24.2 | 12.3–43.9 | 24.2 | 7–12 | 4.0–19.0 | 0.00 |
| 12 | GPT-5.5 (xhigh) | 23.3 | -0.2–46.1 | 23.3 | 5–18 | 3.0–22.0 | 0.00 |
| 13 | Claude Opus 4.8 (max) | 20.8 | -8.3–49.8 | 20.8 | 9–19 | 4.0–24.0 | 0.00 |
| 14 | Claude Sonnet 4.6 (high) | 19.3 | -10.5–53.0 | 19.3 | 11–24 | 2.0–30.0 | 0.01 |
| 15 | Gemini 3.7 Flash (medium) | 19.1 | -0.3–41.9 | 19.1 | 11–18 | 6.0–20.0 | 0.00 |
| 16 | GPT-5.6 Luna (max) | 16.9 | 4.9–29.1 | 16.9 | 11–23 | 6.0–26.0 | 0.00 |
| 17 | Grok 4.5 (high) | 15.8 | -10.9–43.7 | 15.8 | 14–25 | 7.0–32.0 | 0.00 |
| 18 | Claude Opus 4.7 (max) · DeepSWE 1.0 | 15.5 | -7.5–39.7 | 15.5 | 14–22 | 9.0–26.024999999999864 | 0.00 |
| 19 | GLM-5.3 Flash (max) | 13.1 | -0.1–26.6 | 13.1 | 17–26 | 9.0–26.0 | 0.00 |
| 20 | DeepSeek V4 Flash (max) | 12.5 | -7.1–32.1 | 12.5 | 19–23 | 13.0–28.0 | 0.00 |
| 21 | Claude Opus 5 (max) | 11.1 | -2.6–23.4 | 11.1 | 16–28 | 9.0–31.0 | 0.00 |
| 22 | Muse Spark 1.2 (xhigh) | 9.7 | -5.6–31.2 | 9.7 | 16–25 | 11.0–28.0 | 0.00 |
| 23 | Kimi K2.7 Code | 9.2 | -12.0–39.5 | 9.2 | 18–31 | 7.0–36.0 | 0.00 |
| 24 | GLM-5.2 (max) | 8.8 | -12.2–31.0 | 8.8 | 21–27 | 16.975–37.0 | 0.00 |
| 25 | Muse Spark 1.1 (xhigh) | 8.1 | -9.8–30.0 | 8.1 | 15–29 | 8.0–33.0 | 0.00 |
| 26 | GPT-5.4 (xhigh) | 4.8 | -9.2–22.2 | 4.8 | 21–31 | 13.0–36.0 | 0.00 |
| 27 | GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 4.6 | -11.9–30.1 | 4.6 | 22–33 | 14.0–35.024999999999864 | 0.00 |
| 28 | Kimi K2.6 · DeepSWE 1.0 | 4.3 | -11.4–35.0 | 4.3 | 20–38 | 11.0–38.0 | 0.00 |
| 29 | GLM-5.1 · DeepSWE 1.0 | 2.2 | -12.2–19.8 | 2.2 | 24–32 | 21.0–36.0 | 0.00 |
| 30 | Gemini 3.1 Pro Preview (high) | 1.4 | -9.1–12.7 | 1.4 | 27–31 | 24.0–30.0 | 0.00 |
| 31 | MiniMax M3 · DeepSWE 1.0 | 1.1 | -12.2–20.8 | -1.4–3.5 | 28–31 | 26.0–36.0 | 0.00 |
| 32 | Grok Build 0.1 · DeepSWE 1.0 | -1.6 | -11.2–7.8 | -2.2–-1.0 | 29–33 | 27.0–33.0 | 0.00 |
| 33 | Claude Opus 4.6 (max) · DeepSWE 1.0 | -2.3 | -9.9–5.6 | -2.3 | 28–34 | 24.0–34.0 | 0.00 |
| 34 | MiMo V2.5 Pro · DeepSWE 1.0 | -6.5 | -11.0–2.1 | -6.5 | 33–37 | 32.0–38.0 | 0.00 |
| 35 | Claude Haiku 4.5 · DeepSWE 1.0 | -8.1 | -9.5–-7.1 | -8.1 | 32–36 | 21.0–36.0 | 0.00 |
| 36 | Gemini 3 Flash Preview · DeepSWE 1.0 | -8.7 | -15.1–-4.9 | -11.2–-6.2 | 34–36 | 25.0–36.0 | 0.00 |
| 37 | MiniMax M2.7 · DeepSWE 1.0 | -10.5 | -12.3–-8.4 | -11.1–-9.9 | 35–38 | 28.0–38.0 | 0.00 |
| 38 | Qwen3.6 Plus · DeepSWE 1.0 | -10.6 | -13.2–-9.0 | -11.2–-10.0 | 36–38 | 27.0–38.0 | 0.00 |

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
| Claude Opus 4.8 (max) > Claude Sonnet 4.6 (high) | 1.45 | -3.39 to 9.18 | 0.66 | without KaTeX/KaTeX | yes |
| Claude Sonnet 4.6 (high) > Gemini 3.7 Flash (medium) | 0.24 | -15.42 to 24.36 | 0.51 | failure cap=50, panel without Claude Fable 5 (xhigh), panel without Claude Sonnet 5 (max), panel without Gemini 3.5 Flash (high), panel without Grok 4.6 (medium), without testem/testem | yes |
| Gemini 3.7 Flash (medium) > GPT-5.6 Luna (max) | 2.17 | -21.44 to 25.42 | 0.60 | without yjs/yjs | yes |
| GPT-5.6 Luna (max) > Grok 4.5 (high) | 1.09 | -21.68 to 23.43 | 0.57 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, without KaTeX/KaTeX, without csstree/csstree | yes |
| Grok 4.5 (high) > Claude Opus 4.7 (max) · DeepSWE 1.0 | 0.27 | -15.19 to 18.09 | 0.54 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=50, panel without Gemini 3.5 Flash (high), panel without GLM-5.3 (max), panel without Grok 4.5 (high), panel without Grok 4.6 (medium), without csstree/csstree, without testem/testem | yes |
| Claude Opus 4.7 (max) · DeepSWE 1.0 > GLM-5.3 Flash (max) | 2.49 | -12.91 to 20.22 | 0.60 | without yjs/yjs | yes |
| GLM-5.3 Flash (max) > DeepSeek V4 Flash (max) | 0.52 | -6.87 to 11.36 | 0.51 | failure cap=0, failure cap=10, panel without Claude Opus 5 (max), panel without Muse Spark 1.2 (xhigh), without testem/testem | yes |
| DeepSeek V4 Flash (max) > Claude Opus 5 (max) | 1.40 | -13.39 to 17.35 | 0.59 | failure cap=50, without testem/testem, without yjs/yjs | yes |
| Claude Opus 5 (max) > Muse Spark 1.2 (xhigh) | 1.46 | -22.13 to 23.50 | 0.56 | failure cap=0, without KaTeX/KaTeX, without testem/testem | yes |
| Muse Spark 1.2 (xhigh) > Kimi K2.7 Code | 0.45 | -10.65 to 12.11 | 0.53 | failure cap=0, failure cap=10, without KaTeX/KaTeX, without csstree/csstree | yes |
| Kimi K2.7 Code > GLM-5.2 (max) | 0.46 | -16.20 to 17.65 | 0.60 | net weight=0.5, net weight=0.6, without yjs/yjs | yes |
| GLM-5.2 (max) > Muse Spark 1.1 (xhigh) | 0.71 | -22.37 to 25.82 | 0.57 | failure cap=50, without testem/testem | yes |
| Muse Spark 1.1 (xhigh) > GPT-5.4 (xhigh) | 3.23 | -24.66 to 29.72 | 0.62 | without yjs/yjs | yes |
| GPT-5.4 (xhigh) > GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 0.26 | -30.63 to 26.19 | 0.55 | net weight=0.5, panel without Gemini 3.5 Flash (high), panel without Gemini 3.7 Flash (medium), without csstree/csstree, without testem/testem | yes |
| GPT-5.4 mini (xhigh) · DeepSWE 1.0 > Kimi K2.6 · DeepSWE 1.0 | 0.24 | -4.99 to 6.66 | 0.56 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, panel without Claude Opus 5 (max), without testem/testem | yes |
| Kimi K2.6 · DeepSWE 1.0 > GLM-5.1 · DeepSWE 1.0 | 2.11 | -25.45 to 30.88 | 0.62 | without yjs/yjs | yes |
| GLM-5.1 · DeepSWE 1.0 > Gemini 3.1 Pro Preview (high) | 0.84 | -4.86 to 9.53 | 0.61 | failure cap=50, without testem/testem | yes |
| Gemini 3.1 Pro Preview (high) > MiniMax M3 · DeepSWE 1.0 | 0.34 | -12.05 to 4.40 | 0.33 | net weight=0.5, net weight=0.6, net weight=0.7, without KaTeX/KaTeX, without csstree/csstree, without testem/testem | no |
| MiniMax M3 · DeepSWE 1.0 > Grok Build 0.1 · DeepSWE 1.0 | 2.67 | -3.45 to 15.79 | 0.40 | without yjs/yjs | no |
| Grok Build 0.1 · DeepSWE 1.0 > Claude Opus 4.6 (max) · DeepSWE 1.0 | 0.68 | -4.90 to 6.47 | 0.50 | without csstree/csstree, without yjs/yjs | yes |
| Claude Opus 4.6 (max) · DeepSWE 1.0 > MiMo V2.5 Pro · DeepSWE 1.0 | 4.20 | -3.01 to 13.36 | 0.81 | without testem/testem | yes |
| MiMo V2.5 Pro · DeepSWE 1.0 > Claude Haiku 4.5 · DeepSWE 1.0 | 1.66 | -3.20 to 9.32 | 0.67 | failure cap=50, without yjs/yjs | yes |
| Claude Haiku 4.5 · DeepSWE 1.0 > Gemini 3 Flash Preview · DeepSWE 1.0 | 0.52 | -3.95 to 5.85 | 0.01 | failure cap=0, without testem/testem | no |
| Gemini 3 Flash Preview · DeepSWE 1.0 > MiniMax M2.7 · DeepSWE 1.0 | 1.84 | -5.36 to 6.51 | 0.30 | failure cap=0 | no |
| MiniMax M2.7 · DeepSWE 1.0 > Qwen3.6 Plus · DeepSWE 1.0 | 0.10 | -3.18 to 2.13 | 0.12 | failure cap=0, without KaTeX/KaTeX | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

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
| GPT-5.6 Luna (max) | 16.9 (16) | 15.6 (18) | 16.0 (18) | 16.5 (16) | 17.4 (16) | 17.8 (16) | 16.9 (16) | 22.1 (17) | 20.0 (17) | 11.8 (16) |
| Grok 4.5 (high) | 15.8 (17) | 16.2 (17) | 16.1 (17) | 16.0 (18) | 15.7 (17) | 15.5 (17) | 15.8 (17) | 23.3 (16) | 20.3 (16) | 8.3 (18) |
| Claude Opus 4.7 (max) · DeepSWE 1.0 | 15.5 (18) | 17.7 (16) | 17.0 (16) | 16.3 (17) | 14.8 (18) | 14.1 (18) | 15.5 (18) | 21.8 (18) | 19.3 (18) | 9.3 (17) |
| GLM-5.3 Flash (max) | 13.1 (19) | 13.9 (19) | 13.6 (19) | 13.3 (19) | 12.8 (19) | 12.5 (19) | 13.1 (19) | 18.1 (20) | 16.1 (20) | 8.1 (19) |
| DeepSeek V4 Flash (max) | 12.5 (20) | 12.6 (20) | 12.6 (20) | 12.6 (20) | 12.5 (20) | 12.5 (20) | 12.5 (20) | 20.4 (19) | 17.3 (19) | 4.6 (21) |
| Claude Opus 5 (max) | 11.1 (21) | 11.9 (21) | 11.7 (21) | 11.4 (21) | 10.9 (21) | 10.6 (21) | 11.1 (21) | 15.5 (25) | 13.7 (23) | 6.8 (20) |
| Muse Spark 1.2 (xhigh) | 9.7 (22) | 9.9 (22) | 9.8 (22) | 9.8 (22) | 9.6 (22) | 9.5 (22) | 9.7 (22) | 15.7 (23) | 13.3 (24) | 3.6 (22) |
| Kimi K2.7 Code | 9.2 (23) | 9.2 (24) | 9.2 (24) | 9.2 (23) | 9.3 (23) | 9.3 (23) | 9.2 (23) | 18.0 (21) | 14.5 (21) | 0.5 (23) |
| GLM-5.2 (max) | 8.8 (24) | 9.5 (23) | 9.3 (23) | 9.0 (24) | 8.5 (24) | 8.3 (24) | 8.8 (24) | 17.2 (22) | 13.8 (22) | 0.3 (25) |
| Muse Spark 1.1 (xhigh) | 8.1 (25) | 8.0 (25) | 8.0 (25) | 8.0 (25) | 8.1 (25) | 8.1 (25) | 8.1 (25) | 15.7 (24) | 12.7 (25) | 0.4 (24) |
| GPT-5.4 (xhigh) | 4.8 (26) | 4.1 (28) | 4.3 (26) | 4.6 (26) | 5.1 (26) | 5.3 (26) | 4.8 (26) | 13.5 (27) | 10.0 (26) | -3.9 (26) |
| GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 4.6 (27) | 4.1 (27) | 4.2 (28) | 4.4 (27) | 4.7 (27) | 4.9 (27) | 4.6 (27) | 13.4 (28) | 9.9 (28) | -4.2 (27) |
| Kimi K2.6 · DeepSWE 1.0 | 4.3 (28) | 4.3 (26) | 4.3 (27) | 4.3 (28) | 4.4 (28) | 4.4 (28) | 4.3 (28) | 13.7 (26) | 10.0 (27) | -5.0 (28) |
| GLM-5.1 · DeepSWE 1.0 | 2.2 (29) | 2.5 (29) | 2.4 (29) | 2.3 (29) | 2.1 (29) | 2.0 (29) | 2.2 (29) | 11.9 (29) | 8.0 (29) | -7.5 (31) |
| Gemini 3.1 Pro Preview (high) | 1.4 (30) | 1.2 (31) | 1.3 (31) | 1.3 (31) | 1.5 (30) | 1.5 (30) | 1.4 (30) | 9.4 (30) | 6.2 (30) | -6.7 (29) |
| MiniMax M3 · DeepSWE 1.0 | 1.1 (31) | 2.0 (30) | 1.7 (30) | 1.4 (30) | 0.7 (31) | 0.4 (31) | 1.1 (31) | 9.4 (31) | 6.1 (31) | -7.3 (30) |
| Grok Build 0.1 · DeepSWE 1.0 | -1.6 (32) | -1.2 (32) | -1.3 (32) | -1.5 (32) | -1.7 (32) | -1.9 (32) | -1.6 (32) | 6.9 (32) | 3.5 (32) | -10.1 (32) |
| Claude Opus 4.6 (max) · DeepSWE 1.0 | -2.3 (33) | -1.6 (33) | -1.8 (33) | -2.1 (33) | -2.5 (33) | -2.8 (33) | -2.3 (33) | 6.6 (33) | 3.1 (33) | -11.2 (33) |
| MiMo V2.5 Pro · DeepSWE 1.0 | -6.5 (34) | -6.5 (34) | -6.5 (34) | -6.5 (34) | -6.5 (34) | -6.5 (34) | -6.5 (34) | 3.5 (34) | -0.5 (34) | -16.5 (35) |
| Claude Haiku 4.5 · DeepSWE 1.0 | -8.1 (35) | -8.2 (35) | -8.2 (35) | -8.2 (35) | -8.1 (35) | -8.1 (35) | -8.1 (35) | 0.0 (35) | -3.3 (35) | -16.3 (34) |
| Gemini 3 Flash Preview · DeepSWE 1.0 | -8.7 (36) | -8.8 (36) | -8.7 (36) | -8.7 (36) | -8.6 (36) | -8.6 (36) | -8.7 (36) | 0.0 (36) | -3.5 (36) | -17.3 (36) |
| MiniMax M2.7 · DeepSWE 1.0 | -10.5 (37) | -10.6 (37) | -10.6 (37) | -10.5 (37) | -10.5 (37) | -10.4 (37) | -10.5 (37) | 0.0 (37) | -4.2 (37) | -21.0 (37) |
| Qwen3.6 Plus · DeepSWE 1.0 | -10.6 (38) | -10.7 (38) | -10.6 (38) | -10.6 (38) | -10.6 (38) | -10.6 (38) | -10.6 (38) | 0.0 (38) | -4.2 (38) | -21.2 (38) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (0 of 1108 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Fable 5 (xhigh) | 56 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14 |
| Claude Opus 4.8 (max) | 32 | 0 | none |
| Claude Opus 5 (max) | 52 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10, GLM-5.3 Flash (max) 19→20, DeepSeek V4 Flash (max) 20→19, GPT-5.4 mini (xhigh) · DeepSWE 1.0 27→28, Kimi K2.6 · DeepSWE 1.0 28→27 |
| Claude Sonnet 4.6 (high) | 32 | 0 | none |
| Claude Sonnet 5 (max) | 44 | 0 | DeepSeek V4 Pro (max) 9→10, Gemini 3.6 Flash (high) 10→9, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14 |
| DeepSeek V4 Flash (max) | 28 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| DeepSeek V4 Pro (max) | 52 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5 |
| Gemini 3.1 Pro Preview (high) | 8 | 0 | none |
| Gemini 3.5 Flash (high) | 40 | 0 | GPT-5.6 Terra (max) 3→4, Kimi K3 (max) 4→3, Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, DeepSeek V4 Pro (max) 9→10, Gemini 3.6 Flash (high) 10→9, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14, Grok 4.5 (high) 17→18, Claude Opus 4.7 (max) · DeepSWE 1.0 18→17, GPT-5.4 (xhigh) 26→27, GPT-5.4 mini (xhigh) · DeepSWE 1.0 27→26 |
| Gemini 3.6 Flash (high) | 44 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5 |
| Gemini 3.7 Flash (medium) | 44 | 0 | GPT-5.4 (xhigh) 26→27, GPT-5.4 mini (xhigh) · DeepSWE 1.0 27→26 |
| GLM-5.2 (max) | 24 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GLM-5.3 Flash (max) | 48 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GLM-5.3 (max) | 72 | 0 | Gemini 3.5 Flash (high) 7→8, GPT-5.6 Sol (max) 8→7, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10, Grok 4.5 (high) 17→18, Claude Opus 4.7 (max) · DeepSWE 1.0 18→17 |
| GPT-5.4 (xhigh) | 28 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.5 (xhigh) | 40 | 0 | Gemini 3.5 Flash (high) 7→8, GPT-5.6 Sol (max) 8→7, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.6 Luna (max) | 48 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.6 Sol (max) | 60 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| GPT-5.6 Terra (max) | 56 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| Grok 4.5 (high) | 32 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Grok 4.5 (high) 17→18, Claude Opus 4.7 (max) · DeepSWE 1.0 18→17 |
| Grok 4.6 (medium) | 64 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→14, Grok 4.5 (high) 17→18, Claude Opus 4.7 (max) · DeepSWE 1.0 18→17 |
| Kimi K2.7 Code | 20 | 0 | none |
| Kimi K3 (max) | 52 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| Muse Spark 1.1 (xhigh) | 36 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| Muse Spark 1.2 (xhigh) | 44 | 0 | Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10, GLM-5.3 Flash (max) 19→20, DeepSeek V4 Flash (max) 20→19 |
| Qwen3.8 Max (xhigh) | 52 | 0 | Qwen3.8 Max (xhigh) 5→6, Grok 4.6 (medium) 6→5, Gemini 3.6 Flash (high) 10→11, Claude Sonnet 5 (max) 11→10 |
| (dedup panel) | 0 | 0 | none |

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| KaTeX/KaTeX (4) | Claude Fable 5 (xhigh) 1→3, GLM-5.3 (max) 2→6, GPT-5.6 Terra (max) 3→2, Kimi K3 (max) 4→7, Qwen3.8 Max (xhigh) 5→8, Grok 4.6 (medium) 6→13, Gemini 3.5 Flash (high) 7→1, GPT-5.6 Sol (max) 8→4, DeepSeek V4 Pro (max) 9→16, Gemini 3.6 Flash (high) 10→9, Claude Sonnet 5 (max) 11→10, GPT-5.5 (xhigh) 12→5, Claude Opus 4.8 (max) 13→12, Claude Sonnet 4.6 (high) 14→11, GPT-5.6 Luna (max) 16→17, Grok 4.5 (high) 17→14, GLM-5.3 Flash (max) 19→20, DeepSeek V4 Flash (max) 20→23, Claude Opus 5 (max) 21→28, Kimi K2.7 Code 23→19, GLM-5.2 (max) 24→21, Muse Spark 1.1 (xhigh) 25→24, GPT-5.4 (xhigh) 26→25, GPT-5.4 mini (xhigh) · DeepSWE 1.0 27→26, Kimi K2.6 · DeepSWE 1.0 28→27, Gemini 3.1 Pro Preview (high) 30→31, MiniMax M3 · DeepSWE 1.0 31→30, MiniMax M2.7 · DeepSWE 1.0 37→38, Qwen3.6 Plus · DeepSWE 1.0 38→37 |
| csstree/csstree (4) | GPT-5.6 Terra (max) 3→8, Grok 4.6 (medium) 6→3, Gemini 3.5 Flash (high) 7→6, GPT-5.6 Sol (max) 8→15, DeepSeek V4 Pro (max) 9→10, Gemini 3.6 Flash (high) 10→7, GPT-5.5 (xhigh) 12→18, Claude Opus 4.8 (max) 13→9, Claude Sonnet 4.6 (high) 14→12, Gemini 3.7 Flash (medium) 15→13, GPT-5.6 Luna (max) 16→23, Grok 4.5 (high) 17→16, Claude Opus 4.7 (max) · DeepSWE 1.0 18→14, GLM-5.3 Flash (max) 19→17, DeepSeek V4 Flash (max) 20→19, Claude Opus 5 (max) 21→20, Muse Spark 1.2 (xhigh) 22→24, Kimi K2.7 Code 23→21, GLM-5.2 (max) 24→22, Muse Spark 1.1 (xhigh) 25→29, GPT-5.4 (xhigh) 26→31, GPT-5.4 mini (xhigh) · DeepSWE 1.0 27→25, Kimi K2.6 · DeepSWE 1.0 28→26, GLM-5.1 · DeepSWE 1.0 29→27, MiniMax M3 · DeepSWE 1.0 31→28, Grok Build 0.1 · DeepSWE 1.0 32→33, Claude Opus 4.6 (max) · DeepSWE 1.0 33→32 |
| testem/testem (8) | Claude Fable 5 (xhigh) 1→3, GLM-5.3 (max) 2→1, GPT-5.6 Terra (max) 3→2, Kimi K3 (max) 4→6, Grok 4.6 (medium) 6→10, Gemini 3.5 Flash (high) 7→13, GPT-5.6 Sol (max) 8→4, DeepSeek V4 Pro (max) 9→8, Gemini 3.6 Flash (high) 10→12, Claude Sonnet 5 (max) 11→7, GPT-5.5 (xhigh) 12→9, Claude Opus 4.8 (max) 13→19, Claude Sonnet 4.6 (high) 14→24, Gemini 3.7 Flash (medium) 15→11, GPT-5.6 Luna (max) 16→17, Grok 4.5 (high) 17→25, Claude Opus 4.7 (max) · DeepSWE 1.0 18→14, GLM-5.3 Flash (max) 19→26, DeepSeek V4 Flash (max) 20→23, Muse Spark 1.2 (xhigh) 22→16, Kimi K2.7 Code 23→18, GLM-5.2 (max) 24→27, Muse Spark 1.1 (xhigh) 25→15, GPT-5.4 (xhigh) 26→30, GPT-5.4 mini (xhigh) · DeepSWE 1.0 27→22, Kimi K2.6 · DeepSWE 1.0 28→20, GLM-5.1 · DeepSWE 1.0 29→32, Gemini 3.1 Pro Preview (high) 30→29, MiniMax M3 · DeepSWE 1.0 31→28, Grok Build 0.1 · DeepSWE 1.0 32→31, Claude Opus 4.6 (max) · DeepSWE 1.0 33→34, MiMo V2.5 Pro · DeepSWE 1.0 34→33, Claude Haiku 4.5 · DeepSWE 1.0 35→36, Gemini 3 Flash Preview · DeepSWE 1.0 36→35 |
| yjs/yjs (4) | GLM-5.3 (max) 2→4, GPT-5.6 Terra (max) 3→5, Kimi K3 (max) 4→2, Qwen3.8 Max (xhigh) 5→7, Grok 4.6 (medium) 6→3, Gemini 3.5 Flash (high) 7→9, GPT-5.6 Sol (max) 8→6, DeepSeek V4 Pro (max) 9→8, Gemini 3.6 Flash (high) 10→13, Claude Sonnet 5 (max) 11→12, GPT-5.5 (xhigh) 12→10, Claude Opus 4.8 (max) 13→14, Claude Sonnet 4.6 (high) 14→15, Gemini 3.7 Flash (medium) 15→18, GPT-5.6 Luna (max) 16→11, Grok 4.5 (high) 17→19, Claude Opus 4.7 (max) · DeepSWE 1.0 18→22, GLM-5.3 Flash (max) 19→17, Claude Opus 5 (max) 21→16, Muse Spark 1.2 (xhigh) 22→25, Kimi K2.7 Code 23→31, GLM-5.2 (max) 24→23, Muse Spark 1.1 (xhigh) 25→26, GPT-5.4 (xhigh) 26→21, GPT-5.4 mini (xhigh) · DeepSWE 1.0 27→33, Kimi K2.6 · DeepSWE 1.0 28→38, GLM-5.1 · DeepSWE 1.0 29→24, Gemini 3.1 Pro Preview (high) 30→27, MiniMax M3 · DeepSWE 1.0 31→30, Grok Build 0.1 · DeepSWE 1.0 32→29, Claude Opus 4.6 (max) · DeepSWE 1.0 33→28, MiMo V2.5 Pro · DeepSWE 1.0 34→37, Claude Haiku 4.5 · DeepSWE 1.0 35→32, Gemini 3 Flash Preview · DeepSWE 1.0 36→34, MiniMax M2.7 · DeepSWE 1.0 37→35, Qwen3.6 Plus · DeepSWE 1.0 38→36 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (20) | Solved by fewer (20) |
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
| Claude Opus 4.7 (max) · DeepSWE 1.0 | 15.5 (18) | 15.5 (18) |
| GLM-5.3 Flash (max) | 13.1 (19) | 13.1 (19) |
| DeepSeek V4 Flash (max) | 12.5 (20) | 12.5 (20) |
| Claude Opus 5 (max) | 11.1 (21) | 11.1 (21) |
| Muse Spark 1.2 (xhigh) | 9.7 (22) | 9.7 (22) |
| Kimi K2.7 Code | 9.2 (23) | 9.2 (23) |
| GLM-5.2 (max) | 8.8 (24) | 8.8 (24) |
| Muse Spark 1.1 (xhigh) | 8.1 (25) | 8.1 (25) |
| GPT-5.4 (xhigh) | 4.8 (26) | 4.8 (26) |
| GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 4.6 (27) | 4.6 (27) |
| Kimi K2.6 · DeepSWE 1.0 | 4.3 (28) | 4.3 (28) |
| GLM-5.1 · DeepSWE 1.0 | 2.2 (29) | 2.2 (29) |
| Gemini 3.1 Pro Preview (high) | 1.4 (30) | 1.4 (30) |
| MiniMax M3 · DeepSWE 1.0 | 1.1 (31) | 1.1 (31) |
| Grok Build 0.1 · DeepSWE 1.0 | -1.6 (32) | -1.6 (32) |
| Claude Opus 4.6 (max) · DeepSWE 1.0 | -2.3 (33) | -2.3 (33) |
| MiMo V2.5 Pro · DeepSWE 1.0 | -6.5 (34) | -6.5 (34) |
| Claude Haiku 4.5 · DeepSWE 1.0 | -8.1 (35) | -8.1 (35) |
| Gemini 3 Flash Preview · DeepSWE 1.0 | -8.7 (36) | -8.7 (36) |
| MiniMax M2.7 · DeepSWE 1.0 | -10.5 (37) | -10.5 (37) |
| Qwen3.6 Plus · DeepSWE 1.0 | -10.6 (38) | -10.6 (38) |

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
- **Grok 4.5 (high) − Claude Opus 4.7 (max) · DeepSWE 1.0 = 0.27**: failed/failed -0.09 (9), failed/solved -8.19 (3), solved/failed 1.53 (1), solved/solved 7.02 (7). For Grok 4.5 (high): `testem-per-launcher-reports#3` +1.90 (solved/solved), `testem-per-launcher-reports#4` +1.63 (solved/solved), `csstree-shorthand-expansion-compression#4` +1.53 (solved/failed). For Claude Opus 4.7 (max) · DeepSWE 1.0: `katex-multicolumn-array-spans#2` -3.15 (failed/solved), `yjs-map-conflict-detection#4` -3.15 (failed/solved), `katex-multicolumn-array-spans#1` -1.89 (failed/solved).
- **Claude Opus 4.7 (max) · DeepSWE 1.0 − GLM-5.3 Flash (max) = 2.49**: failed/failed -0.05 (7), failed/solved -6.56 (3), solved/failed 1.86 (1), solved/solved 7.25 (9). For Claude Opus 4.7 (max) · DeepSWE 1.0: `yjs-map-conflict-detection#3` +3.05 (solved/solved), `yjs-map-conflict-detection#2` +2.15 (solved/solved), `yjs-map-conflict-detection#1` +1.95 (solved/solved). For GLM-5.3 Flash (max): `testem-bail-on-test-failure#1` -2.73 (failed/solved), `testem-bail-on-test-failure#2` -2.02 (failed/solved), `katex-multicolumn-array-spans#3` -1.81 (failed/solved).
- **GLM-5.3 Flash (max) − DeepSeek V4 Flash (max) = 0.52**: failed/failed -0.15 (7), failed/solved -3.71 (1), solved/failed 12.34 (6), solved/solved -7.97 (6). For GLM-5.3 Flash (max): `testem-bail-on-test-failure#1` +2.68 (solved/failed), `testem-per-launcher-reports#2` +2.55 (solved/failed), `testem-per-launcher-reports#1` +2.04 (solved/failed). For DeepSeek V4 Flash (max): `yjs-map-conflict-detection#2` -3.81 (solved/solved), `katex-multicolumn-array-spans#4` -3.71 (failed/solved), `testem-per-launcher-reports#4` -3.08 (solved/solved).
- **DeepSeek V4 Flash (max) − Claude Opus 5 (max) = 1.40**: failed/failed 0.10 (7), failed/solved -10.93 (6), solved/solved 12.23 (7). For DeepSeek V4 Flash (max): `yjs-map-conflict-detection#2` +4.04 (solved/solved), `testem-per-launcher-reports#3` +3.96 (solved/solved), `testem-per-launcher-reports#4` +3.14 (solved/solved). For Claude Opus 5 (max): `katex-multicolumn-array-spans#1` -3.97 (failed/solved), `testem-bail-on-test-failure#3` -1.78 (failed/solved), `yjs-map-conflict-detection#1` -1.49 (failed/solved).
- **Claude Opus 5 (max) − Muse Spark 1.2 (xhigh) = 1.46**: failed/failed -0.10 (5), failed/solved -4.41 (2), solved/failed 10.06 (4), solved/solved -4.09 (9). For Claude Opus 5 (max): `katex-multicolumn-array-spans#1` +4.10 (solved/failed), `katex-multicolumn-array-spans#4` +2.50 (solved/failed), `testem-bail-on-test-failure#3` +2.02 (solved/failed). For Muse Spark 1.2 (xhigh): `csstree-shorthand-expansion-compression#3` -3.74 (failed/solved), `yjs-map-conflict-detection#3` -3.49 (solved/solved), `yjs-map-conflict-detection#2` -1.84 (solved/solved).
- **Muse Spark 1.2 (xhigh) − Kimi K2.7 Code = 0.45**: failed/failed -0.86 (9), solved/failed 8.58 (6), solved/solved -7.28 (5). For Muse Spark 1.2 (xhigh): `csstree-shorthand-expansion-compression#3` +3.74 (solved/failed), `testem-per-launcher-reports#3` +1.83 (solved/failed), `katex-multicolumn-array-spans#2` +1.08 (solved/failed). For Kimi K2.7 Code: `testem-per-launcher-reports#2` -3.02 (solved/solved), `yjs-map-conflict-detection#2` -1.85 (solved/solved), `yjs-map-conflict-detection#3` -1.07 (solved/solved).
- **Kimi K2.7 Code − GLM-5.2 (max) = 0.46**: failed/failed 0.04 (13), failed/solved -4.99 (2), solved/failed 4.27 (1), solved/solved 1.14 (4). For Kimi K2.7 Code: `yjs-map-conflict-detection#4` +4.27 (solved/failed), `yjs-map-conflict-detection#3` +2.13 (solved/solved), `yjs-map-conflict-detection#2` +1.44 (solved/solved). For GLM-5.2 (max): `testem-per-launcher-reports#4` -3.94 (failed/solved), `yjs-map-conflict-detection#1` -1.96 (solved/solved), `testem-per-launcher-reports#1` -1.05 (failed/solved).
- **GLM-5.2 (max) − Muse Spark 1.1 (xhigh) = 0.71**: failed/failed 1.09 (9), failed/solved -13.29 (5), solved/failed 8.41 (2), solved/solved 4.50 (4). For GLM-5.2 (max): `testem-per-launcher-reports#2` +4.37 (solved/failed), `testem-per-launcher-reports#4` +4.03 (solved/failed), `yjs-map-conflict-detection#1` +2.30 (solved/solved). For Muse Spark 1.1 (xhigh): `yjs-map-conflict-detection#4` -4.38 (failed/solved), `csstree-shorthand-expansion-compression#2` -4.22 (failed/solved), `csstree-shorthand-expansion-compression#4` -3.07 (failed/solved).
- **Muse Spark 1.1 (xhigh) − GPT-5.4 (xhigh) = 3.23**: failed/failed -0.16 (6), failed/solved -15.09 (5), solved/failed 19.48 (7), solved/solved -1.00 (2). For Muse Spark 1.1 (xhigh): `yjs-map-conflict-detection#4` +4.30 (solved/failed), `csstree-shorthand-expansion-compression#2` +4.21 (solved/failed), `yjs-map-conflict-detection#3` +3.38 (solved/failed). For GPT-5.4 (xhigh): `csstree-shorthand-expansion-compression#1` -5.40 (failed/solved), `testem-per-launcher-reports#4` -4.50 (failed/solved), `testem-per-launcher-reports#2` -2.47 (failed/solved).
- **GPT-5.4 (xhigh) − GPT-5.4 mini (xhigh) · DeepSWE 1.0 = 0.26**: failed/failed -0.78 (11), failed/solved -8.83 (2), solved/failed 12.98 (4), solved/solved -3.11 (3). For GPT-5.4 (xhigh): `csstree-shorthand-expansion-compression#1` +5.37 (solved/failed), `testem-per-launcher-reports#4` +4.48 (solved/failed), `testem-per-launcher-reports#2` +2.48 (solved/failed). For GPT-5.4 mini (xhigh) · DeepSWE 1.0: `yjs-map-conflict-detection#1` -4.99 (failed/solved), `yjs-map-conflict-detection#3` -3.85 (failed/solved), `yjs-map-conflict-detection#2` -3.17 (solved/solved).
- **GPT-5.4 mini (xhigh) · DeepSWE 1.0 − Kimi K2.6 · DeepSWE 1.0 = 0.24**: failed/failed -0.58 (15), solved/failed 2.46 (2), solved/solved -1.64 (3). For GPT-5.4 mini (xhigh) · DeepSWE 1.0: `testem-per-launcher-reports#1` +1.41 (solved/failed), `testem-per-launcher-reports#3` +1.05 (solved/failed), `katex-multicolumn-array-spans#4` +0.38 (failed/failed). For Kimi K2.6 · DeepSWE 1.0: `yjs-map-conflict-detection#3` -1.07 (solved/solved), `yjs-map-conflict-detection#1` -0.51 (solved/solved), `testem-bail-on-test-failure#1` -0.18 (failed/failed).
- **Kimi K2.6 · DeepSWE 1.0 − GLM-5.1 · DeepSWE 1.0 = 2.11**: failed/failed 0.49 (15), failed/solved -8.71 (2), solved/failed 10.33 (2). For Kimi K2.6 · DeepSWE 1.0: `yjs-map-conflict-detection#1` +5.35 (solved/failed), `yjs-map-conflict-detection#2` +4.98 (solved/failed), `katex-multicolumn-array-spans#1` +0.15 (failed/failed). For GLM-5.1 · DeepSWE 1.0: `testem-per-launcher-reports#2` -4.68 (failed/solved), `testem-per-launcher-reports#4` -4.03 (failed/solved), `yjs-map-conflict-detection#4` -0.14 (failed/failed).
- **GLM-5.1 · DeepSWE 1.0 − Gemini 3.1 Pro Preview (high) = 0.84**: failed/failed -2.23 (17), solved/failed 4.71 (1), solved/solved -1.64 (2). For GLM-5.1 · DeepSWE 1.0: `testem-per-launcher-reports#2` +4.71 (solved/failed), `katex-multicolumn-array-spans#3` +0.01 (failed/failed), `testem-bail-on-test-failure#3` -0.00 (failed/failed). For Gemini 3.1 Pro Preview (high): `testem-per-launcher-reports#4` -1.00 (solved/solved), `yjs-map-conflict-detection#3` -0.65 (solved/solved), `csstree-shorthand-expansion-compression#2` -0.36 (failed/failed).
- **Gemini 3.1 Pro Preview (high) − MiniMax M3 · DeepSWE 1.0 = 3.31**: failed/failed 1.88 (13), failed/solved -8.45 (4), solved/failed 5.88 (1), solved/solved 4.01 (1). For Gemini 3.1 Pro Preview (high): `yjs-map-conflict-detection#3` +5.88 (solved/failed), `testem-per-launcher-reports#4` +4.01 (solved/solved), `csstree-shorthand-expansion-compression#2` +0.36 (failed/failed). For MiniMax M3 · DeepSWE 1.0: `yjs-map-conflict-detection#4` -2.61 (failed/solved), `yjs-map-conflict-detection#1` -2.30 (failed/solved), `testem-per-launcher-reports#3` -2.02 (failed/solved).
- **MiniMax M3 · DeepSWE 1.0 − Grok Build 0.1 · DeepSWE 1.0 = -0.63**: failed/failed -1.50 (12), failed/solved -0.85 (1), solved/failed 4.34 (2), solved/solved -2.62 (3). For MiniMax M3 · DeepSWE 1.0: `yjs-map-conflict-detection#1` +2.74 (solved/failed), `testem-per-launcher-reports#4` +1.60 (solved/failed), `testem-per-launcher-reports#1` +0.69 (solved/solved). For Grok Build 0.1 · DeepSWE 1.0: `yjs-map-conflict-detection#4` -3.19 (solved/solved), `testem-per-launcher-reports#2` -0.85 (failed/solved), `csstree-shorthand-expansion-compression#1` -0.37 (failed/failed).
- **Grok Build 0.1 · DeepSWE 1.0 − Claude Opus 4.6 (max) · DeepSWE 1.0 = 0.81**: failed/failed 0.78 (12), failed/solved -7.83 (3), solved/failed 8.76 (3), solved/solved -0.90 (1). For Grok Build 0.1 · DeepSWE 1.0: `yjs-map-conflict-detection#4` +5.68 (solved/failed), `testem-per-launcher-reports#3` +2.20 (solved/failed), `testem-per-launcher-reports#1` +0.88 (solved/failed). For Claude Opus 4.6 (max) · DeepSWE 1.0: `testem-per-launcher-reports#4` -3.32 (failed/solved), `yjs-map-conflict-detection#2` -3.22 (failed/solved), `katex-multicolumn-array-spans#1` -1.29 (failed/solved).
- **Claude Opus 4.6 (max) · DeepSWE 1.0 − MiMo V2.5 Pro · DeepSWE 1.0 = 4.20**: failed/failed -0.60 (15), failed/solved -4.04 (1), solved/failed 8.83 (4). For Claude Opus 4.6 (max) · DeepSWE 1.0: `yjs-map-conflict-detection#2` +2.99 (solved/failed), `testem-per-launcher-reports#4` +2.88 (solved/failed), `testem-per-launcher-reports#2` +1.55 (solved/failed). For MiMo V2.5 Pro · DeepSWE 1.0: `yjs-map-conflict-detection#3` -4.04 (failed/solved), `csstree-shorthand-expansion-compression#4` -0.20 (failed/failed), `csstree-shorthand-expansion-compression#2` -0.12 (failed/failed).
- **MiMo V2.5 Pro · DeepSWE 1.0 − Claude Haiku 4.5 · DeepSWE 1.0 = 1.66**: failed/failed -2.16 (19), solved/failed 3.82 (1). For MiMo V2.5 Pro · DeepSWE 1.0: `yjs-map-conflict-detection#3` +3.82 (solved/failed), `testem-per-launcher-reports#4` +0.05 (failed/failed), `testem-per-launcher-reports#2` +0.01 (failed/failed). For Claude Haiku 4.5 · DeepSWE 1.0: `csstree-shorthand-expansion-compression#3` -0.27 (failed/failed), `katex-multicolumn-array-spans#1` -0.24 (failed/failed), `katex-multicolumn-array-spans#3` -0.22 (failed/failed).
- **Claude Haiku 4.5 · DeepSWE 1.0 − Gemini 3 Flash Preview · DeepSWE 1.0 = -0.35**: failed/failed -0.35 (16). For Claude Haiku 4.5 · DeepSWE 1.0: `csstree-shorthand-expansion-compression#4` +0.28 (failed/failed), `katex-multicolumn-array-spans#1` +0.21 (failed/failed), `katex-multicolumn-array-spans#3` +0.17 (failed/failed). For Gemini 3 Flash Preview · DeepSWE 1.0: `yjs-map-conflict-detection#1` -0.42 (failed/failed), `csstree-shorthand-expansion-compression#2` -0.41 (failed/failed), `yjs-map-conflict-detection#2` -0.38 (failed/failed).
- **Gemini 3 Flash Preview · DeepSWE 1.0 − MiniMax M2.7 · DeepSWE 1.0 = 2.50**: failed/failed 2.50 (16). For Gemini 3 Flash Preview · DeepSWE 1.0: `yjs-map-conflict-detection#4` +0.74 (failed/failed), `csstree-shorthand-expansion-compression#2` +0.58 (failed/failed), `yjs-map-conflict-detection#1` +0.47 (failed/failed). For MiniMax M2.7 · DeepSWE 1.0: `katex-multicolumn-array-spans#3` -0.23 (failed/failed), `testem-bail-on-test-failure#1` -0.22 (failed/failed), `testem-per-launcher-reports#1` -0.01 (failed/failed).
- **MiniMax M2.7 · DeepSWE 1.0 − Qwen3.6 Plus · DeepSWE 1.0 = 0.13**: failed/failed 0.13 (18). For MiniMax M2.7 · DeepSWE 1.0: `yjs-map-conflict-detection#3` +0.21 (failed/failed), `katex-multicolumn-array-spans#3` +0.20 (failed/failed), `yjs-map-conflict-detection#1` +0.16 (failed/failed). For Qwen3.6 Plus · DeepSWE 1.0: `yjs-map-conflict-detection#4` -0.41 (failed/failed), `katex-multicolumn-array-spans#1` -0.18 (failed/failed), `csstree-shorthand-expansion-compression#4` -0.16 (failed/failed).

## Regenerate

```sh
python -m parsimony.stability examples/deepswe-javascript/score-panel.json examples/deepswe-javascript/*.jsonl --output examples/deepswe-javascript/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
