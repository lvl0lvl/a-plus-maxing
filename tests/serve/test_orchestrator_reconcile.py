"""Tests for the generalized `orchestrate.reconcile` uniform `cross_domain_seams` pass +
the always-on safety floors + the `care_chat` collect+reconcile control flow (ADR-0043-T2).

This module pins the Wave-3 reconcile generalization: the five hard-coded pair-specific
cross-domain holds are generalized into ONE uniform pass over each candidate's DOMAIN
PROGRAM `cross_domain_seams` (no per-domain-pair branch), while the SAFETY-CRITICAL subset
(RED-S/LEA short-circuit, supplement<->peptide additive-AE, supplement<->Rx BPMH) is re-based
as ALWAYS-ON FLOORS that fire from their own trigger conditions REGARDLESS of whether a
program declares the seam — UNDECLARED (AC-3) or DECLARED (AC-3b/SEC-W3-02) — and also fire
through the new `care_chat` collect+reconcile path (SEC-W3-03). Every fixture DOMAIN PROGRAM
is canonical (PF-S131-01): periodized `prescription`, tiered `monitoring_signals`, a compound
kind's non-empty `required_labs`, and the real `cross_domain_seams` edge shape — each passing
`domain_program.validate`. All fixtures are SYNTHETIC (0 live-API, 0 real operator PII).

The generalization is a SWAP (five holds -> one uniform pass), so the load-bearing tests are
NON-TAUTOLOGICAL: the always-on-floor tests RED under a floor-removal OR a floor-gating
mutation, the care_chat floor tests RED under a collect-strip mutation, and the production-path
`test_uniform_seam_pass_catches_non_hardcoded_pair` REDs on a revert to the pre-generalization
five-holds reconcile (a `workout`<->`supplements` seam is in no hard-coded branch) — PF-S130-01.
"""

import functools
import inspect
import re
import subprocess
from pathlib import Path

import pytest

from scripts.plan import domain_program, orchestrate, router
from scripts.plan.assemble import PROGRAM_KEY
from scripts.plan.domain_program import CROSS_DOMAIN_SEAMS
from scripts.plan.generate_plan import RED_S_LEA_CLINICAL_ROUTING
from scripts.plan.orchestrate import (
    ADDITIVE_AE_HELD,
    RED_S_LEA_CROSS_DOMAIN,
    reconcile,
)
from scripts.serve import care_chat
from scripts.store import store
from tests.plan.test_generate_plan import _seed_store

# The AC-5 per-ADR numstat probe base (mirrors tests/plan/test_generate_plan_uniform.py:55's
# PRE_TASK_HEAD constant pattern). wdhc: the ADR-0043-T2 entry HEAD 9982b952 is an intermediate wave
# commit (orphan-prone — the repo squash-merges); repointed to the merge-base 3e17b1d8 (==
# origin/main), a durable reachable base. Only 0043-T2 edits orchestrate.py in the wave, so its
# numstat vs the merge-base equals vs the entry HEAD; the frozen paths are byte-untouched vs both.
PRE_TASK_HEAD = "3e17b1d8291d86d48441e36177a71f34910fbe57"

# The domain KIND each fixture domain declares (compound-band domains are compound-kind so their
# required_labs is mandatory-and-non-empty, per domain_program.DOMAIN_KIND_RULES).
_DOMAIN_KIND = {
    "workout": "training",
    "nutrition": "training",
    "supplements": "compound",
    "peptides": "compound",
}


# --- canonical DOMAIN PROGRAM + candidate fixtures (PF-S131-01) -----------------


