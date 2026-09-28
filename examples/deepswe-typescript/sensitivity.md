# Score sensitivity: 26 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `deepswe-v1.1-typescript-26-pooled-80-20-v0.6`: 124 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (70 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Fable 5 (xhigh) ≈ Kimi K3 (max) ≈ Claude Opus 4.8 (max) ≈ GPT-5.6 Sol (max) ≈ GPT-5.6 Terra (max) ≈ DeepSeek V4 Pro (max) ≈ GLM-5.3 (max) ≈ Grok 4.6 (medium) ≈ GPT-5.6 Luna (max) ≈ Qwen3.8 Max (xhigh) ≈ GLM-5.2 (max) ≈ Claude Opus 5 (max) ≈ Claude Sonnet 5 (max) ≈ GPT-5.5 (xhigh) ≈ DeepSeek V4 Flash (max) ≈ GLM-5.3 Flash (max) ≈ Grok 4.5 (high) ≈ Gemini 3.7 Flash (medium) ≈ Kimi K2.7 Code ≈ Gemini 3.5 Flash (high) ≈ Gemini 3.6 Flash (high) ≈ Claude Sonnet 4.6 (high) ≈ GPT-5.4 (xhigh) ≈ Muse Spark 1.1 (xhigh) ≈ Muse Spark 1.2 (xhigh) ≈ Gemini 3.1 Pro Preview (high) (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (0 of 25 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 25 pairs): Claude Fable 5 (xhigh) vs Kimi K3 (max), Kimi K3 (max) vs Claude Opus 4.8 (max), Claude Opus 4.8 (max) vs GPT-5.6 Sol (max), GPT-5.6 Sol (max) vs GPT-5.6 Terra (max), GPT-5.6 Terra (max) vs DeepSeek V4 Pro (max), DeepSeek V4 Pro (max) vs GLM-5.3 (max), GLM-5.3 (max) vs Grok 4.6 (medium), Grok 4.6 (medium) vs GPT-5.6 Luna (max), GPT-5.6 Luna (max) vs Qwen3.8 Max (xhigh), Qwen3.8 Max (xhigh) vs GLM-5.2 (max), GLM-5.2 (max) vs Claude Opus 5 (max), Claude Opus 5 (max) vs Claude Sonnet 5 (max), Claude Sonnet 5 (max) vs GPT-5.5 (xhigh), GPT-5.5 (xhigh) vs DeepSeek V4 Flash (max), DeepSeek V4 Flash (max) vs GLM-5.3 Flash (max), GLM-5.3 Flash (max) vs Grok 4.5 (high), Grok 4.5 (high) vs Gemini 3.7 Flash (medium), Gemini 3.7 Flash (medium) vs Kimi K2.7 Code, Kimi K2.7 Code vs Gemini 3.5 Flash (high), Gemini 3.5 Flash (high) vs Gemini 3.6 Flash (high), Gemini 3.6 Flash (high) vs Claude Sonnet 4.6 (high), Claude Sonnet 4.6 (high) vs GPT-5.4 (xhigh), GPT-5.4 (xhigh) vs Muse Spark 1.1 (xhigh), Muse Spark 1.1 (xhigh) vs Muse Spark 1.2 (xhigh), Muse Spark 1.2 (xhigh) vs Gemini 3.1 Pro Preview (high).
- **Rank never changes under any variation**: Claude Fable 5 (xhigh) (1), Kimi K3 (max) (2), GPT-5.6 Terra (max) (5), Muse Spark 1.1 (xhigh) (24), Muse Spark 1.2 (xhigh) (25), Gemini 3.1 Pro Preview (high) (26).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 124 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Fable 5 (xhigh) | 43.3 | 29.4–57.6 | 41.7–44.9 | 1–1 | 1–3 | 0.91 |
| 2 | Kimi K3 (max) | 34.8 | 23.0–46.4 | 33.2–36.4 | 2–2 | 1–8 | 0.03 |
| 3 | Claude Opus 4.8 (max) | 32.8 | 16.3–49.9 | 28.1–37.4 | 3–4 | 2–9 | 0.01 |
| 4 | GPT-5.6 Sol (max) | 30.8 | 16.9–46.2 | 27.6–34.0 | 3–4 | 2–10 | 0.02 |
| 5 | GPT-5.6 Terra (max) | 28.5 | 16.2–42.1 | 26.3–30.7 | 5–5 | 2–13 | 0.01 |
| 6 | DeepSeek V4 Pro (max) | 26.2 | 14.4–39.8 | 23.3–29.1 | 6–8 | 3–15 | 0.00 |
| 7 | GLM-5.3 (max) | 25.8 | 15.2–36.3 | 24.6–27.0 | 6–10 | 3–17 | 0.00 |
| 8 | Grok 4.6 (medium) | 25.5 | 13.0–39.9 | 22.9–28.1 | 6–10 | 3–18 | 0.00 |
| 9 | GPT-5.6 Luna (max) | 23.9 | 10.0–38.6 | 20.0–27.8 | 8–13 | 3–19 | 0.00 |
| 10 | Qwen3.8 Max (xhigh) | 23.7 | 12.2–34.8 | 21.2–26.2 | 8–13 | 5–17 | 0.00 |
| 11 | GLM-5.2 (max) | 23.3 | 14.9–31.6 | 23.3 | 7–14 | 4–17 | 0.00 |
| 12 | Claude Opus 5 (max) | 22.8 | 11.3–36.4 | 19.7–26.0 | 9–15 | 5–19 | 0.00 |
| 13 | Claude Sonnet 5 (max) | 22.4 | 12.5–31.9 | 21.0–23.8 | 10–15 | 4–20 | 0.00 |
| 14 | GPT-5.5 (xhigh) | 22.3 | 9.8–36.7 | 19.0–25.6 | 10–15 | 5–20 | 0.00 |
| 15 | DeepSeek V4 Flash (max) | 21.2 | 10.4–33.2 | 19.4–23.0 | 13–15 | 6–20 | 0.00 |
| 16 | GLM-5.3 Flash (max) | 19.1 | 8.8–30.5 | 16.9–21.3 | 16–17 | 8–22 | 0.00 |
| 17 | Grok 4.5 (high) | 17.5 | 7.7–27.5 | 16.9–18.1 | 17–18 | 10–23 | 0.00 |
| 18 | Gemini 3.7 Flash (medium) | 17.2 | 9.6–26.6 | 16.0–18.4 | 16–19 | 11–21 | 0.00 |
| 19 | Kimi K2.7 Code | 15.0 | 4.3–25.8 | 14.3–15.7 | 18–21 | 9–24 | 0.00 |
| 20 | Gemini 3.5 Flash (high) | 14.4 | 5.0–24.8 | 13.9–14.9 | 19–22 | 11–24 | 0.00 |
| 21 | Gemini 3.6 Flash (high) | 14.1 | 5.7–23.1 | 13.6–14.6 | 19–21 | 14–24 | 0.00 |
| 22 | Claude Sonnet 4.6 (high) | 12.0 | 2.5–22.1 | 11.2–12.8 | 21–23 | 14–26 | 0.00 |
| 23 | GPT-5.4 (xhigh) | 10.1 | 1.6–19.4 | 8.8–11.4 | 22–23 | 18–26 | 0.00 |
| 24 | Muse Spark 1.1 (xhigh) | 7.7 | -0.9–17.3 | 6.5–8.9 | 24–24 | 19–26 | 0.00 |
| 25 | Muse Spark 1.2 (xhigh) | 6.8 | -1.2–15.2 | 5.0–8.6 | 25–25 | 22–26 | 0.00 |
| 26 | Gemini 3.1 Pro Preview (high) | 2.4 | -5.7–11.2 | 1.6–3.2 | 26–26 | 23–26 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Fable 5 (xhigh) > Kimi K3 (max) | 8.48 | -5.13 to 22.58 | 0.85 | none | yes |
| Kimi K3 (max) > Claude Opus 4.8 (max) | 2.07 | -16.74 to 18.73 | 0.25 | none | no |
| Claude Opus 4.8 (max) > GPT-5.6 Sol (max) | 1.99 | -19.00 to 22.19 | 0.18 | without dynamodb-toolbox/dynamodb-toolbox | no |
| GPT-5.6 Sol (max) > GPT-5.6 Terra (max) | 2.25 | -13.41 to 17.19 | 0.28 | none | no |
| GPT-5.6 Terra (max) > DeepSeek V4 Pro (max) | 2.33 | -14.84 to 19.51 | 0.31 | none | no |
| DeepSeek V4 Pro (max) > GLM-5.3 (max) | 0.42 | -14.82 to 17.46 | 0.28 | net weight=1, failure cap=50, panel without Claude Fable 5 (xhigh), without TanStack/query, without baryhuang/claude-code-by-agents, without dynamodb-toolbox/dynamodb-toolbox, without eicrud/eicrud, without jeffijoe/awilix, without open-circle/valibot, without slab/quill, without vadimdemedes/ink, without vitest-dev/vitest | no |
| GLM-5.3 (max) > Grok 4.6 (medium) | 0.29 | -14.91 to 13.37 | 0.28 | net weight=0.5, failure cap=0, failure cap=10, panel without GPT-5.6 Sol (max), panel without Muse Spark 1.2 (xhigh), without TanStack/query, without bombshell-dev/clack, without capricorn86/happy-dom, without dahlia/optique, without gvergnaud/ts-pattern, without platers/obsidian-linter, without pmndrs/koota, without slab/quill, without sql-formatter-org/sql-formatter | no |
| Grok 4.6 (medium) > GPT-5.6 Luna (max) | 1.60 | -17.60 to 22.22 | 0.22 | without arktypeio/arktype, without dynamodb-toolbox/dynamodb-toolbox, without kysely-org/kysely | no |
| GPT-5.6 Luna (max) > Qwen3.8 Max (xhigh) | 0.17 | -18.65 to 18.92 | 0.16 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, panel without Claude Fable 5 (xhigh), panel without Claude Opus 4.8 (max), panel without DeepSeek V4 Pro (max), panel without Kimi K3 (max), panel without Muse Spark 1.1 (xhigh), without TanStack/query, without baryhuang/claude-code-by-agents, without drizzle-team/drizzle-orm, without flightcontrolhq/superjson, without gvergnaud/ts-pattern, without jeffijoe/awilix, without meriyah/meriyah, without open-circle/valibot, without pmndrs/koota, without slab/quill, without sql-formatter-org/sql-formatter | no |
| Qwen3.8 Max (xhigh) > GLM-5.2 (max) | 0.37 | -11.59 to 12.83 | 0.30 | net weight=0.5, failure cap=50, without arktypeio/arktype, without capricorn86/happy-dom, without dahlia/optique, without flightcontrolhq/superjson, without kysely-org/kysely, without platers/obsidian-linter, without pmndrs/koota, without true-myth/true-myth, without unjs/ofetch | no |
| GLM-5.2 (max) > Claude Opus 5 (max) | 0.49 | -14.60 to 13.92 | 0.33 | failure cap=50, without TanStack/query, without baryhuang/claude-code-by-agents, without drizzle-team/drizzle-orm, without eicrud/eicrud, without jeffijoe/awilix, without open-circle/valibot, without sql-formatter-org/sql-formatter, without vadimdemedes/ink | no |
| Claude Opus 5 (max) > Claude Sonnet 5 (max) | 0.47 | -13.31 to 14.83 | 0.19 | without eicrud/eicrud, without gvergnaud/ts-pattern, without open-circle/valibot, without platers/obsidian-linter, without pmndrs/koota, without unjs/ofetch | no |
| Claude Sonnet 5 (max) > GPT-5.5 (xhigh) | 0.12 | -17.02 to 15.87 | 0.25 | net weight=1, failure cap=50, panel without GLM-5.3 (max), panel without GPT-5.6 Sol (max), panel without Grok 4.6 (medium), without TanStack/query, without arktypeio/arktype, without bombshell-dev/clack, without c4spar/cliffy, without capricorn86/happy-dom, without dahlia/optique, without gvergnaud/ts-pattern, without platers/obsidian-linter, without slab/quill, without unjs/ofetch, without vadimdemedes/ink, without vitest-dev/vitest | no |
| GPT-5.5 (xhigh) > DeepSeek V4 Flash (max) | 1.05 | -16.74 to 19.04 | 0.26 | without flightcontrolhq/superjson, without jeffijoe/awilix, without kysely-org/kysely, without meriyah/meriyah, without open-circle/valibot | no |
| DeepSeek V4 Flash (max) > GLM-5.3 Flash (max) | 2.12 | -12.71 to 17.12 | 0.37 | none | no |
| GLM-5.3 Flash (max) > Grok 4.5 (high) | 1.59 | -9.48 to 13.61 | 0.40 | none | no |
| Grok 4.5 (high) > Gemini 3.7 Flash (medium) | 0.28 | -12.77 to 12.33 | 0.39 | failure cap=50, without arktypeio/arktype, without c4spar/cliffy, without capricorn86/happy-dom, without drizzle-team/drizzle-orm, without jeffijoe/awilix, without open-circle/valibot, without slab/quill, without true-myth/true-myth, without unjs/ofetch, without vadimdemedes/ink | no |
| Gemini 3.7 Flash (medium) > Kimi K2.7 Code | 2.22 | -10.50 to 15.86 | 0.53 | failure cap=0, without pmndrs/koota | yes |
| Kimi K2.7 Code > Gemini 3.5 Flash (high) | 0.56 | -12.75 to 13.22 | 0.45 | failure cap=50, without arktypeio/arktype, without dahlia/optique, without drizzle-team/drizzle-orm, without eicrud/eicrud, without jeffijoe/awilix, without true-myth/true-myth, without vadimdemedes/ink | no |
| Gemini 3.5 Flash (high) > Gemini 3.6 Flash (high) | 0.32 | -9.45 to 9.72 | 0.44 | net weight=1, failure cap=50, without TanStack/query, without baryhuang/claude-code-by-agents, without dynamodb-toolbox/dynamodb-toolbox, without kysely-org/kysely, without meriyah/meriyah, without pmndrs/koota, without slab/quill, without true-myth/true-myth, without unjs/ofetch | no |
| Gemini 3.6 Flash (high) > Claude Sonnet 4.6 (high) | 2.11 | -9.11 to 13.06 | 0.57 | none | yes |
| Claude Sonnet 4.6 (high) > GPT-5.4 (xhigh) | 1.91 | -11.29 to 15.98 | 0.49 | without c4spar/cliffy | no |
| GPT-5.4 (xhigh) > Muse Spark 1.1 (xhigh) | 2.38 | -9.10 to 13.61 | 0.49 | none | no |
| Muse Spark 1.1 (xhigh) > Muse Spark 1.2 (xhigh) | 0.96 | -7.44 to 10.32 | 0.22 | none | no |
| Muse Spark 1.2 (xhigh) > Gemini 3.1 Pro Preview (high) | 4.36 | -5.20 to 14.96 | 0.69 | none | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 43.3 (1) | 43.7 (1) | 43.6 (1) | 43.4 (1) | 43.2 (1) | 43.0 (1) | 43.3 (1) | 47.2 (1) | 45.6 (1) | 39.4 (1) |
| Kimi K3 (max) | 34.8 (2) | 35.5 (2) | 35.3 (2) | 35.0 (2) | 34.6 (2) | 34.4 (2) | 34.8 (2) | 38.9 (2) | 37.2 (2) | 30.8 (2) |
| Claude Opus 4.8 (max) | 32.8 (3) | 33.1 (3) | 33.0 (3) | 32.9 (3) | 32.6 (3) | 32.5 (3) | 32.8 (3) | 38.5 (3) | 36.2 (3) | 27.0 (3) |
| GPT-5.6 Sol (max) | 30.8 (4) | 29.6 (4) | 30.0 (4) | 30.4 (4) | 31.1 (4) | 31.5 (4) | 30.8 (4) | 34.9 (4) | 33.2 (4) | 26.7 (4) |
| GPT-5.6 Terra (max) | 28.5 (5) | 27.8 (5) | 28.1 (5) | 28.3 (5) | 28.7 (5) | 29.0 (5) | 28.5 (5) | 32.8 (5) | 31.1 (5) | 24.2 (5) |
| DeepSeek V4 Pro (max) | 26.2 (6) | 26.5 (6) | 26.4 (6) | 26.3 (6) | 26.1 (6) | 26.0 (7) | 26.2 (6) | 31.0 (6) | 29.1 (6) | 21.4 (7) |
| GLM-5.3 (max) | 25.8 (7) | 25.4 (8) | 25.5 (7) | 25.7 (7) | 25.9 (7) | 26.0 (6) | 25.8 (7) | 29.8 (8) | 28.2 (8) | 21.7 (6) |
| Grok 4.6 (medium) | 25.5 (8) | 25.5 (7) | 25.5 (8) | 25.5 (8) | 25.5 (8) | 25.5 (8) | 25.5 (8) | 30.6 (7) | 28.6 (7) | 20.3 (8) |
| GPT-5.6 Luna (max) | 23.9 (9) | 23.4 (11) | 23.6 (10) | 23.7 (9) | 24.0 (9) | 24.2 (9) | 23.9 (9) | 29.1 (10) | 27.0 (10) | 18.6 (9) |
| Qwen3.8 Max (xhigh) | 23.7 (10) | 23.6 (10) | 23.6 (9) | 23.7 (10) | 23.7 (10) | 23.8 (10) | 23.7 (10) | 29.5 (9) | 27.2 (9) | 17.9 (12) |
| GLM-5.2 (max) | 23.3 (11) | 23.6 (9) | 23.5 (11) | 23.4 (11) | 23.2 (11) | 23.1 (11) | 23.3 (11) | 28.7 (11) | 26.6 (11) | 17.9 (11) |
| Claude Opus 5 (max) | 22.8 (12) | 22.9 (12) | 22.9 (12) | 22.9 (12) | 22.8 (12) | 22.8 (12) | 22.8 (12) | 27.7 (12) | 25.7 (12) | 18.0 (10) |
| Claude Sonnet 5 (max) | 22.4 (13) | 22.0 (13) | 22.2 (13) | 22.3 (13) | 22.5 (13) | 22.6 (14) | 22.4 (13) | 27.6 (13) | 25.5 (13) | 17.1 (14) |
| GPT-5.5 (xhigh) | 22.3 (14) | 21.6 (14) | 21.8 (14) | 22.0 (14) | 22.5 (14) | 22.7 (13) | 22.3 (14) | 27.3 (14) | 25.3 (14) | 17.2 (13) |
| DeepSeek V4 Flash (max) | 21.2 (15) | 21.6 (15) | 21.5 (15) | 21.3 (15) | 21.1 (15) | 21.0 (15) | 21.2 (15) | 27.0 (15) | 24.7 (15) | 15.4 (15) |
| GLM-5.3 Flash (max) | 19.1 (16) | 19.4 (16) | 19.3 (16) | 19.2 (16) | 19.0 (16) | 18.9 (16) | 19.1 (16) | 24.8 (16) | 22.5 (16) | 13.4 (16) |
| Grok 4.5 (high) | 17.5 (17) | 17.4 (17) | 17.4 (17) | 17.4 (17) | 17.5 (17) | 17.6 (17) | 17.5 (17) | 23.8 (17) | 21.3 (17) | 11.2 (18) |
| Gemini 3.7 Flash (medium) | 17.2 (18) | 16.9 (18) | 17.0 (18) | 17.1 (18) | 17.3 (18) | 17.4 (18) | 17.2 (18) | 21.9 (19) | 20.0 (18) | 12.6 (17) |
| Kimi K2.7 Code | 15.0 (19) | 14.9 (19) | 14.9 (19) | 15.0 (19) | 15.0 (19) | 15.1 (19) | 15.0 (19) | 22.7 (18) | 19.6 (19) | 7.3 (21) |
| Gemini 3.5 Flash (high) | 14.4 (20) | 14.8 (20) | 14.7 (20) | 14.6 (20) | 14.3 (20) | 14.2 (21) | 14.4 (20) | 21.4 (20) | 18.6 (20) | 7.5 (20) |
| Gemini 3.6 Flash (high) | 14.1 (21) | 13.9 (21) | 13.9 (21) | 14.0 (21) | 14.2 (21) | 14.3 (20) | 14.1 (21) | 20.7 (21) | 18.0 (21) | 7.5 (19) |
| Claude Sonnet 4.6 (high) | 12.0 (22) | 12.2 (22) | 12.2 (22) | 12.1 (22) | 11.9 (22) | 11.8 (22) | 12.0 (22) | 19.7 (22) | 16.6 (22) | 4.3 (22) |
| GPT-5.4 (xhigh) | 10.1 (23) | 9.4 (23) | 9.6 (23) | 9.8 (23) | 10.3 (23) | 10.6 (23) | 10.1 (23) | 16.8 (23) | 14.1 (23) | 3.3 (23) |
| Muse Spark 1.1 (xhigh) | 7.7 (24) | 7.6 (24) | 7.7 (24) | 7.7 (24) | 7.7 (24) | 7.8 (24) | 7.7 (24) | 14.7 (24) | 11.9 (24) | 0.8 (24) |
| Muse Spark 1.2 (xhigh) | 6.8 (25) | 7.1 (25) | 7.0 (25) | 6.9 (25) | 6.6 (25) | 6.5 (25) | 6.8 (25) | 12.8 (25) | 10.4 (25) | 0.7 (25) |
| Gemini 3.1 Pro Preview (high) | 2.4 (26) | 2.4 (26) | 2.4 (26) | 2.4 (26) | 2.4 (26) | 2.4 (26) | 2.4 (26) | 10.0 (26) | 7.0 (26) | -5.2 (26) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (0 of 6372 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Fable 5 (xhigh) | 304 | 0 | DeepSeek V4 Pro (max) 6→7, GLM-5.3 (max) 7→6, GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9 |
| Claude Opus 4.8 (max) | 240 | 0 | GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9 |
| Claude Opus 5 (max) | 292 | 0 | none |
| Claude Sonnet 4.6 (high) | 156 | 0 | none |
| Claude Sonnet 5 (max) | 240 | 0 | none |
| DeepSeek V4 Flash (max) | 240 | 0 | none |
| DeepSeek V4 Pro (max) | 292 | 0 | GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9 |
| Gemini 3.1 Pro Preview (high) | 64 | 0 | none |
| Gemini 3.5 Flash (high) | 180 | 0 | none |
| Gemini 3.6 Flash (high) | 208 | 0 | none |
| Gemini 3.7 Flash (medium) | 300 | 0 | none |
| GLM-5.2 (max) | 220 | 0 | none |
| GLM-5.3 Flash (max) | 240 | 0 | none |
| GLM-5.3 (max) | 300 | 0 | Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→13 |
| GPT-5.4 (xhigh) | 232 | 0 | none |
| GPT-5.5 (xhigh) | 276 | 0 | none |
| GPT-5.6 Luna (max) | 288 | 0 | none |
| GPT-5.6 Sol (max) | 300 | 0 | GLM-5.3 (max) 7→8, Grok 4.6 (medium) 8→7, Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→13 |
| GPT-5.6 Terra (max) | 312 | 0 | none |
| Grok 4.5 (high) | 236 | 0 | none |
| Grok 4.6 (medium) | 264 | 0 | Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→13 |
| Kimi K2.7 Code | 148 | 0 | none |
| Kimi K3 (max) | 288 | 0 | GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9 |
| Muse Spark 1.1 (xhigh) | 244 | 0 | GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9 |
| Muse Spark 1.2 (xhigh) | 256 | 0 | GLM-5.3 (max) 7→8, Grok 4.6 (medium) 8→7 |
| Qwen3.8 Max (xhigh) | 252 | 0 | none |
| (dedup panel) | 0 | 0 | none |

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| TanStack/query (4) | DeepSeek V4 Pro (max) 6→8, Grok 4.6 (medium) 8→6, GPT-5.6 Luna (max) 9→13, GLM-5.2 (max) 11→14, Claude Opus 5 (max) 12→9, Claude Sonnet 5 (max) 13→12, GPT-5.5 (xhigh) 14→11, Gemini 3.5 Flash (high) 20→21, Gemini 3.6 Flash (high) 21→20 |
| arktypeio/arktype (4) | Grok 4.6 (medium) 8→9, GPT-5.6 Luna (max) 9→8, Qwen3.8 Max (xhigh) 10→11, GLM-5.2 (max) 11→10, Claude Opus 5 (max) 12→13, Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→12, GLM-5.3 Flash (max) 16→17, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→16, Kimi K2.7 Code 19→20, Gemini 3.5 Flash (high) 20→19 |
| baryhuang/claude-code-by-agents (4) | DeepSeek V4 Pro (max) 6→7, GLM-5.3 (max) 7→6, GPT-5.6 Luna (max) 9→12, Qwen3.8 Max (xhigh) 10→9, GLM-5.2 (max) 11→14, Claude Opus 5 (max) 12→10, Claude Sonnet 5 (max) 13→11, GPT-5.5 (xhigh) 14→13, Gemini 3.5 Flash (high) 20→21, Gemini 3.6 Flash (high) 21→20 |
| bombshell-dev/clack (4) | GLM-5.3 (max) 7→8, Grok 4.6 (medium) 8→7, Claude Opus 5 (max) 12→13, Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→12 |
| c4spar/cliffy (4) | GLM-5.2 (max) 11→12, Claude Opus 5 (max) 12→13, Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→11, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17, Claude Sonnet 4.6 (high) 22→23, GPT-5.4 (xhigh) 23→22 |
| capricorn86/happy-dom (8) | GLM-5.3 (max) 7→9, Grok 4.6 (medium) 8→7, GPT-5.6 Luna (max) 9→8, Qwen3.8 Max (xhigh) 10→12, GLM-5.2 (max) 11→10, Claude Opus 5 (max) 12→14, Claude Sonnet 5 (max) 13→15, GPT-5.5 (xhigh) 14→11, DeepSeek V4 Flash (max) 15→13, GLM-5.3 Flash (max) 16→17, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→16 |
| dahlia/optique (4) | GLM-5.3 (max) 7→8, Grok 4.6 (medium) 8→7, Qwen3.8 Max (xhigh) 10→12, GLM-5.2 (max) 11→10, Claude Opus 5 (max) 12→11, Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→13, Kimi K2.7 Code 19→20, Gemini 3.5 Flash (high) 20→19 |
| drizzle-team/drizzle-orm (4) | GPT-5.6 Luna (max) 9→12, Qwen3.8 Max (xhigh) 10→9, GLM-5.2 (max) 11→13, Claude Opus 5 (max) 12→10, Claude Sonnet 5 (max) 13→11, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17, Kimi K2.7 Code 19→20, Gemini 3.5 Flash (high) 20→19 |
| dynamodb-toolbox/dynamodb-toolbox (8) | Claude Opus 4.8 (max) 3→4, GPT-5.6 Sol (max) 4→3, DeepSeek V4 Pro (max) 6→7, GLM-5.3 (max) 7→6, Grok 4.6 (medium) 8→10, GPT-5.6 Luna (max) 9→8, Qwen3.8 Max (xhigh) 10→9, Gemini 3.5 Flash (high) 20→21, Gemini 3.6 Flash (high) 21→20 |
| eicrud/eicrud (4) | DeepSeek V4 Pro (max) 6→8, GLM-5.3 (max) 7→6, Grok 4.6 (medium) 8→7, Qwen3.8 Max (xhigh) 10→11, GLM-5.2 (max) 11→14, Claude Opus 5 (max) 12→13, Claude Sonnet 5 (max) 13→10, GPT-5.5 (xhigh) 14→12, Kimi K2.7 Code 19→21, Gemini 3.5 Flash (high) 20→19, Gemini 3.6 Flash (high) 21→20 |
| flightcontrolhq/superjson (4) | GPT-5.6 Luna (max) 9→12, Qwen3.8 Max (xhigh) 10→11, GLM-5.2 (max) 11→9, Claude Opus 5 (max) 12→10, GPT-5.5 (xhigh) 14→15, DeepSeek V4 Flash (max) 15→14 |
| gvergnaud/ts-pattern (4) | DeepSeek V4 Pro (max) 6→7, GLM-5.3 (max) 7→8, Grok 4.6 (medium) 8→6, GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9, Claude Opus 5 (max) 12→14, GPT-5.5 (xhigh) 14→12 |
| jeffijoe/awilix (4) | DeepSeek V4 Pro (max) 6→8, GLM-5.3 (max) 7→6, Grok 4.6 (medium) 8→7, GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9, GLM-5.2 (max) 11→13, Claude Opus 5 (max) 12→11, Claude Sonnet 5 (max) 13→12, GPT-5.5 (xhigh) 14→15, DeepSeek V4 Flash (max) 15→14, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17, Kimi K2.7 Code 19→21, Gemini 3.5 Flash (high) 20→19, Gemini 3.6 Flash (high) 21→20 |
| kysely-org/kysely (4) | Grok 4.6 (medium) 8→10, GPT-5.6 Luna (max) 9→8, Qwen3.8 Max (xhigh) 10→13, GLM-5.2 (max) 11→9, Claude Opus 5 (max) 12→11, Claude Sonnet 5 (max) 13→12, GPT-5.5 (xhigh) 14→15, DeepSeek V4 Flash (max) 15→14, Gemini 3.5 Flash (high) 20→21, Gemini 3.6 Flash (high) 21→20 |
| meriyah/meriyah (4) | GPT-5.6 Luna (max) 9→13, Qwen3.8 Max (xhigh) 10→9, GLM-5.2 (max) 11→10, Claude Opus 5 (max) 12→11, Claude Sonnet 5 (max) 13→12, GPT-5.5 (xhigh) 14→15, DeepSeek V4 Flash (max) 15→14, Gemini 3.5 Flash (high) 20→21, Gemini 3.6 Flash (high) 21→20 |
| open-circle/valibot (4) | DeepSeek V4 Pro (max) 6→7, GLM-5.3 (max) 7→6, GPT-5.6 Luna (max) 9→12, Qwen3.8 Max (xhigh) 10→9, GLM-5.2 (max) 11→13, Claude Opus 5 (max) 12→11, Claude Sonnet 5 (max) 13→10, GPT-5.5 (xhigh) 14→15, DeepSeek V4 Flash (max) 15→14, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17 |
| platers/obsidian-linter (12) | GLM-5.3 (max) 7→9, Grok 4.6 (medium) 8→7, GPT-5.6 Luna (max) 9→8, Qwen3.8 Max (xhigh) 10→12, Claude Opus 5 (max) 12→14, GPT-5.5 (xhigh) 14→10 |
| pmndrs/koota (16) | GLM-5.3 (max) 7→10, Grok 4.6 (medium) 8→9, GPT-5.6 Luna (max) 9→11, Qwen3.8 Max (xhigh) 10→8, GLM-5.2 (max) 11→7, Claude Opus 5 (max) 12→15, Claude Sonnet 5 (max) 13→12, GPT-5.5 (xhigh) 14→13, DeepSeek V4 Flash (max) 15→14, Gemini 3.7 Flash (medium) 18→19, Kimi K2.7 Code 19→18, Gemini 3.5 Flash (high) 20→21, Gemini 3.6 Flash (high) 21→20 |
| slab/quill (4) | DeepSeek V4 Pro (max) 6→8, Grok 4.6 (medium) 8→6, GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9, Claude Sonnet 5 (max) 13→15, GPT-5.5 (xhigh) 14→13, DeepSeek V4 Flash (max) 15→14, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17, Gemini 3.5 Flash (high) 20→21, Gemini 3.6 Flash (high) 21→20 |
| sql-formatter-org/sql-formatter (4) | DeepSeek V4 Pro (max) 6→7, GLM-5.3 (max) 7→8, Grok 4.6 (medium) 8→6, GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→9, GLM-5.2 (max) 11→12, Claude Opus 5 (max) 12→11 |
| true-myth/true-myth (4) | Qwen3.8 Max (xhigh) 10→11, GLM-5.2 (max) 11→10, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17, Kimi K2.7 Code 19→21, Gemini 3.6 Flash (high) 21→19 |
| unjs/ofetch (4) | GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→12, GLM-5.2 (max) 11→9, Claude Opus 5 (max) 12→14, GPT-5.5 (xhigh) 14→11, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17, Gemini 3.5 Flash (high) 20→22, Gemini 3.6 Flash (high) 21→20, Claude Sonnet 4.6 (high) 22→21 |
| vadimdemedes/ink (4) | DeepSeek V4 Pro (max) 6→8, GLM-5.3 (max) 7→6, Grok 4.6 (medium) 8→7, GPT-5.6 Luna (max) 9→10, Qwen3.8 Max (xhigh) 10→11, GLM-5.2 (max) 11→12, Claude Opus 5 (max) 12→9, Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→13, Grok 4.5 (high) 17→18, Gemini 3.7 Flash (medium) 18→17, Kimi K2.7 Code 19→20, Gemini 3.5 Flash (high) 20→19 |
| vitest-dev/vitest (4) | DeepSeek V4 Pro (max) 6→7, GLM-5.3 (max) 7→6, Claude Sonnet 5 (max) 13→14, GPT-5.5 (xhigh) 14→13 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (70) | Solved by fewer (70) |
|---|---:|---:|
| Claude Fable 5 (xhigh) | 43.3 (1) | 43.3 (1) |
| Kimi K3 (max) | 34.8 (2) | 34.8 (2) |
| Claude Opus 4.8 (max) | 32.8 (3) | 32.8 (3) |
| GPT-5.6 Sol (max) | 30.8 (4) | 30.8 (4) |
| GPT-5.6 Terra (max) | 28.5 (5) | 28.5 (5) |
| DeepSeek V4 Pro (max) | 26.2 (6) | 26.2 (6) |
| GLM-5.3 (max) | 25.8 (7) | 25.8 (7) |
| Grok 4.6 (medium) | 25.5 (8) | 25.5 (8) |
| GPT-5.6 Luna (max) | 23.9 (9) | 23.9 (9) |
| Qwen3.8 Max (xhigh) | 23.7 (10) | 23.7 (10) |
| GLM-5.2 (max) | 23.3 (11) | 23.3 (11) |
| Claude Opus 5 (max) | 22.8 (12) | 22.8 (12) |
| Claude Sonnet 5 (max) | 22.4 (13) | 22.4 (13) |
| GPT-5.5 (xhigh) | 22.3 (14) | 22.3 (14) |
| DeepSeek V4 Flash (max) | 21.2 (15) | 21.2 (15) |
| GLM-5.3 Flash (max) | 19.1 (16) | 19.1 (16) |
| Grok 4.5 (high) | 17.5 (17) | 17.5 (17) |
| Gemini 3.7 Flash (medium) | 17.2 (18) | 17.2 (18) |
| Kimi K2.7 Code | 15.0 (19) | 15.0 (19) |
| Gemini 3.5 Flash (high) | 14.4 (20) | 14.4 (20) |
| Gemini 3.6 Flash (high) | 14.1 (21) | 14.1 (21) |
| Claude Sonnet 4.6 (high) | 12.0 (22) | 12.0 (22) |
| GPT-5.4 (xhigh) | 10.1 (23) | 10.1 (23) |
| Muse Spark 1.1 (xhigh) | 7.7 (24) | 7.7 (24) |
| Muse Spark 1.2 (xhigh) | 6.8 (25) | 6.8 (25) |
| Gemini 3.1 Pro Preview (high) | 2.4 (26) | 2.4 (26) |

## What drives each adjacent gap

Difference in mean score split by outcome (a/b), and the tasks that move it most. Contributions are per-task differences divided by the task count, so they sum to the gap.

- **Claude Fable 5 (xhigh) − Kimi K3 (max) = 8.23**: failed/failed 0.11 (30), failed/solved -8.11 (14), solved/failed 12.04 (17), solved/solved 4.20 (57). For Claude Fable 5 (xhigh): `koota-query-predicates#1` +0.98 (solved/failed), `obsidian-linter-link-format-conversion#4` +0.93 (solved/failed), `koota-composite-trait-aspects#4` +0.91 (solved/failed). For Kimi K3 (max): `obsidian-linter-auto-table-of-contents#1` -0.89 (failed/solved), `eicrud-keyset-pagination-cursor#2` -0.85 (failed/solved), `optique-conditional-option-dependencies#3` -0.81 (failed/solved).
- **Kimi K3 (max) − Claude Opus 4.8 (max) = 4.41**: failed/failed -0.12 (27), failed/solved -8.96 (13), solved/failed 17.77 (26), solved/solved -4.27 (44). For Kimi K3 (max): `ts-pattern-match-each#3` +1.00 (solved/failed), `obsidian-linter-auto-table-of-contents#1` +0.96 (solved/failed), `eicrud-keyset-pagination-cursor#2` +0.93 (solved/failed). For Claude Opus 4.8 (max): `dynamodb-toolbox-lazy-recursive-schemas#4` -0.92 (failed/solved), `koota-pair-relation-tracking#3` -0.90 (failed/solved), `claude-code-by-agents-recursive-delegation#1` -0.90 (failed/solved).
- **Claude Opus 4.8 (max) − GPT-5.6 Sol (max) = 4.18**: failed/failed 0.29 (28), failed/solved -12.28 (24), solved/failed 9.24 (12), solved/solved 6.92 (42). For Claude Opus 4.8 (max): `arktype-json-schema-refs-dependencies#1` +1.00 (solved/failed), `koota-pair-relation-tracking#3` +0.94 (solved/failed), `claude-code-by-agents-recursive-delegation#1` +0.93 (solved/failed). For GPT-5.6 Sol (max): `query-persist-restored-query-state#2` -0.98 (failed/solved), `optique-conditional-option-dependencies#3` -0.87 (failed/solved), `claude-code-by-agents-recursive-delegation#4` -0.82 (failed/solved).
- **GPT-5.6 Sol (max) − GPT-5.6 Terra (max) = 2.42**: failed/failed 0.07 (27), failed/solved -6.56 (13), solved/failed 6.91 (13), solved/solved 2.00 (61). For GPT-5.6 Sol (max): `query-persist-restored-query-state#2` +0.89 (solved/failed), `arktype-json-schema-refs-dependencies#4` +0.81 (solved/failed), `optique-conditional-option-dependencies#3` +0.81 (solved/failed). For GPT-5.6 Terra (max): `meriyah-explicit-resource-declarations#2` -0.97 (failed/solved), `meriyah-explicit-resource-declarations#1` -0.92 (failed/solved), `superjson-error-stack-serialization#2` -0.75 (failed/solved).
- **GPT-5.6 Terra (max) − DeepSeek V4 Pro (max) = 1.92**: failed/failed 0.11 (24), failed/solved -7.91 (15), solved/failed 9.73 (18), solved/solved -0.02 (55). For GPT-5.6 Terra (max): `valibot-recursive-schema-composition#1` +1.00 (solved/failed), `valibot-recursive-schema-composition#4` +0.93 (solved/failed), `koota-composite-trait-aspects#4` +0.84 (solved/failed). For DeepSeek V4 Pro (max): `obsidian-linter-scoped-ignore-markers#3` -0.91 (failed/solved), `optique-conditional-option-dependencies#3` -0.90 (failed/solved), `query-persist-restored-query-state#3` -0.81 (failed/solved).
- **DeepSeek V4 Pro (max) − GLM-5.3 (max) = -0.21**: failed/failed -0.13 (20), failed/solved -12.43 (23), solved/failed 11.62 (25), solved/solved 0.73 (47). For DeepSeek V4 Pro (max): `optique-conditional-option-dependencies#3` +0.88 (solved/failed), `koota-deferred-mutation-buffer#2` +0.86 (solved/failed), `claude-code-by-agents-recursive-delegation#3` +0.84 (solved/failed). For GLM-5.3 (max): `optique-conditional-option-dependencies#2` -0.94 (failed/solved), `optique-conditional-option-dependencies#1` -0.86 (failed/solved), `koota-query-predicates#2` -0.85 (failed/solved).
- **GLM-5.3 (max) − Grok 4.6 (medium) = 0.13**: failed/failed 0.21 (32), failed/solved -8.07 (14), solved/failed 9.33 (18), solved/solved -1.34 (52). For GLM-5.3 (max): `ts-pattern-match-each#4` +0.97 (solved/failed), `koota-composite-trait-aspects#1` +0.90 (solved/failed), `optique-conditional-option-dependencies#1` +0.85 (solved/failed). For Grok 4.6 (medium): `optique-conditional-option-dependencies#3` -0.92 (failed/solved), `ts-pattern-match-each#1` -0.87 (failed/solved), `koota-deferred-mutation-buffer#1` -0.79 (failed/solved).
- **Grok 4.6 (medium) − GPT-5.6 Luna (max) = -0.07**: failed/failed 0.21 (23), failed/solved -12.48 (25), solved/failed 8.73 (16), solved/solved 3.48 (46). For Grok 4.6 (medium): `kysely-window-grouping-helpers#2` +0.99 (solved/failed), `ts-pattern-match-each#1` +0.92 (solved/failed), `koota-query-predicates#3` +0.79 (solved/failed). For GPT-5.6 Luna (max): `query-persist-restored-query-state#1` -0.98 (failed/solved), `query-persist-restored-query-state#3` -0.94 (failed/solved), `superjson-error-stack-serialization#2` -0.88 (failed/solved).
- **GPT-5.6 Luna (max) − Qwen3.8 Max (xhigh) = 1.32**: failed/failed -0.36 (24), failed/solved -10.72 (15), solved/failed 12.88 (28), solved/solved -0.48 (43). For GPT-5.6 Luna (max): `koota-pair-relation-tracking#4` +0.95 (solved/failed), `superjson-error-stack-serialization#2` +0.88 (solved/failed), `koota-deferred-mutation-buffer#1` +0.85 (solved/failed). For Qwen3.8 Max (xhigh): `arktype-json-schema-refs-dependencies#2` -0.92 (failed/solved), `obsidian-linter-scoped-ignore-markers#1` -0.92 (failed/solved), `happy-dom-deterministic-intersectionobserver#4` -0.90 (failed/solved).
- **Qwen3.8 Max (xhigh) − GLM-5.2 (max) = -0.83**: failed/failed -0.89 (39), failed/solved -10.30 (15), solved/failed 15.74 (25), solved/solved -5.37 (38). For Qwen3.8 Max (xhigh): `superjson-error-stack-serialization#1` +0.91 (solved/failed), `kysely-window-grouping-helpers#4` +0.90 (solved/failed), `arktype-json-schema-refs-dependencies#2` +0.84 (solved/failed). For GLM-5.2 (max): `ink-grid-box-layout#2` -0.96 (failed/solved), `ts-pattern-match-each#2` -0.92 (failed/solved), `awilix-async-container-initialization#4` -0.86 (failed/solved).
- **GLM-5.2 (max) − Claude Opus 5 (max) = 1.52**: failed/failed 0.96 (31), failed/solved -15.80 (35), solved/failed 8.61 (13), solved/solved 7.75 (38). For GLM-5.2 (max): `ink-grid-box-layout#2` +0.95 (solved/failed), `happy-dom-deterministic-intersectionobserver#1` +0.90 (solved/failed), `awilix-async-container-initialization#4` +0.89 (solved/failed). For Claude Opus 5 (max): `ts-pattern-match-each#1` -0.88 (failed/solved), `obsidian-linter-auto-table-of-contents#4` -0.78 (failed/solved), `obsidian-linter-scoped-ignore-markers#1` -0.74 (failed/solved).
- **Claude Opus 5 (max) − Claude Sonnet 5 (max) = 0.40**: failed/failed -0.73 (28), failed/solved -10.57 (15), solved/failed 11.76 (30), solved/solved -0.07 (41). For Claude Opus 5 (max): `obsidian-linter-auto-table-of-contents#4` +0.80 (solved/failed), `obsidian-linter-scoped-ignore-markers#2` +0.78 (solved/failed), `obsidian-linter-scoped-ignore-markers#3` +0.73 (solved/failed). For Claude Sonnet 5 (max): `quill-shared-toolbar-focus#1` -0.98 (failed/solved), `superjson-error-stack-serialization#1` -0.97 (failed/solved), `koota-deferred-mutation-buffer#4` -0.96 (failed/solved).
- **Claude Sonnet 5 (max) − GPT-5.5 (xhigh) = 1.77**: failed/failed 0.42 (29), failed/solved -11.57 (25), solved/failed 10.46 (16), solved/solved 2.46 (41). For Claude Sonnet 5 (max): `koota-deferred-mutation-buffer#4` +1.01 (solved/failed), `quill-shared-toolbar-focus#1` +0.98 (solved/failed), `quill-shared-toolbar-focus#4` +0.95 (solved/failed). For GPT-5.5 (xhigh): `meriyah-explicit-resource-declarations#4` -0.83 (failed/solved), `superjson-error-stack-serialization#4` -0.82 (failed/solved), `kysely-window-grouping-helpers#1` -0.81 (failed/solved).
- **GPT-5.5 (xhigh) − DeepSeek V4 Flash (max) = 1.45**: failed/failed -0.35 (28), failed/solved -9.76 (17), solved/failed 15.47 (27), solved/solved -3.91 (38). For GPT-5.5 (xhigh): `drizzle-orm-window-function-builders#2` +0.98 (solved/failed), `superjson-error-stack-serialization#4` +0.93 (solved/failed), `superjson-error-stack-serialization#1` +0.82 (solved/failed). For DeepSeek V4 Flash (max): `claude-code-by-agents-recursive-delegation#1` -0.95 (failed/solved), `obsidian-linter-link-format-conversion#1` -0.86 (failed/solved), `cliffy-config-file-parsing#3` -0.83 (failed/solved).
- **DeepSeek V4 Flash (max) − GLM-5.3 Flash (max) = 1.38**: failed/failed -0.09 (37), failed/solved -11.42 (20), solved/failed 10.64 (19), solved/solved 2.26 (37). For DeepSeek V4 Flash (max): `cliffy-config-file-parsing#4` +0.99 (solved/failed), `claude-code-by-agents-recursive-delegation#1` +0.91 (solved/failed), `koota-pair-relation-tracking#3` +0.90 (solved/failed). For GLM-5.3 Flash (max): `arktype-json-schema-refs-dependencies#2` -0.93 (failed/solved), `clack-async-autocomplete-options#3` -0.86 (failed/solved), `happy-dom-deterministic-intersectionobserver#2` -0.83 (failed/solved).
- **GLM-5.3 Flash (max) − Grok 4.5 (high) = 0.63**: failed/failed 0.10 (40), failed/solved -7.85 (16), solved/failed 9.04 (19), solved/solved -0.66 (40). For GLM-5.3 Flash (max): `happy-dom-deterministic-intersectionobserver#2` +0.83 (solved/failed), `clack-async-autocomplete-options#4` +0.76 (solved/failed), `ts-pattern-match-each#3` +0.68 (solved/failed). For Grok 4.5 (high): `dynamodb-toolbox-conditional-attribute-requirements#2` -0.92 (failed/solved), `ink-grid-box-layout#4` -0.86 (failed/solved), `awilix-async-container-initialization#4` -0.66 (failed/solved).
- **Grok 4.5 (high) − Gemini 3.7 Flash (medium) = 1.72**: failed/failed 0.08 (29), failed/solved -13.14 (32), solved/failed 7.36 (16), solved/solved 7.43 (41). For Grok 4.5 (high): `ink-grid-box-layout#4` +0.84 (solved/failed), `arktype-json-schema-refs-dependencies#2` +0.77 (solved/failed), `cliffy-config-file-parsing#1` +0.70 (solved/failed). For Gemini 3.7 Flash (medium): `obsidian-linter-link-format-conversion#3` -0.86 (failed/solved), `kysely-window-grouping-helpers#1` -0.78 (failed/solved), `eicrud-keyset-pagination-cursor#2` -0.77 (failed/solved).
- **Gemini 3.7 Flash (medium) − Kimi K2.7 Code = 1.74**: failed/failed -0.33 (32), failed/solved -9.20 (12), solved/failed 18.80 (50), solved/solved -7.54 (23). For Gemini 3.7 Flash (medium): `obsidian-linter-link-format-conversion#3` +0.86 (solved/failed), `kysely-window-grouping-helpers#1` +0.79 (solved/failed), `kysely-window-grouping-helpers#2` +0.71 (solved/failed). For Kimi K2.7 Code: `awilix-async-container-initialization#1` -0.94 (failed/solved), `query-persist-restored-query-state#4` -0.93 (failed/solved), `ink-grid-box-layout#1` -0.93 (failed/solved).
- **Kimi K2.7 Code − Gemini 3.5 Flash (high) = 2.40**: failed/solved -13.09 (24), solved/failed 13.57 (18), solved/solved 1.92 (19). For Kimi K2.7 Code: `query-persist-restored-query-state#4` +0.93 (solved/failed), `optique-conditional-option-dependencies#1` +0.92 (solved/failed), `awilix-async-container-initialization#1` +0.92 (solved/failed). For Gemini 3.5 Flash (high): `ofetch-per-origin-circuit-breaker#1` -0.89 (failed/solved), `dynamodb-toolbox-lazy-recursive-schemas#1` -0.89 (failed/solved), `claude-code-by-agents-recursive-delegation#3` -0.88 (failed/solved).
- **Gemini 3.5 Flash (high) − Gemini 3.6 Flash (high) = 0.51**: failed/failed 0.14 (55), failed/solved -12.61 (20), solved/failed 9.26 (14), solved/solved 3.71 (31). For Gemini 3.5 Flash (high): `valibot-recursive-schema-composition#2` +0.92 (solved/failed), `koota-deferred-mutation-buffer#2` +0.89 (solved/failed), `dynamodb-toolbox-lazy-recursive-schemas#1` +0.89 (solved/failed). For Gemini 3.6 Flash (high): `sql-formatter-bigquery-pipe-formatting#1` -0.92 (failed/solved), `obsidian-linter-scoped-ignore-markers#3` -0.88 (failed/solved), `optique-conditional-option-dependencies#3` -0.82 (failed/solved).
- **Gemini 3.6 Flash (high) − Claude Sonnet 4.6 (high) = 0.17**: failed/failed -0.10 (54), failed/solved -10.23 (15), solved/failed 13.78 (25), solved/solved -3.28 (24). For Gemini 3.6 Flash (high): `obsidian-linter-scoped-ignore-markers#3` +0.90 (solved/failed), `vitest-duration-sharding#1` +0.85 (solved/failed), `optique-conditional-option-dependencies#3` +0.84 (solved/failed). For Claude Sonnet 4.6 (high): `cliffy-config-file-parsing#3` -0.94 (failed/solved), `awilix-async-container-initialization#1` -0.91 (failed/solved), `obsidian-linter-link-format-conversion#1` -0.82 (failed/solved).
- **Claude Sonnet 4.6 (high) − GPT-5.4 (xhigh) = 2.21**: failed/failed 0.71 (48), failed/solved -12.58 (32), solved/failed 10.84 (13), solved/solved 3.24 (23). For Claude Sonnet 4.6 (high): `eicrud-keyset-pagination-cursor#3` +0.99 (solved/failed), `cliffy-config-file-parsing#3` +0.98 (solved/failed), `obsidian-linter-link-format-conversion#2` +0.94 (solved/failed). For GPT-5.4 (xhigh): `valibot-recursive-schema-composition#1` -0.89 (failed/solved), `meriyah-explicit-resource-declarations#1` -0.85 (failed/solved), `meriyah-explicit-resource-declarations#3` -0.84 (failed/solved).
- **GPT-5.4 (xhigh) − Muse Spark 1.1 (xhigh) = 1.27**: failed/failed 0.38 (35), failed/solved -10.03 (25), solved/failed 7.49 (20), solved/solved 3.44 (34). For GPT-5.4 (xhigh): `kysely-window-grouping-helpers#2` +0.85 (solved/failed), `happy-dom-abort-pending-body-reads#1` +0.66 (solved/failed), `meriyah-explicit-resource-declarations#3` +0.60 (solved/solved). For Muse Spark 1.1 (xhigh): `sql-formatter-bigquery-pipe-formatting#3` -0.94 (failed/solved), `query-persist-restored-query-state#3` -0.87 (failed/solved), `drizzle-orm-window-function-builders#1` -0.78 (failed/solved).
- **Muse Spark 1.1 (xhigh) − Muse Spark 1.2 (xhigh) = -0.20**: failed/failed -0.08 (32), failed/solved -5.54 (17), solved/failed 2.96 (12), solved/solved 2.47 (46). For Muse Spark 1.1 (xhigh): `ts-pattern-match-each#3` +0.53 (solved/solved), `happy-dom-deterministic-intersectionobserver#2` +0.47 (solved/solved), `sql-formatter-bigquery-pipe-formatting#3` +0.45 (solved/solved). For Muse Spark 1.2 (xhigh): `eicrud-keyset-pagination-cursor#1` -0.78 (failed/solved), `koota-query-predicates#1` -0.73 (failed/solved), `eicrud-keyset-pagination-cursor#2` -0.69 (failed/solved).
- **Muse Spark 1.2 (xhigh) − Gemini 3.1 Pro Preview (high) = 4.14**: failed/failed -1.97 (41), failed/solved -1.95 (2), solved/failed 14.04 (47), solved/solved -5.97 (14). For Muse Spark 1.2 (xhigh): `meriyah-explicit-resource-declarations#4` +0.78 (solved/failed), `eicrud-keyset-pagination-cursor#1` +0.74 (solved/failed), `valibot-recursive-schema-composition#1` +0.74 (solved/failed). For Gemini 3.1 Pro Preview (high): `meriyah-explicit-resource-declarations#3` -0.99 (failed/solved), `ts-pattern-match-each#4` -0.96 (failed/solved), `sql-formatter-bigquery-pipe-formatting#1` -0.88 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability examples/deepswe-typescript/score-panel.json examples/deepswe-typescript/*.jsonl --output examples/deepswe-typescript/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
