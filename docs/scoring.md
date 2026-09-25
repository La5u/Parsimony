# Parsimony scoring specification — experimental v0.4

**Status:** the offline calculator is implemented as `python -m parsimony.scoring`. It consumes existing full-file JSONL; it does not download artifacts, tokenize patches or execute code. The existing `leaderboard` command still reports medians separately. This is an experimental scoring rule, not a validated official benchmark release.

v0.4 applies the v0.3 rule to coding units (`net_units`, unit `churn`, analyzer 0.5.0) instead of normalized tokens. A record whose units are unknown (a file does not parse) gets bounds, like any missing measurement. v0.3 differed from v0.2 only in the `out_of_scope` rule.

## 1. Goals

- Every task contributes equally, independent of repository or patch size.
- Only published successful solutions receive positive efficiency credit.
- **70% net coding-unit delta / 30% churn**, after per-task normalization.
- Failed attempts receive bounded, nonpositive footprint penalties.
- A frozen reference panel prevents scores drifting as entrants change.

Failure does not prove every code change was useless. Call the diagnostic **failed-attempt footprint**, not “useless complexity” or “technical debt.” AST/cyclomatic deltas remain diagnostics, not components of this score. Tokens are not a complete measure of complexity or maintainability.

## 2. Frozen reference panel

A panel records fixed task IDs, successful reference agents, measurements, patch/result provenance, base commits, analyzer/Python versions, scoring constants and source JSONL checksums. Its file SHA256 accompanies every score report. At least one successful full-file reference measurement is required for every included task. Duplicate agent/task references are rejected.

Use a curated panel to avoid near-identical submissions dominating calibration. Failed panel patches are not success references. Human patches remain diagnostic references; human authorship alone does not establish a published passing result.

Each candidate uses the same panel, including a reference member's own patch as a tie when scoring that member. Do not use candidate-specific leave-one-out panels. New entrants never change the panel. The freeze command refuses to overwrite an existing panel; a changed cohort/panel requires a new named snapshot.

An official release would additionally freeze the dataset revision/checksum, exact analyzer commit and exclusion rules, audit artifacts and task coverage, and select its population independently of candidate success. Our current ten tasks were chosen from the intersection all ten models solved: they are a **shared-success sample**, not a measurement of full Verified performance or failure behavior.

## 3. Successful-task score: blend normalized percentiles

For task `t`, let `D` be net coding units (added minus deleted) and `H` be churn (added plus deleted). For either metric `x`, smaller is better. Against that task's frozen successful references:

```text
p_x = (number of references with a larger x
       + 0.5 × number of references with an equal x)
      / number of successful references

footprint_percentile = 0.70 × p_D + 0.30 × p_H
successful_task_score = 1 + 99 × footprint_percentile
```

**Normalize first, blend second.** Do not mix raw net/churn counts across tasks. A task involving thousands of units gets the same influence as a small fix. More deletion improves the net component; more churn lowers the churn component. Unlike lexicographic ordering, high churn can outweigh a small net-percentile advantage.

Success scores are from 1 to 100. Tying every reference on both metrics yields 50.5. Beating every reference on both gives 100. Matching a human patch does not necessarily mean 50.5: calibration uses the frozen submission panel, not the human alone.

Percentiles are coarse when reference counts are small. They also saturate: exceeding the largest reference by ten units or a million units yields the same component percentile. Always report raw footprint metrics alongside the score. The blend penalizes rewrites more than net-only ordering but does not eliminate all gaming or replace review of exclusions.

## 4. Failed-task score: same 70/30 priorities, no deletion credit

For a known evaluated failure with complete full-file metrics:

```text
G = max(D, 0)
s = max(1, median(churn of this task's successful references))

growth_burden = G / (s + G)
churn_burden  = H / (s + H)
failure_burden = 0.70 × growth_burden + 0.30 × churn_burden
failed_task_score = −25 × failure_burden
```

- Failures score between −25 and 0, never positive efficiency credit.
- A verified zero-footprint failure scores 0: neutral, not success.
- Deletion earns no credit on failure: negative net is clamped to zero, while deleted units still contribute to churn.
- Increasing growth or churn cannot improve a failure's score.
- The scale floor handles all-zero reference patches; bounding limits the effect of one enormous failed attempt.

The **25-point cap is provisional**. `python -m parsimony.sensitivity` also reports a `net_floor=0` variant: net deltas below zero are clamped, so deleting code (for example untested code that SWE-bench tests cannot protect) earns no net credit. The user-selected 70/30 weights express a preference, not an empirically established law. Validate sensitivity before an official release; never tune weights to reproduce familiar rankings.

### Should a huge successful patch lose to a near-empty failure?

**Not on the same task.** Even the worst success scores 1; the best failure scores 0. Otherwise doing nothing could beat difficult but correct implementations. Bulky successes can rank poorly among successful solutions without being treated as failures.

