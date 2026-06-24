"""Multi-agent whole-plan SAFETY review — the additive whole-plan safety layer.

A `/review-pr`-style multi-lens SAFETY review over the WHOLE assembled plan. `review_plan`
dispatches >=2 independent safety lenses (`medical-safety-reviewer`, `health-edge-case-reviewer`,
the `medical-liaison` as a whole-plan reviewer — all present in `.claude/agents/`, full profiles
inlined per INV-ROLE-INLINING) over the COMPOSED multi-domain plan (the `run_generation`-shaped
result), synthesizes + blind-triages their findings into one deduped set, reads the
already-adjudicated per-finding hold set off the result to EXCLUDE it (no double-gate, no gap),
and returns the synthesized finding set as the gate verdict — the legitimate findings that drive
a revise / a block.

This review WRAPS — it does NOT replace — the inner per-finding `adjudicate` gate. The inner gate
(`scripts/plan/adjudicate.py`, driven through `run_generation`'s `adjudicator` hook) SURVIVES
verbatim as the per-finding layer: it adjudicates INDIVIDUAL held findings one at a time (one
additive-AE, one cross-domain conflict, one Rx-BPMH at a time), never the assembled whole plan.
This tier is the ADDITIVE whole-plan layer that catches EMERGENT cross-domain issues no single
held finding represents — a cumulative stimulant/hepatic load summed across the workout +
nutrition + supplement + peptide domains, or a contraindication visible only when the four domains
are read together — issues the reconciler raises 0 holds for and the per-finding gate therefore
never sees. The two cover disjoint failure classes (per-finding vs whole-plan); neither makes the
other redundant. The lens reasoning is the dispatched lenses' (runtime A), never originated here;
the review adds NO override path of its own and re-authors nothing in `adjudicate` / the reconciler.

`review_plan` is the CALLABLE the orchestrator's `gate_dispatch=` seam targets (the SAFETY gate,
parallel to ADR-0023's quality gate). This module builds the callable + its behavior; the WIRING
of the gate into the orchestrator's loop control flow (calling it post-assembly, re-running it each
revise pass, treating a safety finding as BLOCKING/terminal) is ADR-0022-T2's job (the revise-loop
owner), NOT this module. It does NOT modify `plan_orchestrator.py`.

Gate-callable disposition key (API-02, a DECISION not a defect): this gate's disposition is read
off `passed` (bool); the quality gate's is read off `verdict` (ACCEPT/REVISE) — deliberately
distinct per ADR-0023/0024 (distinct gate semantics). ADR-0022-T2 (Wave 4) owns adapting each
verdict to the revise-loop's common disposition; this module emits its native verdict shape only.
"""

from scripts.plan.plan_orchestrator import _role_profile

# The independent safety lenses dispatched over the COMPOSED whole plan — each a real
# `.claude/agents/<lens>/agent.md` (verified present; `_role_profile` fails loud on a missing one,
# so a nonexistent path never inlines empty and makes the role-inlining contract vacuous). Three
# disjoint lenses (>=2 satisfies AC-1): a clinical-safety reviewer, an edge-case reviewer, and the
# medical-liaison reading the assembled plan AS A WHOLE (distinct from its per-finding gate role).
DEFAULT_LENSES = ("medical-safety-reviewer", "health-edge-case-reviewer", "medical-liaison")


def _dispatch_prompt(lens, assembled_plan):
    """Build a lens dispatch prompt: the full lens profile + the COMPOSED whole plan.

    Inlines the lens's full profile verbatim (INV-ROLE-INLINING, read live from
    `.claude/agents/<lens>/agent.md` via the orchestrator's `_role_profile`) ahead of the assembled
    multi-domain plan — the lens reviews the COMPOSED whole, not a per-finding fragment.

    Args:
        lens (str): The dispatched lens slug.
        assembled_plan (dict): The `run_generation`-shaped result (the composed whole plan).

    Returns:
        (str) The dispatch prompt.
    """
    profile = _role_profile(lens)
    return (
        f"{profile}\n\n"
        "## Assembled multi-domain plan to review AS A WHOLE\n\n"
        "Review the COMPOSED plan below for EMERGENT cross-domain safety issues — cumulative load\n"
        "summed across domains, or a contraindication visible only when the domains are read\n"
        "together — that no single per-finding hold represents. The per-finding holds are already\n"
        "adjudicated by the inner gate; review the assembled survivors.\n\n"
        f"{assembled_plan}\n"
    )


