#!/usr/bin/env bash
# Reproduce ratio diagnostics from published scalars, not patches. No model calls.
# Usage: scripts/diagnose-rankings.sh [OUT_DIR] [--offline]
# Offline mode skips DeepSWE Go, whose scalars are a checksum-bound release asset.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=examples/ranking-diagnostics OFFLINE=0 GO=
for arg in "$@"; do
  case "$arg" in
    --offline) OFFLINE=1 ;;
    *) OUT=$arg ;;
  esac
done
mkdir -p "$OUT"
trap '[ -z "$GO" ] || rm -rf "$GO"' EXIT

report() {
  local name=$1 panel=$2
  shift 2
  python -m parsimony.diagnostics "$panel" "$@" --output "$OUT/$name.json"
}
for lang in python javascript typescript; do
  E=examples/deepswe-$lang
  report deepswe-$lang "$E/score-panel.json" "$E/"*.jsonl
done
if [ "$OFFLINE" = 0 ]; then
  GO=$(mktemp -d)
  python examples/benchmark-discovery/fetch-go-v2-release.py --output "$GO"
  # Same Go population as the website: release 1.0 runs sit beside the checksum-bound asset.
  cp examples/deepswe-go-v2/release-1.0/*.jsonl "$GO/"
  report deepswe-go "$GO/score-panel.json" "$GO/"*.jsonl
else
  printf '%s\n' 'Offline diagnostics: skipping DeepSWE Go; existing report copies are left unchanged.' >&2
fi
E=examples/mini-swe-agent-500
report verified "$E/score-panel.json" "$E/"*.jsonl
E=examples/live-python
report live-python "$E/score-panel.json" "$E/deepseek-v4.1-flash.jsonl" "$E/gpt-5.6-sol.jsonl" \
  "$E/claude-opus-4.8.jsonl" "$E/gpt-5.5-agav.jsonl"
for lang in javascript typescript go; do
  E=examples/live-$lang
  report live-$lang "$E/score-panel.json" "$E/"*-*.jsonl
done
E=examples/sweeper-php
report sweeper-php "$E/score-panel.json" "$E/"sweeper-*.jsonl
