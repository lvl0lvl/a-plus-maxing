#!/usr/bin/env bash
# test_reinsert_out_deny.sh — the crown-jewel "0 real PII in any committed file" probe for
# the deterministic re-insertion OUT pass (ADR-0021-T1). The OUT pass RETURNS a name-bearing
# string (the de-identified render with the real operator name re-inserted) for a
# confirmable-gitignored target; the CALLER (ADR-0025-T1) writes it to the gitignored dropzone.
# This fixture proves the LOCAL-FEATURE-WORKS-BUT-COMMIT-DENIED contract: the actual output of
# `reinsert_out` (PRODUCED by invoking the real module, not a hand-faked string), force-staged
# into the scanned set, is DENIED at commit AND pre-push by the PII hooks (the T0-SCANSCOPE
# coverage over vault/artifacts/generated/). The empty-staged-set control (case 0) proves the
# deny is content-driven, not an empty-set artifact.
#
# MIRRORS .claude/hooks/tests/test_pii_scan_scope_artifacts.sh (cases 0/2/3): a temp git repo
# on a feature branch, the hooks pointed at it via their *_PROJECT_ROOT / *_SCAN_ROOT seams, a
# SYNTHETIC operator-identity config inside the temp tree (NEVER real PII), git add -f
# force-staging the gitignored artifact into the scanned set, the JSON-on-stdin envelope, and a
# bd-cmd no-op stub. Run BY HAND (.claude/hooks/tests/*.sh is NOT auto-discovered by
# scripts/tests/run-all-tests.sh — the T0-SCANSCOPE precedent).
#
# Cases:
#   0  empty staged set                                                  -> ALLOW (control)
#   2  force-staged reinsert_out OUTPUT carrying the identity token       -> DENY (commit)
#   3  the same name-bearing artifact in a push range                     -> DENY (exit 1)
#   4a clean initials-only reinsert_out output (fail-closed/tracked path)  -> ALLOW (commit)
#   4b the same clean artifact in a push range                            -> ALLOW (exit 0)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMIT_HOOK="$SCRIPT_DIR/../block-pii-commit.sh"
PUSH_HOOK="$SCRIPT_DIR/../pre-push-pii-scan.sh"
# The real repo: the scan POLICY (scripts.guard.pii_scan) + the reinsert_out module ship here;
# import them from the real root while the staged set + file contents follow the temp repo.
REAL_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PY="$REAL_ROOT/.venv/bin/python"

PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

# The high-entropy SYNTHETIC operator full name (the AC-1/AC-2 oracle; matches the pytest
# fixture). NEVER the real vault/meta/operator-identity.txt value.
SYN_NAME="Zxqvarn Wolthrip"

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
REPO="$TMP/repo"
mkdir -p "$REPO/vault/artifacts/generated" "$REPO/vault/meta" "$REPO/vault/scaffold/filled"
cd "$REPO"
git init -q; git config user.email t@t.t; git config user.name t
git checkout -q -b feat

# Gitignore the artifacts dropzone + the scaffold/filled profile + the identity config,
# mirroring the trunk. The dropzone + filled profile are gitignored (so the in-band vector is
# `git add -f`); the synthetic config must not auto-stage into the scanned set.
cat > "$REPO/.gitignore" <<'GI'
vault/artifacts/generated/
vault/scaffold/filled/
vault/meta/operator-identity.txt
vault/meta/operator-contact.txt
GI

# SYNTHETIC operator-identity token (one regex per line, the shape pii_scan loads). The first
# + last name, so a re-inserted "Zxqvarn Wolthrip" trips the scan. No contact config is seeded,
# so a deny can ONLY come from this identity token over the data-bearing artifact path.
printf 'Zxqvarn|Wolthrip\n' > "$REPO/vault/meta/operator-identity.txt"

# The SYNTHETIC gitignored identity profile the re-insertion reads the full name from (the
# `# Operator Profile — <full name>` title line). NEVER the real filled profile.
printf '# Operator Profile — %s\n\n- **Age:** 44\n- **Current status:** recovering\n' "$SYN_NAME" \
    > "$REPO/vault/scaffold/filled/operator-profile.md"

# The produced HTML (initials placeholder, handout header shape) — the input to reinsert_out.
PRODUCED_HTML="<html><body><div class='hd-head-block'><div class='hd-status'>Patient ZW · age band 40s · issue status recovering</div></div></body></html>"

# A bd-cmd no-op stub: the commit hook would otherwise try a real bd sync. No .beads/*.db in the
# temp repo so the flush is skipped anyway, but pin it.
printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/bd.sh"; chmod +x "$TMP/bd.sh"

# Seed commit so a push range has a base and HEAD resolves.
git add .gitignore
git commit -q -m "seed"

