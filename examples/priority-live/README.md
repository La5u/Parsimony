# Recent-model static measurement coverage

Clean measurement checkout: **`de633004011e1b6c8dda81d234baefc024a88b75`**,
Python **3.14.7**, analyzer **0.6.0-beta**. Parser pins and 80/20 scoring rules
were not changed. No target code/tests or new model evaluations were executed.

| Configuration / track | Full population | Eligible success | Eligible failure | Eligible / static analyses |
|---|---:|---:|---:|---:|
| DeepSeek V4.1 Flash / TianxiCode, Live Python | 300 | 202 | 85 | 287 / 295 |
| GPT-5.6 Sol / Slingshot 3.4.0, Live Python | 300 | 205 | 83 | 288 / 296 |
| Claude Opus 4.8 / AiWork.Code, Live Python | 300 | 102 | 174 | 276 / 291 |
| GPT-5.6 Sol / Slingshot 3.4.0, Live JavaScript | 108 | 70 | 15 | 85 / 101 |
| GPT-5.6 Sol / Slingshot 3.4.0, Live TypeScript | 111 | 64 | 34 | 98 / 99 |
| Claude Opus 4.8 / MigBot, PolyBench Python | 113 | 69 | 42 | 111 / 111 |

These are **configuration/task analyses, not unique-task or ranking counts**.
Completed static analyses include all-excluded patches: they are out of scope,
not usable zero-footprint solutions. Eligibility applies the existing scorer's
scope rule; no source measurements or formulas were changed.
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

**Publication follow-up:** the [final Live Python board](../live-python/README.md)
now publishes the three Python configurations' numerical data on all 300 tasks,
using explicit uncalibrated-reference bounds and widened rank uncertainty. No
raw artifacts are released; JS/TS/PolyBench remain outside this website release.
The targeted
[DeepSeek release review](../../docs/deepseek-v4.1-live-release-review.md) recommends
an attributed numerical preview, not raw artifact reuse or certified results.
It freshly corroborates all 300 separate patches/metadata/grader reports and
identifies a concrete scoring gap: only 238/300 tasks have usable passing
references in the current three-configuration Python pool. Do not select that
successful-reference subset as the default population.

Static measurements
are retained in external `/tmp/parsimony-priority-run/*.records.jsonl`; raw
inventories/cache also remain external and are not authorized for redistribution
by Parsimony. No blanket publication/output-reuse licence was established.

The published Python board has a numerical-data-only reporting decision,
explicit mixed-harness/protocol disclosures, independently frozen population,
partial-reference bounds and full-population uncertainty. This does not clear
raw reuse or certify original evaluator inputs. Other tracks still need their
own release review. Live imports intentionally do not publish gold reference code or
claim to verify historical evaluator inputs. AiWork has adaptive effort and
submitted-patch transformations; Slingshot has concrete protocol concerns and
sampled operational provenance. Current pages/rankings remain unchanged.

Reproduce using `examples/benchmark-discovery/run-priority-live.py` from a clean
checkout and external storage, after checking applicable terms. The exact commands
are in the audit document. PolyBench inventory/analysis uses `parsimony.polybench`;
its analyzer is cache-only and does not bypass missing-source errors with zeros.
