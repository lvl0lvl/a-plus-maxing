"""Explicit operator confirm/decline act + `/confirm-plan-change` serve route (ADR-0040-T4).

T4 is the terminal, fail-closed release surface of the large-change HOLD. A materially-large
re-gen writes a `pending` `plan-confirm::<domain>` pointer (T3) that T2's read-side skip honors,
so the held plan NEVER stands until the operator explicitly confirms. This task adds the operator
ACT — `confirm.confirm_plan_change(domain, plan_date, decision, *, root, tailor_client=None)` —
that flips that pointer and fires the deferred care-lane tailoring seam, plus the state-changing
`POST /confirm-plan-change` route that fronts it.

Cycle 1 (the ACT, driven directly over a temp store + a fixture `tailor_client`): AC-1 (confirm
promotes; a present-but-invalid decision token fails closed with a `ValueError`, 0 flip, 0
tailoring), AC-2 (tailors once on the pending->confirmed TRANSITION; a repeat confirm short-circuits
-> converse-count == 1 across two confirms, measured at the MODEL-CALL level), AC-3 (fail-closed on
decline / unactioned pending — the reader never stands, the unconfirmed reading stays in append-only
history), AC-4 (a late confirm `plan_date < today` is refused past the staleness bound — the stale
pending is GC'd, all three readers hold the stale date, tailoring keys on `plan_date`), AC-6 (per-
domain confirm resolves independently + the confirm re-fires with the UNION of currently-confirmed
held domains so a prior confirmed domain's fresh-rendered tailored section is never clobbered).

Cycle 2 (the ROUTE, mirroring `test_extract_confirm.py`): AC-5 distinct-branch dispatch + the
CSRF/415 content-type gate + the 413 Content-Length ceiling + the decision-enum 400 + malformed-body
degrade — each over a SEEDED `pending` pointer so the "0 mutation" assertion is non-vacuous.

MOCK/FIXTURE-tested at 0 live spend: the fixture `tailor_client` is a deterministic echo client
(no live API, no key, no socket); every store is a `tmp_path` temp root; the care-lane render is
redirected into a gitignored temp out-dir. 0 real operator PII (synthetic tokens only).
"""

import datetime
import http.client
import io
import json
import threading
from email.message import Message
from pathlib import Path

import pytest

from scripts.plan import horizons
from scripts.serve import confirm
from scripts.serve import plan_loop
from scripts.serve import server as serve_server
from scripts.store import plan_confirm, plan_schema, store

# The tailoring artifact idioms (fixture presentation client + gitignored render seams, 0 spend) —
# reused from the tailoring component test, the established convention for driving the care-lane
# render into a gitignored temp out-dir.
from tests.plan.test_tailoring import _EchoClient, _gitignored_out, _synth_profile

REPO_ROOT = Path(__file__).resolve().parents[2]

# `confirm_plan_change` compares `plan_date` against the WALL-CLOCK today for the standing-window /
# late-confirm split, so an in-window fixture date must be today's real date (equal is in-window).
TODAY = datetime.date.today()
TODAY_STR = TODAY.isoformat()
STALE_STR = "2020-01-01"  # unambiguously < today -> the AC-4 late-confirm date

# Per-domain valid plan documents (the `plan_schema` per-domain validators the seed passes).
_WORKOUT_PLAN = {"exercises": [{"name": "Squat", "sets": 5}]}
_NUTRITION_PLAN = {
    "calorie_goal": 2000,
    "macros": {"protein": 150, "carbs": 200, "fat": 60},
    "meals": [{"name": "Breakfast"}],
}
_PLANS = {"workout": _WORKOUT_PLAN, "nutrition": _NUTRITION_PLAN}


def _seed_pending(root, domain, plan_date):
    """Record a `plan::<domain>` reading for `plan_date` and mark it `pending` (a held re-gen)."""
    plan_schema.record_plan(domain, _PLANS[domain], plan_date, "specialist", root)
    plan_confirm.mark_pending(domain, plan_date, root)


