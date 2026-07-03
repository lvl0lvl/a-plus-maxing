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
from scripts.store import biomarker_meta, loop_schema, plan_schema, store

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
    """POST an (empty-body) application/json tick to `/plan-loop`; return (status, JSON body)."""
    return _post_plan_loop_ctype(port, "application/json")


def _post_plan_loop_ctype(port, content_type):
    """POST an empty-body tick to `/plan-loop` with an explicit Content-Type; return (status, body).

    `content_type` None omits the header entirely (the missing-content-type case).
    """
    import json

    headers = {"Content-Length": "0"}
    if content_type is not None:
        headers["Content-Type"] = content_type
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/plan-loop", body=b"", headers=headers)
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


# --- SEC-1: CSRF content-type gate on /plan-loop --------------------------------


def test_non_json_content_type_refused_before_regenerate(tmp_path, monkeypatch):
    # SEC-1 (MUST FIX): a text/plain (CORS-simple) POST to /plan-loop is refused 415 BEFORE
    # `regenerate` — a cross-site simple POST cannot drive the highest-spend loop tick (every
    # specialist + judge + lens). A regenerate spy asserts the dispatch is NEVER reached, and 0
    # plans are promoted. Turns RED if the gate is removed (regenerate would run → 200 + promotions).
    from scripts.serve import plan_loop

    calls = []
    real_regen = plan_loop.regenerate

    def spy_regen(*a, **k):
        calls.append(1)
        return real_regen(*a, **k)

    monkeypatch.setattr(plan_loop, "regenerate", spy_regen)

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, _ = _post_plan_loop_ctype(port, "text/plain")
        assert status == 415, f"non-json POST returned {status}, expected 415"
        assert calls == [], "regenerate was reached despite the non-json content-type (CSRF gate bypassed)"

        today = datetime.date.today().isoformat()
        root = tmp_path / "store"
        for domain in plan_schema.PLAN_DOMAINS:
            assert _plan_rows_today(root, domain, today) == [], (
                f"a plan was promoted for {domain} despite the 415 refusal"
            )
    finally:
        srv.shutdown()
        srv.server_close()


# --- degraded-fallback branch (QA coverage gap) ---------------------------------


def test_regenerate_raises_returns_degraded(tmp_path, monkeypatch):
    # SHOULD FIX (QA gap): an injected `regenerate` that raises makes the loop answer 200 +
    # degraded=True + a reason (thread survival — never a dropped request), and promotes 0 plans.
    # The broad `except Exception -> degraded` thread-survival branch was previously untested.
    from scripts.serve import plan_loop

    def boom(*a, **k):
        raise RuntimeError("regenerate blew up")

    monkeypatch.setattr(plan_loop, "regenerate", boom)

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())
    srv, port = _loop_server(tmp_path, dispatch, deid_client)
    _serve_in_thread(srv)
    try:
        status, body = _post_plan_loop(port)  # valid application/json
        assert status == 200, f"degraded path returned {status}, expected 200"
        assert body.get("degraded") is True, f"expected degraded=True, got {body}"
        assert body.get("reason"), "the degraded response carried no reason"

        today = datetime.date.today().isoformat()
        root = tmp_path / "store"
        for domain in plan_schema.PLAN_DOMAINS:
            assert _plan_rows_today(root, domain, today) == [], (
                f"a plan was promoted for {domain} despite the degraded-fallback branch"
            )
    finally:
        srv.shutdown()
        srv.server_close()


# =====================================================================================
# ADR-0036-T2: shared debounce gate + three-trigger convergence (derived state) -------
# =====================================================================================

_T2_ON_DATE = "2026-06-18"
_SUSTAINED_DATES = ("2026-06-01", "2026-06-08", "2026-06-16")  # 3 timepoints, 15-day span


