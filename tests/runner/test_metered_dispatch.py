"""The metered specialist-author dispatch seam + the D2 crown-jewel wire-scan (ADR-0049-T1).

Drives `metered_dispatch.build_dispatch` — the metered-lane analog of
`subscription_dispatch.build_dispatch` — over recording fixture seams at $0: the recording SDK
fake REPLACES `_ClaudeNoTrainBackend._client()` (no `anthropic` import, no live call, no key
resolve), so the D2 outbound scan captures the bytes the model API actually receives at the TRUE
SDK boundary (`messages.create`), not the seam-inbound args. The tree carries 0 real operator PII —
the seeded "legal name" is the house synthetic `SYNTHETIC_NAME`, the store-content sentinel a
synthetic token.

  - AC-1: factory shape + the normalize wrap (a NON-normalizing recording client) + the retained
    subscription adapter + 0-side-effect module import;
  - AC-2 (isolation e2e): the metered loop path constructs no subscription session (a regression
    guard — 0 `default_session_factory` / `_spawn_subscription_session` calls; the positive
    metered-lane proof is AC-4);
  - AC-3: the `deid_in` sentinel halts to 0 metered dispatches (placement), a clean summary
    dispatches (the seam is live, not dead);
  - AC-4: the outbound captured AT `messages.create` crosses 0 raw-PII, 0 store-content, only the
    de-id summary (⊆ the imported `SUMMARY_FIELD_SET`), 0 store reads;
  - AC-5: the de-id egress guarantee holds identically across the metered<->subscription lane swap,
    and the three self-invalidation mutants (raw-append / store-read / store-content-append) each
    RED their assertion.
"""

import ast
import importlib
import json
from pathlib import Path

import pytest

from scripts.model.client import ModelClient
from scripts.plan import plan_orchestrator
from scripts.plan.dispatch_budget import DispatchBudget
from scripts.plan.plan_orchestrator import _dispatch_domains, run_orchestrated
from scripts.plan.router import SUMMARY_FIELD_SET
from scripts.runner import metered_dispatch, subscription_dispatch
from scripts.store import store

from tests.plan.test_deid_in import SYNTHETIC_NAME, _FixedDeidClient, _raw_intake
from tests.plan.test_plan_orchestrator import _deid_summary, _sustaining_authors

# The seeded raw-PII sentinels (both SYNTHETIC — 0 real operator PII on the tree). `LEGAL_NAME` is
# the house synthetic name a faithful de-id strips; `STORE_SENTINEL` stands in for store-content that
# must never reach a specialist payload.
LEGAL_NAME = SYNTHETIC_NAME
STORE_SENTINEL = "STORECONTENT-9f8e7d6c-sentinel"

_METERED_SOURCE = Path(__file__).resolve().parents[2] / "scripts" / "runner" / "metered_dispatch.py"


# --- the recording SDK fake: captures the TRUE messages.create egress, no anthropic import --------


class _TextBlock:
    """One `text` content block on a stand-in SDK response (duck-types `_parse_author_envelope`)."""

    type = "text"

    def __init__(self, text):
        self.text = text


class _AuthorResponse:
    """A stand-in SDK author response — `.content` is the block list `_parse_author_envelope` reads."""

    def __init__(self, content):
        self.content = content


def _parseable_author_response():
    """A minimal parseable author envelope response (empty recommendations — the payload is inert)."""
    payload = json.dumps({"specialist": "personal-trainer", "recommendations": []})
    return _AuthorResponse([_TextBlock(payload)])


class _RecordingMessages:
    """Records the `messages.create(**kwargs)` payload (`system` + `messages`) — the true egress."""

    def __init__(self, recorder):
        self._recorder = recorder

    def create(self, **kwargs):
        self._recorder["system"] = kwargs.get("system")
        self._recorder["messages"] = kwargs.get("messages")
        return _parseable_author_response()


class _RecordingSDK:
    """Stands in for the `anthropic.Anthropic` client `_ClaudeNoTrainBackend._client()` returns.

    Records the real `.with_options(timeout=...).messages.create(**kwargs)` egress. NO `anthropic`
    import — the fake IS the SDK, so the metered author path runs at $0 with no live call.
    """

    def __init__(self, recorder):
        self.messages = _RecordingMessages(recorder)

    def with_options(self, **kwargs):
        return self


