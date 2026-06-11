"""Shared inline-CSS/SVG component library for generated HTML artifacts.

Single definition of the reusable rendered components (header, TL;DR banner,
KPI section, inline-SVG sparklines — polyline and bar; the ADR-0009 dashboard
zone primitives — zone, awaiting, ring_scaffold), the colorblind-safe semantic
palette (good / watch / concern) that both the dashboard and report templates
draw from, and the surface-category ACCENTS chrome set (ADR-0009 D3). All
styling is inline — inline `<style>`, inline SVG — with no external asset
references, per the artifact-design-protocol single-file rule.

The palette hex set, the foreground/background contrast pairs, and the
`@media print` block are the source the accessibility gate (ADR-0004-T1 crit 3)
measures against. The hex values, the CIEDE2000 deltaE floor, the named
deuteranopia/protanopia simulation, and the metric are recorded independently in
`vault/decisions/2026-06-05-render-colorblind-safe-palette.md`; this module's
palette MUST match that recorded decision (the gate reads its expected values
from the decision, not from here).
"""

from scripts.store import biomarker_meta

# Colorblind-safe semantic palette. good/watch/concern are the three semantic
# series colors; they are spaced above the recorded CIEDE2000 deltaE floor under
# deuteranopia + protanopia simulation, never red-only. ink/paper are the body
# text/background pair carrying the AA contrast ratio. See the vault/decisions
# entry for the recorded reference set this MUST match.
PALETTE = {
    "good": "#117733",     # green — within-range / improving
    "watch": "#DDAA33",    # amber — drifting / monitor
    "concern": "#882255",  # magenta-rose — out of range (paired with glyph, never red-only)
    "ink": "#1A1A1A",      # body text
    "paper": "#FFFFFF",    # page background
    "muted": "#555555",    # captions / axis labels (AA on paper)
}

# The three semantic series colors, in series order. Adjacent pairs in this order
# are the pairs the crit-3 color-distance assertion walks.
SERIES = ("good", "watch", "concern")

# Surface-category chrome per `vault/design/dashboard-v1-design.md` (ADR-0009 D3):
# accents color zone/card chrome (headers, borders) ONLY — NEVER data state.
# Data state stays exclusively PALETTE good/watch/concern/neutral.
ACCENTS = {
    "training": "#1F6FEB",
    "nutrition": "#E8833A",
    "supplements": "#0E9AA3",
    "peptides": "#7C3AED",
    "sleep": "#5B5BD6",
}


def state_for(item, value=None):
    """Resolve an item's semantic series state from the biomarker metadata registry.

    Delegates to `biomarker_meta.state_for` (real range logic, ADR-0008 D2): a
    registered marker's numeric value inside its reference range reads "good",
    outside reads "concern". A None verdict (unregistered marker, no registered
    range, or non-numeric/absent value) reads "neutral" — no judgment possible,
    rendered muted. Shared by the dashboard, report, and matrix/projection views.

    Args:
        item (str): The tracked-item name (stream prefix tolerated).
        value (int | float | str | None, optional): The latest value the state
            judges; absent -> neutral.

    Returns:
        (str) "good", "concern", or "neutral".
    """
    state = biomarker_meta.state_for(item, value)
    return state if state is not None else "neutral"


