"""Tests for the ADR-0044-T3 re-base of the ADR-0038 horizon composition.

``scripts.plan.horizons.window_block`` (and the ``read_horizons`` ``today`` slot,
and the transitive ``assess_pace``) re-base off the FLAT ``plan::<domain>`` dated
history onto the comprehensive periodization: when a comprehensive plan STANDS for
the render date and covers the domain, the window reads that plan's first-class
dated ``prescription.blocks`` (via ``plan_model.read_standing_plan``, comprehensive-
wins); a pre-migration thin-only store keeps the retained flat range-query (0
crashes, byte-behavior-identical). See ``docs/task-plan/adr-0044-t3.md``.

Everything here is SYNTHETIC — scratch ``tmp_path`` stores, 0 live-API, 0 real
operator PII (AC-4). The comprehensive prescription (``{"blocks":[...]}``) vs the
thin plan (``{"exercises":[...]}``) is the distinguishing signal that makes AC-1 /
AC-2 non-tautological: a revert of the re-base (drop the comprehensive-first
branch) turns the comprehensive-periodization assertions RED (PF-S130-01).

The comprehensive-fixture builders (``_training_program`` / ``_compound_program`` /
``_comprehensive_version``) MIRROR the proven shapes in
``tests/store/test_plan_model.py`` (PF-S131-01 — the canonical periodized
``{"prescription": {"blocks": [{"date","phase","detail"}]}}``); the thin
``_workout_plan`` / ``_enriched_workout_plan`` / ``_goal`` mirror
``tests/plan/test_horizons.py``. ``tests`` is not an importable package, so the
proven shapes are reproduced here rather than cross-imported.
"""

from pathlib import Path

from scripts.plan import horizons
from scripts.store import goal_schema, plan_model, plan_schema, store


# --------------------------------------------------------------------------- #
# Mirrored comprehensive-fixture builders (tests/store/test_plan_model.py).
# --------------------------------------------------------------------------- #


def _training_program(**over):
    """A conformant seven-field training DOMAIN PROGRAM (domain_program.validate)."""
    program = {
        "domain_kind": "training",
        "prescription": {
            "blocks": [
                {"date": "2026-07-13", "phase": "hypertrophy", "detail": "upper/lower x4"},
                {"date": "2026-07-20", "phase": "hypertrophy-2", "detail": "add a top set"},
            ]
        },
        "rationale": {
            "claims": [
                {"claim": "volume drives growth", "certainty": "moderate",
                 "strength": "strong", "causal": True}
            ]
        },
        "monitoring_signals": [{"validity_tier": "high", "signal": "e1RM"}],
        "adjustment_rules": [{"trigger": "rpe>9 two sessions", "action": "deload 10%"}],
        "required_labs": [],
        "refusal_escalation": {},
        "cross_domain_seams": [],
    }
    program.update(over)
    return program


def _compound_program(**over):
    """A conformant seven-field compound DOMAIN PROGRAM (required_labs non-empty)."""
    program = {
        "domain_kind": "compound",
        "prescription": {
            "blocks": [
                {"date": "2026-07-13", "phase": "cycle-wk1", "detail": "250mcg AM"},
                {"date": "2026-07-27", "phase": "cycle-wk3", "detail": "titrate to response"},
            ]
        },
        "rationale": {
            "claims": [
                {"claim": "supports connective-tissue recovery", "certainty": "low",
                 "strength": "weak", "causal": False}
            ]
        },
        "monitoring_signals": [{"validity_tier": "moderate", "signal": "injection-site"}],
        "adjustment_rules": [{"trigger": "site reaction", "action": "hold + reassess"}],
        "required_labs": ["IGF-1", "fasting glucose"],
        "refusal_escalation": {},
        "cross_domain_seams": [],
    }
    program.update(over)
    return program


