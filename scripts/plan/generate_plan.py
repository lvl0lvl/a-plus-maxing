"""Plan-generation production caller — wires author → assemble → store → render.

This is `assemble`'s production caller (the PF-S63-02 core-capability proof). Under the
runtime-A interactive agent-dispatch model (`vault/design/plan-generation-pipeline-v1.md`),
the orchestrator dispatches a plan-author specialist over the de-identified
`router.summarize` summary plus the gated wiki, captures the author's structured output,
and feeds it here. This module then:

  1. derives the canonical summary from the store (`router.summarize`) — the one
     operator-state source, the 0-raw-PII boundary;
  2. wraps the captured author output as the `assemble` roster callable for the domain;
  3. runs `assemble` (the four safety filters — attribution, sourcing-completeness,
     population-mismatch, the fail-closed class-aware HALT filter) over the author's
     recommendations;
  4. translates the SURVIVING (non-struck) recommendations' domain payloads into the
     `plan_schema` domain plan; and
  5. records the plan via `record_plan` — the store write the dashboard plan zone reads.

It is GENERIC across the four plan-domain authors: a new author plugs in by (a) emitting
the universal recommendation contract below and (b) registering a per-domain translator in
`_PLAN_TRANSLATORS`. personal-trainer / workout is the first wired instance; the repeatable
process is documented at `docs/plan-generation/author-dispatch-process.md`.

Universal recommendation contract (what every author emits, what `assemble` filters)::

    {
      "claim": str,             # the recommendation as one sentence (HALT text-matching)
      "source": str,            # citation / wiki provenance (sourcing-completeness)
      "confidence_tier": str,   # evidence tier
      "reversibility": str,     # reversibility note
      "category": str,          # intervention-class (class-aware HALT)
      "grounding": str,         # optional "animal"/"in-vitro" -> population-mismatch flag
      "numbers": [...],         # optional; each carries units + reference_range
      "payload": {...},         # the domain-structured renderable content (per-domain shape)
    }

The author output ENVELOPE is `{"specialist": slug, "recommendations": [rec, ...]}`, or the
thin-library sentinel `{"thin_library": True, "specialist": slug}`.

Clearance gate (operator decision 3 — asymmetric downside): the workout translator drops
every load prescription unless `clearance_granted` is True (a real clinician clearance —
the LM-01 July-13 visit is the V1 unlock). Default-deny ships the deferred coaching state
(movement + sets/reps + cues, no external-load prescription). This is a LOAD-BEARING safety
gate, not defensive programming: the operator's documented recovery context makes shipping
an un-cleared load prescription asymmetrically harmful, so the gate is enforced mechanically
here in addition to the author honoring it (defense in depth), and it fails closed.

Per-domain translators (the small delta each author adds): workout is 1 rec -> 1 exercise;
nutrition AGGREGATES N recs -> one `{calorie_goal, macros, meals}` day plan; supplements is
1 rec -> 1 item; peptides records one compound regimen (the schema is single-compound — a
multi-compound stack is the deferred compound-band two-pass screen). A domain may also own a
pre-translation safety veto in `_DOMAIN_GATES` — nutrition owns the 0.5 critical-floor
RED-S / LEA screen (pipeline Phase 0.5), which short-circuits energy content to clinical-care
routing BEFORE translation when the operator's state trips it. The cross-compound
supplement<->peptide additive-AE screen and the nutrition->workout energy bounce are deferred
to the cross-domain layer (the step-4 reconciler) per the pipeline design.
"""

from scripts.plan import router
from scripts.plan.assemble import assemble
from scripts.store import plan_schema


def _author_callable(author_output):
    """Wrap a captured author output as an `assemble` roster specialist callable.

    Under runtime A the author already reasoned over the summary at dispatch time, so the
    callable returns the captured output verbatim — the `(domain, summary)` args `assemble`
    passes are ignored (the reasoning is not re-run in-process).

    Args:
        author_output (dict): The captured author envelope.

    Returns:
        (Callable) A `specialist(domain, summary) -> dict` returning the captured output.
    """
    def specialist(domain, summary):
        return author_output

    return specialist


def _surviving(recommendations):
    """The composed claims whose actionable content was NOT struck by the HALT filter.

    A struck claim (`actionable_content_struck`) had its actionable regimen suppressed by
    `assemble`'s fail-closed HALT filter; it must not be lifted back into a prescribed plan
    entry. Coverage-gap sections carry no recommendations and never reach here.
    """
    return [c for c in recommendations if not c.get("actionable_content_struck")]


