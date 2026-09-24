"""Offline 70/30 task-normalized scoring of existing full-file measurements."""
import argparse
import hashlib
import json
import statistics
from pathlib import Path

from .benchmark import read_jsonl

VERSION = 'parsimony-70-30-v0.3'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def metrics(m):
    require(m and m.get('mode') == 'full_file', 'full-file metrics required')
    for key in ('tokens_added', 'tokens_deleted', 'churn'):
        require(type(m[key]) is int and m[key] >= 0, f'invalid {key}')
    require(type(m['net_tokens']) is int, 'integer net delta required')
    require(m['net_tokens'] == m['tokens_added'] - m['tokens_deleted'], 'net mismatch')
    require(m['churn'] == m['tokens_added'] + m['tokens_deleted'], 'churn mismatch')
    return m


def out_of_scope(m):
    """Every touched file was excluded: the fix is unmeasured, not a zero footprint."""
    return bool(m.get('touched_files')) and len(m.get('excluded_files', [])) == len(m['touched_files'])


def unique(records):
    seen = set()
    for r in records:
        key = (r['agent'], r['task_id'])
        require(key not in seen, f'duplicate agent/task: {key}')
        require(type(r['resolved']) is bool, 'resolved must be boolean')
        seen.add(key)


def freeze(records, name):
    unique(records)
    require(bool(records), 'empty reference records')
    versions = {(r['analyzer_version'], r['python_version']) for r in records}
    require(len(versions) == 1, 'mixed analyzer/Python versions')
    tasks = {r['task_id']: [] for r in records}
    for r in records:
        if not r['resolved'] or r['analysis_status'] != 'ok':
            continue
        if out_of_scope(metrics(r['metrics'])):
            continue  # an unmeasured patch cannot calibrate footprint percentiles
        tasks[r['task_id']].append({key: r[key] for key in ('agent', 'metrics', 'provenance')})
    for task, refs in tasks.items():
        require(bool(refs), f'no successful reference patch for {task}; select the cohort explicitly')
        bases = {(r['provenance']['repo'], r['provenance']['base_commit']) for r in refs}
        require(len(bases) == 1, f'mixed base repositories/commits: {task}')
    analyzer, python = next(iter(versions))
    return dict(score_version=VERSION, name=name, scope='fixed-cohort-sample',
                analyzer_version=analyzer, python_version=python,
                net_weight=0.7, churn_weight=0.3, failure_cap=25,
                tasks={task: sorted(refs, key=lambda r: r['agent']) for task, refs in sorted(tasks.items())})


def percentile(value, references):
    return sum((value < ref) + 0.5 * (value == ref) for ref in references) / len(references)


def task_score(record, refs):
    """Return a point or conservative bounds; missing data never means zero."""
    if record is None:
        return dict(status='unknown', score=None, lower=-25, upper=100)
    resolved = record['resolved']
    categories = set(record.get('published_result_categories', []))
    no_attempt = bool(categories & {'no_generation', 'no_submission'})
    failed = bool(categories & {'unresolved', 'failed', 'not_resolved'})
    if not resolved and no_attempt:
        # Do not grant a zero penalty to a nonempty attempted patch mislabeled no_generation.
        empty_hash = hashlib.sha256(b'').hexdigest()
        patch_hash = record.get('provenance', {}).get('patch_sha256')
        require(patch_hash in (None, empty_hash), 'no-attempt record contains a nonempty patch')
        require(record.get('metrics') is None, 'no-attempt record unexpectedly carries metrics')
        return dict(status='no_attempt', score=0, lower=0, upper=0)
    if not resolved and (not failed or 'no_logs' in categories):
        return dict(status='unknown', score=None, lower=-25, upper=100)
    if record['analysis_status'] != 'ok' or record.get('metrics') is None:
        return dict(status='missing_metrics', score=None,
                    lower=1 if resolved else -25, upper=100 if resolved else 0)
    m = metrics(record['metrics'])
    if out_of_scope(m):
        return dict(status='out_of_scope', score=None,
                    lower=1 if resolved else -25, upper=100 if resolved else 0)
    expected = refs[0]['provenance']
    actual = record['provenance']
    require((actual.get('repo'), actual.get('base_commit')) == (expected['repo'], expected['base_commit']),
            'candidate base repository/commit differs from frozen reference')
    if resolved:
        net = percentile(m['net_tokens'], [r['metrics']['net_tokens'] for r in refs])
        churn = percentile(m['churn'], [r['metrics']['churn'] for r in refs])
        score = 1 + 99 * (0.7 * net + 0.3 * churn)
        details = dict(net_percentile=net, churn_percentile=churn)
    else:
        scale = max(1, statistics.median(r['metrics']['churn'] for r in refs))
        growth = max(m['net_tokens'], 0)
        burden = 0.7 * growth / (scale + growth) + 0.3 * m['churn'] / (scale + m['churn'])
        score = -25 * burden
        details = dict(failure_scale=scale, failure_burden=burden)
    return dict(status='resolved' if resolved else 'failed', score=score, lower=score, upper=score, **details)


