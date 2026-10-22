# Method and command-line reference

How Parsimony measures a patch, and the commands behind every published number. Start with the [README](../README.md) for the overview.

## How a patch is measured

The parsing and scope details below describe Python. Other language tracks have separate rules; see [language tracks](language-tracks.md).

1. **Correctness gate.** Only attempts listed as resolved in the published results enter the website's solved-footprint comparison. The resolve rate uses the benchmark's full task/attempt population (500 for SWE-bench Verified), not just measured attempts. Parsimony trusts published evaluation and does not revalidate correctness.
2. **Before vs. after.** Each touched implementation file is fetched at the dataset's exact `base_commit`, and the patch is applied in memory with strict position/context validation. Unapplicable patches are recorded as errors, never scored as zero. Network failures are recorded as retryable `fetch_error`.
3. **Coding units.** Each side is parsed with `ast` (docstrings removed) and walked in source order. A unit is one syntactic element: a statement (`if`, `return`, assignment, `def`), an expression (call, attribute access, arithmetic or boolean operation), each comparison, a name or a literal. Each statement block also ends with one `EndBlock` unit, so nesting and moving code into or out of a block count. Punctuation, brackets, commas, load/store markers, comments, formatting and name length are not units: `if x.count(y) > 0: foo(a, b)` is 12 units. Units are unknown (null), never zero, when a file does not parse on both sides (`lexical_files`).
4. **Alignment.** Unit counts come from an exact minimum edit script (Myers diff) over the unit sequence. Rewrites needing more than 500 edits use a line-anchored approximation and are flagged (`approximate_files`).
5. **Footprint.** `net_units = added − deleted`, `churn = added + deleted`. Negative net is genuine shrinking. A renamed name or changed literal is one changed unit; the `structural_churn` diagnostic ignores identifier/literal values. The pre-0.5 metric, normalized lexical tokens (`net_tokens`, `token_churn`), remains a diagnostic. `files_changed` counts implementation files whose normalized code differs.
6. **Scope.** Only `.py` implementation files count. Excluded: test/doc/example/benchmark directories, test filenames, `setup.py`/`conftest.py`, generated files (a header comment in the base commit), protobuf output, migration scripts, vendored and build output. Django's `db/migrations/` and `test/` framework packages count as implementation. Newly added root-level Python files are also excluded as presumed scratch scripts; this heuristic can omit legitimate implementation. Every record lists `touched_files` and `excluded_files`. See `implementation()` and `measure()` in `parsimony/analysis.py` for the exact rules.
7. **Structure (diagnostic).** Full-file AST-node delta and a simple cyclomatic proxy delta (functions/lambdas, branches, loops, handlers, extra boolean operands, comprehension loops/filters, non-default match cases). These are null if either side does not parse.
8. **Human comparison.** The dataset's human `patch` (not `test_patch`) is measured identically. `model_human_ratio` = model churn / human churn, or null when the human churn is zero.

`leaderboard` reports medians (net, churn, human ratio, files, AST and complexity deltas), sample counts and resolve rate, sorted by median net units. `--shared` uses the intersection of resolved **and** analyzable tasks, which avoids task-mix confounding but can favor easy tasks.

## Website ranking: same-task net ratio v1

The website ranking is separate from the CLI median leaderboard above and the archived experimental score below. Its implementation is in `parsimony/site.py` (`solved_by_task`, `same_task_pairs`, `same_task`, and `merged_ratio`).

For each model and base task:

1. Keep only resolved, measured, full-file, in-scope attempts. Average their net units within each model/task; DeepSWE's repeated attempts are pooled here.
2. Keep the task for that model only if at least **3 other ranked models** have eligible measurements on it.
3. Take the mean of those other models' per-task means as the task's comparison footprint. Each peer model has equal weight, regardless of its number of successful attempts.
4. Divide the sum of the model's eligible per-task means by the sum of the corresponding comparison footprints. The ratio is unavailable if there are no eligible tasks or the denominator is nonpositive. Smaller ratios rank first; negative ratios can occur when a model deletes more than it adds.

This is a **ratio of sums**, not a mean of per-task ratios: tasks with larger comparison footprints contribute more. Each model has its own eligible task set and peer mixture. Matching within tasks reduces task-size confounding but does not make the ranking a comparison on a common task population. Results describe footprint conditional on observed successful repairs, not general coding quality or a model's expected footprint on arbitrary tasks. Adding or removing peer models can change ratios and task eligibility.

The website also reports plain means over solved attempts and over all measured attempts; neither is the same-task ranking metric. Missing, unparseable and excluded-only attempts do not count as zero.

### Conditional 95% ranges

With at least **5 eligible base tasks**, each model's range uses 1,000 bootstrap draws of its task-level pairs, with replacement. The comparison footprints are held fixed, and draws with nonpositive comparison totals are discarded. The displayed range is the 2.5th to 97.5th percentile of the remaining ratios. Below 5 tasks no range is given. A range is not a confidence interval for rank or a guarantee that two models differ.

