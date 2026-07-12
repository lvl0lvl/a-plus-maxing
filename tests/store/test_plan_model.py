"""Tests for the comprehensive Plan Model store surface (ADR-0044-T1).

The comprehensive plan is ONE composite object per plan version (per active domain
the seven-field DOMAIN PROGRAM intact + integrated narrative + dated milestones +
compiled monitoring config + plan-level adjustment rules). It rides the FROZEN
``store.append`` / ``keying`` ``(item, timepoint, source)`` identity UNCHANGED as a
richer VALUE (disposition #14): a NEW ``plan-model::`` item namespace, timepoint =
the version date, source = a content-tag version key. No new store primitive, no
second dedupe key, no ``store.correct``.

Everything here is SYNTHETIC — scratch ``tmp_path`` stores, 0 live-API, 0 real
operator PII (AC-6). AC-1 / AC-3 are PRODUCTION-PATH round trips (the REAL record ->
``store.append`` -> resolve path), so a revert to the thin ``plan_schema`` spine
drives them RED (PF-S130-01 non-tautology). AC-5 is the four-part store-adversarial
battery (bead ``pka``); category (d) is run RED-then-revert under two NAMED mutations.
"""

import subprocess
from pathlib import Path

import pytest

from scripts.plan import domain_program
from scripts.store import keying, plan_model, plan_schema, store
from scripts.store.loop_schema import _reading

PRE_TASK_HEAD = "ad35cb62e09bfda8c3999f2ee1e137175a25e627"
REPO_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- #
# Shared synthetic fixture: a comprehensive plan version spanning >=2 domains.
# --------------------------------------------------------------------------- #


def _training_program(**over):
    """A conformant seven-field training DOMAIN PROGRAM (domain_program.validate)."""
    program = {
        "domain_kind": "training",
        "prescription": {
            "blocks": [
                {"date": "2026-07-13", "phase": "hypertrophy", "detail": "upper/lower x4"},
                {"date": "2026-07-20", "phase": "hypertrophy-2", "detail": "add a top set"},
            ]
        },
        "rationale": {
            "claims": [
                {"claim": "volume drives growth", "certainty": "moderate",
                 "strength": "strong", "causal": True}
            ]
        },
        "monitoring_signals": [{"validity_tier": "high", "signal": "e1RM"}],
        "adjustment_rules": [{"trigger": "rpe>9 two sessions", "action": "deload 10%"}],
        "required_labs": [],
        "refusal_escalation": {},
        "cross_domain_seams": [],
    }
    program.update(over)
    return program


def _compound_program(**over):
    """A conformant seven-field compound DOMAIN PROGRAM (required_labs non-empty)."""
    program = {
        "domain_kind": "compound",
        "prescription": {
            "blocks": [
                {"date": "2026-07-13", "phase": "cycle-wk1", "detail": "250mcg AM"},
                {"date": "2026-07-27", "phase": "cycle-wk3", "detail": "titrate to response"},
            ]
        },
        "rationale": {
            "claims": [
                {"claim": "supports connective-tissue recovery", "certainty": "low",
                 "strength": "weak", "causal": False}
            ]
        },
        "monitoring_signals": [{"validity_tier": "moderate", "signal": "injection-site"}],
        "adjustment_rules": [{"trigger": "site reaction", "action": "hold + reassess"}],
        "required_labs": ["IGF-1", "fasting glucose"],
        "refusal_escalation": {},
        "cross_domain_seams": [],
    }
    program.update(over)
    return program


def _comprehensive_version(
    *, date="2026-07-13", narrative="Integrated 12-week block: train hard, recover, monitor.",
    programs=None, milestones=None, monitoring_config=None, adjustment_rules=None,
):
    """Build ONE composite plan version spanning >=2 active domains.

    This carries the comprehensive-ONLY elements the thin ``plan_schema`` record path
    CANNOT hold (integrated narrative + dated milestones + compiled monitoring config
    + >=2 domains in one version) — the input that makes AC-1/AC-3 non-tautological.
    """
    return {
        "date": date,
        "domain_programs": programs if programs is not None else {
            "workout": _training_program(),
            "peptides": _compound_program(),
        },
        "narrative": narrative,
        "milestones": milestones if milestones is not None else [
            {"date": "2026-08-10", "label": "first re-test", "metric": "e1RM +5%"},
            {"date": "2026-09-14", "label": "mid-block panel", "metric": "IGF-1 in range"},
        ],
        "monitoring_config": monitoring_config if monitoring_config is not None else {
            "panels": ["IGF-1", "lipids"], "cadence_days": 30,
        },
        "adjustment_rules": adjustment_rules if adjustment_rules is not None else [
            {"trigger": "2 missed sessions", "action": "re-scope the week"},
        ],
    }


