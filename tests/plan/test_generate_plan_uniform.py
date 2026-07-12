"""Tests for the transitional additive DOMAIN-PROGRAM migration (ADR-0041-T2).

The four translators + `assemble._is_complete` migrate to the uniform seven-field DOMAIN
PROGRAM (`scripts/plan/domain_program.py`) via a TRANSITIONAL ADDITIVE ADAPTER: both the
legacy thin payload AND a full uniform program are valid during the migration. The adapter
lifts a legacy rec's `payload` into the program's `prescription` while the other six fields
ramp, bounded by `domain_program.validate` — a non-conformant program is REJECTED at the
collection boundary (the honest no-plan state), NEVER a silent thin fallback. The seven-field
program rides the FROZEN `record_plan` -> `store.append` ADDITIVELY (the `plan_schema`
open-on-extras seam), so the round-trip drops 0 of 7.

These tests pin (spec ADR-0041-T2 ACs):

  - AC-1 (PF-S130-01 LOAD-BEARING): a uniform program authored through the production path
    round-trips through `record_plan`/`read_plan` carrying all seven fields (0 dropped), for a
    training-kind AND a compound-kind domain, with the renderable shape recorded + the workout
    clearance gate preserved. NON-TAUTOLOGICAL: it REDs against the pre-migration tree (the thin
    translator drops the seven fields) — that RED IS the revert-REDs proof.
  - AC-2: the adapter accepts BOTH a full uniform program AND a legacy thin rec (lifted),
    0 conformant inputs rejected, parametrized across the four translators.
  - AC-3 (fail-closed, LOAD-BEARING): an OLD bespoke non-uniform, non-adapter-liftable shape
    yields `plan is None` (0 non-uniform outputs become a plan). RED-capable under a
    silent-thin-fallback mutation of `_is_complete`.
  - AC-4: the per-ADR-scoped freeze-break numstat — only `generate_plan.py` + `assemble.py`
    changed; the HARD-frozen four + the sibling-superseded surfaces are byte-untouched.
  - AC-5: the module passes offline against synthetic fixtures (0 live-API, 0 real PII, 0
    live-client import).

All fixtures are synthetic literals (no real operator PII); the author envelope rides the
captured-envelope (`_FixedEnvelopeClient`) seam that `compute_plan`/`generate_plan` wrap over
`author_output` — no live `ModelClient`, no live API, 0 spend.
"""

import functools
import subprocess
from pathlib import Path

import pytest

from scripts.plan import domain_program
from scripts.plan.generate_plan import compute_plan, generate_plan
from scripts.store import keying, plan_schema, store

PLAN_DATE = "2026-06-18"
REPO_ROOT = Path(__file__).resolve().parents[2]

# The rec-embedded / plan-attached uniform-program key (the migration's ride key). Held as a
# literal here so the module imports + collects cleanly on the PRE-migration tree (the AC-1
# revert-REDs proof runs the SAME test body against the un-migrated code).
PROGRAM_KEY = "domain_program"

# The task-entry HEAD the AC-4 per-ADR numstat probe diffs against (mirrors
# tests/plan/test_generate_plan.py:901's PRE_TASK_HEAD constant pattern). Recorded at
# ADR-0041-T2 entry on feature/comprehensive-plan-wave-2.
PRE_TASK_HEAD = "20e780fc0dcfa1a9ba155e22bd049cd52bcdd0cb"


# --- fixtures ------------------------------------------------------------------


def _seed_store(root, **overrides):
    """Seed PII-free operator-state items into a real temp store; return a bound reader.

    Backs the pass-through Summary Field-Set fields `assemble_context` reads (mirrors
    tests/plan/test_generate_plan.py's `_seed_store`). Returns a `store.read` pre-bound to
    `root` (the summarize caller contract).
    """
    fields = {
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
    }
    fields.update(overrides)
    for item, value in fields.items():
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": PLAN_DATE, "source": "intake", "value": value},
            root=root,
        )
    return functools.partial(store.read, root=root)


def _author(*recs, specialist="personal-trainer"):
    """A captured author envelope carrying `recs`."""
    return {"specialist": specialist, "recommendations": list(recs)}


