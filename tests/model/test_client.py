"""Tests for the single model boundary — the two-method client (ADR-0015-T1).

`scripts.model.client` is the system's FIRST programmatic model boundary: a swappable
no-train model client with a two-method public interface — `converse(...)` (one intake
turn: assistant reply text + a structured extraction proposal) and
`author(domain, summary)` (the plan-author envelope `assemble` consumes). These tests pin:

  - AC-1 (single model boundary): every model-client import lives ONLY inside
    `scripts/model/`; an `rg` over `scripts/` excluding the seam finds 0;
  - AC-2 (two-method over a MOCK backend): `converse` returns assistant text + an
    extraction proposal, `author` returns the contracted envelope — no live API, no key;
  - AC-3 (swap-clean seam): an injected alternate backend exercises both methods with 0
    caller-side edits, with a negative control proving the assertion is failing-capable;
  - AC-4 (fail-closed typed-raise): each failure mode (failed/empty/errored/timed-out)
    raises a TYPED failure and never returns a fabricated/partial payload, with a negative
    control proving the assertion is failing-capable.

The backend is always a fixture/mock (a fake object returning scripted fixtures); no test
hits a live API or reads a real key.
"""

import subprocess
import traceback

import pytest

from scripts.model.client import ModelCallError, ModelClient


# --- mock backends -------------------------------------------------------------


class _FixtureBackend:
    """A fake backend returning scripted fixtures — never a live API call.

    Attributes:
        converse_result: The fixture `converse` returns (or an Exception to raise).
        author_result: The fixture `author` returns (or an Exception to raise).
        deidentify_result: The fixture `deidentify` returns (or an Exception to raise).
    """

    def __init__(self, converse_result=None, author_result=None, deidentify_result=None):
        self.converse_result = converse_result
        self.author_result = author_result
        self.deidentify_result = deidentify_result

    def converse(self, messages):
        if isinstance(self.converse_result, Exception):
            raise self.converse_result
        return self.converse_result

    def author(self, domain, summary):
        if isinstance(self.author_result, Exception):
            raise self.author_result
        return self.author_result

    def deidentify(self, raw_intake):
        if isinstance(self.deidentify_result, Exception):
            raise self.deidentify_result
        return self.deidentify_result


def _good_converse_fixture():
    """A well-formed backend `converse` result: assistant reply + extraction proposal."""
    return {
        "reply": "How many days a week do you currently train?",
        "extraction": [
            {"field": "training-frequency", "value": "4 days/week", "confidence": "stated"}
        ],
    }


def _good_author_fixture(slug="personal-trainer"):
    """A well-formed backend `author` envelope, grounded against generate_plan.py:37."""
    return {
        "specialist": slug,
        "recommendations": [
            {
                "claim": "Train the squat pattern twice weekly.",
                "source": "wiki/strength-basics",
                "confidence_tier": "high",
                "reversibility": "fully reversible",
                "category": "movement",
                "payload": {"exercise": "back squat", "sets": 3, "reps": 5},
            }
        ],
    }


def _good_deid_summary_fixture():
    """A well-formed backend `deidentify` result: the de-identified summary mapping.

    Shaped from `router.SUMMARY_FIELD_SET` — de-identified band/class tokens only, never raw
    plan-intake PII (no legal name, no raw lab value). This is what the no-train de-id call
    emits from a raw intake.
    """
    return {
        "training-age-band": "10-15y",
        "sex-for-dosing": "male",
        "bodyweight-band": "80-90kg",
        "goal-domains": ["workout"],
        "recovery-status-band": "moderate",
    }


# --- AC-2: two-method boundary over a MOCK backend -----------------------------


def test_converse_returns_reply_and_extraction_over_mock_backend():
    """AC-2: `converse` returns assistant text + a structured extraction proposal."""
    client = ModelClient(backend=_FixtureBackend(converse_result=_good_converse_fixture()))

    result = client.converse([{"role": "user", "content": "I want to get stronger."}])

    assert isinstance(result["reply"], str) and result["reply"]
    assert isinstance(result["extraction"], list)
    assert result["extraction"][0]["field"] == "training-frequency"


def test_author_returns_contracted_envelope_over_mock_backend():
    """AC-2: `author` returns the `{specialist, recommendations}` envelope."""
    client = ModelClient(backend=_FixtureBackend(author_result=_good_author_fixture()))

    envelope = client.author("workout", {"training-frequency": "token-A"})

    assert envelope["specialist"] == "personal-trainer"
    assert isinstance(envelope["recommendations"], list)
    assert envelope["recommendations"][0]["claim"]


