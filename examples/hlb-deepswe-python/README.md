# DeepSWE, harness comparison: Python (33 tasks × 3 attempts, 65 setups)

The Python tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash at low and high effort, and Ripple-65B Preview, each in thirteen coding-agent harnesses, from Joel Niklaus's Harness Leaderboard (v0.1.11). Method, sources, caveats and reproduction are in that README; this folder is the Python board ([page](../../site/harnesses-python.html)).

- Dataset (items with reference solutions) SHA256 `faa57641002ef71ea2fb114a8e31b877cea62cf27b268c63845cb0f52791cc2d`; analyzer `0.11.0-beta`, commit `635dfc1`, Python 3.14.8.
- SHA256: [population.json](population.json) `9cac77c8…`, [score-panel.json](score-panel.json) `5af4db86…`, [scores.json](scores.json) `869811b3…`, [coverage.json](coverage.json) `aa583eb9…`, [sensitivity.json](sensitivity.json) `c8cf98c5…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · Codex | 0.83× | 0.78–0.89× | 19 | +1,416.6 | +1,337.2 | 30.3% | 29/30 |
| 2 | GLM-5.3 Flash (low) · Qwen Code | 0.86× | 0.82–0.90× | 26 | +1,423.6 | +1,382.5 | 45.5% | 45/45 |
| 3 | GLM-5.3 Flash (high) · Codex | 0.87× | 0.81–0.92× | 18 | +1,409.9 | +1,438.7 | 32.3% | 30/32 |
| 3 | GLM-5.3 Flash (low) · Grok Build | 0.87× | 0.82–0.91× | 29 | +1,472.2 | +1,439.6 | 52.5% | 52/52 |
| 5 | GLM-5.3 Flash (low) · pi | 0.89× | 0.85–0.92× | 29 | +1,430.4 | +1,463.4 | 55.6% | 54/55 |
| 6 | GLM-5.3 Flash (low) · fx | 0.90× | 0.86–0.93× | 25 | +1,436.9 | +1,477.1 | 51.5% | 51/51 |
| 7 | GLM-5.3 Flash (low) · Hermes | 0.90× | 0.85–0.95× | 24 | +1,462.7 | +1,502.6 | 50.5% | 48/50 |
| 7 | GLM-5.3 Flash (low) · Kimi Code | 0.90× | 0.86–0.94× | 27 | +1,543.1 | +1,436.6 | 54.5% | 52/54 |
| 9 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.91× | 0.87–0.94× | 28 | +1,470.3 | +1,456.5 | 61.6% | 59/61 |
| 9 | GLM-5.3 Flash (low) · Claude Code | 0.91× | 0.86–0.95× | 25 | +1,591.6 | +1,491.2 | 55.6% | 55/55 |
| 11 | GLM-5.3 Flash (low) · oh-my-pi | 0.91× | 0.85–0.98× | 23 | +1,401.4 | +1,439.8 | 43.4% | 42/43 |
| 12 | GLM-5.3 Flash (low) · OpenClaw | 0.91× | 0.88–0.94× | 25 | +1,459.0 | +1,482.6 | 52.5% | 51/52 |
| 13 | GLM-5.3 Flash (low) · OpenCode | 0.93× | 0.89–0.96× | 25 | +1,476.3 | +1,431.4 | 53.5% | 51/53 |
| 14 | DeepSeek V4.1 Flash (high) · Kimi Code | 0.93× | 0.89–0.97× | 29 | +1,471.2 | +1,548.6 | 61.6% | 59/61 |
| 15 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.93× | 0.89–0.96× | 27 | +1,481.2 | +1,527.1 | 58.6% | 55/58 |
| 16 | DeepSeek V4.1 Flash (low) · Hermes | 0.94× | 0.90–0.97× | 26 | +1,604.7 | +1,547.4 | 57.6% | 54/57 |
| 17 | DeepSeek V4.1 Flash (high) · oh-my-pi | 0.94× | 0.90–1.00× | 28 | +1,448.4 | +1,542.3 | 51.5% | 50/51 |
| 17 | GLM-5.3 Flash (high) · Qwen Code | 0.94× | 0.92–0.97× | 27 | +1,497.4 | +1,544.1 | 59.6% | 58/59 |
| 19 | GLM-5.3 Flash (high) · oh-my-pi | 0.95× | 0.91–0.98× | 27 | +1,500.0 | +1,533.9 | 59.6% | 58/59 |
| 20 | DeepSeek V4.1 Flash (high) · Codex | 0.95× | 0.90–0.99× | 28 | +1,534.5 | +1,549.0 | 64.6% | 60/64 |
| 21 | DeepSeek V4.1 Flash (high) · Grok Build | 0.95× | 0.91–0.99× | 29 | +1,603.1 | +1,598.1 | 60.6% | 58/60 |
| 22 | DeepSeek V4.1 Flash (low) · fx | 0.96× | 0.92–0.99× | 26 | +1,632.1 | +1,580.0 | 58.6% | 57/58 |
| 23 | DeepSeek V4.1 Flash (low) · Kimi Code | 0.96× | 0.92–1.01× | 26 | +1,619.8 | +1,547.3 | 62.6% | 60/62 |
| 24 | GLM-5.3 Flash (high) · Hermes | 0.96× | 0.92–1.00× | 26 | +1,608.0 | +1,604.0 | 53.5% | 53/53 |
| 25 | DeepSeek V4.1 Flash (high) · OpenCode | 0.96× | 0.91–1.01× | 27 | +1,548.6 | +1,646.7 | 55.6% | 53/55 |
| 26 | GLM-5.3 Flash (high) · Kimi Code | 0.96× | 0.92–1.01× | 29 | +1,482.1 | +1,587.0 | 63.6% | 61/63 |
| 27 | DeepSeek V4.1 Flash (high) · OpenClaw | 0.97× | 0.93–1.01× | 27 | +1,623.0 | +1,606.4 | 61.6% | 58/61 |
| 27 | DeepSeek V4.1 Flash (low) · Claude Code | 0.97× | 0.94–1.02× | 28 | +1,648.0 | +1,596.9 | 67.7% | 65/67 |
| 29 | GLM-5.3 Flash (high) · Grok Build | 0.97× | 0.94–1.01× | 29 | +1,552.5 | +1,613.1 | 69.7% | 68/69 |
| 30 | DeepSeek V4.1 Flash (low) · oh-my-pi | 0.97× | 0.92–1.04× | 26 | +1,554.1 | +1,549.0 | 54.5% | 52/54 |
| 31 | DeepSeek V4.1 Flash (low) · Grok Build | 0.97× | 0.95–1.01× | 27 | +1,631.1 | +1,655.2 | 64.6% | 63/64 |
| 32 | DeepSeek V4.1 Flash (low) · OpenClaw | 0.98× | 0.92–1.05× | 25 | +1,503.1 | +1,566.5 | 51.5% | 48/51 |
| 32 | DeepSeek V4.1 Flash (high) · Claude Code | 0.98× | 0.94–1.02× | 30 | +1,666.2 | +1,602.9 | 69.7% | 68/69 |
| 34 | GLM-5.3 Flash (high) · Claude Code | 0.98× | 0.94–1.02× | 27 | +1,527.5 | +1,592.1 | 65.7% | 64/65 |
| 35 | GLM-5.3 Flash (high) · fx | 0.99× | 0.95–1.02× | 29 | +1,595.7 | +1,561.1 | 67.7% | 66/67 |
| 35 | DeepSeek V4.1 Flash (high) · Hermes | 0.99× | 0.94–1.03× | 27 | +1,675.5 | +1,606.9 | 58.6% | 55/58 |
| 37 | DeepSeek V4.1 Flash (high) · fx | 0.99× | 0.96–1.01× | 26 | +1,664.9 | +1,671.2 | 60.6% | 57/60 |
| 38 | GLM-5.3 Flash (high) · OpenCode | 0.99× | 0.94–1.03× | 28 | +1,582.4 | +1,630.5 | 62.6% | 61/62 |
| 39 | DeepSeek V4.1 Flash (low) · OpenCode | 1.00× | 0.97–1.03× | 27 | +1,586.9 | +1,589.8 | 62.6% | 60/62 |
| 39 | GLM-5.3 Flash (high) · pi | 1.00× | 0.95–1.04× | 28 | +1,610.2 | +1,567.7 | 63.6% | 63/63 |
| 41 | DeepSeek V4.1 Flash (low) · Codex | 1.00× | 0.96–1.03× | 27 | +1,547.3 | +1,590.8 | 55.6% | 53/55 |
| 42 | DeepSeek V4.1 Flash (low) · DeepSeek Harness | 1.01× | 0.97–1.05× | 25 | +1,669.4 | +1,672.0 | 53.5% | 52/53 |
| 43 | GLM-5.3 Flash (high) · OpenClaw | 1.01× | 0.95–1.08× | 28 | +1,598.8 | +1,657.3 | 62.6% | 61/62 |
| 44 | DeepSeek V4.1 Flash (high) · pi | 1.01× | 0.98–1.05× | 29 | +1,729.3 | +1,524.2 | 56.6% | 55/56 |
| 45 | GLM-5.3 Flash (low) · DeepSeek Harness | 1.01× | 0.97–1.06× | 27 | +1,713.3 | +1,635.0 | 55.6% | 55/55 |
| 46 | DeepSeek V4.1 Flash (high) · DeepSeek Harness | 1.02× | 0.98–1.07× | 28 | +1,696.0 | +1,726.5 | 66.7% | 63/66 |
| 47 | DeepSeek V4.1 Flash (low) · pi | 1.03× | 0.97–1.09× | 24 | +1,716.6 | +1,589.6 | 56.6% | 55/56 |
| 48 | Ripple-65B Preview · oh-my-pi | 1.05× | 0.97–1.15× | 19 | +1,787.4 | +1,701.6 | 37.4% | 35/37 |
| 49 | GLM-5.3 Flash (high) · DeepSeek Harness | 1.07× | 1.02–1.14× | 29 | +1,726.1 | +1,783.6 | 71.7% | 71/71 |
| 49 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.07× | 1.01–1.13× | 27 | +1,763.5 | +1,771.0 | 62.6% | 62/62 |
| 51 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.07× | 1.01–1.14× | 25 | +1,769.8 | +1,813.5 | 67.7% | 65/67 |
| 52 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.08× | 1.02–1.15× | 26 | +1,809.6 | +1,790.7 | 55.6% | 54/55 |
| 53 | Ripple-65B Preview · OpenClaw | 1.09× | 1.02–1.17× | 22 | +1,821.1 | +1,136.5 | 28.3% | 27/28 |
| 54 | Ripple-65B Preview · OpenCode | 1.09× | 1.04–1.16× | 24 | +1,884.8 | +1,823.0 | 45.5% | 43/45 |
| 55 | Ripple-65B Preview · fx | 1.10× | 1.05–1.16× | 20 | +1,759.6 | +1,603.9 | 40.4% | 37/40 |
| 56 | Ripple-65B Preview · Qwen Code | 1.10× | 1.03–1.20× | 20 | +1,823.4 | +1,533.6 | 31.3% | 28/31 |
| 57 | Ripple-65B Preview · Grok Build | 1.12× | 1.08–1.17× | 21 | +2,000.1 | +1,852.5 | 45.5% | 42/45 |
| 58 | Ripple-65B Preview · DeepSeek Harness | 1.13× | 1.06–1.21× | 18 | +1,996.8 | +1,240.3 | 36.4% | 34/36 |
| 59 | Ripple-65B Preview · Kimi Code | 1.14× | 1.08–1.20× | 23 | +1,835.7 | +1,804.6 | 48.5% | 46/48 |
| 60 | Ripple-65B Preview · pi | 1.14× | 1.07–1.21× | 22 | +1,831.7 | +1,579.2 | 44.4% | 41/44 |
| 61 | Ripple-65B Preview · Hermes | 1.19× | 1.12–1.26× | 23 | +1,873.5 | +1,977.4 | 51.5% | 49/51 |
| 62 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.20× | 1.14–1.26× | 27 | +1,943.0 | +1,938.9 | 64.6% | 61/64 |
| 63 | Ripple-65B Preview · Codex | 1.23× | 1.16–1.31× | 24 | +2,038.5 | +1,924.7 | 48.5% | 46/48 |
| 64 | Ripple-65B Preview · Claude Code | 1.23× | 1.13–1.35× | 22 | +1,967.3 | +1,905.9 | 48.5% | 46/48 |
| 65 | Ripple-65B Preview · mini-SWE-agent | 1.50× | 1.33–1.71× | 19 | +2,684.3 | +1,547.8 | 31.3% | 29/31 |
