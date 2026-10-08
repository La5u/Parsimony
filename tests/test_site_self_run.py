import unittest

from parsimony.site import self_run_models


def record(task, net, status='ok', excluded=False):
    metrics = dict(mode='full_file', net_units=net, churn=abs(net) + 2, touched_files=['a.py'],
                   excluded_files=['a.py'] if excluded else [])
    return dict(agent='self-run-v1_pi_gpt_6_luna_high', task_id=task, self_run=True, benchmark_tasks=20,
                analysis_status=status, metrics=metrics if status == 'ok' else None,
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

    def test_rejects_published_records(self):
        bad = record('a#1', 1)
        del bad['self_run']
        with self.assertRaises(ValueError):
            self_run_models([bad])


if __name__ == '__main__':
    unittest.main()
