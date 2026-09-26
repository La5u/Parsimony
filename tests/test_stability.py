import unittest

from parsimony.scoring import freeze, score_records
from parsimony.stability import (analyze, bootstrap, common_tasks, dedup, drop_agent, group, matrix, render,
                                 summarize, task_value)
from tests.test_scoring import record


def rec(agent, task, net=10, churn=10, resolved=True, sha=None):
    r = record(agent, task, net=net, churn=churn, resolved=resolved)
    r['provenance']['patch_sha256'] = sha or f'{agent}-{task}'
    return r


def cohort():
    """Three agents over four tasks; 'c' alone solves t4, 'a' and 'b' submit an identical t1 patch."""
    return [rec('a', 't1', 5, 9, sha='same'), rec('b', 't1', 5, 9, sha='same'), rec('c', 't1', 20, 30),
            rec('a', 't2', 4, 6), rec('b', 't2', 8, 12), rec('c', 't2', 30, 40, resolved=False),
            rec('a', 't3', 2, 2), rec('b', 't3', 10, 20, resolved=False), rec('c', 't3', 6, 8),
            rec('a', 't4', 3, 5, resolved=False), rec('b', 't4', 7, 9, resolved=False), rec('c', 't4', 9, 11)]


class StabilityTests(unittest.TestCase):
    def test_baseline_matches_published_score(self):
        records = cohort()
        panel = freeze(records, 'p')
        summary = summarize(matrix(panel, group(records), panel['net_weight'], panel['failure_cap']))
        for entry in score_records(panel, records):
            self.assertAlmostEqual(summary['models'][entry['agent']]['full_score'], entry['score'])
            self.assertAlmostEqual(summary['models'][entry['agent']]['score'], entry['score'])

    def test_leave_one_out_equals_refreeze_and_reports_orphans(self):
        records = cohort()
        panel = freeze(records, 'p')
        reduced, orphans = drop_agent(panel, 'c')
        self.assertEqual(orphans, ['t4'])
        refrozen = freeze([r for r in records if r['agent'] != 'c' and r['task_id'] != 't4'], 'q')
        self.assertEqual(reduced['tasks'], refrozen['tasks'])
        # The left-out model is still scored, against the panel without its own patches.
        values = matrix(reduced, group(records), 0.7, 25)
        self.assertNotIn('t4', values['c'])
        self.assertLess(values['c']['t1'][0], task_value(records[2], panel['tasks']['t1'], 0.7, 25)[0])

    def test_dedup_counts_identical_patches_once(self):
        records = cohort()
        panel = freeze(records, 'p')
        deduped, removed = dedup(panel)
        self.assertEqual(removed, 1)
        self.assertEqual([r['agent'] for r in deduped['tasks']['t1']], ['a', 'c'])
        self.assertEqual(len(deduped['tasks']['t2']), 2)
        # With duplicates, the shared patch ties twice (0.5 + 0.5 + 1 over 3); deduplicated, 0.5 + 1 over 2.
        self.assertAlmostEqual(task_value(records[0], panel['tasks']['t1'], 1.0, 25)[0], 1 + 99 * 2 / 3)
        self.assertAlmostEqual(task_value(records[0], deduped['tasks']['t1'], 1.0, 25)[0], 1 + 99 * 0.75)

    def test_paired_difference_ci(self):
        values = {'good': {f't{i}': (60 + i % 3, 0, 0) for i in range(30)},
                  'bad': {f't{i}': (20 + i % 5, 0, 0) for i in range(30)},
                  'twin': {f't{i}': (60 + i % 3, 0, 0) for i in range(30)}}
        tasks = sorted(values['good'])
        result = bootstrap(values, tasks, draws=200, seed=3)
        self.assertEqual(result, bootstrap(values, tasks, draws=200, seed=3))
        gb, bg = result['pairs']['good|bad'], result['pairs']['bad|good']
        self.assertGreater(gb['ci_95'][0], 0)
        self.assertEqual(gb['p_greater'], 1)
        self.assertAlmostEqual(gb['difference'], -bg['difference'])
        self.assertEqual(result['pairs']['good|twin']['ci_95'], [0, 0])
        self.assertEqual(result['models']['bad']['rank_counts'], [0, 0, 200])
        self.assertEqual(sum(result['models']['good']['rank_counts']), 200)

    def test_unscored_tasks_give_bounds_not_points(self):
        records = cohort()
        panel = freeze(records, 'p')
        broken = rec('d', 't2', resolved=False)
        broken['analysis_status'] = 'error'
        candidates = records + [broken, rec('d', 't1'), rec('d', 't3')]  # no t4 record at all
        values = matrix(panel, group(candidates), 0.7, 25)
        self.assertEqual(values['d']['t2'], (None, -25, 0))
        self.assertEqual(values['d']['t4'], (None, -25, 100))
        self.assertEqual(task_value(broken, panel['tasks']['t2'], 0.7, 10), (None, -10, 0))
        self.assertEqual(common_tasks(values), ['t1', 't3'])
        summary = summarize(values)
        d = summary['models']['d']
        self.assertIsNone(d['full_score'])
        self.assertEqual(summary['common_tasks'], 2)
        self.assertAlmostEqual(d['score'], (values['d']['t1'][0] + values['d']['t3'][0]) / 2)
        self.assertLess(d['lower'], d['upper'])
        self.assertAlmostEqual(d['upper'] - d['lower'], (25 + 125) / 4)
        self.assertIsNotNone(summary['models']['a']['full_score'])

    def test_analyze_and_render(self):
        records = cohort()
        panel = freeze(records, 'p')
        result = analyze(panel, records, draws=50, seed=1)
        self.assertEqual(result['baseline'], dict(net_weight=0.8, churn_weight=0.2, failure_cap=25))
        self.assertEqual(result['leave_one_out']['c']['orphaned_tasks'], ['t4'])
        self.assertEqual(len(result['adjacent_pairs']), 2)
        self.assertIn('net_floor=0', result['scenarios'])
        self.assertIn('failure_cap=0', result['scenarios'])
        for scenario in result['scenarios'].values():
            self.assertEqual(sorted(scenario['ranking']), ['a', 'b', 'c'])
        text = render(result, 'python -m parsimony.stability ...')
        self.assertTrue(text.startswith('# '))
        self.assertIn('**Verdict.**', text)


if __name__ == '__main__':
    unittest.main()
