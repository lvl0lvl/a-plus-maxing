"""Tests for the shared control-inversion driver (ADR-0026-T1, the keystone).

`scripts.plan.plan_driver.drive` is the ONE shared revise-loop control flow extracted from
`run_orchestrated`: a generator-coroutine that OWNS the scratch-store lifecycle, the `while True:`
gate->branch->re-dispatch sequencing, the `safety_passed is True` surface gate, the bounded-revise
cap, the preserved halts (de-id sentinel / dispatch-cap / out-of-run-set / revise-exhausted), and
the scratch-and-promote logic. It is driven by a CONSUMER (a fixture `dispatch` in tests, a real
subscription agent in the skill) that captures each yielded dispatch-request's author envelopes and
`.send()`s them back. These pin:

  - AC-10: the driver runs end-to-end under a fixture `dispatch` + a fixture `gate_dispatch` with NO
    live client and NO skill present (independently drivable);
  - AC-2: the no-fork probe — EXACTLY 1 executable copy of the loop control flow (in `plan_driver.py`),
    0 duplicated copies in `plan_orchestrator.py` / `SKILL.md`;
  - AC-4: an injected-safety-not-True disposition (`False`/`None`/absent/non-dict/raised) surfaces
    0 plans (terminal `SAFETY_BLOCKED`);
  - AC-5: a clean accept-fixture promotes >=1 `plan::<domain>` into `root` + carries `dispatch_count`;
  - AC-6: a non-converging revise halts at `revise_cap` (`REVISE_EXHAUSTED`, exactly `revise_cap`
    re-dispatches);
  - AC-7: the de-id sentinel halt (`DEID_HALTED`, 0 dispatches, 0 plans) preserved;
  - AC-8: an out-of-run-set revise target fails closed (`SAFETY_BLOCKED`, no `KeyError`);
  - AC-9: the dispatch-cap halt (`DISPATCH_CAP_EXCEEDED`, 0 plans past the cap) preserved;
  - QA-2: the post-extraction promoted store lines are byte-identical to the COMMITTED pre-extraction
    golden fixture (`tests/plan/fixtures/promote_golden_lines.txt`).

Every client/dispatch is a mock/fixture; no test hits a live API, and the test tree carries 0 real
operator PII (synthetic tokens only).
"""

import json
import subprocess
from pathlib import Path

from scripts.plan import plan_driver
from scripts.plan.dispatch_budget import DISPATCH_CAP_EXCEEDED
from scripts.plan.plan_orchestrator import (
    DEID_HALTED,
    REVISE_EXHAUSTED,
    SAFETY_BLOCKED,
    run_orchestrated,
)
from scripts.store import store

# --- the suite re-imports the sibling fixtures (the recipe's fixture import block) ---
from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
from tests.plan.test_generate_plan import PLAN_DATE, _seed_store
from tests.plan.test_plan_orchestrator import (
    _RecordingDispatch,
    _deid_summary,
    _sustaining_authors,
)
from tests.plan.test_revise_loop import (
    _clean_composing_gate,
    _composing_gate,
    _counting_dispatch,
    _empty_workout_envelope,
    _filled_workout_envelope,
    _recording_quality,
    _recording_safety,
)
from tests.plan.test_quality_judge import _clean_scores
from tests.plan.test_safety_review import _no_findings_dispatch


_GOLDEN = Path("tests/plan/fixtures/promote_golden_lines.txt")


# ===============================================================================
# Cycle 1: AC-10 (driver independently drivable) + AC-2 (no-fork probe)
# ===============================================================================


