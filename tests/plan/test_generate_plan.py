"""Tests for the plan-generation production caller (the PF-S63-02 core-capability proof).

`generate_plan` is `assemble`'s production caller: it derives the summary from the store,
runs one captured author output through `assemble`'s four safety filters for a domain,
translates the surviving recommendations into the `plan_schema` domain plan, and records
it via `record_plan` (the store write the dashboard plan zone reads). These tests pin:

  - the wired path records a workout plan from an author envelope (happy path);
  - the LOAD-BEARING safety gates — the clearance gate (no load prescription without a
    clinician clearance) and the HALT struck-rec exclusion — each mutation-proven RED;
  - the honest no-plan states (thin-library / no recommendations / all-struck record
    NOTHING, never a fabricated regimen);
  - fail-loud on a schema-nonconformant translated plan;
  - the store-adversarial battery (docs/checklists/store-adversarial-tests.md) at the
    generate_plan write boundary — cross-stream isolation, dedupe idempotency, dedupe-key
    boundary, changed-value no-op; and
  - the production path end-to-end (a real store -> generate_plan -> rendered dashboard).
"""

import functools

import pytest

from scripts.generate import generate
from scripts.plan import generate_plan as gp_mod
from scripts.plan.generate_plan import generate_plan
from scripts.store import keying, plan_schema, store

PLAN_DATE = "2026-06-18"


# --- fixtures ------------------------------------------------------------------


def _seed_store(root, **overrides):
    """Seed PII-free operator-state items into a real temp store; return a bound reader.

    Backs the pass-through Summary Field-Set fields `summarize` reads. `overrides` replace
    individual field values. Returns a `store.read` pre-bound to `root` (the summarize
    caller contract).
    """
    fields = {
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
    }
    fields.update(overrides)
    for item, value in fields.items():
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": PLAN_DATE, "source": "intake", "value": value},
            root=root,
        )
    return functools.partial(store.read, root=root)


def _workout_rec(name, sets, *, claim=None, load=None, **rec_extra):
    """A complete workout recommendation (universal contract + workout payload)."""
    payload = {"name": name, "sets": sets, "reps": "8-12", "detail": "controlled tempo"}
    if load is not None:
        payload["load"] = load
    rec = {
        "claim": claim or f"perform {name.lower()} to rebuild a movement base",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        "payload": payload,
    }
    rec.update(rec_extra)
    return rec


def _author(*recs, specialist="personal-trainer"):
    """A captured author envelope carrying `recs`."""
    return {"specialist": specialist, "recommendations": list(recs)}


# --- happy path ----------------------------------------------------------------


def test_records_workout_plan_from_author(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3), _workout_rec("Bodyweight RDL", 3))

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert result["specialist"] == "personal-trainer"
    names = [ex["name"] for ex in result["plan"]["exercises"]]
    assert names == ["Goblet squat", "Bodyweight RDL"]
    # the plan is in the store, attributed to the author
    readings = store.read("plan::workout", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["source"] == "plan::personal-trainer"


def test_summary_is_the_only_operator_state_source(tmp_path):
    # crit-7/8 at the caller boundary: the section surfaces operator inputs read by field
    # name from the summary (the 0-raw-PII boundary), not from any other source.
    store_read = _seed_store(tmp_path, **{"hard-limits": "no fasting"})
    author = _author(_workout_rec("Goblet squat", 3))

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    personalization = result["section"]["personalization"]
    assert personalization.get("hard-limits") == "no fasting"
    assert personalization.get("goal-targets") == "return to pre-Jan-2026 loading"


# --- clearance gate (load-bearing; mutation-proven) ----------------------------


def test_clearance_gate_strips_load_by_default(tmp_path):
    # Default-deny: a load prescription is dropped when no clinician clearance is granted.
    # MUTATION: if `_to_workout_plan` stops popping `load`, this assertion goes RED.
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3, load="60% 1RM"))

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is True
    assert "load" not in result["plan"]["exercises"][0]


