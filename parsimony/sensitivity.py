"""Exploratory paired-task bootstrap and weight/cap sensitivity (not a score release)."""
import argparse
import json
import random
import statistics
from pathlib import Path

from .benchmark import read_jsonl
from .scoring import metrics, percentile, require, unique


def contributions(panel, records, net_weight=0.7, failure_cap=25):
    require(0 <= net_weight <= 1 and failure_cap >= 0, 'invalid sensitivity parameters')
    unique(records)
    groups = {}
    for r in records:
        groups.setdefault(r['agent'], {})[r['task_id']] = r
    require(bool(groups) and bool(panel.get('tasks')), 'nonempty candidate and task sets required')
    out = {}
    for agent, group in groups.items():
        values = {}
        for task, refs in panel['tasks'].items():
            r = group.get(task)
            require(r is not None, f'{agent}: missing task {task}')
            require((r['analyzer_version'], r['python_version']) ==
                    (panel['analyzer_version'], panel['python_version']), 'incompatible analyzer/Python version')
            require(r['analysis_status'] == 'ok' and r.get('metrics'),
                    f'{agent}: incomplete measurements for {task}')
            require((r['provenance'].get('repo'), r['provenance'].get('base_commit')) ==
                    (refs[0]['provenance']['repo'], refs[0]['provenance']['base_commit']),
                    f'{agent}: base commit mismatch on {task}')
            m = metrics(r['metrics'])
            if r['resolved']:
                net = percentile(m['net_tokens'], [ref['metrics']['net_tokens'] for ref in refs])
                churn = percentile(m['churn'], [ref['metrics']['churn'] for ref in refs])
                values[task] = 1 + 99 * (net_weight * net + (1 - net_weight) * churn)
            else:
                categories = set(r.get('published_result_categories', []))
                require(bool(categories & {'unresolved', 'failed', 'not_resolved'}) and 'no_logs' not in categories,
                        f'{agent}: unknown failure category on {task}')
                scale = max(1, statistics.median(ref['metrics']['churn'] for ref in refs))
                growth = max(m['net_tokens'], 0)
                values[task] = -failure_cap * (net_weight * growth / (scale + growth) +
                                                (1 - net_weight) * m['churn'] / (scale + m['churn']))
        out[agent] = values
    return out


def sensitivity(panel, records, draws=2000, seed=42):
    require(type(draws) is int and draws > 0, 'positive integer draws required')
    scenarios = {}
    for weight, cap in ((0.5, 25), (0.7, 25), (1.0, 25), (0.7, 10), (0.7, 50)):
        matrix = contributions(panel, records, weight, cap)
        scenarios[f'net={weight:g},failure_cap={cap}'] = dict(
            sorted(((agent, statistics.mean(scores.values())) for agent, scores in matrix.items()),
                   key=lambda pair: -pair[1]))
    matrix = contributions(panel, records)
    tasks = list(panel['tasks'])
    rng = random.Random(seed)
    samples = {agent: [] for agent in matrix}
    top = {agent: 0.0 for agent in matrix}
    for _ in range(draws):
        drawn = rng.choices(tasks, k=len(tasks))
        scores = {agent: statistics.mean(values[t] for t in drawn) for agent, values in matrix.items()}
        best = max(scores.values())
        winners = [agent for agent, value in scores.items() if abs(value - best) < 1e-12]
        for winner in winners:
            top[winner] += 1 / len(winners)
        for agent, value in scores.items():
            samples[agent].append(value)
    def quantile(values, p):
        ordered = sorted(values)
        return ordered[int(p * (len(ordered) - 1))]
    return dict(status='beta-exploratory-conditional-on-fixed-tasks-and-reference-panel',
                task_count=len(tasks), draws=draws, seed=seed, scenario_scores=scenarios,
                bootstrap={agent: {'score_ci_95': [quantile(values, 0.025), quantile(values, 0.975)],
                                   'top_frequency': top[agent] / draws}
                           for agent, values in sorted(samples.items())})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('panel')
    parser.add_argument('records', nargs='+')
    parser.add_argument('--draws', type=int, default=2000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        panel = json.loads(Path(args.panel).read_text())
        records = [r for path in args.records for r in read_jsonl(path)]
        result = sensitivity(panel, records, args.draws, args.seed)
        with Path(args.output).open('w') as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write('\n')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
