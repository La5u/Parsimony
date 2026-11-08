import json
import tempfile
import unittest
from pathlib import Path

from parsimony import hlb
from parsimony.site import BENCHMARKS, color_group, label, published_sources
from tests.test_deepswe import TOML, FakeCache

ROOT = Path(__file__).resolve().parent.parent
TRIALS = dict(space_commit='abc', setups={
    'glm-5.3-flash_high_codex': dict(model='zai-org/GLM-5.3-Flash', reasoning_effort='high', harness='codex',
                                     harness_version='0.162.1', trials=[
        dict(task='a', attempt=1, trial='a__1', outcome='pass', patch='runs/r/deep-swe/a__1/model.patch'),
        dict(task='a', attempt=2, trial='a__2', outcome='fail', patch='runs/r/deep-swe/a__2/model.patch'),
        dict(task='a', attempt=3, trial='a__3', outcome='pass', patch='runs/r/deep-swe/a__3/model.patch'),
        dict(task='rusty', attempt=1, trial='rusty__1', outcome='pass', patch='runs/r/deep-swe/rusty__1/model.patch')])})


class HarnessLeaderboardTests(unittest.TestCase):
    def test_display_name_puts_the_model_first(self):
        self.assertEqual(hlb.display_name('hlb-deepswe_glm-5.3-flash_high_claude-code'), 'GLM-5.3 Flash (high) · Claude Code')
        self.assertEqual(label('hlb-deepswe_deepseek-v4.1-flash_low_mini-swe-agent'), 'DeepSeek V4.1 Flash (low) · mini-SWE-agent')
        self.assertEqual(hlb.setup_id('deepseek-ai/DeepSeek-V4.1-Flash', 'low', 'pi'), 'deepseek-v4.1-flash_low_pi')

    def test_rows_are_colored_by_harness_with_a_short_chart_label(self):
        self.assertEqual(color_group('hlb-deepswe_deepseek-v4.1-flash_low_mini-swe-agent'),
                         dict(color_group='mini-SWE-agent', short_name='DeepSeek low'))
        self.assertEqual(color_group('deepswe-python_claude-opus'), {})

    def test_dataset_keeps_scored_tasks_of_one_language_with_three_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            for task, language in (('a', 'python'), ('b', 'python'), ('rusty', 'rust')):
                folder = Path(tmp, 'tasks', task)
                (folder / 'solution').mkdir(parents=True)
                (folder / 'task.toml').write_text(TOML.format(task=task, language=language))
                (folder / 'solution' / 'solution.patch').write_text('diff --git a/x b/x\n')
            rows = hlb.dataset(tmp, TRIALS, 'python')
        self.assertEqual([r['instance_id'] for r in rows], ['a#1', 'a#2', 'a#3'])

    def test_load_submission_outcomes_and_missing_patches(self):
        base = hlb.BUCKET + '/runs/r/deep-swe/'
        cache = FakeCache({base + 'a__1/model.patch': b'diff 1', base + 'a__3/model.patch': b''})
        sub = hlb.load_submission('glm-5.3-flash_high_codex', TRIALS, cache, {'a#1', 'a#2', 'a#3'})
        self.assertEqual(sub['agent'], 'hlb-deepswe_glm-5.3-flash_high_codex')
        self.assertEqual(sub['resolved'], {'a#1', 'a#3'})
        self.assertEqual(sub['evaluated'], {'a#1', 'a#2', 'a#3'})
        self.assertEqual(sub['predictions'], {'a#1': 'diff 1', 'a#3': ''})
        self.assertEqual(sub['result_details']['missing_patch'], ['a#2'])
        self.assertEqual(sub['provenance']['harness_version'], '0.162.1')
        self.assertNotIn(base + 'rusty__1/model.patch', cache.requested)

    def test_board_sources_have_three_attempts_per_task(self):
        self.assertEqual(BENCHMARKS['hlb']['attempts'], 3)
        sources = [s for s in published_sources('hlb', 'go') if s['benchmark'] == 'hlb']
        self.assertEqual([s['language'] for s in sources], ['python', 'javascript', 'typescript', 'go'])
        self.assertEqual([s['active'] for s in sources], [False, False, False, True])
        self.assertTrue(all(s['attempts_per_task'] == 3 for s in sources))

    def test_frozen_trials_have_three_scored_attempts_and_a_patch_each(self):
        trials = json.loads((ROOT / 'examples/hlb-deepswe/trials.json').read_text())
        self.assertEqual(len(trials['setups']), 36)
        for name, setup in trials['setups'].items():
            self.assertEqual(name, hlb.setup_id(setup['model'], setup['reasoning_effort'], setup['harness']))
            self.assertIn(setup['harness'], hlb.HARNESSES)
            per_task = {}
            for t in setup['trials']:
                self.assertIn(t['outcome'], ('pass', 'fail'))
                self.assertTrue(t['patch'])
                per_task.setdefault(t['task'], []).append(t['attempt'])
            self.assertEqual(len(per_task), 111)
            self.assertTrue(all(sorted(a) == list(range(1, len(a) + 1)) and len(a) <= 3 for a in per_task.values()))


if __name__ == '__main__':
    unittest.main()
