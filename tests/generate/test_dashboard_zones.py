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


def _calendar_rows(zone):
    """Parse zone 2's month grid into (row_class, [(cell_class, dnum), ...]).

    Cells are matched on the FULL cell markup shape, so a cell whose markup
    diverges from `<div class='dcell...'><span class='dnum'>...</span></div>`
    simply does not parse — the count asserts catch it.
    """
    cal = re.search(r"<div class='cal'>.*", zone, re.S).group(0)
    parts = re.split(r"<div class='(wkrow[^']*)'>", cal)
    return [
        (klass, re.findall(
            r"<div class='(dcell[^']*)'><span class='dnum'>([^<]*)</span></div>",
            body,
        ))
        for klass, body in zip(parts[1::2], parts[2::2])
    ]


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
    # Accent-CATEGORY tint classes are chrome too: a `tint-training`-class pill
    # inside a data fragment would dress data state in category chrome just as
    # surely as the raw hex (state tints good/concern/neutral stay allowed).
    # The event-category tints (lab-draw/check-in/appointment, calendar legend
    # chrome) are banned from data fragments on the same grounds.
    accent_tint_re = re.compile(
        r"tint-(?:training|nutrition|supplements|peptides|sleep"
        r"|lab-draw|check-in|appointment)"
    )
    for fragment in data_fragments:
        leak = accent_tint_re.search(fragment)
        assert leak is None, (
            f"accent tint class {leak.group(0)!r} leaked into a data fragment: "
            f"{fragment[:120]!r}"
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


@pytest.mark.parametrize("today, day_numbers, range_text", [
    # Mid-week, mid-month: the original seam case.
    (datetime.date(2026, 6, 10),
     ["8", "9", "10", "11", "12", "13", "14"], "Jun 8 – 14"),
    # Monday of a month-spanning week: today is the FIRST cell.
    (datetime.date(2026, 6, 29),
     ["29", "30", "1", "2", "3", "4", "5"], "Jun 29 – Jul 5"),
    # Sunday of the same month-spanning week: today is the LAST cell.
    (datetime.date(2026, 7, 5),
     ["29", "30", "1", "2", "3", "4", "5"], "Jun 29 – Jul 5"),
    # A year-spanning week: the row crosses into January.
    (datetime.date(2026, 12, 30),
     ["28", "29", "30", "31", "1", "2", "3"], "Dec 28 – Jan 3"),
])
def test_calendar_strip_renders_week_with_today_marked(
    today, day_numbers, range_text
):
    """The collapsed week view IS the month calendar's current-week row: the
    MON-SUN weekday header strip, then exactly ONE `wk-now` row carrying the
    seam date's Mon-Sun week (7 day-number cells; today's cell tinted with
    the bolded `{day} · Today` marker, exactly once in the whole zone) — plus
    the rendered date-range string, the inert navbtn chevrons, the `Month`
    nav label, and the four legend pills each on its OWN tint."""
    zone = _zones(dashboard.render([], _today=today))["This Week"]
    assert re.findall(r"<div class='mhead'>([A-Za-z]+)</div>", zone) == [
        "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
    ], "the weekday header strip keeps the Mon-Sun order"
    rows = _calendar_rows(zone)
    now_rows = [cells for klass, cells in rows if klass == "wkrow wk-now"]
    assert len(now_rows) == 1, "exactly one row is the current week"
    cells = now_rows[0]
    assert len(cells) == 7
    marker = f"{today.day} · Today"
    assert [n.replace(" · Today", "") for _k, n in cells] == day_numbers
    today_cells = [(k, n) for k, n in cells if "today" in k]
    assert today_cells == [("dcell today", marker)], (
        "exactly the seam date's cell is tinted and `· Today`-marked"
    )
    assert zone.count("· Today") == 1, "exactly the seam cell carries the marker"
    # The header carries the real rendered week range (month-/year-spanning
    # weeks name both months), the navbtn chevrons (week nav + month nav),
    # the Month nav label, and the four event-category legend pills, each on
    # its OWN tint class.
    assert f"<span class='caption'>{range_text}</span>" in zone
    assert zone.count("<span class='navbtn'>‹</span>") == 2
    assert zone.count("<span class='navbtn'>›</span>") == 2
    assert "<span class='caption'>Month</span>" in zone
    for label, tint in (("Training", "training"), ("Lab draw", "lab-draw"),
                        ("Check-in", "check-in"), ("Appointment", "appointment")):
        assert f"<span class='pill tint-{tint}'>{label}</span>" in zone


def test_calendar_week_nav_chevrons_flank_the_range():
    """The header-left week nav is shaped `‹ Jun 8 – 14 ›`: inside the wknav
    fragment a navbtn chevron sits BEFORE the range span and one AFTER it
    (asserted by index, not mere presence)."""
    zone = _zones(dashboard.render([], _today=_TODAY))["This Week"]
    wknav = re.search(r"<div class='wknav'>.*?</div>", zone, re.S).group(0)
    prev_at = wknav.find("<span class='navbtn'>‹</span>")
    range_at = wknav.find("<span class='caption'>Jun 8 – 14</span>")
    next_at = wknav.find("<span class='navbtn'>›</span>")
    assert prev_at != -1 and range_at != -1 and next_at != -1, wknav
    assert prev_at < range_at < next_at, (
        f"week nav must read ‹ range ›, got indexes {prev_at}/{range_at}/{next_at}"
    )
    assert "This week" in wknav
    assert "<svg class='calglyph'" in wknav, "the calendar glyph leads the nav"


def test_calendar_legend_pills_carry_own_tints():
    """Each event-category legend pill rides its OWN tint class — training on
    the ACCENTS tint, the other three on the CHROME event-category tints."""
    zone = _zones(dashboard.render([], _today=_TODAY))["This Week"]
    for label, tint in (("Training", "training"), ("Lab draw", "lab-draw"),
                        ("Check-in", "check-in"), ("Appointment", "appointment")):
        assert f"<span class='pill tint-{tint}'>{label}</span>" in zone, (
            f"legend pill {label!r} must carry tint-{tint}"
        )


def test_calendar_month_nav_sits_on_the_header_right():
    """The header-right group carries the legend pills, then the inert
    `‹ Month ›` nav (navbtn + label + navbtn, in that order), then the caret
    label — the expand control stays pinned in the header in both states."""
    zone = _zones(dashboard.render([], _today=_TODAY))["This Week"]
    ev = re.search(r"<div class='evlegend'>.*?</div>", zone, re.S).group(0)
    assert ev.count("class='pill") == 4, "the four legend pills lead the group"
    prev_at = ev.find("<span class='navbtn'>‹</span>")
    label_at = ev.find("<span class='caption'>Month</span>")
    next_at = ev.find("<span class='navbtn'>›</span>")
    caret_at = ev.find("<label for='calx'")
    assert -1 < prev_at < label_at < next_at < caret_at, (
        f"the group must read ‹ Month › then the caret, got indexes "
        f"{prev_at}/{label_at}/{next_at}/{caret_at}"
    )


@pytest.mark.parametrize("today, in_month, lead, trail", [
    # June 2026 opens ON a Monday: 30 days, no lead, 5 trailing July days.
    (datetime.date(2026, 6, 10), 30, 0, 5),
    (datetime.date(2026, 6, 29), 30, 0, 5),
    # July 2026 starts mid-week (Wed): 31 days, 2 leading June, 2 trailing Aug.
    (datetime.date(2026, 7, 5), 31, 2, 2),
    # December 2026 starts Tue and ends Thu: 1 leading Nov, 3 trailing Jan.
    (datetime.date(2026, 12, 30), 31, 1, 3),
])
def test_calendar_month_grid_renders_full_month_in_place(today, in_month, lead, trail):
    """Zone 2 renders ONE month grid (no separate expand panel): whole weeks
    x 7 of the seam month, the right in-month day-cell count, the exact muted
    lead/trail other-month cells in Mon-Sun reading order, today's cell
    highlighted exactly once, and every cell digit-bearing but EMPTY of event
    content."""
    zone = _zones(dashboard.render([], _today=today))["This Week"]
    assert zone.count("<div class='cal'>") == 1, "exactly ONE calendar grid"
    rows = _calendar_rows(zone)
    for _klass, row_cells in rows:
        assert len(row_cells) == 7, "every row is a whole week x 7"
    cells = [cell for _klass, row_cells in rows for cell in row_cells]
    assert len(cells) == zone.count("'dnum'"), "every cell is day-number only"
    marker = f"{today.day} · Today"
    for klass, num in cells:
        assert re.fullmatch(r"\d+", num) or num == marker, (
            f"cell {klass!r} carries event content: {num!r}"
        )
    muted_flags = ["dout" in klass for klass, _num in cells]
    assert muted_flags.count(False) == in_month
    assert muted_flags[:lead] == [True] * lead and not muted_flags[lead], (
        f"expected exactly {lead} muted leading other-month cells"
    )
    assert muted_flags[-trail:] == [True] * trail if trail else True
    assert not muted_flags[-(trail + 1)], (
        f"expected exactly {trail} muted trailing other-month cells"
    )
    todays = [(klass, num) for klass, num in cells if "today" in klass]
    assert todays == [("dcell today", marker)], (
        "exactly the seam date's cell is highlighted in the month grid"
    )


def test_calendar_reveal_is_checkbox_label_css_no_script():
    """The month reveal is the zero-script mechanism (visual spec zone 2,
    Walter iteration 2): a hidden checkbox FIRST in the card (so the `~`
    sibling rules reach the label and the grid), the header `<label>` caret
    referencing its id, the `:checked` reveal rule + hidden-by-default rule
    in the CSS — and NO `<details>` and NO `<script>` anywhere."""
    html = dashboard.render([], _today=_TODAY)
    zone = _zones(html)["This Week"]
    checkbox = "<input type='checkbox' id='calx' class='calx'>"
    assert checkbox in zone
    assert "<label for='calx'" in zone, "the caret label drives the checkbox"
    card_at = zone.find("<div class='card calcard'>")
    box_at = zone.find(checkbox)
    legend_at = zone.find("<div class='evlegend'>")
    grid_at = zone.find("<div class='cal'>")
    assert -1 < card_at < box_at < legend_at < grid_at, (
        "the checkbox precedes the label's group and the grid as a sibling"
    )
    assert ".calx { display: none; }" in html, "the checkbox itself never shows"
    assert ".cal .wk-hide { display: none; }" in html, "non-current rows hide by default"
    assert ".calx:checked ~ .cal .wk-hide { display: grid; }" in html, (
        "the :checked sibling rule reveals the hidden rows in place"
    )
    assert "<details" not in html, "the separate details/summary expand is gone"
    assert "<script" not in html, "the reveal ships zero scripts (ADR-0004)"


def test_calendar_hidden_rows_are_same_cells_as_current_week():
    """The week view IS a month-calendar row — 'literally exactly the same':
    exactly ONE row carries `wk-now` (and holds today's cell), every other
    row carries `wk-hide`, and the hidden rows' cells ride the IDENTICAL cell
    markup/class as the current week's (`dcell`, modulo the today/other-month
    modifiers)."""
    rows = _calendar_rows(_zones(dashboard.render([], _today=_TODAY))["This Week"])
    assert {klass for klass, _cells in rows} == {"wkrow wk-now", "wkrow wk-hide"}
    assert [klass for klass, _cells in rows].count("wkrow wk-now") == 1
    for klass, cells in rows:
        base_classes = {
            cell_klass.replace(" dout", "").replace(" today", "")
            for cell_klass, _num in cells
        }
        assert base_classes == {"dcell"}, (
            f"row {klass!r} cells diverge from the shared markup: {base_classes}"
        )
        if klass == "wkrow wk-now":
            assert any("today" in c for c, _n in cells), (
                "the current-week row holds today's cell"
            )
        else:
            assert not any("today" in c for c, _n in cells)


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


def test_plan_zone_renders_designed_card_anatomy():
    """Zone 3 renders the 2x2 grid of four specialist-attributed cards with
    the designed empty-state anatomy (visual spec zone 3): per card the accent
    glyph dot, the `via <specialist>` caption, and the `awaiting plan` pill;
    Workout's four em-dash stat boxes (Heart rate tinted); Nutrition's
    calorie-arithmetic row plus exactly three empty macro tracks."""
    zone = _zones(dashboard.render([], _today=_TODAY))["Today's Plan"]
    assert "<div class='grid2'>" in zone
    cards = re.findall(r"<div class='card pcard pc-([a-z]+)'>", zone)
    assert cards == ["training", "nutrition", "supplements", "peptides"]
    assert zone.count("<span class='dot' style='background:#") == 4
    for specialist in ("personal-trainer", "nutritionist",
                       "supplement-specialist", "peptide-specialist"):
        assert f"<span class='caption'>via {specialist}</span>" in zone
    assert zone.count("<span class='pill'>awaiting plan</span>") == 4
    # Workout: the 4-slot stat row, all em-dash values, the LAST box tinted.
    workout = zone.split("<div class='card pcard pc-")[1]
    boxes = re.findall(
        r"<div class='(stat[^']*)'><div class='slabel'>([^<]*)</div>"
        r"<div class='sval'>([^<]*)</div></div>", workout
    )
    assert [(klass, label) for klass, label, _v in boxes] == [
        ("stat", "Elapsed"), ("stat", "Volume"), ("stat", "Sets"),
        ("stat tinted", "Heart rate"),
    ]
    assert all(value == "—" for _k, _l, value in boxes)
    # Nutrition: Goal/Food/Exercise/Remaining + exactly 3 empty macro tracks.
    nutrition = zone.split("<div class='card pcard pc-")[2]
    assert re.findall(r"<div class='slabel'>([^<]*)</div>", nutrition) == [
        "Goal", "Food", "Exercise", "Remaining",
    ]
    assert nutrition.count("<div class='macro'>") == 3
    assert nutrition.count("<div class='track'></div>") == 3
    assert "class='fill'" not in nutrition, "empty macro tracks carry no fill"


def test_populated_hero_non_chip_text_is_digit_free():
    """With wearable readings stored, every digit in the Readiness zone lives
    in a real-data metric chip: stripping the chip-b fragments leaves a
    digit-free remainder (ADR-0009 D2 — no invented score rides in beside the
    real chips)."""
    zone = _zones(dashboard.render(_wearable_read(), _today=_TODAY))["Readiness"]
    without_chips = re.sub(r"<span class='chip-b'>.*?</span>", "", zone)
    text = html_lib.unescape(re.sub(r"<[^>]*>", "", without_chips))
    assert not re.search(r"\d", text), (
        f"non-chip hero text carries a digit: {text!r}"
    )


def test_watchout_only_store_renders_no_pending_draws_row():
    """A labs strip holding only a watch-out (no panel:: items) renders NO
    `Pending draws:` row."""
    watchout_only = [
        {"item": "watch-out::soreness-check",
         "timepoint": "2026-06-08T00:00:00+00:00",
         "source": "manual", "value": "none noticed"},
    ]
    labs = _zones(dashboard.render(watchout_only, _today=_TODAY))["Labs & Bloodwork"]
    assert "none noticed" in labs, "the watch-out row must render"
    assert "Pending draws:" not in labs, (
        "no panel items -> no Pending-draws row"
    )


# zone title -> the designed subtitle copy (visual spec per-zone clauses).
_ZONE_SUBTITLES = {
    "Today's Plan": "Your training, fuel, and protocol for today — built from "
                    "your goals, attributed to each specialist.",
    "Performance & Trends": "How you're tracking — recent readings per metric.",
    "Your Care Team": "What each specialist tracks for you — every claim "
                      "attributed and evidence-gated.",
    "Goals & Progress": "Where each goal stands.",
    "Labs & Bloodwork": "Clinical detail — the supporting layer under your plan.",
}


def test_zone_subtitles_and_hero_caption_pin_designed_copy():
    """Each zone's subtitle and the hero readout caption carry the designed
    copy verbatim (visual spec per-zone clauses); zones 1-2 carry no subtitle
    by design."""
    zones = _zones(dashboard.render([], _today=_TODAY))
    for title, subtitle in _ZONE_SUBTITLES.items():
        m = re.search(r"<div class='subtitle'>(.*?)</div>", zones[title])
        assert m, f"zone {title!r} must carry its subtitle"
        assert html_lib.unescape(m.group(1)) == subtitle
    for title in ("Readiness", "This Week"):
        assert "class='subtitle'" not in zones[title]
    captions = [
        html_lib.unescape(c)
        for c in re.findall(r"<div class='caption'>([^<]*)</div>", zones["Readiness"])
    ]
    assert (
        "Recovery, sleep, and strain scoring arrives with the first "
        "thirty-day wearable window."
    ) in captions, "the hero readout caption must carry the designed copy"
