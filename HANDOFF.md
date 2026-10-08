# Session handoff — 2026-10-07

Current-state snapshot only. History lives in [CHANGELOG.md](CHANGELOG.md) and `git log`; older handoff text is in git history (`git show 9c02b9a:HANDOFF.md`). **Replace this file's facts when they change instead of appending dated sections.**

## Start of session

1. `git pull --ff-only`, `git status --short`, read this file.
2. Before measurement or scoring changes, read `docs/language-tracks.md`, `docs/scoring.md` and the relevant example README.
3. Commit and push directly to **`main`** (owner preference; no branches/PRs).
4. The untracked `.claude/` directory (other worktrees) is unrelated: never add, delete or clean it.

## Owner requirements — do not regress these

Website ranking and columns:

- All six boards rank by a **footprint statistic over measured, in-scope passing AND failed attempts** across the whole frozen population, lowest first, irrespective of passing-reference availability. The statistic is the **plain mean of net units added** (`ranking_metric: measured-net-mean-v1`). A second column and chart metric, **net units added over solved attempts only (mean)** (`measured_solved_net_mean`), is sortable but does not set rank. **No trimmed mean:** the owner tried a 10% trimmed mean on 2026-10-01 and had it removed the same day; do not reintroduce it or another robust statistic without being asked. No coverage gate.
- Default rank is never solved-only, and there is no correctness tie-break (a solved-only default ranking was tried and reverted). The solved-only mean is a sortable column, not the rank. Equal values tie; models with no measurements stay unranked.
- Visible columns: **Rank, Model, Net units added (mean), Net units added, solved (mean), Solved, Measured** (eligible/population). Solved % is upstream resolved / full frozen population, context only. Footprint is raw mean coding units, **not %**, with equal 1/N weight for each measured in-scope attempt, including failures; no correctness weighting. Exclude missing measurements, never zero-fill them.
- Describe the ranking as *smallest measured footprint*, never *best coding model*. Negative deletions and failed no-ops may rank first; say so.
- The 80/20 Score, its calculator data, bootstrap CI and score-rank endpoints remain only as **explicitly labelled archived graph diagnostics**. Do not reintroduce combined-score rank, and do not use its CI/rank ranges as uncertainty for the net ranking. The Score formula (`parsimony-80-20-v0.5`) is unchanged; the owner has not approved a net-only Score.
- Churn, Per solve and the dedicated 95% CI column are removed from the UI (data remains stored).
- Keep benchmarks and language tracks separate; never pool raw units across languages or analyzer versions.

Page behaviour:

- Chart **before** leaderboard; frozen-population **Sources** bar chart **after** leaderboard. Sources uses manifest task counts: DeepSWE Python/JS/TS/Go 34/5/35/34 with 4 attempts per task; Verified 500 and Live Python 300 with 1 attempt per task. Widths are task counts relative to the maximum, not ranking weights. Mark the active board and link reports and manifest hashes. Separate boards, never pooled.