def test_driver_drivable_no_client_no_skill(tmp_path):
    # AC-10: `plan_driver.drive` runs end-to-end under a fixture `dispatch` + a fixture
    # `gate_dispatch` with NO `ModelClient` constructed and NO skill referenced. The driver yields
    # dispatch-requests; this consumer captures each request's authors (via the fixture dispatch
    # seam) and `.send()`s them back, exactly as `run_orchestrated` does. A driver with a hidden
    # dependency on the orchestrator's live wiring or the skill would not complete here.
    store_read = _seed_store(tmp_path)
    summary = _deid_summary()
    authors_map = _sustaining_authors()
    domains = ("workout", "nutrition")

    # the CONSUMER half (what run_orchestrated does): the driver yields dispatch-requests; this
    # consumer captures each request's authors via the fixture authors_map and `.send()`s back.
    gen = plan_driver.drive(
        summary, domains, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
    )
    result = _run_driver(gen, authors_map=authors_map)

    # a plan surfaced + promoted >=1 plan::<domain> into root, and dispatch_count is present
    recorded = [d for d, r in result["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1
    assert "dispatch_count" in result
    assert store.read("plan::workout", root=tmp_path) != []


def test_no_forked_revise_loop():
    # AC-2 (no-fork probe, QA-2): the EXECUTABLE loop control flow exists in EXACTLY 1 place
    # (plan_driver.py), 0 duplicated copies in plan_orchestrator.py / SKILL.md. The probe targets
    # EXECUTABLE control flow (the `while True:` header AND the `disposition.get("safety_passed")
    # is True` expression at a non-comment line), NOT the bare `safety_passed is True` token, which
    # legitimately survives in `plan_orchestrator.py` comments/docstrings (:211/:378). A grep for
    # the bare token would FALSE-POSITIVE-RED on those residual docstrings.
    files = {
        "driver": Path("scripts/plan/plan_driver.py"),
        "orchestrator": Path("scripts/plan/plan_orchestrator.py"),
        "skill": Path(".claude/skills/generate-plan/SKILL.md"),
    }

    def executable_loop_copies(path):
        if not path.exists():
            return 0
        while_headers = 0
        safety_exprs = 0
        for raw in path.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if stripped.startswith("#"):
                continue  # a comment line is never executable control flow
            if stripped == "while True:":
                while_headers += 1
            if 'disposition.get("safety_passed")' in raw and " is True" in raw:
                safety_exprs += 1
        # an executable loop copy needs BOTH the header and the keyed safety expression
        return min(while_headers, safety_exprs)

    driver_copies = executable_loop_copies(files["driver"])
    orch_copies = executable_loop_copies(files["orchestrator"])
    skill_copies = executable_loop_copies(files["skill"])

    assert driver_copies == 1, f"the loop must live in plan_driver.py exactly once: {driver_copies}"
    assert orch_copies == 0, f"a forked loop copy survives in plan_orchestrator.py: {orch_copies}"
    assert skill_copies == 0, f"a forked loop copy survives in SKILL.md: {skill_copies}"


# ===============================================================================
# Cycle 2: AC-4 (injected-safety-not-True -> 0 plans) + AC-5 (promotion-on-accept)
# ===============================================================================


def test_injected_safety_not_true_zero_plans(tmp_path):
    # AC-4: a disposition whose `safety_passed` is not boolean-True surfaces 0 plans across ALL
    # five non-True shapes (False / None / absent key / non-dict result / a raised gate) — terminal
    # SAFETY_BLOCKED. Driven through `run_orchestrated` (the consumer of the shared driver), so the
    # extracted driver's surface gate is the system under test.
    deid_client = _FixedDeidClient(_deid_summary())

    def _raising_gate(assembled_plan):
        raise RuntimeError("safety lens dispatch failed mid-review")

    not_true_gates = (
        lambda p: {"accept": True, "safety_passed": False},   # explicit False
        lambda p: {"accept": True, "safety_passed": None},    # None
        lambda p: {"accept": True},                            # absent key
        lambda p: ["not", "a", "dict"],                        # non-dict result
        _raising_gate,                                         # the gate raised
    )

    for i, gate in enumerate(not_true_gates):
        root = tmp_path / f"case-{i}"
        case_read = _seed_store(root)
        dispatch = _RecordingDispatch(_sustaining_authors())
        out = run_orchestrated(
            _raw_intake(), deid_client, dispatch, case_read, root,
            plan_date=PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
        )
        assert out["reason"] == SAFETY_BLOCKED, f"non-True safety surfaced (not SAFETY_BLOCKED): {gate}"
        assert out["results"] == {}, "an injected-safety-not-True run surfaced a plan"
        for domain in ("workout", "nutrition"):
            assert store.read(f"plan::{domain}", root=root) == []


def test_promotion_on_accept(tmp_path):
    # AC-5: a clean accept-fixture (`{accept: True, safety_passed: True}`) promotes >=1
    # plan::<domain> into root and the result carries dispatch_count.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
        gate_dispatch=_clean_composing_gate(),
    )

    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1
    assert "dispatch_count" in out
    assert store.read("plan::workout", root=tmp_path) != []
    assert store.read("plan::nutrition", root=tmp_path) != []


# ===============================================================================
# Cycle 3: the preserved halts (bounded-revise + de-id-sentinel + out-of-run-set + dispatch-cap)
# ===============================================================================


def test_bounded_revise_halts_at_cap(tmp_path):
    # AC-6: a non-converging quality miss (empty workout every pass) halts at revise_cap and returns
    # REVISE_EXHAUSTED; EXACTLY revise_cap re-dispatches (not revise_cap + 1), 0 plans past.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _counting_dispatch(lambda domain, n: _empty_workout_envelope())
    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate, revise_cap=3,
    )

    assert out["reason"] == REVISE_EXHAUSTED
    assert out["results"] == {}
    assert store.read("plan::workout", root=tmp_path) == []
    workout_calls = [c for c in dispatch.calls if c["domain"] == "workout"]
    # initial dispatch + EXACTLY revise_cap (3) re-dispatches, not 4
    assert len(workout_calls) == 1 + 3, f"re-dispatch count != 3: {len(workout_calls) - 1}"


