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
from scripts.store import loop_schema, store
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
    """Return each caption div/span's decoded text within a card fragment.

    The closing tag backreferences the opening one, so mismatched tag pairs
    never match.
    """
    return [
        html_lib.unescape(text)
        for _tag, text in re.findall(
            r"<(div|span) class='caption'>([^<]*)</\1>", fragment
        )
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
        "<div class='kpi'><div class='label'>Bodyweight</div>"
        "<div class='value'>183 lb</div></div>" in card
    ), "an unparseable timepoint renders the dateless label-over-value form"
    assert "after the trip" not in _captions(card), (
        "the raw timepoint string must never render as the date"
    )


def test_non_string_timepoint_renders_no_date_not_a_crash(tmp_path):
    """A non-string store timepoint renders the card dateless — never a crash.

    Raw `store.append` bypasses the writer validation, so the production read
    path can deliver an int timepoint to the render; `fromisoformat`'s
    documented raise for a non-str is TypeError, not ValueError."""
    root = tmp_path / "store"
    store.append(
        "biomarker::bodyweight",
        {"item": "biomarker::bodyweight", "timepoint": 20260610,
         "source": "test", "value": 184},
        root=root,
    )

    html = generate.run(
        "dashboard", _root=root, _out_dir=tmp_path / "out", _today=_TODAY
    ).read_text()

    card = next(r for r in _trend_rows(html) if "Bodyweight" in r)
    assert "<div class='label'>Bodyweight</div>" in card
    assert "184 lb" in card
    assert "20260610" not in card, "the raw timepoint must never render"


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


def test_delta_chip_in_range_polarity_toward_range_good_tint():
    """ferritin rising toward its range (in-range polarity, improving) ->
    `▲ 5 ng/mL` on the good tint."""
    card = _card(
        _read(
            "biomarker::ferritin",
            ("2026-05-11T00:00:00+00:00", 20),
            ("2026-06-10T00:00:00+00:00", 25),
        ),
        "Ferritin",
    )
    assert "<span class='pill tint-good'>&#9650; 5 ng/mL</span>" in card


def test_delta_chip_in_range_polarity_away_from_range_concern_tint():
    """ferritin falling away from its range (regressing) -> the concern tint."""
    card = _card(
        _read(
            "biomarker::ferritin",
            ("2026-05-11T00:00:00+00:00", 25),
            ("2026-06-10T00:00:00+00:00", 20),
        ),
        "Ferritin",
    )
    assert "<span class='pill tint-concern'>&#9660; 5 ng/mL</span>" in card


def test_delta_chip_within_range_movement_numeric_on_neutral():
    """Within-range movement (distance-to-range unchanged at 0) renders the
    NUMERIC delta on the neutral tint — the deliberate v2 presentation change
    from v1's word-"flat" pill: the value moved, the judgment did not."""
    card = _card(
        _read(
            "biomarker::ferritin",
            ("2026-05-11T00:00:00+00:00", 95),
            ("2026-06-10T00:00:00+00:00", 110),
        ),
        "Ferritin",
    )
    assert "<span class='pill tint-neutral'>&#9650; 15 ng/mL</span>" in card
    assert "flat" not in card, "unequal values never render the word pill"


def test_delta_chip_up_polarity_rising_good_tint():
    """hdl rising (up polarity, improving) -> the numeric delta on good tint."""
    card = _card(
        _read(
            "biomarker::hdl",
            ("2026-05-11T00:00:00+00:00", 50),
            ("2026-06-10T00:00:00+00:00", 60),
        ),
        "HDL",
    )
    assert "<span class='pill tint-good'>&#9650; 10 mg/dL</span>" in card


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


