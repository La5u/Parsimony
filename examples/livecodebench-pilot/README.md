# LiveCodeBench Python — static pilot (not a published board)

The initial six complete generated-code exports share **1,055 tasks**, dated 2023-05-07 through 2025-04-06: Claude Opus 4, Claude Sonnet 4, Gemini 2.5 Pro 06-05, DeepSeek R1-0528, EXAONE 4.0 32B and Qwen3 235B A22B. An expanded snapshot binds **18 configurations** to the same full population, adding GPT-4o, o3/o4-mini High, Grok 3 Mini High, Llama 3.3, Mistral Large, Codestral, QwQ, Qwen 2.5 Coder, DeepSeek V3 and Opus/Sonnet 4 Thinking. These are newly audited benchmark candidates, **not new 2026 frontier models**.

Original `population.json` and `measurement-summary.json` remain immutable six-configuration snapshots, reproducible with the driver at `2645271`. Current `population-18.json` versions the source bindings without changing full task membership or sample index **0**. Five exports cover only 713 or 880 tasks; absent tasks remain unknown outcomes and null footprints in the full 1,055-task population. Grok and DeepSeek V3 have 13 and 30 missing entire code lists with available Boolean outcomes; those footprints remain null, not inferred zeros. Other malformed code/grade pairings are rejected.

Discovery evidence: [`initial audit`](../benchmark-discovery/fresh-code-refresh-2026-10-07.json) and [`expansion audit`](../benchmark-discovery/livecodebench-expansion-2026-10-07.json). The expansion census's `blocked_for_shared1055` describes incompatibility with the original **complete-export-only** driver; the versioned retained-population policy explicitly records exact subset membership and missing artifacts instead of silently treating them as complete. Source sample counts/temperatures differ. This is not a controlled model-only comparison or a reproduction of multi-sample pass@1 estimates.

## Measurement

The pilot statically parses extracted `code_list[0]` with Python **3.14.7**. It uses Parsimony's docstring-free `unit_lines` coding units, including EndBlock markers. Complete submitted files count, without repository/path exclusions. The baseline is empty: added = net = submitted units; deleted = 0. This fresh-code scope is separate from SWE implementation-patch boards; never pool them.

Failures remain measured attempts. Empty bodies, absent code lists/tasks and syntax errors retain null footprints, not zero. Source-reported `graded_list[0]` Boolean outcomes retain the full denominator; absent task outcomes stay unknown. For partial exports, observed solved / 1,055 is explicitly a lower bound with an unknown-outcome interval, not a complete solve rate. No generated code, tests, imports, model APIs or target environment is executed.

Run from a clean committed checkout; outputs must be external:

```sh
# Fetch each population-18.json source_bindings URL into external storage;
# verify its sha256, then pass the original model and source filename.
python examples/benchmark-discovery/measure-livecodebench.py \
  --source-revision 6ca212e9c2039373f6e5069d37ffa9db66e23736 \
  --export Claude-Opus-4=Scenario.codegeneration_1_0.2_eval_all.json=/external/opus.json \
  --output-dir /external/new-pilot-output
```

Repeat `--export` for up to all 18 frozen configurations (quote specifications containing spaces). The driver rejects changed hashes, any export subset other than its exact pinned membership, revision mismatches and dirty tracked code. Numerical rows include task IDs, outcomes, statuses and hashes only. Metadata binds the manifest, input, output rows, script, analyzer sources and commit. Keep raw downloads external; do not commit code, contest statements, prompts or reasoning.

## Initial six-configuration feasibility results

Clean analyzer commit `2645271` / Python 3.14.7 completed **6,263 measurements / 6,330 attempts**, preserving all 1,055 tasks per configuration. Input/output/analyzer bindings and exact means are in [`measurement-summary.json`](measurement-summary.json); per-attempt scalar rows remain external and reproducible with the driver.

| Source model | Measured / 1,055 | Source solved / 1,055 | Mean units, all measured | Mean units, solved |
|---|---:|---:|---:|---:|
| Claude Opus 4 | 1,030 | 658 | 131.09 | 99.14 |
| Claude Sonnet 4 | 1,024 | 627 | 120.67 | 95.58 |
| DeepSeek R1-0528 | 1,054 | 893 | 180.07 | 150.91 |
| EXAONE 4.0 32B | 1,050 | 856 | 186.88 | 154.76 |
| Gemini 2.5 Pro 06-05 | 1,054 | 889 | 169.39 | 137.46 |
| Qwen3 235B A22B | 1,051 | 848 | 165.72 | 139.98 |

These are feasibility statistics, not a model-quality ranking. The 67 unavailable footprints are 24 empty bodies and 43 parse errors; all outcomes remain recorded. No no-generation outcome is inferred from an empty body.

## Expanded 18-configuration snapshot

[`measurement-summary-18.json`](measurement-summary-18.json) combines the unchanged original six metadata records with **12 new configurations**, measured from clean `cbe8768` / Python 3.14.7. The analyzer source hash and exact unit definition match the original pilot. Unchanged inputs were not remeasured. Total: **17,353 eligible static measurements / 18,990 retained task-attempt slots**. Missing footprints remain explicit: **1,209 absent tasks, 43 missing code lists, 318 empty bodies and 67 syntax errors**.

| Additional source configuration | Exported tasks | Measured / 1,055 | Observed source solved / 1,055 | Mean units, all measured |
|---|---:|---:|---:|---:|
| GPT-4o 2024-08-06 | 1,055 | 1,047 | 402 | 119.36 |
| o3 High | 1,055 | 991 | 894 | 155.66 |
| o4-mini High | 1,055 | 1,038 | 921 | 183.20 |
| Grok 3 Mini High | 1,055 | 958 | 824 | 152.94 |
| Llama 3.3 70B Instruct | 713 | 707 | 257* | 104.08 |
| Mistral Large | 880 | 878 | 328* | 123.51 |
| Codestral Latest | 880 | 876 | 315* | 111.50 |
| QwQ Max Preview | 880 | 875 | 704* | 158.33 |
| Qwen 2.5 Coder 32B Instruct | 713 | 657 | 339* | 113.30 |
| DeepSeek V3 | 1,055 | 957 | 525 | 135.87 |
| Claude Opus 4 Thinking | 1,055 | 1,052 | 743 | 123.92 |
| Claude Sonnet 4 Thinking | 1,055 | 1,054 | 723 | 125.22 |

`*` Partial export: only observed successes are known; missing-task outcomes are **unknown**, not failures. Observed solved / 1,055 is a lower bound, not a complete rate. Exact unknown-outcome intervals and solved-only means are in each numerical metadata entry. Do not rank these as coding ability, infer provider identity from source labels, or compare configuration variants as controlled reasoning-effort experiments.

To reproduce the initial six byte-identically use driver/manifest at `2645271`; to reproduce new measurements use the 18-binding manifest and driver at `cbe8768`. Each metadata record retains its original manifest, script and clean analyzer hashes rather than being relabelled to the latest commit. Raw caches and attempt rows remain external.

## Release blockers

This directory is **NONPUBLISHED**: no website board or certified evaluation is implied. Before any board release, review contest/dataset and numerical-publication provenance, confirm task/date-window policy against a pinned benchmark dataset (currently frozen from complete exports), and document generation/evaluation configuration evidence. Repository MIT licensing does not independently clear contest material or provider outputs. Model names and temperatures are source/filename claims, not provider attestations.

The six existing SWE pages and their measurements are unchanged. No archived combined scores are fabricated for this pilot.
