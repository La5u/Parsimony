import csv
import difflib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from parsimony.benchmark import FetchError
from parsimony.release import audit, freeze_dataset
from parsimony.scoring import freeze_population, score_records
from parsimony.site import build
from parsimony.stability import analyze
from parsimony.sweeper import (TASK_REVISION, TRACE_REVISION, analyze_runs, build_dataset,
                              main, sha256)

HAS_PHP = all(importlib.util.find_spec(name) for name in ('tree_sitter', 'tree_sitter_php'))
BASE = '<?php\nfunction total($items) { return 0; }\n'
AFTER = '<?php\nfunction total($items) { return array_sum($items); }\n'
PATCH = ''.join(difflib.unified_diff(BASE.splitlines(keepends=True), AFTER.splitlines(keepends=True),
                                    fromfile='a/src/calc.php', tofile='b/src/calc.php')).encode()


class FakeCache:
    def __init__(self):
        self.urls = []

    def get(self, url):
        self.urls.append(url)
        if url != f'https://raw.githubusercontent.com/owner/repo/{"a" * 40}/src/calc.php':
            raise AssertionError(f'unexpected source URL: {url}')
        return BASE.encode()


class SweeperPopulationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.tasks = self.root / 'tasks.jsonl'
        self.refs = self.root / 'refs'
        self.refs.mkdir()
        tasks = [dict(case_id=f'case-{i}', repo='https://github.com/owner/repo',
                      base_commit='a' * 40, reference_commit='b' * 40, pr=i) for i in (1, 2, 3)]
        self.tasks.write_text(''.join(json.dumps(row) + '\n' for row in tasks))
        for task, paths in zip(tasks, [('src/calc.php', 'tests/CalcTest.php'),
                                      ('templates/page.phtml',), ('tests/calc.php', 'src/calc.js')]):
            (self.refs / f'{task["case_id"]}.json').write_text(json.dumps(dict(files=[
                dict(filename=path, status='modified', additions=1, deletions=1) for path in paths])))
        self.population = self.root / 'population.jsonl'
        self.rows = build_dataset(self.tasks, self.refs, expected_sha256=sha256(self.tasks.read_bytes()))
        self.population.write_text(''.join(json.dumps(row) + '\n' for row in self.rows))

    def test_reference_only_population_and_provenance(self):
        self.assertEqual([r['instance_id'] for r in self.rows], ['case-1', 'case-2'])
        for row in self.rows:
            self.assertEqual(row['repo'], 'owner/repo')
            self.assertEqual(row['language'], 'php')
            self.assertEqual(row['provenance']['dataset_revision'], TASK_REVISION)
            self.assertEqual(row['provenance']['dataset_file_sha256'], sha256(self.tasks.read_bytes()))
            self.assertEqual(row['provenance']['reference_files_sha256'],
                             sha256((self.refs / f'{row["instance_id"]}.json').read_bytes()))
        self.assertEqual(self.rows[0]['task_url'], 'https://github.com/owner/repo/pull/1')
        with self.assertRaisesRegex(ValueError, 'task dataset SHA256 mismatch'):
            build_dataset(self.tasks, self.refs)

    def test_task_without_pr_keeps_reference_commit_link(self):
        tasks = [json.loads(line) for line in self.tasks.read_text().splitlines()]
        tasks[0]['pr'] = None
        self.tasks.write_text(''.join(json.dumps(row) + '\n' for row in tasks))
        rows = build_dataset(self.tasks, self.refs, expected_sha256=sha256(self.tasks.read_bytes()))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['task_url'], f'https://github.com/owner/repo/commit/{"b" * 40}')


