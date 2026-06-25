"""Tests for the A′-inversion self-test driver (ADR-0026-T4).

`scripts.plan._a_prime_self_test._self_test()` is the NON-TAUTOLOGICAL behavioral leg of the
mechanical core-capability gate (`scripts/core-capability-audit.sh`). It drives the ADR-0026-T1
shared driver (via its `run_orchestrated` consumer) with a fixture `dispatch` + the REAL
ADR-0026-T2 `compose_gate_dispatch` composer over fixture judge/review results (ARCH-4 — so the
behavioral leg exercises the T1↔T2 seam end-to-end), through de-id → loop → promote → render, and
asserts the INVERTED loop behaviors:

  - AC-3 (promotion-on-accept): the real composer over an ACCEPT-band fixture judge + a 0-finding
    fixture review emits an accept disposition → the driver promotes ≥1 plan. `_self_test()`
    returns 0 on this wired path.
  - AC-4 (0-plans-on-safety-not-True): the real composer over a fixture review that does NOT pass
    (≥1 finding → the composer's `safety_passed` surface goes not-True — the inversion comes from
    the real composer's fail-closed surface, NOT a hand-shaped not-True disposition) → the driver
    halts SAFETY_BLOCKED and surfaces 0 plans. A spine that surfaced ≥1 plan past a non-True safety
    disposition makes `_self_test()` return non-zero. This is what makes the pass NON-TAUTOLOGICAL —
    it exercises the INVERTED loop, not just "a plan renders."

The FAILURE signal is the NON-ZERO EXIT (QA-3) — `_self_test()` returns non-zero (and prints the
failing behavior) when either inversion breaks; the print is advisory, the exit code is
load-bearing (the audit consumes ONLY the exit code, stdout/stderr suppressed).

Every client / dispatch is a fixture mock; no test hits a live API, and the test tree carries 0
real operator PII (synthetic band/class tokens only).
"""

import re
import subprocess
from pathlib import Path

