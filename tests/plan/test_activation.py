"""ADR-0046-T1 integration tests: the progressive-activation gate + the BUG-01 (bead 58z0)
periodized-prescription reconciliation.

Two coherent units exercised over shared synthetic fixtures:

  - `scripts.plan.activation` — the progressive-activation gate. `active_domains(surface)` computes
    the active CARD-EMITTING domain set (a subset of `activation.CARD_DOMAINS`, the §1-§13 card
    roster, decoupled from the closed-four `plan_schema.PLAN_DOMAINS`) from a de-id-safe operator
    surface; the §14-genetics / §15-labs cross-cutting inputs are partitioned OUT (never card
    domains). AC-1 data-driven, AC-2 reach beyond the four, AC-3 empty-state-no-card, AC-4
    data-present-dispatch, AC-5 fan-out bound, AC-6 partition, plus the current-four
    registry-coherence gate.
  - The `generate_plan` 58z0 `prescription->renderable` projection (over the EXISTING four
    translators): a CANONICAL PERIODIZED prescription (dated `blocks`, per-block `load`) records
    0 `load` at any depth, a BLOCKS-ONLY prescription does not crash `record_plan` (honest no-plan),
    and a periodized program round-trips 0-of-7-dropped with its dated blocks intact.

All fixtures are synthetic literals (no real operator PII); the author envelope rides the captured
`_FixedEnvelopeClient` seam that `compute_plan`/`generate_plan` wrap over `author_output` — no live
`ModelClient`, no live API, 0 spend. The roster-growth production-path AC-2 (a rich domain DISPATCHES
+ records first-class) is ADR-0043-T3 (Wave 4), not here.
"""

import functools
import subprocess
from pathlib import Path

import pytest

from scripts.plan import activation, domain_program, generate_plan, plan_driver
from scripts.store import keying, plan_schema, store

PLAN_DATE = "2026-06-18"
REPO_ROOT = Path(__file__).resolve().parents[2]

# The rec-embedded / plan-attached uniform-program key (the migration's ride key), held as a literal
# so the module imports + collects cleanly on the pre-reconciliation tree (the 58z0 revert-REDs proof
# runs the SAME test body against the un-reconciled code).
PROGRAM_KEY = "domain_program"

# The freeze-break numstat probe base (mirrors tests/plan/test_generate_plan_uniform.py:55's
# PRE_TASK_HEAD pattern). wdhc: the ADR-0046-T1 entry HEAD 7038c25a is an intermediate wave commit
# (orphan-prone — the repo squash-merges); repointed to the merge-base 3e17b1d8 (== origin/main), a
# durable reachable base. Only 0046-T1 edits activation.py/generate_plan.py in the wave, so their
# numstat vs the merge-base equals vs the entry HEAD; the frozen paths are byte-untouched vs both.
PRE_TASK_HEAD = "3e17b1d8291d86d48441e36177a71f34910fbe57"

# The canonical periodized blocks (dated phases, per-block `load` — PF-S131-01). A fresh copy is spun
# per fixture so no test mutates the shared literal.
_PERIODIZED_BLOCKS = (
    {"date": "2026-08-01", "phase": "wk1", "load": "80% 1RM"},
    {"date": "2026-08-08", "phase": "wk2", "load": "82.5% 1RM"},
)


# --- fixtures ------------------------------------------------------------------