def _missing_elements(loaded, expected):
    """Count the comprehensive elements ABSENT from the round-tripped version.

    Every per-domain seven-field program field (for each domain), the narrative, the
    milestones, and the monitoring config must be present on load. Returns the list of
    missing element names — AC-1 asserts it is empty.
    """
    if not isinstance(loaded, dict):
        return ["<version-not-a-dict>"]
    missing = []
    progs = loaded.get("domain_programs")
    if not isinstance(progs, dict) or not progs:
        missing.append("domain_programs")
    else:
        fields = (
            domain_program.REQUIRED_FIELDS
            + domain_program.CONDITIONAL_FIELDS
            + (domain_program.KIND_FIELD,)
        )
        for name, program in expected["domain_programs"].items():
            loaded_program = progs.get(name)
            if not isinstance(loaded_program, dict):
                missing.append(f"domain_programs[{name}]")
                continue
            for field in fields:
                if field in program and field not in loaded_program:
                    missing.append(f"domain_programs[{name}].{field}")
    for element in ("narrative", "milestones", "monitoring_config"):
        if element not in loaded:
            missing.append(element)
    return missing


# --------------------------------------------------------------------------- #
# AC-1 — comprehensive round-trip (PRODUCTION-PATH, PF-S130-01 load-bearing)
# --------------------------------------------------------------------------- #


def test_comprehensive_round_trip_production_path(tmp_path):
    """A >=2-domain version + narrative + milestones + config survives record->load intact."""
    version = _comprehensive_version()
    plan_model.record_plan_version(version, tmp_path)  # REAL record -> store.append
    resolved = plan_model.read_plan_version(version["date"], tmp_path)  # REAL resolve/read

    assert resolved["state"] is None  # standing, not an absence state
    loaded = resolved["version"]
    assert _missing_elements(loaded, version) == []
    # well-typed spot checks across the comprehensive-only elements
    assert isinstance(loaded["narrative"], str) and loaded["narrative"]
    assert len(loaded["domain_programs"]) == 2
    assert loaded["monitoring_config"]["cadence_days"] == 30
    assert all(isinstance(m["date"], str) for m in loaded["milestones"])


# --------------------------------------------------------------------------- #
# AC-1b — fail-closed rejection of a partial version (QA-04, MUST)
# --------------------------------------------------------------------------- #


def _drop(element):
    def mutate(version):
        del version[element]
    return mutate


def _set(element, value):
    def mutate(version):
        version[element] = value
    return mutate


def _nonconformant_program(version):
    # a compound program with an EMPTY required_labs -> domain_program.validate rejects
    version["domain_programs"]["peptides"] = _compound_program(required_labs=[])


@pytest.mark.parametrize(
    "mutate,token",
    [
        (_drop("domain_programs"), "domain_programs"),
        (_drop("narrative"), "narrative"),
        (_drop("milestones"), "milestones"),
        (_drop("monitoring_config"), "monitoring_config"),
        (_nonconformant_program, "peptides"),
        # TEST-01: the version-date guard (_check_date) — real-date, regex, and None branches.
        (_set("date", "2026-13-01"), "date"),
        (_set("date", "not-a-date"), "date"),
        (_drop("date"), "date"),
        # TEST-02 / API-01: undated milestone (no "date" key) is rejected naming milestones.
        (_set("milestones", [{"label": "first re-test"}]), "milestones"),
        # BUG-02 / API-01: a milestone carrying a MALFORMED date fails closed (per-milestone
        # _check_date), and an EMPTY monitoring_config is rejected (non-empty parity).
        (_set("milestones", [{"date": "2026-13-40", "label": "first re-test"}]), "milestones"),
        (_set("monitoring_config", {}), "monitoring_config"),
    ],
)
def test_partial_version_rejected_fail_closed(tmp_path, mutate, token):
    """A partial/non-conformant version RAISES a typed error naming it; 0 stored."""
    version = _comprehensive_version()
    mutate(version)
    with pytest.raises(plan_model.PlanVersionError) as excinfo:
        plan_model.record_plan_version(version, tmp_path)
    message = str(excinfo.value)
    offending = getattr(excinfo.value, "offending_element", "") or ""
    assert token in message or token in offending
    assert store.read(plan_model._PREFIX_MODEL, root=tmp_path) == []  # nothing persisted


