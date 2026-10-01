# Optional JavaScript, TypeScript and Go tracks

Analyzer **0.7.0-beta** measures JavaScript and TypeScript with the **official TypeScript parser** and Go with Tree-sitter. Python still uses the standard-library AST and needs no runtime dependencies. The scoring formula is unchanged: footprint credit for passing patches and footprint penalties for explicitly failed patches, averaged over the frozen score-panel tasks; unavailable measurements remain bounds.

Analyzer 0.6.0 used Tree-sitter for JavaScript/TypeScript as well (`tree-sitter-units-v1`, `tree-sitter-typescript==0.23.2`). That grammar is unmaintained upstream and rejected valid modern TypeScript; 319 of the 322 TypeScript syntax errors in the 0.6.0 DeepSWE records were valid code ([investigation](typescript-parser-investigation.md)). The 0.6.0 records remain in git history; never pool them with 0.7.0 records.

## Install

Use the same Python version for every record in a comparison (the existing boards use **3.14.7**):

```sh
uv venv --python 3.14.7 .venv
uv pip install --python .venv/bin/python -e '.[languages]'   # Go: tree-sitter==0.26.0, tree-sitter-go==0.25.0
npm ci                                                       # JavaScript/TypeScript: typescript@5.9.3 (Node.js)
.venv/bin/python -m unittest discover -s tests -q
```

Dependencies load lazily. A missing Node.js, a missing or different `typescript` version, or missing/different Go grammar versions fail with installation guidance rather than falling back to invented counts. Set `PARSIMONY_TYPESCRIPT_DIR` to a directory whose `node_modules` contains the pinned parser when running outside this checkout, and `PARSIMONY_NODE` to choose the Node.js binary. Tests skip each backend that is not installed; run with both before publishing.

## The same small measurement pipeline

1. Apply the unified diff strictly to the exact base-commit files, without executing anything.
2. Parse both complete files. JavaScript/TypeScript: `parsimony/typescript_units.cjs`, a long-lived Node process, parses each file with `typescript@5.9.3` (script kind by extension: `.ts/.mts/.cts`, `.tsx`, `.js/.mjs/.cjs`, `.jsx`) inside a one-file program with no library, module resolution, type checking or emit. Go: Tree-sitter.
3. Walk syntax units in preorder: statements, expressions, declarations, types, names and literals. Ignore comments, JSDoc, punctuation and a small explicit list of syntactic wrappers (expression statements, parentheses, template spans, import/export clauses, JSX expression containers). Fold operators, modifiers and keywords into their containing unit (`BinaryExpression[+]`, `VariableStatement[export,const]`, `ImportDeclaration[type]`); preserve names and literal values (string literals by value, so quote style is formatting). Add an `EndBlock` marker to blocks and class bodies so nesting/movement costs edits. Whitespace-only JSX text containing a line break is formatting and is skipped.
4. Use the **same Myers unit alignment** as Python: `units_added`, `units_deleted`, `net_units = added − deleted`, `churn = added + deleted`. Large changes use the existing flagged approximation. Identifier/literal-insensitive churn and branch-count complexity delta are diagnostics, not the score.
5. Reject any syntax diagnostic, including TypeScript-only syntax in a JavaScript file, as an analysis error that names the file and line. An unavailable parse is not a zero-size patch. Full-file mode is required; there is no hunk-only fallback.

This is deliberately syntax-derived footprint, **not semantic complexity, maintainability or runtime behavior**. The TypeScript and Tree-sitter ASTs have different node shapes, and neither matches Python's AST: raw unit counts must not be compared across tracks or unit versions. Numeric literal spellings are not canonicalized. JSX text and template-string content remain significant. Tests cannot certify all grammar constructs.

Go tree traversal uses byte offsets and Python-computed line starts, avoiding a native Point-access crash observed with large files on the pinned Python 3.14 / Tree-sitter 0.26.0 combination. Large-tree regression tests cover both backends.

## Scope and provenance

- JavaScript: `.js`, `.jsx`, `.mjs`, `.cjs`; TypeScript: `.ts`, `.tsx`, `.mts`, `.cts`; Go: `.go`.
- **JS- and TS-labelled task tracks both measure JS and TS implementation files**: projects mix them, and DeepSWE labels its KaTeX task JavaScript although its reference fix is TypeScript. The file extension selects the script kind; TSX and JSX are parsed as such. Go and Python remain separate scopes.
- Exclude test/spec/benchmark paths and filenames, dependency/vendor/build/docs/generated directories, TypeScript declaration files, generated protobuf Go files, minified JS, and explicit generated headers in the **base** file. An agent cannot hide edits by adding a generated header.
- New root-level JS/TS/Go files count: root Go packages and JS/TS entry points are normal implementation. The existing Python-only scratch-file rule is unchanged.
- Each non-Python record, its metrics, frozen population and score panel identify the `measurement_track`: task language, unit version (`typescript-compiler-units-v1` for JavaScript/TypeScript, `tree-sitter-units-v1` for Go) and exact parser versions. Freeze, scoring, sensitivity, stability and coverage reject incompatible tracks. Do not relabel existing records with a newer analyzer version or pool them with new measurements.
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
