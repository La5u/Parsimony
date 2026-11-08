"""Stream trajectory files of a submission and count reference-fix access signals per instance.
usage: oracle-audit.py RAWBASE TREEFILE PREFIX OUT.json  (RAWBASE = https://raw.githubusercontent.com/o/r/sha)"""
import sys, re, json, urllib.request, concurrent.futures as cf
rawbase, treefile, prefix, out = sys.argv[1:5]
files = [l.split(' ',1)[1].strip() for l in open(treefile) if l.split(' ',1)[1].startswith(prefix)]
import os
trajs = [f for f in files if '/traj' in f and not re.search(r'(prompt\.txt|patch[^/]*\.diff|meta\.json|git-status\.txt|evaluation\.json|results\.json)$', f)]
res_files = [f for f in files if f.endswith('/results.json') and '/trajs/' not in f and '/logs/' not in f]
def get(p):
    for _ in range(3):
        try: return urllib.request.urlopen(f"{rawbase}/{urllib.parse.quote(p)}", timeout=120).read().decode('utf-8','replace')
        except Exception as e: err=e
    return None
import urllib.parse
def inst_of(p):
    rest = p[len(prefix):].lstrip('/').split('/')
    for seg in rest:
        if '__' in seg: return re.sub(r'\.(md|json|jsonl|txt|traj)$','',seg)
    return None
def scan(p):
    inst = inst_of(p); t = get(p)
    if t is None or inst is None: return inst, None
    m = re.match(r'(.+?)__(.+)-(\d+)$', inst)
    sig = {}
    if m:
        o, r, n = map(re.escape, m.groups())
        sig['own_pr_url'] = len(re.findall(rf'github\.com/{o}/{r}/(?:pull|pulls|issues)/{n}\b|repos/{o}/{r}/(?:pulls|issues)/{n}\b', t, re.I))
    sig['git_show_hash'] = len(re.findall(r'git (?:-C \S+ )?show\s+(?:--\S+\s+)*[0-9a-f]{7,40}\b', t))
    sig['git_log_all'] = len(re.findall(r'git (?:-C \S+ )?log[^\n"]*?(?:--all|--remotes|--branches|origin/)', t))
    sig['git_fetch'] = len(re.findall(r'git (?:-C \S+ )?fetch\b', t))
    sig['webfetch_github_pr'] = len(re.findall(r'github\.com/[\w.-]+/[\w.-]+/(?:pull|commit)/\w+', t))
    return inst, sig
per = {}
with cf.ThreadPoolExecutor(12) as ex:
    for inst, sig in ex.map(scan, trajs):
        if inst is None: continue
        d = per.setdefault(inst, {})
        if sig is None: d['fetch_error'] = True; continue
        for k,v in sig.items(): d[k] = d.get(k,0)+v
resolved = set()
for f in res_files:
    t = get(f)
    try:
        j = json.loads(t); resolved |= set(j.get('success_ids') or j.get('resolved_ids') or j.get('resolved') or [])
    except Exception: pass
summ = {'prefix':prefix,'trajectory_files':len(trajs),'instances':len(per),'resolved_known':len(resolved)}
for k in ['own_pr_url','git_show_hash','git_log_all','git_fetch','webfetch_github_pr']:
    hit = {i for i,d in per.items() if d.get(k)}
    summ[k] = {'instances':len(hit),'resolved':len(hit & resolved)}
anyh = {i for i,d in per.items() if d.get('own_pr_url') or d.get('git_show_hash') or d.get('git_log_all')}
summ['any_strong'] = {'instances':len(anyh),'resolved':len(anyh&resolved)}
json.dump({'summary':summ,'per_instance':per,'resolved':sorted(resolved)}, open(out,'w'), indent=1)
print(json.dumps(summ))
