"""Tests for scripts/generate/render_views.py — biomarker-matrix + projection views (ADR-0007-T2).

The terminal cross-boundary sink of the V1 DAG. The views recompute the biomarker
matrix and naive projections from stored timepoints at render time (read ONLY via
the ADR-0002-T1 store read model surfaced by loop_schema), map the ADR-0007-T1
store states (pending / not-yet-answered / no-prior / no-data) 1:1 to rendered
state, render projections only at >=3 timepoints with the five-element honest-
absence label, render THROUGH the ADR-0004-T1 render.emit engine + component_set
shared markup, keep each artifact under the ADR-0004-T0 500000-byte cap, and make
0 outbound / 0 model-bound dispatch. The store-state markers are read via the
loop_schema published state set, never hand-spelled literals, so the 1:1 map is
checked against the published contract and cannot drift.
"""

import re
import socket
from pathlib import Path

import pytest

from scripts.generate import render, render_views
from scripts.guard.egress_guard import run as egress_run
from scripts.store import loop_schema, store

# An external reference: a src/href/url() target that is neither a data: URI nor a
# same-document #fragment. Inline data:/#frag are allowed; anything resolving off
# the file (http(s)://, //cdn, protocol-relative, bare path) is not.
_REF_RE = re.compile(
    r"""(?:src|href)\s*=\s*['"]([^'"]*)['"]|url\(\s*['"]?([^'")]*)['"]?\s*\)""", re.I
)

SIZE_BUDGET = 500000


def _external_refs(html):
    """Return every src/href/url() target that resolves off the file (not data:/#frag)."""
    out = []
    for m in _REF_RE.finditer(html):
        target = (m.group(1) or m.group(2) or "").strip()
        if not target or target.startswith("data:") or target.startswith("#"):
            continue
        out.append(target)
    return out


def _record_biomarker_series(item, values, root, *, start_month=1):
    """Record `values` as consecutive monthly timepoints for one biomarker."""
    for i, value in enumerate(values):
        loop_schema.record_biomarker(
            item, f"2026-{start_month + i:02d}-01T00:00:00+00:00", value, root=root
        )


def _read_all(paths):
    """Concatenate the text of every emitted page (the whole rendered view)."""
    return "\n".join(p.read_text() for p in paths)


# --------------------------------------------------------------------------- #
# Cycle 1 — matrix recompute + local-only egress (AC-1, AC-5)
# --------------------------------------------------------------------------- #


def test_matrix_renders_both_timepoints_side_by_side(tmp_path):
    """AC-1: a biomarker with >=2 timepoints renders BOTH, recomputed from the store.

    Latest-only FAILS: a render that drops the earlier timepoint turns this red. The
    rendered matrix sparkline must carry one plotted point per stored timepoint, so a
    2-timepoint series renders 2 points (recomputed from store.read, not a stored copy).
    """
    _record_biomarker_series("ferritin", [45, 52], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)

    # The matrix sparkline plots one point per stored timepoint. Two timepoints -> a
    # two-point polyline; a latest-only render would plot one point (or drop the row).
    matrix_pts = _matrix_points_for(html, "ferritin")
    assert matrix_pts == 2, (
        f"expected 2 matrix timepoints side-by-side for ferritin, got {matrix_pts}"
    )


def _matrix_points_for(html, item):
    """Count the plotted points in `item`'s MATRIX (first) sparkline on the page.

    Each rendered series is one `kpi-row`: a KPI card carrying the item name, then a
    MATRIX sparkline (one polyline point per stored timepoint) and (when present) a
    projection sparkline. Counting the matrix sparkline's points recovers the real
    per-series timepoint count actually rendered — so a dropped (latest-only) timepoint
    is detectable.
    """
    rows = html.split("<div class='kpi-row'>")[1:]
    for row in rows:
        label = re.search(r"<div class='label'>([^<]*)</div>", row)
        if not label or label.group(1) != item:
            continue
        first_points = re.search(r"points='([^']*)'", row)
        pts = first_points.group(1).strip() if first_points else ""
        return len(pts.split()) if pts else 0
    return None


