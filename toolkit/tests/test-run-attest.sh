#!/usr/bin/env bash
# test-run-attest.sh — F-007 negative test for run-attest.sh (T3 / ADR-0003).
#
# THE F-007 OBLIGATION: an attestation that cannot prove it REJECTS a fabricated
# or tampered record enforces nothing. run-attest's whole claim is capture-at-
# source: the TOOL ran the command and recorded the real exit/output, and `verify`
# can tell a genuine captured record apart from a hand-authored or post-hoc-edited
# one. This test pins exactly that, and goes RED if `verify` is stubbed to always
# accept (because the BAD cases would then exit 0).
#
# GENUINE     : `run-attest <id> -- <cmd>` runs <cmd> itself, records the REAL exit
#               code + a sha256 over the captured output + a KEYED genuine-capture
#               marker. `verify` ACCEPTS it (exit 0).
# REAL-EXIT   : the recorded exit code is the command's actual exit code (a command
#               that exits 7 produces a record carrying exit 7) — not always 0.
# BAD-HAND    : a hand-written record with NO genuine-capture marker -> verify
#               REJECTS (non-zero). This is the naive fabrication case (no real run).
# BAD-INFORMED: an INFORMED forge — a record whose marker is re-derived from the OLD
#               PUBLIC namespace (the pre-fix unkeyed scheme) WITHOUT the secret
#               capture key, for a command that never ran. The keyed verify must
#               REJECT it (non-zero). This is the load-bearing case the pre-fix test
#               lacked: it proves the marker is genuinely KEYED, not public-derivable.
#               (We do NOT assert the WITH-key forge is defeated — it is the documented
#               irreducible residual: someone who can read the 0600 key can still forge.)
# BAD-TAMPER  : a genuine record whose captured-output file is edited AFTER capture
#               -> sha re-derivation mismatches -> verify REJECTS (non-zero).
# FAIL-CLOSED : verify on a missing record -> FATAL (exit 2), never a clean pass.
# KEY-ABSENT  : verify when the capture key file is gone -> FATAL (exit 2): the keyed
#               marker cannot be recomputed, so "cannot verify" must never read clean.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../lib/test-lib.sh
source "$TEST_DIR/../lib/test-lib.sh"

ATTEST="$TEST_DIR/../scripts/run-attest.sh"

# All artifacts go to a throwaway dir so the suite never dirties the tracked tree.
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
export CLAUDE_PROJECT_DIR="$WORK"
RECDIR="$WORK/.rigor/run-attest"

# --- GENUINE: the tool runs a real command that exits 0 ----------------------
expect_exit 0 bash "$ATTEST" claim-ok -- printf 'the build passes\n'
GENUINE="$RECDIR/claim-ok.json"

if [ ! -f "$GENUINE" ]; then
  echo "[FAIL] genuine run did not produce a record at $GENUINE"
  TESTS_FAILED=$((TESTS_FAILED + 1)); TESTS_RUN=$((TESTS_RUN + 1))
fi

# verify ACCEPTS the genuine record.
expect_exit 0 bash "$ATTEST" verify "$GENUINE"

# --- REAL-EXIT: a command exiting 7 yields a record carrying exit 7 -----------
# run-attest records the REAL exit code; capturing a failing command is itself a
# successful capture, so the attest run exits 0 and the record holds exit=7.
expect_exit 0 bash "$ATTEST" claim-fail -- sh -c 'echo nope; exit 7'
FAILREC="$RECDIR/claim-fail.json"
TESTS_RUN=$((TESTS_RUN + 1))
if grep -Eq '"exit"[[:space:]]*:[[:space:]]*7' "$FAILREC" 2>/dev/null; then
  echo "[PASS] real exit code captured (exit 7 recorded)"
else
  echo "[FAIL] record did not carry the real exit code 7:"; cat "$FAILREC" 2>/dev/null
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi
# The genuine failing-command record still verifies (capture was genuine).
expect_exit 0 bash "$ATTEST" verify "$FAILREC"

