# SWE-bench Pro V2 and SWE-Atlas Refactoring artifact audit

Audit performed 2026-09-29; request timestamps in UTC. This was a read-only discovery audit using pinned public GitHub content and anonymous public S3 HTTP requests. No credentials, model APIs, evaluations, target-code execution, upstream contacts, or modifications to upstream sources were used. Machine-readable request evidence and checksums: [`examples/benchmark-discovery/pro-atlas-artifact-audit.json`](../examples/benchmark-discovery/pro-atlas-artifact-audit.json).

## Findings

### SWE-bench Pro: V2 artifacts blocked; public legacy artifacts are not V2

The pinned [Pro repository](https://github.com/scaleapi/SWE-bench_Pro-os/tree/66f92766bba642462d4bbe5479e83f91f9211862) distinguishes V2 (642 tasks) from the original v1 (731 tasks; HF config `v1` / tag `v1.0`). The V2 README describes public task/verifier/reference-solution material and instructs how new agent runs capture `model.patch` and are authoritatively re-graded. Those instructions are not a historical V2 model-run export. Gold solutions are references, not model submissions.

Contrary to the older investigation's untested-access assumption, the S3 endpoint is anonymously readable: bucket listing request returned HTTP 200 without credentials. The full `swe-bench-pro/` delimiter listing was 1,988 bytes (SHA-256 `a7debe7b00e996b8502b61fdd4bec00da9ee23f1d59b840eec826fbf85e93670`), not truncated, and exposed 15 historical run prefixes. No prefix was identified as a V2 run. The pinned trajectory README calls this the legacy trajectory store and describes those runs as dated leaderboard/paper outputs. Its key names do not independently certify task version, so this is evidence of accessible legacy artifacts, not proof that no separately hosted V2 export exists.

Confirmed example: legacy `claude-45sonnet-10132025` exposes a 77,642-byte `_patch.diff` (SHA-256 `11eb99ed2d27ec103e42e6e2b8e7d40d5f56728df0919bd83cf9f19c5591500c`) and `_output.json` (81 bytes; SHA-256 `2f6451a37971058b4275f2c9e53e28a27cf31bcbe9b27da250bfeebc68d65ed9`) for NodeBB task ID `NodeBB-00c70ce7b0541cfc94afe567921d7668cdc8f4ac`. The explicit output says a before-all hook is `FAILED`. This verifies a public patch and a task-level failure for that legacy attempt only; it does not establish the V2 task mapping or authoritative V2 result. Do not import or relabel it as V2.

**Disposition:** no public V2 model-patch + explicit per-task outcome/failure export was located in the pinned repository or the anonymous S3 run-prefix inventory. V2 is blocked for historical model-run import. Keep V2 gold patches and all legacy model attempts separate; do not implement an importer on this evidence.

### SWE-Atlas Refactoring: public gold patches, no public model attempts

Pinned `scaleapi/SWE-Atlas` at commit `49e4af3b6c803dd54a1cd60ead703aac25de4e21` (current `main` when audited). Its complete, non-truncated Git tree contains 70 `data/rf/` task directories and 91 `data/tw/` task directories. Inspection found task data, verifier assets and gold patches, but no model result/patch paths or per-attempt export. The project README links to aggregate leaderboards; aggregate scores do not provide task-by-task status, final model diffs, or explicit failures. No Atlas anonymous S3 result endpoint was identified in these public repository sources.

At pinned task `69391d8d1ce51c407be1e531`, public config identifies `trufflesecurity_trufflehog`, base `5568b2e0a686cc4d838bddc095b831379143e61b`, Go. Its `solution/gold.patch` is available (29,560 bytes; SHA-256 `056ad7b55002b2c86a459d9668b6817ceb1f74413bf5da2e41df7b6ccdc51588`) and explicitly is a gold/reference patch, never a model attempt or failure record. Keep Refactoring distinct from Test Writing and QnA.

**Disposition:** no public per-model/per-task final patches or explicit per-task outcomes/failures located. Historical Atlas model-run import is blocked; do not synthesize failures from missing outputs or import gold patches as model submissions.

### Provenance and reuse

The pinned Atlas repo includes an Apache-2.0 license (LICENSE SHA-256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`). That does not establish rights for third-party source repositories represented by tasks, nor model-output redistribution rights. Pro source/project and output terms likewise require separate review; public S3 access is not itself a license. No comprehensive license audit of task repositories was performed. Attribution, project-specific licenses, model-output terms, and redistribution permission remain gates before storing or publishing imported data.

## Request evidence / exact commands

All requests used anonymous HTTP via Python `urllib` with `User-Agent: Parsimony-artifact-audit/1.0`; GitHub API requests also used `Accept: application/vnd.github+json`. Request results/checksums are captured in the JSON evidence file. The audit timestamp was `2026-09-29T20:00:18Z`.

Relevant request URLs:

- `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md` — 200, 6,858 bytes, SHA-256 `dde4168fed17ca1ea00b26a93aca78dad43c7b3f981b93a2872428259428231f`.
- `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/traj/README.md` — 200, 1,091 bytes, SHA-256 `41520a962d15cb82e15d66adc18a18a0f973ae4542ef5c5d1e29e2fdec864d04`.
- `https://scaleapi-results.s3.amazonaws.com/?prefix=swe-bench-pro%2F&delimiter=%2F` — 200, 1,988 bytes, SHA-256 above; 15 prefixes, not truncated.
- `https://api.github.com/repos/scaleapi/SWE-Atlas/git/trees/49e4af3b6c803dd54a1cd60ead703aac25de4e21?recursive=1` — 200, 5,670 entries, not truncated (raw response SHA-256 `3b9930c1c3a10d3e73d8d7cdd790b22206e9f0df956b2b6e52ff963deb160da9`).
- Pinned Atlas config and gold patch URLs and their response checksums are in the JSON evidence.

Reproduction: GET the listed URLs without an `Authorization` header, hash raw response bytes with SHA-256, and for the S3 root parse the XML `CommonPrefixes`. To verify the legacy example, GET the exact `_patch.diff` and `_output.json` URLs recorded in the JSON; do not fetch/run trajectories or execute the patch. To recount Atlas task folders, inspect first-level directory names under `data/rf/` and `data/tw/` in the pinned recursive Git tree.

No request here proves that a private or separately hosted run export does not exist. Closure applies only to the inspected public sources. No speculative importer or workaround evaluation is recommended; reopening requires a public, version-identifiable export with model/agent/config, task/base provenance, patches, and explicit outcomes including failures, plus reuse terms.