def _program(domain, *, seams=None):
    """A CANONICAL, `validate`-conformant DOMAIN PROGRAM for `domain` (PF-S131-01).

    Periodized `prescription` (`{"blocks": [{date, load}]}`), each `monitoring_signals` entry
    carrying a `VALIDITY_TIERS` tier, a compound kind's `required_labs` non-empty, and the real
    `cross_domain_seams` edge shape (a list of paired-domain-ref + nature-token entries).
    """
    kind = _DOMAIN_KIND[domain]
    program = {
        domain_program.PRESCRIPTION: {
            "blocks": [{"date": "2026-07-12", "load": {"domain": domain, "unit": 1}}]
        },
        domain_program.RATIONALE: {
            "claims": [{
                "certainty_of_evidence": "moderate",
                "strength_of_recommendation": "strong",
                "causal": True,
            }]
        },
        domain_program.MONITORING_SIGNALS: [
            {"signal": "readiness", domain_program.SIGNAL_TIER_KEY: "moderate"}
        ],
        domain_program.ADJUSTMENT_RULES: [{"if": "signal-low", "then": "deload"}],
        domain_program.REQUIRED_LABS: (
            ["ferritin"]
            if domain_program.DOMAIN_KIND_RULES[kind]["required_labs_nonempty"] else []
        ),
        domain_program.REFUSAL_ESCALATION: {},
        domain_program.CROSS_DOMAIN_SEAMS: list(seams or []),
        domain_program.KIND_FIELD: kind,
    }
    return program


def _seam(with_domain, nature):
    """One `cross_domain_seams` edge: a paired-domain reference + a seam-nature/conflict token."""
    return {orchestrate.SEAM_WITH_DOMAIN: with_domain, orchestrate.SEAM_NATURE: nature}


def _candidate(domain, *, seams=None, meta=None, reason=None, has_plan=True, plan=None):
    """A `reconcile`/collect candidate carrying a canonical DOMAIN PROGRAM under PROGRAM_KEY.

    Mirrors the `compute_plan` candidate shape (`{domain, specialist, plan, section, reason,
    meta}`); the seven-field program rides under `plan[PROGRAM_KEY]` (the 0041-T2 additive ride),
    so `reconcile` reads `cross_domain_seams` off the UNIFORM field. `meta` carries the always-on
    floor triggers (`ae_profile` / `energy_budget` / `conflicts`); `reason` carries the RED-S/LEA
    clinical-routing reason. A held candidate (`has_plan=False`) rides no plan.
    """
    if plan is None and has_plan:
        plan = {"content": domain, PROGRAM_KEY: _program(domain, seams=seams)}
    elif plan is not None:
        plan = {**plan, PROGRAM_KEY: _program(domain, seams=seams)}
    return {
        "domain": domain,
        "specialist": f"{domain}-specialist",
        "plan": plan,
        "section": {},
        "reason": reason,
        "meta": meta or {},
    }


def _assert_program_fixtures_conform():
    """Every canonical fixture program passes `domain_program.validate` (PF-S131-01 gate)."""
    for domain in _DOMAIN_KIND:
        domain_program.validate(_program(domain, seams=[_seam("supplements", "conflict")]))


# --- PF-S131-01: fixture conformance --------------------------------------------


def test_all_fixture_programs_pass_validate():
    """PF-S131-01: every fixture DOMAIN PROGRAM is canonical (passes `validate`), not a stand-in."""
    _assert_program_fixtures_conform()


# --- AC-1: reconcile through ONE code path (0 new per-pair branches) -------------


def test_reconcile_reads_cross_domain_seams_through_one_path():
    """AC-1: a declared seam on ANY pair is detected via the UNIFORM `cross_domain_seams` field,
    through ONE pass (0 new per-domain-pair hard-coded branches)."""
    # An arbitrary pair (nutrition<->peptides) — NOT one of the five hard-coded safety pairs — so a
    # generic uniform pass is the only thing that can reconcile it.
    candidates = {
        "nutrition": _candidate("nutrition", seams=[_seam("peptides", "advisory")]),
        "peptides": _candidate("peptides"),
    }
    out = reconcile(candidates)
    seams = out["report"]["seams"]
    assert any(s["from"] == "nutrition" and s["with_domain"] == "peptides" for s in seams), \
        "the uniform pass must detect the declared seam off the cross_domain_seams field"

    # Structural: the generalization adds NO per-domain-pair branch — reconcile's source carries no
    # domain-name string-literal equality (`== "workout"` etc.); the seam pass iterates generically.
    source = inspect.getsource(reconcile)
    assert re.search(r'==\s*"(workout|nutrition|supplements|peptides)"', source) is None, \
        "a per-domain-pair seam branch (domain-literal ==) would defeat AC-1's one-path property"
    assert "_cross_domain_seams(" in source, "the seam pass must read the uniform field via one accessor"


