# DeepSWE, harness comparison: Go (33 tasks × 3 attempts, 40 setups)

The Go tasks of the [harness comparison](../hlb-deepswe/README.md): GLM-5.3 Flash and DeepSeek V4.1 Flash, low and high effort, in ten coding-agent harnesses (OpenCode 1.19.0 and 2.2.6 separately), from Joel Niklaus's Harness Leaderboard. Method, sources, caveats and reproduction are in that README; this folder is the Go board ([page](../../site/harnesses-go.html)).

- Dataset (items with reference solutions) SHA256 `8f4416a8e8dfea22bfcf9258bb9bcb401f3f7a9bc3f14ca9ce5b79915cf74769`; analyzer `0.10.0-beta`, commit `3e213a1`.
- SHA256: [population.json](population.json) `7acf2bcc…`, [score-panel.json](score-panel.json) `347b03d6…`, [scores.json](scores.json) `0455ca4a…`, [coverage.json](coverage.json) `65ed0386…`, [sensitivity.json](sensitivity.json) `960dfaac…`.

## Ranking (same tasks)

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | GLM-5.3 Flash (low) · Codex | 0.88× | 0.81–0.96× | 19 | +2,721.4 | +2,747.5 | 28.3% | 28/28 |
| 2 | GLM-5.3 Flash (low) · Hermes | 0.92× | 0.88–0.96× | 30 | +3,103.1 | +2,906.4 | 62.6% | 62/62 |
| 2 | GLM-5.3 Flash (low) · pi | 0.92× | 0.89–0.96× | 25 | +3,118.5 | +2,765.0 | 51.5% | 51/51 |
| 4 | DeepSeek V4.1 Flash (high) · Codex | 0.93× | 0.88–0.97× | 28 | +3,016.3 | +2,775.6 | 67.7% | 67/67 |
| 4 | GLM-5.3 Flash (low) · OpenCode 2 | 0.93× | 0.89–0.96× | 28 | +3,172.2 | +2,797.4 | 60.6% | 60/60 |
| 4 | GLM-5.3 Flash (low) · Qwen Code | 0.93× | 0.88–0.99× | 26 | +2,916.6 | +2,750.6 | 52.5% | 52/52 |
| 7 | GLM-5.3 Flash (high) · Qwen Code | 0.94× | 0.89–0.97× | 27 | +2,865.4 | +2,793.6 | 55.6% | 55/55 |
| 7 | DeepSeek V4.1 Flash (low) · Qwen Code | 0.94× | 0.89–0.99× | 26 | +3,017.3 | +2,845.5 | 55.6% | 55/55 |
| 9 | DeepSeek V4.1 Flash (high) · Qwen Code | 0.95× | 0.90–1.00× | 27 | +3,015.9 | +2,811.5 | 64.6% | 64/64 |
| 9 | GLM-5.3 Flash (low) · Claude Code | 0.95× | 0.92–0.97× | 27 | +3,084.5 | +2,842.2 | 59.6% | 59/59 |
| 9 | GLM-5.3 Flash (low) · OpenCode | 0.95× | 0.89–1.01× | 17 | +3,497.2 | +2,474.8 | 26.3% | 26/26 |
| 9 | GLM-5.3 Flash (low) · Kimi Code | 0.95× | 0.92–1.00× | 27 | +3,025.2 | +2,873.6 | 59.6% | 59/59 |
| 13 | DeepSeek V4.1 Flash (low) · Codex | 0.96× | 0.92–0.98× | 29 | +3,073.5 | +2,922.3 | 69.7% | 69/69 |
| 13 | GLM-5.3 Flash (high) · Kimi Code | 0.96× | 0.93–0.98× | 27 | +3,079.4 | +2,988.2 | 68.7% | 68/68 |
| 13 | GLM-5.3 Flash (high) · pi | 0.96× | 0.93–0.99× | 29 | +3,075.8 | +2,928.0 | 68.7% | 68/68 |
| 13 | GLM-5.3 Flash (high) · Codex | 0.96× | 0.93–1.00× | 22 | +3,072.5 | +2,827.0 | 40.4% | 40/40 |
| 17 | DeepSeek V4.1 Flash (high) · Claude Code | 0.97× | 0.91–1.05× | 32 | +3,018.8 | +2,962.8 | 72.7% | 72/72 |
| 18 | DeepSeek V4.1 Flash (low) · Kimi Code | 0.98× | 0.93–1.02× | 32 | +3,047.3 | +3,077.8 | 76.8% | 76/76 |
| 18 | DeepSeek V4.1 Flash (low) · Claude Code | 0.98× | 0.94–1.02× | 29 | +3,214.5 | +2,939.7 | 70.7% | 70/70 |
| 18 | GLM-5.3 Flash (high) · OpenCode 2 | 0.98× | 0.94–1.02× | 31 | +3,261.4 | +3,021.1 | 65.7% | 65/65 |
| 18 | GLM-5.3 Flash (low) · OpenClaw | 0.98× | 0.92–1.05× | 21 | +3,239.6 | +2,855.5 | 30.3% | 30/30 |
| 22 | DeepSeek V4.1 Flash (low) · pi | 1.00× | 0.95–1.06× | 30 | +3,052.8 | +2,913.6 | 69.7% | 69/69 |
| 23 | DeepSeek V4.1 Flash (high) · OpenCode 2 | 1.01× | 0.98–1.03× | 31 | +3,143.7 | +3,033.4 | 75.8% | 75/75 |
| 23 | GLM-5.3 Flash (high) · Claude Code | 1.01× | 0.97–1.07× | 30 | +3,159.1 | +3,012.8 | 66.7% | 66/66 |
| 25 | GLM-5.3 Flash (high) · Hermes | 1.02× | 0.98–1.05× | 28 | +3,175.8 | +3,022.6 | 64.6% | 64/64 |
| 25 | DeepSeek V4.1 Flash (low) · OpenCode 2 | 1.02× | 0.95–1.14× | 29 | +3,202.7 | +3,082.6 | 76.8% | 76/76 |
| 27 | DeepSeek V4.1 Flash (high) · OpenCode | 1.03× | 0.96–1.09× | 26 | +3,107.6 | +2,326.6 | 56.6% | 56/56 |
| 27 | GLM-5.3 Flash (high) · OpenClaw | 1.03× | 0.97–1.11× | 24 | +3,086.1 | +2,962.1 | 32.3% | 32/32 |
| 27 | DeepSeek V4.1 Flash (low) · OpenCode | 1.03× | 0.99–1.08× | 26 | +3,321.7 | +2,647.4 | 55.6% | 55/55 |
| 30 | DeepSeek V4.1 Flash (low) · Hermes | 1.04× | 0.99–1.10× | 31 | +3,162.0 | +3,078.4 | 69.7% | 69/69 |
| 30 | DeepSeek V4.1 Flash (high) · Hermes | 1.04× | 0.99–1.08× | 31 | +3,189.4 | +3,175.6 | 78.8% | 78/78 |
| 30 | GLM-5.3 Flash (low) · mini-SWE-agent | 1.04× | 1.00–1.08× | 30 | +3,486.4 | +3,115.8 | 61.6% | 61/61 |
| 33 | DeepSeek V4.1 Flash (high) · Kimi Code | 1.06× | 0.99–1.14× | 30 | +3,331.4 | +3,176.9 | 66.7% | 66/66 |
| 33 | DeepSeek V4.1 Flash (high) · pi | 1.06× | 1.00–1.14× | 29 | +3,175.0 | +2,844.4 | 65.7% | 65/65 |
| 35 | GLM-5.3 Flash (high) · OpenCode | 1.08× | 1.00–1.17× | 24 | +3,679.5 | +2,346.9 | 39.4% | 39/39 |
| 35 | DeepSeek V4.1 Flash (low) · OpenClaw | 1.08× | 0.92–1.27× | 17 | +3,325.4 | +1,497.4 | 25.3% | 25/25 |
| 37 | GLM-5.3 Flash (high) · mini-SWE-agent | 1.13× | 1.08–1.19× | 30 | +3,680.1 | +3,416.8 | 66.7% | 66/66 |
| 38 | DeepSeek V4.1 Flash (high) · mini-SWE-agent | 1.14× | 1.06–1.24× | 30 | +3,690.0 | +3,249.8 | 70.7% | 70/70 |
| 39 | DeepSeek V4.1 Flash (low) · mini-SWE-agent | 1.15× | 1.08–1.21× | 31 | +3,668.6 | +3,475.5 | 67.7% | 67/67 |
| — | DeepSeek V4.1 Flash (high) · OpenClaw | 1.14× | 0.91–1.36× | 13 | +2,608.1 | +798.4 | 22.2% | 21/22 |
