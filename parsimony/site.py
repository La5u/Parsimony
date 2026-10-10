"""Build the static results website from a frozen panel and measured JSONL (offline)."""
import argparse
import hashlib
import json
import random
import re
import statistics
from pathlib import Path

from .benchmark import read_jsonl
from .deepswe import display_name
from .external import attach
from .scoring import UNCALIBRATED, VERSION, measured, out_of_scope, score_records

TEMPLATE = Path(__file__).resolve().parent.parent / 'site' / 'template.html'
PREFIX = re.compile(r'^\d{8}_mini-v[\d.]+[_-]')
VERSION_OF = re.compile(r'^\d{8}_mini-(v[\d.]+)[_-]')
NAMES = {'claude-4-6-opus': 'Claude Opus 4.6', 'claude-4-5-sonnet-high': 'Claude Sonnet 4.5 (high)',
         'claude-4-5-haiku-high': 'Claude Haiku 4.5 (high)', 'deepseek-3-2-high': 'DeepSeek V3.2 (high)',
         'gemini-3-flash-high': 'Gemini 3 Flash (high)', 'glm-5-high': 'GLM-5 (high)',
         'gpt-5-2-high': 'GPT-5.2 (high)', 'gpt-5-mini': 'GPT-5 mini', 'kimi-k2-5-high': 'Kimi K2.5 (high)',
         'minimax-2-5-high': 'MiniMax M2.5 (high)', 'claude-4-5-opus-high': 'Claude Opus 4.5 (high)',
         'gpt-5-2-codex': 'GPT-5.2 Codex', 'gemini-3-pro-high': 'Gemini 3 Pro (high)',
         'Llama-4-Maverick-17B-Instruct': 'Llama 4 Maverick', 'claude-3-7-sonnet-20250219': 'Claude 3.7 Sonnet',
         'claude-sonnet-4-20250514': 'Claude Sonnet 4', 'gemini-2.5-pro': 'Gemini 2.5 Pro', 'o3-2025-04-16': 'o3',
         'claude-4-opus-20250514': 'Claude Opus 4', 'gpt-5-nano': 'GPT-5 nano', 'gpt-5': 'GPT-5',
         'gpt-oss-120b': 'gpt-oss-120b', 'glm-4.5': 'GLM-4.5', 'gemini-3-pro-preview-20251118': 'Gemini 3 Pro (preview)',
         'gpt-5.1-2025-11-13': 'GPT-5.1', 'gpt-5.1-codex': 'GPT-5.1 Codex', 'minimax-m2': 'MiniMax M2',
         'glm-4.6': 'GLM-4.6', 'devstral-2512': 'Devstral 2512', 'devstral-small-2512': 'Devstral Small 2512',
         'kimi-k2-thinking': 'Kimi K2 Thinking', 'gpt-5.2-2025-12-11': 'GPT-5.2',
         'gpt-5.2-2025-12-11-high': 'GPT-5.2 (high)', 'sonnet-4-5-20250929': 'Claude Sonnet 4.5',
         'claude-opus-4-5-20251101': 'Claude Opus 4.5', 'deepseek-v3.2-reasoner': 'DeepSeek V3.2 (reasoner)',
         'o4-mini-2025-04-16': 'o4-mini', 'qwen3-coder-480b-a35b-instruct': 'Qwen3-Coder 480B',
         'qwen2-5-coder-32b-instruct': 'Qwen2.5-Coder 32B', 'kimi-k2-instruct': 'Kimi K2 Instruct',
         'live-lite-gpt-5.6-sol-slingshot-3.4.0': 'GPT-5.6 Sol · Slingshot 3.4.0',
         'live-lite-gpt-5.5-agav-0.2.0-beta.2': 'GPT-5.5 · agav 0.2.0-beta.2',
         'live-lite-deepseek-v4.1-flash-tianxicode-0.1.423': 'DeepSeek V4.1 Flash · TianxiCode 0.1.423',
         'live-lite-claude-opus-4.8-aiwork': 'Claude Opus 4.8 · AiWork.Code',
         'live-multilang-gpt-5.6-sol-slingshot-3.4.0': 'GPT-5.6 Sol · Slingshot 3.4.0',
         'live-multilang-gpt-5.5-sweagent-medium': 'GPT-5.5 (medium) · SWE-agent'}


