# DeepSWE v1.1 — JavaScript task track

**Beta research preview, not an official ranking.** 26 configurations (one per model), 5 upstream-JavaScript-labelled tasks × four attempts; 520 records including failed and unavailable attempts. The [website board](../../site/javascript.html) ranks by net units added over all measured attempts. Language tracks have separate reference panels and syntax-unit definitions: do not pool them or compare raw counts across tracks.

## Pinned inputs and analyzer

- Tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`.
- Release `v1.1`, fresh-cache run index SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Same 26 configurations as the Python board; [refresh evidence](../deepswe-python/refresh-2026-09-28.json). Gemini 3.8 and GPT-6 Astra artifacts are still unavailable; no model outcomes were invented.
- Analyzer **0.7.0-beta**, clean measurement commit `ca37c314d84d1d5949e2080077c6afc30b916394`, Python **3.14.7**. Dataset SHA256 `30091e2eecbe3661144223b5316fa2d9773c19a3f1b00a6641bba0f1c5f2dd47`.
- Unit track `typescript-compiler-units-v1`: the official TypeScript parser, `typescript@5.9.3`, syntax only. The 0.6.0-beta Tree-sitter records (`tree-sitter-units-v1`) were replaced, not mixed; they were last present at commit `ca37c31` and their raw counts are not comparable. [Why the parser changed](../../docs/archive/typescript-parser-investigation.md). [Rules and limitations](../../docs/language-tracks.md).
- [Population](population.json) contains every attempt; [coverage audit](coverage.json) validates the original dataset, record completeness, base commits and analyzer commit. [Score panel](score-panel.json), [scores](scores.json), [stability](sensitivity.md).

## Coverage before rankings

The frozen population has **20 attempts per model**. The score panel can calibrate **5 of 5 tasks** (20 items): it needs at least one measured, in-scope passing reference per task. Scores, CIs, task selection and the plot's measured-attempt means (including failures) use this score panel; published resolve rate retains the entire population denominator. Attempts from uncalibrated tasks remain in the raw records and coverage report.

Status totals: `ok` 520 (0.6.0-beta: one TypeScript grammar error). A parser/analysis error means **unmeasured**, not benchmark failure or zero footprint. Missing measurements within the panel contribute score bounds. Upstream unknown outcomes remain unknown.

JS-labelled projects measure both JavaScript and TypeScript files, with the script kind chosen by file extension: the KaTeX task is labelled JavaScript upstream but patches TypeScript files. Only five task clusters are available, so bootstrap rank ranges are especially weak evidence.

| Model | Published solved | Measured passing | Measured failed | Analysis errors | Missing patches |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 14 / 20 | 14 | 6 | 0 | 0 |
| Claude Opus 4.8 (max) | 8 / 20 | 8 | 12 | 0 | 0 |
| Claude Opus 5 (max) | 13 / 20 | 13 | 7 | 0 | 0 |
| Claude Sonnet 4.6 (high) | 8 / 20 | 8 | 12 | 0 | 0 |
| Claude Sonnet 5 (max) | 11 / 20 | 11 | 9 | 0 | 0 |
| DeepSeek V4 Flash (max) | 7 / 20 | 7 | 13 | 0 | 0 |
| DeepSeek V4 Pro (max) | 13 / 20 | 13 | 7 | 0 | 0 |
| GLM-5.2 (max) | 6 / 20 | 6 | 14 | 0 | 0 |
| GLM-5.3 (max) | 18 / 20 | 18 | 2 | 0 | 0 |
| GLM-5.3 Flash (max) | 12 / 20 | 12 | 8 | 0 | 0 |
| GPT-5.4 (xhigh) | 7 / 20 | 7 | 13 | 0 | 0 |
| GPT-5.5 (xhigh) | 10 / 20 | 10 | 10 | 0 | 0 |
| GPT-5.6 Luna (max) | 12 / 20 | 12 | 8 | 0 | 0 |
| GPT-5.6 Sol (max) | 15 / 20 | 15 | 5 | 0 | 0 |
| GPT-5.6 Terra (max) | 14 / 20 | 14 | 6 | 0 | 0 |
| Gemini 3.1 Pro Preview (high) | 2 / 20 | 2 | 18 | 0 | 0 |
| Gemini 3.5 Flash (high) | 10 / 20 | 10 | 10 | 0 | 0 |
| Gemini 3.6 Flash (high) | 11 / 20 | 11 | 9 | 0 | 0 |
| Gemini 3.7 Flash (medium) | 11 / 20 | 11 | 9 | 0 | 0 |
| Grok 4.5 (high) | 8 / 20 | 8 | 12 | 0 | 0 |
| Grok 4.6 (medium) | 16 / 20 | 16 | 4 | 0 | 0 |
| Kimi K2.7 Code | 5 / 20 | 5 | 15 | 0 | 0 |
| Kimi K3 (max) | 13 / 20 | 13 | 7 | 0 | 0 |
| Muse Spark 1.1 (xhigh) | 9 / 20 | 9 | 11 | 0 | 0 |
| Muse Spark 1.2 (xhigh) | 11 / 20 | 11 | 9 | 0 | 0 |
| Qwen3.8 Max (xhigh) | 13 / 20 | 13 | 7 | 0 | 0 |

“Measured” in the coverage table means full-file analysis completed; the audit separately reports excluded-only successes and unmeasured-unit records. This does not certify upstream test results or patch correctness. Approximate unit alignment is flagged per record.

## Ranking (same tasks)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Gemini 3.1 Pro Preview (high) | 0.55× | — | 2 | +1,138.0 | +1,446.5 | 10.0% | 2/2 |
| 2 | Gemini 3.5 Flash (high) | 0.79× | — | 4 | +1,926.4 | +2,123.5 | 50.0% | 10/10 |
| 3 | Claude Fable 5 (xhigh) | 0.80× | — | 4 | +1,636.5 | +2,466.8 | 70.0% | 14/14 |
| 4 | Claude Opus 4.8 (max) | 0.83× | — | 3 | +1,672.4 | +2,328.1 | 40.0% | 8/8 |
| 5 | Kimi K2.7 Code | 0.84× | — | 2 | +1,809.2 | +2,412.9 | 25.0% | 5/5 |
| 6 | Gemini 3.6 Flash (high) | 0.86× | — | 4 | +1,853.6 | +2,542.2 | 55.0% | 11/11 |
| 7 | GPT-5.5 (xhigh) | 0.89× | — | 4 | +2,422.1 | +2,491.6 | 50.0% | 10/10 |
| 8 | Kimi K3 (max) | 0.91× | 0.72–1.02× | 5 | +2,379.6 | +2,554.4 | 65.0% | 13/13 |
| 9 | Qwen3.8 Max (xhigh) | 0.93× | — | 4 | +2,078.5 | +2,714.7 | 65.0% | 13/13 |
| 10 | GPT-5.6 Terra (max) | 0.93× | — | 4 | +2,827.9 | +2,682.9 | 70.0% | 14/14 |
| 11 | GLM-5.2 (max) | 0.93× | — | 2 | +1,911.7 | +2,611.4 | 30.0% | 6/6 |
| 12 | Claude Sonnet 5 (max) | 0.94× | 0.68–1.14× | 5 | +3,019.6 | +2,464.9 | 55.0% | 11/11 |
| 13 | GLM-5.3 (max) | 0.96× | 0.84–1.05× | 5 | +2,533.8 | +2,714.2 | 90.0% | 18/18 |
| 14 | DeepSeek V4 Flash (max) | 0.97× | — | 3 | +1,949.1 | +2,591.7 | 35.0% | 7/7 |
| 15 | Gemini 3.7 Flash (medium) | 1.02× | 0.82–1.13× | 5 | +2,366.2 | +2,794.3 | 55.0% | 11/11 |
| 16 | GPT-5.6 Luna (max) | 1.02× | 0.86–1.27× | 5 | +2,958.2 | +2,879.0 | 60.0% | 12/12 |
| 17 | GPT-5.6 Sol (max) | 1.03× | — | 4 | +2,994.1 | +2,892.0 | 75.0% | 15/15 |
| 18 | GPT-5.4 (xhigh) | 1.03× | — | 4 | +2,422.7 | +2,913.6 | 35.0% | 7/7 |
| 19 | Grok 4.5 (high) | 1.05× | — | 3 | +2,373.6 | +2,757.8 | 40.0% | 8/8 |
| 20 | GLM-5.3 Flash (max) | 1.06× | — | 4 | +2,287.3 | +2,844.7 | 60.0% | 12/12 |
| 21 | DeepSeek V4 Pro (max) | 1.07× | — | 4 | +2,691.8 | +2,815.8 | 65.0% | 13/13 |
| 22 | Claude Sonnet 4.6 (high) | 1.07× | — | 3 | +2,313.0 | +2,653.1 | 40.0% | 8/8 |
| 23 | Grok 4.6 (medium) | 1.12× | 0.75–1.40× | 5 | +2,855.3 | +3,183.8 | 80.0% | 16/16 |
| 24 | Claude Opus 5 (max) | 1.18× | — | 4 | +2,466.3 | +3,000.8 | 65.0% | 13/13 |
| 25 | Muse Spark 1.2 (xhigh) | 1.30× | 0.97–1.96× | 5 | +3,002.4 | +3,162.4 | 55.0% | 11/11 |
| 26 | Muse Spark 1.1 (xhigh) | 1.30× | 1.01–1.87× | 5 | +3,422.3 | +3,238.2 | 45.0% | 9/9 |

## Reproduce

Run `npm ci` for the pinned TypeScript parser and use the measurement revision in a clean checkout; **do not relabel results from a different analyzer commit**. From the repository root:

```sh
PY=/path/to/python-3.14.7   # with Node.js on PATH and `npm ci` done in this checkout
$PY -m parsimony.deepswe dataset /path/to/pinned-deep-swe --language javascript --output /tmp/javascript.jsonl
# Dataset hash must match population.json. Analyze each configuration from the refresh evidence:
$PY -m parsimony.deepswe --cache /tmp/deepswe-refresh analyze mini_swe_agent_claude_opus_5_max \
  --dataset /tmp/javascript.jsonl --output /tmp/claude_opus_5_max.jsonl

E=examples/deepswe-javascript
$PY -m parsimony.release audit "$E/population.json" "$E/"*.jsonl \
  --dataset /tmp/javascript.jsonl --output /tmp/javascript-coverage.json
# Freeze into a NEW path after obtaining the complete records, rather than overwriting the panel:
$PY -m parsimony.deepswe panel "$E/"*.jsonl --name deepswe-v1.1-javascript-26-pooled-80-20-v0.7 --output /tmp/javascript-panel.json
$PY -m parsimony.scoring score "$E/score-panel.json" "$E/"*.jsonl --output /tmp/javascript-scores.json
$PY -m parsimony.stability "$E/score-panel.json" "$E/"*.jsonl --output /tmp/javascript-sensitivity.json
$PY -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --benchmark deepswe \
  --sensitivity "$E/sensitivity.json" --output /tmp/javascript.html
```

The UI may be rebuilt with a later site-only revision; measured records, panel references, parser pins and bootstrap inputs stay frozen. DeepSWE is the source of tasks, patches and published outcomes; Parsimony executes none of their code.
