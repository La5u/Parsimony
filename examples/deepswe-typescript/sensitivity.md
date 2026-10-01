# Score sensitivity: 26 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `deepswe-v1.1-typescript-26-pooled-80-20-v0.7`: 132 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (110 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Fable 5 (xhigh) > Kimi K3 (max) ≈ Claude Opus 4.8 (max) ≈ GPT-5.6 Sol (max) ≈ GPT-5.6 Terra (max) ≈ GLM-5.3 (max) ≈ Grok 4.6 (medium) ≈ DeepSeek V4 Pro (max) ≈ Qwen3.8 Max (xhigh) ≈ GLM-5.2 (max) ≈ GPT-5.6 Luna (max) ≈ Claude Opus 5 (max) ≈ GPT-5.5 (xhigh) ≈ Claude Sonnet 5 (max) ≈ DeepSeek V4 Flash (max) ≈ GLM-5.3 Flash (max) ≈ Gemini 3.7 Flash (medium) ≈ Grok 4.5 (high) ≈ Gemini 3.6 Flash (high) ≈ Gemini 3.5 Flash (high) ≈ Kimi K2.7 Code ≈ Claude Sonnet 4.6 (high) ≈ GPT-5.4 (xhigh) ≈ Muse Spark 1.1 (xhigh) ≈ Muse Spark 1.2 (xhigh) ≈ Gemini 3.1 Pro Preview (high) (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (1 of 25 adjacent pairs): Claude Fable 5 (xhigh) > Kimi K3 (max).
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 24 pairs): Kimi K3 (max) vs Claude Opus 4.8 (max), Claude Opus 4.8 (max) vs GPT-5.6 Sol (max), GPT-5.6 Sol (max) vs GPT-5.6 Terra (max), GPT-5.6 Terra (max) vs GLM-5.3 (max), GLM-5.3 (max) vs Grok 4.6 (medium), Grok 4.6 (medium) vs DeepSeek V4 Pro (max), DeepSeek V4 Pro (max) vs Qwen3.8 Max (xhigh), Qwen3.8 Max (xhigh) vs GLM-5.2 (max), GLM-5.2 (max) vs GPT-5.6 Luna (max), GPT-5.6 Luna (max) vs Claude Opus 5 (max), Claude Opus 5 (max) vs GPT-5.5 (xhigh), GPT-5.5 (xhigh) vs Claude Sonnet 5 (max), Claude Sonnet 5 (max) vs DeepSeek V4 Flash (max), DeepSeek V4 Flash (max) vs GLM-5.3 Flash (max), GLM-5.3 Flash (max) vs Gemini 3.7 Flash (medium), Gemini 3.7 Flash (medium) vs Grok 4.5 (high), Grok 4.5 (high) vs Gemini 3.6 Flash (high), Gemini 3.6 Flash (high) vs Gemini 3.5 Flash (high), Gemini 3.5 Flash (high) vs Kimi K2.7 Code, Kimi K2.7 Code vs Claude Sonnet 4.6 (high), Claude Sonnet 4.6 (high) vs GPT-5.4 (xhigh), GPT-5.4 (xhigh) vs Muse Spark 1.1 (xhigh), Muse Spark 1.1 (xhigh) vs Muse Spark 1.2 (xhigh), Muse Spark 1.2 (xhigh) vs Gemini 3.1 Pro Preview (high).
- **Midpoint rank never changes under any variation**: Claude Fable 5 (xhigh) (1), Kimi K3 (max) (2), Muse Spark 1.1 (xhigh) (24), Muse Spark 1.2 (xhigh) (25), Gemini 3.1 Pro Preview (high) (26).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 132 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Fable 5 (xhigh) | 42.3 | 30.1–54.2 | 42.3 | 1–1 | 1–2 | 0.93 |
| 2 | Kimi K3 (max) | 33.1 | 23.0–43.0 | 33.1 | 2–2 | 2–8 | 0.02 |
| 3 | Claude Opus 4.8 (max) | 31.0 | 14.6–47.3 | 26.8–35.3 | 3–4 | 2–10 | 0.01 |
| 4 | GPT-5.6 Sol (max) | 29.5 | 19.6–40.1 | 29.5 | 3–4 | 1–11 | 0.03 |
| 5 | GPT-5.6 Terra (max) | 26.3 | 16.5–36.5 | 25.8–26.7 | 5–6 | 2–15 | 0.00 |
| 6 | GLM-5.3 (max) | 24.5 | 15.4–34.0 | 24.5 | 5–10 | 3–18 | 0.00 |
| 7 | Grok 4.6 (medium) | 24.1 | 14.0–34.9 | 24.1 | 6–12 | 3–18 | 0.00 |
| 8 | DeepSeek V4 Pro (max) | 23.8 | 15.6–32.3 | 23.8 | 6–10 | 3–16 | 0.00 |
| 9 | Qwen3.8 Max (xhigh) | 23.5 | 13.9–32.7 | 22.1–24.9 | 7–12 | 4–17 | 0.00 |
| 10 | GLM-5.2 (max) | 23.2 | 15.4–30.8 | 23.2 | 6–12 | 3–17 | 0.00 |
| 11 | GPT-5.6 Luna (max) | 22.6 | 11.5–34.7 | 20.7–24.5 | 8–14 | 3–19 | 0.00 |
| 12 | Claude Opus 5 (max) | 22.0 | 12.7–31.8 | 20.6–23.5 | 9–16 | 4–19 | 0.00 |
| 13 | GPT-5.5 (xhigh) | 21.3 | 12.1–29.9 | 21.3 | 11–16 | 5–20 | 0.00 |
| 14 | Claude Sonnet 5 (max) | 21.1 | 12.5–30.0 | 20.1–22.0 | 12–16 | 4–20 | 0.00 |
| 15 | DeepSeek V4 Flash (max) | 20.5 | 11.2–30.0 | 20.5 | 13–16 | 5–20 | 0.00 |
| 16 | GLM-5.3 Flash (max) | 19.6 | 10.8–28.3 | 19.1–20.1 | 15–17 | 6–22 | 0.00 |
| 17 | Gemini 3.7 Flash (medium) | 17.5 | 10.7–24.4 | 17.5 | 16–18 | 10–21 | 0.00 |
| 18 | Grok 4.5 (high) | 16.6 | 8.2–25.7 | 16.6 | 17–18 | 10–23 | 0.00 |
| 19 | Gemini 3.6 Flash (high) | 14.2 | 6.8–22.0 | 14.2 | 19–21 | 13–23 | 0.00 |
| 20 | Gemini 3.5 Flash (high) | 13.9 | 5.2–22.9 | 13.9 | 19–22 | 12–23 | 0.00 |
| 21 | Kimi K2.7 Code | 13.8 | 4.5–23.1 | 13.8 | 19–21 | 10–24 | 0.00 |
| 22 | Claude Sonnet 4.6 (high) | 10.9 | 2.3–20.2 | 10.4–11.5 | 21–23 | 15–26 | 0.00 |
| 23 | GPT-5.4 (xhigh) | 9.7 | 2.8–16.9 | 9.7 | 22–23 | 18–25 | 0.00 |
| 24 | Muse Spark 1.1 (xhigh) | 6.0 | -1.5–13.4 | 6.0 | 24–24 | 20–26 | 0.00 |
| 25 | Muse Spark 1.2 (xhigh) | 5.1 | -1.1–11.2 | 5.1 | 25–25 | 22–26 | 0.00 |
| 26 | Gemini 3.1 Pro Preview (high) | 1.9 | -5.1–9.8 | 1.6–2.3 | 26–26 | 23–26 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Fable 5 (xhigh) > Kimi K3 (max) | 9.19 | 0.19 to 18.46 | 0.98 | none | yes |
| Kimi K3 (max) > Claude Opus 4.8 (max) | 2.05 | -13.53 to 16.13 | 0.36 | none | no |
| Claude Opus 4.8 (max) > GPT-5.6 Sol (max) | 1.54 | -15.15 to 17.19 | 0.33 | failure cap=50, without dynamodb-toolbox/dynamodb-toolbox | no |
| GPT-5.6 Sol (max) > GPT-5.6 Terra (max) | 3.25 | -3.99 to 10.15 | 0.80 | none | yes |
| GPT-5.6 Terra (max) > GLM-5.3 (max) | 1.71 | -10.78 to 14.44 | 0.58 | without open-circle/valibot | yes |
| GLM-5.3 (max) > Grok 4.6 (medium) | 0.42 | -8.79 to 8.89 | 0.55 | failure cap=0, failure cap=10, without bombshell-dev/clack, without capricorn86/happy-dom, without gvergnaud/ts-pattern, without keajs/kea, without platers/obsidian-linter, without pmndrs/koota, without slab/quill, without sql-formatter-org/sql-formatter | yes |
| Grok 4.6 (medium) > DeepSeek V4 Pro (max) | 0.31 | -10.99 to 10.57 | 0.52 | net weight=0.5, failure cap=50, panel without Kimi K2.7 Code, without arktypeio/arktype, without bombshell-dev/clack, without dahlia/optique, without drizzle-team/drizzle-orm, without dynamodb-toolbox/dynamodb-toolbox, without flightcontrolhq/superjson, without keajs/kea, without kysely-org/kysely, without pmndrs/koota, without true-myth/true-myth | yes |
| DeepSeek V4 Pro (max) > Qwen3.8 Max (xhigh) | 0.34 | -9.86 to 10.59 | 0.43 | net weight=1, failure cap=0, failure cap=10, without TanStack/query, without baryhuang/claude-code-by-agents, without c4spar/cliffy, without dynamodb-toolbox/dynamodb-toolbox, without gvergnaud/ts-pattern, without jeffijoe/awilix, without open-circle/valibot, without slab/quill, without vitest-dev/vitest | no |
| Qwen3.8 Max (xhigh) > GLM-5.2 (max) | 0.24 | -10.21 to 11.03 | 0.38 | net weight=0.5, net weight=0.6, failure cap=50, panel without GPT-5.4 (xhigh), without Effect-TS/effect, without arktypeio/arktype, without capricorn86/happy-dom, without dahlia/optique, without flightcontrolhq/superjson, without kysely-org/kysely, without platers/obsidian-linter, without pmndrs/koota, without true-myth/true-myth, without unjs/ofetch | no |
| GLM-5.2 (max) > GPT-5.6 Luna (max) | 0.60 | -11.02 to 12.36 | 0.41 | without bombshell-dev/clack, without c4spar/cliffy, without capricorn86/happy-dom, without eicrud/eicrud, without jeffijoe/awilix, without keajs/kea, without platers/obsidian-linter | no |
| GPT-5.6 Luna (max) > Claude Opus 5 (max) | 0.60 | -15.01 to 16.41 | 0.35 | failure cap=50, without TanStack/query, without baryhuang/claude-code-by-agents, without drizzle-team/drizzle-orm, without flightcontrolhq/superjson, without meriyah/meriyah, without open-circle/valibot, without sql-formatter-org/sql-formatter, without vadimdemedes/ink | no |
| Claude Opus 5 (max) > GPT-5.5 (xhigh) | 0.74 | -12.01 to 13.70 | 0.47 | without bombshell-dev/clack, without capricorn86/happy-dom, without gvergnaud/ts-pattern, without platers/obsidian-linter, without pmndrs/koota, without unjs/ofetch | no |
| GPT-5.5 (xhigh) > Claude Sonnet 5 (max) | 0.20 | -11.58 to 12.25 | 0.44 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, panel without GLM-5.3 Flash (max), without Effect-TS/effect, without baryhuang/claude-code-by-agents, without drizzle-team/drizzle-orm, without flightcontrolhq/superjson, without jeffijoe/awilix, without keajs/kea, without kysely-org/kysely, without meriyah/meriyah, without open-circle/valibot | no |
| Claude Sonnet 5 (max) > DeepSeek V4 Flash (max) | 0.58 | -10.84 to 11.72 | 0.47 | net weight=0.5, failure cap=0, without bombshell-dev/clack, without capricorn86/happy-dom, without flightcontrolhq/superjson, without slab/quill, without sql-formatter-org/sql-formatter, without true-myth/true-myth, without vadimdemedes/ink | no |
| DeepSeek V4 Flash (max) > GLM-5.3 Flash (max) | 0.93 | -10.04 to 12.03 | 0.54 | without baryhuang/claude-code-by-agents, without dahlia/optique, without eicrud/eicrud, without vitest-dev/vitest | yes |
| GLM-5.3 Flash (max) > Gemini 3.7 Flash (medium) | 2.11 | -8.30 to 12.40 | 0.62 | without capricorn86/happy-dom | yes |
| Gemini 3.7 Flash (medium) > Grok 4.5 (high) | 0.82 | -9.46 to 10.55 | 0.58 | failure cap=0, failure cap=10, without baryhuang/claude-code-by-agents, without eicrud/eicrud, without flightcontrolhq/superjson, without keajs/kea, without kysely-org/kysely, without platers/obsidian-linter, without pmndrs/koota, without vitest-dev/vitest | yes |
| Grok 4.5 (high) > Gemini 3.6 Flash (high) | 2.48 | -8.74 to 13.66 | 0.66 | none | yes |
| Gemini 3.6 Flash (high) > Gemini 3.5 Flash (high) | 0.32 | -7.93 to 8.68 | 0.56 | net weight=0.5, net weight=0.6, failure cap=0, without arktypeio/arktype, without c4spar/cliffy, without dahlia/optique, without drizzle-team/drizzle-orm, without eicrud/eicrud, without keajs/kea, without platers/obsidian-linter, without sql-formatter-org/sql-formatter, without vadimdemedes/ink, without vitest-dev/vitest | yes |
| Gemini 3.5 Flash (high) > Kimi K2.7 Code | 0.08 | -10.20 to 10.51 | 0.52 | net weight=0.9, net weight=1, failure cap=0, failure cap=10, panel without Claude Sonnet 4.6 (high), panel without DeepSeek V4 Flash (max), panel without Gemini 3.6 Flash (high), panel without Gemini 3.7 Flash (medium), panel without Kimi K2.7 Code, without baryhuang/claude-code-by-agents, without bombshell-dev/clack, without dynamodb-toolbox/dynamodb-toolbox, without gvergnaud/ts-pattern, without keajs/kea, without kysely-org/kysely, without meriyah/meriyah, without pmndrs/koota, without slab/quill, without sql-formatter-org/sql-formatter, without unjs/ofetch | yes |
| Kimi K2.7 Code > Claude Sonnet 4.6 (high) | 2.83 | -8.38 to 13.27 | 0.65 | none | yes |
| Claude Sonnet 4.6 (high) > GPT-5.4 (xhigh) | 1.24 | -9.80 to 12.49 | 0.55 | without c4spar/cliffy, without jeffijoe/awilix, without platers/obsidian-linter | yes |
| GPT-5.4 (xhigh) > Muse Spark 1.1 (xhigh) | 3.68 | -5.16 to 12.14 | 0.79 | none | yes |
| Muse Spark 1.1 (xhigh) > Muse Spark 1.2 (xhigh) | 0.95 | -4.10 to 5.61 | 0.65 | none | yes |
| Muse Spark 1.2 (xhigh) > Gemini 3.1 Pro Preview (high) | 3.13 | -4.15 to 10.26 | 0.78 | none | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 42.3 (1) | 42.7 (1) | 42.6 (1) | 42.4 (1) | 42.1 (1) | 42.0 (1) | 42.3 (1) | 46.4 (1) | 44.7 (1) | 38.2 (1) |
| Kimi K3 (max) | 33.1 (2) | 33.7 (2) | 33.5 (2) | 33.3 (2) | 32.9 (2) | 32.7 (2) | 33.1 (2) | 37.3 (2) | 35.6 (2) | 28.8 (2) |
| Claude Opus 4.8 (max) | 31.0 (3) | 31.4 (3) | 31.3 (3) | 31.2 (3) | 30.9 (3) | 30.8 (3) | 31.0 (3) | 36.9 (3) | 34.6 (3) | 25.2 (4) |
| GPT-5.6 Sol (max) | 29.5 (4) | 28.5 (4) | 28.8 (4) | 29.2 (4) | 29.9 (4) | 30.2 (4) | 29.5 (4) | 33.7 (4) | 32.0 (4) | 25.3 (3) |
| GPT-5.6 Terra (max) | 26.3 (5) | 25.6 (5) | 25.8 (5) | 26.0 (5) | 26.5 (5) | 26.7 (5) | 26.3 (5) | 30.9 (5) | 29.0 (5) | 21.6 (5) |
| GLM-5.3 (max) | 24.5 (6) | 24.3 (6) | 24.4 (6) | 24.4 (6) | 24.6 (6) | 24.7 (6) | 24.5 (6) | 29.0 (9) | 27.2 (7) | 20.1 (6) |
| Grok 4.6 (medium) | 24.1 (7) | 24.1 (8) | 24.1 (7) | 24.1 (7) | 24.2 (7) | 24.2 (7) | 24.1 (7) | 29.7 (6) | 27.5 (6) | 18.6 (8) |
| DeepSeek V4 Pro (max) | 23.8 (8) | 24.2 (7) | 24.1 (8) | 23.9 (8) | 23.7 (8) | 23.6 (9) | 23.8 (8) | 29.0 (8) | 26.9 (9) | 18.6 (7) |
| Qwen3.8 Max (xhigh) | 23.5 (9) | 23.3 (10) | 23.4 (10) | 23.4 (9) | 23.5 (9) | 23.6 (8) | 23.5 (9) | 29.4 (7) | 27.0 (8) | 17.5 (10) |
| GLM-5.2 (max) | 23.2 (10) | 23.5 (9) | 23.4 (9) | 23.3 (10) | 23.1 (10) | 23.0 (10) | 23.2 (10) | 28.4 (10) | 26.3 (10) | 18.1 (9) |
| GPT-5.6 Luna (max) | 22.6 (11) | 22.1 (11) | 22.3 (11) | 22.5 (11) | 22.8 (11) | 23.0 (11) | 22.6 (11) | 28.3 (11) | 26.0 (11) | 17.0 (12) |
| Claude Opus 5 (max) | 22.0 (12) | 22.1 (12) | 22.1 (12) | 22.0 (12) | 22.0 (12) | 22.0 (12) | 22.0 (12) | 26.8 (12) | 24.9 (12) | 17.2 (11) |
| GPT-5.5 (xhigh) | 21.3 (13) | 20.6 (15) | 20.8 (14) | 21.1 (13) | 21.5 (13) | 21.8 (13) | 21.3 (13) | 26.3 (15) | 24.3 (14) | 16.3 (13) |
| Claude Sonnet 5 (max) | 21.1 (14) | 20.8 (14) | 20.9 (13) | 21.0 (14) | 21.2 (14) | 21.3 (14) | 21.1 (14) | 26.5 (14) | 24.3 (13) | 15.7 (14) |
| DeepSeek V4 Flash (max) | 20.5 (15) | 20.9 (13) | 20.8 (15) | 20.6 (15) | 20.4 (15) | 20.3 (15) | 20.5 (15) | 26.6 (13) | 24.1 (15) | 14.5 (15) |
| GLM-5.3 Flash (max) | 19.6 (16) | 19.9 (16) | 19.8 (16) | 19.7 (16) | 19.5 (16) | 19.4 (16) | 19.6 (16) | 25.4 (16) | 23.0 (16) | 13.8 (16) |
| Gemini 3.7 Flash (medium) | 17.5 (17) | 17.2 (17) | 17.3 (17) | 17.4 (17) | 17.6 (17) | 17.6 (17) | 17.5 (17) | 22.2 (18) | 20.3 (18) | 12.7 (17) |
| Grok 4.5 (high) | 16.6 (18) | 16.5 (18) | 16.5 (18) | 16.6 (18) | 16.7 (18) | 16.8 (18) | 16.6 (18) | 23.2 (17) | 20.6 (17) | 10.1 (18) |
| Gemini 3.6 Flash (high) | 14.2 (19) | 14.0 (20) | 14.1 (20) | 14.1 (19) | 14.2 (19) | 14.3 (19) | 14.2 (19) | 20.8 (21) | 18.2 (20) | 7.5 (19) |
| Gemini 3.5 Flash (high) | 13.9 (20) | 14.2 (19) | 14.1 (19) | 14.0 (20) | 13.7 (21) | 13.6 (21) | 13.9 (20) | 21.0 (20) | 18.1 (21) | 6.7 (20) |
| Kimi K2.7 Code | 13.8 (21) | 13.7 (21) | 13.7 (21) | 13.7 (21) | 13.8 (20) | 13.8 (20) | 13.8 (21) | 21.6 (19) | 18.5 (19) | 5.9 (21) |
| Claude Sonnet 4.6 (high) | 10.9 (22) | 11.2 (22) | 11.1 (22) | 11.0 (22) | 10.9 (22) | 10.8 (22) | 10.9 (22) | 18.8 (22) | 15.7 (22) | 3.0 (22) |
| GPT-5.4 (xhigh) | 9.7 (23) | 8.9 (23) | 9.2 (23) | 9.4 (23) | 9.9 (23) | 10.2 (23) | 9.7 (23) | 16.4 (23) | 13.7 (23) | 3.0 (23) |
| Muse Spark 1.1 (xhigh) | 6.0 (24) | 6.0 (24) | 6.0 (24) | 6.0 (24) | 6.0 (24) | 6.0 (24) | 6.0 (24) | 13.4 (24) | 10.4 (24) | -1.4 (24) |
| Muse Spark 1.2 (xhigh) | 5.1 (25) | 5.5 (25) | 5.3 (25) | 5.2 (25) | 4.9 (25) | 4.8 (25) | 5.1 (25) | 11.7 (25) | 9.0 (25) | -1.5 (25) |
| Gemini 3.1 Pro Preview (high) | 1.9 (26) | 1.9 (26) | 1.9 (26) | 1.9 (26) | 1.9 (26) | 2.0 (26) | 1.9 (26) | 9.5 (26) | 6.5 (26) | -5.6 (26) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (0 of 6900 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Fable 5 (xhigh) | 332 | 0 | none |
| Claude Opus 4.8 (max) | 244 | 0 | none |
| Claude Opus 5 (max) | 328 | 0 | none |
| Claude Sonnet 4.6 (high) | 160 | 0 | Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| Claude Sonnet 5 (max) | 248 | 0 | none |
| DeepSeek V4 Flash (max) | 264 | 0 | Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| DeepSeek V4 Pro (max) | 324 | 0 | none |
| Gemini 3.1 Pro Preview (high) | 64 | 0 | none |
| Gemini 3.5 Flash (high) | 188 | 0 | none |
| Gemini 3.6 Flash (high) | 220 | 0 | Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| Gemini 3.7 Flash (medium) | 328 | 0 | Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| GLM-5.2 (max) | 232 | 0 | none |
| GLM-5.3 Flash (max) | 272 | 0 | GPT-5.5 (xhigh) 13→14, Claude Sonnet 5 (max) 14→13 |
| GLM-5.3 (max) | 320 | 0 | none |
| GPT-5.4 (xhigh) | 264 | 0 | Qwen3.8 Max (xhigh) 9→10, GLM-5.2 (max) 10→9 |
| GPT-5.5 (xhigh) | 328 | 0 | none |
| GPT-5.6 Luna (max) | 308 | 0 | none |
| GPT-5.6 Sol (max) | 352 | 0 | none |
| GPT-5.6 Terra (max) | 336 | 0 | none |
| Grok 4.5 (high) | 244 | 0 | none |
| Grok 4.6 (medium) | 292 | 0 | none |
| Kimi K2.7 Code | 152 | 0 | Grok 4.6 (medium) 7→8, DeepSeek V4 Pro (max) 8→7, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| Kimi K3 (max) | 308 | 0 | none |
| Muse Spark 1.1 (xhigh) | 252 | 0 | none |
| Muse Spark 1.2 (xhigh) | 268 | 0 | none |
| Qwen3.8 Max (xhigh) | 272 | 0 | none |
| (dedup panel) | 0 | 0 | none |

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| Effect-TS/effect (4) | Qwen3.8 Max (xhigh) 9→10, GLM-5.2 (max) 10→9, Claude Opus 5 (max) 12→13, GPT-5.5 (xhigh) 13→14, Claude Sonnet 5 (max) 14→12 |
| TanStack/query (4) | DeepSeek V4 Pro (max) 8→10, Qwen3.8 Max (xhigh) 9→8, GLM-5.2 (max) 10→11, GPT-5.6 Luna (max) 11→14, Claude Opus 5 (max) 12→9, GPT-5.5 (xhigh) 13→12, Claude Sonnet 5 (max) 14→13 |
| arktypeio/arktype (4) | Grok 4.6 (medium) 7→10, DeepSeek V4 Pro (max) 8→7, Qwen3.8 Max (xhigh) 9→11, GLM-5.2 (max) 10→8, GPT-5.6 Luna (max) 11→9, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→19 |
| baryhuang/claude-code-by-agents (4) | DeepSeek V4 Pro (max) 8→9, Qwen3.8 Max (xhigh) 9→8, GLM-5.2 (max) 10→11, GPT-5.6 Luna (max) 11→13, Claude Opus 5 (max) 12→10, GPT-5.5 (xhigh) 13→14, Claude Sonnet 5 (max) 14→12, DeepSeek V4 Flash (max) 15→16, GLM-5.3 Flash (max) 16→15, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→19 |
| bombshell-dev/clack (4) | GLM-5.3 (max) 6→9, DeepSeek V4 Pro (max) 8→6, Qwen3.8 Max (xhigh) 9→8, GLM-5.2 (max) 10→11, GPT-5.6 Luna (max) 11→10, Claude Opus 5 (max) 12→13, GPT-5.5 (xhigh) 13→12, Claude Sonnet 5 (max) 14→15, DeepSeek V4 Flash (max) 15→14, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→19 |
| c4spar/cliffy (4) | Grok 4.6 (medium) 7→8, DeepSeek V4 Pro (max) 8→10, Qwen3.8 Max (xhigh) 9→7, GLM-5.2 (max) 10→11, GPT-5.6 Luna (max) 11→9, Gemini 3.6 Flash (high) 19→21, Gemini 3.5 Flash (high) 20→19, Kimi K2.7 Code 21→20, Claude Sonnet 4.6 (high) 22→23, GPT-5.4 (xhigh) 23→22 |
| capricorn86/happy-dom (8) | GLM-5.3 (max) 6→9, Grok 4.6 (medium) 7→6, DeepSeek V4 Pro (max) 8→7, Qwen3.8 Max (xhigh) 9→11, GPT-5.6 Luna (max) 11→8, Claude Opus 5 (max) 12→14, GPT-5.5 (xhigh) 13→12, Claude Sonnet 5 (max) 14→15, DeepSeek V4 Flash (max) 15→13, GLM-5.3 Flash (max) 16→17, Gemini 3.7 Flash (medium) 17→16 |
| dahlia/optique (4) | GLM-5.3 (max) 6→8, Grok 4.6 (medium) 7→9, DeepSeek V4 Pro (max) 8→7, Qwen3.8 Max (xhigh) 9→10, GLM-5.2 (max) 10→6, DeepSeek V4 Flash (max) 15→16, GLM-5.3 Flash (max) 16→15, Gemini 3.6 Flash (high) 19→21, Gemini 3.5 Flash (high) 20→19, Kimi K2.7 Code 21→20 |
| drizzle-team/drizzle-orm (4) | Grok 4.6 (medium) 7→9, DeepSeek V4 Pro (max) 8→7, Qwen3.8 Max (xhigh) 9→8, GPT-5.6 Luna (max) 11→12, Claude Opus 5 (max) 12→11, GPT-5.5 (xhigh) 13→14, Claude Sonnet 5 (max) 14→13, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→19 |
| dynamodb-toolbox/dynamodb-toolbox (8) | Claude Opus 4.8 (max) 3→4, GPT-5.6 Sol (max) 4→3, Grok 4.6 (medium) 7→11, DeepSeek V4 Pro (max) 8→9, Qwen3.8 Max (xhigh) 9→7, GLM-5.2 (max) 10→8, GPT-5.6 Luna (max) 11→10, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| eicrud/eicrud (4) | GLM-5.2 (max) 10→12, GPT-5.6 Luna (max) 11→10, Claude Opus 5 (max) 12→11, DeepSeek V4 Flash (max) 15→16, GLM-5.3 Flash (max) 16→15, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→19 |
| flightcontrolhq/superjson (4) | GLM-5.3 (max) 6→7, Grok 4.6 (medium) 7→9, DeepSeek V4 Pro (max) 8→6, Qwen3.8 Max (xhigh) 9→10, GLM-5.2 (max) 10→8, GPT-5.6 Luna (max) 11→12, Claude Opus 5 (max) 12→11, GPT-5.5 (xhigh) 13→16, DeepSeek V4 Flash (max) 15→13, GLM-5.3 Flash (max) 16→15, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17 |
| gvergnaud/ts-pattern (4) | GLM-5.3 (max) 6→7, Grok 4.6 (medium) 7→6, DeepSeek V4 Pro (max) 8→9, Qwen3.8 Max (xhigh) 9→8, Claude Opus 5 (max) 12→13, GPT-5.5 (xhigh) 13→12, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| jeffijoe/awilix (4) | DeepSeek V4 Pro (max) 8→10, Qwen3.8 Max (xhigh) 9→8, GLM-5.2 (max) 10→12, GPT-5.6 Luna (max) 11→9, Claude Opus 5 (max) 12→11, GPT-5.5 (xhigh) 13→15, Claude Sonnet 5 (max) 14→13, DeepSeek V4 Flash (max) 15→14, Claude Sonnet 4.6 (high) 22→23, GPT-5.4 (xhigh) 23→22 |
| keajs/kea (4) | GLM-5.3 (max) 6→8, DeepSeek V4 Pro (max) 8→6, GLM-5.2 (max) 10→11, GPT-5.6 Luna (max) 11→10, GPT-5.5 (xhigh) 13→15, Claude Sonnet 5 (max) 14→13, DeepSeek V4 Flash (max) 15→14, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17, Gemini 3.6 Flash (high) 19→21, Kimi K2.7 Code 21→19 |
| kysely-org/kysely (4) | GLM-5.3 (max) 6→8, Grok 4.6 (medium) 7→12, DeepSeek V4 Pro (max) 8→6, Qwen3.8 Max (xhigh) 9→10, GLM-5.2 (max) 10→7, GPT-5.6 Luna (max) 11→9, Claude Opus 5 (max) 12→11, GPT-5.5 (xhigh) 13→15, Claude Sonnet 5 (max) 14→13, DeepSeek V4 Flash (max) 15→14, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→19 |
| meriyah/meriyah (4) | GPT-5.6 Luna (max) 11→13, Claude Opus 5 (max) 12→11, GPT-5.5 (xhigh) 13→15, Claude Sonnet 5 (max) 14→12, DeepSeek V4 Flash (max) 15→14, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| open-circle/valibot (4) | GPT-5.6 Terra (max) 5→6, GLM-5.3 (max) 6→5, DeepSeek V4 Pro (max) 8→9, Qwen3.8 Max (xhigh) 9→8, GPT-5.6 Luna (max) 11→13, Claude Opus 5 (max) 12→11, GPT-5.5 (xhigh) 13→15, Claude Sonnet 5 (max) 14→12, DeepSeek V4 Flash (max) 15→14 |
| platers/obsidian-linter (12) | GLM-5.3 (max) 6→7, Grok 4.6 (medium) 7→6, DeepSeek V4 Pro (max) 8→9, Qwen3.8 Max (xhigh) 9→12, GPT-5.6 Luna (max) 11→8, Claude Opus 5 (max) 12→13, GPT-5.5 (xhigh) 13→11, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17, Gemini 3.6 Flash (high) 19→21, Gemini 3.5 Flash (high) 20→19, Kimi K2.7 Code 21→20, Claude Sonnet 4.6 (high) 22→23, GPT-5.4 (xhigh) 23→22 |
| pmndrs/koota (16) | GLM-5.3 (max) 6→10, Grok 4.6 (medium) 7→9, DeepSeek V4 Pro (max) 8→7, Qwen3.8 Max (xhigh) 9→8, GLM-5.2 (max) 10→6, Claude Opus 5 (max) 12→16, GPT-5.5 (xhigh) 13→12, Claude Sonnet 5 (max) 14→13, DeepSeek V4 Flash (max) 15→14, GLM-5.3 Flash (max) 16→15, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→19 |
| slab/quill (4) | GLM-5.3 (max) 6→7, Grok 4.6 (medium) 7→6, DeepSeek V4 Pro (max) 8→9, Qwen3.8 Max (xhigh) 9→8, Claude Sonnet 5 (max) 14→16, DeepSeek V4 Flash (max) 15→14, GLM-5.3 Flash (max) 16→15, Gemini 3.5 Flash (high) 20→21, Kimi K2.7 Code 21→20 |
| sql-formatter-org/sql-formatter (4) | GLM-5.3 (max) 6→7, Grok 4.6 (medium) 7→6, GPT-5.6 Luna (max) 11→12, Claude Opus 5 (max) 12→11, Claude Sonnet 5 (max) 14→15, DeepSeek V4 Flash (max) 15→14, Gemini 3.6 Flash (high) 19→21, Kimi K2.7 Code 21→19 |
| true-myth/true-myth (4) | Grok 4.6 (medium) 7→9, DeepSeek V4 Pro (max) 8→7, Qwen3.8 Max (xhigh) 9→10, GLM-5.2 (max) 10→8, Claude Sonnet 5 (max) 14→15, DeepSeek V4 Flash (max) 15→14 |
| unjs/ofetch (4) | Qwen3.8 Max (xhigh) 9→11, GLM-5.2 (max) 10→9, GPT-5.6 Luna (max) 11→10, Claude Opus 5 (max) 12→13, GPT-5.5 (xhigh) 13→12, Gemini 3.5 Flash (high) 20→22, Kimi K2.7 Code 21→20, Claude Sonnet 4.6 (high) 22→21 |
| vadimdemedes/ink (4) | GLM-5.2 (max) 10→11, GPT-5.6 Luna (max) 11→12, Claude Opus 5 (max) 12→10, Claude Sonnet 5 (max) 14→15, DeepSeek V4 Flash (max) 15→14, Gemini 3.6 Flash (high) 19→20, Gemini 3.5 Flash (high) 20→19 |
| vitest-dev/vitest (4) | Grok 4.6 (medium) 7→8, DeepSeek V4 Pro (max) 8→9, Qwen3.8 Max (xhigh) 9→7, DeepSeek V4 Flash (max) 15→16, GLM-5.3 Flash (max) 16→15, Gemini 3.7 Flash (medium) 17→18, Grok 4.5 (high) 18→17, Gemini 3.6 Flash (high) 19→21, Gemini 3.5 Flash (high) 20→19, Kimi K2.7 Code 21→20 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (110) | Solved by fewer (110) |
|---|---:|---:|
| Claude Fable 5 (xhigh) | 42.3 (1) | 42.3 (1) |
| Kimi K3 (max) | 33.1 (2) | 33.1 (2) |
| Claude Opus 4.8 (max) | 31.0 (3) | 31.0 (3) |
| GPT-5.6 Sol (max) | 29.5 (4) | 29.5 (4) |
| GPT-5.6 Terra (max) | 26.3 (5) | 26.3 (5) |
| GLM-5.3 (max) | 24.5 (6) | 24.5 (6) |
| Grok 4.6 (medium) | 24.1 (7) | 24.1 (7) |
| DeepSeek V4 Pro (max) | 23.8 (8) | 23.8 (8) |
| Qwen3.8 Max (xhigh) | 23.5 (9) | 23.5 (9) |
| GLM-5.2 (max) | 23.2 (10) | 23.2 (10) |
| GPT-5.6 Luna (max) | 22.6 (11) | 22.6 (11) |
| Claude Opus 5 (max) | 22.0 (12) | 22.0 (12) |
| GPT-5.5 (xhigh) | 21.3 (13) | 21.3 (13) |
| Claude Sonnet 5 (max) | 21.1 (14) | 21.1 (14) |
| DeepSeek V4 Flash (max) | 20.5 (15) | 20.5 (15) |
| GLM-5.3 Flash (max) | 19.6 (16) | 19.6 (16) |
| Gemini 3.7 Flash (medium) | 17.5 (17) | 17.5 (17) |
| Grok 4.5 (high) | 16.6 (18) | 16.6 (18) |
| Gemini 3.6 Flash (high) | 14.2 (19) | 14.2 (19) |
| Gemini 3.5 Flash (high) | 13.9 (20) | 13.9 (20) |
| Kimi K2.7 Code | 13.8 (21) | 13.8 (21) |
| Claude Sonnet 4.6 (high) | 10.9 (22) | 10.9 (22) |
| GPT-5.4 (xhigh) | 9.7 (23) | 9.7 (23) |
| Muse Spark 1.1 (xhigh) | 6.0 (24) | 6.0 (24) |
| Muse Spark 1.2 (xhigh) | 5.1 (25) | 5.1 (25) |
| Gemini 3.1 Pro Preview (high) | 1.9 (26) | 1.9 (26) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **Claude Fable 5 (xhigh) − Kimi K3 (max) = 9.19**: failed/failed -0.07 (35), failed/solved -7.29 (14), solved/failed 12.60 (20), solved/solved 3.95 (63). For Claude Fable 5 (xhigh): `koota-query-predicates#1` +0.84 (solved/failed), `obsidian-linter-link-format-conversion#4` +0.83 (solved/failed), `koota-composite-trait-aspects#4` +0.81 (solved/failed). For Kimi K3 (max): `eicrud-keyset-pagination-cursor#2` -0.76 (failed/solved), `optique-conditional-option-dependencies#3` -0.74 (failed/solved), `optique-conditional-option-dependencies#4` -0.69 (failed/solved).
- **Kimi K3 (max) − Claude Opus 4.8 (max) = 3.91**: failed/failed -0.15 (35), failed/solved -8.10 (13), solved/failed 16.27 (27), solved/solved -4.11 (48). For Kimi K3 (max): `ts-pattern-match-each#3` +0.91 (solved/failed), `eicrud-keyset-pagination-cursor#2` +0.83 (solved/failed), `koota-query-predicates#2` +0.82 (solved/failed). For Claude Opus 4.8 (max): `dynamodb-toolbox-lazy-recursive-schemas#4` -0.85 (failed/solved), `claude-code-by-agents-recursive-delegation#1` -0.80 (failed/solved), `koota-pair-relation-tracking#3` -0.79 (failed/solved).
- **Claude Opus 4.8 (max) − GPT-5.6 Sol (max) = 2.21**: failed/failed 0.41 (31), failed/solved -14.17 (31), solved/failed 7.94 (12), solved/solved 8.03 (49). For Claude Opus 4.8 (max): `arktype-json-schema-refs-dependencies#1` +0.87 (solved/failed), `claude-code-by-agents-recursive-delegation#1` +0.81 (solved/failed), `koota-pair-relation-tracking#3` +0.79 (solved/failed). For GPT-5.6 Sol (max): `query-persist-restored-query-state#2` -0.85 (failed/solved), `koota-composite-trait-aspects#4` -0.74 (failed/solved), `vitest-duration-sharding#3` -0.72 (failed/solved).
- **GPT-5.6 Sol (max) − GPT-5.6 Terra (max) = 3.52**: failed/failed 0.08 (30), failed/solved -6.24 (14), solved/failed 7.37 (17), solved/solved 2.31 (70). For GPT-5.6 Sol (max): `query-persist-restored-query-state#2` +0.78 (solved/failed), `arktype-json-schema-refs-dependencies#4` +0.72 (solved/failed), `arktype-json-schema-refs-dependencies#2` +0.68 (solved/failed). For GPT-5.6 Terra (max): `meriyah-explicit-resource-declarations#2` -0.84 (failed/solved), `meriyah-explicit-resource-declarations#1` -0.80 (failed/solved), `effect-sse-httpapi-streaming#1` -0.67 (failed/solved).
- **GPT-5.6 Terra (max) − GLM-5.3 (max) = 1.64**: failed/failed -0.06 (27), failed/solved -9.17 (20), solved/failed 10.39 (25), solved/solved 0.49 (59). For GPT-5.6 Terra (max): `meriyah-explicit-resource-declarations#2` +0.84 (solved/failed), `meriyah-explicit-resource-declarations#1` +0.80 (solved/failed), `koota-composite-trait-aspects#4` +0.72 (solved/failed). For GLM-5.3 (max): `koota-query-predicates#2` -0.73 (failed/solved), `koota-query-predicates#4` -0.72 (failed/solved), `obsidian-linter-scoped-ignore-markers#2` -0.70 (failed/solved).
- **GLM-5.3 (max) − Grok 4.6 (medium) = 0.42**: failed/failed 0.18 (38), failed/solved -7.24 (14), solved/failed 9.42 (21), solved/solved -1.93 (59). For GLM-5.3 (max): `ts-pattern-match-each#4` +0.84 (solved/failed), `koota-composite-trait-aspects#1` +0.79 (solved/failed), `optique-conditional-option-dependencies#1` +0.73 (solved/failed). For Grok 4.6 (medium): `optique-conditional-option-dependencies#3` -0.81 (failed/solved), `ts-pattern-match-each#1` -0.80 (failed/solved), `koota-deferred-mutation-buffer#3` -0.74 (failed/solved).
- **Grok 4.6 (medium) − DeepSeek V4 Pro (max) = 0.31**: failed/failed 0.05 (31), failed/solved -11.30 (28), solved/failed 10.14 (20), solved/solved 1.42 (53). For Grok 4.6 (medium): `true-myth-iterable-collection-combinators#1` +0.79 (solved/failed), `koota-deferred-mutation-buffer#3` +0.76 (solved/failed), `superjson-error-stack-serialization#4` +0.76 (solved/failed). For DeepSeek V4 Pro (max): `koota-deferred-mutation-buffer#2` -0.76 (failed/solved), `query-persist-restored-query-state#1` -0.74 (failed/solved), `query-persist-restored-query-state#3` -0.71 (failed/solved).
- **DeepSeek V4 Pro (max) − Qwen3.8 Max (xhigh) = 0.89**: failed/failed -0.16 (33), failed/solved -8.86 (17), solved/failed 11.03 (28), solved/solved -1.13 (51). For DeepSeek V4 Pro (max): `claude-code-by-agents-recursive-delegation#3` +0.73 (solved/failed), `ts-pattern-match-each#1` +0.70 (solved/failed), `valibot-recursive-schema-composition#2` +0.66 (solved/failed). For Qwen3.8 Max (xhigh): `superjson-error-stack-serialization#1` -0.84 (failed/solved), `happy-dom-deterministic-intersectionobserver#4` -0.77 (failed/solved), `effect-sse-httpapi-streaming#2` -0.74 (failed/solved).
- **Qwen3.8 Max (xhigh) − GLM-5.2 (max) = -0.33**: failed/failed -0.98 (43), failed/solved -11.36 (18), solved/failed 16.41 (29), solved/solved -4.39 (39). For Qwen3.8 Max (xhigh): `kysely-window-grouping-helpers#4` +0.83 (solved/failed), `superjson-error-stack-serialization#1` +0.83 (solved/failed), `arktype-json-schema-refs-dependencies#2` +0.78 (solved/failed). For GLM-5.2 (max): `ink-grid-box-layout#2` -0.87 (failed/solved), `kea-atomic-signal-selectors#4` -0.87 (failed/solved), `ts-pattern-match-each#2` -0.83 (failed/solved).
- **GLM-5.2 (max) − GPT-5.6 Luna (max) = 1.27**: failed/failed 1.03 (31), failed/solved -15.20 (40), solved/failed 11.76 (20), solved/solved 3.68 (37). For GLM-5.2 (max): `kea-atomic-signal-selectors#4` +0.88 (solved/failed), `obsidian-linter-scoped-ignore-markers#3` +0.83 (solved/failed), `kea-atomic-signal-selectors#2` +0.81 (solved/failed). For GPT-5.6 Luna (max): `koota-pair-relation-tracking#4` -0.79 (failed/solved), `ts-pattern-match-each#3` -0.75 (failed/solved), `koota-deferred-mutation-buffer#1` -0.72 (failed/solved).
- **GPT-5.6 Luna (max) − Claude Opus 5 (max) = 1.29**: failed/failed -0.15 (17), failed/solved -14.34 (32), solved/failed 12.13 (30), solved/solved 3.65 (47). For GPT-5.6 Luna (max): `sql-formatter-bigquery-pipe-formatting#1` +0.81 (solved/failed), `superjson-error-stack-serialization#2` +0.76 (solved/failed), `koota-deferred-mutation-buffer#1` +0.73 (solved/failed). For Claude Opus 5 (max): `obsidian-linter-auto-table-of-contents#4` -0.86 (failed/solved), `ts-pattern-match-each#1` -0.80 (failed/solved), `effect-sse-httpapi-streaming#4` -0.80 (failed/solved).
- **Claude Opus 5 (max) − GPT-5.5 (xhigh) = 0.18**: failed/failed 0.10 (24), failed/solved -10.57 (23), solved/failed 10.04 (25), solved/solved 0.60 (57). For Claude Opus 5 (max): `obsidian-linter-auto-table-of-contents#4` +0.83 (solved/failed), `effect-sse-httpapi-streaming#4` +0.79 (solved/failed), `ts-pattern-match-each#1` +0.79 (solved/failed). For GPT-5.5 (xhigh): `superjson-error-stack-serialization#4` -0.80 (failed/solved), `kysely-window-grouping-helpers#1` -0.69 (failed/solved), `meriyah-explicit-resource-declarations#4` -0.69 (failed/solved).
- **GPT-5.5 (xhigh) − Claude Sonnet 5 (max) = 0.45**: failed/failed -0.39 (32), failed/solved -9.46 (17), solved/failed 13.73 (36), solved/solved -3.43 (45). For GPT-5.5 (xhigh): `meriyah-explicit-resource-declarations#4` +0.71 (solved/failed), `drizzle-orm-window-function-builders#2` +0.70 (solved/solved), `superjson-error-stack-serialization#4` +0.70 (solved/failed). For Claude Sonnet 5 (max): `koota-deferred-mutation-buffer#4` -0.86 (failed/solved), `quill-shared-toolbar-focus#1` -0.84 (failed/solved), `quill-shared-toolbar-focus#4` -0.78 (failed/solved).
- **Claude Sonnet 5 (max) − DeepSeek V4 Flash (max) = 0.23**: failed/failed 0.70 (46), failed/solved -11.21 (22), solved/failed 10.72 (19), solved/solved 0.02 (43). For Claude Sonnet 5 (max): `superjson-error-stack-serialization#1` +0.84 (solved/failed), `quill-shared-toolbar-focus#1` +0.84 (solved/failed), `koota-query-predicates#1` +0.82 (solved/failed). For DeepSeek V4 Flash (max): `cliffy-config-file-parsing#4` -0.85 (failed/solved), `dynamodb-toolbox-lazy-recursive-schemas#3` -0.78 (failed/solved), `vitest-duration-sharding#4` -0.78 (failed/solved).
- **DeepSeek V4 Flash (max) − GLM-5.3 Flash (max) = 1.32**: failed/failed -0.10 (43), failed/solved -11.02 (22), solved/failed 9.32 (20), solved/solved 3.12 (46). For DeepSeek V4 Flash (max): `cliffy-config-file-parsing#4` +0.85 (solved/failed), `claude-code-by-agents-recursive-delegation#1` +0.79 (solved/failed), `koota-pair-relation-tracking#3` +0.79 (solved/failed). For GLM-5.3 Flash (max): `arktype-json-schema-refs-dependencies#2` -0.83 (failed/solved), `effect-sse-httpapi-streaming#3` -0.83 (failed/solved), `clack-async-autocomplete-options#3` -0.76 (failed/solved).
- **GLM-5.3 Flash (max) − Gemini 3.7 Flash (medium) = 2.05**: failed/failed 0.09 (31), failed/solved -12.25 (32), solved/failed 9.50 (19), solved/solved 4.71 (49). For GLM-5.3 Flash (max): `effect-sse-httpapi-streaming#3` +0.85 (solved/failed), `arktype-json-schema-refs-dependencies#2` +0.79 (solved/failed), `happy-dom-deterministic-intersectionobserver#2` +0.73 (solved/failed). For Gemini 3.7 Flash (medium): `obsidian-linter-link-format-conversion#3` -0.77 (failed/solved), `kysely-window-grouping-helpers#1` -0.71 (failed/solved), `eicrud-keyset-pagination-cursor#2` -0.71 (failed/solved).
- **Gemini 3.7 Flash (medium) − Grok 4.5 (high) = 0.82**: failed/failed -0.11 (33), failed/solved -7.21 (17), solved/failed 14.64 (38), solved/solved -6.50 (44). For Gemini 3.7 Flash (medium): `obsidian-linter-link-format-conversion#3` +0.77 (solved/failed), `kysely-window-grouping-helpers#1` +0.71 (solved/failed), `eicrud-keyset-pagination-cursor#2` +0.68 (solved/failed). For Grok 4.5 (high): `ink-grid-box-layout#4` -0.74 (failed/solved), `arktype-json-schema-refs-dependencies#2` -0.72 (failed/solved), `koota-pair-relation-tracking#3` -0.67 (failed/solved).
- **Grok 4.5 (high) − Gemini 3.6 Flash (high) = 2.48**: failed/failed -0.31 (49), failed/solved -12.14 (22), solved/failed 13.38 (28), solved/solved 1.55 (33). For Grok 4.5 (high): `dynamodb-toolbox-conditional-attribute-requirements#2` +0.81 (solved/failed), `ink-grid-box-layout#4` +0.73 (solved/failed), `arktype-json-schema-refs-dependencies#2` +0.72 (solved/failed). For Gemini 3.6 Flash (high): `obsidian-linter-scoped-ignore-markers#3` -0.81 (failed/solved), `kea-atomic-signal-selectors#4` -0.78 (failed/solved), `vitest-duration-sharding#1` -0.77 (failed/solved).
- **Gemini 3.6 Flash (high) − Gemini 3.5 Flash (high) = 0.32**: failed/failed -0.18 (62), failed/solved -9.25 (15), solved/failed 13.30 (23), solved/solved -3.54 (32). For Gemini 3.6 Flash (high): `sql-formatter-bigquery-pipe-formatting#1` +0.84 (solved/failed), `obsidian-linter-scoped-ignore-markers#3` +0.80 (solved/failed), `kea-atomic-signal-selectors#4` +0.79 (solved/failed). For Gemini 3.5 Flash (high): `valibot-recursive-schema-composition#2` -0.84 (failed/solved), `dynamodb-toolbox-lazy-recursive-schemas#1` -0.82 (failed/solved), `koota-deferred-mutation-buffer#2` -0.81 (failed/solved).
- **Gemini 3.5 Flash (high) − Kimi K2.7 Code = 0.08**: failed/failed -0.05 (67), failed/solved -12.16 (18), solved/failed 13.86 (27), solved/solved -1.57 (20). For Gemini 3.5 Flash (high): `dynamodb-toolbox-lazy-recursive-schemas#1` +0.81 (solved/failed), `kea-atomic-signal-selectors#2` +0.81 (solved/failed), `ofetch-per-origin-circuit-breaker#1` +0.81 (solved/failed). For Kimi K2.7 Code: `query-persist-restored-query-state#4` -0.84 (failed/solved), `optique-conditional-option-dependencies#1` -0.83 (failed/solved), `awilix-async-container-initialization#1` -0.83 (failed/solved).
- **Kimi K2.7 Code − Claude Sonnet 4.6 (high) = 2.47**: failed/failed 0.18 (71), failed/solved -12.24 (22), solved/failed 12.72 (19), solved/solved 1.81 (18). For Kimi K2.7 Code: `optique-conditional-option-dependencies#1` +0.84 (solved/failed), `drizzle-orm-window-function-builders#1` +0.84 (solved/failed), `query-persist-restored-query-state#2` +0.83 (solved/failed). For Claude Sonnet 4.6 (high): `query-persist-restored-query-state#1` -0.84 (failed/solved), `cliffy-config-file-parsing#3` -0.84 (failed/solved), `cliffy-config-file-parsing#1` -0.81 (failed/solved).
- **Claude Sonnet 4.6 (high) − GPT-5.4 (xhigh) = 1.14**: failed/failed 0.71 (51), failed/solved -13.07 (39), solved/failed 10.33 (14), solved/solved 3.17 (26). For Claude Sonnet 4.6 (high): `eicrud-keyset-pagination-cursor#3` +0.88 (solved/failed), `cliffy-config-file-parsing#3` +0.87 (solved/failed), `query-persist-restored-query-state#1` +0.85 (solved/failed). For GPT-5.4 (xhigh): `valibot-recursive-schema-composition#1` -0.80 (failed/solved), `meriyah-explicit-resource-declarations#1` -0.76 (failed/solved), `meriyah-explicit-resource-declarations#3` -0.75 (failed/solved).
- **GPT-5.4 (xhigh) − Muse Spark 1.1 (xhigh) = 3.68**: failed/failed 0.34 (40), failed/solved -8.84 (26), solved/failed 8.63 (29), solved/solved 3.54 (37). For GPT-5.4 (xhigh): `kysely-window-grouping-helpers#2` +0.73 (solved/failed), `happy-dom-abort-pending-body-reads#1` +0.57 (solved/failed), `vitest-duration-sharding#4` +0.55 (solved/solved). For Muse Spark 1.1 (xhigh): `sql-formatter-bigquery-pipe-formatting#3` -0.81 (failed/solved), `query-persist-restored-query-state#3` -0.75 (failed/solved), `drizzle-orm-window-function-builders#1` -0.67 (failed/solved).
- **Muse Spark 1.1 (xhigh) − Muse Spark 1.2 (xhigh) = 0.95**: failed/failed -0.14 (51), failed/solved -4.65 (18), solved/failed 3.10 (14), solved/solved 2.63 (49). For Muse Spark 1.1 (xhigh): `valibot-recursive-schema-composition#4` +0.58 (solved/failed), `ts-pattern-match-each#3` +0.43 (solved/solved), `query-persist-restored-query-state#3` +0.37 (solved/solved). For Muse Spark 1.2 (xhigh): `eicrud-keyset-pagination-cursor#1` -0.64 (failed/solved), `koota-query-predicates#1` -0.61 (failed/solved), `eicrud-keyset-pagination-cursor#2` -0.59 (failed/solved).
- **Muse Spark 1.2 (xhigh) − Gemini 3.1 Pro Preview (high) = 3.00**: failed/failed -2.57 (61), failed/solved -1.52 (2), solved/failed 12.10 (51), solved/solved -5.01 (14). For Muse Spark 1.2 (xhigh): `meriyah-explicit-resource-declarations#4` +0.66 (solved/failed), `eicrud-keyset-pagination-cursor#1` +0.61 (solved/failed), `valibot-recursive-schema-composition#1` +0.57 (solved/failed). For Gemini 3.1 Pro Preview (high): `meriyah-explicit-resource-declarations#3` -0.80 (failed/solved), `ts-pattern-match-each#4` -0.72 (failed/solved), `sql-formatter-bigquery-pipe-formatting#1` -0.71 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability examples/deepswe-typescript/score-panel.json examples/deepswe-typescript/*.jsonl --output examples/deepswe-typescript/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
