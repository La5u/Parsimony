# Next benchmark sources for model coverage

Investigation date: 2026-09-29. **Recommendation, not an import or new published board.** Parsimony needs existing model patches, exact repository/base revisions and explicit per-attempt outcomes (including failures). Aggregate leaderboard rows, gold patches and transcripts alone do not meet this requirement. Keep benchmarks, languages, harness/configuration and attempts separately identified; do not merge their scores into the current boards.

## Execution update

All four recommended workstreams were investigated on 2026-09-29. Live now has [import tooling and a clean four-task static pilot](swe-bench-live-investigation.md); its full-cohort historical provenance/rights still block a board. [Fresh DeepSWE evidence](../examples/deepswe-python/refresh-2026-09-29.json) has unchanged metadata hashes and 26 usable configurations. [Verified audit](verified-refresh-investigation.md) confirms unchanged experiments revision and rechecks exclusions, including partial Gemini 3.5 coverage. [Pro/Atlas audit](pro-atlas-artifact-audit.md) found anonymously readable legacy Pro S3 artifacts but no identified V2 or Atlas model-attempt export. No new published models/scores are claimed on the strength of this tooling/pilot.

## Priority

1. **SWE-bench Live — first new-benchmark pilot.** The [submission repository](https://github.com/SWE-bench-Live/submission) actually exposes final patches and outcome categories, rather than merely a task corpus. Start with a frozen Python Lite cohort or a predefined Go / JS+TS slice of MultiLang, using supported analyzers. This is a promising source of additional model configurations; it does not guarantee unique model names beyond the existing boards.
2. **Refresh existing Verified and DeepSWE inputs — cheapest route to adding models to the current lists.** Check new/changed artifacts before measuring. The [SWE-bench experiments README](https://github.com/SWE-bench/experiments) now documents both legacy S3 and submitter-hosted GitHub `assets` repositories. An importer should audit this layout rather than assume all submissions still live in S3. The experiments `main` revision inspected here is unchanged from our current Verified provenance, so this inspection itself provides no evidence of new Verified entrants.
3. **SWE-bench Pro V2 — next discovery candidate, conditional on run artifacts.** It is a good patch-footprint fit and has public frozen tasks, but model-run exports and their outcomes must be located and verified first. Do not reuse v1 outcomes for V2.
4. **SWE-bench Multilingual — useful language breadth, less immediate novelty.** The [experiments entries](https://github.com/SWE-bench/experiments/tree/main/evaluation/multilingual) include mini-SWE-agent configurations, mostly already represented model families. Start with supported language slices and verify their artifact links. Broader coverage needs explicit new language analyzers.
5. **SWE-Atlas Refactoring — strong conceptual fit, still artifact-blocked.** See [the investigation](swe-atlas-investigation.md). Obtain model-run exports before implementing an importer; QnA and test-writing are not drop-in implementation-footprint tracks.

Terminal-Bench is lower priority: choose a predefined coding subset only if exact before/after implementation files and per-attempt outcomes are recoverable. Do not measure arbitrary shell transcripts as code or treat all terminal tasks as repository-patch tasks.

## Direct evidence: SWE-bench Live

Inspected submission revision: `cba8a6d3197cd53da09f8527cccbc689782302a6`.

- The [submission README](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/README.md) describes predictions, evaluation results and trajectories for each agent/model configuration.
- The inspected `submissions/multilang/all_languages/sweagent/` directories include `claude-4-5-sonnet`, `deepseek-v3.1-terminus`, `deepseek-v4-pro`, `gemini-3-flash`, `gpt-5.2-medium` and `gpt-5.5-medium`. These are directory labels, not a complete current model inventory or audited model identities.
- A real layout differs from the README's generic `preds.json` / `results.json` example: [GPT-5.5 medium](https://github.com/SWE-bench-Live/submission/tree/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium) stores `result.json` at configuration level and task directories containing `patch.diff` and `trajectory.txt`.
- Its `result.json` explicitly lists 230 submitted IDs, 105 successes, 120 failures, five empty patches, zero errors and zero incomplete entries. **Empty-patch status is not automatically a failed outcome**; preserve it separately unless the source evaluation establishes failure. Validate set disjointness and complete coverage when importing.
- A directly downloaded `Automattic__harper-2962/patch.diff` is a real unified diff. It includes Rust/project-specific `.weir` changes: this proves patch availability, not compatibility with the current analyzer. It must not become a zero-footprint measured success under a supported-language board.
- The [benchmark README](https://github.com/microsoft/SWE-bench-Live) documents Python, MultiLang and Windows datasets, including frozen Python Lite/Verified splits and evolving larger datasets. Pin the exact dataset revision used by a historical run, not today's mutable dataset. A submission's 230 tasks must not be described as covering the entire newer MultiLang dataset.

**Still unaudited:** matching task revisions/base commits to these runs, complete failed-patch availability, retry/selection semantics, every configuration's task set, source/artifact redistribution terms, and counts of genuinely new models. Public availability alone does not settle redistribution rights. A pilot must resolve these before measurement/publication.

## Direct evidence: SWE-bench Pro

Inspected repository revision: `66f92766bba642462d4bbe5479e83f91f9211862`.

- [V2 README](https://github.com/scaleapi/SWE-bench_Pro-os/blob/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md): 642 tasks / 11 repositories, reference solutions, checksums and locked-protocol tooling. The README describes model-patch capture and pristine-sandbox regrading, but these are run instructions, not a historical model export.
- [Trajectory README](https://github.com/scaleapi/SWE-bench_Pro-os/blob/66f92766bba642462d4bbe5479e83f91f9211862/traj/README.md) points to `s3://scaleapi-results/swe-bench-pro/`, says AWS credentials are required to download, and says newer results live on S3 rather than GitHub. Anonymous access was not tested in this initial inspection; credentials were not used. The subsequent [artifact audit](pro-atlas-artifact-audit.md) did confirm anonymous listing/legacy patch access, but not identifiable V2 attempts.
- The inspected legacy `traj/claude-45sonnet-10132025/` contains `eval_results.json`; its task map includes explicit `true` and `false` outcomes. Model patches were not found in that directory listing. Those legacy runs are not evidence of V2 attempt availability or V2 correctness.
- V2's HARD-51 subset was selected using failures of named model families. Prefer the full independently defined V2 population for a general board; disclose selection bias if a hard-subset panel is used.

## First implementation gate

Before adding any board, build a small import manifest for one passing and one explicitly failed attempt in a supported language: dataset revision, task ID, repo/base commit, model/agent/config, attempt/selection policy, patch/outcome URLs and checksums, artifact status, and license/permission evidence. Strictly apply patches and parse offline; never execute submitted code or launch paid model evaluations. Then inventory the full cohort, freeze it independently of success, audit missingness/scope, and measure from a clean committed analyzer revision. Do not alter the published 80/20 formula or reuse old bootstrap results.
