import hashlib
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from parsimony.snapshot import create, key, referenced_urls, restore


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.record = dict(task_id='t', metrics={'touched_files': ['pkg/a b.py']}, human_metrics=None,
                           provenance=dict(repo='org/repo', base_commit='abc',
                                           results_url='https://x/results.json',
                                           patch_location='https://x/all_preds.jsonl#instance_id=t',
                                           failure_reports='https://x/logs/<task>/report.json'))
        self.results = self.root / 'results.jsonl'
        self.results.write_text(json.dumps(self.record) + '\n')
        self.cache = self.root / 'cache'
        self.cache.mkdir()
        for url in ('https://x/results.json', 'https://x/all_preds.jsonl',
                    'https://raw.githubusercontent.com/org/repo/abc/pkg/a%20b.py', 'https://unrelated'):
            (self.cache / key(url)).write_bytes(url.encode())

    def test_references(self):
        urls = referenced_urls([self.record])
        self.assertIn('https://x/all_preds.jsonl', urls)
        self.assertIn('https://x/logs/t/report.json', urls)
        self.assertIn('https://raw.githubusercontent.com/org/repo/abc/pkg/a%20b.py', urls)

    def test_errored_record_sources_come_from_cached_patch(self):
        errored = dict(task_id='e', metrics=None, analysis_status='error',
                       provenance=dict(repo='org/repo', base_commit='abc', patch_location='https://x/e/patch.diff'))
        (self.cache / key('https://x/e/patch.diff')).write_text(
            '--- a/pkg/old.py\n+++ b/pkg/new.py\n@@ -1 +1 @@\n-x\n+y\n')
        self.assertIn('https://raw.githubusercontent.com/org/repo/abc/pkg/old.py',
                      referenced_urls([errored], self.cache))

    def test_shared_predictions_are_parsed_once_per_reference_scan(self):
        from parsimony.artifacts import _parse_predictions
        url = 'https://x/all_preds.jsonl'
        records = []
        predictions = []
        for task in ('a', 'b'):
            records.append(dict(task_id=task, metrics=None, provenance=dict(
                repo='org/repo', base_commit='abc',
                patch_location=url + '#instance_id=' + task)))
            predictions.append(dict(instance_id=task, patch=(
                f'--- a/{task}.py\n+++ b/{task}.py\n@@ -1 +1 @@\n-x\n+y\n')))
        cached = self.cache / key(url)
        cached.write_text('\n'.join(json.dumps(p) for p in predictions))
        with patch('parsimony.snapshot._parse_predictions', wraps=_parse_predictions) as parse:
            urls = referenced_urls(records, self.cache)
        self.assertEqual(parse.call_count, 1)
        for task in ('a', 'b'):
            self.assertIn(f'https://raw.githubusercontent.com/org/repo/abc/{task}.py', urls)
        # Memoization must not leak across scans or hide a subsequently changed file.
        cached.write_text(json.dumps(dict(instance_id='a', patch='')))
        urls = referenced_urls(records, self.cache)
        self.assertNotIn('https://raw.githubusercontent.com/org/repo/abc/a.py', urls)

    def test_create_accepts_result_path_iterator_and_keeps_hashes(self):
        archive = self.root / 'iterator.tar.gz'
        create(iter([self.results]), self.cache, archive)
        with tarfile.open(archive) as tar:
            manifest = json.load(tar.extractfile('manifest.json'))
        self.assertEqual(manifest['results_sha256'], {
            str(self.results): hashlib.sha256(self.results.read_bytes()).hexdigest()})

    def test_restore_replace_failure_cleans_unique_temporary_file(self):
        archive = self.root / 'snap.tar.gz'
        create([self.results], self.cache, archive)
        fresh = self.root / 'fresh'
        fresh.mkdir()
        # A stale temporary file from an older restore must not be overwritten.
        with tarfile.open(archive) as tar:
            first = json.load(tar.extractfile('manifest.json'))['entries'][0]
        stale = fresh / (key(first['url']) + '.restoring')
        stale.write_bytes(b'keep')
        with patch('parsimony.snapshot.os.replace', side_effect=OSError('failed')):
            with self.assertRaisesRegex(OSError, 'failed'):
                restore(archive, fresh)
        self.assertEqual(list(fresh.iterdir()), [stale])
        self.assertEqual(stale.read_bytes(), b'keep')
        self.assertEqual(restore(archive, fresh)['restored'], 3)
        self.assertEqual(stale.read_bytes(), b'keep')

    def test_round_trip_only_referenced_and_verified(self):
        archive = self.root / 'snap.tar.gz'
        summary = create([self.results], self.cache, archive)
        self.assertEqual(summary['files'], 3)  # not the unrelated entry
        fresh = self.root / 'fresh'
        self.assertEqual(restore(archive, fresh), dict(restored=3, already_present=0))
        self.assertEqual(restore(archive, fresh), dict(restored=0, already_present=3))
        self.assertFalse((fresh / key('https://unrelated')).exists())
        (fresh / key('https://x/results.json')).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'existing cache entry differs'):
            restore(archive, fresh)

    def test_incorrect_size_and_non_regular_cache_members_rejected(self):
        import io
        url = 'https://x/entry'
        data = b'content'
        for kind in ('size', 'symlink'):
            with self.subTest(kind=kind):
                archive = self.root / (kind + '.tar.gz')
                manifest = dict(format='parsimony-cache-snapshot-v1', entries=[dict(
                    url=url, size=len(data) + (kind == 'size'),
                    sha256=hashlib.sha256(data).hexdigest())])
                with tarfile.open(archive, 'w:gz') as tar:
                    payload = json.dumps(manifest).encode()
                    info = tarfile.TarInfo('manifest.json')
                    info.size = len(payload)
                    tar.addfile(info, io.BytesIO(payload))
                    info = tarfile.TarInfo('cache/' + key(url))
                    if kind == 'symlink':
                        info.type = tarfile.SYMTYPE
                        info.linkname = 'manifest.json'
                        tar.addfile(info)
                    else:
                        info.size = len(data)
                        tar.addfile(info, io.BytesIO(data))
                fresh = self.root / ('fresh-' + kind)
                with self.assertRaisesRegex(ValueError, 'size differs|not a regular file'):
                    restore(archive, fresh)
                self.assertEqual(list(fresh.iterdir()), [])

    def test_tampered_snapshot_rejected(self):
        archive = self.root / 'snap.tar.gz'
        create([self.results], self.cache, archive)
        with tarfile.open(archive) as tar:
            manifest = json.load(tar.extractfile('manifest.json'))
        manifest['entries'][0]['sha256'] = hashlib.sha256(b'other').hexdigest()
        bad = self.root / 'bad.tar.gz'
        with tarfile.open(archive) as src, tarfile.open(bad, 'w:gz') as dst:
            for member in src.getmembers():
                data = src.extractfile(member).read()
                if member.name == 'manifest.json':
                    data = json.dumps(manifest).encode()
                    member.size = len(data)
                import io
                dst.addfile(member, io.BytesIO(data))
        with self.assertRaisesRegex(ValueError, 'differs from manifest'):
            restore(bad, self.root / 'other')


if __name__ == '__main__':
    unittest.main()