def _seed_prior_plan(root, plan_date):
    """Record one prior plan (workout) dated `plan_date` — the derived last-re-gen anchor."""
    plan_schema.record_plan(
        "workout", {"exercises": [{"name": "Squat", "sets": 3}]},
        plan_date, "personal-trainer", root,
    )


def _seed_biomarker(root, marker, values, dates):
    """Seed a `biomarker::<marker>` series (one reading per value/date) via the frozen writer."""
    for value, day in zip(values, dates):
        loop_schema.record_biomarker(marker, f"{day}T00:00:00+00:00", value, root)


def _new_dated_sets(root, plan_date):
    """Count of NEW dated plan:: sets for `plan_date` (0 or 1 — one generation is one date)."""
    return len({
        r["timepoint"]
        for domain in plan_schema.PLAN_DOMAINS
        for r in store.read(f"plan::{domain}", root=root)
        if r["timepoint"] == plan_date
    })


def _sustained_root(tmp_path, name):
    """A tmp store seeded with operator state + an OLD prior plan + a sustained rising hrv series."""
    root = tmp_path / name
    _seed_store(root)
    _seed_prior_plan(root, "2026-06-01")            # 17 days before the trigger date (>= 7)
    _seed_biomarker(root, "hrv", [40, 50, 60], _SUSTAINED_DATES)  # rising hrv (up) -> improving
    return root


# --- Cycle 1 AC-1/AC-2: the single-vs-sustained falsifiable pair --------------------


def test_debounce_single_reading_vs_sustained_pair(tmp_path):
    # AC-1 + AC-2 (the load-bearing pair): a SINGLE new reading in the window produces 0 new dated
    # plan sets; a SUSTAINED series (>= n across the span, directional) produces exactly 1. The two
    # dispositions MUST differ, or the gate does not discriminate single from sustained.
    from scripts.serve import plan_loop

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())

    single = tmp_path / "single"
    _seed_store(single)
    _seed_biomarker(single, "hrv", [55], ("2026-06-16",))  # one reading — not sustained
    plan_loop.signal(single, trigger=plan_loop.DATA_EVENT_TRIGGER,
                     dispatch=dispatch, deid_client=deid_client, plan_date=_T2_ON_DATE)
    count_single = _new_dated_sets(single, _T2_ON_DATE)

    sustained = _sustained_root(tmp_path, "sustained")
    plan_loop.signal(sustained, trigger=plan_loop.DATA_EVENT_TRIGGER,
                     dispatch=dispatch, deid_client=deid_client, plan_date=_T2_ON_DATE)
    count_sustained = _new_dated_sets(sustained, _T2_ON_DATE)

    assert count_single == 0, "a single reading re-generated (the debounce did not hold)"
    assert count_sustained == 1, "a sustained signal did NOT re-generate (the gate never fires)"
    assert count_single != count_sustained, "the gate does not discriminate single from sustained"


def test_debounce_recent_regen_blocks_min_interval(tmp_path):
    # AC-1 (min-interval leg): a re-gen within the pinned interval blocks a fresh re-gen even with a
    # sustained signal present — the whole-plan re-gen cost bound (Consequences-Negative-1).
    from scripts.serve import plan_loop

    root = tmp_path / "store"
    _seed_store(root)
    _seed_prior_plan(root, "2026-06-15")  # 3 days before the trigger date (< 7)
    _seed_biomarker(root, "hrv", [40, 50, 60], _SUSTAINED_DATES)
    plan_loop.signal(root, trigger=plan_loop.DATA_EVENT_TRIGGER,
                     dispatch=_LoopDispatch(_clean_authors()),
                     deid_client=_FixedDeidClient(_deid_summary()), plan_date=_T2_ON_DATE)
    assert _new_dated_sets(root, _T2_ON_DATE) == 0, "a re-gen fired inside the min interval"


# --- Cycle 1 AC-3: absent-data hold + prompt ----------------------------------------


