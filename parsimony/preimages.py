"""Audit submitted patch preimages against immutable source, without executing code.

This establishes touched-file compatibility, not a historical full checkout,
benchmark protocol compliance, grading correctness, or redistribution rights.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import re
from urllib.parse import quote
from pathlib import Path

from .analysis import apply_patch, parse_patch
from .artifacts import Cache

SHA = re.compile(r'^[0-9a-f]{40}$')
REPO = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')


def blob_hash(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def audit_record(record: dict, cache: Cache) -> dict:
    """Verify every old text file's Git blob prefix and exact hunk application."""
    result = dict(task_id=record['task_id'], repo=record.get('repo'),
                  base_commit=record.get('base_commit'), language=record.get('language'),
                  published_outcome=record.get('published_outcome'), sources=[])
    patch = record.get('patch')
    result['patch_sha256'] = hashlib.sha256(patch.encode()).hexdigest() if isinstance(patch, str) else None
    if (record.get('published_outcome') not in ('success', 'failure')
            or record.get('artifact_status') != 'present' or not patch):
        return dict(result, status='not_required', accepted=False)
    try:
        repo, base = record.get('repo'), record.get('base_commit')
        if (not isinstance(repo, str) or not REPO.fullmatch(repo)
                or any(p in {'.', '..'} for p in repo.split('/'))
                or not isinstance(base, str) or not SHA.fullmatch(base)):
            raise ValueError('unsafe repository or non-immutable base commit')
        files = parse_patch(patch, language=record['language'])
        # Associate index prefixes only with their own unambiguous diff block.
        indexes = {}
        for block in re.split(r'(?m)^diff --git ', patch)[1:]:
            old = re.search(r'(?m)^--- a/(.+)$', block)
            index = re.search(r'(?m)^index ([0-9a-f]+)\.\.([0-9a-f]+)(?: \d+)?$', block)
            if old and index:
                path = old[1].rstrip('\r')
                if path in indexes:
                    raise ValueError('duplicate diff block for old path')
                indexes[path] = index[1]
        old_paths = set()
        all_blobs_match = True
        for file in files:
            if file.old == '/dev/null':
                apply_patch('', file)
                continue
            if file.old in old_paths:
                raise ValueError('duplicate old file path')
            old_paths.add(file.old)
            url = f'https://raw.githubusercontent.com/{repo}/{base}/{quote(file.old, safe="/")}'
            raw = cache.get(url)
            actual = blob_hash(raw)
            prefix = indexes.get(file.old)
            available = prefix is not None and len(prefix) >= 7 and set(prefix) != {'0'}
            matches = available and actual.startswith(prefix)
            source = dict(path=file.old, url=url, bytes=len(raw),
                          sha256=hashlib.sha256(raw).hexdigest(), git_blob_sha1=actual,
                          old_index_prefix=prefix, index_match=bool(matches))
            result['sources'].append(source)
            if available and not matches:
                raise ValueError(f'old Git blob differs at pinned base: {file.old}')
            all_blobs_match = all_blobs_match and matches
            apply_patch(raw.decode('utf-8-sig'), file)
            source['strict_hunks_match'] = True
        if not files:
            raise ValueError('nonempty patch contains no text changes')
        status = ('new_files_only' if not old_paths else
                  'old_blobs_and_hunks_match' if all_blobs_match else 'hunks_match_without_blob_identity')
        return dict(result, status=status,
                    accepted=status in ('new_files_only', 'old_blobs_and_hunks_match'))
    except Exception as exc:
        return dict(result, status='unverified', accepted=False,
                    error=f'{type(exc).__name__}: {exc}')


def audit_run(run: dict, cache: Cache, *, workers: int = 8) -> dict:
    """Retain every inventory record; concurrency changes neither scope nor outcomes."""
    if workers < 1:
        raise ValueError('workers must be positive')
    with ThreadPoolExecutor(max_workers=workers) as pool:
        records = list(pool.map(lambda r: audit_record(r, cache), run['records']))
    counts = {s: sum(r['status'] == s for r in records) for s in sorted({r['status'] for r in records})}
    return dict(schema_version=1, scope='touched-file-preimage-not-full-checkout-certification',
                submission_revision=run.get('submission_revision'),
                dataset_checksum=run.get('dataset', {}).get('dataset_checksum'),
                result_sha256=run.get('result_sha256'), prediction_sha256=run.get('prediction_sha256'),
                historical_dataset_match='unverified', rights_status='unverified-do-not-redistribute',
                records=records, status_counts=counts,
                base_commit_confirmations={r['task_id']: r['base_commit'] for r in records if r['accepted']})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory')
    parser.add_argument('--cache', default='.parsimony-cache')
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    audit = audit_run(json.loads(Path(args.inventory).read_text()),
                      Cache(args.cache, timeout=90), workers=args.workers)
    Path(args.output).write_text(json.dumps(audit, indent=2, sort_keys=True) + '\n')
    print(f"Preimage statuses: {audit['status_counts']}; not full checkout/protocol/rights certification")


if __name__ == '__main__':
    main()
