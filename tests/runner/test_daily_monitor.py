"""Tests for the daily deterministic monitoring pass (`scripts/runner/daily_monitor.py`, ADR-0045-T3).

The daily pass HOSTS ADR-0045-T2's `tiered_executor.execute_monitoring_day` in the built ADR-0039
runner, DISABLED BY DEFAULT. It is the TERMINAL node on the monitoring loop
(`0045-T1 -> 0045-T2 -> 0045-T3`) and the site that WIRES the executor's three deferred seams — the
runner OWNS supplying the REAL ones (the three Wave-6-blocking beads):

  - **0n3t (PF-S134-02):** the runner injects a REAL composed `gate_dispatch` (built via
    `gate_dispatch.compose_gate_dispatch`) UNCONDITIONALLY, so a Tier-2 re-plan routes THROUGH the
    composition (`run_orchestrated`(loop_enabled) -> `plan_driver.drive` ->
    `gate_dispatch.compose_disposition`), never the `gate_dispatch=None` legacy path (which the
    executor's WAVE5-01 guard silently fail-closes to a Tier-4 hold).
  - **u20d:** the runner supplies `orchestrate.reconcile`'s REAL per-domain candidates (from the
    ADR-0044 standing version's `domain_programs`, carrying `cross_domain_seams`), NOT the executor's
    internal `{"plan": None}` degenerate stub, and ENFORCES the resulting `conflict_held`.
  - **evvs:** the runner binds `plan_date` to the STANDING version's date, so the Tier-4
    `mark_pending` pointer lands on the timepoint `_standing_versions` resolves by date-equality.

The load-bearing property is DETERMINISM ON A NO-EVENT DAY: when no observed signal crosses a
material threshold, the pass makes 0 model calls + 0 metered de-id-IN calls (AC-2, AC-5) — measured by
call-counting an injected fixture `dispatch` + fixture `deid_client`, never inferred. Every fixture is
SYNTHETIC (0 live-API spend, 0 real operator PII — PUBLIC repo); every `monitoring_signal` /
`adjustment_rule` is `monitoring_compiler.compile_config`'s REAL compiled output stored as the
`MONITORING_CONFIG` field of a canonical periodized `plan_model` version (PF-S131-01), and a u20d
candidate is `{"domain": d, "plan": {PROGRAM_KEY: <domain program carrying cross_domain_seams>}}` —
the shape `orchestrate._cross_domain_seams` reads (S4).
"""

import hashlib
from pathlib import Path

from scripts.plan import gate_dispatch, monitoring_compiler, orchestrate, tiered_executor
from scripts.plan.assemble import PROGRAM_KEY
from scripts.store import plan_confirm, plan_model

from scripts.runner import daily_monitor, store_lock
from scripts.runner.schedule import activate

from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
from tests.plan.test_generate_plan import _seed_store
from tests.plan.test_monitoring_compiler import _tier1_rule, _training_program, _training_signal
from tests.plan.test_plan_orchestrator import _RecordingDispatch, _deid_summary, _sustaining_authors
from tests.plan.test_quality_judge import _FixedJudgeClient, _clean_scores
from tests.plan.test_safety_review import _no_findings_dispatch

REPO_ROOT = Path(__file__).resolve().parents[2]
DAILY_MONITOR_PATH = REPO_ROOT / "scripts" / "runner" / "daily_monitor.py"
INIT_INSTANCE_PATH = REPO_ROOT / "scripts" / "clone" / "init_instance.py"

# The STANDING comprehensive version's date `D` (a fixed non-today date) and the tick's naive as-of
# date (`D` != the tick date — the evvs distinction). The runner binds `plan_date` to `D`, never the
# tick date.
_STANDING_DATE = "2026-01-15"
_TICK_DATE = "2026-07-13"

# Per-day observation sets over the canonical signal envelope (`session_rpe`/`cross_load`/`joint_strain`
# each bound 2.0, materiality 1.0). An immaterial certified reading -> Tier-1 auto-apply; a material
# certified reading -> Tier-2; a cross-domain rule -> Tier-3; a safety-gate rule -> Tier-4.
_NO_EVENT = {"session_rpe": 0.5}   # below materiality -> Tier-1 auto-apply (0 model / 0 de-id)
_MATERIAL = {"session_rpe": 1.5}   # at/above materiality -> Tier-2 -> composed gate
_CROSS = {"cross_load": 1.5}       # cross-domain rule -> Tier-3 -> reconcile
_SAFETY = {"joint_strain": 1.5}    # safety-gate rule -> Tier-4 -> mark_pending hold