# --------------------------------------------------------------------------- #
# AC-2 — round-trip fidelity, FULL variant space (three independent falsifiers)
# --------------------------------------------------------------------------- #


def test_periodization_survives_round_trip(tmp_path):
    """Every dated periodization block survives store->load with its dates intact."""
    version = _comprehensive_version()
    plan_model.record_plan_version(version, tmp_path)
    loaded = plan_model.read_plan_version(version["date"], tmp_path)["version"]
    for name, program in version["domain_programs"].items():
        expected_blocks = program["prescription"]["blocks"]
        loaded_blocks = loaded["domain_programs"][name]["prescription"]["blocks"]
        assert len(loaded_blocks) == len(expected_blocks)
        assert [b["date"] for b in loaded_blocks] == [b["date"] for b in expected_blocks]


def test_milestones_survive_round_trip(tmp_path):
    """The dated milestones survive store->load with 0 dropped (count + dates intact)."""
    version = _comprehensive_version()
    plan_model.record_plan_version(version, tmp_path)
    loaded = plan_model.read_plan_version(version["date"], tmp_path)["version"]
    assert len(loaded["milestones"]) == len(version["milestones"])
    assert [m["date"] for m in loaded["milestones"]] == [m["date"] for m in version["milestones"]]


def test_monitoring_config_survives_round_trip(tmp_path):
    """The compiled monitoring config survives store->load intact (0 entries dropped)."""
    version = _comprehensive_version()
    plan_model.record_plan_version(version, tmp_path)
    loaded = plan_model.read_plan_version(version["date"], tmp_path)["version"]
    assert loaded["monitoring_config"] == version["monitoring_config"]


# --------------------------------------------------------------------------- #
# AC-3 — standing resolution (PRODUCTION-PATH) + AC-3b absence branches
# --------------------------------------------------------------------------- #


def test_dated_comprehensive_plan_resolves_standing(tmp_path):
    """A version dated the render date resolves STANDING carrying the comprehensive elements."""
    render = "2026-07-13"
    version = _comprehensive_version(date=render)
    plan_model.record_plan_version(version, tmp_path)
    resolved = plan_model.read_plan_version(render, tmp_path)

    assert resolved["state"] is None  # standing, NOT NO_PLAN / NO_PLAN_TODAY
    assert resolved["plan_date"] == render
    standing = resolved["version"]
    assert standing["narrative"] == version["narrative"]
    assert len(standing["milestones"]) == len(version["milestones"])
    assert standing["monitoring_config"] == version["monitoring_config"]
    assert set(standing["domain_programs"]) == {"workout", "peptides"}


def test_resolve_comprehensive_absence_states(tmp_path):
    """Zero readings -> NO_PLAN; readings none dated on_date -> NO_PLAN_TODAY + max date."""
    empty = plan_model.resolve_comprehensive([], "2026-07-13")
    assert empty["state"] == plan_model.NO_PLAN
    assert empty["version"] is None and empty["plan_date"] is None
    assert plan_model.read_plan_version("2026-07-13", tmp_path)["state"] == plan_model.NO_PLAN

    plan_model.record_plan_version(_comprehensive_version(date="2026-07-10"), tmp_path)
    plan_model.record_plan_version(
        _comprehensive_version(date="2026-07-12", narrative="a distinct later version"), tmp_path
    )
    resolved = plan_model.read_plan_version("2026-07-13", tmp_path)
    assert resolved["state"] == plan_model.NO_PLAN_TODAY
    assert resolved["version"] is None
    assert resolved["plan_date"] == "2026-07-12"  # the latest on-file date


