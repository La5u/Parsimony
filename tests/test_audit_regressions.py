"""Regressions for the 2026-10-12 repository audit fixes."""
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from parsimony.analysis import measure, parse_patch
from parsimony.artifacts import Cache
from parsimony.benchmark import leaderboard, read_jsonl
from parsimony.contribute import public_url
from parsimony.scoring import freeze, quantile, score_records, task_score
from tests.test_scoring import record as scored

EDIT = """--- a/pkg/m.py
+++ b/pkg/m.py
@@ -1 +1 @@
-x = 1
+x = 2
"""


class PatchParserTests(unittest.TestCase):
    def test_duplicate_implementation_sections_are_rejected_not_counted_twice(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            measure(EDIT + EDIT, lambda path: 'x = 1\n')
        # A rename into a path edited by another section conflicts as well.
        rename = EDIT.replace('--- a/pkg/m.py', '--- a/pkg/old.py')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            parse_patch(rename + EDIT)

    def test_malformed_hunk_header_or_surplus_edits_are_rejected(self):
        for tail in ('@@ -5,1 +5,1 @\n-y = 1\n+y = 9\n', '+y = 9\n', '-y = 1\n'):
            with self.subTest(tail=tail), self.assertRaisesRegex(ValueError, 'malformed hunk'):
                parse_patch(EDIT + tail)
        # Headers, prose and a format-patch signature between sections remain accepted.
        self.assertEqual(len(parse_patch('Index: pkg/m.py\n' + EDIT + '-- \n2.43.0\n')), 1)

    def test_binary_check_uses_paths_without_git_prefixes(self):
        # A top-level testing/ helper is out of scope; its binary diff must not reject the patch.
        binary = ('diff --git a/testing/data.py b/testing/data.py\n'
                  'Binary files a/testing/data.py and b/testing/data.py differ\n')
        self.assertEqual(len(parse_patch(binary + 'diff --git a/pkg/m.py b/pkg/m.py\n' + EDIT)), 1)
        # A Django migrations-core rename without hunks is unsupported, not silently dropped.
        rename = ('diff --git a/django/db/migrations/state.py b/django/db/migrations/state2.py\n'
                  'similarity index 100%\n')
        with self.assertRaisesRegex(ValueError, 'binary/rename'):
            parse_patch(rename + 'diff --git a/pkg/m.py b/pkg/m.py\n' + EDIT)


class LeaderboardTests(unittest.TestCase):
    def test_out_of_scope_and_unparsed_successes_are_not_zero_footprints(self):
        def row(task, net, **metrics):
            return dict(agent='a', task_id=task, resolved=True, resolve_rate=0.5, analysis_status='ok',
                        model_human_ratio=None, metrics=dict(mode='full_file', net_units=net, churn=abs(net or 0),
                                                             **metrics))
        records = [row('1', 50), row('2', 0, touched_files=['tests/t.py'], excluded_files=['tests/t.py']),
                   row('3', None)]
        board, = leaderboard(records)
        self.assertEqual((board['task_ids'], board['median_net_units']), (['1'], 50))


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.panel = freeze([scored('a'), scored('b', net=5, churn=9)], 'panel')

    def test_explicitly_empty_failed_patch_scores_zero(self):
        empty = {**scored('c', resolved=False), 'published_result_categories': ['empty_patch'],
                 'analysis_status': 'empty_patch', 'metrics': None}
        self.assertEqual(task_score(empty, self.panel['tasks']['task']),
                         dict(status='empty_patch', score=0, lower=0, upper=0))
        attempted = {**empty, 'provenance': {**empty['provenance'], 'patch_sha256': hashlib.sha256(b'x').hexdigest()}}
        with self.assertRaisesRegex(ValueError, 'nonempty patch'):
            task_score(attempted, self.panel['tasks']['task'])

    def test_resolved_record_with_failure_category_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'resolved record'):
            task_score({**scored('c'), 'published_result_categories': ['no_generation']}, self.panel['tasks']['task'])

    def test_complete_score_equals_its_zero_width_interval(self):
        for row in score_records(self.panel, [scored('c', net=4)]):
            self.assertEqual(row['score'], row['lower'])
            self.assertEqual(row['score'], row['upper'])

    def test_quantile_interpolates(self):
        self.assertEqual(quantile(range(10), 0.975), 8.775)
        self.assertEqual(quantile([4, 1], 0.5), 2.5)
        self.assertEqual(quantile([7], 0.025), 7)


class InputSafetyTests(unittest.TestCase):
    def test_contributed_urls_must_be_public_https(self):
        self.assertTrue(public_url('https://raw.githubusercontent.com/o/r/c/p.diff'))
        for url in ('http://example.com/p', 'https://169.254.169.254/x', 'https://localhost/x', 'https://[::1]/x',
                    'https://[::1/x', 'https://u:p@github.com/x', 'https://svc.internal/x', 'file:///etc/passwd'):
            with self.subTest(url=url):
                self.assertFalse(public_url(url))

    def test_cache_bounds_download_size(self):
        class Response(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache(directory, max_bytes=4)
            with patch('parsimony.artifacts.urlopen', return_value=Response(b'12345')):
                with self.assertRaisesRegex(ValueError, 'exceeds'):
                    cache.get('https://example.com/big')
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_jsonl_values_may_contain_unicode_line_separators(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'r.jsonl'
            path.write_text('{"name": "a b"}\n{"name": "c"}\n', encoding='utf-8')
            self.assertEqual([r['name'] for r in read_jsonl(path)], ['a b', 'c'])


if __name__ == '__main__':
    unittest.main()
