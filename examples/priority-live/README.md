# Recent-model static measurement coverage

Clean measurement checkout: **`de633004011e1b6c8dda81d234baefc024a88b75`**,
Python **3.14.7**, analyzer **0.6.0-beta**. Parser pins and 80/20 scoring rules
were not changed. No target code/tests or new model evaluations were executed.

| Configuration / track | Full population | Measured success | Measured failure | All measured |
|---|---:|---:|---:|---:|
| DeepSeek V4.1 Flash / TianxiCode, Live Python | 300 | 204 | 91 | 295 |
| GPT-5.6 Sol / Slingshot 3.4.0, Live Python | 300 | 208 | 88 | 296 |
| Claude Opus 4.8 / AiWork.Code, Live Python | 300 | 102 | 189 | 291 |
| GPT-5.6 Sol / Slingshot 3.4.0, Live JavaScript | 108 | 77 | 24 | 101 |
| GPT-5.6 Sol / Slingshot 3.4.0, Live TypeScript | 111 | 65 | 34 | 99 |
| Claude Opus 4.8 / MigBot, PolyBench Python | 113 | 69 | 42 | 111 |

These are **configuration/task measurements, not unique-task or ranking counts**.
Every full population remains in its external JSONL, including unmeasured items.
Missing measurement does not erase upstream correctness or become zero footprint.
The JSON summary records complete status/outcome counts and hashes of the external
measurement records. Python/JS/TS and Live/PolyBench must never be pooled.

The five `*.preimages.json` files contain metadata/hashes only, not source code,
patches, prompts or trajectories. They bind Live dataset/result/prediction checksums
and independently fetched old-file bytes. Their `base_commit_confirmations` are
**touched-file compatibility approvals**, not full operational-checkout evidence.
See [the full audit](../../docs/priority-live-static-import.md) and
[the broader source/protocol/terms report](../../docs/priority-live-provenance.md).

## Coverage exceptions

- Live Python: five DeepSeek and four GPT preimage exceptions; one Opus preimage
  exception plus seven grader errors and one empty-only item.
- Live JS: four strict-parser rejections and three upstream grader errors.
- Live TS: ten strict-parser rejections, one preimage exception and one grader error.
  Parser recovery is not accepted; rejection does not prove an upstream outcome false.
- PolyBench Opus Python: a transformers tokenization error and a langchain strict
  hunk mismatch remain unmeasured. Its metadata remains `declared-candidate`, not
  a historically certified dataset/evaluator match.
- PolyBench GPT-5.4: **112 generated Python patches of 113 tasks**. All 112 strictly
  match candidate-base hunks, but contain no usable old-blob identity prefixes.
  Without independent operational/full-before-source evidence, measurements are
  withheld. The other task is unsubmitted/unknown, not automatically failed.
  The full source inventory distinguishes 1,998 outside-prediction placeholders
  from the 112 submitted predictions; they are not 1,998 failed model attempts.

## Release status and next steps

**No new ranking board or per-task footprint release yet.** Static measurements
are retained in external `/tmp/parsimony-priority-run/*.records.jsonl`; raw
inventories/cache also remain external and are not authorized for redistribution
by Parsimony. No blanket publication/output-reuse licence was established.

A board still needs an intended-use rights decision, explicit mixed-harness and
protocol disclosures, passing-reference/population review, and full-population
uncertainty. Live imports intentionally do not publish gold reference code or
claim to verify historical evaluator inputs. AiWork has adaptive effort and
submitted-patch transformations; Slingshot has concrete protocol concerns and
sampled operational provenance. Current pages/rankings remain unchanged.

Reproduce using `examples/benchmark-discovery/run-priority-live.py` from a clean
checkout and external storage, after checking applicable terms. The exact commands
are in the audit document. PolyBench inventory/analysis uses `parsimony.polybench`;
its analyzer is cache-only and does not bypass missing-source errors with zeros.
