# Contributing

Issues and pull requests are welcome, including critiques of the method.

## Ways to help

- [Request a model](https://github.com/La5u/Parsimony/issues/new?template=model-request.yml), even without a link. Adding one requires public per-attempt patches and pass/fail outcomes; an export and revision help. An aggregate score is not enough.
- [Report a number that looks wrong](https://github.com/La5u/Parsimony/issues/new?template=number-looks-wrong.yml).
- Question the method with a small patch; see [existing cases](docs/adversarial-validation.md).
- Add a language; see [language tracks](docs/language-tracks.md).
- [Compare your own numbers](docs/custom-benchmarks.md) locally; nothing is uploaded.
- Submit a result bundle or contribute a run below.

Ranked boards use **public artifacts** only. Do not call a model or rerun a benchmark to change a ranked board. [Self-runs](examples/self-run/README.md) and contributed runs are labelled and never ranked.

## Setup

```sh
git clone --depth 1 https://github.com/La5u/Parsimony && cd Parsimony
scripts/check.sh    # tests, page checks and bundle validation, offline
```

Python 3.12 or newer is enough for the Python analyzer. JavaScript/TypeScript tests need Node.js and `npm ci`; Go tests need `pip install '.[languages]'` and a C compiler. Missing extras skip their tests. After changing `parsimony/template.html` or `parsimony/site.py`, run `scripts/rebuild-site.sh` and commit the regenerated `site/` pages. See the [documentation](docs/README.md) for the method and code.

## Contributed runs

Runs use the tasks, scripts, measurement and grading of [self-runs](examples/self-run/README.md). They appear faded and unranked on the front page and DeepSWE Python board, named `Model (effort) · @you`. The maintainer re-measures and re-grades every patch.

1. **Register before running.** Open a pull request that only adds your configuration to `examples/self-run/plan.json`, for example:
   `{"id": "contrib_<you>_<harness>_<model>_<effort>", "harness": "codex", "provider": "openai", "model": "gpt-6-sol", "effort": "high", "tasks": 10, "contributor": "<your GitHub handle>"}`.
   Use the first `tasks` tasks in plan order, at least 5 tasks and 2 attempts per task. `run.py` supports `pi`, `codex` and `claude-code`; another harness needs a change to `run.py` in the same pull request.
2. **Run** on Linux with bubblewrap after the plan pull request merges (setup is in the self-run README):
   `python examples/self-run/run.py $PWD/.scratch/self-run/deep-swe --scratch $PWD/.scratch/self-run --only <id>`
   Do not rerun or drop attempts; publish every planned attempt, including failures.
3. **Submit** `examples/self-run/runs/<id>/` with each attempt's `patch.diff` and `meta.json`, and a public link to `<scratch>/transcripts/<id>/`. Transcript SHA-256s are in `meta.json`. Do not add measurements or outcomes; the maintainer runs `measure.py` and `grade.py`.

## Rules for changes

- Published data is frozen: never edit records in `examples/`. Files in a `release-assets.json` or board population manifest are checksummed, including READMEs. Measurement changes need a new analyzer version and a fresh, separately labelled measurement.
- Unknown outcomes, missing patches and unparseable files stay unknown; never record them as zeros or failures. Errors are never zero.
- Never pool units across languages, benchmarks or analyzer versions.
- Run `scripts/check.sh` before opening a pull request.

## Result bundles

A bundle contains checksummed measured records for one public SWE-bench Verified submission. Export and validate an existing results file:

```sh
python -m parsimony.contribute export examples/mini-swe-agent-500/gemini-3-5-flash.jsonl \
  --agent 20260901_mini-v2.4.2_gemini-3-5-flash --output submissions/your-submission-name
python -m parsimony.contribute validate submissions
```

This reads JSON without network access or analysis. It generates `manifest.json` (agent, task IDs, coverage and checksum), `records.jsonl` (measurements and public provenance) and `leaderboard.json` (summary). Regenerate these files rather than editing them. Do not commit patches or prompts in result bundles.

To measure a new submission on your machine (network and CPU heavy):

```sh
python -m parsimony dataset --output verified.jsonl
python -m parsimony analyze PUBLIC_SUBMISSION_NAME --ref EXPERIMENTS_COMMIT_SHA \
  --dataset verified.jsonl --include-failed --output results.jsonl
python -m parsimony.contribute export results.jsonl --agent PUBLIC_SUBMISSION_NAME \
  --output submissions/your-submission-and-cohort
```

Keep all 500 metadata rows, even for a small sample. Commit the analyzer before measuring so records carry an `analyzer_commit`. Never upload credentials, the download cache or target repositories.

A merged bundle does not automatically add a website row: boards use frozen populations built from complete, audited sources. Offline checks cannot prove measurements match remote patches. Before merging, the maintainer re-downloads and re-measures a random sample:

```sh
python -m parsimony.contribute verify submissions/your-bundle --dataset verified.jsonl --sample 25
```

## Pull request checklist

- Describe what changed and why.
- For data, give the public submission URL and pinned revision, model, harness, analyzer commit, Python version and commands run.
- State how tasks were selected before any result, and list missing or excluded analyses.
- For a contributed run, link the merged plan pull request and public transcript, and give the harness version.
- Confirm `scripts/check.sh` passes.
