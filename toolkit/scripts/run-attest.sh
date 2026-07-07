#!/usr/bin/env bash
# run-attest.sh — executed-verification attestation (capture-at-source). ADR-0003 / T3.
#
# WHAT IT ENFORCES (F-011 "RUN, don't reason"; closes giq.3.6 verify-before-assert
# and giq.3.3 verifier-hallucinated-defect):
#   The doctrine that a verification CLAIM must be EARNED BY EXECUTION, not reasoned
#   about. This tool is the EXECUTOR: it forks the designated command itself, and
#   records the real exit code + the stdout/stderr it observed. The author never
#   gets to supply the "output." Anti-fabrication comes from the tool being the one
#   that ran the command and HOLDING A PER-PROJECT CAPTURE KEY a hand-author lacks —
#   NOT from any unkeyed hash over a public namespace an informed forger can re-derive.
#
# CAPTURE-AT-SOURCE (the load-bearing decision, ADR-0003 Decision):
#   `run-attest.sh <claim-id> -- <cmd...>` EXECUTES <cmd...>, streams combined
#   stdout/stderr to a captured-output SIDECAR (`<id>.out`), records the real exit
#   code, a sha256 over the captured bytes, and a KEYED GENUINE-CAPTURE MARKER the
#   tool computes at capture time under a per-project secret key. It does NOT ingest
#   an externally-supplied output file.
#
# TWO LAYERS, TWO DISTINCT GUARANTEES (do not conflate — ADR-0003 Rationale):
#   1. Capture-at-source  -> anti-FABRICATION (against anyone WITHOUT the capture key).
#      The genuine-capture marker is a KEYED digest: it folds in the contents of a
#      per-project secret key file (mode 0600, 32+ random bytes, created on first
#      capture) along with claim/cmd/exit/output_sha/ts. `verify` recomputes it under
#      the SAME key; a record whose marker does not re-derive is REJECTED. Because the
#      key is secret, an informed forger who read this script (and thus knows the
#      derivation + the old public namespace) STILL cannot mint a valid marker for a
#      command that never ran — re-deriving requires READING the 0600 key, not the
#      public script. A bare sha cannot do this (a sha over an agent-authored fake
#      validates perfectly — the F-007 proxy-not-property trap this guard must avoid),
#      and neither could the previous UNKEYED public-namespace marker.
#   2. sha256 chain       -> anti-TAMPER. `verify` re-reads the sidecar and re-derives
#      output_sha256; a mismatch proves the captured bytes were edited AFTER capture.
#      The chain proves nothing about HOW the bytes were produced — that is layer 1's
#      job — it only guards the record against post-hoc editing.
#
# WHAT THIS DOES AND DOES NOT DEFEAT (honest scope — do not overclaim):
#   - DEFEATED: a fabricated record from anyone WITHOUT the capture key (the marker is
#     keyed; re-derivation needs the 0600 key, not the public script).
#   - DEFEATED: tamper-after-capture (the sha chain catches edited sidecar bytes).
#   - GUARANTEED REAL RUN on the lazy path: capture-at-source means the recorded exit/
#     output came from the tool forking the command, not from author-supplied text.
#   - RESIDUAL, IRREDUCIBLE (pushed to adversarial review): a determined AUTHOR who can
#     READ the local 0600 key file can still forge a marker. There is no trusted secret
#     store at the local mechanical layer to hide the key from someone with filesystem
#     access in the project, so this is irreducible here — exactly like the
#     run-then-misinterpret residual ADR-0003 already names. The mechanical floor
#     raises the bar from "read the public script" to "read a 0600 secret"; closing it
#     fully is an adversarial-review (human) responsibility, not a local-script one.
#
# FAIL-CLOSED (F-008): a missing/unreadable/markerless/sha-mismatched record — or a
#   MISSING CAPTURE KEY at verify time — is FATAL or FAIL, never a silent pass.
#   "Couldn't verify" must never read as "verified clean." For a designated claim this
#   is exempt from AUDIT_ALLOW_SKIP (ADR-0003).
#
# PORTABLE: pure bash + `shasum -a 256` (falls back to `sha256sum`). No python, no jq.
#
# USAGE:
#   run-attest.sh <claim-id> -- <command...>    # capture: run cmd, write record+sidecar
#   run-attest.sh verify <record.json>          # verify: re-derive sha + keyed marker
# Records live under ${RUN_ATTEST_DIR:-${CLAUDE_PROJECT_DIR:-.}/.rigor/run-attest}.
# The capture key lives at ${CLAUDE_PROJECT_DIR:-.}/.rigor/run-attest.key (0600).
# Exit: capture -> 0 on a successful capture (regardless of the captured cmd's exit);
#       verify  -> 0 ACCEPT / 1 REJECT (fabricated or tampered) / 2 FATAL (env/missing/
#                  missing-key — cannot verify without the capture key).

