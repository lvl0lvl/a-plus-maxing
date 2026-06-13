"""Goal-progress store schema (dashboard zone 6 — Goals & Progress).

Records operator goals as one per-goal store stream and reads each back as its
current progress percent. Every write goes THROUGH ``scripts.store.store``
(``append`` / ``correct``) keyed by the one ``scripts.store.keying`` Line Field
Set, and reuses loop_schema's reading constructor — this module defines no
second key and reimplements no store I/O. A goal's percent is DERIVED from its
``(baseline, current, target)`` on read, never stored, so the dashboard renders
progress under the ADR-0009 honesty rule (no fabricated percent; absence renders
the awaiting state). All persistence is local file I/O; 0 model-bound send.

Stream (one disjoint item namespace):
    goal::<slug>   one progress stream per goal; timepoint = the snapshot's
                   YYYY-MM-DD date; source = a constant tag; value = the goal
                   dict ``{label, baseline, current, target[, unit]}``. The
                   latest-dated snapshot is the goal's current state; a same-date
                   re-record is an idempotent no-op (an intended revision goes
                   through ``correct_goal``). The ``::`` separator is not a path
                   separator, so a prefixed id stays a direct child of the store
                   root (``store._item_path`` guard).

percent (read-derived, never stored):
    clamp((current - baseline) / (target - baseline), 0, 1) * 100 — the
    direction-agnostic progress fraction (target above OR below baseline),
    FLOORED at 0 (a regression past the start reads 0% progress, never negative)
    and CEILED at 100 (overshoot reads complete, never > 100). ``baseline`` ==
    ``target`` is rejected at the writer (no progress span to measure across, and
    the division would be undefined); ``label`` is a required non-empty str and
    ``baseline``/``current``/``target`` are required numbers, so a stored goal
    always resolves to an honest 0-100 percent. The value is closed on its
    required fields and open on extras (the ADR-0006-T2 forward-compatibility
    seam): unknown extra keys are permitted and ignored. Writers raise only
    ValueError; readers never raise on absence.
"""

import datetime
import re

from scripts.store import store
from scripts.store.loop_schema import _reading

# Per-stream item-id prefix; the constant source tag every goal snapshot carries
# (one goal per slug, so the source needs no content discriminator — a same
# (slug, date) re-record is an idempotent dedupe no-op, a revision is a
# `correct_goal`).
_PREFIX_GOAL = "goal::"
_TAG_GOAL = "goal-progress"

# Day-keyed timepoints are date-only by contract: a malformed date would sort
# wrong under the store's lexicographic timepoint order (so the wrong snapshot
# could win the latest-wins read) and render a meaningless "as of" — rejected at
# the writer boundary instead (the plan_schema._check_date pattern).
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _is_number(value):
    """Report whether `value` is an int or float (bool excluded — not a measure)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_nonempty_str(value):
    """Report whether `value` is a non-empty str."""
    return isinstance(value, str) and value != ""


def _check_date(value, what):
    """Reject a timepoint that is not a real YYYY-MM-DD calendar date.

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


def _check_goal_value(goal):
    """Validate a goal document against its schema, closed-required/open-extras.

    Raises:
        ValueError: `goal` is not a dict, a required field is missing or
            mistyped, `unit` is present but not a str, or baseline == target
            (no progress span to measure, and the percent would be undefined).
    """
    if not isinstance(goal, dict):
        raise ValueError(f"goal must be a dict, got {type(goal).__name__}")
    if not _is_nonempty_str(goal.get("label")):
        raise ValueError("goal field 'label' must be a non-empty str")
    for field in ("baseline", "current", "target"):
        if field not in goal:
            raise ValueError(f"goal missing required field {field!r}")
        if not _is_number(goal[field]):
            raise ValueError(f"goal field {field!r} must be a number")
    if "unit" in goal and not isinstance(goal["unit"], str):
        raise ValueError("goal field 'unit' must be a str")
    if goal["baseline"] == goal["target"]:
        raise ValueError(
            "goal 'baseline' and 'target' must differ (no progress span to measure)"
        )


def _check_goal_args(slug, goal, on_date):
    """Validate the shared record/correct goal-writer arguments.

    Raises:
        ValueError: Empty/non-str slug, malformed date, or a goal failing its
            schema.
    """
    if not _is_nonempty_str(slug):
        raise ValueError(f"slug must be a non-empty str, got {slug!r}")
    _check_date(on_date, "on_date")
    _check_goal_value(goal)


