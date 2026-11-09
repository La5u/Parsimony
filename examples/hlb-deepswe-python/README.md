# DeepSWE, harness comparison: Python (33 tasks × 3 attempts, 40 setups)

The Python tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash, low and high effort, in ten coding-agent harnesses (OpenCode 1.19.0 and 2.2.6 separately), from Joel Niklaus's Harness Leaderboard. Method, sources, caveats and reproduction are in that README; this folder is the Python board ([page](../../site/harnesses-python.html)).

- Dataset (items with reference solutions) SHA256 `faa57641002ef71ea2fb114a8e31b877cea62cf27b268c63845cb0f52791cc2d`; analyzer `0.10.0-beta`, commit `3e213a1`.
- SHA256: [population.json](population.json) `1304ebda…`, [score-panel.json](score-panel.json) `6f8c828c…`, [scores.json](scores.json) `928c965f…`, [coverage.json](coverage.json) `38ca42e0…`, [sensitivity.json](sensitivity.json) `bd5a1088…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · Codex | 0.83× | 0.77–0.89× | 19 | +1,416.6 | +1,337.2 | 30.3% | 29/30 |
| 2 | GLM-5.3 Flash (low) · Qwen Code | 0.85× | 0.81–0.89× | 26 | +1,423.6 | +1,382.5 | 45.5% | 45/45 |
| 3 | GLM-5.3 Flash (high) · Codex | 0.86× | 0.81–0.92× | 18 | +1,409.9 | +1,431.7 | 32.3% | 30/32 |
| 4 | GLM-5.3 Flash (low) · pi | 0.88× | 0.84–0.93× | 29 | +1,430.4 | +1,463.4 | 55.6% | 54/55 |
| 5 | GLM-5.3 Flash (low) · Kimi Code | 0.89× | 0.83–0.94× | 28 | +1,468.8 | +1,485.4 | 57.6% | 56/57 |
| 6 | GLM-5.3 Flash (low) · Claude Code | 0.91× | 0.86–0.95× | 25 | +1,591.6 | +1,491.2 | 55.6% | 55/55 |
| 7 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.92× | 0.87–0.96× | 29 | +1,552.7 | +1,535.5 | 63.6% | 60/63 |
| 8 | GLM-5.3 Flash (low) · OpenCode 2 | 0.93× | 0.90–0.96× | 25 | +1,476.3 | +1,431.4 | 53.5% | 51/53 |
| 8 | GLM-5.3 Flash (high) · Qwen Code | 0.93× | 0.91–0.95× | 27 | +1,497.4 | +1,544.1 | 59.6% | 58/59 |
| 10 | GLM-5.3 Flash (low) · OpenCode | 0.94× | 0.89–0.99× | 18 | +1,570.5 | +1,434.8 | 35.4% | 33/35 |
| 11 | DeepSeek V4.1 Flash (high) · Codex | 0.95× | 0.90–0.99× | 28 | +1,534.5 | +1,547.9 | 64.6% | 60/64 |
| 11 | GLM-5.3 Flash (low) · Hermes | 0.95× | 0.89–1.02× | 27 | +1,480.3 | +1,515.5 | 51.5% | 50/51 |
| 13 | GLM-5.3 Flash (high) · Kimi Code | 0.96× | 0.91–1.00× | 29 | +1,494.3 | +1,606.1 | 63.6% | 62/63 |
| 13 | DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.96× | 0.91–1.01× | 27 | +1,548.6 | +1,646.7 | 55.6% | 53/55 |
| 13 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.96× | 0.92–1.01× | 29 | +1,576.0 | +1,566.9 | 72.7% | 69/72 |
| 16 | GLM-5.3 Flash (high) · Claude Code | 0.97× | 0.93–1.01× | 27 | +1,527.5 | +1,592.1 | 65.7% | 64/65 |
| 17 | DeepSeek V4.1 Flash (high) · OpenCode | 0.98× | 0.94–1.01× | 20 | +1,628.8 | +1,331.1 | 44.4% | 42/44 |
| 17 | GLM-5.3 Flash (high) · OpenCode 2 | 0.98× | 0.93–1.02× | 28 | +1,582.4 | +1,630.5 | 62.6% | 61/62 |
| 19 | DeepSeek V4.1 Flash (high) · Claude Code | 0.99× | 0.94–1.04× | 30 | +1,678.2 | +1,617.2 | 71.7% | 70/71 |
| 19 | DeepSeek V4.1 Flash (low) · Codex | 0.99× | 0.95–1.04× | 27 | +1,547.3 | +1,595.3 | 55.6% | 53/55 |
| 19 | DeepSeek V4.1 Flash (low) · Hermes | 0.99× | 0.93–1.07× | 30 | +1,608.9 | +1,580.8 | 69.7% | 66/69 |
| 22 | DeepSeek V4.1 Flash (low) · Claude Code | 1.00× | 0.94–1.06× | 29 | +1,706.1 | +1,649.4 | 69.7% | 67/69 |
| 22 | DeepSeek V4.1 Flash (low) · OpenCode | 1.00× | 0.92–1.10× | 23 | +1,527.4 | +1,402.0 | 47.5% | 44/47 |
| 22 | GLM-5.3 Flash (high) · pi | 1.00× | 0.94–1.04× | 28 | +1,610.2 | +1,567.7 | 63.6% | 63/63 |
| 22 | DeepSeek V4.1 Flash (low) · OpenCode 2 | 1.00× | 0.96–1.04× | 27 | +1,586.9 | +1,589.8 | 62.6% | 60/62 |
| 26 | DeepSeek V4.1 Flash (low) · Kimi Code | 1.02× | 0.95–1.10× | 27 | +1,772.0 | +1,723.3 | 62.6% | 60/62 |
| 26 | DeepSeek V4.1 Flash (high) · Kimi Code | 1.02× | 0.97–1.08× | 28 | +1,664.0 | +1,632.1 | 61.6% | 59/61 |
| 28 | GLM-5.3 Flash (high) · Hermes | 1.03× | 0.97–1.09× | 28 | +1,613.9 | +1,656.0 | 59.6% | 59/59 |
| 28 | GLM-5.3 Flash (low) · OpenClaw | 1.03× | 0.94–1.12× | 16 | +1,677.4 | +1,563.2 | 33.3% | 30/33 |
| 30 | GLM-5.3 Flash (high) · OpenCode | 1.05× | 0.99–1.13× | 21 | +1,670.3 | +1,540.1 | 35.4% | 35/35 |
| 31 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.06× | 1.00–1.12× | 27 | +1,763.5 | +1,771.0 | 62.6% | 62/62 |
| 32 | DeepSeek V4.1 Flash (high) · pi | 1.08× | 1.02–1.16× | 30 | +1,778.1 | +1,582.1 | 63.6% | 61/63 |
| 33 | DeepSeek V4.1 Flash (low) · pi | 1.09× | 1.03–1.17× | 29 | +1,793.8 | +1,677.8 | 64.6% | 62/64 |
| 34 | GLM-5.3 Flash (high) · OpenClaw | 1.11× | 1.06–1.18× | 20 | +1,644.5 | +1,664.9 | 39.4% | 39/39 |
| 35 | DeepSeek V4.1 Flash (high) · Hermes | 1.12× | 1.06–1.19× | 31 | +1,801.6 | +1,804.5 | 77.8% | 74/77 |
| 36 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.15× | 1.06–1.26× | 28 | +1,944.2 | +1,903.4 | 61.6% | 59/61 |
| 37 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.16× | 1.03–1.33× | 26 | +1,965.8 | +1,895.8 | 70.7% | 67/70 |
| 38 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.19× | 1.13–1.25× | 28 | +1,936.2 | +1,938.3 | 65.7% | 62/65 |
| — | DeepSeek V4.1 Flash (high) · OpenClaw | 1.26× | 1.04–1.58× | 9 | +1,898.0 | +485.1 | 13.1% | 10/13 |
| — | DeepSeek V4.1 Flash (low) · OpenClaw | 1.22× | 1.08–1.40× | 13 | +1,867.5 | +633.4 | 23.2% | 23/23 |
