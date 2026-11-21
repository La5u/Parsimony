# SWE-bench Multilingual

Boards: [Go](../multilingual-go/README.md) · [JavaScript](../multilingual-javascript/README.md) · [TypeScript](../multilingual-typescript/README.md) · [PHP](../multilingual-php/README.md).

**Tasks.** [SWE-bench Multilingual](https://huggingface.co/datasets/SWE-bench/SWE-bench_Multilingual) at `846e647b` (300 tasks, 41 repositories). Each repository goes to one track by the language its reference fixes change most: Go 42 tasks, JavaScript 28, TypeScript 15, PHP 43. Rust (43), Java (43), C/C++ (42) and Ruby (44) tasks are left out: there is no published board for them (Rust) or no measurement track. `babel__babel-13928` has Flow syntax in `.js` files and is not measurable.

**Runs.** Seventeen setups, one attempt each:
- 14 mini-SWE-agent runs published by SWE-bench (`SWE-bench/experiments` at `40f164d5`, `evaluation/multilingual/`). Pass/fail is from their `per_instance_details.json`. Patches are `logs/<task>/patch.diff` in the `swe-bench-submissions` S3 bucket. Gemini 3.5 Flash keeps its logs in its own repository (pinned at `8dcca985`). Where `patch.diff` is not published (all of GLM-5, some tasks of others), the patch is `info.submission` from the run's trajectory in the same bucket.
- 3 Rusta 1.0.0 + Devscriptor 1.0.4 runs at effort max (DeepSeek V4.1 Flash, GLM-5.3, Kimi K2.8 Preview), from the release [`swe-bench-multilingual`](https://github.com/vladimirpesic/devscriptor-web/releases/tag/swe-bench-multilingual) (tarball sha256 `3adc3cbe…`). Pass/fail is Rusta's own evaluation (`results.json`), not rechecked. Oracle scan of their 900 trajectories: no access to future fixes ([audit](../benchmark-discovery/oracle-audit-rusta-multilingual-2026-11-21.json)).

**Reproduce** (analyzer commit `3cadbda`, Python 3.14.8, `pip install -e '.[languages]' pyarrow`):

```sh
python -m parsimony.multilingual dataset test-00000-of-00001.parquet --language $lang --output dataset.jsonl
python -m parsimony.multilingual analyze ENTRY --dataset dataset.jsonl --output ENTRY.jsonl   # rusta-*: add --rusta-dir DIR --rusta-tarball TGZ
python -m parsimony.release freeze dataset.jsonl --name swe-bench-multilingual-$lang-N --analyzer-commit COMMIT --output population.json
python -m parsimony.scoring freeze *.jsonl --name swe-bench-multilingual-$lang-17 --population population.json --output score-panel.json
python -m parsimony.release audit population.json *.jsonl --dataset dataset.jsonl --output coverage.json
python -m parsimony.scoring score score-panel.json *.jsonl --output scores.json
python -m parsimony.stability score-panel.json *.jsonl --output stability.json --report stability.md
```
