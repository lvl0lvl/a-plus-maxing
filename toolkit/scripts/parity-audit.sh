#!/usr/bin/env bash
# parity-audit.sh — rigor framework canonical audit (cross-cutting mechanism).
#
# ENFORCES: CATALOG <-> DISK <-> DEPLOYED parity for a skills-library-like tree.
#   Finding F-022 (the cracked reference/deployment layer): ~44% of the library was
#   non-functional because referenced/deployed artifacts were MISSING and nothing
#   checked. A skill that cites `references/rubric-methodology.md`, a command that
#   points at `~/.claude/commands/review-pr.md`, a role wired in via
#   `roles/<slug>/agent.md`, a UI skill that is a dead symlink, a `references/` bundle
#   with no SKILL.md to consume it — every one of these is a SILENT crack: the index
#   declares it, but the byte is not on disk / not deployed. This audit closes the
#   crack by resolving every declared artifact and every in-file reference to a real
#   path, and failing closed when one does not resolve.
#
#   Generalized: takes NO hardcoded project paths. Operates on any
#   <root>/skills/<name>/SKILL.md + <root>/commands/*.md + <root>/roles/<slug>/agent.md
#   shaped tree, with an optional CATALOG/INDEX (see CATALOG DETECTION below).
#
# CHECKS:
#   (a) CATALOG parity — every skill/command/role NAME the catalog/index declares
#       EXISTS on disk as its expected artifact.
#   (b) REFERENCE resolution — every reference path inside skill/command files
#       resolves: relative `references/...`, `roles/<slug>/agent.md`, and
#       `~/.claude/...` deploy paths (resolved against --deploy root).
#   (c) NO dead symlinks anywhere under <root> (a symlink whose target is absent).
#   (d) NO orphaned reference bundle — a `references/` dir with no sibling SKILL.md
#       (a bundle nothing can consume == dead weight that reads as present).
#
# BUG-N convention: when a real defect is found/fixed in an audit, annotate the fix
# site with `# BUG-N (context): ...` so the negative test proving the fix has a stable
# referent. An audit that cannot prove it FAILs on bad input does not count (F-007).
#   BUG-22 (F-022, the core crack): a declared/referenced artifact that is absent on
#     disk (or in the deploy root) is a FAIL, not a WARN. "Referenced" is not
#     "present"; only a resolved path counts.
#   BUG-22b (portability): dead-symlink detection uses POSIX `[ -L ] && [ ! -e ]`,
#     NOT `find -L` quirks, so it is identical on BSD (macOS) and GNU. We never feed
#     `find` a `-L` that would hide broken links. We also do NOT use `realpath -e`
#     (absent on stock BSD) — resolution is done with plain `[ -e ]` tests.
#   BUG-22c (deploy mapping): `~/.claude/...` in a file is resolved against the
#     --deploy root (default $HOME/.claude), NOT literally against `~` of whoever
#     runs the audit's cwd — so the check means "is it DEPLOYED", which is the property.
#
# EXIT SEMANTICS (via lib/audit-helpers.sh): 0 PASS / 1 FAIL / 2 FATAL.
#   Any unresolved reference / declared-but-absent artifact / dead symlink /
#   orphan bundle -> FAIL (exit 1). Bad args / missing --lib root -> FATAL (exit 2).
#   Skips are fail-closed (F-008) unless AUDIT_ALLOW_SKIP=1.
#
# CATALOG DETECTION (optional, best-effort, dependency-free — no jq/python):
#   If <root>/catalog.txt (or $PARITY_CATALOG) exists, it is read as a line-oriented
#   manifest of `<kind> <name>` records (kind in skill|command|role; '#' comments and
#   blank lines ignored). Each declared record must resolve to its artifact on disk.
#   When no catalog file is present, the DISK itself is the catalog: every skill/
#   command/role found is checked for reference integrity (checks b,c,d still run).
#
# USAGE:
#   parity-audit.sh --lib <root> [--deploy <root, default $HOME/.claude>]
#   PARITY_CATALOG=/path/to/manifest parity-audit.sh --lib <root>

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/audit-helpers.sh
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

AUDIT_TAG="parity-audit"

# --- Argument parsing (FATAL on bad args) ----------------------------------
LIB=""
DEPLOY="${HOME}/.claude"

usage() {
  emit "usage: parity-audit.sh --lib <root> [--deploy <root, default \$HOME/.claude>]"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --lib)
      [ "$#" -ge 2 ] || { emit "FATAL: --lib requires an argument"; usage; exit 2; }
      LIB="$2"; shift 2 ;;
    --deploy)
      [ "$#" -ge 2 ] || { emit "FATAL: --deploy requires an argument"; usage; exit 2; }
      DEPLOY="$2"; shift 2 ;;
    -h|--help)
      usage; exit 2 ;;
    *)
      emit "FATAL: unknown argument: $1"; usage; exit 2 ;;
  esac
