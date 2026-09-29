# Expanded public SWE-bench Live artifact census

Audit date: **2026-09-29 (UTC)**. This is a public-artifact census and provenance review, **not a benchmark release or a model ranking**. No model API, paid evaluation, submitted/target code, target tests, or dataset commands were executed; no upstream contact was made. Only data downloads and static inspection were performed. Only this document and its [small evidence manifest](../examples/benchmark-discovery/expanded-live-census.json) are added to Parsimony.

## What the broader search adds

Fresh GitHub `main` still resolves to **`cba8a6d3197cd53da09f8527cccbc689782302a6`**, committed 2026-09-29T07:53:41Z: the same pin as the earlier bounded pilot, **not a newly changed submission revision**. The complete recursive tree was fetched: **25,507 entries, `truncated=false`**. All submission artifacts are covered by the inventory below; files outside its run directories are shared AMI documentation, images, and scripts, not additional model runs.

- **57 artifact-bearing run/track directories:** 13 Lite, 37 MultiLang, 7 Windows. Counting each paired JS/TS submission once gives **52 cross-track submission packages**, not 52 unique models or necessarily 52 distinct agent settings. Five JS/TS pairs account for the difference.
- **18 normalized, explicitly named model identities**, across **12 normalized scaffold families**. Brokk's two-model planner/code configurations are not new standalone models; its `Flash3` alias is retained without asserting a provider-specific model ID.
- **Five model names absent from both currently published Parsimony cohorts:** Seed-OSS-36B-Instruct, DeepSeek V3.1 Terminus, DeepSeek V4.1 Flash, Claude Sonnet 3.7, GPT-4.1. The last two were already investigated but excluded from the current Verified board; they are not newly released models. The first two are also older, not evidence of frontier recency. **DeepSeek V4.1 Flash is the clear recent new-model opportunity** (source-labelled run September 21–22, submission documentation September 28).
- GPT-5.5, GPT-5.6 Sol, Claude Opus 4.8, Gemini 3.6 Flash, etc. add newer-than-Verified coverage, but **are already present in DeepSWE**. Different scaffolds, budgets/reasoning settings, retry policies, benchmark populations, and agent versions are configurations/data, not additional unique models. Live contains no inspected GPT-6 Astra, Claude Opus 5, or other model later than those names merely because the census is fresh.

Comparison baseline: [DeepSWE fresh discovery](../examples/deepswe-python/refresh-2026-09-29.json), 26 usable configurations, and [current Verified cohort](../examples/mini-swe-agent-500/README.md), 33 published entries. Those are board/configuration denominators, not a promise of 59 different underlying model identities.

| Normalized model | DeepSWE published | Verified published | What Live adds |
|---|---|---|---|
| Seed-OSS-36B-Instruct | No | No | Older new-to-board identity; Lite partial run |
| DeepSeek V3.1 Terminus | No | No | Older new-to-board identity; MultiLang/Windows |
| DeepSeek V4.1 Flash | No | No | Recent new-to-board identity; TianxiCode Lite |
| Claude Sonnet 3.7 | No | No | Excluded Verified identity; historical Lite example |
| GPT-4.1 | No | No | Excluded Verified identity; historical Lite example |
| Qwen3-Coder-480B-A35B | No | Yes | Older OpenHands Lite data; different Lite population |
| Claude Opus 4.6 | No | Yes | AMI and Slingshot; retries/settings differ |
| Claude Sonnet 4.5 | No | Yes | Multiple scaffolds; also Brokk planner |
| Claude Haiku 4.5 | No | Yes | AMI Go retry configuration |
| GPT-5.2 | No | Yes | SWE-agent/ClaudeCode/Win-Agent medium; Brokk planner |
| Gemini 3 Flash | No | Yes | SWE-agent/Win-Agent; keep Brokk Flash3 alias unresolved |
| GPT-5.5 | Yes | No | Several scaffolds; medium/xhigh; success-only Slai |
| GPT-5.6 Sol | Yes | No | Slingshot 3.3.0/3.4.0; same model, new data/configs |
| Claude Opus 4.8 | Yes | No | AiWork.Code xhigh versus DeepSWE max |
| DeepSeek V4 Pro | Yes | No | Three MultiLang scaffolds plus Windows |
| Claude Sonnet 4.6 | Yes | No | AMI Go; targeted retries |
| Gemini 3.1 Pro Preview | Yes | No | AMI Go; up to 15 retry iterations |
| Gemini 3.6 Flash | Yes | No | AMI Go; up to 5 retry iterations |