def test_author_passes_thin_library_sentinel_through():
    """AC-2: the thin-library sentinel envelope is a valid `author` return."""
    sentinel = {"thin_library": True, "specialist": "peptides"}
    client = ModelClient(backend=_FixtureBackend(author_result=sentinel))

    assert client.author("peptides", {"goal": "token-B"}) == sentinel


def test_deidentify_returns_summary_over_mock_backend():
    """`deidentify` returns the de-identified summary mapping over a MOCK backend.

    The de-id-IN seam (ADR-0020): raw plan-intake in, de-identified summary out — no live
    API, no key (the backend is a fixture). The result is the `SUMMARY_FIELD_SET`-shaped
    de-identified mapping the pipeline consumes.
    """
    summary = _good_deid_summary_fixture()
    client = ModelClient(backend=_FixtureBackend(deidentify_result=summary))

    result = client.deidentify({"legal-name": "Jordan Tester", "raw-lab-values": "ALT 88"})

    assert result == summary
    assert result["training-age-band"] == "10-15y"


# --- AC-1: single model boundary (the one import-point) ------------------------


def test_no_model_client_import_outside_the_seam():
    """AC-1: every model-client import lives ONLY inside `scripts/model/`."""
    result = subprocess.run(
        [
            "rg",
            "-n",
            r"anthropic|openai|\.messages\.create|httpx|requests",
            "scripts/",
            "--glob",
            "!scripts/model/**",
        ],
        capture_output=True,
        text=True,
    )
    # rg exit 1 == no matches (the boundary holds); exit 0 == a leak outside the seam.
    assert result.returncode == 1, (
        "model-client import leaked outside scripts/model/:\n" + result.stdout
    )


# --- AC-3: swap-clean seam (an injected alternate backend) ---------------------


class _AltBackend:
    """An ALTERNATE provider backend — a different object, same two-method shape.

    Proves the swap is a backend injection at the client's seam: no caller-side edit.
    """

    def converse(self, messages):
        return {"reply": "[alt-provider] noted.", "extraction": []}

    def author(self, domain, summary):
        return {"specialist": "alt-author", "recommendations": []}

    def deidentify(self, raw_intake):
        return {"goal-domains": ["workout"], "sex-for-dosing": "unspecified"}


def test_swap_to_alternate_backend_exercises_both_methods():
    """AC-3: an injected alternate backend serves all three methods (swap = injection)."""
    client = ModelClient(backend=_AltBackend())

    converse_out = client.converse([{"role": "user", "content": "hi"}])
    author_out = client.author("workout", {"goal": "token-C"})
    deid_out = client.deidentify({"legal-name": "Pat Sample"})

    assert converse_out["reply"] == "[alt-provider] noted."
    assert author_out["specialist"] == "alt-author"
    assert deid_out["goal-domains"] == ["workout"]


def test_swap_requires_no_caller_side_edit():
    """AC-3: swapping the provider edits 0 caller files (the seam is the only change).

    Negative-control note (documented per the recipe): a one-time hard-wire of the
    default backend (ignoring the injected seam parameter) was confirmed to FAIL the
    `test_swap_to_alternate_backend_exercises_both_methods` assertion (the alternate is
    not used), then reverted to the injectable seam so it passes. Asserting here that
    neither caller imports a provider SDK keeps the swap caller-free.
    """
    for caller in ("scripts/serve/chat.py", "scripts/plan/generate_plan.py"):
        result = subprocess.run(
            ["rg", "-n", r"anthropic|openai|httpx|requests", caller],
            capture_output=True,
            text=True,
        )
        # exit 1 (no match) OR exit 2 (file absent — chat.py is a later wave) both mean
        # the caller carries no provider import; exit 0 would mean a hard-wired provider.
        assert result.returncode != 0, (
            f"{caller} imports a provider SDK — the swap is not caller-free:\n"
            + result.stdout
        )


# --- AC-4: fail-closed typed-raise on every failure mode -----------------------


@pytest.mark.parametrize(
    "bad_result",
    [
        None,  # failed: backend returned nothing
        {},  # empty: backend returned an empty payload
        RuntimeError("backend errored"),  # errored: backend raised
        subprocess.TimeoutExpired(cmd="model", timeout=30),  # timed-out
    ],
    ids=["failed", "empty", "errored", "timed-out"],
)
def test_converse_raises_typed_on_every_failure_mode(bad_result):
    """AC-4: `converse` raises a TYPED failure on each failure mode."""
    client = ModelClient(backend=_FixtureBackend(converse_result=bad_result))

    with pytest.raises(ModelCallError):
        client.converse([{"role": "user", "content": "hi"}])


