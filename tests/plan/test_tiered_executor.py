"""Tests for the four-tier deterministic executor (`scripts/plan/tiered_executor.py`, ADR-0045-T2).

The executor reads ADR-0045-T1's compiled `monitoring_config` + the day's monitoring-signal
observations and routes each observed signal-event into one of four escalation tiers,
**fail-closed by direction** (an unclassifiable or multi-tier event escalates to the HIGHER tier,
never guesses down). The load-bearing property is DETERMINISM ON A NO-EVENT DAY: when no signal
crosses a material threshold, the executor makes 0 model calls + 0 de-id-IN calls + 0 front-door
re-entries (AC-1) — measured by call-counting an injected fixture `dispatch` + fixture `deid_client`
+ a module-attribute spy on the front-door, never inferred.

The seven ACs + the seven Step-2.5 falsifiers are properties of ONE component exercised over the
SAME seeded synthetic fixtures (a REAL `compile_config` output — PF-S131-01, never a hand-built
stand-in). Every fixture is SYNTHETIC (0 live-API spend, 0 real operator PII — PUBLIC repo). The
tier semantics (SE Ask-vs-Proceed rule 3, stated in the recipe Deviation table):

  - observations is a per-signal reading set `{signal_name: observed_value}` the predicate classifies
    against the config's `{signal, bound, materiality_threshold}` envelope (an unobserved signal is
    no event);
  - a certified `TIER1_AUTO_APPLY_SAFE` in-domain rule gates on materiality — immaterial observation
    -> Tier-1 auto-apply (0 model calls), material observation -> Tier-2 (certified-but-material
    re-plan through the composed gate);
  - a `MUST_ESCALATE` cross-domain (`target_domain` != own) rule -> Tier-3, a safety-gate
    (`safety == "gate"`) rule -> Tier-4 — the structural escalations;
  - an in-domain un-certified `MUST_ESCALATE` rule escalates ONLY on a material observation (an
    immaterial un-certified rule does nothing — no unsafe auto-apply) and, positively implicating no
    tier, lands at the Tier-4 fail-closed-UP DEFAULT (F2);
  - a signal implicating more than one tier resolves to the MAX implicated tier (fail-closed-UP).
"""

import subprocess
from pathlib import Path

from scripts.plan import (
    adjust,
    gate_dispatch,
    monitoring_compiler,
    orchestrate,
    plan_orchestrator,
    tiered_executor,
)
from scripts.store import plan_confirm, plan_model

from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
from tests.plan.test_generate_plan import PLAN_DATE, _seed_store
from tests.plan.test_monitoring_compiler import (
    _ambiguous_rule,
    _tier1_rule,
    _training_program,
    _training_signal,
)
from tests.plan.test_plan_orchestrator import (
    _RecordingDispatch,
    _deid_summary,
    _sustaining_authors,
)
from tests.plan.test_quality_judge import _FixedJudgeClient, _clean_scores
from tests.plan.test_safety_review import _no_findings_dispatch

# The DURABLE FORK-POINT SHA (PF-S133-03): the permanent `main` ancestor the frozen-spine numstat
# probe diffs against — NOT a dynamic `git merge-base`, NOT an intermediate SHA.
DURABLE_FORK_POINT = "1cd134c25a09d623af5ecc9c0eed08a49040c7de"
REPO_ROOT = Path(__file__).resolve().parents[2]

_SIGNAL = "session_rpe"  # the canonical training signal (bound 2.0, materiality 1.0)
_IMMATERIAL = 0.5  # below the 1.0 materiality threshold -> no material event
_MATERIAL = 1.5  # at/above the 1.0 materiality threshold (and under the 2.0 bound) -> material


# --- fixtures: a REAL compiled config over the canonical program shape (PF-S131-01) ---------


def _compiled(rules):
    """Compile a one-domain ("workout") config carrying `rules` on the canonical training signal.

    Every signal/rule flows through the REAL `monitoring_compiler.compile_config` (never a
    hand-built config dict) — the PF-S131-01 canonical-fixture requirement. The domain is a REAL
    plan domain ("workout") so a Tier-2 re-plan can dispatch its specialist through `run_orchestrated`.
    """
    program = _training_program(
        monitoring_signals=[_training_signal()], adjustment_rules=list(rules)
    )
    return monitoring_compiler.compile_config({"workout": program})


