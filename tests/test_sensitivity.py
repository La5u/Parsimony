import copy
import unittest

from parsimony.scoring import freeze
from parsimony.sensitivity import contributions, sensitivity
from tests.test_scoring import record


class SensitivityTests(unittest.TestCase):
    def test_default_matches_score_and_reproducible(self):
        refs = [record('a', net=5, churn=9), record('b', net=10, churn=10)]
        panel = freeze(refs, 'sample')
        from parsimony.scoring import score_records
        scores = contributions(panel, refs)
        published = {r['agent']: r['score'] for r in score_records(panel, refs)}
        for agent, values in scores.items():
            self.assertAlmostEqual(values['task'], published[agent])
        result = sensitivity(panel, refs, draws=10, seed=2)
        self.assertEqual(result, sensitivity(panel, refs, draws=10, seed=2))
        self.assertAlmostEqual(sum(v['top_frequency'] for v in result['bootstrap'].values()), 1)

    def test_net_floor_removes_deletion_credit(self):
        refs = [record('a', net=-5, churn=9), record('b', net=10, churn=10)]
        deleter = record('deleter', net=-40, churn=40)
        panel = freeze(refs, 'sample')
        default = contributions(panel, refs + [deleter])['deleter']['task']
        floored = contributions(panel, refs + [deleter], net_floor=0)['deleter']['task']
        self.assertGreater(default, floored)
        self.assertIn('net=0.8,failure_cap=25,net_floor=0', sensitivity(panel, refs, draws=5)['scenario_scores'])

    def test_record_iterators_match_lists(self):
        records = [record('a'), record('b', net=5, churn=9)]
        panel = freeze(records, 'sample')
        self.assertEqual(contributions(panel, iter(records)), contributions(panel, records))
        self.assertEqual(sensitivity(panel, iter(records), draws=10),
                         sensitivity(panel, records, draws=10))

    def test_repeated_attempts_are_resampled_together(self):
        records = [record('a', 'task#1', net=1, churn=1),
                   record('b', 'task#1', net=9, churn=9),
                   record('a', 'task#2', net=9, churn=9),
                   record('b', 'task#2', net=1, churn=1)]
        panel = freeze(records, 'sample')
        scores = contributions(panel, records)
        result = sensitivity(panel, records, draws=100, seed=3)
        for agent in ('a', 'b'):
            mean = sum(scores[agent].values()) / 2
            self.assertEqual(result['bootstrap'][agent]['score_ci_95'], [mean, mean])
            self.assertEqual(result['bootstrap'][agent]['top_frequency'], 0.5)

    def test_invalid_parameters_and_draws(self):
        records = [record()]
        panel = freeze(records, 'sample')
        for name, bad_values in (('net_weight', [-1, 2, float('nan'), float('inf'), True]),
                                 ('failure_cap', [-1, float('nan'), float('inf'), True]),
                                 ('net_floor', [float('nan'), float('inf'), True])):
            for value in bad_values:
                with self.subTest(name=name, value=value), self.assertRaisesRegex(ValueError, 'parameters'):
                    contributions(panel, records, **{name: value})
        for draws in (0, -1, 1.5, True):
            with self.subTest(draws=draws), self.assertRaisesRegex(ValueError, 'draws'):
                sensitivity(panel, records, draws=draws)

    def test_invalid_references_are_rejected(self):
        records = [record('a'), record('b')]
        original = freeze(records, 'sample')
        for kind in ('duplicate', 'metrics', 'base', 'scope'):
            panel = copy.deepcopy(original)
            refs = panel['tasks']['task']
            if kind == 'duplicate':
                refs.append(copy.deepcopy(refs[0]))
            elif kind == 'metrics':
                refs[0]['metrics']['churn'] += 1
            elif kind == 'base':
                refs[1]['provenance']['base_commit'] = 'different'
            else:
                refs[0]['metrics'].update(touched_files=['excluded'], excluded_files=['excluded'])
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                contributions(panel, records)

    def test_incomplete_candidate_is_not_resampled(self):
        panel = freeze([record()], 'sample')
        r = record()
        r['metrics'] = None
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            sensitivity(panel, [r])


if __name__ == '__main__':
    unittest.main()
