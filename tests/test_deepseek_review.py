import importlib.util
import json
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location(
    'deepseek_review', Path(__file__).resolve().parents[1] / 'examples/benchmark-discovery/review-deepseek-live.py')
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


class ReviewTests(unittest.TestCase):
    def fixture(self, resolved=False, patch=b'patch'):
        row = dict(task_id='task', patch='patch', repo='org/repo', base_commit='a' * 40,
                   published_outcome='failure')
        meta = dict(instance_id='task', repo='org/repo', base_commit='a' * 40,
                    model='tianxi-agent-plan/deepseek-flash', binary_version='0.1.423')
        values = [patch, json.dumps(meta).encode(), json.dumps(dict(instance_id='task', resolved=resolved)).encode()]
        class Cache:
            def get(self, url):
                return values[0 if url.endswith('patch.diff') else 1 if url.endswith('meta.json') else 2]
        return row, Cache()

    def test_archived_static_and_scope_counts_are_not_conflated(self):
        path = Path(__file__).resolve().parents[1] / 'examples/priority-live/measurement-summary.json'
        cohorts = json.loads(path.read_text())['cohorts']
        for cohort in cohorts.values():
            if 'static_analysis_outcome_counts' not in cohort:
                continue
            static = sum(cohort['static_analysis_outcome_counts'].values())
            excluded = sum(cohort['out_of_scope_outcome_counts'].values())
            eligible = sum(cohort['footprint_eligible_outcome_counts'].values())
            self.assertEqual(cohort['footprint_eligible_count'], eligible)
            self.assertEqual(static, eligible + excluded)
            self.assertLessEqual(static, cohort['population'])
        deepseek = cohorts['deepseek_v4_1_flash']
        self.assertEqual(deepseek['footprint_eligible_count'], 287)
        self.assertEqual(deepseek['out_of_scope_outcome_counts'], {'failed': 6, 'resolved': 2})

    def test_explicit_failed_report_and_exact_patch_match(self):
        row, cache = self.fixture()
        result = review.audit_row(row, cache, 'https://example.com/pinned')
        self.assertTrue(all(result['checks'].values()))
        self.assertEqual(len(result['sources']), 3)
        self.assertTrue(all(len(s['sha256']) == 64 for s in result['sources']))
        self.assertNotIn('patch', result)

    def test_falsey_report_not_inferred_as_explicit_failure(self):
        row, cache = self.fixture(resolved=0)
        self.assertFalse(review.audit_row(row, cache, 'https://example.com')['checks']['report_outcome'])

    def test_differing_raw_patch_not_silently_normalized(self):
        row, cache = self.fixture(patch=b'patch\n')
        self.assertFalse(review.audit_row(row, cache, 'https://example.com')['checks']['patch_agreement'])
