import hashlib
import json
from pathlib import Path
import re
import unittest

from parsimony.scoring import score_records

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'examples/live-python'


class LivePublicationTests(unittest.TestCase):
    def test_full_population_and_unchanged_measurement_exports(self):
        panel = json.loads((FOLDER / 'score-panel.json').read_text())
        self.assertEqual(len(panel['tasks']), 300)
        self.assertEqual(sum(bool(refs) for refs in panel['tasks'].values()), 238)
        self.assertEqual(sum(len(refs) for refs in panel['tasks'].values()), 509)
        archived = json.loads((ROOT / 'examples/priority-live/measurement-summary.json').read_text())['cohorts']
        groups = {'deepseek-v4.1-flash': 'deepseek_v4_1_flash', 'gpt-5.6-sol': 'gpt_5_6_sol',
                  'claude-opus-4.8': 'claude_opus_4_8'}
        records = []
        forbidden = {'patch', 'model_patch', 'problem_statement', 'test_patch', 'prompt', 'trajectory', 'stdout', 'stderr'}
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden & value.keys())
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
        for filename, key in groups.items():
            raw = (FOLDER / (filename + '.jsonl')).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), archived[key]['measurement_records_sha256'])
            rows = [json.loads(line) for line in raw.splitlines()]
            self.assertEqual(len(rows), 300)
            self.assertEqual({r['task_id'] for r in rows}, set(panel['tasks']))
            inspect(rows)
            records.extend(rows)
        actual = score_records(panel, records)
        stored = json.loads((FOLDER / 'scores.json').read_text())['leaderboard']
        self.assertEqual(actual, stored)
        self.assertTrue(all(r['task_count'] == 300 and r['score'] is None for r in actual))

    def test_one_live_board_with_full_population_bounds_and_navigation(self):
        data = json.loads((FOLDER / 'site-data.json').read_text())
        html = (ROOT / 'site/live.html').read_text()
        embedded = json.loads(re.search(r'type="application/json">(.*?)</script>', html, re.S)[1])
        self.assertEqual(embedded, data)
        self.assertEqual(data['task_count'], 300)
        self.assertEqual(data['population_count'], 300)
        self.assertEqual(data['excluded_tasks'], [])
        self.assertEqual(len(data['uncalibrated_tasks']), 62)
        self.assertEqual({m['company'] for m in data['models']}, {'DeepSeek', 'OpenAI', 'Anthropic'})
        self.assertEqual(sorted(m['measured_attempts'] for m in data['models']), [276, 287, 288])
        self.assertTrue(all(m['score'] is None and m['rank_range'] for m in data['models']))
        for page in ('index', 'javascript', 'typescript', 'go', 'verified'):
            other = (ROOT / 'site' / (page + '.html')).read_text()
            state = json.loads(re.search(r'type="application/json">(.*?)</script>', other, re.S)[1])
            self.assertTrue(any(link['url'] == 'live.html' for link in state['nav']))
