import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from parsimony.artifacts import Cache, load_manifest, load_submission, _parse_predictions, _result_sets


class ArtifactsTests(unittest.TestCase):
    def test_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'preds.jsonl').write_text(json.dumps({'instance_id': 'a', 'model_patch': 'patch'}) + '\n')
            (root / 'results.json').write_text(json.dumps({'resolved': ['a'], 'no_logs': ['b']}))
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps({'agent': 'tester', 'prediction_url': 'preds.jsonl', 'results_url': 'results.json'}))
            loaded = load_manifest(manifest, Cache(root / 'cache'))
            self.assertEqual(loaded['agent'], 'tester')
            self.assertEqual(loaded['resolved'], {'a'})
            self.assertEqual(loaded['evaluated'], {'a', 'b'})
            self.assertEqual(loaded['predictions'], {'a': 'patch'})
            self.assertEqual(len(loaded['provenance']['results_sha256']), 64)

    def test_duplicate_predictions_rejected(self):
        line = json.dumps({'instance_id': 'a', 'patch': ''}).encode() + b'\n'
        with self.assertRaises(ValueError):
            _parse_predictions(line * 2)

    def test_results_required(self):
        with self.assertRaises(ValueError):
            _result_sets({'success': True})
        self.assertEqual(_result_sets({'resolved': []}), (set(), None))

    def test_current_layout_selection_and_missing_patch(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        metadata = b'assets:\n  logs: s3://swe-bench-submissions/bash-only/demo/logs\n'
        details = json.dumps({'b': {'resolved': False}, 'a': {'resolved': True},
                              'c': {'resolved': True}}).encode()
        def fetch(url, _cache):
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return metadata
            if url.endswith('/per_instance_details.json'):
                return details
            if url.endswith('/a/patch.diff'):
                return b'patch-a'
            raise HTTPError(url, 404, 'missing', {}, None)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            loaded = load_submission(submission, Cache(tempfile.mkdtemp()), task_ids=['a', 'c'])
        self.assertEqual(loaded['resolved'], {'a', 'c'})
        self.assertEqual(loaded['evaluated'], {'a', 'b', 'c'})
        self.assertEqual(loaded['predictions'], {'a': 'patch-a'})
        self.assertEqual(loaded['result_details']['missing_patch'], ['c'])

    def test_current_layout_name_null_logs_and_download_limit(self):
        def fetch(url, _cache):
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return b'assets:\n  logs: null\n  trajs: s3://swe-bench-submissions/bash-only/demo/trajs\n'
            if url.endswith('/per_instance_details.json'):
                return b'{"a": {"resolved": true}, "b": {"resolved": true}, "c": {"resolved": false}}'
            if url.endswith('/b/patch.diff'):
                return b'patch-b'
            self.fail('unexpected download: ' + url)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            summary = load_submission('demo', None, task_ids=[])
            self.assertEqual(summary['predictions'], {})
            loaded = load_submission('demo', None, task_ids=['b', 'c'], limit=1)
        self.assertEqual(loaded['resolved'], {'a', 'b'})
        self.assertEqual(loaded['predictions'], {'b': 'patch-b'})
        self.assertEqual(loaded['prediction_locations']['b'],
                         'https://swe-bench-submissions.s3.amazonaws.com/bash-only/demo/logs/b/patch.diff')
        self.assertIn('/tree/main/evaluation/verified/demo', loaded['submission_url'])

    def test_current_layout_requires_real_boolean(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        def fetch(url, _cache):
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return b'assets:\n  logs: s3://swe-bench-submissions/bash-only/demo/logs\n'
            return b'{"a": {"resolved": null}}'
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            with self.assertRaises(ValueError):
                load_submission(submission, Cache(tempfile.mkdtemp()))

    def test_old_non_404_failure_does_not_fallback(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        with patch('parsimony.artifacts._bytes', side_effect=HTTPError('url', 500, 'broken', {}, None)) as fetch:
            with self.assertRaises(HTTPError):
                load_submission(submission, Cache(tempfile.mkdtemp()))
        self.assertEqual(fetch.call_count, 1)

    def test_cache(self):
        import io
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache(directory)
            with patch('parsimony.artifacts.urlopen', return_value=io.BytesIO(b'hello')) as request:
                self.assertEqual(cache.get('https://example.test/a'), b'hello')
                self.assertEqual(cache.get('https://example.test/a'), b'hello')
                self.assertEqual(request.call_count, 1)
