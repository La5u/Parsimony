# DeepSWE Go v2 — corrected parser, full-cohort remeasurement

**Beta research preview, not an official coding-quality ranking.** This replaces the current Go website data with a separately versioned full-cohort release. The [historical v1 records](../deepswe-go/README.md) remain unchanged; they must not be relabelled or mixed with v2.

## Inputs and analyzer

- **26 unchanged model + effort configurations**, 34 frozen tasks × four attempts = **136 slots per configuration / 3,536 records**.
- Upstream task commit: `datacurve-ai/deep-swe@0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`.
- Dataset SHA256: `ea57379e61ffbe05423d03c829f13b4ae89ebe28c1b0da85c2a48fd29f52413d` — byte-identical to v1.
- Exact pinned v1.1 trial export SHA256: `310cb428fe8914cff21b8edcb0b17256884efca55666bd6d6646d223c77d2ce6`.
- Clean analyzer: **0.8.0-beta**, commit `34d59ca8d5f06ffd7ec310dff74a9b8e7ea40cdc`, source SHA256 `14101e9b3d0fbb419be6744951bc58b2a5ca92ddf48750cc16ab38edbd0ccf9b`, Python **3.14.7**.
- Go track: **`tree-sitter-go-units-v2`**, Tree-sitter 0.26.0, checksum-pinned unmerged upstream PR #190 grammar, explicit EOF LF policy. Package version 0.25.0 alone does not identify this grammar. See [parser release details](../../docs/go-parser-v2-release.md) and [language rules](../../docs/language-tracks.md).

No target code was executed, built, installed or tested. The grammar build compiles parser tooling only. Published outcomes are upstream claims; static parser/patch verification is not correctness, model-backend or evaluator certification.

## Coverage and compatibility

| State | v1 | v2 |
| --- | ---: | ---: |
| Measured, in-scope | 3,502 | **3,508** |
| Analysis errors | 7 | **1** |
| Missing patches | 2 | 2 |
| Unanalyzed no-logs/unknown outcomes | 25 | 25 |
| Total retained slots | 3,536 | 3,536 |

**All 3,502 previously measured attempts retain identical primary unit/token footprint metrics.** Their human-reference net/churn values also agree. Three identifier-insensitive `structural_churn` diagnostics change by +2 due to grammar labels; these do not set footprint rank or archived scores. All 3,536 task, outcome, resolve-total, patch and base bindings are unchanged. The archived panel calibrates all 34 tasks / 136 slots.

Six attempts become measurable: five source-reported successful Arcane attempts using Go 1.26 `new(expression)`, and one source-reported failed Scriggo attempt ending with a grouped declaration without a newline. The malformed Helm after-file remains an error, not a zero. See [validation summary](validation-summary.json), [coverage](coverage.json), [per-configuration comparison](comparison-summary.json) and the [original static investigation](../../docs/go-parser-investigation.md).

Default rank remains the plain mean net coding units over measured in-scope passing and failed attempts. The optional **Solved only** view restricts footprint/rank to measured successes. Means and coverage for five configurations change because valid formerly missing attempts are now included. Missing outcomes/measurements are not inferred, zero-filled or converted to failures. This is neither shared-solved-task matching nor a maintainability score.

