# Session handoff — 2026-09-30

## Priority import implementation — 2026-09-30

Added reviewed full-population Live import, candidate PolyBench import, and `parsimony.preimages` old-Git-blob-prefix + strict-hunk audits. See `docs/priority-live-static-import.md` for full five-cohort counts and reproduction. External raw inventories/cache are `/tmp/parsimony-priority-run`; never commit/redistribute them. Unsupported/mismatching preimages remain unmeasured with unchanged upstream outcomes and complete task denominators. These checks certify touched-file compatibility only, not historical full checkout/evaluator/rights. Model/harness configurations and effort-label conflicts remain explicit.

Clean static measurements are now complete at `de633004011e1b6c8dda81d234baefc024a88b75`: DeepSeek Flash Python 295/300, GPT-5.6 Sol Python 296/300, Opus Live Python 291/300, GPT Sol JS 101/108 and TS 99/111, PolyBench Opus Python 111/113. Counts include explicit failures; every denominator is retained. Public metadata/evidence and exact external-record hashes: `examples/priority-live/`. Full footprints remain external, **no new board/per-task release** pending intended-use rights, protocol and passing-reference/population review. GPT-5.4 PolyBench 112/113 generation is real, but all patches have hunk-only corroboration and no usable old-blob prefixes; measurements remain withheld pending stronger before-state/operational evidence. Java/Rust remain secondary, unsupported tracks. Preserve unrelated `.claude/`. No target code/tests or paid evaluations are allowed.


## Latest expanded-source research — 2026-09-29

Owner challenged whether more/newer models or other languages were truly unavailable. **Earlier no-new-cohort conclusion was too narrow:** it applied to the chosen DeepSWE/Verified refresh, not all public inputs. Broader public census now finds:

- **DeepSeek V4.1 Flash / TianxiCode Live Lite:** 300 Python predictions and 204 success / 96 explicit failure results; submitter README expressly identifies V4.1 Flash. Operational bases/terms/layout adapter still need review before publication.
- **GPT-5.2 Codex / SWE-bench Multilingual:** 300 explicit outcome rows and accessible representative successful/failed Go/JS/Rust patches, despite its separate Verified result absence. TS failed sample is HTTP 403. Other Multilingual runs add data for existing models.
- **GPT-5.6 Sol / Live Slingshot v3.4.0:** 300 Python + 108 JS + 111 TS results/predictions (new config/source, not new model identity).
- **SWE-PolyBench Verified:** actual recent GPT-5.4/Opus 4.8 model patch exports; 113 Python/100 JS/100 TS/69 Java task candidate. **SWE-rebench:** Qwen3-Coder OpenHands patches+outcomes exist; July frontier export explicitly omits patches.
- **Full SWE-agent GPT-5.5 base audit materially improves Live feasibility:** all 224 present task trajectories have exact reset-base matches; all 79 nonempty Go/JS/TS patches are covered, retaining 80 submitted records including empty TS. Missing historical HF revision need not block a bounded static import where every relevant base is independently confirmed. Do not infer full 230-task availability or scoring readiness.
- **Java/Rust expansion:** candidate task pools exist across Live/Multilingual/PolyBench; Rust adds five DeepSWE tasks. Current analyzer supports neither. Use separate, versioned tracks; do not sum pools as unique tasks or pool raw units.

Read `docs/language-expansion-opportunities.md`, `docs/expanded-live-census.md`, `docs/expanded-artifact-search.md` and companion discovery JSON. Broad counts include repeated configs/attempts and some partial/retry/success-only packages; not all are valid all-attempt panels. No importer/analyzer changes, new measurements or published scores were made in this research. Next highest-novelty task: add explicitly validated plural `results.json` + keyed `preds.json` Live adapters and a clean DeepSeek V4.1 Flash Python pilot; choose language expansion only after supported-track opportunities.

## Latest UI change — 2026-09-29

Owner approved removing the dedicated **95% CI table column**. Removed it from the shared template and rebuilt all five boards. CI calculations/data, CI graph-axis endpoints and rank ranges remain; scoring and embedded page data are unchanged (full embedded JSON hashes compared before/after). Removed the obsolete CI-column sorting instructions and protected column count/alignment with Node regression assertions. No remeasurement.

