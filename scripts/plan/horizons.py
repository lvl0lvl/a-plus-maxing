"""Time-horizon reads over the goal / calendar / plan store schemas (ADR-0038).

A pure read/query composition: the horizon layer surfaces milestone progress,
the next dated cadence, and per-domain tracking horizons by DELEGATING to the
three store-schema owners' resolvers. It writes no store stream, defines no
``::``-prefixed item id, and re-derives no progress — milestone percent stays
owned by ``goal_schema`` (its read-derived percent is the single progress site).
The next cadence is owned by ``calendar_schema``; the tracked-domain gate by
``plan_schema.TRACKED_DOMAINS`` (``peptides`` is a plan domain but not a tracked
one — it rides the existing watch-out stream). A goal carries no deadline, so its
horizon degrades to rolling maintenance cycles and fabricates no target-date. All
reads are local file I/O; 0 model-bound send.
"""

from scripts.store import calendar_schema, goal_schema, plan_schema

# ADR-0038 D2 enrichment: these three keys ride the ADR-0010 D2 open-on-extras
# seam on ``plan::<domain>`` values — permitted by omission from every domain's
# required/optional dict in ``plan_schema`` (no schema declaration, no new store
# stream). ADR-0038-T3 reads ``week_expectation`` off these values as the
# declared per-week expectation.
HORIZON_EXTRAS = ("phase", "week_intent", "week_expectation")


def plan_extras(plan):
    """Read the horizon extras off a resolved ``plan::<domain>`` value.

    The read-back for the week/month framing: given a resolved plan value,
    return only the ``HORIZON_EXTRAS`` keys present. A plan carrying none of
    them — or a falsy/None plan (an absent-plan resolve) — yields an empty dict
    (the graceful floor), never a raise. Adds no store read; the value is the
    one the T1 read layer already resolved.

    Args:
        plan (dict): A resolved plan value (``read_plan(...)["plan"]``).

    Returns:
        (dict) The subset of `HORIZON_EXTRAS` keys carried by `plan`.
    """
    if not plan:
        return {}
    return {key: plan[key] for key in HORIZON_EXTRAS if key in plan}


def read_horizon(slug, root):
    """Read one goal's milestone horizon, or None when the goal is absent.

    Milestone progress is DELEGATED to ``goal_schema.read_goal`` (whose
    read-derived percent is the single progress site — this layer computes none).
    A goal has no deadline, so the horizon degrades to rolling maintenance cycles
    with no fabricated target-date.

    Args:
        slug (str): The goal's stable identifier.
        root (str | Path): The store root.

    Returns:
        (dict | None) Keys `label`, `milestone` (the resolved goal dict),
        `mode` (`"rolling"`), and `target_date` (always None — never
        fabricated); or None when the goal has no stored snapshot.
    """
    milestone = goal_schema.read_goal(slug, root)
    if milestone is None:
        return None
    return {
        "label": milestone["label"],
        "milestone": milestone,
        "mode": "rolling",
        "target_date": None,
    }


def next_cadence(root, on_date):
    """Read the next dated calendar cadence on or after `on_date`, or None.

    Selects the earliest ``calendar::events`` event dated on/after `on_date`
    (``calendar_schema`` owns the read); creates no schedule object and writes
    nothing.

    Args:
        root (str | Path): The store root.
        on_date (str): The render date, YYYY-MM-DD.

    Returns:
        (dict | None) The next cadence `{category, label, date}`, or None when no
        event is dated on/after `on_date`.
    """
    events_by_date = calendar_schema.read_events(root)
    upcoming = sorted(date for date in events_by_date if date >= on_date)
    if not upcoming:
        return None
    date = upcoming[0]
    event = events_by_date[date][0]
    return {"category": event["category"], "label": event["label"], "date": date}


def domain_horizons(root, on_date):
    """Read per-domain tracking horizons for the tracked plan domains only.

    A domain surfaces a tracking horizon only when it has a plan dated the render
    date AND is a ``plan_schema.TRACKED_DOMAINS`` member — ``peptides`` is a plan
    domain but not a tracked one, so it yields no cadence and no tracking horizon.
    Both non-None ``resolve_plan`` states are skipped: ``NO_PLAN`` (no plan on
    file) and ``NO_PLAN_TODAY`` (a stale plan not dated the render date — surfacing
    its plan_date would mislead the ADR-0038-T3 week/month classifier).

    Args:
        root (str | Path): The store root.
        on_date (str): The render date, YYYY-MM-DD.

    Returns:
        (list) One `{domain, plan_date, extras}` dict per tracked domain with a
        current (render-date) plan on file, in `plan_schema.PLAN_DOMAINS` order.
        `extras` carries the `HORIZON_EXTRAS` keys enriched onto the plan value
        (empty when absent).
    """
    horizons = []
    for domain in plan_schema.PLAN_DOMAINS:
        resolved = plan_schema.read_plan(domain, on_date, root)
        if resolved["state"] is not None:
            continue
        if domain not in plan_schema.TRACKED_DOMAINS:
            continue
        horizons.append({
            "domain": domain,
            "plan_date": resolved["plan_date"],
            "extras": plan_extras(resolved["plan"]),
        })
    return horizons
