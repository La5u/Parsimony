# Seed-OSS Live Python: candidate withheld

This is a public-artifact audit, not a board release, model/provider authentication or independent evaluator certification. No model calls, target-code execution or upstream correspondence occurred.

## Population and before-state evidence

The pinned MIT-IBM / Seed-OSS-36B-Instruct export retains 291 submitted IDs within the existing 300-task Live Lite Python population: 60 source successes, 211 failures, 20 errors and 9 missing/unknown tasks. All repositories and full base commits match the frozen population. The 271 success/failure candidates have corroborated touched-file preimages (268 old-blob/hunk matches; 3 new-files-only), comprising 528 source entries. This is not full-checkout or historical dataset certification.

Source revision: `cba8a6d3197cd53da09f8527cccbc689782302a6`; config: `submissions/lite/20251221-MITIBM-agent-seedoss36b`. The README declares one sample, Seed-OSS orchestrator/subagents, up to 60 calls per agent, unlimited cost, and no precise scaffold version. Agent/model licensing and public availability do not independently authorize raw redistribution.

## Newly found artifact conflict

All **243** available `logs/<task>/patch.diff` files were fetched and hash-bound:

- **4** agree byte-for-byte with aggregate predictions.
- **238** disagree; one separate patch has no corresponding prediction.
- **49** aggregate prediction IDs have no separate rollout patch.

None of the 238 disagreements disappear under final-newline, CRLF or Git header/index normalization. Diagnostic strict application to matching immutable bases found **226 divergent resulting contents or touched scopes**; **12** pairs include unsupported binary/nontext metadata and cannot be classified as identical by the text-only diagnostic. The four exact pairs apply identically. No relaxed/fuzzy application was used. This diagnostic is not a measurement release or a binary-aware evaluator.

The cached README and result categories do not establish which exact patch representation was evaluated. Neither the separate rollout patch nor the aggregate prediction can silently be substituted for the other. Mere preimage compatibility does not establish patch-to-outcome identity.

## Decision

**Withhold footprint publication and outcome-linked static measurements** until public evidence binds the evaluator input to an exact canonical patch. Source-reported 60 successes / 300 frozen tasks (20%) can be described with attribution, but is not independently verified. Do not invent footprint zeros for errors/missing tasks or promote this candidate to the Live leaderboard.

Metadata-only evidence and hashes: [`seedoss-candidate-review-2026-10-07.json`](../examples/benchmark-discovery/seedoss-candidate-review-2026-10-07.json). Raw predictions, rollout patches, base source and detailed audit caches remain external; redistribution is uncleared. No upstream contact or paid evaluation is authorized by this review.
