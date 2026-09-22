# Parsimony

**Beta / research prototype.** No official cross-model ranking or validated full-benchmark score has been released. Sample rankings below are exploratory and must not be treated as model recommendations. The first [500-task coverage audit](examples/beta-500/README.md) found an exclusion defect and is explicitly **not** a leaderboard.

Among agents that **successfully solve the same SWE-bench issue**, which leave the smallest code footprint?

Parsimony imports public **SWE-bench Verified** predictions and published evaluation results, statically measures their Python changes, and compares successful solutions. No LLM API calls, SWE-bench reruns, package installation from target repositories, or execution of submitted code.

## Quick start

Python 3.10+; **no runtime dependencies**. Run from this checkout (installation is optional: `pip install -e .`). Use the same Python version for comparable measurements.

```sh
# Download metadata, base commits, and human patches for all 500 Verified tasks.
python -m parsimony dataset --output verified.jsonl

# Real public artifacts; attempt just five successful tasks per submission.
python -m parsimony analyze \
  20250522_sweagent_claude-4-sonnet-20250514 \
  20250225_sweagent_claude-3-7-sonnet \
  --dataset verified.jsonl --limit 5 --output results.jsonl

# Match on tasks successfully solved AND successfully analyzed by both agents.
python -m parsimony leaderboard results.jsonl --shared > leaderboard.json

# Individual summaries (different task mixes; not a fair head-to-head ranking).
python -m parsimony leaderboard results.jsonl
python -m unittest discover -s tests -v
```

Remove `--limit` for full analysis. Limits select successful tasks alphabetically by default (eligible successes and explicit failures with `--include-failed`), **not a representative sample**; they never change the resolve-rate denominator. Repeat `--task TASK_ID` to analyze a specific matched cohort while retaining all 500 records and the full resolve-rate denominator. Output contains one record per agent/task, including failures, unavailable analyses and tasks skipped by the limit. Output files are overwritten by default. For an interrupted full single-submission run, `--resume` appends only missing task records to the same output; it requires full metadata and cannot be combined with `--limit`, `--task`, or `--manifest`. It verifies the agent, results hash, ref and analyzer/Python versions before appending. It does not retry completed errors. Multiple result files can be passed to `leaderboard`; duplicate agent/task records are rejected. `--agent NAME` (repeatable) selects agents for pairwise/shared comparisons.

A checked-in, live-artifact smoke-test excerpt is in `examples/smoke-results.jsonl`, with `examples/smoke-leaderboard.json`. A larger **10-model × 10-shared-task** sample using mini-SWE-agent v2.0.0 is in `examples/ten-model-results.jsonl` and `examples/ten-model-leaderboard.json`; see [the sample report](examples/ten-model-report.md). These are evidence of pipeline operation, **not statistically meaningful rankings**.

Reproduce the larger sample (pinned GitHub commit, dataset checksum and task IDs):

```sh
python -m examples.run_ten_models --dataset verified.jsonl
```

This saves all 5,000 agent/task records to `.parsimony-cache/ten-model-all-results.jsonl` and the 100 selected records plus leaderboard to `examples/`.

## Contributing or updating results

See [CONTRIBUTING.md](CONTRIBUTING.md) for the PR workflow. Export an existing agent/task JSONL into a checksummed result bundle with `python -m parsimony.contribute export`; GitHub checks regenerate its summary offline. No benchmark reruns are needed to contribute already-analyzed results. Community bundles live in `submissions/`.

## Experimental single score: 70% net / 30% churn

See [the scoring specification](docs/scoring.md): blend per-task reference percentiles with **70% net delta / 30% churn**, then average tasks equally. Successful solutions receive positive credit; known failed attempts receive nonpositive footprint penalties. Scores range from **−25 to 100**; missing measurements produce bounds rather than invented scores.

The offline calculator uses existing JSONL—no downloads or patch reanalysis:

```sh
python -m parsimony.scoring score examples/ten-model-score-panel.json \
  examples/ten-model-results.jsonl --output /tmp/parsimony-scores.json
```

The frozen panel and `examples/ten-model-scores.json` are an experimental **ten-task shared-success sample**, not an official full-benchmark release. The original `leaderboard` command and contributor bundles retain conventional medians as diagnostics. Failed-patch acquisition/analysis is opt-in (`analyze --include-failed`) for supported public artifact layouts; old result files do not contain failed-patch measurements. Missing failures still yield score bounds, not fabricated penalties.

## Beta release preparation: frozen population and coverage

Freeze the **task population before looking at candidate scores**. The following offline tooling does not confer official status, independently verify patches, or change the experimental ten-task score panel:

```sh
# Commit analyzer changes first; freeze requires a clean checkout unless --analyzer-commit is supplied.
python -m parsimony.release freeze verified.jsonl --name verified-500-beta-v1 --output population.json
python -m parsimony analyze SUBMISSION --dataset verified.jsonl --ref EXPERIMENTS_COMMIT \
  --include-failed --output all-results.jsonl
python -m parsimony.release audit population.json all-results.jsonl \
  --dataset verified.jsonl --output coverage.json
```

