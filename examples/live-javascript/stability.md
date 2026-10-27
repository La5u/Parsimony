# Score sensitivity: 6 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `live-multilang-javascript-v1`: 108 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (66 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: GPT-5.6 Sol · Slingshot 3.4.0 ≈ Claude Opus 4.6 · AMI Agent 0.7.0 ≈ DeepSeek V4.1 Flash · TianxiCode 0.1.486 ≈ GPT-5.5 · Slingshot 3.0.0 ≈ GPT-5.5 · Slingshot 2.6.0 ≈ Claude Sonnet 4.5 · Slingshot 2.6.0 (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under leave-one-model-out and deduplicated panels.
- **Stable under every variation and statistically separated** (0 of 5 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 5 pairs): GPT-5.6 Sol · Slingshot 3.4.0 vs Claude Opus 4.6 · AMI Agent 0.7.0, Claude Opus 4.6 · AMI Agent 0.7.0 vs DeepSeek V4.1 Flash · TianxiCode 0.1.486, DeepSeek V4.1 Flash · TianxiCode 0.1.486 vs GPT-5.5 · Slingshot 3.0.0, GPT-5.5 · Slingshot 3.0.0 vs GPT-5.5 · Slingshot 2.6.0, GPT-5.5 · Slingshot 2.6.0 vs Claude Sonnet 4.5 · Slingshot 2.6.0.
- **Midpoint rank never changes under any variation**: GPT-5.5 · Slingshot 2.6.0 (5), Claude Sonnet 4.5 · Slingshot 2.6.0 (6).
- Difficulty strata answer a different question and are not counted as variations; they reverse GPT-5.6 Sol · Slingshot 3.4.0 > Claude Opus 4.6 · AMI Agent 0.7.0 (solved by all); GPT-5.5 · Slingshot 2.6.0 > Claude Sonnet 4.5 · Slingshot 2.6.0 (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 108 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | GPT-5.6 Sol · Slingshot 3.4.0 | 35.3 | 21.1–48.8 | 28.0–42.5 | 1–2 | 1.0–6.0 | 0.60 |
| 2 | Claude Opus 4.6 · AMI Agent 0.7.0 | 34.3 | 13.0–55.5 | 20.7–47.9 | 1–2 | 1.0–6.0 | 0.40 |
| 3 | DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 22.6 | 9.5–35.8 | 16.2–28.9 | 3–4 | 1.0–6.0 | 0.00 |
| 4 | GPT-5.5 · Slingshot 3.0.0 | 21.9 | 2.5–42.8 | 8.7–35.0 | 3–4 | 1.0–6.0 | 0.00 |
| 5 | GPT-5.5 · Slingshot 2.6.0 | 13.7 | -5.2–35.5 | 0.4–27.0 | 5–5 | 1.0–6.0 | 0.00 |
| 6 | Claude Sonnet 4.5 · Slingshot 2.6.0 | 12.2 | -8.5–36.7 | -3.5–28.0 | 6–6 | 1.0–6.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| GPT-5.6 Sol · Slingshot 3.4.0 > Claude Opus 4.6 · AMI Agent 0.7.0 | 0.95 | -29.81 to 31.29 | 0.00 | net weight=0.5, net weight=0.6, failure cap=0, failure cap=10 | no |
| Claude Opus 4.6 · AMI Agent 0.7.0 > DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 11.73 | -18.15 to 42.02 | 0.06 | none | no |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 > GPT-5.5 · Slingshot 3.0.0 | 0.73 | -28.62 to 28.64 | 0.00 | net weight=1, failure cap=0, failure cap=10, without MultiQC/MultiQC, without grommet/grommet, without stdlib-js/stdlib, without sveltejs/svelte | no |
| GPT-5.5 · Slingshot 3.0.0 > GPT-5.5 · Slingshot 2.6.0 | 8.19 | -29.35 to 44.40 | 0.00 | none | no |
| GPT-5.5 · Slingshot 2.6.0 > Claude Sonnet 4.5 · Slingshot 2.6.0 | 1.43 | -39.02 to 40.34 | 0.00 | none | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-5.6 Sol · Slingshot 3.4.0 | 35.3 (1) | 34.9 (2) | 35.0 (2) | 35.1 (1) | 35.4 (1) | 35.5 (1) | 35.4 (1) | 38.3 (2) | 37.1 (2) | 32.2 (1) |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 34.3 (2) | 35.4 (1) | 35.0 (1) | 34.7 (2) | 34.0 (2) | 33.6 (2) | 34.4 (2) | 39.2 (1) | 37.2 (1) | 29.5 (2) |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 22.6 (3) | 22.9 (3) | 22.8 (3) | 22.7 (3) | 22.5 (3) | 22.4 (4) | 22.6 (3) | 26.7 (4) | 25.1 (4) | 18.5 (3) |
| GPT-5.5 · Slingshot 3.0.0 | 21.9 (4) | 21.0 (4) | 21.3 (4) | 21.6 (4) | 22.1 (4) | 22.4 (3) | 21.9 (4) | 28.2 (3) | 25.6 (3) | 15.6 (4) |
| GPT-5.5 · Slingshot 2.6.0 | 13.7 (5) | 13.2 (5) | 13.3 (5) | 13.5 (5) | 13.8 (5) | 14.0 (5) | 13.6 (5) | 21.5 (5) | 18.4 (5) | 5.8 (5) |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 12.2 (6) | 12.3 (6) | 12.3 (6) | 12.3 (6) | 12.2 (6) | 12.2 (6) | 12.1 (6) | 20.7 (6) | 17.3 (6) | 3.8 (6) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (10 of 221 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 54 | 33 | none |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 21 | 29 | none |
| GPT-5.5 · Slingshot 2.6.0 | 30 | 29 | none |
| GPT-5.5 · Slingshot 3.0.0 | 44 | 29 | none |
| GPT-5.6 Sol · Slingshot 3.4.0 | 72 | 44 | none |
| (dedup panel) | 10 | 0 | none |

Tasks that lose their only reference: Claude Opus 4.6 · AMI Agent 0.7.0: `Automattic__mongoose-15485`, `Automattic__mongoose-16153`, `Mintplex-Labs__anything-llm-5252`, `MultiQC__MultiQC-3242`, `TryGhost__Ghost-24345`, `asciidwango__js-primer-1834`, `asciidwango__js-primer-1837`, `facebook__stylex-1192`, `facebook__stylex-1209`, `grommet__grommet-7719`, `jsonata-js__jsonata-809`, `marko-js__marko-2793`, `notionnext-org__NotionNext-4316`, `notionnext-org__NotionNext-4338`, `open-gsd__gsd-core-1794`, `open-gsd__gsd-core-1799`, `open-gsd__gsd-core-2079`, `open-gsd__gsd-core-2233`, `open-gsd__gsd-core-2492`, `playcanvas__engine-9002`, `prettier__prettier-17708`, `proj4js__proj4js-560`, `reactjs__react-rails-1418`, `simple-icons__simple-icons-13659`, `stdlib-js__stdlib-1716`, `stdlib-js__stdlib-5735`, `stdlib-js__stdlib-5914`, `stdlib-js__stdlib-6527`, `stdlib-js__stdlib-7575`, `stdlib-js__stdlib-7590`, `stdlib-js__stdlib-7672`, `sveltejs__svelte-16666`, `sveltejs__svelte-18039`; Claude Sonnet 4.5 · Slingshot 2.6.0: `Automattic__mongoose-16153`, `Mintplex-Labs__anything-llm-5252`, `MultiQC__MultiQC-3242`, `TryGhost__Ghost-24345`, `asciidwango__js-primer-1834`, `asciidwango__js-primer-1837`, `facebook__stylex-1192`, `facebook__stylex-1209`, `grommet__grommet-7719`, `jsonata-js__jsonata-809`, `notionnext-org__NotionNext-4316`, `notionnext-org__NotionNext-4338`, `open-gsd__gsd-core-1794`, `open-gsd__gsd-core-1799`, `open-gsd__gsd-core-2079`, `open-gsd__gsd-core-2233`, `open-gsd__gsd-core-2492`, `playcanvas__engine-9002`, `proj4js__proj4js-560`, `reactjs__react-rails-1418`, `simple-icons__simple-icons-13659`, `stdlib-js__stdlib-1716`, `stdlib-js__stdlib-5735`, `stdlib-js__stdlib-5914`, `stdlib-js__stdlib-6527`, `stdlib-js__stdlib-7575`, `stdlib-js__stdlib-7590`, `stdlib-js__stdlib-7672`, `sveltejs__svelte-16666`; GPT-5.5 · Slingshot 2.6.0: `Automattic__mongoose-16153`, `Mintplex-Labs__anything-llm-5252`, `MultiQC__MultiQC-3242`, `TryGhost__Ghost-24345`, `asciidwango__js-primer-1834`, `asciidwango__js-primer-1837`, `facebook__stylex-1192`, `facebook__stylex-1209`, `grommet__grommet-7719`, `jsonata-js__jsonata-809`, `notionnext-org__NotionNext-4316`, `notionnext-org__NotionNext-4338`, `open-gsd__gsd-core-1794`, `open-gsd__gsd-core-1799`, `open-gsd__gsd-core-2079`, `open-gsd__gsd-core-2233`, `open-gsd__gsd-core-2492`, `playcanvas__engine-9002`, `proj4js__proj4js-560`, `reactjs__react-rails-1418`, `simple-icons__simple-icons-13659`, `stdlib-js__stdlib-1716`, `stdlib-js__stdlib-5735`, `stdlib-js__stdlib-5914`, `stdlib-js__stdlib-6527`, `stdlib-js__stdlib-7575`, `stdlib-js__stdlib-7590`, `stdlib-js__stdlib-7672`, `sveltejs__svelte-16666`; GPT-5.5 · Slingshot 3.0.0: `Automattic__mongoose-16153`, `Mintplex-Labs__anything-llm-5252`, `MultiQC__MultiQC-3242`, `TryGhost__Ghost-24345`, `asciidwango__js-primer-1834`, `asciidwango__js-primer-1837`, `facebook__stylex-1192`, `facebook__stylex-1209`, `grommet__grommet-7719`, `jsonata-js__jsonata-809`, `notionnext-org__NotionNext-4316`, `notionnext-org__NotionNext-4338`, `open-gsd__gsd-core-1794`, `open-gsd__gsd-core-1799`, `open-gsd__gsd-core-2079`, `open-gsd__gsd-core-2233`, `open-gsd__gsd-core-2492`, `playcanvas__engine-9002`, `proj4js__proj4js-560`, `reactjs__react-rails-1418`, `simple-icons__simple-icons-13659`, `stdlib-js__stdlib-1716`, `stdlib-js__stdlib-5735`, `stdlib-js__stdlib-5914`, `stdlib-js__stdlib-6527`, `stdlib-js__stdlib-7575`, `stdlib-js__stdlib-7590`, `stdlib-js__stdlib-7672`, `sveltejs__svelte-16666`; GPT-5.6 Sol · Slingshot 3.4.0: `Automattic__mongoose-16153`, `Mintplex-Labs__anything-llm-5252`, `MultiQC__MultiQC-3242`, `MultiQC__MultiQC-3300`, `TryGhost__Ghost-24345`, `asciidwango__js-primer-1834`, `asciidwango__js-primer-1837`, `codeceptjs__CodeceptJS-5109`, `facebook__stylex-1192`, `facebook__stylex-1209`, `google__zx-1317`, `grommet__grommet-7712`, `grommet__grommet-7719`, `gsd-build__get-shit-done-2107`, `hapijs__joi-3082`, `jsonata-js__jsonata-809`, `jsonata-js__jsonata-814`, `jsonata-js__jsonata-817`, `nock__nock-2880`, `notionnext-org__NotionNext-4253`, `notionnext-org__NotionNext-4290`, `notionnext-org__NotionNext-4316`, `notionnext-org__NotionNext-4338`, `open-gsd__gsd-core-1794`, `open-gsd__gsd-core-1799`, `open-gsd__gsd-core-2079`, `open-gsd__gsd-core-2233`, `open-gsd__gsd-core-2492`, `playcanvas__engine-9000`, `playcanvas__engine-9002`, `playcanvas__engine-9066`, `proj4js__proj4js-560`, `reactjs__react-rails-1418`, `simple-icons__simple-icons-13659`, `stdlib-js__stdlib-1716`, `stdlib-js__stdlib-5735`, `stdlib-js__stdlib-5914`, `stdlib-js__stdlib-6527`, `stdlib-js__stdlib-7575`, `stdlib-js__stdlib-7590`, `stdlib-js__stdlib-7672`, `sveltejs__svelte-16248`, `sveltejs__svelte-16502`, `sveltejs__svelte-16666`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| Automattic/mongoose (4) | none |
| GladysAssistant/Gladys (1) | none |
| Mintplex-Labs/anything-llm (1) | none |
| MultiQC/MultiQC (2) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 3→4, GPT-5.5 · Slingshot 3.0.0 4→3 |
| TryGhost/Ghost (1) | none |
| appium/appium-inspector (1) | none |
| aralroca/next-translate (1) | none |
| asciidwango/js-primer (2) | none |
| camunda/camunda-modeler (1) | none |
| code-charity/youtube (1) | none |
| codeceptjs/CodeceptJS (3) | none |
| cthackers/adm-zip (1) | none |
| cytoscape/cytoscape.js (1) | none |
| decaporg/decap-cms (1) | none |
| docsifyjs/docsify (1) | none |
| ember-cli/ember-cli (1) | none |
| facebook/stylex (2) | none |
| fastify/fastify (1) | none |
| google/zx (1) | none |
| grommet/grommet (4) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 3→4, GPT-5.5 · Slingshot 3.0.0 4→3 |
| gsd-build/get-shit-done (2) | none |
| hapijs/joi (1) | none |
| haraka/Haraka (1) | none |
| hotwired/turbo (1) | none |
| jsonata-js/jsonata (3) | none |
| less/less.js (2) | none |
| marko-js/marko (1) | none |
| moment/luxon (1) | none |
| mozilla/pdf.js (1) | none |
| nock/nock (1) | none |
| nodejs/undici (3) | none |
| notionnext-org/NotionNext (4) | none |
| open-gsd/gsd-core (5) | none |
| openai/codex-plugin-cc (1) | none |
| playcanvas/engine (3) | none |
| preactjs/preact (2) | none |
| prettier/prettier (1) | none |
| proj4js/proj4js (1) | none |
| reactjs/react-rails (1) | none |
| rollup/rollup (5) | none |
| shaka-project/shaka-player (1) | none |
| siimon/prom-client (1) | none |
| simple-icons/simple-icons (1) | none |
| stdlib-js/stdlib (7) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 3→4, GPT-5.5 · Slingshot 3.0.0 4→3 |
| sveltejs/svelte (24) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 3→4, GPT-5.5 · Slingshot 3.0.0 4→3 |
| thlorenz/doctoc (2) | none |
| usebruno/bruno (1) | none |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (108) | Solved by every model (10) | Solved by fewer (98) |
|---|---:|---:|---:|
| GPT-5.6 Sol · Slingshot 3.4.0 | 35.3 (1) | 54.7 (2) | 33.3 (1) |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 34.3 (2) | 62.4 (1) | 31.5 (2) |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 22.6 (3) | 48.5 (4) | 19.9 (3) |
| GPT-5.5 · Slingshot 3.0.0 | 21.9 (4) | 44.0 (5) | 19.6 (4) |
| GPT-5.5 · Slingshot 2.6.0 | 13.7 (5) | 42.8 (6) | 10.7 (5) |
| Claude Sonnet 4.5 · Slingshot 2.6.0 | 12.2 (6) | 48.7 (3) | 8.5 (6) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **GPT-5.6 Sol · Slingshot 3.4.0 − Claude Opus 4.6 · AMI Agent 0.7.0 = -0.22**: failed/failed -0.03 (1), failed/solved -4.56 (5), solved/failed 12.39 (13), solved/solved -8.02 (48). For GPT-5.6 Sol · Slingshot 3.4.0: `thlorenz__doctoc-329` +1.49 (solved/failed), `nodejs__undici-5000` +1.38 (solved/failed), `sveltejs__svelte-16592` +1.19 (solved/failed). For Claude Opus 4.6 · AMI Agent 0.7.0: `shaka-project__shaka-player-8835` -1.35 (failed/solved), `cthackers__adm-zip-559` -1.03 (solved/solved), `nodejs__undici-4453` -1.03 (solved/solved).
- **Claude Opus 4.6 · AMI Agent 0.7.0 − DeepSeek V4.1 Flash · TianxiCode 0.1.486 = 12.53**: failed/failed 0.21 (3), failed/solved -9.09 (11), solved/failed 15.46 (15), solved/solved 5.95 (38). For Claude Opus 4.6 · AMI Agent 0.7.0: `sveltejs__svelte-16542` +1.54 (solved/failed), `decaporg__decap-cms-7495` +1.38 (solved/failed), `sveltejs__svelte-16405` +1.36 (solved/failed). For DeepSeek V4.1 Flash · TianxiCode 0.1.486: `sveltejs__svelte-16502` -1.56 (failed/solved), `thlorenz__doctoc-329` -1.35 (failed/solved), `sveltejs__svelte-16592` -1.19 (failed/solved).
- **DeepSeek V4.1 Flash · TianxiCode 0.1.486 − GPT-5.5 · Slingshot 3.0.0 = 6.90**: failed/failed 0.53 (11), failed/solved -7.27 (10), solved/failed 10.31 (16), solved/solved 3.33 (34). For DeepSeek V4.1 Flash · TianxiCode 0.1.486: `sveltejs__svelte-16502` +1.60 (solved/failed), `MultiQC__MultiQC-3300` +1.47 (solved/failed), `sveltejs__svelte-16248` +0.97 (solved/failed). For GPT-5.5 · Slingshot 3.0.0: `sveltejs__svelte-16542` -1.10 (failed/solved), `nodejs__undici-4453` -0.98 (solved/solved), `rollup__rollup-6051` -0.92 (solved/solved).
- **GPT-5.5 · Slingshot 3.0.0 − GPT-5.5 · Slingshot 2.6.0 = 12.11**: failed/failed -0.05 (27), failed/solved -0.91 (1), solved/failed 12.81 (15), solved/solved 0.26 (29). For GPT-5.5 · Slingshot 3.0.0: `less__less.js-4363` +1.44 (solved/failed), `Automattic__mongoose-15492` +1.20 (solved/failed), `sveltejs__svelte-16668` +1.07 (solved/failed). For GPT-5.5 · Slingshot 2.6.0: `grommet__grommet-7709` -0.91 (failed/solved), `cytoscape__cytoscape.js-3396` -0.69 (solved/solved), `grommet__grommet-7718` -0.69 (solved/solved).
- **GPT-5.5 · Slingshot 2.6.0 − Claude Sonnet 4.5 · Slingshot 2.6.0 = 5.63**: failed/failed -0.76 (33), failed/solved -5.40 (7), solved/failed 11.92 (16), solved/solved -0.14 (14). For GPT-5.5 · Slingshot 2.6.0: `sveltejs__svelte-16466` +1.36 (solved/failed), `nodejs__undici-5011` +1.24 (solved/failed), `gsd-build__get-shit-done-2186` +1.21 (solved/failed). For Claude Sonnet 4.5 · Slingshot 2.6.0: `Automattic__mongoose-15534` -1.06 (failed/solved), `appium__appium-inspector-2178` -0.91 (failed/solved), `sveltejs__svelte-16389` -0.88 (failed/solved).

## Regenerate

```sh
python -m parsimony.stability examples/live-javascript/score-panel.json examples/live-javascript/claude-opus-4.6-ami.jsonl examples/live-javascript/claude-sonnet-4.5-slingshot-2.6.0.jsonl examples/live-javascript/deepseek-v4.1-flash-tianxicode-0.1.486.jsonl examples/live-javascript/gpt-5.5-slingshot-2.6.0.jsonl examples/live-javascript/gpt-5.5-slingshot-3.0.0.jsonl examples/live-javascript/gpt-5.6-sol-slingshot-3.4.0.jsonl --output examples/live-javascript/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
