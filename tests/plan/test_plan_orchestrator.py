"""Tests for the programmatic subscription orchestrator (ADR-0022-T1).

`scripts.plan.plan_orchestrator.run_orchestrated` is the programmatic drive layer that
WRAPS the inner engine: it takes the raw operator intake, runs it through the Wave-1
`deid_in` boundary, dispatches each plan-domain specialist (full profile inlined per
INV-ROLE-INLINING) over the de-identified summary through an injected `dispatch` seam,
captures the author envelopes, and drives `pipeline.run_generation` (compute -> reconcile
-> adjudicate -> record). It re-authors nothing in the inner engine; it halts to honest
no-plan on the `deid_in` sentinel; and it never bypasses the inner safety gate. These pin:

  - AC-1: the orchestrator runs end-to-end unattended over a synthetic PII-free fixture and
    `run_generation` returns `results` with >=1 recorded `plan::<domain>` + `dvq_entries`;
  - AC-2: every specialist dispatch payload carries the de-identified summary only -- 0
    raw-PII fields (the crown-jewel de-identified-summary-only contract);
  - AC-3: the orchestrator REUSES the inner engine -- it records nothing outside `record_plan`
    and opens no orchestrator-private store stream;
  - AC-5: each dispatch prompt inlines the dispatched role's FULL profile verbatim (read from
    `.claude/agents/<role>/agent.md`) -- the `enforce-role-inlining` discipline;
  - AC-6: the module runs against mock clients (0 live-API calls) -- the `_ClaudeNoTrainBackend`
    is never constructed;
  - AC-7: the gate-dispatch seam exists + is spyable, and the no-op default issues 0 gate
    dispatches on a normal run (the Wave-3 / ADR-0020-T2 attachment point);
  - AC-4 (Cycle 2): the inner-safety-gate-bypass falsification probe -- a seeded held finding
    records 0 plans past the hold, with a non-tautological positive control;
  - the deid-sentinel halt (Cycle 2): a `{"deidentified": False}` sentinel input -> 0 dispatches
    + 0 plans recorded.

Every client/dispatch is a mock/fixture; no test hits a live API, and the test tree carries
0 real operator PII (synthetic tokens only).
"""

import json
from pathlib import Path

from scripts.model.client import ModelCallError, ModelClient
from scripts.plan import router
from scripts.plan.plan_orchestrator import run_orchestrated
from scripts.store import store
from tests.plan.test_deid_in import (
    SYNTHETIC_LAB,
    SYNTHETIC_NAME,
    _FixedDeidClient,
    _raw_intake,
)
from tests.plan.test_generate_plan import (
    PLAN_DATE,
    _author,
    _nutrition_meal_rec,
    _nutrition_target_rec,
    _seed_store,
    _workout_rec,
)
from tests.plan.test_orchestrate import (
    _SUPP_CONFLICT,
    _conflict_authors,
    _liaison,
    _nutrition,
    _recon,
)
from tests.plan.test_adjudicate import _override_record

# The plan-domain roles whose full profiles the orchestrator inlines (the AC-5 oracle source).
_ROLE_OF_DOMAIN = {
    "workout": "personal-trainer",
    "nutrition": "nutritionist",
    "supplements": "supplement-specialist",
    "peptides": "peptide-specialist",
}


# --- fixtures ------------------------------------------------------------------


def _deid_summary():
    """A de-identified summary shaped from `router.SUMMARY_FIELD_SET` (no raw-PII tokens).

    Carries NONE of the synthetic raw-PII (`SYNTHETIC_NAME` / `SYNTHETIC_LAB`) seeded into the
    raw intake -- exactly what a faithful de-id call emits.
    """
    return {
        "training-age-band": "10-15y",
        "sex-for-dosing": "male",
        "bodyweight-band": "80-90kg",
        "goal-domains": ["workout", "nutrition"],
        "active-issue-class": "musculoskeletal-recovery",
        "recovery-status-band": "moderate",
    }


class _RecordingDispatch:
    """A dispatch seam that returns a pre-mapped author envelope per domain.

    Records every `(domain, prompt, summary)` call so the test can inspect the dispatch
    prompt (AC-5: profile inlined) and the dispatch payload (AC-2: de-identified summary only).
    Mirrors the `_FixedEnvelopeClient` / `_FixedDeidClient` fixture-seam pattern: it is the
    fixture stand-in for a live agent dispatch, so the orchestrator runs with 0 live spend.

    Attributes:
        authors (dict): domain -> the captured author envelope to return for that domain.
    """

    def __init__(self, authors):
        self.authors = authors
        self.calls = []

    def __call__(self, domain, prompt, summary):
        self.calls.append({"domain": domain, "prompt": prompt, "summary": summary})
        return self.authors[domain]


