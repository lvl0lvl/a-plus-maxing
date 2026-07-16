"""Bead `3ge1` — the ADR-0036-T1 Tier-2 Architect wiring concern (loop dispatch seam).

Two concerns the Architect surfaced on ADR-0036-T1:

  (b) `plan_loop._JUDGE_ROLE` was module-private and re-declared as a coupled literal in the loop
      tests. Export it as the shared public `plan_loop.JUDGE_ROLE` so the dispatch-seam consumers
      (T2/T3/T4) read ONE constant, and surface the dispatch-seam routing DISJOINTNESS precondition:
      the unified `dispatch(name, ...)` seam routes `name` over three name-spaces — a `PLAN_DOMAINS`
      specialist, `JUDGE_ROLE`, or a `safety_review.DEFAULT_LENSES` lens — which MUST be pairwise
      disjoint, else the router is ambiguous (a lens named "workout" would shadow the specialist).

  (a) Production `main()` (`scripts/serve/__main__.py`) supplies no `loop_dispatch`/`loop_deid_client`
      because the standalone `python -m scripts.serve` process has no subscription-agent runtime to
      fulfill the loop's A' aggregate dispatch (ADR-0036 Consequences — the dispatch is the whole
      subscription-session aggregate, not an API call). So `/plan-loop` cannot run live in the
      standalone server; it must degrade with a DISTINCT, HONEST reason (`loop-dispatch-unavailable`),
      not the generic catch-all, and without fabricating a dispatch or arming any spend.
"""

import pytest

from scripts import secret_store
from scripts.model import key_source
from scripts.plan.safety_review import DEFAULT_LENSES
from scripts.serve import __main__ as entry
from scripts.serve import alpha_config
from scripts.serve import plan_loop
from scripts.serve import server as serve_server
from scripts.store.plan_schema import PLAN_DOMAINS

from tests.plan.test_deid_in import _FixedDeidClient
from tests.plan.test_plan_orchestrator import _deid_summary
from tests.serve.test_plan_loop import (
    _LoopDispatch,
    _clean_authors,
    _loop_server,
    _post_plan_loop,
    _post_plan_loop_ctype,
    _serve_in_thread,
)


# --- concern (b): the shared JUDGE_ROLE constant + the routing disjointness precondition ---


def test_judge_role_is_public_shared_constant():
    # The judge role slug is a PUBLIC module constant the dispatch-seam consumers import — not a
    # private `_JUDGE_ROLE` each caller re-declares as a coupled literal (the concern-(b) duplication).
    assert plan_loop.JUDGE_ROLE == "quality-judge"
    # The private `_JUDGE_ROLE` duplicate is actually GONE — one source of truth, not a co-existing
    # private literal a caller could re-couple to (concern (b)'s de-duplication, pinned at the module).
    assert not hasattr(plan_loop, "_JUDGE_ROLE"), "the private _JUDGE_ROLE duplicate must be removed"
    # The `_JudgeClient` adapter dispatches the quality gate through THAT constant (one authority).
    seen = []
    client = plan_loop._JudgeClient(lambda name, prompt, ctx: seen.append(name) or {})
    client.judge({"any": "payload"})
    assert seen == [plan_loop.JUDGE_ROLE], "the judge adapter dispatched a role != JUDGE_ROLE"


def test_dispatch_seam_name_spaces_pairwise_disjoint():
    # The unified dispatch seam routes `name` over three name-spaces; a production router is
    # unambiguous ONLY if they are pairwise disjoint. Mutation-proven: introduce a collision
    # (e.g. DEFAULT_LENSES contains "workout") and this reds.
    specialists = set(PLAN_DOMAINS)
    judge = {plan_loop.JUDGE_ROLE}
    lenses = set(DEFAULT_LENSES)
    assert specialists.isdisjoint(judge), f"specialist name collides with JUDGE_ROLE: {specialists & judge}"
    assert specialists.isdisjoint(lenses), f"specialist name collides with a safety lens: {specialists & lenses}"
    assert judge.isdisjoint(lenses), f"JUDGE_ROLE collides with a safety lens: {judge & lenses}"


