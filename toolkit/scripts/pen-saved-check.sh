#!/usr/bin/env bash
# toolkit/scripts/pen-saved-check.sh — the saved-state precondition for .pen
# extraction (spec §5 amendment PA-5; bead skills_library-b30).
#
# THE PROBLEM (measured 2026-07-02): Pencil holds edits in editor memory with no
# MCP-triggerable save — after 31+ batch_design ops the on-disk .pen mtime was
# 9 DAYS stale. The extractor reads the LIVE EDITOR (MCP) while §6.2 stamps
# pen-sha256 over DISK bytes, so extracting from unsaved state records a hash
# describing a file that does not contain the extracted content — drift-at-birth
# that §6.2's pen-change trigger can never see (disk never moved).
#
# THE MECHANICAL FLOOR: neither bash nor the agent can compare editor content to
# disk content (the .pen is ciphertext at rest; the editor is only reachable via
# MCP). What CAN be proven mechanically is that A SAVE LANDED inside the
# extraction window. Three tool steps around the operator's save (four steps
# total), run by the extraction step:
#
#   1) arm <penPath>     — record the disk state (sha256 + mtime) in the witness
#                          BEFORE the operator saves. FATAL if the .pen is
#                          absent, a symlink, or on the a-plus denylist (the §5
#                          invariants, enforced here too).
#   2) <operator saves in Pencil (Cmd+S)> — the one step no tool can perform.
#   3) verify <penPath>  — PASS iff the disk changed since arm (sha256 differs,
#                          OR same bytes with a NEWER mtime — a rewrite of
#                          identical content still proves editor==disk). FAIL if
#                          nothing was written since arming: the editor's state
#                          is NOT on disk; extraction MUST NOT proceed. On PASS,
#                          re-stamps the witness with the verified sha and emits
#                          `pen-sha256: <sha>` — the extractor stamps THAT value
#                          into export.digest (capture-at-source, F-011).
#   4) check <penPath>   — at stamp time (immediately before export.digest is
#                          written): PASS iff the disk sha still equals the
#                          verified sha; FAIL if the disk moved after verify
#                          (another save landed — re-run verify). This closes
#                          the verify→stamp gap mechanically.
#
# LIMITATIONS (claims match implementation — PF-S1-01):
#   - verify proves A WRITE landed after arm, not that the write came from the
#     editor (a git checkout touching the file also passes). Signal, not the full
#     property; the compensating control is the §6.5 drift re-extraction, which
#     compares live-editor projection to committed exports semantically.
#   - Unsaved edits made AFTER verify+check are invisible here — that is §6.5's
#     documented territory (post-extraction drift), not drift-at-birth.
#   - If Pencil ever skips a true no-op save entirely (no rewrite, no mtime
#     touch), the operator makes a trivial edit+undo before saving; verify's
#     FAIL message says so. Sub-second caveat: mtime compares in WHOLE seconds,
#     so an identical-content save landing in the SAME second as arm reads FAIL
#     (fail-closed friction, never a false PASS) — wait a second and re-save.
#   - The [ -L ] symlink check and the later sha/mtime reads are not atomic — a
#     local writer racing the gap could retarget the read. The same accepted
#     residual as pen-integrity.sh (arch-F2): an actor who can win that race can
#     already write the trusted local state directly.
#
# EXIT CONTRACT (toolkit convention, fail-closed per F-008):
#   0 PASS / 1 FAIL (precondition not met) / 2 FATAL (could not check — absent
#   witness, path mismatch, unreadable pen, symlink, a-plus path, no sha tool).
#   A check that cannot run does not pass.
#
# PORTABILITY: pure bash 3.2 + POSIX sed/grep; sha via shasum -a 256 or
# sha256sum; mtime via stat -f %m (BSD/macOS) or stat -c %Y (GNU). Paths via
# ${CLAUDE_PROJECT_DIR}; witness at ${CLAUDE_PROJECT_DIR}/.rigor/pen-save-witness.json.

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
WITNESS="${PROJECT_DIR}/.rigor/pen-save-witness.json"

fatal() { echo "pen-saved-check: FATAL — $1" >&2; echo "RESULT: FATAL"; exit 2; }
fail()  { echo "pen-saved-check: FAIL — $1" >&2;  echo "RESULT: FAIL";  exit 1; }
pass()  { echo "RESULT: PASS"; exit 0; }

