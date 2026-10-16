# Contributing

Issues and pull requests are welcome, including critiques of the method.

## Ways to help

- **Request a model.** [Open a model request](https://github.com/La5u/Parsimony/issues/new?template=model-request.yml), even without a link. A model can only be added when a benchmark publishes its per-attempt patches and pass/fail outcomes (for example newer models on DeepSWE, SWE-bench Verified or SWE-bench Live), so a link to such an export and its revision helps most. A leaderboard row or aggregate score is not enough.
- **Report a number that looks wrong.** Every board links to [a short form](https://github.com/La5u/Parsimony/issues/new?template=number-looks-wrong.yml) that fills in the board and task.
- **Question the method.** Is a unit counted wrong? Is a scope rule unfair? Open an issue with a small patch that shows it; [docs/adversarial-validation.md](docs/adversarial-validation.md) has the existing cases.
- **Add a language.** Java, Rust and Vue/Twig templates have no analyzer yet. See [docs/language-tracks.md](docs/language-tracks.md).
- **Compare your own numbers.** Every page has *Add your own benchmark*: load a JSON file of per-task code amounts and compare locally. Nothing is uploaded. See [docs/custom-benchmarks.md](docs/custom-benchmarks.md).
- **Submit a result bundle** measured from public SWE-bench Verified artifacts (below).
- **Contribute a run.** Have API credits or a subscription? Run a model on the self-run tasks (below). It appears faded and unranked next to my runs, labelled with your handle.

Ranked boards come only from **public artifacts**: do not call a model or rerun a benchmark to change a ranked board, because nobody else could verify it. [Self-runs](examples/self-run/README.md) and contributed runs are the labelled exception and are never ranked.

## Setup

```sh
git clone --depth 1 https://github.com/La5u/Parsimony && cd Parsimony
scripts/check.sh    # Python tests, page checks, bundle validation (about a minute, offline)
```

The checkout is about 330 MB, almost all measurement data in `examples/`.

Python 3.12 or newer is enough for the Python analyzer. JavaScript/TypeScript tests need Node.js and `npm ci`; Go tests need `pip install '.[languages]'` and a C compiler. Missing extras skip their tests.

Where things live:

- Counting rules: `parsimony/analysis.py` (Python) and `parsimony/languages.py` with `typescript_units.cjs` (other languages).
- Importers: `parsimony/deepswe.py`, `live.py`, `polybench.py`; the Verified importer is in `benchmark.py` and `artifacts.py`.
- Website: `parsimony/template.html` (layout, copy, chart) and `parsimony/site.py` (page data). After changing either, run `scripts/rebuild-site.sh` and commit the regenerated `site/` pages.

## Contributed runs

Contributed runs use the same tasks, scripts, measurement and grading as [my self-runs](examples/self-run/README.md), and show on the front page and the DeepSWE Python board faded, unranked and named `Model (effort) · @you`. I re-measure and re-grade every patch myself, so the numbers never depend on you; what nobody can check is that the patch really came from the model you name, which is why these runs are never ranked.

1. **Register first.** Open a pull request that only adds your configuration to `examples/self-run/plan.json`, before running anything:
   `{"id": "contrib_<you>_<harness>_<model>_<effort>", "harness": "codex", "provider": "openai", "model": "gpt-6-sol", "effort": "high", "tasks": 10, "contributor": "<your GitHub handle>"}`.
   Use the plan's task order (the first `tasks` tasks) and its 2 attempts per task; at least 5 tasks. `run.py` supports the `pi`, `codex` and `claude-code` harnesses; another harness needs a small change to `run.py` in the same pull request.
2. **Run** on Linux with bubblewrap, after the plan pull request is merged:
   `python examples/self-run/run.py ~/deep-swe --scratch ~/parsimony-self-run --only <id>` (setup as in the self-run README). Don't rerun or drop attempts you dislike: every planned attempt is published, failed ones included.
3. **Submit** a pull request with `examples/self-run/runs/<id>/` (each attempt's `patch.diff` and `meta.json`) and a public link to `<scratch>/transcripts/<id>/`, whose SHA-256s are in `meta.json`. Don't add measurements or outcomes: I run `measure.py` and `grade.py` and publish the results.

## Rules for changes

- **Published data is frozen.** Never edit records in `examples/`. Files listed in a `release-assets.json` or a board's population manifest are checksummed, including their READMEs; CI fails with "part of a frozen release" if one changes. A measurement change needs a new analyzer version and a fresh, separately labelled measurement.
- **Missing is not zero.** Unknown outcomes, missing patches and unparseable files stay unknown; never fill them with zeros or failures.
- **Keep boards separate.** Never pool units across languages, benchmarks or analyzer versions.
- Run `scripts/check.sh` before opening a pull request.

## Result bundles

A bundle is a checksummed copy of measured records for one SWE-bench Verified submission. Export one from an existing results file:

```sh
python -m parsimony.contribute export examples/mini-swe-agent-500/gemini-3-5-flash.jsonl \
  --agent 20260901_mini-v2.4.2_gemini-3-5-flash --output submissions/your-submission-name
python -m parsimony.contribute validate submissions
```

This reads JSON only: no network, no patches, no analysis. It writes three files; regenerate them instead of editing them:

```text
submissions/<submission-and-cohort>/
  manifest.json      # agent, task IDs, coverage, records checksum
  records.jsonl      # per-task measurements and public artifact provenance
  leaderboard.json   # generated summary
```

To measure a submission that is not in the repository yet (network and CPU heavy, run on your machine):

```sh
python -m parsimony dataset --output verified.jsonl
python -m parsimony analyze PUBLIC_SUBMISSION_NAME --ref EXPERIMENTS_COMMIT_SHA \
  --dataset verified.jsonl --include-failed --output results.jsonl
python -m parsimony.contribute export results.jsonl --agent PUBLIC_SUBMISSION_NAME \
  --output submissions/your-submission-and-cohort
```

Keep all 500 metadata rows even for a small sample, so the solve-rate denominator stays right. Commit the analyzer before measuring so records carry an `analyzer_commit`. Never upload credentials, the download cache or target repositories.

**What happens next.** A merged bundle does not add a row to the website by itself: boards use frozen task populations that the maintainer builds from complete, audited sources. Offline checks verify checksums, task uniqueness and recomputed summaries, but cannot prove the measurements match the remote patches, so before merging the maintainer re-downloads and re-measures a random sample:

```sh
python -m parsimony.contribute verify submissions/your-bundle --dataset verified.jsonl --sample 25
```

## Pull request checklist

- What changed, and why.
- For data: the public submission URL and pinned revision, model and harness, analyzer commit, Python version, and the commands you ran.
- How tasks were selected, stated before any result, plus missing or excluded analyses.
- For a contributed run: the merged plan pull request, harness version and a public transcript link.
- `scripts/check.sh` passes.