def _uniform_program(prescription, kind, *, required_labs=None):
    """A conformant seven-field DOMAIN PROGRAM (`domain_program.validate` passes).

    `monitoring_signals` carries a VALIDITY_TIERS-member tier; a compound kind gets non-empty
    `required_labs` + non-empty autoregulation floors. Seeds fields the OLD thin path DROPS
    (`monitoring_signals` with a validity tier, `adjustment_rules`, the GRADE `rationale`,
    `cross_domain_seams`) — the AC-1 distinguishing content.
    """
    return {
        domain_program.PRESCRIPTION: prescription,
        domain_program.RATIONALE: {
            "certainty_of_evidence": "moderate",
            "strength_of_recommendation": "strong",
            "causal_marker": "associational",
        },
        domain_program.MONITORING_SIGNALS: [
            {"signal": "morning HRV", domain_program.SIGNAL_TIER_KEY: "moderate"},
        ],
        domain_program.ADJUSTMENT_RULES: [
            {"trigger": "HRV drop >1SD across 3 days", "action": "reduce volume 20%"},
        ],
        domain_program.REQUIRED_LABS: list(required_labs) if required_labs else [],
        domain_program.REFUSAL_ESCALATION: {"marker": "chest pain -> stop + clinician review"},
        domain_program.CROSS_DOMAIN_SEAMS: [
            {"paired_domain": "nutrition", "seam": "energy availability floor"},
        ],
        domain_program.KIND_FIELD: kind,
    }


def _workout_exercise(*, load="60% 1RM"):
    ex = {"name": "Goblet squat", "sets": 3, "reps": "8-12", "detail": "controlled tempo"}
    if load is not None:
        ex["load"] = load
    return ex


def _workout_uniform_rec():
    """A workout (training-kind) rec carrying a FULL uniform program + a legacy payload.

    The legacy `payload` (dropped by the migrated path, read by the pre-migration path)
    isolates the RED to the seven-field round-trip: the un-migrated translator renders the
    payload but drops the seven fields; the migrated translator renders the prescription AND
    rides the seven fields.
    """
    ex = _workout_exercise(load="60% 1RM")
    return {
        "claim": "rebuild a movement base with goblet squats before any loaded pattern",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        "payload": dict(ex),
        PROGRAM_KEY: _uniform_program(dict(ex), "training"),
    }


def _peptides_uniform_rec():
    """A peptides (compound-kind) rec carrying a FULL uniform program + a legacy payload."""
    regimen = {
        "compound": "BPC-157", "dose": "250 mcg", "route": "subcutaneous",
        "cycle_week": 1, "cycle_length_weeks": 4,
    }
    return {
        "claim": "run BPC-157 at 250 mcg subcutaneous for localized tissue support",
        "source": "vault/library/peptides/bpc-157 research-report 2026",
        "confidence_tier": "experimental",
        "reversibility": "reversible on discontinuation",
        "category": "peptide-therapy",
        "payload": dict(regimen),
        PROGRAM_KEY: _uniform_program(dict(regimen), "compound", required_labs=["CBC", "CMP"]),
    }


def _workout_legacy_rec():
    return {
        "claim": "rebuild a movement base with goblet squats",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        "payload": {"name": "Goblet squat", "sets": 3, "reps": "8-12"},
    }


def _nutrition_legacy_recs():
    target = {
        "claim": "set energy and protein at maintenance",
        "source": "ISSN position stand on protein and exercise 2017",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "nutrition",
        "payload": {"calorie_goal": 2400, "macros": {"protein": 180, "carbs": 240, "fat": 70}},
    }
    meal = {
        "claim": "distribute protein across the day with breakfast",
        "source": "ISSN position stand on protein and exercise 2017",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "nutrition",
        "payload": {"meal": {"name": "Breakfast"}},
    }
    return [target, meal]


def _supplement_legacy_rec():
    return {
        "claim": "supplement creatine monohydrate to close a documented gap",
        "source": "Examine.com creatine monograph 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "supplementation",
        "payload": {"name": "Creatine monohydrate", "dose": "5 g", "timing": "daily"},
    }


def _peptide_legacy_rec():
    return {
        "claim": "run BPC-157 at 250 mcg subcutaneous for localized tissue support",
        "source": "vault/library/peptides/bpc-157 research-report 2026",
        "confidence_tier": "experimental",
        "reversibility": "reversible on discontinuation",
        "category": "peptide-therapy",
        "payload": {"compound": "BPC-157", "dose": "250 mcg", "route": "subcutaneous"},
    }


