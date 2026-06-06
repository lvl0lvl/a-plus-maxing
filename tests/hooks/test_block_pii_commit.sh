#!/usr/bin/env bash
# test_block_pii_commit.sh — smoke tests for block-pii-commit.sh (ADR-0005-T1).
#
# The trunk content-scan trust boundary. Fully isolated: BLOCK_PII_COMMIT_PROJECT_ROOT
# points the hook at a temp git repo; BLOCK_PII_COMMIT_PII_SCAN_ROOT points the hook's
# scanner import at a chosen root (a stub for the SEC-01(b) reuse proof, an unimportable
# dir for the fail-closed proof, unset → the real scripts/guard/pii_scan.py).
#
# Mirrors test_block_ungated_vault_write.sh: PASS/FAIL counters, an invoke() stdin-payload
# helper, *_PROJECT_ROOT temp-repo isolation. Every block/allow assertion is keyed on the
# observable deny-JSON on STDOUT (block = `"permissionDecision":"deny"`; allow = no deny),
# NEVER on exit code — this PreToolUse hook exits 0 on both block and allow.
#
# ONE shared filled-scaffold-value path constant (SCAFFOLD_VALUE) drives the .gitignore
# exclusion (AC-1), the negative-placement case (AC-3), and the forced-add block (AC-4) so
# the three restatements cannot drift (Fix 4).
#
# Cases:
#   AC-1   .gitignore ignores the filled-scaffold-value path (git check-ignore exit 0)
#   AC-3   negative placement: scaffold value + store file NOT in git ls-files
#   AC-2/5 clean staged tree -> allow (meaningful only with the SEC-01(b) reuse proof)
#   AC-4   staged filled-scaffold value (git add -f) -> deny, names offending file
#   AC-6   staged vault/store/ file (git add -f) -> deny
#   AC-5f  planted tracked-file PII token (incl. non-canonical-case) -> deny via scan, names file
#   TOCTOU staged file absent from HEAD -> deny (git diff --cached, not git ls-files)
#   scoped-identity (i)  name in non-data-bearing prose -> allow (provenance)
#   scoped-identity (ii) name in a data-bearing path    -> deny (identity leak)
#   fail-closed scan invocation errors with token staged -> deny (default-deny)
#   SEC-01(b) stub scan returns 0 + writes sentinel -> allow AND sentinel present (reuse proof)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$SCRIPT_DIR/../../.claude/hooks/block-pii-commit.sh"
REAL_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ONE shared filled-scaffold-value path constant (Fix 4): the .gitignore exclusion the
# hook + real .gitignore carry, the hook's condition-1 matcher, and AC-1/AC-3/AC-4 all use
# this same representative value. The glob the .gitignore excludes is its parent dir.
SCAFFOLD_VALUE="vault/scaffold/filled/value-001.json"
SCAFFOLD_PREFIX="vault/scaffold/filled/"   # the .gitignore exclusion pattern (matches the hook's identifier)
STORE_FILE="vault/store/entries.ndjson"

PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

TMP="$(mktemp -d)"
trap 'cd /; rm -rf "$TMP"' EXIT
REPO="$TMP/repo"
mkdir -p "$REPO"
cd "$REPO"
git init -q; git config user.email t@t.t; git config user.name t; git checkout -q -b feat

# Seed the scratch repo's .gitignore with the SAME exclusions this task adds to the real
# repo-root .gitignore: the store (ADR-0002-T1) + the filled-scaffold-value glob (this task),
# driven by the one shared constant.
cat > "$REPO/.gitignore" <<EOF
vault/store/
$SCAFFOLD_PREFIX
vault/dna/raw/
vault/meta/operator-identity.txt
EOF
git add .gitignore; git commit -q -m "seed gitignore"

# Seed the operator-identity config so the hook's relative DEFAULT_IDENTITY_CONFIG
# (vault/meta/operator-identity.txt, resolved against the hook's cwd = $REPO) loads
# the name tokens — letting the scoped-identity cases exercise the REAL identity scan.
mkdir -p "$REPO/vault/meta"
printf 'Walter|McGivney\n' > "$REPO/vault/meta/operator-identity.txt"

# invoke(): build the stdin JSON, run the hook against the scratch repo. PROJECT_ROOT
# is the scratch repo (for staged-file detection); the scanner root is pointed at the
# REAL repo so `from scripts.guard.pii_scan import scan` resolves to the real scanner
# (the scratch repo carries no scripts/). The stub / fail-closed cases override
# BLOCK_PII_COMMIT_PII_SCAN_ROOT inline.
invoke() {  # $1 = command string ; echoes hook stdout
    printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "$1" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
        | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK"
}

mkfile() {  # $1 = relpath ; $2 = contents
    mkdir -p "$REPO/$(dirname "$1")"
    printf '%s' "$2" > "$REPO/$1"
}

