"""The comprehensive Plan Model — ONE composite object per plan version (ADR-0044-T1).

This is the canonical plan-model store: per active domain the seven-field
DOMAIN PROGRAM intact (validated via ``scripts.plan.domain_program``), plus an
integrated narrative, dated milestones, a compiled monitoring config, and plan-level
adjustment rules — assembled into ONE composite VALUE per plan version. It SUPERSEDES
the thin ``plan_schema`` record spine (``record_plan`` / ``resolve_plan``) as the
strategic plan-storage mechanism; the thin ``plan::<domain>`` streams are retained for
the ADR-0044-T2 mixed-history reader (comprehensive-wins) during the transition.

The value rides the FROZEN primitive (disposition #14)
-------------------------------------------------------
The comprehensive plan is a richer VALUE, not a new store primitive. The record path
appends through the UNCHANGED ``store.append(item, reading, root)`` and reuses keying's
frozen ``(item, timepoint, source)`` dedupe identity with ``value`` EXCLUDED:

    item       a FIXED ``plan-model::`` namespace, disjoint from ``plan::`` /
               ``plan-track::``. All versions accrue under this one item; a version is
               distinguished by its timepoint + a content-tag version-key source.
    timepoint  the version's declared YYYY-MM-DD date. Date EQUALITY is the standing-
               resolution mechanism, so a malformed date fails loud at the writer.
    source     a content-tag over the composite value (loop_schema._content_tag): two
               DISTINCT versions at one timepoint get distinct sources and both persist;
               an identical re-record hashes to the same tag -> an idempotent store no-op.
    value      the composite version object.

This module defines NO second dedupe key and reimplements no store I/O — the identity is
reached ONLY through ``store.append`` / ``store.read``. There is no ``store.correct``:
plan-model versions are append-only, a revision is a new version. A CHANGED value at
the same ``(item, timepoint, source)`` is a store-dedupe no-op (never a silent overwrite).

Revert hole (ADR-0010 consequences, mirroring ``plan_schema.record_plan_tracking``): once a
later version supersedes an earlier one, re-recording the earlier version is a store-dedupe
no-op (its content-tagged identity already exists), so a superseded version is not restorable
by re-recording — a new forward-dated version is the supported revert path.

Fail-closed conformance
-----------------------
``validate_plan_version`` is the fail-fast boundary: a version missing a domain program /
narrative / milestones / monitoring config, or carrying a per-domain program that
``domain_program.validate`` rejects, raises ``PlanVersionError`` naming the offending
element — never a silent thin fallback, and a partial version is never stored.

Crown-jewel de-id: this module sits DOWNSTREAM of the frozen ``context_assembler``
boundary. It stores specialist/orchestrator PLAN OUTPUT (identity-free by construction) —
no genetics channel, no new carried-identity field.
"""

import datetime
import re

from scripts.plan import domain_program
from scripts.store import store
from scripts.store.loop_schema import _content_tag, _reading

# The plan-version stream's item namespace. The prefix IS the item id: the
# "::" separator is not a path separator, so it stays a direct child of the store root.
_PREFIX_MODEL = "plan-model::"

# The two published absence states, mirroring plan_schema's three-state read vocabulary.
NO_PLAN = "no-plan"
NO_PLAN_TODAY = "no-plan-today"

# Composite version field names — the stable seam every downstream consumer reads.
# (Plan-level ``adjustment_rules`` is a first-class composite element too, but rides as a
# value key: it round-trips without a validate-required check, per the ADR-0044-T1 recipe.)
VERSION_DATE = "date"
DOMAIN_PROGRAMS = "domain_programs"
NARRATIVE = "narrative"
MILESTONES = "milestones"
MONITORING_CONFIG = "monitoring_config"

# Date-only timepoints by contract: date EQUALITY drives standing resolution, so a
# malformed date can never equal a render date and would read absent forever — rejected
# at the writer boundary (mirrors plan_schema._check_date's posture).
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


class PlanVersionError(Exception):
    """The single typed rejection channel for a non-conformant plan version.

    Attributes:
        offending_element (str | None): The missing/malformed version element — a top-level
            element name, or ``domain_programs[<name>]`` for a non-conformant per-domain
            program.
    """

    def __init__(self, message="", *, offending_element=None):
        super().__init__(message)
        self.offending_element = offending_element


def _check_date(value, what):
    """Reject a timepoint that is not a real YYYY-MM-DD calendar date.

    Args:
        value: The candidate date string.
        what (str): The element name for the error message.

    Raises:
        PlanVersionError: `value` is not a YYYY-MM-DD string naming a real date.
    """
    if not isinstance(value, str) or not _DATE_RE.fullmatch(value):
        raise PlanVersionError(
            f"version {what!r} {value!r} is not a YYYY-MM-DD date", offending_element=what
        )
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        raise PlanVersionError(
            f"version {what!r} {value!r} is not a real calendar date", offending_element=what
        ) from None


