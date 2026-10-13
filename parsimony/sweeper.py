"""Import pinned SWEeper-Bench PHP patches and browser-agent verdicts.

Population membership comes only from maintainers' reference file lists. Raw
patches stay external; analysis fetches exact base-commit sources through Cache.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import platform
import re
from pathlib import Path

from .analysis import implementation, measure
from .artifacts import Cache
from .benchmark import ANALYZER_VERSION, FetchError, analyzer_identity, base_source, read_jsonl
from .languages import track

TASK_DATASET = 'zlab-princeton/SWEeper-Bench'
TASK_REVISION = '0a4c5e2ec653b11bc0d99497a49635d3a56d3fa9'
TASK_SHA256 = 'be3ef86ae63efbb139cf977a507f0c2da4ad0ef12da5cfb1fdf285ffb9560c31'
TRACE_DATASET = 'zlab-princeton/SWEeper-Bench-traces'
TRACE_REVISION = '15e41de53a1c7bec06898da56c99d88f368ba17f'
TRACE_URL = f'https://huggingface.co/datasets/{TRACE_DATASET}/resolve/{TRACE_REVISION}'
SHA = re.compile(r'^[0-9a-f]{40}$')
SAFE = re.compile(r'^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*$')


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def repository(value):
    repo = value.removeprefix('https://github.com/').rstrip('/')
    if (not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo)
            or any(part in ('.', '..') for part in repo.split('/'))):
        raise ValueError('repository must be GitHub URL or owner/name')
    return repo


def build_dataset(tasks_path, ref_files, *, expected_sha256=TASK_SHA256):
    raw = Path(tasks_path).read_bytes()
    digest = sha256(raw)
    if digest != expected_sha256:
        raise ValueError('task dataset SHA256 mismatch')
    rows, seen = [], set()
    for task in read_jsonl(tasks_path):
        task_id = task['case_id']
        if not SAFE.fullmatch(task_id) or task_id in seen:
            raise ValueError('missing, unsafe or duplicate case_id')
        seen.add(task_id)
        if not SHA.fullmatch(task['base_commit']) or not SHA.fullmatch(task['reference_commit']):
            raise ValueError(f'{task_id}: commits must be full SHAs')
        ref_raw = (Path(ref_files) / f'{task_id}.json').read_bytes()
        files = json.loads(ref_raw)['files']
        # File membership, including additions/removals/renames, is a reference
        # fact. Model output and evaluation never enter this selection.
        if not any(implementation(file['filename'], 'php') for file in files):
            continue
        repo = repository(task['repo'])  # after the filter: one non-PHP task is hosted on Codeberg
        pr = task.get('pr')
        if pr is not None and (type(pr) is not int or pr <= 0):
            raise ValueError(f'{task_id}: positive PR number required')
        task_url = (f'https://github.com/{repo}/pull/{pr}' if pr is not None else
                    f'https://github.com/{repo}/commit/{task["reference_commit"]}')
        rows.append(dict(instance_id=task_id, repo=repo, base_commit=task['base_commit'], language='php',
                         task_url=task_url,
                         provenance=dict(dataset=TASK_DATASET, dataset_revision=TASK_REVISION,
                                         dataset_file_url=f'https://huggingface.co/datasets/{TASK_DATASET}/resolve/{TASK_REVISION}/data/test.jsonl',
                                         dataset_file_sha256=digest, reference_commit=task['reference_commit'],
                                         reference_files_sha256=sha256(ref_raw),
                                         reference_files_url=f'https://api.github.com/repos/{repo}/compare/{task["base_commit"]}...{task["reference_commit"]}')))
    if not rows:
        raise ValueError('empty PHP population')
    return sorted(rows, key=lambda row: row['instance_id'])


def read_runs(path):
    raw = Path(path).read_bytes()
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    required = {'run_id', 'task_id', 'repo', 'base_commit', 'model', 'harness', 'effort',
                'type', 'overall', 'patch_sha256', 'hf_url'}
    if (not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames))
            or not required <= set(reader.fieldnames)):
        raise ValueError('invalid runs.csv columns')
    return [row for row in reader if row['type'] == 'main'], sha256(raw)


def agent_id(model, harness):
    if not SAFE.fullmatch(model) or not SAFE.fullmatch(harness):
        raise ValueError('unsafe model/harness identifier')
    return f'sweeper-{model}-{harness}'


def analyze_runs(runs_path, dataset_path, patches, cache, *, model, harness):
    dataset = read_jsonl(dataset_path)
    metadata = {row['instance_id']: row for row in dataset}
    if not dataset or len(metadata) != len(dataset):
        raise ValueError('population must contain unique tasks')
    for task_id, meta in metadata.items():
        if (not SAFE.fullmatch(task_id) or meta.get('language') != 'php'
                or repository(meta['repo']) != meta['repo'] or not SHA.fullmatch(meta['base_commit'])):
            raise ValueError('population must contain PHP tasks with exact base metadata')
    rows, runs_digest = read_runs(runs_path)
    selected = [row for row in rows if (row['model'], row['harness']) == (model, harness)]
    if not selected:
        raise ValueError('no main runs for model/harness')
    if len({row['effort'] for row in selected}) != 1:
        raise ValueError('model/harness has multiple efforts; never pool configurations')
    by_task, run_ids = {}, set()
    for row in selected:
        task_id = row['task_id']
        if task_id in by_task or row['run_id'] in run_ids or not SAFE.fullmatch(row['run_id']):
            raise ValueError('duplicate main attempt or unsafe run_id')
        by_task[task_id] = row
        run_ids.add(row['run_id'])
        if row['overall'] not in ('pass', 'fail', 'uncertain', 'infrastructure_failed', '', 'missing'):
            raise ValueError(f'{task_id}: unsupported overall verdict')
        if task_id in metadata:
            meta = metadata[task_id]
            if (repository(row['repo']), row['base_commit']) != (meta['repo'], meta['base_commit']):
                raise ValueError(f'{task_id}: run base metadata differs from population')
    # Validate all available bytes before measuring or writing any records.
    patch_bytes = {}
    for task_id in metadata:
        row = by_task.get(task_id)
        if row is None:
            continue
        path = Path(patches) / f'{row["run_id"]}.patch'
        if not path.exists():
            continue
        raw = path.read_bytes()
        if sha256(raw) != row['patch_sha256']:
            raise ValueError(f'{task_id}: patch SHA256 mismatch')
        patch_bytes[task_id] = raw
    resolved_count = sum(by_task.get(task_id, {}).get('overall') == 'pass' for task_id in metadata)
    commit, source_digest = analyzer_identity()
    measurement_track = track('php')
    records = []
    for task_id, meta in sorted(metadata.items()):
        row = by_task.get(task_id, {})
        overall = row.get('overall') or 'missing'
        outcome = {'pass': 'resolved', 'fail': 'failed'}.get(overall, 'unknown')
        raw = patch_bytes.get(task_id)
        patch_url = f'{TRACE_URL}/{row["run_id"]}/prediction/patch' if row else None
        record = dict(schema_version=2, analyzer_version=ANALYZER_VERSION,
                      python_version=platform.python_version(), analyzer_commit=commit,
                      analyzer_source_sha256=source_digest, measurement_track=measurement_track,
                      agent=agent_id(model, harness), task_id=task_id, resolved=outcome == 'resolved',
                      evaluation_result=outcome, published_outcome=overall,
                      published_result_categories=[outcome] if outcome != 'unknown' else [],
                      submitted=bool(row), published_resolved_count=resolved_count,
                      benchmark_tasks=len(metadata), resolve_rate=resolved_count / len(metadata),
                      provenance={**meta.get('provenance', {}), 'instance_id': task_id,
                                  'repo': meta['repo'], 'base_commit': meta['base_commit'],
                                  'task_url': meta.get('task_url'), 'trace_dataset': TRACE_DATASET,
                                  'trace_revision': TRACE_REVISION,
                                  'result_url': TRACE_URL + '/runs.csv', 'result_sha256': runs_digest,
                                  'run_id': row.get('run_id'), 'hf_url': row.get('hf_url'),
                                  'model': model, 'harness': harness, 'effort': selected[0]['effort'],
                                  'source_run': row, 'patch_url': patch_url, 'patch_location': patch_url,
                                  'patch_sha256': row.get('patch_sha256') or None,
                                  'patch_verified': raw is not None},
                      metrics=None, human_metrics=None, model_human_ratio=None,
                      analysis_status='missing_patch')
        if raw is not None:
            try:
                patch = raw.decode('utf-8-sig')
            except UnicodeDecodeError as exc:  # e.g. a Latin-1 source file inside the diff
                record.update(analysis_status='error', analysis_error=f'UnicodeDecodeError: {exc}')
                records.append(record)
                continue
            record['provenance']['patch_final_newline_restored'] = bool(patch) and not patch.endswith('\n')
            if not patch.strip():
                record['analysis_status'] = 'empty_patch'
            else:
                try:
                    record['metrics'] = measure(patch, base_source(cache, meta), language='php')
                    record['analysis_status'] = 'ok'
                except FetchError as exc:
                    record.update(analysis_status='fetch_error', analysis_error=f'FetchError: {exc}')
                except Exception as exc:
                    record.update(analysis_status='error', analysis_error=f'{type(exc).__name__}: {exc}')
        records.append(record)
    return records


def write_records(path, rows):
    Path(path).write_text(''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows))
    print(f'Wrote {len(rows)} records to {path}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', default='.parsimony-cache')
    commands = parser.add_subparsers(dest='command', required=True)
    dataset = commands.add_parser('dataset', help='select PHP tasks from reference fixes only')
    dataset.add_argument('tasks')
    dataset.add_argument('--ref-files', required=True)
    dataset.add_argument('--output', required=True)
    analyze = commands.add_parser('analyze', help='retain and measure the full PHP population')
    analyze.add_argument('runs')
    analyze.add_argument('--dataset', required=True)
    analyze.add_argument('--patches', required=True)
    analyze.add_argument('--model', required=True)
    analyze.add_argument('--harness', required=True)
    analyze.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'dataset':
            rows = build_dataset(args.tasks, args.ref_files)
        else:
            rows = analyze_runs(args.runs, args.dataset, args.patches, Cache(args.cache, timeout=90),
                                model=args.model, harness=args.harness)
        write_records(args.output, rows)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