def test_cadence_absent_signal_holds_and_prompts(tmp_path):
    # AC-3: a cadence tick with NO new signal in the window holds and prompts (a log-prompt flag),
    # never re-generates on nothing.
    from scripts.serve import plan_loop

    root = tmp_path / "store"
    _seed_store(root)
    _seed_prior_plan(root, "2026-06-01")  # min-interval satisfied; the HOLD is from absent signal
    body = plan_loop.signal(root, trigger=plan_loop.CADENCE_TRIGGER,
                            dispatch=_LoopDispatch(_clean_authors()),
                            deid_client=_FixedDeidClient(_deid_summary()), plan_date=_T2_ON_DATE)
    assert _new_dated_sets(root, _T2_ON_DATE) == 0, "the cadence tick re-generated on absent data"
    assert body.get("log_prompt") is True, "the absent-data hold carried no log-prompt flag"


# --- Cycle 1 AC-4: the debounce parameters are pinned module constants ---------------


def test_debounce_parameters_are_pinned_constants():
    # AC-4: every debounce parameter is a fixed module-level literal a deterministic test reads (not
    # a runtime default / not env-derived). The sustained-window n REUSES the existing honest-absence
    # guardrail — one constant, one home (no second n literal).
    from scripts.serve import plan_loop

    assert plan_loop.MIN_REGEN_INTERVAL_DAYS == 7
    assert plan_loop.SUSTAINED_WINDOW_SPAN_DAYS == 7
    assert plan_loop.SUSTAINED_WINDOW_MIN_READINGS == 3
    assert plan_loop.SUSTAINED_WINDOW_MIN_READINGS == biomarker_meta.PROJECTION_MIN_TIMEPOINTS
    assert plan_loop.SUSTAINED_TREND_DIRECTIONS == ("improving", "regressing")
    # The dead sub-day free-text rate limit was removed (Tier-3 FIX 3): the free-text trigger has no
    # independent bound — it obeys the 7-day min-interval floor like every other trigger.
    assert not hasattr(plan_loop, "FREE_TEXT_RATE_LIMIT_HOURS")


# --- Cycle 1 AC-5: no new store stream (derived state) -------------------------------


def test_debounce_writes_no_new_store_stream(tmp_path, monkeypatch):
    # AC-5: the debounce state is DERIVED — a debounced no-op writes NOTHING, and a re-gen writes
    # only the plan:: promote (0 loop::/debounce::/regen-marker:: id, 0 debounce-marker append). The
    # last-re-gen date reads through plan_schema.resolve_plan (spied), never a stored marker.
    from scripts.serve import plan_loop

    real_append = store.append
    appended = []

    def spy_append(item, *a, **k):
        appended.append(item)
        return real_append(item, *a, **k)

    # (a) a debounced no-op writes 0 store records at all
    drop_root = tmp_path / "drop"
    _seed_store(drop_root)
    _seed_biomarker(drop_root, "hrv", [55], ("2026-06-16",))  # single reading -> debounced
    monkeypatch.setattr(store, "append", spy_append)
    plan_loop.signal(drop_root, trigger=plan_loop.DATA_EVENT_TRIGGER,
                     dispatch=_LoopDispatch(_clean_authors()),
                     deid_client=_FixedDeidClient(_deid_summary()), plan_date=_T2_ON_DATE)
    assert appended == [], f"a debounced no-op wrote store records: {appended}"

    # (b) a re-gen writes only plan:: promotes — never a debounce/last-re-gen marker stream; and the
    # last-re-gen date is read through resolve_plan (a derived read), not a stored marker.
    monkeypatch.setattr(store, "append", real_append)  # real writer while seeding the regen root
    regen_root = _sustained_root(tmp_path, "regen")
    appended.clear()
    resolve_calls = []
    real_resolve = plan_schema.resolve_plan

    def spy_resolve(*a, **k):
        resolve_calls.append(1)
        return real_resolve(*a, **k)

    monkeypatch.setattr(plan_schema, "resolve_plan", spy_resolve)
    monkeypatch.setattr(store, "append", spy_append)
    plan_loop.signal(regen_root, trigger=plan_loop.DATA_EVENT_TRIGGER,
                     dispatch=_LoopDispatch(_clean_authors()),
                     deid_client=_FixedDeidClient(_deid_summary()), plan_date=_T2_ON_DATE)
    assert resolve_calls, "the debounce never read the last-re-gen date via plan_schema.resolve_plan"
    assert any(i.startswith("plan::") for i in appended), "the re-gen promoted no plan:: rows"
    for item in appended:
        assert not item.startswith(("loop::", "debounce::", "regen-marker::")), (
            f"the debounce persisted a new store stream {item!r} (state must be derived)"
        )