def _excluded_finding_ids(assembled_plan):
    """The per-finding hold finding_ids already adjudicated by the inner gate (the exclusion set).

    Reads the already-adjudicated per-finding holds off the `run_generation`-shaped result — the
    additive-AE `adjudication`, every `conflict_adjudications` entry, and every
    `rx_bpmh_adjudications` entry — and collects their `finding_id`s. The whole-plan review EXCLUDES
    any synthesized finding carrying one of these ids: the per-finding gate already owns that hold,
    so re-surfacing it here would either re-adjudicate it (double-gate) or — were the tier to assume
    the inner gate handled a hold it did not — leave a gap. Reading the set off the result (never
    re-running `reconcile`) keeps the per-finding/whole-plan split clean.

    Args:
        assembled_plan (dict): The `run_generation`-shaped result.

    Returns:
        (set) The already-adjudicated per-finding `finding_id`s.
    """
    excluded = set()
    additive = assembled_plan.get("adjudication")
    if isinstance(additive, dict) and additive.get("finding_id") is not None:
        excluded.add(additive["finding_id"])
    for axis in ("conflict_adjudications", "rx_bpmh_adjudications"):
        for outcome in (assembled_plan.get(axis) or {}).values():
            if isinstance(outcome, dict) and outcome.get("finding_id") is not None:
                excluded.add(outcome["finding_id"])
    return excluded


def _dedupe_key(finding):
    """The blind-triage dedupe key for a synthesized finding (its `id`, falling back to `concern`).

    Two lenses flagging the SAME emergent concern carry the same key; the synthesis keeps the first
    and drops the duplicate (the over-block-containing dedupe). A finding with neither `id` nor
    `concern` is keyed by its repr so it is never silently merged with an unrelated finding.
    """
    return finding.get("id") or finding.get("concern") or repr(sorted(finding.items()))


def review_plan(assembled_plan, dispatch, *, lenses=DEFAULT_LENSES):
    """Run the multi-lens whole-plan safety review and return the synthesized gate verdict.

    The SAFETY gate the `gate_dispatch=` seam targets (wired by ADR-0022-T2). It (1) dispatches each
    of `lenses` (>=2 independent safety lenses, full profiles inlined per INV-ROLE-INLINING) over
    the COMPOSED assembled plan through the injected `dispatch` seam; (2) synthesizes + blind-triages
    the union of their findings into one deduped set (a finding flagged by two lenses collapses to
    one — the over-block-containing dedupe); (3) reads the already-adjudicated per-finding hold set
    off the assembled-plan result and EXCLUDES those holds (no double-gate, no gap — the per-finding
    holds stay with the inner gate); (4) returns the synthesized finding set as the gate verdict.

    Adds NO override path of its own and re-authors nothing in `adjudicate` / the reconciler — the
    inner per-finding gate survives verbatim. The lens reasoning is the dispatched lenses' (runtime
    A), never originated here.

    Args:
        assembled_plan (dict): The `run_generation`-shaped result (the COMPOSED multi-domain plan —
            `results` + `reconciliation` + the adjudication records), reviewed as one whole.
        dispatch (Callable): The programmatic lens-dispatch seam,
            `dispatch(lens, prompt, assembled_plan) -> list of finding dicts`. A real agent dispatch
            in production; a fixture mock in tests (so the review runs with 0 live spend).
        lenses (tuple, optional): The >=2 independent lens roster (ENFORCED — a roster of <2
            lenses raises `ValueError`, never a vacuous single-/zero-lens PASS). Defaults to the
            verified `.claude/agents/` set (`DEFAULT_LENSES`).

    Raises:
        ValueError: `lenses` carries fewer than 2 independent lenses (the AC-1 contract).

    Returns:
        (dict) The gate verdict: `findings` (the synthesized, blind-triaged finding set — the
        legitimate findings that drive a revise / a block; `[]` on a clean pass), `passed` (bool —
        True when the set is empty), and `lenses` (the dispatched lens roster).
    """
    # AC-1 contract (fail-loud): a SAFETY gate must never silently PASS on too-few lenses. With
    # <2 independent lenses the multi-lens whole-plan review is not what it claims (a single lens
    # is not the independent cross-check the layer exists to provide), and an empty roster would
    # return a vacuous `passed=True` over 0 dispatches — the exact silent-PASS the gate must avoid.
    if len(lenses) < 2:
        raise ValueError(
            f"safety review requires >=2 independent lenses (AC-1); got {len(lenses)}: "
            f"{tuple(lenses)!r} — refusing to run a vacuous single-/zero-lens safety review"
        )

    excluded = _excluded_finding_ids(assembled_plan)

    synthesized = []
    seen_keys = set()
    for lens in lenses:
        prompt = _dispatch_prompt(lens, assembled_plan)
        for finding in dispatch(lens, prompt, assembled_plan) or []:
            # Exclude a per-finding hold the inner gate already adjudicated (no double-gate, no gap).
            if finding.get("finding_id") in excluded:
                continue
            key = _dedupe_key(finding)
            if key in seen_keys:
                continue  # blind-triage dedupe: the same concern flagged by two lenses collapses
            seen_keys.add(key)
            synthesized.append(finding)

    return {"findings": synthesized, "passed": not synthesized, "lenses": tuple(lenses)}
