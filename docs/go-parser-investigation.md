# DeepSWE Go: all seven analysis errors classified

## Result and release decision

This document preserves the **v1 investigation**. A subsequently implemented, separately versioned correction and full-cohort validation status are documented in [Go parser v2](go-parser-v2-release.md). Use the original stock grammar/environment to reproduce this investigation, not the new same-version-number source package.

The frozen **3,536 records (26 configurations × 136 attempts)** contain exactly
seven `analysis_status=error` records. Static inspection of every in-scope touched
file classifies **six as pinned Tree-sitter limitations and one as invalid
submitted syntax**. There are no unexplained errors in this seven-record census.

| Configuration | Task / attempt | First rejected path (relative to repo) | Side | Classification |
|---|---|---|---|---|
| Claude Opus 4.8 max | arcane-drift-detection-baselines#3 | backend/internal/services/event_service.go | before (also after) | Go 1.26 `new(expression)` grammar gap |
| Claude Sonnet 5 max | arcane-drift-detection-baselines#2 | backend/internal/services/drift_detection_service.go | after, new file | same grammar gap |
| GLM-5.3 max | arcane-drift-detection-baselines#2 | backend/internal/services/event_service.go | before (also after) | same grammar gap |
| GLM-5.3 max | arcane-drift-detection-baselines#3 | backend/internal/services/event_service.go | before (also after) | same grammar gap |
| Kimi K3 max | arcane-drift-detection-baselines#3 | backend/internal/services/drift_detection_service.go | after, new file | same grammar gap |
| Claude Sonnet 4.6 high | helm-array-merge-strategies#2 | pkg/action/upgrade.go | after | fields inserted outside a struct |
| Muse Spark 1.1 xhigh | scriggo-method-declarations#1 | internal/runtime/vm.go | after | grouped declaration at EOF without newline |

All five Arcane attempts are source-reported resolved; Helm and Scriggo are
source-reported failed. **Parser agreement does not certify correctness, types,
imports, buildability or evaluator results.** The six parser-limited attempts
remain missing measurements, not zeros. No published records, scores, population,
reference panel, website or analyzer semantics were changed. These findings do
not authorize silently filling the six missing footprints.

Machine-readable evidence: [go-parser-investigation.json](go-parser-investigation.json).
It contains hashes, provenance URLs, paths, byte lengths, side-specific parser
results, byte offsets, line numbers and classifications, not patches or source.

## Evidence binding and method

Read the handoff, [language rules](language-tracks.md), [scoring policy](archive/scoring.md)
and [Go release README](../examples/deepswe-go/README.md) before auditing.

- Frozen analyzer: `7705e8de13343bbafbfe5bccba665dd2bab8b24a`, 0.6.0-beta,
  source SHA256 `3c7a31f7b62de1f7b786ed8b20e1f49bc41e85069c0783cde41fc8bfae5cdd93`.
  The records retain their original Python 3.14.7 identity.
- Pinned diagnostic parsers: **tree-sitter 0.26.0 / tree-sitter-go 0.25.0**,
  using `/tmp/parsimony-core-audit-venv/bin/python` (Python 3.14.7), and independent
  official **Go 1.23.6 `go/parser`**. The helper uses `AllErrors`, `ParseComments`
  and `SkipObjectResolution`; there is no type checking or package resolution.
  This older official syntax parser accepts general call operands, including
  `new(expression)`: acceptance alone is not proof of pre-1.26 semantic legality.
  The Go 1.26 release notes independently confirm that language feature below.
- Seven patches retrieved by their existing public CloudFront URLs. All seven
  SHA256 values exactly match the records **without any newline restoration**.
  Record-file SHA256, exact JSONL line SHA256 (including newline), line number,
  patch hash and population hash are preserved in the JSON audit.
- Every error record's repository, base commit and analyzer commit agree with
  `examples/deepswe-go/population.json`. Base files were downloaded only from
  `raw.githubusercontent.com/{repo}/{full-base-commit}/{path}`.
- **37 distinct existing in-scope preimage URLs** were fetched across three
  repositories. There are **89 in-scope file pairs**, **54 excluded touched-file
  entries**, and **21 absent before-sides** for new files. Excluded tests/SQL/YAML
  are inventoried but are not analyzed or downloaded separately as base files.
  All 89 strict patch applications succeed; all hunk-offset lists are empty.