# ── portable primitives ───────────────────────────────────────────────────────
# `--` sentinels throughout so a dash-leading path is never parsed as flags.
sha_of() { # $1 = file → 64-hex on stdout, or empty on failure
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 -- "$1" 2>/dev/null | awk '{print $1}'
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum -- "$1" 2>/dev/null | awk '{print $1}'
  fi
}
# mtime_of — epoch seconds, VALUE-guarded on both variants: GNU `stat -f` means
# --file-system and prints an FS-info block to STDOUT while exiting non-zero,
# and `$(A||B)` capture RETAINS A's stdout — a naive BSD-first `||` chain
# therefore returns "<FS garbage><epoch>" on Linux (D1, executed on coreutils).
# GNU-first, and each candidate is accepted only if purely numeric.
mtime_of() { # $1 = file → epoch seconds on stdout, or empty on failure
  local m
  m="$(stat -c %Y -- "$1" 2>/dev/null)"
  case "$m" in ''|*[!0-9]*) m="$(stat -f %m -- "$1" 2>/dev/null)";; esac
  case "$m" in ''|*[!0-9]*) return 1;; esac
  printf '%s' "$m"
}
json_field() { # $1 = json ; $2 = field → value of a quoted string field
  printf '%s' "$1" | tr '\n' ' ' \
    | sed -n "s/.*\"$2\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p"
}

# ── shared pen validation (the §5 invariants, mirrored from pen-integrity.sh) ─
validate_pen() { # $1 = penPath
  local pen="$1" lower lower_joined
  # a-plus denylist: LEXICAL check on the given form AND the base-joined form
  # ($PROJECT_DIR/$pen — catches a relative pen inside an a-plus-rooted project;
  # the D2 parity fix with pen-integrity.sh). Never realpath-resolved — resolving
  # would probe the tree the check keeps us out of.
  lower="$(printf '%s' "$pen" | tr '[:upper:]' '[:lower:]')"
  lower_joined="$(printf '%s/%s' "$PROJECT_DIR" "$pen" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in *a-plus-maxing*) fatal "penPath is under a-plus-maxing ('$pen') — forbidden substrate (NEW-5)";; esac
  case "$lower_joined" in *a-plus-maxing*) fatal "base-joined penPath is under a-plus-maxing ('$PROJECT_DIR/$pen') — forbidden substrate (NEW-5)";; esac
  [ -L "$pen" ] && fatal "pinned .pen is a SYMLINK ('$pen') — repo-residency invariant rejects symlinks (lstat, non-traversing)"
  [ -f "$pen" ] || fatal "pinned .pen absent or not a regular file ('$pen')"
  [ -r "$pen" ] || fatal "pinned .pen unreadable ('$pen')"
  command -v shasum >/dev/null 2>&1 || command -v sha256sum >/dev/null 2>&1 \
    || fatal "no SHA-256 tool (need shasum or sha256sum)"
}

# ── subcommands ───────────────────────────────────────────────────────────────
do_arm() { # $1 = penPath
  local pen="$1" sha mt
  validate_pen "$pen"
  sha="$(sha_of "$pen")"; [ -n "$sha" ] || fatal "could not hash '$pen'"
  mt="$(mtime_of "$pen")"; [ -n "$mt" ] || fatal "could not stat mtime of '$pen'"
  mkdir -p "${PROJECT_DIR}/.rigor" || fatal "cannot create ${PROJECT_DIR}/.rigor"
  printf '{"format":"pen-save-witness-v0","state":"armed","pen_path":"%s","pre_sha256":"%s","pre_mtime":"%s","armed_ts":"%s"}\n' \
    "$pen" "$sha" "$mt" "$(date +%s)" > "$WITNESS" || fatal "cannot write witness $WITNESS"
  echo "pen-saved-check: ARMED — pre-save disk state recorded (sha=${sha}, mtime=${mt})."
  echo "pen-saved-check: now SAVE in the Pencil editor (Cmd+S), then run: pen-saved-check.sh verify '$pen'"
  pass
}

