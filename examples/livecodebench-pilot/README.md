# LiveCodeBench Python — static pilot (not a published board)

Six complete generated-code exports share **1,055 tasks**, dated 2023-05-07 through 2025-04-06. Source labels: Claude Opus 4, Claude Sonnet 4, Gemini 2.5 Pro 06-05, DeepSeek R1-0528, EXAONE 4.0 32B and Qwen3 235B A22B. These are newly audited benchmark candidates, **not new 2026 frontier models**.

`population.json` freezes all task IDs, revision, input hashes and sample index **0**, regardless of outcome. Discovery evidence: [`fresh-code-refresh-2026-10-07.json`](../benchmark-discovery/fresh-code-refresh-2026-10-07.json). Samples per task differ (1, 4 or 10), as do filename-reported temperatures (0.2 or 0.6). This is not a controlled model-only comparison or a reproduction of multi-sample pass@1 estimates.

## Measurement

The pilot statically parses extracted `code_list[0]` with Python **3.14.7**. It uses Parsimony's docstring-free `unit_lines` coding units, including EndBlock markers. Complete submitted files count, without repository/path exclusions. The baseline is empty: added = net = submitted units; deleted = 0. This fresh-code scope is separate from SWE implementation-patch boards; never pool them.

Failures remain measured attempts. Empty bodies and syntax errors retain null footprints, not zero. Source-reported `graded_list[0]` Boolean outcomes retain the full denominator. No generated code, tests, imports, model APIs or target environment is executed.

Run from a clean committed checkout; outputs must be external:

```sh
# Fetch each population.json source_bindings URL into external storage;
# verify its sha256, then pass the original model and source filename.
python examples/benchmark-discovery/measure-livecodebench.py \
  --source-revision 6ca212e9c2039373f6e5069d37ffa9db66e23736 \
  --export Claude-Opus-4=Scenario.codegeneration_1_0.2_eval_all.json=/external/opus.json \
  --output-dir /external/new-pilot-output
```

Repeat `--export` for up to all six frozen configurations. The driver rejects changed hashes, subset populations, revision mismatches and dirty tracked code. Numerical rows include task IDs, outcomes, statuses and hashes only. Metadata binds the manifest, input, output rows, script, analyzer sources and commit. Keep raw downloads external; do not commit code, contest statements, prompts or reasoning.

## Release blockers

This directory is **NONPUBLISHED**: no website board or certified evaluation is implied. Before any board release, review contest/dataset and numerical-publication provenance, confirm task/date-window policy against a pinned benchmark dataset (currently frozen from complete exports), and document generation/evaluation configuration evidence. Repository MIT licensing does not independently clear contest material or provider outputs. Model names and temperatures are source/filename claims, not provider attestations.

The six existing SWE pages and their measurements are unchanged. No archived combined scores are fabricated for this pilot.
