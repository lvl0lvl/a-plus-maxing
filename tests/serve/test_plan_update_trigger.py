"""Manual plan-update trigger + Off/Weekly/Daily schedule setting (ADR-0049-T2, TERMINAL).

The My Info "Plan updates" section: a manual "Update my plan now" trigger that REUSES the
already-routed CSRF-gated `POST /plan-loop` (no new spend route), plus an Off/Weekly/Daily
schedule radio whose pick records the cadence INTENT through a new `POST /settings/schedule`
route (a `store.append` reading, `source:"settings"`). Daily is inert ("coming soon") and arms
no real runner.

All fixture-driven: 0 live network, 0 key read, 0 metered spend. The loop is honestly degraded
(`loop_dispatch = None` at the production site), so every trigger click resolves to the honest
not-yet-available state (AC-1b) — the render/JS assertions prove that gate, and the server
assertions run the real bound routes over tmp roots.
"""

import http.client
import json
import re

from scripts.generate import generate
from scripts.runner.schedule import activate
from scripts.serve import plan_loop
from scripts.serve import server as serve_server
from scripts.store import store
from vault.design.templates import app_shell

from tests.serve.test_app_shell import _complete_profile_readings, _seed_complete_profile
from tests.serve.test_credential_onboarding_ui import _profile_region
from tests.serve.test_plan_loop import (
    _post_plan_loop,
    _post_plan_loop_ctype,
    _serve_in_thread,
)

_SCHEDULE_ITEM = "plan-update-cadence"


# --------------------------------------------------------------------------- #
# fixtures / helpers
# --------------------------------------------------------------------------- #
def _surface_b():
    """The unlocked full shell: a complete profile keeps `screen-profile` (Surface B) in the body."""
    return app_shell.render(_complete_profile_readings())


def _plan_window(html):
    """The `_planUpdate` trigger handler's source window (the ordering-assertion scope, T4-A1 idiom)."""
    fi = html.find("function _planUpdate")
    assert fi != -1, "no _planUpdate trigger handler in the rendered SPA"
    end = html.find("\nfunction ", fi + 1)
    return html[fi:end if end != -1 else fi + 1200]


def _build(tmp_path, **kw):
    """A loopback-bound server over tmp roots; return (srv, port). Seeds nothing (routes seed their own)."""
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", **kw,
    )
    return srv, srv.server_address[1]


def _post_schedule(port, cadence, content_type="application/json"):
    """POST `{cadence}` to `/settings/schedule` with an explicit Content-Type; return (status, body)."""
    body = json.dumps({"cadence": cadence}).encode("utf-8")
    headers = {"Content-Length": str(len(body))}
    if content_type is not None:
        headers["Content-Type"] = content_type
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/settings/schedule", body=body, headers=headers)
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    conn.close()
    return resp.status, (json.loads(raw) if raw else {})


