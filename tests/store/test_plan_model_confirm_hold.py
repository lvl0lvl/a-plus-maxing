"""The ADR-0040 confirm-hold, re-based onto the comprehensive resolver (ADR-0044-T4).

ADR-0044-T2 re-pointed the production standing-plan path onto ``read_standing_plan``,
whose comprehensive-wins branch (``read_plan_version`` -> ``resolve_comprehensive``)
applied NO confirm filter — so a HELD (unconfirmed) large-change comprehensive re-gen
would STAND, bypassing the thin hold. This task closes that hole: ``read_plan_version``
now drops each ``plan-model::`` version whose date carries a non-``confirmed``
(``pending``/``declined``) ``plan-confirm::<domain>`` pointer for ANY covered domain,
mirroring the thin ``filter_confirmed`` generalized from one domain to the composite's
domain set. A held version resolves NOT-standing; a confirmed / no-pointer version stands.

The pointer MECHANISM (``plan_confirm``) is CONSUMED byte-unchanged (AC-4); ``resolve_comprehensive``
stays PURE (the filter runs UPSTREAM of it); ``read_standing_plan`` is UNEDITED (it inherits the
hold TRANSITIVELY). Everything here is SYNTHETIC — scratch ``tmp_path`` stores, 0 live-API, 0 real
operator PII (AC-5). AC-1-prod is a PRODUCTION-PATH round trip through the REAL
``track.resolve_plan_progress``, so the filter-revert drives it RED (PF-S130-01 non-tautology).
AC-4-adversarial is the four-part store-adversarial battery (bead ``pka``); category (d) is run
RED-then-revert under two NAMED mutations (confirm-hold-removal + over-hold). PF-S131-01: every
fixture is the CANONICAL PERIODIZED ``plan_model`` composite (reused ``_comprehensive_version``
builders), recorded via ``record_plan_version``.
"""

import subprocess
from pathlib import Path

