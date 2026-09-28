# DeepSWE: 26 current models × 34 Python tasks × 4 attempts (analyzer 0.5.2)

**Beta research preview, not an official ranking.** [DeepSWE](https://deepswe.datacurve.ai) ([paper](https://arxiv.org/abs/2607.07946), [tasks](https://github.com/datacurve-ai/deep-swe)) is a 2026 benchmark of original, long-horizon tasks from active open-source repositories. Every model runs with mini-SWE-agent, four attempts per task, and DeepSWE publishes each run's final patch and pass/fail. This folder measures the Python tasks; it is the [site](../../site/index.html)'s main board. The [33-model SWE-bench Verified results](../mini-swe-agent-500/README.md) are the second board.

## Pinned inputs

- Analyzer `0.5.2-beta`, commit `1b50e56`, Python 3.14.7.
- DeepSWE tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea` (34 Python tasks). Runs: release `v1.1`, run index `trials.json` SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6` (runs from June to September 2026).
- Dataset (items with reference solutions) SHA256 `41a44998c70248e0a3e2a4cf43a8838b70248537d1f3a458838f2f7e09ecef8a`. Scoring `parsimony-80-20-v0.5`, panel `deepswe-v1.1-python-26-pooled-80-20-v0.5`.
- SHA256: [population.json](population.json) `c16b15f8…`, [score-panel.json](score-panel.json) `c280b21b…`, [scores.json](scores.json) `f3879074…`, [coverage.json](coverage.json) `fbda1b7a…`, [sensitivity.json](sensitivity.json) `940a896e…`.

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
python -m parsimony.site score-panel.json *.jsonl --sensitivity sensitivity.json --benchmark deepswe --output site/index.html
```

## How DeepSWE is scored

- **One configuration per model:** each model's best-scoring configuration (reasoning effort) on DeepSWE's live leaderboard whose patches can be downloaded. GPT-6 Astra and Gemini 3.8 Flash are left out: their patches are not published.
- **Each attempt is an item.** A model has four items per task (`task#1` … `task#4`), 136 in all. Each item is scored against every passing patch of its task, from any model and attempt, and the four attempts of a task are resampled together for intervals and rank ranges.
- **33 tasks are scored:** no model solved `koota-entity-snapshot-rollback`, so it cannot calibrate footprint.
- **Reference solution:** DeepSWE's own solution for each task plays the role of the maintainers' fix (the *Churn vs reference* column). A few solutions lost the leading space of blank context lines; the dataset builder restores it.

## Results

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
