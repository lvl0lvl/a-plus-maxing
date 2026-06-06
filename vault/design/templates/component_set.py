"""Shared inline-CSS/SVG component library for generated HTML artifacts.

Single definition of the reusable rendered components (header, TL;DR banner,
KPI section, inline-SVG sparkline) and the colorblind-safe semantic palette
(good / watch / concern) that both the dashboard and report templates draw from.
All styling is inline — inline `<style>`, inline SVG — with no external asset
references, per the artifact-design-protocol single-file rule.

The palette hex set, the foreground/background contrast pairs, and the
`@media print` block are the source the accessibility gate (ADR-0004-T1 crit 3)
measures against. The hex values, the CIEDE2000 deltaE floor, the named
deuteranopia/protanopia simulation, and the metric are recorded independently in
`vault/decisions/2026-06-05-render-colorblind-safe-palette.md`; this module's
palette MUST match that recorded decision (the gate reads its expected values
from the decision, not from here).
"""

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


def state_for(item):
    """Pick the semantic series state for an item by name (single source of truth).

    Cycles through SERIES so a multi-item artifact exercises all three colors;
    deterministic on the item name so two generations are structurally identical.
    Shared by both the dashboard and report templates.

    Args:
        item (str): The tracked-item name.

    Returns:
        (str) One of SERIES (good / watch / concern).
    """
    return SERIES[sum(ord(c) for c in item) % len(SERIES)]


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
caption, .caption {{ color: var(--muted); font-size: 13px; }}
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


def sparkline(values, state):
    """Return an inline-SVG sparkline polyline for a series, colored by state.

    Args:
        values (list): The numeric series to plot.
        state (str): One of SERIES — selects the semantic color.
    """
    color = PALETTE[state]
    if not values:
        return f"<svg width='180' height='40' role='img' aria-label='no data'></svg>"
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
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


def _escape(text):
    """Minimal HTML-escape for interpolated text/attribute content."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("'", "&#39;")
    )