- One shared table. A task-ID text/datalist input replaces that table with the selected task's attempts (including failures); an All tasks button resets. No second task table. `footprint_tasks` keeps every recorded task ID, including ones outside the old score panel.
- Numeric headers sort on click and reverse on a second click; missing values stay last.
- Graph: one borderless circle per model; company colours are **OpenAI black, xAI purple, Google green, Anthropic orange, DeepSeek blue**. Task failures are disclosed via tooltip and ARIA labels, never a dashed point outline. Selectable X/Y metrics come from the table (default X = net units added, Y = Solved %). Choosing an already-used metric swaps axes. Numeric axes fit visible points with 5% padding; coverage stays 0–100%, and Solved normally stays 0–100% (exception below); constant values use ±5% (min 1 unit); empty views 0–1; negatives supported.
- **Gemini 3.1 Pro range exclusion:** in All tasks only, exclude Gemini 3.1 Pro (including Preview and effort variants) from numeric-axis fitting when at least two other points have finite values on that axis and exclusion changes the fit. Never match Gemini 3.1 Professional or Gemini 3.1 Pro Plus, or remove any model from data, rank or table. Solved normally stays 0–100%; when this exclusion changes its fit, use the other points' 5%-padded range bounded to 0–100%. Coverage stays fixed at 0–100%, and task-view scaling is unchanged. Points outside fitted axes are extrapolated at their true coordinates using the same linear scales, never clamped or replaced with edge markers; disclose them in labels and hover, retaining actual hover/table values. Data and ranks are unchanged; no Pareto overlay.
- **Newest generation emphasised**: `site.py` sets `latest` per model, the highest version within its model line (the name text before the version number). Every generation has a permanent plain HTML name label: **8px, normal weight (400), black, no halo/shadow/border** (effort suffix dropped unless two labels would collide; every label is a fixed 10 CSS pixels to the right of its dot, vertically centered; no leader lines or variable-distance placement). Newest circles and labels have full opacity; older circles use **70% opacity**, older labels **75% opacity**, and all keep hover tooltips. This is chart emphasis only and never affects rank or the table.
- **Green better-corner square**, in the style of Artificial Analysis charts: half the plot in each dimension, at the corner that is better on both axes (lower net/churn/rank, higher solved/score). Top-left on the default axes, without any text caption; hidden when an axis has no better direction (coverage).
- Company colors belong to points/legend swatches; all graph text is black and tooltips have no border/shadow.
- **Light mode only**, even under a dark OS preference.
- Immediate custom tooltip showing the **model name and both selected axis names and actual values, plus task outcome in task view** (no native SVG `<title>`); hides on pointer exit, blur, scroll, resize and redraw. Accessible (ARIA) point labels keep metric details and task outcome.
- Keep visible copy concise, with detailed caveats/archived diagnostics under a collapsed **How to read this** section. Keep a short coding-unit definition visible: syntax elements such as statements, calls, comparisons, names and literals; net = added − removed. Not lines or runtime complexity.
- "Complexity" means static coding-unit footprint, not readability, technical debt or runtime cost.

## Published state

Cloudflare Pages serves `site/` at <https://parsimony.lasu.dev>; a push to `main` redeploys (a successful push does not prove the deployment finished).

| Board | Page | Data | Models | Population | Analyzer |
|---|---|---|---:|---:|---|
| DeepSWE Python (main) | `site/index.html` | `examples/deepswe-python/` | 26 | 34 tasks × 4 attempts | 0.5.2-beta |
| DeepSWE JavaScript | `site/javascript.html` | `examples/deepswe-javascript/` | 26 | 5 × 4 | 0.7.0-beta @ `ca37c31` |
| DeepSWE TypeScript | `site/typescript.html` | `examples/deepswe-typescript/` | 26 | 35 × 4 | 0.7.0-beta @ `ca37c31` |
| DeepSWE Go | `site/go.html` | `examples/deepswe-go/` | 26 | 34 × 4 | 0.6.0-beta |
| SWE-bench Verified | `site/verified.html` | `examples/mini-swe-agent-500/` | 34 | 500 × 1 | 0.5.2-beta |
| SWE-bench Live Lite Python | `site/live.html` | `examples/live-python/` | 4 configs | 300 × 1 | 0.6.0-beta @ `de63300` |

