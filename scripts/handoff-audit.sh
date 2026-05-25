#!/usr/bin/env bash
# handoff-audit.sh — audits HANDOFF.md against:
#   • INV-HO-ROTATION (6-clause rotation rule, volatile-section scope)
#   • INV-HO-NO-STALE-HASH (no commit/sha256 hash prefixes in narrative prose)
#
# Mechanical coverage by clause:
#   Clause 1 (replace, don't accrue)            — NOT mechanizable v1
#       Requires prior-version diff to detect accrued prior-session content;
#       defer to v2 once a session-N-versioned HANDOFF snapshot exists.
#   Clause 2 (Historical pointer format)        — ENFORCED
#       Lines starting with `**Historical (kept for reference):**` must have
#       a non-empty target path.
#   Clause 3 (no sha256 prefixes)               — ENFORCED via INV-HO-NO-STALE-HASH
#   Clause 4 (self-dating volatile facts)       — ENFORCED (line OR section header date)
#   Clause 5 (no duplicate Historical labels)   — ENFORCED
#       Each VOLATILE section may mention "Historical" at most once.
#   Clause 6 (session-close diff check)         — NOT mechanizable v1
#       Procedural close-protocol step; requires diff against prior commit.
#
# Section classification:
#   VOLATILE section = any H2/H3 header containing "volatile" or "VOLATILE".
#   All other sections still get the file-wide INV-HO-NO-STALE-HASH check.
#
# Self-dating policy (lenient):
#   A commit SHA in backticks is allowed when EITHER the same line carries a
#   date stamp (YYYY-MM-DD, "Session N", "S<N> close") OR the enclosing
#   section header carries one. Rationale: the invariant exists so staleness
#   is self-evident; a section-header date achieves that for everything in
#   the section without forcing repetition on every line.
#
# Exit codes:
#   0 — audit passed
#   1 — one or more violations recorded
#   2 — usage error (file not found)
#
# Usage:
#   scripts/handoff-audit.sh                 # audits ./HANDOFF.md
#   scripts/handoff-audit.sh path/to/file    # audits given path

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/audit-helpers.sh
source "$SCRIPT_DIR/lib/audit-helpers.sh"

HANDOFF="${1:-$SCRIPT_DIR/../HANDOFF.md}"

if [[ ! -f "$HANDOFF" ]]; then
    echo "handoff-audit: file not found: $HANDOFF" >&2
    exit 2
fi

audit_init "handoff-audit"

# Parse + check in python; emit pipe-delimited violation records on stdout.
findings=$(python3 - "$HANDOFF" <<'PYEOF'
import re, sys

path = sys.argv[1]
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Walk H2/H3 sections.
sections = []  # list of dicts: start (0-indexed line of header), end, header, volatile
current = None
for i, line in enumerate(lines):
    m = re.match(r'^(#{2,3}) (.+?)\s*$', line)
    if m:
        if current is not None:
            current['end'] = i
            sections.append(current)
        header = m.group(2)
        current = {
            'start': i,
            'end': len(lines),
            'header': header,
            'volatile': 'volatile' in header.lower(),
        }
if current is not None:
    sections.append(current)

# Patterns.
DATE_RE = re.compile(r'\b\d{4}-\d{2}-\d{2}\b|\bSession \d+\b|\bS\d+\s+close\b', re.IGNORECASE)
SHA256_LITERAL_RE = re.compile(r'\bsha256[\s:=]+[0-9a-f]{6,}', re.IGNORECASE)
COMMIT_BACKTICK_RE = re.compile(r'`([0-9a-f]{7,40})`')
HISTORICAL_PRESENT_RE = re.compile(r'\bHistorical\b')
HISTORICAL_VALID_RE = re.compile(
    r'^\s*\*\*Historical \(kept for reference\):\*\*\s+\S'
)

violations = []  # list of (inv_id, line_num_1idx, message)

for sec in sections:
    section_dated = bool(DATE_RE.search(sec['header']))

    # File-wide stale-hash check inside this section's body.
    for offset, line in enumerate(lines[sec['start'] + 1:sec['end']]):
        lineno = sec['start'] + 1 + offset + 1  # human 1-indexed

        # Skip code blocks (rough heuristic: 4-space-indented or fenced — fenced not handled in v1).
        # Skip table rows that are commit references like a beads ticket — these are file-wide
        # so we DO want to check them, no skip.

        if SHA256_LITERAL_RE.search(line):
            violations.append((
                'INV-HO-NO-STALE-HASH',
                lineno,
                f'literal sha256 reference: {line.strip()[:100]}',
            ))

        for m in COMMIT_BACKTICK_RE.finditer(line):
            sha = m.group(1)
            # 40-char strings could be full git SHA; either way treat as commit-hash-class.
            line_dated = bool(DATE_RE.search(line))
            if section_dated or line_dated:
                continue
            violations.append((
                'INV-HO-NO-STALE-HASH',
                lineno,
                f"commit SHA `{sha}` without adjacent date (section '{sec['header']}' not self-dated)",
            ))

    # VOLATILE-section-only checks.
    if not sec['volatile']:
        continue

    historical_hits = []  # (lineno, line) where "Historical" appears
    for offset, line in enumerate(lines[sec['start'] + 1:sec['end']]):
        lineno = sec['start'] + 1 + offset + 1
        if HISTORICAL_PRESENT_RE.search(line):
            historical_hits.append((lineno, line))

    # Clause 5: at most one Historical mention per VOLATILE section.
    if len(historical_hits) > 1:
        line_list = ', '.join(str(n) for n, _ in historical_hits)
        violations.append((
            'INV-HO-ROTATION',
            historical_hits[0][0],
            f"section '{sec['header']}' has {len(historical_hits)} 'Historical' mentions "
            f"(lines {line_list}); clause 5 allows at most 1",
        ))

    # Clause 2: Historical pointer line must match canonical format with target.
    for lineno, line in historical_hits:
        # Only validate lines that LOOK like the pointer form.
        if line.lstrip().startswith('**Historical (kept for reference):**'):
            if not HISTORICAL_VALID_RE.search(line):
                violations.append((
                    'INV-HO-ROTATION',
                    lineno,
                    f'Historical pointer line missing target path (clause 2)',
                ))

# Emit pipe-delimited records for bash to consume.
for inv_id, lineno, msg in violations:
    # Replace pipes in msg to keep parsing simple.
    safe_msg = msg.replace('|', '/')
    print(f'{inv_id}|{lineno}|{safe_msg}')

# Sentinel line with section stats for info().
total = len(sections)
vol = sum(1 for s in sections if s['volatile'])
print(f'__STATS__|{total}|{vol}')
PYEOF
)

# Parse python output, route to violation()/info().
if [[ -z "$findings" ]]; then
    info "no output from analyzer (empty HANDOFF?)"
    audit_summary
    audit_exit
fi

while IFS='|' read -r inv_id lineno msg; do
    if [[ "$inv_id" == "__STATS__" ]]; then
        info "scanned ${lineno} section(s), ${msg} marked VOLATILE"
        continue
    fi
    violation "$inv_id" "line ${lineno}: ${msg}"
done <<< "$findings"

audit_summary
audit_exit
