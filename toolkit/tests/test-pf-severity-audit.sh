#!/usr/bin/env bash
# tests/test-pf-severity-audit.sh — negative test for scripts/pf-severity-audit.sh
# (T5 / ADR-0004 G5 — PF severity-monotonicity / no silent softening; giq.4.2).
#
# F-007 obligation (test-lib.sh): a guard that cannot prove it goes RED on bad
# input enforces nothing. G5 compares each PF entry's severity against its PRIOR
# git revision and FAILs on any DOWNGRADE that lacks an adjacent structured
# `re-grade:` exception marker. Because the property is a between-revision diff,
# the fixtures are built as a tiny HERMETIC throwaway git repo in a temp dir:
#   git init → commit a PF file at severity HIGH → modify to LOW → run the audit
#   against the committed (HEAD) version. The comparison is fully deterministic
#   and self-contained (no dependency on this repo's real history).
#
# Binary ACs proved here (rigor-guards-spec.md T5 / ADR-0004 falsification):
#   (a) silent downgrade (HIGH→LOW, no marker)        → FAIL (exit 1).
#   (b) downgrade WITH an adjacent `re-grade:` marker  → PASS (exit 0).
#   (c) no change (HIGH→HIGH)                          → PASS (exit 0).
#   (d) PF log NOT git-tracked                          → FATAL (exit 2, fail-closed F-008).
#   (e) assert_red_when_guard_removed: (b)→0 / (a)→!=0 — goes RED if the downgrade
#       check is stubbed to always-pass.
#
# The audit accepts `--prior <file>` to supply the prior revision explicitly (the
# testability seam), but the fixtures still exercise the real `git show HEAD:<path>`
# default path so the git-history dependency itself is covered, not bypassed.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TEST_DIR/../lib/test-lib.sh"

AUDIT="$TEST_DIR/../scripts/pf-severity-audit.sh"

# ── hermetic throwaway git repo ────────────────────────────────────────────────
REPO="$(mktemp -d)"
trap 'rm -rf "$REPO"' EXIT
PF="$REPO/process-failures.md"

git -C "$REPO" init -q
git -C "$REPO" config user.email test@example.com
git -C "$REPO" config user.name  test

# Committed (HEAD / "prior") version: a single PF entry at severity HIGH.
cat > "$PF" <<'EOF'
# Process-Failure Log

## PF-S1-01 (2026-06-21): scope drift on the audit family
severity: HIGH
A fix was shipped to a copy instead of the shared home.
EOF
git -C "$REPO" add process-failures.md
git -C "$REPO" commit -q -m "PF-S1-01 at HIGH"

# Helper: rewrite the working-tree PF file (HEAD stays at HIGH for the diff).
set_current() { printf '%s\n' "$1" > "$PF"; }

# Fixture bodies ----------------------------------------------------------------
# (a) silent downgrade HIGH→LOW, no marker.
BAD='# Process-Failure Log

## PF-S1-01 (2026-06-21): scope drift on the audit family
severity: LOW
A fix was shipped to a copy instead of the shared home.'

# (b) same downgrade, but carrying an adjacent structured re-grade: marker.
GOOD_REGRADE='# Process-Failure Log

## PF-S1-01 (2026-06-21): scope drift on the audit family
severity: LOW
re-grade: reclassified after the copy was deleted; blast radius was a throwaway.
A fix was shipped to a copy instead of the shared home.'

# (c) no change — still HIGH.
GOOD_NOCHANGE='# Process-Failure Log

## PF-S1-01 (2026-06-21): scope drift on the audit family
severity: HIGH
A fix was shipped to a copy instead of the shared home.'

echo "== pf-severity-audit (G5) =="

# (e) Core guard-fires proof: marked-downgrade PASSes (0); silent downgrade FAILs
# (!=0). A stub that always exits 0 makes bad_rc=0 → this pair goes RED.
assert_red_when_guard_removed \
  "set_current \"\$GOOD_REGRADE\"; bash '$AUDIT' --pf-log '$PF'" \
  "set_current \"\$BAD\";          bash '$AUDIT' --pf-log '$PF'"