- Each example directory holds measured JSONL, `population.json`, `coverage.json`, `score-panel.json`, `scores.json`, sensitivity/stability reports and a README. Large JSON files are tens of MB: summarise them with Python rather than dumping them into context.
- Live Python: four model + agent configurations (DeepSeek V4.1 Flash · TianxiCode, GPT-5.6 Sol · Slingshot 3.4.0, Claude Opus 4.8 · AiWork, GPT-5.5 · agav 0.2.0-beta.2). The agav addition has 262 eligible footprints / 300 (271 completed analyses, 9 excluded-only), 186 source-reported successes, 85 failures, 29 empty-only unknowns; eligible mean net 50.38549618320611. All 271 nonempty patches have matching old-blob/hunk preimages. See `docs/agav-gpt55-live-release-review.md`; historical measurement authorization is not external board certification. 238/300 tasks calibrated, 62 uncalibrated under opt-in `full-population-uncalibrated-bounds-v1`. Records publish scalars and hashes only, not patches; raw-artifact redistribution remains uncleared (`docs/deepseek-v4.1-live-release-review.md`, `docs/priority-live-provenance.md`). The JSONLs are byte-identical to clean `de63300` measurements; never relabel them.
- Verified now includes **Gemini 3.5 Flash / mini-SWE-agent 2.4.2**: 441 eligible attempts (359 passing, 82 failed), 59 explicit aggregate `no_generation`, all 500 retained. Source-reported Solved 71.8%, measured mean net +36.6031746031746. All 441 separate patches agree with pinned predictions. Measurement commit/source hash exactly match existing Verified 0.5.2; human-reference comparison is intentionally uncomputed. See `docs/gemini-3.5-verified-release.md` and `examples/benchmark-discovery/add-gemini-verified.py`. Old 33-model records, population/panel and reports stay unchanged; current reports use `coverage-34.json`, `scores-34.json`, `sensitivity-34.json`.
- Measured but **not published**: GPT-5.6 Sol JS 101/108 and TS 99/111, PolyBench Opus 4.8 Python 111/113 (metadata/hashes in `examples/priority-live/`; full footprints external). GPT-5.4 PolyBench measurements are withheld (hunk-only corroboration, no usable old-blob prefixes).
- `ten-model-500`, `beta-500-*` and root `ten-model-*` files are historical; never mix them with current cohorts.
- There are zero contributed submission bundles.

### Metric meanings

- **Net units added:** added − deleted coding units per attempt; the board shows each model's mean over measured, in-scope passing and failed attempts. Unknown/out-of-scope records are excluded, never zeroed. Coverage differs by model and is shown in Measured.
- **Solved:** upstream resolved count over the whole frozen population.
- **Score (archived diagnostic, not default):** 80% net / 20% churn percentiles against frozen passing references; failed attempts receive a bounded growth/churn penalty of −25…0, with bounds for unscored items. Bounds are not the bootstrap CI; CI never affects Score.
- **Population vs panel:** a task needs a measured, in-scope passing reference to calibrate Score. Uncalibrated tasks stay in the population and in the footprint ranking.

## Known property of the mean ranking

On Verified a few failed mass deletions decide the top ranks: Llama 4 Maverick is #1 at −244 with a solved-only mean of +10 and a median of +4. The owner knows this and chose the plain mean plus the solved-only column anyway. Smaller footprint also correlates with lower solve rate on every board (Spearman −0.25 to −0.57); failed attempts are not systematically smaller than passing ones, so this is a real model-level tendency.

## Next work, in priority order

### 1. Add newer models to the existing benchmark battery

**Recommended direction: recent models on supported Python/JS/TS/Go tracks first, not another ranking redesign or Java/Rust expansion.** Start with public exports on an existing board's frozen population and, where possible, the same harness. Cross-harness Live additions remain model + agent configurations, not controlled model-only comparisons. This is a plan, not a claim that new exports have been found.

Latest discovery: **2026-10-07** complete GitHub trees for Live, PolyBench and Verified match their stored pins. Complete DeepSWE trials/release/leaderboard hashes are unchanged: 70 configs / 28 model names, Astra has no declared patches; four representative Gemini 3.8 GETs returned 403. This is not a full usable-config patch-availability refresh. GPT-5.2 Codex outcome probes still returned 404. Census: `examples/benchmark-discovery/model-battery-refresh-2026-10-07.json`.

