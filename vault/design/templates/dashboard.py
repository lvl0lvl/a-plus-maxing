"""Dashboard template — the 7-zone "Today" command center (ADR-0009).

Assembles the approved dashboard visual (`vault/design/dashboard-v1-design.md`)
as seven zones: hero readiness, week calendar, today's plan, performance &
trends, care team, goals & progress, and the labs & bloodwork strip. Zones
whose data models do not exist yet render an explicit awaiting-state card
naming WHAT is missing — never an invented number (ADR-0009 D2). Zone/card
chrome draws from `component_set.ACCENTS`; data state stays exclusively the
semantic PALETTE (ADR-0009 D3).

The ADR-0008 D3 routing contract is preserved verbatim: each store item group
routes by its stream prefix, so no string value reaches numeric viz by
construction:

- `biomarker::X` (and an unprefixed all-numeric series, the legacy direct-append
  form) -> a KPI row: clean label, latest value + units when registered, real
  registry-driven state, a bar sparkline over ONLY the numeric values, and a
  trend chip (the polarity word when registered, else a direction-only arrow
  with the neutral class — the ADR-0008 honesty caveat). A biomarker stream
  with no numeric value routes to a plain value row instead of the sparkline.
- `panel::X` -> a state-marker row: clean label + the stored value verbatim.
- `watch-out::X` -> clean label + the stored answers joined `; `.
- `feedback::...` -> a `Physician Feedback` row with each entry as a note line.
- Any OTHER `::` prefix -> KeyError naming the prefix: routing for a new stream
  type is added deliberately, never by silent fallthrough (ADR-0008 D3).
- An unprefixed non-numeric item (the legacy catch-all) -> a plain clean-label +
  latest-value row.

Biomarker rows (and unprefixed numeric series) land in zone 4; panel,
watch-out, feedback, and catch-all rows land in zone 7. All markup and colors
come from `component_set` — no per-template color literals — so the palette
stays single-sourced and the `@media print` block is inherited. A template is
a callable `template(store_read) -> html_str`; `render.emit` inlines +
size-checks + asset-checks the returned markup.
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

# Locale-independent weekday abbreviations for the week-calendar strip.
_WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# Today's-plan cards: (label, ACCENTS key, attributed specialist). Each renders
# an awaiting state until the plan-content schemas land (ADR-0009 zone 3).
_PLAN_CARDS = (
    ("Workout", "training", "personal-trainer"),
    ("Nutrition", "nutrition", "nutritionist"),
    ("Supplements", "supplements", "supplement-specialist"),
    ("Peptides", "peptides", "peptide-specialist"),
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
    """Render the trend chip for a >=2-point numeric series.

    A registered-polarity marker renders the trend WORD (improving / flat /
    regressing) colored by its own semantic state; an unregistered marker
    renders a direction-only arrow with the neutral class — never a good/bad
    color without registered grounds (the ADR-0008 honesty caveat).
    """
    word = biomarker_meta.trend(item, prev, latest)
    if word is not None:
        return f"<span class='chip state-{_TREND_STATE[word]}'>{cs._escape(word)}</span>"
    arrow = "&#8593;" if latest > prev else "&#8595;" if latest < prev else "&#8594;"
    return f"<span class='chip state-neutral'>{arrow}</span>"


def _biomarker_row(item, values):
    """Render one biomarker KPI row from its value series.

    Clean label; the stream's TRUE latest reading as the headline — with units
    when it is numeric and the marker is registered, verbatim with no units
    when non-numeric (ADR-0008 D3); registry-driven state judged on the latest
    NUMERIC value; a bar sparkline over ONLY the numeric values; and a trend
    chip when the series carries >=2 numeric values. A stream with no numeric
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
        f"{cs.bar_sparkline(numeric, state)}"
        f"{chip}"
        "</div>"
    )


def _label_cell(label):
    """Render the label cell shared by the panel / watch-out / feedback rows."""
    return f"<div class='kpi'><div class='label'>{cs._escape(label)}</div></div>"


