# Score sensitivity: 26 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `deepswe-v1.1-python-26-pooled-80-20-v0.5`: 132 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (121 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Fable 5 (xhigh) > Kimi K3 (max) ≈ Claude Opus 4.8 (max) ≈ Claude Sonnet 5 (max) ≈ GPT-5.6 Sol (max) ≈ Grok 4.6 (medium) ≈ GLM-5.3 Flash (max) ≈ Qwen3.8 Max (xhigh) ≈ GPT-5.6 Terra (max) ≈ Grok 4.5 (high) ≈ GLM-5.2 (max) ≈ GPT-5.5 (xhigh) ≈ DeepSeek V4 Flash (max) ≈ Gemini 3.7 Flash (medium) ≈ GLM-5.3 (max) ≈ Claude Opus 5 (max) ≈ DeepSeek V4 Pro (max) ≈ GPT-5.6 Luna (max) ≈ Gemini 3.6 Flash (high) ≈ Gemini 3.5 Flash (high) ≈ GPT-5.4 (xhigh) ≈ Claude Sonnet 4.6 (high) ≈ Kimi K2.7 Code ≈ Muse Spark 1.1 (xhigh) ≈ Muse Spark 1.2 (xhigh) ≈ Gemini 3.1 Pro Preview (high) (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (1 of 25 adjacent pairs): Claude Fable 5 (xhigh) > Kimi K3 (max).
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 24 pairs): Kimi K3 (max) vs Claude Opus 4.8 (max), Claude Opus 4.8 (max) vs Claude Sonnet 5 (max), Claude Sonnet 5 (max) vs GPT-5.6 Sol (max), GPT-5.6 Sol (max) vs Grok 4.6 (medium), Grok 4.6 (medium) vs GLM-5.3 Flash (max), GLM-5.3 Flash (max) vs Qwen3.8 Max (xhigh), Qwen3.8 Max (xhigh) vs GPT-5.6 Terra (max), GPT-5.6 Terra (max) vs Grok 4.5 (high), Grok 4.5 (high) vs GLM-5.2 (max), GLM-5.2 (max) vs GPT-5.5 (xhigh), GPT-5.5 (xhigh) vs DeepSeek V4 Flash (max), DeepSeek V4 Flash (max) vs Gemini 3.7 Flash (medium), Gemini 3.7 Flash (medium) vs GLM-5.3 (max), GLM-5.3 (max) vs Claude Opus 5 (max), Claude Opus 5 (max) vs DeepSeek V4 Pro (max), DeepSeek V4 Pro (max) vs GPT-5.6 Luna (max), GPT-5.6 Luna (max) vs Gemini 3.6 Flash (high), Gemini 3.6 Flash (high) vs Gemini 3.5 Flash (high), Gemini 3.5 Flash (high) vs GPT-5.4 (xhigh), GPT-5.4 (xhigh) vs Claude Sonnet 4.6 (high), Claude Sonnet 4.6 (high) vs Kimi K2.7 Code, Kimi K2.7 Code vs Muse Spark 1.1 (xhigh), Muse Spark 1.1 (xhigh) vs Muse Spark 1.2 (xhigh), Muse Spark 1.2 (xhigh) vs Gemini 3.1 Pro Preview (high).
- **Rank never changes under any variation**: Claude Fable 5 (xhigh) (1), Claude Sonnet 5 (max) (4), GPT-5.6 Sol (max) (5), Kimi K2.7 Code (23), Gemini 3.1 Pro Preview (high) (26).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 132 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Fable 5 (xhigh) | 53.2 | 40.9–65.0 | 53.2 | 1–1 | 1–2 | 0.96 |
| 2 | Kimi K3 (max) | 42.5 | 32.6–52.1 | 42.0–43.0 | 2–3 | 2–4 | 0.00 |
| 3 | Claude Opus 4.8 (max) | 42.4 | 31.0–54.4 | 41.9–42.8 | 2–3 | 2–5 | 0.02 |
| 4 | Claude Sonnet 5 (max) | 38.3 | 25.9–50.1 | 38.3 | 4–4 | 2–9 | 0.02 |
| 5 | GPT-5.6 Sol (max) | 33.2 | 21.6–44.3 | 32.3–34.2 | 5–5 | 3–10 | 0.00 |
| 6 | Grok 4.6 (medium) | 28.3 | 19.5–36.9 | 28.3 | 6–7 | 5–14 | 0.00 |
| 7 | GLM-5.3 Flash (max) | 26.9 | 18.0–36.0 | 25.9–27.9 | 7–9 | 5–15 | 0.00 |
| 8 | Qwen3.8 Max (xhigh) | 26.9 | 17.9–36.1 | 26.9 | 6–10 | 5–15 | 0.00 |
| 9 | GPT-5.6 Terra (max) | 26.5 | 17.6–35.9 | 26.5 | 7–10 | 5–15 | 0.00 |
| 10 | Grok 4.5 (high) | 25.4 | 17.0–34.2 | 25.4 | 8–10 | 6–16 | 0.00 |
| 11 | GLM-5.2 (max) | 22.9 | 12.5–34.3 | 22.0–23.9 | 11–16 | 5–20 | 0.00 |
| 12 | GPT-5.5 (xhigh) | 22.6 | 13.6–32.0 | 22.6 | 11–16 | 6–19 | 0.00 |
| 13 | DeepSeek V4 Flash (max) | 22.3 | 13.5–31.3 | 22.3 | 11–16 | 6–19 | 0.00 |
| 14 | Gemini 3.7 Flash (medium) | 22.2 | 12.7–32.0 | 22.2 | 11–16 | 6–19 | 0.00 |
| 15 | GLM-5.3 (max) | 22.0 | 14.8–29.9 | 21.5–22.4 | 11–17 | 6–19 | 0.00 |
| 16 | Claude Opus 5 (max) | 20.8 | 12.3–30.2 | 19.8–21.7 | 13–17 | 8–20 | 0.00 |
| 17 | DeepSeek V4 Pro (max) | 19.8 | 12.4–27.2 | 19.8 | 15–17 | 10–20 | 0.00 |
| 18 | GPT-5.6 Luna (max) | 17.4 | 10.0–25.8 | 17.4 | 18–19 | 12–21 | 0.00 |
| 19 | Gemini 3.6 Flash (high) | 15.2 | 5.3–25.2 | 15.1–15.3 | 18–19 | 12–23 | 0.00 |
| 20 | Gemini 3.5 Flash (high) | 12.5 | 3.0–23.3 | 12.4–12.6 | 20–21 | 13–25 | 0.00 |
| 21 | GPT-5.4 (xhigh) | 9.6 | 2.9–17.3 | 9.6 | 21–22 | 18–25 | 0.00 |
| 22 | Claude Sonnet 4.6 (high) | 9.6 | 1.7–17.9 | 9.6 | 20–22 | 17–25 | 0.00 |
| 23 | Kimi K2.7 Code | 7.1 | 1.0–13.8 | 7.1 | 23–23 | 20–25 | 0.00 |
| 24 | Muse Spark 1.1 (xhigh) | 4.7 | -0.8–10.3 | 4.7 | 24–25 | 21–25 | 0.00 |
| 25 | Muse Spark 1.2 (xhigh) | 4.2 | -1.6–10.1 | 4.2 | 24–25 | 21–26 | 0.00 |
| 26 | Gemini 3.1 Pro Preview (high) | -0.7 | -6.1–6.0 | -0.8–-0.6 | 26–26 | 24–26 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Fable 5 (xhigh) > Kimi K3 (max) | 10.68 | 3.40 to 18.43 | 1.00 | none | yes |
| Kimi K3 (max) > Claude Opus 4.8 (max) | 0.14 | -9.88 to 10.71 | 0.41 | net weight=1, failure cap=0, failure cap=10, panel without Claude Opus 4.8 (max), panel without Gemini 3.5 Flash (high), without Fatal1ty/mashumaro, without Textualize/textual, without aio-libs/aiomonitor, without celery/kombu, without dateutil/dateutil, without encode/httpx, without fastapi/fastapi, without fgmacedo/python-statemachine, without ipython/ipython, without jkwill87/mnamer, without simonw/sqlite-utils, without tconbeer/sqlfmt | no |
| Claude Opus 4.8 (max) > Claude Sonnet 5 (max) | 4.04 | -8.82 to 16.83 | 0.72 | none | yes |
| Claude Sonnet 5 (max) > GPT-5.6 Sol (max) | 5.10 | -10.62 to 20.93 | 0.71 | none | yes |
| GPT-5.6 Sol (max) > Grok 4.6 (medium) | 4.93 | -6.70 to 15.24 | 0.77 | none | yes |
| Grok 4.6 (medium) > GLM-5.3 Flash (max) | 1.39 | -9.39 to 11.38 | 0.53 | none | yes |
| GLM-5.3 Flash (max) > Qwen3.8 Max (xhigh) | 0.04 | -9.96 to 10.61 | 0.43 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=0, failure cap=10, panel without Claude Opus 5 (max), panel without Gemini 3.1 Pro Preview (high), panel without Gemini 3.5 Flash (high), panel without GLM-5.3 Flash (max), panel without GLM-5.3 (max), panel without GPT-5.4 (xhigh), panel without GPT-5.5 (xhigh), panel without GPT-5.6 Luna (max), panel without Muse Spark 1.1 (xhigh), panel without Muse Spark 1.2 (xhigh), without Fatal1ty/mashumaro, without Gallopsled/pwntools, without PyCQA/bandit, without Textualize/textual, without dateutil/dateutil, without ipython/ipython, without langchain-ai/langchain, without narwhals-dev/narwhals, without numba/numba, without reagento/adaptix, without simonw/sqlite-utils, without skrub-data/skrub | no |
| Qwen3.8 Max (xhigh) > GPT-5.6 Terra (max) | 0.32 | -9.02 to 9.90 | 0.52 | net weight=1, failure cap=50, without aio-libs/aiomonitor, without celery/kombu, without dry-python/returns, without fastapi/fastapi, without fgmacedo/python-statemachine, without google/mobly, without nidhaloff/igel, without psd-tools/psd-tools, without python-attrs/cattrs, without python-poetry/tomlkit, without skrub-data/skrub | yes |
| GPT-5.6 Terra (max) > Grok 4.5 (high) | 1.14 | -8.57 to 10.50 | 0.60 | without fastapi/fastapi, without numba/numba, without reagento/adaptix | yes |
| Grok 4.5 (high) > GLM-5.2 (max) | 2.47 | -10.61 to 15.11 | 0.60 | none | yes |
| GLM-5.2 (max) > GPT-5.5 (xhigh) | 0.37 | -14.79 to 15.83 | 0.45 | failure cap=50, panel without Grok 4.6 (medium), without Gallopsled/pwntools, without fastapi/fastapi, without fgmacedo/python-statemachine, without graphql-python/gql, without ipython/ipython, without jendrikseipp/vulture, without langchain-ai/langchain, without narwhals-dev/narwhals, without nidhaloff/igel, without psd-tools/psd-tools, without python-attrs/cattrs, without tconbeer/sqlfmt | no |
| GPT-5.5 (xhigh) > DeepSeek V4 Flash (max) | 0.23 | -11.30 to 11.47 | 0.52 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, panel without GPT-5.6 Luna (max), panel without Muse Spark 1.1 (xhigh), without Gallopsled/pwntools, without PyCQA/bandit, without Textualize/textual, without aio-libs/aiomonitor, without encode/httpx, without fastapi/fastapi, without google/mobly, without langchain-ai/langchain, without numba/numba, without reagento/adaptix, without simonw/sqlite-utils, without tconbeer/sqlfmt | yes |
| DeepSeek V4 Flash (max) > Gemini 3.7 Flash (medium) | 0.19 | -9.44 to 10.02 | 0.50 | failure cap=50, panel without GPT-5.6 Sol (max), without Fatal1ty/mashumaro, without PyCQA/bandit, without dry-python/returns, without encode/httpx, without fastapi/fastapi, without fgmacedo/python-statemachine, without nidhaloff/igel, without skrub-data/skrub | yes |
| Gemini 3.7 Flash (medium) > GLM-5.3 (max) | 0.19 | -13.45 to 13.67 | 0.47 | failure cap=50, panel without Claude Fable 5 (xhigh), panel without Claude Opus 4.8 (max), panel without Kimi K3 (max), panel without Muse Spark 1.1 (xhigh), without Fatal1ty/mashumaro, without aio-libs/aiomonitor, without dateutil/dateutil, without google/mobly, without ipython/ipython, without jendrikseipp/vulture, without jkwill87/mnamer, without narwhals-dev/narwhals, without psd-tools/psd-tools, without python-attrs/cattrs, without python-poetry/tomlkit, without tconbeer/sqlfmt | no |
| GLM-5.3 (max) > Claude Opus 5 (max) | 1.17 | -7.15 to 10.02 | 0.47 | without PyCQA/bandit, without celery/kombu | no |
| Claude Opus 5 (max) > DeepSeek V4 Pro (max) | 0.97 | -10.06 to 12.89 | 0.51 | failure cap=0, failure cap=10, without Textualize/textual, without fastapi/fastapi, without langchain-ai/langchain, without skrub-data/skrub | yes |
| DeepSeek V4 Pro (max) > GPT-5.6 Luna (max) | 2.46 | -6.24 to 10.70 | 0.72 | none | yes |
| GPT-5.6 Luna (max) > Gemini 3.6 Flash (high) | 2.17 | -9.61 to 13.56 | 0.64 | failure cap=0 | yes |
| Gemini 3.6 Flash (high) > Gemini 3.5 Flash (high) | 2.64 | -5.55 to 10.64 | 0.73 | none | yes |
| Gemini 3.5 Flash (high) > GPT-5.4 (xhigh) | 2.94 | -8.80 to 14.66 | 0.69 | none | yes |
| GPT-5.4 (xhigh) > Claude Sonnet 4.6 (high) | 0.00 | -10.08 to 10.30 | 0.49 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=0, failure cap=10, panel without Claude Opus 5 (max), panel without Claude Sonnet 4.6 (high), panel without Gemini 3.6 Flash (high), panel without Gemini 3.7 Flash (medium), panel without GLM-5.3 Flash (max), panel without GLM-5.3 (max), panel without GPT-5.4 (xhigh), panel without GPT-5.5 (xhigh), panel without GPT-5.6 Luna (max), panel without GPT-5.6 Sol (max), panel without Grok 4.5 (high), panel without Muse Spark 1.1 (xhigh), panel without Muse Spark 1.2 (xhigh), without Fatal1ty/mashumaro, without PyCQA/bandit, without aio-libs/aiomonitor, without celery/kombu, without fastapi/fastapi, without google/mobly, without jkwill87/mnamer, without narwhals-dev/narwhals, without nidhaloff/igel, without numba/numba, without psd-tools/psd-tools, without reagento/adaptix, without simonw/sqlite-utils, without tconbeer/sqlfmt | yes |
| Claude Sonnet 4.6 (high) > Kimi K2.7 Code | 2.52 | -6.22 to 11.65 | 0.71 | none | yes |
| Kimi K2.7 Code > Muse Spark 1.1 (xhigh) | 2.37 | -4.15 to 8.77 | 0.76 | none | yes |
| Muse Spark 1.1 (xhigh) > Muse Spark 1.2 (xhigh) | 0.54 | -2.98 to 3.96 | 0.60 | without ipython/ipython | yes |
| Muse Spark 1.2 (xhigh) > Gemini 3.1 Pro Preview (high) | 4.86 | -2.95 to 12.23 | 0.90 | none | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 53.2 (1) | 53.4 (1) | 53.3 (1) | 53.3 (1) | 53.1 (1) | 53.0 (1) | 53.2 (1) | 55.8 (1) | 54.8 (1) | 50.5 (1) |
| Kimi K3 (max) | 42.5 (2) | 42.7 (2) | 42.6 (2) | 42.5 (2) | 42.4 (2) | 42.4 (3) | 42.5 (2) | 45.8 (3) | 44.5 (3) | 39.1 (2) |
| Claude Opus 4.8 (max) | 42.4 (3) | 42.2 (3) | 42.3 (3) | 42.3 (3) | 42.4 (3) | 42.4 (2) | 42.4 (3) | 46.4 (2) | 44.8 (2) | 38.3 (3) |
| Claude Sonnet 5 (max) | 38.3 (4) | 38.0 (4) | 38.1 (4) | 38.2 (4) | 38.4 (4) | 38.5 (4) | 38.3 (4) | 42.7 (4) | 40.9 (4) | 34.0 (4) |
| GPT-5.6 Sol (max) | 33.2 (5) | 32.9 (5) | 33.0 (5) | 33.1 (5) | 33.3 (5) | 33.4 (5) | 33.2 (5) | 36.6 (5) | 35.2 (5) | 29.9 (5) |
| Grok 4.6 (medium) | 28.3 (6) | 28.2 (6) | 28.2 (6) | 28.3 (6) | 28.3 (6) | 28.3 (6) | 28.3 (6) | 32.5 (6) | 30.8 (6) | 24.1 (6) |
| GLM-5.3 Flash (max) | 26.9 (7) | 26.9 (8) | 26.9 (8) | 26.9 (8) | 26.9 (7) | 26.9 (7) | 26.9 (7) | 30.6 (9) | 29.1 (8) | 23.2 (7) |
| Qwen3.8 Max (xhigh) | 26.9 (8) | 27.0 (7) | 27.0 (7) | 26.9 (7) | 26.8 (8) | 26.8 (9) | 26.9 (8) | 31.9 (7) | 29.9 (7) | 21.8 (9) |
| GPT-5.6 Terra (max) | 26.5 (9) | 26.2 (9) | 26.3 (9) | 26.4 (9) | 26.7 (9) | 26.8 (8) | 26.5 (9) | 30.7 (8) | 29.0 (9) | 22.4 (8) |
| Grok 4.5 (high) | 25.4 (10) | 25.7 (10) | 25.6 (10) | 25.5 (10) | 25.3 (10) | 25.2 (10) | 25.4 (10) | 30.3 (10) | 28.4 (10) | 20.5 (10) |
| GLM-5.2 (max) | 22.9 (11) | 22.9 (11) | 22.9 (11) | 22.9 (11) | 22.9 (11) | 22.9 (11) | 22.9 (11) | 29.3 (11) | 26.8 (11) | 16.5 (15) |
| GPT-5.5 (xhigh) | 22.6 (12) | 22.3 (13) | 22.4 (13) | 22.5 (12) | 22.7 (12) | 22.7 (12) | 22.6 (12) | 27.1 (14) | 25.3 (13) | 18.0 (11) |
| DeepSeek V4 Flash (max) | 22.3 (13) | 22.6 (12) | 22.5 (12) | 22.4 (13) | 22.3 (13) | 22.2 (13) | 22.3 (13) | 28.5 (12) | 26.1 (12) | 16.1 (16) |
| Gemini 3.7 Flash (medium) | 22.2 (14) | 22.1 (14) | 22.1 (14) | 22.1 (14) | 22.2 (14) | 22.2 (14) | 22.2 (14) | 27.4 (13) | 25.3 (14) | 16.9 (14) |
| GLM-5.3 (max) | 22.0 (15) | 22.0 (15) | 22.0 (15) | 22.0 (15) | 21.9 (15) | 21.9 (15) | 22.0 (15) | 26.2 (15) | 24.5 (15) | 17.8 (12) |
| Claude Opus 5 (max) | 20.8 (16) | 20.8 (16) | 20.8 (16) | 20.8 (16) | 20.8 (16) | 20.8 (16) | 20.8 (16) | 24.1 (17) | 22.8 (17) | 17.5 (13) |
| DeepSeek V4 Pro (max) | 19.8 (17) | 20.0 (17) | 19.9 (17) | 19.9 (17) | 19.8 (17) | 19.7 (17) | 19.8 (17) | 25.2 (16) | 23.0 (16) | 14.5 (17) |
| GPT-5.6 Luna (max) | 17.4 (18) | 16.9 (18) | 17.1 (18) | 17.2 (18) | 17.5 (18) | 17.6 (18) | 17.4 (18) | 22.2 (19) | 20.3 (18) | 12.5 (18) |
| Gemini 3.6 Flash (high) | 15.2 (19) | 15.1 (19) | 15.1 (19) | 15.2 (19) | 15.2 (19) | 15.2 (19) | 15.2 (19) | 22.6 (18) | 19.6 (19) | 7.8 (19) |
| Gemini 3.5 Flash (high) | 12.5 (20) | 12.6 (20) | 12.6 (20) | 12.5 (20) | 12.5 (20) | 12.5 (20) | 12.5 (20) | 20.9 (20) | 17.6 (20) | 4.2 (20) |
| GPT-5.4 (xhigh) | 9.6 (21) | 8.9 (22) | 9.1 (22) | 9.4 (22) | 9.8 (21) | 10.1 (21) | 9.6 (21) | 16.8 (22) | 13.9 (22) | 2.4 (21) |
| Claude Sonnet 4.6 (high) | 9.6 (22) | 9.9 (21) | 9.8 (21) | 9.7 (21) | 9.5 (22) | 9.4 (22) | 9.6 (22) | 17.5 (21) | 14.3 (21) | 1.7 (22) |
| Kimi K2.7 Code | 7.1 (23) | 7.0 (23) | 7.0 (23) | 7.1 (23) | 7.1 (23) | 7.1 (23) | 7.1 (23) | 15.4 (23) | 12.1 (23) | -1.2 (23) |
| Muse Spark 1.1 (xhigh) | 4.7 (24) | 4.8 (24) | 4.8 (24) | 4.7 (24) | 4.7 (24) | 4.7 (24) | 4.7 (24) | 11.2 (24) | 8.6 (24) | -1.8 (24) |
| Muse Spark 1.2 (xhigh) | 4.2 (25) | 4.4 (25) | 4.3 (25) | 4.2 (25) | 4.1 (25) | 4.0 (25) | 4.2 (25) | 11.1 (25) | 8.3 (25) | -2.8 (25) |
| Gemini 3.1 Pro Preview (high) | -0.7 (26) | -0.7 (26) | -0.7 (26) | -0.7 (26) | -0.7 (26) | -0.7 (26) | -0.7 (26) | 7.8 (26) | 4.4 (26) | -9.2 (26) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (0 of 7448 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Fable 5 (xhigh) | 388 | 0 | Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→14 |
| Claude Opus 4.8 (max) | 332 | 0 | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→14 |
| Claude Opus 5 (max) | 388 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Claude Sonnet 4.6 (high) | 144 | 0 | GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Claude Sonnet 5 (max) | 312 | 0 | none |
| DeepSeek V4 Flash (max) | 252 | 0 | none |
| DeepSeek V4 Pro (max) | 308 | 0 | none |
| Gemini 3.1 Pro Preview (high) | 44 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7 |
| Gemini 3.5 Flash (high) | 152 | 0 | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7 |
| Gemini 3.6 Flash (high) | 212 | 0 | GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Gemini 3.7 Flash (medium) | 320 | 0 | GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| GLM-5.2 (max) | 212 | 0 | none |
| GLM-5.3 Flash (max) | 372 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| GLM-5.3 (max) | 348 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| GPT-5.4 (xhigh) | 236 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| GPT-5.5 (xhigh) | 348 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| GPT-5.6 Luna (max) | 340 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→12, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| GPT-5.6 Sol (max) | 392 | 0 | DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→13, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| GPT-5.6 Terra (max) | 360 | 0 | none |
| Grok 4.5 (high) | 316 | 0 | GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Grok 4.6 (medium) | 356 | 0 | GLM-5.2 (max) 11→12, GPT-5.5 (xhigh) 12→11 |
| Kimi K2.7 Code | 128 | 0 | none |
| Kimi K3 (max) | 356 | 0 | Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→14 |
| Muse Spark 1.1 (xhigh) | 272 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→12, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→14, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Muse Spark 1.2 (xhigh) | 264 | 0 | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Qwen3.8 Max (xhigh) | 296 | 0 | none |
| (dedup panel) | 0 | 0 | none |

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| Fatal1ty/mashumaro (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GLM-5.2 (max) 11→12, GPT-5.5 (xhigh) 12→14, DeepSeek V4 Flash (max) 13→15, Gemini 3.7 Flash (medium) 14→13, GLM-5.3 (max) 15→11, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Gallopsled/pwntools (4) | GLM-5.3 Flash (max) 7→9, Qwen3.8 Max (xhigh) 8→7, GPT-5.6 Terra (max) 9→8, GLM-5.2 (max) 11→13, DeepSeek V4 Flash (max) 13→11 |
| PyCQA/bandit (12) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GLM-5.2 (max) 11→12, GPT-5.5 (xhigh) 12→14, Gemini 3.7 Flash (medium) 14→11, GLM-5.3 (max) 15→17, Claude Opus 5 (max) 16→15, DeepSeek V4 Pro (max) 17→16, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| Textualize/textual (8) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, Grok 4.6 (medium) 6→7, GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→6, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→12, Claude Opus 5 (max) 16→17, DeepSeek V4 Pro (max) 17→16 |
| aio-libs/aiomonitor (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→8, GPT-5.5 (xhigh) 12→14, DeepSeek V4 Flash (max) 13→12, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→13, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| celery/kombu (8) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→8, GLM-5.3 (max) 15→16, Claude Opus 5 (max) 16→15, Gemini 3.5 Flash (high) 20→21, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→20 |
| dateutil/dateutil (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→13 |
| dry-python/returns (4) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→7, GLM-5.2 (max) 11→12, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→15, Gemini 3.7 Flash (medium) 14→11, GLM-5.3 (max) 15→14 |
| encode/httpx (8) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GPT-5.5 (xhigh) 12→15, DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→12, GLM-5.3 (max) 15→13 |
| fastapi/fastapi (8) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, Qwen3.8 Max (xhigh) 8→10, Grok 4.5 (high) 10→8, GLM-5.2 (max) 11→16, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→12, Gemini 3.7 Flash (medium) 14→11, GLM-5.3 (max) 15→14, Claude Opus 5 (max) 16→17, DeepSeek V4 Pro (max) 17→15, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| fgmacedo/python-statemachine (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→7, GLM-5.2 (max) 11→12, GPT-5.5 (xhigh) 12→11, DeepSeek V4 Flash (max) 13→16, Gemini 3.7 Flash (medium) 14→13, GLM-5.3 (max) 15→14, Claude Opus 5 (max) 16→15 |
| google/mobly (4) | Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→8, GPT-5.5 (xhigh) 12→16, GLM-5.3 (max) 15→12, Claude Opus 5 (max) 16→15, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| graphql-python/gql (4) | GLM-5.2 (max) 11→13, GPT-5.5 (xhigh) 12→11, DeepSeek V4 Flash (max) 13→12 |
| ipython/ipython (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GLM-5.2 (max) 11→13, GPT-5.5 (xhigh) 12→11, DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→16, GLM-5.3 (max) 15→12, Claude Opus 5 (max) 16→15, Muse Spark 1.1 (xhigh) 24→25, Muse Spark 1.2 (xhigh) 25→24 |
| jendrikseipp/vulture (4) | GLM-5.2 (max) 11→16, GPT-5.5 (xhigh) 12→11, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→12, Claude Opus 5 (max) 16→14 |
| jkwill87/mnamer (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GPT-5.5 (xhigh) 12→14, DeepSeek V4 Flash (max) 13→15, Gemini 3.7 Flash (medium) 14→16, GLM-5.3 (max) 15→12, Claude Opus 5 (max) 16→13, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| langchain-ai/langchain (4) | GLM-5.3 Flash (max) 7→9, Qwen3.8 Max (xhigh) 8→7, GPT-5.6 Terra (max) 9→8, GLM-5.2 (max) 11→14, DeepSeek V4 Flash (max) 13→11, Gemini 3.7 Flash (medium) 14→13, Claude Opus 5 (max) 16→17, DeepSeek V4 Pro (max) 17→16 |
| narwhals-dev/narwhals (4) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GLM-5.2 (max) 11→13, DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→11, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| nidhaloff/igel (4) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→7, GLM-5.2 (max) 11→14, GPT-5.5 (xhigh) 12→11, DeepSeek V4 Flash (max) 13→15, Gemini 3.7 Flash (medium) 14→12, GLM-5.3 (max) 15→13, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| numba/numba (4) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.6 Terra (max) 9→10, Grok 4.5 (high) 10→9, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→12, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| psd-tools/psd-tools (4) | Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→8, GLM-5.2 (max) 11→12, GPT-5.5 (xhigh) 12→11, DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→13, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| python-attrs/cattrs (4) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→7, GLM-5.2 (max) 11→13, GPT-5.5 (xhigh) 12→11, DeepSeek V4 Flash (max) 13→12, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→14 |
| python-poetry/tomlkit (4) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→9, GPT-5.6 Terra (max) 9→7, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→16, GLM-5.3 (max) 15→12, Claude Opus 5 (max) 16→15 |
| reagento/adaptix (4) | GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.6 Terra (max) 9→10, Grok 4.5 (high) 10→9, GLM-5.2 (max) 11→12, GPT-5.5 (xhigh) 12→13, DeepSeek V4 Flash (max) 13→11, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| simonw/sqlite-utils (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GLM-5.3 Flash (max) 7→8, Qwen3.8 Max (xhigh) 8→7, GPT-5.5 (xhigh) 12→16, DeepSeek V4 Flash (max) 13→12, Gemini 3.7 Flash (medium) 14→13, GLM-5.3 (max) 15→14, Claude Opus 5 (max) 16→15, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |
| skrub-data/skrub (4) | GLM-5.3 Flash (max) 7→9, GPT-5.6 Terra (max) 9→7, DeepSeek V4 Flash (max) 13→14, Gemini 3.7 Flash (medium) 14→13, Claude Opus 5 (max) 16→17, DeepSeek V4 Pro (max) 17→16 |
| tconbeer/sqlfmt (4) | Kimi K3 (max) 2→3, Claude Opus 4.8 (max) 3→2, GLM-5.2 (max) 11→13, DeepSeek V4 Flash (max) 13→11, Gemini 3.7 Flash (medium) 14→15, GLM-5.3 (max) 15→14, GPT-5.4 (xhigh) 21→22, Claude Sonnet 4.6 (high) 22→21 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (121) | Solved by fewer (121) |
|---|---:|---:|
| Claude Fable 5 (xhigh) | 53.2 (1) | 53.2 (1) |
| Kimi K3 (max) | 42.5 (2) | 42.5 (2) |
| Claude Opus 4.8 (max) | 42.4 (3) | 42.4 (3) |
| Claude Sonnet 5 (max) | 38.3 (4) | 38.3 (4) |
| GPT-5.6 Sol (max) | 33.2 (5) | 33.2 (5) |
| Grok 4.6 (medium) | 28.3 (6) | 28.3 (6) |
| GLM-5.3 Flash (max) | 26.9 (7) | 26.9 (7) |
| Qwen3.8 Max (xhigh) | 26.9 (8) | 26.9 (8) |
| GPT-5.6 Terra (max) | 26.5 (9) | 26.5 (9) |
| Grok 4.5 (high) | 25.4 (10) | 25.4 (10) |
| GLM-5.2 (max) | 22.9 (11) | 22.9 (11) |
| GPT-5.5 (xhigh) | 22.6 (12) | 22.6 (12) |
| DeepSeek V4 Flash (max) | 22.3 (13) | 22.3 (13) |
| Gemini 3.7 Flash (medium) | 22.2 (14) | 22.2 (14) |
| GLM-5.3 (max) | 22.0 (15) | 22.0 (15) |
| Claude Opus 5 (max) | 20.8 (16) | 20.8 (16) |
| DeepSeek V4 Pro (max) | 19.8 (17) | 19.8 (17) |
| GPT-5.6 Luna (max) | 17.4 (18) | 17.4 (18) |
| Gemini 3.6 Flash (high) | 15.2 (19) | 15.2 (19) |
| Gemini 3.5 Flash (high) | 12.5 (20) | 12.5 (20) |
| GPT-5.4 (xhigh) | 9.6 (21) | 9.6 (21) |
| Claude Sonnet 4.6 (high) | 9.6 (22) | 9.6 (22) |
| Kimi K2.7 Code | 7.1 (23) | 7.1 (23) |
| Muse Spark 1.1 (xhigh) | 4.7 (24) | 4.7 (24) |
| Muse Spark 1.2 (xhigh) | 4.2 (25) | 4.2 (25) |
| Gemini 3.1 Pro Preview (high) | -0.7 (26) | -0.7 (26) |

## What drives each adjacent gap

Difference in mean score split by outcome (a/b), and the tasks that move it most. Contributions are per-task differences divided by the task count, so they sum to the gap.

- **Claude Fable 5 (xhigh) − Kimi K3 (max) = 10.40**: failed/failed -0.03 (25), failed/solved -7.11 (10), solved/failed 11.45 (17), solved/solved 6.09 (79). For Claude Fable 5 (xhigh): `kombu-single-active-consumer-priority#1` +0.83 (solved/failed), `dateutil-rfc5545-timezone-interop#2` +0.83 (solved/failed), `mashumaro-flattened-dataclass-fields#4` +0.82 (solved/failed). For Kimi K3 (max): `kombu-single-active-consumer-priority#3` -0.84 (failed/solved), `mashumaro-flattened-dataclass-fields#3` -0.82 (failed/solved), `kombu-virtual-queue-dead-lettering#4` -0.82 (failed/solved).
- **Kimi K3 (max) − Claude Opus 4.8 (max) = 0.14**: failed/failed 0.08 (27), failed/solved -9.44 (15), solved/failed 13.08 (21), solved/solved -3.58 (67). For Kimi K3 (max): `kombu-single-active-consumer-priority#3` +0.85 (solved/failed), `mashumaro-flattened-dataclass-fields#3` +0.83 (solved/failed), `dateutil-rfc5545-timezone-interop#4` +0.80 (solved/failed). For Claude Opus 4.8 (max): `pwntools-tube-multiplexing#4` -0.81 (failed/solved), `psd-tools-blend-range-api#4` -0.81 (failed/solved), `httpx-streaming-json-iteration#2` -0.74 (failed/solved).
- **Claude Opus 4.8 (max) − Claude Sonnet 5 (max) = 4.24**: failed/failed -0.03 (27), failed/solved -13.50 (21), solved/failed 17.10 (27), solved/solved 0.68 (56). For Claude Opus 4.8 (max): `httpx-streaming-json-iteration#2` +0.82 (solved/failed), `cattrs-partial-structuring-recovery#1` +0.81 (solved/failed), `fastapi-deprecation-response-headers#2` +0.80 (solved/failed). For Claude Sonnet 5 (max): `mashumaro-flattened-dataclass-fields#1` -0.84 (failed/solved), `kombu-virtual-queue-dead-lettering#2` -0.80 (failed/solved), `gql-incremental-graphql-delivery#1` -0.79 (failed/solved).
- **Claude Sonnet 5 (max) − GPT-5.6 Sol (max) = 4.63**: failed/failed 0.42 (17), failed/solved -16.61 (37), solved/failed 9.80 (15), solved/solved 11.01 (61). For Claude Sonnet 5 (max): `kombu-virtual-queue-dead-lettering#2` +0.81 (solved/failed), `python-statemachine-state-data-scoping#4` +0.80 (solved/failed), `gql-incremental-graphql-delivery#1` +0.78 (solved/failed). For GPT-5.6 Sol (max): `sqlite-utils-safe-import-checkpoints#3` -0.85 (failed/solved), `sqlite-utils-safe-import-checkpoints#1` -0.82 (failed/solved), `mashumaro-flattened-dataclass-fields#4` -0.80 (failed/solved).
- **GPT-5.6 Sol (max) − Grok 4.6 (medium) = 5.47**: failed/failed -0.01 (20), failed/solved -5.42 (12), solved/failed 9.01 (23), solved/solved 1.89 (75). For GPT-5.6 Sol (max): `mobly-grouped-test-barriers#3` +0.80 (solved/failed), `langchain-request-coalescing#4` +0.69 (solved/failed), `mashumaro-flattened-dataclass-fields#4` +0.64 (solved/solved). For Grok 4.6 (medium): `python-statemachine-state-data-scoping#1` -0.67 (failed/solved), `httpx-streaming-json-iteration#2` -0.64 (failed/solved), `vulture-persistent-analysis-cache#4` -0.61 (failed/solved).
- **Grok 4.6 (medium) − GLM-5.3 Flash (max) = 1.51**: failed/failed -0.13 (16), failed/solved -10.73 (25), solved/failed 8.53 (20), solved/solved 3.85 (68). For Grok 4.6 (medium): `httpx-streaming-json-iteration#2` +0.64 (solved/failed), `vulture-persistent-analysis-cache#4` +0.60 (solved/failed), `bandit-interprocedural-taint-checks#1` +0.58 (solved/failed). For GLM-5.3 Flash (max): `langchain-request-coalescing#3` -0.73 (failed/solved), `httpx-multipart-response-parsing#4` -0.71 (failed/solved), `bandit-interprocedural-taint-checks#3` -0.67 (failed/solved).
- **GLM-5.3 Flash (max) − Qwen3.8 Max (xhigh) = -0.57**: failed/failed -0.25 (27), failed/solved -5.96 (9), solved/failed 11.24 (29), solved/solved -5.61 (64). For GLM-5.3 Flash (max): `langchain-request-coalescing#3` +0.73 (solved/failed), `httpx-multipart-response-parsing#4` +0.70 (solved/failed), `bandit-interprocedural-taint-checks#3` +0.66 (solved/failed). For Qwen3.8 Max (xhigh): `httpx-streaming-json-iteration#1` -0.83 (failed/solved), `igel-persist-feature-schema#2` -0.81 (failed/solved), `httpx-streaming-json-iteration#4` -0.78 (failed/solved).
- **Qwen3.8 Max (xhigh) − GPT-5.6 Terra (max) = 0.32**: failed/failed 0.41 (25), failed/solved -11.79 (33), solved/failed 10.36 (17), solved/solved 1.34 (57). For Qwen3.8 Max (xhigh): `httpx-streaming-json-iteration#1` +0.83 (solved/failed), `skrub-duration-encoding#1` +0.80 (solved/failed), `igel-persist-feature-schema#2` +0.79 (solved/failed). For GPT-5.6 Terra (max): `textual-kitty-key-phases#1` -0.67 (failed/solved), `ipython-session-bundle-replay#4` -0.60 (failed/solved), `adaptix-name-mapping-aliases#1` -0.56 (solved/solved).
- **GPT-5.6 Terra (max) − Grok 4.5 (high) = 1.14**: failed/failed -0.07 (23), failed/solved -9.46 (19), solved/failed 11.30 (30), solved/solved -0.62 (60). For GPT-5.6 Terra (max): `mobly-grouped-test-barriers#1` +0.72 (solved/failed), `numba-stencil-boundary-modes#4` +0.65 (solved/solved), `fastapi-implicit-head-options#1` +0.63 (solved/failed). For Grok 4.5 (high): `langchain-request-coalescing#1` -0.86 (failed/solved), `mobly-grouped-test-barriers#4` -0.75 (failed/solved), `pwntools-tube-multiplexing#1` -0.72 (failed/solved).
- **Grok 4.5 (high) − GLM-5.2 (max) = 2.69**: failed/failed -0.72 (35), failed/solved -11.85 (17), solved/failed 18.83 (42), solved/solved -3.57 (36). For Grok 4.5 (high): `langchain-request-coalescing#1` +0.85 (solved/failed), `mobly-grouped-test-barriers#3` +0.84 (solved/failed), `mobly-grouped-test-barriers#4` +0.78 (solved/failed). For GLM-5.2 (max): `fastapi-implicit-head-options#1` -0.85 (failed/solved), `pwntools-tube-multiplexing#4` -0.85 (failed/solved), `fastapi-deprecation-response-headers#1` -0.84 (failed/solved).
- **GLM-5.2 (max) − GPT-5.5 (xhigh) = -0.03**: failed/failed 0.48 (28), failed/solved -21.06 (49), solved/failed 10.33 (16), solved/solved 10.22 (37). For GLM-5.2 (max): `pwntools-tube-multiplexing#4` +0.86 (solved/failed), `ipython-session-bundle-replay#1` +0.83 (solved/failed), `vulture-persistent-analysis-cache#4` +0.81 (solved/failed). For GPT-5.5 (xhigh): `mobly-grouped-test-barriers#1` -0.81 (failed/solved), `mobly-grouped-test-barriers#2` -0.79 (failed/solved), `sqlite-utils-safe-import-checkpoints#1` -0.77 (failed/solved).
- **GPT-5.5 (xhigh) − DeepSeek V4 Flash (max) = 0.23**: failed/failed -0.35 (29), failed/solved -9.80 (16), solved/failed 15.05 (40), solved/solved -4.67 (47). For GPT-5.5 (xhigh): `httpx-multipart-response-parsing#4` +0.83 (solved/failed), `sqlite-utils-safe-import-checkpoints#4` +0.82 (solved/failed), `sqlite-utils-safe-import-checkpoints#1` +0.76 (solved/failed). For DeepSeek V4 Flash (max): `igel-persist-feature-schema#2` -0.80 (failed/solved), `kombu-virtual-queue-dead-lettering#4` -0.78 (failed/solved), `vulture-persistent-analysis-cache#3` -0.78 (failed/solved).
- **DeepSeek V4 Flash (max) − Gemini 3.7 Flash (medium) = 0.19**: failed/failed 0.36 (32), failed/solved -14.28 (37), solved/failed 10.40 (20), solved/solved 3.71 (43). For DeepSeek V4 Flash (max): `igel-persist-feature-schema#2` +0.82 (solved/failed), `httpx-streaming-json-iteration#2` +0.81 (solved/failed), `python-statemachine-state-data-scoping#1` +0.78 (solved/failed). For Gemini 3.7 Flash (medium): `ipython-session-bundle-replay#4` -0.79 (failed/solved), `adaptix-name-mapping-aliases#3` -0.75 (failed/solved), `dateutil-rfc5545-timezone-interop#2` -0.71 (failed/solved).
- **Gemini 3.7 Flash (medium) − GLM-5.3 (max) = 0.15**: failed/failed -0.10 (19), failed/solved -13.20 (33), solved/failed 11.58 (25), solved/solved 1.88 (54). For Gemini 3.7 Flash (medium): `textual-richlog-follow-state#1` +0.74 (solved/failed), `dateutil-rfc5545-timezone-interop#2` +0.72 (solved/failed), `mnamer-daemon-watch-lifecycle#1` +0.71 (solved/failed). For GLM-5.3 (max): `bandit-structured-nosec-directives#4` -0.81 (failed/solved), `bandit-interprocedural-taint-checks#1` -0.80 (failed/solved), `httpx-multipart-response-parsing#1` -0.63 (solved/solved).
- **GLM-5.3 (max) − Claude Opus 5 (max) = 1.16**: failed/failed -0.04 (22), failed/solved -7.51 (22), solved/failed 5.14 (11), solved/solved 3.57 (74). For GLM-5.3 (max): `bandit-structured-nosec-directives#4` +0.80 (solved/failed), `cattrs-partial-structuring-recovery#3` +0.73 (solved/failed), `textual-richlog-follow-state#3` +0.69 (solved/failed). For Claude Opus 5 (max): `httpx-multipart-response-parsing#4` -0.62 (failed/solved), `httpx-multipart-response-parsing#2` -0.59 (failed/solved), `mashumaro-flattened-dataclass-fields#4` -0.54 (failed/solved).
- **Claude Opus 5 (max) − DeepSeek V4 Pro (max) = 0.69**: failed/failed 0.14 (19), failed/solved -5.36 (14), solved/failed 13.29 (36), solved/solved -7.37 (61). For Claude Opus 5 (max): `httpx-multipart-response-parsing#1` +0.85 (solved/failed), `skrub-duration-encoding#3` +0.78 (solved/failed), `httpx-multipart-response-parsing#3` +0.73 (solved/failed). For DeepSeek V4 Pro (max): `httpx-streaming-json-iteration#2` -0.76 (failed/solved), `httpx-streaming-json-iteration#1` -0.70 (failed/solved), `mnamer-daemon-watch-lifecycle#3` -0.55 (solved/solved).
- **DeepSeek V4 Pro (max) − GPT-5.6 Luna (max) = 2.46**: failed/failed 0.08 (26), failed/solved -9.38 (29), solved/failed 8.94 (21), solved/solved 2.83 (56). For DeepSeek V4 Pro (max): `httpx-streaming-json-iteration#2` +0.76 (solved/failed), `httpx-streaming-json-iteration#1` +0.71 (solved/failed), `aiomonitor-task-snapshots-diff#3` +0.62 (solved/failed). For GPT-5.6 Luna (max): `mobly-grouped-test-barriers#4` -0.77 (failed/solved), `mobly-grouped-test-barriers#3` -0.69 (failed/solved), `httpx-multipart-response-parsing#1` -0.66 (failed/solved).
- **GPT-5.6 Luna (max) − Gemini 3.6 Flash (high) = 2.20**: failed/failed -0.27 (33), failed/solved -7.25 (13), solved/failed 15.17 (45), solved/solved -5.46 (40). For GPT-5.6 Luna (max): `textual-richlog-follow-state#1` +0.80 (solved/failed), `numba-stencil-boundary-modes#2` +0.80 (solved/failed), `sqlite-utils-safe-import-checkpoints#2` +0.72 (solved/failed). For Gemini 3.6 Flash (high): `narwhals-rolling-window-suite#4` -0.76 (failed/solved), `kombu-single-active-consumer-priority#2` -0.74 (failed/solved), `httpx-streaming-json-iteration#3` -0.73 (failed/solved).
- **Gemini 3.6 Flash (high) − Gemini 3.5 Flash (high) = 2.66**: failed/failed -0.32 (67), failed/solved -7.36 (10), solved/failed 12.66 (25), solved/solved -2.32 (28). For Gemini 3.6 Flash (high): `tomlkit-toml-table-converters#4` +0.84 (solved/failed), `adaptix-name-mapping-aliases#2` +0.80 (solved/failed), `tomlkit-toml-table-converters#1` +0.80 (solved/failed). For Gemini 3.5 Flash (high): `igel-persist-feature-schema#3` -0.85 (failed/solved), `igel-persist-feature-schema#4` -0.84 (failed/solved), `numba-stencil-boundary-modes#3` -0.84 (failed/solved).
- **Gemini 3.5 Flash (high) − GPT-5.4 (xhigh) = 3.40**: failed/failed 0.52 (55), failed/solved -14.82 (38), solved/failed 11.60 (18), solved/solved 6.10 (20). For Gemini 3.5 Flash (high): `igel-persist-feature-schema#3` +0.87 (solved/failed), `ipython-session-bundle-replay#3` +0.83 (solved/failed), `kombu-single-active-consumer-priority#3` +0.82 (solved/failed). For GPT-5.4 (xhigh): `fastapi-deprecation-response-headers#4` -0.86 (failed/solved), `fastapi-deprecation-response-headers#3` -0.82 (failed/solved), `tomlkit-toml-table-converters#1` -0.74 (failed/solved).
- **GPT-5.4 (xhigh) − Claude Sonnet 4.6 (high) = 0.00**: failed/failed -0.73 (54), failed/solved -10.96 (19), solved/failed 15.21 (42), solved/solved -3.51 (17). For GPT-5.4 (xhigh): `fastapi-deprecation-response-headers#4` +0.82 (solved/failed), `fastapi-deprecation-response-headers#3` +0.80 (solved/failed), `numba-stencil-boundary-modes#2` +0.71 (solved/failed). For Claude Sonnet 4.6 (high): `vulture-persistent-analysis-cache#2` -0.85 (failed/solved), `python-statemachine-state-data-scoping#2` -0.84 (failed/solved), `langchain-request-coalescing#1` -0.81 (failed/solved).
- **Claude Sonnet 4.6 (high) − Kimi K2.7 Code = 2.52**: failed/failed 0.09 (76), failed/solved -11.62 (20), solved/failed 14.38 (24), solved/solved -0.33 (12). For Claude Sonnet 4.6 (high): `vulture-persistent-analysis-cache#2` +0.83 (solved/failed), `vulture-persistent-analysis-cache#4` +0.82 (solved/failed), `pwntools-tube-multiplexing#3` +0.81 (solved/failed). For Kimi K2.7 Code: `httpx-streaming-json-iteration#2` -0.84 (failed/solved), `mnamer-daemon-watch-lifecycle#4` -0.80 (failed/solved), `sqlite-utils-safe-import-checkpoints#2` -0.79 (failed/solved).
- **Kimi K2.7 Code − Muse Spark 1.1 (xhigh) = 2.37**: failed/failed 0.94 (54), failed/solved -11.22 (46), solved/failed 5.77 (10), solved/solved 6.87 (22). For Kimi K2.7 Code: `mnamer-daemon-watch-lifecycle#4` +0.82 (solved/failed), `fastapi-deprecation-response-headers#1` +0.77 (solved/failed), `langchain-request-coalescing#2` +0.67 (solved/failed). For Muse Spark 1.1 (xhigh): `bandit-interprocedural-taint-checks#1` -0.60 (failed/solved), `sqlfmt-create-table-ddl-formatting#1` -0.50 (failed/solved), `mobly-grouped-test-barriers#2` -0.47 (failed/solved).
- **Muse Spark 1.1 (xhigh) − Muse Spark 1.2 (xhigh) = 0.54**: failed/failed 0.20 (47), failed/solved -4.74 (17), solved/failed 3.94 (19), solved/solved 1.15 (49). For Muse Spark 1.1 (xhigh): `aiomonitor-task-snapshots-diff#3` +0.55 (solved/solved), `bandit-interprocedural-taint-checks#1` +0.44 (solved/solved), `bandit-interprocedural-taint-checks#2` +0.40 (solved/failed). For Muse Spark 1.2 (xhigh): `sqlfmt-create-table-ddl-formatting#2` -0.61 (failed/solved), `httpx-multipart-response-parsing#3` -0.57 (failed/solved), `fastapi-deprecation-response-headers#3` -0.50 (failed/solved).
- **Muse Spark 1.2 (xhigh) − Gemini 3.1 Pro Preview (high) = 4.72**: failed/failed -2.31 (64), failed/solved -1.54 (2), solved/failed 13.29 (56), solved/solved -4.72 (9). For Muse Spark 1.2 (xhigh): `vulture-persistent-analysis-cache#3` +0.68 (solved/failed), `sqlfmt-create-table-ddl-formatting#4` +0.66 (solved/failed), `sqlfmt-create-table-ddl-formatting#2` +0.59 (solved/failed). For Gemini 3.1 Pro Preview (high): `bandit-interprocedural-taint-checks#2` -0.82 (failed/solved), `psd-tools-blend-range-api#4` -0.74 (solved/solved), `ipython-session-bundle-replay#3` -0.73 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability examples/deepswe-python/score-panel.json examples/deepswe-python/*.jsonl --output examples/deepswe-python/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
