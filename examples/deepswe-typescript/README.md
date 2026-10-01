# DeepSWE v1.1 — TypeScript task track

**Beta research preview, not an official ranking.** 26 configurations (one per model), 35 upstream-TypeScript-labelled tasks × four attempts; 3,640 records including failed and unavailable attempts. The [website board](../../site/typescript.html) ranks by net units added over all measured attempts. Language tracks have separate reference panels and syntax-unit definitions: do not pool them or compare raw counts across tracks.

## Pinned inputs and analyzer

- Tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`.
- Release `v1.1`, fresh-cache run index SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Same 26 configurations as the Python board; [refresh evidence](../deepswe-python/refresh-2026-09-28.json). Gemini 3.8 and GPT-6 Astra artifacts are still unavailable; no model outcomes were invented.
- Analyzer **0.7.0-beta**, clean measurement commit `ca37c314d84d1d5949e2080077c6afc30b916394`, Python **3.14.7**. Dataset SHA256 `c03deb677cef4101524071ec7c83ba044b153f8dce96590c75bb3c9c179f54c7`.
- Unit track `typescript-compiler-units-v1`: the official TypeScript parser, `typescript@5.9.3`, syntax only. The 0.6.0-beta Tree-sitter records (`tree-sitter-units-v1`) were replaced, not mixed; they were last present at commit `ca37c31` and their raw counts are not comparable. [Why the parser changed](../../docs/typescript-parser-investigation.md). [Rules and limitations](../../docs/language-tracks.md).
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