done

if [ -z "$LIB" ]; then
  emit "FATAL: --lib <root> is required"; usage; exit 2
fi
if [ ! -d "$LIB" ]; then
  emit "FATAL: --lib root is not a directory: $LIB"; exit 2
fi

# Normalize LIB to an absolute path WITHOUT relying on realpath (BSD lacks -e/-m).
LIB="$(cd "$LIB" && pwd)"

emit "auditing lib=${LIB} deploy=${DEPLOY}"

# --- Helpers ---------------------------------------------------------------

# resolve_exists PATH -> 0 if the path exists (file/dir, following symlinks).
resolve_exists() { [ -e "$1" ]; }

# fixture_filter: drop nested negative-test data (BUG-22e, F-024) — `tests/fixtures/`
# is broken ON PURPOSE to prove the audits go RED, so scanning a vendored toolkit's
# fixtures would false-FAIL. EXCEPTION: if the caller explicitly points --lib AT a
# fixtures tree (e.g. parity-audit's own negative test), scan it fully.
case "$LIB" in
  *tests/fixtures*) fixture_filter() { cat; } ;;
  *)                fixture_filter() { grep -v '/tests/fixtures/' || true; } ;;
esac

# --- (a) CATALOG parity -----------------------------------------------------
# A catalog record `<kind> <name>` must resolve to its on-disk artifact:
#   skill   -> <root>/skills/<name>/SKILL.md
#   command -> <root>/commands/<name>.md   (or <root>/commands/<name>/<name>.md)
#   role    -> <root>/roles/<name>/agent.md
CATALOG="${PARITY_CATALOG:-$LIB/catalog.txt}"
if [ -f "$CATALOG" ]; then
  emit "catalog: ${CATALOG}"
  while IFS= read -r rec || [ -n "$rec" ]; do
    # strip comments / whitespace
    rec="${rec%%#*}"
    # shellcheck disable=SC2086
    set -- $rec
    [ "$#" -ge 2 ] || continue
    kind="$1"; name="$2"
    case "$kind" in
      skill)
        art="$LIB/skills/$name/SKILL.md"
        resolve_exists "$art" || fail "catalog declares skill '$name' but artifact is absent on disk: $art (F-022)" ;;
      command)
        if ! resolve_exists "$LIB/commands/$name.md" && ! resolve_exists "$LIB/commands/$name/$name.md"; then
          fail "catalog declares command '$name' but no command artifact on disk under $LIB/commands/ (F-022)"
        fi ;;
      role)
        art="$LIB/roles/$name/agent.md"
        resolve_exists "$art" || fail "catalog declares role '$name' but artifact is absent on disk: $art (F-022)" ;;
      *)
        warn "catalog record with unknown kind '$kind' (name '$name') — skipping" ;;
    esac
  done < "$CATALOG"
else
  emit "no catalog file (PARITY_CATALOG / $LIB/catalog.txt) — disk is the catalog"
fi

