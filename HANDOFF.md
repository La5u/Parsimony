# Handoff (2026-09-27)

State of Parsimony after the cloud sessions of 2026-09-26/27, for continuing locally in Claude Code. Owner preference: commit and push directly to `main`; no branches or pull requests.

## Where things stand

- **Site** (Cloudflare Pages, output directory `site`, served at https://parsimony.lasu.dev; every push to `main` redeploys):
  - `site/index.html` is the main board: [DeepSWE](examples/deepswe-python/README.md), 26 current models × 34 Python tasks × 4 attempts.
  - `site/verified.html` is the second board: [SWE-bench Verified](examples/mini-swe-agent-500/README.md), 33 mini-SWE-agent models × 500 tasks.
  - The leaderboard shows a 95% bootstrap **rank range** per model (no tiers). Score, 95% CI, Solved, Per solve and Median churn headers now toggle numeric sorting; default is all-task score descending. CI sorts by its lower bound; churn starts ascending; missing values stay last. Rank ranges always refer to the all-task score, regardless of the selected sort. A Node.js interaction test runs through unittest when Node is available.
- **Analyzer 0.5.2-beta** (see [CHANGELOG](CHANGELOG.md)): repairs patch files missing their final newline, falls back to the standard S3 logs folder when `metadata.yaml` names a wrong one, and excludes new root-level files (agent scratch scripts).
- **Statistics** (`parsimony/stability.py`, `parsimony/site.py`): everything uses all tasks. An unscored task counts at the middle of its bounds for scores and ranking, at its worst and best case for intervals; a difference is "distinguishable" only in the worst case. Items `task#attempt` of one task are resampled together; with one item per task this is identical to a plain task bootstrap.
- Older result sets (`examples/ten-model-500`, `beta-500-*`) are history and use older analyzers.

## Environment

- Python **3.14.7** exactly: panels and records are pinned to it, and scoring rejects other versions. `uv python install 3.14.7` (needs a recent uv).
- Standard library only for the package.
- Network: GitHub (raw and API), `swe-bench-submissions.s3.amazonaws.com`, `huggingface.co` / `datasets-server.huggingface.co` (Verified dataset), `deepswe.datacurve.ai` and `d3ujjcmjq6o8v6.cloudfront.net` (DeepSWE runs and patches).
- Downloads are cached by URL under `.parsimony-cache/` (never refreshed; use `--cache` before the subcommand).
- Checks before every push: `python -m unittest discover -s tests -q` and `python -m parsimony.contribute validate submissions`.

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
E=examples/deepswe-python; V=examples/mini-swe-agent-500
NAV=(--nav "DeepSWE (26 current models)=index.html" --nav "SWE-bench Verified (33 models, 2025–26)=verified.html")
python -m parsimony.site $E/score-panel.json $E/*.jsonl --sensitivity $E/sensitivity.json --benchmark deepswe "${NAV[@]}" --output site/index.html
python -m parsimony.site $V/score-panel.json $V/*.jsonl --sensitivity $V/sensitivity.json --benchmark verified "${NAV[@]}" --output site/verified.html
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
2. **More DeepSWE tasks:** measuring TypeScript and Go (likely via tree-sitter as an optional dependency, a separate versioned track) would take DeepSWE from 34 to 103 tasks.
3. **Keep DeepSWE current:** re-run `configs` and `analyze` when new models appear (the live leaderboard updates).
4. **Report broken SWE-bench submissions upstream** (`SWE-bench/experiments`): Gemini 3 Pro (high) `per_instance_details.json` marks all 500 tasks unresolved; GPT-5.2 Codex has no results file; Claude 3.7 Sonnet has 402 patches missing on S3; four runs' `metadata.yaml` name wrong S3 folders.
5. **Blind preference check** (roadmap item 4): side-by-side passing patches, which one would a reviewer merge.
6. **Repository size:** result sets add tens of MB per refresh (panels are 19–25 MB); consider GitHub release assets for raw JSONL.
7. Other sources checked on 2026-09-27: SWE-bench-Live (fresh Python tasks, patches public, but each submission uses a different agent), SWE-bench Pro (public logs stop at late-2025 models), SWE-rebench (no patches published).
