"""V1 generation engine — renders a template against the store read model.

`emit(template, store_read)` assembles a named template against the store read
model, inlines everything into ONE self-contained local HTML file (inline CSS,
inline SVG — 0 external asset references), and RETURNS the path it wrote. The
destination is engine-owned: callers pass no output path. The render path is a
data-out PII boundary — it reads operator data ONLY from the `store_read`
argument (sourced from `store.read` / `keying.py`), opens no network, and
fetches no remote data or asset. Before writing, it scans the asset references
the assembled output carries at their syntactic positions (asset-bearing HTML
attributes + CSS `url()`/`@import` inside `<style>` blocks); if any would resolve
to an external URL (a non-`data:`, non-fragment target), it RAISES and writes no
file. Escaped operator text carrying the same substring never trips the scan.

Published surface (ADR-0004-T1; consumed by ADR-0004-T2/T3, ADR-0006-T2,
ADR-0007-T2): `emit(template, store_read) -> Path`.
"""

import re
from html.parser import HTMLParser
from pathlib import Path

from vault.design.templates import component_set as cs

DEFAULT_OUT_DIR = Path("vault/artifacts/generated")

# ADR-0004-T0 render-size cap (max series-per-view AND max timepoints-per-view),
# re-validated against the real component_set.py render in
# vault/decisions/2026-06-06-adr-0004-t0-cap-revalidation.md (worst-case 16x12 =
# 34117 bytes, cap UNCHANGED). The spike report is gitignored, so the cap value is
# carried here by the pipeline. A change to either number is under Architect
# change-control (the spike's own constraint).
MAX_SERIES_PER_VIEW = 16
MAX_TIMEPOINTS_PER_VIEW = 12

# Attributes that name an asset the browser fetches. Scanned at their syntactic
# position (a real HTML attribute), so escaped operator TEXT carrying the same
# substring never trips. srcset/image-set carry comma-separated candidate lists.
_ASSET_ATTRS = frozenset({"src", "href", "poster"})
_SRCSET_ATTRS = frozenset({"srcset"})

