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

# The four demographic capture field names the amended `#panel-build` "Your details" form
# POSTs (ADR-0034: the born-year text -> a full-date `date-of-birth`, the `bodyweight-band`
# select -> a `bodyweight-kg` NUMBER input; `bodyweight-band` is RETIRED from the markup).
_DEMOGRAPHIC_NAMES = ("date-of-birth", "sex-for-dosing", "bodyweight-kg", "equipment-access-class")

# The four pinned rich-domain free-text field names the comprehensive ADR-0034 wizard carries
# (the `_CHAT_RAW_SOURCE_FIELDS` keys) and the objective-only `#panel-build` form does NOT.
_WIZARD_RICH_FIELDS = ("nutrition-detail", "supplement-stack", "peptide-stack", "training-detail")

# Rich-section field names that MUST NOT appear in the objective-only `#panel-build` form —
# the comprehensive intake routes them through the wizard, never this demographic sub-form.
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
    """AC-2: each demographic <select>'s option values EQUAL the gate enum constant (no-drift).

    The `bodyweight-band` leg is RETIRED — ADR-0034 replaces the band <select> with a
    `bodyweight-kg` number input (no `<option>`s). Only `sex-for-dosing` /
    `equipment-access-class` stay bounded selects checked against the gate constants.
    """
    html = _spa_html()
    for name, constant in (
        ("sex-for-dosing", capture.SEX_OPTIONS),
        ("equipment-access-class", capture.EQUIPMENT_ACCESS_CLASSES),
    ):
        values = set(re.findall(r"<option value='([^']*)'", _select_block(html, name)))
        values.discard("")
        assert values == set(constant), (
            f"the {name!r} options {sorted(values)} drifted from the gate constant {sorted(constant)}"
        )


def test_bodyweight_is_amended_number_input_with_unit_select():
    """AC-2 (amended weight): `#panel-build` carries a `bodyweight-kg` NUMBER input + a lbs/kg unit.

    ADR-0034 replaces the 6-option `bodyweight-band` <select> with a `bodyweight-kg` number
    input (logged over time, not a coarse band) beside a lbs/kg unit select. The retired
    `bodyweight-band` token is ABSENT from the rendered SPA (no silent stale option). Failing-
    capable: reds if the number input is missing or the `bodyweight-band` select survives.
    """
    html = _spa_html()
    assert re.search(r"<input[^>]*type='number'[^>]*name='bodyweight-kg'", html), (
        "the amended `#panel-build` form carries no `bodyweight-kg` number input"
    )
    assert "bodyweight-band" not in html, "the retired `bodyweight-band` band select still renders"
    # the unit select sits beside the number input, offering lbs + kg
    assert ">lbs</option>" in html and ">kg</option>" in html, "no lbs/kg unit select beside the weight"


