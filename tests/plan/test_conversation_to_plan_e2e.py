"""Headline E2E: a served-`/chat` conversation -> a USABLE plan (ADR-0029-T5; PF-S87-01).

This binds the already-built SPA-served path into ONE end-to-end proof (it wires no
production code): a FIXTURE conversation drives the REAL served POST `/chat` turns
(`build_server(0,...)` + the loopback `_post_chat` pattern, the same one `tests/serve/
test_chat.py` uses) -> `persist_capture` -> `router.summarize` -> the wired programmatic
author path (`generate_plan`/`compute_plan`) -> `assemble` -> `record_plan` -> the rendered
dashboard. The model is a FIXTURE/MOCK injected at the ADR-0015 `ModelClient(backend=...)`
seam (scripted `converse` turns + a scripted `author` envelope), so the whole proof is
deterministic, CI-runnable, no network, no key, 0 live spend.

The two LOAD-BEARING properties (PF-S87-01 / the no-tautology headline):

  (a) The headline asserts a USABLE plan, NOT the honest no-plan state: `recorded == True`
      (`recorded = result["plan"] is not None`, `scripts/plan/generate_plan.py:445`), >=1
      domain plan recorded, AND content-traceability — a specific DE-IDENTIFIED value the
      fixture conversation supplied (the operator's free-text goal, which `summarize` passes
      through, `router.py:629`) appears in the rendered plan. NEVER merely "a plan object is
      non-None" (that passes on a fabricated/empty plan — tautological). The mock `author`
      backend personalizes from the de-identified summary it is handed, so the plan content
      is a genuine FUNCTION of the conversation: if the goal did not flow conversation ->
      store -> summarize -> author -> plan, the headline goes RED.

  (b) The negative control proves the headline is FAILING-CAPABLE, not constant-pass: the
      SAME pipeline + the SAME author backend driven with a no-usable-facts (empty/declined)
      conversation observes `recorded == False` (the honest no-plan state) — proving the
      `recorded == True` assertion goes the other way when there is no usable plan.

The LIVE run (real conversation -> real plan via the runtime keychain key) is the operator-
present finish line, carried here as an opt-in + key-gated `skipif` variant referencing
`scripts/model/keychain-setup.md` — explicitly NOT a CI gate (collected + skipped without the
opt-in/key; the CI run uses the mock).
"""

import datetime
import functools
import http.client
import json
import os
import threading
from pathlib import Path

import pytest

from scripts.generate import generate
from scripts.guard import pii_scan
from scripts.model.client import ModelClient
from scripts.plan.generate_plan import generate_plan
from scripts.plan.router import summarize
from scripts.serve import server as serve_server
from scripts.store import store

# A distinctive, escape-safe DE-IDENTIFIED value the fixture conversation supplies as the
# operator's free-text goal (`goal-targets` is a free-text wired token `summarize` passes
# through PII-free). It is the content-traceability anchor: it must appear in the rendered
# plan, having flowed conversation -> store -> summarize -> author -> plan -> render.
GOAL = "return to a 150 kg back squat by autumn 2026"

# An IDENTIFIABLE raw value seeded through a `/chat` turn for the post-conversation PII scan
# (AC-5). `pii_scan`'s value classes catch a dotted-domain email, so the capture gate routes
# it RECORD-ONLY to the gitignored scaffold; it must never survive into a store token or the
# de-identified summary.
EMAIL = "jane.smith.athlete@example.com"

PLAN_DATE = "2026-06-18"

# The operator-present opt-in for the LIVE variant (AC-4). Double-gated on the key AND this
# explicit opt-in so a normal `pytest -q` on the OPERATOR's own machine (where
# ANTHROPIC_API_KEY is routinely exported, per the S90 directive) does NOT make real spend —
# the live real-conversation run is a deliberate operator action, never an accidental one.
_LIVE_OPT_IN = bool(os.environ.get("APLUS_RUN_LIVE")) and bool(os.environ.get("ANTHROPIC_API_KEY"))


