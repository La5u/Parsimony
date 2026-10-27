"""Check offline rebuild orchestration without regenerating pages or downloading data."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


@unittest.skipUnless(shutil.which('bash'), 'requires bash')
class RebuildScriptTests(unittest.TestCase):
    def test_offline_reports_skipped_pages_and_leaves_them_alone(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bin_dir = tmp / 'bin'
            bin_dir.mkdir()
            # Capture commands instead of invoking the generator or any downloader.
            python = bin_dir / 'python'
            python.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$REBUILD_CALLS"\n')
            python.chmod(0o755)
            calls = tmp / 'calls'
            env = {**os.environ, 'PATH': str(bin_dir) + os.pathsep + os.environ.get('PATH', ''),
                   'REBUILD_CALLS': str(calls)}
            for existing in (False, True):
                with self.subTest(existing=existing):
                    output = tmp / ('existing' if existing else 'fresh')
                    output.mkdir()
                    skipped = [output / 'index.html', output / 'go.html']
                    if existing:
                        for page in skipped:
                            page.write_text('keep this published page\n')
                    calls.write_text('')
                    result = subprocess.run(
                        ['bash', str(root / 'scripts/rebuild-site.sh'), str(output), '--offline'],
                        cwd=root, env=env, text=True, capture_output=True, check=True)
                    self.assertIn('skipping DeepSWE go.html and index.html', result.stderr)
                    self.assertIn('existing copies are left unchanged', result.stderr)
                    for page in skipped:
                        if existing:
                            self.assertEqual(page.read_text(), 'keep this published page\n')
                        else:
                            self.assertFalse(page.exists())
                    commands = calls.read_text()
                    self.assertNotIn('fetch-go-v2-release.py', commands)
                    # Only the DeepSWE combined page (which needs Go) is skipped; SWE-Milestone merges local boards.
                    self.assertNotIn('--merge python=examples/deepswe-python', commands)
                    self.assertNotIn('--output ' + str(output / 'index.html'), commands)
                    for name in ('python', 'javascript', 'typescript', 'verified', 'live',
                                 'sweeper-php', 'live-javascript', 'live-typescript', 'live-go', 'swe-milestone',
                                 'polybench-python'):
                        self.assertIn('--output ' + str(output / (name + '.html')), commands)
                    self.assertEqual(len(commands.splitlines()), 11)
