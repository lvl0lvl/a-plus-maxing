"""Dashboard template — the 7-zone "Today" command center (ADR-0009).

Assembles the approved dashboard visual (`vault/design/dashboard-v1-design.md`
zone semantics, `vault/design/dashboard-v1-visual-spec.md` visual language) as
a white app-surface sheet on a gray page: a header bar (product name, real
long-form date, status pill), then seven zones — hero readiness (rings +
readout), week calendar card, today's plan 2x2 cards, performance & trends
metric-card grid, care team, goals & progress, and the labs & bloodwork strip.
Zones whose data models do not exist yet render designed chrome with explicit
empty states (track-only rings, em-dash stat slots, unfilled tracks) naming
WHAT is missing — never an invented number (ADR-0009 D2, 2026-06-11
amendment). Zone/card chrome draws from `component_set.ACCENTS` and the
neutral CHROME tokens; data state stays exclusively the semantic PALETTE
(ADR-0009 D3).

The ADR-0008 D3 routing contract is preserved verbatim: each store item group
routes by its stream prefix, so no string value reaches numeric viz by
construction:

- `biomarker::X` (and an unprefixed all-numeric series, the legacy direct-append
  form) -> a zone-4 metric card: clean label, latest value + units when
  registered, real registry-driven state, a tinted trend pill (the polarity
  word when registered, else a direction-only arrow on the neutral tint — the
  ADR-0008 honesty caveat), and a bar sparkline over ONLY the numeric values.
  A biomarker stream with no numeric value routes to a plain value row instead.
- `panel::X` -> a pending-draw chip: clean label + the stored value verbatim
  (a `.state-marker` element inside the bordered chip).
- `watch-out::X` -> clean label + the stored answers joined `; `.
- `feedback::...` -> a `Physician Feedback` row with each entry as a note line.
- Any OTHER `::` prefix -> KeyError naming the prefix: routing for a new stream
  type is added deliberately, never by silent fallthrough (ADR-0008 D3).
- An unprefixed non-numeric item (the legacy catch-all) -> a plain clean-label +
  latest-value row.

Biomarker cards (and unprefixed numeric series) land in zone 4; panel,
watch-out, feedback, and catch-all rows land in the zone-7 strip card. All
markup and colors come from `component_set` — no per-template color literals —
so the palette stays single-sourced and the `@media print` block is inherited.
A template is a callable `template(store_read) -> html_str`; `render.emit`
inlines + size-checks + asset-checks the returned markup.
"""

import datetime

# Aliased: this module's template surface is itself named `render`.
from scripts.generate import render as render_engine
from scripts.store import biomarker_meta
from vault.design.templates import component_set as cs

# Trend word -> the semantic state coloring it: a registered-polarity verdict is
# a real value judgment (improving reads good, regressing reads concern); flat
# carries no judgment and reads neutral.
_TREND_STATE = {"improving": "good", "flat": "neutral", "regressing": "concern"}

# Locale-independent date names: weekday abbreviations for the week-calendar
# grid, full day/month names for the header bar's long-form date, and month
# abbreviations for the calendar's week range.
_WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_DAY_NAMES = (
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
)
_MONTH_NAMES = (
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
)
_MONTH_ABBR = (
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
)

# Hero readout chips: (display label, registry marker). Each renders ONLY when
# the store carries a numeric reading for the marker (ADR-0009 D2).
_HERO_CHIPS = (("HRV", "hrv"), ("RHR", "rhr"), ("Sleep", "sleep-hours"))

# Today's-plan cards: (label, ACCENTS key, attributed specialist). Each renders
# its designed empty-state anatomy until the plan-content schemas land
# (ADR-0009 zone 3; visual spec zone 3).
_PLAN_CARDS = (
    ("Workout", "training", "personal-trainer"),
    ("Nutrition", "nutrition", "nutritionist"),
    ("Supplements", "supplements", "supplement-specialist"),
    ("Peptides", "peptides", "peptide-specialist"),
)

# The shared plan-card empty-state copy (digit-free per the zone tests).
_AWAITING_PLAN = "No plan on file — plan-content schemas are the next slice."

# The calendar legend's event categories: (label, pill tint name). Training
# rides its ACCENTS tint; the other three are the CHROME event-category tints
# (visual spec zone 2 as amended 2026-06-11) — chrome, never data state.
_EVENT_LEGEND = (
    ("Training", "training"),
    ("Lab draw", "lab-draw"),
    ("Check-in", "check-in"),
    ("Appointment", "appointment"),
)

