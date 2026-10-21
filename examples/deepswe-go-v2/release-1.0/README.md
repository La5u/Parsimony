# DeepSWE Go: release 1.0 runs

The Go board's v1.1 records live in the checksum-bound release asset described in [../README.md](../README.md), which stays unchanged. This folder adds the release 1.0 runs beside it: `scripts/rebuild-site.sh` copies them next to the downloaded asset and uses this folder's `sensitivity.json`. `coverage.json`, `scores.json` and `sensitivity.json`/`.md` here cover all 38 configurations.

## DeepSWE release 1.0 runs (added 2026-10-21)

12 more configurations come from DeepSWE's own archive of **release 1.0** (gated Hugging Face dataset [`datacurve/deep-swe-leaderboard` at `0618ccd`](https://huggingface.co/datasets/datacurve/deep-swe-leaderboard/tree/0618ccdd613e1f0043604f8f4474321e7fe12e29), CC-BY-4.0; access asks you to share your Hugging Face username and email), for models absent from v1.1: Claude Haiku 4.5, Claude Opus 4.6 (max), Claude Opus 4.7 (max), Gemini 3 Flash Preview, GLM-5.1, GPT-5.4 mini (xhigh), Grok Build 0.1, Kimi K2.6, MiMo V2.5 Pro, MiniMax M2.7, MiniMax M3 and Qwen3.6 Plus. Files `v1_0_*.jsonl` in this folder; names end in "· DeepSWE 1.0".

- Same 113 task IDs and base commits as v1.1, and the same mini-SWE-agent harness. v1.1 re-ran every model and rewrote every verifier. On the nine setups present in both releases, pass rates agree within a few points, and per-task differences match chance except on four tasks (`narwhals-rolling-window-suite`, `vulture-persistent-analysis-cache`, `skrub-duration-encoding`, `claude-code-by-agents-recursive-delegation`). Release 1.0 outcomes on those four tasks are recorded as unknown, never as pass or fail.
- Measured at the Go board's analyzer commit `34d59ca` (`tree-sitter-go-units-v2`) with Python 3.14.7, so units are comparable; the frozen panel is unchanged and the new runs are scored against it. Coverage, scores and stability were regenerated with the current scoring code (existing models' archived scores differ only in the last floating-point digit).
- Driver: [`examples/benchmark-discovery/add-deepswe-1.0.py`](../../benchmark-discovery/add-deepswe-1.0.py).
- A model is ranked only with at least 15 shared solved tasks (or half the board's tasks if fewer); otherwise it is listed after the ranked models.
