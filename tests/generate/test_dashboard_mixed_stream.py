"""Mixed-stream dashboard test through the production path (ADR-0008 D5).

Seeds all four loop_schema stream types (biomarker, pending panel, watch-out
answer, physician feedback), the ADR-0010 plan + tracking streams, plus a
legacy unprefixed numeric item via the PRODUCTION writers, then runs
`generate.run("dashboard")` end-to-end and asserts the type-routed render: no
crash on string- or dict-valued streams, no raw `biomarker::`/`plan::` key in
the HTML, clean labels, the panel state verbatim, the watch-out answer, and a
sparkline. RED-proves the `i1t` crash on the pre-ADR-0008 dashboard.

Placement assertions target the ADR-0009/0010 zone model: biomarker rows land
in the Performance & Trends zone (4), panel/watch-out/feedback/catch-all rows
in the Labs & Bloodwork zone (7), plan/tracking content in the Today's Plan
zone (3) — and NOT vice versa.
"""

import datetime
import html as html_lib
import re

import pytest

from scripts.generate import generate
from scripts.store import loop_schema, plan_schema, store

# The fixed seam date the plan resolution compares against (passed through
# `generate.run`'s `_today` seam): Wednesday 2026-06-10.
_TODAY = datetime.date(2026, 6, 10)