@pytest.mark.parametrize(
    "bad_result",
    [
        None,
        {},
        RuntimeError("backend errored"),
        subprocess.TimeoutExpired(cmd="model", timeout=30),
    ],
    ids=["failed", "empty", "errored", "timed-out"],
)
def test_author_raises_typed_on_every_failure_mode(bad_result):
    """AC-4: `author` raises a TYPED failure on each failure mode."""
    client = ModelClient(backend=_FixtureBackend(author_result=bad_result))

    with pytest.raises(ModelCallError):
        client.author("workout", {"goal": "token-D"})


@pytest.mark.parametrize(
    "bad_result",
    [
        None,  # failed: backend returned nothing
        {},  # empty: backend returned an empty payload
        "not-a-mapping",  # malformed: a non-mapping de-id result
        RuntimeError("backend errored"),  # errored: backend raised
        subprocess.TimeoutExpired(cmd="model", timeout=30),  # timed-out
    ],
    ids=["failed", "empty", "malformed", "errored", "timed-out"],
)
def test_deidentify_raises_typed_on_every_failure_mode(bad_result):
    """`deidentify` raises a TYPED failure on each failure mode (fail-closed de-id).

    An empty/malformed/errored de-id call must RAISE — never return a fabricated or partial
    summary that could be mistaken for a valid de-identified payload (the crown-jewel
    fail-closed contract `deid_in` depends on).
    """
    client = ModelClient(backend=_FixtureBackend(deidentify_result=bad_result))

    with pytest.raises(ModelCallError):
        client.deidentify({"legal-name": "Jordan Tester"})


def test_no_train_backend_deidentify_makes_no_live_call_without_the_sdk():
    """AC-9: an UNPATCHED de-id call never reaches a live API — the SDK is absent (0 spend).

    ADR-0027-T1 lit the live `deidentify`. Updated from the prior stub-pin: with the real
    `anthropic` SDK absent from `.venv` (the patch-driven posture), an UNPATCHED call hits the
    lazy `from anthropic import Anthropic` import and raises `ModuleNotFoundError` BEFORE any
    network request — the proof that no test path makes a live de-id call (0 live-API spend).
    The patched-SDK cases above inject a fake at the `_client` seam; this one leaves the seam
    unpatched to prove the absence is what blocks a live call.
    """
    import importlib.util

    from scripts.model.client import _ClaudeNoTrainBackend

    assert importlib.util.find_spec("anthropic") is None, (
        "the anthropic SDK is installed — the 0-live-spend precondition (AC-9) no longer holds"
    )
    with pytest.raises(ModuleNotFoundError):
        _ClaudeNoTrainBackend().deidentify({"legal-name": "Jordan Tester"})


def test_call_error_message_carries_no_raw_input(tmp_path):
    """SEC-01 / SEC-1: `_call`'s `ModelCallError` carries no raw input on str OR the cause chain.

    A backend whose raised exception message embeds a synthetic raw token must not surface that
    token on `str(ModelCallError)` (the message is a CONSTANT — `_call` does not interpolate
    `{exc!r}`) NOR through the `__cause__`/`__context__` chain a caller's `logger.exception()` /
    `traceback.print_exc()` would render. `_call` raises `from None`, INTENTIONALLY SUPPRESSING the
    chain at this PII/key boundary, so `__cause__` is `None` and the rendered traceback is raw-free.
    Scans the str surface (0 hits) AND asserts the chain is severed AND the full rendered traceback
    carries 0 occurrences of the token. A `_call` that interpolated the exception OR kept the
    `from exc` chain would carry the token and turn this RED.
    """
    from scripts.guard import pii_scan

    raw_token = "Jordan Faketestperson"
    config = tmp_path / "synthetic-identity.txt"
    config.write_text(raw_token + "\n")

    class _RawLeakingBackend:
        def deidentify(self, raw_intake):
            raise RuntimeError(f"backend blew up on {raw_token}")

    client = ModelClient(backend=_RawLeakingBackend())

    with pytest.raises(ModelCallError) as excinfo:
        client.deidentify({"legal-name": raw_token})

    e = excinfo.value
    assert e.__cause__ is None  # the chain is suppressed (`from None`) — no raw via __cause__
    assert pii_scan.scan_text(str(e), token_config=config) == 0  # str surface does NOT carry it
    assert raw_token not in str(e)
    tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    assert raw_token not in tb  # the fully-rendered traceback carries 0 occurrences


