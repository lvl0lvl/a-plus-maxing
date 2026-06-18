"""Tests for the cross-domain plan orchestrator + reconciler (the step-4 integration function).

`scripts/plan/orchestrate.py` computes every domain's candidate via `compute_plan` (no record),
reconciles across domains, then records the reconciled set. These tests pin:

  - `compute_plan` separates compute from record (it surfaces the author's `reconciliation`
    meta and records NOTHING — the refactor that lets reconciliation run between the two);
  - the nutrition->workout energy BOUNCE: an unsustainable energy verdict bounces the workout,
    the orchestrator re-authors it once under the ceiling, the REDUCED plan is recorded — and
    when no re-author resolves it (no hook, or still over the ceiling) the workout is HELD,
    never an un-fuelable load (each path mutation-proven RED);
  - the RED-S/LEA cross-domain short-circuit: a tripped nutrition critical-floor screen also
    holds the energy-prescribing workout plan (precedence over a coincident bounce);
  - cross-domain OVERLAP + author-declared conflict detection (detect + report, non-blocking);
  - the store-adversarial battery at the orchestrator write boundary (four-domain cross-stream
    isolation + dedupe idempotency); and
  - the production path end-to-end (orchestrated multi-domain pass -> rendered dashboard).

The real-dispatch E2E (a live personal-trainer + nutritionist exercising the bounce) is run
out-of-band per the integration mandate and captured under docs/plan-generation/examples/.
"""

import datetime

from scripts.generate import generate
from scripts.plan.generate_plan import RED_S_LEA_CLINICAL_ROUTING, compute_plan
from scripts.plan.orchestrate import (
    ENERGY_BOUNCE_HELD,
    ENERGY_BOUNCE_UNRESOLVED,
    RED_S_LEA_CROSS_DOMAIN,
    generate_plans,
    reconcile,
)
from scripts.store import plan_schema, store
from tests.plan.test_generate_plan import (
    PLAN_DATE,
    _author,
    _nutrition_meal_rec,
    _nutrition_target_rec,
    _peptide_rec,
    _seed_store,
    _supplement_rec,
    _workout_rec,
)


def _recon(author, **fields):
    """Attach a top-level `reconciliation` dict (the cross-domain inputs) to an envelope."""
    return {**author, "reconciliation": fields}


def _nutrition(*recs, **recon):
    """A nutritionist envelope with optional `reconciliation` (e.g. an `energy_budget`)."""
    author = _author(*recs, specialist="nutritionist")
    return _recon(author, **recon) if recon else author


# --- compute_plan: compute / record separation (AC1) ---------------------------


def test_compute_plan_surfaces_meta_and_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=620)

    candidate = compute_plan("workout", author, store_read)

    assert candidate["meta"] == {"energy_cost_kcal": 620}
    assert candidate["plan"] is not None
    assert candidate["reason"] is None
    # compute_plan does NOT write — recording is the orchestrator's job, after reconciliation.
    assert store.read("plan::workout", root=tmp_path) == []


def test_compute_plan_meta_empty_without_reconciliation(tmp_path):
    store_read = _seed_store(tmp_path)
    candidate = compute_plan("workout", _author(_workout_rec("Goblet squat", 3)), store_read)
    assert candidate["meta"] == {}


# --- energy bounce (nutrition -> workout joint constraint) ---------------------


def test_no_bounce_records_both_when_energy_sustains(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["bounce"] is None
    assert out["reauthored"] is False
    assert out["results"]["workout"]["recorded"] is True
    assert out["results"]["nutrition"]["recorded"] is True
    workout = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert workout["exercises"][0]["name"] == "Goblet squat"


def test_energy_bounce_reauthors_workout_under_ceiling(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
    }
    calls = []

    def reauthor(domain, constraint):
        calls.append((domain, constraint))
        # the personal-trainer is re-dispatched and returns a reduced session under the ceiling.
        return _recon(_author(_workout_rec("Light goblet squat", 2)), energy_cost_kcal=400)

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE, reauthor=reauthor)

    assert out["reconciliation"]["bounce"]["target"] == "workout"
    assert out["reconciliation"]["bounce"]["sustainable_training_kcal"] == 450
    assert out["reauthored"] is True
    assert calls == [("workout", {"sustainable_training_kcal": 450})]
    assert out["results"]["workout"]["recorded"] is True
    # the RECORDED workout is the re-authored reduced plan — never the bounced un-fuelable one.
    recorded = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert recorded["exercises"][0]["name"] == "Light goblet squat"
    # nutrition still stands (it bounced the workout, not itself).
    assert out["results"]["nutrition"]["recorded"] is True


def test_energy_bounce_unresolved_when_reauthor_exceeds_ceiling(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
    }

    def reauthor(domain, constraint):
        # the re-author still came back over the sustainable ceiling -> the load is not fuelable.
        return _recon(_author(_workout_rec("Still heavy squat", 5)), energy_cost_kcal=800)

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE, reauthor=reauthor)

    assert out["reauthored"] is True
    assert out["results"]["workout"]["recorded"] is False
    assert out["results"]["workout"]["reason"] == ENERGY_BOUNCE_UNRESOLVED
    # nothing un-fuelable reaches the store.
    assert store.read("plan::workout", root=tmp_path) == []


