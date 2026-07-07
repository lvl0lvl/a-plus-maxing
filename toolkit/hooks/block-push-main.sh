#!/usr/bin/env bash
# toolkit/hooks/block-push-main.sh — PreToolUse Bash-tool guard: deny direct
# pushes to a protected trunk branch (main/master by default).
#
# ENFORCES (CDM): INV-BRANCH-NOT-MAIN, push side. Companion hook
# hooks/block-commit-main.sh enforces the commit side of the same invariant.
# Source finding lineage:
#   - PF-S2-06 (a-plus-maxing): five S2 commits landed on main locally before the
#     gap was noticed; push WAS correctly blocked but commit was not. The push
#     guard is the second-line defense for the in-command `cd … && git commit`
#     shape that the commit guard cannot see (it checks the STARTING cwd's repo).
#   - F-008 (rigor toolkit): "couldn't verify" != "verified clean". A hook that
#     cannot determine the command FAILs CLOSED (denies) rather than silently
#     allowing — see TEST MODE exit semantics and the jq-absent fallback below.
#
# SOURCE LINEAGE:
#   - skill_consolidator/.claude/hooks/block-push-main.sh (the push regex + the
#     normalize-then-match shape).
#   - a-plus-maxing/.claude/hooks/block-commit-main.sh (the deny-JSON contract,
#     the `set -uo pipefail` posture, the PROJECT_ROOT/env override idiom).
#
# BUG-1 (carried forward): the original push regex `git\s+push\s+\S+\s+(main|master)\b`
#   used `\S+` for the remote, so it MISSED `git push` with no explicit remote
#   (`git push` while the upstream tracks main) and `git push -u origin main`
#   shapes where flags sit between `push` and the remote. Generalized below to
#   tolerate optional flags and an optional explicit remote, and to match a
#   protected branch token (with optional `refs/heads/`, `HEAD:`, or `+` lease
#   prefix and an optional `:dst` refspec) anywhere in the push argument list.
#
# BUG-2 (carried forward / F-008): both sources read the command via `jq` with no
#   guard for jq being absent — under a missing jq the hook would emit nothing and
#   `exit 0` (silent ALLOW). Here a missing jq falls back to a dependency-free
#   parser; if the command genuinely cannot be extracted the hook FAILs CLOSED.
#
# PORTABILITY: pure bash 3.2 + POSIX grep/tr/sed (no GNU-isms, no `grep -P`,
#   no jq dependency). Tested on BSD (macOS) and GNU userlands.
#
# ── MODES ────────────────────────────────────────────────────────────────────
# HOOK MODE (default): read PreToolUse JSON on stdin, print a Claude Code deny
#   object + `exit 0` to DENY, or `exit 0` with no output to ALLOW. (Claude Code
#   reads the JSON, not the exit code, in hook mode.)
#
# TEST MODE (BLOCK_PUSH_MAIN_TESTMODE=1): a thin shim for the negative test and
#   for use as a rigor audit. Same detection, but the verdict is carried in the
#   EXIT CODE so test-lib's expect_exit / assert_red_when_guard_removed can read
#   it: 0 = ALLOW (clean), 1 = BLOCK (violation found). A command that cannot be
#   extracted at all is exit 2 (FATAL — fail-closed, F-008). The command may be
#   supplied as $1 (raw string) instead of JSON on stdin.
#
# Note: this hook is a stdin/regex guard and does NOT source lib/audit-helpers.sh
# — it is a deny-gate, not a filesystem audit (it has no $violations sweep to
# report). Its companion negative test DOES use lib/test-lib.sh, discharging the
# F-007 obligation that the guard prove it goes RED on bad input.

set -uo pipefail

# Dep preflight (bead skills_library-kfi): under `pipefail` a missing grep/sed/tr
# makes every matcher pipeline return non-zero, which reads as "not our concern"
# → silent ALLOW. A gate whose matcher cannot run must fail CLOSED instead
# (F-008): exit 2 is a PreToolUse blocking error in hook mode and FATAL in test
# mode. `command -v` is a bash builtin, so the preflight itself needs none of the
# tools it checks.
for _dep in grep sed tr; do
  command -v "$_dep" >/dev/null 2>&1 && continue
  echo "block-push-main: DENY — required tool '$_dep' not found on PATH; the matcher cannot run (fail-closed, F-008)" >&2
  exit 2
