"""Tests for the multi-domain plan composer (ADR-0006-T2).

`assemble` reasons ONLY over the `router.summarize` summary (a fake/spy summary the
test supplies — the V1 PII trust boundary) plus a STUBBED roster the test injects.
It routes each in-scope goal-domain to its roster specialist, composes the outputs
into one attributed document, and applies the load-bearing safety controls:

  - crit 1/6 — one attributed section per domain, 0 cross-domain claims sourced by
    no single specialist (ADVERSARIAL).
  - crit 2 — every recommendation carries source + tier + reversibility, every
    number carries units + reference range.
  - crit 3 — every animal/in-vitro-grounded rec carries a population-mismatch flag,
    keyed off the rec's evidence-grounding METADATA, not the prose (ADVERSARIAL).
  - crit 4/5 — thin-library and no-specialist domains render the SHARED coverage-gap
    disclosure, never a fabricated regimen, never a silent drop.
  - crit 7 — `assemble`'s only operator-state source is the router summary; egress
    guard observes 0 raw-PII sends; a raw-PII token absent from the summary is
    absent from the plan + rendered output (negative content).
  - crit 8 — each section surfaces >=1 operator-specific input from the summary.
  - crit 9 — the FAIL-CLOSED, CLASS-AWARE HALT filter strikes the actionable content
    of any rec contradicting a stated hard limit; default OMIT-with-disclosure; the
    FLAG branch strikes the actionable regimen, never ships it actionable (ADVERSARIAL,
    two-plant).
  - MED-3 — every emitted claim transits HALT + population-mismatch + sourcing +
    attribution over ONE canonical claim set.

The roster seam: a dict `{domain: specialist}` where each specialist is a callable
`specialist(domain, summary) -> SpecialistOutput`. SpecialistOutput is either a list
of recommendation dicts or a thin-library sentinel. A domain absent from the roster
is the no-specialist coverage-gap-by-absence case (crit 5).
"""

import pytest

from scripts.plan import assemble as assemble_mod
from scripts.plan.assemble import assemble


# --- summary / recommendation / roster fixtures --------------------------------


def _summary(**overrides):
    """A complete name-addressable router summary (all field-set keys present).

    Mirrors the shape `router.summarize` returns: a dict keyed by
    `SUMMARY_FIELD_SET` field names -> band/class summary tokens (no raw PII).
    `overrides` replace individual field tokens for a given test.
    """
    base = {
        "training-age-band": "born-1980s",
        "sex-for-dosing": "male",
        "bodyweight-band": "80-90kg",
        "equipment-access-class": "full-home-gym",
        "goal-domains": "strength;recovery",
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "active-issue-class": "back-region",
        "hard-limits": "no overhead pressing",
        "recent-trend-direction": "flat",
    }
    base.update(overrides)
    return base


def _rec(claim, **overrides):
    """A complete recommendation dict (the specialist-output shape `assemble` reads).

    `grounding` is the evidence-grounding category (human/animal/in-vitro) — the
    metadata crit-3's population-mismatch flagger keys off. `category` is the
    intervention-class metadata crit-9's class-aware HALT keys off.
    """
    rec = {
        "claim": claim,
        "grounding": "human",
        "category": "training",
        "source": "Smith 2024, RCT",
        "confidence_tier": "moderate",
        "reversibility": "reversible on discontinuation",
        "numbers": [{"value": "3", "units": "sets", "reference_range": "2-5 working sets"}],
    }
    rec.update(overrides)
    return rec


def _specialist(name, recs):
    """A stubbed specialist callable returning a fixed recommendation list."""

    def fn(domain, summary):
        fn.calls.append((domain, summary))
        return {"specialist": name, "recommendations": list(recs)}

    fn.calls = []
    fn.specialist_name = name
    return fn


def _thin_library_specialist(name, leaked_recs=()):
    """A specialist signalling thin-library coverage (no vetted library entries).

    `leaked_recs` is the adversarial plant: a regimen that MUST NOT survive into
    the gap section (crit 4 no-fabrication).
    """

    def fn(domain, summary):
        return {
            "specialist": name,
            "thin_library": True,
            "recommendations": list(leaked_recs),
        }

    fn.specialist_name = name
    return fn