def _style_block():
    """Return the single inline `<style>` block both templates inherit.

    Carries the AA-contrast body pair (ink on paper), the muted caption color,
    the semantic series colors, and an `@media print` block (print-safe).
    """
    p = PALETTE
    return f"""<style>
:root {{
  --good: {p['good']};
  --watch: {p['watch']};
  --concern: {p['concern']};
  --ink: {p['ink']};
  --paper: {p['paper']};
  --muted: {p['muted']};
}}
html, body {{
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.5;
}}
.wrap {{ max-width: 820px; margin: 0 auto; padding: 24px; }}
.tldr {{ border-left: 4px solid var(--good); padding: 8px 16px; margin: 16px 0; }}
.kpi {{ display: inline-block; margin: 8px 16px 8px 0; }}
.kpi .label {{ color: var(--muted); font-size: 13px; }}
.kpi .value {{ font-size: 28px; font-weight: 600; }}
.legend span {{ margin-right: 16px; font-size: 13px; }}
.swatch {{ display: inline-block; width: 12px; height: 12px; vertical-align: middle; margin-right: 4px; }}
.state-good {{ color: var(--good); }}
.state-watch {{ color: var(--watch); }}
.state-concern {{ color: var(--concern); }}
.state-neutral {{ color: var(--muted); }}
.chip {{ font-size: 13px; margin-left: 8px; }}
caption, .caption {{ color: var(--muted); font-size: 13px; }}
.zone {{ margin: 28px 0; }}
.zone h2 {{ font-size: 17px; margin: 0 0 8px; }}
.awaiting {{ color: var(--muted); border: 1px dashed var(--muted); border-radius: 6px; padding: 12px 16px; }}
.cards {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.card {{ border: 1px solid var(--muted); border-radius: 6px; min-width: 170px; padding: 12px; }}
.card .label {{ font-size: 13px; font-weight: 600; }}
.card .body {{ font-size: 13px; }}
.cal {{ display: flex; gap: 8px; }}
.cal .day {{ border: 1px solid var(--muted); border-radius: 6px; padding: 6px 10px; text-align: center; font-size: 13px; }}
.cal .today {{ border: 2px solid var(--ink); font-weight: 600; }}
.grid4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
.ring {{ display: inline-block; text-align: center; margin-right: 16px; }}
@media print {{
  html, body {{ background: #FFFFFF; color: #000000; }}
  .wrap {{ max-width: 100%; padding: 0; }}
  .tldr {{ border-left-color: #000000; }}
}}
</style>"""


def head(title):
    """Return the `<head>` block: charset, title, and the shared style block."""
    return (
        "<head><meta charset='utf-8'>"
        f"<title>{_escape(title)}</title>"
        f"{_style_block()}</head>"
    )


def tldr_banner(text):
    """Return the one-sentence TL;DR banner that opens every artifact."""
    return f"<div class='tldr'>{_escape(text)}</div>"


def legend():
    """Return the semantic-state legend (glyph + label per state, never color-only)."""
    items = []
    for state, glyph, word in (
        ("good", "&#9679;", "in range"),
        ("watch", "&#9650;", "monitor"),
        ("concern", "&#9632;", "out of range"),
    ):
        items.append(
            f"<span class='state-{state}'>"
            f"<span class='swatch' style='background:var(--{state})'></span>"
            f"{glyph} {word}</span>"
        )
    return f"<div class='legend'>{''.join(items)}</div>"


def kpi(label, value):
    """Return a single KPI card: a label over its latest value."""
    return (
        f"<div class='kpi'><div class='label'>{_escape(str(label))}</div>"
        f"<div class='value'>{_escape(str(value))}</div></div>"
    )


def zone(title, body_html, accent=None):
    """Return a dashboard zone section: a titled `<section>` wrapping its body.

    An accent, when given, chromes the section (left border + header underline
    in the accent color) — chrome only, never data state (ADR-0009 D3).

    Args:
        title (str): The zone heading text (escaped).
        body_html (str): The assembled zone body markup, included verbatim.
        accent (str, optional): An ACCENTS hex for the zone chrome.

    Returns:
        (str) The assembled `<section class='zone'>` markup.
    """
    section_style = f" style='border-left: 4px solid {accent}; padding-left: 12px'" if accent else ""
    h2_style = f" style='border-bottom: 2px solid {accent}'" if accent else ""
    return (
        f"<section class='zone'{section_style}>"
        f"<h2{h2_style}>{_escape(str(title))}</h2>{body_html}</section>"
    )


def awaiting(what_is_missing):
    """Return the honest awaiting-state card naming WHAT data is missing.

    The mechanical form of ADR-0009 D2: a muted dashed box carrying the
    missing-data text verbatim-escaped. Callers keep the text digit-free
    (ADR-0009 D2); the zone tests enforce it.

    Args:
        what_is_missing (str): The missing-data text (escaped).

    Returns:
        (str) The assembled `.awaiting` card markup.
    """
    return f"<div class='awaiting'>&#8212; {_escape(str(what_is_missing))}</div>"


