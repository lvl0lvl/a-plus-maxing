#!/usr/bin/env bash
# version-bump-audit.sh — the VERSION forward guard (bead skills_library-bd1).
#
# ENFORCES (Discipline 11 §"The framework + toolkit are versioned; projects pull"):
#   "The version never moves silently" has a converse the toolkit never checked —
#   the TOOLKIT must never move silently either. Toolkit content that lands
#   without a VERSION bump breaks the pull contract: a consuming project diffing
#   its pinned rigor_version against VERSION sees "no delta" and never pulls the
#   changed scripts. Field evidence: #97/#99/#100 landed toolkit scripts + an
#   export format with NO bump; the omissions were only caught (and rolled up)
#   by hand at 1.6.0. This audit catches the class mechanically.
#
# DETECTION CONTRACT — three checks over git history + the working tree:
#   CHECK 1 (committed drift): find the last commit that touched the VERSION
#     file; any WATCHED path changed in commits AFTER it → FAIL per file. The
#     bump commit itself may carry toolkit changes (that is the normal shape —
#     the diff starts from the bump commit, excluding its own changes).
#   CHECK 2 (working-tree drift): a WATCHED path is dirty (staged or unstaged,
#     vs HEAD) while the VERSION file is NOT dirty → FAIL per file. Catches the
#     forward case before it is ever committed.
#   Untracked files under the watched paths count as drift in CHECK 2 (a new
#     script is exactly the #97 class).
#   CHECK 3 (changelog completeness, bead skills_library-azt): D11 rule 1's other
#     half — "bump VERSION + add the CHANGELOG.md row together". VERSION line 1
#     must have a matching '## <version>' heading in the changelog; a missing row
#     means update-rigor's delta for that release is EMPTY (the 1.12.0 field
#     case: VERSION bumped, no row, this audit still passed). Skipped only while
#     VERSION itself is dirty (bump in progress — mirrors CHECK 2's model); the
#     committed state is always enforced.
#
# CADENCE: per-harvest / pre-release (Discipline 11), alongside parity-audit —
#   NOT in the per-close DEFAULT_ROSTER: mid-wave sessions legitimately touch the
#   toolkit across several commits before the wave's single bump lands, and a
#   per-close FAIL would train AUDIT_ALLOW_SKIP reflexes (the giq.1.3 drift).
#   Run it before tagging/announcing a version and at every harvest.
#
# CONFIG (env):
#   RIGOR_VERSION_FILE  — the version file (default: <rigor-root>/VERSION, where
#                         rigor-root is the parent of this script's toolkit/).
#   RIGOR_BUMP_WATCH    — colon-separated repo paths that require a bump when
#                         changed (default: the toolkit/ dir itself).
#   RIGOR_CHANGELOG_FILE — the changelog CHECK 3 reads (default: CHANGELOG.md
#                         next to the version file).
#
# EXIT SEMANTICS (lib/audit-helpers.sh): 0 PASS / 1 FAIL / 2 FATAL.
#   No git / VERSION untracked / not in a work tree → FATAL (a guard that cannot
#   read its history does not pass — F-008).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_TAG="version-bump-audit"
source "$SCRIPT_DIR/../lib/audit-helpers.sh"

RIGOR_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VERSION_FILE="${RIGOR_VERSION_FILE:-$RIGOR_ROOT/VERSION}"
WATCH="${RIGOR_BUMP_WATCH:-$SCRIPT_DIR/..}"

command -v git >/dev/null 2>&1 || { emit "FATAL: git not available"; exit 2; }
[ -f "$VERSION_FILE" ] || { emit "FATAL: version file absent ($VERSION_FILE)"; exit 2; }

# Everything below runs relative to the repo that owns the VERSION file.
VDIR="$(cd "$(dirname "$VERSION_FILE")" && pwd)"
git -C "$VDIR" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || { emit "FATAL: $VDIR is not inside a git work tree"; exit 2; }
REPO_ROOT="$(git -C "$VDIR" rev-parse --show-toplevel)"

