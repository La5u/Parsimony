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

The unchanged static measurements were made from clean analyzer commit
`de633004011e1b6c8dda81d234baefc024a88b75`, analyzer **0.6.0-beta**, Python
**3.14.7**, source SHA-256
`b2b45c86d1cb6ea6b035e697f7191ceaa00bf071f84eb47d1302ab7f2ac21b44`.
The JSONLs are byte-for-byte copies of the archived external measurements. No
record is relabelled to the newer scoring/site implementation commit.

## All-task score bounds

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
Default ordering uses the score-bound midpoint, as on other incomplete boards.
**There is no fabricated point score.** Known in-scope passing and failed
footprints both contribute to the displayed mean net units, including measured
failures whose reference calibration is missing.

Rank ranges use conservative lower/upper rank envelopes within **2,000 paired
full-population task resamples**, not just the order of bound midpoints. The two
leading configurations overlap in rank. Bootstrap score CI/graph endpoints remain
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

Detailed evidence: [targeted DeepSeek review](../../docs/deepseek-v4.1-live-release-review.md),
[full source/protocol/terms audit](../../docs/priority-live-provenance.md),
[preimage/coverage archive](../priority-live/README.md),
[coverage audit](coverage.json), [sensitivity](stability.md).

## Rebuild offline

The population and panel are frozen; do not overwrite them when adding entrants.
A new reference pool requires a separately named snapshot.

```sh
RECORDS='examples/live-python/deepseek-v4.1-flash.jsonl examples/live-python/gpt-5.6-sol.jsonl examples/live-python/claude-opus-4.8.jsonl'
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