def _install_seam_spy(monkeypatch, tmp_path):
    """Redirect `_post_promote_tailoring`'s render into a gitignored temp out-dir; capture its sets.

    The confirm act calls `plan_loop._post_promote_tailoring(...)` WITHOUT render seams (production
    renders to the real default). Under test we spy that call to (a) capture the `promoted_plan` set
    each fire carried (the AC-6b union falsifier) and (b) forward the SAME fixture tailor_client into
    the real seam WITH gitignored temp seams so the artifact write is contained. Mirrors T3's
    `spy_seam`. Returns (seen, out_dir).
    """
    repo, out = _gitignored_out(tmp_path)
    seams = {"out_dir": out, "_today": TODAY,
             "_profile_paths": _synth_profile(tmp_path), "_repo_root": repo}
    seen = []
    real_seam = plan_loop._post_promote_tailoring

    def spy_seam(promoted_plan, render_target, *, tailor_client=None, _tailor_seams=None, **kwargs):
        seen.append(set(promoted_plan))
        return real_seam(promoted_plan, render_target,
                         tailor_client=tailor_client, _tailor_seams=seams, **kwargs)

    monkeypatch.setattr(plan_loop, "_post_promote_tailoring", spy_seam)
    return seen, out


# --------------------------------------------------------------------------- #
# Cycle 1 — the confirm/decline operator ACT
# --------------------------------------------------------------------------- #


def test_confirm_promotes_and_reader_stands(tmp_path, monkeypatch):
    """AC-1 (confirm promotes): an in-window `confirmed` flips the pointer and the reader STANDS.

    Over a seeded `pending` pointer dated today, `confirm_plan_change(..., "confirmed")` sets the
    pointer `confirmed` (`decision_for == "confirmed"`) AND `read_plan` no longer skips it —
    `state is None`, the confirmed plan present.
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", TODAY_STR)
    _install_seam_spy(monkeypatch, tmp_path)
    confirm.confirm_plan_change("workout", TODAY_STR, "confirmed", root=root, tailor_client=_EchoClient())

    assert plan_confirm.decision_for("workout", TODAY_STR, root) == plan_confirm.DECISION_CONFIRMED
    resolved = plan_schema.read_plan("workout", TODAY_STR, root)
    assert resolved["state"] is None and resolved["plan"] is not None, (
        f"the confirmed plan did not stand: {resolved}"
    )


def test_bad_decision_token_fails_closed(tmp_path):
    """AC-1b (decision-enum fail-closed, Security F1): a present-but-invalid token raises, 0 flip/tailor.

    `confirm_plan_change(..., "approved")` — a present decision token not in {confirmed, declined} —
    raises `ValueError`, does NOT flip the pointer (`decision_for` stays `"pending"`), and fires 0
    tailoring (converse call-count 0). Failing-capable: a two-branch `else: confirm` default-allow
    GREEN would flip the pointer to `confirmed`.
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", TODAY_STR)
    client = _EchoClient()
    with pytest.raises(ValueError):
        confirm.confirm_plan_change("workout", TODAY_STR, "approved", root=root, tailor_client=client)
    assert plan_confirm.decision_for("workout", TODAY_STR, root) == plan_confirm.DECISION_PENDING
    assert client.calls == [], "an invalid decision token fired tailoring (default-allow leak)"


