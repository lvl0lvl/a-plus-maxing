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


def test_question_set_derived_from_active_protocols(tmp_path):
    """AC-5(a): the watch-out question set is DERIVED from active protocols/compounds.

    The derived set must cover the watch-outs the supplied protocol implies — it is
    keyed off the operator's active protocols, not a fixed/empty list.
    """
    questions = loop_schema.derive_watchout_questions(["bpc-157"])
    assert len(questions) >= 1
    # Derivation is protocol-keyed: a different active protocol derives a
    # different (or differently-covering) set, not the same fixed list.
    other = loop_schema.derive_watchout_questions([])
    assert questions != other


def test_zero_automated_detection_floor():
    """AC-5(b) / NG-6: loop_schema.py contains 0 threshold/detection step.

    Failing-capable: a planted threshold-evaluation step makes the match count > 0
    and turns this RED.
    """
    assert _ng6_match_count() == 0


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