def test_resolve_same_date_latest_append_wins(tmp_path):
    """TEST-03(a): two DISTINCT versions at ONE on_date -> the LATER-recorded narrative stands.

    Both persist (distinct content tags); the reversed-scan tie-break returns the LAST-appended
    version dated on_date. REDs if resolve scanned forward / first-wins (it would return the
    earlier narrative).
    """
    render = "2026-07-13"
    plan_model.record_plan_version(
        _comprehensive_version(date=render, narrative="the earlier-recorded version"), tmp_path
    )
    plan_model.record_plan_version(
        _comprehensive_version(date=render, narrative="the later-recorded version"), tmp_path
    )
    resolved = plan_model.read_plan_version(render, tmp_path)
    assert resolved["state"] is None
    assert resolved["version"]["narrative"] == "the later-recorded version", (
        "the LAST-appended version dated on_date must win the reversed-scan resolve"
    )


def test_resolve_backdated_exact_date_stands(tmp_path):
    """TEST-03(b): a backdated on_date resolves the EXACT-date version STANDING, not the latest.

    Versions dated 07-10 + 07-12 on file; resolving on_date=07-10 returns the 07-10 version
    STANDING (state None), NOT NO_PLAN_TODAY and NOT the latest-on-file 07-12 version. REDs if
    resolve returned the latest reading instead of the exact-date match.
    """
    plan_model.record_plan_version(
        _comprehensive_version(date="2026-07-10", narrative="the 07-10 version"), tmp_path
    )
    plan_model.record_plan_version(
        _comprehensive_version(date="2026-07-12", narrative="the later 07-12 version"), tmp_path
    )
    resolved = plan_model.read_plan_version("2026-07-10", tmp_path)
    assert resolved["state"] is None, "an exact-date match is a STANDING state, not an absence"
    assert resolved["plan_date"] == "2026-07-10"
    assert resolved["version"]["narrative"] == "the 07-10 version", (
        "the exact-date version must resolve, not the latest-on-file 07-12 version"
    )


# --------------------------------------------------------------------------- #
# AC-4 — per-ADR freeze-break numstat (the value rides the frozen primitive)
# --------------------------------------------------------------------------- #


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


def test_frozen_store_primitive_numstat_zero():
    # The value rides the FROZEN write primitive + inner engine UNCHANGED (disposition #14).
    assert _numstat(PRE_TASK_HEAD, "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py") == ""
    assert _numstat(PRE_TASK_HEAD, "scripts/store/store.py", "scripts/store/keying.py") == ""
    # the <always-frozen> 6-file HARD glob vs the pre-build trunk
    assert _numstat(
        "origin/main",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py", "scripts/plan/router.py",
    ) == ""


