"""The post-assembly plan-quality judge — the `gate_dispatch=` QUALITY gate (ADR-0023-T1).

`quality_judge(assembled_plan, judge_client)` is the producer-independent QUALITY gate the
orchestrator's `gate_dispatch=` seam dispatches over the assembled plan, between generation and
surfacing. It scores the assembled-plan dict (`{"sections": [...]}`, the `assemble`/
`run_generation` output) against `vault/design/plan-quality-rubric.md` via an INJECTED judge
client (a real model client in production, a fixture mock in tests — 0 live spend), and returns
an ACCEPT / REVISE verdict the gate seam reads.

It mirrors the judge-discipline produce->judge pattern: a fresh judge, ISOLATED from the
producer's self-assessment, scores the artifact against a rubric. The producer-independence
contract is load-bearing — the payload handed to the judge client carries the assembled plan +
the rubric ONLY; the specialists' self-assessments (`self_assessment` / `self_score`) and the
orchestrator's notes (`orchestrator_notes`) are STRIPPED, so the judge scores the artifact, not
the producer's claim about it.

It scores QUALITY (followability / coherence / internal consistency / completeness) — DISTINCT
from the clinical-SAFETY review (ADR-0024-T1), which screens clinical risk over the composed
plan. Both wire into the same `gate_dispatch=` seam; this judge has NO clinical-safety hold /
adjudication path. It WRAPS the assembled output; it edits no inner-engine module. The
`gate_dispatch=` seam invocation in `run_orchestrated`'s body, and the bounded revise loop the
REVISE verdict feeds, are ADR-0022-T2's (Wave 4), not this task's.
"""

from pathlib import Path

from scripts.plan import assemble

# The judge-discipline verdicts (Section 6). The gate seam reads ACCEPT vs REVISE; REJECT is
# reserved for the judge-discipline auto-fail short-circuit but folds to REVISE for the gate's
# binary ACCEPT/loop disposition (the revise loop, ADR-0022-T2, reads the verdict, not the label).
ACCEPT = "ACCEPT"
REVISE = "REVISE"

# The coverage-gap kinds `assemble._coverage_gap` emits for an in-scope domain with no vetted
# recommendation. The empty-output gap is the rubric's completeness/coherence auto-fail shape; the
# thin-library / no-specialist gaps are HONEST disclosures (a legible gap is not a quality defect).
_EMPTY_GAP_KINDS = (assemble.EMPTY_OUTPUT_GAP,)

# The four rubric dimensions (vault/design/plan-quality-rubric.md). The producer-independent
# rubric the judge scores against; a per-dimension score below this band is a deduction.
DIMENSIONS = ("followability", "coherence", "internal consistency", "completeness")

# The ACCEPT minimum band (judge-discipline default >=9): every dimension at or above this band
# AND no auto-fail fired yields ACCEPT; otherwise REVISE.
ACCEPT_MIN_BAND = 9

# The producer self-assessment / orchestrator-note fields STRIPPED from the judge payload (the
# producer-independence contract, AC-2). A judge fed these cannot be independent.
_PRODUCER_FIELDS = ("self_assessment", "self_score", "orchestrator_notes")

_RUBRIC_PATH = Path("vault/design/plan-quality-rubric.md")


def _strip_producer_fields(value):
    """Recursively drop the producer self-assessment / orchestrator-note keys from a structure.

    The producer-independence transform (AC-2): the judge payload carries the assembled plan +
    the rubric ONLY — never the specialists' self-assessments nor the orchestrator's notes. A
    deep strip so a self-score nested in any section is removed, not only a top-level one.
    """
    if isinstance(value, dict):
        return {
            k: _strip_producer_fields(v)
            for k, v in value.items()
            if k not in _PRODUCER_FIELDS
        }
    if isinstance(value, list):
        return [_strip_producer_fields(item) for item in value]
    return value


def _build_payload(assembled_plan):
    """Build the producer-independent judge payload: the stripped plan + the rubric.

    The payload the judge client scores: the assembled plan with every producer self-assessment
    and orchestrator note removed, plus the maintained rubric text. This is the ONLY thing the
    judge sees — the source of its independence.
    """
    return {
        "plan": _strip_producer_fields(assembled_plan),
        "rubric": _RUBRIC_PATH.read_text(encoding="utf-8"),
    }


