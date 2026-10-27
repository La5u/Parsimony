import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from parsimony.diagnostics import diagnose, evaluate, markdown, ratio
from parsimony.scoring import freeze
from parsimony.site import same_task, solved_by_task, typical_by_task
from tests.test_scoring import record


def cohort(models=5):
    rows = []
    for i in range(models):
        for t in range(3):
            net = (i + 1) * (t + 1)
            r = record(chr(97 + i), f't{t}', net=net, churn=net)
            r['provenance']['repo'] = f'org/repo{t % 2}'
            rows.append(r)
    return rows


class DiagnosticTests(unittest.TestCase):
    def test_baseline_matches_website_and_does_not_mutate_inputs(self):
        rows = cohort()
        panel = freeze(rows, 'fixture')
        before = copy.deepcopy((panel, rows))
        report = diagnose(panel, rows)
        own = {a: solved_by_task([r for r in rows if r['agent'] == a]) for a in 'abcde'}
        typical = typical_by_task(own)
        for a, m in report['models'].items():
            expected = same_task(own[a], typical, 42)
            self.assertEqual(round(m['ratio'], 3), expected['same_task_net'])
            self.assertEqual(m['comparison_tasks'], expected['same_task_net_tasks'])
            self.assertEqual(m['leave_one_peer_out']['scenarios'], 4)
            self.assertEqual(m['coverage']['eligible_solved_attempts'], 3)
        self.assertEqual((panel, rows), before)
        self.assertIn('not 95% intervals', markdown(report))

    def test_peer_removal_recomputes_three_other_model_gate(self):
        rows = cohort(4)
        report = diagnose(freeze(rows, 'fixture'), rows)
        for m in report['models'].values():
            self.assertIsNotNone(m['ratio'])
            self.assertEqual(m['leave_one_peer_out']['unavailable_scenarios'], 3)
            self.assertIsNone(m['leave_one_peer_out']['rank_range'])

    def test_peer_rank_change_excludes_mechanical_candidate_removal(self):
        rows = cohort(5)
        report = diagnose(freeze(rows, 'fixture'), rows)
        for m in report['models'].values():
            for influence in m['leave_one_peer_out']['top_influences']:
                self.assertEqual(influence['rank_change'], 0)

    def test_task_repeats_are_pooled_before_influence_and_pairwise(self):
        rows = cohort()
        for r in rows:
            r['task_id'] += '#1'
        repeat = copy.deepcopy(rows[0])
        repeat['task_id'] = 't0#2'
        repeat['metrics'].update(net_units=9, churn=9, units_added=9, units_deleted=0)
        rows.append(repeat)
        report = diagnose(freeze(rows, 'fixture'), rows)
        a = report['models']['a']
        self.assertEqual(a['comparison_tasks'], 3)
        self.assertEqual(a['leave_one_task_out']['scenarios'], 3)
        pair = report['pairwise'][0]
        self.assertEqual(pair['shared_solved_measured_tasks'], 3)
        self.assertAlmostEqual(pair['a_net_mean'], (5 + 2 + 3) / 3)
        self.assertEqual(a['coverage']['eligible_solved_attempts'], 4)

    def test_missing_successes_and_failed_attempts_are_not_zero_footprints(self):
        rows = cohort()
        panel = freeze(rows, 'fixture')
        missing = rows[0]
        missing['analysis_status'] = 'fetch_error'
        missing['metrics'] = None
        failed = record('a', 'failed', resolved=False, net=1000, churn=1000)
        rows.append(failed)
        for r in rows:
            if r['agent'] == 'a':
                r['published_resolved_count'] = 4
        report = diagnose(panel, rows)
        c = report['models']['a']['coverage']
        self.assertEqual(c['resolved_records'], 3)
        self.assertEqual(c['eligible_solved_attempts'], 2)
        self.assertEqual(c['published_successes_without_resolved_record'], 1)
        self.assertEqual(c['excluded_success_reasons'], {'fetch_error': 1})
        self.assertEqual(report['models']['a']['comparison_tasks'], 2)

    def test_missing_repository_uses_known_identity_regardless_of_record_order(self):
        rows = cohort()
        panel = freeze(rows, 'fixture')
        rows[0].update(resolved=False, analysis_status='fetch_error', metrics=None, provenance={})
        for ordered in (rows, list(reversed(rows))):
            with self.subTest(missing_first=ordered is rows):
                report = diagnose(panel, ordered)
                self.assertEqual(report['repositories'], 2)
                influences = report['models']['b']['leave_one_repository_out']['top_influences']
                self.assertEqual({r['removed'] for r in influences}, {'org/repo0', 'org/repo1'})

    def test_unknown_repository_bucket_and_conflicting_known_identities(self):
        rows = cohort()
        for r in rows:
            if r['task_id'] == 't0':
                r['provenance']['repo'] = None
        panel = copy.deepcopy(freeze(rows, 'fixture'))
        report = diagnose(panel, rows)
        self.assertEqual(report['repositories'], 3)
        influences = report['models']['a']['leave_one_repository_out']['top_influences']
        self.assertIn('(unknown repository)', {r['removed'] for r in influences})
        rows[0].update(analysis_status='fetch_error', metrics=None)
        rows[3].update(analysis_status='fetch_error', metrics=None)
        rows[0]['provenance']['repo'] = 'org/first'
        rows[3]['provenance']['repo'] = 'org/second'
        with self.assertRaisesRegex(ValueError, 'conflicting repositories for t0'):
            diagnose(panel, rows)

    def test_scope_exclusions_are_disclosed(self):
        rows = cohort()
        panel = copy.deepcopy(freeze(rows, 'fixture'))
        rows[0]['metrics'].update(touched_files=['test.py'], excluded_files=['test.py'])
        result = diagnose(panel, rows)
        self.assertEqual(result['models']['a']['coverage']['excluded_success_reasons'], {'out_of_scope': 1})

    def test_reports_task_and_repository_rank_reversals(self):
        rows = []
        for a in 'abcde':
            for t in (0, 1):
                net = (1 if t == 0 else 100) if a == 'a' else 10
                r = record(a, f't{t}', net=net, churn=net)
                r['provenance']['repo'] = f'org/repo{t}'
                rows.append(r)
        report = diagnose(freeze(rows, 'fixture'), rows)
        a = report['models']['a']
        self.assertEqual(a['rank'], 5)
        self.assertEqual(a['leave_one_task_out']['rank_range'], [1, 5])
        self.assertEqual(a['leave_one_repository_out']['rank_range'], [1, 5])
        influence = a['leave_one_task_out']['top_influences'][0]
        self.assertEqual(influence['removed'], 't1')
        self.assertEqual(influence['rank_change'], -4)
        self.assertAlmostEqual(influence['ratio'], 0.1)

    def test_zero_and_negative_denominators_are_unavailable(self):
        self.assertIsNone(ratio([(1, 0)]))
        self.assertIsNone(ratio([(1, -2)]))
        self.assertIsNone(ratio([]))
        self.assertEqual(ratio([(-2, 1)]), -2)
        own = {a: {'t': (-1, 0)} for a in 'abcd'}
        values, ranks, _ = evaluate(own)
        self.assertTrue(all(v is None for v in values.values()))
        self.assertTrue(all(v is None for v in ranks.values()))

    def test_ranks_use_displayed_ratio_ties(self):
        own = {a: {'t': (v, 0)} for a, v in zip('abcd', (1, 1.00001, 2, 3))}
        _, ranks, _ = evaluate(own)
        self.assertEqual(ranks['a'], ranks['b'])
        self.assertEqual(ranks['c'], 3)

    def test_validation_rejects_duplicates_and_conflicting_counts(self):
        rows = cohort()
        panel = freeze(rows, 'fixture')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            diagnose(panel, rows + [rows[0]])
        rows[0]['published_resolved_count'] = 3
        rows[1]['published_resolved_count'] = 4
        with self.assertRaisesRegex(ValueError, 'conflicting published'):
            diagnose(panel, rows)

    def test_published_reports_match_website_ratios_and_coverage(self):
        root = Path(__file__).resolve().parents[1]
        pages = {'deepswe-python': 'python', 'deepswe-javascript': 'javascript',
                 'deepswe-typescript': 'typescript', 'deepswe-go': 'go',
                 'verified': 'verified', 'live-python': 'live', 'live-javascript': 'live-javascript',
                 'live-typescript': 'live-typescript', 'live-go': 'live-go', 'sweeper-php': 'sweeper-php',
                 'polybench-python': 'polybench-python'}
        for name, page in pages.items():
            with self.subTest(board=name):
                report = json.loads((root / 'examples/ranking-diagnostics' / (name + '.json')).read_text())
                html = (root / 'site' / (page + '.html')).read_text()
                data = json.loads(html.split('<script id="parsimony-data" type="application/json">', 1)[1].split('</script>', 1)[0])
                self.assertEqual(set(report['models']), {m['agent'] for m in data['models']})
                for model in data['models']:
                    diagnostic = report['models'][model['agent']]
                    value = diagnostic['ratio']
                    self.assertEqual(None if value is None else round(value, 3), model['same_task_net'])
                    self.assertEqual(diagnostic['comparison_tasks'], model['same_task_net_tasks'])
                    self.assertEqual(diagnostic['coverage']['eligible_solved_attempts'], model['measured_solved_attempts'])
                    self.assertEqual(diagnostic['coverage']['published_resolved_attempts'], model['upstream_solved_attempts'])
                if name != 'deepswe-go':  # this board's inputs are an external checksum-bound release
                    directory = root / 'examples' / ('mini-swe-agent-500' if name == 'verified' else name)
                    for source in report['inputs']:
                        raw = (directory / source['file']).read_bytes()
                        self.assertEqual(hashlib.sha256(raw).hexdigest(), source['sha256'])

    def test_cli_writes_reproducible_json_markdown_and_input_hashes(self):
        rows = cohort()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            panel = tmp / 'panel.json'
            panel.write_text(json.dumps(freeze(rows, 'fixture')))
            records = tmp / 'records.jsonl'
            records.write_text(''.join(json.dumps(r) + '\n' for r in rows))
            output = tmp / 'diagnostics.json'
            cmd = [sys.executable, '-m', 'parsimony.diagnostics', str(panel), str(records), '--output', str(output)]
            subprocess.run(cmd, check=True, capture_output=True)
            first = output.read_bytes(), output.with_suffix('.md').read_bytes()
            subprocess.run(cmd, check=True, capture_output=True)
            self.assertEqual(first, (output.read_bytes(), output.with_suffix('.md').read_bytes()))
            self.assertEqual(len(json.loads(first[0])['inputs']), 2)
            self.assertEqual(len(json.loads(first[0])['inputs'][0]['sha256']), 64)
