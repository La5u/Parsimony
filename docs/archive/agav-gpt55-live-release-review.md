# GPT-5.5 / agav: Live Python numerical release review

## Decision and scope

Add **source-declared GPT-5.5 / agav 0.2.0-beta.2** to the existing 300-task Live Lite Python footprint board. This is a repository-level numerical reporting decision following artifact, population, touched-file preimage and static-measurement review; **not independent evaluator certification, provider authentication, legal clearance or submitter consent**.

Publish numerical measurements, source links and integrity metadata only. Do not redistribute patches, target source, prompts, trajectories or grader output. The submission repository does not supply a blanket output-redistribution grant; public availability, agent licensing and provider/customer output ownership are not sublicences to Parsimony. Numerical factual reporting follows the same limited scope as the existing [Live release](../examples/live-python/README.md).

The measurement records remain byte-identical to the clean external analyzer export. Their embedded manifest's `approval_scope=external-static-measurement-only`, `board_release_status=not-approved` and `review_url_status=forthcoming` describe authorization **at measurement time**, not this later reporting decision. The local manifest is not an independent external approval. Its `manifest_sha256` binds the published preimage audit, not its own serialized bytes. Do not relabel analyzer identities or rewrite these historical fields to imply broader certification.

## Population, artifacts and results

- Submission revision: `cba8a6d3197cd53da09f8527cccbc689782302a6`.
- [Pinned submission](https://github.com/SWE-bench-Live/submission/tree/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/lite/agav/gpt-5.5).
- Candidate dataset: `SWE-bench-Live/SWE-bench-Live`, revision `b51a86422e10cfd403beb4773e5a2947953e36ec`, `data/lite-00000-of-00001.parquet`.
- Predictions and disjoint result-category union exactly match all **300** existing population IDs. Repositories and bases match the frozen population; it is not a success-selected cohort.
- **186 source-reported successes, 85 failures, 29 empty-only/unknown**. Every nonempty prediction has an explicit success/failure outcome. Empty-only records have no footprint and are not inferred failures or zero measurements.
- Result SHA256: `8524b27bec149fd98d38c7bfcbc0e5784342586fd20e6d805234fd9452ddcb8c`.
- Prediction SHA256: `ca355ec21d37cd06509edba2a665300b766220737bc8e4044535496b9bffbef2`.
- README SHA256: `a2275ebd6c7be038ac7dc621b1b245254bc2a3711d34115ceded3c83820bb372`.

All **271 nonempty patches** passed old Git blob-prefix and strict-hunk preimage checks; **658 touched-file source entries** were checked. The other 29 audits were not required. This corroborates the touched-file before-state, **not entire historical checkouts, original issue/test inputs, image digests or protocol compliance**. The original historical HF input identity stays unverified.

## Measurement and board integration

- Clean analyzer commit: `de633004011e1b6c8dda81d234baefc024a88b75` (0.6.0-beta).
- Source SHA256: `b2b45c86d1cb6ea6b035e697f7191ceaa00bf071f84eb47d1302ab7f2ac21b44`.
- Python: **3.14.7**, matching all existing Live Python records.
- **271/300 completed full-file analyses** (`analysis_status=ok`): 186 source-reported successes and 85 failures. Successful analysis does not guarantee an in-scope footprint.
- **262/300 eligible in-scope footprints**: 185 successful and 77 failed. Nine completed analyses (1 success, 8 failures) touch excluded-only paths and are not ranking inputs; the other 29 records are empty-only/unknown.
- Eligible-attempt mean net units: **50.38549618320611**.
- Eligible solved-only mean net units: **57.52972972972973**.
- Measurement JSONL SHA256: `1e398322396af536e5c58bd07241689bdb8309511229a9c64ce72eaf84a59e53`.

No target source or target tests were executed. Static measurement strictly applied and parsed the submitted prediction patch. Zero final-newline restorations were recorded. Separate-patch/transcript agreement remains `not_checked`; do not claim the full independent grader-export or output-transformation audit.

Keep the population and archived reference panel unchanged: **300 tasks, 509 passing references on 238 tasks, 62 uncalibrated tasks**. Recompute four-entrant coverage, archived scores/stability and the page, without changing the previous three raw exports. Default ranking remains the plain mean over all measured in-scope successes and failures; no token/reasoning expenditure, correctness tie-break, trimming or missing-zero imputation is introduced.

## Attribution and protocol limits

The README declares agav 0.2.0-beta.2, GPT-5.5/OpenAI, one rollout, 100 turns and 900 seconds. Prediction records contain no authenticated provider model identifier. Three available trajectories repeat the attribution and declare matching bases; they are samples, not full operational checkout proof.

Sampled shell calls use `sandbox: none` and transcripts expose macOS host paths. Do not certify container-only execution or network restrictions. Sampled Babel Git-history inspection is rooted at HEAD and does **not** establish future-fix contamination; absence of contamination across the run is also unproven. The README says patches are captured using `git diff`, but no complete original-rollout-to-prediction transformation audit was performed.

These are model + agent configurations, not a controlled model-only experiment. Source-reported correctness is not independently re-evaluated.

## Durable evidence and reproduction

- [Numerical release metadata](../examples/benchmark-discovery/agav-gpt55-release.json).
- [Full touched-file audit metadata](../examples/benchmark-discovery/agav-gpt55-preimages.json): hashes, paths and source URLs only.
- [Measurement authorization metadata](../examples/benchmark-discovery/agav-gpt55-measurement-review.json): historical static-analysis scope only.
- [Measured records](../examples/live-python/gpt-5.5-agav.jsonl).

Reproduction uses the pinned prediction/result and immutable dataset URLs above, external raw storage, `parsimony.live.import_run`, `parsimony.preimages.audit_run`, and `parsimony.live.analyze_run` from the clean analyzer commit. Reconstruct the inventory with config `submissions/lite/agav/gpt-5.5`, agent `agav`, model `GPT-5.5`; analyze with record agent `live-lite-gpt-5.5-agav-0.2.0-beta.2` and language `python`. Verify artifact hashes before using the measurement authorization. Never place the raw cache or imported patch inventory in this repository. The existing [offline rebuild commands](../examples/live-python/README.md#rebuild-offline) require no downloads or remeasurement.
