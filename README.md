# Parsimony

Among agents that **successfully solve the same SWE-bench issue**, which leave the smallest code footprint?

Parsimony imports public **SWE-bench Verified** predictions and published evaluation results, statically measures their Python changes, and compares successful solutions. It makes no LLM API calls, runs no SWE-bench reruns, installs nothing from target repositories and never executes submitted code.

> **Status: beta / research prototype.** No official cross-model ranking or validated full-benchmark score exists. Everything in `examples/` is exploratory and must not be read as a model recommendation. Analyzer `0.5.0-beta` replaced lexical tokens with **coding units** (AST elements) as the primary metric (see the [changelog](CHANGELOG.md)). The current [two-submission 500-task audit](examples/beta-500-v5/README.md) uses it. Older audits are kept for history and are not comparable.

## Quick start

Python 3.12+, **no runtime dependencies for Python analysis**. Optional JavaScript/TypeScript and Go tracks use `pip install '.[languages]'`; see [language tracks](docs/language-tracks.md) for pinned parsers, scope and reproducible commands. Run from this checkout (`pip install -e .` is optional). Measurements depend on the interpreter's tokenizer, so use one pinned Python version for anything you compare.

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

## Methodology

1. **Correctness gate.** Only tasks listed as resolved in the published results earn efficiency credit. The resolve rate is published resolved / 500. Parsimony trusts published evaluation and does not revalidate correctness.
2. **Before vs. after.** Each touched implementation file is fetched at the dataset's exact `base_commit`, and the patch is applied in memory with strict position/context validation. Unapplicable patches are recorded as errors, never scored as zero. Network failures are recorded as retryable `fetch_error`.
3. **Coding units.** Each side is parsed with `ast` (docstrings removed) and walked in source order. A unit is one syntactic element: a statement (`if`, `return`, assignment, `def`), an expression (call, attribute access, arithmetic or boolean operation), each comparison, a name or a literal. Each statement block also ends with one `EndBlock` unit, so nesting and moving code into or out of a block count. Punctuation, brackets, commas, load/store markers, comments, formatting and name length are not units: `if x.count(y) > 0: foo(a, b)` is 12 units. Units are unknown (null), never zero, when a file does not parse on both sides (`lexical_files`).
4. **Alignment.** Unit counts come from an exact minimum edit script (Myers diff) over the unit sequence. Rewrites needing more than 500 edits use a line-anchored approximation and are flagged (`approximate_files`).
5. **Footprint.** `net_units = added − deleted`, `churn = added + deleted`. Negative net is genuine shrinking. A renamed name or changed literal is one changed unit; the `structural_churn` diagnostic ignores identifier/literal values. The pre-0.5 metric, normalized lexical tokens (`net_tokens`, `token_churn`), remains a diagnostic. `files_changed` counts implementation files whose normalized code differs.
6. **Scope.** Only `.py` implementation files count. Excluded: test/doc/example/benchmark directories, test filenames, `setup.py`/`conftest.py`, generated files (a header comment in the base commit), protobuf output, migration scripts, vendored and build output. Django's `db/migrations/` and `test/` framework packages count as implementation. Every record lists `touched_files` and `excluded_files`. See `implementation()` for the exact rules.
7. **Structure (diagnostic).** Full-file AST-node delta and a simple cyclomatic proxy delta (functions/lambdas, branches, loops, handlers, extra boolean operands, comprehension loops/filters, non-default match cases). These are null if either side does not parse.
8. **Human comparison.** The dataset's human `patch` (not `test_patch`) is measured identically. `model_human_ratio` = model churn / human churn, or null when the human churn is zero.

`leaderboard` reports medians (net, churn, human ratio, files, AST and complexity deltas), sample counts and resolve rate, sorted by median net units. `--shared` uses the intersection of resolved **and** analyzable tasks, which avoids task-mix confounding but can favor easy tasks.

## Experimental single score (80% net / 20% churn)

See [the scoring specification](docs/scoring.md). Per-task percentiles against a frozen reference panel are blended 80/20 and averaged with equal task weights. Successes score 1 to 100. Explicitly failed attempts get a nonpositive footprint penalty down to −25. Missing measurements, unknown outcomes and **out-of-scope successes** (every touched file excluded) produce bounds, not invented scores.

```sh
python -m parsimony.scoring score examples/ten-model-score-panel.json \
  examples/ten-model-results.jsonl --output /tmp/parsimony-scores.json
python -m parsimony.sensitivity examples/ten-model-score-panel.json \
  examples/ten-model-results.jsonl --output /tmp/sensitivity.json
```

`sensitivity` runs a paired-task bootstrap and a grid over net weight, failure cap and a `net_floor=0` anti-deletion variant. It covers neither panel composition nor task-selection bias.

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

## Website

`python -m parsimony.site PANEL RECORDS... --output site/index.html` renders a single self-contained page from a frozen panel and measured JSONL, offline: a sortable all-task leaderboard with 95% intervals, a shared task-ID selector, and a scatterplot with one point per model, colored by its developer company. Coordinates are mean churn and mean net coding units added across measured, in-scope passing **and failed** attempts. Hover, focus or tap a point for its model, values and measurement coverage. Selecting a task replaces the same table and plot with that attempt's measurements (including failures); there is no second task table. [`site/index.html`](site/index.html) (the main board) is built from the [DeepSWE results](examples/deepswe-python/README.md) with `--benchmark deepswe`, and [`site/verified.html`](site/verified.html) from the [33-model SWE-bench Verified results](examples/mini-swe-agent-500/README.md); `--nav LABEL=URL` links the boards. Additional 26-model DeepSWE boards cover [JavaScript](examples/deepswe-javascript/README.md), [TypeScript](examples/deepswe-typescript/README.md) and [Go](examples/deepswe-go/README.md), with explicit coverage limitations and separate pinned language tracks. All are served at [parsimony.lasu.dev](https://parsimony.lasu.dev) (Cloudflare Pages, output directory `site`). Edit `site/template.html` for layout and copy. `--sensitivity examples/mini-swe-agent-500/sensitivity.json` adds each model's 95% bootstrap rank range from the stability analysis.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). `python -m parsimony.contribute export` turns existing JSONL into a checksummed bundle under `submissions/`. PR checks validate it offline. `contribute verify` (also a manual CI job) re-downloads recorded patches, checks hashes and re-measures them.

