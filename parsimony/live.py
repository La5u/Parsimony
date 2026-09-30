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
from threading import Lock
from urllib.error import HTTPError
from urllib.parse import quote

from .artifacts import Cache

GITHUB = 'https://github.com/SWE-bench-Live/submission'
HF = 'https://huggingface.co'
SHA = re.compile(r'^[0-9a-f]{40}$')
CATEGORIES = ('success', 'failure', 'error', 'incomplete', 'empty_patch')
LANGUAGES = ('python', 'javascript', 'typescript', 'go')
_CSV_LOCK = Lock()
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
        # Gold patches can exceed csv's 128 KiB default. Bound fields by the
        # already-fetched document and restore the process-wide parser setting.
        with _CSV_LOCK:
            previous_limit = csv.field_size_limit()
            try:
                csv.field_size_limit(max(previous_limit, len(text)))
                rows = list(csv.DictReader(io.StringIO(text)))
            finally:
                csv.field_size_limit(previous_limit)
    else:
        raise ValueError('supported task file formats are JSON, JSONL/NDJSON, CSV and Parquet')
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError('HF task file must contain a list of task objects')
    return rows, dict(dataset=dataset, revision=revision, revision_url=api,
                      revision_sha256=sha256(metadata_bytes), dataset_file_url=url,
                      dataset_file_sha256=sha256(raw))


def _result_categories(result: dict) -> dict[str, set[str]]:
    """Validate source counts before translating the two observed result schemas."""
    if 'resolved_ids' in result or 'unresolved_ids' in result:
        result = dict(result)
        for category, source in (('success', 'resolved'), ('failure', 'unresolved'),
                                 ('error', 'error'), ('empty_patch', 'empty_patch'),
                                 ('incomplete', 'incomplete')):
            key = source + '_ids'
            # AMI schema v2 omits unused artifact/error lists and some counts.
            value = result.get(key, [] if category not in ('success', 'failure') else None)
            result[category + '_ids'] = value
            count_key = source + '_instances'
            result[category] = (result[count_key] if count_key in result else
                                len(value) if isinstance(value, list) else None)
        if 'submitted_ids' not in result:
            lists = [result[category + '_ids'] for category in CATEGORIES]
            if any(not isinstance(ids, list) or any(not isinstance(x, str) for x in ids) for ids in lists):
                raise ValueError('results.json category IDs must be string lists')
            result['submitted_ids'] = sorted(set().union(*lists))
        result['submitted'] = (result['submitted_instances'] if 'submitted_instances' in result else
                               len(result['submitted_ids']) if isinstance(result['submitted_ids'], list) else None)
        completed = result.get('completed_ids')
        if (not isinstance(completed, list) or any(not isinstance(x, str) for x in completed)
                or len(completed) != len(set(completed))
                or type(result.get('completed_instances')) is not int
                or result['completed_instances'] != len(completed)):
            raise ValueError('completed count/IDs disagree')
        outcomes = [result.get('success_ids'), result.get('failure_ids')]
        if any(not isinstance(ids, list) or any(not isinstance(x, str) for x in ids) for ids in outcomes):
            raise ValueError('resolved/unresolved IDs must be string lists')
        if set(completed) != set(outcomes[0]) | set(outcomes[1]):
            raise ValueError('completed IDs disagree with resolved/unresolved IDs')
        if (type(result.get('total_instances')) is not int
                or result['total_instances'] < max(len(completed), len(result['submitted_ids'])
                                                  if isinstance(result['submitted_ids'], list) else 0)):
            raise ValueError('invalid total_instances count')
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


def _optional_bytes(cache: Cache, url: str) -> bytes | None:
    try:
        return cache.get(url)
    except HTTPError as exc:
        if exc.code not in (403, 404):
            raise
        exc.close()
        return None


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f'duplicate JSON key: {key}')
        value[key] = item
    return value