# The week-nav calendar glyph: a tiny inline SVG (muted chrome stroke — no
# accent hex, so the accent-confinement SVG scan stays clean; the box is a
# <path>, not <rect>, so the sparkline bar-cap rect count never picks it up).
_CAL_GLYPH = (
    "<svg class='calglyph' width='14' height='14' viewBox='0 0 14 14' "
    "role='img' aria-label='calendar'>"
    f"<path d='M1 2.75 h12 v10.25 h-12 z M1 5.5 h12' fill='none' "
    f"stroke='{cs.PALETTE['muted']}' stroke-width='1.5'/>"
    "</svg>"
)

# (slug, display name, what it tracks) — mirrors the deployed roster at
# `.claude/agents/`, excluding the 4 internal build/review roles (they track no
# operator data); replaced when a rollup model lands (ADR-0009 D2/consequences).
_SPECIALISTS = (
    ("cardiovascular-specialist", "Cardiovascular Specialist", "Cardio fitness and heart-rate trends"),
    ("dermatologist", "Dermatologist", "Skin observations and follow-ups"),
    ("endocrine-specialist", "Endocrine Specialist", "Hormone and metabolic markers"),
    ("genetics-specialist", "Genetics Specialist", "Genetic context and DTC results"),
    ("gi-specialist", "GI Specialist", "Digestive health and gut symptoms"),
    ("labs-specialist", "Labs Specialist", "Lab panels and bloodwork results"),
    ("longevity-strategist", "Longevity Strategist", "Long-horizon health strategy"),
    ("lymphatic-specialist", "Lymphatic Specialist", "Lymphatic health observations"),
    ("medical-liaison", "Medical Liaison", "Clinician visits and records"),
    ("mental-performance-coach", "Mental Performance Coach", "Focus, stress, and mindset"),
    ("nutritionist", "Nutritionist", "Diet, macros, and meal plans"),
    ("peptide-specialist", "Peptide Specialist", "Peptide protocols and check-ins"),
    ("personal-trainer", "Personal Trainer", "Training plans and session logs"),
    ("recovery-specialist", "Recovery Specialist", "Recovery, soreness, and readiness"),
    ("sleep-coach", "Sleep Coach", "Sleep duration and quality"),
    ("supplement-specialist", "Supplement Specialist", "Supplement stack and timing"),
)


def _series_by_item(store_read):
    """Group the store read model's readings into per-item value series.

    Args:
        store_read (list): The store read model (list of reading dicts).

    Returns:
        (dict) item -> list of values, in store-read (timepoint) order.
    """
    series = {}
    for reading in store_read:
        series.setdefault(reading["item"], []).append(reading["value"])
    return series


def _plain_row(label, value):
    """Render a plain label + latest-value row (no state, no sparkline)."""
    return f"<div class='kpi-row'>{cs.kpi(label, value)}</div>"


def _trend_chip(item, prev, latest):
    """Render the trend pill for a >=2-point numeric series.

    A registered-polarity marker renders the trend WORD (improving / flat /
    regressing) as a pill tinted by its own semantic state; an unregistered
    marker renders a direction-only arrow on the neutral tint — never a
    good/bad color without registered grounds (the ADR-0008 honesty caveat).
    """
    word = biomarker_meta.trend(item, prev, latest)
    if word is not None:
        return cs.pill(word, _TREND_STATE[word])
    arrow = "&#8593;" if latest > prev else "&#8595;" if latest < prev else "&#8594;"
    # Raw span, not cs.pill(): pill() escapes its text, which would render the
    # arrow ENTITY as literal "&#8593;" instead of the arrow glyph.
    return f"<span class='pill tint-neutral'>{arrow}</span>"


def _metric_card(item, values):
    """Render one zone-4 metric card from its value series.

    Card anatomy (visual spec zone 4), top to bottom: clean label; the
    stream's TRUE latest reading as the big value — with units when it is
    numeric and the marker is registered, verbatim with no units when
    non-numeric (ADR-0008 D3); a tinted trend pill when the series carries
    >=2 numeric values; and the bar sparkline (registry-driven state over
    ONLY the numeric values) at the card bottom. A stream with no numeric
    value routes to a plain value row instead.
    """
    numeric = [
        n for value in values if (n := biomarker_meta.to_number(value)) is not None
    ]
    label = biomarker_meta.display_name(item)
    if not numeric:
        return _plain_row(label, values[-1])
    # Tail-window to the pinned per-view cap (single-sourced per ADR-0004): the
    # bar envelope is fixed-width, so an uncapped series computes negative bars.
    numeric = numeric[-render_engine.MAX_TIMEPOINTS_PER_VIEW:]
    latest_reading = values[-1]
    meta = biomarker_meta.get(item)
    if meta and biomarker_meta.to_number(latest_reading) is not None:
        shown = f"{latest_reading} {meta['units']}"
    else:
        shown = str(latest_reading)
    state = cs.state_for(item, numeric[-1])
    chip = _trend_chip(item, numeric[-2], numeric[-1]) if len(numeric) >= 2 else ""
    return (
        "<div class='kpi-row'>"
        f"{cs.kpi(label, shown)}"
        f"{chip}"
        f"{cs.bar_sparkline(numeric, state)}"
        "</div>"
    )