set -uo pipefail

TAG="run-attest"
emit() { echo "[$TAG] $*" >&2; }

# --- sha256 abstraction (portable: macOS shasum, Linux sha256sum) -------------
sha256_of_file() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    emit "FATAL: no sha256 tool (need shasum or sha256sum)"; exit 2
  fi
}
sha256_of_string() {
  # Hash a string without a trailing newline so the digest is stable across shells.
  if command -v shasum >/dev/null 2>&1; then
    printf '%s' "$1" | shasum -a 256 | awk '{print $1}'
  elif command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$1" | sha256sum | awk '{print $1}'
  else
    emit "FATAL: no sha256 tool (need shasum or sha256sum)"; exit 2
  fi
}

# --- Per-project capture key --------------------------------------------------
# The KEYED genuine-capture marker is what makes a hand-authored record fail verify
# even against an INFORMED forger who read this script. The marker folds in the
# contents of a per-project SECRET key file (mode 0600), so re-deriving it requires
# READING the 0600 key — not merely knowing the public derivation/namespace. A
# fabricated record minted without the key produces a marker that does not re-derive
# under the real key => REJECT.
#
# Honest residual: a determined author with filesystem read on the 0600 key can still
# forge. That is irreducible at the local mechanical layer (no trusted secret store)
# and is pushed to adversarial review — see the header "WHAT THIS DOES AND DOES NOT
# DEFEAT" and ADR-0003's run-then-misinterpret residual.
MARKER_NS="rigor.run-attest.capture-at-source.v2-keyed"
KEY_PATH="${RUN_ATTEST_KEY:-${CLAUDE_PROJECT_DIR:-.}/.rigor/run-attest.key}"

# Read the capture key contents. Mode: "create" mints one (0600) if absent (capture
# path); "require" treats absence as FATAL fail-closed (verify path).
read_capture_key() {
  mode="$1"  # create | require
  if [ ! -f "$KEY_PATH" ]; then
    if [ "$mode" = "create" ]; then
      keydir="$(dirname "$KEY_PATH")"
      mkdir -p "$keydir" || { emit "FATAL: cannot create key dir: $keydir"; exit 2; }
      # Generate 32 random bytes -> hex via the same sha tool (portable, no base64 deps).
      umask 077
      if command -v shasum >/dev/null 2>&1; then
        head -c 32 /dev/urandom | shasum -a 256 | awk '{print $1}' > "$KEY_PATH"
      else
        head -c 32 /dev/urandom | sha256sum | awk '{print $1}' > "$KEY_PATH"
      fi
      chmod 0600 "$KEY_PATH" 2>/dev/null || true
      [ -s "$KEY_PATH" ] || { emit "FATAL: failed to generate capture key at $KEY_PATH"; exit 2; }
    else
      emit "FATAL: capture key not found: $KEY_PATH — cannot verify a keyed marker without the key (fail-closed, F-008)"
      exit 2
    fi
  fi
  cat "$KEY_PATH" 2>/dev/null || { emit "FATAL: capture key unreadable: $KEY_PATH"; exit 2; }
}

derive_marker() {
  # derive_marker <key> <claim> <cmd> <exit> <output_sha256> <captured_ts>
  # KEYED: the secret key contents are the first, load-bearing component. Without it
  # the digest cannot be reproduced from the public namespace alone.
  sha256_of_string "${1}|${MARKER_NS}|${2}|${3}|${4}|${5}|${6}"
}

# --- tiny JSON field reader (string/number scalars; no nested objects) --------
json_field() {
  # json_field <file> <key>  -> prints the scalar value (outer quotes stripped,
  # inner escapes preserved verbatim), or empty.
  # BUG-bj4: the string alternative was "[^"]*" — it stopped at the FIRST quote
  # char, including an ESCAPED \" the capture writer legitimately emits for a cmd
  # containing quotes. The truncated rec_cmd then failed the keyed-marker
  # re-derivation -> false REJECT of a genuine record. The value grammar is now
  # ("(\\.|[^"\\])*"): an escaped-anything or any non-quote-non-backslash, so \"
  # and \\ pass through intact. NO unescaping on read — the marker deliberately
  # binds the ESCAPED string exactly as stored (capture derives it over cmd_esc).
  grep -Eo "\"$2\"[[:space:]]*:[[:space:]]*(\"(\\\\.|[^\"\\\\])*\"|[0-9]+)" "$1" 2>/dev/null \
    | head -1 \
    | sed -E "s/^\"$2\"[[:space:]]*:[[:space:]]*//; s/^\"//; s/\"$//"
}

