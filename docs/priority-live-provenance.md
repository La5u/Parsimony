# Priority current Live runs: practical import provenance

Audit: **2026-09-30 UTC**. Companion: [priority-live-provenance.json](../examples/benchmark-discovery/priority-live-provenance.json). This supersedes the priority-run *inspection depth*, not the published measurements or populations, of [expanded-live-census.md](expanded-live-census.md). Only these two new evidence/documentation files are added. No model calls, contact, paid access, target-code/test execution, patch application, measurements, scores or commits were made. Raw research downloads remain outside Parsimony.

Later follow-up: [DeepSeek V4.1 targeted release review](deepseek-v4.1-live-release-review.md)
freshly checks all 300 separate patches/metadata/grader reports, retrieves both
DeepSeek terms pages successfully, and distinguishes completed static analyses
from in-scope footprint eligibility. It does not retroactively certify this
historical audit or clear other configurations.

## Decision

**All five run/track exports have complete submitted-ID and prediction coverage in the pinned candidate task files. None has a full independently confirmed historical checkout/base dictionary for its entire measurement cohort.** Full declarations, actual operational observations, and before-file compatibility are kept separate in the JSON. Do not copy candidate or declared bases into `base_commit_confirmations` merely to pass a gate.

The missing original HF revision is **not** a blanket obstacle to static measurement. Recorded checkout operations or independently corroborated before-source bytes can establish the relevant before-state for a bounded import. Here, ten successful/failed patch examples have matching old-file Git blob prefixes against exact candidate-base source bytes; all available Slingshot trajectories have operational checkout/HEAD corroboration. Full-run historical input identity, protocol compliance and rights remain separate questions.

| Export | Submitted / nonempty predictions | Source success / failure / error / empty-only | Trajectories fully read | Independent full-hash checkout/HEAD evidence |
|---|---:|---|---:|---:|
| TianxiCode / DeepSeek V4.1 Flash, Python | 300 / 300 | 204 / 96 / 0 / 0 | 300 | **0/300**; 300 matching raw metadata/header declarations; 67 abbreviated commit-log candidates |
| AiWork.Code / Opus 4.8, Python | 300 / 299 | 102 / 190 / 7 / 1 | 300 | **3/300** |
| Slingshot 3.4.0 / GPT-5.6 Sol, Python | 300 / 300 | 211 / 89 / 0 / 0 | 14 | **14/300** |
| Slingshot 3.4.0 / GPT-5.6 Sol, JavaScript | 108 / 108 | 79 / 26 / 3 / 0 | 10 | **10/108** |
| Slingshot 3.4.0 / GPT-5.6 Sol, TypeScript | 111 / 111 | 70 / 40 / 1 / 0 | 10 | **10/111** |

These are **1,119 configuration/task records over 519 candidate tasks**, not 1,119 unique tasks. Measurement candidates with present patches and explicit success/failure are respectively **300, 292, 300, 105, 110**. Empty-only AiWork `beeware__briefcase-2214` remains unknown correctness, not a newly inferred failure. Errors are not ordinary graded failures. Preserve every submitted record even when a bounded pilot marks its patch `not_selected`.

## Pins and actual bytes

