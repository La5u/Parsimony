"""Offline bindings for the separately versioned scalar-only Go release."""
import hashlib
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / 'examples/deepswe-go-v2'


class GoPublicationTests(unittest.TestCase):
    def test_population_and_validation_are_bound_to_the_clean_analyzer(self):
        population = json.loads((RELEASE / 'population.json').read_bytes())
        validation = json.loads((RELEASE / 'validation-summary.json').read_bytes())
        self.assertEqual(population['analyzer_commit'], validation['analyzer_commit'])
        self.assertEqual(population['python_version'], '3.14.7')
        self.assertEqual(population['dataset_sha256'], validation['dataset_sha256'])
        self.assertEqual(population['task_count'], 136)
        self.assertEqual(len(population['tasks']), 136)
        self.assertEqual(validation['records'], 3536)
        self.assertEqual(validation['unchanged_outcome_and_provenance_bindings'], 3536)
        self.assertEqual(validation['unchanged_common_primary_measurements'], 3502)
        self.assertEqual(validation['new_statuses'],
                         {'ok': 3508, 'error': 1, 'missing_patch': 2, 'not_resolved': 25})
        self.assertEqual(len(validation['recovered']), 6)
        self.assertEqual(sum(row['resolved'] for row in validation['recovered']), 5)
        self.assertEqual(validation['remaining_errors'][0]['task_id'], 'helm-array-merge-strategies#2')
        self.assertEqual(population['measurement_track'], validation['measurement_track'])
        self.assertEqual(population['measurement_track']['unit_version'], 'tree-sitter-go-units-v2')
        historical = json.loads((ROOT / 'examples/deepswe-go/population.json').read_bytes())
        self.assertNotEqual(population['analyzer_commit'], historical['analyzer_commit'])
        self.assertNotEqual(population['measurement_track'], historical['measurement_track'])
        self.assertEqual(population['tasks'], historical['tasks'])
        self.assertEqual(population['dataset_sha256'], historical['dataset_sha256'])

    def test_page_matches_all_configurations_and_recovered_measurements(self):
        page = (ROOT / 'site/go.html').read_text()
        embedded = re.search(r'<script id="parsimony-data" type="application/json">(.*?)</script>', page, re.S)
        self.assertIsNotNone(embedded)
        data = json.loads(embedded.group(1))
        self.assertEqual(data['analyzer_version'], '0.8.0-beta')
        self.assertEqual(data['measurement_track']['unit_version'], 'tree-sitter-go-units-v2')
        self.assertEqual(len(data['models']), 38)  # 26 release-asset v1.1 configurations + 12 DeepSWE 1.0
        self.assertEqual(data['population_count'], 136)
        comparison = json.loads((RELEASE / 'comparison-summary.json').read_bytes())
        v11 = [m for m in data['models'] if not m['agent'].startswith('deepswe-v1.0_')]
        self.assertEqual(len(v11), 26)
        for model in v11:
            filename = model['agent'].split('_mini_swe_agent_', 1)[1] + '.jsonl'
            measured = comparison[filename]['new']
            self.assertEqual(model['measured_attempts'], measured['eligible'])
            self.assertEqual(model['measured_net_mean'], measured['measured_net_mean'])
            self.assertEqual(model['measured_solved_net_mean'], measured['measured_solved_net_mean'])
            self.assertEqual(model['upstream_solved_attempts'], measured['outcomes']['resolved'])
        self.assertEqual(sum(m['measured_attempts'] for m in v11), 3508)
        source = next(s for s in data['sources'] if s['language'] == 'go')
        self.assertIn('/examples/deepswe-go-v2/', source['report_url'])
        self.assertEqual(source['manifest_sha256'], hashlib.sha256((RELEASE / 'population.json').read_bytes()).hexdigest())

    def test_committed_metadata_matches_release_asset_bindings(self):
        manifest = json.loads((RELEASE / 'release-assets.json').read_bytes())
        self.assertTrue(manifest['archive_url'].startswith('https://github.com/La5u/Parsimony/releases/download/'))
        self.assertGreater(manifest['archive_bytes'], 0)
        self.assertEqual(len(manifest['archive_sha256']), 64)
        for name, binding in manifest['files'].items():
            path = RELEASE / name
            if path.exists():
                raw = path.read_bytes()
                frozen = f'{path} is part of a frozen release (release-assets.json); revert your edit to it'
                self.assertEqual(len(raw), binding['bytes'], frozen)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), binding['sha256'], frozen)
        self.assertEqual(len([name for name in manifest['files'] if name.endswith('.jsonl')]), 26)
        self.assertIn('score-panel.json', manifest['files'])
        self.assertIn('record-comparison.json', manifest['files'])
        self.assertIn('sensitivity.json', manifest['files'])
        self.assertNotIn('dataset.jsonl', manifest['files'])  # human patch text is not redistributed
