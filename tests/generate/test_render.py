"""Tests for the V1 render engine + template component library (ADR-0004-T1).

`render.emit(template, store_read)` writes ONE self-contained HTML file (inline
CSS + inline SVG, no external assets), returns its path, reads operator data only
from the passed store read model, and RAISES on any external-URL asset reference.
The accessibility gate (`test_contrast_and_colorblind`) asserts COMPUTED numbers
(AA contrast ratio, CIEDE2000 deltaE under deuteranopia/protanopia simulation),
with the expected palette + deltaE floor READ FROM the independently-recorded
vault/decisions palette entry — not from the production component_set module —
so the gate is falsifiable if the production palette drifts.
"""

import math
import re
from pathlib import Path

import pytest

from scripts.generate import render
from scripts.generate.render import emit
from vault.design.templates import component_set

REPO_ROOT = Path(__file__).resolve().parents[2]
DECISION_ENTRY = REPO_ROOT / "vault/decisions/2026-06-05-render-colorblind-safe-palette.md"

# An external-reference is a src=/href=/url( whose target is neither a data: URI
# nor a same-document #fragment. Inline assets (data:/#frag) are allowed; anything
# resolving off the file (http(s)://, //cdn, protocol-relative, bare path) is not.
_REF_RE = re.compile(r"""(?:src|href)\s*=\s*['"]([^'"]*)['"]|url\(\s*['"]?([^'")]*)['"]?\s*\)""", re.I)


def _store_read():
    """A fixture store read model: the list-of-readings shape store.read returns.

    Carries three registry-backed items exercising every data-driven
    registry color (ADR-0008: "watch" is reserved, never data-driven):
    rhr's latest is in-range (good), crp's latest is out-of-range (concern),
    and hrv carries no registered range (neutral -> muted), so the AC-3 gate
    walks the rendered colors over real registry-driven output.
    """
    return [
        {"item": "rhr", "timepoint": "2026-05-01T00:00:00+00:00", "source": "whoop", "value": 52},
        {"item": "rhr", "timepoint": "2026-05-02T00:00:00+00:00", "source": "whoop", "value": 54},
        {"item": "rhr", "timepoint": "2026-05-03T00:00:00+00:00", "source": "whoop", "value": 49},
        {"item": "hrv", "timepoint": "2026-05-01T00:00:00+00:00", "source": "whoop", "value": 71},
        {"item": "hrv", "timepoint": "2026-05-02T00:00:00+00:00", "source": "whoop", "value": 88},
        {"item": "hrv", "timepoint": "2026-05-03T00:00:00+00:00", "source": "whoop", "value": 63},
        {"item": "crp", "timepoint": "2026-05-01T00:00:00+00:00", "source": "lab", "value": 5.2},
        {"item": "crp", "timepoint": "2026-05-02T00:00:00+00:00", "source": "lab", "value": 6.1},
        {"item": "crp", "timepoint": "2026-05-03T00:00:00+00:00", "source": "lab", "value": 7.3},
    ]


