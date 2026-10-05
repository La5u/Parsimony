# Add any benchmark

Every Parsimony page has **Add your own benchmark** near the bottom. Download the example JSON, edit it and open it in the file picker. No installation, patches or analyzer required. Files stay in your browser tab; this does not publish them or modify the published boards.

Any benchmark or language works if you know the amount of code used. Counts are user-provided and unverified. Use one consistent unit and measurement method per file; do not mix lines with tokens, or different tokenizers, languages or scopes. Explain the unit precisely (for example, `Python implementation lines, excluding blank lines and comments`).

```json
{
  "benchmark": "My benchmark v1",
  "unit": "implementation lines",
  "measurement": "total",
  "results": [
    {"model": "Agent A", "task": "task-1", "amount": 12, "solved": true},
    {"model": "Agent B", "task": "task-1", "amount": 8, "solved": true},
    {"model": "Agent A", "task": "task-2", "amount": null}
  ]
}
```

## Fields

- `benchmark`: nonempty benchmark name, ideally with its version/cohort.
- `unit`: nonempty unit definition, including analyzer/version and scope where relevant.
- `measurement`: `total` (amount of code used), `net` (added minus removed), or `churn` (added plus removed). Only net may be negative. None is automatically converted into Parsimony coding units.
- `results`: up to 10,000 attempt records, in a file no larger than 5 MB.
- Each record requires nonempty `model` and `task` strings and a finite numeric `amount` or `null` for missing measurements. Zero is a real measured zero.
- Optional `attempt`: string identifier for repeated attempts. Model/task/attempt combinations must be unique.
- Optional `solved`: `true`, `false`, or `null`/omitted for unknown. Missing correctness is never failure.

The viewer sorts by mean measured amount, smallest first. It separately shows solved-only means, solved / known outcomes, unknown outcomes, and measured / recorded counts. Unknown outcomes are not in the known-outcome denominator. Recorded counts are **not** a benchmark population or coverage claim: include missing records explicitly if you want them visible. Different task mixes and incomplete counts can bias comparisons; use a shared cohort and report it. Footprint is not semantic complexity or correctness.

## Share or propose a public benchmark

Share your JSON with its provenance so anyone can open it locally. To propose inclusion in Parsimony, open a GitHub issue or PR with:

1. The JSON (a PR can put it under `submissions/custom/<benchmark-name>.json`).
2. The benchmark source, license, frozen task cohort and published outcomes, if available.
3. How amounts were measured: unit, scope/exclusions, tool version and reproducible command or source artifacts.
4. Missing measurements, repeat-attempt policy and any differing agent/harness configurations.

Public inclusion requires maintainer review and a separate labeled board; submitting a file does not automatically publish a ranking. No reference panel or combined score is required to explore known code amounts locally.
