"""Dashboard template — the at-a-glance value-over-time view.

Assembles the shared `component_set` components (header, TL;DR, legend, KPI cards,
inline-SVG sparklines) into the dashboard layout. All markup and colors come from
`component_set` — no per-template color literals — so the palette stays single-
sourced and the `@media print` block is inherited. A template is a callable
`template(store_read) -> html_str`; `render.emit` inlines + size-checks + asset-
checks the returned markup.
"""

from vault.design.templates import component_set as cs


def _series_by_item(store_read):
    """Group the store read model's readings into per-item value series.

    Args:
        store_read (list): The store read model (list of reading dicts).

    Returns:
        (dict) item -> list of values, in store-read (timepoint) order.
    """
    series = {}
    for reading in store_read:
        series.setdefault(reading["item"], []).append(reading["value"])
    return series


def _state_for(item, values):
    """Pick the semantic series state for an item's series (palette membership)."""
    # Cycle through the semantic series so a dashboard exercises all three colors;
    # deterministic on item name so two generations are structurally identical.
    return cs.SERIES[hash_index(item)]


def hash_index(item):
    """Map an item name to a stable SERIES index (deterministic, data-independent)."""
    return sum(ord(c) for c in item) % len(cs.SERIES)


def render(store_read):
    """Assemble the dashboard HTML from the shared component set.

    Args:
        store_read (list): The store read model passed through by render.emit.

    Returns:
        (str) The assembled dashboard HTML (single document, inline styling).
    """
    series = _series_by_item(store_read)
    cards = []
    for item in sorted(series):
        values = series[item]
        state = _state_for(item, values)
        latest = values[-1] if values else "—"
        cards.append(
            "<div class='kpi-row'>"
            f"{cs.kpi(item, latest)}"
            f"{cs.sparkline(values, state)}"
            "</div>"
        )
    body = (
        "<div class='wrap'>"
        "<h1>Health Dashboard</h1>"
        f"{cs.tldr_banner('At-a-glance value-over-time across tracked items.')}"
        f"{cs.legend()}"
        f"{''.join(cards)}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{cs.head('Health Dashboard')}<body>{body}</body></html>"
