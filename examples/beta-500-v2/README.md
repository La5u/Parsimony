# Verified 500 beta v2: two submissions, frozen population

**Historical beta diagnostic (superseded for metric comparisons by the [investigation](investigation.md)); not an official benchmark leaderboard.** These are static code-footprint measurements gated by published SWE-bench Verified results; we did not execute agent patches or independently verify SWE-bench correctness. Both submissions use mini-SWE-agent v2.0.0; harness diversity and independent metric review are still missing.

## Provenance and reproduction

- **Do not use the conditional median comparisons below as current scores:** the investigation found behavior-changing indentation moves and f-string literal edits that `0.3.0-beta` measured as zero. They remain here to make the investigation reproducible, not to rank models.
- Analyzer commit: `70de30522a079a2a45673b48a2c7ce8c8b558ac5` (Python 3.14.7, `0.3.0-beta`). This commit fixes the false generated-file exclusions found in [the v1 audit](../beta-500/README.md) and includes Django's migration framework implementation while excluding migration scripts.
- Dataset: `princeton-nlp/SWE-bench_Verified`, 500 test rows, SHA256 `82029e78b26e1da0ddc01653c98db18443fab1993e28dff052a38b01c3fd77f7`. Exact dataset JSONL is not checked in; verify the checksum after fetching.
- Published results GitHub revision: `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`; S3 patches are content-hashed **per task**, not versioned by the GitHub revision. Each record retains patch, result, base-commit provenance.
- [population.json](population.json) SHA256 `901658f4dfb2ab37b9dc3e5ea6a6a88aa53856e82f7facb6e9a267ca24611181`. Both [Opus 4.6](opus46-results.jsonl) (SHA256 `be804dc26e003d874ce244885bcb3be37274bfb61395856c59f49fb4e407fe96`) and [Sonnet 4.5 high](sonnet45-results.jsonl) (SHA256 `5ccf1e3c899e2311c95bf827b7de8901bc11f7a0676b31af7bd9f0991d0ef7df`) have 500 task records. [coverage.json](coverage.json) is the coverage audit (source paths refer to `.parsimony-cache/`, with byte-identical copies here).

At the analyzer commit above, in a clean checkout:

```sh
python -m parsimony dataset --output verified.jsonl
sha256sum verified.jsonl  # verify dataset hash above
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-6-opus \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --resume --output opus46-results.jsonl
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-5-sonnet-high \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --resume --output sonnet45-results.jsonl
python -m parsimony.release audit examples/beta-500-v2/population.json \
  opus46-results.jsonl sonnet45-results.jsonl --dataset verified.jsonl --output coverage.json
```

Full-file analysis is CPU-heavy. `--resume` continues after interruption while checking analyzer version, result hash, agent and ref. One transient Opus source-download error on `django__django-11740` was retried using `--task` and its single record replaced after verifying the same published result and analyzer version; other errors were **not** replaced with zero footprints.

## Coverage and matched-success diagnostic

| Measurement | Opus 4.6 | Sonnet 4.5 high |
|---|---:|---:|
| Published resolved (out of 500) | 378 (75.6%) | 357 (71.4%) |
| Resolved full-file analyses | 378/378 | 357/357 |
| Failed patches analyzed | 121 | 141 |
| Failed-patch analysis errors | 1 | 2 |
| Records with zero primary normalized churn, touched paths | 29 | 26 |
| Of those, with positive value-sensitive churn | 27 | 24 |

The [shared-success diagnostic](shared-success-diagnostic.json) matches **335** successfully analyzed tasks. Within this *conditional-on-both-solving* set, the median primary net token delta is **10** (Opus) vs **13** (Sonnet); median churn is **15** vs **18**. These medians **do not rank overall model quality**: they discard failure tasks, are sensitive to normalization and exclusions, and are not the experimental frozen-panel scalar score. Both submissions share a harness and have differing published resolve rates. No official 500-task score/reference panel has been approved.

The remaining full-file analysis errors are strict context mismatches against Verified base commits: `django__django-13513` for both agents, and `sympy__sympy-13031` for Sonnet. All are published **failed** attempts; their failed-footprint scores remain bounded/unknown. They cannot be counted as zero edits. Opus has only four excluded paths (`.txt` documentation and a `.pyi` stub); Sonnet has none. Compared with the v1 Opus audit, 31 task net/churn measurements changed (27 resolved, four failed). For example `django__django-11740` changed from zero to 30 churn after including migration framework code, and `django__django-13012` from zero to 21 after fixing a false generated-code match. **Never pool the v1 and v2 measurements.**

## Spot checks and limits

The [eight-case fresh-cache recheck](recheck.json) downloaded result bytes, patches and base source files afresh; hashes matched provenance, and remeasurement reproduced six successes/known failures and two recorded context errors. This uses **the same analyzer**, so it verifies selected artifact identity/recomputation, **not** independent correctness or metric validity. The checked-in files preserve all task records and allow offline audit. A third party should independently reproduce a random, preregistered patch sample and adjudicate context errors and excluded files before an official release.

**Next:** investigate the failed-patch/base mismatches; audit value-only edits and remaining excluded paths; preregister a full-population successful-reference panel before computing any scalar score. Then test additional harnesses and panel/weight sensitivity. More languages are not yet a priority.
