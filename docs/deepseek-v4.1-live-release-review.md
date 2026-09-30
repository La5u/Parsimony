# DeepSeek V4.1 Flash: targeted release review

Review date: **2026-09-30**. Scope: public TianxiCode 0.1.423 / source-declared
DeepSeek V4.1 Flash, SWE-bench Live Lite **Python, all 300 tasks**.

Publication follow-up: [the final Live Python board](../examples/live-python/README.md)
now retains all 300 tasks with explicit uncalibrated-task bounds and conservative
rank uncertainty. It publishes numerical data only, not raw artifacts. The review
below records the findings before that bounded-score implementation; missing
references are **not** retroactively claimed to exist.

## Decision

**Recommend a clearly labelled numerical research preview, not a certified or
ranked full-population release yet.** Raw patches, source, prompts, trajectories
and training corpora remain **not cleared for redistribution/reuse**.

The earlier blanket “rights/protocol review pending” explanation was too vague.
Numerical reporting and redistributing generated code are different intended
uses. This review finds no express numerical-benchmark reporting prohibition in
the inspected public documents. That is not a licence from Tianxi, clearance of
all third-party rights, or a legal opinion. A preview may report attributed
factual outcomes, static numerical measurements and integrity metadata, without
copying output/source expression or implying endorsement.

**The concrete ranking blocker is reference coverage:** the three already
analyzed Live Python configurations supply usable passing references for only
**238/300 tasks**. The current scorer requires one for every panel task. Do not
silently freeze the 238-task successful-reference subset, fabricate references,
or assign the remaining 62 tasks zero contributions. Acquire compatible,
source-reported passing references; alternatively design and review explicit
uncalibrated-task bounds before publishing a full-population score range.
Neither action authorizes changing the 80% net / 20% churn formula.

## Fresh source checks

Pinned submission: `cba8a6d3197cd53da09f8527cccbc689782302a6`.
Run: `submissions/lite/tianxicode/deepseek-flash`.

Independently fetched **900 immutable source files**: every task's separate
`patch.diff`, `meta.json`, and grader `report.json`. All **300/300** pass:

- Separate patch bytes exactly equal the imported prediction, without repairing
  newlines or editing artifacts.
- Metadata task ID, declared repository/base, routing alias
  `tianxi-agent-plan/deepseek-flash`, and CLI version `0.1.423` match.
- Grader task IDs and explicit boolean outcomes agree with the imported
  **204 successful / 96 failed** result population.

This checks source consistency, not independent correctness or provider-signed
model identity. Metadata bases remain **declarations**, not operational checkout
proof. The previous full preimage audit corroborates complete candidate-base
old-file bytes against patch Git blob prefixes and strict hunks for 295 patches.
A blob prefix is not a full cryptographic identification of the historical object.
The original historical HF input manifest and image digests remain unverified.

[Machine-readable evidence](../examples/priority-live/deepseek-publication-evidence.json)
contains URLs, byte lengths, SHA-256 hashes and check results only. It binds the
archived clean-checkout measurement digest and retains all 300 IDs. Reproduce:

```sh
PYTHONPATH="$PWD" python examples/benchmark-discovery/review-deepseek-live.py \
  --external-dir /tmp/parsimony-priority-run \
  --output /tmp/parsimony-priority-run/deepseek-publication-evidence.json
```

Raw downloads remain external; no target code/tests or paid evaluation is run.

## Important coverage correction

**295 completed static analyses is not 295 footprint-eligible solutions.**
Eight patches touch only files excluded by the existing Python scope. The scorer
already treats these as unmeasured/out-of-scope, not zero-footprint fixes.

| State | Successful | Failed | Total |
|---|---:|---:|---:|
| Full upstream population | 204 | 96 | 300 |
| In-scope, complete static footprint | 202 | 85 | **287** |
| Entire patch out of Python implementation scope | 2 | 6 | 8 |
| Strict patch/preimage rejection | 0 | 5 | 5 |

