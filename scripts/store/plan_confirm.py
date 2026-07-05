"""Bounded plan-confirm pointer stream + caller-side confirmation pre-filter.

A `plan-confirm::<domain>` pointer stream carries exactly ONE decision per
`(domain, plan_date)` — `pending`, `confirmed`, or `declined` — written through
the UNCHANGED `store.append` / `store.correct` sinks under a FIXED source tag.
The pointer VALUE is bounded to `{"decision": <token>}`: no plan content ever
enters this schema-relaxing stream (ADR-0040 Consequences-Negative-1 — an
unbounded value would smuggle plan content into the pointer, a one-way door).

The fixed source tag is load-bearing. There is one pointer per
`(domain, plan_date)`, and `set_decision`'s supersede requires the SAME
`(item, timepoint, source)` identity to already be stored; a content-tagged
source (as `plan-track::` uses) would hash `pending` and `confirmed` to
different tags, so `store.correct` could never find the pending line to flip.

`filter_confirmed` is the caller-side pre-filter: it drops any reading whose
date carries a non-`confirmed` (pending/declined) pointer, keeping no-pointer
and confirmed readings unchanged. Every decision is resolved through the single
`decision_for` path — the store is never re-scanned inline.

This module imports `scripts.store.store` ONLY: ADR-0040-T2 makes
`plan_schema.read_plan` import this module, so a reverse import would cycle.
"""

from scripts.store import store

DECISION_PENDING = "pending"
DECISION_CONFIRMED = "confirmed"
DECISION_DECLINED = "declined"

# Item-namespace prefix for the pointer stream. Read at call time, so removing
# it is the (d)-1 mutation the cross-stream test reddens.
_PREFIX_CONFIRM = "plan-confirm::"

# FIXED source tag (not a content tag): one pointer per (domain, plan_date), so
# pending and its later decision share an identity store.correct can supersede.
_SOURCE = "plan-confirm"


def _item(domain):
    return f"{_PREFIX_CONFIRM}{domain}"


def mark_pending(domain, plan_date, root):
    """Append one pending pointer for a domain and plan date.

    Args:
        domain (str): The plan domain the pointer namespaces.
        plan_date (str): The plan's YYYY-MM-DD date (the pointer timepoint).
        root (str | Path): The store root.
    """
    item = _item(domain)
    store.append(
        item,
        {"item": item, "timepoint": plan_date, "source": _SOURCE,
         "value": {"decision": DECISION_PENDING}},
        root=root,
    )


def set_decision(domain, plan_date, decision, root):
    """Supersede a stored pointer's decision via `store.correct`.

    `store.correct` raises `ValueError` on a `(domain, plan_date)` with no stored
    pointer, so a decision on a never-marked date fails loud with no extra guard.

    Args:
        domain (str): The plan domain the pointer namespaces.
        plan_date (str): The plan's YYYY-MM-DD date (the pointer timepoint).
        decision (str): The new decision token.
        root (str | Path): The store root.

    Raises:
        ValueError: No pointer is stored for `(domain, plan_date)`.
    """
    item = _item(domain)
    store.correct(
        item,
        {"item": item, "timepoint": plan_date, "source": _SOURCE,
         "value": {"decision": decision}},
        root=root,
    )


def decision_for(domain, plan_date, root):
    """Return the current decision for a `(domain, plan_date)`, or None.

    Args:
        domain (str): The plan domain the pointer namespaces.
        plan_date (str): The plan's YYYY-MM-DD date (the pointer timepoint).
        root (str | Path): The store root.

    Returns:
        (str | None) The stored decision token, or None when no pointer exists.
    """
    for reading in store.read(_item(domain), root=root):
        if reading["timepoint"] == plan_date:
            return reading["value"]["decision"]
    return None


def filter_confirmed(readings, domain, root):
    """Drop readings whose date carries a non-`confirmed` pointer.

    Keeps a reading whose date has no pointer or a `confirmed` pointer; drops one
    whose date has a `pending` or `declined` pointer. Each reading's decision is
    resolved through `decision_for` (no inline re-scan of the store).

    Args:
        readings (list): Readings carrying a `timepoint` field.
        domain (str): The plan domain whose pointer stream gates the readings.
        root (str | Path): The store root.

    Returns:
        (list) The readings minus any whose date carries a non-confirmed pointer.
    """
    return [
        reading
        for reading in readings
        if decision_for(domain, reading["timepoint"], root)
        in (None, DECISION_CONFIRMED)
    ]
