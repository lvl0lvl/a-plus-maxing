"""The A′-inversion self-test — the NON-TAUTOLOGICAL behavioral leg of the core-capability gate.

The mechanical core-capability gate (`scripts/core-capability-audit.sh`, PF-S63-02 /
INV-CORE-CAPABILITY) proves the A′ spine stays wired end-to-end. Its structural greps prove the
SHAPE; this self-test proves it RUNS — and proves it runs NON-TAUTOLOGICALLY, by driving the
shared driver (ADR-0026-T1, via its `run_orchestrated` consumer) with a fixture `dispatch` + the
REAL composed `gate_dispatch` (ADR-0026-T2) over fixture judge/review results (ARCH-4 — the
behavioral leg exercises the T1↔T2 seam end-to-end), through de-id → loop → promote → render, and
asserting the INVERTED loop behaviors:

  - PROMOTION-ON-ACCEPT (AC-3): the real composer over an ACCEPT-band fixture judge + a 0-finding
    fixture review emits an accept disposition → the driver promotes ≥1 plan.
  - 0-PLANS-ON-SAFETY-NOT-TRUE (AC-4): the real composer over a fixture review that does NOT pass
    (≥1 finding → the composer's `safety_passed` surface goes not-True, the FAIL-CLOSED inversion
    from the real composer, NOT a hand-shaped not-True disposition) → the driver halts
    SAFETY_BLOCKED and surfaces 0 plans.

A gate asserting only "a plan renders" is tautological; asserting the INVERSION (a plan promotes on
accept AND 0 plans surface past a non-True safety disposition) is the PF-S63-02 discipline.

The FAILURE SIGNAL is the NON-ZERO RETURN/EXIT (QA-3), never a printed message: the audit consumes
ONLY this module's exit code (stdout/stderr suppressed), so a self-test that PRINTED "FAIL" but
returned 0 would read GREEN. `_self_test()` returns 0 iff BOTH inversion legs hold, non-zero (and
prints the failing leg) when either breaks. The `--self-test` CLI entry
(`python -m scripts.plan._a_prime_self_test --self-test`) is what the audit invokes.

Modeled on `generate_plan._self_test`: self-contained synthetic PII-free fixtures (no test-tree
import — production must not depend on `tests/`), 0 live spend (the de-id client, the specialist
`dispatch`, and the composer's judge/review are all fixture mocks). The LIVE subscription dispatch
is OUT of scope (the S94 operator-present attestation): this self-test uses a fixture `dispatch`,
never the live backend.
"""

import functools
import os
import tempfile
from pathlib import Path

from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.plan.plan_orchestrator import SAFETY_BLOCKED, run_orchestrated  # noqa: F401  (SAFETY_BLOCKED re-exported for the suite)
from scripts.store import keying, store

# The env hook the audit→self-test exit-code chain test (QA-3) sets to inject the KNOWN-BROKEN
# (promote-everything) spine WITHOUT making it a production path. A loud WARNING fires if it is set
# in production (mirrors the audit's CORE_CAP_* test-hook warnings) — it is a tests/CI hook only.
BROKEN_SPINE_ENV = "A_PRIME_SELF_TEST_BROKEN_SPINE"

_PLAN_DATE = "2026-06-18"

# A fixture dispatch the LAST run constructed — exposed so the suite can assert the self-test drove
# a fixture seam (AC-6), never the live subscription dispatch. Reset on each leg.
_LAST_DISPATCH = None


# --- synthetic PII-free fixtures (self-contained; modeled on generate_plan._self_test) ---


def _deid_summary():
    """A de-identified summary (band/class tokens only — 0 raw-PII, what a faithful de-id emits)."""
    return {
        "training-age-band": "10-15y",
        "sex-for-dosing": "male",
        "bodyweight-band": "80-90kg",
        "goal-domains": ["workout", "nutrition"],
        "active-issue-class": "musculoskeletal-recovery",
        "recovery-status-band": "moderate",
    }


def _raw_intake():
    """A synthetic raw plan-intake (the de-id client maps it to the PII-free summary, never echoed)."""
    return {
        "legal-name": "Jordan Faketestperson",
        "raw-lab-values": "ALT 412 U/L",
        "goal-targets": "return to pre-Jan-2026 loading",
    }


class _FixedDeidClient:
    """A fixture de-id client: `deidentify(raw_intake)` returns a fixed PII-free summary (0 spend)."""

    def __init__(self, summary):
        self._summary = summary

    def deidentify(self, raw_intake):
        return self._summary


class _RecordingDispatch:
    """A specialist-dispatch seam returning a pre-mapped author envelope per domain (0 spend).

    Records every `(domain, prompt, summary)` call so the self-test can attest it drove a FIXTURE
    dispatch (AC-6), never the live subscription dispatch (S94).

    Attributes:
        authors (dict): domain -> the author envelope to return for that domain.
    """

    def __init__(self, authors):
        self.authors = authors
        self.calls = []

    def __call__(self, domain, prompt, summary):
        self.calls.append({"domain": domain})
        return self.authors[domain]


