# Session handoff — 2026-10-01

Current-state snapshot only. History lives in [CHANGELOG.md](CHANGELOG.md) and `git log`; older handoff text is in git history (`git show 9c02b9a:HANDOFF.md`). **Replace this file's facts when they change instead of appending dated sections.**

## Start of session

1. `git pull --ff-only`, `git status --short`, read this file.
2. Before measurement or scoring changes, read `docs/language-tracks.md`, `docs/scoring.md` and the relevant example README.
3. Commit and push directly to **`main`** (owner preference; no branches/PRs).
4. The untracked `.claude/` directory (other worktrees) is unrelated: never add, delete or clean it.

## Owner requirements — do not regress these

Website ranking and columns:

- All six boards rank by a **footprint statistic over measured, in-scope passing AND failed attempts** across the whole frozen population, lowest first, irrespective of passing-reference availability. The statistic is a **10% trimmed mean of net units added** (`ranking_metric: measured-net-trimmed-mean-10-v1`, owner-approved 2026-10-01): drop floor(n × 5%) attempts at each end per model, so a plain mean below 20 attempts. The plain mean (`measured_net_mean`) stays in the data and as a graph metric. No coverage gate: every measured model is ranked and coverage is shown (a fixed 90% gate would unrank all TypeScript models).
- No solved-only ranking or filtering, and no correctness tie-break (a solved-only ranking was tried and reverted). Equal values tie; models with no measurements stay unranked.
- Visible columns: **Rank, Model, Net units added, Solved, Measured** (eligible/population). Solved % is upstream context only. Never zero-fill missing measurements.
- Describe the ranking as *smallest measured footprint*, never *best coding model*. Negative deletions and failed no-ops may rank first; say so.
- The 80/20 Score, its calculator data, bootstrap CI and score-rank endpoints remain only as **explicitly labelled archived graph diagnostics**. Do not reintroduce combined-score rank, and do not use its CI/rank ranges as uncertainty for the net ranking. The Score formula (`parsimony-80-20-v0.5`) is unchanged; the owner has not approved a net-only Score.
- Churn, Per solve and the dedicated 95% CI column are removed from the UI (data remains stored).
- Keep benchmarks and language tracks separate; never pool raw units across languages or analyzer versions.

Page behaviour:

- One shared table. A task-ID text/datalist input replaces that table with the selected task's attempts (including failures); an All tasks button resets. No second task table. `footprint_tasks` keeps every recorded task ID, including ones outside the old score panel.
- Numeric headers sort on click and reverse on a second click; missing values stay last.
- Graph: one point per model, company colours, selectable X/Y metrics from the table (default X = net units added, Y = Solved %). Choosing an already-used metric swaps axes. Numeric axes fit visible points with 5% padding; Solved stays 0–100%; constant values use ±5% (min 1 unit); empty views 0–1; negatives supported.
- **Light mode only**, even under a dark OS preference.
- Immediate custom tooltip showing the **model name only** (no native SVG `<title>`); hides on pointer exit, blur, scroll, resize and redraw. Accessible point labels keep metric details.
- "Complexity" means static coding-unit footprint, not readability, technical debt or runtime cost.

## Published state

Cloudflare Pages serves `site/` at <https://parsimony.lasu.dev>; a push to `main` redeploys (a successful push does not prove the deployment finished).

| Board | Page | Data | Models | Population | Analyzer |
|---|---|---|---:|---:|---|
| DeepSWE Python (main) | `site/index.html` | `examples/deepswe-python/` | 26 | 34 tasks × 4 attempts | 0.5.2-beta |
| DeepSWE JavaScript | `site/javascript.html` | `examples/deepswe-javascript/` | 26 | 5 × 4 | 0.7.0-beta @ `ca37c31` |
| DeepSWE TypeScript | `site/typescript.html` | `examples/deepswe-typescript/` | 26 | 35 × 4 | 0.7.0-beta @ `ca37c31` |
| DeepSWE Go | `site/go.html` | `examples/deepswe-go/` | 26 | 34 × 4 | 0.6.0-beta |
| SWE-bench Verified | `site/verified.html` | `examples/mini-swe-agent-500/` | 33 | 500 × 1 | 0.5.2-beta |
| SWE-bench Live Lite Python | `site/live.html` | `examples/live-python/` | 3 configs | 300 × 1 | 0.6.0-beta @ `de63300` |

