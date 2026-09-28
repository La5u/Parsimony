# SWE-Atlas import investigation (Refactoring + Test Writing)

## Executive recommendation

**Do not treat the public leaderboard as a source of importable model patches.** The public GitHub repo does provide task definitions, base commits, verifier materials, and *gold/reference* patches; I found no published run-result bundle containing model final patches or per-attempt transcripts. The leaderboard presents aggregate model scores, not task-by-task attempts. Parsimony can reuse the benchmark as an explicitly partial task/patch corpus only if we obtain run artifacts from Scale or model submitters, or retrieve them from a separately published results archive. Importing gold patches as model outputs would be incorrect.

A small discovery spike is reasonable: parse the task `config.json`, pin the SWE-Atlas commit, resolve task `repo` + `base_commit`, and assess whether a permitted gold patch imports cleanly. Keep RF and Test Writing as separate task types and keep benchmark success labels distinct from Parsimony measurements.

## Scope and evidence status

**Verified by direct inspection:** GitHub public repository README, recursive Git tree and selected raw task/config files; live Refactoring leaderboard page. Links below are the source of truth and can change. **Not verified:** availability of non-public Scale run storage, whether individual teams will share artifacts, legal status of upstream repository snapshots beyond their own licenses, or the provenance of leaderboard rows beyond what the page says.

- Official repo: <https://github.com/scaleapi/SWE-Atlas>
- Current repo tree: <https://github.com/scaleapi/SWE-Atlas/tree/main>
- Refactoring leaderboard: <https://labs.scale.com/leaderboard/sweatlas-refactoring>
- Test Writing leaderboard: <https://labs.scale.com/leaderboard/sweatlas-tw>
- README: <https://raw.githubusercontent.com/scaleapi/SWE-Atlas/main/README.md>
- Relevant RF run setup: <https://github.com/scaleapi/SWE-Atlas/tree/main/run_config/rf>
- Relevant TW run setup: <https://github.com/scaleapi/SWE-Atlas/tree/main/run_config/tw>

## Public model coverage (Refactoring)

