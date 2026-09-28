# DeepSWE v1.1 — TypeScript task track

**Beta research preview, not an official ranking.** 26 configurations (one per model), 35 upstream-TypeScript-labelled tasks × four attempts; 3,640 records including failed and unavailable attempts. The [website board](../../site/typescript.html) defaults to all-task score, not per-solve size. Language tracks have separate reference panels and syntax-unit definitions: do not pool them or compare raw counts across tracks.

## Pinned inputs and analyzer

- Tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`.
- Release `v1.1`, fresh-cache run index SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Same 26 configurations as the Python board; [refresh evidence](../deepswe-python/refresh-2026-09-28.json). Gemini 3.8 and GPT-6 Astra artifacts are still unavailable; no model outcomes were invented.
- Analyzer **0.6.0-beta**, clean measurement commit `7705e8de13343bbafbfe5bccba665dd2bab8b24a`, Python **3.14.7**. Dataset SHA256 `c03deb677cef4101524071ec7c83ba044b153f8dce96590c75bb3c9c179f54c7`.
- Unit track `tree-sitter-units-v1`. Exact parsers: tree-sitter 0.26.0, JavaScript 0.25.0, TypeScript 0.23.2, Go 0.25.0. [Rules and limitations](../../docs/language-tracks.md).
- [Population](population.json) contains every attempt; [coverage audit](coverage.json) validates the original dataset, record completeness, base commits and analyzer commit. [Score panel](score-panel.json), [scores](scores.json), [stability](sensitivity.md).

## Coverage before rankings

The frozen population has **140 attempts per model**. The score panel can calibrate **31 of 35 tasks** (124 items): it needs at least one measured, in-scope passing reference per task. Scores, CIs, task selection and the plot's measured-success means use this score panel; published resolve rate retains the entire population denominator. Attempts from uncalibrated tasks remain in the raw records and coverage report.

Status totals: `error` 323, `not_resolved` 24, `ok` 3,293. A parser/analysis error means **unmeasured**, not benchmark failure or zero footprint. Missing measurements within the panel contribute score bounds. Upstream unknown outcomes remain unknown.

Tasks without a usable passing reference: `effect-sse-httpapi-streaming`, `httpx-deterministic-cookie-store`, `kea-atomic-signal-selectors`, `prometheus-transactional-reload-status`.

**Known coverage limitations:** some valid TypeScript constructs fail the pinned grammar, including `export type * as` in a Vitest base file and existing Effect overload syntax. Errors on a base file are not evidence that a model broke syntax. Other after-only errors have not been independently classified as invalid code versus grammar gaps. The upstream task metadata also labels `httpx-deterministic-cookie-store` (Python patches) and `prometheus-transactional-reload-status` (Go patches) TypeScript: their changes are outside this track, and those tasks are not silently moved into another frozen population. Both are retained as excluded-only records. Interpret this track's intervals and coverage before any rank claim.

| Model | Published solved | Measured passing | Measured failed | Analysis errors | Missing patches |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 89 / 140 | 82 | 46 | 12 | 0 |
| Claude Opus 4.8 (max) | 64 / 140 | 63 | 60 | 8 | 0 |
| Claude Opus 5 (max) | 88 / 140 | 79 | 46 | 12 | 0 |
| Claude Sonnet 4.6 (high) | 44 / 140 | 43 | 84 | 12 | 0 |
| Claude Sonnet 5 (max) | 69 / 140 | 67 | 64 | 7 | 0 |
| DeepSeek V4 Flash (max) | 73 / 140 | 67 | 59 | 14 | 0 |
| DeepSeek V4 Pro (max) | 86 / 140 | 78 | 46 | 16 | 0 |
| Gemini 3.1 Pro Preview (high) | 17 / 140 | 17 | 107 | 16 | 0 |
| Gemini 3.5 Flash (high) | 51 / 140 | 49 | 81 | 10 | 0 |
| Gemini 3.6 Flash (high) | 57 / 140 | 54 | 76 | 10 | 0 |
| Gemini 3.7 Flash (medium) | 86 / 140 | 79 | 50 | 11 | 0 |
| GLM-5.2 (max) | 61 / 140 | 58 | 78 | 4 | 0 |
| GLM-5.3 Flash (max) | 72 / 140 | 64 | 62 | 13 | 0 |
| GLM-5.3 (max) | 85 / 140 | 80 | 49 | 11 | 0 |
| GPT-5.4 (xhigh) | 70 / 140 | 62 | 66 | 12 | 0 |
| GPT-5.5 (xhigh) | 87 / 140 | 74 | 49 | 17 | 0 |
| GPT-5.6 Luna (max) | 81 / 140 | 76 | 45 | 15 | 0 |
| GPT-5.6 Sol (max) | 92 / 140 | 79 | 45 | 16 | 0 |
| GPT-5.6 Terra (max) | 91 / 140 | 85 | 41 | 13 | 0 |
| Grok 4.5 (high) | 68 / 140 | 66 | 63 | 11 | 0 |
| Grok 4.6 (medium) | 81 / 140 | 74 | 50 | 16 | 0 |
| Kimi K2.7 Code | 39 / 140 | 38 | 91 | 11 | 0 |
| Kimi K3 (max) | 84 / 140 | 79 | 51 | 10 | 0 |
| Muse Spark 1.1 (xhigh) | 68 / 140 | 66 | 60 | 14 | 0 |
| Muse Spark 1.2 (xhigh) | 71 / 140 | 68 | 52 | 20 | 0 |
| Qwen3.8 Max (xhigh) | 75 / 140 | 70 | 55 | 12 | 0 |

“Measured” in the coverage table means full-file analysis completed; the audit separately reports excluded-only successes and unmeasured-unit records. This does not certify upstream test results or patch correctness. Approximate unit alignment is flagged per record.

## Reproduce

Install the pinned language extra and use the measurement revision in a clean checkout; **do not relabel results from a different analyzer commit**. From the repository root:

```sh
PY=/path/to/python-3.14.7-with-language-extra
$PY -m parsimony.deepswe dataset /path/to/pinned-deep-swe --language typescript --output /tmp/typescript.jsonl
# Dataset hash must match population.json. Analyze each configuration from the refresh evidence:
$PY -m parsimony.deepswe --cache /tmp/deepswe-refresh analyze mini_swe_agent_claude_opus_5_max \
  --dataset /tmp/typescript.jsonl --output /tmp/claude_opus_5_max.jsonl

E=examples/deepswe-typescript
$PY -m parsimony.release audit "$E/population.json" "$E/"*.jsonl \
  --dataset /tmp/typescript.jsonl --output /tmp/typescript-coverage.json
# Freeze into a NEW path after obtaining the complete records, rather than overwriting the panel:
$PY -m parsimony.deepswe panel "$E/"*.jsonl --name deepswe-v1.1-typescript-26-pooled-80-20-v0.6 --output /tmp/typescript-panel.json
$PY -m parsimony.scoring score "$E/score-panel.json" "$E/"*.jsonl --output /tmp/typescript-scores.json
$PY -m parsimony.stability "$E/score-panel.json" "$E/"*.jsonl --output /tmp/typescript-sensitivity.json
$PY -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --benchmark deepswe \
  --sensitivity "$E/sensitivity.json" --output /tmp/typescript.html
```

The UI may be rebuilt with a later site-only revision; measured records, panel references, parser pins and bootstrap inputs stay frozen. DeepSWE is the source of tasks, patches and published outcomes; Parsimony executes none of their code.
