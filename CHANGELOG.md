# Changelog

Analyzer versions change measurements. **Never pool or compare records from different analyzer versions**, and never relabel old records.

## Recent-model static import tooling — 2026-09-30

- Extended Live import to plural results/keyed predictions, complete predefined language populations, reviewed offline analysis and checksum-bound preimage exceptions. Unknown/error/empty/incomplete are not inferred failures.
- Added immutable SWE-PolyBench candidate imports, full placeholder/result inventory and cache-only analysis; historical grading/rights/model attestations remain unverified.
- Added Git old-blob-prefix + strict-hunk auditing and a clean-checkout priority reproduction driver. Full five-cohort preimage audit corroborates 1,094 old-file patches plus two new-file-only patches; 11 exceptions remain unmeasured. No scoring formula/parser pins changed.
- Added research-preview site metadata that discloses mixed harnesses and unresolved historical provenance; not a certification gate bypass.

## Website: remove dedicated 95% CI column

Removed the confidence-interval column from all five boards. CI calculations, graph-axis endpoints and rank ranges remain; embedded data, measurements and scores are unchanged. The remaining numeric columns retain click-to-sort behavior.

## Import/discovery tooling — 2026-09-29

- Added `python -m parsimony.live` for immutable SWE-bench Live run inventories, explicitly mapped multi-file datasets (optional lazy Parquet support), checksums, complete submitted-record retention and evidence-gated offline analysis. Error, missing, empty-only and explicitly failed outcomes stay distinct. This is not a new published board.
- Verified imports can follow submitter-hosted GitHub `assets.repo` predictions/logs and declared refs, retaining official S3 support. Missing reports remain unknown; explicit applied-patch failure reports are imported separately.
- Fresh DeepSWE discovery still has 26 usable configurations and unchanged metadata checksums. Verified/Live/Pro V2/Atlas discovery evidence and publication blockers are documented under `docs/` and `examples/benchmark-discovery/`. Published parser pins, measurements, scoring and pages are unchanged.

## Website: data-fitted scatterplot axes

Numeric axes now use the visible points' minimum and maximum with 5% padding, rather than forcing zero. Solved percentage retains its 0–100% scale. Single/equal values and empty views have safe nonzero ranges; regression checks cover positive, negative, zero and missing values. Scores and measurements are unchanged.

## Website: light mode and immediate model tooltips

All boards now stay in light mode regardless of system theme. Model points show only the model name in an immediate custom hover/focus/tap tooltip, without the delayed native SVG tooltip. CI independence is explicit in the UI and tested: changing bootstrap confidence intervals cannot change Score or its default ordering. No scores or measurements changed.

## Website: selectable comparison axes

Removed Per solve and Median churn from the website, including selected-task views. Net units added is the sole raw footprint column (mean over measured passing/failed attempts in the all-task view). Users can choose any two numeric table values for the company-colored scatterplot; CI/rank endpoints are labeled explicitly. Default: net units versus solved percentage. The page explains the existing 80/20 all-task score, which remains unchanged.

## Website: model and company comparison

The scatterplot now explicitly compares models, using consistent developer-company colors and a legend across all boards. Points average measured, in-scope passing **and failed** attempts, rather than only solves. Hover/focus/tap labels expose model, company and measurement coverage. The all-task scoring formula and rankings are unchanged.

## Website and results — 2026-09-28

- One sortable board defaults to all score-panel tasks; the task-ID selector changes that same board instead of opening a second table. A responsive scatterplot shows mean net coding units added against mean churn per measured solve, or individual measured passing/failed attempts for the selected task. Conditional means are diagnostics; default ranking remains the all-task score. Coverage exclusions and the resolve-rate denominator are disclosed.
- Added separate 26-model DeepSWE JavaScript, TypeScript and Go boards: 7,696 attempt records over 74 additional task definitions, measured from clean commit `7705e8d`. All 5 JS and 34 Go tasks calibrate; 31 of 35 TS tasks calibrate. Known TypeScript grammar gaps and two upstream task-language mismatches remain explicit missingness, not zeros or model failures. Records and audits retain all attempts.

## 0.6.0-beta — 2026-09-28

Optional JavaScript/JSX, TypeScript/TSX and Go analysis uses pinned Tree-sitter grammars, syntax-unit traversal and the existing unit-diff machinery. Python measurements keep their AST implementation. Non-Python datasets require full-file analysis and carry a language/unit/parser-version track; panel creation, scoring, sensitivity and coverage reject mixed tracks. Failed attempts are still measured and penalized. No target code is executed. See [language tracks](docs/language-tracks.md).

