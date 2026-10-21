# DeepSWE: 26 current models × 34 Python tasks × 4 attempts (analyzer 0.5.2)

**Beta research preview, not an official ranking.** [DeepSWE](https://deepswe.datacurve.ai) ([paper](https://arxiv.org/abs/2607.07946), [tasks](https://github.com/datacurve-ai/deep-swe)) is a 2026 benchmark of original, long-horizon tasks from active open-source repositories. Every model runs with mini-SWE-agent, four attempts per task, and DeepSWE publishes each run's final patch and pass/fail. This folder measures the Python tasks; it has its own [board](../../site/python.html) and is one of the four languages combined on the site's front page. The [35-model SWE-bench Verified results](../mini-swe-agent-500/README.md) are the second board.

## Pinned inputs

- Analyzer `0.5.2-beta`, commit `1b50e56`, Python 3.14.7.
- DeepSWE tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea` (34 Python tasks). Runs: release `v1.1`, run index `trials.json` SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6` (runs from June to September 2026).
- Dataset (items with reference solutions) SHA256 `41a44998c70248e0a3e2a4cf43a8838b70248537d1f3a458838f2f7e09ecef8a`. Scoring `parsimony-80-20-v0.5`, panel `deepswe-v1.1-python-26-pooled-80-20-v0.5`.
- SHA256: [population.json](population.json) `c16b15f8…`, [score-panel.json](score-panel.json) `c280b21b…`, [scores.json](scores.json) `3382b497…`, [coverage.json](coverage.json) `9bb953a1…`, [sensitivity.json](sensitivity.json) `be889397…` (the last three regenerated 2026-10-21 with the release 1.0 runs).

```sh
git clone https://github.com/datacurve-ai/deep-swe && git -C deep-swe checkout 0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea
python -m parsimony.deepswe dataset deep-swe --output deepswe-python.jsonl
python -m parsimony.deepswe configs --output configs.json      # each model's best configuration with patches
python -m parsimony.deepswe analyze CONFIG --dataset deepswe-python.jsonl --output CONFIG.jsonl   # per config
python -m parsimony.release freeze deepswe-python.jsonl --name deepswe-v1.1-python-136 --output population.json
python -m parsimony.deepswe panel *.jsonl --name deepswe-v1.1-python-26-pooled-80-20-v0.5 --output score-panel.json
python -m parsimony.release audit population.json *.jsonl --dataset deepswe-python.jsonl --output coverage.json
python -m parsimony.scoring score score-panel.json *.jsonl --output scores.json
python -m parsimony.stability score-panel.json *.jsonl --output sensitivity.json
python -m parsimony.site score-panel.json *.jsonl --sensitivity sensitivity.json --benchmark deepswe --output site/python.html
```

## How DeepSWE is scored

- **One configuration per model:** each model's best-scoring configuration (reasoning effort) on DeepSWE's live leaderboard whose patches can be downloaded. GPT-6 Astra and Gemini 3.8 Flash are left out: their patches are not published.
- **Each attempt is an item.** A model has four items per task (`task#1` … `task#4`), 136 in all. Each item is scored against every passing patch of its task, from any model and attempt, and the four attempts of a task are resampled together for intervals and rank ranges.
- **33 tasks are scored:** no model solved `koota-entity-snapshot-rollback`, so it cannot calibrate footprint.
- **Reference solution:** DeepSWE's own solution for each task plays the role of the maintainers' fix (the *Churn vs reference* column). A few solutions lost the leading space of blank context lines; the dataset builder restores it.

## Ranking (same tasks)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Claude Fable 5 (xhigh) | 0.81× | 0.75–0.87× | 28 | +1,557.5 | +1,509.1 | 74.3% | 97/101 |
| 2 | Claude Opus 4.6 (max) · DeepSWE 1.0 | 0.83× | 0.76–0.91× | 18 | +1,774.6 | +1,696.0 | 27.2% | 35/37 |
| 3 | Claude Sonnet 5 (max) | 0.84× | 0.80–0.89× | 25 | +1,665.9 | +1,563.5 | 59.6% | 78/81 |
| 4 | Claude Opus 4.8 (max) | 0.85× | 0.81–0.89× | 29 | +1,621.9 | +1,592.2 | 63.2% | 83/86 |
| 5 | GLM-5.2 (max) | 0.85× | 0.81–0.90× | 24 | +1,733.2 | +1,591.3 | 41.9% | 53/57 |
| 6 | Kimi K3 (max) | 0.86× | 0.80–0.91× | 30 | +1,641.2 | +1,601.1 | 67.6% | 89/92 |
| 7 | Gemini 3.5 Flash (high) | 0.86× | 0.79–0.94× | 17 | +1,621.5 | +1,707.6 | 29.4% | 38/40 |
| 8 | Claude Sonnet 4.6 (high) | 0.87× | 0.77–0.98× | 19 | +1,684.5 | +1,587.9 | 29.4% | 36/40 |
| 9 | Kimi K2.7 Code | 0.90× | 0.85–0.95× | 20 | +1,737.3 | +1,600.1 | 24.3% | 32/33 |
| 10 | DeepSeek V4 Flash (max) | 0.94× | 0.89–1.01× | 27 | +1,748.7 | +1,770.3 | 48.5% | 63/66 |
| 11 | Qwen3.8 Max (xhigh) | 0.94× | 0.90–0.99× | 27 | +1,697.8 | +1,770.5 | 55.1% | 74/75 |
| 12 | Gemini 3.6 Flash (high) | 0.96× | 0.88–1.02× | 22 | +1,741.9 | +1,835.1 | 41.9% | 53/57 |
| 13 | Grok 4.5 (high) | 0.99× | 0.93–1.06× | 28 | +1,819.8 | +1,886.7 | 58.8% | 79/80 |
| 14 | Claude Opus 4.7 (max) · DeepSWE 1.0 | 1.00× | 0.94–1.07× | 27 | +1,853.9 | +1,867.7 | 50.0% | 63/68 |
| 15 | Grok 4.6 (medium) | 1.01× | 0.97–1.06× | 28 | +1,825.9 | +1,981.0 | 67.6% | 89/92 |
| 16 | GPT-5.4 (xhigh) | 1.04× | 0.97–1.12× | 25 | +1,913.5 | +2,058.9 | 46.3% | 59/63 |
| 17 | Gemini 3.7 Flash (medium) | 1.05× | 0.97–1.16× | 27 | +1,904.2 | +2,038.1 | 60.3% | 80/82 |
| 18 | GLM-5.3 Flash (max) | 1.06× | 1.00–1.12× | 29 | +2,006.5 | +1,998.5 | 69.9% | 93/95 |
| 19 | GPT-5.6 Sol (max) | 1.07× | 1.00–1.14× | 29 | +1,964.2 | +2,031.8 | 74.3% | 98/101 |
| 20 | GPT-5.6 Terra (max) | 1.07× | 1.02–1.12× | 29 | +2,028.7 | +2,096.5 | 68.4% | 90/93 |
| 21 | GPT-5.5 (xhigh) | 1.08× | 1.01–1.15× | 28 | +1,936.7 | +2,102.4 | 66.9% | 87/91 |
| 22 | DeepSeek V4 Pro (max) | 1.08× | 1.02–1.15× | 29 | +2,043.7 | +2,074.7 | 59.6% | 77/81 |
| 23 | GLM-5.3 (max) | 1.08× | 0.99–1.17× | 29 | +2,090.0 | +2,035.5 | 66.2% | 87/90 |
| 24 | GPT-5.6 Luna (max) | 1.15× | 1.08–1.22× | 30 | +2,202.3 | +2,203.8 | 65.4% | 85/89 |
| 25 | Claude Opus 5 (max) | 1.15× | 1.08–1.23× | 28 | +2,183.4 | +2,124.4 | 74.3% | 97/101 |
| 26 | Muse Spark 1.2 (xhigh) | 1.31× | 1.23–1.41× | 27 | +2,484.1 | +2,463.2 | 50.7% | 66/69 |
| 27 | Muse Spark 1.1 (xhigh) | 1.36× | 1.25–1.50× | 24 | +2,562.3 | +2,412.7 | 52.9% | 68/72 |
| — | Gemini 3 Flash Preview · DeepSWE 1.0 | 0.50× | — | 2 | +869.5 | +1,073.0 | 2.9% | 2/4 |
| — | Gemini 3.1 Pro Preview (high) | 0.68× | 0.58–0.78× | 8 | +1,479.5 | +1,156.3 | 8.1% | 11/11 |
| — | Kimi K2.6 · DeepSWE 1.0 | 0.81× | 0.72–0.92× | 14 | +1,543.8 | +1,612.5 | 18.4% | 23/25 |
| — | Qwen3.6 Plus · DeepSWE 1.0 | 0.85× | — | 1 | +1,604.0 | +1,883.3 | 0.7% | 1/1 |
| — | MiMo V2.5 Pro · DeepSWE 1.0 | 0.88× | 0.83–0.93× | 12 | +1,339.8 | +1,667.1 | 15.4% | 20/21 |
| — | Grok Build 0.1 · DeepSWE 1.0 | 0.96× | 0.82–1.13× | 8 | +1,675.7 | +1,646.2 | 11.0% | 15/15 |
| — | MiniMax M3 · DeepSWE 1.0 | 1.03× | 0.92–1.13× | 12 | +2,111.0 | +1,976.7 | 17.6% | 22/24 |
| — | GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 1.05× | 0.93–1.16× | 14 | +1,891.8 | +1,934.7 | 21.3% | 27/29 |
| — | GLM-5.1 · DeepSWE 1.0 | 1.21× | 0.75–2.16× | 8 | +1,953.0 | +1,843.8 | 9.6% | 11/13 |
| — | Claude Haiku 4.5 · DeepSWE 1.0 | — | — | — | — | +1,219.4 | 0.0% | 0/0 |
| — | MiniMax M2.7 · DeepSWE 1.0 | — | — | — | — | +1,684.6 | 0.0% | 0/0 |

## Archived Score diagnostic (not the ranking)

| Rank (95%) | Model | Score | 95% interval | Resolved | Per solve | Median net units | Median churn | Churn vs reference |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1–2 | Claude Fable 5 (xhigh) | 53.2 | 40.9–65.0 | 74.3% | 76.0 | +1430 | 1445 | 0.86× |
| 2–4 | Kimi K3 (max) | 42.0–43.0 | 32.6–52.1 | 67.6% | 67.4 | +1475 | 1516.5 | 0.85× |
| 2–5 | Claude Opus 4.8 (max) | 41.9–42.8 | 31.0–54.4 | 63.2% | 73.2 | +1504.5 | 1504.5 | 0.89× |
| 2–9 | Claude Sonnet 5 (max) | 38.3 | 25.9–50.1 | 59.6% | 72.2 | +1633 | 1648 | 0.93× |
| 3–10 | GPT-5.6 Sol (max) | 32.3–34.2 | 21.6–44.3 | 74.3% | 48.2 | +1833 | 1857 | 1.03× |
| 5–14 | Grok 4.6 (medium) | 28.3 | 19.5–36.9 | 67.6% | 48.2 | +1698 | 1706.5 | 1.06× |
| 5–15 | GLM-5.3 Flash (max) | 25.9–27.9 | 18.0–36.0 | 69.9% | 42.4 | +1839 | 1981 | 1.07× |
| 5–15 | Qwen3.8 Max (xhigh) | 26.9 | 17.9–36.1 | 55.1% | 56.9 | +1564 | 1624 | 0.91× |
| 5–15 | GPT-5.6 Terra (max) | 26.5 | 17.6–35.9 | 68.4% | 45.0 | +1894 | 1921 | 1.11× |
| 6–16 | Grok 4.5 (high) | 25.4 | 17.0–34.2 | 58.8% | 50.7 | +1726.5 | 1726.5 | 1.04× |
| 5–20 | GLM-5.2 (max) | 22.0–23.9 | 12.5–34.3 | 41.9% | 71.2 | +1508 | 1515 | 1.02× |
| 6–19 | GPT-5.5 (xhigh) | 22.6 | 13.6–32.0 | 66.9% | 41.1 | +1935 | 1987 | 1.05× |
| 6–19 | DeepSeek V4 Flash (max) | 22.3 | 13.5–31.3 | 48.5% | 59.8 | +1671.5 | 1689.5 | 0.91× |
| 6–19 | Gemini 3.7 Flash (medium) | 22.2 | 12.7–32.0 | 60.3% | 45.2 | +1878 | 1928.5 | 0.99× |
| 6–19 | GLM-5.3 (max) | 21.5–22.4 | 14.8–29.9 | 66.2% | 39.1 | +1774.5 | 1837.5 | 1.09× |
| 8–20 | Claude Opus 5 (max) | 19.8–21.7 | 12.3–30.2 | 74.3% | 31.8 | +1907 | 1975 | 1.18× |
| 10–20 | DeepSeek V4 Pro (max) | 19.8 | 12.4–27.2 | 59.6% | 43.1 | +1862 | 1884 | 1.03× |
| 12–21 | GPT-5.6 Luna (max) | 17.4 | 10.0–25.8 | 65.4% | 34.5 | +2205 | 2245 | 1.17× |
| 12–23 | Gemini 3.6 Flash (high) | 15.1–15.3 | 5.3–25.2 | 41.9% | 56.2 | +1623 | 1671 | 1.00× |
| 13–25 | Gemini 3.5 Flash (high) | 12.4–12.6 | 3.0–23.3 | 29.4% | 72.7 | +1543 | 1543 | 0.93× |
| 18–25 | GPT-5.4 (xhigh) | 9.6 | 2.9–17.3 | 46.3% | 37.6 | +1774 | 1839 | 1.11× |
| 17–25 | Claude Sonnet 4.6 (high) | 9.6 | 1.7–17.9 | 29.4% | 64.1 | +1428 | 1428 | 0.85× |
| 20–25 | Kimi K2.7 Code | 7.1 | 1.0–13.8 | 24.3% | 63.5 | +1617 | 1639 | 0.92× |
| 21–25 | Muse Spark 1.1 (xhigh) | 4.7 | −0.8–10.3 | 52.9% | 21.7 | +2431 | 2458.5 | 1.35× |
| 21–26 | Muse Spark 1.2 (xhigh) | 4.2 | −1.6–10.1 | 50.7% | 22.2 | +2508 | 2582 | 1.33× |
| 24–26 | Gemini 3.1 Pro Preview (high) | −0.8–−0.6 | −6.1–6.0 | 8.1% | 93.5 | +1407 | 1415 | 0.79× |

- **Footprint matters more here than on SWE-bench Verified.** Per-solve scores range from 22 to 94 (on Verified, 38 to 62), so the ranking is not the resolve rate: Claude Opus 5 and GPT-5.6 Sol solve as many runs as Claude Fable 5 (74%) but write much larger patches (per solve 32 and 48 against 76), and rank far lower.
- **Uncertainty is wide.** With 33 tasks, only Claude Fable 5 is clearly ahead; see the [stability report](sensitivity.md).
- **Churn vs reference** is the median ratio of a model's churn to the reference solution's on its solved runs: below 1× means smaller than DeepSWE's own solution.

## Coverage

| Model | Config | Resolved | Failed measured | Not measured | Approximate |
|---|---|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | `claude_fable_5_xhigh` | 101 | 35 | 0 | 120 |
| Kimi K3 (max) | `kimi_k3_max` | 92 | 43 | 1 | 122 |
| Claude Opus 4.8 (max) | `claude_opus_4_8_max` | 86 | 49 | 1 | 125 |
| Claude Sonnet 5 (max) | `claude_sonnet_5_max` | 81 | 55 | 0 | 125 |
| GPT-5.6 Sol (max) | `gpt_5_6_sol_max` | 101 | 33 | 2 | 122 |
| Grok 4.6 (medium) | `grok_4_6_medium` | 92 | 44 | 0 | 127 |
| GLM-5.3 Flash (max) | `glm_5_3_flash_max` | 95 | 38 | 3 | 124 |
| Qwen3.8 Max (xhigh) | `qwen3_8_max_xhigh` | 75 | 61 | 0 | 128 |
| GPT-5.6 Terra (max) | `gpt_5_6_terra_max` | 93 | 43 | 0 | 124 |
| Grok 4.5 (high) | `grok_4_5_high` | 80 | 56 | 0 | 124 |
| GLM-5.2 (max) | `glm_5_2_max` | 57 | 77 | 2 | 118 |
| GPT-5.5 (xhigh) | `gpt_5_5_xhigh` | 91 | 45 | 0 | 127 |
| DeepSeek V4 Flash (max) | `deepseek_v4_flash_max` | 66 | 70 | 0 | 127 |
| Gemini 3.7 Flash (medium) | `gemini_3_7_flash_medium` | 82 | 54 | 0 | 125 |
| GLM-5.3 (max) | `glm_5_3_max` | 90 | 45 | 1 | 126 |
| Claude Opus 5 (max) | `claude_opus_5_max` | 101 | 33 | 2 | 126 |
| DeepSeek V4 Pro (max) | `deepseek_v4_pro_max` | 81 | 55 | 0 | 128 |
| GPT-5.6 Luna (max) | `gpt_5_6_luna_max` | 89 | 47 | 0 | 125 |
| Gemini 3.6 Flash (high) | `gemini_3_6_flash_high` | 57 | 78 | 1 | 124 |
| Gemini 3.5 Flash (high) | `gemini_3_5_flash_high` | 40 | 95 | 1 | 122 |
| GPT-5.4 (xhigh) | `gpt_5_4_xhigh` | 63 | 73 | 0 | 124 |
| Claude Sonnet 4.6 (high) | `claude_sonnet_4_6_high` | 40 | 96 | 0 | 127 |
| Kimi K2.7 Code | `kimi_k2_7_code_default` | 33 | 103 | 0 | 128 |
| Muse Spark 1.1 (xhigh) | `muse_spark_1_1_xhigh` | 72 | 64 | 0 | 127 |
| Muse Spark 1.2 (xhigh) | `muse_spark_1_2_xhigh` | 69 | 67 | 0 | 127 |
| Gemini 3.1 Pro Preview (high) | `gemini_3_1_pro_preview_high` | 11 | 125 | 0 | 118 |

Every solved run was measured. *Not measured* counts runs DeepSWE marks as errored, one failed patch with a rename or binary change the analyzer does not support, and two unpublished patches; their items get a score range.

**Approximate alignment:** these are long-horizon tasks (median churn around 1,500 to 2,500 units), so most patches exceed the exact diff's 500-edit limit and use the analyzer's flagged line-anchored approximation. Unit totals of new code are unaffected; for rewrites of existing code, added and deleted counts are approximate.

## Limits

Everything in the [main README](../../README.md#limits-and-interpretation) applies. 33 tasks is small; tasks are long features rather than bug fixes; only Python is measured (79 of DeepSWE's 113 tasks are TypeScript, Go, JavaScript or Rust); scores are relative to these 26 models; and correctness is taken from DeepSWE's published results.

## DeepSWE release 1.0 runs (added 2026-10-21)

12 more configurations come from DeepSWE's own archive of **release 1.0** (gated Hugging Face dataset [`datacurve/deep-swe-leaderboard` at `0618ccd`](https://huggingface.co/datasets/datacurve/deep-swe-leaderboard/tree/0618ccdd613e1f0043604f8f4474321e7fe12e29), CC-BY-4.0; access asks you to share your Hugging Face username and email), for models absent from v1.1: Claude Haiku 4.5, Claude Opus 4.6 (max), Claude Opus 4.7 (max), Gemini 3 Flash Preview, GLM-5.1, GPT-5.4 mini (xhigh), Grok Build 0.1, Kimi K2.6, MiMo V2.5 Pro, MiniMax M2.7, MiniMax M3 and Qwen3.6 Plus. Files `v1_0_*.jsonl`; names end in "· DeepSWE 1.0".

- Same 113 task IDs and base commits as v1.1, and the same mini-SWE-agent harness. v1.1 re-ran every model and rewrote every verifier. On the nine setups present in both releases, pass rates agree within a few points, and per-task differences match chance except on four tasks (`narwhals-rolling-window-suite`, `vulture-persistent-analysis-cache`, `skrub-duration-encoding`, `claude-code-by-agents-recursive-delegation`). Release 1.0 outcomes on those four tasks are recorded as unknown, never as pass or fail.
- Measured at this board's analyzer commit with Python 3.14.7, so units are comparable; the frozen panel is unchanged and the new runs are scored against it. Coverage, scores and stability were regenerated with the current scoring code (existing models' archived scores differ only in the last floating-point digit).
- Driver: [`examples/benchmark-discovery/add-deepswe-1.0.py`](../benchmark-discovery/add-deepswe-1.0.py).
- A model is ranked only with at least 15 shared solved tasks (or half the board's tasks if fewer); otherwise it is listed after the ranked models.
