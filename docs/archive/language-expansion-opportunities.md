# Expanded model and language opportunities

Audit date: 2026-09-29. The earlier conclusion of no new complete usable cohorts applied to the selected DeepSWE/Verified refresh, **not all public sources**. Broadening the census found real additional patches/results, including a recent new-to-board model. No analyzer, importer, score, panel or page is changed by this research.

## Strong opportunities

| Priority | Source / configuration | Concrete artifact evidence | Work remaining |
|---|---|---|---|
| 1: new model | Live Lite / TianxiCode DeepSeek V4.1 Flash | 300 Python final predictions, 204 source successes / 96 failures; README explicitly identifies V4.1 Flash, not inferred from `deepseek-flash` folder | Add keyed `preds.json` + plural `results.json` adapter; complete operational base/patch verification, grading-retry and artifact-terms review |
| 1: more data now | Live SWE-agent GPT-5.5 medium | 40 Go / 17 JS / 23 TS submitted records; all 79 nonempty supported-language attempts have exact task-specific historical base resets and patch blobs | Full strict measurement, preserve empty TS record; obtain a second comparable reference cohort; no one-model comparative ranking |
| 2: new-to-board identity | SWE-bench Multilingual / GPT-5.2 Codex | 300 explicit per-instance outcome booleans; sampled successful and failed Go/JS/Rust patches downloadable from official S3 | Pin task-language mapping and operational bases; language-specific frozen panels; representative probes are not full artifact coverage |
| 2: more existing-model data | Live Slingshot GPT-5.6 Sol v3.4.0 | 300 Python results/predictions (211 success / 89 failure), 108 JS and 111 TS records | New agent/configuration, not new underlying model; audit historical inputs and selection; separate Live population |
| 2: more existing-model data | SWE-PolyBench Verified / GPT-5.4 iSWE and Opus 4.8 HMigBot | Public final predictions and sampled explicit success/failure outcomes; dataset has 113 Python / 100 JS / 100 TS / 69 Java tasks | Full outcome/base/retry/replacement review; source rights; explicit adapter and separate benchmark panels |
| 3: training-attempt data | SWE-rebench / Qwen3-Coder OpenHands | Pinned Parquet includes final `model_patch` and explicit outcomes; 4,096 directly inspected attempts | Full duplicate/attempt/config and task-base audit; training collection must not be called monthly/V2 leaderboard |

See [expanded Live census](expanded-live-census.md) and [expanded cross-source search](expanded-artifact-search.md) for exact definitions, pins, URLs, hashes and selection caveats. These are available inputs, not already published Parsimony measurements or independently validated model identities/outcomes.

## What another analyzer would unlock

Current measurement tracks support Python, JS/TS and Go. **Java or Rust are justified next-language candidates**, but existing supported-language imports already offer model/data expansion without a new parser.

- **Java:** 69 SWE-PolyBench Verified tasks; 160 in the pinned Live candidate Java split; 43 according to the pinned SWE-bench Multilingual card. Multiple public model configurations have final patch artifacts in these sources. This is a strong enterprise-relevant expansion candidate.
- **Rust:** five current DeepSWE tasks; 171 in the pinned Live candidate split; 43 according to the Multilingual card. Live has actual Rust model patches, including an AMI Opus 4.6 run with 94 result/prediction IDs, though only 86 predictions are nonempty. DeepSWE Rust extends current models, not new unique model identities.
- **C/C++/C#:** real Live patches exist, but language mixtures, headers, generated code and project-specific scope need explicit rules. The C-labelled Live Tetragon example changes Go/generated files: metadata alone does not justify silently measuring it as C or moving it between cohorts.

These counts are separate benchmark populations, **not a combined unique-task count**. Do not pool raw coding units or scores across languages/sources. New parser/counting rules need pinned dependencies, regression/scope tests, a versioned analyzer/track and clean-cohort measurements. Adding a language does not magically recover unavailable newer-model outputs.

## Direct Multilingual check

Fresh experiments revision remains `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`. All 14 `evaluation/multilingual/` directories were inventoried: twelve have 300 per-instance rows, MiniMax M2.5 has 297, Gemini 3.5 Flash has 264. This yields 4,161 configuration/task outcome rows, not distinct tasks or complete measured attempts.

Pinned HF candidate `SWE-bench/SWE-bench_Multilingual` at `846e647b9f33c0b51b739d005d13d85493c9af09` supplies 300 rows and exact repo/base metadata. Its README describes Ruby 44 / Rust 43 / PHP 43 / Java 43 / Go 42 / C 30 / JS 26 / TS 17 / C++ 12. **Rows have no task-language field**; freeze only after obtaining a pinned explicit per-task/repository mapping, independent of which patches pass. Do not use the card's natural-language `language: en` as programming-language metadata.

For GPT-5.2 Codex, exact `resolved: true/false` task outcomes exist in `per_instance_details.json`, although `results/results.json` is 404. Official metadata points to the multilingual S3 logs. Direct probes returned:

- Go: `caddyserver__caddy-5626` success patch **200**; `caddyserver__caddy-4774` explicit-failure patch **200**.
- JavaScript: `axios__axios-4731` success **200**; `axios__axios-4738` explicit failure **200**.
- TypeScript: `vuejs__core-11589` success **200**; `vuejs__core-11739` explicit-failure patch **403** (unavailable, not empty).
- Rust: `astral-sh__ruff-15330` success **200**; `astral-sh__ruff-15309` explicit failure **200**.

These illustrate repository-language opportunities, not a frozen dataset classification. Exact bytes/checksums and candidate metadata are in [multilingual-expansion-census.json](../examples/benchmark-discovery/multilingual-expansion-census.json). No source patch was executed or newly measured. Seven successful downloads do not prove every artifact is available. Historical dataset/repo bases, full scope, harness protocol, complete missingness and reuse rights remain gates.

## Recommended implementation order

1. Adapt Live's alternate JSON layouts and pilot **DeepSeek V4.1 Flash in Python**, then add supported-language comparative cohorts.
2. Import Multilingual Go/JS/TS, explicitly keeping GPT-5.2 Codex's missing artifacts distinct. Do not splice into existing Verified/DeepSWE panels.
3. Add SWE-PolyBench supported tracks with matched task/harness disclosures.
4. Design **Java first for breadth across three sources**, or Rust first for extending DeepSWE and its existing cohort. Choose explicitly; finish TypeScript coverage investigation rather than relaxing parser rejection.
5. Defer Pro V2/Atlas model import without genuine model exports. Rebench July has recent-model outcomes/transcripts but explicitly omits final patches, so it remains unavailable for footprint measurement.