def _panel_row(item, values):
    """Render a panel state-marker row: clean label + the stored value verbatim."""
    return (
        "<div class='kpi-row'>"
        f"{_label_cell(biomarker_meta.display_name(item))}"
        f"<span class='state-marker'>{cs._escape(str(values[-1]))}</span>"
        "</div>"
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


def _hero_zone():
    """Render zone 1 — readiness: ring scaffolds + the awaiting state.

    Wearable recovery/sleep/strain scoring is LM-02-gated, so the hero renders
    outline-only ring scaffolds and the explicit awaiting copy — no fake
    percentage, ever (ADR-0009 D2).
    """
    rings = "".join(cs.ring_scaffold(label) for label in ("Recovery", "Sleep", "Strain"))
    body = f"<div>{rings}</div>" + cs.awaiting(
        "Awaiting wearable baseline — recovery, sleep, and strain scoring "
        "arrives with the first thirty-day wearable window."
    )
    return cs.zone("Readiness", body, accent=cs.ACCENTS["sleep"])


def _calendar_zone(today):
    """Render zone 2 — the real Mon-Sun strip of `today`'s week.

    Date math is real data (not an awaiting fake); the events row below it is
    an awaiting state until a calendar/event model exists.

    Args:
        today (datetime.date): The date whose week the strip renders.
    """
    monday = today - datetime.timedelta(days=today.weekday())
    cells = []
    for offset in range(7):
        day = monday + datetime.timedelta(days=offset)
        klass = "day today" if day == today else "day"
        cells.append(
            f"<div class='{klass}'>{_WEEKDAYS[day.weekday()]}<br>{day.day}</div>"
        )
    strip = f"<div class='cal'>{''.join(cells)}</div>"
    return cs.zone(
        "This Week",
        strip + cs.awaiting("No scheduled events — the calendar model is pending."),
    )


def _plan_card(label, accent_key, specialist):
    """Render one today's-plan card: accent-chromed label + attribution + awaiting.

    Card chrome (top border, label color) uses the surface-category accent;
    text inside stays ink/muted (ADR-0009 D3).
    """
    accent = cs.ACCENTS[accent_key]
    return (
        f"<div class='card' style='border-top: 3px solid {accent}'>"
        f"<div class='label' style='color: {accent}'>{cs._escape(label)}</div>"
        f"<div class='caption'>{cs._escape(specialist)}</div>"
        f"{cs.awaiting('No plan on file — plan-content schemas are the next slice.')}"
        "</div>"
    )


def _plan_zone():
    """Render zone 3 — today's plan: the four specialist-attributed cards."""
    cards = "".join(_plan_card(*card) for card in _PLAN_CARDS)
    return cs.zone("Today's Plan", f"<div class='cards'>{cards}</div>")


def _care_team_zone():
    """Render zone 5 — the 16 domain-specialist cards in a 4-column grid.

    Per-card status stays the muted "no rollup yet" until a per-specialist
    rollup model exists (ADR-0009 zone 5).
    """
    cards = "".join(
        "<div class='card'>"
        f"<div class='label'>{cs._escape(name)}</div>"
        f"<div class='body'>{cs._escape(tracks)}</div>"
        "<div class='caption'>no rollup yet</div>"
        "</div>"
        for _slug, name, tracks in _SPECIALISTS
    )
    return cs.zone("Your Care Team", f"<div class='grid4'>{cards}</div>")


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
            biomarkers.append(_biomarker_row(item, values))
        elif item.startswith("panel::"):
            panels.append(_panel_row(item, values))
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
            biomarkers.append(_biomarker_row(item, values))
        else:
            other.append(_plain_row(biomarker_meta.display_name(item), values[-1]))

    # Zone 4 — REAL: the routed biomarker rows; the legend renders here because
    # only zones 4 and 7 carry data-state colors. Empty -> its own awaiting card.
    trends_body = (
        cs.legend() + "".join(biomarkers)
        if biomarkers
        else cs.awaiting("No tracked readings yet.")
    )
    # Zone 7 — REAL: the routed panel/watch-out/feedback rows; unprefixed
    # non-numeric items (the legacy catch-all) land here too.
    labs_rows = panels + watchouts + feedback + other
    labs_body = (
        "".join(labs_rows)
        if labs_rows
        else cs.awaiting("No lab results, watch-outs, or notes on file yet.")
    )
    today = _today if _today is not None else datetime.date.today()
    zones = (
        _hero_zone(),
        _calendar_zone(today),
        _plan_zone(),
        cs.zone("Performance & Trends", trends_body),
        _care_team_zone(),
        cs.zone(
            "Goals & Progress",
            cs.awaiting("No goals on file — the goal-progress model is pending."),
        ),
        cs.zone("Labs & Bloodwork", labs_body),
    )
    tldr = "Today's plan and how you're tracking against it — readiness at a glance."
    body = (
        "<div class='wrap'>"
        "<h1>Health Dashboard</h1>"
        f"{cs.tldr_banner(tldr)}"
        f"{''.join(zones)}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{cs.head('Health Dashboard')}<body>{body}</body></html>"
