# 10 models × 10 shared tasks

> **Regenerated with analyzer 0.4.0-beta** (commit `c5a2ee8`, Python 3.14.7). Same plan, tasks, pinned experiments commit and dataset checksum as the original 0.1.0 run, which is kept in git history (commit `51857a0`). The 70/30 score ranking is unchanged, and every score moved by less than one point. In the median-net table, Claude Sonnet 4.5 and MiniMax M2.5 swapped ranks 2 and 3. This is still a pipeline demo, not a model ranking.

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
| 1 | Claude Opus 4.6 | +2 | 12.5 | 75.6% |
| 2 | Claude Sonnet 4.5 (high) | +6 | 12.5 | 71.4% |
| 3 | MiniMax M2.5 (high) | +6.5 | 13 | 75.8% |
| 4 | Kimi K2.5 (high) | +8.5 | 11.5 | 70.8% |
| 5 | Claude Haiku 4.5 (high) | +10 | 11.5 | 66.6% |
| 6 | Gemini 3 Flash (high) | +10.5 | 29 | 75.8% |
| 7 | GLM-5 (high) | +14.5 | 17.5 | 72.8% |
| 8 | GPT-5 mini | +14.5 | 19.5 | 56.2% |
| 9 | GPT-5.2 (high) | +21 | 29 | 72.8% |
| 10 | DeepSeek V3.2 (high) | +27.5 | 43 | 70.0% |

## Experimental 70/30 equal-task score

The same cached measurements also have a frozen-panel score: **70% net-token percentile + 30% churn percentile per task**, mapped into the positive success band, then averaged equally across the ten tasks. Higher is better. This is not the median-net ranking above.

| Rank | Model | Parsimony Score |
|---|---|---:|
| 1 | Kimi K2.5 (high) | 64.16 |
| 2 | Claude Opus 4.6 | 62.63 |
| 3 | GLM-5 (high) | 61.84 |
| 4 | Claude Haiku 4.5 (high) | 58.17 |
| 5 | Claude Sonnet 4.5 (high) | 56.84 |
| 6 | MiniMax M2.5 (high) | 50.30 |
| 7 | GPT-5 mini | 43.03 |
| 8 | Gemini 3 Flash (high) | 41.39 |
| 9 | GPT-5.2 (high) | 33.82 |
| 10 | DeepSeek V3.2 (high) | 32.83 |

All ten models solved all ten selected tasks, so failure penalties are zero **in this selected cohort**. The ten submissions themselves form the frozen reference panel, with self-comparisons counted as ties. Their average score is 50.5 by construction; these are reference-relative scores, not percentages correct.

The ranking change reflects **both** adding churn and replacing a median raw-token summary with an equal-task mean of normalized percentiles. Do not attribute it solely to the 30% churn weight. The sample is still too small for robust model-superiority claims.

Paired-task bootstrap 95% intervals (`python -m parsimony.sensitivity`) span roughly 20 points per model and overlap across the top six. No model is the top scorer in more than 37% of resamples, and the `net_floor=0` anti-deletion variant changes no rank.

See `ten-model-score-panel.json`, `ten-model-scores.json`, and [the scoring specification](../docs/scoring.md).

## Interpretation and limitations

These are ten tasks from ten repositories, selected from the shared-solved intersection. That intersection favors easier tasks, and the one-task-per-repository sampling is not representative of SWE-bench's repository distribution. Ten tasks remain too few for a strong general claim; rankings changed substantially from the three-task sample.

Under 0.1.0, the Django and pytest human patches measured zero churn, because identifier and literal edits were normalized away. For example, the Django fix changes `_default_manager` to `_base_manager`. Since 0.4.0 these real semantic edits count (Django churn 2, pytest 10), so model/human ratios now cover all ten tasks.

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
