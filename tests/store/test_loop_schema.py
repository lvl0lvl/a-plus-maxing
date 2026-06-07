"""Tests for scripts/store/loop_schema.py — lab-loop / watch-out / physician-feedback store schemas.

The schemas write THROUGH scripts/store/store.py (append/read) and the keying.py
Line Field Set; they define no second key and reimplement no store I/O. This suite
asserts the four published store states (pending / not-yet-answered / no-prior /
answered-over-time) with adversarial no-fabrication and drop-fails-the-test
directions, the 0-automated-detection NG-6 floor, and the egress boundary over a
real store/read cycle.
"""

import re
import socket
from pathlib import Path

from scripts.guard.egress_guard import run as egress_run
from scripts.store import keying, loop_schema

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "scripts" / "store" / "loop_schema.py"

# The NG-6 0-automated-detection floor pattern, verbatim from the recipe's
# `rg -n "threshold|detect|evaluat|alert|trigger|abnormal|out.of.range|flag.*signal"`.
NG6_PATTERN = re.compile(
    r"threshold|detect|evaluat|alert|trigger|abnormal|out.of.range|flag.*signal"
)


def _ng6_match_count():
    """Count source lines matching the NG-6 automated-detection pattern (rg-equivalent)."""
    return sum(
        1 for line in SOURCE.read_text().splitlines() if NG6_PATTERN.search(line)
    )


# --- Cycle 1: store-state schema + question derivation + 0-automation floor ---


def test_pending_panel_persists_never_result(tmp_path):
    """AC-1: a recommended-but-undrawn panel reads "pending" across a LATER generation.

    Adversarial: a re-read on a later generation that returns a fabricated result
    (a value / "clear" / absent state) instead of "pending" turns this RED.
    """
    loop_schema.record_pending_panel(
        "lipid_panel", "2026-06-01T08:00:00+00:00", root=tmp_path
    )

    # Re-read on a LATER generation cycle — a distinct later read, no result appended
    # in between. The panel must STILL be pending, not a fabricated result.
    state = loop_schema.read_panel("lipid_panel", root=tmp_path)
    assert state == loop_schema.PENDING
    assert state != "clear"
    assert state is not None  # never an absent state


def test_unanswered_reads_not_yet_answered(tmp_path):
    """AC-2(a): an unanswered watch-out reads "not-yet-answered", never clear/absent."""
    state = loop_schema.read_watchout("sleep_quality", root=tmp_path)
    assert state == loop_schema.NOT_YET_ANSWERED
    assert state != "clear"
    assert state is not None  # never an absent result


def test_single_timepoint_reads_no_prior(tmp_path):
    """AC-2(b): a biomarker with exactly ONE timepoint reads "no-prior".

    Adversarial: a read that fabricates a trend/delta/projection from a single
    point turns this RED.
    """
    loop_schema.record_biomarker(
        "ferritin", "2026-06-01T08:00:00+00:00", 45, root=tmp_path
    )

    result = loop_schema.read_biomarker("ferritin", root=tmp_path)
    assert result["state"] == loop_schema.NO_PRIOR
    assert len(result["timepoints"]) == 1
    # No fabricated trend/delta/projection over one point.
    assert "trend" not in result
    assert "delta" not in result
    assert "projection" not in result


def test_two_timepoints_not_no_prior(tmp_path):
    """AC-2(b) boundary: ≥2 timepoints are NOT no-prior; readings returned as-is."""
    loop_schema.record_biomarker(
        "ferritin", "2026-06-01T08:00:00+00:00", 45, root=tmp_path
    )
    loop_schema.record_biomarker(
        "ferritin", "2026-06-08T08:00:00+00:00", 52, root=tmp_path
    )

    result = loop_schema.read_biomarker("ferritin", root=tmp_path)
    assert result["state"] != loop_schema.NO_PRIOR
    assert len(result["timepoints"]) == 2