def _predictions(raw: bytes) -> dict[str, dict]:
    """Keyed Live predictions and equivalent instance_id list exports."""
    value = json.loads(raw, object_pairs_hook=_unique_object)
    if isinstance(value, dict):
        entries = value.items()
    elif isinstance(value, list):
        if any(not isinstance(row, dict) for row in value):
            raise ValueError('preds.json list must contain prediction objects')
        entries = ((row.get('instance_id'), row) for row in value)
    else:
        raise ValueError('preds.json must be a keyed object or instance_id list')
    predictions = {}
    for task_id, row in entries:
        if not isinstance(task_id, str) or not task_id or task_id in predictions:
            raise ValueError('preds.json has missing or duplicate task IDs')
        if not isinstance(row, dict) or not isinstance(row.get('model_patch'), str):
            raise ValueError(f'{task_id}: prediction must contain string model_patch')
        if 'instance_id' in row and row['instance_id'] != task_id:
            raise ValueError(f'{task_id}: prediction key/instance_id disagree')
        predictions[task_id] = row
    return predictions


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
               dataset_files=None, task_ids: list[str] | None = None,
               verify_patch_files: bool = False, agent: str = 'swe-bench-live',
               model: str | None = None) -> dict:
    """Inventory a run against explicitly mapped immutable dataset files."""
    if not SHA.fullmatch(submission_revision):
        raise ValueError('submission revision must be a full Git commit SHA')
    if config_path.startswith('/') or '..' in Path(config_path).parts:
        raise ValueError('invalid submission configuration path')
    base = f'https://raw.githubusercontent.com/SWE-bench-Live/submission/{submission_revision}/{config_path.strip("/")}'
    result_url = base + '/result.json'
    try:
        result, result_bytes = _json(cache, result_url)
    except HTTPError as exc:
        if exc.code != 404:
            raise
        exc.close()
        result_url = base + '/results.json'
        result, result_bytes = _json(cache, result_url)
    categories = _result_categories(result)
    prediction_url = base + '/preds.json'
    prediction_bytes = _optional_bytes(cache, prediction_url)
    predictions = _predictions(prediction_bytes) if prediction_bytes is not None else {}
    prediction_digest = sha256(prediction_bytes) if prediction_bytes is not None else None
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
    submitted_ids = result.get('submitted_ids', sorted(set().union(*categories.values())))
    submitted = set(submitted_ids)
    run_ids = submitted | set(predictions)
    if not run_ids <= set(by_id):
        raise ValueError(f'run IDs absent from dataset (count={len(run_ids-set(by_id))})')
    selected_ids = set(task_ids or [])
    if selected_ids - set(by_id):
        raise ValueError(f'task selection contains IDs absent from dataset: {sorted(selected_ids-set(by_id))}')
    records = []
    population_ids = submitted_ids + [task for task in by_id if task not in submitted]
    prediction_is_list = (prediction_bytes is not None
                          and prediction_bytes.decode('utf-8-sig').lstrip().startswith('['))
    prediction_indexes = {task: i for i, task in enumerate(predictions)}
    patch_root = (base + '/logs/rollouts'
                  if config_path.strip('/') == 'submissions/lite/tianxicode/deepseek-flash' else base)
    for task_id in population_ids:
        meta = by_id[task_id]
        task_path = f'{patch_root}/{quote(task_id, safe="")}/patch.diff'
        prediction = predictions.get(task_id)
        patch_url = task_path
        patch = None
        patch_digest = sha256(prediction['model_patch'].encode('utf-8')) if prediction is not None else None
        separate_digest = None
        agreement = 'not_checked'
        artifact_status = 'missing'
        if prediction is not None:
            pointer = (str(prediction_indexes[task_id]) if prediction_is_list
                       else task_id.replace('~', '~0').replace('/', '~1'))
            patch_url = prediction_url + '#/' + quote(pointer, safe='') + '/model_patch'
        source_empty = task_id in categories['empty_patch']
        if source_empty:
            artifact_status = 'empty_patch'
            if prediction is not None and prediction['model_patch'].strip():
                raise ValueError(f'{task_id}: empty_patch category disagrees with prediction')
        if selected_ids and task_id not in selected_ids and not source_empty and task_id in run_ids:
            artifact_status = 'not_selected'
        elif task_id in run_ids:
            if prediction is not None:
                patch = prediction['model_patch']
                artifact_status = 'present' if patch.strip() else 'empty_patch'
            if (prediction is None and not source_empty) or verify_patch_files:
                raw_patch = _optional_bytes(cache, task_path)
                if raw_patch is not None:
                    separate_digest = sha256(raw_patch)
                    separate_patch = raw_patch.decode('utf-8-sig')
                    if prediction is not None:
                        if separate_patch != prediction['model_patch']:
                            raise ValueError(f'{task_id}: prediction and patch.diff disagree')
                        agreement = 'matched'
                    else:
                        patch, patch_digest = separate_patch, separate_digest
                        artifact_status = 'present' if patch.strip() else 'empty_patch'
                    if source_empty and separate_patch.strip():
                        raise ValueError(f'{task_id}: empty_patch category disagrees with patch.diff')
                elif verify_patch_files:
                    agreement = 'separate_patch_unavailable'
        if artifact_status == 'empty_patch':
            patch = None
        outcome = next((category for category in ('success', 'failure', 'error', 'incomplete')
                        if task_id in categories[category]), 'unknown')
        provenance = dict(submission_revision=submission_revision,
                          submission_url=f'{GITHUB}/tree/{submission_revision}/{config_path}',
                          result_url=result_url, result_sha256=sha256(result_bytes),
                          patch_url=patch_url, patch_sha256=patch_digest,
                          dataset_file=meta['dataset_file'])
        if prediction is not None:
            provenance.update(prediction_url=prediction_url, prediction_sha256=prediction_digest,
                              prediction_location=patch_url,
                              reported_model=prediction.get('model_name_or_path'),
                              separate_patch_url=task_path, separate_patch_sha256=separate_digest,
                              patch_agreement=agreement)
        record = dict(task_id=task_id, repo=meta['repo'], base_commit=meta['base_commit'],
                      language=meta['language'], submitted=task_id in submitted,
                      published_outcome=outcome,
                      published_result_categories=[c for c in CATEGORIES if task_id in categories[c]],
                      artifact_status=artifact_status, patch=patch, provenance=provenance)
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
                model=model, agent=agent, config=config_path, result_metadata=result,
                prediction_url=prediction_url if prediction_bytes is not None else None,
                prediction_sha256=prediction_digest,
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
    blocked = review.get('blocked_preimages', {}) if isinstance(review, dict) else {}
    if not isinstance(blocked, dict):
        raise ValueError('blocked_preimages must be a task mapping')
    # A failed preimage audit must remain an unmeasured item in the full population.
    # Its evidence is bound to the actual patch, not used to invent zero metrics.
    for task, evidence in blocked.items():
        source = next((r for r in selected if r['task_id'] == task), None)
        if (source is None or not isinstance(evidence, dict)
                or evidence.get('status') not in ('unverified', 'hunks_match_without_blob_identity')
                or evidence.get('patch_sha256') != sha256((source.get('patch') or '').encode())):
            raise ValueError('blocked preimage evidence does not match the selected patch')
    confirmed = isinstance(confirmations, dict) and all(
        confirmations.get(r['task_id']) == r['base_commit'] or r['task_id'] in blocked
        for r in candidates)
    historical_verified = isinstance(review, dict) and review.get('historical_dataset_match') == 'verified'
    prediction_digest = run.get('prediction_sha256')
    prediction_bound = prediction_digest is None or (
        isinstance(prediction_digest, str) and re.fullmatch(r'[0-9a-f]{64}', prediction_digest)
        and isinstance(review, dict) and review.get('prediction_sha256') == prediction_digest
        and all(r['provenance'].get('prediction_sha256') == prediction_digest
                and isinstance(r.get('patch'), str)
                and r['provenance'].get('patch_sha256') == sha256(r['patch'].encode('utf-8'))
                for r in candidates if r['provenance'].get('prediction_url')))
    if (not isinstance(review, dict) or not isinstance(review.get('review_url'), str)
            or not review['review_url'].startswith(('https://', 'http://'))
            or not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest)
            or not re.fullmatch(r'[0-9a-f]{64}', aggregate)
            or dataset.get('dataset_checksum') != aggregate
            or review.get('dataset_checksum') != aggregate
            or not isinstance(result_digest, str) or not re.fullmatch(r'[0-9a-f]{64}', result_digest)
            or review.get('result_sha256') != result_digest
            or not prediction_bound
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
    details['empty_patch'] = [r['task_id'] for r in selected
                              if 'empty_patch' in r.get('published_result_categories', [])]
    predictions = {task: r['patch'] for task, r in submitted.items()}
    dataset = [dict(instance_id=r['task_id'], repo=r['repo'], base_commit=r['base_commit'],
                    language=r['language'], patch='') for r in selected]
    submission = dict(agent=agent, predictions=predictions, resolved=resolved, evaluated=evaluated,
                      result_details=details,
                      provenance=dict(prediction_url=run.get('prediction_url') or run['result_url'],
                                      prediction_sha256=run.get('prediction_sha256'),
                                      result_url=run['result_url'], result_sha256=run['result_sha256'],
                                      model=model if model is not None else run.get('model'), agent=agent,
                                      source_agent=run.get('agent'),
                                      config=run.get('config'), dataset=run['dataset']),
                      prediction_locations={r['task_id']: r['provenance']['patch_url'] for r in selected})
    measure_ids = [r['task_id'] for r in selected
                   if r['artifact_status'] != 'not_selected' and r['task_id'] not in blocked]
    analyzed = {r['task_id']: r for r in analyze_submission(submission, cache, dataset,
                              task_ids=measure_ids, include_failed=True)}
    records = []
    for source in selected:
        record = analyzed[source['task_id']]
        record['published_outcome'] = source['published_outcome']
        record['submitted'] = source.get('submitted', True)
        record['source_result_categories'] = source.get('published_result_categories',
                                                       record['published_result_categories'])
        record['provenance'].update(source['provenance'])
        record['provenance']['historical_dataset_match'] = run.get('historical_dataset_match', 'unverified')
        record['provenance']['reviewed_manifest'] = {
            k: v for k, v in review.items() if k not in ('base_commit_confirmations', 'blocked_preimages')}
        record['provenance']['base_review_scope'] = review.get('scope', 'task-base-confirmation')
        if source['task_id'] in blocked:
            record.update(metrics=None, analysis_status='unverified_preimage',
                          analysis_error=blocked[source['task_id']].get('error',
                              'before-source blob identity not established'))
            record['provenance']['preimage_audit'] = blocked[source['task_id']]
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
    parser.add_argument('--output', required=True, help='normalized JSON run inventory')
    parser.add_argument('--verify-patch-files', action='store_true',
                        help='compare selected predictions with separate patch.diff files when available')
    parser.add_argument('--review-manifest', help='evidence-bound review JSON required for analysis')
    parser.add_argument('--agent', default='swe-bench-live')
    parser.add_argument('--model')
    parser.add_argument('--language', choices=LANGUAGES, default='python')
    parser.add_argument('--records-output', help='optional analyzed JSONL output (requires --review-manifest)')
    args = parser.parse_args()
    if args.records_output and not args.review_manifest:
        parser.error('--records-output requires --review-manifest')
    try:
        cache = Cache(args.cache, timeout=90)
        run = import_run(cache, submission_revision=args.submission_revision,
                         config_path=args.config_path, dataset=args.dataset,
                         dataset_revision=args.dataset_revision, dataset_files=args.dataset_file,
                         task_ids=args.task_id, verify_patch_files=args.verify_patch_files,
                         agent=args.agent, model=args.model)
        if args.review_manifest:
            review_bytes = Path(args.review_manifest).read_bytes()
            review = json.loads(review_bytes)
            if not isinstance(review, dict):
                raise ValueError('review manifest must contain a JSON object')
            run['reviewed_manifest'] = dict(review, manifest_sha256=sha256(review_bytes))
        if args.records_output:
            records = analyze_run(run, cache, agent=args.agent, model=args.model, language=args.language)
            Path(args.records_output).write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
        Path(args.output).write_text(json.dumps(run, sort_keys=True, indent=2) + '\n')
        print(f"Wrote {len(run['records'])} task records to {args.output}; not publication-ready")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
