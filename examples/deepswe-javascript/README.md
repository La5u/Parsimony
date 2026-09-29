# DeepSWE v1.1 — JavaScript task track

**Beta research preview, not an official ranking.** 26 configurations (one per model), 5 upstream-JavaScript-labelled tasks × four attempts; 520 records including failed and unavailable attempts. The [website board](../../site/javascript.html) defaults to all-task score, not per-solve size. Language tracks have separate reference panels and syntax-unit definitions: do not pool them or compare raw counts across tracks.

## Pinned inputs and analyzer

- Tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`.
- Release `v1.1`, fresh-cache run index SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Same 26 configurations as the Python board; [refresh evidence](../deepswe-python/refresh-2026-09-28.json). Gemini 3.8 and GPT-6 Astra artifacts are still unavailable; no model outcomes were invented.
- Analyzer **0.6.0-beta**, clean measurement commit `7705e8de13343bbafbfe5bccba665dd2bab8b24a`, Python **3.14.7**. Dataset SHA256 `30091e2eecbe3661144223b5316fa2d9773c19a3f1b00a6641bba0f1c5f2dd47`.
- Unit track `tree-sitter-units-v1`. Exact parsers: tree-sitter 0.26.0, JavaScript 0.25.0, TypeScript 0.23.2, Go 0.25.0. [Rules and limitations](../../docs/language-tracks.md).
- [Population](population.json) contains every attempt; [coverage audit](coverage.json) validates the original dataset, record completeness, base commits and analyzer commit. [Score panel](score-panel.json), [scores](scores.json), [stability](sensitivity.md).

## Coverage before rankings

The frozen population has **20 attempts per model**. The score panel can calibrate **5 of 5 tasks** (20 items): it needs at least one measured, in-scope passing reference per task. Scores, CIs, task selection and the plot's measured-attempt means (including failures) use this score panel; published resolve rate retains the entire population denominator. Attempts from uncalibrated tasks remain in the raw records and coverage report.

Status totals: `error` 1, `ok` 519. A parser/analysis error means **unmeasured**, not benchmark failure or zero footprint. Missing measurements within the panel contribute score bounds. Upstream unknown outcomes remain unknown.

JS-labelled projects are measured with both JS and TS grammars by file extension: the KaTeX task is labelled JavaScript upstream but patches TypeScript files. One KaTeX record hits a TypeScript parse error; that success is left unmeasured rather than assigned a perfect score. Only five task clusters are available, so bootstrap rank ranges are especially weak evidence.

| Model | Published solved | Measured passing | Measured failed | Analysis errors | Missing patches |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 14 / 20 | 14 | 6 | 0 | 0 |
| Claude Opus 4.8 (max) | 8 / 20 | 8 | 12 | 0 | 0 |
| Claude Opus 5 (max) | 13 / 20 | 13 | 7 | 0 | 0 |
| Claude Sonnet 4.6 (high) | 8 / 20 | 8 | 12 | 0 | 0 |
| Claude Sonnet 5 (max) | 11 / 20 | 11 | 9 | 0 | 0 |
| DeepSeek V4 Flash (max) | 7 / 20 | 7 | 13 | 0 | 0 |
| DeepSeek V4 Pro (max) | 13 / 20 | 13 | 7 | 0 | 0 |
| Gemini 3.1 Pro Preview (high) | 2 / 20 | 2 | 18 | 0 | 0 |
| Gemini 3.5 Flash (high) | 10 / 20 | 10 | 10 | 0 | 0 |
| Gemini 3.6 Flash (high) | 11 / 20 | 11 | 9 | 0 | 0 |
| Gemini 3.7 Flash (medium) | 11 / 20 | 11 | 9 | 0 | 0 |
| GLM-5.2 (max) | 6 / 20 | 6 | 14 | 0 | 0 |
| GLM-5.3 Flash (max) | 12 / 20 | 12 | 8 | 0 | 0 |
| GLM-5.3 (max) | 18 / 20 | 18 | 2 | 0 | 0 |
| GPT-5.4 (xhigh) | 7 / 20 | 7 | 13 | 0 | 0 |
| GPT-5.5 (xhigh) | 10 / 20 | 10 | 10 | 0 | 0 |
| GPT-5.6 Luna (max) | 12 / 20 | 12 | 8 | 0 | 0 |
| GPT-5.6 Sol (max) | 15 / 20 | 15 | 5 | 0 | 0 |
| GPT-5.6 Terra (max) | 14 / 20 | 14 | 6 | 0 | 0 |
| Grok 4.5 (high) | 8 / 20 | 8 | 12 | 0 | 0 |
| Grok 4.6 (medium) | 16 / 20 | 16 | 4 | 0 | 0 |
| Kimi K2.7 Code | 5 / 20 | 5 | 15 | 0 | 0 |
| Kimi K3 (max) | 13 / 20 | 13 | 7 | 0 | 0 |
| Muse Spark 1.1 (xhigh) | 9 / 20 | 8 | 11 | 1 | 0 |
| Muse Spark 1.2 (xhigh) | 11 / 20 | 11 | 9 | 0 | 0 |
| Qwen3.8 Max (xhigh) | 13 / 20 | 13 | 7 | 0 | 0 |

“Measured” in the coverage table means full-file analysis completed; the audit separately reports excluded-only successes and unmeasured-unit records. This does not certify upstream test results or patch correctness. Approximate unit alignment is flagged per record.

## Reproduce

Install the pinned language extra and use the measurement revision in a clean checkout; **do not relabel results from a different analyzer commit**. From the repository root:

```sh
PY=/path/to/python-3.14.7-with-language-extra
$PY -m parsimony.deepswe dataset /path/to/pinned-deep-swe --language javascript --output /tmp/javascript.jsonl
# Dataset hash must match population.json. Analyze each configuration from the refresh evidence:
$PY -m parsimony.deepswe --cache /tmp/deepswe-refresh analyze mini_swe_agent_claude_opus_5_max \
  --dataset /tmp/javascript.jsonl --output /tmp/claude_opus_5_max.jsonl

E=examples/deepswe-javascript
$PY -m parsimony.release audit "$E/population.json" "$E/"*.jsonl \
  --dataset /tmp/javascript.jsonl --output /tmp/javascript-coverage.json
# Freeze into a NEW path after obtaining the complete records, rather than overwriting the panel:
$PY -m parsimony.deepswe panel "$E/"*.jsonl --name deepswe-v1.1-javascript-26-pooled-80-20-v0.6 --output /tmp/javascript-panel.json
$PY -m parsimony.scoring score "$E/score-panel.json" "$E/"*.jsonl --output /tmp/javascript-scores.json
$PY -m parsimony.stability "$E/score-panel.json" "$E/"*.jsonl --output /tmp/javascript-sensitivity.json
$PY -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --benchmark deepswe \
  --sensitivity "$E/sensitivity.json" --output /tmp/javascript.html
```

The UI may be rebuilt with a later site-only revision; measured records, panel references, parser pins and bootstrap inputs stay frozen. DeepSWE is the source of tasks, patches and published outcomes; Parsimony executes none of their code.
