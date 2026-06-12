#!/usr/bin/env bash
# skill-trace-audit.sh — verifies memory/process-failures.md carries, for the
# given session, a close attestation that enumerates per-PR gated-skill
# invocation evidence. PF-S39/S40/S51-family structural fix (bead lz01).
#
# Rule (the S51 interim guard, now mechanical):
#   "The close attestation MUST carry a per-PR invocation table" — one row per
#   PR lifecycle run in-session, attesting /review-pr and /merge were each
#   invoked fresh via the Skill tool (YES) or recording the lapse (NO plus an
#   explicit violation marker).
#
# Audit checks (scoped to the `## Session <N>` section of the PF log):
#   1. The section exists and carries an S<N>-close attestation marker for
#      session N — either the canonical line form pf-attestation-audit.sh
#      validates in HANDOFF.md (`S<N> close (YYYY-MM-DD):`) or the PF-log
#      header form (`### S<N> close attestation (YYYY-MM-DD)`). Canonical-line
#      validation stays pf-attestation-audit.sh's job; this audit only locates
#      the attestation inside the session section.
#   2. The section contains a per-PR invocation table: a markdown table whose
#      header row names a PR column, a `/review-pr` invoked-fresh column, and
#      a `/merge` invoked-fresh column (the S51 shape).
#   3. Every data row's two invocation cells each start with YES, or start
#      with NO and contain the word "violation" (the S51 convention:
#      "**NO — ... (violation, recorded ...)**"). A NO cell without the word
#      "violation" FAILS — an unexplained NO is an unrecorded violation.
#   4. The table has >= 1 data row, UNLESS the section carries the exact
#      zero-PR escape-hatch sentence:
#          No PR lifecycles ran this session.
#      With that sentence present, checks 2 and 4 are waived (nothing to
#      enumerate); any table that IS present is still row-validated (check 3).
#
# Honest limits — this is a RECORD-shape audit, not a transcript-trace audit:
#   it verifies the close attestation ENUMERATES per-PR invocation evidence in
#   the mandated shape. It cannot itself distinguish invoked-fresh from
#   ran-from-cached-context — that distinction is what the table ATTESTS, and
#   its truthfulness remains the orchestrator's at-close responsibility (the
#   session transcript is the only ground truth, and this script does not
#   read it).
#
# Exit codes:
#   0 — record shape conforms
#   1 — one or more violations
#   2 — usage error (missing/non-integer --session, missing file, analyzer
#       failure — never a silent pass)
#
# Usage:
#   scripts/skill-trace-audit.sh --session 52
#   scripts/skill-trace-audit.sh --session 52 --file path/to/pf-log.md

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/audit-helpers.sh
source "$SCRIPT_DIR/lib/audit-helpers.sh"

PF_LOG="$SCRIPT_DIR/../memory/process-failures.md"
REQUIRE_SESSION=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --session)
            REQUIRE_SESSION="${2:-}"
            if [[ -z "$REQUIRE_SESSION" ]]; then
                echo "skill-trace-audit: --session requires an integer argument" >&2
                exit 2
            fi
            shift 2
            ;;
        --session=*)
            REQUIRE_SESSION="${1#--session=}"
            shift
            ;;
        --file)
            PF_LOG="${2:-}"
            if [[ -z "$PF_LOG" ]]; then
                echo "skill-trace-audit: --file requires a path argument" >&2
                exit 2
            fi
            shift 2
            ;;
        --file=*)
            PF_LOG="${1#--file=}"
            shift
            ;;
        *)
            echo "skill-trace-audit: unknown argument: $1" >&2
            exit 2
            ;;
    esac
done

if [[ -z "$REQUIRE_SESSION" ]]; then
    echo "skill-trace-audit: --session <N> is required" >&2
    exit 2
fi
# Non-integer N would crash the analyzer and fall into the empty-findings
# path; reject up front so a bad invocation can never read as a pass.
if [[ ! "$REQUIRE_SESSION" =~ ^[0-9]+$ ]]; then
    echo "skill-trace-audit: --session must be an integer, got: $REQUIRE_SESSION" >&2
    exit 2
fi

if [[ ! -f "$PF_LOG" ]]; then
    echo "skill-trace-audit: file not found: $PF_LOG" >&2
    exit 2
fi

audit_init "skill-trace-audit"

