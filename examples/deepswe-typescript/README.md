# DeepSWE v1.1 — TypeScript task track

**Beta research preview, not an official ranking.** 26 configurations (one per model), 35 upstream-TypeScript-labelled tasks × four attempts; 3,640 records including failed and unavailable attempts. The [website board](../../site/typescript.html) ranks by the same-task ratio: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks; the all-measured mean is shown beside it. Language tracks have separate reference panels and syntax-unit definitions: do not pool them or compare raw counts across tracks.

## Pinned inputs and analyzer

- Tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`.
- Release `v1.1`, fresh-cache run index SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Same 26 configurations as the Python board; [refresh evidence](../deepswe-python/refresh-2026-09-28.json). Gemini 3.8 and GPT-6 Astra artifacts are still unavailable; no model outcomes were invented.
- Analyzer **0.7.0-beta**, clean measurement commit `ca37c314d84d1d5949e2080077c6afc30b916394`, Python **3.14.7**. Dataset SHA256 `c03deb677cef4101524071ec7c83ba044b153f8dce96590c75bb3c9c179f54c7`.
- Unit track `typescript-compiler-units-v1`: the official TypeScript parser, `typescript@5.9.3`, syntax only. The 0.6.0-beta Tree-sitter records (`tree-sitter-units-v1`) were replaced, not mixed; they were last present at commit `ca37c31` and their raw counts are not comparable. [Why the parser changed](../../docs/archive/typescript-parser-investigation.md). [Rules and limitations](../../docs/language-tracks.md).
- [Population](population.json) contains every attempt; [coverage audit](coverage.json) validates the original dataset, record completeness, base commits and analyzer commit. [Score panel](score-panel.json), [scores](scores.json), [stability](sensitivity.md).

## Coverage before rankings

The frozen population has **140 attempts per model**. The score panel can calibrate **33 of 35 tasks** (132 items): it needs at least one measured, in-scope passing reference per task. Scores, CIs, task selection and the plot's measured-attempt means (including failures) use this score panel; published resolve rate retains the entire population denominator. Attempts from uncalibrated tasks remain in the raw records and coverage report.

Status totals: `error` 5, `not_resolved` 24, `ok` 3,611 (0.6.0-beta: 323 errors). A parser/analysis error means **unmeasured**, not benchmark failure or zero footprint. Missing measurements within the panel contribute score bounds. Upstream unknown outcomes remain unknown.

Tasks without a usable passing reference: `httpx-deterministic-cookie-store`, `prometheus-transactional-reload-status`. Upstream metadata labels both TypeScript although their patches are Python and Go, so their changes are outside this track. They are retained as excluded-only records, not silently moved into another frozen population.

**The five remaining analysis errors** are not parser gaps: three patches leave invalid TypeScript (`dynamodb-toolbox-conditional-attribute-requirements`, `dynamodb-toolbox-lazy-recursive-schemas`, `obsidian-linter-auto-table-of-contents`), one leaves an invalid root-level `.cjs` scratch script (`effect-sse-httpapi-streaming`), and one is an unsupported binary/rename/mode-only implementation diff. Each error names the file and line in `analysis_error`. Interpret this track's coverage before any rank claim.

| Model | Published solved | Measured passing | Measured failed | Analysis errors | Missing patches |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 89 / 140 | 89 | 51 | 0 | 0 |
| Claude Opus 4.8 (max) | 64 / 140 | 64 | 67 | 0 | 0 |
| Claude Opus 5 (max) | 88 / 140 | 88 | 49 | 0 | 0 |
| Claude Sonnet 4.6 (high) | 44 / 140 | 44 | 94 | 1 | 0 |
| Claude Sonnet 5 (max) | 69 / 140 | 69 | 69 | 0 | 0 |
| DeepSeek V4 Flash (max) | 73 / 140 | 73 | 67 | 0 | 0 |
| DeepSeek V4 Pro (max) | 86 / 140 | 86 | 54 | 0 | 0 |
| GLM-5.2 (max) | 61 / 140 | 61 | 79 | 0 | 0 |
| GLM-5.3 (max) | 85 / 140 | 85 | 55 | 0 | 0 |
| GLM-5.3 Flash (max) | 72 / 140 | 72 | 67 | 0 | 0 |
| GPT-5.4 (xhigh) | 70 / 140 | 70 | 70 | 0 | 0 |
| GPT-5.5 (xhigh) | 87 / 140 | 87 | 53 | 0 | 0 |
| GPT-5.6 Luna (max) | 81 / 140 | 81 | 55 | 0 | 0 |
| GPT-5.6 Sol (max) | 92 / 140 | 92 | 48 | 0 | 0 |
| GPT-5.6 Terra (max) | 91 / 140 | 91 | 48 | 0 | 0 |
| Gemini 3.1 Pro Preview (high) | 17 / 140 | 17 | 119 | 4 | 0 |
| Gemini 3.5 Flash (high) | 51 / 140 | 51 | 89 | 0 | 0 |
| Gemini 3.6 Flash (high) | 57 / 140 | 57 | 83 | 0 | 0 |
| Gemini 3.7 Flash (medium) | 86 / 140 | 86 | 54 | 0 | 0 |
| Grok 4.5 (high) | 68 / 140 | 68 | 72 | 0 | 0 |
| Grok 4.6 (medium) | 81 / 140 | 81 | 59 | 0 | 0 |
| Kimi K2.7 Code | 39 / 140 | 39 | 101 | 0 | 0 |
| Kimi K3 (max) | 84 / 140 | 84 | 56 | 0 | 0 |
| Muse Spark 1.1 (xhigh) | 68 / 140 | 68 | 72 | 0 | 0 |
| Muse Spark 1.2 (xhigh) | 71 / 140 | 71 | 69 | 0 | 0 |
| Qwen3.8 Max (xhigh) | 75 / 140 | 75 | 62 | 0 | 0 |

“Measured” in the coverage table means full-file analysis completed; the audit separately reports excluded-only successes and unmeasured-unit records. This does not certify upstream test results or patch correctness. Approximate unit alignment is flagged per record.

## Ranking (same tasks)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Kimi K2.7 Code | 0.82× | 0.77–0.87× | 19 | +1,695.8 | +2,034.2 | 27.9% | 38/39 |
| 2 | Gemini 3.5 Flash (high) | 0.83× | 0.74–0.92× | 20 | +1,909.1 | +2,058.0 | 36.4% | 47/51 |
| 3 | Claude Fable 5 (xhigh) | 0.85× | 0.80–0.90× | 29 | +2,078.7 | +2,078.2 | 63.6% | 83/89 |
| 4 | Claude Opus 4.8 (max) | 0.85× | 0.81–0.89× | 22 | +2,062.2 | +2,014.3 | 45.7% | 61/64 |
| 5 | MiMo V2.5 Pro · DeepSWE 1.0 | 0.89× | 0.84–0.94× | 15 | +1,657.4 | +2,063.4 | 25.7% | 32/36 |
| 6 | GLM-5.2 (max) | 0.89× | 0.84–0.95× | 27 | +1,975.1 | +1,932.6 | 43.6% | 58/61 |
| 7 | Claude Sonnet 4.6 (high) | 0.90× | 0.84–0.96× | 16 | +1,981.0 | +2,150.7 | 31.4% | 40/44 |
| 7 | Claude Sonnet 5 (max) | 0.90× | 0.82–0.99× | 25 | +2,122.0 | +2,013.9 | 49.3% | 62/69 |
| 9 | Kimi K3 (max) | 0.93× | 0.89–0.98× | 27 | +2,226.0 | +2,142.5 | 60.0% | 77/84 |
| 10 | Gemini 3.6 Flash (high) | 0.96× | 0.89–1.03× | 23 | +2,296.7 | +2,272.9 | 40.7% | 55/57 |
| 11 | Grok 4.6 (medium) | 0.96× | 0.91–1.01× | 24 | +2,395.7 | +2,392.0 | 57.9% | 73/81 |
| 12 | Qwen3.8 Max (xhigh) | 0.96× | 0.92–1.00× | 27 | +2,278.2 | +2,367.9 | 53.6% | 68/75 |
| 13 | DeepSeek V4 Flash (max) | 0.97× | 0.92–1.03× | 24 | +2,258.0 | +2,408.6 | 52.1% | 66/73 |
| 14 | Claude Opus 4.6 (max) · DeepSWE 1.0 | 0.98× | 0.85–1.16× | 16 | +1,965.0 | +2,165.6 | 31.4% | 40/44 |
| 14 | GLM-5.3 (max) | 0.98× | 0.90–1.07× | 26 | +2,480.9 | +2,362.1 | 60.7% | 80/85 |
| 16 | Grok 4.5 (high) | 0.99× | 0.90–1.09× | 25 | +2,185.1 | +2,364.5 | 48.6% | 61/68 |
| 17 | GLM-5.3 Flash (max) | 0.99× | 0.95–1.04× | 26 | +2,325.3 | +2,419.1 | 51.4% | 68/72 |
| 18 | Claude Opus 4.7 (max) · DeepSWE 1.0 | 1.00× | 0.94–1.07× | 27 | +2,332.2 | +2,533.7 | 52.1% | 70/73 |
| 19 | MiniMax M3 · DeepSWE 1.0 | 1.03× | 0.93–1.14× | 18 | +2,000.8 | +2,514.6 | 22.9% | 28/32 |
| 20 | GPT-5.6 Terra (max) | 1.03× | 0.96–1.10× | 29 | +2,567.5 | +2,542.2 | 65.0% | 84/91 |
| 21 | DeepSeek V4 Pro (max) | 1.03× | 0.99–1.09× | 27 | +2,432.8 | +2,692.8 | 61.4% | 81/86 |
| 22 | GPT-5.6 Sol (max) | 1.05× | 0.97–1.14× | 29 | +2,751.5 | +2,544.4 | 65.7% | 88/92 |
| 23 | Claude Opus 5 (max) | 1.05× | 1.00–1.10× | 28 | +2,538.9 | +2,569.5 | 62.9% | 82/88 |
| 24 | GPT-5.6 Luna (max) | 1.05× | 0.99–1.12× | 27 | +2,437.3 | +2,676.5 | 57.9% | 77/81 |
| 25 | Gemini 3.7 Flash (medium) | 1.09× | 1.04–1.15× | 26 | +2,814.1 | +2,662.2 | 61.4% | 82/86 |
| 26 | GPT-5.5 (xhigh) | 1.11× | 1.03–1.22× | 28 | +2,709.7 | +2,669.8 | 62.1% | 82/87 |
| 27 | GPT-5.4 (xhigh) | 1.13× | 1.05–1.20× | 25 | +2,843.9 | +2,828.4 | 50.0% | 66/70 |
| 28 | Muse Spark 1.2 (xhigh) | 1.30× | 1.19–1.40× | 24 | +2,891.4 | +3,247.3 | 50.7% | 67/71 |
| 29 | Muse Spark 1.1 (xhigh) | 1.37× | 1.22–1.55× | 25 | +2,845.5 | +3,364.8 | 48.6% | 63/68 |
| — | Gemini 3 Flash Preview · DeepSWE 1.0 | 0.76× | — | 4 | +1,554.6 | +1,204.9 | 3.6% | 5/5 |
| — | Gemini 3.1 Pro Preview (high) | 0.81× | 0.66–0.91× | 8 | +1,447.5 | +1,441.7 | 12.1% | 16/17 |
| — | GLM-5.1 · DeepSWE 1.0 | 0.91× | 0.84–0.98× | 13 | +1,428.1 | +2,224.9 | 22.9% | 30/32 |
| — | Grok Build 0.1 · DeepSWE 1.0 | 0.95× | 0.77–1.15× | 6 | +1,905.2 | +2,018.7 | 11.4% | 14/16 |
| — | Kimi K2.6 · DeepSWE 1.0 | 0.96× | 0.83–1.09× | 12 | +1,474.8 | +1,986.3 | 20.0% | 28/28 |
| — | GPT-5.4 mini (xhigh) · DeepSWE 1.0 | 1.02× | 0.89–1.15× | 9 | +1,934.0 | +2,295.8 | 12.1% | 14/17 |
| — | Qwen3.6 Plus · DeepSWE 1.0 | 1.25× | — | 2 | +2,249.0 | +2,147.9 | 1.4% | 2/2 |
| — | Claude Haiku 4.5 · DeepSWE 1.0 | — | — | — | — | +1,445.1 | 0.0% | 0/0 |
| — | MiniMax M2.7 · DeepSWE 1.0 | — | — | — | — | +1,782.7 | 0.0% | 0/0 |

## Reproduce

Run `npm ci` for the pinned TypeScript parser and use the measurement revision in a clean checkout; **do not relabel results from a different analyzer commit**. From the repository root:

```sh
PY=/path/to/python-3.14.7   # with Node.js on PATH and `npm ci` done in this checkout
$PY -m parsimony.deepswe dataset /path/to/pinned-deep-swe --language typescript --output /tmp/typescript.jsonl
# Dataset hash must match population.json. Analyze each configuration from the refresh evidence:
$PY -m parsimony.deepswe --cache /tmp/deepswe-refresh analyze mini_swe_agent_claude_opus_5_max \
  --dataset /tmp/typescript.jsonl --output /tmp/claude_opus_5_max.jsonl

