# DeepSWE, harness comparison: TypeScript (35 tasks × 3 attempts, 40 setups)

The TypeScript tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash, low and high effort, in ten coding-agent harnesses (OpenCode 1.19.0 and 2.2.6 separately), from Joel Niklaus's Harness Leaderboard. Method, sources, caveats and reproduction are in that README; this folder is the TypeScript board ([page](../../site/harnesses-typescript.html)).

- Dataset (items with reference solutions) SHA256 `2f1b3486539845cc3319dc4ed52353c1c7dab4413825293ab171c71a22ddc189`; analyzer `0.11.0-beta`, commit `e12a096` (remeasured 2026-11-10 for the TypeScript scope change: `dtslint/` and `*.tst.ts` type tests excluded; 8 of 4,200 records changed). The other languages stay at `0.10.0-beta`.
- SHA256: [population.json](population.json) `747ab510…`, [score-panel.json](score-panel.json) `12fb9859…`, [scores.json](scores.json) `5498277f…`, [coverage.json](coverage.json) `3795ea09…`, [sensitivity.json](sensitivity.json) `8967ef6f…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (high) · Codex | 0.85× | 0.79–0.93× | 22 | +1,930.2 | +1,896.1 | 34.3% | 35/36 |
| 2 | GLM-5.3 Flash (low) · Qwen Code | 0.87× | 0.80–0.93× | 25 | +2,063.7 | +1,823.3 | 45.7% | 45/48 |
| 3 | GLM-5.3 Flash (low) · Kimi Code | 0.91× | 0.85–0.96× | 21 | +1,843.7 | +1,918.4 | 42.9% | 42/45 |
| 4 | GLM-5.3 Flash (low) · pi | 0.92× | 0.87–0.96× | 23 | +2,018.2 | +1,931.6 | 51.4% | 49/54 |
| 5 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.93× | 0.89–0.96× | 24 | +1,852.8 | +2,041.7 | 58.1% | 57/61 |
| 6 | GLM-5.3 Flash (low) · OpenCode 2 | 0.94× | 0.89–0.98× | 28 | +1,944.4 | +1,982.7 | 54.3% | 54/57 |
| 7 | GLM-5.3 Flash (low) · Hermes | 0.95× | 0.88–1.00× | 19 | +1,939.2 | +2,052.5 | 42.9% | 41/45 |
| 7 | GLM-5.3 Flash (low) · Claude Code | 0.95× | 0.89–1.00× | 24 | +1,994.3 | +2,043.8 | 54.3% | 54/57 |
| 7 | GLM-5.3 Flash (low) · OpenCode | 0.95× | 0.89–1.03× | 18 | +1,785.4 | +1,727.9 | 35.2% | 34/37 |
| 7 | GLM-5.3 Flash (high) · pi | 0.95× | 0.89–1.01× | 22 | +2,152.7 | +2,135.9 | 51.4% | 52/54 |
| 11 | DeepSeek V4.1 Flash (low) · OpenCode 2 | 0.97× | 0.91–1.02× | 24 | +1,889.9 | +2,078.7 | 61.9% | 61/65 |
| 11 | GLM-5.3 Flash (high) · Claude Code | 0.97× | 0.92–1.02× | 24 | +2,175.2 | +2,125.9 | 51.4% | 51/54 |
| 13 | DeepSeek V4.1 Flash (low) · Codex | 0.98× | 0.92–1.04× | 29 | +2,008.4 | +2,013.9 | 61.0% | 59/64 |
| 13 | DeepSeek V4.1 Flash (low) · Kimi Code | 0.98× | 0.93–1.04× | 30 | +2,005.6 | +2,065.4 | 64.8% | 65/68 |
| 13 | GLM-5.3 Flash (high) · Qwen Code | 0.98× | 0.94–1.03× | 23 | +2,192.2 | +2,091.7 | 51.4% | 51/54 |
| 13 | DeepSeek V4.1 Flash (high) · OpenCode 2 | 0.98× | 0.95–1.02× | 27 | +2,074.9 | +2,096.4 | 62.9% | 63/66 |
| 17 | GLM-5.3 Flash (high) · OpenCode | 0.99× | 0.92–1.05× | 15 | +2,067.6 | +1,456.7 | 30.5% | 27/32 |
| 17 | DeepSeek V4.1 Flash (low) · Claude Code | 0.99× | 0.94–1.03× | 24 | +1,999.5 | +2,155.4 | 57.1% | 56/60 |
| 17 | DeepSeek V4.1 Flash (high) · Claude Code | 0.99× | 0.95–1.04× | 24 | +2,081.6 | +2,142.2 | 57.1% | 54/60 |
| 17 | GLM-5.3 Flash (low) · OpenClaw | 0.99× | 0.93–1.06× | 17 | +2,083.3 | +1,978.9 | 28.6% | 27/30 |
| 17 | DeepSeek V4.1 Flash (low) · OpenCode | 0.99× | 0.96–1.03× | 22 | +2,121.5 | +1,797.9 | 50.5% | 47/53 |
| 22 | DeepSeek V4.1 Flash (low) · Hermes | 1.01× | 0.97–1.06× | 31 | +2,190.2 | +2,154.1 | 70.5% | 70/74 |
| 22 | DeepSeek V4.1 Flash (high) · pi | 1.01× | 0.93–1.12× | 28 | +2,054.4 | +1,929.1 | 58.1% | 58/61 |
| 22 | DeepSeek V4.1 Flash (high) · Codex | 1.01× | 0.94–1.09× | 28 | +2,030.7 | +2,129.2 | 58.1% | 58/61 |
| 22 | DeepSeek V4.1 Flash (high) · Kimi Code | 1.01× | 0.96–1.08× | 26 | +2,084.4 | +2,159.8 | 55.2% | 55/58 |
| 26 | DeepSeek V4.1 Flash (high) · OpenCode | 1.02× | 0.97–1.07× | 19 | +2,078.7 | +1,653.7 | 45.7% | 43/48 |
| 26 | GLM-5.3 Flash (high) · Hermes | 1.02× | 0.96–1.08× | 25 | +2,065.0 | +2,118.2 | 53.3% | 53/56 |
| 26 | GLM-5.3 Flash (high) · Kimi Code | 1.02× | 0.96–1.10× | 26 | +2,193.1 | +2,161.4 | 61.9% | 61/65 |
| 26 | GLM-5.3 Flash (high) · OpenCode 2 | 1.02× | 0.96–1.07× | 26 | +2,205.7 | +2,104.4 | 54.3% | 52/57 |
| 30 | DeepSeek V4.1 Flash (high) · Hermes | 1.03× | 0.96–1.12× | 30 | +2,164.2 | +2,245.1 | 70.5% | 69/74 |
| 30 | DeepSeek V4.1 Flash (low) · Qwen Code | 1.03× | 0.94–1.18× | 27 | +2,198.7 | +2,119.2 | 57.1% | 56/60 |
| 32 | DeepSeek V4.1 Flash (low) · pi | 1.05× | 0.96–1.18× | 25 | +2,082.8 | +2,202.1 | 56.2% | 55/59 |
| 32 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.05× | 1.00–1.11× | 22 | +1,957.8 | +2,280.3 | 44.8% | 43/47 |
| 34 | GLM-5.3 Flash (high) · OpenClaw | 1.10× | 1.03–1.18× | 22 | +2,528.0 | +1,927.5 | 40.0% | 38/42 |
| 35 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.11× | 1.04–1.20× | 29 | +2,335.1 | +2,679.7 | 68.6% | 67/72 |
| 36 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.12× | 1.08–1.17× | 26 | +2,283.2 | +2,369.6 | 55.2% | 55/58 |
| 37 | DeepSeek V4.1 Flash (low) · OpenClaw | 1.17× | 0.96–1.46× | 17 | +2,502.1 | +1,088.7 | 21.9% | 22/23 |
| 38 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.19× | 1.06–1.37× | 26 | +2,557.7 | +2,506.5 | 62.9% | 60/66 |
| — | DeepSeek V4.1 Flash (high) · OpenClaw | 1.06× | 0.97–1.19× | 10 | +2,388.6 | +611.2 | 18.1% | 18/19 |
| — | GLM-5.3 Flash (low) · Codex | 0.84× | 0.75–0.91× | 13 | +1,314.8 | +1,778.9 | 23.8% | 21/25 |
