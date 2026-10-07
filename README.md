# Parsimony

Among agents that **successfully solve the same SWE-bench issue**, which leave the smallest code footprint?

Parsimony imports public **SWE-bench Verified** predictions and published evaluation results, statically measures their Python changes, and compares successful solutions. It makes no LLM API calls, runs no SWE-bench reruns, installs nothing from target repositories and never executes submitted code.

> **Status: beta / research prototype.** No official cross-model ranking or validated full-benchmark score exists. Everything in `examples/` is exploratory and must not be read as a model recommendation. Analyzer `0.5.0-beta` replaced lexical tokens with **coding units** (AST elements) as the primary metric (see the [changelog](CHANGELOG.md)). The current [two-submission 500-task audit](examples/beta-500-v5/README.md) uses it. Older audits are kept for history and are not comparable.

## Quick start

Python 3.12+, **no runtime dependencies for Python analysis**. Optional tracks: JavaScript/TypeScript use Node.js and the official TypeScript parser (`npm ci` installs the pinned `typescript`), Go uses `pip install '.[languages]'`; see [language tracks](docs/language-tracks.md) for pinned parsers, scope and reproducible commands. Run from this checkout (`pip install -e .` is optional). Measurements depend on the interpreter's tokenizer, so use one pinned Python version for anything you compare.

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

## Archived experimental score (80% net / 20% churn; not the website default)

See [the scoring specification](docs/scoring.md). Per-task percentiles against a frozen reference panel are blended 80/20 and averaged with equal task weights. Successes score 1 to 100. Explicitly failed attempts get a bounded nonpositive growth/churn penalty down to −25. Missing measurements, unknown outcomes and **out-of-scope successes** (every touched file excluded) produce bounds, not invented scores.

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

