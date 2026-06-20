"""The measure + adjust-read-back legs of the closed loop (plan -> act -> measure -> adjust).

`design/vision.md`: the system "closes the loop — plan -> act -> measure -> adjust — tracking
interventions, biomarkers, and outcomes over time so each plan is backed by what actually happened."
The plan leg is wired (`generate_plan` records `plan::<domain>`); this module wires the next two:

  MEASURE — `record_tracking` is the production caller for `plan_schema.record_plan_tracking` (which
    was schema-only, no production caller — the PF-S63-02 component-built-but-unwired gap). It records
    one observed tracking snapshot (what the operator ACTUALLY did) against a domain's plan. Its
    value-add over the raw schema writer is the honest no-plan-to-track boundary: a domain with no
    recorded plan has nothing to have been "done", so tracking it would render a fabricated-adherence
    surface — `record_tracking` records nothing and returns the no-plan state instead.

  ADJUST (read-back) — `resolve_plan_progress` joins a domain's recorded plan with its tracking
    snapshot into the plan-vs-actual view the re-plan + the dashboard read (the "feeds back into the
    next plan" read side). The domain-specific progression ALGORITHM (how a specialist changes the
    prescription from the progress) is a specialist-reasoning surface deferred to its own session — it
    is NOT computed here; this module provides the honest plan-vs-actual substrate it builds on.

Tracking is OPERATOR-OBSERVED, not specialist-authored — no agent dispatch is part of this flow.
All persistence goes THROUGH `scripts.store.plan_schema` (which writes THROUGH `scripts.store.store`);
this module defines no store key, records no plan, and reuses the plan/tracking streams unchanged.
Writers raise only ValueError; readers never raise on absence.
"""

from scripts.store import plan_schema

# Measure result states. A tracking snapshot records only against an existing plan — the honest
# no-plan-to-track boundary (a domain with zero recorded plans has nothing to have been done).
RECORDED = "recorded"
NO_PLAN_TO_TRACK = "no-plan-to-track"


def record_tracking(domain, tracking, on_date, root):
    """Record one observed tracking snapshot against a domain's plan (the MEASURE leg).

    The production caller for `plan_schema.record_plan_tracking`: validates the domain is tracked,
    confirms a plan EXISTS for the domain (a domain with zero recorded plans has nothing to have been
    done — recording tracking against it would fabricate an adherence surface, so this records nothing
    and returns the no-plan state), then records the snapshot via the reused `record_plan_tracking`.
    The snapshot's own field types are validated inside `record_plan_tracking` (it raises ValueError
    on a malformed snapshot — surfaced loud, never silently dropped).

    Args:
        domain (str): A `plan_schema.TRACKED_DOMAINS` member (workout / nutrition / supplements —
            peptide tracking IS the watch-out stream, not a tracked plan domain).
        tracking (dict): The observed snapshot per the domain's tracking table.
        on_date (str): The snapshot's YYYY-MM-DD date.
        root (str | Path): The store root.

    Returns:
        (dict) A result record: `domain`, `on_date`, `state` (`recorded` | `no-plan-to-track`),
        `recorded` (bool), and `plan_date` (the date of the plan tracked against, or None).

    Raises:
        ValueError: An untracked domain, a malformed date, or a snapshot failing its field-type
            table (raised by `record_plan_tracking` — never a silent drop).
    """
    if domain not in plan_schema.TRACKED_DOMAINS:
        raise ValueError(
            f"untracked plan domain {domain!r}; known: {plan_schema.TRACKED_DOMAINS}"
        )
    plan = plan_schema.read_plan(domain, on_date, root)
    # state == NO_PLAN means the domain has zero recorded plans (resolve_plan over no readings); any
    # other state (a plan today, or NO_PLAN_TODAY = plans on file but none dated on_date) means a plan
    # exists to track against. No plan -> record nothing, the honest no-plan-to-track boundary.
    if plan["state"] == plan_schema.NO_PLAN:
        return {"domain": domain, "on_date": on_date, "state": NO_PLAN_TO_TRACK,
                "recorded": False, "plan_date": None}
    plan_schema.record_plan_tracking(domain, tracking, on_date, root)
    return {"domain": domain, "on_date": on_date, "state": RECORDED,
            "recorded": True, "plan_date": plan["plan_date"]}


def resolve_plan_progress(domain, on_date, root):
    """Join a domain's recorded plan with its tracking snapshot into a plan-vs-actual view (ADJUST read).

    The read-back the re-plan + the dashboard consume: it pairs `read_plan` (the prescription) with
    `read_plan_tracking` (what was actually done) for `domain` on `on_date`. Honest absence states —
    a domain with no plan has no progress (`has_plan` False); a plan with no tracking snapshot is
    plan-only (`has_tracking` False, the operator has not logged yet), never an invented snapshot.
    Pure read; computes no progression verdict (that is the deferred specialist-reasoning adjust).

    Args:
        domain (str): A `plan_schema.TRACKED_DOMAINS` member.
        on_date (str): The render/progress date, YYYY-MM-DD.
        root (str | Path): The store root.

    Returns:
        (dict) `domain`, `plan` (the plan dict | None), `specialist` (str | None), `plan_date`
        (str | None), `tracking` (the snapshot dict | None), `has_plan` (bool), `has_tracking` (bool).

    Raises:
        ValueError: An untracked domain.
    """
    if domain not in plan_schema.TRACKED_DOMAINS:
        raise ValueError(
            f"untracked plan domain {domain!r}; known: {plan_schema.TRACKED_DOMAINS}"
        )
    plan = plan_schema.read_plan(domain, on_date, root)
    tracking = plan_schema.read_plan_tracking(domain, on_date, root)
    has_plan = plan["state"] != plan_schema.NO_PLAN
    return {
        "domain": domain,
        "plan": plan["plan"],
        "specialist": plan["specialist"],
        "plan_date": plan["plan_date"],
        "tracking": tracking,
        "has_plan": has_plan,
        "has_tracking": tracking is not None,
    }
