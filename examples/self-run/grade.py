"""Grade self-run patches with each DeepSWE task's own verifier, in natively built arm64 images.

DeepSWE publishes amd64-only task images. They are rebuilt here from the task's
``environment/Dockerfile`` (its ``mars-base`` base image also ships arm64), then the task's
``tests/Dockerfile`` layers the hidden tests on top, exactly as DeepSWE does but ``FROM`` the local
image. Each patch is mounted as ``/logs/artifacts/model.patch`` and ``/tests/test.sh`` runs without
network, with the CPU and memory limits from ``task.toml``. Results are SELF-GRADED: the rebuilt
environment is not byte-identical to DeepSWE's, so ``--reference`` first checks that every task's
reference solution passes.

    python examples/self-run/grade.py DEEPSWE_CHECKOUT --scratch DIR --build
    python examples/self-run/grade.py DEEPSWE_CHECKOUT --scratch DIR --reference
    python examples/self-run/grade.py DEEPSWE_CHECKOUT --scratch DIR [--only CONFIG] [--task TASK]
    python examples/self-run/grade.py --apply

Finished items are skipped. Each graded item writes ``runs/<config>/<task>__<attempt>/grade.json``;
verifier logs stay in the scratch directory. ``--apply`` copies the grades into ``results/*.jsonl``
(rerun it after ``measure.py``, which writes ungraded records). A timeout is an unknown outcome,
like DeepSWE's errored runs: not solved, and not a failure either.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / 'plan.json').read_text())
ARCH = 'arm64'
# Version-drift pins for unpinned installs in a task's environment/Dockerfile: (old, new) text
# replacements. numba's Dockerfile installs the latest llvmlite but patches numba to accept 0.46.0.
PINS = {'numba-stencil-boundary-modes': [('pip install pytest "numpy<2.0" scipy llvmlite',
                                          'pip install pytest "numpy<2.0" scipy llvmlite==0.46.0')]}


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def podman(*args, check=True, **kw):
    return subprocess.run(['podman', *args], check=check, text=True, **kw)


def image_id(tag):
    r = podman('image', 'inspect', '--format', '{{.Id}}', tag, check=False, capture_output=True)
    return r.stdout.strip() if r.returncode == 0 else None


def tags(task):
    return f'localhost/parsimony-env/{task}:{ARCH}', f'localhost/parsimony-verifier/{task}:{ARCH}'


def build(task_dir, log_dir):
    """Build the environment image, then the verifier image on top of it; skip existing images."""
    env, verifier = tags(task_dir.name)
    log_dir.mkdir(parents=True, exist_ok=True)
    for tag, context, base in ((env, task_dir / 'environment', None), (verifier, task_dir / 'tests', env)):
        if image_id(tag):
            continue
        print(f'{now()} build {tag}', flush=True)
        dockerfile = (context / 'Dockerfile').read_text()
        if base is None:
            for old, new in PINS.get(task_dir.name, []):
                if old not in dockerfile:
                    sys.exit(f'{task_dir.name}: pin target not found: {old}')
                dockerfile = dockerfile.replace(old, new)
        with open(log_dir / f'{task_dir.name}-{tag.split("/")[1]}.log', 'w') as log:
            podman('build', '--arch', ARCH, '--network', 'host', '-t', tag, '-f', '-',
                   *(['--from', base] if base else []), str(context),
                   input=dockerfile, stdout=log, stderr=subprocess.STDOUT)


def run_verifier(task_dir, patch, out_dir, timeout=None):
    """Run the task's verifier on ``patch`` (None grades the pristine base); return reward.json."""
    settings = tomllib.loads((task_dir / 'task.toml').read_text())['verifier']
    limits = settings['environment']
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / 'artifacts').mkdir(parents=True)
    (out_dir / 'verifier').mkdir()
    if patch is not None:
        shutil.copyfile(patch, out_dir / 'artifacts' / 'model.patch')
    started = now()
    name = f'parsimony-grade-{out_dir.parent.name}-{out_dir.name}'.lower()
    podman('rm', '--force', name, check=False, capture_output=True)  # left over from an interrupted run
    try:
        r = podman('run', '--rm', '--name', name, '--network', 'none', '--cpus', str(limits['cpus']),
                   '--memory', f"{limits['memory_mb']}m", '-v', f'{out_dir}:/logs:Z',
                   tags(task_dir.name)[1], 'bash', '/tests/test.sh',
                   check=False, capture_output=True, timeout=timeout or settings['timeout_sec'])
        exit_code, timed_out = r.returncode, False
        (out_dir / 'verifier' / 'test-stdout.txt').write_text(r.stdout + r.stderr)
    except subprocess.TimeoutExpired:  # stopping the client leaves the container running
        podman('rm', '--force', name, check=False, capture_output=True)
        exit_code, timed_out = None, True
    reward_file = out_dir / 'verifier' / 'reward.json'
    reward = json.loads(reward_file.read_text()) if reward_file.exists() else None
    return {'started_at': started, 'finished_at': now(), 'exit_code': exit_code,
            'timeout_sec': timeout or settings['timeout_sec'], 'timed_out': timed_out, 'reward': reward}


