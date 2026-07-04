"""Tests for scripts/plan/horizons.py — the ADR-0038 horizon read-layer.

A pure read/query composition over the goal / calendar / plan store schemas: it
delegates milestone progress to ``goal_schema.resolve_goal`` (the single progress
site — this layer computes no percent), the next dated cadence to
``calendar_schema``, and gates per-domain tracking horizons on
``plan_schema.TRACKED_DOMAINS`` (``peptides`` is untracked). This suite asserts
the delegated-percent equality plus the single-progress-site source guard (AC-1),
the next-cadence selection (AC-2), the peptides-untracked gate (AC-3), the
open-ended rolling degradation with no fabricated target-date (AC-4), and the
no-new-store-stream invariant — the read writes nothing (AC-5).
"""

from pathlib import Path

from scripts.plan import horizons
from scripts.store import calendar_schema, goal_schema, plan_schema, store

_HORIZONS_SRC = Path(__file__).resolve().parents[2] / "scripts" / "plan" / "horizons.py"


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
    """A minimal valid workout plan document."""
    return {"exercises": [{"name": "Squat", "sets": 3}]}


def _peptides_plan():
    """A minimal valid peptides plan document."""
    return {"compound": "BPC-157", "dose": "250mcg", "route": "SubQ"}


# --- AC-1: single-source milestone progress (delegated to goal_schema) ---


def test_horizons_milestone_percent_equals_goal_schema(tmp_path):
    """The horizon milestone percent EQUALS goal_schema._percent exactly.

    The horizon layer never re-derives progress — it carries goal_schema's
    read-derived percent unchanged (the single progress site).
    """
    goal_schema.record_goal("bench", _goal(current=250), "2026-06-10", tmp_path)
    horizon = horizons.read_horizon("bench", tmp_path)
    assert horizon["milestone"]["percent"] == goal_schema._percent(225, 250, 275)
    # The whole milestone sub-dict is goal_schema's resolved goal, unaltered —
    # no fabricated field can hide in it.
    assert horizon["milestone"] == goal_schema.read_goal("bench", tmp_path)


def test_horizons_single_progress_site(tmp_path):
    """No second progress site: horizons.py delegates, never re-derives percent.

    Source guard — the module names no ``_percent`` (so it cannot be a second
    caller) and reaches milestone progress only through ``goal_schema``. Mutation
    check: re-implementing the percent arithmetic in horizons.py turns this RED.
    """
    src = _HORIZONS_SRC.read_text()
    assert "_percent" not in src
    assert "goal_schema" in src


def test_horizons_milestone_absent_reads_none(tmp_path):
    """A goal with no stored snapshot resolves to None (honest absence)."""
    assert horizons.read_horizon("never-seeded", tmp_path) is None


# --- AC-2: next dated cadence (delegated to calendar_schema) ---


def test_horizons_next_cadence_from_calendar_events(tmp_path):
    """The earliest event on/after the render date surfaces as the next cadence.

    Mutation check: dropping the on/after filter (returning the earliest event
    regardless of date) turns the render-date cases below RED.
    """
    calendar_schema.record_event("lab-draw", "Fasting panel", "2026-06-20", tmp_path)
    calendar_schema.record_event("check-in", "Coach call", "2026-06-15", tmp_path)
    assert horizons.next_cadence(tmp_path, "2026-06-10") == {
        "category": "check-in",
        "label": "Coach call",
        "date": "2026-06-15",
    }
    # Past the check-in, the lab-draw is next:
    assert horizons.next_cadence(tmp_path, "2026-06-16") == {
        "category": "lab-draw",
        "label": "Fasting panel",
        "date": "2026-06-20",
    }
    # An event dated exactly on the render date is on/after (inclusive):
    assert horizons.next_cadence(tmp_path, "2026-06-15")["date"] == "2026-06-15"


def test_horizons_next_cadence_absent_reads_none(tmp_path):
    """No event on/after the render date is honest absence, never an invented cadence."""
    calendar_schema.record_event("training", "Lower body", "2026-06-10", tmp_path)
    assert horizons.next_cadence(tmp_path, "2026-06-11") is None


# --- AC-3 (Risk): peptides untracked — no cadence, no plan-track horizon ---


