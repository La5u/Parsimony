# Data

Every directory is frozen: records are never edited or relabelled, and changed measurements get a new directory or analyzer version.

## Published boards

| Directory | Board | Analyzer |
|---|---|---|
| [deepswe-python](deepswe-python/README.md) | DeepSWE Python, 26 models × 34 tasks × 4 attempts | 0.5.2-beta |
| [deepswe-javascript](deepswe-javascript/README.md) | DeepSWE JavaScript, 26 × 5 × 4 | 0.7.0-beta |
| [deepswe-typescript](deepswe-typescript/README.md) | DeepSWE TypeScript, 26 × 35 × 4 | 0.7.0-beta |
| [deepswe-go-v2](deepswe-go-v2/README.md) | DeepSWE Go, 26 × 34 × 4; per-model files in a checksummed release asset | 0.8.0-beta |
| [mini-swe-agent-500](mini-swe-agent-500/README.md) | SWE-bench Verified, 34 configurations × 500 tasks | 0.5.2-beta |
| [live-python](live-python/README.md) | SWE-bench Live Lite Python, 4 configurations × 300 tasks | 0.6.0-beta |
| [self-run](self-run/README.md) | Maintainer-run and self-graded newer models on 10 DeepSWE Python tasks (unranked) | 0.5.2-beta |
| [external](external/) | Pinned Artificial Analysis snapshot and model mapping for the DeepSWE chart axis | – |

Each board directory has one JSONL per model (one record per attempt: metrics, outcome, artifact URLs and SHA-256 hashes), `population.json` (the frozen task set; `population.jsonl` for Live), `coverage.json` and a README with the exact import commands.

## Measured but not published

- [priority-live](priority-live/README.md): GPT-5.6 Sol Live JS/TS and PolyBench Opus 4.8 metadata, pending release review.
- [livecodebench-pilot](livecodebench-pilot/README.md): 18 configurations on 1,055 LiveCodeBench tasks, pending provenance review.
- [benchmark-discovery](benchmark-discovery/): source censuses, release evidence and the scripts that produced them.

## Historical

Superseded cohorts, kept so older reports stay reproducible: [deepswe-go](deepswe-go/README.md) (Go v1), [ten-model-500](ten-model-500/README.md), [beta-500](beta-500/README.md) to [beta-500-v5](beta-500-v5/README.md), [three-task-sample](three-task-sample/), the root `ten-model-*` and `smoke-results.jsonl` files and [ten-model-report.md](ten-model-report.md).