def _seed_store(root, **overrides):
    """Seed PII-free operator-state items into a real temp store; return a bound reader.

    Backs the pass-through Summary Field-Set fields `assemble_context` reads (mirrors
    tests/plan/test_generate_plan_uniform.py's `_seed_store`). Returns a `store.read` pre-bound to
    `root` (the summarize caller contract).
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


def _author(*recs, specialist="personal-trainer"):
    """A captured author envelope carrying `recs`."""
    return {"specialist": specialist, "recommendations": list(recs)}


def _uniform_program(prescription, kind, *, required_labs=None):
    """A conformant seven-field DOMAIN PROGRAM (`domain_program.validate` passes)."""
    return {
        domain_program.PRESCRIPTION: prescription,
        domain_program.RATIONALE: {
            "certainty_of_evidence": "moderate",
            "strength_of_recommendation": "strong",
            "causal_marker": "associational",
        },
        domain_program.MONITORING_SIGNALS: [
            {"signal": "morning HRV", domain_program.SIGNAL_TIER_KEY: "moderate"},
        ],
        domain_program.ADJUSTMENT_RULES: [
            {"trigger": "HRV drop >1SD across 3 days", "action": "reduce volume 20%"},
        ],
        domain_program.REQUIRED_LABS: list(required_labs) if required_labs else [],
        domain_program.REFUSAL_ESCALATION: {"marker": "chest pain -> stop + clinician review"},
        domain_program.CROSS_DOMAIN_SEAMS: [
            {"paired_domain": "nutrition", "seam": "energy availability floor"},
        ],
        domain_program.KIND_FIELD: kind,
    }


def _has_load_at_any_depth(value):
    """Whether a `load` key appears at ANY depth of `value` (dicts + lists)."""
    if isinstance(value, dict):
        return "load" in value or any(_has_load_at_any_depth(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_load_at_any_depth(item) for item in value)
    return False


def _fresh_blocks():
    """A fresh deep copy of the canonical periodized blocks."""
    return [dict(block) for block in _PERIODIZED_BLOCKS]


def _periodized_workout_rec():
    """A workout rec whose uniform-program prescription is PERIODIZED WITH a top-level renderable
    identity (`name`/`sets`) alongside dated `blocks` — the canonical shape that records."""
    prescription = {
        "name": "Back squat", "sets": 3, "load": "75% 1RM", "blocks": _fresh_blocks(),
    }
    return {
        "claim": "periodized back-squat progression",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        PROGRAM_KEY: _uniform_program(prescription, "training"),
    }


def _blocks_only_workout_rec():
    """A workout rec whose prescription is BLOCKS-ONLY — dated `blocks` with NO top-level renderable
    identity (`{"blocks": [...]}`), the degenerate periodized shape the pre-fix path crashed on."""
    prescription = {"blocks": _fresh_blocks()}
    return {
        "claim": "periodized progression with no top-level renderable identity",
        "source": "ACSM resistance-training guidelines 2024",
        "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation",
        "category": "training",
        PROGRAM_KEY: _uniform_program(prescription, "training"),
    }


# --- AC-1: the active set is data-driven ---------------------------------------


def test_active_set_is_data_driven():
    """AC-1: `active_domains` is data-driven — two surfaces yield DIFFERENT active sets equal to
    their computed active domains. A gate returning the same set regardless of surface -> RED."""
    surface1 = {"goals": ["workout"], "data": ["sleep"]}
    surface2 = {
        "goals": ["workout"], "data": ["supplements", "recovery"],
        "mentions": ["longevity"], "lab_or_trait_touches": ["gi"],
    }
    active1 = activation.active_domains(surface1)
    active2 = activation.active_domains(surface2)
    assert active1 == {"workout", "sleep"}
    assert active2 == {"workout", "supplements", "recovery", "longevity", "gi"}
    assert active1 != active2


# --- AC-2: reach a card domain beyond the original four (pure, Option C) --------


def test_active_domains_reaches_new_card_domain():
    """AC-2 (PURE reach, re-grounded Option C): `active_domains(surface)` RETURNS a §1-§13
    `CARD_DOMAINS` domain D BEYOND the original four when D is active on the surface. Non-tautology:
    a closed-four `active_domains` (or a `CARD_DOMAINS` missing D) never returns D -> RED."""
    d = "sleep"
    assert d not in plan_schema.PLAN_DOMAINS, "D must be beyond the closed four to prove reach"
    assert d in activation.CARD_DOMAINS
    surface = {"goals": [d]}
    assert d in activation.active_domains(surface)


# --- AC-3: empty-state domain is not active and records no personalized card ----


def test_empty_state_domain_not_active_no_card(tmp_path):
    """AC-3 (false-positive falsifier): an empty-state domain D (no goal/data) is NOT in
    `active_domains`, AND an empty-state RENDERABLE domain records no personalized card (honest
    no-plan). An always-full activation, or a fabricated card on empty state -> RED."""
    surface = {"goals": ["workout"]}
    empty_state = "dermatology"
    assert empty_state in activation.CARD_DOMAINS
    assert empty_state not in activation.active_domains(surface)

    # A thin-library envelope for a renderable domain records NOTHING (honest no-plan, not a card).
    store_read = _seed_store(tmp_path)
    result = generate_plan.generate_plan(
        "supplements", {"specialist": "supplement-specialist", "thin_library": True},
        store_read, tmp_path, plan_date=PLAN_DATE,
    )
    assert result["recorded"] is False
    assert result["reason"], "the honest no-plan reason must be set (0 fabricated card)"


# --- AC-4: a data-present domain is active -------------------------------------


def test_data_present_domain_is_active():
    """AC-4 (false-negative falsifier): a domain D with data present IS in `active_domains`. A
    missed active domain -> RED. (Composes with AC-2's reach on a beyond-the-four domain.)"""
    d = "endocrine"
    assert d not in plan_schema.PLAN_DOMAINS
    surface = {"data": [d]}
    assert d in activation.active_domains(surface)


# --- AC-5: the active set is bounded to the surface (fan-out) -------------------


def test_fan_out_bounded_to_active_set():
    """AC-5 (fan-out bound): for a NARROW-surface operator, `|active_domains|` is a PROPER subset of
    `CARD_DOMAINS`. `|active set| == |CARD_DOMAINS|` on a narrow surface -> RED."""
    narrow = {"goals": ["workout"]}
    active = activation.active_domains(narrow)
    assert len(active) < len(activation.CARD_DOMAINS)


# --- AC-6: genetics / labs partitioned as cross-cutting inputs (disposition #25)


def test_genetics_labs_partitioned_as_cross_cutting_inputs():
    """AC-6 (roster partition): the §14-genetics / §15-labs specialists are NOT card-emitting —
    absent from `CARD_DOMAINS` (trivially also from the closed-four `PLAN_DOMAINS`) and never
    returned by `active_domains` as card domains, even when the surface names them. Adding
    genetics/labs to `CARD_DOMAINS` -> RED."""
    for cross_cutting in ("genetics", "labs"):
        assert cross_cutting not in activation.CARD_DOMAINS
        assert cross_cutting not in plan_schema.PLAN_DOMAINS
    surface = {
        "goals": ["genetics", "labs", "sleep"],
        "lab_or_trait_touches": ["genetics", "labs"],
    }
    active = activation.active_domains(surface)
    assert "genetics" not in active
    assert "labs" not in active
    assert "sleep" in active, "the surface is otherwise live (partition, not a no-op gate)"
    assert activation.CARD_DOMAINS.isdisjoint(activation.CROSS_CUTTING_INPUTS)


# --- current-four registry coherence -------------------------------------------


def test_registries_coherent_over_current_four():
    """Current-four coherence gate: every `PLAN_DOMAINS` member is dispatchable, translatable, and
    kinded over the CLOSED FOUR; `PLAN_DOMAINS` is still exactly four (growth is Wave 4); and
    `CARD_DOMAINS` (the gate's card roster) has >=13 members. An orphan `PLAN_DOMAINS` member, a
    prematurely-grown `PLAN_DOMAINS`, or a <13 `CARD_DOMAINS` -> RED."""
    current_four = set(plan_schema.PLAN_DOMAINS)
    assert current_four <= set(generate_plan._PLAN_TRANSLATORS)
    assert current_four <= set(plan_driver._ROLE_OF_DOMAIN)
    assert current_four <= set(generate_plan._DOMAIN_KIND)
    assert plan_schema.PLAN_DOMAINS == ("workout", "nutrition", "supplements", "peptides")
    assert len(activation.CARD_DOMAINS) >= 13


# --- BUG-01 / bead 58z0: the periodized-prescription reconciliation ------------


def test_periodized_program_records_zero_load_at_any_depth(tmp_path):
    """58z0-(1): a canonical PERIODIZED workout prescription (dated `blocks`, per-block `load`)
    records with 0 `load` at ANY depth in BOTH every renderable exercise AND the store-bound
    `program["prescription"]` — the clearance gate + deep-strip hold on the periodized shape."""
    store_read = _seed_store(tmp_path)
    result = generate_plan.generate_plan(
        "workout", _author(_periodized_workout_rec()), store_read, tmp_path,
        plan_date=PLAN_DATE, gates={"clearance_granted": False},
    )
    assert result["recorded"] is True, "the periodized workout must record a plan"
    plan = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert plan is not None, "the recorded workout plan must read back"
    for exercise in plan["exercises"]:
        assert not _has_load_at_any_depth(exercise), "an un-cleared load survived in the renderable"
    program = plan.get(PROGRAM_KEY)
    assert program is not None, "the seven-field program must ride the record path"
    assert not _has_load_at_any_depth(program[domain_program.PRESCRIPTION]), (
        "an un-cleared load survived in the store-bound program prescription"
    )


def test_blocks_only_prescription_does_not_crash(tmp_path):
    """58z0-(2): a BLOCKS-ONLY prescription (dated `blocks`, NO top-level `name`/`sets`) does NOT
    crash `generate_plan` — honest handling, never a raised ValueError/KeyError from `record_plan`.

    Revert-REDs proof: against the pre-reconciliation flat-consuming translator, `record_plan` raises
    `ValueError("workout plan exercise missing required field 'name'")` — the call raising == this
    test erroring == RED against the un-reconciled tree.
    """
    store_read = _seed_store(tmp_path)
    result = generate_plan.generate_plan(
        "workout", _author(_blocks_only_workout_rec()), store_read, tmp_path,
        plan_date=PLAN_DATE, gates={"clearance_granted": False},
    )
    # Honest no-plan: no personalized card fabricated from a degenerate periodized-only shape.
    assert result["recorded"] is False, "a blocks-only prescription must not fabricate a card"
    assert result["reason"], "the honest no-plan reason must be set"


def test_periodized_program_round_trips_intact(tmp_path):
    """58z0-(3): a periodized program round-trips — all seven `domain_program` fields present on
    read-back (0 dropped) AND the dated `blocks` intact in the stored `program["prescription"]`.
    CLEARED, so the fidelity leg preserves the blocks (incl. per-block `load`). Dropped/flattened
    blocks -> RED."""
    store_read = _seed_store(tmp_path)
    result = generate_plan.generate_plan(
        "workout", _author(_periodized_workout_rec()), store_read, tmp_path,
        plan_date=PLAN_DATE, gates={"clearance_granted": True},
    )
    assert result["recorded"] is True, "the cleared periodized workout must record a plan"
    plan = plan_schema.read_plan("workout", PLAN_DATE, tmp_path)["plan"]
    assert plan is not None
    program = plan.get(PROGRAM_KEY)
    assert program is not None, "the seven-field program must ride the record path"
    seven = domain_program.REQUIRED_FIELDS + domain_program.CONDITIONAL_FIELDS
    assert [f for f in seven if f not in program] == [], "0-of-7 program fields dropped"
    stored_blocks = program[domain_program.PRESCRIPTION]["blocks"]
    assert stored_blocks == list(_PERIODIZED_BLOCKS), (
        "the dated periodized blocks must round-trip intact (cleared -> load preserved)"
    )


# --- freeze-break numstat (FROZEN-SPINE, per-ADR-scoped) ------------------------


def _numstat(base, *paths):
    """`git diff --numstat <base> -- <paths>` over the repo, stripped."""
    out = subprocess.run(
        ["git", "diff", "--numstat", base, "--", *paths],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def test_per_adr_scoped_freeze_break_numstat():
    """FROZEN-SPINE (per-ADR-scoped): the sanctioned edits touch exactly `activation.py` +
    `generate_plan.py`; `plan_schema.py`/`plan_driver.py` (frozen for this task — the roster growth
    is Wave 4) + the HARD-frozen four are byte-untouched vs the task-entry HEAD; the <always-frozen>
    six-file set is EMPTY over the whole build; and `PLAN_DOMAINS` is STILL the closed four.

    RED-capable: a transient edit to any forbidden file makes (b)/(c) non-empty -> RED; a grown
    `PLAN_DOMAINS` makes (d) RED.
    """
    # (a) the sanctioned edits changed exactly these two surfaces.
    assert _numstat(
        PRE_TASK_HEAD, "scripts/plan/activation.py", "scripts/plan/generate_plan.py"
    ) != "", "the sanctioned edits must change activation.py + generate_plan.py"
    # (b) plan_schema.py + plan_driver.py (frozen for this task) + the HARD-frozen four untouched.
    assert _numstat(
        PRE_TASK_HEAD,
        "scripts/store/plan_schema.py", "scripts/plan/plan_driver.py",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
    ) == "", "plan_schema.py/plan_driver.py + the HARD-frozen four must be byte-untouched"
    # (c) the <always-frozen> six-file HARD set is EMPTY over the whole build (origin/main base).
    assert _numstat(
        "origin/main",
        "scripts/store/store.py", "scripts/store/keying.py",
        "scripts/plan/pipeline.py", "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py", "scripts/plan/router.py",
    ) == "", "the <always-frozen> HARD set must be numstat=0 over the whole build"
    # (d) PLAN_DOMAINS is STILL the closed four (the roster growth is Wave 4 / ADR-0043-T3).
    assert plan_schema.PLAN_DOMAINS == ("workout", "nutrition", "supplements", "peptides")


# --- AC-7: offline, 0 live-API, 0 real PII, 0 live-client import ----------------


def test_module_imports_no_live_client_seam():
    """AC-7: the module imports only pytest + the manifest modules + `scripts.store` fixtures + the
    READ-ONLY `plan_schema`/`plan_driver`/`generate_plan` imports the coherence gate needs — 0
    live-client / live-API import (the author envelope rides the captured `_FixedEnvelopeClient`
    seam that `compute_plan` wraps over `author_output`, no real `ModelClient`)."""
    import inspect
    import sys

    src = inspect.getsource(sys.modules[__name__])
    import_lines = [
        ln for ln in src.splitlines() if ln.strip().startswith(("import ", "from "))
    ]
    joined = "\n".join(import_lines)
    assert "anthropic" not in joined, "no live-API SDK import"
    assert "ModelClient" not in joined, "no live-client import (the captured-envelope seam is used)"
    assert "scripts.model" not in joined, "no live model-client import"