This does not claim every passing patch is maintainable or safe. If a benchmark has an independently defined validity/security requirement, adjudicate it explicitly rather than inferring invalidity from patch size. High AST/cyclomatic growth can still go unpenalized by unit counts: report it, do not silently change the scoring rule.

## 5. Equal-weight single score

For `N` fixed tasks:

```text
success_credit  = sum(successful task scores) / N
failure_penalty = sum(25 × failure_burden on failed tasks) / N
Parsimony Score = success_credit − failure_penalty
               = sum(all task scores) / N
```

This is a **signed −25 to 100 score**, higher better—not a percentage correct. Do not clamp negative scores to zero or omit missing tasks from the denominator. Each task has coefficient `1/N`; repositories and large patches receive no extra weight.

The score combines correctness and footprint. A model with a higher resolve rate is not guaranteed to rank first overall: footprint differences on other tasks can outweigh an extra solve. A strictly resolve-first leaderboard would instead sort by resolve rate then footprint and is a different policy.

Always show published resolve rate, fixed task count, scored-task count, success credit, failure penalty and individual task contributions alongside the score. In our shared-success sample the failure penalty is zero by selection, not evidence about failed attempts.

## 6. Unknown outcomes and missing measurements

Never confuse absent artifacts with an empty patch or an evaluated failure.

| State | Treatment |
|---|---|
| Published resolved, complete analysis | Successful formula |
| Explicit evaluated failure, complete analysis | Failed formula |
| Evaluated, explicitly empty failed patch | Failure score 0 |
| Explicit published no-generation/no-submission | `no_attempt`, score 0; no fabricated metrics |
| Missing logs or evaluation outcome | Unknown correctness |
| Missing patch, analysis/fetch error or skipped task | No point score for required missing measurements |
| Every touched file out of scope (`out_of_scope`) | No point score; excluded from reference panels |

The calculator requires an explicit failed result category (`unresolved`, `failed` or `not_resolved`) before assigning failure penalties. Mere absence from a resolved list is insufficient. `no_logs` stays unknown. `analyze --include-failed` now obtains and analyzes explicitly failed patches for supported layouts; old result files and missing patches still yield bounds rather than fabricated footprint penalties.

Per-task bounds are:

- Known resolved, unknown footprint: `[1, 100]`.
- Known failed, unknown footprint: `[-25, 0]`.
- Unknown correctness or missing task record: `[-25, 100]`.

Average bounds using the fixed task denominator. Any unknown contribution makes the overall `score` null; incomplete entries appear after complete scores without a ranked point estimate. Zero-width intervals indicate complete scores. Withholding data must not improve ranking eligibility.

Non-Python/excluded edits remain outside scope, not proven zero cost. A success that changes **only** excluded files is `out_of_scope`: bounds `[1, 100]`, never the best percentile, and never a reference. Preserve exclusions and audit suspicious scope shifts. Since analyzer 0.4.0, identifier/literal edits count toward primary churn.

## 7. Examples

Reference `(net, churn)` pairs are `(5, 9)`, `(10, 10)`, `(10, 30)`.

- Candidate `(10, 20)`: both percentiles are `1/3`; score **34**.
- Candidate `(4, 1000)`: net percentile `1`, churn percentile `0`; score **70.3**, not 100.
- Candidate `(5, 9)`: both percentiles are `5/6`; score **83.5**. A small net disadvantage can therefore beat a massive rewrite.

For a failed task with reference scale `s = 10`:

| Failed patch `(net, churn)` | Score |
|---|---:|
| `(0, 0)` | 0 |
| `(10, 10)` | −12.5 |
| `(−10, 10)` | −3.75 |
| `(0, 20)` | −5 |

Two equally weighted tasks scoring 34 and −12.5 produce `(34 − 12.5) / 2 = 10.75`, regardless of repository size.

## 8. Offline commands and release work

```sh
# Freeze once; use a new name/path for a changed panel.
python -m parsimony.scoring freeze examples/ten-model-results.jsonl \
  --name ten-model-ten-task-70-30-v0.3 \
  --output examples/ten-model-score-panel.json

# Recompute scores from already-measured JSONL, with no patch analysis.
python -m parsimony.scoring score examples/ten-model-score-panel.json \
  examples/ten-model-results.jsonl --output examples/ten-model-scores.json
```

The existing contribution bundle format still validates conventional footprint summaries, not frozen-panel scalar scores. A contributor may reproduce experimental scores locally and reference the panel hash in their PR; official scalar-score contribution/release validation remains future work.

Before broad claims: audit/approve a frozen release manifest, audit failed-patch categories and coverage, implement release-level artifact validation, expand the task population, and report uncertainty/sensitivity. These are separate from this lightweight cached-data scoring step.
