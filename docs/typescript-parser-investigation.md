# TypeScript parser coverage investigation

**Scope:** classify the known pinned-parser failures in the published TypeScript track and propose a versioned repair. This investigation does not change parsing, scoring, measurements, or published artifacts.

## Published-record summary

Summaries were computed by streaming the 26 JSONL files in `examples/deepswe-typescript/` with Python (not loading or printing the large records). Across 3,640 records, `analysis_status=error` occurs 323 times: 322 report `ValueError: invalid or recovered typescript syntax`, and one reports `ValueError: implementation binary/rename/mode-only diff unsupported`. The current record schema retains the generic parser error, not a Tree-sitter error span or file path, so the published records alone cannot classify all 322 syntax errors.

Two tasks with known base-file grammar limitations have the following syntax-error totals. These task-level counts do not attribute every error to the cited construct:

| Task | Error attempts | Exact base | Known construct |
|---|---:|---|---|
| `vitest-duration-sharding` | 37 (10 + 10 + 8 + 9) | `vitest-dev/vitest` `647e6ade3b99523e3a0387a65fccfe918c331236` | `export type * as` in `packages/vitest/optional-types.d.ts` (lines 4, 7); also re-export at `packages/vitest/src/public/node.ts:209` |
| `effect-sse-httpapi-streaming` | 101 (25 + 25 + 25 + 26) | `Effect-TS/effect` `9245bc59ebfa688e8c92dd691296ee69d0815e59` | existing generic overloaded call-signature value in `packages/platform/src/HttpApiBuilder.ts:910-937`; the surrounding code is a callable type with multiple generic signatures assigned an implementation |

The remaining errors include 96 on `kea-atomic-signal-selectors` (23 + 24 + 23 + 22), plus errors on other tasks. Those counts describe error records, **not distinct invalid source files**; do not infer all other failures are invalid model output. A separate TypeScript grammar walk of source at the two base commits reproduced rejection of the cited files with the pinned parser. It also found other modern TypeScript forms in Effect, including variance annotations (`in` / `out`) in `packages/platform/src/HttpApiEndpoint.ts:55-65`; these are relevant evidence of grammar-version limitations but not the primary minimal overload fixture below.

## Evidence and classification

### Vitest type-only namespace export

- Base source: [optional-types.d.ts at the frozen base commit](https://github.com/vitest-dev/vitest/blob/647e6ade3b99523e3a0387a65fccfe918c331236/packages/vitest/optional-types.d.ts#L1-L8) and [public/node.ts](https://github.com/vitest-dev/vitest/blob/647e6ade3b99523e3a0387a65fccfe918c331236/packages/vitest/src/public/node.ts#L205-L211).
- The declaration `export type * as jsdomTypes from 'jsdom'` is a TypeScript type-only namespace re-export, not a malformed patch. The pinned Tree-sitter TypeScript grammar (`tree-sitter-typescript==0.23.2`, with `tree-sitter==0.26.0`) rejects a minimal instance in the new regression test.
- Classification: **base grammar coverage limitation (high confidence)**. The `.d.ts` file is excluded from measurement and serves only as corroborating grammar evidence; the same construct in the in-scope `src/public/node.ts` is the relevant measurement case. Rejection of existing base syntax cannot establish that an attempt's edited syntax is invalid.

### Effect callable overload signatures

- Base source: [HttpApiBuilder.ts at the frozen base commit](https://github.com/Effect-TS/effect/blob/9245bc59ebfa688e8c92dd691296ee69d0815e59/packages/platform/src/HttpApiBuilder.ts#L910-L940).
- This is a `const` with a type literal containing several generic call signatures and a compatible implementation expression. A reduced two-signature fixture, representative of that declaration shape, is rejected by the pinned parser. This checks the parser only; no Effect tests, TypeScript compiler, or repository code were run.
- Existing base syntax can prevent full-file analysis for any attempt touching that file. The generic published errors do not establish which file or phase caused each of the 101 failures. Do not label all those model patches malformed.
- Classification: **base grammar limitation (high confidence that the pinned parser rejects the fixture and base file; medium confidence about the precise missing grammar production responsible)**. The published parser error does not provide a per-file node span, and the source contains other unsupported modern TS constructs, so we should not claim the overload alone is the sole cause for every rejected changed file.

## Regression fixture

`tests/test_languages.py::TreeSitterLanguageTests.test_pinned_typescript_grammar_rejects_published_base_constructs` pins two small examples to the commits and source locations above, and asserts that the current pinned backend rejects them. It does not suppress parser errors, allow recovered trees, assign zero metrics, or run source code. Like other grammar tests, it is skipped when optional parser dependencies are absent. The standard measurement contract in `docs/language-tracks.md` remains unchanged: syntax-error trees are unmeasured.

## Proposed versioned repair (not implemented)

1. Evaluate a Tree-sitter TypeScript grammar revision (or alternate parser) that accepts both base constructs and representative TSX/declaration-file cases. Test a broader curated corpus, including modern variance annotations, generic overload declarations, malformed syntax, and recovery nodes; do not make acceptance depend only on these two fixtures.
2. Keep strict rejection for genuinely malformed/recovered trees. Add failure diagnostics (path and stable parser error spans) to a **new** analysis-record schema/version so future error audits can distinguish base parse failure, after-file parse failure, and unsupported diff without changing old records.
3. If parser or syntax-unit traversal semantics change, publish a new measurement-track / unit-version identity (for example `tree-sitter-units-v2`) with exact dependency pins and analyzer version. Do not rewrite the existing `tree-sitter-units-v1` records or panels.
4. From a clean, committed analyzer checkout, regenerate records for the complete frozen TypeScript cohort using the existing dataset/base commits. Audit coverage and before/after measurement deltas, verify unchanged task/outcome metadata, then rebuild the population/panel/scores/uncertainty/pages together as a new release. Compare current and candidate coverage before publishing; never splice recovered records into the current board.
5. Treat wrong-language task metadata and other after-only errors as separate investigations. A parser upgrade cannot justify silently moving tasks, dropping failures, or attributing every old error to grammar coverage.

No published measurements, scores, panels, site pages, or `.claude/` contents were changed in this investigation.