def test_never_recorded_biomarker_reads_no_data(tmp_path):
    """F5: a never-recorded biomarker (0 timepoints) reads a DISTINCT "no-data" marker.

    The 0-timepoint case must be distinguishable from both no-prior (1 timepoint) and
    the ≥2-timepoint trend case (state=None) — overloading the same None hides
    never-recorded from has-trend on the published surface.
    """
    result = loop_schema.read_biomarker("never_recorded", root=tmp_path)
    assert result["state"] == loop_schema.NO_DATA
    assert result["timepoints"] == []
    assert loop_schema.NO_DATA != loop_schema.NO_PRIOR
    assert loop_schema.NO_DATA is not None


def test_question_set_derived_from_active_protocols(tmp_path):
    """AC-5(a): the watch-out question set is DERIVED from active protocols/compounds.

    The derived set EQUALS the exact watch-outs the supplied protocol implies — not a
    fixed non-empty set returned for any input. A different protocol derives a
    different covering set, so a fixed-set deriver turns this RED.
    """
    bpc_set = loop_schema.derive_watchout_questions(["bpc-157"])
    assert bpc_set == {"injection_site_reaction", "appetite_change"}

    # A different active protocol derives a different covering set — a deriver that
    # returns the same fixed list for any input fails here.
    other = loop_schema.derive_watchout_questions(["unknown-compound"])
    assert other != bpc_set


def test_empty_or_unknown_protocols_derive_empty_set():
    """F9 / AC-5(a): no active (or only unknown) protocols fabricate no watch-out.

    An operator with no active protocols, or only protocols the map does not cover,
    gets an EMPTY question set — never a fabricated watch-out.
    """
    assert loop_schema.derive_watchout_questions([]) == set()
    assert loop_schema.derive_watchout_questions(["unknown-compound"]) == set()


def test_zero_automated_detection_floor():
    """AC-5(b) / NG-6: loop_schema.py contains 0 threshold/detection step.

    Failing-capable: a planted threshold-evaluation step makes the match count > 0
    and turns this RED.
    """
    assert _ng6_match_count() == 0


def test_published_state_marker_literal_values():
    """Pin the published state markers to their literal values (ADR-0007-T2 contract).

    The markers are read 1:1 by ADR-0007-T2's render views. Pinning the LITERAL
    strings (not just the constant names) turns a silent value change RED before T2
    consumes them.
    """
    assert loop_schema.PENDING == "pending"
    assert loop_schema.NOT_YET_ANSWERED == "not-yet-answered"
    assert loop_schema.NO_DATA == "no-data"
    assert loop_schema.NO_PRIOR == "no-prior"
    assert loop_schema.ANSWERED_OVER_TIME == "answered-over-time"


# --- Stream isolation (F1): the four streams occupy disjoint item namespaces ---


def test_streams_disjoint_under_shared_name(tmp_path):
    """F1: a panel and a biomarker sharing a name do NOT cross-read.

    Adversarial: if the streams shared an item namespace, read_panel would merge a
    biomarker value (a fabricated panel result) and read_biomarker would merge the
    panel's pending row. Each read must return ONLY its own stream's state.
    """
    loop_schema.record_pending_panel(
        "ferritin", "2026-06-01T08:00:00+00:00", root=tmp_path
    )
    loop_schema.record_biomarker(
        "ferritin", "2026-06-01T08:00:00+00:00", 45, root=tmp_path
    )

    assert loop_schema.read_panel("ferritin", root=tmp_path) == loop_schema.PENDING

    biomarker = loop_schema.read_biomarker("ferritin", root=tmp_path)
    assert biomarker["state"] == loop_schema.NO_PRIOR
    assert len(biomarker["timepoints"]) == 1
    assert biomarker["timepoints"][0]["value"] == 45