def test_precondition_helper_reports_collisions():
    # The precondition is surfaced as a callable predicate the dispatch-seam consumers can assert
    # against (concern (b) "surface the ... precondition where T2/T3/T4 read it"). It returns the
    # empty set for the live rosters and the offending overlap under a synthetic collision.
    assert plan_loop.dispatch_route_collisions() == frozenset()
    # specialist <-> lens overlap
    assert plan_loop.dispatch_route_collisions(
        specialists=("workout",), lenses=("workout",)) == frozenset({"workout"})
    # specialist <-> JUDGE_ROLE default overlap (exercises the judge name-space branch)
    assert plan_loop.dispatch_route_collisions(
        specialists=(plan_loop.JUDGE_ROLE,)) == frozenset({plan_loop.JUDGE_ROLE})
    # a name shared across ALL THREE name-spaces reports once
    assert plan_loop.dispatch_route_collisions(
        specialists=("x",), judge="x", lenses=("x",)) == frozenset({"x"})
    # within-roster duplicates are not cross-space collisions
    assert plan_loop.dispatch_route_collisions(
        specialists=("workout", "workout"), lenses=("nutrition",)) == frozenset()


# --- concern (a): honest degradation of /plan-loop in the standalone (seamless) server ----


def _server(tmp_path, *, loop_dispatch=None, loop_deid_client=None):
    """A loopback server with the given loop-seam wiring (default: seamless — the standalone posture)."""
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold",
        loop_dispatch=loop_dispatch, loop_deid_client=loop_deid_client,
    )
    return srv, srv.server_address[1]


def _assert_honest_degraded(port):
    """POST /plan-loop and assert the distinct honest degraded shape (not the generic catch-all)."""
    status, body = _post_plan_loop_ctype(port, "application/json")
    assert status == 200, f"expected 200 honest-degraded, got {status}"
    assert body.get("degraded") is True
    assert body.get("reason") == "loop-dispatch-unavailable", body
    assert body.get("results") == {}


def test_plan_loop_route_honest_when_seams_absent(tmp_path):
    # A seamless server answers /plan-loop with a DISTINCT honest reason (loop-dispatch-unavailable),
    # never the generic "could not run plan loop" catch-all, and never a fabricated plan / thread drop.
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        _assert_honest_degraded(port)
    finally:
        srv.shutdown()
        srv.server_close()


def test_plan_loop_route_honest_when_half_wired(tmp_path):
    # A HALF-wired server (exactly ONE seam present) also degrades honestly — the guard is `or`, not
    # `and`: `regenerate` needs BOTH the dispatch and the deid_client, so one-present-one-None must not
    # drive `regenerate(deid_client=None)` into the generic catch-all. Both mirrors pin the `or`.
    for dispatch, deid_client in ((lambda *a: {}, None), (None, object())):
        srv, port = _server(tmp_path, loop_dispatch=dispatch, loop_deid_client=deid_client)
        _serve_in_thread(srv)
        try:
            _assert_honest_degraded(port)
        finally:
            srv.shutdown()
            srv.server_close()


def test_plan_loop_csrf_gate_precedes_seam_check(tmp_path):
    # The CSRF content-type gate fires BEFORE the seam-availability check: a non-json POST to a
    # seamless server is refused 415, never routed to the honest-degraded 200 (the seam check must
    # not weaken the CSRF refusal).
    srv, port = _server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop_ctype(port, "text/plain")
        assert status == 415, f"expected 415 CSRF refusal, got {status}"
    finally:
        srv.shutdown()
        srv.server_close()


# --- ADR-0049-T1: the metered loop-seam wiring at operator start + the D5 shared-key bridge -------


def _fixture_alpha_config(shared_key):
    """A fixture `AlphaConfig` carrying a synthetic shared key + no vendor creds (the no-BYO default)."""
    return alpha_config.AlphaConfig(vendors={}, shared_api_key=shared_key, client_types={})


class _Abort(Exception):
    """Abort the entry inside the spy `build`, before the serve loop (the house spy-build pattern)."""