Fresh DeepSWE v1.1 discovery found the same 26 usable configurations and identical run-index checksum. Gemini 3.8 patch probes still return 403; GPT-6 Astra runs declare no patches. No invented or relabeled results were added. [Refresh evidence](examples/deepswe-python/refresh-2026-09-28.json).

[SWE-Atlas Refactoring investigation](docs/swe-atlas-investigation.md) found newer-model aggregate scores and public reference patches, but no public per-attempt model patch/result archive; importing its model runs is blocked on artifact access.

## Results: DeepSWE, 26 current models — 2026-09-27

New importer `python -m parsimony.deepswe` for [DeepSWE](https://deepswe.datacurve.ai), a 2026 benchmark that runs every model with mini-SWE-agent four times per task and publishes each run's patch and pass/fail. [examples/deepswe-python](examples/deepswe-python/README.md) measures its 34 Python tasks for 26 current models (Claude Opus 5, Fable 5, GPT-5.6, Kimi K3, GLM-5.3, DeepSeek V4, Grok 4.6, …) and is now the site's main board; the SWE-bench Verified board moves to `site/verified.html`.

Each attempt is an item (`task#attempt`) scored against every passing patch of its task; the stability analysis and the site resample the attempts of a task together, which leaves results with one item per task unchanged. The site builder gains `--benchmark` and `--nav`. Measurement and scoring are unchanged.

## Results: 33 models × 500 tasks — 2026-09-27

[examples/mini-swe-agent-500](examples/mini-swe-agent-500/README.md) replaces the ten-model results as the site's data: 33 models run by SWE-bench with mini-SWE-agent v0.0.0–v2.0.0, measured with analyzer 0.5.2 and scored against a new panel frozen from all 33 (`mini-swe-agent-33-448-solved-80-20-v0.5`). Five models run under two agent versions show that the version alone moves a score by up to 5.6 points.

The stability analysis and the site now compare models over all tasks (an unscored task counts at the middle of its bounds; intervals and distinguishability use its best and worst case) instead of only the tasks where every model has a point score, which fell to 70 of 448 with 33 models. The site shows each model's 95% bootstrap rank range instead of tiers. Scoring is unchanged.

## 0.5.2-beta — 2026-09-27

Two fixes for older published mini-SWE-agent runs (July–August 2025):

- **A patch file missing its final newline is repaired, not rejected.** git ends every diff with a newline (a file without one gets a `\ No newline` marker), but these runs stored patches with it stripped. That turned a trailing blank context line into an empty line without a newline, so most of their patches failed with "patch context differs from base commit" (for example 244 of o3's 292 solved patches). Records now carry `provenance.patch_final_newline_restored`.
- **Patches are found when `metadata.yaml` names a folder that does not exist.** For four runs it points to another run's folder, uses different letter case, or omits `/logs`. When the named S3 folder has no per-task folders, the analyzer uses the bucket's standard `bash-only/<submission>/logs` folder and records `provenance.logs_source`.
- **New files at the repository root are excluded as scratch scripts.** Before mini-SWE-agent v2.0.0, submitted patches kept the scripts agents write while working (`reproduce_issue.py`, `comprehensive_test.py`, …): up to 94% of a model's solved patches, against none under v2.0.0, which drops them. Library code lives in packages and no maintainer fix in SWE-bench Verified adds a root-level file. Edits to existing root-level files still count.

## Results: Claude Opus 4.5 added to ten models × 500 tasks — 2026-09-26

Results only; no measurement or scoring change. Claude Opus 4.5 (high) (`20260217_mini-v2.0.0_claude-4-5-opus-high`) was measured with the same analyzer commit (`b2316a9`, 0.5.0-beta) and Python 3.14.7, and scored against the unchanged ten-model panel without becoming a reference; the ten original scores do not change. It ranks first (≈52.3). GPT-5.2 Codex and Gemini 3 Pro (high) are left out because their published per-task results are missing or mark every task unresolved. See [the example README](examples/ten-model-500/README.md#newcomers).

## Scoring parsimony-80-20-v0.5 — 2026-09-26

Scoring change only: **80% net units / 20% churn** replaces 70/30, for both the success percentile blend and the failure burden. The analyzer (0.5.1-beta) and every measurement are unchanged. All results were re-scored offline from the committed JSONL. The panels were refrozen under new names (`ten-model-ten-task-80-20-v0.5`, `ten-model-439-solved-80-20-v0.5`) with the same tasks and references. The sensitivity grid now uses 0.8 as the baseline and keeps 0.5, 0.7 and 1.0 as alternatives.

The ten models × 500 tasks leaderboard keeps the same order. Scores move by about 0.3 points at most:

| Rank | Model | Score 70/30 | Score 80/20 | Per solve 70/30 | Per solve 80/20 |
|---:|---|---:|---:|---:|---:|
| 1 | Claude Opus 4.6 | 49.1 | 49.1 | 58.4 | 58.3 |
| 2 | MiniMax M2.5 (high) | 47.9–48.1 | 47.8–48.0 | 57.0 | 56.8 |
| 3 | Kimi K2.5 (high) | 44.5 | 44.4–44.5 | 57.4 | 57.3 |
| 4 | Gemini 3 Flash (high) | 43.8 | 44.1 | 52.4 | 52.8 |
| 5 | GLM-5 (high) | 42.4 | 42.4 | 53.1 | 53.0 |
| 6 | Claude Sonnet 4.5 (high) | 39.3 | 39.2–39.3 | 50.9 | 50.8 |
| 7 | Claude Haiku 4.5 (high) | 35.5 | 35.4 | 50.7 | 50.4 |
| 8 | DeepSeek V3.2 (high) | 29.8–30.0 | 30.0–30.2 | 40.9 | 41.0 |
| 9 | GPT-5.2 (high) | 28.4 | 28.7 | 37.1 | 37.4 |
| 10 | GPT-5 mini | 25.2–25.8 | 25.2–25.8 | 45.2 | 45.1 |

Opus is now first in 66% of bootstrap resamples (was 64%) and MiniMax in 34% (was 36%). The 10-task sample also keeps its order.

## 0.5.1-beta — 2026-09-26

Fixes from the [adversarial validation](docs/adversarial-validation.md) (`tests/test_adversarial.py`):

- **A patch can no longer hide an edit by adding a generated-file header.** Only the base commit's version of a file decides whether it is generated; new files are always measured. Previously adding `# Auto-generated, do not edit` to an edited file excluded the whole file.
- **Only a top-level `testing/` directory is excluded.** Nested ones such as `sympy/testing/` and `lib/matplotlib/testing/` are library code.

No published measurement changes: all 5,010 published records re-measure identically, so they keep their 0.5.0 label. `contribute verify` compares against the running analyzer version, so re-verifying them needs a 0.5.0 checkout.

## 0.5.0-beta — 2026-09-25

Metric change: **coding units replace lexical tokens as the primary footprint.**

- A unit is one AST element: a statement, an expression (call, attribute access, arithmetic/boolean operation), each comparison in a chain, a name or a literal. Operators are folded into their expression, and load/store markers and containers (`Expr`, `arguments`, `withitem`, `FormattedValue`) are not units. Punctuation no longer counts: `foo(a, b)` was 6 tokens and is 4 units, and an `if` statement is its header plus one `EndBlock` unit.
- `EndBlock` ends every statement block (`body`, `else`, `finally`), so moving a statement into or out of a block is an edit and nesting costs a unit.
- Units are aligned with the existing Myers diff over the preorder unit sequence. `net_units`, `units_added`, `units_deleted` and `churn` are primary. `structural_churn` is now unit churn with identifier/literal values ignored.
- Units are null (unknown) when any measured file does not parse on both sides. Scoring treats such records as missing measurements and gives them bounds.
- Tokens remain diagnostics: `tokens_added`, `tokens_deleted`, `net_tokens` and the new `token_churn` (formerly `churn`).
- `model_human_ratio` is unit churn over human unit churn. `leaderboard` sorts by `median_net_units` and also reports token medians. `release audit` reports `unmeasured_unit_records`.
- Scoring `parsimony-70-30-v0.4`: the same formula over units.

Results and site: [ten models × 500 tasks](examples/ten-model-500/README.md) with failed patches, a frozen 439-task panel and paired-bootstrap intervals (analyzer commit `b2316a9`, measurement code identical to `54bd8a6`). `python -m parsimony.site` renders it as a static page in `site/index.html`. The two-submission [v5 audit](examples/beta-500-v5/README.md), plus the ten-model and smoke samples, were regenerated with 0.5.0 from the v4 cache snapshot (no downloads). Unit and token churn have a Spearman correlation of 0.99 on the v5 cohorts. The ten-model 70/30 scores moved: GLM-5 and Opus swapped second and third, and Sonnet and Haiku swapped fourth and fifth.

## 0.4.0-beta — 2026-09-24

Metric changes:

- **Primary churn now counts identifier and literal changes.** In earlier versions, edits like `x = 1` → `x = 2`, `a - b` → `b - a` or `foo()` → `bar()` had zero primary footprint. About 6% of successful patches in the v3 audit were affected. Identifier/literal-insensitive churn remains available as the `structural_churn` diagnostic. It replaces `value_sensitive_churn`, which is now the primary metric.
- **Exact minimal token diff.** A Myers (minimum edit distance) diff runs after trimming the common prefix/suffix. It replaces whole-file `difflib.SequenceMatcher(autojunk=False)`, which was quadratic on the low-variety normalized token stream: 292 s for one 54k-token file, versus about 1.6 s now, mostly parsing. On a 40-task sample of gold patches, identifier-insensitive churn matched 0.3.1 for 33 and was lower (minimal) for 7. Rewrites needing more than 500 token edits fall back to a line-anchored alignment and are listed in `approximate_files`.
- Each side of a file is now parsed and tokenized once.
- **Symmetric parse fallback.** When either side of a file fails to parse, both sides are tokenized lexically and the file is listed in `lexical_files`. Previously one side was canonicalized with `ast.unparse` and the other was not, which inflated churn (e.g. 24 counted for 3 real tokens).
- `django/test/` is treated as framework implementation, like `django/db/migrations/`.
- **Shifted hunks apply like `git apply`.** A hunk whose exact context sits at a different line number is applied at the nearest match. Context is never fuzzed, and equidistant matches are rejected as ambiguous. Previously 11 Verified gold patches (e.g. `django__django-15863`, `sympy__sympy-12489`) failed as "context differs", leaving `model_human_ratio` missing. `offset_hunks` counts shifted hunks per record, and `release audit` reports `offset_hunk_records`.

Pipeline:

- Network failures are recorded as retryable `fetch_error` records, not permanent analysis `error`s. `analyze --resume` retries them. A missing base-commit file (HTTP 404) remains an analysis error.
- Legacy (`all_preds.jsonl` + `results.json`) submissions: `--include-failed` reads explicit failures from per-task `logs/<task>/report.json`. Only a report with `resolved: false` and an applied patch counts as `unresolved`. Missing reports stay unknown (`no_report`). The CLI warns when a submission publishes no explicit failures.
- The human reference patch is measured once per task per process instead of once per agent record.
- Records (schema 2) carry `analyzer_commit` (null for uncommitted analyzers) and `analyzer_source_sha256`. `release audit` rejects records whose commit differs from the frozen population. It also reports records lacking one, plus out-of-scope successes and lexical/approximate alignments.
- `evaluation_result` now distinguishes `resolved`, `failed`, `no_generation`, `no_logs` and `unknown`. Previously every non-success was labeled `not_resolved`.

Scoring (`parsimony-70-30-v0.3`):

- A successful patch whose every touched file is out of scope is `out_of_scope`. It gets bounds, not a perfect zero-footprint score, and cannot serve as a reference. The ten-model sample scores are numerically unchanged.
- The sensitivity grid adds a `net_floor=0` variant that removes credit for net deletion.

Contributions:

- `python -m parsimony.contribute verify` re-downloads recorded patches, checks their SHA256 and re-measures them. A manual `workflow_dispatch` CI job runs it on bundles.
- Bundles may carry failed-patch measurements with an explicit failed category, and `fetch_error` records.

Packaging: package version `0.4.0b0`. `requires-python >=3.12` because f-string tokenization differs before 3.12. CI tests 3.12–3.14, but published measurements must use one pinned interpreter.

Commit references in the published 0.4.0 records point to `2d4cec6` (v4 audit, ten-model) and `53f1525` (smoke). These are reworded but tree-identical versions of the commits that ran; the recorded `analyzer_source_sha256` values verify this. Results: the two-submission [v4 audit](examples/beta-500-v4/README.md), plus the ten-model and smoke samples, were regenerated with 0.4.0. `python -m parsimony.snapshot` packs a verified cache snapshot for reproducing them offline. `ast.parse` `SyntaxWarning`s from target sources are silenced.

## 0.3.1-beta — 2026-09-24

- Counted canonical `INDENT`/`DEDENT` block boundaries in primary churn (block moves were zero-footprint).
- Kept f-string literal segments in the value-sensitive diagnostic.
- Published the two-submission [v3 audit](examples/beta-500-v3/README.md) and the [v2 investigation](examples/beta-500-v2/investigation.md).

## 0.3.0-beta — 2026-09-23

- Included Django's migration framework implementation (`django/db/migrations/`) while still excluding numbered migration scripts.

## 0.2.0-beta — 2026-09-22

- Beta population freeze/coverage audit, failed-patch analysis (`--include-failed`) and sensitivity diagnostics.
- The 500-task [beta audit](examples/beta-500/README.md) revealed false generated-file exclusions; the generated-file filter now only recognizes header comments.

## 0.1.0 — 2026-09-22

- MVP: static full-file footprint analysis, leaderboard, 10-model × 10-task sample.
