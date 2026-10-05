"""Offline contract tests for the two-phase pinned Gemini Verified driver."""
from collections import Counter
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from threading import Lock
import unittest
from unittest.mock import Mock, patch

from parsimony import benchmark

SPEC = importlib.util.spec_from_file_location(
    'gemini_verified', Path(__file__).resolve().parents[1] /
    'examples/benchmark-discovery/add-gemini-verified.py')
gemini = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gemini)


class MemoryCache:
    def __init__(self, values):
        self.values = values
        self.calls = []

    def get(self, url):
        self.calls.append(url)
        return self.values[url]  # An unknown URL fails, never falls back to HTTP.


class GeminiVerifiedTests(unittest.TestCase):
    def setUp(self):
        self.http = patch('parsimony.artifacts.urlopen', side_effect=AssertionError('HTTP forbidden'))
        self.http.start()
        self.addCleanup(self.http.stop)
        self.temp = tempfile.TemporaryDirectory(prefix='gemini-offline-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ids = [f'task-{n:03}' for n in range(500)]
        self.records = [dict(task_id=t, provenance=dict(repo='org/repo', base_commit='a' * 40,
                        reference_patch_sha256='do-not-copy'), human_metrics={'churn': 7})
                        for t in reversed(self.ids)]
        self.dataset = gemini.dataset_from_records(self.records)
        self.details = {t: {'resolved': n < 359} for n, t in enumerate(self.ids[:441])}
        self.aggregate = dict(resolved=self.ids[:359], no_generation=self.ids[441:])
        self.logs = f'https://raw.githubusercontent.com/org/artifacts/{gemini.ARTIFACT_REVISION}/logs'
        self.submission = dict(agent=gemini.NAME, submission_url=gemini.SUBMISSION_URL,
            predictions={t: f'patch {t}\n' for t in self.ids[:441]},
            resolved=set(self.ids[:359]), evaluated=set(self.ids[:441]), result_details={},
            provenance=dict(artifact_ref=gemini.ARTIFACT_REVISION,
                            metadata_ref=gemini.SUBMISSION_REVISION,
                            submission_url=gemini.SUBMISSION_URL,
                            failure_logs_url=self.logs, prediction_url=self.logs + '/all_preds.jsonl'))
        self.values = {f'{self.logs}/{t}/patch.diff': p.encode()
                       for t, p in self.submission['predictions'].items()}
        self.values[gemini.BASE + '/per_instance_details.json'] = gemini.encode(self.details)
        self.values[gemini.BASE + '/results/results.json'] = gemini.encode(self.aggregate)
        self.cache = MemoryCache(self.values)

    def bound_files(self):
        submission, evidence = gemini.build_inventory(self.submission,
            gemini.encode(self.details), gemini.encode(self.aggregate), self.dataset,
            self.cache, workers=2, metadata_sha='c' * 64)
        payloads = dict(zip(gemini.FILES, map(gemini.encode, (submission, self.dataset, evidence))))
        for name, raw in payloads.items():
            (self.root / name).write_bytes(raw)
        (self.root / 'manifest.json').write_bytes(gemini.encode(gemini.manifest_for(payloads, 'c' * 64)))
        return submission, evidence

    def rebind(self, name, mutate):
        value = json.loads((self.root / name).read_bytes())
        mutate(value)
        (self.root / name).write_bytes(gemini.encode(value))
        payloads = {f: (self.root / f).read_bytes() for f in gemini.FILES}
        (self.root / 'manifest.json').write_bytes(gemini.encode(gemini.manifest_for(payloads, 'c' * 64)))

    def test_inventory_full_population_and_every_separate_patch_hash(self):
        submission, evidence = self.bound_files()
        loaded, dataset = gemini.load_bound(self.root)
        self.assertEqual(loaded['evaluated'], set(self.ids))
        self.assertEqual(loaded['resolved'], set(self.ids[:359]))
        self.assertEqual(submission['result_details']['unresolved'], self.ids[359:441])
        self.assertEqual(submission['result_details']['no_generation'], self.ids[441:])
        self.assertEqual(len(self.cache.calls), 441)
        self.assertEqual(evidence['separate_patches_agree'], 441)
        self.assertEqual([p['task_id'] for p in evidence['patches']], self.ids[:441])
        for p in evidence['patches']:
            raw = self.values[p['url']]
            self.assertEqual((p['sha256'], p['bytes']), (gemini.sha(raw), len(raw)))
            self.assertIs(type(p['resolved']), bool)
        self.assertEqual([r['instance_id'] for r in dataset], self.ids)
        self.assertTrue(all(set(r) == {'instance_id', 'repo', 'base_commit'} for r in dataset))
        self.assertNotIn('do-not-copy', gemini.encode(dataset).decode())

    def test_inventory_phase_uses_current_importer_without_failure_report_inference(self):
        source = self.root / 'source'
        metadata = source / gemini.METADATA_SOURCE
        metadata.parent.mkdir(parents=True)
        metadata.write_bytes(b''.join(gemini.encode(r).replace(b'\n', b'') + b'\n' for r in self.records))
        output = self.root / 'out'
        output.mkdir()
        with patch.object(gemini, 'REPO', source), \
                patch('parsimony.artifacts.Cache', return_value=self.cache), \
                patch('parsimony.artifacts.load_submission', return_value=self.submission) as importer:
            gemini.inventory(output, workers=2)
            importer.assert_called_once_with(gemini.SUBMISSION_URL, self.cache,
                                             task_ids=[], include_failed=True)
        gemini.load_bound(output)
        with self.assertRaisesRegex(ValueError, 'already exist'):
            gemini.inventory(output, workers=2)

    def test_falsey_or_truthy_non_boolean_details_rejected(self):
        for invalid in (0, 1, None, '', 'false', [], {}):
            with self.subTest(invalid=invalid):
                details = copy.deepcopy(self.details)
                details[self.ids[359]]['resolved'] = invalid
                with self.assertRaisesRegex(ValueError, 'exact boolean'):
                    gemini.outcomes(details, self.aggregate, set(self.ids))

    def test_outcome_conflicts_and_missing_population_rejected(self):
        variants = []
        aggregate = copy.deepcopy(self.aggregate)
        aggregate['resolved'][0] = self.ids[359]
        variants.append((self.details, aggregate))
        for ng in (self.ids[441:-1], self.ids[441:] + [self.ids[441]],
                   [self.ids[0]] + self.ids[442:], [123] + self.ids[442:],
                   ['outside-population'] + self.ids[442:]):
            variants.append((self.details, dict(self.aggregate, no_generation=ng)))
        variants.append((dict(list(self.details.items())[1:]), self.aggregate))
        variants.append((self.details, dict(self.aggregate, failed=self.ids[359:440])))
        variants.append((self.details, dict(self.aggregate, no_logs=[self.ids[359]])))
        for details, aggregate in variants:
            with self.subTest(aggregate=aggregate.keys()), self.assertRaises(ValueError):
                gemini.outcomes(details, aggregate, set(self.ids))

    def test_metadata_missing_duplicate_or_invalid_base_rejected(self):
        for records in (self.records[:-1], self.records[:-1] + [self.records[0]],
                        [dict(self.records[0], provenance={'repo': 'org/repo', 'base_commit': None})]
                        + self.records[1:]):
            with self.assertRaises(ValueError):
                gemini.dataset_from_records(records)

    def test_importer_outcome_prediction_or_pin_conflicts_rejected(self):
        for kind in ('resolved', 'predictions', 'pin', 'type'):
            submission = copy.deepcopy(self.submission)
            if kind == 'resolved':
                submission['resolved'].remove(self.ids[0])
            elif kind == 'predictions':
                del submission['predictions'][self.ids[0]]
            elif kind == 'pin':
                submission['provenance']['artifact_ref'] = 'main'
            else:
                submission['predictions'][self.ids[0]] = 0
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                gemini.build_inventory(submission, gemini.encode(self.details), gemini.encode(self.aggregate),
                                       self.dataset, self.cache, 2, 'c' * 64)

    def test_patch_difference_not_normalized(self):
        self.values[f'{self.logs}/{self.ids[0]}/patch.diff'] = b'patch task-000'
        with self.assertRaisesRegex(ValueError, 'separate patch differs'):
            self.bound_files()

    def test_manifest_rejects_modified_or_missing_bound_files(self):
        self.bound_files()
        for name in gemini.FILES:
            raw = (self.root / name).read_bytes()
            (self.root / name).write_bytes(raw + b' ')
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'binding'):
                gemini.load_bound(self.root)
            (self.root / name).write_bytes(raw)
        (self.root / 'dataset.json').unlink()
        with self.assertRaises(FileNotFoundError):
            gemini.load_bound(self.root)

    def test_manifest_identity_and_file_map_are_exact(self):
        self.bound_files()
        original = json.loads((self.root / 'manifest.json').read_bytes())
        for key in ('submission_revision', 'artifact_revision', 'required_analyzer_commit',
                    'required_python_version', 'dataset_metadata_source', 'files'):
            changed = dict(original, **{key: 'wrong'})
            (self.root / 'manifest.json').write_bytes(gemini.encode(changed))
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'binding'):
                gemini.load_bound(self.root)

    def test_semantic_binding_rejected_even_if_manifest_checksums_updated(self):
        mutations = [
            ('inventory.json', lambda s: s['evaluated'].pop()),
            ('inventory.json', lambda s: s['predictions'].pop(self.ids[0])),
            ('inventory.json', lambda s: s['result_details']['unresolved'].pop()),
            ('dataset.json', lambda d: d[0].update(patch='human reference')),
            ('evidence.json', lambda e: e['patches'][0].update(resolved=1)),
            ('evidence.json', lambda e: e['patches'][0].update(sha256='0' * 64)),
            ('evidence.json', lambda e: e['patches'][0].update(bytes=True)),
            ('evidence.json', lambda e: e.update(dataset_metadata_sha256='0' * 64)),
            ('evidence.json', lambda e: e.update(dataset_source_sha256='0' * 64)),
            ('evidence.json', lambda e: e['patches'].pop()),
        ]
        for name, mutate in mutations:
            self.bound_files()
            self.rebind(name, mutate)
            with self.subTest(name=name), self.assertRaises(ValueError):
                gemini.load_bound(self.root)

    def test_external_guard_rejects_source_paths_and_symlinks_before_writing(self):
        with self.assertRaisesRegex(ValueError, 'external'):
            gemini.external_root(gemini.REPO / 'examples/new-output')
        alias = self.root / 'alias'
        alias.symlink_to(gemini.REPO, target_is_directory=True)
        with self.assertRaises(ValueError):
            gemini.external_root(alias / 'new-output')
        output = self.root / 'out'
        output.mkdir()
        (output / 'inventory.json').symlink_to(gemini.REPO / 'pyproject.toml')
        with self.assertRaises(ValueError):
            gemini.external_root(output)
        (output / 'inventory.json').unlink()
        (output / 'cache').symlink_to(gemini.REPO, target_is_directory=True)
        with self.assertRaises(ValueError):
            gemini.external_root(output)
        (output / 'cache').unlink()
        (output / 'cache').mkdir()
        (output / 'cache/hash').symlink_to(gemini.REPO / 'pyproject.toml')
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            gemini.external_root(output)
        self.assertFalse((output / 'manifest.json').exists())

    def test_external_guard_accepts_external_but_rejects_other_git_checkout(self):
        self.assertEqual(gemini.external_root(self.root / 'new'), self.root / 'new')
        checkout = self.root / 'checkout'
        checkout.mkdir()
        subprocess.run(['git', 'init', '-q', str(checkout)], check=True)
        with self.assertRaisesRegex(ValueError, 'Git checkout'):
            gemini.external_root(checkout / 'out')
        with self.assertRaises(ValueError):
            gemini.external_root(self.root / 'new', checkout=self.root)

    def test_clean_required_analyzer_and_runtime_enforced(self):
        checkout = self.root / 'analyzer'
        for head, dirty in ((gemini.ANALYZER_COMMIT, ' M parsimony/analysis.py'), ('wrong', '')):
            with patch.object(gemini, 'git', side_effect=[str(checkout), head, dirty]), \
                    self.assertRaisesRegex(ValueError, 'clean at 0aa66df'):
                gemini.clean_checkout(checkout)
        with patch.object(gemini.platform, 'python_version', return_value='3.13.0'), \
                self.assertRaisesRegex(ValueError, 'Python 3.14.7'):
            gemini.measure_worker(self.root, checkout, workers=1)
        with patch.object(gemini.platform, 'python_version', return_value=gemini.PYTHON_VERSION), \
                patch.object(gemini, 'clean_checkout'), \
                self.assertRaisesRegex(ValueError, 'wrong checkout'):
            gemini.measure_worker(self.root, checkout, workers=1)

    def test_measure_whole_dataset_per_selection_sorted_records_and_no_human_comparison(self):
        self.bound_files()
        checkout = self.root / 'analyzer'
        identity = Mock(return_value=(gemini.ANALYZER_COMMIT, 'b' * 64))
        analyze = Mock(wraps=benchmark.analyze_submission)
        lock = Lock()
        def recorded_analysis(*args, **kwargs):
            # Mock.call_count increments are not thread-safe on every Python runtime.
            # Keep two worker threads, but serialize this cheap mocked analysis.
            with lock:
                return analyze(*args, **kwargs)
        with patch.object(gemini, 'clean_checkout'), \
                patch.object(gemini.platform, 'python_version', return_value=gemini.PYTHON_VERSION), \
                patch.object(benchmark, '__file__', str(checkout / 'parsimony/benchmark.py')), \
                patch.object(benchmark, 'analyzer_identity', identity), \
                patch.object(benchmark, 'measure', return_value={'churn': 0}), \
                patch.object(benchmark, 'analyze_submission', new=recorded_analysis):
            gemini.measure_worker(self.root, checkout, workers=2)
        records = [json.loads(line) for line in (self.root / 'measurements.jsonl').read_bytes().splitlines()]
        self.assertEqual([r['task_id'] for r in records], self.ids)
        self.assertEqual(Counter(r['evaluation_result'] for r in records),
                         {'resolved': 359, 'failed': 82, 'no_generation': 59})
        self.assertEqual(Counter(r['analysis_status'] for r in records), {'ok': 441, 'not_resolved': 59})
        self.assertTrue(all(r['benchmark_tasks'] == 500 and r['resolve_rate'] == 359 / 500 for r in records))
        self.assertTrue(all(r['human_metrics'] is None and r['model_human_ratio'] is None for r in records))
        self.assertEqual(analyze.call_count, 500)
        for call in analyze.call_args_list:
            self.assertEqual(len(call.kwargs['dataset']), 500)
            self.assertEqual(len(call.kwargs['task_ids']), 1)
            self.assertTrue(call.kwargs['include_failed'])

    def test_measure_launcher_binds_before_spawn_and_selects_clean_checkout_imports(self):
        checkout = self.root / 'analyzer'
        argv = ['driver', 'measure', '--external-dir', str(self.root), '--analyzer-checkout', str(checkout)]
        with patch('sys.argv', argv), patch.object(gemini, 'external_root', return_value=self.root), \
                patch.object(gemini, 'load_bound', side_effect=ValueError('binding mismatch')), \
                patch.object(gemini.subprocess, 'run') as launch, \
                self.assertRaises(SystemExit):
            gemini.main()
        launch.assert_not_called()
        with patch('sys.argv', argv), patch.object(gemini, 'external_root', return_value=self.root), \
                patch.object(gemini, 'load_bound'), patch.object(gemini, 'clean_checkout'), \
                patch.object(gemini.subprocess, 'run') as launch:
            gemini.main()
        call = launch.call_args
        self.assertEqual(call.kwargs['cwd'], checkout)
        self.assertEqual(call.kwargs['env']['PYTHONPATH'], str(checkout))
        self.assertEqual(call.kwargs['env']['PYTHONDONTWRITEBYTECODE'], '1')
        self.assertIn('--worker', call.args[0])


if __name__ == '__main__':
    unittest.main()
