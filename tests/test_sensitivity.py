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

    def test_incomplete_candidate_is_not_resampled(self):
        panel = freeze([record()], 'sample')
        r = record()
        r['metrics'] = None
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            sensitivity(panel, [r])


if __name__ == '__main__':
    unittest.main()
