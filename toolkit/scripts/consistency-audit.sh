#!/usr/bin/env bash
# toolkit/scripts/consistency-audit.sh — CROSS-LAYER CONSISTENCY meta-audit.
#
# WHAT IT ENFORCES:
#   A skill library is built in layers (roles/, skills/, commands/, judge rubrics,
#   close protocols) maintained by different hands at different times. Each layer
#   can be internally valid while contradicting another. This audit walks the WHOLE
#   library and FAILs when one layer is inconsistent with another — the failure mode
#   that no single per-file audit can see.
#
#   FINDINGS DRIVING THIS AUDIT:
#     F-019 (self-deny): the role-inlining hook (../hooks/enforce-role-inlining.sh)
#       would BLOCK the library's OWN pipeline skills, because those skills dispatch
#       roles by EMBED / by-path reference instead of inlining the full 11-section
#       profile. A hook that denies the library that ships it is a cross-layer
#       contradiction. CHECK (a) flags every role dispatch the hook would deny.
#     F-020 (phantom role): a skill/command dispatches a role NAME (roles/<slug>/…)
#       for which no agent.md file exists — a dangling reference across the
#       skill->role layer. CHECK (b) flags it.
#     F-006 (threshold drift): a judge rubric scores 99/100 while every sibling
#       rubric uses the >=9/10 convention. A lone off-convention threshold is a
#       silent miscalibration. CHECK (c) flags 99/100 (or N/100) where the
#       library convention is the X/10 family.
#     F-005 (competing protocols): more than ONE file claims to define "the
#       session-close protocol". Two close protocols means neither is canonical.
#       CHECK (d) flags >1 such definer.
#
# BUG-N convention: a real defect found+fixed in an audit is annotated at the fix
# site with `# BUG-N (context): ...` so the negative test proving the fix has a
# stable referent (see ../lib/audit-helpers.sh, ../lib/test-lib.sh, F-007).
#
# CHECK (a) — the TWO-OBJECT dispatch contract (F-019 reconciliation, S4).
# Role profiles have ONE canonical home: roles/<slug>/agent.md. "Is the profile
# present?" is enforced against two different objects by two layers that do NOT
# contradict each other:
#   - STATIC skill/command TEMPLATES (this audit's object): a role reference is
#     SOUND iff it (A) inlines the full canonical profile (10 fixed sections + one
#     operational-slot synonym, F-002), OR (B) carries a sanctioned by-reference
#     marker ON THE SAME LINE as that slug's roles/<slug>/agent.md ref AND the slug
#     resolves to a real profile. The marker is PER-SLUG, never a file-wide blanket
#     waiver (a blanket marker waiving every dispatch in a file is the F-007 hole
#     this check closes). Any other role-shaped reference (bare EMBED, "see
#     roles/<slug>/agent.md", unmarked path) is UNSANCTIONED -> FAIL: an
#     orchestrator following such a template would emit an under-inlined dispatch.
#   - RUNTIME Task DISPATCHES (../hooks/enforce-role-inlining.sh's object): the
#     orchestrator must EXPAND Mode B into the full 11 sections before dispatch;
#     the hook stays strict and DENIES a bare/unexpanded reference at runtime. This
#     audit does NOT relax that — it certifies the template is sound + resolvable;
#     the hook certifies the dispatch is inlined. Together: no cross-layer conflict.
# Non-shipped working dirs (drafts/, .research/) and the toolkit's own
# tests/fixtures/ are excluded from the dispatch scan (BUG-22e class — an audit
# must not flag its own negative-test data or unshipped scratch).
#
# USAGE:
#   consistency-audit.sh --lib <root> [--allow-skip]
#     --lib <root>   library root containing roles/, skills/, commands/, etc.
#     --allow-skip   opt out of fail-closed when a layer is absent (F-008).
#
# Env:
#   AUDIT_ALLOW_SKIP=1                 same as --allow-skip.
#   CONSISTENCY_BYREF_MARKER           regex for the sanctioned by-reference marker
#                                      that the hook would accept (default below).
#   ROLE_REQUIRED_SECTIONS             newline-list overriding the 10 fixed sections.
#   ROLE_OPERATIONAL_SLOT_SYNONYMS     newline-list overriding the operational slot.
#
# Exit: 0 PASS / 1 FAIL (any cross-layer inconsistency) / 2 FATAL (config/absent layer).
#
# Portable across BSD (macOS bash 3.2) and GNU. Dependency-free (no jq/python).

