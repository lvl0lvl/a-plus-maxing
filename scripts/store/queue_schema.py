"""Doctor-visit-queue store schema (the medical-liaison's collation surface).

The medical-liaison owns the doctor-visit queue: the severity-ranked, source-attributed set of
safety findings the operator brings to the MD visit (medical-liaison design §2.2, §9.4). The
plan-generation pipeline's adjudicated safety findings — the additive-AE, cross-domain-conflict,
and supplement-Rx BPMH outcomes, each cleared-via-override or block-stands — are collated into
this stream by `scripts.plan.orchestrate.collate_doctor_visit_queue`. The rendered SBAR handout
(the one-page artifact) reads this stream; the render itself is a separate design-led surface.

Stream (a disjoint item namespace, like `plan::`/`plan-track::`):
    dvq::queue   the cumulative doctor-visit queue; timepoint = the collation date; source =
                 the safety finding's `finding_id` (the natural per-finding key — distinct
                 findings persist as distinct entries; an identical re-record at the same date
                 is an idempotent no-op; a re-collation on a LATER date appends a fresh entry
                 and `resolve_doctor_visit_queue` keeps the latest per finding_id); value = the
                 queue-entry dict.

Every write goes THROUGH `scripts.store.store.append` keyed by the one `scripts.store.keying`
Line Field Set; this module defines no second key and reimplements no store I/O. All persistence
is local file I/O; 0 model-bound send. Writers raise only ValueError; readers never raise on
absence. Entries are closed on the `finding_id` requirement and open on extras (the liaison adds
GRADE annotations at its dispatch).
"""

import datetime
import re

from scripts.store import store
from scripts.store.loop_schema import _reading

# Day-keyed timepoints are dashed-date-only by contract: date EQUALITY against the render date is
# the resolution mechanism, and `datetime.date.fromisoformat` also accepts the basic-ISO `YYYYMMDD`
# form (Python 3.11+), which would never equal a dashed render date — so require the dashed shape
# explicitly (the `plan_schema._DATE_RE` precedent) on top of the calendar-validity check.
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")

# The queue's single item-id. "dvq::" is the namespace prefix (disjoint from plan::/plan-track::/
# panel::/watch-out::/biomarker::/feedback::), so a read for the queue cannot cross-read another
# stream — the cross-stream namespacing the S41 `read_panel` escape made mandatory.
_PREFIX_DVQ = "dvq::"
_ITEM = "dvq::queue"

# Severity-rank tiers (lower = higher priority = surfaced first to the MD). A non-overridable
# auto-block (CRITICAL / H1-H2 — the vitamin-K/warfarin watchlist class) ranks above any
# overridable band; HIGH above MEDIUM; an unknown band last. The §9.4 "watchlist-high-first"
# discipline is captured at the data layer by the non-overridable tier leading the order.
_BAND_RANK = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
_UNKNOWN_BAND_TIER = 3


def _check_date(value):
    """Reject a timepoint that is not a real YYYY-MM-DD calendar date (writer-boundary, fail-loud).

    A malformed date can never equal a render/collation date downstream, so an entry under one
    would silently never surface — rejected here instead (the `plan_schema` boundary precedent).
    """
    if not isinstance(value, str):
        raise ValueError(
            f"doctor-visit-queue date must be a string, got {type(value).__name__}"
        )
    if not _DATE_RE.match(value):
        raise ValueError(
            f"doctor-visit-queue date {value!r} is not a dashed YYYY-MM-DD date"
        )
    try:
        datetime.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"doctor-visit-queue date {value!r} is not a real YYYY-MM-DD calendar date"
        ) from exc


def record_doctor_visit_queue_entry(entry, on_date, root):
    """Append one safety finding to the doctor-visit queue.

    Item `dvq::queue`, timepoint `on_date`, source = the entry's `finding_id` (the per-finding
    key — distinct findings persist, an identical same-date re-record is an idempotent no-op),
    value = the entry dict. A finding re-collated on a LATER date appends a fresh entry;
    `resolve_doctor_visit_queue` keeps the latest per finding_id.

    Args:
        entry (dict): The queue entry; MUST carry a non-empty string `finding_id`.
        on_date (str): The collation date, YYYY-MM-DD.
        root (str | Path): The store root.

    Raises:
        ValueError: A malformed date, or an entry with no non-empty string `finding_id`.
    """
    _check_date(on_date)
    finding_id = entry.get("finding_id")
    if not isinstance(finding_id, str) or not finding_id.strip():
        raise ValueError(
            "doctor-visit-queue entry must carry a non-empty string finding_id"
        )
    store.append(_ITEM, _reading(_ITEM, on_date, finding_id, entry), root=root)


def _severity_rank(entry):
    """The sort key for a queue entry: (outcome tier, band rank, finding_id) — lower first.

    Outcome tier leads, because a finding's DISPOSITION outranks its band on the MD handout:
        0 — a non-overridable auto-block (CRITICAL / H1-H2): the operator CANNOT proceed; most urgent.
        1 — a block-stands overridable finding (an open concern the override did NOT clear, e.g. a
            vacuous/invalid override): an UNRESOLVED safety concern the doctor must still address.
        2 — a cleared-with-override finding: the operator proceeded with informed consent; the doctor
            should know, but it is lower priority than an unresolved concern.
    An UNRESOLVED block-stands must never rank below a RESOLVED cleared finding (the safety-ordering
    inversion this fixes). Band (CRITICAL>HIGH>MEDIUM>unknown) is the secondary key within a tier; the
    finding_id is the tertiary key so the order is deterministic.
    """
    if bool(entry.get("non_overridable")):
        outcome_tier = 0
    elif entry.get("outcome") == "block-stands":
        outcome_tier = 1
    else:
        outcome_tier = 2
    band_rank = _BAND_RANK.get(entry.get("composite_band"), _UNKNOWN_BAND_TIER)
    return (outcome_tier, band_rank, str(entry.get("finding_id")))


def resolve_doctor_visit_queue(readings):
    """Resolve the cumulative doctor-visit queue: the latest entry per finding_id, severity-ranked.

    Pure over the readings as `store.read` returns them (timepoint-sorted, append-order-stable
    within a timepoint). Each finding_id's LATEST record (last in read order) is its current
    entry; the entries are returned severity-ranked (a non-overridable auto-block first, then
    HIGH, then MEDIUM, then an unknown band; ties broken by finding_id). Zero readings → `[]`
    (an empty queue — never an invented entry).

    Args:
        readings (list): The `dvq::queue` readings, in `store.read` order.

    Returns:
        (list) The current queue entries (each a recorded entry dict), severity-ranked.
    """
    latest = {}
    for reading in readings:
        latest[reading["source"]] = reading["value"]  # later record wins per finding_id (source)
    return sorted(latest.values(), key=_severity_rank)


def read_doctor_visit_queue(root):
    """Resolve the stored doctor-visit queue (see `resolve_doctor_visit_queue`).

    Args:
        root (str | Path): The store root.

    Returns:
        (list) The severity-ranked current queue (possibly empty).
    """
    return resolve_doctor_visit_queue(store.read(_ITEM, root=root))
