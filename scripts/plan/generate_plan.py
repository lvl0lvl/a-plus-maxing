"""Plan-generation production caller — wires author → assemble → store → render.

This is `assemble`'s production caller (the PF-S63-02 core-capability proof). Under the
runtime-A interactive agent-dispatch model (`vault/design/plan-generation-pipeline-v1.md`),
the orchestrator dispatches a plan-author specialist over the identity-stripped
`context_assembler.assemble_context` record plus the gated wiki, captures the author's
structured output, and feeds it here. This module then:

  1. derives the identity-stripped operator-state record from the store
     (`context_assembler.assemble_context`, built on `router.summarize`'s identity-safe
     base) — the one operator-state source and the sole de-id control on the plan path;
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
multi-compound peptide stack within one plan is not supported here). A domain may also own a
pre-translation safety veto in `_DOMAIN_GATES` — nutrition owns the 0.5 critical-floor
RED-S / LEA screen (pipeline Phase 0.5), which short-circuits energy content to clinical-care
routing BEFORE translation when the operator's state trips it. The cross-compound
supplement<->peptide additive-AE screen and the nutrition->workout energy bounce are NOT
per-author concerns — they run in the cross-domain layer (the step-4 reconciler,
`scripts/plan/orchestrate.py`) per the pipeline design.
"""

from scripts.model.client import ModelCallError, ModelClient
from scripts.plan import context_assembler
from scripts.plan.assemble import assemble
from scripts.store import plan_schema

# The honest no-plan reason when the plan-author model call fails (ADR-0015 fail-closed,
# NFR-2): the client raised `ModelCallError`, so the plan is the honest no-plan state —
# never a fabricated or degraded regimen.
AUTHOR_CALL_FAILED = "author-call-failed"


class _FixedEnvelopeClient:
    """A client adapter that authors a fixed, pre-captured envelope.

    The backward-compatible path: a caller that already holds a captured author envelope
    (every existing `compute_plan`/`generate_plan` caller) is adapted into the client seam
    by returning the captured envelope from `author(domain, summary)`. New callers inject a
    real `ModelClient` whose `author` makes the programmatic no-train call (ADR-0015 H-1).

    Attributes:
        author_output (dict): The captured author envelope this adapter returns.
    """

    def __init__(self, author_output):
        self.author_output = author_output

    def author(self, domain, summary):
        return self.author_output


def _author_callable(client):
    """Wrap the model client as an `assemble` roster specialist callable.

    The plan-author envelope is PRODUCED by a programmatic call through the one model client
    (`scripts/model/client.py`'s `author(domain, summary)` — the ADR-0015 H-1 seam), over the
    de-identified `summary` `assemble` hands it. The captured-verbatim feed is retired: the
    envelope is now authored, not passed.

    Args:
        client: A model client exposing `author(domain, summary) -> envelope` (a real
            `ModelClient`, or the `_FixedEnvelopeClient` adapter for the captured-envelope
            path).

    Returns:
        (Callable) A `specialist(domain, summary) -> dict` that authors the envelope via
        `client.author`.
    """
    def specialist(domain, summary):
        return client.author(domain, summary)

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
        if meal is not None:  # present -> pass through; record_plan validates the shape (fail-loud)
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
    surviving recommendation carries a usable item payload (the honest no-plan state). Each item
    here is single-domain filtered by `assemble`; the cross-compound additive-AE /
    supplement<->peptide interaction screen runs in the cross-domain reconciler
    (`scripts/plan/orchestrate.py`), not this single-domain translator.

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
    document (a multi-compound peptide stack within one plan is not supported). The first
    surviving recommendation's `payload` is the regimen; records nothing when none survives (the
    honest no-plan state). The author dispatch is briefed to return one compound for the plan.
    The cross-domain supplement<->peptide additive-AE screen runs in the reconciler.

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

# domain -> safety veto(recommendations, gates) -> reason str | None. Every gate here MUST
# share that signature (the call site invokes them without per-domain branching). Use
# _DOMAIN_GATES for a pre-translation WHOLE-domain veto — a critical safety short-circuit that
# records no plan at all (e.g. nutrition's RED-S/LEA screen); use an in-translator check for
# per-rec suppression that still records a plan (e.g. workout's clearance gate dropping `load`).
_DOMAIN_GATES = {
    "nutrition": _nutrition_safety_gate,
}


