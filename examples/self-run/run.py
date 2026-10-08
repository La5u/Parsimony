"""Self-run pilot: run coding agents on preregistered DeepSWE Python tasks and keep their diffs.

Owner-approved exception to Parsimony's no-model-call rule. Results are SELF-RUN and unverified:
the agent harness differs from DeepSWE's (pi for OpenAI models, Claude Code for Anthropic models),
tasks run on the host Python without the task images or project dependencies, and outcomes are not
graded. They are shown faded and never ranked with published boards.

Each run gets a fresh repository containing only the base commit and its ancestors (no remote, no
later commits or tags), inside a bubblewrap sandbox that can write only the task directory and the
harness credential store, and that hides the DeepSWE checkout (reference solutions), this repository,
the download cache and agent transcripts. Network access remains (the harness needs its API); the
prompt forbids using it, and transcripts are scanned for network use afterwards.

    python examples/self-run/run.py DEEPSWE_CHECKOUT --scratch DIR [--only CONFIG] [--parallel N]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
HOME = Path.home()
RUN_TIMEOUT = 3600
LIMIT_PAUSE = 1800
SUFFIX = ('\n\n---\nThe repository is checked out in the current working directory at the base commit. '
          'Implement the change described above by editing the repository\'s source files. Work autonomously '
          'and do not ask questions. Do not commit. Do not use the network; project dependencies may not be '
          'installed.\n')
LIMIT = re.compile(r'usage limit|rate limit|rate_limit|429|quota|limit reached|extra usage|try again (later|at)', re.I)


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha256(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def git(*args, cwd=None, check=True):
    return subprocess.run(['git', *args], cwd=cwd, check=check, capture_output=True, text=True).stdout


def prepare_repo(mirrors, repo, base, work):
    """A repository holding exactly the base commit's history, checked out on main."""
    mirror = mirrors / repo.replace('/', '__')
    if not mirror.exists():
        git('clone', '-q', '--mirror', f'https://github.com/{repo}.git', str(mirror))
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    git('init', '-q', '-b', 'main', cwd=work)
    git('fetch', '-q', '--no-tags', str(mirror), f'{base}:refs/heads/main', cwd=work)
    git('checkout', '-q', 'main', cwd=work)
    git('config', 'core.hooksPath', '/dev/null', cwd=work)
    git('submodule', 'update', '--init', '--recursive', cwd=work, check=False)
    git('reflog', 'expire', '--expire=now', '--all', cwd=work)
    if git('rev-parse', 'HEAD', cwd=work).strip() != base:
        raise RuntimeError(f'{repo}: HEAD is not {base}')


def sandbox(work, scratch, binds, hides):
    cmd = ['bwrap', '--ro-bind', '/', '/', '--dev', '/dev', '--proc', '/proc', '--tmpfs', '/tmp',
           '--tmpfs', str(ROOT.parent), '--tmpfs', str(scratch)]
    for path in binds:
        cmd += ['--bind', str(path), str(path)]
    for path in hides:  # credential stores are bound first; their transcript folders stay hidden
        if path.exists():
            cmd += ['--tmpfs', str(path)]
    cmd += ['--bind', str(work), str(work), '--unshare-pid', '--die-with-parent', '--chdir', str(work),
            '--setenv', 'PIP_NO_INDEX', '1', '--setenv', 'GIT_TERMINAL_PROMPT', '0']
    return cmd


def harness_command(config, prompt):
    if config['harness'] == 'pi':
        return (['pi', '-p', '--mode', 'json', '--no-session', '--no-context-files', '--no-skills',
                 '--no-extensions', '--no-prompt-templates', '--no-mcp', '--no-themes',
                 '--model', f"{config['provider']}/{config['model']}", '--thinking', config['effort'], prompt],
                [HOME / '.pi'], [HOME / '.pi' / 'agent' / 'sessions'])
    return (['claude', '-p', '--safe-mode', '--no-session-persistence', '--strict-mcp-config', '--no-chrome',
             '--model', config['model'], '--effort', config['effort'], '--permission-mode', 'bypassPermissions',
             '--output-format', 'stream-json', '--verbose', prompt],
            [HOME / '.claude', HOME / '.claude.json'], [HOME / '.claude' / 'projects'])


def harness_version(config):
    tool = 'pi' if config['harness'] == 'pi' else 'claude'
    return subprocess.run([tool, '--version'], capture_output=True, text=True).stdout.strip()


def summarize(config, transcript):
    """Final status and token usage from a harness transcript."""
    error, usage, stop = None, {}, None
    for line in transcript.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if config['harness'] == 'pi':
            message = event.get('message') or {}
            if event.get('type') == 'message_end' and message.get('role') == 'assistant':
                stop = message.get('stopReason')
                error = message.get('errorMessage') or error
                for key, value in (message.get('usage') or {}).items():
                    if isinstance(value, (int, float)):
                        usage[key] = usage.get(key, 0) + value
        elif event.get('type') == 'result':
            stop = event.get('subtype')
            if event.get('is_error'):
                error = str(event.get('result') or event.get('subtype'))
            usage = event.get('usage') or {}
    return stop, error, usage


NETWORK = re.compile(r'\b(curl|wget|git (clone|fetch|pull)|pip (install|download)|requests\.get|urlopen)\b|https?://(?!localhost)', re.I)


def network_attempts(config, transcript):
    """Shell commands the agent ran that look like network use (heuristic, for disclosure only)."""
    hits = []
    for line in transcript.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = json.dumps(event)
        if '"bash"' not in text.lower() and '"Bash"' not in text:
            continue
        for match in re.finditer(r'"command":\s*"((?:[^"\\]|\\.)*)"', text):
            if NETWORK.search(match.group(1)):
                hits.append(match.group(1)[:300])
    return sorted(set(hits))


