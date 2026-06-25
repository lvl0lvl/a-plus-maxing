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

import contextlib
import functools
import os
import tempfile
from pathlib import Path

from scripts.plan import adjudicate, plan_driver
from scripts.plan import quality_judge as quality_judge_mod
from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.plan.plan_orchestrator import SAFETY_BLOCKED, run_orchestrated  # noqa: F401  (SAFETY_BLOCKED re-exported for the suite)
from scripts.store import keying, store

# The env hook the audit→self-test exit-code chain test (QA-3) sets to inject the KNOWN-BROKEN
# (promote-everything) spine WITHOUT making it a production path. A loud WARNING fires if it is set
# in production (mirrors the audit's CORE_CAP_* test-hook warnings) — it is a tests/CI hook only.
BROKEN_SPINE_ENV = "A_PRIME_SELF_TEST_BROKEN_SPINE"

# The env hook the RED-capability check sets to SWALLOW the REAUTHOR / ADJUDICATOR throw/replay
# sentinel (the ADR-0028-T2 throw/replay path REMOVED), so the replay legs yield 0 REAUTHOR / 0
# ADJUDICATOR — the non-tautology proof (AR-002 / PF-S63-02) that the ≥1-yield assertion is NOT
# satisfiable without the throw/replay path. A loud WARNING fires if it is set in production (mirrors
# BROKEN_SPINE_ENV) — it is a tests/CI hook only, never a production path.
SWALLOW_REPLAY_ENV = "A_PRIME_SELF_TEST_SWALLOW_REPLAY"

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


# --- the replay-path fixtures (ADR-0028-T5): a real energy bounce + a held finding ---


def _non_sustaining_authors():
    """A NON-sustaining two-domain author set: a workout OVER the nutrition energy ceiling.

    The workout `reconciliation.energy_cost_kcal` (900) exceeds the nutrition
    `reconciliation.energy_budget.sustainable_training_kcal` (450) with `energy_budget.sustains:
    False` — so the reconciler fires a REAL energy bounce ([orchestrate.py:382-390]) and the engine
    calls the `reauthor` hook, driving the REAUTHOR throw/replay path (ADR-0028-T2). The CONTRAST to
    `_sustaining_authors` (which yields 0 REAUTHOR).
    """
    return {
        "workout": {
            "specialist": "personal-trainer",
            "recommendations": [_workout_rec("Heavy back squat", 5)],
            "reconciliation": {"energy_cost_kcal": 900},
        },
        "nutrition": {
            "specialist": "nutritionist",
            "recommendations": [_nutrition_target_rec(), _nutrition_meal_rec("Breakfast", 600)],
            "reconciliation": {
                "energy_budget": {"sustains": False, "sustainable_training_kcal": 450},
            },
        },
    }


def _held_finding_authors():
    """A held-finding two-domain author set: the workout declares a cross-domain conflict.

    The workout `reconciliation.conflicts` carries one string-`with` entry, so the reconciler holds
    the DECLARING (workout) domain `conflict_held` ([orchestrate.py:413-418]) and `generate_plans`
    routes it to `_adjudicate_with_band` ([orchestrate.py:595]) — driving the ADJUDICATOR throw/replay
    path (ADR-0028-T2). The nutrition budget SUSTAINS (no energy bounce → 0 REAUTHOR). The
    cross-domain-conflict axis is the minimal single-domain ADJUDICATOR trigger (no second compound
    candidate, no operator-Rx-class seeding; recipe Deviation #1). Synthetic PII-free tokens only.
    """
    return {
        "workout": {
            "specialist": "personal-trainer",
            "recommendations": [_workout_rec("Goblet squat", 3)],
            "reconciliation": {
                "energy_cost_kcal": 500,
                "conflicts": [{"with": "synthetic-compound", "with_domain": "supplements",
                               "reason": "synthetic cross-domain conflict (fixture)"}],
            },
        },
        "nutrition": {
            "specialist": "nutritionist",
            "recommendations": [_nutrition_target_rec(), _nutrition_meal_rec("Breakfast", 600)],
            "reconciliation": {
                "energy_budget": {"sustains": True, "sustainable_training_kcal": 700},
            },
        },
    }


