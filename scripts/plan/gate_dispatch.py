"""The composed `gate_dispatch` adapter (ADR-0026-T2) — quality + safety -> the 3-key disposition.

`compose_gate_dispatch(judge_client, review_dispatch, *, lenses)` returns the single-arg
`gate_dispatch(assembled_plan) -> disposition` callable the ADR-0026-T1 shared driver
(`plan_driver.drive`) consumes via its `gate_dispatch=` seam. Over the assembled `run_generation`
result it runs BOTH built gate callables — `quality_judge` (the QUALITY gate, ADR-0023-T1) AND
`review_plan` (the SAFETY gate, ADR-0024-T1) — and maps their native shapes into EXACTLY the 3-key
disposition the driver's single-disposition read consumes:

    {accept: bool, safety_passed: bool, revise_domains: list}

  - `accept` = (`quality_judge`'s `verdict == ACCEPT`).
  - `safety_passed` = (`review_plan`'s `passed`, a bool) — boolean-`True` ONLY when `review_plan`
    returned a dict with `passed is True`. Every malformed composite (a raised / non-dict judge or
    review, a missing `verdict` / `passed` key) yields a `safety_passed` that is NOT boolean-True
    (FAIL-CLOSED), so the driver routes it to `SAFETY_BLOCKED`. The fail-closed default IS the
    contract — the composer NEVER emits `safety_passed: True` on anything but a positive review.
  - `revise_domains` = the run-set domains to re-author on a quality REVISE, per the derivation rule
    in `_revise_domains`. The keys are the EXACT three above — no more, no fewer (a richer shape
    breaks the driver's single-disposition read, OQ-2).

This is a Create-only ADAPTER over the built gate callables — it CONSUMES them and re-authors
nothing. The inner engine, `quality_judge`, `safety_review`, `plan_driver`, and `plan_orchestrator`
stay byte-unchanged; the composer wraps their outputs. The bound `judge_client` + `review_dispatch`
are the gates' collaborators (a fixture mock in tests, a real model/agent dispatch in production);
the returned callable closes over them so the driver's `gate_dispatch=` seam stays single-arg.
"""

from scripts.plan import quality_judge as quality_judge_mod
from scripts.plan import safety_review as safety_review_mod


def _run_set_domains(assembled_plan):
    """The plan domains the assembled `run_generation` result generated this run (the run-set).

    Reads the per-domain section keys off `results` — the same source `revise_domains` intersects
    with, so a derived target can never escape the run-set the driver's out-of-run-set guard checks.
    """
    if isinstance(assembled_plan, dict) and isinstance(assembled_plan.get("results"), dict):
        return [
            domain
            for domain, record in assembled_plan["results"].items()
            if isinstance(record, dict) and isinstance(record.get("section"), dict)
        ]
    return []


def _localized_revise_domains(assembled_plan):
    """The plan domains a STRUCTURAL (empty-domain) deduction localizes to via their sections.

    `quality_judge`'s deductions key on rubric DIMENSIONS, not plan DOMAINS, so the domain must come
    from the assembled result's sections — an in-scope domain whose section carries an empty-output
    coverage-gap (`assemble.EMPTY_OUTPUT_GAP`, the same shape `quality_judge._empty_domain_deductions`
    reads) is the structurally-localizable defect. A contradictory-target structural deduction is
    cross-section and does NOT localize to a single domain (it falls to the all-run-set fallback).
    """
    localized = []
    for domain in _run_set_domains(assembled_plan):
        section = assembled_plan["results"][domain]["section"]
        if section.get("coverage_gap") == quality_judge_mod.assemble.EMPTY_OUTPUT_GAP:
            localized.append(domain)
    return localized


