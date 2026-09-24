import hashlib
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

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