def test_plan_schema_superseded_set_is_exactly_named():
    # The plan_schema.py delta touches ONLY the superseded record spine. The NON-superseded
    # functions stay byte-identical to origin/main (0 unnamed edits). The PLAN_DOMAINS tuple is
    # CARVED OUT — ADR-0043-T3 (Wave 4) grew the dispatch registry from the closed four to the
    # §1-§13 card roster (tuple(sorted(activation.CARD_DOMAINS))); behavioral guarantor
    # tests/plan/test_activation.py::test_registries_coherent_over_grown_roster. Wave-4 frozen-guard
    # reconciliation (F-011), Architect Option-A ruling.
    base = subprocess.run(
        ["git", "show", "origin/main:scripts/store/plan_schema.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    current = (REPO_ROOT / "scripts/store/plan_schema.py").read_text(encoding="utf-8")
    for name in ("correct_plan", "record_plan_tracking", "resolve_tracking", "read_plan_tracking"):
        assert _func_src(current, name) == _func_src(base, name), (
            f"non-superseded plan_schema function {name!r} changed — it must stay byte-frozen"
        )


# --------------------------------------------------------------------------- #
# AC-5 — store-adversarial battery (bead pka): all four categories
# --------------------------------------------------------------------------- #


def test_cross_stream_disjoint(tmp_path):
    # (a) cross-stream namespace collision: the plan-model:: read never returns a thin
    # plan::<domain> value NOR the SEC-01 item-"" decoy. The item-"" decoy is seeded AFTER
    # the version and dated on_date so that IF the prefix were blanked (write+read relocate
    # to item ""), it would win the reversed-scan resolve and be returned (mutation (d)-1).
    root = tmp_path
    version = _comprehensive_version(date="2026-07-13")
    on_date = version["date"]
    plan_model.record_plan_version(version, root)
    plan_schema.record_plan(
        "workout", {"exercises": [{"name": "Squat", "sets": 3}]}, on_date, "coach", root
    )
    store.append(
        "", _reading("", on_date, "decoy-empty-item", "FOREIGN-ITEM-EMPTY"), root=root
    )

    resolved = plan_model.read_plan_version(on_date, root)
    assert resolved["state"] is None
    assert resolved["version"] == version  # the real composite, never a foreign/thin value
    assert resolved["version"] != "FOREIGN-ITEM-EMPTY"

    model_readings = store.read(plan_model._PREFIX_MODEL, root=root)
    assert model_readings, "the plan-model stream is empty (the disjointness check would be vacuous)"
    assert all(r["item"] == plan_model._PREFIX_MODEL for r in model_readings)
    assert not any(r["value"] == "FOREIGN-ITEM-EMPTY" for r in model_readings)
    # the thin decoy persisted in ITS OWN stream (the cross-check is not vacuous)
    assert store.read("plan::workout", root=root)[0]["value"] == {
        "exercises": [{"name": "Squat", "sets": 3}]
    }


def test_same_timepoint_two_versions_persist(tmp_path):
    # (b) same-timepoint dedupe: two DISTINCT versions at ONE timepoint (distinct
    # content-tag sources) BOTH persist; an identical re-record is an idempotent no-op.
    root = tmp_path
    v1 = _comprehensive_version(date="2026-07-13")
    v2 = _comprehensive_version(date="2026-07-13", narrative="a distinct second version")
    plan_model.record_plan_version(v1, root)
    plan_model.record_plan_version(v2, root)
    readings = store.read(plan_model._PREFIX_MODEL, root=root)
    assert len(readings) == 2, f"two distinct versions at one timepoint did not both persist: {len(readings)}"
    assert len({r["source"] for r in readings}) == 2  # distinct version-key sources

    plan_model.record_plan_version(v1, root)  # identical re-record
    assert len(store.read(plan_model._PREFIX_MODEL, root=root)) == 2  # 0 duplicate lines


def test_dedupe_key_boundary_and_no_new_keying(tmp_path):
    # (c-i) 0 new dedupe-key / keying logic in plan_model.py — the identity stays keying's
    # frozen (item, timepoint, source), reached ONLY through store.append.
    source = (REPO_ROOT / "scripts/store/plan_model.py").read_text(encoding="utf-8")
    for token in ("DEDUPE_FIELDS", "dedupe_key", "LINE_FIELDS", "_DEDUPE_EXCLUDED"):
        assert token not in source, f"plan_model.py re-defines store keying logic: {token!r}"

    # (c-ii) same (item, timepoint, source) + a CHANGED value is a store-dedupe no-op:
    # the second write is DROPPED, the first value wins, store.read returns 1 (never a
    # silent overwrite). Exercised directly through the frozen store.append.
    root = tmp_path
    item = plan_model._PREFIX_MODEL
    v1 = _comprehensive_version(date="2026-07-13")
    v2 = _comprehensive_version(date="2026-07-13", narrative="a changed value at the same key")
    store.append(item, _reading(item, "2026-07-13", "fixed-src", v1), root=root)
    store.append(item, _reading(item, "2026-07-13", "fixed-src", v2), root=root)  # same key, changed value
    readings = store.read(item, root=root)
    assert len(readings) == 1  # the value-excluded key dropped the second write
    assert readings[0]["value"] == v1  # the first value stands (no silent overwrite)


# --------------------------------------------------------------------------- #
# AC-6 — suite-local green + 0 real operator PII in the test tree
# --------------------------------------------------------------------------- #


def test_no_operator_identity_literal_in_test_tree():
    source = Path(__file__).read_text(encoding="utf-8").lower()
    # Assembled from splits so the guard's own token list never self-matches.
    forbidden = ["".join(parts) for parts in (
        ("wal", "ter"), ("mcgiv", "ney"), ("wmcgiv", "ney"), ("@", "gmail"),
    )]
    for token in forbidden:
        assert token not in source, "a real operator-identity literal leaked into the test tree"
