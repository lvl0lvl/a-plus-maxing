"""Tests for the 7-zone dashboard visual shell (ADR-0009).

Pins the zone model the visual ships with: all seven zones in design order,
mechanically honest awaiting states (no digits — the no-fake-numbers guard),
accents confined to zone/card chrome (never data state, never inside an SVG),
the decision-pinned PALETTE unchanged (D3), the 16-card care-team grid with
the 4 internal build/review roles excluded, the real week-calendar strip via
the `_today` seam, and the D4 fitness markers rendering units with a neutral
direction-only trend. New fixtures are fitness-domain only (S49 demo-data
constraint).
"""

import datetime
import html as html_lib
import re
from pathlib import Path

from vault.design.templates import component_set, dashboard

REPO_ROOT = Path(__file__).resolve().parents[2]

# A fixed mid-week date for the calendar seam: Wednesday 2026-06-10.
_TODAY = datetime.date(2026, 6, 10)

_ZONE_TITLES = (
    "Readiness",
    "This Week",
    "Today's Plan",
    "Performance & Trends",
    "Your Care Team",
    "Goals & Progress",
    "Labs & Bloodwork",
)

# The deployed internal build/review roles: intentionally OFF the care team
# (they track no operator data — design doc zone 5).
_INTERNAL_ROLES = (
    "health-specialist-architect",
    "health-implementer",
    "health-edge-case-reviewer",
    "medical-safety-reviewer",
)