## Benchmark-expansion continuation — 2026-09-29

Owner said “ok do all” for the four recommended benchmark workstreams. Implemented `parsimony/live.py` + `tests/test_live.py` for immutable multi-file/Parquet inventories and reviewed offline analysis, and extended Verified artifact imports for public submitter-hosted GitHub repositories. Both preserve explicit failures, unknowns, missing/empty artifacts and predefined language scope. Parquet is an optional lazy `pyarrow` dependency.

Fresh discovery evidence:

- `examples/deepswe-python/refresh-2026-09-29.json`: 26 usable configurations, all three metadata hashes unchanged; no new DeepSWE inputs warrant remeasurement.
- `examples/benchmark-discovery/verified-*.json` and `docs/verified-refresh-investigation.md`: experiments revision unchanged; 48 actual mini runs. Excluded Gemini 3.5 has 441 outcome rows and accessible representative patches but incomplete population coverage; GPT-5.2 Codex result files remain unavailable; Claude 3.7 representative patches remain missing. Do not equate missing artifacts with failure or pool newly measured records into the 0.5.2 board.
- `docs/pro-atlas-artifact-audit.md`: Pro anonymous S3 listing is accessible (correcting the prior untested access caveat), but the located patches/results are legacy, not verified V2. Atlas remains gold-only in inspected sources. No identified public V2/Atlas model-run export, no upstream contact or paid workaround.
- `docs/live-provenance-audit.md` and `examples/benchmark-discovery/live-immutable-audit.json`: **direct immutable Parquet** reads found all 230 Live submitted IDs and corroborated four Go/JS bases against raw trajectories. Dataset-server `revision` query links are navigation only, not pinned evidence. The candidate HF upload is August, later than May–June trajectories, and is not proven to be the run input. Artifact redistribution terms are also unverified. No board/public scores are warranted yet.

Verification before the tooling commit: 164 tests passed with pinned parsers + optional pyarrow; stdlib-only passed with 16 skips; zero submission bundles; all five Node page checks passed; `git diff --check` passed. Published analyzer pins/rules, measurements, panels, scores and pages were not changed. `.claude/` remains unrelated and untouched. Clean-checkout pilot subsequently completed at `9b287263b3d167eecc546e2072e749dd23da53f6`: four corroborated Go/JS patches (one source-reported success and one explicit failure per track) all strictly applied/parsed, status `ok`. Summary only: `examples/benchmark-discovery/live-pilot-summary.json`; raw inventories/records remain outside the repository. Full 230-record inventory and language denominators are retained, with unrequested patches explicitly `not_selected`. No scores/panels were built. **Next:** full-cohort historical base/revision, selection and redistribution review before a Live board; decide how to expose Gemini 3.5's partial Verified coverage without relabeling or mixing analyzer records. Temporary clean pilot worktree `/tmp/parsimony-live-pilot` and outputs `/tmp/live-pilot-*.jsonl` may not survive reboot.

## Earlier continuation — 2026-09-29

Owner authorized continuing from this handoff and asked which benchmarks would add model coverage. Pi's global default is now `openai-codex/gpt-6.1-sol`; thinking remains medium. This is a local Pi setting, not project data.

Completed the first bounded parser-investigation step, without changing analyzer rules, pins, published measurements, scoring or pages:

- Added a regression test for pinned-parser rejection of minimal Vitest type-only namespace exports and Effect-style generic overload signatures in `tests/test_languages.py`.
- Added `docs/typescript-parser-investigation.md` with exact base-source links, task-level error counts, limitations and a versioned repair proposal. Generic published errors do not identify file/phase, so do not attribute every task error to these fixtures. The Vitest `.d.ts` example is excluded corroboration; `src/public/node.ts` contains the in-scope construct.
- Added `docs/benchmark-expansion.md`: recommend SWE-bench Live as the first new-benchmark pilot, refresh existing inputs for current-board entrants, then investigate SWE-bench Pro V2 artifacts. Direct GitHub inspection confirmed Live patches and explicit success/failure IDs; full revision/base matching, failed-patch coverage and rights are still unaudited. No importer, model measurement, paid evaluation or upstream contact was performed.
- Verification: 141 tests passed with all pinned parsers; stdlib-only run passed with 16 skips; zero submission bundles validated; all five Node page checks and `git diff --check` passed. External environment: `/tmp/parsimony-ts-investigation` (do not assume it survives reboot).

