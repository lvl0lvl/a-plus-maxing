"""Serve-route → driver front-door binding + anti-degradation guard (ADR-0036-T1).

The Wave-1 gating safety prerequisite: the automated plan-evolution loop's serve trigger
(`POST /plan-loop`) must bind to the FULL-COMPOSITION front door — `plan_loop.regenerate`
-> `plan_orchestrator.run_orchestrated` (loop_enabled) -> `plan_driver.drive` -> the composed
`gate_dispatch` (`compose_disposition`) + the five `orchestrate` cross-domain holds — and must
NEVER reach the screened-only `server._do_generate_plan` route, a bare
`orchestrate.generate_plans` that bypasses `drive`, or the per-domain `adjust.adjust_plan`.
Finding-A safety-parity FAILS outright if any trigger reaches the screened-only route; the
anti-degradation guard (AC-3/AC-4) is the load-bearing deliverable.

Every dispatch / de-id / gate is a mock/fixture; no test hits a live API, and the test tree
carries 0 real operator PII (synthetic tokens only) — the loop drives over the synthetic
`_raw_intake` / `_FixedDeidClient` seams at 0 live spend.

  - AC-1: firing the loop through the serve route produces exactly ONE new dated `plan::<domain>`
    set for the trigger date across all four `PLAN_DOMAINS`;
  - AC-2: the re-gen runs the composed path — `run_orchestrated` + `plan_driver.drive` entered,
    `compose_disposition` + the `orchestrate` reconciler fired;
  - AC-3 (anti-degradation guard): 0 `server._do_generate_plan` + 0 bare-bypass generate_plans;
  - AC-4: 0 `adjust.adjust_plan` on the loop path;
  - AC-5: a held domain (cross-domain-conflict, no adjudicator) is NOT recorded on the re-gen;
  - AC-6: a not-True GATE disposition returns `SAFETY_BLOCKED` with 0 promoted plans;
  - AC-7: the whole suite passes over fixtures with 0 live-API calls (0 `ModelClient` built).
"""

import datetime
import http.client

from scripts.model.client import ModelClient
from scripts.plan import adjust as adjust_mod
from scripts.plan import gate_dispatch as gate_dispatch_mod
from scripts.plan import orchestrate as orchestrate_mod
from scripts.plan import plan_driver
from scripts.plan import plan_orchestrator
from scripts.plan.plan_driver import SAFETY_BLOCKED
from scripts.plan.safety_review import DEFAULT_LENSES
from scripts.serve import server as serve_server
from scripts.store import plan_schema, store

from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
from tests.plan.test_generate_plan import (
    _author,
    _nutrition_meal_rec,
    _nutrition_target_rec,
    _peptide_rec,
    _seed_store,
    _supplement_rec,
    _workout_rec,
)
from tests.plan.test_orchestrate import _SUPP_CONFLICT, _nutrition, _recon
from tests.plan.test_plan_orchestrator import _deid_summary
from tests.plan.test_quality_judge import _clean_scores

# The judge role slug the loop's `_JudgeClient` adapter dispatches through the unified seam.
# Coupled by literal to `plan_loop._JUDGE_ROLE` (the loop is a single subscription-agent dispatch:
# ONE seam answers specialists, the quality judge, and each safety lens, routed by the first arg).
_JUDGE_ROLE = "quality-judge"


# --- the unified subscription-agent dispatch fixture (0 live spend) -------------


class _LoopDispatch:
    """A unified subscription-agent dispatch: routes specialist / judge / lens by the first arg.

    The loop drives ONE dispatch seam (the subscription agent) for every agent class. This fixture
    stands in for it: a plan-domain name returns that domain's captured author envelope, the judge
    role returns the per-dimension score map, and a safety-lens name returns that lens's findings.
    Records every call so a test can inspect what the loop dispatched.

    Attributes:
        authors (dict): domain -> the captured author envelope to return.
        judge_scores (dict): the per-dimension score map the quality judge returns.
        lens_findings (dict): lens -> the finding list that lens emits (default: 0 findings).
    """

    def __init__(self, authors, *, judge_scores=None, lens_findings=None):
        self.authors = authors
        self.judge_scores = judge_scores if judge_scores is not None else _clean_scores()
        self.lens_findings = lens_findings or {}
        self.calls = []

    def __call__(self, name, prompt, context):
        self.calls.append(name)
        if name == _JUDGE_ROLE:
            return dict(self.judge_scores)
        if name in DEFAULT_LENSES:
            return list(self.lens_findings.get(name, []))
        return self.authors[name]