## What was actually available and read

**Full read, not a sample:** all **53 aggregate result files** and **46 `preds.json` files** in the pinned tree were downloaded and parsed. Result lists contain **8,722 configuration/task ID records** (3,619 Lite; 5,027 MultiLang; 76 Windows), with **1,252 distinct task IDs across runs**. This counts the union of per-task ID lists inside each result file, including errors/incomplete/empty categories; the same task in different runs is a separate record. It does **not** count README headline denominators or turn logs as additional attempts.

The aggregate files explicitly list 3,586 success/resolved IDs, 4,676 failure/unresolved IDs, 349 empty-patch IDs, 115 error IDs and 17 incomplete IDs. **Do not sum these to derive a population:** there are 21 overlapping category memberships (20 in AMI Lite, one in OpenHands Qwen). Empty is an artifact category and may overlap evaluation categories. Counts are source-reported, not independently re-evaluated.

The prediction files contain **6,751 records / 6,493 nonempty patch strings**, including predictions without corresponding aggregate results. Those files' complete bytes were available; JSON parse and nonempty strings **do not establish valid diffs, strict application, or final-patch agreement with every separate patch file**. The complete tree additionally inventories 3,581 `patch.diff` files, 119 zero-byte; this is Git blob inventory, not a claim that all 3,581 were individually downloaded/applied. `.patch` and other layouts are additional artifacts already represented by their predictions, not extra attempts.

