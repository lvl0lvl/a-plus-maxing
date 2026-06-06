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
    """A fixture store read model: the list-of-readings shape store.read returns."""
    return [
        {"item": "rhr", "timepoint": "2026-05-01T00:00:00+00:00", "source": "whoop", "value": 52},
        {"item": "rhr", "timepoint": "2026-05-02T00:00:00+00:00", "source": "whoop", "value": 54},
        {"item": "rhr", "timepoint": "2026-05-03T00:00:00+00:00", "source": "whoop", "value": 49},
        {"item": "hrv", "timepoint": "2026-05-01T00:00:00+00:00", "source": "whoop", "value": 71},
        {"item": "hrv", "timepoint": "2026-05-02T00:00:00+00:00", "source": "whoop", "value": 88},
        {"item": "hrv", "timepoint": "2026-05-03T00:00:00+00:00", "source": "whoop", "value": 63},
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


def test_emit_offline_open_zero_outbound(tmp_path):
    """AC-1: opening the emitted file under the egress guard observes 0 outbound.

    The capture wraps the file-OPEN (not emit). run is truthy == 0 outbound
    requests when the file is opened/parsed offline.
    """
    from scripts.guard.egress_guard import run

    path = emit(_inline_template, _store_read(), _out_dir=tmp_path)

    def open_file():
        # Parsing the saved HTML must not reach the network for any asset.
        html = path.read_text()
        assert _external_refs(html) == []

    assert run(open_file)


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


def test_emit_raises_on_external_asset(tmp_path):
    """AC-6: emit RAISES and writes no file when an asset resolves to an external URL."""
    sr = _store_read()
    out = tmp_path / "external"
    out.mkdir()

    # A template whose assembled output references an off-file asset.
    def bad_template(store_read):
        return "<html><head></head><body>"\
            "<img src='https://example.com/logo.png'></body></html>"

    with pytest.raises(ValueError):
        emit(bad_template, sr, _out_dir=out)
    assert list(out.iterdir()) == [], "emit must write 0 files when it refuses"


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
    """AC-4: two dashboard generations from the same store read have 0 structural diff.

    A data-masked structural diff of the two outputs returns 0 differences,
    proving the template/component markup is deterministic and not
    data-order-dependent.
    """
    from vault.design.templates import dashboard

    sr = _store_read()
    a = emit(dashboard, sr, _out_dir=tmp_path / "gen-a").read_text()
    b = emit(dashboard, sr, _out_dir=tmp_path / "gen-b").read_text()
    diff = [
        (i, x, y)
        for i, (x, y) in enumerate(zip(_mask_data(a).splitlines(), _mask_data(b).splitlines()))
        if x != y
    ]
    assert _mask_data(a) == _mask_data(b), f"structural diff != 0: {diff[:3]}"


def test_report_structural_identity(tmp_path):
    """AC-4: the report shares the structural-identity property (0 masked diff)."""
    from vault.design.templates import report

    sr = _store_read()
    a = emit(report, sr, _out_dir=tmp_path / "gen-a").read_text()
    b = emit(report, sr, _out_dir=tmp_path / "gen-b").read_text()
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
    return dict(re.findall(r"--([a-z]+)\s*:\s*(#[0-9A-Fa-f]{6})", html))


def _rendered_series_hexes(html):
    """Collect the series/category hex colors actually used in the rendered output.

    Reads the stroke colors on the inline-SVG sparklines (the per-series colors)
    plus the swatch backgrounds — the colors that distinguish categories.
    """
    strokes = set(re.findall(r"stroke='(#[0-9A-Fa-f]{6})'", html))
    vars_used = _root_vars(html)
    # swatches reference var(--good/--watch/--concern); resolve to their hexes
    sw = re.findall(r"background:var\(--(good|watch|concern)\)", html)
    swatch_hexes = {vars_used[name] for name in sw if name in vars_used}
    return strokes | swatch_hexes


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

    # --- palette membership: every series color RENDERED is a member of the
    # recorded good/watch/concern hex set (read from the decision, not the module)
    expected_set = {v.lower() for v in expected.values()}
    rendered = {h.lower() for h in _rendered_series_hexes(html)}
    assert rendered, "no series colors found in rendered output"
    assert rendered <= expected_set, (
        f"rendered series colors {rendered} not all in recorded palette {expected_set}"
    )

    # --- never red-only: no semantic state distinguished by red alone (the
    # concern state pairs a glyph with its color, and the legend carries glyphs)
    assert "&#9632;" in html or "&#9650;" in html, "semantic states must carry glyphs, not color alone"

    # --- measured CIEDE2000 deltaE for EVERY adjacent-series pair, under EACH
    # recorded simulation, above the recorded floor (computed number vs recorded)
    roles = ("good", "watch", "concern")
    sims = decision["simulation"].split("+")
    for i in range(len(roles) - 1):
        c1 = _hex_to_rgb(expected[roles[i]])
        c2 = _hex_to_rgb(expected[roles[i + 1]])
        for sim in sims:
            s1 = _simulate(c1, sim)
            s2 = _simulate(c2, sim)
            de = _ciede2000(_rgb_to_lab(s1), _rgb_to_lab(s2))
            print(f"AC-3 deltaE {roles[i]}/{roles[i+1]} under {sim} = {de:.2f} (floor {floor})")
            assert de > floor, f"deltaE {de:.2f} for {roles[i]}/{roles[i+1]} under {sim} <= floor {floor}"

    # --- @media print present (print-safe)
    assert "@media print" in html, "emitted file must carry an @media print block"