def _empty_domain_deductions(sections):
    """Rubric auto-fail: an in-scope domain section with 0 actionable recommendations.

    Walks the sections for the `assemble._coverage_gap` empty-output shape (`coverage_gap ==
    EMPTY_OUTPUT_GAP`). The disclosure makes the gap HONEST, but an in-scope domain the specialist
    produced nothing actionable for is a followability + completeness quality defect — the plan
    goes to REVISE to fill it (re-dispatch), never ACCEPT. Anchored to the rubric's followability
    + completeness auto-fails, so the verdict cites the failing dimension.
    """
    deductions = []
    for section in sections:
        if not isinstance(section, dict):
            continue
        if section.get("coverage_gap") in _EMPTY_GAP_KINDS:
            domain = section.get("domain")
            for dim in ("followability", "completeness"):
                deductions.append({
                    "dimension": dim,
                    "reason": (
                        f"in-scope domain {domain!r} surfaced 0 actionable recommendations "
                        f"({section.get('coverage_gap')}) — auto-fail"
                    ),
                })
    return deductions


def _contradictory_target_deductions(sections):
    """Rubric auto-fail: two sections set mutually-contradictory targets for the same axis.

    A `target` reads `"<axis>: <value>"`. Two recommendations sharing an axis but asserting
    different values (e.g. `caloric-balance: surplus` vs `caloric-balance: deficit`) is an
    internal-consistency auto-fail — a plan the operator cannot follow without violating itself.
    Anchored to the rubric's internal-consistency auto-fail.
    """
    axis_values = {}  # axis -> set of asserted values (across all sections)
    for section in sections:
        if not isinstance(section, dict):
            continue
        for rec in (section.get("recommendations") or []):
            if not isinstance(rec, dict):
                continue
            target = rec.get("target")
            if not isinstance(target, str) or ":" not in target:
                continue
            axis, value = (part.strip() for part in target.split(":", 1))
            axis_values.setdefault(axis, set()).add(value)

    deductions = []
    for axis, values in axis_values.items():
        if len(values) > 1:
            deductions.append({
                "dimension": "internal consistency",
                "reason": (
                    f"mutually-contradictory targets for {axis!r}: "
                    f"{sorted(values)} — auto-fail"
                ),
            })
    return deductions


def _structural_deductions(plan):
    """The rubric-anchored structural auto-fails over the assembled plan (a defect -> REVISE).

    The quality-defect falsification floor: a seeded quality defect (an empty in-scope domain or
    mutually-contradictory cross-section targets) produces a deduction here regardless of the
    judge client's score, so a rubber-stamping model that returns all-clean scores cannot surface
    a defective plan as ACCEPT. Each deduction cites the rubric dimension it fails.
    """
    sections = plan.get("sections") or []
    return _empty_domain_deductions(sections) + _contradictory_target_deductions(sections)


def quality_judge(assembled_plan, judge_client):
    """Score an assembled plan for QUALITY against the rubric; return an ACCEPT/REVISE verdict.

    The producer-independent QUALITY gate (ADR-0023-T1): builds the producer-independent payload
    (the assembled plan stripped of self-assessment / orchestrator notes + the rubric), scores
    each rubric dimension via the injected judge client, and returns the verdict the gate seam
    reads. QUALITY only — no clinical-safety hold path (that is ADR-0024-T1).

    Args:
        assembled_plan (dict): The assembled plan `{"sections": [...]}` (the `assemble`/
            `run_generation` output) to score.
        judge_client: The injected judge client — `judge(payload) -> {dimension: score}`. A real
            model client in production; a fixture mock in tests (0 live spend).

    Returns:
        (dict) The verdict `{"verdict": ACCEPT | REVISE, "dimensions": {dim: score}, "deductions":
        [{"dimension", "reason"}]}` — ACCEPT when every dimension is at the ACCEPT band and no
        auto-fail fired; REVISE otherwise, citing the failing dimension(s) the revise loop reads.
    """
    payload = _build_payload(assembled_plan)
    scores = judge_client.judge(payload)

    # The rubric-anchored structural auto-fails: a seeded quality defect (an empty in-scope domain
    # or contradictory cross-section targets) forces REVISE regardless of the judge client's
    # scores — so a rubber-stamping model returning all-clean scores cannot surface a defective
    # plan as ACCEPT (the AC-3 falsification floor).
    deductions = _structural_deductions(assembled_plan)
    deductions += [
        {"dimension": dim, "reason": f"{dim} scored {scores.get(dim)} (below the ACCEPT band)"}
        for dim in DIMENSIONS
        if scores.get(dim, 0) < ACCEPT_MIN_BAND
    ]

    verdict = ACCEPT if not deductions else REVISE
    return {"verdict": verdict, "dimensions": dict(scores), "deductions": deductions}