**Sampled final patch inspection:** 16 separate MultiLang diffs (one source success and one explicit failure in each of Go, JS, TS, Rust, Java, C, C++, C#) plus six embedded Python patches (success/failure for TianxiCode, MIT-IBM Seed-OSS, and Slingshot 3.4.0). Sample paths/checksums are in the JSON. **Full trajectory reads** were performed only for SWE-agent GPT-5.5 medium (all 224 present task trajectories) and TianxiCode DeepSeek V4.1 Flash (all 300 rendered trajectories). Other trajectories/protocols remain sampled or tree-inventoried. The four earlier Go/JS patches were already statically measured in the [pilot](swe-bench-live-investigation.md); this audit performs no new measurements.

### Full directory inventory

Paths below are relative to `submissions/` at the [pinned root](https://github.com/SWE-bench-Live/submission/tree/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions). `R` is the union of IDs in an actually read aggregate result, not `total_instances`; `S/F/Ø/E/I` are source success/failure/empty/error/incomplete ID-list sizes (0 means no IDs listed). `P/nonempty` counts the complete read prediction payload. `D/zero` counts separate `patch.diff` Git blobs and zero-byte blobs. `Match` is result-ID membership in the primary immutable HF candidate, not base verification. A second number after `→` uses the historical alternative/supplement described below, **membership only**.

#### lite

| Directory | R | S/F/Ø/E/I | P/nonempty | D/zero | Match |
|---|---:|---|---|---|---|
| `20250725-openhands-Qwen3-Coder-480B-A35B` | 300 | 74/217/0/9/1 | 300/299 | 299/0 | 125/300 → 300/300 |
| `20251221-MITIBM-agent-seedoss36b` | 291 | 60/211/0/20/0 | 291/291 | 243/0 | 291/291 |
| `Slai-Agent/gpt-5.5-xhigh` | 36 | 36/0/0/0/0 | 36/36 | 0/0 | 36/36 |
| `agav/gpt-5.5` | 300 | 186/85/29/0/0 | 300/271 | 0/0 | 300/300 |
| `aiwork-code/20260909-opus-4-8-xhigh` | 300 | 102/190/1/7/0 | 300/299 | 0/0 | 300/300 |
| `ami-agent/20260623-v0.7.0-claude-opus-4-6` | 300 | 189/110/10/10/1 | 300/290 | 0/0 | 300/300 |
| `sapient-slingshot-agent/v2.6.0/20260629-claude-4.5` | 293 | 36/254/0/3/0 | 293/293 | 0/0 | 293/293 |
| `sapient-slingshot-agent/v3.1.0/20260817-opus-4-6` | 299 | 75/190/0/34/0 | 299/299 | 0/0 | 299/299 |
| `sapient-slingshot-agent/v3.3.0/20260831-gpt-5.6-sol` | 300 | 134/164/0/2/0 | 300/300 | 0/0 | 300/300 |
| `sapient-slingshot-agent/v3.4.0/gpt-5.6-sol` | 300 | 211/89/0/0/0 | 300/300 | 0/0 | 300/300 |
| `sweagent/20250501-sweagent-claude37` | 300 | 53/201/39/1/6 | 294/255 | 255/0 | 300/300 |
| `sweagent/20250501-sweagent-gpt41` | 300 | 49/236/5/1/9 | 291/286 | 0/0 | 300/300 |
| `tianxicode/deepseek-flash` | 300 | 204/96/0/0/0 | 300/300 | 300/0 | 300/300 |

#### multilang

| Directory | R | S/F/Ø/E/I | P/nonempty | D/zero | Match |
|---|---:|---|---|---|---|
| `all_languages/claudecode/claude-4-5-sonnet` | 176 | 59/100/17/0/0 | 0/0 | 187/19 | 170/176 → 176/176 |
| `all_languages/claudecode/deepseek-v3.1-terminus` | 171 | 37/94/40/0/0 | 0/0 | 182/41 | 165/171 → 171/171 |
| `all_languages/claudecode/deepseek-v4-pro` | 240 | 67/118/55/0/0 | 240/185 | 226/41 | 240/240 |
| `all_languages/claudecode/gpt-5-2-medium` | 164 | 53/106/5/0/0 | 0/0 | 173/5 | 158/164 → 164/164 |
| `all_languages/claudecode/gpt-5.5-medium` | 240 | 90/135/15/0/0 | 240/225 | 226/1 | 240/240 |
| `all_languages/openhands/deepseek-v4-pro` | 232 | 76/156/0/0/0 | 0/0 | 240/8 | 232/232 |
| `all_languages/openhands/gpt-5.5-medium` | 235 | 95/140/0/0/0 | 0/0 | 239/4 | 235/235 |
| `all_languages/sweagent/claude-4-5-sonnet` | 165 | 49/54/62/0/0 | 0/0 | 102/0 | 159/165 → 165/165 |
| `all_languages/sweagent/deepseek-v3.1-terminus` | 160 | 40/114/6/0/0 | 0/0 | 148/0 | 154/160 → 160/160 |
| `all_languages/sweagent/deepseek-v4-pro` | 238 | 97/137/4/0/0 | 0/0 | 234/0 | 238/238 |
| `all_languages/sweagent/gemini-3-flash` | 165 | 47/106/12/0/0 | 0/0 | 148/0 | 159/165 → 165/165 |
| `all_languages/sweagent/gpt-5.2-medium` | 165 | 45/116/4/0/0 | 0/0 | 155/0 | 159/165 → 165/165 |
| `all_languages/sweagent/gpt-5.5-medium` | 230 | 105/120/5/0/0 | 0/0 | 224/0 | 230/230 |
| `cs/20260223-brokk-gpt52-flash3` | 20 | 9/6/5/0/0 | 20/15 | 0/0 | 20/20 |
| `cs/20260225-brokk-sonnet45-flash3` | 20 | 9/7/4/0/0 | 20/16 | 0/0 | 20/20 |
| `go/ami-agent/20260716-v0.7.0-claude-opus-4-6` | 138 | 103/35/0/0/0 | 138/138 | 0/0 | 138/138 |
| `go/ami-agent/20260723-v0.7.0-claude-sonnet-4-6` | 138 | 99/39/0/0/0 | 138/138 | 0/0 | 138/138 |
| `go/ami-agent/20260729-v0.7.0-claude-haiku-4-5` | 138 | 90/48/0/0/0 | 138/128 | 0/0 | 138/138 |
| `go/ami-agent/20260729-v0.7.0-gemini-3.1-pro-preview` | 130 | 72/58/0/0/0 | 138/130 | 0/0 | 130/130 |
| `go/ami-agent/20260729-v0.7.0-gemini-3.6-flash` | 130 | 78/52/0/0/0 | 138/130 | 0/0 | 130/130 |
| `java/ami-agent/20260817-v0.7.2-claude-opus-4-6` | 109 | 73/36/0/0/0 | 109/80 | 0/0 | 109/109 |
| `java/brokk-agent/20260218-brokk-gpt52-flash3` | 60 | 25/33/2/0/0 | 60/58 | 0/0 | 53/60 → 60/60 |
| `java/brokk-agent/20260218-brokk-sonnet4.5-flash3` | 60 | 23/34/3/0/0 | 60/57 | 0/0 | 53/60 → 60/60 |
| `java/slingshot-agent/20260707-sapient-slingshot-gpt-5.5` | 109 | 40/69/0/0/0 | 109/109 | 0/0 | 109/109 |
| `java/slingshot-agent/20260812-sapient-slingshot-gpt-5.5` | 109 | 45/64/0/0/0 | 109/109 | 0/0 | 109/109 |
| `java/slingshot-agent/20260901-sapient-slingshot-gpt-5.6-sol` | 160 | 84/76/0/0/0 | 160/160 | 0/0 | 160/160 |
| `js_ts/ami-agent/20260710-v0.7.0-claude-opus-4-6/js` | 93 | 60/33/0/0/0 | 93/86 | 0/0 | 93/93 |
| `js_ts/ami-agent/20260710-v0.7.0-claude-opus-4-6/ts` | 111 | 62/49/0/0/0 | 111/109 | 0/0 | 111/111 |
| `js_ts/slingshot-agent/20260623-slingshot-claude4.5/js` | 93 | 23/62/0/8/0 | 93/93 | 0/0 | 93/93 |
| `js_ts/slingshot-agent/20260623-slingshot-claude4.5/ts` | 107 | 28/77/0/2/0 | 107/107 | 0/0 | 107/107 |
| `js_ts/slingshot-agent/20260629-sapient-slingshot-gpt-5.5/js` | 93 | 31/58/0/4/0 | 93/93 | 0/0 | 93/93 |
| `js_ts/slingshot-agent/20260629-sapient-slingshot-gpt-5.5/ts` | 111 | 46/64/0/1/0 | 111/111 | 0/0 | 111/111 |
| `js_ts/slingshot-agent/20260730-sapient-slingshot-gpt-5.5/js` | 93 | 46/44/0/3/0 | 93/93 | 0/0 | 93/93 |
| `js_ts/slingshot-agent/20260730-sapient-slingshot-gpt-5.5/ts` | 111 | 52/59/0/0/0 | 111/111 | 0/0 | 111/111 |
| `js_ts/slingshot-agent/v3.4.0/gpt-5.6-sol/js` | 108 | 79/26/0/3/0 | 108/108 | 0/0 | 108/108 |
| `js_ts/slingshot-agent/v3.4.0/gpt-5.6-sol/ts` | 111 | 70/40/0/1/0 | 111/111 | 0/0 | 111/111 |
| `rust/ami-agent/20260625-v0.7.0-claude-opus-4-6` | 94 | 46/48/0/0/0 | 94/86 | 0/0 | 94/94 |

#### windows

| Directory | R | S/F/Ø/E/I | P/nonempty | D/zero | Match |
|---|---:|---|---|---|---|
| `Slai-Agent/gpt-5.5-xhigh` | 8 | 8/0/0/0/0 | 8/8 | 0/0 | 8/8 |
| `win-agent/claude-sonnet-4-5` | — | — | 37/34 | 0/0 | — |
| `win-agent/deepseek-v3.1-terminus` | — | — | 35/32 | 0/0 | — |
| `win-agent/deepseek-v4-pro` | 34 | 7/9/14/4/0 | 27/23 | 0/0 | 34/34 |
| `win-agent/gemini-3-flash` | — | — | 38/34 | 0/0 | — |
| `win-agent/gpt-5.2-medium` | — | — | 34/31 | 0/0 | — |
| `win-agent/gpt-5.5-medium` | 34 | 9/11/12/2/0 | 26/26 | 0/0 | 34/34 |


Four older Win-Agent folders have **144 prediction records (131 nonempty)** but no aggregate result file in the complete tree. Two sampled Windows rollouts were agent transcripts, not verified grader exports. Their reported agent test claims cannot supply benchmark correctness labels. The 144 are **not** added to the 8,722 result-record count.

## Immutable task membership: broader than the original 230-ID pilot

All ten primary Parquet files were downloaded directly using full SHA `resolve/` URLs, decoded with external `pyarrow==25.0.1`, and matched by exact `instance_id`. No dataset-server `revision` query was used as immutable evidence. File checksums, sizes, row counts, URLs and access timestamps are in the JSON.

- **Python Lite:** `SWE-bench-Live/SWE-bench-Live` at `b51a86422e10cfd403beb4773e5a2947953e36ec`, `data/lite-00000-of-00001.parquet`, **300 rows**. All result IDs in the twelve other Lite runs match. The July 2025 OpenHands Qwen run instead shares only **125/300 aggregate-listed IDs** (125/299 submitted IDs) with that candidate. Its historical July pin `6b7b42a273195d267e21f67bede59ebedd1d660c` has a **different 300-row Lite population and matches all 300 result-listed IDs / 300 predictions**. Do not compare these as the same frozen population. The May-example run names predate the HF repository's initial May 15 upload; names/dates alone do not bind their input.
- **MultiLang:** candidate `62dc0745c40f067fc366ae3eb1a26136e5928f85`, eight language files, **1,077 rows**: C 111, C++ 142, Go 138, JS 108, Rust 171, Java 160, TS 111, C# 136. All result IDs in the six newer all-language runs match, as do AMI and Slingshot single-language cohorts. Each of seven older all-language runs has **six missing SpotBugs IDs**; each Brokk Java run has **seven**. Directly read historical Java file at `3430730b50bba3ad11b40ca9ba5b224f4034ce1a` (December 29, 2025; **62 rows**) contains every missing SpotBugs ID and all **60/60** Brokk Java IDs. These historical IDs were removed from the candidate, not evidence of corrupt submissions. Finding them does not verify their run bases or justify composing arbitrary multi-revision rows as a coherent benchmark snapshot.
- **Windows:** `SWE-bench-Live/Windows` at `b9fa25f2732dbc2c93b9738b610d053d8b7bd7a9`, `data/test-00000-of-00001.parquet`, **66 rows**, not the README's older “Windows 61” denominator. Historical `ac8b120eaf36957da1884dde9f71fd28ed632487` (May 14) has **61 rows**; all 76 aggregate-listed records match both candidates. The four older prediction-only files also have complete ID membership in the current candidate. The two newer Win-Agent `preds.json` files each have four unmatched, first-character-truncated keys: `otnet__runtime-117105`, `otnet__runtime-117960`, `otnet__runtime-118745`, `OfficeAI__AionUi-2317`. Candidate tasks are spelled `dotnet__…` and `iOfficeAI__…`. Their correctly spelled result IDs are classified empty; the malformed prediction keys contain some nonempty patches. **Do not silently repair keys or override grading with those patches.** GPT-5.5 has 22 exact result-key patch strings / 34 result IDs; DeepSeek V4 Pro has 23 / 34 (20 nonempty).

Taken together, the directly read primary and historical files locate **every aggregate-listed ID in all 53 result files**, without fuzzy ID repair. This is complete **membership** coverage of inspected results, not complete historical input/base/evaluation provenance. Primary and historical HF commit-list responses were also inspected and checksummed.

## Historical bases can be confirmed without an explicit HF run revision

The prior [provenance audit](live-provenance-audit.md) correctly left the historical HF input unknown after four examples. **This broader audit materially improves that finding; it does not require an explicit HF revision when recorded task bases directly establish the relevant before-state.** The two questions must be separated:

1. Which HF snapshot/local task manifest was originally loaded? Still not declared for the SWE-agent cohort. Its trajectories actually name a local `swe_bench_datasets/multilang.jsonl_dev` input. An August upload cannot be assumed to have been a May run input.
2. Are the bases supplied by the immutable candidate the bases recorded in the historical run, for every task we could measure? **Yes for all potentially measurable supported-language tasks of this audited configuration.**

For `multilang/all_languages/sweagent/gpt-5.5-medium`, every one of the **224 present trajectories** contains exactly one distinct `Resetting repository testbed to commit <40-hex>` value, **224/224 exactly equal** to its candidate row's `base_commit`. Each names the corresponding task; the logs identify `azure/gpt-5.5-20260424` and begin May 28–June 1, 2026. Checks are based on task-specific reset lines, not an arbitrary occurrence of a SHA in issue text or a proposed patch. The JSON retains a checksum of the complete canonical per-task evidence manifest and per-sample file hashes; all pinned trajectories can be re-fetched to reconstruct it.

| Split | Submitted | Success | Failure | Empty-only | Present trajectory with matching base |
|---|---:|---:|---:|---:|---:|
| Go | 40 | 15 | 25 | 0 | **40/40** |
| JavaScript | 17 | 7 | 10 | 0 | **17/17** |
| TypeScript | 23 | 15 | 7 | 1 | **22/22 nonempty** |
| All eight splits | 230 | 105 | 120 | 5 | **224/230** |

The six absent trajectories/patches are `DynamoRIO__dynamorio-7561` (**C, explicit failure**) and five empty-only records: `redis__redis-14274` (C), `floci-io__floci-210` / `floci-io__floci-88` (Java), `can1357__oh-my-pi-489` (TS), `Automattic__harper-2973` (Rust). Thus **79/79 nonempty Go/JS/TS attempts have independently corroborated historical bases and patch blobs**, while all 80 supported-split result records, including the empty TS record, must remain in a frozen inventory. There is **not** complete 230-task artifact/base availability; the unsupported C failure is genuinely unavailable, not zero-size or newly inferred failure. Full patch-byte checks/application for the other 73 supported attempts remain to be done.

For the recent **TianxiCode / DeepSeek V4.1 Flash Python run**, all **300/300** rendered trajectory headers declare the repository/base pair matching the immutable Lite row. A conservative scan additionally finds matching **eight-character commit-log lines in 67/300** trajectories; these are corroboration candidates, not a blanket proof of the remaining checkouts (or of full-hash uniqueness). The two sampled histories explicitly show base/source metadata; the sampled Haystack trajectory also shows the initial `git log` output at the matching base. Keep **header declarations** separate from SWE-agent's stronger operational full-hash reset evidence. The other 233 would need operational/patch-before-source confirmation if requiring that stronger standard. The six Python sample hashes do not establish full historical bases for Seed-OSS or Slingshot.

Matching reset/declaration evidence authenticates neither benchmark grading nor raw-log honesty cryptographically, and does not settle selection/retry policies, issue-text changes, test-patch semantics, repository rights, or dataset snapshot identity. It can nonetheless satisfy the existing importer's **independent per-task base-confirmation alternative** for the 79 supported nonempty SWE-agent records after a reviewed evidence-bound manifest; the missing historical HF declaration alone need not block that bounded static import.

## Samples: real final diffs, including failures and unsupported tracks

| Track / result | Configuration or task | Example changed implementation |
|---|---|---|
| go / success | [twpayne__chezmoi-5016](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/twpayne__chezmoi-5016/patch.diff) | `internal/cmd/config.go` |
| go / failure | [kubernetes-sigs__controller-runtime-3494](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/kubernetes-sigs__controller-runtime-3494/patch.diff) | `pkg/cache/internal/informers.go` |
| js / success | [codeceptjs__CodeceptJS-5106](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/codeceptjs__CodeceptJS-5106/patch.diff) | `lib/helper/JSONResponse.js` |
| js / failure | [sveltejs__svelte-16666](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/sveltejs__svelte-16666/patch.diff) | `packages/svelte/src/compiler/phases/3-transform/client/transform-client.js` |
| ts / success | [kepano__defuddle-243](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/kepano__defuddle-243/patch.diff) | `src/markdown.ts` |
| ts / failure | [assistant-ui__assistant-ui-3866](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/assistant-ui__assistant-ui-3866/patch.diff) | `packages/react-langchain/src/index.ts` |
| rust / success | [ProvableHQ__leo-29291](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/ProvableHQ__leo-29291/patch.diff) | `crates/passes/src/const_propagation/ast.rs` |
| rust / failure | [gleam-lang__gleam-5510](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/gleam-lang__gleam-5510/patch.diff) | `compiler-core/src/format.rs` |
| java / success | [iflytek__skillhub-253](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/iflytek__skillhub-253/patch.diff) | `server/skillhub-domain/src/main/java/com/iflytek/skillhub/domain/skill/validation/BasicPrePublishValidator.java` |
| java / failure | [opendataloader-project__opendataloader-pdf-383](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/opendataloader-project__opendataloader-pdf-383/patch.diff) | `java/opendataloader-pdf-core/src/main/java/org/opendataloader/pdf/markdown/MarkdownGenerator.java` |
| c / success | [cilium__tetragon-4069](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/cilium__tetragon-4069/patch.diff) | `pkg/process/podinfo.go` |
| c / failure | [redis__redis-14243](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/redis__redis-14243/patch.diff) | `src/module.c` |
| cpp / success | [WasmEdge__WasmEdge-4772](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/WasmEdge__WasmEdge-4772/patch.diff) | `include/executor/executor.h` |
| cpp / failure | [WasmEdge__WasmEdge-4764](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/WasmEdge__WasmEdge-4764/patch.diff) | `lib/executor/engine/controlInstr.cpp` |
| cs / success | [quartznet__quartznet-2921](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/quartznet__quartznet-2921/patch.diff) | `src/Quartz/Impl/Triggers/DailyTimeIntervalTriggerImpl.cs` |
| cs / failure | [MudBlazor__MudBlazor-13063](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/MudBlazor__MudBlazor-13063/patch.diff) | `src/MudBlazor/Components/FileUpload/MudFileUpload.razor.cs` |
| python / success | [tianxicode/deepseek-flash / deepset-ai__haystack-8489](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/lite/tianxicode/deepseek-flash/preds.json) | `haystack/core/pipeline/pipeline.py` |
| python / failure | [tianxicode/deepseek-flash / aws-cloudformation__cfn-lint-3798](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/lite/tianxicode/deepseek-flash/preds.json) | `src/cfnlint/jsonschema/_keywords.py` |
| python / success | [20251221-MITIBM-agent-seedoss36b / amoffat__sh-744](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/lite/20251221-MITIBM-agent-seedoss36b/preds.json) | `sh.py` |
| python / failure | [20251221-MITIBM-agent-seedoss36b / aiogram__aiogram-1594](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/lite/20251221-MITIBM-agent-seedoss36b/preds.json) | `aiogram/fsm/context.py` |
| python / success | [sapient-slingshot-agent/v3.4.0/gpt-5.6-sol / reflex-dev__reflex-4129](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/lite/sapient-slingshot-agent/v3.4.0/gpt-5.6-sol/preds.json) | `reflex/istate/dynamic.py` |
| python / failure | [sapient-slingshot-agent/v3.4.0/gpt-5.6-sol / aws-cloudformation__cfn-lint-3798](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/lite/sapient-slingshot-agent/v3.4.0/gpt-5.6-sol/preds.json) | `src/cfnlint/jsonschema/_keywords.py` |


All eight MultiLang pairs are from the audited SWE-agent GPT-5.5 configuration; their source outcome is from its full result file and their full base reset matches the immutable row. Python examples are embedded final patches from the three named complete prediction files. Their provenance is sampled except for TianxiCode's full header scan. Samples are **not** denominators or proof of patch parseability. JavaScript examples include generated/log/test artifacts; established scope rules still apply. The **C-labelled `cilium__tetragon-4069` patch also changes Go/generated protobuf files**, illustrating why split labels and extension scope must be reviewed rather than inferred or silently reassigned. Rust, Java, C/C++, and C# remain inventory-only under current supported tracks.

## Selection/protocol findings that change feasibility

- **Slai Lite (36/36 successes) and Windows (8/8) explicitly are incremental success-only packages.** Their missing failed/unknown local attempts are deliberate. They are unsuitable as full all-attempt cohorts for Parsimony's default rankings; no artificial failure rows should fill their omissions. Lite also reclassifies 13 prior raw failures after a pytest XFAIL evaluator fix, without changing patches. Preserve evaluator semantics/version provenance.
- **AMI Go is targeted-retry data:** its READMEs disclose up to two retry iterations for Claude runs, **15** for Gemini 3.1 Pro and **5** for Gemini 3.6 Flash. AMI JS/TS says up to five infrastructure retry rounds; Java says two infrastructure iterations; Lite/Rust claim a single attempt. Do not label all these pass@1 just because there is one final prediction. The Go Gemini summaries have only **130 classified IDs / 138 predictions** each despite README denominator 138. All **16 omitted per-task records** were downloaded: the eight Gemini 3.1 records have `resolved=false`, zero elapsed/turns/test totals, empty exit reasons; the eight Gemini 3.6 records have `exitReason=timeout`, zero test totals and `resolved=false`. These are available detailed records, **not independently verified ordinary failures**. Retain placeholder/timeout/unknown semantics instead of taking the README's “unresolved” as eight additional graded failures.
- **AMI Java has 109 resolved/unresolved IDs and 109 predictions but only 78 `completed_ids`.** Reconcile this metadata inconsistency before selecting an outcome normalization. AMI Lite's empty/error lists overlap resolved/unresolved categories; OpenHands Qwen's incomplete/error membership also overlaps. A strict adapter must preserve source distinctions and disclose conflicts.
- AiWork.Code Opus 4.8, agav, Slingshot, Seed-OSS, and TianxiCode document single-rollout settings, but this census is not a full protocol-compliance audit. TianxiCode documents **grader-process timeout retries**, distinguishable from rerunning the model. MIT-IBM uses an orchestrator plus subagents on the same Seed-OSS model: new scaffold, not several new models.
- Brokk Java/C# combines GPT-5.2 or Sonnet 4.5 planning with `Flash3` coding and has external-trajectory pointers rather than raw local trajectories. External payload completeness/licensing was not audited. Do not attribute these mixed-model runs to GPT-5.2 alone.

## Concrete feasible next imports (no paid evaluation needed)

1. **First broaden the existing bounded Live static import to all 80 supported-split records for SWE-agent GPT-5.5 medium**, in separate Go (40), JS (17), TS (23) tracks. Preserve the one empty TS record and both successes/failures. Historical bases for all 79 potentially measured patches are now directly evidenced; prepare the reviewed checksum-bound provenance manifest rather than waiting for an explicit historical HF SHA. Download/verify the remaining supported patches, before-source files and licenses, then strictly apply/parse from a clean committed analyzer checkout. Do not publish a one-model score panel as a comparative ranking.
2. **Highest novel-model Python candidate: TianxiCode / DeepSeek V4.1 Flash.** 300 exact Lite IDs, 300 nonempty final predictions, 204 success / 96 explicit failure IDs, all 300 trajectory base declarations present. Complete operational/before-source confirmation and rights review, and add a narrowly validated `results.json` + keyed `preds.json` adapter; preserve recorded grading retries. Seed-OSS is the other genuinely new Python identity: 291 submitted/classified IDs and final predictions (60 success, 211 failure, 20 errors), not a complete 300-task run. It needs a partial-population policy and fuller provenance inspection.
3. **Add comparative same-model/configuration data, not pretend model novelty:** GPT-5.6 Sol Slingshot 3.4.0 provides 300 Python predictions/results (211 success / 89 failure) and 108 JS / 111 TS records; AiWork.Code Opus 4.8 has 300 Python records including one empty and seven errors. These are useful separate Live cohorts and new scaffolds/settings for models already on DeepSWE. Complete per-task bases and selection/terms review first. Newer ClaudeCode GPT-5.5 / DeepSeek V4 Pro have full 240-record prediction payloads and source results, making missing separate patch files recoverable **only after validating agreement/provenance**, not by marking them failures.
4. **Second Go/JS/TS references:** inspect SWE-agent DeepSeek V4 Pro (40 Go / 17 JS / 23 TS result IDs; 234 diffs globally) against every historical reset, then create a common task population independent of outcomes. AMI adds whole-language coverage (138 Go) and Claude Sonnet 4.6 / Gemini configurations but cannot be mixed indiscriminately with single-rollout cohorts. Old all-language model runs use different task selections and historical Java rows; broad intersection/selection review remains necessary.
5. **Defer Windows ranking, success-only Slai and unsupported-language measurement.** Win-Agent's four prediction-only runs need real grader records; the two newer runs need the truncated-key/empty-patch conflict reviewed; Windows populations changed from 61 to 66. Unsupported-language artifacts are public and often concrete, but adding parsers/rules is a separate versioned undertaking, not an import-switch change.

`parsimony/live.py` currently expects **`result.json` plus `<task>/patch.diff`** and strict `submitted/success/failure/empty/error` lists. Most Lite/AMI/Slingshot/Windows layouts are **not directly supported**: plural `results.json`, legacy `resolved_ids`, absent submitted lists, dict/list prediction payloads, partial outcomes, and retry metadata require explicit adapters and regression fixtures. No importer or analyzer code is modified here. Freeze new Live populations/panels; never append these records to the 0.5.2 Verified or existing DeepSWE boards.

## Rights and remaining limits

Pinned submission root has no `LICENSE` file; public access and mandatory trajectories are not a redistribution grant. Dataset metadata licenses do not automatically cover underlying project source, issues, model patches, or trajectories. Retain source links/hashes and obtain/confirm artifact-specific reuse/attribution terms before publishing raw data or a board. This repository stores only the census and small hashes/counts, not raw patches/rollouts.

Complete source-result/prediction availability is stronger than representative HTTP probes, but weaker than full static measurement, protocol/retry validation, or independent grading. Full base reset matching is established for one configuration only; other runs are not promoted by inference. Historical alternative membership is not proof of historical cohort binding. Strict patch validity, before-source retrieval, language/generated/test scope, undisclosed failures, all-agent common populations and full artifact rights remain open. All URLs/checksums/access times and exact counting definitions are in the companion JSON; raw research downloads remain outside the repository.

Checks: all **707 downloaded submission files** matched their pinned Git blob hashes; all 224 task-specific reset checks passed; all eight MultiLang file SHA256s agree with the earlier immutable audit. JSON parsing, census-count assertions, whitespace checks and `git diff --check` passed. No analyzer or target-code test run was needed for these documentation-only outputs.
