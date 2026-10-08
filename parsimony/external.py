"""Pinned external capability indices (Artificial Analysis) for website axes; never used for ranking.

`snapshot` fetches the free Artificial Analysis LLM endpoint once, with the key read from the
AA_API_KEY environment variable (never stored), and writes only the index values of explicitly
mapped configurations together with the response hash. Unmapped or mismatched configurations stay
null, never borrowed from another reasoning effort. Attribution to https://artificialanalysis.ai/ is
required by the API terms and is carried in the snapshot.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ENDPOINT = 'https://artificialanalysis.ai/api/v2/data/llms/models'
ATTRIBUTION = 'https://artificialanalysis.ai/'
INDICES = {'aa_intelligence': 'artificial_analysis_intelligence_index',
           'aa_coding': 'artificial_analysis_coding_index'}
# exact: same model and reasoning effort; effort_unlabelled: AA lists a single entry without an
# effort label; undated_alias: the source names an undated provider ID that AA resolves to one
# dated snapshot. Anything weaker is recorded with aa_id null and a reason.
MATCHES = {'exact', 'effort_unlabelled', 'undated_alias'}


def fetch(key):
    request = urllib.request.Request(ENDPOINT, headers={'x-api-key': key, 'User-Agent': 'parsimony'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def snapshot(mapping, raw, fetched_at):
    models = {m['id']: m for m in json.loads(raw)['data']}
    configurations = {}
    for agent, entry in sorted(mapping['configurations'].items()):
        aa_id = entry.get('aa_id')
        if aa_id is None:
            configurations[agent] = dict(aa_id=None, match=None, reason=entry['reason'],
                                         **dict.fromkeys(INDICES))
            continue
        if entry['match'] not in MATCHES:
            raise ValueError(f'{agent}: unknown match type {entry["match"]!r}')
        if aa_id not in models:
            raise ValueError(f'{agent}: Artificial Analysis id {aa_id} is not in the response')
        model = models[aa_id]
        configurations[agent] = dict(aa_id=aa_id, aa_name=model['name'], aa_slug=model['slug'],
                                     aa_release_date=model.get('release_date'), match=entry['match'],
                                     **({'note': entry['note']} if entry.get('note') else {}),
                                     **{k: model['evaluations'].get(v) for k, v in INDICES.items()})
    return dict(source='Artificial Analysis', attribution=ATTRIBUTION, endpoint=ENDPOINT,
                fetched_at=fetched_at, response_sha256=hashlib.sha256(raw).hexdigest(),
                indices=INDICES, configurations=configurations)


def attach(models, snap):
    """Add AA index values to site models; configurations absent from the snapshot stay null."""
    for model in models:
        entry = snap['configurations'].get(model['agent']) or {}
        for key in INDICES:
            model[key] = entry.get(key)
        model['aa_match'] = entry.get('match')
        model['aa_name'] = entry.get('aa_name')
    return dict(source=snap['source'], attribution=snap['attribution'], fetched_at=snap['fetched_at'],
                response_sha256=snap['response_sha256'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    snap = sub.add_parser('snapshot', help='fetch once and write mapped index values')
    snap.add_argument('mapping', help='JSON {"configurations": {agent: {aa_id, match, note} | {aa_id: null, reason}}}')
    snap.add_argument('--output', required=True)
    snap.add_argument('--response', help='use a saved API response instead of fetching')
    listing = sub.add_parser('list', help='print AA ids, names and both indices (for writing the mapping)')
    listing.add_argument('--response', help='use a saved API response instead of fetching')
    args = parser.parse_args()
    if args.response:
        raw = Path(args.response).read_bytes()
    else:
        key = os.environ.get('AA_API_KEY')
        if not key:
            parser.exit(1, 'error: set AA_API_KEY\n')
        raw = fetch(key)
    if args.command == 'list':
        for m in json.loads(raw)['data']:
            e = m['evaluations']
            print('\t'.join(str(x) for x in (m['id'], m['name'], m.get('release_date'),
                                             *(e.get(v) for v in INDICES.values()))))
        return
    fetched_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if args.response:
        fetched_at = datetime.fromtimestamp(Path(args.response).stat().st_mtime, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        result = snapshot(json.loads(Path(args.mapping).read_text()), raw, fetched_at)
    except (KeyError, ValueError) as exc:
        parser.exit(1, f'error: {exc}\n')
    Path(args.output).write_text(json.dumps(result, indent=1) + '\n')
    matched = sum(e['aa_id'] is not None for e in result['configurations'].values())
    print(f'Wrote {args.output}: {matched}/{len(result["configurations"])} configurations matched', file=sys.stderr)


if __name__ == '__main__':
    main()