def test_failure_never_returns_a_fabricated_payload():
    """AC-4: on a failure mode the method RAISES — it never returns a partial payload.

    Negative-control note (documented per the recipe): a one-time change making the
    `empty` failure mode return a fabricated `{"reply": "...", "extraction": []}` was
    confirmed to FAIL this assertion (a payload came back instead of a raise), then
    reverted so the method raises typed. This proves the assertion is failing-capable.
    """
    client = ModelClient(backend=_FixtureBackend(converse_result={}))

    returned = None
    try:
        returned = client.converse([{"role": "user", "content": "hi"}])
    except ModelCallError:
        returned = "RAISED"
    assert returned == "RAISED", "a failure mode returned a payload instead of raising"


# --- ADR-0027-T1: the live no-train de-id backend (patched-SDK, 0 live spend) ------
#
# These cases exercise `_ClaudeNoTrainBackend.deidentify`'s LIVE call against a PATCHED
# anthropic SDK injected at the `_ClaudeNoTrainBackend._client` import site. The real SDK
# is absent from `.venv`, so the suite makes 0 live calls (AC-9). The fake records its
# `messages.create` call args and returns a canned `SUMMARY_FIELD_SET`-shaped envelope.

import json

from scripts.plan.router import SUMMARY_FIELD_SET


def _summary_envelope_text(summary):
    """An anthropic `messages.create` response carrying `summary` as a JSON text block.

    Mirrors the real envelope shape: `.content` is a list of content blocks, each with a
    `.type`; the de-id summary is the JSON body of the first `text` block — the same shape
    the live parse reads.
    """

    class _TextBlock:
        type = "text"

        def __init__(self, text):
            self.text = text

    class _Envelope:
        def __init__(self, blocks):
            self.content = blocks

    return _Envelope([_TextBlock(json.dumps(summary))])


class _FakeAnthropic:
    """A fake `anthropic.Anthropic` recording `messages.create` args, no live call.

    Constructed exactly as the real SDK is (`Anthropic(api_key=...)`); exposes a `messages`
    namespace whose `create(**kwargs)` records the kwargs and returns a scripted envelope
    (or raises a scripted exception). The whole point: the real package is never imported,
    so the absence proves the test is patch-driven (0 live spend).

    Attributes:
        calls: The list of `messages.create` kwargs captured across invocations.
    """

    def __init__(self, response_summary=None, raise_exc=None, raise_seq=None, api_key=None):
        self.api_key = api_key
        self.calls = []
        self._response_summary = response_summary
        self._raise_exc = raise_exc
        self._raise_seq = list(raise_seq) if raise_seq is not None else None

        fake = self

        class _Messages:
            def create(self, **kwargs):
                fake.calls.append(kwargs)
                if fake._raise_seq is not None:
                    exc = fake._raise_seq.pop(0)
                    if exc is not None:
                        raise exc
                elif fake._raise_exc is not None:
                    raise fake._raise_exc
                return _summary_envelope_text(fake._response_summary)

        self.messages = _Messages()

    def with_options(self, **kwargs):
        """Mirror the real SDK's per-request override (`timeout=`); returns a same-shape view.

        The real `Anthropic.with_options(timeout=...)` returns a configured client whose
        `.messages.create` behaves identically — the timeout knob does not alter the recorded
        call. The fake returns itself so the recorded `messages.create` args are unchanged.
        """
        return self


def _good_deid_summary():
    """A well-formed de-identified summary the patched SDK returns (band/class tokens only)."""
    return {
        "training-age-band": "born-1980s",
        "sex-for-dosing": "male",
        "bodyweight-band": "80-90kg",
        "goal-domains": "workout",
        "recovery-status-band": "moderate",
    }


def _patch_backend_client(monkeypatch, fake):
    """Patch `_ClaudeNoTrainBackend._client` to return `fake` — the SDK seam injection.

    Moves the existing backend-seam fixture posture one level down: instead of injecting a
    fixture BACKEND, the test injects a fake SDK at the lazy import site, so the live
    `deidentify` body runs against the fake `messages.create`.
    """
    from scripts.model.client import _ClaudeNoTrainBackend

    monkeypatch.setattr(_ClaudeNoTrainBackend, "_client", lambda self: fake)