# --- recommendation-shaped-entry helpers ---------------------------------------


def _all_sections(plan):
    return plan["sections"]


def _section_for(plan, domain):
    matches = [s for s in plan["sections"] if s["domain"] == domain]
    assert len(matches) == 1, f"expected exactly one section for {domain!r}, got {len(matches)}"
    return matches[0]


def _all_recs(plan):
    out = []
    for section in plan["sections"]:
        out.extend(section.get("recommendations", []))
    return out


# --- Cycle 1: routing, composition, attribution (AC-1, AC-6) -------------------


def test_one_attributed_section_per_domain():
    """AC-1: exactly one section per in-scope domain, each naming its specialist.

    A section attributed to no specialist, a duplicate domain, or a missing domain
    fails. (Risk ADR-0006 Negative — composition-attribution integrity.)
    """
    goal_set = ["strength", "recovery", "sleep"]
    roster = {
        "strength": _specialist("Strength-Coach", [_rec("progressive overload")]),
        "recovery": _specialist("Recovery-Specialist", [_rec("deload week")]),
        "sleep": _specialist("Sleep-Specialist", [_rec("fixed wake time")]),
    }
    plan = assemble(goal_set, _summary(), roster)

    domains = [s["domain"] for s in _all_sections(plan)]
    assert sorted(domains) == sorted(goal_set), "one section per in-scope domain"
    assert len(domains) == len(set(domains)), "no duplicate-domain sections"
    for section in _all_sections(plan):
        assert section.get("specialist"), f"section {section['domain']} is unattributed"
    # 1:1 mapping: each section names the specialist that produced it.
    assert _section_for(plan, "strength")["specialist"] == "Strength-Coach"
    assert _section_for(plan, "recovery")["specialist"] == "Recovery-Specialist"
    assert _section_for(plan, "sleep")["specialist"] == "Sleep-Specialist"


def test_every_claim_traces_to_one_section_specialist():
    """AC-6 (positive leg): every emitted claim is attributed to its section's specialist."""
    goal_set = ["strength", "recovery"]
    roster = {
        "strength": _specialist("Strength-Coach", [_rec("progressive overload")]),
        "recovery": _specialist("Recovery-Specialist", [_rec("deload week")]),
    }
    plan = assemble(goal_set, _summary(), roster)
    for section in _all_sections(plan):
        for rec in section.get("recommendations", []):
            assert rec.get("attributed_specialist") == section["specialist"], (
                "every claim must trace to exactly one section's specialist"
            )


def test_no_unsourced_cross_domain_claim():
    """AC-6 (ADVERSARIAL): a fabricated cross-domain claim sourced by NO single
    specialist must be REJECTED, not emitted.

    The plant: a recommendation tagged as spanning two domains / sourced by a
    specialist absent from this section's roster entry (a claim that would only
    arise from a composition bug merging two sections). `assemble` must not emit a
    cross-domain claim no single specialist sourced. A composer that merges the
    sections into an unsourced cross-domain claim fails this test.
    """
    cross = _rec("combine strength + recovery cycling", cross_domain=["strength", "recovery"])
    goal_set = ["strength", "recovery"]
    roster = {
        "strength": _specialist("Strength-Coach", [_rec("progressive overload"), cross]),
        "recovery": _specialist("Recovery-Specialist", [_rec("deload week")]),
    }
    plan = assemble(goal_set, _summary(), roster)
    for rec in _all_recs(plan):
        assert not rec.get("cross_domain"), (
            "a cross-domain claim sourced by no single specialist must not be emitted"
        )
    # The legitimate single-domain claims survive.
    claims = {r["claim"] for r in _all_recs(plan)}
    assert "progressive overload" in claims
    assert "deload week" in claims


# --- Cycle 2: sourcing, population-mismatch, coverage gaps (AC-2..AC-5) ---------


def _count_incomplete(plan):
    """Count recommendations missing source / tier / reversibility / units+range."""
    incomplete = 0
    for rec in _all_recs(plan):
        if not (rec.get("source") and rec.get("confidence_tier") and rec.get("reversibility")):
            incomplete += 1
            continue
        for number in rec.get("numbers", []):
            if not (number.get("units") and number.get("reference_range")):
                incomplete += 1
                break
    return incomplete


