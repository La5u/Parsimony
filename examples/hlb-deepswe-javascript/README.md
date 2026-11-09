# DeepSWE, harness comparison: JavaScript (5 tasks × 3 attempts, 40 setups)

The JavaScript tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash, low and high effort, in ten coding-agent harnesses (OpenCode 1.19.0 and 2.2.6 separately), from Joel Niklaus's Harness Leaderboard. Method, sources, caveats and reproduction are in that README; this folder is the JavaScript board ([page](../../site/harnesses-javascript.html)). Only 5 tasks, so the order is rough and there are few 95% ranges.

- Dataset (items with reference solutions) SHA256 `0d7e1fbbef85f316e0a2b398833fd5f63fd8f17a281c8856b6e8e439afcdd80f`; analyzer `0.10.0-beta`, commit `3e213a1`.
- SHA256: [population.json](population.json) `3247b719…`, [score-panel.json](score-panel.json) `c1f8f3c2…`, [scores.json](scores.json) `9d9d13b3…`, [coverage.json](coverage.json) `12c23d24…`, [sensitivity.json](sensitivity.json) `b0f494be…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · OpenCode 2 | 0.77× | — | 3 | +1,445.7 | +2,163.1 | 46.7% | 7/7 |
| 2 | GLM-5.3 Flash (high) · Codex | 0.78× | — | 4 | +1,357.8 | +1,910.7 | 40.0% | 6/6 |
| 3 | GLM-5.3 Flash (low) · pi | 0.82× | — | 4 | +1,493.6 | +2,186.1 | 46.7% | 7/7 |
| 4 | GLM-5.3 Flash (low) · Qwen Code | 0.85× | — | 3 | +1,486.6 | +2,274.2 | 33.3% | 5/5 |
| 4 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.85× | — | 4 | +2,417.2 | +2,173.9 | 66.7% | 10/10 |
| 6 | DeepSeek V4.1 Flash (high) · Codex | 0.86× | 0.82–0.94× | 5 | +2,355.8 | +2,253.1 | 73.3% | 11/11 |
| 7 | DeepSeek V4.1 Flash (low) · OpenCode | 0.87× | — | 4 | +2,310.3 | +1,944.0 | 60.0% | 9/9 |
| 7 | GLM-5.3 Flash (low) · Hermes | 0.87× | — | 3 | +1,496.2 | +2,295.8 | 40.0% | 6/6 |
| 7 | DeepSeek V4.1 Flash (high) · Claude Code | 0.87× | 0.75–1.10× | 5 | +2,168.0 | +2,271.1 | 73.3% | 11/11 |
| 10 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.88× | — | 4 | +2,666.2 | +2,459.0 | 60.0% | 9/9 |
| 10 | DeepSeek V4.1 Flash (low) · pi | 0.88× | 0.72–1.25× | 5 | +2,180.3 | +2,448.2 | 66.7% | 10/10 |
| 12 | DeepSeek V4.1 Flash (high) · pi | 0.89× | 0.78–1.03× | 5 | +2,371.5 | +2,135.1 | 80.0% | 12/12 |
| 13 | DeepSeek V4.1 Flash (low) · Hermes | 0.90× | 0.79–1.07× | 5 | +2,363.2 | +2,245.3 | 86.7% | 13/13 |
| 14 | GLM-5.3 Flash (low) · Claude Code | 0.92× | — | 4 | +1,687.6 | +2,321.7 | 46.7% | 7/7 |
| 14 | DeepSeek V4.1 Flash (low) · Claude Code | 0.92× | 0.82–1.08× | 5 | +2,047.2 | +2,291.7 | 66.7% | 10/10 |
| 16 | DeepSeek V4.1 Flash (high) · OpenCode | 0.93× | 0.83–1.08× | 5 | +2,242.1 | +1,815.9 | 66.7% | 10/10 |
| 16 | DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.93× | 0.86–1.05× | 5 | +2,267.3 | +2,346.5 | 73.3% | 11/11 |
| 16 | GLM-5.3 Flash (low) · Codex | 0.93× | — | 3 | +1,578.0 | +1,892.3 | 26.7% | 4/4 |
| 19 | DeepSeek V4.1 Flash (low) · Codex | 0.94× | — | 4 | +2,434.0 | +2,349.3 | 60.0% | 9/9 |
| 20 | GLM-5.3 Flash (high) · Kimi Code | 0.95× | — | 4 | +1,865.4 | +2,544.9 | 46.7% | 7/7 |
| 21 | GLM-5.3 Flash (high) · Qwen Code | 0.97× | — | 4 | +2,194.8 | +2,422.1 | 53.3% | 8/8 |
| 22 | DeepSeek V4.1 Flash (low) · OpenCode 2 | 0.98× | 0.87–1.08× | 5 | +2,259.2 | +2,408.1 | 86.7% | 13/13 |
| 22 | GLM-5.3 Flash (high) · OpenCode 2 | 0.98× | — | 4 | +2,017.4 | +2,415.3 | 60.0% | 9/9 |
| 24 | GLM-5.3 Flash (high) · Claude Code | 0.99× | — | 4 | +2,375.1 | +2,516.9 | 66.7% | 10/10 |
| 24 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 0.99× | 0.80–1.34× | 5 | +2,581.0 | +2,434.3 | 86.7% | 13/13 |
| 26 | DeepSeek V4.1 Flash (high) · Hermes | 1.00× | 0.91–1.10× | 5 | +2,534.0 | +2,446.5 | 73.3% | 11/11 |
| 27 | GLM-5.3 Flash (low) · OpenClaw | 1.01× | — | 3 | +1,826.2 | +2,649.3 | 33.3% | 5/5 |
| 28 | GLM-5.3 Flash (high) · Hermes | 1.04× | — | 4 | +1,865.1 | +2,521.5 | 60.0% | 9/9 |
| 29 | DeepSeek V4.1 Flash (low) · Kimi Code | 1.05× | 0.89–1.33× | 5 | +2,619.4 | +2,587.5 | 73.3% | 11/11 |
| 30 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.08× | — | 4 | +1,921.3 | +2,538.5 | 60.0% | 9/9 |
| 30 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.08× | 0.91–1.40× | 5 | +2,747.9 | +2,775.8 | 93.3% | 14/14 |
| 30 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.08× | — | 4 | +2,007.5 | +2,594.8 | 73.3% | 11/11 |
| 33 | GLM-5.3 Flash (high) · pi | 1.09× | — | 4 | +2,171.8 | +2,489.4 | 60.0% | 9/9 |
| 34 | DeepSeek V4.1 Flash (low) · OpenClaw | 1.37× | — | 3 | +2,465.0 | +1,986.3 | 40.0% | 6/6 |
| 35 | DeepSeek V4.1 Flash (high) · Kimi Code | 1.45× | — | 4 | +3,340.1 | +3,233.1 | 66.7% | 10/10 |
| 36 | DeepSeek V4.1 Flash (high) · OpenClaw | 2.12× | — | 4 | +4,606.7 | +2,171.8 | 40.0% | 6/6 |
| — | GLM-5.3 Flash (high) · OpenClaw | 1.57× | — | 1 | +3,203.0 | +1,802.9 | 6.7% | 1/1 |
| — | GLM-5.3 Flash (high) · OpenCode | 1.07× | — | 1 | +1,609.0 | +1,613.5 | 13.3% | 2/2 |
| — | GLM-5.3 Flash (low) · Kimi Code | 0.88× | — | 2 | +1,613.7 | +2,167.0 | 20.0% | 3/3 |
| — | GLM-5.3 Flash (low) · OpenCode | 1.06× | — | 2 | +1,899.0 | +2,380.4 | 13.3% | 2/2 |
