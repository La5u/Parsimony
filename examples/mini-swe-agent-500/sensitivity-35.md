# Score sensitivity: 35 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `mini-swe-agent-33-448-solved-80-20-v0.5`: 448 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (70 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Opus 4.5 > Claude Opus 4.6 ≈ MiniMax M2.5 ≈ glm-5.1-evalscope ≈ Gemini 3 Pro (preview) ≈ Kimi K2.5 ≈ Gemini 3 Flash ≈ GLM-5 > Claude Sonnet 4.5 ≈ Claude Opus 4 ≈ Claude Haiku 4.5 ≈ Kimi K2 Thinking ≈ Gemini 2.5 Pro ≈ gemini-3-5-flash ≈ GPT-5.1 ≈ Claude Sonnet 4 ≈ GPT-5.1 Codex ≈ GPT-5 ≈ GPT-5.2 ≈ DeepSeek V3.2 ≈ MiniMax M2 ≈ GLM-4.5 ≈ Devstral Small 2512 ≈ o3 ≈ GPT-5.2 ≈ Devstral 2512 ≈ GLM-4.6 ≈ Qwen3-Coder 480B ≈ GPT-5 mini ≈ Kimi K2 Instruct ≈ o4-mini > GPT-5 nano ≈ gpt-oss-120b ≈ Llama 4 Maverick ≈ Qwen2.5-Coder 32B (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (3 of 34 adjacent pairs): Claude Opus 4.5 > Claude Opus 4.6, GLM-5 > Claude Sonnet 4.5, o4-mini > GPT-5 nano.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 31 pairs): Claude Opus 4.6 vs MiniMax M2.5, MiniMax M2.5 vs glm-5.1-evalscope, glm-5.1-evalscope vs Gemini 3 Pro (preview), Gemini 3 Pro (preview) vs Kimi K2.5, Kimi K2.5 vs Gemini 3 Flash, Gemini 3 Flash vs GLM-5, Claude Sonnet 4.5 vs Claude Opus 4, Claude Opus 4 vs Claude Haiku 4.5, Claude Haiku 4.5 vs Kimi K2 Thinking, Kimi K2 Thinking vs Gemini 2.5 Pro, Gemini 2.5 Pro vs gemini-3-5-flash, gemini-3-5-flash vs GPT-5.1, GPT-5.1 vs Claude Sonnet 4, Claude Sonnet 4 vs GPT-5.1 Codex, GPT-5.1 Codex vs GPT-5, GPT-5 vs GPT-5.2, GPT-5.2 vs DeepSeek V3.2, DeepSeek V3.2 vs MiniMax M2, MiniMax M2 vs GLM-4.5, GLM-4.5 vs Devstral Small 2512, Devstral Small 2512 vs o3, o3 vs GPT-5.2, GPT-5.2 vs Devstral 2512, Devstral 2512 vs GLM-4.6, GLM-4.6 vs Qwen3-Coder 480B, Qwen3-Coder 480B vs GPT-5 mini, GPT-5 mini vs Kimi K2 Instruct, Kimi K2 Instruct vs o4-mini, GPT-5 nano vs gpt-oss-120b, gpt-oss-120b vs Llama 4 Maverick, Llama 4 Maverick vs Qwen2.5-Coder 32B.
- **Midpoint rank never changes under any variation**: Claude Opus 4.5 (1), Claude Opus 4.6 (2), MiniMax M2.5 (3), Kimi K2.5 (6), Claude Sonnet 4.5 (9), GPT-5 mini (29), Kimi K2 Instruct (30), o4-mini (31), GPT-5 nano (32), gpt-oss-120b (33), Llama 4 Maverick (34), Qwen2.5-Coder 32B (35).
- Difficulty strata answer a different question and are not counted as variations; they reverse Claude Opus 4.5 > Claude Opus 4.6 (solved by all); MiniMax M2.5 > glm-5.1-evalscope (solved by all); glm-5.1-evalscope > Gemini 3 Pro (preview) (solved by fewer); Gemini 3 Pro (preview) > Kimi K2.5 (solved by all); Gemini 3 Flash > GLM-5 (solved by all); Claude Sonnet 4.5 > Claude Opus 4 (solved by all); Claude Opus 4 > Claude Haiku 4.5 (solved by all); Claude Haiku 4.5 > Kimi K2 Thinking (solved by all); Gemini 2.5 Pro > gemini-3-5-flash (solved by fewer); gemini-3-5-flash > GPT-5.1 (solved by all); Claude Sonnet 4 > GPT-5.1 Codex (solved by all); GPT-5.1 Codex > GPT-5 (solved by all); GPT-5 > GPT-5.2 (solved by all); DeepSeek V3.2 > MiniMax M2 (solved by all); GLM-4.5 > Devstral Small 2512 (solved by fewer); Devstral Small 2512 > o3 (solved by all); o3 > GPT-5.2 (solved by fewer); GPT-5.2 > Devstral 2512 (solved by all); GLM-4.6 > Qwen3-Coder 480B (solved by all); Qwen3-Coder 480B > GPT-5 mini (solved by all); Kimi K2 Instruct > o4-mini (solved by all); Llama 4 Maverick > Qwen2.5-Coder 32B (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 448 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Opus 4.5 | 51.4 | 48.8–54.1 | 51.3–51.4 | 1–1 | 1.0–1.0 | 0.98 |
| 2 | Claude Opus 4.6 | 48.3 | 45.4–51.0 | 48.3 | 2–2 | 2.0–3.0 | 0.01 |
| 3 | MiniMax M2.5 | 46.6 | 43.9–49.4 | 46.5–46.7 | 3–3 | 2.0–5.0 | 0.00 |
| 4 | glm-5.1-evalscope | 44.4 | 41.3–47.5 | 44.4–44.5 | 4–5 | 3.0–7.0 | 0.00 |
| 5 | Gemini 3 Pro (preview) | 44.1 | 41.1–47.2 | 44.0–44.2 | 4–5 | 3.0–8.0 | 0.00 |
| 6 | Kimi K2.5 | 43.5 | 40.4–46.5 | 43.4–43.5 | 6–6 | 4.0–8.0 | 0.00 |
| 7 | Gemini 3 Flash | 42.7 | 40.0–45.5 | 42.7 | 7–8 | 4.0–8.0 | 0.00 |
| 8 | GLM-5 | 41.3 | 38.5–44.3 | 41.3 | 7–8 | 5.0–8.0 | 0.00 |
| 9 | Claude Sonnet 4.5 | 38.0 | 35.2–40.8 | 37.9–38.0 | 9–9 | 9.0–10.0 | 0.00 |
| 10 | Claude Opus 4 | 34.7 | 31.7–37.7 | 34.5–34.8 | 10–13 | 10.0–15.0 | 0.00 |
| 11 | Claude Haiku 4.5 | 34.4 | 31.5–37.3 | 34.4 | 10–12 | 10.0–16.0 | 0.00 |
| 12 | Kimi K2 Thinking | 34.1 | 30.4–37.7 | 33.7–34.6 | 11–15 | 10.0–17.0 | 0.00 |
| 13 | Gemini 2.5 Pro | 33.5 | 28.7–38.1 | 32.4–34.7 | 10–15 | 10.0–18.0 | 0.00 |
| 14 | gemini-3-5-flash | 33.4 | 30.6–36.4 | 33.4 | 10–20 | 10.0–18.0 | 0.00 |
| 15 | GPT-5.1 | 33.4 | 30.2–36.6 | 33.2–33.5 | 11–15 | 10.0–18.0 | 0.00 |
| 16 | Claude Sonnet 4 | 31.9 | 28.9–35.0 | 31.8–31.9 | 14–17 | 12.0–21.0 | 0.00 |
| 17 | GPT-5.1 Codex | 31.5 | 28.8–34.4 | 31.5 | 16–18 | 13.0–22.0 | 0.00 |
| 18 | GPT-5 | 30.2 | 26.7–34.1 | 29.5–31.0 | 18–22 | 15.0–25.0 | 0.00 |
| 19 | GPT-5.2 | 30.1 | 26.4–33.7 | 29.6–30.6 | 16–22 | 14.0–26.0 | 0.00 |
| 20 | DeepSeek V3.2 | 29.1 | 26.3–32.0 | 29.0–29.2 | 20–24 | 17.0–27.0 | 0.00 |
| 21 | MiniMax M2 | 29.0 | 25.4–32.7 | 28.5–29.4 | 19–25 | 17.0–27.0 | 0.00 |
| 22 | GLM-4.5 | 28.6 | 24.5–32.6 | 27.9–29.3 | 20–26 | 17.0–28.0 | 0.00 |
| 23 | Devstral Small 2512 | 28.6 | 25.0–32.3 | 28.2–28.9 | 17–26 | 17.0–28.0 | 0.00 |
| 24 | o3 | 28.4 | 25.1–31.9 | 28.2–28.6 | 21–28 | 17.0–28.0 | 0.00 |
| 25 | GPT-5.2 | 28.2 | 25.6–31.1 | 28.2 | 19–27 | 18.0–28.0 | 0.00 |
| 26 | Devstral 2512 | 28.1 | 24.8–31.3 | 27.8–28.3 | 22–26 | 18.0–28.0 | 0.00 |
| 27 | GLM-4.6 | 27.1 | 23.1–31.1 | 26.3–27.9 | 26–28 | 20.0–29.0 | 0.00 |
| 28 | Qwen3-Coder 480B | 26.1 | 22.0–30.3 | 25.2–27.1 | 25–28 | 22.0–29.0 | 0.00 |
| 29 | GPT-5 mini | 24.5 | 21.1–27.8 | 24.2–24.8 | 29–29 | 26.0–30.0 | 0.00 |
| 30 | Kimi K2 Instruct | 21.9 | 18.2–25.7 | 21.2–22.6 | 30–30 | 29.0–31.0 | 0.00 |
| 31 | o4-mini | 19.6 | 14.1–25.0 | 17.4–21.7 | 31–31 | 30.0–31.0 | 0.00 |
| 32 | GPT-5 nano | 11.8 | 8.3–15.4 | 11.1–12.5 | 32–32 | 32.0–32.0 | 0.00 |
| 33 | gpt-oss-120b | 6.6 | 0.3–13.0 | 3.1–10.1 | 33–33 | 33.0–34.0 | 0.00 |
| 34 | Llama 4 Maverick | 5.2 | -2.3–12.3 | 0.9–9.5 | 34–34 | 33.0–34.0 | 0.00 |
| 35 | Qwen2.5-Coder 32B | -4.3 | -15.0–5.9 | -12.9–4.2 | 35–35 | 35.0–35.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Opus 4.5 > Claude Opus 4.6 | 3.11 | 0.27 to 6.09 | 0.98 | none | yes |
| Claude Opus 4.6 > MiniMax M2.5 | 1.64 | -1.56 to 4.77 | 0.82 | none | yes |
| MiniMax M2.5 > glm-5.1-evalscope | 2.18 | -1.28 to 5.69 | 0.89 | none | yes |
| glm-5.1-evalscope > Gemini 3 Pro (preview) | 0.32 | -3.46 to 4.01 | 0.53 | without django/django, without mwaskom/seaborn, without scikit-learn/scikit-learn | yes |
| Gemini 3 Pro (preview) > Kimi K2.5 | 0.64 | -3.05 to 4.57 | 0.61 | none | yes |
| Kimi K2.5 > Gemini 3 Flash | 0.75 | -2.94 to 4.27 | 0.64 | none | yes |
| Gemini 3 Flash > GLM-5 | 1.38 | -1.88 to 4.70 | 0.78 | without sympy/sympy | yes |
| GLM-5 > Claude Sonnet 4.5 | 3.36 | 0.26 to 6.69 | 0.98 | none | yes |
| Claude Sonnet 4.5 > Claude Opus 4 | 3.32 | -0.02 to 6.62 | 0.97 | none | yes |
| Claude Opus 4 > Claude Haiku 4.5 | 0.23 | -3.23 to 3.64 | 0.54 | failure cap=0, failure cap=10, without django/django, without pydata/xarray, without sympy/sympy | yes |
| Claude Haiku 4.5 > Kimi K2 Thinking | 0.28 | -3.35 to 4.04 | 0.47 | without psf/requests, without pytest-dev/pytest, without scikit-learn/scikit-learn | no |
| Kimi K2 Thinking > Gemini 2.5 Pro | 0.62 | -4.73 to 6.16 | 0.31 | net weight=1, without django/django | no |
| Gemini 2.5 Pro > gemini-3-5-flash | 0.08 | -5.41 to 5.24 | 0.32 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=50, panel without Gemini 3 Pro (preview), panel without Claude Opus 4.5, panel without Claude Opus 4.6, panel without MiniMax M2.5, panel dedup, without astropy/astropy, without matplotlib/matplotlib, without mwaskom/seaborn, without pallets/flask, without pydata/xarray, without scikit-learn/scikit-learn | no |
| gemini-3-5-flash > GPT-5.1 | 0.06 | -3.75 to 3.95 | 0.50 | net weight=0.9, net weight=1, failure cap=0, failure cap=10, panel without o4-mini, panel without gpt-oss-120b, panel without Kimi K2 Instruct, panel without GLM-4.6, panel without GPT-5.2, panel without Gemini 3 Flash, panel without GPT-5.2, panel without Kimi K2.5, panel dedup, without astropy/astropy, without django/django, without psf/requests, without sphinx-doc/sphinx, without sympy/sympy | no |
| GPT-5.1 > Claude Sonnet 4 | 1.52 | -2.27 to 5.33 | 0.76 | none | yes |
| Claude Sonnet 4 > GPT-5.1 Codex | 0.37 | -3.20 to 3.88 | 0.57 | net weight=0.9, net weight=1, failure cap=50, without matplotlib/matplotlib, without pydata/xarray | yes |
| GPT-5.1 Codex > GPT-5 | 1.24 | -2.75 to 5.09 | 0.62 | none | yes |
| GPT-5 > GPT-5.2 | 0.14 | -4.25 to 5.01 | 0.26 | net weight=0.9, net weight=1, failure cap=0, failure cap=10, without django/django, without sphinx-doc/sphinx | no |
| GPT-5.2 > DeepSeek V3.2 | 1.01 | -3.00 to 4.93 | 0.59 | without sympy/sympy | yes |
| DeepSeek V3.2 > MiniMax M2 | 0.13 | -4.05 to 4.38 | 0.41 | net weight=0.5, net weight=0.6, net weight=0.7, net floor=0, failure cap=0, failure cap=10, panel without GPT-5.2, panel without DeepSeek V3.2, without django/django, without sphinx-doc/sphinx, without sympy/sympy | no |
| MiniMax M2 > GLM-4.5 | 0.39 | -4.20 to 5.25 | 0.32 | failure cap=0, failure cap=10, without matplotlib/matplotlib | no |
| GLM-4.5 > Devstral Small 2512 | 0.03 | -4.85 to 4.84 | 0.28 | net weight=0.9, net weight=1, failure cap=50, panel without Claude Sonnet 4, panel without Gemini 2.5 Pro, panel without o4-mini, panel without GLM-4.6, panel without Claude Opus 4.5, panel without Claude Sonnet 4.5, panel without GLM-5, panel without Kimi K2.5, panel without MiniMax M2.5, without astropy/astropy, without django/django, without mwaskom/seaborn, without pydata/xarray, without scikit-learn/scikit-learn | no |
| Devstral Small 2512 > o3 | 0.15 | -4.25 to 4.62 | 0.40 | failure cap=0, failure cap=10, without matplotlib/matplotlib, without psf/requests, without pydata/xarray, without pylint-dev/pylint, without pytest-dev/pytest, without scikit-learn/scikit-learn, without sphinx-doc/sphinx | no |
| o3 > GPT-5.2 | 0.17 | -3.89 to 4.19 | 0.49 | net weight=0.9, net weight=1, failure cap=50, panel without Gemini 3 Flash, panel without GLM-5, without astropy/astropy, without django/django, without scikit-learn/scikit-learn, without sympy/sympy | no |
| GPT-5.2 > Devstral 2512 | 0.18 | -3.64 to 4.23 | 0.49 | net weight=0.5, net weight=0.6, net weight=0.7, net floor=0, panel without GPT-5.2, without django/django, without pytest-dev/pytest, without sphinx-doc/sphinx | no |
| Devstral 2512 > GLM-4.6 | 0.98 | -3.41 to 5.69 | 0.49 | none | no |
| GLM-4.6 > Qwen3-Coder 480B | 0.95 | -4.37 to 6.31 | 0.33 | without django/django, without sphinx-doc/sphinx | no |
| Qwen3-Coder 480B > GPT-5 mini | 1.66 | -3.31 to 6.58 | 0.56 | none | yes |
| GPT-5 mini > Kimi K2 Instruct | 2.59 | -2.18 to 7.17 | 0.80 | none | yes |
| Kimi K2 Instruct > o4-mini | 2.32 | -4.26 to 9.12 | 0.39 | none | no |
| o4-mini > GPT-5 nano | 7.76 | 1.25 to 14.18 | 1.00 | none | yes |
| GPT-5 nano > gpt-oss-120b | 5.17 | -2.22 to 12.79 | 0.74 | none | yes |
| gpt-oss-120b > Llama 4 Maverick | 1.43 | -9.63 to 12.52 | 0.00 | none | no |
| Llama 4 Maverick > Qwen2.5-Coder 32B | 9.55 | -6.21 to 25.09 | 0.02 | none | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.5 | 51.4 (1) | 51.0 (1) | 51.2 (1) | 51.3 (1) | 51.5 (1) | 51.6 (1) | 51.2 (1) | 52.7 (1) | 52.2 (1) | 50.1 (1) |
| Claude Opus 4.6 | 48.3 (2) | 48.2 (2) | 48.2 (2) | 48.2 (2) | 48.3 (2) | 48.3 (2) | 48.1 (2) | 49.6 (2) | 49.0 (2) | 47.0 (2) |
| MiniMax M2.5 | 46.6 (3) | 46.8 (3) | 46.8 (3) | 46.7 (3) | 46.5 (3) | 46.5 (3) | 46.5 (3) | 48.0 (3) | 47.5 (3) | 45.2 (3) |
| glm-5.1-evalscope | 44.4 (4) | 44.4 (4) | 44.4 (4) | 44.4 (4) | 44.4 (4) | 44.4 (4) | 44.3 (4) | 46.3 (4) | 45.6 (4) | 42.5 (4) |
| Gemini 3 Pro (preview) | 44.1 (5) | 43.9 (5) | 44.0 (5) | 44.0 (5) | 44.2 (5) | 44.3 (5) | 44.2 (5) | 45.8 (5) | 45.1 (5) | 42.4 (5) |
| Kimi K2.5 | 43.5 (6) | 43.5 (6) | 43.5 (6) | 43.5 (6) | 43.5 (6) | 43.4 (6) | 43.3 (6) | 45.4 (6) | 44.7 (6) | 41.5 (6) |
| Gemini 3 Flash | 42.7 (7) | 41.8 (7) | 42.1 (7) | 42.4 (7) | 43.0 (7) | 43.3 (7) | 42.3 (7) | 44.4 (7) | 43.7 (7) | 41.0 (7) |
| GLM-5 | 41.3 (8) | 41.3 (8) | 41.3 (8) | 41.3 (8) | 41.3 (8) | 41.3 (8) | 41.2 (8) | 43.1 (8) | 42.4 (8) | 39.6 (8) |
| Claude Sonnet 4.5 | 38.0 (9) | 38.0 (9) | 38.0 (9) | 38.0 (9) | 38.0 (9) | 38.0 (9) | 38.0 (9) | 40.2 (9) | 39.3 (9) | 35.8 (9) |
| Claude Opus 4 | 34.7 (10) | 34.9 (10) | 34.8 (10) | 34.7 (10) | 34.6 (10) | 34.5 (10) | 34.7 (10) | 36.9 (13) | 36.0 (11) | 32.4 (10) |
| Claude Haiku 4.5 | 34.4 (11) | 34.7 (11) | 34.6 (11) | 34.5 (11) | 34.3 (11) | 34.2 (11) | 34.5 (11) | 37.5 (10) | 36.3 (10) | 31.4 (12) |
| Kimi K2 Thinking | 34.1 (12) | 34.5 (12) | 34.4 (12) | 34.3 (12) | 34.0 (12) | 33.9 (14) | 34.3 (12) | 37.2 (11) | 36.0 (12) | 31.1 (13) |
| Gemini 2.5 Pro | 33.5 (13) | 32.9 (14) | 33.1 (14) | 33.3 (14) | 33.7 (13) | 34.0 (12) | 33.4 (13) | 37.1 (12) | 35.7 (13) | 30.0 (15) |
| gemini-3-5-flash | 33.4 (14) | 33.1 (13) | 33.2 (13) | 33.3 (13) | 33.6 (15) | 33.7 (15) | 33.3 (14) | 34.9 (16) | 34.3 (15) | 32.0 (11) |
| GPT-5.1 | 33.4 (15) | 32.5 (15) | 32.8 (15) | 33.1 (15) | 33.7 (14) | 33.9 (13) | 33.2 (15) | 36.2 (14) | 35.1 (14) | 30.6 (14) |
| Claude Sonnet 4 | 31.9 (16) | 32.3 (16) | 32.1 (16) | 32.0 (16) | 31.7 (17) | 31.6 (17) | 32.1 (16) | 35.0 (15) | 33.7 (16) | 28.7 (17) |
| GPT-5.1 Codex | 31.5 (17) | 30.3 (17) | 30.7 (17) | 31.1 (17) | 31.9 (16) | 32.3 (16) | 31.3 (17) | 34.0 (17) | 33.0 (17) | 29.0 (16) |
| GPT-5 | 30.2 (18) | 30.1 (18) | 30.1 (18) | 30.2 (18) | 30.3 (19) | 30.4 (19) | 30.2 (18) | 32.9 (19) | 31.9 (19) | 27.6 (18) |
| GPT-5.2 | 30.1 (19) | 28.9 (21) | 29.3 (19) | 29.7 (19) | 30.5 (18) | 30.9 (18) | 29.9 (19) | 33.3 (18) | 32.0 (18) | 26.9 (19) |
| DeepSeek V3.2 | 29.1 (20) | 28.5 (23) | 28.7 (22) | 28.9 (21) | 29.3 (20) | 29.5 (20) | 28.9 (21) | 31.9 (22) | 30.8 (22) | 26.3 (20) |
| MiniMax M2 | 29.0 (21) | 29.1 (19) | 29.1 (20) | 29.0 (20) | 28.9 (21) | 28.9 (22) | 29.2 (20) | 32.3 (21) | 31.0 (21) | 25.7 (21) |
| GLM-4.5 | 28.6 (22) | 29.1 (20) | 29.0 (21) | 28.8 (22) | 28.4 (25) | 28.2 (25) | 28.9 (22) | 32.5 (20) | 31.0 (20) | 24.6 (26) |
| Devstral Small 2512 | 28.6 (23) | 28.7 (22) | 28.6 (23) | 28.6 (23) | 28.5 (23) | 28.5 (23) | 28.8 (23) | 31.7 (24) | 30.5 (24) | 25.4 (24) |
| o3 | 28.4 (24) | 28.3 (24) | 28.4 (24) | 28.4 (24) | 28.4 (24) | 28.4 (24) | 28.4 (24) | 31.9 (23) | 30.5 (23) | 24.9 (25) |
| GPT-5.2 | 28.2 (25) | 27.2 (26) | 27.6 (26) | 27.9 (26) | 28.6 (22) | 28.9 (21) | 27.9 (26) | 30.8 (25) | 29.8 (25) | 25.7 (22) |
| Devstral 2512 | 28.1 (26) | 28.1 (25) | 28.1 (25) | 28.1 (25) | 28.1 (26) | 28.1 (26) | 28.3 (25) | 30.7 (26) | 29.7 (26) | 25.4 (23) |
| GLM-4.6 | 27.1 (27) | 27.1 (27) | 27.1 (27) | 27.1 (27) | 27.1 (27) | 27.1 (27) | 27.4 (27) | 30.6 (27) | 29.2 (27) | 23.6 (27) |
| Qwen3-Coder 480B | 26.1 (28) | 26.4 (28) | 26.3 (28) | 26.2 (28) | 26.0 (28) | 26.0 (28) | 26.3 (28) | 29.9 (28) | 28.4 (28) | 22.4 (28) |
| GPT-5 mini | 24.5 (29) | 24.5 (29) | 24.5 (29) | 24.5 (29) | 24.5 (29) | 24.5 (29) | 24.3 (29) | 28.0 (29) | 26.6 (29) | 21.0 (29) |
| Kimi K2 Instruct | 21.9 (30) | 22.1 (30) | 22.0 (30) | 22.0 (30) | 21.8 (30) | 21.7 (30) | 22.0 (30) | 25.2 (30) | 23.9 (30) | 18.6 (30) |
| o4-mini | 19.6 (31) | 19.1 (31) | 19.3 (31) | 19.4 (31) | 19.7 (31) | 19.9 (31) | 19.3 (31) | 24.8 (31) | 22.7 (31) | 14.3 (31) |
| GPT-5 nano | 11.8 (32) | 11.3 (32) | 11.5 (32) | 11.6 (32) | 12.0 (32) | 12.1 (32) | 12.0 (32) | 16.8 (32) | 14.8 (32) | 6.8 (32) |
| gpt-oss-120b | 6.6 (33) | 5.7 (33) | 6.0 (33) | 6.3 (33) | 6.9 (33) | 7.2 (33) | 6.6 (33) | 13.5 (33) | 10.7 (33) | -0.2 (33) |
| Llama 4 Maverick | 5.2 (34) | 5.1 (34) | 5.1 (34) | 5.2 (34) | 5.3 (34) | 5.3 (34) | 5.5 (34) | 13.0 (34) | 9.9 (34) | -2.6 (34) |
| Qwen2.5-Coder 32B | -4.3 (35) | -4.3 (35) | -4.3 (35) | -4.3 (35) | -4.4 (35) | -4.4 (35) | -4.2 (35) | 5.3 (35) | 1.4 (35) | -14.0 (35) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (1975 of 9693 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Llama 4 Maverick | 104 | 0 | none |
| Claude Sonnet 4 | 324 | 0 | GLM-4.5 22→23, Devstral Small 2512 23→22 |
| Gemini 2.5 Pro | 264 | 0 | GLM-4.5 22→23, Devstral Small 2512 23→22 |
| o3 | 292 | 0 | none |
| o4-mini | 223 | 0 | gemini-3-5-flash 14→15, GPT-5.1 15→14, GLM-4.5 22→23, Devstral Small 2512 23→22 |
| Claude Opus 4 | 337 | 0 | none |
| Qwen3-Coder 480B | 273 | 0 | none |
| Qwen2.5-Coder 32B | 43 | 0 | none |
| GPT-5 | 319 | 0 | none |
| GPT-5 nano | 173 | 0 | none |
| gpt-oss-120b | 123 | 1 | gemini-3-5-flash 14→15, GPT-5.1 15→14 |
| Kimi K2 Instruct | 216 | 0 | gemini-3-5-flash 14→15, GPT-5.1 15→14 |
| GLM-4.5 | 267 | 0 | none |
| Gemini 3 Pro (preview) | 370 | 1 | Gemini 2.5 Pro 13→14, gemini-3-5-flash 14→13 |
| GPT-5.1 | 329 | 0 | none |
| GPT-5.1 Codex | 330 | 0 | none |
| MiniMax M2 | 302 | 0 | none |
| GLM-4.6 | 273 | 0 | gemini-3-5-flash 14→15, GPT-5.1 15→14, GLM-4.5 22→23, Devstral Small 2512 23→22 |
| Devstral 2512 | 269 | 0 | none |
| Devstral Small 2512 | 280 | 0 | none |
| Kimi K2 Thinking | 314 | 0 | none |
| GPT-5.2 | 345 | 1 | gemini-3-5-flash 14→15, GPT-5.1 15→14, DeepSeek V3.2 20→21, MiniMax M2 21→20 |
| Claude Haiku 4.5 | 333 | 0 | none |
| Claude Opus 4.5 | 384 | 2 | Gemini 2.5 Pro 13→15, gemini-3-5-flash 14→13, GPT-5.1 15→14, GLM-4.5 22→23, Devstral Small 2512 23→22 |
| Claude Sonnet 4.5 | 357 | 0 | GLM-4.5 22→23, Devstral Small 2512 23→22 |
| Claude Opus 4.6 | 378 | 2 | Gemini 2.5 Pro 13→14, gemini-3-5-flash 14→13 |
| DeepSeek V3.2 | 350 | 1 | DeepSeek V3.2 20→21, MiniMax M2 21→20 |
| Gemini 3 Flash | 379 | 2 | gemini-3-5-flash 14→15, GPT-5.1 15→14, o3 24→25, GPT-5.2 25→24 |
| GLM-5 | 364 | 1 | GLM-4.5 22→23, Devstral Small 2512 23→22, o3 24→25, GPT-5.2 25→24 |
| GPT-5.2 | 364 | 0 | gemini-3-5-flash 14→15, GPT-5.1 15→14, GPT-5.2 25→26, Devstral 2512 26→25 |
| GPT-5 mini | 281 | 0 | none |
| Kimi K2.5 | 354 | 0 | gemini-3-5-flash 14→15, GPT-5.1 15→14, GLM-4.5 22→23, Devstral Small 2512 23→22 |
| MiniMax M2.5 | 379 | 2 | Gemini 2.5 Pro 13→14, gemini-3-5-flash 14→13, GLM-4.5 22→23, Devstral Small 2512 23→22 |
| (dedup panel) | 1975 | 0 | Gemini 2.5 Pro 13→15, GPT-5.1 15→13 |

Tasks that lose their only reference: gpt-oss-120b: `matplotlib__matplotlib-23299`; Gemini 3 Pro (preview): `django__django-11734`; GPT-5.2: `django__django-13195`; Claude Opus 4.5: `astropy__astropy-13033`, `django__django-12406`; Claude Opus 4.6: `pylint-dev__pylint-6528`, `pylint-dev__pylint-7277`; DeepSeek V3.2: `django__django-14792`; Gemini 3 Flash: `django__django-11400`, `django__django-16256`; GLM-5: `sympy__sympy-17630`; MiniMax M2.5: `pytest-dev__pytest-10356`, `sympy__sympy-13852`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| astropy/astropy (17) | Gemini 2.5 Pro 13→15, GPT-5.1 15→13, GLM-4.5 22→24, Devstral Small 2512 23→22, o3 24→25, GPT-5.2 25→23 |
| django/django (212) | glm-5.1-evalscope 4→5, Gemini 3 Pro (preview) 5→4, Claude Opus 4 10→13, Claude Haiku 4.5 11→12, Kimi K2 Thinking 12→15, Gemini 2.5 Pro 13→10, gemini-3-5-flash 14→20, GPT-5.1 15→11, Claude Sonnet 4 16→14, GPT-5.1 Codex 17→18, GPT-5 18→22, GPT-5.2 19→16, DeepSeek V3.2 20→24, MiniMax M2 21→19, GLM-4.5 22→21, Devstral Small 2512 23→17, o3 24→28, GPT-5.2 25→27, Devstral 2512 26→23, GLM-4.6 27→26, Qwen3-Coder 480B 28→25 |
| matplotlib/matplotlib (28) | Claude Opus 4 10→11, Claude Haiku 4.5 11→12, Kimi K2 Thinking 12→13, Gemini 2.5 Pro 13→14, gemini-3-5-flash 14→10, Claude Sonnet 4 16→17, GPT-5.1 Codex 17→16, MiniMax M2 21→24, GLM-4.5 22→23, Devstral Small 2512 23→26, o3 24→21, GPT-5.2 25→22, Devstral 2512 26→25 |
| mwaskom/seaborn (2) | glm-5.1-evalscope 4→5, Gemini 3 Pro (preview) 5→4, Gemini 2.5 Pro 13→15, gemini-3-5-flash 14→13, GPT-5.1 15→14, GLM-4.5 22→23, Devstral Small 2512 23→22 |
| pallets/flask (1) | Gemini 2.5 Pro 13→14, gemini-3-5-flash 14→13 |
| psf/requests (8) | Claude Haiku 4.5 11→12, Kimi K2 Thinking 12→11, gemini-3-5-flash 14→15, GPT-5.1 15→14, GLM-4.5 22→23, Devstral Small 2512 23→25, o3 24→22, GPT-5.2 25→24 |
| pydata/xarray (20) | Claude Opus 4 10→11, Claude Haiku 4.5 11→10, Gemini 2.5 Pro 13→15, gemini-3-5-flash 14→13, GPT-5.1 15→14, Claude Sonnet 4 16→17, GPT-5.1 Codex 17→16, GLM-4.5 22→26, o3 24→22, GPT-5.2 25→24, Devstral 2512 26→25 |
| pylint-dev/pylint (7) | Devstral Small 2512 23→24, o3 24→23 |
| pytest-dev/pytest (18) | Claude Haiku 4.5 11→12, Kimi K2 Thinking 12→11, GLM-4.5 22→23, Devstral Small 2512 23→24, o3 24→22, GPT-5.2 25→26, Devstral 2512 26→25 |
| scikit-learn/scikit-learn (32) | glm-5.1-evalscope 4→5, Gemini 3 Pro (preview) 5→4, Claude Haiku 4.5 11→12, Kimi K2 Thinking 12→11, Gemini 2.5 Pro 13→14, gemini-3-5-flash 14→13, DeepSeek V3.2 20→21, MiniMax M2 21→25, GLM-4.5 22→26, Devstral Small 2512 23→24, o3 24→23, GPT-5.2 25→20, Devstral 2512 26→22 |
| sphinx-doc/sphinx (36) | gemini-3-5-flash 14→15, GPT-5.1 15→14, GPT-5 18→19, GPT-5.2 19→18, DeepSeek V3.2 20→23, MiniMax M2 21→20, GLM-4.5 22→21, Devstral Small 2512 23→24, o3 24→22, GPT-5.2 25→26, Devstral 2512 26→25, GLM-4.6 27→28, Qwen3-Coder 480B 28→27 |
| sympy/sympy (67) | Gemini 3 Flash 7→8, GLM-5 8→7, Claude Opus 4 10→12, Claude Haiku 4.5 11→10, Kimi K2 Thinking 12→11, gemini-3-5-flash 14→15, GPT-5.1 15→14, GPT-5.2 19→22, DeepSeek V3.2 20→21, MiniMax M2 21→20, GLM-4.5 22→23, Devstral Small 2512 23→25, o3 24→26, GPT-5.2 25→19, Devstral 2512 26→24 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (448) | Solved by every model (9) | Solved by fewer (439) |
|---|---:|---:|---:|
| Claude Opus 4.5 | 51.4 (1) | 58.9 (4) | 51.2 (1) |
| Claude Opus 4.6 | 48.3 (2) | 58.9 (5) | 48.0 (2) |
| MiniMax M2.5 | 46.6 (3) | 56.9 (7) | 46.4 (3) |
| glm-5.1-evalscope | 44.4 (4) | 62.0 (1) | 44.1 (5) |
| Gemini 3 Pro (preview) | 44.1 (5) | 37.7 (34) | 44.2 (4) |
| Kimi K2.5 | 43.5 (6) | 46.0 (28) | 43.4 (6) |
| Gemini 3 Flash | 42.7 (7) | 41.7 (31) | 42.7 (7) |
| GLM-5 | 41.3 (8) | 54.1 (10) | 41.1 (8) |
| Claude Sonnet 4.5 | 38.0 (9) | 52.0 (15) | 37.7 (9) |
| Claude Opus 4 | 34.7 (10) | 52.0 (13) | 34.3 (10) |
| Claude Haiku 4.5 | 34.4 (11) | 52.0 (14) | 34.1 (11) |
| Kimi K2 Thinking | 34.1 (12) | 58.9 (3) | 33.6 (12) |
| Gemini 2.5 Pro | 33.5 (13) | 47.8 (25) | 33.2 (14) |
| gemini-3-5-flash | 33.4 (14) | 33.8 (35) | 33.4 (13) |
| GPT-5.1 | 33.4 (15) | 52.5 (12) | 33.0 (15) |
| Claude Sonnet 4 | 31.9 (16) | 48.9 (23) | 31.5 (16) |
| GPT-5.1 Codex | 31.5 (17) | 50.5 (17) | 31.1 (17) |
| GPT-5 | 30.2 (18) | 51.5 (16) | 29.8 (18) |
| GPT-5.2 | 30.1 (19) | 53.6 (11) | 29.6 (19) |
| DeepSeek V3.2 | 29.1 (20) | 49.9 (22) | 28.7 (20) |
| MiniMax M2 | 29.0 (21) | 57.8 (6) | 28.4 (21) |
| GLM-4.5 | 28.6 (22) | 50.3 (19) | 28.1 (23) |
| Devstral Small 2512 | 28.6 (23) | 45.7 (29) | 28.2 (22) |
| o3 | 28.4 (24) | 58.9 (2) | 27.8 (25) |
| GPT-5.2 | 28.2 (25) | 48.0 (24) | 27.8 (24) |
| Devstral 2512 | 28.1 (26) | 56.2 (8) | 27.5 (26) |
| GLM-4.6 | 27.1 (27) | 43.8 (30) | 26.7 (27) |
| Qwen3-Coder 480B | 26.1 (28) | 50.0 (21) | 25.6 (28) |
| GPT-5 mini | 24.5 (29) | 50.2 (20) | 24.0 (29) |
| Kimi K2 Instruct | 21.9 (30) | 41.3 (32) | 21.5 (30) |
| o4-mini | 19.6 (31) | 55.6 (9) | 18.8 (31) |
| GPT-5 nano | 11.8 (32) | 50.3 (18) | 11.0 (32) |
| gpt-oss-120b | 6.6 (33) | 47.2 (26) | 5.8 (33) |
| Llama 4 Maverick | 5.2 (34) | 40.4 (33) | 4.5 (34) |
| Qwen2.5-Coder 32B | -4.3 (35) | 46.8 (27) | -5.4 (35) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **Claude Opus 4.5 − Claude Opus 4.6 = 3.15**: failed/failed 0.04 (39), failed/solved -4.02 (24), solved/failed 4.12 (30), solved/solved 3.01 (354). For Claude Opus 4.5: `django__django-13315` +0.22 (solved/failed), `psf__requests-2931` +0.21 (solved/failed), `pydata__xarray-6938` +0.20 (solved/failed). For Claude Opus 4.6: `django__django-13925` -0.24 (failed/solved), `sympy__sympy-14976` -0.24 (failed/solved), `django__django-15957` -0.22 (failed/solved).
- **Claude Opus 4.6 − MiniMax M2.5 = 1.22**: failed/failed 0.04 (36), failed/solved -4.56 (33), solved/failed 4.75 (30), solved/solved 0.99 (346). For Claude Opus 4.6: `django__django-13406` +0.24 (solved/failed), `sympy__sympy-21612` +0.22 (solved/failed), `django__django-15973` +0.22 (solved/failed). For MiniMax M2.5: `sphinx-doc__sphinx-8056` -0.24 (failed/solved), `pylint-dev__pylint-7080` -0.23 (failed/solved), `django__django-15022` -0.23 (failed/solved).
- **MiniMax M2.5 − glm-5.1-evalscope = 2.09**: failed/failed 0.02 (41), failed/solved -3.52 (25), solved/failed 6.55 (42), solved/solved -0.96 (336). For MiniMax M2.5: `sphinx-doc__sphinx-8056` +0.25 (solved/failed), `astropy__astropy-14182` +0.23 (solved/failed), `pylint-dev__pylint-7080` +0.23 (solved/failed). For glm-5.1-evalscope: `pylint-dev__pylint-7277` -0.25 (failed/solved), `django__django-13512` -0.24 (failed/solved), `astropy__astropy-13033` -0.23 (failed/solved).
- **glm-5.1-evalscope − Gemini 3 Pro (preview) = 0.21**: failed/failed -0.05 (45), failed/solved -5.92 (40), solved/failed 4.94 (31), solved/solved 1.24 (330). For glm-5.1-evalscope: `astropy__astropy-13033` +0.25 (solved/failed), `pylint-dev__pylint-7277` +0.24 (solved/failed), `django__django-13512` +0.24 (solved/failed). For Gemini 3 Pro (preview): `django__django-15037` -0.25 (failed/solved), `django__django-12663` -0.23 (failed/solved), `django__django-11433` -0.23 (failed/solved).
- **Gemini 3 Pro (preview) − Kimi K2.5 = 0.53**: failed/failed -0.06 (52), failed/solved -3.99 (25), solved/failed 6.62 (41), solved/solved -2.04 (328). For Gemini 3 Pro (preview): `matplotlib__matplotlib-24149` +0.27 (solved/failed), `sympy__sympy-15599` +0.25 (solved/failed), `pylint-dev__pylint-6386` +0.24 (solved/failed). For Kimi K2.5: `scikit-learn__scikit-learn-25102` -0.25 (failed/solved), `sympy__sympy-15875` -0.23 (failed/solved), `sphinx-doc__sphinx-8593` -0.23 (failed/solved).
- **Kimi K2.5 − Gemini 3 Flash = 0.80**: failed/failed 0.15 (49), failed/solved -6.62 (44), solved/failed 2.98 (20), solved/solved 4.29 (334). For Kimi K2.5: `scikit-learn__scikit-learn-25102` +0.25 (solved/failed), `sympy__sympy-15875` +0.24 (solved/failed), `django__django-14725` +0.23 (solved/failed). For Gemini 3 Flash: `sympy__sympy-21379` -0.24 (failed/solved), `django__django-15563` -0.24 (failed/solved), `sympy__sympy-14248` -0.23 (failed/solved).
- **Gemini 3 Flash − GLM-5 = 1.38**: failed/failed -0.03 (48), failed/solved -3.01 (21), solved/failed 4.95 (36), solved/solved -0.52 (343). For Gemini 3 Flash: `sympy__sympy-14248` +0.23 (solved/failed), `django__django-11885` +0.23 (solved/failed), `django__django-15022` +0.22 (solved/failed). For GLM-5: `pydata__xarray-3993` -0.25 (failed/solved), `sphinx-doc__sphinx-9281` -0.24 (failed/solved), `sphinx-doc__sphinx-10435` -0.21 (failed/solved).
- **GLM-5 − Claude Sonnet 4.5 = 3.34**: failed/failed 0.13 (56), failed/solved -2.91 (27), solved/failed 5.28 (34), solved/solved 0.83 (330). For GLM-5: `sympy__sympy-21379` +0.24 (solved/failed), `sphinx-doc__sphinx-8265` +0.24 (solved/failed), `django__django-14053` +0.24 (solved/failed). For Claude Sonnet 4.5: `sphinx-doc__sphinx-8035` -0.20 (solved/solved), `sympy__sympy-15976` -0.17 (failed/solved), `pytest-dev__pytest-7205` -0.17 (failed/solved).
- **Claude Sonnet 4.5 − Claude Opus 4 = 3.61**: failed/failed -0.14 (69), failed/solved -2.70 (20), solved/failed 5.07 (40), solved/solved 1.38 (316). For Claude Sonnet 4.5: `django__django-15732` +0.21 (solved/failed), `django__django-15554` +0.21 (solved/failed), `django__django-14351` +0.21 (solved/failed). For Claude Opus 4: `django__django-13406` -0.25 (failed/solved), `sympy__sympy-12489` -0.22 (failed/solved), `django__django-13551` -0.21 (failed/solved).
- **Claude Opus 4 − Claude Haiku 4.5 = 0.35**: failed/failed 0.39 (82), failed/solved -3.18 (27), solved/failed 4.53 (33), solved/solved -1.39 (304). For Claude Opus 4: `django__django-13406` +0.25 (solved/failed), `django__django-16100` +0.24 (solved/failed), `django__django-16032` +0.23 (solved/failed). For Claude Haiku 4.5: `pytest-dev__pytest-7490` -0.25 (failed/solved), `scikit-learn__scikit-learn-13124` -0.21 (failed/solved), `psf__requests-5414` -0.21 (failed/solved).
- **Claude Haiku 4.5 − Kimi K2 Thinking = 0.20**: failed/failed -0.05 (84), failed/solved -4.44 (29), solved/failed 5.49 (44), solved/solved -0.80 (285). For Claude Haiku 4.5: `sphinx-doc__sphinx-10449` +0.25 (solved/failed), `django__django-15375` +0.24 (solved/failed), `sphinx-doc__sphinx-8551` +0.21 (solved/failed). For Kimi K2 Thinking: `django__django-13401` -0.26 (failed/solved), `sympy__sympy-13974` -0.25 (failed/solved), `sympy__sympy-19040` -0.25 (failed/solved).
- **Kimi K2 Thinking − Gemini 2.5 Pro = -1.81**: failed/failed -0.48 (86), failed/solved -6.28 (33), solved/failed 9.54 (65), solved/solved -4.59 (229). For Kimi K2 Thinking: `django__django-16560` +0.27 (solved/failed), `sympy__sympy-19040` +0.26 (solved/failed), `sympy__sympy-13974` +0.25 (solved/failed). For Gemini 2.5 Pro: `django__django-15375` -0.29 (failed/solved), `matplotlib__matplotlib-22865` -0.25 (failed/solved), `sphinx-doc__sphinx-8621` -0.25 (failed/solved).
- **Gemini 2.5 Pro − gemini-3-5-flash = 2.59**: failed/failed 0.02 (51), failed/solved -13.05 (103), solved/failed 5.80 (36), solved/solved 9.83 (228). For Gemini 2.5 Pro: `mwaskom__seaborn-3069` +0.28 (solved/failed), `sphinx-doc__sphinx-10673` +0.26 (solved/failed), `sphinx-doc__sphinx-9281` +0.24 (solved/failed). For gemini-3-5-flash: `sphinx-doc__sphinx-8593` -0.26 (failed/solved), `django__django-15916` -0.26 (failed/solved), `psf__requests-1921` -0.25 (failed/solved).
- **gemini-3-5-flash − GPT-5.1 = -0.06**: failed/failed 0.24 (52), failed/solved -4.71 (43), solved/failed 7.50 (65), solved/solved -3.08 (286). For gemini-3-5-flash: `psf__requests-1921` +0.25 (solved/failed), `sympy__sympy-17655` +0.24 (solved/failed), `django__django-15916` +0.23 (solved/failed). For GPT-5.1: `django__django-16950` -0.22 (failed/solved), `matplotlib__matplotlib-24627` -0.22 (failed/solved), `sympy__sympy-15875` -0.22 (failed/solved).
- **GPT-5.1 − Claude Sonnet 4 = 1.51**: failed/failed 0.18 (82), failed/solved -4.76 (35), solved/failed 5.55 (41), solved/solved 0.54 (287). For GPT-5.1: `scikit-learn__scikit-learn-14983` +0.26 (solved/failed), `matplotlib__matplotlib-24627` +0.25 (solved/failed), `django__django-17084` +0.22 (solved/failed). For Claude Sonnet 4: `django__django-13346` -0.21 (failed/solved), `django__django-14539` -0.21 (failed/solved), `sphinx-doc__sphinx-7440` -0.21 (failed/solved).
- **Claude Sonnet 4 − GPT-5.1 Codex = 0.48**: failed/failed -0.56 (80), failed/solved -5.62 (43), solved/failed 4.94 (38), solved/solved 1.72 (286). For Claude Sonnet 4: `scikit-learn__scikit-learn-25102` +0.21 (solved/failed), `django__django-12125` +0.21 (solved/failed), `django__django-11333` +0.21 (solved/failed). For GPT-5.1 Codex: `sympy__sympy-18211` -0.21 (failed/solved), `django__django-11964` -0.21 (failed/solved), `django__django-17084` -0.20 (failed/solved).
- **GPT-5.1 Codex − GPT-5 = 1.53**: failed/failed 0.21 (89), failed/solved -3.23 (27), solved/failed 4.02 (31), solved/solved 0.52 (292). For GPT-5.1 Codex: `django__django-16136` +0.25 (solved/failed), `matplotlib__matplotlib-20488` +0.22 (solved/failed), `sympy__sympy-18211` +0.21 (solved/failed). For GPT-5: `django__django-15916` -0.22 (failed/solved), `scikit-learn__scikit-learn-13124` -0.21 (failed/solved), `sphinx-doc__sphinx-9258` -0.19 (failed/solved).
- **GPT-5 − GPT-5.2 = -1.75**: failed/failed 0.64 (67), failed/solved -6.09 (50), solved/failed 2.13 (15), solved/solved 1.57 (289). For GPT-5: `django__django-15022` +0.24 (solved/failed), `sphinx-doc__sphinx-7454` +0.23 (solved/failed), `pylint-dev__pylint-6903` +0.21 (solved/solved). For GPT-5.2: `django__django-16136` -0.26 (failed/solved), `django__django-16454` -0.25 (failed/solved), `django__django-15280` -0.25 (failed/solved).
- **GPT-5.2 − DeepSeek V3.2 = 3.17**: failed/failed -0.05 (56), failed/solved -2.96 (26), solved/failed 4.63 (37), solved/solved 1.55 (308). For GPT-5.2: `pytest-dev__pytest-6197` +0.25 (solved/failed), `django__django-12663` +0.23 (solved/failed), `django__django-14351` +0.22 (solved/failed). For DeepSeek V3.2: `sympy__sympy-23413` -0.26 (failed/solved), `pytest-dev__pytest-10081` -0.21 (solved/solved), `django__django-15128` -0.21 (failed/solved).
- **DeepSeek V3.2 − MiniMax M2 = -0.24**: failed/failed -0.35 (65), failed/solved -3.42 (28), solved/failed 8.10 (70), solved/solved -4.56 (274). For DeepSeek V3.2: `django__django-15268` +0.25 (solved/failed), `django__django-13568` +0.23 (solved/failed), `sphinx-doc__sphinx-8459` +0.22 (solved/failed). For MiniMax M2: `sphinx-doc__sphinx-9281` -0.24 (failed/solved), `pytest-dev__pytest-7490` -0.21 (failed/solved), `django__django-14765` -0.21 (solved/solved).
- **MiniMax M2 − GLM-4.5 = 0.13**: failed/failed -0.15 (99), failed/solved -4.90 (34), solved/failed 8.14 (65), solved/solved -2.96 (229). For MiniMax M2: `django__django-13279` +0.25 (solved/failed), `django__django-14017` +0.24 (solved/failed), `django__django-15382` +0.24 (solved/failed). For GLM-4.5: `django__django-16877` -0.26 (failed/solved), `pydata__xarray-7393` -0.22 (failed/solved), `sphinx-doc__sphinx-8459` -0.22 (failed/solved).
- **GLM-4.5 − Devstral Small 2512 = 0.26**: failed/failed -0.38 (103), failed/solved -7.37 (61), solved/failed 7.29 (53), solved/solved 0.72 (210). For GLM-4.5: `sympy__sympy-24562` +0.23 (solved/failed), `scikit-learn__scikit-learn-12682` +0.23 (solved/failed), `django__django-16877` +0.23 (solved/failed). For Devstral Small 2512: `django__django-11555` -0.24 (failed/solved), `sympy__sympy-19783` -0.24 (failed/solved), `sympy__sympy-13615` -0.24 (failed/solved).
- **Devstral Small 2512 − o3 = -0.29**: failed/failed 0.06 (92), failed/solved -8.92 (66), solved/failed 6.56 (52), solved/solved 2.02 (222). For Devstral Small 2512: `pydata__xarray-3305` +0.23 (solved/failed), `matplotlib__matplotlib-26291` +0.20 (solved/failed), `sympy__sympy-19346` +0.20 (solved/failed). For o3: `django__django-17084` -0.26 (failed/solved), `django__django-15503` -0.26 (failed/solved), `sympy__sympy-13878` -0.25 (failed/solved).
- **o3 − GPT-5.2 = 0.68**: failed/failed 0.50 (59), failed/solved -9.43 (89), solved/failed 3.16 (22), solved/solved 6.45 (270). For o3: `sympy__sympy-13878` +0.25 (solved/failed), `sympy__sympy-20916` +0.23 (solved/failed), `django__django-15503` +0.23 (solved/failed). For GPT-5.2: `django__django-11265` -0.22 (failed/solved), `pytest-dev__pytest-5787` -0.22 (failed/solved), `sphinx-doc__sphinx-7454` -0.21 (failed/solved).
- **GPT-5.2 − Devstral 2512 = -0.56**: failed/failed -0.84 (59), failed/solved -3.02 (22), solved/failed 10.27 (112), solved/solved -6.97 (247). For GPT-5.2: `django__django-11265` +0.22 (solved/failed), `django__django-15467` +0.22 (solved/solved), `django__django-12304` +0.21 (solved/failed). For Devstral 2512: `sympy__sympy-12096` -0.25 (failed/solved), `django__django-16662` -0.21 (solved/solved), `pylint-dev__pylint-7080` -0.21 (failed/solved).
- **Devstral 2512 − GLM-4.6 = 1.25**: failed/failed 0.48 (107), failed/solved -7.26 (57), solved/failed 6.68 (48), solved/solved 1.35 (211). For Devstral 2512: `django__django-14311` +0.22 (solved/failed), `sympy__sympy-24066` +0.22 (solved/failed), `django__django-15280` +0.21 (solved/failed). For GLM-4.6: `scikit-learn__scikit-learn-10908` -0.27 (failed/solved), `sphinx-doc__sphinx-8056` -0.23 (failed/solved), `django__django-15375` -0.22 (failed/solved).
- **GLM-4.6 − Qwen3-Coder 480B = -0.51**: failed/failed 0.12 (97), failed/solved -7.44 (55), solved/failed 6.28 (46), solved/solved 0.53 (216). For GLM-4.6: `pytest-dev__pytest-7236` +0.25 (solved/failed), `django__django-16595` +0.25 (solved/failed), `matplotlib__matplotlib-20826` +0.24 (solved/failed). For Qwen3-Coder 480B: `django__django-12774` -0.27 (failed/solved), `scikit-learn__scikit-learn-14087` -0.26 (failed/solved), `sphinx-doc__sphinx-10673` -0.24 (failed/solved).
- **Qwen3-Coder 480B − GPT-5 mini = 2.20**: failed/solved -6.95 (54), solved/failed 7.19 (53), solved/solved 1.96 (214). For Qwen3-Coder 480B: `sympy__sympy-24562` +0.24 (solved/failed), `sympy__sympy-14531` +0.23 (solved/failed), `scikit-learn__scikit-learn-14087` +0.23 (solved/failed). For GPT-5 mini: `django__django-16595` -0.25 (failed/solved), `sympy__sympy-13878` -0.25 (failed/solved), `django__django-11239` -0.24 (failed/solved).
- **GPT-5 mini − Kimi K2 Instruct = 2.01**: failed/failed -0.66 (114), failed/solved -5.72 (39), solved/failed 10.70 (96), solved/solved -2.31 (172). For GPT-5 mini: `django__django-16595` +0.25 (solved/failed), `django__django-13012` +0.23 (solved/failed), `django__django-16082` +0.22 (solved/failed). For Kimi K2 Instruct: `sphinx-doc__sphinx-8035` -0.26 (failed/solved), `django__django-13449` -0.25 (failed/solved), `pydata__xarray-2905` -0.25 (failed/solved).
- **Kimi K2 Instruct − o4-mini = -1.16**: failed/failed 0.59 (107), failed/solved -10.05 (73), solved/failed 7.48 (42), solved/solved 0.82 (144). For Kimi K2 Instruct: `astropy__astropy-13579` +0.31 (solved/failed), `django__django-15987` +0.28 (solved/failed), `django__django-12965` +0.28 (solved/failed). For o4-mini: `django__django-15128` -0.30 (failed/solved), `matplotlib__matplotlib-24627` -0.29 (failed/solved), `django__django-13590` -0.27 (failed/solved).
- **o4-mini − GPT-5 nano = 11.29**: failed/failed -0.56 (121), failed/solved -3.49 (26), solved/failed 13.52 (84), solved/solved 1.83 (130). For o4-mini: `pylint-dev__pylint-6903` +0.30 (solved/failed), `django__django-15380` +0.28 (solved/failed), `django__django-13590` +0.27 (solved/failed). For GPT-5 nano: `sympy__sympy-21379` -0.30 (failed/solved), `pytest-dev__pytest-7205` -0.26 (solved/solved), `matplotlib__matplotlib-20826` -0.26 (failed/solved).
- **GPT-5 nano − gpt-oss-120b = 2.31**: failed/failed 0.28 (152), failed/solved -6.09 (38), solved/failed 8.74 (59), solved/solved -0.62 (82). For GPT-5 nano: `django__django-14007` +0.30 (solved/failed), `sympy__sympy-12096` +0.29 (solved/failed), `django__django-11815` +0.28 (solved/failed). For gpt-oss-120b: `sympy__sympy-23824` -0.35 (failed/solved), `scikit-learn__scikit-learn-9288` -0.29 (failed/solved), `django__django-15277` -0.28 (failed/solved).
- **gpt-oss-120b − Llama 4 Maverick = -1.90**: failed/failed -0.23 (111), failed/solved -7.10 (26), solved/failed 7.29 (35), solved/solved -1.85 (63). For gpt-oss-120b: `sympy__sympy-22456` +0.41 (solved/failed), `django__django-15987` +0.41 (solved/failed), `pytest-dev__pytest-7324` +0.35 (solved/failed). For Llama 4 Maverick: `scikit-learn__scikit-learn-26323` -0.44 (failed/solved), `django__django-12039` -0.43 (failed/solved), `django__django-13786` -0.43 (failed/solved).
- **Llama 4 Maverick − Qwen2.5-Coder 32B = 5.87**: failed/failed -0.50 (52), failed/solved -3.37 (5), solved/failed 10.30 (20), solved/solved -0.57 (33). For Llama 4 Maverick: `django__django-11951` +0.98 (solved/failed), `django__django-12039` +0.89 (solved/failed), `django__django-14500` +0.88 (solved/failed). For Qwen2.5-Coder 32B: `sphinx-doc__sphinx-10466` -0.89 (failed/solved), `sympy__sympy-18763` -0.82 (failed/solved), `scikit-learn__scikit-learn-11578` -0.70 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability examples/mini-swe-agent-500/score-panel.json examples/mini-swe-agent-500/*.jsonl --output examples/mini-swe-agent-500/sensitivity-35.json
```

All numbers are in [sensitivity-35.json](sensitivity-35.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
