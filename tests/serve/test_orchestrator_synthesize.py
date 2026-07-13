"""Leg-1-preserved + Leg-2-additive synthesize / front-door / roster-growth (ADR-0043-T3, OPTION 2).

The Wave-4 atomic change: grow the dispatch roster 4 -> the §1-§13 card roster (DERIVED from
``activation.CARD_DOMAINS``), WRAP the composed safety gate at the front door (Leg 1 preserved),
ADD the care-agent synthesize step ON TOP (Leg 2 — one comprehensive plan version recorded via
``plan_model.record_plan_version`` only after the gate surfaces a pass), and land the six co-landing
review beads (ncsy / qrg4 / pule / ubsp / 61cy / _check_plan_args).

Everything is SYNTHETIC — scratch ``tmp_path`` stores, 0 live-API, 0 real operator PII (AC-6). The
front-door drives (AC-4/AC-7/AC-UF/AC-BP/AC-S2/AC-S3) run the REAL ``regenerate`` production path so a
revert of the active-subset narrowing / the additive record / the roster growth drives them RED
(PF-S130-01 non-tautology — proven per-mutation in Step 2.5).
"""

import datetime
import functools
import subprocess
from pathlib import Path

import pytest

from scripts.plan import activation, domain_program, orchestrate
from scripts.plan import plan_driver
from scripts.plan.assemble import PROGRAM_KEY
from scripts.plan.safety_review import DEFAULT_LENSES
from scripts.serve import care_chat, plan_loop
from scripts.store import plan_confirm, plan_model, plan_schema, store

from tests.plan.test_deid_in import _FixedDeidClient
from tests.plan.test_generate_plan import (
    _author,
    _nutrition_meal_rec,
    _nutrition_target_rec,
    _peptide_rec,
    _supplement_rec,
    _workout_rec,
)
from tests.plan.test_orchestrate import _nutrition, _recon
from tests.plan.test_plan_orchestrator import _deid_summary
from tests.plan.test_quality_judge import _clean_scores
from tests.store.test_plan_model import _compound_program, _training_program
from tests.serve.test_plan_loop import _seed_prior_standing

REPO_ROOT = Path(__file__).resolve().parents[2]


# The DURABLE per-wave numstat base: the Wave-4 fork-point (the pre-Wave-4 main tip = the S132-close
# merge #335). A permanent main ancestor, so its numstat vs HEAD equals the wave's diff on the feature
# branch, on squashed main, AND on a fresh clone. NOT an intermediate feature-branch SHA (the wdhc
# orphan flaw) and NOT the dynamic merge-base(origin/main, HEAD): once the wave squash-merges, that
# merge-base collapses to HEAD, emptying the per-wave diff and failing the freeze-break (PF-S133-03).
# Mirrors test_plan_model_reader.py:32's durable-fork-point pattern (the Wave-3 SF-1/wdhc fix).
PRE_TASK_HEAD = "ec8071503a983ed59c8dd230ded05ee5bd9087c5"
_JUDGE_ROLE = plan_loop.JUDGE_ROLE


# --------------------------------------------------------------------------- #
# Synthetic front-door fixtures (0 live spend).
# --------------------------------------------------------------------------- #


class _LoopDispatch:
    """Unified subscription dispatch: routes specialist / judge / lens by the first arg."""

    def __init__(self, authors, *, judge_scores=None, lens_findings=None):
        self.authors = authors
        self.judge_scores = judge_scores if judge_scores is not None else _clean_scores()
        self.lens_findings = lens_findings or {}
        self.calls = []

    def __call__(self, name, prompt, context):
        self.calls.append(name)
        if name == _JUDGE_ROLE:
            return dict(self.judge_scores)
        if name in DEFAULT_LENSES:
            return list(self.lens_findings.get(name, []))
        return self.authors[name]


def _rich_author(domain, *, program=None):
    """A rich-domain (§5-§13) author envelope carrying an embedded seven-field DOMAIN PROGRAM."""
    prog = program if program is not None else _training_program()
    return {
        "specialist": plan_driver._ROLE_OF_DOMAIN.get(domain, f"{domain}-specialist"),
        "recommendations": [{
            "claim": f"a {domain} program for the operator",
            "source": "vetted library", "confidence_tier": "established",
            "reversibility": "reversible", "category": domain,
            "payload": {}, PROGRAM_KEY: prog,
        }],
    }


def _clean_authors(*, extra=None):
    """Clean renderable authors (disjoint compounds -> no additive-AE hold) that all record.

    The workout rec carries a `load` so the ADR-0015 clearance strip (no clearance) is exercised —
    AC-UF (c) asserts only `load` is removed, the movement/sets/reps survive.
    """
    authors = {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3, load="60% 1RM")),
                          energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
        "supplements": _author(_supplement_rec("Creatine", "5 g"),
                              specialist="supplement-specialist"),
        "peptides": _author(_peptide_rec("BPC-157", "250 mcg", "subq"),
                          specialist="peptide-specialist"),
    }
    if extra:
        authors.update(extra)
    return authors


def _blocking_dispatch(authors):
    """A dispatch whose safety lens emits a finding -> the composed gate blocks (SAFETY_BLOCKED)."""
    lens = sorted(DEFAULT_LENSES)[0]
    return _LoopDispatch(authors, lens_findings={
        lens: [{"finding_id": "synthetic-block", "caution": "synthetic safety hold",
                "severity": "high"}]})


def _seed_surface_store(root, *, goal_domains, extra=None):
    """Seed a PII-free operator state whose `router.summarize` activates `goal_domains`.

    `goal_domains` is the space-joined card-domain slug list the deriver projects into the surface's
    `goals` channel (a subset of `activation.CARD_DOMAINS`). Core fields back the summary field-set.
    """
    from scripts.store import keying

    fields = {
        "goal-domains": " ".join(goal_domains),
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
    }
    if extra:
        fields.update(extra)
    for item, value in fields.items():
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": "2026-07-13", "source": "intake", "value": value},
            root=root,
        )
    return functools.partial(store.read, root=root)


