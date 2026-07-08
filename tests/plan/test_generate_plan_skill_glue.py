"""Tests for the `/generate-plan` A′ subscription-driver GLUE contract (ADR-0026-T3).

The `.claude/skills/generate-plan/SKILL.md` front door reconciles the superseded runtime-A
`/generate-plan` session to the A′ subscription-driver path: de-id the raw intake via the
ADR-0027 `ModelClient.deidentify` client → dispatch each plan-domain specialist + each safety
lens as a SUBSCRIPTION agent over the de-identified summary → drive the ONE shared driver
(`plan_driver.drive`, gated through the composed `gate_dispatch`) → `reinsert_out` →
`reemit_maintained`. The skill is PROSE — it CALLS the merged seams, it re-hosts no loop.

This suite is the THIN GLUE CONTRACT over those EXISTING seams (no production Python is added):
the glue is the documented call sequence the skill prose names, exercised against the merged
`deid_in` / `plan_driver` / `gate_dispatch` seams with FIXTURE dispatch (0 live agent dispatch,
0 live spend). It pins the six acceptance criteria:

  - AC-1 (de-id via `ModelClient.deidentify`, NOT `router.summarize`): the glue drives the
    de-id-IN step through `deid_in(raw_intake, ModelClient(backend=<fixture>))` — the de-id seam
    is the `ModelClient.deidentify` call, not a `router.summarize` substitute. The SKILL.md prose
    half is the phase-scoped grep below.
  - AC-2 (0-raw-PII to any subscription agent, FULL-PAYLOAD STRING scan): over a synthetic
    raw-PII intake, every dispatch payload the glue/driver issues carries the de-identified
    summary only — the ENTIRE payload serialized to a string (`json.dumps(payload, default=str)`)
    carries 0 raw-PII tokens (the single method, demonstrated RED against an in-string variant a
    dict/list recursion would miss).
  - AC-3 (no-fork at the skill level): a comment-stripped grep over `SKILL.md` finds 0 copies of
    the EXECUTABLE safety-loop control flow (a `while True:` header + the
    `disposition.get("safety_passed") is True` gate EXPRESSION at a non-comment line) — the skill
    drives the ONE shared driver, it does not re-host the loop.
  - AC-4 (glue drives the shared driver): the glue feeds the shared driver a fixture envelope per
    yielded dispatch-request and the driver completes a synthetic run (de-id → loop → promote).
  - AC-5 (S94-deferral documented): `SKILL.md` documents the LIVE subscription dispatch as the
    S94 operator-present attestation (NOT a mock-test target) — what IS vs ISN'T mock-testable is
    explicit.
  - AC-6 (suite gate): this suite runs with 0 live calls (the `_ClaudeNoTrainBackend` is never
    constructed; every client/dispatch is a fixture).

The LIVE subscription dispatch over REAL agents is the S94 operator-present attestation, NOT a
mock-test target: the glue test drives the shared driver with a FIXTURE `dispatch`, never a real
agent. The glue STRUCTURALLY only ever holds the `deid_in` summary; whether a REAL subscription
agent receives only the summary on the LIVE path is the residual 0-leak property flagged for the
S94 checkpoint owner (SEC-6). Every client/dispatch here is a mock/fixture; no test hits a live
API, and the test tree carries 0 real operator PII (synthetic tokens only).
"""

import inspect
import json
import subprocess
from pathlib import Path

from scripts.guard import pii_scan
from scripts.model.client import ModelClient
from scripts.plan import plan_driver, plan_step
from scripts.plan.deid_in import deid_in
from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.plan.plan_orchestrator import run_orchestrated
from scripts.store import store

from tests.plan.test_deid_in import (
    SYNTHETIC_LAB,
    SYNTHETIC_NAME,
    _FixedDeidClient,
    _identity_config,
    _raw_intake,
)
from tests.plan.test_generate_plan import (
    PLAN_DATE,
    _author,
    _seed_store,
    _workout_rec,
)
from tests.plan.test_orchestrate import _recon
from tests.plan.test_plan_orchestrator import (
    _RecordingDispatch,
    _deid_summary,
    _sustaining_authors,
)
from tests.plan.test_plan_step import _fulfil, _run_through_step
from tests.plan.test_quality_judge import _FixedJudgeClient, _clean_scores
from tests.plan.test_revise_loop import (
    _bpmh_store,
    _clean_composing_gate,
    _clearing_liaison,
    _clearing_reauthor,
    _replay_safety_authors,
)
from tests.plan.test_safety_review import _no_findings_dispatch

# A synthetic contact token that trips the value-CLASS scan (email) WITHOUT any identity config —
# the planted-leak token. Mirrors the `deid_in` contact-PII precedent (test_deid_in.py).
_LEAK_EMAIL = "jordan.fake@test-clinic.example.org"


# The reconciled A′ skill front door under test — the file the prose-grep ACs read.
SKILL_MD = Path(".claude/skills/generate-plan/SKILL.md")

# The two domains the glue exercises (a fuelable workout + a sustaining nutrition budget) — the
# `_sustaining_authors` clean two-domain set surfaces both via a clean composed disposition.
_DOMAINS = ("workout", "nutrition")