done

# Protected branches — space-separated, overridable. Defaults cover the two
# conventional trunk names.
PROTECTED_BRANCHES="${PROTECTED_BRANCHES:-main master}"

TESTMODE="${BLOCK_PUSH_MAIN_TESTMODE:-0}"

# ── command extraction ────────────────────────────────────────────────────────
# Prefer jq when present; otherwise a dependency-free fallback that pulls
# .tool_input.command out of the PreToolUse JSON. Returns the raw command on
# stdout; empty if absent.
extract_command() {
  local json="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -r '.tool_input.command // empty' <<EOF 2>/dev/null
$json
EOF
    return 0
  fi
  # Fallback: pull the "command":"…" value out of tool_input without jq. BSD
  # basic-sed has no `\|` alternation, so we cannot match the escaped-quote class
  # inline; instead swap escaped quotes (\") to a sentinel, grab the [^"] run, then
  # restore. Collapse newlines first so pretty-printed JSON still matches.
  printf '%s' "$json" \
    | tr '\n' ' ' \
    | sed 's/\\"/__ESCQ__/g' \
    | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | sed 's/__ESCQ__/"/g; s/\\\\/\\/g; s/\\n/ /g; s/\\t/ /g'
}

# ── normalization ─────────────────────────────────────────────────────────────
# Map newlines to ';' so a push on a later line is seen, squeeze whitespace, and
# strip the leading/trailing space so a leading-whitespace command is not missed.
normalize() {
  local norm
  norm=$(printf '%s' "$1" | tr '\n' ';' | tr -s '[:space:]' ' ')
  norm="${norm#" "}"; norm="${norm%" "}"
  printf '%s' "$norm"
}

# ── matcher ───────────────────────────────────────────────────────────────────
# is_push_to_protected "<raw command>" — return 0 if the command is a `git push`
# targeting one of $PROTECTED_BRANCHES, else 1.
#
# BUG-1 fix: the branch token is matched ANYWHERE in the push argument list, with
# optional flags and an optional explicit remote between `push` and the branch,
# and an optional `+` (lease prefix), `refs/heads/`, or `HEAD:` adornment and an
# optional `:dst` refspec around the branch name. Word-boundary on both sides so
# `maintenance` / `mastermind` do not false-match.
is_push_to_protected() {
  local norm br re
  norm=$(normalize "$1")
  for br in $PROTECTED_BRANCHES; do
    # git … push … [+][refs/heads/|HEAD:]<br>[:dst]   (br on a word boundary)
    re="git[[:space:]]+push([[:space:]]+[^;&|]*)?[[:space:]](\+)?(refs/heads/)?(HEAD:)?${br}([[:space:]]|:|;|\&|\||$)"
    if printf '%s' "$norm" | grep -qiE "$re"; then
      return 0
    fi
  done
  return 1
}

# ── main ──────────────────────────────────────────────────────────────────────
# Command source: $1 (test mode convenience) else stdin JSON.
RAW=""
if [ "$#" -ge 1 ] && [ -n "${1:-}" ]; then
  RAW="$1"
  COMMAND="$RAW"
else
  HOOK_INPUT="$(cat)"
  COMMAND="$(extract_command "$HOOK_INPUT")"
  RAW="$HOOK_INPUT"
fi

if [ "$TESTMODE" = "1" ]; then
  # Fail-closed (F-008): a non-empty input we could not extract a command from is
  # a "couldn't verify" — exit 2 (FATAL), never a silent allow. An empty input is
  # legitimately not our concern (allow).
  if [ -z "$COMMAND" ]; then
    if [ -n "$RAW" ]; then
      echo "block-push-main: could not extract a command from non-empty input (fail-closed, F-008)" >&2
      exit 2
    fi
    exit 0
  fi
  if is_push_to_protected "$COMMAND"; then
    echo "block-push-main: BLOCK — push to protected branch detected" >&2
    exit 1
  fi
  exit 0
fi

# HOOK MODE.
[ -z "$COMMAND" ] && exit 0   # nothing to inspect → not our concern → allow

if is_push_to_protected "$COMMAND"; then
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"INV-BRANCH-NOT-MAIN: direct push to a protected branch (main/master) blocked. Use a short-lived feature/* or fix/* branch and open a PR. PF-S2-06 recurrence guard."}}'
  exit 0
fi

exit 0