def _drive_regenerate(root, dispatch, *, plan_date):
    """Drive the real `regenerate` production path over a synthetic dispatch/deid seam."""
    return plan_loop.regenerate(
        root, dispatch=dispatch, deid_client=_FixedDeidClient(_deid_summary()),
        plan_date=plan_date, trigger="test")


# =========================================================================== #
# GROUP A — core-atomic
# =========================================================================== #


def test_synthesize_emits_one_integrated_plan(tmp_path):
    # AC-1: the synthesize step composes ONE integrated comprehensive version carrying dated
    # milestones (NOT a per-domain results map with no synthesis). A per-domain-only shape reds.
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition"])
    dispatch = _LoopDispatch(_clean_authors())
    _drive_regenerate(root, dispatch, plan_date="2026-07-13")
    resolved = plan_model.read_plan_version("2026-07-13", root)
    assert resolved["state"] is None, "no standing comprehensive version was recorded"
    version = resolved["version"]
    assert version[plan_model.MILESTONES], "the integrated version carries no milestones"
    assert isinstance(version[plan_model.DOMAIN_PROGRAMS], dict) and version[plan_model.DOMAIN_PROGRAMS]


def test_synthesized_plan_carries_dated_milestones(tmp_path):
    # AC-2: the synthesized version carries >=1 DATED milestone (passes validate_plan_version).
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition"])
    _drive_regenerate(root, _LoopDispatch(_clean_authors()), plan_date="2026-07-13")
    version = plan_model.read_plan_version("2026-07-13", root)["version"]
    milestones = version[plan_model.MILESTONES]
    assert len(milestones) >= 1
    for m in milestones:
        assert "date" in m and isinstance(m["date"], str)


def test_regenerate_wraps_gate_then_synthesizes(tmp_path, monkeypatch):
    # AC-3: regenerate's call graph REACHES run_orchestrated(loop_enabled) + compose_disposition
    # (Leg 1 preserved) AND the synthesize + record_plan_version step (Leg 2 additive). The driver
    # imports compose_disposition lazily from scripts.plan.gate_dispatch inside `drive`, so a spy on
    # gate_dispatch.compose_disposition observes Leg 1; a spy on plan_model.record_plan_version
    # observes Leg 2.
    from scripts.plan import gate_dispatch as gd

    composed, recorded = [], []
    real_compose = gd.compose_disposition
    real_record = plan_model.record_plan_version
    monkeypatch.setattr(gd, "compose_disposition",
                        lambda *a, **k: (composed.append(1), real_compose(*a, **k))[1])
    monkeypatch.setattr(plan_model, "record_plan_version",
                        lambda *a, **k: (recorded.append(1), real_record(*a, **k))[1])

    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition"])
    _drive_regenerate(root, _LoopDispatch(_clean_authors()), plan_date="2026-07-13")
    assert composed, "Leg 1's compose_disposition (the composed gate) never fired"
    assert recorded, "Leg 2's record_plan_version (the additive comprehensive record) never fired"


def test_front_door_dispatches_active_domains(tmp_path):
    # AC-4: the front door dispatches activation.active_domains(surface), NOT the closed grown tuple.
    # A narrow surface dispatches a proper subset of the renderable four.
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition"])
    dispatch = _LoopDispatch(_clean_authors())
    _drive_regenerate(root, dispatch, plan_date="2026-07-13")
    dispatched_specialists = {c for c in dispatch.calls
                              if c not in DEFAULT_LENSES and c != _JUDGE_ROLE}
    assert dispatched_specialists == {"workout", "nutrition"}, dispatched_specialists
    assert dispatched_specialists != set(plan_schema.PLAN_DOMAINS)


