#!/bin/bash
# block-pii-commit.sh — PreToolUse hook for the Bash tool. ADR-0005-T1.
#
# The trunk content-scan trust boundary. When a `git commit` stages (a) a
# filled-scaffold value, (b) a vault/store/ file, or (c) any staged file whose
# CONTENTS carry operator PII, deny the commit. Mirror of block-ungated-vault-write.sh.
#
# Conditions 1 & 2 are PATH/membership checks over the staged set. Condition 3
# delegates the token scan ENTIRELY to scripts/guard/pii_scan.scan_scoped (the
# SEC-01(a) reuse contract; the scope policy is single-sourced with the pre-push
# backstop) — NO bash/rg/grep token reimplementation. The scan is scoped per the
# ADR-0005 amended Decision 2026-06-06 (bead qwj option iii), with the contact
# model made operator-specific at 3lv (the generic @gmail.com trunk-wide pattern
# flooded on synthetic fixture/bead emails — 14 false hits on a routine staged set
# — so it moved to a gitignored config like the name). scan_scoped runs:
#   • trunk-wide — structural store-line patterns + the operator's REAL contact
#     tokens over every staged file EXCEPT tests/ paths, which get the contact
#     tokens ONLY (their structural reading-shaped literals are synthetic fixtures
#     by construction — the known-fixture partition, dv3). The contact has no
#     legitimate tracked use (provenance prose uses the operator's name, never the
#     email). On a fresh clone the config is absent -> structural patterns only.
#   • identity, data-bearing only — the operator-name patterns over health-data
#     paths (scaffold values, store, raw dropzones) where the name IS a leak; the
#     name is accepted provenance in governance/session/design prose and must NOT
#     be flagged trunk-wide.
# Deny if the combined count is >=1.
#
# bd auto-stage coverage (eb1, PR#84 HIST-2): the bd pre-commit git hook stages
# .beads/issues.jsonl INSIDE `git commit`, AFTER this PreToolUse snapshot, so
# that file is invisible to the staged-set capture. The working-tree bd file is
# therefore unconditionally appended to the trunk-wide scan set below on every
# commit, covering bead text ALREADY FLUSHED to .beads/issues.jsonl — the exact
# vector of the historical operator-email leak (bead 46m). NOT covered here:
# bead text still pending in .beads/beads.db at scan time — the bd pre-commit
# hook flushes AND stages it inside `git commit`, after this scan ran, so it
# commits unscanned at this boundary; the pre-push scan remains the backstop
# for that window (tracked: bead ycqo).
#
# Fail-closed (Security HIGH-1): any error in the scan path — import fails, scan
# raises, the python3 -c returns non-zero, or the git/jq plumbing fails — emits
# deny, NEVER allow. This is the opposite of the sibling hooks' allow-on-error
# idioms, which are tolerable for a branch-name annoyance but a silent PII bypass
# at a distribution boundary.
#
# TEST/OVERRIDE ENV (never set in production):
#   BLOCK_PII_COMMIT_PROJECT_ROOT   — git root for staged-file detection.
#   BLOCK_PII_COMMIT_PII_SCAN_ROOT  — sys.path root for the pii_scan import
#                                     (default: PROJECT_ROOT). Tests point it at a
#                                     stub (SEC-01(b)) or an unimportable dir
#                                     (fail-closed).
#
# Exit codes (Claude Code hook convention):
#   prints deny JSON + exits 0 → deny tool call
#   exits 0 with no output      → allow tool call

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Fallback root when the hook input carries no resolvable cwd (see resolve-target-repo
# below). The env override lets tests seed it. Never set in production.
FALLBACK_ROOT="${BLOCK_PII_COMMIT_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

deny() {  # $1 = reason string
    jq -nc --arg r "$1" \
        '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
    exit 0
}

# git-commit detection is single-sourced (bead mic). Sourced AFTER deny() so a load
# failure fails CLOSED: under set -uo pipefail (no set -e) a failed source is non-fatal,
# so without this guard is_git_commit would be undefined and `is_git_commit ... || exit 0`
# would silently ALLOW — skipping the PII scan. This hook is fail-CLOSED (Security HIGH-1),
# so a missing/corrupt matcher lib denies (PR#80 SEC-1).
source "$SCRIPT_DIR/lib/commit-matcher.sh" 2>/dev/null
declare -F is_git_commit >/dev/null 2>&1 || deny "PII-FREE-TRUNK: commit-matcher lib failed to load (is_git_commit undefined). Failing closed — commit blocked."

# Path scope (SCAFFOLD_PREFIX / STORE_PREFIX / PER_SE_DENY_PREFIXES /
# DATA_BEARING_PREFIXES) is single-sourced with the pre-push backstop so the two
# boundaries cannot drift (PR#84 QUAL-1, the PR#80 lesson). Same fail-closed guard.
source "$SCRIPT_DIR/lib/pii-scan-scope.sh" 2>/dev/null
[[ -n "${STORE_PREFIX:-}" ]] || deny "PII-FREE-TRUNK: pii-scan-scope lib failed to load (path prefixes undefined). Failing closed — commit blocked."

# Target-repo resolution single-sourced (bead 29u4): the staged-set scan must read
# the index of the repo RECEIVING the commit (a worktree's, when the commit is
# issued there), not the checkout this script ships in.
source "$SCRIPT_DIR/lib/resolve-target-repo.sh" 2>/dev/null

HOOK_INPUT=$(cat)
COMMAND=$(jq -r '.tool_input.command // empty' <<< "$HOOK_INPUT")
JQ_RC=$?
# Fail-closed (F-BUG1): jq rc != 0 means stdin was not valid JSON — deny. The empty-
# COMMAND early-exit below must NOT swallow that case (it would ALLOW on a parse fail).
# After this guard, an empty COMMAND can only be the legitimate valid-JSON-but-no-
# command-field case -> allow.
if [[ $JQ_RC -ne 0 ]]; then
    deny "PII-FREE-TRUNK: hook stdin was not valid JSON (jq parse failed, rc=$JQ_RC). Failing closed — commit blocked."
fi
[[ -z "$COMMAND" ]] && exit 0

# Only a git commit is our concern — detection single-sourced in lib/commit-matcher.sh (mic).
is_git_commit "$COMMAND" || exit 0

# Resolve the repo receiving the commit (29u4); a missing/corrupt lib falls back to
# the pre-29u4 root — never weaker — with a loud warning (broken install). The
# scanner-import default follows the resolved root (a worktree checkout carries the
# tracked scripts/guard/pii_scan.py); tests always pin it explicitly.
if declare -F resolve_target_repo >/dev/null 2>&1; then
    PROJECT_ROOT=$(resolve_target_repo "$HOOK_INPUT" "$FALLBACK_ROOT")
else
    echo "block-pii-commit: resolve-target-repo lib failed to load; scanning the script-path root." >&2
    PROJECT_ROOT="$FALLBACK_ROOT"
fi
PII_SCAN_ROOT="${BLOCK_PII_COMMIT_PII_SCAN_ROOT:-$PROJECT_ROOT}"

# ── Condition 0: in-command staging defeats the snapshot -> deny (sequencing) ───
# This PreToolUse hook snapshots the staged set BELOW, BEFORE the command runs, so
# any staging done INSIDE the same command (a `git add`, a `git commit -a`, or a
# pathspec `git commit <file>`) is invisible to the content scan — it would scan an
# empty/stale set and sail through (the vacuous-scan hole discovered live at 3lv
# registration). The scannable shape is a plain `git commit` against a
# previously-staged set; these forms deny with sequencing guidance.
#
# SEQ_CMD normalizes for matching (PR#84 SEC-1/BUG-2/BUG-5): newlines -> spaces (a
# multi-line tool call is ONE pre-snapshot unit, so a later-line `git add` must be
# seen), then quoted '...'/"..." segments are stripped so the commit MESSAGE cannot
# trip the staging detectors (`-m 'docs: git add ...'` is not staging — BUG-5) and a
# `;` inside a message cannot hide a trailing `-a` (BUG-2c). The detectors tolerate
# arbitrary git global options (`-c k=v`, `--work-tree=.`, `-C path`) between `git`
# and the subcommand (SEC-1/BUG-2b). Threat model is accidental leakage, not
# adversarial shell. Accepted residual (documented): a bare top-level-filename
# pathspec commit (`git commit notes.md`, no path separator) — caught by the
# pre-push backstop, not here.
SEQ_CMD=$(printf '%s' "$COMMAND" | tr '\n' ' ' | sed "s/'[^']*'//g; s/\"[^\"]*\"//g" | tr -s '[:space:]' ' ')
SEQ_SUBCMD_GAP='([^;&|]*[[:space:]])?'   # any options between git and the subcommand
if printf '%s' "$SEQ_CMD" | grep -qE "(^|[;&|[:space:]])git[[:space:]]+${SEQ_SUBCMD_GAP}(add|mv|rm)([[:space:]]|\$|[;&|])"; then
    deny "PII-FREE-TRUNK: staging and committing in ONE command defeats the content scan (the staged set is snapshotted BEFORE your command runs). Run the 'git add'/'git mv'/'git rm' first as its own command, then 'git commit' separately so the scan sees what you staged."
fi
if printf '%s' "$SEQ_CMD" | grep -qE "(^|[;&|[:space:]])git[[:space:]]+${SEQ_SUBCMD_GAP}commit[[:space:]]${SEQ_SUBCMD_GAP}(-[a-zA-Z]*a[a-zA-Z]*|--all)([[:space:]]|\$|[;&|=])"; then
    deny "PII-FREE-TRUNK: 'git commit -a/--all' stages files itself, AFTER this scan snapshots the staged set — the content scan cannot see them. Stage explicitly with 'git add' (own command), then 'git commit' without -a."
fi
# Pathspec commit: a path-separator-bearing bare argument anywhere after `commit`
# commits that file's working-tree content regardless of the staged set (BUG-2a).
# The bare token must not start with '-' (a flag) and must contain a '/'.
if printf '%s' "$SEQ_CMD" | grep -qE "(^|[;&|[:space:]])git[[:space:]]+${SEQ_SUBCMD_GAP}commit[[:space:]]([^;&|]*[[:space:]])?[^-;&|[:space:]][^;&|[:space:]]*/"; then
    deny "PII-FREE-TRUNK: committing a pathspec ('git commit <path>') commits that file's working-tree content, which this scan (keyed on the staged set) cannot see. 'git add <path>' first as its own command, then 'git commit'."
fi

# Staged set git will actually commit — NOT git ls-files (the HEAD/tracked set), so a
# git add-ed file absent from HEAD is scanned (Fix 3). Filter ACMRT covers Added,
# Copied, Modified, Renamed, Type-changed: R/T must be included or a high-similarity
# rename (or a type change) into a data path injects PII while being dropped from the
# staged set -> silent allow (F-SEC1). For an R entry --name-only emits the DESTINATION
# path, correct for both the path checks and the content scan.
# Capture the git rc explicitly: a process-substitution while-loop would discard it
# and let a broken `git diff --cached` read as an empty staged set -> a silent allow.
# core.quotepath=false: without it git C-quotes a non-ASCII path ("donn\303\251es.md"),
# the python scan open()s that literal, OSError-swallows the miss, and the file goes
# UNSCANNED -> a silent fail-open for any accented/Unicode filename carrying PII
# (PR#84 BUG-1). The flag makes git emit the raw UTF-8 path the scanner can open.
GIT_OUT=$(git -C "$PROJECT_ROOT" -c core.quotepath=false diff --cached --name-only --diff-filter=ACMRT 2>/dev/null)
GIT_RC=$?

# Fail-closed: git-plumbing failure (rc != 0) denies. Distinct from the legitimate
# empty-staged-set case (rc == 0, nothing staged -> the normal "nothing to commit"
# allow path below).
if [[ $GIT_RC -ne 0 ]]; then
    deny "PII-FREE-TRUNK: git-plumbing failure enumerating the staged set (git diff --cached rc=$GIT_RC). Failing closed — commit blocked."
fi

STAGED=()
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    STAGED+=("$f")
done <<< "$GIT_OUT"

# bd auto-stage coverage (eb1 + ycqo): the bd pre-commit git hook flushes pending
# bead text from .beads/beads.db AND stages .beads/issues.jsonl INSIDE `git
# commit`, AFTER the snapshot above. Two measures close that:
#   • flush-before-scan (ycqo): run `bd sync --flush-only` against the target repo
#     BEFORE the jsonl is read, so bead text still pending in the db at scan time
#     is materialized and scanned. DENY on flush failure — fail-closed, matching
#     this hook's git-rc/scan-rc convention and the bd hook's own exit-1-on-flush-
#     failure. Guarded on bd being invocable and the target repo carrying .beads/
#     (a non-beads clone commits without bd; the guard preserves clone semantics).
#     The flush precedes the -f check below because it may CREATE the jsonl.
#   • working-tree append (eb1): the bd file joins the trunk-wide scan set on
#     every commit (dedupe keeps the deny hit-count honest), BEFORE the empty-set
#     exit — a commit with nothing agent-staged still succeeds carrying bd's
#     auto-staged flush, so the scan must run on the bd file alone. The single -f
#     guard avoids leaning on the scanner's OSError swallow (the PR#84 BUG-1
#     fail-open trap class). .beads/ is not a data-bearing prefix — the operator
#     name in bead text is accepted authorship — so the file gets the trunk-wide
#     scope only (structural patterns + contact tokens via scan_scoped).
BD_ISSUES=".beads/issues.jsonl"
BD_CMD="${BLOCK_PII_COMMIT_BD_CMD:-bd}"
if command -v "$BD_CMD" >/dev/null 2>&1 && [[ -d "$PROJECT_ROOT/.beads" ]]; then
    BD_FLUSH_OUT=$( (cd "$PROJECT_ROOT" && "$BD_CMD" sync --flush-only) 2>&1 )
    BD_FLUSH_RC=$?
    if [[ $BD_FLUSH_RC -ne 0 ]]; then
        deny "PII-FREE-TRUNK: bd flush-before-scan failed (bd sync --flush-only rc=$BD_FLUSH_RC) — bead text pending in .beads/beads.db cannot be scanned. Failing closed — commit blocked. Detail: ${BD_FLUSH_OUT:-no output}"
    fi
fi
if [[ -f "$PROJECT_ROOT/$BD_ISSUES" ]]; then
    BD_SEEN=0
    for f in ${STAGED[@]+"${STAGED[@]}"}; do
        [[ "$f" == "$BD_ISSUES" ]] && { BD_SEEN=1; break; }
    done
    [[ $BD_SEEN -eq 0 ]] && STAGED+=("$BD_ISSUES")
fi

[[ ${#STAGED[@]} -eq 0 ]] && exit 0

# Partition the staged set into the data-bearing subset (for the identity scan).
DATA_BEARING=()
for f in "${STAGED[@]}"; do
    for p in "${DATA_BEARING_PREFIXES[@]}"; do
        case "$f" in "$p"*) DATA_BEARING+=("$f"); break ;; esac
    done
done

# ── Condition 1: staged filled-scaffold value (path/membership check) ──────────
for f in "${STAGED[@]}"; do
    case "$f" in
        "$SCAFFOLD_PREFIX"*)
            deny "PII-FREE-TRUNK: staged filled-scaffold value '$f' must not be committed (it carries operator data; it belongs only in the gitignored '$SCAFFOLD_PREFIX'). Unstage it: 'git rm --cached $f'." ;;
    esac
done

# ── Condition 2: staged vault/store/ file (path/membership check) ──────────────
for f in "${STAGED[@]}"; do
    case "$f" in
        "$STORE_PREFIX"*)
            deny "PII-FREE-TRUNK: staged store file '$f' must not be committed ('$STORE_PREFIX' is gitignored operator-data; it stays untracked). Unstage it: 'git rm --cached $f'." ;;
    esac
done

# ── Condition 3: tracked-file PII token — delegated to pii_scan.scan_scoped ─────
# ONE call to the SINGLE-SOURCED scope policy (pii_scan.scan_scoped — shared with
# the pre-push backstop so the gate and its backstop cannot drift; PR#84 QUAL-1).
# The full staged set and the data-bearing subset are passed on argv; scan does
# NOT re-enumerate (TOCTOU-closing capture). The scanner is imported from
# PII_SCAN_ROOT (sys.path-prepended), so a test stub deterministically flips the
# verdict (SEC-01(b)). stdout = hit count; stderr carries `PII-HIT: <path>` lines.
SCAN_ERR_FILE=$(mktemp)
SCAN_OUT=$(
    cd "$PROJECT_ROOT" && \
    BPC_SCAN_ROOT="$PII_SCAN_ROOT" \
    python3 - "${#STAGED[@]}" "${STAGED[@]}" ${DATA_BEARING[@]+"${DATA_BEARING[@]}"} <<'PY' 2>"$SCAN_ERR_FILE"
import os
import sys

sys.path.insert(0, os.environ["BPC_SCAN_ROOT"])
from scripts.guard.pii_scan import scan_scoped

n_staged = int(sys.argv[1])
staged = sys.argv[2:2 + n_staged]
data_bearing = sys.argv[2 + n_staged:]

print(scan_scoped(staged, data_bearing))
PY
)
SCAN_RC=$?
SCAN_ERR=$(cat "$SCAN_ERR_FILE" 2>/dev/null)
rm -f "$SCAN_ERR_FILE"

# Fail-closed: any scan-path error denies (default-deny at the scan boundary).
if [[ $SCAN_RC -ne 0 ]] || ! [[ "$SCAN_OUT" =~ ^[0-9]+$ ]]; then
    deny "PII-FREE-TRUNK: content-scan failed (pii_scan.scan errored, rc=$SCAN_RC). Failing closed — commit blocked. Detail: ${SCAN_ERR:-no stderr}"
fi

if [[ "$SCAN_OUT" -ge 1 ]]; then
    OFFENDERS=$(echo "$SCAN_ERR" | grep '^PII-HIT: ' | sed 's/^PII-HIT: //' | sort -u | head -8)
    # bd-aware remedy (PR#100 F4): the bd file is flush-managed — "unstage it"
    # is not workable (it joins the scan set unstaged, and a direct jsonl edit
    # is overwritten by the next flush), so point at the bd-native fix.
    REMEDY="Remove the PII or unstage the file before committing."
    if grep -qxF "$BD_ISSUES" <<< "$OFFENDERS"; then
        REMEDY="For $BD_ISSUES: edit the offending bead text via 'bd update', then 'bd sync --flush-only' (a direct edit of the jsonl is overwritten by the next flush). For any other offending file: remove the PII or unstage it before committing."
    fi
    deny "PII-FREE-TRUNK: staged file(s) carry operator PII (pii_scan reported $SCAN_OUT hit(s)). Offending file(s):
$OFFENDERS
$REMEDY"
fi

# No condition blocked and no scan error → allow.
exit 0