class _ConverseBackend:
    """A scripted `converse` backend: a configurable reply + extraction proposal per turn.

    Mutate `reply`/`extraction` between turns (the `tests/serve/test_chat.py` pattern) to
    script what each served `/chat` turn lands. The extraction is the `{token: value}` the
    capture gate routes by data class.
    """

    def __init__(self):
        self.reply = "noted"
        self.extraction = {}

    def converse(self, messages):
        return {"reply": self.reply, "extraction": dict(self.extraction)}


class _AuthorBackend:
    """A scripted `author` backend that personalizes from the de-identified summary.

    A faithful stand-in for the real plan-author specialist: it reasons over the
    de-identified `summary` it is handed (never a hardcoded constant). With the operator's
    goal present it authors a workout recommendation whose `detail` REFERENCES that
    de-identified value (the content-traceability anchor); with no goal (an empty/declined
    conversation) it returns the thin-library sentinel — the honest no-plan state. This is
    what makes the headline non-tautological AND the negative control work through the SAME
    backend: the envelope is a genuine function of the conversation-derived summary.
    """

    def author(self, domain, summary):
        goal = summary.get("goal-targets")
        if not goal:
            return {"thin_library": True, "specialist": "personal-trainer"}
        return {
            "specialist": "personal-trainer",
            "recommendations": [
                {
                    "claim": "rebuild a movement base with goblet squats before any loaded pattern",
                    "source": "ACSM resistance-training guidelines 2024",
                    "confidence_tier": "established",
                    "reversibility": "fully reversible on discontinuation",
                    "category": "training",
                    "payload": {
                        "name": "Goblet squat",
                        "sets": 3,
                        "reps": "8-12",
                        "detail": f"progress toward your goal: {goal}",
                    },
                },
            ],
        }


@pytest.fixture(autouse=True)
def _no_live_api(request, monkeypatch):
    """0-live-spend guard: any live key resolution fails the test loudly (AC-3).

    Patches `key_source.resolve` to raise, so every mock test in this module proves
    0 live calls BY CONSTRUCTION — the live backend can never resolve a key here. The
    operator-gated `live` variant is exempt (it makes a real call by design).
    """
    if "live" in request.node.name:
        return
    import scripts.model.key_source as key_source

    def _forbidden(*args, **kwargs):
        raise AssertionError(
            "live key_source.resolve() called — the E2E must be mock-only (0 live spend)"
        )

    monkeypatch.setattr(key_source, "resolve", _forbidden)


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _post_chat(port, payload):
    """POST a JSON `/chat` turn body; return (status, parsed response)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request(
        "POST", "/chat", body=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, json.loads(text)


def _run_served_conversation(tmp_path, turns):
    """Drive `turns` through the REAL served `/chat` over a loopback server + a mock client.

    Builds the server over tmp `store_root`/`scaffold_root`/`dna_root` and a mock converse
    client (the ADR-0015 seam), drives each turn (mutating the backend's scripted extraction
    per turn), tears the server down, and returns the instance-bound store-read surface +
    the tmp roots. The E2E never touches the real store/scaffold and never makes a live call.

    Args:
        tmp_path (Path): The pytest tmp root for the instance.
        turns (list[dict]): Each `{"turn", "covered_domains", "extraction"}` — the operator
            text, the chat domains touched, and the model's scripted extraction proposal.

    Returns:
        (Callable) `store_read` pre-bound to the tmp store root.
        (Path) The tmp store root.
        (Path) The tmp scaffold root.
        (list) The per-turn capture receipts (what actually landed).
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    backend = _ConverseBackend()
    srv = serve_server.build_server(
        0, store_root=store_root, dna_root=tmp_path / "dna",
        scaffold_root=scaffold_root, client=ModelClient(backend=backend),
    )
    port = srv.server_address[1]
    _serve_in_thread(srv)
    receipts = []
    try:
        for turn in turns:
            backend.extraction = turn["extraction"]
            status, resp = _post_chat(
                port, {"turn": turn["turn"], "conversation": [],
                       "covered_domains": turn["covered_domains"]},
            )
            assert status == 200, f"served /chat turn failed: {turn['turn']!r}"
            receipts.append(resp["receipt"])
    finally:
        srv.shutdown()
        srv.server_close()
    store_read = functools.partial(store.read, root=store_root)
    return store_read, store_root, scaffold_root, receipts


