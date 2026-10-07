"""Synthetic tests only: submitted Python is parsed, never executed."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from parsimony.analysis import END_BLOCK, unit_lines, without_docstrings, unit_labels

SCRIPT = Path(__file__).resolve().parents[1] / 'examples/benchmark-discovery/measure-livecodebench.py'
spec = importlib.util.spec_from_file_location('livecodebench_pilot', SCRIPT)
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


def record(qid='a', codes=None, grades=None):
    return dict(question_id=qid, code_list=['x = 1'] if codes is None else codes,
                graded_list=[True] if grades is None else grades,
                output_list=['not Python; do not use this'])


def manifest_for(source, ids, models=('Model',)):
    return dict(revision='a' * 40, population_size=len(ids), task_ids=ids,
                membership_sha256=pilot.membership_hash(ids),
                source_bindings=[dict(model=model, filename='Scenario.codegeneration_1_0.2_eval_all.json',
                                      sha256=pilot.digest(source.read_bytes()),
                                      export_population_size=len(json.loads(source.read_bytes())),
                                      export_membership_sha256=pilot.membership_hash(
                                          r['question_id'] for r in json.loads(source.read_bytes())))
                                 for model in models])


class PilotTests(unittest.TestCase):
    def test_count_and_failure_retention(self):
        source = 'x = 1\nprint(x)'
        rows = pilot.measure([record(codes=[source], grades=[False])])
        expected = sum(len(run) for run in unit_lines(without_docstrings(ast.parse(source))))
        self.assertEqual(rows[0]['units_added'], expected)
        self.assertEqual(rows[0]['units_deleted'], 0)
        self.assertEqual(rows[0]['net_units'], expected)
        self.assertFalse(rows[0]['upstream_solved'])
        summary = pilot.summarize(rows)
        self.assertEqual(summary['mean_measured_all_outcomes'], expected)
        self.assertIsNone(summary['mean_measured_solved_only'])

    def test_docstrings_excluded_and_block_markers_included(self):
        source = '"""module docs"""\ndef f():\n    """function docs"""\n    if True:\n        return 1\n'
        stripped = without_docstrings(ast.parse(source))
        runs = unit_lines(stripped)
        self.assertEqual(sum(unit is END_BLOCK for run in runs for unit in run), 2)
        expected = sum(len(run) for run in runs)
        self.assertEqual(expected, sum(len(unit_labels(n)) for n in ast.walk(stripped)) + 2)
        self.assertEqual(pilot.measure([record(codes=[source])])[0]['net_units'], expected)
        plain = 'def f():\n    if True:\n        return 1\n'
        self.assertEqual(pilot.measure([record(codes=[plain])])[0]['net_units'], expected)

    def test_missing_and_invalid_are_not_zero(self):
        rows = pilot.measure([record('a', ['  '], [False]), record('b', ['def !'], [True])])
        self.assertEqual([r['status'] for r in rows], ['missing_code', 'parse_error'])
        self.assertTrue(all(r['net_units'] is None for r in rows))
        summary = pilot.summarize(rows)
        self.assertEqual(summary['full_population'], 2)
        self.assertEqual(summary['upstream_solved'], 1)
        self.assertIsNone(summary['mean_measured_all_outcomes'])

    def test_sample_zero_not_best_of(self):
        row = pilot.measure([record(codes=['x=1', 'x=1\ny=2'], grades=[False, True])])[0]
        self.assertFalse(row['upstream_solved'])
        self.assertEqual(row['attempt_index'], 0)
        self.assertEqual(row['code_sha256'], hashlib.sha256(b'x=1').hexdigest())

    def test_strict_validation_and_input_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'export.json'
            valid = [record()]
            raw = json.dumps(valid).encode()
            path.write_bytes(raw)
            _, sha = pilot.load_export(path, 1)
            self.assertEqual(sha, hashlib.sha256(raw).hexdigest())
            for bad in ([record(), record()], [record(grades=[1])],
                        [record(grades=['true'])], [record(grades=[])],
                        [record(codes=[None])], [record(codes='x')]):
                with self.subTest(bad=bad):
                    path.write_text(json.dumps(bad))
                    with self.assertRaises(ValueError):
                        pilot.load_export(path, 1)

    def test_output_hash_bindings_and_privacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'input', Path(tmp) / 'output'
            source.write_text(json.dumps([record('b'), record('a', ['secret_name=7'], [False])]))
            manifest = manifest_for(source, ['a', 'b'])
            with patch.object(pilot, 'analyzer_identity', return_value={'script_sha256': pilot.digest(SCRIPT.read_bytes())}), \
                    patch.object(pilot, 'load_manifest', return_value=(manifest, 'manifest hash')):
                pilot.main(['--export', f'Model=Scenario.codegeneration_1_0.2_eval_all.json={source}',
                            '--output-dir', str(output), '--source-revision', 'a' * 40])
            meta = json.loads((output / 'Model.metadata.json').read_text())
            rows = (output / 'Model.rows.jsonl').read_bytes()
            self.assertEqual(meta['population_manifest_sha256'], 'manifest hash')
            self.assertEqual(meta['rows_sha256'], pilot.digest(rows))
            self.assertEqual(meta['input_artifact_sha256'], pilot.digest(source.read_bytes()))
            self.assertEqual(meta['full_task_membership_sha256'], pilot.membership_hash(['a', 'b']))
            self.assertEqual(pilot.membership_hash(['b', 'a']), pilot.membership_hash(['a', 'b']))
            self.assertNotEqual(pilot.membership_hash(['a']), pilot.membership_hash(['a', 'b']))
            self.assertNotIn(b'secret_name', rows)
            self.assertEqual(meta['publication_status'], 'NONPUBLISHED')
            self.assertEqual(meta['source_revision'], 'a' * 40)
            self.assertEqual(meta['source_url'], 'https://raw.githubusercontent.com/LiveCodeBench/submissions/'
                             + 'a' * 40 + '/Model/Scenario.codegeneration_1_0.2_eval_all.json')
            self.assertEqual(meta['track'], 'standalone complete-file Python footprint')

    def test_revision_and_population_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'output'
            for revision in ('main', 'a' * 39, 'g' * 40):
                with self.subTest(revision=revision), self.assertRaises(SystemExit):
                    pilot.main(['--export', 'unused', '--output-dir', str(output),
                                '--source-revision', revision])
            a, b = Path(tmp) / 'a', Path(tmp) / 'b'
            a.write_text(json.dumps([record('a')]))
            b.write_text(json.dumps([record('b')]))
            with patch.object(pilot, 'analyzer_identity', return_value={}), \
                    patch.object(pilot, 'load_manifest', return_value=(manifest_for(a, ['a'], ('A', 'B')), 'hash')), \
                    self.assertRaises(SystemExit):
                pilot.main(['--export', f'A=Scenario.codegeneration_1_0.2_eval_all.json={a}',
                            '--export', f'B=Scenario.codegeneration_1_0.2_eval_all.json={b}',
                            '--output-dir', str(output), '--source-revision', 'a' * 40])
            self.assertFalse(output.exists())

    def test_frozen_manifest_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input'
            source.write_text(json.dumps([record()]))
            valid = manifest_for(source, ['a'])
            for kind in ('artifact', 'subset', 'membership', 'foreign', 'revision', 'binding'):
                manifest = json.loads(json.dumps(valid))
                if kind == 'artifact':
                    manifest['source_bindings'][0]['sha256'] = '0' * 64
                elif kind == 'subset':
                    manifest['source_bindings'][0].update(
                        export_population_size=2,
                        export_membership_sha256=pilot.membership_hash(['a', 'b']))
                elif kind == 'membership':
                    manifest['source_bindings'][0]['export_membership_sha256'] = '0' * 64
                elif kind == 'foreign':
                    manifest.update(task_ids=['b'], membership_sha256=pilot.membership_hash(['b']))
                elif kind == 'revision':
                    manifest['revision'] = 'b' * 40
                else:
                    manifest['source_bindings'] = []
                output = Path(tmp) / kind
                with self.subTest(kind=kind), patch.object(pilot, 'analyzer_identity', return_value={}), \
                        patch.object(pilot, 'load_manifest', return_value=(manifest, 'hash')), \
                        patch.object(pilot, 'measure') as measure, self.assertRaises(SystemExit):
                    pilot.main(['--export', f'Model=Scenario.codegeneration_1_0.2_eval_all.json={source}',
                                '--output-dir', str(output), '--source-revision', 'a' * 40])
                measure.assert_not_called()
                self.assertFalse(output.exists())

    def test_manifest_validation_and_surrogate(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input'
            source.write_text(json.dumps([record(codes=['\ud800'])]))
            with self.assertRaisesRegex(ValueError, 'invalid Unicode code'):
                pilot.load_export(source, 1)
            manifest = manifest_for(source, ['a'])
            path = Path(tmp) / 'manifest'
            path.write_text(json.dumps(manifest))
            with patch.object(pilot, 'POPULATION_MANIFEST', path):
                self.assertEqual(pilot.load_manifest()[1], pilot.digest(path.read_bytes()))
                for key, value in (('population_size', 2), ('membership_sha256', 'bad'),
                                   ('task_ids', ['a', 'a'])):
                    bad = dict(manifest, **{key: value})
                    path.write_text(json.dumps(bad))
                    with self.assertRaisesRegex(ValueError, 'invalid frozen'):
                        pilot.load_manifest()

    def test_manifest_must_be_tracked_and_equal_head(self):
        for response, message in ((pilot.subprocess.CalledProcessError(1, 'git'), 'git tracked'),
                                  (b'not manifest', 'byte-equal')):
            responses = ['', 'script', SCRIPT.read_bytes(), response]
            if isinstance(response, bytes):
                responses.insert(3, 'manifest')
            with self.subTest(message=message), patch.object(pilot.sys, 'version_info', (3, 14, 7)), \
                    patch.object(pilot.subprocess, 'check_output', side_effect=responses):
                with self.assertRaisesRegex(ValueError, 'population manifest.*' + message):
                    pilot.analyzer_identity()

    def test_script_must_be_tracked_and_equal_head(self):
        def git(*args, **kwargs):
            if 'status' in args[0]:
                return ''
            if 'ls-files' in args[0]:
                raise pilot.subprocess.CalledProcessError(1, args[0])
            return b'not script'
        with patch.object(pilot.sys, 'version_info', (3, 14, 7)), patch.object(pilot.subprocess, 'check_output', side_effect=git):
            with self.assertRaisesRegex(ValueError, 'git tracked'):
                pilot.analyzer_identity()
        with patch.object(pilot.sys, 'version_info', (3, 14, 7)), patch.object(pilot.subprocess, 'check_output', side_effect=['', 'script', b'not script']):
            with self.assertRaisesRegex(ValueError, 'byte-equal'):
                pilot.analyzer_identity()

    def test_partial_export_and_space_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'input', Path(tmp) / 'output'
            source.write_text(json.dumps([record('a', [], [True])]))
            model = 'Model (High)'
            manifest = manifest_for(source, ['a', 'b'], (model,))
            with patch.object(pilot, 'analyzer_identity', return_value={}), \
                    patch.object(pilot, 'load_manifest', return_value=(manifest, 'hash')):
                pilot.main(['--export', f'{model}=Scenario.codegeneration_1_0.2_eval_all.json={source}',
                            '--output-dir', str(output), '--source-revision', 'a' * 40])
            rows = [json.loads(line) for line in (output / f'{model}.rows.jsonl').read_text().splitlines()]
            self.assertEqual([r['status'] for r in rows], ['missing_code_list', 'missing_task'])
            self.assertEqual([r['upstream_solved'] for r in rows], [True, None])
            self.assertTrue(all(r['code_sha256'] is None and r['net_units'] is None for r in rows))
            meta = json.loads((output / f'{model}.metadata.json').read_text())
            self.assertIn('/Model%20%28High%29/', meta['source_url'])
            summary = meta['summary']
            self.assertEqual(summary['source_export_population'], 1)
            self.assertEqual(summary['known_outcome_population'], 1)
            self.assertEqual(summary['unknown_outcome_population'], 1)
            self.assertEqual(summary['upstream_solved'], 1)
            self.assertEqual(summary['source_reported_solved_fraction_interval'], [0.5, 1.0])
            self.assertTrue(summary['source_partial_population'])
            self.assertIsNone(summary['mean_measured_all_outcomes'])

    def test_empty_code_list_requires_complete_boolean_grades(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input'
            for samples in (1, 10):
                source.write_text(json.dumps([record(codes=[], grades=[False] * samples)]))
                records, _ = pilot.load_export(source, samples)
                self.assertFalse(pilot.measure(records)[0]['upstream_solved'])
                for grades in ([], [False] * (samples - 1), [1] * samples):
                    source.write_text(json.dumps([record(codes=[], grades=grades)]))
                    with self.assertRaises(ValueError):
                        pilot.load_export(source, samples)
            source.write_text(json.dumps([record(codes=['x=1'], grades=[True] * 10)]))
            with self.assertRaises(ValueError):
                pilot.load_export(source, 10)

    def test_old_six_complete_bindings_preserve_outcomes(self):
        rows = pilot.measure([record('a'), record('b', [' '], [False])], ['a', 'b'])
        summary = pilot.summarize(rows)
        self.assertEqual(summary['upstream_solved_fraction'], 0.5)
        self.assertEqual(summary['unknown_outcome_population'], 0)
        self.assertEqual(summary['source_reported_solved_fraction_interval'], [0.5, 0.5])
        self.assertFalse(summary['source_partial_population'])
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'input', Path(tmp) / 'output'
            source.write_text(json.dumps([record('a'), record('b', [' '], [False])]))
            models = tuple(f'Model{i}' for i in range(6))
            manifest = manifest_for(source, ['a', 'b'], models)
            args = []
            for model in models:
                args.extend(['--export', f'{model}=Scenario.codegeneration_1_0.2_eval_all.json={source}'])
            with patch.object(pilot, 'analyzer_identity', return_value={}), \
                    patch.object(pilot, 'load_manifest', return_value=(manifest, 'hash')):
                pilot.main(args + ['--output-dir', str(output), '--source-revision', 'a' * 40])
            self.assertEqual(list(json.loads((output / 'summary.json').read_text()).values()), [summary] * 6)

    def test_versioned_real_manifest_preserves_initial_snapshot(self):
        original = json.loads((SCRIPT.parents[1] / 'livecodebench-pilot/population.json').read_text())
        expanded, _ = pilot.load_manifest()
        self.assertEqual(expanded['task_ids'], original['task_ids'])
        self.assertEqual(expanded['population_size'], 1055)
        self.assertEqual(expanded['membership_sha256'], original['membership_sha256'])
        self.assertEqual(len(expanded['source_bindings']), 18)
        for old, new in zip(original['source_bindings'], expanded['source_bindings']):
            self.assertEqual({key: new[key] for key in old}, old)
            self.assertEqual(new['export_population_size'], 1055)
            self.assertEqual(new['export_membership_sha256'], original['membership_sha256'])
        self.assertEqual(sorted(binding['export_population_size'] for binding in expanded['source_bindings']),
                         [713] * 2 + [880] * 3 + [1055] * 13)
        self.assertEqual(sum(binding['missing_code_lists'] for binding in expanded['source_bindings']), 43)

    def test_cli_guards(self):
        with patch.object(pilot.sys, 'version_info', (3, 14, 6)):
            with self.assertRaisesRegex(ValueError, '3.14.7'):
                pilot.analyzer_identity()
        with patch.object(pilot.subprocess, 'check_output', return_value=' M parsimony/analysis.py'):
            with self.assertRaisesRegex(ValueError, 'dirty'):
                pilot.analyzer_identity()


if __name__ == '__main__':
    unittest.main()