def test_deid_sentinel_halt(tmp_path):
    # AC-7: a `{deidentified: False}` sentinel -> the driver/orchestrator halts to honest no-plan
    # with 0 dispatches + 0 plans (DEID_HALTED).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient({"deidentified": False, "reason": "deid-call-failed"})
    dispatch = _RecordingDispatch(_sustaining_authors())

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
        gate_dispatch=_clean_composing_gate(),
    )

    assert out["deidentified"] is False
    assert out["reason"] == DEID_HALTED
    assert out["dispatch_count"] == 0
    assert dispatch.calls == [], "a specialist dispatched past the de-id halt"
    for domain in ("workout", "nutrition"):
        assert store.read(f"plan::{domain}", root=tmp_path) == []


def test_out_of_run_set_revise_blocked(tmp_path):
    # AC-8: a revise_domains entry NOT in the run's domains -> terminal SAFETY_BLOCKED, 0 plans, no
    # unguarded KeyError on `_ROLE_OF_DOMAIN[domain]`.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    # the out-of-run-set disposition can only arise at the compose seam (the real
    # `compose_disposition` never escapes the run-set) — inject a mutant `compose` (ADR-0028-T1).
    def out_of_set_producer(assembled_plan):
        return {"judge": {"verdict": "REVISE", "dimensions": {}, "deductions": []}, "review": {}}

    def out_of_set_compose(verdicts, assembled_plan):
        return {"accept": False, "safety_passed": True, "revise_domains": ("not-a-domain",)}

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",),
        gate_dispatch=out_of_set_producer, compose=out_of_set_compose,
    )

    assert out["reason"] == SAFETY_BLOCKED
    assert out["results"] == {}
    assert store.read("plan::workout", root=tmp_path) == []


def test_dispatch_cap_halt(tmp_path):
    # AC-9: with dispatch_cap below the run's tally, the driver halts to honest no-plan
    # (DISPATCH_CAP_EXCEEDED) before the over-budget dispatch — 0 plans past the cap. cap=2:
    # initial workout dispatch (1) + gate dispatch (2), then the revise re-dispatch charge (3 > 2)
    # trips before the over-budget dispatch.
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _counting_dispatch(lambda domain, n: _empty_workout_envelope())
    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=gate, dispatch_cap=2,
    )

    assert out["reason"] == DISPATCH_CAP_EXCEEDED
    assert out["results"] == {}
    assert store.read("plan::workout", root=tmp_path) == []


# ===============================================================================
# Cycle 4: driver-independently-drivable (no live client, no skill) — the suite gate
# ===============================================================================


