import json
import tempfile
import unittest
from pathlib import Path

import hashlib
from unittest.mock import patch

from parsimony.benchmark import ANALYZER_VERSION
from parsimony.contribute import check_records, export, fetch_patch, validate, verify


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

    def test_explicit_failed_patch_metrics_allowed(self):
        self.record.update(resolved=False, published_result_categories=['unresolved'])
        check_records([self.record], self.record['agent'])

    def test_verify_rechecks_hash_and_metrics(self):
        diff = '--- a/pkg/m.py\n+++ b/pkg/m.py\n@@ -1 +1 @@\n-x = 1\n+x = 2\n'
        from parsimony.analysis import measure
        record = dict(agent='a', task_id='t', analyzer_version=ANALYZER_VERSION, analysis_status='ok',
                      metrics=measure(diff, lambda p: 'x = 1\n'),
                      provenance=dict(repo='org/repo', base_commit='abc', patch_location='https://x/t/patch.diff',
                                      patch_sha256=hashlib.sha256(diff.encode()).hexdigest()))
        dataset = [dict(instance_id='t', repo='org/repo', base_commit='abc')]
        class Cache:
            def get(self, url):
                return b'x = 1\n'
        with patch('parsimony.contribute._bytes', return_value=diff.encode()):
            self.assertEqual(verify([record], dataset, Cache())['failures'], 0)
            record['metrics']['churn'] += 1
            self.assertEqual(verify([record], dataset, Cache())['failures'], 1)
            record['provenance']['patch_sha256'] = '0' * 64
            self.assertFalse(verify([record], dataset, Cache())['results'][0]['patch_sha256_matches'])
        old = dict(self.record, analyzer_version='0.1.0')  # older analyzers: hash-only check
        with patch('parsimony.contribute.fetch_patch', return_value='tampered'):
            row = verify([old], [], Cache())['results'][0]
        self.assertIsNone(row['metrics_match'])
        self.assertFalse(row['patch_sha256_matches'])

    def test_verify_rejects_nonpositive_samples_and_duplicate_metadata(self):
        for sample in (0, -1, False):
            with self.subTest(sample=sample), self.assertRaisesRegex(ValueError, 'sample must be positive'):
                verify([], [], None, sample=sample)
        with self.assertRaisesRegex(ValueError, 'duplicate dataset task ID'):
            verify([], [{'instance_id': 't'}, {'instance_id': 't'}], None)

    def test_prediction_fragment_must_match_record_task(self):
        record = dict(task_id='a', provenance={'patch_location': 'https://x/preds#instance_id=b'})
        with patch('parsimony.contribute._bytes') as download:
            with self.assertRaisesRegex(ValueError, 'fragment differs'):
                fetch_patch(record, None)
            download.assert_not_called()

    def test_patch_digest_must_be_sha256(self):
        for digest in ('x', 'g' * 64, 123):
            with self.subTest(digest=digest):
                self.record['provenance']['patch_sha256'] = digest
                with self.assertRaisesRegex(ValueError, 'patch artifact SHA256 required'):
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