def test_feedback_does_not_collide_with_panel(tmp_path):
    """F1: the fixed feedback item does not cross-read a same-named panel."""
    loop_schema.record_pending_panel(
        "physician-feedback", "2026-06-01T08:00:00+00:00", root=tmp_path
    )
    loop_schema.record_physician_feedback(
        "increase dose", "2026-06-01T09:00:00+00:00", root=tmp_path
    )

    assert (
        loop_schema.read_panel("physician-feedback", root=tmp_path)
        == loop_schema.PENDING
    )
    entries = [r["value"] for r in loop_schema.read_physician_feedback(root=tmp_path)]
    assert entries == ["increase dose"]


# --- Same-timepoint carry-forward (F2): distinct entries survive, re-entry dedups ---


def test_distinct_same_timepoint_watchout_answers_both_persist(tmp_path):
    """F2: two DISTINCT same-timepoint watch-out answers both survive the next read.

    Failing-capable: a dedupe identity that excludes the value drops the second
    answer at the same timepoint (a dropped contraindication answer — a safety
    surface). Both must persist.
    """
    tp = "2026-06-01T08:00:00+00:00"
    loop_schema.record_watchout_answer("sleep_quality", "slept 8h", tp, root=tmp_path)
    loop_schema.record_watchout_answer("sleep_quality", "woke at 3am", tp, root=tmp_path)

    answers = [
        r["value"]
        for r in loop_schema.read_watchout_answers("sleep_quality", root=tmp_path)
    ]
    assert "slept 8h" in answers
    assert "woke at 3am" in answers


def test_same_watchout_answer_reentered_dedups(tmp_path):
    """F2: the SAME watch-out answer re-recorded at the same timepoint appears ONCE."""
    tp = "2026-06-01T08:00:00+00:00"
    loop_schema.record_watchout_answer("sleep_quality", "slept 8h", tp, root=tmp_path)
    loop_schema.record_watchout_answer("sleep_quality", "slept 8h", tp, root=tmp_path)

    answers = [
        r["value"]
        for r in loop_schema.read_watchout_answers("sleep_quality", root=tmp_path)
    ]
    assert answers == ["slept 8h"]


def test_distinct_same_timepoint_feedback_both_persist(tmp_path):
    """F2: two DISTINCT same-timepoint physician-feedback entries both survive."""
    tp = "2026-06-01T08:00:00+00:00"
    loop_schema.record_physician_feedback("increase dose", tp, root=tmp_path)
    loop_schema.record_physician_feedback("recheck in 6 weeks", tp, root=tmp_path)

    entries = [r["value"] for r in loop_schema.read_physician_feedback(root=tmp_path)]
    assert "increase dose" in entries
    assert "recheck in 6 weeks" in entries


def test_same_feedback_reentered_dedups(tmp_path):
    """F2: the SAME physician-feedback entry re-recorded at the same timepoint appears ONCE."""
    tp = "2026-06-01T08:00:00+00:00"
    loop_schema.record_physician_feedback("increase dose", tp, root=tmp_path)
    loop_schema.record_physician_feedback("increase dose", tp, root=tmp_path)

    entries = [r["value"] for r in loop_schema.read_physician_feedback(root=tmp_path)]
    assert entries == ["increase dose"]


# --- Cycle 2: watch-out answer carry-to-next-generation ---


def test_watchout_answer_read_next_generation(tmp_path):
    """AC-3: a watch-out answer stored this cycle is read on the NEXT generation.

    Failing-capable: a DROPPED answer (one not surviving into the next-generation
    read) turns this RED. The answer must be read in the NEXT generation, not only
    in the same cycle it was stored — the accepted one-generation loop latency.
    """
    loop_schema.record_watchout_answer(
        "sleep_quality", "slept 8h", "2026-06-01T08:00:00+00:00", root=tmp_path
    )

    # NEXT generation: a distinct later read invocation, modelling the next
    # plan/report generation. The answer must be PRESENT as a next-generation input.
    state = loop_schema.read_watchout("sleep_quality", root=tmp_path)
    assert state == loop_schema.ANSWERED_OVER_TIME

    carried = loop_schema.read_watchout_answers("sleep_quality", root=tmp_path)
    answers = [r["value"] for r in carried]
    assert "slept 8h" in answers  # dropped answer turns this RED