def test_main_wires_metered_seams_and_bridge_closes_default(monkeypatch):
    # AC-2: `main()` hands `build` a non-None loop_dispatch + loop_deid_client, and the D5 bridge
    # closes the no-BYO default (`key_source.resolve` returns the shared key after `main()`).
    shared = "sk-ant-" + "shared-fixture-000"  # synthetic, sk-ant--shaped
    monkeypatch.delenv(key_source.ENV_VAR, raising=False)  # FIRST — isolate the bridge's raw os.environ write
    monkeypatch.setattr(secret_store, "get_secret", lambda *a, **k: None)  # empty keychain (no real keyring)
    monkeypatch.setattr(alpha_config, "load_alpha_config", lambda *a, **k: _fixture_alpha_config(shared))

    captured = {}

    def _spy_build(port, *, client=None, loop_dispatch=None, loop_deid_client=None, **kwargs):
        captured["loop_dispatch"] = loop_dispatch
        captured["loop_deid_client"] = loop_deid_client
        raise _Abort

    with pytest.raises(_Abort):
        entry.main(build=_spy_build, client_factory=lambda: object())

    assert captured["loop_dispatch"] is not None, "main() wired no metered loop_dispatch"
    assert captured["loop_deid_client"] is not None, "main() wired no loop_deid_client"
    assert key_source.resolve() == shared, "the D5 bridge did not close the no-BYO default"


def test_bridge_out_meta_assertion_default_stays_open(monkeypatch):
    # AR-005 in-suite meta-assertion: run `main()` with the bridge monkeypatched to a NO-OP; the
    # no-BYO default is NOT closed, so `key_source.resolve()` raises — the suite ITSELF fails if the
    # bridge is not load-bearing (a prose falsifier is not enough).
    shared = "sk-ant-" + "shared-fixture-001"
    monkeypatch.delenv(key_source.ENV_VAR, raising=False)
    monkeypatch.setattr(secret_store, "get_secret", lambda *a, **k: None)
    monkeypatch.setattr(alpha_config, "load_alpha_config", lambda *a, **k: _fixture_alpha_config(shared))
    monkeypatch.setattr(alpha_config, "provision_shared_key", lambda *a, **k: None)  # bridge no-op

    def _spy_build(port, *, client=None, loop_dispatch=None, loop_deid_client=None, **kwargs):
        raise _Abort

    with pytest.raises(_Abort):
        entry.main(build=_spy_build, client_factory=lambda: object())
    with pytest.raises(key_source.KeyUnavailableError):
        key_source.resolve()


def test_plan_loop_both_seams_wired_routes_non_degraded(tmp_path):
    # AC-2 (AR-002 integration mandate): with BOTH loop seams wired, POST /plan-loop passes the
    # or-guard (server.py:893) and routes confirm -> plan_loop -> run_orchestrated to a real
    # recording-backed result — the complement of this file's seamless/half-wired degraded tests.
    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, body = _post_plan_loop(port)
        assert status == 200, f"expected 200, got {status}"
        assert not (body.get("degraded") is True and body.get("reason") == "loop-dispatch-unavailable"), body
        assert dispatch.calls, "the loop_dispatch was never invoked — the request did not route to run_orchestrated"
    finally:
        srv.shutdown()
        srv.server_close()


def test_main_does_not_leak_shared_key(monkeypatch, capsys):
    # AC-8: `main()`'s stdout/stderr carries the shared-key VALUE 0 times. A negative assertion is
    # vacuously green while unmodified, so its proof is the in-suite meta-assertion below.
    shared = "sk-ant-" + "shared-fixture-002"
    monkeypatch.delenv(key_source.ENV_VAR, raising=False)
    monkeypatch.setattr(secret_store, "get_secret", lambda *a, **k: None)
    monkeypatch.setattr(alpha_config, "load_alpha_config", lambda *a, **k: _fixture_alpha_config(shared))

    def _quiet_build(port, *, client=None, **kwargs):
        raise _Abort

    with pytest.raises(_Abort):
        entry.main(build=_quiet_build, client_factory=lambda: object())
    quiet = capsys.readouterr()
    assert shared not in quiet.out and shared not in quiet.err, "main() leaked the shared key value"

    # AR-005 meta-assertion: the SAME capsys scan MUST catch a deliberately-leaky build spy — so the
    # suite itself fails if the no-leak scan cannot detect a leak.
    def _leaky_build(port, **kwargs):
        print(shared)  # simulate a leak
        raise _Abort

    with pytest.raises(_Abort):
        entry.main(build=_leaky_build, client_factory=lambda: object())
    leaked = capsys.readouterr()
    with pytest.raises(AssertionError):
        assert shared not in leaked.out and shared not in leaked.err
