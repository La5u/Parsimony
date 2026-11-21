# Score sensitivity: 17 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `swe-bench-multilingual-javascript-17`: 28 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (17 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus ≈ multilingual_rusta-kimi ≈ multilingual_rusta-deepseek ≈ multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus ≈ multilingual_20260213_mini-v2.0.0a0_gemini-3-pro ≈ multilingual_rusta-glm ≈ multilingual_20260216_mini-v2.0.0a0_minimax-2-5 ≈ multilingual_20260902_mini-v2.4.6_gemini-3-5-flash ≈ multilingual_20260213_mini-v2.0.0a0_gemini-3-flash ≈ multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 ≈ multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku ≈ multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet ≈ multilingual_20260213_mini-v2.0.0a0_glm-5 ≈ multilingual_20260220_mini-v2.0.0_gpt-5-2-codex ≈ multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 ≈ multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high > multilingual_20260213_mini-v2.0.0a0_gpt-5-mini (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (1 of 16 adjacent pairs): multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high > multilingual_20260213_mini-v2.0.0a0_gpt-5-mini.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 15 pairs): multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus vs multilingual_rusta-kimi, multilingual_rusta-kimi vs multilingual_rusta-deepseek, multilingual_rusta-deepseek vs multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus, multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus vs multilingual_20260213_mini-v2.0.0a0_gemini-3-pro, multilingual_20260213_mini-v2.0.0a0_gemini-3-pro vs multilingual_rusta-glm, multilingual_rusta-glm vs multilingual_20260216_mini-v2.0.0a0_minimax-2-5, multilingual_20260216_mini-v2.0.0a0_minimax-2-5 vs multilingual_20260902_mini-v2.4.6_gemini-3-5-flash, multilingual_20260902_mini-v2.4.6_gemini-3-5-flash vs multilingual_20260213_mini-v2.0.0a0_gemini-3-flash, multilingual_20260213_mini-v2.0.0a0_gemini-3-flash vs multilingual_20260213_mini-v2.0.0a0_kimi-k2-5, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 vs multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku vs multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet, multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet vs multilingual_20260213_mini-v2.0.0a0_glm-5, multilingual_20260213_mini-v2.0.0a0_glm-5 vs multilingual_20260220_mini-v2.0.0_gpt-5-2-codex, multilingual_20260220_mini-v2.0.0_gpt-5-2-codex vs multilingual_20260213_mini-v2.0.0a0_deepseek-3-2, multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 vs multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high.
- **Midpoint rank never changes under any variation**: multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus (1), multilingual_20260213_mini-v2.0.0a0_gpt-5-mini (17).
- Difficulty strata answer a different question and are not counted as variations; they reverse multilingual_rusta-kimi > multilingual_rusta-deepseek (solved by all); multilingual_rusta-deepseek > multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus (solved by all); multilingual_20260213_mini-v2.0.0a0_gemini-3-pro > multilingual_rusta-glm (solved by all); multilingual_20260902_mini-v2.4.6_gemini-3-5-flash > multilingual_20260213_mini-v2.0.0a0_gemini-3-flash (solved by all); multilingual_20260213_mini-v2.0.0a0_gemini-3-flash > multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 (solved by fewer); multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 > multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku (solved by all); multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet > multilingual_20260213_mini-v2.0.0a0_glm-5 (solved by all); multilingual_20260213_mini-v2.0.0a0_glm-5 > multilingual_20260220_mini-v2.0.0_gpt-5-2-codex (solved by fewer); multilingual_20260220_mini-v2.0.0_gpt-5-2-codex > multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 (solved by all); multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high > multilingual_20260213_mini-v2.0.0a0_gpt-5-mini (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 28 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus | 55.5 | 44.6–64.1 | 55.0–55.9 | 1–1 | 1.0–6.0 | 0.64 |
| 2 | multilingual_rusta-kimi | 51.3 | 39.5–61.3 | 50.8–51.7 | 2–5 | 1.0–8.0 | 0.22 |
| 3 | multilingual_rusta-deepseek | 50.2 | 37.9–61.2 | 49.8–50.7 | 2–6 | 1.0–8.0 | 0.09 |
| 4 | multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus | 48.6 | 36.0–59.4 | 48.1–49.0 | 2–4 | 1.0–9.0 | 0.04 |
| 5 | multilingual_20260213_mini-v2.0.0a0_gemini-3-pro | 41.7 | 28.3–53.6 | 41.3–42.2 | 5–9 | 2.0–11.0 | 0.01 |
| 6 | multilingual_rusta-glm | 39.4 | 26.8–50.8 | 39.0–39.9 | 6–13 | 3.0–12.0 | 0.00 |
| 7 | multilingual_20260216_mini-v2.0.0a0_minimax-2-5 | 37.8 | 16.1–59.4 | 30.7–45.0 | 3–9 | 1.0–16.0 | 0.00 |
| 8 | multilingual_20260902_mini-v2.4.6_gemini-3-5-flash | 36.6 | 12.5–59.9 | 25.5–47.8 | 7–14 | 1.0–16.0 | 0.00 |
| 9 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash | 34.7 | 21.2–46.8 | 34.2–35.1 | 7–11 | 4.0–14.0 | 0.00 |
| 10 | multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 | 34.5 | 17.6–51.2 | 31.8–37.2 | 4–12 | 2.0–15.0 | 0.00 |
| 11 | multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku | 34.4 | 18.6–49.5 | 34.0–34.9 | 7–11 | 4.0–15.0 | 0.00 |
| 12 | multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet | 31.0 | 16.6–44.1 | 30.5–31.4 | 8–12 | 5.0–16.0 | 0.00 |
| 13 | multilingual_20260213_mini-v2.0.0a0_glm-5 | 24.6 | 11.7–37.1 | 24.2–25.1 | 12–15 | 8.0–16.0 | 0.00 |
| 14 | multilingual_20260220_mini-v2.0.0_gpt-5-2-codex | 23.8 | 13.2–33.8 | 23.4–24.3 | 13–16 | 9.0–16.0 | 0.00 |
| 15 | multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 | 22.5 | 9.8–35.2 | 22.0–22.9 | 11–15 | 8.0–16.0 | 0.00 |
| 16 | multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high | 19.1 | 9.6–28.4 | 18.6–19.5 | 15–16 | 11.0–16.0 | 0.00 |
| 17 | multilingual_20260213_mini-v2.0.0a0_gpt-5-mini | 4.2 | -7.2–15.4 | 2.0–6.4 | 17–17 | 17.0–17.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus > multilingual_rusta-kimi | 4.22 | -9.48 to 17.94 | 0.68 | none | yes |
| multilingual_rusta-kimi > multilingual_rusta-deepseek | 1.05 | -8.81 to 11.91 | 0.50 | without axios/axios | yes |
| multilingual_rusta-deepseek > multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus | 1.64 | -12.70 to 16.33 | 0.55 | without mrdoob/three.js, without preactjs/preact | yes |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus > multilingual_20260213_mini-v2.0.0a0_gemini-3-pro | 6.85 | -7.35 to 20.54 | 0.80 | none | yes |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-pro > multilingual_rusta-glm | 2.31 | -10.40 to 15.31 | 0.58 | none | yes |
| multilingual_rusta-glm > multilingual_20260216_mini-v2.0.0a0_minimax-2-5 | 1.58 | -23.25 to 22.57 | 0.24 | failure cap=0, without preactjs/preact | no |
| multilingual_20260216_mini-v2.0.0a0_minimax-2-5 > multilingual_20260902_mini-v2.4.6_gemini-3-5-flash | 1.22 | -33.98 to 39.53 | 0.02 | panel dedup, without axios/axios, without immutable-js/immutable-js, without mrdoob/three.js | no |
| multilingual_20260902_mini-v2.4.6_gemini-3-5-flash > multilingual_20260213_mini-v2.0.0a0_gemini-3-flash | 1.94 | -26.05 to 27.65 | 0.11 | without preactjs/preact | no |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-flash > multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 | 0.19 | -17.13 to 17.53 | 0.32 | failure cap=0, panel without multilingual_20260213_mini-v2.0.0a0_deepseek-3-2, panel without multilingual_20260213_mini-v2.0.0a0_gemini-3-pro, panel without multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high, panel without multilingual_20260213_mini-v2.0.0a0_gpt-5-mini, panel without multilingual_20260216_mini-v2.0.0a0_minimax-2-5, panel without multilingual_20260220_mini-v2.0.0_gpt-5-2-codex, without mrdoob/three.js, without preactjs/preact | no |
| multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 > multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku | 0.09 | -16.64 to 17.14 | 0.33 | net weight=0.9, net weight=1, net floor=0, failure cap=0, failure cap=10, panel without multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet, panel without multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus, panel without multilingual_20260213_mini-v2.0.0a0_glm-5, panel without multilingual_20260902_mini-v2.4.6_gemini-3-5-flash, panel without multilingual_rusta-deepseek, panel without multilingual_rusta-glm, panel without multilingual_rusta-kimi, panel dedup, without axios/axios | no |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku > multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet | 3.44 | -13.04 to 20.50 | 0.63 | without preactjs/preact | yes |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet > multilingual_20260213_mini-v2.0.0a0_glm-5 | 6.35 | -6.26 to 18.42 | 0.82 | none | yes |
| multilingual_20260213_mini-v2.0.0a0_glm-5 > multilingual_20260220_mini-v2.0.0_gpt-5-2-codex | 0.80 | -11.70 to 13.73 | 0.48 | without axios/axios, without immutable-js/immutable-js | no |
| multilingual_20260220_mini-v2.0.0_gpt-5-2-codex > multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 | 1.33 | -11.83 to 14.78 | 0.52 | net weight=1, failure cap=0, without preactjs/preact | yes |
| multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 > multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high | 3.41 | -9.49 to 15.89 | 0.65 | none | yes |
| multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high > multilingual_20260213_mini-v2.0.0a0_gpt-5-mini | 14.89 | 4.65 to 26.20 | 1.00 | none | yes |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus | 55.5 (1) | 56.6 (1) | 56.2 (1) | 55.8 (1) | 55.1 (1) | 54.8 (1) | 55.6 (1) | 56.4 (1) | 56.0 (1) | 54.6 (1) |
| multilingual_rusta-kimi | 51.3 (2) | 51.1 (2) | 51.2 (2) | 51.2 (2) | 51.3 (2) | 51.3 (2) | 51.6 (2) | 52.6 (2) | 52.1 (2) | 49.9 (2) |
| multilingual_rusta-deepseek | 50.2 (3) | 50.7 (3) | 50.6 (3) | 50.4 (3) | 50.0 (3) | 49.9 (3) | 50.1 (3) | 51.8 (3) | 51.2 (3) | 48.6 (3) |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus | 48.6 (4) | 48.0 (4) | 48.2 (4) | 48.4 (4) | 48.8 (4) | 49.0 (4) | 48.7 (4) | 49.9 (4) | 49.4 (4) | 47.2 (4) |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-pro | 41.7 (5) | 41.5 (5) | 41.6 (5) | 41.7 (5) | 41.8 (5) | 41.9 (5) | 40.5 (5) | 43.9 (5) | 43.1 (5) | 39.5 (5) |
| multilingual_rusta-glm | 39.4 (6) | 39.6 (6) | 39.6 (6) | 39.5 (6) | 39.3 (6) | 39.3 (6) | 39.5 (6) | 41.7 (7) | 40.8 (6) | 37.1 (6) |
| multilingual_20260216_mini-v2.0.0a0_minimax-2-5 | 37.8 (7) | 38.2 (7) | 38.1 (7) | 38.0 (7) | 37.7 (7) | 37.6 (7) | 37.9 (7) | 42.4 (6) | 40.6 (7) | 33.2 (7) |
| multilingual_20260902_mini-v2.4.6_gemini-3-5-flash | 36.6 (8) | 36.5 (8) | 36.6 (8) | 36.6 (8) | 36.7 (8) | 36.7 (8) | 36.7 (8) | 40.2 (8) | 38.8 (8) | 33.1 (8) |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-flash | 34.7 (9) | 34.3 (9) | 34.4 (9) | 34.5 (9) | 34.8 (9) | 35.0 (10) | 34.8 (9) | 38.2 (11) | 36.8 (10) | 31.2 (9) |
| multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 | 34.5 (10) | 34.0 (10) | 34.2 (10) | 34.3 (10) | 34.7 (11) | 34.8 (11) | 34.5 (11) | 38.2 (10) | 36.7 (11) | 30.7 (10) |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku | 34.4 (11) | 33.4 (11) | 33.7 (11) | 34.1 (11) | 34.8 (10) | 35.1 (9) | 34.5 (10) | 38.9 (9) | 37.1 (9) | 29.9 (11) |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet | 31.0 (12) | 31.0 (12) | 31.0 (12) | 31.0 (12) | 30.9 (12) | 30.9 (12) | 31.1 (12) | 35.2 (12) | 33.5 (12) | 26.7 (12) |
| multilingual_20260213_mini-v2.0.0a0_glm-5 | 24.6 (13) | 24.9 (13) | 24.8 (13) | 24.7 (13) | 24.5 (13) | 24.4 (13) | 24.7 (13) | 28.7 (13) | 27.1 (13) | 20.5 (13) |
| multilingual_20260220_mini-v2.0.0_gpt-5-2-codex | 23.8 (14) | 24.1 (14) | 24.0 (14) | 23.9 (14) | 23.7 (14) | 23.6 (15) | 23.9 (14) | 27.3 (15) | 25.9 (14) | 20.3 (14) |
| multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 | 22.5 (15) | 20.6 (15) | 21.2 (15) | 21.8 (15) | 23.1 (15) | 23.8 (14) | 22.5 (15) | 27.5 (14) | 25.5 (15) | 17.5 (15) |
| multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high | 19.1 (16) | 19.4 (16) | 19.3 (16) | 19.2 (16) | 19.0 (16) | 18.9 (16) | 19.2 (16) | 22.6 (16) | 21.2 (16) | 15.6 (16) |
| multilingual_20260213_mini-v2.0.0a0_gpt-5-mini | 4.2 (17) | 3.9 (17) | 4.0 (17) | 4.1 (17) | 4.3 (17) | 4.4 (17) | 4.2 (17) | 11.6 (17) | 8.6 (17) | -3.2 (17) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (91 of 350 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku | 19 | 1 | none |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus | 24 | 1 | none |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet | 19 | 1 | multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus | 26 | 1 | multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 | 17 | 1 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→9 |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-flash | 20 | 1 | none |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-pro | 23 | 1 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→9 |
| multilingual_20260213_mini-v2.0.0a0_glm-5 | 18 | 1 | multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high | 22 | 1 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→11, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→9, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| multilingual_20260213_mini-v2.0.0a0_gpt-5-mini | 10 | 1 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→9 |
| multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 | 19 | 1 | none |
| multilingual_20260216_mini-v2.0.0a0_minimax-2-5 | 19 | 1 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→11, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→9, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| multilingual_20260220_mini-v2.0.0_gpt-5-2-codex | 21 | 1 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→9 |
| multilingual_20260902_mini-v2.4.6_gemini-3-5-flash | 21 | 1 | multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| multilingual_rusta-deepseek | 25 | 1 | multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→9 |
| multilingual_rusta-glm | 22 | 1 | multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| multilingual_rusta-kimi | 25 | 1 | multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10 |
| (dedup panel) | 91 | 0 | multilingual_20260216_mini-v2.0.0a0_minimax-2-5 7→8, multilingual_20260902_mini-v2.4.6_gemini-3-5-flash 8→7, multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→11, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→9 |

Tasks that lose their only reference: multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_deepseek-3-2: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_gemini-3-flash: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_gemini-3-pro: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_glm-5: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_gpt-5-mini: `axios__axios-5316#1`; multilingual_20260213_mini-v2.0.0a0_kimi-k2-5: `axios__axios-5316#1`; multilingual_20260216_mini-v2.0.0a0_minimax-2-5: `axios__axios-5316#1`; multilingual_20260220_mini-v2.0.0_gpt-5-2-codex: `axios__axios-5316#1`; multilingual_20260902_mini-v2.4.6_gemini-3-5-flash: `axios__axios-5316#1`; multilingual_rusta-deepseek: `axios__axios-5316#1`; multilingual_rusta-glm: `axios__axios-5316#1`; multilingual_rusta-kimi: `axios__axios-5316#1`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| axios/axios (6) | multilingual_rusta-kimi 2→3, multilingual_rusta-deepseek 3→2, multilingual_20260216_mini-v2.0.0a0_minimax-2-5 7→9, multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→12, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→7, multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet 12→11, multilingual_20260213_mini-v2.0.0a0_glm-5 13→15, multilingual_20260220_mini-v2.0.0_gpt-5-2-codex 14→13, multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 15→14 |
| immutable-js/immutable-js (2) | multilingual_20260216_mini-v2.0.0a0_minimax-2-5 7→8, multilingual_20260902_mini-v2.4.6_gemini-3-5-flash 8→7, multilingual_20260213_mini-v2.0.0a0_glm-5 13→14, multilingual_20260220_mini-v2.0.0_gpt-5-2-codex 14→13 |
| mrdoob/three.js (3) | multilingual_rusta-deepseek 3→4, multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus 4→3, multilingual_20260216_mini-v2.0.0a0_minimax-2-5 7→8, multilingual_20260902_mini-v2.4.6_gemini-3-5-flash 8→7, multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→10, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→9 |
| preactjs/preact (17) | multilingual_rusta-kimi 2→5, multilingual_rusta-deepseek 3→6, multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus 4→2, multilingual_20260213_mini-v2.0.0a0_gemini-3-pro 5→9, multilingual_rusta-glm 6→13, multilingual_20260216_mini-v2.0.0a0_minimax-2-5 7→3, multilingual_20260902_mini-v2.4.6_gemini-3-5-flash 8→14, multilingual_20260213_mini-v2.0.0a0_gemini-3-flash 9→7, multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 10→4, multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku 11→10, multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet 12→8, multilingual_20260213_mini-v2.0.0a0_glm-5 13→12, multilingual_20260220_mini-v2.0.0_gpt-5-2-codex 14→16, multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 15→11, multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high 16→15 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (28) | Solved by every model (4) | Solved by fewer (24) |
|---|---:|---:|---:|
| multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus | 55.5 (1) | 63.2 (3) | 54.2 (1) |
| multilingual_rusta-kimi | 51.3 (2) | 45.7 (13) | 52.2 (2) |
| multilingual_rusta-deepseek | 50.2 (3) | 58.8 (5) | 48.8 (3) |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus | 48.6 (4) | 71.2 (1) | 44.8 (4) |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-pro | 41.7 (5) | 49.3 (11) | 40.5 (5) |
| multilingual_rusta-glm | 39.4 (6) | 58.8 (6) | 36.2 (6) |
| multilingual_20260216_mini-v2.0.0a0_minimax-2-5 | 37.8 (7) | 51.5 (8) | 35.6 (7) |
| multilingual_20260902_mini-v2.4.6_gemini-3-5-flash | 36.6 (8) | 47.6 (12) | 34.8 (8) |
| multilingual_20260213_mini-v2.0.0a0_gemini-3-flash | 34.7 (9) | 58.8 (4) | 30.7 (10) |
| multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 | 34.5 (10) | 56.9 (7) | 30.8 (9) |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku | 34.4 (11) | 70.6 (2) | 28.4 (11) |
| multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet | 31.0 (12) | 49.3 (10) | 27.9 (12) |
| multilingual_20260213_mini-v2.0.0a0_glm-5 | 24.6 (13) | 51.1 (9) | 20.2 (14) |
| multilingual_20260220_mini-v2.0.0_gpt-5-2-codex | 23.8 (14) | 40.7 (15) | 21.0 (13) |
| multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 | 22.5 (15) | 42.5 (14) | 19.2 (15) |
| multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high | 19.1 (16) | 20.4 (17) | 18.9 (16) |
| multilingual_20260213_mini-v2.0.0a0_gpt-5-mini | 4.2 (17) | 22.1 (16) | 1.2 (17) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus − multilingual_rusta-kimi = 4.38**: failed/solved -2.84 (1), solved/failed 4.90 (2), solved/solved 2.32 (24). For multilingual_20260213_mini-v2.0.0a0_claude-4-6-opus: `axios__axios-6539#1` +2.60 (solved/failed), `preactjs__preact-4152#1` +2.59 (solved/solved), `axios__axios-4738#1` +2.30 (solved/failed). For multilingual_rusta-kimi: `preactjs__preact-2927#1` -2.84 (failed/solved), `preactjs__preact-3739#1` -2.36 (solved/solved), `axios__axios-5085#1` -1.47 (solved/solved).
- **multilingual_rusta-kimi − multilingual_rusta-deepseek = 1.09**: failed/failed 0.28 (2), solved/solved 0.80 (25). For multilingual_rusta-kimi: `preactjs__preact-3345#1` +2.93 (solved/solved), `preactjs__preact-4436#1` +1.63 (solved/solved), `preactjs__preact-2927#1` +1.47 (solved/solved). For multilingual_rusta-deepseek: `preactjs__preact-4152#1` -1.94 (solved/solved), `preactjs__preact-4316#1` -1.66 (solved/solved), `immutable-js__immutable-js-2005#1` -0.98 (solved/solved).
- **multilingual_rusta-deepseek − multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus = 1.70**: failed/solved -5.02 (2), solved/failed 6.46 (3), solved/solved 0.26 (22). For multilingual_rusta-deepseek: `preactjs__preact-3567#1` +3.34 (solved/failed), `preactjs__preact-3739#1` +2.75 (solved/solved), `mrdoob__three.js-25687#1` +2.48 (solved/failed). For multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus: `axios__axios-6539#1` -2.60 (failed/solved), `axios__axios-4738#1` -2.42 (failed/solved), `axios__axios-5892#1` -1.19 (solved/solved).
- **multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus − multilingual_20260213_mini-v2.0.0a0_gemini-3-pro = 7.10**: failed/failed 0.06 (3), solved/failed 2.73 (1), solved/solved 4.31 (23). For multilingual_20260213_mini-v2.0.0a0_claude-4-5-opus: `axios__axios-6539#1` +2.73 (solved/failed), `preactjs__preact-4316#1` +2.69 (solved/solved), `axios__axios-5892#1` +1.94 (solved/solved). For multilingual_20260213_mini-v2.0.0a0_gemini-3-pro: `preactjs__preact-3739#1` -2.75 (solved/solved), `preactjs__preact-4436#1` -2.04 (solved/solved), `axios__axios-4738#1` -1.39 (solved/solved).
- **multilingual_20260213_mini-v2.0.0a0_gemini-3-pro − multilingual_rusta-glm = 2.39**: failed/failed 0.10 (3), failed/solved -2.24 (1), solved/failed 4.23 (2), solved/solved 0.30 (21). For multilingual_20260213_mini-v2.0.0a0_gemini-3-pro: `axios__axios-4738#1` +3.52 (solved/failed), `preactjs__preact-4436#1` +2.44 (solved/solved), `preactjs__preact-4245#1` +1.69 (solved/solved). For multilingual_rusta-glm: `preactjs__preact-3345#1` -2.24 (failed/solved), `preactjs__preact-2757#1` -1.83 (solved/solved), `preactjs__preact-2927#1` -1.22 (solved/solved).
- **multilingual_rusta-glm − multilingual_20260216_mini-v2.0.0a0_minimax-2-5 = 5.25**: failed/failed -0.11 (2), failed/solved -2.59 (1), solved/failed 7.62 (3), solved/solved 0.33 (18). For multilingual_rusta-glm: `preactjs__preact-3689#1` +3.02 (solved/failed), `preactjs__preact-3345#1` +2.91 (solved/failed), `preactjs__preact-3010#1` +1.82 (solved/solved). For multilingual_20260216_mini-v2.0.0a0_minimax-2-5: `axios__axios-4738#1` -2.59 (failed/solved), `preactjs__preact-4436#1` -2.29 (solved/solved), `preactjs__preact-4316#1` -2.12 (solved/solved).
- **multilingual_20260216_mini-v2.0.0a0_minimax-2-5 − multilingual_20260902_mini-v2.4.6_gemini-3-5-flash = -3.37**: failed/failed -0.03 (1), failed/solved -8.76 (4), solved/solved 5.42 (16). For multilingual_20260216_mini-v2.0.0a0_minimax-2-5: `preactjs__preact-4436#1` +3.67 (solved/solved), `axios__axios-5892#1` +2.83 (solved/solved), `immutable-js__immutable-js-2005#1` +2.20 (solved/solved). For multilingual_20260902_mini-v2.4.6_gemini-3-5-flash: `preactjs__preact-3689#1` -3.45 (failed/solved), `preactjs__preact-3345#1` -2.39 (failed/solved), `preactjs__preact-3567#1` -2.09 (failed/solved).
- **multilingual_20260902_mini-v2.4.6_gemini-3-5-flash − multilingual_20260213_mini-v2.0.0a0_gemini-3-flash = 5.28**: failed/failed 0.02 (2), solved/failed 8.67 (5), solved/solved -3.42 (16). For multilingual_20260902_mini-v2.4.6_gemini-3-5-flash: `preactjs__preact-3454#1` +2.30 (solved/failed), `preactjs__preact-3345#1` +2.04 (solved/failed), `preactjs__preact-3567#1` +1.96 (solved/failed). For multilingual_20260213_mini-v2.0.0a0_gemini-3-flash: `preactjs__preact-3562#1` -2.65 (solved/solved), `mrdoob__three.js-26589#1` -2.15 (solved/solved), `preactjs__preact-4182#1` -1.32 (solved/solved).
- **multilingual_20260213_mini-v2.0.0a0_gemini-3-flash − multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 = -3.28**: failed/failed -0.24 (5), failed/solved -5.52 (2), solved/failed 1.71 (1), solved/solved 0.77 (17). For multilingual_20260213_mini-v2.0.0a0_gemini-3-flash: `preactjs__preact-3562#1` +2.13 (solved/solved), `mrdoob__three.js-26589#1` +1.98 (solved/solved), `preactjs__preact-4245#1` +1.71 (solved/failed). For multilingual_20260213_mini-v2.0.0a0_kimi-k2-5: `immutable-js__immutable-js-2005#1` -3.51 (solved/solved), `preactjs__preact-4436#1` -3.40 (failed/solved), `preactjs__preact-3454#1` -2.12 (failed/solved).
- **multilingual_20260213_mini-v2.0.0a0_kimi-k2-5 − multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku = 0.54**: failed/failed 0.35 (5), failed/solved -0.79 (1), solved/failed 6.34 (2), solved/solved -5.35 (17). For multilingual_20260213_mini-v2.0.0a0_kimi-k2-5: `preactjs__preact-4436#1` +3.45 (solved/failed), `preactjs__preact-2896#1` +2.89 (solved/failed), `axios__axios-4738#1` +2.02 (solved/solved). For multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku: `preactjs__preact-3562#1` -3.35 (solved/solved), `preactjs__preact-4152#1` -2.28 (solved/solved), `mrdoob__three.js-26589#1` -1.98 (solved/solved).
- **multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku − multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet = 3.57**: failed/failed -0.04 (6), failed/solved -6.34 (2), solved/failed 7.51 (2), solved/solved 2.44 (17). For multilingual_20260213_mini-v2.0.0a0_claude-4-5-haiku: `preactjs__preact-3562#1` +3.90 (solved/failed), `preactjs__preact-3739#1` +3.61 (solved/failed), `preactjs__preact-4152#1` +3.24 (solved/solved). For multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet: `preactjs__preact-4182#1` -3.67 (failed/solved), `preactjs__preact-2896#1` -2.67 (failed/solved), `preactjs__preact-4245#1` -1.97 (solved/solved).
- **multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet − multilingual_20260213_mini-v2.0.0a0_glm-5 = 6.58**: failed/failed -0.46 (6), failed/solved -4.29 (2), solved/failed 5.94 (3), solved/solved 5.39 (16). For multilingual_20260213_mini-v2.0.0a0_claude-4-5-sonnet: `preactjs__preact-2927#1` +3.01 (solved/solved), `preactjs__preact-4245#1` +2.93 (solved/failed), `mrdoob__three.js-26589#1` +1.83 (solved/solved). For multilingual_20260213_mini-v2.0.0a0_glm-5: `preactjs__preact-2757#1` -2.64 (failed/solved), `preactjs__preact-3739#1` -1.64 (failed/solved), `axios__axios-5085#1` -0.78 (solved/solved).
- **multilingual_20260213_mini-v2.0.0a0_glm-5 − multilingual_20260220_mini-v2.0.0_gpt-5-2-codex = 0.83**: failed/failed 0.40 (4), failed/solved -6.37 (5), solved/failed 3.45 (2), solved/solved 3.35 (16). For multilingual_20260213_mini-v2.0.0a0_glm-5: `preactjs__preact-4182#1` +2.96 (solved/solved), `axios__axios-5892#1` +2.52 (solved/solved), `immutable-js__immutable-js-2005#1` +2.34 (solved/failed). For multilingual_20260220_mini-v2.0.0_gpt-5-2-codex: `preactjs__preact-4245#1` -2.37 (failed/solved), `mrdoob__three.js-26589#1` -1.83 (solved/solved), `preactjs__preact-3062#1` -1.48 (failed/solved).
- **multilingual_20260220_mini-v2.0.0_gpt-5-2-codex − multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 = 1.38**: failed/failed -0.07 (4), failed/solved -4.77 (2), solved/failed 9.53 (6), solved/solved -3.31 (15). For multilingual_20260220_mini-v2.0.0_gpt-5-2-codex: `preactjs__preact-3763#1` +2.69 (solved/failed), `preactjs__preact-3739#1` +2.31 (solved/failed), `preactjs__preact-4245#1` +2.27 (solved/failed). For multilingual_20260213_mini-v2.0.0a0_deepseek-3-2: `mrdoob__three.js-25687#1` -2.43 (failed/solved), `immutable-js__immutable-js-2005#1` -2.34 (failed/solved), `axios__axios-4731#1` -2.20 (solved/solved).
- **multilingual_20260213_mini-v2.0.0a0_deepseek-3-2 − multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high = 3.53**: failed/failed 0.30 (4), failed/solved -6.89 (6), solved/failed 2.42 (1), solved/solved 7.70 (16). For multilingual_20260213_mini-v2.0.0a0_deepseek-3-2: `axios__axios-4731#1` +2.64 (solved/solved), `mrdoob__three.js-25687#1` +2.42 (solved/failed), `preactjs__preact-3010#1` +1.83 (solved/solved). For multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high: `preactjs__preact-3763#1` -2.69 (failed/solved), `axios__axios-5085#1` -1.81 (solved/solved), `preactjs__preact-4245#1` -1.14 (failed/solved).
- **multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high − multilingual_20260213_mini-v2.0.0a0_gpt-5-mini = 13.01**: failed/failed -0.55 (4), solved/failed 11.85 (9), solved/solved 1.70 (10). For multilingual_20260213_mini-v2.0.0a0_gpt-5-2-high: `preactjs__preact-2896#1` +2.26 (solved/failed), `preactjs__preact-3562#1` +2.23 (solved/failed), `preactjs__preact-2757#1` +2.06 (solved/failed). For multilingual_20260213_mini-v2.0.0a0_gpt-5-mini: `preactjs__preact-3345#1` -0.60 (failed/failed), `preactjs__preact-4152#1` -0.56 (solved/solved), `axios__axios-6539#1` -0.02 (failed/failed).

## Regenerate

```sh
python -m parsimony.stability /home/lasu/coding/parsimony/examples/multilingual-javascript/score-panel.json /home/lasu/coding/parsimony/examples/multilingual-javascript/*.jsonl --output /home/lasu/coding/parsimony/examples/multilingual-javascript/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
