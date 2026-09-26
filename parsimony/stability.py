"""Ranking stability under panel, weight, failure-cap and task-mix changes (analysis, not a score release).

Every variant is rescored from the frozen panel with a complete-data helper that tolerates unscored
tasks: point estimates use the tasks where every model has a point score, and bounds over the whole
panel show how far missing measurements could move each result.
"""
import argparse
import hashlib
import itertools
import json
import random
import re
import statistics
from pathlib import Path

from .benchmark import read_jsonl
from .scoring import metrics, percentile, require, score_records, task_score, unique

PREFIX = re.compile(r'^\d{8}_mini-v[\d.]+_')
NAMES = {'claude-4-6-opus': 'Claude Opus 4.6', 'claude-4-5-sonnet-high': 'Claude Sonnet 4.5',
         'claude-4-5-haiku-high': 'Claude Haiku 4.5', 'deepseek-3-2-high': 'DeepSeek V3.2',
         'gemini-3-flash-high': 'Gemini 3 Flash', 'glm-5-high': 'GLM-5', 'gpt-5-2-high': 'GPT-5.2',
         'gpt-5-mini': 'GPT-5 mini', 'kimi-k2-5-high': 'Kimi K2.5', 'minimax-2-5-high': 'MiniMax M2.5'}
WEIGHTS = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
CAPS = (0, 10, 25, 50)


def label(agent):
    short = PREFIX.sub('', agent)
    return NAMES.get(short, short)


def task_value(record, refs, net_weight, failure_cap, net_floor=None):
    """(score, lower, upper) for one task; score is None when only bounds are known.

    Classification and validation come from ``scoring.task_score``; the value is recomputed here so
    weights, cap and the net floor can vary.
    """
    status = task_score(record, refs)['status']
    if status == 'unknown':
        return None, -failure_cap, 100
    if status == 'no_attempt':
        return 0, 0, 0
    if status in ('missing_metrics', 'out_of_scope'):
        return (None, 1, 100) if record['resolved'] else (None, -failure_cap, 0)
    m = metrics(record['metrics'])
    def net(x):
        return x['net_units'] if net_floor is None else max(x['net_units'], net_floor)
    if status == 'resolved':
        net_p = percentile(net(m), [net(r['metrics']) for r in refs])
        churn_p = percentile(m['churn'], [r['metrics']['churn'] for r in refs])
        score = 1 + 99 * (net_weight * net_p + (1 - net_weight) * churn_p)
    else:
        scale = max(1, statistics.median(r['metrics']['churn'] for r in refs))
        growth = max(m['net_units'], 0)
        score = -failure_cap * (net_weight * growth / (scale + growth) +
                                (1 - net_weight) * m['churn'] / (scale + m['churn']))
    return score, score, score


def group(records):
    unique(records)
    out = {}
    for r in records:
        out.setdefault(r['agent'], {})[r['task_id']] = r
    return out


def matrix(panel, groups, net_weight, failure_cap, net_floor=None):
    """{agent: {task: (score, lower, upper)}} over every panel task; absent records are unknown."""
    require(0 <= net_weight <= 1 and failure_cap >= 0, 'invalid parameters')
    require(bool(groups) and bool(panel.get('tasks')), 'nonempty candidate and task sets required')
    for g in groups.values():
        for r in g.values():
            require((r['analyzer_version'], r['python_version']) ==
                    (panel['analyzer_version'], panel['python_version']), 'incompatible analyzer/Python version')
    return {agent: {task: task_value(g.get(task), refs, net_weight, failure_cap, net_floor)
                    for task, refs in panel['tasks'].items()}
            for agent, g in groups.items()}


def common_tasks(values, tasks=None):
    agents = list(values)
    tasks = list(values[agents[0]]) if tasks is None else tasks
    return [t for t in tasks if t in values[agents[0]] and all(values[a][t][0] is not None for a in agents)]