set -uo pipefail

AUDIT_TAG="${AUDIT_TAG:-consistency-audit}"
# shellcheck source=../lib/audit-helpers.sh disable=SC1091
source "$(dirname "$0")/../lib/audit-helpers.sh"

# ---------------------------------------------------------------------------
# CONFIG (overridable via environment) --------------------------------------
# ---------------------------------------------------------------------------

# The 10 fixed canonical sections, kept in lockstep with enforce-role-inlining.sh
# so CHECK (a) judges acceptance by the SAME yardstick the hook applies (F-019).
if [ -n "${ROLE_REQUIRED_SECTIONS:-}" ]; then
  IFS=$'\n' read -r -d '' -a REQUIRED <<< "${ROLE_REQUIRED_SECTIONS}" || true
else
  REQUIRED=(
    "## Identity" "## Core Rules" "## Role Boundaries" "## Ask vs Proceed"
    "## Loop-Breaking" "## Tools" "## Communication" "## Context Loading"
    "## Anti-Patterns" "## Negative Examples"
  )
fi

# The single operational slot — any ONE synonym satisfies it (F-002).
if [ -n "${ROLE_OPERATIONAL_SLOT_SYNONYMS:-}" ]; then
  IFS=$'\n' read -r -d '' -a SLOT_SYNONYMS <<< "${ROLE_OPERATIONAL_SLOT_SYNONYMS}" || true
else
  SLOT_SYNONYMS=( "## Modes" "## Audit Protocol" "## Task Routing" )
fi

# Sanctioned by-reference marker: a dispatch the hook would ACCEPT without full
# inlining (an explicit, auditable opt-out token on the same line as the ref).
BYREF_MARKER="${CONSISTENCY_BYREF_MARKER:-(INLINE-EXEMPT|by-reference: sanctioned|role-ref: sanctioned)}"

# Reference to a role profile, by slug, anywhere in a dispatching file.
AGENTMD_REGEX='roles/[a-z0-9][a-z0-9-]*/agent\.md'

# sha256_first12 <file> — first 12 lowercase hex chars of the file's sha256.
# Portable: prefer `shasum -a 256` (macOS/BSD) else `sha256sum` (GNU), detected once.
if command -v shasum >/dev/null 2>&1; then
  _sha256() { shasum -a 256 "$1" 2>/dev/null; }
elif command -v sha256sum >/dev/null 2>&1; then
  _sha256() { sha256sum "$1" 2>/dev/null; }
else
  _sha256() { return 1; }
fi
sha256_first12() {
  # stdout: first 12 hex chars; exit 1 if no hasher / unreadable file.
  local out
  out="$(_sha256 "$1")" || return 1
  [ -n "$out" ] || return 1
  printf '%s' "${out%% *}" | cut -c1-12
}

# Non-dispatcher opt-out: a calibration/example CORPUS references role paths as
# SUBJECT MATTER (a sample review OF a profile), not as dispatches. Such a file
# declares itself with this explicit, greppable marker so the dispatch scan does
# not mistake a quoted 'roles/<slug>/agent.md' for a dispatch (F-007: the string
# is a signal, not necessarily a dispatch). Deliberate + auditable, like the
# by-reference marker. Override via CONSISTENCY_NONDISPATCH_MARKER.
NONDISPATCH_MARKER="${CONSISTENCY_NONDISPATCH_MARKER:-consistency-audit: not-a-dispatcher}"

