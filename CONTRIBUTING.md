# Contributing

Issues and pull requests are welcome, including critiques of the method.

## Ways to help

- **Point to a public patch export.** A model can only be added when a benchmark publishes its per-attempt patches and pass/fail outcomes (for example newer models on DeepSWE, SWE-bench Verified or SWE-bench Live). Open an issue with the link and the exact revision. A leaderboard row or aggregate score is not enough; the patches must be downloadable.
- **Question the method.** Is a unit counted wrong? Is a scope rule unfair? Open an issue with a small patch that shows it; [docs/adversarial-validation.md](docs/adversarial-validation.md) has the existing cases.
- **Add a language.** Java, Rust and Vue/Twig templates have no analyzer yet. See [docs/language-tracks.md](docs/language-tracks.md).
- **Compare your own numbers.** Every page has *Add your own benchmark*: load a JSON file of per-task code amounts and compare locally. Nothing is uploaded. See [docs/custom-benchmarks.md](docs/custom-benchmarks.md).
- **Submit a result bundle** measured from public SWE-bench Verified artifacts (below).

Everything must come from **public artifacts**: do not call a model or rerun a benchmark to produce a contribution, because nobody else could verify it. The [self-run pilot](examples/self-run/README.md) is the maintainer's labelled exception and is never ranked.

## Setup

```sh
git clone --depth 1 https://github.com/La5u/Parsimony && cd Parsimony
scripts/check.sh    # Python tests, page checks, bundle validation (about a minute, offline)
```

Python 3.12 or newer is enough for the Python analyzer. JavaScript/TypeScript tests need Node.js and `npm ci`; Go tests need `pip install '.[languages]'` and a C compiler. Missing extras skip their tests.

Where things live:

- Counting rules: `parsimony/analysis.py` (Python) and `parsimony/languages.py` with `typescript_units.cjs` (other languages).
- Importers: `parsimony/deepswe.py`, `live.py`, `polybench.py`; the Verified importer is in `benchmark.py` and `artifacts.py`.
- Website: `parsimony/template.html` (layout, copy, chart) and `parsimony/site.py` (page data). After changing either, run `scripts/rebuild-site.sh` and commit the regenerated `site/` pages.

## Rules for changes

- **Published data is frozen.** Never edit records in `examples/`. A measurement change needs a new analyzer version and a fresh, separately labelled measurement.
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
- `scripts/check.sh` passes.