import scripts.plan._a_prime_self_test as ast_mod
from scripts.plan import plan_driver
from scripts.plan._a_prime_self_test import (
    BROKEN_SPINE_ENV,
    _broken_composer,
    _self_test,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_AUDIT = _REPO_ROOT / "scripts" / "core-capability-audit.sh"


def _audit_text():
    """The audit script's source (for the structural-repoint greps, AC-1/AC-2)."""
    return _AUDIT.read_text(encoding="utf-8")


def _non_comment_lines(text):
    """The audit's non-`#`-comment lines joined (so a token in a `#` comment is not a match)."""
    return "\n".join(
        line for line in text.splitlines() if not re.match(r"^\s*#", line)
    )


# === AC-3: non-tautological promotion-on-accept =================================


def test_self_test_promotes_on_accept():
    # AC-3: on the wired A′ spine the accept leg promotes ≥1 plan (the real composer over an
    # ACCEPT-band judge + a 0-finding review), so `_self_test()` returns 0. A self-test that
    # surfaced 0 plans on accept would return non-zero — this proves the accept inversion holds.
    assert _self_test() == 0, "the wired A′ spine did not return 0 (accept leg promoted 0 plans?)"


def test_accept_leg_records_at_least_one_plan():
    # AC-3 (the inner oracle, non-tautological): drive ONLY the accept leg and assert the driver
    # promoted ≥1 plan into the real store — not just that the run returned a value. A driver that
    # promoted nothing on the composer's accept disposition makes this RED.
    out, root = ast_mod._run_accept_leg()
    assert out.get("reason") is None, f"the accept leg halted: {out.get('reason')}"
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1, "the driver promoted 0 plans on the composer's accept disposition"


# === AC-4: non-tautological 0-plans-on-safety-not-True ==========================


def test_self_test_zero_plans_on_safety_not_true():
    # AC-4: the not-passing review leg surfaces 0 plans (the real composer's fail-closed
    # `safety_passed` goes not-True → the driver halts SAFETY_BLOCKED). `_self_test()` returns 0
    # only because BOTH inversion legs hold; this run keeps the safety leg honest.
    out, root = ast_mod._run_safety_not_true_leg()
    assert out.get("reason") == ast_mod.SAFETY_BLOCKED, (
        f"a not-passing review did not halt SAFETY_BLOCKED: {out.get('reason')}"
    )
    assert out["results"] == {}, "≥1 plan surfaced past a non-True safety disposition"


def test_self_test_returns_nonzero_when_safety_inversion_breaks():
    # AC-4 / QA-3 (the load-bearing inversion probe): inject a KNOWN-BROKEN spine (a
    # promote-everything composer that surfaces a plan PAST a non-True safety disposition) and
    # assert `_self_test()` returns NON-ZERO. A self-test that stayed 0 with the fail-closed gate
    # inverted is the exact PF-S63-02 tautology this criterion prevents.
    assert _self_test(composer_factory=_broken_composer) != 0, (
        "the self-test returned 0 with the fail-closed safety gate inverted (tautological pass)"
    )


def test_broken_spine_env_hook_inverts_the_gate(monkeypatch):
    # QA-3 (the env-hook arm the audit→self-test chain test drives): setting BROKEN_SPINE_ENV
    # injects the promote-everything composer, so `_self_test()` (with no explicit factory) returns
    # non-zero — this is the hook the broken-spine shell case sets to drive the audit RED.
    monkeypatch.setenv(BROKEN_SPINE_ENV, "1")
    assert _self_test() != 0, "the BROKEN_SPINE env hook did not invert the gate"


# === AC-6 / AC-7: fixture dispatch (0 live spend) ===============================


def test_self_test_uses_fixture_dispatch():
    # AC-6: the self-test constructs a fixture `dispatch` (a callable that returns a pre-mapped
    # author envelope) — it never reaches the live subscription dispatch (S94). The accept leg's
    # dispatch records its calls, proving it was the fixture seam.
    out, root = ast_mod._run_accept_leg()
    assert ast_mod._LAST_DISPATCH is not None and ast_mod._LAST_DISPATCH.calls, (
        "the accept leg did not drive a fixture dispatch (live dispatch reached?)"
    )


def test_self_test_constructs_no_live_model_client(monkeypatch):
    # AC-7: `_self_test()` runs over injected fixture clients only — it constructs no live
    # ModelClient (0 live spend). A ModelClient.__init__ spy confirms 0 self-constructed clients
    # across the whole self-test run.
    from scripts.model.client import ModelClient

    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)

    assert _self_test() == 0
    assert instantiations == [], "the self-test constructed a live ModelClient (must use mocks only)"


# === Cycle 2: the audit repoint (CALLER off generate_plan.py + structural A′-spine) ===


def test_audit_caller_repointed():
    # AC-1: the CALLER default is OFF generate_plan.py and ON the A′ driver plan_driver.py, with
    # plan_orchestrator.py pinned as the run_generation greppee (RUN_GEN_HOST). 0 references to
    # generate_plan.py as the CALLER default survive the repoint.
    body = _non_comment_lines(_audit_text())
    assert "scripts/plan/generate_plan.py" not in body, (
        "the audit still pins generate_plan.py as the CALLER (the repoint did not land)"
    )
    assert re.search(r'CALLER="\$\{CORE_CAP_CALLER:-\$REPO_ROOT/scripts/plan/plan_driver\.py\}"', body), (
        "the CALLER default is not the A′ driver plan_driver.py"
    )
    assert re.search(
        r'RUN_GEN_HOST="\$\{CORE_CAP_RUN_GEN_HOST:-\$REPO_ROOT/scripts/plan/plan_orchestrator\.py\}"',
        body,
    ), "the RUN_GEN_HOST greppee default is not plan_orchestrator.py"