def test_driver_has_no_module_scope_live_wiring():
    # AC-10 (the module-scope proof): plan_driver imports no live ModelClient and references no
    # skill at module scope — it is seam-driven (the inner engine + dispatch + gate_dispatch are
    # INPUTS). A driver that imported the live client or the skill at module scope would couple the
    # test/API mode to live wiring.
    src = Path("scripts/plan/plan_driver.py").read_text(encoding="utf-8")
    assert "ModelClient" not in src, "the driver imports a live ModelClient (must be seam-driven)"
    assert "SKILL.md" not in src and "generate-plan" not in src, "the driver references the skill"


def test_driver_suite_gate(tmp_path):
    # AC-11: the three-file suite passes with 0 live calls. A thin in-process re-assert that the
    # driver + the orchestrator + the revise-loop suites co-exist (the full assertion is the
    # command in the recipe; this pins the import graph is consistent in-process).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
        gate_dispatch=_clean_composing_gate(),
    )
    assert out.get("reason") is None


# ===============================================================================
# Cycle 5: the store-seam golden-line (QA-2: byte-identical promoted store lines)
# ===============================================================================


def _capture_promoted_lines(root, monkeypatch_store_append):
    """Drive the clean accept-fixture through `run_orchestrated` and capture promote-into-root lines.

    Returns the sorted `<item>\t<sorted-json-reading>` lines `store.append` received at the
    promote-into-REAL-root seam (the same stable serialization the golden was captured with).
    """
    captured = []
    real_append = store.append

    def recording_append(item, reading, append_root=None, **kwargs):
        # support both positional + keyword root (store.append(item, reading, root=root))
        r = kwargs.get("root", append_root if append_root is not None else store.DEFAULT_ROOT)
        # the relocated promote seam writes ONLY plan::/dvq:: rows into the real root — capture those
        # (the intake-seed writes other items into the same root; they are not the promote seam).
        if str(r) == str(root) and (item.startswith("plan::") or item.startswith("dvq::")):
            captured.append((item, json.dumps(reading, sort_keys=True, default=str)))
        return real_append(item, reading, root=r)

    # seed the operator-state store BEFORE patching (matches the golden-capture sequencing — only
    # the promote-into-root writes are captured, never the intake seed).
    store_read = _seed_store(root)
    monkeypatch_store_append(recording_append)
    out = run_orchestrated(
        _raw_intake(), _FixedDeidClient(_deid_summary()),
        _RecordingDispatch(_sustaining_authors()), store_read, root,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
        gate_dispatch=_clean_composing_gate(),
    )
    assert out.get("reason") is None, f"capture run did not surface a plan: {out.get('reason')}"
    return sorted(f"{item}\t{reading}" for item, reading in captured)


def test_store_seam_golden_line(tmp_path, monkeypatch):
    # QA-2: the post-extraction promoted store lines are byte-identical to the COMMITTED
    # pre-extraction golden fixture (captured at the entry-state HEAD BEFORE GREEN — a static
    # oracle, NOT a runtime re-capture). A silent keying drift at the relocated _promote_plans ->
    # store.append seam (same surface, different bytes) goes RED here.
    golden = [ln for ln in _GOLDEN.read_text(encoding="utf-8").splitlines() if ln]
    assert golden, "the committed golden fixture is empty (capture not wired)"

    live = _capture_promoted_lines(tmp_path, lambda fn: monkeypatch.setattr(store, "append", fn))

    assert live == golden, (
        "the post-extraction promoted store lines drifted from the pre-extraction golden "
        f"(keying drift at the relocated promote seam):\n  golden={golden}\n  live={live}"
    )


def test_store_seam_golden_line_has_teeth(tmp_path, monkeypatch):
    # QA-3 RED-against-a-keying-drift-variant: a promote that mutates the (item, timepoint, source)
    # keying at the relocated seam produces lines that DIFFER from the golden — proving the
    # golden-line diff can catch a keying drift (a golden that cannot go RED is worthless).
    golden = [ln for ln in _GOLDEN.read_text(encoding="utf-8").splitlines() if ln]
    captured = []
    real_append = store.append

    def keying_drift_append(item, reading, **kwargs):
        r = kwargs.get("root", store.DEFAULT_ROOT)
        if str(r) == str(tmp_path):
            # the keying-drift variant: mutate the source tag (a real keying drift)
            drifted = {**reading, "source": reading.get("source", "") + "-DRIFTED"}
            captured.append((item, json.dumps(drifted, sort_keys=True, default=str)))
            return real_append(item, drifted, root=r)
        return real_append(item, reading, root=r)

    monkeypatch.setattr(store, "append", keying_drift_append)
    store_read = _seed_store(tmp_path)
    run_orchestrated(
        _raw_intake(), _FixedDeidClient(_deid_summary()),
        _RecordingDispatch(_sustaining_authors()), store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout", "nutrition"),
        gate_dispatch=_clean_composing_gate(),
    )
    drifted_lines = sorted(f"{item}\t{reading}" for item, reading in captured)

    # the drifted keying DIFFERS from the golden — the golden-line diff has teeth
    assert drifted_lines != golden, "the golden-line diff cannot catch a keying drift (no teeth)"


