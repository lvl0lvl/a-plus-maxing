"""Tests for the mixed-history-tolerant plan reader + the track re-point (ADR-0044-T2).

The reader (`plan_model.read_standing_plan`) resolves a domain's STANDING plan over a
MIXED history — the pre-model thin `plan::<domain>` readings AND the comprehensive
`plan-model::` versions — applying comprehensive-wins precedence (a comprehensive version
standing for the render date and covering the domain wins; otherwise the thin result
verbatim, so a pre-migration thin-only store keeps working). It RIDES the FROZEN `store.read`
UNCHANGED: it writes nothing, rewrites no reading on EITHER stream (append-only preserved,
SEC-W3-01), and defines no store key. The consumer `track.resolve_plan_progress` is
re-pointed off the thin `plan_schema.read_plan` onto this reader.

Everything here is SYNTHETIC — scratch `tmp_path` stores, 0 live-API, 0 real operator PII.
AC-1 / AC-3 / AC-3b are PRODUCTION-PATH round trips (the REAL record -> `store.append` ->
read path, and the REAL `track.resolve_plan_progress`), so the (d) comprehensive-precedence
mutation + the PF-S130-01 revert-to-thin drive them RED (non-tautology). The comprehensive
prescription (`{"blocks":[...]}`) vs the thin plan (`{"exercises":[...]}`) is the distinguishing
signal — PF-S131-01 canonical periodized fixtures, reused from `test_plan_model.py`.
"""

import subprocess
from pathlib import Path

from scripts.plan import domain_program, track
from scripts.store import plan_model, plan_schema, store
from scripts.store.loop_schema import _reading
from tests.store.test_plan_model import _comprehensive_version, _training_program

# This task's rollback target AND the per-ADR numstat base (QA-06: the FIXED entry HEAD,
# pre-commit-runnable + in-flow RED-capability-demonstrable — mirrors test_plan_model.py:27).
PRE_TASK_HEAD = "9f6fe9f9893008b1971e76dcc6cd5063a85fb047"
REPO_ROOT = Path(__file__).resolve().parents[2]

RENDER = "2026-07-13"  # the render date the default _comprehensive_version fixture is dated


# --------------------------------------------------------------------------- #
# Thin-side fixtures (mirror tests/plan/test_track.py's _workout_plan/_seed_plan).
# The thin plan shape {"exercises":[...]} is trivially distinguishable from the
# comprehensive prescription {"blocks":[...]}.
# --------------------------------------------------------------------------- #


def _workout_plan():
    return {"exercises": [{"name": "Squat", "sets": 3, "load": "185 lb", "reps": 8}]}


def _seed_thin(root, domain="workout", date=RENDER, plan=None, specialist="personal-trainer"):
    plan_schema.record_plan(domain, plan or _workout_plan(), date, specialist, root)


def _func_src(source_text, name):
    import ast

    for node in ast.parse(source_text).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(source_text, node)
    raise AssertionError(f"function {name!r} not found in source")