# (a) silent downgrade → FAIL (1).
set_current "$BAD"
expect_exit 1 bash "$AUDIT" --pf-log "$PF"

# Confirm it is specifically the downgrade that is flagged (not an incidental fail).
TESTS_RUN=$((TESTS_RUN + 1))
out="$(set_current "$BAD"; bash "$AUDIT" --pf-log "$PF" 2>&1 || true)"
if printf '%s' "$out" | grep -Eqi 'downgrad|softening|HIGH.*LOW|PF-S1-01'; then
  echo "[PASS] silent downgrade flagged with a specific message"
else
  echo "[FAIL] downgrade not specifically reported:"
  printf '%s\n' "$out"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# (b) downgrade WITH re-grade: marker → PASS (0).
set_current "$GOOD_REGRADE"
expect_exit 0 bash "$AUDIT" --pf-log "$PF"

# (c) no change → PASS (0).
set_current "$GOOD_NOCHANGE"
expect_exit 0 bash "$AUDIT" --pf-log "$PF"

# (d) PF log NOT git-tracked → FATAL (2, fail-closed F-008).
# A brand-new temp file outside any git repo has no prior revision to compare.
UNTRACKED="$(mktemp -d)"
trap 'rm -rf "$REPO" "$UNTRACKED" "$SUBREPO"' EXIT
cat > "$UNTRACKED/process-failures.md" <<'EOF'
## PF-S1-01 (2026-06-21): something
severity: LOW
EOF
expect_exit 2 bash "$AUDIT" --pf-log "$UNTRACKED/process-failures.md"

# (f) SUBDIRECTORY default-path case — the real-world default (memory/).
# Exercises the DEFAULT `git show HEAD:<rel>` path (NO --prior flag) with the PF
# log living in a SUBDIR, committed at HIGH then silently downgraded to LOW in the
# working copy. This is the macOS portability regression guard: when the repo path
# resolves via /private (--show-toplevel) but PF_DIR resolves via /var (cd&&pwd),
# a string-prefix rel-path derivation collapses to the bare basename, which is NOT
# tracked at memory/process-failures.md → skipped()→FATAL(2) and the silent
# downgrade goes UNDETECTED. With git-derived rel path, the downgrade is caught → FAIL(1).
SUBREPO="$(mktemp -d)"
SUBPF="$SUBREPO/memory/process-failures.md"
git -C "$SUBREPO" init -q
git -C "$SUBREPO" config user.email test@example.com
git -C "$SUBREPO" config user.name  test
mkdir -p "$SUBREPO/memory"
cat > "$SUBPF" <<'EOF'
# Process-Failure Log

## PF-S1-01 (2026-06-21): scope drift on the audit family
severity: HIGH
A fix was shipped to a copy instead of the shared home.
EOF
git -C "$SUBREPO" add memory/process-failures.md
git -C "$SUBREPO" commit -q -m "PF-S1-01 at HIGH (subdir)"
# Silent downgrade in the working copy (no re-grade: marker).
printf '%s\n' "$BAD" > "$SUBPF"
# DEFAULT path: no --prior. Must catch the downgrade via git HEAD → FAIL(1).
expect_exit 1 bash "$AUDIT" --pf-log "$SUBPF"

# Confirm it is specifically the subdir downgrade that fires (default git path).
TESTS_RUN=$((TESTS_RUN + 1))
sub_out="$(bash "$AUDIT" --pf-log "$SUBPF" 2>&1 || true)"
if printf '%s' "$sub_out" | grep -Eqi 'downgrad|softening|HIGH.*LOW|PF-S1-01'; then
  echo "[PASS] subdir default-path silent downgrade flagged (macOS portability)"
else
  echo "[FAIL] subdir default-path downgrade not reported (rel-path regression?):"
  printf '%s\n' "$sub_out"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

test_summary
