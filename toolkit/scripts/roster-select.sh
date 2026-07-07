#!/usr/bin/env bash
# toolkit/scripts/roster-select.sh — classify a change set into a review roster (bead gw5).
#
# THE CANONICAL OWNER of the roster-selection rule (re-designated from the consumer-side
# specs/recipes/README.md at rigor 1.18.0 — run-pipeline invariant #7 points here now).
# Before this script the rules lived as prose applied by orchestrator judgment, and the
# failure mode was silent under-review: a tired orchestrator classifies a substantive
# change as docs and nobody records that a choice was made. This script makes the choice
# executable, recorded, and fail-closed.
#
# USAGE
#   roster-select.sh --base <ref> --head <ref>     # classify a committed range
#   roster-select.sh --files <path> [<path>...]    # classify an explicit file list
#   optional: --override scaffold --justification "<text>"
#
# OUTPUT (stdout, ONE grep-anchored line; the caller pastes it into the review header):
#   roster-select: roster=<full-6|docs-3|code-subset-3|recipe> design=<yes|no> \
#     ruleset=<version> reason=<rule-id>[ override-justification="<text>"]
#
# EXIT CONTRACT
#   0  classified — the stdout verdict is authoritative, INCLUDING the rule-7 fail-closed
#      full-6 on ambiguous-but-readable input (an empty diff is a verdict, not an error).
#   2  FATAL — the change set was genuinely unreadable (bad ref, git error, no input).
#      stdout still carries roster=full-6 as a safe default label, and the contract BINDS
#      the caller: on exit 2, widen to full-6 or halt — NEVER fall through to a narrower
#      default (F-008: a roster that could not be computed must not shrink the review).
#   1  unused — roster-select has no ran-clean-negative state; reserved.
#
# RULES (first match wins; reason= names the rule that decided)
#   rule-1  sensitive path class (auth/crypto/migration/schema/CI-exec — the shipped
#           pattern list below + an optional ADDITIVE project overlay at
#           ${CLAUDE_PROJECT_DIR:-.}/.rigor/roster-patterns.local) → full-6. NOT
#           overridable: --override on a rule-1 hit is refused on stderr by name.
#   rule-2  any code/test file changed (changed = added, removed, renamed, or edited —
#           a pure deletion of a guard is as risky as an addition), excluding
#           scaffold-classed files → full-6. NOT overridable (refused by name).
#   rule-3  recipe artifact (specs/recipes/*.md) → recipe (the adversarial-review skill,
#           NOT /review-pr — a recipe must never classify docs-3).
#   rule-4  code-extension files that are ALL scaffold-classed (lockfiles/generated):
#           with --override scaffold + --justification → code-subset-3 (the justification
#           is echoed into the output line — the audit trail is load-bearing); WITHOUT
#           the override → full-6 (there is no silent reduction path).
#   rule-5  zero code/test files → docs-3. Ruled boundaries: a .md containing code
#           fences is still docs-3 (path rules cannot see fence content — accepted);
#           binary/image files under a UI/design path also set design=yes.
#   rule-6  (dimension, additive) any UI-class file — the class is owned by
#           toolkit/lib/ui-class.sh (RIGOR_UI_RE) and sourced fail-closed → design=yes.
#   rule-7  an EMPTY change set (readable but nothing changed) → full-6, exit 0 — an
#           empty diff is a verdict, not an error. Non-code files that match no class
#           (config/data/text) are rule-5 docs-3 by the reviewed plan's ruling.
set -uo pipefail

SELF_DIR="$(CDPATH= cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The ruleset version names the RULES, not the toolkit release; bump it when a rule
# changes so vendored consumers can detect prose-vs-script skew from the output line.
RULESET="1.18.0"

emit() { # emit <roster> <reason> [justification]
  local line="roster-select: roster=$1 design=$DESIGN ruleset=$RULESET reason=$2"
  [ -n "${3:-}" ] && line="$line override-justification=\"$3\""
  printf '%s\n' "$line"
}

fatal() { # fatal <why> — safe default label on stdout, bind the caller via exit 2
  echo "roster-select: FATAL — $1. Widen to full-6 or halt; never narrow (F-008)." >&2
  DESIGN="${DESIGN:-no}"
  emit "full-6" "fatal-unreadable"
  exit 2
}

