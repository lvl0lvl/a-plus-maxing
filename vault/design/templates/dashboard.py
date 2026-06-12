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
  form) -> a zone-4 metric card (Trend Card v2, visual spec zone 4 as amended
  2026-06-12, beads y0h0 + i2yw): clean label + the latest reading's date,
  latest value + units when registered, the ref-range/state caption, a NUMERIC
  delta chip in the metric's own unit tinted by the polarity-aware semantic
  state (neutral without registered grounds — the ADR-0008 honesty caveat), a
  bar sparkline over ONLY the numeric values, and a naive-projection caption
  when derivable — DASHBOARD-ONLY by S52 operator direction (the physician
  report never carries an extrapolation).
  A biomarker stream with no numeric value routes to a plain value row instead.
- `panel::X` -> a pending-draw chip: clean label + the stored value verbatim
  (a `.state-marker` element inside the bordered chip).
- `watch-out::X` -> clean label + the stored answers joined `; `.
- `feedback::...` -> a `Physician Feedback` row with each entry as a note line.
- `plan::<domain>` (a `plan_schema.PLAN_DOMAINS` member) -> the zone-3 plan
  card group, carrying FULL readings (`resolve_plan` needs timepoint+source).
- `plan-track::<domain>` (a `TRACKED_DOMAINS` member) -> the zone-3 tracking
  group. An unknown plan::/plan-track:: suffix raises KeyError naming it.
- Any OTHER `::` prefix -> KeyError naming the prefix: routing for a new stream
  type is added deliberately, never by silent fallthrough (ADR-0008 D3).
- An unprefixed non-numeric item (the legacy catch-all) -> a plain clean-label +
  latest-value row.