def _recording_model_client(recorder):
    """A default-backend `ModelClient` whose SDK seam is REPLACED by the recording fake ($0)."""
    client = ModelClient()  # default `_ClaudeNoTrainBackend`; 0-spend at construct (lazy backend)
    client.backend._client = lambda: _RecordingSDK(recorder)  # replace the SDK seam — no live call
    return client


def _install_store_read_spy(monkeypatch):
    """Module-level spy over `store.read`/`read_all`/`items` — catches a store read via ANY handle."""
    counter = {"n": 0}

    def _spy(*args, **kwargs):
        counter["n"] += 1
        return []

    monkeypatch.setattr(store, "read", _spy)
    monkeypatch.setattr(store, "read_all", _spy)
    monkeypatch.setattr(store, "items", _spy)
    return counter


def _drive_metered(build_adapter, summary, monkeypatch, *, gates=None):
    """Drive `build_adapter`'s dispatch over the workout specialist through the real `_dispatch_domains`
    seam and return the recorded SDK egress + the store-read counter."""
    recorder = {}
    client = _recording_model_client(recorder)
    store_spy = _install_store_read_spy(monkeypatch)
    dispatch = build_adapter(client)
    _dispatch_domains(("workout",), summary, gates or {}, dispatch, DispatchBudget(cap=100))
    return recorder, store_spy


def _crossed_summary(recorder):
    """Parse the de-identified summary out of the recorded user-message content (the crossed bytes)."""
    content = recorder["messages"][0]["content"]
    return json.loads(content.split("\n", 1)[1])


def _assert_clean_metered_egress(recorder, store_spy):
    """The four D2 outbound sub-assertions over the RECORDED `messages.create` payload (the egress)."""
    serialized = json.dumps({"system": recorder.get("system"), "messages": recorder.get("messages")},
                            default=str)
    assert LEGAL_NAME not in serialized, "raw-PII (legal name) crossed to the SDK boundary"
    assert STORE_SENTINEL not in serialized, "store-content sentinel crossed to the SDK boundary"
    crossed = _crossed_summary(recorder)
    assert set(crossed) <= set(SUMMARY_FIELD_SET), (
        "operator-state field outside SUMMARY_FIELD_SET crossed to the SDK boundary")
    assert store_spy["n"] == 0, "the adapter performed a store read"


def _leaky_metered_adapter(mutator):
    """A metered-adapter factory whose dispatch mutates the outbound `context` before forwarding."""
    def build(client):
        base = metered_dispatch.build_dispatch(client)

        def dispatch(name, prompt, context):
            return base(name, prompt, mutator(context))

        return dispatch

    return build


# --- AC-1: factory shape + the normalize wrap + the retained adapter + 0-side-effect import -------


class _RawAuthorClient:
    """A NON-normalizing recording client: `.author` returns a raw envelope with a LIST-valued rec
    scalar field (unlike a real `ModelClient`, which already normalizes at its boundary) — so the
    metered normalize wrap is exercised non-vacuously (QA SHOULD-4)."""

    def __init__(self):
        self.calls = []

    def author(self, name, context):
        self.calls.append((name, context))
        return {"specialist": name, "recommendations": [{"claim": ["over", "the", "limit"]}]}


def test_ac1_factory_shape_forwards_context_and_normalizes():
    # AC-1: build_dispatch(client) returns dispatch(name, prompt, context) that routes the specialist
    # author over client.author(name, CONTEXT) — the pre-built prompt is discarded — and normalizes.
    client = _RawAuthorClient()
    dispatch = metered_dispatch.build_dispatch(client)
    env = dispatch("workout", "PRE-BUILT-PROMPT-should-be-discarded", {"goal-domains": "x"})
    # the adapter forwarded (name, context) — NOT the prompt — to client.author
    assert client.calls == [("workout", {"goal-domains": "x"})]
    # the normalize wrap coerced the list-valued `claim` to the composer's scalar shape
    claim = env["recommendations"][0]["claim"]
    assert isinstance(claim, str), "the metered normalize wrap must coerce a list rec field to a scalar"
    assert claim == "over the limit", "normalize joins a list claim with a single space (SEC-02)"


