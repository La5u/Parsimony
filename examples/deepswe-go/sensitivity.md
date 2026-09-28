# Score sensitivity: 26 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `deepswe-v1.1-go-26-pooled-80-20-v0.6`: 136 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (110 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Fable 5 (xhigh) ≈ Kimi K3 (max) ≈ Claude Opus 4.8 (max) ≈ GLM-5.3 (max) ≈ Qwen3.8 Max (xhigh) ≈ Gemini 3.7 Flash (medium) ≈ Claude Opus 5 (max) ≈ Gemini 3.6 Flash (high) ≈ GLM-5.3 Flash (max) ≈ Claude Sonnet 5 (max) ≈ DeepSeek V4 Flash (max) ≈ Grok 4.6 (medium) ≈ GLM-5.2 (max) ≈ GPT-5.6 Sol (max) ≈ GPT-5.6 Terra (max) ≈ GPT-5.5 (xhigh) ≈ Kimi K2.7 Code ≈ GPT-5.6 Luna (max) ≈ Gemini 3.5 Flash (high) ≈ DeepSeek V4 Pro (max) ≈ Grok 4.5 (high) ≈ GPT-5.4 (xhigh) ≈ Muse Spark 1.2 (xhigh) ≈ Claude Sonnet 4.6 (high) ≈ Muse Spark 1.1 (xhigh) ≈ Gemini 3.1 Pro Preview (high) (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (0 of 25 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 25 pairs): Claude Fable 5 (xhigh) vs Kimi K3 (max), Kimi K3 (max) vs Claude Opus 4.8 (max), Claude Opus 4.8 (max) vs GLM-5.3 (max), GLM-5.3 (max) vs Qwen3.8 Max (xhigh), Qwen3.8 Max (xhigh) vs Gemini 3.7 Flash (medium), Gemini 3.7 Flash (medium) vs Claude Opus 5 (max), Claude Opus 5 (max) vs Gemini 3.6 Flash (high), Gemini 3.6 Flash (high) vs GLM-5.3 Flash (max), GLM-5.3 Flash (max) vs Claude Sonnet 5 (max), Claude Sonnet 5 (max) vs DeepSeek V4 Flash (max), DeepSeek V4 Flash (max) vs Grok 4.6 (medium), Grok 4.6 (medium) vs GLM-5.2 (max), GLM-5.2 (max) vs GPT-5.6 Sol (max), GPT-5.6 Sol (max) vs GPT-5.6 Terra (max), GPT-5.6 Terra (max) vs GPT-5.5 (xhigh), GPT-5.5 (xhigh) vs Kimi K2.7 Code, Kimi K2.7 Code vs GPT-5.6 Luna (max), GPT-5.6 Luna (max) vs Gemini 3.5 Flash (high), Gemini 3.5 Flash (high) vs DeepSeek V4 Pro (max), DeepSeek V4 Pro (max) vs Grok 4.5 (high), Grok 4.5 (high) vs GPT-5.4 (xhigh), GPT-5.4 (xhigh) vs Muse Spark 1.2 (xhigh), Muse Spark 1.2 (xhigh) vs Claude Sonnet 4.6 (high), Claude Sonnet 4.6 (high) vs Muse Spark 1.1 (xhigh), Muse Spark 1.1 (xhigh) vs Gemini 3.1 Pro Preview (high).
- **Rank never changes under any variation**: Claude Fable 5 (xhigh) (1), Kimi K3 (max) (2), Claude Opus 4.8 (max) (3), GPT-5.4 (xhigh) (22), Gemini 3.1 Pro Preview (high) (26).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 136 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Fable 5 (xhigh) | 54.0 | 42.8–63.8 | 54.0 | 1–1 | 1–3 | 0.66 |
| 2 | Kimi K3 (max) | 52.0 | 42.6–61.5 | 51.7–52.4 | 2–2 | 1–3 | 0.31 |
| 3 | Claude Opus 4.8 (max) | 44.0 | 26.7–60.3 | 37.7–50.3 | 3–3 | 1–5 | 0.03 |
| 4 | GLM-5.3 (max) | 35.7 | 25.6–45.5 | 34.9–36.4 | 4–6 | 3–12 | 0.00 |
| 5 | Qwen3.8 Max (xhigh) | 35.1 | 25.7–44.6 | 35.1 | 4–7 | 4–14 | 0.00 |
| 6 | Gemini 3.7 Flash (medium) | 33.8 | 24.8–43.4 | 33.8 | 4–8 | 3–14 | 0.00 |
| 7 | Claude Opus 5 (max) | 33.4 | 23.3–43.9 | 32.0–34.7 | 5–8 | 4–15 | 0.00 |
| 8 | Gemini 3.6 Flash (high) | 33.1 | 24.0–43.2 | 33.1 | 5–8 | 3–16 | 0.00 |
| 9 | GLM-5.3 Flash (max) | 30.7 | 21.8–39.5 | 30.2–31.1 | 9–11 | 5–17 | 0.00 |
| 10 | Claude Sonnet 5 (max) | 30.5 | 17.4–43.9 | 26.5–34.6 | 9–13 | 4–18 | 0.00 |
| 11 | DeepSeek V4 Flash (max) | 30.0 | 21.2–38.6 | 30.0 | 9–13 | 4–17 | 0.00 |
| 12 | Grok 4.6 (medium) | 28.9 | 21.2–36.4 | 28.9 | 9–14 | 6–17 | 0.00 |
| 13 | GLM-5.2 (max) | 28.5 | 19.4–37.3 | 28.5 | 11–14 | 5–19 | 0.00 |
| 14 | GPT-5.6 Sol (max) | 28.1 | 20.3–35.8 | 28.1 | 12–14 | 6–19 | 0.00 |
| 15 | GPT-5.6 Terra (max) | 24.8 | 17.8–32.6 | 24.8 | 15–16 | 8–21 | 0.00 |
| 16 | GPT-5.5 (xhigh) | 24.3 | 17.5–31.8 | 24.3 | 15–17 | 9–21 | 0.00 |
| 17 | Kimi K2.7 Code | 22.0 | 12.2–31.6 | 22.0 | 15–20 | 10–22 | 0.00 |
| 18 | GPT-5.6 Luna (max) | 21.9 | 16.3–27.8 | 21.9 | 17–20 | 13–22 | 0.00 |
| 19 | Gemini 3.5 Flash (high) | 20.5 | 11.3–29.9 | 20.5 | 18–21 | 12–23 | 0.00 |
| 20 | DeepSeek V4 Pro (max) | 20.4 | 14.6–26.2 | 20.4 | 18–21 | 14–23 | 0.00 |
| 21 | Grok 4.5 (high) | 20.1 | 11.1–29.6 | 20.1 | 18–21 | 12–23 | 0.00 |
| 22 | GPT-5.4 (xhigh) | 15.3 | 7.6–23.6 | 15.3 | 22–22 | 18–25 | 0.00 |
| 23 | Muse Spark 1.2 (xhigh) | 12.9 | 5.3–20.9 | 12.9 | 23–24 | 20–26 | 0.00 |
| 24 | Claude Sonnet 4.6 (high) | 10.6 | 2.5–19.5 | 10.5–10.7 | 23–25 | 20–26 | 0.00 |
| 25 | Muse Spark 1.1 (xhigh) | 10.4 | 3.2–17.9 | 10.3–10.5 | 24–25 | 22–26 | 0.00 |
| 26 | Gemini 3.1 Pro Preview (high) | 5.3 | -2.6–14.2 | 5.2–5.5 | 26–26 | 23–26 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Fable 5 (xhigh) > Kimi K3 (max) | 1.92 | -7.06 to 10.11 | 0.65 | none | yes |
| Kimi K3 (max) > Claude Opus 4.8 (max) | 8.04 | -10.96 to 25.62 | 0.58 | none | yes |
| Claude Opus 4.8 (max) > GLM-5.3 (max) | 8.33 | -9.63 to 26.85 | 0.60 | none | yes |
| GLM-5.3 (max) > Qwen3.8 Max (xhigh) | 0.60 | -11.29 to 11.58 | 0.50 | failure cap=0, failure cap=10, without alecthomas/participle, without go-task/task, without goreleaser/goreleaser, without mattn/anko, without open2b/scriggo | no |
| Qwen3.8 Max (xhigh) > Gemini 3.7 Flash (medium) | 1.25 | -10.17 to 12.57 | 0.57 | failure cap=50, without abs-lang/abs, without helm/helm, without open-policy-agent/opa | yes |
| Gemini 3.7 Flash (medium) > Claude Opus 5 (max) | 0.45 | -12.67 to 14.33 | 0.45 | failure cap=50, without beevik/etree, without d5/tengo, without getarcaneapp/arcane, without go-git/go-git, without kgateway-dev/kgateway, without liweiyi88/onedump, without mattn/anko, without prometheus/prometheus, without traefik/yaegi, without wazero/wazero, without xtaci/kcp-go | no |
| Claude Opus 5 (max) > Gemini 3.6 Flash (high) | 0.28 | -14.80 to 14.84 | 0.44 | failure cap=0, failure cap=10, panel without Claude Opus 5 (max), without TomWright/dasel, without abs-lang/abs, without boyter/scc, without carvel-dev/ytt, without cockroachdb/pebble, without go-critic/go-critic, without go-task/task, without googleapis/go-genai, without helm/helm, without open-policy-agent/opa, without open2b/scriggo, without rhysd/actionlint | no |
| Gemini 3.6 Flash (high) > GLM-5.3 Flash (max) | 2.41 | -10.18 to 15.24 | 0.62 | none | yes |
| GLM-5.3 Flash (max) > Claude Sonnet 5 (max) | 0.14 | -15.27 to 17.22 | 0.22 | net weight=0.5, failure cap=0, failure cap=10, panel without Claude Opus 5 (max), panel without DeepSeek V4 Pro (max), panel without GPT-5.6 Luna (max), panel without GPT-5.6 Sol (max), panel without GPT-5.6 Terra (max), panel without Muse Spark 1.1 (xhigh), without abs-lang/abs, without alecthomas/participle, without beevik/etree, without carvel-dev/ytt, without cockroachdb/pebble, without expr-lang/expr, without go-task/task, without golang/geo, without goreleaser/goreleaser, without helm/helm, without prometheus/prometheus, without wazero/wazero | no |
| Claude Sonnet 5 (max) > DeepSeek V4 Flash (max) | 0.58 | -13.53 to 15.92 | 0.24 | failure cap=50, without TomWright/dasel, without alecthomas/participle, without boyter/scc, without carvel-dev/ytt, without d5/tengo, without go-critic/go-critic, without go-git/go-git, without googleapis/go-genai, without helm/helm, without mattn/anko | no |
| DeepSeek V4 Flash (max) > Grok 4.6 (medium) | 1.02 | -9.60 to 12.02 | 0.58 | failure cap=50, without abs-lang/abs, without googleapis/go-genai, without liweiyi88/onedump, without mattn/anko, without open-policy-agent/opa, without wazero/wazero | yes |
| Grok 4.6 (medium) > GLM-5.2 (max) | 0.47 | -9.24 to 10.01 | 0.55 | failure cap=0, failure cap=10, panel without GPT-5.4 (xhigh), panel without Muse Spark 1.1 (xhigh), panel without Muse Spark 1.2 (xhigh), without alecthomas/participle, without carvel-dev/ytt, without cockroachdb/pebble, without d5/tengo, without expr-lang/expr, without go-task/task, without golang/geo, without kgateway-dev/kgateway, without traefik/yaegi, without wazero/wazero, without xtaci/kcp-go | yes |
| GLM-5.2 (max) > GPT-5.6 Sol (max) | 0.33 | -10.02 to 10.50 | 0.52 | net weight=1, failure cap=50, without TomWright/dasel, without boyter/scc, without d5/tengo, without go-git/go-git, without googleapis/go-genai, without goreleaser/goreleaser, without helm/helm, without open-policy-agent/opa, without rhysd/actionlint, without xtaci/kcp-go | yes |
| GPT-5.6 Sol (max) > GPT-5.6 Terra (max) | 3.35 | -4.61 to 11.37 | 0.78 | none | yes |
| GPT-5.6 Terra (max) > GPT-5.5 (xhigh) | 0.51 | -6.77 to 7.87 | 0.54 | without alecthomas/participle, without cockroachdb/pebble, without go-critic/go-critic, without go-task/task, without open-policy-agent/opa, without rhysd/actionlint | yes |
| GPT-5.5 (xhigh) > Kimi K2.7 Code | 2.32 | -8.92 to 14.69 | 0.66 | failure cap=0, without d5/tengo | yes |
| Kimi K2.7 Code > GPT-5.6 Luna (max) | 0.03 | -11.51 to 11.66 | 0.48 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=50, panel without Claude Fable 5 (xhigh), panel without Claude Opus 4.8 (max), panel without Claude Sonnet 5 (max), panel without DeepSeek V4 Flash (max), panel without Gemini 3.5 Flash (high), panel without Gemini 3.6 Flash (high), panel without GLM-5.2 (max), panel without GLM-5.3 Flash (max), panel without GLM-5.3 (max), panel without GPT-5.6 Sol (max), panel without Grok 4.5 (high), panel without Grok 4.6 (medium), panel without Kimi K3 (max), panel without Qwen3.8 Max (xhigh), without abs-lang/abs, without alecthomas/participle, without beevik/etree, without boyter/scc, without carvel-dev/ytt, without getarcaneapp/arcane, without go-git/go-git, without go-task/task, without golang/geo, without googleapis/go-genai, without goreleaser/goreleaser, without helm/helm, without liweiyi88/onedump, without wazero/wazero, without xtaci/kcp-go | yes |
| GPT-5.6 Luna (max) > Gemini 3.5 Flash (high) | 1.39 | -8.63 to 11.30 | 0.61 | failure cap=0, failure cap=10, without d5/tengo, without open2b/scriggo | yes |
| Gemini 3.5 Flash (high) > DeepSeek V4 Pro (max) | 0.10 | -10.65 to 10.60 | 0.52 | net weight=0.5, failure cap=50, panel without Claude Fable 5 (xhigh), panel without Claude Opus 4.8 (max), panel without Claude Sonnet 5 (max), panel without DeepSeek V4 Flash (max), panel without Gemini 3.6 Flash (high), panel without Kimi K2.7 Code, panel without Kimi K3 (max), panel without Qwen3.8 Max (xhigh), without abs-lang/abs, without alecthomas/participle, without beevik/etree, without boyter/scc, without carvel-dev/ytt, without go-critic/go-critic, without go-git/go-git, without golang/geo, without googleapis/go-genai, without goreleaser/goreleaser, without helm/helm, without liweiyi88/onedump, without rhysd/actionlint, without wazero/wazero | yes |
| DeepSeek V4 Pro (max) > Grok 4.5 (high) | 0.33 | -9.08 to 9.96 | 0.52 | failure cap=0, failure cap=10, without Owloops/updo, without d5/tengo, without expr-lang/expr, without getarcaneapp/arcane, without go-task/task, without golang/geo, without kgateway-dev/kgateway, without muesli/termenv, without open-policy-agent/opa, without open2b/scriggo, without prometheus/prometheus | yes |
| Grok 4.5 (high) > GPT-5.4 (xhigh) | 4.81 | -5.79 to 14.78 | 0.82 | none | yes |
| GPT-5.4 (xhigh) > Muse Spark 1.2 (xhigh) | 2.43 | -8.01 to 12.70 | 0.69 | none | yes |
| Muse Spark 1.2 (xhigh) > Claude Sonnet 4.6 (high) | 2.25 | -8.27 to 12.33 | 0.66 | failure cap=0, without getarcaneapp/arcane | yes |
| Claude Sonnet 4.6 (high) > Muse Spark 1.1 (xhigh) | 0.22 | -9.63 to 10.73 | 0.51 | net weight=0.5, net weight=0.6, failure cap=50, panel without DeepSeek V4 Flash (max), panel without Gemini 3.6 Flash (high), panel without Gemini 3.7 Flash (medium), panel without Kimi K2.7 Code, without abs-lang/abs, without alecthomas/participle, without carvel-dev/ytt, without cockroachdb/pebble, without go-critic/go-critic, without helm/helm, without liweiyi88/onedump, without mattn/anko, without open-policy-agent/opa, without open2b/scriggo, without rhysd/actionlint | yes |
| Muse Spark 1.1 (xhigh) > Gemini 3.1 Pro Preview (high) | 5.06 | -5.33 to 13.81 | 0.84 | none | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 54.0 (1) | 54.1 (1) | 54.1 (1) | 54.0 (1) | 53.9 (1) | 53.9 (1) | 54.0 (1) | 57.2 (1) | 55.9 (1) | 50.8 (1) |
| Kimi K3 (max) | 52.0 (2) | 52.6 (2) | 52.4 (2) | 52.2 (2) | 51.9 (2) | 51.7 (2) | 52.0 (2) | 54.5 (2) | 53.5 (2) | 49.6 (2) |
| Claude Opus 4.8 (max) | 44.0 (3) | 44.4 (3) | 44.3 (3) | 44.1 (3) | 43.9 (3) | 43.7 (3) | 44.0 (3) | 48.1 (3) | 46.4 (3) | 39.9 (3) |
| GLM-5.3 (max) | 35.7 (4) | 35.7 (4) | 35.7 (4) | 35.7 (4) | 35.7 (4) | 35.7 (4) | 35.7 (4) | 38.3 (5) | 37.2 (5) | 33.1 (4) |
| Qwen3.8 Max (xhigh) | 35.1 (5) | 35.2 (5) | 35.2 (5) | 35.1 (5) | 35.0 (5) | 35.0 (5) | 35.1 (5) | 39.5 (4) | 37.7 (4) | 30.6 (7) |
| Gemini 3.7 Flash (medium) | 33.8 (6) | 33.6 (6) | 33.7 (6) | 33.8 (6) | 33.9 (6) | 34.0 (6) | 33.8 (6) | 37.0 (7) | 35.7 (7) | 30.7 (6) |
| Claude Opus 5 (max) | 33.4 (7) | 33.3 (7) | 33.3 (7) | 33.4 (7) | 33.4 (7) | 33.4 (7) | 33.4 (7) | 35.9 (8) | 34.9 (8) | 30.8 (5) |
| Gemini 3.6 Flash (high) | 33.1 (8) | 33.0 (8) | 33.0 (8) | 33.1 (8) | 33.1 (8) | 33.2 (8) | 33.1 (8) | 37.7 (6) | 35.9 (6) | 28.5 (8) |
| GLM-5.3 Flash (max) | 30.7 (9) | 30.6 (10) | 30.6 (9) | 30.7 (9) | 30.7 (9) | 30.7 (9) | 30.7 (9) | 34.5 (10) | 33.0 (10) | 26.9 (9) |
| Claude Sonnet 5 (max) | 30.5 (10) | 30.7 (9) | 30.6 (10) | 30.6 (10) | 30.5 (10) | 30.4 (10) | 30.5 (10) | 35.8 (9) | 33.7 (9) | 25.3 (13) |
| DeepSeek V4 Flash (max) | 30.0 (11) | 30.1 (11) | 30.0 (11) | 30.0 (11) | 29.9 (11) | 29.9 (11) | 30.0 (11) | 34.5 (11) | 32.7 (11) | 25.5 (11) |
| Grok 4.6 (medium) | 28.9 (12) | 28.9 (12) | 28.9 (12) | 28.9 (12) | 29.0 (12) | 29.0 (12) | 28.9 (12) | 32.2 (13) | 30.9 (13) | 25.7 (10) |
| GLM-5.2 (max) | 28.5 (13) | 28.3 (13) | 28.4 (13) | 28.4 (13) | 28.5 (13) | 28.6 (14) | 28.5 (13) | 33.4 (12) | 31.4 (12) | 23.5 (14) |
| GPT-5.6 Sol (max) | 28.1 (14) | 27.3 (14) | 27.6 (14) | 27.8 (14) | 28.4 (14) | 28.7 (13) | 28.1 (14) | 30.9 (14) | 29.8 (14) | 25.4 (12) |
| GPT-5.6 Terra (max) | 24.8 (15) | 24.6 (15) | 24.6 (15) | 24.7 (15) | 24.9 (15) | 24.9 (15) | 24.8 (15) | 27.6 (16) | 26.5 (15) | 21.9 (15) |
| GPT-5.5 (xhigh) | 24.3 (16) | 24.1 (16) | 24.2 (16) | 24.2 (16) | 24.3 (16) | 24.4 (16) | 24.3 (16) | 27.4 (17) | 26.2 (16) | 21.1 (16) |
| Kimi K2.7 Code | 22.0 (17) | 21.9 (18) | 21.9 (18) | 21.9 (18) | 22.0 (17) | 22.0 (17) | 22.0 (17) | 28.4 (15) | 25.8 (17) | 15.5 (19) |
| GPT-5.6 Luna (max) | 21.9 (18) | 22.1 (17) | 22.0 (17) | 22.0 (17) | 21.9 (18) | 21.8 (18) | 21.9 (18) | 24.7 (20) | 23.6 (19) | 19.1 (17) |
| Gemini 3.5 Flash (high) | 20.5 (19) | 20.5 (20) | 20.5 (19) | 20.5 (19) | 20.6 (19) | 20.6 (19) | 20.5 (19) | 27.4 (18) | 24.6 (18) | 13.7 (21) |
| DeepSeek V4 Pro (max) | 20.4 (20) | 20.6 (19) | 20.5 (20) | 20.5 (20) | 20.4 (20) | 20.4 (20) | 20.4 (20) | 24.7 (21) | 23.0 (21) | 16.2 (18) |
| Grok 4.5 (high) | 20.1 (21) | 20.1 (21) | 20.1 (21) | 20.1 (21) | 20.1 (21) | 20.1 (21) | 20.1 (21) | 25.5 (19) | 23.3 (20) | 14.7 (20) |
| GPT-5.4 (xhigh) | 15.3 (22) | 14.7 (22) | 14.9 (22) | 15.1 (22) | 15.5 (22) | 15.7 (22) | 15.3 (22) | 20.1 (22) | 18.2 (22) | 10.5 (22) |
| Muse Spark 1.2 (xhigh) | 12.9 (23) | 13.0 (23) | 13.0 (23) | 12.9 (23) | 12.8 (23) | 12.8 (23) | 12.9 (23) | 17.8 (24) | 15.8 (23) | 7.9 (23) |
| Claude Sonnet 4.6 (high) | 10.6 (24) | 10.5 (25) | 10.5 (25) | 10.6 (24) | 10.7 (24) | 10.7 (24) | 10.6 (24) | 19.1 (23) | 15.7 (24) | 2.2 (25) |
| Muse Spark 1.1 (xhigh) | 10.4 (25) | 10.6 (24) | 10.5 (24) | 10.5 (25) | 10.3 (25) | 10.3 (25) | 10.4 (25) | 16.0 (25) | 13.8 (25) | 4.8 (24) |
| Gemini 3.1 Pro Preview (high) | 5.3 (26) | 5.3 (26) | 5.3 (26) | 5.3 (26) | 5.4 (26) | 5.4 (26) | 5.3 (26) | 13.2 (26) | 10.1 (26) | -2.5 (26) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (0 of 8728 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Fable 5 (xhigh) | 388 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| Claude Opus 4.8 (max) | 332 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| Claude Opus 5 (max) | 432 | 0 | Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9 |
| Claude Sonnet 4.6 (high) | 144 | 0 | none |
| Claude Sonnet 5 (max) | 264 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| DeepSeek V4 Flash (max) | 336 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| DeepSeek V4 Pro (max) | 364 | 0 | GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9 |
| Gemini 3.1 Pro Preview (high) | 80 | 0 | none |
| Gemini 3.5 Flash (high) | 216 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |
| Gemini 3.6 Flash (high) | 320 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| Gemini 3.7 Flash (medium) | 408 | 0 | Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| GLM-5.2 (max) | 268 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |
| GLM-5.3 Flash (max) | 376 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |
| GLM-5.3 (max) | 408 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |
| GPT-5.4 (xhigh) | 344 | 0 | Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→12 |
| GPT-5.5 (xhigh) | 408 | 0 | none |
| GPT-5.6 Luna (max) | 428 | 0 | GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9 |
| GPT-5.6 Sol (max) | 428 | 0 | GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |
| GPT-5.6 Terra (max) | 420 | 0 | GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9 |
| Grok 4.5 (high) | 308 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |
| Grok 4.6 (medium) | 400 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |
| Kimi K2.7 Code | 232 | 0 | Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| Kimi K3 (max) | 424 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| Muse Spark 1.1 (xhigh) | 324 | 0 | GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→12 |
| Muse Spark 1.2 (xhigh) | 340 | 0 | Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→12 |
| Qwen3.8 Max (xhigh) | 336 | 0 | Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| (dedup panel) | 0 | 0 | none |

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| Owloops/updo (4) | Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→19 |
| TomWright/dasel (4) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→6, Claude Sonnet 5 (max) 10→11, DeepSeek V4 Flash (max) 11→10, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→13 |
| abs-lang/abs (8) | GLM-5.3 (max) 4→5, Qwen3.8 Max (xhigh) 5→7, Gemini 3.7 Flash (medium) 6→4, Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→6, GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, DeepSeek V4 Flash (max) 11→12, Grok 4.6 (medium) 12→11, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| alecthomas/participle (4) | GLM-5.3 (max) 4→5, Qwen3.8 Max (xhigh) 5→4, GLM-5.3 Flash (max) 9→11, DeepSeek V4 Flash (max) 11→9, Grok 4.6 (medium) 12→14, GLM-5.2 (max) 13→12, GPT-5.6 Sol (max) 14→13, GPT-5.6 Terra (max) 15→16, GPT-5.5 (xhigh) 16→15, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→21, DeepSeek V4 Pro (max) 20→19, Grok 4.5 (high) 21→20, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| beevik/etree (4) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→6, GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, Kimi K2.7 Code 17→19, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→18 |
| boyter/scc (4) | Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, Claude Sonnet 5 (max) 10→11, DeepSeek V4 Flash (max) 11→10, Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→12, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| carvel-dev/ytt (4) | Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, GLM-5.3 Flash (max) 9→11, DeepSeek V4 Flash (max) 11→9, Grok 4.6 (medium) 12→14, GLM-5.2 (max) 13→12, GPT-5.6 Sol (max) 14→13, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| cockroachdb/pebble (4) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→6, GLM-5.3 Flash (max) 9→11, Claude Sonnet 5 (max) 10→9, DeepSeek V4 Flash (max) 11→10, Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→12, GPT-5.6 Terra (max) 15→16, GPT-5.5 (xhigh) 16→15, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| d5/tengo (8) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→6, GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→11, DeepSeek V4 Flash (max) 11→9, Grok 4.6 (medium) 12→14, GPT-5.6 Sol (max) 14→12, GPT-5.5 (xhigh) 16→17, Kimi K2.7 Code 17→16, GPT-5.6 Luna (max) 18→19, Gemini 3.5 Flash (high) 19→18, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20 |
| expr-lang/expr (4) | GLM-5.3 Flash (max) 9→11, Claude Sonnet 5 (max) 10→9, DeepSeek V4 Flash (max) 11→10, Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→12, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20 |
| getarcaneapp/arcane (4) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→6, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20, Muse Spark 1.2 (xhigh) 23→24, Claude Sonnet 4.6 (high) 24→23 |
| go-critic/go-critic (4) | Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, Claude Sonnet 5 (max) 10→11, DeepSeek V4 Flash (max) 11→10, GPT-5.6 Terra (max) 15→16, GPT-5.5 (xhigh) 16→15, GPT-5.6 Luna (max) 18→20, Gemini 3.5 Flash (high) 19→21, DeepSeek V4 Pro (max) 20→18, Grok 4.5 (high) 21→19, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| go-git/go-git (4) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→6, Claude Sonnet 5 (max) 10→11, DeepSeek V4 Flash (max) 11→10, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→13, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| go-task/task (4) | GLM-5.3 (max) 4→5, Qwen3.8 Max (xhigh) 5→4, Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, GLM-5.3 Flash (max) 9→11, Claude Sonnet 5 (max) 10→9, DeepSeek V4 Flash (max) 11→10, Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→12, GPT-5.6 Terra (max) 15→16, GPT-5.5 (xhigh) 16→15, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20 |
| golang/geo (4) | GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, DeepSeek V4 Flash (max) 11→12, Grok 4.6 (medium) 12→14, GLM-5.2 (max) 13→11, GPT-5.6 Sol (max) 14→13, Kimi K2.7 Code 17→20, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→21, DeepSeek V4 Pro (max) 20→19, Grok 4.5 (high) 21→18 |
| googleapis/go-genai (4) | Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, Claude Sonnet 5 (max) 10→12, Grok 4.6 (medium) 12→10, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→13, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→21, DeepSeek V4 Pro (max) 20→19, Grok 4.5 (high) 21→20 |
| goreleaser/goreleaser (4) | GLM-5.3 (max) 4→5, Qwen3.8 Max (xhigh) 5→4, GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→13, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| helm/helm (8) | GLM-5.3 (max) 4→6, Qwen3.8 Max (xhigh) 5→7, Gemini 3.7 Flash (medium) 6→4, Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→5, GLM-5.3 Flash (max) 9→11, DeepSeek V4 Flash (max) 11→9, Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→12, Kimi K2.7 Code 17→19, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→21, DeepSeek V4 Pro (max) 20→18, Grok 4.5 (high) 21→20, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| kgateway-dev/kgateway (4) | Gemini 3.7 Flash (medium) 6→8, Claude Opus 5 (max) 7→6, Gemini 3.6 Flash (high) 8→7, DeepSeek V4 Flash (max) 11→12, Grok 4.6 (medium) 12→14, GLM-5.2 (max) 13→11, GPT-5.6 Sol (max) 14→13, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20 |
| liweiyi88/onedump (4) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→6, DeepSeek V4 Flash (max) 11→13, Grok 4.6 (medium) 12→11, GLM-5.2 (max) 13→12, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| mattn/anko (8) | GLM-5.3 (max) 4→5, Qwen3.8 Max (xhigh) 5→4, Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→6, GLM-5.3 Flash (max) 9→11, Claude Sonnet 5 (max) 10→12, DeepSeek V4 Flash (max) 11→10, Grok 4.6 (medium) 12→9, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| muesli/termenv (4) | Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→19 |
| open-policy-agent/opa (8) | Qwen3.8 Max (xhigh) 5→6, Gemini 3.7 Flash (medium) 6→5, Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, Claude Sonnet 5 (max) 10→11, DeepSeek V4 Flash (max) 11→12, Grok 4.6 (medium) 12→10, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→13, GPT-5.6 Terra (max) 15→16, GPT-5.5 (xhigh) 16→15, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| open2b/scriggo (4) | GLM-5.3 (max) 4→5, Qwen3.8 Max (xhigh) 5→4, Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, GPT-5.6 Luna (max) 18→19, Gemini 3.5 Flash (high) 19→18, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| prometheus/prometheus (4) | Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→6, GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, DeepSeek V4 Pro (max) 20→21, Grok 4.5 (high) 21→20 |
| rhysd/actionlint (4) | Claude Opus 5 (max) 7→8, Gemini 3.6 Flash (high) 8→7, GLM-5.2 (max) 13→14, GPT-5.6 Sol (max) 14→13, GPT-5.6 Terra (max) 15→16, GPT-5.5 (xhigh) 16→15, Gemini 3.5 Flash (high) 19→21, DeepSeek V4 Pro (max) 20→19, Grok 4.5 (high) 21→20, Claude Sonnet 4.6 (high) 24→25, Muse Spark 1.1 (xhigh) 25→24 |
| traefik/yaegi (4) | Gemini 3.7 Flash (medium) 6→8, Claude Opus 5 (max) 7→6, Gemini 3.6 Flash (high) 8→7, Grok 4.6 (medium) 12→13, GLM-5.2 (max) 13→12 |
| wazero/wazero (4) | Qwen3.8 Max (xhigh) 5→6, Gemini 3.7 Flash (medium) 6→8, Claude Opus 5 (max) 7→5, Gemini 3.6 Flash (high) 8→7, GLM-5.3 Flash (max) 9→10, Claude Sonnet 5 (max) 10→9, DeepSeek V4 Flash (max) 11→13, GLM-5.2 (max) 13→11, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17, Gemini 3.5 Flash (high) 19→20, DeepSeek V4 Pro (max) 20→19 |
| xtaci/kcp-go (4) | Qwen3.8 Max (xhigh) 5→6, Gemini 3.7 Flash (medium) 6→7, Claude Opus 5 (max) 7→5, Grok 4.6 (medium) 12→14, GPT-5.6 Sol (max) 14→12, Kimi K2.7 Code 17→18, GPT-5.6 Luna (max) 18→17 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (110) | Solved by fewer (110) |
|---|---:|---:|
| Claude Fable 5 (xhigh) | 54.0 (1) | 54.0 (1) |
| Kimi K3 (max) | 52.0 (2) | 52.0 (2) |
| Claude Opus 4.8 (max) | 44.0 (3) | 44.0 (3) |
| GLM-5.3 (max) | 35.7 (4) | 35.7 (4) |
| Qwen3.8 Max (xhigh) | 35.1 (5) | 35.1 (5) |
| Gemini 3.7 Flash (medium) | 33.8 (6) | 33.8 (6) |
| Claude Opus 5 (max) | 33.4 (7) | 33.4 (7) |
| Gemini 3.6 Flash (high) | 33.1 (8) | 33.1 (8) |
| GLM-5.3 Flash (max) | 30.7 (9) | 30.7 (9) |
| Claude Sonnet 5 (max) | 30.5 (10) | 30.5 (10) |
| DeepSeek V4 Flash (max) | 30.0 (11) | 30.0 (11) |
| Grok 4.6 (medium) | 28.9 (12) | 28.9 (12) |
| GLM-5.2 (max) | 28.5 (13) | 28.5 (13) |
| GPT-5.6 Sol (max) | 28.1 (14) | 28.1 (14) |
| GPT-5.6 Terra (max) | 24.8 (15) | 24.8 (15) |
| GPT-5.5 (xhigh) | 24.3 (16) | 24.3 (16) |
| Kimi K2.7 Code | 22.0 (17) | 22.0 (17) |
| GPT-5.6 Luna (max) | 21.9 (18) | 21.9 (18) |
| Gemini 3.5 Flash (high) | 20.5 (19) | 20.5 (19) |
| DeepSeek V4 Pro (max) | 20.4 (20) | 20.4 (20) |
| Grok 4.5 (high) | 20.1 (21) | 20.1 (21) |
| GPT-5.4 (xhigh) | 15.3 (22) | 15.3 (22) |
| Muse Spark 1.2 (xhigh) | 12.9 (23) | 12.9 (23) |
| Claude Sonnet 4.6 (high) | 10.6 (24) | 10.6 (24) |
| Muse Spark 1.1 (xhigh) | 10.4 (25) | 10.4 (25) |
| Gemini 3.1 Pro Preview (high) | 5.3 (26) | 5.3 (26) |

## What drives each adjacent gap

Difference in mean score split by outcome (a/b), and the tasks that move it most. Contributions are per-task differences divided by the task count, so they sum to the gap.

- **Claude Fable 5 (xhigh) − Kimi K3 (max) = 1.70**: failed/failed 0.04 (19), failed/solved -10.99 (20), solved/failed 6.99 (10), solved/solved 5.66 (86). For Claude Fable 5 (xhigh): `geo-shapeindex-serialization#1` +0.81 (solved/failed), `ytt-jsonpath-query-api#4` +0.81 (solved/failed), `go-critic-doc-link-checker#1` +0.79 (solved/failed). For Kimi K3 (max): `onedump-dump-encryption-pipeline#4` -0.82 (failed/solved), `expr-try-catch-errors#2` -0.77 (failed/solved), `prometheus-typed-label-sorting#3` -0.76 (failed/solved).
- **Kimi K3 (max) − Claude Opus 4.8 (max) = 8.12**: failed/failed -0.35 (14), failed/solved -7.96 (11), solved/failed 16.74 (25), solved/solved -0.31 (72). For Kimi K3 (max): `goreleaser-retry-publish-auditing#4` +0.90 (solved/failed), `anko-typed-variable-bindings#2` +0.89 (solved/failed), `arcane-drift-detection-baselines#2` +0.88 (solved/failed). For Claude Opus 4.8 (max): `tengo-destructuring-bindings#1` -0.85 (failed/solved), `helm-array-merge-strategies#4` -0.85 (failed/solved), `geo-shapeindex-serialization#1` -0.85 (failed/solved).
- **Claude Opus 4.8 (max) − GLM-5.3 (max) = 7.54**: failed/failed 0.31 (14), failed/solved -10.85 (24), solved/failed 8.66 (13), solved/solved 9.42 (70). For Claude Opus 4.8 (max): `tengo-destructuring-bindings#3` +0.88 (solved/failed), `pebble-durability-wait-apis#4` +0.82 (solved/failed), `kcp-go-multiplexed-kcp-streams#1` +0.80 (solved/failed). For GLM-5.3 (max): `abs-stepped-slices#4` -0.84 (failed/solved), `anko-typed-variable-bindings#4` -0.75 (failed/solved), `goreleaser-retry-publish-auditing#4` -0.63 (failed/solved).
- **GLM-5.3 (max) − Qwen3.8 Max (xhigh) = 1.03**: failed/failed -0.02 (20), failed/solved -6.73 (12), solved/failed 13.65 (32), solved/solved -5.86 (70). For GLM-5.3 (max): `goreleaser-retry-publish-auditing#3` +0.73 (solved/failed), `abs-stepped-slices#3` +0.69 (solved/failed), `anko-default-function-arguments#3` +0.67 (solved/solved). For Qwen3.8 Max (xhigh): `helm-array-merge-strategies#3` -0.83 (failed/solved), `kcp-go-multiplexed-kcp-streams#1` -0.73 (failed/solved), `kcp-go-multiplexed-kcp-streams#3` -0.68 (failed/solved).
- **Qwen3.8 Max (xhigh) − Gemini 3.7 Flash (medium) = 1.25**: failed/failed 0.20 (19), failed/solved -14.37 (33), solved/failed 8.91 (15), solved/solved 6.50 (69). For Qwen3.8 Max (xhigh): `helm-array-merge-strategies#3` +0.82 (solved/failed), `opa-rego-rule-profiling#3` +0.78 (solved/failed), `abs-module-cache-flags#2` +0.77 (solved/failed). For Gemini 3.7 Flash (medium): `yaegi-go-embed-directives#1` -0.74 (failed/solved), `yaegi-go-embed-directives#4` -0.74 (failed/solved), `onedump-dump-encryption-pipeline#2` -0.73 (failed/solved).
- **Gemini 3.7 Flash (medium) − Claude Opus 5 (max) = 0.60**: failed/solved -9.40 (24), solved/failed 6.44 (15), solved/solved 3.55 (84). For Gemini 3.7 Flash (medium): `yaegi-go-embed-directives#1` +0.78 (solved/failed), `yaegi-go-embed-directives#4` +0.76 (solved/failed), `kcp-go-multiplexed-kcp-streams#4` +0.75 (solved/failed). For Claude Opus 5 (max): `abs-stepped-slices#1` -0.74 (failed/solved), `opa-rego-rule-profiling#3` -0.73 (failed/solved), `abs-stepped-slices#3` -0.72 (failed/solved).
- **Claude Opus 5 (max) − Gemini 3.6 Flash (high) = -0.21**: failed/solved -8.59 (16), solved/failed 17.82 (45), solved/solved -9.44 (63). For Claude Opus 5 (max): `pebble-durability-wait-apis#4` +0.76 (solved/failed), `task-task-graph-export#2` +0.72 (solved/failed), `abs-stepped-slices#3` +0.72 (solved/failed). For Gemini 3.6 Flash (high): `kcp-go-multiplexed-kcp-streams#1` -0.79 (failed/solved), `kcp-go-multiplexed-kcp-streams#2` -0.76 (failed/solved), `anko-typed-variable-bindings#2` -0.73 (failed/solved).
- **Gemini 3.6 Flash (high) − GLM-5.3 Flash (max) = 2.19**: failed/failed -0.02 (18), failed/solved -16.57 (38), solved/failed 12.00 (23), solved/solved 6.78 (56). For Gemini 3.6 Flash (high): `actionlint-action-pinning-lint#3` +0.83 (solved/failed), `go-git-worktree-merge-conflicts#4` +0.81 (solved/failed), `etree-xml-diff-patch#4` +0.77 (solved/failed). For GLM-5.3 Flash (max): `abs-stepped-slices#2` -0.80 (failed/solved), `dasel-html-document-format#2` -0.76 (failed/solved), `tengo-destructuring-bindings#4` -0.74 (failed/solved).
- **GLM-5.3 Flash (max) − Claude Sonnet 5 (max) = 0.32**: failed/failed -0.27 (17), failed/solved -13.17 (21), solved/failed 21.08 (43), solved/solved -7.33 (45). For GLM-5.3 Flash (max): `abs-stepped-slices#2` +0.85 (solved/failed), `kgateway-consistent-hash-policy#3` +0.83 (solved/failed), `prometheus-typed-label-sorting#2` +0.80 (solved/failed). For Claude Sonnet 5 (max): `tengo-callable-instance-isolation#3` -0.85 (failed/solved), `anko-typed-variable-bindings#1` -0.82 (failed/solved), `anko-typed-variable-bindings#3` -0.79 (failed/solved).
- **Claude Sonnet 5 (max) − DeepSeek V4 Flash (max) = -1.64**: failed/failed 0.40 (29), failed/solved -15.37 (32), solved/failed 10.66 (17), solved/solved 2.67 (49). For Claude Sonnet 5 (max): `go-git-worktree-merge-conflicts#1` +0.86 (solved/failed), `tengo-callable-instance-isolation#1` +0.78 (solved/failed), `scc-bounded-memory-spilling#4` +0.77 (solved/failed). For DeepSeek V4 Flash (max): `wazero-multi-module-snapshots#3` -0.84 (failed/solved), `wazero-multi-module-snapshots#1` -0.83 (failed/solved), `kgateway-consistent-hash-policy#3` -0.79 (failed/solved).
- **DeepSeek V4 Flash (max) − Grok 4.6 (medium) = 1.02**: failed/failed 0.10 (20), failed/solved -13.76 (32), solved/failed 8.68 (16), solved/solved 6.00 (68). For DeepSeek V4 Flash (max): `kgateway-consistent-hash-policy#2` +0.82 (solved/failed), `opa-rego-rule-profiling#4` +0.80 (solved/failed), `opa-template-string-reconstruction#2` +0.78 (solved/failed). For Grok 4.6 (medium): `yaegi-go-embed-directives#4` -0.81 (failed/solved), `scc-bounded-memory-spilling#4` -0.79 (failed/solved), `go-git-worktree-merge-conflicts#1` -0.69 (failed/solved).
- **Grok 4.6 (medium) − GLM-5.2 (max) = 0.47**: failed/failed -0.47 (23), failed/solved -8.11 (13), solved/failed 17.89 (46), solved/solved -8.84 (54). For Grok 4.6 (medium): `yaegi-go-embed-directives#4` +0.80 (solved/failed), `geo-shapeindex-serialization#2` +0.74 (solved/failed), `tengo-destructuring-bindings#1` +0.65 (solved/failed). For GLM-5.2 (max): `opa-template-string-reconstruction#2` -0.80 (failed/solved), `helm-array-merge-strategies#1` -0.75 (failed/solved), `anko-default-function-arguments#1` -0.71 (failed/solved).
- **GLM-5.2 (max) − GPT-5.6 Sol (max) = 0.33**: failed/failed 0.54 (23), failed/solved -16.33 (46), solved/failed 3.67 (6), solved/solved 12.46 (61). For GLM-5.2 (max): `abs-module-cache-flags#2` +0.79 (solved/failed), `helm-array-merge-strategies#1` +0.74 (solved/failed), `abs-module-cache-flags#3` +0.68 (solved/failed). For GPT-5.6 Sol (max): `go-critic-doc-link-checker#3` -0.82 (failed/solved), `arcane-drift-detection-baselines#1` -0.74 (failed/solved), `abs-stepped-slices#2` -0.67 (failed/solved).
- **GPT-5.6 Sol (max) − GPT-5.6 Terra (max) = 3.35**: failed/failed -0.02 (13), failed/solved -6.80 (16), solved/failed 7.94 (18), solved/solved 2.23 (89). For GPT-5.6 Sol (max): `scriggo-method-declarations#2` +0.74 (solved/failed), `dasel-html-document-format#2` +0.64 (solved/failed), `opa-rego-rule-profiling#4` +0.63 (solved/failed). For GPT-5.6 Terra (max): `go-critic-doc-link-checker#2` -0.74 (failed/solved), `participle-grammar-conflict-analysis#4` -0.67 (failed/solved), `opa-rego-rule-profiling#2` -0.66 (failed/solved).
- **GPT-5.6 Terra (max) − GPT-5.5 (xhigh) = 0.51**: failed/solved -6.55 (15), solved/failed 6.60 (18), solved/solved 0.46 (87). For GPT-5.6 Terra (max): `opa-rego-rule-profiling#2` +0.66 (solved/failed), `participle-grammar-conflict-analysis#4` +0.66 (solved/failed), `actionlint-action-pinning-lint#4` +0.53 (solved/solved). For GPT-5.5 (xhigh): `yaegi-go-embed-directives#4` -0.79 (failed/solved), `scriggo-method-declarations#4` -0.75 (failed/solved), `expr-try-catch-errors#4` -0.70 (failed/solved).
- **GPT-5.5 (xhigh) − Kimi K2.7 Code = 2.32**: failed/failed -0.23 (24), failed/solved -5.95 (10), solved/failed 20.70 (54), solved/solved -12.20 (48). For GPT-5.5 (xhigh): `yaegi-go-embed-directives#3` +0.77 (solved/failed), `expr-try-catch-errors#4` +0.69 (solved/failed), `scriggo-method-declarations#4` +0.67 (solved/failed). For Kimi K2.7 Code: `participle-grammar-conflict-analysis#4` -0.82 (failed/solved), `onedump-dump-encryption-pipeline#2` -0.77 (failed/solved), `go-git-worktree-merge-conflicts#1` -0.75 (failed/solved).
- **Kimi K2.7 Code − GPT-5.6 Luna (max) = 0.03**: failed/failed 0.24 (22), failed/solved -18.93 (56), solved/failed 4.56 (7), solved/solved 14.16 (51). For Kimi K2.7 Code: `participle-grammar-conflict-analysis#4` +0.83 (solved/failed), `etree-xml-diff-patch#4` +0.75 (solved/failed), `go-git-worktree-merge-conflicts#1` +0.74 (solved/failed). For GPT-5.6 Luna (max): `yaegi-go-embed-directives#2` -0.82 (failed/solved), `opa-rego-rule-profiling#1` -0.73 (failed/solved), `opa-template-string-reconstruction#4` -0.66 (failed/solved).
- **GPT-5.6 Luna (max) − Gemini 3.5 Flash (high) = 1.39**: failed/failed -0.23 (20), failed/solved -4.38 (9), solved/failed 19.12 (62), solved/solved -13.13 (45). For GPT-5.6 Luna (max): `yaegi-go-embed-directives#2` +0.82 (solved/failed), `scriggo-method-declarations#1` +0.68 (solved/failed), `abs-stepped-slices#1` +0.66 (solved/failed). For Gemini 3.5 Flash (high): `helm-array-merge-strategies#2` -0.71 (failed/solved), `geo-shapeindex-serialization#4` -0.65 (solved/solved), `updo-policy-alerting#4` -0.63 (failed/solved).
- **Gemini 3.5 Flash (high) − DeepSeek V4 Pro (max) = 0.10**: failed/failed 0.30 (34), failed/solved -18.07 (48), solved/failed 6.22 (11), solved/solved 11.64 (43). For Gemini 3.5 Flash (high): `goreleaser-retry-publish-auditing#1` +0.80 (solved/failed), `onedump-dump-encryption-pipeline#2` +0.71 (solved/failed), `helm-array-merge-strategies#2` +0.71 (solved/failed). For DeepSeek V4 Pro (max): `updo-policy-alerting#3` -0.78 (failed/solved), `termenv-preserve-ansi-resets#1` -0.76 (failed/solved), `kgateway-consistent-hash-policy#2` -0.73 (failed/solved).
- **DeepSeek V4 Pro (max) − Grok 4.5 (high) = 0.33**: failed/failed 0.10 (28), failed/solved -7.25 (17), solved/failed 11.73 (31), solved/solved -4.25 (60). For DeepSeek V4 Pro (max): `updo-policy-alerting#3` +0.78 (solved/failed), `termenv-preserve-ansi-resets#1` +0.78 (solved/failed), `prometheus-typed-label-sorting#3` +0.72 (solved/failed). For Grok 4.5 (high): `tengo-destructuring-bindings#1` -0.77 (failed/solved), `anko-typed-variable-bindings#1` -0.60 (failed/solved), `kcp-go-multiplexed-kcp-streams#4` -0.59 (failed/solved).
- **Grok 4.5 (high) − GPT-5.4 (xhigh) = 4.81**: failed/failed 0.01 (27), failed/solved -10.89 (32), solved/failed 9.20 (23), solved/solved 6.48 (54). For Grok 4.5 (high): `goreleaser-retry-publish-auditing#3` +0.76 (solved/failed), `tengo-destructuring-bindings#1` +0.76 (solved/failed), `opa-template-string-reconstruction#3` +0.57 (solved/failed). For GPT-5.4 (xhigh): `prometheus-typed-label-sorting#3` -0.77 (failed/solved), `termenv-preserve-ansi-resets#4` -0.71 (failed/solved), `geo-shapeindex-serialization#2` -0.69 (failed/solved).
- **GPT-5.4 (xhigh) − Muse Spark 1.2 (xhigh) = 2.43**: failed/failed 0.11 (27), failed/solved -7.99 (23), solved/failed 8.93 (24), solved/solved 1.37 (62). For GPT-5.4 (xhigh): `scriggo-method-declarations#1` +0.79 (solved/failed), `termenv-preserve-ansi-resets#4` +0.71 (solved/failed), `scriggo-method-declarations#3` +0.66 (solved/failed). For Muse Spark 1.2 (xhigh): `arcane-drift-detection-baselines#1` -0.82 (failed/solved), `anko-default-function-arguments#2` -0.81 (failed/solved), `wazero-multi-module-snapshots#1` -0.68 (failed/solved).
- **Muse Spark 1.2 (xhigh) − Claude Sonnet 4.6 (high) = 2.28**: failed/failed -0.33 (39), failed/solved -6.80 (11), solved/failed 17.23 (60), solved/solved -7.83 (25). For Muse Spark 1.2 (xhigh): `arcane-drift-detection-baselines#1` +0.82 (solved/failed), `anko-default-function-arguments#2` +0.80 (solved/failed), `arcane-drift-detection-baselines#3` +0.77 (solved/failed). For Claude Sonnet 4.6 (high): `opa-template-string-reconstruction#1` -0.84 (failed/solved), `participle-grammar-conflict-analysis#2` -0.81 (failed/solved), `helm-unified-manifest-stream#1` -0.80 (failed/solved).
- **Claude Sonnet 4.6 (high) − Muse Spark 1.1 (xhigh) = -0.03**: failed/failed 0.69 (43), failed/solved -16.28 (56), solved/failed 5.59 (10), solved/solved 9.98 (25). For Claude Sonnet 4.6 (high): `helm-unified-manifest-stream#2` +0.78 (solved/failed), `participle-grammar-conflict-analysis#2` +0.69 (solved/solved), `pebble-durability-wait-apis#2` +0.68 (solved/failed). For Muse Spark 1.1 (xhigh): `scc-bounded-memory-spilling#4` -0.78 (failed/solved), `tengo-callable-instance-isolation#1` -0.75 (failed/solved), `kcp-go-multiplexed-kcp-streams#4` -0.65 (failed/solved).
- **Muse Spark 1.1 (xhigh) − Gemini 3.1 Pro Preview (high) = 5.04**: failed/failed -1.52 (47), failed/solved -4.64 (6), solved/failed 17.18 (66), solved/solved -5.98 (14). For Muse Spark 1.1 (xhigh): `scc-bounded-memory-spilling#4` +0.77 (solved/failed), `wazero-multi-module-snapshots#4` +0.75 (solved/failed), `tengo-callable-instance-isolation#1` +0.73 (solved/failed). For Gemini 3.1 Pro Preview (high): `opa-rego-rule-profiling#2` -0.86 (failed/solved), `ytt-jsonpath-query-api#4` -0.86 (failed/solved), `go-git-worktree-merge-conflicts#2` -0.84 (failed/solved).

## Regenerate

```sh
python -m parsimony.stability examples/deepswe-go/score-panel.json examples/deepswe-go/*.jsonl --output examples/deepswe-go/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