class _DeidBackend:
    """A fixture model-client backend whose `deidentify` returns a fixed de-identified summary.

    The fixture backend the glue injects into a REAL `ModelClient` so the de-id-IN step routes
    through `ModelClient.deidentify` (the ADR-0027 seam) — NOT a `router.summarize` substitute —
    with 0 live spend (the `_ClaudeNoTrainBackend` is never constructed). It returns the
    band/class summary a faithful de-id call emits, carrying NONE of the synthetic raw-PII tokens.

    Attributes:
        summary (dict): The de-identified summary `deidentify` returns.
    """

    def __init__(self, summary):
        self.summary = summary
        self.calls = []

    def deidentify(self, raw_intake):
        self.calls.append(raw_intake)
        return dict(self.summary)


def _clean_composed_gate():
    """The composed `gate_dispatch` over a clean judge + a no-findings safety dispatch (both PASS).

    The driver's `gate_dispatch=` seam: `compose_gate_dispatch` maps the two gates' native shapes
    into the 3-key disposition the driver reads. A clean composite surfaces the plan (accept +
    safety_passed) so the synthetic run promotes — fixture judge/review, 0 live spend.
    """
    return compose_gate_dispatch(_FixedJudgeClient(_clean_scores()), _no_findings_dispatch())


# === AC-1: the glue's de-id-IN routes through ModelClient.deidentify (not summarize) ===


def test_glue_deid_in_routes_through_model_client():
    # AC-1 (glue half): the A′ de-id-IN step drives `deid_in(raw_intake, ModelClient(backend=...))`
    # — the de-id seam is the injected `ModelClient.deidentify` call (the ADR-0027 path), not a
    # `router.summarize` substitute. The fixture backend records the call so this pins the de-id
    # routed through the model-client seam, and the returned summary is the de-identified summary
    # the dispatch authors over (carrying 0 raw-PII tokens). A glue that called `router.summarize`
    # as the de-id-IN would leave the backend's `.calls` empty -> RED.
    backend = _DeidBackend(_deid_summary())
    client = ModelClient(backend=backend)

    summary = deid_in(_raw_intake(), client)

    # the de-id-IN routed through ModelClient.deidentify (the backend's deidentify fired)
    assert backend.calls, "the de-id-IN did not route through ModelClient.deidentify"
    assert backend.calls[0] == _raw_intake()
    # the returned summary is the de-identified summary (success: no `deidentified` sentinel key)
    assert "deidentified" not in summary
    assert summary == _deid_summary()
    # and it carries 0 of the seeded synthetic raw-PII tokens
    serialized = json.dumps(summary, default=str)
    assert SYNTHETIC_NAME not in serialized
    assert SYNTHETIC_LAB not in serialized


def test_glue_deid_in_uses_only_the_injected_client(monkeypatch):
    # AC-1 (non-vacuous): the glue's de-id-IN constructs NO second ModelClient — it uses ONLY the
    # injected client (the no-second-client half). A ModelClient.__init__ spy confirms `deid_in`
    # self-constructs 0 clients during the call (the only construction is the test's own, before
    # the spy is installed) -> 0 live spend, no hidden live backend.
    backend = _DeidBackend(_deid_summary())
    client = ModelClient(backend=backend)

    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)
    deid_in(_raw_intake(), client)

    assert instantiations == [], "the glue de-id-IN constructed a second ModelClient"


# === AC-4: the glue drives the shared driver to a promoted synthetic run ===


def test_glue_drives_plan_driver_to_promote(tmp_path):
    # AC-4: the glue feeds the shared driver a fixture envelope per yielded dispatch-request and
    # the driver completes a synthetic run (de-id -> loop -> promote). The A′ subscription path is
    # `run_orchestrated` driving `plan_driver.drive` with the composed `gate_dispatch` — the glue
    # CALLS the driver's drive-protocol (the consumer SENDs the captured authors back per yielded
    # request); it does NOT re-host the loop. Fixture `dispatch` (0 live agent dispatch, 0 live
    # spend) + a clean composed disposition surfaces the plan.
    store_read = _seed_store(tmp_path)
    client = ModelClient(backend=_DeidBackend(_deid_summary()))
    dispatch = _RecordingDispatch(_sustaining_authors())
    gate = _clean_composed_gate()

    out = run_orchestrated(
        _raw_intake(), client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=_DOMAINS, gate_dispatch=gate,
    )

    # the driver completed a synthetic run and promoted the survivors into root
    recorded = [d for d, r in out["results"].items() if r.get("recorded") is True]
    assert len(recorded) >= 1, "the glue did not drive the shared driver to a promoted plan"
    assert store.read("plan::workout", root=tmp_path) != []
    # the specialist dispatch fired through the fixture seam (0 live spend)
    assert dispatch.calls, "no specialist dispatch fired through the glue's driver"


def test_glue_drive_protocol_does_not_rehost_the_loop():
    # AC-4 (the glue CALLS the driver, does not re-implement it): the A′ path's autonomous loop is
    # owned by `plan_driver.drive` ALONE. Pin that the consumer the glue drives (`run_orchestrated`)
    # holds NO `while True:` revise-loop control flow of its own — it advances the driver and SENDs
    # captured authors, the loop lives in `plan_driver`. The orchestrator's only `while True:` is
    # the drive-protocol pump (advance + send), not a gate->branch->re-dispatch safety loop; the
    # safety-loop EXPRESSION (`safety_passed is True` as a control-flow gate) lives only in the
    # driver. A consumer that re-hosted the safety gate would carry that expression -> RED.
    import inspect

    from scripts.plan import plan_driver, plan_orchestrator

    orchestrator_src = inspect.getsource(plan_orchestrator)
    driver_src = inspect.getsource(plan_driver)

    # the safety-surface gate EXPRESSION lives in the driver (the ONE definition) ...
    assert 'disposition.get("safety_passed") is True' in driver_src
    # ... and NOT re-hosted in the consumer the glue drives (no forked safety gate).
    assert 'disposition.get("safety_passed") is True' not in orchestrator_src


