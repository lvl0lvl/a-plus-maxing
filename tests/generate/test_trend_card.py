"""Tests for the zone-4 Trend Card v2 anatomy (beads y0h0 + i2yw).

Pins the four signed card additions (visual spec zone 4 as amended 2026-06-12):
the latest reading's date top-right on the label row (`Jun 10`; an unparseable
timepoint renders NO date — honest absence); the ref-range/state caption under
the value row (collapsing to the performance-metric caption without a range);
the NUMERIC delta chip in the metric's own unit, tinted by the polarity-aware
semantic state (flat keeps the prior presentation); and the naive-projection
caption under the sparkline — derivable only at >= PROJECTION_MIN_TIMEPOINTS
numeric readings with parseable dates, and DASHBOARD-ONLY: the placement tests
run the production `generate.run` path for BOTH artifacts and assert the
projection never reaches the physician report (S52 operator direction — an
extrapolation must not read as clinical data).
"""

import datetime
import html as html_lib
import re

from scripts.generate import generate
from scripts.store import loop_schema
from vault.design.templates import dashboard

# A fixed mid-week date for the calendar seam: Wednesday 2026-06-10.
_TODAY = datetime.date(2026, 6, 10)


def _zones(html):
    """Map each rendered zone's decoded h2 title to its full section markup."""
    out = {}
    for section in re.findall(r"<section class='zone'[^>]*>.*?</section>", html, re.S):
        title = re.search(r"<h2[^>]*>([^<]*)</h2>", section).group(1)
        out[html_lib.unescape(title)] = section
    return out


def _trend_rows(html):
    """Split the Performance & Trends zone into its kpi-row card fragments."""
    return _zones(html)["Performance & Trends"].split("<div class='kpi-row'>")[1:]


def _card(read, name):
    """Render `read` and return the zone-4 card fragment carrying `name`."""
    html = dashboard.render(read, _today=_TODAY)
    return next(r for r in _trend_rows(html) if name in r)


def _read(item, *readings):
    """Build a store read for one item from (timepoint, value) pairs."""
    return [
        {"item": item, "timepoint": t, "source": "test", "value": v}
        for t, v in readings
    ]


def _captions(fragment):
    """Return each caption div's decoded text within a card fragment."""
    return [
        html_lib.unescape(c)
        for c in re.findall(r"<(?:div|span) class='caption'>([^<]*)</(?:div|span)>", fragment)
    ]


# --------------------------------------------------------------------------- #
# Reading date — top-right on the label row
# --------------------------------------------------------------------------- #


def test_reading_date_renders_from_latest_timepoint():
    """The label row carries the LATEST reading's date as `Jun 10`."""
    card = _card(
        _read(
            "biomarker::bodyweight",
            ("2026-06-01T00:00:00+00:00", 184),
            ("2026-06-10T00:00:00+00:00", 183),
        ),
        "Bodyweight",
    )
    assert (
        "<div class='labelrow'><div class='label'>Bodyweight</div>"
        "<span class='caption'>Jun 10</span></div>"
    ) in card


def test_reading_date_is_the_latest_not_the_first():
    """The date is the latest reading's, never an earlier timepoint's."""
    card = _card(
        _read(
            "biomarker::bodyweight",
            ("2026-05-03T00:00:00+00:00", 184),
            ("2026-06-10T00:00:00+00:00", 183),
        ),
        "Bodyweight",
    )
    assert "May 3" not in card
    assert "Jun 10" in card


def test_unparseable_timepoint_renders_no_date():
    """A non-ISO latest timepoint renders NO date — not a crash, not raw text."""
    card = _card(
        _read(
            "biomarker::bodyweight",
            ("next visit", 184),
            ("after the trip", 183),
        ),
        "Bodyweight",
    )
    assert (
        "<div class='labelrow'><div class='label'>Bodyweight</div></div>" in card
    ), "an unparseable timepoint must render an empty date slot"
    assert "after the trip" not in _captions(card), (
        "the raw timepoint string must never render as the date"
    )


# --------------------------------------------------------------------------- #
# Ref-range / state caption — under the value row
# --------------------------------------------------------------------------- #