# ===============================================================================
# ADR-0028-T1: the typed discriminated-union request protocol + AUTHOR/GATE inversion
# ===============================================================================


def test_every_yield_tagged_kind(tmp_path):
    # AC-2: every yielded request is a typed discriminated-union request whose `kind` is one of
    # the four reserved tokens — a bare tuple is NEVER yielded (the count of untagged yields == 0).
    store_read = _seed_store(tmp_path)
    summary = _deid_summary()
    authors_map = _sustaining_authors()
    domains = ("workout", "nutrition")

    gen = plan_driver.drive(
        summary, domains, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
    )
    requests = _record_requests(gen, authors_map=authors_map)

    assert requests, "the driver yielded nothing"
    untagged = [r for r in requests if not hasattr(r, "kind")]
    assert untagged == [], f"a bare/untagged request was yielded: {untagged}"
    for r in requests:
        assert r.kind in plan_driver.REQUEST_KINDS, f"untagged or unknown kind: {r.kind!r}"


def test_author_then_gate_ordering(tmp_path):
    # AC-3: a 4-domain accept fixture run records the yielded `kind` sequence == ["AUTHOR", "GATE"]
    # then promote-on-accept (>=1 plan:: row). (Cycle 1 finalizes the GATE leg once Cycle 2 inverts
    # the gate; pre-Cycle-2 this asserts the sequence STARTS with AUTHOR.)
    store_read = _seed_store(tmp_path)
    summary = _deid_summary()
    authors_map = _sustaining_authors()
    domains = ("workout", "nutrition")

    gen = plan_driver.drive(
        summary, domains, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
    )
    requests = _record_requests(gen, authors_map=authors_map)
    kinds = [r.kind for r in requests]

    assert kinds == [plan_driver.AUTHOR, plan_driver.GATE], f"yield-kind sequence: {kinds}"
    assert store.read("plan::workout", root=tmp_path) != []


def test_author_payload_carries_domains_summary_gates(tmp_path):
    # AC-2 (AUTHOR payload shape): the AUTHOR request's payload carries (domains, summary, gates) —
    # the same triple the bare tuple carried — so the consumer drives `_dispatch_domains` over it.
    store_read = _seed_store(tmp_path)
    summary = _deid_summary()
    authors_map = _sustaining_authors()
    domains = ("workout", "nutrition")

    gen = plan_driver.drive(
        summary, domains, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
    )
    first = next(gen)
    assert first.kind == plan_driver.AUTHOR
    req_domains, req_summary, req_gates = first.payload
    assert tuple(req_domains) == domains
    assert req_summary == summary
    assert req_gates == {}
    gen.close()


