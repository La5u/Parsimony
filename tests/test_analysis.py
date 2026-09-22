import difflib
import unittest

from parsimony.analysis import apply_patch, generated, implementation, measure, normalized_tokens, parse_patch, structure


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
        before = 'x = 1\n'
        patch = diff(before, 'x = 2\n', 'django/db/migrations/loader.py')
        result = measure(patch, lambda p: before)
        self.assertEqual(result['touched_files'], ['django/db/migrations/loader.py'])
        self.assertEqual(result['excluded_files'], [])

    def test_behavioral_edits_with_zero_normalized_footprint_are_visible_in_audit(self):
        before = 'manager = base_manager\n'
        after = 'manager = default_manager\n'
        result = measure(diff(before, after, path='pkg/manager.py'), lambda p: before)
        self.assertEqual(result['churn'], 0)
        self.assertEqual(result['touched_files'], ['pkg/manager.py'])
        self.assertEqual(result['files_changed'], 0)
        self.assertGreater(result['value_sensitive_churn'], 0)
        self.assertGreater(measure(diff('x = 1\n', 'x = 2\n'), lambda p: 'x = 1\n')['value_sensitive_churn'], 0)

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

    def test_invalid_ast_unavailable(self):
        self.assertIsNone(structure('print x\n'))

    def test_generated(self):
        self.assertFalse(generated('"""features generated by each transformer"""\n'))
        self.assertFalse(generated('# these values are generated by the method below\nx=1\n'))
        source = '# generated by tool\nx=1\n'
        result = measure(diff(source, source + 'y=2\n'), lambda p: source)
        self.assertEqual(result['files_changed'], 0)