def test_range_caption_registered_in_range():
    """A registered marker with an in-range latest reads `ref … · in range`."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-05-11T00:00:00+00:00", 1.5),
            ("2026-06-10T00:00:00+00:00", 1.2),
        ),
        "CRP",
    )
    assert "ref 0 – 3 mg/L · in range" in _captions(card)


def test_range_caption_registered_out_of_range():
    """An out-of-range latest reads `ref … · out of range`."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-05-11T00:00:00+00:00", 4.1),
            ("2026-06-10T00:00:00+00:00", 5.0),
        ),
        "CRP",
    )
    assert "ref 0 – 3 mg/L · out of range" in _captions(card)


def test_range_caption_non_numeric_latest_has_no_state_suffix():
    """A non-numeric latest renders the range with NO in/out-of-range verdict."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-05-11T00:00:00+00:00", 1.5),
            ("2026-06-10T00:00:00+00:00", "redraw scheduled"),
        ),
        "CRP",
    )
    captions = _captions(card)
    assert "ref 0 – 3 mg/L" in captions, "the bare range renders with no suffix"
    assert "in range" not in " ".join(captions)
    assert "out of range" not in " ".join(captions)


def test_range_caption_registered_without_range_collapses():
    """A registered rangeless marker reads the performance-metric caption."""
    card = _card(
        _read(
            "biomarker::bodyweight",
            ("2026-06-01T00:00:00+00:00", 184),
            ("2026-06-10T00:00:00+00:00", 183),
        ),
        "Bodyweight",
    )
    assert "no reference range · performance metric" in _captions(card)
    assert "ref " not in card


def test_range_caption_unregistered_collapses():
    """An unregistered marker collapses to the same performance-metric caption."""
    card = _card(
        _read(
            "biomarker::spo2",
            ("2026-06-01T00:00:00+00:00", 97),
            ("2026-06-10T00:00:00+00:00", 95),
        ),
        "Spo2",
    )
    assert "no reference range · performance metric" in _captions(card)


# --------------------------------------------------------------------------- #
# Numeric delta chip — value, arrow, unit, polarity-aware tint
# --------------------------------------------------------------------------- #


def test_delta_chip_improving_renders_good_tint_with_unit():
    """crp falling (down polarity, improving) -> `▼ 0.3 mg/L` on the good tint."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-05-11T00:00:00+00:00", 5.2),
            ("2026-06-10T00:00:00+00:00", 4.9),
        ),
        "CRP",
    )
    assert "<span class='pill tint-good'>&#9660; 0.3 mg/L</span>" in card
    assert "improving" not in card, "the v2 chip is numeric, not the trend word"


def test_delta_chip_regressing_renders_concern_tint():
    """alt rising (down polarity, regressing) -> `▲ 20 U/L` on the concern tint."""
    card = _card(
        _read(
            "biomarker::alt",
            ("2026-05-11T00:00:00+00:00", 30),
            ("2026-06-10T00:00:00+00:00", 50),
        ),
        "ALT",
    )
    assert "<span class='pill tint-concern'>&#9650; 20 U/L</span>" in card


def test_delta_chip_no_polarity_renders_neutral_tint():
    """bodyweight (no polarity) -> the numeric delta on the neutral tint."""
    card = _card(
        _read(
            "biomarker::bodyweight",
            ("2026-06-01T00:00:00+00:00", 184),
            ("2026-06-10T00:00:00+00:00", 183),
        ),
        "Bodyweight",
    )
    assert "<span class='pill tint-neutral'>&#9660; 1 lb</span>" in card


def test_delta_chip_unregistered_no_unit_suffix_neutral():
    """An unregistered marker's delta carries NO unit and stays neutral."""
    card = _card(
        _read(
            "biomarker::spo2",
            ("2026-06-01T00:00:00+00:00", 97),
            ("2026-06-10T00:00:00+00:00", 95),
        ),
        "Spo2",
    )
    assert "<span class='pill tint-neutral'>&#9660; 2</span>" in card


