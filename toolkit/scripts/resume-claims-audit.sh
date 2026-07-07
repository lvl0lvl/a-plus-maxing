#!/usr/bin/env bash
# toolkit/scripts/resume-claims-audit.sh — verify a continuity doc's RESUME claims
# against tracker/git reality (bead thm; improvements plan item 2).
#
# rotation-stamp-audit checks continuity-doc SHAPE; nothing checked its CLAIMS. A
# RESUME saying "next is bead X" when X closed last week, or "main @ <sha>" three
# merges ago, passed every gate — and did, on the framework's first consumer, where
# a session opened on a resume that queued two already-landed items. This audit
# reads ONLY the VOLATILE region(s) (same heading regex as rotation-stamp-audit:
# any `#+ ... VOLATILE ...` heading, to the next same-or-shallower heading) and
# verifies the machine-parseable claim classes below. Prose outside the region is
# historical and exempt.
#
# USAGE:  resume-claims-audit.sh <doc> [--beads-dir <dir>] [--heartbeat-limit <K>]
#   env RESUME_AUDIT_BD — bd binary override (tests stub it; the PEN_LINT_BD model)
#
# CLAIM GRAMMAR (the convention HANDOFF authors write against). Off-grammar prose
# is OUT OF SCOPE by design and mostly INVISIBLE to this audit — the coverage line
# surfaces only backticked bead tokens that matched no class and near-miss trunk
# phrasings. A claim you want verified must be written in grammar; a claim written
# off-grammar is neither verified nor guessed at:
#   class 1  bead status — a backticked bead token `<project>-<id>` in the same
#            SENTENCE (period- or line-delimited) as a status keyword
#            (closed|done = closed-class; open|in_progress|blocked|ready =
#            open-class; case-insensitive). Sentences end at a period followed by
#            whitespace, or at line end (version numbers do not split). Verified via
#            `bd show <id> --json` status: closed-class keywords (closed|done)
#            must match status=closed; open-class keywords must match a
#            non-closed status. A token bd cannot find is a FAIL — a claim about
#            a nonexistent bead is a false claim, not an infrastructure error.
#   class 2  trunk position — `main|master|trunk @ <sha>` (7-40 lowercase hex,
#            backticks optional; verified against the doc repo's resolved trunk).
#            FAIL off-trunk; WARN when the trunk has moved past it. Near-miss
#            trunk phrasings (wrong case/spacing) surface in unparsed coverage.
#   class 3  landed PR — `#<N>` in the same sentence as landed|merged. Verified
#            against squash SUBJECTS ENDING in "(#N)" on the trunk (a commit
#            merely mentioning (#N) does not verify a landing).
#   class 4  heartbeat — WARN when more than K commits (default 10) postdate the
#            region's `Stamped YYYY-MM-DD` line (preferred anchor; falls back to
#            the newest date in the region): the resume predates too much history
#            to be trusted un-rotated. One bead claim per sentence — multi-token
#            sentences are ambiguous and count as unparsed.
#
# OUTPUT: one `coverage: parsed=<n> unparsed=<m>` line (unparsed counts
# bead-shaped tokens in the region no class grammar matched — visible, not
# gated). Zero parsed claims in a non-empty region → PASS-VACUOUS WARN (a
# claim-free resume must not read as verified).
#
# EXIT (0/1/2 house convention):
#   0 PASS — including the loud SKIP on a doc with no VOLATILE region (an
#     un-adopted doc is not a failure; adoption is per-doc) and PASS-VACUOUS.
#     The plan's "malformed region → FATAL" clause is discharged by
#     unreachability: the fence-aware awk scoper is total (any present heading
#     yields a well-defined region), so no malformed state is constructible.
#   1 FAIL — at least one claim contradicts tracker/git reality.
#   2 FATAL — the audit could not run: doc missing/unreadable, or `.beads/`
#     present but bd unresolvable (a tracker that exists but cannot be read
#     must not silently skip class 1 — F-008).
set -uo pipefail

fail_count=0 warn_count=0 parsed=0 unparsed=0
emit()  { echo "[resume-claims-audit] $1"; }
fail()  { emit "FAIL: $1"; fail_count=$((fail_count+1)); }
warn()  { emit "WARN: $1"; warn_count=$((warn_count+1)); }
fatal() { emit "FATAL: $1 (audit could not run — F-008)" >&2; exit 2; }

