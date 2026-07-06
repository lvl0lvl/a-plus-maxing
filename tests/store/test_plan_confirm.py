"""Tests for the bounded plan-confirm pointer stream + filter_confirmed (ADR-0040-T1).

`plan_confirm` adds a `plan-confirm::<domain>` pointer stream keyed
`(domain, plan_date) -> {"decision": token}`, written through the UNCHANGED
`store.append` / `store.correct` sinks under a FIXED source tag, plus a
caller-side `filter_confirmed` pre-filter that drops any reading whose date
carries a non-`confirmed` (pending/declined) pointer. The pointer value is
bounded to `{"decision": ...}` — no plan content ever enters this
schema-relaxing stream (ADR-0040 Consequences-Negative-1). The store-adversarial
battery (bead `pka`) is a blocking gate: category (d) runs RED under two named
mutations — the namespace prefix removed, and the store dedupe key widened to
re-include `value`.
"""

from pathlib import Path

import pytest

from scripts.store import keying, plan_confirm, store

D1 = "2026-07-01"
D2 = "2026-07-02"
D3 = "2026-07-03"
D4 = "2026-07-04"


def _item_file(root, item):
    return Path(root) / f"{item}.ndjson"


def _line_count(root, item):
    path = _item_file(root, item)
    if not path.exists():
        return 0
    return len([ln for ln in path.read_text().splitlines() if ln.strip()])


def _reading_at(root, item, timepoint):
    return [r for r in store.read(item, root=root) if r["timepoint"] == timepoint][0]


# --------------------------------------------------------------------------- #
# AC-1: mark_pending appends exactly one pointer; decision_for reads it.
# --------------------------------------------------------------------------- #


def test_mark_pending_appends_one_and_decision_for_reads_it(tmp_path):
    """mark_pending writes exactly one pending pointer; decision_for resolves it."""
    plan_confirm.mark_pending("workout", D1, tmp_path)

    assert _line_count(tmp_path, "plan-confirm::workout") == 1
    assert plan_confirm.decision_for("workout", D1, tmp_path) == "pending"
    # A date with no pointer resolves to None, not a stale/other-date decision.
    assert plan_confirm.decision_for("workout", D2, tmp_path) is None


# --------------------------------------------------------------------------- #
# AC-2: set_decision supersedes via store.correct; never-stored fails loud.
# --------------------------------------------------------------------------- #


def test_set_decision_supersedes(tmp_path):
    """set_decision supersedes the pending value; the pending line never current."""
    plan_confirm.mark_pending("workout", D1, tmp_path)
    plan_confirm.set_decision("workout", D1, "confirmed", tmp_path)

    assert plan_confirm.decision_for("workout", D1, tmp_path) == "confirmed"
    # Append-only audit trail: the pending line stays on disk (2 lines), but
    # read resolves the identity to exactly one current, confirmed reading.
    assert _line_count(tmp_path, "plan-confirm::workout") == 2
    at_d1 = [r for r in store.read("plan-confirm::workout", root=tmp_path)
             if r["timepoint"] == D1]
    assert len(at_d1) == 1
    assert at_d1[0]["value"]["decision"] == "confirmed"


def test_set_decision_unstored_raises(tmp_path):
    """set_decision on a (domain, date) with no stored pointer fails loud, 0 lines."""
    with pytest.raises(ValueError):
        plan_confirm.set_decision("workout", D1, "confirmed", tmp_path)
    assert _line_count(tmp_path, "plan-confirm::workout") == 0


# --------------------------------------------------------------------------- #
# AC-3: filter_confirmed keeps no-pointer + confirmed, drops pending/declined.
# --------------------------------------------------------------------------- #


def test_filter_confirmed_drops_pending(tmp_path):
    """A pending or declined date is dropped; no-pointer and confirmed kept."""
    readings = [
        {"item": "plan::workout", "timepoint": D1, "source": "plan::coach",
         "value": {"tag": "no-ptr"}},
        {"item": "plan::workout", "timepoint": D2, "source": "plan::coach",
         "value": {"tag": "confirmed"}},
        {"item": "plan::workout", "timepoint": D3, "source": "plan::coach",
         "value": {"tag": "pending"}},
        {"item": "plan::workout", "timepoint": D4, "source": "plan::coach",
         "value": {"tag": "declined"}},
    ]
    # D1 gets no pointer; D2 confirmed; D3 pending; D4 declined.
    plan_confirm.mark_pending("workout", D2, tmp_path)
    plan_confirm.set_decision("workout", D2, "confirmed", tmp_path)
    plan_confirm.mark_pending("workout", D3, tmp_path)
    plan_confirm.mark_pending("workout", D4, tmp_path)
    plan_confirm.set_decision("workout", D4, "declined", tmp_path)

    kept = plan_confirm.filter_confirmed(readings, "workout", tmp_path)

    assert len(kept) == 2
    assert {r["timepoint"] for r in kept} == {D1, D2}
    assert D3 not in {r["timepoint"] for r in kept}  # pending dropped
    assert D4 not in {r["timepoint"] for r in kept}  # declined dropped


# --------------------------------------------------------------------------- #
# AC-4: bounded pointer value + no plan-content field names in the source.
# --------------------------------------------------------------------------- #


def test_pointer_value_bounded(tmp_path):
    """A written pointer value's keys are a subset of {"decision"} — no content."""
    plan_confirm.mark_pending("workout", D1, tmp_path)
    pending = _reading_at(tmp_path, "plan-confirm::workout", D1)
    assert set(pending["value"].keys()) <= {"decision"}

    plan_confirm.set_decision("workout", D1, "confirmed", tmp_path)
    confirmed = _reading_at(tmp_path, "plan-confirm::workout", D1)
    assert set(confirmed["value"].keys()) <= {"decision"}


