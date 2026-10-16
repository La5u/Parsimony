# 35 configurations × 500 Verified tasks (analyzer 0.5.2)

**Experimental footprint comparison, not an official coding-ability ranking.** The [Verified board](../../site/verified.html) contains 34 source-reported model + mini-SWE-agent configurations (v0.0.0 to v2.4.2, July 2025 to September 2026) and one GLM-5.1 + EvalScope configuration, over every one of the 500 Verified tasks. Rank uses the same-task ratio: a model's net coding units added on the tasks it solved, divided by what the other ranked models added on those same tasks; the plain solved mean and the all-measured mean are shown beside it. Solved-only mean, upstream Solved % and Measured coverage are separate context. Missing footprints are not zeros; harness versions differ.

## Latest addition: GLM-5.1 · EvalScope

GLM-5.1 comes from a third-party Hugging Face export, [fxiao0369/GLM51-swebench-replay at `5c03de1`](https://huggingface.co/datasets/fxiao0369/GLM51-swebench-replay/tree/5c03de18c6ef604d8cd95da95c1335b717fc0936) (MIT), run with EvalScope's agentic SWE-bench harness, **not mini-SWE-agent**: it is a model + agent configuration, not a controlled comparison with the other rows. Pass/fail is the uploader's own per-task `resolved` value (363/500), not the official leaderboard. **491 of 494 nonempty patches** were measured with the same 0.5.2-beta commit, source hash and Python 3.14.7; 3 are analysis errors and the 6 empty predictions are `no_generation`, not zero. The export strips trailing whitespace from every patch, which drops final blank context lines; for 85 patches exactly the missing blank lines were restored before analysis (each record keeps `source_patch_sha256` and `trailing_context_lines_restored`, and context is still checked against the base commit). Reproduce with [`add-glm51-verified.py`](../benchmark-discovery/add-glm51-verified.py). Current 35-configuration reports: [coverage-35.json](coverage-35.json), [scores-35.json](scores-35.json), [sensitivity-35.json](sensitivity-35.json)/[report](sensitivity-35.md); the 34-configuration files are frozen snapshots.

## Gemini 3.5 Flash

Gemini 3.5 Flash / mini-SWE-agent 2.4.2 adds **441/500 eligible footprints**: 359 passing and 82 failed. The remaining 59 are explicitly source-reported `no_generation`, not fabricated failures or zero-footprint patches. Upstream Solved is **71.8%**; mean net units added is **36.6031746031746**. All 441 separate patches match their monolithic predictions. Analysis used the exact existing 0.5.2 commit/source hash and Python 3.14.7, with no identity relabelling. Human-reference comparisons are intentionally not computed for this addition.

See [release/provenance/reproduction notes](../../docs/archive/gemini-3.5-verified-release.md) and [numerical/hash publication evidence](gemini-3-5-publication-evidence.json). Raw patches, source, prompts and trajectories are not distributed. Existing 33-model records, the 500-task population and archived 33-model passing-reference panel remain unchanged. The site shows 35 configurations; the latest saved reports cover 34: [coverage-34.json](coverage-34.json), [scores-34.json](scores-34.json) and [sensitivity-34.json](sensitivity-34.json)/[report](sensitivity-34.md); the original report files below are historical snapshots, not the current footprint ranking.

## Pinned inputs

- Analyzer commit `0aa66df`, version `0.5.2-beta`, Python 3.14.7. 0.5.2 repairs patch files that lost their final newline, finds patches when `metadata.yaml` names the wrong folder, and excludes scratch scripts at the repository root (see the [changelog](../../CHANGELOG.md)). All 39 measured runs (34 displayed and five older harness duplicates), including the ten-model runs, use it.
- Scoring `parsimony-80-20-v0.5` (80% net units / 20% churn), panel `mini-swe-agent-33-448-solved-80-20-v0.5`.
- Dataset SHA256 `82029e78b26e1da0ddc01653c98db18443fab1993e28dff052a38b01c3fd77f7`, experiments revision `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`.
- Historical 33-model report SHA256 (unchanged): [population.json](population.json) `02a66572…`, [score-panel.json](score-panel.json) `4d18e67f…`, [scores.json](scores.json) `4267ebb6…`, [coverage.json](coverage.json) `43d78bc1…`, [sensitivity.json](sensitivity.json) `07380194…`.

```sh
# For each submission in the tables below (full names are the `agent` field of each JSONL file):
python -m parsimony analyze SUBMISSION --dataset verified.jsonl \
  --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d --include-failed --output NAME.jsonl
# Gemini requires the dedicated bound inventory/measurement driver linked above.
# Keep the existing frozen 33-model passing-reference panel and 500-task population.
# Do not overwrite the historical 33-model report files when adding a configuration:
python -m parsimony.release audit population.json *.jsonl --output coverage-34.json
python -m parsimony.scoring score score-panel.json *.jsonl --output scores-34.json
python -m parsimony.stability score-panel.json *.jsonl --output sensitivity-34.json
# For the current 34-configuration board, use the shared-navigation rebuild in HANDOFF.md:
python -m parsimony.site score-panel.json *.jsonl --sensitivity sensitivity-34.json --benchmark verified --output site/verified.html
```

## Ranking (same tasks)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Qwen2.5-Coder 32B | 0.41× | −0.51 to 1.03× | 42 | +4.6 | -40.3 | 9.0% | 43/45 |
| 2 | Gemini 2.5 Pro | 0.54× | 0.46–0.62× | 264 | +10.3 | +9.3 | 53.6% | 264/268 |
| 3 | Claude Opus 4.5 (high) | 0.67× | 0.59–0.76× | 378 | +15.5 | +21.6 | 76.8% | 384/384 |
| 4 | Gemini 3 Flash (high) | 0.74× | 0.62–0.86× | 375 | +20.1 | +25.1 | 75.8% | 379/379 |
| 5 | Gemini 3 Pro (preview) | 0.75× | 0.65–0.85× | 368 | +17.1 | +23.2 | 74.2% | 370/371 |
| 6 | Claude Opus 4.6 | 0.75× | 0.66–0.83× | 373 | +18.7 | +22.8 | 75.6% | 378/378 |
| 7 | Claude Sonnet 4 | 0.77× | 0.09–1.15× | 324 | +16.5 | +53.7 | 64.8% | 324/324 |
| 8 | MiniMax M2.5 (high) | 0.83× | 0.68–0.98× | 373 | +22.2 | +26.1 | 75.8% | 379/379 |
| 9 | Kimi K2.5 (high) | 0.85× | 0.75–0.96× | 354 | +19.7 | +25.5 | 70.8% | 354/354 |
| 10 | Claude Haiku 4.5 (high) | 0.87× | 0.71–1.03× | 333 | +20.2 | +30.3 | 66.6% | 333/333 |
| 11 | Devstral 2512 | 0.87× | 0.65–1.09× | 268 | +19.5 | +23.8 | 53.8% | 269/269 |
| 12 | GLM-5.1 · EvalScope | 0.88× | 0.78–1.01× | 358 | +20.8 | +26.9 | 72.6% | 363/363 |
| 13 | o4-mini | 0.92× | 0.75–1.13× | 222 | +15.9 | -51.7 | 45.0% | 223/225 |
| 14 | o3 | 0.93× | 0.77–1.14× | 292 | +18.8 | +20.9 | 58.4% | 292/292 |
| 15 | Llama 4 Maverick | 0.94× | 0.56–1.70× | 104 | +10.0 | -244.2 | 21.0% | 104/105 |
| 16 | Kimi K2 Instruct | 0.95× | 0.77–1.20× | 216 | +16.9 | +0.8 | 43.8% | 216/219 |
| 17 | Claude Sonnet 4.5 (high) | 0.95× | 0.84–1.07× | 357 | +21.2 | +29.2 | 71.4% | 357/357 |
| 18 | GLM-5 (high) | 0.97× | 0.87–1.08× | 360 | +22.1 | +30.4 | 72.8% | 364/364 |
| 19 | GPT-5 mini | 0.98× | 0.77–1.20× | 281 | +22.0 | +26.2 | 56.2% | 281/281 |
| 20 | GPT-5.1 | 1.01× | 0.88–1.15× | 327 | +20.4 | +27.4 | 66.0% | 329/330 |
| 21 | GPT-5.1 Codex | 1.03× | 0.91–1.18× | 330 | +21.4 | +26.9 | 66.0% | 330/330 |
| 22 | Qwen3-Coder 480B | 1.05× | 0.89–1.22× | 271 | +18.9 | +29.5 | 55.4% | 273/277 |
| 23 | GLM-4.6 | 1.06× | 0.89–1.27× | 273 | +20.3 | +62.5 | 55.4% | 273/277 |
| 24 | Claude Opus 4 | 1.10× | 0.98–1.25× | 336 | +23.4 | +31.0 | 67.6% | 337/338 |
| 25 | GPT-5 | 1.11× | 0.99–1.25× | 318 | +21.8 | +27.6 | 65.0% | 319/325 |
| 26 | GPT-5 nano | 1.12× | 0.86–1.41× | 173 | +17.3 | -16.8 | 34.8% | 173/174 |
| 27 | gpt-oss-120b | 1.16× | 0.71–1.71× | 122 | +15.0 | -82.2 | 26.0% | 123/130 |
| 28 | gemini-3-5-flash | 1.17× | 1.05–1.30× | 347 | +28.7 | +36.6 | 71.8% | 359/359 |
| 29 | GPT-5.2 | 1.22× | 1.01–1.44× | 343 | +28.5 | +42.9 | 69.0% | 345/345 |
| 30 | DeepSeek V3.2 (high) | 1.22× | 1.11–1.34× | 348 | +27.6 | +35.4 | 70.0% | 350/350 |
| 31 | GLM-4.5 | 1.25× | 0.82–2.01× | 267 | +21.9 | +27.0 | 54.2% | 267/271 |
| 32 | Devstral Small 2512 | 1.30× | 0.19–2.56× | 279 | +27.4 | +52.2 | 56.4% | 280/282 |
| 33 | Kimi K2 Thinking | 1.38× | 0.98–1.93× | 313 | +32.4 | +38.1 | 63.4% | 314/317 |
| 34 | MiniMax M2 | 1.43× | 1.09–1.97× | 299 | +29.7 | +41.1 | 61.0% | 302/305 |
| 35 | GPT-5.2 (high) | 1.67× | 1.45–1.90× | 362 | +36.6 | +50.9 | 72.8% | 364/364 |

## Which runs are included

All 48 mini-SWE-agent runs on Verified at the pinned revision were checked; 39 are measured here.

- **34 on the footprint board**, one per model. Where a model was run twice, the v2.0.0 run is shown.
- **5 older duplicate runs** (GPT-5 mini v1.7.0, Claude Sonnet 4.5 v1.13.3, Claude Opus 4.5 v1.16.0, DeepSeek V3.2 v1.17.1, GPT-5.2 (high) v1.17.2) are in [agent-version-check/](agent-version-check/), scored against the same panel but not references.
- **Left out:** Claude 3.7 Sonnet (402 of 500 patches missing from S3), Llama 4 Scout, GPT-4o, GPT-4.1, GPT-4.1 mini, Gemini 2.0 Flash, Gemini 2.5 Flash and GPT-5.2 Codex (no per-task results file), Gemini 3 Pro (high) (its results file marks all 500 tasks unresolved although its metadata reports 69.6%). Gemini 3.5 Flash's artifact blocker is now resolved by pinned submitter-repository patches plus explicit aggregate no-generation evidence.

## Archived combined-score reference panel (unchanged)

- **448 tasks** that at least one of the 33 models solved with a measurable patch. The other 52 do not calibrate the archived combined score against this panel. All 500 tasks remain in the footprint population; measured attempts on these 52 tasks still contribute to default rank. Choosing tasks by panel success is a known score-panel bias, not a footprint eligibility rule.
- **Reference panel:** every measured, in-scope solved patch of the 33 models on those tasks. Identical patches from different models are not deduplicated.

## Historical 33-model coverage

| Model | Resolved | Failed measured | Errors | Missing patch | Units unknown | Newline restored | Scratch files excluded |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.5 (high) | 384 | 115 | 1 | 0 | 0 | 0 | 0 |
| Claude Opus 4.6 | 378 | 121 | 1 | 0 | 0 | 0 | 0 |
| MiniMax M2.5 (high) | 379 | 117 | 4 | 0 | 0 | 0 | 0 |
| Gemini 3 Pro (preview) | 371 | 128 | 2 | 0 | 0 | 0 | 61 |
| Kimi K2.5 (high) | 354 | 146 | 0 | 0 | 1 | 0 | 0 |
| Gemini 3 Flash (high) | 379 | 121 | 0 | 0 | 0 | 0 | 0 |
| GLM-5 (high) | 364 | 135 | 1 | 0 | 0 | 0 | 0 |
| Claude Sonnet 4.5 (high) | 357 | 141 | 2 | 0 | 0 | 0 | 0 |
| Claude Opus 4 | 338 | 160 | 3 | 0 | 0 | 480 | 369 |
| Claude Haiku 4.5 (high) | 333 | 167 | 0 | 0 | 0 | 0 | 0 |
| Kimi K2 Thinking | 317 | 182 | 4 | 0 | 1 | 0 | 455 |
| Gemini 2.5 Pro | 268 | 211 | 23 | 2 | 8 | 493 | 202 |
| GPT-5.1 | 330 | 168 | 3 | 0 | 0 | 0 | 66 |
| Claude Sonnet 4 | 324 | 174 | 1 | 1 | 0 | 499 | 395 |
| GPT-5.1 Codex | 330 | 169 | 1 | 0 | 0 | 0 | 41 |
| GPT-5 | 325 | 172 | 9 | 0 | 1 | 497 | 69 |
| GPT-5.2 | 345 | 135 | 20 | 0 | 0 | 0 | 43 |
| DeepSeek V3.2 (high) | 350 | 149 | 1 | 0 | 2 | 0 | 0 |
| MiniMax M2 | 305 | 190 | 7 | 0 | 1 | 0 | 441 |
| GLM-4.5 | 271 | 219 | 12 | 2 | 2 | 0 | 426 |
| Devstral Small 2512 | 282 | 217 | 3 | 0 | 1 | 0 | 211 |
| o3 | 292 | 205 | 3 | 0 | 5 | 490 | 65 |
| GPT-5.2 (high) | 364 | 136 | 0 | 0 | 0 | 0 | 0 |
| Devstral 2512 | 269 | 228 | 3 | 0 | 1 | 2 | 168 |
| GLM-4.6 | 277 | 215 | 11 | 1 | 0 | 1 | 395 |
| Qwen3-Coder 480B | 277 | 214 | 12 | 1 | 10 | 478 | 382 |
| GPT-5 mini | 281 | 209 | 10 | 0 | 1 | 0 | 0 |
| Kimi K2 Instruct | 219 | 274 | 8 | 2 | 3 | 405 | 273 |
| o4-mini | 225 | 244 | 31 | 1 | 43 | 491 | 159 |
| GPT-5 nano | 174 | 316 | 11 | 0 | 6 | 420 | 55 |
| gpt-oss-120b | 130 | 322 | 49 | 5 | 33 | 439 | 191 |
| Llama 4 Maverick | 105 | 313 | 82 | 1 | 53 | 0 | 218 |
| Qwen2.5-Coder 32B | 45 | 154 | 299 | 4 | 16 | 238 | 77 |

**Newline restored:** runs up to v1.7.0 stored patch files without their final newline; 0.5.2 restores it. Without this, most of those runs' solved patches could not be measured (for example 244 of o3's 292). **Scratch files excluded:** patches, mostly from runs before v2.0.0, that added scripts such as `reproduce_issue.py` at the repository root; those files are not counted. 46 solved and 591 failed patches could not be measured (Errors and Missing patch); their tasks get a score range instead of a point.

