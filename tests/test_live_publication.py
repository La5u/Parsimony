import hashlib
import json
from pathlib import Path
import re
import unittest

from parsimony.scoring import out_of_scope, score_records

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
        records.extend(json.loads(line) for line in (FOLDER / 'gpt-5.5-agav.jsonl').read_text().splitlines())
        actual = score_records(panel, records)
        stored = json.loads((FOLDER / 'scores.json').read_text())['leaderboard']
        self.assertEqual(actual, stored)
        self.assertTrue(all(r['task_count'] == 300 and r['score'] is None for r in actual))

    def test_gpt55_agav_population_measurements_and_reporting_scope(self):
        raw = (FOLDER / 'gpt-5.5-agav.jsonl').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         '1e398322396af536e5c58bd07241689bdb8309511229a9c64ce72eaf84a59e53')
        rows = [json.loads(line) for line in raw.splitlines()]
        population = {r['instance_id']: r for r in
                      map(json.loads, (FOLDER / 'population.jsonl').read_text().splitlines())}
        self.assertEqual(len(rows), 300)
        self.assertEqual({r['task_id'] for r in rows}, set(population))
        forbidden = {'patch', 'model_patch', 'problem_statement', 'test_patch',
                     'prompt', 'trajectory', 'stdout', 'stderr'}
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden & value.keys())
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
        inspect(rows)
        self.assertEqual(len({r['agent'] for r in rows}), 1)
        for row in rows:
            self.assertEqual(row['provenance']['model'], 'GPT-5.5')
            self.assertEqual(row['provenance']['source_agent'], 'agav')
            base = population[row['task_id']]
            self.assertEqual(row['provenance']['base_commit'], base['base_commit'])
            self.assertEqual(row['provenance']['repo'], base['repo'])
            self.assertEqual(row['analyzer_commit'], 'de633004011e1b6c8dda81d234baefc024a88b75')
            self.assertEqual(row['analyzer_version'], '0.6.0-beta')
            self.assertEqual(row['analyzer_source_sha256'],
                             'b2b45c86d1cb6ea6b035e697f7191ceaa00bf071f84eb47d1302ab7f2ac21b44')
            self.assertEqual(row['python_version'], '3.14.7')
            self.assertEqual(row['benchmark_tasks'], 300)
            self.assertEqual(row['published_resolved_count'], 186)
            self.assertEqual(row['resolve_rate'], 186 / 300)
            outcome = row['published_outcome']
            self.assertIn(outcome, ('success', 'failure', 'unknown'))
            self.assertEqual(row['resolved'], outcome == 'success')
            self.assertEqual(row['source_result_categories'],
                             ['empty_patch'] if outcome == 'unknown' else [outcome])
            if outcome == 'unknown':
                self.assertEqual(row['analysis_status'], 'empty_patch')
                self.assertEqual(row['evaluation_result'], 'unknown')
                self.assertIsNone(row['metrics'])
                self.assertIsNone(row['human_metrics'])
                self.assertIsNone(row['model_human_ratio'])
            else:
                self.assertEqual(row['analysis_status'], 'ok')
                self.assertEqual(row['metrics']['mode'], 'full_file')
        self.assertEqual([sum(r['published_outcome'] == outcome for r in rows)
                          for outcome in ('success', 'failure', 'unknown')], [186, 85, 29])
        analyzed = [r for r in rows if r['metrics'] is not None]
        self.assertEqual(len(analyzed), 271)
        excluded = [r for r in analyzed if out_of_scope(r['metrics'])]
        self.assertEqual(len(excluded), 9)
        self.assertEqual(sum(r['resolved'] for r in excluded), 1)
        measured = [r for r in analyzed if not out_of_scope(r['metrics'])]
        solved = [r for r in measured if r['resolved']]
        self.assertEqual(len(measured), 262)
        self.assertEqual(len(solved), 185)
        self.assertAlmostEqual(sum(r['metrics']['net_units'] for r in measured) / 262,
                               50.38549618320611)
        self.assertAlmostEqual(sum(r['metrics']['net_units'] for r in solved) / 185,
                               57.52972972972973)

    def test_gpt55_audit_metadata_binds_published_records(self):
        folder = ROOT / 'examples/benchmark-discovery'
        release = json.loads((folder / 'agav-gpt55-release.json').read_text())
        audit_bytes = (folder / 'agav-gpt55-preimages.json').read_bytes()
        review_bytes = (folder / 'agav-gpt55-measurement-review.json').read_bytes()
        self.assertEqual(hashlib.sha256(audit_bytes).hexdigest(), release['preimage_audit_sha256'])
        self.assertEqual(hashlib.sha256(review_bytes).hexdigest(), release['measurement_authorization_sha256'])
        audit = json.loads(audit_bytes)
        review = json.loads(review_bytes)
        self.assertEqual(review['manifest_sha256'], release['preimage_audit_sha256'])
        self.assertEqual(review['approval_scope'], 'external-static-measurement-only')
        rows = {r['task_id']: r for r in
                map(json.loads, (FOLDER / 'gpt-5.5-agav.jsonl').read_text().splitlines())}
        self.assertEqual({r['task_id'] for r in audit['records']}, set(rows))
        self.assertEqual(audit['status_counts'], {'old_blobs_and_hunks_match': 271, 'not_required': 29})
        for item in audit['records']:
            row = rows[item['task_id']]
            for key in ('repo', 'base_commit'):
                self.assertEqual(item[key], row['provenance'][key])
            if item['status'] == 'not_required':
                self.assertIsNone(item['patch_sha256'])
                self.assertEqual(row['provenance']['patch_sha256'], hashlib.sha256(b'').hexdigest())
            else:
                self.assertEqual(item['patch_sha256'], row['provenance']['patch_sha256'])
            for key in ('submission_revision', 'result_sha256', 'prediction_sha256'):
                self.assertEqual(audit[key], row['provenance'][key])
            if row['published_outcome'] != 'unknown':
                self.assertEqual(item['status'], 'old_blobs_and_hunks_match')
                self.assertTrue(item['accepted'])
                self.assertTrue(all(s['index_match'] and s['strict_hunks_match']
                                    for s in item['sources']))
        self.assertEqual(release['footprint']['eligible'], 262)

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
        self.assertEqual(sorted(m['measured_attempts'] for m in data['models']), [262, 276, 287, 288])
        self.assertTrue(all(m['score'] is None and m['rank_range'] for m in data['models']))
        for page in ('index', 'javascript', 'typescript', 'go', 'verified'):
            other = (ROOT / 'site' / (page + '.html')).read_text()
            state = json.loads(re.search(r'type="application/json">(.*?)</script>', other, re.S)[1])
            self.assertTrue(any(link['url'] == 'live.html' for link in state['nav']))
