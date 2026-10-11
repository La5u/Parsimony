# Versioned Go parser correction — analyzer 0.8

## Implementation

The [seven-error investigation](go-parser-investigation.md) identified six parser-limited attempts and one invalid submitted patch in the frozen Go v1 cohort. Analyzer **0.8.0-beta** implements a distinct **`tree-sitter-go-units-v2`** track:

- Runtime: `tree-sitter==0.26.0`.
- Grammar: immutable upstream PR #190 source, `botanica-consulting/tree-sitter-go@97cacdcb9e1e699f7b3dfed21386da60ed6e63cd`.
- Source URL: `https://codeload.github.com/botanica-consulting/tree-sitter-go/tar.gz/97cacdcb9e1e699f7b3dfed21386da60ed6e63cd`.
- Archive SHA256: `c653dd381ce89f883393f6d4db7aa1f27772dad79cc932c0f3aff5b15dc9b588`.
- Explicit EOF policy: `append-one-lf-if-nonempty-without-final-lf-v1`.

This grammar is an **unmerged patch**, not an official upstream fixed release. It still reports package version 0.25.0, so the analyzer additionally verifies installed PEP 610 archive URL/checksum metadata. Stock 0.25.0 is rejected for v2. Source metadata is a reproducibility binding, not independent binary authenticity certification. The grammar hash and EOF policy are recorded in every measurement track.

The grammar admits Go 1.26 expression operands to `new`. Before parsing, exactly one LF is appended to nonempty owned source bytes lacking a final LF. This makes the EOF semicolon policy explicit for grouped declarations. Downloaded files and patches, and all recorded source/patch hashes, remain unchanged. Any recovered/error-flagged tree is still rejected; the invalid Helm patch must remain unavailable. No official-parser fallback, ignored error flag, hunk-only estimate or missing-zero imputation is introduced.

Synthetic controls cover literal/call/binary/type operands, **shadowed `new` and `make` identifiers**, grouped const/var/type EOF, newline-equivalent units/rows/end markers, malformed allocations/declarations and the misplaced-field failure. The initial PR #193 candidate was rejected when the first configuration of the full-cohort run exposed a regression on the previously accepted `wazero-multi-module-snapshots#1` Fable patch: indexing a variable named `new` produced an erroneous parser error. That interrupted run is not a release. PR #190 handles shadowing; its AST labels differ on some legacy syntax, which is why the entire cohort is remeasured under a new track instead of assuming count compatibility. JavaScript/Python unit semantics and footprint ranking are unchanged.

## Full-cohort release gate

The v1 Go files under `examples/deepswe-go/` retain their original analyzer/track identities. They are not relabelled or selectively backfilled. A v2 replacement requires remeasurement of **all 26 configurations × 136 attempt slots = 3,536 records**, with the same 34 task populations and four attempt memberships, and a new named population/reference panel.

`examples/benchmark-discovery/remeasure-go.py`:

1. Copies and binds original record bytes, identities and outcome memberships.
2. Retrieves exact pinned upstream task/trial exports; reconstructs the dataset and checks its frozen SHA256.
3. Downloads existing recorded patches with their exact SHA256s and immutable base-commit sources, externally, with request size/time bounds.
4. Requires a clean checkout at a supplied full analyzer commit, matching source hash, track and Python 3.14.7.
5. Remeasures the full cohort offline and verifies task/outcome/base/patch provenance invariants.
6. Produces a new population, coverage report, archived panel and field-by-field comparison externally, without overwriting the historical release.

Preparation downloads raw inputs only; target source is not installed, executed, built or tested. The optional grammar build compiles parser tooling, not benchmark submissions.

## Reproduction

```sh
# Use an environment with Python 3.14.7 and the source dependency in pyproject.toml.
# A compiler and Python headers are needed to build this immutable grammar source.
PY=/path/to/pinned-environment/bin/python
$PY examples/benchmark-discovery/remeasure-go.py prepare \
  --repo "$PWD" --root /tmp/parsimony-go-v2-release
$PY examples/benchmark-discovery/remeasure-go.py verify \
  --root /tmp/parsimony-go-v2-release
# Commit analyzer code; create a detached clean worktree at that exact commit.
# Export analyzer_identity() and track('go') from that worktree, then pass them:
$PY /path/to/clean-worktree/examples/benchmark-discovery/remeasure-go.py measure \
  --root /tmp/parsimony-go-v2-release --worktree /path/to/clean-worktree \
  --commit FULL_ANALYZER_SHA --source-sha256 ANALYZER_SOURCE_SHA256 \
  --track-json /tmp/go-v2-track.json --version 0.8.0-beta \
  --name deepswe-v1.1-go-v0.8
```

## Full-cohort results and numerical release

The complete cohort was remeasured offline at clean **`34d59ca8d5f06ffd7ec310dff74a9b8e7ea40cdc`**, analyzer source SHA256 **`14101e9b3d0fbb419be6744951bc58b2a5ca92ddf48750cc16ab38edbd0ccf9b`**, Python 3.14.7. All **3,536 records** retain their original task, outcome, resolve-total, patch and base bindings. Exact task/trial inputs, **3,509 patch hashes** and **388 in-scope preimage URLs** were verified before measurement. The dataset remains byte-identical to v1.

| Status | Historical v1 | Go v2 |
| --- | ---: | ---: |
| Measured in-scope | 3,502 | **3,508** |
| Analysis error | 7 | **1** |
| Missing patch | 2 | 2 |
| No-logs/unknown, unanalyzed | 25 | 25 |
| Total slots | 3,536 | 3,536 |

All **3,502 commonly measured attempts retain identical primary unit/token footprint values**; common human-reference net/churn also agree. Three identifier-insensitive structural-churn diagnostics increase by two because grammar labels change; they do not affect footprint ranking or the archived formula. Six formerly missing attempts are recovered (five upstream successes, one upstream failure). The single malformed Helm after-file remains unmeasured. No previously measured attempt loses eligibility. Five model means change only because their recovered attempts now enter the denominator/sum.

The new population, coverage, pooled 136-slot reference panel, archived scores and stability diagnostics were regenerated separately. The Go website uses v2; historical JSON/JSONL artifacts remain unchanged. Other boards' measurement payloads are unchanged; their Sources metadata now links to the v2 Go manifest.

See [release README](../examples/deepswe-go-v2/README.md), [validation summary](../examples/deepswe-go-v2/validation-summary.json) and [configuration comparison](../examples/deepswe-go-v2/comparison-summary.json). Large scalar record/panel/comparison files are in a checksummed [release asset](https://github.com/La5u/Parsimony/releases/tag/deepswe-go-v0.8); its [committed member bindings](../examples/deepswe-go-v2/release-assets.json) and downloader verify every byte before extraction. The archive contains no raw source, submitted patches, prompts, trajectories or dataset reference-patch text. Numerical scalar releases do not imply rights to redistribute those artifacts.

Measurement integrity is not independent correctness/model/evaluator certification. Synthetic tests are not substituted for cohort validation; full-cohort measurements are not substituted for benchmark execution.