def test_audit_structural_asserts_a_prime_spine():
    # AC-2 (PER-MODULE per QA-5): the structural checks assert each against its host, each an
    # EXECUTABLE reference — (1) the driver exists ([ -f "$CALLER" ]); (2) RUN_GEN_HOST references
    # pipeline.run_generation(; (3) the driver gates on disposition.get("safety_passed") is True plus
    # the accept / revise_domains reads. The retired record_plan( structural check is DROPPED.
    body = _non_comment_lines(_audit_text())
    assert '[ -f "$CALLER" ]' in body or '[ ! -f "$CALLER" ]' in body, (
        "the driver-exists structural check is missing"
    )
    assert "pipeline.run_generation" in body and "RUN_GEN_HOST" in body, (
        "the run_generation check is not pinned to RUN_GEN_HOST"
    )
    assert 'disposition.get("safety_passed") is True' in body, (
        "the executable disposition-gate surface is not asserted"
    )
    assert "revise_domains" in body, "the revise_domains read is not asserted"
    assert "record_plan(" not in body, (
        "the retired record_plan( structural check was not dropped (it would false-RED the A′ path)"
    )


def test_audit_invokes_a_prime_self_test():
    # AC-5/AC-6 (behavioral repoint): the audit invokes the A′ --self-test module, not
    # generate_plan --self-test, and states the live-dispatch boundary (S94).
    body = _non_comment_lines(_audit_text())
    assert "scripts.plan._a_prime_self_test --self-test" in body, (
        "the audit does not invoke the A′ self-test module"
    )
    assert "scripts.plan.generate_plan --self-test" not in body, (
        "the audit still invokes the retired generate_plan self-test"
    )
    # AC-6: an info/comment line states the live subscription dispatch is out of the audit's reach.
    full = _audit_text()
    assert re.search(r"(?i)live (subscription )?dispatch", full), (
        "the audit does not state the live-dispatch boundary (S94)"
    )


def test_audit_exits_zero_on_wired_spine():
    # AC-5: `bash scripts/core-capability-audit.sh` exits 0 on the wired A′ spine (structural +
    # behavioral checks pass under .venv).
    proc = subprocess.run(["bash", str(_AUDIT)], cwd=_REPO_ROOT, capture_output=True)
    assert proc.returncode == 0, (
        f"the audit did not exit 0 on the wired spine: exit={proc.returncode}\n"
        f"{proc.stderr.decode()}"
    )


# === Cycle 3: the audit→self-test exit-code chain (QA-3: RED on a known-broken spine) ===


def test_audit_propagates_broken_spine_nonzero_exit():
    # QA-3 (the load-bearing non-tautology proof): with the BROKEN_SPINE env hook set, the A′
    # self-test exits NON-ZERO, and `bash scripts/core-capability-audit.sh` PROPAGATES that
    # non-zero exit (does not swallow it to 0). The audit consumes ONLY the self-test's exit code
    # (stdout/stderr suppressed), so a self-test that printed "FAIL" but exit 0'd would read GREEN —
    # this proves the audit's behavioral leg goes RED THROUGH the exit-code path.
    # (a) the broken-spine self-test exits non-zero on its own.
    self_test = subprocess.run(
        [str(_REPO_ROOT / ".venv" / "bin" / "python"), "-m", "scripts.plan._a_prime_self_test", "--self-test"],
        cwd=_REPO_ROOT, capture_output=True,
        env={**__import__("os").environ, "PYTHONPATH": str(_REPO_ROOT), BROKEN_SPINE_ENV: "1"},
    )
    assert self_test.returncode != 0, "the broken-spine self-test did not exit non-zero"
    # (b) the audit propagates the broken-spine self-test's non-zero exit.
    audit = subprocess.run(
        ["bash", str(_AUDIT)], cwd=_REPO_ROOT, capture_output=True,
        env={**__import__("os").environ, BROKEN_SPINE_ENV: "1"},
    )
    assert audit.returncode != 0, (
        f"the audit swallowed the broken-spine self-test's non-zero exit to {audit.returncode} "
        f"(the PF-S63-02 tautology)"
    )


