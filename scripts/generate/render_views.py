"""Biomarker-matrix + projection render-time views (ADR-0007-T2).

The terminal sink of the V1 DAG. `render_views(root, ...)` recomputes the biomarker
matrix and naive projections from stored timepoints AT RENDER TIME, reading operator
data only through the ADR-0002-T1 store read model (surfaced by `loop_schema`), and
assembles them through the ADR-0004-T1 `render.emit` engine + the single
`component_set` shared component def. It maps the ADR-0007-T1 store states 1:1 to
rendered state and keeps each artifact under the ADR-0004-T0 cap. It CONSUMES five
published interfaces (the T1 store-state contract, the T1 render engine + component
library, the T0 cap, the T1 store read model, the T1 egress guard) and publishes no
new broadly-reused interface.

Local-only by construction: it opens no network and runs no model step — it reads the
store and writes self-contained local HTML files.
"""

from scripts.generate import render
from scripts.store import loop_schema
from vault.design.templates import component_set as cs


# The single explicit 1:1 map from each loop_schema published store-state marker to
# its rendered display string (the hyphenated read-KEY -> the spaced display STRING).
# Keyed on the published markers (not hand-spelled literals) so a marker rename in
# loop_schema surfaces here, and a new published state with no entry KeyErrors rather
# than silently falling through to a wrong render (the 2-decision contract surface).
# ANSWERED_OVER_TIME is a watch-out's answered state; it is not a render-time absence
# marker (an answered watch-out renders its answer), so it carries no display row here.
_STATE_DISPLAY = {
    loop_schema.PENDING: loop_schema.PENDING.replace("-", " "),
    loop_schema.NOT_YET_ANSWERED: loop_schema.NOT_YET_ANSWERED.replace("-", " "),
    loop_schema.NO_DATA: loop_schema.NO_DATA.replace("-", " "),
    loop_schema.NO_PRIOR: loop_schema.NO_PRIOR.replace("-", " "),
}


def _state_marker(marker):
    """Render one store-state as an explicit `state-marker` element (1:1 display string).

    Looks the marker up in the single `_STATE_DISPLAY` table — an unmapped marker
    raises `KeyError` rather than rendering a wrong/blank state (the 2-decision
    contract surface fails loud, never silently).
    """
    return f"<span class='state-marker'>{cs._escape(_STATE_DISPLAY[marker])}</span>"


# A projection is rendered only at or above this many stored timepoints. Below it,
# the view renders trend-only (the matrix sparkline) with no projection — the
# honest-absence guardrail (ADR-0007 accepted documented limitation).
PROJECTION_MIN_TIMEPOINTS = 3

# The fixed honest-absence label every rendered projection carries verbatim.
PROJECTION_LABEL = "naive projection from recent trend — not a clinical forecast"

# The named projection method (the projection extends the recent trend linearly).
PROJECTION_METHOD = "linear extrapolation of the recent trend"


def _projection_values(values):
    """Extend `values` one step along the slope of its last two points (naive trend).

    A naive linear extrapolation: the projected next point continues the most-recent
    segment. The returned sequence is the stored values plus the one projected point.
    """
    slope = values[-1] - values[-2]
    return values + [values[-1] + slope]


def _projection_block(values, dates, state):
    """Render the projection sparkline + its five-element honest-absence label.

    The five elements: (1) the fixed PROJECTION_LABEL, (2) the method, (3) the
    datapoint count, (4) a widening uncertainty band (a distinct `proj-band` element),
    (5) the key dates/milestones on the time axis. The sparkline and band draw from
    the shared `component_set` markup; the band widens from the last stored point
    toward the projected one.
    """
    projected = _projection_values(values)
    spark = cs.sparkline(projected, state)
    # A widening uncertainty band: a faint marker spanning the projected step, drawn
    # once as a distinct element so a missing band is detectable. Inline-only.
    band = (
        f"<span class='proj-band' aria-label='widening uncertainty band'>± widening</span>"
    )
    axis = " ".join(cs._escape(d) for d in dates)
    return (
        "<div class='projection'>"
        f"{spark}{band}"
        f"<div class='caption'>{cs._escape(PROJECTION_LABEL)}</div>"
        f"<div class='caption'>method: {cs._escape(PROJECTION_METHOD)}</div>"
        f"<div class='caption'>{len(values)} datapoints</div>"
        f"<div class='caption'>time axis: {axis}</div>"
        "</div>"
    )


