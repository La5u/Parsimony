import json
import tempfile
import unittest
from pathlib import Path

from parsimony.release import audit, freeze_dataset


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dataset = Path(self.tmp.name) / 'data.jsonl'
        self.dataset.write_text(json.dumps({'instance_id': 'a', 'repo': 'org/repo',
                                            'base_commit': 'abc', 'patch': ''}) + '\n')
        self.panel = freeze_dataset(self.dataset, 'beta-test', analyzer_commit='a' * 40)
        self.record = dict(agent='model', task_id='a', python_version=self.panel['python_version'],
                           analyzer_version='0.1.0', published_resolved_count=1,
                           benchmark_tasks=1, resolve_rate=1.0, resolved=True,
                           analysis_status='ok', metrics={'mode': 'full_file', 'excluded_files': ['README.md']},
                           provenance={'repo': 'org/repo', 'base_commit': 'abc'})

    def test_coverage_and_exclusions(self):
        result = audit(self.panel, [self.record], self.dataset)
        row = result['agents'][0]
        self.assertEqual((row['successful_analyses'], row['missing_records']), (1, 0))
        self.assertEqual(row['excluded_files'], ['README.md'])
        missing = audit(self.panel, [{**self.record, 'analysis_status': 'error', 'metrics': None}])
        self.assertEqual(missing['agents'][0]['resolved_missing_analysis'], 1)

    def test_rejects_wrong_dataset_and_duplicate_records(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            audit(self.panel, [self.record, self.record])
        self.dataset.write_text(self.dataset.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            audit(self.panel, [self.record], self.dataset)

    def test_rejects_wrong_base_and_resolve_count(self):
        with self.assertRaisesRegex(ValueError, 'base commit'):
            audit(self.panel, [{**self.record, 'provenance': {'repo': 'org/repo', 'base_commit': 'wrong'}}])
        with self.assertRaisesRegex(ValueError, 'totals disagree'):
            audit(self.panel, [{**self.record, 'resolved': False}])

    def test_analyzer_commit_enforced_when_recorded(self):
        with self.assertRaisesRegex(ValueError, 'analyzer commit'):
            audit(self.panel, [{**self.record, 'analyzer_commit': 'b' * 40}])
        row = audit(self.panel, [{**self.record, 'analyzer_commit': 'a' * 40}])['agents'][0]
        self.assertEqual(row['unverified_analyzer_commit_records'], 0)
        self.assertEqual(audit(self.panel, [self.record])['agents'][0]['unverified_analyzer_commit_records'], 1)

    def test_out_of_scope_and_value_only_counts(self):
        hidden = {**self.record, 'metrics': {'mode': 'full_file', 'churn': 0, 'structural_churn': 0,
                                             'touched_files': ['setup.py'], 'excluded_files': ['setup.py']}}
        row = audit(self.panel, [hidden])['agents'][0]
        self.assertEqual((row['out_of_scope_successes'], row['zero_normalized_edit_records']), (1, 1))
        renamed = {**self.record, 'metrics': {'mode': 'full_file', 'churn': 2, 'structural_churn': 0,
                                              'touched_files': ['a.py'], 'excluded_files': []}}
        self.assertEqual(audit(self.panel, [renamed])['agents'][0]['value_only_edit_records'], 1)

    def test_dataset_population_is_unique(self):
        self.dataset.write_text(self.dataset.read_text() * 2)
        with self.assertRaisesRegex(ValueError, 'unique'):
            freeze_dataset(self.dataset, 'bad', analyzer_commit='a' * 40)


if __name__ == '__main__':
    unittest.main()