def _seed_mixed_store(root):
    """Seed a tmp store with every routed stream type via the production writers.

    The plan + tracking entries are dated the file's fixed seam date; the
    populated-plan assertions pass it through `generate.run`'s `_today` seam,
    so the seeded plans resolve populated regardless of the real date.
    """
    loop_schema.record_biomarker("ferritin", "2026-05-01T00:00:00+00:00", 95, root)
    loop_schema.record_biomarker("ferritin", "2026-05-15T00:00:00+00:00", 110, root)
    loop_schema.record_pending_panel("iron-panel", "2026-05-01T00:00:00+00:00", root)
    loop_schema.record_watchout_answer(
        "injection_site_reaction", "none noticed", "2026-05-02T00:00:00+00:00", root
    )
    loop_schema.record_physician_feedback(
        "discussed at visit", "2026-05-03T00:00:00+00:00", root
    )
    today = _TODAY.isoformat()
    plan_schema.record_plan(
        "workout",
        {"exercises": [{"name": "Bench Press", "sets": 3, "load": "185 lb"}]},
        today, "strength-coach", root,
    )
    plan_schema.record_plan_tracking(
        "workout", {"elapsed_min": 42, "sets_done": {"Bench Press": 2}}, today, root
    )
    plan_schema.record_plan(
        "peptides", {"compound": "bpc-157", "dose": "250 mcg", "route": "subq"},
        today, "peptide-doc", root,
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


def _rows(html, zone_title):
    """Split one zone's section into its kpi-row fragments.

    Splitting inside the zone's own section markup means a row fragment
    terminates at its zone boundary — never running past it to EOF.
    """
    return _zones(html)[zone_title].split("<div class='kpi-row'>")[1:]


def _zones(html):
    """Map each rendered zone's decoded h2 title to its full section markup."""
    out = {}
    for section in re.findall(r"<section class='zone'[^>]*>.*?</section>", html, re.S):
        title = re.search(r"<h2[^>]*>([^<]*)</h2>", section).group(1)
        out[html_lib.unescape(title)] = section
    return out


def test_mixed_stream_store_renders_through_production_path(tmp_path):
    """generate.run('dashboard') over a mixed-stream store renders type-routed HTML."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_mixed_store(root)

    path = generate.run("dashboard", _root=root, _out_dir=out, _today=_TODAY)

    assert path.exists()
    html = path.read_text()
    assert "biomarker::" not in html, "raw store keys must never render as labels"
    assert "panel::" not in html
    assert "watch-out::" not in html
    assert "feedback::" not in html
    assert "plan::" not in html
    assert "plan-track::" not in html

    # PLACEMENT (ADR-0009 D5 + ADR-0010 D5): biomarker rows land in zone 4,
    # panel/watch-out/feedback rows in zone 7, plan content in zone 3 — and
    # not in each other's zone.
    zones = _zones(html)
    trends = zones["Performance & Trends"]
    labs = zones["Labs & Bloodwork"]
    plan_zone = zones["Today's Plan"]
    assert "Bench Press" in plan_zone, "the recorded plan populates its zone-3 card"
    assert "via strength-coach" in plan_zone, "attribution from the plan source"
    assert "awaiting plan" not in plan_zone.partition("<div class='card pcard pc-training'>")[2].partition("<div class='card pcard pc-")[0]
    assert "Bench Press" not in trends, "plan content must not leak into trends"
    assert "Bench Press" not in labs, "plan content must not leak into the labs strip"
    # Second consumer, not a re-route: the peptide card reads the SAME stored
    # watch-out answer zone 7 renders.
    assert "none noticed" in plan_zone, "the peptide card reads the grouped answers"
    # The bar sparkline is the only <rect> producer (S48 invariant): the
    # biomarker series must render its bars inside zone 4 specifically.
    assert "<rect" in trends
    assert "Ferritin" in trends
    assert "ng/mL" in trends, "a registered marker's headline carries its units"
    assert "RHR" in trends
    # Trend Card v2 (beads y0h0 + i2yw) through the production path: the
    # registered rhr card carries its latest reading date on the label row,
    # the ref-range/state caption, and the numeric polarity-tinted delta chip.
    rhr_row = next(r for r in _rows(html, "Performance & Trends") if "RHR" in r)
    assert (
        "<div class='labelrow'><div class='label'>RHR</div>"
        "<span class='caption'>May 2</span></div>"
    ) in rhr_row, "the latest reading's date renders top-right on the label row"
    assert "ref 40 – 100 bpm · in range" in rhr_row, (
        "the registered marker carries its ref-range/state caption"
    )
    assert "<span class='pill tint-good'>&#9660; 3 bpm</span>" in rhr_row, (
        "the delta chip is numeric, in the metric's unit, polarity-tinted"
    )
    assert "Iron Panel" in labs
    assert "Injection Site Reaction" in labs
    assert "none noticed" in labs
    assert "Physician Feedback" in labs
    assert "discussed at visit" in labs
    # The panel's pending state renders as a state-marker element inside the
    # zone-7 Pending-draws chip row, not as a bare value or a KPI headline.
    assert "Pending draws:" in labs
    assert "<span class='state-marker'>pending</span>" in labs
    assert "Ferritin" not in labs, "biomarker rows must not leak into the labs strip"
    assert "state-marker" not in trends, "panel rows must not leak into trends"
    assert "discussed at visit" not in trends


def test_trend_chips_registered_vs_unregistered(tmp_path):
    """F15 (Trend Card v2): a registered marker's delta chip carries the
    NUMERIC movement in its own unit on the polarity-aware tint; an
    unregistered marker's chip stays neutral with NO unit suffix; a
    single-numeric-value series renders no chip."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_mixed_store(root)  # rhr 52 -> 49: registered "down" polarity, improving
    loop_schema.record_biomarker("spo2", "2026-05-01T00:00:00+00:00", 97, root)
    loop_schema.record_biomarker("spo2", "2026-05-02T00:00:00+00:00", 95, root)
    loop_schema.record_biomarker("vitamin-d", "2026-05-01T00:00:00+00:00", 41, root)

    html = generate.run("dashboard", _root=root, _out_dir=out).read_text()

    rhr_row = next(r for r in _rows(html, "Performance & Trends") if "RHR" in r)
    assert "<span class='pill tint-good'>&#9660; 3 bpm</span>" in rhr_row
    assert "improving" not in rhr_row, "the v2 chip is numeric, not the trend word"

    spo2_row = next(r for r in _rows(html, "Performance & Trends") if "Spo2" in r)
    assert "<span class='pill tint-neutral'>&#9660; 2</span>" in spo2_row, (
        "unregistered chip: neutral tint, numeric delta, NO unit suffix"
    )
    assert "improving" not in spo2_row
    assert "regressing" not in spo2_row

    vitd_row = next(r for r in _rows(html, "Performance & Trends") if "Vitamin D" in r)
    assert "pill" not in vitd_row, "a single-value series renders no delta chip"


def test_unprefixed_string_item_renders_plain_row(tmp_path):
    """F17a: an unprefixed string-valued item renders its value with no sparkline."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    store.append(
        "note",
        {"item": "note", "timepoint": "2026-05-01T00:00:00+00:00",
         "source": "manual", "value": "felt fine"},
        root=root,
    )

    html = generate.run("dashboard", _root=root, _out_dir=out).read_text()

    note_row = next(r for r in _rows(html, "Labs & Bloodwork") if "felt fine" in r)
    assert "Note" in note_row, "the catch-all routes its label through display_name"
    assert "<svg" not in note_row
    assert "<rect" not in note_row
    # PLACEMENT (ADR-0009): the catch-all lands in the labs strip (zone 7).
    assert "felt fine" in _zones(html)["Labs & Bloodwork"]


def test_biomarker_stream_all_strings_renders_plain_row(tmp_path):
    """F17b: a biomarker:: stream with ONLY string values renders the clean
    label + verbatim latest value, no sparkline."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    loop_schema.record_biomarker(
        "ferritin", "2026-05-01T00:00:00+00:00", "draw scheduled", root
    )

    html = generate.run("dashboard", _root=root, _out_dir=out).read_text()

    row = next(
        r for r in _rows(html, "Performance & Trends") if "draw scheduled" in r
    )
    assert "Ferritin" in row
    assert "<svg" not in row
    assert "<rect" not in row


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
