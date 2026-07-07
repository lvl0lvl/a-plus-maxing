#!/usr/bin/env bash
# toolkit/scripts/pen-integrity.sh — the §6.2 export-integrity gate (build entry, pure bash).
#
# The build-entry hard dependency every build-time gate (§6.3 wiring, §6.4 seam) declares:
# it decides whether the committed Interaction-Model EXPORTS are still trustworthy before
# anything downstream runs on them. Two independent checks (spec §6.2), both plain bash so
# this runs in CI with no python dependency:
#
#   CHECK 1 — EXPORT INTEGRITY (hand-edit detection).
#     Recomputes the §5 content digest from the export files (reusing scripts/pen-digest.sh)
#     and compares it to the `content-sha256` recorded in export.digest. Any hand-edit of an
#     export that did NOT also recompute the digest -> FAIL (exit 1). This is INTEGRITY, not
#     AUTHENTICITY [BH-F4]: an editor who ALSO recomputes content-sha256 to match passes this
#     check (the documented honest boundary — see LIMITATIONS). The authenticity backstop is
#     CHECK 2 + the §6.5 drift re-extraction, never this check.
#
#   CHECK 2 — PEN-CHANGE TRIGGER [NEW-1] (a change SIGNAL, not a semantic verdict).
#     Recomputes `shasum -a 256` over the WHOLE pinned .pen (opaque encrypted bytes) and
#     compares it to the recorded `pen-sha256`. The .pen ciphertext hash is deterministic and
#     flips on a 1-byte edit, so a mismatch means "the .pen changed since extraction." A
#     mismatch does NOT fail the gate (aesthetic-only edits flip it too — the semantic verdict
#     is §6.5's projection diff). Instead it emits a distinct PEN-CHANGED signal meaning:
#     a fresh §6.5 drift re-extraction is MANDATORY and wave-close is BLOCKED until §6.5 has
#     run on the current .pen and re-stamped pen-sha256. Same hash -> clean.
#
# EXIT CONTRACT (0 PASS / 1 FAIL / 2 FATAL, fail-closed per F-008) — the toolkit convention:
#   0 PASS   — CHECK 1 clean; CHECK 2 clean (pen unchanged), OR CHECK 2 raised PEN-CHANGED.
#              A PEN-CHANGED run still exits 0 (§6.2: "does NOT fail by itself") but its
#              RESULT line reads PASS-WITH-PEN-CHANGED and carries the wave-close-block signal,
#              so it is NOT a plain pass — the wave-close consumer greps for `PEN-CHANGED`.
#   1 FAIL   — CHECK 1 integrity mismatch (a hand-edited export).
#   2 FATAL  — the gate could not run / could not verify freshness: absent, empty, or
#              unparseable export.digest envelope (unknown format:, missing content-sha256 /
#              pen-sha256 / pen-path / stamped); missing/empty config.json or unparseable
#              penPath; config penPath != recorded pen-path (stale/tampered pin); the pinned
#              .pen absent at penPath (repo-residency §5, fail-closed — downgradable, see
#              below), a SYMLINK (repo-residency, non-downgradable), or unreadable/unhashable;
#              an a-plus-maxing penPath [NEW-5]; no SHA-256 tool. A gate that did not run did
#              not pass. FAIL (a real violation) takes precedence over a fail-closed skip.
#   AUDIT_ALLOW_SKIP=1 downgrades ONLY the repo-residency skip (a .pen deliberately kept
#     outside the repo — §5 says such a project MUST declare it and compensate with a mandated
#     §6.5 at wave-close; this flag IS that declaration). It NEVER downgrades the a-plus FATAL,
#     the unparseable-envelope FATAL, or a CHECK 1 integrity FAIL.
#
# THE export.digest ENVELOPE (format-v0, provisional per T-27) [architect-F3 / §5]:
#   Phase-1a stamped export.digest as a bare 64-char content hash. §5 (architect-F3) specifies
#   it as a multi-field envelope. This gate reads that envelope. Format — one `key: value`
#   line per field (NOT JSON, so the gate parses it with sed and needs no python); every field
#   ends the line, file ends in exactly one trailing newline:
#   exactly one SPACE after each colon (`key: value`) — the parser tolerates extra spaces but
#   the canonical form is single-space, so author it that way:
#     format: pen-export-envelope-v0
#     content-sha256: <64 lowercase hex>
#     pen-sha256: <64 lowercase hex>
#     pen-path: <penPath, repo-root-relative; == config.json penPath at extraction>
#     stamped: <ISO-8601 UTC; DATA written at stamp time, never computed by any gate>
#   FIELD OWNERSHIP (the split architect-F3 asked to be defined):
#     - `content-sha256` is computed by pen-digest.sh (bash) over the export set. THIS gate
#       RE-runs pen-digest.sh and compares — pen-digest.sh keeps its Phase-1a contract of
#       emitting ONLY the bare content hash; the envelope wraps that hash, it does not replace
#       the script's output.
#     - `pen-sha256`, `pen-path`, `stamped` are stamped by the EXTRACTOR (the pen-extract agent
#       step; no CLI tool exists yet — R-3). For the committed fixtures they are hand-stamped.
#     - export.digest is NOT itself in the hashed export set (a digest cannot hash itself), so
#       wrapping the bare hash in this envelope does not change `content-sha256`.
#
# LIMITATIONS (claims match implementation — PF-S1-01 / BH-F4):
#   - CHECK 1 is integrity, not authenticity: an edit that ALSO recomputes content-sha256
#     passes it. Closing that is CHECK 2 + §6.5, not this check.
#   - CHECK 2 is a CHANGE signal, not a semantic verdict: it flips on aesthetic-only .pen edits
#     too. Whether a change matters to the wiring projection is §6.5's job.
#   - The a-plus denylist is a LEXICAL path check (case-insensitive substring `a-plus-maxing`
#     on penPath and its base-joined form). It deliberately does NOT realpath-resolve the path:
#     resolving would require probing the very tree the check exists to keep us out of. The
#     symlink-name evasion (a benignly-named symlink pointing INTO a-plus) is closed by a
#     separate invariant: CHECK 2 REJECTS a pinned .pen that is a symlink outright (`[ -L ]`,
#     lstat, non-traversing), so no symlink target is ever resolved or hashed. Defense in depth
#     with the extractor's own check and the standing agent-level rule.
#   - penPath is read from config.json assuming the canonical extractor-emitted form
#     (`"penPath": "..."`). A non-canonical config.json that this cannot parse -> FATAL.
#
# Usage: pen-integrity.sh <export-dir> [--base <repo-root>]
#   <export-dir>  the design/interaction-model directory holding the exports + export.digest.
#   --base        root for resolving a repo-root-relative penPath (the pinned .pen). Default $PWD.
set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-pen-integrity}"
ALLOW_SKIP="${AUDIT_ALLOW_SKIP:-0}"

