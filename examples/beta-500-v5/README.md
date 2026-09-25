# Verified 500 beta v5: two-submission audit with coding units (analyzer 0.5.0)

**Beta diagnostic, not an official Parsimony Score or general model ranking.** This reruns the same two complete 500-task cohorts as [v4](../beta-500-v4/README.md) with analyzer `0.5.0-beta`, which measures **coding units** (AST elements: statements, expressions, comparisons, names, literals and block ends) instead of lexical tokens (see the [changelog](../../CHANGELOG.md)). Upstream artifacts and dataset are unchanged, so every difference from v4 comes from the analyzer. Footprint is gated on published SWE-bench Verified outcomes. The audit does **not** execute patches, independently verify correctness, or calibrate a frozen full-task reference panel.

## Pinned inputs

- Analyzer commit `54bd8a6926aa7542dca2ad6a3b0147c2a2e2cf85`, version `0.5.0-beta`, Python 3.14.7. Every record carries this `analyzer_commit`, and `release audit` enforces it against the population. **Never pool** these records with v1–v4.
- Dataset `princeton-nlp/SWE-bench_Verified`, 500 tasks, JSONL SHA256 `82029e78b26e1da0ddc01653c98db18443fab1993e28dff052a38b01c3fd77f7` (same as v3 and v4; bytes not committed).
- GitHub experiments revision `40f164d5b8f1d249bf95a6df8b74b577fd8e519d` (same as v3 and v4). S3 patches are not versioned by this ref; each record carries its patch SHA256 and URL.
- SHA256 of the files in this directory:
  - [Population manifest](population.json): `980086d2999b858d628661d629238830540df26b54cb143f0e3eb21087d6f231`
  - [Opus results](opus46-results.jsonl): `b292d724fb44273728c91339f9fcb71d0a18ca7c0317f05e92b3f5aa6b56a1af`
  - [Sonnet results](sonnet45-results.jsonl): `bcbff35c6a6195578761779126cb0880bce8b71d510a7ffeca0b7b954b11f964`
  - [coverage.json](coverage.json): `cfcb3259df7c7e3451bf5ee6913162c0d6aebf8f20745fd3a952fe6d13023cb7`

On a checkout of the pinned analyzer commit:

```sh
python -m parsimony dataset --output verified.jsonl
sha256sum verified.jsonl  # verify against the dataset hash above
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-6-opus \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --output opus46-results.jsonl
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-5-sonnet-high \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --output sonnet45-results.jsonl
python -m parsimony.release audit examples/beta-500-v5/population.json \
  opus46-results.jsonl sonnet45-results.jsonl --dataset verified.jsonl --output coverage.json
```

Both cohorts completed in about five minutes on one laptop from the v4 cache, with no downloads, timeouts or resumes. The v4 [cache snapshot](../../CHANGELOG.md) contains every input these results depend on.

## Coverage

| Metric | Opus 4.6 | Sonnet 4.5 high |
|---|---:|---:|
| Published resolved / 500 | 378 (75.6%) | 357 (71.4%) |
| Resolved full-file analyses | 378/378 | 357/357 |
| Failed patches analyzed | 121 | 141 |
| Analysis errors (all failed patches) | 1 | 2 |
| Records with unknown units (a file does not parse) | 0 | 0 |
| Successes with zero unit churn | 0 | 0 |
| Records whose edits are only identifier/literal changes (`value_only_edit_records`) | 31 (v4: 28) | 29 (v4: 25) |
| Human-reference errors | 0 | 0 |
| Approximate alignments (> 500 edits) | 2 | 3 |
| Lexical-fallback / out-of-scope successes | 0 / 0 | 0 / 0 |

Errors and approximate records are the same tasks as in v4: the errors are failed patches whose postimages are already present in the base commits (`django__django-13513` for both agents, `sympy__sympy-13031` for Sonnet), and the approximations are the large rewrites `sympy__sympy-13878` (both, successful), `sphinx-doc__sphinx-11510` (both, failed) and `django__django-16263` (Sonnet, failed).

`value_only_edit_records` rose slightly because `structural_churn` is now unit-based and ignores the values of all constants and names. Tokens treated `None` as a keyword, so `FILE_UPLOAD_PERMISSIONS = None` → `0o644` (`django__django-10914`) was a structural token edit; in units it is a changed literal. Likewise a dotted import module (`distutils.version` → `pkg_resources`, `astropy__astropy-7671`) is one unit, not several tokens.

## Units versus tokens

Every record still carries the 0.4.0 token metrics as diagnostics (`net_tokens`, `token_churn`), and every successful record's `token_churn` equals its v4 `churn`, so the two metrics can be compared on identical patches.

- **Units are about two-thirds of tokens** (median ratio 0.66): punctuation, brackets, dots and commas no longer count.
- **They rank patches almost identically.** Spearman correlation between unit and token churn is 0.99 for both cohorts. Of the 335 shared successes, the Opus-vs-Sonnet churn ordering reverses on only 5 tasks.
- **Where they disagree, units are usually more sensible.** On `django__django-12774`, tokens penalized Opus's single `any(...)` expression for its import line and dotted names (53 vs 48 tokens), while units favor it over Sonnet's flag, loop, `break` and two nested `if`s (29 vs 35 units). Neither metric notices that Sonnet reused Django's existing `total_unique_constraints` helper, which a reviewer would likely prefer.

## Conditional shared-success diagnostic

There are **335 tasks both agents solved**. On this subset the [separate-metric diagnostic](shared-success-diagnostic.json) reports:

- Median net units: **7** (Opus) vs **8** (Sonnet); median net tokens 11 vs 14 as in v4.
- Median unit churn: **12** vs **12** (token churn 17 vs 20).
- Median model/human unit churn ratio: 1.0 for both.
- Opus has smaller / equal / larger unit churn on 122 / 149 / 64 tasks. 91 shared successes have identical patch SHA256s.

This is *not* an overall Parsimony Score: comparing only shared successes excludes failures and can favor easy tasks. Both submissions use mini-SWE-agent v2.0.0, so a reference panel must not treat all patches as independent. Nearly half the shared tasks tie, because most Verified fixes are tiny and admit essentially one solution; units do not change that.

## Fresh-artifact recheck

[recheck.json](recheck.json) comes from `python -m parsimony.contribute verify` on a seeded random sample of 30 records (`--sample 30 --seed 4`) with an **empty cache**. That run re-downloaded 64 patches and base-commit files. All 30 patch SHA256s matched, and all 30 re-measurements were identical.

This is the same analyzer, not an independent implementation, and not an independent correctness evaluation.

## What units do not measure

Coding units count size and nesting, not readability or design. A patch that hardcodes a test input can cost fewer units than a general fix, and reusing an existing helper is not rewarded beyond its smaller size. Test-overfitting detection, nesting depth and reuse signals are separate future diagnostics.
