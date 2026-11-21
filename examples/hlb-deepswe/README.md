# DeepSWE, harness comparison: 3 models × 13 harnesses (65 setups) × 106 tasks × 3 attempts (analyzer 0.11.0)

**Beta research preview, not an official ranking.** Joel Niklaus's [Harness Leaderboard](https://huggingface.co/spaces/joelniklaus/harness-leaderboard) ([article](https://pasqualepillitteri.it/en/news/30849/harness-leaderboard-coding-agent-harness-ranking)) runs the same model in different coding-agent harnesses on the 111 [DeepSWE](https://deepswe.datacurve.ai) v1.1 tasks, at the commit the DeepSWE boards use, three attempts per task, and publishes every trial's final patch and verifier reward in a public [Hugging Face bucket](https://huggingface.co/buckets/joelniklaus/harness-leaderboard). This board measures those patches: **which harness writes less code for the same model.** It is its own board ([all languages](../../site/harnesses.html), [Python](../../site/harnesses-python.html), [JavaScript](../../site/harnesses-javascript.html), [TypeScript](../../site/harnesses-typescript.html), [Go](../../site/harnesses-go.html)) and is never pooled with the DeepSWE boards, which run every model in mini-SWE-agent with four attempts.

## What is measured

- **Setups:** GLM-5.3 Flash and DeepSeek V4.1 Flash at low and high reasoning effort, and Ripple-65B Preview (no effort setting), each in Claude Code 2.1.300, Codex 0.162.1, pi 1.2.0, oh-my-pi 18.18.3, OpenCode 2.2.6, Hermes v0.22.1, mini-SWE-agent 2.4.6, Kimi Code 2.2.0, Qwen Code 0.25.2, OpenClaw 2026.11.1, Grok Build 1.0.77, fx 0.0.16 and DeepSeek Harness 0.2.2-rc.1: the 65 full-stage setups of the leaderboard's public board at version 0.1.11 (Space commit 3cf8a208, 2026-11-21). Flint is left out: it solves 1 to 36 of 333 attempts per harness. Until 2026-11-21 this board held the 40 setups of versions 0.1.1 and 0.1.2 (ten harnesses, OpenCode 1.19.0 and 2.2.6 separately); since then the leaderboard has re-run the Hermes, Kimi Code, OpenClaw and some Qwen Code cells and dropped OpenCode 1.19.0, so the board was rebuilt from 0.1.11 rather than extended (git history keeps the old records).
- **Trials and outcomes:** exactly the trials the public board scores, with its pass/fail, as the leaderboard publishes them in `results/trials.csv.gz` (sha256-listed in `results/index.json`): the earliest three scored attempts per task, after its exclusions (infrastructure failures, cancelled trials, other harness versions, providers outside the model's pool) and its answer-key rules (a trial whose model got access to the task's answer is a fail). [trials.json](trials.json) freezes them with each patch's bucket path; [hlb-results-trials.py](../benchmark-discovery/hlb-results-trials.py) builds it. Our own oracle scan of trajectories was not run on these trials; the leaderboard's answer-key detection and trajectory scan apply instead.
- **Languages:** 33 Python, 5 JavaScript, 35 TypeScript and 33 Go tasks are measured, each on its own board; the 5 Rust tasks are not (no Rust analyzer). 20,670 items, 20,660 measured: 9 patches failed to apply or parse and 1 attempt left no patch.
- **Reference pool:** every passing patch of a task, from any setup and attempt, as on the DeepSWE boards; DeepSWE's own reference solution is the human comparison.

## Ranking, all languages

As on the website: a setup's net units added on the tasks it solved, divided by what the other setups added on those same tasks (0.8× = 20% less code), per language, then averaged over languages weighted by shared tasks. Only tasks solved by at least 3 other setups count; a setup needs 15 such tasks.

This table is the peer ratio. The website now ranks by the ratio to the human fix (`docs/method.md`), so its order differs.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · Codex | 0.85× | 0.81–0.90× | 54 | — | — | 27.4% | 82/87 |
| 2 | GLM-5.3 Flash (high) · Codex | 0.89× | 0.86–0.92× | 66 | — | — | 35.8% | 111/114 |
| 3 | GLM-5.3 Flash (low) · Qwen Code | 0.89× | 0.86–0.91× | 80 | — | — | 47.2% | 147/150 |
| 4 | GLM-5.3 Flash (low) · Grok Build | 0.89× | 0.87–0.91× | 84 | — | — | 56.0% | 175/178 |
| 5 | GLM-5.3 Flash (low) · pi | 0.90× | 0.88–0.92× | 82 | — | — | 52.8% | 162/168 |
| 6 | GLM-5.3 Flash (low) · Hermes | 0.91× | 0.89–0.94× | 79 | — | — | 52.8% | 162/168 |
| 6 | GLM-5.3 Flash (low) · oh-my-pi | 0.91× | 0.88–0.94× | 76 | — | — | 44.7% | 138/142 |
| 8 | GLM-5.3 Flash (low) · Kimi Code | 0.91× | 0.89–0.94× | 80 | — | — | 51.6% | 161/164 |
| 9 | GLM-5.3 Flash (low) · fx | 0.92× | 0.90–0.94× | 83 | — | — | 54.1% | 168/172 |
| 10 | GLM-5.3 Flash (low) · OpenCode | 0.92× | 0.90–0.94× | 84 | — | — | 55.7% | 172/177 |
| 11 | GLM-5.3 Flash (low) · OpenClaw | 0.93× | 0.91–0.95× | 81 | — | — | 52.2% | 163/166 |
| 12 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.93× | 0.91–0.95× | 84 | — | — | 60.4% | 188/192 |
| 13 | GLM-5.3 Flash (low) · Claude Code | 0.93× | 0.90–0.96× | 80 | — | — | 56.0% | 175/178 |
| 14 | DeepSeek V4.1 Flash (low) · Hermes | 0.94× | 0.91–0.97× | 77 | — | — | 53.8% | 165/171 |
| 15 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.94× | 0.92–0.96× | 87 | — | — | 58.8% | 180/187 |
| 15 | DeepSeek V4.1 Flash (low) · oh-my-pi | 0.94× | 0.91–0.97× | 82 | — | — | 57.2% | 175/182 |
| 17 | GLM-5.3 Flash (high) · oh-my-pi | 0.94× | 0.92–0.96× | 81 | — | — | 57.2% | 176/182 |
| 18 | DeepSeek V4.1 Flash (low) · Kimi Code | 0.94× | 0.92–0.97× | 88 | — | — | 62.3% | 192/198 |
| 19 | DeepSeek V4.1 Flash (low) · fx | 0.95× | 0.92–0.97× | 85 | — | — | 60.1% | 186/191 |
| 20 | GLM-5.3 Flash (high) · Qwen Code | 0.95× | 0.93–0.97× | 81 | — | — | 55.3% | 172/176 |
| 21 | DeepSeek V4.1 Flash (high) · Codex | 0.96× | 0.93–0.99× | 90 | — | — | 64.2% | 197/204 |
| 22 | DeepSeek V4.1 Flash (high) · Kimi Code | 0.96× | 0.94–0.98× | 93 | — | — | 60.1% | 187/191 |
| 22 | DeepSeek V4.1 Flash (high) · oh-my-pi | 0.96× | 0.94–0.99× | 84 | — | — | 56.0% | 175/178 |
| 24 | DeepSeek V4.1 Flash (low) · Grok Build | 0.96× | 0.94–0.98× | 89 | — | — | 64.8% | 202/206 |
| 25 | DeepSeek V4.1 Flash (high) · Claude Code | 0.96× | 0.94–0.99× | 90 | — | — | 65.7% | 202/209 |
| 25 | DeepSeek V4.1 Flash (low) · Claude Code | 0.96× | 0.94–0.99× | 86 | — | — | 65.1% | 201/207 |
| 27 | DeepSeek V4.1 Flash (low) · OpenClaw | 0.97× | 0.93–1.01× | 86 | — | — | 56.0% | 172/178 |
| 28 | DeepSeek V4.1 Flash (high) · Grok Build | 0.97× | 0.94–1.00× | 89 | — | — | 65.7% | 202/209 |
| 28 | DeepSeek V4.1 Flash (low) · Codex | 0.97× | 0.95–0.99× | 89 | — | — | 61.9% | 190/197 |
| 30 | GLM-5.3 Flash (high) · pi | 0.97× | 0.95–1.00× | 83 | — | — | 61.0% | 192/194 |
| 31 | DeepSeek V4.1 Flash (high) · OpenClaw | 0.97× | 0.95–1.00× | 90 | — | — | 63.5% | 197/202 |
| 32 | GLM-5.3 Flash (high) · Grok Build | 0.98× | 0.95–1.00× | 85 | — | — | 63.8% | 198/203 |
| 33 | DeepSeek V4.1 Flash (high) · OpenCode | 0.98× | 0.96–1.00× | 90 | — | — | 65.1% | 202/207 |
| 34 | DeepSeek V4.1 Flash (high) · Hermes | 0.98× | 0.96–1.01× | 84 | — | — | 61.9% | 190/197 |
| 34 | DeepSeek V4.1 Flash (low) · pi | 0.98× | 0.95–1.01× | 80 | — | — | 58.5% | 181/186 |
| 36 | GLM-5.3 Flash (high) · Claude Code | 0.99× | 0.96–1.01× | 85 | — | — | 61.3% | 191/195 |
| 37 | DeepSeek V4.1 Flash (high) · fx | 0.99× | 0.96–1.02× | 85 | — | — | 61.0% | 187/194 |
| 38 | GLM-5.3 Flash (high) · Kimi Code | 0.99× | 0.96–1.02× | 87 | — | — | 61.6% | 191/196 |
| 39 | DeepSeek V4.1 Flash (low) · OpenCode | 0.99× | 0.96–1.03× | 85 | — | — | 67.9% | 210/216 |
| 40 | DeepSeek V4.1 Flash (high) · pi | 0.99× | 0.97–1.02× | 88 | — | — | 59.1% | 184/188 |
| 40 | GLM-5.3 Flash (low) · DeepSeek Harness | 0.99× | 0.97–1.01× | 82 | — | — | 57.5% | 179/183 |
| 42 | GLM-5.3 Flash (high) · OpenCode | 0.99× | 0.96–1.02× | 89 | — | — | 60.7% | 187/193 |
| 43 | GLM-5.3 Flash (high) · fx | 1.00× | 0.98–1.02× | 88 | — | — | 61.3% | 188/195 |
| 44 | DeepSeek V4.1 Flash (high) · DeepSeek Harness | 1.01× | 0.99–1.03× | 90 | — | — | 69.8% | 215/222 |
| 44 | GLM-5.3 Flash (high) · OpenClaw | 1.01× | 0.98–1.05× | 81 | — | — | 58.5% | 181/186 |
| 46 | DeepSeek V4.1 Flash (low) · DeepSeek Harness | 1.02× | 0.98–1.07× | 88 | — | — | 66.0% | 205/210 |
| 46 | GLM-5.3 Flash (high) · Hermes | 1.02× | 0.98–1.06× | 88 | — | — | 58.8% | 184/187 |
| 48 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.05× | 1.02–1.08× | 83 | — | — | 56.3% | 175/179 |
| 49 | GLM-5.3 Flash (high) · DeepSeek Harness | 1.06× | 1.03–1.10× | 85 | — | — | 63.8% | 200/203 |
| 50 | Ripple-65B Preview · Qwen Code | 1.07× | 1.02–1.12× | 62 | — | — | 30.5% | 92/97 |
| 51 | Ripple-65B Preview · fx | 1.07× | 1.04–1.11× | 66 | — | — | 38.4% | 115/122 |
| 52 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.07× | 1.04–1.11× | 84 | — | — | 67.0% | 205/213 |
| 53 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.07× | 1.04–1.11× | 87 | — | — | 61.0% | 188/194 |
| 54 | Ripple-65B Preview · oh-my-pi | 1.08× | 1.04–1.12× | 67 | — | — | 36.8% | 114/117 |
| 55 | Ripple-65B Preview · Grok Build | 1.10× | 1.07–1.13× | 71 | — | — | 45.3% | 138/144 |
| 56 | Ripple-65B Preview · OpenClaw | 1.12× | 1.07–1.17× | 52 | — | — | 24.2% | 74/77 |
| 57 | Ripple-65B Preview · Kimi Code | 1.14× | 1.09–1.18× | 75 | — | — | 49.4% | 150/157 |
| 58 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.14× | 1.11–1.18× | 88 | — | — | 62.6% | 193/199 |
| 59 | Ripple-65B Preview · pi | 1.15× | 1.10–1.20× | 73 | — | — | 43.4% | 130/138 |
| 60 | Ripple-65B Preview · DeepSeek Harness | 1.16× | 1.12–1.20× | 59 | — | — | 37.4% | 114/119 |
| 60 | Ripple-65B Preview · Hermes | 1.16× | 1.12–1.21× | 79 | — | — | 48.1% | 147/153 |
| 62 | Ripple-65B Preview · OpenCode | 1.16× | 1.11–1.23× | 76 | — | — | 46.5% | 141/148 |
| 63 | Ripple-65B Preview · Codex | 1.23× | 1.18–1.28× | 78 | — | — | 49.1% | 149/156 |
| 64 | Ripple-65B Preview · Claude Code | 1.24× | 1.18–1.29× | 66 | — | — | 40.9% | 124/130 |
| 65 | Ripple-65B Preview · mini-SWE-agent | 1.41× | 1.32–1.50× | 55 | — | — | 32.1% | 95/102 |

Averaged over its five setups, each harness's ratio: Qwen Code 0.95×, oh-my-pi 0.97×, Codex 0.98×, Grok Build 0.98×, fx 0.98×, Kimi Code 0.99×, pi 1.00×, Hermes 1.00×, OpenClaw 1.00×, OpenCode 1.01×, Claude Code 1.02×, DeepSeek Harness 1.05×, mini-SWE-agent 1.15×. Individual setups move further between low and high effort.

## Caveats

- **Three models, all small or open-weight.** The harness order may differ for frontier models.
- **Solve rates differ a lot** (24% to 70%). Ratios compare only shared solved tasks, but a setup that solves few tasks is compared on the easier ones.
- **Outcomes are the leaderboard's,** not rerun here. Its board can change: rebuild trials.json from a newer `results/` release to refresh.

## Reproduce

```sh
B=https://huggingface.co/buckets/joelniklaus/harness-leaderboard/resolve/results
curl -LO $B/trials.csv.gz && curl -LO $B/index.json   # release 0.1.11 (later releases replace these files)
python examples/benchmark-discovery/hlb-results-trials.py trials.csv.gz index.json 3cf8a20805cbe6bccad1c34db2287aa76487df8e \
  examples/hlb-deepswe/trials.json --skip-model RecursiveSI/flint
git clone https://github.com/datacurve-ai/deep-swe && git -C deep-swe checkout 0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea
for lang in python javascript typescript go; do   # Go needs pip install '.[languages]'; run from a clean checkout
  python -m parsimony.hlb dataset deep-swe --trials examples/hlb-deepswe/trials.json --language $lang --output deepswe-$lang.jsonl
  python -m parsimony.hlb analyze SETUP --trials examples/hlb-deepswe/trials.json --dataset deepswe-$lang.jsonl --output SETUP.jsonl  # per setup
  python -m parsimony.release freeze deepswe-$lang.jsonl --name hlb-deepswe-v1.1-$lang-N --analyzer-commit COMMIT --output population.json
  python -m parsimony.deepswe panel *_*.jsonl --name hlb-deepswe-v1.1-$lang-65-pooled-80-20 --output score-panel.json
  python -m parsimony.release audit population.json *_*.jsonl --dataset deepswe-$lang.jsonl --output coverage.json
  python -m parsimony.scoring score score-panel.json *_*.jsonl --output scores.json
  python -m parsimony.stability score-panel.json *_*.jsonl --output sensitivity.json --report sensitivity.md
done
```

Pinned inputs: Space commit `3cf8a20805cbe6bccad1c34db2287aa76487df8e` (board version 0.1.11, read 2026-11-21), `results/trials.csv.gz` SHA256 `f61691290dafe891e7edcfb947fea4125a05f588066015b13442ce1d55fc2701`, [trials.json](trials.json) SHA256 `c115aa7b769b3f1f5b35a5c6a7bb34903577e60c31f66f8ed8cca2acf3c7b77b`, DeepSWE tasks at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`, analyzer `0.11.0-beta` at commit `635dfc1`, Python 3.14.8. Raw patches stay in the bucket.