**Next concrete task:** classify Kea's 96 error attempts and remaining after-only errors with minimal source fixtures; evaluate candidate grammar versions offline, preserving strict error rejection. Discuss the versioned parser proposal before a full remeasurement. For benchmark expansion, first audit one passing and one failed supported-language SWE-bench Live attempt against the exact historical dataset/base revision and redistribution terms; do not assume the README's sample filenames match actual layouts.

## Prior handoff / published state

Owner asked for a session refresh and recommendations, **not implementation of the next roadmap items yet**. All requested analysis/import/UI work is complete and pushed to `main`. Latest implementation commit: **`28913ad`** (data-fitted graph axes). This handoff is a subsequent docs-only update.

**My recommendation:** fix TypeScript measurement coverage next, then review scoring semantics before adding another benchmark. Start with small reproducible parser fixtures and an offline comparison of existing score variants; do not immediately launch another full measurement run or change published scores.

Owner preference: commit and push directly to **`main`**, no branches/PRs. Preserve unrelated files. `git status --short` currently shows only the pre-existing untracked **`.claude/`**, containing other worktrees; do not add, delete or clean it. No measurement batch remains pending.

For the next session:

1. `git pull --ff-only`; inspect status and read this file.
2. Read `docs/language-tracks.md`, the relevant example README, and `docs/scoring.md` before measurement/scoring changes.
3. Follow the prioritized plan below. Preserve the owner's UI and scoring requirements.
4. Update this handoff after the next meaningful change.

## Owner requirements — do not regress these

- **Default ranking must consider passing AND failed attempts**, including their footprint. We briefly ranked by solved-only footprint; the owner rejected it and it was reverted. Do not reintroduce solved-only rankings.
- **Churn and Per solve are removed from the website**, not from stored measurements or the scoring formula. The owner has **not approved changing the score to net-only**. Keep that distinction explicit.
- Current visible all-task columns: **Rank range, Model, Score, Solved, Net units added**. The dedicated 95% CI column was removed with approval; CI data/calculations and graph-axis endpoints remain. Numeric headers sort on click and reverse on another click; missing values stay last. Score is the default descending sort; net units start ascending.
- **One shared table**, defaulting to all score-panel tasks. A task-ID text/datalist input selects a task/attempt and replaces that same table; no separate task table. An All tasks button resets it.
- **Graph: one point per model, company colors**, selectable X/Y metrics from the visible table. Default X = mean net units added, Y = solved percentage. Interval/rank endpoints are explicit options. Selecting an already-used axis metric swaps axes. Task view offers only task score/net units; returning to all tasks restores the previous all-task axes.
- **Numeric graph axes fit visible points**, with 5% padding rather than forcing zero. Solved stays at 0–100%. Constant/single values use ±5% of magnitude (minimum 1 unit); empty numeric views use 0–1. Negative values are supported. On the current main board, the default net-unit axis is about **1,091–2,528.5**.
- **Light mode only**, even when the OS prefers dark.
- **Immediate model-name-only hover/focus/tap tooltip**. Custom tooltip; no delayed native SVG `<title>` tooltip. Company colors/legend remain, but do not restore company/metric text in the visible hover label. Accessible point labels still carry metric details. Tooltips hide on pointer exit, blur, scrolling, resize and chart redraw.
- **95% CI never contributes to Score.** It was already separate; this is now explained on the page and protected by a regression test. Do not claim we removed CI weighting or change the formula to address that misunderstanding.
- “Complexity” here means **static coding-unit footprint**, not semantic complexity, readability, technical debt or runtime performance.

## Published state

Cloudflare Pages serves `site/` at <https://parsimony.lasu.dev>; a push to `main` triggers redeployment. A successful push is not itself verification that the hosted deployment has completed.