# A rich conversation that lands the distinctive goal (goals domain) + a training fact
# (training domain) through the served path — the chat-sourced rich domains the plan
# personalizes from.
_RICH_TURNS = [
    {"turn": "my goal is to return to a 150 kg back squat by autumn",
     "covered_domains": ["goals"], "extraction": {"goal-targets": GOAL}},
    {"turn": "recovery has been moderate lately",
     "covered_domains": ["training"], "extraction": {"recovery-status-band": "moderate"}},
]


def test_conversation_to_usable_plan_headline(tmp_path):
    """AC-1 (HEADLINE, NON-TAUTOLOGICAL): a served conversation -> a USABLE recorded plan.

    Drives the rich fixture conversation through the REAL served `/chat`, derives the
    de-identified `summarize`, then runs the wired author path (`generate_plan`, mock author
    at the ADR-0015 seam). Asserts (a) `recorded == True` (a plan WAS recorded — NOT the
    honest no-plan state), (b) >=1 exercise recorded, and (c) content-traceability: the
    de-identified goal value the conversation supplied appears BOTH in the recorded plan AND
    in the rendered dashboard. This is failing-capable per the negative control below — it
    goes RED if the end-to-end produces `recorded == False` instead of a usable plan.
    """
    store_read, store_root, _, receipts = _run_served_conversation(tmp_path, _RICH_TURNS)
    # The served path actually landed the chat-sourced tokens (the receipts are not vacuous).
    assert receipts[0]["store"] == ["goal-targets"]
    assert receipts[1]["store"] == ["recovery-status-band"]

    summary = summarize(store_read)
    # The de-identified summary carries the chat-sourced rich-domain tokens the plan
    # personalizes from — including the goal value (passed through PII-free, router.py:629).
    assert summary.get("goal-targets") == GOAL
    assert "recovery-status-band" in summary

    result = generate_plan(
        "workout", None, store_read, store_root,
        plan_date=PLAN_DATE, gates={"clearance_granted": False},
        client=ModelClient(backend=_AuthorBackend()),
    )

    # (a) a USABLE plan was recorded — NOT the honest no-plan state.
    assert result["recorded"] is True, f"no usable plan recorded (reason={result['reason']})"
    assert result["plan"] is not None
    # (b) >=1 domain plan recorded + rendered from the chat-extracted facts.
    assert len(result["plan"]["exercises"]) >= 1
    # The un-cleared load prescription is dropped (the asymmetric-downside clearance gate) —
    # the plan ships as deferred coaching, never an un-cleared load.
    assert all("load" not in ex for ex in result["plan"]["exercises"])

    # (c) content-traceability: the de-identified value the CONVERSATION supplied traces into
    # the recorded plan content. NOT a tautological non-None check — this de-identified value
    # originated in the served `/chat` turn and flowed the whole path.
    plan_detail = result["plan"]["exercises"][0].get("detail", "")
    assert GOAL in plan_detail, "the conversation-supplied goal did not trace into the plan"

    # ...and into the RENDERED plan (the dashboard the operator actually sees today).
    out = generate.run(
        "dashboard", _root=store_root, _out_dir=tmp_path,
        _today=datetime.date.fromisoformat(PLAN_DATE),
    )
    dashboard_html = out.read_text(encoding="utf-8")
    assert GOAL in dashboard_html, "the conversation-supplied goal did not render in the plan"


