"""Measure self-run diffs with a pinned analyzer checkout; outcomes stay not_graded.

Uses the analyzer from ANALYZER_CHECKOUT (a clean worktree of the commit that measured the published
board, so units are comparable) and the DeepSWE reference solutions as the human patch. One JSONL per
configuration, containing every finished attempt; unfinished planned attempts are simply absent and
counted against the planned population on the page, never as zero.

    python examples/self-run/measure.py ANALYZER_CHECKOUT DEEPSWE_CHECKOUT --cache DIR
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('analyzer', type=Path, help='clean worktree of the published board analyzer commit')
    parser.add_argument('checkout', type=Path, help='datacurve-ai/deep-swe checkout at the pinned commit')
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'results')
    args = parser.parse_args()
    sys.path.insert(0, str(args.analyzer.resolve()))
    from parsimony.artifacts import Cache
    from parsimony.benchmark import analyze_submission, analyzer_identity
    from parsimony.deepswe import dataset_rows, read_tasks

    plan = json.loads((HERE / 'plan.json').read_text())
    commit, source = analyzer_identity()
    if commit is None:
        parser.exit(1, 'error: analyzer checkout is dirty or not a git worktree\n')
    tasks = {t['task']: t for t in read_tasks(args.checkout, plan['language'])}
    cache = Cache(args.cache)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for config in plan['configurations']:
        runs = sorted((HERE / 'runs' / config['id']).glob('*/meta.json'))
        if not runs:
            continue
        planned = [t['task'] for t in plan['tasks'][:config['tasks']]]
        population = len(planned) * plan['attempts']
        metas = {(m := json.loads(p.read_text()))['item']: (m, p.parent / 'patch.diff') for p in runs}
        rows = [r for r in dataset_rows([tasks[t] for t in planned], plan['attempts']) if r['instance_id'] in metas]
        predictions = {item: path.read_text() for item, (meta, path) in metas.items()}
        # Ungraded attempts are measured through the failed-patch path, then relabelled not_graded.
        submission = dict(agent=f"self-run-v1_{config['id']}", predictions=predictions, resolved=set(),
                          evaluated=set(predictions), result_details=dict(unresolved=sorted(predictions)),
                          prediction_locations={item: f"examples/self-run/runs/{config['id']}/{item.replace('#', '__')}/patch.diff"
                                                for item in predictions},
                          provenance=dict(prediction_url='examples/self-run/runs', results_url=None, layout='self-run-v1',
                                          config=config['id'], harness=config['harness'], provider=config['provider'],
                                          model=config['model'], reasoning_effort=config['effort'],
                                          deepswe_commit=plan['deepswe_commit'], self_run=True, ref=commit))
        out = args.output_dir / f"{config['id']}.jsonl"
        with out.open('w') as handle:
            for record in analyze_submission(submission, cache, dataset=rows, include_failed=True):
                meta = metas[record['task_id']][0]
                record.update(resolved=False, published_result_categories=['not_graded'], evaluation_result='not_graded',
                              published_resolved_count=None, resolve_rate=None, benchmark_tasks=population, self_run=True)
                record['provenance'].update(harness_version=meta['harness_version'], run_status=meta['status'],
                                            run_seconds=meta['seconds'], network_commands=meta['network_commands'],
                                            run_patch_sha256=meta['patch_sha256'])
                handle.write(json.dumps(record, sort_keys=True) + '\n')
        print(f'{out}: {len(predictions)} of {population} planned attempts', file=sys.stderr)
    print(f'analyzer {commit} source {source}', file=sys.stderr)


if __name__ == '__main__':
    main()