# ===============================================================================
# ADR-0028-T5 Cycle 1: the REAUTHOR + ADJUDICATOR replay-leg fixtures + drivers
# ===============================================================================
#
# The existing self-test (`_sustaining_authors`, `_finding_dispatch`) yields 0 REAUTHOR + 0
# ADJUDICATOR — the throw/replay path (ADR-0028-T2) is never EXERCISED behaviorally. These legs add
# a NON-sustaining-author fixture (a real energy bounce -> a REAUTHOR yield/replay) and a
# held-finding-author fixture (an author-declared cross-domain conflict -> an ADJUDICATOR
# yield/replay), driving the REAL `run_orchestrated` consumer over a clean composed gate with a
# fixture `reauthor` / `adjudicator` hook. The recording hooks + the kind-recording dispatch / gate
# capture the yielded `Request.kind` sequence in fulfilment order (the consumer fulfils each yield
# synchronously, so the recorded order IS the yield order). 0 live spend, synthetic PII-free tokens.


def test_reauthor_leg_yields_reauthor_between_author_and_gate():
    # AC-1: the non-sustaining-author leg (workout over the nutrition energy ceiling, nutrition
    # `energy_budget.sustains is False`) drives a REAL energy bounce -> the memo `reauthor` callable
    # raises the sentinel on the cache-miss pass -> `drive` yields a REAUTHOR request -> the consumer
    # re-authors -> `drive` caches + re-drives. Assert the yielded kind sequence carries >=1 REAUTHOR
    # BETWEEN the first AUTHOR and the first GATE.
    out, kinds, reauthor_calls = ast_mod._run_reauthor_leg()
    assert kinds.count(plan_driver.REAUTHOR) >= 1, f"no REAUTHOR yielded: {kinds}"
    first_author = kinds.index(plan_driver.AUTHOR)
    first_reauthor = kinds.index(plan_driver.REAUTHOR)
    first_gate = kinds.index(plan_driver.GATE)
    assert first_author < first_reauthor < first_gate, f"REAUTHOR not between AUTHOR and GATE: {kinds}"


def test_adjudicator_leg_yields_adjudicator_between_author_and_gate():
    # AC-2: the held-finding leg (one domain declares a cross-domain conflict via
    # `reconciliation.conflicts`) HOLDS the declaring domain -> the memo `adjudicator` callable raises
    # the sentinel on the cache-miss pass -> `drive` yields an ADJUDICATOR request. Assert the yielded
    # kind sequence carries >=1 ADJUDICATOR between the first AUTHOR and the first GATE.
    out, kinds, adjudicator_calls = ast_mod._run_adjudicator_leg()
    assert kinds.count(plan_driver.ADJUDICATOR) >= 1, f"no ADJUDICATOR yielded: {kinds}"
    first_author = kinds.index(plan_driver.AUTHOR)
    first_adjudicator = kinds.index(plan_driver.ADJUDICATOR)
    first_gate = kinds.index(plan_driver.GATE)
    assert first_author < first_adjudicator < first_gate, f"ADJUDICATOR not between AUTHOR and GATE: {kinds}"


def test_replay_rounds_advance_exactly_one_dispatch_each():
    # AC-3: each replay round advances exactly ONE new cache-MISS dispatch (one new memo key), and the
    # cached terminal replay re-fires NONE of them. The reauthor leg dispatches its hook EXACTLY once
    # (one bounce key); the adjudicator leg dispatches its hook EXACTLY once per held finding, each a
    # distinct key. A cached replay that re-raised (re-dispatched) a cached key would inflate these.
    _, _, reauthor_calls = ast_mod._run_reauthor_leg()
    assert len(reauthor_calls) == 1, f"reauthor re-dispatched on a cached replay: {reauthor_calls}"
    _, _, adjudicator_calls = ast_mod._run_adjudicator_leg()
    assert len(adjudicator_calls) == 1, f"adjudicator re-dispatched on a cached replay: {adjudicator_calls}"
    assert len(set(adjudicator_calls)) == len(adjudicator_calls), (
        f"a held finding fired more than once on the cached replay: {adjudicator_calls}"
    )


