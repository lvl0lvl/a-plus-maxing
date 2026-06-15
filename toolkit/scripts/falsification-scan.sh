#!/usr/bin/env bash
# toolkit/scripts/falsification-scan.sh
#
# WHAT IT ENFORCES
#   Scans a process-failure (PF) log entry or an evidence-close note for the four
#   falsification anti-patterns named by the Rigor Framework's Failure-Mode
#   Discipline. These are the failure modes by which a project launders "no/weak
#   evidence" into "the rule re-confirmed," inflating confidence in a probabilistic
#   claim. See CDM-8-10 (Canonical Discipline Map) and its source,
#   extract-failure-discipline.md §3 "Falsification Discipline → Anti-patterns to
#   scan for":
#       - framework-circularity        : the rule defines what counts as evidence
#                                         for the rule (taxonomy-filtered admission).
#       - a-priori-by-construction      : the data point was picked *because* it was
#                                         expected to match (no pre-registration).
#       - increment-by-default          : every clean run advances n. Wrong — only
#                                         Category 1 (CLEAN + new region) advances n.
#       - soft-confirmation-laundering  : a HALT recorded as "the rule did not fail"
#                                         rather than "no evidence produced."
#
# SOURCE LINEAGE
#   NEW — framework-authored (CDM-8-10 / extract-failure-discipline §3). No project
#   shipped a script for this; it is a convergent-absence build. The three
#   session-close categories (1 CLEAN+new / 2 CLEAN+repro / 3 HALT) and the four
#   anti-patterns are taken verbatim from the extract.
#
# ADVISORY, NOT FAIL (design note)
#   Every hit is a WARN, never a fail()/violation. These are heuristic,
#   natural-language pattern matches over prose — high recall, imperfect precision.
#   A hard FAIL on a regex hit over English would false-positive on legitimate notes
#   that *quote* an anti-pattern in order to refute it ("this is NOT increment-by-
#   default because..."), and would make the gate something operators route around.
#   The discipline this enforces is a *human judgement* ("name the category
#   explicitly"); a script can flag the smell but cannot adjudicate the claim. So:
#   hits are surfaced as advisory WARNs for the operator/reviewer to confirm or
#   dismiss. The script therefore normally exits 0 (PASS) even with WARNs.
#
#   The ONE structural exception is the increment-by-default *negative test*
#   contract (Requirement: "a note exhibiting 'every clean run advances n' must be
#   flagged"). To make that assertable as a non-zero exit (the test harness asserts
#   bad-input goes RED), pass --strict: in strict mode any WARN is promoted to a
#   fail() so the bad fixture exits 1. Default (advisory) mode keeps WARNs non-
#   gating. This keeps the everyday gate non-blocking while giving the negative
#   test a real RED to assert against.
#
# BUG-N notes carried forward: none yet (new build). Annotate future real defects
#   at the fix site as `# BUG-N (context): ...` per CDM-5-10 / audit-helpers.sh.
#
# USAGE
#   falsification-scan.sh [--strict] [--allow-skip] [FILE]
#   FALSIFICATION_NOTE=path falsification-scan.sh        # env alternative
#   cat note.md | falsification-scan.sh                  # stdin
#
# EXIT (via verdict): 0 PASS / 1 FAIL (strict + hit, or fatal-as-fail) / 2 FATAL.

set -u

AUDIT_TAG="falsification-scan"
source "$(dirname "$0")/../lib/audit-helpers.sh"

STRICT=0
NOTE="${FALSIFICATION_NOTE:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --strict)      STRICT=1 ;;
    --allow-skip)  AUDIT_ALLOW_SKIP=1 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    --) shift; [ $# -gt 0 ] && NOTE="$1"; break ;;
    -*) emit "FATAL: unknown option '$1'"; exit 2 ;;
    *)  NOTE="$1" ;;
  esac
  shift
done

# Resolve input: FILE arg/env, else stdin (if piped).
SRC=""
if [ -n "$NOTE" ]; then
  if [ ! -r "$NOTE" ]; then
    emit "FATAL: note file not readable: $NOTE"
    exit 2
  fi
  SRC="$NOTE"