def compute_plan(domain, author_output=None, store_read=None, *, gates=None, client=None):
    """Compute a domain's candidate plan WITHOUT recording it.

    Everything `generate_plan` does except the `record_plan` write: author the envelope
    through the one model client, derive the summary, run `assemble`'s four filters for
    `domain`, apply the domain safety veto + the coverage-gap check, and translate the
    surviving recommendations into the candidate plan. The cross-domain orchestrator
    (`scripts/plan/orchestrate.py`) computes every domain's candidate this way and reconciles
    them BEFORE recording (so a cross-domain check — the energy bounce, the RED-S/LEA
    short-circuit — can hold a plan from being written); the single-domain `generate_plan`
    records its candidate directly.

    The plan-author envelope is authored by a programmatic call through `client.author(domain,
    summary)` (the ADR-0015 H-1 seam — the one model boundary). A FAILED author call (the
    client's `ModelCallError` raise) yields the honest no-plan state (`reason ==
    AUTHOR_CALL_FAILED`), never a fabricated or degraded plan (NFR-2). When `client` is omitted,
    a `_FixedEnvelopeClient` over `author_output` is used — the captured-envelope path that
    every existing caller rides; a new caller injects a real `ModelClient`.

    Args:
        domain (str): A `plan_schema.PLAN_DOMAINS` member with a registered translator.
        author_output (dict, optional): The captured author envelope — `{"specialist": slug,
            "recommendations": [...]}` (optionally a top-level `reconciliation` dict
            carrying the cross-domain inputs) or the thin-library sentinel. The captured-path
            input; ignored when `client` is injected.
        store_read (Callable): The store read surface, instance-root pre-bound (the
            `router.summarize` caller contract — an unbound reader silently reads the
            wrong instance).
        gates (dict, optional): Per-domain safety inputs — `clearance_granted` (the workout
            load gate) and `red_s_lea_screen` (the nutrition RED-S/LEA critical-floor veto).
            Defaults to all-conservative.
        client (optional): A model client exposing `author(domain, summary) -> envelope`
            (a real `ModelClient`). When omitted, `author_output` is authored verbatim.

    Returns:
        (dict) `domain`, `specialist`, `plan` (dict | None — NOT yet recorded), `section`
        (the assembled section), `reason` (str | None — the coverage-gap kind, a domain
        safety-veto reason (the nutrition Phase-0.5 screen returns `RED_S_LEA_CLINICAL_ROUTING`
        == `'red-s-lea-clinical-routing'`), `no-actionable-recommendation`, or
        `AUTHOR_CALL_FAILED` when the author model call failed), and `meta` (the author's
        `reconciliation` inputs the reconciler reads — the workout energy cost, the nutrition
        energy-budget verdict, the compound additive-AE profile, author-declared conflicts —
        `{}` if none declared).

    Raises:
        KeyError: `domain` has no registered translator.
    """
    if domain not in _PLAN_TRANSLATORS:
        raise KeyError(
            f"no plan translator for domain {domain!r}; known: {tuple(_PLAN_TRANSLATORS)}"
        )
    gates = gates or {}
    client = client if client is not None else _FixedEnvelopeClient(author_output)
    # S2 precondition (LOW-2): `assemble_context` inherits `summarize`'s cwd-relative
    # `identity_config` default — correct when cwd == the instance root (the single-operator
    # deployment). A divergent-cwd caller must pass an instance-bound config (see the
    # `assemble_context` docstring); this is unchanged from the prior `summarize(store_read)`.
    summary = context_assembler.assemble_context(store_read)

    # Author the envelope through the one model client (H-1). A failed call (the typed
    # `ModelCallError`) is the honest no-plan state — never a fabricated/degraded plan
    # (ADR-0015 fail-closed): we record NOTHING and skip `assemble` entirely.
    try:
        envelope = _author_callable(client)(domain, summary)
    except ModelCallError:
        return {
            "domain": domain, "specialist": None, "plan": None,
            "section": None, "reason": AUTHOR_CALL_FAILED, "meta": {},
        }

    # The already-resolved `envelope` is replayed through a fixed adapter so `assemble`'s
    # roster re-invocation makes NO second model call (the one author call is above).
    roster = {domain: _author_callable(_FixedEnvelopeClient(envelope))}
    section = assemble([domain], summary, roster)["sections"][0]
    specialist = section.get("specialist")
    meta = {}
    if isinstance(envelope, dict) and isinstance(envelope.get("reconciliation"), dict):
        meta = dict(envelope["reconciliation"])

    def candidate(plan, reason):
        return {
            "domain": domain, "specialist": specialist, "plan": plan,
            "section": section, "reason": reason, "meta": meta,
        }

    # Phase-0.5 owned safety veto runs BEFORE any content evaluation (including coverage
    # gaps): a tripped critical-floor screen short-circuits to clinical-care routing
    # regardless of what the author produced, so the veto reason is preserved rather than
    # masked by a coincident coverage-gap kind.
    domain_gate = _DOMAIN_GATES.get(domain)
    if domain_gate is not None:
        veto = domain_gate(section.get("recommendations", []), gates)
        if veto is not None:
            return candidate(None, veto)

    if section.get("coverage_gap"):
        return candidate(None, section["coverage_gap"])

    plan = _PLAN_TRANSLATORS[domain](section.get("recommendations", []), gates)
    if plan is None:
        return candidate(None, "no-actionable-recommendation")
    return candidate(plan, None)


