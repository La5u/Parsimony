# Score sensitivity: 10 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `swe-milestone-typescript-v1`: 18 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (11 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: milestone-claude-code-sonnet-4.6 ≈ milestone-claude-code-opus-4.6 ≈ milestone-gemini-cli-gemini-3.1-pro ≈ milestone-gemini-cli-gemini-3-pro ≈ milestone-gemini-cli-gemini-3-flash ≈ milestone-codex-gpt-5.3-codex ≈ milestone-claude-code-opus-4.5 ≈ milestone-claude-code-sonnet-4.5 ≈ milestone-codex-gpt-5.2 ≈ milestone-codex-gpt-5.2-codex (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under leave-one-repository-out.
- **Stable under every variation and statistically separated** (0 of 9 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 9 pairs): milestone-claude-code-sonnet-4.6 vs milestone-claude-code-opus-4.6, milestone-claude-code-opus-4.6 vs milestone-gemini-cli-gemini-3.1-pro, milestone-gemini-cli-gemini-3.1-pro vs milestone-gemini-cli-gemini-3-pro, milestone-gemini-cli-gemini-3-pro vs milestone-gemini-cli-gemini-3-flash, milestone-gemini-cli-gemini-3-flash vs milestone-codex-gpt-5.3-codex, milestone-codex-gpt-5.3-codex vs milestone-claude-code-opus-4.5, milestone-claude-code-opus-4.5 vs milestone-claude-code-sonnet-4.5, milestone-claude-code-sonnet-4.5 vs milestone-codex-gpt-5.2, milestone-codex-gpt-5.2 vs milestone-codex-gpt-5.2-codex.
- **Midpoint rank never changes under any variation**: milestone-claude-code-sonnet-4.6 (1), milestone-claude-code-opus-4.6 (2), milestone-gemini-cli-gemini-3.1-pro (3), milestone-codex-gpt-5.3-codex (6), milestone-codex-gpt-5.2 (9), milestone-codex-gpt-5.2-codex (10).
- Difficulty strata answer a different question and are not counted as variations; they reverse milestone-claude-code-sonnet-4.6 > milestone-claude-code-opus-4.6 (solved by all); milestone-claude-code-opus-4.6 > milestone-gemini-cli-gemini-3.1-pro (solved by all); milestone-gemini-cli-gemini-3-pro > milestone-gemini-cli-gemini-3-flash (solved by all); milestone-gemini-cli-gemini-3-flash > milestone-codex-gpt-5.3-codex (solved by fewer); milestone-codex-gpt-5.3-codex > milestone-claude-code-opus-4.5 (solved by all); milestone-claude-code-opus-4.5 > milestone-claude-code-sonnet-4.5 (solved by all); milestone-codex-gpt-5.2 > milestone-codex-gpt-5.2-codex (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 18 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | milestone-claude-code-sonnet-4.6 | 41.4 | 15.8–60.6 | 37.9–44.9 | 1–1 | 1.0–5.0 | 0.73 |
| 2 | milestone-claude-code-opus-4.6 | 36.1 | 10.6–56.4 | 32.6–39.5 | 2–2 | 1.0–7.0 | 0.25 |
| 3 | milestone-gemini-cli-gemini-3.1-pro | 22.0 | -1.6–43.7 | 18.5–25.4 | 3–3 | 1.0–10.0 | 0.02 |
| 4 | milestone-gemini-cli-gemini-3-pro | 17.0 | -4.0–35.5 | 13.5–20.5 | 4–5 | 1.0–10.0 | 0.00 |
| 5 | milestone-gemini-cli-gemini-3-flash | 16.1 | -6.5–38.9 | 9.8–22.3 | 4–5 | 1.0–10.0 | 0.00 |
| 6 | milestone-codex-gpt-5.3-codex | 12.8 | -4.5–27.1 | 8.7–17.0 | 6–6 | 2.0–10.0 | 0.00 |
| 7 | milestone-claude-code-opus-4.5 | 10.7 | -5.7–26.1 | 7.3–14.2 | 7–8 | 2.0–10.0 | 0.00 |
| 8 | milestone-claude-code-sonnet-4.5 | 9.9 | -8.5–27.5 | 6.4–13.4 | 7–8 | 3.0–10.0 | 0.00 |
| 9 | milestone-codex-gpt-5.2 | 4.0 | -12.1–21.3 | 0.6–7.5 | 9–9 | 3.0–10.0 | 0.00 |
| 10 | milestone-codex-gpt-5.2-codex | 0.7 | -15.6–18.9 | -2.8–4.1 | 10–10 | 3.0–10.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| milestone-claude-code-sonnet-4.6 > milestone-claude-code-opus-4.6 | 5.35 | -18.41 to 28.52 | 0.42 | none | no |
| milestone-claude-code-opus-4.6 > milestone-gemini-cli-gemini-3.1-pro | 14.09 | -14.17 to 40.44 | 0.72 | none | yes |
| milestone-gemini-cli-gemini-3.1-pro > milestone-gemini-cli-gemini-3-pro | 4.97 | -22.33 to 33.13 | 0.42 | none | no |
| milestone-gemini-cli-gemini-3-pro > milestone-gemini-cli-gemini-3-flash | 0.94 | -26.25 to 30.22 | 0.16 | net weight=0.5, net weight=0.6, net floor=0 | no |
| milestone-gemini-cli-gemini-3-flash > milestone-codex-gpt-5.3-codex | 3.22 | -25.07 to 30.03 | 0.22 | none | no |
| milestone-codex-gpt-5.3-codex > milestone-claude-code-opus-4.5 | 2.10 | -19.31 to 21.57 | 0.21 | none | no |
| milestone-claude-code-opus-4.5 > milestone-claude-code-sonnet-4.5 | 0.82 | -20.01 to 22.32 | 0.20 | failure cap=0, panel without milestone-codex-gpt-5.3-codex | no |
| milestone-claude-code-sonnet-4.5 > milestone-codex-gpt-5.2 | 5.88 | -19.65 to 29.97 | 0.44 | none | no |
| milestone-codex-gpt-5.2 > milestone-codex-gpt-5.2-codex | 3.37 | -22.32 to 28.21 | 0.34 | none | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| milestone-claude-code-sonnet-4.6 | 41.4 (1) | 42.1 (1) | 41.9 (1) | 41.6 (1) | 41.2 (1) | 40.9 (1) | 39.7 (1) | 44.9 (1) | 43.5 (1) | 37.9 (1) |
| milestone-claude-code-opus-4.6 | 36.1 (2) | 39.6 (2) | 38.4 (2) | 37.2 (2) | 34.9 (2) | 33.7 (2) | 37.7 (2) | 39.7 (2) | 38.2 (2) | 32.4 (2) |
| milestone-gemini-cli-gemini-3.1-pro | 22.0 (3) | 20.1 (3) | 20.7 (3) | 21.3 (3) | 22.6 (3) | 23.2 (3) | 22.0 (3) | 27.7 (3) | 25.4 (3) | 16.2 (3) |
| milestone-gemini-cli-gemini-3-pro | 17.0 (4) | 14.5 (5) | 15.4 (5) | 16.2 (4) | 17.8 (4) | 18.6 (4) | 15.3 (5) | 23.2 (4) | 20.7 (4) | 10.8 (4) |
| milestone-gemini-cli-gemini-3-flash | 16.1 (5) | 15.1 (4) | 15.4 (4) | 15.7 (5) | 16.4 (5) | 16.7 (5) | 16.1 (4) | 22.3 (5) | 19.8 (5) | 9.8 (5) |
| milestone-codex-gpt-5.3-codex | 12.8 (6) | 11.8 (6) | 12.2 (6) | 12.5 (6) | 13.2 (6) | 13.5 (6) | 13.9 (6) | 17.1 (6) | 15.4 (6) | 8.5 (6) |
| milestone-claude-code-opus-4.5 | 10.7 (7) | 11.0 (7) | 10.9 (7) | 10.8 (7) | 10.6 (7) | 10.6 (7) | 10.7 (7) | 16.4 (8) | 14.2 (7) | 5.0 (7) |
| milestone-claude-code-sonnet-4.5 | 9.9 (8) | 9.5 (8) | 9.6 (8) | 9.8 (8) | 10.1 (8) | 10.2 (8) | 9.9 (8) | 16.5 (7) | 13.9 (8) | 3.3 (8) |
| milestone-codex-gpt-5.2 | 4.0 (9) | 3.5 (9) | 3.7 (9) | 3.9 (9) | 4.2 (9) | 4.4 (9) | 4.6 (9) | 12.4 (9) | 9.1 (9) | -4.3 (9) |
| milestone-codex-gpt-5.2-codex | 0.7 (10) | 0.3 (10) | 0.4 (10) | 0.5 (10) | 0.8 (10) | 0.9 (10) | 0.7 (10) | 9.8 (10) | 6.2 (10) | -8.5 (10) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (0 of 81 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| milestone-claude-code-opus-4.5 | 8 | 5 | none |
| milestone-claude-code-opus-4.6 | 12 | 5 | none |
| milestone-claude-code-sonnet-4.5 | 6 | 5 | none |
| milestone-claude-code-sonnet-4.6 | 13 | 5 | none |
| milestone-codex-gpt-5.2 | 6 | 5 | none |
| milestone-codex-gpt-5.2-codex | 3 | 5 | none |
| milestone-codex-gpt-5.3-codex | 11 | 5 | milestone-claude-code-opus-4.5 7→8, milestone-claude-code-sonnet-4.5 8→7 |
| milestone-gemini-cli-gemini-3-flash | 6 | 5 | none |
| milestone-gemini-cli-gemini-3-pro | 8 | 5 | none |
| milestone-gemini-cli-gemini-3.1-pro | 8 | 5 | none |
| (dedup panel) | 0 | 0 | none |

Tasks that lose their only reference: milestone-claude-code-opus-4.5: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-claude-code-opus-4.6: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-claude-code-sonnet-4.5: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-claude-code-sonnet-4.6: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-codex-gpt-5.2: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-codex-gpt-5.2-codex: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-codex-gpt-5.3-codex: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-gemini-cli-gemini-3-flash: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-gemini-cli-gemini-3-pro: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`; milestone-gemini-cli-gemini-3.1-pro: `element-web__maintenance_ui_ux`, `element-web__milestone_seed_3f47487_1`, `element-web__milestone_seed_aa99601_1`, `element-web__milestone_seed_e662c19_1`, `element-web__milestone_seed_fba5938_1`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| element-hq/element-web (18) | no tasks left |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (18) | Solved by every model (1) | Solved by fewer (17) |
|---|---:|---:|---:|
| milestone-claude-code-sonnet-4.6 | 41.4 (1) | 6.0 (10) | 43.5 (1) |
| milestone-claude-code-opus-4.6 | 36.1 (2) | 65.4 (4) | 34.3 (2) |
| milestone-gemini-cli-gemini-3.1-pro | 22.0 (3) | 75.2 (3) | 18.8 (3) |
| milestone-gemini-cli-gemini-3-pro | 17.0 (4) | 35.6 (7) | 15.9 (4) |
| milestone-gemini-cli-gemini-3-flash | 16.1 (5) | 85.1 (2) | 12.0 (6) |
| milestone-codex-gpt-5.3-codex | 12.8 (6) | 15.8 (9) | 12.7 (5) |
| milestone-claude-code-opus-4.5 | 10.7 (7) | 45.6 (6) | 8.7 (7) |
| milestone-claude-code-sonnet-4.5 | 9.9 (8) | 55.5 (5) | 7.2 (8) |
| milestone-codex-gpt-5.2 | 4.0 (9) | 25.8 (8) | 2.8 (9) |
| milestone-codex-gpt-5.2-codex | 0.7 (10) | 95.0 (1) | -4.9 (10) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **milestone-claude-code-sonnet-4.6 − milestone-claude-code-opus-4.6 = 7.40**: solved/failed 5.98 (1), solved/solved 1.43 (12). For milestone-claude-code-sonnet-4.6: `element-web__milestone_seed_599112e_1` +5.98 (solved/failed), `element-web__milestone_seed_05df321_1` +4.76 (solved/solved), `element-web__feature_enhancements` +3.43 (solved/solved). For milestone-claude-code-opus-4.6: `element-web__milestone_seed_e9a3625_1_sub-01` -4.57 (solved/solved), `element-web__milestone_seed_56c7fc1_1` -3.38 (solved/solved), `element-web__milestone_seed_e9a3625_1_sub-03` -2.54 (solved/solved).
- **milestone-claude-code-opus-4.6 − milestone-gemini-cli-gemini-3.1-pro = 19.51**: solved/failed 20.06 (4), solved/solved -0.55 (8). For milestone-claude-code-opus-4.6: `element-web__milestone_seed_e9a3625_1_sub-03` +7.32 (solved/failed), `element-web__milestone_seed_be3778b_1` +6.97 (solved/failed), `element-web__milestone_seed_8bb4d44_1` +6.09 (solved/solved). For milestone-gemini-cli-gemini-3.1-pro: `element-web__milestone_seed_e9a3625_1_sub-02` -5.18 (solved/solved), `element-web__feature_enhancements` -4.19 (solved/solved), `element-web__milestone_seed_05df321_1` -2.09 (solved/solved).
- **milestone-gemini-cli-gemini-3.1-pro − milestone-gemini-cli-gemini-3-pro = 6.88**: failed/failed 0.12 (3), failed/solved -9.82 (2), solved/failed 15.39 (2), solved/solved 1.20 (6). For milestone-gemini-cli-gemini-3.1-pro: `element-web__feature_enhancements` +7.72 (solved/failed), `element-web__milestone_seed_e9a3625_1_sub-02` +7.67 (solved/failed), `element-web__milestone_seed_e9a3625_1_sub-01` +3.05 (solved/solved). For milestone-gemini-cli-gemini-3-pro: `element-web__milestone_seed_f59af37_1` -6.17 (failed/solved), `element-web__milestone_seed_7ff1fd2_1` -3.65 (failed/solved), `element-web__milestone_seed_8bb4d44_1` -2.41 (solved/solved).
- **milestone-gemini-cli-gemini-3-pro − milestone-gemini-cli-gemini-3-flash = -0.76**: failed/failed 0.08 (3), failed/solved -11.22 (2), solved/failed 15.20 (3), solved/solved -4.81 (4). For milestone-gemini-cli-gemini-3-pro: `element-web__milestone_seed_f59af37_1` +6.69 (solved/failed), `element-web__milestone_seed_8bb4d44_1` +4.58 (solved/failed), `element-web__milestone_seed_56c7fc1_1` +4.03 (solved/solved). For milestone-gemini-cli-gemini-3-flash: `element-web__milestone_seed_be3778b_1` -5.95 (failed/solved), `element-web__feature_enhancements` -5.27 (failed/solved), `element-web__milestone_seed_e9a3625_1_sub-01` -4.12 (solved/solved).
- **milestone-gemini-cli-gemini-3-flash − milestone-codex-gpt-5.3-codex = 5.82**: failed/failed 0.01 (1), failed/solved -17.46 (4), solved/solved 23.28 (6). For milestone-gemini-cli-gemini-3-flash: `element-web__milestone_seed_e9a3625_1_sub-01` +6.30 (solved/solved), `element-web__milestone_seed_3762d40_1` +4.63 (solved/solved), `element-web__milestone_seed_be3778b_1` +4.20 (solved/solved). For milestone-codex-gpt-5.3-codex: `element-web__milestone_seed_7ff1fd2_1` -6.98 (failed/solved), `element-web__milestone_seed_e9a3625_1_sub-02` -5.30 (failed/solved), `element-web__milestone_seed_e9a3625_1_sub-03` -2.62 (failed/solved).
- **milestone-codex-gpt-5.3-codex − milestone-claude-code-opus-4.5 = 6.06**: solved/failed 10.23 (4), solved/solved -4.17 (7). For milestone-codex-gpt-5.3-codex: `element-web__milestone_seed_7ff1fd2_1` +4.13 (solved/solved), `element-web__milestone_seed_05df321_1` +3.61 (solved/solved), `element-web__milestone_seed_3762d40_1` +2.76 (solved/failed). For milestone-claude-code-opus-4.5: `element-web__maintenance_bug_fixes` -2.83 (solved/solved), `element-web__feature_enhancements` -2.48 (solved/solved), `element-web__milestone_seed_be3778b_1` -2.48 (solved/solved).
- **milestone-claude-code-opus-4.5 − milestone-claude-code-sonnet-4.5 = 1.13**: failed/failed -0.20 (4), failed/solved -3.23 (1), solved/failed 11.86 (3), solved/solved -7.30 (5). For milestone-claude-code-opus-4.5: `element-web__milestone_seed_e9a3625_1_sub-02` +5.92 (solved/failed), `element-web__maintenance_bug_fixes` +3.76 (solved/failed), `element-web__milestone_seed_7ff1fd2_1` +2.17 (solved/failed). For milestone-claude-code-sonnet-4.5: `element-web__milestone_seed_8bb4d44_1` -3.68 (solved/solved), `element-web__milestone_seed_56c7fc1_1` -3.23 (failed/solved), `element-web__feature_enhancements` -2.28 (solved/solved).
- **milestone-claude-code-sonnet-4.5 − milestone-codex-gpt-5.2 = 8.14**: failed/failed 1.27 (4), failed/solved -12.07 (3), solved/failed 16.04 (3), solved/solved 2.91 (3). For milestone-claude-code-sonnet-4.5: `element-web__feature_enhancements` +6.85 (solved/failed), `element-web__milestone_seed_8bb4d44_1` +6.43 (solved/failed), `element-web__milestone_seed_be3778b_1` +2.76 (solved/failed). For milestone-codex-gpt-5.2: `element-web__milestone_seed_7ff1fd2_1` -8.01 (failed/solved), `element-web__milestone_seed_f59af37_1` -2.68 (failed/solved), `element-web__milestone_seed_3762d40_1` -1.38 (failed/solved).
- **milestone-codex-gpt-5.2 − milestone-codex-gpt-5.2-codex = 4.67**: failed/failed -0.99 (6), failed/solved -1.70 (1), solved/failed 17.77 (4), solved/solved -10.41 (2). For milestone-codex-gpt-5.2: `element-web__milestone_seed_7ff1fd2_1` +8.02 (solved/failed), `element-web__milestone_seed_05df321_1` +5.36 (solved/failed), `element-web__milestone_seed_f59af37_1` +2.76 (solved/failed). For milestone-codex-gpt-5.2-codex: `element-web__milestone_seed_e9a3625_1_sub-01` -5.33 (solved/solved), `element-web__milestone_seed_56c7fc1_1` -5.08 (solved/solved), `element-web__feature_enhancements` -1.70 (failed/solved).

## Regenerate

```sh
python -m parsimony.stability examples/swe-milestone-typescript/score-panel.json examples/swe-milestone-typescript/milestone-claude-code-opus-4.5.jsonl examples/swe-milestone-typescript/milestone-claude-code-opus-4.6.jsonl examples/swe-milestone-typescript/milestone-claude-code-sonnet-4.5.jsonl examples/swe-milestone-typescript/milestone-claude-code-sonnet-4.6.jsonl examples/swe-milestone-typescript/milestone-codex-gpt-5.2-codex.jsonl examples/swe-milestone-typescript/milestone-codex-gpt-5.2.jsonl examples/swe-milestone-typescript/milestone-codex-gpt-5.3-codex.jsonl examples/swe-milestone-typescript/milestone-gemini-cli-gemini-3.1-pro.jsonl examples/swe-milestone-typescript/milestone-gemini-cli-gemini-3-flash.jsonl examples/swe-milestone-typescript/milestone-gemini-cli-gemini-3-pro.jsonl --output examples/swe-milestone-typescript/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
