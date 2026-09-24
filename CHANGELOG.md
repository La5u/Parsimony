# Changelog

Analyzer versions change measurements. **Never pool or compare records from different analyzer versions**, and never relabel old records.

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

Results: the two-submission [v4 audit](examples/beta-500-v4/README.md), plus the ten-model and smoke samples, were regenerated with 0.4.0. `python -m parsimony.snapshot` packs a verified cache snapshot for reproducing them offline. `ast.parse` `SyntaxWarning`s from target sources are silenced.

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