- Each example directory holds measured JSONL, `population.json`, `coverage.json`, `score-panel.json`, `scores.json`, sensitivity/stability reports and a README. Large JSON files are tens of MB: summarise them with Python rather than dumping them into context.
- Live Python: three model + agent configurations (DeepSeek V4.1 Flash · TianxiCode, GPT-5.6 Sol · Slingshot 3.4.0, Claude Opus 4.8 · AiWork). 238/300 tasks calibrated, 62 uncalibrated under opt-in `full-population-uncalibrated-bounds-v1`. Records publish scalars and hashes only, not patches; raw-artifact redistribution remains uncleared (`docs/deepseek-v4.1-live-release-review.md`, `docs/priority-live-provenance.md`). The JSONLs are byte-identical to clean `de63300` measurements; never relabel them.
- Measured but **not published**: GPT-5.6 Sol JS 101/108 and TS 99/111, PolyBench Opus 4.8 Python 111/113 (metadata/hashes in `examples/priority-live/`; full footprints external). GPT-5.4 PolyBench measurements are withheld (hunk-only corroboration, no usable old-blob prefixes).
- `ten-model-500`, `beta-500-*` and root `ten-model-*` files are historical; never mix them with current cohorts.
- There are zero contributed submission bundles.

### Metric meanings

- **Net units added:** added − deleted coding units per attempt; the board shows each model's 10% trimmed mean over measured, in-scope passing and failed attempts. Unknown/out-of-scope records are excluded, never zeroed. Coverage differs by model and is shown in Measured.
- **Solved:** upstream resolved count over the whole frozen population.
- **Score (archived diagnostic):** 80% net / 20% churn percentile against frozen passing references, failures −25…0, bounds for unscored items. Bounds are not the bootstrap CI; CI never affects Score.
- **Population vs panel:** a task needs a measured, in-scope passing reference to calibrate Score. Uncalibrated tasks stay in the population and in the footprint ranking.

## Why the trimmed mean (settled 2026-10-01)

The plain mean let a few huge failed patches decide rank. On Verified, Llama 4 Maverick ranked #1 at −244 with a median of +4; its five lowest attempts were failed deletions of 7k–14k units. The trimmed mean fixes that (Llama is now −3, still #1 but by a normal margin), barely moves the DeepSWE orders, and flips Live's top two (Opus 4.8 · AiWork now first). Smaller footprint still correlates with lower solve rate under every statistic tried (Spearman −0.25 to −0.57), and failed attempts are not systematically smaller than passing ones, so this is a real model-level tendency, not an artefact. Median was rejected because of heavy integer ties on Verified. Do not revert to the plain mean without the owner.

## Next work, in priority order

### 1. Remaining JavaScript/TypeScript follow-ups

The parser problem is solved (analyzer 0.7.0, 2026-10-01): JS/TS use the official TypeScript parser, TS errors fell from 323 to 5 of 3,640 records and 33/35 TS tasks calibrate. See `docs/typescript-parser-investigation.md`. What is left:

- Wrong-language upstream metadata: `httpx-deterministic-cookie-store` (Python patches) and `prometheus-transactional-reload-status` (Go patches) are the two uncalibrated TS tasks. Fixing them needs an explicit, versioned dataset correction, never a silent move.
- Scope: Effect's `dtslint/*.tst.ts` type tests count as implementation; an exclusion rule would be a versioned scope change with a remeasure.
- Root-level scratch scripts (`*.cjs`, `*.js`) left by agents count for JS/TS (only Python excludes new root files). One invalid scratch script causes one of the five remaining errors.
- The externally held GPT-5.6 Sol Live JS/TS measurements (`examples/priority-live/`) were made with the 0.6.0 Tree-sitter backend. Remeasure them with 0.7.0 before any release.
- Go still has 7 analysis errors under Tree-sitter; they have not been classified.

### 2. Repository size

`examples/` is ~250 MB in the working tree (~30 MB packed). Move large raw JSONL to versioned release assets with checksums and download commands before the next big import. Do not delete current artifacts or rewrite history without an agreed migration.

### 3. Benchmark and model expansion

- Candidate releases: the measured GPT-5.6 Sol JS/TS and PolyBench Opus cohorts, after passing-reference/population and rights review.
- DeepSWE refresh (2026-09-29): same 26 usable configurations, unchanged checksums. Re-run discovery with a **fresh cache**; only analyze new/changed inputs. GPT-6 Astra declared no patches; Gemini 3.8 Flash patches returned 403.
- Verified: Gemini 3.5 has 441/500 outcome rows (partial coverage, not yet exposed); GPT-5.2 Codex lacks results; Claude 3.7 patches missing.
- SWE-Atlas Refactoring and SWE-bench Pro V2 are blocked on public per-attempt model-patch exports, not importer code (`docs/swe-atlas-investigation.md`, `docs/pro-atlas-artifact-audit.md`). Java/Rust need new unsupported tracks (`docs/language-expansion-opportunities.md`).
- Never contact upstream, publish upstream issues or launch paid evaluations without owner approval.

### 4. Lower priority

- Commit durable browser smoke checks (light mode under dark OS, tooltip, axis swaps, task/reset, mobile) if the UI changes again; Node tests mock the DOM.
- CI `verify` job re-measures on `'3.14'`, not the pinned 3.14.7.
- Blind reviewer preference study on passing patches to validate footprint beyond "smaller".
- Upstream Verified issues to report with approval: Gemini 3 Pro (high) marks all tasks unresolved; some `metadata.yaml` point to wrong S3 folders.

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

### Before every push

```sh
npm ci                                            # pinned TypeScript parser for JS/TS tests
python -m unittest discover -s tests -q          # 226 tests; Go tests skip without the languages extra
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
    --sensitivity "$E/sensitivity.json" --benchmark deepswe "${NAV[@]}" --output "site/$PAGE.html"
done
V=examples/mini-swe-agent-500
python -m parsimony.site "$V/score-panel.json" "$V/"*.jsonl \
  --sensitivity "$V/sensitivity.json" --benchmark verified "${NAV[@]}" --output site/verified.html
L=examples/live-python
python -m parsimony.site "$L/score-panel.json" "$L/deepseek-v4.1-flash.jsonl" "$L/gpt-5.6-sol.jsonl" "$L/claude-opus-4.8.jsonl" \
  --sensitivity "$L/stability.json" --benchmark live "${NAV[@]}" --output site/live.html \
  --data "$L/site-data.json"   # tests require the committed copy to match the page
```

### Inputs

- DeepSWE tasks: `datacurve-ai/deep-swe` @ `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`; release `v1.1`, trials SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Discover configs: `python -m parsimony.deepswe --cache "$(mktemp -d)" configs --output configs.json` and compare with `examples/deepswe-python/refresh-2026-09-29.json`.
- DeepSWE attempts become `task#1`…`task#4` in start-time order; references pool across attempts as `agent#attempt`; bootstrap resamples a task's attempts together. Most large DeepSWE patches exceed the 500-edit exact-diff threshold and use flagged approximate alignment.
- Verified: `python -m parsimony dataset --output verified.jsonl` (SHA256 prefix `82029e78…`), experiments @ `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`.
- Live Python reproduction: `examples/live-python/README.md`.
