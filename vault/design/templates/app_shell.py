"""Served SPA front-end (ADR-0029): the operator-approved prototype design (`app_view.html`)
rendered with the live ingestion load-state.

The design source of truth is `app_view.html` — the verbatim prototype port: inline lucide
SVG + an inlined image (render.emit-clean), honest empty-data, the wired chat composers, and
the demographic form that POSTs the four gate-bound capture tokens to `/upload`. `render`
reads that design and injects the ONE load-state-dependent surface — the Upload "Link your
documents" cards (`<!--DOC_CARDS-->`) — from the ingestion `status` (resolved by
`generate.run('app')` via `scripts.ingest.status`): an empty store shows honest "+ Link"
cards, a loaded stream shows the landed names/counts (names/counts only, never a raw reading
value or rsid). `_lucide.py` vendors the icons.
"""
import html as _html
import pathlib

from scripts.ingest import status as ingest_status

_VIEW = pathlib.Path(__file__).with_name("app_view.html")

# The four 'Link your documents' card icons (the prototype's inline SVG paths), keyed by
# document class — rendered into the load-state-aware cards that replace <!--DOC_CARDS-->.
_DOC_ICONS = {
    "wearable": '<path d="M3 12h4l2 6 4-14 2 8h6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "labs": '<path d="M6 2h7l5 5v15H6z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M13 2v5h5" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    "medical": '<rect x="5" y="3" width="14" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M9 8h6M9 12h6M9 16h4" stroke="currentColor" stroke-width="1.6"/>',
    "dna": '<path d="M8 3c0 5 8 6 8 9s-8 4-8 9M16 3c0 5-8 6-8 9s8 4 8 9" fill="none" stroke="currentColor" stroke-width="1.6"/>',
}

_LINK = "<span class='link'>+ Link</span>"
_LOADED = "<span style='color:var(--good);font-weight:600'>✓ loaded</span>"


def _esc(value):
    """HTML-escape a display string — a filename/source is never trusted raw into markup."""
    return _html.escape(str(value), quote=True)


def _doc_card(icon_key, title, sub, state_html):
    """One 'Link your documents' card (prototype `.doc` markup) for a document class."""
    return (f"<div class='doc'><svg class='ic' viewBox='0 0 24 24'>{_DOC_ICONS[icon_key]}</svg>"
            f"<div class='m'><div class='t'>{title}</div><div class='d'>{sub}</div></div>"
            f"<div class='st'>{state_html}</div></div>")


def _doc_cards(status):
    """The four document cards, driven by the live ingestion load-state (names/counts only).

    An unloaded class shows the honest "+ Link" affordance; a loaded class flips to a
    "✓ loaded" state naming the landed file(s) `_esc`-escaped — never a raw reading value.
    """
    we = status["wearable"]
    if we.get("loaded"):
        sub = (f"{_esc(we['source'])} · {we['count']} readings · {_esc(', '.join(we['items']))} · "
               f"{_esc(we['range'][0])} – {_esc(we['range'][1])}")
        wearable = _doc_card("wearable", "Wearable export (Apple Health)", sub, _LOADED)
    else:
        wearable = _doc_card("wearable", "Wearable export (Apple Health)", "Apple Health export.xml", _LINK)

    labs = status["labs"]
    if labs.get("loaded"):
        labs_card = _doc_card("labs", "Labs &amp; bloodwork", _esc(", ".join(labs["files"])), _LOADED)
    else:
        labs_card = _doc_card("labs", "Labs &amp; bloodwork", "PDF or CSV", _LINK)

    medical = _doc_card("medical", "Medical history", "PDF, document, or paste", _LINK)

    dna = status["dna"]
    if dna.get("loaded"):
        dna_card = _doc_card("dna", "DNA (23andMe)", f"{_esc(dna['files'][0])} landed", _LOADED)
    else:
        dna_card = _doc_card("dna", "DNA (23andMe)", "23andMe raw .zip", _LINK)

    return f"{wearable}{labs_card}{medical}{dna_card}"


def _default_status(store_read):
    """Standalone-render status: wearable from store_read; DNA/labs unknown without their roots."""
    return {"wearable": ingest_status.wearable_status(store_read),
            "dna": {"loaded": False, "files": []},
            "labs": {"loaded": False, "files": []}}


def render(store_read=None, *, status=None, _today=None):
    """Return the inline-asset SPA shell HTML with the Upload doc-cards at the live load-state.

    The design is `app_view.html` (passes render.emit's off-file guard); the only injected
    surface is the four 'Link your documents' cards (`<!--DOC_CARDS-->`), rendered from
    `status`. No fabricated data — an empty store shows honest "+ Link" cards.

    Args:
        store_read (list, optional): The store read model; drives the wearable card's
            load-state when `status` is not injected. None renders the empty state.
        status (dict, optional): The full ingestion load-state (wearable/dna/labs), injected
            by `generate.run('app')`. None falls back to a store-only default.
        _today (date, optional): Accepted for render-engine seam parity; unused here.

    Returns:
        (str) The full self-contained SPA HTML document.
    """
    if store_read is None:
        store_read = []
    status = status if status is not None else _default_status(store_read)
    return _VIEW.read_text(encoding="utf-8").replace("<!--DOC_CARDS-->", _doc_cards(status))
