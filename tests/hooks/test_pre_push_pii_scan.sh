#!/usr/bin/env bash
# test_pre_push_pii_scan.sh — smoke tests for pre-push-pii-scan.sh (bead dv3).
#
# The git pre-push PII backstop. Fully isolated: each case runs the hook inside a
# scratch git repo (the hook resolves its own toplevel via git rev-parse) with
# PRE_PUSH_PII_SCAN_ROOT pointing the scanner import at the REAL repo. The hook's
# contract is git's pre-push stdin ("<local_ref> <local_sha> <remote_ref>
# <remote_sha>" per ref) + exit code (0 allow / non-0 block), so every assertion
# keys on the EXIT CODE — the opposite of the PreToolUse suites' deny-JSON keying.
#
# Cases:
#   clean    clean pushed range -> exit 0
#   contact  operator-contact token in a pushed file -> exit 1, names the file
#   struct   structural store-line in a pushed file -> exit 1
#   fixture  store-line in tests/ -> exit 0; operator contact in tests/ -> exit 1 (TEST-1)
#   path     token-free vault/store/ file -> exit 1 (API-1 path denial)
#   3lv      NON-operator gmail in a pushed file -> exit 0 (config-driven)
#   scope    identity in data-bearing path -> exit 1; identity in prose -> exit 0
#   exist    existing-ref update: leak in range -> exit 1; empty range -> exit 0 (TEST-3)
#   multi    multi-ref stdin, one leaking ref -> exit 1 (TEST-3)
#   delete   ref-deletion push (zero local sha) -> exit 0
#   failsafe unimportable scan root -> exit 1 (fail-closed)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$SCRIPT_DIR/../../.claude/hooks/pre-push-pii-scan.sh"
REAL_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ZERO=0000000000000000000000000000000000000000

PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
REPO="$TMP/repo"
mkdir -p "$REPO"
cd "$REPO"
git init -q; git config user.email t@t.t; git config user.name t; git checkout -q -b feat

cat > "$REPO/.gitignore" <<EOF
vault/store/
vault/scaffold/filled/
vault/dna/raw/
vault/meta/operator-identity.txt
vault/meta/operator-contact.txt
EOF
mkdir -p "$REPO/vault/meta"
printf 'Walter|McGivney\n' > "$REPO/vault/meta/operator-identity.txt"
OPERATOR_CONTACT="op.user@gmail.com"
printf 'op\\.user@gmail\\.com\n' > "$REPO/vault/meta/operator-contact.txt"
git add .gitignore; git commit -qm "seed"

