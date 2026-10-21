#!/usr/bin/env python3
"""Measure DeepSWE release 1.0 configurations for models absent from the v1.1 boards.

Release 1.0 comes from the gated Hugging Face archive ``datacurve/deep-swe-leaderboard``
(accept its terms on huggingface.co first). Its 113 tasks have the same IDs and base commits
as v1.1, but v1.1 rewrote every verifier. On the nine setups present in both releases,
pass rates agree except on REGRADED tasks (|z| > 3 for a pass-rate shift across releases),
so a 1.0 outcome on those tasks is recorded as unknown, never as a pass or a failure.

Run with the analyzer of the board being extended on PYTHONPATH (a clean worktree of the
board's analyzer commit), Python 3.14.7, and a datacurve-ai/deep-swe checkout at 0b9fabb:

    PYTHONPATH=WORKTREE python examples/benchmark-discovery/add-deepswe-1.0.py ARCHIVE \\
        --deepswe DEEPSWE --language python --config mini_swe_agent_claude_opus_4_6_max --output OUT.jsonl

ARCHIVE holds ``submissions/deep-swe/1.0/<model dir>/<config>/<trial>/{result.json,artifacts/model.patch}``
downloaded at REVISION. Patches are read locally; records cite their pinned Hugging Face URLs.
"""
import argparse
import hashlib
import json
from pathlib import Path

from parsimony import deepswe
from parsimony.artifacts import Cache
from parsimony.benchmark import analyze_submission, analyzer_identity

DATASET = 'datacurve/deep-swe-leaderboard'
REVISION = '0618ccdd613e1f0043604f8f4474321e7fe12e29'
BASE = f'https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}'
REGRADED = ('narwhals-rolling-window-suite', 'vulture-persistent-analysis-cache', 'skrub-duration-encoding',
            'claude-code-by-agents-recursive-delegation')
CONFIGS = ('mini_swe_agent_claude_haiku_4_5_default', 'mini_swe_agent_claude_opus_4_6_max',
           'mini_swe_agent_claude_opus_4_7_max', 'mini_swe_agent_gemini_3_flash_preview_default',
           'mini_swe_agent_glm_5_1_default', 'mini_swe_agent_gpt_5_4_mini_xhigh',
           'mini_swe_agent_grok_build_0_1_default', 'mini_swe_agent_kimi_k2_6_default',
           'mini_swe_agent_mimo_v2_5_pro_default', 'mini_swe_agent_minimax_m2_7_default',
           'mini_swe_agent_minimax_m3_default', 'mini_swe_agent_qwen3_6_plus_default')


def trial_rows(archive, config):
    """v1.1-style trial rows for one configuration, from its result.json files."""
    results = sorted(Path(archive).glob(f'submissions/deep-swe/1.0/*/{config}/*/result.json'))
    if not results:
        raise ValueError(f'{config}: no result.json files')
    rows, digest = [], hashlib.sha256()
    for path in results:
        raw = path.read_bytes()
        digest.update(raw)
        result = json.loads(raw)
        agent = result['config']['agent']
        if result['config']['config'] != config or result['trial_name'] != path.parent.name:
            raise ValueError(f'{path}: configuration or trial name mismatch')
        patch = path.parent / 'artifacts' / 'model.patch'
        outcome = result['outcome'] if result.get('included_in_score', True) else 'error'
        if result['task_name'] in REGRADED and outcome in ('pass', 'fail'):
            outcome = 'regraded'  # unknown: v1.1 grades this task differently
        rows.append(dict(config=config, task_name=result['task_name'], trial_name=result['trial_name'],
                         outcome=outcome, has_model_patch=patch.exists(), started_at=result.get('started_at'),
                         model=agent['model_name'], reasoning_effort=agent.get('reasoning_effort'),
                         harness='mini-swe-agent', path=str(path.parent.relative_to(archive))))
    return rows, digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--deepswe', type=Path, required=True, help='datacurve-ai/deep-swe checkout at 0b9fabb')
    parser.add_argument('--language', required=True)
    parser.add_argument('--config', required=True, choices=CONFIGS)
    parser.add_argument('--cache', default=Path.home() / '.parsimony-cache')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if analyzer_identity()[0] is None:
        parser.exit(1, 'error: analyzer checkout is dirty or not a git worktree\n')
    rows, results_sha = trial_rows(args.archive, args.config)
    # The importer's patch URL is base + pattern; with pattern '{trial_name}' and the archive path
    # as trial name, every location is the pinned Hugging Face URL of that trial's model.patch.
    for r in rows:
        r['trial_name'] = f"{r.pop('path')}/artifacts/model.patch"
    local = {f'{BASE}/{r["trial_name"]}': args.archive / r['trial_name'] for r in rows}
    deepswe.fetch_patch = lambda cache, url, tries=4: local[url].read_text() if local[url].exists() else None
    release = dict(release_id='v1.0', artifact_base_url=BASE, artifact_patterns=dict(model_patch='{trial_name}'),
                   trials_sha256=results_sha, release_sha256=None)
    dataset = deepswe.dataset_rows(deepswe.read_tasks(args.deepswe, args.language))
    cache = Cache(args.cache, timeout=90)
    submission = deepswe.load_submission(args.config, rows, release, cache,
                                         {deepswe.cluster(r['instance_id']) for r in dataset})
    submission['provenance'].update(dataset=DATASET, dataset_revision=REVISION, regraded_tasks=list(REGRADED),
                                    results_sha256=results_sha)
    records = list(analyze_submission(submission, cache, dataset, include_failed=True))
    for _ in range(3):  # base files that failed to download: retry those items only
        retry = {r['task_id'] for r in records if r['analysis_status'] == 'fetch_error'}
        if not retry:
            break
        redone = {r['task_id']: r for r in analyze_submission(submission, cache, dataset, task_ids=retry,
                                                                include_failed=True) if r['task_id'] in retry}
        records = [redone.get(r['task_id'], r) for r in records]
    args.output.write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
    print(f'Wrote {len(records)} records to {args.output}')


if __name__ == '__main__':
    main()
