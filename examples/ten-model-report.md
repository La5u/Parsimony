# 10 models × 10 shared tasks

All 10 submissions use **mini-SWE-agent v2.0.0**, dated 2026-02-17. This is a small matched-task sample, not an overall model ranking. No agent code or tests were executed.

There were **211 tasks resolved by all 10 submissions**. We shuffled the sorted intersection with `random.Random(42)` and selected the first ten tasks from distinct repositories. This extends the original three-task cohort without removing or replacing tasks based on metrics:

- `astropy__astropy-7671`
- `django__django-13109`
- `matplotlib__matplotlib-13989`
- `pallets__flask-5014`
- `pydata__xarray-4966`
- `pylint-dev__pylint-6903`
- `pytest-dev__pytest-8399`
- `scikit-learn__scikit-learn-9288`
- `sphinx-doc__sphinx-8721`
- `sympy__sympy-19346`

All **100 model-patch analyses and 100 corresponding human-reference analyses succeeded**, using complete before/after files. Published resolve rates below cover all 500 Verified tasks, not this selected sample. Models with `high` in their submission identifier use the published high-reasoning configuration; Opus 4.6 and GPT-5 mini do not have that suffix.

## Sample ranking

Lower median net normalized-token delta ranks first. Churn is added plus deleted tokens, reported separately; a smaller net delta does not necessarily mean less editing.

| Rank | Model | Median net tokens | Median churn | Published resolve rate |
|---|---|---:|---:|---:|
| 1 | Claude Opus 4.6 | +2 | 8.5 | 75.6% |
| 2 | MiniMax M2.5 (high) | +5.5 | 10.5 | 75.8% |
| 3 | Claude Sonnet 4.5 (high) | +6 | 9 | 71.4% |
| 4 | Kimi K2.5 (high) | +7.5 | 8.5 | 70.8% |
| 5 | Claude Haiku 4.5 (high) | +9 | 9 | 66.6% |
| 6 | Gemini 3 Flash (high) | +9.5 | 27.5 | 75.8% |
| 7 | GLM-5 (high) | +13.5 | 15.5 | 72.8% |
| 8 | GPT-5 mini | +14 | 17 | 56.2% |
| 9 | GPT-5.2 (high) | +18 | 26 | 72.8% |
| 10 | DeepSeek V3.2 (high) | +22.5 | 37 | 70.0% |

## Experimental 70/30 equal-task score

The same cached measurements also have a frozen-panel score: **70% net-token percentile + 30% churn percentile per task**, mapped into the positive success band, then averaged equally across the ten tasks. Higher is better. This is not the median-net ranking above.

| Rank | Model | Parsimony Score |
|---|---|---:|
| 1 | Kimi K2.5 (high) | 64.90 |
| 2 | Claude Opus 4.6 | 62.48 |
| 3 | GLM-5 (high) | 61.54 |
| 4 | Claude Haiku 4.5 (high) | 57.88 |
| 5 | Claude Sonnet 4.5 (high) | 56.98 |
| 6 | MiniMax M2.5 (high) | 50.15 |
| 7 | GPT-5 mini | 42.73 |
| 8 | Gemini 3 Flash (high) | 41.99 |
| 9 | GPT-5.2 (high) | 33.67 |
| 10 | DeepSeek V3.2 (high) | 32.68 |

All ten models solved all ten selected tasks, so failure penalties are zero **in this selected cohort**. The ten submissions themselves form the frozen reference panel, with self-comparisons counted as ties. Their average score is 50.5 by construction; these are reference-relative scores, not percentages correct.

The ranking change reflects **both** adding churn and replacing a median raw-token summary with an equal-task mean of normalized percentiles. Do not attribute it solely to the 30% churn weight. The sample is still too small for robust model-superiority claims.

See `ten-model-score-panel.json`, `ten-model-scores.json`, and [the scoring specification](../docs/scoring.md). No patch reanalysis was needed.

## Interpretation and limitations

These are ten tasks from ten repositories, selected from the shared-solved intersection. That intersection favors easier tasks, and the one-task-per-repository sampling is not representative of SWE-bench's repository distribution. Ten tasks remain too few for a strong general claim; rankings changed substantially from the three-task sample.

Human reference churn is zero after normalization for the Django and pytest tasks. Their model/human ratios are null, not zero, so each model's median human ratio covers **eight tasks**, although all ten reference patches were analyzed successfully. In particular, the Django fix changes `_default_manager` to `_base_manager`: a real semantic fix that identifier normalization intentionally treats as unchanged footprint.

Full per-task token, AST and complexity deltas are retained in JSONL. Medians can conceal variation between individual patches. Parsimony measures footprint, not semantic correctness beyond published evaluation or all technical debt.

## Reproduce and inspect

```sh
python -m parsimony dataset --output verified.jsonl
python -m examples.run_ten_models --dataset verified.jsonl
python -m parsimony leaderboard examples/ten-model-results.jsonl --shared
```

- `ten-model-plan.json`: full submission identifiers, selected tasks, selection rule, pinned experiments commit and dataset checksum.
- `ten-model-results.jsonl`: 100 selected records with metrics, reference metrics and patch/result provenance.
- `ten-model-leaderboard.json`: shared-task medians including AST/complexity and human ratios.
- `three-task-sample/`: the original three-task plan, results and leaderboard, preserved for comparison.
- `.parsimony-cache/ten-model-all-results.jsonl`: all 5,000 records, including unresolved and unselected tasks (local, not committed).
- `.parsimony-cache/ten-model-progress/`: per-submission records saved as each analysis completes. The runner uses separate processes for CPU-heavy static token alignment; it never executes submitted code.
- Public artifact bytes and original source files remain in the local URL cache. S3 patch content is identified by SHA256 in each record.
