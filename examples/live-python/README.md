# SWE-bench Live Lite — Python

Website: **[parsimony.lasu.dev/live.html](https://parsimony.lasu.dev/live.html)**.
One published board, using the same layout as the other benchmarks; no preview
page or alternative solved-only ranking.

## Fixed population and configurations

All **300** tasks in the immutable Lite candidate file are retained, independently
of candidate success, reference availability, or footprint measurement coverage.
`population.jsonl` contains only task IDs, repositories, full base commits and
language, not issue text, gold code or tests. Its frozen manifest binds those
bytes and the underlying HF provenance.

| Source-declared model + agent | Upstream solved / 300 | Eligible footprints / 300 |
|---|---:|---:|
| DeepSeek V4.1 Flash / TianxiCode 0.1.423 | 204 | 287 (202 successful, 85 failed) |
| GPT-5.6 Sol / Slingshot 3.4.0 | 211 | 288 (205 successful, 83 failed) |
| Claude Opus 4.8 / AiWork.Code | 102 | 276 (102 successful, 174 failed) |
| GPT-5.5 / agav0.2.0-beta.2 | 186 | 262 (185 successful, 77 failed) |

The unchanged static measurements were made from clean analyzer commit
`de633004011e1b6c8dda81d234baefc024a88b75`, analyzer **0.6.0-beta**, Python
**3.14.7**, source SHA-256
`b2b45c86d1cb6ea6b035e697f7191ceaa00bf071f84eb47d1302ab7f2ac21b44`.
The JSONLs are byte-for-byte copies of the archived external measurements. No
record is relabelled to the newer scoring/site implementation commit.

## Current website: net-unit footprint ranking

The website now ranks by **mean net units added, ascending**, over all measured
in-scope attempts, including 85 DeepSeek failures, 83 Slingshot failures, 174
AiWork failures and 77 agav failures. Upstream Solved % is separate context. Eligible/population
coverage remains visible (287/300, 288/300, 276/300 and 262/300). GPT-5.5 / agav
has mean net units **50.38549618320611** across eligible attempts and
**57.52972972972973** over eligible solved attempts only. Its 271 completed
full-file analyses (`analysis_status=ok`) include 9 excluded-only attempts
(1 success, 8 failures), which are not ranking inputs: successful analysis does
not guarantee an in-scope footprint. The 29 empty-patch-only records
have unknown correctness and no footprint metrics. Missing footprints are
never zero; models without measurements are unranked. Equal values tie. A failed no-op or large
deletion can rank first: this is footprint comparison, not a coding-ability rank.

Passing references and their absence do not restrict footprint data. Task views
show all recorded tasks and their actual net changes when eligible. The 80/20
score calculations and uncertainty below remain archived optional diagnostics,
not the website's ranking inputs. Raw records and source-reported outcomes are
unchanged.

## Archived all-task combined-score bounds

The frozen pool contains **509 passing reference measurements on 238 tasks**.
The other **62 tasks remain in the denominator**, rather than becoming a
success-derived subset or invented zero contributions.

The point formulas are exactly `parsimony-80-20-v0.5`: 80% net / 20% churn,
success credit 1–100 and failed-attempt penalty −25–0. This panel opts into
`full-population-uncalibrated-bounds-v1`: when calibration is absent, an otherwise
eligible published success has bounds **[1, 100]**, an explicit failure
**[−25, 0]**. Unknown correctness has **[−25, 100]**. Missing/out-of-scope footprints
retain the existing outcome-conditioned bounds. These enclose every admissible
unchanged score; they do not create metrics, references or point estimates.

Thus every configuration has **300 contributions** and a bounded overall Score.
Archived score diagnostics order by score-bound midpoint; the website's default
ordering is mean net units, not the archived score.
**There is no fabricated point score.** Known in-scope passing and failed
footprints both contribute to the displayed net units, including measured
failures whose reference calibration is missing.

Rank ranges use conservative lower/upper rank envelopes within **2,000 paired
full-population task resamples**, not just the order of bound midpoints. Both adjacent pairs among the top three
configurations overlap in archived score rank. Bootstrap score CI/graph endpoints remain
computed separately; there is no dedicated CI table column. Removing a reference
model in sensitivity analysis retains all 300 tasks with enlarged uncertainty.
Reference/task membership does not drift with candidate success or UI filtering.

## Reporting scope and limitations

This release publishes **independently computed numerical measurements and
integrity/provenance metadata**, not model patches, target code, prompts,
trajectories, test output or training corpora. It does not grant rights to those
underlying artifacts. Public dataset/harness licence declarations do not relicense
embedded target source or other users' model outputs. No provider/customer output
assignment or model-weight licence is treated as a grant to Parsimony.

The reporting decision is limited to attributed numerical facts, not a blanket
legal clearance. We made no model/API evaluations, contacts, paid requests or
claims of consent. Plain model/agent names identify the reported configurations;
they do not imply provider, submitter or benchmark endorsement.

All models are **source-declared**, all pass/fail labels **source-reported**.
This is a model + agent comparison, not a controlled model-only experiment.
Historical HF evaluator inputs, image digests and protocol compliance are not
independently certified. Before-file blob-prefix/hunk matches corroborate touched
files, not entire historical checkouts. Failed/empty/error/incomplete states remain
distinct and missing data do not become zero-footprint failures.

Specific caveats retained from the source review:

- DeepSeek: full 300-task patch/metadata/report agreement; routing alias does not
  authenticate the provider backend. Grading retries are not extra model attempts.
- Slingshot: generic prediction model labels, sampled operational provenance,
  persistent memory/live clones and future-commit inspection concerns. Do not
  certify its adherence to the benchmark container protocol.
- AiWork: adaptive reasoning effort, submitted-patch transformations and grader
  errors/empty-only outcome. Do not label this a constant-xhigh run or independently
  certify absence of future-fix contamination.
- agav: GPT-5.5 and agav0.2.0-beta.2 are source-declared labels, not provider
  authentication or independent grading. The 29 empty-patch-only outcomes remain
  unknown, not failed no-ops. The targeted release review does not establish that
  every detailed report was audited or certify historical protocol compliance.

Detailed evidence: [targeted GPT-5.5 / agav review](../../docs/agav-gpt55-live-release-review.md),
[agav discovery metadata](../benchmark-discovery/agav-gpt55-release.json),
[targeted DeepSeek review](../../docs/deepseek-v4.1-live-release-review.md),
[full source/protocol/terms audit](../../docs/priority-live-provenance.md),
[preimage/coverage archive](../priority-live/README.md),
[coverage audit](coverage.json), [sensitivity](stability.md).

## Rebuild offline

The population and panel are frozen; do not overwrite them when adding entrants.
A new reference pool requires a separately named snapshot.

```sh
RECORDS='examples/live-python/deepseek-v4.1-flash.jsonl examples/live-python/gpt-5.6-sol.jsonl examples/live-python/claude-opus-4.8.jsonl examples/live-python/gpt-5.5-agav.jsonl'
python -m parsimony.scoring score examples/live-python/score-panel.json $RECORDS \
  --output /tmp/live-scores.json
cmp examples/live-python/scores.json /tmp/live-scores.json
python -m parsimony.stability examples/live-python/score-panel.json $RECORDS \
  --output examples/live-python/stability.json
python -m parsimony.site examples/live-python/score-panel.json $RECORDS \
  --benchmark live --sensitivity examples/live-python/stability.json \
  --output site/live.html --data examples/live-python/site-data.json \
  --nav 'DeepSWE Python=index.html' --nav 'DeepSWE JavaScript=javascript.html' \
  --nav 'DeepSWE TypeScript=typescript.html' --nav 'DeepSWE Go=go.html' \
  --nav 'SWE-bench Verified=verified.html' --nav 'Live Python=live.html'
```

These commands do arithmetic/rendering only. They do not fetch or execute target
code/tests. Existing DeepSWE/Verified measurement/score data are unchanged, apart
from adding navigation to this separate benchmark/language board.
