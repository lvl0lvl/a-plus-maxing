"""V1 generation engine — renders a template against the store read model.

`emit(template, store_read)` assembles a named template against the store read
model, inlines everything into ONE self-contained local HTML file (inline CSS,
inline SVG — 0 external asset references), and RETURNS the path it wrote. The
destination is engine-owned: callers pass no output path. The render path is a
data-out PII boundary — it reads operator data ONLY from the `store_read`
argument (sourced from `store.read` / `keying.py`), opens no network, and
fetches no remote data or asset. Before writing, it scans every asset reference
the assembled output carries; if any would resolve to an external URL (a
non-`data:`, non-fragment `src=`/`href=`/`url(`), it RAISES and writes no file.

Published surface (ADR-0004-T1; consumed by ADR-0004-T2/T3, ADR-0006-T2,
ADR-0007-T2): `emit(template, store_read) -> Path`.
"""

import re
from pathlib import Path

DEFAULT_OUT_DIR = Path("vault/artifacts/generated")

# A src=/href=/url() whose target is neither a data: URI nor a same-document
# #fragment resolves off the file — an external asset reference. Inline assets
# (data:/#frag) are allowed; anything else (http(s)://, //cdn, bare path) is not.
_REF_RE = re.compile(
    r"""(?:src|href)\s*=\s*['"]([^'"]*)['"]|url\(\s*['"]?([^'")]*)['"]?\s*\)""",
    re.IGNORECASE,
)


def _external_references(html):
    """Return every asset reference in `html` that resolves off the file.

    A reference is off-file unless it is a `data:` URI or a same-document
    `#fragment`. Empty targets are ignored.

    Args:
        html (str): The assembled markup to scan.

    Returns:
        (list) The off-file reference targets (empty when fully inlined).
    """
    refs = []
    for match in _REF_RE.finditer(html):
        target = (match.group(1) or match.group(2) or "").strip()
        if not target or target.startswith("data:") or target.startswith("#"):
            continue
        refs.append(target)
    return refs


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
    path.write_text(html)
    return path
