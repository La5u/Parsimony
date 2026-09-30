# Score sensitivity: 3 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `live-lite-python-300-80-20-v0.5`: 300 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (221 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: GPT-5.6 Sol · Slingshot 3.4.0 ≈ DeepSeek V4.1 Flash · TianxiCode 0.1.423 > Claude Opus 4.8 · AiWork.Code (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under net weight 0.5–1.0 and the net floor or failure cap 0–50 or leave-one-model-out and deduplicated panels or leave-one-repository-out.
- **Stable under every variation and statistically separated** (1 of 2 adjacent pairs): DeepSeek V4.1 Flash · TianxiCode 0.1.423 > Claude Opus 4.8 · AiWork.Code.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 1 pairs): GPT-5.6 Sol · Slingshot 3.4.0 vs DeepSeek V4.1 Flash · TianxiCode 0.1.423.
- **Midpoint rank never changes under any variation**: GPT-5.6 Sol · Slingshot 3.4.0 (1), DeepSeek V4.1 Flash · TianxiCode 0.1.423 (2), Claude Opus 4.8 · AiWork.Code (3).
- Difficulty strata answer a different question and are not counted as variations; they reverse DeepSeek V4.1 Flash · TianxiCode 0.1.423 > Claude Opus 4.8 · AiWork.Code (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 300 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | GPT-5.6 Sol · Slingshot 3.4.0 | 33.6 | 26.2–40.3 | 30.1–37.0 | 1–1 | 1–2 | 0.99 |
| 2 | DeepSeek V4.1 Flash · TianxiCode 0.1.423 | 29.5 | 22.6–35.5 | 26.4–32.5 | 2–2 | 1–2 | 0.01 |
| 3 | Claude Opus 4.8 · AiWork.Code | 12.2 | 4.2–20.3 | 7.9–16.5 | 3–3 | 3–3 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| GPT-5.6 Sol · Slingshot 3.4.0 > DeepSeek V4.1 Flash · TianxiCode 0.1.423 | 4.14 | -6.23 to 14.69 | 0.14 | none | no |
| DeepSeek V4.1 Flash · TianxiCode 0.1.423 > Claude Opus 4.8 · AiWork.Code | 17.28 | 5.10 to 28.50 | 1.00 | none | yes |

## Weights and failure cap

Score on the common tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-5.6 Sol · Slingshot 3.4.0 | 33.6 (1) | 32.8 (1) | 33.1 (1) | 33.3 (1) | 33.9 (1) | 34.1 (1) | 33.7 (1) | 37.0 (1) | 35.7 (1) | 30.2 (1) |
| DeepSeek V4.1 Flash · TianxiCode 0.1.423 | 29.5 (2) | 29.5 (2) | 29.5 (2) | 29.5 (2) | 29.4 (2) | 29.4 (2) | 29.6 (2) | 32.9 (2) | 31.5 (2) | 26.1 (2) |
| Claude Opus 4.8 · AiWork.Code | 12.2 (3) | 12.4 (3) | 12.3 (3) | 12.3 (3) | 12.1 (3) | 12.0 (3) | 12.0 (3) | 18.5 (3) | 16.0 (3) | 5.9 (3) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (22 of 509 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Opus 4.8 · AiWork.Code | 102 | 62 | none |
| DeepSeek V4.1 Flash · TianxiCode 0.1.423 | 202 | 77 | none |
| GPT-5.6 Sol · Slingshot 3.4.0 | 205 | 92 | none |
| (dedup panel) | 22 | 0 | none |

Tasks that lose their only reference: Claude Opus 4.8 · AiWork.Code: `aws-cloudformation__cfn-lint-3764`, `aws-cloudformation__cfn-lint-3767`, `aws-cloudformation__cfn-lint-3768`, `aws-cloudformation__cfn-lint-3770`, `aws-cloudformation__cfn-lint-3779`, `aws-cloudformation__cfn-lint-3789`, `aws-cloudformation__cfn-lint-3798`, `aws-cloudformation__cfn-lint-3805`, `aws-cloudformation__cfn-lint-3817`, `aws-cloudformation__cfn-lint-3821`, `aws-cloudformation__cfn-lint-3854`, `aws-cloudformation__cfn-lint-3855`, `aws-cloudformation__cfn-lint-3856`, `aws-cloudformation__cfn-lint-3862`, `aws-cloudformation__cfn-lint-3866`, `aws-cloudformation__cfn-lint-3875`, `aws-cloudformation__cfn-lint-3890`, `aws-cloudformation__cfn-lint-3947`, `aws-cloudformation__cfn-lint-3982`, `aws-cloudformation__cfn-lint-4002`, `aws-cloudformation__cfn-lint-4009`, `aws-cloudformation__cfn-lint-4016`, `aws-cloudformation__cfn-lint-4023`, `aws-cloudformation__cfn-lint-4032`, `aws-cloudformation__cfn-lint-4051`, `beeware__briefcase-2214`, `bridgecrewio__checkov-6893`, `bridgecrewio__checkov-6895`, `bridgecrewio__checkov-7002`, `conan-io__conan-17092`, `conan-io__conan-17514`, `cyclotruc__gitingest-134`, `falconry__falcon-2419`, `geopandas__geopandas-3471`, `huggingface__smolagents-285`, `huggingface__smolagents-405`, `huggingface__smolagents-731`, `huggingface__smolagents-843`, `instructlab__instructlab-3118`, `joke2k__faker-2142`, `kedro-org__kedro-4387`, `kedro-org__kedro-4406`, `kedro-org__kedro-4408`, `kedro-org__kedro-4427`, `kedro-org__kedro-4580`, `keras-team__keras-20534`, `matplotlib__matplotlib-29431`, `matplotlib__matplotlib-29781`, `mikedh__trimesh-2354`, `pydata__xarray-9586`, `pydata__xarray-9971`, `pypsa__pypsa-1091`, `pypsa__pypsa-1112`, `pypsa__pypsa-1172`, `pypsa__pypsa-1195`, `python-telegram-bot__python-telegram-bot-4617`, `python-telegram-bot__python-telegram-bot-4626`, `python-telegram-bot__python-telegram-bot-4673`, `reata__sqllineage-694`, `stanfordnlp__dspy-1741`, `urllib3__urllib3-3527`, `wemake-services__wemake-python-styleguide-3195`; DeepSeek V4.1 Flash · TianxiCode 0.1.423: `aws-cloudformation__cfn-lint-3764`, `aws-cloudformation__cfn-lint-3767`, `aws-cloudformation__cfn-lint-3768`, `aws-cloudformation__cfn-lint-3770`, `aws-cloudformation__cfn-lint-3779`, `aws-cloudformation__cfn-lint-3789`, `aws-cloudformation__cfn-lint-3798`, `aws-cloudformation__cfn-lint-3805`, `aws-cloudformation__cfn-lint-3817`, `aws-cloudformation__cfn-lint-3821`, `aws-cloudformation__cfn-lint-3854`, `aws-cloudformation__cfn-lint-3855`, `aws-cloudformation__cfn-lint-3856`, `aws-cloudformation__cfn-lint-3862`, `aws-cloudformation__cfn-lint-3866`, `aws-cloudformation__cfn-lint-3875`, `aws-cloudformation__cfn-lint-3890`, `aws-cloudformation__cfn-lint-3947`, `aws-cloudformation__cfn-lint-3982`, `aws-cloudformation__cfn-lint-4002`, `aws-cloudformation__cfn-lint-4009`, `aws-cloudformation__cfn-lint-4016`, `aws-cloudformation__cfn-lint-4023`, `aws-cloudformation__cfn-lint-4032`, `aws-cloudformation__cfn-lint-4051`, `beeware__briefcase-2214`, `bridgecrewio__checkov-6893`, `bridgecrewio__checkov-6895`, `bridgecrewio__checkov-7002`, `conan-io__conan-17092`, `conan-io__conan-17132`, `conan-io__conan-17514`, `cyclotruc__gitingest-115`, `cyclotruc__gitingest-134`, `deepset-ai__haystack-8619`, `deepset-ai__haystack-8879`, `falconry__falcon-2419`, `geopandas__geopandas-3471`, `huggingface__smolagents-285`, `huggingface__smolagents-405`, `huggingface__smolagents-731`, `huggingface__smolagents-843`, `instructlab__instructlab-3118`, `joke2k__faker-2142`, `kedro-org__kedro-4387`, `kedro-org__kedro-4406`, `kedro-org__kedro-4408`, `kedro-org__kedro-4427`, `kedro-org__kedro-4580`, `keras-team__keras-20396`, `keras-team__keras-20534`, `matplotlib__matplotlib-28933`, `matplotlib__matplotlib-29007`, `matplotlib__matplotlib-29431`, `matplotlib__matplotlib-29486`, `matplotlib__matplotlib-29689`, `matplotlib__matplotlib-29721`, `matplotlib__matplotlib-29781`, `mikedh__trimesh-2354`, `pydata__xarray-9586`, `pydata__xarray-9971`, `pypsa__pypsa-1091`, `pypsa__pypsa-1112`, `pypsa__pypsa-1172`, `pypsa__pypsa-1195`, `python-babel__babel-1164`, `python-control__python-control-1064`, `python-telegram-bot__python-telegram-bot-4617`, `python-telegram-bot__python-telegram-bot-4626`, `python-telegram-bot__python-telegram-bot-4673`, `reata__sqllineage-694`, `reflex-dev__reflex-4563`, `run-llama__llama_deploy-330`, `sphinx-doc__sphinx-12975`, `stanfordnlp__dspy-1741`, `urllib3__urllib3-3527`, `wemake-services__wemake-python-styleguide-3195`; GPT-5.6 Sol · Slingshot 3.4.0: `aws-cloudformation__cfn-lint-3764`, `aws-cloudformation__cfn-lint-3767`, `aws-cloudformation__cfn-lint-3768`, `aws-cloudformation__cfn-lint-3770`, `aws-cloudformation__cfn-lint-3779`, `aws-cloudformation__cfn-lint-3789`, `aws-cloudformation__cfn-lint-3798`, `aws-cloudformation__cfn-lint-3805`, `aws-cloudformation__cfn-lint-3817`, `aws-cloudformation__cfn-lint-3821`, `aws-cloudformation__cfn-lint-3854`, `aws-cloudformation__cfn-lint-3855`, `aws-cloudformation__cfn-lint-3856`, `aws-cloudformation__cfn-lint-3862`, `aws-cloudformation__cfn-lint-3866`, `aws-cloudformation__cfn-lint-3875`, `aws-cloudformation__cfn-lint-3890`, `aws-cloudformation__cfn-lint-3947`, `aws-cloudformation__cfn-lint-3982`, `aws-cloudformation__cfn-lint-4002`, `aws-cloudformation__cfn-lint-4009`, `aws-cloudformation__cfn-lint-4016`, `aws-cloudformation__cfn-lint-4023`, `aws-cloudformation__cfn-lint-4032`, `aws-cloudformation__cfn-lint-4051`, `beeware__briefcase-2214`, `bridgecrewio__checkov-6893`, `bridgecrewio__checkov-6895`, `bridgecrewio__checkov-7002`, `conan-io__conan-17092`, `conan-io__conan-17117`, `conan-io__conan-17514`, `conan-io__conan-17538`, `cyclotruc__gitingest-134`, `deepset-ai__haystack-9066`, `falconry__falcon-2419`, `flexget__flexget-4244`, `fonttools__fonttools-3726`, `geopandas__geopandas-3471`, `hiyouga__llama-factory-7505`, `huggingface__smolagents-285`, `huggingface__smolagents-405`, `huggingface__smolagents-731`, `huggingface__smolagents-843`, `instructlab__instructlab-2540`, `instructlab__instructlab-2585`, `instructlab__instructlab-2592`, `instructlab__instructlab-2825`, `instructlab__instructlab-2886`, `instructlab__instructlab-2927`, `instructlab__instructlab-3060`, `instructlab__instructlab-3118`, `joke2k__faker-2142`, `joke2k__faker-2162`, `kedro-org__kedro-4387`, `kedro-org__kedro-4406`, `kedro-org__kedro-4408`, `kedro-org__kedro-4427`, `kedro-org__kedro-4580`, `keras-team__keras-20534`, `koxudaxi__datamodel-code-generator-2327`, `matplotlib__matplotlib-29431`, `matplotlib__matplotlib-29781`, `mikedh__trimesh-2354`, `privacyidea__privacyidea-4206`, `privacyidea__privacyidea-4223`, `privacyidea__privacyidea-4226`, `privacyidea__privacyidea-4233`, `privacyidea__privacyidea-4251`, `pydata__xarray-9586`, `pydata__xarray-9971`, `pypsa__pypsa-1091`, `pypsa__pypsa-1112`, `pypsa__pypsa-1172`, `pypsa__pypsa-1195`, `python-telegram-bot__python-telegram-bot-4617`, `python-telegram-bot__python-telegram-bot-4626`, `python-telegram-bot__python-telegram-bot-4673`, `reata__sqllineage-694`, `reflex-dev__reflex-4129`, `reflex-dev__reflex-4711`, `reflex-dev__reflex-4720`, `reflex-dev__reflex-5039`, `run-llama__llama_deploy-458`, `sissbruecker__linkding-995`, `stanford-crfm__helm-3467`, `stanfordnlp__dspy-1609`, `stanfordnlp__dspy-1741`, `streamlink__streamlink-6381`, `tox-dev__tox-3409`, `urllib3__urllib3-3527`, `wemake-services__wemake-python-styleguide-3195`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| Delgan/loguru (2) | none |
| Flexget/Flexget (2) | none |
| Kozea/WeasyPrint (5) | none |
| PyPSA/PyPSA (4) | none |
| aiogram/aiogram (1) | none |
| amoffat/sh (1) | none |
| arviz-devs/arviz (1) | none |
| aws-cloudformation/cfn-lint (26) | none |
| beancount/beancount (1) | none |
| beetbox/beets (3) | none |
| beeware/briefcase (4) | none |
| bridgecrewio/checkov (3) | none |
| conan-io/conan (30) | none |
| cyclotruc/gitingest (3) | none |
| deepset-ai/haystack (16) | none |
| dynaconf/dynaconf (4) | none |
| encode/starlette (1) | none |
| facebookresearch/hydra (1) | none |
| falconry/falcon (2) | none |
| feast-dev/feast (1) | none |
| fonttools/fonttools (2) | none |
| geopandas/geopandas (1) | none |
| hiyouga/LLaMA-Factory (1) | none |
| huggingface/smolagents (4) | none |
| icloud-photos-downloader/icloud_photos_downloader (1) | none |
| instructlab/instructlab (11) | none |
| ipython/ipython (4) | none |
| iterative/dvc (1) | none |
| jazzband/tablib (1) | none |
| joke2k/faker (5) | none |
| jupyterlab/jupyter-ai (3) | none |
| kedro-org/kedro (5) | none |
| keras-team/keras (7) | none |
| koxudaxi/datamodel-code-generator (3) | none |
| kubernetes-client/python (1) | none |
| matplotlib/matplotlib (12) | none |
| mikedh/trimesh (2) | none |
| modelcontextprotocol/python-sdk (2) | none |
| pallets/flask (2) | none |
| patroni/patroni (1) | none |
| pdm-project/pdm (7) | none |
| privacyidea/privacyidea (5) | none |
| projectmesa/mesa (5) | none |
| pvlib/pvlib-python (7) | none |
| pybamm-team/PyBaMM (3) | none |
| pydata/xarray (7) | none |
| pylint-dev/pylint (5) | none |
| pypa/twine (1) | none |
| python-babel/babel (5) | none |
| python-control/python-control (3) | none |
| python-telegram-bot/python-telegram-bot (3) | none |
| pytorch/torchtune (3) | none |
| qtile/qtile (1) | none |
| reata/sqllineage (2) | none |
| reflex-dev/reflex (12) | none |
| run-llama/llama_deploy (8) | none |
| scrapy-plugins/scrapy-splash (1) | none |
| shapely/shapely (3) | none |
| sissbruecker/linkding (5) | none |
| sphinx-doc/sphinx (6) | none |
| stanford-crfm/helm (1) | none |
| stanfordnlp/dspy (4) | none |
| streamlink/streamlink (7) | none |
| sympy/sympy (1) | none |
| theOehrly/Fast-F1 (1) | none |
| tox-dev/tox (2) | none |
| urllib3/urllib3 (1) | none |
| wemake-services/wemake-python-styleguide (5) | none |
| wireservice/csvkit (2) | none |
| yt-dlp/yt-dlp (4) | none |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All common (221) | Solved by every model (78) | Solved by fewer (143) |
|---|---:|---:|---:|
| GPT-5.6 Sol · Slingshot 3.4.0 | 33.6 (1) | 51.9 (1) | 26.9 (1) |
| DeepSeek V4.1 Flash · TianxiCode 0.1.423 | 29.5 (2) | 49.0 (3) | 22.3 (2) |
| Claude Opus 4.8 · AiWork.Code | 12.2 (3) | 50.5 (2) | -1.8 (3) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **GPT-5.6 Sol · Slingshot 3.4.0 − DeepSeek V4.1 Flash · TianxiCode 0.1.423 = 3.76**: failed/solved -7.73 (30), solved/failed 7.88 (31), solved/solved 3.60 (169). For GPT-5.6 Sol · Slingshot 3.4.0: `pybamm-team__pybamm-4816` +0.33 (solved/failed), `theoehrly__fast-f1-699` +0.32 (solved/failed), `koxudaxi__datamodel-code-generator-2327` +0.31 (solved/failed). For DeepSeek V4.1 Flash · TianxiCode 0.1.423: `matplotlib__matplotlib-29258` -0.39 (failed/solved), `keras-team__keras-20443` -0.38 (failed/solved), `mikedh__trimesh-2363` -0.33 (failed/solved).
- **DeepSeek V4.1 Flash · TianxiCode 0.1.423 − Claude Opus 4.8 · AiWork.Code = 23.22**: failed/solved -1.30 (6), solved/failed 25.33 (102), solved/solved -0.81 (96). For DeepSeek V4.1 Flash · TianxiCode 0.1.423: `beancount__beancount-931` +0.42 (solved/failed), `conan-io__conan-17517` +0.40 (solved/failed), `run-llama__llama_deploy-399` +0.37 (solved/failed). For Claude Opus 4.8 · AiWork.Code: `shapely__shapely-2255` -0.29 (solved/solved), `instructlab__instructlab-2572` -0.27 (failed/solved), `beeware__briefcase-2075` -0.24 (failed/solved).

## Regenerate

```sh
python -m parsimony.stability examples/live-python/score-panel.json examples/live-python/deepseek-v4.1-flash.jsonl examples/live-python/gpt-5.6-sol.jsonl examples/live-python/claude-opus-4.8.jsonl --output examples/live-python/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