def test_ac1_retained_subscription_adapter_still_importable():
    # AC-1: the North-Star subscription adapter is untouched — still built + importable.
    import scripts.runner.subscription_dispatch as s

    assert callable(s.build_dispatch)


def test_ac1_module_import_fires_zero_side_effects(monkeypatch):
    # AC-1: importing the seam arms nothing — 0 key resolve (a canary over the metered key source).
    resolved = []
    monkeypatch.setattr("scripts.model.key_source.resolve", lambda *a, **k: resolved.append(1))
    importlib.reload(metered_dispatch)
    assert resolved == [], "importing metered_dispatch triggered a key resolve (non-zero side effect)"


# --- AC-2 (isolation e2e): the metered loop path constructs no subscription session --------------


class _CountingAuthorClient:
    """A metered-lane recording client wrapping a per-domain author set; counts `.author` calls."""

    def __init__(self, authors):
        self.authors = authors
        self.author_call_count = 0

    def author(self, name, context):
        self.author_call_count += 1
        return self.authors[name]


def test_ac2_metered_loop_constructs_no_subscription_session(tmp_path, monkeypatch):
    # AC-2 (regression guard, AR-003): an end-to-end run_orchestrated over the metered loop_dispatch +
    # a clean-summary deid completes a plan and NEVER constructs a subscription session — a forward
    # guard against a future run_orchestrated subscription fallback. NOT the positive lane proof
    # (AC-4 is); it is architecturally 0-by-default today — that is the guard's point.
    from tests.plan.test_generate_plan import _seed_store

    factory_calls = []
    monkeypatch.setattr(subscription_dispatch, "default_session_factory",
                        lambda *a, **k: factory_calls.append("factory"))
    monkeypatch.setattr(subscription_dispatch, "_spawn_subscription_session",
                        lambda *a, **k: factory_calls.append("spawn"))

    client = _CountingAuthorClient(_sustaining_authors())
    dispatch = metered_dispatch.build_dispatch(client)
    store_read = _seed_store(tmp_path)
    run_orchestrated(
        _raw_intake(), _FixedDeidClient(_deid_summary()), dispatch, store_read, tmp_path,
        plan_date="2026-07-16", domains=("workout", "nutrition"),
    )
    assert client.author_call_count > 0, "the metered loop path never dispatched (a dead seam)"
    assert factory_calls == [], "a subscription session factory was constructed on the metered loop path"


# --- AC-3: the deid_in sentinel halts to 0 metered dispatches; a clean summary dispatches ---------


class _SentinelDeidClient:
    """A de-id client that returns the honest-no-plan sentinel — no de-identified summary."""

    def __init__(self):
        self.calls = []

    def deidentify(self, raw_intake):
        self.calls.append(raw_intake)
        return {"deidentified": False}


class _SpyAuthorClient:
    """A metered client counting `.author` calls — 0 on the sentinel halt (AC-3 placement)."""

    def __init__(self):
        self.author_call_count = 0

    def author(self, name, context):
        self.author_call_count += 1
        return {"specialist": name, "recommendations": []}


def test_ac3_deid_sentinel_halts_to_zero_metered_dispatches(tmp_path):
    from tests.plan.test_generate_plan import _seed_store

    spy = _SpyAuthorClient()
    dispatch = metered_dispatch.build_dispatch(spy)
    store_read = _seed_store(tmp_path)
    result = run_orchestrated(
        _raw_intake(), _SentinelDeidClient(), dispatch, store_read, tmp_path,
        plan_date="2026-07-16", domains=("workout", "nutrition"),
    )
    # the deid_in gate halted BEFORE _dispatch_domains — 0 metered dispatches over a non-summary
    assert spy.author_call_count == 0, "the metered client was invoked on the de-id sentinel halt"
    assert result.get("deidentified") is False
    assert result.get("dispatch_count") == 0


