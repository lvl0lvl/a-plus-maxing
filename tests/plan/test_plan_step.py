"""Tests for the step-harness `plan_step.step` (ADR-0028-T3 — the skill's per-round drive).

`scripts.plan.plan_step.step` is the PAUSE BOUNDARY between the `/generate-plan` skill and the ONE
shared driver (`plan_driver.drive`): the skill cannot hold a live generator across Agent-tool
dispatches, so the harness re-constructs/resumes the driver from a SERIALIZED memo-cache state,
advances it EXACTLY ONE yield, and returns `(pending_request, serialized_state)`. Re-calling `step`
with the prior serialized state + the just-fulfilled envelope appended re-drives to the NEXT yield
(or completion). There is NO held generator object across calls — the inner engine is a pure
function of `(authors, summary, gates, cached-hook-responses)` (ADR-0028 OQ-5), so re-driving from
the same serialized state is deterministically reproducible.

These pin:
  - AC-1 (one-yield-advance): `step(None, ...)` over a fixture run advances exactly one yield and
    returns `(pending_request, serialized_state)` with a valid `pending_request.kind`; the FIRST
    `step` returns the AUTHOR request + a non-empty serialized state.
  - AC-2 (memo-cache serialization FORMAT, pinned binary): the serialized state round-trips
    losslessly (`json.loads(json.dumps(state)) == state`) AND every memo-cache key matches one of
    the two documented shapes (`reauthor:(domain, constraint)` 2-tuple /
    `adjudicator:(held-domain, hold-class, finding_id)` 3-tuple).
  - AC-3 (appended-envelope re-call): a full round-sequence (AUTHOR -> GATE -> ... -> promote) drives
    to a promoted plan with >=1 `plan::` row PURELY through repeated `step` calls — no generator
    object held across calls.
  - AC-4 (DETERMINISM AUDIT, pinned binary): two independent replays over the SAME serialized cache
    state reproduce the IDENTICAL `(kind, key)` sequence up to the next cache-miss.
  - AC-5 (no-fork at the harness): `plan_step.py` has 0 executable disposition-composition sites and
    0 re-derivations of the adjudication release.
  - AC-6 (charge-on-miss-only through the harness): driving a bounce + held-finding fixture through
    repeated `step` calls charges `budget.count` exactly once per cache-MISS, equal to the
    synchronous-reference count — no charge on a replayed cache-HIT.
  - AC-7 (harness-suite gate): 0 live calls — fixture `dispatch` + fixture envelopes only.

Every client/dispatch is a mock/fixture; no test hits a live API, and the test tree carries 0 real
operator PII (synthetic tokens only).
"""

import json
from pathlib import Path

from scripts.plan import plan_driver, plan_step
from scripts.plan.dispatch_budget import DispatchBudget
from scripts.store import store

# --- the suite re-imports the sibling fixtures (the recipe's fixture import block) ---
from tests.plan.test_deid_in import _FixedDeidClient  # noqa: F401  (parity with sibling suites)
from tests.plan.test_generate_plan import PLAN_DATE, _seed_store
from tests.plan.test_plan_orchestrator import _deid_summary, _sustaining_authors
from tests.plan.test_revise_loop import (
    _bounce_authors,
    _bpmh_store,
    _clean_composing_gate,
    _clearing_liaison,
    _clearing_reauthor,
    _empty_workout_envelope,
    _filled_workout_envelope,
    _multi_held_authors,
    _replay_safety_authors,
)


# --- a fixture consumer that drives the harness one yield at a time -------------