def _execute(config, observations, root, *, raw_intake=None, deid_client=None, dispatch=None,
             store_read=None, plan_date=PLAN_DATE, gate_dispatch=None):
    """Drive the executor over `config` + `observations`, filling unexercised seams with defaults."""
    return tiered_executor.execute_monitoring_day(
        config,
        observations,
        _raw_intake() if raw_intake is None else raw_intake,
        _FixedDeidClient(_deid_summary()) if deid_client is None else deid_client,
        _RecordingDispatch(_sustaining_authors()) if dispatch is None else dispatch,
        (lambda *a, **k: []) if store_read is None else store_read,
        root,
        plan_date=plan_date,
        gate_dispatch=gate_dispatch,
    )


def _routing_for(result, signal):
    """The single tier-routing record the executor resolved for `signal` (fails if 0 or >1)."""
    matches = [r for r in result["routings"] if r["signal"] == signal]
    assert len(matches) == 1, f"expected exactly one routing for {signal!r}, got {matches}"
    return matches[0]


def _clean_composed_gate():
    """A REAL composed RAW-VERDICT producer (clean judge + 0-finding review) for a Tier-2 re-plan.

    Mirrors `test_plan_orchestrator.test_gate_dispatch_seam_fires_live`: over the assembled result it
    runs BOTH wired gate callables LIVE and returns their raw `{judge, review}` verdicts (ADR-0028-T1
    producer; the driver composes via `compose_disposition`). 0 live spend (fixture judge/review).
    """
    from scripts.plan.quality_judge import quality_judge
    from scripts.plan.safety_review import review_plan

    judge_client = _FixedJudgeClient(_clean_scores())
    lens_dispatch = _no_findings_dispatch()

    def producer(assembled_plan):
        return {
            "judge": quality_judge(assembled_plan, judge_client),
            "review": review_plan(assembled_plan, lens_dispatch),
        }

    return producer


def _seed_standing_version(root, domain, plan_date):
    """Record ONE standing comprehensive plan version at `plan_date` covering `domain`.

    So a Tier-4 `mark_pending(domain, plan_date, root)` can be OBSERVED to resolve the version
    NOT-standing (AC-4): before the hold, `read_plan_version` stands it; a covered-domain pending
    pointer then holds the whole version as a unit.
    """
    program = _training_program()
    version = {
        "date": plan_date,
        "domain_programs": {domain: program},
        "narrative": "Integrated block: train hard, monitor, adjust.",
        "milestones": [{"date": "2026-08-10", "label": "first re-test", "metric": "e1RM +5%"}],
        "monitoring_config": monitoring_compiler.compile_config({domain: program}),
    }
    plan_model.record_plan_version(version, root)


# === AC-1: no-event-day determinism (confirmation #1, LOAD-BEARING) =============


def test_no_event_day_zero_model_zero_deid_zero_reentry(tmp_path, monkeypatch):
    # AC-1: over a REAL compiled config on a day where NO signal crosses its materiality_threshold,
    # the executor makes 0 model calls (dispatch), 0 de-id-IN calls (deid_client), and 0 front-door
    # re-entries. The front-door spy is a RELIABLE module-attribute patch (F4): the executor
    # references `plan_orchestrator.run_orchestrated`, so the patch intercepts regardless of import
    # binding. The injected dispatch/deid_client 0-counts corroborate (run_orchestrated cannot
    # dispatch/de-id without them). RED-capable: Step-2.5 mutation #1 (front-door re-entry on a
    # no-event day) drives any count > 0.
    reentries = []

    def front_door_spy(*args, **kwargs):
        reentries.append((args, kwargs))
        return {"deidentified": False, "results": {}, "dispatch_count": 0}

    monkeypatch.setattr(plan_orchestrator, "run_orchestrated", front_door_spy)

    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    config = _compiled([_tier1_rule()])  # a certified Tier-1-safe in-domain rule
    result = _execute(
        config, {_SIGNAL: _IMMATERIAL}, tmp_path, deid_client=deid_client, dispatch=dispatch
    )

    assert dispatch.calls == [], "a no-event day dispatched a specialist (0 model calls required)"
    assert deid_client.calls == [], "a no-event day made a de-id-IN call (0 de-id required)"
    assert reentries == [], "a no-event day re-entered the front door (0 re-entries required)"
    # the certified rule was Tier-1 auto-applied (the deterministic no-model path), never escalated
    assert _routing_for(result, _SIGNAL)["tier"] == tiered_executor.TIER_1


