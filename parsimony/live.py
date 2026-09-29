"""Import existing SWE-bench Live runs without executing submitted code.

The importer is intentionally limited to a pinned submission-tree revision and an
explicit file/revision in the Hugging Face task dataset. It never infers task
metadata from task IDs and refuses mutable or unverifiable dataset revisions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote

from .artifacts import Cache

GITHUB = 'https://github.com/SWE-bench-Live/submission'
HF = 'https://huggingface.co'
SHA = re.compile(r'^[0-9a-f]{40}$')
CATEGORIES = ('success', 'failure', 'error', 'incomplete', 'empty_patch')
LANGUAGES = ('python', 'javascript', 'typescript', 'go')
# TS/JS is deliberately retained as a mixed-track label, not guessed/relabelled
# into either single-language track; it remains inventory-only for analysis.
LANGUAGE_ALIASES = {
    'python': 'python', 'go': 'go', 'javascript': 'javascript',
    'typescript': 'typescript',
    'js': 'javascript', 'ts': 'typescript',
    'ts/js': 'typescript-javascript', 'js/ts': 'typescript-javascript',
    'typescript/javascript': 'typescript-javascript', 'javascript/typescript': 'typescript-javascript',
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json(cache: Cache, url: str) -> tuple[dict, bytes]:
    raw = cache.get(url)
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError(f'expected JSON object at {url}')
    return value, raw


def fetch_hf_rows(cache: Cache, dataset: str, revision: str, file_path: str) -> tuple[list[dict], dict]:
    """Fetch JSON/JSONL/CSV from an exact HF commit; reject branch/tag aliases."""
    if not SHA.fullmatch(revision):
        raise ValueError('HF dataset revision must be a full 40-character commit SHA')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', dataset):
        raise ValueError('HF dataset id must be safe owner/name')
    if file_path.startswith('/') or '..' in Path(file_path).parts:
        raise ValueError('invalid HF dataset file path')
    api = f'{HF}/api/datasets/{quote(dataset, safe="/")}/revision/{revision}'
    metadata, metadata_bytes = _json(cache, api)
    resolved = metadata.get('sha')
    if resolved != revision:
        raise ValueError(f'HF revision verification failed: requested {revision}, resolved {resolved!r}')
    url = f'{HF}/datasets/{quote(dataset, safe="/")}/resolve/{revision}/{quote(file_path, safe="/")}'
    raw = cache.get(url)
    if file_path.endswith('.parquet'):
        try:
            import pyarrow.parquet as parquet
        except ImportError as exc:
            raise ValueError('reading Parquet requires the optional pyarrow dependency') from exc
        table = parquet.read_table(io.BytesIO(raw))
        rows = table.to_pylist()
    elif file_path.endswith('.jsonl') or file_path.endswith('.ndjson'):
        text = raw.decode('utf-8-sig')
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    elif file_path.endswith('.json'):
        text = raw.decode('utf-8-sig')
        data = json.loads(text)
        rows = data if isinstance(data, list) else data.get('rows', data.get('data'))
    elif file_path.endswith('.csv'):
        text = raw.decode('utf-8-sig')
        rows = list(csv.DictReader(io.StringIO(text)))
    else:
        raise ValueError('supported task file formats are JSON, JSONL/NDJSON, CSV and Parquet')
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError('HF task file must contain a list of task objects')
    return rows, dict(dataset=dataset, revision=revision, revision_url=api,
                      revision_sha256=sha256(metadata_bytes), dataset_file_url=url,
                      dataset_file_sha256=sha256(raw))


def _result_categories(result: dict) -> dict[str, set[str]]:
    ids = {}
    keys = {'success': 'success_ids', 'failure': 'failure_ids', 'error': 'error_ids',
            'incomplete': 'incomplete_ids', 'empty_patch': 'empty_patch_ids'}
    for category, key in keys.items():
        value = result.get(key)
        if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
            raise ValueError(f'result.json must contain string list {key}')
        if len(value) != len(set(value)):
            raise ValueError(f'{key} contains duplicate IDs')
        count = result.get(category)
        if isinstance(count, bool) or not isinstance(count, int) or count != len(value):
            raise ValueError(f'{category} count/IDs disagree')
        ids[category] = set(value)
    submitted = result.get('submitted_ids')
    if not isinstance(submitted, list) or any(not isinstance(x, str) for x in submitted):
        raise ValueError('result.json must contain submitted_ids')
    submitted_count = result.get('submitted')
    if (len(submitted) != len(set(submitted)) or isinstance(submitted_count, bool)
            or not isinstance(submitted_count, int) or len(submitted) != submitted_count):
        raise ValueError('submitted count/IDs disagree or contain duplicates')
    for category, members in ids.items():
        if not members <= set(submitted):
            raise ValueError(f'{category} contains IDs absent from submitted_ids')
    # Empty patch is an artifact fact; source may also classify its evaluation as failure.
    outcome_categories = [ids[k] for k in ('success', 'failure', 'error', 'incomplete')]
    for i, one in enumerate(outcome_categories):
        if any(one & other for other in outcome_categories[i + 1:]):
            raise ValueError('success/failure/error/incomplete outcome categories overlap')
    if not set.union(*outcome_categories) <= set(submitted):
        raise ValueError('outcome categories contain IDs absent from submitted_ids')
    covered = set.union(*outcome_categories, ids['empty_patch'])
    if set(submitted) != covered:
        raise ValueError('submitted IDs must have an outcome or be listed as empty_patch')
    return ids


def _language(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    return LANGUAGE_ALIASES.get(value.lower(), value)


def _dataset_specs(dataset_file: str | None, dataset_files) -> list[tuple[str | None, str]]:
    if dataset_files is None:
        if not dataset_file:
            raise ValueError('at least one dataset file is required')
        dataset_files = [dataset_file]
    if isinstance(dataset_files, dict):
        specs = [(language, path) for language, path in dataset_files.items()]
    else:
        specs = []
        for item in dataset_files:
            if isinstance(item, str):
                if '=' in item:
                    language, path = item.split('=', 1)
                    specs.append((language, path))
                else:
                    specs.append((None, item))
            elif isinstance(item, dict):
                specs.append((item.get('language'), item.get('file') or item.get('path')))
            elif isinstance(item, (tuple, list)) and len(item) == 2:
                specs.append((item[0], item[1]))
            else:
                raise ValueError('dataset_files entries must be LANGUAGE=PATH or file/language pairs')
    normalized = []
    for language, path in specs:
        language = _language(language)
        if language is None and isinstance(path, str) and not path:
            raise ValueError('dataset file path is required')
        if not isinstance(path, str) or not path:
            raise ValueError('dataset file path is required')
        normalized.append((language, path))
    if not normalized:
        raise ValueError('at least one dataset file is required')
    return normalized


def import_run(cache: Cache, *, submission_revision: str, config_path: str,
               dataset: str, dataset_revision: str, dataset_file: str | None = None,
               dataset_files=None, task_ids: list[str] | None = None) -> dict:
    """Inventory a run against explicitly mapped immutable dataset files."""
    if not SHA.fullmatch(submission_revision):
        raise ValueError('submission revision must be a full Git commit SHA')
    if config_path.startswith('/') or '..' in Path(config_path).parts:
        raise ValueError('invalid submission configuration path')
    base = f'https://raw.githubusercontent.com/SWE-bench-Live/submission/{submission_revision}/{config_path.strip("/")}'
    result_url = base + '/result.json'
    result, result_bytes = _json(cache, result_url)
    categories = _result_categories(result)
    specs = _dataset_specs(dataset_file, dataset_files)
    files, by_id = [], {}
    for explicit_language, file_path in specs:
        task_rows, provenance = fetch_hf_rows(cache, dataset, dataset_revision, file_path)
        files.append(dict(file=file_path, language=explicit_language,
                          revision_url=provenance['revision_url'],
                          revision_sha256=provenance['revision_sha256'],
                          dataset_file_url=provenance['dataset_file_url'],
                          dataset_file_sha256=provenance['dataset_file_sha256']))
        for row in task_rows:
            task_id = row.get('instance_id') or row.get('task_id')
            if not isinstance(task_id, str) or task_id in by_id:
                raise ValueError('HF task dataset has missing or duplicate task IDs across files')
            repo = row.get('repo') or row.get('repository')
            base_commit = row.get('base_commit') or row.get('base_commit_hash')
            if not isinstance(repo, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
                raise ValueError(f'{task_id}: repository must be safe owner/name')
            if not isinstance(base_commit, str) or not SHA.fullmatch(base_commit):
                raise ValueError(f'{task_id}: base_commit must be a full 40-character SHA')
            row_language = _language(row.get('language'))
            if explicit_language and row_language and explicit_language != row_language:
                raise ValueError(f'{task_id}: row language conflicts with explicit file language')
            lang = explicit_language or row_language or 'unknown'
            by_id[task_id] = dict(row, instance_id=task_id, repo=repo, base_commit=base_commit,
                                  language=lang, dataset_file=file_path)
    submitted = set(result['submitted_ids'])
    if not submitted <= set(by_id):
        raise ValueError(f'run IDs absent from dataset (count={len(submitted-set(by_id))})')
    selected_ids = set(task_ids or [])
    if selected_ids - submitted:
        raise ValueError(f'task selection contains IDs absent from submitted_ids: {sorted(selected_ids-submitted)}')
    records = []
    for task_id in result['submitted_ids']:
        meta = by_id[task_id]
        task_path = f'{base}/{quote(task_id, safe="")}/patch.diff'
        artifact_status = 'empty_patch' if task_id in categories['empty_patch'] else 'present'
        patch = None
        patch_digest = None
        if artifact_status == 'present' and selected_ids and task_id not in selected_ids:
            artifact_status = 'not_selected'
        if artifact_status == 'present':
            try:
                raw_patch = cache.get(task_path)
            except HTTPError as exc:
                if exc.code != 404:
                    raise
                exc.close()
                artifact_status = 'missing'
            else:
                patch = raw_patch.decode('utf-8-sig')
                patch_digest = sha256(raw_patch)
                if not patch.strip():
                    artifact_status = 'empty_patch'
                    patch = None
        outcome = next((category for category in ('success', 'failure', 'error', 'incomplete')
                        if task_id in categories[category]), 'unknown')
        record = dict(task_id=task_id, repo=meta['repo'], base_commit=meta['base_commit'],
                      language=meta['language'], published_outcome=outcome,
                      artifact_status=artifact_status, patch=patch,
                      provenance=dict(submission_revision=submission_revision,
                                      submission_url=f'{GITHUB}/tree/{submission_revision}/{config_path}',
                                      result_url=result_url, result_sha256=sha256(result_bytes),
                                      patch_url=task_path, patch_sha256=patch_digest,
                                      dataset_file=meta['dataset_file']))
        records.append(record)
    dataset_checksum = sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode())
    dataset_provenance = dict(dataset=dataset, revision=dataset_revision, files=files,
                              revision_url=files[0]['revision_url'],
                              revision_sha256=files[0]['revision_sha256'],
                              dataset_file_sha256=dataset_checksum,
                              dataset_checksum=dataset_checksum)
    return dict(schema_version=1, submission_revision=submission_revision, dataset=dataset_provenance,
                dataset_task_count=len(by_id), submitted_task_count=len(submitted),
                completeness_audit=dict(submitted_ids_within_dataset=True,
                                        dataset_only_count=len(set(by_id)-submitted)),
                historical_dataset_match='unverified',
                model=None, agent='swe-bench-live', config=config_path,
                result_url=result_url, result_sha256=sha256(result_bytes), records=records,
                rights_status='unreviewed-do-not-publish')


def analyze_run(run: dict, cache: Cache, *, agent: str, language: str = 'python',
                model: str | None = None) -> list[dict]:
    """Analyze one language track after an evidence-bound review of its artifacts."""
    review = run.get('reviewed_manifest')
    digest = review.get('manifest_sha256') if isinstance(review, dict) else None
    confirmations = review.get('base_commit_confirmations', {}) if isinstance(review, dict) else {}
    dataset = run.get('dataset', {})
    files = dataset.get('files', [])
    aggregate = sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode())
    result_digest = run.get('result_sha256')
    submission_sha = run.get('submission_revision')
    if language not in LANGUAGES:
        raise ValueError(f'unsupported language: {language}')
    selected = [r for r in run.get('records', []) if r.get('language') == language]
    if not selected:
        raise ValueError(f'no submitted tasks for language track: {language}')
    candidates = [r for r in selected if r.get('artifact_status') == 'present'
                  and r.get('published_outcome') in ('success', 'failure')]
    confirmed = isinstance(confirmations, dict) and all(
        confirmations.get(r['task_id']) == r['base_commit'] for r in candidates)
    historical_verified = isinstance(review, dict) and review.get('historical_dataset_match') == 'verified'
    if (not isinstance(review, dict) or not isinstance(review.get('review_url'), str)
            or not review['review_url'].startswith(('https://', 'http://'))
            or not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest)
            or not re.fullmatch(r'[0-9a-f]{64}', aggregate)
            or dataset.get('dataset_checksum') != aggregate
            or review.get('dataset_checksum') != aggregate
            or not isinstance(result_digest, str) or not re.fullmatch(r'[0-9a-f]{64}', result_digest)
            or review.get('result_sha256') != result_digest
            or not isinstance(submission_sha, str) or not SHA.fullmatch(submission_sha)
            or review.get('submission_revision') != submission_sha
            or not (historical_verified or (candidates and confirmed))):
        raise ValueError('analysis requires reviewed manifest digest, bound provenance checksums, and historical dataset verification')
    from .benchmark import analyze_submission
    submitted = {r['task_id']: r for r in selected}
    resolved = {r['task_id'] for r in selected if r['published_outcome'] == 'success'}
    evaluated = {r['task_id'] for r in selected if r['published_outcome'] in ('success', 'failure')}
    details = {k: [r['task_id'] for r in selected if r['published_outcome'] == outcome]
               for k, outcome in (('resolved', 'success'), ('failed', 'failure'),
                                  ('error', 'error'), ('incomplete', 'incomplete'))}
    predictions = {task: r['patch'] for task, r in submitted.items()}
    dataset = [dict(instance_id=r['task_id'], repo=r['repo'], base_commit=r['base_commit'],
                    language=r['language'], patch='') for r in selected]
    submission = dict(agent=agent, predictions=predictions, resolved=resolved, evaluated=evaluated,
                      result_details=details,
                      provenance=dict(prediction_url=run['result_url'], model=model, agent=agent,
                                      config=run.get('config'), dataset=run['dataset']),
                      prediction_locations={r['task_id']: r['provenance']['patch_url'] for r in selected})
    measure_ids = [r['task_id'] for r in selected if r['artifact_status'] != 'not_selected']
    analyzed = {r['task_id']: r for r in analyze_submission(submission, cache, dataset,
                              task_ids=measure_ids, include_failed=True)}
    records = []
    for source in selected:
        record = analyzed[source['task_id']]
        record['published_outcome'] = source['published_outcome']
        record['provenance'].update(source['provenance'])
        record['provenance']['reviewed_manifest'] = dict(review)
        if source['artifact_status'] == 'empty_patch':
            record.update(metrics=None, analysis_status='empty_patch')
        elif source['artifact_status'] == 'missing':
            record.update(metrics=None, analysis_status='missing_patch')
        elif source['artifact_status'] == 'not_selected':
            record.update(metrics=None, analysis_status='not_selected')
        records.append(record)
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', default='.parsimony-cache')
    parser.add_argument('--submission-revision', required=True)
    parser.add_argument('--config-path', required=True, help='path under submissions/ at the pinned commit')
    parser.add_argument('--dataset', required=True, help='Hugging Face dataset id')
    parser.add_argument('--dataset-revision', required=True, help='full immutable 40-character HF commit SHA')
    parser.add_argument('--dataset-file', action='append', required=True,
                        help='HF file path, LANGUAGE=PATH for explicit language; repeatable')
    parser.add_argument('--task-id', action='append', default=[], help='fetch patch for selected task (repeatable)')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        run = import_run(Cache(args.cache, timeout=90), submission_revision=args.submission_revision,
                         config_path=args.config_path, dataset=args.dataset,
                         dataset_revision=args.dataset_revision, dataset_files=args.dataset_file,
                         task_ids=args.task_id)
        Path(args.output).write_text(json.dumps(run, sort_keys=True, indent=2) + '\n')
        print(f"Wrote {len(run['records'])} task records to {args.output}; not publication-ready")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
