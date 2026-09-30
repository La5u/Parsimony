import importlib.util
import json
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    'priority_driver', Path(__file__).resolve().parents[1] / 'examples/benchmark-discovery/run-priority-live.py')
driver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(driver)


class PriorityDriverTests(unittest.TestCase):
    def test_measure_requires_commit_identity(self):
        with tempfile.TemporaryDirectory() as root, \
             patch.object(driver, 'analyzer_identity', return_value=(None, 'source-hash')), \
             patch.object(sys, 'argv',
                          ['driver', '--output-dir', root, '--phase', 'measure']), \
             patch('sys.stderr'), patch.object(driver, 'Cache') as cache:
            with self.assertRaises(SystemExit) as raised:
                driver.main()
            self.assertEqual(raised.exception.code, 2)
            cache.assert_not_called()

    def test_review_binds_inventory_and_patch(self):
        run = dict(submission_revision='a', result_sha256='b', prediction_sha256='c',
                   dataset=dict(dataset_checksum='d'), records=[dict(task_id='task', patch='patch')])
        audit = dict(scope='touched-file-preimage-not-full-checkout-certification',
                     submission_revision='a', result_sha256='b', prediction_sha256='c',
                     dataset_checksum='d', base_commit_confirmations={},
                     records=[dict(task_id='task', status='unverified', error='mismatch',
                                   patch_sha256=driver.hashlib.sha256(b'patch').hexdigest())])
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'audit.json'
            path.write_text(json.dumps(audit))
            review = driver.review_manifest(run, audit, path)
            self.assertEqual(review['historical_dataset_match'], 'unverified')
            self.assertIn('task', review['blocked_preimages'])
            run['records'][0]['patch'] = 'different'
            with self.assertRaisesRegex(ValueError, 'patch does not bind'):
                driver.review_manifest(run, audit, path)