# --- Cycle 1: the live de-id call ---------------------------------------------


def test_deidentify_live_returns_dict_and_prompt_carries_raw(monkeypatch):
    """AC-1: live `deidentify` returns a dict; the prompt carries the raw intake.

    With a patched SDK returning a `SUMMARY_FIELD_SET`-shaped envelope, the live call
    returns a `dict`, AND the raw-intake token reaches the captured `messages.create`
    prompt args (the model is given the raw intake to de-identify).
    """
    from scripts.model.client import _ClaudeNoTrainBackend

    fake = _FakeAnthropic(response_summary=_good_deid_summary())
    _patch_backend_client(monkeypatch, fake)

    raw_intake = {"legal-name": "Jordan Faketestperson", "raw-lab-values": "ALT 88"}
    result = _ClaudeNoTrainBackend().deidentify(raw_intake)

    assert isinstance(result, dict)
    assert len(fake.calls) == 1
    prompt_blob = json.dumps(fake.calls[0])
    assert "Jordan Faketestperson" in prompt_blob  # raw intake reached the model prompt


def test_deidentify_model_id_read_from_MODEL_attribute(monkeypatch):
    """AC-2: the call's `model=` is read off `MODEL` — swapping it needs 0 caller edits."""
    from scripts.model.client import _ClaudeNoTrainBackend

    fake = _FakeAnthropic(response_summary=_good_deid_summary())
    _patch_backend_client(monkeypatch, fake)
    monkeypatch.setattr(_ClaudeNoTrainBackend, "MODEL", "sentinel-model-xyz")

    _ClaudeNoTrainBackend().deidentify({"legal-name": "Pat Sample"})

    assert fake.calls[0]["model"] == "sentinel-model-xyz"


def test_deidentify_summary_keys_subset_of_field_set(monkeypatch):
    """AC-3: the parsed summary's keys are a subset of `SUMMARY_FIELD_SET`; `deid_in` passes."""
    from scripts.model.client import ModelClient, _ClaudeNoTrainBackend
    from scripts.plan.deid_in import DEID_CALL_FAILED, deid_in

    fake = _FakeAnthropic(response_summary=_good_deid_summary())
    _patch_backend_client(monkeypatch, fake)

    summary = _ClaudeNoTrainBackend().deidentify({"legal-name": "Pat Sample"})

    out_of_set = set(summary) - set(SUMMARY_FIELD_SET)
    assert out_of_set == set(), f"out-of-set keys leaked: {out_of_set}"

    surfaced = deid_in({"legal-name": "Pat Sample"}, ModelClient(backend=_ClaudeNoTrainBackend()))
    assert surfaced.get("reason") != DEID_CALL_FAILED
    assert set(surfaced) <= set(SUMMARY_FIELD_SET)


# --- Cycle 2: fail-closed family ----------------------------------------------