**Verified leaderboard rows visible when inspected** (score and uncertainty as displayed; score is the leaderboard's aggregate score, not an assertion that this is a resolve percentage). The page describes model/agent combinations, so agent harness is part of each label.

| Displayed model/agent | Score ± |
|---|---:|
| GPT 6 Astra (Codex), xHigh | 59.05 ± 6.43 |
| Fable-5.1 (Claude Code), xHigh | 56.67 ± 6.52 |
| Fable-5 (Claude Code), xHigh | 54.76 ± 6.76 |
| Opus-4.7 (Claude Code) | 48.57 ± 6.73 |
| Opus 4.8 (Claude Code) | 46.67 ± 6.75 |
| GPT-5.5 (Codex), xHigh | 44.79 ± 6.76 |
| Gemini 3.8 Flash (Mini-SWE-Agent) | 44.76 ± 6.76 |
| GPT 5.4 (Codex), xHigh | 44.29 ± 6.76 |
| GLM 5.2 (Mini-SWE-Agent) | 42.38 ± 6.76 |
| GPT 5.3 (Codex), xHigh | 42.38 ± 6.76 |
| Opus-4.6 (Claude Code) | 35.58 ± 6.82 |
| Gemini-3.1-Pro (Gemini CLI) | 33.81 ± 6.64 |
| Sonnet-4.6 (Claude Code) | 32.21 ± 6.77 |
| Glm-5 (Mini-SWE-Agent) | 24.24 ± 6.27 |
| Kimi-K2.5 (Mini-SWE-Agent) | 20.95 ± 6.00 |
| Minimax-M2.5 (Mini-SWE-Agent) | 19.52 ± 5.89 |
| Gemini-3-Flash (Mini-SWE-Agent) | 10.00 ± 4.80 |

The page also says Opus-family results over time are from a random subset of 30 tasks; do not infer that every row used every task, identical attempt count, or same harness. It refers to evaluation of `claude-code`, Codex, Gemini CLI, and Mini-SWE-Agent. The repo's own RF run script is a reproducible *rerun* setup, not a download of those leaderboard runs.

**Test Writing:** the README identifies Test Writing as a separate SWE-Atlas benchmark and the repo has a `data/tw/` task corpus (91 task directories in the inspected `main` tree), plus `run_config/tw/`. I did not transcribe TW model leaderboard rows in this bounded RF-focused investigation; check the current TW page directly before any coverage claim. The RF results/patches must not be represented as TW evidence.

## What can be downloaded; base revisions

- The GitHub repo contains the task data in `data/rf/` and `data/tw/`, not only documentation. The inspected tree had 70 RF task directories and 91 TW task directories. Each RF task contains an `instruction.md`, a task config, test/evaluation files and frequently `solution/gold.patch` + `solution/solve.sh`. The README describes the repo as hosting the benchmark data and run instructions.
- Example RF task: [task directory](https://github.com/scaleapi/SWE-Atlas/tree/main/data/rf/task-69391d8d1ce51c407be1e531), [config](https://raw.githubusercontent.com/scaleapi/SWE-Atlas/main/data/rf/task-69391d8d1ce51c407be1e531/tests/config.json), [gold patch](https://raw.githubusercontent.com/scaleapi/SWE-Atlas/main/data/rf/task-69391d8d1ce51c407be1e531/solution/gold.patch). Config identifies repo `trufflesecurity_trufflehog`, base commit `5568b2e0a686cc4d838bddc095b831379143e61b`, language Go. The gold patch is explicitly a reference, not a public model final patch.
- In the same task, `solution/solve.sh` applies `/solution/gold.patch`; `tests/config.json` contains `task_id`, repo, base commit and language. This is a straightforward recipe to recover the base checkout and apply the gold patch. Per-task task configs set long verifier/agent timeouts and an allowlisted package/toolchain network policy.
- RF assets in public tree total about 11.5 MB; TW about 6.5 MB at the inspected revision. Raw files are downloadable via GitHub, and the full tree can be pinned to a commit. Do not confuse repo `main` (dataset revision) with the repository-under-test base commit recorded in each task config.
- `run_config/rf/opus-4p6_claude-code.sh` runs Harbor with Opus 4.6, `-k 3`, `-n 24`, Modal, high reasoning effort and WebSearch/WebFetch disabled, writing to `results/rf/`. Those result artifacts are generated by running the models; they are not present as public historical results in the repository tree.

## Outcomes, failures, and harness comparability

**Not available in inspected public artifacts:** no per-model/per-task success matrix, attempt-level failure rows, final patch archive, agent transcripts, or run metadata bundle was found in the public repo. The leaderboard is aggregate only. Therefore we cannot recover the requested historical outcome/failure coverage by downloading repo `main`, and cannot distinguish a missing task artifact from a failed run. Do not synthesize failed outcomes from absent patches.

The leaderboard's explanatory text describes a two-part RF evaluation: test execution and an LLM judge (the page names Claude Opus 4.5) grading a set of must-have/nice-to-have rubric claims. A task resolves when tests pass and every must-have rubric passes; test-file modifications trigger automatic failure. The page discusses common misses such as incomplete extraction, stale implementations, missed call sites/imports and stale documentation. These are benchmark-defined outcomes and should not be mapped directly to Parsimony's patch-size/structural measurements.

The benchmark's own launcher uses Harbor and the repo documents a particular setup, but model rows span different agents (Claude Code, Codex, Gemini CLI, Mini-SWE-Agent), effort settings and likely different execution histories. The `opus-4p6` script specifies `-k 3`, while leaderboard page rows do not expose per-attempt records. Consequently:

1. Scores are useful as public context, **not harness-matched labels** for Parsimony.
2. Existing model patch import requires the raw patch and task/base provenance for each attempt, neither of which is evidenced in the repo/page.
3. Re-running a selected model in Harbor would answer a new experiment, contrary to this task's requirement to import existing public runs.
4. RF vs TW evaluators differ materially: RF is refactoring + rubric/test preservation; TW creates tests and uses its own evaluation. They need different provenance and outcome schema.

## Licensing and technical blockers

- **Verified:** SWE-Atlas repo root has an Apache License 2.0 license file: <https://github.com/scaleapi/SWE-Atlas/blob/main/LICENSE>. That permits reuse subject to its terms, including retaining license/attribution notices and marking modified files as appropriate.
- **Caution:** the benchmark data references third-party codebases. Their source licenses remain independently relevant; Apache-2.0 on the SWE-Atlas repo is not evidence that each upstream repository's source or patch is relicensed under Apache. Review source-project licenses before redistributing snapshots or derived full-file contents.
- Model-output rights/terms and redistribution permission are **unverified** from the public repo/page. Even if submitted patches are obtainable, check model provider and submitter terms before storing or publishing them.
- **Technical blocker:** per-attempt patches/results are absent from public inspected sources. A patch-only parser cannot reconstruct a final full tree without exact base commit and path handling; an absent artifact is not an empty patch or failure.
- Task execution relies on Harbor/Modal, Docker images and an external LLM judge API. Reproducing official pass/fail outcomes may require unavailable credentials/services, fixed image digests, and precise evaluator/version/config pins. Parsimony should not invoke these as part of an import-only pipeline.

## Recommended next steps

1. Ask Scale or the named submitters for an export containing at minimum `(benchmark revision, task_id, model/agent/config, attempt index, repo, base_commit, final patch, exit/status, test result, must-have rubric result, failure category)`, plus raw outputs and hashes where permitted. Specifically request failed/partial attempts and state whether `-k`/retries are included.
2. Before data import, pin the SWE-Atlas Git commit and evaluate licensing for SWE-Atlas data, individual upstream base repos, and model artifacts. Keep source URLs, license identifiers, checksums and access date with each imported record.
3. If exports are granted, ingest patches only as **existing attempts** with separate `attempt_status` and `artifact_present` fields. Store absent, infrastructure failure, patch-emission failure, verifier failure, and benchmark rejection distinctly; never turn missing patch into an empty patch.
4. Initially pilot one or two RF tasks and one TW task after artifact access is confirmed. Keep benchmark rubric/test success as a separate source label; run Parsimony measurements offline on the imported final patch/base pair only. Do not claim cross-harness comparability or general leaderboard reproduction.
5. If access to run artifacts is not forthcoming, close the historical-run import as **blocked**. A separately authorized import of gold/reference patches may be useful for analyzer validation, but it is not model coverage and should be labeled accordingly.