# ---------------------------------------------------------------------------
# Argument parsing -----------------------------------------------------------
# ---------------------------------------------------------------------------
LIB=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --lib)        shift; [ "$#" -gt 0 ] || { emit "FATAL: --lib requires a value"; exit 2; }; LIB="$1" ;;
    --lib=*)      LIB="${1#--lib=}" ;;
    --allow-skip) AUDIT_ALLOW_SKIP=1 ;;
    -h|--help)    sed -n '2,40p' "$0"; exit 0 ;;
    --*)          emit "FATAL: unknown arg: $1"; exit 2 ;;
    *)            emit "FATAL: unexpected positional arg: $1 (did you mean --lib $1 ?)"; exit 2 ;;
  esac
  shift
done

if [ -z "$LIB" ]; then
  emit "FATAL: no library root given. Usage: $0 --lib <root> [--allow-skip]"
  exit 2
fi
if [ ! -d "$LIB" ]; then
  emit "FATAL: library root not found: $LIB"
  exit 2
fi
LIB="${LIB%/}"

emit "auditing cross-layer consistency under ${LIB}"

# shipped_filter — drop non-shipped working dirs and (BUG-22e) the toolkit's own
# tests/fixtures from the DISPATCH scan, so the audit never flags its own
# negative-test data or unshipped scratch as a real cross-layer violation.
# vault/ is gitignored local-only knowledge (Obsidian notes, session records) —
# not shipped library content, so its historical mentions of old scores (e.g. a
# past upgrade round's "100/100") are not a live library threshold and must not
# be scanned (bead skills_library-kf4; same non-shipped class as drafts/.research).
# EXEMPTION (BUG-22e pattern): when --lib points AT a fixtures tree (the audit's
# own negative test runs against good/ + bad/ mini-libs UNDER tests/fixtures), we
# must NOT prune tests/fixtures or the whole lib root would vanish. drafts/,
# .research/ and vault/ are always pruned (never a valid lib root for the test).
case "$LIB" in
  *tests/fixtures*) shipped_filter() { grep -Ev '/(drafts|\.research|vault)/' || true; } ;;
  *)                shipped_filter() { grep -Ev '/(drafts|\.research|vault|tests/fixtures)/' || true; } ;;
esac

# ---------------------------------------------------------------------------
# Discover the layers.
# Dispatching files = skills/ + commands/ markdown that reference a role.
# Role profiles = roles/<slug>/agent.md.
# ---------------------------------------------------------------------------
ROLES_DIR="${LIB}/roles"

# dispatch_files — list every skill/command file. Portable, no `find -printf`.
list_dispatch_files() {
  for sub in skills commands; do
    [ -d "${LIB}/${sub}" ] || continue
    # -type f, any depth; restrict to text-ish files (md/sh/txt) to avoid binaries.
    find "${LIB}/${sub}" -type f \( -name '*.md' -o -name '*.sh' -o -name '*.txt' \) 2>/dev/null
  done | shipped_filter
}

DISPATCH_FILES_RAW="$(list_dispatch_files)"

# role_exists <slug> -> 0 if roles/<slug>/agent.md is a real file.
role_exists() {
  [ -f "${ROLES_DIR}/$1/agent.md" ]
}

# profile_fully_inlined <file> — does <file> inline a complete canonical profile?
# Mirrors enforce-role-inlining.sh: all 10 fixed sections present AND >=1 slot synonym.
profile_fully_inlined() {
  local f="$1" section ok=1
  for section in "${REQUIRED[@]}"; do
    grep -qF "$section" "$f" || { ok=0; break; }
  done
  if [ "$ok" -eq 1 ]; then
    local slot slot_ok=0
    for slot in "${SLOT_SYNONYMS[@]}"; do
      grep -qF "$slot" "$f" && { slot_ok=1; break; }
    done
    [ "$slot_ok" -eq 1 ] || ok=0
  fi
  [ "$ok" -eq 1 ]
}