BENCHMARKS = {
    'verified': dict(name='SWE-bench Verified', url='https://www.swebench.com', reference="Maintainers' fix",
                     task_url='https://github.com/{owner}/{repo}/pull/{number}', task_link="Maintainers' pull request",
                     results="SWE-bench's published results", attempts=1),
    'deepswe': dict(name='DeepSWE', url='https://deepswe.datacurve.ai', reference='Reference solution',
                    task_url='https://github.com/datacurve-ai/deep-swe/tree/main/tasks/{task}', task_link='Task on GitHub',
                    results="DeepSWE's published results", attempts=4),
    'live': dict(name='SWE-bench Live Lite', url='https://swe-bench-live.github.io', reference='Reference solution',
                 task_url='https://github.com/{owner}/{repo}/pull/{number}', task_link="Maintainers' pull request",
                 results='public submitter evaluation reports', attempts=1,
                 harness_note='These are model + agent configurations, not a controlled model-only comparison. '
                              'Harnesses, prompts and execution protocols differ; see the cohort report.',
                 notice='Model identity and pass/fail are source-reported; historical evaluator inputs and protocol '
                        'compliance are not independently certified. Footprint rank uses all measured in-scope '
                        'attempts, including failures; missing footprints are not zero. Passing references are not required.'),
    'polybench': dict(name='SWE-PolyBench Verified', url='https://amazon-science.github.io/SWE-PolyBench/',
                      reference="Maintainers' fix", task_url='https://github.com/{owner}/{repo}/pull/{number}',
                      task_link="Maintainers' pull request", results='public submitter evaluation reports', attempts=1,
                      harness_note='Configurations use different agent harnesses and may have different retry/selection '
                                   'protocols. These are not controlled model-only comparisons.',
                      notice='Declared-candidate research measurements: historical evaluator inputs, retries and '
                             'temporal-isolation replacements are source-reported, not independently certified.'),
}


def published_sources(benchmark, language='python', root=None):
    """Describe each frozen board population without selecting successful attempts."""
    root = Path(root) if root is not None else TEMPLATE.parent.parent
    github = 'https://github.com/La5u/Parsimony/blob/main/'
    boards = [
        ('DeepSWE · Python', 'deepswe', 'python', 'deepswe-python', 'population.json', 'index.html'),
        ('DeepSWE · JavaScript', 'deepswe', 'javascript', 'deepswe-javascript', 'population.json', 'javascript.html'),
        ('DeepSWE · TypeScript', 'deepswe', 'typescript', 'deepswe-typescript', 'population.json', 'typescript.html'),
        ('DeepSWE · Go', 'deepswe', 'go', 'deepswe-go', 'population.json', 'go.html'),
        ('SWE-bench Verified', 'verified', 'python', 'mini-swe-agent-500', 'population.json', 'verified.html'),
        ('SWE-bench Live Lite', 'live', 'python', 'live-python', 'population-manifest.json', 'live.html'),
    ]
    sources = []
    for name, key, lang, directory, filename, board_url in boards:
        path = f'examples/{directory}/{filename}'
        raw = (root / path).read_bytes()
        manifest = json.loads(raw)
        tasks = manifest['tasks']
        attempts = 4 if key == 'deepswe' else 1
        if key == 'deepswe':
            groups = {}
            for task in tasks:
                base, separator, attempt = task.rpartition('#')
                if not separator or not base:
                    raise ValueError(f'{path}: invalid attempt ID {task!r}')
                groups.setdefault(base, set()).add(attempt)
            if any(ids != {'1', '2', '3', '4'} for ids in groups.values()):
                raise ValueError(f'{path}: each task must have four attempts (#1–#4)')
            count = len(groups)
        else:
            count = len(tasks)
        sources.append(dict(name=name, benchmark=key, language=lang, tasks=count,
                            attempts_per_task=attempts, population_per_model=len(tasks),
                            active=(benchmark == key and language == lang), board_url=board_url,
                            report_url=github + f'examples/{directory}/README.md',
                            manifest_url=github + path, manifest_sha256=hashlib.sha256(raw).hexdigest(),
                            dataset_sha256=manifest['dataset_sha256']))
    plan_path = 'examples/self-run/plan.json'
    if (root / plan_path).exists():
        # Owner-run pilot: plotted faded on the DeepSWE Python board, never ranked or pooled.
        raw = (root / plan_path).read_bytes()
        plan = json.loads(raw)
        planned = sorted({c['tasks'] * plan['attempts'] for c in plan['configurations']})
        sources.append(dict(name='Self-run pilot · DeepSWE Python tasks', benchmark='self-run', language=plan['language'],
                            tasks=len(plan['tasks']), attempts_per_task=plan['attempts'],
                            population_per_model=f'{planned[0]}–{planned[-1]}' if len(planned) > 1 else planned[0],
                            active=False, self_run=True, board_url='index.html',
                            report_url=github + 'examples/self-run/README.md', manifest_url=github + plan_path,
                            manifest_sha256=hashlib.sha256(raw).hexdigest(), deepswe_commit=plan['deepswe_commit']))
    return sources


