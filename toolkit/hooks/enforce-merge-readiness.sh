#!/usr/bin/env bash
# toolkit/hooks/enforce-merge-readiness.sh — PreToolUse(Bash) guard: deny a
# `gh pr merge` unless the branch's work has passed a CLEAN /review-pr run bound
# to the exact commit being merged (ADR-0007, the no-merge-without-CLEAN-review
# gate — the 4th boundary gate after commit / PR-create).
#
# WHY (the autonomous-roll requirement): an autonomous build→review→merge loop
# stalls when a human must approve every merge. The rule the operator wants is
# "block a merge ONLY when /review-pr did not run CLEAN" — so authorization must
# be MECHANICAL, not a rubber-stampable marker (the ADR-0002 hazard). This hook
# reads the machine verdict /review-pr emits and gates on it. Paired with a
# harness settings rule that ALLOWS `gh pr merge`, this hook becomes the enforcer:
# the classifier stops blocking, and rigor blocks exactly when review is missing.
#
# WHAT IT CONSUMES: the review-verdict artifact /review-pr writes on completion —
#   ${CLAUDE_PROJECT_DIR}/.rigor/review-verdict.json
#   shaped {"result":"CLEAN","head_sha":"<reviewed HEAD sha>","ts":<epoch>}.
#   It does NOT re-run the review — it reads the recorded verdict.
#
# DENY (exit 2 in test mode / deny-object in hook mode) a `gh pr merge` UNLESS:
#   (a) the verdict artifact EXISTS, reads result == CLEAN, AND
#   (b) it is BOUND to HEAD — its head_sha EQUALS the current commit
#       (`git rev-parse HEAD`; the ENFORCE_MERGE_HEAD_SHA override is honored only
#       under TESTMODE, so a durable env var cannot forge the binding in production).
#       Identity, not a marker (ADR-0006 lineage): a CLEAN review of an OLDER
#       commit does NOT authorize merging commits that landed after it — a commit
#       pushed after review moves HEAD, the sha mismatches, and the merge is denied
#       until a fresh review runs. Network-free (mirrors enforce-pr-readiness): the
#       binding is the LOCAL branch tip, so this gates the on-branch autonomous
#       merge; merging a PR you are not checked out on fails closed (sha mismatch).
#   result == FINDINGS / absent / unreadable / unparseable / sha mismatch → RED.
#
# FAIL-CLOSED (F-008): "couldn't read a CLEAN verdict for THIS commit" never reads
# as "reviewed, allow." There is no assume-clean path.
#
# MATCHER: only `gh pr merge` is intercepted, transparent-exec wrappers stripped
# (bead 4jx), word-boundary discipline so `gh pr view` / `echo gh pr merge` /
# `gh pr merge-queue`-shaped tokens do NOT false-block.
#
# PORTABILITY: pure bash 3.2 + POSIX grep/sed/tr + git (git only for the HEAD read,
# guarded by `command -v`); jq optional with a dependency-free fallback.
#
# ── MODES ────────────────────────────────────────────────────────────────────
# HOOK MODE (default): read PreToolUse JSON on stdin; print a Claude Code deny
#   object + `exit 0` to DENY, or `exit 0` with no output to ALLOW.
# TEST MODE (ENFORCE_MERGE_READINESS_TESTMODE=1): verdict in the EXIT CODE for
#   test-lib (0 = ALLOW, 2 = DENY). The DENY reason prints to stderr in both modes.

set -uo pipefail

# Dep preflight (bead skills_library-kfi): under `pipefail` a missing grep/sed/tr
# makes every matcher pipeline return non-zero, which reads as "not our concern"
# → silent ALLOW. A gate whose matcher cannot run must fail CLOSED instead
# (F-008): exit 2 is a PreToolUse blocking error in hook mode and FATAL in test
# mode. `command -v` is a bash builtin, so the preflight itself needs none of the
# tools it checks.
for _dep in grep sed tr; do
  command -v "$_dep" >/dev/null 2>&1 && continue
  echo "enforce-merge-readiness: DENY — required tool '$_dep' not found on PATH; the matcher cannot run (fail-closed, F-008)" >&2
  exit 2