## Historical 33-model combined-score results (not footprint ranks)

| Rank (95%) | Model | Agent | Score | 95% interval | Resolved | Per solve | Median net units | Median churn |
|---:|---|---|---:|---|---:|---:|---:|---:|
| 1 | Claude Opus 4.5 (high) | v2.0.0 | 51.3–51.4 | 48.7–54.1 | 76.8% | 61.5 | +6.5 | 11 |
| 2–3 | Claude Opus 4.6 | v2.0.0 | 48.3 | 45.4–51.0 | 75.6% | 58.7 | +8 | 12 |
| 2–4 | MiniMax M2.5 (high) | v2.0.0 | 46.5–46.7 | 43.8–49.4 | 75.8% | 56.8 | +8 | 12 |
| 3–7 | Gemini 3 Pro (preview) | v1.15.0 | 44.0–44.2 | 41.1–47.2 | 74.2% | 55.3 | +8 | 13 |
| 4–7 | Kimi K2.5 (high) | v2.0.0 | 43.4–43.5 | 40.4–46.5 | 70.8% | 57.5 | +7 | 11 |
| 4–7 | Gemini 3 Flash (high) | v2.0.0 | 42.7 | 40.0–45.5 | 75.8% | 52.5 | +10 | 14 |
| 5–7 | GLM-5 (high) | v2.0.0 | 41.3 | 38.5–44.3 | 72.8% | 53.0 | +9 | 13 |
| 8–9 | Claude Sonnet 4.5 (high) | v2.0.0 | 37.9–38.0 | 35.2–40.8 | 71.4% | 50.4 | +9 | 14 |
| 9–14 | Claude Opus 4 | v1.0.0 | 34.5–34.8 | 31.6–37.7 | 67.6% | 48.9 | +10 | 14 |
| 9–14 | Claude Haiku 4.5 (high) | v2.0.0 | 34.4 | 31.5–37.3 | 66.6% | 50.4 | +8 | 13 |
| 9–15 | Kimi K2 Thinking | v1.17.2 | 33.7–34.6 | 30.4–37.7 | 63.4% | 52.6 | +7 | 11.5 |
| 9–16 | Gemini 2.5 Pro | v1.0.0 | 32.4–34.7 | 28.7–38.1 | 53.6% | 62.2 | +5 | 9 |
| 9–16 | GPT-5.1 | v1.15.0 | 33.2–33.5 | 30.2–36.6 | 66.0% | 49.1 | +10 | 14 |
| 11–19 | Claude Sonnet 4 | v1.0.0 | 31.8–31.9 | 28.9–35.0 | 64.8% | 48.4 | +8 | 12 |
| 11–20 | GPT-5.1 Codex | v1.16.0 | 31.5 | 28.8–34.4 | 66.0% | 46.1 | +10.5 | 16 |
| 13–23 | GPT-5 | v1.7.0 | 29.5–31.0 | 26.7–34.1 | 65.0% | 45.3 | +9 | 13 |
| 13–24 | GPT-5.2 | v1.17.2 | 29.6–30.6 | 26.4–33.7 | 69.0% | 43.3 | +11 | 17 |
| 15–25 | DeepSeek V3.2 (high) | v2.0.0 | 29.0–29.2 | 26.3–32.0 | 70.0% | 40.8 | +12.5 | 18 |
| 15–25 | MiniMax M2 | v1.17.0 | 28.5–29.4 | 25.4–32.7 | 61.0% | 47.4 | +10 | 13 |
| 15–26 | GLM-4.5 | v1.9.1 | 27.9–29.3 | 24.5–32.6 | 54.2% | 53.8 | +7 | 10 |
| 15–26 | Devstral Small 2512 | v1.17.2 | 28.2–28.9 | 24.9–32.3 | 56.4% | 50.4 | +8.5 | 11.5 |
| 15–26 | o3 | v1.0.0 | 28.2–28.6 | 25.0–31.9 | 58.4% | 48.9 | +8 | 12 |
| 16–26 | GPT-5.2 (high) | v2.0.0 | 28.2 | 25.6–31.1 | 72.8% | 37.9 | +15.5 | 24 |
| 16–26 | Devstral 2512 | v1.17.2 | 27.8–28.3 | 24.8–31.3 | 53.8% | 51.2 | +8 | 12 |
| 18–27 | GLM-4.6 | v1.17.1 | 26.3–27.9 | 23.1–31.1 | 55.4% | 49.5 | +8 | 13 |
| 20–27 | Qwen3-Coder 480B | v1.0.0 | 25.2–27.1 | 22.0–30.3 | 55.4% | 48.4 | +8 | 11 |
| 24–28 | GPT-5 mini | v2.0.0 | 24.2–24.8 | 21.1–27.8 | 56.2% | 44.7 | +9 | 13 |
| 27–29 | Kimi K2 Instruct | v1.7.0 | 21.2–22.6 | 18.2–25.7 | 43.8% | 51.5 | +6 | 9 |
| 28–29 | o4-mini | v1.0.0 | 17.4–21.7 | 14.1–25.0 | 45.0% | 49.4 | +7 | 11 |
| 30 | GPT-5 nano | v1.7.0 | 11.1–12.5 | 8.3–15.4 | 34.8% | 43.1 | +8 | 12 |
| 31–32 | gpt-oss-120b | v1.7.0 | 3.1–10.1 | 0.3–13.0 | 26.0% | 46.2 | +6 | 9.5 |
| 31–32 | Llama 4 Maverick | v0.0.0 | 0.9–9.5 | −2.3–12.3 | 21.0% | 55.6 | +4 | 5.5 |
| 33 | Qwen2.5-Coder 32B | v1.0.0 | −12.9–4.2 | −15.1–5.9 | 9.0% | 52.7 | +3 | 4 |

