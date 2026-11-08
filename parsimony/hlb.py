"""Import the Harness Leaderboard's DeepSWE trials (huggingface.co/spaces/joelniklaus/harness-leaderboard).

The Harness Leaderboard runs one model in several coding-agent harnesses (Claude Code, Codex, pi, ...),
three attempts per task, on the 111 DeepSWE v1.1 tasks at the commit the DeepSWE boards use, and
publishes each trial's final patch and verifier reward in a public Hugging Face bucket. Each setup
(model, reasoning effort, harness) is one board row; each attempt is an item ``<task>#<attempt>`` as on
the DeepSWE boards, and the attempts of a task share one reference pool (``deepswe.pooled_panel``).

``trials.json`` freezes the trials the leaderboard's public board scores (which attempt counts and its
pass/fail, after its own exclusions) and where each patch lives in the bucket; it is built by
``examples/benchmark-discovery/hlb-board-trials.py``.

    python -m parsimony.hlb dataset CHECKOUT --trials trials.json --language python --output deepswe-python.jsonl
    python -m parsimony.hlb analyze SETUP --trials trials.json --dataset deepswe-python.jsonl --output SETUP.jsonl
    python -m parsimony.deepswe panel *.jsonl --name NAME --output score-panel.json
"""
import argparse
import hashlib
import http.client
import json
from pathlib import Path

from .artifacts import Cache
from .benchmark import analyze_submission, read_jsonl
from .deepswe import dataset_rows, fetch_patch, read_tasks
from .languages import SUPPORTED

BUCKET = 'https://huggingface.co/buckets/joelniklaus/harness-leaderboard/resolve'
SPACE = 'https://huggingface.co/spaces/joelniklaus/harness-leaderboard'
ATTEMPTS = 3
PREFIX = 'hlb-deepswe_'
MODELS = {'zai-org/GLM-5.3-Flash': 'GLM-5.3 Flash', 'deepseek-ai/DeepSeek-V4.1-Flash': 'DeepSeek V4.1 Flash'}
HARNESSES = {'claude-code': 'Claude Code', 'codex': 'Codex', 'pi': 'pi', 'opencode': 'OpenCode', 'hermes': 'Hermes',
             'mini-swe-agent': 'mini-SWE-agent', 'kimi-code': 'Kimi Code', 'qwen-code': 'Qwen Code', 'openclaw': 'OpenClaw'}


def display_name(agent, setups=None):
    """'hlb-deepswe_glm-5.3-flash_high_claude-code' -> 'GLM-5.3 Flash (high) · Claude Code'."""
    model, effort, harness = agent.removeprefix(PREFIX).split('_')
    name = next((v for k, v in MODELS.items() if k.split('/')[1].lower() == model), model)
    return f'{name} ({effort}) · {HARNESSES.get(harness, harness)}'


def harness_name(agent):
    """'hlb-deepswe_glm-5.3-flash_high_claude-code' -> 'Claude Code' (the board's color group)."""
    harness = agent.removeprefix(PREFIX).split('_')[2]
    return HARNESSES.get(harness, harness)


def short_name(agent):
    """Chart label without the harness, which the color shows: 'GLM high', 'DeepSeek low'."""
    model, effort, _ = agent.removeprefix(PREFIX).split('_')
    return f"{next((v for k, v in MODELS.items() if k.split('/')[1].lower() == model), model).split('-')[0].split(' ')[0]} {effort}"


def setup_id(model, effort, harness):
    return f"{model.split('/')[1].lower()}_{effort}_{harness}"


def dataset(checkout, trials, language):
    """Items of one language for the tasks the leaderboard scores (three attempts each)."""
    scored = {t['task'] for s in trials['setups'].values() for t in s['trials']}
    tasks = [t for t in read_tasks(checkout, language) if t['task'] in scored]
    return dataset_rows(tasks, ATTEMPTS)


def load_submission(setup, trials, cache, items):
    """A submission in the shape ``benchmark.analyze_submission`` expects, for the items of one dataset."""
    spec = trials['setups'][setup]
    predictions, locations, resolved, unresolved, missing = {}, {}, set(), [], []
    evaluated = set()
    for t in spec['trials']:
        item = f"{t['task']}#{t['attempt']}"
        if item not in items:
            continue
        evaluated.add(item)
        (resolved.add(item) if t['outcome'] == 'pass' else unresolved.append(item))
        if not t.get('patch'):
            missing.append(item)
            continue
        locations[item] = f"{BUCKET}/{t['patch']}"
        patch = fetch_patch(cache, locations[item])
        if patch is None:
            missing.append(item)
        else:
            predictions[item] = patch
    return dict(agent=PREFIX + setup, submission_url=SPACE, predictions=predictions, prediction_locations=locations,
                resolved=resolved, evaluated=evaluated,
                result_details=dict(resolved=sorted(resolved), unresolved=sorted(unresolved), no_logs=[],
                                    missing_patch=sorted(missing)),
                provenance=dict(prediction_url=BUCKET, results_url=SPACE, layout='hlb-deepswe-trials-v1',
                                space_commit=trials['space_commit'], model=spec['model'],
                                reasoning_effort=spec['reasoning_effort'], harness=spec['harness'],
                                harness_version=spec['harness_version'], reported_model=spec['model'],
                                trials_sha256=trials.get('sha256'), prediction_sha256=None,
                                submission_url=SPACE, ref=trials['space_commit']))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--cache', default='.parsimony-cache')
    commands = parser.add_subparsers(dest='command', required=True)
    data = commands.add_parser('dataset', help='item metadata from a DeepSWE checkout, for the scored tasks')
    data.add_argument('checkout')
    data.add_argument('--trials', required=True)
    data.add_argument('--language', choices=SUPPORTED, default='python')
    data.add_argument('--output', required=True)
    run = commands.add_parser('analyze', help='measure one setup (model, effort, harness)')
    run.add_argument('setup')
    run.add_argument('--trials', required=True)
    run.add_argument('--dataset', required=True)
    run.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        raw = Path(args.trials).read_bytes()
        trials = dict(json.loads(raw), sha256=hashlib.sha256(raw).hexdigest())
        if args.command == 'dataset':
            rows = dataset(args.checkout, trials, args.language)
            Path(args.output).write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in rows))
            print(f'Wrote {len(rows)} items ({len(rows) // ATTEMPTS} tasks) to {args.output}')
        else:
            if args.setup not in trials['setups']:
                raise ValueError(f'unknown setup {args.setup!r}')
            cache = Cache(args.cache, timeout=90)
            rows = read_jsonl(args.dataset)
            submission = load_submission(args.setup, trials, cache, {r['instance_id'] for r in rows})
            records = list(analyze_submission(submission, cache, rows, include_failed=True))
            for _ in range(3):  # base files that failed to download: retry those items only
                retry = {r['task_id'] for r in records if r['analysis_status'] == 'fetch_error'}
                if not retry:
                    break
                redone = {r['task_id']: r for r in analyze_submission(submission, cache, rows, task_ids=retry,
                                                                        include_failed=True) if r['task_id'] in retry}
                records = [redone.get(r['task_id'], r) for r in records]
            Path(args.output).write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
            print(f'Wrote {len(records)} records to {args.output}')
    except (OSError, ValueError, KeyError, http.client.HTTPException) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
