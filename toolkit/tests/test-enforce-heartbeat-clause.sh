#!/usr/bin/env bash
# test-enforce-heartbeat-clause.sh — negative test for the heartbeat/liveness
# dispatch hook (F-007: an audit that can't prove it FAILs on bad input enforces
# nothing). The hook is a PreToolUse hook that ALWAYS exits 0 and signals via a
# JSON permissionDecision, so we wrap it: run_hook maps "deny" -> exit 1,
# anything else (allow / no decision) -> exit 0. Then test-lib's exit-code
# asserts express "good prompt allowed, bad prompt blocked."
#
# NOTE: intentionally NO `set -e`. test-lib runs commands that are SUPPOSED to
# exit non-zero (that is the whole point of a negative test); `set -e` would
# abort the harness the moment the bad-input case correctly fails.

HERE="$(cd "$(dirname "$0")" && pwd)"
source "${HERE}/../lib/test-lib.sh"

HOOK="${HERE}/../hooks/enforce-heartbeat-clause.sh"
FIX="${HERE}/fixtures/enforce-heartbeat-clause"
mkdir -p "$FIX"

# --- Fixtures ---------------------------------------------------------------
# GOOD: dispatch prompt that inlines the full liveness clause (all default
# markers: heartbeat heading + emit/append status + presume-drop/re-dispatch).
cat > "${FIX}/good.json" <<'EOF'
{
  "tool_name": "Task",
  "tool_input": {
    "prompt": "You are a sub-agent.\n\n## Heartbeat / liveness protocol\n1. Create heartbeat-worker.jsonl as your first action.\n2. After each step, append a status record with progress n/total.\n3. In your final reply, report the heartbeat record count.\n4. If the heartbeat is not maintained the orchestrator will presume a drop and re-dispatch."
  }
}
EOF

# BAD: dispatch prompt with NO liveness clause at all — the silent-drop hole.
cat > "${FIX}/bad-no-clause.json" <<'EOF'
{
  "tool_name": "Task",
  "tool_input": {
    "prompt": "You are a sub-agent. Do the task and report back when finished."
  }
}
EOF

# BAD (W1-9 review, scattered-vocabulary bypass): NO real liveness clause, but
# incidental words — "liveness", an emit-verb ("Output"), "status", and "silent
# drop" — scattered across separate lines. Flattening must NOT let these join into a
# false-PASS: marker-2 requires an emit-verb next to a status-RECORD noun, which a bare
# "status board" is not. Must DENY.
cat > "${FIX}/bad-scattered-vocab.json" <<'EOF'
{
  "tool_name": "Task",
  "tool_input": {
    "prompt": "Check the liveness of the pool.\nOutput the findings.\nThen update the status board.\nNever allow a silent drop of work."
  }
}
EOF

# BAD (specific false-green): has a 'heartbeat' heading and an 'emit status'
# line, but OMITS the drop-detection/re-dispatch semantics — the load-bearing
# teeth. A lazy substring match on just the word 'heartbeat' would false-GREEN
# this; the hook must still DENY because the presume-drop marker is missing.
cat > "${FIX}/bad-no-drop-semantics.json" <<'EOF'
{
  "tool_name": "Task",
  "tool_input": {
    "prompt": "You are a sub-agent.\n\n## Heartbeat\nPlease emit a progress status after each step so I can see liveness. Thanks!"
  }
}
EOF

# GOOD (regression guard, W1-4): the hook's OWN canonical clause, which WRAPS the
# "emit/append a one-line" / "status record" phrase across a line break (and likewise
# "presumes a DROP and" / "re-dispatches"). This previously self-DENIED because the
# line-oriented grep could not match a wrapped marker — the defect that made the hook
# unwireable. It MUST now ALLOW.
# BUG-6 (W1-9 review): built with a heredoc, NOT python3 — a python3-absent box left the
# fixture 0 bytes, so the hook saw an empty prompt and ALLOWed regardless of the fix
# (a maquette-S36 vacuity). The `\n` line-wraps + `\"` JSON-example quotes are literal here.
cat > "${FIX}/good-canonical-wrapped.json" <<'EOF'
{"tool_name":"Task","tool_input":{"prompt":"# Bug Hunter\nYou are a sub-agent.\n\n## Heartbeat / liveness protocol (MANDATORY)\n1. As your FIRST action, create a heartbeat-<agent>.jsonl record.\n2. After every distinct work or verification step, emit/append a one-line\n   status record: {\"ts\":\"<iso8601>\",\"step\":\"<desc>\",\"progress\":\"<n/total>\"}.\n3. In your final reply, attest the heartbeat record count (wc -l).\n4. If the heartbeat stalls, the orchestrator presumes a DROP and\n   re-dispatches. No silent drops.\n"}}
EOF

# EMPTY: not a gatable dispatch (no prompt) — hook must ALLOW (BUG-4).
cat > "${FIX}/empty.json" <<'EOF'
{ "tool_name": "Task", "tool_input": {} }
EOF

# MALFORMED: not valid JSON — hook must DENY (BUG-1, fail-closed).
printf '%s' '{ "tool_input": { "prompt": ' > "${FIX}/malformed.json"

# --- Wrapper: deny -> exit 1, otherwise exit 0 ------------------------------
run_hook() {
  out="$(bash "$HOOK" < "$1" 2>/dev/null)"
  case "$out" in
    *'"permissionDecision":"deny"'* | *'"permissionDecision": "deny"'*) return 1 ;;
    *) return 0 ;;
  esac
}

# --- Assertions -------------------------------------------------------------
# Core F-007 guard: good prompt allowed (0), bad prompt blocked (!=0).
assert_red_when_guard_removed \
  "run_hook '${FIX}/good.json'" \
  "run_hook '${FIX}/bad-no-clause.json'"

# The named false-green: partial clause missing drop semantics MUST be denied.
expect_exit 1 run_hook "${FIX}/bad-no-drop-semantics.json"

# Good case passes on its own.
expect_exit 0 run_hook "${FIX}/good.json"

# Regression: the hook's own WRAPPED canonical clause must ALLOW (W1-4 self-denial fix).
expect_exit 0 run_hook "${FIX}/good-canonical-wrapped.json"

# W1-9 review: the scattered-incidental-vocabulary bypass MUST be DENIED (the flatten
# fix must not let unrelated words on separate lines satisfy the emit->status marker).
expect_exit 1 run_hook "${FIX}/bad-scattered-vocab.json"

# Empty prompt is allowed (not a dispatch we can gate).
expect_exit 0 run_hook "${FIX}/empty.json"

# Malformed JSON is denied (fail-closed).
expect_exit 1 run_hook "${FIX}/malformed.json"

# (kfi) dep preflight: missing grep/sed/tr/awk must fail CLOSED (exit 2) —
# previously PATH='' made marker detection crash under set -e (exit 127, which
# PreToolUse treats as non-blocking = ALLOW). Goes RED if the preflight is
# removed (the stripped copy exits 127, not 2).
expect_exit 2 env PATH='' /bin/bash "${HOOK}" < /dev/null

test_summary
