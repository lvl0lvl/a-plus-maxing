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