def test_mixed_tail_strictly_future_projection_renders():
    """Mixed tail: chip from the last two NUMERIC readings, date from the raw
    latest, projection rendered because its date is strictly future."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-04-11T00:00:00+00:00", 1.1),
            ("2026-05-11T00:00:00+00:00", 1.0),
            ("2026-06-01T00:00:00+00:00", 0.9),
            ("2026-06-10T00:00:00+00:00", "redraw scheduled"),
        ),
        "CRP",
    )
    assert "<span class='pill tint-good'>&#9660; 0.1 mg/L</span>" in card, (
        "the chip derives from the last two numeric readings"
    )
    # The last-two-numeric spacing is 21 days, so one step beyond Jun 1 lands
    # on Jun 22 — strictly after the card's Jun 10 latest-reading date.
    assert _captions(card) == [
        "Jun 10",
        "ref 0 – 3 mg/L",
        "→ 0.8 by Jun 22 · naive projection",
    ], "date from the raw latest; bare range (non-numeric latest); projection"


def test_mixed_tail_past_dated_projection_suppressed():
    """A projected date at or before the card's latest reading date renders NO
    caption — an extrapolation must be a forecast, never a past-dated claim."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-04-11T00:00:00+00:00", 1.1),
            ("2026-05-01T00:00:00+00:00", 1.0),
            ("2026-05-02T00:00:00+00:00", 0.9),
            ("2026-06-10T00:00:00+00:00", "redraw scheduled"),
        ),
        "CRP",
    )
    # The numeric tail projects May 3 — before the card's Jun 10 latest date.
    assert "naive projection" not in card
    assert _captions(card) == ["Jun 10", "ref 0 – 3 mg/L"]


def test_unparseable_latest_timepoint_no_date_and_no_projection():
    """An unparseable LATEST timepoint renders neither the date nor the
    projection — never a forecast on a card that cannot date its own reading."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-04-11T00:00:00+00:00", 1.1),
            ("2026-05-11T00:00:00+00:00", 1.0),
            ("2026-06-01T00:00:00+00:00", 0.9),
            ("when it settles", "redraw scheduled"),
        ),
        "CRP",
    )
    assert "naive projection" not in card
    assert _captions(card) == ["ref 0 – 3 mg/L"], (
        "no date caption, no projection caption — the bare range only"
    )


def test_same_day_last_two_numeric_no_projection():
    """A zero-interval last numeric segment projects the SAME day — not
    strictly future, so no caption (a same-day 'forecast' is fabricated)."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-04-11T00:00:00+00:00", 1.1),
            ("2026-06-10T08:00:00+00:00", 1.0),
            ("2026-06-10T20:00:00+00:00", 0.9),
        ),
        "CRP",
    )
    assert "naive projection" not in card
    assert _captions(card) == ["Jun 10", "ref 0 – 3 mg/L · in range"]


def test_projected_date_overflow_no_crash_no_caption():
    """A reading spacing that overflows the calendar renders no caption — and
    never an OverflowError crash."""
    card = _card(
        _read(
            "biomarker::crp",
            ("0001-01-01T00:00:00+00:00", 1.1),
            ("0001-01-02T00:00:00+00:00", 1.0),
            ("9999-12-31T00:00:00+00:00", 0.9),
        ),
        "CRP",
    )
    assert "naive projection" not in card
    assert _captions(card) == ["Dec 31", "ref 0 – 3 mg/L · in range"]


def test_huge_finite_values_no_infinite_projection():
    """Finite stored values whose projection overflows to inf render no
    caption — '→ inf by …' is a fabricated claim."""
    card = _card(
        _read(
            "biomarker::crp",
            ("2026-04-11T00:00:00+00:00", 8e307),
            ("2026-05-11T00:00:00+00:00", 1e308),
            ("2026-06-10T00:00:00+00:00", 1.7e308),
        ),
        "CRP",
    )
    assert "naive projection" not in card
    assert "inf" not in card


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
    assert "Jul 10" not in report, (
        "the projected DATE must not reach the report in any form"
    )
    # Sparkline coordinate attributes can legitimately contain any digit run;
    # strip them so the value check tests rendered TEXT, not plot geometry.
    assert "0.8" not in re.sub(r" points='[^']*'", "", report), (
        "the projected VALUE must not reach the report in any form"
    )


def test_zero_latest_value_renders_through_production_path(tmp_path):
    """A latest reading of 0 is a real value, never an absence (falsy-zero pin).

    crp 0.3 -> 0 through the production writer + generate.run: the `0 mg/L`
    headline, the improving chip, and the in-range verdict all render.
    """
    root = tmp_path / "store"
    loop_schema.record_biomarker("crp", "2026-05-11T00:00:00+00:00", 0.3, root)
    loop_schema.record_biomarker("crp", "2026-06-10T00:00:00+00:00", 0, root)

    html = generate.run(
        "dashboard", _root=root, _out_dir=tmp_path / "out", _today=_TODAY
    ).read_text()

    card = next(r for r in _trend_rows(html) if "CRP" in r)
    assert "<div class='value'>0 mg/L</div>" in card
    assert "<span class='pill tint-good'>&#9660; 0.3 mg/L</span>" in card
    assert "ref 0 – 3 mg/L · in range" in _captions(card)
