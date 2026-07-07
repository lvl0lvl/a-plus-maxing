#!/usr/bin/env bash
# toolkit/hooks/block-dangerous.sh — PreToolUse/Bash guard that DENIES destructive shell commands.
#
# WHAT IT ENFORCES (CDM: rigor / destructive-command guard):
#   A PreToolUse hook for the Bash tool. It inspects the proposed shell command and
#   returns a `deny` permission decision for forms that are irrecoverable or routinely
#   catastrophic, while ALLOWING their safe cousins:
#     - rm -rf <root>        DENY   (rm -rf / and equivalents)   ALLOW: rm -rf ./build
#     - git reset --hard     DENY                                ALLOW: git reset, git stash
#     - git push --force/-f  DENY                                ALLOW: git push --force-with-lease
#     - git clean -fd        DENY                                ALLOW: git clean -n
#
# SOURCE LINEAGE:
#   Generalized from this repo's own .claude/hooks/block-dangerous.sh, which carries the
#   F-003 regex fix: the rm-root pattern is written to be BSD-grep correct (no GNU-only
#   \b / PCRE constructs in the BRE/ERE path), so it fires identically on macOS (BSD grep,
#   here ugrep-as-grep) and Linux (GNU grep). Project-specific paths were removed and the
#   matching is parameterized; default behavior is unchanged.
#
# BUG / FINDING NOTES CARRIED FORWARD:
#   - BUG-F003 (portability): earlier drafts used \b word boundaries and -P PCRE, which are
#     GNU/PCRE-isms. macOS BSD grep silently treats \b literally -> false-GREEN (dangerous
#     command waved through). FIX: use POSIX ERE only (grep -E), anchor with explicit
#     whitespace/EOL classes ((\s|$)) instead of \b. Every regex below is ERE-portable.
#   - --force-with-lease MUST be allowed: the force-push deny is gated on the ABSENCE of
#     --force-with-lease, not just the presence of -f/--force, so the safe form passes.
#
# USAGE:
#   Hook mode (default): reads the PreToolUse JSON event on stdin, writes the hook
#     decision JSON on stdout, exits 0.  Wire into settings.json PreToolUse/Bash.
#   Check mode (for tests/CI):  block-dangerous.sh --check '<command string>'
#     exit 0 = ALLOW, exit 1 = DENY. Prints a one-line [block-dangerous] reason on deny.
#     This mode is jq-free so the negative test runs anywhere.
#
# Sourcing the shared lib is optional: this is a hook, not a verdict-style audit, but we
# adopt its AUDIT_TAG/emit shape for log uniformity when the lib is present.

set -u

# Dep preflight (bead skills_library-kfi): a missing grep/tr makes every matcher
# pipeline return non-zero (the pipeline's status is grep's 127), which reads as
# "not a dangerous command" → silent ALLOW. A guard whose matcher cannot run must
# fail CLOSED instead (F-008): exit 2 is a PreToolUse blocking error in hook mode
# and non-zero (deny) in --check mode. `command -v` is a bash builtin, so the
# preflight itself needs none of the tools it checks. (block-dangerous's matcher
# uses only grep+tr — NOT sed, unlike the seven sed-parsing hooks; review QUAL-1.)
for _dep in grep tr; do
  command -v "$_dep" >/dev/null 2>&1 && continue
  echo "block-dangerous: DENY — required tool '$_dep' not found on PATH; the matcher cannot run (fail-closed, F-008)" >&2
  exit 2
done

AUDIT_TAG="${AUDIT_TAG:-block-dangerous}"
_lib="$(dirname "$0")/../lib/audit-helpers.sh"
if [ -r "$_lib" ]; then
  # shellcheck source=/dev/null
  . "$_lib"
else
  emit() { echo "[${AUDIT_TAG}] $*"; }
fi

# _flag_present <norm> <short-letter> <long-word>
# True if a short flag cluster conveying <short-letter> (e.g. -rf, -r) OR the long
# form --<long-word> is present as its own whitespace-delimited token. POSIX-ERE,
# BSD+GNU safe (no \b / -P). A long flag is NOT matched by the short pattern because
# the char after its first '-' is another '-', which is outside [a-z].
_flag_present() {
  printf '%s' "$1" | grep -qiE -- "(^| )-[a-z]*$2[a-z]*( |$)" && return 0
  printf '%s' "$1" | grep -qiE -- "(^| )--$3( |$)" && return 0
  return 1
}

