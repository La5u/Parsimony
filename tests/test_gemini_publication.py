import json
from pathlib import Path
import unittest

from parsimony.benchmark import read_jsonl
from parsimony.release import audit
from parsimony.scoring import measured, out_of_scope

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'examples/mini-swe-agent-500'


class GeminiPublicationTests(unittest.TestCase):
    def test_complete_population_and_compatible_identity(self):
        records = read_jsonl(DATA / 'gemini-3-5-flash.jsonl')
        manifest = json.loads((DATA / 'population.json').read_text())
        report = audit(manifest, records)
        self.assertEqual(report['task_count'], 500)
        self.assertEqual(len(records), 500)
        self.assertEqual(sum(r['resolved'] for r in records), 359)
        self.assertEqual(sum(r['evaluation_result'] == 'failed' for r in records), 82)
        missing = [r for r in records if r['evaluation_result'] == 'no_generation']
        self.assertEqual(len(missing), 59)
        self.assertTrue(all(r['metrics'] is None for r in missing))
        self.assertEqual({r['analyzer_commit'] for r in records},
                         {'0aa66dfb6dca76893b0f20e22233317965ff0d25'})
        old = read_jsonl(DATA / 'claude-4-6-opus.jsonl')[0]
        self.assertEqual({r['analyzer_source_sha256'] for r in records},
                         {old['analyzer_source_sha256']})
        self.assertTrue(all(r['human_metrics'] is None and r['model_human_ratio'] is None
                            for r in records))
        eligible = [r for r in records if measured(r) and not out_of_scope(r['metrics'])]
        self.assertEqual(len(eligible), 441)
        evidence = json.loads((DATA / 'gemini-3-5-publication-evidence.json').read_text())
        hashes = {p['task_id']: p['sha256'] for p in evidence['patches']}
        self.assertEqual({r['task_id']: r['provenance']['patch_sha256'] for r in eligible}, hashes)

    def test_board_contains_new_configuration_without_zero_fill(self):
        page = (ROOT / 'site/verified.html').read_text()
        data = json.loads(page.split('type="application/json">')[1].split('</script>')[0])
        self.assertEqual(len(data['models']), 34)
        self.assertEqual(data['population_count'], 500)
        self.assertEqual(data['ranking_metric'], 'measured-net-mean-v1')
        model = next(m for m in data['models'] if 'gemini-3-5-flash' in m['agent'])
        self.assertEqual(model['measured_attempts'], 441)
        self.assertEqual(model['footprint_population_count'], 500)
        self.assertAlmostEqual(model['measured_net_mean'], 36.6031746031746)
        self.assertEqual(model['resolve_rate'], 359 / 500)
        self.assertTrue(model['latest'])
        records = read_jsonl(DATA / 'gemini-3-5-flash.jsonl')
        index = data['models'].index(model)
        cells = {row[0]: row[2][index] for row in data['footprint_tasks']}
        for record in records:
            if record['evaluation_result'] == 'no_generation':
                self.assertFalse(cells[record['task_id']][7])
                self.assertIsNone(cells[record['task_id']][1])