- There are **157 present file-sides**, representing **113 unique byte hashes**.
  Go's official parser accepts 156 present sides and rejects only Helm's after
  file. Tree-sitter rejects ten present sides: nine grammar-limited sides and
  Helm's invalid after file. The extra 21 empty before-side parser comparisons
  are deliberate absent-file placeholders: official Go rejects an empty file
  for lacking `package`, whereas Tree-sitter accepts it. These are **not** 21
  invalid submissions and are never classified as failures.
- Diagnostics use byte offsets and computed line numbers, not native Point
  access. Both complete file sides are parsed, including files after the first
  rejection; there is no hunk-only fallback. The production analyzer aborts at
  the first rejection; the audit continues to check for additional problems.

Downloads were bounded to 16 MiB per artifact with 60-second request timeouts;
raw patches, base files and reconstructed sources stay under
`/tmp/parsimony-go-investigation/cache`. No target checkout, installation,
execution, build, test, `go vet`, model call or upstream contact occurred.
Only our standalone parser helper was compiled. This is an investigation, not
new clean-checkout benchmark measurement or an evaluator/provenance certification.

## 1. Arcane: five attempts, `new(expression)`

Repository `getarcaneapp/arcane`, base
`d34a5e2a6c5eb0f0955039775f5b9538424b58ff`.

The shared `event_service.go` base SHA256 is
`3772f95b9586d69fb53457e541a0de9a31611cbec53b20942dece171ce015a9e`.
Tree-sitter reports two one-byte `ERROR` nodes around the string operand of
`new` at each of lines **415, 436, 457, 495, 516**. The file passes official Go
syntax parsing. Opus 4.8 and both GLM attempts touch this base file; these same
ten errors survive unchanged on their after-sides. Their failure is therefore
not caused by invalid syntax newly introduced by the agent.

Sonnet 5 and Kimi K3 do not touch that problematic existing file. They instead
introduce `new` with a string-expression operand in the new
`drift_detection_service.go`. Sonnet's after-side has four one-byte errors at
lines **136 and 264**; Kimi's has two at **322**. Official Go accepts both complete
new files. All other present in-scope sides in these five attempts pass both
parsers.