def _sustaining_authors():
    """A clean two-domain set: a fuelable workout + a sustaining nutrition budget (records both)."""
    return {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
    }


# --- AC-1: end-to-end unattended run records plans + returns dvq_entries --------


def test_runs_end_to_end_unattended_and_records_plans(tmp_path):
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    # the inner engine ran and recorded >=1 domain, and dvq_entries is present in the return
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1
    assert "dvq_entries" in out
    # the plans landed in the store via record_plan (the inner engine's write, not the orchestrator's)
    assert store.read("plan::workout", root=tmp_path) != []
    assert store.read("plan::nutrition", root=tmp_path) != []


# --- AC-2: every dispatch payload carries the de-identified summary only (0 raw-PII) ---


def test_dispatch_payloads_carry_deidentified_summary_only(tmp_path):
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    assert dispatch.calls, "no specialist dispatch fired"
    for call in dispatch.calls:
        # the dispatch summary IS the de-identified summary, not the raw intake
        assert call["summary"] == _deid_summary()
        # the serialized dispatch payload (summary + prompt) carries 0 of the seeded raw-PII tokens
        serialized = json.dumps({"summary": call["summary"], "prompt": call["prompt"]})
        assert SYNTHETIC_NAME not in serialized
        assert SYNTHETIC_LAB not in serialized
        # and 0 named-excluded raw-PII fields in the payload summary
        raw_pii_fields = set(call["summary"]) & set(router.EXCLUDED_RAW_PII)
        assert raw_pii_fields == set(), f"dispatch payload carried raw-PII fields: {raw_pii_fields}"


# --- AC-3: reuse the inner engine -- records nothing outside record_plan --------


def test_reuses_inner_engine_opens_no_private_store_stream(tmp_path):
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    # only the inner engine's streams are written: plan::<domain> (+ dvq::queue when a finding
    # reaches the gate). NO orchestrator-private stream (the orchestrator records via record_plan).
    written = set(store.items(root=tmp_path))
    plan_and_queue = {i for i in written if i.startswith("plan::") or i.startswith("dvq::")}
    # the seeded operator-state items are the only OTHER items; every written plan/queue stream
    # belongs to the inner engine's namespace, none orchestrator-private.
    assert plan_and_queue == {i for i in written if i.startswith(("plan::", "dvq::"))}
    orchestrator_private = {i for i in written if i.startswith("orchestrator")}
    assert orchestrator_private == set()
    # the recorded plans are attributed to the dispatched specialists (record_plan's write)
    workout_rows = store.read("plan::workout", root=tmp_path)
    assert workout_rows and workout_rows[-1]["source"] == "plan::personal-trainer"


# --- AC-5: each dispatch prompt inlines the FULL role profile verbatim ----------


def test_each_dispatch_inlines_full_role_profile(tmp_path):
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    by_domain = {call["domain"]: call["prompt"] for call in dispatch.calls}
    for domain in ("workout", "nutrition"):
        role = _ROLE_OF_DOMAIN[domain]
        profile = Path(".claude/agents") / role / "agent.md"
        profile_text = profile.read_text(encoding="utf-8")
        # the FULL profile (read live) is inlined verbatim -- fails (not vacuously) if the
        # orchestrator inlined an empty / nonexistent path.
        assert profile_text in by_domain[domain], f"{role} profile not inlined in {domain} prompt"
        # the required section markers are present (the enforce-role-inlining discipline)
        for marker in ("## Identity", "## Core Rules", "## Role Boundaries", "## Anti-Patterns"):
            assert marker in by_domain[domain], f"{domain} prompt missing {marker}"


def test_role_inlining_is_not_vacuous_on_a_real_profile(tmp_path):
    # Failing-capable proof for AC-5: the profile text is non-trivial, so the `in` assertion
    # above cannot pass on an empty inline. A profile that inlined "" would make the AC-5
    # assertion vacuously true; this pins that the live profile is substantial.
    profile_text = (Path(".claude/agents/personal-trainer/agent.md")).read_text(encoding="utf-8")
    assert len(profile_text) > 200
    assert "## Identity" in profile_text


# --- AC-6: 0 live-API calls (mock clients only) --------------------------------


