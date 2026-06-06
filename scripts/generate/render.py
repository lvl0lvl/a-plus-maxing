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

DEFAULT_OUT_DIR = Path("vault/artifacts/generated")

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
