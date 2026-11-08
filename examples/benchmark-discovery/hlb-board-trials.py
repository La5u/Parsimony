"""Freeze the Harness Leaderboard's public-board DeepSWE trial set as trials.json for parsimony.hlb.

A port of hlb.scoring.board_facts (public=True) of the Space (Apache-2.0) at a pinned commit; only the
Space's data files (hlb/data/*.json and the first line of each adapter bundle) are read, its code is not run.
Two additions reproduce what the Space sees from its long-lived cache: a source run's invalid rules
apply to the trial's copies, and a rule listing a trial by name in any run of the same model covers it
(copies of copies name only the first source; the run in between may no longer hold trial facts).
Checked 2026-11-08: every GLM-5.3-Flash and DeepSeek-V4.1-Flash DeepSWE cell matches the published
board's scored and passed counts (index/public.json, generated 2026-11-08T10:06:59Z).

    SPACE_SRC  the Space's files at the pinned commit (hlb/data/...)
    FACTSDIR   bucket files runs/<run>/{run.json,invalid.json,deep-swe/trials-*.jsonl}, '/' replaced by '__'
    WHERE.json {trial: [run whose deep-swe/ folder holds it]} from listing the bucket

usage: hlb-board-trials.py SPACE_SRC FACTSDIR WHERE.json OUT.json
"""
import glob, hashlib, json, os, sys
from collections import Counter, defaultdict

src, factsdir, where, out = sys.argv[1:5]
where = json.load(open(where))
data = lambda n: json.load(open(f'{src}/hlb/data/{n}.json'))
HARN, MODELS, BENCH = data('harnesses')['harnesses'], data('models')['models'], data('benchmarks')['benchmarks']
ATTEMPTS = {'smoke': 1, 'pilot': 1, 'full': 3}
PROVIDER_FAILURE_LIMIT = 6
PROVIDER_FAILURE = {429, 500, 502, 503, 504, 529, 599}
SANDBOX_FAILURE = {"EnvironmentStartTimeoutError", "DockerfileReplayError", "MeterStartError", "OSPrepError", "NetworkPolicyError",
                   "FeatureBenchIsolationError", "SandboxError", "ReadTimeout", "RemoteProtocolError", "ConnectError", "ConnectTimeout",
                   "ReadError", "WriteError", "WriteTimeout", "PoolTimeout"}
LEFT_OUT = 'left out'
RULE_VERDICTS = (LEFT_OUT, 'fail', 'infra')


def adapter_id(name):
    if name is None:
        return None
    with open(f'{src}/hlb/data/{name}.cjs') as f:
        return f"{name}@{hashlib.sha256(f.readline().encode()).hexdigest()[:12]}"


def released(h): return HARN[h].get('released', True) is not False
def public_version(h): return HARN[h].get('public_version', HARN[h]['version'])
def public_adapter(h): return adapter_id(HARN[h]['public_adapter']) if 'public_adapter' in HARN[h] else adapter_id(HARN[h].get('adapter'))


def pool(model):
    spec = MODELS[model]; ref = spec['default_provider']
    return [ref] + [p for p, e in spec.get('equivalence', {}).items() if p != ref and e.get('admitted') is True]


def setup_provider(model, provider):
    spec = MODELS.get(model)
    return spec['default_provider'] if spec and provider in pool(model) else provider


def on_board(run, harness, bench):
    model = MODELS.get(run['model'])
    if not model or harness not in HARN or not released(harness):
        return False
    setup = run['benchmark_setups'].get(bench) or {}
    want = {'commit': BENCH[bench]['commit']}
    return (setup_provider(run['model'], run['provider']) == model['default_provider']
            and run['harness_versions'].get(harness) == public_version(harness)
            and run.get('harness_adapters', {}).get(harness) == public_adapter(harness)
            and setup.get('commit') == want['commit'] and setup.get('reference_isolation') is None)


def outcome(f):
    if (f.get('answer_key') or {}).get('received'):
        return 'fail'
    if f['exception'] == 'CancelledError':
        return 'cancelled'
    if f.get('featurebench_verifier_exception') == 'FeatureBenchIsolationError' or f.get('bridge_rejection'):
        return 'infra'
    if not f['agent_started']:
        return 'infra'
    meter = f['meter'] or {}
    died = f['exception'] not in (None, 'AgentTimeoutError') and not meter.get('n_calls')
    if died or meter.get('last_status') in PROVIDER_FAILURE:
        return 'infra'
    if f['exception'] in SANDBOX_FAILURE or (f['reward'] is not None and f['reward'] < 0):
        return 'infra'
    return 'pass' if (f['reward'] or 0) >= 1.0 else 'fail'


def rule_verdict(f, invalid):
    keys = (('harnesses', 'harness'), ('benchmarks', 'benchmark'), ('tasks', 'task'), ('trials', 'trial'))
    found = {r.get('outcome', LEFT_OUT) for r in (invalid or {}).get('rules', []) if all(f[k2] in r.get(k, [f[k2]]) for k, k2 in keys)}
    return min(found, key=RULE_VERDICTS.index) if found else None


runs = {}
for p in glob.glob(f'{factsdir}/runs__*__run.json'):
    r = json.load(open(p)); runs[r['run_id']] = r
invalid = {os.path.basename(p).split('__')[1]: json.load(open(p)) for p in glob.glob(f'{factsdir}/runs__*__invalid.json')}
facts = [json.loads(l) for p in glob.glob(f'{factsdir}/runs__*__deep-swe__trials-*.jsonl') for l in open(p) if l.strip()]
named = defaultdict(lambda: defaultdict(list))  # trial name -> run -> rules that list it
for r, d in invalid.items():
    for rule in d.get('rules', []):
        for t in rule.get('trials', []):
            named[t][r].append(rule)