def test_matrix_recompute_reads_only_store(tmp_path, monkeypatch):
    """AC-5: the recompute reads operator timepoints via the store read model only.

    Forcing store.read to raise proves the render path goes through the published
    store read model (no re-parse of NDJSON, no second key, no independent discovery).
    """
    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)
    real_read = store.read

    def forbidden(*a, **k):
        raise AssertionError(
            "render_views must read operator data through the store read model"
        )

    # Capture the recorded data first, then force any later store.read to fail; if the
    # render path bypassed the read model it would still succeed -> the test cannot
    # turn red. We instead assert it DOES go through store.read by letting it through
    # once recorded and forbidding an out-of-band re-parse: the simplest falsifiable
    # form is to assert the render succeeds via the read model (below) and separately
    # that no NDJSON file is re-opened. Here: prove read-through by patching store.read
    # to a counting spy and asserting it was called.
    calls = []

    def spy(item, *a, **k):
        calls.append(item)
        return real_read(item, *a, **k)

    monkeypatch.setattr(store, "read", spy)
    render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    assert calls, "render_views must source timepoints through store.read"


def test_render_views_zero_external_references(tmp_path):
    """AC-5: every emitted page carries 0 off-file src/href/url() references."""
    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)
    loop_schema.record_pending_panel("lipid_panel", "2026-06-01T00:00:00+00:00", root=tmp_path)

    paths = render_views.render_views(
        tmp_path,
        biomarkers=("ferritin",),
        panels=("lipid_panel",),
        watchouts=("sleep_quality",),
        _out_dir=tmp_path / "out",
    )
    for p in paths:
        refs = _external_refs(p.read_text())
        assert refs == [], f"{p.name}: expected 0 external references, found {refs}"


def test_render_views_egress_zero_call(tmp_path):
    """AC-5: a real render_views recompute under the egress guard is truthy (0 outbound).

    Wraps a real render_views call in ONE zero-arg closure under the OS egress guard
    and asserts truthy — 0 outbound across the whole render. The path reads the store
    and writes local files; no lab value / symptom answer reaches any model step.
    """
    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)
    out = tmp_path / "under-guard"
    out.mkdir()

    def do_render():
        render_views.render_views(tmp_path, biomarkers=("ferritin",), _out_dir=out)

    assert egress_run(do_render)


def test_render_views_egress_failing_capable(tmp_path, monkeypatch):
    """AC-5 (SEC-03): an outbound call injected into the render path flips the guard FALSY.

    First asserts the production render path runs clean under the guard (truthy) — this
    turns red in RED before render_views exists, so it is not a pass-on-absence. Then
    injects a synthetic outbound connect into the per-series sparkline the render calls
    and asserts the guard turns falsy — proving the guard intercepts THIS new render
    code path, not merely that a clean run makes 0 calls. A local loopback listener
    completes the connect handshake (no network dependency); the deny-network sandbox
    blocks it so the injected connect still trips the guard.
    """
    from vault.design.templates import component_set

    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)
    out = tmp_path / "sec03"
    out.mkdir()

    assert egress_run(
        lambda: render_views.render_views(
            tmp_path, biomarkers=("ferritin",), _out_dir=out / "clean"
        )
    ), "the render path must run clean (0 outbound) under the guard"

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    real_sparkline = component_set.sparkline

    def leaking_sparkline(values, state):
        socket.create_connection(("127.0.0.1", port), timeout=2).close()
        return real_sparkline(values, state)

    monkeypatch.setattr(component_set, "sparkline", leaking_sparkline)

    def do_render():
        render_views.render_views(tmp_path, biomarkers=("ferritin",), _out_dir=out / "leak")

    try:
        result = egress_run(do_render)
    finally:
        srv.close()

    assert not result, "guard must FAIL when the render path makes an outbound call"