def _clean_authors():
    """A clean four-domain author set (disjoint compounds → no additive-AE hold) that all record."""
    return {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
        "supplements": _author(_supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"),
        "peptides": _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
    }


def _held_authors():
    """A four-domain set where supplements declares a cross-domain conflict → supplements is HELD."""
    authors = _clean_authors()
    authors["supplements"] = _recon(
        _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
        conflicts=_SUPP_CONFLICT,
    )
    return authors


def _loop_server(tmp_path, dispatch, deid_client):
    """Build a loopback server whose `/plan-loop` handler drives `regenerate` over tmp roots.

    Seeds a PII-free operator state into the tmp store (the state the loop re-generates from) and
    injects the loop `dispatch` + `deid_client` seams so the E2E runs at 0 live spend and never
    touches the real store.
    """
    _seed_store(tmp_path / "store")
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold",
        loop_dispatch=dispatch, loop_deid_client=deid_client,
    )
    return srv, srv.server_address[1]


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    import threading

    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _post_plan_loop(port):
    """POST an (empty-body) tick to `/plan-loop`; return (status, parsed-JSON body)."""
    import json

    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/plan-loop", body=b"", headers={"Content-Length": "0"})
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    conn.close()
    return resp.status, (json.loads(raw) if raw else {})


def _plan_rows_today(root, domain, today):
    """The `plan::<domain>` rows dated `today` under `root`."""
    return [r for r in store.read(f"plan::{domain}", root=root) if r["timepoint"] == today]


# --- AC-1 + Risk (PF-S63-02: drive the assembled system through the serve entry point) ---


def test_loop_route_produces_one_new_dated_plan_set(tmp_path):
    # AC-1: firing the loop through the REAL serve `/plan-loop` route (bound server + http.client
    # POST — never `import plan_loop.regenerate` in isolation) produces exactly ONE new dated
    # plan set for today across all four PLAN_DOMAINS. The clean composed disposition promotes the
    # survivors; a route that recorded nothing (or 2 dated sets) reds.
    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, body = _post_plan_loop(port)
        assert status == 200, f"POST /plan-loop returned {status}, expected 200"

        today = datetime.date.today().isoformat()
        root = tmp_path / "store"
        dated = set()
        for domain in plan_schema.PLAN_DOMAINS:
            rows = _plan_rows_today(root, domain, today)
            assert len(rows) == 1, f"{domain} did not record exactly one plan for today: {rows}"
            dated.update(r["timepoint"] for r in store.read(f"plan::{domain}", root=root))
        # exactly ONE dated set for the trigger date (one generation, all under today)
        assert dated == {today}, f"expected one new dated plan set for {today}, got dates {dated}"
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-2: the re-gen runs the composed path (run_orchestrated + drive + compose + reconciler) ---


def test_loop_runs_composed_path(tmp_path, monkeypatch):
    # AC-2: the loop enters `run_orchestrated`, `plan_driver.drive` (the loop_enabled path),
    # `compose_disposition` (the ONE composition site), and the `orchestrate` reconciler — proving
    # the trigger drove the full-composition front door, not a screened-only bypass.
    entered_orchestrated = []
    entered_drive = []
    composed = []
    reconciled = []

    real_orchestrated = plan_orchestrator.run_orchestrated
    real_drive = plan_driver.drive
    real_compose = gate_dispatch_mod.compose_disposition
    real_reconcile = orchestrate_mod.reconcile

    def spy_orchestrated(*a, **k):
        entered_orchestrated.append(1)
        return real_orchestrated(*a, **k)

    def spy_drive(*a, **k):
        entered_drive.append(1)
        return real_drive(*a, **k)

    def spy_compose(*a, **k):
        composed.append(1)
        return real_compose(*a, **k)

    def spy_reconcile(*a, **k):
        reconciled.append(1)
        return real_reconcile(*a, **k)

    monkeypatch.setattr(plan_orchestrator, "run_orchestrated", spy_orchestrated)
    monkeypatch.setattr(plan_driver, "drive", spy_drive)
    monkeypatch.setattr(gate_dispatch_mod, "compose_disposition", spy_compose)
    monkeypatch.setattr(orchestrate_mod, "reconcile", spy_reconcile)

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop(port)
        assert status == 200
        assert entered_orchestrated, "the loop never entered run_orchestrated (front door bypassed)"
        assert len(entered_drive) >= 1, "the loop never entered plan_driver.drive (loop_enabled path)"
        assert composed, "compose_disposition never fired (the composed gate did not run)"
        assert reconciled, "the orchestrate reconciler never fired"
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-3 (anti-degradation guard): 0 screened-only path on the loop path -------


def test_loop_never_calls_screened_only_path(tmp_path, monkeypatch):
    # AC-3: the loop path records 0 `server._do_generate_plan` calls (the screened-only route that
    # skips the composed gate + the cross-domain holds). Firing the loop while `drive` is confirmed
    # entered proves generate_plans ran ONLY under the driver, never a bare bypass. A trigger that
    # reached the screened-only route reds. Source-grep backstop below.
    screened_calls = []
    entered_drive = []
    real_do_gen = serve_server.IntakeRequestHandler._do_generate_plan
    real_drive = plan_driver.drive

    def spy_do_gen(self, *a, **k):
        screened_calls.append(1)
        return real_do_gen(self, *a, **k)

    def spy_drive(*a, **k):
        entered_drive.append(1)
        return real_drive(*a, **k)

    monkeypatch.setattr(serve_server.IntakeRequestHandler, "_do_generate_plan", spy_do_gen)
    monkeypatch.setattr(plan_driver, "drive", spy_drive)

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop(port)
        assert status == 200
        assert screened_calls == [], "the loop reached the screened-only _do_generate_plan route"
        assert len(entered_drive) >= 1, "the loop did not run through the driver (front-door bypass)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_plan_loop_source_never_imports_screened_only_path():
    # AC-3 (static backstop): the loop module references NEITHER the screened-only `_do_generate_plan`
    # NOR a bare `generate_plans` — the two paths stay distinct (the anti-degradation guard exists to
    # prevent that convergence). Reds the moment the loop re-imports the screened route.
    from pathlib import Path

    src = Path("scripts/serve/plan_loop.py").read_text()
    assert "_do_generate_plan" not in src, "plan_loop.py references the screened-only _do_generate_plan"
    assert "generate_plans" not in src, "plan_loop.py calls a bare generate_plans (bypassing the driver)"


