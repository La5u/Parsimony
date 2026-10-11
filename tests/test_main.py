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

    def test_resume_preserves_retry_evidence_on_load_or_binding_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            dataset = Path(temp) / 'dataset.jsonl'
            dataset.write_text(json.dumps({'instance_id': 'a', 'repo': 'org/repo',
                                           'base_commit': 'abc'}) + '\n')
            output = Path(temp) / 'results.jsonl'
            previous = dict(agent='agent', task_id='a', analyzer_version=ANALYZER_VERSION,
                            python_version=platform.python_version(), published_resolved_count=1,
                            resolved=True, analysis_status='fetch_error',
                            provenance={'ref': 'main', 'results_sha256': 'original'})
            payload = json.dumps(previous) + '\n'
            args = ['parsimony', 'analyze', 'example', '--dataset', str(dataset),
                    '--resume', '--output', str(output)]
            cases = [OSError('offline'),
                     dict(agent='agent', resolved={'a'}, provenance={'results_sha256': 'changed'}),
                     dict(agent='other', resolved={'a'}, provenance={'results_sha256': 'original'})]
            for result in cases:
                with self.subTest(result=result):
                    output.write_text(payload)
                    options = {'side_effect': result} if isinstance(result, Exception) else {'return_value': result}
                    with patch('sys.argv', args), patch('parsimony.__main__.load_submission', **options), \
                         patch('parsimony.__main__.analyze_submission') as analyze, self.assertRaises(SystemExit):
                        main()
                    analyze.assert_not_called()
                    self.assertEqual(output.read_text(), payload)

    def test_resume_rejects_other_analyzer_source(self):
        with tempfile.TemporaryDirectory() as temp:
            dataset = Path(temp) / 'dataset.jsonl'
            dataset.write_text(json.dumps({'instance_id': 'a', 'repo': 'org/repo', 'base_commit': 'abc'}) + '\n')
            output = Path(temp) / 'results.jsonl'
            output.write_text(json.dumps(dict(agent='agent', task_id='a', analyzer_version=ANALYZER_VERSION,
                                              python_version=platform.python_version(), analyzer_commit=None,
                                              analyzer_source_sha256='0' * 64, analysis_status='ok',
                                              provenance={'ref': 'main'})) + '\n')
            args = ['parsimony', 'analyze', 'example', '--dataset', str(dataset), '--resume', '--output', str(output)]
            with patch('sys.argv', args), self.assertRaises(SystemExit):
                main()


if __name__ == '__main__':
    unittest.main()