def outcome(result):
    if result['timed_out']:
        return 'timeout'
    if result['reward'] is None:
        return 'grading_error'
    return 'pass' if result['reward']['reward'] == 1 else 'fail'


def apply_grades():
    """Set each measured record's outcome from its grade.json; measurements are unchanged."""
    results = {'pass': 'resolved', 'fail': 'unresolved', 'timeout': 'unknown'}
    for path in sorted((HERE / 'results').glob('*.jsonl')):
        records = [json.loads(line) for line in path.read_text().splitlines()]
        missing = [r['task_id'] for r in records
                   if not (HERE / 'runs' / path.stem / r['task_id'].replace('#', '__') / 'grade.json').exists()]
        if missing:  # a configuration is graded all at once, never partly
            print(f"{path}: {len(missing)} attempts not graded yet; left not_graded")
            continue
        for record in records:
            grade = json.loads((HERE / 'runs' / path.stem / record['task_id'].replace('#', '__') / 'grade.json').read_text())
            if grade['outcome'] not in results:
                sys.exit(f"{path.stem} {record['task_id']}: cannot apply outcome {grade['outcome']}")
            if grade['patch_sha256'] not in (None, record['provenance']['run_patch_sha256']):
                sys.exit(f"{path.stem} {record['task_id']}: graded patch differs from the measured one")
            record.update(resolved=grade['outcome'] == 'pass', evaluation_result=results[grade['outcome']],
                          published_result_categories=[results[grade['outcome']]])
            record['provenance'].update(grader=grade['grader'], grade_outcome=grade['outcome'],
                                        grade_timeout_sec=grade['timeout_sec'] if 'timeout_sec' in grade else None,
                                        grade_pins=grade.get('pins', []))
        path.write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in records))
        print(f"{path}: {sum(r['resolved'] for r in records)}/{len(records)} resolved")


def main():
    if sys.argv[1:] == ['--apply']:
        return apply_grades()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('deepswe', type=Path, help='DeepSWE checkout at the plan commit')
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--build', action='store_true', help='only build the task images')
    parser.add_argument('--reference', action='store_true', help='grade the reference solutions')
    parser.add_argument('--only', help='grade one configuration')
    parser.add_argument('--task', help='restrict to one task')
    parser.add_argument('--timeout', type=int, help="verifier timeout in seconds (default: task.toml's)")
    args = parser.parse_args()
    head = subprocess.run(['git', '-C', str(args.deepswe), 'rev-parse', 'HEAD'],
                          check=True, capture_output=True, text=True).stdout.strip()
    if head != PLAN['deepswe_commit']:
        sys.exit(f'DeepSWE checkout is at {head}, plan requires {PLAN["deepswe_commit"]}')
    tasks = [t['task'] for t in PLAN['tasks'] if not args.task or t['task'] == args.task]
    scratch = args.scratch.resolve() / 'grading'

    for task in tasks:
        build(args.deepswe / 'tasks' / task, scratch / 'build-logs')
    if args.build:
        return

    if args.reference:
        for task in tasks:
            task_dir = args.deepswe / 'tasks' / task
            out = scratch / 'reference' / task
            result = run_verifier(task_dir, task_dir / 'solution' / 'solution.patch', out)
            base = run_verifier(task_dir, None, scratch / 'reference-base' / task)
            print(f'{task}: reference {outcome(result)}, base {outcome(base)}', flush=True)
        return

    for config_dir in sorted((HERE / 'runs').iterdir()):
        if args.only and config_dir.name != args.only:
            continue
        for item_dir in sorted(config_dir.iterdir()):
            meta = json.loads((item_dir / 'meta.json').read_text())
            if meta['task'] not in tasks or (item_dir / 'grade.json').exists():
                continue
            task_dir = args.deepswe / 'tasks' / meta['task']
            patch = item_dir / 'patch.diff'
            empty = meta['empty_patch'] or not patch.exists() or patch.stat().st_size == 0
            result = run_verifier(task_dir, None if empty else patch,
                                  scratch / 'runs' / config_dir.name / item_dir.name, args.timeout)
            grade = {'item': meta['item'], 'config': meta['config'], 'outcome': outcome(result),
                     'grader': 'self-graded-arm64-v1', 'deepswe_commit': head, 'arch': ARCH,
                     'pins': PINS.get(meta['task'], []),
                     'patch_sha256': hashlib.sha256(patch.read_bytes()).hexdigest() if not empty else None,
                     'verifier_image': image_id(tags(meta['task'])[1]), **result}
            (item_dir / 'grade.json').write_text(json.dumps(grade, indent=1) + '\n')
            print(f'{now()} {config_dir.name} {item_dir.name}: {grade["outcome"]}', flush=True)


if __name__ == '__main__':
    main()