# invoke(): commit the staged tree, feed the hook one pre-push stdin line pushing
# HEAD to a new remote ref (remote sha ZERO -> empty-tree base: the whole snapshot
# is the range). Echoes nothing; returns the hook's exit code.
invoke() {
    local sha
    sha=$(git -C "$REPO" rev-parse HEAD)
    printf 'refs/heads/feat %s refs/heads/feat %s\n' "$sha" "$ZERO" \
        | (cd "$REPO" && PRE_PUSH_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK" 2>"$TMP/err")
}

commitfile() {  # $1 = relpath ; $2 = contents ; commits (force-add past gitignore)
    mkdir -p "$REPO/$(dirname "$1")"
    printf '%s' "$2" > "$REPO/$1"
    git -C "$REPO" add -f "$1"
    git -C "$REPO" commit -qm "add $1"
}

# ── clean: PII-free pushed range -> exit 0 ──────────────────────────────────────
commitfile "docs/notes.md" "plain notes, nothing sensitive"
invoke; RC=$?
[[ $RC -eq 0 ]] && ok "clean range -> exit 0" || bad "clean range expected 0, got $RC ($(cat "$TMP/err"))"

# ── contact: operator-contact token in a pushed file -> exit 1 + named ──────────
commitfile "docs/leak.md" "reach the operator at $OPERATOR_CONTACT"
invoke; RC=$?
{ [[ $RC -ne 0 ]] && grep -q "docs/leak.md" "$TMP/err"; } \
    && ok "operator contact in range -> blocked + file named" \
    || bad "contact leak expected block naming docs/leak.md, got rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/docs/leak.md"

# ── struct: structural store-line in a pushed file -> exit 1 ────────────────────
commitfile "docs/dump.md" '{"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", "source": "manual", "value": 55}'
invoke; RC=$?
[[ $RC -ne 0 ]] && ok "structural store-line in range -> blocked" \
    || bad "structural leak expected block, got rc=$RC"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/docs/dump.md"

# ── fixture partition (dv3): the SAME store-line in tests/ -> exit 0 ────────────
# Each case resets so later allow-cases assert over only their own plant (TEST-5).
commitfile "tests/store/test_fixture.py" 'PLANT = {"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", "source": "manual", "value": 55}'
invoke; RC=$?
[[ $RC -eq 0 ]] && ok "store-line in tests/ -> exit 0 (synthetic fixture)" \
    || bad "tests/ fixture wrongly blocked (partition missing), rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/tests/store/test_fixture.py"

# ── fixture partition deny-leg (TEST-1): operator CONTACT in tests/ -> exit 1 ────
# The partition drops STRUCTURAL patterns for tests/, NOT the token scans. A real
# operator contact in a tests/ path is still a leak and must block at the backstop.
commitfile "tests/store/test_leak.py" "CONTACT = '$OPERATOR_CONTACT'"
invoke; RC=$?
{ [[ $RC -ne 0 ]] && grep -q "tests/store/test_leak.py" "$TMP/err"; } \
    && ok "operator contact in tests/ -> blocked + named (tokens still run)" \
    || bad "contact in tests/ NOT blocked at backstop (token scan dropped), rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/tests/store/test_leak.py"

# ── path denial (API-1): a force-added vault/store/ file with NO token -> exit 1 ─
# A filled store/scaffold file is operator data by LOCATION; the backstop must deny
# it regardless of token hits (mirrors the commit hook's conditions 1+2).
commitfile "vault/store/entries.ndjson" '{"plain":"no token here, just location"}'
invoke; RC=$?
{ [[ $RC -ne 0 ]] && grep -q "vault/store/entries.ndjson" "$TMP/err"; } \
    && ok "path denial: token-free vault/store/ file -> blocked + named (API-1)" \
    || bad "path denial: vault/store/ file NOT blocked, rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/vault/store/entries.ndjson"

# ── 3lv: NON-operator gmail -> exit 0 (config-driven, no generic flood) ─────────
commitfile "docs/fixture.md" "example fixture address: alice@gmail.com"
invoke; RC=$?
[[ $RC -eq 0 ]] && ok "non-operator gmail -> exit 0 (config-driven)" \
    || bad "non-operator gmail wrongly blocked (generic pattern back?), rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/docs/fixture.md"

# ── scope (i): identity token in plain prose -> exit 0 (data-bearing only) ──────
commitfile "docs/prose.md" "Session note: Walter McGivney reviewed the plan."
invoke; RC=$?
[[ $RC -eq 0 ]] && ok "scope (i) identity in prose -> exit 0 (provenance)" \
    || bad "scope (i) identity in prose wrongly blocked, rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/docs/prose.md"

# ── scope (ii): identity token in a data-bearing path -> exit 1 ─────────────────
commitfile "vault/dna/raw/sample.json" '{"note":"reviewed by Walter McGivney"}'
invoke; RC=$?
{ [[ $RC -ne 0 ]] && grep -q "vault/dna/raw/sample.json" "$TMP/err"; } \
    && ok "scope (ii) identity in data-bearing path -> blocked + named" \
    || bad "scope (ii) expected block naming the dna path, got rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/vault/dna/raw/sample.json"

# ── existing-ref update (TEST-3): scan only the pushed RANGE, not all history ────
# The dominant production push shape: remote_sha is a real prior commit. A leak in
# the new range blocks; the same leak OUTSIDE the range (already-pushed history) is
# not re-scanned (negative placement).
git -C "$REPO" commit -q --allow-empty -m "prior pushed commit"
PRIOR=$(git -C "$REPO" rev-parse HEAD)
commitfile "docs/new-leak.md" "contact $OPERATOR_CONTACT"
HEAD_SHA=$(git -C "$REPO" rev-parse HEAD)
printf 'refs/heads/feat %s refs/heads/feat %s\n' "$HEAD_SHA" "$PRIOR" \
    | (cd "$REPO" && PRE_PUSH_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK" 2>"$TMP/err"); RC=$?
{ [[ $RC -ne 0 ]] && grep -q "docs/new-leak.md" "$TMP/err"; } \
    && ok "existing-ref update: leak in pushed range -> blocked" \
    || bad "existing-ref update: leak in range NOT blocked, rc=$RC ($(cat "$TMP/err"))"
# Inverse: the SAME commit pushed as an already-up-to-date range (base==tip) is empty.
printf 'refs/heads/feat %s refs/heads/feat %s\n' "$HEAD_SHA" "$HEAD_SHA" \
    | (cd "$REPO" && PRE_PUSH_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK" 2>"$TMP/err"); RC=$?
[[ $RC -eq 0 ]] && ok "existing-ref: empty range (base==tip) -> exit 0 (out-of-range not scanned)" \
    || bad "existing-ref empty range expected 0, got $RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q --hard "$PRIOR" 2>/dev/null; rm -f "$REPO/docs/new-leak.md"

# ── multi-ref stdin (TEST-3): one clean ref + one leaking ref -> exit 1 ──────────
commitfile "docs/multi-leak.md" "contact $OPERATOR_CONTACT"
LEAK_SHA=$(git -C "$REPO" rev-parse HEAD)
git -C "$REPO" branch -q clean-branch "$PRIOR" 2>/dev/null || true
CLEAN_SHA=$(git -C "$REPO" rev-parse "$PRIOR")
printf 'refs/heads/clean %s refs/heads/clean %s\nrefs/heads/feat %s refs/heads/feat %s\n' \
    "$CLEAN_SHA" "$ZERO" "$LEAK_SHA" "$ZERO" \
    | (cd "$REPO" && PRE_PUSH_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK" 2>"$TMP/err"); RC=$?
[[ $RC -ne 0 ]] && ok "multi-ref stdin: one leaking ref among two -> blocked" \
    || bad "multi-ref stdin: leaking ref NOT blocked, rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q --hard "$PRIOR" 2>/dev/null; rm -f "$REPO/docs/multi-leak.md"

# ── delete: ref-deletion push (zero local sha) -> exit 0 ────────────────────────
printf 'refs/heads/feat %s refs/heads/feat %s\n' "$ZERO" "$(git -C "$REPO" rev-parse HEAD)" \
    | (cd "$REPO" && PRE_PUSH_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK" 2>"$TMP/err")
RC=$?
[[ $RC -eq 0 ]] && ok "ref-deletion push -> exit 0" || bad "delete push expected 0, got $RC"

# ── failsafe: unimportable scan root -> exit 1 (fail-closed) ────────────────────
BADROOT="$TMP/no-scanner"; mkdir -p "$BADROOT"
sha=$(git -C "$REPO" rev-parse HEAD)
printf 'refs/heads/feat %s refs/heads/feat %s\n' "$sha" "$ZERO" \
    | (cd "$REPO" && PRE_PUSH_PII_SCAN_ROOT="$BADROOT" bash "$HOOK" 2>"$TMP/err")
RC=$?
[[ $RC -ne 0 ]] && ok "unimportable scan root -> blocked (fail-closed)" \
    || bad "fail-closed expected block on scan import error, got rc=$RC"

echo
echo "test_pre_push_pii_scan: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