Thus footprint eligibility is **287/300 (95.7%)**; the published resolve rate
remains **204/300 (68%)**, not 202/287. All 13 footprint-ineligible records retain
their original outcomes and denominator positions. Successful and failed
in-scope footprints must both contribute to any eventual default ranking.

The five privacyIDEA patches include SQLite test-data artifacts and fail the
strict patch parser. Do not infer that their Python implementation edits are
necessarily malformed, or repair/remove binary/test artifacts to force acceptance.
The eight fully excluded task IDs and all 62 missing-reference IDs are preserved
in the evidence. Existing analyzer rules/measurements/scoring are unchanged.
The same static-analysis versus eligibility distinction has been corrected in
the other cohort summaries; their rights/protocol decisions are **not** approved
by this DeepSeek-only review.

## Protocol assessment

Read the pinned root submission rules, run README, environment description and
complete driver log. They describe one problem-only, task-agnostic framed rollout
per task in a Docker task image, with model-endpoint-only networking.

The driver records six rollout waves and grading timeouts/retries. Gold grading
occurs after each wave's rollout; final gold collection is not evidence that all
300 gold patches passed. Preserve grading retries rather than counting them as
extra model attempts. All available final per-task boolean reports agree with
the aggregate. This supports **source-reported** outcome use.

No independent firewall/image audit or complete causality audit establishes that
future Git objects, grading information or other forbidden data were inaccessible.
The run's protocol claims must stay unverified, not silently certified. This is
not evidence that all patches cheated or that the reported outcomes are false.
Do not transfer AiWork/Slingshot-specific concerns to Tianxi without evidence.
Compare configurations as **model + agent**, never controlled model-only results.

## Terms / intended-use assessment

Both official DeepSeek pages were successfully retrieved and read in full in this
review, superseding the earlier DNS failure for this narrow provider-term check:

| Document | Displayed date | Bytes | SHA-256 |
|---|---|---:|---|
| [Terms of Use](https://cdn.deepseek.com/policies/en-US/deepseek-terms-of-use.html) | Updated March 27, 2026 | 39,095 | `e5c52c238ff59a6d274cd66c449f939ba6bd3183fe7927397b595df02887a76d` |
| [Open Platform Terms](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html) | Released April 22; effective April 29, 2026 | 33,904 | `2b433c53cbac75491959025eba5a27908f9f1886352dce0a05f3d5a936d87790` |

- Both section **4.2** assign any output rights to the relevant service user,
  subject to law/terms, and expressly describe research and other uses. The
  general terms exclude assignment of other users' outputs. **This is not an
  assignment or sublicence to Parsimony**, nor proof Tianxi's routing contract
  used these terms or this exact provider deployment.
- General terms **3.1 / 5** require accuracy checks and AI-origin disclosure when
  disseminating outputs; API **8.1** also requires AI-origin disclosure. Attribute
  outcomes to the public submitter and describe code as AI-generated. Do not
  assert independent correctness, model authenticity or benchmark endorsement.
- General **6.2**, API **5.2–5.4** discuss brand use and misleading affiliations.
  Any preview should use plain factual model/agent attribution, not co-branded
  logos or “official/certified/endorsed” language.
- The run README preserves the archive for analysis/reproduction; it supplies no
  blanket downstream output licence. The submission tree's lack of a LICENSE
  is **not proof of a prohibition on publishing independently computed numerical
  facts**, but leaves raw artifact distribution without an established grant.
- Dataset/harness MIT declarations do not relicense underlying target code.
  Target-source rights and any private routing/customer agreement remain distinct.
  Scalar/hash reporting is not distribution of modified target software; do not
  use this decision to distribute patches or waive applicable obligations.

**Allowed recommendation:** attributed numerical/hash research reporting with
full-population coverage and explicit uncertainty. **Not cleared:** raw expression,
training/distillation corpora, provider/submitter-contract compliance claims,
certified correctness/protocol claims, or a 300-task ranked score without valid
reference coverage. No upstream contact, consent request or legal clearance was
fabricated.