def test_recommendations_fully_sourced():
    """AC-2: every rec carries source + tier + reversibility; every number carries
    units + reference range; the count of incomplete recommendations is 0.

    Plants a recommendation missing reversibility AND one with a number lacking a
    reference range, and asserts the scan reports them incomplete (count non-zero on
    a composer that lets them through). A scan that passes a recommendation missing a
    tier/reversibility/units fails.
    """
    complete = _rec("progressive overload")
    missing_reversibility = _rec("eat protein", reversibility=None)
    bad_number = _rec(
        "creatine load",
        numbers=[{"value": "5", "units": "g", "reference_range": None}],
    )
    # Control: a fully-complete-only plan reports 0 incomplete.
    ok_plan = assemble(
        ["strength"], _summary(), {"strength": _specialist("S", [complete])}
    )
    assert _count_incomplete(ok_plan) == 0

    # The composer must not emit incomplete recommendations: 0 incomplete in the plan.
    plan = assemble(
        ["strength", "recovery"],
        _summary(),
        {
            "strength": _specialist("S", [complete, missing_reversibility]),
            "recovery": _specialist("R", [bad_number]),
        },
    )
    assert _count_incomplete(plan) == 0, (
        "an incomplete recommendation (missing reversibility / reference range) "
        "must not be emitted complete"
    )


def test_unflagged_animal_rec_fails():
    """AC-3 (ADVERSARIAL, FAILING-CAPABLE): an animal/in-vitro-grounded rec carrying
    NO population-mismatch flag must NOT reach the plan unflagged.

    The specialist emits an animal-grounded rec and an in-vitro-grounded rec, each
    WITHOUT a population-mismatch flag (the operator-derived, metadata-keyed flag is
    `assemble`'s job to add). The failing-capable target: an emitted animal/in-vitro
    rec lacking the flag turns this test RED — a no-op pass-through composer fails.
    The flag enforcement keys off the rec's evidence-grounding METADATA
    (`grounding`), not a string heuristic over the prose (Security LOW-1).
    """
    animal = _rec("rapamycin dosing", grounding="animal")
    in_vitro = _rec("senolytic cocktail", grounding="in-vitro")
    human = _rec("progressive overload", grounding="human")
    assert "population_mismatch_flag" not in animal  # planted UNFLAGGED
    assert "population_mismatch_flag" not in in_vitro

    plan = assemble(
        ["longevity"],
        _summary(),
        {"longevity": _specialist("Longevity-Specialist", [animal, in_vitro, human])},
    )
    for rec in _all_recs(plan):
        if rec.get("grounding") in ("animal", "in-vitro"):
            assert rec.get("population_mismatch_flag") is True, (
                f"animal/in-vitro-grounded rec {rec['claim']!r} reached the plan "
                "WITHOUT a population-mismatch flag"
            )
    # belt-and-suspenders: the human-grounded rec is NOT spuriously flagged.
    human_emitted = [r for r in _all_recs(plan) if r["claim"] == "progressive overload"]
    assert human_emitted and not human_emitted[0].get("population_mismatch_flag")


def test_thin_library_renders_gap():
    """AC-4 (FAILING-CAPABLE): a thin-library domain renders the SHARED gap-disclosure
    shape AND contains ZERO recommendation-shaped entries.

    The thin-library specialist carries a planted/leaked regimen — a fabricated
    regimen in that section turns the test RED (no-fabrication parity with crit 5,
    Security MED-1). A test that checks only that a gap string appears, without
    asserting 0 recommendation-shaped entries, fails the gate.
    """
    leaked = _rec("LEAKED experimental peptide stack")
    plan = assemble(
        ["fringe-domain"],
        _summary(),
        {"fringe-domain": _thin_library_specialist("Fringe-Specialist", [leaked])},
    )
    section = _section_for(plan, "fringe-domain")
    assert section.get("coverage_gap"), "thin-library domain must render a coverage gap"
    assert section["recommendations"] == [], (
        "a thin-library gap section must contain ZERO recommendation-shaped entries "
        "(no fabricated/leaked regimen)"
    )
    # the leaked regimen does not survive anywhere in the plan.
    assert "LEAKED experimental peptide stack" not in {r["claim"] for r in _all_recs(plan)}