def test_clearance_granted_keeps_load(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Back squat", 3, load="70% 1RM"))

    result = generate_plan(
        "workout", author, store_read, tmp_path,
        plan_date=PLAN_DATE, gates={"clearance_granted": True},
    )

    assert result["plan"]["exercises"][0]["load"] == "70% 1RM"


# --- HALT struck-rec exclusion (load-bearing; mutation-proven) ------------------


def test_struck_rec_excluded_from_plan(tmp_path):
    # hard-limits "no overhead pressing"; a rec asserting an overhead press is struck by
    # assemble's HALT filter and must NOT be lifted back into a prescribed exercise.
    # MUTATION: if `_surviving` stops filtering struck claims, the struck exercise appears.
    store_read = _seed_store(tmp_path)  # hard-limits = "no overhead pressing"
    author = _author(
        _workout_rec("Goblet squat", 3),
        _workout_rec(
            "Overhead press", 3,
            claim="perform overhead pressing for shoulder strength",
            category="overhead-pressing",
        ),
    )

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    names = [ex["name"] for ex in result["plan"]["exercises"]]
    assert names == ["Goblet squat"]


def test_all_recs_struck_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author(
        _workout_rec(
            "Overhead press", 3,
            claim="perform overhead pressing for shoulder strength",
            category="overhead-pressing",
        ),
    )

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-actionable-recommendation"
    assert store.read("plan::workout", root=tmp_path) == []


# --- honest no-plan states -----------------------------------------------------


def test_thin_library_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = {"specialist": "personal-trainer", "thin_library": True}

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == plan_schema_thin_library_kind()
    assert store.read("plan::workout", root=tmp_path) == []


def test_empty_recommendations_records_nothing(tmp_path):
    store_read = _seed_store(tmp_path)
    author = _author()  # zero recommendations

    result = generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert result["recorded"] is False
    assert result["reason"] == "no-recommendations"
    assert store.read("plan::workout", root=tmp_path) == []


# --- fail-loud + routing -------------------------------------------------------


def test_unknown_domain_raises(tmp_path):
    store_read = _seed_store(tmp_path)
    with pytest.raises(KeyError):
        generate_plan("cardio", _author(), store_read, tmp_path, plan_date=PLAN_DATE)


def test_payload_missing_required_field_raises_loud(tmp_path):
    # A translator emitting a schema-nonconformant plan must fail LOUD at record_plan,
    # never silently drop. Here the payload omits the required `sets`.
    store_read = _seed_store(tmp_path)
    bad = _workout_rec("Goblet squat", 3)
    del bad["payload"]["sets"]
    author = _author(bad)

    with pytest.raises(ValueError):
        generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)
    assert store.read("plan::workout", root=tmp_path) == []


# --- store-adversarial battery (docs/checklists/store-adversarial-tests.md) -----


def test_cross_stream_isolation(tmp_path):
    # 1. Cross-stream collision: a workout write lands ONLY in plan::workout; no other
    #    plan stream is written, and reading another plan domain returns nothing.
    store_read = _seed_store(tmp_path)
    generate_plan("workout", _author(_workout_rec("Goblet squat", 3)),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    items = store.items(root=tmp_path)
    plan_items = [i for i in items if i.startswith("plan::")]
    assert plan_items == ["plan::workout"]
    for other in ("nutrition", "supplements", "peptides"):
        assert store.read(f"plan::{other}", root=tmp_path) == []


def test_dedupe_idempotent_rerun(tmp_path):
    # 2. Same-key idempotency: re-running with the same (domain, date, specialist) + value
    #    appends 0 lines (store dedupe), never a silent duplicate.
    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3))
    generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    assert len(store.read("plan::workout", root=tmp_path)) == 1


def test_dedupe_key_boundary_specialist_and_date(tmp_path):
    # 3. Dedupe-key boundary: a differing source (specialist) OR timepoint (date) is a
    #    distinct identity — both persist; they do not collide.
    store_read = _seed_store(tmp_path)
    rec = _workout_rec("Goblet squat", 3)
    generate_plan("workout", _author(rec, specialist="personal-trainer"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", _author(rec, specialist="health-implementer"),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", _author(rec, specialist="personal-trainer"),
                  store_read, tmp_path, plan_date="2026-06-19")

    readings = store.read("plan::workout", root=tmp_path)
    assert len(readings) == 3


def test_changed_value_same_identity_is_noop(tmp_path):
    # 3 (cont.) value is EXCLUDED from the dedupe identity: a re-record with a CHANGED plan
    #    at the same (domain, date, specialist) is dropped (a revision goes via correct_plan,
    #    never a silent overwrite). The first value still reads current.
    store_read = _seed_store(tmp_path)
    generate_plan("workout", _author(_workout_rec("Goblet squat", 3)),
                  store_read, tmp_path, plan_date=PLAN_DATE)
    generate_plan("workout", _author(_workout_rec("Bulgarian split squat", 4)),
                  store_read, tmp_path, plan_date=PLAN_DATE)

    readings = store.read("plan::workout", root=tmp_path)
    assert len(readings) == 1
    assert readings[-1]["value"]["exercises"][0]["name"] == "Goblet squat"


# --- production path end-to-end (integration-verification mandate) -------------


def test_end_to_end_renders_on_dashboard(tmp_path):
    import datetime

    store_read = _seed_store(tmp_path)
    author = _author(_workout_rec("Goblet squat", 3), _workout_rec("Bodyweight RDL", 3))
    generate_plan("workout", author, store_read, tmp_path, plan_date=PLAN_DATE)

    out = generate.run(
        "dashboard", _root=tmp_path, _out_dir=tmp_path,
        _today=datetime.date.fromisoformat(PLAN_DATE),
    )
    html = out.read_text(encoding="utf-8")
    assert "Goblet squat" in html
    assert "Bodyweight RDL" in html
    assert "personal-trainer" in html


# --- helpers -------------------------------------------------------------------


def plan_schema_thin_library_kind():
    """The coverage-gap kind `assemble` reports for a thin-library author output."""
    from scripts.plan.assemble import THIN_LIBRARY_GAP

    return THIN_LIBRARY_GAP