def test_deidentify_sdk_exception_fails_closed_to_sentinel(monkeypatch):
    """AC-4: an injected SDK exception → `ModelCallError` → `deid_in`'s DEID_CALL_FAILED.

    The fake's `messages.create` RAISES on every attempt; the live `deidentify` re-raises
    after the bound, the `_call` wrapper types it `ModelCallError`, and `deid_in` returns the
    honest no-plan sentinel — 0 fabricated/partial summaries past the boundary.
    """
    from scripts.model.client import ModelCallError, ModelClient, _ClaudeNoTrainBackend
    from scripts.plan.deid_in import DEID_CALL_FAILED, deid_in

    fake = _FakeAnthropic(raise_exc=RuntimeError("sdk blew up"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError):
        ModelClient(backend=_ClaudeNoTrainBackend()).deidentify({"legal-name": "Pat Sample"})

    surfaced = deid_in({"legal-name": "Pat Sample"}, ModelClient(backend=_ClaudeNoTrainBackend()))
    assert surfaced == {"deidentified": False, "reason": DEID_CALL_FAILED, "error_type": "ModelCallError"}


def test_deidentify_out_of_set_field_fails_closed(monkeypatch):
    """AC-5: a summary with a field OUTSIDE `SUMMARY_FIELD_SET` → `deid_in` DEID_CALL_FAILED.

    The model emits a band/class summary that smuggles an out-of-set key (a non-faithful
    de-id); `deid_in`'s whitelist rejects it — 0 out-of-set summaries surfaced.
    """
    from scripts.model.client import ModelClient, _ClaudeNoTrainBackend
    from scripts.plan.deid_in import DEID_CALL_FAILED, deid_in

    contaminated = dict(_good_deid_summary())
    contaminated["legal-name"] = "Jordan Faketestperson"  # an out-of-set raw-PII field
    fake = _FakeAnthropic(response_summary=contaminated)
    _patch_backend_client(monkeypatch, fake)

    surfaced = deid_in({"legal-name": "Jordan Faketestperson"},
                       ModelClient(backend=_ClaudeNoTrainBackend()))
    assert surfaced == {"deidentified": False, "reason": DEID_CALL_FAILED}


def test_deidentify_bounded_retry_then_succeed(monkeypatch):
    """AC-6 (succeed-within-bound): the Nth attempt succeeds → the call returns, invoked N times."""
    from scripts.model.client import _ClaudeNoTrainBackend

    # raise on the first N-1 attempts, succeed on the Nth (the success path through the loop).
    raise_seq = [RuntimeError("transient")] * 2 + [None]
    fake = _FakeAnthropic(response_summary=_good_deid_summary(), raise_seq=raise_seq)
    _patch_backend_client(monkeypatch, fake)

    result = _ClaudeNoTrainBackend().deidentify({"legal-name": "Pat Sample"})

    assert isinstance(result, dict)
    assert len(fake.calls) == 3  # invoked exactly the bound, succeeded on the last


def test_deidentify_bounded_retry_then_fail(monkeypatch):
    """AC-6 (exhaust-the-bound): all attempts raise → `ModelCallError` after EXACTLY the bound."""
    from scripts.model.client import (
        ModelCallError,
        _ClaudeNoTrainBackend,
        _DEID_MAX_ATTEMPTS,
    )

    fake = _FakeAnthropic(raise_exc=RuntimeError("always fails"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError):
        _ClaudeNoTrainBackend().deidentify({"legal-name": "Pat Sample"})

    assert len(fake.calls) == _DEID_MAX_ATTEMPTS  # exactly the bound — never unbounded


def test_deidentify_error_surface_carries_no_key_or_raw(monkeypatch, tmp_path):
    """SEC-4: the raised `ModelCallError` str + .args carry no synthetic key or raw-PII token.

    Seeds a synthetic key (patches `key_source.resolve`) + a synthetic raw-PII token, forces
    the failure path with a `messages.create` whose exception message EMBEDS both tokens, and
    asserts `str(exc)` and `exc.args` over the raised `ModelCallError` carry 0 occurrences of
    either — the SEC-01 constant-message `_call` lock holds. RED-capable: a variant
    interpolating `{exc!r}` into the message would leak the token and turn this RED.
    """
    from scripts.guard import pii_scan
    from scripts.model import key_source
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    raw_token = "Jordan Faketestperson"
    # Built at runtime so the source carries NO key-shaped literal (the tree-wide
    # `test_no_api_key_literal_in_tracked_tree` gate flags any `sk-ant-…` literal in the
    # PUBLIC repo). Still an opaque secret substring that must be absent from the error surface.
    key_token = "synthetic-no-train-key-token-DO-NOT-LOG"
    config = tmp_path / "synthetic-identity.txt"
    config.write_text(raw_token + "\n")
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: key_token)

    fake = _FakeAnthropic(raise_exc=RuntimeError(f"sdk error on {raw_token} with {key_token}"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError) as excinfo:
        _ClaudeNoTrainBackend().deidentify({"legal-name": raw_token})

    surface = str(excinfo.value) + repr(excinfo.value.args)
    assert raw_token not in surface
    assert key_token not in surface
    assert pii_scan.scan_text(str(excinfo.value), token_config=config) == 0


def test_deidentify_error_traceback_carries_no_key_or_raw(monkeypatch, tmp_path):
    """SEC-1: the RENDERED traceback (the `__cause__`/`__context__` chain) carries no key or raw token.

    The constant-message `str()`/`.args` surface (the SEC-4 test above) is raw-free regardless of
    the chain, BUT `raise ... from <sdk_exc>` would attach the raw SDK exception (carrying the raw
    intake in the request prompt + the resolved key) as `__cause__` — which a caller's
    `logger.exception()` / `traceback.print_exc()` / `exc_info=True` renders. Forces the failure
    path with an SDK exception EMBEDDING both tokens and asserts the fully-rendered traceback carries
    0 occurrences of either. RED-capable: reverting `from None` to `from last_exc` re-attaches the
    raw `__cause__` and turns this RED (verified against the old form before adopting `from None`).
    """
    from scripts.model import key_source
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    raw_token = "Jordan Faketestperson"
    key_token = "synthetic-no-train-key-token-DO-NOT-LOG"
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: key_token)

    fake = _FakeAnthropic(raise_exc=RuntimeError(f"sdk error on {raw_token} with {key_token}"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError) as excinfo:
        _ClaudeNoTrainBackend().deidentify({"legal-name": raw_token})

    e = excinfo.value
    tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    assert raw_token not in tb
    assert key_token not in tb


# --- Cycle 3: raw-intake-in-memory-only (tmp-tree scan WITH MUTATION) ----------


def _tmp_tree_token_hits(tmp_path, *tokens):
    """Count files under `tmp_path` whose bytes carry ANY of `tokens` (the on-disk rglob scan).

    A filesystem rglob over the whole tmp tree — NOT a `builtins.open` write-spy (which
    misses `os.write` / `pathlib.Path.write_text` / `tempfile` / SDK-internal write paths).
    Returns the count of files carrying either token; 0 means nothing leaked to disk.
    """
    hits = 0
    for path in tmp_path.rglob("*"):
        if not path.is_file():
            continue
        try:
            blob = path.read_text(errors="ignore")
        except OSError:
            continue
        if any(tok in blob for tok in tokens):
            hits += 1
    return hits


def test_deidentify_raw_intake_never_written_to_disk(monkeypatch, tmp_path):
    """AC-7 (clean): no file under the tmp HOME/CWD carries the raw-PII OR the synthetic key.

    Runs the live-wired backend over a synthetic raw-PII intake under an isolated tmp
    HOME/CWD; patches `key_source.resolve` to a synthetic key so the call resolves it, then
    rglobs the whole tmp tree for BOTH the raw token AND the key token → 0 files. The
    KEY-token leg (SEC-2) closes the gitignored-key-residue gap the diff-only grep misses.
    GREEN-on-oracle: the live method holds the raw intake in-memory only.
    """
    from scripts.model import key_source
    from scripts.model.client import _ClaudeNoTrainBackend

    import tempfile

    raw_token = "Jordan Faketestperson"
    key_token = "synthetic-no-train-key-token-DO-NOT-LOG"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    # Redirect tempfile + $TMPDIR/$TMP/$TEMP into the scanned tree too: a
    # `tempfile.NamedTemporaryFile()` write (no dir= -> $TMPDIR -> /var/folders on macOS) would
    # otherwise ESCAPE the rglob and read a false GREEN. The env vars alone do NOT redirect
    # `tempfile` (it memoizes `tempfile.tempdir` on first `gettempdir()`), so set `tempfile.tempdir`
    # directly (monkeypatch auto-restores it); the env vars cover subprocess / SDK-internal writes
    # that read $TMPDIR themselves. Any tempfile-targeted write now lands under `tmp_path`.
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    monkeypatch.setenv("TMPDIR", str(tmp_path))
    monkeypatch.setenv("TMP", str(tmp_path))
    monkeypatch.setenv("TEMP", str(tmp_path))
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: key_token)

    fake = _FakeAnthropic(response_summary=_good_deid_summary())
    _patch_backend_client(monkeypatch, fake)

    _ClaudeNoTrainBackend().deidentify({"legal-name": raw_token, "raw-lab-values": "ALT 88"})

    assert _tmp_tree_token_hits(tmp_path, raw_token, key_token) == 0


def test_deidentify_in_memory_scan_red_on_injected_write(monkeypatch, tmp_path):
    """AC-7 MUTATION: an injected mid-call `write_text(raw_intake)` makes the SAME scan find ≥1.

    Proves the scan is non-vacuous: a backend variant that deliberately writes the raw intake
    to a tmp file mid-call makes the rglob find ≥1 file — the scan DETECTS a real on-disk
    raw-PII write. This RED-capability is the lock; without it the clean GREEN is worthless.
    """
    import tempfile

    from scripts.model import key_source
    from scripts.model.client import _ClaudeNoTrainBackend, _deid_prompt

    raw_token = "Jordan Faketestperson"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    # Redirect tempfile + $TMPDIR/$TMP/$TEMP into the scanned tree (matches the clean test's fixture)
    # so the `tempfile.NamedTemporaryFile()` leak below (no dir= -> $TMPDIR) lands UNDER `tmp_path`.
    # `tempfile` memoizes `tempfile.tempdir` on first `gettempdir()`, so the env vars alone do NOT
    # redirect it — set `tempfile.tempdir` directly (monkeypatch auto-restores). This makes the
    # mutation leg exercise the $TMPDIR escape the clean test now guards against.
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    monkeypatch.setenv("TMPDIR", str(tmp_path))
    monkeypatch.setenv("TMP", str(tmp_path))
    monkeypatch.setenv("TEMP", str(tmp_path))
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: "synthetic-no-train-key-token-DO-NOT-LOG")

    fake = _FakeAnthropic(response_summary=_good_deid_summary())

    class _LeakingBackend(_ClaudeNoTrainBackend):
        def _client(self):
            # inject the leak via a $TMPDIR-targeted tempfile write (NO dir= -> resolves to the
            # redirected $TMPDIR == tmp_path), then behave normally. Proves the TMPDIR-redirected
            # scan catches a tempfile-targeted raw-PII write that a tmp_path-only rglob would miss.
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
                fh.write(_deid_prompt({"legal-name": raw_token}))
            return fake

    _LeakingBackend().deidentify({"legal-name": raw_token})

    # the SAME scan now finds the injected leak — the non-vacuous proof.
    assert _tmp_tree_token_hits(tmp_path, raw_token) >= 1