| Board | Files/results | Models | Frozen tasks | Scored tasks | Attempts/task | Analyzer |
|---|---|---:|---:|---:|---:|---|
| DeepSWE Python (main) | `site/index.html`, `examples/deepswe-python/` | 26 | 34 | 33 | 4 | 0.5.2-beta |
| DeepSWE JavaScript | `site/javascript.html`, `examples/deepswe-javascript/` | 26 | 5 | 5 | 4 | 0.6.0-beta |
| DeepSWE TypeScript | `site/typescript.html`, `examples/deepswe-typescript/` | 26 | 35 | 31 | 4 | 0.6.0-beta |
| DeepSWE Go | `site/go.html`, `examples/deepswe-go/` | 26 | 34 | 34 | 4 | 0.6.0-beta |
| SWE-bench Verified | `site/verified.html`, `examples/mini-swe-agent-500/` | 33 | 500 | 448 | 1 | 0.5.2-beta |

New language tracks contain **7,696 additional attempt records**, including failures and unavailable measurements. Across the four DeepSWE populations: **108 task definitions / 103 calibratable task clusters**, kept in separate panels. Rust's five tasks remain unsupported.

Each example directory has measured JSONL, `population.json`, `coverage.json`, `score-panel.json`, `scores.json`, `sensitivity.json`, `sensitivity.md` and a README explaining exclusions. The large JSON artifacts can be tens of MB: inspect summaries with Python rather than dumping entire panels into agent context.

Older `ten-model-500` and `beta-500-*` results are historical, not additional current boards. Do not mix them with the current cohorts.

### Metric meanings and denominators

- **Score:** current `parsimony-80-20-v0.5` formula. Each passing patch earns 1–100 credit relative to its frozen passing references: 80% net-unit percentile, 20% changed-unit percentile. Explicit failures receive a footprint penalty from −25 to 0. Aggregate over all **score-panel items**, not only successes.
- **Unavailable measurements:** point Score may be null; the table shows possible score bounds. Default sorting/plotting uses their midpoint. These bounds are **not the bootstrap 95% CI**.
- **95% CI / rank ranges:** bootstrap diagnostics computed separately; task attempts are clustered when resampling. An unscored item's best/worst possibilities widen the interval. They do not alter Score. Sorting another column does not redefine the displayed score rank range.
- **Net units added:** added minus deleted coding units. The all-task column is the mean over **measured, in-scope passing and failed attempts in the score panel**; unknown/out-of-scope measurements are excluded, never zero-filled. It can be negative, and coverage can differ by model. It is not the Score.
- **Solved:** resolved count over the entire frozen population, not just score-panel tasks. DeepSWE language-specific rates are not the public benchmark's all-language leaderboard rate.
- **Population vs panel:** a task needs at least one measured, in-scope passing reference to calibrate footprint. Tasks with no usable reference remain in population records/audits but are absent from the score panel. The website's coverage details disclose this; “All tasks” in the selector means all score-panel tasks. Do not describe the score as covering the entire population when it does not.

## What I would do next, in priority order

### 1. Fix TypeScript coverage before expanding the benchmark

**Initial fixture/proposal step is now complete; see the latest continuation above.** Continue classifying remaining failures and evaluating candidate parser fixes. Work offline where possible; do not run submitted code or target-repository tests.

Known issues:

- Only **31/35** TS-labelled tasks calibrate. `effect-sse-httpapi-streaming` and `kea-atomic-signal-selectors` have no usable passing references under the current parser.
- Valid TypeScript constructs rejected by the pinned grammar include `export type * as` in a Vitest base file and existing Effect overload syntax. Parse failure on the base is **not evidence that the model wrote invalid code**. Other after-only errors have not all been classified.
- Upstream TS metadata labels `httpx-deterministic-cookie-store` as TypeScript although patches are Python, and `prometheus-transactional-reload-status` although patches are Go. They currently remain excluded-only records, not silently reassigned to another frozen track.
- JS-labelled KaTeX modifies TypeScript. JS and TS tracks therefore both measure JS/TS extensions, with grammar chosen by file extension. Do not restrict JS-labelled tasks to `.js` alone.
- Final analysis errors: **323 TS records** (322 syntax errors + one unsupported implementation-only diff), **7 Go**, **1 JS**. No residual `fetch_error` records in the published new-language runs. See coverage files for outcomes and excluded-only successes; do not conflate analysis error with benchmark failure.

