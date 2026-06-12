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

# A tight, MEASURED per-page byte ceiling. The worst case — a full-cap page of
# MAX_SERIES_PER_VIEW series x MAX_TIMEPOINTS_PER_VIEW timepoints, every series
# carrying a projection — measured ~24232 bytes (S49, after the visual-spec chrome
# grew the shared style block). The 29000 ceiling adds a ~20% margin: it RIDES the
# real worst-case bytes so a materially-inflated page (a double-render, a per-window
# projection regression, a cap breach that lands more rows on a page) turns it red,
# unlike the 25x-headroom SIZE_BUDGET ceiling which cannot.
MEASURED_PAGE_CEILING = 29000


def _external_refs(html):
    """Return every src/href/url() target that resolves off the file (not data:/#frag)."""
    out = []
    for m in _REF_RE.finditer(html):
        target = (m.group(1) or m.group(2) or "").strip()
        if not target or target.startswith("data:") or target.startswith("#"):
            continue
        out.append(target)
    return out


def _all_asset_refs(html):
    """Return every src/href/url() target in the page, INCLUDING inline data: URIs.

    Unlike `_external_refs`, this keeps data: targets so the offline-open walk has
    a real asset to resolve. Same-document `#fragment` hrefs (no asset) are dropped.
    """
    out = []
    for m in _REF_RE.finditer(html):
        target = (m.group(1) or m.group(2) or "").strip()
        if not target or target.startswith("#"):
            continue
        out.append(target)
    return out


# The shared chart-component style def (the component_set <style>/:root block) is
# the single shared-defs source every rendered row draws from. It must appear
# EXACTLY ONCE per emitted page, referenced per series (not re-emitted per row).
# `:root {` is its falsifiable occurrence marker.
_SHARED_DEFS_MARKER = ":root {"


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
    """AC-5: the recompute sources operator timepoints through the store read model.

    Patches store.read to a counting spy (delegating to the real read) and asserts the
    render path invoked it — proving timepoints come through the published read model,
    not an out-of-band NDJSON re-parse or a second key.
    """
    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)
    real_read = store.read
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


def test_render_views_shared_defs_appears_once_per_page(tmp_path):
    """AC-5 (migrated from the retired ADR-0004-T2 suite): shared defs emit ONCE per page.

    The component_set shared-defs block (:root { ... }) is emitted once per page and
    REFERENCED per series (one chart svg per rendered series), proving the markup is
    shared from component_set.py, not re-emitted per row. A per-row re-emit of the
    shared def pushes the count above 1 and turns this red.
    """
    n_series = 8
    items = _matrix_store_biomarkers(n_series, 4, tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=items, _out_dir=tmp_path / "out"
    )
    for p in paths:
        html = p.read_text()
        shared_defs_count = html.count(_SHARED_DEFS_MARKER)
        assert shared_defs_count == 1, (
            f"{p.name}: shared chart-component def must appear exactly once, "
            f"found {shared_defs_count}"
        )
    # the def is REFERENCED per series (one chart svg per rendered series), not
    # re-declared per series: across the view, every series carries its own chart.
    whole = _read_all(paths)
    series_refs = whole.count("<svg ")
    assert series_refs >= n_series, (
        f"each series must reference the shared def via its own chart, "
        f"got {series_refs} charts for {n_series} series"
    )


def test_render_views_offline_open_zero_outbound(tmp_path):
    """AC-5 (migrated from the retired ADR-0004-T2 suite): asset-open walk sees 0 outbound.

    Parses every emitted page for EVERY asset reference and actually attempts to OPEN
    each target under the egress guard — an off-file reference would attempt a socket
    connect the guard surfaces as falsy. The all-inline render keeps the walk at 0
    outbound. Distinct from the static `_external_refs(html) == []` check: an injected
    external `src=` asset turns this red.
    """
    import urllib.request

    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)
    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )

    def open_and_walk_assets():
        for p in paths:
            for target in _all_asset_refs(p.read_text()):
                # A data: URI resolves in-process; an off-host URL would attempt a
                # socket connect here, which the OS egress guard would surface.
                with urllib.request.urlopen(target) as resp:
                    resp.read()

    assert egress_run(open_and_walk_assets)


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