def _label_cell(label):
    """Render the label cell shared by the panel / watch-out / feedback rows."""
    return f"<div class='kpi'><div class='label'>{cs._escape(label)}</div></div>"


def _panel_chip(item, values):
    """Render a pending-draw chip: clean label + the stored value verbatim.

    The state stays a `.state-marker` element inside the bordered chip (the
    ADR-0008 panel-state contract, restyled per visual spec zone 7). Built as
    a raw span rather than via `cs.chip_b` because chip_b escapes its WHOLE
    text argument — the nested state-marker element needs raw construction
    (each text piece is escaped individually instead).
    """
    return (
        "<span class='chip-b'>"
        f"{cs._escape(biomarker_meta.display_name(item))} "
        f"<span class='state-marker'>{cs._escape(str(values[-1]))}</span></span>"
    )


def _watchout_row(item, values):
    """Render a watch-out row: clean label + the stored answers joined '; '."""
    answers = "; ".join(cs._escape(str(value)) for value in values)
    return (
        "<div class='kpi-row'>"
        f"{_label_cell(biomarker_meta.display_name(item))}"
        f"<div class='value'>{answers}</div>"
        "</div>"
    )


def _feedback_row(values):
    """Render the physician-feedback row: one note line per stored entry."""
    notes = "".join(
        f"<div class='caption'>{cs._escape(str(value))}</div>" for value in values
    )
    return f"<div class='kpi-row'>{_label_cell('Physician Feedback')}{notes}</div>"


def _latest_numeric_reading(store_read, marker):
    """Return a marker's latest numeric reading across both item forms, or None.

    Tolerates the `biomarker::`-prefixed and legacy unprefixed item forms
    TOGETHER: the latest is decided by timepoint over the MERGED readings of
    both forms, so a stale reading in one form never shadows a newer one in
    the other, and an all-non-numeric prefixed form never suppresses the
    legacy form's numeric.

    Args:
        store_read (list): The store read model (list of reading dicts).
        marker (str): The registry marker name (unprefixed).
    """
    forms = (f"biomarker::{marker}", marker)
    readings = sorted(
        (r for r in store_read if r["item"] in forms),
        key=lambda r: r["timepoint"],
    )
    for reading in reversed(readings):
        if biomarker_meta.to_number(reading["value"]) is not None:
            return reading["value"]
    return None


def _topbar(today):
    """Render the header bar: product name + long-form date, status pill + chip.

    The status pill carries the awaiting state until wearable scoring exists
    (ADR-0009 D2); the date is real data from the same `_today` seam the
    calendar uses.

    Args:
        today (datetime.date): The seam date the long-form date renders.
    """
    date_text = (
        f"{_DAY_NAMES[today.weekday()]} · {_MONTH_NAMES[today.month - 1]} "
        f"{today.day}, {today.year}"
    )
    return (
        "<header class='topbar'>"
        "<div><div class='product'>A+ Maxing</div>"
        f"<div class='date'>{cs._escape(date_text)}</div></div>"
        f"<div>{cs.pill('— awaiting wearable baseline')} {cs.chip_b('Today')}</div>"
        "</header>"
    )