Desired acceptance criteria:

1. Distinguish base grammar limitations, after-only syntax problems, unsupported diffs and wrong-language scope using minimal fixtures with source URLs/base commits.
2. Keep malformed/recovered trees explicitly unmeasured. Never suppress parser errors or assign zero to make coverage look better.
3. Propose explicit, versioned dataset corrections for wrong-language metadata, independent of which model succeeded. Preserve existing populations as historical artifacts.
4. If parser/counting rules or pins change, version the analyzer/track appropriately; commit, freeze new populations and remeasure affected cohorts from a clean checkout. Do not splice new records into old panels or hand-relabel records.
5. Compare coverage and measurement deltas before publishing new scores, then rebuild panels, scores, bootstrap reports and pages together.

### 2. Review whether Score should remain 80/20 — do not silently change it

The user removed churn from the **UI**, but Score still includes it. Make any future scoring decision explicit.

- Read existing sensitivity reports first; they already vary net weight and failure penalties.
- Compare the published formula with a clearly labelled net-only candidate offline across the same frozen records. Inspect rank changes and deletion/rewrite-heavy patches, especially on Verified, rather than assuming DeepSWE's nearly linear net/churn graph proves churn useless everywhere.
- A genuinely churn-free candidate needs an explicit failure rule too: the current failure penalty and its reference scale use changed units. Setting only the success blend's net weight to 1 is **not necessarily a fully churn-free score**.
- Preserve correctness gating, failures and missingness bounds. Do not replace Score with mean raw net units or solved-only footprint.
- Discuss the results with the owner before changing the published formula. A scoring change needs a new score version and regenerated panels/scores/uncertainty; do not reuse old CI/rank ranges for a new score.

### 3. Refresh model coverage when artifacts actually become available

A fresh-cache check on **2026-09-28** found the same **26 usable DeepSWE configurations**, with unchanged trials checksum. Evidence: `examples/deepswe-python/refresh-2026-09-28.json`.

- GPT-6 Astra configurations declare no model patches in that snapshot.
- First declared Gemini 3.8 Flash patches for high/medium returned HTTP 403. This is a probe result, not proof every possible patch URL is unavailable.
- Repeat discovery using a **fresh cache**, compare checksums/configurations, then analyze only genuinely new or changed available inputs. Do not remeasure unchanged cohorts merely to call it a refresh.
- Keep missing artifact / unknown outcome / explicit failure distinct. Never invent model patches or infer failure just because an artifact is absent.

### 4. SWE-Atlas is blocked on artifacts, not on writing an importer

Read `docs/swe-atlas-investigation.md`.

- **QnA is not a good footprint benchmark**: its output is an answer, not a repository patch.
- **Refactoring** is a better fit and has newer-model aggregate results, public tasks, exact base revisions and gold patches.
- No public per-model/per-task attempt export with model patches and failure results was found in the inspected sources. Gold patches are not model outputs.
- Next useful step: obtain an existing-run export from Scale/submitters containing model/agent/config, attempt, exact task/base revision, final patch and per-attempt evaluation outcomes, including failures; review redistribution terms.
- Do not contact/publish upstream on the owner's behalf without approval, and do not launch paid model evaluations as a workaround.
- Terminal-Bench 4.0 has not been proven importable for this purpose; terminal transcripts/aggregate scores alone are insufficient. Any coding subset would need a predefined scope and recoverable before/after code, kept separate from other panels.

### 5. Practical follow-ups, lower priority

- Add durable browser smoke checks (light mode under dark OS preference, instant name tooltip, axis changes, task/reset, mobile layout) if more UI changes are made. Current Node tests mock the DOM; Chromium was also checked manually, but the temporary CDP scripts are not committed.
- Consider versioned release assets/compressed raw artifacts before another large refresh. Keep checksums and reproducible download commands; do not delete current artifacts or rewrite Git history without an agreed migration.
- A blind reviewer preference study on passing patches could validate whether footprint is useful beyond being smaller. This is a research task, not evidence already established.
- Upstream Verified issues to report with approval: Gemini 3 Pro (high) marks all tasks unresolved; GPT-5.2 Codex lacks results; Claude 3.7 Sonnet had many missing S3 patches; some `metadata.yaml` files point to wrong S3 folders. Existing analyzer fixes handle several artifact issues; see CHANGELOG/history before duplicating investigation.

