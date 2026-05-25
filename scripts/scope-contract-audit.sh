#!/usr/bin/env bash
# scope-contract-audit.sh — verifies HANDOFF.md carries a current scope
# contract block per INV-SCOPE-CONTRACT.
#
# Rule (from INVARIANTS.md):
#   "Every session has a written scope contract before any work: Goal, binary
#    ACs, Files I WILL touch, Files I will NOT touch, NOT doing, Invariants
#    at risk."
#
# Audit checks:
#   1. HANDOFF.md contains at least one section matching
#        `## Scope Contract — Session <N>`
#   2. The highest-N scope contract block contains all six required subfields:
#        Goal, Acceptance criteria, Files I WILL touch, Files I will NOT touch,
#        NOT doing, Invariants at risk
#   3. The highest-N block contains at least one binary AC checkbox
#        (`- [ ]` or `- [x]`)
#
# What it does NOT verify (v1 limitations):
#   • Whether N matches the "current session" — there is no canonical source
#     for current-N outside the file itself; the audit assumes the highest-N
#     contract IS the current one. The close-protocol caller is responsible
#     for ensuring a new contract is appended each session.
#   • AC evaluation status at close (PASS/FAIL/CHANGED/N/A) — close-protocol
#     drift-check covers that separately.
#
# Exit codes:
#   0 — audit passed (contract present, well-formed)
#   1 — audit failed (missing or malformed contract)
#   2 — usage error
#
# Usage:
#   scripts/scope-contract-audit.sh                # audits ./HANDOFF.md
#   scripts/scope-contract-audit.sh path/to/file   # audits given path
#   scripts/scope-contract-audit.sh --session 5    # require highest N >= 5

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
                echo "scope-contract-audit: --session requires an integer argument" >&2
                exit 2
            fi
            shift 2
            ;;
        --session=*)
            REQUIRE_SESSION="${1#--session=}"
            shift
            ;;
        -*)
            echo "scope-contract-audit: unknown flag: $1" >&2
            exit 2
            ;;
        *)
            HANDOFF="$1"
            shift
            ;;
    esac
done

if [[ ! -f "$HANDOFF" ]]; then
    echo "scope-contract-audit: file not found: $HANDOFF" >&2
    exit 2
fi

audit_init "scope-contract-audit"

findings=$(python3 - "$HANDOFF" "$REQUIRE_SESSION" <<'PYEOF'
import re, sys

path = sys.argv[1]
require_session_raw = sys.argv[2]
require_session = int(require_session_raw) if require_session_raw else None

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Find all Scope Contract sections.
HEADER_RE = re.compile(r'^##\s+Scope Contract\s+[—–-]\s+Session\s+(\d+)\b', re.IGNORECASE)

contracts = []  # list of dicts: n, header_lineno, end_lineno
current = None
for i, line in enumerate(lines):
    m = HEADER_RE.match(line)
    if m:
        if current is not None:
            current['end'] = i
            contracts.append(current)
        current = {
            'n': int(m.group(1)),
            'start': i,
            'end': len(lines),
            'header': line.rstrip('\n'),
        }
    elif current is not None and re.match(r'^##\s+\S', line):
        # Hit next H2 — close current contract section.
        current['end'] = i
        contracts.append(current)
        current = None
if current is not None:
    contracts.append(current)

violations = []

if not contracts:
    violations.append((
        'INV-SCOPE-CONTRACT',
        0,
        'no `## Scope Contract — Session <N>` section found in file',
    ))
else:
    # Validate the highest-N contract.
    latest = max(contracts, key=lambda c: c['n'])
    body = ''.join(lines[latest['start']:latest['end']])

    REQUIRED_FIELDS = [
        ('Goal',                  re.compile(r'^\s*Goal:',                  re.MULTILINE)),
        ('Acceptance criteria',   re.compile(r'^\s*Acceptance criteria:',   re.MULTILINE)),
        ('Files I WILL touch',    re.compile(r'^\s*Files I WILL touch:',    re.MULTILINE)),
        ('Files I will NOT touch',re.compile(r'^\s*Files I will NOT touch:',re.MULTILINE)),
        ('NOT doing',             re.compile(r'^\s*NOT doing:',             re.MULTILINE)),
        ('Invariants at risk',    re.compile(r'^\s*Invariants at risk:',    re.MULTILINE)),
    ]

    for name, rx in REQUIRED_FIELDS:
        if not rx.search(body):
            violations.append((
                'INV-SCOPE-CONTRACT',
                latest['start'] + 1,
                f"Session {latest['n']} contract missing required field: {name}",
            ))

    # At least one binary AC checkbox.
    if not re.search(r'^\s*-\s+\[[ xX]\]\s+\S', body, re.MULTILINE):
        violations.append((
            'INV-SCOPE-CONTRACT',
            latest['start'] + 1,
            f"Session {latest['n']} contract has no binary AC checkbox (`- [ ]` or `- [x]`)",
        ))

    # --session enforcement.
    if require_session is not None and latest['n'] < require_session:
        violations.append((
            'INV-SCOPE-CONTRACT',
            latest['start'] + 1,
            f'highest contract is Session {latest["n"]}, required >= {require_session}',
        ))

# Emit.
for inv_id, lineno, msg in violations:
    safe_msg = msg.replace('|', '/')
    print(f'{inv_id}|{lineno}|{safe_msg}')

print(f'__STATS__|{len(contracts)}|' +
      (str(max(c["n"] for c in contracts)) if contracts else 'none'))
PYEOF
)

if [[ -z "$findings" ]]; then
    info "no output from analyzer"
    audit_summary
    audit_exit
fi

while IFS='|' read -r inv_id lineno msg; do
    if [[ "$inv_id" == "__STATS__" ]]; then
        info "${lineno} contract(s) found, latest Session ${msg}"
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