def test_empty_conversation_yields_honest_no_plan_state(tmp_path):
    """AC-2 (FAILING-CAPABLE NEGATIVE CONTROL): the SAME pipeline, no usable facts -> no plan.

    Drives an empty/declined conversation (a turn that lands nothing) through the SAME served
    `/chat` -> `summarize` -> the SAME `_AuthorBackend` -> `generate_plan`. With no goal in
    the summary, the faithful author returns the thin-library sentinel and the pipeline
    records NOTHING — `recorded == False`, the honest no-plan state. This proves AC-1's
    `recorded == True` headline is failing-capable (it would go RED here), distinguishing a
    usable plan from the no-plan state. The ONLY difference from AC-1 is the conversation.
    """
    empty_turns = [
        {"turn": "I'd rather not get into specifics right now",
         "covered_domains": ["goals"], "extraction": {}},
    ]
    store_read, store_root, _, receipts = _run_served_conversation(tmp_path, empty_turns)
    # The empty turn landed nothing — there are no usable facts to plan from.
    assert receipts[0]["store"] == []
    summary = summarize(store_read)
    assert "goal-targets" not in summary

    result = generate_plan(
        "workout", None, store_read, store_root,
        plan_date=PLAN_DATE, gates={"clearance_granted": False},
        client=ModelClient(backend=_AuthorBackend()),
    )

    # The honest no-plan state — NOT a usable plan. AC-1 asserts the opposite for the rich
    # conversation, so the headline assertion is not constant-pass.
    assert result["recorded"] is False
    assert result["plan"] is None


def test_mock_tested_no_live_api_no_network(tmp_path):
    """AC-3 (mock-tested, 0 live spend): the headline path runs with no key, no network.

    The autouse `_no_live_api` guard makes `key_source.resolve` raise, so this whole
    conversation -> usable-plan run completing proves it makes 0 live `key_source.resolve()`-
    gated call — the model is the FIXTURE/MOCK injected at the ADR-0015 seam. A structural
    assertion confirms the mock-backend injection and that the test imports no live SDK path.
    """
    store_read, store_root, _, _ = _run_served_conversation(tmp_path, _RICH_TURNS)
    result = generate_plan(
        "workout", None, store_read, store_root,
        plan_date=PLAN_DATE, gates={"clearance_granted": False},
        client=ModelClient(backend=_AuthorBackend()),
    )
    assert result["recorded"] is True  # completed under the resolve-raising guard => 0 live call

    src = Path(__file__).read_text(encoding="utf-8")
    assert "ModelClient(backend=" in src, "the E2E must inject the mock at the ADR-0015 seam"
    # Needle built from parts so this assertion's own literal cannot self-match the source.
    sdk = "anthropic"
    assert f"import {sdk}" not in src and f"from {sdk}" not in src, (
        "the E2E must import no live model-SDK call path"
    )


