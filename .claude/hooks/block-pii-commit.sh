#!/bin/bash
# block-pii-commit.sh — PreToolUse hook for the Bash tool. ADR-0005-T1.
#
# The trunk content-scan trust boundary. When a `git commit` stages (a) a
# filled-scaffold value, (b) a vault/store/ file, or (c) any staged file whose
# CONTENTS carry operator PII, deny the commit. Mirror of block-ungated-vault-write.sh.
#
# Conditions 1 & 2 are PATH/membership checks over the staged set. Condition 3
# delegates the token scan ENTIRELY to the cross-spec scripts/guard/pii_scan.scan
# (the SEC-01(a) reuse contract) — NO bash/rg/grep token reimplementation. The
# scan is scoped per the ADR-0005 amended Decision 2026-06-06 (bead qwj option iii):
#   • agnostic, trunk-wide — scan(<full staged set>, identity_config=<non-existent>)
#     so only the operator-AGNOSTIC patterns (@gmail.com contact + structural store
#     lines) run over every staged file; the operator NAME is accepted provenance in
#     governance/session/design prose and must NOT be flagged trunk-wide.
#   • identity, data-bearing only — scan(<data-bearing subset>, DEFAULT_IDENTITY_CONFIG)
#     so the operator-name patterns run only over health-data paths (scaffold values,
#     store, raw dropzones) where the name IS a leak.
# Deny if EITHER call returns >=1.
#
# Fail-closed (Security HIGH-1): any error in the scan path — import fails, scan
# raises, the python3 -c returns non-zero, or the git/jq plumbing fails — emits
# deny, NEVER allow. This is the opposite of the sibling hooks' allow-on-error
# idioms, which are tolerable for a branch-name annoyance but a silent PII bypass
# at a distribution boundary.
#
# TEST/OVERRIDE ENV (never set in production):
#   BLOCK_PII_COMMIT_PROJECT_ROOT   — git root for staged-file detection.
#   BLOCK_PII_COMMIT_PII_SCAN_ROOT  — sys.path root for the pii_scan import
#                                     (default: PROJECT_ROOT). Tests point it at a
#                                     stub (SEC-01(b)) or an unimportable dir
#                                     (fail-closed).
#
# Exit codes (Claude Code hook convention):
#   prints deny JSON + exits 0 → deny tool call
#   exits 0 with no output      → allow tool call

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${BLOCK_PII_COMMIT_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
PII_SCAN_ROOT="${BLOCK_PII_COMMIT_PII_SCAN_ROOT:-$PROJECT_ROOT}"

# ONE shared path/glob constant (Fix 4): the filled-scaffold-value prefix that the
# repo-root .gitignore excludes, condition 1 matches, and the test's representative
# value lives under. Conditions 1 & 2 + the data-bearing partition all key off this.
SCAFFOLD_PREFIX="vault/scaffold/filled/"
STORE_PREFIX="vault/store/"
# Data-bearing dropzones (gitignored health-data paths) the identity scan also covers.
DATA_BEARING_PREFIXES=("$SCAFFOLD_PREFIX" "$STORE_PREFIX" "vault/dna/raw/" "vault/labs/raw/")

deny() {  # $1 = reason string
    jq -nc --arg r "$1" \
        '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
    exit 0
}

COMMAND=$(jq -r '.tool_input.command // empty' < /dev/stdin)
[[ -z "$COMMAND" ]] && exit 0

NORM=$(echo "$COMMAND" | tr -s '[:space:]' ' ')

# Only a git commit is our concern (same matcher as the sibling hooks).
if ! echo "$NORM" | grep -qE '(^|[;&|] *)git +([^|&;]*\s)?commit( |$)'; then
    exit 0
fi

# Staged set git will actually commit (added/copied/modified) — NOT git ls-files
# (the HEAD/tracked set), so a git add-ed file absent from HEAD is scanned (Fix 3).
# A git-plumbing failure here is fail-closed: empty staged set on error -> deny.
STAGED=()
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    STAGED+=("$f")
done < <(git -C "$PROJECT_ROOT" diff --cached --name-only --diff-filter=ACM 2>/dev/null)

[[ ${#STAGED[@]} -eq 0 ]] && exit 0

# Partition the staged set into the data-bearing subset (for the identity scan).
DATA_BEARING=()
for f in "${STAGED[@]}"; do
    for p in "${DATA_BEARING_PREFIXES[@]}"; do
        case "$f" in "$p"*) DATA_BEARING+=("$f"); break ;; esac
    done
done

# ── Condition 1: staged filled-scaffold value (path/membership check) ──────────
for f in "${STAGED[@]}"; do
    case "$f" in
        "$SCAFFOLD_PREFIX"*)
            deny "PII-FREE-TRUNK: staged filled-scaffold value '$f' must not be committed (it carries operator data; it belongs only in the gitignored '$SCAFFOLD_PREFIX'). Unstage it: 'git rm --cached $f'." ;;
    esac
done

# ── Condition 2: staged vault/store/ file (path/membership check) ──────────────
for f in "${STAGED[@]}"; do
    case "$f" in
        "$STORE_PREFIX"*)
            deny "PII-FREE-TRUNK: staged store file '$f' must not be committed ('$STORE_PREFIX' is gitignored operator-data; it stays untracked). Unstage it: 'git rm --cached $f'." ;;
    esac
done

# ── Condition 3: tracked-file PII token — delegated to pii_scan.scan ───────────
# TWO scoped calls to the SAME published surface (no pii_scan.py change). The full
# staged set and the data-bearing subset are passed on argv; scan does NOT
# re-enumerate (TOCTOU-closing capture). The scanner is imported from PII_SCAN_ROOT
# (sys.path-prepended), so a test stub deterministically flips the verdict (SEC-01(b)).
# stdout = combined hit count; stderr carries scan's `PII-HIT: <path>` lines.
SCAN_ERR_FILE=$(mktemp)
SCAN_OUT=$(
    BPC_SCAN_ROOT="$PII_SCAN_ROOT" \
    python3 - "${#STAGED[@]}" "${STAGED[@]}" ${DATA_BEARING[@]+"${DATA_BEARING[@]}"} <<'PY' 2>"$SCAN_ERR_FILE"
import os
import sys

sys.path.insert(0, os.environ["BPC_SCAN_ROOT"])
from scripts.guard.pii_scan import scan, DEFAULT_IDENTITY_CONFIG

n_staged = int(sys.argv[1])
staged = sys.argv[2:2 + n_staged]
data_bearing = sys.argv[2 + n_staged:]

# (1) agnostic, trunk-wide: a guaranteed-NON-EXISTENT identity_config makes
# _load_identity_patterns return [] (never "" / "." — those resolve to an existing
# cwd and would turn the identity patterns on / raise).
agnostic = scan(staged, identity_config="/nonexistent/aplus-no-identity")
# (2) identity, data-bearing only: default (name-bearing) identity_config.
identity = scan(data_bearing, identity_config=DEFAULT_IDENTITY_CONFIG) if data_bearing else 0

print(agnostic + identity)
PY
)
SCAN_RC=$?
SCAN_ERR=$(cat "$SCAN_ERR_FILE" 2>/dev/null)
rm -f "$SCAN_ERR_FILE"

# Fail-closed: any scan-path error denies (default-deny at the scan boundary).
if [[ $SCAN_RC -ne 0 ]] || ! [[ "$SCAN_OUT" =~ ^[0-9]+$ ]]; then
    deny "PII-FREE-TRUNK: content-scan failed (pii_scan.scan errored, rc=$SCAN_RC). Failing closed — commit blocked. Detail: ${SCAN_ERR:-no stderr}"
fi

if [[ "$SCAN_OUT" -ge 1 ]]; then
    OFFENDERS=$(echo "$SCAN_ERR" | grep '^PII-HIT: ' | sed 's/^PII-HIT: //' | sort -u | head -8)
    deny "PII-FREE-TRUNK: staged file(s) carry operator PII (pii_scan reported $SCAN_OUT hit(s)). Offending file(s):
$OFFENDERS
Remove the PII or unstage the file before committing."
fi

# No condition blocked and no scan error → allow.
exit 0