def validate_plan_version(version):
    """Raise `PlanVersionError` unless `version` is a conformant plan version.

    Fail-closed on the model-level required elements: at least one per-domain program (each
    passing `domain_program.validate`), a non-empty narrative, at least one dated milestone,
    and a well-typed monitoring config. A partial or non-conformant version raises a typed
    error naming the offending element — never a silent thin fallback.

    Args:
        version (Mapping): The composite plan version.

    Raises:
        PlanVersionError: The version is not a mapping, is missing a required element, or
            carries a per-domain program `domain_program.validate` rejects.
    """
    if not isinstance(version, dict):
        raise PlanVersionError(
            f"version is not a mapping (got {type(version).__name__})",
            offending_element="version",
        )

    programs = version.get(DOMAIN_PROGRAMS)
    if not isinstance(programs, dict) or not programs:
        raise PlanVersionError(
            f"version missing required element {DOMAIN_PROGRAMS!r} (>=1 domain program)",
            offending_element=DOMAIN_PROGRAMS,
        )
    for name, program in programs.items():
        try:
            domain_program.validate(program)
        except domain_program.DomainProgramError as exc:
            raise PlanVersionError(
                f"{DOMAIN_PROGRAMS}[{name!r}] is a non-conformant domain program: {exc}",
                offending_element=f"{DOMAIN_PROGRAMS}[{name!r}]",
            ) from exc

    narrative = version.get(NARRATIVE)
    if not isinstance(narrative, str) or not narrative:
        raise PlanVersionError(
            f"version missing required element {NARRATIVE!r} (a non-empty str)",
            offending_element=NARRATIVE,
        )

    milestones = version.get(MILESTONES)
    if not isinstance(milestones, list) or not milestones:
        raise PlanVersionError(
            f"version missing required element {MILESTONES!r} (>=1 dated milestone)",
            offending_element=MILESTONES,
        )
    for i, milestone in enumerate(milestones):
        if not isinstance(milestone, dict) or "date" not in milestone:
            raise PlanVersionError(
                f"version element {MILESTONES!r} carries an undated milestone",
                offending_element=MILESTONES,
            )
        _check_date(milestone["date"], f"{MILESTONES}[{i}].date")

    if not isinstance(version.get(MONITORING_CONFIG), dict) or not version.get(MONITORING_CONFIG):
        raise PlanVersionError(
            f"version missing required element {MONITORING_CONFIG!r} (a non-empty mapping)",
            offending_element=MONITORING_CONFIG,
        )


def record_plan_version(version, root):
    """Record one plan version — the value rides the frozen `store.append`.

    Validates the composite fail-closed FIRST (per-domain `domain_program.validate` + the
    model-level required-element check + a real declared date), then appends ONE reading via
    the UNCHANGED `store.append`: item = the fixed `plan-model::` namespace, timepoint = the
    version's declared date, source = the content-tag version key, value = the composite.

    Inherits the store dedupe: two DISTINCT versions at one timepoint both persist (distinct
    version keys); an identical re-record is an idempotent no-op; a CHANGED value at the same
    `(item, timepoint, source)` is a store-dedupe no-op, never a silent overwrite.

    Args:
        version (Mapping): The composite plan version.
        root (str | Path): The store root.

    Raises:
        PlanVersionError: The version is partial, non-conformant, or carries a bad date.
    """
    validate_plan_version(version)
    _check_date(version.get(VERSION_DATE), VERSION_DATE)
    store.append(
        _PREFIX_MODEL,
        _reading(_PREFIX_MODEL, version[VERSION_DATE], _content_tag(_PREFIX_MODEL, version), version),
        root=root,
    )


def resolve_comprehensive(readings, on_date):
    """Resolve a plan-model item's readings to its standing-or-absence state for a date.

    Pure over the readings as `store.read` returns them (timepoint-sorted, append-order-stable
    within a timepoint), mirroring `plan_schema.resolve_plan`'s reversed-scan latest-wins shape
    over the composite value: zero readings resolve to `NO_PLAN`; readings none of which is dated
    `on_date` resolve to `NO_PLAN_TODAY` carrying the latest on-file date; otherwise the LAST
    reading in file (append) order dated `on_date` wins — a STANDING state carrying the composite.

    Args:
        readings (list): One plan-model item's readings, in `store.read` order.
        on_date (str): The render date, YYYY-MM-DD.

    Returns:
        (dict) Keys `state` (`NO_PLAN` | `NO_PLAN_TODAY` | None), `version`, and `plan_date`.
    """
    if not readings:
        return {"state": NO_PLAN, "version": None, "plan_date": None}
    for reading in reversed(readings):
        if reading["timepoint"] == on_date:
            return {"state": None, "version": reading["value"], "plan_date": on_date}
    return {
        "state": NO_PLAN_TODAY,
        "version": None,
        "plan_date": max(reading["timepoint"] for reading in readings),
    }


def read_plan_version(on_date, root):
    """Resolve the stored plan version for a date (see `resolve_comprehensive`).

    Args:
        on_date (str): The render date, YYYY-MM-DD.
        root (str | Path): The store root.

    Returns:
        (dict) The `resolve_comprehensive` result over the `plan-model::` item's readings.
    """
    return resolve_comprehensive(store.read(_PREFIX_MODEL, root=root), on_date)
