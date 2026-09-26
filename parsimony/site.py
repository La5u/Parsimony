"""Build the static results website from a frozen panel and measured JSONL (offline)."""
import argparse
import hashlib
import json
import random
import re
import statistics
from pathlib import Path

from .benchmark import read_jsonl
from .scoring import VERSION, score_records

TEMPLATE = Path(__file__).resolve().parent.parent / 'site' / 'template.html'
PREFIX = re.compile(r'^\d{8}_mini-v[\d.]+_')
NAMES = {'claude-4-6-opus': 'Claude Opus 4.6', 'claude-4-5-sonnet-high': 'Claude Sonnet 4.5 (high)',
         'claude-4-5-haiku-high': 'Claude Haiku 4.5 (high)', 'deepseek-3-2-high': 'DeepSeek V3.2 (high)',
         'gemini-3-flash-high': 'Gemini 3 Flash (high)', 'glm-5-high': 'GLM-5 (high)',
         'gpt-5-2-high': 'GPT-5.2 (high)', 'gpt-5-mini': 'GPT-5 mini', 'kimi-k2-5-high': 'Kimi K2.5 (high)',
         'minimax-2-5-high': 'MiniMax M2.5 (high)'}


def label(agent):
    short = PREFIX.sub('', agent)
    return NAMES.get(short, short)


def median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def bootstrap(board, draws, seed):
    """Paired task bootstrap over tasks where every entry has a point score."""
    tasks = [t for t in board[0]['tasks'] if all(e['tasks'][t]['score'] is not None for e in board)]
    rng = random.Random(seed)
    samples = {e['agent']: [] for e in board}
    top = dict.fromkeys(samples, 0.0)
    for _ in range(draws):
        drawn = rng.choices(tasks, k=len(tasks))
        means = {e['agent']: statistics.fmean(e['tasks'][t]['score'] for t in drawn) for e in board}
        best = max(means.values())
        winners = [a for a, v in means.items() if abs(v - best) < 1e-12]
        for agent, value in means.items():
            samples[agent].append(value)
            top[agent] += (agent in winners) / len(winners)
    def quantile(values, p):
        ordered = sorted(values)
        return ordered[int(p * (len(ordered) - 1))]
    return len(tasks), {a: dict(ci=[quantile(v, 0.025), quantile(v, 0.975)], top=top[a] / draws)
                        for a, v in samples.items()}


def build(panel, records, draws=2000, seed=42):
    # Rank by score, or by the midpoint of the possible range when some tasks are unscored.
    board = sorted(score_records(panel, records),
                   key=lambda e: -(e['score'] if e['score'] is not None else (e['lower'] + e['upper']) / 2))
    groups = {}
    for r in records:
        groups.setdefault(r['agent'], {})[r['task_id']] = r
    common, intervals = bootstrap(board, draws, seed)
    models = []
    for entry in board:
        group = groups[entry['agent']]
        ok = [r for r in group.values() if r['resolved'] and r['analysis_status'] == 'ok'
              and r['metrics']['churn'] is not None]
        statuses = [t['status'] for t in entry['tasks'].values()]
        solved_scores = [t['score'] for t in entry['tasks'].values() if t['status'] == 'resolved']
        # Failure penalty from the failures that could be measured; complete only when nothing is unscored.
        known_penalty = -sum(t['score'] for t in entry['tasks'].values()
                             if t['status'] == 'failed' and t['score'] is not None) / len(entry['tasks'])
        models.append(dict(
            agent=entry['agent'], name=label(entry['agent']), score=entry['score'],
            lower=entry['lower'], upper=entry['upper'], ci=intervals[entry['agent']]['ci'],
            top=intervals[entry['agent']]['top'],
            success_credit=entry['success_credit'], failure_penalty=entry['failure_penalty'],
            known_failure_penalty=known_penalty,
            solved_mean=statistics.fmean(solved_scores) if solved_scores else None,
            resolve_rate=entry['published_resolve_rate'],
            solved=statuses.count('resolved'), failed=statuses.count('failed'),
            unscored=sum(t['score'] is None for t in entry['tasks'].values()),
            net_units=median(r['metrics']['net_units'] for r in ok),
            churn=median(r['metrics']['churn'] for r in ok),
            token_churn=median(r['metrics'].get('token_churn') for r in ok),
            human_ratio=median(r.get('model_human_ratio') for r in ok)))
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
            cells.append([scored['status'][0], m.get('net_units'), m.get('churn'),
                          None if scored['score'] is None else round(scored['score'], 1)])
        tasks.append([task, human, cells])
    return dict(score_version=VERSION, panel=panel['name'], analyzer_version=panel['analyzer_version'],
                python_version=panel['python_version'], task_count=len(panel['tasks']),
                bootstrap_tasks=common, draws=draws, models=models, tasks=tasks)


def tiers(sensitivity):
    """Tier per agent: a new tier starts after each adjacent pair that is distinguishable and never flips."""
    pairs = sensitivity['adjacent_pairs']
    tier = 1
    result = {pairs[0]['a']: tier} if pairs else {a: 1 for a in sensitivity.get('ranking', [])}
    for pair in pairs:
        if pair['distinguishable'] and not pair['flips_in']:
            tier += 1
        result[pair['b']] = tier
    return result


def render(data, standalone=True):
    # Escape '<' so no data string can close the embedding <script> element.
    payload = json.dumps(data, separators=(',', ':')).replace('<', '\\u003c')
    page = TEMPLATE.read_text().replace('__PARSIMONY_DATA__', payload)
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
    parser.add_argument('--sensitivity', help='sensitivity.json from parsimony.stability; adds tiers')
    parser.add_argument('--fragment', action='store_true', help='omit the <html>/<head> wrapper')
    args = parser.parse_args()
    try:
        raw = Path(args.panel).read_bytes()
        data = build(json.loads(raw), [r for path in args.records for r in read_jsonl(path)])
        data['panel_sha256'] = hashlib.sha256(raw).hexdigest()
        if args.sensitivity:
            tier = tiers(json.loads(Path(args.sensitivity).read_text()))
            for model in data['models']:
                model['tier'] = tier[model['agent']]
        Path(args.output).write_text(render(data, not args.fragment))
        if args.data:
            Path(args.data).write_text(json.dumps(data, indent=1) + '\n')
        print(f'Wrote {args.output} (offline; no patch analysis)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
