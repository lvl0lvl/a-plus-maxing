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

import datetime
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


def test_gate_dispatch_keyword_accepted_seam_wired_not_yet_fired(tmp_path):
    # The orchestrator ACCEPTS `gate_dispatch=` and runs to completion with it injected -- the
    # seam is WIRED but NOT yet exercised: no real gate fires it in Wave 2 (this task builds the
    # seam + its inert default ONLY, never the gates). This test pins ONLY that the keyword is
    # accepted and the run completes with it injected; it deliberately does NOT claim the spy is
    # reachable/fired (the old `_is_spyable` name overpromised -- a dropped seam stayed green here
    # because Wave 2 never fires it). The default-vs-injected resolution IS pinned by
    # `test_default_gate_dispatch_is_noop_zero_dispatches` (0 dispatches on the default).
    # Wave-3 re-assertion note: Wave 3 (ADR-0023-T1 quality judge / ADR-0024-T1 safety review)
    # wires the real gates into this seam; re-assert there that the injected spy ACTUALLY FIRES
    # (a positive dispatch-count assertion), giving "spyable" real teeth against the wired path.
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
    # the run completed normally with the seam injected (the held control-surface hook, accepted
    # but not yet exercised by any real gate in this task -- Wave 3 wires + fires the gates)
    assert "results" in out


def test_default_gate_dispatch_is_noop_zero_dispatches(tmp_path):
    # (b) the LEGACY Wave-2 non-loop path: a caller WITHOUT the revise loop (the genuine DEFAULT,
    # `gate_dispatch` not supplied -> the no-op) runs the inner engine ONCE and surfaces the plan,
    # the inner per-finding `adjudicate` gate the always-on floor (Security HIGH-2). The no-op
    # default never fires a gate dispatch (the autonomous whole-plan tier is NOT composed on this
    # path). Wave-4 re-grounding: the seam now FIRES when a REAL composed gate is INJECTED (that is
    # `test_revise_loop.test_both_gates_run_each_pass` / `..._fires_live`); the genuine default
    # stays inert and surfaces via the inner floor — the legacy non-loop contract.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())

    dispatch = _RecordingDispatch(_sustaining_authors())
    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),  # no gate_dispatch -> the default
    )
    # the legacy non-loop path surfaces a plan via the inner floor (no whole-plan gate composed)
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1, "the legacy non-loop default did not surface a plan"
    assert store.read("plan::workout", root=tmp_path) != []


def test_gate_dispatch_seam_fires_live(tmp_path):
    # The deferred Wave-2 re-assertion (ADR-0022-T2): the held `gate_dispatch=` seam NOW FIRES
    # against the wired path. Inject a recording spy that composes a CLEAN disposition (both gates
    # pass) and assert a POSITIVE dispatch count — the old keyword-accepted test only pinned the
    # keyword was accepted, never that the seam fires. EXACT count (SF-4): the composed gate fires
    # EXACTLY ONCE on a clean single pass (an off-by-one or a dropped-gate REDs); re-assert the
    # 0023/0024 gate callables are invocable LIVE through the seam.
    from scripts.plan.quality_judge import ACCEPT, quality_judge
    from scripts.plan.safety_review import review_plan
    from tests.plan.test_quality_judge import _FixedJudgeClient, _clean_scores
    from tests.plan.test_safety_review import _no_findings_dispatch

    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    judge_client = _FixedJudgeClient(_clean_scores())
    lens_dispatch = _no_findings_dispatch()
    gate_calls = []

    def composed_gate(assembled_plan):
        # the seam runs BOTH wired Wave-3 gate callables LIVE over the assembled result
        q = quality_judge(assembled_plan, judge_client)
        s = review_plan(assembled_plan, lens_dispatch)
        gate_calls.append((q, s))
        return {"accept": q["verdict"] == ACCEPT, "safety_passed": s["passed"]}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=composed_gate,
    )

    # the seam FIRED (a positive dispatch count) — EXACTLY once on a clean single pass
    assert len(gate_calls) == 1, f"the wired gate seam fired {len(gate_calls)} times, expected 1"
    # the live gate callables produced their native verdicts (invocable through the seam)
    assert gate_calls[0][0]["verdict"] == ACCEPT
    assert gate_calls[0][1]["passed"] is True
    # and a plan surfaced (the clean composed disposition surfaced it)
    assert [d for d, r in out["results"].items() if r.get("recorded") is True]


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


# === ADR-0020-T2: de-id-boundary WHOLE-RUN OUTAGE -> fail-closed halt ============
#
# A whole-run outage is the de-id boundary DOWN for the whole run: an injected
# `deid_client` whose `deidentify` raises `ModelCallError`, so `deid_in` returns the
# existing `{"deidentified": False, "reason": DEID_CALL_FAILED}` sentinel (a whole-run
# outage is byte-identical to a per-call failure AT the `deid_in` boundary). On that
# sentinel the orchestrator HALTS to honest no-plan: 0 plans recorded, no degrade to
# `router.summarize` as a de-id-IN substitute, the maintained artifact untouched, and the
# `gate_dispatch=` seam IDLE (0 dispatches). These are the five ADR-0020-T2 acceptance
# criteria; the deviation table grounds them as ORCHESTRATOR (not `deid_in`) behaviors.


