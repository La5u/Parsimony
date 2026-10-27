# Changelog

Analyzer versions change measurements. **Never pool or compare records from different analyzer versions**, and never relabel old records.

## Unreleased — SWE-PolyBench Verified Python board

**Data.** New board `site/polybench-python.html` (`examples/polybench-python/`): 5 model + agent setups on all 113 Python tasks of SWE-PolyBench Verified (`b3fca77`). Claude Opus 4.8 · HMigBot comes from the upstream submission branch (`e7062f4`); Opus 5.5 · AiWork.Code (PR 47), Opus 5.5 · Jitto Build (PR 46), GPT-5.6 Sol · Slingshot 3.4.0 (PR 44) and DeepSeek V4 Flash · Mobile Coder 1.2.4 (PR 40) come from open, unmerged submission pull requests pinned at their head commits (disclosed on the page). All were measured at `be4df4d` (0.10.0-beta, Python 3.14.7): 559/565 attempts; one before-state withheld, one analysis error, 4 empty patches (including AiWork's patch withdrawn after its leakage audit). Jitto Build's own README reports 129 of 294 resolved patches are near-copies of the reference fix. GPT-5.6 Sol · Slingshot ranks first at 0.65×. Every page's navigation and Sources list gain the board. **Importer.** `parsimony.polybench` reads PR heads (checking each descends from upstream `e7062f4`), records submitter task dispositions and audits touched-file before-states; GPT-5.4 stays withheld.

## Unreleased — Claude Opus 5.5 · AiWork.Code on Live Python (open network)

**Data.** Live Python gains Claude Opus 5.5 (xhigh) · AiWork.Code, from the open, unmerged SWE-bench-Live submission PR 60 pinned at its head `3602256`: 215/300 solved (submitter-run official harness), 287 attempts measured at the board's analyzer `de63300` (0.6.0-beta), 5 empty patches kept as unknown, all 295 nonempty patches matching old blobs and hunks. The run had open network access and could read upstream repositories, issues and fixes, unlike the board's GitHub-blocked Opus 4.8 run; it is labelled "(open network)" and the board notice and README say so. It ranks 5th of 5 at 1.33×; with a fifth peer, shared tasks rise from 73 to 92–158, and GPT-5.6 Sol · Slingshot (3rd) and Opus 4.8 · AiWork (4th) swap places.

## Unreleased — DeepSeek V4.1 Flash · TianxiCode on Live JavaScript and TypeScript

**Data.** Live JavaScript and Live TypeScript gain a sixth configuration, DeepSeek V4.1 Flash · TianxiCode 0.1.486, from the unmerged SWE-bench-Live/submission PR 64 pinned at its head commit `8275820`: JavaScript 58/108 solved (99 measured), TypeScript 56/111 (106 measured). It was measured with the boards' 0.10.0-beta analyzer at `4c02b61` and scored against the unchanged frozen panels. All 216 nonempty patches match their `trajs/*/patch.diff` copies, so no tasks are set aside; 3 incomplete tasks per board keep an unknown outcome. With a sixth peer, more tasks reach the three-peer gate, so JavaScript ranks shift (GPT-5.5 · Slingshot 3.0.0 moves from 3rd to 1st). **Importer.** `import_run` finds the combined JS/TS run's patches under `trajs/`; the driver splits the one run across the two boards.

## Unreleased — Chart shows each model line's newest generation

**Site.** The chart (scatter and bars) shows each model line's newest generation that has values on the current axes, so older generations no longer crowd it or stretch its axes. Hovering any point of a line shows that line's older generations, lighter and labelled. **Show older generations** under Change chart (`?older=1`) charts them all. The table, rank and measurements are unchanged. Page data gains `line` and `generation_rank` per model.

## Unreleased — Open-weight view filter

**Site.** Boards that have both open-weight and proprietary models gain a Weights control under Change chart: All models, Open weights, or Proprietary. It hides rows and points only. Rank, same-task ratios and measurements stay those of the full board; `?weights=open` and `?weights=closed` restore the view. gpt-oss counts as open-weight; Muse Spark, Qwen Plus and hosted Qwen Flash as proprietary; Qwen Max and unknown developers stay in the all-models view. No analyzer rules or measurements changed.

## Unreleased — Pairwise view of tasks both models solved

**Site.** Language boards gain **On tasks both solved**: pick two models to see mean net syntax units on the intersection of their solved, measured tasks (DeepSWE attempts averaged first), a ratio of sums, and the tasks with the largest absolute differences. Combined-language pages omit it. Rank, measurements and the three-peer ranking gate are unchanged. `?a=` and `?b=` restore the pair.

## Unreleased — DeepSWE 1.0 models on the index axes; Solved axis fits the data

**Site.** The 12 DeepSWE release 1.0 models added after the 2026-10-08 snapshot are now mapped (`aa-mapping.json`) in a new snapshot, `examples/external/artificial-analysis-2026-10-22.json`: 9 matched by model and reasoning effort; GLM-5.1, Kimi K2.6 and MiMo V2.5 Pro stay blank because their default runs don't record a thinking mode and Artificial Analysis lists both modes. All 35 earlier entries have identical values. The 2026-10-08 file stays, since the frozen Go release README cites it. The Solved axis now ends at the next 5% above the best model instead of 100%.

## Unreleased — Artificial Analysis indices on SWE-bench Verified

**Site.** The Verified board gets the Artificial Analysis Intelligence and Coding Index axes from a new pinned snapshot (`examples/external/artificial-analysis-2026-10-22-verified.json`, mapping `aa-mapping-verified.json`): 27 of 35 configurations matched by model and reasoning effort, read from each run's trajectory or submission metadata (older runs that set no effort use the provider default). Eight stay blank with a reason, e.g. GPT-5.2 (high), which Artificial Analysis lists only at Medium and Xhigh. As on DeepSWE, the index becomes the default Y axis and never affects rank. Boards with human-fix ratios now open the chart on net syntax units vs. the human fix (X) against the Intelligence Index, or Solved where there is no index; the table still sorts by rank. The DeepSWE snapshot (2026-10-08) is unchanged.

## Unreleased — Human-fix axis, metric explanations and chart export

**Site.** New chart axis "Net units vs. human fix, same tasks (×)" (`human_task_net`): a model's solved net units over the human reference fix's on the same tasks, as a ratio of sums with a task-bootstrap range, on boards with measured human fixes (DeepSWE Python/JavaScript/TypeScript/Go, Verified, self-runs); the DeepSWE all-languages page combines the per-language human-fix ratios the same way as its peer ratio. The task view shows the human fix's net units. Site labels renamed: net units → **net syntax units**, units changed → **churn**, complexity → **decision points** (field names unchanged). (i) buttons beside the axis selectors and table headers explain each metric. Measured (%) is no longer a chart axis (it stays a table column), churn is only an axis in the task view, and churn axes get no "better" zone. New "Download chart (PNG)" and "Copy image" buttons export the current chart with its labels and legend. Rank, measurements and existing ratios are unchanged.

## Unreleased — Current-ranking diagnostics and quiet coverage disclosures

**Diagnostics.** Add `python -m parsimony.diagnostics` and `scripts/diagnose-rankings.sh`: reproducible task/repository/peer omission checks, matched-task comparisons, denominator concentration, missing-success coverage and hashed inputs for each of the ten language boards. Reports live under `examples/ranking-diagnostics/`; they do not evaluate the combined-language aggregate. CI checks regenerated reports. **Site.** Add limitations to the existing collapsed help and success-coverage explanations to Measured-cell hover text, without new columns or controls. Rebuilt pages retain identical embedded ranking data. No analyzer rules or measurements changed.

## Unreleased — Audit documentation and offline rebuild disclosure

**Documentation.** Specify the website's same-task ratio, eligibility, weighting and conditional bootstrap ranges separately from the CLI leaderboard and archived score. Disclose the root-level Python exclusion and selection/missingness limitations; correct stale ranking and TODO descriptions. **Tooling.** Offline site rebuilds now explicitly report that DeepSWE Go and the combined front page are skipped, with an orchestration regression test. No analyzer rules, measurements, ranking calculations or generated pages changed.

## Unreleased — DeepSeek V4.1 Flash · TianxiCode on Live Go — 2026-10-17

**Data.** Live Go gains a seventh configuration: DeepSeek V4.1 Flash · TianxiCode 0.1.486 (submission pinned at `641b727`, added upstream 2026-10-16), 88/138 solved, measured with the same 0.10.0-beta analyzer at `9dd189a` as the other six. 24 tasks whose `trajs/*/patch.diff` differs from `preds.json` are set aside unmeasured; the panel frozen with the six AMI runs is unchanged and the new run is scored against it. **Importer.** `import_run` finds this run's separate patches under `trajs/`.

## Unreleased — DeepSWE release 1.0 models; ranking minimum — 2026-10-21

**Data.** The four DeepSWE boards gain 12 configurations from DeepSWE's gated release 1.0 archive (`datacurve/deep-swe-leaderboard` at `0618ccd`) for models absent from v1.1: Claude Haiku 4.5, Opus 4.6, Opus 4.7, Gemini 3 Flash Preview, GLM-5.1, GPT-5.4 mini, Grok Build 0.1, Kimi K2.6, MiMo V2.5 Pro, MiniMax M2.7, MiniMax M3, Qwen3.6 Plus, each measured at its board's analyzer commit with Python 3.14.7 and scored against the unchanged panels. Same task IDs and base commits; release 1.0 outcomes on four tasks whose v1.1 grading changed are unknown. Go's release asset is unchanged; the new Go records and reports live in `examples/deepswe-go-v2/release-1.0/`. **Site.** A model is ranked only with at least 15 shared solved tasks on a page, or half the page's tasks if fewer (DeepSWE JavaScript: 3 of 5); others are listed faded after the ranked models. Combined pages count shared tasks across languages.

## Unreleased — SWE-Milestone feature-work board — 2026-10-21

**Data.** New page `site/swe-milestone.html`: SWE-Milestone per-milestone trials (gated Hugging Face `DeepCommit-ai/SWE-Milestone-log` at `03d82b7`), 10 model + agent setups (Claude Code, Codex, Gemini CLI) on 60 milestones of feature work: Go 30 (go-zero, navidrome), TypeScript 18 (element-web), Python 12 (scikit-learn). Three language boards in `examples/swe-milestone-*`, combined by same-task ratios as on the front page. Measured with 0.10.0-beta at `feb9d04`. **Importer.** `parsimony.milestone` rebuilds each patch as the published source snapshot minus the milestone's start state (the HEAD of its digest-pinned image); files a snapshot lacks count as deleted only with evidence, and snapshots missing most source files are recorded as `partial_snapshot`, never zero.

## Unreleased — SWE-bench Live Go board — 2026-10-14

**Data.** New board `site/live-go.html`: six AMI Agent submissions to SWE-bench Live MultiLang Go (Claude Opus 4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1 Pro Preview, Gemini 3.6 Flash, Qwen3.8-27B) on all 138 tasks, measured with 0.10.0-beta at `9dd189a` and `tree-sitter-go-units-v2`. Retry settings differ by configuration and are disclosed. Separate from the DeepSWE Go board.

## Unreleased — SWE-bench Live JavaScript and TypeScript boards — 2026-10-14

**Data.** New boards `site/live-javascript.html` (108 tasks) and `site/live-typescript.html` (111 tasks): five public SWE-bench Live MultiLang submissions (Claude Opus 4.6 · AMI Agent, Claude Sonnet 4.5 · Slingshot 2.6.0, GPT-5.5 · Slingshot 2.6.0 and 3.0.0, GPT-5.6 Sol · Slingshot 3.4.0), submissions pinned at `99bae66`, dataset at `62dc074`, measured with 0.10.0-beta at `4c02b61` and the official TypeScript parser. Before-state audits in `examples/live-multilang/`. **Importer.** AMI result files without `completed_ids` are accepted when their counts match; the download cache rejects responses shorter than their Content-Length.

## Unreleased — Task difficulty and complexity on the site — 2026-10-14

**Ranking.** Boards now rank by code relative to the other models on the same solved tasks (`same-task-net-ratio-v1`), so solving only small tasks no longer looks parsimonious. The plain solved mean stays as a column. **Site.** New chart metrics: complexity added (solved mean) and both same-task ratios; the task view shows the task's typical solved patch. No measurements changed.

## Unreleased — SWEeper-Bench PHP board — 2026-10-13

**Data.** New board `site/sweeper-php.html`: 15 model + agent configurations from SWEeper-Bench (pinned Hugging Face tasks `0a4c5e2` and traces `15e41de`) on the 128 tasks whose reference fix changes PHP, measured with the 0.10.0-beta PHP track (`parsimony/sweeper.py`). 1,851 of 1,920 attempts measured; 8 uncertain or infrastructure-failed outcomes stay unknown. See `examples/sweeper-php/README.md`.

## Unreleased — GLM-5.1 on SWE-bench Verified — 2026-10-13

**Data.** The Verified board adds GLM-5.1 run with EvalScope (pinned Hugging Face export, uploader-reported outcomes), measured with the board's 0.5.2-beta analyzer: 491 of 494 nonempty patches, 363/500 solved, 6 empty patches kept as `no_generation`. The export stripped trailing whitespace, so 85 patches had their final blank context lines restored (checked against the base commit; counts recorded per record). The page names it as the only row not run with mini-SWE-agent. Reports: `coverage-35.json`, `scores-35.json`, `sensitivity-35.json`.

## 0.10.0-beta — PHP track — 2026-10-13

**Analyzer.** New PHP measurement track `tree-sitter-php-units-v1` (Tree-sitter 0.26.0 with `tree-sitter-php==0.25.1`, `.php`/`.phtml`). Named syntax nodes are units except wrappers, punctuation, comments, `<?php`/`?>` tags and inline HTML; `$name` and plain strings are one unit; operators and modifiers fold into their parent. Complexity adds functions, closures, branches, loops, catches, match arms, ternaries, `??` and short-circuit operators. PHPUnit `*Test.php` files plus the shared test/vendor/generated directories are out of scope. Python, JavaScript/TypeScript and Go unit definitions are unchanged. No board uses PHP yet; on GPT-6 Astra's 124 PHP patches from SWEeper-Bench (pinned `15e41de`), 118 measured, 3 had context that differs from the base commit, 2 base files do not parse as modern PHP and 1 was rename-only.

## Unreleased — simpler site, self-graded pilot and repository cleanup — 2026-10-13

**Site.** The Count attempts selector is removed. Boards rank by the mean net units added over measured solved attempts (`ranking_metric: measured-solved-net-mean-v1`, previously mislabelled `measured-net-mean-v1`); page data lists models in that order. The all-measured mean is a fixed second column and, with every other column, one of a single list of chart metrics; bars show the X metric. Task views list every attempt. Limits now state the solve-rate correlation (Spearman 0.33–0.60 on boards with 26+ models). Self-run models are self-graded in rebuilt task images (`examples/self-run/grade.py`) and show Solved and the solved-only mean.

**Repository.** `scripts/check.sh` and `scripts/rebuild-site.sh` replace the copy-pasted command blocks (CI uses the rebuild script). The README is a short overview with a worked example; the methodology and CLI reference moved to `docs/method.md`; dated investigations moved to `docs/archive/`; `examples/README.md` indexes current and historical data. Measurements and analyzer behaviour are unchanged.

## 0.9.0-beta — strict patch parsing, scoring/spec fixes and site cleanup — 2026-10-12

**Site.** Count attempts now defaults to Solved only on every board (`?attempts=all` selects All measured); the page template moved to `parsimony/template.html` so it is not deployed; proper page titles, canonical/Open Graph/Twitter metadata, an SVG favicon and `site/_headers` were added; chart point labels near the right edge flip left so mobile pages do not scroll sideways.

**Analyzer.** The shared patch parser now rejects malformed `@@` hunk headers, surplus `+`/`-` lines after a hunk and repeated sections for one implementation file (previously skipped or applied twice to the same base). The binary/rename guard checks repository paths without git's `a/`/`b/` prefixes, so top-level `testing/` and Django migrations-core paths follow the documented scope rules. Unit definitions are unchanged. All 20,621 published SWE-bench Verified (34 configurations) and Live (4) patches were re-fetched, matched their recorded SHA-256 and re-parsed: **no previously measured patch is newly rejected**; all 489 rejections were already analysis errors. The 1,000 Verified gold/test patches and 116 self-run patches also parse. Historical records keep their 0.8 identity; DeepSWE cohorts were not re-surveyed.

**Scoring (v0.5, now matching docs/archive/scoring.md section 6).** An explicitly empty failed patch (`empty_patch`) scores 0 instead of an unknown −25…100 bound; resolved records carrying failure/no-attempt categories are rejected; complete scores use the same arithmetic as their bounds (last-digit changes only). Regenerated `examples/live-python/scores.json` (GPT-5.5 agav bounds 21.6–40.4 → 24.0–30.7; Claude Opus 4.8 7.9–16.5 → 8.0–16.1; order unchanged) and `examples/ten-model-scores.json` (two last-digit changes). Other historical score files are kept; they reproduce to within 1e-14. Bootstrap CIs (site, sensitivity, stability) now use interpolated quantiles instead of index flooring, so page CIs shift slightly. `sensitivity` scores no-attempt/empty records as 0 instead of failing.

**Leaderboard CLI.** Out-of-scope successes (every touched file excluded) and unparsed records no longer enter medians or the `--shared` set as zero footprints, matching scoring and the site.

**Security.** Workflow-dispatch input is passed via the environment, not interpolated into shell; actions are pinned to commit SHAs. Downloads are capped (1 GiB); contributed bundle URLs must be public HTTPS hosts (no IP literals, localhost or credentials); snapshot restore bounds manifest/entry/total sizes before reading. The Node parser's stderr goes to a temporary file rather than an undrained pipe. `release audit` rejects mixed analyzer source hashes; `freeze` runs git in the Parsimony checkout. Site links pass a scheme allowlist.

**Website.** Removed the archived combined-score, CI and rank-bound axis options. Leaderboard headers and model names wrap so the table fits the page (and a 390px phone). Hovering or focusing a scatter point draws dashed lines to the same company's same-version models (e.g. GPT-6 Sol ↔ Astra ↔ Luna, not 6.1). Empty patches show as such in task views. The Go page's report link no longer points at a local path (`site --sensitivity-report`). CI rebuilds the five offline pages and compares them byte-for-byte.

## 0.8.0-beta — source-pinned Go grammar and versioned EOF policy

Go now uses `tree-sitter-go-units-v2`: Tree-sitter 0.26.0 plus immutable upstream PR #190 source (URL/SHA256 checked via installed archive metadata), and an explicit parsing-only final-LF policy. Stock grammar 0.25.0 is not accepted for v2 despite the source package retaining that version. Strict syntax-error rejection remains. An initial PR #193 candidate was rejected after full-cohort testing exposed a shadowed-`new` regression.

Remeasured **26 configurations × 136 slots = 3,536 records** at clean `34d59ca`, Python 3.14.7, on the byte-identical frozen Go dataset and checksum-bound patches/outcomes/preimages. **Six parser-limited attempts recovered; one genuinely invalid Helm patch remains unmeasured.** All 3,502 common primary footprints and human net/churn values agree. Three structural-churn diagnostics change by +2; they do not set rank. All outcome/provenance bindings are unchanged, as are the historical Go artifacts.

New named population, coverage, archived panel/scores/stability and Go page are published separately. Large scalar files are in the checksummed `deepswe-go-v0.8` release asset; raw source/patches are excluded. Other boards' measurements remain unchanged; Sources metadata links to the new Go manifest. See [Go release details](docs/go-parser-v2-release.md) and [release README](examples/deepswe-go-v2/README.md).

## Website and maintenance — solved-only option and repository audit

All six boards retain All measured as default and offer Count attempts: Solved only (`?attempts=solved`), updating footprint rank, means, coverage and task/chart views consistently. Failed/unknown attempts and ungraded self-runs are excluded in that view; upstream Solved %, external indices and archived diagnostics remain independent. Missing measurements are never zero-filled. Keyboard focus, tooltip dismissal, HTML structure and no-JavaScript behavior have regression coverage.

Repository maintenance fixed iterator consumption, resume evidence loss, malformed input/provenance validation, parser-worker lifecycle, cache/snapshot inefficiencies and external-index redirect/size risks. Repeated task attempts remain clustered in sensitivity resampling. Expanded adversarial tests demonstrate compact validation removal and helper delegation; footprint does not certify maintainability. See [repository audit](docs/archive/repository-audit.md), [site audit](docs/archive/site-audit.md) and [adversarial validation](docs/adversarial-validation.md).

## Discovery: 12 more fresh-code configurations; Seed-OSS conflict — 2026-10-07

Expanded the NONPUBLISHED LiveCodeBench pilot from six to **18 configurations**, adding GPT-4o, o3/o4-mini High, Grok 3 Mini High, Llama 3.3, Mistral Large, Codestral, QwQ, Qwen 2.5 Coder, DeepSeek V3 and Claude 4 Thinking variants. Clean `cbe8768` measured only new checksum-bound inputs; original six exports/metadata remain unchanged. Total **17,353 measurements / 18,990 retained task-attempt slots**; explicit missing states comprise 1,209 absent tasks, 43 absent code lists, 318 empty bodies and 67 parse errors. Exact subset-export bindings preserve the full frozen population; unknown outcomes stay unknown, with observed solve-fraction bounds. No board or model-quality ranking is implied.

Deeper Seed-OSS Live auditing found substantial rollout/prediction patch conflicts, so its footprint release is withheld despite usable touched-file preimages. A bounded BigCodeBench search still lacks exact paired per-task outcomes; the official requests dataset is access-restricted. Added four regression tests (269 total with pinned parsers). See `examples/livecodebench-pilot/README.md` and `docs/archive/seedoss-live-candidate-review.md`. No target code, model APIs or paid evaluations ran; existing website boards are unchanged.

## Discovery: LiveCodeBench static feasibility pilot — 2026-10-07

Bounded source refreshes confirm unchanged Verified, Live, PolyBench and complete DeepSWE metadata. Existing blockers remain: missing Codex outcomes, no Astra declared patches, sampled Gemini 3.8 HTTP 403s. Body-level discovery verified six LiveCodeBench exports with common 1,055-task membership and paired code/outcomes; all 327 BigCodeBench sample exports lack paired outcomes.

A checksum-bound **NONPUBLISHED** complete-file Python pilot freezes sample index 0 and all exported tasks. Clean `2645271` / Python 3.14.7 measured 6,263/6,330 attempts, retaining 24 empty bodies and 43 parse errors as null footprints. It uses existing docstring-free coding units including EndBlock; raw code and scalar rows remain external. Summary/hash metadata, frozen population and reproduction driver are committed. No target code, evaluations or model calls ran. No seventh website board or new frontier-model claim: dataset/provenance/configuration release review remains pending. Existing website records, rankings and scores are unchanged. Twelve regression tests added; 265 pinned-parser tests and all six Node page checks pass. See `examples/livecodebench-pilot/README.md` and `docs/archive/new-model-discovery.md`.

## Battery: Gemini 3.5 Flash added to Verified — 2026-10-02

Fresh public listings confirm unchanged Live, PolyBench and Verified pins; DeepSWE leaderboard/release hashes are unchanged, but the full trials/config refresh timed out. The candidate census records that limitation rather than claiming fresh patch availability.

Verified expands from 33 to **34 configurations** with source-reported Gemini 3.5 Flash / mini-SWE-agent 2.4.2. Pinned artifact commit `2f6637a` supplies 441 predictions that agree byte-for-byte with separate patch files: 359 passing and 82 failed. Aggregate outcomes explicitly identify the other 59 tasks as no generation; all 500 remain in the population, with no missing-zero imputation. Static analysis measured all 441 submitted attempts using clean `0aa66df`, Python 3.14.7 and the identical existing 0.5.2 source hash; mean net units added is +36.6031746031746. No model calls or target tests ran. Human-reference comparison is intentionally uncomputed for this addition.

The importer honors immutable `info.commit` behind explicit assets pins; a tested reproduction driver checksum-binds inventory, population metadata and numerical/hash evidence, and launches the pinned clean analyzer. Raw artifacts remain external; publication is not blanket reuse/licensing or evaluator/model certification. Existing 33-model measurements, population/panel and reports are unchanged; new 34-configuration reports and the Verified page are published separately. See `docs/archive/gemini-3.5-verified-release.md`.

## Website: plain-mean ranking and solved-only mean column — 2026-10-01

At the owner's request the 10% trimmed mean is removed. Boards rank by the plain mean of net units added over all measured attempts again (`measured-net-mean-v1`), and a new sortable column and chart metric shows the mean over upstream-solved attempts only (`measured_solved_net_mean`, with `measured_solved_attempts`). Rank stays on the all-attempt mean. Measurements and scores are unchanged.

## Website: newest-generation emphasis, name labels and better-corner zone — 2026-10-01

The comparison chart now draws each model line's newest generation at full color with a permanent name label, fades earlier generations, and shades the corner that is better on both axes in green (top-left by default: smaller footprint, more solved). The chart is taller to fit labels. `site.py` adds a `latest` flag per model (highest version within its model line); rank, table, measurements and scores are unchanged. Hover tooltips still work for every point.

## 0.7.0-beta — JavaScript/TypeScript measured with the official TypeScript parser — 2026-10-01

**Measurement revision for the JavaScript and TypeScript tracks.** Python and Go measurements are unchanged.

- `tree-sitter-typescript==0.23.2` is unmaintained upstream and rejected valid modern TypeScript. A replay of all 323 TypeScript analysis errors, checked against the official TypeScript parser, found 319 valid files (261 of them unmodified base files), 3 invalid patches and 1 unsupported diff ([investigation](docs/archive/typescript-parser-investigation.md)).
- JavaScript and TypeScript now use `typescript@5.9.3` (pinned in `package.json`/`package-lock.json`, installed with `npm ci`) through a long-lived Node worker, `parsimony/typescript_units.cjs`. It parses syntax only; any syntax diagnostic, including TypeScript-only syntax in a JavaScript file, remains an explicit analysis error that now names the file and line. New unit track `typescript-compiler-units-v1`; raw counts are not comparable with `tree-sitter-units-v1`. Go keeps Tree-sitter, and its track identity now lists only the Go pins. The worker is part of the analyzer source hash.
- Remeasured all 26 DeepSWE configurations from clean commit `ca37c31` against the unchanged datasets: TypeScript errors 323 → 5 of 3,640, calibratable tasks 31 → 33 of 35; JavaScript 520 of 520 measured. No previously measured record fails; upstream outcomes and patch hashes are identical; old and new net units correlate at 0.999. New populations, coverage audits, panels (`…-v0.7`), scores, stability reports and both pages were rebuilt together. The 0.6.0 records were replaced in place and were last present at commit `ca37c31`.
- The `languages` extra now installs only `tree-sitter` and `tree-sitter-go`. CI installs Node 22 and runs `npm ci`.

## Website: trimmed-mean footprint ranking — 2026-10-01

All six boards now rank by a **10% trimmed mean** of net coding units added (`measured-net-trimmed-mean-10-v1`): each model drops floor(n × 5%) measured attempts at each end, so the plain mean is used below 20 attempts. Passing and failed attempts still both count, there is still no correctness tie-break, and there is no coverage gate. Under the plain mean a few failed mass deletions decided rank; on Verified, Llama 4 Maverick ranked first at −244 against a median of +4. The plain mean stays in page data (`measured_net_mean`) and as a graph metric. No measurement, score, CI or task cell changed; only model order and the new field did. Verified and DeepSWE orders shift slightly. On Live, Claude Opus 4.8 · AiWork moves to first.

## Website: footprint-only default ranking — 2026-09-30

At the owner's request, all six boards now rank by mean net coding units added, lowest first. Passing and failed measured attempts count, including population items outside the old passing-reference score panel. Upstream Solved % and explicit measured/population coverage are context only. Primary columns are Rank, Model, Net units added, Solved, Measured; missing means remain unranked and ties share rank. Task views use net footprint without correctness weighting. The 80/20 calculator, scores, CI and score-rank data remain unchanged as clearly labelled archived optional diagnostics, never footprint ranks. No raw measurement or outcome was changed; no target/model evaluation was performed.

## Website: final Live Lite Python board — 2026-09-30

Published one separate `site/live.html` board with DeepSeek V4.1 Flash / TianxiCode, GPT-5.6 Sol / Slingshot and Claude Opus 4.8 / AiWork. All 300 predefined tasks remain, including explicit failures and missing/out-of-scope data. An opt-in frozen-population calibration policy assigns conservative bounds when passing references are absent; unchanged 80/20 point formulas and no fabricated references/zero penalties. Rank intervals include missing-data envelopes within paired task bootstrap resamples. Known failed footprints remain in the net-unit mean even when uncalibrated. Original measurement JSONLs/identities are unchanged; numerical metadata only, no raw code/patches. Existing five boards' embedded measurements/scores are identical apart from navigation. Same clean layout and columns; no separate preview, no dedicated CI column. 218 tests pass with optional parsers, stdlib-only 16 skips; all six Node checks and both score reproductions pass.

## DeepSeek V4.1 targeted release review — 2026-09-30

Freshly checked 900 pinned patch/metadata/grader files: all 300 DeepSeek tasks agree. Retrieved/read both official DeepSeek terms pages; numerical previews are distinct from uncleared raw artifact reuse. Corrected coverage reporting: 295 static analyses include eight fully out-of-scope patches, leaving 287 eligible footprints (202 successful, 85 failed). Existing scorer already excludes these; no measurements/formulas changed. Current Live Python reference pool covers 238/300 tasks, so no solved-subset default ranking or fabricated full-population score is published. Evidence and review are committed; existing pages remain unchanged.

## Recent-model clean static measurement audit — 2026-09-30

Measured six supported cohorts from clean commit `de63300`, retaining complete populations and explicit failures: DeepSeek V4.1 Flash, GPT-5.6 Sol Python/JS/TS, Live Opus 4.8 and PolyBench Opus 4.8 Python. Published hash/coverage metadata only under `examples/priority-live/`; no new ranking/per-task footprint release pending rights/protocol/reference review. GPT-5.4 PolyBench has 112 generated patches with strict hunk compatibility but no old-blob identity; measurements remain gated. Existing boards and 80/20 scoring are unchanged.

## Recent-model static import tooling — 2026-09-30

- Extended Live import to plural results/keyed predictions, complete predefined language populations, reviewed offline analysis and checksum-bound preimage exceptions. Unknown/error/empty/incomplete are not inferred failures.
- Added immutable SWE-PolyBench candidate imports, full placeholder/result inventory and cache-only analysis; historical grading/rights/model attestations remain unverified.
- Added Git old-blob-prefix + strict-hunk auditing and a clean-checkout priority reproduction driver. Full five-cohort preimage audit corroborates 1,094 old-file patches plus two new-file-only patches; 11 exceptions remain unmeasured. No scoring formula/parser pins changed.
- Added research-preview site metadata that discloses mixed harnesses and unresolved historical provenance; not a certification gate bypass.

## Website: remove dedicated 95% CI column

Removed the confidence-interval column from all five boards. CI calculations, graph-axis endpoints and rank ranges remain; embedded data, measurements and scores are unchanged. The remaining numeric columns retain click-to-sort behavior.

## Import/discovery tooling — 2026-09-29

- Added `python -m parsimony.live` for immutable SWE-bench Live run inventories, explicitly mapped multi-file datasets (optional lazy Parquet support), checksums, complete submitted-record retention and evidence-gated offline analysis. Error, missing, empty-only and explicitly failed outcomes stay distinct. This is not a new published board.
- Verified imports can follow submitter-hosted GitHub `assets.repo` predictions/logs and declared refs, retaining official S3 support. Missing reports remain unknown; explicit applied-patch failure reports are imported separately.
- Fresh DeepSWE discovery still has 26 usable configurations and unchanged metadata checksums. Verified/Live/Pro V2/Atlas discovery evidence and publication blockers are documented under `docs/` and `examples/benchmark-discovery/`. Published parser pins, measurements, scoring and pages are unchanged.

## Website: data-fitted scatterplot axes

Numeric axes now use the visible points' minimum and maximum with 5% padding, rather than forcing zero. Solved percentage retains its 0–100% scale. Single/equal values and empty views have safe nonzero ranges; regression checks cover positive, negative, zero and missing values. Scores and measurements are unchanged.

## Website: light mode and immediate model tooltips

All boards now stay in light mode regardless of system theme. Model points show only the model name in an immediate custom hover/focus/tap tooltip, without the delayed native SVG tooltip. CI independence is explicit in the UI and tested: changing bootstrap confidence intervals cannot change Score or its default ordering. No scores or measurements changed.

## Website: selectable comparison axes

Removed Per solve and Median churn from the website, including selected-task views. Net units added is the sole raw footprint column (mean over measured passing/failed attempts in the all-task view). Users can choose any two numeric table values for the company-colored scatterplot; CI/rank endpoints are labeled explicitly. Default: net units versus solved percentage. The page explains the existing 80/20 all-task score, which remains unchanged.

## Website: model and company comparison

The scatterplot now explicitly compares models, using consistent developer-company colors and a legend across all boards. Points average measured, in-scope passing **and failed** attempts, rather than only solves. Hover/focus/tap labels expose model, company and measurement coverage. The all-task scoring formula and rankings are unchanged.

## Website and results — 2026-09-28

- One sortable board defaults to all score-panel tasks; the task-ID selector changes that same board instead of opening a second table. A responsive scatterplot shows mean net coding units added against mean churn per measured solve, or individual measured passing/failed attempts for the selected task. Conditional means are diagnostics; default ranking remains the all-task score. Coverage exclusions and the resolve-rate denominator are disclosed.
- Added separate 26-model DeepSWE JavaScript, TypeScript and Go boards: 7,696 attempt records over 74 additional task definitions, measured from clean commit `7705e8d`. All 5 JS and 34 Go tasks calibrate; 31 of 35 TS tasks calibrate. Known TypeScript grammar gaps and two upstream task-language mismatches remain explicit missingness, not zeros or model failures. Records and audits retain all attempts.

## 0.6.0-beta — 2026-09-28

Optional JavaScript/JSX, TypeScript/TSX and Go analysis uses pinned Tree-sitter grammars, syntax-unit traversal and the existing unit-diff machinery. Python measurements keep their AST implementation. Non-Python datasets require full-file analysis and carry a language/unit/parser-version track; panel creation, scoring, sensitivity and coverage reject mixed tracks. Failed attempts are still measured and penalized. No target code is executed. See [language tracks](docs/language-tracks.md).

Fresh DeepSWE v1.1 discovery found the same 26 usable configurations and identical run-index checksum. Gemini 3.8 patch probes still return 403; GPT-6 Astra runs declare no patches. No invented or relabeled results were added. [Refresh evidence](examples/deepswe-python/refresh-2026-09-28.json).

[SWE-Atlas Refactoring investigation](docs/archive/swe-atlas-investigation.md) found newer-model aggregate scores and public reference patches, but no public per-attempt model patch/result archive; importing its model runs is blocked on artifact access.

## Results: DeepSWE, 26 current models — 2026-09-27

New importer `python -m parsimony.deepswe` for [DeepSWE](https://deepswe.datacurve.ai), a 2026 benchmark that runs every model with mini-SWE-agent four times per task and publishes each run's patch and pass/fail. [examples/deepswe-python](examples/deepswe-python/README.md) measures its 34 Python tasks for 26 current models (Claude Opus 5, Fable 5, GPT-5.6, Kimi K3, GLM-5.3, DeepSeek V4, Grok 4.6, …) and is now the site's main board; the SWE-bench Verified board moves to `site/verified.html`.

Each attempt is an item (`task#attempt`) scored against every passing patch of its task; the stability analysis and the site resample the attempts of a task together, which leaves results with one item per task unchanged. The site builder gains `--benchmark` and `--nav`. Measurement and scoring are unchanged.

## Results: 33 models × 500 tasks — 2026-09-27

[examples/mini-swe-agent-500](examples/mini-swe-agent-500/README.md) replaces the ten-model results as the site's data: 33 models run by SWE-bench with mini-SWE-agent v0.0.0–v2.0.0, measured with analyzer 0.5.2 and scored against a new panel frozen from all 33 (`mini-swe-agent-33-448-solved-80-20-v0.5`). Five models run under two agent versions show that the version alone moves a score by up to 5.6 points.

The stability analysis and the site now compare models over all tasks (an unscored task counts at the middle of its bounds; intervals and distinguishability use its best and worst case) instead of only the tasks where every model has a point score, which fell to 70 of 448 with 33 models. The site shows each model's 95% bootstrap rank range instead of tiers. Scoring is unchanged.

## 0.5.2-beta — 2026-09-27

Two fixes for older published mini-SWE-agent runs (July–August 2025):

- **A patch file missing its final newline is repaired, not rejected.** git ends every diff with a newline (a file without one gets a `\ No newline` marker), but these runs stored patches with it stripped. That turned a trailing blank context line into an empty line without a newline, so most of their patches failed with "patch context differs from base commit" (for example 244 of o3's 292 solved patches). Records now carry `provenance.patch_final_newline_restored`.
- **Patches are found when `metadata.yaml` names a folder that does not exist.** For four runs it points to another run's folder, uses different letter case, or omits `/logs`. When the named S3 folder has no per-task folders, the analyzer uses the bucket's standard `bash-only/<submission>/logs` folder and records `provenance.logs_source`.
- **New files at the repository root are excluded as scratch scripts.** Before mini-SWE-agent v2.0.0, submitted patches kept the scripts agents write while working (`reproduce_issue.py`, `comprehensive_test.py`, …): up to 94% of a model's solved patches, against none under v2.0.0, which drops them. Library code lives in packages and no maintainer fix in SWE-bench Verified adds a root-level file. Edits to existing root-level files still count.

## Results: Claude Opus 4.5 added to ten models × 500 tasks — 2026-09-26

Results only; no measurement or scoring change. Claude Opus 4.5 (high) (`20260217_mini-v2.0.0_claude-4-5-opus-high`) was measured with the same analyzer commit (`b2316a9`, 0.5.0-beta) and Python 3.14.7, and scored against the unchanged ten-model panel without becoming a reference; the ten original scores do not change. It ranks first (≈52.3). GPT-5.2 Codex and Gemini 3 Pro (high) are left out because their published per-task results are missing or mark every task unresolved. See [the example README](examples/ten-model-500/README.md#newcomers).

## Scoring parsimony-80-20-v0.5 — 2026-09-26

Scoring change only: **80% net units / 20% churn** replaces 70/30, for both the success percentile blend and the failure burden. The analyzer (0.5.1-beta) and every measurement are unchanged. All results were re-scored offline from the committed JSONL. The panels were refrozen under new names (`ten-model-ten-task-80-20-v0.5`, `ten-model-439-solved-80-20-v0.5`) with the same tasks and references. The sensitivity grid now uses 0.8 as the baseline and keeps 0.5, 0.7 and 1.0 as alternatives.

The ten models × 500 tasks leaderboard keeps the same order. Scores move by about 0.3 points at most:

| Rank | Model | Score 70/30 | Score 80/20 | Per solve 70/30 | Per solve 80/20 |
|---:|---|---:|---:|---:|---:|
| 1 | Claude Opus 4.6 | 49.1 | 49.1 | 58.4 | 58.3 |
| 2 | MiniMax M2.5 (high) | 47.9–48.1 | 47.8–48.0 | 57.0 | 56.8 |
| 3 | Kimi K2.5 (high) | 44.5 | 44.4–44.5 | 57.4 | 57.3 |
| 4 | Gemini 3 Flash (high) | 43.8 | 44.1 | 52.4 | 52.8 |
| 5 | GLM-5 (high) | 42.4 | 42.4 | 53.1 | 53.0 |
| 6 | Claude Sonnet 4.5 (high) | 39.3 | 39.2–39.3 | 50.9 | 50.8 |
| 7 | Claude Haiku 4.5 (high) | 35.5 | 35.4 | 50.7 | 50.4 |
| 8 | DeepSeek V3.2 (high) | 29.8–30.0 | 30.0–30.2 | 40.9 | 41.0 |
| 9 | GPT-5.2 (high) | 28.4 | 28.7 | 37.1 | 37.4 |
| 10 | GPT-5 mini | 25.2–25.8 | 25.2–25.8 | 45.2 | 45.1 |

Opus is now first in 66% of bootstrap resamples (was 64%) and MiniMax in 34% (was 36%). The 10-task sample also keeps its order.

## 0.5.1-beta — 2026-09-26

Fixes from the [adversarial validation](docs/adversarial-validation.md) (`tests/test_adversarial.py`):

- **A patch can no longer hide an edit by adding a generated-file header.** Only the base commit's version of a file decides whether it is generated; new files are always measured. Previously adding `# Auto-generated, do not edit` to an edited file excluded the whole file.
- **Only a top-level `testing/` directory is excluded.** Nested ones such as `sympy/testing/` and `lib/matplotlib/testing/` are library code.

No published measurement changes: all 5,010 published records re-measure identically, so they keep their 0.5.0 label. `contribute verify` compares against the running analyzer version, so re-verifying them needs a 0.5.0 checkout.

## 0.5.0-beta — 2026-09-25

Metric change: **coding units replace lexical tokens as the primary footprint.**

- A unit is one AST element: a statement, an expression (call, attribute access, arithmetic/boolean operation), each comparison in a chain, a name or a literal. Operators are folded into their expression, and load/store markers and containers (`Expr`, `arguments`, `withitem`, `FormattedValue`) are not units. Punctuation no longer counts: `foo(a, b)` was 6 tokens and is 4 units, and an `if` statement is its header plus one `EndBlock` unit.
- `EndBlock` ends every statement block (`body`, `else`, `finally`), so moving a statement into or out of a block is an edit and nesting costs a unit.
- Units are aligned with the existing Myers diff over the preorder unit sequence. `net_units`, `units_added`, `units_deleted` and `churn` are primary. `structural_churn` is now unit churn with identifier/literal values ignored.
- Units are null (unknown) when any measured file does not parse on both sides. Scoring treats such records as missing measurements and gives them bounds.
- Tokens remain diagnostics: `tokens_added`, `tokens_deleted`, `net_tokens` and the new `token_churn` (formerly `churn`).
- `model_human_ratio` is unit churn over human unit churn. `leaderboard` sorts by `median_net_units` and also reports token medians. `release audit` reports `unmeasured_unit_records`.
- Scoring `parsimony-70-30-v0.4`: the same formula over units.

Results and site: [ten models × 500 tasks](examples/ten-model-500/README.md) with failed patches, a frozen 439-task panel and paired-bootstrap intervals (analyzer commit `b2316a9`, measurement code identical to `54bd8a6`). `python -m parsimony.site` renders it as a static page in `site/index.html`. The two-submission [v5 audit](examples/beta-500-v5/README.md), plus the ten-model and smoke samples, were regenerated with 0.5.0 from the v4 cache snapshot (no downloads). Unit and token churn have a Spearman correlation of 0.99 on the v5 cohorts. The ten-model 70/30 scores moved: GLM-5 and Opus swapped second and third, and Sonnet and Haiku swapped fourth and fifth.

## 0.4.0-beta — 2026-09-24

Metric changes:

- **Primary churn now counts identifier and literal changes.** In earlier versions, edits like `x = 1` → `x = 2`, `a - b` → `b - a` or `foo()` → `bar()` had zero primary footprint. About 6% of successful patches in the v3 audit were affected. Identifier/literal-insensitive churn remains available as the `structural_churn` diagnostic. It replaces `value_sensitive_churn`, which is now the primary metric.
- **Exact minimal token diff.** A Myers (minimum edit distance) diff runs after trimming the common prefix/suffix. It replaces whole-file `difflib.SequenceMatcher(autojunk=False)`, which was quadratic on the low-variety normalized token stream: 292 s for one 54k-token file, versus about 1.6 s now, mostly parsing. On a 40-task sample of gold patches, identifier-insensitive churn matched 0.3.1 for 33 and was lower (minimal) for 7. Rewrites needing more than 500 token edits fall back to a line-anchored alignment and are listed in `approximate_files`.
- Each side of a file is now parsed and tokenized once.
- **Symmetric parse fallback.** When either side of a file fails to parse, both sides are tokenized lexically and the file is listed in `lexical_files`. Previously one side was canonicalized with `ast.unparse` and the other was not, which inflated churn (e.g. 24 counted for 3 real tokens).
- `django/test/` is treated as framework implementation, like `django/db/migrations/`.
- **Shifted hunks apply like `git apply`.** A hunk whose exact context sits at a different line number is applied at the nearest match. Context is never fuzzed, and equidistant matches are rejected as ambiguous. Previously 11 Verified gold patches (e.g. `django__django-15863`, `sympy__sympy-12489`) failed as "context differs", leaving `model_human_ratio` missing. `offset_hunks` counts shifted hunks per record, and `release audit` reports `offset_hunk_records`.

Pipeline:

- Network failures are recorded as retryable `fetch_error` records, not permanent analysis `error`s. `analyze --resume` retries them. A missing base-commit file (HTTP 404) remains an analysis error.
- Legacy (`all_preds.jsonl` + `results.json`) submissions: `--include-failed` reads explicit failures from per-task `logs/<task>/report.json`. Only a report with `resolved: false` and an applied patch counts as `unresolved`. Missing reports stay unknown (`no_report`). The CLI warns when a submission publishes no explicit failures.
- The human reference patch is measured once per task per process instead of once per agent record.
- Records (schema 2) carry `analyzer_commit` (null for uncommitted analyzers) and `analyzer_source_sha256`. `release audit` rejects records whose commit differs from the frozen population. It also reports records lacking one, plus out-of-scope successes and lexical/approximate alignments.
- `evaluation_result` now distinguishes `resolved`, `failed`, `no_generation`, `no_logs` and `unknown`. Previously every non-success was labeled `not_resolved`.

Scoring (`parsimony-70-30-v0.3`):

- A successful patch whose every touched file is out of scope is `out_of_scope`. It gets bounds, not a perfect zero-footprint score, and cannot serve as a reference. The ten-model sample scores are numerically unchanged.
- The sensitivity grid adds a `net_floor=0` variant that removes credit for net deletion.

Contributions:

- `python -m parsimony.contribute verify` re-downloads recorded patches, checks their SHA256 and re-measures them. A manual `workflow_dispatch` CI job runs it on bundles.
- Bundles may carry failed-patch measurements with an explicit failed category, and `fetch_error` records.

Packaging: package version `0.4.0b0`. `requires-python >=3.12` because f-string tokenization differs before 3.12. CI tests 3.12–3.14, but published measurements must use one pinned interpreter.

Commit references in the published 0.4.0 records point to `2d4cec6` (v4 audit, ten-model) and `53f1525` (smoke). These are reworded but tree-identical versions of the commits that ran; the recorded `analyzer_source_sha256` values verify this. Results: the two-submission [v4 audit](examples/beta-500-v4/README.md), plus the ten-model and smoke samples, were regenerated with 0.4.0. `python -m parsimony.snapshot` packs a verified cache snapshot for reproducing them offline. `ast.parse` `SyntaxWarning`s from target sources are silenced.

## 0.3.1-beta — 2026-09-24

- Counted canonical `INDENT`/`DEDENT` block boundaries in primary churn (block moves were zero-footprint).
- Kept f-string literal segments in the value-sensitive diagnostic.
- Published the two-submission [v3 audit](examples/beta-500-v3/README.md) and the [v2 investigation](examples/beta-500-v2/investigation.md).

## 0.3.0-beta — 2026-09-23

- Included Django's migration framework implementation (`django/db/migrations/`) while still excluding numbered migration scripts.

## 0.2.0-beta — 2026-09-22

- Beta population freeze/coverage audit, failed-patch analysis (`--include-failed`) and sensitivity diagnostics.
- The 500-task [beta audit](examples/beta-500/README.md) revealed false generated-file exclusions; the generated-file filter now only recognizes header comments.

## 0.1.0 — 2026-09-22

- MVP: static full-file footprint analysis, leaderboard, 10-model × 10-task sample.
