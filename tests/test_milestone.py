import io
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from parsimony import milestone
from parsimony.milestone import Git, agent_id, analyze, build_dataset, diff, outcome, read_snapshot

REPO_DIR = 'owner_proj_v1_v2'
START = {'pkg/calc.py': 'def total(items):\n    return 0\n',
         'pkg/old.py': 'def unused():\n    return 1\n',
         'pkg/test_calc.py': 'def test_total():\n    pass\n'}
END = {'pkg/calc.py': 'def total(items):\n    return sum(items)\n',
       'pkg/old.py': 'def unused():\n    return 1\n'}


def git(root, *args, env=None):
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True,
                          env=env).stdout.strip()


def commit(work, files, message):
    for path in work.rglob('*.py'):
        path.unlink()
    for path, text in files.items():
        (work / path).parent.mkdir(parents=True, exist_ok=True)
        (work / path).write_text(text)
    git(work, 'add', '-A')
    git(work, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', message)
    return git(work, 'rev-parse', 'HEAD')


def snapshot(path, files):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(path, 'w') as tar:
        for name, text in files.items():
            raw = text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(raw)
            tar.addfile(info, io.BytesIO(raw))


class MilestoneTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        work = root / 'work'
        work.mkdir()
        git(work, 'init', '-q')
        start = commit(work, START, 'start')
        end = commit(work, END, 'end')
        git(work, 'tag', 'milestone-M01-start', start)
        git(work, 'tag', 'milestone-M01-end', end)
        self.gits = root / 'git'
        git(root, 'clone', '-q', '--bare', str(work), str(self.gits / REPO_DIR))
        git(self.gits / REPO_DIR, 'update-ref', 'refs/start/M01', start)
        self.data = root / 'data' / REPO_DIR
        self.data.mkdir(parents=True)
        (self.data / 'metadata.json').write_text(json.dumps(dict(repo_name='owner/proj', repo_src_dirs=['pkg/'])))
        (self.data / 'milestones.csv').write_text('id,title,category,commits\nM01,Totals,Feature,abc1234\n'
                                                  'M02,Docs only,Feature,def5678\n')
        (self.data / 'selected_milestone_ids.txt').write_text('M01\n')
        # The harness filters tests out of every snapshot; one model deletes old.py.
        base = {k: v for k, v in START.items() if 'test_' not in k}
        self.cells = {}
        for config, files, resolved in (
                ('_claude-code_model-a_run_001', {'pkg/calc.py': END['pkg/calc.py']}, True),
                ('_codex_model-b_run_001', {**base, 'pkg/calc.py': 'def total(items):\n    t = 0\n'
                                            '    for i in items:\n        t += i\n    return t\n'}, False)):
            cell = self.data / 'mstone_trial' / config / 'M01' / 'evaluation'
            snapshot(cell / 'source_snapshot.tar', files)
            (cell / 'evaluation_result.json').write_text(json.dumps(dict(milestone_id='M01', resolved=not resolved)))
            (cell / 'evaluation_result_filtered.json').write_text(json.dumps(dict(milestone_id='M01', resolved=resolved)))
        self.baselines = root / 'baselines.json'
        self.baselines.write_text(json.dumps({f'{REPO_DIR}/M01': dict(image='img@sha256:' + '0' * 64, head=start)}))
        self.root = root
        repos = patch.object(milestone, 'REPOS', {REPO_DIR: ('proj', 'python')})
        repos.start()
        self.addCleanup(repos.stop)
        self.rows = build_dataset(root / 'data', self.baselines, self.gits)
        self.population = root / 'population.jsonl'
        self.population.write_text(''.join(json.dumps(r) + '\n' for r in self.rows))

    def test_population_is_graded_milestones_with_in_scope_reference_changes(self):
        self.assertEqual([r['instance_id'] for r in self.rows], ['proj__M01'])
        row = self.rows[0]
        self.assertEqual((row['repo'], row['language']), ('owner/proj', 'python'))
        self.assertEqual(row['task_url'], 'https://github.com/owner/proj/commit/abc1234')
        self.assertEqual(row['provenance']['reference_files'], 1)

    def test_start_state_must_match_extracted_image(self):
        self.baselines.write_text(json.dumps({f'{REPO_DIR}/M01': dict(image='x', head='f' * 40)}))
        with self.assertRaisesRegex(ValueError, 'start state differs'):
            build_dataset(self.root / 'data', self.baselines, self.gits)

    def test_diff_applies_to_the_start_state(self):
        before = {'pkg/a.py': b'x = 1\n', 'pkg/gone.py': b'y = 2\n', 'pkg/test_a.py': b'pass\n'}
        after = {'pkg/a.py': b'x = 2\n', 'pkg/new.py': b'z = 3', 'pkg/test_a.py': b'fail\n', 'pkg/gone.py': None}
        text, paths = diff(before, after, 'python')
        self.assertEqual(paths, ['pkg/a.py', 'pkg/gone.py', 'pkg/new.py'])  # tests are out of scope
        self.assertIn('diff --git a/pkg/new.py b/pkg/new.py\nnew file mode 100644\n--- /dev/null\n+++ b/pkg/new.py\n', text)
        self.assertIn('deleted file mode 100644\n--- a/pkg/gone.py\n+++ /dev/null\n', text)
        self.assertIn('\\ No newline at end of file', text)
        with tempfile.TemporaryDirectory() as tmp:
            for path, raw in before.items():
                (Path(tmp) / path).parent.mkdir(parents=True, exist_ok=True)
                (Path(tmp) / path).write_bytes(raw)
            git(tmp, 'init', '-q')
            subprocess.run(['git', '-C', tmp, 'apply', '-'], input=text.encode(), check=True)
            self.assertEqual((Path(tmp) / 'pkg/new.py').read_bytes(), b'z = 3')
            self.assertFalse((Path(tmp) / 'pkg/gone.py').exists())

    def test_outcome_prefers_filtered_result(self):
        cell = self.data / 'mstone_trial' / '_claude-code_model-a_run_001' / 'M01' / 'evaluation'
        result, name, _ = outcome(cell)
        self.assertEqual((result['resolved'], name), (True, 'evaluation_result_filtered.json'))
        (cell / 'evaluation_result_filtered.json').unlink()
        self.assertEqual(outcome(cell)[0]['resolved'], False)

    def test_agent_ids(self):
        self.assertEqual(agent_id('_gemini-cli_gemini-3.1-pro_run_002'), 'milestone-gemini-cli-gemini-3.1-pro')
        with self.assertRaises(ValueError):
            agent_id('feature_old_srs')

    def test_unsafe_snapshot_paths_are_rejected(self):
        path = self.root / 'bad.tar'
        snapshot(path, {'../escape.py': 'x = 1\n'})
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            read_snapshot(path)

    def test_deletions_need_evidence_beyond_a_filtered_snapshot(self):
        a, = analyze(self.population, self.root / 'data', self.gits, 'milestone-claude-code-model-a', 'python')
        b, = analyze(self.population, self.root / 'data', self.gits, 'milestone-codex-model-b', 'python')
        # Model A's snapshot lacks old.py, but model B kept it and the reference keeps it:
        # it is a deletion. Model B kept it, so only calc.py changed.
        self.assertEqual((a['analysis_status'], a['provenance']['patch_files'], a['provenance']['deleted_files']),
                         ('ok', 2, 1))
        self.assertEqual((b['analysis_status'], b['provenance']['patch_files'], b['provenance']['deleted_files']),
                         ('ok', 1, 0))
        self.assertEqual((a['resolved'], b['resolved']), (True, False))
        self.assertIn('pkg/old.py', a['metrics']['touched_files'])
        self.assertNotIn('pkg/old.py', b['metrics']['touched_files'])
        self.assertGreater(b['metrics']['net_units'], 0)
        self.assertEqual(a['human_metrics']['files_changed'], 1)
        self.assertEqual(a['benchmark_tasks'], 1)
        self.assertEqual(a['provenance']['result_file'], 'evaluation_result_filtered.json')

    def test_file_missing_from_every_snapshot_is_treated_as_filtered(self):
        cell = self.data / 'mstone_trial' / '_codex_model-b_run_001' / 'M01' / 'evaluation'
        snapshot(cell / 'source_snapshot.tar', {'pkg/calc.py': END['pkg/calc.py']})
        a, = analyze(self.population, self.root / 'data', self.gits, 'milestone-claude-code-model-a', 'python')
        self.assertEqual((a['provenance']['patch_files'], a['provenance']['deleted_files']), (1, 0))

    def test_snapshot_missing_most_start_files_is_not_measured(self):
        cell = self.data / 'mstone_trial' / '_codex_model-b_run_001' / 'M01' / 'evaluation'
        snapshot(cell / 'source_snapshot.tar', {'pkg/new.py': 'x = 1\n'})
        with patch.object(milestone, 'PARTIAL_MIN_FILES', 1):
            b, = analyze(self.population, self.root / 'data', self.gits, 'milestone-codex-model-b', 'python')
        self.assertEqual((b['analysis_status'], b['metrics'], b['resolved']), ('partial_snapshot', None, False))
        self.assertEqual(b['provenance']['missing_start_files'], 2)

    def test_git_lists_regular_files_under_source_dirs(self):
        repo = Git(self.gits / REPO_DIR)
        files = repo.files(repo.resolve('refs/start/M01'), ['pkg/'])
        self.assertEqual(sorted(files), sorted(START))


if __name__ == '__main__':
    unittest.main()
