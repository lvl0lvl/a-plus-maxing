"""Care-agent decompose→brief orchestration tests (ADR-0043-T1).

`care_chat.decompose` + the `_care_messages` orchestration rewrite turn the care agent from a
reply-only chatbot into the Orchestrator that DECOMPOSES the operator's goals + assembled state into
one per-specialist brief per active domain. Each brief carries the ADR-0042 assembled record
(identity-stripped, genetics-carved, health-substance detail UNCOLLAPSED), NOT a coarse
`router.summarize` band. Additive to the existing agent: `_care_profile` + the capture path stay
byte-unchanged, so the conversational tests stay green.

PF-S130-01: the production-path test drives the REAL `care_chat.respond` (not `_care_messages` in
isolation) and asserts the orchestration content flows through it — content the old reply-only prompt
did NOT carry — so a revert of the rewrite turns it RED (non-tautological).

MOCK/FIXTURE-tested at 0 live spend: a recording mock backend records the converse payload; the store
is a tmp root; ALL fixtures are SYNTHETIC (0 real operator PII, 0 live API, no key).
"""

import functools
import json
import subprocess
from pathlib import Path

from scripts.plan import router
from scripts.plan.context_assembler import assemble_context
from scripts.serve import care_chat
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]


class _RecordingBackend:
    """A converse backend that records the payload and returns a scripted reply."""

    def __init__(self, *, reply="Noted."):
        self.reply = reply
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        return {"reply": self.reply, "extraction": []}


def _seed(root):
    """Seed a ≥2-domain synthetic profile: stated goals + raw supplement/training/peptide free-text."""
    tp = "2026-06-01T00:00:00+00:00"
    for item, value in (
        ("sex-for-dosing", "male"),
        ("equipment-access-class", "full-home-gym"),
        ("goal-domains", "Workout;Nutrition"),
        ("goal-priority-order", "recovery then strength"),
        ("date-of-birth", "1970"),
        ("raw-supplement-free-text", "creatine 5g daily, omega-3 2g"),
        ("raw-training-detail-free-text", "PPL 6-day split, RPE 8"),
        ("raw-peptide-free-text", "BPC-157 250mcg BID"),
    ):
        store.append(item, {"item": item, "timepoint": tp, "source": "intake", "value": value}, root=root)


def _reader(root):
    return functools.partial(store.read, root=root)


# A plain synthetic assembled record for the pure-`decompose` ACs (a `raw-*` detail per domain +
# stated goals) — the recipe-sanctioned unit fixture. The `raw-*` keys are UNCOLLAPSED detail a coarse
# band would drop, so the band mutation (Step 2.5) reds AC-2/AC-3.
_ASSEMBLED_STATE = {
    "raw-supplement-free-text": "creatine 5g daily, omega-3 2g",
    "raw-training-detail-free-text": "PPL 6-day split, RPE 8",
    "raw-peptide-free-text": "BPC-157 250mcg BID",
    "goal-domains": "Workout;Nutrition",
    "goal-priority-order": "recovery then strength",
    "sex-for-dosing": "male",
    "equipment-access-class": "full-home-gym",
}
_GOALS = {"goal-domains": "Workout;Nutrition", "goal-priority-order": "recovery then strength"}


# --- AC-1: emit N briefs, one per active domain ------------------------------------------------

def test_decompose_emits_one_brief_per_active_domain():
    """Brief count == active-specialist count (≥2-domain fixture)."""
    active = frozenset({"workout", "peptides"})
    briefs = care_chat.decompose(_GOALS, _ASSEMBLED_STATE, active)
    assert isinstance(briefs, list), "decompose must return a list of briefs"
    assert len(briefs) == len(active), (
        f"brief count {len(briefs)} != active-specialist count {len(active)}"
    )


# --- AC-2: each brief carries the assembled record, NOT a coarse band ---------------------------

