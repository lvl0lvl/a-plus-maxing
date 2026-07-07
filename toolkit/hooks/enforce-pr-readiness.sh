#!/usr/bin/env bash
# toolkit/hooks/enforce-pr-readiness.sh — PreToolUse Bash-tool guard: deny a
# `gh pr create` unless the work is ready (ADR-0002, the no-premature-PR gate).
#
# ENFORCES (CDM): CDM-1-21 "no PR until deliverable complete + gates passed +
# authorized", the F-005 residual. This is the third member of the boundary-gate
# family (after block-commit-main / block-push-main) and reuses their idiom:
# extract the command from the PreToolUse JSON, match precisely, deny via exit 2.
#
# WHAT IT CONSUMES (ADR-0001 interface, SHA-bound per ADR-0006): the persisted
# gate-verdict artifact
#   ${CLAUDE_PROJECT_DIR}/.rigor/commit-gate-verdict.json
#   shaped {"roster_result":"GREEN","ts":<epoch>,"certified_parent":"<sha(s)>"}.
# It does NOT re-run the gate roster — it reads ADR-0001's recorded verdict.
#
# DENY (exit 2) a `gh pr create` UNLESS BOTH:
#   (a) the verdict artifact EXISTS, reads roster_result == GREEN, and is BOUND to
#       HEAD — its certified_parent (the SHA set the certified commit was built on;
#       empty string = certified root) EQUALS HEAD's raw parent set, read from the
#       raw commit object (`git cat-file commit HEAD`; the ENFORCE_PR_HEAD_PARENTS
#       override exists for tests and is honored only in TESTMODE). Identity, not
#       wall-clock: the reverted time-comparison
#       (BUG-1 fix, d6dc4a0) was fail-open on an un-gated HEAD (any commit with an
#       old-enough parent read fresh), a merge HEAD (first-parent time says nothing
#       about the merged-in commits), and a shallow clone (HEAD~1 unresolvable read
#       as root → fresh). Absent / unreadable / unparseable / non-GREEN / unbound /
#       pre-ADR-0006 shape (no certified_parent) → treated as RED.
#   (b) an authorization marker is present:
#       ${CLAUDE_PROJECT_DIR}/.rigor/pr-authorized   OR   $RIGOR_PR_AUTHORIZED=1.
#
# FAIL-CLOSED (F-008): "couldn't read it" NEVER reads as "GREEN, allow." A missing,
# garbage, or unbound verdict denies. There is no "assume green" path.
#
# MATCHER: only `gh pr create` is intercepted. `gh pr view`, `gh pr list`,
# `gh project create`, and embedded text (`echo gh pr create`) must NOT false-block
# — the word-boundary discipline the family establishes for git-shaped commands,
# ported to the `gh pr create` subcommand triple.
#
# PORTABILITY: pure bash 3.2 + POSIX grep/sed/tr + git (git only for the HEAD
# parent-set read, guarded by `command -v`); jq optional with a dependency-free
# fallback. No GNU-isms, no `grep -P`, no jq dependency.
#
# ── MODES ────────────────────────────────────────────────────────────────────
# HOOK MODE (default): read PreToolUse JSON on stdin; print a Claude Code deny
#   object + `exit 0` to DENY, or `exit 0` with no output to ALLOW. (Claude Code
#   reads the JSON, not the exit code, in hook mode.)
#
# TEST MODE (ENFORCE_PR_READINESS_TESTMODE=1): verdict carried in the EXIT CODE so
#   test-lib's expect_exit / assert_red_when_guard_removed can read it: 0 = ALLOW
#   (ready / not our concern), 2 = DENY (not ready / fail-closed). The DENY reason
#   is printed to stderr in both modes.

set -uo pipefail

# Dep preflight (bead skills_library-kfi): under `pipefail` a missing grep/sed/tr
# makes every matcher pipeline return non-zero, which reads as "not our concern"
# → silent ALLOW. A gate whose matcher cannot run must fail CLOSED instead
# (F-008): exit 2 is a PreToolUse blocking error in hook mode and FATAL in test
# mode. `command -v` is a bash builtin, so the preflight itself needs none of the
# tools it checks.
for _dep in grep sed tr; do
  command -v "$_dep" >/dev/null 2>&1 && continue
  echo "enforce-pr-readiness: DENY — required tool '$_dep' not found on PATH; the matcher cannot run (fail-closed, F-008)" >&2
  exit 2
done

TESTMODE="${ENFORCE_PR_READINESS_TESTMODE:-0}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
VERDICT_FILE="${PROJECT_DIR}/.rigor/commit-gate-verdict.json"
MARKER_FILE="${PROJECT_DIR}/.rigor/pr-authorized"