# --- AC-2: 0 declared-seam conflicts reach the output un-reconciled --------------


def test_declared_seam_conflict_never_unreconciled():
    """AC-2: every declared `cross_domain_seams` CONFLICT seam is detected + held/routed — 0
    declared conflicts reach the output un-reconciled. The drop-seam mutation REDs this."""
    candidates = {
        "workout": _candidate("workout", seams=[_seam("supplements", "conflict")]),
        "supplements": _candidate("supplements", seams=[_seam("workout", "conflict")]),
    }
    out = reconcile(candidates)
    declared = [("workout", "supplements"), ("supplements", "workout")]
    reconciled = {(s["from"], s["with_domain"]) for s in out["report"]["seams"]}
    assert set(declared) <= reconciled, "every declared conflict seam must be reconciled (0 un-reconciled)"
    # A conflict-nature seam HOLDS the declaring domain (the independent conflict_held set).
    assert "workout" in out["conflict_held"] and "supplements" in out["conflict_held"]


# --- AC-3: always-on safety floors fire when the seam is UNDECLARED (SAFETY) -----


def test_red_s_lea_floor_fires_undeclared():
    """AC-3 (SAFETY): a tripped nutrition RED-S/LEA reason + an energy-prescribing workout, with
    EMPTY cross_domain_seams, holds the workout — the floor fires regardless of declaration."""
    candidates = {
        "nutrition": _candidate("nutrition", reason=RED_S_LEA_CLINICAL_ROUTING),
        "workout": _candidate("workout"),
    }
    out = reconcile(candidates)
    assert out["holds"].get("workout") == RED_S_LEA_CROSS_DOMAIN


def test_additive_ae_floor_fires_undeclared():
    """AC-3 (SAFETY): a supplement + peptide sharing an additive-AE class via meta.ae_profile, with
    EMPTY seams, holds the supplement."""
    shared = {"ae_profile": {"additive_classes": ["bleeding-risk"]}}
    candidates = {
        "supplements": _candidate("supplements", meta=dict(shared)),
        "peptides": _candidate("peptides", meta=dict(shared)),
    }
    out = reconcile(candidates)
    assert out["holds"].get("supplements") == ADDITIVE_AE_HELD


def test_rx_bpmh_floor_fires_undeclared():
    """AC-3 (SAFETY): a compound whose additive-AE class intersects an operator Rx-interaction
    class, with EMPTY seams, lands in rx_bpmh_held."""
    candidates = {
        "supplements": _candidate(
            "supplements", meta={"ae_profile": {"additive_classes": ["bleeding-risk"]}}
        ),
    }
    out = reconcile(candidates, operator_rx_classes={"bleeding-risk"})
    assert "supplements" in out["rx_bpmh_held"]


# --- AC-3b: always-on floors fire even when the seam IS DECLARED (SEC-W3-02) -----


def test_red_s_lea_floor_fires_even_when_seam_declared():
    """AC-3b (SEC-W3-02): the RED-S/LEA floor fires even when a nutrition<->workout seam is declared
    (the floor is NOT gated behind declaration). The floor-GATING mutation REDs this."""
    candidates = {
        "nutrition": _candidate(
            "nutrition", reason=RED_S_LEA_CLINICAL_ROUTING, seams=[_seam("workout", "advisory")]
        ),
        "workout": _candidate("workout", seams=[_seam("nutrition", "advisory")]),
    }
    out = reconcile(candidates)
    assert out["holds"].get("workout") == RED_S_LEA_CROSS_DOMAIN


