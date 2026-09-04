#!/bin/bash
set -eo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "ARGV RECEIVED: $*"
if OUT=$(python3 "$D/unit_test_runner.py" __shell-settings "$@" 2>&1); then
  echo "PREFLIGHT OK"; echo "TEST_PATH=$(echo "$OUT" | tail -1)"
else
  echo "PREFLIGHT FAILED: $OUT"; exit 2
fi