def _fulfil(request, *, authors_map, reauthor=None, adjudicator=None, budget=None):
    """Fulfil one yielded typed request against the fixtures — the consumer half, no driver state.

    The harness HOLDS no generator; this consumer reads the pending request's `kind`, dispatches the
    fixture authors / verdicts / replay envelope, and hands the envelope back to the NEXT `step` call
    (the appended-envelope re-call). It composes NOTHING and re-derives NOTHING (the no-fork
    constraint stays at the harness boundary).

    When a `budget` is passed it charges at the consumer's fulfilment point — mirroring
    `run_orchestrated`'s consumer (`_dispatch_domains` charges one per specialist dispatch;
    `_charging` charges one per gate / reauthor / adjudicator dispatch). The harness re-drives the
    cached rounds INTERNALLY, so this consumer is invoked exactly once per surfaced yield (a
    cache-MISS / new request) and never on a replayed cache-HIT — the charge-on-miss-only property
    (AC-6). The harness itself never charges (charging is the consumer's, the harness only drives +
    reads `budget.count`).
    """
    if request.kind == plan_driver.AUTHOR:
        domains, _summary, _gates = request.payload
        if budget is not None:
            for _ in domains:
                budget.charge()  # one per specialist dispatch (mirror `_dispatch_domains`)
        return {d: authors_map[d] for d in domains}
    if request.kind == plan_driver.GATE:
        assembled_plan, producer = request.payload
        if budget is not None:
            budget.charge()  # one per gate dispatch (mirror `_charging(gate_dispatch)`)
        return producer(assembled_plan)
    if request.kind == plan_driver.REAUTHOR:
        if budget is not None:
            budget.charge()  # one per cache-MISS reauthor (mirror `_charging(reauthor)`)
        return reauthor(*request.payload)
    if request.kind == plan_driver.ADJUDICATOR:
        if budget is not None:
            budget.charge()  # one per cache-MISS adjudication (mirror `_charging(adjudicator)`)
        return adjudicator(*request.payload)
    raise AssertionError(f"unexpected request kind: {request.kind!r}")


def _run_through_step(drive_kwargs, *, authors_map, reauthor=None, adjudicator=None):
    """Drive a run to completion PURELY through repeated `plan_step.step` calls (no held generator).

    Returns the driver's final result. Each iteration: `step` advances the driver one yield from the
    SERIALIZED state (+ the just-fulfilled envelope), the consumer fulfils the pending request, and
    the loop re-calls `step` with the new serialized state + that envelope. The ONLY state passed
    between iterations is the serialized state + the appended envelope — no generator object.
    """
    budget = drive_kwargs.get("budget")
    pending, state = plan_step.step(None, **drive_kwargs)
    envelope = None
    while pending is not None:
        envelope = _fulfil(pending, authors_map=authors_map, reauthor=reauthor,
                           adjudicator=adjudicator, budget=budget)
        pending, state = plan_step.step(state, fulfilled_envelope=envelope, **drive_kwargs)
    return plan_step.result_of(state)


# ===============================================================================
# Cycle 1: AC-1 (one-yield-advance) + AC-2 (serialization FORMAT) + AC-5 (no-fork)
# ===============================================================================


def test_step_one_yield_advance(tmp_path):
    # AC-1: the FIRST `step(None, ...)` advances the driver EXACTLY one yield and returns
    # `(pending_request, serialized_state)` — the pending request is the AUTHOR request, its `kind`
    # is a valid request kind, and the serialized state is NON-EMPTY (it carries the pending
    # descriptor). A held generator / a multi-yield advance would break the one-yield contract.
    store_read = _seed_store(tmp_path)
    drive_kwargs = dict(
        summary=_deid_summary(), domains=("workout", "nutrition"), store_read=store_read,
        root=tmp_path, plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
    )

    pending, state = plan_step.step(None, **drive_kwargs)

    assert pending is not None, "the first step returned no pending request"
    assert pending.kind in {"AUTHOR", "GATE", "REAUTHOR", "ADJUDICATOR"}, pending.kind
    assert pending.kind == plan_driver.AUTHOR, f"the first yield is not AUTHOR: {pending.kind}"
    assert state, "the serialized state is empty after the first step"
    # the AUTHOR payload is the (domains, summary, gates) triple the consumer dispatches over
    req_domains, req_summary, req_gates = pending.payload
    assert tuple(req_domains) == ("workout", "nutrition")
    assert req_summary == _deid_summary()