def test_horizons_peptides_untracked(tmp_path):
    """A plan::peptides document yields 0 peptide cadences / tracking horizons.

    Peptides is a plan domain but NOT a tracked one (it rides the watch-out
    stream). Mutation check: gating on PLAN_DOMAINS instead of TRACKED_DOMAINS
    (or hard-coding the tracked set to include peptides) turns this RED.
    """
    plan_schema.record_plan("peptides", _peptides_plan(), "2026-06-10", "pep-doc", tmp_path)
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-10", "coach", tmp_path)
    domains = [h["domain"] for h in horizons.domain_horizons(tmp_path, "2026-06-10")]
    assert "peptides" not in domains
    assert domains.count("peptides") == 0
    # A tracked domain with a plan still surfaces (the gate is not a blanket drop):
    assert "workout" in domains


# --- Tier-3 review (HIGH): NO_PLAN_TODAY is skipped, never crashes ---


def test_horizons_no_plan_today_absent_no_crash(tmp_path):
    """A plan dated D1 read at D2 (a stale plan) yields NO tracking horizon, no crash.

    ``resolve_plan`` returns ``NO_PLAN_TODAY`` (plan=None) for a domain whose
    latest plan is not dated the render date. ``domain_horizons`` must skip it
    alongside ``NO_PLAN`` — surfacing a stale plan_date misleads the ADR-0038-T3
    classifier. Mutation check: guarding only on ``NO_PLAN`` (the pre-fix code)
    raises ``TypeError`` inside ``plan_extras(None)`` — this test reds.
    """
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-10", "coach", tmp_path)
    # Read the render date TEN days after the recorded plan -> NO_PLAN_TODAY:
    view = horizons.domain_horizons(tmp_path, "2026-06-20")
    assert [h["domain"] for h in view] == []
    # A same-date plan still surfaces (the skip is not a blanket drop):
    same_date = horizons.domain_horizons(tmp_path, "2026-06-10")
    assert [h["domain"] for h in same_date] == ["workout"]


# --- AC-4 (Risk): open-ended goal degrades to rolling cycles, no fabricated date ---


def test_horizons_open_ended_goal_degrades(tmp_path):
    """A deadline-less goal keeps an honest percent and fabricates no target-date.

    The horizon degrades to rolling maintenance cycles (mode "rolling") and emits
    no synthesized target-date. Mutation check: projecting a completion date from
    the progress rate (a fabricated target_date) turns this RED.
    """
    goal_schema.record_goal("fat", _goal(label="Body fat", baseline=18, current=15,
                                         target=12, unit="%"), "2026-06-10", tmp_path)
    horizon = horizons.read_horizon("fat", tmp_path)
    # Honest percent, still single-sourced through goal_schema:
    assert horizon["milestone"]["percent"] == goal_schema._percent(18, 15, 12)
    assert horizon["mode"] == "rolling"
    assert horizon["target_date"] is None
    # No fabricated target-date can hide under another key: the horizon carries
    # exactly these keys, and the milestone sub-dict is goal_schema's resolved goal.
    assert set(horizon) == {"label", "milestone", "mode", "target_date"}


# --- AC-5 (Risk): the read writes no new store stream ---


def test_horizons_writes_no_new_store_stream(tmp_path):
    """Every horizon read is pure: 0 new item ids, 0 store.append.

    Mutation check: writing a plan-arc:: / horizon:: / periodization:: stream (or
    any store.append) turns this RED — the items set would grow past the seeded
    goal:: / calendar::events / plan:: streams.
    """
    goal_schema.record_goal("bench", _goal(), "2026-06-10", tmp_path)
    calendar_schema.record_event("lab-draw", "Fasting panel", "2026-06-20", tmp_path)
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-10", "coach", tmp_path)
    before = set(store.items(tmp_path))

    horizons.read_horizon("bench", tmp_path)
    horizons.next_cadence(tmp_path, "2026-06-10")
    horizons.domain_horizons(tmp_path, "2026-06-10")

    after = set(store.items(tmp_path))
    assert after == before
    assert after == {"goal::bench", "calendar::events", "plan::workout"}
    # Source guard: the read defines no new ::-prefixed stream and never calls
    # the store write primitive (the behavioral before==after check above is the
    # primary proof; this guards the write path in source too).
    src = _HORIZONS_SRC.read_text()
    assert "store.append" not in src
    assert "store.correct" not in src
    for forbidden in ("plan-arc::", "horizon::", "periodization::"):
        assert forbidden not in src
    # Egress guard (Architect breaks-if): the frozen-glob carve-out's behavioral
    # guard also covers model-send / network-egress — the read layer names no
    # author/de-id/model-send symbol and no network transport. Mutation check:
    # adding a `converse`/`requests`/`socket` call to horizons.py reds this.
    for egress in ("converse", "author", "deidentify", "deid_in",
                   "client.", "requests", "urllib", "socket", "ModelClient"):
        assert egress not in src, f"horizons.py names an egress symbol {egress!r}"