# ---------------------------------------------------------------------------
# CHECK (a) + (b): role dispatches across the skill->role layer.
#
# For every dispatching file that references roles/<slug>/agent.md:
#   (b) the <slug> MUST resolve to a real role file (F-020); else FAIL.
#   (a) if the slug resolves, the dispatch must be one the role-inlining hook
#       ACCEPTS: full profile inlined, OR a sanctioned by-reference marker on the
#       file. A bare/EMBED/by-path dispatch is one the hook DENIES (F-019) -> FAIL.
# ---------------------------------------------------------------------------
checked_dispatch=0
if [ -n "$DISPATCH_FILES_RAW" ]; then
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    [ -f "$f" ] || continue
    # A file that declares itself a non-dispatcher corpus (calibration/example
    # review content quoting role paths as subjects) is skipped in the dispatch
    # scan. Explicit, greppable, deliberate — not a directory heuristic.
    if grep -qF "$NONDISPATCH_MARKER" "$f" 2>/dev/null; then
      emit "  ${f}: declared non-dispatcher corpus (dispatch scan skipped)"
      continue
    fi
    # collect distinct referenced slugs in this file
    slugs="$(grep -oE "$AGENTMD_REGEX" "$f" 2>/dev/null \
              | sed -E 's#^roles/([a-z0-9][a-z0-9-]*)/agent\.md$#\1#' \
              | sort -u)"
    [ -n "$slugs" ] || continue
    checked_dispatch=1
    while IFS= read -r slug; do
      [ -n "$slug" ] || continue
      # (b) F-020: phantom role — the dispatched name has no agent.md.
      if ! role_exists "$slug"; then
        # BUG-020 (phantom dispatch): a dispatch of a nonexistent role slug.
        fail "F-020 phantom role: ${f} dispatches roles/${slug}/agent.md but no such role profile exists"
        continue
      fi
      # (a) Mode B — sanctioned by-reference. The marker must appear ADJACENT to THIS
      # slug's roles/<slug>/agent.md ref (within a ~30-char window, either side), not
      # merely on the same line. Same-line-only acceptance leaked: a line carrying
      # multiple role refs where only one is marked would waive ALL of them (the
      # marker binds to a slug, not to a line). The slug already resolved
      # (role_exists check above), so Mode B is marker + resolution, both verified.
      if grep -qE "${BYREF_MARKER}.{0,30}roles/${slug}/agent\.md|roles/${slug}/agent\.md.{0,30}${BYREF_MARKER}" "$f" 2>/dev/null; then
        # OPTIONAL content pin (15j): a marker may pin the sanctioned profile's
        # content with `roles/<slug>/agent.md sha256:<first12hex>` right after the
        # slug path. When pinned, the CURRENT profile hash must match the pin —
        # else the profile DRIFTED behind a stale reference (a section removed /
        # content rewritten) while the marker still says "sanctioned". Pinning is
        # OPT-IN: an unpinned marker is accepted on marker + resolution as before.
        pin="$(grep -oE "roles/${slug}/agent\.md sha256:[0-9a-f]{12}" "$f" 2>/dev/null \
                | head -n1 | sed -E 's/.*sha256:([0-9a-f]{12})$/\1/')"
        if [ -n "$pin" ]; then
          actual="$(sha256_first12 "${ROLES_DIR}/${slug}/agent.md")" || actual=""
          if [ -z "$actual" ]; then
            skipped "cannot verify content pin for roles/${slug}/agent.md (no sha256 tool or unreadable profile)"
            continue
          fi
          if [ "$actual" != "$pin" ]; then
            # BUG-15j (stale content pin): the sanctioned profile drifted behind a
            # stale by-reference. The marker still says "sanctioned" but the file
            # changed since it was pinned.
            fail "profile drift behind a stale reference: roles/${slug}/agent.md content changed since it was sanctioned (pinned ${pin}, now ${actual}); re-sanction with the current hash"
            continue
          fi
          emit "  ${f}: role '${slug}' sanctioned by-reference (content pin sha256:${pin} verified)"
          continue
        fi
        emit "  ${f}: role '${slug}' sanctioned by-reference (adjacent per-slug marker + resolves)"
        continue
      fi
      # (a) Mode A — full inline.
      if profile_fully_inlined "$f"; then
        emit "  ${f}: role '${slug}' fully inlined (Mode A)"
        continue
      fi
      # BUG-019 (unsanctioned reference): a static template that references a role
      # but neither inlines it (Mode A) nor sanctions it per-slug (Mode B). An
      # orchestrator following this template would emit an under-inlined runtime
      # dispatch that enforce-role-inlining.sh DENIES (INV-PROFILE-INLINING).
      fail "F-019 unsanctioned role reference: ${f} references role '${slug}' but neither inlines the full 11-section profile (Mode A) nor carries a sanctioned per-slug by-reference marker (Mode B) — a faithful dispatch from this template would be hook-DENIED at runtime"
    done <<< "$slugs"
  done <<< "$DISPATCH_FILES_RAW"
