"""Offline beta release manifest and fixed-population coverage audit.

This does not certify upstream correctness or patch authenticity. It makes missing
measurements and provenance visible before an experimental score is published.
"""
import argparse
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path

from .benchmark import read_jsonl
from .scoring import out_of_scope


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def freeze_dataset(path, name, analyzer_commit=None):
    rows = read_jsonl(path)
    ids = [r['instance_id'] for r in rows]
    if not rows or len(ids) != len(set(ids)) or any(not r.get('repo') or not r.get('base_commit') for r in rows):
        raise ValueError('dataset must have unique task IDs, repository and base commits')
    if not analyzer_commit:
        analyzer_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
        if subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip():
            raise ValueError('dirty checkout: specify an immutable analyzer commit after committing changes')
    if not re.fullmatch(r'[0-9a-fA-F]{40}', analyzer_commit):
        raise ValueError('analyzer commit must be a full 40-character Git SHA')
    return dict(format='parsimony-beta-population-v1', name=name, dataset_sha256=sha(path),
                analyzer_commit=analyzer_commit, python_version=platform.python_version(),
                task_count=len(ids), tasks={r['instance_id']: {'repo': r['repo'], 'base_commit': r['base_commit']}
                                            for r in sorted(rows, key=lambda r: r['instance_id'])})


def audit(panel, records, dataset_path=None):
    if panel.get('format') != 'parsimony-beta-population-v1':
        raise ValueError('unsupported population manifest')
    if dataset_path and sha(dataset_path) != panel['dataset_sha256']:
        raise ValueError('dataset checksum differs from frozen population')
    ids = panel['tasks']
    if len(ids) != panel['task_count']:
        raise ValueError('manifest task count mismatch')
    groups = {}
    for r in records:
        agent, task = r['agent'], r['task_id']
        if task not in ids:
            raise ValueError(f'task outside frozen population: {task}')
        group = groups.setdefault(agent, {})
        if task in group:
            raise ValueError(f'duplicate agent/task: {agent} / {task}')
        group[task] = r
        if r['python_version'] != panel['python_version']:
            raise ValueError(f'incompatible Python version: {agent} / {task}')
        # Records from 0.4.0 carry the analyzer commit; older ones are counted as unverified below.
        if r.get('analyzer_commit', panel['analyzer_commit']) != panel['analyzer_commit']:
            raise ValueError(f'analyzer commit differs from frozen population: {agent} / {task}')
        provenance = r.get('provenance', {})
        if provenance.get('repo') != ids[task]['repo'] or provenance.get('base_commit') != ids[task]['base_commit']:
            raise ValueError(f'base commit mismatch: {agent} / {task}')
    agents = []
    for agent, group in sorted(groups.items()):
        versions = {r['analyzer_version'] for r in group.values()}
        if len(versions) != 1:
            raise ValueError(f'mixed analyzer versions: {agent}')
        rates = {(r['published_resolved_count'], r['benchmark_tasks'], r['resolve_rate']) for r in group.values()}
        if len(rates) != 1:
            raise ValueError(f'inconsistent published totals: {agent}')
        resolved_count, denominator, rate = next(iter(rates))
        if denominator != len(ids) or resolved_count / denominator != rate:
            raise ValueError(f'invalid published totals: {agent}')
        resolved = [r for r in group.values() if r['resolved']]
        if len(group) == len(ids) and len(resolved) != resolved_count:
            raise ValueError(f'published and recorded resolved totals disagree: {agent}')
        ok = [r for r in group.values() if r['analysis_status'] == 'ok' and (r.get('metrics') or {}).get('mode') == 'full_file']
        successful = [r for r in ok if r['resolved']]
        failed = [r for r in ok if not r['resolved']]
        excluded = sorted({path for r in ok for path in r['metrics'].get('excluded_files', [])})
        zero_normalized_edits = sum(bool(r['metrics'].get('touched_files')) and r['metrics']['churn'] == 0
                                    for r in ok if 'churn' in r['metrics'])
        def value_only(m):
            if 'structural_churn' in m:  # >= 0.4.0: identifier/literal edits count as churn
                return bool(m['churn']) and m['structural_churn'] == 0
            return m.get('churn') == 0 and m.get('value_sensitive_churn', 0) > 0
        hidden_value_edits = sum(value_only(r['metrics']) for r in ok)
        statuses = {status: sum(r['analysis_status'] == status for r in group.values())
                    for status in sorted({r['analysis_status'] for r in group.values()})}
        agents.append(dict(agent=agent, analyzer_version=next(iter(versions)),
                           published_resolve_rate=rate, records=len(group), missing_records=len(ids) - len(group),
                           resolved_records=len(resolved), successful_analyses=len(successful),
                           failed_analyses=len(failed), resolved_missing_analysis=len(resolved) - len(successful),
                           analysis_status_counts=statuses, excluded_files=excluded,
                           zero_normalized_edit_records=zero_normalized_edits,
                           value_only_edit_records=hidden_value_edits,
                           out_of_scope_successes=sum(out_of_scope(r['metrics']) for r in successful),
                           unmeasured_unit_records=sum(r['metrics'].get('churn', 0) is None for r in ok),
                           lexical_fallback_records=sum(bool(r['metrics'].get('lexical_files')) for r in ok),
                           approximate_alignment_records=sum(bool(r['metrics'].get('approximate_files')) for r in ok),
                           offset_hunk_records=sum(bool(r['metrics'].get('offset_hunks')) for r in ok),
                           unverified_analyzer_commit_records=sum('analyzer_commit' not in r
                                                                  for r in group.values())))
    return dict(status='beta-coverage-not-certification', population=panel['name'],
                population_sha256=hashlib.sha256(json.dumps(panel, sort_keys=True).encode()).hexdigest(),
                task_count=len(ids), agents=agents)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    freeze = commands.add_parser('freeze', help='freeze task population; refuses overwrite')
    freeze.add_argument('dataset')
    freeze.add_argument('--name', required=True)
    freeze.add_argument('--analyzer-commit', help='immutable analyzer commit (defaults to clean HEAD)')
    freeze.add_argument('--output', required=True)
    check = commands.add_parser('audit', help='report full-population coverage, not a ranking')
    check.add_argument('manifest')
    check.add_argument('records', nargs='+')
    check.add_argument('--dataset', help='verify original dataset bytes against manifest')
    check.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'freeze':
            result = freeze_dataset(args.dataset, args.name, args.analyzer_commit)
        else:
            panel = json.loads(Path(args.manifest).read_text())
            records = [r for path in args.records for r in read_jsonl(path)]
            result = audit(panel, records, args.dataset)
            result['manifest_sha256'] = sha(args.manifest)
            result['records_sha256'] = {p: sha(p) for p in args.records}
        with Path(args.output).open('x' if args.command == 'freeze' else 'w') as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write('\n')
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