## Ranking (same tasks)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Gemini 3.1 Pro Preview (high) | 0.70× | 0.62–0.76× | 11 | +2,825.8 | +2,170.2 | 14.7% | 20/20 |
| 2 | Claude Fable 5 (xhigh) | 0.82× | 0.78–0.86× | 31 | +2,937.0 | +2,836.3 | 71.3% | 97/97 |
| 3 | Claude Opus 4.8 (max) | 0.86× | 0.81–0.90× | 29 | +2,970.7 | +2,725.9 | 61.8% | 84/84 |
| 4 | Claude Sonnet 5 (max) | 0.86× | 0.82–0.90× | 27 | +2,853.0 | +2,584.9 | 49.3% | 67/67 |
| 5 | Kimi K2.7 Code | 0.87× | 0.83–0.92× | 24 | +2,998.9 | +2,954.4 | 42.6% | 58/58 |
| 6 | Gemini 3.5 Flash (high) | 0.88× | 0.83–0.91× | 24 | +2,759.7 | +2,892.5 | 39.7% | 54/54 |
| 7 | Claude Sonnet 4.6 (high) | 0.88× | 0.80–0.97× | 21 | +2,847.3 | +2,988.4 | 26.5% | 36/36 |
| 8 | GLM-5.2 (max) | 0.89× | 0.82–0.94× | 28 | +3,112.3 | +2,725.3 | 49.3% | 67/67 |
| 9 | Kimi K3 (max) | 0.89× | 0.85–0.93× | 32 | +3,085.7 | +3,048.1 | 78.7% | 107/107 |
| 10 | Gemini 3.6 Flash (high) | 0.91× | 0.87–0.96× | 30 | +2,921.8 | +2,985.1 | 58.8% | 80/80 |
| 11 | Qwen3.8 Max (xhigh) | 0.92× | 0.87–0.97× | 28 | +3,340.1 | +3,148.0 | 61.8% | 84/84 |
| 12 | DeepSeek V4 Flash (max) | 0.97× | 0.93–1.02× | 29 | +3,334.1 | +3,250.2 | 61.8% | 84/84 |
| 13 | GLM-5.3 (max) | 1.00× | 0.96–1.04× | 32 | +3,476.7 | +3,293.7 | 76.5% | 104/104 |
| 14 | GLM-5.3 Flash (max) | 1.00× | 0.95–1.06× | 31 | +3,543.3 | +3,415.0 | 69.1% | 94/94 |
| 15 | Gemini 3.7 Flash (medium) | 1.01× | 0.97–1.06× | 29 | +3,554.7 | +3,545.2 | 75.0% | 102/102 |
| 16 | Grok 4.5 (high) | 1.02× | 0.95–1.08× | 25 | +3,695.3 | +3,459.7 | 56.6% | 77/77 |
| 17 | Grok 4.6 (medium) | 1.03× | 0.98–1.08× | 30 | +3,730.0 | +3,462.1 | 73.5% | 100/100 |
| 18 | Claude Opus 5 (max) | 1.04× | 0.99–1.10× | 32 | +3,682.5 | +3,538.1 | 79.4% | 108/108 |
| 19 | DeepSeek V4 Pro (max) | 1.08× | 1.03–1.13× | 32 | +3,747.9 | +3,738.6 | 66.9% | 91/91 |
| 20 | GPT-5.5 (xhigh) | 1.09× | 1.04–1.15× | 32 | +3,682.0 | +3,661.2 | 75.0% | 102/102 |
| 21 | GPT-5.6 Sol (max) | 1.11× | 1.02–1.22× | 30 | +3,927.7 | +3,749.9 | 78.7% | 107/107 |
| 22 | GPT-5.6 Terra (max) | 1.11× | 1.05–1.16× | 32 | +3,730.9 | +3,720.5 | 77.2% | 105/105 |
| 23 | GPT-5.6 Luna (max) | 1.13× | 1.08–1.19× | 33 | +3,663.0 | +3,847.4 | 78.7% | 107/107 |
| 24 | GPT-5.4 (xhigh) | 1.14× | 1.08–1.21× | 28 | +3,710.8 | +3,815.4 | 63.2% | 86/86 |
| 25 | Muse Spark 1.2 (xhigh) | 1.24× | 1.15–1.35× | 29 | +4,273.1 | +4,051.5 | 62.5% | 85/85 |
| 26 | Muse Spark 1.1 (xhigh) | 1.28× | 1.18–1.38× | 28 | +4,397.3 | +4,285.1 | 59.6% | 81/81 |

## Scalar release assets, not raw artifacts

Large record JSONLs, pooled reference panel, full comparison, diagnostic JSON and preparation/release hash metadata are stored in the checksummed [Go v0.8 release asset](https://github.com/La5u/Parsimony/releases/tag/deepswe-go-v0.8), not duplicated in Git. This directory keeps small manifests/reports only:

- [Population](population.json), [coverage](coverage.json), [validation](validation-summary.json).
- Archived [scores](scores.json), [sensitivity report](sensitivity.md).
- [Asset URL, byte length and SHA256 bindings](release-assets.json).

The asset contains **scalar/metadata files only**: no task source, patches, dataset rows containing reference patches, prompts or trajectories. Raw inputs stay external. Numerical publication does not grant raw-artifact redistribution rights. Existing public task/model/harness attribution is retained in the scalar records.

Download and verify every member before writing it, without overwriting conflicting files:

```sh
python examples/benchmark-discovery/fetch-go-v2-release.py --output /tmp/parsimony-go-v2-scalars
```

## Rebuild and reproduce

After downloading the asset, rebuild the page offline with a current site generator. The default AA snapshot is external context and does not affect rank:

```sh
E=/tmp/parsimony-go-v2-scalars
python -m parsimony.scoring score "$E/score-panel.json" "$E/"*.jsonl --output /tmp/go-v2-scores.json
cmp "$E/scores.json" /tmp/go-v2-scores.json
python -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl \
  --sensitivity "$E/sensitivity.json" --benchmark deepswe \
  --external examples/external/artificial-analysis-2026-10-08.json --output /tmp/go-v2.html
```

For fresh measurement, check out clean `34d59ca8d5f06ffd7ec310dff74a9b8e7ea40cdc`, install its exact language dependency (C compiler/Python headers required), and use `examples/benchmark-discovery/remeasure-go.py`. Preparation verifies the dataset, trial export, 3,509 patch hashes and 388 in-scope base-file URLs; measurement is offline and identity-bound. The [release details](../../docs/go-parser-v2-release.md) give exact parameters. Do not treat scalar downloads as raw caches or resume v1 records under v2.
