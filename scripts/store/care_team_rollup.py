"""Per-specialist 30-day freshness rollup over the existing store streams.

A read-model (NO new store stream): attributes each store reading to its owning
specialist and reduces the specialist's readings to a freshness status from the
most-recent timepoint. The dashboard Zone 5 ("Your Care Team") renders the
status; specialists with no mapped data render the honest "no data yet" state.

The specialist->stream mapping and the 30-day status rule are the adopted
decision `vault/decisions/2026-06-13-care-team-rollup-zone5-mapping.md` (Walter,
S58). Store timepoints are ISO strings — date-only `YYYY-MM-DD` (plan/calendar)
or full datetimes `YYYY-MM-DDTHH:MM:SS+00:00` (the loop streams); the rollup
trusts that writer-validated format (store-trusts-writer) and reduces each to its
nominal calendar date for the day arithmetic.
"""
import datetime

# Status thresholds in days from `today` to the latest mapped timepoint (a
# future timepoint -> days clamps to 0 -> current). Decision note Decision 2.
CURRENT_MAX_DAYS = 30
STALE_MAX_DAYS = 60

# specialist slug -> (item prefixes it owns, calendar event categories it owns).
# A non-calendar item belongs to a specialist when it == a prefix or starts with
# one; the prefixes are disjoint across specialists. `calendar::events` readings
# route by their value category instead. Decision note Decision 1. Specialists
# absent from this map (the 10 streamless domains) carry no data -> the render
# fills the honest "no data yet" state.
SPECIALIST_STREAMS = {
    "personal-trainer": (("plan::workout", "plan-track::workout"), ("training",)),
    "nutritionist": (("plan::nutrition", "plan-track::nutrition"), ()),
    "supplement-specialist": (("plan::supplements", "plan-track::supplements"), ()),
    "peptide-specialist": (("plan::peptides", "watch-out::"), ()),
    "labs-specialist": (("panel::", "biomarker::"), ("lab-draw",)),
    "medical-liaison": (("feedback::",), ("appointment", "check-in")),
}

# Inverted calendar route: event category -> owning specialist (categories are
# disjoint across specialists by construction above).
_CATEGORY_OWNER = {
    category: slug
    for slug, (_prefixes, categories) in SPECIALIST_STREAMS.items()
    for category in categories
}

_CALENDAR_ITEM = "calendar::events"


def _owner_by_item(item):
    """Return the specialist slug owning a prefixed item, or None.

    The non-calendar route: matches an item against each specialist's stream
    prefixes (`item == prefix` or `item.startswith(prefix)`). `calendar::events`
    routes by category in `resolve_rollup` instead, so it is never matched here.
    """
    for slug, (prefixes, _categories) in SPECIALIST_STREAMS.items():
        for prefix in prefixes:
            if item == prefix or item.startswith(prefix):
                return slug
    return None


def _timepoint_date(timepoint):
    """The nominal calendar date of a store timepoint, or None when unparseable.

    Store timepoints are ISO `YYYY-MM-DD[Thh:mm:ss…]` strings — date-only
    (plan/calendar) or full datetimes (the loop streams). The date is the first
    10 chars, parsed with the house `datetime.date.fromisoformat` (the
    `render_views` date-axis convention, mirroring `component_set.reading_date`).
    An unparseable or non-string timepoint reads None — the reading then does not
    contribute to the freshness, the same honest-absence degrade the trend card
    takes (never a crash; matched by the existing unparseable-timepoint tests).
    """
    try:
        return datetime.date.fromisoformat(timepoint[:10])
    except (TypeError, ValueError):
        return None


def _status(latest, today):
    """Classify a specialist's latest mapped timepoint into a freshness status.

    Args:
        latest (datetime.date): The most-recent recorded-data timepoint (on or
            before `today` — `resolve_rollup` excludes future timepoints).
        today (datetime.date): The reference date for the freshness window.

    Returns:
        (dict) `{state, days}` — state is `current` | `stale` | `dormant`; days
        is the age `today - latest` (>= 0 since `latest` is never in the future).
    """
    days = (today - latest).days
    if days <= CURRENT_MAX_DAYS:
        state = "current"
    elif days <= STALE_MAX_DAYS:
        state = "stale"
    else:
        state = "dormant"
    return {"state": state, "days": days}


def resolve_rollup(store_read, today):
    """Reduce the store readings to a per-specialist freshness status.

    Pure over the store read model. Each reading is attributed to at most one
    specialist (by item prefix, or by calendar event category); the specialist's
    status is taken from its most-recent RECORDED-DATA timepoint. Future-dated
    timepoints are EXCLUDED — an upcoming scheduled event is activity (shown in
    Zone 2 This Week), not recorded data, and labeling it "updated today" would
    assert a data update that never happened. So a specialist whose only mapped
    reading is a future event, like one with no mapped reading at all, is ABSENT
    from the result (the Zone 5 render fills the honest "no data yet" state).

    Args:
        store_read (list): The store read model (list of reading dicts).
        today (datetime.date): The reference date for the freshness window.

    Returns:
        (dict) specialist slug -> `{state, days}` for every specialist with
        recorded data on or before `today`.
    """
    latest = {}
    for reading in store_read:
        item = reading["item"]
        if item == _CALENDAR_ITEM:
            slug = _CATEGORY_OWNER.get(reading["value"]["category"])
        else:
            slug = _owner_by_item(item)
        if slug is None:
            continue
        day = _timepoint_date(reading["timepoint"])
        if day is None or day > today:
            continue
        if slug not in latest or day > latest[slug]:
            latest[slug] = day
    return {slug: _status(day, today) for slug, day in latest.items()}
