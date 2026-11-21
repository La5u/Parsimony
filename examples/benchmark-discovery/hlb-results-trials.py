"""Freeze the Harness Leaderboard's DeepSWE trials as trials.json for parsimony.hlb, from its published results/.

Since v0.1.9 the leaderboard publishes exactly the trials its public board counts (results/trials.csv.gz, hashed in
results/index.json), so this replaces the port of its scoring code (hlb-board-trials.py, used up to v0.1.2).
Only scored DeepSWE trials (pass or fail, attempts 1-3) are kept; infra-excluded trials are not scored by the board.

usage: hlb-results-trials.py TRIALS.csv.gz INDEX.json SPACE_COMMIT OUT.json [--skip-model ID ...]
"""
import csv, gzip, hashlib, json, sys
from collections import Counter

trials_csv, index_json, space_commit, out, *rest = sys.argv[1:]
skip = set(rest[rest.index('--skip-model') + 1:]) if '--skip-model' in rest else set()
index = json.load(open(index_json))
digest = hashlib.sha256(open(trials_csv, 'rb').read()).hexdigest()
if index['files']['results/trials.csv.gz']['sha256'] != digest:
    sys.exit(f'trials.csv.gz sha256 {digest} does not match index.json')
setups = {}
for r in csv.DictReader(gzip.open(trials_csv, 'rt')):
    if r['benchmark'] != 'deep-swe' or r['verdict'] not in ('pass', 'fail') or r['model'] in skip:
        continue
    key = f"{r['model'].split('/')[1].lower()}_{r['effort']}_{r['harness']}"
    s = setups.setdefault(key, dict(model=r['model'], reasoning_effort=r['effort'], harness=r['harness'],
                                    harness_version=r['harness_version'], trials=[]))
    s['trials'].append(dict(task=r['task'], attempt=int(r['attempt']), trial=r['trial'], outcome=r['verdict'],
                            patch=f"{r['trial_path'].rstrip('/')}/artifacts/logs/artifacts/model.patch"))
for s in setups.values():
    s['trials'].sort(key=lambda t: (t['task'], t['attempt']))
doc = dict(source=f"Harness Leaderboard public board v{index['release']}, results/trials.csv.gz (sha256 {digest}), "
                  'DeepSWE v1.1 (111 tasks at datacurve-ai/deep-swe 0b9fabbb), full stage, 3 attempts',
           space='https://huggingface.co/spaces/joelniklaus/harness-leaderboard', space_commit=space_commit,
           release=index['release'], bucket='https://huggingface.co/buckets/joelniklaus/harness-leaderboard',
           setups=dict(sorted(setups.items())))
with open(out, 'w') as stream:
    json.dump(doc, stream, indent=1, sort_keys=True)
    stream.write('\n')
for k, v in doc['setups'].items():
    print(k, dict(Counter(t['outcome'] for t in v['trials'])))
