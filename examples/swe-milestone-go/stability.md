# Score sensitivity: 10 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `swe-milestone-go-v1`: 30 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (16 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: milestone-claude-code-opus-4.6 ≈ milestone-gemini-cli-gemini-3.1-pro ≈ milestone-claude-code-sonnet-4.6 ≈ milestone-gemini-cli-gemini-3-pro ≈ milestone-claude-code-opus-4.5 ≈ milestone-codex-gpt-5.3-codex ≈ milestone-codex-gpt-5.2 ≈ milestone-codex-gpt-5.2-codex ≈ milestone-gemini-cli-gemini-3-flash ≈ milestone-claude-code-sonnet-4.5 (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under failure cap 0–50.
- **Stable under every variation and statistically separated** (0 of 9 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 9 pairs): milestone-claude-code-opus-4.6 vs milestone-gemini-cli-gemini-3.1-pro, milestone-gemini-cli-gemini-3.1-pro vs milestone-claude-code-sonnet-4.6, milestone-claude-code-sonnet-4.6 vs milestone-gemini-cli-gemini-3-pro, milestone-gemini-cli-gemini-3-pro vs milestone-claude-code-opus-4.5, milestone-claude-code-opus-4.5 vs milestone-codex-gpt-5.3-codex, milestone-codex-gpt-5.3-codex vs milestone-codex-gpt-5.2, milestone-codex-gpt-5.2 vs milestone-codex-gpt-5.2-codex, milestone-codex-gpt-5.2-codex vs milestone-gemini-cli-gemini-3-flash, milestone-gemini-cli-gemini-3-flash vs milestone-claude-code-sonnet-4.5.
- **Midpoint rank never changes under any variation**: milestone-claude-code-opus-4.6 (1), milestone-gemini-cli-gemini-3-flash (9).
- Difficulty strata answer a different question and are not counted as variations; they reverse milestone-gemini-cli-gemini-3.1-pro > milestone-claude-code-sonnet-4.6 (solved by all); milestone-claude-code-sonnet-4.6 > milestone-gemini-cli-gemini-3-pro (solved by fewer); milestone-gemini-cli-gemini-3-pro > milestone-claude-code-opus-4.5 (solved by all); milestone-codex-gpt-5.2-codex > milestone-gemini-cli-gemini-3-flash (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 30 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | milestone-claude-code-opus-4.6 | 21.3 | 2.1–40.3 | 17.1–25.4 | 1–1 | 1.0–7.0 | 0.84 |
| 2 | milestone-gemini-cli-gemini-3.1-pro | 12.4 | -4.2–27.9 | 8.2–16.5 | 2–3 | 1.0–10.0 | 0.07 |
| 3 | milestone-claude-code-sonnet-4.6 | 9.8 | -6.8–25.3 | 5.7–14.0 | 2–5 | 1.0–10.0 | 0.07 |
| 4 | milestone-gemini-cli-gemini-3-pro | 9.2 | -6.8–24.5 | 5.1–13.4 | 3–5 | 1.0–10.0 | 0.01 |
| 5 | milestone-claude-code-opus-4.5 | 7.3 | -8.1–22.4 | 3.2–11.5 | 4–5 | 1.0–10.0 | 0.00 |
| 6 | milestone-codex-gpt-5.3-codex | 2.4 | -12.0–16.6 | -2.1–7.0 | 6–7 | 1.0–10.0 | 0.01 |
| 7 | milestone-codex-gpt-5.2 | 1.0 | -13.3–15.2 | -3.6–5.5 | 6–8 | 1.0–10.0 | 0.00 |
| 8 | milestone-codex-gpt-5.2-codex | -2.4 | -14.8–9.7 | -7.0–2.2 | 6–10 | 1.0–10.0 | 0.00 |
| 9 | milestone-gemini-cli-gemini-3-flash | -4.7 | -15.1–5.1 | -9.3–-0.1 | 9–9 | 2.0–10.0 | 0.00 |
| 10 | milestone-claude-code-sonnet-4.5 | -7.0 | -16.3–2.1 | -11.1–-2.8 | 8–10 | 3.0–10.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| milestone-claude-code-opus-4.6 > milestone-gemini-cli-gemini-3.1-pro | 8.90 | -13.55 to 29.82 | 0.55 | none | yes |
| milestone-gemini-cli-gemini-3.1-pro > milestone-claude-code-sonnet-4.6 | 2.55 | -20.24 to 24.14 | 0.23 | without navidrome/navidrome | no |
| milestone-claude-code-sonnet-4.6 > milestone-gemini-cli-gemini-3-pro | 0.61 | -22.26 to 23.91 | 0.17 | net floor=0, panel without milestone-claude-code-opus-4.6, panel without milestone-codex-gpt-5.3-codex, without zeromicro/go-zero | no |
| milestone-gemini-cli-gemini-3-pro > milestone-claude-code-opus-4.5 | 1.89 | -17.96 to 21.63 | 0.15 | without navidrome/navidrome | no |
| milestone-claude-code-opus-4.5 > milestone-codex-gpt-5.3-codex | 4.89 | -16.76 to 26.04 | 0.28 | none | no |
| milestone-codex-gpt-5.3-codex > milestone-codex-gpt-5.2 | 1.48 | -20.98 to 23.39 | 0.13 | without zeromicro/go-zero | no |
| milestone-codex-gpt-5.2 > milestone-codex-gpt-5.2-codex | 3.35 | -18.00 to 25.39 | 0.21 | without navidrome/navidrome | no |
| milestone-codex-gpt-5.2-codex > milestone-gemini-cli-gemini-3-flash | 2.34 | -16.74 to 20.98 | 0.10 | without zeromicro/go-zero | no |
| milestone-gemini-cli-gemini-3-flash > milestone-claude-code-sonnet-4.5 | 2.24 | -13.65 to 16.80 | 0.03 | without zeromicro/go-zero | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| milestone-claude-code-opus-4.6 | 21.3 (1) | 21.7 (1) | 21.5 (1) | 21.4 (1) | 21.1 (1) | 21.0 (1) | 19.9 (1) | 28.0 (1) | 25.3 (1) | 14.6 (1) |
| milestone-gemini-cli-gemini-3.1-pro | 12.4 (2) | 10.8 (2) | 11.3 (2) | 11.8 (2) | 12.9 (2) | 13.4 (2) | 12.5 (2) | 19.2 (2) | 16.4 (2) | 5.6 (2) |
| milestone-claude-code-sonnet-4.6 | 9.8 (3) | 9.3 (3) | 9.5 (3) | 9.7 (3) | 10.0 (3) | 10.2 (3) | 9.1 (4) | 16.6 (3) | 13.9 (3) | 3.0 (3) |
| milestone-gemini-cli-gemini-3-pro | 9.2 (4) | 9.0 (4) | 9.1 (4) | 9.1 (4) | 9.3 (4) | 9.4 (4) | 9.5 (3) | 16.5 (4) | 13.6 (4) | 2.0 (4) |
| milestone-claude-code-opus-4.5 | 7.3 (5) | 8.3 (5) | 8.0 (5) | 7.7 (5) | 7.0 (5) | 6.7 (5) | 7.7 (5) | 15.3 (5) | 12.1 (5) | -0.6 (5) |
| milestone-codex-gpt-5.3-codex | 2.4 (6) | 2.2 (6) | 2.3 (6) | 2.4 (6) | 2.5 (6) | 2.6 (6) | 2.6 (6) | 11.1 (6) | 7.6 (6) | -6.2 (6) |
| milestone-codex-gpt-5.2 | 1.0 (7) | -0.3 (7) | 0.1 (7) | 0.5 (7) | 1.4 (7) | 1.8 (7) | 1.0 (7) | 10.0 (7) | 6.4 (7) | -8.1 (7) |
| milestone-codex-gpt-5.2-codex | -2.4 (8) | -3.4 (8) | -3.1 (8) | -2.7 (8) | -2.0 (8) | -1.7 (8) | -2.8 (8) | 6.5 (8) | 2.9 (8) | -11.3 (8) |
| milestone-gemini-cli-gemini-3-flash | -4.7 (9) | -5.8 (9) | -5.4 (9) | -5.1 (9) | -4.4 (9) | -4.0 (9) | -3.7 (9) | 3.8 (9) | 0.4 (9) | -13.3 (9) |
| milestone-claude-code-sonnet-4.5 | -7.0 (10) | -7.3 (10) | -7.2 (10) | -7.1 (10) | -6.9 (10) | -6.7 (10) | -6.6 (10) | 2.7 (10) | -1.2 (10) | -16.6 (10) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (0 of 77 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| milestone-claude-code-opus-4.5 | 9 | 10 | none |
| milestone-claude-code-opus-4.6 | 12 | 12 | milestone-claude-code-sonnet-4.6 3→4, milestone-gemini-cli-gemini-3-pro 4→3 |
| milestone-claude-code-sonnet-4.5 | 2 | 10 | none |
| milestone-claude-code-sonnet-4.6 | 11 | 10 | none |
| milestone-codex-gpt-5.2 | 7 | 11 | none |
| milestone-codex-gpt-5.2-codex | 5 | 11 | none |
| milestone-codex-gpt-5.3-codex | 8 | 11 | milestone-claude-code-sonnet-4.6 3→4, milestone-gemini-cli-gemini-3-pro 4→3 |
| milestone-gemini-cli-gemini-3-flash | 4 | 10 | none |
| milestone-gemini-cli-gemini-3-pro | 9 | 10 | none |
| milestone-gemini-cli-gemini-3.1-pro | 10 | 10 | none |
| (dedup panel) | 0 | 0 | none |

Tasks that lose their only reference: milestone-claude-code-opus-4.5: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-claude-code-opus-4.6: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M019`, `go-zero__M023`, `go-zero__M024`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-claude-code-sonnet-4.5: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-claude-code-sonnet-4.6: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-codex-gpt-5.2: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `go-zero__M028`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-codex-gpt-5.2-codex: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `go-zero__M026`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-codex-gpt-5.3-codex: `go-zero__M003`, `go-zero__M005`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-gemini-cli-gemini-3-flash: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-gemini-cli-gemini-3-pro: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`; milestone-gemini-cli-gemini-3.1-pro: `go-zero__M003`, `go-zero__M007.1`, `go-zero__M007.2`, `go-zero__M009`, `go-zero__M010`, `go-zero__M018`, `go-zero__M023`, `go-zero__M025`, `navidrome__milestone_003_sub-01`, `navidrome__milestone_003_sub-02`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| navidrome/navidrome (7) | milestone-gemini-cli-gemini-3.1-pro 2→3, milestone-claude-code-sonnet-4.6 3→2, milestone-gemini-cli-gemini-3-pro 4→5, milestone-claude-code-opus-4.5 5→4, milestone-codex-gpt-5.3-codex 6→7, milestone-codex-gpt-5.2 7→8, milestone-codex-gpt-5.2-codex 8→6 |
| zeromicro/go-zero (23) | milestone-claude-code-sonnet-4.6 3→5, milestone-gemini-cli-gemini-3-pro 4→3, milestone-claude-code-opus-4.5 5→4, milestone-codex-gpt-5.3-codex 6→7, milestone-codex-gpt-5.2 7→6, milestone-codex-gpt-5.2-codex 8→10, milestone-claude-code-sonnet-4.5 10→8 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (30) | Solved by every model (1) | Solved by fewer (29) |
|---|---:|---:|---:|
| milestone-claude-code-opus-4.6 | 21.3 (1) | 77.2 (3) | 19.3 (1) |
| milestone-gemini-cli-gemini-3.1-pro | 12.4 (2) | 66.3 (4) | 10.5 (2) |
| milestone-claude-code-sonnet-4.6 | 9.8 (3) | 82.2 (2) | 7.3 (4) |
| milestone-gemini-cli-gemini-3-pro | 9.2 (4) | 15.8 (9) | 9.0 (3) |
| milestone-claude-code-opus-4.5 | 7.3 (5) | 95.0 (1) | 4.3 (5) |
| milestone-codex-gpt-5.3-codex | 2.4 (6) | 55.5 (5) | 0.6 (6) |
| milestone-codex-gpt-5.2 | 1.0 (7) | 25.8 (8) | 0.1 (7) |
| milestone-codex-gpt-5.2-codex | -2.4 (8) | 6.0 (10) | -2.7 (8) |
| milestone-gemini-cli-gemini-3-flash | -4.7 (9) | 45.6 (6) | -6.5 (9) |
| milestone-claude-code-sonnet-4.5 | -7.0 (10) | 35.6 (7) | -8.4 (10) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **milestone-claude-code-opus-4.6 − milestone-gemini-cli-gemini-3.1-pro = 13.35**: failed/failed -0.10 (4), failed/solved -12.06 (4), solved/failed 17.79 (6), solved/solved 7.72 (6). For milestone-claude-code-opus-4.6: `go-zero__M027` +3.66 (solved/failed), `go-zero__M001` +3.64 (solved/failed), `go-zero__M019` +3.10 (solved/failed). For milestone-gemini-cli-gemini-3.1-pro: `go-zero__M014` -3.78 (failed/solved), `navidrome__milestone_003_sub-03` -3.64 (failed/solved), `go-zero__M021` -2.98 (failed/solved).
- **milestone-gemini-cli-gemini-3.1-pro − milestone-claude-code-sonnet-4.6 = 3.83**: failed/failed -0.04 (6), failed/solved -13.49 (4), solved/failed 9.43 (3), solved/solved 7.92 (7). For milestone-gemini-cli-gemini-3.1-pro: `go-zero__M013` +3.48 (solved/failed), `go-zero__M021` +2.99 (solved/failed), `go-zero__M017` +2.97 (solved/failed). For milestone-claude-code-sonnet-4.6: `go-zero__M008` -4.33 (failed/solved), `go-zero__M020` -4.26 (failed/solved), `go-zero__M004` -3.61 (failed/solved).
- **milestone-claude-code-sonnet-4.6 − milestone-gemini-cli-gemini-3-pro = 0.91**: failed/failed 0.12 (7), failed/solved -8.79 (2), solved/failed 14.58 (4), solved/solved -4.99 (7). For milestone-claude-code-sonnet-4.6: `go-zero__M008` +4.37 (solved/failed), `go-zero__M020` +4.25 (solved/failed), `go-zero__M004` +3.67 (solved/failed). For milestone-gemini-cli-gemini-3-pro: `go-zero__M021` -4.64 (failed/solved), `go-zero__M017` -4.15 (failed/solved), `navidrome__milestone_001` -2.83 (solved/solved).
- **milestone-gemini-cli-gemini-3-pro − milestone-claude-code-opus-4.5 = 2.84**: failed/failed 0.10 (8), failed/solved -5.21 (3), solved/failed 10.24 (3), solved/solved -2.29 (6). For milestone-gemini-cli-gemini-3-pro: `go-zero__M021` +4.81 (solved/failed), `navidrome__milestone_002` +2.97 (solved/failed), `navidrome__milestone_003_sub-03` +2.45 (solved/failed). For milestone-claude-code-opus-4.5: `navidrome__milestone_004` -3.96 (solved/solved), `go-zero__M001` -2.45 (failed/solved), `go-zero__M013` -1.72 (failed/solved).
- **milestone-claude-code-opus-4.5 − milestone-codex-gpt-5.3-codex = 3.66**: failed/failed 0.48 (8), failed/solved -10.45 (3), solved/failed 8.13 (3), solved/solved 5.49 (5). For milestone-claude-code-opus-4.5: `go-zero__M027` +3.86 (solved/failed), `go-zero__M022` +3.39 (solved/solved), `go-zero__M017` +2.39 (solved/failed). For milestone-codex-gpt-5.3-codex: `navidrome__milestone_003_sub-03` -5.19 (failed/solved), `go-zero__M005` -3.28 (failed/solved), `go-zero__M008` -1.98 (failed/solved).
- **milestone-codex-gpt-5.3-codex − milestone-codex-gpt-5.2 = 3.51**: failed/failed 0.29 (7), failed/solved -9.62 (3), solved/failed 15.44 (5), solved/solved -2.59 (3). For milestone-codex-gpt-5.3-codex: `navidrome__milestone_003_sub-03` +5.55 (solved/failed), `go-zero__M005` +3.61 (solved/failed), `go-zero__M020` +3.09 (solved/failed). For milestone-codex-gpt-5.2: `navidrome__milestone_002` -4.66 (failed/solved), `go-zero__M028` -3.23 (failed/solved), `go-zero__M001` -2.20 (solved/solved).
- **milestone-codex-gpt-5.2 − milestone-codex-gpt-5.2-codex = 3.70**: failed/failed -0.64 (9), failed/solved -11.70 (3), solved/failed 14.94 (5), solved/solved 1.10 (1). For milestone-codex-gpt-5.2: `go-zero__M001` +4.71 (solved/failed), `navidrome__milestone_002` +4.64 (solved/failed), `go-zero__M028` +3.20 (solved/failed). For milestone-codex-gpt-5.2-codex: `go-zero__M022` -4.21 (failed/solved), `go-zero__M027` -4.05 (failed/solved), `go-zero__M026` -3.44 (failed/solved).
- **milestone-codex-gpt-5.2-codex − milestone-gemini-cli-gemini-3-flash = 4.09**: failed/failed -0.96 (10), failed/solved -5.39 (3), solved/failed 12.64 (4), solved/solved -2.20 (1). For milestone-codex-gpt-5.2-codex: `go-zero__M027` +4.06 (solved/failed), `go-zero__M022` +3.91 (solved/failed), `go-zero__M026` +3.42 (solved/failed). For milestone-gemini-cli-gemini-3-flash: `go-zero__M013` -2.56 (failed/solved), `navidrome__milestone_004` -2.20 (solved/solved), `navidrome__milestone_002` -2.08 (failed/solved).
- **milestone-gemini-cli-gemini-3-flash − milestone-claude-code-sonnet-4.5 = 3.67**: failed/failed 0.62 (14), failed/solved -2.49 (1), solved/failed 5.02 (3), solved/solved 0.52 (1). For milestone-gemini-cli-gemini-3-flash: `go-zero__M013` +2.36 (solved/failed), `navidrome__milestone_002` +1.95 (solved/failed), `go-zero__M001` +0.71 (solved/failed). For milestone-claude-code-sonnet-4.5: `navidrome__milestone_007` -2.49 (failed/solved), `go-zero__M022` -0.14 (failed/failed), `navidrome__milestone_001` -0.05 (failed/failed).

## Regenerate

```sh
python -m parsimony.stability examples/swe-milestone-go/score-panel.json examples/swe-milestone-go/milestone-claude-code-opus-4.5.jsonl examples/swe-milestone-go/milestone-claude-code-opus-4.6.jsonl examples/swe-milestone-go/milestone-claude-code-sonnet-4.5.jsonl examples/swe-milestone-go/milestone-claude-code-sonnet-4.6.jsonl examples/swe-milestone-go/milestone-codex-gpt-5.2-codex.jsonl examples/swe-milestone-go/milestone-codex-gpt-5.2.jsonl examples/swe-milestone-go/milestone-codex-gpt-5.3-codex.jsonl examples/swe-milestone-go/milestone-gemini-cli-gemini-3.1-pro.jsonl examples/swe-milestone-go/milestone-gemini-cli-gemini-3-flash.jsonl examples/swe-milestone-go/milestone-gemini-cli-gemini-3-pro.jsonl --output examples/swe-milestone-go/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
