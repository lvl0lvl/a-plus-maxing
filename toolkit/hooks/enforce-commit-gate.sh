#!/usr/bin/env bash
# toolkit/hooks/enforce-commit-gate.sh — PreToolUse(Bash) commit-time fail-closed
# gate. On a `git commit` invocation, run the project's configured gate roster
# ($RIGOR_COMMIT_GATE); DENY (exit 2) on any non-zero / run-error result, and on
# GREEN persist a staleness-stampable verdict artifact for downstream gates.
#
# ENFORCES (ADR-0001, T1; giq.1.6/1.3 P0): a `git commit` over a RED test/audit
# roster is denied at the moment of commit, not caught sessions later at close.
#
# SOURCE LINEAGE: input method, command extraction, and the BUG-3-hardened
# git-commit matcher are taken verbatim from hooks/block-commit-main.sh so the
# marginal surface is one new check (run the gate), not a new mechanism. The deny
# is the same PreToolUse exit-2 contract.
#
# FAIL-CLOSED (F-008): "couldn't verify" must never read as "verified clean."
#   - $RIGOR_COMMIT_GATE non-zero          → DENY (the gate said RED).
#   - $RIGOR_COMMIT_GATE could not RUN     → DENY (a check that cannot run does
#     not pass — mirrors lib/audit-helpers.sh skipped()→FATAL).
#   - $RIGOR_COMMIT_GATE GREEN             → ALLOW + write verdict (GREEN + epoch ts
#     + certified_parent — the SHA binding enforce-pr-readiness.sh checks, ADR-0006).
#   - $RIGOR_COMMIT_GATE UNSET             → loud stderr SKIP + ALLOW (never silent,
#     never false-block an unconfigured project — ADR-0001 Decision).
#
# RESIDUAL (carried from block-commit-main.sh:39): the cwd-anchored Bash matcher
#   only inspects the proposed command text — it catches `git commit`, `git -C
#   <path> commit`, and `cd <path> && git commit` shapes by text, but a commit made
#   entirely outside any git invocation the hook sees is out of scope; ADR-0001
#   Decision §2 ships a git-native pre-commit hook as the layered second line.
#
# PORTABILITY: pure bash 3.2 + POSIX grep/tr/sed; jq optional (dependency-free
#   fallback parser). Paths via ${CLAUDE_PROJECT_DIR}; no absolute paths.

set -uo pipefail

# Dep preflight (bead skills_library-kfi): under `pipefail` a missing grep/sed/tr
# makes every matcher pipeline return non-zero, which reads as "not our concern"
# → silent ALLOW. A gate whose matcher cannot run must fail CLOSED instead
# (F-008): exit 2 is a PreToolUse blocking error in hook mode and FATAL in test
# mode. `command -v` is a bash builtin, so the preflight itself needs none of the
# tools it checks.
for _dep in grep sed tr; do
  command -v "$_dep" >/dev/null 2>&1 && continue
  echo "enforce-commit-gate: DENY — required tool '$_dep' not found on PATH; the matcher cannot run (fail-closed, F-008)" >&2
  exit 2
done

# ── command extraction (jq optional, dependency-free fallback) ─────────────────
# Matches block-commit-main.sh's input method exactly.
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

# ── git-commit matcher (BUG-3, from block-commit-main.sh) ──────────────────────
# Anchors at start / after a separator, tolerates env-var + path prefixes and
# flags between `git` and `commit` (so `git -C <path> commit` matches), and ends on
# space / separator / EOL — so `commit-tree`, `git config`, `git status`, and
# `echo … commit` are NOT matched. `cd <path> && git commit` matches because the
# `git commit` clause follows the `&&` separator.
COMMIT_MATCHER_RE='(^|[;&|] *)([A-Za-z_][A-Za-z0-9_]*=[^ ;&|]* +)*([^ ;&|]*/)?git +([^|&;]*[[:space:]])?commit( |[;&|]|$)'

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

is_git_commit() {  # $1 = raw command; 0 if a git commit invocation, else 1
  local norm folded
  norm=$(printf '%s' "$1" | tr '\n' ';' | tr -s '[:space:]' ' ')
  norm="${norm#" "}"; norm="${norm%" "}"
  # Pass 1 — exact (the pre-pif behavior, byte-preserved): the -[uCg] value-flag
  # class consumes `env -C dir` / `sudo -u user` correctly while leaving a
  # lowercase `-c` generic (setsid's -c takes NO argument — consuming a value
  # there would false-ALLOW `setsid -c git commit`).
  printf '%s' "$(strip_transparent_wrappers "$norm")" | grep -qE "$COMMIT_MATCHER_RE" && return 0
  # Pass 2 — case-folded (bead skills_library-pif): on a case-insensitive FS
  # `GIT commit` / `TIMEOUT 5 git commit` execute exactly like their lowercase
  # forms, but pass 1 reads them as not-a-commit → un-gated commit (executed
  # triage C3). Folding lowercases `-C` too, so this pass widens the value-flag
  # class to -[ucg]. OR-semantics make the fold purely ADDITIVE: it can only
  # over-MATCH (fail-closed friction), never lose a pass-1 catch.
  folded="$(printf '%s' "$norm" | tr '[:upper:]' '[:lower:]')"
  printf '%s' "$(strip_transparent_wrappers "$folded" ucg)" | grep -qE "$COMMIT_MATCHER_RE"
}

