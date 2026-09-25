import json
import unittest

from parsimony.scoring import freeze
from parsimony.site import build, label, render
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