# --- AC-1: uniform program round-trips through the production path (PF-S130-01) --


def test_uniform_program_round_trips_zero_fields_dropped(tmp_path):
    """AC-1 (LOAD-BEARING, PRODUCTION PATH): a uniform DOMAIN PROGRAM authored through the
    `generate_plan` -> `assemble` -> migrated translator -> `record_plan` -> `read_plan` path
    round-trips carrying all seven program fields (0 dropped), for a training-kind AND a
    compound-kind domain, with the renderable shape recorded + the workout clearance gate
    preserved.

    NON-TAUTOLOGICAL / revert-REDs (PF-S130-01): against the PRE-migration tree the thin
    translator drops the seven non-renderable fields, so `plan['domain_program']` is absent and
    this test REDs — that RED is the distinguishing proof the migration happened.
    """
    seven = domain_program.REQUIRED_FIELDS + domain_program.CONDITIONAL_FIELDS

    # training-kind domain (workout) — the clearance gate strips `load` (no clearance granted).
    root_w = tmp_path / "workout"
    store_read = _seed_store(root_w)
    result = generate_plan(
        "workout", _author(_workout_uniform_rec()), store_read, root_w, plan_date=PLAN_DATE,
    )
    assert result["recorded"] is True, "the uniform-program workout must record a plan"
    resolved = plan_schema.read_plan("workout", PLAN_DATE, root_w)
    plan = resolved["plan"]
    assert plan is not None, "the recorded workout plan must read back"
    program = plan.get(PROGRAM_KEY)
    assert program is not None, (
        "the seven-field DOMAIN PROGRAM must ride the frozen record path (0-of-7 dropped)"
    )
    assert [f for f in seven if f not in program] == [], (
        "all seven program fields must round-trip through record_plan/read_plan"
    )
    # the thin renderable shape still rendered (record_plan accepted it)
    assert [ex["name"] for ex in plan["exercises"]] == ["Goblet squat"]
    # the workout clearance gate is PRESERVED (a LOAD-BEARING safety gate)
    assert "load" not in plan["exercises"][0], "the clearance gate must strip load without clearance"
    # QA-T2-01 (SAFETY-ADJACENT): the clearance gate strips `load` from the STORE-BOUND program
    # prescription too — not only the renderable exercise. `program["prescription"]` rides
    # record_plan -> store.append into stored plan state (and ADR-0044 first-class storage), so an
    # un-cleared load must not survive there while the renderable assertion above stays green.
    assert "load" not in program[domain_program.PRESCRIPTION], (
        "the clearance gate must strip load from the store-bound program prescription too"
    )
    # QA-T2-02: the non-prescription ramped field VALUES round-trip byte-equal (the 0044-T1 AC-2
    # fidelity bar), not just the seven KEYS above — a migration emitting the keys with an
    # emptied/renamed sub-value would pass key-presence but fail here. Values are the
    # `_uniform_program` fixture's known literals.
    assert program[domain_program.MONITORING_SIGNALS] == [
        {"signal": "morning HRV", domain_program.SIGNAL_TIER_KEY: "moderate"}
    ], "monitoring_signals (with its validity tier) must round-trip value-intact"
    assert program[domain_program.ADJUSTMENT_RULES] == [
        {"trigger": "HRV drop >1SD across 3 days", "action": "reduce volume 20%"}
    ], "adjustment_rules must round-trip value-intact"
    assert program[domain_program.RATIONALE] == {
        "certainty_of_evidence": "moderate",
        "strength_of_recommendation": "strong",
        "causal_marker": "associational",
    }, "the GRADE rationale must round-trip value-intact"
    assert program[domain_program.CROSS_DOMAIN_SEAMS] == [
        {"paired_domain": "nutrition", "seam": "energy availability floor"}
    ], "cross_domain_seams must round-trip value-intact"
    assert program[domain_program.REQUIRED_LABS] == [], (
        "training required_labs must round-trip value-intact (empty-OK for a training kind)"
    )

    # compound-kind domain (peptides) — the seven fields ride the single-compound plan.
    root_p = tmp_path / "peptides"
    store_read_p = _seed_store(root_p)
    result_p = generate_plan(
        "peptides", _author(_peptides_uniform_rec(), specialist="peptide-specialist"),
        store_read_p, root_p, plan_date=PLAN_DATE,
    )
    assert result_p["recorded"] is True, "the uniform-program peptides must record a plan"
    resolved_p = plan_schema.read_plan("peptides", PLAN_DATE, root_p)
    plan_p = resolved_p["plan"]
    assert plan_p is not None
    program_p = plan_p.get(PROGRAM_KEY)
    assert program_p is not None, "the compound seven-field program must ride the record path"
    assert [f for f in seven if f not in program_p] == [], (
        "compound: all seven program fields must round-trip (0 dropped)"
    )
    # QA-T2-02 (compound): the ramped field VALUES round-trip byte-equal — required_labs is the
    # distinguishing compound value (mandatory-and-non-empty for a compound kind, ["CBC","CMP"] in
    # the fixture), plus a monitoring-signal validity tier, mirroring 0044-T1 AC-2's == bar.
    assert program_p[domain_program.REQUIRED_LABS] == ["CBC", "CMP"], (
        "compound required_labs must round-trip value-intact"
    )
    assert program_p[domain_program.MONITORING_SIGNALS] == [
        {"signal": "morning HRV", domain_program.SIGNAL_TIER_KEY: "moderate"}
    ], "compound: monitoring_signals must round-trip value-intact"
    assert plan_p["compound"] == "BPC-157", "the single-compound renderable regimen must record"


