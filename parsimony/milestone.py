"""Import SWE-Milestone per-milestone trials: feature development, one milestone at a time.

Each attempt starts from the milestone's prepared start state (the HEAD of its pinned
image, extracted into a local bare repository) and is published as a filtered source
snapshot. The patch is rebuilt here as snapshot minus start state, for in-scope files of
the repository's language only. Raw snapshots stay external; records hold scalars and hashes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path

from .analysis import implementation, measure
from .benchmark import ANALYZER_VERSION, analyzer_identity, read_jsonl
from .languages import track

DATASET = 'DeepCommit-ai/SWE-Milestone-log'
REVISION = '03d82b7e48d4c5c8c3c76a8a8bb80901659d9f99'
DATASET_URL = f'https://huggingface.co/datasets/{DATASET}/tree/{REVISION}'
IMAGE_VERSION = 'v1.0.2'
# Repositories in a supported language: dataset directory -> (short id, language).
REPOS = {'navidrome_navidrome_v0.57.0_v0.58.0': ('navidrome', 'go'),
         'zeromicro_go-zero_v1.6.0_v1.9.3': ('go-zero', 'go'),
         'scikit-learn_scikit-learn_1.5.2_1.6.0': ('scikit-learn', 'python'),
         'element-hq_element-web_v1.11.95_v1.11.97': ('element-web', 'typescript')}
# A snapshot missing more than this share of the start state's in-scope files, and more than
# PARTIAL_MIN_FILES of them, is incomplete. Real deletions in this data touch at most a few files.
PARTIAL_SNAPSHOT = 0.25
PARTIAL_MIN_FILES = 20
SHA = re.compile(r'^[0-9a-f]{40}$')
SAFE = re.compile(r'^[A-Za-z0-9_.-]+$')


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


class Git:
    """Read-only access to one extracted bare repository."""

    def __init__(self, path):
        self.path = str(path)

    def run(self, *args, binary=False):
        out = subprocess.run(['git', f'--git-dir={self.path}', *args], check=True, capture_output=True).stdout
        return out if binary else out.decode()

    def resolve(self, ref):
        return self.run('rev-parse', '--verify', '--end-of-options', f'{ref}^{{commit}}').strip()

    def files(self, commit, dirs):
        """Map path -> blob id for files under the source dirs."""
        out = self.run('ls-tree', '-r', '-z', '--full-tree', commit, '--', *dirs)
        files = {}
        for entry in filter(None, out.split('\0')):
            meta, path = entry.split('\t', 1)
            mode, kind, blob = meta.split()
            if kind == 'blob' and mode != '120000':
                files[path] = blob
        return files

    def blob(self, blob):
        return self.run('cat-file', 'blob', blob, binary=True)


def read_snapshot(path):
    """Regular files of a source_snapshot.tar as path -> bytes."""
    files = {}
    with tarfile.open(path) as tar:
        for member in tar:
            if member.isfile():
                name = member.name.removeprefix('./')
                if name.startswith('/') or '..' in name.split('/'):
                    raise ValueError(f'unsafe snapshot path: {name}')
                files[name] = tar.extractfile(member).read()
    return files


def diff(before, after, language):
    """Unified git diff of in-scope files from two path -> bytes maps (None = absent)."""
    paths = sorted(p for p in set(before) | set(after)
                   if before.get(p) != after.get(p) and implementation(p, language))
    chunks = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for i, path in enumerate(paths):
            sides = []
            for side, files in (('a', before), ('b', after)):
                if files.get(path) is None:
                    sides.append('/dev/null')
                else:
                    target = root / side / str(i)
                    target.parent.mkdir(exist_ok=True)
                    target.write_bytes(files[path])
                    sides.append(f'{side}/{i}')
            out = subprocess.run(['git', 'diff', '--no-index', '--no-renames', '--no-color', '--no-ext-diff',
                                  *sides], cwd=root, capture_output=True)
            if out.returncode not in (0, 1):
                raise RuntimeError(out.stderr.decode(errors='replace'))
            text = out.stdout.decode('utf-8')
            # Keep git's hunks; write the header with the repository path.
            hunks = text[text.find('\n@@') + 1:] if '\n@@' in text else ''
            if not hunks:
                raise ValueError(f'{path}: no text hunks (binary or mode-only change)')
            old = '/dev/null' if sides[0] == '/dev/null' else f'a/{path}'
            new = '/dev/null' if sides[1] == '/dev/null' else f'b/{path}'
            mode = ('new file mode 100644\n' if old == '/dev/null' else
                    'deleted file mode 100644\n' if new == '/dev/null' else '')
            chunks.append(f'diff --git a/{path} b/{path}\n{mode}--- {old}\n+++ {new}\n{hunks}')
    return ''.join(chunks), paths


def milestones(data, repo_dir):
    with open(Path(data) / repo_dir / 'milestones.csv', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    selected = Path(data) / repo_dir / 'selected_milestone_ids.txt'
    ids = selected.read_text().split() if selected.exists() else [r['id'] for r in rows]
    return {r['id']: r for r in rows if r['id'] in ids}


def build_dataset(data, baselines, gits):
    """Population: graded milestones whose reference change touches an in-scope file."""
    data, gits = Path(data), Path(gits)
    baselines = json.loads(Path(baselines).read_text())
    rows = []
    for repo_dir, (short, language) in REPOS.items():
        meta = json.loads((data / repo_dir / 'metadata.json').read_text())
        git = Git(gits / repo_dir)
        for mid, row in sorted(milestones(data, repo_dir).items()):
            image = baselines[f'{repo_dir}/{mid}']
            head = git.resolve(f'refs/start/{mid}')
            if head != image['head'] or not SHA.fullmatch(head):
                raise ValueError(f'{repo_dir}/{mid}: start state differs from the extracted image HEAD')
            start, end = (git.resolve(f'refs/tags/milestone-{mid}-{side}') for side in ('start', 'end'))
            ref_before = git.files(start, meta['repo_src_dirs'])
            ref_after = git.files(end, meta['repo_src_dirs'])
            changed = [p for p in set(ref_before) | set(ref_after)
                       if ref_before.get(p) != ref_after.get(p) and implementation(p, language)]
            if not changed:
                continue
            commits = [c for c in row['commits'].split(';') if c]
            rows.append(dict(instance_id=f'{short}__{mid}', repo=meta['repo_name'], base_commit=head,
                             language=language, milestone=mid, title=row['title'], category=row['category'],
                             task_url=f"https://github.com/{meta['repo_name']}/commit/{commits[-1]}" if commits else None,
                             provenance=dict(dataset=DATASET, dataset_revision=REVISION, dataset_dir=repo_dir,
                                             image=image['image'], image_version=IMAGE_VERSION,
                                             start_tag_commit=start, end_tag_commit=end,
                                             src_dirs=meta['repo_src_dirs'], reference_commits=commits,
                                             reference_files=len(changed))))
    return rows


def configs(data, repo_dir):
    return sorted(p.name for p in (Path(data) / repo_dir / 'mstone_trial').iterdir() if p.is_dir())


def agent_id(config):
    # "_claude-code_opus-4.6_run_001" -> "milestone-claude-code-opus-4.6"
    m = re.fullmatch(r'_([a-z-]+)_(.+)_run_\d+', config)
    if not m:
        raise ValueError(f'unexpected configuration name: {config}')
    return f'milestone-{m[1]}-{m[2]}'


def outcome(cell):
    """Prefer evaluation_result_filtered.json, as the benchmark's own collector does."""
    filtered = cell / 'evaluation_result_filtered.json'
    path = filtered if filtered.exists() else cell / 'evaluation_result.json'
    raw = path.read_bytes()
    result = json.loads(raw)
    if type(result.get('resolved')) is not bool:
        raise ValueError(f'{path}: resolved must be a boolean')
    return result, path.name, sha256(raw)