def label(agent):
    if agent.startswith('deepswe-'):
        return display_name(agent)
    short = PREFIX.sub('', agent)
    return NAMES.get(short, short)


def company(agent):
    """Model developer, not the agent harness or hosting provider."""
    name = label(agent).lower()
    for prefixes, owner in (
        (('claude',), 'Anthropic'), (('gpt', 'o3', 'o4', 'o1'), 'OpenAI'),
        (('gemini',), 'Google'), (('deepseek',), 'DeepSeek'),
        (('qwen',), 'Alibaba'), (('grok',), 'xAI'), (('glm',), 'Z.ai'),
        (('kimi',), 'Moonshot AI'), (('minimax',), 'MiniMax'),
        (('llama', 'muse'), 'Meta'), (('devstral', 'mistral', 'codestral'), 'Mistral AI'),
    ):
        if name.startswith(prefixes):
            return owner
    return 'Other'


GENERATION = re.compile(r'\d+(?:\.\d+)*')


def generation(name):
    """(model line, version) from a display name: 'Claude Opus 4.8 (max)' -> ('claude opus', (4, 8))."""
    match = GENERATION.search(name)
    if not match:
        return name.lower(), ()
    return name[:match.start()].strip().lower(), tuple(int(part) for part in match.group().split('.'))


def newest_generation(names):
    """Names whose version is the highest of their model line (the text before the version)."""
    newest = {}
    for name in names:
        line, version = generation(name)
        newest[line] = max(newest.get(line, version), version)
    return {name for name in names if generation(name)[1] == newest[generation(name)[0]]}


def median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def bootstrap(board, draws, seed):
    """Paired task bootstrap over all tasks; unscored tasks enter at their lower and upper bounds.

    The CI runs from the 2.5% quantile of the resampled lower mean to the 97.5% quantile of the
    upper mean; the top share follows the midpoint. With point scores only this is the ordinary
    percentile bootstrap.
    """
    tasks = list(board[0]['tasks'])
    groups = {}
    for t in tasks:  # items task#attempt of one task are resampled together
        groups.setdefault(t.split('#', 1)[0], []).append(t)
    groups = list(groups.values())
    rng = random.Random(seed)
    lows = {e['agent']: [] for e in board}
    highs = {e['agent']: [] for e in board}
    top = dict.fromkeys(lows, 0.0)
    for _ in range(draws):
        drawn = [t for g in rng.choices(groups, k=len(groups)) for t in g]
        low = {e['agent']: statistics.fmean(e['tasks'][t]['lower'] for t in drawn) for e in board}
        high = {e['agent']: statistics.fmean(e['tasks'][t]['upper'] for t in drawn) for e in board}
        mid = {a: low[a] + high[a] for a in low}
        best = max(mid.values())
        winners = [a for a, v in mid.items() if abs(v - best) < 1e-12]
        for agent in low:
            lows[agent].append(low[agent])
            highs[agent].append(high[agent])
            top[agent] += (agent in winners) / len(winners)
    def quantile(values, p):
        ordered = sorted(values)
        return ordered[int(p * (len(ordered) - 1))]
    return len(tasks), {a: dict(ci=[quantile(lows[a], 0.025), quantile(highs[a], 0.975)], top=top[a] / draws)
                        for a in lows}