# ── AC-1: .gitignore ignores the filled-scaffold-value path ────────────────────
git -C "$REPO" check-ignore "$SCAFFOLD_VALUE" >/dev/null 2>&1 \
    && ok "AC-1 git check-ignore $SCAFFOLD_VALUE exit 0" \
    || bad "AC-1 scaffold value not ignored by scratch .gitignore"

# ── AC-3: negative placement — scaffold value + store file NOT in tracked set ───
mkfile "$SCAFFOLD_VALUE" '{"item":"x"}'
mkfile "$STORE_FILE" '{"item":"x"}'
git -C "$REPO" add -A >/dev/null 2>&1   # honors .gitignore; should add neither
LISTED=$(git -C "$REPO" ls-files -- "$SCAFFOLD_VALUE" "$STORE_FILE")
[[ -z "$LISTED" ]] \
    && ok "AC-3 negative placement: 0 of {scaffold,store} in git ls-files" \
    || bad "AC-3 expected 0 tracked, got: $LISTED"
git -C "$REPO" reset -q
rm -f "$REPO/$SCAFFOLD_VALUE" "$REPO/$STORE_FILE"

# ── AC-2 / AC-5 pass-direction: clean staged tree -> allow ─────────────────────
mkfile "docs/notes.md" "Plain notes, no PII, no scaffold value."
git -C "$REPO" add docs/notes.md
OUT=$(invoke "git commit -m 'docs'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "AC-2/AC-5 clean staged tree -> allow (no-deny stdout)" \
    || bad "AC-2/AC-5 unexpected deny on clean tree: $OUT"
git -C "$REPO" reset -q

# ── AC-4: staged filled-scaffold value (forced past .gitignore) -> deny + name ─
mkfile "$SCAFFOLD_VALUE" '{"item":"weight","value":80}'
git -C "$REPO" add -f "$SCAFFOLD_VALUE"
OUT=$(invoke "git commit -m 'oops scaffold'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"$SCAFFOLD_VALUE"* ]]; } \
    && ok "AC-4 staged scaffold value DENIED + offending file named" \
    || bad "AC-4 expected deny naming $SCAFFOLD_VALUE, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/$SCAFFOLD_VALUE"

# ── AC-6: staged vault/store/ file -> deny ─────────────────────────────────────
mkfile "$STORE_FILE" '{"item":"x"}'
git -C "$REPO" add -f "$STORE_FILE"
OUT=$(invoke "git commit -m 'oops store'")
[[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
    && ok "AC-6 staged vault/store/ file DENIED" \
    || bad "AC-6 expected deny, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/$STORE_FILE"

# ── AC-5 fail-direction: planted tracked-file PII token via scan's >=1 ──────────
# The planted SET carries BOTH a canonical token (which the consumed pii_scan.scan
# detects, so the hook genuinely blocks via scan's >=1 and names the file) AND a
# non-canonical-case token (Fix 7). The non-canonical token SURFACES an inherited
# pii_scan normalization gap at this boundary: scan() is case-sensitive on the
# `@gmail.com` literal, so `Op.User@Gmail.COM` scores 0 hits. The hook MUST NOT
# reimplement the token scan in bash (SEC-01(b) reuse contract) and MUST NOT edit
# the read-only pii_scan.py (ADR-0001-T1), so closing the gap is an UPSTREAM fix —
# flagged, not patched here. This case proves the hook blocks a scan-detectable
# token; the gap is recorded as an architectural finding.
mkfile "docs/leak.md" "Canonical op.user@gmail.com and non-canonical Op.User@Gmail.COM."
git -C "$REPO" add docs/leak.md
OUT=$(invoke "git commit -m 'leak'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"docs/leak.md"* ]]; } \
    && ok "AC-5 planted PII token (canonical + non-canonical present) DENIED + file named via scan" \
    || bad "AC-5 expected deny naming docs/leak.md, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/leak.md"

# ── TOCTOU: staged file absent from HEAD -> deny (git diff --cached set) ────────
mkfile "docs/fresh.md" "contact alice@gmail.com"
git -C "$REPO" add docs/fresh.md   # never committed -> absent from HEAD; in staged set
OUT=$(invoke "git commit -m 'fresh'")
[[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
    && ok "TOCTOU staged-not-in-HEAD file scanned + DENIED" \
    || bad "TOCTOU expected deny on staged-not-in-HEAD, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/fresh.md"

# ── Scoped-identity (i): operator name in NON-data-bearing prose -> allow ───────
# Identity check is path-scoped; a name in HANDOFF/design prose is accepted provenance.
mkfile "HANDOFF.md" "Session note: Walter McGivney reviewed the wave-3 plan."
git -C "$REPO" add HANDOFF.md
OUT=$(invoke "git commit -m 'handoff'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "scoped-identity (i) name-in-prose -> allow (provenance, identity not trunk-wide)" \
    || bad "scoped-identity (i) name-in-prose wrongly DENIED (identity ran trunk-wide): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/HANDOFF.md"

# ── Scoped-identity (ii): operator name in a DATA-BEARING path -> deny ──────────
# Uses a vault/dna/raw/ path: data-bearing (so the IDENTITY scan covers it) but NOT
# caught by conditions 1/2 (scaffold/store membership), so the block must come from
# the identity scan over the data-bearing subset — proving the scoping, not a path
# check. The name carries no @gmail.com, so only the identity patterns can flag it.
mkfile "vault/dna/raw/sample.json" '{"note":"reviewed by Walter McGivney"}'
git -C "$REPO" add -f "vault/dna/raw/sample.json"
OUT=$(invoke "git commit -m 'name in data path'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"vault/dna/raw/sample.json"* ]]; } \
    && ok "scoped-identity (ii) name-in-data-path -> DENY (identity scan, not path check)" \
    || bad "scoped-identity (ii) name-in-data-path NOT denied via identity scan: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/vault/dna/raw/sample.json"

# ── Fail-closed: scan invocation errors with a token staged -> deny ────────────
# Point the scanner root at a dir with NO importable scripts/guard/pii_scan -> import
# fails -> python3 -c returns non-zero. The hook must DENY, never allow.
mkfile "docs/leak2.md" "contact bob@gmail.com"
git -C "$REPO" add docs/leak2.md
BADROOT="$TMP/no-scanner-here"; mkdir -p "$BADROOT"
OUT=$(printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "git commit -m 'x'" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
      | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$BADROOT" bash "$HOOK")
[[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
    && ok "fail-closed: scan import error -> DENY (default-deny)" \
    || bad "fail-closed expected deny on scan error, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/leak2.md"

# ── SEC-01(b): stub scan returns 0 + writes sentinel -> allow AND sentinel ─────
# THE load-bearing reuse proof: a deterministic stub scanner flips the decision.
mkfile "docs/leak3.md" "contact carol@gmail.com"
git -C "$REPO" add docs/leak3.md
STUBROOT="$TMP/stubroot"; mkdir -p "$STUBROOT/scripts/guard"
SENTINEL="$TMP/sec01b-sentinel"
cat > "$STUBROOT/scripts/guard/pii_scan.py" <<PY
import os
from pathlib import Path
DEFAULT_IDENTITY_CONFIG = Path("vault/meta/operator-identity.txt")
def scan(tracked_files, identity_config=DEFAULT_IDENTITY_CONFIG):
    open(os.environ["SEC01B_SENTINEL"], "w").write("ran")
    return 0
PY
OUT=$(printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "git commit -m 'x'" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
      | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$STUBROOT" \
        SEC01B_SENTINEL="$SENTINEL" bash "$HOOK")
{ [[ "$OUT" != *'"deny"'* ]] && [[ -f "$SENTINEL" ]]; } \
    && ok "SEC-01(b) stub scan=0 -> allow AND sentinel written (reuse proven)" \
    || bad "SEC-01(b) NO-GO: deny-while-stub-0 or sentinel absent (sentinel=$([[ -f "$SENTINEL" ]] && echo yes || echo no)); out: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/leak3.md"

# ── cwd fail-open (Finding 1): hook run from a SUBDIRECTORY of PROJECT_ROOT ─────
# pii_scan.scan does open(path) relative to the PROCESS cwd. If the hook does not
# cd into PROJECT_ROOT before invoking the scan subprocess, the repo-relative staged
# paths fail to open (OSError swallowed), scan returns 0, and the planted token
# commits unscanned (ALLOW). The block must hold regardless of the agent's cwd.
mkfile "docs/leak4.md" "contact dave@gmail.com"
git -C "$REPO" add docs/leak4.md
SUBDIR="$REPO/docs/sub"; mkdir -p "$SUBDIR"
OUT=$(cd "$SUBDIR" && printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "git commit -m 'x'" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
      | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"docs/leak4.md"* ]]; } \
    && ok "cwd-independent scan: planted token DENIED from a subdirectory cwd" \
    || bad "cwd fail-open: token NOT denied when hook run from subdir, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/leak4.md"

# ── git-plumbing fail-open (Finding 2): PROJECT_ROOT is a NON-git directory ─────
# `git diff --cached` fails (not a repo); the staged set must NOT silently read as
# empty -> allow. A git-plumbing failure (rc != 0) is fail-closed -> deny, distinct
# from the legitimate empty-staged-set case (rc == 0, nothing staged -> allow).
NONGIT="$TMP/nongit"; mkdir -p "$NONGIT"
OUT=$(printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "git commit -m 'x'" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
      | BLOCK_PII_COMMIT_PROJECT_ROOT="$NONGIT" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK")
[[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
    && ok "git-plumbing fail-closed: non-git PROJECT_ROOT -> DENY (not silent allow)" \
    || bad "git-plumbing fail-open: non-git PROJECT_ROOT allowed, got: $OUT"

# ── F-SEC1: high-similarity rename injecting PII -> deny (--diff-filter=ACMRT) ───
# A rename above git's similarity threshold is classified R, which --diff-filter=ACM
# DROPS from the staged set -> empty set -> silent ALLOW even though the destination
# carries injected PII. The filter must include R (and T) so the destination path is
# enumerated; git diff --name-only emits the DESTINATION for an R entry, which is
# correct for both the path checks and the content scan.
yes "lorem ipsum dolor sit amet padding line" | head -200 > "$REPO/big.txt"
git -C "$REPO" add big.txt; git -C "$REPO" commit -q -m "seed big"
git -C "$REPO" mv big.txt renamed.txt
printf '\ncontact erin@gmail.com\n' >> "$REPO/renamed.txt"
git -C "$REPO" add renamed.txt
OUT=$(invoke "git commit -m 'rename inject'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"renamed.txt"* ]]; } \
    && ok "F-SEC1 high-similarity rename with injected PII DENIED + destination named" \
    || bad "F-SEC1 rename-bypass: injected-PII rename NOT denied, got: $OUT"
git -C "$REPO" reset -q --soft HEAD~1; git -C "$REPO" reset -q
rm -f "$REPO/big.txt" "$REPO/renamed.txt"

# ── F-BUG1: malformed (non-JSON) stdin -> deny (jq parse fail-closed) ───────────
# jq exits non-zero on non-JSON stdin with empty stdout. The hook must capture jq's
# rc and DENY on parse failure, not fall through the empty-COMMAND early-exit (which
# only legitimately handles valid JSON with no command field -> allow).
OUT=$(printf 'not-json-at-all' \
      | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" bash "$HOOK")
[[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
    && ok "F-BUG1 malformed stdin -> DENY (jq parse fail-closed)" \
    || bad "F-BUG1 jq fail-open: malformed stdin allowed, got: $OUT"

# ── F-TEST1: CHARACTERIZATION — non-canonical-case token ALONE -> currently allow ─
# PINS the inherited pii_scan case-sensitivity gap (bead 2x1): scan()'s contact
# pattern is case-sensitive on the `@gmail.com` literal, so a token whose domain is
# upper/mixed case (`Op.User@Gmail.COM`) scores 0 hits. With ONLY that token staged
# (no canonical token, no other PII) the hook does NOT deny. pii_scan.py is read-only,
# so this characterizes the gap rather than fixing it. WHEN the upstream gap is closed
# (case-insensitive match) this turns RED and MUST be updated to assert deny.
mkfile "docs/noncanon.md" "Reach out to Op.User@Gmail.COM for details."
git -C "$REPO" add docs/noncanon.md
OUT=$(invoke "git commit -m 'noncanon only'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "F-TEST1 non-canonical token alone -> allow (PINS pii_scan case gap, bead 2x1)" \
    || bad "F-TEST1 case gap closed upstream? non-canonical token now denied — update this case: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/noncanon.md"

# ── F-TEST2: non-numeric rc-0 scan output -> deny (^[0-9]+$ fail-closed clause) ──
# A stub scan that prints a NON-NUMERIC string and returns rc 0 must be caught by the
# `! [[ "$SCAN_OUT" =~ ^[0-9]+$ ]]` clause -> deny, BEFORE the `-ge 1` arithmetic
# (which is false on non-numeric -> would ALLOW). Exercises that clause in isolation.
mkfile "docs/leak5.md" "contact frank@gmail.com"
git -C "$REPO" add docs/leak5.md
NUMSTUB="$TMP/numstub"; mkdir -p "$NUMSTUB/scripts/guard"
cat > "$NUMSTUB/scripts/guard/pii_scan.py" <<PY
from pathlib import Path
DEFAULT_IDENTITY_CONFIG = Path("vault/meta/operator-identity.txt")
def scan(tracked_files, identity_config=DEFAULT_IDENTITY_CONFIG):
    print("not-a-number")
    return 0
PY
OUT=$(printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "git commit -m 'x'" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
      | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$NUMSTUB" bash "$HOOK")
[[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
    && ok "F-TEST2 non-numeric rc-0 scan output -> DENY (^[0-9]+\$ fail-closed clause)" \
    || bad "F-TEST2 non-numeric output fell through to -ge 1 -> ALLOW, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/leak5.md"

echo
echo "test_block_pii_commit: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