def summarize(values, tasks=None):
    """Point score on common tasks, bounds over all given tasks, and the resulting ranking."""
    agents = list(values)
    tasks = list(values[agents[0]]) if tasks is None else list(tasks)
    common = common_tasks(values, tasks)
    require(bool(common), 'no task has a point score for every model')
    out = {}
    for a in agents:
        cells = [values[a][t] for t in tasks]
        out[a] = dict(score=statistics.fmean(values[a][t][0] for t in common),
                      lower=statistics.fmean(c[1] for c in cells),
                      upper=statistics.fmean(c[2] for c in cells),
                      full_score=(statistics.fmean(c[0] for c in cells)
                                  if all(c[0] is not None for c in cells) else None))
    ranking = sorted(agents, key=lambda a: (-out[a]['score'], a))
    return dict(task_count=len(tasks), common_tasks=len(common), ranking=ranking, models=out)


def drop_agent(panel, agent):
    """The panel rebuilt without one model's references; tasks left without a reference are removed."""
    tasks, orphans = {}, []
    for task, refs in panel['tasks'].items():
        kept = [r for r in refs if r['agent'] != agent]
        if kept:
            tasks[task] = kept
        else:
            orphans.append(task)
    return dict(panel, name=f"{panel['name']}-without-{agent}", tasks=tasks), orphans


def dedup(panel):
    """Identical patches (same patch_sha256) count once per task."""
    tasks, removed = {}, 0
    for task, refs in panel['tasks'].items():
        seen, kept = set(), []
        for r in refs:
            key = r['provenance'].get('patch_sha256') or ('agent', r['agent'])
            if key not in seen:
                seen.add(key)
                kept.append(r)
        removed += len(refs) - len(kept)
        tasks[task] = kept
    return dict(panel, name=f"{panel['name']}-dedup", tasks=tasks), removed


def quantile(values, p):
    ordered = sorted(values)
    return ordered[int(p * (len(ordered) - 1))]


def bootstrap(values, tasks, draws=2000, seed=42):
    """Paired task bootstrap: rank distribution and paired CIs on every pairwise score difference."""
    require(type(draws) is int and draws > 0, 'positive integer draws required')
    agents = sorted(values)
    rng = random.Random(seed)
    means = {a: [] for a in agents}
    ranks = {a: [0] * len(agents) for a in agents}
    for _ in range(draws):
        drawn = rng.choices(tasks, k=len(tasks))
        scores = {a: statistics.fmean(values[a][t][0] for t in drawn) for a in agents}
        for position, a in enumerate(sorted(agents, key=lambda a: (-scores[a], a))):
            ranks[a][position] += 1
        for a in agents:
            means[a].append(scores[a])
    pairs = {}
    for a, b in itertools.permutations(agents, 2):
        diffs = [x - y for x, y in zip(means[a], means[b])]
        point = statistics.fmean(values[a][t][0] - values[b][t][0] for t in tasks)
        pairs[f'{a}|{b}'] = dict(difference=point, ci_95=[quantile(diffs, 0.025), quantile(diffs, 0.975)],
                                 p_greater=sum(d > 0 for d in diffs) / draws)
    models = {}
    for a in agents:
        expanded = [position + 1 for position, n in enumerate(ranks[a]) for _ in range(n)]
        models[a] = dict(score_ci_95=[quantile(means[a], 0.025), quantile(means[a], 0.975)],
                         rank_counts=ranks[a], rank_ci_95=[quantile(expanded, 0.025), quantile(expanded, 0.975)],
                         top_frequency=ranks[a][0] / draws)
    return dict(draws=draws, seed=seed, task_count=len(tasks), models=models, pairs=pairs)


def outcome(record):
    if record is None:
        return 'missing'
    return 'solved' if record['resolved'] else 'failed'