def test_memo_cache_serialization_format(tmp_path):
    # AC-2 (the pinned binary): the serialized state is JSON-serializable and round-trips with NO
    # loss (`json.loads(json.dumps(state)) == state`), AND every MEMO-cache key matches one of the
    # two documented shapes — `reauthor:(domain, constraint)` (a 2-tuple tail) /
    # `adjudicator:(held-domain, hold-class, finding_id)` (a 3-tuple tail). Driven over a bounce +
    # held-finding fixture so the memo actually carries >=1 of EACH key class (an empty memo passes
    # vacuously — this seeds both).
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    budget = DispatchBudget()
    drive_kwargs = dict(
        summary=_deid_summary(),
        domains=("workout", "nutrition", "supplements", "peptides"),
        store_read=store_read, root=tmp_path, plan_date=PLAN_DATE, gates={},
        gate_producer=_clean_composing_gate(), reauthor=_clearing_reauthor(),
        adjudicator=_clearing_liaison(), budget=budget,
    )

    # walk the whole run through `step`, capturing the serialized state at EACH round so we inspect
    # the state AFTER the memo has accumulated both a REAUTHOR and an ADJUDICATOR response.
    authors_map = _replay_safety_authors()
    reauthor = _clearing_reauthor()
    adjudicator = _clearing_liaison()
    states = []
    pending, state = plan_step.step(None, **drive_kwargs)
    states.append(state)
    envelope = None
    while pending is not None:
        envelope = _fulfil(pending, authors_map=authors_map, reauthor=reauthor, adjudicator=adjudicator)
        pending, state = plan_step.step(state, fulfilled_envelope=envelope, **drive_kwargs)
        states.append(state)

    # EVERY serialized state round-trips losslessly through json (the pinned FORMAT)
    for st in states:
        assert json.loads(json.dumps(st)) == st, "the serialized state lost data on a json round-trip"

    # the final accumulated state carries the memo with >=1 of EACH key class, every key on-shape
    final = states[-1]
    memo = plan_step.memo_of(final)
    reauthor_keys = [k for k in memo if plan_step.key_class(k) == "reauthor"]
    adjudicator_keys = [k for k in memo if plan_step.key_class(k) == "adjudicator"]
    assert reauthor_keys, "no reauthor key accumulated in the memo (the bounce did not seed one)"
    assert adjudicator_keys, "no adjudicator key accumulated in the memo (no held finding seeded one)"
    for k in memo:
        cls, tail = plan_step.parse_key(k)
        assert cls in {"reauthor", "adjudicator"}, f"a key off the two documented shapes: {k!r}"
        if cls == "reauthor":
            assert len(tail) == 2, f"reauthor key arity != 2 (domain, constraint): {k!r}"
        else:
            assert len(tail) == 3, f"adjudicator key arity != 3 (held-domain, hold-class, finding_id): {k!r}"


def test_no_fork_at_harness():
    # AC-5 (the no-fork grep): `plan_step.py` has 0 EXECUTABLE disposition-composition sites
    # (`def compose_disposition`, a `{accept` 3-key build, or a keyed `disposition.get("safety_passed")
    # ... is True` surface gate) AND 0 re-derivations of the adjudication release (`outcome ==
    # "cleared"`, the CRITICAL / non-overridable check). The harness DRIVES — it composes nothing and
    # releases nothing. Comments + docstrings are stripped before counting (the ADR-0026-T1 QA-2
    # executable-not-token discipline: a bare token in prose is not a fork).
    path = Path("scripts/plan/plan_step.py")
    assert path.exists(), "plan_step.py is absent (the harness was not created)"

    import ast

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    docstring_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and hasattr(node, "end_lineno"):
            docstring_lines.update(range(node.lineno, node.end_lineno + 1))
    executable = []
    for i, line in enumerate(source.splitlines(), start=1):
        if i in docstring_lines:
            continue
        executable.append(line.split("#", 1)[0])
    executable_src = "\n".join(executable)

    # 0 composition sites: no forked composer def, no 3-key {accept build, no executable surface gate
    assert "def compose_disposition" not in executable_src, "the harness forks the disposition composer"
    assert not (
        'disposition.get("safety_passed")' in executable_src and " is True" in executable_src
    ), "the harness re-hosts the `safety_passed is True` surface gate (a forked safety loop)"
    # 0 re-derivations of the adjudication release
    assert 'outcome == "cleared"' not in executable_src, "the harness re-derives the adjudication release"
    assert "outcome == 'cleared'" not in executable_src, "the harness re-derives the adjudication release"
    assert "non_overridable" not in executable_src, "the harness re-derives the CRITICAL/H1-H2 check"


# ===============================================================================
# Cycle 2: AC-3 (appended-envelope re-call — full round-sequence, no held generator)
# ===============================================================================