def _override_record():
    """A content-valid HIGH override record (synthetic, PII-free) the clearing liaison carries.

    Mirrors the `adjudicate.validate_override_record` content schema (the canonical override literal,
    a content-bearing operator_reason at the HIGH evidence rung, a risks-of-proceeding clause, a
    contradictions-log ref). `caution_verbatim` is set by the liaison to the held finding's caution
    verbatim (the release condition). Synthetic tokens only — 0 raw operator PII.
    """
    return {
        "caution_verbatim": "",  # the liaison sets this verbatim to the finding's caution
        "composite_band": "HIGH",
        "risks_communicated": {
            "risks_of_proceeding": (
                "Proceeding may compound the flagged cross-domain interaction; the combined load is "
                "not offset by home monitoring."
            ),
        },
        "operator_reason": (
            "Accepting the monitored cross-domain tradeoff for the recovery benefit, under physician "
            "follow-up."
        ),
        "evidence_tier_required": adjudicate.evidence_tier_required("HIGH"),
        "evidence_provided": {"rung": "understanding+appreciation+reasoning"},
        "override_literal": adjudicate.OVERRIDE_LITERAL,
        "voluntariness_note": "Chosen without coercion after the risks were explained.",
        "timestamp": "2026-06-25T10:00:00-04:00",
        "contradictions_log_ref": "vault/meta/contradictions.md#fixture",
    }


def _clearing_liaison_envelope(finding_id):
    """A content-valid HIGH liaison adjudication envelope that clears a held finding (synthetic)."""
    return {
        "finding_id": finding_id,
        "composite_band": "HIGH",
        "harm_class": None,
        "severity_final": {"set_by": adjudicate.LIAISON_SET_BY},
        "override_record": _override_record(),
    }


def _recording_reauthor(kinds):
    """A spied energy-bounce re-author hook: appends a REAUTHOR kind per call, returns a fuelable session.

    The re-authored workout's `reconciliation.energy_cost_kcal` (400) is UNDER the bounce ceiling
    (450), so the replayed pass completes (the workout surfaces, not the `ENERGY_BOUNCE_UNRESOLVED`
    hold). Records every call on `.calls` (one per cache-MISS dispatch).
    """
    calls = []

    def reauthor(domain, constraint):
        kinds.append(plan_driver.REAUTHOR)
        calls.append((domain, constraint.get("sustainable_training_kcal")))
        return {
            "specialist": "personal-trainer",
            "recommendations": [_workout_rec("Light goblet squat", 2)],
            "reconciliation": {"energy_cost_kcal": 400},
        }

    reauthor.calls = calls
    return reauthor


def _recording_adjudicator(kinds):
    """A spied medical-liaison hook: appends an ADJUDICATOR kind per call, clears with a content-valid override.

    Echoes the held finding's caution verbatim into the override record (the release condition), so a
    held domain releases and the pass surfaces. Records every call on `.calls` (one per cache-MISS
    dispatch).
    """
    calls = []

    def adjudicator(safety_finding):
        kinds.append(plan_driver.ADJUDICATOR)
        calls.append((safety_finding["source"], safety_finding["held_domain"]))
        envelope = _clearing_liaison_envelope(safety_finding["finding_id"])
        envelope["override_record"]["caution_verbatim"] = safety_finding["caution"]
        return envelope

    adjudicator.calls = calls
    return adjudicator


def _kind_recording_dispatch(authors, kinds):
    """A fixture dispatch over `authors` that records an AUTHOR kind per specialist dispatch (0 spend)."""
    base = _RecordingDispatch(authors)

    def dispatch(domain, prompt, summary):
        kinds.append(plan_driver.AUTHOR)
        return base(domain, prompt, summary)

    dispatch.base = base
    return dispatch


def _kind_recording_gate(kinds):
    """A clean composed gate (ACCEPT + 0 findings) recording a GATE kind per producer dispatch."""
    producer = _real_composer(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())

    def gate(assembled_plan):
        kinds.append(plan_driver.GATE)
        return producer(assembled_plan)

    return gate


# --- the real composer + the broken-spine inversion ----------------------------


def _real_composer(judge_client, review_dispatch):
    """The REAL composed `gate_dispatch` over the fixture judge/review (ARCH-4, the T1↔T2 seam)."""
    return compose_gate_dispatch(judge_client, review_dispatch)


