import json
import unittest

from parsimony.external import attach, snapshot

RAW = json.dumps({'data': [
    {'id': 'a1', 'name': 'Model A (Max)', 'slug': 'model-a', 'release_date': '2026-09-01',
     'evaluations': {'artificial_analysis_intelligence_index': 50.5, 'artificial_analysis_coding_index': 77.0}},
    {'id': 'b1', 'name': 'Model B', 'slug': 'model-b', 'release_date': '2026-08-01',
     'evaluations': {'artificial_analysis_intelligence_index': 30.0, 'artificial_analysis_coding_index': None}},
]}).encode()


class ExternalTest(unittest.TestCase):
    def test_snapshot_keeps_only_mapped_values_and_nulls(self):
        mapping = {'configurations': {
            'agent-a': {'aa_id': 'a1', 'match': 'exact'},
            'agent-b': {'aa_id': 'b1', 'match': 'effort_unlabelled', 'note': 'single entry'},
            'agent-c': {'aa_id': None, 'reason': 'effort not listed'}}}
        snap = snapshot(mapping, RAW, '2026-10-08T00:00:00Z')
        self.assertEqual(snap['configurations']['agent-a']['aa_coding'], 77.0)
        self.assertIsNone(snap['configurations']['agent-b']['aa_coding'])  # missing upstream stays null
        self.assertEqual(snap['configurations']['agent-b']['note'], 'single entry')
        self.assertIsNone(snap['configurations']['agent-c']['aa_intelligence'])
        self.assertEqual(snap['configurations']['agent-c']['reason'], 'effort not listed')
        self.assertEqual(len(snap['response_sha256']), 64)
        self.assertNotIn('Model A (Max)', json.dumps(snap['configurations']['agent-c']))

    def test_snapshot_rejects_unknown_ids_and_match_types(self):
        with self.assertRaises(ValueError):
            snapshot({'configurations': {'x': {'aa_id': 'zz', 'match': 'exact'}}}, RAW, 't')
        with self.assertRaises(ValueError):
            snapshot({'configurations': {'x': {'aa_id': 'a1', 'match': 'similar'}}}, RAW, 't')

    def test_attach_leaves_unmapped_models_null(self):
        snap = snapshot({'configurations': {'agent-a': {'aa_id': 'a1', 'match': 'exact'}}}, RAW, 't')
        models = [{'agent': 'agent-a'}, {'agent': 'other'}]
        meta = attach(models, snap)
        self.assertEqual(models[0]['aa_intelligence'], 50.5)
        self.assertIsNone(models[1]['aa_coding'])
        self.assertIsNone(models[1]['aa_match'])
        self.assertEqual(meta['attribution'], 'https://artificialanalysis.ai/')


if __name__ == '__main__':
    unittest.main()