New benchmark feasibility: **18 LiveCodeBench Python configurations × 1,055 retained tasks** (2023-05-07–2025-04-06), with **17,353 measured footprints / 18,990 task-attempt slots**. `examples/livecodebench-pilot/population-18.json` versions exact source-export bindings and fixed sample index 0 while preserving original `population.json` / `measurement-summary.json`. Clean `cbe8768` / Python 3.14.7 measured only the 12 new inputs; `measurement-summary-18.json` reuses the original six metadata records unchanged from `2645271`. Source hash and unit definition match. Five exports have 713/880 records and missing-task outcomes stay unknown; missing footprints comprise 1,209 absent tasks, 43 absent code lists, 318 empty bodies and 67 parse errors, never zeros. Observed solved / 1,055 is a lower bound for partial exports. Source labels span OpenAI, xAI, Meta, Mistral, Qwen, DeepSeek, Anthropic, Google and EXAONE; do not call these newly released 2026 frontier models. This is **NONPUBLISHED**, not a seventh website board: pinned benchmark-dataset corroboration, rights/numerical-publication review and configuration evidence remain blockers. Raw code and scalar rows stay external. Evidence: `examples/benchmark-discovery/livecodebench-expansion-2026-10-07.json` and the initial fresh-code census.

Seed-OSS Live Python is now explicitly **withheld**: 291 submitted / 300 (60 success, 211 failure, 20 error, 9 unknown) and 271 candidate preimages pass, but 238 separate rollout patches differ from aggregate predictions. Four match, one lacks a prediction; strict diagnostic comparison finds 226 divergent results/scopes and 12 unsupported nontext changes. Evaluated-patch linkage is unproven; do not measure/publish by silently choosing a patch representation. See `docs/seedoss-live-candidate-review.md` and its numerical/hash census.

All 327 BigCodeBench sample exports were body-inspected but have no paired outcomes. Further official public outcome search found aggregate-only results and a 401 requests-dataset blocker, not global absence proof. Evidence: `examples/benchmark-discovery/bigcode-outcomes-search-2026-10-07.json`.

Next existing-board work remains Live GPT-5.6 Sol JS/TS remeasurement or a newly available public export. Fresh-code release work is separate and must not pool units with repository patches.

Next-session discovery checklist:

1. Refresh **DeepSWE** configs with a fresh cache (command under Inputs), compare against `examples/deepswe-python/refresh-2026-09-29.json`, and inspect every new/changed configuration. Last refresh found the same 26 usable configs. Recheck GPT-6 Astra (previously no declared patches) and Gemini 3.8 Flash (previously HTTP 403), but do not treat either as available until artifacts are retrieved. Look for newer generations across all represented model families, not only the current leaders.
2. Refresh public **Live** submission listings and **PolyBench** run listings at newly pinned upstream commits. Prioritize newer Python configurations alongside DeepSeek V4.1 Flash, GPT-5.6 Sol and Opus 4.8, then supported JS/TS cohorts. Model names in listings are source claims: require actual task-level patches, outcome records and usable preimages. Existing importer run choices and the priority driver are explicit inventories, not automatic discovery of future submissions; extend them only after checking the new export shape and population.
3. Refresh **Verified** public experiments for genuinely newer model exports. Gemini 3.5 is now included with explicit outcomes for all 500 tasks. Recheck remaining blocked runs as secondary work: GPT-5.2 Codex still returned 404 for both per-instance and aggregate results on 2026-10-02; Claude 3.7 patches are missing. Retain the 500-task population and unknown outcomes, never convert missing rows into failures or measured zeros.
4. Produce a small committed, numerical/metadata-only candidate census: source URL and immutable revision, source-reported model + harness, benchmark/language, population and attempts, patch/outcome availability, preimage tier, current blocker and next action. Record unavailable candidates too. Do not commit fetched patches, prompts or trajectories.

Choose the first releasable newer-model cohort by **artifact completeness and compatibility**, not solve rate or expected footprint rank. Discovery can be refreshed broadly; static analysis should run only for new/changed checksum-bound inputs. Prefer adding comparable recent configurations to existing boards over opening a sparsely populated benchmark just to show a new model.

### 2. Release the already located recent-model cohorts

These are concrete fallbacks if fresh discovery yields no immediately releasable newer exports:

- **GPT-5.6 Sol Live JS/TS:** preimages were audited and measurements exist externally (`examples/priority-live/`), but they use the old 0.6.0 Tree-sitter backend. Remeasure with the current 0.7.0 official TypeScript parser in a clean checkout. Freeze the complete language populations (108 JS / 111 TS); retain successes, failures, missing/error and out-of-scope records. Publish separate Live language tracks, not on the DeepSWE language boards. Audit release/provenance rights before publishing numerical exports.
- **PolyBench Opus 4.8 Python:** 111/113 attempts have static measurements. Complete the provenance/population release review and publish a separate PolyBench board if justified. Preserve all 113 population items and distinguish missing measurements from failures. Do not mix it with Live or Verified.
- **PolyBench GPT-5.4:** still blocked on historical before-state identity. Candidate-base hunk matches without usable old-blob prefixes are insufficient for release; seek stronger public operational/reset or byte-identity evidence, not permissive patch application. Lower priority than accessible newer-model cohorts.

Passing references are needed only for archived combined-score diagnostics, **not** footprint eligibility or default ranking. Do not select a solved-derived population or delay a valid footprint release solely because some tasks have no passing reference. Use bounded archived scoring where needed without inventing scores.

### 3. Acceptance checklist for every battery addition

- Pin upstream submission/dataset revisions, full task/attempt membership, patch and outcome checksums, model/harness attribution and language mapping. Preserve submitted versus placeholder/missing distinctions. Corroborate touched-file preimages; do not claim full-checkout, evaluator or model-backend certification from that evidence.
- Use a clean committed analyzer worktree with external cache/raw storage and Python 3.14.7. A same-board comparison must use compatible analyzer/track identities: use the existing identity where operationally possible, otherwise remeasure the comparison cohort and version the release. Never relabel old records or pool incompatible versions. JS/TS worktrees require their own pinned `npm ci`.
- Retain the entire predefined population. Report eligible/population coverage plus source-reported outcomes and exclusion/error reasons. Rank by the plain mean over all measured in-scope attempts, including failures; preserve the separate solved-only mean column. No trimming, correctness tie-break, coverage gate or missing-zero imputation.
- Review numerical publication separately from raw-artifact redistribution. Publish attributed scalars/hashes, coverage and reproduction metadata; do not assume an output ownership clause grants rights to another submitter's artifacts. Keep raw patches/source/prompts/trajectories external unless separately cleared.
- Freeze/version population, numerical exports and diagnostics; update the example README, board navigation and Published state table. Rebuild all affected pages with the shared template, run the full pinned-parser suite and Node checks, reproduce archived score arithmetic, then commit/push `main`. Verify deployment if accessible; report access failures rather than claiming a push proves deployment.

Before a large import, resolve storage growth: `examples/` is ~250 MB working-tree (~30 MB packed). Prefer versioned release assets for large measurement JSONL, with immutable checksums and reproduction/download commands. A raw-artifact cache is not a publication asset. Do not delete current artifacts or rewrite history without an agreed migration.

### 4. Maintenance and secondary expansion

- Owner direction: Parsimony stays focused on delivered implementation footprint. A separate verbosity/yap/output-token/reasoning-expenditure benchmark is **noted for later only**; do not implement it or mix generation tokens into Parsimony ranking. Continue prioritizing model additions.
- Fresh bounded discovery: DeepSWE's complete 31,617-trial export matches the stored SHA256; GPT-6 Astra has zero declared patches across five configs, and sampled Astra/Gemini 3.8 patch GETs returned HTTP 403. Live/Verified/PolyBench submission revisions remain at their stored pins. See `docs/new-model-discovery.md`.

The parser problem is solved (0.7.0, 2026-10-01): JS/TS use the official TypeScript parser, TS errors fell from 323 to 5 of 3,640 records and 33/35 TS tasks calibrate. Do not let residual cleanup displace newer-model additions. See `docs/typescript-parser-investigation.md`:

