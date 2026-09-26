# Ten models × 500 Verified tasks, plus Claude Opus 4.5 (analyzer 0.5.0)

**Beta research preview, not an official ranking.** Every SWE-bench Verified task for the ten mini-SWE-agent v2.0.0 submissions of 2026-02-17, measured in coding units, including explicitly failed patches. This replaces the [10-task demo](../ten-model-report.md) as the main result: it includes failures and has uncertainty over hundreds of tasks. It is rendered as the [site](../../site/index.html) with `python -m parsimony.site`. Claude Opus 4.5 (high), from the same run, was added later and is scored against the ten-model panel without becoming a reference (see [Newcomers](#newcomers)).

## Pinned inputs

- Analyzer commit `b2316a9`, version `0.5.0-beta`, Python 3.14.7. Measurement code is identical to `54bd8a6` (v5 audit); the commit adds only the site builder. Opus and Sonnet records were re-measured with it and match v5 in every field except analyzer identity.
- Scoring `parsimony-80-20-v0.5` (80% net units / 20% churn), panel `ten-model-439-solved-80-20-v0.5`.
- Dataset SHA256 `82029e78b26e1da0ddc01653c98db18443fab1993e28dff052a38b01c3fd77f7`, experiments revision `40f164d5b8f1d249bf95a6df8b74b577fd8e519d` (both as in v5).
- SHA256: [population.json](population.json) `a19f7243…`, [score-panel.json](score-panel.json) `843f0d25…`, [scores.json](scores.json) `53680960…`, [coverage.json](coverage.json) `e0075f83…` (both including Claude Opus 4.5).

```sh
for m in claude-4-6-opus claude-4-5-sonnet-high claude-4-5-haiku-high deepseek-3-2-high gemini-3-flash-high \
         glm-5-high gpt-5-2-high gpt-5-mini kimi-k2-5-high minimax-2-5-high; do
  python -m parsimony analyze 20260217_mini-v2.0.0_$m --dataset verified.jsonl \
    --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d --include-failed --output $m.jsonl
done
# Newcomer, measured later from a worktree at the same analyzer commit (git worktree add ../p050 b2316a9):
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-5-opus-high --dataset verified.jsonl \
  --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d --include-failed --output claude-4-5-opus-high.jsonl
python -m parsimony.scoring score examples/ten-model-500/score-panel.json *.jsonl --output scores.json
python -m parsimony.stability examples/ten-model-500/score-panel.json *.jsonl --output sensitivity.json
python -m parsimony.site examples/ten-model-500/score-panel.json *.jsonl --sensitivity sensitivity.json \
  --output site/index.html
```

## Newcomers

Claude Opus 4.5 (high) is scored against the frozen ten-model panel and is **not a reference**: the population, the panel and the ten original scores are unchanged, and the stability analysis leaves out only the ten panel models' references. **Newcomers get no credit for the 61 tasks none of the original ten solved**; those tasks have no reference patch and stay outside the population even when a newcomer solves them. Opus 4.5 solves 2 of them (`astropy__astropy-13033`, `django__django-12406`), which earn it nothing.

Two other v2.0.0 Verified runs published at the pinned revision are left out because their published results cannot be used: GPT-5.2 Codex has no `per_instance_details.json`, and Gemini 3 Pro (high)'s marks all 500 tasks unresolved, although its `metadata.yaml` reports 69.6% resolved and its per-task `report.json` files show resolved tasks. Gemini 3.5 Flash is published with mini-SWE-agent v2.4.2, so it is left out to keep one harness.

## Scored population

- **439 tasks** that at least one of the ten models solved. The 61 tasks none of the ten solved have no successful reference patch and cannot calibrate footprint. Choosing tasks by panel success is a known bias: an official release needs a population chosen independently of the candidates.
- **Reference panel:** all 4,390 records on those tasks; every successful patch is a reference for its task. Identical patches from different models are not deduplicated.
- 211 tasks were solved by all ten models.

## Coverage

| Model | Resolved | Failed measured | Errors | Units unknown | Approximate |
|---|---:|---:|---:|---:|---:|
| Claude Opus 4.5 (high) | 384 | 115 | 1 | 0 | 2 |
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

Every successful patch was measured. All 20 errors and 4 unknown-unit records are **failed** patches: 13 whose context does not match the base commit, 3 rename-only or binary diffs, 1 malformed hunk, and 7 that leave Python unparseable. Following the scoring spec, those tasks get a range instead of a point, so six models have a score range rather than a single score (about 0.6 points wide at most).

## Results

| Model | Score | 95% interval | Resolved | Per solve | Median net units | Median churn |
|---|---:|---|---:|---:|---:|---:|
| Claude Opus 4.5 (high) | ≈52.3 | 50.0–55.8 | 76.8% | 61.4 | +6.5 | 11 |
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
- **Footprint separates models clearly at the extremes.** Opus 4.5 writes the smallest successful patches (per solve 61.4), followed by Opus 4.6, Kimi and MiniMax (57–58). GPT-5.2 and DeepSeek write the largest (37–41), with median churn roughly double.
- **Intervals** come from 2,000 paired resamples of the 421 tasks where every model has a point score. Opus 4.5 is first in 99% of resamples and Opus 4.6 in 1%. Without Opus 4.5, Opus 4.6 was first in 66% and MiniMax in 34%.
- Gemini 3 Flash solves as many tasks as MiniMax but ranks fourth, because its successful patches are larger.

## Limits

Everything in the [main README](../../README.md#limits-and-interpretation) applies. Units measure size and nesting, not readability; scores are relative to the ten panel models; all eleven use one harness; and correctness is taken from published results.
