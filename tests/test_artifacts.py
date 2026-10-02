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

    def test_submitter_github_assets_use_declared_path_and_pin(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        requested = []
        def fetch(url, _cache):
            requested.append(url)
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return (b'assets:\n  repo: https://github.com/submitter/run-artifacts\n'
                        b'  ref: refs/tags/run-v1\n  logs: https://github.com/submitter/run-artifacts/tree/main/artifacts/logs\n'
                        b'info:\n  commit: 2f6637a2557da1f7b5f2b583ab7090a077bbeed2\n')
            if url.endswith('/per_instance_details.json'):
                return (b'{"pass":{"resolved":true},"fail":{"resolved":false},'
                        b'"absent":{"resolved":false,"status":"no_logs"},'
                        b'"mystery":{"resolved":false,"status":"unknown"}}')
            if url.endswith('/pass/patch.diff'):
                return b'passing patch'
            if url.endswith('/fail/patch.diff'):
                return b'failed patch'
            if url.endswith('/pass/report.json'):
                return b'{"pass":{"resolved":true}}'
            raise HTTPError(url, 404, 'missing', {}, None)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            loaded = load_submission(submission, Cache(tempfile.mkdtemp()), include_failed=True)
        prefix = 'https://raw.githubusercontent.com/submitter/run-artifacts/refs/tags/run-v1/artifacts/logs'
        self.assertEqual(loaded['predictions'], {'pass': 'passing patch', 'fail': 'failed patch'})
        self.assertEqual(loaded['result_details']['no_logs'], ['absent'])
        self.assertEqual(loaded['result_details']['unknown'], ['mystery'])
        self.assertEqual(loaded['result_details']['missing_patch'], [])
        self.assertEqual(loaded['prediction_locations']['pass'], prefix + '/pass/patch.diff')
        self.assertEqual(loaded['provenance']['ref'], 'refs/tags/run-v1')
        self.assertEqual(loaded['provenance']['layout'], 'submitter-github-per-instance-v1')
        self.assertFalse(any('s3.amazonaws.com' in url for url in requested))

    def test_info_commit_pins_per_instance_assets_without_inventing_outcomes(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        commit = '2f6637a2557da1f7b5f2b583ab7090a077bbeed2'
        requested = []
        metadata = (f'info:\n  commit: "{commit}"\n'
                    'assets:\n  repo: https://github.com/submitter/artifacts/tree/main/run\n'
                    '  logs: https://github.com/submitter/artifacts/tree/main/run/logs\n').encode()
        def fetch(url, _cache):
            requested.append(url)
            if url.endswith('/metadata.yaml'):
                return metadata
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/per_instance_details.json'):
                return b'{"pass":{"resolved":true},"fail":{"resolved":false}}'
            if url.endswith('/fail/patch.diff'):
                return b'failed patch'
            raise AssertionError('unexpected request: ' + url)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            summary = load_submission(submission, None, task_ids=[], include_failed=True)
            self.assertEqual(summary['predictions'], {})
            self.assertFalse(any(url.endswith('/patch.diff') for url in requested))
            loaded = load_submission(submission, None, task_ids=['fail'], limit=1, include_failed=True)
        prefix = f'https://raw.githubusercontent.com/submitter/artifacts/{commit}/run'
        self.assertIn(prefix + '/all_preds.jsonl', requested)
        self.assertIn(prefix + '/logs/fail/patch.diff', requested)
        self.assertFalse(any('/submitter/artifacts/main/' in url for url in requested))
        self.assertEqual(loaded['predictions'], {'fail': 'failed patch'})
        self.assertEqual(loaded['evaluated'], {'pass', 'fail'})
        self.assertEqual(loaded['result_details']['unresolved'], ['fail'])
        self.assertEqual(loaded['result_details']['no_generation'], [])
        self.assertEqual(loaded['prediction_locations']['pass'], prefix + '/logs/pass/patch.diff')
        self.assertEqual(loaded['provenance']['metadata_ref'], 'main')
        self.assertEqual(loaded['provenance']['artifact_ref'], commit)
        self.assertEqual(loaded['provenance']['ref'], commit)

    def test_monolithic_info_pin_and_explicit_assets_pin_precedence(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        info_commit = '2f6637a2557da1f7b5f2b583ab7090a077bbeed2'
        asset_commit = 'a' * 40
        cases = [('', info_commit),
                 ('  ref: refs/tags/run-v1\n', 'refs/tags/run-v1'),
                 (f'  commit: {asset_commit}\n  ref: refs/tags/run-v1\n', asset_commit)]
        for declared_pin, expected_ref in cases:
            with self.subTest(pin=declared_pin):
                requested = []
                def fetch(url, _cache):
                    requested.append(url)
                    if url.endswith('/metadata.yaml'):
                        return (f'info:\n  commit: {info_commit}\nassets:\n'
                                '  repo: https://github.com/submitter/artifacts/tree/main/run\n'
                                + declared_pin +
                                '  logs: https://github.com/submitter/artifacts/tree/main/run/logs\n').encode()
                    if url.endswith('/all_preds.jsonl'):
                        return b'{"instance_id":"pass","patch":"p"}\n{"instance_id":"fail","patch":"q"}\n'
                    if url.endswith('/results/results.json'):
                        return b'{"resolved":["pass"]}'
                    if url.endswith('/fail/report.json'):
                        return b'{"fail":{"resolved":false,"patch_exists":true,"patch_successfully_applied":true}}'
                    raise AssertionError('unexpected request: ' + url)
                with patch('parsimony.artifacts._bytes', side_effect=fetch):
                    loaded = load_submission(submission, None, include_failed=True)
                prefix = f'https://raw.githubusercontent.com/submitter/artifacts/{expected_ref}/run'
                self.assertIn(prefix + '/all_preds.jsonl', requested)
                self.assertIn(prefix + '/logs/fail/report.json', requested)
                self.assertEqual(loaded['provenance']['artifact_ref'], expected_ref)
                self.assertEqual(loaded['provenance']['metadata_ref'], 'main')
                self.assertEqual(loaded['result_details']['unresolved'], ['fail'])

    def test_invalid_info_commit_rejected_before_artifact_requests(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        for value in ('main', 'abc123', 'g' * 40, 'a' * 39, 'a' * 41, 'null', '~', '', '../main'):
            with self.subTest(commit=value):
                metadata = (f'info:\n  commit: {value}\nassets:\n'
                            '  repo: https://github.com/submitter/artifacts\n'
                            '  ref: main\n').encode()
                with patch('parsimony.artifacts._bytes', return_value=metadata) as fetch:
                    with self.assertRaisesRegex(ValueError, 'info.commit.*40-character'):
                        load_submission(submission, None, task_ids=[])
                self.assertEqual(fetch.call_count, 1)

    def test_info_commit_scalar_subset(self):
        from parsimony.artifacts import _metadata_scalars
        commit = 'A' * 40
        for indent in ('  ', '    '):
            metadata = (f'info:\n{indent}authors: [one, two]\n{indent}commit: \'{commit}\'\n'
                        'assets:\n  logs: logs\n').encode()
            self.assertEqual(_metadata_scalars(metadata), {'info.commit': commit, 'logs': 'logs'})
        self.assertEqual(_metadata_scalars(f'info:\n  nested:\n    commit: {commit}\n'.encode()), {})
        with self.assertRaisesRegex(ValueError, 'duplicate info YAML key'):
            _metadata_scalars(f'info:\n  commit: {commit}\n  commit: {commit}\n'.encode())

    def test_submitter_assets_default_to_logs_and_missing_is_not_failure(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        def fetch(url, _cache):
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return b'assets:\n  repo: https://github.com/submitter/repo\n  logs: null\n'
            if url.endswith('/per_instance_details.json'):
                return b'{"gone":{"resolved":true},"no-log":{"resolved":false,"status":"no_logs"}}'
            if url.endswith('/gone/patch.diff'):
                raise HTTPError(url, 404, 'missing', {}, None)
            raise AssertionError('unexpected request: ' + url)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            loaded = load_submission(submission, Cache(tempfile.mkdtemp()))
        self.assertEqual(loaded['result_details']['missing_patch'], ['gone'])
        self.assertEqual(loaded['result_details']['no_logs'], ['no-log'])
        self.assertNotIn('no-log', loaded['predictions'])
        self.assertEqual(loaded['prediction_locations']['gone'],
                         'https://raw.githubusercontent.com/submitter/repo/main/logs/gone/patch.diff')

    def test_unsupported_assets_yaml_fails_clearly(self):
        from parsimony.artifacts import _metadata_scalars
        with self.assertRaisesRegex(ValueError, 'unsupported assets YAML'):
            _metadata_scalars(b'assets:\n  repo: [not, a, scalar]\n')

    def test_current_layout_selection_and_missing_patch(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        metadata = b'assets:\n  logs: s3://swe-bench-submissions/bash-only/demo/logs\n'
        details = json.dumps({'b': {'resolved': False}, 'a': {'resolved': True},
                              'c': {'resolved': True}}).encode()
        def fetch(url, _cache):
            if '?list-type=2' in url:
                return b'<KeyCount>1</KeyCount>'
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
            if '?list-type=2' in url:
                return b'<KeyCount>1</KeyCount>'
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

    def test_current_layout_fetches_only_explicit_failures_when_opted_in(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        requested = []
        def fetch(url, _cache):
            if '?list-type=2' in url:
                return b'<KeyCount>1</KeyCount>'
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return b'assets:\n  logs: s3://swe-bench-submissions/bash-only/demo/logs\n'
            if url.endswith('/per_instance_details.json'):
                return (b'{"ok":{"resolved":true},"failed":{"resolved":false},'
                        b'"nolog":{"resolved":false,"status":"no_logs"},'
                        b'"nogeneration":{"resolved":false,"status":"no_generation"}}')
            requested.append(url)
            if url.endswith('/ok/patch.diff'):
                return b'ok-patch'
            if url.endswith('/failed/patch.diff'):
                return b'failed-patch'
            raise AssertionError('unexpected download: ' + url)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            loaded = load_submission(submission, Cache(tempfile.mkdtemp()), include_failed=True)
        self.assertEqual(loaded['predictions'], {'ok': 'ok-patch', 'failed': 'failed-patch'})
        self.assertEqual(loaded['result_details']['unresolved'], ['failed'])
        self.assertEqual(loaded['result_details']['no_logs'], ['nolog'])
        self.assertEqual(loaded['result_details']['no_generation'], ['nogeneration'])
        self.assertFalse(any('/nolog/' in url or '/nogeneration/' in url for url in requested))

    def test_current_layout_falls_back_to_standard_logs_folder(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        def fetch(url, _cache):
            if '?list-type=2' in url:
                return b'<KeyCount>1</KeyCount>' if 'prefix=bash-only/demo/logs/a/' in url else b'<KeyCount>0</KeyCount>'
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return b'assets:\n  logs: s3://swe-bench-submissions/bash-only/demo\n'
            if url.endswith('/per_instance_details.json'):
                return b'{"a": {"resolved": true}}'
            if url == 'https://swe-bench-submissions.s3.amazonaws.com/bash-only/demo/logs/a/patch.diff':
                return b'patch-a'
            raise AssertionError('unexpected download: ' + url)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            loaded = load_submission(submission, Cache(tempfile.mkdtemp()))
        self.assertEqual(loaded['predictions'], {'a': 'patch-a'})
        self.assertEqual(loaded['provenance']['logs_source'], 'standard-folder')

    def test_current_layout_rejects_empty_logs_folders(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        def fetch(url, _cache):
            if '?list-type=2' in url:
                return b'<KeyCount>0</KeyCount>'
            if url.endswith('/all_preds.jsonl'):
                raise HTTPError(url, 404, 'missing', {}, None)
            if url.endswith('/metadata.yaml'):
                return b'assets:\n  logs: s3://swe-bench-submissions/bash-only/Other-Run/logs\n'
            if url.endswith('/per_instance_details.json'):
                return b'{"a": {"resolved": true}}'
            raise AssertionError('unexpected download: ' + url)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            with self.assertRaisesRegex(ValueError, 'no standard logs folder'):
                load_submission(submission, Cache(tempfile.mkdtemp()))

    def test_current_layout_requires_real_boolean(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/main/evaluation/verified/demo'
        def fetch(url, _cache):
            if '?list-type=2' in url:
                return b'<KeyCount>1</KeyCount>'
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

    def test_legacy_failures_come_from_explicit_reports(self):
        s3 = 'https://swe-bench-submissions.s3.amazonaws.com/verified/demo'
        preds = b''.join(json.dumps({'instance_id': t, 'model_patch': 'p'}).encode() + b'\n'
                         for t in ('ok', 'failed', 'unapplied', 'noreport', 'nogen'))
        requested = []
        def fetch(url, _cache):
            if '?list-type=2' in url:
                return b'<KeyCount>1</KeyCount>'
            if url.endswith('/all_preds.jsonl'):
                return preds
            if url.endswith('/results/results.json'):
                return b'{"resolved": ["ok"], "no_generation": ["nogen"], "no_logs": []}'
            if url.endswith('/report.json'):
                requested.append(url)
            task = url.split('/')[-2]
            if task == 'noreport':
                raise HTTPError(url, 404, 'missing', {}, None)
            return json.dumps({task: {'resolved': False, 'patch_exists': True,
                                      'patch_successfully_applied': task != 'unapplied'}}).encode()
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            plain = load_submission('demo', None)
            self.assertNotIn('unresolved', plain['result_details'])
            self.assertEqual(requested, [])
            loaded = load_submission('demo', None, include_failed=True)
            self.assertEqual(loaded['result_details']['unresolved'], ['failed'])
            self.assertEqual(loaded['result_details']['no_report'], ['noreport', 'unapplied'])
            self.assertEqual(requested, [f'{s3}/logs/{t}/report.json' for t in ('failed', 'noreport', 'unapplied')])
            self.assertIn('failed', loaded['evaluated'])
            requested.clear()
            load_submission('demo', None, task_ids=['failed'], include_failed=True)
            self.assertEqual(requested, [f'{s3}/logs/failed/report.json'])

    def test_official_monolithic_assets_and_independent_refs(self):
        submission = 'https://github.com/SWE-bench/experiments/tree/abc123/evaluation/verified/demo'
        requested = []
        def fetch(url, _cache):
            requested.append(url)
            if url.endswith('/metadata.yaml'):
                return b'assets:\n  repo: https://github.com/submitter/artifacts\n'
            if url.endswith('/all_preds.jsonl'):
                return b'{"instance_id":"ok","patch":"p"}\n{"instance_id":"bad","patch":"q"}\n'
            if url.endswith('/results/results.json'):
                return b'{"resolved":["ok"]}'
            if url.endswith('/bad/report.json'):
                return b'{"bad":{"resolved":false,"patch_exists":true,"patch_successfully_applied":true}}'
            raise AssertionError(url)
        with patch('parsimony.artifacts._bytes', side_effect=fetch):
            loaded = load_submission(submission, Cache(tempfile.mkdtemp()), include_failed=True)
        self.assertEqual(loaded['predictions'], {'ok': 'p', 'bad': 'q'})
        self.assertEqual(loaded['result_details']['unresolved'], ['bad'])
        self.assertEqual(loaded['provenance']['metadata_ref'], 'abc123')
        self.assertEqual(loaded['provenance']['artifact_ref'], 'main')
        self.assertIn('https://raw.githubusercontent.com/submitter/artifacts/main/all_preds.jsonl', requested)
        self.assertIn('https://raw.githubusercontent.com/SWE-bench/experiments/abc123/evaluation/verified/demo/results/results.json', requested)

    def test_github_logs_must_match_declared_repo(self):
        from parsimony.artifacts import _github_asset
        with self.assertRaisesRegex(ValueError, 'must use the assets.repo'):
            _github_asset('https://github.com/other/repo/tree/main/logs',
                          'https://github.com/submitter/repo', 'main')

    def test_metadata_top_level_scalar_ends_assets_section(self):
        from parsimony.artifacts import _metadata_scalars
        self.assertEqual(_metadata_scalars(b'assets:\n  repo: https://github.com/a/b\nname: later\n  logs: ignored\n'),
                         {'repo': 'https://github.com/a/b'})
        with self.assertRaisesRegex(ValueError, 'duplicate assets'):
            _metadata_scalars(b'assets:\n  repo: https://github.com/a/b\n  repo: https://github.com/c/d\n')

    def test_cache(self):
        import io
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache(directory)
            with patch('parsimony.artifacts.urlopen', return_value=io.BytesIO(b'hello')) as request:
                self.assertEqual(cache.get('https://example.test/a'), b'hello')
                self.assertEqual(cache.get('https://example.test/a'), b'hello')
                self.assertEqual(request.call_count, 1)
