"""Mixed-stream dashboard test through the production path (ADR-0008 D5).

Seeds all four loop_schema stream types (biomarker, pending panel, watch-out
answer, physician feedback) plus a legacy unprefixed numeric item via the
PRODUCTION writers, then runs `generate.run("dashboard")` end-to-end and asserts
the type-routed render: no crash on string-valued streams, no raw `biomarker::`
key in the HTML, clean labels, the panel state verbatim, the watch-out answer,
and a sparkline. RED-proves the `i1t` crash on the pre-ADR-0008 dashboard.
"""

import pytest

from scripts.generate import generate
from scripts.store import loop_schema, store


def _seed_mixed_store(root):
    """Seed a tmp store with all four stream types via the production writers."""
    loop_schema.record_biomarker("ferritin", "2026-05-01T00:00:00+00:00", 95, root)
    loop_schema.record_biomarker("ferritin", "2026-05-15T00:00:00+00:00", 110, root)
    loop_schema.record_pending_panel("iron-panel", "2026-05-01T00:00:00+00:00", root)
    loop_schema.record_watchout_answer(
        "injection_site_reaction", "none noticed", "2026-05-02T00:00:00+00:00", root
    )
    loop_schema.record_physician_feedback(
        "discussed at visit", "2026-05-03T00:00:00+00:00", root
    )
    # The legacy direct-append form: an unprefixed numeric series.
    for timepoint, value in (
        ("2026-05-01T00:00:00+00:00", 52),
        ("2026-05-02T00:00:00+00:00", 49),
    ):
        store.append(
            "rhr",
            {"item": "rhr", "timepoint": timepoint, "source": "whoop", "value": value},
            root=root,
        )


def test_mixed_stream_store_renders_through_production_path(tmp_path):
    """generate.run('dashboard') over a mixed-stream store renders type-routed HTML."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_mixed_store(root)

    path = generate.run("dashboard", _root=root, _out_dir=out)

    assert path.exists()
    html = path.read_text()
    assert "biomarker::" not in html, "raw store keys must never render as labels"
    assert "Ferritin" in html
    assert "pending" in html
    assert "none noticed" in html
    assert "<svg" in html


def test_unknown_stream_prefix_fails_loud(tmp_path):
    """F6: a `::` item outside the four routed prefixes raises KeyError naming it.

    Routing for a new stream type is added deliberately, never by silent
    fallthrough (ADR-0008 D3).
    """
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_mixed_store(root)
    store.append(
        "custom::thing",
        {"item": "custom::thing", "timepoint": "2026-05-01T00:00:00+00:00",
         "source": "x", "value": 1},
        root=root,
    )

    with pytest.raises(KeyError) as exc:
        generate.run("dashboard", _root=root, _out_dir=out)
    assert "custom::" in str(exc.value)


def test_biomarker_non_numeric_latest_renders_verbatim_no_units(tmp_path):
    """F19: the KPI headline is the stream's TRUE latest reading.

    A non-numeric latest renders verbatim with no units; state and sparkline
    still come from the numeric series.
    """
    root = tmp_path / "store"
    out = tmp_path / "out"
    loop_schema.record_biomarker("ferritin", "2026-05-01T00:00:00+00:00", 95, root)
    loop_schema.record_biomarker("ferritin", "2026-05-15T00:00:00+00:00", 110, root)
    loop_schema.record_biomarker(
        "ferritin", "2026-06-01T00:00:00+00:00", "redraw scheduled", root
    )

    html = generate.run("dashboard", _root=root, _out_dir=out).read_text()
    assert "redraw scheduled" in html
    assert "redraw scheduled ng/mL" not in html, "non-numeric headline carries no units"
    assert "<rect" in html, "the numeric series still renders its bar sparkline"