def pair_outcomes(values, groups, tasks, a, b, top=5):
    """Decompose mean(a) - mean(b) by outcome pair and list the tasks that contribute most."""
    n = len(tasks)
    by_kind, rows = {}, []
    for t in tasks:
        d = values[a][t][0] - values[b][t][0]
        kind = f'{outcome(groups[a].get(t))}/{outcome(groups[b].get(t))}'
        entry = by_kind.setdefault(kind, dict(tasks=0, contribution=0.0))
        entry['tasks'] += 1
        entry['contribution'] += d / n
        rows.append(dict(task=t, outcome=kind, a=values[a][t][0], b=values[b][t][0], contribution=d / n))
    rows.sort(key=lambda r: (-r['contribution'], r['task']))
    return dict(a=a, b=b, difference=sum(r['contribution'] for r in rows),
                by_outcome=dict(sorted(by_kind.items())), favoring_a=rows[:top],
                favoring_b=sorted(rows[-top:], key=lambda r: (r['contribution'], r['task'])))


def repo_of(refs):
    return refs[0]['provenance']['repo']


def analyze(panel, records, draws=2000, seed=42):
    groups = group(records)
    weight, cap = panel['net_weight'], panel['failure_cap']
    require(abs(weight + panel['churn_weight'] - 1) < 1e-9, 'panel weights must sum to one')
    base_values = matrix(panel, groups, weight, cap)
    base = summarize(base_values)
    published = {e['agent']: e['score'] for e in score_records(panel, records)}
    for agent, m in base['models'].items():
        if m['full_score'] is not None and published[agent] is not None:
            require(abs(m['full_score'] - published[agent]) < 1e-9, f'baseline disagrees with scoring: {agent}')
    order = base['ranking']
    adjacent = list(zip(order, order[1:]))

    scenarios = {'baseline': dict(family='baseline', **base)}
    for w in WEIGHTS:
        if w != weight:
            scenarios[f'net_weight={w:g}'] = dict(family='weights', **summarize(matrix(panel, groups, w, cap)))
    scenarios['net_floor=0'] = dict(family='weights', **summarize(matrix(panel, groups, weight, cap, 0)))
    for c in CAPS:
        if c != cap:
            scenarios[f'failure_cap={c}'] = dict(family='failure_cap', **summarize(matrix(panel, groups, weight, c)))

    leave_one_out = {}
    for agent in sorted(groups):
        reduced, orphans = drop_agent(panel, agent)
        scenarios[f'panel_without={agent}'] = dict(family='panel', **summarize(matrix(reduced, groups, weight, cap)))
        leave_one_out[agent] = dict(orphaned_tasks=orphans,
                                    references_removed=sum(r['agent'] == agent
                                                           for refs in panel['tasks'].values() for r in refs))
    deduped, removed = dedup(panel)
    scenarios['panel_dedup'] = dict(family='panel', **summarize(matrix(deduped, groups, weight, cap)))

    repos = {}
    for task, refs in panel['tasks'].items():
        repos.setdefault(repo_of(refs), []).append(task)
    for repo, tasks in sorted(repos.items()):
        rest = [t for t in panel['tasks'] if t not in set(tasks)]
        if common_tasks(base_values, rest):
            scenarios[f'without_repo={repo}'] = dict(family='task_mix', **summarize(base_values, rest))

    everyone = [t for t in panel['tasks'] if all(groups[a].get(t, {}).get('resolved') is True for a in groups)]
    rest = [t for t in panel['tasks'] if t not in set(everyone)]
    strata = {k: summarize(base_values, ts) for k, ts in (('solved_by_all', everyone), ('solved_by_fewer', rest))
              if common_tasks(base_values, ts)}

    common = common_tasks(base_values)
    boot = bootstrap(base_values, common, draws, seed)

    def position(ranking, agent):
        return ranking.index(agent) + 1
    rank_range = {a: [min(position(s['ranking'], a) for s in scenarios.values()),
                      max(position(s['ranking'], a) for s in scenarios.values())] for a in order}
    pairs = []
    for a, b in adjacent:
        flips = [name for name, s in scenarios.items() if s['models'][a]['score'] <= s['models'][b]['score']]
        stats = boot['pairs'][f'{a}|{b}']
        pairs.append(dict(a=a, b=b, difference=stats['difference'], ci_95=stats['ci_95'],
                          p_greater=stats['p_greater'], distinguishable=stats['ci_95'][0] > 0,
                          flips_in=flips,
                          flips_in_strata=[k for k, s in strata.items()
                                           if s['models'][a]['score'] <= s['models'][b]['score']],
                          bounds_separate=base['models'][a]['lower'] > base['models'][b]['upper'],
                          outcomes=pair_outcomes(base_values, groups, common, a, b)))
    return dict(status='analysis-not-a-score-release', score_version=panel['score_version'], panel=panel['name'],
                baseline=dict(net_weight=weight, churn_weight=panel['churn_weight'], failure_cap=cap),
                task_count=len(panel['tasks']), common_tasks=len(common),
                panel_references=sum(len(r) for r in panel['tasks'].values()), dedup_references_removed=removed,
                leave_one_out=leave_one_out, repositories={r: len(t) for r, t in sorted(repos.items())},
                strata_tasks={'solved_by_all': len(everyone), 'solved_by_fewer': len(rest)},
                ranking=order, rank_range=rank_range, adjacent_pairs=pairs,
                scenarios=scenarios, strata=strata, bootstrap=boot)