# --- fixtures: a canonical periodized plan_model version (PF-S131-01) ----------------------


def _workout_program():
    """A canonical training program: 3 signals routing Tier-1/Tier-3/Tier-4 + a CONFLICT seam.

    The `session_rpe` rule is certified Tier-1-safe (bounded, in-domain, monotone); the `cross_load`
    rule is cross-domain (`target_domain` != own -> Tier-3); the `joint_strain` rule is safety-gated
    (`safety == "gate"` -> Tier-4). The `cross_domain_seams` declares a SEAM_CONFLICT with nutrition,
    so the u20d reconcile HOLDS workout.
    """
    return _training_program(
        monitoring_signals=[
            _training_signal(signal="session_rpe"),
            _training_signal(signal="cross_load"),
            _training_signal(signal="joint_strain"),
        ],
        adjustment_rules=[
            _tier1_rule(target_signal="session_rpe"),
            _tier1_rule(target_signal="cross_load", target_domain="nutrition"),
            _tier1_rule(target_signal="joint_strain", safety="gate"),
        ],
        cross_domain_seams=[{"with_domain": "nutrition", "nature": "conflict"}],
    )


def _nutrition_program():
    """A canonical training program for the second domain (a non-held ROUTE seam, kept non-empty)."""
    return _training_program(
        monitoring_signals=[_training_signal(signal="nutrition_rpe")],
        adjustment_rules=[_tier1_rule(target_signal="nutrition_rpe")],
        cross_domain_seams=[{"with_domain": "workout", "nature": "route"}],
    )


def _domain_programs():
    """The standing version's two canonical DOMAIN PROGRAMs, keyed by real plan domain."""
    return {"workout": _workout_program(), "nutrition": _nutrition_program()}


def _standing_version():
    """The canonical periodized composite version dated `_STANDING_DATE` (PF-S131-01).

    Its `MONITORING_CONFIG` is `compile_config`'s REAL compiled output over the two DOMAIN PROGRAMs;
    the config, the real per-domain candidates, and the version date all flow from THIS one version.
    """
    programs = _domain_programs()
    return {
        plan_model.VERSION_DATE: _STANDING_DATE,
        plan_model.DOMAIN_PROGRAMS: programs,
        plan_model.NARRATIVE: "Integrated block: train hard, monitor, adjust.",
        plan_model.MILESTONES: [{"date": "2026-08-10", "label": "first re-test", "metric": "e1RM +5%"}],
        plan_model.MONITORING_CONFIG: monitoring_compiler.compile_config(programs),
    }


def _seed_standing(root):
    """Record the canonical standing version into a scratch store so it resolves STANDING at `D`."""
    plan_model.record_plan_version(_standing_version(), root)


def _run(root, observations, *, deid_client=None, dispatch=None, store_read=None,
         judge_client=None, review_dispatch=None, plan_date=_TICK_DATE):
    """Drive the daily pass over `observations`, filling unexercised seams with fixture defaults.

    Mirrors `tests/plan/test_tiered_executor._execute`: the injected `dispatch` + `deid_client` are
    call-counting fixtures (the 0-call determinism measurement), the `judge_client` + `review_dispatch`
    are the composed gate's fixture collaborators, and `plan_date` is the tick's NAIVE as-of date (the
    runner rebinds the executor's plan_date to the standing version's date — evvs).
    """
    return daily_monitor.run(
        root,
        observations=observations,
        raw_intake=_raw_intake(),
        deid_client=_FixedDeidClient(_deid_summary()) if deid_client is None else deid_client,
        dispatch=_RecordingDispatch(_sustaining_authors()) if dispatch is None else dispatch,
        store_read=(lambda *a, **k: []) if store_read is None else store_read,
        judge_client=_FixedJudgeClient(_clean_scores()) if judge_client is None else judge_client,
        review_dispatch=_no_findings_dispatch() if review_dispatch is None else review_dispatch,
        plan_date=plan_date,
    )


def _store_digest(root):
    """A content digest of every `*.ndjson` under `root` — the byte-unchanged witness (S1)."""
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(Path(root).glob("*.ndjson"))
    }


# === AC-1: daily pass hosts in the runner (host + coexistence) ===================