elif [ ! -t 0 ]; then
  SRC="$(mktemp 2>/dev/null || echo /tmp/fscan.$$)"
  cat > "$SRC"
  trap 'rm -f "$SRC"' EXIT
else
  # No input at all. A scan that cannot see a note has not verified anything:
  # fail-closed via skipped() (F-008) — exit 2 unless --allow-skip.
  skipped "no note provided (pass FILE, FALSIFICATION_NOTE=, or pipe on stdin)"
  verdict
fi

if [ ! -s "$SRC" ]; then
  skipped "note is empty: $SRC"
  verdict
fi

# Portable, case-insensitive prose match (BSD+GNU grep both honor -i -E).
# Returns 0 if pattern present.
hits() { grep -iE "$1" "$SRC" >/dev/null 2>&1; }

# flag — advisory WARN; promote to fail() only under --strict so the negative
# test can assert a non-zero exit.
flag() {
  local label="$1" detail="$2"
  warn "$label — $detail"
  if [ "$STRICT" = "1" ]; then
    fail "$label (strict: advisory flag promoted to violation)"
  fi
}

found_any=0

# --- 1. increment-by-default -------------------------------------------------
# "every clean run advances n" / always increment / n always goes up regardless
# of region. This is the contract negative-test case and must be caught.
if hits 'every[ -]+clean[ -]+(run|result|pass)[s]?[^.]*(advance|increment|bump|raise)[^.]*\bn\b' \
   || hits '(always|every time|each time)[^.]*(increment|advance|bump)[^.]*\bn\b' \
   || hits '\bn\b[^.]*(always|every clean)[^.]*(advance|increment|\+\+|\+ ?1)'; then
  flag "increment-by-default" \
       "note advances n on every clean run; only Category 1 (CLEAN+new region) may increment n (extract §3)"
  found_any=1
fi

# --- 2. framework-circularity ------------------------------------------------
# evidence admitted only because the rule's own taxonomy filtered it in.
if hits '(rule|framework|taxonomy|criteria)[^.]*(defines|determines|decides|filters)[^.]*(what counts as|which data|the evidence|admissib)' \
   || hits 'evidence[^.]*(because|since)[^.]*(rule|taxonomy|framework)[^.]*(classified|filtered|admitted|qualifies)' \
   || hits 'circular(ity)?'; then
  flag "framework-circularity" \
       "evidence may be admissible only because the rule's own taxonomy filtered it in; such data cannot falsify the rule (extract §3)"
  found_any=1
fi

# --- 3. a-priori-by-construction ---------------------------------------------
# data point selected *because* expected to match; no pre-registration.
if hits '(selected|chose|picked|cherry[- ]?picked)[^.]*(because|since)[^.]*(expect|likely|known)[^.]*(match|confirm|pass|hold)' \
   || hits 'by[- ]?construction' \
   || hits '(no|without)[^.]*(pre[- ]?regist|prediction registered|registered prediction)' \
   || hits 'expected[^.]*(to match|to confirm|to pass)[^.]*(so|therefore|hence)'; then
  flag "a-priori-by-construction" \
       "data point may have been selected because it was expected to match; pre-register predictions before running (extract §3)"
  found_any=1
fi

# --- 4. soft-confirmation-laundering -----------------------------------------
# a HALT / no-evidence run recorded as "the rule did not fail" / re-confirmed.
if hits 'halt[^.]*(did not fail|didn.?t fail|still holds|re[- ]?confirm|confirm)' \
   || hits '(no evidence|did not produce evidence|no data)[^.]*(did not fail|still holds|confirm|holds)' \
   || hits '(rule did not fail|did not fail.*so.*confirm|count(s|ed)? as (a )?confirmation)'; then
  flag "soft-confirmation-laundering" \
       "a HALT / no-evidence run may be recorded as 'the rule did not fail' instead of 'no evidence produced'; HALTs are HALTs (extract §3)"
  found_any=1
fi

if [ "$found_any" = "0" ]; then
  emit "no falsification anti-pattern heuristics matched"
fi

verdict