class _FixedJudgeClient:
    """A fixture QUALITY judge: `judge(payload)` returns a fixed per-dimension score map (0 spend)."""

    def __init__(self, scores):
        self._scores = scores

    def judge(self, payload):
        return dict(self._scores)


def _clean_scores():
    """An ACCEPT-band score map (every rubric dimension at 9 → the judge ACCEPTs)."""
    return {
        "followability": 9,
        "coherence": 9,
        "internal consistency": 9,
        "completeness": 9,
    }


def _no_findings_dispatch():
    """A safety-lens dispatch where every lens emits 0 findings (review passes → safety_passed)."""
    def dispatch(lens, prompt, assembled_plan):
        return []

    return dispatch


def _finding_dispatch():
    """A safety-lens dispatch where one lens emits ≥1 finding (review does NOT pass → not-True).

    The not-passing review is what drives the real composer's `safety_passed` surface to not-True
    (the FAIL-CLOSED inversion comes from the real composer, not a hand-shaped disposition).
    """
    def dispatch(lens, prompt, assembled_plan):
        if lens == "medical-safety-reviewer":
            return [{
                "id": "cumulative-hepatic-load",
                "concern": "cumulative hepatic load across domains exceeds the safe ceiling",
                "severity": "high",
            }]
        return []

    return dispatch


def _seed_store(root):
    """Seed PII-free operator-state items into a real temp store; return a bound reader."""
    fields = {
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
    }
    for item, value in fields.items():
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": _PLAN_DATE, "source": "intake", "value": value},
            root=root,
        )
    return functools.partial(store.read, root=root)


def _workout_rec(name, sets):
    """A complete workout recommendation (universal contract + workout payload)."""
    return {
        "claim": f"perform {name.lower()} to rebuild a movement base",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        "payload": {"name": name, "sets": sets, "reps": "8-12", "detail": "controlled tempo"},
    }


def _nutrition_target_rec():
    """A nutrition day-target recommendation (calorie + macro payload)."""
    return {
        "claim": "set energy and protein at maintenance to support training recovery",
        "source": "ISSN position stand on protein and exercise 2017",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "nutrition",
        "payload": {
            "calorie_goal": 2400,
            "macros": {"protein": 180, "carbs": 240, "fat": 70},
        },
    }


def _nutrition_meal_rec(name, kcal):
    """A nutrition single-meal recommendation (payload carries one `meal`)."""
    return {
        "claim": f"distribute protein across the day with {name.lower()}",
        "source": "ISSN position stand on protein and exercise 2017",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "nutrition",
        "payload": {"meal": {"name": name, "kcal": kcal}},
    }


def _sustaining_authors():
    """A clean two-domain author set: a fuelable workout + a sustaining nutrition budget."""
    return {
        "workout": {
            **{"specialist": "personal-trainer",
               "recommendations": [_workout_rec("Goblet squat", 3)]},
            "reconciliation": {"energy_cost_kcal": 500},
        },
        "nutrition": {
            **{"specialist": "nutritionist",
               "recommendations": [_nutrition_target_rec(), _nutrition_meal_rec("Breakfast", 600)]},
            "reconciliation": {
                "energy_budget": {"sustains": True, "sustainable_training_kcal": 700},
            },
        },
    }


# --- the real composer + the broken-spine inversion ----------------------------


def _real_composer(judge_client, review_dispatch):
    """The REAL composed `gate_dispatch` over the fixture judge/review (ARCH-4, the T1↔T2 seam)."""
    return compose_gate_dispatch(judge_client, review_dispatch)


def _broken_composer(judge_client, review_dispatch):
    """A KNOWN-BROKEN promote-everything composer — the fail-closed gate INVERTED (QA-3 probe).

    Returns a `gate_dispatch` that surfaces an accept + `safety_passed: True` disposition for EVERY
    plan regardless of the review's findings — so a plan surfaces PAST a non-True safety disposition,
    inverting the fail-closed gate. The self-test's safety-not-True leg must then surface ≥1 plan,
    breaking the inversion assertion → `_self_test()` returns non-zero (the audit→self-test
    exit-code chain goes RED). This is the deliberately-broken spine, never a production path.
    """
    def gate_dispatch(assembled_plan):
        return {"accept": True, "safety_passed": True, "revise_domains": []}

    return gate_dispatch


# --- the two inversion legs ----------------------------------------------------


