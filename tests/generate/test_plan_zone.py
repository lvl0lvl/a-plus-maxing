"""Tests for the zone-3 plan cards and the report's plan routing (ADR-0010).

Seeds plans + tracking through the PRODUCTION writers (`plan_schema`), then
asserts the dashboard's populated card anatomy per domain (workout dots / stat
boxes / chips, nutrition arithmetic + meals states, supplements counter,
peptides protocol line + watch-out controls), the two published absence states
with their digit-free copy, slot-level honesty (absent operands read em-dash,
never 0), deliberate routing (unknown plan domains KeyError), placement +
NEGATIVE placement (plan content in zone 3 only — not zone 4, not zone 7, not
the report's numeric paths), the via-attribution from the `plan::` source, and
measured AA contrast for the new inert-button text pairs.
"""

import datetime
import html as html_lib
import re

import pytest

from scripts.generate import generate
from scripts.store import loop_schema, plan_schema, store
from vault.design.templates import component_set as cs
from vault.design.templates import dashboard

# The fixed seam date the plan resolution compares against (matches the zone
# tests' calendar seam): Wednesday 2026-06-10.
_TODAY = datetime.date(2026, 6, 10)
_DATE = "2026-06-10"


def _zones(html):
    """Map each rendered zone's decoded h2 title to its full section markup."""
    out = {}
    for section in re.findall(r"<section class='zone'[^>]*>.*?</section>", html, re.S):
        title = re.search(r"<h2[^>]*>([^<]*)</h2>", section).group(1)
        out[html_lib.unescape(title)] = section
    return out


def _render(root):
    """Render the dashboard over a tmp store through the read model + seam."""
    return dashboard.render(store.read_all(root), _today=_TODAY)


def _cards(zone):
    """Split zone 3 into accent-key -> card fragment (fragment runs to the next card)."""
    parts = re.split(r"<div class='card pcard pc-([a-z]+)'>", zone)
    return dict(zip(parts[1::2], parts[2::2]))


def _stat_boxes(fragment):
    """Parse a card fragment's stat boxes as (class, label, value) tuples."""
    return re.findall(
        r"<div class='(stat[^']*)'><div class='slabel'>([^<]*)</div>"
        r"<div class='sval'>([^<]*)</div></div>", fragment
    )


def _text(fragment):
    """Return a fragment's tag-stripped, entity-decoded text."""
    return html_lib.unescape(re.sub(r"<[^>]*>", "", fragment))


def _workout_plan():
    """The workout plan fixture: two exercises, one fully annotated."""
    return {
        "exercises": [
            {"name": "Bench Press", "sets": 3, "load": "185 lb", "reps": 8,
             "detail": "3s eccentric"},
            {"name": "Squat", "sets": 4},
        ]
    }


def _nutrition_plan():
    """The nutrition plan fixture: goal, macros, three meals, water target."""
    return {
        "calorie_goal": 2800,
        "macros": {"protein": 180, "carbs": 300, "fat": 80},
        "meals": [
            {"name": "Breakfast", "contents": "eggs, oats", "kcal": 650},
            {"name": "Lunch", "kcal": 900},
            {"name": "Dinner"},
        ],
        "water_l": 3,
    }


def _supplements_plan():
    """The supplements plan fixture: three items, one without timing."""
    return {
        "items": [
            {"name": "Creatine", "dose": "5 g", "timing": "AM"},
            {"name": "Magnesium", "dose": "400 mg", "timing": "PM"},
            {"name": "Omega-3", "dose": "2 g"},
        ]
    }


def _peptides_plan():
    """The peptides plan fixture: full protocol incl. cycle, tags, evidence."""
    return {
        "compound": "bpc-157", "dose": "250 mcg", "route": "subq",
        "cycle_week": 2, "cycle_length_weeks": 8,
        "tags": ["experimental"], "evidence": "View protocol & evidence",
    }


# --- absence states ---


