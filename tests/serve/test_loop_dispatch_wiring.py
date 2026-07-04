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

import http.client
import json

from scripts.plan.safety_review import DEFAULT_LENSES
from scripts.serve import plan_loop
from scripts.serve import server as serve_server
from scripts.store.plan_schema import PLAN_DOMAINS

from tests.serve.test_plan_loop import _serve_in_thread


# --- concern (b): the shared JUDGE_ROLE constant + the routing disjointness precondition ---


def test_judge_role_is_public_shared_constant():
    # The judge role slug is a PUBLIC module constant the dispatch-seam consumers import — not a
    # private `_JUDGE_ROLE` each caller re-declares as a coupled literal (the concern-(b) duplication).
    assert plan_loop.JUDGE_ROLE == "quality-judge"
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
    assert plan_loop.dispatch_route_collisions(
        specialists=("workout",), lenses=("workout",)) == frozenset({"workout"})


# --- concern (a): honest degradation of /plan-loop in the standalone (seamless) server ----


def _seamless_server(tmp_path):
    """A loopback server built WITHOUT the loop seams — the production standalone posture."""
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold",
    )  # no loop_dispatch / loop_deid_client — main() supplies none (no subscription runtime)
    return srv, srv.server_address[1]


def _post_plan_loop(port, content_type="application/json"):
    headers = {"Content-Length": "0"}
    if content_type is not None:
        headers["Content-Type"] = content_type
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/plan-loop", body=b"", headers=headers)
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    conn.close()
    return resp.status, (json.loads(raw) if raw else {})


def test_plan_loop_route_honest_when_seams_absent(tmp_path):
    # A seamless server answers /plan-loop with a DISTINCT honest reason (loop-dispatch-unavailable),
    # never the generic "could not run plan loop" catch-all, and never a fabricated plan / thread drop.
    srv, port = _seamless_server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, body = _post_plan_loop(port)
        assert status == 200, f"expected 200 honest-degraded, got {status}"
        assert body.get("degraded") is True
        assert body.get("reason") == "loop-dispatch-unavailable", body
        assert body.get("results") == {}
    finally:
        srv.shutdown()
        srv.server_close()


def test_plan_loop_csrf_gate_precedes_seam_check(tmp_path):
    # The CSRF content-type gate fires BEFORE the seam-availability check: a non-json POST to a
    # seamless server is refused 415, never routed to the honest-degraded 200 (the seam check must
    # not weaken the CSRF refusal).
    srv, port = _seamless_server(tmp_path)
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop(port, content_type="text/plain")
        assert status == 415, f"expected 415 CSRF refusal, got {status}"
    finally:
        srv.shutdown()
        srv.server_close()
