# Score sensitivity: 10 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `swe-milestone-python-v1`: 12 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (8 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: milestone-claude-code-opus-4.5 ≈ milestone-claude-code-sonnet-4.6 ≈ milestone-codex-gpt-5.3-codex ≈ milestone-claude-code-opus-4.6 ≈ milestone-codex-gpt-5.2-codex ≈ milestone-gemini-cli-gemini-3-pro ≈ milestone-claude-code-sonnet-4.5 ≈ milestone-gemini-cli-gemini-3-flash ≈ milestone-gemini-cli-gemini-3.1-pro ≈ milestone-codex-gpt-5.2 (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under leave-one-repository-out.
- **Stable under every variation and statistically separated** (0 of 9 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 9 pairs): milestone-claude-code-opus-4.5 vs milestone-claude-code-sonnet-4.6, milestone-claude-code-sonnet-4.6 vs milestone-codex-gpt-5.3-codex, milestone-codex-gpt-5.3-codex vs milestone-claude-code-opus-4.6, milestone-claude-code-opus-4.6 vs milestone-codex-gpt-5.2-codex, milestone-codex-gpt-5.2-codex vs milestone-gemini-cli-gemini-3-pro, milestone-gemini-cli-gemini-3-pro vs milestone-claude-code-sonnet-4.5, milestone-claude-code-sonnet-4.5 vs milestone-gemini-cli-gemini-3-flash, milestone-gemini-cli-gemini-3-flash vs milestone-gemini-cli-gemini-3.1-pro, milestone-gemini-cli-gemini-3.1-pro vs milestone-codex-gpt-5.2.
- **Midpoint rank never changes under any variation**: milestone-claude-code-opus-4.5 (1), milestone-gemini-cli-gemini-3-pro (6), milestone-claude-code-sonnet-4.5 (7), milestone-codex-gpt-5.2 (10).
- Difficulty strata answer a different question and are not counted as variations; they reverse milestone-claude-code-sonnet-4.6 > milestone-codex-gpt-5.3-codex (solved by all); milestone-codex-gpt-5.3-codex > milestone-claude-code-opus-4.6 (solved by fewer); milestone-claude-code-opus-4.6 > milestone-codex-gpt-5.2-codex (solved by all); milestone-codex-gpt-5.2-codex > milestone-gemini-cli-gemini-3-pro (solved by all); milestone-claude-code-sonnet-4.5 > milestone-gemini-cli-gemini-3-flash (solved by all); milestone-gemini-cli-gemini-3-flash > milestone-gemini-cli-gemini-3.1-pro (solved by fewer); milestone-gemini-cli-gemini-3.1-pro > milestone-codex-gpt-5.2 (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 12 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | milestone-claude-code-opus-4.5 | 25.4 | -2.8–51.1 | 21.2–29.6 | 1–1 | 1.0–10.0 | 0.47 |
| 2 | milestone-claude-code-sonnet-4.6 | 18.0 | -6.5–38.2 | 13.9–22.2 | 2–5 | 1.0–10.0 | 0.07 |
| 3 | milestone-codex-gpt-5.3-codex | 17.9 | -9.3–44.6 | 13.7–22.1 | 2–5 | 1.0–10.0 | 0.09 |
| 4 | milestone-claude-code-opus-4.6 | 17.6 | -7.2–41.0 | 13.4–21.7 | 2–5 | 1.0–10.0 | 0.06 |
| 5 | milestone-codex-gpt-5.2-codex | 17.6 | -7.4–41.8 | 13.4–21.7 | 2–5 | 1.0–10.0 | 0.14 |
| 6 | milestone-gemini-cli-gemini-3-pro | 15.3 | -11.7–43.0 | 11.2–19.5 | 6–6 | 1.0–10.0 | 0.15 |
| 7 | milestone-claude-code-sonnet-4.5 | 11.2 | -12.8–34.4 | 7.1–15.4 | 7–7 | 1.0–10.0 | 0.02 |
| 8 | milestone-gemini-cli-gemini-3-flash | 8.8 | -12.9–29.2 | 4.6–13.0 | 8–9 | 1.0–10.0 | 0.00 |
| 9 | milestone-gemini-cli-gemini-3.1-pro | 7.8 | -13.1–26.6 | 3.6–11.9 | 8–9 | 1.0–10.0 | 0.00 |
| 10 | milestone-codex-gpt-5.2 | 1.2 | -14.8–15.5 | -2.9–5.4 | 10–10 | 2.0–10.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| milestone-claude-code-opus-4.5 > milestone-claude-code-sonnet-4.6 | 7.36 | -25.09 to 37.49 | 0.47 | none | no |
| milestone-claude-code-sonnet-4.6 > milestone-codex-gpt-5.3-codex | 0.14 | -27.36 to 28.14 | 0.21 | net weight=0.9, net weight=1, failure cap=0, failure cap=10, panel without milestone-codex-gpt-5.2, panel without milestone-codex-gpt-5.2-codex, panel without milestone-gemini-cli-gemini-3-flash, panel without milestone-gemini-cli-gemini-3.1-pro | no |
| milestone-codex-gpt-5.3-codex > milestone-claude-code-opus-4.6 | 0.33 | -32.24 to 33.60 | 0.28 | net weight=0.5, net weight=0.6, failure cap=50, panel without milestone-claude-code-opus-4.5, panel without milestone-codex-gpt-5.3-codex, panel without milestone-gemini-cli-gemini-3-flash, panel without milestone-gemini-cli-gemini-3-pro | no |
| milestone-claude-code-opus-4.6 > milestone-codex-gpt-5.2-codex | 0.00 | -38.76 to 37.85 | 0.29 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10, panel without milestone-claude-code-opus-4.5, panel without milestone-claude-code-opus-4.6, panel without milestone-claude-code-sonnet-4.6, panel without milestone-codex-gpt-5.2, panel without milestone-codex-gpt-5.2-codex | no |
| milestone-codex-gpt-5.2-codex > milestone-gemini-cli-gemini-3-pro | 2.25 | -29.76 to 30.81 | 0.30 | none | no |
| milestone-gemini-cli-gemini-3-pro > milestone-claude-code-sonnet-4.5 | 4.08 | -28.81 to 38.30 | 0.37 | none | no |
| milestone-claude-code-sonnet-4.5 > milestone-gemini-cli-gemini-3-flash | 2.45 | -23.99 to 28.60 | 0.26 | none | no |
| milestone-gemini-cli-gemini-3-flash > milestone-gemini-cli-gemini-3.1-pro | 1.02 | -27.51 to 30.11 | 0.26 | failure cap=50, panel without milestone-claude-code-opus-4.6 | no |
| milestone-gemini-cli-gemini-3.1-pro > milestone-codex-gpt-5.2 | 6.52 | -18.72 to 30.05 | 0.39 | none | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| milestone-claude-code-opus-4.5 | 25.4 (1) | 25.7 (1) | 25.6 (1) | 25.5 (1) | 25.3 (1) | 25.2 (1) | 25.4 (1) | 31.6 (1) | 29.1 (1) | 19.3 (1) |
| milestone-claude-code-sonnet-4.6 | 18.0 (2) | 18.2 (2) | 18.2 (2) | 18.1 (2) | 18.0 (3) | 17.9 (3) | 18.0 (2) | 24.1 (4) | 21.7 (3) | 12.0 (2) |
| milestone-codex-gpt-5.3-codex | 17.9 (3) | 17.2 (5) | 17.4 (5) | 17.7 (3) | 18.1 (2) | 18.4 (2) | 17.9 (3) | 24.9 (2) | 22.1 (2) | 10.9 (4) |
| milestone-claude-code-opus-4.6 | 17.6 (4) | 17.4 (4) | 17.5 (4) | 17.5 (4) | 17.6 (4) | 17.7 (4) | 17.6 (4) | 23.3 (5) | 21.0 (5) | 11.9 (3) |
| milestone-codex-gpt-5.2-codex | 17.6 (5) | 17.4 (3) | 17.5 (3) | 17.5 (5) | 17.6 (5) | 17.7 (5) | 17.6 (5) | 24.3 (3) | 21.6 (4) | 10.8 (5) |
| milestone-gemini-cli-gemini-3-pro | 15.3 (6) | 15.1 (6) | 15.2 (6) | 15.2 (6) | 15.4 (6) | 15.5 (6) | 15.3 (6) | 22.9 (6) | 19.9 (6) | 7.7 (6) |
| milestone-claude-code-sonnet-4.5 | 11.2 (7) | 11.9 (7) | 11.7 (7) | 11.5 (7) | 11.0 (7) | 10.8 (7) | 11.2 (7) | 19.1 (7) | 16.0 (7) | 3.4 (7) |
| milestone-gemini-cli-gemini-3-flash | 8.8 (8) | 8.1 (8) | 8.3 (8) | 8.6 (8) | 9.0 (8) | 9.3 (8) | 8.8 (8) | 16.8 (8) | 13.6 (8) | 0.8 (9) |
| milestone-gemini-cli-gemini-3.1-pro | 7.8 (9) | 7.2 (9) | 7.4 (9) | 7.6 (9) | 8.0 (9) | 8.2 (9) | 7.8 (9) | 14.5 (9) | 11.8 (9) | 1.0 (8) |
| milestone-codex-gpt-5.2 | 1.2 (10) | 1.2 (10) | 1.2 (10) | 1.2 (10) | 1.3 (10) | 1.3 (10) | 1.2 (10) | 8.9 (10) | 5.8 (10) | -6.4 (10) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (0 of 50 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| milestone-claude-code-opus-4.5 | 6 | 4 | milestone-claude-code-sonnet-4.6 2→3, milestone-codex-gpt-5.3-codex 3→5, milestone-codex-gpt-5.2-codex 5→2 |
| milestone-claude-code-opus-4.6 | 6 | 4 | milestone-claude-code-opus-4.6 4→5, milestone-codex-gpt-5.2-codex 5→4, milestone-gemini-cli-gemini-3-flash 8→9, milestone-gemini-cli-gemini-3.1-pro 9→8 |
| milestone-claude-code-sonnet-4.5 | 4 | 4 | none |
| milestone-claude-code-sonnet-4.6 | 6 | 4 | milestone-claude-code-opus-4.6 4→5, milestone-codex-gpt-5.2-codex 5→4 |
| milestone-codex-gpt-5.2 | 5 | 4 | milestone-claude-code-sonnet-4.6 2→4, milestone-claude-code-opus-4.6 4→5, milestone-codex-gpt-5.2-codex 5→2 |
| milestone-codex-gpt-5.2-codex | 5 | 5 | milestone-claude-code-sonnet-4.6 2→3, milestone-codex-gpt-5.3-codex 3→2, milestone-claude-code-opus-4.6 4→5, milestone-codex-gpt-5.2-codex 5→4 |
| milestone-codex-gpt-5.3-codex | 5 | 4 | milestone-codex-gpt-5.3-codex 3→4, milestone-claude-code-opus-4.6 4→3 |
| milestone-gemini-cli-gemini-3-flash | 4 | 4 | milestone-claude-code-sonnet-4.6 2→5, milestone-claude-code-opus-4.6 4→2, milestone-codex-gpt-5.2-codex 5→4 |
| milestone-gemini-cli-gemini-3-pro | 4 | 4 | milestone-codex-gpt-5.3-codex 3→5, milestone-claude-code-opus-4.6 4→3, milestone-codex-gpt-5.2-codex 5→4 |
| milestone-gemini-cli-gemini-3.1-pro | 5 | 4 | milestone-claude-code-sonnet-4.6 2→5, milestone-codex-gpt-5.3-codex 3→2, milestone-claude-code-opus-4.6 4→3, milestone-codex-gpt-5.2-codex 5→4 |
| (dedup panel) | 0 | 0 | none |

Tasks that lose their only reference: milestone-claude-code-opus-4.5: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-claude-code-opus-4.6: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-claude-code-sonnet-4.5: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-claude-code-sonnet-4.6: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-codex-gpt-5.2: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-codex-gpt-5.2-codex: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`, `scikit-learn__M13`; milestone-codex-gpt-5.3-codex: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-gemini-cli-gemini-3-flash: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-gemini-cli-gemini-3-pro: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`; milestone-gemini-cli-gemini-3.1-pro: `scikit-learn__M12.1`, `scikit-learn__M12.2`, `scikit-learn__M12.4`, `scikit-learn__M12.5`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| scikit-learn/scikit-learn (12) | no tasks left |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (12) | Solved by every model (1) | Solved by fewer (11) |
|---|---:|---:|---:|
| milestone-claude-code-opus-4.5 | 25.4 (1) | 45.6 (6) | 23.6 (1) |
| milestone-claude-code-sonnet-4.6 | 18.0 (2) | 25.8 (8) | 17.3 (3) |
| milestone-codex-gpt-5.3-codex | 17.9 (3) | 68.3 (3) | 13.3 (4) |
| milestone-claude-code-opus-4.6 | 17.6 (4) | 15.8 (9) | 17.7 (2) |
| milestone-codex-gpt-5.2-codex | 17.6 (5) | 85.1 (2) | 11.4 (5) |
| milestone-gemini-cli-gemini-3-pro | 15.3 (6) | 95.0 (1) | 8.1 (6) |
| milestone-claude-code-sonnet-4.5 | 11.2 (7) | 59.4 (5) | 6.9 (8) |
| milestone-gemini-cli-gemini-3-flash | 8.8 (8) | 68.3 (4) | 3.4 (9) |
| milestone-gemini-cli-gemini-3.1-pro | 7.8 (9) | 6.0 (10) | 7.9 (7) |
| milestone-codex-gpt-5.2 | 1.2 (10) | 35.6 (7) | -1.9 (10) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **milestone-claude-code-opus-4.5 − milestone-claude-code-sonnet-4.6 = 11.03**: failed/failed 0.02 (1), failed/solved -10.31 (1), solved/failed 11.80 (1), solved/solved 9.53 (5). For milestone-claude-code-opus-4.5: `scikit-learn__M12.3` +11.80 (solved/failed), `scikit-learn__M11` +6.19 (solved/solved), `scikit-learn__M17` +3.89 (solved/solved). For milestone-claude-code-sonnet-4.6: `scikit-learn__M06` -10.31 (failed/solved), `scikit-learn__M01` -4.40 (solved/solved), `scikit-learn__M13` +0.02 (failed/failed).
- **milestone-claude-code-sonnet-4.6 − milestone-codex-gpt-5.3-codex = 0.21**: failed/solved -3.55 (1), solved/failed 13.75 (2), solved/solved -10.00 (4). For milestone-claude-code-sonnet-4.6: `scikit-learn__M06` +10.21 (solved/failed), `scikit-learn__M04` +4.40 (solved/solved), `scikit-learn__M11` +3.54 (solved/failed). For milestone-codex-gpt-5.3-codex: `scikit-learn__M03` -5.32 (solved/solved), `scikit-learn__M17` -4.95 (solved/solved), `scikit-learn__M01` -4.12 (solved/solved).
- **milestone-codex-gpt-5.3-codex − milestone-claude-code-opus-4.6 = 0.50**: failed/failed 0.03 (1), failed/solved -14.99 (2), solved/failed 2.96 (1), solved/solved 12.49 (4). For milestone-codex-gpt-5.3-codex: `scikit-learn__M01` +11.00 (solved/solved), `scikit-learn__M03` +6.56 (solved/solved), `scikit-learn__M17` +3.18 (solved/solved). For milestone-claude-code-opus-4.6: `scikit-learn__M11` -9.73 (failed/solved), `scikit-learn__M04` -8.25 (solved/solved), `scikit-learn__M06` -5.26 (failed/solved).
- **milestone-claude-code-opus-4.6 − milestone-codex-gpt-5.2-codex = 0.01**: failed/solved -14.91 (2), solved/failed 27.90 (3), solved/solved -12.98 (3). For milestone-claude-code-opus-4.6: `scikit-learn__M04` +12.93 (solved/failed), `scikit-learn__M11` +9.73 (solved/failed), `scikit-learn__M17` +5.30 (solved/solved). For milestone-codex-gpt-5.2-codex: `scikit-learn__M01` -9.62 (solved/solved), `scikit-learn__M03` -8.66 (solved/solved), `scikit-learn__M13` -7.82 (failed/solved).
- **milestone-codex-gpt-5.2-codex − milestone-gemini-cli-gemini-3-pro = 3.38**: failed/solved -15.97 (2), solved/failed 19.21 (3), solved/solved 0.14 (2). For milestone-codex-gpt-5.2-codex: `scikit-learn__M13` +7.74 (solved/failed), `scikit-learn__M12.3` +7.05 (solved/failed), `scikit-learn__M17` +4.41 (solved/failed). For milestone-gemini-cli-gemini-3-pro: `scikit-learn__M06` -12.66 (failed/solved), `scikit-learn__M04` -3.31 (failed/solved), `scikit-learn__M03` -1.24 (solved/solved).
- **milestone-gemini-cli-gemini-3-pro − milestone-claude-code-sonnet-4.5 = 6.12**: failed/failed 0.13 (3), failed/solved -9.73 (1), solved/failed 12.91 (1), solved/solved 2.80 (3). For milestone-gemini-cli-gemini-3-pro: `scikit-learn__M06` +12.91 (solved/failed), `scikit-learn__M01` +6.05 (solved/solved), `scikit-learn__M03` +4.45 (solved/solved). For milestone-claude-code-sonnet-4.5: `scikit-learn__M11` -9.73 (failed/solved), `scikit-learn__M04` -7.70 (solved/solved), `scikit-learn__M17` -0.51 (failed/failed).
- **milestone-claude-code-sonnet-4.5 − milestone-gemini-cli-gemini-3-flash = 3.68**: failed/failed 0.41 (3), failed/solved -7.96 (1), solved/failed 9.73 (1), solved/solved 1.50 (3). For milestone-claude-code-sonnet-4.5: `scikit-learn__M11` +9.73 (solved/failed), `scikit-learn__M04` +4.26 (solved/solved), `scikit-learn__M17` +0.55 (failed/failed). For milestone-gemini-cli-gemini-3-flash: `scikit-learn__M06` -7.96 (failed/solved), `scikit-learn__M01` -1.65 (solved/solved), `scikit-learn__M03` -1.11 (solved/solved).
- **milestone-gemini-cli-gemini-3-flash − milestone-gemini-cli-gemini-3.1-pro = 1.53**: failed/failed -0.32 (2), failed/solved -12.42 (2), solved/failed 7.85 (1), solved/solved 6.42 (3). For milestone-gemini-cli-gemini-3-flash: `scikit-learn__M06` +7.85 (solved/failed), `scikit-learn__M03` +7.80 (solved/solved), `scikit-learn__M13` +0.06 (failed/failed). For milestone-gemini-cli-gemini-3.1-pro: `scikit-learn__M11` -9.73 (failed/solved), `scikit-learn__M17` -2.69 (failed/solved), `scikit-learn__M01` -1.38 (solved/solved).
- **milestone-gemini-cli-gemini-3.1-pro − milestone-codex-gpt-5.2 = 9.78**: failed/failed 1.42 (2), failed/solved -2.90 (1), solved/failed 7.51 (1), solved/solved 3.75 (4). For milestone-gemini-cli-gemini-3.1-pro: `scikit-learn__M01` +7.51 (solved/failed), `scikit-learn__M11` +6.19 (solved/solved), `scikit-learn__M04` +4.81 (solved/solved). For milestone-codex-gpt-5.2: `scikit-learn__M03` -3.71 (solved/solved), `scikit-learn__M17` -3.54 (solved/solved), `scikit-learn__M06` -2.90 (failed/solved).

## Regenerate

```sh
python -m parsimony.stability examples/swe-milestone-python/score-panel.json examples/swe-milestone-python/milestone-claude-code-opus-4.5.jsonl examples/swe-milestone-python/milestone-claude-code-opus-4.6.jsonl examples/swe-milestone-python/milestone-claude-code-sonnet-4.5.jsonl examples/swe-milestone-python/milestone-claude-code-sonnet-4.6.jsonl examples/swe-milestone-python/milestone-codex-gpt-5.2-codex.jsonl examples/swe-milestone-python/milestone-codex-gpt-5.2.jsonl examples/swe-milestone-python/milestone-codex-gpt-5.3-codex.jsonl examples/swe-milestone-python/milestone-gemini-cli-gemini-3.1-pro.jsonl examples/swe-milestone-python/milestone-gemini-cli-gemini-3-flash.jsonl examples/swe-milestone-python/milestone-gemini-cli-gemini-3-pro.jsonl --output examples/swe-milestone-python/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
