"""Plan-content / plan-tracking store schemas (ADR-0010).

The plan zone's data-in schemas record two operator-facing streams — per-domain
specialist-attributed plan documents and per-domain day-snapshot tracking — and
read them back through two published absence states. Every write goes THROUGH
``scripts.store.store`` (``append`` / ``correct``) keyed by the one
``scripts.store.keying`` Line Field Set; this module defines no second key,
reimplements no store I/O, and imports loop_schema's content-tag derivation
rather than re-deriving it. All persistence is local file I/O; 0 model-bound
send.

Streams (disjoint item namespaces, ADR-0010 D1/D3):
    plan::<domain>        one day-keyed plan document per domain; timepoint =
                          the plan's declared YYYY-MM-DD date; source =
                          ``plan::<specialist-slug>`` (the attribution home,
                          rendered as the card's ``via`` caption); value = the
                          structured plan content. Revisions go through
                          ``correct_plan`` (append-supersede): a re-record with
                          a CHANGED value is a store-dedupe no-op, never a
                          silent overwrite.
    plan-track::<domain>  day-snapshot tracking for workout / nutrition /
                          supplements, content-tagged sources (distinct same-day
                          snapshots both persist; an identical re-entry is an
                          idempotent no-op); the latest-appended snapshot for a
                          date wins on read. Peptide tracking IS the existing
                          watch-out stream — no fourth tracked domain.

The two published absence states are read 1:1 by the dashboard plan zone
(ADR-0010 D4):
    no-plan        a domain with zero stored plan documents
    no-plan-today  plans on file, none whose date equals the render date

Presence is not a third marker: a resolved plan is its value + attribution.
Content schemas are closed on required fields and open on extras (the ADR-0006
T2 forward-compatibility seam): unknown extra keys are permitted and ignored.
Writers raise only ValueError; readers never raise on absence.
"""

import datetime
import re

from scripts.store import plan_confirm, store
from scripts.store.loop_schema import _content_tag, _reading

NO_PLAN = "no-plan"
NO_PLAN_TODAY = "no-plan-today"

# The closed plan-domain set (ADR-0010 D1) and its tracked subset (D3).
PLAN_DOMAINS = ("workout", "nutrition", "supplements", "peptides")
TRACKED_DOMAINS = ("workout", "nutrition", "supplements")

# Per-stream item-id prefixes. "plan::" doubles as the source-tag prefix for
# specialist attribution (``plan::<specialist-slug>``); "plan-track::" is the
# content-tag prefix for tracking sources. The "::" separator is not a path
# separator, so prefixed ids stay direct children of the store root.
_PREFIX_PLAN = "plan::"
_PREFIX_TRACK = "plan-track::"