def _to_workout_plan(recommendations, gates):
    """Translate surviving workout recommendations into a `plan_schema` workout plan.

    Each recommendation's `payload` is the exercise dict (`name` + `sets` required;
    `reps` / `detail` / `load` optional — the `plan_schema` workout schema). Unless a
    clinician clearance is granted, the `load` prescription is dropped from every exercise
    (the asymmetric-downside clearance gate) so the plan ships as deferred coaching, never
    an un-cleared load prescription.

    Args:
        recommendations (list): The assembled workout section's composed claims.
        gates (dict): Per-domain safety inputs; reads `clearance_granted` (default False).

    Returns:
        (dict | None) `{"exercises": [...]}` when >=1 surviving recommendation carries a
        usable exercise payload, else None (record nothing — the dashboard renders the
        honest no-plan state rather than a fabricated regimen).
    """
    clearance_granted = bool(gates.get("clearance_granted"))
    exercises = []
    for claim in _surviving(recommendations):
        payload = claim.get("payload")
        if not isinstance(payload, dict):
            continue
        exercise = dict(payload)
        if not clearance_granted:
            exercise.pop("load", None)
        exercises.append(exercise)
    if not exercises:
        return None
    return {"exercises": exercises}


RED_S_LEA_CLINICAL_ROUTING = "red-s-lea-clinical-routing"


def _to_nutrition_plan(recommendations, gates):
    """Aggregate surviving nutrition recommendations into a `plan_schema` nutrition plan.

    Unlike the 1:1 workout translator, nutrition AGGREGATES: the surviving recommendations
    compose one day plan. A recommendation's `payload` carries day targets (`calorie_goal`
    int, `macros` {protein, carbs, fat}, `water_l?`) and/or a single `meal` ({name, contents?,
    kcal?}); the day-target fields are taken from the surviving recommendation(s) carrying them
    (a later one supersedes) and each surviving `meal` accumulates. A plan needs day targets
    AND >=1 meal; if any is absent among the survivors (e.g. the energy-prescribing
    recommendation was struck), nothing is recorded — the honest no-plan state, never a
    fabricated regimen. Present-but-malformed fields pass through to `record_plan` and fail
    loud there.

    Args:
        recommendations (list): The assembled nutrition section's composed claims.
        gates (dict): Per-domain safety inputs (unused here; the RED-S/LEA critical-floor
            screen runs as a pre-translation veto in `_nutrition_safety_gate`).

    Returns:
        (dict | None) `{calorie_goal, macros, meals[, water_l]}` when the survivors compose a
        complete plan, else None.
    """
    calorie_goal = None
    macros = None
    water_l = None
    meals = []
    for claim in _surviving(recommendations):
        payload = claim.get("payload")
        if not isinstance(payload, dict):
            continue
        if "calorie_goal" in payload:
            calorie_goal = payload["calorie_goal"]
        if "macros" in payload:
            macros = payload["macros"]
        if "water_l" in payload:
            water_l = payload["water_l"]
        meal = payload.get("meal")
        if isinstance(meal, dict):
            meals.append(meal)
    if calorie_goal is None or macros is None or not meals:
        return None
    plan = {"calorie_goal": calorie_goal, "macros": macros, "meals": meals}
    if water_l is not None:
        plan["water_l"] = water_l
    return plan


def _to_supplements_plan(recommendations, gates):
    """Translate surviving supplement recommendations into a `plan_schema` supplements plan.

    1 recommendation -> 1 item: each surviving recommendation's `payload` is a supplement item
    ({name, dose, timing?} — the `plan_schema` supplements schema). Records nothing when no
    surviving recommendation carries a usable item payload (the honest no-plan state). The
    cross-compound additive-AE / supplement<->peptide interaction screen is the deferred
    compound-band step; each item here is single-domain filtered by `assemble`.

    Args:
        recommendations (list): The assembled supplements section's composed claims.
        gates (dict): Per-domain safety inputs (none for supplements in this slice).

    Returns:
        (dict | None) `{"items": [...]}` when >=1 surviving recommendation carries a usable
        item payload, else None.
    """
    items = []
    for claim in _surviving(recommendations):
        payload = claim.get("payload")
        if not isinstance(payload, dict):
            continue
        items.append(dict(payload))
    if not items:
        return None
    return {"items": items}