def analyze(dataset_path, data, gits, agent, language):
    data, gits = Path(data), Path(gits)
    dataset = [r for r in read_jsonl(dataset_path) if r['language'] == language]
    if not dataset:
        raise ValueError(f'no {language} milestones in the population')
    commit, source_digest = analyzer_identity()
    measurement_track = track(language)
    cells, results = {}, {}
    for row in dataset:
        repo_dir = row['provenance']['dataset_dir']
        matches = [c for c in configs(data, repo_dir) if agent_id(c) == agent]
        if len(matches) != 1:
            raise ValueError(f'{agent}: expected one configuration in {repo_dir}, found {matches}')
        cells[row['instance_id']] = data / repo_dir / 'mstone_trial' / matches[0] / row['milestone']
        results[row['instance_id']] = outcome(cells[row['instance_id']] / 'evaluation')
    resolved_count = sum(r[0]['resolved'] for r in results.values())
    human_cache, records = {}, []
    for row in dataset:
        task, repo_dir, mid = row['instance_id'], row['provenance']['dataset_dir'], row['milestone']
        git = Git(gits / repo_dir)
        dirs = row['provenance']['src_dirs']
        result, result_name, result_digest = results[task]
        snapshot_path = cells[task] / 'evaluation' / 'source_snapshot.tar'
        record = dict(schema_version=2, analyzer_version=ANALYZER_VERSION, python_version=platform.python_version(),
                      analyzer_commit=commit, analyzer_source_sha256=source_digest,
                      measurement_track=measurement_track, agent=agent, task_id=task,
                      resolved=result['resolved'], evaluation_result='resolved' if result['resolved'] else 'failed',
                      published_result_categories=['resolved' if result['resolved'] else 'failed'],
                      published_resolved_count=resolved_count, benchmark_tasks=len(dataset),
                      resolve_rate=resolved_count / len(dataset),
                      provenance={**row['provenance'], 'instance_id': task, 'repo': row['repo'],
                                  'base_commit': row['base_commit'], 'task_url': row['task_url'],
                                  'cell': str(cells[task].relative_to(data)), 'result_file': result_name,
                                  'result_sha256': result_digest, 'patch_location': None, 'patch_sha256': None},
                      metrics=None, human_metrics=None, model_human_ratio=None, analysis_status='missing_patch')
        records.append(record)
        if not snapshot_path.exists():
            continue
        raw = snapshot_path.read_bytes()
        record['provenance'].update(snapshot_sha256=sha256(raw), patch_location=f"{record['provenance']['cell']}/evaluation/source_snapshot.tar")
        base_files = git.files(row['base_commit'], dirs)
        after = read_snapshot(snapshot_path)
        # The snapshot omits test/excluded files, so a start-state file it lacks is only a deletion
        # when another configuration's snapshot of this milestone kept it, or the reference deletes it.
        kept = set()
        for other in (data / repo_dir / 'mstone_trial').iterdir():
            path = other / mid / 'evaluation' / 'source_snapshot.tar'
            if path.exists() and other.name != cells[task].parent.name:
                with tarfile.open(path) as tar:
                    kept |= {m.name.removeprefix('./') for m in tar if m.isfile()}
        end_files = git.files(row['provenance']['end_tag_commit'], dirs)
        in_scope = {p for p in base_files if implementation(p, language)}
        before = {p: git.blob(base_files[p]) for p in in_scope | (set(after) & set(base_files))}
        missing = in_scope - set(after)
        record['provenance']['missing_start_files'] = len(missing)
        if len(missing) > max(PARTIAL_MIN_FILES, PARTIAL_SNAPSHOT * len(in_scope)):
            # The agent's commit lacked whole source directories (the harness logs them as
            # non-existent); the evaluator overlays snapshots, so this is not evidence of deletion.
            record['analysis_status'] = 'partial_snapshot'
            continue
        state = dict(after)
        for p in missing:
            state[p] = before[p] if (p not in kept and p in end_files) else None
        try:
            patch, paths = diff(before, state, language)
        except UnicodeDecodeError as exc:
            record.update(analysis_status='error', analysis_error=f'UnicodeDecodeError: {exc}')
            continue
        record['provenance'].update(patch_sha256=sha256(patch.encode()), patch_files=len(paths),
                                    deleted_files=sum(state.get(p) is None for p in paths))
        if not patch:
            record['analysis_status'] = 'empty_patch'
            continue

        def source(path, files=base_files):
            if path not in files:
                raise ValueError(f'{path} does not exist at the start state')
            return git.blob(files[path]).decode('utf-8-sig')

        try:
            record['metrics'] = measure(patch, source, language=language)
            record['analysis_status'] = 'ok'
        except Exception as exc:
            record.update(analysis_status='error', analysis_error=f'{type(exc).__name__}: {exc}')
            continue
        if task not in human_cache:
            start = row['provenance']['start_tag_commit']
            ref_before, ref_after = git.files(start, dirs), end_files
            human_cache[task] = None
            try:
                ref_patch, _ = diff({p: git.blob(b) for p, b in ref_before.items() if implementation(p, language)},
                                    {p: git.blob(b) for p, b in ref_after.items() if implementation(p, language)},
                                    language)
                human_cache[task] = measure(ref_patch, lambda p: source(p, ref_before), language=language)
            except Exception as exc:
                record['human_error'] = f'{type(exc).__name__}: {exc}'
        human = human_cache[task]
        if human is not None:
            record['human_metrics'] = human
            if human['churn'] and record['metrics']['churn'] is not None:
                record['model_human_ratio'] = record['metrics']['churn'] / human['churn']
    return records


def write_records(path, rows):
    Path(path).write_text(''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows))
    print(f'Wrote {len(rows)} records to {path}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    dataset = commands.add_parser('dataset', help='select graded milestones with in-scope reference changes')
    dataset.add_argument('data', help=f'{DATASET} download at {REVISION[:7]}')
    dataset.add_argument('--baselines', required=True, help='baselines.json from the image extraction')
    dataset.add_argument('--git', required=True, help='directory of extracted bare repositories')
    dataset.add_argument('--output', required=True)
    run = commands.add_parser('analyze', help='measure one configuration on one language')
    run.add_argument('data')
    run.add_argument('--dataset', required=True)
    run.add_argument('--git', required=True)
    run.add_argument('--agent', required=True, help='e.g. milestone-claude-code-opus-4.6')
    run.add_argument('--language', required=True, choices=sorted({lang for _, lang in REPOS.values()}))
    run.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'dataset':
            rows = build_dataset(args.data, args.baselines, args.git)
        else:
            rows = analyze(args.dataset, args.data, args.git, args.agent, args.language)
        write_records(args.output, rows)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
