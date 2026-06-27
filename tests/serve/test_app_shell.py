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

# The left-nav screens the served SPA body must carry (AC-6). The wizard has none of
# "Chat with Team" / "Profile", so the set distinguishes the SPA from it. (Upload Documents
# was merged into the Chat-with-Team workspace, so it is no longer a separate nav item.)
_NAV_MARKERS = ("Dashboard", "Plan", "Chat with Team", "Profile")


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
    """AC-3 (lucide vendored inline): the rendered SPA loads no CDN/off-file lucide script.

    The prototype's `<script src="https://unpkg.com/lucide@latest/...">` is gone and the
    icons are vendored inline (the inlined icon table swapped to inline `<svg>` by the
    bundled `createIcons`) — so the SPA carries no `unpkg`/CDN reference, no http-sourced
    asset, and no external `<script src>`; render.emit (AC-1) is the off-file guard. The
    bare string "lucide" legitimately survives as the local `data-lucide` attribute /
    vendor-JS name — a local label, NOT an off-file reference.
    """
    html = _spa_html()
    assert "unpkg" not in html, "the rendered SPA still references the unpkg CDN"
    assert 'src="http' not in html, "the rendered SPA carries an http-sourced asset"
    assert "<script src" not in html, "the rendered SPA loads an external script (lucide not vendored inline)"
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


# --------------------------------------------------------------------------- #
# ADR-0029-T3 — wire the Upload Documents surface: demographic form -> /upload,
# chat composer -> /chat, honest ingestion-state. Fixture-driven, 0 live spend.
# --------------------------------------------------------------------------- #
import functools
import re

from scripts.plan.router import summarize
from scripts.serve import capture
from scripts.store import store

# An identity config ABSENT on disk (the fresh-clone posture): value-class PII patterns
# still run, operator-identity detection is empty. Mirrors test_intake_demographics.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"

# The four demographic capture field names the activated Upload form must POST.
_DEMOGRAPHIC_NAMES = ("date-of-birth", "sex-for-dosing", "bodyweight-band", "equipment-access-class")

# The bodyweight kg gate token -> its pinned pounds-range DISPLAY label. The POSTed value is
# the kg band token (so persist_capture validates); the operator reads pounds. 6-band 1:1 map.
_BODYWEIGHT_LB_LABELS = {
    "under-60kg": "Under 132 lb", "60-70kg": "132–154 lb", "70-80kg": "154–176 lb",
    "80-90kg": "176–198 lb", "90-100kg": "198–220 lb", "over-100kg": "Over 220 lb",
}

# Rich-section field names that MUST NOT appear in the objective-only Upload form — they are
# the chat-only surface (gathered at POST /chat), never form fields (the ADR-0018 split).
_RICH_SECTION_NAMES = (
    "goal-domains", "goal-targets", "goal-priority-order", "hard-limits",
    "recovery-status-band", "train-around", "dietary-pattern", "meals-per-day",
    "allergies", "food-preferences", "supplement-stack", "peptide-stack",
    "rx-interaction-classes", "nutrition-detail", "training-detail",
)

# The fabricated ingestion counts the prototype presented as the operator's data — an honest
# empty-store render carries NONE of these (ADR-0009 D2 honest-data).
_FABRICATED_INGEST = ("12,480 readings", "✓ ingested", "2 of 4 categories", "parsing labs")


def _upload_form_html(html):
    """Extract the POSTing `<form ... action='/upload' ...>...</form>` from the rendered SPA."""
    m = re.search(r"<form[^>]*action='/upload'[^>]*>(.*?)</form>", html, re.DOTALL)
    assert m is not None, "the SPA has no POSTing capture form (action='/upload')"
    return m.group(0)


def _form_field_names(form_html):
    """Every `name='...'` attribute the form submits (input/select/textarea)."""
    return set(re.findall(r"name='([^']+)'", form_html))


def _select_block(html, name):
    """The `<select name='<name>'>...</select>` inner block from the rendered SPA."""
    m = re.search(rf"<select[^>]*name='{re.escape(name)}'[^>]*>(.*?)</select>", html, re.DOTALL)
    assert m is not None, f"the {name!r} demographic select is not rendered"
    return m.group(1)


