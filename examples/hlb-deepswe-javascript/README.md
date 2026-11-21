# DeepSWE, harness comparison: JavaScript (5 tasks × 3 attempts, 65 setups)

The JavaScript tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash at low and high effort, and Ripple-65B Preview, each in thirteen coding-agent harnesses, from Joel Niklaus's Harness Leaderboard (v0.1.11). Method, sources, caveats and reproduction are in that README; this folder is the JavaScript board ([page](../../site/harnesses-javascript.html)). Only 5 tasks, so the order is rough and there are few 95% ranges.

- Dataset (items with reference solutions) SHA256 `0d7e1fbbef85f316e0a2b398833fd5f63fd8f17a281c8856b6e8e439afcdd80f`; analyzer `0.11.0-beta`, commit `635dfc1`, Python 3.14.8.
- SHA256: [population.json](population.json) `2622bcca…`, [score-panel.json](score-panel.json) `6f1a0dc8…`, [scores.json](scores.json) `7c0b6b44…`, [coverage.json](coverage.json) `84df7c0b…`, [sensitivity.json](sensitivity.json) `f9c4579e…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · OpenClaw | 0.76× | — | 3 | +1,399.2 | +2,227.7 | 33.3% | 5/5 |
| 2 | GLM-5.3 Flash (low) · OpenCode | 0.78× | — | 3 | +1,445.7 | +2,163.1 | 46.7% | 7/7 |
| 3 | GLM-5.3 Flash (high) · Codex | 0.80× | — | 4 | +1,357.8 | +1,910.7 | 40.0% | 6/6 |
| 4 | GLM-5.3 Flash (low) · Kimi Code | 0.80× | — | 3 | +1,340.4 | +2,213.7 | 46.7% | 7/7 |
| 5 | GLM-5.3 Flash (low) · Hermes | 0.83× | — | 3 | +1,472.0 | +2,193.2 | 46.7% | 7/7 |
| 6 | GLM-5.3 Flash (low) · pi | 0.83× | — | 4 | +1,493.6 | +2,186.1 | 46.7% | 7/7 |
| 7 | GLM-5.3 Flash (low) · DeepSeek Harness | 0.85× | — | 4 | +1,476.9 | +2,285.9 | 46.7% | 7/7 |
| 8 | GLM-5.3 Flash (low) · Qwen Code | 0.86× | — | 3 | +1,486.6 | +2,274.2 | 33.3% | 5/5 |
| 9 | DeepSeek V4.1 Flash (low) · Hermes | 0.87× | — | 4 | +2,010.7 | +2,252.0 | 40.0% | 6/6 |
| 10 | DeepSeek V4.1 Flash (low) · oh-my-pi | 0.89× | — | 4 | +2,179.0 | +1,949.1 | 60.0% | 9/9 |
| 11 | DeepSeek V4.1 Flash (high) · DeepSeek Harness | 0.90× | 0.80–0.96× | 5 | +2,161.5 | +2,161.5 | 100.0% | 15/15 |
| 12 | DeepSeek V4.1 Flash (high) · Codex | 0.90× | 0.85–0.97× | 5 | +2,355.8 | +2,253.1 | 73.3% | 11/11 |
| 13 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.91× | — | 4 | +2,379.9 | +2,297.5 | 53.3% | 8/8 |
| 14 | DeepSeek V4.1 Flash (low) · Grok Build | 0.92× | 0.87–0.98× | 5 | +2,428.7 | +2,220.7 | 73.3% | 11/11 |
| 15 | DeepSeek V4.1 Flash (high) · Grok Build | 0.92× | 0.86–1.03× | 5 | +2,285.4 | +2,208.8 | 66.7% | 10/10 |
| 16 | DeepSeek V4.1 Flash (low) · DeepSeek Harness | 0.93× | 0.87–1.00× | 5 | +2,163.8 | +2,283.5 | 73.3% | 11/11 |
| 17 | GLM-5.3 Flash (low) · Claude Code | 0.93× | — | 4 | +1,687.6 | +2,321.7 | 46.7% | 7/7 |
| 18 | DeepSeek V4.1 Flash (high) · Claude Code | 0.94× | 0.82–1.14× | 5 | +2,253.7 | +2,299.4 | 66.7% | 10/10 |
| 19 | DeepSeek V4.1 Flash (high) · fx | 0.94× | 0.85–0.99× | 5 | +2,500.6 | +2,253.3 | 73.3% | 11/11 |
| 20 | GLM-5.3 Flash (low) · Codex | 0.94× | — | 3 | +1,578.0 | +1,892.3 | 26.7% | 4/4 |
| 20 | DeepSeek V4.1 Flash (high) · Hermes | 0.94× | — | 4 | +2,234.5 | +2,270.0 | 66.7% | 10/10 |
| 22 | GLM-5.3 Flash (low) · fx | 0.95× | — | 4 | +1,821.7 | +2,439.3 | 46.7% | 7/7 |
| 23 | DeepSeek V4.1 Flash (low) · fx | 0.95× | — | 4 | +2,466.8 | +2,282.1 | 73.3% | 11/11 |
| 24 | GLM-5.3 Flash (high) · fx | 0.95× | — | 3 | +1,799.5 | +2,472.7 | 40.0% | 6/6 |
| 25 | DeepSeek V4.1 Flash (high) · OpenClaw | 0.96× | 0.90–0.98× | 5 | +2,140.2 | +2,307.4 | 80.0% | 12/12 |
| 26 | DeepSeek V4.1 Flash (low) · pi | 0.96× | — | 4 | +2,293.4 | +2,477.9 | 60.0% | 9/9 |
| 27 | DeepSeek V4.1 Flash (low) · Claude Code | 0.96× | 0.88–1.11× | 5 | +2,047.2 | +2,291.7 | 66.7% | 10/10 |
| 28 | DeepSeek V4.1 Flash (high) · OpenCode | 0.97× | 0.92–1.04× | 5 | +2,267.3 | +2,346.5 | 73.3% | 11/11 |
| 28 | DeepSeek V4.1 Flash (high) · pi | 0.97× | 0.94–1.03× | 5 | +2,558.4 | +2,246.1 | 73.3% | 11/11 |
| 30 | DeepSeek V4.1 Flash (high) · Kimi Code | 0.97× | — | 4 | +1,855.7 | +2,383.5 | 46.7% | 7/7 |
| 31 | DeepSeek V4.1 Flash (low) · Codex | 0.98× | — | 4 | +2,434.0 | +2,349.3 | 60.0% | 9/9 |
| 32 | DeepSeek V4.1 Flash (high) · oh-my-pi | 1.00× | — | 4 | +1,819.0 | +2,397.3 | 60.0% | 9/9 |
| 32 | DeepSeek V4.1 Flash (low) · Kimi Code | 1.00× | 0.89–1.06× | 5 | +2,633.8 | +2,434.3 | 53.3% | 8/8 |
| 34 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.01× | 0.92–1.14× | 5 | +2,594.9 | +2,426.5 | 80.0% | 12/12 |
| 35 | GLM-5.3 Flash (high) · Qwen Code | 1.01× | — | 4 | +2,194.8 | +2,422.1 | 53.3% | 8/8 |
| 36 | DeepSeek V4.1 Flash (low) · OpenClaw | 1.01× | 0.95–1.21× | 5 | +2,444.6 | +2,419.7 | 66.7% | 10/10 |
| 37 | DeepSeek V4.1 Flash (low) · OpenCode | 1.02× | 0.92–1.11× | 5 | +2,259.2 | +2,408.1 | 86.7% | 13/13 |
| 38 | Ripple-65B Preview · Codex | 1.02× | — | 4 | +2,430.1 | +2,690.3 | 46.7% | 7/7 |
| 39 | GLM-5.3 Flash (high) · OpenClaw | 1.03× | — | 3 | +1,655.5 | +2,517.7 | 53.3% | 8/8 |
| 40 | GLM-5.3 Flash (high) · OpenCode | 1.03× | — | 4 | +2,017.4 | +2,415.3 | 60.0% | 9/9 |
| 41 | DeepSeek V4.1 Flash (low) · Qwen Code | 1.03× | — | 4 | +2,577.8 | +2,463.0 | 80.0% | 12/12 |
| 42 | GLM-5.3 Flash (high) · Grok Build | 1.03× | 0.90–1.13× | 5 | +2,005.8 | +2,498.7 | 73.3% | 11/11 |
| 43 | GLM-5.3 Flash (high) · Claude Code | 1.03× | — | 4 | +2,375.1 | +2,516.9 | 66.7% | 10/10 |
| 44 | GLM-5.3 Flash (high) · Hermes | 1.09× | — | 4 | +2,285.6 | +2,609.0 | 53.3% | 8/8 |
| 45 | Ripple-65B Preview · DeepSeek Harness | 1.09× | — | 3 | +2,970.8 | +2,064.1 | 26.7% | 4/4 |
| 46 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.10× | — | 4 | +1,921.3 | +2,538.5 | 60.0% | 9/9 |
| 47 | Ripple-65B Preview · Kimi Code | 1.10× | — | 4 | +3,080.5 | +2,628.2 | 53.3% | 8/8 |
| 48 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.10× | — | 4 | +2,007.5 | +2,594.8 | 73.3% | 11/11 |
| 49 | GLM-5.3 Flash (high) · Kimi Code | 1.13× | — | 4 | +2,245.9 | +2,636.7 | 53.3% | 8/8 |
| 50 | GLM-5.3 Flash (high) · pi | 1.14× | — | 4 | +2,171.8 | +2,489.4 | 60.0% | 9/9 |
| 51 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.14× | 0.98–1.39× | 5 | +2,692.3 | +2,714.6 | 86.7% | 13/13 |
| 52 | GLM-5.3 Flash (high) · DeepSeek Harness | 1.14× | 0.96–1.23× | 5 | +2,864.3 | +2,836.1 | 66.7% | 10/10 |
| 53 | Ripple-65B Preview · OpenCode | 1.14× | — | 3 | +2,058.8 | +2,576.2 | 40.0% | 6/6 |
| 54 | Ripple-65B Preview · Grok Build | 1.15× | — | 4 | +2,365.1 | +2,731.7 | 60.0% | 9/9 |
| 55 | Ripple-65B Preview · oh-my-pi | 1.19× | — | 4 | +2,560.9 | +2,634.9 | 53.3% | 8/8 |
| 56 | Ripple-65B Preview · Hermes | 1.28× | — | 3 | +2,138.0 | +2,363.1 | 40.0% | 6/6 |
| 57 | Ripple-65B Preview · pi | 1.37× | — | 3 | +2,503.2 | +2,788.6 | 40.0% | 6/6 |
| — | GLM-5.3 Flash (low) · Grok Build | 0.81× | — | 2 | +1,469.2 | +2,059.3 | 40.0% | 6/6 |
| — | Ripple-65B Preview · Qwen Code | 0.92× | — | 2 | +1,731.7 | +2,152.2 | 20.0% | 3/3 |
| — | GLM-5.3 Flash (low) · oh-my-pi | 0.97× | — | 2 | +1,849.3 | +2,249.7 | 20.0% | 3/3 |
| — | GLM-5.3 Flash (high) · oh-my-pi | 0.99× | — | 2 | +1,808.8 | +2,314.3 | 40.0% | 6/6 |
| — | Ripple-65B Preview · OpenClaw | 1.26× | — | 1 | +2,675.0 | +831.4 | 13.3% | 2/2 |
| — | Ripple-65B Preview · Claude Code | 1.28× | — | 2 | +2,510.2 | +2,546.9 | 26.7% | 4/4 |
| — | Ripple-65B Preview · fx | 1.34× | — | 1 | +2,844.7 | +1,663.3 | 20.0% | 3/3 |
| — | Ripple-65B Preview · mini-SWE-agent | 1.79× | — | 2 | +3,407.0 | +2,327.2 | 20.0% | 3/3 |