def test_gate_payload_raw_inputs_one_composition_site(tmp_path):
    # AC-4 (GATE carries RAW INPUTS, driver composes — no-fork, ADR-0028-T1 OQ-2): the GATE request
    # payload carries the assembled plan + a RAW-VERDICT PRODUCER (NOT a composed disposition
    # callable, the OQ-2-rejected shape). The PRODUCER, when invoked, returns RAW `{judge, review}`
    # verdicts — NOT a finished `{accept, safety_passed, revise_domains}` disposition (this is the
    # load-bearing assertion: it goes RED against the old composed-callable wire, where invoking the
    # payload's callable returned a disposition). The consumer `.send()`s those RAW verdicts; `drive`
    # composes them via `compose_disposition`. PLUS the no-fork grep: EXACTLY 1 composition site +
    # EXACTLY 1 surface gate — 0 duplicates in the consumer / SKILL.md.
    store_read = _seed_store(tmp_path)
    summary = _deid_summary()
    authors_map = _sustaining_authors()
    domains = ("workout", "nutrition")
    producer = _clean_composing_gate()

    gen = plan_driver.drive(
        summary, domains, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={}, gate_producer=producer,
    )
    # drive the AUTHOR request, then capture the GATE request and inspect its payload directly
    author_req = next(gen)
    assert author_req.kind == plan_driver.AUTHOR
    a_domains, _, _ = author_req.payload
    gate_req = gen.send({d: authors_map[d] for d in a_domains})

    assert gate_req.kind == plan_driver.GATE, f"the 2nd yield is not a GATE request: {gate_req.kind}"
    assembled_plan, producer_in_payload = gate_req.payload
    # the payload carries the assembled plan (RAW INPUT) — a dict with `results`, NOT a disposition
    assert isinstance(assembled_plan, dict) and "results" in assembled_plan
    # the payload carries NO finished disposition: no accept/safety_passed/revise_domains keys
    assert not any(k in assembled_plan for k in ("accept", "safety_passed", "revise_domains"))
    # the payload carries the PRODUCER (the same object the consumer holds — the dispatch unit)
    assert producer_in_payload is producer
    # LOAD-BEARING (non-tautological, RED against the old composed-callable wire): the producer
    # returns RAW VERDICTS — a dict keyed `judge`/`review`, NOT a composed disposition. The old wire
    # yielded a callable that returned `{accept, safety_passed, revise_domains}`; this asserts the
    # WIRE now carries raw inputs the skill can fulfil by dispatching agents.
    raw = producer_in_payload(assembled_plan)
    assert set(raw.keys()) == {"judge", "review"}, f"the producer did not return raw verdicts: {raw!r}"
    assert not any(k in raw for k in ("accept", "safety_passed", "revise_domains")), (
        "the GATE payload's producer returned a COMPOSED disposition (the OQ-2-rejected wire shape)"
    )
    gen.close()

    # the no-fork grep oracle: EXACTLY 1 composition site + EXACTLY 1 surface gate (executable)
    assert _composition_sites() == 1, "more than one compose_gate_dispatch composition site"
    assert _executable_surface_gates() == 1, "more than one executable safety_passed surface gate"


def test_revise_pass_second_author_then_gate(tmp_path):
    # AC-5: a revise-then-accept disposition → the recorded yielded `kind` sequence ==
    # ["AUTHOR", "GATE", "AUTHOR", "GATE"] and >=1 plan promotes.
    store_read = _seed_store(tmp_path)
    summary = _deid_summary()

    # pass-0 workout empty (REVISE), re-dispatch returns FILLED (ACCEPT on pass-1).
    call_n = {"workout": 0}

    def authors_for(domains):
        out = {}
        for d in domains:
            if d == "workout":
                call_n["workout"] += 1
                out[d] = (_filled_workout_envelope() if call_n["workout"] >= 2
                          else _empty_workout_envelope())
            else:
                out[d] = _sustaining_authors()[d]
        return out

    gate = _composing_gate(
        _recording_quality(_clean_scores()),
        _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )

    gen = plan_driver.drive(
        summary, ("workout",), store_read, tmp_path,
        plan_date=PLAN_DATE, gates={}, gate_producer=gate,
    )
    kinds = []
    request = next(gen)
    try:
        while True:
            kinds.append(request.kind)
            if request.kind == plan_driver.AUTHOR:
                req_domains, _, _ = request.payload
                fulfilment = authors_for(req_domains)
            else:
                assembled_plan, gate_cb = request.payload
                fulfilment = gate_cb(assembled_plan)
            request = gen.send(fulfilment)
    except StopIteration:
        pass

    assert kinds == [plan_driver.AUTHOR, plan_driver.GATE, plan_driver.AUTHOR, plan_driver.GATE], kinds
    assert store.read("plan::workout", root=tmp_path) != []