# --- AC-4: 0 adjust.adjust_plan on the loop path --------------------------------


def test_loop_never_calls_adjust(tmp_path, monkeypatch):
    # AC-4: the loop path records 0 `adjust.adjust_plan` calls (the per-domain re-plan that skips the
    # cross-domain reconciler + the composed gate). A loop that re-used the adjust leg reds. Source-
    # grep backstop below.
    adjust_calls = []
    real_adjust = adjust_mod.adjust_plan

    def spy_adjust(*a, **k):
        adjust_calls.append(1)
        return real_adjust(*a, **k)

    monkeypatch.setattr(adjust_mod, "adjust_plan", spy_adjust)

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop(port)
        assert status == 200
        assert adjust_calls == [], "the loop path called adjust.adjust_plan (per-domain bypass)"
    finally:
        srv.shutdown()
        srv.server_close()


def test_plan_loop_source_never_references_adjust():
    # AC-4 (static backstop): the loop module never references `adjust` (the per-domain path).
    from pathlib import Path

    src = Path("scripts/serve/plan_loop.py").read_text()
    assert "adjust" not in src, "plan_loop.py references adjust (the per-domain re-plan bypass)"


# --- AC-5: held-domain-stays-held on the re-gen ---------------------------------


def test_held_domain_stays_held_on_regen(tmp_path):
    # AC-5: a domain HELD by the new-data composition (a cross-domain-conflict hold, no adjudicator
    # wired → recorded: False) is NOT recorded on the re-gen — clearance is re-derived per re-gen,
    # never inherited. The non-declaring survivors still promote (positive control that the pass ran).
    dispatch = _LoopDispatch(_held_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, body = _post_plan_loop(port)
        assert status == 200

        today = datetime.date.today().isoformat()
        root = tmp_path / "store"
        # the held supplements domain recorded NOTHING for today (0 held domains past the hold)
        assert _plan_rows_today(root, "supplements", today) == [], (
            "the held supplements domain was recorded on the re-gen (a hold was inherited/bypassed)"
        )
        assert body["results"]["supplements"]["recorded"] is False
        # positive control: a non-held survivor DID record (the pass ran; the hold is what suppressed it)
        assert len(_plan_rows_today(root, "peptides", today)) == 1, (
            "no survivor recorded — the held-domain assertion would be vacuous"
        )
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-6: fail-closed surface gate preserved -----------------------------------


def test_not_true_gate_returns_safety_blocked(tmp_path):
    # AC-6: a fixture whose GATE disposition returns `safety_passed` not-True (a safety lens emits a
    # finding → the review does not pass) makes the run return SAFETY_BLOCKED and promote 0 plans into
    # `root` (the fail-closed surface — a blocked plan never touches the rendered store).
    dispatch = _LoopDispatch(
        _clean_authors(),
        lens_findings={"medical-safety-reviewer": [
            {"id": "cumulative-hepatic-load",
             "concern": "cumulative hepatic load across domains exceeds the safe ceiling",
             "severity": "high"},
        ]},
    )
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, body = _post_plan_loop(port)
        assert status == 200
        assert body["reason"] == SAFETY_BLOCKED, f"expected SAFETY_BLOCKED, got {body.get('reason')}"

        today = datetime.date.today().isoformat()
        root = tmp_path / "store"
        # 0 plan:: rows promoted into `root` across EVERY domain (the fail-closed surface)
        for domain in plan_schema.PLAN_DOMAINS:
            assert _plan_rows_today(root, domain, today) == [], (
                f"a plan was promoted for {domain} despite the not-True safety gate (fail-closed broken)"
            )
    finally:
        srv.shutdown()
        srv.server_close()


# --- AC-7: 0 live-API calls (mock clients only) ---------------------------------


def test_loop_makes_no_live_backend_call(tmp_path, monkeypatch):
    # AC-7: the loop runs over the injected mocks only — it constructs no `ModelClient` (and thus no
    # live no-train backend). A `ModelClient.__init__` spy confirms 0 self-constructed clients on the
    # loop path (0 live spend).
    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop(port)
        assert status == 200
        assert instantiations == [], "the loop path constructed a ModelClient (must use only injected mocks)"
    finally:
        srv.shutdown()
        srv.server_close()