# Day-keyed timepoints are date-only by contract: date EQUALITY against the
# render date is the today-resolution mechanism (D4), so a malformed date
# would silently render the card awaiting forever — rejected at the writer
# boundary instead (operator-approved boundary validation).
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _is_int(value):
    """Report whether `value` is an int (bool excluded — it is not a count)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value):
    """Report whether `value` is an int or float (bool excluded)."""
    return _is_int(value) or isinstance(value, float)


def _is_nonneg_int(value):
    """Report whether `value` is an int >= 0 (bool excluded)."""
    return _is_int(value) and value >= 0


def _is_nonneg_number(value):
    """Report whether `value` is an int or float >= 0 (bool excluded)."""
    return _is_number(value) and value >= 0


def _is_nonempty_str(value):
    """Report whether `value` is a non-empty str."""
    return isinstance(value, str) and value != ""


def _check_date(value, what):
    """Reject a timepoint that is not a real YYYY-MM-DD calendar date.

    Date equality IS the today-resolution mechanism (ADR-0010 D4): a malformed
    or impossible date can never equal a render date, so the plan would
    silently read absent forever. Fails loud at the writer boundary instead.

    Args:
        value: The candidate date string.
        what (str): The argument name for the error message.

    Raises:
        ValueError: `value` is not a YYYY-MM-DD string naming a real date.
    """
    if not isinstance(value, str) or not _DATE_RE.fullmatch(value):
        raise ValueError(f"{what} {value!r} is not a YYYY-MM-DD date")
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{what} {value!r} is not a real calendar date") from None


def _check_fields(what, mapping, required, optional):
    """Validate a dict's required/optional fields against their predicates.

    Closed on required fields, open on extras (ADR-0010 D2): a missing or
    mistyped required field raises, a present-but-mistyped optional field
    raises, and unknown extra keys are permitted and ignored.

    Args:
        what (str): The structure name for error messages.
        mapping (dict): The structure to validate.
        required (dict): field -> (predicate, expectation text).
        optional (dict): field -> (predicate, expectation text).

    Raises:
        ValueError: `mapping` is not a dict, a required field is missing or
            mistyped, or a present optional field is mistyped.
    """
    if not isinstance(mapping, dict):
        raise ValueError(f"{what} must be a dict, got {type(mapping).__name__}")
    for field, (check, expects) in required.items():
        if field not in mapping:
            raise ValueError(f"{what} missing required field {field!r}")
        if not check(mapping[field]):
            raise ValueError(f"{what} field {field!r} must be {expects}")
    for field, (check, expects) in optional.items():
        if field in mapping and not check(mapping[field]):
            raise ValueError(f"{what} field {field!r} must be {expects}")


def _is_dict_list(value):
    """Report whether `value` is a list of >=1 dicts."""
    return (
        isinstance(value, list)
        and len(value) >= 1
        and all(isinstance(entry, dict) for entry in value)
    )


def _is_str_list(value):
    """Report whether `value` is a list of strs (empty allowed)."""
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def _check_unique_names(what, entries):
    """Reject duplicate entry names within one plan document.

    A duplicate name renders contradictory claims (two same-named exercises
    fill one counter's dots twice; a duplicate supplement double-checks one
    row) — rejected at the writer boundary like the typo'd macro key.

    Args:
        what (str): The entry kind for the error message.
        entries (list): The validated entry dicts (each carries `name`).

    Raises:
        ValueError: Two entries share a name.
    """
    seen = set()
    for entry in entries:
        name = entry["name"]
        if name in seen:
            raise ValueError(f"{what} name {name!r} appears more than once")
        seen.add(name)


def _validate_workout_plan(plan):
    """Validate a workout plan document: schema table + unique exercise names."""
    _check_fields(
        "workout plan", plan,
        {"exercises": (_is_dict_list, "a list of >=1 exercise dicts")}, {},
    )
    for exercise in plan["exercises"]:
        _check_fields(
            "workout plan exercise", exercise,
            {
                "name": (_is_nonempty_str, "a non-empty str"),
                # Ceiling 100: unbounded sets drives multi-GB string
                # materialization in the per-set dot renderer through the
                # legitimate writer (schema-table bound).
                "sets": (lambda v: _is_int(v) and 1 <= v <= 100, "an int in 1..100"),
            },
            {
                "load": (lambda v: isinstance(v, str), "a str"),
                "reps": (lambda v: _is_int(v) or isinstance(v, str), "an int or str"),
                "detail": (lambda v: isinstance(v, str), "a str"),
            },
        )
    _check_unique_names("workout plan exercise", plan["exercises"])


def _validate_nutrition_plan(plan):
    """Validate a nutrition plan document: schema table + unique meal names."""
    _check_fields(
        "nutrition plan", plan,
        {
            "calorie_goal": (lambda v: _is_int(v) and v > 0, "an int > 0"),
            "macros": (lambda v: isinstance(v, dict), "a dict"),
            "meals": (_is_dict_list, "a list of >=1 meal dicts"),
        },
        {"water_l": (lambda v: _is_number(v) and v > 0, "a number > 0")},
    )
    _check_fields(
        "nutrition plan macros", plan["macros"],
        {
            macro: (lambda v: _is_int(v) and v > 0, "an int > 0")
            for macro in ("protein", "carbs", "fat")
        },
        {},
    )
    for meal in plan["meals"]:
        _check_fields(
            "nutrition plan meal", meal,
            {"name": (_is_nonempty_str, "a non-empty str")},
            {
                "contents": (lambda v: isinstance(v, str), "a str"),
                "kcal": (_is_int, "an int"),
            },
        )
    _check_unique_names("nutrition plan meal", plan["meals"])


def _validate_supplements_plan(plan):
    """Validate a supplements plan document: schema table + unique item names."""
    _check_fields(
        "supplements plan", plan,
        {"items": (_is_dict_list, "a list of >=1 item dicts")}, {},
    )
    for entry in plan["items"]:
        _check_fields(
            "supplements plan item", entry,
            {
                "name": (_is_nonempty_str, "a non-empty str"),
                "dose": (lambda v: isinstance(v, str), "a str"),
            },
            {"timing": (lambda v: isinstance(v, str), "a str")},
        )
    _check_unique_names("supplements plan item", plan["items"])


def _validate_peptides_plan(plan):
    """Validate a peptides plan document against its schema table."""
    _check_fields(
        "peptides plan", plan,
        {
            "compound": (_is_nonempty_str, "a non-empty str"),
            "dose": (lambda v: isinstance(v, str), "a str"),
            "route": (lambda v: isinstance(v, str), "a str"),
        },
        {
            "cycle_week": (lambda v: _is_int(v) and v >= 1, "an int >= 1"),
            "cycle_length_weeks": (lambda v: _is_int(v) and v >= 1, "an int >= 1"),
            "tags": (_is_str_list, "a list of strs"),
            "evidence": (lambda v: isinstance(v, str), "a str"),
        },
    )


_PLAN_VALIDATORS = {
    "workout": _validate_workout_plan,
    "nutrition": _validate_nutrition_plan,
    "supplements": _validate_supplements_plan,
    "peptides": _validate_peptides_plan,
}


def _is_sets_done(value):
    """Report whether `value` is a dict of exercise name -> int >= 0."""
    return isinstance(value, dict) and all(
        isinstance(name, str) and _is_int(count) and count >= 0
        for name, count in value.items()
    )


def _is_macros_g(value):
    """Report whether `value` is a dict of a protein/carbs/fat subset -> ints >= 0.

    Keys outside the three macro names are rejected (a typo'd macro key would
    otherwise silently never render against its plan target); a negative gram
    count is rejected like every other tracked numeric.
    """
    return isinstance(value, dict) and all(
        key in ("protein", "carbs", "fat") and _is_nonneg_int(grams)
        for key, grams in value.items()
    )


def _validate_workout_tracking(tracking):
    """Validate a workout tracking snapshot's known-field types.

    Every numeric field carries a >= 0 floor (the sets_done discipline): a
    negative tracked value renders a fabricated claim surface.
    """
    _check_fields(
        "workout tracking", tracking, {},
        {
            "elapsed_min": (_is_nonneg_number, "a number >= 0"),
            "volume_lb": (_is_nonneg_number, "a number >= 0"),
            "sets_done": (_is_sets_done, "a dict of exercise name -> int >= 0"),
            "heart_rate_bpm": (_is_nonneg_number, "a number >= 0"),
            "steps": (_is_nonneg_int, "an int >= 0"),
            "kcal_burned": (_is_nonneg_int, "an int >= 0"),
            "exercise_min": (_is_nonneg_int, "an int >= 0"),
        },
    )


def _validate_nutrition_tracking(tracking):
    """Validate a nutrition tracking snapshot's known-field types.

    Every numeric field carries a >= 0 floor (the sets_done discipline): a
    negative tracked value renders a fabricated claim surface.
    """
    _check_fields(
        "nutrition tracking", tracking, {},
        {
            "food_kcal": (_is_nonneg_int, "an int >= 0"),
            "exercise_kcal": (_is_nonneg_int, "an int >= 0"),
            "macros_g": (_is_macros_g, "a dict of protein/carbs/fat -> ints >= 0"),
            "meals_logged": (_is_str_list, "a list of meal names"),
            "water_l": (_is_nonneg_number, "a number >= 0"),
        },
    )


def _validate_supplements_tracking(tracking):
    """Validate a supplements tracking snapshot: `taken` is required.

    `{"taken": []}` is the explicit "none taken" snapshot (renders `0 of m`),
    distinct from no snapshot at all (renders `— of m`).
    """
    _check_fields(
        "supplements tracking", tracking,
        {"taken": (_is_str_list, "a list of item names")}, {},
    )


_TRACKING_VALIDATORS = {
    "workout": _validate_workout_tracking,
    "nutrition": _validate_nutrition_tracking,
    "supplements": _validate_supplements_tracking,
}


def _check_plan_args(domain, plan, plan_date, specialist):
    """Validate the shared record/correct plan-writer arguments.

    Raises:
        ValueError: Unknown domain, malformed date, empty specialist, or a
            plan failing its domain schema table.
    """
    if domain not in PLAN_DOMAINS:
        raise ValueError(f"unknown plan domain {domain!r}; known: {PLAN_DOMAINS}")
    _check_date(plan_date, "plan_date")
    if not _is_nonempty_str(specialist):
        raise ValueError(f"specialist must be a non-empty str, got {specialist!r}")
    _PLAN_VALIDATORS[domain](plan)


def record_plan(domain, plan, plan_date, specialist, root):
    """Record one specialist-attributed plan document for a domain and date.

    Appends exactly one reading via `store.append`: item ``plan::<domain>``,
    timepoint = `plan_date`, source = ``plan::<specialist>``, value = `plan`.
    Inherits the store dedupe: re-recording a CHANGED value for a stored
    (domain, date, specialist) identity is a no-op — never a silent overwrite;
    an intended value change goes through `correct_plan`.

    Superseded (ADR-0044-T1): ``scripts.store.plan_model.record_plan_version`` is the
    canonical comprehensive plan-storage entry — ONE composite version per date (per
    active domain the seven-field DOMAIN PROGRAM + integrated narrative + dated
    milestones + compiled monitoring config) under the disjoint ``plan-model::`` stream.
    This thin single-domain ``plan::<domain>`` record path is retained for the pre-model
    history the ADR-0044-T2 mixed-history reader still consumes (comprehensive-wins).

    Args:
        domain (str): A `PLAN_DOMAINS` member.
        plan (dict): The plan content per the domain's schema table (closed on
            required fields, open on extras).
        plan_date (str): The plan's declared YYYY-MM-DD date.
        specialist (str): The attributed specialist slug (non-empty).
        root (str | Path): The store root.

    Raises:
        ValueError: Unknown domain, malformed date, empty specialist, or a
            missing/mistyped schema field.
    """
    _check_plan_args(domain, plan, plan_date, specialist)
    item = f"{_PREFIX_PLAN}{domain}"
    store.append(
        item, _reading(item, plan_date, f"{_PREFIX_PLAN}{specialist}", plan), root=root
    )


def correct_plan(domain, plan, plan_date, specialist, root):
    """Supersede an already-stored plan document's value via `store.correct`.

    Same validation as `record_plan`; the (domain, date, specialist) identity
    must already be stored — a mistyped correction fails loud instead of
    silently creating a new plan. The prior lines' logical content stays in
    the file (append-only audit trail); every read resolves to this value.

    Args:
        domain (str): A `PLAN_DOMAINS` member.
        plan (dict): The superseding plan content per the domain's schema table.
        plan_date (str): The plan's declared YYYY-MM-DD date.
        specialist (str): The attributed specialist slug (non-empty).
        root (str | Path): The store root.

    Raises:
        ValueError: A `record_plan` validation failure, or no stored reading
            carries the (domain, date, specialist) identity.
    """
    _check_plan_args(domain, plan, plan_date, specialist)
    item = f"{_PREFIX_PLAN}{domain}"
    store.correct(
        item, _reading(item, plan_date, f"{_PREFIX_PLAN}{specialist}", plan), root=root
    )


def record_plan_tracking(domain, tracking, on_date, root):
    """Record one day-snapshot tracking entry for a tracked domain.

    Appends item ``plan-track::<domain>`` at `on_date` under a content-tagged
    source (loop_schema's derivation on the ``plan-track::`` prefix), so two
    distinct same-day snapshots both persist while an identical re-entry stays
    an idempotent no-op — unless a distinct snapshot intervened (the revert
    hole, ADR-0010 consequences): after recording snapshot A then B,
    re-recording A is a store-dedupe no-op (A's content-tagged identity
    already exists) and the read keeps serving B; reverting requires
    re-recording with any differing content. Peptide tracking IS the existing
    watch-out stream — "peptides" is not a tracked domain here.

    Args:
        domain (str): A `TRACKED_DOMAINS` member.
        tracking (dict): The snapshot per the domain's tracking table (known
            fields type-checked; extras permitted).
        on_date (str): The snapshot's YYYY-MM-DD date.
        root (str | Path): The store root.

    Raises:
        ValueError: Untracked domain, malformed date, or a mistyped known field.
    """
    if domain not in TRACKED_DOMAINS:
        raise ValueError(
            f"untracked plan domain {domain!r}; known: {TRACKED_DOMAINS}"
        )
    _check_date(on_date, "on_date")
    _TRACKING_VALIDATORS[domain](tracking)
    item = f"{_PREFIX_TRACK}{domain}"
    store.append(
        item,
        _reading(item, on_date, _content_tag(_PREFIX_TRACK, tracking), tracking),
        root=root,
    )


def resolve_plan(readings, on_date):
    """Resolve a plan item's readings to its plan-or-absence state for a date.

    Pure over the readings as `store.read` returns them (timepoint-sorted,
    append-order-stable within a timepoint). Zero readings resolve to the
    `NO_PLAN` state; readings none of which is dated `on_date` resolve to
    `NO_PLAN_TODAY` carrying the latest on-file date; otherwise the LAST
    reading in `store.read` list order dated `on_date` wins — the append
    order of DISTINCT identities (the `read_panel` reversed-scan shape): a
    correction supersedes its identity's value WITHOUT re-promoting it past
    a later-recorded same-date plan — and resolves to the plan value plus
    its specialist attribution (the source minus the ``plan::`` prefix).

    Superseded (ADR-0044-T1): ``scripts.store.plan_model.resolve_comprehensive`` is the
    canonical comprehensive resolver — it mirrors this reversed-scan latest-wins-per-date
    shape (and this three-state NO_PLAN / NO_PLAN_TODAY vocabulary) over the composite
    plan-version value. This thin ``plan::<domain>`` resolver is retained for the pre-model
    history the ADR-0044-T2 mixed-history reader still consumes (comprehensive-wins).

    Args:
        readings (list): One plan item's readings, in `store.read` order.
        on_date (str): The render date, YYYY-MM-DD.

    Returns:
        (dict) Keys `state` (`NO_PLAN` | `NO_PLAN_TODAY` | None), `plan`,
        `specialist`, and `plan_date`.
    """
    if not readings:
        return {"state": NO_PLAN, "plan": None, "specialist": None, "plan_date": None}
    for reading in reversed(readings):
        if reading["timepoint"] == on_date:
            return {
                "state": None,
                "plan": reading["value"],
                "specialist": reading["source"].removeprefix(_PREFIX_PLAN),
                "plan_date": on_date,
            }
    return {
        "state": NO_PLAN_TODAY,
        "plan": None,
        "specialist": None,
        "plan_date": max(r["timepoint"] for r in readings),
    }


def read_plan(domain, on_date, root):
    """Resolve a domain's stored plan for a date (see `resolve_plan`).

    Args:
        domain (str): A `PLAN_DOMAINS` member.
        on_date (str): The render date, YYYY-MM-DD.
        root (str | Path): The store root.

    Returns:
        (dict) The `resolve_plan` result over the domain's stored readings.

    Raises:
        ValueError: Unknown domain.
    """
    if domain not in PLAN_DOMAINS:
        raise ValueError(f"unknown plan domain {domain!r}; known: {PLAN_DOMAINS}")
    readings = plan_confirm.filter_confirmed(
        store.read(f"{_PREFIX_PLAN}{domain}", root=root), domain, root
    )
    return resolve_plan(readings, on_date)


def resolve_tracking(readings, on_date):
    """Resolve a tracking item's readings to the date's snapshot, or None.

    Pure over the readings as `store.read` returns them: the latest-appended
    snapshot dated `on_date` wins; no snapshot for the date is None (absence —
    never an invented empty snapshot).

    Args:
        readings (list): One tracking item's readings, in `store.read` order.
        on_date (str): The render date, YYYY-MM-DD.

    Returns:
        (dict | None) The snapshot value, or None.
    """
    for reading in reversed(readings):
        if reading["timepoint"] == on_date:
            return reading["value"]
    return None


def read_plan_tracking(domain, on_date, root):
    """Resolve a tracked domain's stored snapshot for a date (see `resolve_tracking`).

    Args:
        domain (str): A `TRACKED_DOMAINS` member.
        on_date (str): The render date, YYYY-MM-DD.
        root (str | Path): The store root.

    Returns:
        (dict | None) The date's latest-appended snapshot value, or None.

    Raises:
        ValueError: Untracked domain.
    """
    if domain not in TRACKED_DOMAINS:
        raise ValueError(
            f"untracked plan domain {domain!r}; known: {TRACKED_DOMAINS}"
        )
    return resolve_tracking(store.read(f"{_PREFIX_TRACK}{domain}", root=root), on_date)
