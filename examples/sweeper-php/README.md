# SWEeper-Bench — PHP

Website: **[parsimony.lasu.dev/sweeper-php.html](https://parsimony.lasu.dev/sweeper-php.html)**.

[SWEeper-Bench](https://sweeperbench.com) gives agents a running web application and an open-ended prompt naming a product area; a browser agent then checks that the target bug is fixed (*target*) and that related behaviour still works (*preservation*). Each of its 200 tasks comes from a different repository. Most are PHP applications, so this board measures the PHP code each agent changed.

**This compares model + agent setups, not models alone:** each model ran in its own agent (Codex, Claude Code, Cursor, Kimi Code and others), at the effort shown. Pass/fail is SWEeper's own verdict, not rechecked here. One attempt per task, so rank ranges are wide.

## Population

All tasks whose **maintainers' reference fix** changes at least one in-scope PHP file (`.php`, `.phtml`; tests, vendor and generated code excluded): **128 of 200**. The rule uses only the reference fix, never model output or outcomes. `reference-files/` holds the changed-file lists (GitHub compare `base...reference`; Codeberg commit files for the one Codeberg task, which is Go). `population.jsonl` lists task, repository and base commit; `population-manifest.json` freezes it.

Every one of the 128 tasks is kept for every configuration. Measurements count PHP files only; other files in a patch (JavaScript, templates, CSS) are listed as excluded, not counted.

## Results (analyzer 0.10.0-beta, `tree-sitter-php-units-v1`)

| # | Model · agent | Net units, solved (mean) | Net units, all measured (mean) | Solved / 128 | Measured / 128 |
|---:|---|---:|---:|---:|---:|
| 1 | Qwen3.8 Max (none) · Codex | +8.2 | +29.6 | 40 | 112 |
| 2 | GLM-5.3 Flash (max) · Codex | +22.9 | +29.0 | 55 | 114 |
| 3 | Kimi K3 (high) · Kimi Code | +39.4 | +40.7 | 66 | 115 |
| 4 | DeepSeek V4.1 Flash (xhigh) · DeepSeek harness | +40.7 | +39.2 | 68 | 120 |
| 5 | GPT-5.6 Terra (xhigh) · Codex | +42.7 | +38.5 | 46 | 103 |
| 6 | GPT-5.6 Luna (xhigh) · Codex | +49.7 | +45.1 | 57 | 106 |
| 7 | Muse Spark 1.3 (xhigh) · Muse Code | +54.2 | +45.3 | 65 | 112 |
| 8 | Claude Opus 5 (xhigh) · Claude Code | +55.3 | +52.4 | 71 | 117 |
| 9 | GLM-5.3 (max) · Codex | +61.7 | +43.9 | 56 | 118 |
| 10 | DeepSeek V4 Pro (xhigh) · DeepSeek harness | +64.0 | +64.4 | 66 | 117 |
| 11 | GPT-5.6 Sol (xhigh) · Codex | +68.7 | +70.5 | 63 | 114 |
| 12 | GPT-6 Astra (xhigh) · Codex | +69.3 | +60.3 | 78 | 117 |
| 13 | Claude Fable 5.1 (xhigh) · Claude Code | +91.7 | +83.1 | 73 | 118 |
| 14 | Qwen3.8 Flash (xhigh) · Codex | +131.7 | +128.8 | 76 | 116 |
| 15 | Grok 4.6 (xhigh-fast) · Cursor | +156.8 | +168.3 | 78 | 119 |

Of 1,920 attempts: **1,851 measured**, 67 analysis errors (30 base or patched files that do not parse as modern PHP, 21 binary/rename-only diffs, 15 patches with non-UTF-8 bytes, 1 file missing at the base commit) and 2 missing patches. Outcomes: 958 pass, 954 fail, 8 unknown (`uncertain` or `infrastructure_failed`, never counted as failures). Missing measurements are never zero. Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md).

## Sources

- Tasks: Hugging Face [`zlab-princeton/SWEeper-Bench` at `0a4c5e2`](https://huggingface.co/datasets/zlab-princeton/SWEeper-Bench/tree/0a4c5e2ec653b11bc0d99497a49635d3a56d3fa9), `data/test.jsonl` SHA-256 `be3ef86a…`.
- Runs: Hugging Face [`zlab-princeton/SWEeper-Bench-traces` at `15e41de`](https://huggingface.co/datasets/zlab-princeton/SWEeper-Bench-traces/tree/15e41de53a1c7bec06898da56c99d88f368ba17f), `runs.csv` rows with `type = main` (15 configurations × 200 tasks; ablations ignored). Every patch matched its `patch_sha256`.
- Licence: traces and tasks CC BY 4.0. Records hold scalars and hashes only; patches are not redistributed.
- Measured at analyzer commit `03d5c59`, Python 3.14.8, `tree-sitter==0.26.0`, `tree-sitter-php==0.25.1`.

## Reproduce

```sh
pip install tree-sitter==0.26.0 tree-sitter-php==0.25.1
REV=15e41de53a1c7bec06898da56c99d88f368ba17f
curl -LO https://huggingface.co/datasets/zlab-princeton/SWEeper-Bench/resolve/0a4c5e2ec653b11bc0d99497a49635d3a56d3fa9/data/test.jsonl
curl -LO https://huggingface.co/datasets/zlab-princeton/SWEeper-Bench-traces/resolve/$REV/runs.csv
python -m parsimony.sweeper dataset test.jsonl --ref-files examples/sweeper-php/reference-files --output population.jsonl
# Download each main run's patch to patches/<run_id>.patch from
#   https://huggingface.co/datasets/zlab-princeton/SWEeper-Bench-traces/resolve/$REV/<run_id>/prediction/patch
python -m parsimony.sweeper --cache .parsimony-cache analyze runs.csv --dataset population.jsonl \
  --patches patches --model gpt-6-astra --harness codex --output sweeper-gpt-6-astra-codex.jsonl
# repeat for each model/harness pair; then, offline:
S=examples/sweeper-php
python -m parsimony.release freeze $S/population.jsonl --name sweeper-php-v1 --output population-manifest.json
python -m parsimony.scoring freeze $S/sweeper-*.jsonl --name sweeper-php-v1 --population $S/population-manifest.json --output score-panel.json
python -m parsimony.release audit $S/population-manifest.json $S/sweeper-*.jsonl --output coverage.json
python -m parsimony.stability $S/score-panel.json $S/sweeper-*.jsonl --output stability.json
```