def _to_peptides_plan(recommendations, gates):
    """Translate the surviving peptide recommendation into a `plan_schema` peptides plan.

    The `plan_schema` peptides plan is a SINGLE compound regimen ({compound, dose, route,
    cycle_week?, cycle_length_weeks?, tags?, evidence?}); V1 records one compound per plan
    document (a multi-compound stack is the deferred compound-band two-pass screen, not a
    single-author plan). The first surviving recommendation's `payload` is the regimen; records
    nothing when none survives (the honest no-plan state). The author dispatch is briefed to
    return one compound for the plan.

    Args:
        recommendations (list): The assembled peptides section's composed claims.
        gates (dict): Per-domain safety inputs (none for peptides in this slice).

    Returns:
        (dict | None) The single-compound plan from the first surviving recommendation, else
        None.
    """
    for claim in _surviving(recommendations):
        payload = claim.get("payload")
        if isinstance(payload, dict):
            return dict(payload)
    return None


def _nutrition_safety_gate(recommendations, gates):
    """The nutrition 0.5 critical-floor RED-S / LEA screen — a pre-translation safety veto.

    Nutritionist-owned, non-overridable (pipeline Phase 0.5): a fail-safe RED-S / LEA /
    disordered-eating screen that runs BEFORE energy-prescribing content. When the operator's
    state trips the screen, all energy-deficit content short-circuits to clinical-care
    routing — mechanically, nutrition records no plan. The screen is operator-STATE driven (the
    orchestrator runs the Phase-0.5 screen and sets `gates["red_s_lea_screen"]` to `True` or
    `"tripped"`); `recommendations` is accepted for veto-hook uniformity. Defense in depth: the
    author also honors it at dispatch, and this fails closed.

    Args:
        recommendations (list): The assembled nutrition section's composed claims.
        gates (dict): Per-domain safety inputs; reads `red_s_lea_screen` (default clear).

    Returns:
        (str | None) The clinical-routing reason when the screen is tripped, else None.
    """
    if gates.get("red_s_lea_screen") in (True, "tripped"):
        return RED_S_LEA_CLINICAL_ROUTING
    return None


# domain -> translator(recommendations, gates) -> plan dict | None. A new plan-domain author
# wires in by adding its translator here (workout is 1:1; nutrition aggregates; supplements is
# 1 rec -> 1 item; peptides records one compound regimen).
_PLAN_TRANSLATORS = {
    "workout": _to_workout_plan,
    "nutrition": _to_nutrition_plan,
    "supplements": _to_supplements_plan,
    "peptides": _to_peptides_plan,
}

# domain -> safety veto(recommendations, gates) -> reason str | None. An OWNED pre-translation
# screen (pipeline Phase 0.5) that withholds the whole plan for safety, distinct from a coverage
# gap or empty authorship. nutrition owns the RED-S/LEA critical-floor screen.
_DOMAIN_GATES = {
    "nutrition": _nutrition_safety_gate,
}


def generate_plan(domain, author_output, store_read, root, *, plan_date, gates=None):
    """Run one plan-author's output through the safety filters and record the plan.

    The production caller of `assemble` (PF-S63-02). Derives the summary from the store,
    runs the author's recommendations through `assemble`'s four filters for `domain`, then
    translates the surviving recommendations into the domain plan and records it via
    `record_plan`. A coverage-gap section, or a section whose recommendations are all
    struck / payload-less, records NOTHING — the dashboard renders the honest no-plan state
    rather than a fabricated regimen.

    Args:
        domain (str): A `plan_schema.PLAN_DOMAINS` member with a registered translator.
        author_output (dict): The captured author envelope — `{"specialist": slug,
            "recommendations": [...]}` or the thin-library sentinel.
        store_read (Callable): The store read surface, instance-root pre-bound (the
            `router.summarize` caller contract — an unbound reader silently reads the
            wrong instance).
        root (str | Path): The store root the plan is recorded into.
        plan_date (str): The plan's YYYY-MM-DD date (date equality is the dashboard's
            today-resolution — record for the render date to surface as today's plan).
        gates (dict, optional): Per-domain safety inputs — `clearance_granted` (the workout
            load gate) and `red_s_lea_screen` (the nutrition RED-S/LEA critical-floor veto).
            Defaults to all-conservative.

    Returns:
        (dict) A result record: `domain`, `specialist`, `recorded` (bool), `plan`
        (dict | None), `section` (the assembled section), `reason` (str | None — the
        coverage-gap kind, a domain safety-veto reason (e.g. the RED-S/LEA clinical-routing
        short-circuit), or `no-actionable-recommendation` when nothing was recorded).

    Raises:
        KeyError: `domain` has no registered translator.
        ValueError: `record_plan` rejected the translated plan (a translator emitted a
            schema-nonconformant plan, or the author omitted attribution) — surfaced
            loud, never silently dropped.
    """
    if domain not in _PLAN_TRANSLATORS:
        raise KeyError(
            f"no plan translator for domain {domain!r}; known: {tuple(_PLAN_TRANSLATORS)}"
        )
    gates = gates or {}
    summary = router.summarize(store_read)
    roster = {domain: _author_callable(author_output)}
    section = assemble([domain], summary, roster)["sections"][0]
    specialist = section.get("specialist")

    if section.get("coverage_gap"):
        return {
            "domain": domain, "specialist": specialist, "recorded": False,
            "plan": None, "section": section, "reason": section["coverage_gap"],
        }

    domain_gate = _DOMAIN_GATES.get(domain)
    if domain_gate is not None:
        veto = domain_gate(section.get("recommendations", []), gates)
        if veto is not None:
            return {
                "domain": domain, "specialist": specialist, "recorded": False,
                "plan": None, "section": section, "reason": veto,
            }

    plan = _PLAN_TRANSLATORS[domain](section.get("recommendations", []), gates)
    if plan is None:
        return {
            "domain": domain, "specialist": specialist, "recorded": False,
            "plan": None, "section": section, "reason": "no-actionable-recommendation",
        }

    plan_schema.record_plan(domain, plan, plan_date, specialist, root)
    return {
        "domain": domain, "specialist": specialist, "recorded": True,
        "plan": plan, "section": section, "reason": None,
    }


