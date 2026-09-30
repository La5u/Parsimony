import hashlib
import json
import unittest
from urllib.error import HTTPError
from unittest.mock import patch
import sys
import types
import tempfile
from pathlib import Path

from parsimony.live import analyze_run, fetch_hf_rows, import_run, main, _predictions, _result_categories

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


class LargeDatasetTests(unittest.TestCase):
    def test_csv_gold_patch_larger_than_default_limit_and_limit_restored(self):
        import csv
        before = csv.field_size_limit()
        url = DATA.replace('tasks.jsonl', 'tasks.csv')
        patch_text = 'x' * (before + 1)
        cache = FixtureCache({API: json.dumps({'sha': HF_REV}).encode(),
                              url: ('instance_id,patch\ntask,' + patch_text + '\n').encode()})
        rows, source = fetch_hf_rows(cache, 'org/tasks', HF_REV, 'tasks.csv')
        self.assertEqual(rows[0]['patch'], patch_text)
        self.assertEqual(csv.field_size_limit(), before)
        self.assertEqual(source['dataset_file_url'], url)


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
            ROOT + '/preds.json': HTTPError(ROOT, 404, 'missing', {}, None),
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
        absent = next(r for r in run['records'] if r['task_id'] == 'not-submitted')
        self.assertEqual(absent['published_outcome'], 'unknown')
        self.assertFalse(absent['submitted'])
        self.assertEqual(absent['artifact_status'], 'missing')
        self.review(run)
        records = analyze_run(run, self.cache, agent='pilot')
        self.assertTrue(all(r['benchmark_tasks'] == 7 for r in records))
        absent = next(r for r in records if r['task_id'] == 'not-submitted')
        self.assertEqual(absent['evaluation_result'], 'unknown')
        self.assertIsNone(absent['metrics'])

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