def test_malformed_gate_send_back_safety_blocked(tmp_path):
    # AC-6 (GATE fail-closed shape): a malformed GATE disposition sent back across the shapes (a
    # non-dict / a missing key / a raised gate) → `drive` returns terminal SAFETY_BLOCKED, 0 plans.
    summary = _deid_summary()
    authors_map = _sustaining_authors()
    domains = ("workout", "nutrition")

    def _raising_gate(assembled_plan):
        raise RuntimeError("safety lens dispatch failed mid-review")

    malformed_gates = (
        lambda p: {"accept": True, "safety_passed": False},   # explicit False
        lambda p: {"accept": True, "safety_passed": None},    # None
        lambda p: {"accept": True},                            # absent key
        lambda p: ["not", "a", "dict"],                        # non-dict result
        _raising_gate,                                         # the gate raised
    )

    for i, gate in enumerate(malformed_gates):
        root = tmp_path / f"case-{i}"
        store_read = _seed_store(root)
        gen = plan_driver.drive(
            summary, domains, store_read, root,
            plan_date=PLAN_DATE, gates={}, gate_producer=gate,
        )
        out = _run_driver(gen, authors_map=authors_map)
        assert out["reason"] == SAFETY_BLOCKED, f"malformed GATE not SAFETY_BLOCKED: {gate}"
        assert out["results"] == {}
        for domain in domains:
            assert store.read(f"plan::{domain}", root=root) == []


def test_unknown_kind_fails_closed(tmp_path, monkeypatch):
    # AC-8 (unknown-kind fails closed — Negative-1 mitigation): a synthetic request whose `kind` is
    # NOT in REQUEST_KINDS reaches the consumer's fulfilment switch → the consumer does NOT
    # default-allow; it routes to a fail-closed halt with 0 plans surfaced. Driven by monkeypatching
    # `plan_driver.drive` to yield ONE unrecognized-kind request, then asserting `run_orchestrated`
    # surfaces 0 plans (no default-allow, no escaping dispatch).
    store_read = _seed_store(tmp_path)
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())

    def _unknown_kind_driver(*args, **kwargs):
        # a synthetic driver yielding a single request with a kind outside REQUEST_KINDS
        sent = yield plan_driver.Request("UNRECOGNIZED", (("workout",), _deid_summary(), {}))
        # if the consumer default-allowed and sent back, this would surface a plan — it must not
        yield plan_driver.Request(plan_driver.AUTHOR, (("workout",), _deid_summary(), {}))

    monkeypatch.setattr(plan_driver, "drive", _unknown_kind_driver)

    out = run_orchestrated(
        _raw_intake(), deid_client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=("workout",), gate_dispatch=_clean_composing_gate(),
    )

    # the unknown kind fails closed: 0 plans surfaced, honest no-plan reason, no escaping dispatch
    assert out.get("results", {}) == {}, "an unknown request kind surfaced a plan (default-allow)"
    assert out.get("reason") is not None, "the unknown kind did not route to an honest no-plan halt"
    assert store.read("plan::workout", root=tmp_path) == []
    # the unknown kind was NOT default-dispatched (the consumer did not fulfil it as an AUTHOR)
    assert dispatch.calls == [], "the consumer dispatched an unrecognized-kind request"


# --- no-fork grep oracles (AC-4) ------------------------------------------------

# The files the no-fork probe scans for a SECOND composition site / surface gate (the latent
# forked-safety-loop failure vector). `plan_step.py` is ABSENT this wave (T3 creates it).
_NO_FORK_FILES = (
    Path("scripts/plan/plan_orchestrator.py"),
    Path("scripts/plan/plan_step.py"),
    Path(".claude/skills/generate-plan/SKILL.md"),
)


def _composition_sites():
    """Count the executable 3-key-disposition composition sites OUTSIDE the ONE in `gate_dispatch`.

    A composition site builds the `{accept, safety_passed, revise_domains}` disposition (ADR-0028-T1:
    that mapping now lives in `compose_disposition`, called by `drive` — the ONE composition site; the
    producer `compose_gate_dispatch` returns RAW verdicts and builds NO disposition). The canonical
    site is `compose_disposition` in `gate_dispatch.py`; a SECOND in the consumer / the skill is the
    fork. The count returned here is the canonical site + any EXTRA (forked) site in the scanned
    files. A well-formed tree returns 1 (the single `compose_disposition` definition).
    """
    sites = 0
    # the canonical composition site (the disposition mapping)
    composer = Path("scripts/plan/gate_dispatch.py").read_text(encoding="utf-8")
    sites += composer.count("def compose_disposition")
    # any FORKED composer in the scanned files (an executable def, not a comment/doc reference)
    for path in _NO_FORK_FILES:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if stripped.startswith("#"):
                continue
            if "def compose_disposition" in raw:
                sites += 1
    return sites


