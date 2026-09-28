# DeepSWE v1.1 — Go task track

**Beta research preview, not an official ranking.** 26 configurations (one per model), 34 upstream-Go-labelled tasks × four attempts; 3,536 records including failed and unavailable attempts. The [website board](../../site/go.html) defaults to all-task score, not per-solve size. Language tracks have separate reference panels and syntax-unit definitions: do not pool them or compare raw counts across tracks.

## Pinned inputs and analyzer

- Tasks: `datacurve-ai/deep-swe` at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`.
- Release `v1.1`, fresh-cache run index SHA256 `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`. Same 26 configurations as the Python board; [refresh evidence](../deepswe-python/refresh-2026-09-28.json). Gemini 3.8 and GPT-6 Astra artifacts are still unavailable; no model outcomes were invented.
- Analyzer **0.6.0-beta**, clean measurement commit `7705e8de13343bbafbfe5bccba665dd2bab8b24a`, Python **3.14.7**. Dataset SHA256 `ea57379e61ffbe05423d03c829f13b4ae89ebe28c1b0da85c2a48fd29f52413d`.
- Unit track `tree-sitter-units-v1`. Exact parsers: tree-sitter 0.26.0, JavaScript 0.25.0, TypeScript 0.23.2, Go 0.25.0. [Rules and limitations](../../docs/language-tracks.md).
- [Population](population.json) contains every attempt; [coverage audit](coverage.json) validates the original dataset, record completeness, base commits and analyzer commit. [Score panel](score-panel.json), [scores](scores.json), [stability](sensitivity.md).

## Coverage before rankings

The frozen population has **136 attempts per model**. The score panel can calibrate **34 of 34 tasks** (136 items): it needs at least one measured, in-scope passing reference per task. Scores, CIs, task selection and the plot's measured-success means use this score panel; published resolve rate retains the entire population denominator. Attempts from uncalibrated tasks remain in the raw records and coverage report.

Status totals: `error` 7, `missing_patch` 2, `not_resolved` 25, `ok` 3,502. A parser/analysis error means **unmeasured**, not benchmark failure or zero footprint. Missing measurements within the panel contribute score bounds. Upstream unknown outcomes remain unknown.

| Model | Published solved | Measured passing | Measured failed | Analysis errors | Missing patches |
|---|---:|---:|---:|---:|---:|
| Claude Fable 5 (xhigh) | 97 / 136 | 97 | 39 | 0 | 0 |
| Claude Opus 4.8 (max) | 84 / 136 | 83 | 39 | 1 | 0 |
| Claude Opus 5 (max) | 108 / 136 | 108 | 25 | 0 | 0 |
| Claude Sonnet 4.6 (high) | 36 / 136 | 36 | 99 | 1 | 0 |
| Claude Sonnet 5 (max) | 67 / 136 | 66 | 61 | 1 | 0 |
| DeepSeek V4 Flash (max) | 84 / 136 | 84 | 52 | 0 | 0 |
| DeepSeek V4 Pro (max) | 91 / 136 | 91 | 45 | 0 | 0 |
| Gemini 3.1 Pro Preview (high) | 20 / 136 | 20 | 114 | 0 | 2 |
| Gemini 3.5 Flash (high) | 54 / 136 | 54 | 82 | 0 | 0 |
| Gemini 3.6 Flash (high) | 80 / 136 | 80 | 56 | 0 | 0 |
| Gemini 3.7 Flash (medium) | 102 / 136 | 102 | 34 | 0 | 0 |
| GLM-5.2 (max) | 67 / 136 | 67 | 69 | 0 | 0 |
| GLM-5.3 Flash (max) | 94 / 136 | 94 | 41 | 0 | 0 |
| GLM-5.3 (max) | 104 / 136 | 102 | 32 | 2 | 0 |
| GPT-5.4 (xhigh) | 86 / 136 | 86 | 50 | 0 | 0 |
| GPT-5.5 (xhigh) | 102 / 136 | 102 | 34 | 0 | 0 |
| GPT-5.6 Luna (max) | 107 / 136 | 107 | 29 | 0 | 0 |
| GPT-5.6 Sol (max) | 107 / 136 | 107 | 29 | 0 | 0 |
| GPT-5.6 Terra (max) | 105 / 136 | 105 | 31 | 0 | 0 |
| Grok 4.5 (high) | 77 / 136 | 77 | 59 | 0 | 0 |
| Grok 4.6 (medium) | 100 / 136 | 100 | 36 | 0 | 0 |
| Kimi K2.7 Code | 58 / 136 | 58 | 78 | 0 | 0 |
| Kimi K3 (max) | 107 / 136 | 106 | 29 | 1 | 0 |
| Muse Spark 1.1 (xhigh) | 81 / 136 | 81 | 54 | 1 | 0 |
| Muse Spark 1.2 (xhigh) | 85 / 136 | 85 | 51 | 0 | 0 |
| Qwen3.8 Max (xhigh) | 84 / 136 | 84 | 52 | 0 | 0 |

“Measured” in the coverage table means full-file analysis completed; the audit separately reports excluded-only successes and unmeasured-unit records. This does not certify upstream test results or patch correctness. Approximate unit alignment is flagged per record.

## Reproduce

Install the pinned language extra and use the measurement revision in a clean checkout; **do not relabel results from a different analyzer commit**. From the repository root:

```sh
PY=/path/to/python-3.14.7-with-language-extra
$PY -m parsimony.deepswe dataset /path/to/pinned-deep-swe --language go --output /tmp/go.jsonl
# Dataset hash must match population.json. Analyze each configuration from the refresh evidence:
$PY -m parsimony.deepswe --cache /tmp/deepswe-refresh analyze mini_swe_agent_claude_opus_5_max \
  --dataset /tmp/go.jsonl --output /tmp/claude_opus_5_max.jsonl

E=examples/deepswe-go
$PY -m parsimony.release audit "$E/population.json" "$E/"*.jsonl \
  --dataset /tmp/go.jsonl --output /tmp/go-coverage.json
# Freeze into a NEW path after obtaining the complete records, rather than overwriting the panel:
$PY -m parsimony.deepswe panel "$E/"*.jsonl --name deepswe-v1.1-go-26-pooled-80-20-v0.6 --output /tmp/go-panel.json
$PY -m parsimony.scoring score "$E/score-panel.json" "$E/"*.jsonl --output /tmp/go-scores.json
$PY -m parsimony.stability "$E/score-panel.json" "$E/"*.jsonl --output /tmp/go-sensitivity.json
$PY -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --benchmark deepswe \
  --sensitivity "$E/sensitivity.json" --output /tmp/go.html
```

The UI may be rebuilt with a later site-only revision; measured records, panel references, parser pins and bootstrap inputs stay frozen. DeepSWE is the source of tasks, patches and published outcomes; Parsimony executes none of their code.