# Repo-relative spelling of a path (git pathspecs want these). pwd -P so the
# comparison against git's PHYSICAL --show-toplevel holds under a symlinked
# tempdir (macOS /var/folders → /private/var).
rel_of() { # $1 = path → repo-relative on stdout, or empty if outside the repo
  local abs
  abs="$(cd "$(dirname "$1")" 2>/dev/null && pwd -P)/$(basename "$1")" || return 1
  case "$abs" in
    "$REPO_ROOT"/*) printf '%s' "${abs#"$REPO_ROOT"/}" ;;
    "$REPO_ROOT")   printf '.' ;;
    *) return 1 ;;
  esac
}

VERSION_REL="$(rel_of "$VERSION_FILE")" \
  || { emit "FATAL: version file is outside the repo ($VERSION_FILE)"; exit 2; }

# VERSION must itself be tracked — an untracked version file has no bump history.
git -C "$REPO_ROOT" ls-files --error-unmatch "$VERSION_REL" >/dev/null 2>&1 \
  || { emit "FATAL: version file is not tracked by git ($VERSION_REL)"; exit 2; }

LAST_BUMP="$(git -C "$REPO_ROOT" log -1 --format=%H -- "$VERSION_REL")"
[ -n "$LAST_BUMP" ] || { emit "FATAL: no commit touches the version file ($VERSION_REL)"; exit 2; }
emit "last VERSION commit: $(git -C "$REPO_ROOT" log -1 --format='%h %s' -- "$VERSION_REL")"

# Split the colon list ONCE into an array (review E5: the earlier in-loop IFS
# juggling required every continue to re-arm IFS=':' — a missed re-arm in a
# future edit would silently break splitting for later entries). read -ra also
# performs no pathname expansion, so a glob metachar in a watch path cannot
# widen or narrow the watch (review E3).
IFS=':' read -r -a WATCH_ENTRIES <<< "$WATCH"

EVALUATED=0
for w in "${WATCH_ENTRIES[@]}"; do
  [ -n "$w" ] || continue
  WREL="$(rel_of "$w")" || { skipped "watched path outside the repo: $w"; continue; }
  [ -e "$w" ] || { skipped "watched path absent: $w"; continue; }

  # git must actually SEE the path (review E2): on a case-insensitive FS a
  # wrong-case watch entry exists on disk but matches no git pathspec, so every
  # check below would run over nothing and read clean — a silent fail-open.
  # Tracked or untracked visibility counts; a path git cannot see is a skipped
  # check, never a pass (F-008).
  if [ -z "$(git -C "$REPO_ROOT" ls-files -- "$WREL")" ] \
     && [ -z "$(git -C "$REPO_ROOT" ls-files --others --exclude-standard -- "$WREL")" ]; then
    skipped "watched path invisible to git (case mismatch or empty dir): $w"
    continue
  fi
  EVALUATED=$((EVALUATED + 1))

  # CHECK 1 — committed drift since the last bump. Net diff: a file touched and
  # fully reverted between the bump and HEAD does NOT fail (the pull contract
  # cares about content delta, not churn). Heredoc, not a pipe — the while-loop
  # must run in the PARENT shell so fail() mutates the violations counter
  # (a `git | while` subshell would discard it).
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    fail "committed since the last VERSION bump without a bump: $f (landed after $(git -C "$REPO_ROOT" log -1 --format=%h -- "$VERSION_REL"))"
  done <<EOF
$(git -C "$REPO_ROOT" diff --name-only "$LAST_BUMP"..HEAD -- "$WREL")
EOF

  # CHECK 2 — working-tree drift while VERSION is clean. (Same heredoc-not-pipe
  # reasoning as CHECK 1.)
  VERSION_DIRTY=0
  if ! git -C "$REPO_ROOT" diff --quiet HEAD -- "$VERSION_REL" 2>/dev/null; then
    VERSION_DIRTY=1
  fi
  if [ "$VERSION_DIRTY" -eq 0 ]; then
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      fail "working-tree change without a VERSION change: $f"
    done <<EOF
$(git -C "$REPO_ROOT" diff --name-only HEAD -- "$WREL"; \
  git -C "$REPO_ROOT" ls-files --others --exclude-standard -- "$WREL")
EOF
  else
    emit "working tree: VERSION is dirty alongside any watched changes (bump in progress) — CHECK 2 satisfied"
  fi
done

# CHECK 3 — CHANGELOG completeness (bead skills_library-azt). Independent of the
# watch list: it compares VERSION line 1 against the changelog headings. Enforced
# only when VERSION is CLEAN vs HEAD (a dirty VERSION is a bump in progress whose
# row may legitimately still be being written — CHECK 2's model); the committed
# state, where the 1.12.0 omission lived, is always checked. The trailing
# boundary char keeps '## 1.1' from satisfying a 1.1.x VERSION and vice versa.
CHANGELOG_FILE="${RIGOR_CHANGELOG_FILE:-$(dirname "$VERSION_FILE")/CHANGELOG.md}"
if git -C "$REPO_ROOT" diff --quiet HEAD -- "$VERSION_REL" 2>/dev/null; then
  CUR_VERSION="$(sed -n '1p' "$VERSION_FILE" | tr -d '[:space:]')"
  if [ -z "$CUR_VERSION" ]; then
    fail "VERSION line 1 is empty — no version to check against the changelog ($VERSION_FILE)"
  elif [ ! -f "$CHANGELOG_FILE" ]; then
    fail "VERSION reads $CUR_VERSION but the changelog is absent ($CHANGELOG_FILE) — the version moved without its row (D11 rule 1)"
  else
    # Escape the ERE metachars a semver can carry ('.' always, '+' build meta).
    # BSD sed rejects a backslash inside a bracket expression, so the class is
    # kept to these two; any exotic char in VERSION simply fails the match —
    # the fail-CLOSED direction (a FAIL naming the heading, never a pass).
    VER_RE="$(printf '%s' "$CUR_VERSION" | sed 's/[.+]/\\&/g')"
    # Trailing boundary is WHITESPACE-or-EOL, not "any non-[0-9.]" (review BUG-2):
    # the latter let a PRERELEASE heading `## 1.2.0-rc.1` satisfy a FINAL VERSION
    # `1.2.0` (the '-' matched [^0-9.]) — a fail-OPEN of the exact "version moved
    # without its row" class this check exists to catch. A real heading always has
    # a space (`## 1.13.0 (2026-07-04) — …`) or ends the line after the version,
    # so `[[:space:]]|$` admits every legitimate row while a prerelease suffix
    # (which continues with a non-space char) no longer counts.
    grep -qE "^##[[:space:]]+${VER_RE}([[:space:]]|$)" "$CHANGELOG_FILE" \
      || fail "VERSION reads $CUR_VERSION but $CHANGELOG_FILE has no '## $CUR_VERSION' heading — the version moved without its changelog row (D11 rule 1); update-rigor's delta for this release is EMPTY"
  fi
else
  emit "VERSION is dirty (bump in progress) — CHECK 3 deferred to the committed state"
fi

# A watch list that evaluated ZERO paths ran zero checks — that is not a pass
# (review E1: a colon-only or all-empty RIGOR_BUMP_WATCH previously PASSed
# vacuously over real drift). Fail-closed via skipped().
[ "$EVALUATED" -gt 0 ] || skipped "no valid watched paths were evaluated (RIGOR_BUMP_WATCH='$WATCH')"

verdict
