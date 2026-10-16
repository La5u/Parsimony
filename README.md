# Parsimony

How much code do AI models add?

Parsimony takes the patches that agents published for public benchmarks (DeepSWE, SWE-bench Verified, SWE-bench Live), parses the code before and after each patch, and counts how many **coding units** each one added and removed. Nothing is run, so anyone can recompute every number from the published data.

**Website: [parsimony.lasu.dev](https://parsimony.lasu.dev)**

## What the leaderboard shows

Some tasks need far more code than others, and each model solves a different set. So each model is ranked by **the net coding units it added on the tasks it solved, divided by what the other models added on those same tasks** (0.8× = 20% less code), smallest first. Only tasks that at least 3 other models solved count. Next to it are the plain mean over solved attempts, the mean over all measured attempts (failures included), the benchmark's own solve rate, and how many attempts could be measured. The chart can also show complexity added (branches, loops, functions), raw or relative to the same tasks, and each task's typical solved patch is shown when you pick a task.

Less code isn't automatically better; see [Limits](#limits).

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

Each benchmark and language has its own board, since unit counts can't be compared across them. The **DeepSWE, all languages** page combines only the four DeepSWE ratios: each model's per-language ratio, averaged with its shared tasks per language as weights (unit counts are never added across languages).

| Page | Benchmark | Models | Tasks × attempts | Analyzer | Data |
|---|---|---:|---|---|---|
| [DeepSWE Python](https://parsimony.lasu.dev/) | DeepSWE v1.1 | 26 | 34 × 4 | 0.5.2-beta | [examples/deepswe-python](examples/deepswe-python/README.md) |
| [DeepSWE JavaScript](https://parsimony.lasu.dev/javascript.html) | DeepSWE v1.1 | 26 | 5 × 4 | 0.7.0-beta | [examples/deepswe-javascript](examples/deepswe-javascript/README.md) |
| [DeepSWE TypeScript](https://parsimony.lasu.dev/typescript.html) | DeepSWE v1.1 | 26 | 35 × 4 | 0.7.0-beta | [examples/deepswe-typescript](examples/deepswe-typescript/README.md) |
| [DeepSWE Go](https://parsimony.lasu.dev/go.html) | DeepSWE v1.1 | 26 | 34 × 4 | 0.8.0-beta | [examples/deepswe-go-v2](examples/deepswe-go-v2/README.md) |
| [DeepSWE, all languages](https://parsimony.lasu.dev/deepswe.html) | DeepSWE v1.1 | 26 | 108 × 4 | per language | the four boards above |
| [SWE-bench Verified](https://parsimony.lasu.dev/verified.html) | SWE-bench Verified | 35 | 500 × 1 | 0.5.2-beta | [examples/mini-swe-agent-500](examples/mini-swe-agent-500/README.md) |
| [Live Python](https://parsimony.lasu.dev/live.html) | SWE-bench Live Lite | 4 | 300 × 1 | 0.6.0-beta | [examples/live-python](examples/live-python/README.md) |
| [Live JavaScript](https://parsimony.lasu.dev/live-javascript.html) | SWE-bench Live MultiLang | 5 | 108 × 1 | 0.10.0-beta | [examples/live-javascript](examples/live-javascript/README.md) |
| [Live TypeScript](https://parsimony.lasu.dev/live-typescript.html) | SWE-bench Live MultiLang | 5 | 111 × 1 | 0.10.0-beta | [examples/live-typescript](examples/live-typescript/README.md) |
| [Live Go](https://parsimony.lasu.dev/live-go.html) | SWE-bench Live MultiLang | 6 | 138 × 1 | 0.10.0-beta | [examples/live-go](examples/live-go/README.md) |
| [SWEeper PHP](https://parsimony.lasu.dev/sweeper-php.html) | SWEeper-Bench | 15 | 128 × 1 | 0.10.0-beta | [examples/sweeper-php](examples/sweeper-php/README.md) |

Each data directory holds one JSONL file per model with every attempt's measurement, the artifact hashes it came from and the frozen task population. The DeepSWE Python page also shows a few newer models I ran myself on 3–10 tasks ([my runs](examples/self-run/README.md)); they're faded and not ranked.

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

- **Smaller isn't always better.** Units measure size, not readability or design.
- **Models that write more code also tend to solve more tasks** (Spearman 0.33–0.60 on the boards with 26+ models).
- **The agent matters**, not only the model. DeepSWE and Verified use mini-SWE-agent for every model except GLM-5.1 on Verified (EvalScope); Live configurations each use their own agent.
- **Pass/fail comes from the benchmarks.** Tests aren't rerun.
- **Some attempts can't be measured** (missing files, parse errors). They're left out, and the Measured column shows how many.

## Contributing

Ideas, critiques and data are welcome. The most useful thing is a link to a public export of per-attempt patches and outcomes for a newer model. See [CONTRIBUTING.md](CONTRIBUTING.md). Contact: [lasushin@proton.me](mailto:lasushin@proton.me).

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
