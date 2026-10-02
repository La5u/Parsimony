# Gemini 3.5 Flash: Verified battery addition

This adds a source-reported Gemini 3.5 Flash / mini-SWE-agent 2.4.2 run to the
Verified Python board. It is new coverage on that board, not a claim that Gemini
3.5 is the latest Gemini generation globally. No model calls, target installs or
benchmark tests were executed.

## Immutable sources and complete population

- Experiments: `SWE-bench/experiments` at
  `40f164d5b8f1d249bf95a6df8b74b577fd8e519d`,
  `evaluation/verified/20260901_mini-v2.4.2_gemini-3-5-flash`.
- Submitter artifacts: `john-b-yang/20260901_mini-v2.4.2_gemini-3-5-flash`
  at `2f6637a2557da1f7b5f2b583ab7090a077bbeed2`, the run metadata's
  `info.commit`, independently confirmed as the artifact repository commit.
  Mutable `main` links are not the measurement identity.
- The 441 per-instance records contain exact boolean outcomes: 359 resolved and
  82 failed. Aggregate `results/results.json` lists the remaining 59 task IDs
  explicitly as `no_generation`. These sets are disjoint and cover exactly the
  existing 500-task Verified population. Missing per-instance rows alone were
  not interpreted as failures.
- Every one of the 441 separate `logs/<task>/patch.diff` files was fetched and
  checked byte-for-byte against its monolithic prediction. Publication evidence
  contains URLs, hashes and counts, not patch bodies.

The importer now accepts a full immutable `info.commit` as the fallback artifact
pin; explicit `assets.commit` and `assets.ref` retain precedence. The dedicated
reproduction driver independently checks all outcomes and population membership.
Generic importer absence inference has not been weakened.

## Compatible static measurement

The run was measured in a clean detached checkout of
`0aa66dfb6dca76893b0f20e22233317965ff0d25` (0.5.2-beta), with Python 3.14.7.
Its analyzer source hash is
`d758592142590615335aa822027bfc3597dc41b89e4dacfa5d740579796b2b6d`, identical
to the existing Verified measurements. Records were not relabelled to the new
importer commit.

Repo/base metadata is derived from the existing 500-record Opus cohort and
checked against the frozen population during release audit. Files are read from
the exact Git base commits and patches undergo strict full-file analysis. Human
reference comparison is intentionally not computed: the derived metadata does
not include the maintainers' patches, and no reference hash or measurement is
invented.

All 441 submitted attempts have eligible full-file footprints: **359 passing +
82 failed**, mean net units added **36.6031746031746**. The 59 no-generation
records retain their source outcome and have no footprint; they do not contribute
zero. Upstream Solved remains **359/500 = 71.8%**, independently of footprint
coverage **441/500**. Default rank uses all measured attempts, not the solved-only
mean. No population filtering, trimming or correctness tie-break is introduced.

## Release and limitations

Existing 33-model raw records, population and passing-reference score panel stay
unchanged. The panel remains an archived 33-model reference pool, not the default
footprint population. New `scores-34.json`, `coverage-34.json` and
`sensitivity-34.json` supplement rather than overwrite those historical reports.
The footprint website now contains 34 configurations over the same 500 tasks.
The published `gemini-3-5-flash.jsonl` SHA-256 is
`99dde1a4b4cf5562b3e2ac9eb29d2084d257f5029819a948459dea2dec6fcf83`.
All 33 archived combined-score entries reproduce exactly against the unchanged
reference panel; their old files have not been overwritten.

Only attributed numerical records and checksum evidence are distributed.
Public accessibility and an output ownership provision are not a blanket grant
to redistribute another submitter's code, prompts or trajectories. Raw artifacts
and caches remain external. This is not legal certification or a training-reuse
permission. Historical evaluator behavior, provider/model authenticity and
protocol compliance are source-reported, not independently certified. The
harness version differs from older configurations; do not present this as a
controlled model-only experiment.

## Reproduction

From the repository root, using Python 3.14.7:

```sh
git worktree add --detach /tmp/parsimony-verified-measure 0aa66df
PYTHONPATH=. python examples/benchmark-discovery/add-gemini-verified.py inventory \
  --external-dir /tmp/parsimony-gemini-repro
python examples/benchmark-discovery/add-gemini-verified.py measure \
  --external-dir /tmp/parsimony-gemini-repro \
  --analyzer-checkout /tmp/parsimony-verified-measure
```

Use a fresh external output directory. The inventory phase uses the current
importer; the measurement phase explicitly launches the pinned old analyzer.
The manifest binds inventory, repo/base dataset metadata and publication
evidence. It verifies the analyzer checkout is clean before and after analysis.
No target code or tests are run. Keep the generated raw inventory/cache external.