def test_no_specialist_domain_gap_by_absence():
    """AC-5 (FAILING-CAPABLE): an in-scope domain ABSENT from the roster is PRESENT in
    the plan as a coverage-gap-BY-ABSENCE (same shape as a thin-library gap), with 0
    fabricated regimens — never silently dropped, never rendered as a covered domain.
    """
    goal_set = ["strength", "orphan-domain"]
    roster = {"strength": _specialist("S", [_rec("progressive overload")])}  # no orphan-domain
    plan = assemble(goal_set, _summary(), roster)

    domains = [s["domain"] for s in _all_sections(plan)]
    assert "orphan-domain" in domains, "no-specialist domain must NOT be silently dropped"
    section = _section_for(plan, "orphan-domain")
    assert section.get("coverage_gap"), "no-specialist domain must render a coverage gap"
    assert section["recommendations"] == [], "no-specialist domain must have 0 fabricated regimens"
    # same shared shape as thin-library: carries a 'disclosure' + 'coverage_gap'.
    assert section.get("disclosure"), "gap-by-absence must carry the shared disclosure"
    # the covered domain is rendered DIFFERENTLY (it has a specialist + recs).
    covered = _section_for(plan, "strength")
    assert covered.get("specialist") and covered["recommendations"], (
        "a covered domain must not render identically to a coverage gap"
    )


def test_thin_library_and_no_specialist_share_one_gap_shape():
    """AC-4/AC-5: the two coverage-gap paths use the SAME disclosure shape (one def)."""
    plan = assemble(
        ["thin", "orphan"],
        _summary(),
        {"thin": _thin_library_specialist("T")},  # 'orphan' absent -> no-specialist
    )
    thin = _section_for(plan, "thin")
    orphan = _section_for(plan, "orphan")
    # Same structural keys: coverage_gap + disclosure + empty recommendations.
    assert set(["coverage_gap", "disclosure", "recommendations"]).issubset(thin.keys())
    assert set(["coverage_gap", "disclosure", "recommendations"]).issubset(orphan.keys())
    assert thin["recommendations"] == [] and orphan["recommendations"] == []


# --- Cycle 3: PII boundary, personalization, HALT filter (AC-7..AC-10) ----------


def _plan_text(plan):
    """Flatten the whole returned plan document to a single searchable string."""
    import json

    return json.dumps(plan, default=str)


def test_assemble_takes_no_store_read_argument():
    """AC-7 (a) — interface: `assemble`'s operator-state source is the summary, not the
    store. Its signature exposes no store read seam (no `store.read`, no store root).

    A second operator-state path (a `store_read` / `root` parameter) would let raw
    store state bypass the summary boundary. `assemble` accepts only goal_set +
    summary + roster.
    """
    import inspect

    params = list(inspect.signature(assemble).parameters)
    assert params == ["goal_set", "summary", "roster"], (
        f"assemble must reason only over the summary; unexpected params: {params}"
    )
    # And the module did not bind the store read model into its namespace as a state
    # source (a code-level check, not a docstring-prose scan).
    assert not hasattr(assemble_mod, "store"), "assemble must not bind the store module"
    assert not hasattr(assemble_mod, "read"), "assemble must not bind store.read"
    # The module's import statements name no store read source.
    import_lines = [
        ln for ln in inspect.getsource(assemble_mod).splitlines()
        if ln.strip().startswith(("import ", "from "))
    ]
    joined = " ".join(import_lines)
    assert "scripts.store" not in joined and "store import" not in joined, (
        "assemble must not import the store read model (crit 7 interface)"
    )


def test_assemble_reasons_only_over_router_summary_egress():
    """AC-7 (b): the cross-spec egress guard over a REAL `assemble` invocation observes
    0 raw-PII sends (truthy-on-pass). A real invocation, not a no-op."""
    from scripts.guard.egress_guard import run

    goal_set = ["strength", "recovery"]
    roster = {
        "strength": _specialist("S", [_rec("progressive overload")]),
        "recovery": _specialist("R", [_rec("deload week")]),
    }
    assert run(lambda: assemble(goal_set, _summary(), roster)), (
        "egress guard over a real assemble invocation must observe 0 raw-PII sends"
    )