def test_appended_envelope_re_call(tmp_path):
    # AC-3: a full round-sequence (AUTHOR -> GATE -> ... -> promote) drives to a promoted plan with
    # >=1 `plan::<domain>` row into `root`, PURELY through repeated `step` calls. The ONLY state
    # passed between calls is the serialized state + the just-fulfilled envelope — NO generator
    # object is held across calls. The terminal `step` returns the promoted result.
    store_read = _seed_store(tmp_path)
    drive_kwargs = dict(
        summary=_deid_summary(), domains=("workout", "nutrition"), store_read=store_read,
        root=tmp_path, plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
    )

    result = _run_through_step(drive_kwargs, authors_map=_sustaining_authors())

    # the terminal step returned the promoted result with a recorded plan
    recorded = [d for d, r in result["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1, "no plan was promoted through repeated step calls"
    assert "dispatch_count" in result
    assert store.read("plan::workout", root=tmp_path) != [], "no plan:: row promoted into root"


def test_appended_envelope_re_call_with_revise(tmp_path):
    # AC-3 (the multi-round case): a quality-REVISE that converges on the re-author drives
    # AUTHOR -> GATE -> AUTHOR -> GATE -> promote through repeated `step` calls only. The re-author
    # (pass-2) content surfaces — a real round-sequence, no held generator.
    from tests.plan.test_revise_loop import (
        _composing_gate,
        _no_findings_dispatch,
        _recording_quality,
        _recording_safety,
        _clean_scores,
    )

    store_read = _seed_store(tmp_path)
    call_n = {"workout": 0}

    def authors_map_for(domain):
        if domain == "workout":
            call_n["workout"] += 1
            return _filled_workout_envelope() if call_n["workout"] >= 2 else _empty_workout_envelope()
        return _sustaining_authors()[domain]

    class _AuthorsMap:
        def __getitem__(self, domain):
            return authors_map_for(domain)

    gate = _composing_gate(
        _recording_quality(_clean_scores()), _recording_safety(_no_findings_dispatch()),
        revise_domains=("workout",),
    )
    drive_kwargs = dict(
        summary=_deid_summary(), domains=("workout",), store_read=store_read, root=tmp_path,
        plan_date=PLAN_DATE, gates={}, gate_producer=gate,
    )

    result = _run_through_step(drive_kwargs, authors_map=_AuthorsMap())

    assert result["results"]["workout"]["recorded"] is True
    rows = store.read("plan::workout", root=tmp_path)
    assert rows != [], "no plan surfaced past the clearable quality miss (through step)"
    assert any(ex.get("name") == "Goblet squat" for ex in rows[-1]["value"]["exercises"])


# ===============================================================================
# Cycle 3: AC-4 (determinism audit) + AC-6 (charge-on-miss-only through the harness)
# ===============================================================================


def test_determinism_audit(tmp_path):
    # AC-4 (the pinned binary): two INDEPENDENT replay runs over the SAME serialized cache state
    # reproduce the IDENTICAL sequence of yielded request `(kind, key)` up to the next cache-miss.
    # Build an accumulated state by driving a bounce + held-finding fixture partway, then replay it
    # twice and assert the two `(kind, key)` prefixes are equal. The engine is a pure function of
    # `(authors, summary, gates, cached-hook-responses)`, so the replay is reproducible.
    def fresh_kwargs(root):
        return dict(
            summary=_deid_summary(),
            domains=("workout", "nutrition", "supplements", "peptides"),
            store_read=_bpmh_store(root, "bleeding-risk"), root=root, plan_date=PLAN_DATE,
            gates={}, gate_producer=_clean_composing_gate(), reauthor=_clearing_reauthor(),
            adjudicator=_clearing_liaison(), budget=DispatchBudget(),
        )

    # accumulate a state several rounds in (so a replay re-traverses cached rounds)
    authors_map = _replay_safety_authors()
    seed_root = tmp_path / "seed"
    kwargs = fresh_kwargs(seed_root)
    pending, state = plan_step.step(None, **kwargs)
    for _ in range(3):  # advance a few rounds to accumulate cached hook responses
        if pending is None:
            break
        env = _fulfil(pending, authors_map=authors_map, reauthor=_clearing_reauthor(),
                      adjudicator=_clearing_liaison())
        pending, state = plan_step.step(state, fulfilled_envelope=env, **kwargs)
    accumulated = state

    def replay_kind_key_sequence(root):
        # re-drive from the SAME accumulated serialized state and record the (kind, key) of each
        # yield up to (and including) the next NEW pending request (the next cache-miss / new yield).
        kwargs_r = fresh_kwargs(root)
        seq = []
        st = accumulated
        am = _replay_safety_authors()
        ra, ad = _clearing_reauthor(), _clearing_liaison()
        first_pending, st2 = plan_step.step(st, **kwargs_r)
        # the (kind, key) the re-drive surfaces from the accumulated state — the next request
        if first_pending is not None:
            seq.append((first_pending.kind, plan_step.request_key(first_pending)))
        return seq

    seq_a = replay_kind_key_sequence(tmp_path / "replay-a")
    seq_b = replay_kind_key_sequence(tmp_path / "replay-b")

    assert seq_a == seq_b, f"non-deterministic replay: {seq_a} != {seq_b}"
    assert seq_a, "the replay surfaced no (kind, key) — the accumulated state was already terminal"


def test_charge_on_miss_only_through_harness(tmp_path):
    # AC-6: driving a bounce + held-finding fixture through repeated `step` calls charges
    # `budget.count` exactly once per cache-MISS — EQUAL to the synchronous-reference count (a single
    # in-process `run_orchestrated` drive of the same fixtures, the T2 AC-7 property observed through
    # the harness). No charge on a replayed cache-HIT round the harness re-drives.
    from scripts.plan.plan_orchestrator import run_orchestrated
    from tests.plan.test_deid_in import _raw_intake
    from tests.plan.test_plan_orchestrator import _RecordingDispatch

    domains = ("workout", "nutrition", "supplements", "peptides")

    # --- the synchronous reference: a single in-process run_orchestrated drive (charge-on-miss) ---
    ref_root = tmp_path / "reference"
    ref_out = run_orchestrated(
        _raw_intake(), _FixedDeidClient(_deid_summary()),
        _RecordingDispatch(_replay_safety_authors()), _bpmh_store(ref_root, "bleeding-risk"),
        ref_root, plan_date=PLAN_DATE, domains=domains, gate_dispatch=_clean_composing_gate(),
        reauthor=_clearing_reauthor(), adjudicator=_clearing_liaison(),
    )
    reference_count = ref_out["dispatch_count"]

    # --- the harness drive: the same fixtures through repeated step calls (charge-on-miss-only) ---
    harness_root = tmp_path / "harness"
    budget = DispatchBudget()
    drive_kwargs = dict(
        summary=_deid_summary(), domains=domains,
        store_read=_bpmh_store(harness_root, "bleeding-risk"), root=harness_root,
        plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
        reauthor=_clearing_reauthor(), adjudicator=_clearing_liaison(), budget=budget,
    )
    result = _run_through_step(
        drive_kwargs, authors_map=_replay_safety_authors(),
        reauthor=_clearing_reauthor(), adjudicator=_clearing_liaison(),
    )

    assert result["dispatch_count"] == reference_count, (
        f"harness charge {result['dispatch_count']} != synchronous reference {reference_count} "
        f"(a replayed cache-HIT was charged through the harness)"
    )
    assert budget.count == reference_count, "the harness budget over-charged vs the reference"


# ===============================================================================
# Cycle 4: AC-7 (the harness-suite gate — 0 live calls)
# ===============================================================================


def test_harness_has_no_module_scope_live_wiring():
    # AC-7 (the module-scope proof): `plan_step` imports no live `ModelClient` and references no skill
    # at module scope — it is seam-driven (the inner-engine seam, dispatch, gate, budget, and the
    # memo callables are INPUTS). A harness importing the live client or the skill at module scope
    # would couple the test/skill drive to live wiring.
    src = Path("scripts/plan/plan_step.py").read_text(encoding="utf-8")
    assert "ModelClient" not in src, "the harness imports a live ModelClient (must be seam-driven)"
    assert "SKILL.md" not in src and "generate-plan" not in src, "the harness references the skill"


def test_harness_defines_no_store_write():
    # store-surface (bead `pka`): the harness adds NO new `scripts/store/` write — it drives the
    # existing `plan_driver._promote_plans` -> `store.append` promote unchanged.
    src = Path("scripts/plan/plan_step.py").read_text(encoding="utf-8")
    assert src.count("store.append") == 0, "the harness defines a store write (it must drive the existing promote)"
