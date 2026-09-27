import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError

from parsimony.deepswe import (attempts, blank_context, choose_configs, cluster, dataset_rows, display_name,
                               fetch_patch, load_submission, pooled_panel, read_tasks)
from parsimony.scoring import score_records
from parsimony.stability import bootstrap, clusters, drop_agent
from tests.test_scoring import record

TOML = '''schema_version = "1.3"
[metadata]
task_id = "{task}"
language = "{language}"
repository_url = "https://github.com/owner/{task}"
base_commit_hash = "abc123"
'''
RELEASE = dict(release_id='v1.1', artifact_base_url='https://cdn.example/',
               artifact_patterns=dict(model_patch='v1.1/trial-artifacts/{trial_name}/artifacts/model.patch'))


def trial(config, task, name, outcome='pass', started='2026-09-01T00:00:00Z', patch=True):
    return dict(config=config, task_name=task, trial_name=name, outcome=outcome, started_at=started,
                has_model_patch=patch, model=config.split('_')[0], reasoning_effort='high', harness='mini-swe-agent')


class FakeCache:
    def __init__(self, files):
        self.files, self.requested = files, []

    def get(self, url):
        self.requested.append(url)
        if url not in self.files:
            raise HTTPError(url, 404, 'missing', {}, None)
        return self.files[url]