# ── command extraction (jq optional, dependency-free fallback) ─────────────────
# Lineage: block-push-main.sh / block-commit-main.sh.
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
# Map newlines to ';' so a later-line invocation is seen, squeeze whitespace, strip
# leading/trailing space so a leading-whitespace command is not missed.
normalize() {
  local norm
  norm=$(printf '%s' "$1" | tr '\n' ';' | tr -s '[:space:]' ' ')
  norm="${norm#" "}"; norm="${norm%" "}"
  printf '%s' "$norm"
}

# strip_transparent_wrappers (bead skills_library-4jx) — remove a leading
# TRANSPARENT-EXEC wrapper and its own options/args at every command position
# (start, or after ; & |), repeatedly, so a command a shell would run AS the gated
# operation is seen as such. Wrappers stripped: command exec nohup builtin time env
# sudo doas nice ionice setsid stdbuf unbuffer caffeinate timeout xargs — each runs
# its argument as a command. After the wrapper, a run of its own leading tokens is
# consumed: -flags, NAME=val assignments, bare numeric/duration scalars (timeout's
# `5`, nice's `10`), and a value-taking `-u`/`-C`/`-g` flag with its separated
# argument (env -u NAME, env -C dir, sudo -u user). The command is the first token
# that is none of those, so `timeout 5 git commit` / `nice -n 10 git commit` /
# `env -u X git commit` all reduce to `git commit`; `env FOO=bar ./deploy.sh` and
# `sudo -u git commit` (runs `commit` as user git) correctly do NOT. Only exec-
# transparent words strip (echo/printf/`environment`/`commander`/`timeouty` do not —
# the trailing space anchors the whole word), preserving every `echo git commit`
# must-NOT-block case. Done as a pre-pass, not a matcher-regex change: BSD grep
# mis-handles a second starred/alternated prefix group at the separator anchor.
# IRREDUCIBLE CEILING (a text pre-pass cannot close these — beaded, not claimed):
# re-quoting wrappers `bash -c "git commit"` / `sh -c` / `script -c`; token
# obfuscation `\git` / `"git" commit` / `g\it`; `env -S "git commit"` (recombines a
# quoted string). The gate is a discipline floor (ADR-0002: attested-not-proven,
# rubber-stampable), not an adversarial control; the commit side has the git-native
# pre-commit backstop, the PR side needs server-side branch protection (ADR-0002 OQ-3).
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
# is_pr_create "<raw command>" — 0 if the command is a `gh pr create` invocation,
# else 1. Anchored at start or after a command separator (so `echo gh pr create`
# does NOT match), tolerates env-var and path prefixes on `gh` and transparent-exec
# wrappers (stripped in the pre-pass), requires the exact `pr create` subcommand
# triple, and ends `create` on a word boundary (space / separator / EOL) so `gh pr
# createx` does not match. `gh pr view` and `gh project create` lack the `pr create`
# adjacency and never match.
is_pr_create() {
  local norm folded re
  norm=$(normalize "$1")
  re='(^|[;&|] *)([A-Za-z_][A-Za-z0-9_]*=[^ ;&|]* +)*([^ ;&|]*/)?gh +pr +create( |[;&|]|$)'
  # Pass 1 — exact (the pre-pif behavior, byte-preserved): -[uCg] consumes
  # `env -C dir` correctly; a lowercase `-c` stays generic (setsid's -c takes no
  # argument). Pass 2 — case-folded (bead skills_library-pif): the matcher grep
  # was already -i, but the STRIP's wrapper list was case-sensitive, so
  # `TIMEOUT 5 gh pr create` evaded on a case-insensitive FS. Folding lowercases
  # `-C` too, so the folded pass widens the value-flag class to -[ucg].
  # OR-semantics make the fold purely ADDITIVE: it can only over-MATCH
  # (fail-closed friction), never lose a pass-1 catch.
  printf '%s' "$(strip_transparent_wrappers "$norm")" | grep -qiE "$re" && return 0
  folded="$(printf '%s' "$norm" | tr '[:upper:]' '[:lower:]')"
  printf '%s' "$(strip_transparent_wrappers "$folded" ucg)" | grep -qiE "$re"
}

# ── verdict read + SHA binding (fail-closed, ADR-0006) ────────────────────────
# Pull a JSON string field's value without jq (dependency-free). Echoes empty if
# the field is absent/unreadable.
json_str_field() { # $1 = json ; $2 = field
  printf '%s' "$1" \
    | tr '\n' ' ' \
    | sed -n "s/.*\"$2\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p"
}