def _revise_domains(verdict, assembled_plan):
    """Derive the run-set domains to re-author from a quality REVISE verdict (the AC-2 rule).

    The derivation rule (on a REVISE verdict; an ACCEPT carries no revise targets):
      1. Each STRUCTURAL (empty-domain) deduction localizes to its specific plan domain via the
         assembled result's section.
      2. Every OTHER deduction (a contradictory-target structural deduction, or a DIMENSION-level
         below-band deduction — neither localizing to a single domain) maps to ALL run-set domains
         (the conservative re-author fallback — NEVER a silent `[]` that would collapse the
         autonomous-revise leg).
      3. The result is INTERSECTED with the run-set domains (so `revise_domains` is a subset of the
         run-set — never an out-of-run-set target that trips the driver's guard).
    On a REVISE with no localizable domain, the fallback fills ALL run-set domains.

    Args:
        verdict (dict): The `quality_judge` verdict `{verdict, dimensions, deductions}`.
        assembled_plan (dict): The assembled `run_generation` result.

    Returns:
        (list) The run-set domains to re-author (a subset of the run-set; ordered by the run-set).
    """
    run_set = _run_set_domains(assembled_plan)
    localized = _localized_revise_domains(assembled_plan)
    # Compare the TOTAL deduction count against the EMPTY-DOMAIN deduction count (re-derived from
    # the SAME source `quality_judge` uses — `_empty_domain_deductions` emits TWO deductions per
    # empty-domain section, one per {followability, completeness}, so a localized-DOMAIN count
    # under-counts the deductions a single empty domain raises). A deduction beyond the structural
    # empty-domain set is non-localizing (a contradictory-target structural deduction or a
    # dimension-level below-band miss) -> all run-set; otherwise every REVISE-causing deduction is a
    # localizable empty-domain defect -> the specific localized domains.
    sections = [assembled_plan["results"][domain]["section"] for domain in run_set]
    empty_domain_deductions = quality_judge_mod._empty_domain_deductions(sections)
    if len(verdict["deductions"]) > len(empty_domain_deductions):
        targets = set(run_set)
    else:
        targets = set(localized)
    # Intersect with the run-set (subset guard) and order by the run-set for a stable result.
    return [domain for domain in run_set if domain in targets]


def compose_gate_dispatch(judge_client, review_dispatch, *,
                          lenses=safety_review_mod.DEFAULT_LENSES,
                          _quality_judge=quality_judge_mod.quality_judge,
                          _review=safety_review_mod.review_plan):
    """Compose the quality + safety gates into the driver's single-arg `gate_dispatch` callable.

    Binds the gates' collaborators (the `judge_client` and the review `dispatch` + `lenses`) and
    returns `gate_dispatch(assembled_plan) -> {accept, safety_passed, revise_domains}` — the EXACT
    3-key disposition the ADR-0026-T1 driver consumes. The returned callable runs BOTH gates over
    the assembled `run_generation` result and maps their native shapes, FAIL-CLOSED on any malformed
    composite (a raised / non-dict judge or review, a missing key never yields `safety_passed: True`).

    Args:
        judge_client: The injected QUALITY judge client — `judge(payload) -> {dimension: score}`. A
            real model client in production; a fixture mock in tests (0 live spend).
        review_dispatch (Callable): The injected SAFETY lens-dispatch seam,
            `dispatch(lens, prompt, assembled_plan) -> list of finding dicts`. A real agent dispatch
            in production; a fixture mock in tests.
        lenses (tuple, optional): The >=2 independent safety-lens roster forwarded to `review_plan`
            (which itself raises on <2 lenses). Defaults to `safety_review.DEFAULT_LENSES` (3 lenses).
        _quality_judge (Callable, optional): The QUALITY gate callable seam (defaults to the built
            `quality_judge.quality_judge`); a test-injection point, not a production override.
        _review (Callable, optional): The SAFETY gate callable seam (defaults to the built
            `safety_review.review_plan`); a test-injection point, not a production override.

    Returns:
        (Callable) The single-arg `gate_dispatch(assembled_plan) -> disposition` the driver consumes.
    """
    def gate_dispatch(assembled_plan):
        verdict = _quality_judge(assembled_plan, judge_client)
        review = _review(assembled_plan, review_dispatch, lenses=lenses)

        accept = isinstance(verdict, dict) and verdict.get("verdict") == quality_judge_mod.ACCEPT
        # FAIL-CLOSED: safety_passed is boolean-True ONLY when review_plan returned a dict whose
        # `passed` is boolean-True. A non-dict review or a missing `passed` key yields False.
        safety_passed = isinstance(review, dict) and review.get("passed") is True

        revise_domains = [] if accept else _revise_domains(verdict, assembled_plan)
        return {
            "accept": accept,
            "safety_passed": safety_passed,
            "revise_domains": revise_domains,
        }

    return gate_dispatch
