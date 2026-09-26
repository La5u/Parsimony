import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from parsimony.scoring import freeze
from parsimony.site import build, label, main, render, tiers
from tests.test_scoring import record


class SiteTests(unittest.TestCase):
    def test_build_and_render(self):
        records = [record('20260217_mini-v2.0.0_claude-4-6-opus', 't1', net=5, churn=9),
                   record('20260217_mini-v2.0.0_claude-4-6-opus', 't2', net=0, churn=0, resolved=False),
                   record('other-agent', 't1', net=10, churn=30),
                   record('other-agent', 't2', net=3, churn=3)]
        panel = freeze(records, 'site-test')
        data = build(panel, records, draws=50)
        # Ranked by score: the other agent also solved t2.
        self.assertEqual([m['name'] for m in data['models']], ['other-agent', 'Claude Opus 4.6'])
        opus = data['models'][1]
        self.assertEqual((opus['solved'], opus['failed']), (1, 1))
        self.assertLessEqual(opus['ci'][0], opus['score'])
        self.assertEqual([t[0] for t in data['tasks']], ['t1', 't2'])
        self.assertEqual([cell[0] for cell in data['tasks'][1][2]], ['r', 'f'])
        page = render(data)
        self.assertTrue(page.startswith('<!doctype html>'))
        embedded = page.split('type="application/json">')[1].split('</script>')[0]
        self.assertEqual(json.loads(embedded)['panel'], 'site-test')
        self.assertFalse(render(data, standalone=False).startswith('<!doctype'))
        hostile = render({**data, 'panel': '</script><script>alert(1)</script>'})
        self.assertEqual(hostile.count('</script>'), page.count('</script>'))

    def test_label_falls_back_to_identifier(self):
        self.assertEqual(label('20260217_mini-v2.0.0_new-model'), 'new-model')


def pair(a, b, distinguishable, flips_in=()):
    return dict(a=a, b=b, distinguishable=distinguishable, flips_in=list(flips_in))


class TierTests(unittest.TestCase):
    def test_firm_boundary_tie_and_flipped_pair(self):
        sensitivity = dict(ranking=list('abcde'), adjacent_pairs=[
            pair('a', 'b', True),                           # firm boundary
            pair('b', 'c', False),                          # tie
            pair('c', 'd', True, ['without_repo=x/y']),     # distinguishable but flips
            pair('d', 'e', True)])                          # firm boundary
        self.assertEqual(tiers(sensitivity), dict(a=1, b=2, c=2, d=2, e=3))

    def test_single_model(self):
        self.assertEqual(tiers(dict(ranking=['a'], adjacent_pairs=[])), dict(a=1))


class MainTests(unittest.TestCase):
    def run_main(self, *extra):
        records = [record('agent-a', 't1', net=5, churn=9), record('agent-b', 't1', net=10, churn=30)]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / 'panel.json').write_text(json.dumps(freeze(records, 'main-test')))
            (tmp / 'r.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
            argv = ['site', str(tmp / 'panel.json'), str(tmp / 'r.jsonl'), '--output', str(tmp / 'index.html'),
                    '--data', str(tmp / 'data.json'), *[a.replace('TMP', str(tmp)) for a in extra]]
            if extra:
                (tmp / 'sensitivity.json').write_text(json.dumps(dict(
                    ranking=['agent-a', 'agent-b'], adjacent_pairs=[pair('agent-a', 'agent-b', True)])))
            with mock.patch.object(sys, 'argv', argv), redirect_stdout(StringIO()):
                main()
            self.assertTrue((tmp / 'index.html').read_text().startswith('<!doctype html>'))
            return json.loads((tmp / 'data.json').read_text())['models']

    def test_build_without_sensitivity(self):
        self.assertTrue(all('tier' not in m for m in self.run_main()))

    def test_build_with_sensitivity(self):
        models = self.run_main('--sensitivity', 'TMP/sensitivity.json')
        self.assertEqual({m['agent']: m['tier'] for m in models}, {'agent-a': 1, 'agent-b': 2})
