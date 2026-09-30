import copy
import unittest

from parsimony.scoring import freeze, freeze_population, score_records, task_score
from parsimony.site import build
from parsimony.stability import analyze, bootstrap, drop_agent, group, matrix
from tests.test_scoring import record


class FullPopulationTests(unittest.TestCase):
    def setUp(self):
        self.records = [record('a', 'solved'), record('a', 'uncalibrated', resolved=False),
                        record('b', 'solved', resolved=False), record('b', 'uncalibrated', resolved=False)]
        for r in self.records:
            r.update(analyzer_commit='a' * 40, evaluation_result='resolved' if r['resolved'] else 'failed')
        self.population = dict(format='parsimony-beta-population-v1', task_count=2,
                               analyzer_commit='a' * 40, python_version='3.14',
                               tasks={t: dict(repo='org/repo', base_commit='abc')
                                      for t in ('solved', 'uncalibrated')})
        self.panel = freeze_population(self.records, 'full', self.population)

    def test_uncalibrated_task_keeps_denominator_and_never_becomes_zero(self):
        self.assertEqual(len(self.panel['tasks']), 2)
        self.assertEqual(self.panel['tasks']['uncalibrated'], [])
        results = {r['agent']: r for r in score_records(self.panel, self.records)}
        self.assertEqual(results['a']['task_count'], 2)
        self.assertIsNone(results['a']['score'])
        self.assertEqual((results['a']['lower'], results['a']['upper']), (12.75, 25.25))
        missing = results['a']['tasks']['uncalibrated']
        self.assertEqual((missing['status'], missing['score'], missing['lower'], missing['upper']),
                         ('uncalibrated', None, -25, 0))
        self.assertEqual((results['b']['lower'], results['b']['upper']), (-18.75, -6.25))

    def test_unknown_bounds_enclose_unchanged_formula_for_any_reference(self):
        for resolved in (False, True):
            candidate = record('candidate', net=5, churn=9, resolved=resolved)
            bounded = task_score(candidate, [])
            for size in (0, 1, 10, 1000000):
                exact = task_score(candidate, [record('ref', net=size, churn=size)])['score']
                self.assertLessEqual(bounded['lower'], exact)
                self.assertLessEqual(exact, bounded['upper'])

    def test_existing_calibrated_scores_are_identical(self):
        calibrated = [r for r in self.records if r['task_id'] == 'solved']
        population = dict(self.population, task_count=1, tasks={'solved': self.population['tasks']['solved']})
        strict = freeze(calibrated, 'strict')
        bounded = freeze_population(calibrated, 'bounded', population)
        a = score_records(strict, calibrated)
        b = score_records(bounded, calibrated)
        for left, right in zip(a, b):
            self.assertEqual(left['tasks'], right['tasks'])
            self.assertEqual(left['score'], right['score'])

    def test_missing_candidate_and_out_of_scope_do_not_gain_zero(self):
        hidden = copy.deepcopy(self.records)
        hidden[0]['metrics'].update(touched_files=['test.py'], excluded_files=['test.py'])
        result = score_records(self.panel, hidden)[0]
        self.assertIsNone(result['score'])
        missing = score_records(self.panel, [self.records[0]])[0]['tasks']['uncalibrated']
        self.assertEqual((missing['lower'], missing['upper']), (-25, 100))

    def test_stability_preserves_population_when_reference_removed(self):
        dropped, _ = drop_agent(self.panel, 'a')
        self.assertEqual(set(dropped['tasks']), set(self.panel['tasks']))
        values = matrix(dropped, group(self.records), 0.8, 25)
        self.assertEqual(values['a']['solved'], (None, 1, 100))
        self.assertEqual(values['b']['solved'], (None, -25, 0))
        self.assertEqual(matrix(self.panel, group(self.records), 0.8, 50)['a']['uncalibrated'], (None, -50, 0))

    def test_rank_ranges_include_missing_data_not_just_midpoint_order(self):
        values = {'a': {'task': (None, 0, 10)}, 'b': {'task': (None, 4, 12)},
                  'c': {'task': (-20, -20, -20)}}
        result = bootstrap(values, ['task'], draws=20, bound_ranks=True)
        self.assertEqual(result['models']['a']['rank_ci_95'], [1, 2])
        self.assertEqual(result['models']['b']['rank_ci_95'], [1, 2])
        self.assertEqual(result['models']['c']['rank_ci_95'], [3, 3])
        complete = analyze(self.panel, self.records, draws=20)
        self.assertEqual(complete['task_count'], 2)
        self.assertEqual(complete['repositories'], {'org/repo': 2})
        self.assertIn('rank_policy', complete['bootstrap'])

    def test_legacy_empty_reference_panels_still_rejected(self):
        legacy = copy.deepcopy(self.panel)
        del legacy['calibration_policy']
        with self.assertRaisesRegex(ValueError, 'empty reference'):
            score_records(legacy, self.records)

    def test_frozen_population_base_and_analyzer_enforced(self):
        for key, value in [('repo', 'other/repo'), ('base_commit', 'other')]:
            bad = copy.deepcopy(self.records)
            bad[0]['provenance'][key] = value
            with self.assertRaisesRegex(ValueError, 'base'):
                freeze_population(bad, 'bad', self.population)
            with self.assertRaisesRegex(ValueError, 'base'):
                score_records(self.panel, bad)
        bad = copy.deepcopy(self.records)
        bad[0]['analyzer_commit'] = 'b' * 40
        with self.assertRaisesRegex(ValueError, 'analyzer commit'):
            score_records(self.panel, bad)

    def test_site_includes_uncalibrated_failed_footprint_and_outcome(self):
        data = build(self.panel, self.records, draws=20)
        self.assertEqual(data['task_count'], 2)
        self.assertEqual(data['excluded_tasks'], [])
        self.assertEqual(data['uncalibrated_tasks'], ['uncalibrated'])
        self.assertTrue(all(m['measured_attempts'] == 2 for m in data['models']))
        row = next(t for t in data['tasks'] if t[0] == 'uncalibrated')
        self.assertTrue(all(cell[0] == 'c' and cell[6] == 'f' and cell[3] is None for cell in row[2]))
