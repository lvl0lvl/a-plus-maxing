"""Tests for the GENERATE-leg production caller (`scripts/plan/pipeline.py` `run_generation`).

`run_generation` is the `/generate-plan` invocation seam: it calls `orchestrate.generate_plans`
(the reconciled multi-domain pass) + `collate_doctor_visit_queue` (the `dvq::queue`) as ONE
recorded GENERATE pass. Until this seam, `generate_plans` had NO production caller. These pin:

  - a clean multi-domain pass records each domain's plan + an EMPTY queue (no held finding);
  - an adjudicated held finding the liaison CLEARS records the domain AND collates a dvq entry
    (the `generate_plans`+`collate` stitch production lacked) -- mutation-proven against the
    no-adjudicator control (the finding holds but is never queued);
  - a block-stands held finding does NOT record the plan but STILL queues it for the MD;
  - `on_date` defaults to `plan_date` (the value-domain default);
  - empty authors record nothing; and
  - the store-surface battery at the seam (cross-stream isolation, dedupe idempotency, mutation).

The real-dispatch E2E (a live specialist authoring a plan fed through `run_generation`) is run
out-of-band, documented in the `/generate-plan` skill's running+verifying section.
"""

from scripts.plan import pipeline
from scripts.store import plan_schema, store
from tests.plan.test_generate_plan import (
    PLAN_DATE,
    _author,
    _nutrition_meal_rec,
    _nutrition_target_rec,
    _seed_store,
    _workout_rec,
)
from tests.plan.test_orchestrate import (
    _SUPP_CONFLICT,
    _conflict_authors,
    _liaison,
    _nutrition,
    _recon,
)


def _sustaining_authors():
    """A clean multi-domain GENERATE set: a fuelable workout + a sustaining nutrition budget."""
    return {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
    }


# --- a clean pass: plans recorded, no held finding -> empty queue --------------

