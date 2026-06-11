"""Tests for the 7-zone dashboard visual shell (ADR-0009 + visual spec).

Pins the zone model AND the visual language the dashboard ships with: all
seven zones in design order, mechanically honest empty states (no digits —
the no-fake-numbers guard; track-only hero rings with no arc; an unfilled
goals track), accents confined to zone/card chrome (never data state, never
inside an SVG), the decision-pinned PALETTE unchanged (D3), the 16-card
care-team grid with the 4 internal build/review roles excluded, the real
week-calendar card via the `_today` seam, the header bar's long-form seam
date, real hero metric chips ONLY when the store carries them, the grid6
metric cards, and the page-frame sheet tokens. New fixtures are
fitness-domain only (S49 demo-data constraint).
"""

import datetime
import html as html_lib
import re
from pathlib import Path

import pytest

from scripts.generate import generate
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


def _mixed_fitness_read():
    """A mixed fitness-domain store read populating BOTH data zones: the
    bodyweight biomarker series (zone 4) plus a panel, a watch-out answer, and
    a physician-feedback note (zone 7)."""
    return _bodyweight_read() + [
        {"item": "panel::movement-screen", "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "manual", "value": "pending"},
        {"item": "watch-out::soreness-check", "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "manual", "value": "none noticed"},
        {"item": "feedback::physician-feedback",
         "timepoint": "2026-06-08T00:00:00+00:00", "source": "manual",
         "value": "keep current training block"},
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
    """The fully-awaiting zones carry NO digits anywhere; the calendar's copy is clean.

    The mechanical no-fake-numbers guard (ADR-0009 D2), rendered from an EMPTY
    store so the hero's real-metric chips (legitimate digits) cannot
    false-trip: with an empty store, EVERY digit in Readiness, Today's Plan,
    or Goals & Progress is by definition invented — so those zones are checked
    on their WHOLE tag-stripped, entity-decoded text. Readiness's awaiting
    state is the designed headline (the visual spec replaced its dashed card);
    Today's Plan and Goals & Progress keep dashed awaiting rows. This Week's
    date digits are legitimate, so it checks only its muted awaiting caption.
    """
    zones = _zones(dashboard.render([], _today=_TODAY))
    assert "Awaiting wearable baseline" in zones["Readiness"], (
        "the hero must render its awaiting headline"
    )
    for title in ("Today's Plan", "Goals & Progress"):
        assert _awaiting_texts(zones[title]), (
            f"zone {title!r} must render an awaiting card"
        )
    for title in ("Readiness", "Today's Plan", "Goals & Progress"):
        text = html_lib.unescape(re.sub(r"<[^>]*>", "", zones[title]))
        assert not re.search(r"\d", text), (
            f"fully-awaiting zone {title!r} carries a digit: {text!r}"
        )
    captions = re.findall(r"<div class='caption'>(.*?)</div>", zones["This Week"], re.S)
    awaiting = [c for c in captions if "No scheduled events" in c]
    assert awaiting, "zone 'This Week' must render its muted awaiting caption"
    for text in awaiting:
        assert not re.search(r"\d", html_lib.unescape(re.sub(r"<[^>]*>", "", text))), (
            f"awaiting caption in 'This Week' carries a digit: {text!r}"
        )


def test_accent_hexes_only_in_chrome():
    """ACCENTS hexes never color data state: no accent inside any SVG block,
    no state-* element carrying an accent inline style, and no accent anywhere
    inside the data zones' kpi-row / state-marker / value / caption fragments
    (ADR-0009 D3). Rendered from a mixed store so zones 4 AND 7 both carry
    data rows the scan covers."""
    html = dashboard.render(_mixed_fitness_read(), _today=_TODAY)
    zones = _zones(html)
    svg_blocks = re.findall(r"<svg.*?</svg>", html, re.S)
    assert svg_blocks, "the rendered dashboard must carry SVG (rings + sparkline)"
    state_tags = re.findall(r"<[^>]*class='[^']*state-[^']*'[^>]*>", html)
    assert state_tags, "the rendered dashboard must carry state-classed elements"
    data_fragments = []
    for title in ("Performance & Trends", "Labs & Bloodwork"):
        rows = zones[title].split("<div class='kpi-row'>")[1:]
        assert rows, f"data zone {title!r} must carry kpi rows"
        data_fragments.extend(rows)
        data_fragments.extend(re.findall(
            r"<[^>]*class='[^']*(?:state-marker|value|caption)[^']*'[^>]*>",
            zones[title],
        ))
    for accent in component_set.ACCENTS.values():
        for block in svg_blocks:
            assert accent not in block, f"accent {accent} leaked into an SVG block"
        for tag in state_tags:
            assert accent not in tag, f"accent {accent} leaked into a state element"
        for fragment in data_fragments:
            assert accent not in fragment, (
                f"accent {accent} leaked into a data fragment: {fragment[:120]!r}"
            )
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


@pytest.mark.parametrize("today, day_numbers, today_cell", [
    # Mid-week, mid-month: the original seam case.
    (datetime.date(2026, 6, 10),
     ["8", "9", "10", "11", "12", "13", "14"], ("day today", "Wed", "10")),
    # Monday of a month-spanning week: today is the FIRST cell.
    (datetime.date(2026, 6, 29),
     ["29", "30", "1", "2", "3", "4", "5"], ("day today", "Mon", "29")),
    # Sunday of the same month-spanning week: today is the LAST cell.
    (datetime.date(2026, 7, 5),
     ["29", "30", "1", "2", "3", "4", "5"], ("day today", "Sun", "5")),
    # A year-spanning week: the strip crosses into January.
    (datetime.date(2026, 12, 30),
     ["28", "29", "30", "31", "1", "2", "3"], ("day today", "Wed", "30")),
])
def test_calendar_strip_renders_week_with_today_marked(today, day_numbers, today_cell):
    """The week grid renders 7 real columns of the seam date's Mon-Sun week,
    and exactly the seam date's column carries the .today class + the
    `· Today` marker."""
    zone = _zones(dashboard.render([], _today=today))["This Week"]
    cells = re.findall(
        r"<div class='(day[^']*)'><div class='dhead'>([A-Za-z]+) (\d+)", zone
    )
    assert len(cells) == 7
    assert [c[1] for c in cells] == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    assert [c[2] for c in cells] == day_numbers
    today_cells = [c for c in cells if "today" in c[0]]
    assert today_cells == [today_cell]
    assert zone.count("· Today") == 1, "exactly the seam column carries the marker"


def test_fitness_marker_renders_units_and_neutral_trend():
    """A bodyweight series renders its lb units and a NEUTRAL direction-only
    arrow — polarity is None, so no good/concern trend coloring (ADR-0009 D4)."""
    html = dashboard.render(_bodyweight_read(), _today=_TODAY)
    trends = _zones(html)["Performance & Trends"]
    assert "Bodyweight" in trends
    assert "183 lb" in trends
    row = trends.split("<div class='kpi-row'>")[1]
    assert "<span class='pill tint-neutral'>" in row
    assert "&#8595;" in row, "direction-only arrow (184 -> 183 falls)"
    assert "improving" not in row
    assert "regressing" not in row


def test_production_path_renders_zone_shell(tmp_path):
    """generate.run('dashboard') over an EMPTY store emits the full zone shell.

    The production path (store read -> template -> render.emit) must deliver
    all seven decoded zone titles in design order, the hero's awaiting
    headline (zone 1's designed empty state), and awaiting cards in the
    Today's Plan, Performance & Trends, Goals & Progress, and Labs &
    Bloodwork zones (3/4/6/7).
    """
    root = tmp_path / "store"
    root.mkdir()
    path = generate.run("dashboard", _root=root, _out_dir=tmp_path / "out")
    html = path.read_text()
    titles = [
        html_lib.unescape(t) for t in re.findall(r"<h2[^>]*>([^<]*)</h2>", html)
    ]
    assert tuple(titles) == _ZONE_TITLES
    zones = _zones(html)
    assert "Awaiting wearable baseline" in zones["Readiness"], (
        "the hero must render its awaiting headline through the production path"
    )
    for title in ("Today's Plan", "Performance & Trends",
                  "Goals & Progress", "Labs & Bloodwork"):
        assert _awaiting_texts(zones[title]), (
            f"zone {title!r} must render an awaiting card through the production path"
        )


def test_empty_store_renders_awaiting_in_data_zones():
    """An empty store renders zones 4 and 7 as their own awaiting cards."""
    zones = _zones(dashboard.render([], _today=_TODAY))
    for title in ("Performance & Trends", "Labs & Bloodwork"):
        assert _awaiting_texts(zones[title]), (
            f"empty-store zone {title!r} must render an awaiting card, not an empty section"
        )
        assert "kpi-row" not in zones[title]


def _wearable_read():
    """A fitness-domain store read carrying the three hero readout markers.

    `rhr` uses the legacy unprefixed item form on purpose — the hero chip
    lookup must tolerate both forms.
    """
    return [
        {"item": "biomarker::hrv", "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "whoop", "value": 58},
        {"item": "biomarker::hrv", "timepoint": "2026-06-09T00:00:00+00:00",
         "source": "whoop", "value": 64},
        {"item": "rhr", "timepoint": "2026-06-09T00:00:00+00:00",
         "source": "whoop", "value": 49},
        {"item": "biomarker::sleep-hours", "timepoint": "2026-06-09T00:00:00+00:00",
         "source": "whoop", "value": 7.5},
    ]


def test_hero_rings_render_track_only_with_no_wearable_scoring():
    """The hero renders exactly 3 rings, each track-only: one circle (the
    light track), NO colored arc (no second circle, no dash geometry), and the
    em-dash where the value would be (ADR-0009 D2 — never a fake percentage).
    Holds with AND without store data, since wearable SCORING does not exist
    in either case."""
    for store_read in ([], _wearable_read()):
        zone = _zones(dashboard.render(store_read, _today=_TODAY))["Readiness"]
        assert zone.count("<div class='ring'>") == 3
        assert zone.count("<circle") == 3, "a track-only ring draws ONE circle"
        assert "stroke-dasharray" not in zone, "no arc without a real score"
        assert "stroke-linecap" not in zone, "no arc cap geometry without a score"
        assert len(re.findall(r"<text[^>]*>—</text>", zone)) == 3, (
            "each ring centers an em-dash in the value slot"
        )


def test_hero_metric_chips_render_only_from_stored_readings():
    """The hero chips row carries real latest readings WITH units when the
    store has them, and NO bordered chip at all when it does not (ADR-0009
    D2 in both directions)."""
    with_data = _zones(dashboard.render(_wearable_read(), _today=_TODAY))["Readiness"]
    assert "<span class='chip-b'>HRV 64 ms</span>" in with_data, "latest hrv reading"
    assert "<span class='chip-b'>RHR 49 bpm</span>" in with_data, "legacy unprefixed rhr"
    assert "<span class='chip-b'>Sleep 7.5 h</span>" in with_data
    empty = _zones(dashboard.render([], _today=_TODAY))["Readiness"]
    assert "chip-b" not in empty, "an empty store renders no metric chip"
    partial = _zones(dashboard.render(_bodyweight_read(), _today=_TODAY))["Readiness"]
    assert "chip-b" not in partial, "a non-hero marker renders no metric chip"


def test_hero_chip_latest_decided_across_both_item_forms():
    """The hero chip carries the timepoint-latest numeric when BOTH item forms
    exist, and an all-non-numeric prefixed form does not suppress the legacy
    form's chip (the or-chain regression)."""
    stale_prefixed = [
        {"item": "biomarker::rhr", "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "whoop", "value": 52},
        {"item": "rhr", "timepoint": "2026-06-09T00:00:00+00:00",
         "source": "whoop", "value": 49},
    ]
    zone = _zones(dashboard.render(stale_prefixed, _today=_TODAY))["Readiness"]
    assert "<span class='chip-b'>RHR 49 bpm</span>" in zone, (
        "the chip must carry the timepoint-latest numeric across BOTH forms"
    )
    assert "RHR 52" not in zone, "a stale prefixed reading must not shadow the newer one"

    nonnumeric_prefixed = [
        {"item": "biomarker::rhr", "timepoint": "2026-06-09T00:00:00+00:00",
         "source": "manual", "value": "redraw scheduled"},
        {"item": "rhr", "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "whoop", "value": 52},
    ]
    zone = _zones(dashboard.render(nonnumeric_prefixed, _today=_TODAY))["Readiness"]
    assert "<span class='chip-b'>RHR 52 bpm</span>" in zone, (
        "an all-non-numeric prefixed form must not suppress the legacy form's chip"
    )


def test_header_bar_carries_seam_date_long_form():
    """The header bar renders the product name, the real long-form seam date,
    the muted awaiting status pill, and the Today chip — and the old h1 is
    gone (the header bar replaced it)."""
    html = dashboard.render([], _today=_TODAY)
    assert "<header class='topbar'>" in html
    assert "A+ Maxing" in html
    assert "Wednesday · June 10, 2026" in html, "the long-form date derives from _today"
    assert "— awaiting wearable baseline" in html
    assert "<span class='chip-b'>Today</span>" in html
    assert "<h1>" not in html


def test_trends_renders_one_metric_card_per_item_in_grid6():
    """Zone 4 lays its metric cards out in the 6-column grid: one kpi-row
    card per tracked item, inside `.grid6`."""
    read = _bodyweight_read() + [
        {"item": "biomarker::steps", "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "phone", "value": 9000},
    ]
    trends = _zones(dashboard.render(read, _today=_TODAY))["Performance & Trends"]
    assert "<div class='grid6'>" in trends
    assert trends.count("<div class='kpi-row'>") == 2, "one card per item"


def test_goals_track_renders_without_fill():
    """Zone 6 renders the designed empty progress track: the track element is
    present, the fill element is NOT, and no percent renders (ADR-0009 D2)."""
    zone = _zones(dashboard.render([], _today=_TODAY))["Goals & Progress"]
    assert "<div class='track'></div>" in zone
    assert "class='fill'" not in zone
    assert "%" not in zone


def test_page_frame_sheet_tokens_present():
    """The artifact carries the app-surface page frame: the gray page-bg and
    card-border CHROME tokens in :root, and the 1140px white sheet wrap."""
    html = dashboard.render([], _today=_TODAY)
    assert "--page-bg: #F3F4F6" in html
    assert "--card-border: #E5E7EB" in html
    assert "<div class='wrap'>" in html
    assert "max-width: 1140px" in html
