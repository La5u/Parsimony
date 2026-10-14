# Score sensitivity: 5 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `live-multilang-typescript-v1`: 111 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (68 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: GPT-5.6 Sol · Slingshot 3.4.0 ≈ Claude Opus 4.6 · AMI Agent 0.7.0 ≈ GPT-5.5 · Slingshot 3.0.0 ≈ GPT-5.5 · Slingshot 2.6.0 ≈ Claude Sonnet 4.5 · Slingshot 2.6.0 (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under net weight 0.5–1.0 and the net floor or failure cap 0–50 or leave-one-model-out and deduplicated panels or leave-one-repository-out.
- **Stable under every variation and statistically separated** (0 of 4 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 4 pairs): GPT-5.6 Sol · Slingshot 3.4.0 vs Claude Opus 4.6 · AMI Agent 0.7.0, Claude Opus 4.6 · AMI Agent 0.7.0 vs GPT-5.5 · Slingshot 3.0.0, GPT-5.5 · Slingshot 3.0.0 vs GPT-5.5 · Slingshot 2.6.0, GPT-5.5 · Slingshot 2.6.0 vs Claude Sonnet 4.5 · Slingshot 2.6.0.
- **Midpoint rank never changes under any variation**: GPT-5.6 Sol · Slingshot 3.4.0 (1), Claude Opus 4.6 · AMI Agent 0.7.0 (2), GPT-5.5 · Slingshot 3.0.0 (3), GPT-5.5 · Slingshot 2.6.0 (4), Claude Sonnet 4.5 · Slingshot 2.6.0 (5).
- Difficulty strata answer a different question and are not counted as variations; they reverse GPT-5.5 · Slingshot 2.6.0 > Claude Sonnet 4.5 · Slingshot 2.6.0 (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 111 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | GPT-5.6 Sol · Slingshot 3.4.0 | 29.5 | 15.7–42.2 | 23.5–35.6 | 1–1 | 1.0–4.0 | 0.88 |
| 2 | Claude Opus 4.6 · AMI Agent 0.7.0 | 25.1 | 11.4–38.4 | 18.7–31.5 | 2–2 | 1.0–5.0 | 0.12 |
| 3 | GPT-5.5 · Slingshot 3.0.0 | 16.1 | 4.5–26.2 | 11.6–20.6 | 3–3 | 1.0–5.0 | 0.00 |
| 4 | GPT-5.5 · Slingshot 2.6.0 | 11.3 | -0.0–22.0 | 6.3–16.2 | 4–4 | 1.0–5.0 | 0.00 |
| 5 | Claude Sonnet 4.5 · Slingshot 2.6.0 | 8.3 | -5.1–22.6 | 1.0–15.7 | 5–5 | 1.0–5.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| GPT-5.6 Sol · Slingshot 3.4.0 > Claude Opus 4.6 · AMI Agent 0.7.0 | 4.41 | -17.12 to 24.34 | 0.03 | none | no |
| Claude Opus 4.6 · AMI Agent 0.7.0 > GPT-5.5 · Slingshot 3.0.0 | 9.05 | -9.95 to 28.63 | 0.34 | none | no |
| GPT-5.5 · Slingshot 3.0.0 > GPT-5.5 · Slingshot 2.6.0 | 4.83 | -10.79 to 19.65 | 0.06 | none | no |
| GPT-5.5 · Slingshot 2.6.0 > Claude Sonnet 4.5 · Slingshot 2.6.0 | 2.91 | -17.77 to 22.16 | 0.01 | none | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-5.6 Sol · Slingshot 3.4.0 | 29.5 (1) | 28.5 (1) | 28.9 (1) | 29.2 (1) | 29.9 (1) | 30.2 (1) | 29.0 (1) | 34.0 (1) | 32.2 (1) | 25.1 (1) |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 25.1 (2) | 25.8 (2) | 25.6 (2) | 25.4 (2) | 24.9 (2) | 24.7 (2) | 25.5 (2) | 30.1 (2) | 28.1 (2) | 20.2 (2) |
| GPT-5.5 · Slingshot 3.0.0 | 16.1 (3) | 16.0 (3) | 16.0 (3) | 16.1 (3) | 16.1 (3) | 16.2 (3) | 15.9 (3) | 21.9 (3) | 19.6 (3) | 10.2 (3) |
| GPT-5.5 · Slingshot 2.6.0 | 11.3 (4) | 10.9 (4) | 11.1 (4) | 11.2 (4) | 11.4 (4) | 11.5 (4) | 11.4 (4) | 18.0 (4) | 15.3 (4) | 4.5 (4) |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 8.3 (5) | 8.6 (5) | 8.5 (5) | 8.4 (5) | 8.3 (5) | 8.2 (5) | 8.6 (5) | 16.9 (5) | 13.5 (5) | -0.2 (5) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (1 of 245 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 56 | 40 | none |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 27 | 35 | none |
| GPT-5.5 · Slingshot 2.6.0 | 45 | 35 | none |
| GPT-5.5 · Slingshot 3.0.0 | 51 | 35 | none |
| GPT-5.6 Sol · Slingshot 3.4.0 | 66 | 40 | none |
| (dedup panel) | 1 | 0 | none |

Tasks that lose their only reference: Claude Opus 4.6 · AMI Agent 0.7.0: `QwenLM__qwen-code-349`, `Shopify__hydrogen-3072`, `TanStack__form-1664`, `TanStack__router-4629`, `TanStack__router-4685`, `TanStack__router-4716`, `TanStack__router-4751`, `TanStack__router-4915`, `TypeCellOS__BlockNote-2629`, `assistant-ui__assistant-ui-3866`, `better-auth__better-auth-4175`, `can1357__oh-my-pi-489`, `cloudflare__workers-sdk-10032`, `cloudflare__workers-sdk-10209`, `cloudflare__workers-sdk-9866`, `firefox-devtools__profiler-3073`, `firefox-devtools__profiler-5512`, `formbricks__formbricks-5903`, `formbricks__formbricks-6270`, `formbricks__formbricks-6302`, `formbricks__formbricks-6361`, `formbricks__formbricks-6413`, `ghostfolio__ghostfolio-5093`, `gsd-build__gsd-2-2738`, `gsd-build__gsd-2-3258`, `honojs__hono-4249`, `jestjs__jest-15714`, `lightdash__lightdash-15838`, `maplibre__maplibre-gl-js-6216`, `maplibre__maplibre-gl-js-6266`, `mui__base-ui-2269`, `puppeteer__puppeteer-14826`, `recharts__recharts-6124`, `remotion-dev__remotion-5529`, `remotion-dev__remotion-5532`, `taiga-family__taiga-ui-11501`, `twentyhq__twenty-13858`, `vercel__ai-7326`, `vercel__ai-7552`, `vercel__ai-7608`; Claude Sonnet 4.5 · Slingshot 2.6.0: `QwenLM__qwen-code-349`, `Shopify__hydrogen-3072`, `TanStack__router-4629`, `TanStack__router-4685`, `TanStack__router-4751`, `TanStack__router-4915`, `assistant-ui__assistant-ui-3866`, `better-auth__better-auth-4175`, `can1357__oh-my-pi-489`, `cloudflare__workers-sdk-10032`, `cloudflare__workers-sdk-10209`, `cloudflare__workers-sdk-9866`, `firefox-devtools__profiler-3073`, `firefox-devtools__profiler-5512`, `formbricks__formbricks-5903`, `formbricks__formbricks-6270`, `formbricks__formbricks-6302`, `formbricks__formbricks-6361`, `formbricks__formbricks-6413`, `ghostfolio__ghostfolio-5093`, `gsd-build__gsd-2-3258`, `honojs__hono-4249`, `jestjs__jest-15714`, `maplibre__maplibre-gl-js-6216`, `maplibre__maplibre-gl-js-6266`, `mui__base-ui-2269`, `puppeteer__puppeteer-14826`, `recharts__recharts-6124`, `remotion-dev__remotion-5529`, `remotion-dev__remotion-5532`, `taiga-family__taiga-ui-11501`, `twentyhq__twenty-13858`, `vercel__ai-7326`, `vercel__ai-7552`, `vercel__ai-7608`; GPT-5.5 · Slingshot 2.6.0: `QwenLM__qwen-code-349`, `Shopify__hydrogen-3072`, `TanStack__router-4629`, `TanStack__router-4685`, `TanStack__router-4751`, `TanStack__router-4915`, `assistant-ui__assistant-ui-3866`, `better-auth__better-auth-4175`, `can1357__oh-my-pi-489`, `cloudflare__workers-sdk-10032`, `cloudflare__workers-sdk-10209`, `cloudflare__workers-sdk-9866`, `firefox-devtools__profiler-3073`, `firefox-devtools__profiler-5512`, `formbricks__formbricks-5903`, `formbricks__formbricks-6270`, `formbricks__formbricks-6302`, `formbricks__formbricks-6361`, `formbricks__formbricks-6413`, `ghostfolio__ghostfolio-5093`, `gsd-build__gsd-2-3258`, `honojs__hono-4249`, `jestjs__jest-15714`, `maplibre__maplibre-gl-js-6216`, `maplibre__maplibre-gl-js-6266`, `mui__base-ui-2269`, `puppeteer__puppeteer-14826`, `recharts__recharts-6124`, `remotion-dev__remotion-5529`, `remotion-dev__remotion-5532`, `taiga-family__taiga-ui-11501`, `twentyhq__twenty-13858`, `vercel__ai-7326`, `vercel__ai-7552`, `vercel__ai-7608`; GPT-5.5 · Slingshot 3.0.0: `QwenLM__qwen-code-349`, `Shopify__hydrogen-3072`, `TanStack__router-4629`, `TanStack__router-4685`, `TanStack__router-4751`, `TanStack__router-4915`, `assistant-ui__assistant-ui-3866`, `better-auth__better-auth-4175`, `can1357__oh-my-pi-489`, `cloudflare__workers-sdk-10032`, `cloudflare__workers-sdk-10209`, `cloudflare__workers-sdk-9866`, `firefox-devtools__profiler-3073`, `firefox-devtools__profiler-5512`, `formbricks__formbricks-5903`, `formbricks__formbricks-6270`, `formbricks__formbricks-6302`, `formbricks__formbricks-6361`, `formbricks__formbricks-6413`, `ghostfolio__ghostfolio-5093`, `gsd-build__gsd-2-3258`, `honojs__hono-4249`, `jestjs__jest-15714`, `maplibre__maplibre-gl-js-6216`, `maplibre__maplibre-gl-js-6266`, `mui__base-ui-2269`, `puppeteer__puppeteer-14826`, `recharts__recharts-6124`, `remotion-dev__remotion-5529`, `remotion-dev__remotion-5532`, `taiga-family__taiga-ui-11501`, `twentyhq__twenty-13858`, `vercel__ai-7326`, `vercel__ai-7552`, `vercel__ai-7608`; GPT-5.6 Sol · Slingshot 3.4.0: `QwenLM__qwen-code-349`, `Shopify__hydrogen-3072`, `TanStack__router-4629`, `TanStack__router-4685`, `TanStack__router-4751`, `TanStack__router-4915`, `TanStack__router-4978`, `assistant-ui__assistant-ui-3866`, `better-auth__better-auth-4175`, `can1357__oh-my-pi-489`, `cloudflare__workers-sdk-10032`, `cloudflare__workers-sdk-10209`, `cloudflare__workers-sdk-9866`, `firefox-devtools__profiler-3073`, `firefox-devtools__profiler-5512`, `formbricks__formbricks-5903`, `formbricks__formbricks-6270`, `formbricks__formbricks-6302`, `formbricks__formbricks-6361`, `formbricks__formbricks-6413`, `getsentry__sentry-javascript-17013`, `ghostfolio__ghostfolio-5093`, `gpbl__react-day-picker-2816`, `gsd-build__gsd-2-3258`, `honojs__hono-4249`, `jestjs__jest-15714`, `lightdash__lightdash-16521`, `maplibre__maplibre-gl-js-6216`, `maplibre__maplibre-gl-js-6266`, `mui__base-ui-2269`, `puppeteer__puppeteer-14826`, `recharts__recharts-6124`, `remotion-dev__remotion-5529`, `remotion-dev__remotion-5532`, `reown-com__appkit-4542`, `taiga-family__taiga-ui-11501`, `twentyhq__twenty-13858`, `vercel__ai-7326`, `vercel__ai-7552`, `vercel__ai-7608`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| ChainSafe/lodestar (1) | none |
| MetaMask/metamask-mobile (5) | none |
| Milkdown/milkdown (1) | none |
| NVIDIA/NemoClaw (1) | none |
| QwenLM/qwen-code (2) | none |
| RocketChat/Rocket.Chat.ReactNative (1) | none |
| RooCodeInc/Roo-Code (1) | none |
| Shopify/hydrogen (2) | none |
| TanStack/form (2) | none |
| TanStack/router (8) | none |
| TypeCellOS/BlockNote (1) | none |
| antvis/G2 (2) | none |
| assistant-ui/assistant-ui (1) | none |
| aws-amplify/amplify-ui (1) | none |
| better-auth/better-auth (1) | none |
| can1357/oh-my-pi (1) | none |
| chimurai/http-proxy-middleware (1) | none |
| cloudflare/workers-sdk (3) | none |
| code-yeongyu/oh-my-openagent (1) | none |
| denoland/std (1) | none |
| dsherret/ts-morph (1) | none |
| ether/etherpad (1) | none |
| excalidraw/excalidraw (1) | none |
| firefox-devtools/profiler (2) | none |
| formbricks/formbricks (5) | none |
| getsentry/sentry-javascript (2) | none |
| ghostfolio/ghostfolio (1) | none |
| gpbl/react-day-picker (2) | none |
| gsd-build/gsd-2 (5) | none |
| highcharts/highcharts (1) | none |
| honojs/hono (3) | none |
| iOfficeAI/AionUi (1) | none |
| jestjs/jest (1) | none |
| jhlywa/chess.js (1) | none |
| katspaugh/wavesurfer.js (1) | none |
| kepano/defuddle (1) | none |
| lightdash/lightdash (2) | none |
| maplibre/maplibre-gl-js (2) | none |
| mikro-orm/mikro-orm (1) | none |
| mnfst/manifest (1) | none |
| monkeytypegame/monkeytype (1) | none |
| mui/base-ui (5) | none |
| mui/mui-x (1) | none |
| openai/openai-agents-js (5) | none |
| openapi-ts/openapi-typescript (1) | none |
| orval-labs/orval (1) | none |
| owid/owid-grapher (2) | none |
| puppeteer/puppeteer (1) | none |
| react-hook-form/react-hook-form (2) | none |
| recharts/recharts (3) | none |
| remotion-dev/remotion (2) | none |
| reown-com/appkit (1) | none |
| surveyjs/survey-library (1) | none |
| taiga-family/taiga-ui (1) | none |
| tailwindlabs/tailwindcss (1) | none |
| twentyhq/twenty (1) | none |
| unocss/unocss (1) | none |
| unplugin/unplugin-vue-components (1) | none |
| vercel/ai (3) | none |
| vueuse/vueuse (1) | none |
| webdriverio/webdriverio (1) | none |
| withastro/starlight (2) | none |
| wxt-dev/wxt (1) | none |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (111) | Solved by every model (22) | Solved by fewer (89) |
|---|---:|---:|---:|
| GPT-5.6 Sol · Slingshot 3.4.0 | 29.5 (1) | 55.1 (2) | 23.2 (1) |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 25.1 (2) | 50.5 (3) | 18.9 (2) |
| GPT-5.5 · Slingshot 3.0.0 | 16.1 (3) | 45.1 (4) | 8.9 (3) |
| GPT-5.5 · Slingshot 2.6.0 | 11.3 (4) | 44.0 (5) | 3.2 (4) |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 8.3 (5) | 57.8 (1) | -3.9 (5) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **GPT-5.6 Sol · Slingshot 3.4.0 − Claude Opus 4.6 · AMI Agent 0.7.0 = 7.32**: failed/failed -0.03 (1), failed/solved -5.38 (6), solved/failed 13.87 (15), solved/solved -1.15 (48). For GPT-5.6 Sol · Slingshot 3.4.0: `denoland__std-6775` +1.32 (solved/failed), `surveyjs__survey-library-11137` +1.30 (solved/failed), `QwenLM__qwen-code-3310` +1.26 (solved/failed). For Claude Opus 4.6 · AMI Agent 0.7.0: `ChainSafe__lodestar-8203` -1.43 (failed/solved), `openai__openai-agents-js-318` -0.99 (solved/solved), `TanStack__form-1664` -0.97 (failed/solved).
- **Claude Opus 4.6 · AMI Agent 0.7.0 − GPT-5.5 · Slingshot 3.0.0 = 11.25**: failed/failed -0.06 (4), failed/solved -9.98 (11), solved/failed 16.22 (18), solved/solved 5.07 (37). For Claude Opus 4.6 · AMI Agent 0.7.0: `openapi-ts__openapi-typescript-2365` +1.31 (solved/failed), `gsd-build__gsd-2-3946` +1.25 (solved/failed), `unplugin__unplugin-vue-components-858` +1.25 (solved/failed). For GPT-5.5 · Slingshot 3.0.0: `getsentry__sentry-javascript-17078` -1.29 (failed/solved), `orval-labs__orval-2328` -1.18 (failed/solved), `code-yeongyu__oh-my-openagent-3013` -1.16 (failed/solved).
- **GPT-5.5 · Slingshot 3.0.0 − GPT-5.5 · Slingshot 2.6.0 = 7.91**: failed/failed 0.75 (22), failed/solved -0.41 (1), solved/failed 5.39 (7), solved/solved 2.18 (44). For GPT-5.5 · Slingshot 3.0.0: `recharts__recharts-6070` +1.30 (solved/failed), `getsentry__sentry-javascript-17078` +1.25 (solved/failed), `antvis__G2-7076` +1.00 (solved/solved). For GPT-5.5 · Slingshot 2.6.0: `aws-amplify__amplify-ui-6665` -1.07 (solved/solved), `vueuse__vueuse-5336` -0.80 (solved/solved), `webdriverio__webdriverio-14672` -0.70 (solved/solved).
- **GPT-5.5 · Slingshot 2.6.0 − Claude Sonnet 4.5 · Slingshot 2.6.0 = 7.05**: failed/failed -0.11 (26), failed/solved -2.31 (3), solved/failed 14.20 (20), solved/solved -4.72 (23). For GPT-5.5 · Slingshot 2.6.0: `highcharts__highcharts-23356` +1.42 (solved/failed), `antvis__G2-7021` +1.33 (solved/failed), `excalidraw__excalidraw-9760` +1.11 (solved/failed). For Claude Sonnet 4.5 · Slingshot 2.6.0: `MetaMask__metamask-mobile-17208` -1.34 (failed/solved), `kepano__defuddle-243` -1.10 (solved/solved), `dsherret__ts-morph-1663` -1.05 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability /home/lasu/coding/Parsimony/examples/live-typescript/score-panel.json /home/lasu/coding/Parsimony/examples/live-typescript/claude-opus-4.6-ami.jsonl /home/lasu/coding/Parsimony/examples/live-typescript/claude-sonnet-4.5-slingshot-2.6.0.jsonl /home/lasu/coding/Parsimony/examples/live-typescript/gpt-5.5-slingshot-2.6.0.jsonl /home/lasu/coding/Parsimony/examples/live-typescript/gpt-5.5-slingshot-3.0.0.jsonl /home/lasu/coding/Parsimony/examples/live-typescript/gpt-5.6-sol-slingshot-3.4.0.jsonl --output /home/lasu/coding/Parsimony/examples/live-typescript/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