def test_no_plan_state_renders_empty_anatomy_and_copy(tmp_path):
    """An empty store renders all four cards in the no-plan state: the muted
    `awaiting plan` pill, the new digit-free dashed-row copy (the stale "next
    slice" line is gone), and the default specialist attribution."""
    zone = _zones(_render(tmp_path))["Today's Plan"]
    assert zone.count("<span class='pill'>awaiting plan</span>") == 4
    assert zone.count("No plan on file — record one to fill this card.") == 4
    assert "next slice" not in zone, "the stale empty-state copy must be replaced"
    assert "Plan on file is for another day" not in zone
    assert not re.search(r"\d", _text(zone)), "the no-plan zone must be digit-free"
    for specialist in ("personal-trainer", "nutritionist",
                       "supplement-specialist", "peptide-specialist"):
        assert f"via {specialist}" in zone


def test_no_plan_today_state_renders_other_day_copy(tmp_path):
    """A plan on file dated another day renders the no-plan-today copy (digit-
    free), the muted pill, and the em-dash empty anatomy — never yesterday's
    plan content presented as today's."""
    plan_schema.record_plan("workout", _workout_plan(), "2026-06-08", "coach", tmp_path)
    zone = _zones(_render(tmp_path))["Today's Plan"]
    card = _cards(zone)["training"]
    assert "Plan on file is for another day — none recorded for today." in card
    assert "<span class='pill'>awaiting plan</span>" in card
    assert "Bench Press" not in card, "another day's plan content must not render"
    assert not re.search(r"\d", _text(card)), "the no-plan-today card is digit-free"
    # The other three cards stay in the no-plan state.
    assert zone.count("No plan on file — record one to fill this card.") == 3


# --- workout card ---


