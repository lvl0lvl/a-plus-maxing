#!/usr/bin/env bash
# test_pii_scan_scope_artifacts.sh — fixture for the scan-scope hole on the
# maintained-output path (ADR-0021-T0-SCANSCOPE). The scoped operator-NAME scan
# (pii_scan.scan_scoped, identity tokens over the data_bearing subset) must reach
# vault/artifacts/generated/, the dropzone the ADR-0021 re-insertion and ADR-0025
# maintained-output renders land in — else a committed plan render carrying a
# re-inserted REAL name is name-scanned by neither PII hook.
#
# Fully isolated: a temp git repo (mktemp -d) on a feature branch, the hooks
# pointed at it via their *_PROJECT_ROOT / *_SCAN_ROOT env seams, and a SYNTHETIC
# operator-identity config inside the temp tree (no real PII enters the test).
# vault/artifacts/generated/ is gitignored, so each artifact is force-staged
# (git add -f) to enter the scanned set — a plain `git add` no-ops and the hook
# would exit 0 for the WRONG reason (empty staged set, not a clean scan).
#
# Non-tautological: the deny cases (AC-2 commit, AC-3 push) and the allow case
# (AC-4 clean artifact) differ ONLY by the presence of the identity token in an
# equally force-staged file. The empty-staged-set control (case 0) proves the
# deny is content-driven, not an empty-set artifact.
#
# Cases:
#   0 empty staged set                                          -> ALLOW (control)
#   2 force-staged artifact carrying the identity token, commit -> DENY
#   3 same name-bearing artifact in a push range                -> DENY (exit 1)
#   4a clean initials-only artifact, commit                     -> ALLOW
#   4b clean initials-only artifact in a push range             -> ALLOW (exit 0)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMIT_HOOK="$SCRIPT_DIR/../block-pii-commit.sh"
PUSH_HOOK="$SCRIPT_DIR/../pre-push-pii-scan.sh"
# The scan POLICY (scripts.guard.pii_scan) ships with this checkout; import it from
# the real repo root while the staged set + file contents follow the temp repo.
REAL_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
REPO="$TMP/repo"
mkdir -p "$REPO/vault/artifacts/generated" "$REPO/vault/meta"
cd "$REPO"
git init -q; git config user.email t@t.t; git config user.name t
git checkout -q -b feat

# Gitignore the artifacts dropzone + the identity config, mirroring the trunk:
# the dropzone is gitignored (so the in-band vector is `git add -f`), and the
# synthetic config must not auto-stage into the scanned set.
cat > "$REPO/.gitignore" <<'GI'
vault/artifacts/generated/
vault/meta/operator-identity.txt
vault/meta/operator-contact.txt
GI

# SYNTHETIC operator-identity token (one regex per line, the shape pii_scan loads).
# NEVER the real vault/meta/operator-identity.txt value. No contact config is
# seeded, so the trunk-wide contact scan stays empty and a deny can ONLY come from
# this identity token over the data-bearing artifact path.
printf 'Janet Q Testperson\n' > "$REPO/vault/meta/operator-identity.txt"

# A bd-cmd no-op stub: the commit hook would otherwise try a real `bd sync`. There
# is no .beads/*.db in the temp repo so the flush is skipped anyway, but pin it.
printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/bd.sh"; chmod +x "$TMP/bd.sh"

# Seed commit so a push range has a base and HEAD resolves.
git add .gitignore
git commit -q -m "seed"

NAME_ART="vault/artifacts/generated/plan.html"
# Name-bearing render: the identity token re-inserted into the maintained output.
printf '<html><body><h1>Plan for Janet Q Testperson</h1></body></html>\n' > "$REPO/$NAME_ART"
# Clean render: initials-only, no identity token, no contact token (the legitimate
# de-identified artifact this dropzone exists to hold).
CLEAN_ART="vault/artifacts/generated/plan-clean.html"
printf '<html><body><h1>Plan for J.Q.T.</h1></body></html>\n' > "$REPO/$CLEAN_ART"