fi

if [ "$checked_dispatch" -eq 0 ]; then
  # No role dispatches found at all -> the cross-layer property is unverifiable.
  skipped "no role-dispatching skill/command files found under ${LIB} (F-019/F-020 unverifiable)"
else
  emit "role-dispatch consistency: walked skill/command -> role references"
fi

# ---------------------------------------------------------------------------
# CHECK (c): the DISPROVEN 99/100 judge-pass target (F-006).
#
# F-006 is NOT "any N/100". The framework's genesis project disproved one specific
# anti-pattern: a LITERAL 99/100 (or 100/100) judge-PASS target chased via
# multi-attempt iteration — unreachable (field scores capped 88-96) and
# counterproductive. The framework EXPLICITLY KEEPS per-finding confidence /
# source-credibility 0-100 SCORES (Discipline 6: "separate confidence (0-100) from
# a judge PASS threshold"). So this check flags only the literal 99/100|100/100
# pass-target — NOT graduated lower bars (85/100, 92/100) or 0-100 metrics — and
# EXEMPTS meta-prose that merely names 99/100 to discuss its removal (F-007: the
# string is a signal, an active unreachable pass-gate is the property).
# ---------------------------------------------------------------------------
# Scope: text files across the lib, MINUS non-shipped + the toolkit's own
# tests/fixtures (BUG-22e class — never flag our own negative-test data).
THRESH_FILES="$(find "$LIB" -type f \( -name '*.md' -o -name '*.txt' \) 2>/dev/null | shipped_filter)"

# The disproven literal target: a WHOLE-number 99 (or 100) over 100. The left
# boundary rejects a leading digit OR decimal point so "199/100", "99/1000", and a
# fractional "8.99/100" do NOT match; the right boundary rejects a trailing digit
# ("99/1000"). Graduated lower bars (85/100, 92/100) and 0-100 confidence/
# credibility SCORES are legitimate and deliberately NOT matched.
drift_re='(^|[^0-9.])(99|100)[[:space:]]*/[[:space:]]*100([^0-9]|$)'
# A hit is EXEMPT only when a removal/negation word sits BEFORE the number on the
# same line (the framework changelog: "DELETE/Removed the literal 99/100"; a rubric
# fix: "not an unreachable 99/100"). Adjacency is required: a bare "literal" or an
# "F-006" citation does NOT exempt — citing a finding id does not make a gate
# inactive ("Pass threshold: require a literal 99/100" must still FAIL). Word-AFTER-
# number does not exempt either ("99/100 supersedes the old bar" is an ACTIVE gate).
removal_adj='([Dd]elet|[Rr]emov|[Dd]isprov|[Ss]upersed|[Rr]etir|[Dd]ropp|[Kk]ill|[Nn]o longer|not |never |n.t )[^0-9]{0,60}(99|100)[[:space:]]*/[[:space:]]*100'

f006_hits=""
if [ -n "$THRESH_FILES" ]; then
  while IFS= read -r tf; do
    [ -n "$tf" ] || continue
    # grep -n -> "lineno:content"; drop only lines whose 99/100 is preceded by a
    # removal/negation word (signal != property — an active gate is not exempted
    # by an incidental keyword elsewhere on the line).
    matches="$(grep -nE "$drift_re" "$tf" 2>/dev/null | grep -ivE "$removal_adj" || true)"
    [ -n "$matches" ] || continue
    while IFS= read -r m; do
      [ -n "$m" ] || continue
      f006_hits="${f006_hits}${tf}:${m}"$'\n'
    done <<< "$matches"
  done <<< "$THRESH_FILES"