DOC="${1:-}"
shift || true
BEADS_DIR="" HEARTBEAT_LIMIT=10
while [ $# -gt 0 ]; do
  case "$1" in
    --beads-dir)        [ $# -ge 2 ] || fatal "$1 requires a value"
                        BEADS_DIR="$2"; shift 2 ;;
    --heartbeat-limit)  [ $# -ge 2 ] || fatal "$1 requires a value"
                        HEARTBEAT_LIMIT="$2"; shift 2 ;;
    *) fatal "unknown argument '$1'" ;;
  esac
done

[ -n "$DOC" ] || fatal "no document argument"
[ -f "$DOC" ] && [ -r "$DOC" ] || fatal "document '$DOC' missing or unreadable"

DOC_DIR="$(cd "$(dirname "$DOC")" && pwd)"
REPO_ROOT="$(git -C "$DOC_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
TRUNK=""
if [ -n "$REPO_ROOT" ]; then
  TRUNK="$(git -C "$REPO_ROOT" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')"
  if [ -z "$TRUNK" ]; then
    for c in main master trunk; do
      git -C "$REPO_ROOT" rev-parse --verify -q "$c" >/dev/null 2>&1 && { TRUNK="$c"; break; }
    done
  fi
fi
# classes 2-4 verify against the trunk; a doc outside a git repo skips them LOUDLY
# (a silent skip reads as verified — the exact failure this audit exists to kill)

# --- extract the VOLATILE region(s): same heading regex as rotation-stamp-audit, ----
# --- fence-aware (a ```-fenced example heading must not open a phantom region) ------
REGION="$(awk '
  /^```/ { fence = !fence; next }
  fence { next }
  /^#+[ \t].*VOLATILE/ { inr=1; lvl=length($1); next }
  inr && /^#+[ \t]/ { if (length($1) <= lvl) { inr=0 } else { print; next } }
  inr { print }
' "$DOC")"
HEADING_PRESENT="$(awk '
  /^```/ { fence = !fence; next }
  fence { next }
  /^#+[ \t].*VOLATILE/ { print "Y"; exit }
' "$DOC")"

if [ -z "$HEADING_PRESENT" ]; then
  emit "SKIP: no VOLATILE region in $DOC (doc not yet adopted; adoption is per-doc)"
  emit "coverage: parsed=0 unparsed=0 region=absent"
  exit 0
fi
if [ -z "$(printf '%s' "$REGION" | tr -d '[:space:]')" ]; then
  # adopted but EMPTIED is not un-adopted — it flows to PASS-VACUOUS below, never SKIP
  warn "VOLATILE region is present but EMPTY — an emptied resume is not an un-adopted doc"
  REGION=" "
fi

# --- resolve bd + the beads dir (class 1) ---------------------------------------------
BD="${RESUME_AUDIT_BD:-}"
[ -n "$BD" ] || BD="$(command -v bd || true)"
if [ -z "$BEADS_DIR" ]; then
  d="$DOC_DIR"
  while [ "$d" != "/" ]; do
    [ -d "$d/.beads" ] && { BEADS_DIR="$d/.beads"; break; }
    d="$(dirname "$d")"
  done
fi
[ -n "$REPO_ROOT" ] || emit "SKIP: doc is not inside a git repo — trunk claims (classes 2-4) not checked"

CLASS1=1
if [ -n "$BEADS_DIR" ] && [ -d "$BEADS_DIR" ]; then
  { [ -n "$BD" ] && [ -x "$BD" ]; } || fatal ".beads present at $BEADS_DIR but bd is unresolvable (set RESUME_AUDIT_BD)"
else
  emit "SKIP: no .beads directory found — bead-status claims (class 1) not checked"
  CLASS1=0
fi

# --- walk the region sentence-by-sentence ---------------------------------------------
BEAD_TOKEN_RE='`[a-z0-9][a-z0-9_-]*-[a-z0-9]{2,5}`'
# ONE vocabulary, two classes; the gate set is their union (grep -i covers case)
CLOSED_KW='closed|done'
OPEN_KW='open|in_progress|blocked|ready'   # no `next`: section vocabulary, not status
STATUS_KW_RE="(${CLOSED_KW}|${OPEN_KW})"

# sentences: split on period-followed-by-whitespace or line end — a bare-period
# split would fragment version numbers ("rigor 1.17.0") away from their claim's
# keyword and silently demote real claims to unparsed
SENTENCES="$(printf '%s\n' "$REGION" | sed -E $'s/\\.[ \t]/\\\n/g')"