def test_replay_legs_complete_on_terminal_cache_all_hit():
    # AC-4: after the last replay round caches the last hook response, the terminal cache-all-hit
    # re-drive completes (0 sentinels escape) and returns a terminal `run_generation` result. The
    # reauthor leg's fuelable re-author surfaces (a promote); the adjudicator leg's cleared held domain
    # surfaces — a terminal result (a promote OR an honest-no-plan halt), never an escaping sentinel.
    out_reauthor, _, _ = ast_mod._run_reauthor_leg()
    assert "results" in out_reauthor, "the reauthor leg did not return a terminal run_generation result"
    assert out_reauthor["results"]["workout"]["recorded"] is True, (
        "the fuelable re-authored workout did not surface on the terminal replay"
    )
    out_adjudicator, _, _ = ast_mod._run_adjudicator_leg()
    assert "results" in out_adjudicator, "the adjudicator leg did not return a terminal run_generation result"
    assert out_adjudicator["results"]["workout"]["recorded"] is True, (
        "the cleared held domain did not surface on the terminal replay"
    )


# ===============================================================================
# ADR-0028-T5 Cycle 2: the non-tautology floor + the preserved gates + the audit
# ===============================================================================


def test_non_tautology_contrast_sustaining_yields_zero_replay():
    # AC-5 (the non-tautology FLOOR, AR-002 / PF-S63-02): the SAME typed-request protocol over the
    # SUSTAINING fixture (BOTH hooks wired) yields 0 REAUTHOR + 0 ADJUDICATOR, WHILE the new
    # non-sustaining + held-finding fixtures yield >=1 of each. The explicit CONTRAST proves the >=1
    # comes from the FIXTURE (a real bounce / a real hold), not from the protocol always yielding —
    # the property that would be UNSATISFIABLE by the pre-existing sustaining fixtures.
    _, sustaining_kinds = ast_mod._run_sustaining_replay_leg()
    assert sustaining_kinds.count(plan_driver.REAUTHOR) == 0, (
        f"the sustaining fixture yielded a REAUTHOR (no real bounce should fire): {sustaining_kinds}"
    )
    assert sustaining_kinds.count(plan_driver.ADJUDICATOR) == 0, (
        f"the sustaining fixture yielded an ADJUDICATOR (no held finding should fire): {sustaining_kinds}"
    )
    _, reauthor_kinds, _ = ast_mod._run_reauthor_leg()
    _, adjudicator_kinds, _ = ast_mod._run_adjudicator_leg()
    assert reauthor_kinds.count(plan_driver.REAUTHOR) >= 1, "the non-sustaining fixture yielded 0 REAUTHOR"
    assert adjudicator_kinds.count(plan_driver.ADJUDICATOR) >= 1, "the held-finding fixture yielded 0 ADJUDICATOR"


def test_self_test_drives_reauthor_leg_and_breaks_nonzero(monkeypatch):
    # AC-6 (the self-test DRIVES the reauthor leg): a replay-leg-break analogue — stub the reauthor
    # leg to yield 0 REAUTHOR (the throw/replay path removed) and assert `_self_test()` returns
    # NON-ZERO. If `_self_test()` did not drive the reauthor leg, the stub would be inert and it would
    # stay 0 — so this is RED until the self-test gains the reauthor-inversion check.
    real_leg = ast_mod._run_reauthor_leg

    def zero_reauthor_leg(**kwargs):
        out, kinds, calls = real_leg(**kwargs)
        return out, [k for k in kinds if k != plan_driver.REAUTHOR], calls

    monkeypatch.setattr(ast_mod, "_run_reauthor_leg", zero_reauthor_leg)
    assert _self_test() != 0, "the self-test did not catch a reauthor leg yielding 0 REAUTHOR"


def test_self_test_drives_adjudicator_leg_and_breaks_nonzero(monkeypatch):
    # AC-6 (the self-test DRIVES the adjudicator leg): the symmetric replay-leg-break analogue — stub
    # the adjudicator leg to yield 0 ADJUDICATOR and assert `_self_test()` returns NON-ZERO.
    real_leg = ast_mod._run_adjudicator_leg

    def zero_adjudicator_leg(**kwargs):
        out, kinds, calls = real_leg(**kwargs)
        return out, [k for k in kinds if k != plan_driver.ADJUDICATOR], calls

    monkeypatch.setattr(ast_mod, "_run_adjudicator_leg", zero_adjudicator_leg)
    assert _self_test() != 0, "the self-test did not catch an adjudicator leg yielding 0 ADJUDICATOR"


