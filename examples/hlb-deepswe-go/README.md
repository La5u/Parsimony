# DeepSWE, harness comparison: Go (33 tasks × 3 attempts, 65 setups)

The Go tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash at low and high effort, and Ripple-65B Preview, each in thirteen coding-agent harnesses, from Joel Niklaus's Harness Leaderboard (v0.1.11). Method, sources, caveats and reproduction are in that README; this folder is the Go board ([page](../../site/harnesses-go.html)).

- Dataset (items with reference solutions) SHA256 `8f4416a8e8dfea22bfcf9258bb9bcb401f3f7a9bc3f14ca9ce5b79915cf74769`; analyzer `0.11.0-beta`, commit `635dfc1`, Python 3.14.8.
- SHA256: [population.json](population.json) `3d62b0d2…`, [score-panel.json](score-panel.json) `57d48d43…`, [scores.json](scores.json) `d4065ded…`, [coverage.json](coverage.json) `8333af4f…`, [sensitivity.json](sensitivity.json) `1c543668…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · Codex | 0.87× | 0.81–0.96× | 19 | +2,721.4 | +2,772.3 | 28.3% | 28/28 |
| 2 | GLM-5.3 Flash (low) · oh-my-pi | 0.90× | 0.86–0.94× | 25 | +2,990.4 | +2,778.9 | 45.5% | 45/45 |
| 3 | GLM-5.3 Flash (low) · pi | 0.91× | 0.87–0.95× | 25 | +3,118.5 | +2,765.0 | 51.5% | 51/51 |
| 4 | GLM-5.3 Flash (high) · oh-my-pi | 0.91× | 0.88–0.94× | 29 | +3,098.6 | +2,865.6 | 63.6% | 63/63 |
| 5 | GLM-5.3 Flash (low) · OpenCode | 0.92× | 0.88–0.95× | 28 | +3,172.2 | +2,797.4 | 60.6% | 60/60 |
| 6 | GLM-5.3 Flash (low) · Kimi Code | 0.92× | 0.89–0.95× | 27 | +2,933.7 | +2,869.6 | 56.6% | 56/56 |
| 7 | GLM-5.3 Flash (low) · Grok Build | 0.92× | 0.89–0.95× | 28 | +3,133.4 | +2,858.8 | 59.6% | 59/59 |
| 7 | GLM-5.3 Flash (low) · Hermes | 0.92× | 0.88–0.96× | 29 | +3,147.4 | +2,842.4 | 58.6% | 58/58 |
| 9 | DeepSeek V4.1 Flash (high) · Codex | 0.92× | 0.87–0.97× | 29 | +3,022.0 | +2,873.7 | 68.7% | 68/68 |
| 10 | GLM-5.3 Flash (high) · Qwen Code | 0.93× | 0.89–0.96× | 27 | +2,865.4 | +2,793.6 | 55.6% | 55/55 |
| 10 | DeepSeek V4.1 Flash (low) · Hermes | 0.93× | 0.89–0.96× | 27 | +3,067.8 | +2,857.0 | 60.6% | 60/60 |
| 10 | GLM-5.3 Flash (low) · OpenClaw | 0.93× | 0.90–0.96× | 29 | +3,087.5 | +2,911.9 | 57.6% | 57/57 |
| 13 | GLM-5.3 Flash (low) · Qwen Code | 0.93× | 0.88–0.98× | 26 | +2,916.6 | +2,750.6 | 52.5% | 52/52 |
| 14 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.93× | 0.89–0.97× | 29 | +2,987.5 | +2,875.5 | 66.7% | 66/66 |
| 15 | DeepSeek V4.1 Flash (low) · oh-my-pi | 0.93× | 0.89–0.97× | 29 | +3,028.5 | +2,877.9 | 65.7% | 65/65 |
| 16 | DeepSeek V4.1 Flash (low) · OpenClaw | 0.93× | 0.90–0.97× | 29 | +2,946.1 | +2,799.7 | 62.6% | 62/62 |
| 17 | GLM-5.3 Flash (low) · fx | 0.94× | 0.90–0.97× | 28 | +3,024.9 | +2,790.4 | 57.6% | 57/57 |
| 18 | DeepSeek V4.1 Flash (high) · Claude Code | 0.94× | 0.89–0.98× | 32 | +2,940.8 | +2,906.1 | 72.7% | 72/72 |
| 18 | GLM-5.3 Flash (low) · Claude Code | 0.94× | 0.91–0.98× | 27 | +3,084.5 | +2,842.2 | 59.6% | 59/59 |
| 20 | GLM-5.3 Flash (high) · Codex | 0.94× | 0.91–0.99× | 22 | +3,072.5 | +2,827.0 | 40.4% | 40/40 |
| 20 | DeepSeek V4.1 Flash (low) · Codex | 0.94× | 0.92–0.97× | 29 | +3,073.5 | +2,922.3 | 69.7% | 69/69 |
| 22 | DeepSeek V4.1 Flash (low) · Grok Build | 0.95× | 0.92–0.98× | 31 | +2,945.0 | +2,920.2 | 72.7% | 72/72 |
| 22 | GLM-5.3 Flash (high) · pi | 0.95× | 0.92–0.98× | 29 | +3,075.8 | +2,928.0 | 68.7% | 68/68 |
| 24 | DeepSeek V4.1 Flash (low) · Kimi Code | 0.95× | 0.92–1.00× | 28 | +2,937.8 | +2,925.3 | 67.7% | 67/67 |
| 25 | DeepSeek V4.1 Flash (low) · pi | 0.95× | 0.92–0.99× | 30 | +2,932.8 | +2,830.1 | 66.7% | 66/66 |
| 26 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.96× | 0.92–0.99× | 30 | +2,846.0 | +2,902.8 | 61.6% | 61/61 |
| 27 | DeepSeek V4.1 Flash (high) · pi | 0.96× | 0.94–0.99× | 27 | +3,030.1 | +2,770.6 | 63.6% | 63/63 |
| 28 | DeepSeek V4.1 Flash (low) · Claude Code | 0.97× | 0.92–1.00× | 29 | +3,207.7 | +2,934.9 | 70.7% | 70/70 |
| 29 | GLM-5.3 Flash (high) · OpenCode | 0.97× | 0.93–1.02× | 31 | +3,261.4 | +3,021.1 | 65.7% | 65/65 |
| 30 | DeepSeek V4.1 Flash (low) · fx | 0.97× | 0.92–1.02× | 29 | +3,059.2 | +2,942.6 | 65.7% | 65/65 |
| 30 | DeepSeek V4.1 Flash (high) · Hermes | 0.97× | 0.94–1.00× | 30 | +3,097.2 | +2,985.9 | 71.7% | 71/71 |
| 32 | DeepSeek V4.1 Flash (high) · Kimi Code | 0.97× | 0.94–1.01× | 31 | +2,959.3 | +2,892.9 | 62.6% | 62/62 |
| 33 | DeepSeek V4.1 Flash (high) · OpenClaw | 0.98× | 0.94–1.01× | 32 | +3,094.8 | +3,042.5 | 75.8% | 75/75 |
| 33 | GLM-5.3 Flash (high) · Grok Build | 0.98× | 0.95–1.01× | 27 | +3,136.7 | +3,027.9 | 60.6% | 60/60 |
| 35 | DeepSeek V4.1 Flash (high) · fx | 0.98× | 0.94–1.03× | 29 | +2,972.0 | +3,001.4 | 66.7% | 66/66 |
| 36 | DeepSeek V4.1 Flash (high) · oh-my-pi | 0.99× | 0.96–1.03× | 29 | +3,170.1 | +2,967.3 | 69.7% | 69/69 |
| 37 | GLM-5.3 Flash (high) · Kimi Code | 0.99× | 0.94–1.05× | 30 | +3,084.0 | +3,102.8 | 69.7% | 69/69 |
| 38 | DeepSeek V4.1 Flash (high) · OpenCode | 0.99× | 0.96–1.02× | 31 | +3,143.7 | +3,033.4 | 75.8% | 75/75 |
| 39 | GLM-5.3 Flash (low) · DeepSeek Harness | 1.00× | 0.96–1.04× | 28 | +3,258.0 | +3,081.9 | 65.7% | 65/65 |
| 40 | GLM-5.3 Flash (high) · Claude Code | 1.00× | 0.96–1.06× | 30 | +3,159.1 | +3,012.8 | 66.7% | 66/66 |
| 41 | GLM-5.3 Flash (high) · OpenClaw | 1.00× | 0.96–1.06× | 26 | +3,282.9 | +3,145.0 | 58.6% | 58/58 |
| 41 | DeepSeek V4.1 Flash (high) · Grok Build | 1.00× | 0.93–1.08× | 29 | +3,385.9 | +3,149.3 | 74.7% | 74/74 |
| 43 | GLM-5.3 Flash (high) · fx | 1.01× | 0.97–1.05× | 31 | +3,348.7 | +3,125.6 | 66.7% | 66/66 |
| 44 | DeepSeek V4.1 Flash (low) · OpenCode | 1.01× | 0.95–1.10× | 29 | +3,202.7 | +3,082.6 | 76.8% | 76/76 |
| 45 | DeepSeek V4.1 Flash (high) · DeepSeek Harness | 1.02× | 1.00–1.05× | 30 | +3,154.2 | +3,163.1 | 73.7% | 73/73 |
| 46 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.02× | 0.98–1.07× | 30 | +3,480.3 | +3,112.1 | 61.6% | 61/61 |
| 47 | Ripple-65B Preview · Qwen Code | 1.03× | 0.96–1.10× | 25 | +3,148.9 | +2,663.9 | 38.4% | 38/38 |
| 48 | GLM-5.3 Flash (high) · Hermes | 1.05× | 0.97–1.14× | 29 | +3,367.0 | +3,183.8 | 66.7% | 66/66 |
| 49 | DeepSeek V4.1 Flash (low) · DeepSeek Harness | 1.06× | 0.98–1.19× | 31 | +3,237.4 | +3,194.6 | 82.8% | 82/82 |
| 49 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.06× | 1.01–1.11× | 29 | +3,461.8 | +3,306.7 | 70.7% | 70/70 |
| 51 | Ripple-65B Preview · fx | 1.06× | 1.02–1.11× | 24 | +3,044.4 | +2,647.5 | 42.4% | 42/42 |
| 52 | GLM-5.3 Flash (high) · DeepSeek Harness | 1.07× | 1.01–1.13× | 28 | +3,307.7 | +3,262.8 | 61.6% | 61/61 |
| 53 | Ripple-65B Preview · Grok Build | 1.09× | 1.03–1.14× | 27 | +3,281.8 | +3,278.9 | 51.5% | 51/51 |
| 54 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.09× | 1.04–1.14× | 28 | +3,530.8 | +3,349.8 | 62.6% | 62/62 |
| 55 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.10× | 1.05–1.16× | 30 | +3,661.4 | +3,404.9 | 65.7% | 65/65 |
| 56 | Ripple-65B Preview · Hermes | 1.11× | 1.03–1.19× | 29 | +3,567.8 | +3,871.2 | 49.5% | 49/49 |
| 57 | Ripple-65B Preview · pi | 1.11× | 1.04–1.18× | 26 | +3,282.4 | +3,284.5 | 44.4% | 44/44 |
| 57 | Ripple-65B Preview · Kimi Code | 1.11× | 1.04–1.18× | 25 | +3,298.9 | +3,521.9 | 47.5% | 47/47 |
| 59 | Ripple-65B Preview · OpenCode | 1.12× | 1.05–1.19× | 26 | +3,643.4 | +3,377.2 | 52.5% | 52/52 |
| 60 | Ripple-65B Preview · oh-my-pi | 1.14× | 1.06–1.22× | 28 | +3,450.7 | +3,094.2 | 45.5% | 45/45 |
| 61 | Ripple-65B Preview · DeepSeek Harness | 1.15× | 1.10–1.20× | 24 | +3,550.6 | +2,608.8 | 45.5% | 45/45 |
| 62 | Ripple-65B Preview · OpenClaw | 1.16× | 1.07–1.27× | 19 | +3,148.7 | +1,947.3 | 32.3% | 32/32 |
| 63 | Ripple-65B Preview · Claude Code | 1.22× | 1.13–1.33× | 25 | +3,696.6 | +3,635.2 | 46.5% | 46/46 |
| 64 | Ripple-65B Preview · Codex | 1.23× | 1.16–1.30× | 27 | +3,623.9 | +3,217.8 | 54.5% | 54/54 |
| 65 | Ripple-65B Preview · mini-SWE-agent | 1.31× | 1.23–1.39× | 20 | +3,794.1 | +2,350.5 | 40.4% | 40/40 |