def test_confirm_tailors_once_then_reconfirm_short_circuits(tmp_path, monkeypatch):
    """AC-2 (tailors once, transition short-circuit — QA T4-1 / Architect F1): converse-count == 1.

    The first confirm fires the deferred tailoring exactly once on the pending->confirmed TRANSITION
    (converse call-count 1). A SECOND confirm of the SAME (domain, plan_date) short-circuits
    (`decision_for` already `"confirmed"`) and fires 0 ADDITIONAL converse — converse-count == 1
    across two confirms, measured at the MODEL-CALL level. Failing-capable: without the transition
    short-circuit the second confirm re-fires converse (count == 2).
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", TODAY_STR)
    seen, _ = _install_seam_spy(monkeypatch, tmp_path)
    client = _EchoClient()

    confirm.confirm_plan_change("workout", TODAY_STR, "confirmed", root=root, tailor_client=client)
    assert len(client.calls) == 1, "the first confirm did not fire tailoring exactly once"

    confirm.confirm_plan_change("workout", TODAY_STR, "confirmed", root=root, tailor_client=client)
    assert len(client.calls) == 1, (
        "the repeat confirm re-fired the metered tailoring pass (no transition short-circuit)"
    )
    assert seen == [{"workout"}], f"the tailoring seam fired more than once on the transition: {seen}"


def test_decline_and_pending_never_stand(tmp_path):
    """AC-3 (fail-closed on decline / unactioned pending — Risk Decision §5): the reader never stands.

    A `declined` decision leaves the held re-gen non-standing (`read_plan` walks back to the PRIOR
    standing plan, `NO_PLAN_TODAY`, plan None — never the held plan) with 0 tailored artifact, and the
    unconfirmed `plan::workout` reading STAYS in append-only history (auditable, never standing). An
    unactioned `pending` pointer (no confirm call at all) likewise never stands.
    """
    declined_root = tmp_path / "declined"
    # A realistic large-change hold REPLACES a prior standing plan (dated earlier, no pointer -> it
    # stands); the held today re-gen is the swap awaiting confirm.
    yesterday = (TODAY - datetime.timedelta(days=1)).isoformat()
    plan_schema.record_plan("workout", _WORKOUT_PLAN, yesterday, "specialist", declined_root)
    _seed_pending(declined_root, "workout", TODAY_STR)
    client = _EchoClient()
    confirm.confirm_plan_change("workout", TODAY_STR, "declined", root=declined_root, tailor_client=client)

    resolved = plan_schema.read_plan("workout", TODAY_STR, declined_root)
    assert resolved["plan"] is None, f"a declined re-gen surfaced a plan: {resolved}"
    assert resolved["state"] == plan_schema.NO_PLAN_TODAY, f"a declined re-gen stood: {resolved}"
    assert resolved["plan_date"] == yesterday, "the held/declined plan walked back to today"
    assert client.calls == [], "a declined domain was tailored (raw egress past the confirm gate)"
    held = [r for r in store.read("plan::workout", root=declined_root) if r["timepoint"] == TODAY_STR]
    assert len(held) == 1, "the unconfirmed reading was not retained in append-only history"

    # An unactioned pending pointer (no confirm) never stands either.
    pending_root = tmp_path / "pending"
    _seed_pending(pending_root, "workout", TODAY_STR)
    only_pending = plan_schema.read_plan("workout", TODAY_STR, pending_root)
    assert only_pending["plan"] is None
    assert only_pending["state"] in (plan_schema.NO_PLAN, plan_schema.NO_PLAN_TODAY)


def test_late_confirm_refused_all_readers_hold(tmp_path):
    """AC-4 (late-confirm defined semantics — Risk OQ-7 / AR-008): a stale confirm is refused.

    A `confirm_plan_change(..., "confirmed")` where `plan_date < today` is REFUSED past the staleness
    bound — the stale pending is GC'd (`decision_for == "declined"`), and all three standing-plan
    readers hold the stale date: `read_plan` -> `NO_PLAN_TODAY`, `window_block` (7 AND 30) never
    surfaces the stale plan, and 0 tailoring fires (the deferred tailoring keys on `plan_date`, so no
    past-dated section renders as the current day).
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", STALE_STR)
    client = _EchoClient()
    confirm.confirm_plan_change("workout", STALE_STR, "confirmed", root=root, tailor_client=client)

    assert plan_confirm.decision_for("workout", STALE_STR, root) == plan_confirm.DECISION_DECLINED, (
        "a late confirm was honored instead of GC'd to declined"
    )
    resolved = plan_schema.read_plan("workout", STALE_STR, root)
    assert resolved["plan"] is None, f"a stale confirm surfaced a plan: {resolved}"
    assert resolved["state"] in (plan_schema.NO_PLAN, plan_schema.NO_PLAN_TODAY)
    for span in (7, 30):
        block = horizons.window_block("workout", root, STALE_STR, span)
        assert block is None or block["plan_date"] != STALE_STR, (
            f"span {span}: the stale held plan surfaced in the window block: {block}"
        )
    assert client.calls == [], "a late confirm fired tailoring (a past-dated section rendered as today)"


