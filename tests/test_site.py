import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from parsimony.scoring import freeze
from parsimony.site import add_rank_ranges, build, label, main, render
from tests.test_scoring import record


class SiteTests(unittest.TestCase):
    def test_build_and_render(self):
        records = [record('20260217_mini-v2.0.0_claude-4-6-opus', 't1', net=5, churn=9),
                   record('20260217_mini-v2.0.0_claude-4-6-opus', 't2', net=0, churn=0, resolved=False),
                   record('other-agent', 't1', net=10, churn=30),
                   record('other-agent', 't2', net=3, churn=3)]
        panel = freeze(records, 'site-test')
        data = build(panel, records, draws=50)
        # Footprint leads even though the other agent solves more and scores higher overall.
        self.assertEqual([m['name'] for m in data['models']], ['Claude Opus 4.6', 'other-agent'])
        opus = data['models'][0]
        self.assertLess(opus['score'], data['models'][1]['score'])
        self.assertGreater(opus['solved_mean'], data['models'][1]['solved_mean'])
        self.assertEqual(opus['published_solved'], 1)
        self.assertEqual((opus['solved'], opus['failed']), (1, 1))
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

    def test_footprint_missingness_and_deterministic_ties(self):
        refs = [record('ref', task=t) for t in ('t1', 't2', 't3')]
        panel = freeze(refs, 'coverage-test')
        missing = record('a', 't2')
        missing.update(analysis_status='fetch_error', metrics=None)
        excluded = record('a', 't3', net=0, churn=0)
        excluded['metrics'].update(touched_files=['setup.py'], excluded_files=['setup.py'])
        records = [record('b', 't1'), record('a', 't1'), missing, excluded,
                   record('none', 't1', resolved=False),
                   record('a', 'outside-panel', net=1000, churn=1000)]
        data = build(panel, records, draws=20)
        self.assertEqual([m['agent'] for m in data['models']], ['a', 'b', 'none'])
        a, b, none = data['models']
        self.assertEqual(a['solved_mean'], b['solved_mean'])
        self.assertEqual((a['solved'], a['published_solved'], a['churn']), (1, 3, 10))
        self.assertIsNone(none['solved_mean'])
        self.assertIsNone(none['churn'])
        self.assertEqual(data, build(panel, list(reversed(records)), draws=20))

    def test_footprint_and_all_task_uncertainty_are_separate(self):
        page = render(build(freeze([record()], 'test'), [record()], draws=10))
        headline = page.split('<table id="board">')[1].split('</table>')[0]
        self.assertIn('Footprint credit', headline)
        self.assertNotIn('95%', headline)
        self.assertNotIn('rank-head', headline)
        self.assertIn('Models solve different task subsets', page)
        self.assertIn('id="score-board"', page)
        self.assertIn('these do not apply to the footprint ordering', page)

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

    def test_build_without_sensitivity(self):
        self.assertTrue(all('rank_range' not in m for m in self.run_main()))

    def test_build_with_sensitivity(self):
        models = self.run_main('--sensitivity', 'TMP/sensitivity.json')
        self.assertEqual({m['agent']: m['rank_range'] for m in models}, {'agent-a': [1, 1], 'agent-b': [1, 2]})
