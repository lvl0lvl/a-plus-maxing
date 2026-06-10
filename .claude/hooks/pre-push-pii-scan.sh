#!/bin/bash
# pre-push-pii-scan.sh — git pre-push hook (bead dv3). PII backstop on the push range.
#
# block-pii-commit.sh gates only AGENT-issued git commits inside a Claude session;
# commits from a human terminal/IDE (and anything the commit-time scan missed)
# bypass it entirely. This git-native pre-push hook is the defense-in-depth
# backstop at the LAST local boundary before content reaches the remote: it scans
# every file changed in the pushed range with the SAME two scopes as the commit
# hook (the SEC-01(a) reuse contract — scripts/guard/pii_scan.scan, no bash/grep
# token reimplementation):
#   • trunk-wide — structural store-line patterns + the operator-contact tokens
#     (gitignored config; empty on a fresh clone -> structural only)
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
#     question belongs to a history audit, not a push gate.
#
# stdin (git pre-push contract): "<local_ref> <local_sha> <remote_ref> <remote_sha>"
# per ref being pushed.
# TEST ENV (never set in production): PRE_PUSH_PII_SCAN_ROOT — sys.path root for
# the pii_scan import (default: the repo toplevel).

set -uo pipefail

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

# Same data-bearing partition as block-pii-commit.sh (the identity-scan scope).
DATA_BEARING_PREFIXES=("vault/scaffold/filled/" "vault/store/" "vault/dna/raw/" "vault/labs/raw/")

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
    DIFF_OUT=$(git diff --name-only --diff-filter=ACMRT "$base" "$local_sha" 2>/dev/null)
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
from scripts.guard.pii_scan import scan, DEFAULT_CONTACT_CONFIG, DEFAULT_IDENTITY_CONFIG

n_changed = int(sys.argv[1])
changed = sys.argv[2:2 + n_changed]
data_bearing = sys.argv[2 + n_changed:]

# Known-fixture partition (dv3, mirrors block-pii-commit.sh): tests/ fixtures
# embed synthetic reading-shaped literals by construction, so the structural
# patterns run only outside tests/; fixture paths still get the contact tokens.
fixtures = [f for f in changed if f.startswith("tests/")]
non_fixtures = [f for f in changed if not f.startswith("tests/")]

trunk = scan(non_fixtures, identity_config=DEFAULT_CONTACT_CONFIG)
trunk += scan(fixtures, identity_config=DEFAULT_CONTACT_CONFIG, include_structural=False)
identity = scan(data_bearing, identity_config=DEFAULT_IDENTITY_CONFIG) if data_bearing else 0

print(trunk + identity)
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
