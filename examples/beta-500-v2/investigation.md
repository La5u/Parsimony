# Follow-up investigation: failed-patch errors and zero footprints

**Status: beta forensics, not a new score.** All numbers below describe the frozen `0.3.0-beta` [two-submission audit](README.md). The targeted metric fix is `0.3.1-beta`; old records have **not** been relabeled or silently rescored. Do not publish a new ranking until both 500-task cohorts are reanalyzed on one frozen revision.

## Three failed-patch context errors: stale patches, not whitespace

All three records are **published unresolved**. Fresh downloads matched the recorded patch SHA256s; the diffs use ordinary LF text. Strict hunk application to the Verified base correctly rejects them. For each hunk, the patch's complete **new-side text is already present** in the base file, while the complete old-side text is absent:

| Task / submissions | Base commit / file | Patch SHA256 | Evidence |
|---|---|---|---|
| `django__django-13513`, Opus **and** Sonnet | `6599608c4d0befdcb820ddccce55f183f247ae4f`, `django/views/debug.py` | `49ce43dc56503aa4ea09c520524f01860d4aea512870178f9518a601cf37953c` | Patch expects `return explicit or implicit`; fetched base at lines 400–402 already has the patch's `suppress_context` logic. Hunk claims line 396 while method starts at 397. Base file SHA256 `dc923e3d85aebac6dd350e0a93f733addd42de456bcb1d69f7fff5fcbdb630be`. |
| `sympy__sympy-13031`, Sonnet | `2dfa7457f20ee187fbb09b5b6a1631da4458388c`, `sympy/matrices/common.py` | `7498250dc175486cbc8cd094c5049d419f1fff57b5221bee710c942c9f8f2040` | Both hunk postimages already appear at lines 242–244 and 478–480. Fetched base file SHA256 `18fa44c060e8cee6ad7e1522281afc20fca36c95c283f56e1265c45e0a5e7b5a`; its Git blob ID `7ef51bc847426b1b3adf1a227a1fd4e94dd1c73e` matches the patch's abbreviated **new-side** blob `7ef51bc84`. |

**Decision:** keep these analyses as errors with unknown failed footprints. Do not shift hunk coordinates, apply with fuzz, or infer zero cost from an already-present postimage: that would invent a measurement of what the agent actually submitted against this base. An optional future `already_applied` diagnostic should verify all hunk postimages and remain separate from scored footprints. The repeated identical Django patch is *one distinct patch*, not two independent examples.

## Why measured zero can conceal behavior changes

| Frozen `0.3.0-beta` records | Opus | Sonnet |
|---|---:|---:|
| All successfully analyzed records with zero primary normalized churn | 37 | 27 |
| Zero with at least one touched file | 29 | 26 |
| Zero primary churn **but positive value-sensitive churn** | 27 | 24 |

These are diagnostic counts, **not** evidence of 27/24 incorrect predictions or deliberate gaming. Examples checked directly against cached patches/base files:

- `django__django-13109` replaces `_default_manager` with `_base_manager`. Primary churn **0**, value-sensitive churn **2**, as intended by identifier normalization.
- `pytest-dev__pytest-8399` changes an f-string prefix from `unittest_` to `_unittest_`. Both old metrics were **0**, because `FSTRING_MIDDLE` was also collapsed in value-sensitive mode. After the targeted fix, primary churn remains 0, but value-sensitive churn becomes **2**.
- `sympy__sympy-19637` moves `hit = kern in s` **inside** a `while` block. Both old metrics were **0**, because `INDENT`/`DEDENT` tokens were discarded. Counting canonical block-boundary tokens changes both churn measures to **2** on the same downloaded patch. This is a genuine semantic blind spot in the primary metric, not merely an excluded file.
- Several failed tasks have truly empty patches (SHA256 of zero bytes, `e3b0c442...`). A zero failed-patch footprint is valid **only** when the submitted patch is actually empty; no success credit follows.

`0.3.1-beta` now counts canonical `INDENT`/`DEDENT` block boundaries (not the amount of whitespace) in the primary metric and preserves `FSTRING_MIDDLE` in the secondary value-sensitive diagnostic. Unit tests cover block moves, f-string literal changes and formatting-only indentation. These changes **invalidate comparisons to the published `0.3.0-beta` footprint numbers** even where a particular record might not change. Identifier/literal changes are still deliberately absent from the primary metric; whether they should influence a future official score requires an explicit, preregistered scoring decision.

## Reference-panel independence

On the 335 tasks both agents solved, **91 patches have identical SHA256s**; 13 of the 17 tasks on which both have zero-primary/positive-value footprints have identical patches. They must not be treated as 91 independent examples of model efficiency. A future reference panel should deduplicate identical patches *per task* and publish the panel construction rule before entrants are scored. Different hashes are not proof of genuinely independent solutions.

**Next release gate:** pin a new clean analyzer commit and population manifest, rerun both complete cohorts under `0.3.1-beta`, then audit any zero-primary cases and recheck raw hashes. After an independent reviewer reproduces a preregistered random sample, choose a reference panel and test score sensitivity. Until then, the [v2 medians](README.md) are historical diagnostics, not an official model ranking.
