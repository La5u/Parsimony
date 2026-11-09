# DeepSWE, harness comparison: 2 models × 2 efforts × 10 harnesses × 106 tasks × 3 attempts (analyzer 0.10.0)

**Beta research preview, not an official ranking.** Joel Niklaus's [Harness Leaderboard](https://huggingface.co/spaces/joelniklaus/harness-leaderboard) ([article](https://pasqualepillitteri.it/en/news/30849/harness-leaderboard-coding-agent-harness-ranking)) runs the same model in different coding-agent harnesses on the 111 [DeepSWE](https://deepswe.datacurve.ai) v1.1 tasks, at the commit the DeepSWE boards use, three attempts per task, and publishes every trial's final patch and verifier reward in a public [Hugging Face bucket](https://huggingface.co/buckets/joelniklaus/harness-leaderboard). This board measures those patches: **which harness writes less code for the same model.** It is its own board ([all languages](../../site/harnesses.html), [Python](../../site/harnesses-python.html), [JavaScript](../../site/harnesses-javascript.html), [TypeScript](../../site/harnesses-typescript.html), [Go](../../site/harnesses-go.html)) and is never pooled with the DeepSWE boards, which run every model in mini-SWE-agent with four attempts.

## What is measured

- **Setups:** GLM-5.3 Flash and DeepSeek V4.1 Flash, at low and high reasoning effort, each in Claude Code 2.1.300, Codex 0.162.1, pi 1.2.0, OpenCode 1.19.0, OpenCode 2.2.6 (shown as OpenCode 2, its own harness), Hermes v0.22.1, mini-SWE-agent 2.4.6, Kimi Code 2.2.0, Qwen Code 0.25.2 and OpenClaw 2026.10.4: the 36 full-stage setups of the leaderboard's public board at version 0.1.1 (Space commit a1b2bee9), plus the 4 OpenCode 2.2.6 setups that replaced OpenCode 1.19.0 on its board at version 0.1.2 (Space commit c60b5e2e, frozen in [trials-opencode-2.json](trials-opencode-2.json)). Flint is left out: it runs only in OpenCode and solves few tasks.
- **Trials and outcomes:** exactly the trials the public board scores, with its pass/fail: the earliest three scored attempts per task, after its exclusions (infrastructure failures, cancelled trials, other harness versions, providers outside the model's pool) and its answer-key rules (a trial whose model received the task's reference solution or hidden tests is a fail; DeepSWE trials that looked their answer up online before the tasks ran offline were re-run). [trials.json](trials.json) freezes them with each patch's bucket path; [hlb-board-trials.py](../benchmark-discovery/hlb-board-trials.py) builds it by porting the board's selection (its Space code is not run). Every one of the 40 setups matches the published board's scored and passed counts. Our own oracle scan of trajectories was not run on these trials; the leaderboard's answer-key detection and trajectory scan apply instead.
- **Languages:** 33 Python, 5 JavaScript, 35 TypeScript and 33 Go tasks are measured, each on its own board; the 5 Rust tasks are not (no Rust analyzer). 12,720 items, 12,704 measured: 10 patches failed to apply or parse and 6 failed attempts left nothing to measure.
- **Reference pool:** every passing patch of a task, from any setup and attempt, as on the DeepSWE boards; DeepSWE's own reference solution is the human comparison.

## Ranking, all languages

As on the website: a setup's net units added on the tasks it solved, divided by what the other setups added on those same tasks (0.8× = 20% less code), per language, then averaged over languages weighted by shared tasks. Only tasks solved by at least 3 other setups count; a setup needs 15 such tasks.

This table is the peer ratio. The website now ranks by the ratio to the human fix (`docs/method.md`), so its order differs.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · Codex | 0.85× | 0.81–0.90× | 54 | 27.4% | 82/87 |
| 2 | GLM-5.3 Flash (low) · Qwen Code | 0.88× | 0.85–0.91× | 80 | 47.2% | 147/150 |
| 3 | GLM-5.3 Flash (high) · Codex | 0.89× | 0.86–0.92× | 66 | 35.8% | 111/114 |
| 4 | GLM-5.3 Flash (low) · pi | 0.90× | 0.88–0.93× | 81 | 52.5% | 161/167 |
| 5 | GLM-5.3 Flash (low) · Kimi Code | 0.92× | 0.89–0.94× | 78 | 51.6% | 160/164 |
| 5 | GLM-5.3 Flash (low) · OpenCode 2 | 0.92× | 0.90–0.95× | 84 | 55.7% | 172/177 |
| 7 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.93× | 0.90–0.95× | 84 | 61.9% | 190/197 |
| 7 | GLM-5.3 Flash (low) · Claude Code | 0.93× | 0.91–0.96× | 80 | 56.0% | 175/178 |
| 9 | GLM-5.3 Flash (low) · Hermes | 0.94× | 0.91–0.97× | 79 | 51.6% | 159/164 |
| 10 | GLM-5.3 Flash (high) · Qwen Code | 0.95× | 0.93–0.97× | 81 | 55.3% | 172/176 |
| 10 | GLM-5.3 Flash (low) · OpenCode | 0.95× | 0.92–0.99× | 55 | 31.4% | 95/100 |
| 12 | DeepSeek V4.1 Flash (high) · Codex | 0.96× | 0.93–0.98× | 89 | 63.8% | 196/203 |
| 13 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.97× | 0.93–1.02× | 86 | 61.9% | 190/197 |
| 13 | DeepSeek V4.1 Flash (low) · Codex | 0.97× | 0.95–1.00× | 89 | 61.9% | 190/197 |
| 13 | GLM-5.3 Flash (high) · Kimi Code | 0.97× | 0.94–1.00× | 86 | 63.8% | 198/203 |
| 16 | GLM-5.3 Flash (high) · pi | 0.98× | 0.95–1.00× | 83 | 61.0% | 192/194 |
| 16 | DeepSeek V4.1 Flash (high) · Claude Code | 0.98× | 0.94–1.01× | 91 | 67.3% | 207/214 |
| 16 | DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.98× | 0.96–1.00× | 90 | 65.1% | 202/207 |
| 16 | DeepSeek V4.1 Flash (low) · Claude Code | 0.98× | 0.96–1.01× | 87 | 65.7% | 203/209 |
| 16 | GLM-5.3 Flash (high) · Claude Code | 0.98× | 0.96–1.01× | 85 | 61.3% | 191/195 |
| 21 | GLM-5.3 Flash (high) · OpenCode 2 | 0.99× | 0.96–1.02× | 89 | 60.7% | 187/193 |
| 21 | DeepSeek V4.1 Flash (low) · Kimi Code | 0.99× | 0.96–1.03× | 94 | 68.2% | 212/217 |
| 23 | DeepSeek V4.1 Flash (low) · OpenCode 2 | 1.00× | 0.96–1.04× | 85 | 67.9% | 210/216 |
| 23 | DeepSeek V4.1 Flash (low) · OpenCode | 1.00× | 0.97–1.04× | 75 | 51.6% | 155/164 |
| 23 | DeepSeek V4.1 Flash (high) · OpenCode | 1.00× | 0.97–1.03× | 70 | 49.7% | 151/158 |
| 23 | GLM-5.3 Flash (low) · OpenClaw | 1.00× | 0.96–1.04× | 57 | 30.8% | 92/98 |
| 27 | DeepSeek V4.1 Flash (low) · Hermes | 1.01× | 0.98–1.04× | 97 | 70.8% | 218/225 |
| 28 | GLM-5.3 Flash (high) · Hermes | 1.02× | 0.99–1.05× | 85 | 59.1% | 185/188 |
| 29 | DeepSeek V4.1 Flash (low) · pi | 1.04× | 1.00–1.09× | 89 | 63.5% | 196/202 |
| 29 | DeepSeek V4.1 Flash (high) · pi | 1.04× | 1.00–1.09× | 92 | 63.2% | 196/201 |
| 31 | GLM-5.3 Flash (high) · OpenCode | 1.05× | 1.00–1.09× | 61 | 34.0% | 103/108 |
| 31 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.05× | 1.02–1.08× | 83 | 56.3% | 175/179 |
| 33 | DeepSeek V4.1 Flash (high) · Hermes | 1.06× | 1.02–1.10× | 97 | 75.5% | 232/240 |
| 34 | DeepSeek V4.1 Flash (high) · Kimi Code | 1.08× | 1.00–1.16× | 88 | 61.3% | 190/195 |
| 34 | GLM-5.3 Flash (high) · OpenClaw | 1.08× | 1.05–1.13× | 67 | 35.8% | 110/114 |
| 36 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.13× | 1.08–1.18× | 93 | 67.0% | 206/213 |
| 37 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.15× | 1.11–1.18× | 88 | 62.9% | 194/200 |
| 38 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.16× | 1.09–1.23× | 87 | 69.2% | 211/220 |
| 39 | DeepSeek V4.1 Flash (low) · OpenClaw | 1.17× | 1.06–1.30× | 50 | 24.2% | 76/77 |
| 40 | DeepSeek V4.1 Flash (high) · OpenClaw | 1.25× | 1.09–1.41× | 36 | 18.9% | 55/60 |

Averaged over its four setups, each harness's ratio: Codex 0.92×, Qwen Code 0.93×, Claude Code 0.97×, OpenCode 2 0.97×, Kimi Code 0.99×, pi 0.99×, OpenCode 1.00×, Hermes 1.01×, mini-SWE-agent 1.12×, OpenClaw 1.13×. Individual setups move further between low and high effort.

## Caveats

- **Two models, both small.** The harness order may differ for frontier models.
- **Solve rates differ a lot** (19% to 75%). Ratios compare only shared solved tasks, but a setup that solves few tasks is compared on the easier ones.
- **Outcomes are the leaderboard's,** not rerun here. Its board can change: re-run hlb-board-trials.py at a newer Space commit to refresh.

## Reproduce

```sh
# Bucket files runs/<run>/{run.json,invalid.json,deep-swe/trials-*.jsonl} ('/' -> '__') in FACTS/, a listing of each run's
# deep-swe/ trial folders in where.json, and the Space's hlb/data/ at commit a1b2bee9 in SPACE/ (HF token recommended).
python examples/benchmark-discovery/hlb-board-trials.py SPACE FACTS where.json examples/hlb-deepswe/trials.json
git clone https://github.com/datacurve-ai/deep-swe && git -C deep-swe checkout 0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea
for lang in python javascript typescript go; do   # Go needs pip install '.[languages]'
  python -m parsimony.hlb dataset deep-swe --trials examples/hlb-deepswe/trials.json --language $lang --output deepswe-$lang.jsonl
  python -m parsimony.hlb analyze SETUP --trials examples/hlb-deepswe/trials.json --dataset deepswe-$lang.jsonl --output SETUP.jsonl  # per setup
  python -m parsimony.release freeze deepswe-$lang.jsonl --name hlb-deepswe-v1.1-$lang-N --output population.json
  python -m parsimony.deepswe panel *_*.jsonl --name hlb-deepswe-v1.1-$lang-40-pooled-80-20 --output score-panel.json
  python -m parsimony.release audit population.json *_*.jsonl --dataset deepswe-$lang.jsonl --output coverage.json
  python -m parsimony.scoring score score-panel.json *_*.jsonl --output scores.json
  python -m parsimony.stability score-panel.json *_*.jsonl --output sensitivity.json --report sensitivity.md
done
```

Pinned inputs for the 4 OpenCode 2.2.6 setups: Space commit `c60b5e2e38a2382723e8828a22f9bc54fb4b64ca` (board version 0.1.2, facts read 2026-11-09), [trials-opencode-2.json](trials-opencode-2.json) SHA256 `104f1820eb238fac4cdd5141619d3d7aa0efb4b014644178dfc39710807d0912`; run hlb-board-trials.py at that commit and keep only OpenCode, renamed `opencode-2`.

Pinned inputs for the other 36: Space commit `a1b2bee98f28b1e23dc18e4856b356b8254d3812` (board version 0.1.1, facts read 2026-11-08), [trials.json](trials.json) SHA256 `a09a59343505d922e4b3d910148ba1f3deceae10b0e642ecf8f2544a8868f983`, DeepSWE tasks at `0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea`, analyzer `0.10.0-beta` at commit `3e213a1`. Raw patches stay in the bucket.