## Code and data map

- `parsimony/analysis.py`: strict patch application, scope/generated-file rules, shared unit-diff engine, Python AST units, optional language dispatch.
- `parsimony/languages.py`: pinned lazy Tree-sitter backend, syntax-unit rules, parser/track identity. **Do not reintroduce repeated native Point access**: it crashed on large trees with Python 3.14 / Tree-sitter 0.26.0. Use owned source bytes, byte offsets and computed line starts; large-tree regression test exists.
- `parsimony/benchmark.py`: records, analyzer identity, published outcomes, failure handling, base files and reference measurements.
- `parsimony/deepswe.py`: task dataset, config discovery, attempt import, pooled references.
- `parsimony/scoring.py`: published formula / bounds / track compatibility. `stability.py` and `sensitivity.py`: diagnostic variants and bootstrap.
- `parsimony/release.py`: frozen populations and coverage audits.
- `parsimony/site.py`: offline page-data generation, model-company labels, mean net metrics and graph data. `site/template.html`: all interaction/CSS/graph rendering. Rebuild **all five** HTML pages after changing either.
- `tests/test_site.py`, `tests/site_sorting.cjs`: generator and JS interaction checks, including CI independence, missing values, all axis pairs, company colors, task-cell alignment, light mode, tooltip behavior and axis extents.
- `tests/test_languages.py`, `tests/test_multilanguage.py`: optional parsers, scope, value/formatting changes, invalid syntax and failed-patch measurement.
- `docs/scoring.md`, `docs/language-tracks.md`, `docs/adversarial-validation.md`, example READMEs: methodology and limitations.

## Environment, provenance and measurement rules

- Published records use **Python 3.14.7**. Use it for comparable new measurements. Scoring rejects mixed recorded analyzer/Python versions; offline arithmetic/page generation does not itself execute target code.
- Python analysis is standard-library only. Optional language pins: `tree-sitter==0.26.0`, `tree-sitter-javascript==0.25.0`, `tree-sitter-typescript==0.23.2`, `tree-sitter-go==0.25.0`. Install with `.[languages]`. Non-Python records/panels carry language, `tree-sitter-units-v1` and exact dependency versions; do not pool tracks or raw counts across languages.
- All 7,696 new-language records were measured at clean commit **`7705e8de13343bbafbfe5bccba665dd2bab8b24a`**, analyzer 0.6.0-beta. Existing Python boards retain 0.5.2-beta records. Never relabel them as 0.6.0.
- **Measure from a clean, committed checkout**, ideally a detached worktree with cache/output outside it. `analyzer_identity` hashes every `parsimony/*.py` file, including `site.py`; UI-generator changes can therefore change the source identity even if footprint rules are unchanged. Do not edit that source tree while jobs run.
- `release freeze` refuses a dirty checkout; `.claude/` makes the main checkout dirty for that check. Do not remove it to work around the guard—use a clean measurement worktree. Freeze at the exact commit used for measurement; `release audit` checks the population commit.
- Changes to grammar/counting rules require compatible new versioned records/panels. Missing/unparsed/excluded-only fixes must not masquerade as zero-size successes.
- The cache is immutable **by URL**, never refreshed. Use a new cache for mutable upstream metadata; `--cache` is before the subcommand.
- Network endpoints: GitHub raw/API, SWE-bench S3, Hugging Face dataset server, DeepSWE site and its CloudFront artifact base. No model API calls or target code execution are needed for import/measurement.
- Temporary environments/caches/scripts from this session may have disappeared after reboot. At handoff, `/tmp/parsimony-refresh/analyzer` remains a **prunable Git worktree registration**, not a usable checkout. Existing `.claude/worktrees/*` are unrelated; leave them alone. Do not depend on old `/tmp` paths in a refreshed session.

