import csv
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from parsimony.artifacts import Cache
from parsimony.polybench import (
    COMMIT_URL, DATASET, DATASET_REVISION, LANGUAGE_COUNTS, RAW, RUNS,
    SUBMISSION_REVISION, TREE_URL, analyze_run, import_run, main,
)

ISWE = '20260422_iswe_agent'
MIGBOT = '20260623_migbot_claude-opus-4-8'
PASS = 'huggingface__transformers-12981'
FAIL = 'huggingface__transformers-13491'
MISSING = 'keras-team__keras-20002'
DIFF = 'diff --git a/pkg/a.py b/pkg/a.py\n--- a/pkg/a.py\n+++ b/pkg/a.py\n@@ -1 +1 @@\n-x = 1\n+y = 2\n'
HF_API = f'https://huggingface.co/api/datasets/{DATASET}/revision/{DATASET_REVISION}'
HF_CSV = f'https://huggingface.co/datasets/{DATASET}/resolve/{DATASET_REVISION}/test.csv'
BASE_URL = 'https://raw.githubusercontent.com/org/repo/' + 'c' * 40 + '/pkg/a.py'


def encoded(value):
    return json.dumps(value).encode()


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


class PolyBenchTests(unittest.TestCase):
    def fixture(self, run_name=ISWE):
        self.run_name = run_name
        self.prefix = f'evaluation/PBVerified/{run_name}'
        self.root = RAW + '/' + self.prefix
        tasks = []
        for lang, count in LANGUAGE_COUNTS.items():
            ids = [f'org__{lang}-{i}' for i in range(count)]
            if lang == 'python':
                ids[:3] = [PASS, FAIL, MISSING]
            tasks.extend(dict(instance_id=task_id, repo='org/repo', base_commit='c' * 40,
                              language=lang.title(), patch='DO NOT USE GOLD PATCH') for task_id in ids)
        self.tasks = tasks
        csv_text = io.StringIO()
        writer = csv.DictWriter(csv_text, fieldnames=tasks[0].keys())
        writer.writeheader()
        writer.writerows(tasks)
        self.predictions = [dict(instance_id=r['instance_id'], model_patch=DIFF,
                                 model_name_or_path=RUNS[run_name]['model'])
                            for r in tasks if run_name == MIGBOT or
                            (r['language'] == 'Python' and r['instance_id'] != MISSING)]
        pred_ids = {r['instance_id'] for r in self.predictions}
        # Actual source layout: logs/<instance_id>_result.json, not nested task
        # directories, keyed report.json, or a successes-only aggregate.
        result_ids = [r['instance_id'] for r in tasks]
        if run_name == ISWE:
            result_ids += [f'outside__full-harness-{i}' for i in range(2110 - len(tasks))]
        entries = [dict(path=self.prefix + '/all_preds.jsonl', type='blob')]
        values = {COMMIT_URL: encoded(dict(sha=SUBMISSION_REVISION, tree=dict(sha='d' * 40))),
                  HF_API: encoded(dict(sha=DATASET_REVISION)), HF_CSV: csv_text.getvalue().encode(),
                  self.root + '/README.md': b'113 Python tasks; full harness output is not the cohort',
                  self.root + '/metadata.yaml': b'name: iSWE-Agent\noss: false\n'}
        if run_name == MIGBOT:
            values[self.root + '/README.md'] = (b'70 Feature + 312 complementary; 29 relay retries; '
                                               b'five unconditional replacements; frozen-set re-evaluation')
            values[self.root + '/metadata.yaml'] = b'name: HMigBot\noss: false\n'
            values[self.root + '/temporal_history_isolation_audit.json'] = encoded({'cases': []})
        for task_id in result_ids:
            generated = task_id in pred_ids
            success = generated and task_id == PASS
            result = dict(instance_id=task_id, generation=generated, resolved=success,
                          patch_applied=generated, with_logs=generated, all_f2p_passed=success,
                          no_p2p_failed=generated, passed_tests=[], failed_tests=[])
            path = self.prefix + f'/logs/{task_id}_result.json'
            entries.append(dict(path=path, type='blob', sha='e' * 40))
            values[RAW + '/' + path] = encoded(result)
        values[TREE_URL] = encoded(dict(sha='d' * 40, truncated=False, tree=entries))
        self.cache = FixtureCache(values)
        self.save_predictions()
        return self.cache

    def save_predictions(self):
        self.cache.values[self.root + '/all_preds.jsonl'] = b'\n'.join(encoded(r) for r in self.predictions)

    def change_result(self, task_id, **changes):
        url = self.root + f'/logs/{task_id}_result.json'
        result = json.loads(self.cache.values[url])
        result.update(changes)
        self.cache.values[url] = encoded(result)

    def inventory(self, language='python'):
        return import_run(self.cache, run_name=self.run_name, language=language)

    def offline(self, directory, with_source=True):
        cache = Cache(directory)
        if with_source:
            (cache.cache_dir / hashlib.sha256(BASE_URL.encode()).hexdigest()).write_bytes(b'x = 1\n')
        return cache

    def test_iswe_full_layout_and_population_placeholder_distinction(self):
        self.fixture()
        run = self.inventory()
        by_id = {r['task_id']: r for r in run['records']}
        self.assertEqual(run['listed_result_count'], 2110)
        self.assertEqual(run['submitted_task_count'], 112)
        self.assertEqual(len(run['records']), 382)
        self.assertEqual(len(run['population_ids']), 113)
        self.assertIn(MISSING, run['population_ids'])
        self.assertEqual(len(run['non_submitted_results']), 1998)
        self.assertEqual(by_id[MISSING]['published_outcome'], 'unknown')
        self.assertFalse(by_id[MISSING]['submitted'])
        self.assertEqual(by_id[MISSING]['artifact_status'], 'missing')
        self.assertEqual(by_id[PASS]['published_outcome'], 'success')
        self.assertEqual(by_id[FAIL]['published_outcome'], 'failure')
        self.assertTrue(all(r['classification'] == 'non_submitted_placeholder'
                            for r in run['non_submitted_results']))
        self.assertEqual(run['historical_dataset_match'], 'unverified')
        self.assertEqual(run['rights_status'], 'unreviewed-do-not-publish')
        self.assertEqual(run['provenance_status'], 'declared-candidate')
        self.assertTrue(all(r['scope_status'] == 'unsupported_language' for r in run['records']
                            if r['language'] == 'java'))
        self.assertEqual(by_id[PASS]['provenance']['patch_sha256'], hashlib.sha256(DIFF.encode()).hexdigest())
        result_url = self.root + f'/logs/{PASS}_result.json'
        self.assertEqual(by_id[PASS]['provenance']['result_sha256'],
                         hashlib.sha256(self.cache.values[result_url]).hexdigest())
        self.assertEqual(run['dataset']['dataset_file_sha256'], hashlib.sha256(self.cache.values[HF_CSV]).hexdigest())
        self.assertEqual(run['documents']['metadata.yaml']['text'], 'name: iSWE-Agent\noss: false\n')
        self.assertEqual(len(self.cache.requested), len(set(self.cache.requested)))

    def test_migbot_all382_and_disclosed_selection_sources(self):
        self.fixture(MIGBOT)
        run = self.inventory('javascript')
        self.assertEqual(run['submitted_task_count'], 382)
        self.assertEqual(run['listed_result_count'], 382)
        self.assertEqual(len(run['population_ids']), 100)
        self.assertEqual(run['non_submitted_results'], [])
        self.assertTrue(all(r['reported_model'] == 'claude-opus-4-8' for r in run['records']))
        disclosure = run['declaration']['selection_disclosure']
        for text in ('29', 'five', 'frozen-set re-evaluation', 'No independent'):
            self.assertIn(text, disclosure)
        audit = run['documents']['temporal_history_isolation_audit.json']
        self.assertEqual(audit['source']['sha256'], hashlib.sha256(encoded({'cases': []})).hexdigest())

    def test_missing_result_unknown_not_failure_and_http404_distinct(self):
        self.fixture()
        tree = json.loads(self.cache.values[TREE_URL])
        tree['tree'] = [r for r in tree['tree'] if not r['path'].endswith(FAIL + '_result.json')]
        self.cache.values[TREE_URL] = encoded(tree)
        url = self.root + f'/logs/{PASS}_result.json'
        self.cache.values[url] = HTTPError(url, 404, 'missing', {}, None)
        run = self.inventory()
        rows = {r['task_id']: r for r in run['records']}
        self.assertEqual(rows[FAIL]['published_outcome'], 'unknown')
        self.assertEqual(rows[PASS]['published_outcome'], 'unknown')
        self.assertEqual(rows[FAIL]['artifact_status'], 'present')
        self.assertNotIn(self.root + f'/logs/{FAIL}_result.json', self.cache.requested)
        self.assertIn(PASS, run['unavailable_result_ids'])

    def test_non404_download_error_is_not_silently_missing(self):
        self.fixture()
        url = self.root + f'/logs/{FAIL}_result.json'
        self.cache.values[url] = HTTPError(url, 403, 'forbidden', {}, None)
        with self.assertRaises(HTTPError) as caught:
            self.inventory()
        caught.exception.close()

    def test_incomplete_task_population_and_unsafe_repo_fail_closed(self):
        for kind in ('incomplete', 'repo', 'base'):
            with self.subTest(kind=kind):
                self.fixture()
                rows = self.tasks[:-1] if kind == 'incomplete' else self.tasks
                if kind == 'repo':
                    rows[0]['repo'] = '../escape'
                elif kind == 'base':
                    rows[0]['base_commit'] = 'main'
                text = io.StringIO()
                writer = csv.DictWriter(text, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
                self.cache.values[HF_CSV] = text.getvalue().encode()
                with self.assertRaisesRegex(ValueError, 'complete|unsafe repository|full SHA'):
                    self.inventory()

    def test_offline_strict_analysis_pass_fail_missing_and_exact_base_hash(self):
        self.fixture()
        # An unrelated failed test is not grounds to contradict authoritative
        # resolved=true. The real exporter contains this kind of row.
        self.change_result(PASS, failed_tests=['unrelated-test'])
        run = self.inventory()
        with tempfile.TemporaryDirectory() as directory:
            cache = self.offline(directory)
            with patch.object(cache, 'get', side_effect=AssertionError('network cache called')):
                rows = {r['task_id']: r for r in analyze_run(run, cache)}
        self.assertEqual(len(rows), 113)
        self.assertEqual(rows[PASS]['analysis_status'], 'ok')
        self.assertEqual(rows[FAIL]['analysis_status'], 'ok')
        self.assertEqual(rows[PASS]['evaluation_result'], 'resolved')
        self.assertEqual(rows[FAIL]['evaluation_result'], 'failed')
        self.assertEqual(rows[FAIL]['harness_result_flags']['generation'], True)
        self.assertEqual(rows[FAIL]['provenance']['failure_semantics'], 'upstream-reported-not-attributed-to-patch')
        self.assertEqual(rows[MISSING]['evaluation_result'], 'unknown')
        self.assertEqual(rows[MISSING]['analysis_status'], 'missing_patch')
        self.assertIsNone(rows[MISSING]['metrics'])
        self.assertTrue(all(r['benchmark_tasks'] == 113 for r in rows.values()))
        source = rows[FAIL]['provenance']['base_sources'][0]
        self.assertEqual(source, dict(url=BASE_URL, sha256=hashlib.sha256(b'x = 1\n').hexdigest(), bytes=6))
        self.assertEqual(rows[PASS]['provenance']['historical_dataset_match'], 'unverified')
        self.assertEqual(rows[PASS]['provenance']['model_identity'], 'submitter-label-not-independent-attestation')
        self.assertEqual(rows[MISSING]['provenance']['base_sources'], [])

    def test_empty_no_generation_unknown_and_uncached_base_remain_unmeasured(self):
        self.fixture()
        self.predictions[0]['model_patch'] = ''
        self.save_predictions()
        self.change_result(PASS, generation=False, resolved=False, patch_applied=False,
                           with_logs=False, all_f2p_passed=False, no_p2p_failed=False)
        url = self.root + f'/logs/{FAIL}_result.json'
        self.cache.values[url] = HTTPError(url, 404, 'missing', {}, None)
        run = self.inventory()
        with tempfile.TemporaryDirectory() as directory:
            rows = {r['task_id']: r for r in analyze_run(run, self.offline(directory, False))}
        self.assertEqual(rows[PASS]['analysis_status'], 'empty_patch')
        self.assertEqual(rows[PASS]['published_outcome'], 'no_generation')
        self.assertEqual(rows[PASS]['evaluation_result'], 'no_generation')
        self.assertEqual(rows[FAIL]['published_outcome'], 'unknown')
        self.assertEqual(rows[FAIL]['analysis_status'], 'unknown_outcome')
        cached_missing = rows['org__python-3']
        self.assertEqual(cached_missing['analysis_status'], 'fetch_error')
        self.assertEqual(cached_missing['evaluation_result'], 'failed')
        self.assertIsNone(cached_missing['metrics'])
        self.assertEqual(cached_missing['provenance']['base_sources'],
                         [dict(url=BASE_URL, sha256=None, status='unavailable_offline')])

    def test_strict_application_error_does_not_relabel_upstream_failure(self):
        self.fixture()
        self.predictions[1]['model_patch'] = DIFF.replace('-x = 1', '-wrong = 1')
        self.save_predictions()
        run = self.inventory()
        with tempfile.TemporaryDirectory() as directory:
            rows = {r['task_id']: r for r in analyze_run(run, self.offline(directory))}
        self.assertEqual(rows[FAIL]['analysis_status'], 'error')
        self.assertEqual(rows[FAIL]['evaluation_result'], 'failed')
        self.assertIsNone(rows[FAIL]['metrics'])

    def test_unsafe_duplicate_prediction_dataset_and_tree_ids(self):
        for kind in ('unsafe', 'duplicate', 'dataset', 'tree'):
            with self.subTest(kind=kind):
                self.fixture()
                if kind == 'unsafe':
                    self.predictions[0]['instance_id'] = '../escape'
                    self.save_predictions()
                elif kind == 'duplicate':
                    self.predictions.append(self.predictions[0])
                    self.save_predictions()
                elif kind == 'dataset':
                    text = self.cache.values[HF_CSV].decode().splitlines()
                    text.append(text[1])
                    self.cache.values[HF_CSV] = '\n'.join(text).encode()
                else:
                    tree = json.loads(self.cache.values[TREE_URL])
                    tree['tree'].append(tree['tree'][1])
                    self.cache.values[TREE_URL] = encoded(tree)
                with self.assertRaisesRegex(ValueError, 'unsafe|duplicate'):
                    self.inventory()

    def test_outcome_mismatch_and_missing_prediction_generation_fail_closed(self):
        changes = [dict(instance_id='other'), dict(resolved='false'), dict(generation=False),
                   dict(resolved=True, all_f2p_passed=False), dict(resolved=True, patch_applied=False)]
        for change in changes:
            with self.subTest(change=change):
                self.fixture()
                self.change_result(FAIL, **change)
                with self.assertRaisesRegex(ValueError, 'mismatch|boolean|contradict'):
                    self.inventory()
        self.fixture()
        self.change_result(MISSING, generation=True)
        with self.assertRaisesRegex(ValueError, 'absent from predictions'):
            self.inventory()
        self.fixture()
        self.predictions[0]['base_commit'] = 'f' * 40
        self.save_predictions()
        with self.assertRaisesRegex(ValueError, 'base_commit mismatch'):
            self.inventory()
        self.fixture()
        self.predictions[0]['model_name_or_path'] = 'another-model'
        self.save_predictions()
        with self.assertRaisesRegex(ValueError, 'model label mismatch'):
            self.inventory()

    def test_bad_layout_duplicate_json_keys_and_revision_verification(self):
        for kind in ('layout', 'keys', 'commit', 'tree', 'truncated', 'hf'):
            with self.subTest(kind=kind):
                self.fixture()
                if kind == 'keys':
                    self.cache.values[self.root + f'/logs/{PASS}_result.json'] = (
                        b'{"instance_id":"' + PASS.encode() + b'","resolved":true,"resolved":false}')
                elif kind == 'commit':
                    self.cache.values[COMMIT_URL] = encoded(dict(sha='a' * 40, tree=dict(sha='d' * 40)))
                elif kind == 'hf':
                    self.cache.values[HF_API] = encoded(dict(sha='a' * 40))
                else:
                    tree = json.loads(self.cache.values[TREE_URL])
                    if kind == 'layout':
                        tree['tree'][1]['path'] = self.prefix + '/nested/x_result.json'
                    elif kind == 'tree':
                        tree['sha'] = 'a' * 40
                    else:
                        tree['truncated'] = True
                    self.cache.values[TREE_URL] = encoded(tree)
                with self.assertRaises(ValueError):
                    self.inventory()

    def test_analysis_unsupported_track_and_subsets_fail_without_source_access(self):
        self.fixture()
        run = self.inventory('java')
        with self.assertRaisesRegex(ValueError, 'unsupported analysis track'):
            analyze_run(run, None)
        run = self.inventory()
        with self.assertRaisesRegex(ValueError, 'match the inventoried'):
            analyze_run(run, None, language='javascript')
        run['records'] = [r for r in run['records'] if r['published_outcome'] == 'success']
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            analyze_run(run, None)
        with self.assertRaisesRegex(ValueError, 'unsupported run'):
            import_run(self.cache, run_name='other')
        with self.assertRaises(TypeError):
            import_run(self.cache, run_name=ISWE, task_ids=[PASS])

    def test_cli_inventory_fetch_and_offline_analysis(self):
        self.fixture()
        with tempfile.TemporaryDirectory() as directory:
            inventory_path = Path(directory) / 'inventory.json'
            output = Path(directory) / 'records.jsonl'
            args = ['polybench', '--cache', directory, 'inventory', '--run', ISWE,
                    '--language', 'python', '--output', str(inventory_path)]
            with patch('sys.argv', args), patch('parsimony.polybench.Cache', return_value=self.cache), patch('builtins.print'):
                main()
            self.assertEqual(json.loads(inventory_path.read_text())['listed_result_count'], 2110)
            cache = self.offline(directory)
            args = ['polybench', '--cache', directory, 'analyze', str(inventory_path), '--output', str(output)]
            with patch('sys.argv', args), patch('parsimony.polybench.Cache', return_value=cache), patch('builtins.print'):
                with patch.object(cache, 'get', side_effect=AssertionError('network')):
                    main()
            self.assertEqual(len(output.read_text().splitlines()), 113)


if __name__ == '__main__':
    unittest.main()
