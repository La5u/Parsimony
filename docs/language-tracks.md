# Optional JavaScript, TypeScript and Go tracks

Analyzer **0.6.0-beta** adds an optional Tree-sitter backend. Python still uses the standard-library AST and needs no runtime dependencies. The scoring formula is unchanged: footprint credit for passing patches and footprint penalties for explicitly failed patches, averaged over the frozen score-panel tasks; unavailable measurements remain bounds.

## Install

Use the same Python version for every record in a comparison (the existing boards use **3.14.7**):

```sh
uv venv --python 3.14.7 .venv
uv pip install --python .venv/bin/python -e '.[languages]'
.venv/bin/python -m unittest discover -s tests -q
```

Exact pins: `tree-sitter==0.26.0`, `tree-sitter-javascript==0.25.0`, `tree-sitter-typescript==0.23.2`, `tree-sitter-go==0.25.0`. Imports are lazy; missing or different grammar versions fail with installation guidance rather than falling back to invented counts. The tests skip grammar-dependent cases without this extra; run both environments before publishing.

## The same small measurement pipeline

1. Apply the unified diff strictly to the exact base-commit files, without executing anything.
2. Parse both complete files with the grammar selected by extension.
3. Walk syntax units in preorder: statements, expressions, declarations, types, names and literals. Ignore comments, punctuation and a small explicit list of syntactic wrappers. Fold operators/modifiers into their containing unit; preserve names and literal content. Add an `EndBlock` marker to blocks so nesting/movement costs edits.
4. Use the **same Myers unit alignment** as Python: `units_added`, `units_deleted`, `net_units = added − deleted`, `churn = added + deleted`. Large changes use the existing flagged approximation. Identifier/literal-insensitive churn and branch-count complexity delta are diagnostics, not the score.
5. Reject syntax-error/recovery trees as analysis errors. An unavailable parse is not a zero-size patch. Full-file mode is required; there is no hunk-only grammar fallback.

This is deliberately syntax-derived footprint, **not semantic complexity, maintainability or runtime behavior**. Tree-sitter has different node shapes from Python's AST; raw unit counts must not be compared across tracks. Literal spellings are not fully semantically canonicalized; equivalent escapes/numeric spellings can count as changes. JSX text and template-string content remain significant. Tests cannot certify all grammar constructs.

Tree traversal uses byte offsets and Python-computed line starts, avoiding a native Point-access crash observed with large files on the pinned Python 3.14 / Tree-sitter 0.26.0 combination. Large-tree traversal has a regression test.

## Scope and provenance

- JavaScript: `.js`, `.jsx`, `.mjs`, `.cjs`; TypeScript: `.ts`, `.tsx`, `.mts`, `.cts`; Go: `.go`.
- **JS- and TS-labelled task tracks both measure JS and TS implementation files**: projects mix them, and DeepSWE labels its KaTeX task JavaScript although its reference fix is TypeScript. Extension selects the grammar; TSX has its own grammar. Go and Python remain separate scopes.
- Exclude test/spec/benchmark paths and filenames, dependency/vendor/build/docs/generated directories, TypeScript declaration files, generated protobuf Go files, minified JS, and explicit generated headers in the **base** file. An agent cannot hide edits by adding a generated header.
- New root-level JS/TS/Go files count: root Go packages and JS/TS entry points are normal implementation. The existing Python-only scratch-file rule is unchanged.
- Each non-Python record, its metrics, frozen population and score panel identify the `measurement_track`: task language, `tree-sitter-units-v1`, and exact dependency versions. Freeze, scoring, sensitivity, stability and coverage reject incompatible tracks. Do not relabel existing Python records as 0.6.0 or pool them with new measurements.
- A track is chosen by dataset metadata, never inferred from whether an individual attempt passed. All attempts in that population remain records. A task without any measured passing reference cannot calibrate the current score and is explicitly absent from the score panel, not silently called a failure.

## DeepSWE workflow

The task snapshot already used by the Python board has 35 TypeScript, 34 Go and 5 JavaScript tasks: **74 additional tasks / 296 attempts per model**. Python plus these tracks covers 108 of 113 task definitions; Rust remains unsupported.

```sh
git clone https://github.com/datacurve-ai/deep-swe /tmp/deep-swe
git -C /tmp/deep-swe checkout 0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea

# Commit analyzer changes first. Run measurements from that clean revision.
PY=.venv/bin/python
$PY -m parsimony.deepswe dataset /tmp/deep-swe --language go --output /tmp/go.jsonl
$PY -m parsimony.release freeze /tmp/go.jsonl --name deepswe-v1.1-go-v0.6 --output /tmp/go-population.json

# Use a fresh cache for mutable upstream metadata, not an old immutable URL cache.
$PY -m parsimony.deepswe --cache /tmp/deepswe-refresh configs --output /tmp/configs.json
$PY -m parsimony.deepswe --cache /tmp/deepswe-refresh analyze mini_swe_agent_claude_opus_5_max \
  --dataset /tmp/go.jsonl --output /tmp/opus-go.jsonl
```

Repeat for every selected configuration, separately for `javascript`, `typescript`, and `go`. Inspect errors, missing patches, excluded-only successes, grammar failures and approximation counts **before** freezing a pooled reference panel or publishing a ranking. Use `parsimony.release audit` against each language population. Never concatenate language records into a single score panel.
