#!/usr/bin/env python3
"""Cross-check AiWork.Code + Claude Opus 5.5 (Live Lite, open PR 60) trajectories against preds.json.

The submission has no separate patch file: `trajs/<id>.md` is the agent's JSON event stream, and
its tool outputs are often truncated previews. So the check is corroboration only: does the last
tool output that shows a diff contain the exact preds.json patch? A complete, conflicting final
copy would set a task aside (as with TianxiCode Go); none exists here. Also counts the model/effort
markers and trajectories that end without a completion event. Inputs and raw cache stay external;
output is scalars and hashes only. Never executes target code.

    PYTHONPATH=. python examples/benchmark-discovery/review-aiwork-opus55-live.py \
      --external-dir ~/parsimony-live-ml/opus55 --output examples/benchmark-discovery/aiwork-opus55-release.json
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path

from parsimony.artifacts import Cache
from parsimony.scoring import measured, out_of_scope

REVISION = '36022565d01a5f828d65e7ef9a541d056c579beb'
CONFIG = 'submissions/lite/aiwork-code/20261021-opus-5-5-xhigh'
ROOT = f'https://raw.githubusercontent.com/SWE-bench-Live/submission/{REVISION}/{CONFIG}'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strings(value, depth=0):
    """Every string in an event, also inside JSON-encoded tool results."""
    if isinstance(value, str):
        yield value
        if depth < 4 and value[:1] in '{[':
            try:
                yield from strings(json.loads(value), depth + 1)
            except ValueError:
                pass
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item, depth)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item, depth)


def review(task, patch, raw):
    diff_events, copies, names = [], [], Counter()
    for i, line in enumerate(raw.decode('utf-8').splitlines()):
        try:
            event = json.loads(line)
        except ValueError:
            continue  # the CLI's plain-text banner lines
        names[event.get('event', {}).get('name')] += 1
        found = list(strings(event))
        if any('diff --git' in s for s in found):
            diff_events.append(i)
        if patch and any(patch in s for s in found):
            copies.append(i)
    text = raw.decode('utf-8')
    if not patch:
        status = 'empty_patch'
    elif not copies:
        status = 'no_full_copy_in_trajectory'
    elif copies[-1] == diff_events[-1]:
        status = 'last_diff_output_contains_patch'
    else:
        status = 'earlier_diff_output_contains_patch'
    return dict(task_id=task, status=status, trajectory_sha256=sha(raw), bytes=len(raw),
                completed=names['stream.completed'] > 0,
                model_marker='"model":"primary/claude-opus-5-5"' in text,
                effort_marker='"effort":"xhigh"' in text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--external-dir', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    external = Path(args.external_dir)
    run = json.loads((external / 'claude_opus_5_5.inventory.json').read_text())
    if run['submission_revision'] != REVISION or run['config'] != CONFIG or len(run['records']) != 300:
        parser.error('expected the pinned full 300-task Opus 5.5 cohort')
    cache = Cache(external / 'cache', timeout=90)
    patches = {r['task_id']: r['patch'] or '' for r in run['records']}
    with ThreadPoolExecutor(max_workers=12) as pool:
        evidence = list(pool.map(lambda t: review(t, patches[t], cache.get(f'{ROOT}/trajs/{t}.md')),
                                 sorted(patches)))
    raw = (external / 'claude_opus_5_5.records.jsonl').read_bytes()
    records = [json.loads(line) for line in raw.splitlines()]
    audit_bytes = (external / 'claude_opus_5_5.preimages.json').read_bytes()
    eligible = [r for r in records if measured(r) and not out_of_scope(r['metrics'])]
    excluded = [r for r in records if measured(r) and out_of_scope(r['metrics'])]
    solved = [r for r in eligible if r['resolved']]
    identity = {(r['analyzer_commit'], r['analyzer_version'], r['analyzer_source_sha256'], r['python_version'])
                for r in records}
    if len(identity) != 1:
        raise ValueError('mixed analyzer identities')
    commit, version, source, python = identity.pop()
    summary = dict(
        schema_version=1, label='Claude Opus 5.5 (xhigh) · AiWork.Code', agent=records[0]['agent'],
        source=dict(repository='SWE-bench-Live/submission', pull_request=60, pull_request_state='open, unmerged',
                    head_repository='x4vierli/submission', submission_revision=REVISION, config=CONFIG,
                    submission_url=f'https://github.com/SWE-bench-Live/submission/tree/{REVISION}/{CONFIG}'),
        open_network=('Submission README: every rollout ran with open network access; the agent could search '
                      'the web and read the upstream repository, issues, pull requests and commits and adapt '
                      'an upstream fix (in-container probe: github = OPEN). The board\'s Claude Opus 4.8 · '
                      'AiWork.Code run (20260909) ran with GitHub blocked.'),
        dataset_checksum=run['dataset']['dataset_checksum'], result_sha256=run['result_sha256'],
        prediction_sha256=run['prediction_sha256'], preimage_audit_sha256=sha(audit_bytes),
        preimage_status_counts=json.loads(audit_bytes)['status_counts'],
        records_sha256=sha(raw), analyzer_commit=commit, analyzer_version=version,
        analyzer_source_sha256=source, python_version=python, population=len(records),
        published_outcome_counts=dict(Counter(r['published_outcome'] for r in records)),
        analysis_status_counts=dict(Counter(r['analysis_status'] for r in records)),
        footprint=dict(eligible=len(eligible), excluded_only=len(excluded),
                       successful_eligible=len(solved), failed_eligible=len(eligible) - len(solved),
                       excluded_outcomes=dict(Counter(r['evaluation_result'] for r in excluded)),
                       mean_net_units=sum(r['metrics']['net_units'] for r in eligible) / len(eligible),
                       solved_mean_net_units=sum(r['metrics']['net_units'] for r in solved) / len(solved)),
        trajectory_check=dict(
            status_counts=dict(Counter(e['status'] for e in evidence)),
            without_completion_event=sorted(e['task_id'] for e in evidence if not e['completed']),
            model_marker=sum(e['model_marker'] for e in evidence),
            effort_xhigh_marker=sum(e['effort_marker'] for e in evidence),
            set_aside=[], semantics='corroboration only; trajectories hold no separate final patch copy'),
        evidence=evidence,
        rights_status='numeric-metadata-only-not-raw-artifact-redistribution',
        protocol_status='source-reported-not-independently-certified', historical_dataset_match='unverified')
    Path(args.output).write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print({k: v for k, v in summary.items() if k != 'evidence'})


if __name__ == '__main__':
    main()
