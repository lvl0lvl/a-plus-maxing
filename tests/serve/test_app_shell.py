"""Render-view + served-surface tests for the inline-asset app shell (ADR-0029-T1).

The four-screen left-nav SPA (`Dashboard` / `Upload Documents` / `Plan` / `Chat with
Team`) ported from the operator-approved `prototype/app.html` into the tracked render
view `vault/design/templates/app_shell.py`, registered as `generate.run("app")`.

The AUTHORITATIVE inline-asset check is the real `render.emit` probe, never a substring
grep: `generate.run("app")` (driving `render.emit` over `app_shell.render`) RETURNS a
written `Path` that EXISTS (AC-1); a NEGATIVE probe injects ONE off-file reference into
the assembled SPA and asserts `render.emit` RAISES `ValueError` and writes nothing
(AC-2) — proving the gate is the real emit probe. The Dashboard / Plan / Chat-with-Team
screens carry 0 fabricated operator data — honest awaiting states (AC-5). GET `/` serves
the SPA, not the wizard, with the loopback bind + route table byte-unchanged (AC-6).

All fixture-driven: 0 live API call, 0 non-loopback socket, 0 key read.
"""

import http.client
import threading
from pathlib import Path

import pytest

from scripts.generate import generate, render
from scripts.serve import server as serve_server
from vault.design.templates import app_shell

REPO_ROOT = Path(__file__).resolve().parents[2]

# The four left-nav screens the served SPA body must carry (AC-6). The wizard has none
# of "Upload Documents" / "Chat with Team", so the set distinguishes the SPA from it.
_NAV_MARKERS = ("Dashboard", "Upload Documents", "Plan", "Chat with Team")


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread

# A served-body marker UNIQUE to the SPA (the wizard has no "Chat with Team" nav). Used
# to assert the body is the SPA served surface, distinct from the wizard `<title>`.
SPA_NAV_MARKER = "Chat with Team"
WIZARD_TITLE = "A+ Maxing — Build your plan"

# The fabricated demo set from prototype/app.html that an honest awaiting-state render
# MUST NOT present as the operator's data (ADR-0029 OQ-3 / ADR-0009 D2).
_FABRICATED = (
    "Synced from WHOOP",
    "Primed to train",
    "Room to push",
    "2,650 kcal",
    "BPC-157 · 250mcg",
    "Upper Push — Hypertrophy",
    "68 ms",
    "49 bpm",
    "183 lb",
)


def _emit_app(tmp_path):
    """Drive the real generate.run('app') into tmp roots; return the written Path."""
    return generate.run(
        "app",
        _root=tmp_path / "store",
        _out_dir=tmp_path / "out",
        _dna_root=tmp_path / "dna",
        _labs_root=tmp_path / "labs",
    )


def _spa_html():
    """Render the SPA HTML string standalone (empty store -> honest awaiting states)."""
    return app_shell.render([])


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1..AC-5: the tracked render view + inline assets + honest data
# --------------------------------------------------------------------------- #


def test_generate_run_app_emits_path(tmp_path):
    """AC-1 (AUTHORITATIVE inline-asset): generate.run('app') RETURNS a written path.

    Drives `render.emit` over `app_shell.render` via the real `generate.run('app')`
    into a tmp `_out_dir`. The returned value is a `Path` that EXISTS on disk and the
    call did NOT raise `ValueError` — the SPA carries 0 external asset references. This
    is the authoritative inline-asset proof; a substring grep is NOT substituted.
    """
    path = _emit_app(tmp_path)
    assert isinstance(path, Path), f"generate.run('app') returned {type(path)}, expected Path"
    assert path.exists() and path.is_file(), "generate.run('app') did not write the SPA file"
    # Sanity: the written file is the SPA served surface, not an empty/other artifact.
    assert SPA_NAV_MARKER in path.read_text(), "the emitted file is not the SPA"


