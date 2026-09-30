#!/usr/bin/env python3
"""Reproduce priority Live inventories/audits/static measurements in external storage.

Run with PYTHONPATH pointing at a clean committed Parsimony checkout. The cache
and inventory contain upstream patches and must NOT be committed or redistributed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from parsimony.artifacts import Cache
from parsimony.benchmark import analyzer_identity
from parsimony.live import import_run, analyze_run
from parsimony.preimages import audit_run

REVISION = 'cba8a6d3197cd53da09f8527cccbc689782302a6'
PYTHON_DATASET = 'SWE-bench-Live/SWE-bench-Live'
PYTHON_REVISION = 'b51a86422e10cfd403beb4773e5a2947953e36ec'
MULTILANG_REVISION = '62dc0745c40f067fc366ae3eb1a26136e5928f85'
COHORTS = [
    ('deepseek_v4_1_flash', 'lite/tianxicode/deepseek-flash', 'TianxiCode 0.1.423',
     'DeepSeek V4.1 Flash', 'python', 'live-lite-deepseek-v4.1-flash-tianxicode-0.1.423'),
    ('gpt_5_6_sol', 'lite/sapient-slingshot-agent/v3.4.0/gpt-5.6-sol', 'Slingshot 3.4.0',
     'GPT-5.6 Sol', 'python', 'live-lite-gpt-5.6-sol-slingshot-3.4.0'),
    ('claude_opus_4_8', 'lite/aiwork-code/20260909-opus-4-8-xhigh', 'AiWork.Code',
     'Claude Opus 4.8', 'python', 'live-lite-claude-opus-4.8-aiwork'),
    ('gpt_5_6_sol_js', 'multilang/js_ts/slingshot-agent/v3.4.0/gpt-5.6-sol/js', 'Slingshot 3.4.0',
     'GPT-5.6 Sol', 'javascript', 'live-multilang-gpt-5.6-sol-slingshot-3.4.0'),
    ('gpt_5_6_sol_ts', 'multilang/js_ts/slingshot-agent/v3.4.0/gpt-5.6-sol/ts', 'Slingshot 3.4.0',
     'GPT-5.6 Sol', 'typescript', 'live-multilang-gpt-5.6-sol-slingshot-3.4.0'),
]


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def review_manifest(run, audit, audit_path):
    for key in ('submission_revision', 'result_sha256', 'prediction_sha256'):
        if audit[key] != run[key]:
            raise ValueError(f'preimage audit {key} does not bind this inventory')
    if audit['dataset_checksum'] != run['dataset']['dataset_checksum']:
        raise ValueError('preimage audit dataset checksum does not bind this inventory')
    patches = {r['task_id']: r for r in run['records']}
    for r in audit['records']:
        patch = patches[r['task_id']].get('patch')
        checksum = hashlib.sha256(patch.encode()).hexdigest() if isinstance(patch, str) else None
        if r['patch_sha256'] != checksum:
            raise ValueError('preimage audit patch does not bind this inventory')
    return dict(status='approved', scope=audit['scope'],
                dataset_checksum=audit['dataset_checksum'], result_sha256=audit['result_sha256'],
                prediction_sha256=audit['prediction_sha256'], historical_dataset_match='unverified',
                submission_revision=audit['submission_revision'],
                base_commit_confirmations=audit['base_commit_confirmations'],
                blocked_preimages={r['task_id']: dict(status=r['status'], patch_sha256=r['patch_sha256'],
                                                     error=r.get('error', 'old blob identity unavailable'))
                                   for r in audit['records'] if r['status'] in
                                   ('unverified', 'hunks_match_without_blob_identity')},
                manifest_sha256=hashlib.sha256(audit_path.read_bytes()).hexdigest(),
                rights_status='numeric-metadata-only-not-raw-artifact-redistribution',
                protocol_status='source-reported-not-independently-certified')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--phase', choices=('inventory', 'audit', 'measure'), required=True)
    parser.add_argument('--cohort', choices=[c[0] for c in COHORTS], action='append')
    parser.add_argument('--workers', type=int, default=12)
    args = parser.parse_args()
    root = Path(args.output_dir).resolve()
    repo = Path(__file__).resolve().parents[2]
    if root.is_relative_to(repo):
        parser.error('use external storage: raw source/patch artifacts are not for redistribution')
    root.mkdir(parents=True, exist_ok=True)
    commit, _source_sha256 = analyzer_identity()
    if args.phase == 'measure':
        dirty = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'],
                               cwd=repo, capture_output=True, text=True, check=True).stdout.strip()
        if not commit or dirty:
            parser.error('measure only from a clean committed analyzer checkout')
    cache = Cache(root / 'cache', timeout=90)
    for name, config, source_agent, model, language, agent in COHORTS:
        if args.cohort and name not in args.cohort:
            continue
        inventory = root / (name + '.inventory.json')
        audit_path = root / (name + '.preimages.json')
        if args.phase == 'inventory':
            is_python = language == 'python'
            split = {'python': 'lite', 'javascript': 'js', 'typescript': 'ts'}[language]
            run = import_run(cache, submission_revision=REVISION, config_path='submissions/' + config,
                             dataset=PYTHON_DATASET if is_python else 'SWE-bench-Live/MultiLang',
                             dataset_revision=PYTHON_REVISION if is_python else MULTILANG_REVISION,
                             dataset_files=[(language, f'data/{split}-00000-of-00001.parquet')],
                             agent=source_agent, model=model)
            save(inventory, run)
            print(name, 'population', len(run['records']), flush=True)
        else:
            run = json.loads(inventory.read_text())
            if args.phase == 'audit':
                audit = audit_run(run, cache, workers=args.workers)
                save(audit_path, audit)
                print(name, audit['status_counts'], flush=True)
            else:
                audit = json.loads(audit_path.read_text())
                run['reviewed_manifest'] = review_manifest(run, audit, audit_path)
                records = analyze_run(run, cache, agent=agent, model=model, language=language)
                output = root / (name + '.records.jsonl')
                output.write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
                statuses = {s: sum(r['analysis_status'] == s for r in records)
                            for s in sorted({r['analysis_status'] for r in records})}
                print(name, 'analysis', statuses, flush=True)


if __name__ == '__main__':
    main()