def _biomarker_row(item, marker, values, dates):
    """Render one biomarker row, mapping its store-state 1:1 to its rendered state.

    A no-data (0-timepoint) or no-prior (1-timepoint) biomarker renders its distinct
    state marker only — no matrix sparkline, no fabricated trend/delta/projection over
    too few points. A >=2-timepoint biomarker (marker is None) renders its matrix
    sparkline (every stored timepoint side-by-side, recomputed from the store sequence)
    plus, at >=PROJECTION_MIN_TIMEPOINTS, a naive projection. Draws ALL markup from the
    shared `component_set` def (referenced, never re-declared).
    """
    if marker is not None:
        # no-data / no-prior: render the distinct state marker, never a fabricated trend.
        return _state_row(item, marker)
    state = cs.state_for(item)
    projection = (
        _projection_block(values, dates, state)
        if len(values) >= PROJECTION_MIN_TIMEPOINTS
        else ""
    )
    return (
        "<div class='kpi-row'>"
        f"{cs.kpi(item, values[-1])}"
        f"{cs.sparkline(values, state)}"
        f"{projection}"
        "</div>"
    )


def _state_row(item, marker):
    """Render one panel/watch-out row: the item label + its 1:1 state marker."""
    return (
        "<div class='kpi-row'>"
        f"<div class='kpi'><div class='label'>{cs._escape(item)}</div></div>"
        f"{_state_marker(marker)}"
        "</div>"
    )


