# Parsimony

How much code do AI coding models add? Parsimony measures published patches from public benchmarks. It parses code before and after each patch and counts **coding units** added and removed. It does not run the patches, so anyone can recompute the numbers from the published data.

**[Explore the leaderboard](https://parsimony.lasu.dev)**

## How to read it

Tasks vary in size, and models solve different tasks. The ranking compares each model's net units added on solved tasks with what other models added on those same tasks. A ratio of 0.8× means 20% less code; smaller ratios rank first, and only tasks solved by at least 3 other models count.

The table also shows means for solved attempts and for all measured attempts, the benchmark's solve rate, and measurement coverage. The chart can show added complexity or a task's typical solved patch. **Change chart** filters open-weight or proprietary models without changing rank: the peer set remains the whole board. Language boards can compare two models on tasks both solved; that view does not use the three-peer gate or change rank.

A coding unit is a syntax element such as a statement, call, comparison, name or literal. Comments, formatting, punctuation and name length do not count. Tests, docs and generated files are excluded. See the [counting and ranking methods](docs/method.md).

## Boards

Each benchmark and language has its own board: unit counts cannot be compared across them. The [front page](https://parsimony.lasu.dev/) combines the four DeepSWE language ratios, weighted by shared tasks per language; it does not add units across languages. Browse all boards on the site and find their data and reproduction notes in [examples](examples/README.md). Each data directory has per-attempt measurements, artifact hashes and a frozen task population. A few [self-runs](examples/self-run/README.md) appear faded and unranked on the front page and DeepSWE Python board.

## Quick start

Python 3.12 or newer is required; the Python analyzer has no dependencies.

```sh
git clone --depth 1 https://github.com/La5u/Parsimony && cd Parsimony
scripts/check.sh                    # tests and page checks, offline
scripts/rebuild-site.sh --offline   # rebuild all except index.html and DeepSWE go.html
```

The offline rebuild leaves `site/index.html` and `site/go.html` unchanged or absent. Omit `--offline` to rebuild them too; this downloads a checksum-bound DeepSWE Go data asset. JavaScript and TypeScript tests need Node.js and `npm ci`; Go tests need `pip install '.[languages]'` and a C compiler. Missing extras skip those tests.

Measure a published SWE-bench submission:

```sh
python -m parsimony dataset --output verified.jsonl
python -m parsimony analyze 20250522_sweagent_claude-4-sonnet-20250514 --dataset verified.jsonl --limit 5 --output results.jsonl
```

See [the method](docs/method.md) for more commands, including failed patches, frozen populations, caching and snapshots.

## Limits

- Smaller code is not necessarily better: units do not measure readability or design. Models that write more code also tend to solve more tasks.
- The agent matters. DeepSWE and Verified use mini-SWE-agent except GLM-5.1 on Verified (EvalScope); Live configurations each use their own agent.
- Pass/fail comes from the benchmarks; tests are not rerun. Missing or unparseable attempts are omitted, not treated as zero. Missingness can bias comparisons.
- Rankings describe successful, measured repairs. Models have different comparison tasks and peers; same-task normalization does not remove selection bias. Large patches can dominate the ratio. The 95% ranges cover task resampling, not all uncertainty. See the [ranking specification](docs/method.md#website-ranking-same-task-net-ratio-v1).

## Contributing

Issues, critiques and data are welcome. A link to public per-attempt patches and outcomes is especially useful. See [CONTRIBUTING.md](CONTRIBUTING.md), the [documentation index](docs/README.md) and [changelog](CHANGELOG.md). Contact: [lasushin@proton.me](mailto:lasushin@proton.me).

Licensed under the [MIT License](LICENSE).