# ===============================================================================
# ADR-0028-T5 Cycle 3: the RED-capability proof (the load-bearing non-tautology)
# ===============================================================================
#
# The non-tautology floor is RED-CAPABLE: the >=1-REAUTHOR / >=1-ADJUDICATOR assertion FAILS when the
# throw/replay path (ADR-0028-T2) is removed. The sentinel-SWALLOWING mutant returns a benign value on
# a cache MISS instead of raising `_ReplayNeeded`, so `drive` NEVER yields a REAUTHOR / ADJUDICATOR
# request — driving the SAME fixtures through it makes the >=1 assertion go RED. This proves the >=1 is
# NOT satisfiable by a driver that does not EXERCISE the replay path (the AR-002 / PF-S63-02 floor).


def test_red_capability_swallowed_replay_yields_zero_reauthor():
    # AC-5 / AR-002 (RED-CAPABLE, the load-bearing proof): drive the SAME non-sustaining fixture
    # through the sentinel-SWALLOWING mutant and assert it yields 0 REAUTHOR — the >=1-REAUTHOR
    # assertion goes RED against a driver that does not exercise the throw/replay path.
    _, kinds, calls = ast_mod._run_reauthor_leg(swallow_replay=True)
    assert kinds.count(plan_driver.REAUTHOR) == 0, f"the swallow mutant still yielded a REAUTHOR: {kinds}"
    assert calls == [], "the swallow mutant still dispatched the reauthor hook (the sentinel was not swallowed)"


def test_red_capability_swallowed_replay_yields_zero_adjudicator():
    # AC-5 / AR-002 (the symmetric RED-capability proof): the SAME held-finding fixture through the
    # swallow mutant yields 0 ADJUDICATOR — the >=1-ADJUDICATOR assertion goes RED.
    _, kinds, calls = ast_mod._run_adjudicator_leg(swallow_replay=True)
    assert kinds.count(plan_driver.ADJUDICATOR) == 0, f"the swallow mutant still yielded an ADJUDICATOR: {kinds}"
    assert calls == [], "the swallow mutant still dispatched the adjudicator hook (the sentinel was not swallowed)"


def test_red_capability_wired_path_still_yields_the_contrast():
    # the CONTRAST that gives the mutant teeth: the SAME legs on the WIRED path (swallow_replay=False,
    # the default) yield >=1 each. RED with the mutant, GREEN on the wired spine — the proof the >=1
    # assertion DEPENDS on the throw/replay path, not asserted vacuously.
    _, kinds_reauthor, _ = ast_mod._run_reauthor_leg(swallow_replay=False)
    _, kinds_adjudicator, _ = ast_mod._run_adjudicator_leg(swallow_replay=False)
    assert kinds_reauthor.count(plan_driver.REAUTHOR) >= 1, "the wired reauthor leg yielded 0 REAUTHOR"
    assert kinds_adjudicator.count(plan_driver.ADJUDICATOR) >= 1, "the wired adjudicator leg yielded 0 ADJUDICATOR"


def test_swallow_replay_env_hook_breaks_self_test(monkeypatch):
    # AC-6 (the replay-leg-break analogue at the exit-code level): with SWALLOW_REPLAY_ENV set,
    # `_self_test()` drives the replay legs through the swallow mutant -> 0 REAUTHOR / 0 ADJUDICATOR ->
    # the replay-leg inversion fails -> `_self_test()` returns NON-ZERO (the audit->self-test chain
    # goes RED on a broken throw/replay path, mirroring the BROKEN_SPINE_ENV arm).
    monkeypatch.setenv(ast_mod.SWALLOW_REPLAY_ENV, "1")
    assert _self_test() != 0, "the SWALLOW_REPLAY env hook did not break the replay-leg inversion"
