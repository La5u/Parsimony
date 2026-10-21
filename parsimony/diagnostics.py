"""Offline diagnostics for the website's same-task net ratio (not the archived score).

No patch fetching, analysis, outcome inference, or changes to published rankings.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import statistics

from .benchmark import read_jsonl
from .scoring import measured, out_of_scope, score_records
from .site import label, same_task_pairs, solved_by_task, typical_by_task

VERSION = 'same-task-net-diagnostics-v1'


def ratio(pairs):
    denominator = sum(b for _, b in pairs)
    return sum(a for a, _ in pairs) / denominator if pairs and denominator > 0 else None


def evaluate(per_model):
    """Use website eligibility and displayed (three-decimal) ratios for competition ranks."""
    typical = typical_by_task(per_model)
    pairs = {a: {t: p[0] for t, v in own.items()
                 if (p := same_task_pairs({t: v}, typical, 0))}
             for a, own in per_model.items()}
    values = {a: ratio(list(p.values())) for a, p in pairs.items()}
    displayed = {a: round(v, 3) for a, v in values.items() if v is not None}
    ranks = {a: 1 + sum(x < displayed[a] for x in displayed.values()) if a in displayed else None
             for a in per_model}
    return values, ranks, pairs


def coverage(records, own):
    successes = [r for r in records if r['resolved']]
    eligible = [r for r in successes if measured(r) and r['metrics'].get('mode') == 'full_file'
                and not out_of_scope(r['metrics'])]
    reasons = Counter()
    for r in successes:
        m = r.get('metrics') or {}
        if not measured(r):
            status = r.get('analysis_status', 'missing_metrics')
            reason = status if status != 'ok' else ('lexical_files' if m.get('lexical_files') else 'missing_units')
            reasons[reason] += 1
        elif m.get('mode') != 'full_file':
            reasons['not_full_file'] += 1
        elif out_of_scope(m):
            reasons['out_of_scope'] += 1
    reported = {r['published_resolved_count'] for r in records
                if r.get('published_resolved_count') is not None}
    if len(reported) > 1:
        raise ValueError('conflicting published resolved counts')
    published = next(iter(reported), len(successes))
    if published < len(successes):
        raise ValueError('published resolved count smaller than resolved records')
    return dict(resolved_records=len(successes), published_resolved_attempts=published,
                eligible_solved_attempts=len(eligible), eligible_solved_base_tasks=len(own),
                published_successes_without_resolved_record=published - len(successes),
                excluded_success_reasons=dict(sorted(reasons.items())))


def perturbations(per_model, baseline, cases, *, drop_peer=False):
    """Summarize rank/ratio changes; retain top three influences, not a second leaderboard."""
    results = {a: [] for a in per_model}
    _, baseline_ranks, _ = evaluate(per_model)
    for name, removed in cases:
        if drop_peer:
            subset = {a: ts for a, ts in per_model.items() if a != name}
            # Compare against the original ratios with the removed candidate absent:
            # merely removing a competitor must not count as a baseline shift.
            reference_values = {a: baseline[a] for a in subset}
            displayed = {a: round(v, 3) for a, v in reference_values.items() if v is not None}
            reference_ranks = {a: 1 + sum(x < displayed[a] for x in displayed.values())
                               if a in displayed else None for a in subset}
        else:
            subset = {a: {t: v for t, v in ts.items() if t not in removed}
                      for a, ts in per_model.items()}
            reference_ranks = baseline_ranks
        values, ranks, pairs = evaluate(subset)
        for a in subset:
            before, after = baseline[a], values[a]
            results[a].append(dict(removed=name, ratio=after, rank=ranks[a],
                                   comparison_tasks=len(pairs[a]),
                                   ratio_change=after - before if before is not None and after is not None else None,
                                   rank_change=ranks[a] - reference_ranks[a]
                                   if ranks[a] is not None and reference_ranks[a] is not None else None))
    out = {}
    for a, rows in results.items():
        ranks = [r['rank'] for r in rows if r['rank'] is not None]
        values = [r['ratio'] for r in rows if r['ratio'] is not None]
        changes = [r['ratio_change'] for r in rows if r['ratio_change'] is not None]
        influences = sorted(rows, key=lambda r: (r['ratio'] is None,
                            abs(r['rank_change'] or 0), abs(r['ratio_change'] or 0)), reverse=True)[:3]
        out[a] = dict(scenarios=len(rows), unavailable_scenarios=sum(r['ratio'] is None for r in rows),
                      rank_range=[min(ranks), max(ranks)] if ranks else None,
                      ratio_range=[min(values), max(values)] if values else None,
                      max_abs_ratio_change=max(map(abs, changes), default=None), top_influences=influences)
    return out


def diagnose(panel, records):
    records = list(records)
    score_records(panel, records)  # existing duplicate, identity, track and panel validation
    groups, repos = {}, {}
    for r in records:
        groups.setdefault(r['agent'], []).append(r)
        task = r['task_id'].split('#', 1)[0]
        repo = r.get('provenance', {}).get('repo')
        if repo:
            if repos.get(task) is not None and repos[task] != repo:
                raise ValueError(f'conflicting repositories for {task}')
            repos[task] = repo
        else:
            repos.setdefault(task, None)
    repos = {task: repo or '(unknown repository)' for task, repo in repos.items()}
    per_model = {a: solved_by_task(rs) for a, rs in sorted(groups.items())}
    values, ranks, pairs = evaluate(per_model)
    tasks = sorted({t for ts in per_model.values() for t in ts})
    repositories = sorted({repos[t] for t in tasks})
    task_drops = perturbations(per_model, values, [(t, {t}) for t in tasks])
    repo_drops = perturbations(per_model, values,
                               [(repo, {t for t in tasks if repos[t] == repo}) for repo in repositories])
    peer_drops = perturbations(per_model, values, [(a, set()) for a in per_model], drop_peer=True)
    models = {}
    for a, own in per_model.items():
        p = pairs[a]
        denominator = sum(y for _, y in p.values())
        biggest = max(p, key=lambda t: abs(p[t][1])) if p else None
        models[a] = dict(name=label(a), ratio=values[a], rank=ranks[a],
                         coverage=coverage(groups[a], own), comparison_tasks=len(p),
                         reported_harnesses=sorted({r.get('provenance', {}).get('source_agent')
                                                    for r in groups[a] if r.get('provenance', {}).get('source_agent')}),
                         retry_policy='Not inferred; consult the pinned source run report.',
                         comparison_denominator=denominator,
                         largest_abs_comparison_task=biggest,
                         largest_abs_comparison_share=abs(p[biggest][1]) / denominator
                         if biggest is not None and denominator > 0 else None,
                         nonpositive_comparison_tasks=sum(y <= 0 for _, y in p.values()),
                         leave_one_task_out=task_drops[a], leave_one_repository_out=repo_drops[a],
                         leave_one_peer_out=peer_drops[a])
    matched = []
    for a, b in itertools.combinations(per_model, 2):
        common = sorted(per_model[a].keys() & per_model[b].keys())
        av = [per_model[a][t][0] for t in common]
        bv = [per_model[b][t][0] for t in common]
        matched.append(dict(a=a, b=b, shared_solved_measured_tasks=len(common),
                            a_net_mean=statistics.fmean(av) if av else None,
                            b_net_mean=statistics.fmean(bv) if bv else None,
                            mean_difference_a_minus_b=statistics.fmean(x - y for x, y in zip(av, bv))
                            if common else None,
                            ratio_a_over_b=sum(av) / sum(bv) if bv and sum(bv) > 0 else None))
    return dict(diagnostic_version=VERSION, ranking_metric='same-task-net-ratio-v1', panel=panel['name'],
                limitations=[
                    'Descriptive sensitivity, not confidence intervals or a replacement ranking.',
                    'Successful measured repairs only; missing footprints are not imputed.',
                    'Each task/repository deletion preserves peer eligibility rules; peer deletion recomputes them.',
                    'Peer rank changes exclude the mechanical effect of removing a competing candidate.',
                    'Pairwise comparisons use all shared solved measured base tasks, without the three-peer gate.',
                    'Repository omission tests influence; it is not a repository-cluster bootstrap.',
                    'Harness, retry policy and upstream outcome validity are not inferred from model labels.',
                    'Combined-language ranking is not evaluated; run this separately for each language board.'],
                base_tasks=len(tasks), repositories=len(repositories), models=models, pairwise=matched)


def markdown(report):
    lines = ['# Same-task net ratio diagnostics', '',
             f"Panel: `{report['panel']}` · `{report['diagnostic_version']}`", '',
             'These diagnostics do not change the website ranking. Lower footprint is not better coding quality.', '',
             '## Coverage and influence', '',
             '| Configuration | Ratio | Shared tasks | Measured / published successes | Largest task share | Task-drop rank range | Repo-drop rank range |',
             '|---|---:|---:|---:|---:|---:|---:|']
    def fmt(v):
        return '—' if v is None else f'{v:.3f}'
    def span(v):
        return '—' if v is None else f'{v[0]}–{v[1]}'
    for a, m in sorted(report['models'].items(), key=lambda item: (item[1]['rank'] is None, item[1]['rank'] or 0, item[0])):
        c = m['coverage']
        name = m['name'].replace('|', '\\|').replace('\n', ' ')
        lines.append(f"| {name} | {fmt(m['ratio'])} | {m['comparison_tasks']} | "
                     f"{c['eligible_solved_attempts']}/{c['published_resolved_attempts']} | "
                     f"{fmt(m['largest_abs_comparison_share'])} | "
                     f"{span(m['leave_one_task_out']['rank_range'])} | {span(m['leave_one_repository_out']['rank_range'])} |")
    lines += ['', 'Largest task share is the largest absolute per-task peer footprint divided by the total peer footprint; cancellation can make it exceed 1. Unavailable perturbations are counted separately in JSON, not included in rank ranges.', '',
              '## Interpretation', ''] + ['- ' + text for text in report['limitations']]
    lines += ['', 'JSON includes missing-success reasons, top task/repository/peer influences, unavailable scenarios, and pairwise matched-task means. Rank ranges are sensitivity extrema, not 95% intervals.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('panel')
    parser.add_argument('records', nargs='+')
    parser.add_argument('--output', required=True, help='JSON report; Markdown is written alongside it')
    args = parser.parse_args()
    try:
        paths = [Path(args.panel), *(Path(p) for p in args.records)]
        report = diagnose(json.loads(paths[0].read_text()),
                          [r for path in paths[1:] for r in read_jsonl(path)])
        # Sorted so shell glob order (locale-dependent) cannot change the report bytes.
        report['inputs'] = [dict(file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
                            for path in [paths[0], *sorted(paths[1:], key=lambda p: p.name)]]
        output = Path(args.output)
        if output.suffix != '.json':
            raise ValueError('--output must end in .json')
        output.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
        output.with_suffix('.md').write_text(markdown(report))
        print(f'Wrote {output} and {output.with_suffix(".md")} (offline; no patch analysis)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