def test_each_brief_carries_the_assembled_record(tmp_path):
    """Every brief carries the ADR-0042 assembled record (a seeded raw detail), not the coarse band.

    The band control is `router.summarize`'s output over the SAME store — it collapses the raw
    free-text; the assembled record keeps it uncollapsed. The Step-2.5 band mutation (carry the
    collapsed subset) drops the seeded detail and reds this test.
    """
    root = tmp_path / "store"
    _seed(root)
    assembled_state = assemble_context(_reader(root))
    band = router.summarize(_reader(root))
    band_blob = json.dumps(band, sort_keys=True)
    assert "creatine 5g daily" not in band_blob, "fixture invalid: the coarse band already carries the raw detail"

    active = frozenset({"workout", "peptides"})
    briefs = care_chat.decompose(_GOALS, assembled_state, active)
    assert briefs, "decompose returned no briefs"
    for b in briefs:
        blob = json.dumps(b["assembled_state"], sort_keys=True)
        assert "creatine 5g daily" in blob, "a brief dropped the seeded supplement detail (collapsed to a band)"
        assert "PPL 6-day split" in blob, "a brief dropped the seeded training detail (collapsed to a band)"
        assert b["assembled_state"] != band, "a brief collapsed to the coarse router.summarize band"


# --- AC-3: under-briefed falsifier (RED-capable) ------------------------------------------------

def _carries_full_record(brief, assembled_state):
    """The predicate a well-formed brief satisfies: it carries the FULL assembled record."""
    return brief.get("assembled_state") == assembled_state


def test_under_briefed_brief_reds():
    """Every returned brief carries the full assembled record; one missing it drives RED.

    This is the assertion the Step-2.5 band mutation turns RED (a brief carrying only the coarse
    subset != the full `_ASSEMBLED_STATE`).
    """
    active = frozenset({"workout", "peptides"})
    briefs = care_chat.decompose(_GOALS, _ASSEMBLED_STATE, active)
    assert briefs, "decompose returned no briefs"
    for b in briefs:
        assert _carries_full_record(b, _ASSEMBLED_STATE), (
            "a brief omitted the assembled record (or carried only a coarse band)"
        )


# --- AC-4: no un-briefed active specialist, no duplicate briefs ---------------------------------

def test_every_active_domain_gets_exactly_one_brief():
    """The briefed set == the injected active set; exactly one brief per domain (0 un-briefed, 0 dupes)."""
    active = frozenset({"workout", "peptides", "nutrition"})
    briefs = care_chat.decompose(_GOALS, _ASSEMBLED_STATE, active)
    assert {b["domain"] for b in briefs} == set(active), "the briefed domains != the injected active set"
    assert len(briefs) == len(active), "brief count != active count (a domain was skipped or duplicated)"


# --- AC-5: capture call site + _care_profile byte-unchanged -------------------------------------

def _func_src(source_text, name):
    """The exact source segment of the top-level `def name` (mirrors test_plan_model.py:295)."""
    import ast

    for node in ast.parse(source_text).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(source_text, node)
    raise AssertionError(f"function {name!r} not found in source")


def _persist_extraction_src(source_text):
    """The exact source segment of the `extract.persist_extraction(...)` capture call."""
    import ast

    for node in ast.walk(ast.parse(source_text)):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "persist_extraction"):
            return ast.get_source_segment(source_text, node)
    raise AssertionError("extract.persist_extraction(...) call not found in source")


