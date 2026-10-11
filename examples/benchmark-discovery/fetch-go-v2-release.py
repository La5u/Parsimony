#!/usr/bin/env python3
"""Download and verify the scalar-only Go v2 release; never overwrite local files.

Run from the repository root. Expected archive bytes/hash and every extracted
file hash come from the committed release-assets.json, not a mutable URL response.
No benchmark source/patches are downloaded or executed by this tool.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile
from urllib.request import Request, urlopen


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unpack(raw, manifest, output):
    require(len(raw) == manifest['archive_bytes'] and sha(raw) == manifest['archive_sha256'],
            'release archive checksum or size mismatch')
    expected = manifest['files']
    checked = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            require(member.isfile() and len(name.parts) == 1 and member.name in expected
                    and member.name not in checked, 'unexpected or unsafe archive member')
            binding = expected[member.name]
            require(member.size == binding['bytes'], 'archive member size mismatch')
            data = archive.extractfile(member).read()
            require(sha(data) == binding['sha256'], 'archive member checksum mismatch')
            checked[member.name] = data
    require(set(checked) == set(expected), 'release archive membership mismatch')
    output = Path(output)
    # Preflight every existing destination before writing anything.
    for name, data in checked.items():
        target = output / name
        require(not target.is_symlink(), 'refusing destination symlink')
        require(not target.exists() or target.read_bytes() == data, f'existing file differs: {target}')
    output.mkdir(parents=True, exist_ok=True)
    for name, data in checked.items():
        target = output / name
        if not target.exists():
            with target.open('xb') as stream:
                stream.write(data)
    return len(checked)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path,
                        default=Path('examples/deepswe-go-v2/release-assets.json'))
    parser.add_argument('--output', type=Path, required=True, help='external scalar-data directory')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_bytes())
        size = manifest['archive_bytes']
        require(type(size) is int and 0 < size <= 64 * 1024 * 1024, 'invalid release archive size')
        request = Request(manifest['archive_url'], headers={'User-Agent': 'parsimony-scalar-release/1'})
        with urlopen(request, timeout=60) as response:
            raw = response.read(size + 1)
        count = unpack(raw, manifest, args.output)
        print(f'Verified {count} scalar/metadata files in {args.output}')
    except (OSError, ValueError, KeyError, TypeError, tarfile.TarError) as exc:
        parser.exit(1, f'error: {exc}\n')


if __name__ == '__main__':
    main()
