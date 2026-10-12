#!/usr/bin/env bash
# Run the offline checks: Python tests, page behaviour tests, submission bundles and whitespace.
# JavaScript/TypeScript tests need `npm ci`; Go tests need `pip install '.[languages]'`.
# Without them those tests are skipped, not failed.
#
#   scripts/check.sh
set -euo pipefail
cd "$(dirname "$0")/.."

python -m unittest discover -s tests -q
python -m parsimony.contribute validate submissions
node tests/custom_benchmark.cjs
for page in index javascript typescript go verified live; do
  node tests/site_sorting.cjs "site/$page.html"
done
git diff --check
echo 'All checks passed.'