# --- Cycle 2 AC-6: three triggers converge on the one debounced entry ---------------


def test_route_upload_notifies_the_debounced_entry(tmp_path, monkeypatch):
    # AC-6: a wearable land reaches the ONE debounced entry with a data-event trigger (0 direct
    # regenerate from the trigger site).
    from scripts.serve import plan_loop, route
    from tests.serve.test_route import _write_healthkit_xml

    calls = []
    monkeypatch.setattr(plan_loop, "signal", lambda root, **k: calls.append(k.get("trigger")))
    staged = tmp_path / "export.xml"
    _write_healthkit_xml(staged, day="2026-05-01", value="55")
    route.route_upload(staged, root=tmp_path / "store", dna_root=tmp_path / "dna")
    assert calls == [plan_loop.DATA_EVENT_TRIGGER], f"route_upload did not notify the entry: {calls}"


def test_land_confirmed_notifies_the_debounced_entry(tmp_path, monkeypatch):
    # AC-6: a confirmed-lab land reaches the ONE debounced entry with a data-event trigger.
    from scripts.serve import confirm, plan_loop

    calls = []
    monkeypatch.setattr(plan_loop, "signal", lambda root, **k: calls.append(k.get("trigger")))
    confirm.land_confirmed(
        [{"item": "ferritin", "timepoint": "2026-05-01", "source": "labs", "value": "120"}],
        root=tmp_path / "store",
    )
    assert calls == [plan_loop.DATA_EVENT_TRIGGER], f"land_confirmed did not notify: {calls}"


def test_respond_notifies_on_capture_completion_only_derived_tokens(tmp_path, monkeypatch):
    # AC-6: a care-chat capture completion reaches the ONE debounced entry with a free-text trigger,
    # and the notify carries only the derived trigger label — never the raw turn text (finding-C).
    # The fail-closed degraded branch does NOT notify.
    from scripts.serve import care_chat, plan_loop
    from tests.serve.test_care_chat import _RecordingBackend, _seed

    root = tmp_path / "store"
    _seed(root)
    calls = []
    monkeypatch.setattr(plan_loop, "signal", lambda r, **k: calls.append((k.get("trigger"), r, k)))
    turn = "I slept 5 hours and my resting HR was 48"
    care_chat.respond(turn, [], client=_RecordingBackend(), store_root=root)
    assert [c[0] for c in calls] == [plan_loop.FREE_TEXT_TRIGGER], f"respond did not notify: {calls}"
    assert turn not in repr(calls), "the free-text notify carried the raw turn text (finding-C boundary)"

    calls.clear()
    care_chat.respond(turn, [], client=_RecordingBackend(raise_error=True), store_root=root)
    assert calls == [], "the fail-closed degraded branch notified the loop (must skip on degrade)"