def build(panel, records, draws=2000, seed=42):
    # Rank by score, or by the midpoint of the possible range when some tasks are unscored.
    board = sorted(score_records(panel, records),
                   key=lambda e: -(e['score'] if e['score'] is not None else (e['lower'] + e['upper']) / 2))
    bounded = panel.get('calibration_policy') == UNCALIBRATED
    groups = {}
    for r in records:
        groups.setdefault(r['agent'], {})[r['task_id']] = r
    common, intervals = bootstrap(board, draws, seed)
    population_tasks = set(panel['tasks']) | {t for group in groups.values() for t in group}
    models = []
    for entry in board:
        group = groups[entry['agent']]
        ok = [group[t] for t, value in entry['tasks'].items() if value['status'] == 'resolved']
        statuses = [t['status'] for t in entry['tasks'].values()]
        solved_scores = [t['score'] for t in entry['tasks'].values() if t['status'] == 'resolved']
        solved_metrics = [r['metrics'] for r in ok]
        # Footprint ranking does not depend on correctness or reference coverage.
        footprint_records = [r for r in group.values() if measured(r)
                             and r['metrics'].get('mode') == 'full_file'
                             and not out_of_scope(r['metrics'])]
        measured_metrics = [r['metrics'] for r in footprint_records]
        solved_footprints = [r['metrics']['net_units'] for r in footprint_records if r['resolved']]
        # Failure penalty from the failures that could be measured; complete only when nothing is unscored.
        known_penalty = -sum(t['score'] for t in entry['tasks'].values()
                             if t['status'] == 'failed' and t['score'] is not None) / len(entry['tasks'])
        models.append(dict(
            agent=entry['agent'], name=label(entry['agent']), company=company(entry['agent']), score=entry['score'],
            footprint_population_count=max(len(population_tasks), max((r.get('benchmark_tasks', len(population_tasks))
                                                           for r in group.values()), default=len(population_tasks))),
            measured_attempts=len(measured_metrics),
            measured_net_mean=statistics.fmean(m['net_units'] for m in measured_metrics) if measured_metrics else None,
            # Same measured, in-scope population restricted to upstream-solved attempts.
            measured_solved_attempts=len(solved_footprints),
            measured_solved_net_mean=statistics.fmean(solved_footprints) if solved_footprints else None,
            measured_churn_mean=statistics.fmean(m['churn'] for m in measured_metrics) if measured_metrics else None,
            lower=entry['lower'], upper=entry['upper'], ci=intervals[entry['agent']]['ci'],
            top=intervals[entry['agent']]['top'],
            success_credit=entry['success_credit'], failure_penalty=entry['failure_penalty'],
            known_failure_penalty=known_penalty,
            solved_mean=statistics.fmean(solved_scores) if solved_scores else None,
            solved_net_mean=statistics.fmean(m['net_units'] for m in solved_metrics) if solved_metrics else None,
            solved_churn_mean=statistics.fmean(m['churn'] for m in solved_metrics) if solved_metrics else None,
            resolve_rate=entry['published_resolve_rate'],
            solved=statuses.count('resolved'), failed=statuses.count('failed'),
            unscored=sum(t['score'] is None for t in entry['tasks'].values()),
            net_units=median(r['metrics']['net_units'] for r in ok),
            churn=median(r['metrics']['churn'] for r in ok),
            token_churn=median(r['metrics'].get('token_churn') for r in ok),
            human_ratio=median(r.get('model_human_ratio') for r in ok)))
    models.sort(key=lambda m: (m['measured_net_mean'] is None,
                               m['measured_net_mean'] if m['measured_net_mean'] is not None else 0, m['name']))
    # Chart emphasis only: older generations and their labels are slightly lighter; rank ignores this.
    newest = newest_generation([m['name'] for m in models])
    for m in models:
        m['latest'] = m['name'] in newest
    order = [m['agent'] for m in models]
    tasks = []
    for task in panel['tasks']:
        cells = []
        human = None
        for agent in order:
            r = groups[agent].get(task)
            scored = next(e for e in board if e['agent'] == agent)['tasks'][task]
            m = (r or {}).get('metrics') or {}
            if r and r.get('human_metrics'):
                human = r['human_metrics']['churn']
            cell = [scored['status'][0] if scored['status'] != 'uncalibrated' else 'c',
                    m.get('net_units'), m.get('churn'),
                    None if scored['score'] is None else round(scored['score'], 1),
                    scored['lower'], scored['upper']]
            if bounded:
                cell.append('r' if r and r['resolved'] else
                            'f' if r and r.get('evaluation_result') == 'failed' else 'u')
            cells.append(cell)
        tasks.append([task, human, cells])
    footprint_tasks = []
    scored_tasks = {row[0]: row for row in tasks}
    for task in sorted(population_tasks):
        cells = []
        for index, agent in enumerate(order):
            r = groups[agent].get(task)
            eligible = bool(r and measured(r) and r['metrics'].get('mode') == 'full_file'
                            and not out_of_scope(r['metrics']))
            cell = list(scored_tasks[task][2][index]) if task in scored_tasks else ['u', None, None, None, None, None]
            while len(cell) < 7:
                cell.append(None)
            categories = set((r or {}).get('published_result_categories', []))
            cell[6] = ('r' if r and r['resolved'] else 'f' if r and
                       (r.get('evaluation_result') == 'failed' or
                        (categories & {'unresolved', 'failed', 'not_resolved'} and 'no_logs' not in categories)) else 'u')
            if eligible:
                cell[1:3] = [r['metrics']['net_units'], r['metrics']['churn']]
            cell.append(eligible)
            cells.append(cell)
        footprint_tasks.append([task, (scored_tasks.get(task) or [None, None])[1], cells])
    # Pooled panels label references agent#attempt; count models, not attempts.
    references = {r['agent'].split('#', 1)[0] for refs in panel['tasks'].values() for r in refs}
    versions = sorted({m.group(1) for a in order if (m := VERSION_OF.match(a))},
                      key=lambda v: tuple(int(x) for x in v[1:].split('.')))
    return dict(**(dict(calibration_policy=UNCALIBRATED,
                        uncalibrated_tasks=[t for t, refs in panel['tasks'].items() if not refs]) if bounded else {}),
                measurement_track=panel.get('measurement_track'),
                ranking_metric='measured-net-mean-v1', footprint_tasks=footprint_tasks,
                score_version=VERSION, panel=panel['name'], references=len(references), harness=versions, analyzer_version=panel['analyzer_version'],
                python_version=panel['python_version'], task_count=len(panel['tasks']),
                population_count=max(len(footprint_tasks), max((r.get('benchmark_tasks', len(footprint_tasks)) for r in records),
                                     default=len(footprint_tasks))),
                excluded_tasks=sorted({r['task_id'] for r in records} - panel['tasks'].keys()),
                bootstrap_tasks=common, draws=draws, models=models, tasks=tasks)


