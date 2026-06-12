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


@pytest.mark.parametrize("marker, units", [
    ("bodyweight", "lb"),
    ("sleep-hours", "h"),
    ("est-1rm", "lb"),
    ("steps", "steps"),
])
def test_get_fitness_marker_units_without_range(marker, units):
    """A D4 fitness marker registers its units and NO invented reference range."""
    meta = biomarker_meta.get(marker)
    assert meta["units"] == units
    assert meta["reference_range"] is None


# --- to_number ---------------------------------------------------------------


def test_to_number_nan_reads_none():
    """A "nan" cell coerces to None — never a NaN float."""
    assert biomarker_meta.to_number("nan") is None


def test_to_number_overflow_reads_none():
    """A "1e999" cell (float overflow to inf) coerces to None."""
    assert biomarker_meta.to_number("1e999") is None


# --- display_name ------------------------------------------------------------


@pytest.mark.parametrize("item, expected", [
    ("biomarker::ferritin", "Ferritin"),
    ("hrv", "HRV"),
    ("fasting-glucose", "Fasting Glucose"),
    ("watch-out::injection_site_reaction", "Injection Site Reaction"),
    ("panel::iron-panel", "Iron Panel"),
    ("biomarker::ldl", "LDL"),
    ("biomarker::est-1rm", "Est 1RM"),
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


def test_state_for_non_finite_reads_none():
    """A non-finite value reads None (neutral) — never a fabricated "concern"."""
    assert biomarker_meta.state_for("crp", "1e999") is None


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


def test_trend_sleep_hours_rising_improves():
    """The D4 "up"-polarity fitness marker: more sleep reads improving."""
    assert biomarker_meta.trend("sleep-hours", 6, 7) == "improving"


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


def test_trend_in_range_polarity_without_range_reads_none(monkeypatch):
    """An "in-range" polarity with no registered range reads None (no distance)."""
    monkeypatch.setitem(
        biomarker_meta.METADATA,
        "rangeless-marker",
        {"units": "x", "reference_range": None, "good_direction": "in-range"},
    )
    assert biomarker_meta.trend("rangeless-marker", 10, 20) is None


def test_trend_in_range_equal_distance_opposite_sides_reads_flat():
    """Equal distance-to-range on OPPOSITE sides reads flat (ferritin 20 -> 410).

    Both readings sit 10 from the (30, 400) range — below it, then above it —
    so the distance is unchanged and the verdict is flat, not improving.
    """
    assert biomarker_meta.trend("ferritin", 20, 410) == "flat"


def test_trend_in_range_landing_on_boundary_improves():
    """Moving from outside onto the range boundary (distance 10 -> 0) improves."""
    assert biomarker_meta.trend("ferritin", 20, 30) == "improving"


def test_trend_in_range_boundary_no_change_reads_flat():
    """Two readings exactly on the boundary (distance 0 -> 0) read flat."""
    assert biomarker_meta.trend("ferritin", 30, 30) == "flat"


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


# --- projection_values -------------------------------------------------------


def test_projection_values_extends_one_step_along_last_segment():
    """The projection appends ONE point continuing the last two points' slope."""
    assert biomarker_meta.projection_values([45, 52, 60]) == [45, 52, 60, 68]


def test_projection_values_negative_slope():
    """A falling last segment projects further down (naive, no clamping)."""
    assert biomarker_meta.projection_values([10, 8, 5]) == [10, 8, 5, 2]


def test_projection_values_flat_segment_projects_flat():
    """An equal last pair projects the same value again."""
    assert biomarker_meta.projection_values([7, 7]) == [7, 7, 7]


def test_projection_values_uses_only_last_two_points():
    """Earlier points never influence the projected step (last-segment slope)."""
    assert biomarker_meta.projection_values([100, 1, 2])[-1] == 3


def test_projection_values_does_not_mutate_input():
    """The input series is returned extended as a NEW list, never mutated."""
    values = [1, 2, 3]
    biomarker_meta.projection_values(values)
    assert values == [1, 2, 3]


def test_projection_min_timepoints_is_three():
    """The honest-absence guardrail constant lives on the shared seam."""
    assert biomarker_meta.PROJECTION_MIN_TIMEPOINTS == 3


def test_render_views_min_timepoints_single_sourced():
    """render_views ASSIGNS its constant from the seam (textual pin + value).

    An `is` identity check would be vacuous here — CPython interns small
    ints, so a hand-spelled 3 would pass it; the source-line pin is what
    proves the single-sourcing.
    """
    import inspect

    from scripts.generate import render_views

    assert (
        "PROJECTION_MIN_TIMEPOINTS = biomarker_meta.PROJECTION_MIN_TIMEPOINTS"
        in inspect.getsource(render_views)
    ), "render_views must assign the constant FROM the biomarker_meta seam"
    assert (
        render_views.PROJECTION_MIN_TIMEPOINTS
        == biomarker_meta.PROJECTION_MIN_TIMEPOINTS
    )