# --- AC-2: the transitional adapter accepts BOTH shapes (0 conformant rejected) -


def test_adapter_accepts_full_uniform_program(tmp_path):
    """AC-2 (uniform shape): a full uniform program flows through `compute_plan`/`assemble`
    and produces a plan (`plan is not None`, the program validates)."""
    store_read = _seed_store(tmp_path)
    rec = {
        "claim": "rebuild a movement base with goblet squats",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        PROGRAM_KEY: _uniform_program(_workout_exercise(load=None), "training"),
    }
    result = compute_plan(
        "workout", {"specialist": "personal-trainer", "recommendations": [rec]}, store_read,
    )
    assert result["plan"] is not None, "a full uniform program must be accepted (0 conformant rejected)"


@pytest.mark.parametrize(
    "domain, recs, specialist",
    [
        ("workout", [_workout_legacy_rec()], "personal-trainer"),
        ("nutrition", _nutrition_legacy_recs(), "nutritionist"),
        ("supplements", [_supplement_legacy_rec()], "supplement-specialist"),
        ("peptides", [_peptide_legacy_rec()], "peptide-specialist"),
    ],
)
def test_adapter_lifts_legacy_thin_payload(tmp_path, domain, recs, specialist):
    """AC-2 (legacy shape, QA-01): a CLEAN legacy thin rec (with the completeness metadata)
    ALWAYS lifts to a conformant program -> `plan is not None`, across ALL FOUR translators.

    The two compound params (supplements/peptides) ramp `required_labs` + autoregulation to
    non-empty transitional floors, so the lift SUCCEEDS (it does NOT fail closed — fail-closed
    is reserved for AC-3's genuinely-non-liftable bespoke shape). 0 conformant inputs rejected.
    """
    store_read = _seed_store(tmp_path)
    result = compute_plan(
        domain, {"specialist": specialist, "recommendations": recs}, store_read,
    )
    assert result["plan"] is not None, (
        f"{domain}: a clean legacy rec must lift to a conformant program (never fail closed)"
    )


# --- AC-3: non-liftable bespoke shape rejected at the collection boundary --------


def _bespoke_partial_program_rec():
    """A bespoke NON-uniform rec: a PARTIAL program (missing the required monitoring_signals +
    adjustment_rules) so `domain_program.validate` FAILS.

    It emits an explicit (partial) program, so it is NOT a liftable legacy thin rec (a rec that
    emits a program must be conformant — no ramp). It ALSO carries legacy metadata + a valid
    renderable payload, so a silent-thin-fallback (the anti-behavior) WOULD accept it — the
    distinguishing content that makes the AC-3 rejection non-tautological.
    """
    return {
        "claim": "rebuild a movement base with goblet squats",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        "payload": {"name": "Goblet squat", "sets": 3},
        PROGRAM_KEY: {
            domain_program.PRESCRIPTION: {"name": "Goblet squat", "sets": 3},
            domain_program.RATIONALE: {"certainty_of_evidence": "low"},
            domain_program.KIND_FIELD: "training",
            # missing MONITORING_SIGNALS + ADJUSTMENT_RULES -> validate raises -> non-conformant
        },
    }