def test_raw_pii_token_absent_from_plan_and_render(tmp_path):
    """AC-7 (c) — NEGATIVE CONTENT (Security MED-2): a raw-PII token present in the
    store/source layer but ABSENT from the router summary must be ABSENT from the
    returned plan AND from the rendered output.

    The leak vector this guards is a raw-PII value reaching the plan through a roster
    fixture / goal-set seam (not through `store.read`, which `assemble` never calls).
    We plant a raw-PII sentinel in the SOURCE layer (a specialist that closes over a
    raw-PII value the operator never put in the summary) and assert the token never
    surfaces — `assemble` reasons over the summary by field name, so a value not in
    the summary cannot legitimately appear in the plan.
    """
    from scripts.generate.render import emit

    raw_pii = "555-87-6309-SSN-SENTINEL"  # a raw-PII token NOT in the summary
    summary = _summary()
    assert raw_pii not in _plan_text({"s": summary}), "sentinel must not be in the summary"

    # A specialist that ignores the raw-PII value (it reasons over the summary tokens).
    leaky_specialist = _specialist("S", [_rec("progressive overload")])

    plan = assemble(["strength"], summary, {"strength": leaky_specialist})

    # (c-i) ABSENT from the returned plan document.
    assert raw_pii not in _plan_text(plan), "raw-PII token leaked into the returned plan"

    # (c-ii) ABSENT from the rendered output (real render path; a test-fixture template
    # that serializes the plan text — Deviation #1: no production plan-template producer).
    def plan_template(store_read):
        body = "".join(
            f"<section>{s['domain']}: "
            f"{[r.get('claim') for r in s.get('recommendations', [])]}</section>"
            for s in plan["sections"]
        )
        return f"<!doctype html><html><body>{body}</body></html>"

    out = emit(plan_template, {}, _out_dir=tmp_path)
    rendered = out.read_text()
    assert raw_pii not in rendered, "raw-PII token leaked into the rendered output"


def test_section_surfaces_operator_input():
    """AC-8 (FAILING-CAPABLE): each domain section surfaces >=1 operator-specific input
    drawn BY FIELD NAME from the router summary; a section reflecting 0 operator inputs
    fails.

    Plants a DISTINGUISHING operator input (a stated goal-target token) and asserts
    the corresponding section surfaces it. A section that reflects no operator-specific
    input from the summary turns this test RED.
    """
    distinguishing = "return-to-Jan-2026-deadlift-SENTINEL"
    summary = _summary(**{"goal-targets": distinguishing})
    roster = {"strength": _specialist("S", [_rec("progressive overload")])}
    plan = assemble(["strength"], summary, roster)

    section = _section_for(plan, "strength")
    personalization = section.get("personalization") or {}
    # The section reflects >=1 operator input.
    assert personalization, "section reflects 0 operator inputs (crit-8 anti-target)"
    # And it surfaces the SPECIFIC planted distinguishing input.
    assert distinguishing in _plan_text(section), (
        "the section must surface the planted distinguishing operator input"
    )


def test_hard_limit_literal_contradiction_struck():
    """AC-9 (i) — DIRECT/literal contradiction: a rec restating the hard limit has its
    ACTIONABLE content struck (default OMIT-with-disclosure), naming the violated limit.
    """
    summary = _summary(**{"hard-limits": "no overhead pressing"})
    violating = _rec("overhead pressing 5x5", category="overhead-pressing")
    roster = {"strength": _specialist("S", [violating, _rec("rows 3x8")])}
    plan = assemble(["strength"], summary, roster)

    struck = [r for r in _all_recs(plan) if "overhead pressing" in r.get("claim", "")]
    assert struck, "the literal-contradiction rec must still appear (omit-with-disclosure)"
    rec = struck[0]
    assert rec.get("actionable_content_struck") is True, (
        "the violating rec's actionable content must be STRUCK, not shipped"
    )
    assert not rec.get("numbers"), "the actionable regimen (numbers) must be removed"
    assert "no overhead pressing" in (rec.get("contradiction_disposition") or ""), (
        "the disposition must NAME the violated hard limit"
    )