- **Rank (95%)** is the range covering 95% of the model's ranks over 2,000 paired resamples of the tasks. Overlapping ranges mean the order is uncertain; only a few neighbours are clearly separated (see the [stability report](sensitivity.md)).
- **Score and intervals** use all 448 tasks. An unscored task counts at the middle of its range for the score and ranking, and at its best and worst case for the interval.
- **The score is mostly correctness.** A solved task scores 1–100 and a failure −25–0, so resolve rate dominates. *Per solve* isolates footprint: Gemini 2.5 Pro, Claude Opus 4.5, Claude Opus 4.6 and Kimi K2.5 write the smallest successful patches (57–62); GPT-5.2 (high) and DeepSeek V3.2 the largest (38–41).

## Agent version matters

Five models were run under two mini-SWE-agent versions. Scored against the same panel:

| Model | Older run | Score | Resolved | Per solve | v2.0.0 score | Resolved | Per solve |
|---|---|---:|---:|---:|---:|---:|---:|
| GPT-5 mini | v1.7.0 | 25.8–26.4 | 59.8% | 44.2 | 24.2–24.8 | 56.2% | 44.7 |
| Claude Sonnet 4.5 (high) | v1.13.3 | 37.6–38.0 | 70.6% | 51.0 | 37.9–38.0 | 71.4% | 50.4 |
| Claude Opus 4.5 (high) | v1.16.0 | 45.7 | 74.4% | 57.5 | 51.3–51.4 | 76.8% | 61.5 |
| DeepSeek V3.2 (high) | v1.17.1 | 27.9–30.3 | 60.0% | 48.4 | 29.0–29.2 | 70.0% | 40.8 |
| GPT-5.2 (high) | v1.17.2 | 31.0–31.4 | 71.8% | 42.3 | 28.2 | 72.8% | 37.9 |

The same model moves by up to 5.6 points, and per-solve footprint shifts in both directions. That is larger than many gaps between neighbouring models, so **differences between models run under different agent versions (the Agent column) are not purely model differences.** Only the eleven v2.0.0 runs share one harness.

## Limits

Everything in the [main README](../../README.md#limits-and-interpretation) applies. Units measure size and nesting, not readability; scores are relative to these 33 models; the agent version varies; and correctness is taken from published results.
