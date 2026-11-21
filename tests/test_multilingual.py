import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from parsimony import multilingual as ml
from parsimony.benchmark import read_jsonl
from parsimony.site import label
from tests.test_deepswe import FakeCache

ENTRY = '20260213_mini-v2.0.0a0_claude-4-6-opus'
METADATA = b'info:\n  mini-swe-agent_version: 2.0.0a0\n  name: Claude 4.6 Opus\ntags:\n  name: ignored\n'


def task(instance, repo, *paths):
    return dict(instance_id=instance, repo=repo, base_commit='abc',
                patch=''.join(f'diff --git a/{p} b/{p}\n--- a/{p}\n+++ b/{p}\n@@ -1 +1 @@\n-old\n+new\n'
                              for p in paths))


def official_cache(outcomes, patches):
    base = f'{ml.EXPERIMENTS}/{ENTRY}'
    return FakeCache({f'{base}/metadata.yaml': METADATA,
                      f'{base}/per_instance_details.json': json.dumps(outcomes).encode(),
                      **{f'{ml.BUCKET}/{ENTRY}/logs/{item}/patch.diff': data for item, data in patches.items()}})


class MultilingualTests(unittest.TestCase):
    def test_each_repo_uses_its_dominant_non_test_source_language(self):
        tasks = [task('a', 'owner/mixed', 'src/a.tsx', 'tests/a.php', 'src/a_test.go'),
                 task('b', 'owner/mixed', 'src/b.ts', 'src/b.js'),
                 task('c', 'owner/mixed', 'README.md'), task('d', 'owner/rust', 'src/d.rs'),
                 task('e', 'owner/js', 'src/e.js', 'src/e.d.ts'), task('f', 'owner/cpp', 'include/f.hpp')]
        self.assertEqual(ml.repo_languages(tasks), {'owner/mixed': 'typescript', 'owner/rust': 'rust',
                                                     'owner/js': 'javascript', 'owner/cpp': 'c/c++'})
        for paths in [('README.md',), ('a.ts', 'b.go')]:
            with self.assertRaisesRegex(ValueError, 'owner/ambiguous: no unique source language'):
                ml.repo_languages([task('g', 'owner/ambiguous', *paths)])

    def test_parquet_generates_one_item_per_task_with_reference_patch(self):
        try:
            import pyarrow as pa
            import pyarrow.parquet as parquet
        except ImportError:
            self.skipTest('optional pyarrow dependency is unavailable')
        go = task('a', 'owner/go', 'a.go')
        docs = task('b', 'owner/go', 'README.md')
        tasks = [go, docs, task('c', 'owner/php', 'src/c.php'), task('d', 'owner/java', 'src/D.java')]
        with tempfile.TemporaryDirectory() as tmp, patch('builtins.print') as report:
            path = Path(tmp, 'tasks.parquet')
            parquet.write_table(pa.Table.from_pylist([dict(row, test_patch='ignored') for row in tasks]), path)
            rows = ml.dataset(path, 'go')
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(rows, [dict(row, instance_id=row['instance_id'] + '#1', language='go',
                                     dataset_file_sha256=digest) for row in [go, docs]])
        self.assertTrue(any('owner/java' in call.args[0] and '(excluded)' in call.args[0]
                            for call in report.call_args_list))

    def test_official_submission_uses_pinned_metadata_and_only_fetches_evaluated_items(self):
        outcomes = {task_id: dict(resolved=task_id in ('a', 'c')) for task_id in ('a', 'b', 'c', 'other')}
        cache = official_cache(outcomes, {'a': b'diff a', 'b': b'\n '})
        sub = ml.load_submission(ENTRY, cache, {'a#1', 'b#1', 'c#1', 'no-log#1'})
        self.assertEqual(sub['agent'], ml.PREFIX + ENTRY)
        self.assertEqual(sub['evaluated'], {'a#1', 'b#1', 'c#1'})
        self.assertEqual(sub['resolved'], {'a#1', 'c#1'})
        self.assertEqual(sub['predictions'], {'a#1': 'diff a'})
        self.assertEqual(sub['result_details'], dict(resolved=['a#1', 'c#1'], unresolved=['b#1'],
                                                     no_logs=['no-log#1'], missing_patch=['b#1', 'c#1']))
        self.assertIn(ml.EXPERIMENTS_COMMIT, sub['provenance']['results_url'])
        self.assertEqual(sub['provenance']['harness_version'], '2.0.0a0')
        self.assertEqual(sub['provenance']['reported_model'], 'Claude 4.6 Opus')
        self.assertEqual(len(cache.requested), 6)  # c also tries its trajectory
        self.assertEqual(label(sub['agent']), 'Claude Opus 4.6 · mini-SWE-agent 2.0')

    def test_missing_log_patch_falls_back_to_trajectory_submission(self):
        cache = official_cache({'a': dict(resolved=True)}, {})
        url = f'{ml.BUCKET}/{ENTRY}/trajs/a/a.traj.json'
        cache.files[url] = json.dumps(dict(info=dict(submission='diff t'))).encode()
        sub = ml.load_submission(ENTRY, cache, {'a#1'})
        self.assertEqual(sub['predictions'], {'a#1': 'diff t'})
        self.assertEqual(sub['prediction_locations'], {'a#1': url + '#info.submission'})

    def test_rusta_submission_reads_local_results_and_verifies_optional_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp, 'glm')
            root.mkdir()
            predictions = [dict(instance_id=t, model_patch=p) for t, p in [('a', 'diff a'), ('b', 'diff b'), ('c', '')]]
            results = dict(a=dict(resolved=True, patch_applied=True), b=dict(resolved=False, patch_applied=False),
                           c=dict(resolved=False, reason='empty patch'), d=dict(resolved=False, reason='no prediction'))
            raw = ''.join(json.dumps(row) + '\n' for row in predictions).encode()
            (root / 'all_preds.jsonl').write_bytes(raw)
            (root / 'results.json').write_text(json.dumps(results))
            archive = Path(tmp, 'release.tar.gz')
            archive.write_bytes(b'archive')
            cache = FakeCache({})
            items = {f'{t}#1' for t in results}
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                ml.load_submission('rusta-glm', cache, items, tmp, archive)
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            with patch.object(ml, 'RUSTA_SHA256', digest):
                sub = ml.load_submission('rusta-glm', cache, items, tmp, archive)
            self.assertFalse(ml.load_submission('rusta-glm', cache, items, tmp)['provenance']['release_sha256_verified'])
        self.assertEqual(cache.requested, [])
        self.assertEqual(sub['evaluated'], items)
        self.assertEqual(sub['resolved'], {'a#1'})
        self.assertEqual(sub['predictions'], {'a#1': 'diff a', 'b#1': 'diff b'})
        self.assertEqual(sub['result_details']['missing_patch'], ['c#1', 'd#1'])
        self.assertEqual(sub['provenance']['release_sha256'], digest)
        self.assertTrue(sub['provenance']['release_sha256_verified'])
        self.assertEqual(sub['provenance']['prediction_sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(sub['provenance']['reported_model'], 'glm-5.3')
        self.assertEqual(label(sub['agent']), 'GLM-5.3 (max) · Rusta 1.0.0')

    def test_analyze_cli_includes_failed_items_and_retries_base_fetches(self):
        reference = task('a', 'owner/go', 'source.go')
        row = dict(reference, instance_id='a#1', language='go')
        missing = dict(row, instance_id='b#1')
        cache = official_cache({'a': dict(resolved=False), 'b': dict(resolved=True)}, {'a': row['patch'].encode()})
        source = 'https://raw.githubusercontent.com/owner/go/abc/source.go'

        def get(url):
            if url == source and url not in cache.requested:
                cache.requested.append(url)
                raise ConnectionResetError('retry me')
            return FakeCache.get(cache, url)

        cache.files[source] = b'old\n'
        cache.get = get

        def measure(patch_text, get_source, language):
            self.assertEqual(get_source('source.go'), 'old\n')
            self.assertEqual(patch_text, reference['patch'])
            self.assertEqual(language, 'go')
            return dict(churn=2)

        with tempfile.TemporaryDirectory() as tmp:
            dataset, output = Path(tmp, 'dataset.jsonl'), Path(tmp, 'out.jsonl')
            dataset.write_text(json.dumps(row) + '\n' + json.dumps(missing) + '\n')
            argv = ['multilingual', 'analyze', ENTRY, '--dataset', str(dataset), '--output', str(output)]
            with patch.object(sys, 'argv', argv), patch.object(ml, 'Cache', return_value=cache), \
                    patch('parsimony.languages.track', return_value={'language': 'go'}), \
                    patch('parsimony.benchmark.measure', side_effect=measure), \
                    patch('parsimony.benchmark.human_cache', {}), patch('builtins.print'):
                ml.main()
            failed, absent = read_jsonl(output)
        self.assertEqual(failed['evaluation_result'], 'failed')
        self.assertEqual(failed['analysis_status'], 'ok')
        self.assertEqual(failed['model_human_ratio'], 1)
        self.assertEqual(cache.requested.count(source), 3)
        self.assertEqual(absent['analysis_status'], 'missing_patch')
        self.assertIsNone(absent['metrics'])
