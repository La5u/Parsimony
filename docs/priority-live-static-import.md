# Priority Live static import

This is a **touched-file compatibility audit**, not certification of a historical
checkout, dataset/evaluator match, model identity, harness homogeneity, temporal
isolation, or grading correctness. Public outcomes remain submitter-reported.

## Full source-population audit

Pinned submission revision: `cba8a6d3197cd53da09f8527cccbc689782302a6`.
Python candidate dataset revision: `b51a86422e10cfd403beb4773e5a2947953e36ec`.
MultiLang candidate revision: `62dc0745c40f067fc366ae3eb1a26136e5928f85`.

| Configuration | Population | Old blobs + strict hunks | New-file-only | Not required | Unverified |
|---|---:|---:|---:|---:|---:|
| DeepSeek V4.1 Flash / TianxiCode 0.1.423 | 300 | 295 | 0 | 0 | 5 |
| GPT-5.6 Sol / Slingshot 3.4.0, Python | 300 | 296 | 0 | 0 | 4 |
| Claude Opus 4.8 / AiWork.Code | 300 | 290 | 1 | 8 | 1 |
| GPT-5.6 Sol / Slingshot 3.4.0, JavaScript | 108 | 104 | 1 | 3 | 0 |
| GPT-5.6 Sol / Slingshot 3.4.0, TypeScript | 111 | 109 | 0 | 1 | 1 |

The audit checks complete raw file bytes against the submitted patch's old Git
blob prefix (minimum seven hex digits), then applies every text hunk strictly.
A prefix match is not a full cryptographic old-object identification; both
prefix and complete downloaded blob/SHA-256 are retained in the evidence.
New-file-only patches have no old preimage to corroborate. Context-only matches
are not promoted to blob-identity confirmation. Unsafe paths, unsupported diffs,
missing source, malformed hunks and mismatches remain explicit exceptions.

Five DeepSeek exceptions are strict patch-parser rejections in privacyIDEA
patches containing SQLite test-data artifacts, not proof that the Python source
edits themselves are malformed. GPT-5.6 Python has
three unsupported implementation binary/rename/mode-only changes and a csvkit
context mismatch. Opus has an unsupported smolagents diff. GPT-5.6 TS has an
unsafe/unsupported TanStack router path. No raw artifact is edited to make it
pass. Error/empty/incomplete cases are not converted to explicit failures.

Evidence binds dataset, prediction, result and individual patch checksums.
Unverified patches stay in the predefined language population with their real
published outcome and **no footprint measurement**, never invented zero units.
Operational reset evidence remains a distinct tier; do not relabel these
results as operational full-checkout confirmations.

## Static measurement and reproduction

Use external storage: inventories/cache contain raw third-party source/patches
and are **not authorized for redistribution by this project**. The public
reporting scope is numeric measurements and provenance metadata, not copied
source. Existing source terms and submitter identity/effort conflicts remain
in `priority-live-provenance.md`; no blanket artifact licence is asserted.
The Opus run specifically needs its declared-model/effort caveat retained.

From a clean committed checkout, with the existing exact optional parser pins
and optional `pyarrow==25.0.1` installed:

```sh
export PYTHONPATH="$PWD"
OUT=/tmp/parsimony-priority-run
python examples/benchmark-discovery/run-priority-live.py --output-dir "$OUT" --phase inventory
python examples/benchmark-discovery/run-priority-live.py --output-dir "$OUT" --phase audit
python examples/benchmark-discovery/run-priority-live.py --output-dir "$OUT" --phase measure
```

The driver refuses dirty/uncommitted measurement checkouts and in-repository
raw output. Each cohort produces an external JSONL of static measurement records
without source code or model patches. Nothing imports or runs target code/tests.
Python, JavaScript and TypeScript populations must remain separate, as must
analyzer versions and other benchmarks. Keep scoring at 80% net / 20% churn,
including successful **and explicitly failed** attempts; missing measurement
coverage remains uncertainty rather than success-only filtering.

No new board is certified merely by this audit. Any research preview must visibly
identify configurations as **model + harness**, disclose unresolved historical
and protocol provenance, and retain complete-population bounds and coverage.
