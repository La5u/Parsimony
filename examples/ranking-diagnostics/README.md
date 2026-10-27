# Same-task ranking diagnostics

Descriptive checks of the website's **current same-task net ratio**, not the archived combined score and not a replacement leaderboard. Published measurements and ranks are unchanged. Reports use successful, measured, full-file, in-scope repairs only; unknown footprints are never treated as zero.

## Reports

Each Markdown summary has a JSON companion with complete pairwise comparisons, coverage reasons, source file hashes, and the three largest task/repository/peer influences per configuration.

| Benchmark | Reports |
|---|---|
| DeepSWE | [Python](deepswe-python.md), [JavaScript](deepswe-javascript.md), [TypeScript](deepswe-typescript.md), [Go](deepswe-go.md) |
| SWE-bench Verified | [Verified](verified.md) |
| SWE-bench Live | [Python](live-python.md), [JavaScript](live-javascript.md), [TypeScript](live-typescript.md), [Go](live-go.md) |
| SWEeper | [PHP](sweeper-php.md) |
| SWE-PolyBench Verified | [Python](polybench-python.md) |

The all-languages DeepSWE aggregate is **not** diagnosed here. Its constituent boards are checked independently. Owner-run/contributed configurations are not included in the ranked peer population.

## What the checks mean

- **Coverage:** eligible successful attempts versus published successes, with reasons for excluded successful records and a separate count for published successes absent from resolved records. Attempt coverage is not the same as the number of base tasks used in a ratio.
- **Task influence:** recompute ratios and ranks after removing each base task. DeepSWE's repeated attempts are pooled before removal. Rank ranges are extrema across these omissions, **not confidence intervals**.
- **Repository influence:** repeat after removing each repository. This tests dependence on one repository; it is not a repository-cluster bootstrap. Missing repository identities are grouped explicitly as unknown.
- **Peer influence:** remove one configuration and rebuild the comparison footprints and eligibility gates. Rank changes compare against the original ratios with that candidate absent, so merely removing a competitor does not count as a baseline rank shift.
- **Largest task share:** largest absolute per-task peer footprint divided by the total peer footprint. This can exceed 1 when positive and negative footprints cancel. It measures denominator concentration, not total estimator influence; use omission checks too.
- **Matched comparisons:** for each pair of configurations, report mean net units on the intersection of their solved, measured base tasks. These do not require three other peers. They remain conditional on both configurations succeeding; no causal or significance claim follows from them.

Nonpositive denominators produce unavailable ratios. Unavailable perturbations are counted separately, not assigned a last-place rank. Ranks use the website's three-decimal ratios and competition ties. Harness labels are copied only when explicitly present in provenance; retry policies are not inferred. Consult the pinned run reports linked from each board's source directory for evaluation-protocol differences.

## Reproduce

Python only; no optional parsers or model calls. The full command downloads the checksum-bound DeepSWE Go scalar release asset, not target code or patches:

```sh
scripts/diagnose-rankings.sh /tmp/ranking-diagnostics
# All locally committed cohorts, skipping DeepSWE Go:
scripts/diagnose-rankings.sh /tmp/ranking-diagnostics --offline
```

To diagnose one cohort:

```sh
python -m parsimony.diagnostics examples/live-go/score-panel.json \
  examples/live-go/*-*.jsonl --output /tmp/live-go-diagnostics.json
```

Use the exact cohort input patterns in `scripts/diagnose-rankings.sh`; some directories also contain task-population JSONL files that are not measurement records. JSON reports record input basenames and SHA256 hashes (not temporary directories), so identical inputs reproduce identical reports. No timestamps or random sampling are used.

See [method](../../docs/method.md#website-ranking-same-task-net-ratio-v1) for the metric specification. The checks do not resolve selection bias, missing-measurement bias, uncertainty in upstream outcomes, or different harness/retry protocols. They are sensitivity evidence, not benchmark certification.