Biomarker cards (and unprefixed numeric series) land in zone 4; panel,
watch-out, feedback, and catch-all rows land in the zone-7 strip card; plan
and tracking readings render ONLY in the zone-3 cards (ADR-0010 D5 — never
`_metric_card`, sparklines, or the labs strip). The peptide card additionally
reads the grouped watch-out answers (a second consumer of the zone-7 routed
stream, not a re-route). All
markup and colors come from `component_set` — no per-template color literals —
so the palette stays single-sourced and the `@media print` block is inherited.
A template is a callable `template(store_read) -> html_str`; `render.emit`
inlines + size-checks + asset-checks the returned markup.
"""

import datetime
import math

# Aliased: this module's template surface is itself named `render`.
from scripts.generate import render as render_engine
from scripts.store import biomarker_meta, loop_schema, plan_schema
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

# Today's-plan cards: (label, plan domain, ACCENTS key, default specialist).
# A resolved plan renders the populated anatomy attributed to ITS specialist
# (the `plan::` source); the absence states keep the default attribution and
# the designed empty anatomy (ADR-0010 D4/D5; visual spec zone 3 as amended
# 2026-06-12).
_PLAN_CARDS = (
    ("Workout", "workout", "training", "personal-trainer"),
    ("Nutrition", "nutrition", "nutrition", "nutritionist"),
    ("Supplements", "supplements", "supplements", "supplement-specialist"),
    ("Peptides", "peptides", "peptides", "peptide-specialist"),
)

# The plan-card absence-state copy, one line per published absence state
# (digit-free per the zone tests; ADR-0010 D5 — awaiting copy names what is
# missing).
_NO_PLAN_COPY = "No plan on file — record one to fill this card."
_NO_PLAN_TODAY_COPY = "Plan on file is for another day — none recorded for today."

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


def _readings_by_item(store_read):
    """Group the store read model's readings into per-item reading lists.

    Full readings, not value series: the plan routes need timepoint+source
    (`resolve_plan`'s attribution + today-resolution inputs); the other routes
    derive their value series from these lists.

    Args:
        store_read (list): The store read model (list of reading dicts).

    Returns:
        (dict) item -> list of readings, in store-read (timepoint) order.
    """
    by_item = {}
    for reading in store_read:
        by_item.setdefault(reading["item"], []).append(reading)
    return by_item


def _plain_row(label, value):
    """Render a plain label + latest-value row (no state, no sparkline)."""
    return f"<div class='kpi-row'>{cs.kpi(label, value)}</div>"


def _format_number(number):
    """Format a numeric for card chips/captions: no float noise, no trailing zeros.

    `.10g` keeps health-scale magnitudes in plain decimal while collapsing
    float artifacts (`0.30000000000000004` -> `0.3`) and integral floats
    (`3.0` -> `3`, `20.0` -> `20`).
    """
    return f"{number:.10g}"


def _reading_date(timepoint):
    """Parse a stored timepoint's date part, or None when not ISO-parseable.

    Store timepoints are ISO `YYYY-MM-DD[Thh:mm:ss…]` strings; the date is the
    first 10 chars (the render_views date-axis convention) parsed with the
    house `datetime.date.fromisoformat`. An unparseable — or non-string —
    timepoint reads None: the card renders NO date, never a raw string and
    never a crash (honest absence).
    """
    try:
        return datetime.date.fromisoformat(timepoint[:10])
    except (TypeError, ValueError):
        return None


def _short_date(day):
    """Format a date as the card's short form, e.g. `Jun 10`."""
    return f"{_MONTH_ABBR[day.month - 1]} {day.day}"


def _delta_chip(item, prev, latest):
    """Render the numeric delta chip for a >=2-point numeric series.

    The chip carries the latest-minus-prev movement in the metric's own unit
    (`▼ 0.3 mg/L`, `▲ 20 lb`; no unit suffix for an unregistered marker),
    tinted by the polarity-aware semantic state via `biomarker_meta.trend`
    (improving=good, regressing=concern, flat/no-polarity=neutral — never a
    good/bad color without registered grounds, the ADR-0008 honesty caveat).
    Equal values keep the prior flat presentation: the registered-polarity
    `flat` word pill, else the neutral direction arrow.
    """
    # Both raw-span branches below bypass cs.pill(): pill() escapes its WHOLE
    # text, which would render the arrow ENTITY as literal "&#8594;"/"&#9650;"
    # instead of the glyph. The arrow stays raw; the text half is escaped
    # individually instead.
    word = biomarker_meta.trend(item, prev, latest)
    if latest == prev:
        if word is not None:
            return cs.pill(word, _TREND_STATE[word])
        return "<span class='pill tint-neutral'>&#8594;</span>"
    state = _TREND_STATE[word] if word is not None else "neutral"
    arrow = "&#9650;" if latest > prev else "&#9660;"
    meta = biomarker_meta.get(item)
    unit = f" {meta['units']}" if meta else ""
    return (
        f"<span class='pill tint-{state}'>{arrow} "
        f"{cs._escape(f'{_format_number(abs(latest - prev))}{unit}')}</span>"
    )


def _range_caption(item, latest):
    """Render the ref-range/state caption under the card's value row.

    A registered marker with a range reads `ref {low} – {high} {units}` plus
    the latest value's range verdict (` · in range` / ` · out of range`; a
    non-numeric latest renders the range with NO verdict — no judgment
    possible). A marker without a range — registered rangeless and
    unregistered alike — collapses to the performance-metric caption: absence
    of clinical metadata is what makes it a performance metric.
    """
    meta = biomarker_meta.get(item)
    if meta is None or meta["reference_range"] is None:
        text = "no reference range · performance metric"
    else:
        low, high = meta["reference_range"]
        state = biomarker_meta.state_for(item, latest)
        suffix = {"good": " · in range", "concern": " · out of range"}.get(state, "")
        text = (
            f"ref {_format_number(low)} – {_format_number(high)} "
            f"{meta['units']}{suffix}"
        )
    return f"<div class='caption'>{cs._escape(text)}</div>"


def _projection_caption(numeric_readings, numeric, day):
    """Render the naive-projection caption, or '' when not derivable.

    DASHBOARD-ONLY (S52 operator direction): the physician report must never
    carry an extrapolation. Renders only from real stored data, when ALL of
    these hold: at least `biomarker_meta.PROJECTION_MIN_TIMEPOINTS` numeric
    readings; parseable dates on the last two of them AND on the card's
    latest reading (`day` — the same date the label row renders top-right); a
    finite projected value (the shared `biomarker_meta.projection_values`
    seam's); a projected date that computes without overflowing the calendar;
    and a projected date STRICTLY AFTER the card's latest reading date — an
    extrapolation must be a forecast, never a past- or same-day-dated claim.
    The projected date is one step beyond the latest numeric reading at the
    spacing of the last two numeric reading dates (naive, consistent with the
    value extrapolation). Otherwise NO caption — never a fabricated date or
    value.

    Args:
        numeric_readings (list): The series' numeric readings — full store
            reading dicts (`timepoint`, `value`) in store-read order.
        numeric (list): The coerced float series the card plots (one float
            per numeric reading, tail-windowed to the per-view cap; the
            projection slope reads only the last two).
        day (datetime.date | None): The card's latest-reading date — the
            `_reading_date(readings[-1])` the label row renders top-right —
            or None when that timepoint is unparseable.
    """
    if len(numeric_readings) < biomarker_meta.PROJECTION_MIN_TIMEPOINTS:
        return ""
    if day is None:
        return ""
    latest = _reading_date(numeric_readings[-1]["timepoint"])
    prev = _reading_date(numeric_readings[-2]["timepoint"])
    if latest is None or prev is None:
        return ""
    projected = biomarker_meta.projection_values(numeric)[-1]
    if not math.isfinite(projected):
        return ""
    try:
        projected_day = latest + (latest - prev)
    except OverflowError:
        return ""
    if projected_day <= day:
        return ""
    text = (
        f"→ {_format_number(projected)} by "
        f"{_short_date(projected_day)} · naive projection"
    )
    return f"<div class='caption'>{cs._escape(text)}</div>"


def _metric_card(item, readings):
    """Render one zone-4 metric card from its FULL readings (timepoint + value).

    Card anatomy (visual spec zone 4 as amended 2026-06-12, beads y0h0 +
    i2yw), top to bottom: the label row — clean label with the LATEST
    reading's date top-right (`Jun 10`; an unparseable timepoint renders no
    date); the stream's TRUE latest reading as the big value — with units
    when it is numeric and the marker is registered, verbatim with no units
    when non-numeric (ADR-0008 D3); the ref-range/state caption; the numeric
    delta chip when the series carries >=2 numeric values; the bar sparkline
    (registry-driven state over ONLY the numeric values); and the
    naive-projection caption when derivable (dashboard-only — never on the
    physician report). A stream with no numeric value routes to a plain
    value row instead.

    Args:
        item (str): The store item id (stream prefix tolerated).
        readings (list): The item's FULL readings in store-read (timepoint)
            order — dicts carrying at least `timepoint` (ISO string) and
            `value` (the stored value: numeric, numeric string, or free
            text).
    """
    # The single numeric-coercion pass: the filtered readings and their float
    # values come from one walk, shared by the chip, sparkline, and projection.
    numeric_readings, numeric = [], []
    for reading in readings:
        number = biomarker_meta.to_number(reading["value"])
        if number is not None:
            numeric_readings.append(reading)
            numeric.append(number)
    label = biomarker_meta.display_name(item)
    if not numeric_readings:
        return _plain_row(label, readings[-1]["value"])
    # Tail-window to the pinned per-view cap (single-sourced per ADR-0004): the
    # bar envelope is fixed-width, so an uncapped series computes negative bars.
    numeric = numeric[-render_engine.MAX_TIMEPOINTS_PER_VIEW:]
    latest_reading = readings[-1]["value"]
    meta = biomarker_meta.get(item)
    if meta and biomarker_meta.to_number(latest_reading) is not None:
        shown = f"{latest_reading} {meta['units']}"
    else:
        shown = str(latest_reading)
    day = _reading_date(readings[-1]["timepoint"])
    top_right = _short_date(day) if day is not None else None
    state = cs.state_for(item, numeric[-1])
    chip = _delta_chip(item, numeric[-2], numeric[-1]) if len(numeric) >= 2 else ""
    projection = _projection_caption(numeric_readings, numeric, day)
    return (
        "<div class='kpi-row'>"
        f"{cs.kpi(label, shown, top_right=top_right)}"
        f"{_range_caption(item, latest_reading)}"
        f"{chip}"
        f"{cs.bar_sparkline(numeric, state)}"
        f"{projection}"
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


def _set_dots(total, filled, accent_hex):
    """Render an exercise's per-set progress dots: filled accent, rest border-gray.

    Non-text chrome (ADR-0010 D5): the filled count is the TRACKED sets-done
    for the exercise (0 when untracked — an unfilled dot IS the honest
    absence); fills draw only the existing accent / card-border hexes.
    """
    dots = (
        f"<span class='setdot' style='background:{accent_hex}'></span>" * filled
        + f"<span class='setdot' style='background:{cs.CHROME['card-border']}'></span>"
        * (total - filled)
    )
    return f"<span class='setdots'>{dots}</span>"


def _btnfill(text, accent_key):
    """Render an inert accent-filled button (no href, no script; ADR-0004).

    The fill is the CHROME `*-text` shade of the card accent — the hex already
    AA-measured >= 4.5 against its ~10% tint, so paper text on the SAME hex
    measures higher still (the tint is darker than paper; the contrast ratio
    is symmetric) — never a new color pair.
    """
    return (
        f"<span class='btnfill' style='background:{cs.CHROME[accent_key + '-text']}'>"
        f"{cs._escape(text)}</span>"
    )


def _workout_empty(copy):
    """Render the workout card's designed empty anatomy: stat row + dashed row.

    The populated-card labels govern both states (visual spec supersession):
    four stat boxes — Elapsed / Volume / Sets done / Heart rate, all em-dash,
    the heart-rate box on the neutral state tint (no reading, no judgment).
    """
    boxes = (
        cs.stat_box("Elapsed") + cs.stat_box("Volume") + cs.stat_box("Sets done")
        + cs.stat_box("Heart rate", tint="neutral")
    )
    return f"<div class='statrow'>{boxes}</div>{cs.awaiting(copy)}"


def _nutrition_empty(copy):
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
    return f"<div class='statrow'>{boxes}</div>{macros}{cs.awaiting(copy)}"


def _list_empty(copy):
    """Render the supplements/peptides empty list area: the dashed row only."""
    return cs.awaiting(copy)


# domain -> the card's designed empty-state body builder (visual spec zone 3),
# taking the absence-state copy line.
_EMPTY_BODIES = {
    "workout": _workout_empty,
    "nutrition": _nutrition_empty,
    "supplements": _list_empty,
    "peptides": _list_empty,
}


def _workout_populated(plan, tracking):
    """Render the workout card's populated anatomy from plan + tracking snapshot.

    Slot-level honesty (ADR-0010 D5): every tracked slot renders only from a
    PRESENT tracking field — an absent operand is an em-dash / unfilled dot /
    omitted chip, never 0. The sets-done box renders only when the snapshot
    carries `sets_done`; its numerator sums the snapshot counts for the PLAN's
    exercise names only (the supplements counter's taken ∩ plan rule — an
    unknown key never inflates the claim); a per-exercise sets_done above its
    planned sets raises (never a silently capped claim); sets_done keys
    matching no plan exercise render no row. The
    heart-rate box is live-state tinted (`cs.stat_box(tint=...)`); the
    rest-timer footer and Resume button are static inert chrome.

    Args:
        plan (dict): The resolved workout plan document.
        tracking (dict | None): The day's tracking snapshot, or None.

    Returns:
        (str) The card body markup.

    Raises:
        ValueError: An exercise's tracked sets_done exceeds its planned sets.
    """
    tracking = tracking if tracking is not None else {}
    exercises = plan["exercises"]
    sets_done = tracking.get("sets_done")
    if sets_done is not None:
        for exercise in exercises:
            done = sets_done.get(exercise["name"], 0)
            if done > exercise["sets"]:
                raise ValueError(
                    f"sets_done {done} exceeds the planned {exercise['sets']} "
                    f"sets for {exercise['name']!r}"
                )
        sets_value = (
            f"{sum(sets_done.get(e['name'], 0) for e in exercises)}"
            f"/{sum(e['sets'] for e in exercises)}"
        )
    else:
        sets_value = "—"
    elapsed = f"{tracking['elapsed_min']} min" if "elapsed_min" in tracking else "—"
    volume = f"{tracking['volume_lb']} lb" if "volume_lb" in tracking else "—"
    hr = tracking.get("heart_rate_bpm")
    boxes = (
        cs.stat_box("Elapsed", elapsed) + cs.stat_box("Volume", volume)
        + cs.stat_box("Sets done", sets_value)
        + cs.stat_box(
            "Heart rate",
            f"{hr} bpm" if hr is not None else "—",
            tint=cs.state_for("heart-rate", hr),
        )
    )
    chips = [
        cs.chip_b(text.format(tracking[field]))
        for field, text in (
            ("steps", "{} steps"), ("kcal_burned", "{} kcal"),
            ("exercise_min", "{} min exercise"),
        )
        if field in tracking
    ]
    chips_row = f"<div class='chips'>{''.join(chips)}</div>" if chips else ""
    done_by_name = sets_done if sets_done is not None else {}
    rows = []
    for exercise in exercises:
        parts = [str(exercise[f]) for f in ("load", "reps") if f in exercise]
        caption = (
            f"<span class='caption'>{cs._escape(' × '.join(parts))}</span>"
            if parts else ""
        )
        detail = (
            f"<div class='caption'>{cs._escape(exercise['detail'])}</div>"
            if "detail" in exercise else ""
        )
        rows.append(
            "<div class='prow'>"
            f"<span class='plabel'>{cs._escape(exercise['name'])}</span>"
            f"{caption}"
            f"{_set_dots(exercise['sets'], done_by_name.get(exercise['name'], 0), cs.ACCENTS['training'])}"
            f"</div>{detail}"
        )
    footer = (
        "<div class='resttimer'><span class='caption'>Rest timer —</span>"
        f"{_btnfill('Resume', 'training')}</div>"
    )
    return f"<div class='statrow'>{boxes}</div>{chips_row}{''.join(rows)}{footer}"


def _fill_track(label, value, target, unit):
    """Render one labeled value/target track (macros, water).

    The caption carries the TRUE numbers (`{label} {v} / {t} {unit}`; an
    untracked value reads `— / {t}` with no fill — never a 0 default); the
    fill geometry clamps to 0-100% (nutrition accent hex, non-text chrome):
    a negative width is invalid CSS a browser DROPS, which would render a
    FULL bar.
    """
    if value is None:
        caption = f"{label} — / {target} {unit}"
        bar = cs.track_bar()
    else:
        caption = f"{label} {value} / {target} {unit}"
        bar = cs.track_bar(
            round(max(0.0, min(100, value / target * 100)), 1),
            cs.ACCENTS["nutrition"],
        )
    return f"<div class='macro'><div class='caption'>{cs._escape(caption)}</div>{bar}</div>"


def _nutrition_populated(plan, tracking):
    """Render the nutrition card's populated anatomy from plan + tracking snapshot.

    Slot-level honesty (ADR-0010 D5): Goal comes from the plan; Food/Exercise
    only from present tracking fields; Remaining = goal − food + exercise ONLY
    when all three operands exist (an absent operand is NOT 0 — the slot reads
    em-dash). Macro and water tracks caption true numbers; the meals checklist
    marks logged meals with the PALETTE-good check, the first unlogged meal
    `Up next`, later unlogged meals an inert `Log` chip; `Add food` is inert
    muted link-text.

    Args:
        plan (dict): The resolved nutrition plan document.
        tracking (dict | None): The day's tracking snapshot, or None.

    Returns:
        (str) The card body markup.
    """
    tracking = tracking if tracking is not None else {}
    goal = plan["calorie_goal"]
    food = tracking.get("food_kcal")
    exercise = tracking.get("exercise_kcal")
    remaining = (
        goal - food + exercise if food is not None and exercise is not None else "—"
    )
    boxes = (
        cs.stat_box("Goal", goal)
        + cs.stat_box("Food", food if food is not None else "—")
        + cs.stat_box("Exercise", exercise if exercise is not None else "—")
        + cs.stat_box("Remaining", remaining, tinted=True)
    )
    macros_g = tracking.get("macros_g", {})
    tracks = "".join(
        _fill_track(label, macros_g.get(key), plan["macros"][key], "g")
        for label, key in (
            ("Protein", "protein"), ("Carbs", "carbs"), ("Fat", "fat"),
        )
    )
    logged = set(tracking.get("meals_logged", ()))
    rows = ["<div class='caption'>Today's meals · from your plan</div>"]
    up_next_taken = False
    for meal in plan["meals"]:
        if meal["name"] in logged:
            marker = "<span class='state-good'>✓</span>"
        elif not up_next_taken:
            marker = cs.chip_b("Up next")
            up_next_taken = True
        else:
            marker = cs.chip_b("Log")
        contents = (
            f"<span class='caption'>{cs._escape(meal['contents'])}</span>"
            if "contents" in meal else ""
        )
        kcal = (
            f"<span class='caption'>{cs._escape(str(meal['kcal']))} kcal</span>"
            if "kcal" in meal else ""
        )
        rows.append(
            "<div class='prow'>"
            f"<span class='plabel'>{cs._escape(meal['name'])}</span>"
            f"{contents}{kcal}{marker}</div>"
        )
    rows.append("<span class='linkish'>Add food</span>")
    water = (
        _fill_track("Water", tracking.get("water_l"), plan["water_l"], "L")
        if "water_l" in plan else ""
    )
    return f"<div class='statrow'>{boxes}</div>{tracks}{''.join(rows)}{water}"


def _supplements_populated(plan, tracking):
    """Render the supplements card's populated anatomy from plan + tracking.

    The counter chip distinguishes the explicit none-taken snapshot from no
    snapshot (ADR-0010 D4): `{"taken": []}` reads `0 of m taken` on the card
    accent tint; NO snapshot reads the muted `— of m taken` — never a 0
    default. The taken count is the intersection with the plan's item names.
    Rows: name, dose caption, timing chip when present, the PALETTE-good check
    when taken else an unfilled marker dot.

    Args:
        plan (dict): The resolved supplements plan document.
        tracking (dict | None): The day's tracking snapshot, or None.

    Returns:
        (str) The card body markup.
    """
    items = plan["items"]
    names = {entry["name"] for entry in items}
    if tracking is None:
        taken = frozenset()
        counter = cs.pill(f"— of {len(items)} taken")
    else:
        taken = frozenset(tracking["taken"])
        counter = cs.pill(f"{len(taken & names)} of {len(items)} taken", "supplements")
    rows = []
    for entry in items:
        marker = (
            "<span class='state-good'>✓</span>"
            if entry["name"] in taken
            else f"<span class='setdot' style='background:{cs.CHROME['card-border']}'></span>"
        )
        timing = cs.chip_b(entry["timing"]) if "timing" in entry else ""
        rows.append(
            "<div class='prow'>"
            f"<span class='plabel'>{cs._escape(entry['name'])}</span>"
            f"<span class='caption'>{cs._escape(entry['dose'])}</span>"
            f"{timing}{marker}</div>"
        )
    return f"<div class='prow'>{counter}</div>{''.join(rows)}"


def _peptides_populated(plan, watchout_answers):
    """Render the peptides card's populated anatomy from plan + watch-out answers.

    Protocol line `{compound} · {dose} · {route}`; the week caption renders
    only when BOTH cycle fields are present; tags render as plain bordered
    chips (no tint — no special `experimental` styling is invented). The
    watch-out rows derive from `loop_schema.derive_watchout_questions` over
    the plan's compound and read the GROUPED zone-7 watch-out answers (second
    consumer, not a re-route): an answered question shows its latest answer as
    a bordered chip, an unanswered one an inert accent `Answer` button. The
    optional evidence field renders as inert link-styled muted caption.

    Args:
        plan (dict): The resolved peptides plan document.
        watchout_answers (dict): watch-out name -> stored answer values.

    Returns:
        (str) The card body markup.
    """
    protocol = f"{plan['compound']} · {plan['dose']} · {plan['route']}"
    parts = [f"<div class='label'>{cs._escape(protocol)}</div>"]
    if "cycle_week" in plan and "cycle_length_weeks" in plan:
        parts.append(
            f"<div class='caption'>Week {cs._escape(str(plan['cycle_week']))} of "
            f"{cs._escape(str(plan['cycle_length_weeks']))}</div>"
        )
    if plan.get("tags"):
        parts.append(
            f"<div class='prow'>{''.join(cs.chip_b(tag) for tag in plan['tags'])}</div>"
        )
    for question in sorted(loop_schema.derive_watchout_questions([plan["compound"]])):
        answers = watchout_answers.get(question)
        control = (
            cs.chip_b(str(answers[-1])) if answers else _btnfill("Answer", "peptides")
        )
        parts.append(
            "<div class='prow'>"
            f"<span class='plabel'>{cs._escape(biomarker_meta.display_name(question))}</span>"
            f"{control}</div>"
        )
    if "evidence" in plan:
        parts.append(f"<span class='linkish'>{cs._escape(plan['evidence'])}</span>")
    return "".join(parts)


def _plan_card(label, domain, accent_key, default_specialist,
               plan_readings, track_readings, watchout_answers, on_date):
    """Render one today's-plan card per the visual-spec anatomy.

    Resolves the domain's plan for `on_date` (ADR-0010 D4): a resolved plan
    renders the populated anatomy attributed `via` ITS specialist (from the
    `plan::` source, not the static default) under an accent-tinted `today`
    status pill; either absence state renders the designed empty anatomy, the
    muted `awaiting plan` pill, and its own dashed-row copy. Accents color
    chrome only — text inside stays ink/muted (ADR-0009 D3).

    Args:
        label (str): The card title text (escaped).
        domain (str): The `plan_schema.PLAN_DOMAINS` member the card renders.
        accent_key (str): The `ACCENTS` key coloring the card chrome.
        default_specialist (str): The `via` attribution for the absence states.
        plan_readings (dict): domain -> the `plan::<domain>` full readings.
        track_readings (dict): domain -> the `plan-track::<domain>` readings.
        watchout_answers (dict): watch-out name -> stored answer values (the
            peptide card's second-consumer read of the zone-7 stream).
        on_date (str): The render date plans resolve against, YYYY-MM-DD.

    Raises:
        ValueError: The workout tracking claims more sets done than planned.
    """
    accent = cs.ACCENTS[accent_key]
    resolved = plan_schema.resolve_plan(plan_readings.get(domain, []), on_date)
    if resolved["state"] is None:
        specialist = resolved["specialist"]
        pill = cs.pill("today", accent_key)
        tracking = plan_schema.resolve_tracking(track_readings.get(domain, []), on_date)
        if domain == "workout":
            body = _workout_populated(resolved["plan"], tracking)
        elif domain == "nutrition":
            body = _nutrition_populated(resolved["plan"], tracking)
        elif domain == "supplements":
            body = _supplements_populated(resolved["plan"], tracking)
        else:
            body = _peptides_populated(resolved["plan"], watchout_answers)
    else:
        specialist = default_specialist
        pill = cs.pill("awaiting plan")
        copy = (
            _NO_PLAN_COPY if resolved["state"] == plan_schema.NO_PLAN
            else _NO_PLAN_TODAY_COPY
        )
        body = _EMPTY_BODIES[domain](copy)
    head = (
        "<div class='pchead'>"
        f"<span class='dot' style='background:{accent}'></span>"
        f"<span class='ptitle' style='color:{accent}'>{cs._escape(label)}</span>"
        f"<span class='caption'>via {cs._escape(specialist)}</span>"
        f"{pill}"
        "</div>"
    )
    return f"<div class='card pcard pc-{accent_key}'>{head}{body}</div>"


def _plan_zone(plan_readings, track_readings, watchout_answers, today):
    """Render zone 3 — today's plan: the 2x2 specialist-attributed card grid.

    Args:
        plan_readings (dict): domain -> the `plan::<domain>` full readings.
        track_readings (dict): domain -> the `plan-track::<domain>` readings.
        watchout_answers (dict): watch-out name -> stored answer values (the
            peptide card's second-consumer read of the zone-7 stream).
        today (datetime.date): The seam date plans resolve against (D4).
    """
    on_date = today.isoformat()
    cards = "".join(
        _plan_card(*card, plan_readings, track_readings, watchout_answers, on_date)
        for card in _PLAN_CARDS
    )
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
        KeyError: An item carries a `::` prefix outside the routed stream
            types, or an unknown plan::/plan-track:: domain suffix (fail-loud;
            ADR-0008 D3).
        ValueError: A workout tracking snapshot claims more sets done than the
            plan schedules for an exercise (never a silently capped claim).
    """
    by_item = _readings_by_item(store_read)
    biomarkers, panels, watchouts, feedback, other = [], [], [], [], []
    plan_readings, track_readings, watchout_answers = {}, {}, {}
    for item in sorted(by_item):
        readings = by_item[item]
        values = [r["value"] for r in readings]
        if item.startswith("biomarker::"):
            biomarkers.append(_metric_card(item, readings))
        elif item.startswith("panel::"):
            panels.append(_panel_chip(item, values))
        elif item.startswith("watch-out::"):
            watchouts.append(_watchout_row(item, values))
            # Second consumer, not a re-route: the peptide plan card reads the
            # same grouped answers for its watch-out rows (ADR-0010 D5).
            watchout_answers[item[len("watch-out::"):]] = values
        elif item.startswith("feedback::"):
            feedback.append(_feedback_row(values))
        elif item.startswith("plan-track::"):
            domain = item[len("plan-track::"):]
            if domain not in plan_schema.TRACKED_DOMAINS:
                raise KeyError(
                    f"unrouted plan-track:: domain {domain!r}: routing for a new "
                    f"stream type is added deliberately, never by silent fallthrough"
                )
            track_readings[domain] = readings
        elif item.startswith("plan::"):
            domain = item[len("plan::"):]
            if domain not in plan_schema.PLAN_DOMAINS:
                raise KeyError(
                    f"unrouted plan:: domain {domain!r}: routing for a new "
                    f"stream type is added deliberately, never by silent fallthrough"
                )
            plan_readings[domain] = readings
        elif "::" in item:
            prefix = item.split("::", 1)[0] + "::"
            raise KeyError(
                f"unrouted stream prefix {prefix!r}: routing for a new stream "
                f"type is added deliberately, never by silent fallthrough"
            )
        elif all(biomarker_meta.to_number(value) is not None for value in values):
            biomarkers.append(_metric_card(item, readings))
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
        _plan_zone(plan_readings, track_readings, watchout_answers, today),
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