# === AC-2: 0-raw-PII to any dispatch — the FULL-PAYLOAD STRING scan (QA-5 + QA-7) ===


def _serialized_dispatch_payloads(dispatch):
    """Serialize EVERY captured dispatch payload to a single string (the QA-7 full-payload scan).

    `_RecordingDispatch` captures each `(domain, prompt, summary)` the consumer issued as
    `{"domain", "prompt", "summary"}`. The scan serializes the ENTIRE payload to a string via
    `json.dumps(payload, default=str)` and yields THAT string — the single method (NOT a
    dict/list recursion). The live `_dispatch_prompt` payload is itself a FLAT STRING with
    `json.dumps(summary)` embedded ([plan_orchestrator.py:101-124]), so a dict/list recursion
    alone would miss a raw token sitting INSIDE the stringified prompt; the whole-payload-to-string
    serialize catches a raw token wherever it lands — top-level, a nested sub-dict, OR embedded in
    the stringified prompt body.
    """
    return [json.dumps(call, default=str) for call in dispatch.calls]


def test_no_raw_pii_in_any_dispatch_payload_serialized(tmp_path):
    # AC-2 (the crown-jewel 0-leak, FULL-PAYLOAD STRING scan): over a synthetic raw-PII intake (a
    # seeded legal name + lab value), every dispatch payload the glue/driver issues carries the
    # de-identified summary only — the ENTIRE payload serialized to a string carries 0 raw-PII
    # tokens. The glue only ever holds the `deid_in` summary, never the raw intake, after the
    # de-id-IN step. A variant whose dispatch payload embedded the raw intake (in a nested field OR
    # concatenated into the prompt string) would go RED on the serialized-string scan -> the
    # whole-payload-to-string serialize is load-bearing.
    store_read = _seed_store(tmp_path)
    client = ModelClient(backend=_DeidBackend(_deid_summary()))
    dispatch = _RecordingDispatch(_sustaining_authors())
    gate = _clean_composed_gate()

    run_orchestrated(
        _raw_intake(), client, dispatch, store_read, tmp_path,
        plan_date=PLAN_DATE, domains=_DOMAINS, gate_dispatch=gate,
    )

    assert dispatch.calls, "no specialist dispatch fired (the scan would be vacuous)"
    for serialized in _serialized_dispatch_payloads(dispatch):
        assert SYNTHETIC_NAME not in serialized, "a dispatch payload carried the raw legal name"
        assert SYNTHETIC_LAB not in serialized, "a dispatch payload carried the raw lab value"


def test_full_payload_scan_goes_red_against_an_in_string_raw_token():
    # AC-2 (the scan has TEETH — the in-string-raw-token case a dict/list recursion would MISS):
    # a dispatch payload whose `prompt` is a FLAT STRING with the raw legal name concatenated in
    # (the `_dispatch_prompt` shape, but raw-contaminated) MUST go RED on the full-payload-string
    # scan. A dict/list recursion over `{"domain", "prompt", "summary"}` whose `summary` is clean
    # but whose `prompt` STRING embeds the raw token would MISS it (the raw is inside a string
    # value, not a separate key) — so this proves the whole-payload-to-string serialize is the
    # load-bearing method, not an interchangeable alternative.
    clean_summary = _deid_summary()
    # the contaminated payload: a clean summary, but the raw name embedded in the FLAT prompt string
    contaminated = {
        "domain": "workout",
        "prompt": f"## role profile ...\n\n## summary\n{json.dumps(clean_summary)}\n"
                  f"raw operator note: {SYNTHETIC_NAME}\n",
        "summary": clean_summary,
    }

    # the full-payload-string scan CATCHES the in-string raw token (goes RED)
    serialized = json.dumps(contaminated, default=str)
    assert SYNTHETIC_NAME in serialized, (
        "the full-payload-string scan must catch a raw token embedded in the prompt string"
    )
    # and the dict/list-recursion ALTERNATIVE would MISS it (the summary dict is clean — the raw
    # lives only inside the prompt STRING value) — proving the serialize method is load-bearing.
    summary_only_serialized = json.dumps(contaminated["summary"], default=str)
    assert SYNTHETIC_NAME not in summary_only_serialized, (
        "the summary-only (recursion-equivalent) scan misses the in-string raw token — the "
        "full-payload-string serialize is the load-bearing single method"
    )


# === AC-3 / AC-1-prose / AC-5: the SKILL.md prose contract (greps) ===


def _comment_stripped_lines(path):
    """Yield the SKILL.md lines with fenced-code/comment-only lines stripped (the no-fork grep base).

    The no-fork probe targets EXECUTABLE control flow, not a descriptive prose mention. A Markdown
    skill carries no Python comments, but a code FENCE may legitimately show a call-sequence
    snippet; this strips lines whose stripped form starts with `#` (a Markdown heading or a
    comment) so a heading naming `safety_passed` descriptively does not false-RED. The probe then
    asserts the EXECUTABLE expressions (`while True:` + the gate expression) are absent on the
    surviving lines.
    """
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            continue
        yield raw_line