SELF_RUN_MODELS = {'gpt-6-luna': 'GPT-6 Luna', 'gpt-6-sol': 'GPT-6 Sol', 'gpt-6.1-sol': 'GPT-6.1 Sol',
                   'gpt-6-astra': 'GPT-6 Astra', 'gpt-5.6-sol': 'GPT-5.6 Sol', 'claude-haiku-5-5': 'Claude Haiku 5.5',
                   'claude-sonnet-5-5': 'Claude Sonnet 5.5', 'claude-opus-5-5': 'Claude Opus 5.5',
                   'claude-sonnet-5': 'Claude Sonnet 5'}
HARNESSES = {'pi': 'pi', 'claude-code': 'Claude Code'}


def self_run_models(records):
    """Unranked, ungraded owner-run configurations, summarised like measured board models."""
    groups = {}
    for r in records:
        if not r.get('self_run'):
            raise ValueError(f"{r['agent']}: not a self-run record")
        groups.setdefault(r['agent'], []).append(r)
    models = []
    for agent, group in sorted(groups.items()):
        provenance = group[0]['provenance']
        eligible = [r['metrics'] for r in group if measured(r) and r['metrics'].get('mode') == 'full_file'
                    and not out_of_scope(r['metrics'])]
        name = f"{SELF_RUN_MODELS.get(provenance['model'], provenance['model'])} ({provenance['reasoning_effort']})"
        models.append(dict(
            agent=agent, name=name, company=company(name), self_run=True, latest=True,
            harness=HARNESSES.get(provenance['harness'], provenance['harness']),
            tasks=len({r['task_id'].split('#', 1)[0] for r in group}), attempts=len(group),
            footprint_population_count=group[0]['benchmark_tasks'], measured_attempts=len(eligible),
            measured_net_mean=statistics.fmean(m['net_units'] for m in eligible) if eligible else None,
            measured_churn_mean=statistics.fmean(m['churn'] for m in eligible) if eligible else None,
            measured_solved_net_mean=None, resolve_rate=None))
    return models