emit() { echo "[${AUDIT_TAG}] $*"; }
fatal() { emit "FATAL: $*"; exit 2; }  # hard, non-downgradable: the gate cannot run.

DIR=""
BASE="$PWD"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --base) shift; [ "$#" -gt 0 ] || fatal "--base needs a value"; BASE="$1" ;;
    --base=*) BASE="${1#*=}" ;;
    -h|--help) sed -n '2,84p' "$0"; exit 0 ;;
    --*) fatal "unknown arg: $1" ;;
    *) [ -z "$DIR" ] && DIR="$1" || fatal "unexpected extra arg: $1" ;;
  esac
  shift
done

[ -n "$DIR" ] || fatal "usage: pen-integrity.sh <export-dir> [--base <repo-root>]"
[ -d "$DIR" ] || fatal "export dir not found / not a directory: $DIR"

HERE="$(cd "$(dirname "$0")" && pwd)"
DIGEST_SH="$HERE/pen-digest.sh"
[ -f "$DIGEST_SH" ] || fatal "pen-digest.sh not found next to this gate ($DIGEST_SH)"

# SHA-256 tool for CHECK 2's .pen hash (CHECK 1's hash is pen-digest.sh's own concern).
if command -v shasum >/dev/null 2>&1; then PEN_HASH="shasum -a 256"
elif command -v sha256sum >/dev/null 2>&1; then PEN_HASH="sha256sum"
else fatal "need shasum or sha256sum to hash the pinned .pen (CHECK 2)"; fi