def _bodyweight_read():
    """A fitness-domain store read: two bodyweight readings, latest lower."""
    return [
        {"item": "biomarker::bodyweight", "timepoint": "2026-06-01T00:00:00+00:00",
         "source": "scale", "value": 184},
        {"item": "biomarker::bodyweight", "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "scale", "value": 183},
    ]


def _zones(html):
    """Map each rendered zone's decoded h2 title to its full section markup."""
    out = {}
    for section in re.findall(r"<section class='zone'[^>]*>.*?</section>", html, re.S):
        title = re.search(r"<h2[^>]*>([^<]*)</h2>", section).group(1)
        out[html_lib.unescape(title)] = section
    return out


def _awaiting_texts(fragment):
    """Return each awaiting card's decoded inner text within a markup fragment."""
    return [
        html_lib.unescape(re.sub(r"<[^>]*>", "", inner))
        for inner in re.findall(r"<div class='awaiting'>(.*?)</div>", fragment, re.S)
    ]


def test_all_seven_zone_titles_render_in_order():
    """The seven design zones render top-to-bottom in the approved order."""
    html = dashboard.render([], _today=_TODAY)
    titles = [
        html_lib.unescape(t) for t in re.findall(r"<h2[^>]*>([^<]*)</h2>", html)
    ]
    assert tuple(titles) == _ZONE_TITLES


def test_awaiting_states_carry_no_digits():
    """The hero/plan/goals awaiting cards exist and carry NO digits.

    The mechanical no-fake-numbers guard (ADR-0009 D2): an unbuilt zone names
    what is missing and never renders an invented number. The calendar zone's
    date digits live outside its awaiting card, so it is checked on the card
    text alone too.
    """
    zones = _zones(dashboard.render([], _today=_TODAY))
    for title in ("Readiness", "This Week", "Today's Plan", "Goals & Progress"):
        texts = _awaiting_texts(zones[title])
        assert texts, f"zone {title!r} must render an awaiting card"
        for text in texts:
            assert not re.search(r"\d", text), (
                f"awaiting card in {title!r} carries a digit: {text!r}"
            )


def test_accent_hexes_only_in_chrome():
    """ACCENTS hexes never color data state: no accent inside any SVG block,
    and no state-* element carrying an accent inline style (ADR-0009 D3)."""
    html = dashboard.render(_bodyweight_read(), _today=_TODAY)
    svg_blocks = re.findall(r"<svg.*?</svg>", html, re.S)
    assert svg_blocks, "the rendered dashboard must carry SVG (rings + sparkline)"
    state_tags = re.findall(r"<[^>]*class='[^']*state-[^']*'[^>]*>", html)
    assert state_tags, "the rendered dashboard must carry state-classed elements"
    for accent in component_set.ACCENTS.values():
        for block in svg_blocks:
            assert accent not in block, f"accent {accent} leaked into an SVG block"
        for tag in state_tags:
            assert accent not in tag, f"accent {accent} leaked into a state element"
    # The accents DO render as chrome (zone/card borders), not nowhere at all.
    for accent in component_set.ACCENTS.values():
        assert accent in html


def test_palette_unchanged():
    """The decision-pinned semantic PALETTE is exactly its 6 recorded entries (D3)."""
    assert component_set.PALETTE == {
        "good": "#117733",
        "watch": "#DDAA33",
        "concern": "#882255",
        "ink": "#1A1A1A",
        "paper": "#FFFFFF",
        "muted": "#555555",
    }


def test_care_team_renders_16_cards_without_internal_roles():
    """Zone 5 renders the 16 domain specialists; the 4 internal roles are off."""
    zone = _zones(dashboard.render([], _today=_TODAY))["Your Care Team"]
    assert zone.count("<div class='card'>") == 16
    assert zone.count("no rollup yet") == 16
    for slug in _INTERNAL_ROLES:
        assert slug not in zone
        humanized = slug.replace("-", " ").title()
        assert humanized not in zone, f"internal role {humanized!r} on the care team"


def test_specialists_tuple_mirrors_deployed_roster():
    """The care-team slug column plus the 4 internal roles is EXACTLY the
    deployed `.claude/agents/` roster — slug drift (an agent added, removed,
    or renamed without the tuple following) fails here."""
    deployed = {
        p.name for p in (REPO_ROOT / ".claude" / "agents").iterdir() if p.is_dir()
    }
    care_team = {slug for slug, _name, _tracks in dashboard._SPECIALISTS}
    assert care_team | set(_INTERNAL_ROLES) == deployed


def test_calendar_strip_renders_week_with_today_marked():
    """The week strip renders 7 real cells of the seam date's Mon-Sun week,
    and exactly the seam date's cell carries the .today class."""
    zone = _zones(dashboard.render([], _today=_TODAY))["This Week"]
    cells = re.findall(r"<div class='(day[^']*)'>([A-Za-z]+)<br>(\d+)</div>", zone)
    assert len(cells) == 7
    assert [c[1] for c in cells] == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    assert [c[2] for c in cells] == ["8", "9", "10", "11", "12", "13", "14"]
    today_cells = [c for c in cells if "today" in c[0]]
    assert today_cells == [("day today", "Wed", "10")]


def test_fitness_marker_renders_units_and_neutral_trend():
    """A bodyweight series renders its lb units and a NEUTRAL direction-only
    arrow — polarity is None, so no good/concern trend coloring (ADR-0009 D4)."""
    html = dashboard.render(_bodyweight_read(), _today=_TODAY)
    trends = _zones(html)["Performance & Trends"]
    assert "Bodyweight" in trends
    assert "183 lb" in trends
    row = trends.split("<div class='kpi-row'>")[1]
    assert "<span class='chip state-neutral'>" in row
    assert "&#8595;" in row, "direction-only arrow (184 -> 183 falls)"
    assert "improving" not in row
    assert "regressing" not in row


def test_empty_store_renders_awaiting_in_data_zones():
    """An empty store renders zones 4 and 7 as their own awaiting cards."""
    zones = _zones(dashboard.render([], _today=_TODAY))
    for title in ("Performance & Trends", "Labs & Bloodwork"):
        assert _awaiting_texts(zones[title]), (
            f"empty-store zone {title!r} must render an awaiting card, not an empty section"
        )
        assert "kpi-row" not in zones[title]
