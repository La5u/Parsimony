#!/usr/bin/env python3
"""Recheck DeepSeek Live patch/report/metadata agreement; never execute target code.

Inputs/raw cache remain external. Output is scalar/hash provenance only.
Rights and protocol decisions are editorial review, not inferred by this script.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path

from parsimony.artifacts import Cache
from parsimony.scoring import measured, out_of_scope


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def audit_row(row, cache, root):
    task = row['task_id']
    paths = [f'logs/rollouts/{task}/patch.diff', f'logs/rollouts/{task}/meta.json',
             f'logs/evaluationresults/{task}/report.json']
    raw = [cache.get(root + '/' + path) for path in paths]
    meta, report = json.loads(raw[1]), json.loads(raw[2])
    checks = dict(patch_agreement=raw[0] == row['patch'].encode(),
                  metadata_id=meta.get('instance_id') == task,
                  declared_repo_base=(meta.get('repo'), meta.get('base_commit')) == (row['repo'], row['base_commit']),
                  model_alias=meta.get('model') == 'tianxi-agent-plan/deepseek-flash',
                  agent_version=meta.get('binary_version') == '0.1.423',
                  report_id=report.get('instance_id') == task,
                  report_outcome=type(report.get('resolved')) is bool and
                  report['resolved'] == (row['published_outcome'] == 'success'))
    return dict(task_id=task, checks=checks,
                sources=[dict(url=root + '/' + path, bytes=len(content), sha256=sha(content))
                         for path, content in zip(paths, raw)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--external-dir', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    external = Path(args.external_dir)
    run = json.loads((external / 'deepseek_v4_1_flash.inventory.json').read_text())
    if (run['submission_revision'] != 'cba8a6d3197cd53da09f8527cccbc689782302a6'
            or run['config'] != 'submissions/lite/tianxicode/deepseek-flash'
            or len(run['records']) != 300):
        parser.error('expected the pinned full 300-task DeepSeek cohort')
    cache = Cache(external / 'cache', timeout=60)
    root = 'https://raw.githubusercontent.com/SWE-bench-Live/submission/' + run['submission_revision'] + '/' + run['config']
    with ThreadPoolExecutor(max_workers=12) as pool:
        evidence = list(pool.map(lambda row: audit_row(row, cache, root), run['records']))
    records_path = external / 'deepseek_v4_1_flash.records.jsonl'
    raw = records_path.read_bytes()
    records = [json.loads(line) for line in raw.splitlines()]
    archived = Path(__file__).resolve().parents[2] / 'examples/priority-live/measurement-summary.json'
    expected = json.loads(archived.read_text())['cohorts']['deepseek_v4_1_flash']['measurement_records_sha256']
    if sha(raw) != expected:
        raise ValueError('measurement bytes differ from the archived clean-checkout evidence')
    if (len(records) != 300 or len({r['task_id'] for r in records}) != 300
            or {r['task_id'] for r in records} != {r['task_id'] for r in run['records']}):
        raise ValueError('measurement and inventory task populations differ')
    excluded = [r for r in records if measured(r) and out_of_scope(r['metrics'])]
    eligible = [r for r in records if measured(r) and not out_of_scope(r['metrics'])]
    references = set()
    for name in ('deepseek_v4_1_flash', 'gpt_5_6_sol', 'claude_opus_4_8'):
        group = [json.loads(line) for line in (external / (name + '.records.jsonl')).read_bytes().splitlines()]
        references.update(r['task_id'] for r in group
                          if r['resolved'] and measured(r) and not out_of_scope(r['metrics']))
    summary = dict(schema_version=1, submission_revision=run['submission_revision'],
                   dataset_checksum=run['dataset']['dataset_checksum'],
                   result_sha256=run['result_sha256'], prediction_sha256=run['prediction_sha256'],
                   measurement_records_sha256=sha(raw), population=300,
                   agreement_checks={key: sum(e['checks'][key] for e in evidence) for key in evidence[0]['checks']},
                   all_checks_pass=all(all(e['checks'].values()) for e in evidence),
                   static_analysis_count=sum(measured(r) for r in records),
                   footprint_eligible_count=len(eligible),
                   footprint_eligible_outcomes=dict(Counter(r['evaluation_result'] for r in eligible)),
                   out_of_scope=[dict(task_id=r['task_id'], evaluation_result=r['evaluation_result']) for r in excluded],
                   missing_reference_task_ids=sorted({r['task_id'] for r in records} - references),
                   passing_reference_task_count=len(references), evidence=evidence,
                   full_population_score_status='blocked-missing-passing-references',
                   historical_dataset_match='unverified', operational_full_checkout_status='unverified')
    Path(args.output).write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print({k: v for k, v in summary.items() if k not in ('evidence', 'missing_reference_task_ids', 'out_of_scope')})
    if not summary['all_checks_pass']:
        raise SystemExit('Source agreement checks failed; do not approve publication')


if __name__ == '__main__':
    main()