def test_delta_chip_flat_equal_values_keeps_word_pill():
    """Equal values on a polarity marker keep the existing `flat` word pill."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-05-11T00:00:00+00:00", 2.0),
            ("2026-06-10T00:00:00+00:00", 2.0),
        ),
        "CRP",
    )
    assert "<span class='pill tint-neutral'>flat</span>" in card
    assert "&#9650;" not in card and "&#9660;" not in card


def test_delta_chip_flat_equal_values_unregistered_keeps_arrow():
    """Equal values on an unregistered marker keep the neutral flat arrow."""
    card = _card(
        _read(
            "biomarker::spo2",
            ("2026-06-01T00:00:00+00:00", 97),
            ("2026-06-10T00:00:00+00:00", 97),
        ),
        "Spo2",
    )
    assert "<span class='pill tint-neutral'>&#8594;</span>" in card


def test_single_numeric_reading_renders_no_chip():
    """Fewer than 2 numeric readings -> no delta chip (existing behavior)."""
    card = _card(
        _read("biomarker::crp", ("2026-06-10T00:00:00+00:00", 1.2)),
        "CRP",
    )
    assert "pill" not in card, "a single-value series renders no delta chip"


# --------------------------------------------------------------------------- #
# Naive-projection caption — under the sparkline, honest absence
# --------------------------------------------------------------------------- #

_CRP_THREE = (
    ("2026-04-11T00:00:00+00:00", 1.1),
    ("2026-05-11T00:00:00+00:00", 1.0),
    ("2026-06-10T00:00:00+00:00", 0.9),
)


def test_projection_caption_renders_exact_form_at_three_timepoints():
    """>=3 numeric readings render `→ {v} by {date} · naive projection`.

    Slope 1.0 -> 0.9 projects 0.8; the last two dates are 30 days apart, so
    one step beyond Jun 10 lands on Jul 10 — the spec literal exactly.
    """
    card = _card(_read("biomarker::crp", *_CRP_THREE), "CRP")
    assert "→ 0.8 by Jul 10 · naive projection" in _captions(card)


def test_projection_caption_sits_after_the_sparkline():
    """The projection caption renders under the bar sparkline, not above it."""
    card = _card(_read("biomarker::crp", *_CRP_THREE), "CRP")
    assert card.index("</svg>") < card.index("naive projection")


def test_projection_caption_absent_below_three_timepoints():
    """2 numeric readings -> NO projection caption (honest absence)."""
    card = _card(_read("biomarker::crp", *_CRP_THREE[1:]), "CRP")
    assert "naive projection" not in card
    assert "→" not in card


def test_projection_caption_absent_when_dates_unparseable():
    """3 numeric readings with unparseable dates -> NO caption, never a fabricated date."""
    card = _card(
        _read(
            "biomarker::crp",
            ("first draw", 1.1),
            ("second draw", 1.0),
            ("third draw", 0.9),
        ),
        "CRP",
    )
    assert "naive projection" not in card
    assert "0.8" not in card, "no projected value may render without real dates"


# --------------------------------------------------------------------------- #
# Placement + negative — the projection is DASHBOARD-ONLY (production path)
# --------------------------------------------------------------------------- #


def _seed_projectable_store(root):
    """Seed crp with 3 monthly readings via the production writer."""
    for timepoint, value in _CRP_THREE:
        loop_schema.record_biomarker("crp", timepoint, value, root)


def test_projection_renders_on_dashboard_not_on_report(tmp_path):
    """generate.run over the SAME store: the caption is in the dashboard
    artifact and appears NOWHERE in the physician report (S52 operator
    direction — an extrapolation must not read as clinical data)."""
    root = tmp_path / "store"
    _seed_projectable_store(root)

    dash = generate.run(
        "dashboard", _root=root, _out_dir=tmp_path / "out", _today=_TODAY
    ).read_text()
    report = generate.run(
        "report", _root=root, _out_dir=tmp_path / "out"
    ).read_text()

    assert "→ 0.8 by Jul 10 · naive projection" in dash, (
        "the dashboard artifact must carry the projection caption"
    )
    assert "naive projection" not in report, (
        "the physician report must never carry the projection"
    )
    assert "0.8" not in report, (
        "the projected VALUE must not reach the report in any form"
    )
    assert "Jul 10" not in report, (
        "the projected DATE must not reach the report in any form"
    )
