"""Safety controls for the static, frozen-input Go remeasurement driver."""
import hashlib
import importlib.util
import io
import json
import tarfile
from pathlib import Path
import tempfile
import unittest

from parsimony.artifacts import Cache

PATH = Path(__file__).resolve().parents[1] / 'examples/benchmark-discovery/remeasure-go.py'
spec = importlib.util.spec_from_file_location('go_remeasurement', PATH)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


fetch_spec = importlib.util.spec_from_file_location('go_release_fetch', PATH.with_name('fetch-go-v2-release.py'))
fetch = importlib.util.module_from_spec(fetch_spec)
fetch_spec.loader.exec_module(fetch)


class GoReleaseDownloadTests(unittest.TestCase):
    def archive(self, members):
        stream = io.BytesIO()
        files = {}
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            for name, data, kind in members:
                member = tarfile.TarInfo(name)
                member.size = len(data)
                member.type = kind
                archive.addfile(member, io.BytesIO(data))
                files[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        raw = stream.getvalue()
        return raw, {'archive_bytes': len(raw), 'archive_sha256': hashlib.sha256(raw).hexdigest(), 'files': files}

    def test_verified_scalar_download_is_idempotent(self):
        raw, manifest = self.archive([('model.jsonl', b'{}\n', tarfile.REGTYPE)])
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(fetch.unpack(raw, manifest, directory), 1)
            self.assertEqual(fetch.unpack(raw, manifest, directory), 1)
            self.assertEqual((Path(directory) / 'model.jsonl').read_bytes(), b'{}\n')
            with self.assertRaisesRegex(ValueError, 'archive checksum'):
                fetch.unpack(raw + b'x', manifest, directory)

    def test_unsafe_members_and_incomplete_membership_are_rejected(self):
        for name, kind in [('../escape', tarfile.REGTYPE), ('symlink', tarfile.SYMTYPE),
                           ('directory', tarfile.DIRTYPE)]:
            raw, manifest = self.archive([(name, b'', kind)])
            with tempfile.TemporaryDirectory() as directory, self.assertRaisesRegex(ValueError, 'unsafe'):
                fetch.unpack(raw, manifest, directory)
        raw, manifest = self.archive([('a.json', b'{}', tarfile.REGTYPE)])
        manifest['files']['missing.json'] = manifest['files']['a.json']
        with tempfile.TemporaryDirectory() as directory, self.assertRaisesRegex(ValueError, 'membership'):
            fetch.unpack(raw, manifest, directory)

    def test_conflicts_are_detected_before_any_new_file_is_written(self):
        raw, manifest = self.archive([('new.json', b'{}', tarfile.REGTYPE),
                                      ('existing.json', b'{}', tarfile.REGTYPE)])
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing.json'
            target.write_bytes(b'other')
            with self.assertRaisesRegex(ValueError, 'existing file differs'):
                fetch.unpack(raw, manifest, directory)
            self.assertEqual(target.read_bytes(), b'other')
            self.assertFalse((Path(directory) / 'new.json').exists())


class GoRemeasurementTests(unittest.TestCase):
    def test_immutable_files_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'release/record.json'
            driver.dump(path, {'n': 1})
            original = path.read_bytes()
            driver.dump(path, {'n': 1})
            with self.assertRaisesRegex(ValueError, 'refusing changed'):
                driver.dump(path, {'n': 2})
            self.assertEqual(path.read_bytes(), original)
            with self.assertRaises(ValueError):
                driver.dump(path, {'n': float('nan')})
            self.assertEqual(path.read_bytes(), original)

    def test_offline_cache_checks_hash_and_size_without_fetch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = driver.cache_class(Cache)(root, offline=True)
            url = 'https://example.org/patch.diff'
            with self.assertRaisesRegex(ValueError, 'offline cache miss'):
                cache.get(url)
            data = b'patch bytes'
            driver.immutable(root / 'cache' / driver.digest(url.encode()), data)
            self.assertEqual(cache.get(url, driver.digest(data)), data)
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                cache.get(url, '0' * 64)
            with self.assertRaisesRegex(ValueError, 'exceeds bound'):
                cache.get(url, bound=2)

    def test_cache_output_must_be_external(self):
        repo = Path('/tmp/example-checkout')
        with self.assertRaisesRegex(ValueError, 'outside checkout'):
            driver.external(repo / 'cache', repo)
        driver.external(Path('/tmp/independent-cache'), repo)

    def test_path_inventory_covers_new_and_metadata_only_files(self):
        patch = ('diff --git a/a.go b/a.go\n--- /dev/null\n+++ b/a.go\n'
                 '@@ -0,0 +1 @@\n+package p\n'
                 'diff --git a/b.go b/c.go\nrename from b.go\nrename to c.go\n')
        self.assertEqual(driver.touched(patch), [
            {'old': '/dev/null', 'new': 'a.go'}, {'old': 'b.go', 'new': 'c.go'}])
        for path in ('../escape.go', '/escape.go', 'a b.go', '"a.go"'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                driver.touched(f'--- a/{path}\n+++ b/{path}\n')

    def test_comparison_retains_nested_metric_and_binding_changes(self):
        before = {'metrics': {'net_units': 2}, 'old_only': None}
        after = {'metrics': {'net_units': 3}, 'new_only': 'value'}
        changes = driver.differences(before, after)
        self.assertEqual(changes['metrics.net_units'], {'old': 2, 'new': 3})
        self.assertFalse(changes['new_only']['old_present'])
        self.assertFalse(changes['old_only']['new_present'])
        self.assertEqual(driver.differences(before, json.loads(json.dumps(before))), {})
