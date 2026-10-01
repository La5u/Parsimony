import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from parsimony.scoring import freeze
from parsimony.site import add_rank_ranges, build, company, label, main, newest_generation, render, trimmed_mean
from tests.test_scoring import record


class SiteTests(unittest.TestCase):
    def test_build_and_render(self):
        records = [record('20260217_mini-v2.0.0_claude-4-6-opus', 't1', net=5, churn=9),
                   record('20260217_mini-v2.0.0_claude-4-6-opus', 't2', net=0, churn=0, resolved=False),
                   record('other-agent', 't1', net=10, churn=30),
                   record('other-agent', 't2', net=3, churn=3)]
        panel = freeze(records, 'site-test')
        data = build(panel, records, draws=50)
        # Footprint rank ignores correctness: Opus has the smaller measured mean.
        self.assertEqual([m['name'] for m in data['models']], ['Claude Opus 4.6', 'other-agent'])
        opus = data['models'][0]
        self.assertEqual((opus['solved'], opus['failed']), (1, 1))
        self.assertEqual((opus['solved_net_mean'], opus['solved_churn_mean']), (5, 9))
        self.assertEqual((opus['measured_net_mean'], opus['measured_churn_mean']), (2.5, 4.5))
        self.assertEqual(opus['measured_attempts'], 2)
        self.assertEqual(opus['company'], 'Anthropic')
        self.assertLessEqual(opus['ci'][0], opus['score'])
        self.assertEqual([t[0] for t in data['tasks']], ['t1', 't2'])
        self.assertEqual((data['references'], data['harness']), (2, ['v2.0.0']))
        self.assertEqual([cell[0] for cell in data['tasks'][1][2]], ['f', 'r'])
        page = render(data)
        self.assertTrue(page.startswith('<!doctype html>'))
        embedded = page.split('type="application/json">')[1].split('</script>')[0]
        self.assertEqual(json.loads(embedded)['panel'], 'site-test')
        self.assertFalse(render(data, standalone=False).startswith('<!doctype'))
        hostile = render({**data, 'panel': '</script><script>alert(1)</script>'})
        self.assertEqual(hostile.count('</script>'), page.count('</script>'))

    def test_confidence_intervals_do_not_affect_scores_or_order(self):
        records = [record('a', 't1', net=1, churn=1), record('a', 't2', net=2, churn=2),
                   record('b', 't1', net=9, churn=9), record('b', 't2', resolved=False)]
        panel = freeze(records, 'ci-independent')
        missing = record('c', 't1')
        missing.update(metrics=None, analysis_status='fetch_error')
        records.append(missing)
        before = build(panel, records, draws=20)
        intervals = {a: dict(ci=[-9999, 9999], top=0) for a in ('a', 'b', 'c')}
        with mock.patch('parsimony.site.bootstrap', return_value=(2, intervals)):
            after = build(panel, records, draws=20)
        for first, second in zip(before['models'], after['models']):
            for key in ('agent', 'score', 'lower', 'upper'):
                self.assertEqual(first[key], second[key], key)
            self.assertNotEqual(first['ci'], second['ci'])

    def test_footprint_means_include_failures_and_tasks_without_references(self):
        records = [record('a', 't1', net=2, churn=4), record('a', 't2', net=6, churn=8),
                   record('a', 't3', net=100, churn=100, resolved=False),
                   record('b', 't3', net=1, churn=1)]
        panel = freeze(records, 'plot-test')
        records += [record('a', 'outside', net=999, churn=999)]
        data = build(panel, records, draws=20)
        a = next(m for m in data['models'] if m['agent'] == 'a')
        self.assertEqual((a['solved_net_mean'], a['solved_churn_mean']), (4, 6))
        self.assertEqual((a['net_units'], a['churn']), (4, 6))
        self.assertEqual(data['excluded_tasks'], ['outside'])
        self.assertEqual(a['measured_net_mean'], 1107 / 4)
        self.assertEqual(a['measured_churn_mean'], 1111 / 4)
        self.assertEqual(a['measured_attempts'], 4)
        self.assertEqual(a['footprint_population_count'], 4)
        self.assertEqual({t[0] for t in data['footprint_tasks']}, {'t1', 't2', 't3', 'outside'})
        for r in records:
            if r['agent'] == 'a' and r['task_id'] in ('t1', 't2'):
                r['analysis_status'] = 'fetch_error'
                r['metrics'] = None
        data = build(panel, records, draws=20)
        a = next(m for m in data['models'] if m['agent'] == 'a')
        self.assertIsNone(a['solved_net_mean'])
        self.assertIsNone(a['solved_churn_mean'])
        self.assertIsNone(a['churn'])
        # Failed attempts remain in the model point; missing measurements do not become zeros.
        self.assertEqual((a['measured_net_mean'], a['measured_churn_mean']), (549.5, 549.5))
        self.assertEqual(a['measured_attempts'], 2)
        i = next(i for i, m in enumerate(data['models']) if m['agent'] == 'a')
        t1 = next(t for t in data['tasks'] if t[0] == 't1')
        self.assertEqual(t1[2][i][3:], [None, 1, 100])

    def test_footprint_ranking_retains_missing_population_and_failed_noops(self):
        refs = [record('a', 't1', net=9, churn=9), record('a', 't2', net=8, churn=8)]
        panel = freeze(refs, 'missing-population')
        missing = record('c', 't1')
        missing.update(metrics=None, analysis_status='fetch_error')
        data = build(panel, [refs[0], record('b', 't1', net=0, churn=0, resolved=False), missing], draws=20)
        self.assertEqual(data['ranking_metric'], 'measured-net-trimmed-mean-10-v1')
        self.assertEqual([m['agent'] for m in data['models']], ['b', 'a', 'c'])
        self.assertEqual([m['measured_net_mean'] for m in data['models']], [0, 9, None])
        self.assertEqual([m['measured_net_trimmed_mean'] for m in data['models']], [0, 9, None])
        self.assertEqual([m['measured_attempts'] for m in data['models']], [1, 1, 0])
        self.assertEqual([m['footprint_population_count'] for m in data['models']], [2, 2, 2])
        self.assertEqual([row[0] for row in data['footprint_tasks']], ['t1', 't2'])
        self.assertTrue(all(cell[7] is False for cell in data['footprint_tasks'][1][2]))

    @unittest.skipUnless(shutil.which('node'), 'JavaScript interaction test requires Node.js')
    def test_single_failed_mass_deletion_does_not_decide_rank(self):
        tasks = [f't{i:02}' for i in range(20)]
        steady = [record('steady', t, net=5, churn=5) for t in tasks]
        # 19 larger patches plus one failed deletion: the plain mean is lower, the trimmed mean is not.
        deleter = [record('deleter', t, net=20, churn=20) for t in tasks[1:]]
        deleter.append(record('deleter', tasks[0], net=-5000, churn=5000, resolved=False))
        panel = freeze(steady, 'trimmed')
        data = build(panel, steady + deleter, draws=20)
        by_agent = {m['agent']: m for m in data['models']}
        self.assertLess(by_agent['deleter']['measured_net_mean'], by_agent['steady']['measured_net_mean'])
        self.assertEqual(by_agent['deleter']['measured_net_trimmed_mean'], 20)
        self.assertEqual([m['agent'] for m in data['models']], ['steady', 'deleter'])

    def test_newest_generation_per_model_line(self):
        names = ['Claude Opus 5 (max)', 'Claude Opus 4.8 (max)', 'Claude Sonnet 4.6 (high)', 'GPT-5.6 Sol (max)',
                 'GPT-5.6 Luna (max)', 'GPT-5.5 (xhigh)', 'GPT-5 mini', 'Kimi K3 (max)', 'Kimi K2.7 Code',
                 'gpt-oss-120b', 'o3', 'o4-mini', 'Claude Opus 4', 'other-agent']
        self.assertEqual(newest_generation(names), {
            'Claude Opus 5 (max)', 'Claude Sonnet 4.6 (high)', 'GPT-5.6 Sol (max)', 'GPT-5.6 Luna (max)',
            'Kimi K3 (max)', 'gpt-oss-120b', 'o4-mini', 'other-agent'})
        records = [record('20260217_mini-v2.0.0_claude-4-6-opus', 't1', net=5, churn=9),
                   record('20251124_mini-v1.16.0_claude-opus-4-5-20251101', 't1', net=7, churn=9)]
        data = build(freeze(records, 'generations'), records, draws=20)
        self.assertEqual({m['name']: m['latest'] for m in data['models']},
                         {label(records[0]['agent']): True, label(records[1]['agent']): False})

    def test_trimmed_mean(self):
        self.assertIsNone(trimmed_mean([]))
        self.assertEqual(trimmed_mean([1, 2, 100]), 103 / 3)  # Fewer than 20 values: plain mean.
        self.assertEqual(trimmed_mean([-1000] + [1] * 18 + [1000]), 1)  # One value dropped from each end.

    def test_column_sorting(self):
        records = [record()]
        page = render(build(freeze(records, 'sorting-test'), records, draws=10))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'index.html'
            path.write_text(page)
            result = subprocess.run(['node', str(Path(__file__).with_name('site_sorting.cjs')), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_company_is_model_developer(self):
        for agent, expected in {
            'deepswe-v1.1_mini_swe_agent_claude_opus_5_max': 'Anthropic',
            'deepswe-v1.1_mini_swe_agent_gpt_5_6_sol_max': 'OpenAI',
            'deepswe-v1.1_mini_swe_agent_gemini_3_7_flash_medium': 'Google',
            'deepswe-v1.1_mini_swe_agent_muse_spark_1_2_xhigh': 'Meta',
            'deepswe-v1.1_mini_swe_agent_glm_5_3_max': 'Z.ai',
            'deepswe-v1.1_mini_swe_agent_qwen3_8_max_xhigh': 'Alibaba',
            'deepswe-v1.1_mini_swe_agent_kimi_k3_max': 'Moonshot AI',
            'deepswe-v1.1_mini_swe_agent_grok_4_6_medium': 'xAI',
            'deepswe-v1.1_mini_swe_agent_deepseek_v4_pro_max': 'DeepSeek',
            '20250720_mini-v0.0.0-Llama-4-Maverick-17B-Instruct': 'Meta',
            '20260217_mini-v2.0.0_minimax-2-5-high': 'MiniMax',
            'devstral-2512': 'Mistral AI', 'o3-2025-04-16': 'OpenAI',
            'other-model': 'Other',
        }.items():
            self.assertEqual(company(agent), expected, agent)

    def test_model_plot_no_measurements_is_missing_not_zero(self):
        panel = freeze([record('ref')], 'empty-plot')
        missing = record('candidate')
        missing.update(metrics=None, analysis_status='fetch_error')
        model, = build(panel, [missing], draws=10)['models']
        self.assertIsNone(model['measured_net_mean'])
        self.assertIsNone(model['measured_churn_mean'])
        self.assertEqual(model['measured_attempts'], 0)

    def test_label_falls_back_to_identifier(self):
        self.assertEqual(label('20260217_mini-v2.0.0_new-model'), 'new-model')
        self.assertEqual(label('20250720_mini-v0.0.0-Llama-4-Maverick-17B-Instruct'), 'Llama 4 Maverick')


def sensitivity(ranges):
    return dict(bootstrap=dict(models={a: dict(rank_ci_95=r) for a, r in ranges.items()}))


class RankRangeTests(unittest.TestCase):
    def test_rank_ranges_from_bootstrap(self):
        models = [dict(agent='a'), dict(agent='b')]
        add_rank_ranges(models, sensitivity(dict(a=[1, 1], b=[2, 3])))
        self.assertEqual([m['rank_range'] for m in models], [[1, 1], [2, 3]])

    def test_model_missing_from_sensitivity_gets_no_range(self):
        models = [dict(agent='a'), dict(agent='new')]
        add_rank_ranges(models, sensitivity(dict(a=[1, 2])))
        self.assertEqual([m['rank_range'] for m in models], [[1, 2], None])


class MainTests(unittest.TestCase):
    def run_main(self, *extra):
        records = [record('agent-a', 't1', net=5, churn=9), record('agent-b', 't1', net=10, churn=30)]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / 'panel.json').write_text(json.dumps(freeze(records, 'main-test')))
            (tmp / 'r.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
            argv = ['site', str(tmp / 'panel.json'), str(tmp / 'r.jsonl'), '--output', str(tmp / 'index.html'),
                    '--data', str(tmp / 'data.json'), *[a.replace('TMP', str(tmp)) for a in extra]]
            if '--sensitivity' in extra:
                (tmp / 'sensitivity.json').write_text(json.dumps(sensitivity({'agent-a': [1, 1], 'agent-b': [1, 2]})))
            with mock.patch.object(sys, 'argv', argv), redirect_stdout(StringIO()):
                main()
            self.assertTrue((tmp / 'index.html').read_text().startswith('<!doctype html>'))
            self.last = Path(tempfile.mkdtemp())
            (self.last / 'data.json').write_text((tmp / 'data.json').read_text())
            return json.loads((tmp / 'data.json').read_text())['models']

    def test_benchmark_and_nav(self):
        models = self.run_main('--benchmark', 'deepswe', '--nav', 'Other board=other.html')
        self.assertEqual(len(models), 2)
        data = json.loads((self.last / 'data.json').read_text())
        self.assertEqual(data['benchmark']['name'], 'DeepSWE')
        self.assertEqual(data['nav'], [dict(label='Other board', url='other.html')])

    def test_live_discloses_mixed_harnesses_and_candidate_provenance(self):
        self.run_main('--benchmark', 'live')
        data = json.loads((self.last / 'data.json').read_text())
        self.assertEqual(data['benchmark']['name'], 'SWE-bench Live Lite')
        self.assertIn('not a controlled model-only comparison', data['benchmark']['harness_note'])
        self.assertIn('not independently certified', data['benchmark']['notice'])
        self.assertEqual(company('live-lite-gpt-5.6-sol-slingshot-3.4.0'), 'OpenAI')
        self.assertEqual(company('live-lite-deepseek-v4.1-flash-tianxicode-0.1.423'), 'DeepSeek')
        self.assertEqual(company('live-lite-claude-opus-4.8-aiwork'), 'Anthropic')
        self.assertIn('Slingshot 3.4.0', label('live-lite-gpt-5.6-sol-slingshot-3.4.0'))

    def test_build_without_sensitivity(self):
        self.assertTrue(all('rank_range' not in m for m in self.run_main()))

    def test_build_with_sensitivity(self):
        models = self.run_main('--sensitivity', 'TMP/sensitivity.json')
        self.assertEqual({m['agent']: m['rank_range'] for m in models}, {'agent-a': [1, 1], 'agent-b': [1, 2]})
