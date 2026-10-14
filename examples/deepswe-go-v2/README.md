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
