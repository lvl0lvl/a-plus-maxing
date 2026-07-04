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

import datetime

from scripts.store import calendar_schema, goal_schema, plan_schema, store

# Trailing window spans in days, anchored on (and inclusive of) the render date
# (OQ-2 boundary decision): a window is the `span` dates [on_date - (span-1),
# on_date], so the render date is always in-window — today's plan counts toward
# this week and this month.
WEEK_SPAN_DAYS = 7
MONTH_SPAN_DAYS = 30

# The fixed classifier vocabulary (AC-4): the deterministic expectation-vs-actual
# comparison returns exactly one of these three tokens.
BEHIND, ON_TRACK, AHEAD = "behind", "on-track", "ahead"
CLASSIFICATIONS = (BEHIND, ON_TRACK, AHEAD)

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


def _in_window(timepoint, on_date, span_days):
    """Report whether a YYYY-MM-DD timepoint falls in the trailing window.

    The window is the `span_days` dates ending on and including `on_date`:
    [on_date - (span_days - 1), on_date]. The single window-membership predicate
    both the week and month queries share.

    Args:
        timepoint (str): The reading's date, YYYY-MM-DD.
        on_date (str): The render date, YYYY-MM-DD.
        span_days (int): The window width in days.

    Returns:
        (bool) Whether `timepoint` is in the trailing window ending on `on_date`.
    """
    end = datetime.date.fromisoformat(on_date)
    start = end - datetime.timedelta(days=span_days - 1)
    point = datetime.date.fromisoformat(str(timepoint).split("T", 1)[0])
    return start <= point <= end


def window_block(domain, root, on_date, span_days):
    """Select a domain's latest plan reading in the trailing window, or None.

    Widens ``plan_schema.resolve_plan``'s single-date equality to window
    membership: over the domain's ``plan::<domain>`` readings, keep those whose
    timepoint is in-window and return the latest-dated one. The ADR-0036 loop
    day-keys a new dated plan on every trigger (RT-09), so multiple dated plans
    can share one window — the max-timepoint reading is "the block", mirroring
    ``resolve_plan``'s latest-wins (the last store-order reading at the max date).

    Args:
        domain (str): A `plan_schema.PLAN_DOMAINS` member.
        root (str | Path): The store root.
        on_date (str): The render date, YYYY-MM-DD.
        span_days (int): The trailing window width in days.

    Returns:
        (dict | None) Keys `plan_date` (the block's date) and `extras` (the
        `HORIZON_EXTRAS` week-framing off the block value); or None when no plan
        falls in the window.
    """
    readings = store.read(f"plan::{domain}", root=root)
    in_window = [r for r in readings if _in_window(r["timepoint"], on_date, span_days)]
    if not in_window:
        return None
    latest_date = max(r["timepoint"] for r in in_window)
    block = None
    for reading in in_window:
        if reading["timepoint"] == latest_date:
            block = reading
    return {"plan_date": latest_date, "extras": plan_extras(block["value"])}


def read_horizons(domain, slug, root, on_date):
    """Compose the four tracking horizons for a domain + goal on a render date.

    Today's action is the date-equality plan (``plan_schema.read_plan`` — the
    render-date plan when present, ``NO_PLAN``/``NO_PLAN_TODAY`` when absent, never
    the nearest date). This week's block and the month arc are the latest-in-window
    plans over the 7- and 30-day trailing windows. The milestone is the goal's
    derived progress via ``read_horizon`` (the single progress owner). Composes
    over the existing schema owners only — writes no store stream, defines no
    ``::``-prefixed item id.

    Args:
        domain (str): A `plan_schema.PLAN_DOMAINS` member.
        slug (str): The goal's stable identifier.
        root (str | Path): The store root.
        on_date (str): The render date, YYYY-MM-DD.

    Returns:
        (dict) Keys `today` (the `resolve_plan` result), `week` and `month` (the
        `window_block` results, or None), and `milestone` (the `read_horizon`
        result, or None).
    """
    return {
        "today": plan_schema.read_plan(domain, on_date, root),
        "week": window_block(domain, root, on_date, WEEK_SPAN_DAYS),
        "month": window_block(domain, root, on_date, MONTH_SPAN_DAYS),
        "milestone": read_horizon(slug, root),
    }


