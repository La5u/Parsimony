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
import math
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


MAX_RESPONSE_BYTES = 16 * 1024 * 1024


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # urllib otherwise copies x-api-key to redirected requests, including other hosts.
        return None


def fetch(key):
    if not isinstance(key, str) or not key.strip() or any(c in key for c in '\r\n'):
        raise ValueError('invalid AA_API_KEY')
    request = urllib.request.Request(ENDPOINT, headers={'x-api-key': key, 'User-Agent': 'parsimony'})
    with urllib.request.build_opener(_NoRedirect()).open(request, timeout=60) as response:
        raw = response.read(MAX_RESPONSE_BYTES + 1)
    if len(raw) > MAX_RESPONSE_BYTES:
        raise ValueError('Artificial Analysis response exceeds size limit')
    return raw


def _object(value, label):
    if not isinstance(value, dict):
        raise ValueError(f'{label} must be an object')
    return value


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be a nonempty string')
    return value


def _index(value, label):
    if value is not None and (type(value) not in (int, float) or
                              (isinstance(value, float) and not math.isfinite(value))):
        raise ValueError(f'{label} must be a finite number or null')
    return value


def _response_models(raw):
    response = _object(json.loads(raw), 'response')
    data = response.get('data')
    if not isinstance(data, list):
        raise ValueError('response data must be a list')
    models = {}
    for model in data:
        _object(model, 'response model')
        aa_id = _text(model.get('id'), 'response model id')
        if aa_id in models:
            raise ValueError(f'duplicate Artificial Analysis id {aa_id}')
        _text(model.get('name'), f'{aa_id}: name')
        _text(model.get('slug'), f'{aa_id}: slug')
        evaluations = _object(model.get('evaluations'), f'{aa_id}: evaluations')
        for name in INDICES.values():
            _index(evaluations.get(name), f'{aa_id}: {name}')
        models[aa_id] = model
    return models


def snapshot(mapping, raw, fetched_at):
    models = _response_models(raw)
    _object(mapping, 'mapping')
    entries = _object(mapping.get('configurations'), 'mapping configurations')
    for agent, entry in entries.items():
        _text(agent, 'agent')
        _object(entry, f'{agent}: configuration')
        if 'aa_id' not in entry:
            raise ValueError(f'{agent}: aa_id is required (use explicit null for unmapped configurations)')
        if entry['aa_id'] is None:
            _text(entry.get('reason'), f'{agent}: reason')
        else:
            _text(entry['aa_id'], f'{agent}: aa_id')
            _text(entry.get('match'), f'{agent}: match')
    configurations = {}
    for agent, entry in sorted(entries.items()):
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
    _object(snap, 'snapshot')
    configurations = _object(snap.get('configurations'), 'snapshot configurations')
    # Validate before mutating any site models, including stale values on unmapped entries.
    for agent, entry in configurations.items():
        _object(entry, f'{agent}: configuration')
        for key in INDICES:
            _index(entry.get(key), f'{agent}: {key}')
        if entry.get('aa_id') is None and any(entry.get(key) is not None for key in INDICES):
            raise ValueError(f'{agent}: unmapped configuration has index values')
    metadata = dict(source=snap['source'], attribution=snap['attribution'], fetched_at=snap['fetched_at'],
                    response_sha256=snap['response_sha256'])
    for model in models:
        entry = configurations.get(model['agent']) or {}
        for key in INDICES:
            model[key] = entry.get(key)
        model['aa_match'] = entry.get('match')
        model['aa_name'] = entry.get('aa_name')
    return metadata


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
        try:
            raw = fetch(key)
        except ValueError as exc:
            parser.exit(1, f'error: {exc}\n')
        except OSError:
            parser.exit(1, 'error: Artificial Analysis fetch failed\n')
    if args.command == 'list':
        try:
            response_models = _response_models(raw)
        except ValueError as exc:
            parser.exit(1, f'error: {exc}\n')
        for m in response_models.values():
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