# Small slices of bytes fetched from submission commit
# cba8a6d3197cd53da09f8527cccbc689782302a6 (results.json + preds.json).
# Category membership, field names, model labels and patch strings are source data;
# counts are reduced to the slice. HF task metadata below is deliberately mocked.
# Full source result SHA256s, in fixture order:
# 37fc86fe512305239c37cc0941c1acbc2c1c552318f0517158b85bc463f60f78
# f4f6a4d6c0eb3f36dec80e67bf5bc54c11426e6c46d6ac22659fab933d2be6e2
# a2c1e5ca4721b4e0eda122b9d3363325f853c463c0d1f22683c8f974ffe0d398
# 8a640495e50e9c20a9dc3f66c2d45e9c5aa3589562cab009c64a77797fafc21d
# d4475ae7be5abac5a3c1f7a49428e2fc5e19728834f58c37c3ca13f13ecd368e
PINNED_LAYOUTS = [
    ('lite/tianxicode/deepseek-flash', 'python',
     {'success': ['amoffat__sh-744'], 'failure': ['falconry__falcon-2419']},
     {'amoffat__sh-744': {'model_patch':
         'diff --git a/sh.py b/sh.py\nindex d52d8b6..1b26c78 100644\n'
         '--- a/sh.py\n+++ b/sh.py\n@@ -889,6 +889,9 @@ class RunningCommand:\n'
         '     def __await__(self):\n         async def wait_for_completion():\n'
         '             await self.aio_output_complete.wait()\n'
         '+            if self.call_args["return_cmd"]:\n+                self.wait()\n'
         '+                return self\n             return str(self)\n \n'
         '         return wait_for_completion().__await__()\n'}}),
    ('lite/sapient-slingshot-agent/v3.4.0/gpt-5.6-sol', 'python',
     {'success': ['sympy__sympy-27462'], 'failure': ['aws-cloudformation__cfn-lint-4023']},
     {'sympy__sympy-27462': {'model_name_or_path': 'SWE-Bench Agent', 'model_patch':
         'diff --git a/sympy/printing/pycode.py b/sympy/printing/pycode.py\n'
         'index 9d768b8c0a..f07785d612 100644\n'
         '--- a/sympy/printing/pycode.py\n+++ b/sympy/printing/pycode.py\n'
         '@@ -557,7 +557,7 @@ def _print_sign(self, e):\n \n'
         '     def _print_Not(self, expr):\n         PREC = precedence(expr)\n'
         "-        return self._operators['not'] + self.parenthesize(expr.args[0], PREC)\n"
         "+        return self._operators['not'] + ' ' + self.parenthesize(expr.args[0], PREC)\n"
         ' \n     def _print_IndexedBase(self, expr):\n         return expr.name\n'
         'diff --git a/sympy/printing/tests/test_pycode.py b/sympy/printing/tests/test_pycode.py\n'
         'index 84ac7c1c87..932b703c28 100644\n'
         '--- a/sympy/printing/tests/test_pycode.py\n+++ b/sympy/printing/tests/test_pycode.py\n'
         '@@ -1,3 +1,4 @@\n+from sympy import Not\n from sympy.codegen import Assignment\n'
         ' from sympy.codegen.ast import none\n from sympy.codegen.cfunctions import expm1, log1p\n'
         '@@ -40,6 +41,7 @@ def test_PythonCodePrinter():\n'
         "     assert prntr.doprint(And(x, y)) == 'x and y'\n"
         "     assert prntr.doprint(Or(x, y)) == 'x or y'\n"
         "     assert prntr.doprint(1/(x+y)) == '1/(x + y)'\n"
         "+    assert prntr.doprint(Not(x)) == 'not x'\n"
         '     assert not prntr.module_imports\n \n'
         "     assert prntr.doprint(pi) == 'math.pi'\n"}}),
    ('lite/aiwork-code/20260909-opus-4-8-xhigh', 'python',
     {'success': ['python-control__python-control-1111'],
      'failure': ['matplotlib__matplotlib-29007'], 'error': ['reflex-dev__reflex-5039'],
      'empty_patch': ['beeware__briefcase-2214']},
     {'beeware__briefcase-2214': {'model_name_or_path': 'claude-opus-4-8',
                               'instance_id': 'beeware__briefcase-2214', 'model_patch': ''},
      'python-control__python-control-1111': {'model_name_or_path': 'claude-opus-4-8',
          'instance_id': 'python-control__python-control-1111', 'model_patch':
          'diff --git a/control/flatsys/flatsys.py b/control/flatsys/flatsys.py\n'
          'index 7d76b9d7..5818d118 100644\n'
          '--- a/control/flatsys/flatsys.py\n+++ b/control/flatsys/flatsys.py\n'
          '@@ -721,8 +721,7 @@ def solve_flat_ocp(\n \n     # Process final time\n'
          '     timepts = np.atleast_1d(timepts)\n-    Tf = timepts[-1]\n'
          '-    T0 = timepts[0] if len(timepts) > 1 else T0\n'
          '+    T0 = timepts[0] if len(timepts) > 1 else 0\n \n'
          '     # Process keyword arguments\n     if trajectory_constraints is None:\n'}}),
    ('multilang/js_ts/slingshot-agent/v3.4.0/gpt-5.6-sol/js', 'javascript',
     {'success': ['hotwired__turbo-1421'], 'failure': ['jsonata-js__jsonata-809'],
      'error': ['proj4js__proj4js-560']},
     {'jsonata-js__jsonata-809': {'model_name_or_path': 'SWE-Bench Agent', 'model_patch':
         'diff --git a/src/functions.js b/src/functions.js\nindex 6f1d035..1c0f8f5 100644\n'
         '--- a/src/functions.js\n+++ b/src/functions.js\n'
         '@@ -342,7 +342,7 @@ const functions = (() => {\n      */\n'
         '     async function contains(str, token) {\n'
         '         // undefined inputs always return undefined\n'
         "-        if (typeof str === 'undefined') {\n"
         "+        if (typeof str === 'undefined' || typeof token === 'undefined') {\n"
         '             return undefined;\n         }\n \n'
         'diff --git a/test/test-suite/groups/function-contains/case007.json '
         'b/test/test-suite/groups/function-contains/case007.json\nnew file mode 100644\n'
         'index 0000000..e35fac4\n--- /dev/null\n'
         '+++ b/test/test-suite/groups/function-contains/case007.json\n@@ -0,0 +1,6 @@\n'
         '+{\n+    "expr": "$contains(\\"Hello World\\", nothing)",\n'
         '+    "dataset": null,\n+    "bindings": {},\n+    "undefinedResult": true\n+}\n'}}),
    ('multilang/js_ts/slingshot-agent/v3.4.0/gpt-5.6-sol/ts', 'typescript',
     {'success': ['honojs__hono-4269'], 'failure': ['QwenLM__qwen-code-349'],
      'error': ['better-auth__better-auth-4175']},
     {'honojs__hono-4269': {'model_name_or_path': 'SWE-Bench Agent', 'model_patch':
         'diff --git a/src/request.test.ts b/src/request.test.ts\n'
         'index 5e700059..a278bead 100644\n--- a/src/request.test.ts\n+++ b/src/request.test.ts\n'
         "@@ -222,6 +222,18 @@ describe('Body methods with caching', () => {\n"
         '     )\n   })\n \n'
         "+  test('req.json() should keep the content as is', async () => {\n"
         '+    const text = \'{ "foo" : "bar" }\'\n+    const req = new HonoRequest(\n'
         "+      new Request('http://localhost', {\n+        method: 'POST',\n"
         '+        body: text,\n+      })\n+    )\n'
         '+    expect(await req.json()).toEqual(JSON.parse(text))\n'
         '+    expect(await req.text()).toEqual(text)\n+  })\n+\n'
         "   test('req.arrayBuffer()', async () => {\n"
         '     const buffer = new TextEncoder().encode(\'{"foo":"bar"}\').buffer\n'
         '     const req = new HonoRequest(\n'
         'diff --git a/src/request.ts b/src/request.ts\nindex e93617c8..5dc034d3 100644\n'
         '--- a/src/request.ts\n+++ b/src/request.ts\n'
         "@@ -243,7 +243,7 @@ export class HonoRequest<P extends string = '/', I extends Input['out'] = {}> {\n"
         '    * ```\n    */\n   json<T = any>(): Promise<T> {\n'
         "-    return this.#cachedBody('json')\n"
         "+    return this.#cachedBody('text').then((text: string) => JSON.parse(text))\n"
         '   }\n \n   /**\n'}}),
]