# ---- parse the export.digest envelope (sed; NOT JSON) ------------------------
ENVELOPE="$DIR/export.digest"
[ -f "$ENVELOPE" ] || fatal "no export.digest envelope in $DIR — a §6.2 gate with no recorded digest cannot run (fail-closed)"
[ -s "$ENVELOPE" ] || fatal "export.digest is empty in $DIR (fail-closed)"

# Tolerant of the header's column-aligned form: strip the key + colon + ANY following
# whitespace, so a hand-authored `pen-sha256:     <hex>` parses to the bare value (else the
# padding would poison the hex/path checks with a misleading diagnostic — BH2/CQ1).
env_field() { sed -n "s/^$1:[[:space:]]*//p" "$ENVELOPE" | head -n1; }
REC_FORMAT="$(env_field format)"
REC_CONTENT="$(env_field content-sha256)"
REC_PEN="$(env_field pen-sha256)"
REC_PENPATH="$(env_field pen-path)"
REC_STAMPED="$(env_field stamped)"

# Envelope completeness first: an unknown format or a missing field means we cannot trust our
# reading of the rest (fail-closed). format: pins the schema; stamped: is required provenance.
[ "$REC_FORMAT" = "pen-export-envelope-v0" ] || fatal "export.digest format is '$REC_FORMAT', expected pen-export-envelope-v0 (unknown/unsupported envelope — fail-closed)"
HEX64='^[0-9a-f]{64}$'
[[ "$REC_CONTENT" =~ $HEX64 ]] || fatal "export.digest has no valid 64-hex content-sha256 (unparseable/partial envelope — fail-closed)"
[[ "$REC_PEN" =~ $HEX64 ]] || fatal "export.digest has no valid 64-hex pen-sha256 (older/partial export cannot drive the §6.2 pen-change trigger — fail-closed)"
[ -n "$REC_PENPATH" ] || fatal "export.digest has no pen-path (unparseable/partial envelope — fail-closed)"
[ -n "$REC_STAMPED" ] || fatal "export.digest has no stamped field (incomplete envelope — fail-closed)"

# ---- resolve the pinned penPath from config.json (the authoritative pin, §5) --
CONFIG="$DIR/config.json"
[ -f "$CONFIG" ] || fatal "no config.json in $DIR — cannot resolve the pinned .pen path"
PENPATH="$(sed -n 's/.*"penPath"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$CONFIG" | head -n1)"
[ -n "$PENPATH" ] || fatal "config.json has no parseable penPath (expected canonical \"penPath\": \"...\")"

# ---- a-plus-maxing denylist [NEW-5] — LEXICAL, before any FS access TO PENPATH ----
# (config.json was read above to obtain penPath; this runs before ANY access to the penPath
# or the pinned .pen itself.) Runs on the config penPath AND the recorded pen-path AND their
# base-joined forms, so no channel can smuggle an a-plus path. We never stat/realpath these —
# the check IS what keeps us out of that tree (see LIMITATIONS). Hard FATAL; not downgradable.
lc() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]'; }
for p in "$PENPATH" "$REC_PENPATH" "$BASE/$PENPATH" "$BASE/$REC_PENPATH"; do
  case "$(lc "$p")" in
    *a-plus-maxing*) fatal "penPath resolves under a-plus-maxing ('$p') — denied [NEW-5], never verify against that tree" ;;
  esac
done

# ---- pin consistency: config penPath must equal the recorded pen-path --------
# config.json is digest-covered (a config edit trips CHECK 1 until re-extraction); the envelope
# pen-path is NOT, so this equality is what binds a hand-edited pen-path back to the pin.
[ "$PENPATH" = "$REC_PENPATH" ] || fatal "config.json penPath ('$PENPATH') != export.digest pen-path ('$REC_PENPATH') — stale or tampered pin; re-extract"

