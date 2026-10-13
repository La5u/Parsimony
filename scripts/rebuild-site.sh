#!/usr/bin/env bash
# Rebuild the six website pages from committed data. No patch analysis, no model calls.
#
#   scripts/rebuild-site.sh [OUT_DIR] [--offline]
#
# OUT_DIR defaults to site/. The Go page needs a checksum-bound scalar asset that is downloaded
# from a GitHub release; --offline skips that page. After rebuilding into site/, `git status`
# should show no changes unless the template, site.py or data changed.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=site OFFLINE=0
for arg in "$@"; do
  case "$arg" in
    --offline) OFFLINE=1 ;;
    *) OUT=$arg ;;
  esac
done
mkdir -p "$OUT"

NAV=(--nav 'DeepSWE Python=index.html' --nav 'DeepSWE JavaScript=javascript.html' --nav 'DeepSWE TypeScript=typescript.html'
     --nav 'DeepSWE Go=go.html' --nav 'SWE-bench Verified=verified.html' --nav 'Live Python=live.html')
AA=examples/external/artificial-analysis-2026-10-08.json

LANGS=(python javascript typescript)
if [ "$OFFLINE" = 0 ]; then
  GO=$(mktemp -d)
  python examples/benchmark-discovery/fetch-go-v2-release.py --output "$GO"
  LANGS+=(go)
fi

for lang in "${LANGS[@]}"; do
  E=examples/deepswe-$lang PAGE=$lang EXTRA=()
  [ "$lang" = python ] && PAGE=index EXTRA=(--self-run examples/self-run/results/*.jsonl)
  [ "$lang" = go ] && E=$GO EXTRA=(--sensitivity-report examples/deepswe-go-v2/sensitivity.md)
  python -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --sensitivity "$E/sensitivity.json" \
    --benchmark deepswe "${NAV[@]}" --output "$OUT/$PAGE.html" --external "$AA" "${EXTRA[@]}"
done

V=examples/mini-swe-agent-500
python -m parsimony.site "$V/score-panel.json" "$V/"*.jsonl --sensitivity "$V/sensitivity-35.json" \
  --benchmark verified "${NAV[@]}" --output "$OUT/verified.html"

L=examples/live-python
DATA=$L/site-data.json
[ "$OUT" = site ] || DATA=$OUT/live-data.json  # tests require the committed copy to match site/live.html
python -m parsimony.site "$L/score-panel.json" "$L/deepseek-v4.1-flash.jsonl" "$L/gpt-5.6-sol.jsonl" \
  "$L/claude-opus-4.8.jsonl" "$L/gpt-5.5-agav.jsonl" --sensitivity "$L/stability.json" --benchmark live \
  "${NAV[@]}" --output "$OUT/live.html" --data "$DATA"
