#!/usr/bin/env bash
# tests/test-close-audit.sh — negative test for the close-audit.sh meta-audit.
#
# F-007 obligation: prove the gate goes RED (non-zero) on bad input. The whole
# point of close-audit (F-008 / maquette BUG-002) is that a GREEN must cover only
# audits that GENUINELY RAN. So the load-bearing negative case here is:
#   a constituent audit that CANNOT RUN (missing / non-executable / exits >=2)
#   MUST NOT yield a clean (exit 0) close — it must FATAL (exit 2).
#
# Cases:
#   GOOD: a scripts dir whose only constituent (a *-audit.sh) exits 0 -> close exits 0.
#   BAD1: a constituent that exits 2 (couldn't run / broken parser) -> close exits 2.
#   BAD2: a constituent present but NOT executable                  -> close exits 2.
#   BAD3: a constituent missing entirely (named but absent)         -> close exits 2.
#   BAD4: a constituent that exits 1 (real violation)               -> close exits 1.
#   ALLOW-SKIP: BAD1 with AUDIT_ALLOW_SKIP=1 -> downgraded to clean (0), proving the
#               documented fail-closed opt-out works (and that BAD1 was truly skip-gated,
#               not an accidental pass).

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "${TEST_DIR}/../lib/test-lib.sh"

CLOSE_AUDIT="${TEST_DIR}/../scripts/close-audit.sh"
FIX="${TEST_DIR}/fixtures/close-audit"

# The roster-mechanics assertions below exercise the CONSTITUENT logic, not the
# suite-first step (W1-3). Skip the suite here so these cases don't run the real
# suite (which would recurse back into this test). The dedicated suite-first cases
# at the end override this with a trivial fake suite. Robust whether this test is
# run directly or via run-all-tests.sh (which also exports this).
export CLOSE_AUDIT_SKIP_SUITE=1

rm -rf "$FIX"
mkdir -p "$FIX"

# --- helper: a constituent stub that exits with a given code -----------------
make_constituent() {
  # make_constituent <dir> <basename> <exit_code>
  d="$1"; name="$2"; code="$3"
  cat > "${d}/${name}" <<EOF
#!/usr/bin/env bash
echo "[stub] ${name} exiting ${code}"
exit ${code}
EOF
  chmod +x "${d}/${name}"
}

# === GOOD: a dir whose sole constituent passes ===============================
GOOD="${FIX}/good"
mkdir -p "$GOOD"
make_constituent "$GOOD" "alpha-audit.sh" 0
make_constituent "$GOOD" "beta-audit.sh"  0

# === BAD1: a constituent that FATALs (exit 2 — couldn't run) =================
BAD_FATAL="${FIX}/bad-fatal"
mkdir -p "$BAD_FATAL"
make_constituent "$BAD_FATAL" "alpha-audit.sh" 0
make_constituent "$BAD_FATAL" "broken-audit.sh" 2   # broken parser / missing input

# === BAD2: a constituent present but not executable =========================
BAD_NOEXEC="${FIX}/bad-noexec"
mkdir -p "$BAD_NOEXEC"
make_constituent "$BAD_NOEXEC" "alpha-audit.sh" 0
cat > "${BAD_NOEXEC}/inert-audit.sh" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod -x "${BAD_NOEXEC}/inert-audit.sh"   # cannot run -> cannot attest

# === BAD3: a named constituent that is missing ==============================
BAD_MISSING="${FIX}/bad-missing"
mkdir -p "$BAD_MISSING"
make_constituent "$BAD_MISSING" "alpha-audit.sh" 0
# we will reference a non-existent 'ghost-audit.sh' explicitly by arg

# === BAD4: a constituent with a real violation (exit 1) =====================
BAD_VIOL="${FIX}/bad-viol"
mkdir -p "$BAD_VIOL"
make_constituent "$BAD_VIOL" "alpha-audit.sh" 0
make_constituent "$BAD_VIOL" "dirty-audit.sh" 1

# --- assertions --------------------------------------------------------------

# GOOD discovers both constituents, both pass -> exit 0.
expect_exit 0 bash "$CLOSE_AUDIT" --scripts-dir "$GOOD"