E=examples/deepswe-typescript
$PY -m parsimony.release audit "$E/population.json" "$E/"*.jsonl \
  --dataset /tmp/typescript.jsonl --output /tmp/typescript-coverage.json
# Freeze into a NEW path after obtaining the complete records, rather than overwriting the panel:
$PY -m parsimony.deepswe panel "$E/"*.jsonl --name deepswe-v1.1-typescript-26-pooled-80-20-v0.7 --output /tmp/typescript-panel.json
$PY -m parsimony.scoring score "$E/score-panel.json" "$E/"*.jsonl --output /tmp/typescript-scores.json
$PY -m parsimony.stability "$E/score-panel.json" "$E/"*.jsonl --output /tmp/typescript-sensitivity.json
$PY -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --benchmark deepswe \
  --sensitivity "$E/sensitivity.json" --output /tmp/typescript.html
```

The UI may be rebuilt with a later site-only revision; measured records, panel references, parser pins and bootstrap inputs stay frozen. DeepSWE is the source of tasks, patches and published outcomes; Parsimony executes none of their code.

## DeepSWE release 1.0 runs (added 2026-10-21)

12 more configurations come from DeepSWE's own archive of **release 1.0** (gated Hugging Face dataset [`datacurve/deep-swe-leaderboard` at `0618ccd`](https://huggingface.co/datasets/datacurve/deep-swe-leaderboard/tree/0618ccdd613e1f0043604f8f4474321e7fe12e29), CC-BY-4.0; access asks you to share your Hugging Face username and email), for models absent from v1.1: Claude Haiku 4.5, Claude Opus 4.6 (max), Claude Opus 4.7 (max), Gemini 3 Flash Preview, GLM-5.1, GPT-5.4 mini (xhigh), Grok Build 0.1, Kimi K2.6, MiMo V2.5 Pro, MiniMax M2.7, MiniMax M3 and Qwen3.6 Plus. Files `v1_0_*.jsonl`; names end in "· DeepSWE 1.0".

- Same 113 task IDs and base commits as v1.1, and the same mini-SWE-agent harness. v1.1 re-ran every model and rewrote every verifier. On the nine setups present in both releases, pass rates agree within a few points, and per-task differences match chance except on four tasks (`narwhals-rolling-window-suite`, `vulture-persistent-analysis-cache`, `skrub-duration-encoding`, `claude-code-by-agents-recursive-delegation`). Release 1.0 outcomes on those four tasks are recorded as unknown, never as pass or fail.
- Measured at this board's analyzer commit with Python 3.14.7, so units are comparable; the frozen panel is unchanged and the new runs are scored against it. Coverage, scores and stability were regenerated with the current scoring code (existing models' archived scores differ only in the last floating-point digit).
- Driver: [`examples/benchmark-discovery/add-deepswe-1.0.py`](../benchmark-discovery/add-deepswe-1.0.py).
- A model is ranked only with at least 15 shared solved tasks (or half the board's tasks if fewer); otherwise it is listed after the ranked models.