# --- VERIFY subcommand --------------------------------------------------------
do_verify() {
  rec="${1:-}"
  [ -n "$rec" ] || { emit "FATAL: verify requires a record path"; exit 2; }
  if [ ! -f "$rec" ]; then
    emit "FATAL: record not found: $rec (a missing attestation is not a clean pass — F-008)"
    exit 2
  fi

  # Duplicate-key REJECT (bead skills_library-ql4): json_field binds the FIRST
  # occurrence of a key while jq/python parsers bind the LAST — a record carrying
  # a duplicate key verifies against one value while every JSON viewer displays
  # another (a decoy cmd appended to a genuine record still ACCEPTed, but a
  # viewer showed the decoy). A genuine capture writes each key exactly once;
  # any duplicate is a doctored record → REJECT before any field is trusted.
  # The count runs over a NEWLINE-FLATTENED view (review MEDIUM/BUG-1): grep -Eo
  # is line-oriented, so a decoy key split across a newline (`"cmd"\n: "…"`) —
  # which a real JSON parser still binds — was NOT counted; flattening makes the
  # scan see what jq sees. Key tokens cannot hide inside stored values: cmd is
  # escaped (\" for every value quote) and claim/output_file are charset-
  # restricted below (no " : , \), so a raw '"<key>":' sequence only occurs as a
  # key (review LOW/BUG-3 — the pre-fix claim charset let it appear in a value).
  rec_flat="$(tr '\n' ' ' < "$rec" 2>/dev/null)"
  for k in claim cmd exit output_file output_sha256 captured_ts capture_marker; do
    dup_n="$(printf '%s' "$rec_flat" | grep -Eo "\"$k\"[[:space:]]*:" 2>/dev/null | wc -l | tr -d '[:space:]')"
    if [ "${dup_n:-0}" -gt 1 ]; then
      emit "REJECT: duplicate \"$k\" key in record ($dup_n occurrences) — verify would bind the first while JSON viewers show the last (doctored record)"
      exit 1
    fi
  done

  claim="$(json_field "$rec" claim)"
  rec_cmd="$(json_field "$rec" cmd)"
  rec_exit="$(json_field "$rec" exit)"
  stored_sha="$(json_field "$rec" output_sha256)"
  stored_marker="$(json_field "$rec" capture_marker)"
  captured_ts="$(json_field "$rec" captured_ts)"
  outfile="$(json_field "$rec" output_file)"

  # Layer 1 (anti-fabrication): a genuine capture ALWAYS writes the marker and a
  # sidecar path. A hand-authored record omits them -> REJECT.
  if [ -z "$stored_marker" ] || [ -z "$outfile" ] || [ -z "$stored_sha" ]; then
    emit "REJECT: record lacks a genuine-capture marker / sidecar / sha — hand-authored, not captured at source (ADR-0003 anti-fabrication)"
    exit 1
  fi

  # Resolve the sidecar relative to the record's own directory (records are portable).
  recdir="$(cd "$(dirname "$rec")" && pwd)"
  case "$outfile" in
    /*) sidecar="$outfile" ;;
    *)  sidecar="$recdir/$outfile" ;;
  esac
  if [ ! -f "$sidecar" ]; then
    emit "FATAL: captured-output sidecar missing: $sidecar (cannot re-derive — F-008)"
    exit 2
  fi

  # Layer 2 (anti-tamper): re-derive the sha over the sidecar bytes. Mismatch means
  # the captured output was edited AFTER capture -> REJECT.
  actual_sha="$(sha256_of_file "$sidecar")"
  if [ "$actual_sha" != "$stored_sha" ]; then
    emit "REJECT: captured-output sha mismatch (stored=$stored_sha actual=$actual_sha) — output edited after capture (tamper)"
    exit 1
  fi

  # Layer 1 confirm: re-derive the KEYED genuine-capture marker from the record's
  # fields + the re-hashed sidecar, using the per-project capture key. A forger who
  # guessed the schema, namespace, and derivation but NOT the secret key produces a
  # marker that does not re-derive -> REJECT. A missing key is FATAL (fail-closed).
  capkey="$(read_capture_key require)" || exit $?
  expect_marker="$(derive_marker "$capkey" "$claim" "$rec_cmd" "$rec_exit" "$actual_sha" "$captured_ts")"
  if [ "$expect_marker" != "$stored_marker" ]; then
    emit "REJECT: keyed genuine-capture marker does not re-derive (expected=$expect_marker stored=$stored_marker) — not captured at source under this project's key (fabricated)"
    exit 1
  fi

  emit "ACCEPT: $rec — keyed capture-at-source marker re-derives and output sha intact (claim='$claim', exit=$rec_exit)"
  exit 0
}

# --- CAPTURE (default) subcommand ---------------------------------------------
do_capture() {
  claim="${1:-}"; shift || true
  [ -n "$claim" ] || { emit "FATAL: usage: run-attest.sh <claim-id> -- <command...>"; exit 2; }
  # Sanitize the claim-id (review LOW/BUG-3). It is BOTH a filename and an
  # unescaped JSON value (written raw as "claim" and "$claim.out"), so it must
  # carry no path separator/space AND none of the JSON-structural chars " : , \
  # that would let a value forge a '"<key>":' token (the dup-key guard's
  # trusted-charset premise). NOTE the pre-fix pattern `*[/" "]*` was a quoted
  # space — it rejected only `/` and space, never `"`. Each class is its own
  # pattern so the quoting of " and \ stays legible.
  case "$claim" in
    *[/:,]* | *' '* | *'"'* | *'\'* | .* | verify)
      emit "FATAL: invalid claim-id: '$claim' (no / space : , \" \\ ; not '.'-leading or 'verify')"; exit 2 ;;
  esac
  if [ "${1:-}" != "--" ]; then
    emit "FATAL: expected '--' before the command: run-attest.sh <claim-id> -- <command...>"; exit 2
  fi
  shift
  [ $# -gt 0 ] || { emit "FATAL: no command given after '--'"; exit 2; }

  dir="${RUN_ATTEST_DIR:-${CLAUDE_PROJECT_DIR:-.}/.rigor/run-attest}"
  mkdir -p "$dir" || { emit "FATAL: cannot create record dir: $dir"; exit 2; }
  rec="$dir/$claim.json"
  sidecar="$dir/$claim.out"

  # CAPTURE-AT-SOURCE: the tool itself runs the command and captures combined
  # stdout+stderr. The author supplies the command, never the output.
  emit "capturing: $* (claim='$claim')"
  "$@" >"$sidecar" 2>&1
  cmd_exit=$?

  out_sha="$(sha256_of_file "$sidecar")"
  ts="$(date +%s)"

  # Record the command as a single string. JSON-escape backslashes, double-quotes,
  # and NEWLINES (bead skills_library-ql4: an argv element containing a literal
  # newline previously landed multi-line in the record; grep -Eo is line-oriented,
  # so verify read back only the first physical line → keyed-marker mismatch →
  # false REJECT of a genuine capture). The awk stage joins the sed-escaped lines
  # with a literal \n; the marker binds this ESCAPED single-line form and verify
  # reads the same bytes back, so no unescape exists anywhere.
  cmd_str="$*"
  cmd_esc="$(printf '%s' "$cmd_str" | sed 's/\\/\\\\/g; s/"/\\"/g' \
    | awk 'NR>1{printf "\\n"} {printf "%s", $0}')"

  # KEYED marker: mint/read the per-project 0600 capture key and fold its secret
  # contents into the digest along with claim/cmd/exit/output_sha/ts.
  capkey="$(read_capture_key create)" || exit $?
  marker="$(derive_marker "$capkey" "$claim" "$cmd_esc" "$cmd_exit" "$out_sha" "$ts")"

  cat > "$rec" <<EOF
{
  "claim": "$claim",
  "cmd": "$cmd_esc",
  "exit": $cmd_exit,
  "output_file": "$claim.out",
  "output_sha256": "$out_sha",
  "captured_ts": $ts,
  "capture_marker": "$marker",
  "marker_ns": "$MARKER_NS"
}
EOF

  emit "captured: exit=$cmd_exit sha=$out_sha -> $rec (sidecar: $sidecar)"
  # A successful CAPTURE exits 0 even if the captured command failed: recording a
  # failing command is itself a genuine capture. The captured exit lives in the record.
  exit 0
}

# --- dispatch -----------------------------------------------------------------
case "${1:-}" in
  ""|-h|--help)
    grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  verify)
    shift; do_verify "$@" ;;
  *)
    do_capture "$@" ;;
esac
