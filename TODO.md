# TODO

Development is direct-to-`main`. Keep planned work here and in the detailed [handoff](HANDOFF.md), rather than opening GitHub issues unless explicitly requested. Preserve frozen records; measurement changes require a versioned analyzer and validation.

## Supported tracks and model additions — priority

- [x] **Classify the seven DeepSWE Go analysis errors.** Static investigation completed; evidence and regression tests are linked below.
- [ ] **Implement a versioned Go parser fix and cohort revalidation.** All seven DeepSWE Go errors are now classified with hash-bound static evidence: five Arcane `new(expression)` grammar gaps, one Scriggo grouped-declaration EOF/newline gap, one genuinely invalid Helm after-file. See [investigation](docs/go-parser-investigation.md) and metadata JSON. Choose a corrected pinned grammar or an official Go unit backend before implementing; version eligibility/unit changes and remeasure the full Go cohort in a clean committed checkout. Existing unavailable measurements remain missing, never zero. No acceptance/metric fix has been implemented.
- [ ] **Find usable newer-model exports on existing boards.** Prioritize DeepSWE Python/JS/TS/Go, SWE-bench Verified and Live. Require per-attempt patches, explicit outcomes, frozen task population, usable before-state identity and pinned revisions/checksums; aggregate scores and model labels alone are insufficient. Recheck Astra's absent declared patches and Gemini 3.8's inaccessible patches, and review the changed TianxiCode Live configuration without replacing the published pinned run. See [current discovery](docs/new-model-discovery.md). Availability is an external blocker, not evidence that exports do not exist anywhere. Never launch paid evaluations or contact upstream without approval.

## New language tracks — deferred

Prefer supported-track model additions first. Counts below are discovery leads, not certified releasable populations; recheck source revisions and artifact compatibility before implementation.

- [ ] **Java analyzer and separate board.** Investigate the documented 69 SWE-PolyBench Verified, 160 candidate SWE-bench Live and 43 SWE-bench Multilingual tasks. Select and pin a parser; define coding units, scope exclusions and generated-source/build-file handling; add adversarial/regression tests and a versioned track identity. Audit task-level artifacts and publication rights before release. Never pool raw units with other languages.
- [ ] **Rust analyzer and separate board.** Investigate the documented 5 DeepSWE, 171 candidate SWE-bench Live and 43 SWE-bench Multilingual tasks. Select and pin a parser; explicitly define macro counting and test/bench/example/generated-code scope; add adversarial/regression tests and a versioned track identity. Audit task-level artifacts and publication rights before release. Never pool raw units with other languages.

Details: [language expansion opportunities](docs/language-expansion-opportunities.md).

## Measurement and professional-release follow-up

- [ ] Version strict malformed-patch and duplicate/conflicting-file-section rejection; evaluate historical artifacts before updating published measurements.
- [ ] Define reproducible analyzer resource limits and explicit unavailable outcomes.
- [ ] Complete mobile scatter, screen-reader, contrast/zoom and hosted security-header checks without regressing approved graph behavior.
- [ ] Stress-test near-limit custom imports and define a responsiveness budget.

Evidence, remaining gates and reproduction commands: [repository audit](docs/repository-audit.md), [site audit](docs/site-audit.md).