def test_cross_kind_triggers_within_window_dedupe(tmp_path):
    # AC-6 (dedupe): two DIFFERENT-kind triggers inside the same window drive at most 1 re-gen — the
    # shared gate drops the second (the first re-gen sets last-re-gen to today, inside the min
    # interval for the second). Non-tautological: exactly one re-gen results, not zero.
    from scripts.serve import care_chat, plan_loop, route
    from tests.serve.test_care_chat import _RecordingBackend, _seed
    from tests.serve.test_route import _write_healthkit_xml

    root = tmp_path / "store"
    _seed_store(root)
    _seed(root)  # care-profile fields for router.summarize
    _seed_prior_plan(root, "2026-06-01")  # old regen -> min-interval satisfied for trigger 1
    _seed_biomarker(root, "hrv", [40, 50, 60], _SUSTAINED_DATES)
    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())

    # trigger 1 — a wearable data-event through route.route_upload -> re-gen
    staged = tmp_path / "export.xml"
    _write_healthkit_xml(staged, day="2026-06-17", value="61")
    route.route_upload(staged, root=root, dna_root=tmp_path / "dna",
                       loop_dispatch=dispatch, loop_deid_client=deid_client)
    # trigger 2 — a care-chat free-text of a DIFFERENT kind, same window -> dropped by the gate
    care_chat.respond("resting HR trending down", [], client=_RecordingBackend(),
                      store_root=root, loop_dispatch=dispatch, loop_deid_client=deid_client)

    today = datetime.date.today().isoformat()
    assert _new_dated_sets(root, today) == 1, "cross-kind triggers produced != 1 re-gen (dedupe broken)"


# =====================================================================================
# Tier-3 review fixes: cross-stream debounce, dead free-text bound, signal isolation ---
# =====================================================================================


def test_debounce_no_cross_stream_false_fire(tmp_path):
    # FIX 2 (HIGH, store-adversarial cross-stream): the direction conjunct and the sustained-length
    # conjunct must be satisfied by the SAME stream. A directional-but-SHORT stream (`hrv` rising over
    # a 2-reading blip) ALONGSIDE an unrelated long FLAT stream (`alt`, 3 readings over 15 days) must
    # NOT re-generate — no single stream carries both a directional trend AND the sustained length.
    # Pre-fix (worst-wins direction over one stream + any-stream length over another) fires → RED.
    from scripts.serve import plan_loop

    root = tmp_path / "store"
    _seed_store(root)
    # NO prior plan -> min-interval is vacuously satisfied (last=None); the gate reduces to the signal.
    _seed_biomarker(root, "hrv", [40, 60], ("2026-06-14", "2026-06-16"))   # directional, but 2 readings
    _seed_biomarker(root, "alt", [30, 30, 30], _SUSTAINED_DATES)           # 3 readings/15 days, FLAT
    store_read = __import__("functools").partial(store.read, root=root)

    assert plan_loop._sustained_signal(store_read) is False, (
        "a directional blip in hrv borrowed alt's flat long series (cross-stream false-fire)"
    )
    assert plan_loop._should_regenerate(store_read, on_date=_T2_ON_DATE) is False

    # E2E through the debounced entry: 0 new dated plan sets (the store-adversarial cross-stream case).
    plan_loop.signal(root, trigger=plan_loop.DATA_EVENT_TRIGGER,
                     dispatch=_LoopDispatch(_clean_authors()),
                     deid_client=_FixedDeidClient(_deid_summary()), plan_date=_T2_ON_DATE)
    assert _new_dated_sets(root, _T2_ON_DATE) == 0, "cross-stream signal re-generated (debounce broke)"


def test_single_stream_sustained_still_fires(tmp_path):
    # FIX 2 (positive control): a SINGLE stream that alone carries BOTH conjuncts (hrv rising over 3
    # readings / 15 days) still fires — the tightened gate did not become a blanket drop.
    from scripts.serve import plan_loop

    root = _sustained_root(tmp_path, "one-stream")  # hrv [40,50,60] over _SUSTAINED_DATES, old prior plan
    store_read = __import__("functools").partial(store.read, root=root)
    assert plan_loop._sustained_signal(store_read) is True
    plan_loop.signal(root, trigger=plan_loop.DATA_EVENT_TRIGGER,
                     dispatch=_LoopDispatch(_clean_authors()),
                     deid_client=_FixedDeidClient(_deid_summary()), plan_date=_T2_ON_DATE)
    assert _new_dated_sets(root, _T2_ON_DATE) == 1


