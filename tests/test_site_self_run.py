import unittest

from parsimony.site import self_run_models


def record(task, net, status='ok', excluded=False, result='not_graded'):
    metrics = dict(mode='full_file', net_units=net, churn=abs(net) + 2, touched_files=['a.py'],
                   excluded_files=['a.py'] if excluded else [])
    return dict(agent='self-run-v1_pi_gpt_6_luna_high', task_id=task, self_run=True, benchmark_tasks=20,
                evaluation_result=result, resolved=result == 'resolved', analysis_status=status, metrics=metrics if status == 'ok' else None,
                provenance=dict(model='gpt-6-luna', reasoning_effort='high', harness='pi'))


class SelfRunTest(unittest.TestCase):
    def test_summary_uses_measured_in_scope_attempts_only(self):
        [model] = self_run_models([record('a#1', 10), record('a#2', 20), record('b#1', 0, status='error'),
                                   record('c#1', 99, excluded=True)])
        self.assertEqual(model['name'], 'GPT-6 Luna (high)')
        self.assertEqual(model['company'], 'OpenAI')
        self.assertEqual(model['harness'], 'pi')
        self.assertTrue(model['self_run'])
        self.assertEqual((model['tasks'], model['attempts'], model['measured_attempts']), (3, 4, 2))
        self.assertEqual(model['measured_net_mean'], 15)
        self.assertEqual(model['footprint_population_count'], 20)
        self.assertIsNone(model['resolve_rate'])  # never graded
        self.assertIsNone(model['measured_solved_net_mean'])

    def test_self_graded_summary_adds_solved(self):
        [model] = self_run_models([record('a#1', 10, result='resolved'), record('a#2', 20, result='unresolved'),
                                   record('b#1', 0, status='error', result='resolved'),
                                   record('c#1', 99, excluded=True, result='resolved'), record('d#1', 30, result='unknown')])
        self.assertTrue(model['graded'])
        self.assertEqual(model['upstream_solved_attempts'], 3)  # every resolved attempt, measured or not
        self.assertEqual(model['resolve_rate'], 3 / 20)  # over the planned population
        self.assertEqual(model['measured_solved_attempts'], 1)  # only measured, in-scope successes
        self.assertEqual(model['measured_solved_net_mean'], 10)
        self.assertEqual(model['measured_net_mean'], 20)  # timeouts (unknown) still count as measured

    def test_same_task_ratio_uses_every_ranked_model_as_baseline(self):
        typical = {'a': [20, None, 3], 'd': [60, None, 3], 'e': [5, None, 2]}
        [model] = self_run_models([record('a#1', 10, result='resolved'), record('d#1', 30, result='resolved'),
                                   record('e#1', 1, result='resolved')], typical)
        self.assertEqual(model['same_task_net'], 0.5)  # (10 + 30) / (20 + 60); task e has only 2 models
        self.assertEqual(model['same_task_net_tasks'], 2)
        self.assertIsNone(model['same_task_net_ci'])  # fewer than 5 tasks: no range
        self.assertIsNone(model['same_task_complexity'])
        [ungraded] = self_run_models([record('a#1', 10)], typical)
        self.assertIsNone(ungraded['same_task_net'])

    def test_rejects_published_records(self):
        bad = record('a#1', 1)
        del bad['self_run']
        with self.assertRaises(ValueError):
            self_run_models([bad])


if __name__ == '__main__':
    unittest.main()