def _comprehensive_version(
    *, date="2026-07-13", narrative="Integrated 12-week block: train hard, recover, monitor.",
    programs=None, milestones=None, monitoring_config=None, adjustment_rules=None,
):
    """Build ONE composite plan version spanning >=1 active domain."""
    return {
        "date": date,
        "domain_programs": programs if programs is not None else {
            "workout": _training_program(),
            "peptides": _compound_program(),
        },
        "narrative": narrative,
        "milestones": milestones if milestones is not None else [
            {"date": "2026-08-10", "label": "first re-test", "metric": "e1RM +5%"},
            {"date": "2026-09-14", "label": "mid-block panel", "metric": "IGF-1 in range"},
        ],
        "monitoring_config": monitoring_config if monitoring_config is not None else {
            "panels": ["IGF-1", "lipids"], "cadence_days": 30,
        },
        "adjustment_rules": adjustment_rules if adjustment_rules is not None else [
            {"trigger": "2 missed sessions", "action": "re-scope the week"},
        ],
    }


# --------------------------------------------------------------------------- #
# Mirrored thin-side builders (tests/plan/test_horizons.py).
# --------------------------------------------------------------------------- #


def _goal(label="Bench 1RM", baseline=225, current=250, target=275, unit="lb"):
    """A minimal valid goal document (an increase goal at 50% by default)."""
    return {
        "label": label,
        "baseline": baseline,
        "current": current,
        "target": target,
        "unit": unit,
    }


def _workout_plan():
    """A minimal valid FLAT workout plan document (the thin decoy shape)."""
    return {"exercises": [{"name": "Squat", "sets": 3}]}


def _enriched_workout_plan(week_intent, week_expectation=None):
    """A flat workout plan carrying the horizon week-framing extras (the thin decoy)."""
    plan = _workout_plan()
    plan["week_intent"] = week_intent
    if week_expectation is not None:
        plan["week_expectation"] = week_expectation
    return plan


# --------------------------------------------------------------------------- #
# AC-1 — horizon re-base onto the comprehensive periodization (PF-S130-01).
# --------------------------------------------------------------------------- #


def test_window_block_reads_comprehensive_periodization(tmp_path):
    """A comprehensive plan drives the window; a coexisting flat DECOY is NOT read.

    Non-tautological (PF-S130-01): the comprehensive in-window block (07-13, phase
    "hypertrophy") gives a DIFFERENT answer than the coexisting flat plan::workout
    decoy dated 07-10. Reverting the re-base returns the 07-10 decoy -> RED.
    """
    on_date = "2026-07-13"
    plan_model.record_plan_version(_comprehensive_version(date=on_date), tmp_path)
    # Coexisting flat plan::workout DECOY dated in-window on a DIFFERENT date.
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("flat decoy"), "2026-07-10", "coach", tmp_path
    )

    block = horizons.window_block("workout", tmp_path, on_date, horizons.WEEK_SPAN_DAYS)
    assert block is not None
    # The comprehensive block's date, NOT the 07-10 flat decoy's date.
    assert block["plan_date"] == "2026-07-13"
    # A comprehensive-block framing key the flat decoy does not carry.
    assert block["extras"].get("phase") == "hypertrophy"

    # read_horizons composes the same comprehensive periodization into the week slot.
    goal_schema.record_goal("bench", _goal(), "2026-07-01", tmp_path)
    view = horizons.read_horizons("workout", "bench", tmp_path, on_date)
    assert view["week"]["plan_date"] == "2026-07-13"


def test_window_block_comprehensive_no_flat_history_needed(tmp_path):
    """A comprehensive-only store (NO flat reading) still yields the periodization block.

    The "0 reads of the retired flat plan::<domain> history" falsifier: the answer
    does not depend on the flat stream. Reverting the re-base falls to the empty
    flat range-query -> None -> RED.
    """
    on_date = "2026-07-13"
    plan_model.record_plan_version(_comprehensive_version(date=on_date), tmp_path)
    assert store.read("plan::workout", root=tmp_path) == []  # no flat history at all

    block = horizons.window_block("workout", tmp_path, on_date, horizons.WEEK_SPAN_DAYS)
    assert block is not None
    assert block["plan_date"] == "2026-07-13"


# --------------------------------------------------------------------------- #
# AC-2 — window membership preserved over the comprehensive blocks.
# --------------------------------------------------------------------------- #