class LiveJSONLayoutTests(unittest.TestCase):
    def fixture(self, index=0, *, as_list=False):
        path, language, memberships, predictions = PINNED_LAYOUTS[index]
        memberships = {key: memberships.get(key, []) for key in
                       ('success', 'failure', 'error', 'incomplete', 'empty_patch')}
        submitted = [task for ids in memberships.values() for task in ids]
        result = {key: len(ids) for key, ids in memberships.items()}
        result.update({key + '_ids': ids for key, ids in memberships.items()})
        result.update(submitted=len(submitted), submitted_ids=submitted)
        if index == 2:
            result = dict(schema_version=2, total_instances=len(submitted),
                          submitted_instances=len(submitted), submitted_ids=submitted,
                          completed_instances=len(memberships['success'] + memberships['failure']),
                          completed_ids=memberships['success'] + memberships['failure'],
                          resolved_instances=len(memberships['success']), resolved_ids=memberships['success'],
                          unresolved_instances=len(memberships['failure']), unresolved_ids=memberships['failure'],
                          error_instances=len(memberships['error']), error_ids=memberships['error'],
                          empty_patch_instances=len(memberships['empty_patch']),
                          empty_patch_ids=memberships['empty_patch'], incomplete_ids=[])
        root = ROOT.rsplit('/submissions/', 1)[0] + '/submissions/' + path
        # List coverage is an equivalent export of observed keyed rows, not a
        # claim that these five priority sources use lists.
        payload = ([dict(row, instance_id=task) for task, row in predictions.items()]
                   if as_list else predictions)
        tasks = [dict(instance_id=task, repo='org/repo', base_commit='c' * 40, language=language)
                 for task in submitted]
        tasks.append(dict(instance_id='dataset-only', repo='org/repo', base_commit='c' * 40,
                          language=language))
        values = {root + '/result.json': HTTPError(root, 404, 'missing', {}, None),
                  root + '/results.json': json.dumps(result).encode(),
                  root + '/preds.json': json.dumps(payload).encode(),
                  API: json.dumps({'sha': HF_REV}).encode(),
                  DATA: '\n'.join(json.dumps(row) for row in tasks).encode()}
        for task in submitted:
            patch_root = root + '/logs/rollouts' if index == 0 else root
            values[patch_root + '/' + task + '/patch.diff'] = HTTPError(root, 404, 'missing', {}, None)
        cache = FixtureCache(values)
        args = dict(submission_revision=REV, config_path='submissions/' + path,
                    dataset='org/tasks', dataset_revision=HF_REV, dataset_file='tasks.jsonl')
        return cache, args, result, predictions, root

    def review(self, run):
        LiveImporterTests.review(self, run)
        run['reviewed_manifest']['prediction_sha256'] = run['prediction_sha256']

    def test_all_priority_source_layouts_preserve_population_categories_and_locations(self):
        for index in range(len(PINNED_LAYOUTS)):
            with self.subTest(index=index):
                cache, args, result, predictions, root = self.fixture(index)
                run = import_run(cache, **args, agent='source-agent', model='reviewed-model')
                self.assertEqual(run['result_metadata'], result)
                self.assertEqual(run['agent'], 'source-agent')
                self.assertEqual(run['model'], 'reviewed-model')
                self.assertEqual(run['result_url'], root + '/results.json')
                self.assertEqual(run['result_sha256'], hashlib.sha256(cache.values[run['result_url']]).hexdigest())
                self.assertEqual(run['prediction_sha256'], hashlib.sha256(cache.values[root + '/preds.json']).hexdigest())
                self.assertEqual(len(run['records']), len(result['submitted_ids']) + 1)
                by_id = {r['task_id']: r for r in run['records']}
                categories = _result_categories(result)
                for category, ids in categories.items():
                    for task in ids:
                        self.assertIn(category, by_id[task]['published_result_categories'])
                        self.assertEqual(by_id[task]['published_outcome'],
                                         category if category != 'empty_patch' else 'unknown')
                self.assertEqual(by_id['dataset-only']['published_outcome'], 'unknown')
                for task, source in predictions.items():
                    record = by_id[task]
                    self.assertEqual(record['language'], PINNED_LAYOUTS[index][1])
                    self.assertEqual(record['patch'], source['model_patch'] or None)
                    self.assertEqual(record['provenance']['patch_sha256'],
                                     hashlib.sha256(source['model_patch'].encode()).hexdigest())
                    self.assertTrue(record['provenance']['patch_url'].startswith(root + '/preds.json#/'))
                    self.assertNotIn(record['provenance']['separate_patch_url'], cache.requested)

    def test_keyed_and_list_predictions_and_validation(self):
        for as_list in (False, True):
            cache, args, _, predictions, root = self.fixture(as_list=as_list)
            run = import_run(cache, **args)
            row = next(r for r in run['records'] if r['task_id'] in predictions)
            expected_pointer = '0' if as_list else row['task_id']
            self.assertEqual(row['provenance']['patch_url'], root + '/preds.json#/' + expected_pointer + '/model_patch')
        for payload in ([{'model_patch': ''}], [{'instance_id': 'x', 'model_patch': ''}] * 2,
                        {'x': {'instance_id': 'y', 'model_patch': ''}}, {'x': {'model_patch': None}}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                _predictions(json.dumps(payload).encode())

    def test_optional_actual_tianxicode_patch_path_agreement_and_mismatch(self):
        cache, args, _, predictions, root = self.fixture()
        task = next(iter(predictions))
        location = root + '/logs/rollouts/' + task + '/patch.diff'
        # Also fetched this actual pinned standalone patch; its bytes equal the prediction.
        cache.values[location] = predictions[task]['model_patch'].encode()
        run = import_run(cache, **args, verify_patch_files=True)
        row = next(r for r in run['records'] if r['task_id'] == task)
        self.assertEqual(row['provenance']['patch_agreement'], 'matched')
        self.assertEqual(row['provenance']['separate_patch_sha256'], row['provenance']['patch_sha256'])
        cache.values[location] += b'\n'
        with self.assertRaisesRegex(ValueError, 'prediction and patch.diff disagree'):
            import_run(cache, **args, verify_patch_files=True)

    def test_monolithic_review_binding_and_analysis_denominator(self):
        cache, args, result, _, _ = self.fixture()
        run = import_run(cache, **args, task_ids=[result['success_ids'][0]], model='model')
        self.review(run)
        with patch('parsimony.benchmark.measure', return_value={'mode': 'full_file'}) as measure:
            records = analyze_run(run, cache, agent='pilot')
        self.assertEqual(measure.call_count, 1)
        self.assertEqual(len(records), 3)
        self.assertTrue(all(r['benchmark_tasks'] == 3 and r['resolve_rate'] == 1 / 3 for r in records))
        self.assertTrue(all(r['provenance']['model'] == 'model' for r in records))
        failed = next(r for r in records if r['published_outcome'] == 'failure')
        self.assertEqual(failed['evaluation_result'], 'failed')
        self.assertEqual(failed['analysis_status'], 'not_selected')
        del run['reviewed_manifest']['prediction_sha256']
        with self.assertRaisesRegex(ValueError, 'bound provenance checksums'):
            analyze_run(run, cache, agent='pilot')

    def test_empty_category_and_prediction_conflict_fails_closed(self):
        cache, args, _, _, root = self.fixture(2)
        predictions = json.loads(cache.values[root + '/preds.json'])
        predictions['beeware__briefcase-2214']['model_patch'] = 'nonempty'
        cache.values[root + '/preds.json'] = json.dumps(predictions).encode()
        with self.assertRaisesRegex(ValueError, 'empty_patch category disagrees'):
            import_run(cache, **args)

    def test_prediction_only_dataset_task_remains_unknown_and_bad_ids_are_not_repaired(self):
        cache, args, _, predictions, root = self.fixture()
        payload = dict(predictions, **{'dataset-only': {'model_patch': 'ungraded patch'}})
        cache.values[root + '/preds.json'] = json.dumps(payload).encode()
        run = import_run(cache, **args)
        row = next(r for r in run['records'] if r['task_id'] == 'dataset-only')
        self.assertEqual(row['published_outcome'], 'unknown')
        self.assertFalse(row['submitted'])
        self.assertEqual(row['artifact_status'], 'present')
        payload['missing-dataset-id'] = payload.pop('dataset-only')
        cache.values[root + '/preds.json'] = json.dumps(payload).encode()
        with self.assertRaisesRegex(ValueError, 'absent from dataset'):
            import_run(cache, **args)

    def test_observed_ami_v2_without_submitted_or_unresolved_counts(self):
        # Actual AMI Go schema at the same pin: only these lists/counts present.
        result = dict(total_instances=2, completed_instances=2, resolved_instances=1,
                      completed_ids=['0xERR0R__blocky-2016', 'cadence-workflow__cadence-7182'],
                      resolved_ids=['0xERR0R__blocky-2016'], unresolved_ids=['cadence-workflow__cadence-7182'],
                      language='go', dataset='SWE-bench-Live/MultiLang', split='go', schema_version=2)
        categories = _result_categories(result)
        self.assertEqual(categories['failure'], {'cadence-workflow__cadence-7182'})
        result['resolved_instances'] = 99
        with self.assertRaisesRegex(ValueError, 'success count'):
            _result_categories(result)

    def test_v2_count_lists_completed_and_outcome_conflicts_fail_closed(self):
        for field, replacement in (('resolved_instances', True), ('unresolved_instances', 99),
                                   ('error_instances', 2), ('empty_patch_instances', 9),
                                   ('submitted_instances', 8), ('completed_instances', 3),
                                   ('completed_ids', []), ('total_instances', 1),
                                   ('resolved_ids', None), ('submitted_ids', None)):
            cache, args, result, _, root = self.fixture(2)
            result[field] = replacement
            cache.values[root + '/results.json'] = json.dumps(result).encode()
            with self.subTest(field=field), self.assertRaises(ValueError):
                import_run(cache, **args)
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
            _predictions(b'{"x":{"model_patch":""},"x":{"model_patch":""}}')

    def test_analysis_keeps_error_empty_incomplete_and_absent_outcomes_unknown(self):
        cache, args, result, _, root = self.fixture(2)
        # Add an incomplete category using the observed conventional schema,
        # reclassifying an existing fixture error only for this validation test.
        memberships = _result_categories(result)
        result = {key: len(ids) for key, ids in memberships.items()}
        result.update({key + '_ids': sorted(ids) for key, ids in memberships.items()})
        result.update(submitted=4, submitted_ids=[task for ids in memberships.values() for task in ids])
        result['incomplete_ids'], result['incomplete'] = result['error_ids'], result['error']
        result['error_ids'], result['error'] = [], 0
        cache.values[root + '/results.json'] = json.dumps(result).encode()
        run = import_run(cache, **args)
        self.review(run)
        with patch('parsimony.benchmark.measure', return_value={'mode': 'full_file'}) as measure:
            rows = analyze_run(run, cache, agent='pilot')
        self.assertEqual(measure.call_count, 1)
        self.assertTrue(all(r['benchmark_tasks'] == 5 for r in rows))
        incomplete = next(r for r in rows if r['published_outcome'] == 'incomplete')
        self.assertEqual(incomplete['evaluation_result'], 'unknown')
        self.assertIn('incomplete', incomplete['published_result_categories'])
        empty = next(r for r in rows if 'empty_patch' in r['published_result_categories'])
        self.assertEqual(empty['evaluation_result'], 'unknown')
        self.assertEqual(empty['analysis_status'], 'empty_patch')
        self.assertIsNone(empty['metrics'])
        source = next(r for r in run['records'] if r['published_outcome'] == 'success')
        source['patch'] += '\n'
        with self.assertRaisesRegex(ValueError, 'bound provenance checksums'):
            analyze_run(run, cache, agent='pilot')

    def test_unsupported_dataset_language_is_inventory_only_not_relabelled(self):
        cache, args, _, _, _ = self.fixture()
        tasks = [json.loads(line) for line in cache.values[DATA].decode().splitlines()]
        tasks[-1]['language'] = 'Java'
        cache.values[DATA] = '\n'.join(json.dumps(r) for r in tasks).encode()
        run = import_run(cache, **args)
        self.assertEqual(run['records'][-1]['language'], 'Java')
        self.review(run)
        with self.assertRaisesRegex(ValueError, 'unsupported language'):
            analyze_run(run, cache, agent='pilot', language='Java')
        with patch('parsimony.benchmark.measure', return_value={'mode': 'full_file'}):
            rows = analyze_run(run, cache, agent='pilot')
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r['benchmark_tasks'] == 2 for r in rows))

    def test_optional_unavailable_separate_patch_does_not_override_prediction(self):
        cache, args, _, predictions, root = self.fixture()
        task = next(iter(predictions))
        location = root + '/logs/rollouts/' + task + '/patch.diff'
        cache.values[location] = HTTPError(location, 403, 'unavailable', {}, None)
        run = import_run(cache, **args, verify_patch_files=True)
        row = next(r for r in run['records'] if r['task_id'] == task)
        self.assertEqual(row['artifact_status'], 'present')
        self.assertEqual(row['provenance']['patch_agreement'], 'separate_patch_unavailable')
        self.assertEqual(row['published_outcome'], 'success')

    def test_cli_inventory_and_optional_reviewed_records(self):
        cache, args, _, _, _ = self.fixture()
        run = import_run(cache, **args)
        self.review(run)
        with tempfile.TemporaryDirectory() as tmp:
            output, records, review = [str(Path(tmp) / name) for name in ('run.json', 'records.jsonl', 'review.json')]
            Path(review).write_text(json.dumps(run['reviewed_manifest']))
            argv = ['parsimony.live', '--submission-revision', REV, '--config-path', args['config_path'],
                    '--dataset', 'org/tasks', '--dataset-revision', HF_REV, '--dataset-file', 'tasks.jsonl',
                    '--output', output, '--agent', 'cli-agent', '--model', 'cli-model', '--language', 'python']
            with patch.object(sys, 'argv', argv), patch('parsimony.live.Cache', return_value=cache), patch('builtins.print'):
                main()
            self.assertEqual(json.loads(Path(output).read_text())['agent'], 'cli-agent')
            with patch.object(sys, 'argv', argv + ['--review-manifest', review, '--records-output', records]), \
                 patch('parsimony.live.Cache', return_value=cache), patch('builtins.print'), \
                 patch('parsimony.benchmark.measure', return_value={'mode': 'full_file'}):
                main()
            normalized = json.loads(Path(output).read_text())
            self.assertEqual(normalized['reviewed_manifest']['manifest_sha256'], hashlib.sha256(Path(review).read_bytes()).hexdigest())
            rows = [json.loads(line) for line in Path(records).read_text().splitlines()]
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(r['agent'] == 'cli-agent' and r['provenance']['model'] == 'cli-model' for r in rows))
            self.assertTrue(all(r['provenance']['dataset'] == run['dataset'] for r in rows))
            with patch.object(sys, 'argv', argv + ['--records-output', records]), \
                 patch('parsimony.live.Cache') as no_network, patch('sys.stderr'), \
                 self.assertRaises(SystemExit):
                main()
            no_network.assert_not_called()


    def test_blocked_patch_stays_in_full_population_without_metrics(self):
        fixture = LiveImporterTests()
        fixture.setUp()
        run = fixture.run_import()
        fixture.review(run)
        self.cache = fixture.cache
        failure = next(r for r in run['records'] if r['task_id'] == 'fail')
        run['reviewed_manifest']['blocked_preimages'] = {
            'fail': dict(status='unverified',
                         patch_sha256=hashlib.sha256(failure['patch'].encode()).hexdigest(),
                         error='old blob mismatch')}
        records = {r['task_id']: r for r in analyze_run(run, self.cache, agent='pilot')}
        self.assertEqual(records['fail']['analysis_status'], 'unverified_preimage')
        self.assertIsNone(records['fail']['metrics'])
        self.assertEqual(records['fail']['evaluation_result'], 'failed')
        self.assertEqual(records['fail']['benchmark_tasks'], 5)
        self.assertEqual(records['pass']['analysis_status'], 'ok')
        run['reviewed_manifest']['blocked_preimages']['fail']['patch_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'evidence does not match'):
            analyze_run(run, self.cache, agent='pilot')


if __name__ == '__main__':
    unittest.main()