fi

if [ -n "$f006_hits" ]; then
  while IFS= read -r hit; do
    [ -n "$hit" ] || continue
    # BUG-006 (threshold drift): an active, unreachable literal 99/100 judge-PASS
    # target (genesis-disproven). Use >=9/10 per dimension + bounded revise + run-it.
    fail "F-006 threshold drift: unreachable literal 99/100 judge-pass target (genesis-disproven — use >=9/10 + bounded revise + executed verification) — ${hit}"
  done <<< "$f006_hits"
else
  emit "judge-threshold convention: no disproven 99/100 judge-pass target (graduated bars + 0-100 confidence/credibility scores are not flagged)"
fi

# ---------------------------------------------------------------------------
# CHECK (d): exactly ONE definer of "the session-close protocol" (F-005).
#
# A file DEFINES the close protocol if it both names it and declares it (a heading
# or a "the session-close protocol" definitional phrase). >1 definer = competing
# protocols, neither canonical -> FAIL.
# ---------------------------------------------------------------------------
# Docs only (.md/.txt) — a close protocol is DEFINED in documentation, never in a
# .sh; scanning .sh false-counted shell comments (a '#' comment looks like a heading,
# and "close-protocol" in an audit's own header is a MENTION). Exclude the toolkit's
# own tests/fixtures (the F-005 negative-test data DELIBERATELY competes) + non-shipped.
ALL_TEXT="$(find "$LIB" -type f \( -name '*.md' -o -name '*.txt' \) 2>/dev/null | shipped_filter)"
# Definitional signal: a HEADING that names the close protocol. The bare definite-
# article phrase "the session-close protocol" is a MENTION (prose pointing AT it, an
# adoption step) — NOT a definition — and is deliberately NOT matched (signal !=
# property: a doc that references the protocol is not a competing definer of it).
define_re='^#+[[:space:]].*([Ss]ession[- ][Cc]lose|[Cc]lose)[- ][Pp]rotocol'

# A close-protocol section that is NOT the canonical definition declares its kind:
# a project INSTANCE (a specific project's own protocol), a GENERATOR (a template
# that writes the protocol into a new project), or a DERIVED extract (a deep-dive
# that points at the canonical). These are sanctioned-distinct (CDM-3: one owner,
# others point) — they are not competing canonical definers and are not counted.
CLOSE_NONCANON_MARKER="${CONSISTENCY_CLOSE_NONCANON_MARKER:-close-protocol:[[:space:]]*(instance|generator|derived)}"

close_definers=""
close_count=0
if [ -n "$ALL_TEXT" ]; then
  while IFS= read -r cf; do
    [ -n "$cf" ] || continue
    if grep -qE "$define_re" "$cf" 2>/dev/null; then
      if grep -qE "$CLOSE_NONCANON_MARKER" "$cf" 2>/dev/null; then
        emit "  ${cf}: sanctioned non-canonical close protocol (instance/generator/derived) — not counted"
        continue
      fi
      close_definers="${close_definers}${cf}"$'\n'
      close_count=$((close_count + 1))
    fi
  done <<< "$ALL_TEXT"
fi

if [ "$close_count" -gt 1 ]; then
  # BUG-005 (competing close protocols): more than one file defines THE close protocol.
  defs="$(printf '%s' "$close_definers" | tr '\n' ' ')"
  fail "F-005 competing close protocols: ${close_count} files each define 'the session-close protocol' (expected at most 1): ${defs}"
elif [ "$close_count" -eq 1 ]; then
  emit "session-close protocol: exactly one canonical definer (consistent)"
else
  emit "session-close protocol: no definer present (nothing to deconflict)"
fi

verdict