def _percent(baseline, current, target):
    """Return the progress percent toward target, direction-agnostic, 0-100.

    The fraction of the way from `baseline` to `target` the `current` value has
    moved. `baseline` != `target` is a writer invariant, so the denominator is
    never 0 for a stored goal. 100.0 is returned ONLY at true completion
    (`current` reaching/passing `target`) and 0.0 only at/below `baseline`; a
    sub-completion fraction never ROUNDS UP to a false "100%" (99.95% reads 99.9)
    — the ADR-0009 no-fabricated-completion rule.
    """
    fraction = (current - baseline) / (target - baseline)
    if fraction >= 1:
        return 100.0
    if fraction <= 0:
        return 0.0
    return min(99.9, round(fraction * 100, 1))


def record_goal(slug, goal, on_date, root):
    """Record one goal-progress snapshot for a goal slug and date.

    Appends exactly one reading via `store.append`: item ``goal::<slug>``,
    timepoint = `on_date`, source = the constant goal tag, value = `goal`.
    Inherits the store dedupe: re-recording a CHANGED value for a stored
    (slug, date) identity is a no-op — never a silent overwrite; an intended
    value change goes through `correct_goal`.

    Args:
        slug (str): The goal's stable identifier (non-empty).
        goal (dict): The goal per the value schema (closed on required fields,
            open on extras): `label`, `baseline`, `current`, `target`, and an
            optional `unit`.
        on_date (str): The snapshot's YYYY-MM-DD date.
        root (str | Path): The store root.

    Raises:
        ValueError: Empty slug, malformed date, or a missing/mistyped/degenerate
            schema field.
    """
    _check_goal_args(slug, goal, on_date)
    item = f"{_PREFIX_GOAL}{slug}"
    store.append(item, _reading(item, on_date, _TAG_GOAL, goal), root=root)


def correct_goal(slug, goal, on_date, root):
    """Supersede an already-stored goal snapshot's value via `store.correct`.

    Same validation as `record_goal`; the (slug, date) identity must already be
    stored — a mistyped correction fails loud instead of silently creating a new
    snapshot. The prior lines' logical content stays in the file (append-only
    audit trail); every read resolves to this value.

    Args:
        slug (str): The goal's stable identifier (non-empty).
        goal (dict): The superseding goal per the value schema.
        on_date (str): The snapshot's YYYY-MM-DD date.
        root (str | Path): The store root.

    Raises:
        ValueError: A `record_goal` validation failure, or no stored reading
            carries the (slug, date) identity.
    """
    _check_goal_args(slug, goal, on_date)
    item = f"{_PREFIX_GOAL}{slug}"
    store.correct(item, _reading(item, on_date, _TAG_GOAL, goal), root=root)


def resolve_goal(readings):
    """Resolve a goal item's readings to its current progress, or None if absent.

    Pure over the readings as `store.read` returns them. Zero readings resolve to
    None (absence — the dashboard renders the awaiting state, never an invented
    percent). Otherwise the snapshot with the latest timepoint wins
    (order-independent — `max` by timepoint, not a positional assumption) and
    resolves to its label, derived percent, and the raw baseline/current/target
    plus the optional unit and the snapshot date.

    Args:
        readings (list): One goal item's readings, in `store.read` order.

    Returns:
        (dict | None) Keys `label`, `percent`, `baseline`, `current`, `target`,
        `unit`, `on_date`; or None when `readings` is empty.
    """
    if not readings:
        return None
    latest = max(readings, key=lambda r: r["timepoint"])
    goal = latest["value"]
    return {
        "label": goal["label"],
        "percent": _percent(goal["baseline"], goal["current"], goal["target"]),
        "baseline": goal["baseline"],
        "current": goal["current"],
        "target": goal["target"],
        "unit": goal.get("unit"),
        "on_date": latest["timepoint"],
    }


def read_goal(slug, root):
    """Resolve a single goal's stored progress (see `resolve_goal`).

    Args:
        slug (str): The goal's stable identifier (non-empty).
        root (str | Path): The store root.

    Returns:
        (dict | None) The `resolve_goal` result over the goal's stored readings.

    Raises:
        ValueError: Empty/non-str slug.
    """
    if not _is_nonempty_str(slug):
        raise ValueError(f"slug must be a non-empty str, got {slug!r}")
    return resolve_goal(store.read(f"{_PREFIX_GOAL}{slug}", root=root))


def read_goals(root):
    """Resolve every stored goal's current progress, in slug order.

    Enumerates the store's ``goal::`` items via `store.items` (the single
    enumeration owner — no consumer walks the on-disk layout) and resolves each.
    A goal item whose every line is corrupted resolves to None and is skipped
    (honest absence), so a goal appears only when it has a readable snapshot.

    Args:
        root (str | Path): The store root.

    Returns:
        (list) (slug, resolved) pairs in store-item (lexicographic) order.
    """
    out = []
    for item in store.items(root):
        if item.startswith(_PREFIX_GOAL):
            resolved = resolve_goal(store.read(item, root=root))
            if resolved is not None:
                out.append((item[len(_PREFIX_GOAL):], resolved))
    return out