# --- ADR-0038-T2 Cycle 1: enrichment convention rides the D2 open-on-extras seam ---


def test_horizon_extras_enriched_plan_validates(tmp_path):
    """A plan::<domain> value carrying the horizon extras validates (AC-1).

    The three-key horizon-extra convention rides the ADR-0010 D2 open-on-extras
    seam — the keys are permitted by omission from every domain's required/optional
    dict, so record_plan raises nothing and the read-back carries them unaltered.
    """
    plan = _workout_plan()
    phase_key, intent_key, expect_key = horizons.HORIZON_EXTRAS
    plan[phase_key] = "accumulation"
    plan[intent_key] = "build base volume"
    plan[expect_key] = "3 sessions this week"
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert resolved["state"] is None
    assert resolved["plan"][intent_key] == "build base volume"


def test_horizon_flat_plan_still_validates(tmp_path):
    """A flat plan::<domain> value WITHOUT the extras still validates (AC-2).

    The graceful floor: enrichment is optional, so a plan carrying none of the
    horizon-extra keys validates through record_plan exactly as before.
    """
    plan = _workout_plan()
    assert not any(key in plan for key in horizons.HORIZON_EXTRAS)
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert resolved["state"] is None
    assert resolved["plan"] == plan


def test_horizon_typo_extra_ignored(tmp_path):
    """A typo'd horizon key still validates and is not a recognized extra (AC-5).

    The standing D2 tradeoff: an unknown extra (``weak_intent``) is permitted and
    ignored, never rejected — it is absent from the horizon-extra convention.
    """
    plan = _workout_plan()
    plan["weak_intent"] = "typo, not a real horizon key"
    assert "weak_intent" not in horizons.HORIZON_EXTRAS
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert resolved["state"] is None


# --- ADR-0038-T2 Cycle 2: read the extras back into the horizon view ---


def test_horizon_extras_read_back(tmp_path):
    """The read-back accessor surfaces the horizon extras off a resolved plan (AC-4).

    Given a resolved plan::<domain> value, ``plan_extras`` returns exactly the
    horizon-extra keys present — the read-back the week/month framing consumes.
    An unknown key (the typo) is not a horizon extra, so it is not surfaced.
    """
    plan = _workout_plan()
    plan["phase"] = "accumulation"
    plan["week_intent"] = "build base volume"
    plan["weak_intent"] = "typo — not a horizon extra"
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    extras = horizons.plan_extras(resolved["plan"])
    assert extras == {"phase": "accumulation", "week_intent": "build base volume"}


def test_horizon_extras_surface_in_domain_view(tmp_path):
    """A seeded enriched plan surfaces its week_intent in the horizon view (AC-4).

    The domain-horizon composition reads the extras off the resolved plan value
    (the T1 read layer, no new store read) into an ``extras`` framing key.
    """
    plan = _workout_plan()
    plan["week_intent"] = "build base volume"
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    view = horizons.domain_horizons(tmp_path, "2026-06-10")
    workout = next(h for h in view if h["domain"] == "workout")
    assert workout["extras"]["week_intent"] == "build base volume"


def test_horizon_extras_flat_plan_empty(tmp_path):
    """A resolved plan with no extras yields an empty framing, never a raise (AC-2 floor).

    The graceful floor consistent with the flat-plan validation: the read-back
    tolerates a plan carrying no horizon-extra keys.
    """
    plan = _workout_plan()
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    resolved = plan_schema.read_plan("workout", "2026-06-10", tmp_path)
    assert horizons.plan_extras(resolved["plan"]) == {}
    view = horizons.domain_horizons(tmp_path, "2026-06-10")
    workout = next(h for h in view if h["domain"] == "workout")
    assert workout["extras"] == {}


# --- ADR-0038-T3 Cycle 1: date-range week/month query + today-by-date-equality ---


def _enriched_workout_plan(week_intent, week_expectation=None):
    """A workout plan carrying the horizon week-framing extras."""
    plan = _workout_plan()
    plan["week_intent"] = week_intent
    if week_expectation is not None:
        plan["week_expectation"] = week_expectation
    return plan


