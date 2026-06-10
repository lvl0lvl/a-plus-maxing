"""Report template — the physician-ready, longer-form clinician-facing artifact.

Assembles the same shared `component_set` components into the report layout: a
TL;DR, a legend, and a per-item section carrying the latest value, a sparkline,
and the readings as a comparison table. All markup and colors come from
`component_set` — no per-template color literals — so the palette stays single-
sourced and the `@media print` block is inherited. A template is a callable
`template(store_read) -> html_str`.
"""

from vault.design.templates import component_set as cs


def _readings_by_item(store_read):
    """Group the store read model's readings into per-item reading lists."""
    by_item = {}
    for reading in store_read:
        by_item.setdefault(reading["item"], []).append(reading)
    return by_item


def _table(readings):
    """Return a comparison table (timepoint, source, value) for one item's readings."""
    rows = "".join(
        "<tr>"
        f"<td>{cs._escape(r['timepoint'])}</td>"
        f"<td>{cs._escape(r['source'])}</td>"
        f"<td>{cs._escape(str(r['value']))}</td>"
        "</tr>"
        for r in readings
    )
    return (
        "<table><caption class='caption'>readings</caption>"
        "<thead><tr><th>timepoint</th><th>source</th><th>value</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def render(store_read):
    """Assemble the physician-ready report HTML from the shared component set.

    Args:
        store_read (list): The store read model passed through by render.emit.

    Returns:
        (str) The assembled report HTML (single document, inline styling).
    """
    by_item = _readings_by_item(store_read)
    sections = []
    for item in sorted(by_item):
        readings = by_item[item]
        values = [r["value"] for r in readings]
        state = cs.state_for(item, values[-1] if values else None)
        latest = values[-1] if values else "—"
        sections.append(
            "<section>"
            f"<h2>{cs._escape(item)}</h2>"
            f"{cs.kpi(item, latest)}"
            f"{cs.sparkline(values, state)}"
            f"{_table(readings)}"
            "</section>"
        )
    body = (
        "<div class='wrap'>"
        "<h1>Physician Report</h1>"
        f"{cs.tldr_banner('Per-item readings with trend and source, for clinician review.')}"
        f"{cs.legend()}"
        f"{''.join(sections)}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{cs.head('Physician Report')}<body>{body}</body></html>"