done

TESTMODE="${ENFORCE_MERGE_READINESS_TESTMODE:-0}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
VERDICT_FILE="${PROJECT_DIR}/.rigor/review-verdict.json"

# ── command extraction (jq optional, dependency-free fallback) ─────────────────
# Lineage: enforce-pr-readiness.sh / block-commit-main.sh.
extract_command() {
  local json="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -r '.tool_input.command // empty' <<EOF 2>/dev/null
$json
EOF
    return 0
  fi
  printf '%s' "$json" \
    | tr '\n' ' ' \
    | sed 's/\\"/__ESCQ__/g' \
    | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | sed 's/__ESCQ__/"/g; s/\\\\/\\/g; s/\\n/ /g; s/\\t/ /g'
}

# ── normalization ─────────────────────────────────────────────────────────────
normalize() {
  local norm
  norm=$(printf '%s' "$1" | tr '\n' ';' | tr -s '[:space:]' ' ')
  norm="${norm#" "}"; norm="${norm%" "}"
  printf '%s' "$norm"
}

# strip_transparent_wrappers (bead skills_library-4jx) — remove a leading
# TRANSPARENT-EXEC wrapper and its own options/args at every command position, so
# `command gh pr merge` / `env -u X gh pr merge` are seen as the merge they exec.
# Only transparent-exec words strip (echo/printf do not), preserving the
# `echo gh pr merge` must-NOT-block case. Byte-identical to the commit/PR gates.
strip_transparent_wrappers() {  # $1 = normalized command; $2 = value-flag class
                                # (default uCg); echoes wrappers removed
  local s="$1" prev cls="${2:-uCg}"
  while :; do
    prev="$s"
    s="$(printf '%s' "$s" | sed -E 's/(^|[;&|][[:space:]]*)(command|exec|nohup|builtin|time|env|sudo|doas|nice|ionice|setsid|stdbuf|unbuffer|caffeinate|timeout|xargs)([[:space:]]+(-['"$cls"'][[:space:]]+[^ ;&|]+|-[^ ;&|]*|[A-Za-z_][A-Za-z0-9_]*=[^ ;&|]*|[0-9][^ ;&|]*))*[[:space:]]+/\1/g')"
    [ "$s" = "$prev" ] && break
  done
  printf '%s' "$s"
}

# ── matcher ───────────────────────────────────────────────────────────────────
# is_pr_merge "<raw command>" — 0 if a `gh pr merge` invocation, else 1. Anchored
# at start / after a separator (so `echo gh pr merge` does NOT match), tolerates
# env-var / path prefixes on `gh`, requires the exact `pr merge` subcommand pair,
# and ends `merge` on a word boundary so `gh pr merge-queue`-style tokens do not
# false-match. `gh pr view` / `gh project merge` lack the `pr merge` adjacency.
is_pr_merge() {
  local norm folded re
  norm=$(normalize "$1")
  re='(^|[;&|] *)([A-Za-z_][A-Za-z0-9_]*=[^ ;&|]* +)*([^ ;&|]*/)?gh +pr +merge( |[;&|]|$)'
  # Pass 1 — exact (the pre-pif behavior, byte-preserved): -[uCg] consumes
  # `env -C dir` correctly; a lowercase `-c` stays generic (setsid's -c takes no
  # argument). Pass 2 — case-folded (bead skills_library-pif): the matcher grep
  # was already -i, but the STRIP's wrapper list was case-sensitive, so
  # `TIMEOUT 5 gh pr merge` evaded on a case-insensitive FS. Folding lowercases
  # `-C` too, so the folded pass widens the value-flag class to -[ucg].
  # OR-semantics make the fold purely ADDITIVE: it can only over-MATCH
  # (fail-closed friction), never lose a pass-1 catch.
  printf '%s' "$(strip_transparent_wrappers "$norm")" | grep -qiE "$re" && return 0
  folded="$(printf '%s' "$norm" | tr '[:upper:]' '[:lower:]')"
  printf '%s' "$(strip_transparent_wrappers "$folded" ucg)" | grep -qiE "$re"
}

