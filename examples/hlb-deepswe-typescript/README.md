# DeepSWE, harness comparison: TypeScript (35 tasks × 3 attempts, 65 setups)

The TypeScript tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash at low and high effort, and Ripple-65B Preview, each in thirteen coding-agent harnesses, from Joel Niklaus's Harness Leaderboard (v0.1.11). Method, sources, caveats and reproduction are in that README; this folder is the TypeScript board ([page](../../site/harnesses-typescript.html)).

- Dataset (items with reference solutions) SHA256 `2f1b3486539845cc3319dc4ed52353c1c7dab4413825293ab171c71a22ddc189`; analyzer `0.11.0-beta`, commit `635dfc1`, Python 3.14.8.
- SHA256: [population.json](population.json) `621c51a8…`, [score-panel.json](score-panel.json) `3c173c71…`, [scores.json](scores.json) `278b00a8…`, [coverage.json](coverage.json) `74e47a7b…`, [sensitivity.json](sensitivity.json) `09c5bc24…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (high) · Codex | 0.86× | 0.80–0.93× | 22 | +1,930.2 | +1,896.1 | 34.3% | 35/36 |
| 2 | GLM-5.3 Flash (low) · Qwen Code | 0.88× | 0.82–0.93× | 25 | +2,063.7 | +1,823.3 | 45.7% | 45/48 |
| 3 | GLM-5.3 Flash (low) · Grok Build | 0.89× | 0.85–0.93× | 25 | +1,854.8 | +1,928.6 | 58.1% | 58/61 |
| 4 | DeepSeek V4.1 Flash (low) · fx | 0.91× | 0.86–0.95× | 26 | +1,850.2 | +1,907.6 | 54.3% | 53/57 |
| 5 | DeepSeek V4.1 Flash (low) · Kimi Code | 0.91× | 0.86–0.95× | 29 | +1,933.8 | +2,026.7 | 58.1% | 57/61 |
| 6 | GLM-5.3 Flash (low) · fx | 0.92× | 0.88–0.96× | 26 | +1,873.3 | +1,901.0 | 54.3% | 53/57 |
| 7 | GLM-5.3 Flash (low) · pi | 0.92× | 0.87–0.96× | 24 | +2,023.5 | +1,954.7 | 52.4% | 50/55 |
| 8 | GLM-5.3 Flash (low) · oh-my-pi | 0.92× | 0.86–0.96× | 26 | +1,948.0 | +1,980.8 | 48.6% | 48/51 |
| 9 | DeepSeek V4.1 Flash (low) · oh-my-pi | 0.92× | 0.88–0.97× | 23 | +1,825.6 | +1,985.8 | 51.4% | 49/54 |
| 10 | GLM-5.3 Flash (low) · Hermes | 0.92× | 0.88–0.96× | 23 | +2,008.6 | +1,859.6 | 50.5% | 49/53 |
| 11 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.93× | 0.89–0.97× | 23 | +1,904.4 | +1,973.3 | 50.5% | 51/53 |
| 12 | GLM-5.3 Flash (low) · OpenCode | 0.94× | 0.89–0.98× | 28 | +1,944.4 | +1,982.7 | 54.3% | 54/57 |
| 13 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.94× | 0.89–0.99× | 26 | +1,856.6 | +1,978.3 | 57.1% | 56/60 |
| 13 | GLM-5.3 Flash (low) · Kimi Code | 0.94× | 0.87–1.01× | 23 | +1,966.3 | +1,998.5 | 44.8% | 46/47 |
| 15 | DeepSeek V4.1 Flash (high) · oh-my-pi | 0.94× | 0.88–0.99× | 23 | +1,902.8 | +2,015.8 | 46.7% | 47/49 |
| 16 | GLM-5.3 Flash (low) · Claude Code | 0.94× | 0.88–1.00× | 24 | +2,001.3 | +2,047.6 | 54.3% | 54/57 |
| 17 | DeepSeek V4.1 Flash (low) · OpenCode | 0.95× | 0.91–0.99× | 24 | +1,889.9 | +2,078.7 | 61.9% | 61/65 |
| 18 | GLM-5.3 Flash (high) · pi | 0.95× | 0.90–1.00× | 22 | +2,161.4 | +2,140.5 | 51.4% | 52/54 |
| 19 | GLM-5.3 Flash (low) · OpenClaw | 0.95× | 0.92–1.00× | 24 | +1,939.7 | +1,949.7 | 49.5% | 50/52 |
| 20 | DeepSeek V4.1 Flash (low) · Claude Code | 0.96× | 0.91–1.01× | 24 | +1,955.9 | +2,130.7 | 57.1% | 56/60 |
| 21 | DeepSeek V4.1 Flash (low) · Hermes | 0.96× | 0.89–1.07× | 20 | +1,787.8 | +2,022.4 | 45.7% | 45/48 |
| 22 | GLM-5.3 Flash (high) · Grok Build | 0.96× | 0.92–1.01× | 24 | +2,247.9 | +2,113.3 | 60.0% | 59/63 |
| 23 | DeepSeek V4.1 Flash (high) · Grok Build | 0.97× | 0.93–1.00× | 26 | +2,078.7 | +2,100.1 | 61.9% | 60/65 |
| 23 | GLM-5.3 Flash (high) · Claude Code | 0.97× | 0.92–1.01× | 24 | +2,156.8 | +2,116.4 | 51.4% | 51/54 |
| 25 | DeepSeek V4.1 Flash (low) · Codex | 0.97× | 0.91–1.03× | 29 | +2,008.4 | +2,034.3 | 61.0% | 59/64 |
| 26 | GLM-5.3 Flash (high) · oh-my-pi | 0.97× | 0.92–1.02× | 23 | +2,140.2 | +2,040.0 | 51.4% | 49/54 |
| 27 | DeepSeek V4.1 Flash (low) · pi | 0.97× | 0.91–1.04× | 22 | +2,064.5 | +2,219.0 | 52.4% | 51/55 |
| 28 | DeepSeek V4.1 Flash (high) · OpenClaw | 0.98× | 0.93–1.02× | 26 | +2,015.5 | +2,028.0 | 51.4% | 52/54 |
| 29 | GLM-5.3 Flash (low) · DeepSeek Harness | 0.98× | 0.96–1.00× | 23 | +2,093.3 | +2,109.6 | 53.3% | 52/56 |
| 30 | DeepSeek V4.1 Flash (high) · Kimi Code | 0.98× | 0.95–1.01× | 29 | +2,002.7 | +2,057.5 | 58.1% | 59/61 |
| 31 | GLM-5.3 Flash (high) · Qwen Code | 0.98× | 0.94–1.03× | 23 | +2,192.2 | +2,091.7 | 51.4% | 51/54 |
| 32 | DeepSeek V4.1 Flash (high) · OpenCode | 0.98× | 0.94–1.02× | 27 | +2,074.9 | +2,096.4 | 62.9% | 63/66 |
| 32 | DeepSeek V4.1 Flash (low) · Grok Build | 0.98× | 0.94–1.02× | 26 | +2,155.5 | +2,122.7 | 56.2% | 56/59 |
| 34 | DeepSeek V4.1 Flash (low) · OpenClaw | 0.99× | 0.92–1.07× | 27 | +1,995.1 | +2,061.0 | 52.4% | 52/55 |
| 34 | DeepSeek V4.1 Flash (high) · Claude Code | 0.99× | 0.95–1.03× | 23 | +2,099.1 | +2,140.1 | 55.2% | 52/58 |
| 36 | GLM-5.3 Flash (high) · Kimi Code | 0.99× | 0.92–1.06× | 24 | +1,939.5 | +2,158.6 | 53.3% | 53/56 |
| 37 | DeepSeek V4.1 Flash (low) · DeepSeek Harness | 0.99× | 0.92–1.05× | 27 | +2,078.7 | +2,164.6 | 61.0% | 60/64 |
| 38 | Ripple-65B Preview · oh-my-pi | 0.99× | 0.93–1.05× | 16 | +1,806.9 | +1,934.2 | 25.7% | 26/27 |
| 39 | DeepSeek V4.1 Flash (high) · Hermes | 1.00× | 0.95–1.04× | 23 | +2,150.1 | +2,141.8 | 55.2% | 54/58 |
| 40 | DeepSeek V4.1 Flash (high) · pi | 1.00× | 0.94–1.06× | 27 | +1,979.9 | +1,940.2 | 55.2% | 55/58 |
| 41 | DeepSeek V4.1 Flash (high) · fx | 1.01× | 0.93–1.09× | 25 | +2,043.0 | +1,992.9 | 54.3% | 53/57 |
| 42 | DeepSeek V4.1 Flash (high) · DeepSeek Harness | 1.01× | 0.97–1.05× | 27 | +2,105.6 | +2,212.4 | 64.8% | 64/68 |
| 43 | GLM-5.3 Flash (high) · OpenCode | 1.01× | 0.97–1.06× | 26 | +2,205.7 | +2,104.4 | 54.3% | 52/57 |
| 44 | GLM-5.3 Flash (high) · fx | 1.02× | 0.98–1.07× | 25 | +2,350.4 | +2,133.8 | 53.3% | 50/56 |
| 45 | DeepSeek V4.1 Flash (high) · Codex | 1.02× | 0.95–1.10× | 28 | +2,030.7 | +2,129.2 | 58.1% | 58/61 |
| 46 | GLM-5.3 Flash (high) · OpenClaw | 1.03× | 0.97–1.09× | 24 | +2,275.6 | +2,124.9 | 55.2% | 54/58 |
| 47 | GLM-5.3 Flash (high) · Hermes | 1.03× | 0.96–1.10× | 29 | +2,266.6 | +2,191.0 | 57.1% | 57/60 |
| 48 | GLM-5.3 Flash (high) · DeepSeek Harness | 1.03× | 0.97–1.09× | 23 | +2,243.2 | +2,293.3 | 58.1% | 58/61 |
| 49 | Ripple-65B Preview · fx | 1.04× | 0.97–1.13× | 21 | +2,090.6 | +1,725.8 | 35.2% | 33/37 |
| 50 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.05× | 0.99–1.10× | 22 | +1,957.8 | +2,280.3 | 44.8% | 43/47 |
| 51 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.06× | 1.00–1.14× | 28 | +2,226.0 | +2,600.7 | 61.9% | 60/65 |
| 52 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.07× | 1.00–1.16× | 25 | +2,251.9 | +2,463.1 | 60.0% | 57/63 |
| 53 | Ripple-65B Preview · Grok Build | 1.09× | 1.03–1.16× | 19 | +2,112.3 | +2,375.1 | 37.1% | 36/39 |
| 54 | Ripple-65B Preview · Qwen Code | 1.10× | 0.99–1.21× | 15 | +1,806.7 | +1,707.2 | 23.8% | 23/25 |
| 55 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.12× | 1.07–1.18× | 27 | +2,337.3 | +2,423.3 | 56.2% | 56/59 |
| 56 | Ripple-65B Preview · Kimi Code | 1.16× | 1.09–1.27× | 23 | +2,041.6 | +2,552.8 | 51.4% | 49/54 |
| 57 | Ripple-65B Preview · pi | 1.17× | 1.08–1.30× | 22 | +2,308.5 | +2,471.8 | 41.9% | 39/44 |
| 58 | Ripple-65B Preview · Hermes | 1.18× | 1.11–1.27× | 24 | +2,273.2 | +2,564.5 | 44.8% | 43/47 |
| 59 | Ripple-65B Preview · Codex | 1.26× | 1.16–1.37× | 23 | +2,251.1 | +2,375.4 | 44.8% | 42/47 |
| 60 | Ripple-65B Preview · Claude Code | 1.26× | 1.17–1.41× | 17 | +1,917.6 | +2,219.4 | 30.5% | 28/32 |
| 61 | Ripple-65B Preview · OpenCode | 1.29× | 1.13–1.49× | 23 | +2,318.2 | +2,453.9 | 42.9% | 40/45 |
| — | GLM-5.3 Flash (low) · Codex | 0.82× | 0.73–0.89× | 13 | +1,314.8 | +1,778.9 | 23.8% | 21/25 |
| — | Ripple-65B Preview · OpenClaw | 1.10× | 1.01–1.24× | 10 | +1,554.0 | +954.1 | 14.3% | 13/15 |
| — | Ripple-65B Preview · DeepSeek Harness | 1.23× | 1.13–1.36× | 14 | +1,709.2 | +1,058.5 | 32.4% | 31/34 |
| — | Ripple-65B Preview · mini-SWE-agent | 1.37× | 1.21–1.55× | 14 | +1,826.4 | +829.7 | 26.7% | 23/28 |