The population manifest pins dataset bytes, all task IDs/base commits, Python version, and analyzer commit. `audit` rejects out-of-population and duplicate records, mismatched base commits or denominators, and reports missing/analyzed successes and failures, analysis statuses, excluded paths, zero-normalized-edit records and identifier/literal-only edits. It is **coverage reporting, not authenticity certification**: upstream predictions and evaluations need independent review. `--include-failed` attempts explicitly failed patches; missing logs/patches remain unknown. `--limit` limits eligible analysis attempts, so omit it for coverage runs. New analyses carry analyzer version `0.2.1-beta` and a diagnostic `value_sensitive_churn` that retains identifiers/literals (still ignores formatting, comments and docstrings); do **not** mix them with the checked-in `0.1.0` sample in comparative panels. Existing results must be regenerated to acquire failed patches; the checked-in ten-task example remains a shared-success sample. An official score additionally needs a preregistered, successful-reference panel covering every frozen task.

For a **complete** existing score panel, run an exploratory paired-task bootstrap and sensitivity grid (net weights 50/70/100%, failure caps 10/25/50):

```sh
python -m parsimony.sensitivity examples/ten-model-score-panel.json \
  examples/ten-model-results.jsonl --output /tmp/sensitivity.json
```

Incomplete measurements are rejected rather than imputed. Resampling the ten shared-success tasks does **not** make their selection representative; neither these intervals nor top frequencies establish general model superiority.

## Artifacts and caching