def _hero_zone(store_read):
    """Render zone 1 — readiness hero: track-only rings + the designed readout.

    Wearable recovery/sleep/strain scoring is LM-02-gated, so the rings render
    track-only (no arc, em-dash value slot — never a fake percentage, ADR-0009
    D2) and the readout headline IS the awaiting state. The chips row carries
    ONLY real latest store readings (`_HERO_CHIPS` markers) with registered
    units; a marker with no numeric reading renders no chip. Ring colors per
    the visual spec: Recovery = PALETTE good, Sleep = ACCENTS sleep, Strain =
    ACCENTS training (chrome around a value, not data state — D3).

    Args:
        store_read (list): The store read model (list of reading dicts).
    """
    rings = "".join(
        cs.progress_ring(label, value=None, color=color)
        for label, color in (
            ("Recovery", cs.PALETTE["good"]),
            ("Sleep", cs.ACCENTS["sleep"]),
            ("Strain", cs.ACCENTS["training"]),
        )
    )
    chips = []
    for label, marker in _HERO_CHIPS:
        reading = _latest_numeric_reading(store_read, marker)
        if reading is not None:
            units = biomarker_meta.get(marker)["units"]
            chips.append(cs.chip_b(f"{label} {reading} {units}"))
    chips_row = f"<div class='chips'>{''.join(chips)}</div>" if chips else ""
    readout = (
        "<div class='readout'>"
        "<div class='headline'>Awaiting wearable baseline</div>"
        "<div class='caption'>Recovery, sleep, and strain scoring arrives "
        "with the first thirty-day wearable window.</div>"
        f"{chips_row}"
        "</div>"
    )
    body = f"<div class='card hero'><div class='rings'>{rings}</div>{readout}</div>"
    return cs.zone("Readiness", body)


def _week_range(monday, sunday):
    """Format a Mon-Sun week's real date range, e.g. `Jun 8 – 14`.

    A month-spanning week names both months (`Jun 29 – Jul 5`).
    """
    if monday.month == sunday.month:
        return f"{_MONTH_ABBR[monday.month - 1]} {monday.day} – {sunday.day}"
    return (
        f"{_MONTH_ABBR[monday.month - 1]} {monday.day} – "
        f"{_MONTH_ABBR[sunday.month - 1]} {sunday.day}"
    )


def _navbtn(symbol):
    """Render an inert square bordered chevron button (no behavior yet)."""
    return f"<span class='navbtn'>{cs._escape(symbol)}</span>"


