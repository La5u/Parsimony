# SWE-Milestone — TypeScript

Website: **[parsimony.lasu.dev/swe-milestone.html](https://parsimony.lasu.dev/swe-milestone.html)** (Go, TypeScript and Python combined). Other languages: [Go](../swe-milestone-go/README.md) · [Python](../swe-milestone-python/README.md).

[SWE-Milestone](https://swe-milestone.com) ([paper](https://arxiv.org/abs/2603.13428)) gives an agent a feature specification for one *milestone* of a real project's history, a group of upstream commits, and grades the result with the maintainers' tests. This board uses its **per-milestone trials** (`mstone_trial`): each milestone starts fresh from its own prepared start state. The end-to-end trials, where one agent works through every milestone in one workspace, are not used: each snapshot there includes all earlier milestones' work, and most attempts fail.

**This compares model + agent setups, not models alone:** each model ran in its vendor's CLI agent (Claude Code, Codex, Gemini CLI). One attempt per milestone, so rank ranges are wide. Pass/fail is SWE-Milestone's own test verdict, not rechecked here. These runs date from January–February 2026, so the models are older than on the other boards.

## Population

Repositories: `element-hq/element-web` (18 milestones; `.ts`/`.tsx`/`.js`/`.jsx` files). A milestone is included when it is graded (`selected_milestone_ids.txt`, or every milestone where no list exists) and its reference change, start tag to end tag, touches at least one in-scope TypeScript file. The rule uses only the reference, never model output or outcomes. `population.jsonl` lists every milestone with its start commit; `population-manifest.json` freezes it. All 10 configurations have an outcome for every milestone.

## How a patch is rebuilt

SWE-Milestone publishes each attempt as `source_snapshot.tar`: the source directories at the agent's submission tag, with tests removed. The start state is the HEAD of the milestone's pinned image (`manifests/digests-v1.0.2.tsv` in the harness), It was extracted from each image into a local repository. The patch is snapshot minus start state, for in-scope files only, measured on the start-state sources.

- A start-state file missing from a snapshot counts as **deleted** only if another configuration's snapshot of that milestone kept it, or the reference deletes it. Otherwise the harness filtered it out.
- A snapshot missing more than a quarter (and more than 20) of the start state's in-scope files is **incomplete** (`partial_snapshot`): the agent's commit lacked whole source directories, which the harness logs as non-existent. Its outcome is kept; its footprint is unknown, never zero. This affects 3 GPT-5.2 Go attempts.
- The trial logs agree: every log that names its start commit (`Fallback base commit`, 474 of 600) names the image HEAD for its final attempt (471), except GPT-5.2 on go-zero M017, M018 and M025. Those three ran on 2026-02-08 from a different start state, and they are the three incomplete snapshots above. The other 126 logs (all 120 scikit-learn, 6 navidrome) only name the release tag they squash onto.
- Outcomes come from `evaluation_result_filtered.json` when present, otherwise `evaluation_result.json`, as SWE-Milestone's own collector does.

Of 180 attempts: 173 measured, 4 empty patches, 3 whose result does not parse. Outcomes: 82 pass, 98 fail. Missing measurements are never zero. Coverage: [coverage.json](coverage.json); stability: [stability.md](stability.md).

## Results (analyzer 0.10.0-beta)

Same-task ratio, as on the website: a model's net units added on the milestones it solved, divided by what the other ranked models added on those same milestones (0.8× = 20% less code). This ranks the smallest measured footprint, not the best coding model.

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Gemini 3 Pro · Gemini CLI | 0.69× | -5.93–1.02× | 8 | +155.5 | +340.6 | 44.4% | 8/8 |
| 2 | GPT-5.2 Codex · Codex | 0.86× | — | 3 | +471.0 | +462.5 | 16.7% | 3/3 |
| 3 | Gemini 3 Flash · Gemini CLI | 0.87× | 0.76–0.96× | 6 | +441.8 | +358.0 | 38.9% | 6/7 |
| 4 | Gemini 3.1 Pro · Gemini CLI | 0.89× | 0.80–0.98× | 8 | +619.2 | +417.1 | 44.4% | 8/8 |
| 5 | GPT-5.2 · Codex | 0.92× | -2.32–2.76× | 6 | +179.5 | +522.8 | 33.3% | 6/6 |
| 6 | Claude Sonnet 4.5 · Claude Code | 0.98× | 0.89–1.08× | 6 | +541.0 | +517.9 | 33.3% | 6/6 |
| 7 | Claude Opus 4.5 · Claude Code | 1.00× | 0.95–1.05× | 8 | +851.0 | +553.3 | 44.4% | 8/8 |
| 8 | Claude Sonnet 4.6 · Claude Code | 1.03× | 0.14–1.40× | 11 | +560.7 | +448.4 | 72.2% | 13/13 |
| 9 | GPT-5.3 Codex · Codex | 1.14× | 1.02–1.38× | 9 | +833.1 | +545.7 | 61.1% | 11/11 |
| 10 | Claude Opus 4.6 · Claude Code | 1.15× | 0.85–4.43× | 11 | +636.9 | +448.7 | 66.7% | 12/12 |

Combined across Go, TypeScript and Python (each language's ratio weighted by its shared milestones; units are never added across languages):

| Rank | Model | Vs. others, same tasks | 95% range | Tasks | Net units, solved (mean) | Net units, all measured (mean) | Solved | Measured |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 1 | Gemini 3 Pro · Gemini CLI | 0.81× | -1.15–1.00× | 20 | — | — | 35.0% | 21/21 |
| 2 | Claude Sonnet 4.5 · Claude Code | 0.91× | 0.80–1.04× | 12 | — | — | 20.0% | 12/12 |
| 3 | GPT-5.3 Codex · Codex | 0.94× | 0.68–1.48× | 19 | — | — | 40.0% | 24/24 |
| 4 | Gemini 3 Flash · Gemini CLI | 0.94× | 0.89–1.06× | 14 | — | — | 25.0% | 14/15 |
| 5 | Claude Opus 4.6 · Claude Code | 0.95× | 0.21–2.19× | 26 | — | — | 50.0% | 30/30 |
| 6 | Claude Opus 4.5 · Claude Code | 0.95× | 0.57–1.29× | 22 | — | — | 38.3% | 23/23 |
| 7 | Gemini 3.1 Pro · Gemini CLI | 1.02× | 0.91–1.09× | 21 | — | — | 38.3% | 23/23 |
| 8 | Claude Sonnet 4.6 · Claude Code | 1.09× | 0.52–1.31× | 25 | — | — | 50.0% | 30/30 |
| 9 | GPT-5.2 · Codex | 1.15× | 0.50–2.10× | 16 | — | — | 30.0% | 18/18 |
| 10 | GPT-5.2 Codex · Codex | 1.33× | 0.85–1.66× | 10 | — | — | 21.7% | 13/13 |

## Sources

- Runs: Hugging Face [`DeepCommit-ai/SWE-Milestone-log` at `03d82b7`](https://huggingface.co/datasets/DeepCommit-ai/SWE-Milestone-log/tree/03d82b7e48d4c5c8c3c76a8a8bb80901659d9f99), `mstone_trial/` (10 configurations). Gated: Hugging Face asks you to share your username and email with the dataset owner; access is approved automatically. Licence MIT.
- Start states: Docker Hub images `hyd2apse/swe-milestone__<repo>__<milestone>` pinned by digest in [`manifests/digests-v1.0.2.tsv`](https://github.com/DeepCommit-ai/SWE-Milestone/blob/17a8f1593e172e26b36cea15e2b30fb9536c93f5/manifests/digests-v1.0.2.tsv) of the harness at `17a8f15`. Each record holds the image digest, the start commit and the start/end tag commits.
- Records hold scalars and hashes only; snapshots are not redistributed.
- Measured at analyzer commit `feb9d04`, Python 3.14.8, TypeScript 5.9.3, `tree-sitter==0.26.0` with the pinned Go grammar (`tree-sitter-go-units-v2`).

## Reproduce

```sh
hf download DeepCommit-ai/SWE-Milestone-log --repo-type dataset --revision 03d82b7e48d4c5c8c3c76a8a8bb80901659d9f99 \
  --local-dir data --include '*/metadata.json' '*/milestones.csv' '*/selected_milestone_ids.txt' '*/mstone_trial/*'
# For each milestone, pull its image by digest and fetch /testbed HEAD as refs/start/<milestone>, plus all tags,
# into git/<dataset dir> (a bare repository); record digest and HEAD in baselines.json.
python -m parsimony.milestone dataset data --baselines baselines.json --git git --output population-all.jsonl
# split population-all.jsonl by language, then for each of the 10 configurations:
python -m parsimony.milestone analyze data --dataset population.jsonl --git git \
  --agent milestone-claude-code-opus-4.6 --language typescript --output milestone-claude-code-opus-4.6.jsonl
E=examples/swe-milestone-typescript
python -m parsimony.release freeze $E/population.jsonl --name swe-milestone-typescript-v1 --output population-manifest.json
python -m parsimony.scoring freeze $E/milestone-*.jsonl --name swe-milestone-typescript-v1 --population $E/population-manifest.json --output score-panel.json
python -m parsimony.release audit $E/population-manifest.json $E/milestone-*.jsonl --output coverage.json
python -m parsimony.stability $E/score-panel.json $E/milestone-*.jsonl --output stability.json
```