def test_skill_md_no_forked_loop():
    # AC-3 (no-fork at the skill level): a comment-stripped grep over SKILL.md finds 0 copies of
    # the EXECUTABLE safety-loop control flow — a `while True:` loop HEADER and the
    # `disposition.get("safety_passed") is True` gate EXPRESSION at a non-comment line (target the
    # executable EXPRESSION, not a bare `safety_passed` token, so a descriptive prose mention does
    # not false-RED). The skill drives the ONE shared driver; the loop lives in `plan_driver.py`.
    lines = list(_comment_stripped_lines(SKILL_MD))
    forked_loop_headers = [ln for ln in lines if "while True:" in ln]
    assert forked_loop_headers == [], (
        f"SKILL.md re-hosts a `while True:` safety loop (the A-naive fork): {forked_loop_headers}"
    )
    forked_gate_exprs = [
        ln for ln in lines if 'disposition.get("safety_passed") is True' in ln
    ]
    assert forked_gate_exprs == [], (
        f"SKILL.md re-hosts the safety-gate EXPRESSION (the forked loop): {forked_gate_exprs}"
    )


def test_no_fork_grep_has_teeth():
    # AC-3 (the grep has TEETH): the comment-stripped grep DOES find the executable expressions
    # when they are present on a non-comment line — proving `test_skill_md_no_forked_loop` is not a
    # tautology that would pass on any input. A synthetic forked-loop snippet at a non-comment line
    # is caught; the same snippet as a `#`-prefixed comment line is correctly ignored.
    forked = [
        "    while True:",
        '        if disposition.get("safety_passed") is True:',
    ]
    commented = [
        "# while True:",
        '# if disposition.get("safety_passed") is True:',
    ]
    # the executable lines ARE caught (non-comment)
    assert any("while True:" in ln for ln in forked if not ln.strip().startswith("#"))
    assert any(
        'disposition.get("safety_passed") is True' in ln
        for ln in forked if not ln.strip().startswith("#")
    )
    # the same snippet as a comment is correctly skipped (no false-RED on a descriptive mention)
    assert all(ln.strip().startswith("#") for ln in commented)


def _names_summarize_as_deid_in(line):
    """True when `line` POSITIVELY names `router.summarize` as the A′ de-id-IN / operator-state source.

    The phase-scoped predicate the AC-1 prose grep + its teeth-proof share. A line POSITIVELY names
    the role when it mentions a de-id-IN / "operator-state source" phrase AND does NOT negate it (an
    "is NOT" disambiguation) and is NOT the persisted-side store-read-gate survivor sentence — those
    last two are the REQUIRED disambiguation, not a violation.
    """
    lowered = line.lower()
    names_role = (
        "operator-state source" in lowered
        or "de-id in" in lowered
        or "de-id-in" in lowered
        or "0-raw-pii token state" in lowered
    )
    if not names_role:
        return False
    # the REQUIRED disambiguation negates the role / names the persisted-side survivor — not a violation
    disambiguates = (
        "is not the" in lowered
        or "not the a′ de-id" in lowered
        or "persisted-side" in lowered
        or "store-read gate" in lowered
    )
    return not disambiguates


def test_skill_prose_names_deid_in_path():
    # AC-1 (prose half, PHASE-scoped): SKILL.md names the `deid_in` / `ModelClient.deidentify`
    # de-id-IN path AND 0 surviving `router.summarize` reference NAMES it as the A′ de-id-IN /
    # operator-state source. The grep is PHASE-scoped, NOT a whole-file `router.summarize`-absent
    # count: `router.summarize` LEGITIMATELY survives elsewhere named as the persisted-side
    # store-read gate (per deid_in.py:11-14) — that surviving mention is REQUIRED to stand,
    # disambiguated as NOT the A′ operator-state source.
    text = SKILL_MD.read_text(encoding="utf-8")

    # (a) the A′ de-id-IN path is named
    assert "ModelClient.deidentify" in text, "SKILL.md does not name the ModelClient.deidentify de-id-IN"
    assert "deid_in" in text, "SKILL.md does not name the deid_in de-id-IN boundary"

    # (b) no `router.summarize` is named as the A′ de-id-IN / operator-state source — scan every
    # line mentioning `router.summarize`; none may POSITIVELY name it as a de-id-IN / "operator-state
    # source" (the two superseded refs at the old [:48] / [:61] are removed/replaced). A line that
    # NEGATES the role ("`router.summarize` is NOT the A′ de-id-IN") or names the persisted-side
    # store-read gate is the REQUIRED disambiguation, not a violation.
    for line in text.splitlines():
        if "router.summarize" not in line:
            continue
        if _names_summarize_as_deid_in(line):
            raise AssertionError(
                f"SKILL.md still names `router.summarize` as the A′ de-id-IN/operator-state source: {line!r}"
            )

    # (c) the disambiguation sentence is PRESENT: `router.summarize` survives ONLY as the
    # persisted-side store-read gate, NOT the A′ operator-state source.
    lowered_text = text.lower()
    assert "persisted-side" in lowered_text and "store-read gate" in lowered_text, (
        "SKILL.md is missing the `router.summarize` persisted-side store-read-gate disambiguation"
    )