# head_parents — HEAD's raw parent set (space-separated SHAs; empty for a root
# commit), read from the RAW commit object. cat-file is the one read a shallow
# clone does not graft-blind: `rev-parse HEAD^` and `log --format=%P` both misread
# a shallow boundary as a root (the exact fail-open the reverted time-comparison
# had). The first-blank-line stop keeps a commit-MESSAGE line starting "parent "
# from being read as a header. ENFORCE_PR_HEAD_PARENTS (set-but-possibly-empty:
# empty = root) overrides for repo-independent tests — honored ONLY under
# ENFORCE_PR_READINESS_TESTMODE=1, so the PRODUCTION path always reads real git
# and a durable env var (direnv, settings hook env) cannot forge the binding.
# Echoes the parent set on stdout. Return: 0 established / 2 cannot establish
# (no git / no HEAD / unreadable object → fail-closed RED).
head_parents() {
  if [ "$TESTMODE" = "1" ] && [ -n "${ENFORCE_PR_HEAD_PARENTS+x}" ]; then
    printf '%s' "$ENFORCE_PR_HEAD_PARENTS"; return 0
  fi
  command -v git >/dev/null 2>&1 || return 2
  git -C "$PROJECT_DIR" rev-parse --verify HEAD >/dev/null 2>&1 || return 2
  local raw
  raw="$(git -C "$PROJECT_DIR" cat-file commit HEAD 2>/dev/null)" || return 2
  printf '%s' "$raw" | sed -n '/^$/q; s/^parent //p' | tr '\n' ' ' | sed 's/ *$//'
  return 0
}

# verdict_is_bound_green — return 0 ONLY if the artifact exists, parses, reads
# roster_result GREEN, carries a certified_parent field, and that field EQUALS
# HEAD's raw parent set exactly. Every other case (absent, unreadable, unparseable,
# non-GREEN, field missing [pre-ADR-0006 shape], mismatch [un-gated / merge /
# forged HEAD], or parents unestablishable) returns 1 (RED) — fail-closed, no
# "assume green."
verdict_is_bound_green() {
  [ -f "$VERDICT_FILE" ] || { DENY_REASON="verdict artifact absent ($VERDICT_FILE)"; return 1; }
  local raw result cert parents rs
  raw="$(cat "$VERDICT_FILE" 2>/dev/null)" || { DENY_REASON="verdict artifact unreadable"; return 1; }
  [ -n "$raw" ] || { DENY_REASON="verdict artifact empty"; return 1; }

  result="$(json_str_field "$raw" roster_result)"
  [ "$result" = "GREEN" ] || { DENY_REASON="verdict roster_result is not GREEN (got '${result:-<unparseable>}')"; return 1; }

  # certified_parent must be PRESENT as a quoted string (empty string = certified
  # root commit). A pre-ADR-0006 verdict lacks it → RED: an unbound GREEN proves
  # nothing about WHICH commit it certified. Re-run the commit gate.
  if ! printf '%s' "$raw" | tr '\n' ' ' | grep -qE '"certified_parent"[[:space:]]*:[[:space:]]*"'; then
    DENY_REASON="verdict lacks certified_parent (pre-ADR-0006 shape) — re-run the commit gate"
    return 1
  fi
  cert="$(json_str_field "$raw" certified_parent)"

  parents="$(head_parents)"; rs=$?
  if [ "$rs" -ne 0 ]; then
    DENY_REASON="cannot establish HEAD's parent set (no git/HEAD) — fail-closed"
    return 1
  fi

  if [ "$parents" != "$cert" ]; then
    DENY_REASON="verdict is NOT BOUND to HEAD (certified_parent='${cert:-<root>}' vs HEAD parents='${parents:-<root>}') — an un-gated or merge commit landed after the gate; re-run the commit gate"
    return 1
  fi
  return 0
}

# marker_present — file marker OR env flag.
marker_present() {
  [ -f "$MARKER_FILE" ] && return 0
  [ "${RIGOR_PR_AUTHORIZED:-}" = "1" ] && return 0
  return 1
}

# is_ready — BOTH conditions must hold. Sets DENY_REASON on failure.
is_ready() {
  verdict_is_bound_green || return 1
  if ! marker_present; then
    DENY_REASON="authorization marker absent (need $MARKER_FILE or \$RIGOR_PR_AUTHORIZED=1)"
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

DENY_REASON=""

# Not a `gh pr create` → not our concern → allow.
if [ -z "$COMMAND" ] || ! is_pr_create "$COMMAND"; then
  exit 0
fi

if is_ready; then
  # Ready: allow in both modes.
  exit 0
fi

# NOT ready → DENY. Print the reason to stderr in both modes (fail-closed).
echo "enforce-pr-readiness: DENY gh pr create — $DENY_REASON" >&2

if [ "$TESTMODE" = "1" ]; then
  exit 2
fi

# HOOK MODE: emit the Claude Code deny object.
printf '%s\n' "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"CDM-1-21 (ADR-0002/0006): no PR until ready. ${DENY_REASON}. Ensure the commit-gate verdict (.rigor/commit-gate-verdict.json) is a GREEN bound to HEAD (re-run the commit gate if commits landed since) and set the authorization marker (.rigor/pr-authorized or RIGOR_PR_AUTHORIZED=1) once the deliverable is complete.\"}}"
exit 0
