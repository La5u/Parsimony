# 10 models × 10 shared tasks

> **Regenerated with analyzer 0.5.0-beta** (commit `54bd8a6`, Python 3.14.7), which measures **coding units** (AST elements) instead of lexical tokens. Same plan, tasks, pinned experiments commit and dataset checksum as the original 0.1.0 run; the 0.4.0 version is in git history (commit `f621010`). This is still a pipeline demo, not a model ranking.

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

Lower median net coding-unit delta ranks first. Churn is units added plus deleted, reported separately; a smaller net delta does not necessarily mean less editing. Token medians (the pre-0.5 metric) are shown for comparison.

| Rank | Model | Median net units | Median unit churn | Median net tokens | Median token churn | Published resolve rate |
|---|---|---:|---:|---:|---:|---:|
| 1 | Claude Opus 4.6 | +2 | 10 | +2 | 12.5 | 75.6% |
| 2 | MiniMax M2.5 (high) | +4 | 10 | +6.5 | 13 | 75.8% |
| 3 | Claude Sonnet 4.5 (high) | +4.5 | 10 | +6 | 12.5 | 71.4% |
| 4 | Kimi K2.5 (high) | +6.5 | 11 | +8.5 | 11.5 | 70.8% |
| 5 | Gemini 3 Flash (high) | +7 | 20 | +10.5 | 29 | 75.8% |
| 6 | Claude Haiku 4.5 (high) | +7.5 | 10 | +10 | 11.5 | 66.6% |
| 7 | GLM-5 (high) | +9.5 | 11 | +14.5 | 17.5 | 72.8% |
| 8 | GPT-5 mini | +9.5 | 13.5 | +14.5 | 19.5 | 56.2% |
| 9 | GPT-5.2 (high) | +15.5 | 19.5 | +21 | 29 | 72.8% |
| 10 | DeepSeek V3.2 (high) | +20.5 | 29 | +27.5 | 43 | 70.0% |

## Experimental 80/20 equal-task score

The same cached measurements also have a frozen-panel score: **80% net-unit percentile + 20% churn percentile per task** (scoring `parsimony-80-20-v0.5`), mapped into the positive success band, then averaged equally across the ten tasks. Higher is better. This is not the median-net ranking above.

| Rank | Model | Parsimony Score |
|---|---|---:|
| 1 | Kimi K2.5 (high) | 62.88 |
| 2 | GLM-5 (high) | 62.18 |
| 3 | Claude Opus 4.6 | 60.50 |
| 4 | Claude Sonnet 4.5 (high) | 56.44 |
| 5 | Claude Haiku 4.5 (high) | 54.76 |
| 6 | MiniMax M2.5 (high) | 52.58 |
| 7 | GPT-5 mini | 44.36 |
| 8 | Gemini 3 Flash (high) | 43.77 |
| 9 | GPT-5.2 (high) | 34.26 |
| 10 | DeepSeek V3.2 (high) | 33.27 |

All ten models solved all ten selected tasks, so failure penalties are zero **in this selected cohort**. The ten submissions themselves form the frozen reference panel, with self-comparisons counted as ties. Their average score is 50.5 by construction; these are reference-relative scores, not percentages correct.

The ranking change reflects **both** adding churn and replacing a median raw-token summary with an equal-task mean of normalized percentiles. Do not attribute it solely to the 20% churn weight. The sample is still too small for robust model-superiority claims.

Moving from the 70/30 weights (`parsimony-70-30-v0.4`) to 80/20 changes no rank; the gap between Kimi and GLM-5 widens from 0.54 to 0.70 points. Compared with the 70/30 scores under the 0.4.0 token analyzer, GLM-5 and Opus swapped second and third, Sonnet and Haiku swapped fourth and fifth, and Kimi and the bottom five kept their ranks. Paired-task bootstrap 95% intervals (`python -m parsimony.sensitivity`) span roughly 16 to 28 points per model and overlap across the top six. No model is the top scorer in more than 31% of resamples, and the `net_floor=0` anti-deletion variant changes no rank.

See `ten-model-score-panel.json`, `ten-model-scores.json`, and [the scoring specification](../docs/scoring.md).

## Interpretation and limitations

These are ten tasks from ten repositories, selected from the shared-solved intersection. That intersection favors easier tasks, and the one-task-per-repository sampling is not representative of SWE-bench's repository distribution. Ten tasks remain too few for a strong general claim; rankings changed substantially from the three-task sample.

Under 0.1.0, the Django and pytest human patches measured zero churn, because identifier and literal edits were normalized away. For example, the Django fix changes `_default_manager` to `_base_manager`. Since 0.4.0 these real semantic edits count (Django churn 2 units, pytest 10), so model/human ratios now cover all ten tasks.

Full per-task unit, token, AST and complexity deltas are retained in JSONL. Medians can conceal variation between individual patches. Parsimony measures footprint, not semantic correctness beyond published evaluation or all technical debt.

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
