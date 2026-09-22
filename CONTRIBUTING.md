# Contributing benchmark results

Use pull requests to add or update **reproducible result bundles**, not hand-edited scores. All tools use the Python standard library. We welcome small samples when they are clearly labeled.

**Current bundle format:** successful-solution footprint medians, resolve rate and per-task measurements. The [70/30 signed-score calculator](docs/scoring.md) is experimental and separate from bundle validation; do not substitute scalar scores for the generated median summary. You may include a reproducible scalar-score command and frozen panel hash in the PR description. Failed-patch analysis is available with `analyze --include-failed` for supported layouts, but existing bundles and sample scores do not contain it.

## Fast path: existing analysis, no heavy computation

From the checkout, export one agent from an existing Parsimony JSONL file:

```sh
python -m parsimony.contribute export examples/ten-model-results.jsonl \
  --agent 20260217_mini-v2.0.0_claude-4-6-opus \
  --output submissions/20260217-mini-opus46-ten-task-sample

python -m parsimony.contribute validate submissions
```

This only reads JSON and recomputes aggregates. It makes no network requests, runs no patches, and performs no token/AST analysis. Choose a unique descriptive directory name. Export overwrites that directory's three generated files:

```text
submissions/<submission-and-cohort>/
  manifest.json       # format, agent, task IDs, coverage, records checksum
  records.jsonl       # task measurements and public artifact provenance
  leaderboard.json   # generated summary; never edit this by hand
```

Use `sample` results to demonstrate a pipeline or extend coverage—not to claim a full-benchmark score. `complete-record-set` only means 500 task records are present; inspect analysis coverage separately. Comparing different task sets is not a fair head-to-head ranking.

To update a bundle, regenerate it with the same command from the new JSONL. Explain changed task coverage, artifacts, interpreter/analyzer version or bug fixes in the PR. Do not silently relabel an older submission as a newer model. For a new source submission or materially different cohort, use a new directory.

## New artifacts or new tasks

This step is optional and can be CPU/network intensive. Do it on your own machine when appropriate; PR checks never rerun it.

```sh
python -m parsimony dataset --output verified.jsonl
python -m parsimony analyze PUBLIC_SUBMISSION_NAME \
  --ref EXPERIMENTS_COMMIT_SHA --dataset verified.jsonl \
  --task TASK_ID_1 --task TASK_ID_2 --output results.jsonl

python -m parsimony.contribute export results.jsonl \
  --agent PUBLIC_SUBMISSION_NAME --output submissions/your-submission-and-cohort
```

Use all 500 metadata rows even for a small sample, preserving the Verified resolve-rate denominator. Pin upstream revisions where possible and keep the cached artifact bytes locally. Public results, patch locations, hashes and base commits must be preserved in records. Never upload credentials, private patches, the download cache or entire target repositories.

If you introduce a new layout, add a small adapter and mocked tests. Do not call an LLM or rerun SWE-bench to produce a contribution to this public-artifact benchmark.

## PR checklist and review

- Identify the public submission, exact revision/artifact hashes, agent/model and harness.
- Include the analysis/export commands, Python version, analyzer commit and dataset revision/checksum in the PR description.
- Explain task selection **before** discussing the resulting rank. Disclose missing/failed analyses and exclusions.
- Commit all three generated bundle files; regenerate summaries instead of editing them.
- Run `python -m unittest discover -s tests -q` and the offline validator.
- Include before/after summaries and the reason for a score update. Do not conflate analyzer corrections with improved model behavior.

GitHub Actions runs only offline unit tests and bundle validation. It checks checksums, task uniqueness, basic metric identities, resolve totals, scope labels and recomputed summaries. **It cannot prove that contributed measurements match the remote patches or that published results are authentic.** Maintainers review artifact provenance and may reproduce selected measurements before merging. A checksum detects changed bytes, not fabricated data.

Successful patches only are eligible for today's efficiency metrics. The experimental scalar calculator supports bounded failure penalties, but auditing failed-patch coverage and approving an official fixed benchmark/reference panel remain release work. Contributions do not automatically change the frozen sample panel or establish an official benchmark release.

For matched comparisons after merging multiple bundles:

```sh
python -m parsimony leaderboard \
  submissions/agent-a-cohort/records.jsonl \
  submissions/agent-b-cohort/records.jsonl --shared
```

Pass only one record per agent/task. Different analyzer/Python versions are not comparable; the exporter rejects mixed versions within a bundle, but reviewers must also check compatibility across bundles. Keep exploratory samples separate from official benchmark releases.