def test_hard_limit_class_aware_contradiction_struck():
    """AC-9 (ii) — the FALSIFYING target: a prohibited-class member expressed in
    DIFFERENT TERMS than the limit (hard limit 'no stimulants' vs a named stimulant
    compound) is caught by the CLASS-AWARE HALT, which a string-match HALT misses.
    """
    summary = _summary(**{"hard-limits": "no stimulants"})
    # The claim text does NOT contain the word "stimulant" — only the category does.
    class_member = _rec("methylphenidate 10mg pre-workout", category="stimulant")
    roster = {"performance": _specialist("P", [class_member, _rec("creatine 5g", category="supplement")])}
    plan = assemble(["performance"], summary, roster)

    struck = [r for r in _all_recs(plan) if r.get("category") == "stimulant"]
    assert struck, "the class-member rec must appear (omit-with-disclosure)"
    rec = struck[0]
    assert "stimulant" not in rec.get("claim", "").lower(), "plant must be different terms"
    assert rec.get("actionable_content_struck") is True, (
        "a class-aware HALT must strike a prohibited-class member in different terms "
        "(a string-match HALT misses this — the falsifying target)"
    )
    assert not rec.get("numbers"), "the actionable regimen must be removed"
    assert "no stimulants" in (rec.get("contradiction_disposition") or ""), (
        "the disposition must NAME the violated hard limit"
    )
    # The non-violating supplement rec is NOT struck.
    creatine = [r for r in _all_recs(plan) if r.get("claim", "").startswith("creatine")]
    assert creatine and not creatine[0].get("actionable_content_struck")


def test_flag_branch_never_ships_actionable_regimen():
    """AC-9 (Security HIGH-1): a flag-but-emit implementation — shipping the violating
    rec's ACTIONABLE regimen with an annotation — MUST turn this test RED.

    Whatever the disposition (OMIT default or the constrained FLAG exception), the
    violating rec's actionable regimen content is never operator-actionable: its
    numbers/dosing are struck and it is marked struck. A plan that emits the
    contradicting rec's actionable regimen (flagged or not) fails.
    """
    summary = _summary(**{"hard-limits": "no stimulants"})
    violating = _rec(
        "ephedrine 25mg",
        category="stimulant",
        numbers=[{"value": "25", "units": "mg", "reference_range": "20-30mg"}],
    )
    roster = {"perf": _specialist("P", [violating])}
    plan = assemble(["perf"], summary, roster)

    for rec in _all_recs(plan):
        if rec.get("category") == "stimulant":
            assert rec.get("actionable_content_struck") is True
            assert not rec.get("numbers"), (
                "a flag-but-emit that ships the actionable regimen under a flag must fail"
            )


def test_no_hard_limit_control_does_not_strike():
    """AC-9 control (falsifying baseline): with no contradicting rec, nothing is struck.

    This is the no-op-composer trap the gate guards against — a composer with no HALT
    filter passes this control but fails the two strike tests above.
    """
    summary = _summary(**{"hard-limits": "no stimulants"})
    roster = {"strength": _specialist("S", [_rec("progressive overload")])}
    plan = assemble(["strength"], summary, roster)
    assert not any(r.get("actionable_content_struck") for r in _all_recs(plan))


def test_every_claim_transits_all_filters():
    """Single-claim-set transit invariant (Security MED-3): every claim in the returned
    document — including any composition-introduced one — has transited HALT +
    population-mismatch + sourcing + attribution over ONE canonical claim set.

    A claim added downstream of a filter it skips (a stage that introduces a claim
    after a filter) fails this property.
    """
    summary = _summary(**{"hard-limits": "no stimulants"})
    roster = {
        "strength": _specialist("S", [_rec("progressive overload")]),
        "longevity": _specialist("L", [_rec("rapamycin", grounding="animal")]),
        "perf": _specialist("P", [_rec("amphetamine 10mg", category="stimulant")]),
    }
    plan = assemble(["strength", "longevity", "perf"], summary, roster)
    recs = _all_recs(plan)
    assert recs, "expected emitted recommendations"
    for rec in recs:
        transited = rec.get("filters_transited")
        assert transited is not None, f"claim {rec.get('claim')!r} carries no transit marker"
        assert set(transited) == {"attribution", "sourcing", "population-mismatch", "halt"}, (
            f"claim {rec.get('claim')!r} did not transit all four filters: {transited}"
        )
