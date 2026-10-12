# Expanded public coding-artifact search

Audit: 2026-09-29 UTC. Read `HANDOFF.md`, the [prior Pro/Atlas audit](pro-atlas-artifact-audit.md), and its evidence first. This is anonymous discovery through Python `urllib`, not a model evaluation. No credentials, paid evaluation, target-code execution, patch application, contacts, measurements, or existing-file changes.

**Evidence:** [expanded-artifact-search.json](../examples/benchmark-discovery/expanded-artifact-search.json) records 234 exact request URLs, UTC timestamps, HTTP status, byte lengths and SHA-256 hashes, pinned revisions, range headers, artifact examples and blockers. Hashes refer to raw downloaded bytes; patch-field hashes explicitly refer to UTF-8 field contents. Transient signed public-download redirect queries are omitted, not used as source pins.

## What actually expands usable artifact coverage

| Source | Verified availability | Disposition |
|---|---|---|
| **SWE-PolyBench Verified** | GPT-5.4/iSWE and Claude Opus 4.8/HMigBot final predictions, sampled explicit successes **and failures**, public task/base joins; GPT-5-mini/Kodah also has predictions/results | Strongest additional repair-benchmark candidate; audit full outcomes, selection, historical inputs and rights before import |
| **SWE-rebench OpenHands collection** | Qwen3-Coder-480B final `model_patch` + explicit `resolved=0/1`, verified directly in pinned Parquet | Feasible offline import pilot; training collection, not monthly leaderboard or V2 |
| **Pro November Gemini export** | 728 explicit task booleans and matching patch objects, including empty patches | Separate **legacy** candidate only; no verified Pro V2 input provenance or new model identity |
| **SWE-rebench July 2026** | Recent-model transcripts and explicit outcomes, **submitted patches deliberately omitted** | Not aggregate-only, but blocked for patch-footprint import |
| SWE-rebench website; newer Pro leaderboard models | Aggregate statistics/claims | Not attempt imports |
| LiveCodeBench | Generated programs and explicit grading | Different completion benchmark, not repository repair patches |
| Aider polyglot | Aggregate model/config summaries in inspected sources | Per-task final-code/outcome export not located |

“Available” does not mean independently attested provider identity, redistribution permission, complete cohort audit, or ready-to-publish scores. Missing artifacts are never inferred failures.

## 1. SWE-bench Pro: enumerate S3, not just GitHub's old list

The pinned [trajectory README](https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/traj/README.md) explicitly says newer results are uploaded to S3 rather than GitHub. Its documented namespace is `s3://scaleapi-results/swe-bench-pro/`.

Anonymous ListObjectsV2 with `prefix=swe-bench-pro/`, `delimiter=/`, and a fresh query returned **all 15 prefixes, `IsTruncated=false`**—the same prefix set as the earlier audit. Every prefix was then enumerated **recursively**, following continuation tokens until false: **48 listing pages, 37,408 objects**. No prefix was excluded because it was absent from GitHub. Both bucket-root listing probes returned **403**: completeness applies to the entire *documented namespace*, not undiscovered namespaces, other buckets, or private exports.

Counts below are object-listing facts, not downloaded-body/solved counts. `pairs` means `_patch.diff` and `_output.json` share a task directory. `empty` means the listed patch has size zero. Every run also had a representative trajectory, patch and test output read and hashed.

| Run prefix under `swe-bench-pro/` | `.traj` | Patches | Test outputs / pairs | Empty patches |
|---|---:|---:|---:|---:|
| `claude-45haiku-10222025` | 729 | 730 | 727 | 11 |
| `claude-45sonnet-10132025` | 730 | 730 | 726 | 11 |
| `claude-4sonnet-10132025` | 563 | 562 | 553 | 2 |
| `claude-opus-4-1-paper` | 730 | 663 | 643 | 24 |
| `claude-sonnet-4-paper` | 637 | 631 | 611 | 88 |
| `gemini-2-5-pro-preview-250-turns-debug-nov17` | 730 | 728 | 724 | 45 |
| `gemini-2-5-pro-preview-250-turns-debug-oct22` | 730 | 728 | 724 | 45 |
| `gemini-2-5-pro-preview-paper` | 730 | 719 | 696 | 29 |
| `glm-4p5-10222025` | 730 | 729 | 728 | 16 |
| `gpt-4o-paper` | 643 | 619 | 596 | 16 |
| `gpt-5-250-turns-10132025` | 730 | 729 | 721 | 105 |
| `gpt-5-codex-debug-oct22` | 729 | 708 | 707 | 124 |
| `gpt-5-high-paper` | 730 | 730 | 707 | 250 |
| `gptoss-paper` | 728 | 728 | 702 | 305 |
| `kimi-paper` | 729 | 729 | 706 | 23 |