# ── PRODUCE the artifacts by invoking the REAL reinsert_out (not hand-faked strings) ─────────
# Case 2/3 (DENY): a confirmable-gitignored target -> reinsert_out returns the name-bearing
# string. Write it to the gitignored dropzone (what the ADR-0025-T1 caller does).
NAME_ART="vault/artifacts/generated/plan.html"
PYTHONPATH="$REAL_ROOT" "$PY" - "$REPO" "$PRODUCED_HTML" > "$REPO/$NAME_ART" <<'PYEOF'
import sys
from pathlib import Path
from scripts.plan.reinsert_out import reinsert_out
repo, html = sys.argv[1], sys.argv[2]
target = Path(repo) / "vault" / "artifacts" / "generated" / "plan.html"
profile = (Path(repo) / "vault" / "scaffold" / "filled" / "operator-profile.md",)
sys.stdout.write(reinsert_out(html, target, _profile_paths=profile, _repo_root=Path(repo)))
PYEOF
grep -q "$SYN_NAME" "$REPO/$NAME_ART" \
    && ok "produced: reinsert_out output over a gitignored target carries the full name" \
    || bad "produced: reinsert_out output did NOT carry the full name (the feature is broken)"

# Case 4a/4b (ALLOW): a TRACKED target -> reinsert_out fails closed to the initials-only string.
CLEAN_ART="vault/artifacts/generated/plan-clean.html"
PYTHONPATH="$REAL_ROOT" "$PY" - "$REPO" "$PRODUCED_HTML" > "$REPO/$CLEAN_ART" <<'PYEOF'
import sys
from pathlib import Path
from scripts.plan.reinsert_out import reinsert_out
repo, html = sys.argv[1], sys.argv[2]
tracked_target = Path(repo) / "vault" / "report.html"  # not under the gitignored dropzone
profile = (Path(repo) / "vault" / "scaffold" / "filled" / "operator-profile.md",)
sys.stdout.write(reinsert_out(html, tracked_target, _profile_paths=profile, _repo_root=Path(repo)))
PYEOF
{ ! grep -q "$SYN_NAME" "$REPO/$CLEAN_ART"; } \
    && ok "produced: reinsert_out output over a TRACKED target is initials-only (name absent)" \
    || bad "produced: the full name LEAKED onto the fail-closed/tracked output"

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
push_invoke() {  # echoes nothing; returns the hook's exit code
    local sha
    sha=$(git rev-parse HEAD)
    printf 'refs/heads/feat %s refs/heads/feat %s\n' "$sha" "0000000000000000000000000000000000000000" \
        | PRE_PUSH_PII_SCAN_ROOT="$REAL_ROOT" bash "$PUSH_HOOK"
}

# ── Case 0 (control): empty staged set -> ALLOW. Proves the case-2 deny is content-driven. ───
git reset -q
OUT=$(commit_invoke)
[[ "$OUT" != *'"deny"'* ]] \
    && ok "case0 (control): empty staged set allowed (deny is not empty-set-driven)" \
    || bad "case0: empty staged set unexpectedly denied: $OUT"

# ── Case 2 (DENY): the name-bearing reinsert_out output, force-staged, commit -> DENY ────────
git reset -q
git add -f "$NAME_ART"
OUT=$(commit_invoke)
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
  && [[ "$OUT" == *"$NAME_ART"* ]] \
  && [[ "$OUT" == *"operator PII"* ]]; } \
    && ok "case2 (DENY): name-bearing reinsert_out output DENIED at commit (names $NAME_ART)" \
    || bad "case2 (DENY): name-bearing output NOT denied at commit (scan-scope hole), got: $OUT"

# ── Case 3 (push DENY): the same name-bearing artifact in a push range -> DENY (exit 1) ──────
git reset -q
git add -f "$NAME_ART"
git commit -q -m "name-bearing render"
push_invoke >/tmp/_rio_pps_out 2>/tmp/_rio_pps_err
RC=$?
{ [[ $RC -eq 1 ]] && grep -q "$NAME_ART" /tmp/_rio_pps_err; } \
    && ok "case3 (push DENY): name-bearing artifact in push range DENIED (exit 1, names $NAME_ART)" \
    || bad "case3 (push DENY): name-bearing artifact NOT denied at push (rc=$RC), err: $(cat /tmp/_rio_pps_err)"
# Reset HEAD back to the seed so the clean-case push range carries only the clean art.
git reset -q --hard HEAD~1

# ── Case 4a (ALLOW): the clean initials-only reinsert_out output, commit -> ALLOW ────────────
git reset -q
git add -f "$CLEAN_ART"
OUT=$(commit_invoke)
[[ "$OUT" != *'"deny"'* ]] \
    && ok "case4a (ALLOW): clean initials-only reinsert_out output ALLOWED at commit (no over-block)" \
    || bad "case4a (ALLOW): clean artifact wrongly denied at commit (over-block), got: $OUT"

# ── Case 4b (ALLOW): the same clean artifact in a push range -> ALLOW (exit 0) ───────────────
git reset -q
git add -f "$CLEAN_ART"
git commit -q -m "clean render"
push_invoke >/tmp/_rio_pps_out 2>/tmp/_rio_pps_err
RC=$?
[[ $RC -eq 0 ]] \
    && ok "case4b (ALLOW): clean initials-only artifact in push range ALLOWED (exit 0)" \
    || bad "case4b (ALLOW): clean artifact wrongly denied at push (rc=$RC), err: $(cat /tmp/_rio_pps_err)"

echo
echo "test_reinsert_out_deny: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
