"""Dataset metadata, per-task records, and matched-task aggregation."""
from __future__ import annotations

import hashlib
import json
import statistics
import platform
import subprocess
from functools import lru_cache
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote

from .analysis import measure

ANALYZER_VERSION = '0.5.1-beta'
FAILED_CATEGORIES = {'unresolved', 'failed', 'not_resolved'}


# Human reference measurements, shared by every submission analyzed in this process.
human_cache = {}


class FetchError(Exception):
    """A retryable download failure, distinct from a patch that cannot be analyzed."""


@lru_cache(maxsize=None)
def analyzer_identity():
    """Commit (None when uncommitted/unavailable) and hash of the analyzer sources."""
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for path in sorted(root.glob('*.py')):
        digest.update(path.name.encode() + b'\0' + path.read_bytes() + b'\0')
    commit = None
    try:
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', str(root)], cwd=root,
                               capture_output=True, text=True, check=True).stdout.strip()
        if not dirty:
            commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True,
                                    text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return commit, digest.hexdigest()


def evaluation_result(resolved, categories):
    if resolved:
        return 'resolved'
    for category in ('no_generation', 'no_submission', 'no_logs'):
        if category in categories:
            return category
    return 'failed' if categories & FAILED_CATEGORIES else 'unknown'


def fetch_dataset(cache):
    rows = []
    for offset in range(0, 500, 100):
        url = ('https://datasets-server.huggingface.co/rows?dataset=princeton-nlp%2F'
               f'SWE-bench_Verified&config=default&split=test&offset={offset}&length=100')
        data = json.loads(cache.get(url))
        for row in data['rows']:
            if row.get('truncated_cells'):
                raise ValueError('dataset server truncated a cell; supply full metadata JSONL')
            rows.append(row['row'])
    if len(rows) != 500 or len({r['instance_id'] for r in rows}) != 500:
        raise ValueError('expected 500 unique Verified tasks')
    return rows


def base_source(cache, meta):
    """Return get_source(path) reading exact base-commit files from GitHub."""
    def get_source(path):
        url = f"https://raw.githubusercontent.com/{meta['repo']}/{meta['base_commit']}/{quote(path, safe='/')}"
        try:
            return cache.get(url).decode('utf-8-sig')
        except HTTPError as exc:
            if exc.code == 404:
                raise ValueError(f'{path} does not exist at the base commit') from exc
            raise FetchError(f'{url}: HTTP {exc.code}') from exc
        except OSError as exc:  # URLError, timeouts, connection resets
            raise FetchError(f'{url}: {exc}') from exc
    return get_source


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def analyze_submission(submission, cache, dataset=None, limit=None, patch_only=False, task_ids=None,
                       include_failed=False):
    metadata = {row['instance_id']: row for row in (dataset or [])}
    tasks = sorted(set(metadata) or (set(submission['predictions']) | submission['resolved'] |
                                    (submission['evaluated'] or set())))
    # The public Verified benchmark has a fixed 500-task denominator, even when
    # a submission omits predictions or evaluation logs.
    denominator = len(metadata) if metadata else 500
    if metadata and not submission['resolved'] <= metadata.keys():
        raise ValueError('resolved tasks outside supplied dataset')
    selected = None if task_ids is None else set(task_ids)
    if selected is not None and not selected <= set(tasks):
        raise ValueError('selected tasks outside benchmark population')
    analyzed = 0
    commit, source_sha256 = analyzer_identity()
    for task in tasks:
        patch = submission['predictions'].get(task)
        resolved = task in submission['resolved']
        meta = metadata.get(task)
        categories = [key for key, value in submission.get('result_details', {}).items()
                      if isinstance(value, list) and task in value]
        record = dict(schema_version=2, analyzer_version=ANALYZER_VERSION, python_version=platform.python_version(),
                      analyzer_commit=commit, analyzer_source_sha256=source_sha256,
                      agent=submission['agent'], task_id=task, resolved=resolved,
                      published_result_categories=categories,
                      evaluation_result=evaluation_result(resolved, set(categories)),
                      published_resolved_count=len(submission['resolved']),
                      benchmark_tasks=denominator, resolve_rate=len(submission['resolved']) / denominator,
                      provenance={**submission['provenance'], 'instance_id': task,
                                  'patch_location': submission.get('prediction_locations', {}).get(
                                      task, submission['provenance']['prediction_url'] + '#instance_id=' + task),
                                  'patch_sha256': hashlib.sha256(patch.encode()).hexdigest() if patch is not None else None},
                      metrics=None, human_metrics=None, model_human_ratio=None,
                      analysis_status='not_resolved')
        if meta:
            record['provenance'].update(repo=meta['repo'], base_commit=meta['base_commit'],
                                        reference_patch_sha256=hashlib.sha256(meta.get('patch', '').encode()).hexdigest())
        categories = set(record['published_result_categories'])
        analyzable_failure = include_failed and bool(categories & FAILED_CATEGORIES) \
            and 'no_logs' not in categories
        if not resolved and not analyzable_failure:
            yield record
            continue
        if selected is not None and task not in selected:
            record['analysis_status'] = 'not_selected'
            yield record
            continue
        if limit is not None and analyzed >= limit:
            record['analysis_status'] = 'limit'
            yield record
            continue
        analyzed += 1
        if patch is None:
            record['analysis_status'] = 'missing_patch'
            yield record
            continue
        if not patch_only and not meta:
            record['analysis_status'] = 'missing_base_metadata'
            yield record
            continue
        source = None if patch_only else base_source(cache, meta)
        try:
            record['metrics'] = measure(patch, source)
            record['analysis_status'] = 'ok'
            if meta and meta.get('patch'):
                # The human patch is identical for every agent: measure it once per task.
                key = (meta['repo'], meta['base_commit'], meta['patch'], patch_only)
                if key not in human_cache:
                    try:
                        human_cache[key] = (measure(meta['patch'], source), None)
                    except FetchError:
                        raise
                    except Exception as exc:
                        human_cache[key] = (None, f'{type(exc).__name__}: {exc}')
                human, error = human_cache[key]
                if human is not None:
                    record['human_metrics'] = human
                    if human['churn'] and record['metrics']['churn'] is not None:
                        record['model_human_ratio'] = record['metrics']['churn'] / human['churn']
                else:
                    record['human_error'] = error
        except FetchError as exc:
            # Retryable: --resume re-attempts these instead of freezing a network blip.
            record.update(metrics=None, human_metrics=None, model_human_ratio=None,
                          analysis_status='fetch_error', analysis_error=f'FetchError: {exc}')
        except Exception as exc:
            record['analysis_status'] = 'error'
            record['analysis_error'] = f'{type(exc).__name__}: {exc}'
        yield record