def _broken_composer(judge_client, review_dispatch):
    """A KNOWN-BROKEN promote-everything producer — the fail-closed gate INVERTED (QA-3 probe).

    Returns a RAW-VERDICT producer (ADR-0028-T1) that emits a clean ACCEPT judge + a passing review
    for EVERY plan REGARDLESS of the real review's findings — so when `compose_disposition` maps it,
    a plan surfaces PAST a non-True safety disposition, inverting the fail-closed gate. The
    self-test's safety-not-True leg must then surface ≥1 plan, breaking the inversion assertion →
    `_self_test()` returns non-zero (the audit→self-test exit-code chain goes RED). The broken spine
    lives in the PRODUCER (it ignores the findings the real producer would surface), never in
    `compose_disposition` (the one composition site stays correct) and never a production path.
    """
    def gate_producer(assembled_plan):
        return {
            "judge": {"verdict": quality_judge_mod.ACCEPT, "dimensions": {}, "deductions": []},
            "review": {"passed": True, "findings": [], "lenses": ()},
        }

    return gate_producer


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


# --- the RED-capability mutant (ADR-0028-T5): swallow the throw/replay sentinel ---


def _swallowing_memo_hook(kind, key_of, memo):
    """A MUTANT memo hook that SWALLOWS the replay sentinel (the throw/replay path REMOVED; QA mutant).

    Mirrors `plan_driver._memo_hook`, but on a cache MISS it returns a benign `None` instead of
    raising the `_ReplayNeeded` sentinel — so the byte-frozen engine NEVER unwinds the sentinel,
    `drive` NEVER catches it, and NO REAUTHOR / ADJUDICATOR request is ever yielded. Driving the
    replay legs through this mutant makes the ≥1-REAUTHOR / ≥1-ADJUDICATOR assertion go RED — the
    proof the assertion DEPENDS on the ADR-0028-T2 throw/replay path (it is NOT satisfiable by a
    driver that does not exercise it). A tests/CI hook only, never a production path.
    """
    def wrapper(*args):
        key = key_of(*args)
        if key in memo:
            return memo[key]
        return None

    return wrapper


@contextlib.contextmanager
def _replay_path(swallow):
    """Optionally swap `plan_driver._memo_hook` for the sentinel-SWALLOWING mutant around a leg drive.

    `swallow=False` (the default / production posture) leaves the REAL throw/replay path intact.
    `swallow=True` installs `_swallowing_memo_hook` (the RED-capability mutant) for the duration and
    RESTORES the real hook on exit — so the ≥1-yield assertion can be shown to go RED when the
    throw/replay path is removed. A loud WARNING fires while the mutant is active (mirrors the
    BROKEN_SPINE_ENV warning); it is a tests/CI hook only, never a production path.
    """
    if not swallow:
        yield
        return
    print(
        "a-prime self-test: WARNING: the replay-path SWALLOW mutant is active (tests/CI only — the "
        "throw/replay sentinel is swallowed, 0 REAUTHOR/ADJUDICATOR yields)"
    )
    real_memo_hook = plan_driver._memo_hook
    plan_driver._memo_hook = _swallowing_memo_hook
    try:
        yield
    finally:
        plan_driver._memo_hook = real_memo_hook


# --- the three replay legs (ADR-0028-T5): REAUTHOR + ADJUDICATOR throw/replay ----


def _drive_replay_leg(authors, kinds, *, label, reauthor=None, adjudicator=None, swallow_replay=False):
    """Drive `run_orchestrated` over `authors` with the given hooks + a clean kind-recording gate.

    The shared scaffold for the three replay legs (the recording legs differ only in their fixture +
    which hook(s) are wired): a fixture `_FixedDeidClient`, the kind-recording dispatch + clean
    composed gate (so the `kinds` list captures the yield order), a real temp store, and the
    `run_orchestrated` drive — optionally through the sentinel-SWALLOWING mutant (`swallow_replay`).
    `kinds` is mutated in place by the dispatch / gate / hooks (the caller reads it back). Returns the
    `run_orchestrated` result. Does NOT touch the accept / safety-not-True legs (their behavior is the
    EXISTING A′-inversion gates, untouched).

    Args:
        authors (dict): The fixture author set (domain -> envelope).
        kinds (list): The kind-recording accumulator (mutated in place by the dispatch / gate / hooks).
        label (str): The leg's scratch-dir stem.
        reauthor (Callable, optional): The energy-bounce re-author hook (`None` -> not wired).
        adjudicator (Callable, optional): The held-finding liaison hook (`None` -> not wired).
        swallow_replay (bool, optional): When True, install the sentinel-SWALLOWING mutant (the
            throw/replay path removed). Defaults to False (the real path).

    Returns:
        (dict) The `run_orchestrated` result.
    """
    global _LAST_DISPATCH
    deid_client = _FixedDeidClient(_deid_summary())
    dispatch = _kind_recording_dispatch(authors, kinds)
    _LAST_DISPATCH = dispatch.base
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / label
        store_read = _seed_store(root)
        gate = _kind_recording_gate(kinds)
        with _replay_path(swallow_replay):
            return run_orchestrated(
                _raw_intake(), deid_client, dispatch, store_read, root,
                plan_date=_PLAN_DATE, domains=("workout", "nutrition"),
                gate_dispatch=gate, reauthor=reauthor, adjudicator=adjudicator,
            )