def classify(expectation, actual):
    """Classify an actual per-week rate against the declared expectation slope.

    A pure deterministic comparison — no model call. Both arguments are signed
    per-week rates in the goal's unit; the expectation's sign is the goal's target
    direction. Progress-toward-target is compared: an actual whose toward-target
    progress is slower than the expectation is `BEHIND`, equal is `ON_TRACK`,
    faster is `AHEAD`. Direction-agnostic in the spirit of ``goal_schema`` — a
    downward weight goal (expectation -0.4) reads -0.1 as `BEHIND` and -0.5 as
    `AHEAD`.

    Args:
        expectation (int | float): The declared per-week slope toward target.
        actual (int | float): The realized per-week rate, same unit and orientation.

    Returns:
        (str) One of `CLASSIFICATIONS`.
    """
    direction = 1 if expectation >= 0 else -1
    expected = expectation * direction
    toward = actual * direction
    if toward < expected:
        return BEHIND
    if toward > expected:
        return AHEAD
    return ON_TRACK


def actual_weekly_rate(slug, root):
    """Derive a goal's realized per-week rate over its observed snapshot span, or None.

    Measures the ``current`` reading's change across the SAME window the span is
    sized over: the earliest in-span snapshot's ``current`` to the latest
    snapshot's ``current``, divided by the elapsed weeks. Anchoring the numerator
    on the earliest snapshot's reading — not the goal's fixed ``baseline`` — keeps
    numerator and denominator over one window, so a goal already partway when
    snapshots begin is not overstated (the two agree only when the earliest
    snapshot's current equals baseline). Presence is still gated through
    ``goal_schema.resolve_goal`` (the single derived-progress owner); a goal with
    no readable snapshot, or a single-snapshot goal (no measurable span), yields
    None — honest absence, never a fabricated rate. Reads only; writes nothing.

    Args:
        slug (str): The goal's stable identifier.
        root (str | Path): The store root.

    Returns:
        (float | None) The realized per-week rate (latest current - earliest
        in-span current over the snapshot span in weeks), or None when there is
        no multi-day span.
    """
    readings = store.read(f"goal::{slug}", root=root)
    if goal_schema.resolve_goal(readings) is None:
        return None
    snapshots = sorted(readings, key=lambda r: r["timepoint"])
    span_days = (
        datetime.date.fromisoformat(snapshots[-1]["timepoint"])
        - datetime.date.fromisoformat(snapshots[0]["timepoint"])
    ).days
    if span_days <= 0:
        return None
    start_val = snapshots[0]["value"]["current"]
    end_val = snapshots[-1]["value"]["current"]
    return (end_val - start_val) / (span_days / 7)


def assess_pace(domain, slug, root, on_date):
    """Classify a goal's realized pace against the week's declared expectation, or None.

    Sources the expectation from the this-week block's ``week_expectation`` D2
    extra (the date-range plan history) and the actual from ``actual_weekly_rate``
    (routed through ``goal_schema``), then feeds both into ``classify``. Returns
    None when either input is absent — a non-numeric/absent expectation, a zero
    expectation (an undefined target direction, not a maintenance verdict), or a
    goal with no measurable span — inventing no verdict. Reads only; writes no
    store item.

    Args:
        domain (str): A `plan_schema.PLAN_DOMAINS` member.
        slug (str): The goal's stable identifier.
        root (str | Path): The store root.
        on_date (str): The render date, YYYY-MM-DD.

    Returns:
        (str | None) One of `CLASSIFICATIONS`, or None on absent inputs.
    """
    block = window_block(domain, root, on_date, WEEK_SPAN_DAYS)
    if block is None:
        return None
    expectation = block["extras"].get("week_expectation")
    if not isinstance(expectation, (int, float)) or isinstance(expectation, bool):
        return None
    if expectation == 0:
        return None
    actual = actual_weekly_rate(slug, root)
    if actual is None:
        return None
    return classify(expectation, actual)


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