def _numstat(base, *paths):
    out = subprocess.run(
        ["git", "diff", "--numstat", base, "--", *paths],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


# --------------------------------------------------------------------------- #
# AC-1 — mixed-history read, comprehensive-wins (disposition #16, load-bearing)
# --------------------------------------------------------------------------- #


def test_mixed_history_comprehensive_wins(tmp_path):
    """A thin reading + a comprehensive version, both dated the render date: comprehensive wins,
    the thin coexists, and NEITHER stream is rewritten on read (append-only, SEC-W3-01)."""
    root = tmp_path
    _seed_thin(root, domain="workout", date=RENDER)  # thin {"exercises":[...]}
    version = _comprehensive_version(date=RENDER)  # covers workout (training) + peptides (compound)
    plan_model.record_plan_version(version, root)

    # Capture BOTH streams before the read (SEC-W3-01: symmetric append-immutability).
    thin_before = store.read("plan::workout", root=root)
    model_before = store.read(plan_model._PREFIX_MODEL, root=root)

    resolved = plan_model.read_standing_plan("workout", RENDER, root)

    # The comprehensive plan WINS over the coexisting thin reading.
    assert resolved["state"] is None  # standing, not an absence state
    expected = version["domain_programs"]["workout"][domain_program.PRESCRIPTION]
    assert resolved["plan"] == expected
    assert "blocks" in resolved["plan"]  # the comprehensive periodized prescription
    assert "exercises" not in resolved["plan"]  # NOT the thin plan
    assert resolved["plan_date"] == RENDER

    # Append-only preserved on BOTH streams — 0 readings rewritten (SEC-W3-01, symmetric).
    thin_after = store.read("plan::workout", root=root)
    model_after = store.read(plan_model._PREFIX_MODEL, root=root)
    assert thin_after == thin_before  # thin plan::workout byte-unchanged (values + count)
    assert len(thin_after) == len(thin_before)
    assert model_after == model_before  # comprehensive plan-model:: byte-unchanged
    assert len(model_after) == len(model_before)


# --------------------------------------------------------------------------- #
# AC-2 — thin-only fallback (no comprehensive version yet) — pre-migration store
# --------------------------------------------------------------------------- #


def test_thin_only_fallback_resolves(tmp_path):
    """A store with ONLY thin readings resolves without error via the reader — the thin
    result verbatim (standing thin plan + absence states), 0 crashes."""
    root = tmp_path
    _seed_thin(root, domain="workout", date=RENDER, specialist="personal-trainer")

    resolved = plan_model.read_standing_plan("workout", RENDER, root)
    # identical to today's plan_schema.read_plan result (the thin resolve, unchanged)
    assert resolved == plan_schema.read_plan("workout", RENDER, root)
    assert resolved["state"] is None
    assert resolved["plan"] == _workout_plan()  # the thin plan, carrying "exercises"
    assert resolved["specialist"] == "personal-trainer"  # thin specialist attribution preserved
    assert resolved["plan_date"] == RENDER

    # a thin store with no plan FOR the date -> NO_PLAN_TODAY carrying the latest on-file date
    absent = plan_model.read_standing_plan("workout", "2026-07-20", root)
    assert absent["state"] == plan_schema.NO_PLAN_TODAY
    assert absent["plan"] is None
    assert absent["plan_date"] == RENDER  # the latest on-file date

    # a domain with zero plans -> NO_PLAN, no crash
    none = plan_model.read_standing_plan("nutrition", RENDER, root)
    assert none["state"] == plan_schema.NO_PLAN
    assert none["plan"] is None


# --------------------------------------------------------------------------- #
# AC-3 — consumer re-point, PRODUCTION-PATH (PF-S130-01 load-bearing)
# --------------------------------------------------------------------------- #


def test_resolve_plan_progress_comprehensive_wins_production_path(tmp_path):
    """The REAL track.resolve_plan_progress over a MIXED history returns has_plan True + the
    comprehensive prescription (not the thin plan, not NO_PLAN), all return-dict keys intact."""
    root = tmp_path
    _seed_thin(root, domain="workout", date=RENDER)  # thin plan
    plan_model.record_plan_version(_comprehensive_version(date=RENDER), root)  # later comprehensive

    result = track.resolve_plan_progress("workout", RENDER, root)  # REAL production path

    assert result["has_plan"] is True
    expected = _comprehensive_version(date=RENDER)["domain_programs"]["workout"][domain_program.PRESCRIPTION]
    assert result["plan"] == expected
    assert "blocks" in result["plan"]  # the comprehensive prescription
    assert "exercises" not in result["plan"]  # NOT the thin plan
    # every existing return-dict KEY intact (downstream consumers read the same shape)
    assert set(result) == {
        "domain", "plan", "specialist", "plan_date", "tracking", "has_plan", "has_tracking",
    }
    assert result["domain"] == "workout"
    assert result["plan_date"] == RENDER


def test_resolve_plan_progress_comprehensive_only_not_no_plan(tmp_path):
    """AC-3b: a comprehensive-only store (no thin plan for the domain) resolves has_plan True with
    the comprehensive prescription — NOT a NO_PLAN absence on a stored plan."""
    root = tmp_path
    plan_model.record_plan_version(_comprehensive_version(date=RENDER), root)  # NO thin plan::workout

    result = track.resolve_plan_progress("workout", RENDER, root)

    assert result["has_plan"] is True  # NOT has_plan False on a stored comprehensive plan
    assert result["plan"] is not None
    assert "blocks" in result["plan"]
    assert result["plan_date"] == RENDER


# --------------------------------------------------------------------------- #
# AC-4 — store-adversarial battery (bead pka), all four categories, over the READER
# --------------------------------------------------------------------------- #


def test_reader_cross_stream_disjoint(tmp_path):
    """(a) cross-stream namespace collision: the reader for domain X never returns domain Y's
    plan, and the comprehensive read never returns a thin value NOR the SEC-01 item-"" decoy."""
    root = tmp_path
    _seed_thin(root, domain="workout", date=RENDER, plan={"exercises": [{"name": "Squat", "sets": 3}]})
    _seed_thin(root, domain="nutrition", date=RENDER, specialist="nutritionist",
               plan={"calorie_goal": 2600, "macros": {"protein": 180, "carbs": 300, "fat": 80},
                     "meals": [{"name": "Breakfast", "contents": "eggs", "kcal": 650}]})
    # a comprehensive version covering ONLY workout (nutrition must fall through to its thin plan)
    version = _comprehensive_version(date=RENDER, programs={"workout": _training_program()})
    plan_model.record_plan_version(version, root)
    # SEC-01 item-"" decoy dated on_date — IF the model prefix were blanked it would win the resolve
    store.append("", _reading("", RENDER, "decoy-empty-item", "FOREIGN-ITEM-EMPTY"), root=root)

    # nutrition: comprehensive does not cover it -> thin fallback returns nutrition's plan, never workout's
    nut = plan_model.read_standing_plan("nutrition", RENDER, root)
    assert "calorie_goal" in nut["plan"] and "exercises" not in nut["plan"]
    # workout: comprehensive-wins prescription, never nutrition's, never the item-"" decoy
    wk = plan_model.read_standing_plan("workout", RENDER, root)
    assert "blocks" in wk["plan"]
    assert "calorie_goal" not in wk["plan"]
    assert wk["plan"] != "FOREIGN-ITEM-EMPTY"

    # the comprehensive stream is disjoint: only the real composite, never the foreign item-"" value
    model_readings = store.read(plan_model._PREFIX_MODEL, root=root)
    assert model_readings, "the plan-model stream is empty (the disjointness check would be vacuous)"
    assert all(r["item"] == plan_model._PREFIX_MODEL for r in model_readings)
    assert not any(r["value"] == "FOREIGN-ITEM-EMPTY" for r in model_readings)
    # the thin decoy persisted in ITS OWN stream (the cross-check is not vacuous)
    assert store.read("plan::workout", root=root)  # workout's thin stream is populated


def test_reader_same_timepoint_latest_comprehensive_resolves(tmp_path):
    """(b) same-timepoint dedupe: two DISTINCT comprehensive versions at one timepoint both persist;
    the reader's reversed-scan resolves the LAST-appended; an identical re-record is a no-op."""
    root = tmp_path
    v1 = _comprehensive_version(
        date=RENDER, narrative="the earlier-recorded version",
        programs={"workout": _training_program(
            prescription={"blocks": [{"date": RENDER, "phase": "A", "detail": "first"}]})},
    )
    v2 = _comprehensive_version(
        date=RENDER, narrative="the later-recorded version",
        programs={"workout": _training_program(
            prescription={"blocks": [{"date": RENDER, "phase": "B", "detail": "second"}]})},
    )
    plan_model.record_plan_version(v1, root)
    plan_model.record_plan_version(v2, root)
    assert len(store.read(plan_model._PREFIX_MODEL, root=root)) == 2  # both distinct versions persist

    resolved = plan_model.read_standing_plan("workout", RENDER, root)
    assert resolved["state"] is None
    assert resolved["plan"]["blocks"][0]["detail"] == "second"  # the LAST-appended version stands

    plan_model.record_plan_version(v2, root)  # identical re-record
    assert len(store.read(plan_model._PREFIX_MODEL, root=root)) == 2  # 0 duplicate lines (idempotent)


def test_reader_no_new_keying(tmp_path):
    """(c) the reader ADDITION defines 0 new dedupe-key/keying logic AND calls 0 write primitive —
    it is read-only over BOTH streams, identity reached only through the frozen store.read."""
    source = (REPO_ROOT / "scripts/store/plan_model.py").read_text(encoding="utf-8")
    reader_src = _func_src(source, "read_standing_plan")  # SCOPED to the reader body, not the module

    # (c-i) 0 new dedupe-key / keying logic in the reader addition
    for token in ("DEDUPE_FIELDS", "dedupe_key", "LINE_FIELDS", "_DEDUPE_EXCLUDED"):
        assert token not in reader_src, f"the reader re-defines store keying logic: {token!r}"
    # (c-ii) 0 write-primitive CALLS in the reader addition (SEC-W3-01, symmetric on both streams)
    for call in ("store.append(", "store.correct(", ".append(", ".correct(", "record_plan_version("):
        assert call not in reader_src, f"the reader invokes a write primitive: {call!r}"


# --------------------------------------------------------------------------- #
# AC-FS — per-ADR freeze-break numstat (the FROZEN-SPINE constraint the task carries)
# --------------------------------------------------------------------------- #


def test_frozen_spine_numstat_and_scoped_delta():
    """The reader rides the frozen primitive: the frozen four + assemble.py (+ adjust.py/router.py)
    are byte-frozen vs PRE_TASK_HEAD, and the <always-frozen> 6-file glob is byte-frozen vs origin/main.
    (QA-W3-02: plan_schema.py/orchestrate.py/generate_plan.py are Wave-3 sibling-superseded and DROPPED
    from the persisted probe — a later sibling commit would false-RED them.)"""
    # (a) the HARD-frozen four + assemble.py (no Wave-3 editor) + adjust.py/router.py vs PRE_TASK_HEAD
    assert _numstat(
        PRE_TASK_HEAD,
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/assemble.py", "scripts/plan/adjust.py", "scripts/plan/router.py",
    ) == ""
    # (b) the <always-frozen> 6-file HARD glob vs the pre-build trunk
    assert _numstat(
        "origin/main",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py", "scripts/plan/router.py",
    ) == ""


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
