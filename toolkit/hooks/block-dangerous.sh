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

AUDIT_TAG="${AUDIT_TAG:-block-dangerous}"
_lib="$(dirname "$0")/../lib/audit-helpers.sh"
if [ -r "$_lib" ]; then
  # shellcheck source=/dev/null
  . "$_lib"
else
  emit() { echo "[${AUDIT_TAG}] $*"; }
fi

# is_dangerous <command-string>
# Returns 0 (true) and echoes a human reason if the command is a denied destructive form.
# Returns 1 (false) for safe commands. Pure POSIX-ERE grep; portable BSD + GNU.
is_dangerous() {
  # Normalize runs of whitespace to single spaces so patterns are spacing-agnostic.
  norm=$(printf '%s' "$1" | tr -s '[:space:]' ' ')

  # rm -rf <root>: -r and -f in either order (clustered or separate), then a path that
  # begins at filesystem root ("/" followed by whitespace or end-of-line). ERE-only.
  # BUG-F003: (\s|$) instead of \b — \b is not portable to BSD grep.
  if printf '%s' "$norm" | grep -qiE 'rm +(-[a-z]*r[a-z]*  *(-[a-z]*f[a-z]* +)?|-[a-z]*f[a-z]*  *(-[a-z]*r[a-z]* +)?)/( |$)'; then
    echo "Destructive rm at filesystem root blocked."
    return 0
  fi

  if printf '%s' "$norm" | grep -qiE 'git +reset +--hard'; then
    echo "git reset --hard blocked. Use git stash or git checkout instead."
    return 0
  fi

  # Force push: deny -f / --force, but ALLOW --force-with-lease (presence of lease vetoes).
  if printf '%s' "$norm" | grep -qiE 'git +push +.*(-f( |$)|--force( |$))' \
     && ! printf '%s' "$norm" | grep -qiE -- '--force-with-lease'; then
    echo "git push --force blocked. Use --force-with-lease if needed."
    return 0
  fi

  # git clean with both -f and -d (clustered either order). -n (dry-run) is unaffected.
  if printf '%s' "$norm" | grep -qiE 'git +clean +.*-[a-z]*f[a-z]*d|git +clean +.*-[a-z]*d[a-z]*f'; then
    echo "git clean -fd blocked. Review untracked files manually."
    return 0
  fi

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