### Newly inspected November outcome export

[November `output/eval_results.json`](https://scaleapi-results.s3.amazonaws.com/swe-bench-pro/gemini-2-5-pro-preview-250-turns-debug-nov17/output/eval_results.json) contains **728 explicit booleans: 142 true, 586 false**. All 728 IDs have listed patches; 724 have test-output objects. Four outcome IDs lack test-output objects; their booleans are **upstream-reported**, not failures inferred by this audit from missing files.

Two downloaded OpenLibrary examples establish both sides:

- `…c506c1b0…`: boolean **true**, 2,499-byte patch, six `PASSED` tests; patch SHA-256 `60e88467504dcf524d10ab85a0edca046caaf16b1b15f685bf834c6474a5498f`.
- `…7c8dc180…`: boolean **false**, 7,045-byte patch, 95 `PASSED` and 12 `FAILED` tests; patch SHA-256 `3187e8960579ea37896dd351b3a70c4744faa781783b0a7441f058513be6c7e9`.

Full instance IDs and URLs are in `swe_bench_pro.november_explicit_outcome_export.examples`. The downloaded outcome export SHA-256 is `53955fcef2ae0dded3c017ac7258b0625c55d183925e513cfd7a2cdf29de6866`.

The [pinned evaluator](https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/swe_bench_pro_eval.py), lines 545–565, computes required F2P/P2P test membership but also emits false on missing evaluator output or exceptions. Preserve source-reported false plus unknown/error reason; do not claim every false represents a code-caused test failure. This source revision is not proven to be the historical evaluator. Other runs' sampled `_output.json` files are task-associated **test statuses**, not sufficient alone to assign authoritative `resolved` without historical required-test sets. All-PASSED observed tests need not prove task success.

### Model/config metadata, not prefix inference

Parsed `replay_config` identifies the configured routing name and limits for **one sampled trajectory per run**, not whole-run homogeneity or an independent provider attestation:

- Haiku/Sonnet 4.5: `anthropic/claude-haiku-4-5`, `anthropic/claude-sonnet-4-5`; Sonnet 4 dated: `anthropic/claude-sonnet-4-20250514`.
- **Prefix conflicts:** `claude-opus-4-1-paper` sample config says **`anthropic/claude-4-sonnet-20250514`**; `claude-sonnet-4-paper` sample config says **`anthropic/claude-opus-4-1-20250805`**. Do not relabel a whole run from either its prefix or a single conflicting sample.
- All three Gemini samples: `gemini/gemini-2.5-pro-preview-06-05`. November's separate config agrees, and its sampled trajectory bytes are **identical to the October sample**. Newer evaluation/upload material is not proof of a new independent model run.
- GLM: `fireworks_ai/glm-4p5`; GPT-4o: `openai/gpt-4o`; GPT-5: `openai/gpt-5`, `reasoning_effort=high`; Codex: `openai/gpt-5-codex`; GPT-OSS: `fireworks_ai/gpt-oss-120b`; Kimi: `fireworks_ai/kimi-k2-instruct`. All use the `litellm_proxy/` prefix; no proxy endpoint was contacted.

Samples report SWE-agent **1.1.0**, hash `unavailable`, temperature/top-p **1/1**. Dated samples have per-instance cost limit 0 and call limit 250; some still have total cost limit 5000. Paper samples have per-instance cost limits **1, 2, or 4** and call limits **50 or 100**. Thus README shorthand “paper $2 / dated no cost cap” is not an exact per-attempt config. Full sample fields and base commits are recorded in JSON.

### Version boundary and newer leaderboard claims

The [V2 README](https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md) describes **642 Harbor tasks**, versus the original **731**. These S3 configs are legacy/v1-style SWE-agent exports, with no immutable dataset revision/Harbor-V2 split attestation. Counts, overlapping IDs and reference patches do not certify V2. **V2 remains blocked; November may be considered only as a distinct legacy population after historical task/base/outcome and rights review.**

The [official Pro leaderboard](https://scale.com/leaderboard/swe_bench_pro_public) mentions GPT-5.4, Muse Spark, Claude Opus 4.6, Gemini 3.1 Pro and GLM-4.6. No matching final-patch export was found among the completely enumerated 15 prefixes. Those are leaderboard claims, not newly available patch cohorts.

## 2. SWE-rebench: official HF datasets versus attempt exports

Discovery used HF dataset search, Nebius's dataset inventory, the official site's links, and the [SWE-rebench organization](https://github.com/SWE-rebench). The pinned [V2 builder repository](https://github.com/SWE-rebench/SWE-rebench-V2) publishes construction prompts/evaluator/sample tasks, not a historical multi-model patch export in its inspected tree.

### Positive candidate: Qwen3-Coder with OpenHands

[`nebius/SWE-rebench-openhands-trajectories`](https://huggingface.co/datasets/nebius/SWE-rebench-openhands-trajectories/tree/35455389ab51bf5e2306bfd436ef72d0f98bf882) pins **67,074 rows** in one 2,079,503,354-byte Parquet object. Its card identifies **Qwen3-Coder-480B-A35B-Instruct / OpenHands v0.54.0**; final `model_patch`, `resolved`, `exit_status`, task and trajectory IDs are actual columns.

This was verified **directly against the pinned raw Parquet**, not just a dataset-server preview: anonymous byte-range reads of the footer and six first-row-group columns yielded **4,096 attempts: 1,991 resolved=1, 2,105 resolved=0; three empty patch rows**. Two nonempty examples were joined to the immutable original SWE-rebench filtered-task file at `89cdfbab4ab1bd8f5a658bb212d1b63624f4f881`:

| Task | Explicit outcome | Base commit | Model-patch SHA-256 (UTF-8) |
|---|---|---|---|
| `PlasmaFAIR__sdf-xarray-24` | 0 | `2cca296198333d0997371693c1607929d1379679` | `a9cce7855b26bce523b8c2c41107dd0c1b0d2a7b885a54ea0b8e11f55b6f3ed3` |
| `tianocore__edk2-pytool-library-372` | 1 | `f521d59041afee6a8a82206b3871960409aaa612` | `f85f48a59248826f1083b539b681bb77fd93b32e473d6843d596d41e19ec85d3` |

The full Parquet's advertised LFS hash is **not** claimed as whole-download verified; range checksums and offsets are recorded. The 33,886,640-byte filtered task file **was** fully downloaded and its hash matched the advertised LFS hash. Config defaults include temperature 0.7/top-p 0.8, but selection of a particular config section for every exported row is unproven; other model sections in `config.toml` are not evidence of their run exports.

**Feasible:** a pinned, separate offline pilot including explicit failed patches. **Still required:** full cohort/duplicate-attempt audit, exact historical task snapshot and bases, generation-config provenance and selection policy, source licenses and model-output terms. This is a training collection on **original SWE-rebench**, not the monthly leaderboard or SWE-rebench V2.

### July 2026: real recent-model outcomes, no final patches

[`ibragim-bad/swe_rebench_07_2026_trajectories`](https://huggingface.co/datasets/ibragim-bad/swe_rebench_07_2026_trajectories/tree/cdae27cdd16673f0c682871ad55d325f24cc7020) is a public normalized export, not merely an aggregate claim. The pinned manifest declares **9,435 trajectories, 111 tasks, 17 participants, five runs each, 85 gzip shards**. The tree lists all 85 shards; one was downloaded and parsed.

Participants: GPT-5.6 Sol/Luna, GLM-5.2, DeepSeek-V4 Pro, Fable 5, Grok 4.5, MiMo V2.5 Pro, MiniMax M3, Opus 5, Sonnet 5, Qwen3.5-35B-A3B, Qwen3.6-27B/35B-A3B, and Claude Code/Codex/Cursor/Junie. These are exporter participant labels, not independent identity attestations.

The GPT-5.6 Sol run-0 shard has **111 rows: 68 resolved, 43 failed**, and explicitly identifies `model=gpt-5.6-sol`, medium reasoning, `scaffold=swelike`. The manifest reports 4,751 resolved, 4,683 failed and **one skipped** overall: the manifest's 4,684 “unresolved” total must not be called 4,684 evaluated failures.

**Hard blocker:** both card and manifest state **submitted patches are not included**. Events can be truncated or omitted and built-in system prompts can be unavailable. Do not reconstruct final diffs from tool snippets. Rights are `license: other`, with third-party repository/provider terms retained. The official leaderboard task card also directs the July cohort to Harbor Hub; the old HF leaderboard task dataset is not proof of that cohort's historical bases.

### Other HF results that must not be mistaken for complete attempts

- **Official monthly leaderboard:** the [site](https://swe-rebench.com/) embeds 117 configuration entries with `rangeStats` aggregates (including a duplicate GLM-5.1 label), a problem catalog and insights; no final `model_patch` field found. The HF [`SWE-rebench-leaderboard`](https://huggingface.co/datasets/nebius/SWE-rebench-leaderboard/tree/34d5a58864acf91613740a09ec5d205228dcfa39) contains task/base/**gold** patches, not these model submissions. Keep aggregate claims separate from July's outcome-only export.
- **GLM-5.1 multi-harness:** pinned `isaacrehg/SWE_rebench_v2-GLM5.1-multiharness` has two fully downloaded Parquet files: **45 rows**, conversations and `completed`, but no final patch or correctness field. Actual row metadata is **34 `z-ai/glm-5.1` + 11 `claude-sonnet-4-6`**, despite the GLM-only card label. Harnesses observed: Hermes, Cline, Claude Code, Codex, pi. `completed` is not `resolved`.
- **GLM-5.1 pi successful traces:** pinned `whitecircle/swe-rebench-v2-glm-5.1-pi-agent-successful-traces` declares **7,777 success-selected traces**, 3,837 Python issues/four rollouts, columns `task_id/messages/tools/num_turns`. Bodies were not downloaded. No declared final patch/outcome columns or failed-attempt coverage; not an all-attempt cohort.

Original SWE-rebench, language-agnostic **V2**, monthly cohorts and July's Harbor population must remain distinct.

## 3. Alternative repair benchmark: SWE-PolyBench Verified

The [official site](https://amazon-science.github.io/SWE-PolyBench/) links directly to the repository's **`submission` branch**, not `main`. Pinned submission commit: **`e7062f4a848ca7775bc1c1313f7aa419bd6a3ec1`**. Its complete tree has **14,160 entries**, seven run directories with `all_preds.jsonl` and per-instance `_result.json` paths. This is genuine model-patch discovery beyond gold-only tasks.

Three recent prediction files were fully downloaded:

| Submission | Actual prediction/model evidence | Coverage and cautions |
|---|---|---|
| `20260623_migbot_claude-opus-4-8` | 382 nonempty predictions, every row labels `claude-opus-4-8`; 382 result paths | Sampled explicit pass/fail and base joins. Submitter describes 29 infrastructure retries, five temporal-isolation replacements and frozen-set re-evaluation; preserve these selection/provenance facts |
| `20260422_iswe_agent` | 112 nonempty Python predictions, `iSWE-Agent-GPT-5.4`; sampled localization config `azure-gpt-5.4`, high reasoning | Card claims 113-task Python cohort; `keras-team__keras-20002` has no prediction. Tree has **2,110** harness result files, including `generation=false` placeholders outside submitted cohort—do not import those as model failures |
| `20260430_kodah_gpt-5-mini` | 382 predictions, 47 empty; README identifies GPT-5-mini, 113 Python rows label `Kodah (gpt-5-mini)` | Other 269 model labels are null; underlying config not independently established for each row. Sampled passing and failing outcomes available |

Pinned [`AmazonScience/SWE-PolyBench_Verified`](https://huggingface.co/datasets/AmazonScience/SWE-PolyBench_Verified/tree/b3fca77b637379f0c01ad86d18753a7ac1998b53) `test.csv` was fully downloaded: **382 unique tasks, Python 113 / JavaScript 100 / TypeScript 100 / Java 69**. All inspected prediction IDs match this snapshot. Exact `repo/base_commit` joins work; that does not prove this current HF revision was the historical generation input. Some README language counts are inconsistent, so use the pinned task records rather than prose to define a new population.

Examples:

- iSWE `huggingface__transformers-12981`: explicit `resolved=true`, nonempty patch, base `75b8990d9068a2c6ef448c190f2595c17fbcb993`; `…13491`: explicit `resolved=false`, nonempty patch, base `1c191efc3abc391072ff0094a8108459bc08e3fa`.
- HMigBot `microsoft__vscode-177084`: explicit **true**, patch-field hash `85361c8771e4f6432c8231dd2a61ca5e45aa4813f9adbef3ca105ac4f1da6ee5`; `sveltejs__svelte-3702`: explicit **false**, hash `860cd6e951a4c0e8175e989c56daa74ee274bddf85ab96b0e3348fec1dca167b`. Both are temporal-isolation replacement cases disclosed by the submitter.

**Feasible imports:** separate Python/JS/TS populations and frozen agent/config identities, retaining failures, empty/missing patches and unsupported Java as explicit scope records. **Not yet cleared:** all outcome bodies (only samples audited), exact historical dataset/evaluator inputs, retries/replacements, underlying model/config homogeneity, original repositories and model-output redistribution terms. The project MIT license alone does not clear these.

Older listed submissions (Prometheus GPT-5, Rovo, prior iSWE) are additional *listed candidates*, not newly body-audited cohorts; notably Rovo lists 381 result files. Do not turn that missing file into a failure.

## 4. Other public coding benchmarks screened

- **LiveCodeBench:** [official submission repository](https://github.com/LiveCodeBench/submissions) pinned at the revision in JSON has 153 non-truncated tree entries. A `Claude-Opus-4` export contains **1,055 generated programs**, `code_list`, `graded_list` and `pass@1`: **658 true / 397 false** for its single generation per row. Public code + grading is real, but model identity here is folder provenance rather than row-level config. These are standalone contest-program completions, with no repair-base/diff. They need a separately designed benchmark/panel, not synthetic repair patches. Inspected official performance/submission snapshots largely cover 2025-era models; no verified 2026 frontier export located here.
- **Aider polyglot:** [official leaderboard](https://aider.chat/docs/leaderboards/) and pinned `aider/website/_data/polyglot_leaderboard.yml` include 225-exercise aggregate pass counts/configs, including GPT-5 high. No per-task final source/diffs plus explicit attempt results located in the inspected tree/pages. Aggregate rates and `dirname` labels cannot reconstruct attempts.
- **BigCodeBench / Terminal-Bench:** landing-page/old-repository probes only, not exhaustive artifact audits. The Terminal-Bench repository probe redirects to `harbor-framework/terminal-bench-1`; it is **not** evidence about Terminal-Bench 2/4 availability. Neither is promoted as a recent importable cohort by this audit.

## Reproduction and priority

1. GET the exact sources in JSON anonymously with `User-Agent: Parsimony-expanded-artifact-audit/1.0`; hash raw bodies. For S3 use the recorded continuation URLs, check each final `IsTruncated=false`, and count suffixes/task-directory joins. ETags are not assumed SHA-256.
2. HF API search discovers revisions; use `/resolve/<commit>/…` for evidence. Reproduce Qwen reads using recorded byte ranges, Parquet metadata and six projected columns with PyArrow (audit used **25.0.1**). Never execute conversation/tool contents. Dataset-server preview is discovery only.
3. First pursue **SWE-PolyBench GPT-5.4/Opus 4.8** full-cohort provenance/rights, then **Qwen3-Coder SWE-rebench** offline import pilot, then a separately authorized **legacy Pro November** population. July frontier transcripts and Pro V2 remain blocked for footprint without real version-identifiable submitted patches.

No importer or board was implemented. No result absence was converted into failure. All closure claims apply only to inspected public sources, not all possible hosting locations.
