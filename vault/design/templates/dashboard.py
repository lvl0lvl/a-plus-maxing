"""Dashboard template — the type-routed at-a-glance view (ADR-0008 D3).

Routes each store item group by its stream prefix, so no string value reaches
numeric viz by construction:

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

Sections render biomarkers (sorted) first, then panels, watch-outs, feedback,
and other rows. All markup and colors come from `component_set` — no
per-template color literals — so the palette stays single-sourced and the
`@media print` block is inherited. A template is a callable
`template(store_read) -> html_str`; `render.emit` inlines + size-checks +
asset-checks the returned markup.
"""

# Aliased: this module's template surface is itself named `render`.
from scripts.generate import render as render_engine
from scripts.store import biomarker_meta
from vault.design.templates import component_set as cs

# Trend word -> the semantic state coloring it: a registered-polarity verdict is
# a real value judgment (improving reads good, regressing reads concern); flat
# carries no judgment and reads neutral.
_TREND_STATE = {"improving": "good", "flat": "neutral", "regressing": "concern"}


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


def render(store_read):
    """Assemble the type-routed dashboard HTML from the shared component set.

    Args:
        store_read (list): The store read model passed through by render.emit.

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
    rows = biomarkers + panels + watchouts + feedback + other
    body = (
        "<div class='wrap'>"
        "<h1>Health Dashboard</h1>"
        f"{cs.tldr_banner('At-a-glance value-over-time across tracked items.')}"
        f"{cs.legend()}"
        f"{''.join(rows)}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{cs.head('Health Dashboard')}<body>{body}</body></html>"