# --- BAD-HAND: a hand-authored record with no genuine-capture marker ----------
# An agent fabricates a record by hand. There is no real captured-output file and
# no genuine-capture marker the tool would have written. verify must REJECT.
HANDDIR="$WORK/hand"
mkdir -p "$HANDDIR"
cat > "$HANDDIR/claim-fake.json" <<'EOF'
{
  "claim": "claim-fake",
  "cmd": "pytest -q",
  "exit": 0,
  "output_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "captured_ts": 1700000000
}
EOF
# The fabricated output an agent might place next to it (still no real marker).
printf 'all tests passed\n' > "$HANDDIR/claim-fake.out"
expect_exit 1 bash "$ATTEST" verify "$HANDDIR/claim-fake.json"

# --- BAD-INFORMED: an informed forge using the OLD PUBLIC-NAMESPACE marker --------
# This is the case the pre-fix test never exercised. The forger READ the script, so it
# knows the schema, the derivation order, and the OLD public namespace
# "rigor.run-attest.capture-at-source.v1". It mints a record for a command that NEVER
# ran by re-deriving that UNKEYED marker over claim|sha|ts — WITHOUT the secret capture
# key. Under the pre-fix unkeyed scheme this forged record verified clean (rc 0), which
# is exactly the F-007 proxy-not-property trap. Under the keyed marker it must REJECT.
INFDIR="$WORK/informed"
mkdir -p "$INFDIR"
INF_OUT="$INFDIR/claim-informed.out"
printf 'fabricated: all green, nothing ran\n' > "$INF_OUT"
# A real sha over the forged output (the forger can compute this freely).
if command -v shasum >/dev/null 2>&1; then
  INF_SHA="$(shasum -a 256 "$INF_OUT" | awk '{print $1}')"
else
  INF_SHA="$(sha256sum "$INF_OUT" | awk '{print $1}')"
fi
INF_TS=1700000001
INF_CLAIM="claim-informed"
# Re-derive the OLD public-namespace marker exactly as the pre-fix script did:
#   sha256("rigor.run-attest.capture-at-source.v1|<claim>|<sha>|<ts>")  -- NO KEY.
OLD_NS="rigor.run-attest.capture-at-source.v1"
if command -v shasum >/dev/null 2>&1; then
  INF_MARKER="$(printf '%s' "${OLD_NS}|${INF_CLAIM}|${INF_SHA}|${INF_TS}" | shasum -a 256 | awk '{print $1}')"
else
  INF_MARKER="$(printf '%s' "${OLD_NS}|${INF_CLAIM}|${INF_SHA}|${INF_TS}" | sha256sum | awk '{print $1}')"
fi
cat > "$INFDIR/claim-informed.json" <<EOF
{
  "claim": "$INF_CLAIM",
  "cmd": "pytest -q",
  "exit": 0,
  "output_file": "claim-informed.out",
  "output_sha256": "$INF_SHA",
  "captured_ts": $INF_TS,
  "capture_marker": "$INF_MARKER",
  "marker_ns": "$OLD_NS"
}
EOF
# The capture key exists (the GENUINE run above created it), but the forger did not use
# it. The keyed re-derivation will not match the public-namespace marker -> REJECT (1).
expect_exit 1 bash "$ATTEST" verify "$INFDIR/claim-informed.json"

# --- BAD-TAMPER: edit the captured output AFTER a genuine capture --------------
# Genuinely capture, then tamper with the stored captured-output bytes. The sha
# re-derivation must mismatch -> verify REJECTS (non-zero).
expect_exit 0 bash "$ATTEST" claim-tamper -- printf 'original output\n'
TAMPREC="$RECDIR/claim-tamper.json"
# Locate the captured-output sidecar (the record points to it) and corrupt it.
OUTFILE="$RECDIR/claim-tamper.out"
TESTS_RUN=$((TESTS_RUN + 1))
if [ -f "$OUTFILE" ]; then
  printf 'TAMPERED output\n' > "$OUTFILE"
  echo "[PASS] tampered captured-output sidecar in place"
