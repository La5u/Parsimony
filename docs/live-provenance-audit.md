# SWE-bench Live provenance audit

Investigation date: 2026-09-29. Bounded source audit only: no submitted patch, model, target repository, or test suite was executed. This is provenance research, not authorization to score or redistribute artifacts.

## Finding

The public Hugging Face API confirms both IDs in the earlier investigation, with different meanings:

- [`SWE-bench-Live/MultiLang`](https://huggingface.co/api/datasets/SWE-bench-Live/MultiLang) is the multilingual corpus. Its configuration has separate `c`, `cpp`, `go`, `js`, `rust`, `java`, `ts`, and `cs` language splits.
- [`SWE-bench-Live/SWE-bench-Live`](https://huggingface.co/api/datasets/SWE-bench-Live/SWE-bench-Live) is the distinct original SWE-bench-style dataset with `test`, `lite`, `verified`, and `full` splits. It is **not** the matching source for the multilingual submission cohort.

The best historical candidate for the pinned run is MultiLang revision [`62dc0745c40f067fc366ae3eb1a26136e5928f85`](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/62dc0745c40f067fc366ae3eb1a26136e5928f85), whose HF history labels it “Upload dataset” on 2026-08-20. It postdates the submitted trajectories (May–June 2026) and predates the pinned submission commit (2026-09-29); it therefore cannot be assumed to be the run's original input. Initial dataset-server queries found all 230 IDs, but their `revision` query parameter does not establish immutable row provenance. A subsequent direct read of all eight Parquet files through `resolve/62dc…/` URLs independently confirmed all 230 IDs; none were missing. Exact immutable-file checksums are recorded in [`live-immutable-audit.json`](../examples/benchmark-discovery/live-immutable-audit.json). The four spot-checked task `base_commit` values also exactly match the “Resetting repository testbed to commit …” lines in their raw trajectories (examples below). The cohort is therefore supported as a 230-ID subset of this immutable candidate snapshot, with direct base-revision corroboration for the examples.

**Caveat / provenance status:** the submission's pinned README and configuration do not name a Hugging Face revision or parquet path. Thus this audit did not find an explicit run manifest proving that revision `62dc…` was the source actually loaded by the run. The historical run-to-dataset binding remains **unknown**, not proven; complete ID membership and sampled base-commit agreement make `62dc…` a corroborated metadata candidate, not a declared run input. Its date is later than the trajectories and does not establish historical input provenance. Do not treat a later current `main` SHA or the distinct `SWE-bench-Live/SWE-bench-Live` dataset as equivalent evidence.

## Immutable dataset record

- Repository: `SWE-bench-Live/MultiLang`
- Candidate revision SHA: `62dc0745c40f067fc366ae3eb1a26136e5928f85`
- Revision record: [HF revision](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/62dc0745c40f067fc366ae3eb1a26136e5928f85) / [HF commits API](https://huggingface.co/api/datasets/SWE-bench-Live/MultiLang/commits/main)
- Dataset README at that revision: [README.md](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/resolve/62dc0745c40f067fc366ae3eb1a26136e5928f85/README.md)
- Format: Parquet. Config `default`, one file per language split:
  - `data/c-00000-of-00001.parquet`
  - `data/cpp-00000-of-00001.parquet`
  - `data/go-00000-of-00001.parquet`
  - `data/js-00000-of-00001.parquet`
  - `data/rust-00000-of-00001.parquet`
  - `data/java-00000-of-00001.parquet`
  - `data/ts-00000-of-00001.parquet`
  - `data/cs-00000-of-00001.parquet`
- Relevant task metadata fields include `instance_id`, `repo`, `base_commit`, `patch`, `test_patch`, `commit_url(s)`, and test commands. README identifies each split as a language task set.
- Exact files for the Go and JavaScript examples below: `data/go-00000-of-00001.parquet` and `data/js-00000-of-00001.parquet`.

For contrast, the other public API ID currently exposes `data/202401-00000-of-00001.parquet` through `data/202505-00000-of-00001.parquet`, plus `data/test-00000-of-00001.parquet`, `data/lite-00000-of-00001.parquet`, `data/verified-00000-of-00001.parquet`, and two `full` shards. Its API identifies the dataset formats/splits; it does not establish provenance for this MultiLang run.

## Submission evidence and supported-language examples

Pinned artifact root: [GPT-5.5 medium configuration at submission `cba8a6d3197cd53da09f8527cccbc689782302a6`](https://github.com/SWE-bench-Live/submission/tree/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium). Its [`result.json`](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/result.json) declares 230 submitted IDs, 105 success IDs, 120 failure IDs, and five empty-patch IDs. Empty patch is an independent artifact category; do not merge it into success/failure without the run's evaluation semantics.

The following pairs use the result file's explicit success/failure lists. Each immutable HF row's repository and base revision agrees with the trajectory's recorded testbed reset. Links point to the actual patch and trajectory in the pinned submission commit; the HF row links pin its dataset revision.

| Language / result | Task | Dataset `repo` / `base_commit` | Patch | Trajectory / base evidence | Dataset row |
|---|---|---|---|---|---|
| Go success | `twpayne__chezmoi-5016` | `twpayne/chezmoi` / `5ffd82cb395bc0c33ad885234a72bef108f8243c` | [patch.diff](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/twpayne__chezmoi-5016/patch.diff) | [trajectory.txt](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/twpayne__chezmoi-5016/trajectory.txt) | [pinned row lookup (offset 70)](https://datasets-server.huggingface.co/rows?dataset=SWE-bench-Live%2FMultiLang&config=default&split=go&offset=70&length=1&revision=62dc0745c40f067fc366ae3eb1a26136e5928f85) |
| Go failure | `kubernetes-sigs__controller-runtime-3494` | `kubernetes-sigs/controller-runtime` / `885e77d7d9fc1a010362c5fae19cda13e64f3ae8` | [patch.diff](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/kubernetes-sigs__controller-runtime-3494/patch.diff) | [trajectory.txt](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/kubernetes-sigs__controller-runtime-3494/trajectory.txt) | [pinned row lookup (offset 69)](https://datasets-server.huggingface.co/rows?dataset=SWE-bench-Live%2FMultiLang&config=default&split=go&offset=69&length=1&revision=62dc0745c40f067fc366ae3eb1a26136e5928f85) |
| JavaScript success | `codeceptjs__CodeceptJS-5106` | `codeceptjs/CodeceptJS` / `5535d166535183c9766319081237342a140998d9` | [patch.diff](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/codeceptjs__CodeceptJS-5106/patch.diff) | [trajectory.txt](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/codeceptjs__CodeceptJS-5106/trajectory.txt) | [pinned row lookup (offset 11)](https://datasets-server.huggingface.co/rows?dataset=SWE-bench-Live%2FMultiLang&config=default&split=js&offset=11&length=1&revision=62dc0745c40f067fc366ae3eb1a26136e5928f85) |
| JavaScript failure | `sveltejs__svelte-16666` | `sveltejs/svelte` / `e883cd086bd5f93b086220c7f2e2304bcb958eb8` | [patch.diff](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/sveltejs__svelte-16666/patch.diff) | [trajectory.txt](https://github.com/SWE-bench-Live/submission/blob/cba8a6d3197cd53da09f8527cccbc689782302a6/submissions/multilang/all_languages/sweagent/gpt-5.5-medium/sveltejs__svelte-16666/trajectory.txt) | [pinned row lookup (offset 2)](https://datasets-server.huggingface.co/rows?dataset=SWE-bench-Live%2FMultiLang&config=default&split=js&offset=2&length=1&revision=62dc0745c40f067fc366ae3eb1a26136e5928f85) |

The HF row links are navigation aids only: dataset-server `revision` parameters may be ignored, so they are not immutable evidence. The orchestrator subsequently verified the four rows by downloading the exact SHA-resolved Go/JS Parquet files and matching base hashes against the pinned raw trajectories; see `live-immutable-audit.json`. Rows contain no language field: language must come from the documented split/file mapping. The audit did not execute dataset commands or patches.

The result classification is source-reported only; this work did not re-run evaluation to independently validate it. All four patch files are present at the pinned submission paths. The candidate snapshot's `base_commit` field matched all four trajectory reset lines exactly. No claim is made here about compatibility with a Parsimony analyzer.

## Revision trajectory and selection

The HF MultiLang commit history records `62dc…` (“Upload dataset”, 2026-08-20), followed by later data uploads and README edits; its present `main` resolves to `3638632e8153a10ca422c1022bed79023084b5c9` (README-only update dated 2026-09-20). The immutable August dataset revision is a pre-submission snapshot, but later than the recorded May–June trajectories; it is not proven to preserve the exact run input. The pinned GitHub submission commit is dated 2026-09-29. This timeline rules out treating a mutable current default as an adequate historical pin, but does not itself document which snapshot the run loaded.

## Licensing, terms, and reuse gate

- MultiLang README front matter declares `license: mit`; HF API also tags the dataset MIT. The inspected pinned README contains no separate terms authorizing redistribution of underlying source code, issue text, patches, trajectories, or other third-party material. A `LICENSE` file at this revision was not present (resolve returned 404).
- The submission README says the repository hosts results, trajectories, and evaluation logs; requires raw rollout trajectories (or representative samples under stated conditions) to verify protocol compliance. The pinned repository has no root `LICENSE` file (404), and its README does not grant a license or artifact reuse/redistribution rights.
- MIT metadata should be retained with attribution for the dataset's own covered material; it is not proof that every embedded repository patch, issue statement, trajectory, model output, or other contributor work can be redistributed under MIT. No blanket permission for reuse of submission artifacts was located. Review upstream project licenses and obtain/confirm rights for the specific artifacts and intended use before retaining or publishing them. Public unauthenticated download is not a reuse grant.

## Audit limits / disposition

The immutable candidate has complete submitted-ID membership (230/230) and four corroborated Go/JS base revisions, supporting a strong candidate cohort link. Explicit declaration by the run of this dataset revision remains unknown. A complete per-task base-commit comparison across all 230 trajectories was not performed. Preserve failure/empty/unavailable distinctions and all source checksums if proceeding. No patches/models/targets/tests were run; no scoring or redistribution is authorized by this audit.