# ── commit-hook invoker ─────────────────────────────────────────────────────────
commit_invoke() {  # echoes the commit hook's stdout (deny JSON, or empty on allow)
    printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "git commit -m wip" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
        | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" \
          BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" \
          BLOCK_PII_COMMIT_BD_CMD="$TMP/bd.sh" \
          bash "$COMMIT_HOOK"
}

# ── push-hook invoker ───────────────────────────────────────────────────────────
# The pre-push hook scans the COMMIT RANGE (not the index): it needs the artifact
# committed, and reads stdin as "<local_ref> <local_sha> <remote_ref> <remote_sha>".
# A fresh-remote push (remote_sha all-zero) bases the diff on the empty tree, so the
# committed artifact lands in the scanned range. Run from inside the repo (the hook
# resolves its toplevel via git rev-parse).
push_invoke() {  # echoes nothing; returns the hook's exit code
    local sha
    sha=$(git rev-parse HEAD)
    printf 'refs/heads/feat %s refs/heads/feat %s\n' "$sha" "0000000000000000000000000000000000000000" \
        | PRE_PUSH_PII_SCAN_ROOT="$REAL_ROOT" bash "$PUSH_HOOK"
}

# ── Case 0 (control): empty staged set -> ALLOW. Proves the AC-2 deny below is
# content-driven (a non-empty data-bearing scan), not an empty-set artifact. ──────
git reset -q
OUT=$(commit_invoke)
[[ "$OUT" != *'"deny"'* ]] \
    && ok "case0 (control): empty staged set allowed (deny is not empty-set-driven)" \
    || bad "case0: empty staged set unexpectedly denied: $OUT"

# ── Case 2 (AC-2): force-staged name-bearing artifact, commit -> DENY ────────────
git reset -q
git add -f "$NAME_ART"
OUT=$(commit_invoke)
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
  && [[ "$OUT" == *"$NAME_ART"* ]] \
  && [[ "$OUT" == *"operator PII"* ]]; } \
    && ok "case2 (AC-2): name-bearing artifact commit DENIED by the identity scan (names $NAME_ART)" \
    || bad "case2 (AC-2): name-bearing artifact NOT denied at commit (scan-scope hole), got: $OUT"

# ── Case 3 (AC-3): the same name-bearing artifact in a push range -> DENY ─────────
git reset -q
git add -f "$NAME_ART"
git commit -q -m "name-bearing render"
push_invoke >/tmp/_pps_out 2>/tmp/_pps_err
RC=$?
{ [[ $RC -eq 1 ]] && grep -q "$NAME_ART" /tmp/_pps_err; } \
    && ok "case3 (AC-3): name-bearing artifact in push range DENIED (exit 1, names $NAME_ART)" \
    || bad "case3 (AC-3): name-bearing artifact NOT denied at push (rc=$RC), err: $(cat /tmp/_pps_err)"
# Reset HEAD back to the seed so the clean-case push range carries only the clean art.
git reset -q --hard HEAD~1

# ── Case 4a (AC-4): clean initials-only artifact, commit -> ALLOW ────────────────
git reset -q
git add -f "$CLEAN_ART"
OUT=$(commit_invoke)
[[ "$OUT" != *'"deny"'* ]] \
    && ok "case4a (AC-4): clean initials-only artifact commit ALLOWED (no over-block)" \
    || bad "case4a (AC-4): clean artifact wrongly denied at commit (over-block), got: $OUT"

# ── Case 4b (AC-4): the same clean artifact in a push range -> ALLOW (exit 0) ─────
git reset -q
git add -f "$CLEAN_ART"
git commit -q -m "clean render"
push_invoke >/tmp/_pps_out 2>/tmp/_pps_err
RC=$?
[[ $RC -eq 0 ]] \
    && ok "case4b (AC-4): clean initials-only artifact in push range ALLOWED (exit 0)" \
    || bad "case4b (AC-4): clean artifact wrongly denied at push (rc=$RC), err: $(cat /tmp/_pps_err)"

echo
echo "test_pii_scan_scope_artifacts: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
