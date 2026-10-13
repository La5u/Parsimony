# Parsimony

How much code do coding agents write to fix real issues?

Parsimony takes the patches that agents published for public benchmarks (DeepSWE, SWE-bench Verified, SWE-bench Live), parses the code before and after each patch, and counts how many **coding units** each one added and removed. It never runs the code, never calls a model and never reruns a benchmark: every number comes from public artifacts and can be recomputed.

**Website: [parsimony.lasu.dev](https://parsimony.lasu.dev)** · Status: research preview

## What the leaderboard shows

Each model is ranked by its **mean net coding units added over the attempts that solved the task**, smallest first. Next to it are the same mean over all measured attempts (failures included), the benchmark's own solve rate, and how many attempts could be measured.

A smaller footprint is not a better model. Units measure size, not readability or design, and models that write more code also tend to solve more tasks. See [Limits](#limits).

## A worked example

A coding unit is one syntax element: a statement, call, comparison, name or literal. Comments, formatting, punctuation and name length do not count. This patch replaces a loop with `sum`:

```diff
 def total(items):
-    result = 0
-    for item in items:
-        result = result + item
-    return result
+    return sum(items)
```

The analyzer counts **13 units removed and 3 added: net −10**. Try it:

```python
from parsimony.analysis import measure
before = 'def total(items):\n    result = 0\n    for item in items:\n        result = result + item\n    return result\n'
patch = '--- a/calc.py\n+++ b/calc.py\n@@ -1,5 +1,2 @@\n def total(items):\n-    result = 0\n-    for item in items:\n-        result = result + item\n-    return result\n+    return sum(items)\n'
print(measure(patch, get_source=lambda path: before)['net_units'])  # -10
```

The full counting rules, scope (test, docs and generated files are excluded) and alignment are in [docs/method.md](docs/method.md).

## Boards

Benchmarks and languages are never pooled: raw units are not comparable across languages or analyzer versions.

| Page | Benchmark | Models | Tasks × attempts | Analyzer | Data |
|---|---|---:|---|---|---|
| [DeepSWE Python](https://parsimony.lasu.dev/) | DeepSWE v1.1 | 26 | 34 × 4 | 0.5.2-beta | [examples/deepswe-python](examples/deepswe-python/README.md) |
| [DeepSWE JavaScript](https://parsimony.lasu.dev/javascript.html) | DeepSWE v1.1 | 26 | 5 × 4 | 0.7.0-beta | [examples/deepswe-javascript](examples/deepswe-javascript/README.md) |
| [DeepSWE TypeScript](https://parsimony.lasu.dev/typescript.html) | DeepSWE v1.1 | 26 | 35 × 4 | 0.7.0-beta | [examples/deepswe-typescript](examples/deepswe-typescript/README.md) |
| [DeepSWE Go](https://parsimony.lasu.dev/go.html) | DeepSWE v1.1 | 26 | 34 × 4 | 0.8.0-beta | [examples/deepswe-go-v2](examples/deepswe-go-v2/README.md) |
| [SWE-bench Verified](https://parsimony.lasu.dev/verified.html) | SWE-bench Verified | 35 | 500 × 1 | 0.5.2-beta | [examples/mini-swe-agent-500](examples/mini-swe-agent-500/README.md) |
| [Live Python](https://parsimony.lasu.dev/live.html) | SWE-bench Live Lite | 4 | 300 × 1 | 0.6.0-beta | [examples/live-python](examples/live-python/README.md) |

Each data directory holds one JSONL file per model with every attempt's measurement, the artifact hashes it came from and the frozen task population. The DeepSWE Python page also shows a few newer models the maintainer ran and graded on 10 tasks ([self-run pilot](examples/self-run/README.md)); they are faded and never ranked.

## Quick start

Python 3.12 or newer; the Python analyzer has no dependencies.

```sh
git clone --depth 1 https://github.com/La5u/Parsimony && cd Parsimony
scripts/check.sh                    # tests and page checks, offline
scripts/rebuild-site.sh --offline   # rebuild the pages from committed data
```

JavaScript and TypeScript need Node.js and `npm ci`; Go needs `pip install '.[languages]'` and a C compiler. Without them those tests are skipped. To measure a published SWE-bench submission yourself:

```sh
python -m parsimony dataset --output verified.jsonl
python -m parsimony analyze 20250522_sweagent_claude-4-sonnet-20250514 --dataset verified.jsonl --limit 5 --output results.jsonl
```

More commands (failed patches, frozen populations, caching, snapshots) are in [docs/method.md](docs/method.md).

## Limits

- **Size is not quality.** Small code can be cryptic, wrong beyond the tests or hard to maintain; a larger patch may add useful validation.
- **Bigger footprints go with higher solve rates.** On every board with 26 or more models, the Spearman correlation between the solved-only footprint and the solve rate is 0.33–0.60.
- **The agent matters.** Footprints depend on the harness and its settings, not only the model. DeepSWE and Verified use mini-SWE-agent for every model except GLM-5.1 on Verified (EvalScope); Live configurations each use their own agent.
- **Outcomes are the benchmark's.** Pass/fail comes from the published results; Parsimony does not rerun tests.
- **Coverage is partial.** Some attempts cannot be measured (missing artifacts, unparseable files); they are excluded, never counted as zero, and shown in the Measured column.

## Contributing

Ideas, critiques and data are welcome. The most useful thing is a link to a public export of per-attempt patches and outcomes for a newer model. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Repository map

| Path | What it is |
|---|---|
| `parsimony/` | Analyzer (`analysis.py`, `languages.py`), importers (`deepswe.py`, `live.py`, `polybench.py`), site generator (`site.py`, `template.html`) |
| `examples/` | Published data per board, plus historical cohorts (see [examples/README.md](examples/README.md)) |
| `site/` | The generated website pages |
| `scripts/` | `check.sh` and `rebuild-site.sh` |
| `docs/` | Method, language tracks, validation; `docs/archive/` holds dated investigations |
| `HANDOFF.md`, `TODO.md`, `CHANGELOG.md` | Maintainer notes, backlog and history |

Licensed under the [MIT License](LICENSE).
