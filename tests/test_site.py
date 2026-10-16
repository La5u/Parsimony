import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from parsimony.scoring import freeze
from parsimony.benchmark import read_jsonl
from parsimony.site import (add_rank_ranges, build, build_merged, company, label, main, merged_ratio, newest_generation,
                            published_sources, render)
from tests.test_scoring import record


class SiteTests(unittest.TestCase):
    def test_published_sources_counts_and_hashes(self):
        root = Path(__file__).resolve().parent.parent
        sources = published_sources('deepswe', root=root)
        *sources, self_run = sources  # the owner-run pilot is listed last, never as a frozen board
        self.assertEqual([s['tasks'] for s in sources], [34, 5, 35, 34, 500, 300, 108, 111, 138, 128])
        self.assertEqual([s['population_per_model'] for s in sources], [136, 20, 140, 136, 500, 300, 108, 111, 138, 128])
        self.assertEqual([s['attempts_per_task'] for s in sources], [4, 4, 4, 4, 1, 1, 1, 1, 1, 1])
        self.assertIn('/examples/deepswe-go-v2/', sources[3]['manifest_url'])
        go_population = json.loads((root / 'examples/deepswe-go-v2/population.json').read_bytes())
        self.assertEqual(go_population['measurement_track']['unit_version'], 'tree-sitter-go-units-v2')
        self.assertEqual([s['board_url'] for s in sources],
                         ['python.html', 'javascript.html', 'typescript.html', 'go.html', 'verified.html', 'live.html', 'live-javascript.html', 'live-typescript.html', 'live-go.html', 'sweeper-php.html'])
        plan = (root / 'examples/self-run/plan.json').read_bytes()
        self.assertTrue(self_run['self_run'])
        self.assertFalse(self_run['active'])
        self.assertEqual((self_run['tasks'], self_run['attempts_per_task'], self_run['population_per_model']), (10, 2, '10–20'))
        self.assertEqual(self_run['manifest_sha256'], hashlib.sha256(plan).hexdigest())
        self.assertEqual(self_run['deepswe_commit'], json.loads(plan)['deepswe_commit'])
        for source in sources:
            path = source['manifest_url'].split('/blob/main/')[1]
            raw = (root / path).read_bytes()
            self.assertEqual(source['manifest_sha256'], hashlib.sha256(raw).hexdigest(),
                             f'{path} changed but site/ was not rebuilt; run scripts/rebuild-site.sh')
            self.assertEqual(source['dataset_sha256'], json.loads(raw)['dataset_sha256'])
            self.assertEqual(source['report_url'], source['manifest_url'].rsplit('/', 1)[0] + '/README.md')

    def test_codex_self_runs_share_their_pi_runs_external_scores(self):
        page = (Path(__file__).resolve().parents[1] / 'site' / 'index.html').read_text()
        raw = page.split('<script id="parsimony-data" type="application/json">', 1)[1].split('</script>', 1)[0]
        models = {m['agent']: m for m in json.loads(raw)['self_run_models']}
        codex = [a for a in models if '_codex_' in a]
        self.assertTrue(codex)
        for agent in codex:
            pi = models[agent.replace('_codex_', '_pi_', 1)]
            self.assertIsNotNone(models[agent]['aa_intelligence'], agent)
            self.assertEqual(models[agent]['aa_intelligence'], pi['aa_intelligence'])

    def test_published_sources_active_board(self):
        for benchmark, language, index in [('deepswe', 'python', 0), ('deepswe', 'javascript', 1),
                                            ('deepswe', 'typescript', 2), ('deepswe', 'go', 3),
                                            ('verified', 'python', 4), ('live', 'python', 5),
                                            ('polybench', 'python', None)]:
            sources = published_sources(benchmark, language)
            self.assertEqual([i for i, s in enumerate(sources) if s['active']],
                             [] if index is None else [index])

    def test_published_sources_reads_only_manifests_and_validates_attempts(self):
        root = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            for source in published_sources('live'):
                path = source['manifest_url'].split('/blob/main/')[1]
                target = temporary / path
                target.parent.mkdir(parents=True)
                shutil.copyfile(root / path, target)
            # No success panels or records exist in this root.
            self.assertEqual(published_sources('live', root=temporary), published_sources('live'))
            path = temporary / 'examples/deepswe-python/population.json'
            manifest = json.loads(path.read_bytes())
            manifest['tasks'].pop(next(iter(manifest['tasks'])))
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'four attempts'):
                published_sources('live', root=temporary)

    def test_build_and_render(self):
        records = [record('20260217_mini-v2.0.0_claude-4-6-opus', 't1', net=5, churn=9),
                   record('20260217_mini-v2.0.0_claude-4-6-opus', 't2', net=0, churn=0, resolved=False),
                   record('other-agent', 't1', net=10, churn=30),
                   record('other-agent', 't2', net=3, churn=3)]
        panel = freeze(records, 'site-test')
        data = build(panel, records, draws=50)
        # Footprint rank ignores correctness: Opus has the smaller measured mean.
        self.assertEqual([m['name'] for m in data['models']], ['Claude Opus 4.6', 'other-agent'])
        opus = data['models'][0]
        self.assertEqual((opus['solved'], opus['failed']), (1, 1))
        self.assertEqual((opus['solved_net_mean'], opus['solved_churn_mean']), (5, 9))
        self.assertEqual((opus['measured_net_mean'], opus['measured_churn_mean']), (2.5, 4.5))
        self.assertEqual(opus['measured_attempts'], 2)
        self.assertEqual(opus['company'], 'Anthropic')
        self.assertLessEqual(opus['ci'][0], opus['score'])
        self.assertEqual([t[0] for t in data['tasks']], ['t1', 't2'])
        self.assertEqual((data['references'], data['harness']), (2, ['v2.0.0']))
        self.assertEqual([cell[0] for cell in data['tasks'][1][2]], ['f', 'r'])
        # Archived score order differs from footprint order; task cells must follow model order.
        self.assertLess(opus['score'], data['models'][1]['score'])
        self.assertEqual([cell[1] for cell in data['tasks'][0][2]], [5, 10])
        self.assertEqual([cell[1] for cell in data['tasks'][1][2]], [0, 3])
        page = render(data)
        self.assertTrue(page.startswith('<!doctype html>'))
        embedded = page.split('type="application/json">')[1].split('</script>')[0]
        self.assertEqual(json.loads(embedded)['panel'], 'site-test')
        self.assertFalse(render(data, standalone=False).startswith('<!doctype'))
        hostile = render({**data, 'panel': '</script><script>alert(1)</script>'})
        self.assertEqual(hostile.count('</script>'), page.count('</script>'))

    def test_document_head_titles_navigation_and_fallback(self):
        from html.parser import HTMLParser
        from parsimony.site import BENCHMARKS

        class Structure(HTMLParser):
            def __init__(self):
                super().__init__()
                self.in_head = False
                self.metadata = []

            def handle_starttag(self, tag, attrs):
                if tag == 'head':
                    self.in_head = True
                if tag in {'title', 'meta', 'style'}:
                    self.metadata.append((tag, self.in_head))

            def handle_endtag(self, tag):
                if tag == 'head':
                    self.in_head = False

        for benchmark, language, expected in [
                ('deepswe', 'python', 'DeepSWE · Python'),
                ('deepswe', 'javascript', 'DeepSWE · JavaScript'),
                ('deepswe', 'typescript', 'DeepSWE · TypeScript'),
                ('deepswe', 'go', 'DeepSWE · Go'),
                ('verified', 'python', 'SWE-bench Verified · Python'),
                ('live', 'python', 'SWE-bench Live Lite · Python')]:
            data = dict(models=[], tasks=[], benchmark=BENCHMARKS[benchmark],
                        measurement_track=dict(language=language))
            page = render(data)
            parser = Structure()
            parser.feed(page)
            self.assertEqual(parser.metadata, [('meta', True), ('meta', True), ('title', True),
                                                ('meta', True)] + [('meta', True)] * 10 + [('style', True)])
            self.assertIn(f'<title>Parsimony: {expected}</title>', page)
            self.assertIn('<nav id="nav" aria-label="Leaderboards"', page)
            self.assertIn('<noscript>', page)
            self.assertIn('The charts and leaderboard need JavaScript', page)
            for fragment_tag in ('rel="canonical" href="https://parsimony.lasu.dev/"', 'property="og:site_name" content="Parsimony"',
                                 'name="twitter:card" content="summary_large_image"', 'property="og:image" content="https://parsimony.lasu.dev/og.png?v=2026-10-16"', 'property="og:url" content="https://parsimony.lasu.dev/"'):
                self.assertIn(fragment_tag, page)
            fragment = render(data, standalone=False)
            self.assertNotIn('<head>', fragment)
            self.assertNotIn('<body>', fragment)
            self.assertNotIn('<!-- BODY -->', fragment)
            self.assertIn(f'<title>Parsimony: {expected}</title>', fragment)
        index = render(data, page_name='site/index.html')
        self.assertIn('<title>Parsimony: which AI coding agent changes the least code?</title>', index)
        self.assertIn('property="og:title" content="Parsimony: which AI coding agent changes the least code?"', index)
        other = render(data, page_name='go.html')
        self.assertIn('rel="canonical" href="https://parsimony.lasu.dev/go"', other)
        self.assertIn('property="og:url" content="https://parsimony.lasu.dev/go"', other)
        hostile = render(dict(benchmark=dict(name='</title><script>bad</script>')))
        self.assertIn('&lt;/title&gt;&lt;script&gt;bad&lt;/script&gt;', hostile)
        self.assertEqual(hostile.count('</title>'), 1)

    def test_example_and_custom_importer_are_embedded(self):
        import html
        import re

        page = render({'models': [], 'tasks': []})
        self.assertNotIn('__CUSTOM_BENCHMARK_JS__', page)
        self.assertIn('id="custom-file"', page)
        self.assertIn('function validateBenchmark(data)', page)
        self.assertNotIn('id="coverage-note"', page)
        self.assertNotIn("$('rank-head')", page)
        examples = re.findall(r'<pre><code>(.*?)</code></pre>', page, re.S)
        self.assertEqual(len(examples), 2)
        functions = []
        for example in examples:
            namespace = {}
            exec(html.unescape(example), namespace)
            functions.append(namespace['has_negative'])
        for values, expected in [([], False), ([0, 2], False), ([3, -1, 2], True), ([-1], True)]:
            for function in functions:
                self.assertEqual(function(values), expected)

    def test_confidence_intervals_do_not_affect_scores_or_order(self):
        records = [record('a', 't1', net=1, churn=1), record('a', 't2', net=2, churn=2),
                   record('b', 't1', net=9, churn=9), record('b', 't2', resolved=False)]
        panel = freeze(records, 'ci-independent')
        missing = record('c', 't1')
        missing.update(metrics=None, analysis_status='fetch_error')
        records.append(missing)
        before = build(panel, records, draws=20)
        intervals = {a: dict(ci=[-9999, 9999], top=0) for a in ('a', 'b', 'c')}
        with mock.patch('parsimony.site.bootstrap', return_value=(2, intervals)):
            after = build(panel, records, draws=20)
        for first, second in zip(before['models'], after['models']):
            for key in ('agent', 'score', 'lower', 'upper'):
                self.assertEqual(first[key], second[key], key)
            self.assertNotEqual(first['ci'], second['ci'])

    def test_footprint_means_include_failures_and_tasks_without_references(self):
        records = [record('a', 't1', net=2, churn=4), record('a', 't2', net=6, churn=8),
                   record('a', 't3', net=100, churn=100, resolved=False),
                   record('b', 't3', net=1, churn=1)]
        panel = freeze(records, 'plot-test')
        records += [record('a', 'outside', net=999, churn=999)]
        data = build(panel, records, draws=20)
        a = next(m for m in data['models'] if m['agent'] == 'a')
        self.assertEqual((a['solved_net_mean'], a['solved_churn_mean']), (4, 6))
        self.assertEqual((a['net_units'], a['churn']), (4, 6))
        self.assertEqual(data['excluded_tasks'], ['outside'])
        self.assertEqual(a['measured_net_mean'], 1107 / 4)
        # Solved-only mean covers every measured solved attempt, including tasks outside the score panel.
        self.assertEqual((a['measured_solved_net_mean'], a['measured_solved_attempts']), (1007 / 3, 3))
        self.assertEqual(a['measured_churn_mean'], 1111 / 4)
        self.assertEqual(a['measured_attempts'], 4)
        self.assertEqual(a['footprint_population_count'], 4)
        self.assertEqual({t[0] for t in data['footprint_tasks']}, {'t1', 't2', 't3', 'outside'})
        for r in records:
            if r['agent'] == 'a' and r['task_id'] in ('t1', 't2'):
                r['analysis_status'] = 'fetch_error'
                r['metrics'] = None
        data = build(panel, records, draws=20)
        a = next(m for m in data['models'] if m['agent'] == 'a')
        self.assertIsNone(a['solved_net_mean'])
        self.assertIsNone(a['solved_churn_mean'])
        self.assertIsNone(a['churn'])
        # Failed attempts remain in the model point; missing measurements do not become zeros.
        self.assertEqual((a['measured_net_mean'], a['measured_churn_mean']), (549.5, 549.5))
        self.assertEqual(a['measured_attempts'], 2)
        i = next(i for i, m in enumerate(data['models']) if m['agent'] == 'a')
        t1 = next(t for t in data['tasks'] if t[0] == 't1')
        self.assertEqual(t1[2][i][3:], [None, 1, 100])

    def test_solved_footprint_counts_attempts_and_upstream_denominator(self):
        records = [record('a', 'task#1', net=2, churn=4),
                   record('a', 'task#2', net=8, churn=12),
                   record('a', 'task#3', net=-90, churn=90, resolved=False),
                   record('a', 'task#4', net=100, churn=100)]
        records[-1].update(metrics=None, analysis_status='fetch_error')
        refs = [record('reference', f'task#{i}') for i in range(1, 5)]
        panel = freeze(refs, 'repeated-attempts')
        data = build(panel, records, draws=20)
        model = data['models'][0]
        self.assertEqual(model['upstream_solved_attempts'], 3)
        self.assertEqual(model['measured_solved_attempts'], 2)
        self.assertEqual(model['measured_solved_net_mean'], 5)
        self.assertEqual(model['measured_solved_churn_mean'], 8)
        self.assertEqual(model['measured_attempts'], 3)
        self.assertEqual(model['footprint_population_count'], 4)
        # Published correctness counts cover attempts whose footprints are unavailable.
        for r in records:
            r.update(published_resolved_count=7, benchmark_tasks=12)
        model = build(panel, records, draws=20)['models'][0]
        self.assertEqual(model['upstream_solved_attempts'], 7)
        self.assertEqual(model['footprint_population_count'], 12)
        self.assertEqual(model['measured_solved_attempts'], 2)
        self.assertEqual(model['measured_solved_churn_mean'], 8)

    def test_footprint_ranking_retains_missing_population_and_failed_noops(self):
        refs = [record('a', 't1', net=9, churn=9), record('a', 't2', net=8, churn=8)]
        panel = freeze(refs, 'missing-population')
        missing = record('c', 't1')
        missing.update(metrics=None, analysis_status='fetch_error')
        data = build(panel, [refs[0], record('b', 't1', net=0, churn=0, resolved=False), missing], draws=20)
        self.assertEqual(data['ranking_metric'], 'same-task-net-ratio-v1')
        self.assertEqual([m['agent'] for m in data['models']], ['a', 'b', 'c'])  # too few models for a same-task ratio: solved mean, unmeasured last
        self.assertEqual([m['measured_net_mean'] for m in data['models']], [9, 0, None])  # the failed no-op is kept
        self.assertEqual([m['measured_solved_net_mean'] for m in data['models']], [9, None, None])
        self.assertEqual([m['measured_attempts'] for m in data['models']], [1, 1, 0])
        self.assertEqual([m['upstream_solved_attempts'] for m in data['models']], [1, 0, 1])
        self.assertEqual([m['measured_solved_attempts'] for m in data['models']], [1, 0, 0])
        self.assertEqual([m['measured_solved_churn_mean'] for m in data['models']], [9, None, None])
        self.assertEqual([m['footprint_population_count'] for m in data['models']], [2, 2, 2])
        self.assertEqual([row[0] for row in data['footprint_tasks']], ['t1', 't2'])
        self.assertTrue(all(cell[7] is False for cell in data['footprint_tasks'][1][2]))

    def test_rank_uses_solved_mean_and_reports_all_measured_mean(self):
        tasks = [f't{i:02}' for i in range(20)]
        steady = [record('steady', t, net=5, churn=5) for t in tasks]
        # One failed mass deletion pulls the all-measured mean down; the solved-only rank ignores it.
        deleter = [record('deleter', t, net=20, churn=20) for t in tasks[1:]]
        deleter.append(record('deleter', tasks[0], net=-5000, churn=5000, resolved=False))
        data = build(freeze(steady, 'means'), steady + deleter, draws=20)
        self.assertEqual(data['ranking_metric'], 'same-task-net-ratio-v1')
        self.assertEqual([m['agent'] for m in data['models']], ['steady', 'deleter'])
        steady_row, deleter_row = data['models']
        self.assertEqual(deleter_row['measured_net_mean'], (19 * 20 - 5000) / 20)
        self.assertEqual((deleter_row['measured_solved_net_mean'], deleter_row['measured_solved_attempts']), (20, 19))
        self.assertEqual((steady_row['measured_solved_net_mean'], steady_row['measured_solved_attempts']), (5, 20))
        self.assertNotIn('measured_net_trimmed_mean', deleter_row)

    def test_same_task_ratio_corrects_for_task_difficulty(self):
        small, big = [f's{i}' for i in range(5)], [f'b{i}' for i in range(5)]

        def solves(agent, tasks, net):
            rows = [record(agent, t, net=net(t), churn=abs(net(t))) for t in tasks]
            for r in rows:
                r['metrics']['complexity_delta'] = net(r['task_id']) // 10
            return rows
        size = lambda t: 10 if t.startswith('s') else 100
        records = [r for name in ('p', 'q', 'r', 's') for r in solves(name, small + big, size)]
        records += solves('easy', small, size)  # same code as everyone, but only on small tasks
        records += solves('lean', big, lambda t: size(t) * 4 // 5)  # 20% less code on the big tasks
        data = build(freeze(records, 'difficulty'), records, draws=20)
        models = {m['agent']: m for m in data['models']}
        self.assertEqual(models['easy']['measured_solved_net_mean'], 10)
        self.assertEqual(models['lean']['measured_solved_net_mean'], 80)
        self.assertEqual(models['easy']['same_task_net'], 1)
        self.assertAlmostEqual(models['lean']['same_task_net'], 0.8)
        self.assertAlmostEqual(models['lean']['same_task_complexity'], 0.8)
        self.assertEqual(models['lean']['same_task_net_tasks'], 5)
        self.assertEqual(models['lean']['same_task_net_ci'], [0.8, 0.8])
        # Ranked on the same-task ratio, not the plain mean that rewards solving only small tasks.
        self.assertEqual(data['models'][0]['agent'], 'lean')
        # Typical solved patch per task: every model that solved it (leave-one-out happens per model).
        self.assertEqual(data['task_typical']['s0'], [10, 1, 5])
        self.assertEqual(data['task_typical']['b0'], [96, 9.6, 5])
        cell = next(row for row in data['footprint_tasks'] if row[0] == 'b0')[2][0]
        self.assertEqual(cell[8], cell[1] // 10 if cell[7] else None)

    def test_same_task_ratio_needs_three_other_models_and_five_tasks_for_a_range(self):
        records = [record(name, t, net=10, churn=10) for name in ('a', 'b', 'c') for t in ('t1', 't2')]
        data = build(freeze(records, 'too-few'), records, draws=20)
        self.assertTrue(all(m['same_task_net'] is None and m['same_task_net_tasks'] == 0 for m in data['models']))
        records += [record('d', t, net=5, churn=5) for t in ('t1', 't2')]
        data = build(freeze(records, 'enough'), records, draws=20)
        d = next(m for m in data['models'] if m['agent'] == 'd')
        self.assertEqual((d['same_task_net'], d['same_task_net_tasks'], d['same_task_net_ci']), (0.5, 2, None))

    def test_newest_generation_per_model_line(self):
        names = ['Claude Opus 5 (max)', 'Claude Opus 4.8 (max)', 'Claude Sonnet 4.6 (high)', 'GPT-5.6 Sol (max)',
                 'GPT-5.6 Luna (max)', 'GPT-5.5 (xhigh)', 'GPT-5 mini', 'Kimi K3 (max)', 'Kimi K2.7 Code',
                 'gpt-oss-120b', 'o3', 'o4-mini', 'Claude Opus 4', 'other-agent']
        self.assertEqual(newest_generation(names), {
            'Claude Opus 5 (max)', 'Claude Sonnet 4.6 (high)', 'GPT-5.6 Sol (max)', 'GPT-5.6 Luna (max)',
            'Kimi K3 (max)', 'gpt-oss-120b', 'o4-mini', 'other-agent'})
        records = [record('20260217_mini-v2.0.0_claude-4-6-opus', 't1', net=5, churn=9),
                   record('20251124_mini-v1.16.0_claude-opus-4-5-20251101', 't1', net=7, churn=9)]
        data = build(freeze(records, 'generations'), records, draws=20)
        self.assertEqual({m['name']: m['latest'] for m in data['models']},
                         {label(records[0]['agent']): True, label(records[1]['agent']): False})

    @unittest.skipUnless(shutil.which('node'), 'JavaScript interaction test requires Node.js')
    def test_column_sorting(self):
        records = [record()]
        page = render(build(freeze(records, 'sorting-test'), records, draws=10))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'index.html'
            path.write_text(page)
            result = subprocess.run(['node', str(Path(__file__).with_name('site_sorting.cjs')), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_company_is_model_developer(self):
        for agent, expected in {
            'deepswe-v1.1_mini_swe_agent_claude_opus_5_max': 'Anthropic',
            'deepswe-v1.1_mini_swe_agent_gpt_5_6_sol_max': 'OpenAI',
            'deepswe-v1.1_mini_swe_agent_gemini_3_7_flash_medium': 'Google',
            'deepswe-v1.1_mini_swe_agent_muse_spark_1_2_xhigh': 'Meta',
            'deepswe-v1.1_mini_swe_agent_glm_5_3_max': 'Z.ai',
            'deepswe-v1.1_mini_swe_agent_qwen3_8_max_xhigh': 'Alibaba',
            'deepswe-v1.1_mini_swe_agent_kimi_k3_max': 'Moonshot AI',
            'deepswe-v1.1_mini_swe_agent_grok_4_6_medium': 'xAI',
            'deepswe-v1.1_mini_swe_agent_deepseek_v4_pro_max': 'DeepSeek',
            '20250720_mini-v0.0.0-Llama-4-Maverick-17B-Instruct': 'Meta',
            '20260217_mini-v2.0.0_minimax-2-5-high': 'MiniMax',
            'devstral-2512': 'Mistral AI', 'o3-2025-04-16': 'OpenAI',
            'other-model': 'Other',
        }.items():
            self.assertEqual(company(agent), expected, agent)

    def test_model_plot_no_measurements_is_missing_not_zero(self):
        panel = freeze([record('ref')], 'empty-plot')
        missing = record('candidate')
        missing.update(metrics=None, analysis_status='fetch_error')
        model, = build(panel, [missing], draws=10)['models']
        self.assertIsNone(model['measured_net_mean'])
        self.assertIsNone(model['measured_churn_mean'])
        self.assertEqual(model['measured_attempts'], 0)

    def test_label_falls_back_to_identifier(self):
        self.assertEqual(label('20260217_mini-v2.0.0_new-model'), 'new-model')
        self.assertEqual(label('20260901_mini-v2.4.2_gemini-3-5-flash'), 'Gemini 3.5 Flash')
        self.assertEqual(label('20250720_mini-v0.0.0-Llama-4-Maverick-17B-Instruct'), 'Llama 4 Maverick')


def sensitivity(ranges):
    return dict(bootstrap=dict(models={a: dict(rank_ci_95=r) for a, r in ranges.items()}))


class RankRangeTests(unittest.TestCase):
    def test_rank_ranges_from_bootstrap(self):
        models = [dict(agent='a'), dict(agent='b')]
        add_rank_ranges(models, sensitivity(dict(a=[1, 1], b=[2, 3])))
        self.assertEqual([m['rank_range'] for m in models], [[1, 1], [2, 3]])

    def test_model_missing_from_sensitivity_gets_no_range(self):
        models = [dict(agent='a'), dict(agent='new')]
        add_rank_ranges(models, sensitivity(dict(a=[1, 2])))
        self.assertEqual([m['rank_range'] for m in models], [[1, 2], None])


class MainTests(unittest.TestCase):
    def run_main(self, *extra):
        records = [record('agent-a', 't1', net=5, churn=9), record('agent-b', 't1', net=10, churn=30)]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / 'panel.json').write_text(json.dumps(freeze(records, 'main-test')))
            (tmp / 'r.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
            argv = ['site', str(tmp / 'panel.json'), str(tmp / 'r.jsonl'), '--output', str(tmp / 'index.html'),
                    '--data', str(tmp / 'data.json'), *[a.replace('TMP', str(tmp)) for a in extra]]
            if '--sensitivity' in extra:
                (tmp / 'sensitivity.json').write_text(json.dumps(sensitivity({'agent-a': [1, 1], 'agent-b': [1, 2]})))
            with mock.patch.object(sys, 'argv', argv), redirect_stdout(StringIO()):
                main()
            self.assertTrue((tmp / 'index.html').read_text().startswith('<!doctype html>'))
            self.data = json.loads((tmp / 'data.json').read_text())
            return self.data['models']

    def test_benchmark_and_nav(self):
        models = self.run_main('--benchmark', 'deepswe', '--nav', 'Other board=other.html')
        self.assertEqual(len(models), 2)
        data = self.data
        self.assertEqual(data['benchmark']['name'], 'DeepSWE')
        self.assertEqual(data['nav'], [dict(label='Other board', url='other.html', current=False)])

    def test_nav_marks_the_board_being_built(self):
        self.run_main('--benchmark', 'deepswe', '--nav', 'This board=index.html', '--nav', 'Other board=other.html')
        self.assertEqual([item['current'] for item in self.data['nav']], [True, False])

    def test_live_discloses_mixed_harnesses_and_candidate_provenance(self):
        self.run_main('--benchmark', 'live')
        data = self.data
        self.assertEqual(data['benchmark']['name'], 'SWE-bench Live Lite')
        self.assertIn('not models alone', data['benchmark']['harness_note'])
        self.assertIn('not checked independently', data['benchmark']['notice'])
        self.assertEqual(company('live-lite-gpt-5.6-sol-slingshot-3.4.0'), 'OpenAI')
        self.assertEqual(company('live-lite-deepseek-v4.1-flash-tianxicode-0.1.423'), 'DeepSeek')
        self.assertEqual(company('live-lite-claude-opus-4.8-aiwork'), 'Anthropic')
        self.assertIn('Slingshot 3.4.0', label('live-lite-gpt-5.6-sol-slingshot-3.4.0'))

    def test_build_without_sensitivity(self):
        self.assertTrue(all('rank_range' not in m for m in self.run_main()))

    def test_build_with_sensitivity(self):
        models = self.run_main('--sensitivity', 'TMP/sensitivity.json')
        self.assertEqual({m['agent']: m['rank_range'] for m in models}, {'agent-a': [1, 1], 'agent-b': [1, 2]})


class MergedDeepSWETests(unittest.TestCase):
    def test_merged_ratio_weights_languages_by_shared_tasks(self):
        # Python 2 tasks at 0.5x, Go 1 task at 2x: (0.5 * 2 + 2 * 1) / 3 = 1. Raw totals would give 7/8.
        self.assertAlmostEqual(merged_ratio({'python': [(1, 2), (1, 2)], 'go': [(4, 2)]}), 1.0)
        self.assertAlmostEqual(merged_ratio({'python': [(-1, 2), (-1, 2)], 'go': [(4, 2)]}), (-0.5 * 2 + 2) / 3)
        self.assertAlmostEqual(merged_ratio({'python': [(1, 2)], 'go': [], 'js': [(1, -1)]}), 0.5)
        self.assertIsNone(merged_ratio({'python': []}))

    def test_model_missing_from_a_language_is_partial_and_listed_last(self):
        root = Path(__file__).resolve().parent.parent / 'examples' / 'deepswe-javascript'
        panel = json.loads((root / 'score-panel.json').read_text())
        records = [r for path in sorted(root.glob('*.jsonl')) for r in read_jsonl(path)]
        dropped = records[0]['agent']
        data = build_merged([('javascript', panel, records),
                             ('go', panel, [r for r in records if r['agent'] != dropped])], draws=20)
        partial = [m for m in data['models'] if m.get('partial')]
        self.assertEqual([m['agent'] for m in partial], [dropped])
        self.assertEqual(list(partial[0]['languages']), ['javascript'])
        self.assertIs(data['models'][-1], partial[0])
        self.assertIn('self_run_typical', data)

    def test_each_language_keeps_its_own_board_ratio(self):
        root = Path(__file__).resolve().parent.parent / 'examples'
        boards, expected = [], {}
        for language in ('javascript', 'typescript'):
            directory = root / f'deepswe-{language}'
            panel = json.loads((directory / 'score-panel.json').read_text())
            records = [r for path in sorted(directory.glob('*.jsonl')) for r in read_jsonl(path)]
            boards.append((language, panel, records))
            expected[language] = {m['agent']: m['same_task_net'] for m in build(panel, records, draws=20)['models']}
        data = build_merged(boards, draws=20)
        self.assertEqual([(l['key'], l['tasks'], l['attempts']) for l in data['merged']['languages']],
                         [('javascript', 5, 4), ('typescript', 35, 4)])
        self.assertEqual(len(data['models']), 26)
        for m in data['models']:
            for language, values in m['languages'].items():
                self.assertEqual(values['net'], expected[language][m['agent']], (m['name'], language))
            self.assertNotIn('measured_solved_net_mean', m)  # raw units are never pooled across languages
        values = [m['same_task_net'] for m in data['models']]
        self.assertEqual(values, sorted(values))