def test_per_domain_confirm_resolves_independently(tmp_path):
    """AC-6a (per-domain confirm — OQ-3, resolver): each domain resolves independently, no stranding.

    Given a held re-gen marking "workout" AND "nutrition" `pending` (both dated today), confirming
    "workout" and declining "nutrition" leaves `read_plan("workout")` standing and
    `read_plan("nutrition")` at `NO_PLAN_TODAY` — no partial-confirm stranding.
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", TODAY_STR)
    _seed_pending(root, "nutrition", TODAY_STR)
    # tailor_client=None -> the tailoring seam stays a pass-through (0 render), so this asserts the
    # RESOLVER independence only.
    confirm.confirm_plan_change("workout", TODAY_STR, "confirmed", root=root)
    confirm.confirm_plan_change("nutrition", TODAY_STR, "declined", root=root)

    workout = plan_schema.read_plan("workout", TODAY_STR, root)
    nutrition = plan_schema.read_plan("nutrition", TODAY_STR, root)
    assert workout["state"] is None and workout["plan"] is not None, "the confirmed domain did not stand"
    assert nutrition["plan"] is None, "the declined domain stood (partial-confirm stranding)"
    assert nutrition["state"] in (plan_schema.NO_PLAN, plan_schema.NO_PLAN_TODAY)


def test_per_domain_confirm_retains_both_tailored_sections(tmp_path, monkeypatch):
    """AC-6b (per-domain confirm — Architect F2, tailoring composition): union re-fire, no clobber.

    Confirming "workout" THEN "nutrition" (both dated today) re-fires the deferred tailoring with the
    UNION of currently-confirmed held domains, so the fresh (replace-not-accrete) maintained artifact
    carries BOTH tailored sections. Failing-capable: a per-domain re-fire carrying only the just-
    confirmed domain would render fresh and DROP "workout"'s section (the second seam set would be
    {"nutrition"} and `data-domain='workout'` would be absent from the artifact).
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", TODAY_STR)
    _seed_pending(root, "nutrition", TODAY_STR)
    seen, out = _install_seam_spy(monkeypatch, tmp_path)
    client = _EchoClient()

    confirm.confirm_plan_change("workout", TODAY_STR, "confirmed", root=root, tailor_client=client)
    confirm.confirm_plan_change("nutrition", TODAY_STR, "confirmed", root=root, tailor_client=client)

    assert seen[0] == {"workout"}, f"the first confirm did not fire with just workout: {seen}"
    assert seen[1] == {"workout", "nutrition"}, (
        f"the second confirm did not re-fire with the confirmed UNION (clobber risk): {seen}"
    )
    text = (out / "maintained.html").read_text(encoding="utf-8")
    assert "data-domain='workout'" in text, "the prior confirmed domain's section was clobbered"
    assert "data-domain='nutrition'" in text, "the just-confirmed domain's section is missing"


# --------------------------------------------------------------------------- #
# Concurrency — TOCTOU double-spend under ThreadingHTTPServer (bead hgnt, P2)
# --------------------------------------------------------------------------- #


def _counting_seam(fires, fires_guard):
    """A `_post_promote_tailoring` stand-in that only COUNTS fires (0 render, 0 converse).

    Each fire = one metered care-lane converse in production, so the fire count IS the
    double-spend observable. Records `set(promoted_plan)` under a lock (the two request threads
    call it concurrently); never forwards to the real seam, so no `tailoring.tailor` / model call.
    """
    def seam(promoted_plan, render_target, *, tailor_client=None, plan_date=None, **kwargs):
        with fires_guard:
            fires.append(set(promoted_plan))
        return None
    return seam


