# Verified 500 beta v3: indentation-aware two-submission audit

**Beta diagnostic, not an official Parsimony Score or general model ranking.** This reruns both complete 500-task cohorts with the analyzer fix described in the [v2 investigation](../beta-500-v2/investigation.md). It gates footprint on published SWE-bench Verified outcomes; it does **not** execute patches, independently verify correctness, or calibrate a frozen full-task reference panel.

## Pinned inputs

- Analyzer commit `84a1a3dd33807b1e135661bc72cd2461681546c9`, version `0.3.1-beta`, Python 3.14.7. **Never pool** these metrics with v1/v2 records. Canonical `INDENT`/`DEDENT` now count toward primary churn; the secondary value-sensitive diagnostic preserves f-string literal content.
- Dataset `princeton-nlp/SWE-bench_Verified`, 500 tasks, JSONL SHA256 `82029e78b26e1da0ddc01653c98db18443fab1993e28dff052a38b01c3fd77f7` (dataset bytes not committed).
- GitHub experiments revision `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`. S3 patches are not versioned by this GitHub ref; each record carries its patch SHA256 and URL.
- [Population manifest](population.json) SHA256 `6a80c1189a0b5d79032903b85d326d76a534b34d15b0580df93e178616688ef0`; [Opus results](opus46-results.jsonl) SHA256 `4da4676597fc2dbde2466259c39bcbded9ac510607f2e136522e32b77a571afd`; [Sonnet results](sonnet45-results.jsonl) SHA256 `49c79824a6bedafb0cec67e491528a7b7d7af907634a6aa0366d24d70c0300d1`. Coverage counts and exclusions appear in [coverage.json](coverage.json); its source path strings refer to byte-identical `.parsimony-cache/` copies.

On a checkout of the pinned analyzer commit:

```sh
python -m parsimony dataset --output verified.jsonl
sha256sum verified.jsonl # verify against dataset hash above
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-6-opus \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --resume --output opus46-v3-results.jsonl
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-5-sonnet-high \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --resume --output sonnet45-v3-results.jsonl
python -m parsimony.release audit examples/beta-500-v3/population.json \
  opus46-v3-results.jsonl sonnet45-v3-results.jsonl --dataset verified.jsonl --output coverage.json
```

CPU-intensive analyses were resumed after process timeouts; the final 1,000 records have no missing tasks. If a fresh S3 artifact changes, compare its SHA256 to the recorded hash rather than silently replacing it.

## Coverage and conditional diagnostic

| Metric | Opus 4.6 | Sonnet 4.5 high |
|---|---:|---:|
| Published resolved / 500 | 378 (75.6%) | 357 (71.4%) |
| Resolved full-file analyses | 378/378 | 357/357 |
| Failed patches analyzed | 121 | 141 |
| Failed patch analysis errors | 1 | 2 |
| Records with touched files and zero primary churn | 28 | 25 |
| Of those, with positive value-sensitive churn | 28 | 25 |

There are **335 tasks both agents solved**. On this conditional shared-success subset the [separate-metric diagnostic](shared-success-diagnostic.json) reports median net normalized tokens **11** (Opus) vs **14** (Sonnet), and median churn **17** vs **19**. These do *not* represent an overall Parsimony Score; comparing only shared successes excludes failures and can favor easy tasks. Both submissions use mini-SWE-agent v2.0.0. Of their 335 shared successes, 91 have identical patch SHA256s, so panel construction must not treat all reference patches as independent.

The three errors are failed submissions whose patch postimages are already present in the published base commits: `django__django-13513` for both agents, and `sympy__sympy-13031` for Sonnet. Their footprint remains **unknown, not zero**; see the [investigation](../beta-500-v2/investigation.md). The corrected metric finds positive primary churn for the block-moving `sympy__sympy-19637` fix (previously zero), and the diagnostic catches the `pytest-dev__pytest-8399` f-string change. Compared with v2, primary net/churn measurements changed for 256 Opus and 278 Sonnet task records. Identifiers and literals can still change behavior while scoring zero *primary* churn by design: the secondary value-sensitive metric exposes but does not score these edits.

Eight deliberately chosen [fresh-artifact spot checks](recheck.json) matched patch/result hashes and remeasured outputs (including two recorded context failures). They use the **same analyzer**, not an independent implementation or independent correctness evaluation. Independent random-sample review and a preregistered, deduplicated successful-reference panel are prerequisites for any official scalar score. Language expansion should wait.