def test_no_content_fields_in_source():
    """The module source carries 0 plan::-content field names (bounded stream)."""
    text = Path(plan_confirm.__file__).read_text()
    for field in ("exercises", "meals", "items", "compound"):
        assert text.count(field) == 0, f"content field {field!r} leaked into module"


# --------------------------------------------------------------------------- #
# AC-5: store-adversarial battery — (a) cross-stream, (b) same-timepoint dedupe,
# (c) correction-path boundary, (d) mutation-RED under the two named mutations.
# --------------------------------------------------------------------------- #


def test_cross_stream_disjoint(tmp_path):
    """(a) A read for one domain never returns another domain's or a bare item's."""
    # Distinct domains are disjoint item files.
    plan_confirm.mark_pending("workout", D1, tmp_path)
    plan_confirm.mark_pending("nutrition", D1, tmp_path)
    plan_confirm.set_decision("nutrition", D1, "confirmed", tmp_path)
    assert plan_confirm.decision_for("workout", D1, tmp_path) == "pending"
    assert plan_confirm.decision_for("nutrition", D1, tmp_path) == "confirmed"

    # Namespace decoy: a decision-shaped reading under the BARE item `workout`
    # must never be cross-read by decision_for (this decoy is what (d)-1 bites).
    store.append(
        "workout",
        {"item": "workout", "timepoint": D2, "source": "decoy",
         "value": {"decision": "confirmed"}},
        root=tmp_path,
    )
    assert plan_confirm.decision_for("workout", D2, tmp_path) is None


def test_same_timepoint_two_sources_persist(tmp_path):
    """(b) Two distinct-source writes at one (item, timepoint) persist; re-write no-op."""
    item = "plan-confirm::workout"
    store.append(item, {"item": item, "timepoint": D1, "source": "s1",
                        "value": {"decision": "pending"}}, root=tmp_path)
    store.append(item, {"item": item, "timepoint": D1, "source": "s2",
                        "value": {"decision": "confirmed"}}, root=tmp_path)
    assert len(store.read(item, root=tmp_path)) == 2

    before = _line_count(tmp_path, item)
    # Identical (item, timepoint, source) re-write is an idempotent no-op.
    store.append(item, {"item": item, "timepoint": D1, "source": "s1",
                        "value": {"decision": "pending"}}, root=tmp_path)
    assert _line_count(tmp_path, item) == before


def test_correction_path_boundary(tmp_path):
    """(c) Idempotent re-set, superseded-not-current, fail-loud, cross-stream isolation."""
    plan_confirm.mark_pending("workout", D1, tmp_path)
    plan_confirm.set_decision("workout", D1, "confirmed", tmp_path)

    # Re-running the same decision appends 0 lines (idempotent correction).
    n = _line_count(tmp_path, "plan-confirm::workout")
    plan_confirm.set_decision("workout", D1, "confirmed", tmp_path)
    assert _line_count(tmp_path, "plan-confirm::workout") == n
    # A superseded pending never renders current.
    assert plan_confirm.decision_for("workout", D1, tmp_path) == "confirmed"

    # A set_decision on a never-stored (domain, date) fails loud.
    with pytest.raises(ValueError):
        plan_confirm.set_decision("workout", D2, "confirmed", tmp_path)

    # A correction on workout never surfaces in the nutrition stream.
    plan_confirm.mark_pending("nutrition", D1, tmp_path)
    plan_confirm.set_decision("workout", D1, "declined", tmp_path)
    assert plan_confirm.decision_for("nutrition", D1, tmp_path) == "pending"


def test_mutation_prefix_removed_breaks_cross_stream(tmp_path, monkeypatch):
    """(d)-1 Removing _PREFIX_CONFIRM turns the cross-stream guard RED.

    The bare-item decoy is shielded ONLY by the namespace prefix. With the real
    prefix, decision_for ignores it (None); mutated to "", decision_for reads the
    bare item and surfaces the decoy — the exact RED that test_cross_stream_disjoint
    would show. If decision_for did not depend on the prefix, the baseline None
    assertion would already fail, so this is not tautological.
    """
    store.append(
        "workout",
        {"item": "workout", "timepoint": D1, "source": "decoy",
         "value": {"decision": "confirmed"}},
        root=tmp_path,
    )
    assert plan_confirm.decision_for("workout", D1, tmp_path) is None

    monkeypatch.setattr(plan_confirm, "_PREFIX_CONFIRM", "")
    assert plan_confirm.decision_for("workout", D1, tmp_path) == "confirmed"


def test_mutation_dedupe_widened_breaks_supersede(tmp_path, monkeypatch):
    """(d)-2 Widening the store dedupe key to include value breaks set_decision.

    With value in the dedupe identity, store.correct can no longer match the
    stored pending line to supersede it (pending value != the new value → a
    different identity → fails loud). This is the exact RED that
    test_set_decision_supersedes would show. The lever is DEDUPE_FIELDS directly
    (patching _DEDUPE_EXCLUDED is inert — DEDUPE_FIELDS is import-frozen from it).
    """
    # Baseline: supersede works with the real (value-excluded) dedupe key.
    plan_confirm.mark_pending("workout", D1, tmp_path)
    plan_confirm.set_decision("workout", D1, "confirmed", tmp_path)
    assert plan_confirm.decision_for("workout", D1, tmp_path) == "confirmed"

    # Fresh pending on a new date, then widen the dedupe key to include value.
    plan_confirm.mark_pending("workout", D2, tmp_path)
    monkeypatch.setattr(keying, "DEDUPE_FIELDS", keying.LINE_FIELDS)
    with pytest.raises((ValueError, TypeError)):
        plan_confirm.set_decision("workout", D2, "confirmed", tmp_path)
