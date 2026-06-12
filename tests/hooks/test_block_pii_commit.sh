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
#   fixture  store-line in docs/ -> deny; SAME line in tests/ -> allow (partition);
#            operator contact in tests/ -> deny (tokens run everywhere)
#   seq      stage-and-commit in one command / commit -a -> deny (sequencing guard);
#            amend + plain commit stay allowed (scannable shapes)
#   3lv (i)   non-operator gmail -> allow (the generic-gmail flood is gone)
#   3lv (ii)  operator contact, NO config -> allow (config-driven; clone semantics)
#   3lv (iii) operator contact in docs prose -> deny (contact scope is trunk-wide)
#   eb1       dirty working-tree .beads/issues.jsonl (bd auto-stage vector) -> deny,
#             even with NOTHING staged; token-free bd file + clean staged -> allow
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
vault/meta/operator-contact.txt
EOF
git add .gitignore; git commit -q -m "seed gitignore"

# Seed the operator-identity config so the hook's relative DEFAULT_IDENTITY_CONFIG
# (vault/meta/operator-identity.txt, resolved against the hook's cwd = $REPO) loads
# the name tokens — letting the scoped-identity cases exercise the REAL identity scan.
mkdir -p "$REPO/vault/meta"
printf 'Walter|McGivney\n' > "$REPO/vault/meta/operator-identity.txt"

# Seed the operator-contact config (3lv): contact detection is config-driven and
# TRUNK-WIDE — the hook's relative DEFAULT_CONTACT_CONFIG resolves here. The one
# synthetic token below is what every contact plant in this suite uses; a
# DIFFERENT gmail address (alice@) is deliberately NOT in the config, proving the
# generic-gmail flood is gone (see the 3lv allow cases).
OPERATOR_CONTACT="op.user@gmail.com"
printf 'op\\.user@gmail\\.com\n' > "$REPO/vault/meta/operator-contact.txt"

# bd flush stub (ycqo): the hook runs `bd sync --flush-only` before reading the bd
# jsonl. Real bd exits 1 in a scratch repo carrying .beads/ without a database (the
# "fresh clone" shape), which would turn every eb1 allow-case into a fail-closed
# deny — so invoke() pins BLOCK_PII_COMMIT_BD_CMD to a no-op stub. The ycqo cases
# below substitute flushing/failing stubs inline.
BD_NOOP="$TMP/bd-noop.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$BD_NOOP"; chmod +x "$BD_NOOP"

