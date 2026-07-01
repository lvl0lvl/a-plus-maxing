"""Read-only intake-referral collation tests (ADR-0033-0035-T3).

`scripts/serve/referral.py`'s `collate` reads the `referral::*` store items written by
the capture safety region and returns the POSITIVE safety-screen referral flags for the
doctor-visit / My-Info display (the safety-bypass falsification: a positive answer yields
a flag, a negative yields none). It is READ-ONLY / 0-egress by construction: it calls no
store write path and imports no outbound client / model SDK. All fixture-driven over a
tmp store root; 0 live spend.
"""

import functools
from pathlib import Path

from scripts.serve import capture, referral
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# An identity config ABSENT on disk (the fresh-clone posture the capture tests use).
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"


def _bound(root):
    """The instance-bound store read surface `collate` consumes (mirrors summarize's contract)."""
    return functools.partial(store.read, root=root)


def test_collate_returns_positive_referral_flags(tmp_path):
    """AC-2 collate: a POSITIVE exercise-safety answer + NEGATIVE phq2/apnea -> `collate`
    returns the exercise-safety flag and NOT the phq2/apnea flags.

    The safety-bypass falsification, read side: the flag trips ONLY on a positive answer.
    Failing-capable: a no-op collate reds the positive assertion.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "chest-pain", "phq2": "not-at-all", "apnea": "no"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    flags = referral.collate(_bound(store_root))
    assert "exercise-safety" in flags, "the positive exercise-safety referral was not collated"
    assert "phq2" not in flags, "a negative phq2 wrongly collated a referral"
    assert "apnea" not in flags, "a negative apnea wrongly collated a referral"


def test_collate_returns_no_flag_for_negative(tmp_path):
    """AC-2 collate: an all-negative answer set -> `collate` returns no referral flags.

    Failing-capable: an always-collate route reds the empty assertion.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "none", "phq2": "not-at-all", "apnea": "no"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    assert referral.collate(_bound(store_root)) == [], (
        "an all-negative safety answer set wrongly collated a referral flag"
    )


def test_collate_returns_all_positive_flags(tmp_path):
    """AC-2 collate: all three screens positive -> `collate` returns all three flags."""
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "chest-pain", "phq2": "nearly-every-day", "apnea": "yes"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    flags = referral.collate(_bound(store_root))
    assert set(flags) == {"exercise-safety", "phq2", "apnea"}, (
        f"collate did not return all three positive referral flags: {flags}"
    )


def test_referral_imports_no_outbound_client_no_sdk_no_store_write():
    """AC-6 crown-jewel (STRUCTURAL): `referral.py` imports no outbound HTTP client, no
    model SDK, and calls no store write path — it is read-only / 0-egress by construction.

    Source-grep = 0 for each banned marker. Failing-capable: an outbound import / a model
    SDK import / a store write call reds the grep.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "referral.py").read_text()
    banned = (
        "import anthropic",
        "socket.create_connection",
        "urllib.request",
        "http.client",
        "requests",
        "httpx",
        "store.append",
        "store.correct",
        "scripts.model",
    )
    for marker in banned:
        assert marker not in src, (
            f"referral.py carries a banned outbound/write marker {marker!r} — it must be "
            f"read-only / 0-egress"
        )


def test_referral_is_distinct_from_the_plan_time_doctor_visit_queue():
    """AC-6 / boundary: `referral.py` imports neither the frozen plan-time doctor-visit
    queue schema nor orchestrate — the intake-referral collation is a separate serve-layer
    surface, distinct from the medical-liaison `dvq::queue`.

    Failing-capable: importing `queue_schema` / `orchestrate` reds the assertion.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "referral.py").read_text()
    assert "queue_schema" not in src, "referral.py imports the frozen plan-time queue schema"
    assert "orchestrate" not in src, "referral.py imports the frozen plan-time orchestrate"
    assert "dvq::" not in src, "referral.py touches the plan-time dvq:: stream"


def test_collate_screens_match_the_capture_safety_screens():
    """REFACTOR / single-source-of-truth: the screens `collate` reads are exactly the
    screens the capture safety region writes — no divergent list.

    Failing-capable: adding/removing a screen in one module without the other reds this
    (a drift guard, so the two pinned lists cannot silently diverge).
    """
    capture_screens = set(capture._SAFETY_SCREEN_FIELDS.values())
    assert set(referral._REFERRAL_SCREENS) == capture_screens, (
        f"referral._REFERRAL_SCREENS {referral._REFERRAL_SCREENS} diverged from the "
        f"capture safety screens {sorted(capture_screens)}"
    )
