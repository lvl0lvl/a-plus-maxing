"""Served SPA front-end (ADR-0029): the operator-approved prototype ported verbatim —
inline assets (lucide vendored as SVG, image inlined as a data: URI; render.emit-clean),
honest empty-data on every data slot, and the chat composers wired to the live /chat route.
The design source of truth is `app_view.html` (the ported prototype); `_lucide.py` vendors the icons."""
import pathlib

_VIEW = pathlib.Path(__file__).with_name("app_view.html")


def render(store_read=None, *, status=None, _today=None):
    """Return the self-contained inline-asset SPA shell HTML (passes render.emit's off-file guard)."""
    return _VIEW.read_text(encoding="utf-8")