def score_records(panel, records):
    require(panel['score_version'] == VERSION, 'unsupported score version')
    require((panel['net_weight'], panel['churn_weight'], panel['failure_cap']) == (0.7, 0.3, 25),
            'weights differ from score version')
    require(bool(panel['tasks']), 'empty task set')
    for refs in panel['tasks'].values():
        require(bool(refs), 'empty reference panel for task')
        require(len({r['agent'] for r in refs}) == len(refs), 'duplicate reference agent')
        for ref in refs:
            metrics(ref['metrics'])
    unique(records)
    groups = {}
    for r in records:
        require((r['analyzer_version'], r['python_version']) ==
                (panel['analyzer_version'], panel['python_version']), 'incompatible analyzer/Python version')
        groups.setdefault(r['agent'], {})[r['task_id']] = r
    results = []
    for agent, group in sorted(groups.items()):
        tasks = {t: task_score(group.get(t), refs) for t, refs in panel['tasks'].items()}
        n = len(tasks)
        known = [v['score'] for v in tasks.values() if v['score'] is not None]
        complete = len(known) == n
        rates = {r['resolve_rate'] for r in group.values()}
        require(len(rates) == 1, 'inconsistent published resolve rate')
        results.append(dict(agent=agent, score_version=VERSION, panel=panel['name'],
                            score=statistics.mean(known) if complete else None,
                            lower=sum(t['lower'] for t in tasks.values()) / n,
                            upper=sum(t['upper'] for t in tasks.values()) / n,
                            success_credit=sum(max(v, 0) for v in known) / n if complete else None,
                            failure_penalty=-sum(min(v, 0) for v in known) / n if complete else None,
                            task_count=n, scored_tasks=len(known), published_resolve_rate=next(iter(rates)),
                            tasks=tasks))
    return sorted(results, key=lambda r: (r['score'] is None, -(r['score'] or 0), r['agent']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('freeze', help='freeze a reference panel; refuses to overwrite')
    make.add_argument('records', nargs='+')
    make.add_argument('--name', required=True)
    make.add_argument('--output', required=True)
    run = commands.add_parser('score', help='score existing JSONL against an unchanged panel')
    run.add_argument('panel')
    run.add_argument('records', nargs='+')
    run.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        records = [r for path in args.records for r in read_jsonl(path)]
        if args.command == 'freeze':
            result = freeze(records, args.name)
            result['source_sha256'] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in args.records}
        else:
            raw = Path(args.panel).read_bytes()
            panel = json.loads(raw)
            result = dict(panel_sha256=hashlib.sha256(raw).hexdigest(), score_version=VERSION,
                          scope=panel['scope'], leaderboard=score_records(panel, records))
        with Path(args.output).open('x' if args.command == 'freeze' else 'w') as stream:
            stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
        print(f'Wrote {args.output} (offline; no patch analysis)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
