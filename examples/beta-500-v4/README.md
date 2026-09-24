# Verified 500 beta v4: two-submission audit with analyzer 0.4.0

**Beta diagnostic, not an official Parsimony Score or general model ranking.** This reruns the same two complete 500-task cohorts as [v3](../beta-500-v3/README.md) with analyzer `0.4.0-beta` (see the [changelog](../../CHANGELOG.md)). Upstream artifacts and dataset are unchanged, so every difference from v3 comes from the analyzer. Footprint is gated on published SWE-bench Verified outcomes. The audit does **not** execute patches, independently verify correctness, or calibrate a frozen full-task reference panel.

## Pinned inputs

- Analyzer commit `c5a2ee8f49a2ebc0278785a0929c9b6c2538467a`, version `0.4.0-beta`, Python 3.14.7. Every record carries this `analyzer_commit` and one `analyzer_source_sha256`, and `release audit` enforces them against the population. **Never pool** these records with v1–v3.
- Dataset `princeton-nlp/SWE-bench_Verified`, 500 tasks, JSONL SHA256 `82029e78b26e1da0ddc01653c98db18443fab1993e28dff052a38b01c3fd77f7` (same as v3; bytes not committed).
- GitHub experiments revision `40f164d5b8f1d249bf95a6df8b74b577fd8e519d` (same as v3). S3 patches are not versioned by this ref; each record carries its patch SHA256 and URL.
- SHA256 of the files in this directory:
  - [Population manifest](population.json): `bae090cdecae1634a22f4584db64589a2853b0d6e32ec0897fbef26e0699c402`
  - [Opus results](opus46-results.jsonl): `a420eefc9dfe08a50a75c1460774023209d9120aa19559bf5aa813ced97ded7f`
  - [Sonnet results](sonnet45-results.jsonl): `95351943fe3df2c58e699928102064d2d88d11a2b87a9aa857fd67aba90cfecc`
  - [coverage.json](coverage.json): `52700ad54cc7871c7c4b4c433b2aa5e5ff97d6489e9d7817c6743a3c5ee76add`

On a checkout of the pinned analyzer commit:

```sh
python -m parsimony dataset --output verified.jsonl
sha256sum verified.jsonl  # verify against the dataset hash above
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-6-opus \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --resume --output opus46-results.jsonl
python -m parsimony analyze 20260217_mini-v2.0.0_claude-4-5-sonnet-high \
  --dataset verified.jsonl --ref 40f164d5b8f1d249bf95a6df8b74b577fd8e519d \
  --include-failed --resume --output sonnet45-results.jsonl
python -m parsimony.release audit examples/beta-500-v4/population.json \
  opus46-results.jsonl sonnet45-results.jsonl --dataset verified.jsonl --output coverage.json
```

Both cohorts completed in about four minutes on one laptop from a warm cache, with no timeouts or resumes (v3 needed several). A later commit only silences `SyntaxWarning`s that `ast.parse` emits for target-repository sources; a 60-record re-measurement with it matched exactly.

## Coverage

| Metric | Opus 4.6 | Sonnet 4.5 high |
|---|---:|---:|
| Published resolved / 500 | 378 (75.6%) | 357 (71.4%) |
| Resolved full-file analyses | 378/378 | 357/357 |
| Failed patches analyzed | 121 | 141 |
| Analysis errors (all failed patches) | 1 | 2 |
| Successes with zero primary churn | **0** (v3: 22) | **0** (v3: 19) |
| Records whose edits are only identifier/literal changes (`value_only_edit_records`) | 28 | 25 |
| Human-reference errors | **0** (v3: 11) | **0** (v3: 11) |
| Successes with a model/human ratio | 378 (v3: 344) | 357 (v3: 326) |
| Approximate alignments (> 500 token edits) | 2 | 3 |
| Lexical-fallback / out-of-scope successes | 0 / 0 | 0 / 0 |

## What changed from v3

- **Identifier/literal fixes now have a footprint.** Every one of the 41 v3 successes with zero primary churn (e.g. `django__django-11099`, `sphinx-doc__sphinx-10323`) now has positive churn (2–6 tokens). They are counted in `value_only_edit_records`: churn comes only from identifier/literal changes, and `structural_churn` is 0.
- **All human references measure.** v3 failed on 11 gold patches whose hunks sit at shifted line numbers. 0.4.0 applies them by exact context, like `git apply` (`human_metrics.offset_hunks`). No *model* patch needed an offset.
- **Minimal alignment.** `structural_churn` is the v3 metric's token view aligned with an exact minimum edit script. It was never higher than v3's churn, and lower for 30 Opus and 42 Sonnet records, where difflib had overstated edits. Primary net/churn changed for 130 Opus and 155 Sonnet records overall.
- **Errors unchanged.** The three errors are the failed submissions whose patch postimages are already present in the base commits: `django__django-13513` for both agents and `sympy__sympy-13031` for Sonnet. Their footprint remains unknown, not zero; see the [v2 investigation](../beta-500-v2/investigation.md).
- **Approximate records** are large rewrites: `sympy__sympy-13878` (successful for both agents, churn 721 and 727), plus failed `sphinx-doc__sphinx-11510` (both) and `django__django-16263` (Sonnet). Their churn is an upper bound from line-anchored alignment.

## Conditional shared-success diagnostic

There are **335 tasks both agents solved**. On this subset the [separate-metric diagnostic](shared-success-diagnostic.json) reports:

- Median net tokens: **11** (Opus) vs **14** (Sonnet).
- Median churn: **17** vs **20** (v3: 17 vs 19).
- Median model/human churn ratio: 1.0 for both, now over all 335 tasks.

This is *not* an overall Parsimony Score: comparing only shared successes excludes failures and can favor easy tasks. Both submissions use mini-SWE-agent v2.0.0, and 91 of the 335 shared successes have identical patch SHA256s, so a reference panel must not treat all patches as independent.

## Fresh-artifact recheck

[recheck.json](recheck.json) comes from `python -m parsimony.contribute verify` on a seeded random sample of 30 records (`--sample 30 --seed 4`) with an **empty cache**. That run re-downloaded 64 patches and base-commit files. All 30 patch SHA256s matched, and all 30 re-measurements were identical.

This is the same analyzer, not an independent implementation, and not an independent correctness evaluation. Independent random-sample review and a preregistered, deduplicated successful-reference panel remain prerequisites for any official scalar score.

## Offline reproduction from a cache snapshot

`python -m parsimony.snapshot create` packed every cache entry these results depend on: 1,823 files, 44.3 MB raw, 9.6 MB compressed. It covers artifacts, patches and base-commit sources, including those of errored records and renamed files. The ten-model and smoke samples are in the same snapshot.

After `snapshot restore` into an empty cache (every SHA256 is checked on restore), re-running both cohorts, the ten-model sample and the smoke sample reproduced all 1,110 records exactly, and nothing was downloaded. Identical fields: metrics, human metrics, ratios, statuses, provenance and outcomes; only the analyzer identity differed, because the rerun used a newer commit.

The archive is not committed (it is a build artifact in `dist/`). Where it is published is recorded in the [changelog](../../CHANGELOG.md).

