#!/usr/bin/env bash
# role-completeness-audit.sh — at-rest verification that every role profile
# (roles/<slug>/agent.md) carries the canonical 11-section structure the
# enforce-role-inlining.sh DISPATCH hook requires.
#
# WHY (surfaced S10, bead `bue`): the dispatch hook (INV-PROFILE-INLINING) fires
# only when an agent is actually dispatched with the role. consistency-audit
# checks that role REFERENCES resolve, not that each profile is structurally
# complete. So a role missing a canonical section — e.g. game-designer's absent
# operational slot (bead `0c8`) — ships silently and only fails at dispatch time.
# This audit is the AT-REST twin of the dispatch hook: it catches the broken
# profile in the repo, before anything tries to dispatch it.
#
# Required structure (mirrors enforce-role-inlining.sh EXACTLY):
#   10 fixed sections + 1 operational slot (## Modes | ## Audit Protocol | ## Task Routing).
#
# Exit: 0 PASS / 1 FAIL (a profile missing a section) / 2 FATAL (bad args / no roles).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_TAG="role-completeness-audit"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

LIB=""
while [ $# -gt 0 ]; do
  case "$1" in
    --lib) LIB="${2:-}"; shift 2 ;;
    --lib=*) LIB="${1#--lib=}"; shift ;;
    *) emit "FATAL: unknown arg: $1"; exit 2 ;;
  esac
done
[ -n "$LIB" ] || { emit "FATAL: --lib <library-root> is required"; exit 2; }
[ -d "$LIB/roles" ] || { emit "FATAL: no roles/ dir under $LIB"; exit 2; }

# The 10 fixed canonical sections (verbatim from enforce-role-inlining.sh).
REQUIRED=(
  "## Identity" "## Core Rules" "## Role Boundaries" "## Ask vs Proceed"
  "## Loop-Breaking" "## Tools" "## Communication" "## Context Loading"
  "## Anti-Patterns" "## Negative Examples"
)
# The 9th operational slot varies by role.
SLOTS=( "## Modes" "## Audit Protocol" "## Task Routing" )

# validate_frontmatter <slug> <profile-path>
# If the profile begins with a `---` YAML frontmatter block, verify (a) the block
# is valid YAML and (b) it carries non-empty name/title/description keys. A profile
# WITHOUT a frontmatter block is allowed (backward compat) — this is a no-op then.
# WHY (dogfooding finding): roles/*/agent.md frontmatter is parsed by downstream
# consumers (the website build, gray-matter). Unquoted colons produced invalid YAML
# that these section-grep audits passed while the website build FAILED. The library
# must validate what tools depend on.
validate_frontmatter() {
  local slug="$1" prof="$2"
  # Frontmatter only counts when `---` is the VERY FIRST line of the file.
  IFS= read -r first_line < "$prof" || first_line=""
  [ "$first_line" = "---" ] || return 0   # no frontmatter block -> nothing to validate

  # BUG-1 (W1-1, 2026-07-02): PyYAML is an OPTIONAL dependency for this SECONDARY
  # sub-check only. The audit's load-bearing property — the 10+1 section-completeness
  # that mirrors the dispatch hook — is dependency-free and always runs. The
  # frontmatter YAML lint is the only part that needs PyYAML, so it is a documented
  # optional-dep non-blocker (parity with lib/gate_attest.py's optional
  # python3+jsonschema, which loud-skips so the suite stays green). We WARN (loud,
  # non-gating) rather than skipped()/FATAL: the prior skipped() forced the WHOLE
  # section audit to FATAL on any box without PyYAML, making it perpetually-red
  # (PF-S1-05) and taking run-all-tests.sh — and therefore close-audit once it runs
  # the suite — permanently red. F-008 still bites where it matters: the property
  # that CANNOT be verified without the dep (frontmatter YAML) is loudly flagged
  # unverified, never reported clean; the section property, verifiable without the
  # dep, still decides PASS/FAIL. When PyYAML IS present, invalid-YAML / missing-key
  # frontmatter still FAILs — the negative test proves that direction still bites.
  if ! python3 -c "import yaml" >/dev/null 2>&1; then
    warn "role '$slug' frontmatter: python3+PyYAML unavailable — YAML lint NOT run (section-completeness still enforced)"
    return 0
  fi

  local result
  result="$(python3 - "$prof" <<'PY'
import sys, yaml
path = sys.argv[1]
with open(path, "r", encoding="utf-8") as fh:
    text = fh.read()
lines = text.split("\n")
# lines[0] is the opening '---'; find the closing '---'.
end = None
for i in range(1, len(lines)):
    if lines[i].strip() == "---":
        end = i
        break
if end is None:
    print("no-close")
    sys.exit(0)
block = "\n".join(lines[1:end])
try:
    data = yaml.safe_load(block)
except yaml.YAMLError as e:
    msg = " ".join(str(e).split())
    print("invalid-yaml\t" + msg)
    sys.exit(0)
if not isinstance(data, dict):
    print("not-mapping")
    sys.exit(0)
missing = [k for k in ("name", "title", "description")
           if k not in data
           or data[k] is None
           or str(data[k]).strip() == ""]
if missing:
    print("missing-keys\t" + ",".join(missing))
    sys.exit(0)
print("ok")
PY
)"

  local code="${result%%	*}"
  local detail="${result#*	}"
  case "$code" in
    ok)          emit "role '$slug': frontmatter valid (name/title/description present)" ;;
    no-close)    fail "role '$slug' frontmatter: opening '---' has no closing '---' delimiter" ;;
    invalid-yaml) fail "role '$slug' frontmatter: invalid YAML — $detail" ;;
    not-mapping) fail "role '$slug' frontmatter: not a YAML mapping (expected name/title/description keys)" ;;
    missing-keys) fail "role '$slug' frontmatter: missing or empty required key(s): $detail" ;;
    *)           fail "role '$slug' frontmatter: validator produced unexpected output: '$result'" ;;
  esac
}

found_any=0
for prof in "$LIB"/roles/*/agent.md; do
  [ -f "$prof" ] || continue
  found_any=1
  slug="$(basename "$(dirname "$prof")")"
  missing=""
  for sec in "${REQUIRED[@]}"; do
    grep -qF "$sec" "$prof" || missing="$missing '$sec'"
  done
  slot_ok=0
  for slot in "${SLOTS[@]}"; do
    grep -qF "$slot" "$prof" && { slot_ok=1; break; }
  done
  [ "$slot_ok" -eq 1 ] || missing="$missing '## Modes (or ## Audit Protocol / ## Task Routing)'"
  if [ -n "$missing" ]; then
    fail "role '$slug' incomplete — missing:$missing — would be DENIED by enforce-role-inlining on dispatch"
  else
    emit "role '$slug': complete (11 sections)"
  fi
  validate_frontmatter "$slug" "$prof"
done

[ "$found_any" -eq 1 ] || { emit "FATAL: no roles/*/agent.md profiles found under $LIB"; exit 2; }
verdict
