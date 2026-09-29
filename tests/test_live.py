import hashlib
import json
import unittest
from urllib.error import HTTPError
from unittest.mock import patch
import sys
import types

from parsimony.live import analyze_run, fetch_hf_rows, import_run

REV = 'a' * 40
HF_REV = 'b' * 40
ROOT = ('https://raw.githubusercontent.com/SWE-bench-Live/submission/' + REV
        + '/submissions/python/sweagent/demo')
API = f'https://huggingface.co/api/datasets/org/tasks/revision/{HF_REV}'
DATA = f'https://huggingface.co/datasets/org/tasks/resolve/{HF_REV}/tasks.jsonl'


class FixtureCache:
    def __init__(self, values):
        self.values = values
        self.requested = []

    def get(self, url):
        self.requested.append(url)
        if url not in self.values:
            raise AssertionError('unexpected request: ' + url)
        value = self.values[url]
        if isinstance(value, Exception):
            raise value
        return value


class LiveImporterTests(unittest.TestCase):
    def setUp(self):
        result = dict(submitted=5, submitted_ids=['pass', 'fail', 'empty', 'err', 'todo'],
                      success=1, success_ids=['pass'], failure=2, failure_ids=['fail', 'empty'],
                      empty_patch=1, empty_patch_ids=['empty'], error=1, error_ids=['err'],
                      incomplete=1, incomplete_ids=['todo'])
        tasks = [dict(instance_id=task, repo='org/repo', base_commit='c' * 40, language='python')
                 for task in result['submitted_ids']]
        self.cache = FixtureCache({
            ROOT + '/result.json': json.dumps(result).encode(),
            API: json.dumps({'sha': HF_REV}).encode(),
            DATA: ('\n'.join(json.dumps(row) for row in tasks)).encode(),
            ROOT + '/pass/patch.diff': b'diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n@@ -1 +1 @@\n-x = 1\n+y = 2\n',
            ROOT + '/fail/patch.diff': b'diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n@@ -1 +1 @@\n-x = 1\n+y = 2\n',
            ROOT + '/err/patch.diff': HTTPError(ROOT, 404, 'missing', {}, None),
            ROOT + '/todo/patch.diff': HTTPError(ROOT, 404, 'missing', {}, None),
            'https://raw.githubusercontent.com/org/repo/' + 'c' * 40 + '/a.py': b'x = 1\n',
        })

    def run_import(self, **kwargs):
        args = dict(submission_revision=REV, config_path='submissions/python/sweagent/demo',
                    dataset='org/tasks', dataset_revision=HF_REV, dataset_file='tasks.jsonl')
        args.update(kwargs)
        return import_run(self.cache, **args)

    def test_import_preserves_outcomes_empty_patch_and_provenance(self):
        run = self.run_import()
        by_id = {r['task_id']: r for r in run['records']}
        self.assertEqual([by_id[x]['published_outcome'] for x in ('pass', 'fail', 'err', 'todo')],
                         ['success', 'failure', 'error', 'incomplete'])
        self.assertEqual(by_id['empty']['published_outcome'], 'failure')
        self.assertEqual(by_id['empty']['artifact_status'], 'empty_patch')
        self.assertIsNone(by_id['empty']['patch'])
        self.assertEqual(by_id['pass']['provenance']['patch_sha256'],
                         hashlib.sha256(self.cache.values[ROOT + '/pass/patch.diff']).hexdigest())
        self.assertEqual(run['rights_status'], 'unreviewed-do-not-publish')
        self.assertIn(API, self.cache.requested)

    def test_unavailable_patch_is_distinct_from_empty_and_failure(self):
        self.cache.values[ROOT + '/fail/patch.diff'] = HTTPError(ROOT, 404, 'missing', {}, None)
        run = self.run_import()
        fail = next(row for row in run['records'] if row['task_id'] == 'fail')
        self.assertEqual(fail['published_outcome'], 'failure')
        self.assertEqual(fail['artifact_status'], 'missing')

    def test_shared_strict_analyzer_handles_success_failure_and_empty_separately(self):
        run = self.run_import()
        self.review(run)
        records = {row['task_id']: row for row in analyze_run(run, self.cache, agent='pilot')}
        self.assertEqual(records['pass']['analysis_status'], 'ok')
        self.assertEqual(records['fail']['analysis_status'], 'ok')
        self.assertEqual(records['pass']['evaluation_result'], 'resolved')
        self.assertEqual(records['fail']['evaluation_result'], 'failed')
        self.assertEqual(records['empty']['analysis_status'], 'empty_patch')
        self.assertIsNone(records['empty']['metrics'])
        self.assertEqual(records['err']['analysis_status'], 'missing_patch')
        self.assertEqual(records['todo']['analysis_status'], 'missing_patch')
        self.assertFalse(records['err']['resolved'])
        self.assertEqual(records['err']['evaluation_result'], 'unknown')

    def test_empty_only_submitted_ids_are_unknown_and_dataset_may_be_larger(self):
        result = json.loads(self.cache.values[ROOT + '/result.json'])
        result['submitted_ids'].append('only-empty')
        result['submitted'] += 1
        result['empty_patch_ids'].append('only-empty')
        result['empty_patch'] += 1
        self.cache.values[ROOT + '/result.json'] = json.dumps(result).encode()
        tasks = [json.loads(line) for line in self.cache.values[DATA].decode().splitlines()]
        tasks.append(dict(instance_id='only-empty', repo='org/repo', base_commit='c' * 40,
                          language='python'))
        tasks.append(dict(instance_id='not-submitted', repo='org/repo', base_commit='c' * 40,
                          language='python'))
        self.cache.values[DATA] = ('\n'.join(json.dumps(row) for row in tasks)).encode()
        run = self.run_import()
        row = next(r for r in run['records'] if r['task_id'] == 'only-empty')
        self.assertEqual(row['published_outcome'], 'unknown')
        self.assertEqual(run['dataset_task_count'], 7)
        self.assertEqual(run['completeness_audit']['dataset_only_count'], 1)

    def review(self, run):
        run['reviewed_manifest'] = dict(
            review_url='https://example.org/reviews/live-run',
            manifest_sha256='d' * 64,
            dataset_checksum=run['dataset']['dataset_checksum'],
            result_sha256=run['result_sha256'],
            submission_revision=run['submission_revision'],
            historical_dataset_match='verified')

    def test_analysis_requires_evidence_bound_review_and_preserves_dataset_language(self):
        run = self.run_import()
        with self.assertRaisesRegex(ValueError, 'reviewed manifest'):
            analyze_run(run, self.cache, agent='pilot')
        self.review(run)
        records = analyze_run(run, self.cache, agent='pilot', language='python')
        self.assertTrue(all(row.get('measurement_track') is None for row in records))
        self.assertTrue(all(source['language'] == 'python' for source in run['records']))
        with self.assertRaisesRegex(ValueError, 'no submitted tasks'):
            analyze_run(run, self.cache, agent='pilot', language='go')

    def test_category_count_and_base_metadata_validation(self):
        result = json.loads(self.cache.values[ROOT + '/result.json'])
        result['failure'] = 99
        self.cache.values[ROOT + '/result.json'] = json.dumps(result).encode()
        with self.assertRaisesRegex(ValueError, 'failure count'):
            self.run_import()
        self.setUp()
        rows = [json.loads(line) for line in self.cache.values[DATA].decode().splitlines()]
        rows[0]['base_commit'] = 'abc'
        self.cache.values[DATA] = ('\n'.join(json.dumps(row) for row in rows)).encode()
        with self.assertRaisesRegex(ValueError, 'full 40-character'):
            self.run_import()

    def test_mutable_or_unverified_hf_revision_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'full 40-character'):
            self.run_import(dataset_revision='main')
        self.cache.values[API] = b'{"sha":"' + b'c' * 40 + b'"}'
        with self.assertRaisesRegex(ValueError, 'verification failed'):
            self.run_import()

    def test_dataset_id_and_base_metadata_are_mandatory(self):
        self.cache.values[DATA] = json.dumps({"instance_id":"different","repo":"org/repo",
                                               "base_commit":"c" * 40,"language":"python"}).encode()
        with self.assertRaisesRegex(ValueError, 'absent from dataset'):
            self.run_import()

    def test_mixed_languages_are_inventoried_and_supported_track_selected(self):
        rows = [json.loads(line) for line in self.cache.values[DATA].decode().splitlines()]
        labels = ['Python', 'JavaScript', 'TypeScript', 'Go', 'TS/JS']
        for row, label in zip(rows, labels):
            row['language'] = label
        self.cache.values[DATA] = ('\n'.join(json.dumps(row) for row in rows)).encode()
        run = self.run_import()
        self.assertEqual([r['language'] for r in run['records']],
                         ['python', 'javascript', 'typescript', 'go', 'typescript-javascript'])
        self.review(run)
        records = analyze_run(run, self.cache, agent='pilot', language='python')
        self.assertEqual([r['task_id'] for r in records], ['pass'])

    def test_explicit_multifile_language_mapping_and_task_selection_preserve_inventory(self):
        rows = [json.loads(line) for line in self.cache.values[DATA].decode().splitlines()]
        for row in rows:
            row.pop('language')
        first, second = rows[:3], rows[3:]
        files = ['python=python.jsonl', 'go=go.jsonl']
        urls = [f'https://huggingface.co/datasets/org/tasks/resolve/{HF_REV}/{name}'
                for name in ('python.jsonl', 'go.jsonl')]
        self.cache.values[urls[0]] = '\n'.join(json.dumps(r) for r in first).encode()
        self.cache.values[urls[1]] = '\n'.join(json.dumps(r) for r in second).encode()
        run = self.run_import(dataset_files=files, task_ids=['pass'])
        self.assertEqual([r['language'] for r in run['records']],
                         ['python', 'python', 'python', 'go', 'go'])
        self.assertEqual([r['artifact_status'] for r in run['records']],
                         ['present', 'not_selected', 'empty_patch', 'not_selected', 'not_selected'])
        self.assertEqual(len(run['dataset']['files']), 2)
        self.review(run)
        records = {r['task_id']: r for r in analyze_run(run, self.cache, agent='pilot')}
        self.assertEqual(records['fail']['analysis_status'], 'not_selected')
        self.assertEqual(records['fail']['evaluation_result'], 'failed')
        self.assertEqual(records['fail']['schema_version'], 2)
        self.assertTrue(all(r['benchmark_tasks'] == 3 for r in records.values()))
        self.assertTrue(all(r['published_resolved_count'] == 1 for r in records.values()))
        self.assertFalse(any(url in self.cache.requested for url in
                             (ROOT + '/fail/patch.diff', ROOT + '/err/patch.diff', ROOT + '/todo/patch.diff')))

    def test_explicit_language_conflict_and_cross_file_duplicate_fail(self):
        rows = [json.loads(line) for line in self.cache.values[DATA].decode().splitlines()]
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            self.run_import(dataset_files=[('go', 'tasks.jsonl')])
        duplicate_url = f'https://huggingface.co/datasets/org/tasks/resolve/{HF_REV}/other.jsonl'
        self.cache.values[duplicate_url] = json.dumps(rows[0]).encode()
        with self.assertRaisesRegex(ValueError, 'duplicate task IDs across files'):
            self.run_import(dataset_files=['tasks.jsonl', 'other.jsonl'])

    def test_review_manifest_fails_closed_without_digest_or_historical_verification(self):
        run = self.run_import()
        self.review(run)
        del run['reviewed_manifest']['manifest_sha256']
        with self.assertRaisesRegex(ValueError, 'reviewed manifest digest'):
            analyze_run(run, self.cache, agent='pilot')
        self.review(run)
        run['reviewed_manifest']['historical_dataset_match'] = 'unverified'
        with self.assertRaisesRegex(ValueError, 'historical dataset verification'):
            analyze_run(run, self.cache, agent='pilot')

    def test_parquet_reader_uses_optional_lazy_pyarrow_and_raw_bytes(self):
        values = {API: json.dumps({'sha': HF_REV}).encode(),
                  f'https://huggingface.co/datasets/org/tasks/resolve/{HF_REV}/tasks.parquet': b'PARQUET'}
        cache = FixtureCache(values)
        fake = types.ModuleType('pyarrow.parquet')
        seen = []
        fake.read_table = lambda source: (seen.append(source.read()) or types.SimpleNamespace(
            to_pylist=lambda: [{'instance_id': 'x'}]))
        package = types.ModuleType('pyarrow')
        package.parquet = fake
        with patch.dict(sys.modules, {'pyarrow': package, 'pyarrow.parquet': fake}):
            rows, _ = fetch_hf_rows(cache, 'org/tasks', HF_REV, 'tasks.parquet')
        self.assertEqual(rows, [{'instance_id': 'x'}])
        self.assertEqual(seen, [b'PARQUET'])

    def test_parquet_missing_optional_dependency_has_informative_error(self):
        values = {API: json.dumps({'sha': HF_REV}).encode(),
                  f'https://huggingface.co/datasets/org/tasks/resolve/{HF_REV}/tasks.parquet': b'PARQUET'}
        cache = FixtureCache(values)
        original = __import__
        def importer(name, *args, **kwargs):
            if name == 'pyarrow.parquet':
                raise ImportError('missing')
            return original(name, *args, **kwargs)
        with patch('builtins.__import__', side_effect=importer):
            with self.assertRaisesRegex(ValueError, 'optional pyarrow'):
                fetch_hf_rows(cache, 'org/tasks', HF_REV, 'tasks.parquet')

    def test_empty_only_real_population_layout_is_covered(self):
        from parsimony.live import _result_categories
        result = dict(submitted=230, submitted_ids=[f't{i}' for i in range(230)],
                      success=105, success_ids=[f't{i}' for i in range(105)],
                      failure=120, failure_ids=[f't{i}' for i in range(105, 225)],
                      error=0, error_ids=[], incomplete=0, incomplete_ids=[],
                      empty_patch=5, empty_patch_ids=[f't{i}' for i in range(225, 230)])
        categories = _result_categories(result)
        self.assertEqual(len(categories['empty_patch']), 5)

    def test_missing_outcome_and_empty_ids_are_rejected(self):
        from parsimony.live import _result_categories
        result = dict(submitted=1, submitted_ids=['lost'], success=0, success_ids=[],
                      failure=0, failure_ids=[], error=0, error_ids=[], incomplete=0,
                      incomplete_ids=[], empty_patch=0, empty_patch_ids=[])
        with self.assertRaisesRegex(ValueError, 'outcome or be listed'):
            _result_categories(result)

    def test_outcome_overlap_is_rejected(self):
        result = json.loads(self.cache.values[ROOT + '/result.json'])
        result['failure_ids'].append('pass')
        result['failure'] += 1
        self.cache.values[ROOT + '/result.json'] = json.dumps(result).encode()
        with self.assertRaisesRegex(ValueError, 'overlap'):
            self.run_import()


if __name__ == '__main__':
    unittest.main()