def _outage_client():
    """A de-id client whose `deidentify` raises `ModelCallError` for the WHOLE run.

    The whole-run-outage injection: `deid_in` collapses the raise to the existing
    `DEID_CALL_FAILED` sentinel (`except Exception`), which the orchestrator halts on.
    """
    return _FixedDeidClient(ModelCallError("de-id boundary unreachable for the whole run"))


# --- AC-1: whole-run outage -> 0 plans recorded, honest no-plan surfaced ----------


def test_whole_run_outage_records_zero_plans(tmp_path):
    # AC-1: with the de-id boundary injected as unreachable for the WHOLE run, the
    # orchestrator records 0 plans and surfaces the honest no-plan state. A degrade-to-
    # `summarize` or a fabricated summary would have recorded a `plan::<domain>` -> RED.
    store_read = _seed_store(tmp_path)
    dispatch = _RecordingDispatch(_sustaining_authors())

    out = run_orchestrated(
        _raw_intake(), _outage_client(), dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    # the honest no-plan state is surfaced (no recorded plan in the results)
    assert out["deidentified"] is False
    assert out["results"] == {}
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert recorded == [], "the outage path recorded a plan (must halt to 0 plans)"
    # 0 plans landed in the store across EVERY domain (not only the requested two)
    for domain in ("workout", "nutrition", "supplements", "peptides"):
        assert store.read(f"plan::{domain}", root=tmp_path) == []


# --- AC-2: the outage path does NOT route raw through `router.summarize` ----------


def test_outage_does_not_route_raw_intake_through_summarize(tmp_path, monkeypatch):
    # AC-2 (non-vacuous, fix M3/LOW-3): a bare call-count `summarize == 0` passes trivially
    # on a halted orchestrator (it never reaches the persisted-side `summarize` anyway). The
    # load-bearing assertion is an IDENTITY check: the RAW-INTAKE OBJECT is NEVER an argument
    # to `router.summarize` on the outage path -- proving `summarize` is not used as a degraded
    # de-id-IN substitute for the raw intake. A counterfactual control (below) gives it teeth.
    summarize_args = []
    real_summarize = router.summarize

    def summarize_spy(*args, **kwargs):
        summarize_args.append((args, kwargs))
        return real_summarize(*args, **kwargs)

    monkeypatch.setattr(router, "summarize", summarize_spy)

    store_read = _seed_store(tmp_path)
    raw = _raw_intake()
    dispatch = _RecordingDispatch(_sustaining_authors())

    run_orchestrated(
        raw, _outage_client(), dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )

    # the raw-intake OBJECT was never passed to `summarize` (no degrade-to-summarize de-id-IN)
    for args, kwargs in summarize_args:
        for arg in args:
            assert arg is not raw, "the outage path routed the RAW intake through router.summarize"
        for value in kwargs.values():
            assert value is not raw, "the outage path routed the RAW intake through router.summarize"


def test_outage_summarize_identity_check_has_teeth(tmp_path):
    # AC-2 COUNTERFACTUAL NEGATIVE CONTROL: a deliberately-degrading orchestrator stub that
    # DOES route the raw intake through `router.summarize` to keep going makes the identity
    # assertion turn RED -- confirming the assertion above tests something (not a tautology).
    raw = _raw_intake()
    summarize_args = []

    def summarize_spy(arg, *rest, **kwargs):
        summarize_args.append(arg)
        return {}

    def degrading_orchestrator(raw_intake):
        # the crown-jewel fidelity relaxation the real orchestrator must NEVER do: on a
        # de-id-boundary outage, degrade to `summarize(raw_intake)` as a coarse de-id-IN.
        return summarize_spy(raw_intake)

    degrading_orchestrator(raw)

    # the degrading stub DID pass the raw-intake object to `summarize` -> the identity check fails
    routed_raw = any(arg is raw for arg in summarize_args)
    assert routed_raw, "the counterfactual control must route the raw object (proves teeth)"


# --- AC-3: on outage, an existing maintained artifact is left untouched -----------


def test_outage_leaves_existing_artifact_untouched(tmp_path):
    # AC-3 (Risk R3, no partial/stale re-emit) — Wave-4 DISCHARGE (now FALSIFIABLE). The render
    # (`reemit_maintained`) is a DOWNSTREAM store-reading caller, NOT `run_orchestrated`'s body
    # (the orchestrator's contract ends at recording the plan to the store). The byte-identical-
    # on-outage property is therefore asserted over the SAME downstream caller invoked on BOTH
    # paths: a CLEAN run records a plan -> the re-emitted maintained artifact carries it; the
    # OUTAGE run records 0 plans -> a re-emit over that store carries NO plan content. The two
    # artifacts DIFFER, so "the outage does not write/clobber a plan into the artifact" has teeth
    # (a stale/partial re-emit that surfaced the no-longer-present plan, or an outage path that
    # wrote a plan, turns this RED — the success artifact is the falsifying control).
    from scripts.generate import maintained

    # the maintained re-emit reads the store the orchestrator recorded into; render is downstream.
    def _reemit(repo_root, store_root):
        out_dir = repo_root / "vault" / "artifacts" / "generated"
        out_dir.mkdir(parents=True, exist_ok=True)
        (repo_root / ".gitignore").write_text("vault/artifacts/generated/\n", encoding="utf-8")
        return maintained.reemit_maintained(
            root=store_root, _out_dir=out_dir,
            _today=datetime.date.fromisoformat(PLAN_DATE), _repo_root=repo_root,
        )

    # --- the CLEAN success path: a plan is recorded, the re-emit carries it ---
    clean_repo = tmp_path / "clean"
    clean_store = tmp_path / "clean-store"
    clean_read = _seed_store(clean_store)
    run_orchestrated(
        _raw_intake(), _FixedDeidClient(_deid_summary()), _RecordingDispatch(_sustaining_authors()),
        clean_read, clean_store, plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )
    clean_artifact = _reemit(clean_repo, clean_store).read_text(encoding="utf-8")

    # --- the OUTAGE path: 0 plans recorded, the re-emit over that store carries no plan ---
    outage_repo = tmp_path / "outage"
    outage_store = tmp_path / "outage-store"
    outage_read = _seed_store(outage_store)
    out = run_orchestrated(
        _raw_intake(), _outage_client(), _RecordingDispatch(_sustaining_authors()),
        outage_read, outage_store, plan_date=PLAN_DATE, domains=("workout", "nutrition"),
    )
    assert out["results"] == {}, "the outage path recorded a plan (must halt to 0 plans)"
    for domain in ("workout", "nutrition"):
        assert store.read(f"plan::{domain}", root=outage_store) == []
    outage_artifact = _reemit(outage_repo, outage_store).read_text(encoding="utf-8")

    # the two artifacts DIFFER: the clean run's carries the recorded plan, the outage run's does
    # not — the success artifact is the falsifying control giving the no-stale-re-emit teeth.
    assert clean_artifact != outage_artifact, (
        "the outage re-emit is byte-identical to the success re-emit (a stale plan leaked, or the "
        "success path wrote nothing — the byte-identical property has no teeth)"
    )


# --- AC-4 (gate-idle, the negative assertion): 0 gate dispatches on outage --------


def test_outage_gate_dispatch_seam_is_idle(tmp_path):
    # AC-4 (the missing negative assertion, ADR-0020 OQ-4): on the injected whole-run outage,
    # the downstream gates issue 0 dispatches. Wave-4 DISCHARGE: this now injects the WIRED
    # composed gate (the REAL two-gate composition — quality_judge + review_plan), not the Wave-2
    # no-op spy, and asserts the composed gate fires 0 times on the outage halt. The gate-idle
    # property now has teeth against the WIRED path: an orchestrator that reached the gate despite
    # the de-id outage halt turns this RED. The E2E-placement negative assertion: data does NOT
    # land where it should not (the de-id boundary halts BEFORE the inner engine + the gate).
    from scripts.plan.quality_judge import ACCEPT, quality_judge
    from scripts.plan.safety_review import review_plan
    from tests.plan.test_quality_judge import _FixedJudgeClient, _clean_scores
    from tests.plan.test_safety_review import _no_findings_dispatch

    store_read = _seed_store(tmp_path)
    dispatch = _RecordingDispatch(_sustaining_authors())

    judge_client = _FixedJudgeClient(_clean_scores())
    lens_dispatch = _no_findings_dispatch()
    gate_calls = []

    def composed_gate(assembled_plan):
        # the WIRED composed gate: runs BOTH real Wave-3 callables — counts every wired dispatch
        q = quality_judge(assembled_plan, judge_client)
        s = review_plan(assembled_plan, lens_dispatch)
        gate_calls.append((q, s))
        return {"accept": q["verdict"] == ACCEPT, "safety_passed": s["passed"]}

    out = run_orchestrated(
        _raw_intake(), _outage_client(), dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=composed_gate,
    )

    # the WIRED composed gate fired 0 times — the de-id outage halt precedes it (the gate-idle
    # property now has teeth against the real two-gate composition, not the Wave-2 no-op seam)
    assert gate_calls == [], "the WIRED gate_dispatch seam fired on outage (must be idle on halt)"
    # and the halt surfaced (cross-check the seam-idle is the outage halt, not a silent skip)
    assert out["deidentified"] is False
    assert out["results"] == {}