verdicts = {}
for f in facts:
    # A rule covers the trial in every run that holds it. The source run's own trial files may be gone
    # from the bucket (only the kept copy stays), so its rules are applied to the copy here.
    vs = [rule_verdict(f, invalid.get(r)) for r in (f['run_id'], f.get('reused_from')) if r]
    # A copy of a copy names only the first source; rules that list the trial by name in any other
    # run of the same model (a run in between, whose own files are gone) cover it too.
    vs += [rule_verdict(f, {'rules': rules}) for r, rules in named.get(f['trial'], {}).items()
           if r in runs and runs[r]['model'] == (runs.get(f['run_id']) or {}).get('model')]
    vs = [v for v in vs if v]
    v = min(vs, key=RULE_VERDICTS.index) if vs else None
    if v and (f['id'] not in verdicts or RULE_VERDICTS.index(v) < RULE_VERDICTS.index(verdicts[f['id']])):
        verdicts[f['id']] = v
judged = lambda f: verdicts.get(f['id']) or outcome(f)
ended_on_provider = lambda f: f['id'] not in verdicts and outcome(f) == 'infra' and bool((f['meter'] or {}).get('n_calls')) and (f['meter'] or {}).get('last_status') in PROVIDER_FAILURE
order_of = lambda f: ((runs.get(f.get('reused_from') or '') or runs.get(f['run_id']) or {}).get('created_at', ''), f['id'])
def copy_rank(rid):
    r = runs.get(rid) or {}
    return r.get('stage') != 'full', r.get('created_at') or '~', rid

tasks = set(BENCH['deep-swe']['subsets']['full'])
groups, failures, copies = defaultdict(dict), defaultdict(lambda: defaultdict(set)), defaultdict(set)
for f in facts:
    copies[f['id']].add(f['run_id'])
    run = runs.get(f['run_id'])
    if run is None or run['stage'] != 'full' or f['benchmark'] != 'deep-swe' or f['task'] not in tasks or not on_board(run, f['harness'], 'deep-swe') \
            or setup_provider(run['model'], f.get('provider') or run['provider']) != MODELS[run['model']]['default_provider']:
        continue
    o = judged(f)
    if o in (LEFT_OUT, 'cancelled'):
        continue
    key = (run['model'], run['reasoning_effort'], f['harness'])
    if ended_on_provider(f):
        failures[key][f['task']].add(f['id'])
    order = order_of(f)
    have = groups[key].get(f['id'])
    if have is None or (order, copy_rank(f['run_id'])) < (have['_order'], copy_rank(have['run_id'])):
        groups[key][f['id']] = {**f, '_outcome': o, '_order': order}

cells = {}
for key, by_id in groups.items():
    by_task = defaultdict(list)
    for f in sorted(by_id.values(), key=lambda f: f['_order']):
        by_task[f['task']].append(f)
    kept = []
    for task, att in by_task.items():
        scored = sum(judged(f) in ('pass', 'fail') for f in att)
        failed = [f for f in att if ended_on_provider(f)]
        filled = {f['id'] for f in failed[:3 - scored]} if scored < 3 and len(failures[key].get(task, set())) >= PROVIDER_FAILURE_LIMIT else set()
        n = 0
        for f in att:
            o = 'fail' if f['id'] in filled else f['_outcome']
            if o not in ('pass', 'fail'):
                continue  # infra trials are kept by the board for its error rate only
            n += 1
            if n > 3:
                continue
            kept.append(dict(task=task, attempt=n, trial=f['trial'], id=f['id'], outcome=o, run_id=f['run_id'],
                             reused_from=f.get('reused_from'), copies=sorted(copies[f['id']]), reward=f['reward'],
                             provider_exhausted=f['id'] in filled, answer_key_requested=bool((f.get('answer_key') or {}).get('requested'))))
    cells[' | '.join(key)] = kept

MODEL_IDS = {'zai-org/GLM-5.3-Flash', 'deepseek-ai/DeepSeek-V4.1-Flash'}  # complete full-stage runs on the public board
setups = {}
for key, kept in sorted(cells.items()):
    model, effort, harness = key.split(' | ')
    if model not in MODEL_IDS:
        continue
    for t in kept:
        runs_with = where.get(t['trial'], [])
        t['patch'] = f"runs/{runs_with[0]}/deep-swe/{t['trial']}/artifacts/logs/artifacts/model.patch" if runs_with else None
    setups[f"{model.split('/')[1].lower()}_{effort}_{harness}"] = dict(
        model=model, reasoning_effort=effort, harness=harness, harness_version=public_version(harness),
        trials=[{k: t[k] for k in ('task', 'attempt', 'trial', 'outcome', 'patch')} for t in sorted(kept, key=lambda t: (t['task'], t['attempt']))])
space_commit = os.path.basename(os.path.normpath(src)).split('-')[-1]
doc = dict(source='Harness Leaderboard public board, DeepSWE v1.1 (111 tasks at datacurve-ai/deep-swe 0b9fabbb), full stage, 3 attempts',
           space='https://huggingface.co/spaces/joelniklaus/harness-leaderboard', space_commit=space_commit,
           bucket='https://huggingface.co/buckets/joelniklaus/harness-leaderboard', setups=setups)
with open(out, 'w') as stream:
    json.dump(doc, stream, indent=1, sort_keys=True)
    stream.write('\n')
for k, v in setups.items():
    c = Counter(t['outcome'] for t in v['trials'])
    print(k, dict(c), 'no patch:', sum(not t['patch'] for t in v['trials']))