# --- Cycle 1: demographic form -> /upload + markup<->gate enum + round-trip --- #


def test_upload_form_posts_the_four_demographic_names_to_upload():
    """AC-1: the Upload 'About you' form POSTs exactly the four demographic name= to /upload."""
    form = _upload_form_html(_spa_html())
    assert "method='post'" in form, "the capture form is not a POST"
    names = _form_field_names(form)
    missing = [n for n in _DEMOGRAPHIC_NAMES if n not in names]
    assert not missing, f"the upload form does not POST these demographic inputs: {missing}"


def test_demographic_selects_built_from_the_gate_constants():
    """AC-2: each demographic <select>'s option values EQUAL the gate enum constant (no-drift)."""
    html = _spa_html()
    for name, constant in (
        ("sex-for-dosing", capture.SEX_OPTIONS),
        ("bodyweight-band", capture.BODYWEIGHT_BANDS),
        ("equipment-access-class", capture.EQUIPMENT_ACCESS_CLASSES),
    ):
        values = set(re.findall(r"<option value='([^']*)'", _select_block(html, name)))
        values.discard("")
        assert values == set(constant), (
            f"the {name!r} options {sorted(values)} drifted from the gate constant {sorted(constant)}"
        )


def test_bodyweight_band_six_options_with_pinned_pounds_labels():
    """AC-2: bodyweight-band has 6 kg-token options (not 7) with the pinned pounds labels."""
    block = _select_block(_spa_html(), "bodyweight-band")
    pairs = re.findall(r"<option value='([^']*)'>([^<]*)</option>", block)
    real = [(v, t) for v, t in pairs if v != ""]
    assert len(real) == 6, f"bodyweight-band has {len(real)} real options, expected 6 (not the prototype's 7)"
    labels = dict(real)
    for token, label in _BODYWEIGHT_LB_LABELS.items():
        assert labels.get(token) == label, (
            f"bodyweight option {token!r} label is {labels.get(token)!r}, expected the pinned {label!r}"
        )


