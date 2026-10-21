"""Print a board's same-task ranking as a Markdown table from its built page, for the board README.

    python scripts/readme-ranking-table.py site/sweeper-php.html
"""
import re, json, sys
def rows(page):
    s = open(page).read()
    d = json.loads(re.search(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', s, re.S).group(1))
    return [m for m in d['models'] if not m.get('self_run')]
def f(v, signed=True):
    return '—' if v is None else (f'{v:+,.1f}' if signed else f'{v:,.1f}')
def table(page):
    ms = rows(page)
    out = ['| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |',
           '|---:|---|---:|---|---:|---:|---:|---:|---:|']
    rank, prev, ranked = 0, None, 0
    for m in ms:
        r = m.get('same_task_net')
        unranked = m.get('few_tasks') or m.get('partial')  # listed, not ranked
        if r is not None and not unranked:
            ranked += 1
            if r != prev: rank, prev = ranked, r
        ci = m.get('same_task_net_ci')
        out.append(f"| {rank if r is not None and not unranked else '—'} | {m['name']} | {'—' if r is None else f'{r:.2f}×'} | "
                   f"{f'{ci[0]:.2f}–{ci[1]:.2f}×' if ci else '—'} | {m.get('same_task_net_tasks') or '—'} | {f(m.get('measured_solved_net_mean'))} | {f(m.get('measured_net_mean'))} | "
                   f"{'—' if m.get('resolve_rate') is None else f'{100 * m['resolve_rate']:.1f}%'} | {m.get('measured_solved_attempts', 0)}/{m.get('upstream_solved_attempts', 0)} |")
    return '\n'.join(out)
if __name__ == '__main__':
    print(table(sys.argv[1]))