def test_ac3_clean_summary_dispatches_the_metered_seam():
    # Falsifier: a clean summary → the metered seam IS invoked (proves the 0-count above is the
    # sentinel halt, not a dead seam).
    spy = _SpyAuthorClient()
    dispatch = metered_dispatch.build_dispatch(spy)
    _dispatch_domains(("workout", "nutrition"), _deid_summary(), {}, dispatch, DispatchBudget(cap=100))
    assert spy.author_call_count == 2, "the metered seam did not dispatch over a clean summary"


# --- AC-4: outbound captured AT the SDK boundary — 0 raw-PII, 0 store-content, ⊆ allowlist, 0 reads


def test_ac4_outbound_capture_at_sdk_boundary_is_clean(monkeypatch):
    # AC-4: the de-id strips the seeded raw-PII → the summary the adapter forwards is clean; captured
    # at the true SDK boundary (messages.create), the egress crosses 0 raw-PII, 0 store-content, only
    # the de-id summary (⊆ the IMPORTED SUMMARY_FIELD_SET), with 0 store reads.
    deid = _FixedDeidClient(_deid_summary())
    summary = deid.deidentify({"legal-name": LEGAL_NAME, "free-text": STORE_SENTINEL, **_raw_intake()})
    recorder, store_spy = _drive_metered(metered_dispatch.build_dispatch, summary, monkeypatch)
    _assert_clean_metered_egress(recorder, store_spy)
    # the only operator-state that crossed IS the de-id summary; the system prompt is PII-free
    assert _crossed_summary(recorder) == _deid_summary()


def test_ac4_falsifier_field_outside_allowlist_reds(monkeypatch):
    # Falsifier: a summary field OUTSIDE SUMMARY_FIELD_SET (a BENIGN value, so the raw-PII/store
    # checks pass and the ⊆ check is the one that REDs) → proves the assertion binds to the real
    # IMPORTED allowlist, not a copied literal.
    summary = {**_deid_summary(), "novel-field-outside-allowlist": "some-band"}
    recorder, store_spy = _drive_metered(metered_dispatch.build_dispatch, summary, monkeypatch)
    with pytest.raises(AssertionError, match="outside SUMMARY_FIELD_SET"):
        _assert_clean_metered_egress(recorder, store_spy)


def test_ac4_structural_no_scripts_store_import():
    # AC-4(d) structural half: metered_dispatch's IMPORTS reference no scripts.store symbol (the
    # primary 0-store-read guarantee; the module-level spy + mutant is the non-tautological backstop).
    # AST-inspected (not a substring scan — the module docstring names `scripts.store` in prose).
    tree = ast.parse(_METERED_SOURCE.read_text(encoding="utf-8"))
    package_parts = ["scripts", "runner"]  # metered_dispatch.py's containing package
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                imported.append(node.module or "")
            else:  # resolve a RELATIVE import to its absolute module (Sec Tier-2 LOW)
                anchor = package_parts[: len(package_parts) - (node.level - 1)]
                if node.module:
                    imported.append(".".join(anchor + [node.module]))
                else:  # bare `from .. import X` — each name is a submodule of the anchor
                    imported += [".".join(anchor + [alias.name]) for alias in node.names]
    store_imports = [m for m in imported if m == "scripts.store" or m.startswith("scripts.store.")]
    assert store_imports == [], f"metered_dispatch must import no scripts.store symbol: {store_imports}"


# --- AC-5: lane-swap invariance + the three-mutant self-invalidation gate ------------------------


class _RecordingSession:
    """A subscription session recording the FULL (name, prompt, context) it receives (AC-5 egress)."""

    def __init__(self):
        self.received = None

    def __call__(self, name, prompt, context):
        self.received = {"name": name, "prompt": prompt, "context": context}
        return {"specialist": name, "recommendations": []}


def _drive_subscription(summary, *, gates=None):
    """Drive the subscription adapter over the same seam and return the session's received egress."""
    session = _RecordingSession()
    _dispatch_domains(("workout",), summary, gates or {},
                      subscription_dispatch.build_dispatch(session), DispatchBudget(cap=100))
    return session


def _assert_clean_subscription_egress(session):
    """The subscription lane's egress carries 0 raw-PII, 0 store-content, operator-state ⊆ allowlist."""
    serialized = json.dumps(session.received, default=str)
    assert LEGAL_NAME not in serialized, "raw-PII crossed on the subscription lane"
    assert STORE_SENTINEL not in serialized, "store-content crossed on the subscription lane"
    assert set(session.received["context"]) <= set(SUMMARY_FIELD_SET), (
        "subscription operator-state outside SUMMARY_FIELD_SET")