def test_additive_ae_floor_fires_even_when_seam_declared():
    """AC-3b (SEC-W3-02): the additive-AE floor fires even when a supplements<->peptides seam is
    declared. The floor-GATING mutation REDs this."""
    shared = {"ae_profile": {"additive_classes": ["bleeding-risk"]}}
    candidates = {
        "supplements": _candidate(
            "supplements", meta=dict(shared), seams=[_seam("peptides", "advisory")]
        ),
        "peptides": _candidate(
            "peptides", meta=dict(shared), seams=[_seam("supplements", "advisory")]
        ),
    }
    out = reconcile(candidates)
    assert out["holds"].get("supplements") == ADDITIVE_AE_HELD


def test_rx_bpmh_floor_fires_even_when_seam_declared():
    """AC-3b (SEC-W3-02): the Rx-BPMH floor fires even when a seam is declared on the compound's
    pair. The floor-GATING mutation REDs this."""
    candidates = {
        "supplements": _candidate(
            "supplements",
            meta={"ae_profile": {"additive_classes": ["bleeding-risk"]}},
            seams=[_seam("peptides", "advisory")],
        ),
    }
    out = reconcile(candidates, operator_rx_classes={"bleeding-risk"})
    assert "supplements" in out["rx_bpmh_held"]


# --- AC-4: the five prior behaviors' safety content is re-based, not deleted -----


def test_five_prior_behaviors_still_reconcile():
    """AC-4: each of the five prior behaviors still reconciles its case post-generalization."""
    # 1. RED-S/LEA short-circuit.
    out = reconcile({
        "nutrition": _candidate("nutrition", reason=RED_S_LEA_CLINICAL_ROUTING),
        "workout": _candidate("workout"),
    })
    assert out["holds"].get("workout") == RED_S_LEA_CROSS_DOMAIN
    assert out["report"]["red_s_lea_cross_domain"] is True

    # 2. Energy bounce (transitional meta.energy_budget read preserved).
    out = reconcile({
        "nutrition": _candidate(
            "nutrition",
            meta={"energy_budget": {"sustains": False, "sustainable_training_kcal": 450}},
        ),
        "workout": _candidate("workout", meta={"energy_cost_kcal": 900}),
    })
    assert out["report"]["bounce"] is not None
    assert out["report"]["bounce"]["target"] == "workout"

    # 3. Overlap + author-declared conflict (transitional meta.conflicts read preserved).
    out = reconcile({
        "supplements": _candidate(
            "supplements",
            meta={"conflicts": [{"with_domain": "peptides", "with": "bpc-157", "reason": "x"}]},
        ),
        "peptides": _candidate("peptides"),
    })
    assert "supplements" in out["conflict_held"]
    assert any(c["from"] == "supplements" for c in out["report"]["conflicts"])

    # 4. Additive-AE screen.
    shared = {"ae_profile": {"additive_classes": ["bleeding-risk"]}}
    out = reconcile({
        "supplements": _candidate("supplements", meta=dict(shared)),
        "peptides": _candidate("peptides", meta=dict(shared)),
    })
    assert out["holds"].get("supplements") == ADDITIVE_AE_HELD

    # 5. Supplement<->Rx BPMH screen.
    out = reconcile(
        {"supplements": _candidate(
            "supplements", meta={"ae_profile": {"additive_classes": ["bleeding-risk"]}}
        )},
        operator_rx_classes={"bleeding-risk"},
    )
    assert "supplements" in out["rx_bpmh_held"]


# --- AC-5: per-ADR-scoped freeze-break numstat ----------------------------------


