# Self-run pilot (SELF-RUN, unverified)

An owner-approved exception to Parsimony's "no model calls" rule: newer models that have no public
per-task patches are run by the owner on a few DeepSWE Python tasks, so their footprint can be
plotted next to published boards. **These are not benchmark submissions.** On the website they are
faded, labelled self-run on hover and never ranked.

`plan.json` was committed before any run. It fixes the tasks (the first 10 DeepSWE Python tasks by
`sha256("parsimony-self-run-v1:" + task_id)`), 2 attempts per task, high effort, and the
configurations: OpenAI models through [pi](https://github.com/badlogic/pi-mono) on a ChatGPT
subscription, Anthropic models through Claude Code (`--safe-mode`) on a Claude subscription. Pi
cannot use the Claude subscription (Anthropic bills third-party apps as extra usage), so the two
companies use different harnesses: compare within a company, not across. Since 14 Oct 2026 the GPT-6 family (Luna, Sol, 6.1 Sol, Astra) also runs through the
[Codex CLI](https://github.com/openai/codex) on the same tasks and subscription, so pi and Codex can be compared for the
same model; on the site these show as `· pi` and `· Codex`. Codex runs with `--ephemeral --ignore-user-config`, web
search off and its own workspace-write sandbox for shell commands. GPT-5.6 Sol and Claude
Sonnet 5 also run as anchors, since they are on the published DeepSWE board; their gap shows the
effect of the harness and environment.

Differences from DeepSWE, all identical across self-run configurations:

- Agent harness: pi or Claude Code instead of mini-SWE-agent.
- Environment: host Python 3.14 in a bubblewrap sandbox with the repository at its base commit
  only (no later history, no remote). No task Docker image, no project dependencies.
- Network is not blocked, because the harness calls its API. The prompt forbids network use;
  `meta.json` lists any shell commands that look like network use.
- Footprint is measured from the final diff exactly like published patches. Outcomes are
  **self-graded** afterwards (see Grading); `meta.json` keeps the run-time `outcome: not_graded`.

The sandbox can write only the task directory and the harness credential store. It hides the
DeepSWE checkout (reference solutions), this repository, the download cache and agent transcripts.

## Contributed runs

Since 16 Oct 2026 other people can run configurations too ([CONTRIBUTING.md](../../CONTRIBUTING.md#contributed-runs)):
registered in `plan.json` with a `contributor` handle before running, run with `run.py`, then measured and graded here
exactly like my runs. They show as `Model (effort) · @handle`, faded and unranked. I can verify the patches, the
measurements and the outcomes, but not that the named model wrote them.

## Running

```sh
mkdir -p ~/parsimony-self-run
git clone https://github.com/datacurve-ai/deep-swe ~/parsimony-self-run/deep-swe
git -C ~/parsimony-self-run/deep-swe checkout 0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea
nohup python examples/self-run/run.py ~/parsimony-self-run/deep-swe --scratch ~/parsimony-self-run \
  > ~/parsimony-self-run/run.log 2>&1 &
```

Runs are resumable: finished items are skipped. Usage-limit errors pause that harness for 30
minutes and retry the same item; they are never recorded as results. Each finished item writes
`runs/<config>/<task>__<attempt>/patch.diff` and `meta.json`; transcripts stay in the scratch
directory.

## Grading (2026-10-12)

`grade.py` grades every diff with the task's own DeepSWE verifier (`tests/test.sh`, hidden tests,
pass only if every new and existing listed test passes), offline, with `task.toml`'s CPU and memory
limits. DeepSWE's task images are amd64-only, so they are rebuilt natively for arm64 from each task's
`environment/Dockerfile`; the one change is a pin `llvmlite==0.46.0` for numba, whose Dockerfile
installs the latest llvmlite but patches numba for 0.46.0 (recorded in each `grade.json`). Before
grading, every task's reference solution passed and every unpatched base failed in these images.

A test suite that hangs is an unknown outcome (`timeout`), like DeepSWE's errored runs: not solved,
still measured. Five hangs ran to DeepSWE's 30-minute limit; the last two items used a 5-minute cap
(the reference suites finish in under 3 minutes), recorded as `timeout_sec`. All seven are gql or
kombu attempts.

```sh
python examples/self-run/grade.py ~/parsimony-self-run/deep-swe --scratch ~/parsimony-self-run --build
python examples/self-run/grade.py ~/parsimony-self-run/deep-swe --scratch ~/parsimony-self-run --reference
python examples/self-run/grade.py ~/parsimony-self-run/deep-swe --scratch ~/parsimony-self-run
python examples/self-run/grade.py --apply   # copy outcomes into results/*.jsonl
```

| Configuration | Solved | Timeouts | Net units added, solved (mean) | Net units added (mean) |
|---|---:|---:|---:|---:|
| Claude Haiku 5.5 (high) | 9/20 | 0 | 1,501 | 1,449 |
| Claude Opus 5.5 (high) | 6/10 | 1 | 2,137 | 1,949 |
| Claude Sonnet 5.5 (high) | 6/10 | 1 | 1,974 | 1,779 |
| GPT-5.6 Sol (high) | 4/10 | 1 | 1,660 | 1,725 |
| GPT-6.1 Sol (high) · Codex | 13/20 | 0 | 1,255 | 1,348 |
| GPT-6.1 Sol (high) · pi | 10/20 | 0 | 1,356 | 1,395 |
| GPT-6 Astra (high) · Codex | 3/10 (4 run) | 0 | 1,109 | 1,179 |
| GPT-6 Astra (high) · pi | 6/10 | 1 | 1,327 | 1,326 |
| GPT-6 Luna (high) · Codex | 4/20 | 0 | 901 | 1,025 |
| GPT-6 Luna (high) · pi | 3/20 | 0 | 1,076 | 857 |
| GPT-6 Sol (high) · Codex | 10/20 | 0 | 1,160 | 1,226 |
| GPT-6 Sol (high) · pi | 7/20 | 3 | 1,354 | 1,116 |

Codex GPT-6 Astra is paused at 4 of its 10 planned attempts (owner request, 2026-10-16, to save Codex usage);
the 6 unrun attempts count as not solved, so its Solved is a floor.

On the site, graded self-runs also appear in the default Solved-only view, still faded and unranked.

## Anchor check (2026-10-09)

GPT-5.6 Sol ran self-run (pi, high effort) on the first 5 tasks × 2 attempts. Its mean net units
added was **1,725** versus **1,969** for the published DeepSWE runs of GPT-5.6 Sol (mini-SWE-agent,
max effort) on the same 5 tasks × 4 attempts: a ratio of about **0.88**. Per task the self-run
attempts fall inside or slightly below the published range, except tomlkit (2,690–2,703 versus
3,251–3,556). The self-run setup therefore appears to shrink footprints modestly, not to explain the
much smaller GPT-6 Luna footprint (931 on the same 5 tasks). One anchor on 5 tasks is weak evidence;
the effort level also differs. The Claude Sonnet 5 anchor has not been run.
