#!/bin/bash
# APLUS-MANAGED dv3 pre-push-pii-scan
# pre-push-pii-scan.sh — git pre-push hook (bead dv3). PII backstop on the push range.
#
# The "APLUS-MANAGED" sentinel above (line 2) is the install-ownership marker
# scripts/clone/init_instance.py keys on: it refreshes a .git/hooks/pre-push hook
# only when that exact line is present, and never clobbers a hook lacking it.
#
# block-pii-commit.sh gates only AGENT-issued git commits inside a Claude session;
# commits from a human terminal/IDE (and anything the commit-time scan missed)
# bypass it entirely. This git-native pre-push hook is the defense-in-depth
# backstop at the LAST local boundary before content reaches the remote. It mirrors
# the commit hook's THREE conditions over the files changed in the pushed range
# (the SEC-01(a) reuse contract — scripts/guard/pii_scan, no bash/grep token
# reimplementation; the scope policy is single-sourced via lib/pii-scan-scope.sh):
#   • path denial — a changed file under vault/scaffold/filled/ or vault/store/ is
#     operator data by LOCATION, blocked regardless of token hits (PR#84 API-1; the
#     human-terminal path is exactly where `git add -f` past .gitignore happens).
#   • trunk-wide — structural store-line patterns + the operator-contact tokens,
#     skipping the structural pass for tests/ fixture paths (the dv3 partition)
#   • identity, data-bearing only — operator-name tokens over health-data paths
# and blocks the push (exit 1) on any hit. Fail-closed: any scan/plumbing error
# blocks, never allows.
#
# SOURCE OF TRUTH is this tracked file; scripts/clone/init_instance.py installs a
# copy to .git/hooks/pre-push at clone init (git does not track .git/hooks).
# KNOWN LIMITS (documented, accepted — defense-in-depth, not a guarantee):
#   • `git push --no-verify` bypasses any pre-push hook.
#   • Changed paths are scanned from the WORKING TREE (the same disk-content
#     approximation block-pii-commit.sh uses for the staged set): PII that was
#     committed AND since removed from disk is not seen here — the history
#     question belongs to a history audit, not a push gate. The commit hook's
#     historical bd-auto-stage blind spot (PR#84 HIST-2) is closed at the commit
#     boundary since eb1 (block-pii-commit.sh appends the working-tree
#     .beads/issues.jsonl to its trunk-wide scan set on every commit); this layer
#     remains the backstop for human-terminal commits, which bypass the
#     agent-only commit hook entirely.
#
# stdin (git pre-push contract): "<local_ref> <local_sha> <remote_ref> <remote_sha>"
# per ref being pushed.
# TEST ENV (never set in production): PRE_PUSH_PII_SCAN_ROOT — sys.path root for
# the pii_scan import (default: the repo toplevel).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZERO=0000000000000000000000000000000000000000
# git's well-known empty-tree object: the diff base for a push with no usable
# remote base (brand-new repo, no origin/main).
EMPTY_TREE=4b825dc642cb6eb9a060e54bf8d69288fbee4904

TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
if [[ -z "$TOPLEVEL" ]]; then
    echo "pre-push-pii-scan: cannot resolve repo toplevel — blocking (fail-closed)" >&2
    exit 1
fi
cd "$TOPLEVEL" || { echo "pre-push-pii-scan: cd failed — blocking (fail-closed)" >&2; exit 1; }
SCAN_ROOT="${PRE_PUSH_PII_SCAN_ROOT:-$TOPLEVEL}"

# Path scope (PER_SE_DENY_PREFIXES + DATA_BEARING_PREFIXES) single-sourced with the
# commit hook so the two boundaries cannot drift (PR#84 QUAL-1). The install copies
# this hook to .git/hooks/pre-push, where SCRIPT_DIR resolves to .git/hooks, so the
# lib is read from the tracked .claude/hooks/lib via the repo toplevel.
source "$TOPLEVEL/.claude/hooks/lib/pii-scan-scope.sh" 2>/dev/null \
    || source "$SCRIPT_DIR/lib/pii-scan-scope.sh" 2>/dev/null
if [[ -z "${STORE_PREFIX:-}" ]]; then
    echo "pre-push-pii-scan: pii-scan-scope lib failed to load — blocking (fail-closed)" >&2
    exit 1