# --- the UI class: single-sourced, fail-closed (same contract as design-gate) ---------
UI_CLASS_LIB="$SELF_DIR/../lib/ui-class.sh"
[ -f "$UI_CLASS_LIB" ] || fatal "toolkit/lib/ui-class.sh missing; the UI class is undefined"
# shellcheck source=../lib/ui-class.sh
. "$UI_CLASS_LIB"
[ -n "${RIGOR_UI_RE:-}" ] || fatal "ui-class.sh loaded but RIGOR_UI_RE is undefined"

# --- the classes ----------------------------------------------------------------------
CODE_RE='\.(sh|bash|zsh|py|js|mjs|cjs|ts|tsx|jsx|sql|rb|go|rs|java|c|h|cc|cxx|cs|cpp|hpp|swift|kt|php|pl|lua|scala|ex|exs|r|jl|dart|m|mm|ipynb|vue|svelte|astro)$'
SCAFFOLD_RE='(^|/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|Gemfile\.lock|poetry\.lock|Cargo\.lock|composer\.lock)$|\.generated\.|(^|/)(dist|build|node_modules)/'
RECIPE_RE='(^|/)specs/recipes/[^/]+\.md$'
DESIGN_PATH_RE='(^|/)(design|designs|ui)/.*\.(png|jpe?g|gif|svg|webp)$'

# Shipped sensitive-path classes (rule-1). One ERE per element.
SENSITIVE_RES=(
  '(^|/)(auth|authn|authz|oauth|sso|session|login|signing|signature)[^/]*(/|$)'
  '(crypt|cipher|secret|credential|token|keychain|private[_-]?key)'
  '(^|/)(migrations?|schema)(/|\.)'
  '(^|/)\.github/workflows/'
  '(^|/)(Dockerfile|Makefile)([^/]*)$'
  '(^|/)hooks?/'
  '(^|/)(bin|scripts?)/[^/.]+$'
  '\.(pem|key|crt|p12|pfx)$'
  '\.env(\.[A-Za-z0-9_-]+)?$'
)
# ADDITIVE project overlay — can only ADD sensitive patterns, never remove (fail-safe).
OVERLAY="${CLAUDE_PROJECT_DIR:-.}/.rigor/roster-patterns.local"
if [ -f "$OVERLAY" ]; then
  while IFS= read -r pat; do
    case "$pat" in ''|'#'*) continue;; esac
    # Validate at load: an invalid ERE would make grep error inside match_any, which
    # reads as a NON-match — the overlay's added sensitivity would silently not apply
    # (fail-open). A pattern that cannot be compiled is FATAL, not ignored.
    printf 'x\n' | grep -qE "$pat" 2>/dev/null
    [ $? -le 1 ] || fatal "overlay pattern '$pat' in $OVERLAY is not a valid ERE"
    SENSITIVE_RES+=("$pat")
  done < "$OVERLAY"
fi

# --- parse args -----------------------------------------------------------------------
BASE="" HEAD="" OVERRIDE="" JUSTIFICATION="" DESIGN="no" FILES_MODE=""
declare -a FILES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --base|--head|--override|--justification)
      # a value flag with no value must FATAL — an unguarded `shift 2` fails without
      # set -e and leaves $1 in place, spinning this loop forever (executed hang)
      [ $# -ge 2 ] || fatal "$1 requires a value" ;;
  esac
  case "$1" in
    --base)  BASE="$2"; shift 2 ;;
    --head)  HEAD="$2"; shift 2 ;;
    --files) FILES_MODE=1; shift; while [ $# -gt 0 ] && [ "${1#--}" = "$1" ]; do FILES+=("$1"); shift; done ;;
    --override) OVERRIDE="$2"; shift 2 ;;
    --justification) JUSTIFICATION="$2"; shift 2 ;;
    *) fatal "unknown argument '$1'" ;;
  esac
done

if [ -n "$OVERRIDE" ]; then
  [ "$OVERRIDE" = "scaffold" ] || fatal "unknown override '$OVERRIDE' (only 'scaffold' exists)"
  [ -n "$JUSTIFICATION" ] || fatal "--override scaffold requires --justification (the audit trail is load-bearing)"
  # The output contract is ONE grep-anchored line; a justification carrying a newline or
  # a double quote can forge a second, narrower verdict line or break the field framing
  # (executed in review as a docs-3 forgery). Reject rather than sanitize — the audit
  # trail must be what the caller typed, or nothing.
  case "$JUSTIFICATION" in
    *$'\n'*|*$'\r'*|*'"'*) fatal "--justification must not contain newlines or double quotes (one-line output invariant)" ;;
  esac
