# Ten models × 500 Verified tasks (analyzer 0.5.0)

**Beta research preview, not an official ranking.** Every SWE-bench Verified task for the ten mini-SWE-agent v2.0.0 submissions of 2026-02-17, measured in coding units, including explicitly failed patches. This replaces the [10-task demo](../ten-model-report.md) as the main result: it includes failures and has uncertainty over hundreds of tasks. It is rendered as the [site](../../site/index.html) with `python -m parsimony.site`.

## Pinned inputs

- Analyzer commit `b2316a9`, version `0.5.0-beta`, Python 3.14.7. Measurement code is identical to `54bd8a6` (v5 audit); the commit adds only the site builder. Opus and Sonnet records were re-measured with it and match v5 in every field except analyzer identity.
- Scoring `parsimony-80-20-v0.5` (80% net units / 20% churn), panel `ten-model-439-solved-80-20-v0.5`.
- Dataset SHA256 `82029e78b26e1da0ddc01653c98db18443fab1993e28dff052a38b01c3fd77f7`, experiments revision `40f164d5b8f1d249bf95a6df8b74b577fd8e519d` (both as in v5).
- SHA256: [population.json](population.json) `a19f7243…`, [score-panel.json](score-panel.json) `843f0d25…`, [scores.json](scores.json) `e493ec69…`, [coverage.json](coverage.json) `0b60e075…`.

```sh
for m in claude-4-6-opus claude-4-5-sonnet-high claude-4-5-haiku-high deepseek-3-2-high gemini-3-flash-high \
         glm-5-high gpt-5-2-high gpt-5-mini kimi-k2-5-high minimax-2-5-high; do
  python -m parsimony analyze 20260217_mini-v2.0.0_$m --dataset verified.jsonl \
    --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d --include-failed --output $m.jsonl
done
python -m parsimony.scoring score examples/ten-model-500/score-panel.json *.jsonl --output scores.json
python -m parsimony.site examples/ten-model-500/score-panel.json *.jsonl --output site/index.html
```

## Scored population

- **439 tasks** that at least one of the ten models solved. The 61 tasks nobody solved have no successful reference patch and cannot calibrate footprint. Choosing tasks by panel success is a known bias: an official release needs a population chosen independently of the candidates.
- **Reference panel:** all 4,390 records on those tasks; every successful patch is a reference for its task. Identical patches from different models are not deduplicated.
- 211 tasks were solved by all ten models.

## Coverage

| Model | Resolved | Failed measured | Errors | Units unknown | Approximate |
|---|---:|---:|---:|---:|---:|
| Claude Opus 4.6 | 378 | 121 | 1 | 0 | 2 |
| Claude Sonnet 4.5 (high) | 357 | 141 | 2 | 0 | 3 |
| Claude Haiku 4.5 (high) | 333 | 167 | 0 | 0 | 3 |
| DeepSeek V3.2 (high) | 350 | 149 | 1 | 2 | 2 |
| Gemini 3 Flash (high) | 379 | 121 | 0 | 0 | 2 |
| GLM-5 (high) | 364 | 135 | 1 | 0 | 3 |
| GPT-5.2 (high) | 364 | 136 | 0 | 0 | 12 |
| GPT-5 mini | 281 | 209 | 10 | 1 | 2 |
| Kimi K2.5 (high) | 354 | 146 | 0 | 1 | 2 |
| MiniMax M2.5 (high) | 379 | 117 | 4 | 0 | 5 |

Every successful patch was measured. All 19 errors and 4 unknown-unit records are **failed** patches: 12 whose context does not match the base commit, 3 rename-only or binary diffs, 1 malformed hunk, and 7 that leave Python unparseable. Following the scoring spec, those tasks get a range instead of a point, so five models have a score range rather than a single score (about 0.6 points wide at most).

## Results

| Model | Score | 95% interval | Resolved | Per solve | Median net units | Median churn |
|---|---:|---|---:|---:|---:|---:|
| Claude Opus 4.6 | 49.1 | 46.0–51.7 | 75.6% | 58.3 | +8 | 12 |
| MiniMax M2.5 (high) | 47.8–48.0 | 45.6–50.9 | 75.8% | 56.8 | +8 | 12 |
| Kimi K2.5 (high) | 44.4–44.5 | 41.9–47.9 | 70.8% | 57.3 | +7 | 11 |
| Gemini 3 Flash (high) | 44.1 | 41.2–46.7 | 75.8% | 52.8 | +10 | 14 |
| GLM-5 (high) | 42.4 | 39.9–45.5 | 72.8% | 53.0 | +9 | 13 |
| Claude Sonnet 4.5 (high) | 39.2–39.3 | 37.1–42.8 | 71.4% | 50.8 | +9 | 14 |
| Claude Haiku 4.5 (high) | 35.4 | 33.0–39.0 | 66.6% | 50.4 | +8 | 13 |
| DeepSeek V3.2 (high) | 30.0–30.2 | 27.8–33.8 | 70.0% | 41.0 | +12.5 | 18 |
| GPT-5.2 (high) | 28.7 | 26.3–31.8 | 72.8% | 37.4 | +15.5 | 24 |
| GPT-5 mini | 25.2–25.8 | 23.7–30.0 | 56.2% | 45.1 | +9 | 13 |

- **The score is mostly correctness.** A solved task scores 1–100 and a failure −25–0, so resolve rate dominates. *Per solve* (mean score over a model's solved tasks, 50.5 typical) isolates footprint.
- **Footprint separates models clearly at the extremes.** Opus, Kimi and MiniMax write the smallest successful patches (per solve 57–58). GPT-5.2 and DeepSeek write the largest (37–41), with median churn roughly double.
- **Intervals** come from 2,000 paired resamples of the 421 tasks where every model has a point score. Opus is first in 66% of resamples and MiniMax in 34%; no other model tops any meaningful share.
- Gemini 3 Flash solves as many tasks as MiniMax but ranks fourth, because its successful patches are larger.

## Limits

Everything in the [main README](../../README.md#limits-and-interpretation) applies. Units measure size and nesting, not readability; scores are relative to these ten models; all ten use one harness; and correctness is taken from published results.