def test_resulted_panel_renders_result_value(tmp_path):
    """AC-4 (bead byj): a landed panel result renders as a value row, never a crash.

    Pre-fix, a landed result flowed from read_panel straight into _STATE_DISPLAY
    (which maps only the 4 absence markers) and the KeyError killed the WHOLE page
    render. The contract: pending renders the pending marker; a landed result renders
    the escaped result value (the answered-watchout value-row shape) with no pending
    marker in the row. Deleting the result branch re-raises KeyError and reds this.
    """
    loop_schema.record_pending_panel(
        "lipid_panel", "2026-06-01T00:00:00+00:00", root=tmp_path
    )
    loop_schema.record_panel_result(
        "lipid_panel", "results received", "2026-06-08T00:00:00+00:00", root=tmp_path
    )

    paths = render_views.render_views(
        tmp_path, panels=("lipid_panel",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    row = _row_for(html, "lipid_panel")
    assert row, "the resulted panel must render its row (not crash the page render)"
    assert "results received" in row, "the landed result value must render in the row"
    # The resulted row renders a VALUE, not a state marker — and the 'pending'
    # display string is absent from the whole rendered view.
    assert _state_marker_in(row) == "", (
        "a resulted panel renders its result value, not a state marker"
    )
    assert _display_for(loop_schema.PENDING) not in _state_markers(html), (
        "a resulted panel must not still render the 'pending' marker"
    )


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
    """AC-6: an over-cap worst-case view paginates, each page within the MEASURED ceiling.

    Feeds more series than the ADR-0004-T0 cap (MAX_SERIES_PER_VIEW) so the render must
    split: >=2 returned paths. Each page must be under the tight MEASURED per-page ceiling
    (the failing-capable bound — reds on material byte inflation), with the 25x-headroom
    SIZE_BUDGET kept only as a secondary sanity ceiling. A single unpaginated over-cap
    file fails the page count.
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
        # the failing-capable bound: a full-cap page rides ~24232 bytes (S49 — the
        # MEASURED_PAGE_CEILING comment above records the measurement); this reds if
        # a page inflates materially past the measured worst case.
        assert size < MEASURED_PAGE_CEILING, (
            f"{p.name}: {size} bytes >= measured ceiling {MEASURED_PAGE_CEILING}"
        )
        assert size < SIZE_BUDGET, f"{p.name}: {size} bytes >= sanity ceiling {SIZE_BUDGET}"


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


# --------------------------------------------------------------------------- #
# Cycle 4 — single-projection windowing + projection value + escaping (F2-F10)
# --------------------------------------------------------------------------- #


def _projection_blocks(html, item):
    """Return every `<div class='projection'>...</div>` block in `item`'s row(s)."""
    blocks = []
    for window in re.findall(
        r"<div class='kpi-row'>.*?(?=<div class='kpi-row'>|</div></div></body>|$)",
        html,
        re.S,
    ):
        label = re.search(r"<div class='label'>([^<]*)</div>", window)
        if not label or label.group(1) != item:
            continue
        blocks.extend(re.findall(r"<div class='projection'>.*?</div></div>", window, re.S))
    return blocks


def test_over_cap_renders_exactly_one_projection_from_true_last_two(tmp_path):
    """F2: a >12-timepoint biomarker renders ONE projection, from the SERIES' last two points.

    The over-cap windowing must NOT re-run the projection guard per window (that emits
    one projection per >=3-point window, the leading one a MID-SERIES segment mislabeled
    as a forward forecast). Exactly one projection is emitted, on the FINAL window, and
    its projected point reflects the true last-two-stored-points slope. Current code
    emits two projections -> red.
    """
    # 15 points, last two = [70, 78] (slope +8 -> projected 86); a mid-series segment
    # (e.g. points 11..12) has a different slope, so a mid-series projection differs.
    values = [10, 18, 24, 31, 37, 44, 50, 57, 63, 50, 40, 55, 62, 70, 78]
    _record_biomarker_series("ferritin", values, tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    blocks = _projection_blocks(html, "ferritin")
    assert len(blocks) == 1, f"expected exactly ONE projection, got {len(blocks)}"

    # The single projection extrapolates the TRUE last two stored points (78 + (78-70))
    # = 86, NOT a mid-series segment. The final window is [62, 70, 78]; the projection
    # plot is [62, 70, 78, 86]. Recover the projected value off the two known points
    # (70 -> ys[1], 78 -> ys[2]) and assert ~86 (the true +8 forward slope).
    ys = [float(p.split(",")[1]) for p in re.search(r"points='([^']*)'", blocks[0]).group(1).split()]
    assert len(ys) == 4, "the final-window projection plots its 3 points plus ONE projected"
    px_per_unit = (ys[2] - ys[1]) / (78 - 70)
    projected = 78 + (ys[3] - ys[2]) / px_per_unit
    assert abs(projected - 86) < 0.5, (
        f"projection must use the SERIES' true last two points (slope +8 -> 86); "
        f"recovered {projected:.2f} (a mid-series segment slope -> a different value)"
    )


def test_thirteen_timepoints_no_degenerate_row_all_points_preserved(tmp_path):
    """F3: a 13-timepoint biomarker emits no 1-point window; all 13 points are preserved.

    13 = cap(12) + 1, so a naive split yields a final 1-point window — a degenerate
    contextless matrix row (a 1-point sparkline draws nothing). The final sub-2-point
    window must fold into the previous (carry the boundary point) so every window has
    >=2 plotted points, while the union still represents all 13 stored points. Current
    code emits a 1-point window -> red.
    """
    values = list(range(40, 53))  # 13 points
    assert len(values) == render.MAX_TIMEPOINTS_PER_VIEW + 1
    _record_biomarker_series("ferritin", values, tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    windows = list(_all_matrix_windows_for(html, "ferritin"))
    assert windows, "the over-cap biomarker must render at least one matrix window"
    assert all(w >= 2 for w in windows), (
        f"no window may be a degenerate <2-point row, got window sizes {windows}"
    )
    assert all(w <= render.MAX_TIMEPOINTS_PER_VIEW for w in windows), (
        f"every window must stay within the cap, got {windows}"
    )
    assert sum(windows) == len(values), (
        f"all {len(values)} points must be preserved exactly once, got total {sum(windows)}"
    )


def test_projection_value_is_naive_extrapolation(tmp_path):
    """F5: the projection's plotted point IS the naive extrapolation (last + (last-prev)).

    A known-slope series [45, 52, 60] (slope +8) projects to 68. The projection
    sparkline plots [45, 52, 60, 68]; recovering the projected point's VALUE from the
    SVG y-axis (calibrated off two known plotted points) must yield 68 — a flat (60),
    reversed, or fabricated projection reds.
    """
    _record_biomarker_series("ferritin", [45, 52, 60], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin",), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    block = _projection_blocks(html, "ferritin")[0]
    pts = re.search(r"points='([^']*)'", block).group(1).split()
    ys = [float(p.split(",")[1]) for p in pts]
    assert len(ys) == 4, "the projection plots the stored points plus ONE projected"
    # Calibrate the y-axis off the two known plotted stored points (52 -> ys[1],
    # 60 -> ys[2]) — slope is pixels-per-unit — then invert ys[3] to its value. This is
    # independent of the plot's own lo/hi, so a flat projection (60 again) reads back 60.
    px_per_unit = (ys[2] - ys[1]) / (60 - 52)
    projected = 60 + (ys[3] - ys[2]) / px_per_unit
    assert abs(projected - 68) < 0.5, (
        f"projected point must encode 68 (naive +8 extrapolation); recovered {projected:.2f} "
        f"(flat -> 60, reversed/fabricated -> elsewhere)"
    )


def test_matrix_multi_series_independent_per_series_recompute(tmp_path):
    """F6: two biomarkers with DIFFERENT timepoint counts each recompute independently.

    ferritin=[45,52] (2tp, trend-only) and hba1c=[5.1,5.4,5.6,5.5] (4tp, projects).
    Each renders its OWN point count (2 and 4) with no length-alignment, and only
    hba1c (>=3tp) carries a projection — proving per-series recompute with no
    cross-contamination.
    """
    _record_biomarker_series("ferritin", [45, 52], tmp_path)
    _record_biomarker_series("hba1c", [5.1, 5.4, 5.6, 5.5], tmp_path)

    paths = render_views.render_views(
        tmp_path, biomarkers=("ferritin", "hba1c"), _out_dir=tmp_path / "out"
    )
    html = _read_all(paths)
    assert _matrix_points_for(html, "ferritin") == 2
    assert _matrix_points_for(html, "hba1c") == 4
    assert not _projection_blocks(html, "ferritin"), (
        "the 2-timepoint series must NOT carry a projection"
    )
    assert len(_projection_blocks(html, "hba1c")) == 1, (
        "the 4-timepoint series must carry exactly one projection"
    )


def test_answered_watchout_renders_all_answers_over_time(tmp_path):
    """F7: an answered-over-time watch-out renders BOTH stored answers, not latest-only.

    Two answers recorded at successive timepoints ("good" then "poor") must both appear
    in the rendered row, so a latest-only regression that drops the earlier answer reds.
    """
    loop_schema.record_watchout_answer(
        "sleep_quality", "good", "2026-06-01T00:00:00+00:00", root=tmp_path
    )
    loop_schema.record_watchout_answer(
        "sleep_quality", "poor", "2026-07-01T00:00:00+00:00", root=tmp_path
    )

    paths = render_views.render_views(
        tmp_path, watchouts=("sleep_quality",), _out_dir=tmp_path / "out"
    )
    row = _row_for(_read_all(paths), "sleep_quality")
    assert "good" in row and "poor" in row, (
        "both answers over time must render; a latest-only render drops the earlier one"
    )


def test_empty_input_renders_one_valid_page_zero_refs(tmp_path):
    """F9: render_views with no panels/watchouts/biomarkers emits exactly 1 valid page.

    The page must be a valid document (doctype present) carrying 0 external references.
    """
    paths = render_views.render_views(tmp_path, _out_dir=tmp_path / "out")
    assert len(paths) == 1, f"empty input must emit exactly 1 page, got {len(paths)}"
    html = paths[0].read_text()
    assert html.lstrip().lower().startswith("<!doctype html>"), "page must carry the doctype"
    assert _external_refs(html) == [], "the empty page must carry 0 external references"


def test_operator_text_is_escaped_no_injection(tmp_path):
    """F10: operator data carrying HTML/script/url() is escaped, not injected, and emits.

    render_views renders raw operator data (a terminal PII sink); escaping is delegated
    to component_set. A watch-out answer containing <script>, a quote, and a url(...)
    substring must (a) still emit (the emit external-asset scan is not tripped by the
    ESCAPED text) and (b) appear escaped — no live <script> tag, the raw < and > are
    entity-encoded. Pins the delegated-escaping contract in render_views' own suite.
    """
    payload = "good<script>alert('x')</script> url(http://lab.example/x) \"q\""
    loop_schema.record_watchout_answer(
        "sleep_quality", payload, "2026-06-01T00:00:00+00:00", root=tmp_path
    )

    # (a) emits (render.emit's external-asset scan parses by syntactic position and is
    # NOT tripped by the escaped operator url() carried as text content — a raise here
    # would surface as render_views propagating ValueError instead of returning a path).
    paths = render_views.render_views(
        tmp_path, watchouts=("sleep_quality",), _out_dir=tmp_path / "out"
    )
    assert len(paths) == 1 and paths[0].exists(), (
        "the page must emit; the escaped operator url() must not trip the egress scan"
    )
    html = paths[0].read_text()
    # (b) no live tag injected; the raw markup is entity-encoded.
    assert "<script>" not in html, "raw <script> must not be injected into the output"
    assert "&lt;script&gt;" in html, "the operator <script> text must render escaped"
    # (c) the operator double quotes render entity-encoded (bead vp5p: _escape
    # covers the full & < > ' " set; a dropped &quot; replace turns this red).
    assert "&quot;q&quot;" in html, "operator double quotes must render entity-encoded"