def test_event_day_same_fixtures_reach_nonzero(tmp_path):
    # AC-1 counterfactual control (B2): the SAME dispatch/deid_client INSTANCES that read 0 on the
    # no-event day reach call_count > 0 over an EVENT-day (material-in-domain) config — Tier-2 routes
    # through `run_orchestrated`, which consumes them. Proves the AC-1 == 0 is a real measurement, not
    # a dead never-called fixture. (A positive control paired to AC-1, not a mutation-battery row.)
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    config = _compiled([_tier1_rule()])  # certified rule

    # no-event first: the SAME instances read 0 (the counterfactual anchor)
    _execute(config, {_SIGNAL: _IMMATERIAL}, tmp_path,
             deid_client=deid_client, dispatch=dispatch, store_read=store_read)
    assert dispatch.calls == [] and deid_client.calls == []

    # event day: a material observation on the certified in-domain rule -> Tier-2 -> run_orchestrated
    result = _execute(config, {_SIGNAL: _MATERIAL}, tmp_path, deid_client=deid_client,
                      dispatch=dispatch, store_read=store_read, gate_dispatch=_clean_composed_gate())

    assert len(dispatch.calls) > 0, "the event day did not dispatch (the fixture is dead, not a proof)"
    assert len(deid_client.calls) > 0, "the event day made no de-id-IN call (the fixture is dead)"
    assert _routing_for(result, _SIGNAL)["tier"] == tiered_executor.TIER_2


# === AC-2: finding-A parity — Tier-2 re-plans THROUGH the composition (PF-S133-02) ===


def test_material_in_domain_replans_through_composition_not_bare_leg(tmp_path, monkeypatch):
    # AC-2: a material in-domain event routes to Tier-2 and the re-plan reaches the composed gate —
    # a spy on `compose_disposition` FIRES (the re-plan applied the composed gate + per-domain floor +
    # the fail-closed `safety_passed is True` surface gate, the SAME composition ADR-0043-T3's Leg-1
    # uses), AND a spy on `adjust.adjust_plan` records 0 calls (NEVER the bare single-domain leg).
    # RED-capable: Step-2.5 mutation #2 (route Tier-2 through `adjust.adjust_plan`). Backstop bead
    # `a-plus-maxing-kn29` (not re-scoped here).
    store_read = _seed_store(tmp_path)

    compose_calls = []
    real_compose = gate_dispatch.compose_disposition

    def compose_spy(verdicts, assembled_plan):
        compose_calls.append(True)
        return real_compose(verdicts, assembled_plan)

    # module-attribute patch: `plan_driver.drive` lazily does `from ...gate_dispatch import
    # compose_disposition` at call time, so patching the module attribute intercepts the composition.
    monkeypatch.setattr(gate_dispatch, "compose_disposition", compose_spy)

    adjust_calls = []
    monkeypatch.setattr(adjust, "adjust_plan", lambda *a, **k: adjust_calls.append(True))

    config = _compiled([_tier1_rule()])
    result = _execute(config, {_SIGNAL: _MATERIAL}, tmp_path,
                      store_read=store_read, gate_dispatch=_clean_composed_gate())

    assert _routing_for(result, _SIGNAL)["tier"] == tiered_executor.TIER_2
    assert compose_calls, "the Tier-2 re-plan did not reach the composed gate (compose_disposition)"
    assert adjust_calls == [], "the Tier-2 re-plan called the bare adjust.adjust_plan leg (finding-A)"


# === AC-3: cross-domain -> Tier-3 reconciler (confirmation #3) ===================


