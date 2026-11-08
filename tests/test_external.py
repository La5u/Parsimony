import copy
import hashlib
import io
import json
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

from parsimony.external import ENDPOINT, MAX_RESPONSE_BYTES, _NoRedirect, attach, fetch, main, snapshot

RAW = json.dumps({'data': [
    {'id': 'a1', 'name': 'Model A (Max)', 'slug': 'model-a', 'release_date': '2026-09-01',
     'evaluations': {'artificial_analysis_intelligence_index': 50.5, 'artificial_analysis_coding_index': 77.0}},
    {'id': 'b1', 'name': 'Model B', 'slug': 'model-b', 'release_date': '2026-08-01',
     'evaluations': {'artificial_analysis_intelligence_index': 30.0, 'artificial_analysis_coding_index': None}},
]}).encode()



def _pages():
    data = json.loads(RAW)['data']
    return [json.dumps({'tier': 'free', 'intelligence_index_version': 5.0,
                        'pagination': {'page': n, 'page_size': 1, 'total_pages': 2, 'has_more': n == 1},
                        'data': [data[n - 1]]}).encode() for n in (1, 2)]


class ExternalTest(unittest.TestCase):
    def test_duplicate_index_version_cli_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            response = Path(tmp) / 'response.json'
            response.write_bytes(RAW)
            argv = ['external', 'snapshot', 'mapping.json', '--output', 'output.json',
                    '--response', str(response), '--index-version', 'aa_intelligence=5.0',
                    '--index-version', 'aa_intelligence=6.0']
            with patch('sys.argv', argv), patch('sys.stderr', new_callable=io.StringIO) as stderr:
                with self.assertRaises(SystemExit) as exc:
                    main()
            self.assertEqual(exc.exception.code, 1)
            self.assertEqual(stderr.getvalue(), "error: --index-version 'aa_intelligence' given twice\n")

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
        self.assertEqual(snap['response_sha256'], hashlib.sha256(RAW).hexdigest())
        self.assertNotIn('Model A (Max)', json.dumps(snap['configurations']['agent-c']))

    def test_snapshot_rejects_unknown_ids_and_match_types(self):
        with self.assertRaises(ValueError):
            snapshot({'configurations': {'x': {'aa_id': 'zz', 'match': 'exact'}}}, RAW, 't')
        with self.assertRaises(ValueError):
            snapshot({'configurations': {'x': {'aa_id': 'a1', 'match': 'similar'}}}, RAW, 't')

    def test_response_validation(self):
        original = json.loads(RAW)
        invalid = [None, [], {}, {'data': {}}, {'data': [None]}]
        duplicate = copy.deepcopy(original)
        duplicate['data'].append(copy.deepcopy(duplicate['data'][0]))
        invalid.append(duplicate)
        for field, value in [('id', []), ('id', ''), ('name', None), ('slug', ''),
                             ('evaluations', None)]:
            response = copy.deepcopy(original)
            response['data'][0][field] = value
            invalid.append(response)
        for response in invalid:
            with self.subTest(response=response), self.assertRaises(ValueError):
                snapshot({'configurations': {}}, json.dumps(response).encode(), 't')

    def test_indices_require_finite_numbers_or_null(self):
        for value in [True, False, '50', [], {}, float('nan'), float('inf'), -float('inf')]:
            response = json.loads(RAW)
            response['data'][0]['evaluations']['artificial_analysis_coding_index'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                snapshot({'configurations': {}}, json.dumps(response).encode(), 't')
        response = json.loads(RAW)
        response['data'][0]['evaluations'] = {'artificial_analysis_coding_index': -2}
        snap = snapshot({'configurations': {'x': {'aa_id': 'a1', 'match': 'exact'}}},
                        json.dumps(response).encode(), 't')
        self.assertEqual(snap['configurations']['x']['aa_coding'], -2)
        self.assertIsNone(snap['configurations']['x']['aa_intelligence'])

    def test_mapping_validation(self):
        invalid = [None, [], {}, {'configurations': []}]
        for entry in [None, [], {}, {'reason': 'missing id'}, {'aa_id': None},
                      {'aa_id': None, 'reason': ''}, {'aa_id': []},
                      {'aa_id': 'a1', 'match': []}]:
            invalid.append({'configurations': {'x': entry}})
        invalid.append({'configurations': {'': {'aa_id': None, 'reason': 'unmapped'}}})
        for mapping in invalid:
            with self.subTest(mapping=mapping), self.assertRaises(ValueError):
                snapshot(mapping, RAW, 't')

    def test_attach_rejects_invalid_values_before_mutating(self):
        base = snapshot({'configurations': {'x': {'aa_id': 'a1', 'match': 'exact'}}}, RAW, 't')
        for value in [True, '12', float('nan'), float('inf')]:
            snap = copy.deepcopy(base)
            snap['configurations']['x']['aa_coding'] = value
            models = [{'agent': 'other', 'aa_coding': 123}, {'agent': 'x'}]
            before = copy.deepcopy(models)
            with self.subTest(value=value), self.assertRaises(ValueError):
                attach(models, snap)
            self.assertEqual(models, before)
        base['configurations']['x']['aa_id'] = None
        with self.assertRaises(ValueError):
            attach([], base)

    def test_fetch_is_bounded_and_sets_headers(self):
        with patch('parsimony.external.urllib.request.build_opener') as build:
            opener = build.return_value
            opener.open.side_effect = [io.BytesIO(page) for page in _pages()]
            merged = json.loads(fetch('secret-test-key'))
            self.assertEqual(merged, {'tier': 'free', 'intelligence_index_version': 5.0,
                                      'data': json.loads(RAW)['data']})
            urls = [call.args[0].full_url for call in opener.open.call_args_list]
            self.assertEqual(urls, [f'{ENDPOINT}?page=1', f'{ENDPOINT}?page=2'])
            request = opener.open.call_args.args[0]
            self.assertEqual(request.get_header('X-api-key'), 'secret-test-key')
            self.assertEqual(opener.open.call_args.kwargs['timeout'], 60)
            self.assertIsInstance(build.call_args.args[0], _NoRedirect)
            opener.open.side_effect = [io.BytesIO(b'x' * (MAX_RESPONSE_BYTES + 1))]
            with self.assertRaisesRegex(ValueError, 'size limit'):
                fetch('secret-test-key')

    def test_fetch_rejects_inconsistent_or_endless_pages(self):
        first, second = _pages()
        changed = json.loads(second)
        changed['intelligence_index_version'] = 5.1
        skipped = json.loads(second)
        skipped['pagination']['page'] = 3
        endless = json.loads(first)
        cases = [(json.dumps(changed).encode(), 'changed between pages'),
                 (json.dumps(skipped).encode(), 'unexpected pagination')]
        with patch('parsimony.external.urllib.request.build_opener') as build:
            opener = build.return_value
            for page, message in cases:
                opener.open.side_effect = [io.BytesIO(first), io.BytesIO(page)]
                with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                    fetch('secret-test-key')

            def page_n(request, timeout):
                endless['pagination']['page'] = int(request.full_url.rsplit('=', 1)[1])
                return io.BytesIO(json.dumps(endless).encode())
            opener.open.side_effect = page_n
            with self.assertRaisesRegex(ValueError, 'more than'):
                fetch('secret-test-key')

    def test_redirects_cannot_forward_api_key(self):
        request = urllib.request.Request(ENDPOINT, headers={'x-api-key': 'secret-test-key'})
        handler = _NoRedirect()
        for status in [301, 302, 303, 307, 308]:
            with self.subTest(status=status):
                self.assertIsNone(handler.redirect_request(
                    request, None, status, 'redirect', {}, 'https://other.example/'))
                self.assertIsNone(handler.http_error_302(
                    request, io.BytesIO(), status, 'redirect',
                    {'location': 'https://other.example/'}))

    def test_fetch_rejects_invalid_keys_without_network_access(self):
        with patch('parsimony.external.urllib.request.build_opener') as build:
            for key in [None, '', ' ', 'secret\rvalue', 'secret\nvalue']:
                with self.subTest(key=key), self.assertRaises(ValueError):
                    fetch(key)
            build.assert_not_called()

    def test_index_versions_are_validated_and_carried_to_the_site(self):
        mapping = {'configurations': {'agent-a': {'aa_id': 'a1', 'match': 'exact'}}}
        self.assertNotIn('index_versions', snapshot(mapping, RAW, 't'))
        for versions in [{'aa_unknown': '5.0'}, {'aa_intelligence': ''}, {'aa_intelligence': 5}]:
            with self.subTest(versions=versions), self.assertRaises(ValueError):
                snapshot(mapping, RAW, 't', versions)
        snap = snapshot(mapping, RAW, 't', {'aa_intelligence': '5.0'})
        self.assertEqual(attach([{'agent': 'agent-a'}], snap)['index_versions'], {'aa_intelligence': '5.0'})

    def test_index_version_is_taken_from_the_response(self):
        mapping = {'configurations': {'agent-a': {'aa_id': 'a1', 'match': 'exact'}}}
        response = dict(json.loads(RAW), tier='free', intelligence_index_version=5)
        raw = json.dumps(response).encode()
        self.assertEqual(snapshot(mapping, raw, 't')['index_versions'], {'aa_intelligence': '5.0'})
        self.assertEqual(snapshot(mapping, raw, 't', {'aa_intelligence': '5.0'})['index_versions'],
                         {'aa_intelligence': '5.0'})
        with self.assertRaisesRegex(ValueError, 'differs from the response'):
            snapshot(mapping, raw, 't', {'aa_intelligence': '4.0'})
        for version in [True, '5.0', 0, float('nan')]:
            response['intelligence_index_version'] = version
            with self.subTest(version=version), self.assertRaises(ValueError):
                snapshot(mapping, json.dumps(response).encode(), 't')

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