## Examples (all exploratory)

| Example | Analyzer | What it shows |
|---|---|---|
| [deepswe-python](examples/deepswe-python/README.md) | 0.5.2-beta | 26 current models (2026) × 34 DeepSWE Python tasks × 4 attempts, one agent (mini-SWE-agent); imported with `python -m parsimony.deepswe` (the website's main board) |
| [deepswe-javascript](examples/deepswe-javascript/README.md) | 0.6.0-beta | 26 models × 5 JS-labelled tasks × 4 attempts; all 5 tasks calibratable; JS/TS grammars by file extension |
| [deepswe-typescript](examples/deepswe-typescript/README.md) | 0.6.0-beta | 26 models × 35 TS-labelled tasks × 4 attempts; 31 tasks calibratable, with grammar gaps and two upstream language-label mismatches documented |
| [deepswe-go](examples/deepswe-go/README.md) | 0.6.0-beta | 26 models × 34 Go tasks × 4 attempts; all 34 tasks calibratable |
| [mini-swe-agent-500](examples/mini-swe-agent-500/README.md) | 0.5.2-beta | 33 models × all 500 tasks with failures, mini-SWE-agent v0.0.0–v2.0.0; frozen panel, scores, rank ranges and an agent-version check (the website's second board) |
| [ten-model-500](examples/ten-model-500/README.md) | 0.5.0-beta | Ten models (plus Claude Opus 4.5) × all 500 tasks, mini-SWE-agent v2.0.0 only; superseded as the website's data |
| [beta-500-v5](examples/beta-500-v5/README.md) | 0.5.0-beta | Two complete 500-task cohorts in coding units; units vs tokens, coverage audit, fresh-artifact recheck |
| [beta-500-v4](examples/beta-500-v4/README.md) | 0.4.0-beta | Two complete 500-task cohorts in tokens (superseded by v5) |
| [beta-500-v3](examples/beta-500-v3/README.md) | 0.3.1-beta | Two complete 500-task cohorts; coverage audit (superseded by v4) |
| [beta-500-v2 investigation](examples/beta-500-v2/investigation.md) | 0.3.0-beta | Metric blind spots fixed in 0.3.1 |
| [beta-500](examples/beta-500/README.md) | 0.2.0-beta | First coverage audit (exclusion defect) |
| [ten-model report](examples/ten-model-report.md), `ten-model-*.json` | 0.5.0-beta | 10 models × 10 shared-success tasks; pipeline demo (superseded by ten-model-500) |
| `smoke-results.jsonl` | 0.5.0-beta | Live-artifact smoke test, legacy layout (`--limit 5`, experiments `40f164d`) |

The smoke and ten-model samples were regenerated with 0.5.0 (`python -m examples.run_ten_models` for the latter). Earlier versions are in git history.

## Limits and interpretation

**Code footprint is not technical debt.** Small code can be cryptic, incorrect beyond the benchmark tests, insecure or hard to maintain. Larger changes may add valuable validation. Human patches are a baseline, not an optimum. Net-weighted scores reward deletion, and SWE-bench tests do not protect untested code, so check the `net_floor` sensitivity variant.

The existing Python boards measure Python only. Analyzer 0.6.0 adds optional [JavaScript/TypeScript and Go tracks](docs/language-tracks.md), kept separate from Python and each other; raw counts are not cross-language comparable. Scope is unified text diffs only: binary/rename-only diffs and quoted paths are unsupported. There is no call-graph, runtime, maintainability or behavioral-equivalence modeling. Path and generated-file filters are heuristic. Interpreter tokenizer/AST changes (notably f-strings) change results. Coding units measure size and nesting, not readability: a test-specific hardcoded branch can cost fewer units than a general fix.

## Roadmap (priority order)

1. Freeze the full task population and independently reproduce public patch/result artifacts. Publish coverage and missingness before rankings. The [v5 audit](examples/beta-500-v5/README.md) does this for two submissions with a fresh-artifact recheck; more harnesses and independent review remain.
2. Validate footprint against adversarial patches. [Done for 0.5.1](docs/adversarial-validation.md): formatting, renames, excluded files, generated headers and deletions are tested; unrelated deletion, moved code and hardcoded test inputs remain known limitations.
3. Evaluate score sensitivity to panel composition, weights, failure cap and task mix, with paired uncertainty and per-task outcomes.
   [Stability report for 33 models × 500 tasks](examples/mini-swe-agent-500/sensitivity.md) (`python -m parsimony.stability`): weights and cap never change a rank; most neighbouring models are statistically tied, and the agent version alone moves a model by up to 5.6 points.
4. Validate units against blind human preferences on patch pairs, and add readability diagnostics (test-input hardcoding, nesting depth, reuse of existing helpers).
5. Expand to more models and harnesses on the **same frozen tasks**. Optional JS/TS and Go tracks are published in 0.6.0 with 7,696 additional attempt records and audited coverage (70 of 74 additional tasks calibratable). [SWE-Atlas investigation](docs/swe-atlas-investigation.md): newer-model aggregate scores exist, but public per-attempt model patches/results were not found.