def _run_reauthor_leg(*, swallow_replay=False):
    """Drive the REAUTHOR replay leg: a non-sustaining author set → a real energy bounce → replay.

    Drives the REAL `run_orchestrated` consumer over the NON-sustaining author set (workout over the
    nutrition energy ceiling, `energy_budget.sustains: False`) with a clean composed gate + a fixture
    `reauthor` hook. The energy bounce fires → the memo `reauthor` callable raises the sentinel on the
    cache-miss pass → `drive` yields a REAUTHOR request → the consumer re-authors a fuelable session →
    `drive` caches it + re-drives over a fresh scratch store → the replay surfaces the re-authored
    workout. Records the yielded `Request.kind` sequence in the consumer's fulfilment order (which IS
    the yield order — the consumer fulfils each yield synchronously). 0 live spend.

    Args:
        swallow_replay (bool, optional): When True, install the sentinel-SWALLOWING mutant (the
            RED-capability hook) so the throw/replay path is removed and 0 REAUTHOR is yielded — the
            non-tautology proof. Defaults to False (the real throw/replay path).

    Returns:
        (dict) The `run_orchestrated` result.
        (list) The yielded `Request.kind` sequence (AUTHOR / REAUTHOR / GATE, in fulfilment order).
        (list) The `reauthor` hook's recorded calls (one per cache-MISS dispatch).
    """
    kinds = []
    reauthor = _recording_reauthor(kinds)
    out = _drive_replay_leg(
        _non_sustaining_authors(), kinds, label="reauthor", reauthor=reauthor,
        swallow_replay=swallow_replay,
    )
    return out, kinds, reauthor.calls


def _run_adjudicator_leg(*, swallow_replay=False):
    """Drive the ADJUDICATOR replay leg: a held-finding author set → a real adjudication → replay.

    Drives the REAL `run_orchestrated` consumer over the held-finding author set (one domain declares
    a cross-domain conflict via `reconciliation.conflicts`) with a clean composed gate + a fixture
    `adjudicator` hook. The declaring domain enters `conflict_held` → the memo `adjudicator` callable
    raises the sentinel on the cache-miss pass → `drive` yields an ADJUDICATOR request → the consumer
    dispatches the liaison → `drive` caches it + re-drives → the content-valid override releases the
    hold and the pass surfaces. Records the yielded `Request.kind` sequence in fulfilment order. 0
    live spend.

    Args:
        swallow_replay (bool, optional): When True, install the sentinel-SWALLOWING mutant so the
            throw/replay path is removed and 0 ADJUDICATOR is yielded — the non-tautology proof.
            Defaults to False (the real throw/replay path).

    Returns:
        (dict) The `run_orchestrated` result.
        (list) The yielded `Request.kind` sequence (AUTHOR / ADJUDICATOR / GATE, in fulfilment order).
        (list) The `adjudicator` hook's recorded calls (one per cache-MISS dispatch).
    """
    kinds = []
    adjudicator = _recording_adjudicator(kinds)
    out = _drive_replay_leg(
        _held_finding_authors(), kinds, label="adjudicator", adjudicator=adjudicator,
        swallow_replay=swallow_replay,
    )
    return out, kinds, adjudicator.calls


def _run_sustaining_replay_leg():
    """Drive the sustaining author set through the SAME replay protocol (the non-tautology contrast).

    Drives `_sustaining_authors` (the existing clean fixture) with BOTH the `reauthor` AND the
    `adjudicator` hooks wired + a clean gate — the SAME typed-request protocol the two replay legs
    drive. The fixture sustains (no energy bounce) and declares no conflict (no held finding), so it
    yields 0 REAUTHOR + 0 ADJUDICATOR: the explicit CONTRAST (AR-002) that proves the replay legs'
    >=1 yields come from the FIXTURE, not from the protocol always yielding them (0 vs >=1, same
    driver, same hooks wired). 0 live spend.

    Returns:
        (dict) The `run_orchestrated` result.
        (list) The yielded `Request.kind` sequence (AUTHOR / GATE only — no REAUTHOR / ADJUDICATOR).
    """
    kinds = []
    out = _drive_replay_leg(
        _sustaining_authors(), kinds, label="sustaining",
        reauthor=_recording_reauthor(kinds), adjudicator=_recording_adjudicator(kinds),
    )
    return out, kinds