def run_one(config, task, attempt, args, instruction):
    item = f"{task['task']}#{attempt}"
    out = HERE / 'runs' / config['id'] / item.replace('#', '__')
    meta_path = out / 'meta.json'
    if meta_path.exists() and json.loads(meta_path.read_text())['status'] in ('completed', 'timeout', 'error'):
        return 'done'
    work = args.scratch / 'work' / config['id'] / item.replace('#', '__')
    prepare_repo(args.scratch / 'mirrors', task['repo'], task['base_commit'], work)
    prompt = instruction + SUFFIX
    command, binds, hides = harness_command(config, prompt)
    started, clock = now(), time.monotonic()
    try:
        proc = subprocess.run(sandbox(work, args.scratch, binds, hides) + command, capture_output=True,
                              text=True, timeout=RUN_TIMEOUT)
        transcript, stderr, code, timed_out = proc.stdout, proc.stderr, proc.returncode, False
    except subprocess.TimeoutExpired as exc:
        transcript = (exc.stdout or b'').decode(errors='replace') if isinstance(exc.stdout, bytes) else (exc.stdout or '')
        stderr = (exc.stderr or b'').decode(errors='replace') if isinstance(exc.stderr, bytes) else (exc.stderr or '')
        code, timed_out = None, True
    seconds = round(time.monotonic() - clock)
    stop, error, usage = summarize(config, transcript)
    limited = bool(error and LIMIT.search(error)) or (not transcript.strip() and LIMIT.search(stderr or ''))
    git('add', '-A', cwd=work)
    patch = subprocess.run(['git', 'diff', '--cached', '--binary', task['base_commit']], cwd=work,
                           capture_output=True).stdout.decode('utf-8', errors='replace')
    status = ('usage_limited' if limited else 'timeout' if timed_out else
              'error' if error or code not in (0, None) else 'completed')
    log_dir = args.scratch / 'transcripts' / config['id']
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"{item.replace('#', '__')}.jsonl").write_text(transcript)
    if status == 'usage_limited':
        shutil.rmtree(work, ignore_errors=True)
        return 'limited'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'patch.diff').write_text(patch)
    meta = dict(item=item, task=task['task'], attempt=attempt, config=config['id'], harness=config['harness'],
                harness_version=harness_version(config), provider=config['provider'], model=config['model'],
                effort=config['effort'], repo=task['repo'], base_commit=task['base_commit'],
                instruction_sha256=sha256(instruction), prompt_sha256=sha256(prompt), started_at=started,
                seconds=seconds, status=status, stop_reason=stop, exit_code=code,
                error=(error or (stderr[-500:] if status == 'error' else None)), usage=usage,
                patch_sha256=sha256(patch), patch_bytes=len(patch.encode()), empty_patch=not patch.strip(),
                transcript_sha256=sha256(transcript), network_commands=network_attempts(config, transcript),
                outcome='not_graded')
    meta_path.write_text(json.dumps(meta, indent=1) + '\n')
    shutil.rmtree(work, ignore_errors=True)
    return status


def queue(plan, tasks, only):
    """Task-major order, so every configuration finishes the shared core tasks first."""
    jobs = []
    for index, task in enumerate(tasks):
        for attempt in range(1, plan['attempts'] + 1):
            for config in plan['configurations']:
                if (not only or config['id'] in only) and index < config['tasks']:
                    jobs.append((config, task, attempt))
    return jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('checkout', type=Path, help='datacurve-ai/deep-swe checkout at the pinned commit')
    parser.add_argument('--scratch', type=Path, required=True, help='mirrors, work trees and transcripts')
    parser.add_argument('--only', action='append', help='configuration id (repeatable)')
    parser.add_argument('--parallel', type=int, default=4, help='concurrent runs per harness')
    args = parser.parse_args()
    args.scratch = args.scratch.resolve()
    plan = json.loads((HERE / 'plan.json').read_text())
    if git('rev-parse', 'HEAD', cwd=args.checkout).strip() != plan['deepswe_commit']:
        parser.exit(1, 'error: DeepSWE checkout is not at the pinned commit\n')
    tasks = plan['tasks']
    instructions = {t['task']: (args.checkout / 'tasks' / t['task'] / 'instruction.md').read_text() for t in tasks}
    for t in tasks:
        if sha256(instructions[t['task']]) != t['instruction_sha256']:
            parser.exit(1, f"error: {t['task']}: instruction changed\n")
    jobs = queue(plan, tasks, set(args.only or []))
    lock = threading.Lock()
    paused = {}

    def worker(harness):
        while True:
            with lock:
                pending = [j for j in jobs if j[0]['harness'] == harness]
                if not pending:
                    return
                job = pending[0]
                jobs.remove(job)
            config, task, attempt = job
            while True:
                while paused.get(harness, 0) > time.time():
                    time.sleep(30)
                try:
                    result = run_one(config, task, attempt, args, instructions[task['task']])
                except Exception as exc:  # setup failures are logged and retried later, never scored
                    print(f'{now()} {config["id"]} {task["task"]}#{attempt}: setup failed: {exc}', flush=True)
                    result = 'limited'
                print(f'{now()} {config["id"]} {task["task"]}#{attempt}: {result}', flush=True)
                if result != 'limited':
                    break
                with lock:
                    paused[harness] = max(paused.get(harness, 0), time.time() + LIMIT_PAUSE)

    threads = [threading.Thread(target=worker, args=(h,)) for h in ('pi', 'claude-code') for _ in range(args.parallel)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