def test_energy_bounce_held_without_reauthor_hook(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["bounce"] is not None
    assert out["reauthored"] is False
    assert out["results"]["workout"]["recorded"] is False
    assert out["results"]["workout"]["reason"] == ENERGY_BOUNCE_HELD
    assert store.read("plan::workout", root=tmp_path) == []


# --- RED-S/LEA cross-domain short-circuit (pipeline Phase 0.5) ------------------


def test_red_s_lea_short_circuits_workout(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
        ),
    }

    out = generate_plans(
        authors, store_read, tmp_path, plan_date=PLAN_DATE, gates={"red_s_lea_screen": True}
    )

    assert out["reconciliation"]["red_s_lea_cross_domain"] is True
    assert out["results"]["nutrition"]["recorded"] is False
    assert out["results"]["nutrition"]["reason"] == RED_S_LEA_CLINICAL_ROUTING
    # the energy-prescribing workout is ALSO held to clinical-care routing.
    assert out["results"]["workout"]["recorded"] is False
    assert out["results"]["workout"]["reason"] == RED_S_LEA_CROSS_DOMAIN
    assert store.read("plan::workout", root=tmp_path) == []


def test_red_s_lea_takes_precedence_over_energy_bounce(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=900),
        # both the critical-floor screen trips AND the energy verdict is unsustainable.
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
    }

    out = generate_plans(
        authors, store_read, tmp_path, plan_date=PLAN_DATE, gates={"red_s_lea_screen": True}
    )

    # the safety short-circuit wins: no bounce directive, workout held under RED-S/LEA.
    assert out["reconciliation"]["bounce"] is None
    assert out["reauthored"] is False
    assert out["results"]["workout"]["reason"] == RED_S_LEA_CROSS_DOMAIN


# --- overlap + author-declared conflict detection (detect + report) ------------


def test_overlap_detected_across_supplement_and_peptide(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "supplements": _author(
            _supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"
        ),
        "peptides": _author(
            _peptide_rec("Creatine", "5 g", "oral"), specialist="peptide-specialist"
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert {"intervention": "creatine", "domains": ["peptides", "supplements"]} in (
        out["reconciliation"]["overlaps"]
    )
    # V1 detection is non-blocking: both plans still record (adjudication is the S73 gate).
    assert out["results"]["supplements"]["recorded"] is True
    assert out["results"]["peptides"]["recorded"] is True


def test_no_overlap_when_interventions_distinct(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "supplements": _author(
            _supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"
        ),
        "peptides": _author(
            _peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["overlaps"] == []


def test_author_declared_conflict_surfaced(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "supplements": _recon(
            _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
            conflicts=[
                {"with_domain": "peptides", "with": "bpc-157",
                 "reason": "additive bleeding risk — needs review"},
            ],
        ),
        "peptides": _author(
            _peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    conflicts = out["reconciliation"]["conflicts"]
    assert any(c["from"] == "supplements" and c["with"] == "bpc-157" for c in conflicts)


# --- reconcile is pure (no I/O) ------------------------------------------------


def test_reconcile_is_pure_and_reports_bounce_directive():
    workout = {
        "domain": "workout", "specialist": "personal-trainer",
        "plan": {"exercises": [{"name": "Squat", "sets": 5}]}, "section": {}, "reason": None,
        "meta": {"energy_cost_kcal": 900},
    }
    nutrition = {
        "domain": "nutrition", "specialist": "nutritionist",
        "plan": {"calorie_goal": 2000, "macros": {"protein": 1, "carbs": 1, "fat": 1},
                 "meals": [{"name": "Breakfast"}]},
        "section": {}, "reason": None,
        "meta": {"energy_budget": {"sustains": False, "sustainable_training_kcal": 450}},
    }

    out = reconcile({"workout": workout, "nutrition": nutrition})

    # the bounce is a DIRECTIVE for the orchestrator to re-author, not a hold reconcile applies.
    assert out["holds"] == {}
    assert out["report"]["bounce"]["sustainable_training_kcal"] == 450
    assert out["report"]["bounce"]["workout_cost_kcal"] == 900


# --- store-adversarial battery at the orchestrator write boundary --------------


def test_orchestrator_four_domain_cross_stream_isolation(tmp_path):
    # A multi-domain orchestrated pass keeps each domain's plan in its OWN stream — no
    # cross-contamination across the four plan streams.
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _author(_workout_rec("Goblet squat", 3)),
        "nutrition": _nutrition(_nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600)),
        "supplements": _author(
            _supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"
        ),
        "peptides": _author(
            _peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    for domain in ("workout", "nutrition", "supplements", "peptides"):
        assert out["results"][domain]["recorded"] is True
        assert len(store.read(f"plan::{domain}", root=tmp_path)) == 1
    # each stream holds its own domain's shape — no leakage.
    assert "exercises" in plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert "calorie_goal" in plan_schema.read_plan("nutrition", PLAN_DATE, tmp_path)["plan"]
    assert "items" in plan_schema.read_plan("supplements", PLAN_DATE, tmp_path)["plan"]
    assert "compound" in plan_schema.read_plan("peptides", PLAN_DATE, tmp_path)["plan"]


def test_orchestrator_dedupe_idempotent_rerun(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _author(_workout_rec("Goblet squat", 3)),
        "supplements": _author(
            _supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"
        ),
    }

    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert len(store.read("plan::workout", root=tmp_path)) == 1
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


# --- production path end-to-end (integration-verification mandate) -------------


def test_orchestrator_end_to_end_renders_on_dashboard(tmp_path):
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(calorie_goal=2600),
            _nutrition_meal_rec("Breakfast", contents="eggs, oats", kcal=650),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
        "supplements": _author(
            _supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"
        ),
        "peptides": _author(
            _peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"
        ),
    }

    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    out = generate.run(
        "dashboard", _root=tmp_path, _out_dir=tmp_path,
        _today=datetime.date.fromisoformat(PLAN_DATE),
    )
    html = out.read_text(encoding="utf-8")
    assert "Goblet squat" in html
    assert "Creatine" in html
    assert "BPC-157" in html