def test_skill_prose_documents_s94_deferral():
    # AC-5 (S94-deferral documented): SKILL.md documents that the LIVE subscription dispatch over
    # real agents is the S94 operator-present attestation (NOT a mock-test target) — so what IS vs
    # ISN'T mock-testable is explicit. A grep for the S94-deferral note.
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "S94" in text, "SKILL.md does not document the S94 deferral of the live dispatch"
    lowered = text.lower()
    assert "live" in lowered and ("attestation" in lowered or "operator-present" in lowered), (
        "SKILL.md does not document the live subscription dispatch as the S94 operator-present "
        "attestation (what IS vs ISN'T mock-testable must be explicit)"
    )


# === AC-1 prose disambiguation grep teeth (non-tautology for the persisted-side check) ===


def test_skill_prose_grep_distinguishes_deid_in_from_persisted_summarize():
    # AC-1 (the phase-scoped grep has TEETH): a synthetic SKILL-prose fragment that named
    # `router.summarize` as the operator-state source MUST trip the de-id-IN check, while a
    # fragment naming it as the persisted-side store-read gate MUST pass — proving the grep
    # distinguishes the superseded A′ de-id-IN role from the legitimate persisted-side survivor.
    superseded = "The author's ONLY operator-state source is `router.summarize(store_read)`."
    legitimate = "`router.summarize` survives ONLY as the persisted-side store-read gate."
    disambiguation = "`router.summarize` is NOT the A′ de-id-IN / operator-state source."

    assert _names_summarize_as_deid_in(superseded), (
        "the grep must catch the superseded operator-state-source ref"
    )
    assert not _names_summarize_as_deid_in(legitimate), (
        "the grep must not flag the persisted-side survivor"
    )
    assert not _names_summarize_as_deid_in(disambiguation), (
        "the grep must not flag the required disambiguation sentence (it NEGATES the role)"
    )


# ===============================================================================
# ADR-0028-T4 Cycle 1: the NEW value-scan over the DERIVED GATE / ADJUDICATOR /
# REAUTHOR yield payloads at the harness boundary (the crown jewel)
# ===============================================================================
#
# The FIRST-EVER scan over the engine-DERIVED yield payloads (the assembled plan /
# the safety finding / the re-author constraint). The AUTHOR seam is structurally
# clean (the orchestrator holds only the de-identified summary), so AUTHOR is not
# scanned; the derived payloads' PII-freeness is transitive-but-unverified, so the
# harness value-scans each one with `pii_scan.scan_text_full` (the same utility the
# `deid_in` boundary uses) BEFORE it leaves the process, failing CLOSED on a hit.


def _drive_collecting_requests(drive_kwargs, *, authors_map, reauthor=None, adjudicator=None):
    """Drive a run to completion through repeated `plan_step.step`, collecting each yielded request.

    Mirrors `test_plan_step._run_through_step` but RETAINS each surfaced pending request so a test
    can scan the DERIVED yield payloads. The ONLY state across iterations is the serialized state +
    the just-fulfilled envelope — no held generator.

    Returns:
        (list) The yielded `Request`s surfaced to the consumer (in order).
        (dict) The terminal serialized state (read its result via `plan_step.result_of`).
    """
    requests = []
    pending, state = plan_step.step(None, **drive_kwargs)
    envelope = None
    while pending is not None:
        requests.append(pending)
        envelope = _fulfil(pending, authors_map=authors_map, reauthor=reauthor, adjudicator=adjudicator)
        pending, state = plan_step.step(state, fulfilled_envelope=envelope, **drive_kwargs)
    return requests, state


def test_no_raw_pii_in_any_derived_yield_payload(tmp_path):
    # AC-2 (the crown jewel, 0 raw-PII over the DERIVED payloads): drive a bounce + held-finding
    # fixture run through the harness; the GATE assembled-plan (payload[0]) + the ADJUDICATOR safety
    # finding (payload) + the REAUTHOR constraint (payload) yield payloads each scan 0 raw-PII against
    # an identity config matching the synthetic name/lab tokens — the first-ever scan over those
    # DERIVED artifacts. And the run completes through the harness (the harness's INTERNAL value-scan
    # passed — it did NOT fail closed on a clean run).
    config = _identity_config(tmp_path)
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    drive_kwargs = dict(
        summary=_deid_summary(),
        domains=("workout", "nutrition", "supplements", "peptides"),
        store_read=store_read, root=tmp_path, plan_date=PLAN_DATE, gates={},
        gate_producer=_clean_composing_gate(),
        reauthor=_clearing_reauthor(), adjudicator=_clearing_liaison(),
        identity_config=config,
    )

    requests, state = _drive_collecting_requests(
        drive_kwargs, authors_map=_replay_safety_authors(),
        reauthor=_clearing_reauthor(), adjudicator=_clearing_liaison(),
    )

    # all three DERIVED yield kinds actually surfaced (else the scan is vacuous)
    kinds = {r.kind for r in requests}
    assert plan_driver.GATE in kinds, "no GATE yield surfaced (the scan would be vacuous)"
    assert plan_driver.REAUTHOR in kinds, "no REAUTHOR yield surfaced (the bounce did not fire)"
    assert plan_driver.ADJUDICATOR in kinds, "no ADJUDICATOR yield surfaced (no held finding fired)"

    # each DERIVED payload scans 0 raw-PII — GATE scoped to payload[0] (the assembled plan); the
    # REAUTHOR constraint + the ADJUDICATOR finding scanned whole (the carried Architect doc action).
    for r in requests:
        if r.kind == plan_driver.GATE:
            assert pii_scan.scan_text_full(str(r.payload[0]), token_config=config) == 0, (
                "the GATE assembled-plan yield payload carried raw-PII"
            )
        elif r.kind in (plan_driver.REAUTHOR, plan_driver.ADJUDICATOR):
            assert pii_scan.scan_text_full(str(r.payload), token_config=config) == 0, (
                f"a {r.kind} yield payload carried raw-PII"
            )

    # the run completed through the harness (the harness's own value-scan did NOT fail closed)
    result = plan_step.result_of(state)
    assert result is not None, "the harness run did not complete"
    assert result.get("reason") != plan_step.YIELD_PAYLOAD_PII, "a clean run wrongly failed closed"