def ring_scaffold(label):
    """Return a hero awaiting-state ring: an unfilled outline circle + label.

    Used ONLY by the hero zone's awaiting state — stroke muted, no fill, no
    percentage text, so the scaffold carries no implied score (ADR-0009 D2).

    Args:
        label (str): The ring's caption text (escaped).

    Returns:
        (str) The assembled `.ring` markup (inline SVG + caption).
    """
    return (
        "<div class='ring'>"
        "<svg width='72' height='72' role='img' aria-label='awaiting data'>"
        f"<circle cx='36' cy='36' r='30' fill='none' stroke='{PALETTE['muted']}' stroke-width='4'/>"
        "</svg>"
        f"<div class='caption'>{_escape(str(label))}</div></div>"
    )


# The empty-series stub both sparkline components return: same envelope, no data.
_EMPTY_SERIES_SVG = "<svg width='180' height='40' role='img' aria-label='no data'></svg>"


def _series_color(state):
    """Resolve a semantic state to its series color (fail-loud).

    "neutral" is the ONE approved non-SERIES state (no judgment, rendered
    muted); any other unknown state token KeyErrors rather than silently
    rendering muted — matching the render_views `_STATE_DISPLAY` contract.
    """
    return PALETTE["muted"] if state == "neutral" else PALETTE[state]


def _series_scale(values):
    """Return the (lo, span) normalization for a numeric series (span never 0)."""
    lo, hi = min(values), max(values)
    return lo, (hi - lo) or 1


def sparkline(values, state):
    """Return an inline-SVG sparkline polyline for a series, colored by state.

    Args:
        values (list): The numeric series to plot.
        state (str): The semantic state — a SERIES color or "neutral" (muted);
            any other token KeyErrors.
    """
    color = _series_color(state)
    if not values:
        return _EMPTY_SERIES_SVG
    lo, span = _series_scale(values)
    n = len(values)
    step = 180 / max(n - 1, 1)
    pts = " ".join(
        f"{i * step:.1f},{38 - (v - lo) / span * 36:.1f}" for i, v in enumerate(values)
    )
    return (
        "<svg width='180' height='40' role='img' "
        f"aria-label='{_escape(state)} sparkline'>"
        f"<polyline fill='none' stroke='{color}' stroke-width='2' points='{pts}'/>"
        "</svg>"
    )


def bar_sparkline(values, state):
    """Return an inline-SVG bar sparkline for a series, colored by state.

    Bottom-aligned `<rect>` columns in the same 180x40 envelope as `sparkline`:
    n bars filling the 180px width with a 2px gap, heights scaled from the
    series min..max to 4..36px (min 4px so every bar is visible; a constant
    series renders equal-height bars). The dashboard's bars-not-paths component
    (ADR-0008 D2); the polyline `sparkline` remains for the matrix/projection
    views' ADR-0007 contract.

    Args:
        values (list): The numeric series to plot.
        state (str): The semantic state — a SERIES color or "neutral" (muted);
            any other token KeyErrors.
    """
    color = _series_color(state)
    if not values:
        return _EMPTY_SERIES_SVG
    lo, span = _series_scale(values)
    n = len(values)
    width = (180 - 2 * (n - 1)) / n
    bars = "".join(
        f"<rect x='{i * (width + 2):.1f}' y='{40 - h:.1f}' "
        f"width='{width:.1f}' height='{h:.1f}' fill='{color}'/>"
        for i, h in ((i, 4 + (v - lo) / span * 32) for i, v in enumerate(values))
    )
    return (
        "<svg width='180' height='40' role='img' "
        f"aria-label='{_escape(state)} bar sparkline'>{bars}</svg>"
    )


def _escape(text):
    """Minimal HTML-escape for interpolated text/attribute content."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("'", "&#39;")
    )