- Wrong-language TS metadata: `httpx-deterministic-cookie-store` has Python patches; `prometheus-transactional-reload-status` has Go patches. Correct only through an explicit versioned dataset change, never a silent move.
- Effect's `dtslint/*.tst.ts` type tests and new root-level JS/TS scratch scripts currently count as implementation. Excluding them requires a versioned scope change and remeasurement; one invalid scratch script explains one remaining TS error.
- Classify the 7 Go Tree-sitter analysis errors; leave them missing, not zero, pending a fix.
- SWE-Atlas Refactoring and SWE-bench Pro V2 remain blocked on public per-attempt patch exports, not importer code (`docs/swe-atlas-investigation.md`, `docs/pro-atlas-artifact-audit.md`). Java/Rust require new analyzers and separate tracks (`docs/language-expansion-opportunities.md`); defer until supported recent-model sources are exhausted or the owner reprioritizes.
- Add durable real-browser smoke checks if changing UI again; Node tests mock the DOM. Pin CI `verify` from `'3.14'` to 3.14.7 for reproducibility. A blind reviewer study is optional later validation, not a gate for footprint reporting.
- Never contact upstream, file issues or launch paid evaluations without owner approval. Known Verified issues for an approved future report: Gemini 3 Pro (high) marks all tasks unresolved; some `metadata.yaml` point to wrong S3 folders.

## Code and data map

- `parsimony/analysis.py`: strict patch application, scope/generated-file rules, unit-diff engine, Python AST units, language dispatch.
- `parsimony/typescript_units.cjs`: Node worker that parses JS/TS with the pinned official TypeScript parser and emits units, tokens and structure; part of the analyzer source hash.
- `parsimony/languages.py`: backend dispatch, the long-lived Node worker client (JS/TS) and the pinned lazy Tree-sitter backend (Go). **Do not reintroduce repeated native Point access** (crashed on large trees with Python 3.14 / tree-sitter 0.26.0); use owned bytes, byte offsets and computed line starts.
- `parsimony/benchmark.py`: records, analyzer identity, outcomes, failures, reference measurements.
- `parsimony/deepswe.py`, `live.py`, `polybench.py`, `artifacts.py`, `preimages.py`: importers and provenance audits.
- `parsimony/scoring.py` (formula, bounds, track compatibility), `stability.py`, `sensitivity.py` (diagnostics, bootstrap).
- `parsimony/release.py`: frozen populations and coverage audits.
- `parsimony/site.py`: offline page data (`build()` sets `ranking_metric` and sorts models). `site/template.html`: all interaction, CSS and graph code. Rebuild **all six** pages after changing either.
- Tests: `tests/test_site.py` + `tests/site_sorting.cjs` (generator and page behaviour), `tests/test_languages.py`, `tests/test_multilanguage.py`, plus per-module tests.

## Measurement rules

- Published Python records use **Python 3.14.7**; use it for comparable measurements. Scoring rejects mixed analyzer/Python versions.
- Optional parser pins: JS/TS `typescript@5.9.3` via `npm ci` (Node.js; unit track `typescript-compiler-units-v1`); Go `tree-sitter==0.26.0`, `tree-sitter-go==0.25.0` via `.[languages]` (`tree-sitter-units-v1`). A measurement worktree needs its own `npm ci`; `node_modules/` is ignored, so the checkout stays clean.
- DeepSWE JS/TS records were measured at clean `ca37c31` (0.7.0-beta), Go at clean `7705e8d` (0.6.0-beta); Python boards keep 0.5.2-beta. Never relabel. `deepswe panel` refuses to overwrite an existing panel: write to a new path, or delete the old file deliberately when replacing a track.
- Measure from a **clean committed checkout**, ideally a detached worktree with cache/output outside it. `analyzer_identity` hashes every `parsimony/*.py`, including `site.py`. `release freeze` refuses a dirty tree, and `.claude/` makes the main checkout dirty: use a worktree, don't delete `.claude/`.
- The download cache is immutable by URL (`--cache` goes before the subcommand); use a fresh cache for mutable upstream metadata.
- Missing artifact, unknown outcome and explicit failure are distinct. Never infer failure from absence or invent patches.
- No model API calls, target-code execution or target-repo installs.

## Commands

