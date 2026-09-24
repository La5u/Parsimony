import difflib
import random
import time
import unittest

from parsimony.analysis import (apply_patch, generated, implementation, measure, myers, myers_blocks,
                                normalized_tokens, parse_patch, structure, token_diff)


def diff(before, after, path='pkg/core.py', old=None, new=None):
    return ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                       fromfile=old or 'a/' + path, tofile=new or 'b/' + path))


class AnalysisTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalized_tokens('x = "hello" # comment\ny=102\n'),
                         normalized_tokens("long_name='bye'\nz = 0xff\n"))
        self.assertEqual(normalized_tokens('f(x)\n'), normalized_tokens('f(\n (x),\n)\n'))

    def test_docstrings_not_code(self):
        before = 'def f():\n    return 1\n'
        after = 'def f():\n    """docs"""\n    return 1\n'
        result = measure(diff(before, after), lambda p: before)
        self.assertEqual(result['churn'], 0)
        self.assertEqual(result['ast_delta'], 0)
        # A docstring sharing a line must not hide implementation code.
        self.assertIn('=', normalized_tokens('"docs"; x = 1\n'))

    def test_block_move_is_not_zero_footprint(self):
        before = 'def f():\n    while cond:\n        kern += 1\n    hit = kern in s\n    return hit\n'
        after = 'def f():\n    while cond:\n        kern += 1\n        hit = kern in s\n    return hit\n'
        result = measure(diff(before, after), lambda p: before)
        self.assertGreater(result['churn'], 0)
        self.assertGreater(result['structural_churn'], 0)
        self.assertEqual(normalized_tokens('def f():\n  return 1\n'),
                         normalized_tokens('def f():\n    return 1\n'))

    def test_fstring_literal_edit_counts(self):
        before = 'def f(x):\n    return f"unittest_{x}"\n'
        after = 'def f(x):\n    return f"_unittest_{x}"\n'
        result = measure(diff(before, after), lambda p: before)
        self.assertEqual(result['churn'], 2)
        self.assertEqual(result['structural_churn'], 0)

    def test_deletion_rewarded(self):
        before = 'def f(x):\n    if x:\n        return x\n    return 0\n'
        after = 'def f(x):\n    return x\n'
        result = measure(diff(before, after), lambda p: before)
        self.assertLess(result['net_tokens'], 0)
        self.assertGreater(result['churn'], 0)
        self.assertEqual(result['complexity_delta'], -1)
        self.assertLess(result['ast_delta'], 0)

    def test_exclusions(self):
        patch = ''.join(diff('x=1\n', 'x=1\ny=2\n', p) for p in
                        ['tests/test_x.py', 'docs/conf.py', 'vendor/library.py', 'x.lock', 'migrations/001.py'])
        result = measure(patch, lambda p: self.fail('excluded path fetched'))
        self.assertEqual(result['churn'], 0)
        self.assertEqual(len(result['excluded_files']), 5)
        self.assertEqual(result['touched_files'], result['excluded_files'])

    def test_django_migration_core_included_but_migration_scripts_excluded(self):
        for path in ('django/db/migrations/loader.py',
                     'django/db/migrations/operations/models.py'):
            self.assertTrue(implementation(path), path)
        for path in ('myapp/migrations/0001_initial.py',
                     'django/db/migrations/0001_initial.py'):
            self.assertFalse(implementation(path), path)
        self.assertTrue(implementation('django/test/testcases.py'))
        self.assertFalse(implementation('tests/test_client/tests.py'))
        self.assertFalse(implementation('django/test/test_utils.py'))
        before = 'x = 1\n'
        patch = diff(before, 'x = 2\n', 'django/db/migrations/loader.py')
        result = measure(patch, lambda p: before)
        self.assertEqual(result['touched_files'], ['django/db/migrations/loader.py'])
        self.assertEqual(result['excluded_files'], [])

    def test_identifier_and_literal_edits_are_primary_footprint(self):
        before = 'manager = base_manager\n'
        after = 'manager = default_manager\n'
        result = measure(diff(before, after, path='pkg/manager.py'), lambda p: before)
        self.assertEqual((result['net_tokens'], result['churn'], result['files_changed']), (0, 2, 1))
        self.assertEqual(result['structural_churn'], 0)
        for old, new in (('x = 1\n', 'x = 2\n'), ('y = a - b\n', 'y = b - a\n')):
            self.assertGreater(measure(diff(old, new), lambda p: old)['churn'], 0)
        # Formatting and comments remain free.
        self.assertEqual(measure(diff('x = 1\n', '# note\nx = (1)\n'), lambda p: 'x = 1\n')['churn'], 0)

    def test_unparseable_side_tokenizes_both_sides_lexically(self):
        before = ''.join(f'def g{i}(x):\n    """doc {i}"""\n    return (x+{i},)\n' for i in range(20))
        after = before + 'print "x"\n'
        result = measure(diff(before, after), lambda p: before)
        self.assertEqual(result['churn'], 2)  # `print` and the string, not a canonical re-render
        self.assertEqual(result['lexical_files'], ['pkg/core.py'])
        self.assertIsNone(result['ast_delta'])

    def test_myers_is_minimal(self):
        def lcs(a, b):
            row = [0] * (len(b) + 1)
            for x in a:
                prev = 0
                for j, y in enumerate(b, 1):
                    prev, row[j] = row[j], prev + 1 if x == y else max(row[j], row[j - 1])
            return row[-1]
        rng = random.Random(0)
        for _ in range(300):
            a = [rng.choice('abc') for _ in range(rng.randint(0, 12))]
            b = [rng.choice('abc') for _ in range(rng.randint(0, 12))]
            common = lcs(a, b)
            self.assertEqual(myers(a, b), (len(b) - common, len(a) - common))
            blocks = myers_blocks(a, b)
            self.assertEqual(sum(a2 - a1 for a1, a2, _, _ in blocks), len(a) - common)
            self.assertEqual(sum(b2 - b1 for _, _, b1, b2 in blocks), len(b) - common)
        self.assertIsNone(myers(list('ab'), list('cd'), max_d=3))

    def test_large_repetitive_file_is_fast(self):
        before = ''.join(f'def g{i}(x, y):\n    if x > {i}:\n        return x + y * {i}\n    return x\n'
                         for i in range(1000))
        after = 'import os\n' + before.replace('return x + y * 999', 'return x - y * 999 + 1')
        started = time.perf_counter()
        result = measure(diff(before, after), lambda p: before)
        self.assertLess(time.perf_counter() - started, 10)
        self.assertEqual(result['tokens_added'] - result['tokens_deleted'], 4)
        self.assertEqual(result['approximate_files'], [])

    def test_token_diff_is_minimal_and_flags_large_rewrites(self):
        a = [('x', '=', '1'), ('y', '=', '2')]
        self.assertEqual(token_diff(a, a), (0, 0, False))
        self.assertEqual(token_diff(a, []), (0, 6, False))
        # Moving a statement into a new block: exact minimum, not a line-level rewrite.
        before = [('ID', '=', 'ID', '(', ')'), ('return', 'ID')]
        after = [('if', 'ID', ':'), ('INDENT', 'ID', '=', 'ID', '(', ')'), ('DEDENT', 'return', 'ID')]
        self.assertEqual(token_diff(before, after), (5, 0, False))
        rng = random.Random(1)
        rewrite = token_diff([(str(rng.random()),) for _ in range(700)], [(str(rng.random()),) for _ in range(700)])
        self.assertEqual(rewrite, (700, 700, True))

    def test_add_delete_and_multiple_hunks(self):
        text = 'x = 1\n'
        added = measure(diff('', text, old='/dev/null'), lambda p: self.fail('new file fetched'))
        deleted = measure(diff(text, '', new='/dev/null'), lambda p: text)
        self.assertEqual(added['net_tokens'], -deleted['net_tokens'])
        before = ''.join(f'x{i} = {i}\n' for i in range(30))
        after = before.replace('x0 = 0', 'x0 = foo()').replace('x29 = 29', 'x29 = bar()')
        file = parse_patch(diff(before, after))[0]
        self.assertEqual(len(file.hunks), 2)
        self.assertEqual(apply_patch(before, file), after)

    def test_context_validation_and_paths(self):
        patch = diff('x=1\n', 'x=2\n')
        with self.assertRaises(ValueError):
            measure(patch, lambda p: 'different\n')
        with self.assertRaises(ValueError):
            parse_patch('--- a/../unsafe.py\n+++ b/../unsafe.py\n')
        with self.assertRaises(ValueError):
            parse_patch('--- a/a.py\n+++ b/a.py\n@@ -1,2 +1 @@\n-a\n+b\n')

    def test_shifted_hunks_apply_by_exact_context_like_git_apply(self):
        before = ''.join(f'x{i} = {i}\n' for i in range(20))
        after = before.replace('x10 = 10', 'x10 = f(10)').replace('x15 = 15', 'x15 = g(15)')
        patch = diff(before, after)
        shifted = 'import os\nimport sys\n' + before  # base gained two lines above both hunks
        offsets = []
        self.assertEqual(apply_patch(shifted, parse_patch(patch)[0], offsets), 'import os\nimport sys\n' + after)
        self.assertEqual(offsets, [2])  # second hunk inherits the shift
        self.assertEqual(measure(patch, lambda p: shifted)['offset_hunks'], 1)
        with self.assertRaisesRegex(ValueError, 'differs'):
            apply_patch(shifted.replace('x9 = 9', 'x9 = 99'), parse_patch(patch)[0])
        # Identical context at equal distances on both sides cannot be placed.
        hunk = parse_patch('--- a/m.py\n+++ b/m.py\n@@ -3,1 +3,1 @@\n-b\n+B\n')[0]
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            apply_patch('a\nb\nc\nb\n', hunk)  # `b` sits one line before and after line 3
        self.assertEqual(apply_patch('a\nb\nc\nd\nb\n', hunk), 'a\nB\nc\nd\nb\n')  # nearest wins

    def test_no_final_newline(self):
        patch = '--- a/a.py\n+++ b/a.py\n@@ -1 +1 @@\n-x=1\n\\ No newline at end of file\n+x=2\n\\ No newline at end of file\n'
        self.assertEqual(apply_patch('x=1', parse_patch(patch)[0]), 'x=2')

    def test_patch_only_labeled(self):
        result = measure(diff('x=1\n', 'x=f(1)\n'))
        self.assertEqual(result['mode'], 'patch_only')
        self.assertIsNone(result['ast_delta'])

    def test_mixed_unsupported_implementation_not_silently_ignored(self):
        patch = diff('x=1\n', 'x=f(1)\n')
        patch += 'diff --git a/old.py b/new.py\nsimilarity index 100%\nrename from old.py\nrename to new.py\n'
        with self.assertRaises(ValueError):
            measure(patch, lambda p: 'x=1\n')

    def test_docstring_stripped_once(self):
        before = 'def f():\n    """doc"""\n    "marker"\n    return 1\n'
        after = before.replace('return 1', 'return 2')
        result = measure(diff(before, after), lambda p: before)
        self.assertEqual(result['ast_delta'], 0)
        self.assertEqual(structure(before)[0], structure(after)[0])

    def test_target_syntax_warnings_are_silent(self):
        import warnings
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            self.assertIsNotNone(structure('x = "\\*"\n'))  # source text: x = "\*"
        self.assertEqual([w for w in caught if issubclass(w.category, SyntaxWarning)], [])

    def test_invalid_ast_unavailable(self):
        self.assertIsNone(structure('print x\n'))

    def test_generated(self):
        self.assertFalse(generated('"""features generated by each transformer"""\n'))
        self.assertFalse(generated('# these values are generated by the method below\nx=1\n'))
        source = '# generated by tool\nx=1\n'
        result = measure(diff(source, source + 'y=2\n'), lambda p: source)
        self.assertEqual(result['files_changed'], 0)