def test_watchout_state_transitions_on_answer(tmp_path):
    """F10: one watch-out key transitions not-yet-answered -> answered-over-time.

    Before any answer the read is not-yet-answered; after recording an answer the
    SAME key reads answered-over-time. A read stuck on either marker turns this RED.
    """
    assert (
        loop_schema.read_watchout("sleep_quality", root=tmp_path)
        == loop_schema.NOT_YET_ANSWERED
    )

    loop_schema.record_watchout_answer(
        "sleep_quality", "slept 8h", "2026-06-01T08:00:00+00:00", root=tmp_path
    )

    assert (
        loop_schema.read_watchout("sleep_quality", root=tmp_path)
        == loop_schema.ANSWERED_OVER_TIME
    )


# --- Cycle 3: physician-feedback carry-forward ---


def test_physician_feedback_carried_forward(tmp_path):
    """AC-4: a recorded physician-feedback entry is carried forward to the next generation.

    Failing-capable: a DROPPED entry (one not surviving into the next-generation
    read) turns this RED. Parallel to AC-3 — the entry is read in the NEXT
    generation, not only the cycle it was recorded.
    """
    loop_schema.record_physician_feedback(
        "increase dose to 500mcg", "2026-06-01T08:00:00+00:00", root=tmp_path
    )

    # NEXT plan/report generation read.
    carried = loop_schema.read_physician_feedback(root=tmp_path)
    entries = [r["value"] for r in carried]
    assert "increase dose to 500mcg" in entries  # dropped entry turns this RED


# --- Cycle 4: egress boundary over the store/read cycle ---


def _real_store_read_cycle(tmp_path):
    """Run a REAL loop-schema store/read cycle: append a watch-out answer, then read."""
    loop_schema.record_watchout_answer(
        "sleep_quality", "slept 8h", "2026-06-01T08:00:00+00:00", root=tmp_path
    )
    return loop_schema.read_watchout_answers("sleep_quality", root=tmp_path)


def test_store_read_cycle_zero_egress(tmp_path):
    """AC-6 (pass direction): a REAL loop-schema store/read cycle makes 0 outbound calls.

    The closure exercises the production loop-schema path (append→read), not a no-op;
    egress_guard.run returns TRUTHY because the path is local file I/O only.
    """
    result = egress_run(lambda: _real_store_read_cycle(tmp_path))
    assert result  # truthy == 0 outbound, 0 model-bound send


def test_sec03_injected_outbound_fails_guard(tmp_path):
    """AC-6 / SEC-03 (fail direction): an outbound call in the cycle flips the guard FALSY.

    The closure performs the REAL loop-schema store/read AND issues a genuine outbound
    connect — proving egress_guard.run intercepts the NEW loop-schema store path, not
    merely that a clean cycle makes 0 calls. A guard that does NOT flip to FALSY is a
    no-go. A local backlog listener makes the connect complete (kernel handshake)
    without external network dependency or an accept thread.
    """
    # Deliberate loopback-listener (not the sibling egress suites' off-host-connect +
    # network-skip idiom): a local backlog listener completes the connect handshake
    # with no network dependency, so there is no offline-skip flakiness; the deny-
    # network sandbox blocks loopback, so the injected connect still trips the guard.
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    def _cycle_with_outbound():
        _real_store_read_cycle(tmp_path)
        socket.create_connection(("127.0.0.1", port), timeout=2).close()
        return "done"

    try:
        result = egress_run(_cycle_with_outbound)
    finally:
        srv.close()

    assert not result  # falsy == FAIL: the injected outbound call was intercepted