def test_four_horizon_composition(tmp_path):
    """AC-1: one render date yields today/week/month/milestone from one store.

    Today's action is the date-equality plan, the week block and month arc are
    the latest-in-window plans, the milestone is the goal's derived percent — all
    from the seeded streams. Mutation check: a store scan after the read finds no
    ``plan-arc::``/``horizon::``/``periodization::`` stream (0 new store keys).
    """
    goal_schema.record_goal("bench", _goal(current=250), "2026-06-10", tmp_path)
    plan = _enriched_workout_plan("build base volume")
    plan_schema.record_plan("workout", plan, "2026-06-10", "coach", tmp_path)
    view = horizons.read_horizons("workout", "bench", tmp_path, "2026-06-10")
    # Today's action: the render-date plan via date equality.
    assert view["today"]["state"] is None
    assert view["today"]["plan"] == plan
    # This-week block + month arc: the same plan is in both trailing windows.
    assert view["week"]["plan_date"] == "2026-06-10"
    assert view["week"]["extras"]["week_intent"] == "build base volume"
    assert view["month"]["plan_date"] == "2026-06-10"
    # Milestone: the goal's derived percent, single-sourced through goal_schema.
    assert view["milestone"]["milestone"]["percent"] == goal_schema._percent(225, 250, 275)
    # 0 new store streams — only the seeded goal:: and plan:: items exist.
    items = set(store.items(tmp_path))
    assert items == {"goal::bench", "plan::workout"}
    for forbidden in ("plan-arc::", "horizon::", "periodization::"):
        assert not any(item.startswith(forbidden) for item in items)


def test_latest_in_window_selection(tmp_path):
    """AC-2 (Risk RT-09): two same-window dated plans select the latest as the block.

    The ADR-0036 loop day-keys a new dated ``plan::<domain>`` on every trigger, so
    multiple dated plans fall in one week window. The range query selects the
    later-dated reading (max timepoint). Mutation check: selecting the earliest (or
    any non-max) in-window reading turns this RED.
    """
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("early week"), "2026-06-05", "coach", tmp_path
    )
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("late week"), "2026-06-08", "coach", tmp_path
    )
    view = horizons.read_horizons("workout", "bench", tmp_path, "2026-06-10")
    # Both plans are inside the 7-day trailing window [06-04, 06-10]; the later wins.
    assert view["week"]["plan_date"] == "2026-06-08"
    assert view["week"]["extras"]["week_intent"] == "late week"


def test_window_boundary_inclusive(tmp_path):
    """AC-2 boundary (OQ-2): the trailing window is inclusive of its far edge.

    The week window is the 7 dates ending on (and including) the render date:
    [render - 6, render]. A plan dated exactly render-6 is in-window; the same plan
    read one day later (render-7) falls out and the block is absent. Pins the
    boundary as a binary the test reads.
    """
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("edge"), "2026-06-04", "coach", tmp_path
    )
    # render 06-10: window [06-04, 06-10] — the plan sits on the far edge, in-window.
    edge_in = horizons.read_horizons("workout", "bench", tmp_path, "2026-06-10")
    assert edge_in["week"]["plan_date"] == "2026-06-04"
    # render 06-11: window [06-05, 06-11] — the plan is now one day out, no block.
    edge_out = horizons.read_horizons("workout", "bench", tmp_path, "2026-06-11")
    assert edge_out["week"] is None


def test_today_by_date_equality(tmp_path):
    """AC-3 (Risk): the today slot resolves by strict date equality, never nearest.

    With a plan dated yesterday and a plan dated the render date, the today slot
    returns the render-date plan. With NO render-date plan, it reads
    ``NO_PLAN_TODAY`` — never the yesterday plan. Mutation check: resolving today
    to the nearest in-window reading turns the second assertion RED.
    """
    yesterday = _enriched_workout_plan("yesterday")
    today = _enriched_workout_plan("today")
    plan_schema.record_plan("workout", yesterday, "2026-06-09", "coach", tmp_path)
    plan_schema.record_plan("workout", today, "2026-06-10", "coach", tmp_path)
    view = horizons.read_horizons("workout", "bench", tmp_path, "2026-06-10")
    assert view["today"]["state"] is None
    assert view["today"]["plan"] == today
    # Drop the render-date plan: only yesterday's is on file -> NO_PLAN_TODAY, never nearest.
    fresh = tmp_path / "no-today"
    plan_schema.record_plan("workout", yesterday, "2026-06-09", "coach", fresh)
    no_today = horizons.read_horizons("workout", "bench", fresh, "2026-06-10")
    assert no_today["today"]["state"] == plan_schema.NO_PLAN_TODAY
    assert no_today["today"]["plan"] is None