def test_demographic_fields_round_trip_through_the_built_capture_seam(tmp_path):
    """AC-3: the W1-valid demographic legs round-trip through the unchanged persist_capture.

    Two legs, each W1-valid AND W2-invariant (no cross-wave coupling to T2's deriver/weight
    capture): (a) the full-date `date-of-birth` persists VERBATIM to the `date-of-birth` raw
    store item via the UNCHANGED `_DOB_FIELD` special-case (the raw write does not change when
    T2 repurposes the deriver to exact-age); (b) `sex-for-dosing` passes through to its own
    WIRED_TOKEN. The amended weight is a `bodyweight-kg` field whose CAPTURE routing is T2's W2
    work (record-only at W1, store empty), so a weight->store round-trip is DELIBERATELY absent
    here — the weight is covered by the AC-2 markup + AC-7 prefill cases, both bypassing capture.
    """
    html = _spa_html()

    def first_opt(name):
        vals = [v for v in re.findall(r"<option value='([^']*)'", _select_block(html, name)) if v]
        return vals[0]

    fields = {"date-of-birth": "1986-04-12", "sex-for-dosing": first_opt("sex-for-dosing")}
    store_root = tmp_path / "store"
    capture.persist_capture(
        fields, root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # (a) the full date round-trips VERBATIM to the named-excluded `date-of-birth` raw source.
    dob = store.read("date-of-birth", root=store_root)
    assert dob and dob[-1]["value"] == "1986-04-12", "the DOB full date did not round-trip to its raw store item"
    # (b) `sex-for-dosing` passes through to the summary token (a WIRED_TOKEN, stable across W2).
    summary = summarize(functools.partial(store.read, root=store_root), identity_config=_ABSENT_IDENTITY)
    assert summary.get("sex-for-dosing") == fields["sex-for-dosing"], "sex-for-dosing did not pass through"


def test_upload_form_is_objective_only_zero_rich_section_fields():
    """AC-6 (form-leg): the `#panel-build` "Your details" form's name set is EXACTLY the amended demographics.

    ADR-0034 SUPERSEDES the ADR-0018 "objective-only form vs chat-only rich fields" split: the
    comprehensive intake routes the rich-domain fields through the WIZARD (asserted positively in
    Case W6), so the assertion is SCOPED to the `#panel-build` demographic sub-form (the first
    `action='/upload'` form) — its data fields are EXACTLY the four amended demographics, with no
    rich-section field leaking onto this objective sub-form.
    """
    names = _form_field_names(_upload_form_html(_spa_html()))
    leaked = [n for n in _RICH_SECTION_NAMES if n in names]
    assert not leaked, f"the `#panel-build` demographic form carries rich-section fields: {leaked}"
    assert names == set(_DEMOGRAPHIC_NAMES), (
        f"the `#panel-build` form's data fields are not exactly the amended demographic set: {sorted(names)}"
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
    # unchanged on-device store sink — it never leaves the machine. /generate-plan is the
    # in-app plan-engine trigger: a same-origin POST that authors over the de-identified
    # summary through the no-train author (the SAME off-machine class as /chat, never a new
    # one) and records locally. The off-machine egress set is still the no-train author lane
    # (the per-target loopback assertion above is the egress guard, byte-unchanged; the
    # enumerated set grows by the one authorized in-app route).
    assert set(targets) <= {"/chat", "/upload", "/settings/key", "/confirm-extraction", "/generate-plan"}, (
        f"the SPA fetches a path beyond the known loopback routes "
        f"(/chat + /upload + /settings/key + /confirm-extraction + /generate-plan): {sorted(set(targets))}"
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
    """AC-1: the Upload surface carries a confirm-review panel + a per-reading confirm control.

    The confirm-review panel (container + review-list mount + confirm action) lands inside
    the locked ws-docs `#panel-build` Upload surface, and a per-reading control template
    renders each extracted reading's (item, timepoint, source, value) with a confirm affordance —
    the checkbox is the sole include/exclude control (uncheck = exclude, reversible; the per-row
    Reject button was removed per Tier-2 design review). The confirm checkbox carries an accessible
    name (WCAG 4.1.2). Failing-capable: reds if the panel, any of the four reading slots, the
    confirm affordance, or its accessible name is absent.
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
    # WCAG 4.1.2 Level A: the confirm checkbox must carry an accessible name (an empty <label>
    # wrap would announce "checkbox, checked" with no name to a screen reader).
    cb = re.search(r'<input[^>]*class="reading-confirm"[^>]*>', tpl)
    assert cb is not None, "the per-reading confirm checkbox is not rendered"
    assert "aria-label=" in cb.group(0), "the reading-confirm checkbox carries no accessible name (WCAG 4.1.2)"


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
    """AC-4: the confirm handler collects only the checked/confirmed rows; an unchecked reading is omitted.

    The confirm collector reads each per-reading row's confirm control (`.reading-confirm`) and
    filters by its `.checked` state into a `picked` subset, then POSTs `{readings:picked}` — so an
    unchecked reading is excluded from the body, not the full extracted set. Failing-capable: reds
    if the collector stops filtering by the confirm control or posts the full set.
    """
    html = _spa_html()
    i = html.find("fetch('/confirm-extraction'")
    assert i != -1, "no /confirm-extraction flow to check the subset collection"
    collector = html[max(0, i - 900):i + 60]
    assert "reading-confirm" in collector, "the confirm collector does not read the per-reading confirm control"
    assert ".checked" in collector, "the confirm collector does not filter by the confirm control's checked state"
    assert "JSON.stringify({readings:picked})" in html, "the confirm POST sends a set other than the confirmed subset"


def test_confirm_zero_selected_does_not_post_or_show_false_success():
    """HIGH (no false success): a 0-confirmed Confirm click does not POST and shows no landed-success.

    The confirm handler guards on the confirmed subset: when `picked` is empty it returns BEFORE
    the /confirm-extraction fetch (0 land) and shows an honest 'Nothing selected' message instead
    of a '✓ Landed' success. Failing-capable: reds if the guard is removed — a no-op would then
    POST `{readings:[]}` and the landed-success would render for a 0-land no-op.
    """
    html = _spa_html()
    fi = html.find("fetch('/confirm-extraction'")
    assert fi != -1, "no /confirm-extraction flow to guard"
    gi = html.find("if(!picked.length)")
    assert gi != -1, "the confirm handler has no 0-confirmed guard"
    assert gi < fi, "the 0-confirmed guard does not short-circuit before the POST"
    guard = html[gi:fi]
    assert "return" in guard, "the 0-confirmed guard does not return before the POST"
    assert "Nothing selected" in guard, "the 0-confirmed path shows no honest 'nothing selected' message"
    # the landed-success message lives ONLY after the fetch resolves — never on the 0-confirmed no-op path
    si = html.find("✓ Landed ")
    assert si > fi, "the landed-success message is not gated behind the confirm POST"


def test_confirm_success_gated_on_http_status_no_false_landed():
    """Tier-3 F2 (no false success / no data loss): '✓ Landed' + the panel-clear fire ONLY on a real land.

    The /confirm-extraction error bodies (400 degraded / 413 / 415) all carry `landed:[]`, so an
    unconditional `.then(r=>r.json()).then(d=>'✓ Landed '+(d.landed||[]).length)` would paint a green
    'Landed 0' success on an HTTP error AND clear the pending review (`showReview([])`) — a false
    success with silent data loss. The handler must read the response status (`res.ok`) and gate BOTH
    the landed-success message and the `showReview([])` clear behind it (mirroring the /settings/key +
    /chat handlers), with a failure branch that keeps the panel. Failing-capable: revert to the
    unconditional `.then(r=>r.json())` success and the `res.ok` gate disappears.
    """
    html = _spa_html()
    i = html.find("fetch('/confirm-extraction'")
    assert i != -1, "no /confirm-extraction flow to check status-gating"
    ok_i = html.find("res.ok", i)
    assert ok_i != -1, "the confirm handler does not gate success on the HTTP response status (res.ok)"
    landed_i = html.find("✓ Landed ", i)
    clear_i = html.find("showReview([])", i)
    assert landed_i != -1 and ok_i < landed_i, "the '✓ Landed' success is not gated behind the res.ok check"
    assert clear_i != -1 and ok_i < clear_i, "the showReview([]) panel-clear is not gated behind the res.ok check"
    assert "Could not land" in html[i:i + 1400], "the confirm handler has no failure branch that keeps the review panel"


# --------------------------------------------------------------------------- #
# ADR-0031-T5 — the SPA honest-partial note on the review panel: surface T4's
# {readings, partial, notes} /upload payload so a too-large/dense extraction shows
# an honest note instead of the silent "no new data" awaiting state (QA-1). The
# note lands in the EXISTING locked Clinical-Light review panel (no redesign, no
# new surface). Fixture-driven, 0 live spend (the rendered-SPA string + the real
# generate.run('app') emit).
# --------------------------------------------------------------------------- #


def _extraction_note_open_tag(block):
    """The opening <div ...> tag of the partial-extraction note element, or None."""
    return re.search(r'<div[^>]*id="extraction-note"[^>]*>', block)


# --- Cycle 1: the partial-note element + default honest-empty (inline-asset clean) --- #


def test_partial_note_keeps_spa_inline_asset_clean(tmp_path):
    """AC-4 (AUTHORITATIVE inline-asset): generate.run('app') emits a Path with the note, no off-file ref.

    Drives the REAL `generate.run('app')` (render.emit RAISES ValueError on any off-file asset
    reference) and asserts it returns a written Path that EXISTS and carries the partial-extraction
    note element, with no off-file `<script src>`. The note adds 0 off-file asset; a substring grep
    is NOT substituted for the emit probe. Failing-capable: reds if the note element is absent or it
    introduces an off-file `<script src>`.
    """
    path = _emit_app(tmp_path)
    assert isinstance(path, Path) and path.exists(), "generate.run('app') did not emit with the partial-note element"
    emitted = path.read_text()
    assert 'id="extraction-note"' in emitted, "the emitted SPA carries no partial-extraction note element"
    assert "<script src" not in emitted, "the partial note added an off-file <script src> reference"


def test_partial_note_element_default_hidden_and_honest_empty():
    """AC-1 (HONEST-EMPTY): the partial-note element is present, default-hidden, and bakes 0 note/fabricated data.

    The note element (`id="extraction-note"`) lands in the locked ws-docs `#panel-build` review-panel
    surface, is DEFAULT-HIDDEN (carries `display:none` — its text is injected client-side from T4's
    `notes`), and bakes NO note text / NO fabricated reading as the operator's data. The existing
    honest-empty invariants still hold (the awaiting marker + the exactly-empty review-list).
    Failing-capable: reds if the note element is absent, is not default-hidden, bakes note/fabricated
    text, or breaks the honest-empty invariants.
    """
    block = _panel_build_html(_spa_html())
    note = re.search(r'<div[^>]*id="extraction-note"[^>]*>(.*?)</div>', block, re.DOTALL)
    assert note is not None, "no partial-extraction note element in the #panel-build (ws-docs) review-panel surface"
    open_tag = _extraction_note_open_tag(block)
    assert open_tag is not None and "display:none" in open_tag.group(0), "the partial-note element is not default-hidden"
    assert note.group(1).strip() == "", "the partial-note element bakes note text into the default render (not honest-empty)"
    present = [tok for tok in (_FABRICATED + _FABRICATED_READING) if tok in note.group(0)]
    assert present == [], f"the partial-note element bakes fabricated tokens: {present}"
    # the existing honest-empty invariants are preserved (the note is a default-hidden SIBLING)
    assert "data-awaiting='extraction'" in block, "the panel's honest awaiting-state marker was dropped"
    assert '<div id="review-list"></div>' in block, "the review-list is no longer empty by default (the note broke it)"


# --- Cycle 2: the partial/notes inline-JS branch + the QA-1 awaiting-state gate --- #


def test_partial_extraction_note_path_wired():
    """AC-2: the inline JS reads d.partial/d.notes from /upload and references the note element.

    The `up(f)` upload-response / `showReview` flow READS the partial signal + notes from T4's
    `/upload` JSON payload (`d.partial`, `d.notes` — the discriminator no longer drops them) AND
    references the note element (`getElementById('extraction-note')`) so the note is populated/shown
    from the payload. Failing-capable: reds if the discriminator drops `d.partial`/`d.notes` or the
    inline JS never reaches the note element.
    """
    html = _spa_html()
    assert "d.partial" in html, "the upload discriminator drops the partial signal (no d.partial)"
    assert "d.notes" in html, "the upload discriminator drops the notes (no d.notes)"
    assert "getElementById('extraction-note')" in html, "the inline JS never references the partial-note element"


def test_partial_empty_shows_note_and_hides_awaiting():
    """QA-1 (LOAD-BEARING): partial+empty shows the note + hides the awaiting state.

    The awaiting-display gate in `showReview` is `readings.length||partial` (NOT just
    `readings.length`), so `partial==True` with `readings==[]` HIDES the silent 'no new data'
    awaiting state; AND the note-show gates on the `partial` signal (the note is shown + populated
    from `notes` when partial, independent of `readings.length`). Whitespace is normalized before
    the substring assertion so the gate matches regardless of spacing. Failing-capable: reds if the
    gate reverts to `readings.length` only, or the note-show drops the `partial` gate.
    """
    html = _spa_html().replace(" ", "")
    assert "readings.length||partial" in html, (
        "the awaiting-display gate is not (readings.length||partial) — a partial+empty extraction "
        "would re-show the silent 'no new data' awaiting state (QA-1)"
    )
    assert "if(partial)" in html, "the note-show does not gate on the partial signal"
    assert "notes.join" in html, "the note is not populated from the notes list when partial"


def test_genuinely_empty_not_partial_keeps_honest_awaiting():
    """AC-3 (empty side): a genuinely-empty (not-partial) extraction keeps the honest awaiting state, note hidden.

    A genuinely-empty extraction (0 findings, not partial) still shows the honest awaiting state and
    NOT the note: the default-rendered awaiting `.empty` div is visible (no `display:none` baked onto
    it), the note element is default-hidden, and the note-show is gated behind `partial` (so a
    non-partial response leaves the note hidden). Failing-capable: reds if the note is shown
    unconditionally (the partial gate dropped) or the awaiting marker is removed — proving a partial
    is never collapsed into, and the empty state is never replaced by, the note.
    """
    block = _panel_build_html(_spa_html())
    aw = re.search(r"<div[^>]*data-awaiting='extraction'[^>]*>", block)
    assert aw is not None, "the honest awaiting-state marker was removed"
    assert "display:none" not in aw.group(0), "the awaiting `.empty` div is hidden by default (honest empty broken)"
    note = _extraction_note_open_tag(block)
    assert note is not None and "display:none" in note.group(0), "the partial-note element is not default-hidden"
    html = _spa_html().replace(" ", "")
    assert "if(partial)" in html, "the note-show is not gated behind the partial signal (a non-partial render would show it)"


def test_extraction_note_carries_role_status_for_screen_readers():
    """design-reviewer S1 (WCAG 4.1.3): the dynamically-shown partial-note carries role="status".

    The #extraction-note element is shown client-side when an extraction is partial; without
    role="status" (implicit aria-live="polite") a screen reader never announces the
    document-quality note. Mirrors the T4/W4 reading-confirm aria-label precedent. Failing-capable:
    reds if role="status" is removed from the note element.
    """
    note = _extraction_note_open_tag(_panel_build_html(_spa_html()))
    assert note is not None, "no partial-extraction note element in the review-panel surface"
    assert 'role="status"' in note.group(0), (
        'the #extraction-note carries no role="status" — its partial note is never announced (WCAG 4.1.3)'
    )


# --------------------------------------------------------------------------- #
# PR #270 — the wired Plan-screen render guards: the placeholder specialist grid
# stays empty when real plans render (HIST-02), the plan-zone marker is substituted,
# an injected exercise name is HTML-escaped (XSS), and the extracted-genotype dna
# status renders in BOTH templates without an IndexError (API-01). Fixture-driven.
# --------------------------------------------------------------------------- #


def test_rendered_spa_substitutes_plan_zone_and_keeps_specialists_grid():
    """HIST-02: the SPA substitutes the <!--PLAN_ZONE--> marker and keeps the #plan-specialists grid.

    `render` replaces `<!--PLAN_ZONE-->` with the Plan-screen body (the awaiting state on an empty
    store), so the raw marker is GONE from the rendered SPA; the `#plan-specialists` grid element
    (which the init JS still references) stays present. Failing-capable: reds if the marker is left
    un-substituted or the grid element is deleted (the line-572 init JS would then null-deref).
    """
    html = _spa_html()
    assert "<!--PLAN_ZONE-->" not in html, "the plan-zone marker was not substituted by render"
    assert 'id="plan-specialists"' in html, "the #plan-specialists grid the init JS references is gone"


def test_plan_specialists_fill_gated_on_awaiting_plan_state():
    """HIST-02: the placeholder specialist-grid fill is GATED on the awaiting-plan state.

    The init JS only populates `#plan-specialists` with the 'Generated on plan run' placeholder cards
    when the awaiting-plan element (`#screen-plan [data-awaiting="plan"]`) is present — so when the
    server has substituted <!--PLAN_ZONE--> with real recorded plans (that element absent), the
    placeholder grid stays empty and the recorded plans are the sole Plan content. Failing-capable:
    reds if the fill becomes unconditional again (the dual-render the finding flagged).
    """
    html = _spa_html().replace(" ", "")
    assert "if(document.querySelector('#screen-plan[data-awaiting=\"plan\"]')){" in html, (
        "the #plan-specialists placeholder fill is not gated on the awaiting-plan state (dual-render)"
    )


def test_plan_zone_escapes_injected_exercise_name(tmp_path):
    """XSS: a `<script>` in a recorded exercise name renders HTML-escaped, never raw.

    Seeds a `plan::workout` reading whose exercise name carries `<script>alert(1)</script>`, renders
    the SPA over the store read, and asserts the name appears HTML-ESCAPED (`&lt;script&gt;...`) and
    the raw `<script>alert(1)</script>` token is ABSENT — the server-side `_esc` on every plan value
    holds. Failing-capable: drop the `_esc` on the exercise name and the raw token leaks into markup.
    """
    import datetime

    from scripts.store import plan_schema, store

    payload = "<script>alert(1)</script>"
    plan_schema.record_plan(
        "workout", {"exercises": [{"name": payload, "sets": 3}]},
        "2026-06-18", "personal-trainer", tmp_path,
    )
    html = app_shell.render(store.read_all(tmp_path), _today=datetime.date(2026, 6, 18))

    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html, "the injected exercise name is not HTML-escaped"
    assert payload not in html, "the raw <script> token leaked into the rendered markup (XSS)"


def test_extracted_genotype_dna_status_renders_in_both_doc_cards():
    """API-01: an extracted-genotype dna status (files: [], count: N) renders in BOTH templates.

    `dna_status` over `dna-report` readings with an empty dropzone returns `{loaded: True, files: [],
    count: N}`; BOTH `app_shell._doc_cards` AND `intake._doc_cards` must render it WITHOUT an
    IndexError (the prior `dna['files'][0]` guarded only by `if loaded` crashed on the empty files
    list). Each renders the genotype-count detail instead of a filename. Failing-capable: revert
    either guard to `dna['files'][0]` and the matching render raises.
    """
    from scripts.ingest import status as ingest_status
    from vault.design.templates import intake

    readings = [
        {"item": "MTNR1B rs10830963", "timepoint": "2026-04-01", "source": "dna-report", "value": "(C;G)"},
        {"item": "APOE rs429358", "timepoint": "2026-04-01", "source": "dna-report", "value": "(T;T)"},
    ]
    dna = ingest_status.dna_status(readings, REPO_ROOT / "no_such_dna_dropzone_dir")
    assert dna == {"loaded": True, "files": [], "count": 2}

    status = {"wearable": {"loaded": False}, "labs": {"loaded": False, "files": []}, "dna": dna}
    # Neither render raises (the API-01 crash); each names the genotype count, not a (missing) file.
    assert "2 genotypes landed" in app_shell._doc_cards(status), "app_shell did not render the genotype count"
    assert "2 genotypes landed" in intake._doc_cards(status), "intake did not render the genotype count"


# --------------------------------------------------------------------------- #
# In-app 'Generate plan' trigger: the Plan-screen button POSTs /generate-plan and
# the inline JS swaps the re-rendered Plan zone in. Fixture-driven (rendered-SPA string).
# --------------------------------------------------------------------------- #


def test_plan_screen_generate_button_wired_to_generate_plan():
    """The Plan-screen 'Generate plan' button is wired to POST /generate-plan and render the reply.

    The awaiting-plan state carries a `#plan-gen-run` button + a `#plan-gen-status` line, the Plan
    zone is wrapped in a stable `#plan-zone` container the inline JS swaps the re-rendered plans
    into, and the inline JS fetches `/generate-plan` and reads the `need_key` / `plan_html` /
    `results` reply. Failing-capable: reds if the button / status / zone is dropped or the fetch
    + reply-reads are unwired.
    """
    html = _spa_html()
    assert 'id="plan-gen-run"' in html, "the Plan screen has no Generate-plan button"
    assert "id='plan-gen-status'" in html or 'id="plan-gen-status"' in html, "no generate-status line"
    assert 'id="plan-zone"' in html, "the Plan zone has no stable container the JS swaps into"
    assert "fetch('/generate-plan'" in html, "the Plan JS does not POST /generate-plan"
    assert "d.need_key" in html, "the Plan JS does not read the no-key signal"
    assert "d.plan_html" in html, "the Plan JS does not render the returned plan zone"
    assert "d.results" in html, "the Plan JS does not surface the per-domain results"


# --------------------------------------------------------------------------- #
# Intake demographic re-hydration: the 'About you' form pre-fills from the
# operator's saved store values so they do not re-type saved demographics each
# visit. Fixture-driven (the rendered-SPA string over a seeded store root).
# --------------------------------------------------------------------------- #


def _seed_demographics(root, values, *, timepoint="2026-06-01T00:00:00+00:00", source="intake"):
    """Append one `source:"intake"` reading per (item, value) pair under the store root."""
    for item, value in values.items():
        store.append(
            item, {"item": item, "timepoint": timepoint, "source": source, "value": value}, root=root,
        )


def test_demographic_form_prefills_each_saved_value(tmp_path):
    """PREFILL-1: a store with saved demographics pre-fills EACH amended form field + shows the banner.

    Seeds the saved demographic readings (the amended full-date birthdate + the `bodyweight-kg`
    number + the two selects + the chat-only goal-domains) and renders the SPA over the resolved
    read model. The amended date input carries `value='1986-04-12'`, the `bodyweight-kg` number
    carries `value='82'`, and each <select> pre-SELECTS the saved option. The '✓ Saved — edit to
    update' banner is shown so the operator sees they were remembered. Failing-capable: reds if any
    field renders blank/default or the banner is absent.
    """
    root = tmp_path / "store"
    _seed_demographics(root, {
        "date-of-birth": "1986-04-12",
        "sex-for-dosing": "male",
        "bodyweight-kg": "82",
        "equipment-access-class": "full-home-gym",
        "goal-domains": "Workout;Nutrition",  # chat-only field: no form surface, not pre-filled
    })
    html = app_shell.render(store.read_all(root))
    assert "name='date-of-birth' value='1986-04-12'>" in html, "the full-date birthdate is not pre-filled"
    assert "name='bodyweight-kg' value='82'" in html, "the bodyweight-kg number is not pre-filled"
    assert "<option value='male' selected>" in html, "sex-for-dosing not pre-selected"
    assert "<option value='full-home-gym' selected>" in html, "equipment-access-class not pre-selected"
    assert "data-prefill='saved'" in html and "✓ Saved" in html, "no saved-state banner on the pre-filled form"
    # goal-domains has no <select>/checkbox surface on the demographic sub-form, so it is not
    # injected as a fabricated form option (it stays a chat-only field gathered at POST /chat).
    assert "<option value='Workout' selected>" not in html, "goal-domains was injected as a form option"


def test_prefill_tracks_the_saved_weight_and_resolves_latest(tmp_path):
    """PREFILL-2 (non-tautological + latest-wins): a DIFFERENT saved weight pre-fills a DIFFERENT value.

    Content-traceability: rendering with bodyweight-kg='90' pre-fills value='90' and NOT '60'; with
    bodyweight-kg='60' it pre-fills '60' and NOT '90' — the pre-fill tracks the stored value, it is
    not a fixed/tautological fill. Latest-wins: with two readings for the item, the greater-timepoint
    value is pre-filled and the stale one is not. Failing-capable: reds if the fill is fixed, ignores
    the saved value, or pre-fills the older reading.
    """
    root_a = tmp_path / "a"
    _seed_demographics(root_a, {"bodyweight-kg": "90"})
    html_a = app_shell.render(store.read_all(root_a))
    assert "name='bodyweight-kg' value='90'" in html_a, "the saved 90 weight is not pre-filled"
    assert "name='bodyweight-kg' value='60'" not in html_a, "a different (unsaved) weight was pre-filled"

    root_b = tmp_path / "b"
    _seed_demographics(root_b, {"bodyweight-kg": "60"})
    html_b = app_shell.render(store.read_all(root_b))
    assert "name='bodyweight-kg' value='60'" in html_b, "the saved 60 weight is not pre-filled"
    assert "name='bodyweight-kg' value='90'" not in html_b, "a different (unsaved) weight was pre-filled"

    root_c = tmp_path / "c"
    _seed_demographics(root_c, {"bodyweight-kg": "60"}, timepoint="2026-05-01T00:00:00+00:00")
    _seed_demographics(root_c, {"bodyweight-kg": "90"}, timepoint="2026-06-01T00:00:00+00:00")
    html_c = app_shell.render(store.read_all(root_c))
    assert "name='bodyweight-kg' value='90'" in html_c, "the latest reading is not pre-filled"
    assert "name='bodyweight-kg' value='60'" not in html_c, "the stale (older) reading was pre-filled"


def test_demographic_form_blank_default_on_empty_store():
    """PREFILL-3 (HONEST-EMPTY): an empty store renders the amended form blank/default with no banner.

    With no saved readings, no demographic <select> carries a `selected` option, the amended date
    + `bodyweight-kg` number inputs carry no `value=` attribute, and the saved-state banner is
    absent — the form is honest blank, no fabricated pre-fill. Failing-capable: reds if any option
    is pre-selected, an input gains a value, or the banner renders on an empty store.
    """
    html = _spa_html()  # app_shell.render([])
    assert "data-prefill='saved'" not in html, "the saved-state banner renders on an empty store"
    assert "name='date-of-birth'>" in html, "the amended date input is not blank/default"
    assert "value='" not in _panel_build_html(html).split("name='bodyweight-kg'", 1)[1][:40], (
        "the bodyweight-kg number carries a value on an empty store"
    )
    for name in ("sex-for-dosing", "equipment-access-class"):
        assert "selected" not in _select_block(html, name), (
            f"the {name} select pre-selects an option on an empty store"
        )


# --------------------------------------------------------------------------- #
# ADR-0033-0035-T4 Cycle 1 — the AMENDED demographic inputs (full-date birthdate
# + bodyweight-kg number) + the `_prefill_form` CONSUMER-INTEGRITY rework: the
# retargeted string-replace cannot silently no-op against the RETIRED targets.
# --------------------------------------------------------------------------- #


def test_amended_birthdate_is_full_date_input_old_year_text_gone():
    """AC-2 (amended birthdate): `#panel-build` carries a full-date `date-of-birth` input, year-text GONE.

    ADR-0034 replaces the born-year text input (`placeholder="e.g. 1986"`) with a full-date
    `<input type='date' name='date-of-birth'>`. The retired year-text markup is ABSENT from the
    rendered SPA — so a stale `_prefill_form` replace against it cannot pass vacuously. Failing-
    capable: reds if the date input is missing or the old year-text placeholder survives.
    """
    html = _spa_html()
    assert re.search(r"<input[^>]*type='date'[^>]*name='date-of-birth'", html), (
        "the amended `#panel-build` form carries no full-date `date-of-birth` input"
    )
    assert 'placeholder="e.g. 1986"' not in html, "the retired born-year text input still renders"


def test_prefill_consumer_integrity_no_silent_noop(tmp_path):
    """AC-7 (consumer integrity): the reworked `_prefill_form` fills the AMENDED targets, retired ones GONE.

    The silent-no-op trap (CLAUDE.md Factory-to-Component Wiring Rule): `_prefill_form` prefills by
    STRING REPLACE against literal markup. T4 retires the `placeholder="e.g. 1986"` year-text target
    AND the `bodyweight-band` <option> target; a replace against an absent literal would silently
    no-op (a saved value renders blank, no error). This gate proves the consumer + markup were
    reconciled together: a seeded full-date DOB + `bodyweight-kg` reading PREFILL the amended date
    `value=` + number `value=` (the replace hits the NEW targets), AND both retired targets are GONE
    from the rendered SPA (so no stale replace can pass vacuously). Failing-capable: revert the
    markup (keep the year-text) and the date `value=` assertion reds; revert the consumer retarget
    (keep targeting the year-text literal) and the prefill no-ops -> the `value=` assertion reds.
    """
    root = tmp_path / "store"
    _seed_demographics(root, {"date-of-birth": "1986-04-12", "bodyweight-kg": "82"})
    html = app_shell.render(store.read_all(root))
    # the prefill hits the AMENDED targets (the rework wired the new replace literals)
    assert "name='date-of-birth' value='1986-04-12'>" in html, "the amended date input was not pre-filled"
    assert "name='bodyweight-kg' value='82'" in html, "the amended bodyweight-kg number was not pre-filled"
    assert "data-prefill='saved'" in html and "✓ Saved" in html, "no saved-state banner on the pre-filled form"
    # the RETIRED targets are GONE — a stale replace cannot pass vacuously
    assert 'placeholder="e.g. 1986"' not in html, "the retired year-text replace target still renders"
    assert "bodyweight-band" not in html, "the retired bodyweight-band <option> replace target still renders"


# --------------------------------------------------------------------------- #
# ADR-0033-0035-T4 Cycle 2 — the 9-step Create-Profile WIZARD (matching the
# operator-signed-off mockup), the rich-domain + safety field names, the generic
# render-state-driven source labels, the existing-seam Documents/API-key reuse,
# and the inline-asset render gate. Rendered-HTML / real-emit, 0 live spend.
# --------------------------------------------------------------------------- #

# The 9 wizard step headings in mockup order (`prototype/intake-onboarding-mockup.html`), as
# they appear in the rendered markup (the `&` in three headings is HTML-escaped to `&amp;`).
_WIZARD_STEP_HEADINGS = (
    "Demographics", "Goals", "Training &amp; activity", "Diet", "Supplements &amp; peptides",
    "Medications", "Health &amp; lifestyle", "Documents", "API key",
)

# The generic multi-source wearable/DNA names the wizard Documents step lists (parsed locally),
# so no single operator source is the sole affordance (NFR-4 recurring-flag class).
_GENERIC_SOURCES = ("Apple Health", "Garmin", "Whoop", "Oura", "Fitbit", "23andMe", "AncestryDNA")

# Every same-origin loopback path the SPA may fetch/POST to (no new route — ADR-0033).
_KNOWN_LOOPBACK = {"/chat", "/upload", "/settings/key", "/confirm-extraction", "/generate-plan"}


def _wizard_html(html):
    """The `#screen-wizard` Create-Profile wizard section the 9 steps live in."""
    m = re.search(r'<section[^>]*id="screen-wizard"[^>]*>(.*?)</section>', html, re.DOTALL)
    assert m is not None, "the rendered SPA carries no `#screen-wizard` Create-Profile section"
    return m.group(1)


def test_wizard_has_nine_step_containers_with_headings():
    """W1/AC-1: the wizard parses to 9 `data-step` containers (1-9) each with its mockup heading.

    Failing-capable: a missing step container or a dropped heading reds the per-step assertion.
    """
    wiz = _wizard_html(_spa_html())
    steps = set(re.findall(r'data-step="(\d)"', wiz))
    assert steps == {str(n) for n in range(1, 10)}, f"the wizard does not carry steps 1-9: {sorted(steps)}"
    for heading in _WIZARD_STEP_HEADINGS:
        assert heading in wiz, f"the wizard is missing the step heading {heading!r}"


def test_wizard_demographics_step_carries_amended_fields_and_guidance():
    """W2/AC-2: the wizard demographics step carries the amended fields + the privacy guidance copy.

    The full-date `date-of-birth`, the `bodyweight-kg` number + lbs/kg unit, `sex-for-dosing`, the
    OPTIONAL race/ethnicity field + occupation, plus the 'only your age is used' / 'stays on your
    machine' / 'never sent to the planner' guidance. Failing-capable: reds if any field or the
    privacy copy is dropped.
    """
    wiz = _wizard_html(_spa_html())
    assert re.search(r"<input[^>]*type='date'[^>]*name='date-of-birth'", wiz), "no full-date birthdate in the wizard"
    assert re.search(r"<input[^>]*type='number'[^>]*name='bodyweight-kg'", wiz), "no bodyweight-kg number in the wizard"
    assert ">lbs</option>" in wiz and ">kg</option>" in wiz, "no lbs/kg unit select in the wizard demographics step"
    assert "name='sex-for-dosing'" in wiz, "no sex-for-dosing field in the wizard"
    assert "name='race-ethnicity'" in wiz, "no optional race/ethnicity field in the wizard"
    assert "name='occupation'" in wiz, "no occupation field in the wizard"
    assert "only your age is used" in wiz, "the birthdate privacy guidance is missing"
    assert "stays on your machine" in wiz, "the on-device birthdate copy is missing"
    assert "never sent to the planner" in wiz, "the race/ethnicity de-identification copy is missing"


def test_wizard_carries_rich_domain_and_safety_controls_no_cannabis():
    """W3/AC-3: the wizard carries the pinned rich-domain field names + the safety screens, NO cannabis.

    The four `_CHAT_RAW_SOURCE_FIELDS` rich-domain names, the exercise-safety (chest pain / dizziness
    / shortness of breath), apnea, PHQ-2, smoker (Yes/Former→years/Never), and alcohol
    (None/Rarely/Monthly/Weekly/Most days) controls. The sensitive record-only roster is CLOSED — no
    recreational-substance control (capture.py forward constraint). Failing-capable: reds if a field
    name or safety control is absent, or a cannabis control appears.
    """
    wiz = _wizard_html(_spa_html())
    for field in _WIZARD_RICH_FIELDS:
        assert f"name='{field}'" in wiz, f"the wizard does not carry the rich-domain field {field!r}"
    # exercise-safety screen
    assert "chest pain" in wiz and "dizziness" in wiz and "shortness of breath" in wiz, "no exercise-safety screen"
    # sleep-apnea screen
    assert "stop breathing" in wiz, "no sleep-apnea screen"
    # PHQ-2
    assert "little interest or pleasure" in wiz and "down, depressed, or hopeless" in wiz, "no PHQ-2 screen"
    # smoker: Yes / Former (-> years since quit) / Never
    assert "Former" in wiz and "Never" in wiz and "since you quit" in wiz, "no smoker (Former->years/Never) control"
    # alcohol frequency band
    for band in ("None", "Rarely", "Monthly", "Weekly", "Most days"):
        assert band in wiz, f"the alcohol frequency band {band!r} is missing"
    # the CLOSED record-only roster: no recreational-substance control
    assert "cannabis" not in wiz.lower(), "the wizard carries a cannabis/recreational-substance control (forbidden)"


def test_wizard_documents_and_key_reuse_existing_seams_with_key_affordance():
    """W4/AC-4: Documents reuses /upload→/confirm-extraction, the key step /settings/key; no new route.

    Every fetch target stays within the known same-origin loopback set (the wizard adds NO new path),
    and the API-key step carries the empty-vs-saved keystate affordance (masked + greyed `disabled` +
    `✓ Saved`). Failing-capable: reds if a new fetch path appears or the key affordance is absent.
    """
    html = _spa_html()
    assert "fetch('/upload'" in html, "the existing /upload flow the wizard Documents step reuses is gone"
    assert "fetch('/confirm-extraction'" in html, "the existing /confirm-extraction flow is gone"
    assert "/settings/key" in html, "the existing /settings/key flow the wizard key step reuses is gone"
    targets = set(re.findall(r"fetch\(\s*['\"]([^'\"]+)['\"]", html))
    assert targets and targets <= _KNOWN_LOOPBACK, f"the wizard added a fetch path beyond the known set: {sorted(targets - _KNOWN_LOOPBACK)}"
    wiz = _wizard_html(html)
    assert "keymask" in wiz, "the wizard key step carries no masked key affordance"
    assert "disabled" in wiz, "the wizard key step carries no greyed (disabled) saved-key state"
    assert "✓ Saved" in wiz, "the wizard key step carries no '✓ Saved' affordance"


def test_wizard_and_doc_cards_use_generic_render_state_driven_source_labels():
    """W5/AC-5: all three surfaces use GENERIC source labels (the NFR-4 recurring-flag class).

    (a) the wizard Documents step lists the generic multi-source affordance ('parsed locally' + the
    named sources) with no single-operator-source as the sole label; (b) `_doc_cards`: the literal
    'Wearable export (Apple Health)' is GONE, and a NON-'Apple Health' loaded source renders a
    render-state-driven '· detected: <source>' suffix; (c) the upload-status copy no longer singles
    out one operator source. Failing-capable: revert any surface to the hardcoded single source.
    """
    html = _spa_html()
    wiz = _wizard_html(html)
    # (a) wizard Documents step: generic multi-source affordance
    assert "parsed locally" in wiz, "the wizard Documents step drops the 'parsed locally' assurance"
    for source in _GENERIC_SOURCES:
        assert source in wiz, f"the wizard Documents step does not name the supported source {source!r}"
    # (b) _doc_cards: the hardcoded single-source title is gone; the source is render-state-driven
    assert "Wearable export (Apple Health)" not in html, "the _doc_cards wearable card still hardcodes 'Apple Health'"
    status = {
        "wearable": {"loaded": True, "source": "Garmin", "count": 1, "items": ["hrv"],
                     "range": ["2026-06-01", "2026-06-02"]},
        "dna": {"loaded": False, "files": []},
        "labs": {"loaded": False, "files": []},
    }
    loaded = app_shell.render([], status=status)
    assert "Wearable export · detected: Garmin" in loaded, "the wearable title does not track the loaded source (render-state-driven)"
    assert "Wearable export (Apple Health)" not in loaded, "the loaded wearable card still hardcodes 'Apple Health'"
    # (c) the upload-status copy no longer singles out one operator source
    assert "an Apple Health .zip" not in html, "the upload-status copy still singles out one operator source"


def test_wizard_carries_rich_fields_panel_build_form_does_not():
    """W6/AC-2/AC-6: the rich-domain fields route through the WIZARD, not the objective `#panel-build` form.

    The ADR-0034 supersession positive control (pairs with the re-scoped objective-only reconcile):
    each rich-domain field is in the wizard AND absent from the `#panel-build` form name set — proving
    the objective-only assertion re-SCOPED the coverage, not deleted it. Failing-capable: reds if a
    rich field leaks onto the demographic form or is missing from the wizard.
    """
    html = _spa_html()
    wiz = _wizard_html(html)
    panel_form_names = _form_field_names(_upload_form_html(html))
    for field in _WIZARD_RICH_FIELDS:
        assert f"name='{field}'" in wiz, f"the wizard does not carry the rich-domain field {field!r}"
        assert field not in panel_form_names, f"the rich-domain field {field!r} leaked onto the objective `#panel-build` form"


def test_wizard_keeps_spa_inline_asset_clean(tmp_path):
    """W7/AC-6 (AUTHORITATIVE inline-asset): generate.run('app') emits a Path with the wizard, no off-file ref.

    Drives the REAL `generate.run('app')` (render.emit RAISES ValueError on any off-file asset
    reference) and asserts it returns a written Path that EXISTS, carries the wizard, and has no
    off-file `<script src>`. A substring grep is NOT substituted for the emit probe.
    """
    path = _emit_app(tmp_path)
    assert isinstance(path, Path) and path.exists(), "generate.run('app') did not emit with the wizard"
    emitted = path.read_text()
    assert 'id="screen-wizard"' in emitted, "the emitted SPA carries no Create-Profile wizard"
    assert "<script src" not in emitted, "the wizard added an off-file <script src> reference"


# --------------------------------------------------------------------------- #
# ADR-0033-0035-T5 — the Create-Profile EQUIPMENT screen (`#screen-equipment`):
# the 4-class `equipment-access-class` SELECT + the access-gated 4-group / 29-item
# checklist (the SPECIFIC cardio machines, never a generic "cardio machine") + the
# bodyweight-only hide-and-note + a distinct inline `<svg>` per item. Markup-only —
# the Create-Profile submit is wired by T10 (the T4↔T5 seam adjudication), so these
# cases assert the served MARKUP, region-scoped to `#screen-equipment`. E1 is
# RE-SCOPED region-scoped: the recipe's stale whole-SPA `count==1` is dropped because
# the SPA legitimately carries TWO `equipment-access-class` controls by design — the
# Create-Profile equipment screen (this) and the unlocked My-Info `#panel-build`
# surface (create once, edit later). Rendered-HTML / real-emit, 0 live spend.
# --------------------------------------------------------------------------- #

from scripts.plan import router as _router

# The four checklist group headings (mockup `#mock-equipment`), `&` HTML-escaped to `&amp;`.
_EQUIP_GROUP_HEADINGS = (
    "Free weights &amp; racks", "Cardio machines", "Resistance machines",
    "Bodyweight &amp; accessories",
)
# The per-group item counts, in heading order (7 + 6 + 5 + 11 = 29).
_EQUIP_GROUP_COUNTS = (7, 6, 5, 11)
# The six SPECIFIC cardio machines (never a single generic "cardio machine").
_CARDIO_MACHINES = ("Treadmill", "Exercise bike", "Stair", "Elliptical", "Rowing", "Air")
# The pinned bodyweight-only note copy (mockup `#equip-bw-note`).
_EQUIP_BW_NOTE = "No equipment needed — we'll program bodyweight-only"
# The new record-only local field the 29 detail items submit under (NOT a planner token).
_EQUIP_DETAIL_FIELD = "equipment-detail"


def _equip_screen(html):
    """The `#screen-equipment` Create-Profile equipment screen region from the rendered SPA."""
    m = re.search(r'<section[^>]*id="screen-equipment"[^>]*>(.*?)</section>', html, re.DOTALL)
    assert m is not None, "the rendered SPA carries no `#screen-equipment` Create-Profile equipment screen"
    return m.group(1)


def _equip_group_counts(region):
    """Per-group `equipment-detail` item counts, in `_EQUIP_GROUP_HEADINGS` order.

    Each group heading is immediately followed by its `.equip-grid`, whose only children are the
    item `<label>`s (no nested `<div>`), so the group's items are the `name='equipment-detail'`
    controls captured between the heading and the grid's closing `</div>`.
    """
    counts = []
    for heading in _EQUIP_GROUP_HEADINGS:
        i = region.find(heading)
        assert i != -1, f"the equipment screen is missing the group heading {heading!r}"
        grid = re.search(r'<div class="equip-grid">(.*?)</div>', region[i:], re.DOTALL)
        assert grid is not None, f"the {heading!r} group has no `.equip-grid` item container"
        counts.append(grid.group(1).count(f"name='{_EQUIP_DETAIL_FIELD}'"))
    return tuple(counts)


# --- Cycle 1: the access SELECT (region-scoped no-drift) + gating + bw-note + field-name --- #


def test_equip_screen_access_select_is_region_scoped_four_class_no_drift():
    """E1 (AC-1, RE-SCOPED region-scoped per the T4↔T5 seam adjudication): the equipment screen
    carries the 4-class `equipment-access-class` select, option values == the gate constant.

    The recipe's stale whole-SPA `count==1` guard is DROPPED: the served SPA legitimately carries
    two `equipment-access-class` controls — the Create-Profile equipment screen (this one) and the
    unlocked My-Info `#panel-build` surface. So the no-drift assertion is SCOPED to
    `#screen-equipment`, and is failing-capable there (the panel-build select can NOT satisfy it):
    before the equipment screen exists `_equip_screen` reds; a dropped/extra class or a
    label-not-token value reds the set-equality.
    """
    region = _equip_screen(_spa_html())
    values = set(re.findall(r"<option value='([^']*)'", _select_block(region, "equipment-access-class")))
    values.discard("")
    assert values == set(capture.EQUIPMENT_ACCESS_CLASSES), (
        f"the equipment screen access-class options {sorted(values)} drifted from the gate "
        f"constant {sorted(capture.EQUIPMENT_ACCESS_CLASSES)}"
    )


def test_equip_screen_access_gates_checklist_and_bodyweight_only_note():
    """E2 (AC-3): the access select carries a gating hook; the checklist container is present
    (shown for a non-bodyweight value); the bodyweight-only note is present, default-hidden, pinned.

    Server-rendered static HTML + client JS, so the markup half is asserted (the test does not
    execute JS): the access select's `onchange=` gating hook, the `#equip-detail` checklist host
    (default-shown), and the `#equip-bw-note` element default-hidden (`display:none`) carrying the
    pinned copy. Failing-capable: remove the hook / the container / the note or its copy → reds.
    """
    region = _equip_screen(_spa_html())
    sel_open = re.search(r"<select[^>]*name='equipment-access-class'[^>]*>", region)
    assert sel_open is not None, "the equipment screen has no equipment-access-class select"
    assert "onchange=" in sel_open.group(0), "the access select carries no gating hook (onchange=)"
    assert 'id="equip-detail"' in region, "the equipment screen has no access-gated checklist container"
    note = re.search(r'<div[^>]*id="equip-bw-note"[^>]*>', region)
    assert note is not None, "the equipment screen has no bodyweight-only note element"
    assert "display:none" in note.group(0), "the bodyweight-only note is not default-hidden"
    assert _EQUIP_BW_NOTE in region, "the bodyweight-only note is missing its pinned copy"


def test_equip_detail_items_submit_record_only_local_field_not_planner_token():
    """E3 (AC-5, MARKUP half / QA-F2): the access select submits the planner token; the 29 detail
    items submit under the NEW local field `equipment-detail`, record-only BY CONSTRUCTION.

    The access select submits `name='equipment-access-class'` (the pinned planner token); the 29
    detail items submit under `name='equipment-detail'` — a field absent from BOTH
    `router.SUMMARY_FIELD_SET` and `capture.WIRED_TOKENS`, so `persist_capture`'s default routes it
    record-only (the planner gets no new token from the detailed set). The routing itself is T1's
    `test_capture.py` contract — asserted here only at the field-NAME + membership level. Failing-
    capable: naming the detail field a SUMMARY_FIELD_SET token reds the `∉` assertions.
    """
    region = _equip_screen(_spa_html())
    assert "name='equipment-access-class'" in region, "the equipment access select does not submit the planner token"
    assert region.count(f"name='{_EQUIP_DETAIL_FIELD}'") == 29, (
        "the equipment screen does not carry 29 detail items under the record-only `equipment-detail` field"
    )
    assert _EQUIP_DETAIL_FIELD not in _router.SUMMARY_FIELD_SET, "`equipment-detail` leaked into the planner SUMMARY_FIELD_SET"
    assert _EQUIP_DETAIL_FIELD not in capture.WIRED_TOKENS, "`equipment-detail` leaked into capture.WIRED_TOKENS"


# --- Cycle 2: the 4-group / 29-item checklist + distinct inline <svg> + the render gate --- #


def test_equip_checklist_four_groups_29_items_specific_cardio_machines():
    """E4 (AC-2): the checklist carries the four groups with per-group counts (7, 6, 5, 11) and the
    SIX specific cardio machines (never a single generic "cardio machine").

    Parses `#screen-equipment` for the four group headings and counts each group's
    `equipment-detail` items. Also asserts the cardio group enumerates >= 5 of the 6 named machines
    — the not-a-generic-"cardio machine" guard. Failing-capable: a miscount or a generic-collapse
    of the cardio group reds.
    """
    region = _equip_screen(_spa_html())
    for heading in _EQUIP_GROUP_HEADINGS:
        assert heading in region, f"the equipment checklist is missing the group heading {heading!r}"
    assert _equip_group_counts(region) == _EQUIP_GROUP_COUNTS, (
        f"the per-group item counts are not {_EQUIP_GROUP_COUNTS} (sum 29)"
    )
    ci, ri = region.find("Cardio machines"), region.find("Resistance machines")
    cardio_seg = region[ci:ri]
    present = [m for m in _CARDIO_MACHINES if m in cardio_seg]
    assert len(present) >= 5, f"the cardio group names only {present} — a generic-collapse regression"


def test_equip_items_carry_distinct_inline_svg_icons_no_off_file_asset():
    """E5 (AC-4, markup leg): each of the 29 items carries a distinct inline `.eq-ic` `<svg>` icon,
    with 0 off-file asset in the equipment region.

    Counts the per-item icon svgs (the `.eq-ic` block) == 29, asserts the set of distinct icon-svg
    blocks has >= 20 members (not one repeated placeholder), and asserts the region carries no
    off-file `<img src>` / non-`data:` external `src`. Failing-capable: a single repeated
    placeholder icon reds the distinct-count; an off-file `<img src>` reds the no-asset assertion.
    """
    region = _equip_screen(_spa_html())
    icons = re.findall(r'<span class="eq-ic"><svg.*?</svg></span>', region, re.DOTALL)
    assert len(icons) == 29, f"the equipment region carries {len(icons)} per-item icons, expected 29"
    assert len(set(icons)) >= 20, f"the item icons are not distinct ({len(set(icons))} unique) — a repeated placeholder"
    assert "<img" not in region, "the equipment region carries an off-file <img> asset"
    assert 'src="http' not in region and "src='http" not in region, "the equipment region carries an http-sourced asset"


def test_equip_screen_keeps_spa_inline_asset_clean(tmp_path):
    """E6 (AC-4, AUTHORITATIVE inline-asset): generate.run('app') emits a Path with the equipment
    screen, no off-file ref.

    Drives the REAL `generate.run('app')` (render.emit RAISES ValueError on any off-file asset
    reference) and asserts it returns a written Path that EXISTS, carries `#screen-equipment`, and
    has no off-file `<script src>`. A substring grep is NOT substituted for the emit probe.
    """
    path = _emit_app(tmp_path)
    assert isinstance(path, Path) and path.exists(), "generate.run('app') did not emit with the equipment screen"
    emitted = path.read_text()
    assert 'id="screen-equipment"' in emitted, "the emitted SPA carries no `#screen-equipment` equipment screen"
    assert "<script src" not in emitted, "the equipment screen added an off-file <script src> reference"