The pinned grammar recognizes traditional `new(type)` but not all expression
operands. Identifier operands can be parsed as types; string literals cannot.
The synthetic case `package p` followed by a variable initialized with
`new("sample")` reproduces rejection, while `new(string)` is accepted.
[Official Go 1.26 notes](https://go.dev/doc/go1.26) explicitly state that `new`
now permits an expression specifying the initial value. The bounded fetched
HTML was 69,376 bytes, SHA256
`4399238e3ba0509479885d4d8494faa95259014ab11b17be392fbd0f8504affe`;
it remains external. We make no claim about the targets' declared toolchain
compatibility or type correctness from syntax parsing.

## 2. Helm: one invalid after-file

Repository `helm/helm`, base
`42f78ba60edf531d5161e00d9819a7c34d976343`.

Sonnet 4.6's patch inserts two field-style declarations **after** the closing
brace of the `Upgrade` struct in `pkg/action/upgrade.go`. These are not valid
package-level declarations. The before-side passes both parsers; the after-side
fails both. Official Go's first diagnostic is **line 137, column 2, byte offset
5584**, `expected declaration, found MergeStrategies`. Tree-sitter starts its
recovery region at line 137 (offset 5600) and produces many downstream recovery
errors; these are cascades, not separate root causes. The other eight present
before-sides and nine other after-sides pass both parsers (one additional before
is absent for a new file). A tiny synthetic field outside a struct is likewise
rejected by both parsers.

This is genuine syntax invalidity in the submitted implementation, not a grammar
false positive. Its upstream failure remains a distinct outcome field. It should
remain unmeasured even if the Go backend is fixed.

## 3. Scriggo: EOF semicolon handling, no error child

Repository `open2b/scriggo`, base
`11703bb5e02cca28d08fe83ac9a4bdd2e087235e`.

Muse Spark's `internal/runtime/vm.go` before-side passes both parsers; its
31,926-byte after-side passes official Go but fails Tree-sitter. The file ends
with the closing `)` of a grouped `const` declaration and **no final newline**.
The Tree-sitter `source_file` root has `has_error=true`, yet every child has
`has_error=false` and there are **no `ERROR` or missing nodes**. The JSON explicitly
records this unlocalized root error rather than falsely reporting no error.

As a diagnostic-only perturbation, appending one newline yields a 31,927-byte
file accepted by both parsers, SHA256
`ad4de89de6d0083f08b795fa88974d2527bfbc4d617ee89f831c6ffb2ed69987`.
The untouched submitted after-file SHA256 is
`8f4236336b93694f5505ad51b89b12f9f380959fd22c93b65865714730e61fd5`.
A short grouped const declaration at EOF reproduces the root-only flag; the
identical declaration with a newline passes. Grouped `var` and `type`
declarations also exhibit the EOF issue in exploratory synthetic checks. The
confirmed regression test and durable audit control use grouped `const`.
All 16 other file pairs in this attempt pass both parsers.

Do not append a newline to the submitted patch to manufacture a hash match, and
do not weaken `root.has_error` rejection. The newline experiment is not a new
measurement, changed patch or permissible silent normalization.

## Proposed fix — not implemented

These are real backend coverage limitations, not arithmetic or scope bugs.
A future **semantically versioned analyzer release** should either:

1. pin and audit a corrected Go grammar supporting expression operands to
   `new` and correct EOF semicolon handling, retaining strict error rejection;
   or
2. adopt the official Go parser as the Go unit backend with an explicitly new
   unit definition/track, as was done separately for TypeScript.

Even a parser upgrade or parsing-only EOF normalization changes eligibility and
potentially unit shapes/counts. It needs a new analyzer/track identity, synthetic
positive and negative controls, complete Go cohort remeasurement in a clean
committed checkout and new named release artifacts. Do not substitute an official
parser's acceptance for a malformed Tree-sitter AST and then count recovered
units. Do not silently exclude these files, ignore root-only errors or fill
missing values with zero. No fix is implemented here and the scoring formula is
unchanged. Approval of the approach precedes implementation/release work.

## Reproduction and validation

The committed audit and helper contain only tooling and original synthetic code:

```sh
# Supply official Go 1.23.6 for the host architecture, kept under /tmp.
# Audited linux-arm64 archive: https://go.dev/dl/go1.23.6.linux-arm64.tar.gz
# SHA256 561c780e8f4a8955d32bf72e46af0b5ee5e0debe1e4633df9a03781878219202
# Size 70,272,843 bytes; verify checksum before extracting (100 MiB download bound).
GOTOOLCHAIN=local GOCACHE=/tmp/parsimony-go-investigation/build-cache \
  /tmp/parsimony-go-investigation/arm64/go/bin/go build \
  -o /tmp/parsimony-go-investigation/go-parser-audit \
  examples/benchmark-discovery/go-parser-audit.go
/tmp/parsimony-core-audit-venv/bin/python \
  examples/benchmark-discovery/audit-go-parser.py \
  --cache /tmp/parsimony-go-investigation/cache \
  --parser /tmp/parsimony-go-investigation/go-parser-audit \
  --output /tmp/go-parser-investigation.json
cmp docs/go-parser-investigation.json /tmp/go-parser-investigation.json
/tmp/parsimony-core-audit-venv/bin/python -m unittest discover -s tests -q
git diff --check
```

The host was aarch64 and initially had no Go installed. Two checksum-verified
amd64 toolchains (Go 1.27.2 and 1.23.6) failed to start under host emulation;
these were tooling setup failures, not submitted-source failures. The matching
arm64 Go 1.23.6 toolchain successfully built only our helper. Toolchain archives
and build cache remain external.

Validation: all seven patch hashes and population/base bindings pass; all 89
strict file applications have zero offsets; every present side was independently
parsed. Five durable synthetic comparisons pass their expected disagreement or
agreement checks. Three small regression tests preserve current strict rejection
and accepted controls; no production parser code changed. The full pinned Python
suite ran **353 tests, OK, 7 skipped** (existing optional/environment skips).
The focused language suite also passed **26 tests with no skips**. A second audit
run reproduced the committed metadata JSON byte-for-byte (`cmp` passed),
`git diff --check` passed, and every existing Go `.json` / `.jsonl` release
artifact was checked byte-identical to `HEAD`.
The pre-existing local change in `tests/test_livecodebench_pilot.py` was preserved,
not owned or altered by this investigation. Reproduction is static only; none of
these validations ran target tests or executed target code.
