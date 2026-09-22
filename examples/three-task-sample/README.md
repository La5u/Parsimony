# Original three-task snapshot

These files preserve the initial 10-model × 3-task sample. The parent directory now contains the expanded 10-task run, retaining these original three tasks. Both runs use the same model submissions, pinned experiments revision, dataset and scoring methodology.

Inspect the original leaderboard with:

```sh
python -m parsimony leaderboard examples/three-task-sample/ten-model-results.jsonl --shared
```