def test_window_block_block_membership_preserved(tmp_path):
    """The boundary-inclusive _in_window predicate carries over to block dates.

    on_date 2026-07-13: week window [07-07, 07-13]; month window [06-14, 07-13].
    In-window kept + latest-wins; a block that is in-month-but-out-of-week is
    dropped by the week window and admitted by the month window; all-out-of-week
    -> None; the far edge (07-07) is inclusive.
    """
    on_date = "2026-07-13"

    def _version(root, block_dates):
        blocks = [{"date": d, "phase": "p", "week_intent": d} for d in block_dates]
        plan_model.record_plan_version(
            _comprehensive_version(
                date=on_date,
                programs={"workout": _training_program(prescription={"blocks": blocks})},
            ),
            root,
        )

    # (i) in-week block kept (latest-wins); the 06-20 block is out of the week window.
    root_i = tmp_path / "in-and-out"
    _version(root_i, ["2026-07-13", "2026-06-20"])
    week = horizons.window_block("workout", root_i, on_date, horizons.WEEK_SPAN_DAYS)
    assert week is not None and week["plan_date"] == "2026-07-13"

    # (ii) a version whose ONLY block is in-month-but-out-of-week: week None, month admits it.
    root_ii = tmp_path / "month-only"
    _version(root_ii, ["2026-06-20"])
    assert horizons.window_block("workout", root_ii, on_date, horizons.WEEK_SPAN_DAYS) is None
    month = horizons.window_block("workout", root_ii, on_date, horizons.MONTH_SPAN_DAYS)
    assert month is not None and month["plan_date"] == "2026-06-20"

    # (iii) ALL blocks out of the week window (one day before the far edge) -> None.
    root_iii = tmp_path / "all-out"
    _version(root_iii, ["2026-07-06"])  # 07-07 is the window start; 07-06 is out
    assert horizons.window_block("workout", root_iii, on_date, horizons.WEEK_SPAN_DAYS) is None

    # (iv) the far edge (07-07) is boundary-inclusive.
    root_edge = tmp_path / "edge-in"
    _version(root_edge, ["2026-07-07"])
    edge = horizons.window_block("workout", root_edge, on_date, horizons.WEEK_SPAN_DAYS)
    assert edge is not None and edge["plan_date"] == "2026-07-07"


# --------------------------------------------------------------------------- #
# AC-3 — thin-only pre-migration back-compat via the mixed-history reader.
# --------------------------------------------------------------------------- #


def test_window_block_thin_only_backcompat(tmp_path):
    """A thin-only store keeps the flat range-query behavior byte-identical (0 crashes).

    Two in-window thin readings -> the LATEST-in-window block (the retained flat
    range-query); a thin store with no in-window plan -> None.
    """
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("early"), "2026-07-08", "coach", tmp_path
    )
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("late"), "2026-07-11", "coach", tmp_path
    )
    # Both inside the 7-day window [07-07, 07-13]; the later wins (identical to today).
    block = horizons.window_block("workout", tmp_path, "2026-07-13", horizons.WEEK_SPAN_DAYS)
    assert block is not None
    assert block["plan_date"] == "2026-07-11"
    assert block["extras"]["week_intent"] == "late"
    # No in-window plan for a later render date -> None.
    assert horizons.window_block("workout", tmp_path, "2026-08-01", horizons.WEEK_SPAN_DAYS) is None


def test_read_horizons_thin_only_no_crash(tmp_path):
    """read_horizons over a thin-only store returns all four slots without raising."""
    goal_schema.record_goal("bench", _goal(), "2026-07-01", tmp_path)
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("wk"), "2026-07-10", "coach", tmp_path
    )
    view = horizons.read_horizons("workout", "bench", tmp_path, "2026-07-13")
    assert set(view) == {"today", "week", "month", "milestone"}
    # The week/month slots resolve via the retained flat range-query.
    assert view["week"]["plan_date"] == "2026-07-10"
    assert view["month"]["plan_date"] == "2026-07-10"


# --------------------------------------------------------------------------- #
# AC-3b — read_horizons today re-sources to the comprehensive-wins reader.
# --------------------------------------------------------------------------- #


def test_read_horizons_today_comprehensive_wins(tmp_path):
    """A comprehensive plan standing for the render date surfaces as today's action.

    Reverting the today re-source (read plan_schema.read_plan) over a
    comprehensive-only store returns NO_PLAN -> RED.
    """
    on_date = "2026-07-13"
    plan_model.record_plan_version(_comprehensive_version(date=on_date), tmp_path)
    goal_schema.record_goal("bench", _goal(), "2026-07-01", tmp_path)

    view = horizons.read_horizons("workout", "bench", tmp_path, on_date)
    assert view["today"]["state"] is None  # standing, not a thin NO_PLAN
    assert "blocks" in view["today"]["plan"]  # the comprehensive prescription


