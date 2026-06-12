"""Corrected-value round-trip pins over the rendered consumer surfaces (bead 1vi).

A `store.correct` superseding append must surface as the corrected value in
EVERY rendered consumer of the store read model — the physician report and the
dashboard (both fed by `store.read_all` through `generate.run`) and the
biomarker-matrix views (fed by `loop_schema.read_biomarker`). Each pin asserts
both directions: the corrected value IS rendered and the superseded original is
NOT (placement, not mere existence — a page carrying both would silently encode
the pre-1vi first-write-wins read).

The values are deliberately distinctive 4-digit integers so a substring match
cannot collide with dates, page numbers, or sparkline geometry.
"""

from scripts.generate import generate, render_views
from scripts.store import loop_schema, store

T1 = "2026-05-01T00:00:00+00:00"
T2 = "2026-05-02T00:00:00+00:00"


def _corrected(item, timepoint, value):
    """Build the superseding reading for a loop_schema-recorded biomarker."""
    # "manual" is loop_schema's biomarker source tag — the stored identity the
    # correction must hit exactly.
    return {"item": item, "timepoint": timepoint, "source": "manual", "value": value}


def _seed_corrected_store(root):
    """Seed one biomarker timepoint (4441) and supersede it with 5552."""
    loop_schema.record_biomarker("rhr", T1, 4441, root)
    store.correct("biomarker::rhr", _corrected("biomarker::rhr", T1, 5552), root=root)


def test_report_renders_corrected_value_not_original(tmp_path):
    """The physician report path renders the superseding value only."""
    root = tmp_path / "store"
    _seed_corrected_store(root)

    html = generate.run("report", _root=root, _out_dir=tmp_path / "out").read_text()
    assert "5552" in html
    assert "4441" not in html


def test_dashboard_renders_corrected_value_not_original(tmp_path):
    """The dashboard data layer renders the superseding value only."""
    root = tmp_path / "store"
    _seed_corrected_store(root)

    html = generate.run("dashboard", _root=root, _out_dir=tmp_path / "out").read_text()
    assert "5552" in html
    assert "4441" not in html


def test_render_views_render_corrected_value_not_original(tmp_path):
    """The biomarker-matrix view renders the corrected latest value only.

    Two timepoints (so the series renders as a trend row with a real latest
    value, not an absence marker); the LATEST timepoint's value is corrected.
    """
    root = tmp_path / "store"
    loop_schema.record_biomarker("rhr", T1, 4441, root)
    loop_schema.record_biomarker("rhr", T2, 9990, root)
    store.correct("biomarker::rhr", _corrected("biomarker::rhr", T2, 5552), root=root)

    paths = render_views.render_views(root, biomarkers=("rhr",), _out_dir=tmp_path / "out")
    html = "".join(p.read_text() for p in paths)
    assert "5552" in html
    assert "9990" not in html
