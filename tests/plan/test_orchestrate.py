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
  - the supplement<->peptide additive-AE screen (pipeline Phase 3): a shared additive-AE class or
    an author-declared pairwise interaction HOLDS the supplement before recording, never an
    un-screened additive-AE compound stack (mutation-proven RED);
  - the store-adversarial battery at the orchestrator write boundary (four-domain cross-stream
    isolation + dedupe idempotency); and
  - the production path end-to-end (orchestrated multi-domain pass -> rendered dashboard).

The real-dispatch E2E (a live personal-trainer + nutritionist exercising the bounce) is run
out-of-band per the integration mandate and captured under docs/plan-generation/examples/.
"""

import datetime
import json
from pathlib import Path

import pytest

from scripts.generate import generate
from scripts.plan.generate_plan import RED_S_LEA_CLINICAL_ROUTING, compute_plan
from scripts.plan.orchestrate import (
    ADDITIVE_AE_HELD,
    CONFLICT_HELD,
    ENERGY_BOUNCE_HELD,
    ENERGY_BOUNCE_UNRESOLVED,
    RED_S_LEA_CROSS_DOMAIN,
    RX_BPMH_HELD,
    collate_doctor_visit_queue,
    generate_plans,
    reconcile,
)
from scripts.store import queue_schema
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
from scripts.plan import adjudicate
from tests.plan.test_adjudicate import _envelope, _override_record


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
    # EXACTLY ONE workout write reached the store — the bounced 900-kcal plan was never written
    # (resolve_plan returns the last-appended, so the name assertion alone would stay green if a
    # bug wrote both; this count assertion is what makes the store-safety property non-vacuous).
    assert len(store.read("plan::workout", root=tmp_path)) == 1
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
    # cross-stream: holding the workout does NOT drop nutrition.
    assert out["results"]["nutrition"]["recorded"] is True
    assert len(store.read("plan::nutrition", root=tmp_path)) == 1


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
    # cross-stream: holding the workout does NOT drop nutrition.
    assert out["results"]["nutrition"]["recorded"] is True
    assert len(store.read("plan::nutrition", root=tmp_path)) == 1


def test_energy_bounce_unresolved_when_reauthor_returns_none(tmp_path):
    # a re-dispatch that fails / returns nothing must HOLD the workout, never leave the
    # un-fuelable session recorded — the reauthor hook returning None is that failure mode.
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         reauthor=lambda domain, constraint: None)

    assert out["reauthored"] is True
    assert out["results"]["workout"]["recorded"] is False
    assert out["results"]["workout"]["reason"] == ENERGY_BOUNCE_UNRESOLVED
    assert store.read("plan::workout", root=tmp_path) == []
    # cross-stream: holding the workout does NOT drop nutrition.
    assert out["results"]["nutrition"]["recorded"] is True
    assert len(store.read("plan::nutrition", root=tmp_path)) == 1


def test_energy_bounce_unresolved_when_ceiling_absent(tmp_path):
    # F02: a sustains:false verdict that OMITS sustainable_training_kcal (ceiling=None) must HOLD
    # the workout, never crash — mutation-proves the `ceiling is None` guard (deleting it would
    # reach `new_cost > None` → TypeError on the safety-critical bounce path).
    store_read = _seed_store(tmp_path)
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False},  # no sustainable_training_kcal -> ceiling is None
        ),
    }

    out = generate_plans(
        authors, store_read, tmp_path, plan_date=PLAN_DATE,
        reauthor=lambda domain, constraint: _recon(
            _author(_workout_rec("Light goblet squat", 2)), energy_cost_kcal=200
        ),
    )

    assert out["reauthored"] is True
    assert out["results"]["workout"]["recorded"] is False
    assert out["results"]["workout"]["reason"] == ENERGY_BOUNCE_UNRESOLVED
    assert store.read("plan::workout", root=tmp_path) == []


def test_clearance_gate_strips_load_through_orchestrator(tmp_path):
    # F05: the clearance gate (no load without clinician clearance) must hold on the ORCHESTRATOR
    # path, not just single-domain. A loaded workout rec, default gates -> load stripped; granting
    # clearance keeps it. Deleting the gate in _to_workout_plan would record the load here too.
    store_read = _seed_store(tmp_path)
    authors = {"workout": _author(_workout_rec("Back squat", 4, load="70% 1RM"))}

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    recorded = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert out["results"]["workout"]["recorded"] is True
    assert all("load" not in ex for ex in recorded["exercises"])  # default-deny strips load

    cleared = _seed_store(tmp_path / "cleared")
    out2 = generate_plans(
        authors, cleared, tmp_path / "cleared", plan_date=PLAN_DATE,
        gates={"clearance_granted": True},
    )
    recorded2 = plan_schema.read_plan("workout", PLAN_DATE, tmp_path / "cleared")["plan"]
    assert out2["results"]["workout"]["recorded"] is True
    assert recorded2["exercises"][0]["load"] == "70% 1RM"  # clearance keeps the load


def test_generate_plans_empty_authors_is_clean(tmp_path):
    # a degenerate empty pass records nothing and returns a clean reconciliation report.
    store_read = _seed_store(tmp_path)

    out = generate_plans({}, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["results"] == {}
    assert out["reauthored"] is False
    assert out["reconciliation"]["bounce"] is None
    assert out["reconciliation"]["overlaps"] == []


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
    # V1 detection is non-blocking: both plans still record (adjudication is the S74 liaison gate).
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


def test_overlap_dedupes_domains_and_reports_distinct(tmp_path):
    # F06 (reject-but-adopt): a 3-domain overlap is unreachable (only supplements + peptides
    # contribute compound identities), and a within-domain duplicate is rejected upstream by
    # record_plan's unique-name check — so the dedup is exercised at the reconcile layer, which
    # runs BEFORE recording. reconcile-level: a within-domain duplicate identity yields NO
    # self-overlap (the set dedup; the old list form would report ["supplements","supplements"]).
    supp = {
        "domain": "supplements", "specialist": "supplement-specialist", "section": {}, "reason": None,
        "plan": {"items": [{"name": "Creatine", "dose": "5 g"}, {"name": "Creatine", "dose": "3 g"}]},
        "meta": {},
    }
    assert reconcile({"supplements": supp})["report"]["overlaps"] == []

    # end-to-end: the genuine cross-domain (supplements↔peptides) overlap reports ONE entry with
    # distinct sorted domains.
    store_read = _seed_store(tmp_path)
    cross = {
        "supplements": _author(_supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"),
        "peptides": _author(_peptide_rec("Creatine", "5 g", "oral"), specialist="peptide-specialist"),
    }
    out = generate_plans(cross, store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["reconciliation"]["overlaps"] == [
        {"intervention": "creatine", "domains": ["peptides", "supplements"]}
    ]


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
    # cfaj (S75): the declaring domain is now HELD pending the liaison gate — the safe default with
    # no adjudicator wired (was detect-only/record pre-S75). The non-declaring peptide is unaffected.
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == CONFLICT_HELD
    assert store.read("plan::supplements", root=tmp_path) == []
    assert out["results"]["peptides"]["recorded"] is True


def test_author_declared_conflicts_accumulate_across_authors(tmp_path):
    # F07: conflicts declared by MULTIPLE authors all accumulate (the loop runs to completion).
    # Also pins F01: each entry's `from` is the DECLARING domain, never an author-supplied override.
    store_read = _seed_store(tmp_path)
    authors = {
        "supplements": _recon(
            _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
            conflicts=[{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding risk"}],
        ),
        "peptides": _recon(
            _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
            # this author tries to SUPPLY its own 'from' — the orchestrator must override it.
            conflicts=[{"from": "spoofed", "with_domain": "supplements", "with": "fish oil",
                        "reason": "additive bleeding risk"}],
        ),
    }

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    conflicts = out["reconciliation"]["conflicts"]
    assert len(conflicts) == 2
    assert {c["from"] for c in conflicts} == {"supplements", "peptides"}  # not "spoofed"
    # cfaj (S75): BOTH declaring domains are held (no adjudicator). The held set == the declaring set.
    assert out["results"]["supplements"]["reason"] == CONFLICT_HELD
    assert out["results"]["peptides"]["reason"] == CONFLICT_HELD
    assert store.read("plan::supplements", root=tmp_path) == []
    assert store.read("plan::peptides", root=tmp_path) == []


# --- cross-domain conflict adjudication via the liaison gate (cfaj, Phase 4) ----


def _conflict_authors(supp_conflicts=None, pep_conflicts=None):
    """A supplements + peptides author pair, each with optional `reconciliation.conflicts`."""
    supp = _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist")
    pep = _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist")
    return {
        "supplements": _recon(supp, conflicts=supp_conflicts) if supp_conflicts else supp,
        "peptides": _recon(pep, conflicts=pep_conflicts) if pep_conflicts else pep,
    }


_SUPP_CONFLICT = [{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding risk"}]


def test_conflict_holds_declaring_domain_without_adjudicator(tmp_path):
    # CORE mutation-proof: a declared cross-domain conflict HOLDS the declaring domain before
    # recording (the safe default). Removing the `holds[domain] = CONFLICT_HELD` line records it
    # here -> RED. The non-declaring peptide records.
    store_read = _seed_store(tmp_path)
    out = generate_plans(_conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
                         plan_date=PLAN_DATE)
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == CONFLICT_HELD
    assert store.read("plan::supplements", root=tmp_path) == []
    assert out["results"]["peptides"]["recorded"] is True
    assert len(store.read("plan::peptides", root=tmp_path)) == 1


def test_reconcile_sets_conflict_hold_purely():
    # reconcile (pure, no I/O) sets the conflict hold on the declaring domain that carries a plan.
    supp = {"domain": "supplements", "specialist": "supplement-specialist", "section": {},
            "reason": None, "plan": {"items": [{"name": "Fish oil", "dose": "2 g"}]},
            "meta": {"conflicts": _SUPP_CONFLICT}}
    outcome = reconcile({"supplements": supp})
    assert "supplements" in outcome["conflict_held"]  # tracked independently of `holds`
    assert "supplements" not in outcome["holds"]
    assert any(c["from"] == "supplements" for c in outcome["report"]["conflicts"])


def test_conflict_no_plan_is_not_held():
    # A domain that declares a conflict but computed NO plan has nothing to hold.
    supp = {"domain": "supplements", "specialist": "supplement-specialist", "section": {},
            "reason": "some-reason", "plan": None, "meta": {"conflicts": _SUPP_CONFLICT}}
    outcome = reconcile({"supplements": supp})
    assert "supplements" not in outcome["conflict_held"]
    assert "supplements" not in outcome["holds"]


def test_conflict_liaison_override_releases_and_records(tmp_path):
    # The liaison gate clears a conflict-held domain via a content-valid override -> it records.
    store_read = _seed_store(tmp_path)
    out = generate_plans(_conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "cleared"
    assert out["results"]["supplements"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_conflict_liaison_autoblock_keeps_held(tmp_path):
    # A non-overridable (CRITICAL) liaison adjudication holds the conflict-held domain.
    store_read = _seed_store(tmp_path)
    out = generate_plans(_conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=_liaison("CRITICAL"))
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "block-stands"
    assert out["conflict_adjudications"]["supplements"]["non_overridable"] is True
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_conflict_liaison_vacuous_override_keeps_held(tmp_path):
    store_read = _seed_store(tmp_path)
    liaison = _liaison("HIGH", override=_override_record("HIGH", operator_reason="trust me"))
    out = generate_plans(_conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=liaison)
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "block-stands"
    assert store.read("plan::supplements", root=tmp_path) == []


def test_conflict_safety_finding_id_and_caution(tmp_path):
    # The orchestrator routes a deterministic finding_id + a caution reproducing the conflict.
    store_read = _seed_store(tmp_path)
    liaison = _liaison("MEDIUM")
    generate_plans(_conflict_authors(supp_conflicts=_SUPP_CONFLICT), store_read, tmp_path,
                   plan_date=PLAN_DATE, adjudicator=liaison)
    assert len(liaison.calls) == 1
    finding = liaison.calls[0]
    assert finding["finding_id"] == "conflict:supplements:peptides/bpc-157"
    assert finding["held_domain"] == "supplements"
    assert "bpc-157" in finding["caution"]


def test_conflict_additive_ae_takes_precedence_over_conflict_hold(tmp_path):
    # A supplement that BOTH declares a conflict AND trips the additive-AE screen is ADDITIVE_AE_HELD
    # (the compound-band screen is more specific); the conflict hold does not shadow it.
    store_read = _seed_store(tmp_path)
    authors = _conflict_authors(supp_conflicts=_SUPP_CONFLICT)
    authors["supplements"] = _recon(
        _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
        conflicts=_SUPP_CONFLICT, ae_profile={"additive_classes": ["bleeding-risk"]},
    )
    authors["peptides"] = _recon(
        _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
        ae_profile={"additive_classes": ["bleeding-risk"]},
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD


def test_conflict_adjudicator_not_called_without_conflict(tmp_path):
    # Non-tautology control: no declared conflict -> no conflict hold, no conflict adjudication.
    store_read = _seed_store(tmp_path)
    liaison = _liaison("MEDIUM")
    out = generate_plans(_conflict_authors(), store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=liaison)
    assert out["conflict_adjudications"] == {}
    assert out["results"]["supplements"]["recorded"] is True


def test_real_conflict_liaison_cleared_envelope_records(tmp_path):
    # AC3 codified: the REAL captured medical-liaison conflict-adjudication envelope (a content-valid
    # MEDIUM override of an author-declared cross-domain conflict), run through the production path,
    # RELEASES the conflict-held supplement — the conflict axis closed via the SAME S74 gate, verified
    # E2E with genuine liaison output (not a stub).
    store_read = _seed_store(tmp_path)
    env = _example_envelope("liaison-conflict-cleared.example.json")
    conflict = [{"with_domain": "peptides", "with": "bpc-157",
                 "reason": "additive bleeding risk, needs review"}]
    out = generate_plans(_conflict_authors(supp_conflicts=conflict), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=lambda finding: env)
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "cleared"
    assert out["results"]["supplements"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_real_conflict_liaison_blocked_envelope_keeps_held(tmp_path):
    # Tier-3 TEST-3 (parity with the additive-AE block companion): the REAL-shape blocked conflict
    # envelope (a vacuous override at HIGH) keeps the conflict-declaring supplement held, with the
    # rejection reasons pinned so the conflict E2E goes RED if the INV-OVERRIDE-RECORD-SCHEMA sub-gate
    # regresses on this axis.
    store_read = _seed_store(tmp_path)
    env = _example_envelope("liaison-conflict-blocked.example.json")
    conflict = [{"with_domain": "peptides", "with": "bpc-157",
                 "reason": "additive bleeding risk, needs review"}]
    out = generate_plans(_conflict_authors(supp_conflicts=conflict), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=lambda finding: env)
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []
    reasons = out["conflict_adjudications"]["supplements"]["reasons"]
    assert any("operator_reason" in r for r in reasons)
    assert any("rung" in r for r in reasons)


def test_conflict_from_non_compound_domain_held_and_adjudicated(tmp_path):
    # A conflict declared by a NON-compound domain (workout) is held + adjudicated the same way —
    # the gate is domain-agnostic (compute_plan lifts `reconciliation.conflicts` for every domain).
    workout = _recon(_author(_workout_rec("Goblet squat", 3)),
                     conflicts=[{"with_domain": "nutrition", "with": "deficit", "reason": "load vs intake"}])
    out = generate_plans({"workout": workout}, _seed_store(tmp_path), tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["workout"]["reason"] == CONFLICT_HELD
    cleared = generate_plans({"workout": workout}, _seed_store(tmp_path / "b"), tmp_path / "b",
                             plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    assert cleared["conflict_adjudications"]["workout"]["outcome"] == "cleared"
    assert cleared["results"]["workout"]["recorded"] is True


def test_conflict_adjudicator_returning_none_keeps_held(tmp_path):
    # Parity with the additive-AE path: a conflict adjudicator that returns None leaves the block held.
    out = generate_plans(_conflict_authors(supp_conflicts=_SUPP_CONFLICT), _seed_store(tmp_path),
                         tmp_path, plan_date=PLAN_DATE, adjudicator=lambda finding: None)
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_conflict_multiple_declaring_domains_each_adjudicated(tmp_path):
    # The loop adjudicates EACH conflict-held domain independently (one entry per declarer).
    authors = _conflict_authors(
        supp_conflicts=[{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"}],
        pep_conflicts=[{"with_domain": "supplements", "with": "fish oil", "reason": "additive bleeding"}],
    )
    out = generate_plans(authors, _seed_store(tmp_path), tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_liaison("MEDIUM"))
    assert set(out["conflict_adjudications"]) == {"supplements", "peptides"}
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "cleared"
    assert out["conflict_adjudications"]["peptides"]["outcome"] == "cleared"
    assert out["results"]["supplements"]["recorded"] is True
    assert out["results"]["peptides"]["recorded"] is True


def test_red_s_lea_precedence_over_a_coincident_conflict(tmp_path):
    # A workout short-circuited by the nutrition RED-S/LEA screen stays RED-S/LEA-held even if it
    # declares a conflict — RED-S/LEA precedence; the conflict hold does not shadow it.
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500,
                          conflicts=[{"with_domain": "nutrition", "with": "deficit", "reason": "x"}]),
        "nutrition": _nutrition(_nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600)),
    }
    out = generate_plans(authors, _seed_store(tmp_path), tmp_path, plan_date=PLAN_DATE,
                         gates={"red_s_lea_screen": True})
    assert out["results"]["workout"]["reason"] == RED_S_LEA_CROSS_DOMAIN


def test_energy_bounce_and_conflict_are_independent_holds(tmp_path):
    # Tier-3 BUG-1 fix: a workout that declares a conflict AND is energy-bounced (no reauthor) carries
    # BOTH holds INDEPENDENTLY. The bounce hold makes it not record; the conflict is INDEPENDENTLY
    # adjudicated (not "overwritten" by the bounce). With a clearing liaison, the conflict clears but
    # the workout STILL does not record — the bounce hold stands. (Pre-fix the conflict was shadowed.)
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900,
                          conflicts=[{"with_domain": "nutrition", "with": "deficit", "reason": "x"}]),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
    }
    out = generate_plans(authors, _seed_store(tmp_path), tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_liaison("MEDIUM"))
    assert out["results"]["workout"]["reason"] == ENERGY_BOUNCE_HELD  # held (bounce), not recorded
    assert out["conflict_adjudications"]["workout"]["outcome"] == "cleared"  # conflict adjudicated independently
    assert store.read("plan::workout", root=tmp_path) == []  # the bounce hold still suppresses it


def test_bounce_success_with_conflict_keeps_workout_conflict_held(tmp_path):
    # Tier-3 BUG-1 fix: a workout that declares a conflict AND is energy-bounced but reauthored fuelable
    # is NOT released by the successful bounce — its INDEPENDENT conflict hold stands (no adjudicator).
    # Pre-fix the success path left a stale single-reason hold and could record the reauthored plan.
    def reauthor(domain, constraint):
        return _recon(_author(_workout_rec("Light goblet squat", 2)),
                      energy_cost_kcal=constraint["sustainable_training_kcal"] - 50,
                      conflicts=[{"with_domain": "nutrition", "with": "deficit", "reason": "x"}])
    authors = {
        "workout": _recon(_author(_workout_rec("Heavy back squat", 5)), energy_cost_kcal=900,
                          conflicts=[{"with_domain": "nutrition", "with": "deficit", "reason": "x"}]),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": False, "sustainable_training_kcal": 450},
        ),
    }
    out = generate_plans(authors, _seed_store(tmp_path), tmp_path, plan_date=PLAN_DATE, reauthor=reauthor)
    assert out["reauthored"] is True
    assert out["results"]["workout"]["recorded"] is False  # the independent conflict hold stands
    assert out["results"]["workout"]["reason"] == CONFLICT_HELD
    assert store.read("plan::workout", root=tmp_path) == []


def test_additive_ae_cleared_but_distinct_conflict_keeps_supplement_held(tmp_path):
    # Tier-3 SEC-1 MUST-FIX: a supplement that BOTH trips the additive-AE screen AND declares a DISTINCT
    # cross-domain conflict is held by both. Clearing the additive-AE override must NOT release it — the
    # distinct conflict still holds it. Pre-fix the additive-AE clear (del holds["supplements"]) recorded
    # the supplement with the conflict never adjudicated. With a per-finding adjudicator that clears the
    # additive-AE but BLOCKS the conflict (CRITICAL), the supplement stays held.
    store_read = _seed_store(tmp_path)
    authors = {
        "supplements": _recon(
            _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
            ae_profile={"additive_classes": ["bleeding-risk"]},
            conflicts=[{"with_domain": "workout", "with": "high-volume", "reason": "recovery load"}],
        ),
        "peptides": _recon(
            _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
            ae_profile={"additive_classes": ["bleeding-risk"]},
        ),
    }

    def adjudicator(safety_finding):
        # Clear the additive-AE finding (MEDIUM override); BLOCK the distinct conflict (CRITICAL auto-block).
        band = "CRITICAL" if safety_finding["source"] == "cross-domain-conflict" else "MEDIUM"
        env = _envelope(band=band, finding_id=safety_finding["finding_id"])
        if env["override_record"] is not None:
            env["override_record"]["caution_verbatim"] = safety_finding["caution"]
        return env

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=adjudicator)
    assert out["adjudication"]["outcome"] == "cleared"  # the additive-AE WAS cleared
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "block-stands"  # the conflict was NOT
    assert out["results"]["supplements"]["recorded"] is False  # still held by the open conflict
    assert store.read("plan::supplements", root=tmp_path) == []


def test_conflict_safety_finding_multi_conflict_per_domain_sorted(tmp_path):
    # Tier-3 TEST-2: a domain declaring 2+ conflicts aggregates into ONE finding with sorted, order-stable
    # finding_id tokens AND caution detail (so the caution the liaison must reproduce verbatim is
    # regenerable). Input is deliberately out-of-sorted-order.
    store_read = _seed_store(tmp_path)
    liaison = _liaison("MEDIUM")
    authors = _conflict_authors(supp_conflicts=[
        {"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"},
        {"with_domain": "nutrition", "with": "fish-protein", "reason": "allergen overlap"},
    ])
    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=liaison)
    finding = liaison.calls[0]
    # sorted by (with_domain, with): nutrition/fish-protein before peptides/bpc-157
    assert finding["finding_id"] == "conflict:supplements:nutrition/fish-protein;peptides/bpc-157"
    assert finding["caution"].index("fish-protein") < finding["caution"].index("bpc-157")


# --- supplement<->peptide additive-AE screen (pipeline Phase 3) ----------------


def _compound_authors(supp_recon=None, pep_recon=None):
    """A supplements + peptides author pair, each with an optional `reconciliation` dict."""
    supp = _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist")
    pep = _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist")
    return {
        "supplements": _recon(supp, **supp_recon) if supp_recon else supp,
        "peptides": _recon(pep, **pep_recon) if pep_recon else pep,
    }


def test_additive_ae_shared_class_holds_supplement(tmp_path):
    # CORE mutation-proof: a supplement and a peptide that each clear their single-domain filters
    # but BOTH carry the same additive-AE class (bleeding-risk) is an additive combination. The
    # screen HOLDS the supplement (it finalizes last) and surfaces the finding. Deleting the
    # screen would record the supplement here -> this test goes RED, which is the proof.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk", "malignancy-risk"]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["additive_ae"] == [
        {"kind": "shared-class", "ae_class": "bleeding-risk", "between": ["peptides", "supplements"]}
    ]
    # the supplement is HELD (the honest no-stack state), never the un-screened additive stack.
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD
    assert store.read("plan::supplements", root=tmp_path) == []
    # cross-stream: holding the supplement does NOT drop the peptide draft.
    assert out["results"]["peptides"]["recorded"] is True
    assert len(store.read("plan::peptides", root=tmp_path)) == 1


def test_additive_ae_class_match_is_case_insensitive(tmp_path):
    # the class tokens are normalized (lowercased/stripped) before intersection — two authors
    # writing the same class with different casing/spacing still match.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["  Bleeding-Risk "]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["additive_ae"][0]["ae_class"] == "bleeding-risk"
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD


def test_additive_ae_declared_interaction_from_peptide_side(tmp_path):
    # bidirectional path A: the PEPTIDE author names the supplement item in a pairwise interaction.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        pep_recon={"ae_profile": {"interactions": [
            {"with": "Fish oil", "mechanism": "additive antiplatelet effect", "severity": "moderate"}
        ]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    finding = out["reconciliation"]["additive_ae"][0]
    assert finding["kind"] == "declared-interaction"
    assert finding["from"] == "peptides"
    assert finding["with"] == "fish oil"
    # mechanism + severity ride through for the S74 liaison to adjudicate.
    assert finding["mechanism"] == "additive antiplatelet effect"
    assert finding["severity"] == "moderate"
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD
    # store-safety pinned DIRECTLY on the interaction path (not only via the reason proxy): the
    # interaction-driven hold must keep the supplement out of the store, like the shared-class path.
    assert store.read("plan::supplements", root=tmp_path) == []
    assert out["results"]["peptides"]["recorded"] is True


def test_additive_ae_declared_interaction_from_supplement_side(tmp_path):
    # bidirectional path B: the SUPPLEMENT author names the peptide compound in a pairwise
    # interaction — the same finding fires (the screen checks BOTH authors' declarations).
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"interactions": [
            {"with": "BPC-157", "mechanism": "additive angiogenic load", "severity": "high"}
        ]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    finding = out["reconciliation"]["additive_ae"][0]
    assert finding["from"] == "supplements"
    assert finding["with"] == "bpc-157"
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD


def test_no_additive_ae_when_profiles_disjoint(tmp_path):
    # NON-TAUTOLOGY control: distinct additive classes + no declared interaction -> NO finding and
    # BOTH compounds record. Proves the screen discriminates rather than always-holding.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["gi-irritation"]}},
        pep_recon={"ae_profile": {"additive_classes": ["malignancy-risk"]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["additive_ae"] == []
    assert out["results"]["supplements"]["recorded"] is True
    assert out["results"]["peptides"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_additive_ae_inert_without_a_peptide(tmp_path):
    # the screen needs BOTH compound domains to carry a plan — a supplement alone (even with an
    # ae_profile) has no peptide to be additive WITH, so it records normally.
    store_read = _seed_store(tmp_path)
    supp = _recon(
        _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
        ae_profile={"additive_classes": ["bleeding-risk"]},
    )

    out = generate_plans({"supplements": supp}, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["additive_ae"] == []
    assert out["results"]["supplements"]["recorded"] is True


def test_additive_ae_screen_inert_without_ae_profiles(tmp_path):
    # a supplement + peptide pair that declare NO ae_profile records both — the screen only fires
    # on a declared additive class or interaction, never by mere co-presence (overlap ≠ additive AE).
    store_read = _seed_store(tmp_path)

    out = generate_plans(_compound_authors(), store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["reconciliation"]["additive_ae"] == []
    assert out["results"]["supplements"]["recorded"] is True
    assert out["results"]["peptides"]["recorded"] is True


def test_additive_ae_held_supplement_idempotent_on_rerun(tmp_path):
    # store-safety: re-running an additive-AE pass never leaks the held supplement into the store.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )

    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    assert store.read("plan::supplements", root=tmp_path) == []
    assert len(store.read("plan::peptides", root=tmp_path)) == 1


def test_reconcile_additive_ae_is_pure():
    # reconcile surfaces the finding + the supplement hold with NO I/O (mirrors the bounce-purity
    # pin); the orchestrator applies the hold.
    supp = {
        "domain": "supplements", "specialist": "supplement-specialist", "section": {}, "reason": None,
        "plan": {"items": [{"name": "Fish oil", "dose": "2 g"}]},
        "meta": {"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    }
    pep = {
        "domain": "peptides", "specialist": "peptide-specialist", "section": {}, "reason": None,
        "plan": {"compound": "BPC-157", "dose": "250 mcg", "route": "subq"},
        "meta": {"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    }

    out = reconcile({"supplements": supp, "peptides": pep})

    assert out["report"]["additive_ae"][0]["ae_class"] == "bleeding-risk"
    assert out["holds"]["supplements"] == ADDITIVE_AE_HELD


def test_additive_ae_end_to_end_renders_peptide_holds_supplement(tmp_path):
    # integration mandate: an additive-AE pass renders the peptide draft on the dashboard while the
    # held supplement does NOT surface its (un-screened) stack — the production-path proof.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )

    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    out = generate.run(
        "dashboard", _root=tmp_path, _out_dir=tmp_path,
        _today=datetime.date.fromisoformat(PLAN_DATE),
    )
    html = out.read_text(encoding="utf-8")
    assert "BPC-157" in html  # the peptide draft renders
    assert "Fish oil" not in html  # the held supplement's stack never reaches the card


def test_additive_ae_malformed_profile_is_inert_by_design(tmp_path):
    # DELIBERATE trusted-author contract (not an accident): a present-but-MALFORMED ae_profile —
    # additive_classes a string not a list, a non-dict ae_profile, a non-list interactions, an
    # interaction missing `with` — is treated as NO declaration (no finding, supplement records).
    # The screen reads the structured form; a malformed one is not guessed at. This pins the
    # fail-direction so a future refactor cannot silently WIDEN it. (Fail-loud is an S74 candidate.)
    malformed = [
        {"ae_profile": {"additive_classes": "bleeding-risk"}},          # string, not a list
        {"ae_profile": ["bleeding-risk"]},                              # not a dict
        {"ae_profile": {"interactions": {"with": "BPC-157"}}},          # interactions not a list
        {"ae_profile": {"interactions": [{"mechanism": "x"}]}},         # interaction missing `with`
    ]
    for i, supp_recon in enumerate(malformed):
        root = tmp_path / f"m{i}"
        sr = _seed_store(root)
        out = generate_plans(
            _compound_authors(supp_recon=supp_recon,
                              pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}}),
            sr, root, plan_date=PLAN_DATE,
        )
        assert out["reconciliation"]["additive_ae"] == [], f"malformed[{i}] must produce no finding"
        assert out["results"]["supplements"]["recorded"] is True, f"malformed[{i}] records (inert)"
        assert len(store.read("plan::supplements", root=root)) == 1


def test_additive_ae_interaction_with_is_normalized(tmp_path):
    # the interaction `with` token is normalized (lowercase/strip) independently of the class path:
    # a mixed-case/whitespace `with` still matches the other compound's identity.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"interactions": [
            {"with": "  Bpc-157 ", "mechanism": "x", "severity": "moderate"}
        ]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    finding = out["reconciliation"]["additive_ae"][0]
    assert finding["kind"] == "declared-interaction" and finding["with"] == "bpc-157"
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD


def test_additive_ae_holds_whole_multi_item_supplement(tmp_path):
    # one additive item holds the ENTIRE supplement plan (the conservative no-stack state) — the
    # whole multi-item plan is suppressed, not just the offending item.
    store_read = _seed_store(tmp_path)
    supp = _recon(
        _author(_supplement_rec("Fish oil", "2 g"), _supplement_rec("Creatine", "5 g"),
                specialist="supplement-specialist"),
        ae_profile={"additive_classes": ["bleeding-risk"]},
    )
    pep = _recon(
        _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
        ae_profile={"additive_classes": ["bleeding-risk"]},
    )

    out = generate_plans({"supplements": supp, "peptides": pep}, store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD
    assert store.read("plan::supplements", root=tmp_path) == []  # the whole stack is held


def test_additive_ae_both_sides_declare_yields_finding_per_direction(tmp_path):
    # when BOTH authors name the other compound, each declaration is a distinct finding (the
    # liaison sees both authors' reasoning); the hold is set ONCE regardless. Dedup, if wanted, is
    # the S74 liaison gate's call — V1 surfaces both directions faithfully.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"interactions": [{"with": "BPC-157", "mechanism": "a", "severity": "moderate"}]}},
        pep_recon={"ae_profile": {"interactions": [{"with": "Fish oil", "mechanism": "b", "severity": "moderate"}]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    findings = out["reconciliation"]["additive_ae"]
    froms = sorted(f["from"] for f in findings if f["kind"] == "declared-interaction")
    assert froms == ["peptides", "supplements"]  # one finding per declaring direction
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD  # held once


def test_additive_ae_interaction_severity_mechanism_optional(tmp_path):
    # an interaction with no severity/mechanism still fires the hold (they ride through as None for
    # the S74 liaison; their absence does not suppress the safety finding).
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        pep_recon={"ae_profile": {"interactions": [{"with": "Fish oil"}]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    finding = out["reconciliation"]["additive_ae"][0]
    assert finding["with"] == "fish oil"
    assert finding["mechanism"] is None and finding["severity"] is None
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD


def test_additive_ae_two_shared_classes_each_a_finding(tmp_path):
    # the screen emits ONE finding per shared additive-AE class, in sorted order — pins the
    # `sorted(supp & pep)` enumeration (cardinality + ordering) the single-class tests never reach.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["serotonergic", "bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk", "serotonergic"]}},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    shared = [f for f in out["reconciliation"]["additive_ae"] if f["kind"] == "shared-class"]
    assert [f["ae_class"] for f in shared] == ["bleeding-risk", "serotonergic"]  # one each, sorted
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD  # held ONCE
    assert store.read("plan::supplements", root=tmp_path) == []


def test_additive_ae_shared_class_and_interaction_combine(tmp_path):
    # a single pass can trigger BOTH detection paths: the screen runs the shared-class intersection
    # AND the interaction passes unconditionally, so both finding kinds surface, hold set once.
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {
            "additive_classes": ["bleeding-risk"],
            "interactions": [{"with": "Fish oil", "mechanism": "x", "severity": "high"}],
        }},
    )

    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)

    kinds = sorted(f["kind"] for f in out["reconciliation"]["additive_ae"])
    assert kinds == ["declared-interaction", "shared-class"]  # both paths fired in one pass
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD  # held once
    assert store.read("plan::supplements", root=tmp_path) == []


# --- medical-liaison terminal adjudication gate (pipeline Phase 4) -------------


def _liaison(band="HIGH", harm_class=None, override="auto", set_by="auto"):
    """An adjudicator hook that echoes the received finding's id + caution into an envelope.

    Records every call on `.calls` so a test can assert the gate ran (or did not) and on what.
    """
    calls = []

    def hook(safety_finding):
        calls.append(safety_finding)
        env = _envelope(band=band, harm_class=harm_class, finding_id=safety_finding["finding_id"],
                        override=override, set_by=set_by)
        if env["override_record"] is not None:
            env["override_record"]["caution_verbatim"] = safety_finding["caution"]
        return env

    hook.calls = calls
    return hook


def _held_pair():
    """A fish-oil + BPC-157 pair that both declare bleeding-risk -> the supplement is held."""
    return _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )


def test_liaison_valid_override_releases_and_records_supplement(tmp_path):
    # CORE mutation-proof: a held additive-AE supplement clears via a content-valid HIGH override
    # -> the hold is RELEASED and the supplement RECORDS. Removing `del holds["supplements"]` (the
    # release) leaves it held -> this test goes RED, the proof the gate actually clears.
    store_read = _seed_store(tmp_path)
    liaison = _liaison("HIGH")

    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=liaison)

    assert out["adjudication"]["outcome"] == "cleared"
    assert out["adjudication"]["override_record"] is not None
    assert out["results"]["supplements"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1
    # cross-stream: clearing the supplement does not disturb the peptide draft.
    assert out["results"]["peptides"]["recorded"] is True
    assert len(store.read("plan::peptides", root=tmp_path)) == 1


def test_liaison_critical_autoblock_keeps_supplement_held(tmp_path):
    store_read = _seed_store(tmp_path)
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_liaison("CRITICAL"))

    assert out["adjudication"]["outcome"] == "block-stands"
    assert out["adjudication"]["non_overridable"] is True
    assert out["adjudication"]["reasons"] == [adjudicate.AUTO_BLOCK_SENTINEL]
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_liaison_critical_override_path_rejected_keeps_held(tmp_path):
    # INV-CRITICAL-NON-OVERRIDABLE at the wiring: a CRITICAL finding that arrives WITH an override
    # path never releases — the block stands. Mutation: dropping the non-overridable gate would let
    # the override path clear the supplement -> RED.
    store_read = _seed_store(tmp_path)
    liaison = _liaison("CRITICAL", override=_override_record("HIGH"), set_by=adjudicate.LIAISON_SET_BY)

    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=liaison)

    assert out["adjudication"]["outcome"] == "block-stands"
    assert out["adjudication"]["non_overridable"] is True
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_liaison_vacuous_override_keeps_held(tmp_path):
    store_read = _seed_store(tmp_path)
    liaison = _liaison("HIGH", override=_override_record("HIGH", operator_reason="trust me"))

    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=liaison)

    assert out["adjudication"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_no_adjudicator_keeps_held_supplement_held(tmp_path):
    # The safe default (S73 behavior, unchanged): no adjudicator wired -> the supplement stays held
    # and no adjudication ran.
    store_read = _seed_store(tmp_path)
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE)

    assert out["adjudication"] is None
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_adjudicator_returning_none_keeps_held(tmp_path):
    # A wired adjudicator that returns None (a real liaison dispatch can fail / decline to emit) is
    # treated as no adjudication -> the block stands (parity with the reauthor-returns-None path).
    store_read = _seed_store(tmp_path)
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=lambda finding: None)
    assert out["adjudication"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_adjudicator_that_raises_is_fail_loud_and_records_nothing(tmp_path):
    # Review TEST-3: a liaison dispatch that ERRORS is fail-loud — the exception propagates out of
    # generate_plans (matching the unguarded reauthor hook), and because it raises BEFORE the
    # recording loop, NOTHING is recorded. The safe no-release direction: an errored adjudication
    # never silently records the held supplement.
    store_read = _seed_store(tmp_path)

    def boom(safety_finding):
        raise RuntimeError("liaison dispatch failed")

    with pytest.raises(RuntimeError):
        generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=boom)
    assert store.read("plan::supplements", root=tmp_path) == []
    assert store.read("plan::peptides", root=tmp_path) == []


def test_adjudicator_not_called_without_a_held_finding(tmp_path):
    # Non-tautology control: a clean (no declared additive-AE) compound pair is NOT held, so the
    # liaison gate never runs and both compounds record.
    store_read = _seed_store(tmp_path)
    liaison = _liaison("HIGH")

    out = generate_plans(_compound_authors(), store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=liaison)

    assert out["adjudication"] is None
    assert liaison.calls == []
    assert out["results"]["supplements"]["recorded"] is True
    assert out["results"]["peptides"]["recorded"] is True


def test_liaison_receives_deterministic_finding_id_and_caution(tmp_path):
    # The orchestrator routes a `safety_finding` with a deterministic id + the caution the override
    # record must reproduce verbatim — the contract the real liaison echoes.
    store_read = _seed_store(tmp_path)
    liaison = _liaison("HIGH")

    generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=liaison)

    assert len(liaison.calls) == 1
    finding = liaison.calls[0]
    assert finding["finding_id"] == "additive-ae:class:bleeding-risk"
    assert finding["held_domain"] == "supplements"
    assert "bleeding-risk" in finding["caution"]


def test_liaison_cleared_supplement_renders_on_dashboard(tmp_path):
    # Integration: a cleared supplement reaches the store and renders on the dashboard.
    store_read = _seed_store(tmp_path)
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_liaison("HIGH"))

    assert out["adjudication"]["outcome"] == "cleared"
    rendered = generate.run(
        "dashboard", _root=tmp_path, _out_dir=tmp_path,
        _today=datetime.date.fromisoformat(PLAN_DATE),
    )
    html = rendered.read_text(encoding="utf-8")
    assert "Fish oil" in html  # the cleared supplement renders
    assert "BPC-157" in html  # the peptide draft renders alongside


def _example_envelope(name):
    """Load a captured medical-liaison adjudication envelope from docs/plan-generation/examples."""
    path = Path(__file__).resolve().parents[2] / "docs/plan-generation/examples" / name
    return json.loads(path.read_text(encoding="utf-8"))


def test_real_liaison_cleared_envelope_releases_supplement(tmp_path):
    # AC5 codified: the REAL captured medical-liaison cleared envelope (a content-valid MEDIUM
    # informed-refusal override), run through the production path, RELEASES the held supplement —
    # the held-line closer verified end-to-end with genuine liaison output, not a stub.
    store_read = _seed_store(tmp_path)
    env = _example_envelope("liaison-adjudication-cleared.example.json")
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=lambda finding: env)
    assert out["adjudication"]["outcome"] == "cleared"
    assert out["results"]["supplements"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_real_liaison_blocked_envelope_keeps_held(tmp_path):
    # The companion: the REAL refusal scenario (a vacuous override at HIGH) leaves the block
    # standing — the supplement is never recorded on insistence.
    store_read = _seed_store(tmp_path)
    env = _example_envelope("liaison-adjudication-blocked.example.json")
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=lambda finding: env)
    assert out["adjudication"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []
    # Single-gate isolation (review TEST-1): the blocked fixture is rejected on BOTH the vacuous
    # operator_reason AND the sub-HIGH rung. Pinning each rejection reason makes this E2E go RED if
    # EITHER INV-OVERRIDE-RECORD-SCHEMA sub-gate regresses (not only if both fail at once).
    reasons = out["adjudication"]["reasons"]
    assert any("operator_reason" in r for r in reasons)
    assert any("rung" in r for r in reasons)


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


def test_orchestrator_dedupe_key_boundary_date(tmp_path):
    # dedupe-key boundary (store-adversarial item 3): a different plan_date is a DISTINCT
    # identity at the generate_plans boundary — both records persist, no collision.
    store_read = _seed_store(tmp_path)
    authors = {"workout": _author(_workout_rec("Goblet squat", 3))}

    generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plans(authors, store_read, tmp_path, plan_date="2026-06-19")

    assert len(store.read("plan::workout", root=tmp_path)) == 2


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
    assert "Breakfast" in html  # nutrition round-trips through the orchestrated pass too
    assert "2600" in html
    assert "Creatine" in html
    assert "BPC-157" in html


# --- supplement<->Rx BPMH screen + adjudication (rxbp, pipeline Phase 4) ---------
#
# The operator's present Rx-interaction classes are seeded as the curated, de-identified
# `rx-interaction-classes` store item (never raw drug names — that boundary is proven in
# tests/plan/test_router.py). generate_plans reads them through `router.summarize` and holds a
# compound whose declared additive-AE class stacks against them, routing it through the SAME gate.


def _bpmh_store(tmp_path, rx_classes):
    """A seeded store whose operator carries the given curated Rx-interaction-class token list."""
    return _seed_store(tmp_path, **{"rx-interaction-classes": rx_classes})


def _bpmh_supp_authors(supp_classes, pep_classes=None):
    """A supplement (declaring `supp_classes`) + a peptide pair for the BPMH screen."""
    return _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": supp_classes}},
        pep_recon={"ae_profile": {"additive_classes": pep_classes}} if pep_classes else None,
    )


def _selective_liaison(by_source):
    """An adjudicator returning a band per finding `source` (or None -> no envelope, block stands).

    Lets a test clear ONE concern while leaving another open — the interaction probe (PF-S75-01).
    """
    calls = []

    def hook(safety_finding):
        calls.append(safety_finding)
        band = by_source.get(safety_finding["source"])
        if band is None:
            return None
        env = _envelope(band=band, finding_id=safety_finding["finding_id"])
        if env["override_record"] is not None:
            env["override_record"]["caution_verbatim"] = safety_finding["caution"]
        return env

    hook.calls = calls
    return hook


def _supp_candidate(additive_classes):
    """A raw supplements candidate dict (no I/O) declaring `additive_classes` for the BPMH screen."""
    return {"domain": "supplements", "specialist": "supplement-specialist", "section": {},
            "reason": None, "plan": {"items": [{"name": "Fish oil", "dose": "2 g"}]},
            "meta": {"ae_profile": {"additive_classes": additive_classes}}}


def test_reconcile_sets_rx_bpmh_hold_purely():
    # CORE mutation-proof: reconcile (pure, no I/O) holds a compound whose declared additive-AE class
    # intersects the operator's present Rx classes, in the INDEPENDENT rx_bpmh_held set. Remove the
    # screen -> empty.
    outcome = reconcile({"supplements": _supp_candidate(["bleeding-risk"])},
                        operator_rx_classes={"bleeding-risk"})
    assert "supplements" in outcome["rx_bpmh_held"]
    assert outcome["report"]["rx_bpmh"] == [{"held_domain": "supplements", "classes": ["bleeding-risk"]}]
    assert "supplements" not in outcome["holds"]  # tracked independently of `holds`


def test_reconcile_no_rx_bpmh_hold_when_disjoint():
    outcome = reconcile({"supplements": _supp_candidate(["bleeding-risk"])},
                        operator_rx_classes={"cyp3a4-pgp"})  # operator on a different class
    assert outcome["rx_bpmh_held"] == []
    assert outcome["report"]["rx_bpmh"] == []


def test_reconcile_no_rx_bpmh_hold_without_operator_classes():
    # The default (no operator_rx_classes arg) is the backward-compatible no-Rx surface -> no hold.
    outcome = reconcile({"supplements": _supp_candidate(["bleeding-risk"])})
    assert outcome["rx_bpmh_held"] == []


def test_rx_bpmh_holds_supplement_without_adjudicator(tmp_path):
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == RX_BPMH_HELD
    assert store.read("plan::supplements", root=tmp_path) == []
    # cross-stream: the peptide (no operator-Rx match, declared no class) still records.
    assert out["results"]["peptides"]["recorded"] is True


def test_rx_bpmh_no_hold_without_operator_rx(tmp_path):
    # BACKWARD-COMPAT: a no-medication operator (no curated rx-interaction-classes item) -> no BPMH hold.
    store_read = _seed_store(tmp_path)  # no rx-interaction-classes seeded -> "" -> empty set
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["supplements"]["recorded"] is True
    assert out["reconciliation"]["rx_bpmh"] == []


def test_rx_bpmh_match_is_case_insensitive(tmp_path):
    store_read = _bpmh_store(tmp_path, "Bleeding-Risk")  # curated value normalizes to bleeding-risk
    out = generate_plans(_bpmh_supp_authors(["  BLEEDING-risk "]), store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["supplements"]["reason"] == RX_BPMH_HELD


def test_rx_bpmh_screens_peptides_too(tmp_path):
    # GENERALIZATION: the screen is symmetric — a PEPTIDE stacking against the operator's Rx is held
    # too (a peptide + anticoagulant is the same watchlist case as a supplement + anticoagulant).
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    authors = _compound_authors(
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    assert out["results"]["peptides"]["recorded"] is False
    assert out["results"]["peptides"]["reason"] == RX_BPMH_HELD
    assert {f["held_domain"] for f in out["reconciliation"]["rx_bpmh"]} == {"peptides"}


def test_rx_bpmh_liaison_override_releases_and_records(tmp_path):
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    assert out["results"]["supplements"]["recorded"] is True
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "cleared"
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_rx_bpmh_liaison_autoblock_keeps_held(tmp_path):
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=_liaison("CRITICAL"))
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == RX_BPMH_HELD
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "block-stands"


def test_rx_bpmh_liaison_vacuous_override_keeps_held(tmp_path):
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    liaison = _liaison("HIGH", override=_override_record("HIGH", operator_reason="trust me"))
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=liaison)
    assert out["results"]["supplements"]["recorded"] is False
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "block-stands"


def test_rx_bpmh_adjudicator_returning_none_keeps_held(tmp_path):
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=lambda finding: None)
    assert out["results"]["supplements"]["recorded"] is False
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "block-stands"


def test_rx_bpmh_adjudicator_not_called_without_match(tmp_path):
    store_read = _bpmh_store(tmp_path, "cyp3a4-pgp")  # operator on a class the supplement does not declare
    liaison = _liaison("MEDIUM")
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=liaison)
    assert out["results"]["supplements"]["recorded"] is True
    assert out["rx_bpmh_adjudications"] == {}
    assert liaison.calls == []


def test_rx_bpmh_safety_finding_id_and_caution(tmp_path):
    # The deterministic finding_id + caution the liaison echoes (sorted classes; verbatim caution).
    store_read = _bpmh_store(tmp_path, "bleeding-risk;cyp3a4-pgp")
    liaison = _liaison("MEDIUM")
    generate_plans(_bpmh_supp_authors(["cyp3a4-pgp", "bleeding-risk"]), store_read, tmp_path,
                   plan_date=PLAN_DATE, adjudicator=liaison)
    finding = next(c for c in liaison.calls if c["source"] == "rx-bpmh")
    assert finding["finding_id"] == "rx-bpmh:supplements:bleeding-risk;cyp3a4-pgp"
    assert finding["held_domain"] == "supplements"
    assert "bleeding-risk, cyp3a4-pgp" in finding["caution"]


# --- PF-S75-01 interaction probe: rx-bpmh COMPOSES with the other holds ----------
# A compound can carry several concurrent concerns (additive-AE + rx-bpmh + conflict). Each clears
# on its OWN adjudication; clearing one MUST NOT release a domain whose other concern is still open.
# (This is exactly the S74/S75 safety-design-hole class — probed at Tier-1, not left to Tier-3.)


def test_rx_bpmh_and_additive_ae_are_independent_holds(tmp_path):
    # The supplement is held by BOTH additive-AE (bleeding-risk shared with the peptide) AND rx-bpmh
    # (cyp3a4-pgp matches the operator's Rx). Clearing the additive-AE override must NOT release it
    # while the rx-bpmh concern is open — the SEC-1 analog.
    store_read = _bpmh_store(tmp_path, "cyp3a4-pgp")
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk", "cyp3a4-pgp"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    # additive-AE clears (MEDIUM), rx-bpmh blocks (CRITICAL): the supplement STAYS held.
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_selective_liaison({"additive-ae": "MEDIUM", "rx-bpmh": "CRITICAL"}))
    assert out["adjudication"]["outcome"] == "cleared"  # additive-AE DID clear
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False  # but the supplement is NOT released
    assert out["results"]["supplements"]["reason"] == RX_BPMH_HELD
    assert store.read("plan::supplements", root=tmp_path) == []


def test_rx_bpmh_cleared_but_additive_ae_keeps_held(tmp_path):
    # The reverse direction: rx-bpmh clears, additive-AE blocks -> still held (additive-AE open).
    store_read = _bpmh_store(tmp_path, "cyp3a4-pgp")
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk", "cyp3a4-pgp"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_selective_liaison({"additive-ae": "CRITICAL", "rx-bpmh": "MEDIUM"}))
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "cleared"
    assert out["adjudication"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == ADDITIVE_AE_HELD


def test_rx_bpmh_and_additive_ae_both_cleared_records(tmp_path):
    # Both concerns cleared -> the supplement records. (Proves the dual hold is RELEASABLE, not a deadlock.)
    store_read = _bpmh_store(tmp_path, "cyp3a4-pgp")
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk", "cyp3a4-pgp"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_selective_liaison({"additive-ae": "MEDIUM", "rx-bpmh": "MEDIUM"}))
    assert out["adjudication"]["outcome"] == "cleared"
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "cleared"
    assert out["results"]["supplements"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_rx_bpmh_and_conflict_are_independent_holds(tmp_path):
    # A supplement held by BOTH a cross-domain conflict AND rx-bpmh: clearing the conflict must NOT
    # release it while the rx-bpmh is open (the conflict_held x rx_bpmh_held interaction).
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    authors = _compound_authors(
        supp_recon={
            "conflicts": [{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"}],
            "ae_profile": {"additive_classes": ["bleeding-risk"]},
        },
    )
    # conflict clears (MEDIUM), rx-bpmh blocks (CRITICAL) -> still held.
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_selective_liaison({"cross-domain-conflict": "MEDIUM", "rx-bpmh": "CRITICAL"}))
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "cleared"
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "block-stands"
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == RX_BPMH_HELD


# --- AC4: real medical-liaison rxbp dispatch, captured + run through the production path ---------
# Two REAL captured envelopes adjudicating the SAME finding_id (rx-bpmh:supplements:bleeding-risk) to
# OPPOSITE outcomes on the specific medication — the BPMH gate's marquee clinical discrimination:
# aspirin (antiplatelet) -> HIGH/H3 overridable -> clears; warfarin (anticoagulant, narrow TI) ->
# CRITICAL/H2 -> non-overridable auto-block. Not stubs — captured out-of-band per the integration mandate.


def test_real_rx_bpmh_liaison_cleared_envelope_records(tmp_path):
    # The REAL aspirin+fish-oil envelope (HIGH/H3, content-valid HIGH-rung informed-refusal override),
    # run through the production path, RELEASES the BPMH-held supplement: it records.
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    env = _example_envelope("liaison-rxbp-cleared.example.json")
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=lambda finding: env)
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "cleared"
    assert out["results"]["supplements"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_real_rx_bpmh_liaison_blocked_envelope_keeps_held(tmp_path):
    # The REAL warfarin+fish-oil envelope (CRITICAL/H2 mechanical-auto-block, null override path), run
    # through the production path, KEEPS the supplement held — the marquee BPMH safety property: an
    # anticoagulant interaction is non-overridable, and the operator's informed-refusal does not lower it.
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    env = _example_envelope("liaison-rxbp-blocked.example.json")
    out = generate_plans(_bpmh_supp_authors(["bleeding-risk"]), store_read, tmp_path,
                         plan_date=PLAN_DATE, adjudicator=lambda finding: env)
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "block-stands"
    assert out["rx_bpmh_adjudications"]["supplements"]["non_overridable"] is True
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == RX_BPMH_HELD
    assert store.read("plan::supplements", root=tmp_path) == []


def test_rx_bpmh_additive_ae_and_conflict_all_three_independent(tmp_path):
    # PF-S75-01 triple-concern probe (QA Tier-2 SHOULD-FIX): ONE supplement held by ALL THREE concerns
    # at once — additive-AE (`holds`, shared bleeding-risk with the peptide), a cross-domain conflict
    # (`conflict_held`), AND rx-bpmh (`rx_bpmh_held`, cyp3a4-pgp matches the operator Rx). Clearing TWO
    # while the third is open must keep it held — the sequential recording-loop check past two cleared
    # concerns must not short-circuit. The supplement declares cyp3a4-pgp (operator-matched) PLUS
    # bleeding-risk (peptide-shared) so the three holds land on the one domain, isolated from the peptide.
    store_read = _bpmh_store(tmp_path, "cyp3a4-pgp")
    authors = _compound_authors(
        supp_recon={
            "conflicts": [{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"}],
            "ae_profile": {"additive_classes": ["bleeding-risk", "cyp3a4-pgp"]},
        },
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    # additive-AE + conflict CLEAR (MEDIUM), rx-bpmh BLOCKS (CRITICAL): the supplement STAYS held.
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_selective_liaison(
                             {"additive-ae": "MEDIUM", "cross-domain-conflict": "MEDIUM", "rx-bpmh": "CRITICAL"}))
    assert out["adjudication"]["outcome"] == "cleared"  # additive-AE cleared
    assert out["conflict_adjudications"]["supplements"]["outcome"] == "cleared"  # conflict cleared
    assert out["rx_bpmh_adjudications"]["supplements"]["outcome"] == "block-stands"  # rx-bpmh open
    assert out["results"]["supplements"]["recorded"] is False  # but the supplement is NOT released
    assert out["results"]["supplements"]["reason"] == RX_BPMH_HELD  # the still-open concern
    assert store.read("plan::supplements", root=tmp_path) == []


def test_rx_bpmh_additive_ae_and_conflict_all_three_cleared_records(tmp_path):
    # The releasable proof: with ALL THREE concerns cleared, the triple-held supplement records (not a deadlock).
    store_read = _bpmh_store(tmp_path, "cyp3a4-pgp")
    authors = _compound_authors(
        supp_recon={
            "conflicts": [{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"}],
            "ae_profile": {"additive_classes": ["bleeding-risk", "cyp3a4-pgp"]},
        },
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_selective_liaison(
                             {"additive-ae": "MEDIUM", "cross-domain-conflict": "MEDIUM", "rx-bpmh": "MEDIUM"}))
    assert out["results"]["supplements"]["recorded"] is True
    assert len(store.read("plan::supplements", root=tmp_path)) == 1


def test_rx_bpmh_peptide_hold_composes_with_additive_ae_supplement_hold(tmp_path):
    # QA Tier-2 SHOULD-FIX (multi-DOMAIN composition in one pass): the supplement is additive-AE-held
    # (`holds`) while the PEPTIDE is rx-bpmh-held (`rx_bpmh_held`) — distinct domains, distinct concerns,
    # each cleared on its own gate call. With no adjudicator BOTH stay held; the two independent sets do
    # not interfere across domains.
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    authors = _compound_authors(
        supp_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)
    # supplement: additive-AE held (shared bleeding-risk); also rx-bpmh-matches but additive-AE is the shown reason.
    assert out["results"]["supplements"]["recorded"] is False
    # peptide: rx-bpmh held (its bleeding-risk class matches the operator Rx) — held on its OWN concern.
    assert out["results"]["peptides"]["recorded"] is False
    assert out["results"]["peptides"]["reason"] == RX_BPMH_HELD
    assert {f["held_domain"] for f in out["reconciliation"]["rx_bpmh"]} == {"supplements", "peptides"}


def test_rx_bpmh_and_conflict_both_open_without_adjudicator_held(tmp_path):
    # TEST-rxbp-2 (Tier-3): a supplement held by BOTH an open conflict AND an open rx-bpmh match, with
    # NO adjudicator, stays held — pinning the recording loop's fixed precedence (holds -> conflict_held
    # -> rx_bpmh_held) so a reorder is a decision, not a silent change of the surfaced reason. Both
    # concerns are detected in their INDEPENDENT sets; conflict is surfaced as the reason (checked first).
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    authors = _compound_authors(
        supp_recon={
            "conflicts": [{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"}],
            "ae_profile": {"additive_classes": ["bleeding-risk"]},
        },
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE)  # no adjudicator
    assert out["results"]["supplements"]["recorded"] is False
    assert out["results"]["supplements"]["reason"] == CONFLICT_HELD  # precedence: conflict before rx-bpmh
    assert "supplements" in {f["held_domain"] for f in out["reconciliation"]["rx_bpmh"]}  # rx-bpmh detected too
    assert any(c["from"] == "supplements" for c in out["reconciliation"]["conflicts"])


# --- doctor-visit-queue collation (S77, the medical-liaison's owned collation surface) ----------
# collate_doctor_visit_queue reads a generate_plans result + records each ADJUDICATED safety finding
# (additive-AE / conflict / rx-bpmh; cleared-with-override OR block-stands) into the dvq::queue stream,
# severity-ranked on read. generate_plans itself is unchanged (the collation is a separate call).


def test_generate_plans_writes_no_queue_stream(tmp_path):
    # BACKWARD-COMPAT: generate_plans alone never writes the dvq:: stream (the collation is separate).
    store_read = _seed_store(tmp_path)
    generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    assert queue_schema.read_doctor_visit_queue(tmp_path) == []


def test_collate_records_cleared_additive_ae(tmp_path):
    # An additive-AE supplement cleared via a MEDIUM override -> one queue entry, the finding_id +
    # caution matching the adjudicated safety_finding verbatim (so the SBAR render reproduces it).
    store_read = _seed_store(tmp_path)
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    recorded = collate_doctor_visit_queue(out, PLAN_DATE, tmp_path)
    assert len(recorded) == 1
    queue = queue_schema.read_doctor_visit_queue(tmp_path)
    assert len(queue) == 1
    e = queue[0]
    assert e["axis"] == "additive-ae"
    assert e["finding_id"].startswith("additive-ae:")
    assert e["caution"].startswith("Supplement<->peptide additive")  # verbatim from the safety_finding
    assert e["outcome"] == "cleared-with-override"
    assert e["composite_band"] == "MEDIUM"
    assert e["non_overridable"] is False
    assert e["held_domain"] == "supplements"
    assert e["source_specialist"] == "supplement-specialist"


def test_collate_non_overridable_block_stands_entry(tmp_path):
    # A CRITICAL auto-block -> a block-stands entry flagged non_overridable (ranks highest for the MD).
    store_read = _seed_store(tmp_path)
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=_liaison("CRITICAL"))
    collate_doctor_visit_queue(out, PLAN_DATE, tmp_path)
    e = queue_schema.read_doctor_visit_queue(tmp_path)[0]
    assert e["outcome"] == "block-stands"
    assert e["non_overridable"] is True
    assert e["composite_band"] == "CRITICAL"


def test_collate_records_conflict_and_rx_bpmh(tmp_path):
    # A supplement that declares a conflict AND trips rx-bpmh (operator on the matching Rx class),
    # both adjudicated MEDIUM -> two queue entries (one per axis), both cleared.
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    authors = _compound_authors(
        supp_recon={
            "conflicts": [{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"}],
            "ae_profile": {"additive_classes": ["bleeding-risk"]},
        },
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    collate_doctor_visit_queue(out, PLAN_DATE, tmp_path)
    queue = queue_schema.read_doctor_visit_queue(tmp_path)
    axes = {e["axis"] for e in queue}
    assert "cross-domain-conflict" in axes and "rx-bpmh" in axes
    assert all(e["source_specialist"] == "supplement-specialist" for e in queue)


def test_collate_empty_without_adjudicator(tmp_path):
    # No adjudicator -> nothing reached the gate -> nothing adjudicated -> empty queue.
    store_read = _seed_store(tmp_path)
    out = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE)
    assert collate_doctor_visit_queue(out, PLAN_DATE, tmp_path) == []
    assert queue_schema.read_doctor_visit_queue(tmp_path) == []


def test_collate_severity_ranked_e2e(tmp_path):
    # E2E: a supplement held by additive-AE (CRITICAL auto-block) AND a conflict (MEDIUM cleared) ->
    # the queue surfaces the non-overridable auto-block FIRST (the MD-priority ordering).
    store_read = _seed_store(tmp_path)
    authors = _compound_authors(
        supp_recon={
            "conflicts": [{"with_domain": "peptides", "with": "bpc-157", "reason": "additive bleeding"}],
            "ae_profile": {"additive_classes": ["bleeding-risk"]},
        },
        pep_recon={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
    )
    out = generate_plans(authors, store_read, tmp_path, plan_date=PLAN_DATE,
                         adjudicator=_selective_liaison({"additive-ae": "CRITICAL", "cross-domain-conflict": "MEDIUM"}))
    collate_doctor_visit_queue(out, PLAN_DATE, tmp_path)
    queue = queue_schema.read_doctor_visit_queue(tmp_path)
    assert queue[0]["non_overridable"] is True  # the CRITICAL additive-AE auto-block leads
    assert queue[0]["axis"] == "additive-ae"
    assert any(e["axis"] == "cross-domain-conflict" and e["outcome"] == "cleared-with-override" for e in queue)


def test_real_liaison_collation_agrees_on_safety_tier_lead(tmp_path):
    # AC4: the REAL captured medical-liaison collation (doctor-visit-queue-collated.example.json) ranked
    # the non-overridable CRITICAL warfarin auto-block FIRST. The code's resolve_doctor_visit_queue
    # reproduces that SAFETY-TIER lead (the integration check). Intra-band the liaison refines clinically
    # (conflict above the generic additive-AE) while the code's tiebreak is deterministic finding_id —
    # the liaison's refinement is its dispatch-time judgment, not the data layer's, so only the
    # safety-critical lead is asserted equal here.
    collation = _example_envelope("doctor-visit-queue-collated.example.json")
    raw_entries = [
        {"finding_id": "additive-ae:class:bleeding-risk", "axis": "additive-ae",
         "caution": "Supplement<->peptide additive adverse-event risk (shared additive-AE classes: bleeding-risk)",
         "held_domain": "supplements", "source_specialist": "supplement-specialist",
         "outcome": "cleared-with-override", "non_overridable": False, "composite_band": "MEDIUM"},
        {"finding_id": "rx-bpmh:supplements:bleeding-risk", "axis": "rx-bpmh",
         "caution": "Supplement<->Rx BPMH interaction: supplements contributes additive-AE class(es) bleeding-risk that stack against the operator's present medication interaction class(es) bleeding-risk",
         "held_domain": "supplements", "source_specialist": "supplement-specialist",
         "outcome": "block-stands", "non_overridable": True, "composite_band": "CRITICAL"},
        {"finding_id": "conflict:supplements:peptides/bpc-157", "axis": "cross-domain-conflict",
         "caution": "Author-declared cross-domain conflict from supplements: bpc-157 (peptides) — additive bleeding risk, needs review",
         "held_domain": "supplements", "source_specialist": "supplement-specialist",
         "outcome": "cleared-with-override", "non_overridable": False, "composite_band": "MEDIUM"},
    ]
    for e in raw_entries:
        queue_schema.record_doctor_visit_queue_entry(e, PLAN_DATE, tmp_path)
    ranked = queue_schema.read_doctor_visit_queue(tmp_path)
    # the code leads with the non-overridable auto-block — matching the liaison's rank-1
    assert ranked[0]["finding_id"] == collation["ranked_finding_ids"][0] == "rx-bpmh:supplements:bleeding-risk"
    assert ranked[0]["non_overridable"] is True
    # the liaison rendered no clinical verdict (the queue is questions/observations for the doctor)
    assert collation["clinical_verdict_rendered"] is False
    # all three findings are present in the data-layer queue (none dropped)
    assert {e["finding_id"] for e in ranked} == set(collation["ranked_finding_ids"])


def test_collate_cumulative_latest_disposition_wins(tmp_path):
    # SHOULD-FIX-2 (Tier-2): re-collating the SAME finding on a LATER date supersedes its earlier
    # disposition through the collation path (block-stands at date 1 -> cleared at date 2 -> the queue
    # shows cleared). Pins latest-wins at the collation-integration level, not only the schema layer.
    store_read = _seed_store(tmp_path)
    blocked = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=_liaison("CRITICAL"))
    collate_doctor_visit_queue(blocked, "2026-06-19", tmp_path)
    assert queue_schema.read_doctor_visit_queue(tmp_path)[0]["outcome"] == "block-stands"
    cleared = generate_plans(_held_pair(), store_read, tmp_path, plan_date=PLAN_DATE, adjudicator=_liaison("MEDIUM"))
    collate_doctor_visit_queue(cleared, "2026-06-20", tmp_path)  # later date, same finding_id
    queue = queue_schema.read_doctor_visit_queue(tmp_path)
    assert len(queue) == 1  # one finding, the latest record wins
    assert queue[0]["outcome"] == "cleared-with-override"  # the 06-20 cleared disposition supersedes
