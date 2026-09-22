import json
import tempfile
import unittest
from pathlib import Path

from parsimony.contribute import check_records, export, validate


class ContributionTests(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).resolve().parents[1] / 'examples' / 'ten-model-results.jsonl'
        self.record = json.loads(source.read_text().splitlines()[0])

    def test_round_trip_and_tampered_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'input.jsonl'
            source.write_text(json.dumps(self.record) + '\n')
            bundle = root / 'bundle'
            export(source, self.record['agent'], bundle)
            validate(bundle)
            self.assertEqual(json.loads((bundle / 'manifest.json').read_text())['coverage'], 'sample')
            (bundle / 'leaderboard.json').write_text('[]')
            with self.assertRaises(ValueError):
                validate(bundle)

    def test_failed_patch_never_gets_scored(self):
        self.record['resolved'] = False
        with self.assertRaises(ValueError):
            check_records([self.record], self.record['agent'])

    def test_invalid_churn_and_duplicate_tasks(self):
        with self.assertRaises(ValueError):
            check_records([self.record, self.record], self.record['agent'])
        self.record['metrics']['churn'] += 1
        with self.assertRaises(ValueError):
            check_records([self.record], self.record['agent'])

    def test_bad_resolve_rate_and_missing_provenance(self):
        self.record['resolve_rate'] = 1
        with self.assertRaises(ValueError):
            check_records([self.record], self.record['agent'])
        self.record['resolve_rate'] = self.record['published_resolved_count'] / 500
        del self.record['provenance']['results_sha256']
        with self.assertRaises(ValueError):
            check_records([self.record], self.record['agent'])