def _month_calendar(today):
    """Render zone 2's ONE month calendar — the week row IS a month row.

    The full grid of `today`'s month in the week strip's Mon-Sun order: a
    weekday header strip (`wkhead` of `mhead` abbrevs), then one `wkrow` per
    real week from the Monday on/before the 1st through the Sunday on/after
    the month's last day. Every row is the SAME 7-cell markup (`dcell`, day
    number top-corner): leading/trailing other-month days muted (`dout`),
    today's cell tinted with the bolded `{day} · Today` marker, every cell
    empty of events (none exist yet). The current week's row carries `wk-now`
    (always visible); every other row carries `wk-hide` (hidden until the
    header caret's `:checked` rule reveals them in place — visual spec zone 2,
    amended 2026-06-11 Walter iteration 2).

    Args:
        today (datetime.date): The date whose month the calendar renders.
    """
    monday = today - datetime.timedelta(days=today.weekday())
    first = today.replace(day=1)
    start = first - datetime.timedelta(days=first.weekday())
    # day 1 + 32 days always lands in the next month, whatever the length.
    last = (first + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    end = last + datetime.timedelta(days=6 - last.weekday())
    head = "".join(f"<div class='mhead'>{wd}</div>" for wd in _WEEKDAYS)
    rows = [f"<div class='wkhead'>{head}</div>"]
    week = start
    while week <= end:
        cells = []
        for offset in range(7):
            day = week + datetime.timedelta(days=offset)
            klass = "dcell"
            if day.month != today.month:
                klass += " dout"
            num = str(day.day)
            if day == today:
                klass += " today"
                num += " · Today"
            cells.append(f"<div class='{klass}'><span class='dnum'>{num}</span></div>")
        row_klass = "wkrow wk-now" if week == monday else "wkrow wk-hide"
        rows.append(f"<div class='{row_klass}'>{''.join(cells)}</div>")
        week += datetime.timedelta(days=7)
    return f"<div class='cal'>{''.join(rows)}</div>"


def _calendar_zone(today):
    """Render zone 2 — the month calendar collapsed to `today`'s Mon-Sun week.

    Per the visual spec as amended 2026-06-11, Walter iteration 2: "the week
    view is actually just hiding the rest of the month's calendar." Header
    left: calendar glyph + `This week` + the week nav shaped `‹ Jun 8 – 14 ›`
    (inert square chevron buttons flanking the real range). Header right: the
    four event-category legend pills, each in its OWN tint; the inert
    `‹ Month ›` nav; then the expand control — a `<label>` caret chip pinned
    in the header in BOTH states. Body: ONE contiguous month grid
    (`_month_calendar`) whose non-current `wk-hide` rows are hidden by
    default; the caret's hidden checkbox `:checked` sibling rule reveals them
    in place — zero scripts (ADR-0004 single-file rule intact), normal
    document flow, so expanding pushes every zone beneath DOWN, never
    overlays. The muted awaiting caption stays under the grid. Date math is
    real data from the seam; the events stay an awaiting state until a
    calendar/event model exists.

    Args:
        today (datetime.date): The date whose week the calendar renders.
    """
    monday = today - datetime.timedelta(days=today.weekday())
    week_range = _week_range(monday, monday + datetime.timedelta(days=6))
    # The zero-script reveal mechanism: this hidden checkbox is the card's
    # FIRST child so the `~` sibling selectors reach the label and the grid.
    toggle = "<input type='checkbox' id='calx' class='calx'>"
    wknav = (
        "<div class='wknav'>"
        f"{_CAL_GLYPH}<span class='card-title'>This week</span>"
        f"{_navbtn('‹')}<span class='caption'>{cs._escape(week_range)}</span>{_navbtn('›')}"
        "</div>"
    )
    legend = "".join(cs.pill(label, tint) for label, tint in _EVENT_LEGEND)
    evlegend = (
        f"<div class='evlegend'>{legend}"
        f"{_navbtn('‹')}<span class='caption'>Month</span>{_navbtn('›')}"
        "<label for='calx' class='calbtn' aria-label='expand to month view'>"
        "<span class='x-closed'>⌄</span><span class='x-open'>⌃</span></label>"
        "</div>"
    )
    caption = (
        "<div class='caption'>No scheduled events — the calendar model is "
        "pending.</div>"
    )
    return cs.zone(
        "This Week",
        f"<div class='card calcard'>{toggle}{wknav}{evlegend}"
        f"{_month_calendar(today)}{caption}</div>",
    )


def _workout_body():
    """Render the workout card's designed empty anatomy: stat row + empty list.

    Four em-dash stat boxes (the last accent-tinted via the card's CSS
    context), then the dashed empty-state row (visual spec zone 3).
    """
    boxes = (
        cs.stat_box("Elapsed") + cs.stat_box("Volume") + cs.stat_box("Sets")
        + cs.stat_box("Heart rate", tinted=True)
    )
    return f"<div class='statrow'>{boxes}</div>{cs.awaiting(_AWAITING_PLAN)}"


def _nutrition_body():
    """Render the nutrition card's designed empty anatomy.

    The calorie-arithmetic stat row (Goal − Food + Exercise = Remaining, all
    em-dash, Remaining tinted), three empty macro tracks, then the dashed
    empty-state row (visual spec zone 3).
    """
    boxes = (
        cs.stat_box("Goal") + cs.stat_box("Food") + cs.stat_box("Exercise")
        + cs.stat_box("Remaining", tinted=True)
    )
    macros = "".join(
        f"<div class='macro'><div class='caption'>{m} —</div>{cs.track_bar()}</div>"
        for m in ("Protein", "Carbs", "Fat")
    )
    return f"<div class='statrow'>{boxes}</div>{macros}{cs.awaiting(_AWAITING_PLAN)}"


def _list_body():
    """Render the supplements/peptides items-list area: the dashed empty row only."""
    return cs.awaiting(_AWAITING_PLAN)


# label -> the card's designed empty-state body builder (visual spec zone 3).
_PLAN_BODIES = {
    "Workout": _workout_body,
    "Nutrition": _nutrition_body,
    "Supplements": _list_body,
    "Peptides": _list_body,
}


def _plan_card(label, accent_key, specialist):
    """Render one today's-plan card per the visual-spec anatomy.

    Header row: accent glyph dot + accent-colored title + `via <specialist>`
    muted caption + the muted `awaiting plan` status pill; then the card's
    designed empty-state body. Accents color chrome only — text inside stays
    ink/muted (ADR-0009 D3).
    """
    accent = cs.ACCENTS[accent_key]
    head = (
        "<div class='pchead'>"
        f"<span class='dot' style='background:{accent}'></span>"
        f"<span class='ptitle' style='color:{accent}'>{cs._escape(label)}</span>"
        f"<span class='caption'>via {cs._escape(specialist)}</span>"
        f"{cs.pill('awaiting plan')}"
        "</div>"
    )
    return f"<div class='card pcard pc-{accent_key}'>{head}{_PLAN_BODIES[label]()}</div>"


def _plan_zone():
    """Render zone 3 — today's plan: the 2x2 specialist-attributed card grid."""
    cards = "".join(_plan_card(*card) for card in _PLAN_CARDS)
    return cs.zone(
        "Today's Plan",
        f"<div class='grid2'>{cards}</div>",
        subtitle="Your training, fuel, and protocol for today — built from "
        "your goals, attributed to each specialist.",
    )


def _care_team_zone():
    """Render zone 5 — the 16 domain-specialist compact cards, 4-column grid.

    Per-card anatomy (visual spec zone 5): glyph dot + name, tracks line,
    status line. The status stays the muted "no rollup yet" until a
    per-specialist rollup model exists (ADR-0009 zone 5).
    """
    cards = "".join(
        "<div class='card'>"
        f"<div class='label'><span class='dot'></span>{cs._escape(name)}</div>"
        f"<div class='body'>{cs._escape(tracks)}</div>"
        "<div class='caption'>no rollup yet</div>"
        "</div>"
        for _slug, name, tracks in _SPECIALISTS
    )
    return cs.zone(
        "Your Care Team",
        f"<div class='grid4'>{cards}</div>",
        subtitle="What each specialist tracks for you — every claim "
        "attributed and evidence-gated.",
    )


def render(store_read, _today=None):
    """Assemble the 7-zone type-routed dashboard HTML from the shared component set.

    Args:
        store_read (list): The store read model passed through by render.emit.
        _today (datetime.date, optional): Test-only calendar seam; defaults to
            the current date.

    Returns:
        (str) The assembled dashboard HTML (single document, inline styling).

    Raises:
        KeyError: An item carries a `::` prefix outside the four routed stream
            types (fail-loud; ADR-0008 D3).
    """
    series = _series_by_item(store_read)
    biomarkers, panels, watchouts, feedback, other = [], [], [], [], []
    for item in sorted(series):
        values = series[item]
        if item.startswith("biomarker::"):
            biomarkers.append(_metric_card(item, values))
        elif item.startswith("panel::"):
            panels.append(_panel_chip(item, values))
        elif item.startswith("watch-out::"):
            watchouts.append(_watchout_row(item, values))
        elif item.startswith("feedback::"):
            feedback.append(_feedback_row(values))
        elif "::" in item:
            prefix = item.split("::", 1)[0] + "::"
            raise KeyError(
                f"unrouted stream prefix {prefix!r}: routing for a new stream "
                f"type is added deliberately, never by silent fallthrough"
            )
        elif all(biomarker_meta.to_number(value) is not None for value in values):
            biomarkers.append(_metric_card(item, values))
        else:
            other.append(_plain_row(biomarker_meta.display_name(item), values[-1]))

    # Zone 4 — REAL: the routed biomarker metric cards in the 6-column grid;
    # the legend sits in zone 4 — the one zone whose cards carry data-state
    # colors — beside the colors it explains. Empty -> its own awaiting card.
    trends_body = (
        cs.legend() + f"<div class='grid6'>{''.join(biomarkers)}</div>"
        if biomarkers
        else cs.awaiting("No tracked readings yet.")
    )
    # Zone 7 — REAL: one compact strip card — the pending-draw chips row, then
    # the routed watch-out/feedback rows; unprefixed non-numeric items (the
    # legacy catch-all) land here too.
    pending = (
        f"<div class='pending'><span class='caption'>Pending draws:</span> {''.join(panels)}</div>"
        if panels
        else ""
    )
    labs_inner = pending + "".join(watchouts + feedback + other)
    labs_body = "<div class='card strip'>{}</div>".format(
        labs_inner
        or cs.awaiting("No lab results, watch-outs, or notes on file yet.")
    )
    today = _today if _today is not None else datetime.date.today()
    zones = (
        _hero_zone(store_read),
        _calendar_zone(today),
        _plan_zone(),
        cs.zone(
            "Performance & Trends",
            trends_body,
            subtitle="How you're tracking — recent readings per metric.",
        ),
        _care_team_zone(),
        cs.zone(
            "Goals & Progress",
            f"<div class='goal-row'>{cs.track_bar()}</div>"
            + cs.awaiting("No goals on file — the goal-progress model is pending."),
            subtitle="Where each goal stands.",
        ),
        cs.zone(
            "Labs & Bloodwork",
            labs_body,
            subtitle="Clinical detail — the supporting layer under your plan.",
        ),
    )
    body = (
        "<div class='wrap'>"
        f"{_topbar(today)}"
        f"{''.join(zones)}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{cs.head('Health Dashboard')}<body>{body}</body></html>"
