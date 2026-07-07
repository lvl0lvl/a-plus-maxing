#!/usr/bin/env bash
# test-gate-attest.sh — negative+positive tests for the shared gate_attest engine
# (lib/gate_attest.py), discovered by run-all-tests.sh. gate_attest is the OPTIONAL
# python component of the toolkit (mechanically-attested gates; PF-S3-01 lineage).
# It requires python3 + the `jsonschema` package. When those are absent the engine
# itself is unusable, so this test SKIPS LOUDLY (never silently): visible message,
# non-fatal — a bash-only project that doesn't use gate_attest stays green.
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[test-gate-attest] SKIPPED (loud): python3 not found — gate_attest engine not testable here."
  exit 0
fi
if ! python3 -c 'import jsonschema' >/dev/null 2>&1; then
  echo "[test-gate-attest] SKIPPED (loud): python 'jsonschema' not installed — gate_attest requires it."
  echo "[test-gate-attest]   install with: python3 -m pip install jsonschema   (then this test runs)"
  exit 0
fi

python3 "$DIR/gate_attest_selftest.py"
rc=$?
if [ "$rc" -eq 0 ]; then
  echo "[test-gate-attest] RESULT: PASS"
else
  echo "[test-gate-attest] RESULT: FAIL (gate_attest self-test rc=$rc)"
fi
exit "$rc"
