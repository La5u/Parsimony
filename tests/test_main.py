import json
import platform
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from parsimony.__main__ import main
from parsimony.benchmark import ANALYZER_VERSION


class ResumeTests(unittest.TestCase):
    def test_resume_keeps_prior_record_and_only_fetches_missing_task(self):
        with tempfile.TemporaryDirectory() as temp:
            dataset = Path(temp) / 'dataset.jsonl'
            dataset.write_text(''.join(json.dumps({'instance_id': t, 'repo': 'org/repo',
                                                    'base_commit': 'abc'}) + '\n' for t in ('a', 'b')))
            output = Path(temp) / 'results.jsonl'
            previous = dict(agent='agent', task_id='a', analyzer_version=ANALYZER_VERSION,
                            python_version=platform.python_version(), published_resolved_count=1,
                            resolved=True, analysis_status='ok', provenance={'ref': 'commit', 'results_sha256': 'hash'})
            output.write_text(json.dumps(previous) + '\n')
            submission = dict(agent='agent', resolved={'a'}, provenance={'results_sha256': 'hash'})
            def load(_name, _cache, _ref, task_ids, limit, include_failed):
                self.assertEqual(task_ids, ['b'])
                self.assertTrue(include_failed)
                return submission
            def analyze(_submission, _cache, _metadata, _limit, _patch_only, task_ids, include_failed):
                self.assertEqual(task_ids, ['b'])
                yield previous
                yield {'agent': 'agent', 'task_id': 'b'}
            args = ['parsimony', 'analyze', 'example', '--dataset', str(dataset), '--patch-only',
                    '--ref', 'commit', '--include-failed', '--resume', '--output', str(output)]
            with patch('sys.argv', args), patch('parsimony.__main__.load_submission', side_effect=load), \
                 patch('parsimony.__main__.analyze_submission', side_effect=analyze):
                main()
            rows = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual([r['task_id'] for r in rows], ['a', 'b'])

    def test_resume_retries_fetch_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            dataset = Path(temp) / 'dataset.jsonl'
            dataset.write_text(''.join(json.dumps({'instance_id': t, 'repo': 'org/repo',
                                                    'base_commit': 'abc'}) + '\n' for t in ('a', 'b')))
            output = Path(temp) / 'results.jsonl'
            common = dict(agent='agent', analyzer_version=ANALYZER_VERSION, python_version=platform.python_version(),
                          published_resolved_count=2, resolved=True, provenance={'ref': 'main', 'results_sha256': 'hash'})
            output.write_text(json.dumps({**common, 'task_id': 'a', 'analysis_status': 'ok'}) + '\n' +
                              json.dumps({**common, 'task_id': 'b', 'analysis_status': 'fetch_error'}) + '\n')
            submission = dict(agent='agent', resolved={'a', 'b'}, provenance={'results_sha256': 'hash'})
            def analyze(_submission, _cache, _metadata, _limit, _patch_only, task_ids, include_failed):
                self.assertEqual(task_ids, ['b'])
                yield {'agent': 'agent', 'task_id': 'b', 'analysis_status': 'ok'}
            args = ['parsimony', 'analyze', 'example', '--dataset', str(dataset), '--patch-only',
                    '--resume', '--output', str(output)]
            with patch('sys.argv', args), patch('parsimony.__main__.load_submission', return_value=submission), \
                 patch('parsimony.__main__.analyze_submission', side_effect=analyze):
                main()
            rows = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual([(r['task_id'], r['analysis_status']) for r in rows], [('a', 'ok'), ('b', 'ok')])


if __name__ == '__main__':
    unittest.main()