def test_per_adr_scoped_freeze_break_numstat():
    # AC-5: the growth/wiring surfaces are NON-empty vs PRE_TASK_HEAD; the frozen four + the
    # always-frozen HARD six are EMPTY. Subprocess git diff (mirrors test_generate_plan_uniform).
    grown = [
        "scripts/store/plan_schema.py", "scripts/plan/plan_driver.py",
        "scripts/plan/generate_plan.py", "scripts/serve/care_chat.py",
        "scripts/serve/plan_loop.py", "scripts/serve/server.py",
        "scripts/plan/orchestrate.py", "scripts/plan/domain_program.py",
        "scripts/store/plan_model.py",
    ]
    out = subprocess.run(
        ["git", "diff", "--numstat", PRE_TASK_HEAD, "--", *grown],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    assert out.strip(), "the growth/wiring surfaces must be NON-empty vs PRE_TASK_HEAD"

    frozen_scoped = ["scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
                     "scripts/store/store.py", "scripts/store/keying.py"]
    out = subprocess.run(
        ["git", "diff", "--numstat", PRE_TASK_HEAD, "--", *frozen_scoped],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    assert out.strip() == "", f"a scoped-frozen file changed: {out}"

    always_frozen = ["scripts/store/store.py", "scripts/store/keying.py",
                     "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
                     "scripts/plan/adjust.py", "scripts/plan/router.py"]
    out = subprocess.run(
        ["git", "diff", "--numstat", "origin/main", "--", *always_frozen],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    assert out.strip() == "", f"an always-frozen HARD file changed vs origin/main: {out}"


def test_module_green_no_live_client(tmp_path):
    # AC-6: the module runs with 0 live-API, 0 real PII — a grep confirms 0 live-client construction
    # + no real operator-identity literal. Needles are concatenated at runtime so they never
    # self-match this assertion's own source text.
    src = Path(__file__).read_text(encoding="utf-8")
    assert ("Model" + "Client(") not in src, "no live ModelClient may be constructed"
    assert ("wmcgiv" + "ney") not in src, "no real operator identity literal"
    assert ("@gmail" + ".com") not in src, "no real operator email literal"


def test_rich_domain_dispatches_and_records_first_class(tmp_path):
    # AC-7 (PF-S130-01): a rich domain D beyond the four (sleep), active in the surface, is authored
    # + reconciled through the always-on floors and records FIRST-CLASS in the comprehensive version
    # via plan_model.record_plan_version -> read_plan_version round-trips D's program. RED against
    # the un-grown tree (sleep not a PLAN_DOMAINS member -> never dispatched/folded).
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition", "sleep"])
    authors = _clean_authors(extra={"sleep": _rich_author("sleep")})
    _drive_regenerate(root, _LoopDispatch(authors), plan_date="2026-07-13")
    version = plan_model.read_plan_version("2026-07-13", root)["version"]
    assert "sleep" in version[plan_model.DOMAIN_PROGRAMS], version[plan_model.DOMAIN_PROGRAMS].keys()
    domain_program.validate(version[plan_model.DOMAIN_PROGRAMS]["sleep"])


def test_plan_domains_grown_to_card_roster():
    # AC-8: the roster grew to the §1-§13 card roster.
    assert len(plan_schema.PLAN_DOMAINS) >= 13


def test_front_door_records_active_subset_not_all_domains(tmp_path):
    # AC-9: the front door records the active SUBSET (via plan_model), NOT set(results)==PLAN_DOMAINS.
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition"])
    _drive_regenerate(root, _LoopDispatch(_clean_authors()), plan_date="2026-07-13")
    programs = plan_model.read_plan_version("2026-07-13", root)["version"][plan_model.DOMAIN_PROGRAMS]
    assert set(programs) == {"workout", "nutrition"}
    assert set(programs) != set(plan_schema.PLAN_DOMAINS)


def test_registries_coherent_over_grown_roster():
    # AC-10: set(PLAN_DOMAINS) <= _PLAN_TRANSLATORS & _ROLE_OF_DOMAIN & _DOMAIN_KIND (0 orphan).
    from scripts.plan import generate_plan

    members = set(plan_schema.PLAN_DOMAINS)
    assert members <= set(generate_plan._PLAN_TRANSLATORS)
    assert members <= set(plan_driver._ROLE_OF_DOMAIN)
    assert members <= set(generate_plan._DOMAIN_KIND)


def test_plan_domains_derives_from_card_domains():
    # AC-11 / sgur A3: PLAN_DOMAINS is DERIVED from activation.CARD_DOMAINS (not two literals
    # asserted equal). The derivation propagates: a CARD_DOMAINS member appears in PLAN_DOMAINS,
    # and the set-equality holds structurally.
    assert set(plan_schema.PLAN_DOMAINS) == set(activation.CARD_DOMAINS)
    # derivation-propagation: injecting a synthetic card domain into the source set the derivation
    # reads must propagate into a freshly-derived PLAN_DOMAINS (two independent literals would not).
    import importlib

    injected = frozenset(activation.CARD_DOMAINS | {"synthetic-card-domain"})
    orig = activation.CARD_DOMAINS
    try:
        activation.CARD_DOMAINS = injected
        reloaded = importlib.reload(plan_schema)
        assert "synthetic-card-domain" in set(reloaded.PLAN_DOMAINS)
    finally:
        activation.CARD_DOMAINS = orig
        importlib.reload(plan_schema)


def test_grown_roster_consumers_tolerate_growth(tmp_path):
    # AC-D1 (RULING D1): each grown-roster iterator consumer behaves correctly over the grown roster.
    from scripts.plan import horizons, plan_orchestrator, tailoring
    from scripts.serve import confirm

    # tailoring._TAILORING_SECTION_KEYS grows in lockstep (derived).
    assert set(tailoring._TAILORING_SECTION_KEYS) == set(plan_schema.PLAN_DOMAINS)
    # plan_orchestrator.DEFAULT_DOMAINS stays the four (decoupled).
    assert set(plan_orchestrator.DEFAULT_DOMAINS) == {"workout", "nutrition", "supplements", "peptides"}
    # confirm.confirm_plan_change on a rich member no longer ValueErrors on the unknown-domain check.
    root = tmp_path / "store"
    root.mkdir(parents=True, exist_ok=True)
    try:
        confirm.confirm_plan_change("sleep", "2026-07-13", "confirmed", root=root)
    except ValueError as exc:
        assert "unknown" not in str(exc).lower(), f"rich domain rejected as unknown: {exc}"
    except Exception:
        pass  # any non-unknown-domain path (no pointer, etc.) is fine
    # horizons.domain_horizons over a store with no rich data returns 0 spurious horizon for sleep
    # (absence-tolerant: the grown roster iterates sleep, but the state/TRACKED_DOMAINS filter skips it).
    horizons_out = horizons.domain_horizons(root, "2026-07-13")
    assert "sleep" not in {h.get("domain") for h in horizons_out}


def test_operator_surface_deriver_is_deid_safe(tmp_path):
    # AC-S1 (RULING 2, crown-jewel): the derived surface's channel values are card slugs only, and a
    # summary seeded with a synthetic raw-PII / raw-genotype token carries 0 such token.
    raw_email = "op.user" + chr(64) + "example.invalid"  # a synthetic PII-shaped token
    surface = plan_loop.derive_operator_surface({
        "goal-domains": f"workout rs1801133-AA-RAW-GENOTYPE {raw_email}",
        "genetic-trait-classes": "rs9999-GG-raw",
        "active-issue-class": "musculoskeletal",
    })
    known = set(activation.CARD_DOMAINS) | set(activation.CROSS_CUTTING_INPUTS)
    for channel, values in surface.items():
        for v in values:
            assert v in known, f"non-slug token {v!r} leaked into channel {channel!r}"
    flat = " ".join(v for values in surface.values() for v in values)
    assert "RAW" not in flat and "example.invalid" not in flat and "rs9999" not in flat


def test_front_door_derives_surface_then_dispatches_active_subset(tmp_path):
    # AC-S2: the front door DERIVES the surface then dispatches exactly active_domains(surface).
    root = tmp_path / "store"
    read = _seed_surface_store(root, goal_domains=["workout", "sleep"])
    from scripts.plan import router

    surface = plan_loop.derive_operator_surface(router.summarize(read))
    active = activation.active_domains(surface)
    assert active == {"workout", "sleep"}, active
    dispatch = _LoopDispatch(_clean_authors(extra={"sleep": _rich_author("sleep")}))
    _drive_regenerate(root, dispatch, plan_date="2026-07-13")
    dispatched = {c for c in dispatch.calls if c not in DEFAULT_LENSES and c != _JUDGE_ROLE}
    assert dispatched == {"workout", "sleep"}, dispatched


def test_rich_only_surface_floors_to_renderable_core():
    # AC-S4 (renderable-core floor, plan_loop.active_plan_domains): a RICH-only surface — a
    # genetics/labs cross-cutting touch with NO renderable-domain signal — activates NO card
    # domain, so active_plan_domains FLOORS it to EXACTLY the four RENDERABLE_DOMAINS (the
    # baseline plan; never zero out an existing operator's plan). RED capability: drop the
    # `active |= RENDERABLE_DOMAINS` floor and the surface resolves to the EMPTY set instead.
    summary = {"genetic-trait-classes": "genetics"}  # rich cross-cutting substrate, no card domain
    surface = plan_loop.derive_operator_surface(summary)
    assert activation.active_domains(surface) == frozenset(), "surface must carry no active card domain"
    assert plan_loop.active_plan_domains(summary) == set(plan_schema.RENDERABLE_DOMAINS)


def test_debounce_floor_engages_after_comprehensive_regen(tmp_path):
    # AC-S3 (RULING 1 consequence): after a comprehensive re-gen the debounce floor engages —
    # _last_regen_date advances from the recorded comprehensive version (a renderable-LESS all-rich
    # re-gen writes NO thin plan:: row, so a plan::-only marker would starve). Non-tautological under
    # OPTION 2 per the caveat.
    root = tmp_path / "store"
    root.mkdir(parents=True, exist_ok=True)
    # record ONLY a comprehensive (plan-model::) version, no thin plan:: rows.
    version = {
        plan_model.VERSION_DATE: "2026-07-13",
        plan_model.DOMAIN_PROGRAMS: {"sleep": _training_program(), "recovery": _training_program()},
        plan_model.NARRATIVE: "All-rich comprehensive re-gen.",
        plan_model.MILESTONES: [{"date": "2026-07-20", "label": "re-test"}],
        plan_model.MONITORING_CONFIG: {"cadence_days": 30},
    }
    plan_model.record_plan_version(version, root)
    read = functools.partial(store.read, root=root)
    assert plan_loop._last_regen_date(read, "2026-07-14") == "2026-07-13"


def test_usable_plan_floor_normal_safe_plan_records_full_comprehensive(tmp_path):
    # AC-UF (usability floor): a normal SAFE plan (a) passes the composed gate (safety_passed True),
    # (b) records a FULL comprehensive version (narrative + >=1 dated milestone + non-empty
    # monitoring_config + >=2 domain_programs; NOT SAFETY_BLOCKED / shell), (c) the workout program
    # RETAINS its exercises (the strip removes only `load`).
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout", "nutrition", "supplements", "peptides"])
    result = _drive_regenerate(root, _LoopDispatch(_clean_authors()), plan_date="2026-07-13")
    assert result.get("reason") != plan_driver.SAFETY_BLOCKED
    resolved = plan_model.read_plan_version("2026-07-13", root)
    assert resolved["state"] is None, "a normal safe plan recorded NO standing comprehensive version"
    version = resolved["version"]
    assert isinstance(version[plan_model.NARRATIVE], str) and version[plan_model.NARRATIVE]
    assert version[plan_model.MILESTONES]
    assert version[plan_model.MONITORING_CONFIG]
    programs = version[plan_model.DOMAIN_PROGRAMS]
    assert len(programs) >= 2, programs.keys()
    workout_presc = programs["workout"][domain_program.PRESCRIPTION]
    assert not _contains_load(workout_presc), "the clearance strip left a load prescription"
    assert _has_movement(workout_presc), "the strip hollowed the workout to no exercises"


def test_blocked_regen_preserves_prior_plan(tmp_path):
    # AC-BP: a blocked re-gen returns SAFETY_BLOCKED, records NO new comprehensive version (the prior
    # stands byte-identical), 0 partial write for the re-gen date.
    root = tmp_path / "store"
    # A rich domain (sleep) is active so a record-on-block mutation (moving synthesize before the
    # pass-guard) would author+record sleep's rich program on the block — AC-BP catches that.
    _seed_surface_store(root, goal_domains=["workout", "nutrition", "sleep"])
    prior = {
        plan_model.VERSION_DATE: "2026-07-06",
        plan_model.DOMAIN_PROGRAMS: {"workout": _training_program(), "peptides": _compound_program()},
        plan_model.NARRATIVE: "Prior standing plan.",
        plan_model.MILESTONES: [{"date": "2026-07-20", "label": "re-test"}],
        plan_model.MONITORING_CONFIG: {"cadence_days": 30},
    }
    plan_model.record_plan_version(prior, root)
    before = store.read(plan_model._PREFIX_MODEL, root=root)

    blocking = _blocking_dispatch(_clean_authors(extra={"sleep": _rich_author("sleep")}))
    result = _drive_regenerate(root, blocking, plan_date="2026-07-13")
    assert result.get("reason") == plan_driver.SAFETY_BLOCKED
    after = store.read(plan_model._PREFIX_MODEL, root=root)
    assert after == before, "the blocked re-gen mutated the comprehensive version stream"
    # 0 partial write for the re-gen date: no standing version dated 2026-07-13.
    assert plan_model.read_plan_version("2026-07-13", root)["state"] is not None
    # no thin plan:: rows for the re-gen date either.
    for d in plan_schema.RENDERABLE_DOMAINS:
        rows = [r for r in store.read(f"plan::{d}", root=root) if r["timepoint"] == "2026-07-13"]
        assert rows == [], f"{d} partial-wrote a thin row on a blocked re-gen"


# --- FIX A safety cluster (Tier-3 W4-02 / HCR-01 / W4-01) ---------------------------
# The rich-domain leg of care_chat.synthesize is under-processed vs the renderable leg: it must
# VALIDATE (drop non-conformant) and LOAD-STRIP each rich program before folding (mirror the
# renderable leg), and plan_loop.regenerate's ADR-0040 hold + rich-author dispatch must be robust to
# a Leg-2 raise. Each test is a per-mutation revert-RED (PF-S130-01 non-tautology).


def _rich_author_env(program):
    """A rich-domain author envelope carrying a single embedded program under PROGRAM_KEY."""
    return {"specialist": "sleep-specialist", "recommendations": [{PROGRAM_KEY: program}]}


def test_synthesize_drops_nonconformant_rich_program(tmp_path):
    # W4-02: a rich author returning a PRESENT-but-non-conformant program (missing monitoring_signals)
    # is DROPPED at the fold (mirror generate_plan._lift_program), not folded to crash the downstream
    # monitoring_compiler.compile_config (KeyError on program[MONITORING_SIGNALS]). synthesize records
    # ONLY the conformant programs and does NOT raise. REDs (KeyError) if the validate/drop is removed.
    root = tmp_path / "store"
    read = _seed_surface_store(root, goal_domains=["workout"])
    run_result = {"results": {"workout": {"recorded": True, "plan": {PROGRAM_KEY: _training_program()}}}}
    nonconformant = _training_program()
    del nonconformant[domain_program.MONITORING_SIGNALS]  # a required field -> non-conformant
    version = care_chat.synthesize(
        {"workout", "sleep"}, run_result, lambda d: _rich_author_env(nonconformant),
        read, on_date="2026-07-13", root=root)
    assert version is not None, "the conformant renderable program should still compose a version"
    programs = version[plan_model.DOMAIN_PROGRAMS]
    assert "sleep" not in programs, "the non-conformant rich program was folded (validate/drop absent)"
    assert "workout" in programs
    assert plan_model.read_plan_version("2026-07-13", root)["state"] is None, "no version recorded"


def test_synthesize_strips_load_from_rich_program(tmp_path):
    # HCR-01: a rich author whose prescription carries per-block + top-level `load` is folded with load
    # DEEP-STRIPPED — no un-cleared load reaches the stored comprehensive state (ADR-0015/BUG-01).
    # Clearance is not plumbed to the rich path, so the strip is UNCONDITIONAL. REDs if the strip is removed.
    root = tmp_path / "store"
    read = _seed_surface_store(root, goal_domains=["workout"])
    loaded = {"name": "sleep-protocol", "load": "top-level",
              "blocks": [{"date": "2026-07-13", "load": "60% 1RM", "detail": "x"}]}
    run_result = {"results": {"workout": {"recorded": True, "plan": {PROGRAM_KEY: _training_program()}}}}
    version = care_chat.synthesize(
        {"workout", "sleep"}, run_result,
        lambda d: _rich_author_env(_training_program(prescription=loaded)),
        read, on_date="2026-07-13", root=root)
    assert "sleep" in version[plan_model.DOMAIN_PROGRAMS], "the rich program was not folded"
    sleep_presc = version[plan_model.DOMAIN_PROGRAMS]["sleep"][domain_program.PRESCRIPTION]
    assert not _contains_load(sleep_presc), f"un-cleared load reached stored comprehensive state: {sleep_presc}"


def test_regen_isolates_raising_rich_author_and_holds(tmp_path):
    # W4-01 (PF-S130-01 production path): a materially-large regen (>= LARGE_CHANGE_THRESHOLD_DOMAINS
    # renderable swaps) + a rich domain (sleep) whose Leg-2 author RAISES. The rich-author dispatch is
    # isolated (try/except -> None), so regenerate does NOT raise; and because the ADR-0040 hold runs
    # BEFORE Leg 2, mark_pending fired for every promoted domain (the thin swap is held, no unconfirmed
    # standing swap). REDs if the rich-author isolation is reverted (the raise then propagates out).
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=[*plan_schema.RENDERABLE_DOMAINS, "sleep"])
    _seed_prior_standing(root, plan_schema.RENDERABLE_DOMAINS)  # 4 differing priors -> large change

    class _RaisingRichDispatch(_LoopDispatch):
        def __call__(self, name, prompt, context):
            if name == "sleep":
                raise RuntimeError("transient rich dispatch failure")
            return super().__call__(name, prompt, context)

    result = plan_loop.regenerate(  # must NOT raise
        root, dispatch=_RaisingRichDispatch(_clean_authors()),
        deid_client=_FixedDeidClient(_deid_summary()), plan_date="2026-07-13", trigger="test")
    promoted = [d for d, r in result["results"].items() if r.get("recorded")]
    assert set(promoted) == set(plan_schema.RENDERABLE_DOMAINS), promoted
    for domain in promoted:
        assert plan_confirm.decision_for(domain, "2026-07-13", root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: the ADR-0040 hold did not fire (a Leg-2 raise skipped it)"
        )


def test_regen_hold_fires_before_leg2(tmp_path, monkeypatch):
    # W4-01 (hold reorder): the ADR-0040 hold runs BEFORE Leg 2, so even a Leg-2 (synthesize) raise
    # cannot skip it. Force synthesize to raise; regenerate propagates it, but mark_pending ALREADY
    # fired for every promoted domain (no unconfirmed standing swap / partial write). REDs if the hold
    # is moved back AFTER Leg 2 (the raise then skips mark_pending).
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=list(plan_schema.RENDERABLE_DOMAINS))
    _seed_prior_standing(root, plan_schema.RENDERABLE_DOMAINS)

    def _boom(*a, **k):
        raise RuntimeError("Leg-2 synthesize failure")

    monkeypatch.setattr(care_chat, "synthesize", _boom)
    with pytest.raises(RuntimeError):
        plan_loop.regenerate(
            root, dispatch=_LoopDispatch(_clean_authors()),
            deid_client=_FixedDeidClient(_deid_summary()), plan_date="2026-07-13", trigger="test")
    for domain in plan_schema.RENDERABLE_DOMAINS:
        assert plan_confirm.decision_for(domain, "2026-07-13", root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: the hold did not fire before Leg 2 (a Leg-2 raise skipped mark_pending)"
        )


def test_collect_raises_on_duplicate_domain(tmp_path):
    # 61cy: care_chat.collect FAILS LOUD on a duplicate domain (no silent last-wins dedupe).
    root = tmp_path / "store"
    _seed_surface_store(root, goal_domains=["workout"])
    read = functools.partial(store.read, root=root)
    collected = [
        {"domain": "supplements", "plan": None, "meta": {}, "reason": None},
        {"domain": "supplements", "plan": None, "meta": {}, "reason": None},
    ]
    with pytest.raises(ValueError):
        care_chat.collect(collected, read)


def test_validatorless_domain_raises_valueerror_not_keyerror(tmp_path):
    # _check_plan_args guard (signed off): a grown PLAN_DOMAINS member lacking a thin validator raises
    # ValueError, not a raw KeyError, at the record boundary.
    root = tmp_path / "store"
    root.mkdir(parents=True, exist_ok=True)
    assert "sleep" in plan_schema.PLAN_DOMAINS and "sleep" not in plan_schema._PLAN_VALIDATORS
    with pytest.raises(ValueError):
        plan_schema.record_plan("sleep", {"any": "plan"}, "2026-07-13", "sleep-coach", root)


def test_record_repoint_store_adversarial(tmp_path):
    # Store-adversarial battery over the record_plan_version re-point surface (bead pka):
    # (a) cross-stream isolation; (b) same-timepoint distinct versions both persist + idempotence;
    # (c) dedupe-key boundary (no new keying); (d) category-(d) mutation-RED is Step-2.5 #12.
    root = tmp_path / "store"
    root.mkdir(parents=True, exist_ok=True)
    v1 = {
        plan_model.VERSION_DATE: "2026-07-13",
        plan_model.DOMAIN_PROGRAMS: {"workout": _training_program()},
        plan_model.NARRATIVE: "v1", plan_model.MILESTONES: [{"date": "2026-08-01"}],
        plan_model.MONITORING_CONFIG: {"cadence_days": 30},
    }
    v2 = {**v1, plan_model.NARRATIVE: "v2-distinct",
          plan_model.DOMAIN_PROGRAMS: {"nutrition": _training_program()}}
    plan_model.record_plan_version(v1, root)
    plan_model.record_plan_version(v2, root)
    plan_model.record_plan_version(v1, root)  # idempotent re-record
    model_rows = store.read(plan_model._PREFIX_MODEL, root=root)
    assert len(model_rows) == 2, "two distinct versions must persist; an identical re-record is a no-op"
    # (a) cross-stream: the plan-model:: stream never returns a thin plan:: row.
    assert all(r["item"] == plan_model._PREFIX_MODEL for r in model_rows)
    # (c) dedupe-key boundary: the re-point introduces NO new keying literal in plan_model.
    src = (REPO_ROOT / "scripts/store/plan_model.py").read_text(encoding="utf-8")
    assert "keying." not in src, "the re-point must not reach into keying (identity stays frozen)"


# =========================================================================== #
# GROUP B — seam-channel (ncsy / pule)
# =========================================================================== #


def _seam_program(paired, *, nature=None):
    """A conformant training program declaring ONE cross_domain_seams edge (pinned key-names)."""
    return _training_program(cross_domain_seams=[{
        domain_program.SEAM_WITH_DOMAIN: paired,
        domain_program.SEAM_NATURE: nature if nature is not None else domain_program.SEAM_CONFLICT,
    }])


def _seam_candidate(domain, paired, *, nature=None):
    return {
        "domain": domain, "specialist": f"{domain}-specialist",
        "plan": {"items": [{"name": "x", "dose": "1"}], PROGRAM_KEY: _seam_program(paired, nature=nature)},
        "meta": {}, "reason": None, "section": None,
    }


def test_seam_sourced_conflict_yields_faithful_finding(tmp_path):
    # ncsy (PF-S130-01): a SEAM_CONFLICT-nature seam on a pair NOT declared via meta.conflicts yields
    # a FAITHFUL _conflict_safety_finding (with_domain + nature preserved; non-empty finding_id /
    # caution), NOT the degenerate `conflict:<d>:` empty finding.
    outcome = orchestrate.reconcile({"supplements": _seam_candidate("supplements", "peptides")})
    assert "supplements" in outcome["conflict_held"]
    conflicts = [c for c in outcome["report"]["conflicts"] if c.get("from") == "supplements"]
    finding = orchestrate._conflict_safety_finding("supplements", conflicts)
    assert finding["finding_id"] != "conflict:supplements:", "degenerate empty finding (ncsy unfixed)"
    assert finding["caution"], "empty caution (ncsy unfixed)"
    assert "peptides" in finding["finding_id"], "the paired with_domain was not preserved"


def test_seam_and_meta_conflict_single_finding_no_double_count(tmp_path):
    # ncsy: a domain held by BOTH a seam-conflict AND a meta.conflicts author conflict produces
    # exactly ONE faithful finding (no double-count).
    cand = _seam_candidate("supplements", "peptides")
    cand["meta"] = {"conflicts": [{"with_domain": "workout", "with": "creatine", "reason": "x"}]}
    outcome = orchestrate.reconcile({"supplements": cand})
    held = list(outcome["conflict_held"])
    assert held.count("supplements") == 1, held
    conflicts = [c for c in outcome["report"]["conflicts"] if c.get("from") == "supplements"]
    finding = orchestrate._conflict_safety_finding("supplements", conflicts)
    assert finding["finding_id"] and finding["caution"]


def test_seam_keys_pinned_in_domain_program():
    # pule: the {with_domain, nature} seam-edge key-names are single-sourced in domain_program and
    # REFERENCED by orchestrate.SEAM_*.
    assert domain_program.SEAM_WITH_DOMAIN == "with_domain"
    assert domain_program.SEAM_NATURE == "nature"
    assert orchestrate.SEAM_WITH_DOMAIN is domain_program.SEAM_WITH_DOMAIN
    assert orchestrate.SEAM_NATURE is domain_program.SEAM_NATURE
    assert orchestrate.SEAM_CONFLICT is domain_program.SEAM_CONFLICT


def test_authored_seam_reconciles_no_silent_drop():
    # pule: a seam authored per the pinned key-names RECONCILES (0 silent drop).
    outcome = orchestrate.reconcile({"supplements": _seam_candidate("supplements", "peptides")})
    assert outcome["report"]["seams"], "a well-formed authored seam was silently dropped"
    assert outcome["report"]["seams"][0][domain_program.SEAM_WITH_DOMAIN] == "peptides"


def test_malformed_seam_inert_documented():
    # pule: a genuinely malformed seam (no paired-domain reference) is documented-inert.
    cand = {
        "domain": "supplements", "specialist": "s",
        "plan": {"items": [{"name": "x", "dose": "1"}],
                 PROGRAM_KEY: _training_program(cross_domain_seams=[{"garbage": True}])},
        "meta": {}, "reason": None, "section": None,
    }
    outcome = orchestrate.reconcile({"supplements": cand})
    assert outcome["report"]["seams"] == [], "a malformed seam must be inert"


def _seam_ae_program(paired, *, additive_classes):
    """A conformant training program whose ONE cross_domain_seams edge carries an Option-B ae_profile."""
    return _training_program(cross_domain_seams=[{
        domain_program.SEAM_WITH_DOMAIN: paired,
        domain_program.SEAM_AE_PROFILE: {"additive_classes": additive_classes},
    }])


def test_seam_ae_held_rich_domain_dropped_from_comprehensive(tmp_path):
    # kn29 / SEC-W4-01 P7 (end-to-end fail-closed DROP): two rich domains sharing a bleeding-risk class
    # on their cross_domain_seams ae_profile are BOTH held by the Option-B rich additive-AE screen ->
    # DROPPED from the composed comprehensive version (the honest no-plan-for-that-domain state, never
    # folded un-screened). The programs are CONFORMANT (so the drop is due to the HOLD, not validate) —
    # RED if the SEAM_ADDITIVE_AE_HELD population is removed (they fold back into the composed version).
    root = tmp_path / "store"
    read = _seed_surface_store(root, goal_domains=["workout"])
    run_result = {"results": {"workout": {"recorded": True, "plan": {PROGRAM_KEY: _training_program()}}}}

    def _author_rich(domain):
        other = "stress" if domain == "sleep" else "sleep"
        return _rich_author_env(_seam_ae_program(other, additive_classes=["bleeding-risk"]))

    version = care_chat.synthesize(
        {"workout", "sleep", "stress"}, run_result, _author_rich,
        read, on_date="2026-07-13", root=root)
    programs = version[plan_model.DOMAIN_PROGRAMS]
    assert "sleep" not in programs and "stress" not in programs, programs.keys()
    assert "workout" in programs  # the un-held renderable program still composes the version


def test_seam_rx_bpmh_held_rich_domain_dropped_from_comprehensive(tmp_path):
    # kn29 / SEC-W4-01 SF-1 (path-c Rx-BPMH end-to-end DROP): a rich domain held SOLELY via the seam
    # Rx-BPMH re-base — its pooled seam ae_profile class intersects the operator's present
    # `rx-interaction-classes` — lands in the DISTINCT `rx_bpmh_held` set and is DROPPED from the
    # composed comprehensive version. The fail-closed postcondition THROUGH `rx_bpmh_held`, previously
    # unasserted e2e. Non-tautological: sleep is the only rich domain (no shared-class pair, no
    # interaction), so the drop is caused ONLY by path (c). RED if screen 5's seam class source is
    # reverted to meta-only (sleep then folds back into the composed version).
    root = tmp_path / "store"
    read = _seed_surface_store(root, goal_domains=["workout"],
                               extra={"rx-interaction-classes": "bleeding-risk"})
    run_result = {"results": {"workout": {"recorded": True, "plan": {PROGRAM_KEY: _training_program()}}}}
    version = care_chat.synthesize(
        {"workout", "sleep"}, run_result,
        lambda d: _rich_author_env(_seam_ae_program("workout", additive_classes=["bleeding-risk"])),
        read, on_date="2026-07-13", root=root)
    programs = version[plan_model.DOMAIN_PROGRAMS]
    assert "sleep" not in programs, programs.keys()  # held via seam Rx-BPMH -> dropped fail-closed
    assert "workout" in programs  # the un-held renderable program still composes the version


# =========================================================================== #
# GROUP C — contract pins (ubsp / qrg4)
# =========================================================================== #


def test_prescription_contract_pins_top_level_identity():
    # ubsp (LOAD-BEARING): domain_program's prescription contract STATES renderable-identity is a
    # TOP-LEVEL prescription field. The specific pinned phrase (whitespace-normalized so a wrapped
    # docstring still matches) — removing it (mutation #11) REDs this.
    src = (REPO_ROOT / "scripts/plan/domain_program.py").read_text(encoding="utf-8")
    normalized = " ".join(src.split()).lower()
    assert "top-level prescription field" in normalized, "the ubsp top-level-identity pin is absent"
    assert "renderable" in normalized and "identity" in normalized


def test_top_level_identity_prescription_projects():
    # ubsp characterization (pre-existing _project_renderable boundary): a top-level-identity
    # periodized prescription projects to the flat renderable form.
    presc = {"name": "Goblet squat", "sets": 3, "blocks": [{"date": "2026-07-13", "load": "60%"}]}
    projected = domain_program.project_renderable(presc, "workout", strip_load=True)
    assert projected is not None and projected["name"] == "Goblet squat"
    assert not _contains_load(projected)


def test_identity_in_blocks_is_documented_no_plan():
    # ubsp characterization: a degenerate periodized-only prescription (identity only inside blocks,
    # no top-level identity) projects to honest no-plan (None).
    presc = {"blocks": [{"date": "2026-07-13", "name": "Goblet squat", "load": "60%"}]}
    assert domain_program.project_renderable(presc, "workout", strip_load=True) is None


def _seed_unheld_comprehensive(root, domain_programs, *, date):
    """Record an UN-HELD comprehensive version (no pending confirm pointer — qrg4 fixture caveat)."""
    version = {
        plan_model.VERSION_DATE: date, plan_model.DOMAIN_PROGRAMS: domain_programs,
        plan_model.NARRATIVE: "standing", plan_model.MILESTONES: [{"date": date}],
        plan_model.MONITORING_CONFIG: {"cadence_days": 30},
    }
    plan_model.record_plan_version(version, root)


def test_read_standing_plan_returns_comprehensive_prescription(tmp_path):
    # qrg4 (SE-discretion: docstring+consumer reconciliation, NOT a reader-output projection — the
    # landed ADR-0044-T3 horizons rebase + the reader tests consume the periodized PRESCRIPTION, so
    # projecting the reader output would break them). read_standing_plan on a standing comprehensive
    # domain returns the DOMAIN PROGRAM's periodized PRESCRIPTION (the shape its consumers were built
    # for — track.resolve_plan_progress -> horizons/adjust/maintained/dashboard), under read_plan's
    # top-level {state, plan, specialist, plan_date} keys.
    root = tmp_path / "store"
    root.mkdir(parents=True, exist_ok=True)
    presc = {"name": "Goblet squat", "sets": 3, "blocks": [{"date": "2026-07-13", "load": "60%"}]}
    _seed_unheld_comprehensive(root, {"workout": _training_program(prescription=presc)},
                               date="2026-07-13")
    resolved = plan_model.read_standing_plan("workout", "2026-07-13", root)
    assert resolved["state"] is None
    assert set(resolved) == {"state", "plan", "specialist", "plan_date"}, resolved
    assert resolved["plan"] == presc, resolved["plan"]
    assert resolved["specialist"] is None  # comprehensive branch is orchestrator-synthesized


def test_read_standing_plan_docstring_reconciled():
    # qrg4 LOAD-BEARING deliverable: the read_standing_plan docstring no longer FALSELY claims the
    # comprehensive branch is a "pure call-site swap" returning read_plan's renderable shape — it is
    # reconciled to state the comprehensive branch returns the periodized prescription.
    src = (REPO_ROOT / "scripts/store/plan_model.py").read_text(encoding="utf-8")
    normalized = " ".join(src.split())  # collapse wraps so a line-wrapped phrase still matches
    assert "pure call-site swap" in normalized and "corrected here" in normalized, (
        "the read_standing_plan docstring still carries the un-reconciled pure-swap claim"
    )
    assert "periodized" in normalized and "PRESCRIPTION" in normalized


def test_stale_comprehensive_thin_wins_sf2(tmp_path):
    # qrg4 SF-2: a comprehensive version dated < on_date + a thin plan dated on_date -> the thin plan
    # resolves (comprehensive-wins only when it STANDS for on_date).
    root = tmp_path / "store"
    root.mkdir(parents=True, exist_ok=True)
    _seed_unheld_comprehensive(root, {"workout": _training_program()}, date="2026-07-06")
    plan_schema.record_plan("workout", {"exercises": [{"name": "Bench", "sets": 3}]},
                            "2026-07-13", "personal-trainer", root)
    resolved = plan_model.read_standing_plan("workout", "2026-07-13", root)
    assert resolved["plan"] == {"exercises": [{"name": "Bench", "sets": 3}]}


def test_two_domain_comprehensive_returns_domain_b_prescription_low2(tmp_path):
    # qrg4 LOW-2: a >=2-domain comprehensive version -> domain B returns B's prescription, not A's.
    root = tmp_path / "store"
    root.mkdir(parents=True, exist_ok=True)
    a = _training_program(prescription={"name": "Squat", "sets": 3})
    b = _compound_program(prescription={"compound": "BPC-157", "dose": "250mcg"})
    _seed_unheld_comprehensive(root, {"workout": a, "peptides": b}, date="2026-07-13")
    resolved = plan_model.read_standing_plan("peptides", "2026-07-13", root)
    assert resolved["state"] is None
    assert resolved["plan"].get("compound") == "BPC-157", resolved["plan"]


# --------------------------------------------------------------------------- #
# small load helpers (mirror generate_plan._contains_load without importing privates broadly)
# --------------------------------------------------------------------------- #


def _contains_load(value):
    if isinstance(value, dict):
        return "load" in value or any(_contains_load(v) for v in value.values())
    if isinstance(value, list):
        return any(_contains_load(v) for v in value)
    return False


def _has_movement(value):
    """Whether a projected workout prescription still carries movement identity (name)."""
    if isinstance(value, dict):
        return "name" in value or any(_has_movement(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_movement(v) for v in value)
    return False
