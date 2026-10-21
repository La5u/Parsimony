#!/usr/bin/env bash
# Rebuild the website pages from frozen data. No patch analysis, no model calls.
#
#   scripts/rebuild-site.sh [OUT_DIR] [--offline]
#
# OUT_DIR defaults to site/. The Go page needs a checksum-bound scalar asset that is downloaded
# from a GitHub release; --offline skips that page and the all-languages DeepSWE page (index.html) built from it. After rebuilding into site/, `git status`
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

NAV=(--nav 'DeepSWE, all languages=index.html' --nav 'DeepSWE Python=python.html' --nav 'DeepSWE JavaScript=javascript.html'
     --nav 'DeepSWE TypeScript=typescript.html' --nav 'DeepSWE Go=go.html' --nav 'SWE-bench Verified=verified.html' --nav 'Live Python=live.html'
     --nav 'Live JavaScript=live-javascript.html' --nav 'Live TypeScript=live-typescript.html' --nav 'Live Go=live-go.html' --nav 'SWEeper PHP=sweeper-php.html'
     --nav 'SWE-Milestone, features=swe-milestone.html')
AA=examples/external/artificial-analysis-2026-10-08.json

LANGS=(python javascript typescript)
if [ "$OFFLINE" = 0 ]; then
  GO=$(mktemp -d)
  python examples/benchmark-discovery/fetch-go-v2-release.py --output "$GO"
  # DeepSWE release 1.0 runs are committed beside the checksum-bound v1.1 asset, never inside it.
  cp examples/deepswe-go-v2/release-1.0/*.jsonl "$GO/"
  cp examples/deepswe-go-v2/release-1.0/sensitivity.json "$GO/sensitivity.json"
  LANGS+=(go)
fi

for lang in "${LANGS[@]}"; do
  E=examples/deepswe-$lang PAGE=$lang EXTRA=()
  [ "$lang" = python ] && EXTRA=(--self-run examples/self-run/results/*.jsonl)
  [ "$lang" = go ] && E=$GO EXTRA=(--sensitivity-report examples/deepswe-go-v2/release-1.0/sensitivity.md)
  python -m parsimony.site "$E/score-panel.json" "$E/"*.jsonl --sensitivity "$E/sensitivity.json" \
    --benchmark deepswe "${NAV[@]}" --output "$OUT/$PAGE.html" --external "$AA" "${EXTRA[@]}"
done

if [ "$OFFLINE" = 0 ]; then
  # Same-task ratios of the four DeepSWE language boards combined; raw units are never pooled.
  python -m parsimony.site --merge python=examples/deepswe-python --merge javascript=examples/deepswe-javascript \
    --merge typescript=examples/deepswe-typescript --merge go="$GO" --benchmark deepswe "${NAV[@]}" \
    --output "$OUT/index.html" --external "$AA" --self-run examples/self-run/results/*.jsonl
fi

V=examples/mini-swe-agent-500
python -m parsimony.site "$V/score-panel.json" "$V/"*.jsonl --sensitivity "$V/sensitivity-35.json" \
  --benchmark verified "${NAV[@]}" --output "$OUT/verified.html"

L=examples/live-python
DATA=$L/site-data.json
[ "$OUT" = site ] || DATA=$OUT/live-data.json  # tests require the committed copy to match site/live.html
python -m parsimony.site "$L/score-panel.json" "$L/deepseek-v4.1-flash.jsonl" "$L/gpt-5.6-sol.jsonl" \
  "$L/claude-opus-4.8.jsonl" "$L/gpt-5.5-agav.jsonl" --sensitivity "$L/stability.json" --benchmark live \
  "${NAV[@]}" --output "$OUT/live.html" --data "$DATA"

S=examples/sweeper-php
python -m parsimony.site "$S/score-panel.json" "$S/"sweeper-*.jsonl --sensitivity "$S/stability.json" \
  --benchmark sweeper "${NAV[@]}" --output "$OUT/sweeper-php.html"

for lang in javascript typescript go; do
  M=examples/live-$lang
  python -m parsimony.site "$M/score-panel.json" "$M/"*-*.jsonl --sensitivity "$M/stability.json" \
    --benchmark live-multilang "${NAV[@]}" --output "$OUT/live-$lang.html"
done

# SWE-Milestone feature work: Go, TypeScript and Python boards combined by same-task ratios, as on index.html.
python -m parsimony.site --merge go=examples/swe-milestone-go --merge typescript=examples/swe-milestone-typescript \
  --merge python=examples/swe-milestone-python --benchmark milestone "${NAV[@]}" --output "$OUT/swe-milestone.html"