def test_demographic_fields_round_trip_through_the_built_capture_seam(tmp_path):
    """AC-3: the four form name=/value pairs round-trip through the unchanged persist_capture."""
    html = _spa_html()

    def first_opt(name):
        vals = [v for v in re.findall(r"<option value='([^']*)'", _select_block(html, name)) if v]
        return vals[0]

    # The values the rendered form would POST: a birth year + a real option per demographic select.
    fields = {
        "date-of-birth": "1986",
        "sex-for-dosing": first_opt("sex-for-dosing"),
        "bodyweight-band": first_opt("bodyweight-band"),
        "equipment-access-class": first_opt("equipment-access-class"),
    }
    store_root = tmp_path / "store"
    capture.persist_capture(
        fields, root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    summary = summarize(functools.partial(store.read, root=store_root), identity_config=_ABSENT_IDENTITY)
    expected = {
        "training-age-band": "born-1980s",  # DERIVED from the date-of-birth raw source
        "sex-for-dosing": fields["sex-for-dosing"],
        "bodyweight-band": fields["bodyweight-band"],
        "equipment-access-class": fields["equipment-access-class"],
    }
    orphaned = [t for t in expected if summary.get(t) != expected[t]]
    assert not orphaned, f"these demographic tokens stayed orphaned on the SPA surface: {orphaned}"


def test_upload_form_is_objective_only_zero_rich_section_fields():
    """AC-6 (form-leg): the Upload form's name set is EXACTLY the four demographics, 0 rich-section."""
    names = _form_field_names(_upload_form_html(_spa_html()))
    leaked = [n for n in _RICH_SECTION_NAMES if n in names]
    assert not leaked, f"the objective-only form carries rich-section fields: {leaked}"
    assert names == set(_DEMOGRAPHIC_NAMES), (
        f"the upload form's data fields are not exactly the demographic set: {sorted(names)}"
    )


# --- Cycle 2: chat composer -> /chat fetch + receipt render + single-egress surface --- #


def test_chat_composer_fetches_chat_renders_reply_and_intake_progress():
    """AC-4: the chat composer POSTs to /chat, mounts the reply, AND surfaces intake progress.

    The operator-approved SPA uses ONE event-delegated composer across the dashboard,
    Upload, and Team chats (vs the merged build's single `#chat-turns`): it POSTs
    `{turn, conversation}` to the ADR-0016 one-turn /chat lane, appends the assistant
    `reply` to the thread, and degrades to an "unavailable" fallback when the backend
    errors — never a fabricated reply. It also consumes the receipt's de-identified
    `progress` (`intake_complete` / `target_domain`) into a `.chat-progress` indicator so
    the operator sees what's left and when they can generate a plan. Failing-capable: reds
    if the composer stops fetching /chat, carrying the turn, consuming the reply, or
    reading the intake-progress signal.
    """
    html = _spa_html()
    assert "fetch('/chat'" in html, "the chat composer JS does not fetch the /chat route"
    assert "turn:txt" in html, "the /chat POST body does not carry the typed turn"
    assert "d.reply" in html, "the chat JS does not consume the assistant reply"
    assert "chat-thread" in html, "no thread container the assistant reply mounts into"
    assert "unavailable" in html, "the chat JS has no degraded/unavailable fallback"
    assert "intake_complete" in html, "the chat JS does not read the intake-complete progress signal"
    assert "chat-progress" in html, "the chat has no intake-progress indicator element"


def test_spa_fetch_targets_are_all_same_origin_loopback():
    """AC-6 (fetch-leg): every fetch target is a same-origin loopback path (0 non-loopback class)."""
    html = _spa_html()
    targets = re.findall(r"fetch\(\s*['\"]([^'\"]+)['\"]", html)
    assert targets, "the SPA makes no fetch call (the chat composer is not wired)"
    for t in targets:
        assert t.startswith("/") and not t.startswith("//") and "://" not in t, (
            f"fetch target {t!r} is not a same-origin loopback path (a new outbound class)"
        )
    # /settings/key is a LOCAL loopback route (Profile API-key save): a same-origin POST
    # whose key is written to the on-device keychain — it never leaves the machine, so it
    # adds NO new egress class. /confirm-extraction (ADR-0030-T4) is likewise a LOCAL
    # same-origin POST: the operator-confirmed extracted-readings subset lands through the
    # unchanged on-device store sink — it never leaves the machine. The off-machine egress
    # set is still the ADR-0016 /chat one-turn alone (the per-target loopback assertion above
    # is the egress guard, byte-unchanged; the enumerated set grows by the one authorized route).
    assert set(targets) <= {"/chat", "/upload", "/settings/key", "/confirm-extraction"}, (
        f"the SPA fetches a path beyond the known loopback routes "
        f"(/chat + /upload + /settings/key + /confirm-extraction): {sorted(set(targets))}"
    )


# --- Cycle 3: honest ingestion-state + INLINE-ASSET guard under T3's additions --- #


def test_upload_ingestion_state_is_honest_on_empty_store(tmp_path):
    """AC-5: the Upload ingestion-state renders the real load-state — 0 fabricated counts on empty."""
    html = _emit_app(tmp_path).read_text()
    present = [tok for tok in _FABRICATED_INGEST if tok in html]
    assert present == [], f"the Upload ingestion-state presents fabricated counts: {present}"
    # The document cards render the real empty-store load-state: not-linked '+ Link' affordances.
    assert "+ Link" in html, "the empty-store ingestion-state shows no not-linked document card"


def test_doc_cards_render_loaded_labs_card_with_escaped_filename():
    """TEST-1: a labs-LOADED status renders the loaded labs card naming the escaped file(s).

    The labs-loaded branch of `_doc_cards` (`status["labs"]["loaded"]` true) flips the labs
    card to the '✓ loaded' state and shows the landed filenames `_esc`-escaped — mirrors the
    dna-loaded render assertion in `test_server.py` (the wearable + dna loaded branches are
    covered there; the labs-loaded branch had none). Seeds a labs status whose filename
    carries an HTML-special char and asserts the rendered shell carries the loaded marker,
    the ESCAPED filename, and the second file. Failing-capable: reds if the loaded branch
    stops naming the file or drops the escaping (an unescaped `<panel>` would leak).
    """
    status = {
        "wearable": {"loaded": False},
        "dna": {"loaded": False, "files": []},
        "labs": {"loaded": True, "files": ["cmp_<panel>.pdf", "lipids.csv"]},
    }
    html = app_shell.render([], status=status)
    assert "✓ loaded" in html, "the labs-loaded card shows no loaded marker"
    assert "cmp_&lt;panel&gt;.pdf" in html, "the loaded labs card does not name the escaped filename"
    assert "lipids.csv" in html, "the loaded labs card does not name the second landed file"
    assert "cmp_<panel>.pdf" not in html, "the loaded labs card leaked the unescaped filename"


def test_t3_additions_keep_the_spa_inline_asset_clean(tmp_path):
    """INLINE-ASSET guard (re-run under T3): generate.run('app') still emits a Path, no off-file ref."""
    path = _emit_app(tmp_path)  # render.emit RAISES ValueError on any off-file asset reference
    assert isinstance(path, Path) and path.exists(), "generate.run('app') did not emit under T3 additions"
    assert "<script src" not in path.read_text(), "T3 added an off-file <script src> reference"


# --------------------------------------------------------------------------- #
# ADR-0030-T4 — the SPA operator-confirm UI on Upload Documents: render the
# extracted readings for review/confirm with an HONEST empty state; the confirm
# action POSTs only the confirmed subset to /confirm-extraction. Fixture-driven,
# 0 live spend (the rendered-SPA string + the real generate.run('app') emit).
# --------------------------------------------------------------------------- #


def _panel_build_html(html):
    """The inner content of the locked ws-docs `#panel-build` Upload surface the panel lands in."""
    m = re.search(
        r'<div class="ws-panel active ws-docs" id="panel-build">(.*?)'
        r'<div class="ws-panel" id="panel-generate">',
        html, re.DOTALL,
    )
    assert m is not None, "the ws-docs #panel-build Upload surface is not in the rendered SPA"
    return m.group(1)


def _reading_row_template(html):
    """The per-reading confirm/reject control template the inline JS instantiates per reading."""
    m = re.search(r'<template[^>]*id="reading-row-tpl"[^>]*>(.*?)</template>', html, re.DOTALL)
    assert m is not None, "the per-reading confirm/reject control template is not rendered"
    return m.group(1)


# Sample-reading tokens (the prototype's fabricated demo readings) that an honest empty
# confirm-review panel MUST NOT bake into the HTML as the operator's data (ADR-0009 D2).
_FABRICATED_READING = (
    "BPC-157 · 250mcg", "183 lb", "49 bpm", "68 ms", "Upper Push — Hypertrophy",
)


# --- Cycle 1: the confirm-review panel + per-reading controls + honest empty state --- #


def test_confirm_review_panel_and_per_reading_control_present():
    """AC-1: the Upload surface carries a confirm-review panel + a per-reading confirm/reject control.

    The confirm-review panel (container + review-list mount + confirm action) lands inside
    the locked ws-docs `#panel-build` Upload surface, and a per-reading control template
    renders each extracted reading's (item, timepoint, source, value) with a confirm AND a
    reject affordance. Failing-capable: reds if the panel or any of the four reading slots /
    the confirm / the reject affordance is absent.
    """
    html = _spa_html()
    block = _panel_build_html(html)
    assert 'id="review-panel"' in block, "no confirm-review panel in the #panel-build (ws-docs) surface"
    assert 'id="review-list"' in block, "no review-list container the per-reading rows mount into"
    assert 'id="confirm-readings"' in block, "no confirm action on the review panel"
    tpl = _reading_row_template(html)
    for field in ("item", "timepoint", "source", "value"):
        assert f'data-field="{field}"' in tpl, f"the per-reading control renders no {field} slot"
    assert "reading-confirm" in tpl, "the per-reading control has no confirm affordance"
    assert "reading-reject" in tpl, "the per-reading control has no reject affordance"


def test_confirm_review_panel_is_honest_empty_by_default():
    """AC-3 (HONEST-DATA): the confirm-review panel's default state bakes 0 fabricated reading.

    A default render (no extraction has run client-side) presents NO placeholder
    (item, timepoint, source, value) row as the operator's data: the review-list is empty,
    no fabricated sample-reading token appears, and the panel carries the locked awaiting-state
    marker. Failing-capable: reds if any sample reading is baked into the panel as data or the
    awaiting marker is dropped.
    """
    block = _panel_build_html(_spa_html())
    present = [tok for tok in (_FABRICATED + _FABRICATED_READING) if tok in block]
    assert present == [], f"the confirm-review panel presents fabricated readings: {present}"
    assert "data-awaiting='extraction'" in block, "the panel carries no honest awaiting-state marker"
    assert '<div id="review-list"></div>' in block, "the review-list is not empty by default (a reading is baked in)"


def test_confirm_panel_keeps_spa_inline_asset_clean(tmp_path):
    """AC-5 (AUTHORITATIVE inline-asset): generate.run('app') emits a Path with the panel, no off-file ref.

    Drives the REAL `generate.run('app')` (render.emit RAISES ValueError on any off-file asset
    reference) and asserts it returns a written Path that EXISTS and carries the confirm-review
    panel, with no off-file `<script src>`. Couples the panel's presence to the emit gate — a
    substring grep is NOT substituted for the emit probe.
    """
    path = _emit_app(tmp_path)
    assert isinstance(path, Path) and path.exists(), "generate.run('app') did not emit with the confirm panel"
    emitted = path.read_text()
    assert 'id="review-panel"' in emitted, "the emitted SPA carries no confirm-review panel"
    assert "<script src" not in emitted, "the confirm panel added an off-file <script src> reference"


# --- Cycle 2: the /upload -> /confirm-extraction inline JS (only the confirmed subset) --- #


def test_upload_extraction_payload_drives_confirm_extraction_post():
    """AC-2: the inline JS carries a fetch('/upload') -> fetch('/confirm-extraction') flow.

    The upload POST surfaces T3's extracted-readings review payload, then the confirm action
    POSTs to `/confirm-extraction` — sending the CSRF-gate `application/json` Content-Type the
    route requires and the aligned `{readings: ...}` body (the SAME key `/upload`'s review
    payload returns, re-posted verbatim). Failing-capable: reds if the confirm flow is absent
    or drops the application/json header / the aligned readings key.
    """
    html = _spa_html()
    assert "fetch('/upload'" in html, "the upload flow no longer fetches /upload"
    assert "fetch('/confirm-extraction'" in html, "the inline JS has no /confirm-extraction confirm flow"
    i = html.find("fetch('/confirm-extraction'")
    window = html[i:i + 220]
    assert "'Content-Type':'application/json'" in window, "the confirm POST omits the application/json CSRF header"
    assert "JSON.stringify({readings:" in window, "the confirm POST does not send the aligned {readings:...} body"


def test_confirm_posts_only_the_confirmed_subset():
    """AC-4: the confirm handler collects only the checked/confirmed rows; a rejected reading is omitted.

    The confirm collector reads each per-reading row's confirm control (`.reading-confirm`) and
    filters by its `.checked` state into a `picked` subset, then POSTs `{readings:picked}` — so an
    unchecked/rejected reading is excluded from the body, not the full extracted set. Failing-
    capable: reds if the collector stops filtering by the confirm control or posts the full set.
    """
    html = _spa_html()
    i = html.find("fetch('/confirm-extraction'")
    assert i != -1, "no /confirm-extraction flow to check the subset collection"
    collector = html[max(0, i - 600):i + 60]
    assert "reading-confirm" in collector, "the confirm collector does not read the per-reading confirm control"
    assert ".checked" in collector, "the confirm collector does not filter by the confirm control's checked state"
    assert "JSON.stringify({readings:picked})" in html, "the confirm POST sends a set other than the confirmed subset"
