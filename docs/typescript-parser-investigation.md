# TypeScript parser coverage investigation

**Outcome (analyzer 0.7.0-beta):** JavaScript and TypeScript are now measured with the official TypeScript parser (`typescript@5.9.3`) instead of `tree-sitter-typescript==0.23.2`. Of the 322 syntax errors in the 0.6.0 DeepSWE TypeScript records, **319 were valid TypeScript** that the old grammar rejected, and only **3 were invalid model code**. See [language tracks](language-tracks.md) for the new backend and [the TypeScript example](../examples/deepswe-typescript/README.md) for the remeasured coverage.

**Remeasurement result** (clean commit `ca37c31`, all 26 configurations): TypeScript analysis errors fell from 323 to 5 of 3,640 records and calibratable tasks rose from 31 to 33 of 35; JavaScript is 520 of 520 measured (was 519). No record that measured under 0.6.0 fails under 0.7.0, and upstream outcomes and patch hashes are identical. On the 3,812 attempts measured by both backends, net units correlate at 0.999 (TypeScript) and 0.9998 (JavaScript); new counts are about 2% higher because node shapes differ. The five remaining errors are the three invalid patches below, one invalid root-level `.cjs` scratch script that a base-file failure used to mask, and the unsupported diff.

## Method (2026-10-01)

1. **Replay.** Every 0.6.0 TypeScript `error` record was re-analysed from its recorded patch (SHA256-verified) and exact base-commit files with the pinned 0.6.0 parser, recording which file failed, on which side (unmodified base file, or only after the patch), and the innermost Tree-sitter `ERROR`/`MISSING` node. The replay reproduced the published counts exactly: 322 syntax errors and one unsupported binary/rename/mode-only diff.
2. **Oracle.** Each of the 65 distinct failing files was checked with the official TypeScript parser (`typescript@5.9.3`, `createSourceFile` parse diagnostics only: no type checking, module resolution or execution). 62 parse cleanly; 3 have genuine syntax errors.
3. **Upstream.** `tree-sitter-typescript` has had no grammar change since 0.23.2 (November 2024), and the causes below are open upstream issues (#348 `export type * as`, #370 variance annotations, #335 generic call signatures separated by line breaks). No newer grammar release was available to evaluate.

## Classification of the 323 error records

Each record is attributed to the first file that failed, so a record counts once.

| Records | Failing side | Cause | Valid TypeScript? |
|---:|---|---|---|
| 177 | base | A generic call signature `<T>(…)` on a new line after an unterminated interface or type member (kea `src/types.ts`, Effect `HttpApiBuilder.ts`) | yes |
| 40 | base | `export type * from` / `export type * as X from` (vitest `public/node.ts`, meriyah, ofetch) | yes |
| 29 | base | A property named `in` on a new line in an object type (dynamodb-toolbox `parseCondition/condition.ts`) | yes |
| 15 | base | Type-parameter variance annotations `in` / `out` (Effect `HttpApi.ts`) | yes |
| 39 | after | Inline import types such as `import('./types').Aspect[]` written by the model | yes |
| 8 | after | A namespace member in a parenthesized type, `(type.Any \| undefined)[]` | yes |
| 3 | after | Contextual keywords as names (`let satisfies`, `using.flags`) | yes |
| 2 | after | `export type *` written by the model | yes |
| 1 | after | A tagged template with type arguments, ``sql<…>`…` `` | yes |
| 5 | after | Other valid constructs | yes |
| 3 | after | Invalid code in the patched file (dynamodb-toolbox ×2, obsidian-linter) | **no** |
| 1 | — | Binary/rename/mode-only implementation diff (not a parser issue) | — |

261 records (81%) failed on an **unmodified base file**: the model's patch was never the problem. The four base-file gaps alone made `effect-sse-httpapi-streaming` and `kea-atomic-signal-selectors` uncalibratable.

## Decision

Patching the unmaintained grammar would need roughly ten separate grammar and external-scanner fixes, and new gaps would keep appearing. The official TypeScript parser defines valid TypeScript, is pinned through npm (`package.json`, `package-lock.json`), and parses syntax without type checking or executing anything. Measurement rules (strict rejection of any syntax diagnostic, no zero-filling, full-file mode only) are unchanged. Because node shapes differ, the JavaScript and TypeScript tracks moved to a new unit version, `typescript-compiler-units-v1`, and both were fully remeasured from a clean commit. 0.6.0 records stay in git history and are never pooled with 0.7.0 records.

Regression fixtures for every construct above live in `tests/test_languages.py` (`test_modern_typescript_rejected_by_the_old_grammar`), alongside invalid-syntax and TypeScript-in-JavaScript rejection tests.

## Remaining issues (unchanged by the parser switch)

- Upstream TS metadata labels `httpx-deterministic-cookie-store` (Python patches) and `prometheus-transactional-reload-status` (Go patches) TypeScript. They remain excluded-only records in this track; correcting them needs an explicit, versioned dataset correction.
- `packages/platform/dtslint/*.tst.ts` (Effect type tests) counts as implementation under the current path rules; a scope rule for `dtslint/` and `.tst.ts` would be a separate versioned change.