from scripts.plan import domain_program, track
from scripts.store import plan_confirm, plan_model, plan_schema, store
from scripts.store.loop_schema import _reading
from tests.store.test_plan_model import (
    _comprehensive_version,
    _compound_program,
    _training_program,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


# The DURABLE per-wave numstat base: the Wave-4 fork-point (the pre-Wave-4 main tip = the S132-close
# merge #335). A permanent main ancestor, so its numstat vs HEAD equals the wave's diff on the feature
# branch, on squashed main, AND on a fresh clone. NOT an intermediate feature-branch SHA (the wdhc
# orphan flaw) and NOT the dynamic merge-base(origin/main, HEAD): once the wave squash-merges, that
# merge-base collapses to HEAD, emptying the per-wave diff and failing the freeze-break (PF-S133-03).
# Mirrors test_plan_model_reader.py:32's durable-fork-point pattern (the Wave-3 SF-1/wdhc fix).
PRE_TASK_HEAD = "ec8071503a983ed59c8dd230ded05ee5bd9087c5"

RENDER = "2026-07-13"  # the render date the default _comprehensive_version fixture is dated


# --------------------------------------------------------------------------- #
# Shared synthetic fixtures: a >=3-domain (large-change) periodized composite,
# in the held / confirmed / no-pointer states (PF-S131-01 canonical shape).
# --------------------------------------------------------------------------- #


def _large_change_programs():
    """A >=3-domain periodized program set (>=3 covered domains clears the large-change threshold).

    All three domains are TRACKED_DOMAINS members (so AC-1-prod's ``resolve_plan_progress`` reaches
    each); a mix of training + compound kinds, each a conformant seven-field ``domain_program``.
    """
    return {
        "workout": _training_program(),
        "nutrition": _training_program(),
        "supplements": _compound_program(),
    }


def _large_change_version(**over):
    """A large-change comprehensive version dated RENDER covering >=3 periodized domains."""
    return _comprehensive_version(date=RENDER, programs=_large_change_programs(), **over)


def _seed_held_comprehensive(root, version):
    """Record `version` + mark EVERY covered domain `pending` at its date (held as a unit)."""
    plan_model.record_plan_version(version, root)
    date = version[plan_model.VERSION_DATE]
    for domain in version[plan_model.DOMAIN_PROGRAMS]:
        plan_confirm.mark_pending(domain, date, root)


def _seed_confirmed_comprehensive(root, version):
    """Record `version` + mark pending then set CONFIRMED for every covered domain (confirmed unit)."""
    plan_model.record_plan_version(version, root)
    date = version[plan_model.VERSION_DATE]
    for domain in version[plan_model.DOMAIN_PROGRAMS]:
        plan_confirm.mark_pending(domain, date, root)
        plan_confirm.set_decision(domain, date, plan_confirm.DECISION_CONFIRMED, root)


def _seed_no_pointer_comprehensive(root, version):
    """Record `version` and mark NOTHING (no confirm pointer on any domain)."""
    plan_model.record_plan_version(version, root)


def _numstat(base, *paths):
    out = subprocess.run(
        ["git", "diff", "--numstat", base, "--", *paths],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def _func_src(source_text, name):
    import ast

    for node in ast.parse(source_text).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(source_text, node)
    raise AssertionError(f"function {name!r} not found in source")


# --------------------------------------------------------------------------- #
# AC-1 — unconfirmed large-change comprehensive plan -> NOT standing (resolver)
# --------------------------------------------------------------------------- #


def test_held_comprehensive_does_not_stand(tmp_path):
    """A held (pending-pointer on >=3 covered domains) comprehensive version does NOT stand.

    The confirm-hold drops the held version, so ``read_plan_version`` resolves an ABSENCE state
    (never the held version); ``read_standing_plan`` on a covered domain short-circuits the
    comprehensive-wins branch and falls through to the thin path. Append-only preserved — the
    ``plan-model::`` stream is byte-unchanged after the read (0 versions rewritten). RED-capable:
    the Step-2.5 (d-1) confirm-hold-removal mutation stands the held version.
    """
    root = tmp_path
    version = _large_change_version()
    _seed_held_comprehensive(root, version)

    model_before = store.read(plan_model._PREFIX_MODEL, root=root)
    resolved = plan_model.read_plan_version(RENDER, root)
    assert resolved["state"] is not None  # an absence state, NOT standing
    assert resolved["state"] in (plan_model.NO_PLAN, plan_model.NO_PLAN_TODAY)
    assert resolved["version"] is None  # the held version is never returned

    standing = plan_model.read_standing_plan("workout", RENDER, root)
    assert standing["state"] is not None  # falls through to thin (no thin plan) -> absence
    assert standing["plan"] is None  # NOT the held comprehensive prescription

    model_after = store.read(plan_model._PREFIX_MODEL, root=root)
    assert model_after == model_before  # append-only: 0 versions rewritten on read
    assert len(model_after) == len(model_before) == 1


# --------------------------------------------------------------------------- #
# AC-1-prod — PRODUCTION-PATH, held comprehensive not standing (PF-S130-01)
# --------------------------------------------------------------------------- #


def test_held_comprehensive_not_standing_production_path(tmp_path):
    """The REAL ``track.resolve_plan_progress`` over a HELD comprehensive-only version -> has_plan False.

    Comprehensive-only (NO thin ``plan::workout``), so the comprehensive-wins branch is what would
    stand WITHOUT the re-base — this isolates the re-base, not the thin filter. RED-capable: the
    Step-2.5 filter-revert stands the held version through the comprehensive-wins branch (has_plan True).
    """
    root = tmp_path
    version = _large_change_version()
    _seed_held_comprehensive(root, version)  # comprehensive-only, NO thin plan::workout

    result = track.resolve_plan_progress("workout", RENDER, root)  # REAL production path
    assert result["has_plan"] is False  # the held comprehensive plan does NOT stand
    assert result["plan"] is None  # not the held prescription
    assert set(result) == {
        "domain", "plan", "specialist", "plan_date", "tracking", "has_plan", "has_tracking",
    }
    assert result["domain"] == "workout"


# --------------------------------------------------------------------------- #
# AC-2 — confirmed comprehensive plan STANDS (0 false holds)
# --------------------------------------------------------------------------- #


def test_confirmed_comprehensive_stands(tmp_path):
    """A confirmed (all covered domains ``DECISION_CONFIRMED``) comprehensive version STANDS.

    The hold RELEASES on confirm — 0 false holds on a confirmed plan. RED-capable ONLY via the
    Step-2.5 (d-2) OVER-HOLD mutation (the removal/revert mutations leave a confirmed version standing).
    """
    root = tmp_path
    version = _large_change_version()
    _seed_confirmed_comprehensive(root, version)

    resolved = plan_model.read_plan_version(RENDER, root)
    assert resolved["state"] is None  # STANDING
    assert resolved["version"]["narrative"] == version["narrative"]

    standing = plan_model.read_standing_plan("workout", RENDER, root)
    assert standing["state"] is None
    expected = version["domain_programs"]["workout"][domain_program.PRESCRIPTION]
    assert standing["plan"] == expected
    assert "blocks" in standing["plan"]  # the comprehensive periodized prescription


# --------------------------------------------------------------------------- #
# AC-3 — no-pointer default STANDS (no default hold)
# --------------------------------------------------------------------------- #


def test_no_pointer_comprehensive_stands(tmp_path):
    """A comprehensive version with NO confirm pointer STANDS — the hold fires only on a pending domain.

    RED-capable ONLY via the Step-2.5 (d-2) OVER-HOLD mutation (a no-pointer version stands with or
    without the filter, so the removal/revert mutations do not falsify it).
    """
    root = tmp_path
    version = _large_change_version()
    _seed_no_pointer_comprehensive(root, version)

    resolved = plan_model.read_plan_version(RENDER, root)
    assert resolved["state"] is None  # no default hold
    assert resolved["version"]["narrative"] == version["narrative"]

    standing = plan_model.read_standing_plan("workout", RENDER, root)
    assert standing["state"] is None
    assert standing["plan"] == version["domain_programs"]["workout"][domain_program.PRESCRIPTION]
    assert "blocks" in standing["plan"]


# --------------------------------------------------------------------------- #
# AC-4 — the ADR-0040 pointer MECHANISM byte-unchanged (non-tautological pairing)
# --------------------------------------------------------------------------- #


def test_confirm_mechanism_byte_unchanged():
    """The pointer mechanism ``plan_confirm.py`` is byte-unchanged WHILE the re-base surface changed.

    The non-tautological pairing the ADR-0044-T4 AC names: EMPTY numstat on the mechanism, NON-EMPTY
    on ``plan_model.py``. Plus a grep that the pointer stream + its sinks are intact. RED-capable via
    the AC-4 forbidden-file mutation (a throwaway ``plan_confirm.py`` edit REDs the EMPTY leg).
    """
    assert _numstat(PRE_TASK_HEAD, "scripts/store/plan_confirm.py") == ""  # mechanism untouched
    assert _numstat(PRE_TASK_HEAD, "scripts/store/plan_model.py") != ""  # re-base surface changed

    confirm_src = (REPO_ROOT / "scripts/store/plan_confirm.py").read_text(encoding="utf-8")
    for token in (
        "def mark_pending", "def set_decision", "def decision_for", "def filter_confirmed",
        '_PREFIX_CONFIRM = "plan-confirm::"', '_SOURCE = "plan-confirm"',
    ):
        assert token in confirm_src, f"the pointer mechanism token is missing: {token!r}"


# --------------------------------------------------------------------------- #
# AC-4-FS — frozen-spine numstat (the <always-frozen> six + the mechanism)
# --------------------------------------------------------------------------- #


def test_frozen_spine_numstat():
    """The <always-frozen> six + ``plan_confirm.py`` are byte-frozen vs the pre-build trunk (origin/main)."""
    assert _numstat(
        "origin/main",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py", "scripts/plan/router.py",
        "scripts/store/plan_confirm.py",
    ) == ""


# --------------------------------------------------------------------------- #
# AC-4-adversarial — store-adversarial battery (bead pka), all four categories
# --------------------------------------------------------------------------- #


def test_confirm_hold_cross_stream_disjoint(tmp_path):
    """(a) cross-stream namespace collision over the confirm-hold surface.

    A pointer for a domain OUTSIDE the version's ``domain_programs`` does NOT hold it; a pointer for
    a COVERED domain does. The hold reads ONLY ``plan-confirm::`` decisions via ``decision_for`` —
    never a ``plan::<domain>`` value NOR the SEC-01 item-"" decoy (both seeded dated on_date; the
    version resolves on its real pointers only).
    """
    outside = tmp_path / "outside"
    version = _comprehensive_version(
        date=RENDER,
        programs={"workout": _training_program(), "nutrition": _training_program(),
                  "supplements": _compound_program()},
    )
    plan_model.record_plan_version(version, outside)
    plan_confirm.mark_pending("peptides", RENDER, outside)  # peptides is NOT a covered domain
    # decoys dated on_date: a thin plan::workout value + an item-"" SEC-01 decoy — inert to the hold
    plan_schema.record_plan("workout", {"exercises": [{"name": "Squat", "sets": 3}]}, RENDER, "coach", outside)
    store.append("", _reading("", RENDER, "decoy-empty-item", "FOREIGN-ITEM-EMPTY"), root=outside)

    resolved = plan_model.read_plan_version(RENDER, outside)
    assert resolved["state"] is None, "a pointer OUTSIDE the version's domains must not hold it"
    assert resolved["version"] == version  # the real composite, never a foreign/thin value
    assert resolved["version"] != "FOREIGN-ITEM-EMPTY"

    covered = tmp_path / "covered"
    plan_model.record_plan_version(version, covered)
    plan_confirm.mark_pending("workout", RENDER, covered)  # workout IS a covered domain
    held = plan_model.read_plan_version(RENDER, covered)
    assert held["state"] is not None, "a pointer for a COVERED domain must hold the version"
    assert held["version"] is None


def test_confirm_hold_same_timepoint(tmp_path):
    """(b) same-timepoint per-pointer resolution — ONE shared date D, TWO versions, one pointer-set.

    Two DISTINCT versions at the SAME date D (distinct narratives) both persist. The (domain, D)
    pending pointers hold the SHARED timepoint, so BOTH same-date versions drop — the reversed-scan
    latest-wins does NOT stand the later-appended B while held. On confirm, the shared-timepoint hold
    RELEASES and the reversed-scan latest-wins stands the last-appended (B). This is the SAME-timepoint
    keying interplay, not the trivially-independent two-different-dates case.
    """
    root = tmp_path
    v_a = _comprehensive_version(date=RENDER, narrative="version A (earlier-recorded)",
                                 programs=_large_change_programs())
    v_b = _comprehensive_version(date=RENDER, narrative="version B (later-recorded)",
                                 programs=_large_change_programs())
    plan_model.record_plan_version(v_a, root)
    plan_model.record_plan_version(v_b, root)  # B last

    readings = store.read(plan_model._PREFIX_MODEL, root=root)
    assert len(readings) == 2, "two distinct versions at one timepoint did not both persist"
    assert len({r["source"] for r in readings}) == 2  # distinct content-tag version sources

    for domain in v_b[plan_model.DOMAIN_PROGRAMS]:
        plan_confirm.mark_pending(domain, RENDER, root)
    held = plan_model.read_plan_version(RENDER, root)
    assert held["state"] is not None, "the shared-timepoint pointers must hold BOTH same-date versions"
    assert held["version"] is None

    for domain in v_b[plan_model.DOMAIN_PROGRAMS]:
        plan_confirm.set_decision(domain, RENDER, plan_confirm.DECISION_CONFIRMED, root)
    stood = plan_model.read_plan_version(RENDER, root)
    assert stood["state"] is None  # the shared-timepoint hold released
    assert stood["version"]["narrative"] == "version B (later-recorded)"  # last-appended wins


def test_confirm_hold_no_new_keying(tmp_path):
    """(c) dedupe-key boundary — the confirm-hold ADDITION defines 0 new keying + calls 0 write primitive.

    Scoped to the confirm-hold addition (the new filter helper + the ``read_plan_version`` edit), NOT
    the whole module (which legitimately carries ``record_plan_version`` / ``store.append``). The
    identity stays ``keying``'s frozen ``(item, timepoint, source)``, reached only through ``store.read``;
    the addition is READ-only over both streams.
    """
    source = (REPO_ROOT / "scripts/store/plan_model.py").read_text(encoding="utf-8")
    addition = _func_src(source, "_standing_versions") + "\n" + _func_src(source, "read_plan_version")

    for token in ("DEDUPE_FIELDS", "dedupe_key", "LINE_FIELDS", "_DEDUPE_EXCLUDED"):
        assert token not in addition, f"the confirm-hold addition re-defines keying logic: {token!r}"
    for call in ("store.append(", "store.correct(", "mark_pending(", "set_decision(",
                 "record_plan_version("):
        assert call not in addition, f"the confirm-hold addition invokes a write primitive: {call!r}"


# --------------------------------------------------------------------------- #
# AC-5 — suite-local green + 0 real operator PII in the test tree
# --------------------------------------------------------------------------- #


def test_no_operator_identity_literal_in_test_tree():
    source = Path(__file__).read_text(encoding="utf-8").lower()
    # Assembled from splits so the guard's own token list never self-matches.
    forbidden = ["".join(parts) for parts in (
        ("wal", "ter"), ("mcgiv", "ney"), ("wmcgiv", "ney"), ("@", "gmail"),
    )]
    for token in forbidden:
        assert token not in source, "a real operator-identity literal leaked into the test tree"
