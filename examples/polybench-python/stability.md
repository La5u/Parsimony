# Score sensitivity: 5 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `swe-polybench-verified-python-v1`: 113 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (103 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: polybench-deepseek-v4-flash-mobile-coder-1.2.4 ≈ polybench-claude-opus-5.5-jitto-build ≈ polybench-gpt-5.6-sol-slingshot-3.4.0 ≈ polybench-claude-opus-5.5-aiwork-code ≈ polybench-claude-opus-4.8-hmigbot (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (0 of 4 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 4 pairs): polybench-deepseek-v4-flash-mobile-coder-1.2.4 vs polybench-claude-opus-5.5-jitto-build, polybench-claude-opus-5.5-jitto-build vs polybench-gpt-5.6-sol-slingshot-3.4.0, polybench-gpt-5.6-sol-slingshot-3.4.0 vs polybench-claude-opus-5.5-aiwork-code, polybench-claude-opus-5.5-aiwork-code vs polybench-claude-opus-4.8-hmigbot.
- **Midpoint rank never changes under any variation**: none.
- Difficulty strata answer a different question and are not counted as variations; they reverse polybench-deepseek-v4-flash-mobile-coder-1.2.4 > polybench-claude-opus-5.5-jitto-build (solved by fewer); polybench-claude-opus-5.5-jitto-build > polybench-gpt-5.6-sol-slingshot-3.4.0 (solved by all); polybench-gpt-5.6-sol-slingshot-3.4.0 > polybench-claude-opus-5.5-aiwork-code (solved by fewer); polybench-claude-opus-5.5-aiwork-code > polybench-claude-opus-4.8-hmigbot (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 113 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | polybench-deepseek-v4-flash-mobile-coder-1.2.4 | 37.6 | 30.3–44.1 | 36.7–38.4 | 1–2 | 1.0–4.0 | 0.55 |
| 2 | polybench-claude-opus-5.5-jitto-build | 37.0 | 30.9–42.2 | 36.3–37.8 | 1–2 | 1.0–3.0 | 0.43 |
| 3 | polybench-gpt-5.6-sol-slingshot-3.4.0 | 30.5 | 22.6–38.1 | 29.6–31.4 | 3–5 | 1.0–5.0 | 0.01 |
| 4 | polybench-claude-opus-5.5-aiwork-code | 29.2 | 22.8–35.0 | 28.5–30.0 | 3–4 | 2.0–5.0 | 0.00 |
| 5 | polybench-claude-opus-4.8-hmigbot | 27.9 | 20.4–35.0 | 26.4–29.3 | 4–5 | 2.0–5.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| polybench-deepseek-v4-flash-mobile-coder-1.2.4 > polybench-claude-opus-5.5-jitto-build | 0.53 | -8.46 to 9.80 | 0.39 | net weight=0.5, net weight=0.6, net weight=0.7, failure cap=50, panel without polybench-gpt-5.6-sol-slingshot-3.4.0, without keras-team/keras, without langchain-ai/langchain | no |
| polybench-claude-opus-5.5-jitto-build > polybench-gpt-5.6-sol-slingshot-3.4.0 | 6.49 | -3.05 to 15.56 | 0.88 | none | yes |
| polybench-gpt-5.6-sol-slingshot-3.4.0 > polybench-claude-opus-5.5-aiwork-code | 1.31 | -7.76 to 10.07 | 0.47 | without huggingface/transformers | no |
| polybench-claude-opus-5.5-aiwork-code > polybench-claude-opus-4.8-hmigbot | 1.35 | -7.95 to 10.84 | 0.41 | none | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| polybench-deepseek-v4-flash-mobile-coder-1.2.4 | 37.6 (1) | 35.6 (2) | 36.2 (2) | 36.9 (2) | 38.2 (1) | 38.9 (1) | 37.6 (1) | 39.8 (1) | 38.9 (1) | 35.3 (2) |
| polybench-claude-opus-5.5-jitto-build | 37.0 (2) | 36.8 (1) | 36.8 (1) | 36.9 (1) | 37.1 (2) | 37.2 (2) | 36.9 (2) | 38.4 (2) | 37.9 (2) | 35.6 (1) |
| polybench-gpt-5.6-sol-slingshot-3.4.0 | 30.5 (3) | 31.0 (3) | 30.9 (3) | 30.7 (3) | 30.4 (3) | 30.2 (3) | 31.0 (3) | 33.7 (3) | 32.5 (3) | 27.3 (3) |
| polybench-claude-opus-5.5-aiwork-code | 29.2 (4) | 29.9 (4) | 29.7 (4) | 29.4 (4) | 29.0 (4) | 28.8 (4) | 29.2 (4) | 31.6 (4) | 30.7 (4) | 26.8 (4) |
| polybench-claude-opus-4.8-hmigbot | 27.9 (5) | 28.2 (5) | 28.1 (5) | 28.0 (5) | 27.8 (5) | 27.7 (5) | 27.5 (5) | 31.1 (5) | 29.8 (5) | 24.6 (5) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (22 of 390 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| polybench-claude-opus-4.8-hmigbot | 69 | 8 | none |
| polybench-claude-opus-5.5-aiwork-code | 80 | 8 | none |
| polybench-claude-opus-5.5-jitto-build | 97 | 12 | none |
| polybench-deepseek-v4-flash-mobile-coder-1.2.4 | 80 | 16 | none |
| polybench-gpt-5.6-sol-slingshot-3.4.0 | 64 | 8 | polybench-deepseek-v4-flash-mobile-coder-1.2.4 1→2, polybench-claude-opus-5.5-jitto-build 2→1 |
| (dedup panel) | 22 | 0 | none |

Tasks that lose their only reference: polybench-claude-opus-4.8-hmigbot: `huggingface__transformers-13989`, `huggingface__transformers-28115`, `keras-team__keras-18871`, `keras-team__keras-19459`, `keras-team__keras-19466`, `keras-team__keras-19826`, `keras-team__keras-19973`, `langchain-ai__langchain-5625`; polybench-claude-opus-5.5-aiwork-code: `huggingface__transformers-13989`, `huggingface__transformers-28115`, `keras-team__keras-18871`, `keras-team__keras-19459`, `keras-team__keras-19466`, `keras-team__keras-19826`, `keras-team__keras-19973`, `langchain-ai__langchain-5625`; polybench-claude-opus-5.5-jitto-build: `huggingface__transformers-13989`, `huggingface__transformers-17082`, `huggingface__transformers-23141`, `huggingface__transformers-23223`, `huggingface__transformers-27717`, `huggingface__transformers-28115`, `keras-team__keras-18871`, `keras-team__keras-19459`, `keras-team__keras-19466`, `keras-team__keras-19826`, `keras-team__keras-19973`, `langchain-ai__langchain-5625`; polybench-deepseek-v4-flash-mobile-coder-1.2.4: `huggingface__transformers-13989`, `huggingface__transformers-15843`, `huggingface__transformers-25765`, `huggingface__transformers-27114`, `huggingface__transformers-27663`, `huggingface__transformers-28115`, `huggingface__transformers-7562`, `huggingface__transformers-8747`, `keras-team__keras-18871`, `keras-team__keras-19459`, `keras-team__keras-19466`, `keras-team__keras-19826`, `keras-team__keras-19863`, `keras-team__keras-19973`, `keras-team__keras-20002`, `langchain-ai__langchain-5625`; polybench-gpt-5.6-sol-slingshot-3.4.0: `huggingface__transformers-13989`, `huggingface__transformers-28115`, `keras-team__keras-18871`, `keras-team__keras-19459`, `keras-team__keras-19466`, `keras-team__keras-19826`, `keras-team__keras-19973`, `langchain-ai__langchain-5625`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| Significant-Gravitas/AutoGPT (1) | none |
| huggingface/transformers (72) | polybench-gpt-5.6-sol-slingshot-3.4.0 3→5, polybench-claude-opus-5.5-aiwork-code 4→3, polybench-claude-opus-4.8-hmigbot 5→4 |
| keras-team/keras (22) | polybench-deepseek-v4-flash-mobile-coder-1.2.4 1→2, polybench-claude-opus-5.5-jitto-build 2→1 |
| langchain-ai/langchain (13) | polybench-deepseek-v4-flash-mobile-coder-1.2.4 1→2, polybench-claude-opus-5.5-jitto-build 2→1 |
| yt-dlp/yt-dlp (5) | none |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (113) | Solved by every model (43) | Solved by fewer (70) |
|---|---:|---:|---:|
| polybench-deepseek-v4-flash-mobile-coder-1.2.4 | 37.6 (1) | 54.1 (2) | 27.4 (2) |
| polybench-claude-opus-5.5-jitto-build | 37.0 (2) | 44.4 (5) | 32.5 (1) |
| polybench-gpt-5.6-sol-slingshot-3.4.0 | 30.5 (3) | 59.7 (1) | 12.6 (5) |
| polybench-claude-opus-5.5-aiwork-code | 29.2 (4) | 44.5 (4) | 19.9 (3) |
| polybench-claude-opus-4.8-hmigbot | 27.9 (5) | 49.8 (3) | 14.4 (4) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **polybench-deepseek-v4-flash-mobile-coder-1.2.4 − polybench-claude-opus-5.5-jitto-build = 0.69**: failed/solved -13.21 (25), solved/failed 4.50 (8), solved/solved 9.40 (72). For polybench-deepseek-v4-flash-mobile-coder-1.2.4: `keras-team__keras-19636` +0.75 (solved/solved), `huggingface__transformers-27114` +0.65 (solved/failed), `huggingface__transformers-22649` +0.64 (solved/solved). For polybench-claude-opus-5.5-jitto-build: `huggingface__transformers-5122` -0.77 (failed/solved), `huggingface__transformers-25884` -0.76 (failed/solved), `huggingface__transformers-31217` -0.75 (failed/solved).
- **polybench-claude-opus-5.5-jitto-build − polybench-gpt-5.6-sol-slingshot-3.4.0 = 6.87**: solved/failed 16.07 (33), solved/solved -9.20 (64). For polybench-claude-opus-5.5-jitto-build: `huggingface__transformers-31217` +0.81 (solved/failed), `keras-team__keras-18553` +0.81 (solved/failed), `yt-dlp__yt-dlp-4841` +0.71 (solved/failed). For polybench-gpt-5.6-sol-slingshot-3.4.0: `huggingface__transformers-8554` -0.75 (solved/solved), `keras-team__keras-19924` -0.71 (solved/solved), `keras-team__keras-19838` -0.66 (solved/solved).
- **polybench-gpt-5.6-sol-slingshot-3.4.0 − polybench-claude-opus-5.5-aiwork-code = 1.53**: failed/failed -0.14 (20), failed/solved -10.33 (21), solved/failed 3.10 (5), solved/solved 8.89 (59). For polybench-gpt-5.6-sol-slingshot-3.4.0: `huggingface__transformers-30899` +0.85 (solved/failed), `keras-team__keras-19838` +0.79 (solved/failed), `huggingface__transformers-21345` +0.75 (solved/solved). For polybench-claude-opus-5.5-aiwork-code: `Significant-Gravitas__AutoGPT-4652` -0.76 (failed/solved), `yt-dlp__yt-dlp-5933` -0.74 (failed/solved), `huggingface__transformers-19590` -0.71 (failed/solved).
- **polybench-claude-opus-5.5-aiwork-code − polybench-claude-opus-4.8-hmigbot = 0.75**: failed/failed 0.11 (16), failed/solved -5.34 (9), solved/failed 9.43 (18), solved/solved -3.45 (60). For polybench-claude-opus-5.5-aiwork-code: `yt-dlp__yt-dlp-5933` +0.75 (solved/failed), `huggingface__transformers-13693` +0.73 (solved/failed), `huggingface__transformers-26568` +0.73 (solved/failed). For polybench-claude-opus-4.8-hmigbot: `huggingface__transformers-25884` -0.77 (failed/solved), `huggingface__transformers-23126` -0.73 (solved/solved), `huggingface__transformers-7075` -0.72 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability examples/polybench-python/score-panel.json examples/polybench-python/polybench-claude-opus-4.8-hmigbot.jsonl examples/polybench-python/polybench-claude-opus-5.5-aiwork-code.jsonl examples/polybench-python/polybench-claude-opus-5.5-jitto-build.jsonl examples/polybench-python/polybench-deepseek-v4-flash-mobile-coder-1.2.4.jsonl examples/polybench-python/polybench-gpt-5.6-sol-slingshot-3.4.0.jsonl --output examples/polybench-python/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
