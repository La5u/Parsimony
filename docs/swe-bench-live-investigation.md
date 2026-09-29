# SWE-bench Live existing-run importer

Investigation: 2026-09-29. **Audit/pilot tooling, not a published benchmark release.** No models, submitted code, target tests, or dataset commands are executed. The analyzer only strictly applies patches and parses source offline.

## Implemented path

`python -m parsimony.live` inventories one configuration at a full GitHub commit against one or more files at a full Hugging Face commit. It checks the HF resolved SHA and records exact file-byte checksums plus an aggregate manifest checksum. JSON, JSONL/NDJSON, CSV and Parquet are supported; Parquet requires optional `pyarrow`, imported lazily (not required for ordinary Parsimony use).

Repeat `--dataset-file LANGUAGE=PATH` for language splits. Actual MultiLang Parquet rows have **no language field**; explicit mappings from its pinned README are required. Known aliases normalize Go/Python/JS/TS labels; mixed `TS/JS` and unsupported languages remain inventory-only, never inferred from a patch. Conflicting language assignments and duplicate task IDs fail closed.

```sh
# Install optional pyarrow into an external environment if using Parquet.
# MultiLang has eight files; the loop supplies all of them, not a single split.
FILES=()
for split in c cpp go js rust java ts cs; do
  FILES+=(--dataset-file "$split=data/$split-00000-of-00001.parquet")
done
python -m parsimony.live --cache /tmp/live-cache \
  --submission-revision cba8a6d3197cd53da09f8527cccbc689782302a6 \
  --config-path submissions/multilang/all_languages/sweagent/gpt-5.5-medium \
  --dataset SWE-bench-Live/MultiLang \
  --dataset-revision 62dc0745c40f067fc366ae3eb1a26136e5928f85 \
  "${FILES[@]}" \
  --task-id twpayne__chezmoi-5016 \
  --task-id kubernetes-sigs__controller-runtime-3494 \
  --task-id codeceptjs__CodeceptJS-5106 \
  --task-id sveltejs__svelte-16666 --output /tmp/live-inventory.json
```

The candidate dataset revision in this example is **not proven to be the historical run input**. Inventory is permissible evidence gathering, not authorization to score. `--task-id` limits patch downloads only; every submitted record stays in the inventory, with unrequested artifacts marked `not_selected`. Missing and empty patches, explicit failures, errors, incomplete runs and unknown outcomes remain distinct. Empty-only IDs do not become failures. The larger dataset's unsubmitted-task count is disclosed.

`analyze_run()` uses the standard benchmark record schema and a single supported language track. It requires an evidence-bound reviewed manifest (URL, digest, matching dataset/result checksums and submission revision), plus either verified historical dataset matching or independent base-commit confirmation for every potentially measured task. This gate records a review, not a cryptographic proof of its truth. Do not set it merely because a supplied SHA exists. Analyze from a clean committed analyzer checkout; no paid model calls or target-code execution are needed.

## Evidence and outstanding gates

- Submission commit `cba8a6d3197cd53da09f8527cccbc689782302a6` exposes `result.json` and task-level `patch.diff` / `trajectory.txt`. GPT-5.5 medium declares 230 submitted IDs: 105 successes, 120 failures and five empty-only IDs; errors/incomplete counts are zero.
- Both documented HF IDs are public: `SWE-bench-Live/MultiLang` and the separate Python `SWE-bench-Live/SWE-bench-Live`. A prior guessed ID's HTTP 401 was not evidence that these are inaccessible.
- Direct immutable Parquet reads confirmed all 230 submitted IDs in candidate MultiLang revision `62dc0745…`, with four Go/JS bases independently corroborated against raw trajectories. See [provenance audit](live-provenance-audit.md) and [immutable-file evidence](../examples/benchmark-discovery/live-immutable-audit.json). Dataset-server `revision` query parameters alone are not reliable pinning evidence.
- The candidate upload is August 2026, **later** than May–June trajectories. No explicit run manifest naming its dataset revision was found. Four corroborated bases do not establish full-cohort historical revision/selection semantics.
- Dataset metadata declares MIT, but the submission repository has no inspected root license or blanket artifact redistribution grant. Third-party source and artifact rights need separate review. No raw patches/trajectories are added to this repository by this investigation.

Before any board: finish full-cohort base/revision and retry/selection audits; establish artifact reuse/attribution terms; freeze a supported-language population independently of outcomes; measure from a clean analyzer revision; audit missingness and scope; then build a separate panel, scores, uncertainty and page. Do not merge this source into current boards or change their 80/20 formula.