def test_ac5_lane_swap_deid_guarantee_holds_identically(monkeypatch):
    # AC-5: scan EACH lane's egress (not the shared input). The invariant is the de-id guarantee
    # (0 raw-PII, 0 store-content, operator-state ⊆ SUMMARY_FIELD_SET) — NOT byte-identity: the
    # subscription lane's prompt embeds the role profile + gates and is far larger.
    deid = _FixedDeidClient(_deid_summary())
    summary = deid.deidentify({"legal-name": LEGAL_NAME, "free-text": STORE_SENTINEL})

    recorder, store_spy = _drive_metered(metered_dispatch.build_dispatch, summary, monkeypatch)
    _assert_clean_metered_egress(recorder, store_spy)

    session = _drive_subscription(summary)
    _assert_clean_subscription_egress(session)
    # the lanes are NOT byte-identical — the invariant is the de-id guarantee, not the byte count
    assert session.received["prompt"] != recorder["messages"][0]["content"]


def test_ac5_lane_swap_subscription_falsifier_reds():
    # In-suite RED-capability proof for the SUBSCRIPTION lane's egress scan (QA Tier-2 SHOULD-FIX;
    # AR-005 parity with the metered mutants — a negative assertion needs an in-suite falsifier, not
    # only out-of-band reasoning): a raw legal name injected under an allowlisted key into the summary
    # the subscription lane forwards → the subscription egress scan REDs.
    session = _drive_subscription({**_deid_summary(), "recovery-status-band": LEGAL_NAME})
    with pytest.raises(AssertionError, match="raw-PII crossed on the subscription lane"):
        _assert_clean_subscription_egress(session)


def test_ac5_lane_swap_falsifier_context_injection_reds(monkeypatch):
    # Falsifier: a lane-stub that injects a raw field into the forwarded context → the scan REDs.
    build = _leaky_metered_adapter(lambda ctx: {**ctx, "raw-legal-name": LEGAL_NAME})
    recorder, store_spy = _drive_metered(build, _deid_summary(), monkeypatch)
    with pytest.raises(AssertionError):
        _assert_clean_metered_egress(recorder, store_spy)


def test_ac5_mutation_gate_raw_pii_append(monkeypatch):
    # Mutant (a): append the legal name under an allowlisted key → the 0-raw-PII assertion REDs.
    build = _leaky_metered_adapter(lambda ctx: {**ctx, "recovery-status-band": LEGAL_NAME})
    recorder, store_spy = _drive_metered(build, _deid_summary(), monkeypatch)
    with pytest.raises(AssertionError, match="raw-PII"):
        _assert_clean_metered_egress(recorder, store_spy)


def test_ac5_mutation_gate_store_content_append(monkeypatch):
    # Mutant (c): append the store-content sentinel under an allowlisted key → the 0-store-content
    # assertion REDs (QA MUST-FIX-1 — the previously-missing store-content mutant).
    build = _leaky_metered_adapter(lambda ctx: {**ctx, "active-issue-class": STORE_SENTINEL})
    recorder, store_spy = _drive_metered(build, _deid_summary(), monkeypatch)
    with pytest.raises(AssertionError, match="store-content"):
        _assert_clean_metered_egress(recorder, store_spy)


def test_ac5_mutation_gate_store_read(monkeypatch):
    # Mutant (b): open a direct-import store read → the 0-store-read assertion REDs, caught by the
    # MODULE-LEVEL spy (proving the spy is load-bearing even against a direct-import read, Sec MEDIUM-2).
    def build(client):
        base = metered_dispatch.build_dispatch(client)

        def dispatch(name, prompt, context):
            store.read("plan::workout", root="/nonexistent")  # the spy intercepts — no real access
            return base(name, prompt, context)

        return dispatch

    recorder, store_spy = _drive_metered(build, _deid_summary(), monkeypatch)
    with pytest.raises(AssertionError, match="store read"):
        _assert_clean_metered_egress(recorder, store_spy)
