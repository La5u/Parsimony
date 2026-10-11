"""Exploratory paired-task bootstrap and weight/cap sensitivity (not a score release)."""
import argparse
import json
import math
import random
import statistics
from pathlib import Path

from .benchmark import read_jsonl
from .scoring import (measured, metrics, out_of_scope, percentile, quantile, require,
                      require_measurement_track, task_score, unique)


def contributions(panel, records, net_weight=0.8, failure_cap=25, net_floor=None):
    """Per-task scores; ``net_floor=0`` removes credit for net deletion (anti-deletion variant)."""
    require(all(type(x) in (int, float) and math.isfinite(x)
                for x in (net_weight, failure_cap)) and
            0 <= net_weight <= 1 and failure_cap >= 0 and
            (net_floor is None or (type(net_floor) in (int, float) and math.isfinite(net_floor))),
            'invalid sensitivity parameters')
    records = list(records)
    def net(m):
        return m['net_units'] if net_floor is None else max(m['net_units'], net_floor)
    unique(records)
    groups = {}
    for r in records:
        groups.setdefault(r['agent'], {})[r['task_id']] = r
    require(bool(groups) and bool(panel.get('tasks')), 'nonempty candidate and task sets required')
    for task, refs in panel['tasks'].items():
        require(bool(refs), f'uncalibrated task {task}; use bounded stability analysis')
        require(len({ref['agent'] for ref in refs}) == len(refs), 'duplicate reference agent')
        bases = set()
        for ref in refs:
            require(not out_of_scope(metrics(ref['metrics'])), 'out-of-scope reference')
            bases.add((ref['provenance']['repo'], ref['provenance']['base_commit']))
        require(len(bases) == 1, f'mixed reference bases on {task}')
    out = {}
    for agent, group in groups.items():
        values = {}
        for task, refs in panel['tasks'].items():
            require(bool(refs), f'{agent}: uncalibrated task {task}; use bounded stability analysis')
            r = group.get(task)
            require(r is not None, f'{agent}: missing task {task}')
            require_measurement_track(panel, r)
            require((r['analyzer_version'], r['python_version']) ==
                    (panel['analyzer_version'], panel['python_version']), 'incompatible analyzer/Python version')
            if task_score(r, refs)['status'] in ('no_attempt', 'empty_patch'):
                values[task] = 0  # scored 0 by every variant, as in scoring and stability
                continue
            require(measured(r),
                    f'{agent}: incomplete measurements for {task}')
            require((r['provenance'].get('repo'), r['provenance'].get('base_commit')) ==
                    (refs[0]['provenance']['repo'], refs[0]['provenance']['base_commit']),
                    f'{agent}: base commit mismatch on {task}')
            m = metrics(r['metrics'])
            require(not out_of_scope(m), f'{agent}: every touched file out of scope on {task}')
            if r['resolved']:
                net_p = percentile(net(m), [net(ref['metrics']) for ref in refs])
                churn = percentile(m['churn'], [ref['metrics']['churn'] for ref in refs])
                values[task] = 1 + 99 * (net_weight * net_p + (1 - net_weight) * churn)
            else:
                categories = set(r.get('published_result_categories', []))
                require(bool(categories & {'unresolved', 'failed', 'not_resolved'}) and 'no_logs' not in categories,
                        f'{agent}: unknown failure category on {task}')
                scale = max(1, statistics.median(ref['metrics']['churn'] for ref in refs))
                growth = max(m['net_units'], 0)
                values[task] = -failure_cap * (net_weight * growth / (scale + growth) +
                                                (1 - net_weight) * m['churn'] / (scale + m['churn']))
        out[agent] = values
    return out


def sensitivity(panel, records, draws=2000, seed=42):
    require(type(draws) is int and draws > 0, 'positive integer draws required')
    records = list(records)
    scenarios = {}
    for weight, cap, floor in ((0.8, 25, None), (0.5, 25, None), (0.7, 25, None), (1.0, 25, None),
                               (0.8, 10, None), (0.8, 50, None), (0.8, 25, 0)):
        matrix = contributions(panel, records, weight, cap, floor)
        label = f'net={weight:g},failure_cap={cap}' + ('' if floor is None else f',net_floor={floor}')
        scenarios[label] = dict(
            sorted(((agent, statistics.mean(scores.values())) for agent, scores in matrix.items()),
                   key=lambda pair: -pair[1]))
    matrix = contributions(panel, records)
    tasks = list(panel['tasks'])
    # Repeated attempts share a task and must remain paired within each resample.
    clusters = {}
    for task in tasks:
        clusters.setdefault(task.split('#', 1)[0], []).append(task)
    clusters = list(clusters.values())
    rng = random.Random(seed)
    samples = {agent: [] for agent in matrix}
    top = {agent: 0.0 for agent in matrix}
    for _ in range(draws):
        drawn = [task for cluster in rng.choices(clusters, k=len(clusters)) for task in cluster]
        scores = {agent: statistics.mean(values[t] for t in drawn) for agent, values in matrix.items()}
        best = max(scores.values())
        winners = [agent for agent, value in scores.items() if abs(value - best) < 1e-12]
        for winner in winners:
            top[winner] += 1 / len(winners)
        for agent, value in scores.items():
            samples[agent].append(value)
    samples = {agent: sorted(values) for agent, values in samples.items()}
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
            json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write('\n')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