These ranges cover task resampling conditional on the eligible measurements. They do **not** cover missing-measurement bias, peer-panel selection, within-task attempt variability, repository clustering, differing retry policies or incorrect upstream outcomes. Existing `parsimony.stability` reports concern the archived combined score, not this ranking.

### Combined DeepSWE board

The front page averages each model's per-language ratios, weighted by that model's eligible task count in each usable language (positive comparison total). Raw unit counts are never pooled across languages. Ranges resample tasks within each language. Models absent from a language board are shown as partial and not ranked. Because task eligibility differs by model, language weights can differ too.

### Net units vs. the human fix (chart axis, not a rank)

Where the benchmark's human reference fix was measured (all four DeepSWE languages, SWE-bench Verified and the self-runs; not Live, SWEeper or SWE-Milestone), `human_task_net` divides the sum of a model's per-task solved net units by the sum of the human fix's net units on those same tasks (in-scope, full-file human measurements only). Like the same-task ratio it is a ratio of sums, so human fixes with net ≤ 0 (117 of Verified's 500) do not make it undefined; it is unavailable when the human total is nonpositive. Ranges use the same 1,000-draw task bootstrap from 5 tasks. A human fix is one reference, not an optimum, and this ratio never sets rank. The task view also shows the human fix's net units (`task_human`). The combined DeepSWE page averages the per-language human-fix ratios, weighted by each model's shared tasks per language (`merged_ratio`), like its peer ratio; ranges resample tasks within each language.

### Offline ranking diagnostics

[Published diagnostics](../examples/ranking-diagnostics/README.md) cover each language board separately: leave-one-task/repository/peer-out sensitivity, pairwise matched-task means, comparison-denominator concentration and missing-success coverage. These are descriptive checks, not confidence intervals or a new ranking. They do not evaluate the combined-language aggregate.

```sh
scripts/diagnose-rankings.sh /tmp/ranking-diagnostics --offline
# Omit --offline to also download the checksum-bound DeepSWE Go scalars and diagnose that board.
```

JSON reports include exact input hashes, unavailable perturbations and top influences; Markdown summaries show coverage and rank-sensitivity ranges. No target code is fetched or run. Harness/retry differences remain source-reported limitations, not inferred corrections.

## Command line

Python 3.12+, **no runtime dependencies for Python analysis**. Optional tracks: JavaScript/TypeScript use Node.js and the official TypeScript parser (`npm ci` installs the pinned `typescript`), Go uses `pip install '.[languages]'` (the current checksum-pinned grammar builds from source, requiring a C compiler and Python development headers); see [language tracks](language-tracks.md) for pinned parsers, scope and reproducible commands. Analyzer 0.8 introduced a versioned Go grammar/EOF fix and 0.9 rejects malformed hunk headers and duplicate file sections instead of skipping or double-counting them; published historical cohorts keep their recorded analyzer identities. Run from this checkout (`pip install -e .` is optional). Measurements depend on the interpreter's tokenizer, so use one pinned Python version for anything you compare.

```sh
# Metadata, base commits and human patches for all 500 Verified tasks.
python -m parsimony dataset --output verified.jsonl

# Analyze five successful tasks per submission (alphabetical, NOT a representative sample).
python -m parsimony analyze \
  20250522_sweagent_claude-4-sonnet-20250514 \
  20250225_sweagent_claude-3-7-sonnet \
  --dataset verified.jsonl --limit 5 --output results.jsonl

# Compare only tasks solved AND analyzed by every selected agent.
python -m parsimony leaderboard results.jsonl --shared > leaderboard.json

python -m unittest discover -s tests -v
```

Useful `analyze` options:

- `--limit N` only limits analysis attempts. It never changes the resolve-rate denominator.
- `--task TASK_ID` (repeatable) analyzes a chosen cohort while keeping all 500 records.
- `--include-failed` also measures explicitly failed patches (see [failed patches](#failed-patches)).
- `--resume` appends missing records to an interrupted full single-submission run and retries `fetch_error` records. It verifies agent, results hash, ref and analyzer/Python versions first.
- `--patch-only` gives hunk-only estimates without fetching sources. These are a separate, less reliable mode that is never pooled with full-file results.

Output has one record per agent/task, including failures, unavailable analyses and skipped tasks. `leaderboard` rejects duplicate agent/task records. `--agent NAME` selects agents.

## Beta release tooling: frozen population and coverage

Freeze the task population **before** looking at candidate scores:

```sh
# Commit analyzer changes first; freeze requires a clean checkout unless --analyzer-commit is given.
python -m parsimony.release freeze verified.jsonl --name verified-500-beta-v1 --output population.json
python -m parsimony analyze SUBMISSION --dataset verified.jsonl --ref EXPERIMENTS_COMMIT \
  --include-failed --output all-results.jsonl
python -m parsimony.release audit population.json all-results.jsonl \
  --dataset verified.jsonl --output coverage.json
```

The manifest pins dataset bytes, task IDs/base commits, Python version and analyzer commit. `audit` checks records against it: population, duplicates, base commits, resolve totals and the `analyzer_commit` every record carries since 0.4.0. It reports coverage, statuses, exclusions, zero-footprint, value-only, out-of-scope, lexical and approximate records. This is **coverage reporting, not authenticity certification**. An official score additionally needs a preregistered, deduplicated successful-reference panel covering every frozen task.

## Artifacts, failed patches and caching

**Legacy layout.** Predictions come from the public `swe-bench-submissions` S3 bucket (`verified/<submission>/all_preds.jsonl`), and `results/results.json` from [SWE-bench/experiments](https://github.com/SWE-bench/experiments/tree/main/evaluation/verified) on GitHub. **Current mini-SWE-agent layout** (used on 404): `per_instance_details.json` supplies per-task booleans, and patches come from `logs/<task>/patch.diff` via `metadata.yaml`. Unsupported layouts fail explicitly. For custom or local artifacts, write a JSON manifest:

```json
{"agent": "unique-agent-name", "submission_url": "https://example.org/submission",
 "prediction_url": "all_preds.jsonl", "results_url": "results.json"}
```

```sh
python -m parsimony analyze --manifest submission.json --dataset verified.jsonl --output results.jsonl
```

### Failed patches

Mere absence from `resolved` is never treated as failure. With `--include-failed`, failures must come from explicit evidence:

- The current layout uses `resolved: false` per instance.
- Legacy submissions (whose `results.json` has no failure list) use per-task `logs/<task>/report.json` with `resolved: false` and an applied patch.

Missing logs or reports remain unknown, and a warning is printed when a submission publishes no explicit failures.

### Provenance and caching

`--ref COMMIT` pins GitHub results (S3 is not versioned by it). Records keep SHA256 hashes of predictions, results and each patch, artifact URLs, base commit, reference patch hash, analyzer version/commit/source hash and Python version. Downloads are cached atomically by URL under `.parsimony-cache/` (`--cache PATH` goes *before* the subcommand). Cached URLs are never refreshed, so use a new cache for mutable upstream changes. Keep the metadata JSONL and cache alongside results for reproducibility. To share exactly the bytes a result set depends on, pack a verified snapshot:

```sh
python -m parsimony.snapshot create examples/beta-500-v4/*-results.jsonl --output cache-v4.tar.gz
python -m parsimony.snapshot restore cache-v4.tar.gz --cache .parsimony-cache  # checks every SHA256 first
```

## Archived experimental score (80% net / 20% churn; not the website default)

See [the scoring specification](archive/scoring.md). Per-task percentiles against a frozen reference panel are blended 80/20 and averaged with equal task weights. Successes score 1 to 100. Explicitly failed attempts get a bounded nonpositive growth/churn penalty down to −25. Missing measurements, unknown outcomes and **out-of-scope successes** (every touched file excluded) produce bounds, not invented scores.

```sh
python -m parsimony.scoring score examples/ten-model-score-panel.json \
  examples/ten-model-results.jsonl --output /tmp/parsimony-scores.json
python -m parsimony.sensitivity examples/ten-model-score-panel.json \
  examples/ten-model-results.jsonl --output /tmp/sensitivity.json
```

`sensitivity` runs a paired-task bootstrap and a grid over net weight, failure cap and a `net_floor=0` anti-deletion variant. It covers neither panel composition nor task-selection bias.

## Limits

See the [repository audit and release-readiness review](archive/repository-audit.md) for engineering fixes, validation commands and outstanding release gates, and the [browser/accessibility audit](archive/site-audit.md) for tested behavior and remaining gaps. These audits are not independent benchmark certification or an accessibility-conformance claim.

**Code footprint is not technical debt.** Small code can be cryptic, incorrect beyond the benchmark tests, insecure or hard to maintain. Larger changes may add valuable validation. Human patches are a baseline, not an optimum. Net-weighted scores reward deletion, and SWE-bench tests do not protect untested code, so check the `net_floor` sensitivity variant.

The existing Python boards measure Python only. Optional [JavaScript/TypeScript and Go tracks](language-tracks.md) (introduced in analyzer 0.6.0; JavaScript/TypeScript moved to the official TypeScript parser in 0.7.0, Go to a versioned corrected grammar/EOF policy in 0.8.0) are kept separate from Python and each other; raw counts are not cross-language comparable. Scope is unified text diffs only: binary/rename-only diffs, quoted paths, malformed hunk headers and repeated sections for one implementation file are unsupported (recorded as errors, never scored). There is no call-graph, runtime, maintainability or behavioral-equivalence modeling. Path and generated-file filters are heuristic. Interpreter tokenizer/AST changes (notably f-strings) change results. Coding units measure size and nesting, not readability: a test-specific hardcoded branch can cost fewer units than a general fix.