# --------------------------------------------------------------------------- #
# AC-3c — assess_pace re-sources transitively through window_block (spec :260).
# --------------------------------------------------------------------------- #


def test_assess_pace_comprehensive_branch_returns_verdict(tmp_path):
    """assess_pace returns a verdict (not None) for a comprehensive week_expectation block.

    Pins the transitive re-source (Deviation #3): a comprehensive in-window block
    carrying a numeric week_expectation must surface it in window_block's extras so
    assess_pace returns a CLASSIFICATIONS member. A silent key-drop, or the
    Step-2.5 comprehensive-first revert (block None over the comprehensive-only
    store), returns None -> RED.
    """
    on_date = "2026-07-13"
    programs = {"workout": _training_program(prescription={"blocks": [
        {"date": on_date, "phase": "cut", "week_intent": "deficit", "week_expectation": -0.4},
    ]})}
    plan_model.record_plan_version(
        _comprehensive_version(date=on_date, programs=programs), tmp_path
    )
    # Two goal snapshots (distinct dates, changing current) so actual_weekly_rate is non-None.
    goal = _goal(label="Weight", baseline=100, current=100, target=90, unit="kg")
    goal_schema.record_goal("weight", goal, "2026-07-01", tmp_path)
    goal_schema.record_goal("weight", {**goal, "current": 99}, on_date, tmp_path)

    verdict = horizons.assess_pace("workout", "weight", tmp_path, on_date)
    assert verdict in horizons.CLASSIFICATIONS  # a verdict, NOT None


# --------------------------------------------------------------------------- #
# AC-D1 — growth-tolerant over the co-wave PLAN_DOMAINS growth (RULING D1).
# --------------------------------------------------------------------------- #


def test_horizons_growth_tolerant_over_grown_roster(tmp_path, monkeypatch):
    """A grown-roster domain with no comprehensive periodization contributes nothing.

    0043-T3 grows plan_schema.PLAN_DOMAINS (the constant domain_horizons iterates);
    TRACKED_DOMAINS stays the three. A grown member (``sleep``) with no plan
    resolves absent/None -- never a crash. RED-capable: an impl that indexed the
    standing version's domain_programs[domain] without the coverage guard KeyErrors
    on the uncovered sleep.
    """
    monkeypatch.setattr(plan_schema, "PLAN_DOMAINS", plan_schema.PLAN_DOMAINS + ("sleep",))
    on_date = "2026-07-13"
    programs = {
        "workout": _training_program(),
        "nutrition": _training_program(),
        "supplements": _compound_program(),
        "peptides": _compound_program(),
    }
    plan_model.record_plan_version(
        _comprehensive_version(date=on_date, programs=programs), tmp_path
    )
    goal_schema.record_goal("bench", _goal(), "2026-07-01", tmp_path)

    # sleep: a grown member with NO comprehensive periodization and NO thin plan.
    assert horizons.window_block("sleep", tmp_path, on_date, horizons.WEEK_SPAN_DAYS) is None
    view = horizons.read_horizons("sleep", "bench", tmp_path, on_date)
    assert set(view) == {"today", "week", "month", "milestone"}
    assert view["today"]["state"] in (plan_schema.NO_PLAN, plan_schema.NO_PLAN_TODAY)
    assert view["week"] is None and view["month"] is None
    # domain_horizons does not raise over the grown roster and surfaces no sleep horizon.
    domains = [h["domain"] for h in horizons.domain_horizons(tmp_path, on_date)]
    assert "sleep" not in domains


# --------------------------------------------------------------------------- #
# AC-4 — 0 real operator PII in the test tree.
# --------------------------------------------------------------------------- #


def test_no_operator_identity_literal_in_test_tree():
    source = Path(__file__).read_text(encoding="utf-8").lower()
    # Assembled from splits so the guard's own token list never self-matches.
    forbidden = ["".join(parts) for parts in (
        ("wal", "ter"), ("mcgiv", "ney"), ("wmcgiv", "ney"), ("@", "gmail"),
    )]
    for token in forbidden:
        assert token not in source, "a real operator-identity literal leaked into the test tree"