def fmt(x, digits=1):
    return f'{x:.{digits}f}'


def verdict(result):
    order, pairs = result['ranking'], result['adjacent_pairs']
    blocks, current = [], [order[0]]
    for p in pairs:
        if p['distinguishable'] and not p['flips_in']:
            blocks.append(current)
            current = [p['b']]
        else:
            current.append(p['b'])
    blocks.append(current)
    firm = [p for p in pairs if p['distinguishable'] and not p['flips_in']]
    tied = [p for p in pairs if not p['distinguishable']]
    lines = ['**Verdict.** Read the ranking as tiers, not positions: '
             + ' > '.join(' ≈ '.join(label(a) for a in b) for b in blocks)
             + ' (≈ marks an adjacent pair that is statistically tied or reversed by some variation).', '']
    scenarios = result['scenarios']
    moving = sorted({scenarios[f]['family'] for p in pairs for f in p['flips_in']})
    quiet = [f for f in ('weights', 'failure_cap', 'panel', 'task_mix') if f not in moving]
    families = dict(weights='net weight 0.5–1.0 and the net floor', failure_cap='failure cap 0–50',
                    panel='leave-one-model-out and deduplicated panels', task_mix='leave-one-repository-out')
    if quiet:
        lines.append('- **No rank changes at all** under ' + ' or '.join(families[f] for f in quiet) + '.')
    lines.append(f'- **Stable under every variation and statistically separated** ({len(firm)} of {len(pairs)} '
                 'adjacent pairs): ' + (', '.join(f"{label(p['a'])} > {label(p['b'])}" for p in firm) or 'none') + '.')
    lines.append(f'- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; {len(tied)} '
                 'pairs): ' + (', '.join(f"{label(p['a'])} vs {label(p['b'])}" for p in tied) or 'none') + '.')
    other = [p for p in pairs if p['distinguishable'] and p['flips_in']]
    if other:
        lines.append('- **Separated at baseline but reversed by some variation**: '
                     + '; '.join(f"{label(p['a'])} > {label(p['b'])} (reversed by "
                                 f"{', '.join(pretty(f) for f in p['flips_in'])})" for p in other) + '.')
    fixed = [a for a in order if result['rank_range'][a][0] == result['rank_range'][a][1]]
    lines.append('- **Rank never changes under any variation**: '
                 + (', '.join(f"{label(a)} ({result['rank_range'][a][0]})" for a in fixed) or 'none') + '.')
    strata = [f"{label(p['a'])} > {label(p['b'])} ({', '.join(k.replace('_', ' ') for k in p['flips_in_strata'])})"
              for p in pairs if p['flips_in_strata']]
    if strata:
        lines.append('- Difficulty strata answer a different question and are not counted as variations; they reverse '
                     + '; '.join(strata) + '.')
    return lines


def pretty(name):
    key, _, value = name.partition('=')
    if key == 'panel_without':
        return f'panel without {label(value)}'
    if key == 'without_repo':
        return f'without {value}'
    return name.replace('_', ' ')