else
  echo "[FAIL] expected captured-output sidecar at $OUTFILE (verify cannot re-derive)"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi
expect_exit 1 bash "$ATTEST" verify "$TAMPREC"

# --- FAIL-CLOSED: verify on a missing record is FATAL, never a clean pass ------
expect_exit 2 bash "$ATTEST" verify "$RECDIR/does-not-exist.json"

# --- KEY-ABSENT: verify with the capture key removed is FATAL (fail-closed) -----
# A genuine record that ACCEPTS while the key is present must FATAL (exit 2) once the
# key file is gone: the keyed marker cannot be recomputed, so verification is
# impossible and "cannot verify" must never silently read as "verified clean" (F-008).
KEYFILE="$WORK/.rigor/run-attest.key"
TESTS_RUN=$((TESTS_RUN + 1))
if [ -f "$KEYFILE" ]; then
  echo "[PASS] capture key was created on first capture: $KEYFILE"
else
  echo "[FAIL] expected a capture key at $KEYFILE after a genuine capture"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi
# Move the key aside, prove verify FATALs, then restore it for later assertions.
KEYBAK="$WORK/run-attest.key.bak"
mv "$KEYFILE" "$KEYBAK" 2>/dev/null
expect_exit 2 bash "$ATTEST" verify "$GENUINE"
mv "$KEYBAK" "$KEYFILE" 2>/dev/null

# --- HEADLINE GUARD PROOF: genuine ACCEPTS, fabricated REJECTS -----------------
# Goes RED if verify is stubbed to always-accept (bad would then exit 0).
assert_red_when_guard_removed \
  "bash '$ATTEST' verify '$GENUINE'" \
  "bash '$ATTEST' verify '$HANDDIR/claim-fake.json'"

# Same proof for the tamper axis.
assert_red_when_guard_removed \
  "bash '$ATTEST' verify '$FAILREC'" \
  "bash '$ATTEST' verify '$TAMPREC'"

# --- BUG-bj4 regression: a cmd containing quotes / backslashes must round-trip -
# The capture writer JSON-escapes the cmd (\" / \\); json_field's old value
# grammar ("[^"]*") truncated at the first escaped quote, so rec_cmd fed a WRONG
# string into the keyed-marker re-derivation -> false REJECT of a genuine record.
# These captures go RED under the old reader and ACCEPT under the fixed one.
QREC="$RECDIR/claim-quotes.json"
expect_exit 0 bash "$ATTEST" claim-quotes -- bash -c 'echo "quoted arg" "second \"nested\""'
expect_exit 0 bash "$ATTEST" verify "$QREC"
BREC="$RECDIR/claim-backslash.json"
expect_exit 0 bash "$ATTEST" claim-backslash -- echo 'back\slash and "quote"'
expect_exit 0 bash "$ATTEST" verify "$BREC"
# Trailing-quote edge: the value's last content chars are an ESCAPED quote.
TREC="$RECDIR/claim-trailq.json"
expect_exit 0 bash "$ATTEST" claim-trailq -- echo 'ends-with-"'
expect_exit 0 bash "$ATTEST" verify "$TREC"

# Auto-pinned RED pair (review E6): the property the grammar fix rests on is
# that a cmd read back DIFFERENTLY from what capture bound (the old reader's
# truncation-at-\") cannot re-derive the keyed marker. good = the genuine
# quoted record ACCEPTs; bad = the same record with cmd truncated the way the
# old grammar read it REJECTs. Goes RED if verify stops binding cmd.
TRUNC="$RECDIR/claim-quotes-truncated.json"
sed 's/"cmd": ".*",/"cmd": "bash -c echo ",/' "$QREC" > "$TRUNC"
assert_red_when_guard_removed \
  "bash '$ATTEST' verify '$QREC'" \
  "bash '$ATTEST' verify '$TRUNC'"