# ── verdict read + SHA binding (fail-closed) ──────────────────────────────────
json_str_field() { # $1 = json ; $2 = field
  printf '%s' "$1" \
    | tr '\n' ' ' \
    | sed -n "s/.*\"$2\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p"
}

# head_sha — the current commit the merge would carry. The ENFORCE_MERGE_HEAD_SHA
# override is honored ONLY under TESTMODE, so the PRODUCTION path always reads real
# git and a durable env var (direnv, a settings hook `env` block, a leftover export)
# cannot forge the binding — the same hardening enforce-pr-readiness applies to its
# ENFORCE_PR_HEAD_PARENTS override (bug-hunt caught this gate had dropped the gate).
# Else git; else empty (→ cannot establish → fail-closed RED). Return 0 established
# / 2 cannot establish.
head_sha() {
  if [ "$TESTMODE" = "1" ] && [ -n "${ENFORCE_MERGE_HEAD_SHA:-}" ]; then
    printf '%s' "$ENFORCE_MERGE_HEAD_SHA"; return 0
  fi
  command -v git >/dev/null 2>&1 || return 2
  git -C "$PROJECT_DIR" rev-parse --verify HEAD 2>/dev/null || return 2
}

DENY_REASON=""

# verdict_is_clean_bound — 0 ONLY if the artifact exists, parses, reads
# result CLEAN, carries a head_sha, and that head_sha EQUALS the current commit.
# Every other case → 1 (RED), fail-closed.
verdict_is_clean_bound() {
  [ -f "$VERDICT_FILE" ] || { DENY_REASON="review-verdict artifact absent ($VERDICT_FILE) — run /review-pr on this branch first"; return 1; }
  local raw result vsha cur rs
  raw="$(cat "$VERDICT_FILE" 2>/dev/null)" || { DENY_REASON="review-verdict unreadable"; return 1; }
  [ -n "$raw" ] || { DENY_REASON="review-verdict empty"; return 1; }

  result="$(json_str_field "$raw" result)"
  [ "$result" = "CLEAN" ] || { DENY_REASON="review verdict is not CLEAN (got '${result:-<unparseable>}') — findings unresolved; re-run /review-pr"; return 1; }

  vsha="$(json_str_field "$raw" head_sha)"
  [ -n "$vsha" ] || { DENY_REASON="review-verdict head_sha missing/unparseable"; return 1; }

  cur="$(head_sha)"; rs=$?
  if [ "$rs" -ne 0 ] || [ -z "$cur" ]; then
    DENY_REASON="cannot establish current HEAD (no git/HEAD) — fail-closed"
    return 1
  fi
  if [ "$vsha" != "$cur" ]; then
    DENY_REASON="review verdict is for a DIFFERENT commit (reviewed=$vsha vs HEAD=$cur) — a commit landed after the review; re-run /review-pr before merging"
    return 1
  fi
  return 0
}

# ── main ──────────────────────────────────────────────────────────────────────
RAW=""
if [ "$#" -ge 1 ] && [ -n "${1:-}" ]; then
  COMMAND="$1"; RAW="$1"
else
  HOOK_INPUT="$(cat)"
  COMMAND="$(extract_command "$HOOK_INPUT")"
  RAW="$HOOK_INPUT"
fi

# Not a `gh pr merge` → not our concern → allow.
if [ -z "$COMMAND" ] || ! is_pr_merge "$COMMAND"; then
  exit 0
fi

if verdict_is_clean_bound; then
  exit 0
fi

# NOT ready → DENY. Reason to stderr in both modes (fail-closed).
echo "enforce-merge-readiness: DENY gh pr merge — $DENY_REASON" >&2

if [ "$TESTMODE" = "1" ]; then
  exit 2
fi

# HOOK MODE: emit the Claude Code deny object.
printf '%s\n' "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"ADR-0007: no merge without a CLEAN /review-pr bound to this commit. ${DENY_REASON}. Run /review-pr on this branch; it writes .rigor/review-verdict.json on a CLEAN pass, and the merge is authorized mechanically once that verdict is bound to HEAD.\"}}"
exit 0