class DeepSWETests(unittest.TestCase):
    def test_read_tasks_keeps_one_language_and_repairs_solutions(self):
        with tempfile.TemporaryDirectory() as tmp:
            for task, language in (('py-task', 'python'), ('go-task', 'go')):
                d = Path(tmp, 'tasks', task)
                (d / 'solution').mkdir(parents=True)
                (d / 'task.toml').write_text(TOML.format(task=task, language=language))
                (d / 'solution' / 'solution.patch').write_text(
                    '--- a/x.py\n+++ b/x.py\n@@ -1,3 +1,3 @@\n-a\n+b\n\n c\n')
            tasks = read_tasks(tmp)
        self.assertEqual([(t['task'], t['repo'], t['base_commit']) for t in tasks], [('py-task', 'owner/py-task', 'abc123')])
        self.assertIn('\n \n c\n', tasks[0]['patch'])
        rows = dataset_rows(tasks)
        self.assertEqual([r['instance_id'] for r in rows], [f'py-task#{k}' for k in range(1, 5)])
        self.assertEqual({cluster(r['instance_id']) for r in rows}, {'py-task'})

    def test_blank_context_counts_hunk_lines(self):
        # '--- c' inside the hunk is a removed line, not a file header.
        patch = '--- a/x.py\n+++ b/x.py\n@@ -1,3 +1,2 @@\n-a\n\n--- c\n'
        self.assertEqual(blank_context(patch), '--- a/x.py\n+++ b/x.py\n@@ -1,3 +1,2 @@\n-a\n \n--- c\n')
        self.assertEqual(blank_context(patch.replace('\n\n', '\n \n')), patch.replace('\n\n', '\n \n'))

    def test_choose_configs_takes_best_config_with_patches(self):
        board = [dict(model='m', reasoning_effort='max', config='m_max', pass_rate=0.8),
                 dict(model='m', reasoning_effort='high', config='m_high', pass_rate=0.7),
                 dict(model='n', reasoning_effort='high', config='n_high', pass_rate=0.9)]
        trials = ([trial('m_max', 't', f'a{i}', patch=False) for i in range(4)] +
                  [trial('m_high', 't', f'b{i}') for i in range(4)] + [trial('n_high', 't', f'c{i}') for i in range(4)])
        self.assertEqual([c['config'] for c in choose_configs(board, trials)], ['n_high', 'm_high'])

    def test_choose_configs_skips_unavailable_patches(self):
        board = [dict(model='m', reasoning_effort='max', config='m_max', pass_rate=0.8),
                 dict(model='m', reasoning_effort='high', config='m_high', pass_rate=0.7)]
        trials = [trial('m_max', 't', 'a'), trial('m_high', 't', 'b')]
        chosen = choose_configs(board, trials, available=lambda config: config != 'm_max')
        self.assertEqual([c['config'] for c in chosen], ['m_high'])

    def test_fetch_patch_treats_forbidden_as_missing(self):
        class Forbidden:
            def get(self, url):
                raise HTTPError(url, 403, 'forbidden', {}, None)
        self.assertIsNone(fetch_patch(Forbidden(), 'https://cdn.example/x'))

        class Flaky:
            calls = 0
            def get(self, url):
                self.calls += 1
                if self.calls < 3:
                    raise ConnectionResetError('reset')
                return b'patch'
        self.assertEqual(fetch_patch(Flaky(), 'https://cdn.example/x'), 'patch')

    def test_display_names(self):
        names = {'gpt_5_6_sol_max': 'GPT-5.6 Sol (max)', 'claude_opus_5_max': 'Claude Opus 5 (max)',
                 'glm_5_3_flash_max': 'GLM-5.3 Flash (max)', 'kimi_k2_7_code_default': 'Kimi K2.7 Code',
                 'qwen3_8_max_xhigh': 'Qwen3.8 Max (xhigh)', 'deepseek_v4_pro_max': 'DeepSeek V4 Pro (max)'}
        for config, name in names.items():
            self.assertEqual(display_name(f'deepswe-v1.1_mini_swe_agent_{config}'), name)

    def test_attempts_are_numbered_by_start_time(self):
        trials = [trial('c', 't', 'late', started='2026-09-02'), trial('c', 't', 'early', started='2026-09-01'),
                  trial('c', 'other', 'x'), trial('d', 't', 'y')]
        items = attempts(trials, 'c', {'t'})
        self.assertEqual({k: v['trial_name'] for k, v in items.items()}, {'t#1': 'early', 't#2': 'late'})

    def test_load_submission_outcomes_and_missing_patches(self):
        base = 'https://cdn.example/v1.1/trial-artifacts'
        trials = [trial('c', 't', 'p', 'pass', '1'), trial('c', 't', 'f', 'fail', '2'),
                  trial('c', 't', 'e', 'excluded_error', '3'), trial('c', 't', 'n', 'pass', '4', patch=False)]
        cache = FakeCache({f'{base}/p/artifacts/model.patch': b'patch-p', f'{base}/f/artifacts/model.patch': b'patch-f'})
        s = load_submission('c', trials, RELEASE, cache, {'t'})
        self.assertEqual(s['agent'], 'deepswe-v1.1_c')
        self.assertEqual(s['resolved'], {'t#1', 't#4'})
        self.assertEqual(s['predictions'], {'t#1': 'patch-p', 't#2': 'patch-f'})
        self.assertEqual(s['result_details']['unresolved'], ['t#2'])
        self.assertEqual(s['result_details']['no_logs'], ['t#3'])
        self.assertEqual(s['result_details']['missing_patch'], ['t#4'])
        self.assertEqual(len(cache.requested), 2)  # no download for errored or patchless runs

    def test_pooled_panel_shares_references_across_attempts(self):
        records = [record('a', 't#1', net=5, churn=9), record('a', 't#2', net=7, churn=9),
                   record('b', 't#1', net=9, churn=9), record('b', 't#2', net=1, churn=1, resolved=False),
                   record('a', 'u#1', net=1, churn=1, resolved=False), record('b', 'u#1', net=1, churn=1, resolved=False)]
        panel = pooled_panel(records, 'p')
        self.assertEqual(sorted(panel['tasks']), ['t#1', 't#2'])  # u has no passing patch
        refs = panel['tasks']['t#1']
        self.assertIs(refs, panel['tasks']['t#2'])
        self.assertEqual(sorted(r['agent'] for r in refs), ['a#1', 'a#2', 'b#1'])
        # Scoring accepts the pooled panel, and leaving a model out removes all its attempts.
        self.assertEqual(len(score_records(panel, records)), 2)
        reduced, _ = drop_agent(panel, 'a')
        self.assertEqual([r['agent'] for r in reduced['tasks']['t#1']], ['b#1'])

    def test_bootstrap_resamples_attempts_of_a_task_together(self):
        self.assertEqual(clusters(['t#1', 't#2', 'u#1', 'v']), [['t#1', 't#2'], ['u#1'], ['v']])
        point = lambda v: (v, v, v)
        # Two tasks, four attempts each: a leads on one task, b on the other.
        values = {'a': {f'{t}#{k}': point(90 if t == 't' else 10) for t in 'tu' for k in range(1, 5)},
                  'b': {f'{t}#{k}': point(10 if t == 't' else 90) for t in 'tu' for k in range(1, 5)}}
        tasks = sorted(values['a'])
        diffs = bootstrap(values, tasks, draws=300, seed=2)['pairs']['a|b']
        # Resampling whole tasks gives only -80, 0 or +80: the interval spans both signs.
        self.assertLess(diffs['ci_95'][0], 0)
        self.assertGreater(diffs['ci_95'][1], 0)


if __name__ == '__main__':
    unittest.main()