def test_clean_pass_records_plans_and_empty_queue(tmp_path):
    store_read = _seed_store(tmp_path)
    out = pipeline.run_generation(_sustaining_authors(), store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["workout"]["recorded"] is True
    assert out["results"]["nutrition"]["recorded"] is True
    assert out["dvq_entries"] == []                                   # nothing reached the gate
    assert "reconciliation" in out and "results" in out               # the generate_plans shape + dvq
    workout = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert workout["exercises"][0]["name"] == "Goblet squat"


# --- an adjudicated held finding: records + collates the dvq (the missing stitch) ---

def test_cleared_held_finding_records_and_queues(tmp_path):
    store_read = _seed_store(tmp_path)
    out = pipeline.run_generation(
        _conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
        plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    assert out["results"]["supplements"]["recorded"] is True          # cleared -> records
    assert len(out["dvq_entries"]) == 1                               # the stitch: collate ran
    entry = out["dvq_entries"][0]
    assert entry["held_domain"] == "supplements"
    assert entry["outcome"] == "cleared-with-override"
    assert "bpc-157" in entry["caution"]
    # the finding landed in the dvq::queue store stream (not only the return value)
    queued = store.read("dvq::queue", root=tmp_path)
    assert any("bpc-157" in r["value"]["caution"] for r in queued)


def test_held_finding_without_adjudicator_records_and_queues_nothing(tmp_path):
    """MUTATION control: the same held finding with NO adjudicator never reaches the gate -> the
    domain holds (no plan) AND collate queues nothing (only adjudicated dispositions land)."""
    store_read = _seed_store(tmp_path)
    out = pipeline.run_generation(
        _conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["supplements"]["recorded"] is False         # held, no override
    assert store.read("plan::supplements", root=tmp_path) == []
    assert out["dvq_entries"] == []                                   # un-adjudicated -> not queued
    assert store.read("dvq::queue", root=tmp_path) == []
    # PARTIAL split at the seam: the non-conflicting peptides domain still records alongside the hold
    assert out["results"]["peptides"]["recorded"] is True
    assert len(store.read("plan::peptides", root=tmp_path)) == 1


# --- block-stands: no plan, but the MD still sees the finding ------------------

def test_block_stands_not_recorded_but_still_queued(tmp_path):
    store_read = _seed_store(tmp_path)
    out = pipeline.run_generation(
        _conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
        plan_date=PLAN_DATE, adjudicator=_liaison("CRITICAL"))
    assert out["results"]["supplements"]["recorded"] is False         # block stands -> no plan
    assert store.read("plan::supplements", root=tmp_path) == []
    assert len(out["dvq_entries"]) == 1                               # but it IS queued for the MD
    entry = out["dvq_entries"][0]
    assert entry["held_domain"] == "supplements" and entry["outcome"] == "block-stands"
    assert entry["non_overridable"] is True


# --- on_date value domain: defaults to plan_date ------------------------------

def test_on_date_defaults_to_plan_date(tmp_path):
    store_read = _seed_store(tmp_path)
    pipeline.run_generation(                                          # on_date omitted
        _conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
        plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    queued = store.read("dvq::queue", root=tmp_path)
    assert queued and all(r["timepoint"] == PLAN_DATE for r in queued)

    # an explicit on_date dates the collation apart from the plans
    store_read2 = _seed_store(tmp_path / "apart")
    pipeline.run_generation(
        _conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read2, tmp_path / "apart",
        plan_date=PLAN_DATE, on_date="2026-07-15", adjudicator=_liaison("MEDIUM"))
    assert all(r["timepoint"] == "2026-07-15"
               for r in store.read("dvq::queue", root=tmp_path / "apart"))


# --- empty authors record nothing ---------------------------------------------

def test_empty_authors_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    out = pipeline.run_generation({}, store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"] == {}
    assert out["dvq_entries"] == []
    assert store.read("plan::workout", root=tmp_path) == []


# --- the store-surface battery at the seam ------------------------------------

def test_adversarial_cross_stream_isolation(tmp_path):
    """The multi-domain pass keeps each domain's plan in its own stream (no cross-contamination)."""
    store_read = _seed_store(tmp_path)
    pipeline.run_generation(_sustaining_authors(), store_read, tmp_path, plan_date=PLAN_DATE)
    workout = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    nutrition = plan_schema.read_plan("nutrition", PLAN_DATE, tmp_path)["plan"]
    assert "exercises" in workout and "exercises" not in nutrition    # workout shape only in workout
    assert "calorie_goal" in nutrition and "calorie_goal" not in workout
    assert store.read("plan::supplements", root=tmp_path) == []       # an un-authored domain stays empty


def test_adversarial_idempotent_rerun(tmp_path):
    """Re-running the same GENERATE pass at the same date is idempotent (store dedupe holds)."""
    store_read = _seed_store(tmp_path)
    authors = _conflict_authors(supp_conflicts=_SUPP_CONFLICT)
    pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                            adjudicator=_liaison("MEDIUM"))
    first_supp = len(store.read("plan::supplements", root=tmp_path))
    first_dvq = len(store.read("dvq::queue", root=tmp_path))
    pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                            adjudicator=_liaison("MEDIUM"))           # identical re-run
    assert len(store.read("plan::supplements", root=tmp_path)) == first_supp == 1
    assert len(store.read("dvq::queue", root=tmp_path)) == first_dvq == 1


def test_adversarial_mutation_records_authored_content(tmp_path):
    """The recorded plan carries the AUTHORED content (the record is caused by the authors)."""
    store_read = _seed_store(tmp_path)
    authors = {"workout": _recon(_author(_workout_rec("Distinctive-pipeline-lift", 3)),
                                 energy_cost_kcal=500)}
    pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    names = [ex["name"] for ex in plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]["exercises"]]
    assert "Distinctive-pipeline-lift" in names


# --- the seam FORWARDS gates + reauthor to generate_plans (the wiring contract) ---

def test_gates_forwarded_clearance_keeps_load(tmp_path):
    """gates reach compute_plan THROUGH the seam: a non-default clearance_granted=True KEEPS load.
    (A severed gates=None at the seam would default-deny and drop the load -> this goes RED.)"""
    store_read = _seed_store(tmp_path)
    authors = {"workout": _recon(_author(_workout_rec("Back squat", 3, load="70% 1RM")),
                                 energy_cost_kcal=500)}
    out = pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                                  gates={"clearance_granted": True})
    assert out["results"]["workout"]["recorded"] is True
    ex = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]["exercises"][0]
    assert ex.get("load") == "70% 1RM"                               # cleared load survived -> gates forwarded


def test_reauthor_forwarded_energy_bounce_records(tmp_path):
    """The reauthor hook reaches generate_plans THROUGH the seam: an energy bounce re-dispatches and
    the reduced workout records. (A severed reauthor=None at the seam would HOLD it -> this goes RED.)"""
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450}),
    }
    calls = []

    def reauthor(domain, constraint):
        calls.append((domain, constraint))
        return _recon(_author(_workout_rec("Light goblet squat", 2)), energy_cost_kcal=400)

    out = pipeline.run_generation(authors, store_read, tmp_path, plan_date=PLAN_DATE, reauthor=reauthor)
    assert out["reauthored"] is True                                 # the bounce re-dispatch ran via the seam
    assert calls == [("workout", {"sustainable_training_kcal": 450})]
    assert out["results"]["workout"]["recorded"] is True
    recorded = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert recorded["exercises"][0]["name"] == "Light goblet squat"  # the reduced re-author, not the bounced load