def test_non_liftable_bespoke_shape_rejected_at_collection(tmp_path):
    """AC-3 (fail-closed, LOAD-BEARING, falsification #2): a bespoke non-uniform shape that is
    NOT adapter-liftable produces `plan is None` (the honest no-plan state) — 0 non-uniform
    outputs become a plan (so 0 reach `orchestrate.reconcile`).

    RED-capable via the SILENT-THIN-FALLBACK mutation (Step 1-continued): if `_is_complete` fell
    back to the thin accept on `domain_program.validate` failure, this partial-program rec would
    lift-render and yield a plan -> this test REDs.
    """
    store_read = _seed_store(tmp_path)
    result = compute_plan(
        "workout",
        {"specialist": "personal-trainer", "recommendations": [_bespoke_partial_program_rec()]},
        store_read,
    )
    assert result["plan"] is None, (
        "a non-liftable bespoke (partial-program) shape must fail closed — never a silent thin "
        "fallback (0 non-uniform outputs become a plan)"
    )
    assert result["reason"], "the honest no-plan reason must be set (coverage-gap / no-actionable)"


# --- AC-4: the per-ADR-scoped freeze-break numstat ------------------------------


def _numstat(base, *paths):
    """`git diff --numstat <base> -- <paths>` over the repo, stripped (mirror :978)."""
    out = subprocess.run(
        ["git", "diff", "--numstat", base, "--", *paths],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def test_per_adr_scoped_freeze_break_numstat():
    """AC-4: the supersession is BOUNDED to `generate_plan.py` + `assemble.py`; the HARD-frozen
    four + the sibling-superseded surfaces (0043 `orchestrate.py`, 0042 `router.py`) are
    byte-untouched in THIS commit, and the `<always-frozen>` set is EMPTY over the whole build
    (`origin/main` base).

    0044 `plan_schema.py` is DROPPED from (b): this probe is working-tree-scoped (PRE_TASK_HEAD
    base), and 0044-T1's sibling record-spine supersession legitimately edits plan_schema.py, so
    freezing it here false-REDs. 0041-T2 itself never touched plan_schema.py (guarantor
    tests/store/test_plan_model.py). Wave-2 frozen-guard reconciliation, Architect Option-A ruling.

    RED-capable: a transient edit to any forbidden file makes (b)/(c) non-empty -> RED.
    """
    # (a) the sanctioned supersession changed exactly these two surfaces.
    assert _numstat(
        PRE_TASK_HEAD, "scripts/plan/generate_plan.py", "scripts/plan/assemble.py"
    ) != "", "the sanctioned supersession must change generate_plan.py + assemble.py"
    # (b) the HARD-frozen four + the sibling-superseded surfaces are untouched in THIS commit.
    assert _numstat(
        PRE_TASK_HEAD,
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/orchestrate.py", "scripts/plan/router.py",
    ) == "", "the frozen four + sibling-superseded surfaces must be byte-untouched in this commit"
    # (c) the <always-frozen> HARD set is EMPTY over the whole build (origin/main base).
    assert _numstat(
        "origin/main",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py", "scripts/plan/router.py",
    ) == "", "the <always-frozen> HARD set must be numstat=0 over the whole build"


# --- AC-5: offline, 0 live-API, 0 real PII, 0 live-client import -----------------


def test_module_imports_no_live_client_seam():
    """AC-5: the module imports only pytest + the manifest modules + `scripts.store` fixtures —
    0 live-client / live-API import (the author envelope rides the captured `_FixedEnvelopeClient`
    seam that `compute_plan` wraps over `author_output`, no real `ModelClient`)."""
    import inspect
    import sys

    src = inspect.getsource(sys.modules[__name__])
    import_lines = [
        ln for ln in src.splitlines() if ln.strip().startswith(("import ", "from "))
    ]
    joined = "\n".join(import_lines)
    assert "anthropic" not in joined, "no live-API SDK import"
    assert "ModelClient" not in joined, "no live-client import (the captured-envelope seam is used)"
    assert "scripts.model" not in joined, "no live model-client import"
