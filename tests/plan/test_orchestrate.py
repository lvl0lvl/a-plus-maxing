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

from scripts.generate import generate
from scripts.plan.generate_plan import RED_S_LEA_CLINICAL_ROUTING, compute_plan
from scripts.plan.orchestrate import (
    ADDITIVE_AE_HELD,
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
