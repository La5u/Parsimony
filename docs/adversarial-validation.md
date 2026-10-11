# Adversarial validation of the footprint metric

Roadmap item 2: does the footprint move when it should, and stay still when it should not? Each case below is a test in [`tests/test_adversarial.py`](../tests/test_adversarial.py) with its expected footprint asserted. Original numbers are for analyzer `0.5.1-beta`; the validation/assert-removal and helper-delegation regressions also run against the current analyzer (Python 3.14.7). These are static full-file measurements: target code is never imported or executed. The token columns show the pre-0.5 metric (`net_tokens`, `token_churn`), which every record still carries.

## Results

| Case | Net units | Unit churn | Net tokens | Token churn | Verdict |
|---|---:|---:|---:|---:|---|
| Comments and blank lines | 0 | 0 | 0 | 0 | correct |
| Line wrapping, parentheses, trailing comma | 0 | 0 | 0 | 0 | correct |
| Quote style and implicit string concatenation | 0 | 0 | 0 | 0 | correct |
| Semicolon-joined statements | 0 | 0 | 0 | 0 | correct |
| Tabs instead of spaces | 0 | 0 | 0 | 0 | correct |
| f-string spacing | 0 | 0 | 0 | 0 | correct |
| Docstring added | 0 | 0 | 0 | 0 | correct |
| Same literal value (`255` → `0xff`) | 0 | 0 | 0 | 0 | correct |
| Identifier-only rename (2 occurrences) | 0 | 4 | 0 | 4 | correct: a rename is a real edit |
| Keyword arguments reordered | 0 | 4 | 0 | 8 | counted, though equivalent |
| Guard clause added (reference edit) | 14 | 14 | 18 | 18 | correct |
| Same edit in `tests/`, `docs/`, `setup.py`, config files | 0 | 0 | 0 | 0 | correct: out of scope, and scored as unmeasured |
| Guard clause plus a large test-file edit | 14 | 14 | 18 | 18 | correct: tests neither hide nor inflate |
| Generated-file header added to an edited file | 14 | 14 | 18 | 18 | **fixed in 0.5.1** (was 0) |
| Code added under `sympy/testing/` | 14 | 14 | 18 | 18 | **fixed in 0.5.1** (was excluded) |
| Diff from a backup copy (`x.py.bak` → `x.py`) | — | — | — | — | correct: out of scope, scored as unmeasured |
| Unrelated unused function deleted | −12 | 12 | −19 | 19 | limitation |
| Required implementation validation removed | −14 | 14 | −18 | 18 | limitation: smaller but loses rejection |
| Implementation invariant assert removed | −8 | 8 | −8 | 8 | limitation: smaller but loses a check |
| Inline validation delegated to an existing helper | −10 | 12 | −12 | 14 | smaller local footprint, not a quality verdict |
| Two functions swapped | 0 | 8 | 0 | 8 | limitation |
| General fix vs. hardcoded test input | 12 vs 12 | 14 vs 12 | 17 vs 19 | 19 vs 19 | limitation, worse with units |

## What failed and how it was fixed

**A header comment could hide an edit.** Files were excluded as generated if *either* side had a header such as `# Auto-generated, do not edit`. A patch that added that comment to the file it changed made its whole edit invisible: a 14-unit change measured 0. Since 0.5.1 only the base commit's version decides, and new files are always counted. Genuinely generated files in the repository (header already present) stay excluded.

**Library code under `testing/` was excluded.** Any directory named `testing` was treated as tests. That is right for pytest's top-level `testing/` suite, but `sympy/testing/` and `lib/matplotlib/testing/` ship as library code. Since 0.5.1 only a top-level `testing/` directory is excluded.

Neither fix changes a published measurement: all 5,010 published records (ten models × 500 tasks and the smoke sample) re-measure identically under 0.5.1, so they keep their 0.5.0 label.

## Known limitations

- **Unrelated deletion earns net credit.** The analyzer cannot tell whether deleted code was related to the issue. Deleting an unused function lowers net units by 12. Churn, 20% of the score, still charges for it, and the `net_floor=0` sensitivity variant removes the credit. SWE-bench's tests do not protect untested code.
- **Moved code counts as edits.** Swapping two functions costs 8 units although nothing changed. Moves are rare in bug fixes; a tree-diff with move detection would fix this.
- **Hardcoding a test's input is cheaper than fixing the bug.** The special case costs 12 units, the general fix 14. Tokens happened to tie these on churn and favor the general fix on net; units reverse that because they no longer charge for the literal list's brackets and commas. Size cannot detect this: it needs a separate check comparing new literals and branches with the task's hidden tests.

## Compact does not mean maintainable or correct

Three regression examples use `pkg/core.py`, an in-scope implementation file, with exact base text. None changes scope or measurement rules; all remain measured, not excluded-only. The tests pin both unit and token net/churn.

- **Validation removed:** change `area(width, height)` from rejecting `width < 0 or height < 0` with `raise ValueError(width, height)` to just `return width * height`. This earns −14 net units despite losing the required rejection of negative dimensions.
- **Assert removed:** delete `assert width >= 0 and height >= 0` immediately before that return. This earns −8 net units while removing an implementation invariant check (when assertions are enabled), not test-suite code.
- **Existing helper reused:** keep this helper unchanged in the same implementation file, then replace the inline guard in `area` with `validate_dimensions(width, height)`:

  ```python
  def validate_dimensions(width, height):
      if width < 0 or height < 0:
          raise ValueError(width, height)
  ```

  Delegation earns −10 net units with 12 units of churn. The helper's existing body is not newly delivered code, so it adds no diff footprint; nothing moves into an excluded directory. Churn is not the sum of whole deleted/added statements: sequence alignment retains shared names. This example is ordinary reuse by source inspection, not runtime certification or proof that indirection is more maintainable.

The same net-credit direction covers both lost checks and plausible reuse. A compact patch alone cannot establish correctness, readability, or maintainability. Outcomes and review are separate evidence; these regressions document the metric, not a proposal to penalize deletions, change ranking, or execute target code. The current ranking uses plain mean net units; references above to churn's 20% weight concern the archived Score only.

## Not tested here

Semantic equivalence (for example `not a == b` versus `a != b`), cross-file refactors, and code hidden in excluded directories that implementation files then import. The coverage audit lists every excluded file, so the last case can be reviewed by hand.