## Commands

### Tests before every push

```sh
python -m unittest discover -s tests -q
python -m parsimony.contribute validate submissions

# Optional-parser coverage; use a fresh external environment if necessary.
uv venv --python 3.14.7 /tmp/parsimony-checks
uv pip install --python /tmp/parsimony-checks/bin/python '.[languages]'
/tmp/parsimony-checks/bin/python -m unittest discover -s tests -q

for page in index javascript typescript go verified; do
  node tests/site_sorting.cjs "site/$page.html"
done
git diff --check
```

Last implementation verification: **140 tests passed with all parsers** (15 optional grammar tests skip in a stdlib-only environment); all five page interaction checks passed. Chromium confirmed the main graph's fitted net axis and unchanged 0–100% Solved axis. Before the latest pushes, embedded data were also compared against prior pages: scores, CIs, ranks and measurements were unchanged. New-language coverage audits and byte-identical score reproduction passed at publication. There are currently zero contributed submission bundles.

### Rebuild all five pages (offline; no remeasurement)

```sh
NAV=(--nav 'DeepSWE Python=index.html' --nav 'DeepSWE JS=javascript.html' --nav 'DeepSWE TS=typescript.html' --nav 'DeepSWE Go=go.html' --nav 'SWE-bench Verified=verified.html')
for lang in python javascript typescript go; do
  E=examples/deepswe-$lang; PAGE=$lang; [ "$lang" = python ] && PAGE=index
  python -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl \
    --sensitivity "$E/sensitivity.json" --benchmark deepswe "${NAV[@]}" --output "site/$PAGE.html"
done
V=examples/mini-swe-agent-500
python -m parsimony.site "$V/score-panel.json" "$V/"*.jsonl \
  --sensitivity "$V/sensitivity.json" --benchmark verified "${NAV[@]}" --output site/verified.html
```

### Discover fresh DeepSWE configurations

```sh
CACHE=$(mktemp -d /tmp/parsimony-discovery-XXXXXX)
python -m parsimony.deepswe --cache "$CACHE" configs --output "$CACHE/configs.json"
```

Compare that output to `examples/deepswe-python/refresh-2026-09-28.json` before planning measurements. Current release: `v1.1`; run index `https://deepswe.datacurve.ai/artifacts/v1.1/trials.json` (about 51 MB). Last imported trials SHA256: `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Patch URLs come from `release.json`; 403/404 are treated as missing, not empty patches.

### Measurement/reproduction inputs

- DeepSWE task snapshot: `datacurve-ai/deep-swe` at **`0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`**.
- Dataset: `python -m parsimony.deepswe dataset CHECKOUT --language LANGUAGE --output DATASET.jsonl` (one track at a time).
- Analyze: `python -m parsimony.deepswe --cache CACHE analyze CONFIG --dataset DATASET.jsonl --output CONFIG.jsonl`, from the correctly pinned clean analyzer checkout. Includes explicit failures.
- Freeze a population before measuring, audit it afterward, then `parsimony.deepswe panel` into a **new output path**. Follow the example README commands and inspect missingness before publishing.
- Four DeepSWE attempts become `task#1`…`task#4` in start-time order. Passing references are pooled across attempts and labelled `agent#attempt`; bootstrap resamples the four items of each task together.
- Most large DeepSWE patches exceed the 500-edit exact-diff threshold and use flagged approximate alignment. Keep those flags visible in audits.
- Verified metadata: `python -m parsimony dataset --output verified.jsonl`, SHA256 prefix `82029e78…`; experiments revision **`40f164d5b8f1d249bf95a6df8b74b577fd8e519d`**.

## Recent implementation history

- `7705e8d`: optional JS/TS/Go analyzer and source investigations; **measurement revision**.
- `24fbb41`: published language records/boards and unified task dashboard.
- `8d00b48`: company-colored per-model comparison, including measured failures.
- `26343c0`: removed churn/Per solve from UI; selectable axes and net-unit column.
- `1a7a63b`: light mode, immediate model-only tooltips, explicit/tested CI independence.
- `28913ad`: data-fitted numeric axes with padding; Solved remains 0–100%.