def _barrier_on_first_decision_for(monkeypatch, barrier):
    """Rendezvous BOTH confirm threads on their FIRST `decision_for` (the L200 transition check).

    Nothing calls `decision_for` before the transition check, so each thread's first call IS that
    check — barriering there guarantees both threads read `pending` before EITHER calls
    `set_decision` (the exact TOCTOU window). Subsequent `decision_for` calls (the union build, any
    `read_plan`-internal resolve) pass straight through. Returns the un-patched `decision_for` so the
    test's own final state read bypasses the barrier. The barrier wait carries a timeout so the
    lock-serialized (fixed) path cannot deadlock: only one thread is ever inside the critical
    section, so its lone wait times out and it proceeds; the other thread is still lock-blocked.
    """
    real_decision_for = plan_confirm.decision_for
    checked = set()
    checked_guard = threading.Lock()

    def barriered(domain, plan_date, root):
        result = real_decision_for(domain, plan_date, root)
        tid = threading.get_ident()
        with checked_guard:
            first = tid not in checked
            checked.add(tid)
        if first:
            try:
                barrier.wait(timeout=2.0)
            except threading.BrokenBarrierError:
                pass  # the fixed path: the solo thread times out and proceeds alone (no deadlock)
        return result

    monkeypatch.setattr(plan_confirm, "decision_for", barriered)
    return real_decision_for


