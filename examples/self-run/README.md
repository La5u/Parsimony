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
companies use different harnesses: compare within a company, not across. GPT-5.6 Sol and Claude
Sonnet 5 also run as anchors, since they are on the published DeepSWE board; their gap shows the
effect of the harness and environment.

Differences from DeepSWE, all identical across self-run configurations:

- Agent harness: pi or Claude Code instead of mini-SWE-agent.
- Environment: host Python 3.14 in a bubblewrap sandbox with the repository at its base commit
  only (no later history, no remote). No task Docker image, no project dependencies.
- Network is not blocked, because the harness calls its API. The prompt forbids network use;
  `meta.json` lists any shell commands that look like network use.
- Outcomes are **not graded** (`outcome: not_graded`). Footprint is measured from the final diff
  exactly like published patches.

The sandbox can write only the task directory and the harness credential store. It hides the
DeepSWE checkout (reference solutions), this repository, the download cache and agent transcripts.

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