def _page_html(rows, page_no):
    """Assemble one view page from rendered rows, page_no in the title.

    The shared component def (`cs.head`) is emitted ONCE per page; the per-row markup
    references it. Everything is inlined (0 external references), routed through `emit`.
    """
    body = (
        "<div class='wrap'>"
        f"<h1>Biomarker Matrix &amp; Projection (page {page_no})</h1>"
        f"{cs.tldr_banner('Biomarker matrix with per-series projection, recomputed at render time.')}"
        f"{cs.legend()}"
        f"{''.join(rows)}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{cs.head('Biomarker Matrix')}<body>{body}</body></html>"


def _watchout_row(root, watchout):
    """Build one watch-out row: unanswered -> the 'not yet answered' marker, else answers."""
    state = loop_schema.read_watchout(watchout, root=root)
    if state == loop_schema.NOT_YET_ANSWERED:
        return _state_row(watchout, loop_schema.NOT_YET_ANSWERED)
    answers = [
        cs._escape(str(r["value"]))
        for r in loop_schema.read_watchout_answers(watchout, root=root)
    ]
    return (
        "<div class='kpi-row'>"
        f"<div class='kpi'><div class='label'>{cs._escape(watchout)}</div></div>"
        f"<div class='value'>{'; '.join(answers)}</div>"
        "</div>"
    )


def _matrix_units(root, biomarkers):
    """Read each biomarker into a render unit, mapped 1:1 to its store state.

    Reads through `loop_schema.read_biomarker` (which sources its timepoints from the
    ADR-0002-T1 `store.read` sequence) — no NDJSON re-parse, no second key. A no-data /
    no-prior biomarker becomes a pre-rendered 0-timepoint marker unit; a >=2-timepoint
    trend biomarker becomes a windowable unit carrying its values/dates so pagination
    can split it across the timepoint axis preserving every stored point.

    Returns:
        (list) Units. A marker unit is `("marker", item, html)`; a trend unit is
        `("trend", item, values, dates)`.
    """
    units = []
    for item in biomarkers:
        result = loop_schema.read_biomarker(item, root=root)
        marker = result["state"]
        if marker is not None:
            units.append(("marker", item, _biomarker_row(item, marker, [], [])))
        else:
            values = [r["value"] for r in result["timepoints"]]
            dates = [r["timepoint"][:10] for r in result["timepoints"]]
            units.append(("trend", item, values, dates))
    return units


def _units(root, panels, watchouts, biomarkers):
    """Build every render unit in panel / watch-out / biomarker order.

    Panels and watch-outs are 0-timepoint marker units; biomarkers are marker-or-trend
    units (see `_matrix_units`).

    Returns:
        (list) Render units (marker or trend) in render order.
    """
    units = [
        ("marker", p, _state_row(p, loop_schema.read_panel(p, root=root)))
        for p in panels
    ]
    units += [("marker", w, _watchout_row(root, w)) for w in watchouts]
    units += _matrix_units(root, biomarkers)
    return units


def _windowed_rows(unit):
    """Expand one unit into (row_html, n_timepoints) sub-rows within the timepoint cap.

    A marker unit yields its single 0-timepoint row. A trend unit with more than
    MAX_TIMEPOINTS_PER_VIEW stored points is split into consecutive timepoint windows,
    each a self-contained matrix row, so every emitted row stays within the timepoint
    bound while the union preserves every stored point (no dropped slice, no phantom
    empty row). The cap is the single per-view bound (reused from `render`).

    Returns:
        (list) (row_html, n_timepoints) pairs for this unit.
    """
    if unit[0] == "marker":
        return [(unit[2], 0)]
    _kind, item, values, dates = unit
    cap = render.MAX_TIMEPOINTS_PER_VIEW
    rows = []
    for start in range(0, len(values), cap):
        v = values[start:start + cap]
        d = dates[start:start + cap]
        rows.append((_biomarker_row(item, None, v, d), len(v)))
    return rows


def _pages(units):
    """Split units into pages within the ADR-0004-T0 cap (series AND timepoints).

    Each unit is first expanded into timepoint-windowed sub-rows (each <= the timepoint
    cap), then the flat row stream is paged at <= MAX_SERIES_PER_VIEW rows per page. The
    cap is the single source of both per-view bounds (reused from `render`, never a
    second size check). The <500000-byte budget follows from the cap (ADR-0004-T0
    re-validated worst-case 16x12 = 34117 bytes), not a runtime byte check.

    Returns:
        (list) Pages, each a list of row_html within both cap bounds (>=1 page).
    """
    flat = [row for unit in units for row, _n in _windowed_rows(unit)]
    pages = [
        flat[start:start + render.MAX_SERIES_PER_VIEW]
        for start in range(0, len(flat), render.MAX_SERIES_PER_VIEW)
    ]
    return pages or [[]]


def render_views(root, *, panels=(), watchouts=(), biomarkers=(), _out_dir=None):
    """Render the biomarker-matrix + projection views from the store, capped per view.

    Recomputes the matrix and projections at render time from the store read model:
    reads each biomarker's stored timepoints (via `loop_schema.read_biomarker`) and
    renders them side-by-side, and maps each ADR-0007-T1 store state (pending /
    not-yet-answered / no-prior / no-data) 1:1 to its rendered state. Splits an over-cap
    view into per-page slices within the ADR-0004-T0 cap and routes every page through
    the published `render.emit(template, store_read) -> Path`, so each is a single
    self-contained inline file under the 500000-byte budget. Reads operator data only
    through the store read model; opens no network and runs no model step.

    Args:
        root (str | Path): The store root the views read operator data from.
        panels (tuple, optional): Recommended-panel ids to render their pending state.
        watchouts (tuple, optional): Watch-out ids to render their answered state.
        biomarkers (tuple, optional): Biomarker ids to render in the matrix/projection.
        _out_dir (Path, optional): Test-only output-dir seam, forwarded to `emit`.

    Returns:
        (list) The Path of each page written (length 1 at/below cap, >=2 over-cap).
    """
    units = _units(root, panels, watchouts, biomarkers)

    paths = []
    for page_no, page_rows in enumerate(_pages(units), start=1):
        def page_template(_store_read, _rows=page_rows, _page_no=page_no):
            return _page_html(_rows, _page_no)

        page_template.__name__ = f"render_view_page_{page_no}"
        paths.append(render.emit(page_template, [], _out_dir=_out_dir))
    return paths