def test_workout_populated_full_snapshot(tmp_path):
    """The populated workout card renders every signed slot from real data:
    stat boxes (Sets done summed over tracked/planned, heart-rate live-state
    tinted), present-field chips, exercise rows with load × reps captions and
    accent/border progress dots, the detail caption, the inert rest-timer
    footer, the `via` attribution from the plan source, and the accent-tinted
    `today` pill."""
    plan_schema.record_plan("workout", _workout_plan(), _DATE, "strength-coach", tmp_path)
    plan_schema.record_plan_tracking("workout", {
        "elapsed_min": 42, "volume_lb": 12450, "sets_done": {"Bench Press": 2},
        "heart_rate_bpm": 128, "steps": 8200, "kcal_burned": 520,
    }, _DATE, tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["training"]
    assert "<span class='caption'>via strength-coach</span>" in card, (
        "attribution comes from the resolved plan source, not the static default"
    )
    assert "via personal-trainer" not in card
    assert "<span class='pill tint-training'>today</span>" in card
    assert "awaiting plan" not in card
    assert _stat_boxes(card) == [
        ("stat", "Elapsed", "42 min"), ("stat", "Volume", "12450 lb"),
        ("stat", "Sets done", "2/7"), ("stat tint-neutral", "Heart rate", "128 bpm"),
    ], "heart-rate is unregistered: neutral tint, never an invented judgment"
    assert "<span class='chip-b'>8200 steps</span>" in card
    assert "<span class='chip-b'>520 kcal</span>" in card
    assert "min exercise" not in card, "an absent tracking field renders no chip"
    assert "<span class='plabel'>Bench Press</span>" in card
    assert "<span class='caption'>185 lb × 8</span>" in card
    assert "<div class='caption'>3s eccentric</div>" in card
    accent_dot = f"<span class='setdot' style='background:{cs.ACCENTS['training']}'></span>"
    border_dot = f"<span class='setdot' style='background:{cs.CHROME['card-border']}'></span>"
    assert card.count(accent_dot) == 2, "Bench Press: 2 tracked sets filled"
    assert card.count(border_dot) == 5, "1 remaining Bench set + 4 untracked Squat sets"
    assert "Rest timer —" in card
    assert (
        f"<span class='btnfill' style='background:{cs.CHROME['training-text']}'>"
        "Resume</span>"
    ) in card
    assert "<a " not in card and "href" not in card and "<script" not in card, (
        "the Resume button is static inert chrome (ADR-0004)"
    )


def test_workout_plan_without_tracking_renders_dashes(tmp_path):
    """A plan with NO tracking snapshot renders em-dash stat slots (never
    0/total), zero filled dots, and no chips row — absence is absence."""
    plan_schema.record_plan("workout", _workout_plan(), _DATE, "coach", tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["training"]
    assert _stat_boxes(card) == [
        ("stat", "Elapsed", "—"), ("stat", "Volume", "—"),
        ("stat", "Sets done", "—"), ("stat tint-neutral", "Heart rate", "—"),
    ]
    assert "0/7" not in card, "no snapshot must not fabricate a 0-of-total claim"
    assert f"background:{cs.ACCENTS['training']}'></span>" not in card.split("<div class='prow'>", 1)[1], (
        "no tracked set: no accent-filled dot"
    )
    assert "<div class='chips'>" not in card
    assert "<span class='pill tint-training'>today</span>" in card


def test_workout_sets_done_overflow_raises(tmp_path):
    """A tracked sets_done above the planned sets RAISES — never a silently
    capped dot claim (ADR-0010 D5)."""
    plan_schema.record_plan("workout", _workout_plan(), _DATE, "coach", tmp_path)
    plan_schema.record_plan_tracking(
        "workout", {"sets_done": {"Bench Press": 4}}, _DATE, tmp_path
    )
    with pytest.raises(ValueError, match="Bench Press"):
        _render(tmp_path)


def test_workout_sets_done_unknown_exercise_not_rendered(tmp_path):
    """A sets_done key matching no plan exercise renders no row and never
    counts: the Sets-done numerator sums only the PLAN's exercise names (the
    supplements counter's taken ∩ plan rule), and the unknown key never
    raises (the overflow check guards plan exercises only)."""
    plan_schema.record_plan("workout", _workout_plan(), _DATE, "coach", tmp_path)
    plan_schema.record_plan_tracking(
        "workout", {"sets_done": {"Bench Press": 2, "Deadlift": 6}}, _DATE, tmp_path
    )
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["training"]
    assert "Deadlift" not in card
    assert ("stat", "Sets done", "2/7") in _stat_boxes(card), (
        "the numerator counts plan-intersecting keys only"
    )
    # An unknown-only snapshot, value far above the plan total: 100 unknown
    # sets can never inflate the numerator past the denominator — 0/7, no raise.
    plan_schema.record_plan_tracking(
        "workout", {"sets_done": {"Deadlift": 100}}, _DATE, tmp_path
    )
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["training"]
    assert ("stat", "Sets done", "0/7") in _stat_boxes(card)


# --- nutrition card ---


def test_nutrition_populated_arithmetic_macros_meals_water(tmp_path):
    """The populated nutrition card: Goal from plan, Food/Exercise from
    tracking, Remaining derived from all three; macro tracks caption true
    numbers with the accent fill only where tracked; the meals checklist walks
    logged ✓ / Up next / Log in plan order with the Add-food link; the water
    track follows the macro rules."""
    plan_schema.record_plan("nutrition", _nutrition_plan(), _DATE, "macro-coach", tmp_path)
    plan_schema.record_plan_tracking("nutrition", {
        "food_kcal": 1450, "exercise_kcal": 320, "macros_g": {"protein": 120},
        "meals_logged": ["Breakfast"], "water_l": 1.5,
    }, _DATE, tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["nutrition"]
    assert "via macro-coach" in card
    assert "<span class='pill tint-nutrition'>today</span>" in card
    assert _stat_boxes(card) == [
        ("stat", "Goal", "2800"), ("stat", "Food", "1450"),
        ("stat", "Exercise", "320"), ("stat tinted", "Remaining", "1670"),
    ], "Remaining = goal − food + exercise, all three operands present"
    assert "Protein 120 / 180 g" in _text(card)
    assert "Carbs — / 300 g" in _text(card)
    assert "Fat — / 80 g" in _text(card)
    fills = re.findall(r"<div class='fill' style='width:([\d.]+)%;background:([^']*)'>", card)
    assert fills == [
        ("66.7", cs.ACCENTS["nutrition"]),  # protein: 120/180
        ("50.0", cs.ACCENTS["nutrition"]),  # water: 1.5/3
    ], "only the tracked tracks fill, in the nutrition accent"
    assert "Today's meals · from your plan" in _text(card)
    assert "eggs, oats" in card and "650 kcal" in card
    breakfast, lunch, dinner = (
        card.split("<span class='plabel'>Breakfast</span>", 1)[1]
        .partition("<span class='plabel'>Lunch</span>")[0],
        card.partition("<span class='plabel'>Lunch</span>")[2]
        .partition("<span class='plabel'>Dinner</span>")[0],
        card.partition("<span class='plabel'>Dinner</span>")[2],
    )
    assert "<span class='state-good'>✓</span>" in breakfast, "logged meal: good check"
    assert "<span class='chip-b'>Up next</span>" in lunch, "first unlogged: Up next"
    assert "<span class='chip-b'>Log</span>" in dinner, "later unlogged: Log chip"
    assert "<span class='linkish'>Add food</span>" in card
    assert "Water 1.5 / 3 L" in _text(card)


def test_nutrition_missing_operand_remaining_is_em_dash(tmp_path):
    """An absent operand is NOT 0: with no food_kcal the Remaining slot reads
    em-dash, never goal + exercise presented as the remainder."""
    plan_schema.record_plan("nutrition", _nutrition_plan(), _DATE, "coach", tmp_path)
    plan_schema.record_plan_tracking("nutrition", {"exercise_kcal": 320}, _DATE, tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["nutrition"]
    assert _stat_boxes(card) == [
        ("stat", "Goal", "2800"), ("stat", "Food", "—"),
        ("stat", "Exercise", "320"), ("stat tinted", "Remaining", "—"),
    ]
    assert "3120" not in card, "a partial Remaining is an invented number"


def test_nutrition_fill_clamps_but_caption_carries_true_numbers(tmp_path):
    """An over-target macro clamps the fill geometry at 100% while the caption
    keeps the true value/target pair."""
    plan_schema.record_plan("nutrition", _nutrition_plan(), _DATE, "coach", tmp_path)
    plan_schema.record_plan_tracking(
        "nutrition", {"macros_g": {"protein": 200}}, _DATE, tmp_path
    )
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["nutrition"]
    assert "Protein 200 / 180 g" in _text(card)
    assert "width:100%" in card
    assert not re.search(r"width:1\d\d\.", card), "the fill never exceeds 100%"


def test_nutrition_negative_value_renders_zero_width_fill(tmp_path):
    """A negative tracked macro (bad data bypassing the writer floor via raw
    store.append) renders width:0.0% fill geometry — a negative width is
    invalid CSS a browser DROPS, which would render a FULL bar — while the
    caption carries the true number (the honest display of bad data)."""
    plan_schema.record_plan("nutrition", _nutrition_plan(), _DATE, "coach", tmp_path)
    reading = {"item": "plan-track::nutrition", "timepoint": _DATE,
               "source": "plan-track::raw", "value": {"macros_g": {"protein": -50}}}
    store.append("plan-track::nutrition", reading, root=tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["nutrition"]
    assert "Protein -50 / 180 g" in _text(card), "the caption keeps the true number"
    assert "width:0.0%" in card
    assert "width:-" not in card, "negative geometry must never reach the CSS"


# --- supplements card ---


def test_supplements_no_snapshot_renders_muted_dash_counter(tmp_path):
    """NO snapshot reads `— of m taken` on the muted pill (never 0): absence
    of tracking is not an empty checklist."""
    plan_schema.record_plan("supplements", _supplements_plan(), _DATE, "stack-coach", tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["supplements"]
    assert "<span class='pill'>— of 3 taken</span>" in card
    assert "0 of 3" not in card
    assert "<span class='pill tint-supplements'>today</span>" in card
    assert "via stack-coach" in card
    border_dot = f"<span class='setdot' style='background:{cs.CHROME['card-border']}'></span>"
    assert card.count(border_dot) == 3, "every row carries the unfilled marker"
    assert "<span class='chip-b'>AM</span>" in card
    assert "<span class='chip-b'>PM</span>" in card
    omega = card.partition("<span class='plabel'>Omega-3</span>")[2]
    assert "<span class='chip-b'>" not in omega.partition("</div>")[0], (
        "an item without timing renders no timing chip"
    )


def test_supplements_empty_taken_renders_zero_counter(tmp_path):
    """`{"taken": []}` is the explicit none-taken snapshot: `0 of m taken` on
    the card tint — distinct from the no-snapshot em-dash."""
    plan_schema.record_plan("supplements", _supplements_plan(), _DATE, "coach", tmp_path)
    plan_schema.record_plan_tracking("supplements", {"taken": []}, _DATE, tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["supplements"]
    assert "<span class='pill tint-supplements'>0 of 3 taken</span>" in card
    assert "— of 3 taken" not in card


def test_supplements_taken_intersects_plan_names(tmp_path):
    """The counter counts only taken names matching the plan; taken rows carry
    the PALETTE-good check, untaken rows the unfilled marker."""
    plan_schema.record_plan("supplements", _supplements_plan(), _DATE, "coach", tmp_path)
    plan_schema.record_plan_tracking(
        "supplements", {"taken": ["Creatine", "Zinc"]}, _DATE, tmp_path
    )
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["supplements"]
    assert "<span class='pill tint-supplements'>1 of 3 taken</span>" in card
    assert "Zinc" not in card, "a taken name outside the plan renders no row"
    creatine = card.partition("<span class='plabel'>Creatine</span>")[2].partition("</div>")[0]
    assert "<span class='state-good'>✓</span>" in creatine
    magnesium = card.partition("<span class='plabel'>Magnesium</span>")[2].partition("</div>")[0]
    assert "state-good" not in magnesium
    assert "setdot" in magnesium


# --- peptides card ---


def test_peptides_populated_protocol_watchouts_and_evidence(tmp_path):
    """The populated peptides card: the protocol line, the both-fields week
    caption, plain bordered tag chips (no invented `experimental` styling),
    watch-out rows from the compound's derived question set — the answered one
    as a bordered chip read from the GROUPED zone-7 stream (second consumer),
    the unanswered one as the inert accent Answer button — and the evidence
    link-styled caption."""
    plan_schema.record_plan("peptides", _peptides_plan(), _DATE, "peptide-doc", tmp_path)
    loop_schema.record_watchout_answer(
        "injection_site_reaction", "none noticed", "2026-06-09T08:00:00+00:00", tmp_path
    )
    html = _render(tmp_path)
    zones = _zones(html)
    card = _cards(zones["Today's Plan"])["peptides"]
    assert "bpc-157 · 250 mcg · subq" in _text(card)
    assert "Week 2 of 8" in _text(card)
    assert "<span class='chip-b'>experimental</span>" in card, (
        "tags are plain bordered chips — no tint, no special styling"
    )
    assert "tint-peptides'>experimental" not in card
    assert "Injection Site Reaction" in card
    assert "<span class='chip-b'>none noticed</span>" in card, (
        "the answered watch-out renders its latest stored answer"
    )
    assert "Appetite Change" in card
    assert (
        f"<span class='btnfill' style='background:{cs.CHROME['peptides-text']}'>"
        "Answer</span>"
    ) in card, "the unanswered watch-out renders the inert accent Answer button"
    assert "<span class='linkish'>View protocol &amp; evidence</span>" in card
    assert "<a " not in card and "href" not in card, "every control is inert"
    # Second consumer, not a re-route: the answer still renders in zone 7.
    assert "none noticed" in zones["Labs & Bloodwork"]


def test_peptides_week_caption_needs_both_cycle_fields(tmp_path):
    """The week caption renders only when BOTH cycle fields are present."""
    plan = {k: v for k, v in _peptides_plan().items() if k != "cycle_length_weeks"}
    plan_schema.record_plan("peptides", plan, _DATE, "coach", tmp_path)
    card = _cards(_zones(_render(tmp_path))["Today's Plan"])["peptides"]
    assert "Week" not in _text(card), "a lone cycle_week renders no week caption"


# --- routing: fail-loud + placement ---


def test_unknown_plan_domain_fails_loud(tmp_path):
    """A plan::/plan-track:: item outside the published domain sets raises
    KeyError naming the domain — deliberate routing, no silent fallthrough."""
    reading = {"item": "plan::cardio", "timepoint": _DATE,
               "source": "plan::coach", "value": {"x": 1}}
    store.append("plan::cardio", reading, root=tmp_path)
    with pytest.raises(KeyError) as exc:
        _render(tmp_path)
    assert "cardio" in str(exc.value)


def test_untracked_plan_track_domain_fails_loud(tmp_path):
    """plan-track::peptides is unrouted (peptide tracking IS the watch-out
    stream): KeyError naming the domain."""
    reading = {"item": "plan-track::peptides", "timepoint": _DATE,
               "source": "plan-track::x", "value": {"taken": []}}
    store.append("plan-track::peptides", reading, root=tmp_path)
    with pytest.raises(KeyError) as exc:
        _render(tmp_path)
    assert "peptides" in str(exc.value)


def _seed_all_domains(root, on_date=_DATE):
    """Seed all four plan domains + the three tracking snapshots via the writers."""
    plan_schema.record_plan("workout", _workout_plan(), on_date, "strength-coach", root)
    plan_schema.record_plan_tracking(
        "workout", {"elapsed_min": 42, "sets_done": {"Bench Press": 2}}, on_date, root
    )
    plan_schema.record_plan("nutrition", _nutrition_plan(), on_date, "macro-coach", root)
    plan_schema.record_plan_tracking(
        "nutrition", {"food_kcal": 1450, "exercise_kcal": 320}, on_date, root
    )
    plan_schema.record_plan("supplements", _supplements_plan(), on_date, "stack-coach", root)
    plan_schema.record_plan_tracking("supplements", {"taken": ["Creatine"]}, on_date, root)
    plan_schema.record_plan("peptides", _peptides_plan(), on_date, "peptide-doc", root)


def test_plan_content_renders_in_zone3_only(tmp_path):
    """Placement + NEGATIVE placement (ADR-0010 D5): plan/tracking content
    renders ONLY inside the zone-3 cards — never zone 4 (no metric card, no
    sparkline over plan data), never zone 7, and no raw plan::/plan-track::
    key leaks into the artifact."""
    _seed_all_domains(tmp_path)
    loop_schema.record_biomarker("bodyweight", "2026-06-08T00:00:00+00:00", 183, tmp_path)
    html = _render(tmp_path)
    assert "plan::" not in html and "plan-track::" not in html, (
        "raw store keys must never render"
    )
    zones = _zones(html)
    plan_zone = zones["Today's Plan"]
    trends = zones["Performance & Trends"]
    labs = zones["Labs & Bloodwork"]
    for marker in ("Bench Press", "2800", "Creatine", "bpc-157"):
        assert marker in plan_zone, f"plan content {marker!r} renders in zone 3"
        assert marker not in trends, f"plan content {marker!r} leaked into zone 4"
        assert marker not in labs, f"plan content {marker!r} leaked into zone 7"
    assert trends.count("<div class='kpi-row'>") == 1, (
        "zone 4 carries exactly the seeded biomarker card — no plan-derived card"
    )
    assert "<svg" not in plan_zone, "the plan cards draw no sparkline"


def test_production_path_renders_populated_plan_zone(tmp_path):
    """generate.run('dashboard') over writer-seeded plans dated the REAL today
    renders the populated zone-3 cards end-to-end (factory wiring, not a
    template-only seam test)."""
    root = tmp_path / "store"
    _seed_all_domains(root, on_date=datetime.date.today().isoformat())
    path = generate.run("dashboard", _root=root, _out_dir=tmp_path / "out")
    zone = _zones(path.read_text())["Today's Plan"]
    assert zone.count("'>today</span>") == 4, "all four cards resolve populated"
    assert "awaiting plan" not in zone
    assert "Bench Press" in zone and "via strength-coach" in zone


# --- report routing ---


def _report_sections(html):
    """Map each report section's raw h2 heading to its section markup."""
    out = {}
    for section in re.findall(r"<section>.*?</section>", html, re.S):
        heading = re.search(r"<h2>([^<]*)</h2>", section).group(1)
        out[html_lib.unescape(heading)] = section
    return out


def test_report_routes_plan_items_to_verbatim_tables(tmp_path):
    """The report renders plan::/plan-track:: items as heading + readings
    table ONLY — no KPI, no sparkline (a dict value reaching numeric viz is
    the production crash this routing exists to prevent) — while biomarker
    sections keep their numeric path. Runs the PRODUCTION path."""
    root = tmp_path / "store"
    _seed_all_domains(root)
    loop_schema.record_biomarker("bodyweight", "2026-06-01T00:00:00+00:00", 184, root)
    loop_schema.record_biomarker("bodyweight", "2026-06-08T00:00:00+00:00", 183, root)

    path = generate.run("report", _root=root, _out_dir=tmp_path / "out")

    sections = _report_sections(path.read_text())
    plan_headings = [h for h in sections if h.startswith(("plan::", "plan-track::"))]
    assert sorted(plan_headings) == [
        "plan-track::nutrition", "plan-track::supplements", "plan-track::workout",
        "plan::nutrition", "plan::peptides", "plan::supplements", "plan::workout",
    ], "every plan stream renders its own report section"
    for heading in plan_headings:
        section = sections[heading]
        assert "<table>" in section, f"{heading} must render its readings table"
        assert "<svg" not in section, f"{heading} must not reach the sparkline path"
        assert "class='kpi'" not in section, f"{heading} must render no KPI"
    assert "Bench Press" in sections["plan::workout"], "the table str()s the value verbatim"
    bodyweight = sections["biomarker::bodyweight"]
    assert "<svg" in bodyweight and "class='kpi'" in bodyweight, (
        "numeric sections keep their KPI + sparkline path"
    )


# --- measured AA pairs for the new text-on-fill chrome ---


def _hex_to_rgb(h):
    """Convert '#rrggbb' to an (r, g, b) tuple of 0-255 ints."""
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _contrast_ratio(fg, bg):
    """WCAG contrast ratio between two hex colors: (L1+0.05)/(L2+0.05)."""
    def lum(rgb):
        r, g, b = (
            c / 12.92 if (c := v / 255) <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
            for v in rgb
        )
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    l1, l2 = lum(_hex_to_rgb(fg)), lum(_hex_to_rgb(bg))
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def test_btnfill_text_pairs_measure_aa(tmp_path):
    """Every rendered inert-button fill carries paper text at a COMPUTED >= 4.5
    contrast (WCAG AA normal text): the fills are the CHROME `*-text` shades
    already gate-measured against their (darker-than-paper) tints, asserted
    here over the actually-rendered pairs — extending the AA discipline to the
    new chrome, never weakening the existing gate."""
    _seed_all_domains(tmp_path)
    html = _render(tmp_path)
    fills = re.findall(r"<span class='btnfill' style='background:(#[0-9A-Fa-f]{6})'>", html)
    assert sorted(set(fills)) == sorted(
        {cs.CHROME["training-text"], cs.CHROME["peptides-text"]}
    ), "the rendered button fills are exactly the two cards' *-text shades"
    for fill in set(fills):
        ratio = _contrast_ratio(cs.PALETTE["paper"], fill)
        assert ratio >= 4.5, f"paper on {fill} computes {ratio:.2f} < 4.5"
