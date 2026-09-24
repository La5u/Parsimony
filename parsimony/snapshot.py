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
import tarfile
from pathlib import Path
from urllib.parse import quote

from .benchmark import read_jsonl

FORMAT = 'parsimony-cache-snapshot-v1'
DATASET_URLS = [('https://datasets-server.huggingface.co/rows?dataset=princeton-nlp%2F'
                 f'SWE-bench_Verified&config=default&split=test&offset={offset}&length=100')
                for offset in range(0, 500, 100)]


def key(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


def referenced_urls(records):
    """Every URL a record's analysis could have downloaded."""
    urls = set(DATASET_URLS)
    for r in records:
        p = r.get('provenance', {})
        for field in ('results_url', 'prediction_url', 'metadata_url'):
            if p.get(field):
                urls.add(p[field])
        if p.get('patch_location'):
            urls.add(p['patch_location'].split('#instance_id=')[0])
        if p.get('failure_reports'):
            urls.add(p['failure_reports'].replace('<task>', r['task_id']))
        if p.get('repo') and p.get('base_commit'):
            for metrics in (r.get('metrics'), r.get('human_metrics')):
                for path in (metrics or {}).get('touched_files', []):
                    urls.add(f"https://raw.githubusercontent.com/{p['repo']}/{p['base_commit']}/"
                             f"{quote(path, safe='/')}")
    return urls


def create(result_paths, cache_dir, output):
    cache_dir = Path(cache_dir)
    records = [r for path in result_paths for r in read_jsonl(path)]
    entries, missing = [], 0
    for url in sorted(referenced_urls(records)):
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
        manifest = json.load(tar.extractfile('manifest.json'))
        if manifest.get('format') != FORMAT:
            raise ValueError('unsupported snapshot format')
        restored = skipped = 0
        for entry in manifest['entries']:
            name = key(entry['url'])
            data = tar.extractfile('cache/' + name).read()
            if hashlib.sha256(data).hexdigest() != entry['sha256']:
                raise ValueError(f"snapshot content differs from manifest: {entry['url']}")
            target = cache_dir / name
            if target.exists():
                if hashlib.sha256(target.read_bytes()).hexdigest() != entry['sha256']:
                    raise ValueError(f"existing cache entry differs from snapshot: {entry['url']}")
                skipped += 1
                continue
            tmp = target.with_suffix('.restoring')
            tmp.write_bytes(data)
            tmp.replace(target)
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