Fresh GitHub `main` still resolves to **`cba8a6d3197cd53da09f8527cccbc689782302a6`**, dated 2026-09-29T07:53:41Z. The [fresh commit response](https://api.github.com/repos/SWE-bench-Live/submission/commits/main) was hashed; all inspected submission payloads were checked against their Git blob IDs in the earlier complete, non-truncated pinned tree. **2,369 distinct submission files** are individually listed with byte count, SHA256 and Git blob SHA1 in the JSON, including the complete five result/prediction payloads, 634 trajectories, 300 Tianxi raw metadata files, 300 commands, 300 separate final patches, 815 detailed grader reports, and two raw event-stream examples. Additional cached status/test-output files are not counted as audited evidence merely because they were downloaded.

The three complete Parquet byte streams were re-read, SHA256-verified against the prior direct immutable downloads, and decoded using external `pyarrow==25.0.1`. Fresh revision-API responses resolve to the requested full SHAs. This is **actual file/row evidence**, not dataset-server navigation or a README denominator.

| HF dataset / split | Revision / file | Bytes / rows | Exact file SHA256 |
|---|---|---:|---|
| `SWE-bench-Live/SWE-bench-Live` / `lite` | `b51a86422e10cfd403beb4773e5a2947953e36ec` / `data/lite-00000-of-00001.parquet` | 14,442,471 / 300 | `7ee0a75c41bfc954fd441b67ce738fc5c1cbae00721c4e30e7db4d893057c9ab` |
| `SWE-bench-Live/MultiLang` / `js` | `62dc0745c40f067fc366ae3eb1a26136e5928f85` / `data/js-00000-of-00001.parquet` | 45,122,982 / 108 | `bc6ec49ffaf9db97840d55eba6954fae8f5fb0fb071cf49e187f36ffadd55a7a` |
| `SWE-bench-Live/MultiLang` / `ts` | `62dc0745c40f067fc366ae3eb1a26136e5928f85` / `data/ts-00000-of-00001.parquet` | 31,013,117 / 111 | `7e23783e27230c9cfab1035690035c25523043d6af635bc78da3fd2010c32714` |

Direct links: [Lite bytes](https://huggingface.co/datasets/SWE-bench-Live/SWE-bench-Live/resolve/b51a86422e10cfd403beb4773e5a2947953e36ec/data/lite-00000-of-00001.parquet), [JS bytes](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/resolve/62dc0745c40f067fc366ae3eb1a26136e5928f85/data/js-00000-of-00001.parquet), [TS bytes](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/resolve/62dc0745c40f067fc366ae3eb1a26136e5928f85/data/ts-00000-of-00001.parquet).

The JSON retains **all 519 exact repository/base pairs**, row indices, explicit split-to-language mapping, and hashes of full decoded task rows, without retaining gold patches or issue text. These are labelled `candidate_tasks`, **not the run's original task manifest**. Tianxi explicitly names the HF dataset and Lite split; AiWork names Lite/300 but not the exact HF input repository/file; Slingshot's READMEs name scaffold/model/rollouts, while its directories and result IDs supply track/population context. None of the inspected priority-run declarations pins an original HF revision. Exact membership and matching declared/observed bases do not prove the original issue text, test patch, test lists or image digest. Lite rows do not actually contain an image field; Tianxi's image tags come from its raw metadata. MultiLang rows contain `docker_image`. Tags are not immutable image digests; no containers were pulled or started.

## Run-specific findings

All paths below are relative to `submissions/` in the pinned [submission tree](https://github.com/SWE-bench-Live/submission/tree/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions). Exact raw URLs/hashes are reconstructible from the JSON's URL template and `source_file_manifest`.

### TianxiCode: full declarations, not 300 operational reset confirmations

Path: `lite/tianxicode/deepseek-flash`.

- All **300 `logs/rollouts/<id>/meta.json`** records have the correct task ID, repository and full base against the immutable Lite row. All 300 rendered headers agree. All 300 summary records exactly equal their separate metadata files. Binary version is `0.1.423`, model alias `tianxi-agent-plan/deepseek-flash`, extraction `git diff HEAD`; all 300 command files specify that alias. The complete raw metadata field inventory has **no separate `artifact_base_commit` field**: `git diff HEAD` names an extraction operation, not an observed HEAD SHA. **All 300 separate patch bytes equal the keyed `preds.json` strings**, including byte counts in metadata.
- **DeepSeek V4.1 Flash is the README/environment expansion of that routing alias**, not independently authenticated provider model identity. Do not relabel it as another DeepSeek version by guessing from the folder name.
- The raw Haystack event stream corroborates the rendered initial clean status and eight-character `git log` head. The `snapshot` 40-hex values in raw events are agent snapshot identifiers, **not repository checkout evidence**. `metadata.openai` is a compatibility metadata namespace, **not evidence this was an OpenAI model**.
- The conservative rendered-output scan finds 67 matching eight-character commit lines. This remains abbreviated corroboration, not a 300-task full-hash reset audit or full-hash uniqueness proof. The two independently fetched before-source samples below strengthen a bounded pilot, not the other 298 patches.
- All **300 detailed grader reports** parse and agree with the aggregate's 204 true / 96 false verdicts. These are the submitter's harness records, not independent re-evaluation.
- `logs/driver.log` records six rollout waves, separate agent-patch and gold grading, killed grader subprocesses and final collect-only passes. Preserve grader timeout/retry/post-rollout gold-validation provenance; do not count those as additional model attempts. The source claims problem-only prompts and model-endpoint-only networking; a driver HTTP probe is not a complete independent network/protocol audit.

### AiWork.Code: actual wire model agrees; reasoning setting is not constant

Path: `lite/aiwork-code/20260909-opus-4-8-xhigh`.

- All 300 predictions name `claude-opus-4-8`; **all 300 full raw-event trajectories record wire model `claude-opus-4-8`**. This is much stronger than a filename-only label, although still source-recorded, not provider-signed proof.
- The README advertises `reasoning_effort=xhigh`, but recorded adaptive-thinking rounds include **xhigh in 300 tasks, medium in 257, high in 121**. These counts overlap and are task-level presence, not independent attempts or deduplicated API-call counts. Preserve nominal setting **and** actual per-call adaptation; do not describe this as 300 constant-xhigh runs.
- Full-hash HEAD observations match only three inspected tasks: `stanford-crfm__helm-3467` (trajectory line **99**, `git log -1 --format="%H %s" HEAD` result), `run-llama__llama_deploy-356` (line **347**, `rev-parse HEAD` result), `jupyterlab__jupyter-ai-1022` (line **944**, HEAD/parent result). The JSON supplies the **complete confirmed three-entry dictionary** and task-specific locators; it does not fill the other 297 entries from HF metadata. The complete raw-event scan found no separate artifact-base field or full per-task repository/base header manifest.
- The README says submitted patches have overlapping gold-test edits stripped in six tasks and build/coverage artifacts stripped in seven; three resolved test-edit tasks were regraded. Measure the **submitted transformed patch**, not an assumed untouched raw rollout diff. No complete transformation-to-original-patch audit was performed.
- The seven grader errors and one empty-only timeout are not converted to failed attempts. No separate detailed grader reports are present in this run tree.
- Network isolation does not establish absence of future fixes in local Git objects. For example, the Jupyter trajectory itself labels a commit “gold” and investigates it; that label alone is not independently verified gold identity. This is a concrete contamination/protocol-review concern, not proof that every task used a gold solution or that recorded base HEAD is wrong.

### Slingshot: all available trajectories corroborated, but strongly sampled

Paths: `lite/sapient-slingshot-agent/v3.4.0/gpt-5.6-sol` and `multilang/js_ts/slingshot-agent/v3.4.0/gpt-5.6-sol/{js,ts}`.

- All 519 predictions use generic `model_name_or_path="SWE-Bench Agent"`. The three READMEs declare **Sapient Slingshot 3.4.0 / GPT-5.6-Sol** and one greedy rollout. Do not replace the model with the generic prediction label, or treat that label as independent GPT wire-model verification. No provider endpoint/model-version attestation was established.
- Every one of the **14 Python + 10 JS + 10 TS available trajectories** declares the matching candidate repository/base. All 34 also have successful full-hash checkout commands or full-hash HEAD outputs. The JSON includes **the complete confirmed dictionary for this available subset**, with the actual operations, not just a checksum of an unavailable private manifest. It is **not** a full-run 300/108/111 base dictionary.
- Twenty-nine trajectories have matching full-hash HEAD output; five others have successful checkout-to-exact-full-hash evidence. No separate artifact-base field was found in the available exports, and not every observation is a final artifact-time HEAD check. The exported transcript and submitted patch still need final-patch/before-source agreement review beyond the examples below.
- **All ten JS and all ten TS trajectory samples are explicit grader failures**, despite trajectory metadata saying `status: completed`. Python samples are nine successes / five failures. “Completed” means agent completion, not benchmark correctness; the samples cannot be used as representative outcome denominators or to establish bases for the unsampled successes.
- The entire available detailed grader export agrees with aggregate success/failure: **300 Python, 105 JS, 110 TS reports**. The three JS error IDs and one TS error ID lack detailed report files; keep the explicit aggregate error status, not inferred failure.
- Actual transcripts show macOS host paths, live GitHub clones, persistent memory and, in some files, sub-agent and future-commit inspection. These are concrete conflicts/concerns relative to the shared submission README's container-only protocol; do not certify compliance merely because a README says one rollout. A base match can still support static footprint provenance without establishing benchmark protocol comparability.
- `stdlib-js__stdlib-5735` initially discovers a parent/workspace Git repository (`b362e75…`) before correcting the checkout to `72d1412ee12e86641d68fc537f64a24350861611`. Do not take the first SHA anywhere in the transcript as the task's artifact base. Full context shows the correction.

## Independent before-source examples

One aggregate-labelled success and failure was checked for **each of the five exports**. Every existing old path in each selected patch was fetched at its exact candidate repository/full base; its complete byte stream was hashed and its Git blob SHA1 matched the patch's old-index prefix. **57 old-path comparisons across ten patch examples all match**. Added paths were not falsely fetched as existing files. This checks preimage compatibility; it does not apply/parse the patch, prove an entire historical checkout identity, or independently grade it.

| Export | Success example | Failure example | Existing old paths checked, success / failure |
|---|---|---|---:|
| TianxiCode Python | `deepset-ai__haystack-8489` | `aws-cloudformation__cfn-lint-3798` | 5 / 2 |
| AiWork Python | `deepset-ai__haystack-8489` | `aws-cloudformation__cfn-lint-3798` | 5 / 1 |
| Slingshot Python | `deepset-ai__haystack-8489` | `aws-cloudformation__cfn-lint-3798` | 8 / 17 |
| Slingshot JS | `sveltejs__svelte-16542` | `sveltejs__svelte-16666` | 15 / 1 |
| Slingshot TS | `owid__owid-grapher-5115` | `remotion-dev__remotion-5529` | 2 / 1 |

The JSON's `before_source_samples` contains the actual source URLs, complete byte SHA256/Git blob hashes and submitted-patch hashes. This is affirmative practical before-state evidence even for the two successful JS/TS examples that have no public Slingshot trajectory. A reviewer can approve an appropriately bounded, strictly applied/parsed static pilot on such evidence without falsely marking the original HF snapshot as verified. No full-run before-source audit is claimed.

### Source language labels also conflict

The immutable JS split contains `MultiQC__MultiQC-3242`, whose Slingshot patch changes Python (`multiqc/core/special_case_modules/custom_content.py`) and Python tests, not JS/TS. Keep the supplied JS population label and disclose excluded scope; do not silently move it to Python. JS-labelled patches can legitimately contain TypeScript, `.cts` or `.cjs` files; the JSON inventories all changed-path suffixes rather than applying an incomplete `.js`-only heuristic. Suffix inventory is not analyzer scope/measurement success.

## Licenses and output reuse: distinct layers

1. **Dataset / harness:** both pinned HF READMEs declare MIT. Benchmark code has an actual [MIT LICENSE at `microsoft/SWE-bench-Live@62d02936…`](https://raw.githubusercontent.com/microsoft/SWE-bench-Live/62d02936a0726fbf4597b05bd07b09fb99eddae6/LICENSE). Neither license automatically sublicenses every embedded issue, target source, contributor patch or trajectory.
2. **Target source:** nine repositories' license files were read at exact sampled task bases and hashed. Haystack/Lodestar: Apache-2.0; Svelte/OWID: MIT; cfn-lint: **MIT No Attribution (MIT-0)**, not ordinary MIT; privacyIDEA: AGPL-3.0 text; Pylint: GPL-2.0 text; MultiQC: GPL-3.0 text. GPL text alone does not establish “only” versus “or later” for every file. Preserve notices and review modified/vendored-file terms; this is **sampled rights coverage**, not clearance for all 519 tasks.
3. **Non-permissive example:** [Remotion's exact task-base `LICENSE.md`](https://raw.githubusercontent.com/remotion-dev/remotion/e6563480623e4e48d23a2fd6b8060cd46f1a01e0/LICENSE.md) is a custom, eligibility/use-case-limited license. It requires a company license outside its free-eligible group and forbids copying/modifying for selling/renting/licensing/relicensing/sublicensing one's derivative. Do not label the whole TS corpus MIT or acquire paid access as a workaround. Intended static-analysis/publication use needs separate review.
4. **Submitted outputs:** no root LICENSE or run-specific output redistribution/training grant was found in the complete pinned tree and inspected READMEs. Tianxi says the archive is kept for analysis/reproduction; that states purpose but does not expressly grant blanket downstream redistribution. Public downloads and required trajectory deposits are not a sublicense from submitters. This repository stores hashes/scalar provenance only, not source files, patches, prompts or rollouts.
5. **Provider contracts:** the fetched [Anthropic Commercial Terms](https://www.anthropic.com/legal/commercial-terms), effective June 17, 2025, assign Outputs to the **Customer** subject to compliance (section B); section D.4 restricts access to build competing products/services, including training competing AI models, or supporting third parties doing so. This does not assign rights to Parsimony; a negotiated customer contract may differ. Three official OpenAI terms endpoints returned **403**, and the DeepSeek terms fetch failed DNS resolution. Slingshot's provider/customer contract and Tianxi's routing/output contract remain unknown. Do not invent verified provider permission, infer it from a weight-model license, or mistake OpenAI-compatible event metadata for applicable OpenAI terms.

Static metric reporting, raw-patch redistribution and training/reuse of outputs are **different intended uses**. No blanket prohibition on publishing numerical benchmark metrics was established here, but neither publication nor artifact reuse is approved. Keep rights as `unverified-do-not-redistribute`; obtain/confirm the relevant terms before any downstream release. No upstream contact was made.

## Recommendations for the current `live.analyze_run` gate

This evidence is **not an approved `reviewed_manifest`**. Relevant inspected working-tree code: `parsimony/live.py:246–388` imports inventories; **`analyze_run`, `:391–432`**, checks review provenance/base/prediction bindings. The committed importer at audit start lacked plural-result/keyed-prediction support. Concurrent **uncommitted adapter work** now adds it; this research did not modify or test that implementation. The JSON records the inspected source-file hash. Validate those adapters against these actual payloads rather than hand-renaming files or running a new evaluation; line numbers can shift with that separate work.

- Normalize AiWork `resolved_ids` / `unresolved_ids` explicitly; retain seven errors and the empty-only record. Bind keyed prediction bytes as well as outcome bytes. Preserve model declaration versus raw alias/wire identity, nominal versus observed reasoning effort, selection/transformations, and grader retry metadata.
- Use the JSON's per-run `gate_binding_recommendation`: actual `submission_revision`, result **and prediction** SHA256, exact HF revision response/file hashes, and mapped **`files[]`** entries. `dataset_checksum` must hash the canonical imported `files[]` provenance list, **not just a Parquet file or concatenation of row bases**. Its aggregate is also stored as `dataset_file_sha256` by the current importer. If importing JS and TS together, recompute the aggregate over that exact ordered two-file list; the supplied single-track values are not interchangeable.
- Set `historical_dataset_match` to **`unverified`** while the original input manifest is unknown. Use only reviewed per-task operational confirmations, or an explicitly reviewed before-state corroboration alternative. Do not promote the full Tianxi declaration dictionary, candidate rows, abbreviated logs, arbitrary snapshot SHAs or agent `completed` status into confirmations.
- The gate requires confirmation for every **present explicit-success/failure candidate** in the selected language, not every error/empty/unselected row. A partial review can retain full denominators and mark all other patches `not_selected`. Today the strongest operational dictionaries cover **3 AiWork / 14 Slingshot Python / 10 Slingshot JS / 10 Slingshot TS** only. Before-source spot compatibility supports a proposed bounded pilot, not automatic full-run gate approval.
- Hash the **final approved immutable review bytes**, and supply a real commit-pinned review URL after approval. The current gate validates digest format and metadata bindings but **does not fetch/hash-check the review document, enforce `rights_status`, or verify protocol**. A syntactically acceptable manifest is not rights/protocol certification. Do not fabricate approval or use an arbitrary 64-hex value.
- Before broader measurement, independently validate remaining patch before-states (not necessarily discover an undeclared old HF SHA), final-patch/transcript agreement, licenses/terms, source scope and selection/protocol. Freeze separate Python/JS/TS Live populations; never append these records to existing DeepSWE/Verified panels.

Checks: five complete result/prediction ID equalities; three complete Parquet hash/decode checks; 300 Tianxi raw metadata/header/candidate and summary-record agreements; 300 separate-patch/prediction byte equalities; all 300 AiWork wire-model observations; all 34 available Slingshot base declarations and operational checks; 815 aggregate/detailed grader agreements; ten before-source examples / 57 matching old-file indexes. JSON/schema-count and whitespace checks were run. No analyzer or target tests were needed.