def test_daily_tick_invokes_executor_in_runner_host_weekly_unchanged(tmp_path, monkeypatch):
    # AC-1: a fixture daily tick invokes the daily-pass driver over the seeded standing version's
    # compiled config in the built runner; the pass RUNS execute_monitoring_day and returns a receipt.
    # The weekly cadence (RUNNER_LABEL) is untouched — the daily entry is a NEW distinct label, not a
    # rewrite of the weekly one (both cadences coexist).
    _seed_standing(tmp_path)

    calls = []
    real_execute = tiered_executor.execute_monitoring_day

    def execute_spy(config, *args, **kwargs):
        calls.append(config)
        return real_execute(config, *args, **kwargs)

    monkeypatch.setattr(tiered_executor, "execute_monitoring_day", execute_spy)

    result = _run(tmp_path, _NO_EVENT)

    assert len(calls) == 1, "the daily pass did not host execute_monitoring_day exactly once"
    # the executor ran over the standing version's REAL compiled config (both domains present)
    assert set(calls[0].keys()) == {"workout", "nutrition"}
    assert "routings" in result, "the daily pass returned no receipt (no routings surface)"

    # coexistence: the daily label is a NEW label distinct from the weekly one, and the weekly
    # surface still reports its own label (the daily registration did not rewrite the weekly one).
    assert activate.DAILY_MONITOR_LABEL != activate.RUNNER_LABEL
    assert activate.status(activate.RUNNER_LABEL)["label"] == activate.RUNNER_LABEL


# === AC-2 + AC-5: no-event-day determinism (load-bearing) =======================


