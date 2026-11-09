# DeepSWE, harness comparison: Python (33 tasks × 3 attempts, 40 setups)

The Python tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash, low and high effort, in ten coding-agent harnesses (OpenCode 1.19.0 and 2.2.6 separately), from Joel Niklaus's Harness Leaderboard. Method, sources, caveats and reproduction are in that README; this folder is the Python board ([page](../../site/harnesses-python.html)).

- Dataset (items with reference solutions) SHA256 `faa57641002ef71ea2fb114a8e31b877cea62cf27b268c63845cb0f52791cc2d`; analyzer `0.10.0-beta`, commit `3e213a1`.
- SHA256: [population.json](population.json) `1304ebda…`, [score-panel.json](score-panel.json) `6f8c828c…`, [scores.json](scores.json) `928c965f…`, [coverage.json](coverage.json) `38ca42e0…`, [sensitivity.json](sensitivity.json) `bd5a1088…`.

## Ranking (same tasks)

This table predates the OpenCode 2.2.6 setups (36 setups); the 40-setup ranking is on the [website](https://parsimony.lasu.dev/harnesses-python.html) and in [scores.json](scores.json).

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · Codex | 0.83× | 0.77–0.88× | 19 | +1,416.6 | +1,337.2 | 30.3% | 29/30 |
| 2 | GLM-5.3 Flash (low) · Qwen Code | 0.85× | 0.81–0.89× | 26 | +1,423.6 | +1,382.5 | 45.5% | 45/45 |
| 3 | GLM-5.3 Flash (high) · Codex | 0.86× | 0.80–0.91× | 18 | +1,409.9 | +1,431.7 | 32.3% | 30/32 |
| 4 | GLM-5.3 Flash (low) · pi | 0.88× | 0.84–0.92× | 29 | +1,430.4 | +1,463.4 | 55.6% | 54/55 |
| 5 | GLM-5.3 Flash (low) · Kimi Code | 0.89× | 0.83–0.94× | 28 | +1,468.8 | +1,485.4 | 57.6% | 56/57 |
| 6 | GLM-5.3 Flash (low) · Claude Code | 0.90× | 0.85–0.94× | 25 | +1,591.6 | +1,491.2 | 55.6% | 55/55 |
| 7 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.91× | 0.86–0.96× | 29 | +1,552.7 | +1,535.5 | 63.6% | 60/63 |
| 8 | GLM-5.3 Flash (high) · Qwen Code | 0.93× | 0.90–0.95× | 27 | +1,497.4 | +1,544.1 | 59.6% | 58/59 |
| 9 | GLM-5.3 Flash (low) · OpenCode | 0.94× | 0.89–0.99× | 18 | +1,570.5 | +1,434.8 | 35.4% | 33/35 |
| 10 | DeepSeek V4.1 Flash (high) · Codex | 0.94× | 0.89–0.99× | 28 | +1,534.5 | +1,547.9 | 64.6% | 60/64 |
| 11 | GLM-5.3 Flash (low) · Hermes | 0.95× | 0.89–1.02× | 27 | +1,480.3 | +1,515.5 | 51.5% | 50/51 |
| 12 | GLM-5.3 Flash (high) · Kimi Code | 0.95× | 0.91–1.00× | 29 | +1,494.3 | +1,606.1 | 63.6% | 62/63 |
| 13 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.95× | 0.91–1.01× | 29 | +1,576.0 | +1,566.9 | 72.7% | 69/72 |
| 14 | GLM-5.3 Flash (high) · Claude Code | 0.97× | 0.93–1.00× | 27 | +1,527.5 | +1,592.1 | 65.7% | 64/65 |
| 15 | DeepSeek V4.1 Flash (high) · OpenCode | 0.97× | 0.93–1.01× | 20 | +1,628.8 | +1,331.1 | 44.4% | 42/44 |
| 16 | DeepSeek V4.1 Flash (high) · Claude Code | 0.99× | 0.94–1.04× | 30 | +1,678.2 | +1,617.2 | 71.7% | 70/71 |
| 17 | DeepSeek V4.1 Flash (low) · Codex | 0.99× | 0.94–1.03× | 27 | +1,547.3 | +1,595.3 | 55.6% | 53/55 |
| 17 | DeepSeek V4.1 Flash (low) · Hermes | 0.99× | 0.92–1.07× | 30 | +1,608.9 | +1,580.8 | 69.7% | 66/69 |
| 17 | DeepSeek V4.1 Flash (low) · Claude Code | 0.99× | 0.94–1.05× | 29 | +1,706.1 | +1,649.4 | 69.7% | 67/69 |
| 20 | DeepSeek V4.1 Flash (low) · OpenCode | 0.99× | 0.92–1.10× | 23 | +1,527.4 | +1,402.0 | 47.5% | 44/47 |
| 20 | GLM-5.3 Flash (high) · pi | 0.99× | 0.94–1.04× | 28 | +1,610.2 | +1,567.7 | 63.6% | 63/63 |
| 22 | DeepSeek V4.1 Flash (low) · Kimi Code | 1.01× | 0.94–1.09× | 27 | +1,772.0 | +1,723.3 | 62.6% | 60/62 |
| 23 | DeepSeek V4.1 Flash (high) · Kimi Code | 1.01× | 0.96–1.07× | 28 | +1,664.0 | +1,632.1 | 61.6% | 59/61 |
| 24 | GLM-5.3 Flash (low) · OpenClaw | 1.02× | 0.94–1.12× | 16 | +1,677.4 | +1,563.2 | 33.3% | 30/33 |
| 25 | GLM-5.3 Flash (high) · Hermes | 1.02× | 0.97–1.08× | 28 | +1,613.9 | +1,656.0 | 59.6% | 59/59 |
| 26 | GLM-5.3 Flash (high) · OpenCode | 1.05× | 0.98–1.13× | 21 | +1,670.3 | +1,540.1 | 35.4% | 35/35 |
| 27 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.05× | 1.00–1.11× | 27 | +1,763.5 | +1,771.0 | 62.6% | 62/62 |
| 28 | DeepSeek V4.1 Flash (high) · pi | 1.07× | 1.02–1.16× | 30 | +1,778.1 | +1,582.1 | 63.6% | 61/63 |
| 29 | DeepSeek V4.1 Flash (low) · pi | 1.09× | 1.03–1.16× | 29 | +1,793.8 | +1,677.8 | 64.6% | 62/64 |
| 30 | GLM-5.3 Flash (high) · OpenClaw | 1.11× | 1.05–1.17× | 20 | +1,644.5 | +1,664.9 | 39.4% | 39/39 |
| 31 | DeepSeek V4.1 Flash (high) · Hermes | 1.12× | 1.06–1.19× | 31 | +1,801.6 | +1,804.5 | 77.8% | 74/77 |
| 32 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.15× | 1.06–1.26× | 28 | +1,944.2 | +1,903.4 | 61.6% | 59/61 |
| 33 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.16× | 1.03–1.32× | 26 | +1,965.8 | +1,895.8 | 70.7% | 67/70 |
| 34 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.18× | 1.12–1.24× | 28 | +1,936.2 | +1,938.3 | 65.7% | 62/65 |
| — | DeepSeek V4.1 Flash (low) · OpenClaw | 1.22× | 1.07–1.39× | 13 | +1,867.5 | +633.4 | 23.2% | 23/23 |
| — | DeepSeek V4.1 Flash (high) · OpenClaw | 1.26× | 1.04–1.57× | 9 | +1,898.0 | +485.1 | 13.1% | 10/13 |
