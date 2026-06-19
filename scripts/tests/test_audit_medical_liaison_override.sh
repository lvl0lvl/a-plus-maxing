#!/usr/bin/env bash
# test_audit_medical_liaison_override.sh — negative tests for the mdv override gate.
#
# Anti-tautological by construction (F-007): the GOOD fixtures are content-valid
# adjudication envelopes that genuinely PASS, and each BAD fixture violates exactly ONE
# rule so its FAIL is attributable. Proves the gate goes RED on a bad override record —
# a vacuous operator_reason, a missing canonical literal, a sub-band evidence rung, and
# (the non-overridable invariant) an override path on a CRITICAL / H1 finding.
#
# Cases:
#   good_high / good_medium       valid override at the band rung           → exit 0
#   good_autoblock                CRITICAL, no override, auto-block sentinel → exit 0
#   good_block_stands             HIGH, no override (operator has not yet)   → exit 0
#   bad_vacuous                   "because I want to try it" at HIGH         → exit 1 (schema)
#   bad_no_literal                override_literal not canonical            → exit 1 (schema)
#   bad_rung                      HIGH with a clear-choice rung              → exit 1 (schema)
#   bad_critical_override         CRITICAL carrying an override path         → exit 1 (non-overridable)
#   bad_h1_override               H1 carrying an override path               → exit 1 (non-overridable)
#   bad_autoblock_setby           CRITICAL null override, set_by=liaison     → exit 1 (non-overridable)
#   no-arg / missing-file         usage / could-not-run                     → exit 2

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AUDIT="$REPO_ROOT/scripts/audit-medical-liaison-override.sh"
PY="$REPO_ROOT/.venv/bin/python"; [ -x "$PY" ] || PY="$(command -v python3)"
FIX="$(mktemp -d)"; trap 'rm -rf "$FIX"' EXIT

# Build all fixtures via python (DRY + correct 10-field records). The factories mirror
# scripts/plan/adjudicate.py's contract, NOT its implementation, so the gate is not
# graded against its own output.
"$PY" - "$FIX" <<'PY'
import json, sys
fix = sys.argv[1]
LIT = "operator is overriding a safety block"
CAUTION = "Supplement<->peptide additive adverse-event risk (shared additive-AE classes: bleeding-risk)"

def record(band="HIGH", **ov):
    rung = "understanding+appreciation+reasoning" if band == "HIGH" else "clear-choice"
    r = {
        "caution_verbatim": CAUTION,
        "composite_band": band,
        "risks_communicated": {
            "general": "additive antiplatelet effect raises bleeding risk",
            "risks_of_proceeding": "may cause prolonged bleeding or hemorrhage not offset by home monitoring",
        },
        "operator_reason": "recovering a connective-tissue injury under physician follow-up; accepting the monitored bleeding-risk tradeoff",
        "evidence_tier_required": rung,
        "evidence_provided": {"rung": rung},
        "override_literal": LIT,
        "voluntariness_note": "chosen without coercion after the risks were explained",
        "timestamp": "2026-06-19T10:00:00-04:00",
        "contradictions_log_ref": "vault/meta/contradictions.md#C-088",
    }
    r.update(ov)
    return r

def env(band="HIGH", harm=None, override="auto", set_by="auto"):
    non_ov = band == "CRITICAL" or harm in ("H1", "H2")
    rec = (None if non_ov else record(band)) if override == "auto" else override
    if set_by == "auto":
        set_by = "mechanical-auto-block-per-R3" if non_ov else "medical-liaison"
    return {
        "finding_id": "additive-ae:class:bleeding-risk", "composite_band": band, "harm_class": harm,
        "verdict": "BLOCK_WITH_OVERRIDE_PATH",
        "severity_final": {"set_by": set_by, "verdict": "BLOCK_WITH_OVERRIDE_PATH"},
        "override_record": rec,
    }

def w(name, obj):
    with open(f"{fix}/{name}.json", "w") as h:
        json.dump(obj, h)

w("good_high", env("HIGH"))
w("good_medium", env("MEDIUM"))
w("good_autoblock", env("CRITICAL"))
w("good_block_stands", env("HIGH", override=None, set_by="medical-liaison"))
w("bad_vacuous", env("HIGH", override=record("HIGH", operator_reason="because I want to try it")))
w("bad_no_literal", env("HIGH", override=record("HIGH", override_literal="I accept this")))
w("bad_rung", env("HIGH", override=record("HIGH", evidence_provided={"rung": "clear-choice"})))
w("bad_critical_override", env("CRITICAL", override=record("HIGH"), set_by="medical-liaison"))
w("bad_h1_override", env("HIGH", harm="H1", override=record("HIGH"), set_by="medical-liaison"))
w("bad_autoblock_setby", env("CRITICAL", set_by="medical-liaison"))
PY

PASS=0; FAIL=0
ok()  { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

expect() { # <fixture> <expected-rc> <label>
    bash "$AUDIT" "$FIX/$1.json" >/dev/null 2>&1; local rc=$?
    if [ "$rc" -eq "$2" ]; then ok "$3 (rc=$rc)"; else bad "$3 (expected $2, got $rc)"; fi
}

expect good_high            0 "valid HIGH override -> sound"
expect good_medium          0 "valid MEDIUM override -> sound"
expect good_autoblock       0 "CRITICAL auto-block -> sound"
expect good_block_stands    0 "HIGH no-override (block stands) -> sound"
expect bad_vacuous          1 "vacuous operator_reason -> RED (schema)"
expect bad_no_literal       1 "missing canonical literal -> RED (schema)"
expect bad_rung             1 "evidence rung below band -> RED (schema)"
expect bad_critical_override 1 "CRITICAL override path -> RED (non-overridable)"
expect bad_h1_override      1 "H1 override path -> RED (non-overridable)"
expect bad_autoblock_setby  1 "CRITICAL wrong set_by -> RED (non-overridable)"

bash "$AUDIT" >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 2 ]; then ok "no-arg -> exit 2"; else bad "no-arg -> exit 2 (got $rc)"; fi
bash "$AUDIT" "$FIX/nonexist.json" >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 2 ]; then ok "missing file -> exit 2"; else bad "missing file -> exit 2 (got $rc)"; fi

echo "test_audit_medical_liaison_override: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