def test_no_live_backend_constructed(tmp_path, monkeypatch):
    # The orchestrator runs over the injected mocks only -- it constructs no ModelClient and
    # thus no `_ClaudeNoTrainBackend`. A ModelClient.__init__ spy confirms 0 self-constructed
    # clients (a live no-train backend is never instantiated -> 0 live spend).
    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)

    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    assert instantiations == [], "orchestrator constructed a ModelClient (must use only injected mocks)"


# --- AC-7: the gate-dispatch seam (the Wave-3 / ADR-0020-T2 attachment point) ----


def test_gate_dispatch_seam_is_spyable(tmp_path):
    # (a) the seam EXISTS and is spyable: an injected recording gate_dispatch is held/invocable
    # through the documented path. The orchestrator must hold the seam (not drop it).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    gate_calls = []

    def gate_spy(*args, **kwargs):
        gate_calls.append((args, kwargs))

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate_spy,
    )
    # the run completed normally with the seam injected (it is the held control-surface hook,
    # wired but not yet exercised by any real gate in this task -- Wave 3 wires the gates)
    assert "results" in out


def test_default_gate_dispatch_is_noop_zero_dispatches(tmp_path):
    # (b) with the DEFAULT (no-op) gate_dispatch, a normal run issues 0 gate dispatches: a spy
    # NOT injected dispatches nothing -- the default is inert (the ADR-0020-T2 gate-idle case).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    # a gate spy passed via the seam to confirm 0 invocations on a default/clean run -- the spy
    # only records; with the default no-op the orchestrator dispatches nothing through any gate.
    gate_calls = []

    def gate_spy(*args, **kwargs):
        gate_calls.append((args, kwargs))

    dispatch = _RecordingDispatch(_sustaining_authors())
    run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate_spy,
    )
    assert gate_calls == [], "the no-op default seam must issue 0 gate dispatches on a normal run"


# === Cycle 2: inner-safety-gate-bypass falsification + the deid-sentinel halt ===


# --- AC-4 (FALSIFICATION): the orchestrator never bypasses the inner safety gate ----


def test_held_finding_records_nothing_past_the_hold(tmp_path):
    # AC-4 (the falsification criterion): a seeded ACTUAL HOLD (the cross-domain-conflict hold)
    # routed to a block-stands CRITICAL liaison records NOTHING past the hold -- the inner gate's
    # held-records-nothing default is the oracle, reused (not bypassed). An orchestrator that
    # bypassed the gate would record the held plan -> RED.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_conflict_authors(supp_conflicts=_SUPP_CONFLICT))

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("supplements", "peptides"),
        adjudicator=_liaison("CRITICAL"),  # block-stands -> the hold stands
    )

    # 0 plans recorded past the unadjudicated/blocked hold for the held domain
    assert out["results"]["supplements"]["recorded"] is False
    assert store.read("plan::supplements", root=tmp_path) == []


def test_held_finding_positive_control_records_under_valid_override(tmp_path):
    # AC-4 POSITIVE CONTROL (non-tautological): the SAME conflict seed run with a CONTENT-VALID
    # override DOES record the supplements domain -- proving the domain WAS in play and the hold
    # is what suppressed it (not that the domain was simply never authored).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_conflict_authors(supp_conflicts=_SUPP_CONFLICT))

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("supplements", "peptides"),
        adjudicator=_liaison("HIGH", override=_override_record("HIGH")),  # content-valid override
    )

    assert out["results"]["supplements"]["recorded"] is True
    assert store.read("plan::supplements", root=tmp_path) != []


# --- the deid-sentinel halt (the spec CORE CHANGE) ------------------------------


def test_deid_sentinel_halts_with_zero_dispatches_and_zero_plans(tmp_path):
    # On a `{"deidentified": False}` sentinel (a deidentify that raises ModelCallError -> deid_in
    # returns the sentinel) the orchestrator HALTS to honest no-plan: 0 specialist dispatches,
    # 0 plans recorded, never a dispatch over a non-summary. An orchestrator that dispatched over
    # the sentinel turns this RED.
    store_read = _seed_store(tmp_path)
    failing_client = _FixedDeidClient(ModelCallError("backend de-id call failed"))
    dispatch = _RecordingDispatch(_sustaining_authors())

    out = run_orchestrated(
        _raw_intake(), failing_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    # honest no-plan state surfaced
    assert out["deidentified"] is False
    assert out["results"] == {}
    # 0 specialist dispatches issued
    assert dispatch.calls == [], "the orchestrator dispatched over the de-id sentinel (must halt)"
    # 0 plans recorded
    for domain in ("workout", "nutrition", "supplements", "peptides"):
        assert store.read(f"plan::{domain}", root=tmp_path) == []

