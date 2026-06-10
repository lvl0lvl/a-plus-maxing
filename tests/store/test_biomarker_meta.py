"""Tests for the biomarker metadata registry (ADR-0008 D1).

Covers the four accessors: prefix-tolerant lookup with honest-absence None for
unknown markers, clean display labels with acronym casing, inclusive-bounds
range state with no invented "watch" band, and polarity-aware trend labels for
all three good-direction polarities including the in-range distance logic.
"""

import pytest

from scripts.store import biomarker_meta


# --- get -------------------------------------------------------------------


def test_get_resolves_bare_marker():
    """A bare marker name resolves to its METADATA entry."""
    assert biomarker_meta.get("ferritin") == biomarker_meta.METADATA["ferritin"]


@pytest.mark.parametrize("prefixed", [
    "biomarker::ferritin",
    "panel::ferritin",
    "watch-out::ferritin",
])
def test_get_strips_stream_prefix(prefixed):
    """A stream-prefixed item resolves to the same entry as the bare name."""
    assert biomarker_meta.get(prefixed) == biomarker_meta.METADATA["ferritin"]


def test_get_is_case_insensitive():
    """An upper-cased marker name resolves (lookup lowercases)."""
    assert biomarker_meta.get("FERRITIN") == biomarker_meta.METADATA["ferritin"]


@pytest.mark.parametrize("item", ["spo2", "biomarker::mystery-marker", ""])
def test_get_unknown_marker_returns_none(item):
    """An unregistered marker reads None — never a fabricated entry."""
    assert biomarker_meta.get(item) is None


# --- display_name ------------------------------------------------------------


@pytest.mark.parametrize("item, expected", [
    ("biomarker::ferritin", "Ferritin"),
    ("hrv", "HRV"),
    ("fasting-glucose", "Fasting Glucose"),
    ("watch-out::injection_site_reaction", "Injection Site Reaction"),
    ("panel::iron-panel", "Iron Panel"),
    ("biomarker::ldl", "LDL"),
])
def test_display_name(item, expected):
    """display_name strips the prefix and title-cases words, acronyms upper-case."""
    assert biomarker_meta.display_name(item) == expected


# --- state_for ---------------------------------------------------------------


def test_state_for_in_range_reads_good():
    """A value inside the registered range reads good."""
    assert biomarker_meta.state_for("rhr", 60) == "good"


def test_state_for_out_of_range_reads_concern():
    """A value outside the registered range reads concern."""
    assert biomarker_meta.state_for("rhr", 110) == "concern"


@pytest.mark.parametrize("value", [40, 100])
def test_state_for_boundary_is_inclusive(value):
    """A value exactly on a range bound reads good (inclusive bounds)."""
    assert biomarker_meta.state_for("rhr", value) == "good"


def test_state_for_prefixed_item_resolves():
    """The stream-prefixed item name resolves to the same verdict."""
    assert biomarker_meta.state_for("biomarker::crp", 5.0) == "concern"


def test_state_for_coerces_numeric_strings():
    """A numeric string value is judged like its number."""
    assert biomarker_meta.state_for("rhr", "60") == "good"


@pytest.mark.parametrize("value", ["pending", None, ""])
def test_state_for_non_numeric_reads_none(value):
    """A non-coercible value reads None (neutral)."""
    assert biomarker_meta.state_for("rhr", value) is None


def test_state_for_no_registered_range_reads_none():
    """A registered marker without a reference range reads None (hrv)."""
    assert biomarker_meta.state_for("hrv", 50) is None


def test_state_for_unknown_marker_reads_none():
    """An unregistered marker reads None — no fabricated judgment."""
    assert biomarker_meta.state_for("spo2", 97) is None


def test_state_for_never_returns_watch():
    """No value on any registered marker reads watch (reserved per ADR-0008 D1)."""
    for marker, meta in biomarker_meta.METADATA.items():
        if meta["reference_range"] is None:
            continue
        low, high = meta["reference_range"]
        for value in (low - 1, low, (low + high) / 2, high, high + 1):
            assert biomarker_meta.state_for(marker, value) != "watch"


# --- trend -------------------------------------------------------------------


def test_trend_up_polarity_rising_improves():
    """An "up" marker rising reads improving (hrv)."""
    assert biomarker_meta.trend("hrv", 50, 60) == "improving"


def test_trend_up_polarity_falling_regresses():
    """An "up" marker falling reads regressing (hrv)."""
    assert biomarker_meta.trend("hrv", 60, 50) == "regressing"


def test_trend_down_polarity_rising_regresses():
    """A "down" marker rising reads regressing (alt)."""
    assert biomarker_meta.trend("alt", 30, 50) == "regressing"


def test_trend_down_polarity_falling_improves():
    """A "down" marker falling reads improving (alt)."""
    assert biomarker_meta.trend("alt", 50, 30) == "improving"


def test_trend_equal_values_read_flat():
    """Equal prev/latest values read flat regardless of polarity."""
    assert biomarker_meta.trend("hrv", 50, 50) == "flat"
    assert biomarker_meta.trend("alt", 30, 30) == "flat"


def test_trend_in_range_distance_shrinking_improves():
    """An "in-range" marker moving toward its range reads improving (ferritin)."""
    assert biomarker_meta.trend("ferritin", 20, 28) == "improving"


def test_trend_in_range_distance_growing_regresses():
    """An "in-range" marker moving away from its range reads regressing."""
    assert biomarker_meta.trend("ferritin", 50, 20) == "regressing"


def test_trend_in_range_both_inside_read_flat():
    """Two in-range values (distance 0 -> 0) read flat, not improving."""
    assert biomarker_meta.trend("ferritin", 50, 60) == "flat"


def test_trend_prefixed_item_resolves():
    """The stream-prefixed item name resolves the same polarity."""
    assert biomarker_meta.trend("biomarker::alt", 30, 50) == "regressing"


@pytest.mark.parametrize("prev, latest", [("x", 50), (50, "x"), (None, 50)])
def test_trend_non_numeric_reads_none(prev, latest):
    """A non-coercible value on either side reads None."""
    assert biomarker_meta.trend("hrv", prev, latest) is None


def test_trend_unknown_marker_reads_none():
    """An unregistered marker reads None — no fabricated value judgment."""
    assert biomarker_meta.trend("spo2", 95, 98) is None