def test_capture_call_site_byte_unchanged():
    """The additive rewrite left the gated capture call + `_care_profile` BYTE-unchanged vs origin/main (AC-5).

    Hardened from a 4-landmark `in`-check to byte-equality (QA-T2-03): `_care_profile`'s full source AND
    the `extract.persist_extraction(...)` capture-call region are extracted from BOTH the current tree and
    `origin/main` and asserted byte-identical — so a change to either region that preserved the old landmark
    substrings can no longer pass. The care agent still PROPOSES facts through the same
    de-identify-by-data-class gate, and the private full-profile builder is untouched.
    """
    current = Path(care_chat.__file__).read_text()
    base = subprocess.run(
        ["git", "show", "origin/main:scripts/serve/care_chat.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert _func_src(current, "_care_profile") == _func_src(base, "_care_profile"), (
        "_care_profile changed vs origin/main — the additive rewrite must leave it byte-unchanged"
    )
    assert _persist_extraction_src(current) == _persist_extraction_src(base), (
        "the extract.persist_extraction capture-call region changed vs origin/main"
    )


# --- PF-S130-01: production-path integration (MANDATORY, non-tautological) ----------------------

def test_orchestration_prompt_flows_through_respond_real_path(tmp_path):
    """The orchestration decompose→brief content flows through the REAL `respond` path.

    Drives the whole `respond -> _care_messages -> converse` path (not `_care_messages` in isolation):
    the recorded index-0 context carries the orchestration system-prompt block AND one brief per active
    domain, each carrying the assembled record — content the OLD reply-only prompt did NOT carry. The
    Step-2.5 revert-to-reply-only mutation turns this RED (proving it is not tautological).
    """
    root = tmp_path / "store"
    _seed(root)
    scaffold = tmp_path / "scaffold"
    backend = _RecordingBackend()
    active = frozenset({"workout", "peptides"})
    care_chat.respond("plan my next block", [], client=backend, store_root=root,
                      scaffold_root=scaffold, active_domains=active)
    assert len(backend.calls) == 1, "the care turn did not make exactly one converse call"
    first = json.loads(backend.calls[0][0]["content"])
    # the orchestration system-prompt block — absent from the old reply-only prompt
    assert first.get("orchestration"), "the orchestration system-prompt block is absent through the real respond path"
    # one brief per active domain, each carrying the assembled record
    briefs = first.get("briefs")
    assert briefs and len(briefs) == len(active), f"expected {len(active)} briefs through the real path, got {briefs}"
    assert {b["domain"] for b in briefs} == set(active), "the real-path briefs do not cover the injected active set"
    for b in briefs:
        blob = json.dumps(b["assembled_state"], sort_keys=True)
        assert "creatine 5g daily" in blob, "a real-path brief dropped the seeded assembled detail"


# --- QA-03: `respond` derives a NON-EMPTY goals into each brief ---------------------------------

def test_respond_derives_goals_into_briefs(tmp_path):
    """`respond` threads a NON-EMPTY derived `goals` (the seeded stated goal) into every brief.

    Closes the gap that the unit ACs seed `goals` directly into `decompose`, bypassing `respond`'s
    derivation. Drives the REAL path: a broken/empty derivation in `respond` reds this.
    """
    root = tmp_path / "store"
    _seed(root)
    scaffold = tmp_path / "scaffold"
    backend = _RecordingBackend()
    active = frozenset({"workout", "peptides"})
    care_chat.respond("go", [], client=backend, store_root=root,
                      scaffold_root=scaffold, active_domains=active)
    first = json.loads(backend.calls[0][0]["content"])
    briefs = first["briefs"]
    assert briefs, "no briefs were produced through the real path"
    for b in briefs:
        assert b.get("goals"), f"a brief carried an empty derived goals: {b.get('goals')}"
        assert "recovery then strength" in json.dumps(b["goals"]), (
            "the seeded stated goal was not derived into the brief"
        )


# --- Additive preservation: no active set => byte-equivalent to today's conversational turn ------

def test_respond_default_no_active_set_preserves_conversation(tmp_path):
    """`respond` with NO injected active set still returns `{reply, receipt}` + the care-conversation context.

    Proves the orchestration is ADDITIVE: the existing agent (the empty-set default caller, e.g.
    server.py:498) is unaffected — no orchestration block, no briefs, the conversational context intact.
    """
    root = tmp_path / "store"
    _seed(root)
    scaffold = tmp_path / "scaffold"
    backend = _RecordingBackend()
    result = care_chat.respond("hi", [], client=backend, store_root=root, scaffold_root=scaffold)
    assert set(result) >= {"reply", "receipt"}, "the default no-active-set return shape changed"
    first = json.loads(backend.calls[0][0]["content"])
    assert first.get("task") == "care-conversation", "the conversational context was dropped"
    assert "briefs" not in first, "briefs leaked into a no-active-set turn (not additive)"
    assert "orchestration" not in first, "the orchestration block leaked into a no-active-set turn (not additive)"