# --- (b) REFERENCE resolution ----------------------------------------------
# For every skill SKILL.md and every command file, resolve in-file references.
# References are resolved against the FILE's own directory (relative ones) and
# against the --deploy root (~/.claude ones).
audit_file_refs() {
  file="$1"
  base="$(dirname "$file")"

  # references/<path>  — relative bundle references resolved against the file dir.
  # BUG-22g (substring immunity, F-007): only a STANDALONE `references/<path>` token is
  # a relative bundle ref. A `references/<path>` that is the tail of a longer path
  # (e.g. `~/.claude/skills_library/skills/rubric/references/x.md`) is NOT a relative
  # ref — it is a deploy/anchored path handled by the `~/.claude/...` resolver below.
  # Matching it here resolved it against THIS file's own references/ dir and false-FAILed
  # every anchored reference. So extract the MAXIMAL path token and keep only tokens that
  # begin with `references/` or `./references/` — both name THIS file's own bundle dir.
  # (BUG-22h: a leading `./` is the same relative ref; keeping only bare `references/`
  # over-suppressed it, so a dead `./references/x.md` slipped through the audit.)
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    # BUG-22 (F-022): referenced != present. Only a resolved path passes.
    resolve_exists "$base/$ref" \
      || fail "$file references '$ref' but it does not resolve to disk: $base/$ref (F-022)"
  done <<EOF
$(grep -oE '[A-Za-z0-9._~/-]*references/[A-Za-z0-9._/-]+' "$file" 2>/dev/null | grep -E '^(\./)?references/' | sort -u)
EOF

  # roles/<slug>/agent.md — role wiring resolved against the LIB root.
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    resolve_exists "$LIB/$ref" \
      || fail "$file references role '$ref' but it does not resolve to disk: $LIB/$ref (F-022)"
  done <<EOF
$(grep -oE 'roles/[A-Za-z0-9._-]+/agent\.md' "$file" 2>/dev/null | sort -u)
EOF

  # ~/.claude/<path> — deploy references resolved against the --deploy root.
  # BUG-22c: a deploy path is "is it DEPLOYED", resolved against $DEPLOY not literal ~.
  # Trailing-slash tokens denote a directory; bare tokens denote a file or dir.
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    # BUG-22d (portability): the '~' in the strip-pattern MUST be quoted, else bash
    # tilde-expands it to $HOME and the prefix never matches, silently leaving the
    # path unstripped and the deploy check false-FAILing (or false-PASSing).
    # BUG-22f (documentation immunity, F-007): a deploy path containing an ellipsis
    # placeholder ('...') is ILLUSTRATIVE prose — a command/skill documenting deploy
    # paths (e.g. deploy-and-verify.md's own examples), not a real reference. Resolving
    # it would make an artifact's own documentation fail the audit forever. Skip it.
    case "$ref" in *...*) continue ;; esac
    sub="${ref#'~/.claude/'}"
    sub="${sub%/}"
    [ -z "$sub" ] && continue
    # The ANCHOR: ~/.claude/skills_library is a symlink that points AT the library
    # root (--lib). roles/ and library-internal bundles have no native ~/.claude home,
    # so the canonical single-source way to reference them is via the anchor. A
    # reference under it therefore resolves against $LIB (where the anchor points),
    # NOT the deploy root — this is what makes the anchored deploy model auditable.
    case "$sub" in
      skills_library)
        resolve_exists "$LIB" \
          || fail "$file references the anchor '$ref' but the library root is absent: $LIB (F-022)"
        continue ;;
      skills_library/*)
        anchored="$LIB/${sub#skills_library/}"
        resolve_exists "$anchored" \
          || fail "$file references anchored path '$ref' but it is absent: $anchored (F-022)"
        continue ;;
    esac
    resolve_exists "$DEPLOY/$sub" \
      || fail "$file references deploy path '$ref' but it is not deployed: $DEPLOY/$sub (F-022)"
  done <<EOF
$(grep -oE '~/\.claude/[A-Za-z0-9._/-]+' "$file" 2>/dev/null | sort -u)
EOF
}

# Skills
if [ -d "$LIB/skills" ]; then
  while IFS= read -r skill_md; do
    [ -z "$skill_md" ] && continue
    audit_file_refs "$skill_md"
  done <<EOF
$(find "$LIB/skills" -type f -name 'SKILL.md' 2>/dev/null)
EOF
fi

# Commands (top-level *.md and nested <name>/<name>.md style)
if [ -d "$LIB/commands" ]; then
  while IFS= read -r cmd_md; do
    [ -z "$cmd_md" ] && continue
    audit_file_refs "$cmd_md"
  done <<EOF
$(find "$LIB/commands" -type f -name '*.md' 2>/dev/null)
EOF
fi

# --- (c) NO dead symlinks ---------------------------------------------------
# BUG-22b: POSIX dead-link test, identical on BSD+GNU. We do NOT use find -L.
# BUG-22e (fresh-start dogfood, F-024): EXCLUDE tests/fixtures/ — negative-test
#   data is broken ON PURPOSE (a dead symlink, an orphan bundle) to prove the
#   audits go RED. A project that vendors a toolkit must not false-FAIL on that
#   deliberate breakage; a project's OWN negative-test fixtures are exempt too.
while IFS= read -r link; do
  [ -z "$link" ] && continue
  # A symlink whose target does not exist (follow it: [ -e ] is false but [ -L ] true).
  if [ -L "$link" ] && [ ! -e "$link" ]; then
    tgt="$(readlink "$link" 2>/dev/null)"
    fail "dead symlink: $link -> ${tgt:-?} (target does not resolve) (F-022)"
  fi
done <<EOF
$(find "$LIB" -type l 2>/dev/null | fixture_filter)
EOF

# --- (d) NO orphaned reference bundle --------------------------------------
# A references/ dir with no sibling SKILL.md is a bundle nothing consumes.
# (BUG-22e: tests/fixtures/ excluded — see (c).)
while IFS= read -r refdir; do
  [ -z "$refdir" ] && continue
  parent="$(dirname "$refdir")"
  if [ ! -f "$parent/SKILL.md" ]; then
    fail "orphaned reference bundle: $refdir has no sibling SKILL.md ($parent/SKILL.md absent) (F-022)"
  fi
done <<EOF
$(find "$LIB" -type d -name 'references' 2>/dev/null | fixture_filter)
EOF

verdict
