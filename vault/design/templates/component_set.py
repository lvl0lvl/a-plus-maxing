"""Shared inline-CSS/SVG component library for generated HTML artifacts.

Single definition of the reusable rendered components (header, TL;DR banner,
KPI section, inline-SVG sparklines — polyline and bar; the ADR-0009 dashboard
zone primitives — zone, awaiting, progress_ring, pill, chip_b, stat_box,
track_bar), the colorblind-safe semantic palette (good / watch / concern) that
both the dashboard and report templates draw from, the surface-category
ACCENTS chrome set (ADR-0009 D3), and the neutral CHROME app-surface tokens
(`vault/design/dashboard-v1-visual-spec.md`). All styling is inline — inline
`<style>`, inline SVG — with no external asset references, per the
artifact-design-protocol single-file rule.

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

# Neutral app-surface chrome (`vault/design/dashboard-v1-visual-spec.md`) —
# chrome, NOT data state: the gray page frame, card/sheet borders, and the
# ~10% tint backgrounds the pills / stat boxes / calendar use. Tints are fixed
# hex literals (no runtime color math); each comment names the base color the
# tint is ~10% of.
CHROME = {
    "page-bg": "#F3F4F6",          # the gray page behind the white sheet
    "card-border": "#E5E7EB",      # card/sheet/track borders + ring track
    "good-tint": "#E7F1EB",        # PALETTE good #117733
    "concern-tint": "#F3E9EE",     # PALETTE concern #882255
    "neutral-tint": "#EEEEEE",     # PALETTE muted #555555
    "training-tint": "#EAF1FD",    # ACCENTS training #1F6FEB
    "nutrition-tint": "#FDF3EB",   # ACCENTS nutrition #E8833A
    "supplements-tint": "#E7F5F6", # ACCENTS supplements #0E9AA3
    "peptides-tint": "#F2EBFD",    # ACCENTS peptides #7C3AED
    "sleep-tint": "#EFEFFB",       # ACCENTS sleep #5B5BD6
    "today-tint": "#EFF4FE",       # calendar today column (light training-blue tint)
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
    the semantic series colors, the app-surface frame (gray page, white sheet,
    card system, grids, pills, stat boxes, tracks — the visual-spec chrome),
    and an `@media print` block (print-safe: white page, ink text, plain 1px
    borders, shadows off, grids flatten).
    """
    p = PALETTE
    c = CHROME
    a = ACCENTS
    return f"""<style>
:root {{
  --good: {p['good']};
  --watch: {p['watch']};
  --concern: {p['concern']};
  --ink: {p['ink']};
  --paper: {p['paper']};
  --muted: {p['muted']};
  --page-bg: {c['page-bg']};
  --card-border: {c['card-border']};
}}
html, body {{
  margin: 0;
  background: var(--page-bg);
  color: var(--ink);
  font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.5;
}}
.wrap {{ max-width: 1140px; margin: 24px auto; padding: 28px; background: var(--paper); border: 1px solid var(--card-border); border-radius: 12px; }}
.topbar {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; border-bottom: 1px solid var(--card-border); padding-bottom: 14px; }}
.topbar .product {{ font-size: 17px; font-weight: 700; }}
.topbar .date {{ color: var(--muted); font-size: 13px; }}
.tldr {{ border-left: 4px solid var(--good); padding: 8px 16px; margin: 16px 0; }}
.kpi {{ display: inline-block; margin: 8px 16px 8px 0; }}
.kpi .label {{ color: var(--muted); font-size: 13px; }}
.kpi .value {{ font-size: 28px; font-weight: 700; }}
.legend span {{ margin-right: 16px; font-size: 13px; }}
.swatch {{ display: inline-block; width: 12px; height: 12px; vertical-align: middle; margin-right: 4px; }}
.state-good {{ color: var(--good); }}
.state-watch {{ color: var(--watch); }}
.state-concern {{ color: var(--concern); }}
.state-neutral {{ color: var(--muted); }}
.chip {{ font-size: 13px; margin-left: 8px; }}
caption, .caption {{ color: var(--muted); font-size: 13px; }}
.zone {{ margin: 30px 0; }}
.zone h2 {{ font-size: 16px; margin: 0 0 2px; }}
.subtitle {{ color: var(--muted); font-size: 13px; margin: 0 0 10px; }}
.awaiting {{ color: var(--muted); border: 1px dashed var(--muted); border-radius: 6px; padding: 12px 16px; }}
.cards {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.card {{ background: var(--paper); border: 1px solid var(--card-border); border-radius: 10px; padding: 14px; box-shadow: 0 1px 2px rgba(0,0,0,.05); }}
.card .label {{ font-size: 13px; font-weight: 600; }}
.card .body {{ font-size: 13px; }}
.grid2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }}
.grid4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}
.grid6 {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; }}
.grid6 .kpi-row {{ border: 1px solid var(--card-border); border-radius: 10px; padding: 14px; box-shadow: 0 1px 2px rgba(0,0,0,.05); }}
.grid6 .kpi {{ display: block; margin: 0; }}
.grid6 .kpi .label {{ font-size: 11px; }}
.grid6 .kpi .value {{ font-size: 21px; }}
.grid6 svg {{ width: 100%; height: 40px; display: block; margin-top: 8px; }}
.cal {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; }}
.cal .day {{ border: 1px solid var(--card-border); border-radius: 8px; padding: 6px 8px; font-size: 12px; }}
.cal .dhead {{ text-align: center; }}
.cal .dslot {{ min-height: 70px; }}
.cal .today {{ background: {c['today-tint']}; font-weight: 600; }}
.calhead {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }}
.calhead .card-title {{ font-size: 14px; font-weight: 600; }}
.pill {{ display: inline-block; border-radius: 999px; font-size: 12px; padding: 2px 10px; background: {c['neutral-tint']}; color: var(--muted); }}
.tint-good {{ background: {c['good-tint']}; color: var(--good); }}
.tint-concern {{ background: {c['concern-tint']}; color: var(--concern); }}
.tint-neutral {{ background: {c['neutral-tint']}; color: var(--muted); }}
.tint-training {{ background: {c['training-tint']}; color: {a['training']}; }}
.tint-nutrition {{ background: {c['nutrition-tint']}; color: {a['nutrition']}; }}
.tint-supplements {{ background: {c['supplements-tint']}; color: {a['supplements']}; }}
.tint-peptides {{ background: {c['peptides-tint']}; color: {a['peptides']}; }}
.tint-sleep {{ background: {c['sleep-tint']}; color: {a['sleep']}; }}
.chip-b {{ display: inline-block; border-radius: 999px; font-size: 12px; padding: 2px 10px; border: 1px solid var(--card-border); color: var(--ink); }}
.stat {{ border: 1px solid var(--card-border); border-radius: 8px; text-align: center; padding: 8px 4px; }}
.stat .slabel {{ font-size: 11px; color: var(--muted); }}
.stat .sval {{ font-size: 16px; font-weight: 600; }}
.stat.tinted {{ background: var(--page-bg); }}
.pc-training .stat.tinted {{ background: {c['training-tint']}; }}
.pc-nutrition .stat.tinted {{ background: {c['nutrition-tint']}; }}
.statrow {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 10px 0; }}
.track {{ height: 8px; border-radius: 999px; background: var(--card-border); }}
.fill {{ height: 8px; border-radius: 999px; }}
.macro {{ margin: 8px 0; }}
.goal-row {{ margin: 0 0 10px; }}
.hero {{ display: flex; gap: 28px; align-items: center; flex-wrap: wrap; }}
.hero .headline {{ font-size: 16px; font-weight: 700; }}
.hero .chips {{ margin-top: 10px; }}
.hero .chips .chip-b {{ margin-right: 8px; }}
.ring {{ display: inline-block; text-align: center; margin-right: 16px; }}
.dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--muted); vertical-align: middle; margin-right: 6px; }}
.pchead {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
.pchead .ptitle {{ font-size: 14px; font-weight: 600; }}
.pchead .pill {{ margin-left: auto; }}
.pending {{ margin-bottom: 8px; }}
.pending .chip-b {{ margin-right: 8px; }}
@media print {{
  html, body {{ background: #FFFFFF; color: #000000; }}
  .wrap {{ max-width: 100%; padding: 0; border: none; border-radius: 0; }}
  .card, .grid6 .kpi-row, .stat {{ box-shadow: none; }}
  .cal .today {{ background: #FFFFFF; }}
  .tldr {{ border-left-color: #000000; }}
  .grid6 {{ grid-template-columns: repeat(3, 1fr); }}
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


def zone(title, body_html, subtitle=None):
    """Return a dashboard zone section: a titled `<section>` wrapping its body.

    Zones separate by whitespace, never rules/borders (visual spec); a
    subtitle, when given, renders as the muted one-line caption under the
    heading.

    Args:
        title (str): The zone heading text (escaped).
        body_html (str): The assembled zone body markup, included verbatim.
        subtitle (str, optional): The muted one-line caption under the heading.

    Returns:
        (str) The assembled `<section class='zone'>` markup.
    """
    sub = f"<div class='subtitle'>{_escape(str(subtitle))}</div>" if subtitle else ""
    return (
        "<section class='zone'>"
        f"<h2>{_escape(str(title))}</h2>{sub}{body_html}</section>"
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


def progress_ring(label, value=None, color=None):
    """Return a hero progress ring: a light full-circle track + optional value arc.

    The honest state (value None) renders the track only — no colored arc, an
    em-dash centered where the value would be, label beneath (ADR-0009 D2). A
    real value renders the colored arc with rounded caps and the value centered
    — the arc is chrome around a value, never a data-state semantic (D3).

    Args:
        label (str): The ring's caption text (escaped).
        value (int | float, optional): The 0-100 score; None -> awaiting state.
        color (str, optional): The arc stroke hex; unused while value is None.

    Returns:
        (str) The assembled `.ring` markup (inline SVG + caption).
    """
    circumference = 263.9  # 2 * pi * r, r = 42
    arc = ""
    if value is not None:
        arc = (
            f"<circle cx='48' cy='48' r='42' fill='none' stroke='{color}' "
            "stroke-width='9' stroke-linecap='round' "
            f"stroke-dasharray='{value / 100 * circumference:.1f} {circumference}' "
            "transform='rotate(-90 48 48)'/>"
        )
    shown = "—" if value is None else str(value)
    fill = PALETTE["muted"] if value is None else PALETTE["ink"]
    aria = "awaiting data" if value is None else str(value)
    return (
        "<div class='ring'>"
        f"<svg width='96' height='96' role='img' aria-label='{_escape(aria)}'>"
        f"<circle cx='48' cy='48' r='42' fill='none' stroke='{CHROME['card-border']}' stroke-width='9'/>"
        f"{arc}"
        "<text x='48' y='56' text-anchor='middle' font-size='24' "
        f"font-weight='700' fill='{fill}'>{_escape(shown)}</text>"
        "</svg>"
        f"<div class='caption'>{_escape(str(label))}</div></div>"
    )


def pill(text, tint_state=None):
    """Return a tinted pill: ~10% tint background, base-color 12px text.

    `tint_state` names a CHROME tint (good / concern / neutral, or an ACCENTS
    category); None renders the muted default. An unknown tint name KeyErrors
    rather than silently rendering unstyled — matching `_series_color`.

    Args:
        text (str): The pill text (escaped).
        tint_state (str, optional): The CHROME tint name (without `-tint`).

    Returns:
        (str) The assembled `.pill` markup.
    """
    if tint_state is None:
        return f"<span class='pill'>{_escape(str(text))}</span>"
    if f"{tint_state}-tint" not in CHROME:
        raise KeyError(tint_state)
    return f"<span class='pill tint-{tint_state}'>{_escape(str(text))}</span>"


def chip_b(text):
    """Return a bordered chip: 1px neutral border, ink 12px text.

    The pills/chips component's second flavor (visual spec) — metric chips,
    pending items, legend entries, inert controls.

    Args:
        text (str): The chip text (escaped).
    """
    return f"<span class='chip-b'>{_escape(str(text))}</span>"


def stat_box(label, value="—", tinted=False):
    """Return a bordered stat box: centered 11px label over its 16px value.

    The em-dash default is the honest empty slot (ADR-0009 D2). tinted=True
    adds the highlight class; the enclosing card's CSS picks the tint color.

    Args:
        label (str): The box label (escaped).
        value (str, optional): The box value (escaped); defaults to an em-dash.
        tinted (bool, optional): Highlight the box with the context tint.
    """
    klass = "stat tinted" if tinted else "stat"
    return (
        f"<div class='{klass}'><div class='slabel'>{_escape(str(label))}</div>"
        f"<div class='sval'>{_escape(str(value))}</div></div>"
    )


def track_bar(fill_pct=None, color=None):
    """Return a thin progress track; the honest state (fill_pct None) has no fill.

    Args:
        fill_pct (int | float, optional): The 0-100 fill width; None -> empty
            track (ADR-0009 D2 — never an invented fill).
        color (str, optional): The fill hex; unused while fill_pct is None.
    """
    if fill_pct is None:
        return "<div class='track'></div>"
    return (
        "<div class='track'>"
        f"<div class='fill' style='width:{fill_pct}%;background:{color}'></div>"
        "</div>"
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