def test_post_conversation_pii_zero_leak(tmp_path):
    """AC-5 (CROWN-JEWEL PII 0-leak): a raw value seeded in a `/chat` turn does not survive.

    Seeds an IDENTIFIABLE raw email through a served `/chat` turn (under a free-text token),
    then asserts a post-conversation `pii_scan` over the store + the `summarize` output finds
    0 raw operator PII — the de-identification held end-to-end. The email IS captured to the
    gitignored scaffold (the honest record-only route, proving the seed actually flowed
    through the conversation), and is NOT present in any store token or the summary.
    """
    pii_turns = _RICH_TURNS + [
        {"turn": f"by the way reach me at {EMAIL}",
         "covered_domains": ["goals"],
         "extraction": {"hard-limits": f"no overhead pressing; reach me at {EMAIL}"}},
    ]
    store_read, store_root, scaffold_root, receipts = _run_served_conversation(tmp_path, pii_turns)
    # The PII-laden free-text routed RECORD-ONLY (the capture gate caught the email past the
    # model-bound token); the store receipt for that turn is empty.
    assert receipts[-1]["store"] == []
    assert receipts[-1]["scaffold"] == ["hard-limits"]

    summary = summarize(store_read)
    summary_text = json.dumps(summary, default=str)

    # The raw email did NOT survive into the de-identified side.
    assert EMAIL not in summary_text
    store_files = [str(p) for p in store_root.rglob("*") if p.is_file()]
    assert not any(EMAIL in Path(p).read_text(encoding="utf-8") for p in store_files)

    # pii_scan count over the store + the summary == 0 (the de-identification held). The
    # fixture store lines are synthetic by construction, so the structural net is off (bead
    # dv3) and only the value/identity classes run — exactly the raw-PII classes AC-5 guards.
    assert pii_scan.scan(store_files, include_structural=False) == 0
    assert pii_scan.scan_text_full(summary_text) == 0

    # ...but the email WAS captured to the gitignored operator record (the honest route),
    # proving the seed reached the conversation surface and the boundary actively re-routed it.
    scaffold_text = "".join(
        p.read_text(encoding="utf-8") for p in scaffold_root.rglob("*") if p.is_file()
    )
    assert EMAIL in scaffold_text


def test_live_variant_is_present_and_gated():
    """AC-4 (the live variant is present + skipped without the opt-in/key — NOT a CI gate).

    Asserts the operator-gated live variant carries a `skipif` gate whose condition is truthy
    in this (keyless / opt-out) env (so it is collected + skipped here, never run in CI), and
    whose reason references the `keychain-setup.md` runbook. The CI run uses the mock.
    """
    marks = [
        m for m in getattr(test_live_conversation_to_plan_operator_gated, "pytestmark", [])
        if m.name == "skipif"
    ]
    assert marks, "the live variant must carry a skipif gate"
    assert any(m.args and m.args[0] for m in marks), (
        "the live variant must be skipped in this keyless/opt-out env"
    )
    assert any("keychain-setup.md" in str(m.kwargs.get("reason", "")) for m in marks), (
        "the live variant's skip reason must reference the keychain-setup runbook"
    )


@pytest.mark.skipif(
    not _LIVE_OPT_IN,
    reason=(
        "operator-gated live variant (real conversation -> live converse via the runtime "
        "keychain key): set APLUS_RUN_LIVE=1 with ANTHROPIC_API_KEY exported "
        "(see scripts/model/keychain-setup.md). NOT a CI gate — the CI run uses the mock."
    ),
)
def test_live_conversation_to_plan_operator_gated(tmp_path):
    """AC-4 LIVE (operator-present finish line): a real served `/chat` turn via the live API.

    The build's FINAL operator-present checkpoint. Exercises the WIRED live `converse` leg
    end-to-end through the served `/chat` (a real no-train API call resolved via the runtime
    keychain key) and asserts a real assistant reply comes back. The real-plan author leg is
    the documented next operator-present step (the live `author` backend is wired by
    ADR-0015-T3); CI exercises the full conversation -> usable-plan path against the mock
    above. Double-gated on APLUS_RUN_LIVE + the key so a normal operator `pytest -q` (key
    exported per the S90 directive) never makes accidental spend.
    """
    store_root = tmp_path / "store"
    srv = serve_server.build_server(
        0, store_root=store_root, dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold",  # client=None -> the live ModelClient (no-train)
    )
    port = srv.server_address[1]
    _serve_in_thread(srv)
    try:
        status, resp = _post_chat(
            port, {"turn": "I'm returning to training after a layoff; where do I start?",
                   "conversation": [], "covered_domains": ["training"]},
        )
        assert status == 200
        assert resp.get("degraded") is not True, f"the live converse turn degraded: {resp}"
        assert resp.get("reply"), "the live converse turn returned no assistant reply"
    finally:
        srv.shutdown()
        srv.server_close()
