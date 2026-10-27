#!/usr/bin/env python3
"""Reproduce SWE-bench Live MultiLang JavaScript/TypeScript/Go inventories, audits and measurements in external storage.

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

REVISION = '99bae66f923b3dfeab2d18366c0593929c5722de'
MULTILANG_REVISION = '62dc0745c40f067fc366ae3eb1a26136e5928f85'
BASE = 'multilang/js_ts/'
CONFIGS = [
    ('ami_claude_opus_4_6', 'ami-agent/20260710-v0.7.0-claude-opus-4-6', 'AMI Agent 0.7.0', 'Claude Opus 4.6'),
    ('slingshot_claude_sonnet_4_5', 'slingshot-agent/20260623-slingshot-claude4.5', 'Slingshot 2.6.0', 'Claude Sonnet 4.5'),
    ('slingshot_gpt_5_5_v2', 'slingshot-agent/20260629-sapient-slingshot-gpt-5.5', 'Slingshot 2.6.0', 'GPT-5.5'),
    ('slingshot_gpt_5_5_v3', 'slingshot-agent/20260730-sapient-slingshot-gpt-5.5', 'Slingshot 3.0.0', 'GPT-5.5'),
    ('slingshot_gpt_5_6_sol', 'slingshot-agent/v3.4.0/gpt-5.6-sol', 'Slingshot 3.4.0', 'GPT-5.6 Sol'),
]
COHORTS = [(f'{name}_{split}', f'{BASE}{path}/{split}', agent, model, language,
            f"live-multilang-{model.lower().replace(' ', '-')}-{agent.lower().replace(' ', '-')}")
           for split, language in (('js', 'javascript'), ('ts', 'typescript'))
           for name, path, agent, model in CONFIGS]
GO_CONFIGS = [
    ('ami_claude_opus_4_6', '20260716-v0.7.0-claude-opus-4-6', 'AMI Agent 0.7.0', 'Claude Opus 4.6'),
    ('ami_claude_sonnet_4_6', '20260723-v0.7.0-claude-sonnet-4-6', 'AMI Agent 0.7.0', 'Claude Sonnet 4.6'),
    ('ami_claude_haiku_4_5', '20260729-v0.7.0-claude-haiku-4-5', 'AMI Agent 0.7.0', 'Claude Haiku 4.5'),
    ('ami_gemini_3_1_pro_preview', '20260729-v0.7.0-gemini-3.1-pro-preview', 'AMI Agent 0.7.0', 'Gemini 3.1 Pro Preview'),
    ('ami_gemini_3_6_flash', '20260729-v0.7.0-gemini-3.6-flash', 'AMI Agent 0.7.0', 'Gemini 3.6 Flash'),
    ('ami_qwen3_8_27b', '20260923-v0.7.2-qwen3.8-27b', 'AMI Agent 0.7.2', 'Qwen3.8-27B'),
]
COHORTS += [(f'{name}_go', f'multilang/go/ami-agent/{path}', agent, model, 'go',
             f"live-multilang-{model.lower().replace(' ', '-')}-{agent.lower().replace(' ', '-')}")
            for name, path, agent, model in GO_CONFIGS]
# Added upstream after REVISION; pinned separately so the earlier cohorts stay byte-identical.
# Its patch.diff files are cross-checked against preds.json. On these 24 tasks the two differ in content
# and the logs don't show which one was evaluated, so they are left unmeasured (not_selected), never zero.
LATER_REVISIONS = {'tianxicode_deepseek_v4_1_flash_go': '641b727c8a5e3e5d0af08a348e632b12c3f11aef',
                   # Unmerged PR 64 (wei64), pinned at its head commit; served by the upstream repo's raw URLs.
                   'tianxicode_deepseek_v4_1_flash_js': '8275820e4fd36720d5281ce73e8fc5beb16fb404',
                   'tianxicode_deepseek_v4_1_flash_ts': '8275820e4fd36720d5281ce73e8fc5beb16fb404'}
PATCH_DISAGREEMENTS = {'tianxicode_deepseek_v4_1_flash_go': {
    'akuity__kargo-4687', 'caddyserver__caddy-7189', 'chenhg5__cc-connect-303',
    'cucumber__godog-695', 'envoyproxy__gateway-8521', 'github__gh-aw-22943',
    'github__gh-aw-23348', 'github__gh-aw-23870', 'github__gh-aw-24043',
    'github__gh-aw-24521', 'github__gh-aw-26074', 'gohugoio__hugo-14757',
    'jesseduffield__lazygit-4750', 'kubernetes-sigs__kueue-8597', 'kyverno__kyverno-15834',
    'libp2p__go-libp2p-3306', 'moby__moby-50281', 'nats-io__nats-server-7175',
    'nextlevelbuilder__goclaw-841', 'oauth2-proxy__oauth2-proxy-2524', 'open-telemetry__opentelemetry-collector-contrib-42164',
    'open-telemetry__opentelemetry-collector-contrib-46272', 'open-telemetry__opentelemetry-ebpf-profiler-734', 'tmc__langchaingo-1350',
}}
COHORTS += [('tianxicode_deepseek_v4_1_flash_go', 'multilang/go/tianxi/deepseek-flash', 'TianxiCode 0.1.486',
             'DeepSeek V4.1 Flash', 'go', 'live-multilang-deepseek-v4.1-flash-tianxicode-0.1.486')]
# One run covers both JS and TS (one preds.json/results.json); each board imports its own split and
# sets the other split's tasks aside (outside_dataset_count), as with the cross-language runs.
COMBINED_SPLITS = {'tianxicode_deepseek_v4_1_flash_js', 'tianxicode_deepseek_v4_1_flash_ts'}
COHORTS += [(f'tianxicode_deepseek_v4_1_flash_{split}', 'multilang/js_ts/tianxi/deepseek-flash', 'TianxiCode 0.1.486',
             'DeepSeek V4.1 Flash', language, 'live-multilang-deepseek-v4.1-flash-tianxicode-0.1.486')
            for split, language in (('js', 'javascript'), ('ts', 'typescript'))]
# Cross-language runs (all_languages): only their Go tasks are imported; other languages are set aside.
HARNESS = {'claudecode': 'Claude Code', 'openhands': 'OpenHands', 'sweagent': 'SWE-agent'}
ALL_LANGUAGE_RUNS = [
    ('claudecode', 'claude-4-5-sonnet', 'Claude Sonnet 4.5'), ('claudecode', 'deepseek-v3.1-terminus', 'DeepSeek V3.1 Terminus'),
    ('claudecode', 'deepseek-v4-pro', 'DeepSeek V4 Pro'), ('claudecode', 'gpt-5-2-medium', 'GPT-5.2 (medium)'),
    ('claudecode', 'gpt-5.5-medium', 'GPT-5.5 (medium)'), ('openhands', 'deepseek-v4-pro', 'DeepSeek V4 Pro'),
    ('openhands', 'gpt-5.5-medium', 'GPT-5.5 (medium)'), ('sweagent', 'claude-4-5-sonnet', 'Claude Sonnet 4.5'),
    ('sweagent', 'deepseek-v3.1-terminus', 'DeepSeek V3.1 Terminus'), ('sweagent', 'deepseek-v4-pro', 'DeepSeek V4 Pro'),
    ('sweagent', 'gemini-3-flash', 'Gemini 3 Flash'), ('sweagent', 'gpt-5.2-medium', 'GPT-5.2 (medium)'),
    ('sweagent', 'gpt-5.5-medium', 'GPT-5.5 (medium)'),
]
COHORTS += [(f"all_{harness}_{folder.replace('-', '_').replace('.', '_')}_go", f'multilang/all_languages/{harness}/{folder}',
             HARNESS[harness], model, 'go', f"live-multilang-{folder}-{harness}")
            for harness, folder, model in ALL_LANGUAGE_RUNS]


def selected_tasks(repo, name):
    if name not in PATCH_DISAGREEMENTS:
        return None
    tasks = json.loads((repo / 'examples/live-go/population-manifest.json').read_text())['tasks']
    return sorted(set(tasks) - PATCH_DISAGREEMENTS[name])


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
                review_url='https://github.com/La5u/Parsimony/blob/main/examples/live-multilang/' + audit_path.name,
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
            split = {'javascript': 'js', 'typescript': 'ts', 'go': 'go'}[language]
            run = import_run(cache, submission_revision=LATER_REVISIONS.get(name, REVISION),
                             config_path='submissions/' + config, verify_patch_files=name in LATER_REVISIONS,
                             dataset='SWE-bench-Live/MultiLang', dataset_revision=MULTILANG_REVISION,
                             dataset_files=[(language, f'data/{split}-00000-of-00001.parquet')],
                             agent=source_agent, model=model, task_ids=selected_tasks(repo, name),
                             set_aside_outside=config.startswith('multilang/all_languages/') or name in COMBINED_SPLITS)
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