def _self_test(composer_factory=None):
    """Run the A′-inversion self-test; return 0 iff ALL FOUR inversion legs hold, else non-zero.

    The behavioral core-capability gate (PF-S63-02, NON-TAUTOLOGICAL) — four inversion legs, each
    returning non-zero (and printing the failing leg) on a break:
      (a) PROMOTION-ON-ACCEPT: the accept leg promotes ≥1 plan on the real composer's accept
          disposition;
      (b) 0-PLANS-ON-SAFETY-NOT-TRUE: the safety-not-True leg surfaces 0 plans past the real
          composer's fail-closed (not-True) disposition;
      (c) REAUTHOR REPLAY (ADR-0028-T5): the non-sustaining-author leg drives a REAL energy bounce →
          ≥1 REAUTHOR throw/replay yield and completes (a tautological self-test would assert the
          replay leg "ran" without proving the replay path is exercised);
      (d) ADJUDICATOR REPLAY (ADR-0028-T5): the held-finding leg drives a REAL cross-domain-conflict
          hold → ≥1 ADJUDICATOR throw/replay yield and completes.
    Returns 0 only when ALL FOUR hold; non-zero when any inversion breaks (the print is advisory, the
    exit code is the load-bearing failure signal, QA-3 — the audit consumes ONLY the exit code).

    Args:
        composer_factory (Callable, optional): The `(judge_client, review_dispatch) -> gate_dispatch`
            composer factory for legs (a)/(b). Defaults to the REAL `compose_gate_dispatch` — or the
            broken promote-everything composer when `A_PRIME_SELF_TEST_BROKEN_SPINE` is set (the QA-3
            exit-code-chain hook; a loud WARNING fires, it is a tests/CI hook, never production). The
            replay legs (c)/(d) always drive the REAL clean composed gate (the inversion they test is
            the THROW/REPLAY path, not the composer).

    Returns:
        (int) 0 when all four inversions hold; non-zero when any breaks.
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

    # The SWALLOW_REPLAY_ENV test hook removes the throw/replay path for legs (c)/(d) (a loud WARNING
    # fires inside `_replay_path`) so the audit→self-test chain can be driven RED on a broken replay
    # path, mirroring the BROKEN_SPINE_ENV arm. Default (unset) → the real throw/replay path.
    swallow_replay = bool(os.environ.get(SWALLOW_REPLAY_ENV))

    # (c) REAUTHOR REPLAY: the non-sustaining-author leg must yield ≥1 REAUTHOR and complete (a
    # tautological pass would not EXERCISE the throw/replay path — the AR-002 non-tautology floor).
    out_reauthor, reauthor_kinds, _ = _run_reauthor_leg(swallow_replay=swallow_replay)
    if reauthor_kinds.count(plan_driver.REAUTHOR) < 1:
        print(
            "a-prime self-test FAIL: the non-sustaining leg yielded 0 REAUTHOR "
            "(the energy-bounce throw/replay path is not exercised — the PF-S63-02 tautology)"
        )
        return 1
    if "results" not in out_reauthor:
        print("a-prime self-test FAIL: the REAUTHOR replay leg did not complete to a terminal result")
        return 1

    # (d) ADJUDICATOR REPLAY: the held-finding leg must yield ≥1 ADJUDICATOR and complete.
    out_adjudicator, adjudicator_kinds, _ = _run_adjudicator_leg(swallow_replay=swallow_replay)
    if adjudicator_kinds.count(plan_driver.ADJUDICATOR) < 1:
        print(
            "a-prime self-test FAIL: the held-finding leg yielded 0 ADJUDICATOR "
            "(the held-finding throw/replay path is not exercised — the PF-S63-02 tautology)"
        )
        return 1
    if "results" not in out_adjudicator:
        print("a-prime self-test FAIL: the ADJUDICATOR replay leg did not complete to a terminal result")
        return 1

    print(
        "a-prime self-test PASS: promotion-on-accept + 0-plans-on-safety-not-True + "
        "≥1-REAUTHOR-replay + ≥1-ADJUDICATOR-replay "
        "(de-id -> driver -> real composer -> throw/replay -> promote -> render, the A′ spine wired)"
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