def test_value_scan_helper_reds_on_a_planted_leak():
    # AC-3 (RED-capability, DEMONSTRATED not assumed): the harness value-scan returns >=1 on a
    # planted-leak DERIVED payload and 0 on a clean one. GATE is scoped to payload[0] (the assembled
    # plan); payload[1] (the `gate_producer` callable) is EXCLUDED — it str()s to an inert
    # `<function ...>` repr, scoped out explicitly so a future producer closing over operator-derived
    # data is not silently included AND so the scan targets the actual derived-PII surface (the
    # carried Architect doc action). REAUTHOR / ADJUDICATOR payloads are scanned whole.
    producer = lambda assembled_plan: {}  # an inert raw-verdict producer

    clean_gate = plan_driver.Request(plan_driver.GATE, ({"plan": "Goblet squat 3x8"}, producer))
    leak_gate = plan_driver.Request(plan_driver.GATE, ({"plan": f"note {_LEAK_EMAIL}"}, producer))
    assert plan_step._scan_yield_payload(clean_gate, pii_scan.DEFAULT_IDENTITY_CONFIG) == 0
    assert plan_step._scan_yield_payload(leak_gate, pii_scan.DEFAULT_IDENTITY_CONFIG) >= 1, (
        "the value-scan did not catch a planted leak in the GATE assembled-plan payload"
    )

    # the gate_producer CALLABLE (payload[1]) is NOT scanned even when its repr would carry a token
    producer_closing_over_leak = lambda assembled_plan: _LEAK_EMAIL
    producer_gate = plan_driver.Request(
        plan_driver.GATE, ({"plan": "clean"}, producer_closing_over_leak)
    )
    assert plan_step._scan_yield_payload(producer_gate, pii_scan.DEFAULT_IDENTITY_CONFIG) == 0, (
        "the scan must be scoped to payload[0]; the gate_producer callable is not scanned"
    )

    # REAUTHOR / ADJUDICATOR payloads are scanned WHOLE (they ARE the derived artifact)
    leak_reauthor = plan_driver.Request(
        plan_driver.REAUTHOR, ("workout", {"note": _LEAK_EMAIL})
    )
    leak_adjudicator = plan_driver.Request(
        plan_driver.ADJUDICATOR, ({"finding_id": _LEAK_EMAIL, "held_domain": "supplements"},)
    )
    assert plan_step._scan_yield_payload(leak_reauthor, pii_scan.DEFAULT_IDENTITY_CONFIG) >= 1
    assert plan_step._scan_yield_payload(leak_adjudicator, pii_scan.DEFAULT_IDENTITY_CONFIG) >= 1

    # the AUTHOR seam is structurally clean — it is NOT scanned (the de-identified summary only)
    author_with_token = plan_driver.Request(
        plan_driver.AUTHOR, (("workout",), {"x": _LEAK_EMAIL}, {})
    )
    assert plan_step._scan_yield_payload(author_with_token, pii_scan.DEFAULT_IDENTITY_CONFIG) == 0


def test_dated_derived_plan_is_not_flagged_as_pii():
    # contracts-1 (core-capability regression fix): a model-authored plan legitimately carries
    # SCHEDULE dates (deload weeks, retest cadences, check-in dates). The frozen GATE scan of the
    # DERIVED assembled plan does NOT opt into the DOB class (it is OPT-IN, default off — see the
    # pii_scan _VALUE_PII_PATTERNS note), so a schedule date here is NOT a DOB leak; the operator's
    # real DOB is age-banded upstream and never reaches this derived artifact. Had the DOB class
    # defaulted ON (the original-PR shape), these dates would score >0 -> YIELD_PAYLOAD_PII -> NO
    # plan (the core capability). RED-capable: flipping scan_text_full's include_dob default back
    # to True makes these dates score >0 and this assertion reds.
    producer = lambda assembled_plan: {}
    dated_plan = {
        "workout": "Deload the week of 2026-07-14; retest lipids by 2026-09-01.",
        "check_in": "next review 08/15/2026",
    }
    dated_gate = plan_driver.Request(plan_driver.GATE, (dated_plan, producer))
    assert plan_step._scan_yield_payload(dated_gate, pii_scan.DEFAULT_IDENTITY_CONFIG) == 0, (
        "a legitimately-dated derived plan must NOT be flagged as raw PII (contracts-1)"
    )
    # the opt-out narrows the DOB date class ONLY — the base contact/identifier classes stay live,
    # so a REAL operator contact leaking into the derived plan STILL fails closed.
    leak_reauthor = plan_driver.Request(plan_driver.REAUTHOR, ("workout", {"note": _LEAK_EMAIL}))
    assert plan_step._scan_yield_payload(leak_reauthor, pii_scan.DEFAULT_IDENTITY_CONFIG) >= 1, (
        "include_dob=False must not disable the base contact classes on the derived-plan scan"
    )