Latest validation: 269 tests passed with Python 3.14.7 and the exact optional parser pins (16 LiveCodeBench pilot tests); the default Python suite skips Go tests without the languages extra. GPT-5.5/agav is integrated as the fourth Live Python configuration; its 300 rows, artifact/audit bindings and excluded-only semantics have regression coverage. All six Node page checks passed. Population/base/analyzer audit passed for all 500 Gemini records, all 33 archived score entries reproduce exactly, and existing raw records/panel/population/report files remain unchanged. External reproducible inventory/measurement data: `/tmp/parsimony-gemini-bound`; clean old analyzer: `/tmp/parsimony-verified-measure` (temporary paths, not durable publication inputs).

### Before every push

```sh
npm ci                                            # pinned TypeScript parser for JS/TS tests
python -m unittest discover -s tests -q          # 269 tests collected; Go tests skip without the languages extra
python -m parsimony.contribute validate submissions
uv venv --python 3.14.7 /tmp/parsimony-checks
uv pip install --python /tmp/parsimony-checks/bin/python '.[languages]'
/tmp/parsimony-checks/bin/python -m unittest discover -s tests -q
for page in index javascript typescript go verified live; do node tests/site_sorting.cjs "site/$page.html"; done
git diff --check
```

### Rebuild all six pages (offline, no remeasurement)

This reproduces every committed page byte-for-byte; check with `git status` after running it.

```sh
NAV=(--nav 'DeepSWE Python=index.html' --nav 'DeepSWE JavaScript=javascript.html' --nav 'DeepSWE TypeScript=typescript.html'
     --nav 'DeepSWE Go=go.html' --nav 'SWE-bench Verified=verified.html' --nav 'Live Python=live.html')
for lang in python javascript typescript go; do
  E=examples/deepswe-$lang; PAGE=$lang; [ "$lang" = python ] && PAGE=index
  python -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl \
    --sensitivity "$E/sensitivity.json" --benchmark deepswe "${NAV[@]}" --output "site/$PAGE.html" \
    --external examples/external/artificial-analysis-2026-10-08.json
done
V=examples/mini-swe-agent-500
python -m parsimony.site "$V/score-panel.json" "$V/"*.jsonl \
  --sensitivity "$V/sensitivity-34.json" --benchmark verified "${NAV[@]}" --output site/verified.html
L=examples/live-python
python -m parsimony.site "$L/score-panel.json" "$L/deepseek-v4.1-flash.jsonl" "$L/gpt-5.6-sol.jsonl" "$L/claude-opus-4.8.jsonl" "$L/gpt-5.5-agav.jsonl" \
  --sensitivity "$L/stability.json" --benchmark live "${NAV[@]}" --output site/live.html \
  --data "$L/site-data.json"   # tests require the committed copy to match the page
```

### Inputs

- Artificial Analysis axis (DeepSWE boards only): `examples/external/aa-mapping.json` is the hand-curated agent → AA model `id` mapping (match `exact` / `effort_unlabelled` / `undated_alias`, or `aa_id: null` with a reason; never borrow another effort's score). Refresh with `AA_API_KEY=... python -m parsimony.external snapshot examples/external/aa-mapping.json --output examples/external/artificial-analysis-YYYY-MM-DD.json` (`list` prints candidate ids). The key is read from the environment only; never commit it. Attribution to https://artificialanalysis.ai/ is required by the free-API terms and is shown on the page. Verified and Live have no mapping yet (older or effort-unspecified configurations).

- DeepSWE tasks: `datacurve-ai/deep-swe` @ `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`; release `v1.1`, trials SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Discover configs: `python -m parsimony.deepswe --cache "$(mktemp -d)" configs --output configs.json` and compare with `examples/deepswe-python/refresh-2026-09-29.json`.
- DeepSWE attempts become `task#1`…`task#4` in start-time order; references pool across attempts as `agent#attempt`; bootstrap resamples a task's attempts together. Most large DeepSWE patches exceed the 500-edit exact-diff threshold and use flagged approximate alignment.
- Verified: `python -m parsimony dataset --output verified.jsonl` (SHA256 prefix `82029e78…`), experiments @ `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`.
- Live Python reproduction: `examples/live-python/README.md`.
