# Score sensitivity: 11 models × 500 tasks

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `ten-model-439-solved-80-20-v0.5`: 439 tasks, point estimates on the 421 tasks where every model has a point score.

**Verdict.** Read the ranking as tiers, not positions: Claude Opus 4.5 > Claude Opus 4.6 ≈ MiniMax M2.5 > Kimi K2.5 ≈ Gemini 3 Flash ≈ GLM-5 ≈ Claude Sonnet 4.5 > Claude Haiku 4.5 > DeepSeek V3.2 ≈ GPT-5.2 ≈ GPT-5 mini (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under net weight 0.5–1.0 and the net floor or failure cap 0–50.
- **Stable under every variation and statistically separated** (4 of 10 adjacent pairs): Claude Opus 4.5 > Claude Opus 4.6, MiniMax M2.5 > Kimi K2.5, Claude Sonnet 4.5 > Claude Haiku 4.5, Claude Haiku 4.5 > DeepSeek V3.2.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 6 pairs): Claude Opus 4.6 vs MiniMax M2.5, Kimi K2.5 vs Gemini 3 Flash, Gemini 3 Flash vs GLM-5, GLM-5 vs Claude Sonnet 4.5, DeepSeek V3.2 vs GPT-5.2, GPT-5.2 vs GPT-5 mini.
- **Rank never changes under any variation**: Claude Opus 4.5 (1), Kimi K2.5 (4), Claude Sonnet 4.5 (7), Claude Haiku 4.5 (8), DeepSeek V3.2 (9).
- Difficulty strata answer a different question and are not counted as variations; they reverse Claude Opus 4.6 > MiniMax M2.5 (solved by fewer); MiniMax M2.5 > Kimi K2.5 (solved by all); Kimi K2.5 > Gemini 3 Flash (solved by fewer); Gemini 3 Flash > GLM-5 (solved by all); Claude Sonnet 4.5 > Claude Haiku 4.5 (solved by all); Claude Haiku 4.5 > DeepSeek V3.2 (solved by fewer); GPT-5.2 > GPT-5 mini (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap on the common tasks (2000 draws, seed 42). Bounds are over all 439 tasks, treating unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Opus 4.5 | 52.8 | 50.0–55.8 | 52.3 | 1–1 | 1–1 | 0.99 |
| 2 | Claude Opus 4.6 | 49.0 | 46.0–51.7 | 49.1 | 2–3 | 2–3 | 0.01 |
| 3 | MiniMax M2.5 | 48.2 | 45.6–50.9 | 47.8–48.0 | 2–3 | 2–4 | 0.00 |
| 4 | Kimi K2.5 | 44.9 | 41.9–47.9 | 44.4–44.5 | 4–4 | 3–6 | 0.00 |
| 5 | Gemini 3 Flash | 43.9 | 41.2–46.7 | 44.1 | 5–6 | 4–6 | 0.00 |
| 6 | GLM-5 | 42.7 | 39.9–45.5 | 42.4 | 5–6 | 4–7 | 0.00 |
| 7 | Claude Sonnet 4.5 | 39.8 | 37.1–42.8 | 39.2–39.3 | 7–7 | 6–7 | 0.00 |
| 8 | Claude Haiku 4.5 | 36.0 | 33.0–39.0 | 35.4 | 8–8 | 8–8 | 0.00 |
| 9 | DeepSeek V3.2 | 30.7 | 27.8–33.8 | 30.0–30.2 | 9–9 | 9–10 | 0.00 |
| 10 | GPT-5.2 | 28.9 | 26.3–31.8 | 28.7 | 10–11 | 9–11 | 0.00 |
| 11 | GPT-5 mini | 26.7 | 23.7–30.0 | 25.2–25.8 | 10–11 | 10–11 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Opus 4.5 > Claude Opus 4.6 | 3.78 | 0.86 to 6.82 | 0.99 | none | yes |
| Claude Opus 4.6 > MiniMax M2.5 | 0.75 | -2.51 to 3.89 | 0.66 | panel without Claude Opus 4.6, without pydata/xarray | yes |
| MiniMax M2.5 > Kimi K2.5 | 3.37 | 0.34 to 6.44 | 0.98 | none | yes |
| Kimi K2.5 > Gemini 3 Flash | 0.96 | -2.92 to 4.68 | 0.69 | none | yes |
| Gemini 3 Flash > GLM-5 | 1.23 | -2.34 to 4.76 | 0.75 | without sympy/sympy | yes |
| GLM-5 > Claude Sonnet 4.5 | 2.87 | -0.45 to 6.05 | 0.95 | none | yes |
| Claude Sonnet 4.5 > Claude Haiku 4.5 | 3.83 | 0.84 to 6.99 | 0.99 | none | yes |
| Claude Haiku 4.5 > DeepSeek V3.2 | 5.33 | 1.95 to 8.73 | 1.00 | none | yes |
| DeepSeek V3.2 > GPT-5.2 | 1.73 | -1.94 to 5.16 | 0.82 | none | yes |
| GPT-5.2 > GPT-5 mini | 2.22 | -1.41 to 5.79 | 0.88 | without django/django | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.5 | 52.8 (1) | 52.6 (1) | 52.7 (1) | 52.7 (1) | 52.8 (1) | 52.9 (1) | 52.7 (1) | 53.8 (1) | 53.4 (1) | 51.7 (1) |
| Claude Opus 4.6 | 49.0 (2) | 49.1 (2) | 49.0 (2) | 49.0 (2) | 49.0 (2) | 48.9 (2) | 49.0 (2) | 50.1 (2) | 49.7 (2) | 47.9 (2) |
| MiniMax M2.5 | 48.2 (3) | 48.6 (3) | 48.5 (3) | 48.4 (3) | 48.1 (3) | 48.0 (3) | 48.2 (3) | 49.3 (3) | 48.9 (3) | 47.2 (3) |
| Kimi K2.5 | 44.9 (4) | 45.0 (4) | 45.0 (4) | 44.9 (4) | 44.8 (4) | 44.8 (4) | 44.8 (4) | 46.6 (4) | 45.9 (4) | 43.2 (4) |
| Gemini 3 Flash | 43.9 (5) | 42.9 (5) | 43.3 (5) | 43.6 (5) | 44.2 (5) | 44.6 (5) | 43.6 (5) | 45.3 (5) | 44.8 (5) | 42.5 (5) |
| GLM-5 | 42.7 (6) | 42.8 (6) | 42.7 (6) | 42.7 (6) | 42.7 (6) | 42.6 (6) | 42.8 (6) | 44.2 (6) | 43.6 (6) | 41.2 (6) |
| Claude Sonnet 4.5 | 39.8 (7) | 39.9 (7) | 39.9 (7) | 39.8 (7) | 39.8 (7) | 39.8 (7) | 40.1 (7) | 41.7 (7) | 41.0 (7) | 37.9 (7) |
| Claude Haiku 4.5 | 36.0 (8) | 36.6 (8) | 36.4 (8) | 36.2 (8) | 35.8 (8) | 35.6 (8) | 36.2 (8) | 38.8 (8) | 37.7 (8) | 33.2 (8) |
| DeepSeek V3.2 | 30.7 (9) | 30.1 (9) | 30.3 (9) | 30.5 (9) | 30.8 (9) | 31.0 (9) | 30.7 (9) | 33.2 (9) | 32.2 (9) | 28.1 (9) |
| GPT-5.2 | 28.9 (10) | 28.0 (10) | 28.3 (10) | 28.6 (10) | 29.3 (10) | 29.6 (10) | 28.7 (10) | 31.2 (10) | 30.3 (10) | 26.7 (10) |
| GPT-5 mini | 26.7 (11) | 26.9 (11) | 26.8 (11) | 26.8 (11) | 26.7 (11) | 26.6 (11) | 26.6 (11) | 29.8 (11) | 28.6 (11) | 23.6 (11) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks whose only reference was that model's patch leave the panel. The dedup panel counts byte-identical patches once per task (921 of 3539 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Haiku 4.5 | 333 | 0 | none |
| Claude Sonnet 4.5 | 357 | 1 | none |
| Claude Opus 4.6 | 378 | 7 | Claude Opus 4.6 2→3, MiniMax M2.5 3→2 |
| DeepSeek V3.2 | 350 | 3 | none |
| Gemini 3 Flash | 379 | 4 | none |
| GLM-5 | 364 | 4 | none |
| GPT-5.2 | 364 | 2 | none |
| GPT-5 mini | 281 | 1 | none |
| Kimi K2.5 | 354 | 1 | none |
| MiniMax M2.5 | 379 | 4 | none |
| (dedup panel) | 921 | 0 | none |

Tasks that lose their only reference: Claude Sonnet 4.5: `astropy__astropy-14369`; Claude Opus 4.6: `django__django-10097`, `django__django-11790`, `django__django-12273`, `pylint-dev__pylint-6528`, `pylint-dev__pylint-7277`, `scikit-learn__scikit-learn-14087`, `sympy__sympy-17318`; DeepSeek V3.2: `django__django-14792`, `scikit-learn__scikit-learn-26194`, `sympy__sympy-13974`; Gemini 3 Flash: `django__django-11141`, `django__django-11400`, `django__django-16256`, `pylint-dev__pylint-4970`; GLM-5: `astropy__astropy-13977`, `django__django-13344`, `psf__requests-6028`, `sympy__sympy-17630`; GPT-5.2: `pylint-dev__pylint-8898`, `pytest-dev__pytest-5787`; GPT-5 mini: `django__django-12308`; Kimi K2.5: `matplotlib__matplotlib-20676`; MiniMax M2.5: `django__django-15695`, `mwaskom__seaborn-3187`, `pytest-dev__pytest-10356`, `sympy__sympy-13852`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| astropy/astropy (15) | none |
| django/django (207) | GPT-5.2 10→11, GPT-5 mini 11→10 |
| matplotlib/matplotlib (27) | none |
| mwaskom/seaborn (2) | none |
| pallets/flask (1) | none |
| psf/requests (8) | none |
| pydata/xarray (20) | Claude Opus 4.6 2→3, MiniMax M2.5 3→2 |
| pylint-dev/pylint (7) | none |
| pytest-dev/pytest (18) | none |
| scikit-learn/scikit-learn (32) | none |
| sphinx-doc/sphinx (36) | none |
| sympy/sympy (66) | Gemini 3 Flash 5→6, GLM-5 6→5 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (421) | Solved by every model (211) | Solved by fewer (210) |
|---|---:|---:|---:|
| Claude Opus 4.5 | 52.8 (1) | 61.8 (1) | 43.7 (1) |
| Claude Opus 4.6 | 49.0 (2) | 57.9 (2) | 40.1 (3) |
| MiniMax M2.5 | 48.2 (3) | 56.1 (4) | 40.4 (2) |
| Kimi K2.5 | 44.9 (4) | 57.4 (3) | 32.3 (5) |
| Gemini 3 Flash | 43.9 (5) | 50.3 (8) | 37.5 (4) |
| GLM-5 | 42.7 (6) | 54.1 (5) | 31.2 (6) |
| Claude Sonnet 4.5 | 39.8 (7) | 51.3 (7) | 28.3 (7) |
| Claude Haiku 4.5 | 36.0 (8) | 52.2 (6) | 19.7 (9) |
| DeepSeek V3.2 | 30.7 (9) | 41.3 (10) | 19.9 (8) |
| GPT-5.2 | 28.9 (10) | 38.8 (11) | 19.0 (10) |
| GPT-5 mini | 26.7 (11) | 45.6 (9) | 7.7 (11) |

## What drives each adjacent gap

Difference in mean score split by outcome (a/b), and the tasks that move it most. Contributions are per-task differences divided by the task count, so they sum to the gap.

- **Claude Opus 4.5 − Claude Opus 4.6 = 3.78**: failed/failed 0.06 (31), failed/solved -3.59 (22), solved/failed 3.92 (27), solved/solved 3.38 (341). For Claude Opus 4.5: `django__django-13315` +0.27 (solved/failed), `psf__requests-2931` +0.24 (solved/failed), `sympy__sympy-22456` +0.24 (solved/failed). For Claude Opus 4.6: `django__django-15957` -0.24 (failed/solved), `sympy__sympy-14976` -0.23 (failed/solved), `psf__requests-5414` -0.23 (failed/solved).
- **Claude Opus 4.6 − MiniMax M2.5 = 0.75**: failed/failed 0.02 (26), failed/solved -4.56 (32), solved/failed 4.35 (28), solved/solved 0.94 (335). For Claude Opus 4.6: `sympy__sympy-21612` +0.22 (solved/failed), `psf__requests-5414` +0.22 (solved/failed), `django__django-12193` +0.22 (solved/failed). For MiniMax M2.5: `django__django-15022` -0.23 (failed/solved), `sphinx-doc__sphinx-8056` -0.23 (failed/solved), `pylint-dev__pylint-7080` -0.23 (failed/solved).
- **MiniMax M2.5 − Kimi K2.5 = 3.37**: failed/failed 0.01 (41), failed/solved -1.83 (13), solved/failed 5.91 (39), solved/solved -0.72 (328). For MiniMax M2.5: `scikit-learn__scikit-learn-13124` +0.25 (solved/failed), `astropy__astropy-14182` +0.23 (solved/failed), `matplotlib__matplotlib-24149` +0.23 (solved/failed). For Kimi K2.5: `scikit-learn__scikit-learn-13328` -0.21 (failed/solved), `scikit-learn__scikit-learn-25102` -0.21 (failed/solved), `pytest-dev__pytest-7432` -0.19 (failed/solved).
- **Kimi K2.5 − Gemini 3 Flash = 0.96**: failed/failed 0.18 (39), failed/solved -6.59 (41), solved/failed 2.74 (18), solved/solved 4.63 (323). For Kimi K2.5: `scikit-learn__scikit-learn-25102` +0.25 (solved/failed), `sympy__sympy-18698` +0.21 (solved/failed), `sympy__sympy-15875` +0.20 (solved/failed). For Gemini 3 Flash: `django__django-15563` -0.24 (failed/solved), `matplotlib__matplotlib-26291` -0.24 (failed/solved), `sympy__sympy-21379` -0.24 (failed/solved).
- **Gemini 3 Flash − GLM-5 = 1.23**: failed/failed -0.03 (36), failed/solved -3.21 (21), solved/failed 5.11 (34), solved/solved -0.65 (330). For Gemini 3 Flash: `pytest-dev__pytest-7324` +0.24 (solved/failed), `sympy__sympy-14248` +0.23 (solved/failed), `pylint-dev__pylint-6386` +0.23 (solved/failed). For GLM-5: `pydata__xarray-3993` -0.26 (failed/solved), `sphinx-doc__sphinx-9281` -0.25 (failed/solved), `django__django-16560` -0.24 (failed/solved).
- **GLM-5 − Claude Sonnet 4.5 = 2.87**: failed/failed 0.14 (44), failed/solved -2.98 (26), solved/failed 4.92 (31), solved/solved 0.79 (320). For GLM-5: `sphinx-doc__sphinx-8265` +0.25 (solved/failed), `sphinx-doc__sphinx-9281` +0.24 (solved/failed), `django__django-14053` +0.24 (solved/failed). For Claude Sonnet 4.5: `sympy__sympy-15976` -0.21 (failed/solved), `pytest-dev__pytest-7205` -0.20 (failed/solved), `sphinx-doc__sphinx-8035` -0.18 (solved/solved).
- **Claude Sonnet 4.5 − Claude Haiku 4.5 = 3.83**: failed/failed 0.19 (64), failed/solved -1.36 (11), solved/failed 5.65 (36), solved/solved -0.66 (310). For Claude Sonnet 4.5: `sympy__sympy-14711` +0.24 (solved/failed), `sphinx-doc__sphinx-8621` +0.23 (solved/failed), `django__django-16032` +0.22 (solved/failed). For Claude Haiku 4.5: `django__django-16662` -0.22 (failed/solved), `astropy__astropy-14309` -0.20 (solved/solved), `psf__requests-5414` -0.20 (failed/solved).
- **Claude Haiku 4.5 − DeepSeek V3.2 = 5.33**: failed/failed 0.05 (63), failed/solved -4.48 (37), solved/failed 2.70 (20), solved/solved 7.06 (301). For Claude Haiku 4.5: `pytest-dev__pytest-7490` +0.24 (solved/failed), `psf__requests-5414` +0.24 (solved/failed), `sympy__sympy-18211` +0.22 (solved/failed). For DeepSeek V3.2: `django__django-16032` -0.25 (failed/solved), `django__django-11433` -0.23 (failed/solved), `django__django-16454` -0.23 (failed/solved).
- **DeepSeek V3.2 − GPT-5.2 = 1.73**: failed/failed 0.05 (51), failed/solved -4.27 (32), solved/failed 2.10 (20), solved/solved 3.85 (318). For DeepSeek V3.2: `pytest-dev__pytest-10081` +0.20 (solved/solved), `sympy__sympy-24539` +0.19 (solved/solved), `sphinx-doc__sphinx-7440` +0.19 (solved/solved). For GPT-5.2: `sympy__sympy-24562` -0.25 (failed/solved), `django__django-11964` -0.21 (failed/solved), `django__django-15916` -0.21 (failed/solved).
- **GPT-5.2 − GPT-5 mini = 2.22**: failed/failed -0.30 (52), failed/solved -2.51 (19), solved/failed 9.22 (90), solved/solved -4.19 (260). For GPT-5.2: `django__django-11265` +0.24 (solved/failed), `sphinx-doc__sphinx-7454` +0.24 (solved/failed), `sympy__sympy-24562` +0.24 (solved/failed). For GPT-5 mini: `sympy__sympy-13878` -0.26 (failed/solved), `sphinx-doc__sphinx-10673` -0.23 (failed/solved), `django__django-16819` -0.21 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability examples/ten-model-500/score-panel.json examples/ten-model-500/*.jsonl --output examples/ten-model-500/sensitivity.json
```

All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