def leaderboard(records, shared=False, agents=None, mode='full_file'):
    selected = set(agents or [r['agent'] for r in records])
    by_agent = {a: {} for a in sorted(selected)}
    for r in records:
        if r['agent'] not in selected:
            continue
        group = by_agent[r['agent']]
        if r['task_id'] in group:
            raise ValueError(f"duplicate agent/task: {r['agent']} / {r['task_id']}")
        group[r['task_id']] = r
    eligible = {a: {t for t, r in group.items() if r['resolved'] and r['analysis_status'] == 'ok'
                    and r['metrics']['mode'] == mode} for a, group in by_agent.items()}
    common = set.intersection(*eligible.values()) if eligible else set()
    rows = []
    for agent, group in by_agent.items():
        ids = common if shared else eligible[agent]
        subset = [group[t] for t in sorted(ids)]
        def median(field):
            values = [r['metrics'][field] for r in subset if r['metrics'].get(field) is not None]
            return statistics.median(values) if values else None
        ratios = [r['model_human_ratio'] for r in subset if r.get('model_human_ratio') is not None]
        rates = {r['resolve_rate'] for r in group.values()}
        if len(rates) > 1:
            raise ValueError(f'inconsistent resolve rates for {agent}')
        rows.append(dict(agent=agent, resolve_rate=next(iter(rates), None),
                         successful_tasks_analyzed=len(subset), comparison='shared' if shared else 'individual',
                         mode=mode, task_ids=sorted(ids),
                         median_net_units=median('net_units'), median_churn=median('churn'),
                         median_net_tokens=median('net_tokens'), median_token_churn=median('token_churn'),
                         median_model_human_ratio=statistics.median(ratios) if ratios else None,
                         human_ratio_tasks=len(ratios), median_files_changed=median('files_changed'),
                         median_ast_delta=median('ast_delta'), median_complexity_delta=median('complexity_delta'),
                         structure_tasks=sum(r['metrics'].get('ast_delta') is not None for r in subset)))
    return sorted(rows, key=lambda r: (r['median_net_units'] is None, r['median_net_units'] or 0, r['agent']))