fi

CHANGED=()
while read -r _local_ref local_sha _remote_ref remote_sha; do
    # Ref deletion pushes carry the zero local sha — nothing outbound to scan.
    [[ -z "${local_sha:-}" || "$local_sha" == "$ZERO" ]] && continue
    if [[ "${remote_sha:-$ZERO}" == "$ZERO" ]]; then
        # New remote ref: base on the mainline merge-base when one exists, else
        # the empty tree (scan everything reachable in the pushed snapshot).
        base=$(git merge-base "$local_sha" origin/main 2>/dev/null) || base=""
        [[ -z "$base" ]] && base="$EMPTY_TREE"
    else
        base="$remote_sha"
    fi
    # core.quotepath=false: a non-ASCII path would otherwise be C-quoted and skip
    # the scan (a silent fail-open — PR#84 BUG-1), matching the commit hook.
    DIFF_OUT=$(git -c core.quotepath=false diff --name-only --diff-filter=ACMRT "$base" "$local_sha" 2>/dev/null)
    DIFF_RC=$?
    if [[ $DIFF_RC -ne 0 ]]; then
        echo "pre-push-pii-scan: git diff failed (rc=$DIFF_RC) enumerating the push range — blocking (fail-closed)" >&2
        exit 1
    fi
    while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        [[ -f "$f" ]] || continue   # changed path no longer on disk -> nothing to read
        CHANGED+=("$f")
    done <<< "$DIFF_OUT"
done

[[ ${#CHANGED[@]} -eq 0 ]] && exit 0

# ── Path denial (PR#84 API-1): a changed file under a per-se-deny prefix is ──────
# operator data by location — block regardless of token hits, mirroring the commit
# hook's conditions 1+2. The human-terminal push path is exactly where a `git add -f`
# past .gitignore can land a filled-scaffold/store file carrying no token.
for f in "${CHANGED[@]}"; do
    for p in "${PER_SE_DENY_PREFIXES[@]}"; do
        case "$f" in
            "$p"*)
                echo "pre-push-pii-scan: PII-FREE-TRUNK: pushed range includes operator-data path '$f' (under '$p'). Remove it from the pushed commits before pushing." >&2
                exit 1 ;;
        esac
    done
done

DATA_BEARING=()
for f in "${CHANGED[@]}"; do
    for p in "${DATA_BEARING_PREFIXES[@]}"; do
        case "$f" in "$p"*) DATA_BEARING+=("$f"); break ;; esac
    done
done

ERR_FILE=$(mktemp)
TOTAL=$(
    PPS_SCAN_ROOT="$SCAN_ROOT" \
    python3 - "${#CHANGED[@]}" "${CHANGED[@]}" ${DATA_BEARING[@]+"${DATA_BEARING[@]}"} <<'PY' 2>"$ERR_FILE"
import os
import sys

sys.path.insert(0, os.environ["PPS_SCAN_ROOT"])
from scripts.guard.pii_scan import scan_scoped

n_changed = int(sys.argv[1])
changed = sys.argv[2:2 + n_changed]
data_bearing = sys.argv[2 + n_changed:]

# Single-sourced scope policy (the dv3 fixture partition + the two-scope scan),
# shared with block-pii-commit.sh so the gate and its backstop cannot drift.
print(scan_scoped(changed, data_bearing))
PY
)
SCAN_RC=$?
SCAN_ERR=$(cat "$ERR_FILE" 2>/dev/null)
rm -f "$ERR_FILE"

if [[ $SCAN_RC -ne 0 ]] || ! [[ "$TOTAL" =~ ^[0-9]+$ ]]; then
    echo "pre-push-pii-scan: content scan failed (rc=$SCAN_RC) — blocking (fail-closed). Detail: ${SCAN_ERR:-no stderr}" >&2
    exit 1
fi

if [[ "$TOTAL" -ge 1 ]]; then
    {
        echo "pre-push-pii-scan: PII-FREE-TRUNK: the pushed range carries operator PII ($TOTAL hit(s)). Offending file(s):"
        echo "$SCAN_ERR" | grep '^PII-HIT: ' | sed 's/^PII-HIT: //' | sort -u | head -8
        echo "Remove the PII (rewrite the offending commits) before pushing."
    } >&2
    exit 1
fi

exit 0
