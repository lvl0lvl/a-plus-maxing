#!/usr/bin/env bash
# pf-attestation-audit.sh — verifies HANDOFF.md carries a process-failure
# attestation line for the current session per INV-PF-ATTESTATION.
#
# Rule (from INVARIANTS.md):
#   "Every session close either appends a PF entry OR explicitly attests
#    'No new PF-class entries this session' with rationale."
#
# CLAUDE.md close protocol step 4 prescribes the attestation form:
#     S<N> close (YYYY-MM-DD): <attestation text — affirmative or negative>
#
# Examples that satisfy the audit (both are valid — the rule accepts either):
#   S4 close (2026-05-25): One new PF entry promoted (PF-S3-01, ...). No
#   additional PF-class incidents observed during the S4 work.
#
#   S6 close (2026-06-10): No new PF-class entries this session. Two
#   surprises observed but neither rose to PF level (...).
#
# Audit checks:
#   1. HANDOFF.md contains at least one line matching the canonical
#      attestation prefix `S<N> close (YYYY-MM-DD):` followed by content.
#   2. If --session N is supplied, the highest-N attestation must match.
#
# What it does NOT verify (v1 limitations):
#   • Semantic correctness of the attestation text (whether the "No new PF"
#     claim is honest). That is human-judgment territory; the close-protocol
#     drift checks cover it separately.
#   • Cross-reference against memory/process-failures.md — a future v2 can
#     require that "X new PF entry" lines correspond to actual new entries
#     in the log, but v1 just enforces presence of the attestation line.
#
# Exit codes:
#   0 — attestation present (and matches --session N if supplied)
#   1 — attestation missing or session mismatch
#   2 — usage error
#
# Usage:
#   scripts/pf-attestation-audit.sh                # audits ./HANDOFF.md
#   scripts/pf-attestation-audit.sh path/to/file
#   scripts/pf-attestation-audit.sh --session 5    # require highest N = 5

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/audit-helpers.sh
source "$SCRIPT_DIR/lib/audit-helpers.sh"

HANDOFF="$SCRIPT_DIR/../HANDOFF.md"
REQUIRE_SESSION=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --session)
            REQUIRE_SESSION="${2:-}"
            if [[ -z "$REQUIRE_SESSION" ]]; then
                echo "pf-attestation-audit: --session requires an integer argument" >&2
                exit 2
            fi
            shift 2
            ;;
        --session=*)
            REQUIRE_SESSION="${1#--session=}"
            shift
            ;;
        -*)
            echo "pf-attestation-audit: unknown flag: $1" >&2
            exit 2
            ;;
        *)
            HANDOFF="$1"
            shift
            ;;
    esac
done

if [[ ! -f "$HANDOFF" ]]; then
    echo "pf-attestation-audit: file not found: $HANDOFF" >&2
    exit 2
fi

audit_init "pf-attestation-audit"

findings=$(python3 - "$HANDOFF" "$REQUIRE_SESSION" <<'PYEOF'
import re, sys

path = sys.argv[1]
require_session_raw = sys.argv[2]
require_session = int(require_session_raw) if require_session_raw else None

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Canonical attestation line:
#   S<N> close (YYYY-MM-DD): <non-empty rest>
ATTEST_RE = re.compile(
    r'^\s*S(\d+)\s+close\s+\((\d{4}-\d{2}-\d{2})\):\s+\S'
)

hits = []  # list of (n, date, lineno, text)
for i, line in enumerate(lines, start=1):
    m = ATTEST_RE.match(line)
    if m:
        hits.append((int(m.group(1)), m.group(2), i, line.rstrip('\n')))

violations = []

if not hits:
    violations.append((
        'INV-PF-ATTESTATION',
        0,
        'no `S<N> close (YYYY-MM-DD):` attestation line found in HANDOFF.md',
    ))
else:
    latest = max(hits, key=lambda h: h[0])
    if require_session is not None and latest[0] != require_session:
        violations.append((
            'INV-PF-ATTESTATION',
            latest[2],
            f'latest attestation is Session {latest[0]}, --session required {require_session}',
        ))

for inv_id, lineno, msg in violations:
    safe_msg = msg.replace('|', '/')
    print(f'{inv_id}|{lineno}|{safe_msg}')

# Sentinel: count + latest N + latest date.
if hits:
    latest = max(hits, key=lambda h: h[0])
    print(f'__STATS__|{len(hits)}|S{latest[0]} ({latest[1]})')
else:
    print(f'__STATS__|0|none')
PYEOF
)

if [[ -z "$findings" ]]; then
    info "no output from analyzer"
    audit_summary
    audit_exit
fi

while IFS='|' read -r inv_id lineno msg; do
    if [[ "$inv_id" == "__STATS__" ]]; then
        info "${lineno} attestation line(s) found; latest ${msg}"
        continue
    fi
    if [[ "$lineno" == "0" ]]; then
        violation "$inv_id" "$msg"
    else
        violation "$inv_id" "line ${lineno}: ${msg}"
    fi
done <<< "$findings"

audit_summary
audit_exit