declare -a SEEN_TOKENS=()
TRUNK_SUBJECTS=""
BD_CACHE="" bd_calls=0 BD_CALL_LIMIT="${RESUME_AUDIT_BD_LIMIT:-100}" BD_LIMIT_HIT=0
while IFS= read -r s; do
  [ -n "$s" ] || continue

  # class 1 — bead-status claims. The keyword test runs on TOKEN-STRIPPED text: a
  # bead id whose suffix is itself a status word (`proj-done`) must not supply its
  # own claim (executed false-FAIL in review). One bead claim per sentence: a
  # sentence with MULTIPLE tokens and one keyword is ambiguous binding — skipped,
  # surfacing in the coverage line's unparsed count (the SEEN_TOKENS subtraction).
  if printf '%s\n' "$s" | grep -qE "$BEAD_TOKEN_RE"; then
    s_nok="$(printf '%s\n' "$s" | sed -E "s/$BEAD_TOKEN_RE//g")"
    ntok="$(printf '%s\n' "$s" | grep -oE "$BEAD_TOKEN_RE" | sort -u | wc -l | tr -d ' ')"
    if printf '%s\n' "$s_nok" | grep -qwiE "$STATUS_KW_RE" && [ "$ntok" = 1 ]; then
    kw_closed=0
    printf '%s\n' "$s_nok" | grep -qwiE "($CLOSED_KW)" && kw_closed=1
    kw_open=0
    printf '%s\n' "$s_nok" | grep -qwiE "($OPEN_KW)" && kw_open=1
    while IFS= read -r tok; do
      id="${tok#\`}"; id="${id%\`}"
      if [ "$CLASS1" = 0 ]; then continue; fi   # unverified -> counts as unparsed below
      if [ "$kw_closed" = 1 ] && [ "$kw_open" = 1 ]; then
        continue   # mixed-class keywords — ambiguous, lands in unparsed
      fi
      SEEN_TOKENS+=("$id")
      # one bd call per unique id, hard-bounded: a crafted or enormous doc must not
      # amplify into thousands of process spawns at a close gate (executed DoS in
      # review: 20k tokens -> 18k bd calls)
      case "$BD_CACHE" in
        *"|$id="*) status="${BD_CACHE#*"|$id="}"; status="${status%%|*}" ;;
        *)
          if [ "$bd_calls" -ge "$BD_CALL_LIMIT" ]; then
            [ "$BD_LIMIT_HIT" = 0 ] && warn "bd call limit ($BD_CALL_LIMIT unique ids) reached — remaining bead claims unverified (counted unparsed)"
            BD_LIMIT_HIT=1
            SEEN_TOKENS=("${SEEN_TOKENS[@]:0:$((${#SEEN_TOKENS[@]}-1))}")
            continue
          fi
          bd_calls=$((bd_calls+1))
          json="$("$BD" show "$id" --json 2>/dev/null)" || json=""
          status="$(printf '%s' "$json" | grep -oE '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')"
          BD_CACHE="${BD_CACHE}|$id=${status}|"
          ;;
      esac
      if [ -z "$status" ]; then
        fail "bead \`$id\` claimed in the RESUME but bd cannot find it (a claim about a nonexistent bead is a false claim)"
        parsed=$((parsed+1)); continue
      fi
      if [ "$kw_closed" = 1 ]; then
        [ "$status" = "closed" ] || fail "bead \`$id\` claimed closed/done but bd status is '$status'"
      else
        [ "$status" != "closed" ] || fail "bead \`$id\` claimed open-class but bd status is 'closed'"
      fi
      parsed=$((parsed+1))
    done < <(printf '%s\n' "$s" | grep -oE "$BEAD_TOKEN_RE")
    fi
  fi

  # class 3 — landed/merged PR claims
  if printf '%s\n' "$s" | grep -qwiE '(landed|merged)'; then
    while IFS= read -r pr; do
      n="${pr#\#}"
      if [ -n "$REPO_ROOT" ] && [ -n "$TRUNK" ]; then
        # subject-END anchor: a commit merely MENTIONING (#N) must not verify a
        # landing (executed false-PASS in review); squash subjects end with (#N).
        # Herestring, NOT a pipe: `git | grep -q` under pipefail turns grep's
        # early exit into git's SIGPIPE 141 on long histories — a TRUE claim
        # false-FAILed on the real repo while the short-history fixture passed.
        [ -n "$TRUNK_SUBJECTS" ] || TRUNK_SUBJECTS="$(git -C "$REPO_ROOT" log --format=%s "$TRUNK" 2>/dev/null)"
        if grep -qE "\(#${n}\)\$" <<< "$TRUNK_SUBJECTS"; then :; else
          fail "PR #$n claimed landed/merged but no squash subject ending \"(#$n)\" is on $TRUNK"
        fi
        parsed=$((parsed+1))
      fi
    done < <(printf '%s\n' "$s" | grep -oE '#[0-9]+')
  fi