def _executable_surface_gates():
    """Count the executable `safety_passed is True` surface gates OUTSIDE the ONE in `plan_driver`.

    The ONLY surface gate is the `disposition.get("safety_passed") is True` check in
    `plan_driver.drive`; a SECOND executable copy in the consumer / the skill is the fork. The probe
    targets EXECUTABLE control flow (the keyed `disposition.get("safety_passed") ... is True`
    expression at a non-comment line), NOT the bare `safety_passed is True` token (which survives
    legitimately in `plan_orchestrator.py` docstrings/comments). Returns 1 for a well-formed tree
    (the single surface gate in `plan_driver.py`).
    """
    gates = 0
    driver = Path("scripts/plan/plan_driver.py").read_text(encoding="utf-8")
    for raw in driver.splitlines():
        stripped = raw.strip()
        if stripped.startswith("#"):
            continue
        if 'disposition.get("safety_passed")' in raw and " is True" in raw:
            gates += 1
    for path in _NO_FORK_FILES:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if stripped.startswith("#"):
                continue
            if 'disposition.get("safety_passed")' in raw and " is True" in raw:
                gates += 1
    return gates


# --- driver helpers -------------------------------------------------------------


def _record_requests(gen, *, dispatch=None, authors_map=None):
    """Drive a `plan_driver.drive` generator to completion, recording every yielded typed request.

    The typed-request consumer half: prime the generator, and for each yielded request, switch on
    `request.kind` — fulfill an AUTHOR request from the fixture authors_map and a GATE request by
    invoking the gate over the assembled plan — and `.send()` the fulfilment back. Returns the list
    of yielded requests (not the final result), so a test can assert the yield-kind sequence.
    """
    authors_map = authors_map or _sustaining_authors()
    requests = []
    request = next(gen)
    try:
        while True:
            requests.append(request)
            request = _fulfil_and_advance(gen, request, authors_map)
    except StopIteration:
        return requests


def _run_driver(gen, *, dispatch=None, authors_map=None):
    """Advance a `plan_driver.drive` generator to completion, fulfilling each yielded typed request.

    The CONSUMER half of the typed-request drive-protocol (what `run_orchestrated` does): prime the
    generator, and for each yielded request switch on `request.kind` — fulfill an AUTHOR request
    from the fixture authors_map and a GATE request by invoking the gate over the assembled plan —
    and `.send()` the fulfilment back. A gate that RAISES is THROWN into the driver (mirroring the
    consumer), whose fail-closed wrap reads it as ambiguous. Returns the driver's final result.
    """
    authors_map = authors_map or _sustaining_authors()
    try:
        request = next(gen)
        while True:
            request = _fulfil_and_advance(gen, request, authors_map)
    except StopIteration as done:
        return done.value


def _fulfil_and_advance(gen, request, authors_map):
    """Fulfil one typed request and advance the driver — the shared consumer step for the helpers.

    Switches on `request.kind`: an AUTHOR request is fulfilled from the fixture authors_map; a GATE
    request is fulfilled by invoking the gate over the assembled plan, and a gate that RAISES is
    THROWN into the driver (so the driver's GATE-yield fail-closed wrap converts it to ambiguous ->
    SAFETY_BLOCKED, exactly as the production consumer does). Returns the next yielded request.
    """
    if request.kind == plan_driver.AUTHOR:
        domains, summary, gates = request.payload
        return gen.send({d: authors_map[d] for d in domains})
    if request.kind == plan_driver.GATE:
        assembled_plan, gate = request.payload
        try:
            disposition = gate(assembled_plan)
        except Exception as gate_error:
            return gen.throw(gate_error)
        return gen.send(disposition)
    raise AssertionError(f"unexpected request kind: {request.kind!r}")