def _self_test():
    """Run the wired path on a synthetic PII-free fixture and assert a plan renders.

    The mechanical core-capability gate's behavioral check (PF-S63-02): seeds a synthetic
    operator-state store, feeds a fixture author output through `generate_plan`, then
    renders the dashboard and asserts the workout card is populated from the recorded plan.
    Deterministic (no agent dispatch) so it runs in CI. Returns 0 on a wired path, 1 on any
    break.
    """
    import datetime
    import tempfile

    from scripts.generate import generate
    from scripts.store import keying, store

    fields = {
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
    }
    author_output = {
        "specialist": "personal-trainer",
        "recommendations": [
            {
                "claim": "rebuild a movement base with goblet squats before any loaded pattern",
                "source": "ACSM resistance-training guidelines 2024",
                "confidence_tier": "established",
                "reversibility": "fully reversible on discontinuation",
                "category": "training",
                "payload": {
                    "name": "Goblet squat", "sets": 3, "reps": "8-12",
                    "detail": "bodyweight or light; controlled tempo, full depth",
                    "load": "60% 1RM",  # struck by the clearance gate (no clearance yet)
                },
            },
        ],
    }
    plan_date = "2026-06-18"
    with tempfile.TemporaryDirectory() as tmp:
        for item, value in fields.items():
            store.append(
                item,
                {f: None for f in keying.LINE_FIELDS}
                | {"item": item, "timepoint": plan_date, "source": "intake", "value": value},
                root=tmp,
            )

        def store_read(item):
            return store.read(item, root=tmp)

        result = generate_plan(
            "workout", author_output, store_read, tmp,
            plan_date=plan_date, gates={"clearance_granted": False},
        )
        if not result["recorded"]:
            print(f"core-capability self-test FAIL: no plan recorded ({result['reason']})")
            return 1
        if any("load" in ex for ex in result["plan"]["exercises"]):
            print("core-capability self-test FAIL: load prescription shipped without clearance")
            return 1
        out = generate.run(
            "dashboard", _root=tmp, _out_dir=tmp,
            _today=datetime.date.fromisoformat(plan_date),
        )
        if "Goblet squat" not in out.read_text(encoding="utf-8"):
            print("core-capability self-test FAIL: dashboard did not render the recorded plan")
            return 1
    print("core-capability self-test PASS: author -> assemble -> record_plan -> dashboard wired")
    return 0


def main(argv=None):
    """CLI entry: `--self-test` runs the wired-path gate check.

    Interactive plan generation runs via the orchestrator (runtime A), not this CLI — the
    only CLI action is the deterministic self-test the mechanical core-capability gate calls.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Plan-generation production caller.")
    parser.add_argument(
        "--self-test", action="store_true",
        help="run the wired-path self-test (the core-capability gate's behavioral check)",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    parser.error("no action; use --self-test")


if __name__ == "__main__":
    import sys

    sys.exit(main())
