# Handoff (2026-09-28)

State of Parsimony after the cloud sessions and local follow-up of 2026-09-28. Owner preference: commit and push directly to `main`; no branches or pull requests.

## Where things stand

- **Site** (Cloudflare Pages, output directory `site`, served at https://parsimony.lasu.dev; every push to `main` redeploys):
  - `site/index.html` is the main board: [DeepSWE](examples/deepswe-python/README.md), 26 current models × 34 Python tasks × 4 attempts.
  - `site/verified.html`: [SWE-bench Verified](examples/mini-swe-agent-500/README.md), 33 mini-SWE-agent models × 500 tasks.
  - `site/javascript.html`, `site/typescript.html`, `site/go.html`: 26 models in each separate language track; frozen populations 5, 35 and 34 tasks respectively, four attempts each. Panels cover 5, 31 and 34 tasks. Full records, coverage, panels, scores and sensitivity live in `examples/deepswe-{javascript,typescript,go}/`.
  - One shared table defaults to all score-panel tasks; the task-ID input replaces it with a selected attempt. The graph has one point per model, colored by developer company, with user-selectable X/Y metrics from the visible table. Default: mean net units added vs solved percentage. Numeric axes fit visible points with 5% padding; equal/single values use ±5% of magnitude (minimum 1 unit), empty axes use 0–1, and solved percentage always stays at 0–100%. Net units include measured passing AND failed attempts. Per solve and churn are removed from the UI, but the historical 80/20 scoring formula is unchanged. A selected task offers task score/net units only; all-task axes are restored on reset. Pages always use light mode. Hover/focus/tap immediately shows only the model name in a custom tooltip; native SVG hover titles are removed. Failed task attempts retain dashed outlines. CI is a separate uncertainty display, never an input to Score; a regression test enforces this.
  - The leaderboard shows a 95% bootstrap **rank range** per model (no tiers). Score, 95% CI, Solved and Net units added headers toggle numeric sorting; default is all-task score descending. CI sorts by its lower bound; net units start ascending; missing values stay last. Rank ranges always refer to the all-task score, regardless of the selected sort. A Node.js interaction test runs through unittest when Node is available.
- **Analyzer 0.6.0-beta** adds optional pinned Tree-sitter JS/TS/Go tracks; see [language tracks](docs/language-tracks.md). Existing published Python records remain 0.5.2-beta and must not be relabeled. New root-level files are excluded only for Python (normal Go/JS/TS entry points count).
- **Statistics** (`parsimony/stability.py`, `parsimony/site.py`): everything uses all tasks. An unscored task counts at the middle of its bounds for scores and ranking, at its worst and best case for intervals; a difference is "distinguishable" only in the worst case. Items `task#attempt` of one task are resampled together; with one item per task this is identical to a plain task bootstrap.
- Older result sets (`examples/ten-model-500`, `beta-500-*`) are history and use older analyzers.

## Environment

- Python **3.14.7** exactly: panels and records are pinned to it, and scoring rejects other versions. `uv python install 3.14.7` (needs a recent uv).
- Python analysis is standard-library only. Non-Python analysis requires the exact optional pins in `.[languages]`; see `docs/language-tracks.md`. All 7,696 new attempt records were measured in a clean detached checkout at `7705e8de13343bbafbfe5bccba665dd2bab8b24a`. Keep that revision for reproduction; do not measure with the later UI-only source hash.
- Network: GitHub (raw and API), `swe-bench-submissions.s3.amazonaws.com`, `huggingface.co` / `datasets-server.huggingface.co` (Verified dataset), `deepswe.datacurve.ai` and `d3ujjcmjq6o8v6.cloudfront.net` (DeepSWE runs and patches).
- Downloads are cached by URL under `.parsimony-cache/` (never refreshed; use `--cache` before the subcommand).
- Checks before every push: `python -m unittest discover -s tests -q` and `python -m parsimony.contribute validate submissions`. Run the suite with `.[languages]` installed too. Latest verification: 140 tests passed with all parsers (15 optional tests skip without them), all five generated pages passed Node interaction checks, Chromium checked task switching/plot rendering, and all new coverage audits plus byte-identical score reproduction passed.

## Rules that bite

- **Measure only from a clean, committed checkout.** Records carry `analyzer_commit` and a hash of every file in `parsimony/`; a dirty tree gives `analyzer_commit: null`, and `release audit` requires the population's commit. Do not edit `parsimony/` while measurements run: runs that start later import the edited code.
- `release freeze` refuses a dirty checkout; freeze the population after committing, at the commit you measure with.
- Never pool records from different analyzer versions or Python versions (scoring enforces it).
- Freezing a panel needs every task to have a measured, in-scope passing patch: for SWE-bench, filter the records to those tasks first (see `examples/mini-swe-agent-500/README.md`); `parsimony.deepswe panel` filters itself.
- Before publishing numbers, spot-check error counts per run: every broken input so far (stripped newlines, wrong S3 folders, scratch scripts, a results file marking all tasks unresolved) first showed up as an odd count.

## Rebuilding the boards

DeepSWE (full commands in its README):

```sh
git clone https://github.com/datacurve-ai/deep-swe && git -C deep-swe checkout 0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea
python -m parsimony.deepswe dataset deep-swe --output deepswe-python.jsonl        # SHA256 41a44998…
python -m parsimony.deepswe configs --output configs.json
python -m parsimony.deepswe analyze CONFIG --dataset deepswe-python.jsonl --output CONFIG.jsonl
python -m parsimony.deepswe panel examples/deepswe-python/*.jsonl --name NAME --output score-panel.json
```

Site pages:

```sh
NAV=(--nav 'DeepSWE Python=index.html' --nav 'DeepSWE JS=javascript.html' --nav 'DeepSWE TS=typescript.html' --nav 'DeepSWE Go=go.html' --nav 'SWE-bench Verified=verified.html')
for lang in python javascript typescript go; do
  E=examples/deepswe-$lang; PAGE=$lang; [ "$lang" = python ] && PAGE=index
  python -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --sensitivity "$E/sensitivity.json" --benchmark deepswe "${NAV[@]}" --output "site/$PAGE.html"
done
V=examples/mini-swe-agent-500
python -m parsimony.site "$V/score-panel.json" "$V/"*.jsonl --sensitivity "$V/sensitivity.json" --benchmark verified "${NAV[@]}" --output site/verified.html
```

The Verified dataset is `python -m parsimony dataset --output verified.jsonl` (SHA256 `82029e78…`), experiments revision `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`.

## DeepSWE specifics

- Run index: `https://deepswe.datacurve.ai/artifacts/v1.1/trials.json` (51 MB); patch URLs from `release.json` (`artifact_base_url` + `artifact_patterns.model_patch`). The CDN answers **403** for unpublished patches; the importer treats that as missing.
- One configuration per model: the best `pass_rate` on `leaderboard-live.json` whose patches download. GPT-6 Astra and Gemini 3.8 Flash had none published on 2026-09-27; re-run `configs` to pick them up later.
- Each attempt is an item `task#k` (k by start time). The pooled panel labels references `agent#k`; `stability.reference_agent` strips the attempt.
- Most DeepSWE patches exceed the exact diff's 500-edit limit, so records use the flagged approximate alignment.
- Only 34 of 113 tasks are Python; the rest are TypeScript (35), Go (34), JavaScript (5), Rust (5).

## Open ideas, roughly in priority order

1. **Keep footprint scoring over all tasks (owner clarification, 2026-09-28).** Never rank only by solved-task footprint: failed attempts and their added/changed code must count too. The solved-only headline change was reverted. Keep the all-task score and uncertainty as the headline; per-solve footprint is a diagnostic only. Missing measurements remain bounds, not dropped observations. The current metric measures code footprint, not design complexity directly.
2. **More DeepSWE tasks:** JS/TS/Go tracks are published: 70 of 74 additional task definitions calibrate (108 definitions / 103 scored task clusters including Python). Next priority: TypeScript grammar coverage. `effect-sse-httpapi-streaming` and `kea-atomic-signal-selectors` lack usable passing references; pinned grammars also reject some valid constructs in other tasks. Upstream TS metadata incorrectly labels `httpx-deterministic-cookie-store` (Python) and `prometheus-transactional-reload-status` (Go); these remain recorded as out of scope, not reassigned silently. See each new example README for counts. Rust remains unsupported.
3. **Keep DeepSWE current:** fresh-cache check on 2026-09-28 found the same 26 configurations and identical trials hash. Gemini 3.8 patch probes remain 403; GPT-6 Astra declares no patches. Evidence: `examples/deepswe-python/refresh-2026-09-28.json`. SWE-Atlas investigation in `docs/swe-atlas-investigation.md`: blocked on unavailable public model patch/per-attempt result exports, not task definitions.
4. **Report broken SWE-bench submissions upstream** (`SWE-bench/experiments`): Gemini 3 Pro (high) `per_instance_details.json` marks all 500 tasks unresolved; GPT-5.2 Codex has no results file; Claude 3.7 Sonnet has 402 patches missing on S3; four runs' `metadata.yaml` name wrong S3 folders.
5. **Blind preference check** (roadmap item 4): side-by-side passing patches, which one would a reviewer merge.
6. **Repository size:** result sets add tens of MB per refresh (panels are 19–25 MB); consider GitHub release assets for raw JSONL.
7. Other sources checked on 2026-09-27: SWE-bench-Live (fresh Python tasks, patches public, but each submission uses a different agent), SWE-bench Pro (public logs stop at late-2025 models), SWE-rebench (no patches published).
