import copy
import unittest

from parsimony.scoring import freeze, score_records, task_score


def record(agent='a', task='task', net=10, churn=10, resolved=True):
    return dict(agent=agent, task_id=task, resolved=resolved, analysis_status='ok',
                analyzer_version='0.1', python_version='3.14', resolve_rate=0.5,
                published_result_categories=['resolved' if resolved else 'unresolved'],
                provenance=dict(repo='org/repo', base_commit='abc'),
                metrics=dict(mode='full_file', net_tokens=net, churn=churn,
                             tokens_added=(churn + net) // 2, tokens_deleted=(churn - net) // 2))


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.panel = freeze([record('a', net=5, churn=9), record('b'),
                             record('c', net=10, churn=30)], 'test-panel')

    def test_blend_and_rewrite_cost(self):
        refs = self.panel['tasks']['task']
        value = task_score(record('candidate', net=10, churn=20), refs)
        self.assertAlmostEqual(value['score'], 34)
        rewrite = task_score(record('rewrite', net=4, churn=1000), refs)
        small = task_score(record('small', net=5, churn=9), refs)
        self.assertAlmostEqual(rewrite['score'], 70.3)
        self.assertGreater(small['score'], rewrite['score'])

    def test_reference_panel_average_is_midpoint(self):
        refs = [record('a', net=5, churn=9), record('b'), record('c', net=10, churn=30)]
        values = score_records(self.panel, refs)
        self.assertAlmostEqual(sum(r['score'] for r in values) / len(values), 50.5)

    def test_ties_and_self_reference(self):
        panel = freeze([record()], 'self')
        result = score_records(panel, [record()])[0]
        self.assertAlmostEqual(result['score'], 50.5)

    def test_failure_penalties(self):
        refs = freeze([record()], 'failure')['tasks']['task']
        self.assertEqual(task_score(record(resolved=False, net=0, churn=0), refs)['score'], 0)
        self.assertAlmostEqual(task_score(record(resolved=False), refs)['score'], -12.5)
        self.assertAlmostEqual(task_score(record(resolved=False, net=-10), refs)['score'], -3.75)
        worst_success = task_score(record(net=1000000, churn=1000000), refs)['score']
        self.assertEqual(worst_success, 1)
        self.assertGreater(worst_success, task_score(record(resolved=False, net=0, churn=0), refs)['score'])
        worse_failure = task_score(record(resolved=False, net=100, churn=100), refs)['score']
        self.assertLess(worse_failure, -12.5)

    def test_zero_baseline_and_equal_task_weights(self):
        panel = freeze([record(task='tiny', net=0, churn=0),
                        record(task='large', net=1000000, churn=1000000)], 'sizes')
        result = score_records(panel, [record(task='tiny', net=2, churn=2),
                                       record(task='large', net=2, churn=2)])[0]
        self.assertEqual(result['score'], 50.5)  # (1 + 100) / 2
        failed = task_score(record(resolved=False, net=0, churn=0), panel['tasks']['tiny'])
        self.assertEqual(failed['score'], 0)

    def test_missing_records_and_unknown_evaluation(self):
        r = record()
        r['metrics'] = None
        r['analysis_status'] = 'error'
        result = score_records(self.panel, [r])[0]
        self.assertIsNone(result['score'])
        self.assertEqual((result['lower'], result['upper']), (1, 100))
        r['resolved'] = False
        r['published_result_categories'] = ['no_logs']
        result = score_records(self.panel, [r])[0]
        self.assertEqual((result['lower'], result['upper']), (-25, 100))
        r['published_result_categories'] = ['unresolved']
        self.assertEqual(score_records(self.panel, [r])[0]['upper'], 0)
        r['task_id'] = 'outside-cohort'
        self.assertEqual(score_records(self.panel, [r])[0]['scored_tasks'], 0)

    def test_no_generation_distinct_from_missing_patch(self):
        r = record(resolved=False)
        r['metrics'] = None
        r['analysis_status'] = 'not_resolved'
        r['published_result_categories'] = ['no_generation']
        self.assertEqual(score_records(self.panel, [r])[0]['score'], 0)
        r['provenance']['patch_sha256'] = __import__('hashlib').sha256(b'nonempty').hexdigest()
        with self.assertRaisesRegex(ValueError, 'nonempty patch'):
            score_records(self.panel, [r])
        r['published_result_categories'] = ['unresolved']
        self.assertIsNone(score_records(self.panel, [r])[0]['score'])

    def test_freeze_does_not_change_when_scoring_and_rejects_duplicates(self):
        before = copy.deepcopy(self.panel)
        score_records(self.panel, [record('new')])
        self.assertEqual(self.panel, before)
        with self.assertRaises(ValueError):
            score_records(self.panel, [record(), record()])
        with self.assertRaises(ValueError):
            freeze([record(resolved=False)], 'no-successes')
        r = record()
        r['python_version'] = 'different'
        with self.assertRaises(ValueError):
            score_records(self.panel, [r])