def test_value_scan_fails_closed_on_planted_leak(tmp_path):
    # AC-3 (the INTEGRATED fail-closed through the harness): a planted raw-PII token (a contact token)
    # in a workout author surfaces in the assembled plan (the GATE payload[0]); the harness value-scan
    # catches it and FAILS CLOSED — the GATE request is NEVER surfaced to the consumer (the payload
    # does not leave the process), the harness halts to the fail-closed sentinel, and 0 plan rows
    # promote into the real root.
    store_read = _seed_store(tmp_path)
    contaminated = {
        # the contact token rides in the exercise name -> it surfaces verbatim in the assembled plan
        "workout": _recon(_author(_workout_rec(f"Goblet squat {_LEAK_EMAIL}", 3)), energy_cost_kcal=500),
        "nutrition": _sustaining_authors()["nutrition"],
    }
    drive_kwargs = dict(
        summary=_deid_summary(), domains=("workout", "nutrition"), store_read=store_read,
        root=tmp_path, plan_date=PLAN_DATE, gates={}, gate_producer=_clean_composing_gate(),
    )

    requests, state = _drive_collecting_requests(drive_kwargs, authors_map=contaminated)

    # the harness FAILED CLOSED on the planted leak (the derived GATE payload did not leave the process)
    result = plan_step.result_of(state)
    assert result == {"deidentified": False, "reason": plan_step.YIELD_PAYLOAD_PII}, (
        f"the harness did not fail closed on the planted leak: {result}"
    )
    # NO GATE request carrying the leaked payload was ever surfaced to the consumer
    assert all(r.kind != plan_driver.GATE for r in requests), (
        "a contaminated GATE payload leaked past the harness scan to the consumer"
    )
    # and 0 plan rows promoted into the real root (the fail-closed surface)
    assert store.read("plan::workout", root=tmp_path) == [], "a plan promoted past the failed-closed scan"


# ===============================================================================
# ADR-0028-T4 Cycle 2: the skill-drives-via-`plan_step.py` glue — 0 synchronous
# agent calls inside `drive` (every dispatch is a yielded-request fulfilment)
# ===============================================================================


def _stack_checked(fn):
    """Wrap a dispatch hook so it records whether it was invoked synchronously from inside `drive`.

    When the CONSUMER fulfils a yielded request, the `drive` generator is SUSPENDED (paused at a
    yield), so its frame is NOT on the active call stack — a dispatch that fires with `drive` /
    `_run_with_replay` / `_drive_to_next` on the stack would be a SYNCHRONOUS agent call inside the
    driver's frame (the control-inversion the harness exists to prevent). The wrapper records the
    total call count + how many fired with a driver frame on the stack.
    """
    drive_frames = {"drive", "_run_with_replay", "_drive_to_next", "_send_round"}
    record = {"calls": 0, "inside_drive": 0}

    def wrapper(*args, **kwargs):
        stack_fns = {fr.function for fr in inspect.stack()}
        if stack_fns & drive_frames:
            record["inside_drive"] += 1
        record["calls"] += 1
        return fn(*args, **kwargs)

    wrapper.record = record
    return wrapper


def test_zero_synchronous_agent_calls_inside_drive(tmp_path):
    # AC-5: drive de-id -> AUTHOR -> GATE -> (REAUTHOR/ADJUDICATOR replay) -> (revise) -> promote
    # through the harness over a bounce + held-finding fixture; the count of SYNCHRONOUS
    # judge/lens/reauthor/adjudicator agent calls INSIDE `drive`'s frame is 0 — every dispatch is the
    # CONSUMER's fulfilment of a yielded request (the driver is SUSPENDED at the yield when the
    # dispatch fires). A spy records every dispatch's call-stack origin; a dispatch with a driver
    # frame on the stack -> RED. The harness inverts every agent-touching dispatch into a yield.
    store_read = _bpmh_store(tmp_path, "bleeding-risk")
    gate_spy = _stack_checked(_clean_composing_gate())
    reauthor_spy = _stack_checked(_clearing_reauthor())
    adjudicator_spy = _stack_checked(_clearing_liaison())
    drive_kwargs = dict(
        summary=_deid_summary(),
        domains=("workout", "nutrition", "supplements", "peptides"),
        store_read=store_read, root=tmp_path, plan_date=PLAN_DATE, gates={},
        gate_producer=gate_spy,
        # the drive-side reauthor/adjudicator are truthiness-only (they WIRE the engine memo hooks);
        # the real dispatch is the CONSUMER's spy below — the harness never calls these directly.
        reauthor=_clearing_reauthor(), adjudicator=_clearing_liaison(),
    )

    result = _run_through_step(
        drive_kwargs, authors_map=_replay_safety_authors(),
        reauthor=reauthor_spy, adjudicator=adjudicator_spy,
    )

    # the run promoted >=1 plan (the bounce + held finding cleared) — else the assertions are vacuous
    recorded = [d for d, r in result["results"].items() if r.get("recorded") is True]
    assert recorded, "the harness did not drive the fixtures to a promoted plan"
    # every dispatch fired (the spies are non-vacuous)
    assert gate_spy.record["calls"] >= 1, "the GATE producer never fired"
    assert reauthor_spy.record["calls"] >= 1, "the bounce reauthor never fired (the spy is vacuous)"
    assert adjudicator_spy.record["calls"] >= 1, "the adjudicator never fired (the spy is vacuous)"
    # and NONE fired synchronously inside `drive`'s frame (0 synchronous agent calls inside drive)
    assert gate_spy.record["inside_drive"] == 0, "a GATE dispatch fired synchronously inside drive"
    assert reauthor_spy.record["inside_drive"] == 0, "a REAUTHOR dispatch fired synchronously inside drive"
    assert adjudicator_spy.record["inside_drive"] == 0, "an ADJUDICATOR dispatch fired synchronously inside drive"