The default adapter supports submission directory names or GitHub `tree` URLs for [SWE-bench/experiments](https://github.com/SWE-bench/experiments/tree/main/evaluation/verified): predictions from the public `swe-bench-submissions` S3 bucket (`verified/<submission>/all_preds.jsonl`), and published `results/results.json` from GitHub. It reads both `model_patch` and `patch` prediction fields and requires an explicit `resolved` result list.

On HTTP 404, a second adapter supports newer mini-SWE-agent submissions: `per_instance_details.json` provides explicit per-task boolean `resolved` results, and `metadata.yaml` identifies the public S3 logs/trajectory prefix. Patches are downloaded individually from `logs/<task>/patch.diff`, for selected successful tasks by default (and explicitly failed tasks with `--include-failed`). Where metadata has `logs: null`, the adapter checks the conventional sibling `logs` prefix beside `trajs`; missing patches remain unavailable, never zero-scored. Both artifact layouts preserve full published resolve totals. Unsupported layouts fail explicitly.

`--ref COMMIT` pins GitHub results; default is `main`. S3 predictions are not versioned by that ref. SHA256 hashes of predictions, results and each patch preserve artifact identity. Records also retain submission URL, artifact URLs, task ID, patch location, published result categories, reported model, base commit, reference patch hash and analyzer/Python versions. The submission directory is the agent identity, avoiding ambiguous model labels.

Downloads (dataset responses, patches, results, original repository files) are cached atomically by URL under `.parsimony-cache/`. Put global `--cache PATH` **before** the subcommand to change it. Cached URLs are not automatically refreshed: use a new cache to fetch mutable upstream changes. Preserve the metadata JSONL and cache alongside results for reproducibility. Dataset metadata comes from [princeton-nlp/SWE-bench_Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified); truncated responses are rejected.

Other layouts can be added as small adapters returning the same mapping from `parsimony/artifacts.py`. An explicit local JSON manifest already supports custom/local artifacts:

```json
{
  "agent": "unique-agent-name",
  "submission_url": "https://example.org/submission",
  "prediction_url": "all_preds.jsonl",
  "results_url": "results.json"
}
```

```sh
python -m parsimony analyze --manifest submission.json \
  --dataset verified.jsonl --output results.jsonl
```

Sources may be HTTP(S) URLs or paths relative to the manifest. Results must have `{"resolved": ["task-id", "..."]}`. This adapter still assumes the Verified benchmark; without metadata its denominator is 500. If supplying local metadata, use JSONL with `instance_id`, `repo`, `base_commit`, and optional human `patch` per task, covering the intended benchmark denominator. Do not provide an accidental subset when reporting Verified resolve rates.

## Methodology

1. **Correctness gate.** Only tasks listed as resolved in published results are eligible for positive efficiency credit. With `--include-failed`, explicitly failed patches can receive nonpositive experimental penalties; missing-generation and missing-log tasks are never rewarded for small/empty patches. Resolve rate is published resolved tasks / 500 (or the supplied metadata population), not successful static analyses / sampled tasks. Parsimony trusts published evaluation; it does not revalidate correctness.
2. **Before vs. after.** Fetch each touched implementation file at the dataset's exact `base_commit`, then apply unified-diff hunks in memory with strict position/context validation. New/deleted files use an empty before/after. No checkout, imports, test execution or shell patch commands. Unsupported/unapplicable patches and download errors are recorded, never silently scored as zero.
3. **Normalized tokens.** Parse valid Python with `ast`, remove docstrings, and canonicalize syntax with `ast.unparse`; tokenize with Python's tokenizer. Ignore comments, whitespace/indentation and line endings; map identifiers to `ID`, strings to `STR`, and numbers to `NUM`. Keywords/operators remain. Canonicalization also removes redundant parentheses and optional trailing commas. Align before/after token sequences with `SequenceMatcher(autojunk=False)` to count tokens added/deleted. This measures normalized structural edits, not literal diff-line sizes. Non-parseable Python uses lexical tokenization where possible; AST metrics are unavailable.
4. **Footprint.** `net_tokens = tokens_added - tokens_deleted`; `churn = tokens_added + tokens_deleted`. Negative net is genuine shrinking within this normalization. Report churn alongside net to expose rewrites. `files_changed` counts implementation files with different normalized token sequences (not formatting/comment-only changes).
5. **Scope.** Primary metrics include `.py` implementation only. Exclude test/doc/example/benchmark directories, test filenames, generated/protobuf files, migrations, vendored/external code and build outputs. Non-Python files, lockfiles and ordinary documentation are outside scope. Generated markers in the first 2,000 characters are excluded heuristically. Excluded paths are listed in every measurement; see `implementation()` for exact rules.
6. **Structure.** Sum full-file **AST-node delta** (all AST nodes, minus docstrings) and a simple **cyclomatic proxy delta**: function/lambda baselines plus `if`/conditional expressions, loops, exception handlers, extra boolean operands, comprehension loops/filters and non-default match cases. This is an explicitly defined proxy, not a claim of equivalence to every McCabe tool. If either side cannot parse, aggregate structural deltas are null, not zero.
7. **Human comparison.** Analyze the dataset's original human `patch` identically (not `test_patch`). `model_human_ratio` is **model churn / human churn**. Churn is used because net deltas can be zero or negative, making net ratios misleading. Zero human churn or unavailable reference analysis yields null. Both complete metric objects are retained.

The leaderboard reports medians of net tokens, churn, human ratio, changed files, AST delta and complexity delta, plus sample counts and resolve rate. Null values are omitted from medians; ratio/structure coverage is reported. It sorts by median net tokens, but does not combine correctness, churn and footprint into an opaque composite score.

`--shared` uses the intersection of resolved **and analyzable** tasks across selected agents, with exact task IDs in the output. This avoids task-mix confounding but can still select an unrepresentative easy subset. Inspect sample sizes and analysis failures. Full-file and patch-only records are never pooled.

### Patch-only fallback

```sh
python -m parsimony analyze SUBMISSION --patch-only --limit 5 --output estimates.jsonl
python -m parsimony leaderboard estimates.jsonl --mode patch_only --shared
```

Explicitly opt-in only: compare old/new hunk excerpts without fetching source. Fragments may lack indentation context, multiline literals, or docstrings; lexical errors are recorded. AST/complexity deltas are null. Prefer full-file analysis; patch-only estimates are not interchangeable with it.

## Limits and interpretation

**Code footprint/complexity is not all technical debt.** Small code can be cryptic, incorrect beyond benchmark tests, poorly designed, insecure, or hard to maintain. Larger changes may add valuable validation or improve architecture. Tests/docs excluded from the primary metric still matter. Human patches are a baseline, not an optimal minimum; identifier normalization intentionally discards semantic distinctions.

This MVP focuses on Python and unified text diffs. Binary/rename-only diffs, quoted paths and some legacy Python cannot be fully analyzed. It does not model dependencies, whole-project call graphs, runtime complexity, maintainability or behavioral equivalence. Repository-wide complexity changes are approximated by touched-file deltas; untouched files cancel. Token alignment can choose different equivalent edit scripts; interpreter AST/tokenizer changes (notably f-strings) can change results. Path/generated-file filters are heuristic and can miss or over-exclude files. Measurements include `touched_files` as an audit trail even when normalized churn is zero or every path is excluded. The secondary `value_sensitive_churn` catches identifier/literal edits but is not a semantic-equivalence or maintainability metric. The beta 500-task audit used `0.2.0-beta` and revealed false generated-file exclusions; current `0.2.1-beta` only recognizes generated-file **header comments**. Do not compare these analyzer versions or relabel the older records. A production benchmark should audit exclusions, pin every upstream revision, expand artifact/grammar support, and consider complexity distributions rather than just total deltas.

## Beta roadmap (in priority order)

1. Freeze the full task population and independently reproduce public patch/result artifacts; publish coverage and missingness before rankings.
2. Validate footprint against identifier/literal-only edits, excluded files, and other adversarial patches; compare alternative metrics without silently changing score versions.
3. Evaluate score sensitivity to reference-panel composition, 70/30 weights, failure cap and task mix; report paired uncertainty and per-task outcomes. The beta tool currently covers weights/caps and paired-task resampling, **not** panel composition or task-selection bias.
4. Expand to more models and harnesses on the **same frozen tasks** with consistent provenance. Add other programming languages only as separate versioned tracks once the Python metric is validated.

The offline release audit is a step toward (1), **not completion of this roadmap**.