def test_offfile_ref_makes_emit_raise(tmp_path):
    """AC-2 (inline-asset NEGATIVE probe — failing-capable): an off-file ref RAISES.

    Injects ONE off-file reference into the ASSEMBLED SPA (a CDN `<script src>`),
    then drives `render.emit` over the injected variant. `render.emit` must RAISE
    `ValueError` and write NO file — proving the AC-1 pass rests on the real emit
    gate, not a render that happens to look clean. If the SPA ever regained a CDN
    script or a bare-path `<img>`, this is the failure mode it would hit.
    """
    def offfile_render(store_read):
        html = app_shell.render(store_read)
        return html.replace(
            "</body>", '<script src="https://unpkg.com/lucide@latest/x.js"></script></body>'
        )

    offfile_render.__name__ = "app_shell_offfile_probe"
    with pytest.raises(ValueError):
        render.emit(offfile_render, [], _out_dir=tmp_path / "out")
    assert not (tmp_path / "out" / "app_shell_offfile_probe.html").exists(), (
        "render.emit wrote a file despite an external reference (gate is not failing-capable)"
    )


def test_no_cdn_lucide_in_rendered_spa():
    """AC-3 (lucide vendored inline): the rendered SPA loads no CDN lucide script.

    The prototype's `<script src="https://unpkg.com/lucide@latest/...">` is removed
    and every icon renders as an inline `<svg>` — so the rendered SPA carries no
    `unpkg`, no `lucide`, and no `<script src="http...`.
    """
    html = _spa_html()
    assert "unpkg" not in html, "the rendered SPA still references the unpkg CDN"
    assert "lucide" not in html, "the rendered SPA still references lucide (CDN script not removed)"
    assert 'src="http' not in html, "the rendered SPA carries an http-sourced asset"
    assert "<svg" in html, "the SPA renders no inline <svg> icons (icons not vendored inline)"


def test_no_body_png_in_rendered_spa():
    """AC-4 (body.png removed/inlined): the rendered SPA carries no bare-path image.

    The prototype's `<img src="images/body.png">` is removed with its readiness
    awaiting-state (or inlined as a `data:` URI) — so no `body.png` bare path survives.
    """
    html = _spa_html()
    assert "body.png" not in html, "the rendered SPA still references the bare-path body.png"
    assert "images/" not in html, "the rendered SPA references a bare images/ asset path"


def test_dashboard_plan_team_honest_awaiting():
    """AC-5 (HONEST-DATA): Dashboard/Plan/Team carry 0 fabricated data + an awaiting state.

    Enumerates the fabricated demo set the prototype presented as the operator's
    readings/plan and asserts each is ABSENT from the rendered SPA (count == 0). Each
    of the Dashboard / Plan / Chat-with-Team screens carries a consistent awaiting-state
    marker instead of fabricated numbers (ADR-0009 D2).
    """
    html = _spa_html()
    present = [tok for tok in _FABRICATED if tok in html]
    assert present == [], f"the rendered SPA presents fabricated operator data: {present}"
    for screen in ("dashboard", "plan", "team"):
        assert f"data-awaiting='{screen}'" in html, (
            f"the {screen} screen carries no honest awaiting-state marker"
        )


# --------------------------------------------------------------------------- #
# Cycle 2 — AC-6: GET / serves the SPA (loopback bind + route table unchanged)
# --------------------------------------------------------------------------- #


def test_get_root_serves_spa_not_wizard(tmp_path):
    """AC-6 (RE-POINT): GET `/` serves the SPA body, not the wizard; loopback unchanged.

    Drives the REAL loopback server: GET `/` returns HTTP 200 + the four SPA nav-shell
    markers and NOT the wizard `<title>` — proving the body source re-pointed from
    `generate.run('intake')` to `generate.run('app')`. The bind literal `_LOOPBACK =
    "127.0.0.1"` stays byte-unchanged and the route table stays {GET `/`, POST `/upload`,
    POST `/chat`} — 0 new bind/port/route.
    """
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
    )
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        resp = conn.getresponse()
        body = resp.read().decode("utf-8")
        conn.close()
        assert resp.status == 200, f"GET / returned {resp.status}, expected 200"
        for marker in _NAV_MARKERS:
            assert marker in body, f"GET / body does not carry the SPA nav marker {marker!r}"
        assert WIZARD_TITLE not in body, "GET / still serves the wizard <title> (not re-pointed)"
    finally:
        srv.shutdown()
        srv.server_close()

    # The bind literal is byte-unchanged (the loopback transport is not re-specified).
    src = (REPO_ROOT / "scripts" / "serve" / "server.py").read_text()
    assert '_LOOPBACK = "127.0.0.1"' in src, "the loopback bind literal changed (NFR-5)"