# --- ql4 (a): newline-in-cmd round-trip ----------------------------------------
# An argv element containing a literal NEWLINE previously landed multi-line in the
# record; the line-oriented reader read back only the first physical line → keyed-
# marker mismatch → false REJECT of a GENUINE capture. Capture now \n-escapes into
# the single-line cmd_esc; this capture goes RED under the old writer.
NLREC="$RECDIR/claim-newline.json"
expect_exit 0 bash "$ATTEST" claim-newline -- printf '%s' 'line1
line2'
expect_exit 0 bash "$ATTEST" verify "$NLREC"
# The recorded cmd is single-line: the raw newline became a literal \n sequence.
TESTS_RUN=$((TESTS_RUN + 1))
if grep -F 'line1\nline2' "$NLREC" >/dev/null 2>&1; then
  echo "[PASS] newline-arg cmd recorded single-line (\\n-escaped)"
else
  echo "[FAIL] record lacks the \\n-escaped cmd:"; cat "$NLREC" 2>/dev/null
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# --- ql4 (b): duplicate-key REJECT ----------------------------------------------
# The display-divergence attack: append a decoy "cmd" to a GENUINE record. verify
# bound the FIRST key (genuine → ACCEPT) while jq/python viewers show the LAST
# (the decoy). A duplicate-keyed record is doctored → must REJECT (1).
DUPREC="$RECDIR/claim-dup.json"
{ sed '$d' "$GENUINE"; printf ',"cmd": "decoy --never-ran"\n}\n'; } > "$DUPREC"
expect_exit 1 bash "$ATTEST" verify "$DUPREC"
# Guard-fires pair: the same record without the decoy ACCEPTs; with it REJECTs.
assert_red_when_guard_removed \
  "bash '$ATTEST' verify '$GENUINE'" \
  "bash '$ATTEST' verify '$DUPREC'"

# ql4 review MEDIUM/BUG-1: a decoy key split across a NEWLINE (`"cmd"\n: "…"`) — a
# real JSON parser still binds it (last-key-wins) — evaded the line-oriented count.
# The flattened count must catch it → REJECT. Goes RED if the flatten is removed
# (the pre-fix per-file grep counts the split key as 0 and ACCEPTs the decoy).
NLDUP="$RECDIR/claim-nldup.json"
{ sed '$d' "$GENUINE"; printf ',\n  "cmd"\n  : "decoy --never-ran"\n}\n'; } > "$NLDUP"
expect_exit 1 bash "$ATTEST" verify "$NLDUP"
assert_red_when_guard_removed \
  "bash '$ATTEST' verify '$GENUINE'" \
  "bash '$ATTEST' verify '$NLDUP'"

# ql4 review SHOULD-FIX-3: the dup-key loop covers all 7 keys, not just cmd. A
# split non-cmd decoy (`"exit"`) must also REJECT.
EXDUP="$RECDIR/claim-exdup.json"
{ sed '$d' "$GENUINE"; printf ',\n  "exit"\n  : 137\n}\n'; } > "$EXDUP"
expect_exit 1 bash "$ATTEST" verify "$EXDUP"

# ql4 review LOW/BUG-3: a claim-id carrying JSON-structural chars (" : ,) is
# FATAL (2) at capture — previously it passed the `*[/" "]*` sanitizer (a quoted
# space that never rejected "), landed raw in the record, and false-REJECTED the
# GENUINE capture (a `"cmd":` token inside the claim value read as a duplicate key).
expect_exit 2 bash "$ATTEST" 'x","cmd":"evil' -- echo hi
expect_exit 2 bash "$ATTEST" 'has:colon'       -- echo hi
expect_exit 2 bash "$ATTEST" 'has,comma'       -- echo hi
# A clean claim-id with none of those still captures fine (the sanitizer did not
# over-tighten): dashes and underscores remain valid.
expect_exit 0 bash "$ATTEST" ok_claim-1 -- echo hi

test_summary
