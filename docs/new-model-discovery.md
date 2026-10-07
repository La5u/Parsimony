# Current-model discovery and next additions

This search inspected public artifacts only: no model calls, paid evaluations, upstream contact or target-code execution. Parsimony remains a delivered-code footprint benchmark. A separate verbosity/yap/token-generation study is deferred, not implemented.

## Fresh DeepSWE check

The complete `https://deepswe.datacurve.ai/artifacts/v1.1/trials.json` was retrieved externally: 51,023,870 bytes, 31,617 trials, 70 configurations, 28 source-reported model names. Metadata bytes match the stored census:

- `release.json`: SHA256 `0b77963ed8c54ef40c5f744ade178b54bfae2662ed94f9235cee85eb542bdc85`.
- `leaderboard-live.json`: SHA256 `a7c15d66288fd249c020b9931c017b92d1a3b90e480b3ff34974b752bd030019`.
- `trials.json`: SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`.

The only names outside the existing 26-model DeepSWE inventory remain GPT-6 Astra and Gemini 3.8 Flash. Astra has **0 declared patches / 452 trials** in each of low/medium/high/xhigh/max. Gemini has declared patches for all 447 high and 452 medium trials. Two deterministic representative GETs per configuration (one source success, one failure) returned **HTTP 403**, 14/14 probes. This establishes sampled inaccessibility, not exhaustive Gemini patch absence. Version URLs are not independently proven immutable; hashes pin the observed metadata bytes.

Opus 5 and Sonnet 5 max configurations are already measured on all four DeepSWE language boards. Do not duplicate them or relabel as 5.5. No GPT-6.1, Ara, Opus 5.5 or Sonnet 5.5 generated-code export was located in the inspected inventories; this is not proof of global absence.

## 2026-10-07 refresh and fresh-code pilot

Bounded fresh checks retrieved complete DeepSWE metadata and GitHub trees for Verified, Live and PolyBench. All known revisions/hashes remain unchanged; no new existing-board export was located. GPT-5.2 Codex outcomes still returned 404, Astra still declares no patches, and four Gemini 3.8 Flash success/failure patch probes returned 403. These are sampled access results, not proof that no other export exists. Numerical evidence: [`model-battery-refresh-2026-10-07.json`](../examples/benchmark-discovery/model-battery-refresh-2026-10-07.json).

New body-level discovery verified six complete LiveCodeBench Python exports, then 12 additional configurations. The [NONPUBLISHED static pilot](../examples/livecodebench-pilot/README.md) now has **18 configurations × 1,055 retained tasks**, with **17,353 measured attempts**. Five exports have only 713/880 source tasks and Grok/DeepSeek V3 have absent code lists; the versioned protocol preserves all missing tasks as unknown outcomes/null footprints and missing artifacts as null footprints without zero-fill. Exact export membership and hashes remain mandatory. Original six snapshots are unchanged; only new inputs were measured. This adds concrete benchmark/model-family coverage, not a published board or new frontier-model claim. Generation configurations differ, and dataset/rights provenance still needs release review. Full expansion evidence: [`livecodebench-expansion-2026-10-07.json`](../examples/benchmark-discovery/livecodebench-expansion-2026-10-07.json).

The deeper [Seed-OSS Live audit](seedoss-live-candidate-review.md) found that 238/243 separate rollout patches disagree with aggregate predictions (4 exact matches, 1 without a prediction). Strict diagnostic comparison classified 226 as divergent result/scope and 12 as unsupported nontext changes, not trivial newline/header transformations. Touched-file preimages alone do not bind evaluated outcomes to exact patches. **Withhold its footprint release** pending evaluator-input linkage; retain 60 success / 211 failure / 20 error / 9 unknown categories across all 300 tasks.

A further [BigCodeBench outcome search](../examples/benchmark-discovery/bigcode-outcomes-search-2026-10-07.json) inspected pinned official repositories/leaderboard data in 25 bounded requests. The official requests dataset returned 401 and public result files are aggregates, not exact per-sample outcome pairings. This scoped access blocker is not proof that no paired export exists elsewhere.

BigCodeBench v0.2.4's complete 94,704,640-byte archive was retrieved and all 327 exports / 156 model labels inspected. It contains no paired outcome fields or outcome-result members; one Sonnet export has duplicate task records. Sanitized/calibrated filenames do not establish correctness. Exact asset hash, body counts and blockers: [`fresh-code-refresh-2026-10-07.json`](../examples/benchmark-discovery/fresh-code-refresh-2026-10-07.json).

## Existing-source revisions

Fresh public revision checks still resolve to:

| Source | Revision |
|---|---|
| Live submission main | `cba8a6d3197cd53da09f8527cccbc689782302a6` |
| Verified experiments main | `40f164d5b8f1d249bf95a6df8b74b577fd8e519d` |
| PolyBench submission branch | `e7062f4a848ca7775bc1c1313f7aa419bd6a3ec1` |

Gemini 3.5 Flash Verified is **already published**, not a new candidate. PolyBench Opus 4.8 remains measured externally but needs its existing population/provenance release work.

## Actual progress: fourth Live Python configuration

[GPT-5.5 / agav 0.2.0-beta.2](agav-gpt55-live-release-review.md) is now integrated into the local Live Python board: 300 population records, 271 completed analyses (`analysis_status=ok`) and 262 eligible in-scope footprints (185 successes, 77 failures). Completed full-file analysis does not guarantee footprint eligibility: 9 analyses are excluded-only (1 success, 8 failures). Upstream outcomes remain 186 successes, 85 failures and 29 empty-only unknowns. The ranking mean is 50.38549618320611 net units across eligible attempts; the eligible solved-only mean is 57.52972972972973. All 271 nonempty patches passed touched-file preimage auditing. Analyzer identity matches the other three entrants exactly. This adds a recent model to the Live board, not a globally new model identity: GPT-5.5 already exists in DeepSWE.

The separate ClaudeCode GPT-5.5 / DeepSeek V4 Pro all-language runs have **zero overlap with the Python Lite 300-task population**. They belong to MultiLang and cannot become Python additions by relabelling. Fresh GPT prediction/result audit verified 240 submitted IDs, 90 successes, 135 failures and 15 empty-only records; DeepSeek results have 67 successes, 118 failures, 55 empty-only records. Its full prediction refresh exceeded a 10 MB cap, though the earlier complete census read it. Use supported language cohorts and full preimage audits, not an arbitrary success-selected subset.

## Next actionable cohorts

1. **Live GPT-5.6 Sol JS/TS:** remeasure existing externally audited cohorts with 0.7.0's official TypeScript parser, retain all 108 JS / 111 TS tasks, then release separate comparative language boards when additional entrants are ready.
2. **Live SWE-agent GPT-5.5 and DeepSeek V4 Pro:** complete matching reset/preimage audits on the supported MultiLang cohorts. GPT-5.5's prior census has operational full-hash reset confirmation for all 79 nonempty Go/JS/TS attempts (40/17/22); preserve its empty TS item and predefined populations.
3. **Live AMI Opus 4.6 JS/TS:** final predictions and explicit aggregate outcomes are accessible in pinned `submissions/multilang/js_ts/ami-agent/20260710-v0.7.0-claude-opus-4-6/{js,ts}`. Existing census counts 93 JS / 111 TS records. Audit all preimages and disclose infrastructure retries and missing/empty scope; raw payload presence alone is not release readiness.
4. **Live Go AMI configurations:** Opus 4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1 Pro / 3.6 Flash have real final predictions. They use targeted retries, unlike single-rollout configurations. Gemini's 138 predictions versus 130 classified aggregate IDs require the detailed placeholder/timeout distinctions documented in [expanded census](expanded-live-census.md). Never promote them to ordinary failures just to fill counts.
5. **New-to-Parsimony older identities:** Seed-OSS-36B-Instruct (partial Lite 291-record run) and DeepSeek V3.1 Terminus are candidates if recent sources remain blocked. Preserve full benchmark denominators and historical population/version distinctions.

## More tests without paid runs

- **LiveCodeBench submissions**, pin `6ca212e9c2039373f6e5069d37ffa9db66e23736`: complete 153-entry inventory exposes model `*_eval_all.json` exports, including Opus 4. Generated code plus per-sample outcomes still need body verification, frozen date-window/sample policy and rights review. This would be a separate fresh-code Python population, not SWE patch data.
- **BigCodeBench v0.2.4** exposes `sanitized_calibrated_samples.zip` (94,704,640 bytes), documented as pregenerated model code. Model inventory, paired outcomes and exact asset digest still need auditing before import.
- **Aider** inspected tree contains benchmark harness/leaderboard metadata but no complete final-file exports; **EvalPlus** inspected results tree contains aggregate results, not verified generated solutions. Scores alone are insufficient.
- **SWE-bench Pro / Atlas** remain blocked on actual per-model patch exports. A grader result file or reference task corpus is not a candidate solution export.

User-accessible Codex/pi models and documented free OpenCode routes could support a separate secondary fresh-code pilot. No calls have been made. Freeze tasks, tests, exact configurations and credential-isolated generation/evaluation before starting; verify entitlement and obtain approval for any paid route. Provider labels and routing aliases are not authenticated model identities. Do not substitute output-token counts for retained implementation units.