read_witness() { # → sets W_STATE W_PATH W_PRE_SHA W_PRE_MT W_VER_SHA; FATALs if unusable
  [ -f "$WITNESS" ] || fatal "witness absent ($WITNESS) — run 'arm' first"
  local raw; raw="$(cat "$WITNESS" 2>/dev/null)" || fatal "witness unreadable"
  [ -n "$raw" ] || fatal "witness empty"
  [ "$(json_field "$raw" format)" = "pen-save-witness-v0" ] || fatal "witness format unknown (not pen-save-witness-v0)"
  W_STATE="$(json_field "$raw" state)"
  W_PATH="$(json_field "$raw" pen_path)"
  W_PRE_SHA="$(json_field "$raw" pre_sha256)"
  W_PRE_MT="$(json_field "$raw" pre_mtime)"
  W_VER_SHA="$(json_field "$raw" verified_sha256)"
}

do_verify() { # $1 = penPath
  local pen="$1" sha mt
  validate_pen "$pen"
  read_witness
  [ "$W_PATH" = "$pen" ] || fatal "witness is for a different pen ('$W_PATH' != '$pen') — re-arm"
  [ "$W_STATE" = "armed" ] || fatal "witness state is '$W_STATE', expected 'armed' — re-arm (verify is single-shot)"
  [ -n "$W_PRE_SHA" ] && [ -n "$W_PRE_MT" ] || fatal "witness missing pre_sha256/pre_mtime — re-arm"
  sha="$(sha_of "$pen")"; [ -n "$sha" ] || fatal "could not hash '$pen'"
  mt="$(mtime_of "$pen")"; [ -n "$mt" ] || fatal "could not stat mtime of '$pen'"
  # Both mtimes must be numeric BEFORE the comparison below — a non-numeric value
  # would make the arithmetic test error out (false) and skip the FAIL branch,
  # reading as PASS. Fail-closed: unparseable freshness is FATAL, never a pass.
  case "$mt" in ''|*[!0-9]*) fatal "current mtime non-numeric ('$mt')";; esac
  case "$W_PRE_MT" in ''|*[!0-9]*) fatal "witness pre_mtime non-numeric ('$W_PRE_MT') — re-arm";; esac

  if [ "$sha" = "$W_PRE_SHA" ] && [ "$mt" -le "$W_PRE_MT" ]; then
    fail "no save landed since arming (sha and mtime unchanged) — the editor's state is NOT on disk. Save in Pencil (Cmd+S) and re-run verify. If Pencil skips a no-op save, make a trivial edit+undo first. Extraction MUST NOT proceed (drift-at-birth, b30)."
  fi

  # A write landed after arming: bytes changed, or identical bytes rewritten
  # with a newer mtime (still proves editor==disk at save time).
  printf '{"format":"pen-save-witness-v0","state":"verified","pen_path":"%s","pre_sha256":"%s","pre_mtime":"%s","verified_sha256":"%s","verified_mtime":"%s","verified_ts":"%s"}\n' \
    "$pen" "$W_PRE_SHA" "$W_PRE_MT" "$sha" "$mt" "$(date +%s)" > "$WITNESS" || fatal "cannot rewrite witness"
  echo "pen-saved-check: SAVE WITNESSED — disk now carries the saved state."
  echo "pen-sha256: $sha"
  echo "pen-saved-check: extract NOW and stamp export.digest with the sha above; run 'check' immediately before stamping."
  pass
}

do_check() { # $1 = penPath
  local pen="$1" sha
  validate_pen "$pen"
  read_witness
  [ "$W_PATH" = "$pen" ] || fatal "witness is for a different pen ('$W_PATH' != '$pen') — re-arm"
  [ "$W_STATE" = "verified" ] || fatal "witness state is '$W_STATE', expected 'verified' — run arm + verify first"
  [ -n "$W_VER_SHA" ] || fatal "witness missing verified_sha256 — re-run verify"
  sha="$(sha_of "$pen")"; [ -n "$sha" ] || fatal "could not hash '$pen'"
  if [ "$sha" != "$W_VER_SHA" ]; then
    fail "disk .pen moved AFTER verify (sha $sha != verified $W_VER_SHA) — another save landed; re-run verify so the stamp describes the extracted state."
  fi
  echo "pen-sha256: $sha"
  pass
}

# ── main ──────────────────────────────────────────────────────────────────────
[ "$#" -ge 2 ] || fatal "usage: pen-saved-check.sh {arm|verify|check} <penPath>"
CMD="$1"; PEN="$2"
case "$CMD" in
  arm)    do_arm "$PEN" ;;
  verify) do_verify "$PEN" ;;
  check)  do_check "$PEN" ;;
  *)      fatal "unknown subcommand '$CMD' (want arm|verify|check)" ;;
esac
