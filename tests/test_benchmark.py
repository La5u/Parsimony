import copy
import unittest

from parsimony.benchmark import analyze_submission, leaderboard


def record(agent, task, resolved=True, net=1):
    return dict(agent=agent, task_id=task, resolved=resolved, resolve_rate=0.5,
                analysis_status='ok', model_human_ratio=None,
                metrics=dict(mode='full_file', net_tokens=net, churn=abs(net),
                             files_changed=1, ast_delta=net, complexity_delta=0))


class BenchmarkTests(unittest.TestCase):
    def test_failed_never_ranked(self):
        rows = leaderboard([record('a', '1', False, -999), record('a', '2', True, 10)])
        self.assertEqual(rows[0]['median_net_tokens'], 10)
        self.assertEqual(rows[0]['successful_tasks_analyzed'], 1)

    def test_shared(self):
        records = [record('a', '1'), record('a', '2'), record('b', '2'), record('b', '3')]
        rows = leaderboard(records, shared=True)
        self.assertTrue(all(r['task_ids'] == ['2'] for r in rows))
        self.assertTrue(all(r['successful_tasks_analyzed'] == 1 for r in rows))
        self.assertEqual(leaderboard(records, True, ['a'])[0]['task_ids'], ['1', '2'])
        self.assertEqual(leaderboard(records, True, ['a', 'missing'])[0]['successful_tasks_analyzed'], 0)

    def test_duplicates_rejected(self):
        r = record('a', '1')
        with self.assertRaises(ValueError):
            leaderboard([r, copy.deepcopy(r)])

    def test_empty_shared_is_not_zero_score(self):
        rows = leaderboard([record('a', '1'), record('b', '2')], shared=True)
        self.assertTrue(all(r['median_net_tokens'] is None for r in rows))

    def test_correctness_gate_and_limit_keep_denominator(self):
        submission = dict(agent='a', predictions={'a': '', 'b': '', 'c': ''}, resolved={'a', 'b'},
                          evaluated={'a', 'b', 'c'}, provenance={'prediction_url': 'local'})
        rows = list(analyze_submission(submission, None, limit=1, patch_only=True))
        self.assertEqual([r['analysis_status'] for r in rows], ['ok', 'limit', 'not_resolved'])
        self.assertTrue(all(r['resolve_rate'] == 2 / 500 for r in rows))
        self.assertIsNone(rows[2]['metrics'])

    def test_task_selection_keeps_denominator_and_patch_location(self):
        submission = dict(agent='a', predictions={'a': '', 'b': '', 'c': ''}, resolved={'a', 'b'},
                          evaluated={'a', 'b', 'c'}, provenance={'prediction_url': 'local'},
                          prediction_locations={'b': 'https://example.test/b/patch.diff'})
        rows = list(analyze_submission(submission, None, task_ids=['b'], limit=1, patch_only=True))
        self.assertEqual([r['analysis_status'] for r in rows], ['not_selected', 'ok', 'not_resolved'])
        self.assertTrue(all(r['resolve_rate'] == 2 / 500 for r in rows))
        self.assertEqual(rows[1]['provenance']['patch_location'], 'https://example.test/b/patch.diff')
        with self.assertRaises(ValueError):
            list(analyze_submission(submission, None, task_ids=['unknown'], patch_only=True))

    def test_failed_patch_analysis_requires_opt_in_and_explicit_category(self):
        submission = dict(agent='a', predictions={'failed': ''}, resolved=set(), evaluated={'failed', 'nolog'},
                          result_details={'unresolved': ['failed'], 'no_logs': ['nolog']},
                          provenance={'prediction_url': 'local'})
        default = list(analyze_submission(submission, None, patch_only=True))
        self.assertEqual([r['analysis_status'] for r in default], ['not_resolved', 'not_resolved'])
        opted_in = list(analyze_submission(submission, None, patch_only=True, include_failed=True))
        self.assertEqual([r['analysis_status'] for r in opted_in], ['ok', 'not_resolved'])
        self.assertFalse(opted_in[0]['resolved'])
        self.assertEqual(opted_in[0]['evaluation_result'], 'not_resolved')

    def test_modes_not_mixed(self):
        r = record('a', '1')
        r['metrics']['mode'] = 'patch_only'
        self.assertEqual(leaderboard([r])[0]['successful_tasks_analyzed'], 0)
        self.assertEqual(leaderboard([r], mode='patch_only')[0]['successful_tasks_analyzed'], 1)