# --- ADR-0038-T3 Cycle 2: deterministic expectation-vs-actual classifier ---


def test_expectation_vs_actual_classifier(tmp_path):
    """AC-4 (Risk): the classifier is a pure deterministic expectation-vs-actual map.

    A declared per-week expectation and an actual per-week rate map to a fixed
    ``behind``/``on-track``/``ahead`` verdict by comparison of progress-toward-
    target — direction-agnostic, so a downward weight goal (expectation -0.4) reads
    -0.1 as behind and -0.5 as ahead. No model/presentation layer is invoked (a
    pure arithmetic comparison; the module names no model-send symbol — the egress
    guard in ``test_horizons_writes_no_new_store_stream`` covers that structurally).
    Mutation check: swapping the < / > comparison, or dropping the direction
    normalization, turns a pair RED.
    """
    # Downward (weight-loss) goal: expectation -0.4 kg/wk toward target.
    assert horizons.classify(-0.4, -0.1) == "behind"
    assert horizons.classify(-0.4, -0.4) == "on-track"
    assert horizons.classify(-0.4, -0.5) == "ahead"
    # Upward (gain) goal: expectation +0.4 toward target — same verdicts by direction.
    assert horizons.classify(0.4, 0.1) == "behind"
    assert horizons.classify(0.4, 0.4) == "on-track"
    assert horizons.classify(0.4, 0.5) == "ahead"
    # The three verdict tokens are a single fixed tuple the AC reads.
    assert horizons.CLASSIFICATIONS == ("behind", "on-track", "ahead")


def test_classifier_single_progress_site_no_new_stream(tmp_path):
    """AC-5 (Risk): the pace assessment reads goal_schema + plan history, writes nothing.

    The expectation is sourced from the this-week block's ``week_expectation`` D2
    extra (the date-range plan history); the actual is the goal's realized weekly
    rate via ``goal_schema.resolve_goal`` (the single derived-progress owner — this
    layer re-derives no percent). The path writes no store item. Mutation check:
    re-implementing the goal percent locally (``_percent`` in src) reds the source
    guard; writing any stream reds the before==after scan.
    """
    # Goal: lose 10 (100 -> 90 target). Two snapshots 14 days apart -> -1 over 2 wk
    # = -0.5 kg/wk realized (the actual). resolve_goal owns the derived progress.
    goal = _goal(label="Weight", baseline=100, current=100, target=90, unit="kg")
    goal_schema.record_goal("weight", goal, "2026-06-01", tmp_path)
    goal_schema.record_goal(
        "weight", {**goal, "current": 99}, "2026-06-15", tmp_path
    )
    # This-week plan declares a -0.4 kg/wk expectation (the D2 extra, numeric).
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("cut", week_expectation=-0.4),
        "2026-06-15", "coach", tmp_path,
    )
    before = set(store.items(tmp_path))
    verdict = horizons.assess_pace("workout", "weight", tmp_path, "2026-06-15")
    after = set(store.items(tmp_path))
    # -0.5 actual beats the -0.4 expectation toward target -> ahead.
    assert verdict == "ahead"
    assert verdict in horizons.CLASSIFICATIONS
    # No new store stream written by the assessment path.
    assert after == before
    assert after == {"goal::weight", "plan::workout"}
    # Single progress site: routes through goal_schema, never a local percent.
    src = _HORIZONS_SRC.read_text()
    assert "_percent" not in src
    assert "resolve_goal" in src


def test_assess_pace_absent_inputs_read_none(tmp_path):
    """AC-5 floor: absent expectation or actual yields None, never a fabricated verdict.

    With no declared numeric ``week_expectation`` and/or no multi-week goal span,
    the pace assessment is honest absence — it invents no rate and returns None.
    """
    # A plan with no numeric week_expectation and a single-snapshot goal (no span).
    goal_schema.record_goal("weight", _goal(baseline=100, current=99, target=90),
                            "2026-06-15", tmp_path)
    plan_schema.record_plan(
        "workout", _enriched_workout_plan("cut"), "2026-06-15", "coach", tmp_path
    )
    assert horizons.assess_pace("workout", "weight", tmp_path, "2026-06-15") is None
