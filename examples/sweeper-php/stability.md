# Score sensitivity: 15 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `sweeper-php-v1`: 128 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (68 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: sweeper-deepseek-v4.1-flash-deepseek-harness ≈ sweeper-glm-5.3-flash-codex ≈ sweeper-kimi-k3-kimi-code ≈ sweeper-gpt-6-astra-codex ≈ sweeper-claude-opus-5-claude-code ≈ sweeper-muse-spark-1.3-muse-code ≈ sweeper-deepseek-v4-pro-deepseek-harness ≈ sweeper-gpt-5.6-luna-codex ≈ sweeper-claude-fable-5-1-claude-code ≈ sweeper-gpt-5.6-sol-codex ≈ sweeper-glm-5.3-codex ≈ sweeper-qwen3.8-max-codex ≈ sweeper-gpt-5.6-terra-codex ≈ sweeper-qwen3.8-flash-codex ≈ sweeper-grok-4.6-cursor (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **Stable under every variation and statistically separated** (0 of 14 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 14 pairs): sweeper-deepseek-v4.1-flash-deepseek-harness vs sweeper-glm-5.3-flash-codex, sweeper-glm-5.3-flash-codex vs sweeper-kimi-k3-kimi-code, sweeper-kimi-k3-kimi-code vs sweeper-gpt-6-astra-codex, sweeper-gpt-6-astra-codex vs sweeper-claude-opus-5-claude-code, sweeper-claude-opus-5-claude-code vs sweeper-muse-spark-1.3-muse-code, sweeper-muse-spark-1.3-muse-code vs sweeper-deepseek-v4-pro-deepseek-harness, sweeper-deepseek-v4-pro-deepseek-harness vs sweeper-gpt-5.6-luna-codex, sweeper-gpt-5.6-luna-codex vs sweeper-claude-fable-5-1-claude-code, sweeper-claude-fable-5-1-claude-code vs sweeper-gpt-5.6-sol-codex, sweeper-gpt-5.6-sol-codex vs sweeper-glm-5.3-codex, sweeper-glm-5.3-codex vs sweeper-qwen3.8-max-codex, sweeper-qwen3.8-max-codex vs sweeper-gpt-5.6-terra-codex, sweeper-gpt-5.6-terra-codex vs sweeper-qwen3.8-flash-codex, sweeper-qwen3.8-flash-codex vs sweeper-grok-4.6-cursor.
- **Midpoint rank never changes under any variation**: sweeper-gpt-5.6-terra-codex (13), sweeper-qwen3.8-flash-codex (14), sweeper-grok-4.6-cursor (15).
- Difficulty strata answer a different question and are not counted as variations; they reverse sweeper-deepseek-v4.1-flash-deepseek-harness > sweeper-glm-5.3-flash-codex (solved by all); sweeper-glm-5.3-flash-codex > sweeper-kimi-k3-kimi-code (solved by fewer); sweeper-kimi-k3-kimi-code > sweeper-gpt-6-astra-codex (solved by fewer); sweeper-gpt-6-astra-codex > sweeper-claude-opus-5-claude-code (solved by all); sweeper-claude-opus-5-claude-code > sweeper-muse-spark-1.3-muse-code (solved by all); sweeper-muse-spark-1.3-muse-code > sweeper-deepseek-v4-pro-deepseek-harness (solved by fewer); sweeper-deepseek-v4-pro-deepseek-harness > sweeper-gpt-5.6-luna-codex (solved by all); sweeper-gpt-5.6-luna-codex > sweeper-claude-fable-5-1-claude-code (solved by fewer); sweeper-claude-fable-5-1-claude-code > sweeper-gpt-5.6-sol-codex (solved by all); sweeper-glm-5.3-codex > sweeper-qwen3.8-max-codex (solved by all); sweeper-qwen3.8-max-codex > sweeper-gpt-5.6-terra-codex (solved by fewer); sweeper-gpt-5.6-terra-codex > sweeper-qwen3.8-flash-codex (solved by fewer).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 128 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | sweeper-deepseek-v4.1-flash-deepseek-harness | 26.9 | 15.5–37.1 | 22.9–30.9 | 1–2 | 1.0–14.0 | 0.35 |
| 2 | sweeper-glm-5.3-flash-codex | 26.6 | 13.5–38.9 | 21.6–31.5 | 1–3 | 1.0–15.0 | 0.31 |
| 3 | sweeper-kimi-k3-kimi-code | 26.1 | 15.3–35.8 | 22.5–29.7 | 2–4 | 1.0–14.0 | 0.17 |
| 4 | sweeper-gpt-6-astra-codex | 25.1 | 14.5–34.7 | 21.0–29.2 | 3–4 | 1.0–15.0 | 0.13 |
| 5 | sweeper-claude-opus-5-claude-code | 23.4 | 12.4–33.4 | 19.2–27.6 | 5–6 | 1.0–15.0 | 0.03 |
| 6 | sweeper-muse-spark-1.3-muse-code | 21.4 | 10.5–32.0 | 17.0–25.8 | 5–7 | 1.0–15.0 | 0.00 |
| 7 | sweeper-deepseek-v4-pro-deepseek-harness | 21.0 | 10.5–30.7 | 17.0–25.0 | 6–8 | 1.0–15.0 | 0.00 |
| 8 | sweeper-gpt-5.6-luna-codex | 20.4 | 9.4–30.7 | 16.0–24.8 | 7–10 | 1.0–15.0 | 0.00 |
| 9 | sweeper-claude-fable-5-1-claude-code | 20.2 | 9.8–30.1 | 15.9–24.5 | 8–10 | 1.0–15.0 | 0.00 |
| 10 | sweeper-gpt-5.6-sol-codex | 19.4 | 6.9–31.7 | 13.6–25.3 | 8–11 | 1.0–15.0 | 0.00 |
| 11 | sweeper-glm-5.3-codex | 18.3 | 8.4–27.5 | 14.9–21.8 | 10–12 | 1.0–15.0 | 0.00 |
| 12 | sweeper-qwen3.8-max-codex | 17.8 | 6.2–28.8 | 13.5–22.0 | 11–12 | 1.0–15.0 | 0.00 |
| 13 | sweeper-gpt-5.6-terra-codex | 16.0 | 4.5–26.8 | 11.0–21.0 | 13–13 | 1.0–15.0 | 0.00 |
| 14 | sweeper-qwen3.8-flash-codex | 13.6 | 4.0–22.9 | 9.4–17.9 | 14–14 | 2.0–15.0 | 0.00 |
| 15 | sweeper-grok-4.6-cursor | 10.4 | 0.4–21.0 | 4.9–15.9 | 15–15 | 3.0–15.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| sweeper-deepseek-v4.1-flash-deepseek-harness > sweeper-glm-5.3-flash-codex | 0.36 | -16.29 to 16.72 | 0.02 | failure cap=0, failure cap=10, panel without sweeper-claude-fable-5-1-claude-code, panel without sweeper-grok-4.6-cursor, panel without sweeper-qwen3.8-flash-codex, without Cacti/cacti, without Cotonti/Cotonti, without InvoiceShelf/InvoiceShelf, without LimeSurvey/LimeSurvey, without adminerevo/adminerevo, without chevereto/chevereto, without forkcms/forkcms, without friendica/friendica, without mantisbt/mantisbt, without phpbb/phpbb, without phpservermon/phpservermon, without redaxo/core, without tastyigniter/TastyIgniter, without thelia/thelia, without typecho/typecho, without typemill/typemill, without xenocrat/chyrp-lite, without zencart/zencart | no |
| sweeper-glm-5.3-flash-codex > sweeper-kimi-k3-kimi-code | 0.46 | -14.50 to 15.76 | 0.01 | net weight=0.5, failure cap=50, without agentejo/cockpit, without eventum/eventum, without marcantondahmen/automad, without opendocman/opendocman, without phpList/phplist3, without q2a/question2answer | no |
| sweeper-kimi-k3-kimi-code > sweeper-gpt-6-astra-codex | 1.00 | -13.78 to 15.68 | 0.04 | net weight=1 | no |
| sweeper-gpt-6-astra-codex > sweeper-claude-opus-5-claude-code | 1.66 | -13.57 to 17.22 | 0.04 | none | no |
| sweeper-claude-opus-5-claude-code > sweeper-muse-spark-1.3-muse-code | 2.03 | -13.34 to 17.32 | 0.03 | net weight=0.5 | no |
| sweeper-muse-spark-1.3-muse-code > sweeper-deepseek-v4-pro-deepseek-harness | 0.37 | -14.63 to 16.11 | 0.01 | panel without sweeper-claude-opus-5-claude-code, without BookStackApp/BookStack, without DomainMOD/DomainMOD, without InvoicePlane/InvoicePlane, without InvoiceShelf/InvoiceShelf, without Piwigo/Piwigo, without dotclear/dotclear, without fluxbb/fluxbb, without galette/galette, without joomla/joomla-cms, without modxcms/revolution, without phpbb/phpbb, without tastyigniter/TastyIgniter, without typemill/typemill, without zenphoto/zenphoto | no |
| sweeper-deepseek-v4-pro-deepseek-harness > sweeper-gpt-5.6-luna-codex | 0.63 | -13.93 to 15.61 | 0.01 | without chevereto/chevereto, without cmsimple-xh/cmsimple-xh, without openemr/openemr, without shaarli/Shaarli | no |
| sweeper-gpt-5.6-luna-codex > sweeper-claude-fable-5-1-claude-code | 0.17 | -15.72 to 15.78 | 0.01 | net weight=0.9, net weight=1, failure cap=50, panel without sweeper-deepseek-v4-pro-deepseek-harness, panel without sweeper-deepseek-v4.1-flash-deepseek-harness, panel without sweeper-gpt-5.6-sol-codex, panel without sweeper-gpt-6-astra-codex, panel without sweeper-muse-spark-1.3-muse-code, without MISP/MISP, without Piwigo/Piwigo, without YOURLS/YOURLS, without ad-aures/castopod, without agentejo/cockpit, without ampache/ampache, without bolt/core, without coppermine-gallery/cpg1.6.x, without cubecart/v6, without cypht-org/cypht, without dokuwiki/dokuwiki, without dotclear/dotclear, without emlog/emlog, without eventum/eventum, without filegator/filegator, without flyspray/flyspray, without friendica/friendica, without gamonoid/icehrm, without grocy/grocy, without invoiceninja/invoiceninja, without koel/koel, without marcantondahmen/automad, without phpbb/phpbb, without pluxml/PluXml, without q2a/question2answer, without salesagility/SuiteCRM, without vrana/adminer, without wolfcms/wolfcms, without zenphoto/zenphoto | no |
| sweeper-claude-fable-5-1-claude-code > sweeper-gpt-5.6-sol-codex | 0.82 | -16.50 to 17.29 | 0.01 | net weight=1, failure cap=0, without shaarli/Shaarli | no |
| sweeper-gpt-5.6-sol-codex > sweeper-glm-5.3-codex | 1.07 | -14.50 to 17.38 | 0.01 | net weight=0.5 | no |
| sweeper-glm-5.3-codex > sweeper-qwen3.8-max-codex | 0.58 | -14.09 to 15.39 | 0.04 | failure cap=0, panel without sweeper-grok-4.6-cursor, without cmsimple-xh/cmsimple-xh, without crater-invoice-inc/crater, without galette/galette, without librenms/librenms, without phpbb/phpbb, without vrana/adminer, without xenocrat/chyrp-lite, without zenphoto/zenphoto | no |
| sweeper-qwen3.8-max-codex > sweeper-gpt-5.6-terra-codex | 1.75 | -15.30 to 19.26 | 0.04 | none | no |
| sweeper-gpt-5.6-terra-codex > sweeper-qwen3.8-flash-codex | 2.37 | -13.84 to 17.96 | 0.03 | none | no |
| sweeper-qwen3.8-flash-codex > sweeper-grok-4.6-cursor | 3.24 | -13.37 to 18.93 | 0.03 | none | no |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sweeper-deepseek-v4.1-flash-deepseek-harness | 26.9 (1) | 26.8 (1) | 26.9 (1) | 26.9 (1) | 26.9 (1) | 27.0 (1) | 27.1 (1) | 31.5 (2) | 29.7 (2) | 22.3 (1) |
| sweeper-glm-5.3-flash-codex | 26.6 (2) | 26.4 (3) | 26.5 (2) | 26.5 (2) | 26.6 (2) | 26.6 (2) | 26.3 (2) | 31.9 (1) | 29.8 (1) | 21.2 (3) |
| sweeper-kimi-k3-kimi-code | 26.1 (3) | 26.7 (2) | 26.5 (3) | 26.3 (3) | 25.9 (3) | 25.7 (4) | 25.9 (3) | 30.9 (3) | 29.0 (3) | 21.3 (2) |
| sweeper-gpt-6-astra-codex | 25.1 (4) | 24.0 (4) | 24.4 (4) | 24.7 (4) | 25.4 (4) | 25.8 (3) | 25.1 (4) | 29.1 (4) | 27.5 (4) | 21.1 (4) |
| sweeper-claude-opus-5-claude-code | 23.4 (5) | 21.7 (6) | 22.3 (5) | 22.9 (5) | 24.0 (5) | 24.6 (5) | 23.8 (5) | 27.9 (5) | 26.1 (5) | 18.9 (5) |
| sweeper-muse-spark-1.3-muse-code | 21.4 (6) | 21.9 (5) | 21.7 (6) | 21.6 (6) | 21.2 (6) | 21.0 (6) | 21.3 (6) | 26.0 (6) | 24.2 (6) | 16.8 (6) |
| sweeper-deepseek-v4-pro-deepseek-harness | 21.0 (7) | 21.6 (7) | 21.4 (7) | 21.2 (7) | 20.9 (7) | 20.7 (7) | 21.0 (7) | 25.7 (7) | 23.8 (7) | 16.3 (7) |
| sweeper-gpt-5.6-luna-codex | 20.4 (8) | 21.1 (8) | 20.8 (8) | 20.6 (8) | 20.2 (9) | 19.9 (10) | 20.8 (8) | 25.6 (8) | 23.5 (8) | 15.2 (9) |
| sweeper-claude-fable-5-1-claude-code | 20.2 (9) | 20.4 (9) | 20.3 (9) | 20.3 (9) | 20.2 (8) | 20.1 (9) | 20.0 (9) | 24.8 (10) | 23.0 (9) | 15.7 (8) |
| sweeper-gpt-5.6-sol-codex | 19.4 (10) | 18.3 (11) | 18.7 (10) | 19.0 (10) | 19.8 (10) | 20.1 (8) | 19.0 (10) | 24.9 (9) | 22.7 (10) | 13.9 (10) |
| sweeper-glm-5.3-codex | 18.3 (11) | 18.4 (10) | 18.4 (11) | 18.4 (11) | 18.3 (11) | 18.3 (11) | 18.4 (11) | 23.2 (12) | 21.3 (11) | 13.4 (11) |
| sweeper-qwen3.8-max-codex | 17.8 (12) | 17.9 (12) | 17.8 (12) | 17.8 (12) | 17.7 (12) | 17.7 (12) | 17.6 (12) | 23.5 (11) | 21.2 (12) | 12.0 (12) |
| sweeper-gpt-5.6-terra-codex | 16.0 (13) | 16.3 (13) | 16.2 (13) | 16.1 (13) | 15.9 (13) | 15.8 (13) | 16.2 (13) | 22.2 (13) | 19.7 (13) | 9.8 (13) |
| sweeper-qwen3.8-flash-codex | 13.6 (14) | 12.7 (14) | 13.0 (14) | 13.3 (14) | 14.0 (14) | 14.3 (14) | 13.6 (14) | 18.3 (14) | 16.4 (14) | 9.0 (14) |
| sweeper-grok-4.6-cursor | 10.4 (15) | 9.7 (15) | 9.9 (15) | 10.2 (15) | 10.6 (15) | 10.9 (15) | 10.4 (15) | 15.6 (15) | 13.5 (15) | 5.2 (15) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (6 of 923 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| sweeper-claude-fable-5-1-claude-code | 70 | 30 | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| sweeper-claude-opus-5-claude-code | 70 | 30 | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| sweeper-deepseek-v4-pro-deepseek-harness | 64 | 31 | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| sweeper-deepseek-v4.1-flash-deepseek-harness | 67 | 30 | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| sweeper-glm-5.3-codex | 55 | 30 | none |
| sweeper-glm-5.3-flash-codex | 53 | 30 | none |
| sweeper-gpt-5.6-luna-codex | 55 | 30 | none |
| sweeper-gpt-5.6-sol-codex | 60 | 30 | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| sweeper-gpt-5.6-terra-codex | 45 | 30 | none |
| sweeper-gpt-6-astra-codex | 75 | 32 | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| sweeper-grok-4.6-cursor | 71 | 31 | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| sweeper-kimi-k3-kimi-code | 65 | 31 | none |
| sweeper-muse-spark-1.3-muse-code | 62 | 30 | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| sweeper-qwen3.8-flash-codex | 73 | 31 | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| sweeper-qwen3.8-max-codex | 38 | 30 | none |
| (dedup panel) | 6 | 0 | none |

Tasks that lose their only reference: sweeper-claude-fable-5-1-claude-code: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-claude-opus-5-claude-code: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-deepseek-v4-pro-deepseek-harness: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-130`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-deepseek-v4.1-flash-deepseek-harness: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-glm-5.3-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-glm-5.3-flash-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-gpt-5.6-luna-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-gpt-5.6-sol-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-gpt-5.6-terra-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-gpt-6-astra-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-060`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-144`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-grok-4.6-cursor: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-174`, `sweeper-177`, `sweeper-180`; sweeper-kimi-k3-kimi-code: `sweeper-001`, `sweeper-026`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-muse-spark-1.3-muse-code: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-qwen3.8-flash-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-168`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`; sweeper-qwen3.8-max-codex: `sweeper-001`, `sweeper-029`, `sweeper-039`, `sweeper-042`, `sweeper-046`, `sweeper-052`, `sweeper-053`, `sweeper-057`, `sweeper-061`, `sweeper-070`, `sweeper-076`, `sweeper-084`, `sweeper-089`, `sweeper-093`, `sweeper-097`, `sweeper-098`, `sweeper-101`, `sweeper-105`, `sweeper-108`, `sweeper-123`, `sweeper-124`, `sweeper-132`, `sweeper-145`, `sweeper-152`, `sweeper-160`, `sweeper-165`, `sweeper-169`, `sweeper-170`, `sweeper-177`, `sweeper-180`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| AbanteCart/abantecart-src (1) | none |
| BookStackApp/BookStack (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| CE-PhoenixCart/PhoenixCart (1) | none |
| Cacti/cacti (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| Combodo/iTop (1) | none |
| Cotonti/Cotonti (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| Dolibarr/dolibarr (1) | none |
| DomainMOD/DomainMOD (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| ExpressionEngine/ExpressionEngine (1) | none |
| FOSSBilling/FOSSBilling (1) | none |
| FreshRSS/FreshRSS (1) | none |
| Froxlor/Froxlor (1) | none |
| GetSimpleCMS/GetSimpleCMS (1) | none |
| ImpressCMS/impresscms (1) | none |
| InvoicePlane/InvoicePlane (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| InvoiceShelf/InvoiceShelf (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| Kovah/LinkAce (1) | none |
| Leantime/leantime (1) | none |
| LibreBooking/app (1) | none |
| LimeSurvey/LimeSurvey (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| LinkStackOrg/LinkStack (1) | none |
| LycheeOrg/Lychee (1) | none |
| MISP/MISP (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| Piwigo/Piwigo (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| SergiX44/XBackBone (1) | none |
| SimpleMachines/SMF (1) | none |
| SolidInvoice/SolidInvoice (1) | none |
| Sylius/Sylius (1) | none |
| Typesetter/Typesetter (1) | none |
| WonderCMS/wondercms (1) | none |
| YOURLS/YOURLS (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| ad-aures/castopod (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| adminerevo/adminerevo (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| agentejo/cockpit (1) | sweeper-glm-5.3-flash-codex 2→3, sweeper-kimi-k3-kimi-code 3→2, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| akaunting/akaunting (1) | none |
| alexjustesen/speedtest-tracker (1) | none |
| alextselegidis/easyappointments (1) | none |
| ampache/ampache (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| anchorcms/anchor-cms (1) | none |
| bagisto/bagisto (1) | none |
| bolt/core (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| chevereto/chevereto (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-deepseek-v4-pro-deepseek-harness 7→8, sweeper-gpt-5.6-luna-codex 8→7 |
| cmsimple-xh/cmsimple-xh (1) | sweeper-deepseek-v4-pro-deepseek-harness 7→8, sweeper-gpt-5.6-luna-codex 8→7, sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| concretecms/concretecms (1) | none |
| coppermine-gallery/cpg1.6.x (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| craftcms/cms (1) | none |
| crater-invoice-inc/crater (1) | sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| cubecart/v6 (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| cydrobolt/polr (1) | none |
| cypht-org/cypht (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| danpros/htmly (1) | none |
| dokuwiki/dokuwiki (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| dotclear/dotclear (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| e107inc/e107 (1) | none |
| emlog/emlog (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| espocrm/espocrm (1) | none |
| eventum/eventum (1) | sweeper-glm-5.3-flash-codex 2→3, sweeper-kimi-k3-kimi-code 3→2, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| filegator/filegator (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| firefly-iii/firefly-iii (1) | none |
| flarum/framework (1) | none |
| flatpressblog/flatpress (1) | none |
| fluxbb/fluxbb (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| flyspray/flyspray (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| foodcoopshop/foodcoopshop (1) | none |
| forkcms/forkcms (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| fossar/selfoss (1) | none |
| freescout-help-desk/freescout (1) | none |
| friendica/friendica (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| galette/galette (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6, sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| gamonoid/icehrm (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| getkirby/kirby (1) | none |
| glpi-project/glpi (1) | none |
| grocy/grocy (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| grokability/snipe-it (1) | none |
| humhub/humhub (1) | none |
| invoiceninja/invoiceninja (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| joomla/joomla-cms (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| kanboard/kanboard (1) | none |
| kimai/kimai (1) | none |
| koel/koel (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| librenms/librenms (1) | sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| linuxserver/Heimdall (1) | none |
| litecart/litecart (1) | none |
| mantisbt/mantisbt (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| marcantondahmen/automad (1) | sweeper-glm-5.3-flash-codex 2→3, sweeper-kimi-k3-kimi-code 3→2, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| mautic/mautic (1) | none |
| modxcms/revolution (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| monicahq/monica (1) | none |
| mybb/mybb (1) | none |
| nilsteampassnet/TeamPass (1) | none |
| octobercms/october (1) | none |
| omeka/omeka-s (1) | none |
| opencart/opencart (1) | none |
| opencats/OpenCATS (1) | none |
| opendocman/opendocman (1) | sweeper-glm-5.3-flash-codex 2→3, sweeper-kimi-k3-kimi-code 3→2 |
| openemr/openemr (1) | sweeper-deepseek-v4-pro-deepseek-harness 7→8, sweeper-gpt-5.6-luna-codex 8→7 |
| opensourcepos/opensourcepos (1) | none |
| orangehrm/orangehrm (1) | none |
| osTicket/osTicket (1) | none |
| pagekit/pagekit (1) | none |
| part-db/Part-DB-server (1) | none |
| phpList/phplist3 (1) | sweeper-glm-5.3-flash-codex 2→3, sweeper-kimi-k3-kimi-code 3→2 |
| phpbb/phpbb (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8, sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| phpipam/phpipam (1) | none |
| phpmyadmin/phpmyadmin (1) | none |
| phpservermon/phpservermon (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| pluck-cms/pluck (1) | none |
| pluxml/PluXml (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| projectsend/projectsend (1) | none |
| q2a/question2answer (1) | sweeper-glm-5.3-flash-codex 2→3, sweeper-kimi-k3-kimi-code 3→2, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| redaxo/core (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| roundcube/roundcubemail (1) | none |
| salesagility/SuiteCRM (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| shaarli/Shaarli (1) | sweeper-deepseek-v4-pro-deepseek-harness 7→8, sweeper-gpt-5.6-luna-codex 8→7, sweeper-claude-fable-5-1-claude-code 9→10, sweeper-gpt-5.6-sol-codex 10→9 |
| silverstripe/silverstripe-framework (1) | none |
| tastyigniter/TastyIgniter (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| thelia/thelia (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| thirtybees/thirtybees (1) | none |
| thorsten/phpMyFAQ (1) | none |
| typecho/typecho (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| typemill/typemill (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6 |
| vrana/adminer (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8, sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| wallabag/wallabag (1) | none |
| wintercms/winter (1) | none |
| wolfcms/wolfcms (1) | sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8 |
| xenocrat/chyrp-lite (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1, sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |
| zencart/zencart (1) | sweeper-deepseek-v4.1-flash-deepseek-harness 1→2, sweeper-glm-5.3-flash-codex 2→1 |
| zenphoto/zenphoto (1) | sweeper-muse-spark-1.3-muse-code 6→7, sweeper-deepseek-v4-pro-deepseek-harness 7→6, sweeper-gpt-5.6-luna-codex 8→9, sweeper-claude-fable-5-1-claude-code 9→8, sweeper-glm-5.3-codex 11→12, sweeper-qwen3.8-max-codex 12→11 |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (128) | Solved by every model (17) | Solved by fewer (111) |
|---|---:|---:|---:|
| sweeper-deepseek-v4.1-flash-deepseek-harness | 26.9 (1) | 59.7 (4) | 21.9 (2) |
| sweeper-glm-5.3-flash-codex | 26.6 (2) | 73.5 (2) | 19.4 (5) |
| sweeper-kimi-k3-kimi-code | 26.1 (3) | 60.8 (3) | 20.8 (3) |
| sweeper-gpt-6-astra-codex | 25.1 (4) | 37.6 (13) | 23.2 (1) |
| sweeper-claude-opus-5-claude-code | 23.4 (5) | 44.1 (11) | 20.3 (4) |
| sweeper-muse-spark-1.3-muse-code | 21.4 (6) | 51.5 (9) | 16.8 (8) |
| sweeper-deepseek-v4-pro-deepseek-harness | 21.0 (7) | 47.9 (10) | 16.9 (7) |
| sweeper-gpt-5.6-luna-codex | 20.4 (8) | 55.6 (5) | 15.0 (9) |
| sweeper-claude-fable-5-1-claude-code | 20.2 (9) | 38.8 (12) | 17.4 (6) |
| sweeper-gpt-5.6-sol-codex | 19.4 (10) | 52.6 (7) | 14.3 (10) |
| sweeper-glm-5.3-codex | 18.3 (11) | 52.1 (8) | 13.2 (11) |
| sweeper-qwen3.8-max-codex | 17.8 (12) | 79.2 (1) | 8.3 (15) |
| sweeper-gpt-5.6-terra-codex | 16.0 (13) | 54.5 (6) | 10.1 (13) |
| sweeper-qwen3.8-flash-codex | 13.6 (14) | 27.9 (14) | 11.5 (12) |
| sweeper-grok-4.6-cursor | 10.4 (15) | 21.7 (15) | 8.7 (14) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **sweeper-deepseek-v4.1-flash-deepseek-harness − sweeper-glm-5.3-flash-codex = 1.01**: failed/failed -0.28 (19), failed/solved -3.13 (4), solved/failed 13.95 (18), solved/solved -9.53 (47). For sweeper-deepseek-v4.1-flash-deepseek-harness: `sweeper-004` +1.17 (solved/failed), `sweeper-027` +1.14 (solved/failed), `sweeper-146` +1.06 (solved/failed). For sweeper-glm-5.3-flash-codex: `sweeper-143` -1.05 (failed/solved), `sweeper-148` -1.01 (failed/solved), `sweeper-011` -0.96 (solved/solved).
- **sweeper-glm-5.3-flash-codex − sweeper-kimi-k3-kimi-code = 0.74**: failed/failed 0.28 (20), failed/solved -10.78 (16), solved/failed 5.05 (6), solved/solved 6.19 (47). For sweeper-glm-5.3-flash-codex: `sweeper-011` +1.14 (solved/failed), `sweeper-143` +0.98 (solved/failed), `sweeper-025` +0.96 (solved/failed). For sweeper-kimi-k3-kimi-code: `sweeper-158` -1.15 (failed/solved), `sweeper-146` -1.01 (failed/solved), `sweeper-141` -0.98 (failed/solved).
- **sweeper-kimi-k3-kimi-code − sweeper-gpt-6-astra-codex = 3.76**: failed/failed -0.28 (13), failed/solved -10.23 (15), solved/failed 3.75 (6), solved/solved 10.52 (57). For sweeper-kimi-k3-kimi-code: `sweeper-158` +1.03 (solved/failed), `sweeper-114` +0.86 (solved/solved), `sweeper-087` +0.85 (solved/solved). For sweeper-gpt-6-astra-codex: `sweeper-059` -1.16 (failed/solved), `sweeper-184` -1.12 (failed/solved), `sweeper-005` -0.89 (failed/solved).
- **sweeper-gpt-6-astra-codex − sweeper-claude-opus-5-claude-code = -0.38**: failed/failed -0.09 (11), failed/solved -5.43 (8), solved/failed 6.71 (11), solved/solved -1.56 (60). For sweeper-gpt-6-astra-codex: `sweeper-178` +0.93 (solved/failed), `sweeper-143` +0.84 (solved/failed), `sweeper-005` +0.79 (solved/failed). For sweeper-claude-opus-5-claude-code: `sweeper-190` -0.99 (failed/solved), `sweeper-036` -0.88 (solved/solved), `sweeper-080` -0.86 (failed/solved).
- **sweeper-claude-opus-5-claude-code − sweeper-muse-spark-1.3-muse-code = 2.12**: failed/failed 0.14 (17), failed/solved -2.80 (5), solved/failed 8.87 (12), solved/solved -4.08 (55). For sweeper-claude-opus-5-claude-code: `sweeper-051` +1.03 (solved/failed), `sweeper-190` +1.01 (solved/failed), `sweeper-035` +0.90 (solved/failed). For sweeper-muse-spark-1.3-muse-code: `sweeper-176` -1.00 (failed/solved), `sweeper-195` -0.95 (solved/solved), `sweeper-103` -0.79 (solved/solved).
- **sweeper-muse-spark-1.3-muse-code − sweeper-deepseek-v4-pro-deepseek-harness = 0.40**: failed/failed 0.10 (19), failed/solved -7.51 (11), solved/failed 6.28 (9), solved/solved 1.53 (52). For sweeper-muse-spark-1.3-muse-code: `sweeper-015` +1.22 (solved/failed), `sweeper-115` +1.19 (solved/failed), `sweeper-065` +1.13 (solved/failed). For sweeper-deepseek-v4-pro-deepseek-harness: `sweeper-128` -1.19 (failed/solved), `sweeper-021` -1.04 (failed/solved), `sweeper-163` -0.82 (solved/solved).
- **sweeper-deepseek-v4-pro-deepseek-harness − sweeper-gpt-5.6-luna-codex = -2.84**: failed/failed -0.20 (20), failed/solved -5.03 (7), solved/failed 7.22 (12), solved/solved -4.83 (47). For sweeper-deepseek-v4-pro-deepseek-harness: `sweeper-021` +1.09 (solved/failed), `sweeper-024` +1.01 (solved/failed), `sweeper-158` +0.84 (solved/failed). For sweeper-gpt-5.6-luna-codex: `sweeper-200` -0.90 (solved/solved), `sweeper-034` -0.90 (failed/solved), `sweeper-173` -0.90 (failed/solved).
- **sweeper-gpt-5.6-luna-codex − sweeper-claude-fable-5-1-claude-code = 4.37**: failed/failed 0.62 (18), failed/solved -8.49 (15), solved/failed 3.74 (4), solved/solved 8.49 (50). For sweeper-gpt-5.6-luna-codex: `sweeper-011` +1.06 (solved/failed), `sweeper-025` +1.00 (solved/failed), `sweeper-095` +0.97 (solved/solved). For sweeper-claude-fable-5-1-claude-code: `sweeper-100` -1.01 (failed/solved), `sweeper-135` -0.97 (failed/solved), `sweeper-107` -0.97 (failed/solved).
- **sweeper-claude-fable-5-1-claude-code − sweeper-gpt-5.6-sol-codex = 1.23**: failed/failed 0.42 (15), failed/solved -3.20 (5), solved/failed 7.60 (13), solved/solved -3.58 (53). For sweeper-claude-fable-5-1-claude-code: `sweeper-100` +1.04 (solved/failed), `sweeper-107` +1.04 (solved/failed), `sweeper-135` +1.02 (solved/failed). For sweeper-gpt-5.6-sol-codex: `sweeper-019` -0.94 (solved/solved), `sweeper-074` -0.87 (solved/solved), `sweeper-059` -0.84 (failed/solved).
- **sweeper-gpt-5.6-sol-codex − sweeper-glm-5.3-codex = -0.51**: failed/failed -0.68 (24), failed/solved -3.44 (5), solved/failed 6.75 (11), solved/solved -3.14 (48). For sweeper-gpt-5.6-sol-codex: `sweeper-074` +1.05 (solved/failed), `sweeper-044` +0.90 (solved/failed), `sweeper-036` +0.87 (solved/solved). For sweeper-glm-5.3-codex: `sweeper-141` -1.11 (failed/solved), `sweeper-013` -1.02 (failed/solved), `sweeper-024` -0.92 (solved/solved).
- **sweeper-glm-5.3-codex − sweeper-qwen3.8-max-codex = 0.52**: failed/failed -0.68 (27), failed/solved -6.31 (8), solved/failed 15.39 (24), solved/solved -7.88 (29). For sweeper-glm-5.3-codex: `sweeper-003` +1.16 (solved/failed), `sweeper-141` +1.13 (solved/failed), `sweeper-024` +1.07 (solved/failed). For sweeper-qwen3.8-max-codex: `sweeper-196` -1.17 (failed/solved), `sweeper-185` -1.08 (failed/solved), `sweeper-035` -0.94 (failed/solved).
- **sweeper-qwen3.8-max-codex − sweeper-gpt-5.6-terra-codex = 0.98**: failed/failed 0.53 (27), failed/solved -17.38 (20), solved/failed 12.41 (11), solved/solved 5.41 (23). For sweeper-qwen3.8-max-codex: `sweeper-154` +1.30 (solved/failed), `sweeper-008` +1.29 (solved/failed), `sweeper-007` +1.29 (solved/failed). For sweeper-gpt-5.6-terra-codex: `sweeper-015` -1.25 (failed/solved), `sweeper-003` -1.17 (failed/solved), `sweeper-062` -1.11 (failed/solved).
- **sweeper-gpt-5.6-terra-codex − sweeper-qwen3.8-flash-codex = 7.26**: failed/failed 0.90 (12), failed/solved -11.54 (27), solved/failed 2.91 (4), solved/solved 14.99 (39). For sweeper-gpt-5.6-terra-codex: `sweeper-197` +1.09 (solved/solved), `sweeper-148` +1.05 (solved/solved), `sweeper-003` +1.03 (solved/solved). For sweeper-qwen3.8-flash-codex: `sweeper-162` -1.08 (failed/solved), `sweeper-005` -0.89 (failed/solved), `sweeper-185` -0.81 (failed/solved).
- **sweeper-qwen3.8-flash-codex − sweeper-grok-4.6-cursor = 7.26**: failed/failed 0.08 (8), failed/solved -3.76 (12), solved/failed 8.47 (13), solved/solved 2.47 (57). For sweeper-qwen3.8-flash-codex: `sweeper-049` +1.13 (solved/failed), `sweeper-162` +1.13 (solved/failed), `sweeper-005` +0.91 (solved/failed). For sweeper-grok-4.6-cursor: `sweeper-136` -0.98 (failed/solved), `sweeper-103` -0.64 (solved/solved), `sweeper-115` -0.56 (failed/solved).

## Regenerate

```sh
python -m parsimony.stability examples/sweeper-php/score-panel.json examples/sweeper-php/sweeper-claude-fable-5-1-claude-code.jsonl examples/sweeper-php/sweeper-claude-opus-5-claude-code.jsonl examples/sweeper-php/sweeper-deepseek-v4.1-flash-deepseek-harness.jsonl examples/sweeper-php/sweeper-deepseek-v4-pro-deepseek-harness.jsonl examples/sweeper-php/sweeper-glm-5.3-codex.jsonl examples/sweeper-php/sweeper-glm-5.3-flash-codex.jsonl examples/sweeper-php/sweeper-gpt-5.6-luna-codex.jsonl examples/sweeper-php/sweeper-gpt-5.6-sol-codex.jsonl examples/sweeper-php/sweeper-gpt-5.6-terra-codex.jsonl examples/sweeper-php/sweeper-gpt-6-astra-codex.jsonl examples/sweeper-php/sweeper-grok-4.6-cursor.jsonl examples/sweeper-php/sweeper-kimi-k3-kimi-code.jsonl examples/sweeper-php/sweeper-muse-spark-1.3-muse-code.jsonl examples/sweeper-php/sweeper-qwen3.8-flash-codex.jsonl examples/sweeper-php/sweeper-qwen3.8-max-codex.jsonl --output examples/sweeper-php/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