def _numstat(base, *paths):
    """`git diff --numstat <base> -- <paths>` over the repo, stripped (mirror the uniform probe)."""
    repo = Path(__file__).resolve().parents[2]
    out = subprocess.run(
        ["git", "diff", "--numstat", base, "--", *paths],
        cwd=repo, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def test_per_adr_scoped_freeze_break_numstat():
    """AC-5: orchestrate.py NON-empty (the sanctioned generalization); the frozen four + assemble.py
    EMPTY vs PRE_TASK_HEAD; the <always-frozen> HARD six EMPTY vs origin/main. generate_plan.py +
    plan_schema.py are DROPPED from the forbidden list (Deviation #1 — a Wave-3 sibling edits them)."""
    # (a) the sanctioned generalization.
    assert _numstat(PRE_TASK_HEAD, "scripts/plan/orchestrate.py") != "", \
        "orchestrate.py must carry the sanctioned cross_domain_seams generalization"
    # (b) the frozen four + assemble.py — no Wave-3 editor — untouched by THIS task.
    assert _numstat(
        PRE_TASK_HEAD,
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/store/store.py", "scripts/store/keying.py", "scripts/plan/assemble.py",
    ) == "", "the frozen four + assemble.py must be numstat=0 vs PRE_TASK_HEAD"
    # (c) the <always-frozen> HARD six — invariant 1, over the whole build (origin/main base).
    assert _numstat(
        "origin/main",
        "scripts/store/store.py", "scripts/store/keying.py", "scripts/plan/pipeline.py",
        "scripts/plan/adjudicate.py", "scripts/plan/adjust.py", "scripts/plan/router.py",
    ) == "", "the <always-frozen> HARD six must be numstat=0 over the whole build"


# --- AC-6: module hygiene (0 live-API, 0 real PII) ------------------------------


def test_module_imports_no_live_client_or_operator_pii():
    """AC-6: this module imports no live model client + carries no real operator-identity literal.

    Both checks read the module's AST (imports + string constants) rather than raw text, so the
    check literals themselves cannot false-match (0 live-client import; 0 email-address literal —
    the operator-identity class — without this file itself embedding any operator PII).
    """
    import ast

    tree = ast.parse(Path(__file__).read_text())
    imported = set()
    literals = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.append(node.value)
    assert not any("model" in module for module in imported), \
        "the reconcile suite must not import the live model client (0 live-API)"
    # 0 email-address literal (the operator-identity class). The pattern is assembled from fragments
    # none of which self-match, so no operator PII is embedded and no check literal false-positives.
    email_re = re.compile(r"[A-Za-z0-9._%+-]+" + "@" + r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    assert not any(email_re.search(text) for text in literals), \
        "no operator email literal in the reconcile suite (synthetic fixtures only)"


# --- PF-S130-01: production-path non-hardcoded-pair seam (non-tautological) ------


def test_uniform_seam_pass_catches_non_hardcoded_pair(tmp_path):
    """PF-S130-01 (MANDATORY): drive the production reconcile path — orchestrate.reconcile AND the
    care_chat collect+reconcile — with a `workout`<->`supplements` CONFLICT seam (a pair in NONE of
    the five hard-coded branches). The seam is detected + held (0 un-reconciled). REDs on a revert
    to the pre-generalization five-holds reconcile (that pair is in no hard-coded branch)."""
    collected = [
        _candidate("workout", seams=[_seam("supplements", "conflict")]),
        _candidate("supplements", seams=[_seam("workout", "conflict")]),
    ]
    # Direct production reconcile path.
    direct = reconcile({c["domain"]: c for c in collected})
    assert any(
        s["from"] == "workout" and s["with_domain"] == "supplements" for s in direct["report"]["seams"]
    ), "the workout<->supplements seam must be caught by the uniform pass"
    assert "workout" in direct["conflict_held"], "a non-hardcoded-pair conflict seam must HOLD the declarer"

    # The care_chat collect+reconcile path routes THROUGH the same one orchestrate.reconcile.
    store_read = _seed_store(tmp_path)
    via_collect = care_chat.collect(collected, store_read)
    assert any(
        s["from"] == "workout" and s["with_domain"] == "supplements"
        for s in via_collect["report"]["seams"]
    )
    assert "workout" in via_collect["conflict_held"]


# --- care_chat: byte-unchanged capture/decompose + collect routes through ONE path


def test_capture_and_decompose_byte_unchanged():
    """The 0043-T1 capture call block + `decompose`/`_derive_goals` are byte-unchanged (this task's
    collect+reconcile is ADDITIVE, placed after + disjoint from the decompose region)."""
    source = Path(care_chat.__file__).read_text()
    capture_block = (
        'extract.persist_extraction(\n'
        '        result.get("extraction"), turn_text, root=store_root,\n'
        '        scaffold_root=scaffold_root, identity_config=identity_config,\n'
        '    )'
    )
    assert capture_block in source, "the 0043-T1 capture call block must be byte-unchanged"
    decompose_block = (
        '    return [\n'
        '        {"domain": domain, "assembled_state": assembled_state, "goals": goals}\n'
        '        for domain in active_domains\n'
        '    ]'
    )
    assert decompose_block in source, "decompose must be byte-unchanged"
    derive_goals_block = (
        '    return {key: value for key, value in record.items() if key.startswith("goal")}'
    )
    assert derive_goals_block in source, "_derive_goals must be byte-unchanged"


def test_collect_routes_through_one_reconcile_path(tmp_path):
    """The care_chat collect step gathers seeded specialist DOMAIN PROGRAMs and routes them through
    the ONE orchestrate.reconcile path (not a second bespoke reconciler), returning report/holds."""
    store_read = _seed_store(tmp_path)
    collected = [
        _candidate("nutrition", seams=[_seam("workout", "advisory")]),
        _candidate("workout"),
    ]
    out = care_chat.collect(collected, store_read)
    # The return IS the orchestrate.reconcile contract (report + the three independent hold sets).
    assert set(out) == {"report", "holds", "conflict_held", "rx_bpmh_held"}
    assert "seams" in out["report"]
    # The collect reaches orchestrate.reconcile through ONE path (a function-level import), no second
    # reconciler defined in care_chat.
    assert not hasattr(care_chat, "reconcile"), "collect must route through orchestrate, not a fork"


# --- care_chat collect-path safety floors (SEC-W3-03, BLOCKING) -----------------


def test_red_s_lea_floor_fires_through_care_chat_collect(tmp_path):
    """SEC-W3-03: the RED-S/LEA floor fires through the care_chat collect+reconcile — the collect
    PRESERVES the source `reason`. REDs if the collect drops the reason."""
    store_read = _seed_store(tmp_path)
    collected = [
        _candidate("nutrition", reason=RED_S_LEA_CLINICAL_ROUTING),
        _candidate("workout"),
    ]
    out = care_chat.collect(collected, store_read)
    assert out["holds"].get("workout") == RED_S_LEA_CROSS_DOMAIN


def test_additive_ae_floor_fires_through_care_chat_collect(tmp_path):
    """SEC-W3-03: the additive-AE floor fires through the care_chat collect+reconcile — the collect
    PRESERVES the source `meta.ae_profile`. REDs if the collect drops meta."""
    store_read = _seed_store(tmp_path)
    shared = {"ae_profile": {"additive_classes": ["bleeding-risk"]}}
    collected = [
        _candidate("supplements", meta=dict(shared)),
        _candidate("peptides", meta=dict(shared)),
    ]
    out = care_chat.collect(collected, store_read)
    assert out["holds"].get("supplements") == ADDITIVE_AE_HELD


def test_rx_bpmh_floor_fires_through_care_chat_collect(tmp_path):
    """SEC-W3-03: the Rx-BPMH floor fires through the care_chat collect+reconcile — the collect
    DERIVES+threads operator_rx_classes from the store. REDs if the collect defaults it to
    frozenset() (the floor goes dead)."""
    store_read = _seed_store(tmp_path, **{"rx-interaction-classes": "bleeding-risk"})
    collected = [
        _candidate("supplements", meta={"ae_profile": {"additive_classes": ["bleeding-risk"]}}),
    ]
    out = care_chat.collect(collected, store_read)
    assert "supplements" in out["rx_bpmh_held"]