fi

# --- collect the change set -----------------------------------------------------------
if [ -z "$FILES_MODE" ] && [ ${#FILES[@]} -eq 0 ]; then
  [ -n "$BASE" ] && [ -n "$HEAD" ] || fatal "no input (need --base/--head or --files)"
  git rev-parse --verify --quiet "$BASE^{commit}" >/dev/null || fatal "base ref '$BASE' unreadable"
  git rev-parse --verify --quiet "$HEAD^{commit}" >/dev/null || fatal "head ref '$HEAD' unreadable"
  # --no-renames: rename detection collapses a rename to its DESTINATION, so a code
  # file renamed to a docs path would vanish from the change set (executed: guard.sh →
  # guard.md classified docs-3). Both sides of a rename are part of the change set,
  # exactly like a deletion (rule-2's deletion clause).
  DIFF_OUT="$(git diff --name-only --no-renames "$BASE...$HEAD" 2>/dev/null)" \
    || fatal "git diff failed for $BASE...$HEAD"
  while IFS= read -r f; do [ -n "$f" ] && FILES+=("$f"); done <<< "$DIFF_OUT"
fi

# Classification matching is CASE-INSENSITIVE (grep -i): App.TS is code on any
# filesystem, and macOS/Windows treat it as identical to app.ts — an uppercase
# extension must not reach a reduced roster (executed bypass in review). Rule-6 alone
# stays case-sensitive to match design-gate's UI_RE semantics exactly (the two tools
# must never disagree on the design dimension; widening both is bead 3ut).
match_any() { # match_any <path> <re...>
  local p="$1"; shift
  local re
  for re in "$@"; do printf '%s\n' "$p" | grep -qiE "$re" && return 0; done
  return 1
}

# --- classify -------------------------------------------------------------------------
HIT_SENSITIVE="" HIT_CODE="" HIT_SCAFFOLD="" HIT_RECIPE=""
for f in ${FILES[@]+"${FILES[@]}"}; do
  printf '%s\n' "$f" | grep -qE "$RIGOR_UI_RE" && DESIGN="yes"
  printf '%s\n' "$f" | grep -qiE "$DESIGN_PATH_RE" && DESIGN="yes"
  if match_any "$f" "${SENSITIVE_RES[@]}"; then HIT_SENSITIVE="$f"
  elif printf '%s\n' "$f" | grep -qiE "$RECIPE_RE"; then HIT_RECIPE="$f"
  elif printf '%s\n' "$f" | grep -qiE "$SCAFFOLD_RE"; then HIT_SCAFFOLD="$f"
  elif printf '%s\n' "$f" | grep -qiE "$CODE_RE"; then HIT_CODE="$f"
  fi
done

refuse_override() { # refuse_override <rule> <offending-path>
  [ -n "$OVERRIDE" ] && echo "roster-select: override REFUSED — $1 hit ('$2') is not reducible" >&2
}

# Precedence here differs from the loop's per-file bucketing on purpose: the loop
# assigns each file its single class; THIS chain picks the roster, and any code
# anywhere outranks recipe/scaffold (a recipe+code diff widens to full-6).
if [ ${#FILES[@]} -eq 0 ]; then
  emit "full-6" "rule-7-empty"                                   # empty is a verdict
elif [ -n "$HIT_SENSITIVE" ]; then
  refuse_override "rule-1" "$HIT_SENSITIVE"
  emit "full-6" "rule-1"
elif [ -n "$HIT_CODE" ]; then
  refuse_override "rule-2" "$HIT_CODE"
  emit "full-6" "rule-2"
elif [ -n "$HIT_RECIPE" ]; then
  emit "recipe" "rule-3"
elif [ -n "$HIT_SCAFFOLD" ]; then
  if [ "$OVERRIDE" = "scaffold" ]; then
    emit "code-subset-3" "rule-4" "$JUSTIFICATION"
  else
    emit "full-6" "rule-4-default"                               # no silent reduction
  fi
else
  emit "docs-3" "rule-5"
fi
exit 0
