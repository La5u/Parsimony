import shutil
import unittest
from pathlib import Path

from parsimony.analysis import implementation, measure

HAS_PARSER = bool(shutil.which('node')) and (Path(__file__).resolve().parent.parent / 'node_modules/typescript').exists()


NEW_ROOT = """diff --git a/scratch.ts b/scratch.ts
new file mode 100644
--- /dev/null
+++ b/scratch.ts
@@ -0,0 +1 @@
+const a = 1;
"""


class JavaScriptTypeScriptScopeTests(unittest.TestCase):
    def test_type_tests_are_out_of_scope(self):
        self.assertFalse(implementation('packages/effect/dtslint/Array.tst.ts', 'typescript'))
        self.assertFalse(implementation('dtslint/Schema.ts', 'typescript'))
        self.assertFalse(implementation('src/foo.tst.ts', 'typescript'))

    def test_ordinary_sources_stay_in_scope(self):
        self.assertTrue(implementation('src/first.ts', 'typescript'))
        self.assertTrue(implementation('src/dtslintish.ts', 'typescript'))

    @unittest.skipUnless(HAS_PARSER, 'needs Node.js and npm ci')
    def test_new_root_script_is_excluded(self):
        for language in ('javascript', 'typescript'):
            name = 'scratch.ts' if language == 'typescript' else 'scratch.js'
            metrics = measure(NEW_ROOT.replace('scratch.ts', name), get_source=lambda path: '', language=language)
            self.assertEqual(metrics['excluded_files'], [name])
            self.assertEqual(metrics['files_changed'], 0)


if __name__ == '__main__':
    unittest.main()