# --- Cycle 4: the crown-jewel raw-PII-leak probe ------------------------------


def test_deidentify_no_raw_pii_token_past_boundary(monkeypatch):
    """AC-8 (clean, crown-jewel): 0 raw tokens past the de-id boundary.

    Seeds a synthetic legal name + a synthetic lab value into the raw intake; the patched
    SDK returns a `SUMMARY_FIELD_SET`-shaped band/class summary (no raw tokens). Asserts the
    summary the backend returns AND the summary `deid_in` surfaces carry 0 of those raw
    tokens — count past the boundary = 0. GREEN-on-oracle: the live method returns only the
    parsed patched summary; the seed reaching the assertion proves the probe is wired.
    """
    from scripts.model.client import ModelClient, _ClaudeNoTrainBackend
    from scripts.plan.deid_in import deid_in

    raw_name = "Jordan Faketestperson"
    raw_lab = "ALT 88 AST 92"
    fake = _FakeAnthropic(response_summary=_good_deid_summary())
    _patch_backend_client(monkeypatch, fake)

    returned = _ClaudeNoTrainBackend().deidentify({"legal-name": raw_name, "raw-lab-values": raw_lab})
    surfaced = deid_in({"legal-name": raw_name, "raw-lab-values": raw_lab},
                       ModelClient(backend=_ClaudeNoTrainBackend()))

    returned_blob = json.dumps(returned)
    surfaced_blob = json.dumps(surfaced)
    for token in (raw_name, raw_lab, "Jordan", "88"):
        assert token not in returned_blob, f"raw token {token!r} leaked into the returned summary"
        assert token not in surfaced_blob, f"raw token {token!r} leaked into the deid_in summary"


