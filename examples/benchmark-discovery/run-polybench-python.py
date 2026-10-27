#!/usr/bin/env python3
"""Reproduce the SWE-PolyBench Python board inputs in external storage.

  PYTHONPATH=. python examples/benchmark-discovery/run-polybench-python.py --output-dir DIR --phase inventory
  PYTHONPATH=. python examples/benchmark-discovery/run-polybench-python.py --output-dir DIR --phase audit
  PYTHONPATH=/clean/worktree python examples/benchmark-discovery/run-polybench-python.py --output-dir DIR --phase measure

inventory: pinned run inventories (upstream branch e7062f4 or a pull request head) and the
           113-task Python population (population.jsonl).
audit:     touched-file preimage audits; fetches every old file at the pinned base commit.
measure:   offline static analysis from the cache, from a clean committed analyzer checkout.

The cache and inventories contain upstream patches and must NOT be committed or redistributed;
DIR must lie outside the repository. Records and audits hold scalars and hashes only.
"""
import argparse
import json
import subprocess
from pathlib import Path

import parsimony
from parsimony.artifacts import Cache
from parsimony.benchmark import analyzer_identity
from parsimony.polybench import RUNS, analyze_run, audit_preimages, import_run

COHORTS = [
    '20260623_migbot_claude-opus-4-8',
    '20261021_aiwork-code_claude-opus-5-5',
    '20261010_jitto-build_claude-opus-5-5',
    '20261006_sapientslingshot_gpt-5.6-sol',
    '20260901_mobile-coder_deepseek-v4-flash',
]  # GPT-5.4 (20260422_iswe_agent) is withheld: before-state identity unproven.
LANGUAGE = 'python'


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--phase', choices=('inventory', 'audit', 'measure'), required=True)
    parser.add_argument('--cohort', choices=COHORTS, action='append')
    parser.add_argument('--workers', type=int, default=12)
    args = parser.parse_args()
    root = Path(args.output_dir).resolve()
    repo = Path(__file__).resolve().parents[2]
    if root.is_relative_to(repo):
        parser.error('use external storage: raw source/patch artifacts are not for redistribution')
    root.mkdir(parents=True, exist_ok=True)
    if args.phase == 'measure':
        analyzer = Path(parsimony.__file__).resolve().parents[1]
        commit, _ = analyzer_identity()
        dirty = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'],
                               cwd=analyzer, capture_output=True, text=True, check=True).stdout.strip()
        if not commit or dirty:
            parser.error('measure only from a clean committed analyzer checkout')
    cache = Cache(root / 'cache', timeout=90)
    population = None
    for name in COHORTS:
        if args.cohort and name not in args.cohort:
            continue
        inventory = root / f'{name}.inventory.json'
        audit_path = root / f'{name}.preimages.json'
        if args.phase == 'inventory':
            run = import_run(cache, run_name=name, language=LANGUAGE)
            save(inventory, run)
            rows = [dict(instance_id=r['task_id'], repo=r['repo'], base_commit=r['base_commit'], language=LANGUAGE)
                    for r in run['records'] if r['language'] == LANGUAGE]
            if population is not None and rows != population:
                raise SystemExit('runs disagree on the pinned Python population')
            population = rows
            print(name, 'population', len(run['population_ids']), 'submitted', run['submitted_task_count'], flush=True)
        elif args.phase == 'audit':
            run = json.loads(inventory.read_text())
            audit = audit_preimages(run, cache, workers=args.workers)
            save(audit_path, audit)
            print(name, audit['status_counts'], flush=True)
        else:
            run = json.loads(inventory.read_text())
            audit = json.loads(audit_path.read_text())
            records = analyze_run(run, cache, preimages=audit)
            output = root / (RUNS[name]['record_agent'] + '.jsonl')
            output.write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
            statuses = {s: sum(r['analysis_status'] == s for r in records)
                        for s in sorted({r['analysis_status'] for r in records})}
            print(name, 'analysis', statuses, flush=True)
    if population is not None:
        (root / 'population.jsonl').write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in population))


if __name__ == '__main__':
    main()
