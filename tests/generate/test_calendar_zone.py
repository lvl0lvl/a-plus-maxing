"""Tests for the dashboard zone 2 — This Week event rendering (visual spec + calendar_schema).

Pins that stored calendar events land as category-tinted pills in their matching
month-calendar day cells, that a no-event day keeps the bare day-number cell
markup (the empty-store path the calendar-shell tests pin), that the awaiting
caption shows ONLY when no events are stored, and that the raw `calendar::` key
never leaks. New fixtures are fitness/clinical-domain only.
"""

import datetime
import html as html_lib
import re

from vault.design.templates import dashboard

# Wednesday 2026-06-10 — the calendar seam date (June 2026).
_TODAY = datetime.date(2026, 6, 10)


def _zone2(store_read):
    """Render the dashboard and return the 'This Week' <section> markup."""
    html = dashboard.render(store_read, _today=_TODAY)
    for section in re.findall(r"<section class='zone'>.*?</section>", html, re.S):
        title = html_lib.unescape(re.search(r"<h2>([^<]*)</h2>", section).group(1))
        if title == "This Week":
            return section
    raise AssertionError("This Week zone not found")


def _event(category, label, on_date):
    """One calendar::events store reading (the render's resolve_events input shape)."""
    return {
        "item": "calendar::events",
        "timepoint": on_date,
        "source": f"calendar::{category}-{label}",  # distinct content-tag stand-in
        "value": {"category": category, "label": label},
    }


def test_calendar_events_render_as_category_tinted_pills():
    """Each stored event renders a pill in its category's measured tint, no awaiting caption."""
    zone = _zone2([
        _event("lab-draw", "Fasting panel", "2026-06-10"),
        _event("appointment", "Dr. Smith", "2026-06-10"),
        _event("training", "Lower body", "2026-06-12"),
    ])
    assert "No scheduled events" not in zone
    assert "Fasting panel" in zone and "Dr. Smith" in zone and "Lower body" in zone
    for category in ("lab-draw", "appointment", "training"):
        assert f"pill tint-{category}" in zone


def test_calendar_event_lands_in_its_own_day_cell():
    """An event on the 12th lands in the 12th's cell; a no-event day stays bare."""
    zone = _zone2([_event("training", "Lower body", "2026-06-12")])
    # the 12th cell carries the event pill in its evlist
    cell12 = re.search(r"<span class='dnum'>12</span><div class='evlist'>(.*?)</div>", zone)
    assert cell12 is not None and "Lower body" in cell12.group(1)
    # the 11th (no event) keeps the bare day-number cell markup
    assert "<span class='dnum'>11</span></div>" in zone


def test_calendar_empty_store_is_awaiting_and_bare_cells():
    """No events -> the awaiting caption + bare cells (no in-cell evlist).

    (The four event-category LEGEND pills always render in the header; this
    asserts no EVENT pills landed in any day cell, i.e. no `evlist`.)
    """
    zone = _zone2([])
    assert "No scheduled events — the calendar model is pending." in zone
    assert "class='evlist'" not in zone


def test_calendar_never_leaks_raw_event_key():
    """The raw `calendar::` store key never renders as text."""
    zone = _zone2([_event("lab-draw", "Fasting panel", "2026-06-10")])
    assert "calendar::" not in zone


def test_calendar_today_cell_keeps_today_marker_with_events():
    """An event on today renders in the today cell without dropping the `· Today` marker."""
    zone = _zone2([_event("check-in", "Weekly check-in", "2026-06-10")])
    cell = re.search(
        r"<div class='dcell today'><span class='dnum'>10 . Today</span><div class='evlist'>(.*?)</div></div>",
        zone,
    )
    assert cell is not None and "Weekly check-in" in cell.group(1)