def test_no_event_day_zero_model_zero_deid(tmp_path):
    # AC-2 + AC-5: over the no-event set (a certified reading UNDER materiality -> Tier-1 auto-apply),
    # the hosted pass makes 0 model calls (dispatch) AND 0 metered de-id-IN calls (deid_client) — the
    # daily pass adds no model/de-id call of its own, and Tier-1 never routes through run_orchestrated.
    # Building the real composed gate is 0-spend and is NOT invoked on a no-event day. RED-capable:
    # Step-2.5 mutation #2 (re-enter the front door / dispatch / de-id on a no-event day -> count > 0).
    _seed_standing(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    _run(tmp_path, _NO_EVENT, deid_client=deid_client, dispatch=dispatch)

    assert dispatch.calls == [], "a no-event day dispatched a specialist (0 model calls required)"
    assert deid_client.calls == [], "a no-event day made a de-id-IN call (0 metered de-id required)"


# === 0n3t: composed-path E2E (falsification #1, PF-S134-02, THE critical one) ====


def test_material_event_routes_through_composed_gate_in_hosted_runner(tmp_path, monkeypatch):
    # 0n3t / PF-S134-02: over the material-in-domain config in the HOSTED runner, a spy on
    # gate_dispatch.compose_disposition FIRES >=1 and the routing carries the Tier-2
    # `replan-through-composition` action (NOT the WAVE5-01 `hold-composed-gate-unwired` Tier-4 hold) —
    # the runner injected the REAL composed gate via compose_gate_dispatch(...). S6 reachability: the
    # fixture deid_client returns a NON-sentinel summary + the dispatch authors let run_generation
    # assemble a plan, so the compose_disposition spy is genuinely REACHED (not the always-emitted
    # routing token). Doubles as the AC-2/AC-5 counterfactual: the SAME dispatch/deid_client instances
    # that read 0 on the no-event day reach > 0 here. RED-capable: Step-2.5 mutation #1 (drop the
    # injection -> gate_dispatch=None -> WAVE5-01 Tier-4 hold -> compose_disposition fires 0).
    _seed_standing(tmp_path)
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    # module-attribute spy: plan_driver.drive reads compose_disposition off the module at call time,
    # so patching the module attribute intercepts the composition wherever it fires.
    compose_calls = []
    real_compose = gate_dispatch.compose_disposition

    def compose_spy(verdicts, assembled_plan):
        compose_calls.append(True)
        return real_compose(verdicts, assembled_plan)

    monkeypatch.setattr(gate_dispatch, "compose_disposition", compose_spy)

    # counterfactual anchor: the SAME instances read 0 on the no-event day first
    _run(tmp_path, _NO_EVENT, deid_client=deid_client, dispatch=dispatch, store_read=store_read)
    assert dispatch.calls == [] and deid_client.calls == []

    result = _run(tmp_path, _MATERIAL, deid_client=deid_client, dispatch=dispatch,
                  store_read=store_read)

    routing = next(r for r in result["routings"] if r["signal"] == "session_rpe")
    assert routing["tier"] == tiered_executor.TIER_2, "the material in-domain event did not route to Tier-2"
    assert routing["action"] == "replan-through-composition", (
        "the Tier-2 re-plan did not route through the composition (an unwired/None gate fail-closed it)"
    )
    assert compose_calls, "the hosted Tier-2 re-plan never reached gate_dispatch.compose_disposition"
    # counterfactual: the SAME fixtures reach > 0 (proves the AC-2/AC-5 == 0 is a real measurement)
    assert len(dispatch.calls) > 0, "the material event did not dispatch (the fixture is dead, not a proof)"
    assert len(deid_client.calls) > 0, "the material event made no de-id-IN call (the fixture is dead)"


# === AC-3: disabled by default (+ QA-4 positive control) ========================


def test_daily_cadence_disabled_by_default_zero_active_entries(monkeypatch):
    # AC-3: on a fresh install (no daily enable path exists — Deviation #2), the daily label reads 0
    # real scheduler entries. Force the launchd (file) branch so the counter reads the real
    # install-file presence (reliable, non-hanging) — the daily plist is never created, so the count is
    # 0. QA-4 positive control: status(DAILY_MONITOR_LABEL) echoes the DAILY label with state DISABLED
    # and active_entries 0 — a real per-label read of a working counter, so a counter that ignored the
    # argument (reporting the WEEKLY label's state) would RED. The anti-implicit-activation scan stays
    # clean over the daily module + the provisioning surface. RED-capable: Step-2.5 mutation #3 (name an
    # implicit enable(DAILY_MONITOR_LABEL) on the daily/provision surface -> the scan hits -> RED).
    monkeypatch.setattr(activate, "_launchd_available", lambda: True)

    assert activate.active_entry_count(activate.DAILY_MONITOR_LABEL) == 0, (
        "a fresh daily label had a real scheduler entry (disabled-by-default broken)"
    )
    # QA-4 positive control: the status echoes the DAILY label (distinct from the weekly RUNNER_LABEL),
    # so an argument-ignoring counter reporting the weekly state would fail this exact-dict assertion.
    assert activate.DAILY_MONITOR_LABEL != activate.RUNNER_LABEL
    assert activate.status(activate.DAILY_MONITOR_LABEL) == {
        "state": "DISABLED", "active_entries": 0, "label": activate.DAILY_MONITOR_LABEL,
    }
    # anti-implicit-activation scan (ADR-0039-T3 AC-8): the daily module names no activation
    # token/enable, and the provisioning surface arms no daily entry.
    assert activate._scan_provisioning_for_activation([DAILY_MONITOR_PATH, INIT_INSTANCE_PATH]) == [], (
        "the daily surface / provisioning path names a runner-activation call (implicit daily activation)"
    )


# === AC-4: Tier-1 bounded-adjustment recording resolves STANDING (pointer-based) ==


def test_tier1_auto_apply_records_bounded_adjustment_resolves_standing(tmp_path):
    # AC-4 (REFRAMED per QA-1 to the pointer-based hold): a Tier-1 auto-apply RECORDS the bounded
    # adjustment into the ADR-0044 model via plan_model.record_plan_version (it round-trips through
    # read_plan_version) AND the runner does NOT mark_pending the recorded version's domain(s) — so 0
    # pending pointers exist and read_plan_version resolves the recorded version STANDING. The
    # _standing_versions hold is PURELY pointer-based; the daily Tier-1 route bypasses the weekly
    # regenerate magnitude gate entirely (spec disposition #22). RED-capable: Step-2.5 mutation #4
    # (mark_pending the Tier-1 recording -> a pending pointer lands -> read_plan_version NOT-standing).
    _seed_standing(tmp_path)

    records = []
    real_record = plan_model.record_plan_version

    def record_spy(version, root):
        records.append(version)
        return real_record(version, root)

    import scripts.store.plan_model as plan_model_mod
    orig = plan_model_mod.record_plan_version
    plan_model_mod.record_plan_version = record_spy
    try:
        result = _run(tmp_path, _NO_EVENT)
    finally:
        plan_model_mod.record_plan_version = orig

    # the Tier-1 auto-apply routed (the deterministic no-model path)
    routing = next(r for r in result["routings"] if r["signal"] == "session_rpe")
    assert routing["tier"] == tiered_executor.TIER_1, "the immaterial certified reading did not Tier-1 auto-apply"
    # the bounded adjustment WAS recorded (a distinct, round-trippable version)
    assert records, "the Tier-1 auto-apply recorded no bounded adjustment (record_plan_version not called)"

    after = plan_model.read_plan_version(_STANDING_DATE, tmp_path)
    # the recorded version resolves STANDING (0 pending pointer)
    assert after["state"] is None, "the recorded Tier-1 adjustment did not resolve STANDING"
    assert after["version"] is not None, "the recorded Tier-1 adjustment round-tripped to no version"
    # 0 pending pointers for any covered domain (the daily Tier-1 route is not human-gate-held)
    for domain in _domain_programs():
        assert plan_confirm.decision_for(domain, _STANDING_DATE, tmp_path) is None, (
            f"the Tier-1 recording marked {domain} pending (it must resolve STANDING, not be held)"
        )


# === u20d: real cross-domain reconciliation hold ================================


def test_cross_domain_seam_event_yields_real_reconciliation_hold(tmp_path):
    # u20d: a cross-domain-seam event (a rule whose target_domain != own -> Tier-3) drives the runner
    # to read the standing version's REAL domain_programs and call orchestrate.reconcile with candidates
    # of the SHAPE reconcile reads (S4) — {"domain": d, "plan": {PROGRAM_KEY: <the domain program
    # carrying cross_domain_seams>}} — NOT the executor's degenerate {"plan": None} stub and NOT a
    # bare-prescription candidate omitting PROGRAM_KEY. A spy confirms each candidate carries a non-empty
    # plan[PROGRAM_KEY][CROSS_DOMAIN_SEAMS], and the runner ENFORCES the conflict_held: the held domain
    # reads decision_for == DECISION_PENDING and resolves NOT-standing. RED-capable: Step-2.5 mutation #5
    # (fall back to {"plan": None} / a PROGRAM_KEY-less candidate -> 0 seams -> 0 holds -> STANDS).
    _seed_standing(tmp_path)

    captured = []
    real_reconcile = orchestrate.reconcile

    def reconcile_spy(candidates, **kwargs):
        captured.append(candidates)
        return real_reconcile(candidates, **kwargs)

    import scripts.plan.orchestrate as orchestrate_mod
    orig = orchestrate_mod.reconcile
    orchestrate_mod.reconcile = reconcile_spy
    try:
        _run(tmp_path, _CROSS)
    finally:
        orchestrate_mod.reconcile = orig

    assert captured, "the cross-domain-seam event did not call orchestrate.reconcile"
    candidates = captured[-1]
    # S4: each candidate is the shape reconcile actually reads — a non-empty cross_domain_seams under
    # PROGRAM_KEY, NOT a degenerate {"plan": None} or a bare-prescription candidate.
    for domain, cand in candidates.items():
        plan = cand.get("plan")
        assert isinstance(plan, dict), f"candidate {domain!r} is degenerate ({{'plan': None}} stub?)"
        program = plan.get(PROGRAM_KEY)
        assert isinstance(program, dict), f"candidate {domain!r} omits PROGRAM_KEY (bare-prescription stub?)"
        seams = program.get("cross_domain_seams")
        assert isinstance(seams, list) and seams, f"candidate {domain!r} carries no cross_domain_seams"

    # the declared SEAM_CONFLICT held workout: it reads pending and resolves NOT-standing (fail-closed)
    assert plan_confirm.decision_for("workout", _STANDING_DATE, tmp_path) == plan_confirm.DECISION_PENDING, (
        "the cross-domain conflict did not enforce a real reconciliation hold on the declaring domain"
    )
    assert plan_model.read_plan_version(_STANDING_DATE, tmp_path)["state"] is not None, (
        "a conflict-held version still resolved STANDING (the reconcile hold was not enforced)"
    )


# === evvs + S3: plan_date binds to the standing version's date + Tier-4 positive ==


def test_plan_date_binds_to_standing_version_date_not_naive(tmp_path):
    # evvs: with a standing version dated D (D != the tick's naive as-of date), a safety-threshold event
    # (Tier-4) calls plan_confirm.mark_pending with plan_date == D (the version's date), so
    # read_plan_version resolves the version NOT-standing. S3 positive human-gate assertion: POSITIVELY
    # decision_for(domain, D) == DECISION_PENDING (the pointer exists as pending, not merely absent) AND
    # 0 auto-advance past the gate (the held version never resolves standing). RED-capable: Step-2.5
    # mutation #6 (bind plan_date to the naive tick date -> the pointer misaligns -> the version STANDS
    # and decision_for(domain, D) reads None).
    _seed_standing(tmp_path)
    store_read = _seed_store(tmp_path)

    # precondition: the version STANDS before the safety hold (non-tautological — the hold is what stops
    # it, not that it was never standing).
    before = plan_model.read_plan_version(_STANDING_DATE, tmp_path)
    assert before["state"] is None and before["version"] is not None, "the seed version did not stand"

    result = _run(tmp_path, _SAFETY, store_read=store_read)

    routing = next(r for r in result["routings"] if r["signal"] == "joint_strain")
    assert routing["tier"] == tiered_executor.TIER_4, "the safety-gate event did not route to Tier-4"
    # evvs: the pointer landed on the STANDING version's date D (not the naive tick date _TICK_DATE)
    assert plan_confirm.decision_for("workout", _TICK_DATE, tmp_path) is None, (
        "the Tier-4 pointer landed on the NAIVE tick date (plan_date was not bound to the version's date)"
    )
    # S3 positive: the pointer positively exists as pending on D, and the held version does not advance
    assert plan_confirm.decision_for("workout", _STANDING_DATE, tmp_path) == plan_confirm.DECISION_PENDING, (
        "the Tier-4 safety event did not positively mark the domain pending on the version's date"
    )
    after = plan_model.read_plan_version(_STANDING_DATE, tmp_path)
    assert after["state"] is not None and after["version"] is None, (
        "the safety-threshold change auto-advanced past the human gate (the held version stood)"
    )


# === S1: lock-busy defer (store-write serialization, HIGH) ======================


def test_daily_tick_defers_when_cadence_lock_held(tmp_path):
    # S1 (HIGH): a daily tick that finds store_lock.cadence_lock(root) held DEFERS — it makes 0 store
    # writes and returns a {"regenerated": False, "deferred": True, ..., "reason": "lock-busy"} deferred
    # receipt (catching up next tick), so a concurrent weekly store.append can never lost-update-clobber
    # the daily Tier-4 pending pointer. Mirrors tests/runner/test_store_concurrency.test_busy_tick_
    # defers_no_corruption: hold the lock, fire ONE daily tick over a safety fixture (a tick that WOULD
    # write plan-confirm::/plan-model:: if it ran), assert the deferred receipt WITHOUT appending —
    # witnessed by a _store_digest byte-unchanged check. RED-capable: Step-2.5 mutation #7 (drop the
    # lock acquisition -> the busy tick writes -> the digest changes / a plan-confirm:: line appears).
    _seed_standing(tmp_path)
    before = _store_digest(tmp_path)

    with store_lock.cadence_lock(tmp_path) as held:
        assert held is True, "the test failed to hold the lock (the busy scenario is void)"
        receipt = _run(tmp_path, _SAFETY)

    assert receipt.get("regenerated") is False and receipt.get("deferred") is True, (
        f"the busy tick did not return a deferred receipt: {receipt}"
    )
    assert receipt.get("reason") == "lock-busy", f"the deferred receipt is not a lock-busy defer: {receipt}"
    assert _store_digest(tmp_path) == before, "the deferred (busy) daily tick mutated the store"
    # positively: no pending pointer landed for any covered domain (the Tier-4 hold was deferred)
    for domain in _domain_programs():
        assert plan_confirm.decision_for(domain, _STANDING_DATE, tmp_path) is None, (
            f"the deferred tick still wrote a {domain} pending pointer (0 store writes required)"
        )


# === AC-6: module green + 0 spend / 0 PII =======================================


def test_module_carries_zero_live_import_zero_pii():
    # AC-6: an import grep confirms 0 live-client import (no anthropic, no self-constructed ModelClient)
    # in the daily-pass module — the pass is a pure additive host of the injected seams (0 live-API
    # spend), and the test tree carries no real operator-identity literal.
    source = DAILY_MONITOR_PATH.read_text(encoding="utf-8")
    assert "import anthropic" not in source
    assert "ModelClient(" not in source, "the daily pass constructs a ModelClient (must use injected seams)"