def render(result, command):
    order = result['ranking']
    base = result['scenarios']['baseline']
    boot = result['bootstrap']
    b = result['baseline']
    out = ['# Score sensitivity: ten models × 500 tasks', '',
           f"Analysis, not a score release. Baseline `{result['score_version']}` "
           f"(net {b['net_weight']:g} / churn {b['churn_weight']:g}, failure cap {b['failure_cap']:g}), "
           f"panel `{result['panel']}`: {result['task_count']} tasks, point estimates on the "
           f"{result['common_tasks']} tasks where every model has a point score.", '']
    out += verdict(result)
    out += ['', '## Ranking', '',
            'Rank range is the best and worst rank across all weight, cap, panel and repository variations. '
            'Bootstrap is a paired task bootstrap on the common tasks '
            f"({boot['draws']} draws, seed {boot['seed']}). Bounds are over all {result['task_count']} tasks, "
            'treating unscored tasks at their best and worst case.', '',
            '| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |',
            '|---:|---|---:|---|---|---|---|---:|']
    for i, a in enumerate(order, 1):
        m, bm, rr = base['models'][a], boot['models'][a], result['rank_range'][a]
        bounds = fmt(m['lower']) if fmt(m['upper']) == fmt(m['lower']) else f"{fmt(m['lower'])}–{fmt(m['upper'])}"
        out.append(f"| {i} | {label(a)} | {fmt(m['score'])} | {fmt(bm['score_ci_95'][0])}–{fmt(bm['score_ci_95'][1])} "
                   f"| {bounds} | {rr[0]}–{rr[1]} | {bm['rank_ci_95'][0]}–{bm['rank_ci_95'][1]} "
                   f"| {bm['top_frequency']:.2f} |")
    out += ['', '## Adjacent pairs', '',
            '| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |',
            '|---|---:|---|---:|---|---|']
    for p in result['adjacent_pairs']:
        flips = ', '.join(pretty(f) for f in p['flips_in']) or 'none'
        out.append(f"| {label(p['a'])} > {label(p['b'])} | {fmt(p['difference'], 2)} | "
                   f"{fmt(p['ci_95'][0], 2)} to {fmt(p['ci_95'][1], 2)} | {p['p_greater']:.2f} | {flips} | "
                   f"{'yes' if p['bounds_separate'] else 'no'} |")
    out += ['', '## Weights and failure cap', '', 'Score on the common tasks; rank in parentheses.', '']
    names = [n for n, s in result['scenarios'].items() if s['family'] in ('baseline', 'weights', 'failure_cap')]
    out += scenario_table(result, names, order)
    out += ['', '## Panel composition', '',
            'Each model\'s references removed in turn (all ten still scored); tasks whose only reference was '
            'that model\'s patch leave the panel. The dedup panel counts byte-identical patches once per task '
            f"({result['dedup_references_removed']} of {result['panel_references']} references removed).", '',
            '| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |', '|---|---:|---:|---|']
    for a, info in result['leave_one_out'].items():
        s = result['scenarios'][f'panel_without={a}']
        out.append(f"| {label(a)} | {info['references_removed']} | {len(info['orphaned_tasks'])} | "
                   f"{changes(order, s['ranking'])} |")
    out.append(f"| (dedup panel) | {result['dedup_references_removed']} | 0 | "
               f"{changes(order, result['scenarios']['panel_dedup']['ranking'])} |")
    orphans = {a: i['orphaned_tasks'] for a, i in result['leave_one_out'].items() if i['orphaned_tasks']}
    if orphans:
        out += ['', 'Tasks that lose their only reference: ' + '; '.join(
            f"{label(a)}: {', '.join(f'`{t}`' for t in ts)}" for a, ts in orphans.items()) + '.']
    out += ['', '## Task mix', '', 'Leave one repository out (task count in parentheses):', '',
            '| Without | Ranking changes vs baseline |', '|---|---|']
    for repo, n in result['repositories'].items():
        s = result['scenarios'].get(f'without_repo={repo}')
        out.append(f"| {repo} ({n}) | {changes(order, s['ranking']) if s else 'no tasks left'} |")
    columns = [(f"All common ({result['common_tasks']})", base)] + [
        (f"{'Solved by every model' if k == 'solved_by_all' else 'Solved by fewer'} ({s['common_tasks']})", s)
        for k, s in result['strata'].items()]
    out += ['', 'Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes '
            'correctness and footprint.', '',
            '| Model | ' + ' | '.join(c for c, _ in columns) + ' |', '|---|' + '---:|' * len(columns)]
    for a in order:
        cells = [f"{fmt(s['models'][a]['score'])} ({s['ranking'].index(a) + 1})" for _, s in columns]
        out.append(f"| {label(a)} | " + ' | '.join(cells) + ' |')
    out += ['', '## What drives each adjacent gap', '',
            'Difference in mean score split by outcome (a/b), and the tasks that move it most. '
            'Contributions are per-task differences divided by the task count, so they sum to the gap.', '']
    for p in result['adjacent_pairs']:
        o = p['outcomes']
        parts = ', '.join(f"{k} {fmt(v['contribution'], 2)} ({v['tasks']})" for k, v in o['by_outcome'].items()
                          if abs(v['contribution']) >= 0.005)
        top_a = ', '.join(f"`{r['task']}` {r['contribution']:+.2f} ({r['outcome']})" for r in o['favoring_a'][:3])
        top_b = ', '.join(f"`{r['task']}` {r['contribution']:+.2f} ({r['outcome']})" for r in o['favoring_b'][:3])
        out.append(f"- **{label(p['a'])} − {label(p['b'])} = {fmt(o['difference'], 2)}**: {parts}. "
                   f"For {label(p['a'])}: {top_a}. For {label(p['b'])}: {top_b}.")
    out += ['', '## Regenerate', '', '```sh', command, '```', '',
            'All numbers are in [sensitivity.json](sensitivity.json). The analysis is conditional on this cohort '
            'and task population; the panel is built from the same models it ranks.', '']
    return '\n'.join(out)