def test_free_text_trigger_obeys_seven_day_floor(tmp_path):
    # FIX 3 (MEDIUM): the free-text trigger has NO independent sub-day bound — it obeys the SAME 7-day
    # min-interval floor as every trigger. A prior plan 3 days back blocks a free-text re-gen (the
    # 7-day floor, not a phantom 24h clock); a prior plan 17 days back lets it fire on a sustained
    # signal. The removed dead constant is asserted gone in test_debounce_parameters_are_pinned_constants.
    from scripts.serve import plan_loop

    dispatch = _LoopDispatch(_clean_authors())
    deid_client = _FixedDeidClient(_deid_summary())

    # (a) 3 days since last re-gen (< 7): blocked by the min-interval floor even with a sustained signal.
    inside = tmp_path / "inside"
    _seed_store(inside)
    _seed_prior_plan(inside, "2026-06-15")  # 3 days before _T2_ON_DATE
    _seed_biomarker(inside, "hrv", [40, 50, 60], _SUSTAINED_DATES)
    plan_loop.signal(inside, trigger=plan_loop.FREE_TEXT_TRIGGER,
                     dispatch=dispatch, deid_client=deid_client, plan_date=_T2_ON_DATE)
    assert _new_dated_sets(inside, _T2_ON_DATE) == 0, "free-text re-gen fired inside the 7-day floor"

    # (b) 17 days since last re-gen (>= 7) + sustained signal: the free-text trigger fires.
    outside = _sustained_root(tmp_path, "outside")  # old prior plan @ 2026-06-01 + sustained hrv
    plan_loop.signal(outside, trigger=plan_loop.FREE_TEXT_TRIGGER,
                     dispatch=dispatch, deid_client=deid_client, plan_date=_T2_ON_DATE)
    assert _new_dated_sets(outside, _T2_ON_DATE) == 1, "free-text re-gen did not fire past the 7-day floor"


def test_signal_raise_does_not_break_primary_handlers(tmp_path, monkeypatch):
    # FIX 4 (Security MEDIUM-1 / bug Finding 4): a raising loop `signal` must NEVER break a primary
    # handler's response — the loop notify is additive (the data already landed). Each of the three
    # trigger sites (route / confirm / care_chat) wraps `signal` fail-open. Pre-fix (no try/except) the
    # raise propagates out of the primary handler -> RED.
    from scripts.serve import care_chat, confirm, plan_loop, route
    from tests.serve.test_care_chat import _RecordingBackend, _seed
    from tests.serve.test_route import _write_healthkit_xml

    def boom(*a, **k):
        raise RuntimeError("plan-loop signal blew up")

    monkeypatch.setattr(plan_loop, "signal", boom)
    root = tmp_path / "store"
    _seed_store(root)
    _seed(root)  # care-profile fields for care_chat.respond

    # route.route_upload — the wearable land still returns its source unaffected.
    staged = tmp_path / "export.xml"
    _write_healthkit_xml(staged, day="2026-05-01", value="55")
    source = route.route_upload(staged, root=root, dna_root=tmp_path / "dna")
    assert source == "healthkit", "route_upload did not return normally despite a raising signal"

    # confirm.land_confirmed — the confirmed land still returns its receipt unaffected.
    receipt = confirm.land_confirmed(
        [{"item": "ferritin", "timepoint": "2026-05-01", "source": "labs", "value": "120"}],
        root=root,
    )
    assert receipt == {"store": ["ferritin"]}, "land_confirmed did not return its receipt"

    # care_chat.respond — the care-chat reply still returns unaffected.
    result = care_chat.respond("I slept 5 hours", [], client=_RecordingBackend(), store_root=root)
    assert "reply" in result and "receipt" in result, "care_chat.respond did not return its reply"
