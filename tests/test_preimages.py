import unittest

from parsimony.preimages import audit_record, audit_run, blob_hash


class Cache:
    def __init__(self, raw=b'x = 1\n'):
        self.raw = raw
        self.urls = []

    def get(self, url):
        self.urls.append(url)
        return self.raw


def record(patch=None, **extra):
    prefix = blob_hash(b'x = 1\n')[:12]
    return dict(task_id='task', repo='org/repo', base_commit='a' * 40, language='python',
                published_outcome='failure', artifact_status='present',
                patch=patch if patch is not None else (
                    f'diff --git a/pkg/a.py b/pkg/a.py\nindex {prefix}..abcdef123456 100644\n'
                    '--- a/pkg/a.py\n+++ b/pkg/a.py\n@@ -1 +1 @@\n-x = 1\n+x = 2\n'), **extra)


class PreimageTests(unittest.TestCase):
    def test_full_blob_and_hunk_match_for_explicit_failure(self):
        cache = Cache()
        audit = audit_record(record(), cache)
        self.assertTrue(audit['accepted'])
        self.assertEqual(audit['status'], 'old_blobs_and_hunks_match')
        self.assertEqual(audit['sources'][0]['bytes'], 6)
        self.assertTrue(audit['sources'][0]['strict_hunks_match'])
        self.assertIn('/' + 'a' * 40 + '/pkg/a.py', cache.urls[0])

    def test_mismatching_blob_never_accepted(self):
        result = audit_record(record(), Cache(b'x = 2\n'))
        self.assertFalse(result['accepted'])
        self.assertIn('old Git blob differs', result['error'])

    def test_matching_blob_but_invalid_hunks_never_accepted(self):
        item = record()
        item['patch'] = item['patch'].replace('-x = 1', '-x = 9')
        result = audit_record(item, Cache())
        self.assertFalse(result['accepted'])
        self.assertIn('context differs', result['error'])

    def test_missing_index_keeps_context_only_distinct(self):
        item = record()
        item['patch'] = '\n'.join(line for line in item['patch'].split('\n') if not line.startswith('index '))
        result = audit_record(item, Cache())
        self.assertEqual(result['status'], 'hunks_match_without_blob_identity')
        self.assertFalse(result['accepted'])

    def test_new_files_require_no_base_fetch_but_valid_hunks(self):
        patch = 'diff --git a/pkg/new.py b/pkg/new.py\n--- /dev/null\n+++ b/pkg/new.py\n@@ -0,0 +1 @@\n+x = 2\n'
        cache = Cache()
        result = audit_record(record(patch), cache)
        self.assertTrue(result['accepted'])
        self.assertEqual(result['status'], 'new_files_only')
        self.assertEqual(cache.urls, [])

    def test_unknown_outcome_not_a_failure_and_not_fetched(self):
        item = record()
        item['published_outcome'] = 'unknown'
        cache = Cache()
        self.assertEqual(audit_record(item, cache)['status'], 'not_required')
        self.assertEqual(cache.urls, [])

    def test_fetch_errors_are_unverified(self):
        class Broken:
            def get(self, url):
                raise OSError('offline')
        result = audit_record(record(), Broken())
        self.assertFalse(result['accepted'])
        self.assertIn('offline', result['error'])

    def test_binary_and_unsafe_paths_stay_unverified(self):
        for patch in ['diff --git a/pkg/a.py b/pkg/a.py\nBinary files differ\n',
                      '--- a/../x.py\n+++ b/../x.py\n@@ -1 +1 @@\n-x\n+y\n']:
            result = audit_record(record(patch), Cache())
            self.assertFalse(result['accepted'])

    def test_inventory_retained_and_review_bound_to_artifacts(self):
        item = record()
        missing = dict(item, task_id='missing', artifact_status='missing', patch=None)
        run = dict(records=[item, missing], submission_revision='a' * 40,
                   dataset=dict(dataset_checksum='b' * 64), result_sha256='c' * 64,
                   prediction_sha256='d' * 64)
        result = audit_run(run, Cache(), workers=2)
        self.assertEqual(len(result['records']), 2)
        self.assertEqual(result['base_commit_confirmations'], {'task': 'a' * 40})
        self.assertEqual(result['prediction_sha256'], 'd' * 64)
        self.assertEqual(result['historical_dataset_match'], 'unverified')
        with self.assertRaises(ValueError):
            audit_run(run, Cache(), workers=0)


if __name__ == '__main__':
    unittest.main()