def test_cross_domain_seam_escalates_to_tier3_reconciler_not_auto_applied(tmp_path, monkeypatch):
    # AC-3: a cross-domain-seam adjustment (a rule whose target_domain != its own domain) routes to
    # Tier-3 (the `orchestrate.reconcile` spy FIRES) and is NOT auto-applied at Tier-1 (0 cross-domain
    # Tier-1 auto-applies). RED-capable: Step-2.5 mutation #3 (auto-apply the cross-domain event at
    # Tier-1, skipping reconcile).
    reconcile_calls = []
    real_reconcile = orchestrate.reconcile

    def reconcile_spy(candidates, **kwargs):
        reconcile_calls.append(candidates)
        return real_reconcile(candidates, **kwargs)

    monkeypatch.setattr(orchestrate, "reconcile", reconcile_spy)

    config = _compiled([_tier1_rule(target_domain="nutrition")])  # cross-domain -> MUST_ESCALATE
    result = _execute(config, {_SIGNAL: _IMMATERIAL}, tmp_path)

    routing = _routing_for(result, _SIGNAL)
    assert routing["tier"] == tiered_executor.TIER_3, "cross-domain did not escalate to Tier-3"
    assert reconcile_calls, "Tier-3 did not call orchestrate.reconcile (the cross-domain reconciler)"
    # 0 cross-domain auto-applied at Tier-1 (the mis-classification-too-little guard)
    assert not [r for r in result["routings"] if r["tier"] == tiered_executor.TIER_1]


# === AC-4: safety-threshold HELD at Tier-4 (falsification #1; Ruling 1 / Option B) ===


def test_safety_threshold_holds_at_tier4_decision_pending_not_standing(tmp_path):
    # AC-4 (STRENGTHENED per Ruling 1 / Option B to a POSITIVE assertion): a safety-threshold event
    # (`safety == "gate"`) HOLDS at Tier-4 because the executor CALLS `plan_confirm.mark_pending`
    # directly for the safety-affected domain — magnitude-INDEPENDENT. Asserts POSITIVELY
    # `decision_for == DECISION_PENDING` AND `read_plan_version` resolves the safety-affected version
    # NOT-standing (0 auto-advance past the human/medical-liaison gate). RED-capable: Step-2.5 mutation
    # #4 (DROP the mark_pending write -> decision_for returns None -> the version STANDS).
    store_read = _seed_store(tmp_path)
    _seed_standing_version(tmp_path, "workout", PLAN_DATE)

    # precondition: the version STANDS before the safety hold (non-tautological — the hold is what
    # stops it, not that it was never standing)
    before = plan_model.read_plan_version(PLAN_DATE, tmp_path)
    assert before["state"] is None and before["version"] is not None, "the seed version did not stand"

    config = _compiled([_tier1_rule(safety="gate")])  # safety-gate -> MUST_ESCALATE
    result = _execute(config, {_SIGNAL: _MATERIAL}, tmp_path, store_read=store_read)

    assert _routing_for(result, _SIGNAL)["tier"] == tiered_executor.TIER_4
    # POSITIVE assertion: the executor marked the domain pending (the human-gate hold)
    assert plan_confirm.decision_for("workout", PLAN_DATE, tmp_path) == plan_confirm.DECISION_PENDING
    # and the safety-affected version resolves NOT-standing (0 auto-advance)
    after = plan_model.read_plan_version(PLAN_DATE, tmp_path)
    assert after["state"] is not None, "the safety-threshold change advanced past the human gate (stood)"
    assert after["version"] is None, "a held safety version still resolved standing"


# === AC-5: out-of-bounds / un-certifiable entry surfaces a rejection (falsification #3, F3) ===


def test_out_of_bounds_entry_surfaces_rejection_zero_tier1_auto_apply(tmp_path):
    # AC-5 (F3: a SURFACED, observable rejection, NOT a silent discard): a mis-compiled out-of-bounds /
    # un-certifiable (non-`TIER1_AUTO_APPLY_SAFE`) entry ESCALATES / is REJECTED with an OBSERVABLE
    # escalation record PRESENT in the tier-routing result — 0 out-of-bounds Tier-1 auto-applies. The
    # test asserts the rejection's PRESENCE (not merely the absence of a Tier-1 apply). RED-capable:
    # Step-2.5 mutation #5 (auto-apply at Tier-1, OR silently discard with no surfaced record).
    config = _compiled([_ambiguous_rule()])  # missing direction -> un-certifiable -> MUST_ESCALATE
    result = _execute(config, {_SIGNAL: _MATERIAL}, tmp_path)

    # the un-certifiable entry is SURFACED (present in the routing result), never silently dropped
    routing = _routing_for(result, _SIGNAL)
    assert routing["tier"] != tiered_executor.TIER_1, "an un-certifiable entry auto-applied at Tier-1"
    # 0 un-certifiable entries auto-applied at Tier-1 across the whole result
    assert not [r for r in result["routings"] if r["tier"] == tiered_executor.TIER_1]


# === AC-6: fail-closed by direction (two tests) =================================