# ---- verdict state ----------------------------------------------------------
violations=0
skips=0
pen_changed=0
fail() { emit "FAIL: $*"; violations=$((violations + 1)); }
skipped() {
  if [ "$ALLOW_SKIP" = "1" ]; then
    emit "SKIPPED: $* (allowed via AUDIT_ALLOW_SKIP=1; not gating — .pen declared out-of-repo, §5 repo-residency)"
  else
    emit "SKIPPED: $* (fail-closed: a freshness check that cannot run does not pass — F-008)"
    skips=$((skips + 1))
  fi
}

# ================= CHECK 1 — export integrity =================================
if ! recomputed="$(bash "$DIGEST_SH" "$DIR" 2>/dev/null)"; then
  fatal "pen-digest.sh could not compute the content digest over $DIR (missing export / format invariant) — cannot verify integrity"
fi
if [ "$recomputed" = "$REC_CONTENT" ]; then
  emit "ok: CHECK 1 export integrity — content-sha256 matches ($REC_CONTENT)"
else
  fail "CHECK 1 export integrity — recomputed content digest $recomputed != recorded $REC_CONTENT: an export was hand-edited without re-stamping export.digest (§6.2 check 1)"
fi

# ================= CHECK 2 — pen-change trigger ===============================
# Presupposes a clean integrity state (a build-time gate refuses to run on a FAILed integrity
# check, §6.2); if CHECK 1 failed we do not trust the recorded pen-sha256 either.
if [ "$violations" -gt 0 ]; then
  emit "note: CHECK 2 not evaluated — CHECK 1 integrity failed; re-stamp export.digest, then re-run"
else
  case "$PENPATH" in
    /*) pen_file="$PENPATH" ;;
    *)  pen_file="$BASE/$PENPATH" ;;
  esac
  # Reject a symlinked pin BEFORE any existence/hash (`[ -L ]` = lstat, does NOT traverse):
  # a symlink can retarget the freshness check off the committed bytes, so the target is never
  # resolved or hashed (arch-F2; also closes the symlink-name a-plus evasion). Non-downgradable.
  if [ -L "$pen_file" ]; then
    fatal "pinned .pen must not be a symlink (repo-residency §5): '$pen_file' — a symlink can retarget the freshness check off the committed bytes"
  fi
  if [ ! -f "$pen_file" ]; then
    skipped "CHECK 2 pen-change trigger — pinned .pen not found at '$pen_file' (repo-residency §5): cannot recompute its hash to detect a change"
  else
    cur_pen="$($PEN_HASH "$pen_file" 2>/dev/null | awk '{print $1}')"
    # An empty / non-hex result means shasum could not read the file (perms / IO). "Couldn't
    # hash" must NOT read as "unchanged" (BH1): fail-closed rather than emit a false PEN-CHANGED.
    if [ -z "$cur_pen" ] || ! [[ "$cur_pen" =~ $HEX64 ]]; then
      fatal "could not hash pinned .pen at '$pen_file' (unreadable / IO error) — cannot verify freshness"
    fi
    if [ "$cur_pen" = "$REC_PEN" ]; then
      emit "ok: CHECK 2 pen-change trigger — pinned .pen ciphertext sha256 unchanged since extraction"
    else
      pen_changed=1
      emit "PEN-CHANGED: pinned .pen ciphertext sha256 ($cur_pen) differs from recorded pen-sha256 ($REC_PEN)"
      emit "PEN-CHANGED: a fresh §6.5 drift re-extraction is MANDATORY; wave-close is BLOCKED until §6.5 runs on the current .pen and re-stamps pen-sha256"
    fi
  fi
fi

# ================= verdict ===================================================
# FAIL (a real violation) takes precedence over a fail-closed skip (mirrors audit-helpers.sh).
if [ "$violations" -gt 0 ]; then
  emit "RESULT: FAIL (${violations} integrity violation(s))"
  exit 1
fi
if [ "$skips" -gt 0 ]; then
  emit "RESULT: FATAL (${skips} freshness check(s) could not run — fail-closed)"
  exit 2
fi
if [ "$pen_changed" -eq 1 ]; then
  emit "RESULT: PASS-WITH-PEN-CHANGED (integrity clean; wave-close blocked pending a §6.5 re-extraction)"
  exit 0
fi
emit "RESULT: PASS (exports intact; pinned .pen unchanged)"
exit 0