@unittest.skipUnless(HAS_PHP, 'install tree-sitter + tree-sitter-php for SWEeper measurements')
class SweeperAnalysisTests(SweeperPopulationTests):
    def setUp(self):
        super().setUp()
        self.patches = self.root / 'patches'
        self.patches.mkdir()
        self.runs = self.root / 'runs.csv'
        self.run_rows = [dict(run_id=f'run-{i}', task_id=f'case-{i}', repo='https://github.com/owner/repo',
                              base_commit='a' * 40, model='gpt-6-astra', harness='codex', effort='xhigh',
                              type='main', overall=outcome, patch_sha256=sha256(PATCH),
                              hf_url=f'https://example.org/run-{i}', dataset_revision='c' * 40,
                              prediction_status='completed', evaluation_status='completed',
                              target=outcome, preservation='pass')
                         for i, outcome in ((1, 'pass'), (2, 'fail'))]
        for row in self.run_rows:
            (self.patches / f'{row["run_id"]}.patch').write_bytes(PATCH)
        self.cache = FakeCache()
        self.save_runs()

    def save_runs(self):
        with self.runs.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(self.run_rows[0]))
            writer.writeheader()
            writer.writerows(self.run_rows)

    def records(self):
        return analyze_runs(self.runs, self.population, self.patches, self.cache,
                            model='gpt-6-astra', harness='codex')

    def test_outcomes_scope_and_hash_provenance(self):
        rows = self.records()
        self.assertEqual([r['evaluation_result'] for r in rows], ['resolved', 'failed'])
        for row in rows:
            self.assertEqual(row['analysis_status'], 'ok')
            self.assertGreater(row['metrics']['net_units'], 0)
            self.assertEqual(row['benchmark_tasks'], 2)
            self.assertEqual(row['resolve_rate'], .5)
            self.assertEqual(row['measurement_track']['language'], 'php')
            self.assertEqual(row['provenance']['patch_sha256'], sha256(PATCH))
            self.assertTrue(row['provenance']['patch_verified'])
            self.assertEqual(row['provenance']['trace_revision'], TRACE_REVISION)
            self.assertEqual(row['provenance']['result_sha256'], sha256(self.runs.read_bytes()))
            self.assertIn(TRACE_REVISION, row['provenance']['patch_location'])
            self.assertEqual(row['provenance']['source_run']['dataset_revision'], 'c' * 40)

    def test_unknown_verdicts_still_measure_available_patches(self):
        for outcome in ('uncertain', 'infrastructure_failed', '', 'missing'):
            with self.subTest(outcome=outcome):
                self.run_rows[1]['overall'] = outcome
                self.save_runs()
                row = self.records()[1]
                self.assertEqual(row['evaluation_result'], 'unknown')
                self.assertFalse(row['resolved'])
                self.assertEqual(row['published_result_categories'], [])
                self.assertEqual(row['analysis_status'], 'ok')
                self.assertGreater(row['metrics']['net_units'], 0)

    def test_missing_patch_and_missing_run_are_retained(self):
        (self.patches / 'run-1.patch').unlink()
        rows = self.records()
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0]['resolved'])
        self.assertEqual(rows[0]['analysis_status'], 'missing_patch')
        self.assertIsNone(rows[0]['metrics'])
        self.assertFalse(rows[0]['provenance']['patch_verified'])
        self.run_rows.pop()
        self.save_runs()
        row = self.records()[1]
        self.assertEqual(row['evaluation_result'], 'unknown')
        self.assertEqual(row['analysis_status'], 'missing_patch')
        self.assertIsNone(row['metrics'])
        self.assertIsNone(row['provenance']['patch_sha256'])
        self.assertFalse(row['submitted'])

    def test_hash_mismatch_rejected_before_source_fetch(self):
        (self.patches / 'run-2.patch').write_bytes(PATCH + b'bad')
        with self.assertRaisesRegex(ValueError, 'patch SHA256 mismatch'):
            self.records()
        self.assertEqual(self.cache.urls, [])

    def test_ablation_ignored_duplicates_and_base_mismatch_rejected(self):
        self.run_rows.append(dict(self.run_rows[0], type='ablation-harness'))
        self.save_runs()
        self.assertEqual(len(self.records()), 2)
        self.run_rows[-1]['type'] = 'main'
        self.save_runs()
        with self.assertRaisesRegex(ValueError, 'duplicate main attempt'):
            self.records()
        self.run_rows.pop()
        self.run_rows[1]['base_commit'] = 'd' * 40
        self.save_runs()
        with self.assertRaisesRegex(ValueError, 'base metadata differs'):
            self.records()

    def test_efforts_are_never_pooled(self):
        self.run_rows[1]['effort'] = 'max'
        self.save_runs()
        with self.assertRaisesRegex(ValueError, 'multiple efforts'):
            self.records()

    def test_empty_and_fetch_error_are_not_zero(self):
        (self.patches / 'run-2.patch').write_bytes(b'')
        self.run_rows[1]['patch_sha256'] = sha256(b'')
        self.save_runs()
        with patch.object(self.cache, 'get', side_effect=FetchError('offline')):
            rows = self.records()
        self.assertEqual([r['analysis_status'] for r in rows], ['fetch_error', 'empty_patch'])
        self.assertTrue(all(r['metrics'] is None for r in rows))

    def test_undecodable_patch_is_an_error_not_a_crash(self):
        raw = PATCH.replace(b'array_sum', b'array_sum /* \xa9 */')
        (self.patches / 'run-2.patch').write_bytes(raw)
        self.run_rows[1]['patch_sha256'] = sha256(raw)
        self.save_runs()
        rows = self.records()
        self.assertEqual([r['analysis_status'] for r in rows], ['ok', 'error'])
        self.assertIn('UnicodeDecodeError', rows[1]['analysis_error'])
        self.assertIsNone(rows[1]['metrics'])

    def test_release_panel_stability_and_site_compatibility(self):
        rows = self.records()
        # Tests bind the current source hash and leave an uncommitted analyzer
        # commit null, exactly as records do; no fake clean identity.
        population = freeze_dataset(self.population, 'test', analyzer_commit='a' * 40)
        population['analyzer_commit'] = rows[0]['analyzer_commit']
        self.assertEqual(audit(population, rows, self.population)['task_count'], 2)
        panel = freeze_population(rows, 'test-panel', population)
        self.assertEqual(set(panel['tasks']), {'case-1', 'case-2'})
        self.assertEqual(len(score_records(panel, rows)), 1)
        self.assertEqual(analyze(panel, rows, draws=10)['task_count'], 2)
        data = build(panel, rows, draws=10)
        self.assertEqual(data['population_count'], 2)
        self.assertEqual(data['task_urls']['case-1'], 'https://github.com/owner/repo/pull/1')
        self.assertEqual(data['models'][0]['measured_attempts'], 2)
        self.assertEqual(data['models'][0]['measured_solved_attempts'], 1)

    def test_cli_cache_before_subcommand(self):
        output = self.root / 'results.jsonl'
        args = ['sweeper', '--cache', str(self.root / 'cache'), 'analyze', str(self.runs),
                '--dataset', str(self.population), '--patches', str(self.patches),
                '--model', 'gpt-6-astra', '--harness', 'codex', '--output', str(output)]
        with patch('sys.argv', args), patch('parsimony.sweeper.Cache', return_value=self.cache) as cache, \
                patch('builtins.print'):
            main()
        cache.assert_called_once_with(str(self.root / 'cache'), timeout=90)
        self.assertEqual(len(output.read_text().splitlines()), 2)


if __name__ == '__main__':
    unittest.main()