def test_concurrent_same_domain_confirm_tailors_exactly_once(tmp_path, monkeypatch):
    """TOCTOU double-spend (bead hgnt): two concurrent same-(domain, plan_date) confirms tailor ONCE.

    `ThreadingHTTPServer` dispatches concurrent confirms on separate threads in ONE process. Two
    confirms of the SAME held `(domain, plan_date)` can both pass the pending->confirmed TRANSITION
    check (both read `pending`) BEFORE either flips, so both flip and both fire the metered
    `_post_promote_tailoring` seam -> a DOUBLE converse (defeats ADR-0040 AC-2 converse-count == 1).
    A `Barrier(2)` on each thread's first `decision_for` FORCES that interleave deterministically; a
    counting seam records each fire. Failing-capable: WITHOUT the per-root lock both threads fire
    (2). WITH it the second thread short-circuits on the flipped pointer (1).
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", TODAY_STR)

    fires, fires_guard = [], threading.Lock()
    monkeypatch.setattr(plan_loop, "_post_promote_tailoring", _counting_seam(fires, fires_guard))
    real_decision_for = _barrier_on_first_decision_for(monkeypatch, threading.Barrier(2))

    errors = []

    def worker():
        try:
            confirm.confirm_plan_change(
                "workout", TODAY_STR, "confirmed", root=root, tailor_client=_EchoClient())
        except Exception as exc:  # a worker raise -> surfaced as a test failure in the main thread
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)

    assert not any(thread.is_alive() for thread in threads), "a confirm worker hung (deadlock?)"
    assert errors == [], f"a confirm worker raised: {errors!r}"
    assert real_decision_for("workout", TODAY_STR, root) == plan_confirm.DECISION_CONFIRMED
    assert len(fires) == 1, (
        f"the metered tailoring seam fired {len(fires)}x for two concurrent same-domain confirms "
        f"(TOCTOU double-spend); expected exactly 1"
    )


def test_concurrent_cross_domain_confirm_no_union_clobber(tmp_path, monkeypatch):
    """TOCTOU union clobber (bead hgnt, AC-6b): concurrent different-domain confirms keep BOTH sections.

    The confirmed-union build reads EVERY confirmed domain, so two concurrent confirms of DIFFERENT
    domains race it: a confirm can build its union BEFORE the other's flip is visible yet fire the
    fresh (replace-not-accrete) render LAST, clobbering the other domain's just-confirmed section.
    Role-keyed ordering gates force exactly that tail deterministically — the leader (workout) builds a
    stale `{workout}` union, the follower (nutrition) then flips + fires the full union, and the
    leader's stale fire lands LAST. Failing-capable: WITHOUT the per-root lock the last fire carries
    only `{workout}` (nutrition clobbered); WITH it the two confirms serialize so the last fire carries
    the full `{workout, nutrition}` union. The gate waits carry a timeout so the lock-serialized path
    (where the follower is lock-blocked and can never fire) cannot deadlock.
    """
    root = tmp_path / "store"
    _seed_pending(root, "workout", TODAY_STR)
    _seed_pending(root, "nutrition", TODAY_STR)

    fires, fires_guard = [], threading.Lock()
    leader_built, follower_fired = threading.Event(), threading.Event()

    real_set_decision = plan_confirm.set_decision

    def gated_set_decision(domain, plan_date, decision, root):
        # The follower flips only AFTER the leader has built its (deliberately stale) union, so the
        # leader's union never sees nutrition. The leader flips immediately.
        if threading.current_thread().name == "follower":
            leader_built.wait(timeout=2.0)
        return real_set_decision(domain, plan_date, decision, root)

    def ordering_seam(promoted_plan, render_target, *, tailor_client=None, plan_date=None, **kwargs):
        domains = set(promoted_plan)
        if threading.current_thread().name == "leader":
            leader_built.set()               # the leader's union (L208-213) is already built
            follower_fired.wait(timeout=2.0)  # hold the leader's stale fire until the follower fired
            with fires_guard:
                fires.append(domains)
        else:
            with fires_guard:
                fires.append(domains)
            follower_fired.set()
        return None

    monkeypatch.setattr(plan_confirm, "set_decision", gated_set_decision)
    monkeypatch.setattr(plan_loop, "_post_promote_tailoring", ordering_seam)

    errors = []

    def worker(domain):
        try:
            confirm.confirm_plan_change(
                domain, TODAY_STR, "confirmed", root=root, tailor_client=_EchoClient())
        except Exception as exc:
            errors.append(exc)

    threads = [
        threading.Thread(target=worker, args=("workout",), name="leader"),
        threading.Thread(target=worker, args=("nutrition",), name="follower"),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)

    assert not any(thread.is_alive() for thread in threads), "a confirm worker hung (deadlock?)"
    assert errors == [], f"a confirm worker raised: {errors!r}"
    assert len(fires) == 2, f"expected one fire per domain confirm, got {fires!r}"
    assert fires[-1] == {"workout", "nutrition"}, (
        f"the last tailoring fire carried a stale union {fires[-1]!r}, clobbering the other confirmed "
        f"domain's section (TOCTOU union race); expected the full {{workout, nutrition}} union"
    )


# --------------------------------------------------------------------------- #
# Cycle 2 — the POST /confirm-plan-change serve route (CSRF/415 + 413 + enum + dispatch)
# --------------------------------------------------------------------------- #


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _server_with_confirm(tmp_path):
    """Build a loopback server over tmp roots (production-un-wired tailor seam -> 0 spend)."""
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold",
    )
    return srv, srv.server_address[1]


def _post(port, path, payload, *, content_type="application/json"):
    """POST `payload` (JSON-encoded dict/list, or raw bytes) to `path`; return (status, parsed-or-raw).

    `content_type=None` omits the `Content-Type` header entirely (the no-header CSRF case).
    """
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = json.dumps(payload).encode("utf-8") if isinstance(payload, (dict, list)) else payload
    headers = {} if content_type is None else {"Content-Type": content_type}
    conn.request("POST", path, body=body, headers=headers)
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    try:
        return resp.status, json.loads(text)
    except json.JSONDecodeError:
        return resp.status, text


def _drive_confirm_plan_change_inproc(store_root, *, content_type, content_length, body):
    """Drive `_do_confirm_plan_change` in-process (no socket); return the raw response bytes.

    Bypasses `BaseHTTPRequestHandler.__init__`'s socket setup so the oversize-Content-Length 413 path
    is exercised deterministically (declaring a huge Content-Length while rfile carries a tiny body has
    no connection-reset race here). Mirrors `test_extract_confirm._drive_confirm_inproc`.
    """
    bound = type("BoundIntakeRequestHandler", (serve_server.IntakeRequestHandler,),
                 {"store_root": store_root})
    handler = bound.__new__(bound)
    handler.path = "/confirm-plan-change"
    handler.command = "POST"
    handler.requestline = "POST /confirm-plan-change HTTP/1.1"
    handler.request_version = "HTTP/1.1"
    headers = Message()
    headers["Content-Type"] = content_type
    headers["Content-Length"] = str(content_length)
    handler.headers = headers
    handler.rfile = io.BytesIO(body)
    handler.wfile = io.BytesIO()
    handler._do_confirm_plan_change()
    return handler.wfile.getvalue()


def test_route_distinct_branch_dispatch(tmp_path):
    """AC-5 (distinct-branch dispatch): /confirm-plan-change reaches its own handler; unknown 404s.

    A valid JSON body flips the `plan-confirm::` pointer (only `confirm_plan_change` does that — its
    own handler), the sibling `/confirm-extraction` route still answers its own handler on the same
    server (a distinct branch), and an unknown POST still 404s (three bodies -> three distinct paths).
    """
    srv, port = _server_with_confirm(tmp_path)
    _serve_in_thread(srv)
    try:
        root = tmp_path / "store"
        _seed_pending(root, "workout", TODAY_STR)
        status, _ = _post(port, "/confirm-plan-change",
                          {"domain": "workout", "plan_date": TODAY_STR, "decision": "confirmed"})
        assert status == 200, f"/confirm-plan-change returned {status}, expected 200"
        assert plan_confirm.decision_for("workout", TODAY_STR, root) == plan_confirm.DECISION_CONFIRMED, (
            "the route did not reach confirm_plan_change (pointer not flipped)"
        )
        # The sibling /confirm-extraction still reaches its OWN handler (distinct branch, unaffected).
        ext_status, _ = _post(port, "/confirm-extraction", {"readings": []})
        assert ext_status == 200, f"/confirm-extraction stopped answering: {ext_status}"
        # An unknown POST still 404s.
        unk_status, _ = _post(port, "/not-a-route", {"x": 1})
        assert unk_status == 404, f"an unknown POST returned {unk_status}, expected 404"
    finally:
        srv.shutdown()
        srv.server_close()


def test_route_malformed_body_400_unflipped(tmp_path):
    """AC-5 (malformed / missing-field body): degrades 400 over the SEEDED pointer, 0 flip.

    A non-JSON body and a missing-field JSON body each answer a degraded non-2xx before any pointer
    flip — the seeded `pending` pointer stays `"pending"` (non-vacuous 0-mutation), the thread survives.
    """
    srv, port = _server_with_confirm(tmp_path)
    _serve_in_thread(srv)
    try:
        root = tmp_path / "store"
        _seed_pending(root, "workout", TODAY_STR)
        for bad in (b"not json at all{{{", {"domain": "workout"}):  # missing plan_date/decision
            status, resp = _post(port, "/confirm-plan-change", bad)
            assert status != 200, f"a malformed body returned {status} (accepted?)"
            assert plan_confirm.decision_for("workout", TODAY_STR, root) == plan_confirm.DECISION_PENDING, (
                f"a malformed body flipped the pointer: {bad!r}"
            )
        # The server survived — a well-formed confirm still lands on the same port.
        ok_status, _ = _post(port, "/confirm-plan-change",
                             {"domain": "workout", "plan_date": TODAY_STR, "decision": "confirmed"})
        assert ok_status == 200, "the handler died after malformed bodies"
    finally:
        srv.shutdown()
        srv.server_close()


def test_route_bad_decision_token_400_unflipped(tmp_path):
    """AC-5 (decision-enum reject, Security F1 route-level): `decision:"approved"` -> 400, 0 flip.

    A valid-JSON `application/json` body carrying a present-but-invalid `decision` returns 400 with the
    seeded pointer UNFLIPPED — the act-level `ValueError` degrades to a 400 via the same catch-and-
    degrade, never a default-allow flip to `confirmed`.
    """
    srv, port = _server_with_confirm(tmp_path)
    _serve_in_thread(srv)
    try:
        root = tmp_path / "store"
        _seed_pending(root, "workout", TODAY_STR)
        status, resp = _post(port, "/confirm-plan-change",
                          {"domain": "workout", "plan_date": TODAY_STR, "decision": "approved"})
        assert status == 400, f"a bad decision token returned {status}, expected 400"
        assert plan_confirm.decision_for("workout", TODAY_STR, root) == plan_confirm.DECISION_PENDING, (
            "a present-but-invalid decision token flipped the pointer (default-allow leak)"
        )
        # The error body echoes the route's OWN {domain, decision} shape (the 200 success shape), not
        # the sibling-copied `confirmed` key. Failing-capable: the old `{"confirmed": None}` body reds.
        assert "confirmed" not in resp, f"the error body carries the sibling-copied 'confirmed' key: {resp}"
        assert resp.get("domain", "MISSING") is None and resp.get("decision", "MISSING") is None, (
            f"the error body does not echo the route's domain/decision shape: {resp}"
        )
    finally:
        srv.shutdown()
        srv.server_close()


def test_route_text_plain_and_no_ctype_415_no_flip(tmp_path):
    """AC-5 / SEC-0040-01 (CSRF/415, FAILING-CAPABLE): text/plain AND no-Content-Type -> 415, 0 flip.

    A cross-site CORS-simple POST (`text/plain`, or NO `Content-Type` header) carrying a valid confirm
    body must be refused 415 BEFORE any body parse, with the seeded `pending` pointer NOT flipped.
    Failing-capable: drop the content-type gate and the `text/plain` `decision:"confirmed"` body flips
    the pointer to `confirmed`, reddening the 0-flip assertion.
    """
    srv, port = _server_with_confirm(tmp_path)
    _serve_in_thread(srv)
    try:
        root = tmp_path / "store"
        _seed_pending(root, "workout", TODAY_STR)  # a 415 never flips, so one seed covers both cases
        body = {"domain": "workout", "plan_date": TODAY_STR, "decision": "confirmed"}
        for ctype in ("text/plain", None):
            status, resp = _post(port, "/confirm-plan-change", body, content_type=ctype)
            assert status == 415, f"content-type {ctype!r} returned {status}, expected 415"
            assert plan_confirm.decision_for("workout", TODAY_STR, root) == plan_confirm.DECISION_PENDING, (
                f"a {ctype!r} confirm flipped the pointer (the CSRF gate was bypassed)"
            )
            # The 415 body echoes the route's OWN {domain, decision} shape, not the sibling `confirmed`.
            assert "confirmed" not in resp, f"the 415 body carries the sibling-copied 'confirmed' key: {resp}"
            assert resp.get("domain", "MISSING") is None and resp.get("decision", "MISSING") is None, (
                f"the 415 body does not echo the route's domain/decision shape: {resp}"
            )
    finally:
        srv.shutdown()
        srv.server_close()


def test_route_oversize_content_length_413_no_flip(tmp_path):
    """AC-5 / SEC-0040-02 (413 ceiling): an over-ceiling Content-Length -> 413 BEFORE any read, 0 flip.

    Declares a Content-Length above `_CONFIRM_MAX_BYTES` while rfile carries a tiny body; the handler
    answers 413 from the header BEFORE reading the body, the seeded pointer stays `"pending"`. Driven
    in-process for determinism (the 413 status flip is failing-capable on its own — no seed needed for
    that, but the pointer stays pending to also prove 0 mutation).
    """
    store_root = tmp_path / "store"
    _seed_pending(store_root, "workout", TODAY_STR)
    declared = serve_server._CONFIRM_MAX_BYTES + 1
    out = _drive_confirm_plan_change_inproc(
        store_root, content_type="application/json", content_length=declared, body=b"{}"
    )
    status_line = out.split(b"\r\n", 1)[0]
    assert b"413" in status_line, f"an oversize confirm did not return 413: {status_line!r}"
    assert plan_confirm.decision_for("workout", TODAY_STR, store_root) == plan_confirm.DECISION_PENDING, (
        "an oversize confirm flipped the pointer (the body was read past the ceiling)"
    )