# ── deny helper (PreToolUse exit-2 contract) ──────────────────────────────────
deny() {  # $1 = reason
  echo "enforce-commit-gate: DENY — $1" >&2
  exit 2
}

# ── main ──────────────────────────────────────────────────────────────────────
# Read the proposed command (command may be supplied as $1 instead of stdin JSON,
# mirroring block-commit-main.sh).
if [ "$#" -ge 1 ] && [ -n "${1:-}" ]; then
  COMMAND="$1"
else
  HOOK_INPUT="$(cat)"
  COMMAND="$(extract_command "$HOOK_INPUT")"
fi

# Empty command, or not a git commit → not our concern (ALLOW).
[ -n "$COMMAND" ] || exit 0
is_git_commit "$COMMAND" || exit 0

# Unconfigured: loud SKIP + ALLOW. Never silent, never false-block (ADR-0001).
if [ -z "${RIGOR_COMMIT_GATE:-}" ]; then
  echo "enforce-commit-gate: SKIP — \$RIGOR_COMMIT_GATE is not set; commit-time gate NOT enforced for this commit. Configure it (e.g. via fresh-start) so commits are checked against a roster. ALLOWING (unconfigured projects are not false-blocked)." >&2
  exit 0
fi

# Run the configured gate. A run-error (command not found / cannot execute) is
# fail-closed: a check that cannot RUN does not PASS (F-008).
GATE_OUT="$(eval "$RIGOR_COMMIT_GATE" 2>&1)"
GATE_RC=$?

if [ "$GATE_RC" -eq 127 ] || [ "$GATE_RC" -eq 126 ]; then
  deny "the configured gate could not RUN (\$RIGOR_COMMIT_GATE='$RIGOR_COMMIT_GATE' exited $GATE_RC). Fail-closed: a gate that cannot run does not pass (F-008). Fix the gate command, then commit."
fi

if [ "$GATE_RC" -ne 0 ]; then
  deny "commit gate is RED (\$RIGOR_COMMIT_GATE exited $GATE_RC). Commit blocked over a failing roster (giq.1.6 recurrence guard). Make the gate GREEN, then commit. Last gate output:"$'\n'"$GATE_OUT"
fi

# GREEN: persist the verdict artifact (GREEN + epoch ts + certified_parent SHA
# binding, ADR-0006) under .rigor, then ALLOW.
#
# certified_parent = the SHA the certified commit will be built on: HEAD at gate
# time for a plain commit, HEAD's raw parent set for --amend (the amend REPLACES
# HEAD, so the new commit inherits HEAD's parents), empty for an unborn branch
# (the certified commit will be the root) — and the same fail-closed empty when
# git is unavailable or HEAD is unreadable (a git-present reader then rejects any
# non-root HEAD). enforce-pr-readiness.sh later requires
# HEAD's raw parent set to EQUAL this exactly — identity, not wall-clock (the
# reverted time-comparison was fail-open on un-gated / merge / shallow HEADs).
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
RIGOR_DIR="$PROJECT_DIR/.rigor"
mkdir -p "$RIGOR_DIR"
TS="$(date +%s)"

# raw_head_parents — HEAD's parent SHAs (space-separated) from the RAW commit
# object. cat-file is the one read a shallow clone does not graft-blind (rev-parse
# HEAD^ and log --format=%P both misread a shallow boundary as a root). The
# first-blank-line stop keeps a commit-MESSAGE line starting "parent " from being
# read as a header.
raw_head_parents() {
  git -C "$PROJECT_DIR" cat-file commit HEAD 2>/dev/null \
    | sed -n '/^$/q; s/^parent //p' | tr '\n' ' ' | sed 's/ *$//'
}

CERTIFIED_PARENT=""
if command -v git >/dev/null 2>&1 \
   && git -C "$PROJECT_DIR" rev-parse --verify HEAD >/dev/null 2>&1; then
  # --amend detection (bead skills_library-8ul) scans a QUOTE-STRIPPED copy of the
  # command: a plain commit whose -m message merely CONTAINED a whitespace-bounded
  # "--amend" token previously mis-bound certified_parent to HEAD's parents → the
  # reader false-DENIED the happy path (executed triage C4). Stripping is textual
  # ('…' pairs first, then "…" pairs honoring \") — not a shell parse: an
  # unbalanced-quote command can still mis-detect in either direction, which stays
  # fail-closed — a mis-recorded parent only ever produces a reader DENY (re-run
  # the gate), never an ALLOW (ADR-0006 Consequences).
  AMEND_SCAN="$(printf '%s' "$COMMAND" | sed -E "s/'[^']*'//g" | sed -E 's/"(\\.|[^"\\])*"//g')"
  if printf '%s' "$AMEND_SCAN" | grep -qE '(^|[[:space:]])--amend([[:space:]]|$|[;&|])'; then
    CERTIFIED_PARENT="$(raw_head_parents)"
  else
    CERTIFIED_PARENT="$(git -C "$PROJECT_DIR" rev-parse --verify HEAD 2>/dev/null)"
  fi
fi

printf '{"roster_result":"GREEN","ts":%s,"certified_parent":"%s"}\n' \
  "$TS" "$CERTIFIED_PARENT" > "$RIGOR_DIR/commit-gate-verdict.json"

exit 0
