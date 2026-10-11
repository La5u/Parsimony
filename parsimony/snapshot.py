"""Portable, verified snapshots of the download cache behind result files.

``create`` packs only the cache entries that the given result JSONL files
reference (artifacts, patches, failure reports and base-commit sources), with a
manifest of URL -> content SHA256. ``restore`` checks every file against that
manifest before placing it in a cache, so reproduction needs no network access
and cannot silently use changed upstream bytes.
"""
import argparse
import hashlib
import io
import json
import os
import tarfile
import tempfile
from pathlib import Path
from urllib.parse import quote

from .analysis import parse_patch
from .artifacts import MAX_DOWNLOAD_BYTES, _parse_predictions
from .benchmark import read_jsonl

FORMAT = 'parsimony-cache-snapshot-v1'
MAX_MANIFEST_BYTES = 256 * 1024 * 1024
MAX_SNAPSHOT_BYTES = 64 * 1024 * 1024 * 1024
DATASET_URLS = [('https://datasets-server.huggingface.co/rows?dataset=princeton-nlp%2F'
                 f'SWE-bench_Verified&config=default&split=test&offset={offset}&length=100')
                for offset in range(0, 500, 100)]


def key(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


def cached_patch(record, cache_dir, predictions_cache=None):
    """The record's patch text from the cache, or None."""
    location = record.get('provenance', {}).get('patch_location')
    if not location or cache_dir is None:
        return None
    url, _, task = location.partition('#instance_id=')
    if task and predictions_cache is not None and url in predictions_cache:
        return predictions_cache[url].get(task)
    path = Path(cache_dir) / key(url)
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return None
    if not task:
        return data.decode('utf-8', 'replace')
    predictions = _parse_predictions(data)[1]
    if predictions_cache is not None:
        predictions_cache[url] = predictions
    return predictions.get(task)


def referenced_urls(records, cache_dir=None):
    """Every URL a record's analysis could have downloaded.

    Base-commit sources come from recorded touched files and, when the patch is
    cached, from re-parsing it: errored records carry no metrics, and renames
    are fetched by their old path.
    """
    urls = set(DATASET_URLS)
    # Monolithic prediction exports can be large and shared by hundreds of records.
    # Keep this memo local: a later call must see any changed cache contents.
    predictions_cache = {}
    for r in records:
        p = r.get('provenance', {})
        for field in ('results_url', 'prediction_url', 'metadata_url'):
            if p.get(field):
                urls.add(p[field])
        if p.get('patch_location'):
            urls.add(p['patch_location'].split('#instance_id=')[0])
        if p.get('failure_reports'):
            urls.add(p['failure_reports'].replace('<task>', r['task_id']))
        if not (p.get('repo') and p.get('base_commit')):
            continue
        paths = {path for metrics in (r.get('metrics'), r.get('human_metrics'))
                 for path in (metrics or {}).get('touched_files', [])}
        try:
            patch = cached_patch(r, cache_dir, predictions_cache)
            if patch:
                paths.update(f.old for f in parse_patch(patch) if f.old != '/dev/null')
        except ValueError:
            pass  # unparseable predictions/patches never reached a source download
        for path in paths:
            urls.add(f"https://raw.githubusercontent.com/{p['repo']}/{p['base_commit']}/{quote(path, safe='/')}")
    return urls


def create(result_paths, cache_dir, output):
    cache_dir = Path(cache_dir)
    result_paths = list(result_paths)
    records = [r for path in result_paths for r in read_jsonl(path)]
    entries, missing = [], 0
    for url in sorted(referenced_urls(records, cache_dir)):
        path = cache_dir / key(url)
        if not path.exists():
            missing += 1  # e.g. excluded files that were never fetched, or directory prefixes
            continue
        data = path.read_bytes()
        entries.append(dict(url=url, sha256=hashlib.sha256(data).hexdigest(), size=len(data)))
    manifest = dict(format=FORMAT, entries=entries,
                    results_sha256={str(p): hashlib.sha256(Path(p).read_bytes()).hexdigest()
                                    for p in result_paths})
    with tarfile.open(output, 'x:gz') as tar:
        payload = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
        info = tarfile.TarInfo('manifest.json')
        info.size = len(payload)
        tar.addfile(info, io.BytesIO(payload))
        for entry in entries:
            name = key(entry['url'])
            info = tarfile.TarInfo('cache/' + name)
            info.size = entry['size']
            with (cache_dir / name).open('rb') as stream:
                tar.addfile(info, stream)
    return dict(files=len(entries), bytes=sum(e['size'] for e in entries), unreferenced_or_missing=missing)


def restore(archive, cache_dir):
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, 'r:gz') as tar:
        # Sizes come from the (untrusted) archive itself: bound them before reading so a
        # compressed bomb cannot exhaust memory or disk. Hashes in the manifest only prove
        # self-consistency; restore snapshots only from sources you trust.
        info = tar.getmember('manifest.json')
        if not info.isfile() or info.size > MAX_MANIFEST_BYTES:
            raise ValueError('snapshot manifest missing or too large')
        manifest = json.load(tar.extractfile(info))
        if manifest.get('format') != FORMAT:
            raise ValueError('unsupported snapshot format')
        sizes = [entry.get('size') for entry in manifest['entries']]
        if not all(type(size) is int and 0 <= size <= MAX_DOWNLOAD_BYTES for size in sizes) \
                or sum(sizes) > MAX_SNAPSHOT_BYTES:
            raise ValueError('snapshot entry sizes invalid or over the restore limit')
        restored = skipped = 0
        for entry in manifest['entries']:
            name = key(entry['url'])
            member = tar.getmember('cache/' + name)
            if not member.isfile():
                raise ValueError(f"snapshot cache entry is not a regular file: {entry['url']}")
            if member.size != entry['size']:
                raise ValueError(f"snapshot size differs from manifest: {entry['url']}")
            data = tar.extractfile(member).read()
            if hashlib.sha256(data).hexdigest() != entry['sha256']:
                raise ValueError(f"snapshot content differs from manifest: {entry['url']}")
            target = cache_dir / name
            if target.exists():
                if hashlib.sha256(target.read_bytes()).hexdigest() != entry['sha256']:
                    raise ValueError(f"existing cache entry differs from snapshot: {entry['url']}")
                skipped += 1
                continue
            fd, tmp = tempfile.mkstemp(prefix=name + '.', dir=cache_dir)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(data)
                os.replace(tmp, target)
            finally:
                try:
                    os.unlink(tmp)
                except FileNotFoundError:
                    pass
            restored += 1
    return dict(restored=restored, already_present=skipped)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('create', help='pack cache entries referenced by result files')
    make.add_argument('results', nargs='+')
    make.add_argument('--cache', default='.parsimony-cache')
    make.add_argument('--output', required=True, help='new .tar.gz path (never overwritten)')
    load = commands.add_parser('restore', help='verify and unpack a snapshot into a cache')
    load.add_argument('archive')
    load.add_argument('--cache', default='.parsimony-cache')
    args = parser.parse_args()
    try:
        if args.command == 'create':
            summary = create(args.results, args.cache, args.output)
        else:
            summary = restore(args.archive, args.cache)
        print(json.dumps(summary))
    except (OSError, ValueError, KeyError, tarfile.TarError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