findings=$(python3 - "$PF_LOG" "$REQUIRE_SESSION" <<'PYEOF'
import re, sys

path = sys.argv[1]
n = int(sys.argv[2])

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# ── Locate the `## Session <N>` section (H2 to next H2 or EOF). ──────────
SESSION_RE = re.compile(r'^##\s+Session\s+(\d+)\b')
H2_RE = re.compile(r'^##\s+\S')

start = None
for i, line in enumerate(lines):
    m = SESSION_RE.match(line)
    if m and int(m.group(1)) == n:
        start = i
        break

violations = []  # (lineno_1idx, message); 0 = no line anchor

if start is None:
    violations.append((0, f'no `## Session {n}` section found in PF log'))
    for lineno, msg in violations:
        print(f'INV-SKILL-TRACE|{lineno}|{msg.replace("|", "/")}')
    print('__STATS__|0|0 data row(s)')
    sys.exit(0)

end = len(lines)
for i in range(start + 1, len(lines)):
    if H2_RE.match(lines[i]):
        end = i
        break

section = lines[start:end]
body = ''.join(section)

# ── Check 1: S<N>-close attestation marker (line form or header form). ───
ATTEST_RE = re.compile(
    r'^\s*(?:#{1,6}\s+)?S(\d+)\s+close(?:\s+attestation)?\s*\((\d{4}-\d{2}-\d{2})\)'
)
attest_ns = []
for line in section:
    m = ATTEST_RE.match(line)
    if m:
        attest_ns.append(int(m.group(1)))
if n not in attest_ns:
    if attest_ns:
        others = ', '.join(f'S{x}' for x in sorted(set(attest_ns)))
        violations.append((
            start + 1,
            f'close attestation in the Session {n} section is for {others}, not S{n}',
        ))
    else:
        violations.append((
            start + 1,
            f'no S{n} close attestation found in the Session {n} section',
        ))

# ── Zero-PR escape hatch (exact sentence). ────────────────────────────────
no_lifecycle = 'No PR lifecycles ran this session.' in body

# ── Check 2: find per-PR invocation table(s). ─────────────────────────────
def cells(line):
    parts = [c.strip() for c in line.strip().split('|')]
    if parts and parts[0] == '':
        parts = parts[1:]
    if parts and parts[-1] == '':
        parts = parts[:-1]
    return parts

def is_separator(row):
    return all(re.fullmatch(r':?-{2,}:?|:?-:?', c) for c in row) and len(row) > 0

def norm(cell):
    return cell.strip().strip('*_').strip()

n_tables = 0
n_rows = 0

i = 0
while i < len(section):
    line = section[i]
    if not line.lstrip().startswith('|'):
        i += 1
        continue
    header = cells(line)
    pr_col = review_col = merge_col = None
    for idx, c in enumerate(header):
        c_plain = re.sub(r'[`*_]', '', c).strip()
        low = c_plain.lower()
        if re.fullmatch(r'pr', low):
            pr_col = idx
        elif '/review-pr' in low and 'invoked' in low and 'fresh' in low:
            review_col = idx
        elif '/merge' in low and 'invoked' in low and 'fresh' in low:
            merge_col = idx
    if pr_col is None or review_col is None or merge_col is None:
        i += 1
        continue

    n_tables += 1
    i += 1
    # Skip the markdown separator row.
    if i < len(section) and section[i].lstrip().startswith('|') \
            and is_separator(cells(section[i])):
        i += 1

    while i < len(section) and section[i].lstrip().startswith('|'):
        row = cells(section[i])
        lineno = start + i + 1  # human 1-indexed
        if is_separator(row):
            i += 1
            continue
        n_rows += 1
        if len(row) <= max(review_col, merge_col):
            violations.append((
                lineno,
                f'malformed data row (fewer cells than the header): {section[i].strip()[:80]}',
            ))
            i += 1
            continue
        pr_label = row[pr_col] if pr_col < len(row) else '?'
        for col, skill in ((review_col, '/review-pr'), (merge_col, '/merge')):
            cell = row[col]
            v = norm(cell)
            if v.startswith('YES'):
                continue
            if v.startswith('NO'):
                if not re.search(r'\bviolation\b', cell, re.IGNORECASE):
                    violations.append((
                        lineno,
                        f'row {pr_label}: {skill} cell starts with NO but lacks '
                        f'the word "violation" — an unexplained NO is an '
                        f'unrecorded violation',
                    ))
                continue
            violations.append((
                lineno,
                f'row {pr_label}: {skill} cell starts with neither YES nor NO: '
                f'{cell[:60]}',
            ))
        i += 1

# ── Checks 2 + 4: table existence / row count, escape-hatch-aware. ───────
if n_tables == 0 and not no_lifecycle:
    violations.append((
        start + 1,
        f'no per-PR invocation table found in the Session {n} section '
        f'(and no "No PR lifecycles ran this session." sentence)',
    ))
if n_tables > 0 and n_rows == 0 and not no_lifecycle:
    violations.append((
        start + 1,
        f'per-PR invocation table has no data rows '
        f'(and no "No PR lifecycles ran this session." sentence)',
    ))

for lineno, msg in violations:
    print(f'INV-SKILL-TRACE|{lineno}|{msg.replace("|", "/")}')

hatch = '; zero-PR escape hatch present' if no_lifecycle else ''
print(f'__STATS__|{n_tables}|{n_rows} data row(s) (Session {n}){hatch}')
PYEOF
)
analyzer_rc=$?

if [[ $analyzer_rc -ne 0 || -z "$findings" ]]; then
    # Never let an analyzer crash read as a clean audit.
    echo "skill-trace-audit: analyzer failed (rc=$analyzer_rc)" >&2
    exit 2
fi

while IFS='|' read -r inv_id lineno msg; do
    if [[ "$inv_id" == "__STATS__" ]]; then
        info "${lineno} invocation table(s) found; ${msg}"
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