def add_rank_ranges(models, sensitivity):
    """Set each model's 95% bootstrap rank range from the stability analysis; None when it is missing."""
    boot = sensitivity['bootstrap']['models']
    for model in models:
        entry = boot.get(model['agent'])
        model['rank_range'] = list(entry['rank_ci_95']) if entry else None


def render(data, standalone=True):
    # Escape '<' so no data string can close the embedding <script> element.
    payload = json.dumps(data, separators=(',', ':')).replace('<', '\\u003c')
    custom_js = TEMPLATE.with_name('custom-benchmark.js').read_text()
    page = (TEMPLATE.read_text().replace('__CUSTOM_BENCHMARK_JS__', custom_js)
            .replace('__PARSIMONY_DATA__', payload))
    if standalone:
        page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body>\n'
                + page + '\n</body>\n</html>\n')
    return page


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('panel')
    parser.add_argument('records', nargs='+')
    parser.add_argument('--output', default='site/index.html')
    parser.add_argument('--data', help='also write the page data as JSON here')
    parser.add_argument('--sensitivity', help='sensitivity.json from parsimony.stability; adds rank ranges')
    parser.add_argument('--fragment', action='store_true', help='omit the <html>/<head> wrapper')
    parser.add_argument('--benchmark', choices=sorted(BENCHMARKS), default='verified')
    parser.add_argument('--nav', action='append', default=[], metavar='LABEL=URL', help='link to another board')
    parser.add_argument('--self-run', nargs='+', default=[], metavar='JSONL',
                        help='self-run results (examples/self-run/results); plotted faded, never ranked')
    parser.add_argument('--external', help='pinned Artificial Analysis snapshot from parsimony.external; adds axes only')
    args = parser.parse_args()
    try:
        raw = Path(args.panel).read_bytes()
        data = build(json.loads(raw), [r for path in args.records for r in read_jsonl(path)])
        data['panel_sha256'] = hashlib.sha256(raw).hexdigest()
        data['benchmark'] = BENCHMARKS[args.benchmark]
        track = data.get('measurement_track') or {}
        data['sources'] = published_sources(args.benchmark, track.get('language') or 'python')
        data['nav'] = [dict(zip(('label', 'url'), item.split('=', 1))) for item in args.nav]
        if args.self_run:
            data['self_run_models'] = self_run_models([r for path in args.self_run for r in read_jsonl(path)])
        if args.external:
            snapshot = json.loads(Path(args.external).read_text())
            data['external'] = attach(data['models'], snapshot)
            attach(data.get('self_run_models', []), snapshot)
        if args.sensitivity:
            sensitivity = json.loads(Path(args.sensitivity).read_text())
            add_rank_ranges(data['models'], sensitivity)
            if sensitivity['bootstrap'].get('rank_policy'):
                data['rank_policy'] = sensitivity['bootstrap']['rank_policy']
            report = Path(args.sensitivity).with_suffix('.md').as_posix()
            data['sensitivity_url'] = f'https://github.com/La5u/Parsimony/blob/main/{report}'
        Path(args.output).write_text(render(data, not args.fragment))
        if args.data:
            Path(args.data).write_text(json.dumps(data, indent=1) + '\n')
        print(f'Wrote {args.output} (offline; no patch analysis)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