def test_ambiguous_multi_tier_event_escalates_up_to_higher_tier(tmp_path, monkeypatch):
    # AC-6 (max-of-implicated): a B3-constructed ambiguous signal — ONE (immaterial) observation
    # matching BOTH an in-domain Tier-1 rule (-> Tier-1) AND a cross-domain rule (-> Tier-3 structural)
    # — resolves to Tier-3 (the HIGHER IMPLICATED tier), never a guessed Tier-1 auto-apply. RED-capable:
    # Step-2.5 mutation #6 (resolve the multi-tier event DOWN to the lower implicated tier).
    monkeypatch.setattr(orchestrate, "reconcile", lambda candidates, **kw: {"report": {}})

    # two rules on the SAME signal: certified in-domain (Tier-1) + cross-domain (Tier-3) — the one
    # event genuinely implicates two tiers. Immaterial observation, so the certified rule is Tier-1
    # (not Tier-2) and the ambiguity is the recipe's Tier-1 + Tier-3.
    config = _compiled([_tier1_rule(), _tier1_rule(target_domain="nutrition")])
    result = _execute(config, {_SIGNAL: _IMMATERIAL}, tmp_path)

    assert _routing_for(result, _SIGNAL)["tier"] == tiered_executor.TIER_3, (
        "a multi-tier event did not escalate UP to the higher implicated tier (Tier-3)"
    )


def test_no_tier_implicated_must_escalate_defaults_to_tier4(tmp_path):
    # AC-6 (F2 / Ruling 2, the fail-closed-UP DEFAULT): a `MUST_ESCALATE` entry the predicate cannot
    # positively pin to Tier-2 (material in-domain), Tier-3 (cross-domain), or Tier-4-by-safety — a
    # non-monotone in-domain escalate rule, NO tier positively implicated — lands at Tier-4 by DEFAULT
    # (held per AC-4: decision_for == DECISION_PENDING, NOT-standing), NEVER Tier-1/2/3. RED-capable:
    # Step-2.5 mutation #7 (route a no-tier-implicated MUST_ESCALATE DOWN to Tier-1/2/3). Non-overlapping
    # with mutation #6 (which targets a POSITIVELY Tier-1+Tier-3-implicated ambiguity).
    store_read = _seed_store(tmp_path)
    _seed_standing_version(tmp_path, "workout", PLAN_DATE)

    config = _compiled([_tier1_rule(direction=["increase", "decrease"])])  # non-monotone -> MUST_ESCALATE
    result = _execute(config, {_SIGNAL: _MATERIAL}, tmp_path, store_read=store_read)

    assert _routing_for(result, _SIGNAL)["tier"] == tiered_executor.TIER_4, (
        "a no-tier-implicated MUST_ESCALATE did not default to the fail-closed-UP Tier-4"
    )
    # held per AC-4 (the terminal fail-closed tier), never advanced
    assert plan_confirm.decision_for("workout", PLAN_DATE, tmp_path) == plan_confirm.DECISION_PENDING
    assert plan_model.read_plan_version(PLAN_DATE, tmp_path)["version"] is None


# === AC-7: module green + 0 spend / 0 PII =======================================


def test_module_carries_zero_live_import_zero_pii():
    # AC-7: an import grep confirms 0 live-client import (no `anthropic`, no self-constructed
    # ModelClient) and no real operator-identity literal in the executor module — the tier-routing
    # engine is a pure additive consumer of the injected seams (0 live-API spend).
    source = (REPO_ROOT / "scripts/plan/tiered_executor.py").read_text(encoding="utf-8")
    assert "import anthropic" not in source
    assert "ModelClient(" not in source, "the executor constructs a ModelClient (must use injected seams)"


# === B4: adjust.py frozen (finding-A parity durability, PF-S133-02) =============


def test_adjust_py_untouched_numstat_empty():
    # B4: the Tier-2 route THROUGH the composition keeps the bare `adjust.adjust_plan` leg byte-frozen.
    # A durable pytest regression of the frozen-spine numstat probe (not only the Step-4 shell
    # command), against the DURABLE FORK-POINT SHA (PF-S133-03), never a dynamic merge-base.
    diff = subprocess.run(
        ["git", "diff", "--numstat", DURABLE_FORK_POINT, "--", "scripts/plan/adjust.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert diff.stdout.strip() == "", f"adjust.py is not byte-frozen (finding-A parity):\n{diff.stdout}"