**Current website ranking:** lowest mean net coding units added first, across all measured in-scope attempts (successful and failed), with equal 1/N weight for each measured in-scope attempt, without correctness weighting or passing-reference selection. Missing measurements are excluded, never zero-filled. Footprint values are raw mean coding units, **not percentages**; Solved % is upstream resolved / full frozen population. Columns are Rank, Model, Net units added (mean), Net units added over solved attempts only (mean), upstream Solved %, and Measured eligible/population; any numeric column can be sorted, and rank stays on the all-attempt mean. Equal means tie and models with no measurements stay unranked. Partial coverage can bias the order; this is smallest measured footprint, not best coding ability. Failed no-ops and large deletions can rank first, and a few very large failed deletions can dominate a mean (on Verified, the #1 model's mean is −244 against +10 over solved attempts). A 10% trimmed mean was used briefly on 2026-10-01 and removed at the owner's request. The historical 80/20 scores, CI and score ranks remain available only as explicitly labelled optional archived diagnostics; they do not determine website rank.

`python -m parsimony.site PANEL RECORDS... --output site/index.html` renders one self-contained page offline from a frozen panel and measured JSONL. Each page has:

- the chart **before** the sortable leaderboard table with the columns above;
- a **Sources** bar chart **after** the leaderboard, derived from frozen population manifests: DeepSWE Python/JavaScript/TypeScript/Go have 34/5/35/34 tasks and 4 attempts per task; Verified has 500 tasks and Live Python 300, each with 1 attempt per task. Bar widths are task counts relative to the largest population, not ranking weights. The active board is marked, with report links and manifest hashes; boards remain separate, never pooled;
- a task-ID selector that swaps the same table and plot to one task's attempts, including failures (there is no second task table);
- a scatterplot with one borderless circle per model, colored by developer company: OpenAI black, xAI purple, Google green, Anthropic orange and DeepSeek blue. Every generation is labelled by name in plain HTML text, 8px, normal weight (400), black, with no halo, shadow or border. Each model line's newest generation (highest version, e.g. Claude Opus 5 over 4.8) has full-opacity circles and labels; older circles use 70% opacity and older labels 75%. Every label is vertically centered a fixed 10 CSS pixels to the right of its dot, without leader lines or variable-distance placement. Task failures are disclosed in the tooltip and accessible (ARIA) label, never with a dashed point outline. An uncaptioned green area marks the better corner on both axes (top-left for the default view: smaller footprint, more solved) and is omitted when an axis has no better direction. You pick the X/Y metrics from the table; the defaults are mean net units added vs. solved %; the solved-only mean is also selectable. Numeric axes fit the visible points with 5% padding. In All tasks only, Gemini 3.1 Pro (including Preview and effort variants) is excluded from numeric-axis fitting when at least two other points have finite values on that axis and exclusion changes the fit; Gemini 3.1 Professional and Gemini 3.1 Pro Plus are not excluded. Solved normally stays at 0–100%; when this exclusion changes its fit, it uses the other points' 5%-padded range bounded to 0–100%. Coverage stays fixed at 0–100%, and task-view scaling is unchanged. Points outside fitted axes are extrapolated at their true coordinates using the same linear scales, never clamped or replaced with edge markers; labels and hover disclose this, and hover details and the table retain actual values. Data and ranks are unchanged; there is no Pareto overlay.

Visible copy stays compact, with detailed caveats and archived-score explanations collapsed under **How to read this**. Pages are always light mode and show an instant tooltip with the model name and both selected axis names and values, plus the task outcome in task view. The archived 80/20 Score, its bootstrap 95% CI and rank ranges (`--sensitivity`) are available only as labelled optional graph metrics. They never affect the net ranking, and the CI never affects Score.

| Page | Data | Build flag |
|---|---|---|
| [`site/index.html`](site/index.html) (main) | [DeepSWE Python](examples/deepswe-python/README.md), 26 models | `--benchmark deepswe` |
| `site/javascript.html`, `typescript.html`, `go.html` | DeepSWE [JavaScript](examples/deepswe-javascript/README.md), [TypeScript](examples/deepswe-typescript/README.md), [Go](examples/deepswe-go/README.md); separate pinned tracks with explicit coverage limits | `--benchmark deepswe` |
| [`site/verified.html`](site/verified.html) | [SWE-bench Verified](examples/mini-swe-agent-500/README.md), 34 configurations | `--benchmark verified` |
| `site/live.html` | [Live Lite Python](examples/live-python/README.md): DeepSeek V4.1 Flash, GPT-5.6 Sol, Claude Opus 4.8 and GPT-5.5 / agav0.2.0-beta.2 as source-declared model + agent configurations on all 300 tasks | `--benchmark live` |

`--nav LABEL=URL` links the boards. All pages are served at [parsimony.lasu.dev](https://parsimony.lasu.dev) (Cloudflare Pages, output directory `site`). Edit `site/template.html` for layout and copy, then rebuild all six pages ([HANDOFF.md](HANDOFF.md#rebuild-all-six-pages-offline-no-remeasurement) has the exact commands).

## Bring your own benchmark

Every website page includes a local JSON importer near the bottom. Explore any benchmark with known code amounts—lines, tokens, bytes or your own defined units—without running the analyzer. Download the example, edit it and open it in the browser. Imports stay local, are labeled unverified and never mix with published boards. See [the format and public contribution guide](docs/custom-benchmarks.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). `python -m parsimony.contribute export` turns existing JSONL into a checksummed bundle under `submissions/`. PR checks validate it offline. `contribute verify` (also a manual CI job) re-downloads recorded patches, checks hashes and re-measures them.

## Examples (all exploratory)

| Example | Analyzer | What it shows |
|---|---|---|
| [deepswe-python](examples/deepswe-python/README.md) | 0.5.2-beta | 26 current models (2026) × 34 DeepSWE Python tasks × 4 attempts, one agent (mini-SWE-agent); imported with `python -m parsimony.deepswe` (the website's main board) |
| [deepswe-javascript](examples/deepswe-javascript/README.md) | 0.7.0-beta | 26 models × 5 JS-labelled tasks × 4 attempts; all 5 tasks calibratable; official TypeScript parser, script kind by file extension |
| [deepswe-typescript](examples/deepswe-typescript/README.md) | 0.7.0-beta | 26 models × 35 TS-labelled tasks × 4 attempts; official TypeScript parser; 33 tasks calibratable (5 analysis errors in 3,640 records), two upstream language-label mismatches documented |
| [deepswe-go](examples/deepswe-go/README.md) | 0.6.0-beta | 26 models × 34 Go tasks × 4 attempts; all 34 tasks calibratable |
| [mini-swe-agent-500](examples/mini-swe-agent-500/README.md) | 0.5.2-beta | 34 configurations × all 500 tasks with failures, mini-SWE-agent v0.0.0–v2.4.2; Gemini 3.5 Flash added with 441 measured attempts and 59 explicit no-generation outcomes; frozen population, archived score diagnostics and agent-version checks |
| [livecodebench-pilot](examples/livecodebench-pilot/README.md) | 0.7.0-beta units, separate complete-file scope | **NONPUBLISHED** fresh-code pilot: 18 configurations × 1,055 retained Python tasks; 17,353 measured attempts, fixed sample index 0, explicit partial-export/unknown/missing/failed states; original six snapshots preserved; provenance release review pending |
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

The existing Python boards measure Python only. Optional [JavaScript/TypeScript and Go tracks](docs/language-tracks.md) (analyzer 0.6.0; JavaScript/TypeScript moved to the official TypeScript parser in 0.7.0) are kept separate from Python and each other; raw counts are not cross-language comparable. Scope is unified text diffs only: binary/rename-only diffs and quoted paths are unsupported. There is no call-graph, runtime, maintainability or behavioral-equivalence modeling. Path and generated-file filters are heuristic. Interpreter tokenizer/AST changes (notably f-strings) change results. Coding units measure size and nesting, not readability: a test-specific hardcoded branch can cost fewer units than a general fix.

## Roadmap (priority order)

1. Freeze the full task population and independently reproduce public patch/result artifacts. Publish coverage and missingness before rankings. The [v5 audit](examples/beta-500-v5/README.md) does this for two submissions with a fresh-artifact recheck; more harnesses and independent review remain.
2. Validate footprint against adversarial patches. [Done for 0.5.1](docs/adversarial-validation.md): formatting, renames, excluded files, generated headers and deletions are tested; unrelated deletion, moved code and hardcoded test inputs remain known limitations.
3. Evaluate score sensitivity to panel composition, weights, failure cap and task mix, with paired uncertainty and per-task outcomes.
   [Stability report for 33 models × 500 tasks](examples/mini-swe-agent-500/sensitivity.md) (`python -m parsimony.stability`): weights and cap never change a rank; most neighbouring models are statistically tied, and the agent version alone moves a model by up to 5.6 points.
4. Validate units against blind human preferences on patch pairs, and add readability diagnostics (test-input hardcoding, nesting depth, reuse of existing helpers).
5. Expand to more models and harnesses on the **same frozen tasks**. Optional JS/TS and Go tracks are published with 7,696 additional attempt records and audited coverage (72 of 74 additional tasks calibratable; JS/TS remeasured in 0.7.0 with the official TypeScript parser). [SWE-Atlas investigation](docs/swe-atlas-investigation.md): newer-model aggregate scores exist, but public per-attempt model patches/results were not found.