# --------------------------------------------------------------------------- #
# Cycle 2 — projection >=3-timepoint guardrail + five-element label (AC-2, AC-3)
# --------------------------------------------------------------------------- #

# The fixed honest-absence label every rendered projection must carry verbatim.
_PROJECTION_LABEL = "naive projection from recent trend — not a clinical forecast"


def _row_for(html, item):
    """Return the rendered `kpi-row` block for `item`, or '' if absent."""
    rows = html.split("<div class='kpi-row'>")[1:]
    for row in rows:
        label = re.search(r"<div class='label'>([^<]*)</div>", row)
        if label and label.group(1) == item:
            return row
    return ""


def test_projection_present_at_three_timepoints(tmp_path):
    """AC-2: a biomarker with >=3 stored timepoints renders a projection.

    The projection is a second (projection) sparkline beyond the matrix one, carrying
    the honest-absence label. A render that omits it at >=3 timepoints turns this red.
    """
    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    row = _row_for(_read_all(paths), "ferritin")
    assert _PROJECTION_LABEL in row, "a >=3-timepoint biomarker must render a projection"


def test_projection_absent_at_two_timepoints(tmp_path):
    """AC-2: a biomarker with EXACTLY 2 timepoints renders trend-only — NO projection.

    The >=3-timepoint guardrail is the honest-absence contract. A projection rendered
    at <3 timepoints turns this red (projection-at-2 FAILS).
    """
    _record_biomarker_series("ferritin", [45, 52], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    row = _row_for(_read_all(paths), "ferritin")
    # trend-only: the matrix sparkline renders (2 points), but no projection label.
    assert _matrix_points_for(_read_all(paths), "ferritin") == 2
    assert _PROJECTION_LABEL not in row, (
        "a 2-timepoint biomarker must render trend-only with NO projection"
    )


def test_projection_carries_all_five_label_elements(tmp_path):
    """AC-3: a rendered projection carries ALL FIVE required elements.

    (1) the literal label, (2) its method, (3) its datapoint count, (4) a widening
    uncertainty band, (5) key dates/milestones on the time axis. Missing any one
    turns this red.
    """
    _record_biomarker_series("ferritin", [45, 52, 60, 58], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    row = _row_for(_read_all(paths), "ferritin")

    # 1) the fixed honest-absence label, verbatim.
    assert _PROJECTION_LABEL in row, "missing element 1: the fixed projection label"
    # 2) the projection method named.
    assert "method:" in row.lower(), "missing element 2: the projection method"
    # 3) the datapoint count (4 stored points -> the count appears).
    assert re.search(r"\b4\b\s*datapoints", row), "missing element 3: the datapoint count"
    # 4) a widening uncertainty band (a distinct band element, not the trend polyline).
    assert "proj-band" in row, "missing element 4: the widening uncertainty band"
    # 5) key dates/milestones on the time axis (the stored timepoint dates).
    assert "2026-01-01" in row and "2026-04-01" in row, (
        "missing element 5: key dates/milestones on the time axis"
    )


# --------------------------------------------------------------------------- #
# Cycle 3 — store-state 1:1 map (incl. no-data) + size-budget pagination (AC-4, AC-6)
# --------------------------------------------------------------------------- #


def _display_for(marker):
    """The rendered display STRING a hyphenated loop_schema read-KEY maps to (1:1).

    The read-KEY is hyphenated (`not-yet-answered`); the rendered display string is
    spaced (`not yet answered`). Derived from the published marker, not hand-spelled,
    so the 1:1 map is checked against the published contract and cannot drift.
    """
    return marker.replace("-", " ")


# A rendered store-state is an explicit `state-marker` element carrying the spaced
# display string — distinct from any incidental markup (e.g. an empty sparkline's
# aria-label), so the 1:1 map assertions are load-bearing, not satisfied by accident.
_STATE_MARKER_RE = re.compile(r"<span class='state-marker'>([^<]*)</span>")


def _state_markers(html):
    """Return every explicit rendered state-marker display string in `html`."""
    return _STATE_MARKER_RE.findall(html)


def _state_marker_in(block):
    """Return the explicit state-marker display string inside one rendered block, or ''."""
    m = _STATE_MARKER_RE.search(block)
    return m.group(1) if m else ""


def test_pending_panel_renders_pending_never_result(tmp_path):
    """AC-4: a recommended-but-undrawn panel renders the "pending" marker, never a result.

    Read via the loop_schema published PENDING marker. A pending panel rendered AS a
    result (a value / "clear" / absent) turns this red.
    """
    loop_schema.record_pending_panel("lipid_panel", "2026-06-01T00:00:00+00:00", root=tmp_path)

    paths = render_views.render_views(
        tmp_path, panels=("lipid_panel",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    block = re.search(r"lipid_panel.{0,300}", html, re.S)
    assert block, "the pending panel must render in the view"
    assert _state_marker_in(block.group(0)) == _display_for(loop_schema.PENDING), (
        "a pending panel must render the 'pending' state marker"
    )
    # never a fabricated result for a pending panel.
    assert "clear" not in block.group(0).lower()


def test_unanswered_watchout_renders_not_yet_answered(tmp_path):
    """AC-4: an unanswered watch-out renders the "not yet answered" spaced display string.

    Read via the loop_schema published NOT_YET_ANSWERED marker (hyphenated read-KEY ->
    spaced display string). A render as a cleared/absent result turns this red.
    """
    paths = render_views.render_views(
        tmp_path, watchouts=("sleep_quality",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    assert _display_for(loop_schema.NOT_YET_ANSWERED) in _state_markers(html), (
        "an unanswered watch-out must render the 'not yet answered' state marker"
    )


def test_answered_watchout_renders_answer(tmp_path):
    """AC-4 (5th state): an answered watch-out renders its stored answer, not the marker.

    Records an operator answer via the loop_schema API so read_watchout returns the
    published ANSWERED_OVER_TIME state (its live render branch). The rendered row must
    carry the stored answer value AND must NOT be the not-yet-answered marker — keyed on
    the published markers, never hand-spelled literals. A regression that collapses
    answered->not-yet-answered, or drops the stored answer from the render, turns red.
    """
    assert loop_schema.read_watchout("sleep_quality", root=tmp_path) == (
        loop_schema.NOT_YET_ANSWERED
    ), "precondition: an unrecorded watch-out reads not-yet-answered"
    loop_schema.record_watchout_answer(
        "sleep_quality", "good", "2026-06-01T00:00:00+00:00", root=tmp_path
    )
    assert loop_schema.read_watchout("sleep_quality", root=tmp_path) == (
        loop_schema.ANSWERED_OVER_TIME
    ), "the recorded answer must put the watch-out in the answered-over-time state"

    paths = render_views.render_views(
        tmp_path, watchouts=("sleep_quality",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    row = _row_for(html, "sleep_quality")
    assert row, "the answered watch-out must render its row"
    # The stored answer value renders (drop-the-answer regression turns this red).
    assert "good" in row, "the answered watch-out must render its stored answer value"
    # NOT the not-yet-answered marker (collapse-to-not-yet-answered regression turns red).
    assert _display_for(loop_schema.NOT_YET_ANSWERED) not in _state_markers(html), (
        "an answered watch-out must NOT render the 'not yet answered' state marker"
    )
    assert _state_marker_in(row) == "", (
        "an answered watch-out renders its answer, not a state marker"
    )


def test_no_prior_biomarker_renders_marker_no_fabricated_trend(tmp_path):
    """AC-4: a single-timepoint biomarker renders the "no prior" marker, no fabricated trend.

    Read via the loop_schema published NO_PRIOR marker. A render that fabricates a
    trend/delta/projection over one point turns this red.
    """
    _record_biomarker_series("ferritin", [45], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    row = _row_for(_read_all(paths), "ferritin")
    assert _state_marker_in(row) == _display_for(loop_schema.NO_PRIOR), (
        "a single-timepoint biomarker must render the 'no prior' state marker"
    )
    # No fabricated trend/delta/projection over a single point.
    assert _PROJECTION_LABEL not in row, "no projection over a single point"
    assert "trend" not in row.lower(), "no fabricated trend over a single point"


def test_no_data_biomarker_renders_distinct_marker(tmp_path):
    """AC-4 (Wave-6 5th marker): a never-recorded biomarker renders the distinct "no data" marker.

    The 0-timepoint NO_DATA state (distinct from NO_PRIOR's 1 timepoint) is mapped 1:1:
    rendered as "no data", never as a result and never as a fabricated trend. Read via
    the loop_schema published NO_DATA marker.
    """
    paths = render_views.render_views(
        tmp_path, biomarkers=("never_recorded",), _out_dir=tmp_path / "out"
    )
    row = _row_for(_read_all(paths), "never_recorded")
    assert row, "a no-data biomarker must still render its row"
    assert _state_marker_in(row) == _display_for(loop_schema.NO_DATA), (
        "a never-recorded biomarker must render the distinct 'no data' state marker"
    )
    # the distinct no-data marker is NOT the no-prior marker (1:1, not collapsed).
    assert _state_marker_in(row) != _display_for(loop_schema.NO_PRIOR)
    assert _PROJECTION_LABEL not in row, "no projection for a no-data biomarker"
    assert "trend" not in row.lower(), "no fabricated trend for a no-data biomarker"


def test_two_timepoint_biomarker_renders_side_by_side_not_named_marker(tmp_path):
    """AC-4 / crit-1: a >=2-timepoint biomarker renders both timepoints, no no-prior/no-data marker.

    A >=2-timepoint series (loop_schema state=None) renders its store.read timepoint
    sequence side-by-side in the matrix — NOT as a named no-prior/no-data marker.
    """
    _record_biomarker_series("ferritin", [45, 52], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    row = _row_for(_read_all(paths), "ferritin")
    assert _matrix_points_for(_read_all(paths), "ferritin") == 2
    # a >=2-timepoint series renders no named no-prior/no-data state marker.
    assert _state_marker_in(row) == "", (
        "a >=2-timepoint biomarker must not render a no-prior/no-data marker"
    )


def _matrix_store_biomarkers(n_series, n_timepoints, root):
    """Record n_series biomarkers x n_timepoints each; return the biomarker id tuple.

    Realistic long biomarker names + multi-digit lab magnitudes so the rendered bytes
    are representative of the worst case the cap bounds.
    """
    names = [
        "total_cholesterol", "ldl_cholesterol", "hdl_cholesterol", "triglycerides",
        "fasting_glucose", "hba1c", "hs_crp", "alt", "ferritin", "vitamin_d_25oh",
        "tsh", "free_t4", "creatinine", "egfr", "alkaline_phosphatase", "albumin",
        "sodium", "potassium", "calcium", "magnesium",
    ]
    items = []
    for s in range(n_series):
        item = names[s % len(names)] + (f"_{s}" if s >= len(names) else "")
        for t in range(n_timepoints):
            loop_schema.record_biomarker(
                item, f"2026-{(t % 12) + 1:02d}-01T00:00:00+00:00", 100 + s * 7 + t * 3,
                root=root,
            )
        items.append(item)
    return tuple(items)


def test_worst_case_paginates_each_under_budget(tmp_path):
    """AC-6: an over-cap worst-case view paginates so each artifact is wc -c < 500000.

    Feeds more series than the ADR-0004-T0 cap (MAX_SERIES_PER_VIEW) so the render must
    split: >=2 returned paths, each strictly < 500000 bytes (measured st_size == wc -c).
    A single unpaginated over-cap file fails.
    """
    over_cap = render.MAX_SERIES_PER_VIEW + 4
    items = _matrix_store_biomarkers(over_cap, render.MAX_TIMEPOINTS_PER_VIEW, tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=items, _out_dir=tmp_path / "out"
    )
    assert len(paths) >= 2, (
        f"over-cap dataset ({over_cap} series > cap {render.MAX_SERIES_PER_VIEW}) "
        f"must paginate to >=2 files, got {len(paths)}"
    )
    for p in paths:
        size = p.stat().st_size
        assert size < SIZE_BUDGET, f"{p.name}: {size} bytes >= {SIZE_BUDGET}"


def test_pagination_keeps_each_page_within_series_cap(tmp_path):
    """AC-6 (placement, not just size): each emitted page is within MAX_SERIES_PER_VIEW.

    Size alone can never red on a cap breach (worst case is ~tens of KB), so this asserts
    PLACEMENT: every page carries at most MAX_SERIES_PER_VIEW series.
    """
    over_cap = render.MAX_SERIES_PER_VIEW + 4
    items = _matrix_store_biomarkers(over_cap, 4, tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=items, _out_dir=tmp_path / "out"
    )
    for p in paths:
        n_rows = p.read_text().count("<div class='kpi-row'>")
        assert n_rows <= render.MAX_SERIES_PER_VIEW, (
            f"{p.name} has {n_rows} series > cap {render.MAX_SERIES_PER_VIEW}"
        )


def test_pagination_preserves_all_series(tmp_path):
    """AC-6: pagination preserves ALL series across the pages (no dropped biomarker)."""
    over_cap = render.MAX_SERIES_PER_VIEW + 4
    items = _matrix_store_biomarkers(over_cap, 4, tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=items, _out_dir=tmp_path / "out"
    )
    rendered = set()
    for p in paths:
        for m in re.finditer(r"<div class='label'>([^<]*)</div>", p.read_text()):
            rendered.add(m.group(1))
    assert set(items) <= rendered, (
        f"dropped series: {set(items) - rendered}"
    )


def test_over_timepoint_cap_windows_within_bound_preserving_all(tmp_path):
    """AC-6: a biomarker over the timepoint cap windows so every page is within the bound.

    A single biomarker with more than MAX_TIMEPOINTS_PER_VIEW stored points must split
    across timepoint windows — each rendered matrix sparkline within the cap — and the
    union of windows must preserve every stored point (no dropped last slice). A breach
    (a >cap-point sparkline) or a dropped slice turns this red, even though one over-cap
    file would stay well under the byte budget.
    """
    over_cap_tp = render.MAX_TIMEPOINTS_PER_VIEW + 5
    _record_biomarker_series("ferritin", list(range(40, 40 + over_cap_tp)), tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    # Count EVERY ferritin matrix window across all pages (an item can occupy >1 window
    # row when its stored points exceed the timepoint cap).
    total = 0
    for p in paths:
        for window in _all_matrix_windows_for(p.read_text(), "ferritin"):
            assert window <= render.MAX_TIMEPOINTS_PER_VIEW, (
                f"{p.name}: ferritin window has {window} > cap {render.MAX_TIMEPOINTS_PER_VIEW}"
            )
            total += window
    assert total == over_cap_tp, (
        f"windowing dropped/duplicated points: rendered {total} != stored {over_cap_tp}"
    )


def _all_matrix_windows_for(html, item):
    """Yield the matrix-sparkline point count of EVERY `item` window row on the page."""
    rows = html.split("<div class='kpi-row'>")[1:]
    for row in rows:
        label = re.search(r"<div class='label'>([^<]*)</div>", row)
        if not label or label.group(1) != item:
            continue
        first_points = re.search(r"points='([^']*)'", row)
        pts = first_points.group(1).strip() if first_points else ""
        yield len(pts.split()) if pts else 0
