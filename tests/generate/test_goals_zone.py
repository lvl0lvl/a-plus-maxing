"""Tests for the dashboard zone 6 — Goals & Progress (visual spec + goal_schema).

Pins the populated goal-row anatomy (label left, percent right, good-green
progress fill), the slug-ordered rows, the bottom landmark note card that renders
ONLY in the populated state, the raw-key-never-leaks guard, and the honest empty
state (one unfilled track row + the digit-free awaiting copy, NO percent, NO
landmark card) — the visual spec's "Honest state (current)". New fixtures are
fitness-domain only (the S49 demo-data constraint).
"""

import datetime
import html as html_lib
import re

from vault.design.templates import component_set, dashboard

_TODAY = datetime.date(2026, 6, 10)


def _zone6(store_read):
    """Render the dashboard and return the 'Goals & Progress' <section> markup."""
    html = dashboard.render(store_read, _today=_TODAY)
    for section in re.findall(r"<section class='zone'>.*?</section>", html, re.S):
        title = html_lib.unescape(re.search(r"<h2>([^<]*)</h2>", section).group(1))
        if title == "Goals & Progress":
            return section
    raise AssertionError("Goals & Progress zone not found")


def _goal_reading(slug, label, baseline, current, target, on_date="2026-06-08", unit="lb"):
    """One goal:: store reading (the render's `resolve_goal` input shape)."""
    return {
        "item": f"goal::{slug}",
        "timepoint": on_date,
        "source": "goal-progress",
        "value": {"label": label, "baseline": baseline, "current": current,
                  "target": target, "unit": unit},
    }


def test_goals_zone_renders_rows_with_percent_and_good_fill():
    """Each goal renders its label, derived percent, and a PALETTE-good fill track."""
    zone = _zone6([
        _goal_reading("bench-1rm", "Bench 1RM", 225, 250, 275),
        _goal_reading("body-fat", "Body fat %", 18, 15, 12, unit="%"),
    ])
    assert "Bench 1RM" in zone and "Body fat %" in zone
    # both halfway across -> 50% (direction-agnostic), format_number drops the .0
    assert zone.count(">50%<") == 2
    # the good-green fill at 50% width, PALETTE good — never an accent/data-state color
    assert f"width:50.0%;background:{component_set.PALETTE['good']}" in zone
    assert "class='ghead'" in zone
    # the row is percent-ONLY: the raw baseline/current/target/unit never reach the
    # DOM, so a resolve_goal regression that corrupts them (while the derived percent
    # coincidentally matches) cannot hide behind the percent assertion above.
    assert all(raw not in zone for raw in ("225", "250", "275", "lb"))


def test_goals_zone_percent_keeps_decimals_and_clamps():
    """A non-integer percent renders its decimal; overshoot clamps to 100, not >100."""
    zone = _zone6([
        _goal_reading("third", "One-third there", 0, 1, 3, unit=""),   # 33.3%
        _goal_reading("over", "Overshot", 100, 200, 150, unit=""),     # clamps 100
    ])
    assert ">33.3%<" in zone
    assert ">100%<" in zone
    assert ">133" not in zone  # never renders an over-100 percent


def test_goals_zone_landmark_note_renders_only_when_populated():
    """The landmark note card follows the rows when goals exist, absent when empty."""
    populated = _zone6([_goal_reading("bench-1rm", "Bench 1RM", 225, 250, 275)])
    assert "Next milestone" in populated
    assert html_lib.unescape(dashboard._LANDMARK_NOTE) in html_lib.unescape(populated)
    empty = _zone6([])
    assert "Next milestone" not in empty


def test_goals_zone_empty_state_is_awaiting_and_digit_free():
    """No goals -> the honest awaiting card + an unfilled track, with NO digits."""
    zone = _zone6([])
    assert "<div class='awaiting'>" in zone
    assert "No goals on file" in zone
    assert "class='fill'" not in zone  # the empty track has no fill (no invented %)
    text = html_lib.unescape(re.sub(r"<[^>]*>", " ", zone))
    assert not any(ch.isdigit() for ch in text), f"empty goals zone has a digit: {text!r}"


def test_goals_zone_never_leaks_raw_goal_key():
    """The goal slug/key never renders as a label — only the goal's own label."""
    zone = _zone6([_goal_reading("bench-1rm", "Bench 1RM", 225, 250, 275)])
    assert "goal::" not in zone


def test_goals_zone_rows_render_in_slug_order():
    """Rows render in store-item (slug) order regardless of input order."""
    zone = _zone6([
        _goal_reading("zzz-last", "Zulu goal", 0, 5, 10, unit=""),
        _goal_reading("aaa-first", "Alpha goal", 0, 5, 10, unit=""),
    ])
    assert zone.index("Alpha goal") < zone.index("Zulu goal")