def _get_schedule(port):
    """GET `/settings/schedule`; return (status, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", "/settings/schedule")
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    conn.close()
    return resp.status, (json.loads(raw) if raw else {})


def _append_spy(monkeypatch):
    """Spy on `store.append` (call-through); return the recorded (item, reading) call list."""
    calls = []
    real = store.append

    def spy(item, reading, root=store.DEFAULT_ROOT):
        calls.append((item, reading))
        return real(item, reading, root)

    monkeypatch.setattr(store, "append", spy)
    return calls


# --------------------------------------------------------------------------- #
# AC-1 -- one re-gen per explicit request (count regenerate, NOT dispatch calls)
# --------------------------------------------------------------------------- #
def test_ac1_one_regenerate_per_request(tmp_path, monkeypatch):
    """AC-1: a POST to `/plan-loop` drives `plan_loop.regenerate` EXACTLY ONCE; 0 with no request.

    Counts `regenerate` invocations (a wrapped-fn counter) — NOT dispatch calls (~8/tick). BOTH loop
    seams are injected so the counter is reached past the `or`-degrade guard. Falsifier: a double-fire
    -> count 2 -> the `== 1` assertion REDs; a fire with no request -> the `== 0` assertion REDs.
    """
    calls = {"n": 0}

    def counting(*a, **k):
        calls["n"] += 1
        return {"results": {}, "degraded": True, "reason": "counted"}

    monkeypatch.setattr(plan_loop, "regenerate", counting)
    srv, port = _build(tmp_path, loop_dispatch=lambda *a, **k: {}, loop_deid_client=object())
    _serve_in_thread(srv)
    try:
        assert calls["n"] == 0, "regenerate fired with no request"
        status, _ = _post_plan_loop(port)
        assert status == 200, f"POST /plan-loop returned {status}, expected 200"
        assert calls["n"] == 1, f"regenerate invoked {calls['n']} times for one request (expected 1)"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# AC-1b -- the degraded state is honest, never a fake success (the T4-A1 class)
# --------------------------------------------------------------------------- #
def test_ac1b_success_render_gated_on_not_degraded():
    """AC-1b: the trigger's success render sits BEHIND `!d.degraded && !d.error`.

    Since `loop_dispatch = None`, every `/plan-loop` POST returns `{degraded:true}` — so the success
    text MUST be gated on `!d.degraded` (the degraded body renders the honest not-live affordance, NOT
    "Plan updated"). Ordering assertion (the T4-A1 idiom): the `d.degraded` gate precedes the success
    token; the degraded branch carries the not-live copy; the `.catch` carries a failure affordance
    (no empty catch). Falsifier: gate success on `r.ok`/unconditionally -> the `d.degraded` gate
    vanishes ahead of the success token -> RED.
    """
    win = _plan_window(_surface_b())
    degraded_i = win.find("d.degraded")
    error_i = win.find("d.error")
    success_i = win.find("Plan updated")
    assert degraded_i != -1, "the trigger does not gate on d.degraded (paints success on any 200)"
    assert error_i != -1, "the trigger does not also gate on d.error"
    assert success_i != -1, "the trigger has no success-render text"
    assert degraded_i < success_i, "the success render is not gated behind the !d.degraded check"
    # the degraded branch renders the honest not-yet-available copy, keyed on the reason
    assert "Automatic plan updates are not live yet" in win, (
        "the degraded branch has no honest not-yet-available affordance"
    )
    # no empty .catch (the T4-A1 lesson): the failure path surfaces a retry affordance
    assert "Could not reach the app" in win, "the trigger .catch has no failure affordance"


# --------------------------------------------------------------------------- #
# AC-2 -- the "Plan updates" section renders (co-located positive + negative)
# --------------------------------------------------------------------------- #
def test_ac2_plan_updates_section_renders():
    """AC-2: `screen-profile` carries the mockup's enumerated Plan-updates elements (Off default `on`).

    NOTE the deliberate mockup deviation (for the Tier-3 Design agent): the mockup's `updatePlan()`
    paints an unconditional "Plan updated" success after a 1.4s setTimeout — a prototype fiction. The
    build renders the honest degraded state instead (AC-1b). That is not infidelity.
    Falsifier: drop any enumerated element -> RED.
    """
    region = _profile_region(_surface_b())
    assert "Plan updates" in region, "no 'Plan updates' seclab"
    assert "Update my plan now" in region, "no 'Update my plan now' trigger button"
    assert "Automatic updates" in region, "no 'Automatic updates' klab"
    assert "Coming soon" in region, "no 'Coming soon' pill"
    # the Off/Weekly/Daily radio trio, Off default-`on`
    for cadence in ("off", "weekly", "daily"):
        assert f'data-sched="{cadence}"' in region, f"no {cadence} schedule radio"
    off = re.search(r'<label class="([^"]*)"[^>]*data-sched="off"', region)
    assert off is not None and "on" in off.group(1).split(), "the Off radio is not default-selected (`on`)"
    weekly = re.search(r'<label class="([^"]*)"[^>]*data-sched="weekly"', region)
    assert weekly is not None and "on" not in weekly.group(1).split(), "Weekly is default-selected"
    # co-located negative: the mockup's prototype-fiction success is NOT the rendered default state
    assert "Plan updated · just now" not in region, (
        "the section renders the prototype-fiction success as static markup (must be JS-gated behind !d.degraded)"
    )


# --------------------------------------------------------------------------- #
# AC-3 -- the schedule setting persists the intent (source:settings, last-by-timepoint)
# --------------------------------------------------------------------------- #
def test_ac3_schedule_persists_intent(tmp_path, monkeypatch):
    """AC-3: POST records a conformant `plan-update-cadence` reading (source `settings`); GET reads back
    the LAST by timepoint; unset defaults to `off`; an unknown cadence is rejected 4xx AND 0-appended.
    Falsifier: the reading absent / the default wrong / an unknown cadence appended -> RED.
    """
    calls = _append_spy(monkeypatch)
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        # unset -> default off
        gstatus, gbody = _get_schedule(port)
        assert gstatus == 200 and gbody.get("cadence") == "off", f"unset default not off: {gbody}"

        # POST weekly -> a conformant reading lands, source settings
        pstatus, _ = _post_schedule(port, "weekly")
        assert pstatus == 200, f"POST weekly returned {pstatus}"
        assert len(calls) == 1, f"POST weekly appended {len(calls)} readings (expected 1)"
        item, reading = calls[0]
        assert item == _SCHEDULE_ITEM
        assert reading["item"] == _SCHEDULE_ITEM and reading["value"] == "weekly"
        assert reading["source"] == "settings", f"reading source is {reading['source']!r}, not 'settings'"
        assert "timepoint" in reading, "the reading carries no timepoint"

        # GET reads the last-by-timepoint
        _, gbody = _get_schedule(port)
        assert gbody.get("cadence") == "weekly", f"GET after weekly returned {gbody}"

        # a second pick supersedes (last-by-timepoint)
        _post_schedule(port, "off")
        _, gbody = _get_schedule(port)
        assert gbody.get("cadence") == "off", f"GET after off returned {gbody}"

        # the store carries the append-only cadence history (2 series points)
        rows = store.read(_SCHEDULE_ITEM, root=tmp_path / "store")
        assert [r["value"] for r in rows] == ["weekly", "off"], f"cadence history wrong: {rows}"

        # unknown cadence -> 4xx AND 0 further append
        before = len(calls)
        ustatus, _ = _post_schedule(port, "hourly")
        assert 400 <= ustatus < 500, f"unknown cadence returned {ustatus}, expected a 4xx"
        assert len(calls) == before, "an unknown cadence still appended a reading"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# AC-4 -- Daily inert + the real scheduler untouched (the behavioral guard)
# --------------------------------------------------------------------------- #
def test_ac4_daily_inert_scheduler_untouched(tmp_path, monkeypatch):
    """AC-4: selecting Daily records the intent but arms NO real runner.

    The self-standing behavioral guard (NOT a vacuous enable-spy — server.py imports activate 0
    times): after POST daily, the REAL scheduler state for DAILY_MONITOR_LABEL is untouched
    (`active_entry_count == 0` / status DISABLED), AND `activate.enable` is never called
    (belt-and-braces). Falsifier: an `enable(DAILY_MONITOR_LABEL)` call -> active_entry_count goes
    nonzero -> RED.
    """
    enabled = []
    monkeypatch.setattr(activate, "enable", lambda *a, **k: enabled.append((a, k)))
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        pstatus, pbody = _post_schedule(port, "daily")
        assert pstatus == 200, f"POST daily returned {pstatus}"
        assert pbody.get("cadence") == "daily", f"POST daily body {pbody}"
        # the intent is recorded ...
        rows = store.read(_SCHEDULE_ITEM, root=tmp_path / "store")
        assert rows and rows[-1]["value"] == "daily", "the daily intent was not recorded"
        # ... but NOTHING armed a daily runner
        assert activate.active_entry_count(activate.DAILY_MONITOR_LABEL) == 0, (
            "a real daily scheduler entry was armed (Daily must be inert)"
        )
        assert activate.status(activate.DAILY_MONITOR_LABEL)["state"] == "DISABLED"
        assert enabled == [], "activate.enable was called (Daily must arm nothing)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_ac4_render_states_not_live():
    """AC-4 (render arm): the rendered UI states scheduled auto-runs are not yet live.

    The "Coming soon" pill + the note copy communicate that manual is available now and scheduled
    updates are not. Falsifier: drop the not-live copy -> RED.
    """
    region = _profile_region(_surface_b())
    assert "Coming soon" in region, "no 'Coming soon' pill"
    assert "Scheduled updates are coming soon" in region, "the note does not state scheduled updates are not live"


# --------------------------------------------------------------------------- #
# AC-5 -- CSRF 415-before-any-spend, mutation-proven (LOAD-BEARING)
# --------------------------------------------------------------------------- #
def test_ac5a_plan_loop_textplain_refused_415(tmp_path, monkeypatch):
    """AC-5(a): a cross-site `text/plain` POST to `/plan-loop` is refused 415 BEFORE any work.

    The RED-capable falsifier is the STATUS: with BOTH seams injected, dropping the gate flips the
    text/plain POST to a 200 degraded body AND reaches regenerate. Asserts 415 AND 0 regenerate
    invocations on the refused path (non-vacuous because both seams are present).
    """
    calls = {"n": 0}
    monkeypatch.setattr(plan_loop, "regenerate", lambda *a, **k: calls.__setitem__("n", calls["n"] + 1) or {})
    srv, port = _build(tmp_path, loop_dispatch=lambda *a, **k: {}, loop_deid_client=object())
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop_ctype(port, "text/plain")
        assert status == 415, f"text/plain /plan-loop returned {status}, expected 415"
        assert calls["n"] == 0, "regenerate fired on the CSRF-refused path (gate did not precede the seam)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_ac5a_ui_trigger_posts_plan_loop():
    """AC-5(a) render arm: the UI trigger POSTs `/plan-loop` (reuses the routed CSRF-gated loop, not a
    new spend route). Falsifier: the trigger fetches a different/new route -> RED."""
    html = _surface_b()
    assert "fetch('/plan-loop'" in html, "the trigger does not POST the routed /plan-loop"


def test_ac5b_schedule_textplain_refused_415_zero_append(tmp_path, monkeypatch):
    """AC-5(b), LOAD-BEARING: a cross-site `text/plain` POST to `/settings/schedule` is refused 415 with
    `store.append` invoked 0 times (no early-return sits between the gate and the append, so this is
    non-vacuous). Falsifier: drop the CSRF gate -> the text/plain POST appends -> RED.
    """
    calls = _append_spy(monkeypatch)
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        status, _ = _post_schedule(port, "weekly", content_type="text/plain")
        assert status == 415, f"text/plain /settings/schedule returned {status}, expected 415"
        assert len(calls) == 0, "the CSRF-refused text/plain POST still appended a reading"
        assert store.read(_SCHEDULE_ITEM, root=tmp_path / "store") == [], "a reading landed on the 415 path"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# AC-7 -- inline-only emit + the fetch-allowlist admission
# --------------------------------------------------------------------------- #
def test_ac7_inline_emit_carries_plan_updates(tmp_path):
    """AC-7 (inline arm): `generate.run('app')` returns a written Path (no off-file `ValueError`) with the
    Plan-updates section present. The authoritative inline-asset proof is the real emit, not a grep."""
    _seed_complete_profile(tmp_path / "store")
    path = generate.run(
        "app", _root=tmp_path / "store", _out_dir=tmp_path / "out",
        _dna_root=tmp_path / "dna", _labs_root=tmp_path / "labs",
    )
    assert path.exists() and path.is_file(), "generate.run('app') did not write the SPA"
    html = path.read_text()
    assert "Plan updates" in html, "the emitted SPA carries no Plan-updates section"
    assert "fetch('/settings/schedule'" in html, "the emitted SPA does not fetch /settings/schedule"


def test_ac7_both_new_targets_in_allowlist_sinks():
    """AC-7 (allowlist arm): `/plan-loop` + `/settings/schedule` are admitted to BOTH allowlist sinks in
    test_app_shell.py (exact literals, no prefix loosening). This mirror-asserts the admission so a
    reverted admission REDs here too. Falsifier: drop either literal from either sink -> RED."""
    from tests.serve import test_app_shell as tas

    for target in ("/plan-loop", "/settings/schedule"):
        assert target in tas._KNOWN_LOOPBACK, f"{target} not admitted to _KNOWN_LOOPBACK"
    # the same-origin assertion-set sink is inline in the test body: assert the source carries the literal
    import inspect

    src = inspect.getsource(tas.test_spa_fetch_targets_are_all_same_origin_loopback)
    for target in ("/plan-loop", "/settings/schedule"):
        assert f'"{target}"' in src, f"{target} not admitted to the same-origin allowlist assertion set"