# is_dangerous <command-string>
# Returns 0 (true) and echoes a human reason if the command is a denied destructive form.
# Returns 1 (false) for safe commands. Pure POSIX-ERE grep; portable BSD + GNU.
is_dangerous() {
  # Normalize runs of whitespace to single spaces so patterns are spacing-agnostic.
  norm=$(printf '%s' "$1" | tr -s '[:space:]' ' ')

  # git reset --hard is a specific dangerous phrase — a whole-string match is correct:
  # unlike the decomposed checks below it cannot be assembled across two commands.
  if printf '%s' "$norm" | grep -qiE 'git +reset +--hard'; then
    echo "git reset --hard blocked. Use git stash or git checkout instead."
    return 0
  fi

  # BUG-3 (W1-2 review, 2026-07-02): the rm-root / git-clean / git-push-force checks are
  # DECOMPOSED — each requires several sub-conditions to CO-OCCUR (rm token AND recursive
  # AND force AND a root target; or clean AND force AND -d; or push AND force). The prior
  # version tested each sub-condition against the WHOLE command, so tokens from DIFFERENT
  # invocations in a compound command satisfied them jointly and DENIED safe commands
  # (`rm -rf ./build && ls /`, `git clean -f ./x ; ls -d */`, `git push origin main ; rm -f x`)
  # — the exact PF-S1-05 over-block the guard warns against. Evaluate each decomposed check
  # PER SEGMENT (split the normalized command on ; & |) so the sub-conditions must belong
  # to ONE invocation. Whole-command danger in ANY segment (`ls / && rm -rf /`) is still
  # caught because that dangerous invocation is its own segment.
  while IFS= read -r seg; do
    [ -n "$seg" ] || continue

    # rm -rf <root>: rm + a recursive flag + a force flag (clustered -rf/-fr, separate
    # -r -f, or long --recursive --force) + a ROOT target ("/" or the root glob "/*") in
    # THIS segment. Scope stays narrow to the root target so deep absolute paths
    # (`rm -rf /tmp/scratch`, `/home/x/build`) are NOT over-blocked (PF-S1-05). KNOWN
    # RESIDUAL: a quote-wrapped root (`rm -rf '/'`) is not caught (pre-existing; the token
    # carries the quote) — tracked, not introduced here.
    if printf '%s' "$seg" | grep -qiE '(^| )rm( |$)' \
       && _flag_present "$seg" r recursive \
       && _flag_present "$seg" f force \
       && printf '%s' "$seg" | grep -qiE -- '(^| )/\*?( |$)'; then
      echo "Destructive rm at filesystem root blocked."
      return 0
    fi

    # git clean with BOTH force (-f/--force) and directories (-d) in ANY flag form
    # (clustered -fd/-df or separate -f -d / -d -f), within THIS segment. -n alone is safe.
    if printf '%s' "$seg" | grep -qiE '(^| )git +clean( |$)' \
       && _flag_present "$seg" f force \
       && _flag_present "$seg" d directories; then
      echo "git clean -fd blocked. Review untracked files manually."
      return 0
    fi

    # git push force: deny -f / --force within THIS segment, but ALLOW --force-with-lease.
    # Per-segment evaluation also fixes the sibling non-adjacency defect the prior
    # whole-command check had (`git push origin main ; rm -f x` no longer false-DENIES).
    if printf '%s' "$seg" | grep -qiE 'git +push +.*(-f( |$)|--force( |$))' \
       && ! printf '%s' "$seg" | grep -qiE -- '--force-with-lease'; then
      echo "git push --force blocked. Use --force-with-lease if needed."
      return 0
    fi
  done <<EOF
$(printf '%s' "$norm" | tr ';&|' '\n')
EOF

  return 1
}

# emit_deny_json <reason> — print the PreToolUse deny decision.
emit_deny_json() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$1"
}

main() {
  if [ "${1:-}" = "--check" ]; then
    # jq-free test/CI mode: exit 1 = DENY, 0 = ALLOW.
    cmd="${2:-}"
    if reason=$(is_dangerous "$cmd"); then
      emit "DENY: $reason"
      return 1
    fi
    return 0
  fi

  # Hook mode: read the event JSON from stdin and extract the command.
  if ! command -v jq >/dev/null 2>&1; then
    # No jq: fail-OPEN for the hook (do not block the tool on our own env error),
    # but make the gap loud. We cannot inspect the command without a JSON reader.
    emit "FATAL: jq not found; cannot inspect command — allowing (fail-open hook)." >&2
    exit 0
  fi
  COMMAND=$(jq -r '.tool_input.command // empty')
  if reason=$(is_dangerous "$COMMAND"); then
    emit_deny_json "$reason"
  fi
  exit 0
}

main "$@"