# ===============================================================================
# ADR-0028-T4 Cycle 3: the SKILL.md prose reconcile — drives via `plan_step.py`,
# no-fork-at-skill (loop OR release), the S94 live-subscription-dispatch deferral
# ===============================================================================


def test_skill_prose_drives_via_plan_step():
    # AC-1: SKILL.md Phase 2 drives the shared driver THROUGH the `plan_step.py` step-harness (not a
    # direct in-session `plan_driver.drive` generator), and documents the per-class subscription-
    # dispatch fulfilment: the skill fulfils each yielded typed request (AUTHOR / GATE / REAUTHOR /
    # ADJUDICATOR) via a SUBSCRIPTION agent dispatch and re-calls the harness with the appended
    # envelope. A SKILL.md that still drives `plan_driver.drive` directly (no `plan_step` reference,
    # no per-round harness loop) -> RED.
    text = SKILL_MD.read_text(encoding="utf-8")

    # the harness is named as the drive mechanism (the per-round `step`)
    assert "plan_step" in text, "SKILL.md does not name plan_step as the drive mechanism"
    assert "plan_step.step" in text, "SKILL.md does not name plan_step.step (the per-round drive entry)"
    # the four yielded typed-request kinds' fulfilment is documented
    for kind in ("AUTHOR", "GATE", "REAUTHOR", "ADJUDICATOR"):
        assert kind in text, f"SKILL.md does not document fulfilling the {kind} yielded request"
    # the per-round re-call is documented (fulfil a yield via a subscription dispatch, re-call the harness)
    lowered = text.lower()
    assert "subscription" in lowered, "SKILL.md does not document the subscription-dispatch fulfilment"
    assert "envelope" in lowered, "SKILL.md does not document re-calling the harness with the fulfilled envelope"


def test_skill_md_no_forked_loop_or_release():
    # AC-6 (no-fork at the skill — loop OR release): a comment-stripped grep over SKILL.md finds 0
    # copies of the EXECUTABLE safety-loop control flow (a `while True:` header, the
    # `disposition.get("safety_passed") is True` gate EXPRESSION at a non-comment line) AND 0
    # re-derivations of the adjudication release (`outcome == "cleared"`). The skill DRIVES the ONE
    # driver via the harness; the loop + the composition + the release stay in the inner engine. The
    # probe targets executable control flow (not a bare token a descriptive prose mention carries),
    # stripping comments/prose before counting (ADR-0026-T1 QA-2 / ADR-0028-T3 AC-5 discipline).
    lines = list(_comment_stripped_lines(SKILL_MD))

    forked_loop_headers = [ln for ln in lines if "while True:" in ln]
    assert forked_loop_headers == [], f"SKILL.md re-hosts a `while True:` safety loop: {forked_loop_headers}"

    forked_gate_exprs = [ln for ln in lines if 'disposition.get("safety_passed") is True' in ln]
    assert forked_gate_exprs == [], f"SKILL.md re-hosts the safety-gate EXPRESSION: {forked_gate_exprs}"

    rederived_release = [
        ln for ln in lines if 'outcome == "cleared"' in ln or "outcome == 'cleared'" in ln
    ]
    assert rederived_release == [], (
        f"SKILL.md re-derives the adjudication release (`outcome == cleared`): {rederived_release}"
    )


def test_skill_prose_documents_s94_live_deferral():
    # AC-7 (MOCK/FIXTURE-tested + S94 noted): SKILL.md documents that the LIVE subscription dispatch
    # (the skill dispatching REAL agents per round, real key, real spend) is the operator-present S94
    # attestation, NOT a mock-test target — so what IS vs ISN'T mock-testable is explicit. The glue
    # test's fixture construction (the glue drives a fixture dispatch, never a real agent) is the
    # mock-tested half.
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "S94" in text, "SKILL.md does not document the S94 deferral of the live dispatch"
    lowered = text.lower()
    assert "live" in lowered and ("attestation" in lowered or "operator-present" in lowered), (
        "SKILL.md does not document the live subscription dispatch as the S94 operator-present "
        "attestation (what IS vs ISN'T mock-testable must be explicit)"
    )
    assert "subscription" in lowered, "SKILL.md does not name the live subscription dispatch"
