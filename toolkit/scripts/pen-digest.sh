#!/usr/bin/env bash
# toolkit/scripts/pen-digest.sh — compute the §5 Interaction-Model export digest.
#
# The design-process-overhaul spec (§5) defines the export CONTENT digest as a SHA-256 over
# the canonicalized concatenation of the export set. This is the plain-bash computation of
# that content digest — the value pen-extract stamps as the `content-sha256` field of the
# export.digest envelope (§5 / architect-F3) and the §6.2 export-integrity gate
# (scripts/pen-integrity.sh) recomputes. This script's contract is UNCHANGED from Phase 1a:
# it emits ONLY the bare 64-char content hash; the envelope wraps that value, it does not
# replace this output. tests/test-pen-lint.sh PROVES the committed content-sha256 recomputes
# from good/ AND that a one-byte edit to any export changes it.
#
# CANONICALIZATION RULE (v0 — this IS the format; keep it byte-stable):
#   1. File set + fixed order (§5, amended 2026-07-02): index.md, then each machine.*.json
#      (C-locale sorted by filename), then wiring-manifest.json, retired-wireids.txt,
#      config.json, exceptions.json. exceptions.json IS in the digest set — the §5 list was
#      amended to include it (F-C's digest coverage of the res-3 sign-off store was the
#      intended design; the earlier §5 omission was the spec inconsistency, now fixed).
#   2. "sorted keys" is an AUTHORING invariant: the extractor emits every JSON export with
#      object keys in sorted order (fixtures are authored that way). This script does NOT
#      re-sort — plain bash cannot reliably canonicalise JSON key order — it relies on the
#      emitted form and a key-reorder hand-edit therefore CHANGES the digest (detected).
#   3. "normalized whitespace": each line has trailing whitespace stripped; every export
#      file MUST end with exactly one trailing newline (format invariant) so file
#      boundaries in the concatenation are unambiguous. This script ENFORCES the invariant
#      (T-04): a file with no trailing newline, or with a blank final line, is FATAL.
#   4. digest = SHA-256 (shasum, or sha256sum where shasum is absent) of the normalized
#      concatenation, lower-case hex, no trailing text.
#
# Exit: prints the 64-char hex digest on stdout and exits 0; FATAL (exit 2) if the export
#       dir / any required file is missing, a file violates the trailing-newline invariant,
#       or no SHA-256 tool is available (a digest that cannot be computed is not clean).
set -uo pipefail

DIR="${1:-}"
[ -n "$DIR" ] || { echo "pen-digest: FATAL — usage: pen-digest.sh <export-dir>" >&2; exit 2; }
[ -d "$DIR" ] || { echo "pen-digest: FATAL — not a directory: $DIR" >&2; exit 2; }

files=()
[ -f "$DIR/index.md" ] || { echo "pen-digest: FATAL — missing index.md in $DIR" >&2; exit 2; }
files+=("$DIR/index.md")

mfound=0
while IFS= read -r m; do [ -n "$m" ] && { files+=("$m"); mfound=1; }; done \
  < <(LC_ALL=C find "$DIR" -maxdepth 1 -name 'machine.*.json' 2>/dev/null | LC_ALL=C sort)
[ "$mfound" -eq 1 ] || { echo "pen-digest: FATAL — no machine.*.json in $DIR" >&2; exit 2; }

for f in wiring-manifest.json retired-wireids.txt config.json exceptions.json; do
  [ -f "$DIR/$f" ] || { echo "pen-digest: FATAL — missing $f in $DIR" >&2; exit 2; }
  files+=("$DIR/$f")
done

# Enforce the exactly-one-trailing-newline invariant the digest relies on (T-04). A file
# with no trailing newline would merge into the next file at the boundary; a blank final
# line would shift bytes — either makes the digest silently spacing-sensitive. FATAL both.
for f in "${files[@]}"; do
  bytes=$(wc -c <"$f")
  if [ "$bytes" -eq 0 ]; then
    echo "pen-digest: FATAL — $f is empty (needs exactly one trailing newline)" >&2; exit 2
  fi
  last=$(tail -c1 "$f" | od -An -tx1 | tr -dc '0-9a-f')
  if [ "$last" != "0a" ]; then
    echo "pen-digest: FATAL — $f lacks a trailing newline (format invariant)" >&2; exit 2
  fi
  if [ "$bytes" -ge 2 ]; then
    prev=$(tail -c2 "$f" | head -c1 | od -An -tx1 | tr -dc '0-9a-f')
    if [ "$prev" = "0a" ]; then
      echo "pen-digest: FATAL — $f has >1 trailing newline (format invariant: exactly one)" >&2; exit 2
    fi
  fi
done

# Resolve a SHA-256 tool up front (T-14): shasum (BSD/macOS), else sha256sum (GNU).
if command -v shasum >/dev/null 2>&1; then HASH="shasum -a 256"
elif command -v sha256sum >/dev/null 2>&1; then HASH="sha256sum"
else echo "pen-digest: FATAL — need shasum or sha256sum to compute the digest" >&2; exit 2; fi

# strip trailing whitespace per line; sed emits each line \n-terminated. With the
# trailing-newline invariant this yields an unambiguous byte stream to hash.
LC_ALL=C sed -e 's/[[:space:]]*$//' "${files[@]}" | $HASH | awk '{print $1}'