done <<< "$SENTENCES"

# class 2 — trunk-position claims (line-scoped; `main|master|trunk @ <sha>`)
TRUNK_CLAIM_RE='(main|master|trunk) @ `?[0-9a-f]{7,40}`?'
while IFS= read -r sha; do
  [ -n "$sha" ] || continue
  if [ -z "$REPO_ROOT" ] || [ -z "$TRUNK" ]; then continue; fi
  parsed=$((parsed+1))
  if ! git -C "$REPO_ROOT" cat-file -e "${sha}^{commit}" 2>/dev/null; then
    fail "trunk claim '@ $sha' — no such commit"
  elif ! git -C "$REPO_ROOT" merge-base --is-ancestor "$sha" "$TRUNK" 2>/dev/null; then
    fail "trunk claim '@ $sha' — commit is not on $TRUNK"
  elif [ "$(git -C "$REPO_ROOT" rev-parse "$TRUNK")" != "$(git -C "$REPO_ROOT" rev-parse "$sha")" ]; then
    warn "trunk claim '@ $sha' — $TRUNK has moved past it (stale but truthful; rotate)"
  fi
done < <(printf '%s\n' "$REGION" | grep -oE "$TRUNK_CLAIM_RE" | grep -oE '[0-9a-f]{7,40}')
# near-miss trunk claims (wrong case, no spaces, short sha) are VISIBLE, not vanished
loose="$(printf '%s\n' "$REGION" | grep -ciE '(main|master|trunk)[[:space:]]*@' || true)"
strict="$(printf '%s\n' "$REGION" | grep -cE "$TRUNK_CLAIM_RE" || true)"
[ "${loose:-0}" -gt "${strict:-0}" ] && unparsed=$((unparsed + loose - strict))

# class 4 — heartbeat: commits since the region's newest date stamp
if [ -n "$REPO_ROOT" ] && [ -n "$TRUNK" ]; then
  newest="$(printf '%s\n' "$REGION" | grep -oiE 'Stamped 20[0-9]{2}-[0-9]{2}-[0-9]{2}' | grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' | sort | tail -1)"
  [ -n "$newest" ] || newest="$(printf '%s\n' "$REGION" | grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' | sort | tail -1)"
  if [ -n "$newest" ]; then
    since_count="$(git -C "$REPO_ROOT" log --oneline "$TRUNK" --since="$newest 23:59" 2>/dev/null | wc -l | tr -d ' ')"
    if [ "$since_count" -gt "$HEARTBEAT_LIMIT" ]; then
      warn "heartbeat: $since_count commits on main postdate the region's newest stamp ($newest) — limit $HEARTBEAT_LIMIT; rotate the RESUME"
    fi
  fi
fi

# coverage — bead-shaped tokens in the region that no class-1 sentence matched
total_tokens="$(printf '%s\n' "$REGION" | grep -oE "$BEAD_TOKEN_RE" | sort -u | wc -l | tr -d ' ')"
matched_tokens="$(printf '%s\n' ${SEEN_TOKENS[@]+"${SEEN_TOKENS[@]}"} | sort -u | grep -c . || true)"
[ "$total_tokens" -ge "$matched_tokens" ] && unparsed=$((unparsed + total_tokens - matched_tokens))

emit "coverage: parsed=$parsed unparsed=$unparsed"
if [ "$unparsed" -gt 0 ] && [ "$parsed" -gt 0 ]; then
  warn "$unparsed bead-shaped token(s) in the region were NOT verified (ambiguous or off-grammar sentences) — a false claim can hide there; write one claim per sentence"
fi
if [ "$parsed" = 0 ]; then
  warn "PASS-VACUOUS: the VOLATILE region carries no parseable claims — nothing was verified; a claim-free resume is not a verified resume"
fi

if [ "$fail_count" -gt 0 ]; then
  emit "RESULT: FAIL ($fail_count claim(s) contradict reality; warns=$warn_count)"
  exit 1
fi
emit "RESULT: PASS (parsed=$parsed warns=$warn_count)"
exit 0