# invoke(): build the stdin JSON, run the hook against the scratch repo. PROJECT_ROOT
# is the scratch repo (for staged-file detection); the scanner root is pointed at the
# REAL repo so `from scripts.guard.pii_scan import scan` resolves to the real scanner
# (the scratch repo carries no scripts/). The stub / fail-closed cases override
# BLOCK_PII_COMMIT_PII_SCAN_ROOT inline.
invoke() {  # $1 = command string ; echoes hook stdout
    printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "$1" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
        | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" \
          BLOCK_PII_COMMIT_BD_CMD="$BD_NOOP" bash "$HOOK"
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
# The planted SET carries BOTH a canonical token AND a non-canonical-case token.
# Detection is config-driven since 3lv: the seeded operator-contact config supplies
# the token, the loader compiles it IGNORECASE (2x1), so BOTH forms hit and the
# hook genuinely blocks via scan's >=1 and names the file. The hook MUST NOT
# reimplement the token scan in bash (SEC-01(b) reuse contract).
mkfile "docs/leak.md" "Canonical op.user@gmail.com and non-canonical Op.User@Gmail.COM."
git -C "$REPO" add docs/leak.md
OUT=$(invoke "git commit -m 'leak'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"docs/leak.md"* ]]; } \
    && ok "AC-5 planted PII token (canonical + non-canonical present) DENIED + file named via scan" \
    || bad "AC-5 expected deny naming docs/leak.md, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/leak.md"

# ── TOCTOU: staged file absent from HEAD -> deny (git diff --cached set) ────────
mkfile "docs/fresh.md" "contact $OPERATOR_CONTACT"
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
mkfile "docs/leak2.md" "contact op.user@gmail.com"
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
mkfile "docs/leak3.md" "contact op.user@gmail.com"
git -C "$REPO" add docs/leak3.md
STUBROOT="$TMP/stubroot"; mkdir -p "$STUBROOT/scripts/guard"
SENTINEL="$TMP/sec01b-sentinel"
cat > "$STUBROOT/scripts/guard/pii_scan.py" <<PY
import os
from pathlib import Path
DEFAULT_IDENTITY_CONFIG = Path("vault/meta/operator-identity.txt")
DEFAULT_CONTACT_CONFIG = Path("vault/meta/operator-contact.txt")
def scan(tracked_files, token_config=DEFAULT_IDENTITY_CONFIG, include_structural=True, identity_config=None):
    return 0
def scan_scoped(changed, data_bearing, contact_config=DEFAULT_CONTACT_CONFIG, identity_config=DEFAULT_IDENTITY_CONFIG):
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
mkfile "docs/leak4.md" "contact op.user@gmail.com"
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
printf '\ncontact op.user@gmail.com\n' >> "$REPO/renamed.txt"
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

# ── F-TEST1: non-canonical-case token ALONE -> DENY (bead 2x1 case gap CLOSED) ──
# The config loader compiles every identity/contact token re.IGNORECASE (2x1,
# PR #75), so an upper/mixed-case form of the seeded contact token
# (`Op.User@Gmail.COM`) scores >=1. With ONLY that token staged the hook DENIES via
# the scan and names the file — the case-insensitive boundary holds end-to-end.
mkfile "docs/noncanon.md" "Reach out to Op.User@Gmail.COM for details."
git -C "$REPO" add docs/noncanon.md
OUT=$(invoke "git commit -m 'noncanon only'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"docs/noncanon.md"* ]]; } \
    && ok "F-TEST1 non-canonical token alone -> DENY (bead 2x1 case gap closed)" \
    || bad "F-TEST1 expected deny on non-canonical token (2x1 closed), got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/noncanon.md"

# ── F-TEST2: non-numeric rc-0 scan output -> deny (^[0-9]+$ fail-closed clause) ──
# A stub scan that prints a NON-NUMERIC string and returns rc 0 must be caught by the
# `! [[ "$SCAN_OUT" =~ ^[0-9]+$ ]]` clause -> deny, BEFORE the `-ge 1` arithmetic
# (which is false on non-numeric -> would ALLOW). Exercises that clause in isolation.
mkfile "docs/leak5.md" "contact op.user@gmail.com"
git -C "$REPO" add docs/leak5.md
NUMSTUB="$TMP/numstub"; mkdir -p "$NUMSTUB/scripts/guard"
cat > "$NUMSTUB/scripts/guard/pii_scan.py" <<PY
from pathlib import Path
DEFAULT_IDENTITY_CONFIG = Path("vault/meta/operator-identity.txt")
DEFAULT_CONTACT_CONFIG = Path("vault/meta/operator-contact.txt")
def scan(tracked_files, token_config=DEFAULT_IDENTITY_CONFIG, include_structural=True, identity_config=None):
    return 0
def scan_scoped(changed, data_bearing, contact_config=DEFAULT_CONTACT_CONFIG, identity_config=DEFAULT_IDENTITY_CONFIG):
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

# ── fixture partition (dv3): structural patterns skip tests/, tokens do not ─────
# A reading-shaped literal in a NON-fixture path is the real leaked-store vector
# and must deny; the SAME literal in tests/ is a synthetic fixture by construction
# and must commit; an operator-contact token in tests/ is STILL a leak and denies.
STORE_LINE='{"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", "source": "manual", "value": 55}'
mkfile "docs/pasted-reading.md" "$STORE_LINE"
git -C "$REPO" add docs/pasted-reading.md
OUT=$(invoke "git commit -m 'pasted'")
[[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
    && ok "fixture-partition: store-line in docs/ -> DENY (structural net live)" \
    || bad "fixture-partition: store-line in docs/ NOT denied: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/pasted-reading.md"

mkfile "tests/store/test_fixture.py" "PLANT = '$STORE_LINE'"
git -C "$REPO" add tests/store/test_fixture.py
OUT=$(invoke "git commit -m 'fixture'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "fixture-partition: store-line in tests/ -> ALLOW (synthetic fixture)" \
    || bad "fixture-partition: tests/ fixture wrongly DENIED (clonability regression): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/tests/store/test_fixture.py"

mkfile "tests/store/test_leak.py" "CONTACT = '$OPERATOR_CONTACT'"
git -C "$REPO" add tests/store/test_leak.py
OUT=$(invoke "git commit -m 'leakfixture'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"tests/store/test_leak.py"* ]]; } \
    && ok "fixture-partition: operator contact in tests/ -> DENY (tokens still run)" \
    || bad "fixture-partition: contact in tests/ NOT denied (token scan dropped): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/tests/store/test_leak.py"

# ── seq: stage-and-commit in ONE command -> deny (condition-0 sequencing guard) ──
# The PreToolUse staged-set snapshot predates any `git add` inside the same command,
# so single-call add+commit (and `git commit -a`, which stages by itself) would be
# scanned against an EMPTY staged set — a vacuous boundary for the dominant agent
# idiom (discovered live at 3lv registration). These deny EVEN ON A CLEAN TREE:
# the guard is about sequencing, not content.
for seqform in "git add docs/x.md && git commit -m 'x'" \
               "git rm old.md && git commit -m 'x'" \
               "printf 'y' > f && git add f && git commit -m 'x'" \
               "git commit -am 'x'" \
               "git commit -a -m 'x'" \
               "git commit --all -m 'x'"; do
    OUT=$(invoke "$seqform")
    [[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
        && ok "seq stage+commit single-call DENIED: $seqform" \
        || bad "seq guard missed single-call form: '$seqform' got: $OUT"
done

# seq global-option evasion (PR#84 SEC-1/BUG-2): a global option between `git` and
# the staging subcommand / `commit` must NOT let the form slip past the guard.
for evasion in "git -c user.email=x@y.z add f && git commit -m 'x'" \
               "git --work-tree=. add f && git commit -m 'x'" \
               "git -c k=v commit -am 'x'" \
               "git -C . commit -am 'x'" \
               $'git \\\nadd f && git commit -m x' \
               "git commit -m 'fix; tidy' -a"; do
    OUT=$(invoke "$evasion")
    [[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
        && ok "seq global-opt/newline/msg-semicolon evasion DENIED: ${evasion//$'\n'/\\n}" \
        || bad "seq evasion slipped past guard: '${evasion//$'\n'/\\n}' got: $OUT"
done

# seq pathspec commit (PR#84 BUG-2a): a path-separator-bearing pathspec arg after
# commit commits working-tree content the staged-set scan can't see -> deny.
for pathspec in "git commit -m 'x' docs/leak.md" "git commit docs/sub/file.md -m x"; do
    OUT=$(invoke "$pathspec")
    [[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
        && ok "seq pathspec commit DENIED: $pathspec" \
        || bad "seq pathspec commit slipped past guard: '$pathspec' got: $OUT"
done

# seq message-text FP (PR#84 BUG-5/TEST-2): the guard must NOT deny a plain commit
# whose -m MESSAGE merely MENTIONS git add/rm/-a/--all — quoted segments are
# stripped before the match. Pins the accepted boundary: plain commits with
# subcommand-shaped message text stay allowed.
for okmsg in "git commit -m 'docs: explain git add usage'" \
             "git commit -m 'note: git rm removes files'" \
             "git commit -m 'fix -and improve'" \
             "git commit -m 'document the -a flag'" \
             "git commit -m 'use --all carefully'"; do
    OUT=$(invoke "$okmsg")
    [[ "$OUT" != *'"deny"'* ]] \
        && ok "seq message-text mentioning add/-a allowed: $okmsg" \
        || bad "seq message-text FALSE-POSITIVE denied a plain commit: '$okmsg' got: $OUT"
done

# seq allow-boundary: amend (uses the VISIBLE staged set) and a plain commit are
# the scannable shapes and must NOT trip the sequencing guard.
for okform in "git commit --amend -m 'x'" "git commit -m 'plain'" "git -c k=v commit -m 'global opt, no -a'"; do
    OUT=$(invoke "$okform")
    [[ "$OUT" != *'"deny"'* ]] \
        && ok "seq scannable shape allowed: $okform" \
        || bad "seq guard false-positive on scannable shape '$okform': $OUT"
done

# ── 3lv (i): a NON-operator email -> ALLOW (the generic-gmail flood is GONE) ─────
# The load-bearing clonability fix: a synthetic gmail address that is NOT in the
# operator-contact config (the shape of the scanner's own test fixtures and bead
# example emails) must commit cleanly. Reds under the pre-3lv generic trunk-wide
# `@gmail.com` pattern — the 14-false-hit flood that blocked registration (S43).
mkfile "docs/fixture-email.md" "example fixture address: alice@gmail.com"
git -C "$REPO" add docs/fixture-email.md
OUT=$(invoke "git commit -m 'fixture email'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "3lv (i) non-operator gmail -> ALLOW (generic-gmail flood gone)" \
    || bad "3lv (i) synthetic fixture email wrongly DENIED (generic pattern back?): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/fixture-email.md"

# ── 3lv (ii): operator contact WITHOUT config -> ALLOW (clone semantics) ─────────
# On a fresh clone the contact config is absent, so even the operator's own
# address is undetectable there (structural patterns still run). Proves contact
# detection is config-driven at the HOOK level, mirroring the identity model.
mv "$REPO/vault/meta/operator-contact.txt" "$TMP/contact-config-parked"
mkfile "docs/clone-sim.md" "contact $OPERATOR_CONTACT"
git -C "$REPO" add docs/clone-sim.md
OUT=$(invoke "git commit -m 'clone sim'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "3lv (ii) operator contact with NO config -> ALLOW (config-driven, clone-safe)" \
    || bad "3lv (ii) expected allow without contact config, got: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/clone-sim.md"
mv "$TMP/contact-config-parked" "$REPO/vault/meta/operator-contact.txt"

# ── 3lv (iii): operator contact in NON-data-bearing prose -> DENY (trunk-wide) ───
# The contact scope is TRUNK-WIDE, unlike the name (data-bearing only): the email
# has no legitimate tracked use. A contact token in plain docs prose must deny.
mkfile "docs/contact-in-prose.md" "reach the operator at $OPERATOR_CONTACT"
git -C "$REPO" add docs/contact-in-prose.md
OUT=$(invoke "git commit -m 'contact prose'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"docs/contact-in-prose.md"* ]]; } \
    && ok "3lv (iii) operator contact in docs prose -> DENY (contact is trunk-wide)" \
    || bad "3lv (iii) contact in prose NOT denied trunk-wide: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/contact-in-prose.md"

# ── eb1: bd auto-stage coverage — working-tree .beads/issues.jsonl is scanned ───
# The bd pre-commit git hook stages .beads/issues.jsonl INSIDE `git commit`, AFTER
# this hook's staged-set snapshot, so freshly-flushed bead text (the 46m leak
# vector) would otherwise commit unscanned. The hook appends the working-tree bd
# file to its trunk-wide scan set on EVERY commit when it exists. The bd file is
# deliberately NOT git-added here — that is the exact blind-spot shape.
mkfile ".beads/issues.jsonl" "{\"id\":\"x-1\",\"title\":\"ping $OPERATOR_CONTACT about labs\"}"
mkfile "docs/clean-note.md" "Plain clean note."
git -C "$REPO" add docs/clean-note.md
OUT=$(invoke "git commit -m 'note'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *".beads/issues.jsonl"* ]]; } \
    && ok "eb1 (1) dirty bd file + clean staged file -> DENY naming .beads/issues.jsonl" \
    || bad "eb1 (1) bd-file token NOT denied (bd auto-stage blind spot open): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/clean-note.md"

# eb1 (2): NOTHING staged, same dirty bd file -> deny. Uniquely pins that the bd
# append precedes the empty-staged-set early exit: a commit with nothing
# agent-staged still succeeds carrying bd's auto-staged flush, so the scan must
# run on the bd file alone (pre-eb1, the hook allowed via that exit). The deny
# must NAME .beads/issues.jsonl (PR#100 F6): a bare deny check also matches the
# fail-closed ERROR deny, passing vacuously when the scan path is broken.
OUT=$(invoke "git commit -m 'flush only'")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *".beads/issues.jsonl"* ]]; } \
    && ok "eb1 (2) EMPTY staged set + dirty bd file -> DENY naming .beads/issues.jsonl" \
    || bad "eb1 (2) empty-staged-set commit allowed or deny did not name the bd file: $OUT"

# eb1 (3): token-free bd file + clean staged file -> allow (the flood boundary —
# the bd corpus must not over-block routine commits; content is neither a contact
# token nor store-line shaped).
mkfile ".beads/issues.jsonl" '{"id":"x-1","title":"routine governance task"}'
mkfile "docs/clean-note2.md" "Another plain note."
git -C "$REPO" add docs/clean-note2.md
OUT=$(invoke "git commit -m 'note2'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "eb1 (3) token-free bd file + clean staged file -> ALLOW (no over-blocking)" \
    || bad "eb1 (3) token-free bd file wrongly DENIED (flood boundary breached): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/clean-note2.md"

# eb1 (4): token-free bd file, NOTHING staged -> allow (PR#100 F5). Pins that
# the bd append does not turn (empty staged set + bd file present) into a
# per-se deny: a routine flush-only commit with clean bead text must pass.
# Reds if the hook denies on bd-file presence instead of bd-file content.
OUT=$(invoke "git commit -m 'flush only clean'")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "eb1 (4) token-free bd file + EMPTY staged set -> ALLOW (content, not presence)" \
    || bad "eb1 (4) flush-only clean commit wrongly DENIED (per-se bd deny): $OUT"
rm -rf "$REPO/.beads"

# ── cvr: hardened matcher catches bypass-form commits (env/path/trailing-sep) ───
# With a PII file staged, the hook must DENY even when the commit command uses an
# env-var prefix, an absolute git path, or a trailing separator — forms the prior
# matcher let bypass (a silent PII-distribution hole now this hook is registered).
mkfile "docs/leak6.md" "contact op.user@gmail.com"
git -C "$REPO" add docs/leak6.md
for bypass in "EDITOR=vim git commit -m x" "/usr/bin/git commit -m x" "git commit;" \
              "git commit&" "FOO=1 BAR=2 git commit" "EDITOR=vim git commit;" \
              " git commit" $'ls\ngit commit'; do
    OUT=$(invoke "$bypass")
    [[ "$OUT" == *'"permissionDecision":"deny"'* ]] \
        && ok "cvr bypass-form commit DENIED: ${bypass//$'\n'/\\n}" \
        || bad "cvr bypass NOT denied (matcher gap): '${bypass//$'\n'/\\n}' got: $OUT"
done
git -C "$REPO" reset -q; rm -f "$REPO/docs/leak6.md"

# ── 29u4: worktree-aware target-repo resolution via the hook input's cwd ───────
# A commit issued from a linked worktree lands on THAT worktree's index; the scan
# must run there. The env override seeds the FALLBACK root ($REPO, staged set left
# clean), so a deny can only come from resolving the worktree. The identity/contact
# configs are per-checkout (gitignored), so the worktree seeds its own copies —
# mirroring a real worktree, where an absent config degrades to structural-only
# (clone semantics, same as 3lv (ii)).
WT="$TMP/wt"
git -C "$REPO" worktree add -q -b wt-feat "$WT"
mkdir -p "$WT/vault/meta"
printf 'Walter|McGivney\n' > "$WT/vault/meta/operator-identity.txt"
printf 'op\\.user@gmail\\.com\n' > "$WT/vault/meta/operator-contact.txt"

invoke_cwd() {  # $1 = command string ; $2 = payload cwd ; echoes hook stdout
    printf '{"cwd":%s,"tool_input":{"command":%s}}' \
        "$(printf '%s' "$2" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
        "$(printf '%s' "$1" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
        | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" \
          BLOCK_PII_COMMIT_BD_CMD="$BD_NOOP" bash "$HOOK"
}

# 29u4 (1): PII staged in the WORKTREE -> DENY (the vacuous-pass case)
mkdir -p "$WT/docs"
printf 'contact %s\n' "$OPERATOR_CONTACT" > "$WT/docs/leak-wt.md"
git -C "$WT" add docs/leak-wt.md
OUT=$(invoke_cwd "git commit -m 'wt leak'" "$WT")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"docs/leak-wt.md"* ]]; } \
    && ok "29u4 (1) worktree-staged PII -> DENY naming the file (cwd resolution)" \
    || bad "29u4 (1) worktree-staged PII NOT denied (worktree-blind scan), got: $OUT"
git -C "$WT" reset -q; rm -f "$WT/docs/leak-wt.md"

# 29u4 (2) control: clean worktree staged set -> ALLOW (resolution must not over-block)
printf 'plain worktree note\n' > "$WT/docs/clean-wt.md"
git -C "$WT" add docs/clean-wt.md
OUT=$(invoke_cwd "git commit -m 'wt clean'" "$WT")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "29u4 (2) clean worktree staged set -> ALLOW" \
    || bad "29u4 (2) clean worktree commit wrongly DENIED: $OUT"
git -C "$WT" reset -q; rm -f "$WT/docs/clean-wt.md"

# ── ycqo: flush-before-scan — pending bead text reaches the jsonl ONLY via flush ─
# The bd pre-commit git hook flushes .beads/beads.db AND stages the jsonl INSIDE
# `git commit`, AFTER this hook's scan — so bead text still pending in the db at
# scan time committed unscanned. The hook must run `bd sync --flush-only` BEFORE
# reading the jsonl. Simulated hermetically: the "pending db text" lives in a side
# file the flushing bd STUB appends to the jsonl when invoked (cwd = the target
# repo, as the hook runs it); pre-ycqo the hook never invoked bd, so the dirty
# text stayed pending and the commit sailed through.
PENDING="$TMP/pending-bead.txt"
printf '{"id":"x-2","title":"ping %s about labs"}\n' "$OPERATOR_CONTACT" > "$PENDING"
BD_FLUSH="$TMP/bd-flush.sh"
cat > "$BD_FLUSH" <<EOF
#!/usr/bin/env bash
cat "$PENDING" >> .beads/issues.jsonl
exit 0
EOF
chmod +x "$BD_FLUSH"
BD_FAIL="$TMP/bd-fail.sh"
printf '#!/usr/bin/env bash\necho "bd: no beads database found" >&2\nexit 1\n' > "$BD_FAIL"
chmod +x "$BD_FAIL"

invoke_bd() {  # $1 = command string ; $2 = bd command override ; echoes hook stdout
    printf '{"tool_input":{"command":%s}}' \
        "$(printf '%s' "$1" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
        | BLOCK_PII_COMMIT_PROJECT_ROOT="$REPO" BLOCK_PII_COMMIT_PII_SCAN_ROOT="$REAL_ROOT" \
          BLOCK_PII_COMMIT_BD_CMD="$2" bash "$HOOK"
}

# ycqo (1): clean jsonl on disk, dirty text PENDING (db-only) at scan time -> the
# in-hook flush materializes it BEFORE the jsonl read -> DENY naming the bd file.
# A db file is seeded: the flush only runs when a database exists (db-gate) —
# without one nothing can be pending and the flush is skipped.
mkfile ".beads/issues.jsonl" '{"id":"x-1","title":"routine clean task"}'
: > "$REPO/.beads/beads.db"
mkfile "docs/clean-note3.md" "Plain note."
git -C "$REPO" add docs/clean-note3.md
OUT=$(invoke_bd "git commit -m 'note3'" "$BD_FLUSH")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *".beads/issues.jsonl"* ]]; } \
    && ok "ycqo (1) pending-in-db dirty text flushed-then-scanned -> DENY naming the bd file" \
    || bad "ycqo (1) pending dirty text NOT caught (flush-before-scan missing): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/clean-note3.md"; rm -rf "$REPO/.beads"

# ycqo (2): flush FAILURE -> DENY (fail-closed, matching the git-rc/scan-rc
# convention and bd's own exit-1-on-flush-failure) — pending text it could not
# flush cannot be scanned. Db seeded so the flush path (not the db-gate skip) runs.
mkfile ".beads/issues.jsonl" '{"id":"x-1","title":"routine clean task"}'
: > "$REPO/.beads/beads.db"
mkfile "docs/clean-note4.md" "Plain note."
git -C "$REPO" add docs/clean-note4.md
OUT=$(invoke_bd "git commit -m 'note4'" "$BD_FAIL")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *"flush"* ]]; } \
    && ok "ycqo (2) bd flush failure -> DENY (fail-closed)" \
    || bad "ycqo (2) flush failure NOT denied (fail-open on flush rc): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/clean-note4.md"; rm -rf "$REPO/.beads"

# ycqo (3): db present but NO jsonl yet — the flush CREATES it carrying the
# dirty text -> DENY. Pins the ordering: flush runs BEFORE the jsonl existence
# check, not after (an after-check flush would miss a freshly-created jsonl).
mkdir -p "$REPO/.beads"
: > "$REPO/.beads/beads.db"
mkfile "docs/clean-note5.md" "Plain note."
git -C "$REPO" add docs/clean-note5.md
OUT=$(invoke_bd "git commit -m 'note5'" "$BD_FLUSH")
{ [[ "$OUT" == *'"permissionDecision":"deny"'* ]] && [[ "$OUT" == *".beads/issues.jsonl"* ]]; } \
    && ok "ycqo (3) flush-created jsonl with dirty text -> DENY (flush precedes existence check)" \
    || bad "ycqo (3) flush-created jsonl NOT scanned (existence check precedes flush): $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/clean-note5.md"; rm -rf "$REPO/.beads"

# ycqo (4) control: bd UNAVAILABLE + clean jsonl -> ALLOW (a checkout without bd
# commits on the as-is jsonl scan, no flush, no per-se deny). Db seeded so the
# skip provably comes from the bd-availability guard, not the db-gate.
mkfile ".beads/issues.jsonl" '{"id":"x-1","title":"routine clean task"}'
: > "$REPO/.beads/beads.db"
mkfile "docs/clean-note6.md" "Plain note."
git -C "$REPO" add docs/clean-note6.md
OUT=$(invoke_bd "git commit -m 'note6'" "$TMP/no-such-bd")
[[ "$OUT" != *'"deny"'* ]] \
    && ok "ycqo (4) bd unavailable + clean jsonl -> ALLOW (flush guard skips, scan still runs)" \
    || bad "ycqo (4) bd-absent commit wrongly DENIED: $OUT"
git -C "$REPO" reset -q; rm -f "$REPO/docs/clean-note6.md"; rm -rf "$REPO/.beads"

echo
echo "test_block_pii_commit: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