# CSS asset references, matched only inside <style> blocks (never over text
# content): url(...), @import "...", and image-set(...) candidate lists.
_CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]*)['\"]?\s*\)", re.IGNORECASE)
_CSS_IMPORT_RE = re.compile(r"@import\s+['\"]([^'\"]+)['\"]", re.IGNORECASE)


def _is_external(target):
    """True if an asset target resolves off the file (not a data: URI or #fragment).

    Empty targets are ignored. Everything else — http(s)://, protocol-relative
    `//cdn`, or a bare path — resolves off the single self-contained file.
    """
    target = target.strip()
    return bool(target) and not target.startswith(("data:", "#"))


def _srcset_targets(value):
    """Yield each candidate URL from a srcset / image-set comma-separated list."""
    for candidate in value.split(","):
        url = candidate.strip().split()[0] if candidate.strip() else ""
        if url:
            yield url


class _AssetScanner(HTMLParser):
    """Collect off-file asset references from asset-bearing attributes + <style> CSS.

    References are read at their syntactic positions only — real HTML attributes
    and CSS `url()`/`@import` inside `<style>` blocks — so escaped operator text
    containing the same substrings never registers as an asset reference.

    Attributes:
        refs (list): The off-file reference targets discovered so far.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        attrs = {k: (v or "") for k, v in attrs}
        if tag == "style":
            self._in_style = True
        for name, value in attrs.items():
            if name in _ASSET_ATTRS and _is_external(value):
                self.refs.append(value.strip())
            elif name in _SRCSET_ATTRS:
                self.refs.extend(t for t in _srcset_targets(value) if _is_external(t))
        # <meta http-equiv=refresh content="0;url=https://...">
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            url = re.search(r"url\s*=\s*(\S+)", attrs.get("content", ""), re.IGNORECASE)
            if url and _is_external(url.group(1)):
                self.refs.append(url.group(1).strip())

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if not self._in_style:
            return
        for match in _CSS_URL_RE.finditer(data):
            if _is_external(match.group(1)):
                self.refs.append(match.group(1).strip())
        for match in _CSS_IMPORT_RE.finditer(data):
            if _is_external(match.group(1)):
                self.refs.append(match.group(1).strip())


def _external_references(html):
    """Return every off-file asset reference in `html`, by syntactic position.

    Scans asset-bearing HTML attributes (src/href/poster/srcset, meta-refresh)
    and CSS `url()`/`@import` inside `<style>` blocks. A reference is off-file
    unless it is a `data:` URI or a same-document `#fragment`; escaped operator
    text carrying the same substring is not an asset reference and never trips.

    Args:
        html (str): The assembled markup to scan.

    Returns:
        (list) The off-file reference targets (empty when fully inlined).
    """
    scanner = _AssetScanner()
    scanner.feed(html)
    scanner.close()
    return scanner.refs


def _assemble(template, store_read):
    """Resolve a template to its assembled HTML against the store read model.

    A template is either a module exposing `render(store_read)` (the dashboard /
    report templates) or a plain callable `template(store_read) -> str`.
    """
    renderer = getattr(template, "render", template)
    return renderer(store_read)


def _name_for(template):
    """Derive a stable, filesystem-safe basename for the template's output file."""
    name = getattr(template, "__name__", None) or template.__class__.__name__
    return name.rsplit(".", 1)[-1]


def emit(template, store_read, *, _out_dir=None):
    """Render `template` against `store_read` into one self-contained HTML file.

    Reads operator data only from `store_read`; opens no network and discovers no
    file independently. Inlines everything (inline CSS + inline SVG, 0 external
    asset references). Before writing, raises if any assembled asset reference
    would resolve to an external URL — refusing to emit a network-dependent file.

    Args:
        template: A template module exposing `render(store_read)`, or a callable
            `template(store_read) -> str` returning the assembled HTML.
        store_read (list): The store read model (the data `store.read` returns).
        _out_dir (Path, optional): Test-only output-dir seam. Not part of the
            published `emit(template, store_read)` interface; defaults to the
            engine-owned `vault/artifacts/generated/`.

    Returns:
        (Path) The path of the single HTML file written.

    Raises:
        ValueError: An assembled asset reference resolves to an external URL
            (the file is not written).
    """
    html = _assemble(template, store_read)

    refs = _external_references(html)
    if refs:
        raise ValueError(
            f"refusing to emit a network-dependent file: external asset reference(s) {refs}"
        )

    out_dir = Path(_out_dir) if _out_dir is not None else DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{_name_for(template)}.html"
    path.write_text(html, encoding="utf-8")
    return path


def _series_in_order(store_read):
    """Group the store read model into per-item value series, in first-seen order.

    Returns:
        (list) (item, values) pairs; `values` are the readings in store-read order.
    """
    series = {}
    for reading in store_read:
        series.setdefault(reading["item"], []).append(reading["value"])
    return list(series.items())


def _matrix_projection_html(page_series, page_no):
    """Assemble one matrix+projection page from per-item series, page_no in the title.

    Draws ALL chart-component markup from the shared `component_set` (head/style,
    legend, KPI cards, inline-SVG sparklines) — the shared-defs block is emitted
    ONCE via `cs.head`, then REFERENCED per series (one matrix sparkline + one
    projection sparkline per series), never re-emitted per series. A projection
    sparkline extends each series by its last value (a placeholder local recompute);
    everything is inlined (0 external references).

    Args:
        page_series (list): (item, values) pairs for the series on this page.
        page_no (int): The 1-based page index (distinguishes split pages).

    Returns:
        (str) The assembled single-document HTML for this page.
    """
    rows = []
    for item, values in page_series:
        state = cs.state_for(item)
        latest = values[-1] if values else "—"
        projection = values + [values[-1]] if values else values
        rows.append(
            "<div class='kpi-row'>"
            f"{cs.kpi(item, latest)}"
            f"{cs.sparkline(values, state)}"
            f"{cs.sparkline(projection, state)}"
            "</div>"
        )
    body = (
        "<div class='wrap'>"
        f"<h1>Biomarker Matrix &amp; Projection (page {page_no})</h1>"
        f"{cs.tldr_banner('Biomarker matrix with per-series projection.')}"
        f"{cs.legend()}"
        f"{''.join(rows)}"
        "</div>"
    )
    return f"<!doctype html><html lang='en'>{cs.head('Biomarker Matrix')}<body>{body}</body></html>"


def _page_slices(store_read):
    """Split a store read into per-page (item, values) groups within the cap.

    A page carries at most MAX_SERIES_PER_VIEW series AND at most
    MAX_TIMEPOINTS_PER_VIEW timepoints per series; a series with more timepoints is
    split across pages too, so every page stays within both cap bounds. A cap-or-
    below dataset yields exactly one page.

    Returns:
        (list) Pages, each a list of (item, values) pairs within both cap bounds.
    """
    series = _series_in_order(store_read)
    pages = []
    for s_start in range(0, max(len(series), 1), MAX_SERIES_PER_VIEW):
        series_page = series[s_start:s_start + MAX_SERIES_PER_VIEW]
        max_tp = max((len(v) for _, v in series_page), default=0)
        for t_start in range(0, max(max_tp, 1), MAX_TIMEPOINTS_PER_VIEW):
            pages.append([
                (item, values[t_start:t_start + MAX_TIMEPOINTS_PER_VIEW])
                for item, values in series_page
            ])
    return pages


def emit_matrix_projection(store_read, *, _out_dir=None):
    """Render the biomarker matrix + projection from `store_read`, capped per view.

    The caller-side render path above the single-file `emit` primitive: it slices an
    over-cap dataset into per-page slices (each within the ADR-0004-T0 cap of
    MAX_SERIES_PER_VIEW series AND MAX_TIMEPOINTS_PER_VIEW timepoints), calls the
    published `emit(template, store_read) -> Path` ONCE per slice (each page template
    carries a distinct name so `_name_for` derives a distinct basename), and returns
    the list of written paths. A cap-or-below dataset yields exactly one path; an
    over-cap dataset paginates to >=2 paths. Each page routes through the SAME `emit`
    inline + external-asset + size discipline, so each is self-contained and within
    the budget. Reads operator data only from `store_read`; makes no model step.

    Args:
        store_read (list): The store read model (the data `store.read` returns).
        _out_dir (Path, optional): Test-only output-dir seam (same as `emit`).

    Returns:
        (list) The Path of each page written (length 1 at/below cap, >=2 over-cap).
    """
    paths = []
    for page_no, page_series in enumerate(_page_slices(store_read), start=1):
        def page_template(_store_read, _page_series=page_series, _page_no=page_no):
            return _matrix_projection_html(_page_series, _page_no)

        page_template.__name__ = f"matrix_projection_page_{page_no}"
        paths.append(emit(page_template, store_read, _out_dir=_out_dir))
    return paths