def scenario_table(result, names, order):
    head = '| Model | ' + ' | '.join(f'`{n}`' for n in names) + ' |'
    rows = [head, '|---|' + '---:|' * len(names)]
    for a in order:
        cells = []
        for n in names:
            s = result['scenarios'][n]
            cells.append(f"{fmt(s['models'][a]['score'])} ({s['ranking'].index(a) + 1})")
        rows.append(f'| {label(a)} | ' + ' | '.join(cells) + ' |')
    return rows


def changes(base, ranking):
    moved = [f'{label(a)} {base.index(a) + 1}→{ranking.index(a) + 1}' for a in base
             if ranking.index(a) != base.index(a)]
    return ', '.join(moved) or 'none'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('panel')
    parser.add_argument('records', nargs='+')
    parser.add_argument('--draws', type=int, default=2000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', required=True, help='JSON output; the Markdown report goes next to it')
    parser.add_argument('--report', help='Markdown report path (default: OUTPUT with .md suffix)')
    args = parser.parse_args()
    try:
        raw = Path(args.panel).read_bytes()
        records = [r for path in args.records for r in read_jsonl(path)]
        result = analyze(json.loads(raw), records, args.draws, args.seed)
        result['panel_sha256'] = hashlib.sha256(raw).hexdigest()
        output = Path(args.output)
        output.write_text(json.dumps(result, indent=1, allow_nan=False) + '\n')
        folders = {str(Path(p).parent) for p in args.records}
        shown = args.records
        if len(folders) == 1:
            folder = Path(next(iter(folders)))
            if sorted(map(str, folder.glob('*.jsonl'))) == sorted(map(str, map(Path, args.records))):
                shown = [str(folder / '*.jsonl')]
        command = ' '.join(['python -m parsimony.stability', args.panel, *shown,
                            *(['--draws', str(args.draws)] if args.draws != 2000 else []),
                            *(['--seed', str(args.seed)] if args.seed != 42 else []), '--output', args.output])
        report = Path(args.report) if args.report else output.with_suffix('.md')
        report.write_text(render(result, command))
        print(f'Wrote {output} and {report} (offline; no patch analysis)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