def _run_accept_leg(composer_factory=_real_composer):
    """Drive the accept leg: real composer over an ACCEPT judge + a 0-finding review.

    Returns the `run_orchestrated` result + the store root so the caller can assert ≥1 plan
    promoted (the promotion-on-accept inversion).

    Returns:
        (dict) The `run_orchestrated` result.
        (Path) The store root the plans promoted into.
    """
    global _LAST_DISPATCH
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    _LAST_DISPATCH = dispatch
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "accept"
        store_read = _seed_store(root)
        gate = composer_factory(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())
        out = run_orchestrated(
            _raw_intake(), deid_client, dispatch, store_read, root,
            plan_date=_PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
        )
        return out, root


def _run_safety_not_true_leg(composer_factory=_real_composer):
    """Drive the safety-not-True leg: real composer over a NOT-passing review (≥1 finding).

    On the wired spine the real composer's `safety_passed` surface goes not-True → the driver halts
    SAFETY_BLOCKED, 0 plans surface. A broken (promote-everything) composer surfaces ≥1 plan past
    the non-True disposition — the inversion the self-test catches.

    Returns:
        (dict) The `run_orchestrated` result.
        (Path) The store root.
    """
    global _LAST_DISPATCH
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _RecordingDispatch(_sustaining_authors())
    _LAST_DISPATCH = dispatch
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "blocked"
        store_read = _seed_store(root)
        gate = composer_factory(_FixedJudgeClient(_clean_scores()), _finding_dispatch())
        out = run_orchestrated(
            _raw_intake(), deid_client, dispatch, store_read, root,
            plan_date=_PLAN_DATE, domains=("workout", "nutrition"), gate_dispatch=gate,
        )
        return out, root


def _self_test(composer_factory=None):
    """Run the A′-inversion self-test; return 0 iff BOTH inversion legs hold, else non-zero.

    The behavioral core-capability gate (PF-S63-02, NON-TAUTOLOGICAL): (a) the accept leg promotes
    ≥1 plan on the real composer's accept disposition, and (b) the safety-not-True leg surfaces 0
    plans past the real composer's fail-closed (not-True) disposition. Returns 0 only when BOTH
    hold; returns non-zero (and prints the failing leg — the print is advisory, the exit code is the
    load-bearing failure signal, QA-3) when either inversion breaks.

    Args:
        composer_factory (Callable, optional): The `(judge_client, review_dispatch) -> gate_dispatch`
            composer factory. Defaults to the REAL `compose_gate_dispatch` — or the broken
            promote-everything composer when `A_PRIME_SELF_TEST_BROKEN_SPINE` is set (the QA-3
            exit-code-chain hook; a loud WARNING fires, it is a tests/CI hook, never production).

    Returns:
        (int) 0 when both inversions hold; non-zero when either breaks.
    """
    if composer_factory is None:
        if os.environ.get(BROKEN_SPINE_ENV):
            print(
                f"a-prime self-test: WARNING: test-hook env var {BROKEN_SPINE_ENV} is active "
                f"(tests/CI only — injecting the known-broken promote-everything spine)"
            )
            composer_factory = _broken_composer
        else:
            composer_factory = _real_composer

    # (a) PROMOTION-ON-ACCEPT: the accept leg must promote ≥1 plan.
    out_accept, _ = _run_accept_leg(composer_factory)
    if out_accept.get("reason") is not None:
        print(f"a-prime self-test FAIL: the accept leg halted ({out_accept.get('reason')})")
        return 1
    recorded = [d for d, r in out_accept["results"].items() if r.get("recorded") is True]
    if len(recorded) < 1:
        print("a-prime self-test FAIL: the driver promoted 0 plans on the composer's accept disposition")
        return 1

    # (b) 0-PLANS-ON-SAFETY-NOT-TRUE: the not-passing review leg must surface 0 plans.
    out_blocked, _ = _run_safety_not_true_leg(composer_factory)
    if out_blocked.get("results"):
        print(
            "a-prime self-test FAIL: ≥1 plan surfaced past a non-True safety disposition "
            "(the fail-closed gate is inverted — the PF-S63-02 tautology)"
        )
        return 1

    print(
        "a-prime self-test PASS: promotion-on-accept + 0-plans-on-safety-not-True "
        "(de-id -> driver -> real composer -> promote -> render, the A′ spine wired)"
    )
    return 0


def main(argv=None):
    """CLI entry: `--self-test` runs the A′-inversion behavioral gate check.

    The only CLI action is the deterministic self-test the mechanical core-capability gate invokes
    (`python -m scripts.plan._a_prime_self_test --self-test`). The autonomous GENERATE pass runs via
    the orchestrator (runtime A), not this CLI.
    """
    import argparse

    parser = argparse.ArgumentParser(description="A′-inversion core-capability self-test.")
    parser.add_argument(
        "--self-test", action="store_true",
        help="run the A′-inversion self-test (the core-capability gate's behavioral check)",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    parser.error("no action; use --self-test")


if __name__ == "__main__":
    import sys

    sys.exit(main())