def test_deidentify_leak_variant_probe_goes_red(monkeypatch):
    """AC-8 LEAK VARIANT: the clean probe's own assertion FAILS against a leaky SDK → RED-capable.

    Proves the crown-jewel probe is not vacuous: a non-faithful SDK that echoes the raw legal
    name into an IN-SET field value (so it survives `deid_in`'s key whitelist) pushes a raw
    token past the boundary. Re-running the CLEAN probe's exact 0-raw-token assertion over the
    leaky surfaced summary RAISES — the probe detects the leak. A probe that cannot go RED is
    worthless; this is the demonstration.
    """
    from scripts.model.client import ModelClient, _ClaudeNoTrainBackend
    from scripts.plan.deid_in import deid_in

    raw_name = "Jordan Faketestperson"
    leaky = {"sex-for-dosing": raw_name}  # the raw name echoed into an in-set field value
    fake = _FakeAnthropic(response_summary=leaky)
    _patch_backend_client(monkeypatch, fake)

    surfaced = deid_in({"legal-name": raw_name}, ModelClient(backend=_ClaudeNoTrainBackend()))

    # the in-set-key/raw-value summary passes the key whitelist, so the raw token IS surfaced —
    # the clean probe's 0-raw-token assertion fails here, which is the RED-capability proof.
    surfaced_blob = json.dumps(surfaced)
    probe_passes = raw_name not in surfaced_blob
    assert not probe_passes, "the leak variant did not surface the raw token — the probe is vacuous"