def generate_plan(domain, author_output=None, store_read=None, root=None, *,
                  plan_date, gates=None, client=None):
    """Run one plan-author's output through the safety filters and record the plan.

    The single-domain production caller of `assemble` (PF-S63-02): computes the candidate
    via `compute_plan` (author the envelope through the one model client -> summary ->
    `assemble`'s four filters -> domain veto / coverage-gap -> translate), then records it via
    `record_plan`. A coverage-gap section, a section whose recommendations are all struck /
    payload-less, OR a FAILED author model call records NOTHING — the dashboard renders the
    honest no-plan state rather than a fabricated regimen. The cross-domain orchestrator uses
    `compute_plan` + `record_plan` directly so reconciliation runs between the two.

    Args:
        domain (str): A `plan_schema.PLAN_DOMAINS` member with a registered translator.
        author_output (dict, optional): The captured author envelope — `{"specialist": slug,
            "recommendations": [...]}` or the thin-library sentinel. The captured-path input;
            ignored when `client` is injected.
        store_read (Callable): The store read surface, instance-root pre-bound (the
            `router.summarize` caller contract — an unbound reader silently reads the
            wrong instance).
        root (str | Path): The store root the plan is recorded into.
        plan_date (str): The plan's YYYY-MM-DD date (date equality is the dashboard's
            today-resolution — record for the render date to surface as today's plan).
        gates (dict, optional): Per-domain safety inputs — `clearance_granted` (the workout
            load gate) and `red_s_lea_screen` (the nutrition RED-S/LEA critical-floor veto).
            Defaults to all-conservative.
        client (optional): A model client exposing `author(domain, summary) -> envelope`
            (a real `ModelClient`). When omitted, `author_output` is authored verbatim.

    Returns:
        (dict) A result record: `domain`, `specialist`, `recorded` (bool), `plan`
        (dict | None), `section` (the assembled section), `reason` (str | None — the
        coverage-gap kind, the domain safety-veto reason, `no-actionable-recommendation`,
        or `AUTHOR_CALL_FAILED` when the author model call failed) when nothing was recorded.

    Raises:
        KeyError: `domain` has no registered translator.
        ValueError: `record_plan` rejected the translated plan (a translator emitted a
            schema-nonconformant plan, or the author omitted attribution) — surfaced
            loud, never silently dropped.
    """
    result = compute_plan(domain, author_output, store_read, gates=gates, client=client)
    recorded = result["plan"] is not None
    if recorded:
        plan_schema.record_plan(domain, result["plan"], plan_date, result["specialist"], root)
    return {
        "domain": domain, "specialist": result["specialist"], "recorded": recorded,
        "plan": result["plan"], "section": result["section"], "reason": result["reason"],
    }


def _self_test():
    """Run the wired path on a synthetic PII-free fixture and assert a plan renders.

    The mechanical core-capability gate's behavioral check (PF-S63-02): seeds a synthetic
    operator-state store, authors a fixture envelope through the one model client (a
    deterministic mock backend at the seam — no live agent dispatch, no live API), runs it
    through `generate_plan`, then renders the dashboard and asserts the workout card is
    populated from the recorded plan. Deterministic so it runs in CI. Returns 0 on a wired
    path, 1 on any break.

    Scope: this proves the SHARED path shape (author -> assemble -> record_plan -> render)
    via the workout instance — the infrastructure every domain rides. Per-domain translation
    + render coverage (nutrition / supplements / peptides) is held by the `tests/plan/` E2E
    suite, not duplicated into this gate.
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

        # The author output is produced THROUGH the one model client (ADR-0015 H-1) — a
        # deterministic mock backend at the seam, never a live agent dispatch or live API,
        # so the wired-path gate runs in CI.
        class _FixtureBackend:
            def author(self, domain, summary):
                return author_output

        result = generate_plan(
            "workout", None, store_read, tmp,
            plan_date=plan_date, gates={"clearance_granted": False},
            client=ModelClient(backend=_FixtureBackend()),
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
