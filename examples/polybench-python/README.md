# SWE-PolyBench Verified — Python

Website: **[parsimony.lasu.dev/polybench-python.html](https://parsimony.lasu.dev/polybench-python.html)**.

[SWE-PolyBench](https://amazon-science.github.io/SWE-PolyBench/) Verified has 382 issue-fix tasks in Java, JavaScript, TypeScript and Python. This board measures the **113 Python tasks**, one attempt per task, from five public submissions.

**This compares model + agent setups, not models alone:** each model ran in its submitter's own agent. Model names and pass/fail are the submitters' reports (the SWE-PolyBench evaluator's `<id>_result.json` `resolved` flag), not rechecked here.

**Four of the five runs are open, unmerged submission pull requests** to `amazon-science/SWE-PolyBench`, read at their head commits (the owner approved including them). Only HMigBot (Opus 4.8) is merged upstream. Pull requests can still change or be rejected; this board keeps the pinned heads below.

## Disclosures

- **Jitto Build (Opus 5.5)** says in its own README that **129 of its 294 resolved patches (43.9%) are near-verbatim copies of the reference fix** (difflib ratio ≥ 0.8 over changed non-test lines; 13 exact matches), and that its score would be 165/382 if all of them were counted unresolved. It reports no leak of the fixes it could find (no network, history cut to the base commit), but cannot rule out training-data memorisation. Its small footprint ratio partly reflects writing the maintainers' fix.
- **AiWork.Code (Opus 5.5)** withdrew three patches after its own leakage audit (`google__guava-3971`, `google__guava-5696`, `keras-team__keras-19915`): the evaluator had resolved them, but the submitted patch is empty and they count as unresolved. Of these, `keras-team__keras-19915` is in this population and is recorded with `source_disposition: withdrawn_after_leakage_audit`, outcome `no_generation`, no footprint. Two Python tasks never ran (`huggingface__transformers-13989`, `keras-team__keras-19838`, `source_disposition: never_ran`). The submitter also reports that 57 of its 274 resolved instances show direct evidence of recalling the upstream fix (floor 217/382).
- **HMigBot (Opus 4.8)** assembled its run from a 70-task Feature run and a 312-task complementary run, retried 29 empty-patch relay failures and replaced five trajectories after a history-isolation correction (its README).
- **Slingshot (GPT-5.6 Sol)** predictions are labelled `SWE-Bench Agent`; the README and metadata name Sapient Slingshot 3.4.0 on `gpt-5.6-sol`. **Mobile Coder (DeepSeek V4 Flash)** predictions carry no model label; its README names Mobile Coder 1.2.4 with DeepSeek V4 Flash at `max`.
- Not included: iSWE-Agent GPT-5.4 is withheld because its patches carry no usable old-blob identity, so its before-state is unproven ([priority-live](../priority-live/README.md)).

## Population

All 113 Python tasks of `AmazonScience/SWE-PolyBench_Verified` at `b3fca77` (`test.csv` SHA-256 `0c8138e7…`; 382 tasks = Python 113, JavaScript 100, TypeScript 100, Java 69). `population.jsonl` lists task, repository and base commit; `population-manifest.json` freezes it (`swe-polybench-verified-python-v1`). The rule uses only the dataset's language label, never model output or outcomes. Every one of the 113 tasks is kept for every configuration.

## Results (analyzer 0.10.0-beta at `be4df4d`, Python 3.14.7)

As on the website: a model's net units added on the tasks it solved, divided by what the other ranked models added on those same tasks (0.8× = 20% less code). Only tasks solved by at least 3 other models count (*Tasks*); there is no 95% range below 5 tasks. This ranks the smallest measured footprint, not the best coding model. With five configurations each ratio is against only four peers, so ranks are rough.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GPT-5.6 Sol · Slingshot 3.4.0 | 0.65× | 0.56–0.86× | 60 | +37.4 | +39.2 | 56.6% | 64/64 |
| 2 | DeepSeek V4 Flash (max) · Mobile Coder 1.2.4 | 1.01× | 0.78–1.12× | 59 | +38.6 | +31.9 | 70.8% | 80/80 |
| 3 | Claude Opus 4.8 · HMigBot | 1.03× | 0.85–1.17× | 60 | +36.9 | +50.7 | 61.9% | 69/70 |
| 4 | Claude Opus 5.5 (high) · AiWork.Code | 1.12× | 0.89–1.31× | 64 | +39.3 | +38.2 | 70.8% | 80/80 |
| 5 | Claude Opus 5.5 (high) · Jitto Build (Claude Code) | 1.18× | 1.08–1.33× | 67 | +40.9 | +41.8 | 85.8% | 97/97 |

Of 565 attempts: **559 measured** (390 passing, 169 failing upstream), 4 empty patches (AiWork 3, Jitto 1: `no_generation`, never zero), 1 analysis error (HMigBot `huggingface__transformers-29449`, an upstream failure: a patched file does not tokenize) and 1 withheld before-state (HMigBot `langchain-ai__langchain-4646`: the patch context differs from the pinned base file, so the touched-file preimage is unverified; its upstream success is kept, its footprint is not measured). No outcome is unknown and no patch is missing. 8 of 113 tasks have no measured passing patch and are uncalibrated for the archived Score. Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md); ratio diagnostics: [polybench-python.md](../ranking-diagnostics/polybench-python.md).

| Configuration | Measured | Upstream pass / fail / no generation (Python) | Exclusions |
|---|---:|---|---|
| Claude Opus 4.8 · HMigBot | 111/113 | 70 / 43 / 0 | 1 analysis error (a failure), 1 unverified preimage (a success) |
| Claude Opus 5.5 · AiWork.Code | 110/113 | 80 / 30 / 3 | 3 empty (1 withdrawn after leakage audit, 2 never ran) |
| Claude Opus 5.5 · Jitto Build | 112/113 | 97 / 15 / 1 | 1 empty (`huggingface__transformers-13989`, never attempted) |
| GPT-5.6 Sol · Slingshot 3.4.0 | 113/113 | 64 / 49 / 0 | none |
| DeepSeek V4 Flash · Mobile Coder 1.2.4 | 113/113 | 80 / 33 / 0 | none |

## Sources

| Configuration | Source | Pinned commit | `all_preds.jsonl` SHA-256 | Upstream solved (all 382) |
|---|---|---|---|---:|
| Claude Opus 4.8 · HMigBot | `amazon-science/SWE-PolyBench` submission branch (merged) | `e7062f4a848ca7775bc1c1313f7aa419bd6a3ec1` | `fec28ea7…` | 196 |
| Claude Opus 5.5 · AiWork.Code | open [PR 47](https://github.com/amazon-science/SWE-PolyBench/pull/47), `x4vierli/SWE-PolyBench` | `d2b1f885a66387fa8ad5d670aa1d690c41965a4e` | `5daf60df…` | 274 |
| Claude Opus 5.5 · Jitto Build | open [PR 46](https://github.com/amazon-science/SWE-PolyBench/pull/46), `charliefrantowski/SWE-PolyBench` | `30150b6f06d8e2acfdba897fe473726515baff92` | `c91a487f…` | 293 |
| GPT-5.6 Sol · Slingshot 3.4.0 | open [PR 44](https://github.com/amazon-science/SWE-PolyBench/pull/44), `sanjuatps/SWE-PolyBench-S1` | `2c177685c6bf424badb6c3722aaf8c778a178a08` | `6376de77…` | 185 |
| DeepSeek V4 Flash · Mobile Coder 1.2.4 | open [PR 40](https://github.com/amazon-science/SWE-PolyBench/pull/40), `WilliamRocketRen/SWE-PolyBench` | `46905351979ebe9da1d0d82c0fff2871daddaf85` | `ad6ba5ee…` | 241 |

- Each pull request head is a single commit whose only parent is the pinned upstream `e7062f4`; the importer checks this and reads `evaluation/PBVerified/<run>/` (`all_preds.jsonl`, `logs/<id>_result.json` for all 382 tasks, README, metadata and audit files, all hash-bound in each record's provenance).
- Before-state: every nonempty Python patch was checked against the files at the dataset's base commit (old blob hash equals the patch's `index` prefix and every hunk applies strictly; `parsimony.polybench preimages`). 560 of 561 nonempty patches pass; the one failure is withheld. Audits (hashes only): [preimages/](preimages/). This is touched-file evidence, not a certified historical checkout or evaluator input.
- Records hold scalars and hashes only; patches, prompts and trajectories are not redistributed. Redistribution of the raw submissions has not been cleared.
- One analyzer identity for the board: all five configurations measured from a clean detached worktree at `be4df4d` with Python 3.14.7 (the earlier 0.6.0-beta Opus 4.8 measurement in [priority-live](../priority-live/README.md) is superseded here, not pooled).

## Reproduce

```sh
# inventories and preimage audits (network; raw patches stay in external storage)
PYTHONPATH=. python examples/benchmark-discovery/run-polybench-python.py --output-dir ~/pb --phase inventory
PYTHONPATH=. python examples/benchmark-discovery/run-polybench-python.py --output-dir ~/pb --phase audit
# offline measurement from a clean worktree at be4df4d, Python 3.14.7
git worktree add --detach /tmp/pb-analyzer be4df4d
(cd /tmp/pb-analyzer && PYTHONPATH=. python examples/benchmark-discovery/run-polybench-python.py --output-dir ~/pb --phase measure)
cp ~/pb/polybench-*.jsonl ~/pb/population.jsonl examples/polybench-python/
P=examples/polybench-python N=swe-polybench-verified-python-v1
export PYTHONPATH=/tmp/pb-analyzer   # with python -P so the analyzer, not this checkout, is imported
python -P -m parsimony.release freeze $P/population.jsonl --name $N --output $P/population-manifest.json
python -P -m parsimony.scoring freeze $P/polybench-*.jsonl --name $N --population $P/population-manifest.json --output $P/score-panel.json
python -P -m parsimony.release audit $P/population-manifest.json $P/polybench-*.jsonl --output $P/coverage.json
python -P -m parsimony.scoring score $P/score-panel.json $P/polybench-*.jsonl --output $P/scores.json
python -P -m parsimony.stability $P/score-panel.json $P/polybench-*.jsonl --output $P/stability.json
```
