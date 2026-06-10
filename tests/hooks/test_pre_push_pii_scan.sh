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
#   3lv      NON-operator gmail in a pushed file -> exit 0 (config-driven)
#   scope    identity in data-bearing path -> exit 1; identity in prose -> exit 0
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
commitfile "tests/store/test_fixture.py" 'PLANT = {"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", "source": "manual", "value": 55}'
invoke; RC=$?
[[ $RC -eq 0 ]] && ok "store-line in tests/ -> exit 0 (synthetic fixture)" \
    || bad "tests/ fixture wrongly blocked (partition missing), rc=$RC ($(cat "$TMP/err"))"

# ── 3lv: NON-operator gmail -> exit 0 (config-driven, no generic flood) ─────────
commitfile "docs/fixture.md" "example fixture address: alice@gmail.com"
invoke; RC=$?
[[ $RC -eq 0 ]] && ok "non-operator gmail -> exit 0 (config-driven)" \
    || bad "non-operator gmail wrongly blocked (generic pattern back?), rc=$RC ($(cat "$TMP/err"))"

# ── scope (i): identity token in plain prose -> exit 0 (data-bearing only) ──────
commitfile "docs/prose.md" "Session note: Walter McGivney reviewed the plan."
invoke; RC=$?
[[ $RC -eq 0 ]] && ok "scope (i) identity in prose -> exit 0 (provenance)" \
    || bad "scope (i) identity in prose wrongly blocked, rc=$RC ($(cat "$TMP/err"))"

# ── scope (ii): identity token in a data-bearing path -> exit 1 ─────────────────
commitfile "vault/dna/raw/sample.json" '{"note":"reviewed by Walter McGivney"}'
invoke; RC=$?
{ [[ $RC -ne 0 ]] && grep -q "vault/dna/raw/sample.json" "$TMP/err"; } \
    && ok "scope (ii) identity in data-bearing path -> blocked + named" \
    || bad "scope (ii) expected block naming the dna path, got rc=$RC ($(cat "$TMP/err"))"
git -C "$REPO" reset -q HEAD~1; rm -f "$REPO/vault/dna/raw/sample.json"

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