# Core F-008 negative: a couldn't-run constituent must NOT yield a clean close.
# (exit 2, NOT 0.) This is the load-bearing assertion.
expect_exit 2 bash "$CLOSE_AUDIT" --scripts-dir "$BAD_FATAL"

# Non-executable constituent -> FATAL (couldn't run).
expect_exit 2 bash "$CLOSE_AUDIT" --scripts-dir "$BAD_NOEXEC"

# Missing-but-named constituent -> FATAL.
expect_exit 2 bash "$CLOSE_AUDIT" --scripts-dir "$BAD_MISSING" alpha-audit.sh ghost-audit.sh

# Real violation -> FAIL (exit 1), distinct from FATAL.
expect_exit 1 bash "$CLOSE_AUDIT" --scripts-dir "$BAD_VIOL"

# Bundled guard-fires assertion: good=0, the canonical bad (couldn't-run)=non-zero.
assert_red_when_guard_removed \
  "bash '$CLOSE_AUDIT' --scripts-dir '$GOOD'" \
  "bash '$CLOSE_AUDIT' --scripts-dir '$BAD_FATAL'"

# Documented fail-closed opt-out: AUDIT_ALLOW_SKIP=1 downgrades the couldn't-run
# FATAL to a clean pass — proving BAD1 was skip-gated (not an accidental pass) and
# that the opt-out is wired. A real violation must still NOT be downgraded.
expect_exit 0 env AUDIT_ALLOW_SKIP=1 bash "$CLOSE_AUDIT" --scripts-dir "$BAD_FATAL"
expect_exit 1 env AUDIT_ALLOW_SKIP=1 bash "$CLOSE_AUDIT" --scripts-dir "$BAD_VIOL"

# === Suite-first step (W1-3): close-audit runs run-all-tests.sh BEFORE the audits ===
# The load-bearing F-007 protection: if a negative test can no longer prove its audit
# goes RED on bad input, the close is blocked before any audit is trusted to go green.
# Trivial fake suites stand in for run-all-tests.sh (real path overridable via
# $CLOSE_AUDIT_SUITE) so these cases exercise the step without recursing into the suite.
SUITE_PASS="${FIX}/suite-pass.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$SUITE_PASS"; chmod +x "$SUITE_PASS"
SUITE_FAIL="${FIX}/suite-fail.sh"
printf '#!/usr/bin/env bash\necho "[fake-suite] a negative test regressed"; exit 1\n' > "$SUITE_FAIL"; chmod +x "$SUITE_FAIL"
SUITE_MISSING="${FIX}/no-such-suite.sh"   # deliberately never created

# Passing suite + clean roster -> the audits then run and pass -> exit 0.
expect_exit 0 env CLOSE_AUDIT_SKIP_SUITE=0 CLOSE_AUDIT_SUITE="$SUITE_PASS" bash "$CLOSE_AUDIT" --scripts-dir "$GOOD"
# FAILING suite -> close BLOCKED (exit 1) BEFORE the audits, even over a clean roster.
expect_exit 1 env CLOSE_AUDIT_SKIP_SUITE=0 CLOSE_AUDIT_SUITE="$SUITE_FAIL" bash "$CLOSE_AUDIT" --scripts-dir "$GOOD"
# MISSING suite -> FATAL (exit 2): cannot prove the audits still FAIL on bad input.
expect_exit 2 env CLOSE_AUDIT_SKIP_SUITE=0 CLOSE_AUDIT_SUITE="$SUITE_MISSING" bash "$CLOSE_AUDIT" --scripts-dir "$GOOD"

# Guard-fires pairing for the suite-first step: passing suite GREEN, broken suite RED.
assert_red_when_guard_removed \
  "env CLOSE_AUDIT_SKIP_SUITE=0 CLOSE_AUDIT_SUITE='$SUITE_PASS' bash '$CLOSE_AUDIT' --scripts-dir '$GOOD'" \
  "env CLOSE_AUDIT_SKIP_SUITE=0 CLOSE_AUDIT_SUITE='$SUITE_FAIL' bash '$CLOSE_AUDIT' --scripts-dir '$GOOD'"

test_summary