def _store_read_variant():
    """A second read: SAME items/structure as `_store_read`, DIFFERENT values + order.

    Same three items, same per-item reading count, identical non-data text, so it
    is structurally equivalent — but every value differs and the readings are
    reordered. The values keep each item's registry-driven state AND trend
    direction equal to `_store_read`'s (rhr good/improving, crp
    concern/regressing, hrv neutral/regressing), since state classes and trend
    words are data-derived markup under ADR-0008. Two generations from
    `_store_read` vs this one are byte-different pre-mask, so the
    masked-structure equality is load-bearing.
    """
    return [
        {"item": "crp", "timepoint": "2026-06-03T00:00:00+00:00", "source": "lab", "value": 8.4},
        {"item": "crp", "timepoint": "2026-06-01T00:00:00+00:00", "source": "lab", "value": 9.0},
        {"item": "crp", "timepoint": "2026-06-02T00:00:00+00:00", "source": "lab", "value": 9.6},
        {"item": "hrv", "timepoint": "2026-06-02T00:00:00+00:00", "source": "whoop", "value": 92},
        {"item": "hrv", "timepoint": "2026-06-01T00:00:00+00:00", "source": "whoop", "value": 80},
        {"item": "hrv", "timepoint": "2026-06-03T00:00:00+00:00", "source": "whoop", "value": 65},
        {"item": "rhr", "timepoint": "2026-06-01T00:00:00+00:00", "source": "whoop", "value": 60},
        {"item": "rhr", "timepoint": "2026-06-03T00:00:00+00:00", "source": "whoop", "value": 55},
        {"item": "rhr", "timepoint": "2026-06-02T00:00:00+00:00", "source": "whoop", "value": 48},
    ]


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
    """Return every src/href/url() target in the file, INCLUDING inline data: URIs.

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


def _inline_template(store_read):
    """A Cycle-1 template assembling the real component_set (no dashboard dependency).

    Exercises the engine + component library end-to-end for the PII-boundary tests
    without coupling Cycle 1 to the dashboard/report modules (those are Cycle 2).
    """
    body = (
        "<div class='wrap'>"
        f"{component_set.tldr_banner('inline cycle-1 fixture')}"
        f"{component_set.legend()}"
        f"{component_set.kpi('rhr', store_read[0]['value'])}"
        f"{component_set.sparkline([r['value'] for r in store_read], 'good')}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{component_set.head('fixture')}<body>{body}</body></html>"


# --------------------------------------------------------------------------- #
# Cycle 1 — engine + component library + PII boundary (AC-1, AC-5, AC-6)
# --------------------------------------------------------------------------- #


def test_emit_returns_written_path(tmp_path):
    """emit returns the path of the one self-contained file it wrote (AC-1)."""
    path = emit(_inline_template, _store_read(), _out_dir=tmp_path)
    assert isinstance(path, Path)
    assert path.exists()
    assert path.is_file()


def test_emit_zero_external_asset_references(tmp_path):
    """AC-1: the emitted file carries 0 off-file src/href/url() references."""
    path = emit(_inline_template, _store_read(), _out_dir=tmp_path)
    html = path.read_text()
    refs = _external_refs(html)
    assert refs == [], f"expected 0 external references, found {refs}"


def _inline_data_asset_template(store_read):
    """A template carrying one inline `data:` image asset (resolves locally, no net)."""
    pixel = "data:image/gif;base64,R0lGODlhAQABAAAAACw="
    body = (
        "<div class='wrap'>"
        f"{component_set.tldr_banner('offline-open fixture')}"
        f"<img src='{pixel}'>"
        f"{component_set.sparkline([r['value'] for r in store_read], 'good')}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{component_set.head('fixture')}<body>{body}</body></html>"


def test_emit_offline_open_zero_outbound(tmp_path):
    """AC-1: resolving the emitted file's assets under the egress guard observes 0 outbound.

    The closure parses the emitted file for EVERY asset reference and actually
    attempts to OPEN each target — so the egress guard would observe a network
    attempt if any reference resolved off-host. With all-inline `data:` assets the
    captured outbound count stays 0 (urlopen resolves data: URIs in-process). This
    proves something distinct from the static `_external_refs(html) == []` check.
    """
    import urllib.request

    from scripts.guard.egress_guard import run

    path = emit(_inline_data_asset_template, _store_read(), _out_dir=tmp_path)

    def open_and_walk_assets():
        html = path.read_text()
        refs = _all_asset_refs(html)
        assert refs, "fixture must carry at least one asset ref to make the walk meaningful"
        for target in refs:
            # A data: URI resolves in-process; an off-host URL would attempt a
            # socket connect here, which the OS egress guard would surface.
            with urllib.request.urlopen(target) as resp:
                resp.read()

    assert run(open_and_walk_assets)


def test_emit_egress_zero_call(tmp_path):
    """AC-5: a real emit wrapped in one closure under the egress guard is truthy.

    0 outbound calls observed across the whole emit invocation — the render path
    reads only the store read model and fetches no remote data/asset.
    """
    from scripts.guard.egress_guard import run

    sr = _store_read()
    out = tmp_path / "emit-under-guard"
    out.mkdir()

    def do_emit():
        emit(_inline_template, sr, _out_dir=out)

    assert run(do_emit)


def test_emit_reads_only_store_argument(tmp_path, monkeypatch):
    """AC-5: emit takes its data from the store_read arg, not independent discovery.

    Forcing store.read to raise proves emit never calls it — it consumes the read
    model it was handed.
    """
    from scripts.store import store

    def forbidden(*a, **k):
        raise AssertionError("emit must not call store.read; it consumes store_read")

    monkeypatch.setattr(store, "read", forbidden)
    path = emit(_inline_template, _store_read(), _out_dir=tmp_path)
    assert path.exists()


# Each fragment, embedded in a minimal document, references an off-file asset
# through a distinct syntactic vector. emit MUST raise + write 0 files for each.
_EXTERNAL_BODIES = {
    "img-https": "<body><img src='https://example.com/logo.png'></body>",
    "css-url": "<head><style>.h{background:url(https://cdn.example/bg.png)}</style></head><body></body>",
    "protocol-relative-src": "<body><img src='//cdn.example/logo.png'></body>",
    "link-href": "<head><link rel='stylesheet' href='https://cdn.example/site.css'></head><body></body>",
    "css-import": "<head><style>@import \"https://cdn.example/theme.css\";</style></head><body></body>",
    "srcset": "<body><img srcset='https://cdn.example/logo@2x.png 2x'></body>",
    "video-poster": "<body><video poster='https://cdn.example/frame.jpg'></video></body>",
    "meta-refresh": "<head><meta http-equiv='refresh' content='0;url=https://evil.example/'></head><body></body>",
}


@pytest.mark.parametrize("name", sorted(_EXTERNAL_BODIES))
def test_emit_raises_on_external_asset(tmp_path, name):
    """AC-6: emit RAISES and writes 0 files for each external-asset vector.

    Covers img/src https, CSS url(), protocol-relative src, off-file <link href>,
    CSS @import, srcset, <video poster>, and a meta-refresh redirect URL.
    """
    body = _EXTERNAL_BODIES[name]
    out = tmp_path / "external"
    out.mkdir()

    def bad_template(store_read):
        return f"<!doctype html><html>{body}</html>"

    with pytest.raises(ValueError):
        emit(bad_template, _store_read(), _out_dir=out)
    assert list(out.iterdir()) == [], "emit must write 0 files when it refuses"


def test_emit_allows_inline_data_and_fragment_assets(tmp_path):
    """AC-6 positive control: data: URI assets and #fragment hrefs do NOT raise.

    A template referencing only inline `data:` assets and same-document `#frag`
    hrefs is fully self-contained, so emit writes the file without raising.
    """
    out = tmp_path / "inline"
    out.mkdir()
    pixel = "data:image/gif;base64,R0lGODlhAQABAAAAACw="

    def inline_template(store_read):
        return (
            "<!doctype html><html><head>"
            "<style>.h{background:url('" + pixel + "')}</style></head><body>"
            f"<img src='{pixel}'><a href='#section'>jump</a>"
            "</body></html>"
        )

    path = emit(inline_template, _store_read(), _out_dir=out)
    assert path.exists()


def test_emit_allows_operator_text_containing_url(tmp_path):
    """F4 regression: a store-read data field carrying `url(http://...)` does NOT raise.

    The scan reads asset references at their syntactic positions, so benign
    operator text that happens to contain `url(http://...)` (escaped into text
    content) is not an asset reference — the report generates.
    """
    from vault.design.templates import report

    out = tmp_path / "operator-text"
    out.mkdir()
    sr = [
        {"item": "note", "timepoint": "2026-05-01T00:00:00+00:00",
         "source": "see url(http://lab.example/x)", "value": 1},
        {"item": "note", "timepoint": "2026-05-02T00:00:00+00:00",
         "source": "ref http://lab.example/y", "value": 2},
    ]
    path = emit(report, sr, _out_dir=out)
    assert path.exists()


@pytest.mark.parametrize("component", [
    component_set.sparkline,
    component_set.bar_sparkline,
])
def test_sparkline_unknown_state_raises(component):
    """F5: an unknown state token KeyErrors instead of silently rendering muted.

    "neutral" is the one approved non-SERIES state; any other token (a typo, a
    future unmapped state) fails loud, matching the render_views _STATE_DISPLAY
    contract.
    """
    with pytest.raises(KeyError):
        component([1.0, 2.0], "bogus-state")
    assert component([1.0, 2.0], "neutral")  # the approved non-SERIES state renders


def test_progress_ring_value_renders_arc_value_and_numeric_aria():
    """F17: a real 0-100 value renders the colored arc with plausible dash
    geometry, the centered value text, and a numeric aria-label."""
    svg = component_set.progress_ring("Recovery", 72, color="#117733")
    m = re.search(r"stroke-dasharray='([\d.]+) ([\d.]+)'", svg)
    assert m, "a valued ring must draw the arc dash geometry"
    arc_len, circumference = float(m.group(1)), float(m.group(2))
    assert abs(arc_len - 0.72 * circumference) < 0.1, (
        f"arc length {arc_len} must be ~72% of the circumference {circumference}"
    )
    assert "stroke='#117733'" in svg
    assert re.search(r"<text[^>]*>72</text>", svg), "the value text must render"
    assert "aria-label='72'" in svg, "a valued ring carries a numeric aria-label"


def test_progress_ring_out_of_range_value_raises():
    """F17/F3: a value outside 0-100 ValueErrors instead of rendering a
    full/overflowing ring."""
    for bogus in (150, -1):
        with pytest.raises(ValueError):
            component_set.progress_ring("Recovery", bogus, color="#117733")


def test_track_bar_fill_renders_width_and_color():
    """F17: a 60% fill renders the width:60% fill div in the given color."""
    markup = component_set.track_bar(60, "#117733")
    assert "<div class='fill' style='width:60%;background:#117733'></div>" in markup


def test_pill_unknown_tint_raises():
    """F17/F4: a tint name outside the tintable set KeyErrors — including the
    CHROME-only `today` token, which has no `.tint-*` rule."""
    for bogus in ("bogus", "today"):
        with pytest.raises(KeyError):
            component_set.pill("x", bogus)


def test_bar_sparkline_empty_series_renders_no_data_stub():
    """An empty series renders the no-data svg with zero rects."""
    svg = component_set.bar_sparkline([], "good")
    assert "aria-label='no data'" in svg
    assert "<rect" not in svg


def test_bar_sparkline_single_value_spans_width():
    """A single value renders one rect spanning the full 180px width."""
    svg = component_set.bar_sparkline([7.0], "good")
    rects = re.findall(r"<rect [^/>]*/>", svg)
    assert len(rects) == 1
    assert "width='180.0'" in rects[0]


def _rect_heights(svg):
    """Extract the height attribute of each <rect> (not the svg envelope's)."""
    return [
        re.search(r"height='([\d.]+)'", rect).group(1)
        for rect in re.findall(r"<rect [^/>]*/>", svg)
    ]


def test_bar_sparkline_constant_series_equal_heights():
    """A constant series renders equal-height bars (the span-0 fallback)."""
    heights = _rect_heights(component_set.bar_sparkline([5.0, 5.0, 5.0], "good"))
    assert len(heights) == 3
    assert len(set(heights)) == 1


def test_bar_sparkline_min_max_heights_hit_bounds():
    """The series min and max scale to the 4px and 36px height bounds."""
    heights = _rect_heights(component_set.bar_sparkline([0.0, 10.0], "good"))
    assert heights == ["4.0", "36.0"]


def test_dashboard_long_series_windows_to_cap(tmp_path):
    """F4: a 120-point series renders at most the cap's bars, every width positive.

    Without the tail window, 120 bars in the 180px envelope compute a NEGATIVE
    per-bar width — invisible/garbage rects. The dashboard must render only the
    LAST `render.MAX_TIMEPOINTS_PER_VIEW` values (the pinned ADR-0004 cap,
    single-sourced from render.py).
    """
    from vault.design.templates import dashboard

    sr = [
        {"item": "biomarker::rhr", "timepoint": f"2026-01-01T{t // 60:02d}:{t % 60:02d}:00+00:00",
         "source": "whoop", "value": 50 + (t % 7)}
        for t in range(120)
    ]
    html = emit(dashboard, sr, _out_dir=tmp_path).read_text()
    widths = [float(w) for w in re.findall(r"<rect [^>]*?width='(-?[\d.]+)'", html)]
    assert widths, "the long series must render bars"
    assert len(widths) <= render.MAX_TIMEPOINTS_PER_VIEW, (
        f"{len(widths)} rects > cap {render.MAX_TIMEPOINTS_PER_VIEW}"
    )
    assert all(w > 0 for w in widths), f"non-positive rect widths: {sorted(widths)[:3]}"


# --------------------------------------------------------------------------- #
# Cycle 2 — dashboard + report templates, size, structural identity (AC-2, AC-4, AC-7)
# --------------------------------------------------------------------------- #

SIZE_BUDGET = 500000


def _mask_data(html):
    """Mask data-dependent values so only template/component STRUCTURE remains.

    Replaces digit runs (KPI values, table cells) and SVG point coordinates with
    placeholders, leaving the markup skeleton. Two renders that share structure
    but differ in data collapse to the same masked string; a structural change
    (a moved/added/removed element) does not.
    """
    masked = re.sub(r"points='[^']*'", "points='MASKED'", html)
    masked = re.sub(r"\d+(?:\.\d+)?", "N", masked)
    return masked


def test_dashboard_size_under_budget(tmp_path):
    """AC-2: the emitted dashboard file is strictly < 500000 bytes."""
    from vault.design.templates import dashboard

    path = emit(dashboard, _store_read(), _out_dir=tmp_path)
    size = path.stat().st_size
    assert size < SIZE_BUDGET, f"dashboard {size} bytes, budget {SIZE_BUDGET}"


def test_report_size_under_budget(tmp_path):
    """AC-2: the emitted report file is strictly < 500000 bytes."""
    from vault.design.templates import report

    path = emit(report, _store_read(), _out_dir=tmp_path)
    size = path.stat().st_size
    assert size < SIZE_BUDGET, f"report {size} bytes, budget {SIZE_BUDGET}"


def test_two_generation_structural_identity(tmp_path):
    """AC-4: two dashboard generations from DIFFERENT-data reads share 0 structural diff.

    The two reads carry the same items/structure but different VALUES and reordered
    readings, so the raw outputs are byte-different; the data-masked structural diff
    returns 0, proving the markup is structurally identical DESPITE different data
    (the masking — not shared input — is load-bearing).
    """
    from vault.design.templates import dashboard

    a = emit(dashboard, _store_read(), _out_dir=tmp_path / "gen-a").read_text()
    b = emit(dashboard, _store_read_variant(), _out_dir=tmp_path / "gen-b").read_text()
    assert a != b, "different-data reads must produce byte-different output pre-mask"
    diff = [
        (i, x, y)
        for i, (x, y) in enumerate(zip(_mask_data(a).splitlines(), _mask_data(b).splitlines()))
        if x != y
    ]
    assert _mask_data(a) == _mask_data(b), f"structural diff != 0: {diff[:3]}"


def test_report_series_colors_registry_driven(tmp_path):
    """F1: the report's data-driven series colors are registry-driven, not all-muted.

    Mirrors the dashboard color leg of the AC-3 gate over the same fixture: rhr's
    latest is in-range (good) and crp's latest is out-of-range (concern), so the
    rendered sparkline strokes must include BOTH the good and concern decision
    hexes. A report path that judges state without the latest value renders every
    series muted and fails here.
    """
    from vault.design.templates import report

    expected = _parse_decision()["palette"]
    html = emit(report, _store_read(), _out_dir=tmp_path).read_text()
    colors = _rendered_series_colors(html)
    assert expected["good"].lower() in colors, f"good hex not rendered: {colors}"
    assert expected["concern"].lower() in colors, f"concern hex not rendered: {colors}"


def test_report_structural_identity(tmp_path):
    """AC-4: the report shares the structural-identity property (0 masked diff).

    Fed two DIFFERENT-data but structurally-equivalent reads, so the masked-structure
    equality — not identical input — carries the assertion.
    """
    from vault.design.templates import report

    a = emit(report, _store_read(), _out_dir=tmp_path / "gen-a").read_text()
    b = emit(report, _store_read_variant(), _out_dir=tmp_path / "gen-b").read_text()
    assert a != b, "different-data reads must produce byte-different output pre-mask"
    assert _mask_data(a) == _mask_data(b)


# --------------------------------------------------------------------------- #
# Cycle 3 — MEASURED-VALUE accessibility / color-vision-safety gate (AC-3)
# --------------------------------------------------------------------------- #
#
# The expected palette hex set, the CIEDE2000 deltaE floor, and the named
# deuteranopia/protanopia simulation are READ FROM the independently-recorded
# vault/decisions entry — NOT from component_set.py — so the gate is FALSIFIABLE
# if the production palette drifts from the recorded decision. The contrast ratio
# and per-adjacent-pair deltaE are COMPUTED numbers, never booleans.


def _parse_decision():
    """Parse the recorded palette decision: hex set, deltaE floor, simulation name.

    Reads `vault/decisions/2026-06-05-render-colorblind-safe-palette.md`, which
    records the good/watch/concern hex set, the numeric CIEDE2000 deltaE floor,
    and the named color-vision simulation. The Cycle-3 assertions read their
    expected values from here, NOT from component_set.py.

    Returns:
        (dict) keys 'palette' (role->hex), 'floor' (float), 'simulation' (str).
    """
    text = DECISION_ENTRY.read_text()
    palette = dict(re.findall(r"^(good|watch|concern)\s*=\s*(#[0-9A-Fa-f]{6})\s*$", text, re.M))
    floor = float(re.search(r"^ciede2000_delta_e_floor\s*=\s*([0-9.]+)\s*$", text, re.M).group(1))
    simulation = re.search(r"^simulation\s*=\s*(\S+)\s*$", text, re.M).group(1)
    return {"palette": palette, "floor": floor, "simulation": simulation}


def _hex_to_rgb(h):
    """Convert '#rrggbb' to an (r, g, b) tuple of 0-255 ints."""
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _srgb_to_linear(c):
    """Convert one 0-1 sRGB channel to linear-light (WCAG / IEC 61966-2-1)."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _rel_luminance(rgb):
    """WCAG relative luminance of an (r, g, b) 0-255 color."""
    r, g, b = (_srgb_to_linear(v / 255) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(fg, bg):
    """WCAG contrast ratio between two (r,g,b) colors: (L1+0.05)/(L2+0.05)."""
    l1, l2 = _rel_luminance(fg), _rel_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# Brettel/Viénot-Mollon 1999 single-plane dichromat simulation matrices,
# applied to LINEAR-light sRGB. Standard closed-form; no third-party dependency.
_SIM_MATRICES = {
    "deuteranopia": (
        (0.625, 0.375, 0.0),
        (0.70, 0.30, 0.0),
        (0.0, 0.30, 0.70),
    ),
    "protanopia": (
        (0.567, 0.433, 0.0),
        (0.558, 0.442, 0.0),
        (0.0, 0.242, 0.758),
    ),
}


def _simulate(rgb, kind):
    """Simulate a dichromat's perception of an (r,g,b) color (linear-space matrix)."""
    lin = [_srgb_to_linear(v / 255) for v in rgb]
    m = _SIM_MATRICES[kind]
    out = []
    for row in m:
        out.append(sum(row[i] * lin[i] for i in range(3)))
    # back to sRGB 0-255
    srgb = []
    for c in out:
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        srgb.append(round(max(0.0, min(1.0, c)) * 255))
    return tuple(srgb)


def _rgb_to_lab(rgb):
    """Convert an (r,g,b) 0-255 color to CIELAB (D65)."""
    r, g, b = (_srgb_to_linear(v / 255) for v in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.00000
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _ciede2000(lab1, lab2):
    """CIEDE2000 color-difference deltaE between two CIELAB colors (closed form)."""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    avg_Lp = (L1 + L2) / 2
    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    avg_C = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(avg_C ** 7 / (avg_C ** 7 + 25 ** 7))) if avg_C else 0.0
    a1p, a2p = a1 * (1 + G), a2 * (1 + G)
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    avg_Cp = (C1p + C2p) / 2

    def hp(ap, bp):
        if ap == 0 and bp == 0:
            return 0.0
        h = math.degrees(math.atan2(bp, ap))
        return h + 360 if h < 0 else h

    h1p, h2p = hp(a1p, b1), hp(a2p, b2)
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)

    if C1p * C2p == 0:
        avg_hp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        avg_hp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        avg_hp = (h1p + h2p + 360) / 2
    else:
        avg_hp = (h1p + h2p - 360) / 2

    T = (
        1
        - 0.17 * math.cos(math.radians(avg_hp - 30))
        + 0.24 * math.cos(math.radians(2 * avg_hp))
        + 0.32 * math.cos(math.radians(3 * avg_hp + 6))
        - 0.20 * math.cos(math.radians(4 * avg_hp - 63))
    )
    d_ro = 30 * math.exp(-(((avg_hp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(avg_Cp ** 7 / (avg_Cp ** 7 + 25 ** 7)) if avg_Cp else 0.0
    Sl = 1 + (0.015 * (avg_Lp - 50) ** 2) / math.sqrt(20 + (avg_Lp - 50) ** 2)
    Sc = 1 + 0.045 * avg_Cp
    Sh = 1 + 0.015 * avg_Cp * T
    Rt = -math.sin(math.radians(2 * d_ro)) * Rc
    return math.sqrt(
        (dLp / Sl) ** 2
        + (dCp / Sc) ** 2
        + (dHp / Sh) ** 2
        + Rt * (dCp / Sc) * (dHp / Sh)
    )


def _root_vars(html):
    """Parse the `:root` CSS custom properties (--name: #hex) from the emitted file."""
    return dict(re.findall(r"--([a-z-]+)\s*:\s*(#[0-9A-Fa-f]{6})", html))


def _rendered_series_colors(html):
    """Collect the data-driven series color hexes actually rendered.

    Reads the stroke colors on inline-SVG polyline sparklines AND the fill
    colors on bar-sparkline rects — the per-series colors chosen from the
    store-read data through the registry, NOT the always-present legend
    swatches (which are self-satisfying) and NOT the hero rings' neutral
    chrome (track/text — never data state). A color only appears here if a
    store-read item rendered it.
    """
    return {
        h.lower()
        for tag in re.findall(r"<(?:polyline|rect)\b[^>]*>", html)
        for h in re.findall(r"(?:stroke|fill)='(#[0-9A-Fa-f]{6})'", tag)
    }


def test_contrast_and_colorblind(tmp_path):
    """AC-3 (Wave 3->4 go/no-go): COMPUTED contrast + CIEDE2000 deltaE, never booleans.

    Reads expected palette + deltaE floor + simulation name from the recorded
    vault/decisions entry (NOT component_set.py). Computes the AA contrast ratio
    and the per-adjacent-pair CIEDE2000 deltaE under the recorded deutan/protan
    simulation from the EMITTED file; asserts each computed number against the
    recorded/WCAG thresholds. Falsifiable if the production palette drifts.
    """
    from vault.design.templates import dashboard

    decision = _parse_decision()
    expected = decision["palette"]
    floor = decision["floor"]

    html = emit(dashboard, _store_read(), _out_dir=tmp_path).read_text()
    root = _root_vars(html)

    # --- measured AA contrast ratio (>= 4.5 normal) — pinned upstream by WCAG-AA
    fg = _hex_to_rgb(root["ink"])
    bg = _hex_to_rgb(root["paper"])
    ratio = _contrast_ratio(fg, bg)
    print(f"AC-3 contrast ratio ink/paper = {ratio:.2f} (need >= 4.5)")
    assert ratio >= 4.5, f"contrast {ratio:.2f} < 4.5"
    # muted caption color must clear the large-text floor (>= 3.0)
    muted_ratio = _contrast_ratio(_hex_to_rgb(root["muted"]), bg)
    print(f"AC-3 contrast ratio muted/paper = {muted_ratio:.2f} (need >= 3.0)")
    assert muted_ratio >= 3.0, f"muted contrast {muted_ratio:.2f} < 3.0"

    # --- rendered tint fg/bg pairs: every pill `.tint-*` rule's text color on
    # its tint background, the tinted stat boxes' label (muted) + value (ink)
    # text on each tinted background, and the calendar today cell's ink text on
    # its tint — each COMPUTED >= 4.5 (WCAG AA normal text, 12px pill text).
    # A regressed tint pair (e.g. an accent base hex back on its ~10% tint)
    # turns this red.
    def resolve(color):
        m = re.fullmatch(r"var\(--([a-z-]+)\)", color)
        return root[m.group(1)] if m else color

    # `[a-z-]` in the name class: the event-category tints (lab-draw, check-in,
    # appointment) are hyphenated — a `[a-z]+` class would silently skip them
    # and the gate would never measure their pairs.
    tint_rules = re.findall(
        r"\.tint-([a-z][a-z-]*) \{ background: (#[0-9A-Fa-f]{6}); "
        r"color: (var\(--[a-z-]+\)|#[0-9A-Fa-f]{6}); \}",
        html,
    )
    assert len(tint_rules) >= 11, f"expected the full .tint-* rule set, got {tint_rules}"
    tint_pairs = [
        (f"tint-{name} text", resolve(fg), tint_bg) for name, tint_bg, fg in tint_rules
    ]
    stat_bgs = re.findall(r"\.stat\.tinted \{ background: ([^;]+); \}", html)
    assert len(stat_bgs) >= 3, f"expected the default + per-card tinted stat rules, got {stat_bgs}"
    for stat_bg in (resolve(b) for b in stat_bgs):
        tint_pairs.append(("tinted stat slabel (muted)", root["muted"], stat_bg))
        tint_pairs.append(("tinted stat sval (ink)", root["ink"], stat_bg))
    today_bg = re.search(r"\.cal \.today \{ background: (#[0-9A-Fa-f]{6})", html).group(1)
    tint_pairs.append(("calendar today cell (ink)", root["ink"], today_bg))
    # The muted other-month day cells: `.cal .dout` backgrounds carry muted
    # `.dnum` text — its value is a var() reference, resolved like the rest.
    dout_bg = resolve(
        re.search(r"\.cal \.dout \{ background: ([^;]+); \}", html).group(1)
    )
    tint_pairs.append(("calendar other-month cell (muted)", root["muted"], dout_bg))
    for what, fg_hex, bg_hex in tint_pairs:
        tint_ratio = _contrast_ratio(_hex_to_rgb(fg_hex), _hex_to_rgb(bg_hex))
        print(f"AC-3 tint contrast {what} {fg_hex}/{bg_hex} = {tint_ratio:.2f} (need >= 4.5)")
        assert tint_ratio >= 4.5, (
            f"tint pair {what} {fg_hex} on {bg_hex} computes {tint_ratio:.2f} < 4.5"
        )

    roles = ("good", "watch", "concern")

    # --- rendered semantic hexes by role, parsed from the emitted :root block —
    # the colors ACTUALLY rendered into the HTML, not the decision-vs-decision set.
    rendered_by_role = {role: root[role].lower() for role in roles}

    # --- role->hex EQUALITY against the recorded decision: each rendered role hex
    # must EQUAL the decision hex for that role (a member-collision, e.g. good
    # taking watch's hex, is now caught — subset membership would have shipped it).
    for role in roles:
        assert rendered_by_role[role] == expected[role].lower(), (
            f"rendered {role}={rendered_by_role[role]} != decision {expected[role].lower()}"
        )

    # --- the three rendered semantic colors must be mutually DISTINCT (a collision
    # -> identical hex -> ΔE 0 -> fail).
    distinct = set(rendered_by_role.values())
    assert len(distinct) == len(roles), (
        f"rendered semantic colors not mutually distinct: {rendered_by_role}"
    )

    # --- the data-driven series colors (NOT the legend swatches) must be exactly
    # the registry-driven set the seed data exercises through the PRODUCTION
    # dashboard: rhr in-range -> good, crp out-of-range -> concern, hrv
    # no-registered-range -> neutral (muted). watch is reserved (ADR-0008 D1)
    # and can never be data-driven.
    colors = _rendered_series_colors(html)
    expected_colors = {
        expected["good"].lower(), expected["concern"].lower(), root["muted"].lower()
    }
    assert colors == expected_colors, (
        f"data-driven series colors {colors} != registry-driven set {expected_colors}"
    )

    # --- never red-only: no semantic state distinguished by red alone (the
    # concern state pairs a glyph with its color, and the legend carries glyphs)
    assert "&#9632;" in html or "&#9650;" in html, "semantic states must carry glyphs, not color alone"

    # --- measured CIEDE2000 deltaE for EVERY adjacent-series pair, computed over
    # the RENDERED hexes (not the decision set), under EACH recorded simulation,
    # above the recorded floor.
    sims = decision["simulation"].split("+")
    for i in range(len(roles) - 1):
        c1 = _hex_to_rgb(rendered_by_role[roles[i]])
        c2 = _hex_to_rgb(rendered_by_role[roles[i + 1]])
        for sim in sims:
            s1 = _simulate(c1, sim)
            s2 = _simulate(c2, sim)
            de = _ciede2000(_rgb_to_lab(s1), _rgb_to_lab(s2))
            print(f"AC-3 deltaE {roles[i]}/{roles[i+1]} under {sim} = {de:.2f} (floor {floor})")
            assert de > floor, f"deltaE {de:.2f} for {roles[i]}/{roles[i+1]} under {sim} <= floor {floor}"

    # --- @media print present (print-safe)
    assert "@media print" in html, "emitted file must carry an @media print block"


# --------------------------------------------------------------------------- #
# ADR-0004-T2 — matrix/projection render path under the ADR-0004-T0 spike cap
# (AC-1 worst-case <500KB, AC-2 over-cap paginates to >=2 files, AC-3 at-cap
#  single-file + 0-external + offline-open-0-outbound, AC-4 shared-defs-once,
#  AC-5 egress-0 + 0-model + SEC-03 failing-capable). The cap (16 series-per-view
#  AND 12 timepoints-per-view) is the ADR-0004-T0 parameter re-validated against
#  the real component_set.py render (vault/decisions/2026-06-06-adr-0004-t0-cap-
#  revalidation.md: worst-case 16x12 = 34117 bytes, cap UNCHANGED).
# --------------------------------------------------------------------------- #

# The shared chart-component style def (the component_set <style>/:root block) is
# the single shared-defs source both the matrix and projection sections draw from.
# It must appear EXACTLY ONCE in an emitted view, referenced per series (not
# re-emitted per series). `:root {` is its falsifiable occurrence marker.
_SHARED_DEFS_MARKER = ":root {"


def _matrix_store(n_series, n_timepoints):
    """Build a matrix/projection store read: `n_series` items x `n_timepoints` each.

    The list-of-readings shape `store.read` returns, in timepoint order per series,
    with realistic long biomarker names + multi-digit lab magnitudes so the rendered
    bytes are representative of the worst case the cap bounds.
    """
    names = [
        "total_cholesterol", "ldl_cholesterol", "hdl_cholesterol", "triglycerides",
        "fasting_glucose", "hba1c", "hs_crp", "alt", "ferritin", "vitamin_d_25oh",
        "tsh", "free_t4", "creatinine", "egfr", "alkaline_phosphatase", "albumin",
        "sodium", "potassium", "calcium", "magnesium",
    ]
    rows = []
    for s in range(n_series):
        item = names[s % len(names)] + (f"_{s}" if s >= len(names) else "")
        for t in range(n_timepoints):
            rows.append({
                "item": item,
                "timepoint": f"2026-{(t % 12) + 1:02d}-01T00:00:00+00:00",
                "source": "lab",
                "value": 100 + s * 7 + t * 3,
            })
    return rows


def test_matrix_projection_worst_case_under_budget(tmp_path):
    """AC-1: worst-case matrix+projection at the cap maximum is < 500000 bytes.

    Renders the most asset-heavy SINGLE page — the cap maximum 16 series x 12
    timepoints, the heaviest a single emitted page holds before pagination triggers
    — through the matrix/projection path and asserts the measured byte count of the
    returned file < 500000 (a real render, not an estimate). This is the true
    single-page worst case the crit-1 gate names; a lighter input (e.g. the 10x4
    spike-measured shape) would under-shoot it.
    """
    paths = render.emit_matrix_projection(
        _matrix_store(render.MAX_SERIES_PER_VIEW, render.MAX_TIMEPOINTS_PER_VIEW),
        _out_dir=tmp_path,
    )
    assert len(paths) == 1, f"the at-cap maximum emits one file, got {len(paths)}"
    size = paths[0].stat().st_size
    assert size < SIZE_BUDGET, f"worst-case matrix+projection {size} bytes >= {SIZE_BUDGET}"


def test_matrix_projection_at_cap_single_file(tmp_path):
    """AC-3: a dataset AT the cap (16 series x 12 timepoints) emits exactly one file.

    The render at the cap's max bounds stays a single self-contained file (the
    over-cap split direction is AC-2's job, not this one).
    """
    paths = render.emit_matrix_projection(_matrix_store(16, 12), _out_dir=tmp_path)
    assert len(paths) == 1, f"a dataset AT the cap emits exactly one file, got {len(paths)}"
    assert paths[0].stat().st_size < SIZE_BUDGET


def test_matrix_projection_zero_external_references(tmp_path):
    """AC-3: the emitted matrix/projection file carries 0 off-file references."""
    paths = render.emit_matrix_projection(_matrix_store(6, 4), _out_dir=tmp_path)
    refs = _external_refs(paths[0].read_text())
    assert refs == [], f"expected 0 external references, found {refs}"


def test_matrix_projection_offline_open_zero_outbound(tmp_path):
    """AC-3: opening every asset in the emitted file under the guard observes 0 outbound.

    Parses the emitted file for EVERY asset reference and actually OPENs each target
    under the egress guard — an off-host reference would attempt a socket connect the
    guard would surface. All-inline render keeps the captured outbound count at 0.
    """
    import urllib.request

    from scripts.guard.egress_guard import run

    paths = render.emit_matrix_projection(_matrix_store(4, 4), _out_dir=tmp_path)
    path = paths[0]

    def open_and_walk_assets():
        for target in _all_asset_refs(path.read_text()):
            with urllib.request.urlopen(target) as resp:
                resp.read()

    assert run(open_and_walk_assets)


def test_matrix_projection_shared_defs_appears_once(tmp_path):
    """AC-4: the shared chart-component style def appears exactly once, referenced per view.

    The component_set shared-defs block (:root { ... }) is emitted ONCE and the
    per-series sparklines reference it (one per series), proving the markup is shared
    from component_set.py, not re-emitted per series. A per-series re-emit of the
    shared def would push the count above 1; per-series duplication of the def is 0.
    """
    n_series = 8
    paths = render.emit_matrix_projection(_matrix_store(n_series, 4), _out_dir=tmp_path)
    html = paths[0].read_text()

    shared_defs_count = html.count(_SHARED_DEFS_MARKER)
    assert shared_defs_count == 1, (
        f"shared chart-component def must appear exactly once, found {shared_defs_count}"
    )

    # the def is REFERENCED per series (one sparkline stroke per rendered series),
    # not re-declared per series: per-series duplication of the shared def is 0.
    per_series_def_duplication = shared_defs_count - 1
    assert per_series_def_duplication == 0
    series_refs = html.count("<svg ")
    assert series_refs >= n_series, (
        f"each series must reference the shared def via its own chart, "
        f"got {series_refs} charts for {n_series} series"
    )


def test_matrix_projection_egress_zero_call(tmp_path):
    """AC-5: a real matrix/projection emit under the egress guard is truthy (0 outbound).

    Wraps a real emit_matrix_projection call in ONE zero-arg closure under the guard
    and asserts truthy — 0 outbound across the whole render. The render path reads
    only the store_read it is passed and makes no model step (no lab value / symptom
    answer is dispatched anywhere — it reads the store and writes a local file).
    """
    from scripts.guard.egress_guard import run

    sr = _matrix_store(6, 4)
    out = tmp_path / "mp-under-guard"
    out.mkdir()

    def do_emit():
        render.emit_matrix_projection(sr, _out_dir=out)

    assert run(do_emit)


def test_matrix_projection_reads_only_store_argument(tmp_path, monkeypatch):
    """AC-5: the render takes its data from store_read, not independent discovery.

    Forcing store.read to raise proves the render path never calls it — the matrix/
    projection recompute consumes the read model it was handed (no model step, no
    re-parse of NDJSON).
    """
    from scripts.store import store

    def forbidden(*a, **k):
        raise AssertionError("matrix/projection render must consume store_read, not call store.read")

    monkeypatch.setattr(store, "read", forbidden)
    paths = render.emit_matrix_projection(_matrix_store(4, 4), _out_dir=tmp_path)
    assert paths and paths[0].exists()


def test_matrix_projection_egress_failing_capable(tmp_path, monkeypatch):
    """AC-5 (SEC-03, W4->5 boundary): an outbound call injected into the render path
    drives egress_guard.run to FAIL/falsy.

    Proves the guard actually intercepts THIS new render code path — not merely that
    a clean run makes 0 calls, and not merely because the function is absent. First
    asserts the (existing) render path runs clean under the guard (truthy), then
    injects a synthetic outbound socket connect into the matrix/projection assembly
    (via the shared-component sparkline it calls per series) and asserts the guard
    turns falsy. The connect is BLOCKED by the OS deny-network sandbox and that
    blocked-egress error surfaces (uncaught), which is how the guard reports the
    intercept — so the test can only pass once the production path exists AND is
    wrapped by the guard.
    """
    import socket

    from scripts.guard.egress_guard import run
    from vault.design.templates import component_set

    sr = _matrix_store(3, 4)
    out = tmp_path / "mp-leak"
    out.mkdir()

    # The render path must exist and run clean under the guard (truthy) — this turns
    # red in RED (no emit_matrix_projection yet), so the test is not a pass-on-absence.
    assert run(lambda: render.emit_matrix_projection(sr, _out_dir=out / "clean")), (
        "the matrix/projection render path must run clean (0 outbound) under the guard"
    )

    real_sparkline = component_set.sparkline

    def leaking_sparkline(values, state):
        # A synthetic outbound from inside the render. Under the guard's OS deny-
        # network sandbox the connect is blocked and raises; we let it surface so the
        # guard reports the intercept (falsy). Outside the guard this would connect.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("93.184.216.34", 80))
        finally:
            s.close()
        return real_sparkline(values, state)

    monkeypatch.setattr(component_set, "sparkline", leaking_sparkline)

    def do_emit():
        render.emit_matrix_projection(sr, _out_dir=out / "leak")

    assert not run(do_emit), "guard must FAIL when the render path makes an outbound call"


def test_matrix_projection_over_cap_paginates(tmp_path):
    """AC-2: a dataset ABOVE the ADR-0004-T0 cap paginates to >=2 files, each <500KB.

    Feeds a dataset exceeding the cap's max-series-per-view (16) so the render must
    split across artifacts rather than emit one over-cap file: >=2 returned paths,
    each strictly < 500000 bytes. A single (over-budget or over-cap) file fails.
    """
    over_cap_series = render.MAX_SERIES_PER_VIEW + 4
    paths = render.emit_matrix_projection(
        _matrix_store(over_cap_series, 4), _out_dir=tmp_path
    )
    assert len(paths) >= 2, (
        f"over-cap dataset ({over_cap_series} series > cap {render.MAX_SERIES_PER_VIEW}) "
        f"must paginate to >=2 files, got {len(paths)}"
    )
    for p in paths:
        assert p.stat().st_size < SIZE_BUDGET, f"paginated file {p} {p.stat().st_size} >= {SIZE_BUDGET}"
        # PLACEMENT, not just size: every page is within the series cap (size alone
        # can never red on a cap breach — the worst case is ~34KB).
        assert len(_page_series_from_html(p.read_text())) <= render.MAX_SERIES_PER_VIEW


def test_matrix_projection_over_cap_timepoints_paginates(tmp_path):
    """AC-2: exceeding the max-timepoints-per-view bound also paginates to >=2 files."""
    over_cap_tp = render.MAX_TIMEPOINTS_PER_VIEW + 3
    paths = render.emit_matrix_projection(
        _matrix_store(4, over_cap_tp), _out_dir=tmp_path
    )
    assert len(paths) >= 2, (
        f"over-cap timepoints ({over_cap_tp} > cap {render.MAX_TIMEPOINTS_PER_VIEW}) "
        f"must paginate to >=2 files, got {len(paths)}"
    )
    for p in paths:
        assert p.stat().st_size < SIZE_BUDGET
        # PLACEMENT, not just size: every rendered series on every page is within
        # the timepoint cap (a 13-timepoint page would stay under budget but breach).
        for item, n in _page_series_from_html(p.read_text()).items():
            assert n <= render.MAX_TIMEPOINTS_PER_VIEW, (
                f"{p.name} series {item} has {n} > cap {render.MAX_TIMEPOINTS_PER_VIEW}"
            )


def _page_series_from_html(html):
    """Parse an emitted matrix/projection page into {item: matrix_timepoint_count}.

    Each rendered series is one `kpi-row`: a KPI card carrying the item name, then a
    MATRIX sparkline (first svg, exactly one polyline point per stored timepoint) and
    a PROJECTION sparkline (one extra point). Counting the matrix sparkline's points
    recovers the REAL per-series timepoint count actually rendered onto the page — so
    a phantom empty-series row (0 points) or a dropped timepoint is detectable.

    Splits rows on the `kpi-row` boundary (the marker opening each series block) so
    nested `</div>` inside a row never mis-splits it.

    Returns:
        (dict) item name -> count of timepoints rendered in its matrix sparkline.
    """
    counts = {}
    rows = html.split("<div class='kpi-row'>")[1:]  # drop the head/legend prefix
    for row in rows:
        label = re.search(r"<div class='label'>([^<]*)</div>", row)
        first_points = re.search(r"points='([^']*)'", row)  # the matrix (first) sparkline
        if not label:
            continue
        pts = first_points.group(1).strip() if first_points else ""
        counts[label.group(1)] = len(pts.split()) if pts else 0
    return counts


def _ragged_store(specs):
    """Build a store read with per-item timepoint counts from {item: n_timepoints}."""
    rows = []
    for item, n in specs.items():
        for t in range(n):
            rows.append({
                "item": item,
                "timepoint": f"2026-{(t % 12) + 1:02d}-01T00:00:00+00:00",
                "source": "lab",
                "value": 100 + t,
            })
    return rows


def test_matrix_projection_ragged_series_no_phantom_rows(tmp_path):
    """F4: ragged-length series spanning >1 timepoint-page emit NO phantom empty row.

    A long series (spans 2 timepoint-pages) and a short series (fits page 1) must NOT
    put the short series on the long series's overflow page as a 0-value '—' row.
    Asserts no emitted page renders any series with 0 timepoints.
    """
    long_n = render.MAX_TIMEPOINTS_PER_VIEW + 5  # spans 2 timepoint-pages
    short_n = 3                                  # fits page 1 only
    sr = _ragged_store({"long_series": long_n, "short_series": short_n})

    paths = render.emit_matrix_projection(sr, _out_dir=tmp_path)
    assert len(paths) >= 2, "ragged dataset over the timepoint cap must paginate"

    for p in paths:
        counts = _page_series_from_html(p.read_text())
        for item, n in counts.items():
            assert n > 0, f"phantom empty row: {item} rendered with 0 timepoints on {p.name}"


def test_matrix_projection_pages_within_cap_bounds(tmp_path):
    """F11: EVERY emitted page is within the cap bounds (placement, not just count/size).

    Parses each emitted page and asserts per-page series count <= MAX_SERIES_PER_VIEW
    AND each rendered series's timepoint count <= MAX_TIMEPOINTS_PER_VIEW — so a cap
    breach (e.g. a 13-timepoint page) turns the test red even though it stays well
    under the 500000-byte budget.
    """
    # over BOTH bounds at once: more series than the series cap, more timepoints than
    # the timepoint cap, so pages split on both axes.
    sr = _matrix_store(render.MAX_SERIES_PER_VIEW + 4, render.MAX_TIMEPOINTS_PER_VIEW + 3)
    paths = render.emit_matrix_projection(sr, _out_dir=tmp_path)

    for p in paths:
        counts = _page_series_from_html(p.read_text())
        assert len(counts) <= render.MAX_SERIES_PER_VIEW, (
            f"page {p.name} has {len(counts)} series > cap {render.MAX_SERIES_PER_VIEW}"
        )
        for item, n in counts.items():
            assert n <= render.MAX_TIMEPOINTS_PER_VIEW, (
                f"page {p.name} series {item} has {n} timepoints "
                f"> cap {render.MAX_TIMEPOINTS_PER_VIEW}"
            )


def test_matrix_projection_pagination_preserves_all_data(tmp_path):
    """F12: pagination preserves ALL series and ALL timepoints across the pages.

    The union over every returned page must reconstruct the input's series set and
    per-series timepoint counts (counting REAL rendered data points, so a dropped
    last slice OR a phantom empty row both turn the test red). Uses ragged series so
    a uniform-length shortcut cannot pass it.
    """
    spec = {
        "alpha": render.MAX_TIMEPOINTS_PER_VIEW + 7,   # spans 2 timepoint-pages
        "beta": render.MAX_TIMEPOINTS_PER_VIEW,        # exactly one page
        "gamma": 4,                                    # short
    }
    sr = _ragged_store(spec)
    paths = render.emit_matrix_projection(sr, _out_dir=tmp_path)

    rendered = {}
    for p in paths:
        for item, n in _page_series_from_html(p.read_text()).items():
            rendered[item] = rendered.get(item, 0) + n

    assert set(rendered) == set(spec), (
        f"series set not preserved: rendered {set(rendered)} != input {set(spec)}"
    )
    for item, n in spec.items():
        assert rendered[item] == n, (
            f"timepoints for {item} not preserved: rendered {rendered[item]} != input {n}"
        )
