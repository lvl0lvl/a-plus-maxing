"""Calendar-event store schema (dashboard zone 2 — This Week).

Records operator calendar events as one content-tagged store stream and reads
them back grouped by date for the month-calendar render. Writes THROUGH
``scripts.store.store`` (``append``) on the one ``scripts.store.keying`` Line
Field Set, reusing loop_schema's reading constructor + content-tag derivation —
defines no second key, reimplements no store I/O. All persistence is local file
I/O; 0 model-bound send.

Stream (one item, content-tagged sources — the ``plan-track`` pattern):
    calendar::events   one event per reading; timepoint = the event's
                       YYYY-MM-DD date; source = a content tag over the value
                       (loop_schema's derivation on the ``calendar::`` prefix),
                       so two DISTINCT events on the same date both persist while
                       an identical re-entry is an idempotent no-op; value =
                       ``{category, label}``. ``category`` is one of
                       `EVENT_CATEGORIES` (the four signed event-category tint
                       names); ``label`` is the event's display text. The render
                       groups events by date and lands a category-tinted pill in
                       each matching day cell. The ``::`` separator is not a path
                       separator, so the prefixed id stays a direct child of the
                       store root.

Corrections are by re-recording (the content-tagged stream is OUTSIDE
``store.correct``'s content-independent-source contract, like the loop_schema
watch-out/feedback streams). Writers raise only ValueError; readers never raise
on absence.
"""

import datetime
import re

from scripts.store import store
from scripts.store.loop_schema import _content_tag, _reading

# The fixed item id under which all calendar events accrue as one stream.
_EVENTS_ITEM = "calendar::events"

# The four signed event categories — ALSO the event-category tint names the
# render pairs each pill with (component_set CHROME training/lab-draw/check-in/
# appointment tint+text pairs, AA-measured). A category outside this set has no
# rendered tint pair (component_set.pill KeyErrors), so it is rejected at the
# writer boundary instead of failing at render.
EVENT_CATEGORIES = ("training", "lab-draw", "check-in", "appointment")

# Date-only timepoints by contract: the render matches an event's timepoint
# against a calendar day's `date.isoformat()`, so a timestamped or malformed
# date would silently never land in a cell — rejected at the writer instead
# (the plan_schema._check_date pattern).
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _is_nonempty_str(value):
    """Report whether `value` is a non-empty str."""
    return isinstance(value, str) and value != ""


def _check_date(value, what):
    """Reject a timepoint that is not a real YYYY-MM-DD calendar date.

    Args:
        value: The candidate date string.
        what (str): The argument name for the error message.

    Raises:
        ValueError: `value` is not a YYYY-MM-DD string naming a real date.
    """
    if not isinstance(value, str) or not _DATE_RE.fullmatch(value):
        raise ValueError(f"{what} {value!r} is not a YYYY-MM-DD date")
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{what} {value!r} is not a real calendar date") from None


def _check_event(category, label):
    """Validate an event's category and label.

    Raises:
        ValueError: `category` is not an `EVENT_CATEGORIES` member, or `label`
            is not a non-empty str.
    """
    if category not in EVENT_CATEGORIES:
        raise ValueError(
            f"unknown event category {category!r}; known: {EVENT_CATEGORIES}"
        )
    if not _is_nonempty_str(label):
        raise ValueError(f"event label must be a non-empty str, got {label!r}")


def record_event(category, label, on_date, root):
    """Record one calendar event for a date.

    Appends item ``calendar::events`` at `on_date` under a content-tagged source
    (loop_schema's derivation on the ``calendar::`` prefix), so two DISTINCT
    same-date events both persist while an identical re-entry (same category +
    label + date) is an idempotent no-op. Corrections are by re-recording with
    differing content (the content-tagged stream is outside `store.correct`).

    Args:
        category (str): An `EVENT_CATEGORIES` member (also the pill tint name).
        label (str): The event's display text (non-empty).
        on_date (str): The event's YYYY-MM-DD date.
        root (str | Path): The store root.

    Raises:
        ValueError: Unknown category, empty label, or a malformed date.
    """
    _check_event(category, label)
    _check_date(on_date, "on_date")
    value = {"category": category, "label": label}
    store.append(
        _EVENTS_ITEM,
        _reading(_EVENTS_ITEM, on_date, _content_tag("calendar::", value), value),
        root=root,
    )


def resolve_events(readings):
    """Group a calendar-event stream's readings by date.

    Pure over the readings as `store.read` returns them (timepoint-sorted). Each
    date maps to its events in store-read order; an empty stream is an empty
    dict (absence — the render shows the awaiting caption, never invented cells).

    Args:
        readings (list): The `calendar::events` readings, in `store.read` order.

    Returns:
        (dict) date string -> list of `{category, label}` event dicts.
    """
    by_date = {}
    for reading in readings:
        by_date.setdefault(reading["timepoint"], []).append(reading["value"])
    return by_date


def read_events(root):
    """Resolve every stored calendar event grouped by date (see `resolve_events`).

    Args:
        root (str | Path): The store root.

    Returns:
        (dict) date string -> list of `{category, label}` event dicts.
    """
    return resolve_events(store.read(_EVENTS_ITEM, root=root))
