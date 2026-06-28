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
        extract_readings_result: The fixture `extract_readings` returns (or an Exception to raise).
    """

    def __init__(
        self,
        converse_result=None,
        author_result=None,
        deidentify_result=None,
        extract_readings_result=None,
    ):
        self.converse_result = converse_result
        self.author_result = author_result
        self.deidentify_result = deidentify_result
        self.extract_readings_result = extract_readings_result

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

    def extract_readings(self, file_content, media_type):
        if isinstance(self.extract_readings_result, Exception):
            raise self.extract_readings_result
        return self.extract_readings_result


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

    if importlib.util.find_spec("anthropic") is not None:
        pytest.skip(
            "anthropic SDK installed (operator live mode) — the absence-based 0-live-spend guard "
            "(AC-9) is N/A; the patched failure-mode tests cover the fail-closed paths"
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


# --- ADR-0029-T2: the live no-train converse backend (patched-SDK, 0 live spend) ---
#
# These cases exercise `_ClaudeNoTrainBackend.converse`'s LIVE call against a PATCHED
# anthropic SDK injected at the `_ClaudeNoTrainBackend._client` import site, mirroring the
# ADR-0027-T1 deid posture above. The real SDK is absent from `.venv`, so the suite makes 0
# live calls. The CONVERSE envelope is the converse analogue of `_summary_envelope_text`'s
# deid envelope: `_summary_envelope_text` is shape-agnostic (it JSON-dumps any dict into a
# `.content` text block), so passing a converse-shaped `{"reply", "extraction"}` fixture
# yields a converse-shaped envelope with no new builder — `_FakeAnthropic` is reused as-is.


def _good_converse_turn():
    """A well-formed converse turn the patched SDK returns: reply text + extraction proposal."""
    return {
        "reply": "How many days a week do you currently train?",
        "extraction": [
            {"field": "training-frequency", "value": "4 days/week", "confidence": "stated"}
        ],
    }


# --- Cycle 1: the live converse call ------------------------------------------


def test_converse_live_returns_reply_and_extraction(monkeypatch):
    """AC-1: live `converse` returns the contracted `{reply, extraction}` shape.

    With a patched SDK returning a converse-shaped envelope (injected at `_client`, no live
    API/key), the backend-direct call returns a dict whose `reply` is a non-empty str and
    whose `extraction` is a list, AND the same result passes the public `ModelClient.converse`
    validation ([:47-60]) without raising. The `NotImplementedError` stub is gone.
    """
    from scripts.model.client import ModelClient, _ClaudeNoTrainBackend

    fake = _FakeAnthropic(response_summary=_good_converse_turn())
    _patch_backend_client(monkeypatch, fake)
    messages = [{"role": "user", "content": "I want to get stronger."}]

    result = _ClaudeNoTrainBackend().converse(messages)

    assert isinstance(result["reply"], str) and result["reply"]
    assert isinstance(result["extraction"], list)

    public = ModelClient(backend=_ClaudeNoTrainBackend()).converse(messages)
    assert public == result  # the contracted shape passes the public validation


def test_converse_live_resolves_runtime_key_through_client(monkeypatch):
    """AC-2: the key is resolved at call time via `key_source.resolve` inside `_client`.

    Injects a fake `anthropic` module so the REAL `_client` runs (no `_patch_backend_client`
    here), patches `key_source.resolve` to a sentinel, and asserts the SDK `_client`
    constructs was handed THAT sentinel as its `api_key` — the key is read at call time
    through `key_source.resolve`, never a tracked file or a module-load capture. Driven
    end-to-end through `converse`.
    """
    import sys
    import types

    from scripts.model import key_source
    from scripts.model.client import _ClaudeNoTrainBackend

    sentinel_key = "sentinel-runtime-key-xyz"
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: sentinel_key)

    fake = _FakeAnthropic(response_summary=_good_converse_turn())
    captured = {}

    def _make(api_key=None):
        captured["api_key"] = api_key
        return fake

    fake_anthropic = types.ModuleType("anthropic")
    fake_anthropic.Anthropic = _make
    monkeypatch.setitem(sys.modules, "anthropic", fake_anthropic)

    _ClaudeNoTrainBackend().converse([{"role": "user", "content": "hi"}])

    assert captured["api_key"] == sentinel_key  # call-time key, no tracked-file read


def test_converse_live_bounded_retry_then_succeed(monkeypatch):
    """AC-4 (succeed-within-bound): the Nth attempt succeeds → the call returns, invoked N times."""
    from scripts.model.client import _ClaudeNoTrainBackend

    # raise on the first N-1 attempts, succeed on the Nth (the success path through the loop).
    raise_seq = [RuntimeError("transient")] * 2 + [None]
    fake = _FakeAnthropic(response_summary=_good_converse_turn(), raise_seq=raise_seq)
    _patch_backend_client(monkeypatch, fake)

    result = _ClaudeNoTrainBackend().converse([{"role": "user", "content": "hi"}])

    assert isinstance(result, dict)
    assert len(fake.calls) == 3  # invoked exactly the bound, succeeded on the last


def test_converse_live_bounded_retry_then_fail(monkeypatch):
    """AC-4 (exhaust-the-bound): all attempts raise → `ModelCallError` after EXACTLY the bound."""
    from scripts.model.client import (
        ModelCallError,
        _ClaudeNoTrainBackend,
        _CONVERSE_MAX_ATTEMPTS,
    )

    fake = _FakeAnthropic(raise_exc=RuntimeError("always fails"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError):
        _ClaudeNoTrainBackend().converse([{"role": "user", "content": "hi"}])

    assert len(fake.calls) == _CONVERSE_MAX_ATTEMPTS  # exactly the bound — never unbounded


def test_converse_live_makes_no_live_call_without_the_sdk():
    """AC-4 (0 live spend): an UNPATCHED converse call never reaches a live API — the SDK is absent.

    With the real `anthropic` SDK absent from `.venv` (the patch-driven posture), an UNPATCHED
    call hits the lazy `from anthropic import Anthropic` import and raises `ModuleNotFoundError`
    BEFORE any network request — the proof that no test path makes a live converse call (0
    live-API spend), mirroring the deid 0-spend pin.
    """
    import importlib.util

    from scripts.model.client import _ClaudeNoTrainBackend

    if importlib.util.find_spec("anthropic") is not None:
        pytest.skip(
            "anthropic SDK installed (operator live mode) — the absence-based 0-live-spend guard "
            "is N/A; the patched failure-mode tests cover the fail-closed paths"
        )
    with pytest.raises(ModuleNotFoundError):
        _ClaudeNoTrainBackend().converse([{"role": "user", "content": "hi"}])


# --- Cycle 2: the fail-closed / no-leak surface --------------------------------


@pytest.mark.parametrize(
    "fake_kwargs",
    [
        {"response_summary": None},  # failed: a null body
        {"response_summary": {}},  # empty: no reply/extraction
        {"response_summary": {"reply": "hi"}},  # malformed: missing extraction
        {"raise_exc": RuntimeError("sdk errored")},  # errored: the SDK raised
        {"raise_exc": subprocess.TimeoutExpired(cmd="model", timeout=30)},  # timed-out
    ],
    ids=["failed", "empty", "malformed", "errored", "timed-out"],
)
def test_converse_live_raises_typed_on_every_failure_mode(monkeypatch, fake_kwargs):
    """AC-3: live `converse` raises `ModelCallError` on every failure mode — 0 fabricated turns.

    Each failure mode injected at the patched SDK (a null / empty / malformed body, a raised
    exception, a timeout-style raise) makes the live `converse` exhaust the bound and raise the
    typed `ModelCallError` — never returning a fabricated or partial turn (the parse helper's
    shape gate rejects a truthy-but-malformed body; the public `ModelClient.converse` validation
    is the outer net). Mirrors the deid fail-closed family.

    RED-capable: against the Cycle-1-PRE `NotImplementedError` stub these errored; and a converse
    that returned a fabricated `{"reply": ..., "extraction": []}` on the empty mode (instead of
    raising) was confirmed to fail the `== "RAISED"` assertion, then reverted.
    """
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    fake = _FakeAnthropic(**fake_kwargs)
    _patch_backend_client(monkeypatch, fake)

    returned = None
    try:
        returned = _ClaudeNoTrainBackend().converse([{"role": "user", "content": "hi"}])
    except ModelCallError:
        returned = "RAISED"
    assert returned == "RAISED", "a failure mode returned a payload instead of raising"


def test_converse_error_surface_carries_no_key_or_raw(monkeypatch, tmp_path):
    """AC-3 (SEC): the raised `ModelCallError` str + .args carry no synthetic key or raw-PII token.

    Seeds a synthetic key (patches `key_source.resolve`) + a synthetic raw-PII token, forces the
    failure path with a `messages.create` whose exception message EMBEDS both tokens, and asserts
    `str(exc)` and `exc.args` over the raised `ModelCallError` carry 0 occurrences of either — the
    SEC-01 constant-message lock holds. RED-capable: a variant interpolating `{exc!r}` into the
    converse message would leak the token and turn this RED (confirmed by temporarily interpolating
    the SDK exception into the raise, observing the assertion fail, then reverting to the constant).
    """
    from scripts.guard import pii_scan
    from scripts.model import key_source
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    raw_token = "Jordan Faketestperson"
    key_token = "synthetic-no-train-key-token-DO-NOT-LOG"
    config = tmp_path / "synthetic-identity.txt"
    config.write_text(raw_token + "\n")
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: key_token)

    fake = _FakeAnthropic(raise_exc=RuntimeError(f"sdk error on {raw_token} with {key_token}"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError) as excinfo:
        _ClaudeNoTrainBackend().converse([{"role": "user", "content": raw_token}])

    surface = str(excinfo.value) + repr(excinfo.value.args)
    assert raw_token not in surface
    assert key_token not in surface
    assert pii_scan.scan_text(str(excinfo.value), token_config=config) == 0


def test_converse_error_traceback_carries_no_key_or_raw(monkeypatch, tmp_path):
    """AC-3 (SEC): the RENDERED traceback (`__cause__`/`__context__` chain) carries no key or raw token.

    `raise ... from <sdk_exc>` would attach the raw SDK exception (carrying the raw conversation in
    the request + the resolved key) as `__cause__` — which a caller's `logger.exception()` /
    `traceback.print_exc()` renders. Forces the failure path with an SDK exception EMBEDDING both
    tokens and asserts the fully-rendered traceback carries 0 occurrences of either AND
    `__cause__ is None` (the `from None` lock). RED-capable: reverting `from None` to `from <exc>`
    re-attaches the raw `__cause__` and turns this RED (confirmed by temporarily reverting the
    raise, observing the assertion fail, then restoring `from None`).
    """
    from scripts.model import key_source
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    raw_token = "Jordan Faketestperson"
    key_token = "synthetic-no-train-key-token-DO-NOT-LOG"
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: key_token)

    fake = _FakeAnthropic(raise_exc=RuntimeError(f"sdk error on {raw_token} with {key_token}"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError) as excinfo:
        _ClaudeNoTrainBackend().converse([{"role": "user", "content": raw_token}])

    e = excinfo.value
    assert e.__cause__ is None  # the chain is severed (`from None`)
    tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    assert raw_token not in tb
    assert key_token not in tb


# --- ADR-0030-T1: the no-train extract_readings method (mock/patched-SDK, 0 live spend) ---
#
# `ModelClient.extract_readings(file_content, media_type)` is the no-train extraction
# primitive: the uploaded file content + its media type in, a list of Line-Field-Set readings
# out. These cases pin it the way the deid/converse blocks pin their methods — the public
# fail-closed wrapper over a MOCK `_FixtureBackend` (Cycle 1), the live `_ClaudeNoTrainBackend`
# call against a PATCHED anthropic SDK (Cycle 2), and the SEC crown-jewel no-leak pair
# (Cycle 3). The real SDK may be present (operator live mode), so every case injects a fixture
# backend or a fake SDK at the `_client` seam — 0 live calls, 0 key, 0 network.

from scripts.store.keying import LINE_FIELDS


def _good_reading(item="HbA1c", value="5.4%"):
    """A well-formed Line-Field-Set reading (item, timepoint, source, value)."""
    return {"item": item, "timepoint": "2026-01-15", "source": "quest-labs", "value": value}


def _good_readings_list():
    """A well-formed readings list the backend/fixture returns — every reading conformant."""
    return [
        _good_reading("HbA1c", "5.4%"),
        _good_reading("ALT", "31 U/L"),
    ]


# --- Cycle 1: the public ModelClient.extract_readings fail-closed wrapper (MOCK backend) ---


def test_extract_readings_returns_line_field_set_list_over_mock_backend():
    """AC-1: `extract_readings` returns a list whose every reading carries the Line Field Set."""
    readings = _good_readings_list()
    client = ModelClient(backend=_FixtureBackend(extract_readings_result=readings))

    result = client.extract_readings(b"%PDF-1.4 ...", "application/pdf")

    assert isinstance(result, list) and result
    for reading in result:
        assert set(LINE_FIELDS) <= set(reading), f"reading missing a Line Field Set key: {reading}"


def test_extract_readings_non_list_return_fails_closed():
    """AC-1a: a non-`list` backend return raises `ModelCallError` (public fail-closed validation)."""
    client = ModelClient(backend=_FixtureBackend(extract_readings_result={"readings": "oops"}))

    with pytest.raises(ModelCallError):
        client.extract_readings(b"file", "text/csv")


def test_extract_readings_field_short_reading_fails_closed():
    """AC-1a: a list carrying ONE field-short reading (missing `value`) raises `ModelCallError`."""
    short = [{"item": "HbA1c", "timepoint": "2026-01-15", "source": "quest-labs"}]  # no `value`
    client = ModelClient(backend=_FixtureBackend(extract_readings_result=short))

    with pytest.raises(ModelCallError):
        client.extract_readings(b"file", "text/csv")


def test_extract_readings_returns_the_injected_parse_not_a_constant():
    """AC-2 (NON-TAUTOLOGICAL): fixture A → readings A, a DIFFERENT fixture B → readings B.

    Proves the method returns the injected backend parse, not a hardcoded constant: two
    different fixtures yield two different (and unequal) returns, each equal to its injection.
    """
    readings_a = [_good_reading("HbA1c", "5.4%")]
    readings_b = [_good_reading("Vitamin D", "42 ng/mL"), _good_reading("TSH", "2.1 mIU/L")]

    client_a = ModelClient(backend=_FixtureBackend(extract_readings_result=readings_a))
    client_b = ModelClient(backend=_FixtureBackend(extract_readings_result=readings_b))

    out_a = client_a.extract_readings(b"file-a", "application/pdf")
    out_b = client_b.extract_readings(b"file-b", "image/png")

    assert out_a == readings_a
    assert out_b == readings_b
    assert out_a != out_b  # the return tracks the fixture — not a constant


@pytest.mark.parametrize(
    "bad_result",
    [
        None,  # failed: backend returned nothing
        {},  # empty: backend returned an empty payload
        "not-a-list",  # malformed: a truthy non-list body
        RuntimeError("backend errored"),  # errored: backend raised
        subprocess.TimeoutExpired(cmd="model", timeout=30),  # timed-out
    ],
    ids=["failed", "empty", "malformed", "errored", "timed-out"],
)
def test_extract_readings_raises_typed_on_every_failure_mode(bad_result):
    """AC-3: `extract_readings` raises a TYPED failure on each failure mode — 0 fabricated readings.

    An empty/malformed/errored/timed-out extraction must RAISE — never return a fabricated or
    partial readings payload that could be mistaken for a valid extraction (the fail-closed
    fidelity-ceiling contract the ingestion path depends on).
    """
    client = ModelClient(backend=_FixtureBackend(extract_readings_result=bad_result))

    returned = None
    try:
        returned = client.extract_readings(b"file", "application/pdf")
    except ModelCallError:
        returned = "RAISED"
    assert returned == "RAISED", "a failure mode returned a payload instead of raising"


@pytest.mark.parametrize("scalar", [None, 42, True, 1.5], ids=["none", "int", "bool", "float"])
def test_extract_readings_non_dict_reading_element_fails_closed(scalar):
    """AC-1a (Tier-2 MUST-FIX): a list carrying a non-dict scalar reading raises `ModelCallError`.

    A list element that is not a dict (`[None]`, `[42]`, `[True]`, `[1.5]`) must fail closed with
    the TYPED `ModelCallError`, never a raw `TypeError`. Without the `isinstance(reading, dict)`
    guard, `keying.is_conformant(scalar)` evaluates `field in scalar` → raw `TypeError` that escapes
    the NFR-3 typed contract callers `except ModelCallError`. RED-capable: drop the dict guard and
    this raises `TypeError`, failing the `pytest.raises(ModelCallError)`.
    """
    client = ModelClient(backend=_FixtureBackend(extract_readings_result=[scalar]))

    with pytest.raises(ModelCallError):
        client.extract_readings(b"file", "application/pdf")


def test_extract_readings_empty_list_fails_closed():
    """AC-3 (Tier-2 SHOULD-FIX): a backend-returned `[]` fails closed via `_call`'s empty check.

    Pins the documented empty-list decision: a zero-reading result is no-usable-readings, raising
    `ModelCallError` (`_call`'s `if not result`), consistent with the `deidentify` mirror. Locks the
    behavior against a future `_call` refactor that might let a falsy list through.
    """
    client = ModelClient(backend=_FixtureBackend(extract_readings_result=[]))

    with pytest.raises(ModelCallError):
        client.extract_readings(b"file", "text/csv")


# --- Cycle 2: the live _ClaudeNoTrainBackend.extract_readings (patched SDK, 0 live spend) ---
#
# `_summary_envelope_text` is shape-agnostic — it JSON-dumps any object into a `.content` text
# block — so a readings-LIST fixture yields a readings envelope the live parse reads back, with
# no new builder. The fake records its `messages.create` kwargs in `.calls`.


def test_extract_readings_live_returns_scripted_readings(monkeypatch):
    """AC-1/AC-2 live: the backend returns the model's parsed readings, not a constant.

    With a patched SDK returning a readings-list envelope, the live call returns that list; a
    DIFFERENT scripted list → different readings (the live non-tautological proof).
    """
    from scripts.model.client import _ClaudeNoTrainBackend

    readings_a = _good_readings_list()
    fake_a = _FakeAnthropic(response_summary={"readings": readings_a})
    _patch_backend_client(monkeypatch, fake_a)
    out_a = _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")
    assert out_a == readings_a

    readings_b = [_good_reading("TSH", "2.1 mIU/L")]
    fake_b = _FakeAnthropic(response_summary={"readings": readings_b})
    _patch_backend_client(monkeypatch, fake_b)
    out_b = _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")
    assert out_b == readings_b

    assert out_a != out_b  # the parse tracks the scripted SDK envelope — not a constant


def test_extract_readings_pdf_carries_base64_document_block(monkeypatch):
    """AC-5 (document): a `application/pdf` file reaches the model as a base64 `document` block."""
    import base64

    from scripts.model.client import _ClaudeNoTrainBackend

    fake = _FakeAnthropic(response_summary={"readings": _good_readings_list()})
    _patch_backend_client(monkeypatch, fake)

    raw = b"%PDF-1.4 fake document bytes"
    _ClaudeNoTrainBackend().extract_readings(raw, "application/pdf")

    block = fake.calls[0]["messages"][0]["content"][0]
    assert block["type"] == "document"
    assert block["source"]["type"] == "base64"
    assert block["source"]["media_type"] == "application/pdf"
    assert base64.standard_b64decode(block["source"]["data"]) == raw  # the raw file reached the model
    # Tier-2 SHOULD-FIX: the structured-output constraint is present (a regression dropping it reds).
    # Asserts presence only — the schema internals stay discretionary (NFR-7).
    assert "output_config" in fake.calls[0]


def test_extract_readings_image_carries_base64_image_block(monkeypatch):
    """AC-5 (image): an image media type reaches the model as a base64 `image` block."""
    import base64

    from scripts.model.client import _ClaudeNoTrainBackend

    fake = _FakeAnthropic(response_summary={"readings": _good_readings_list()})
    _patch_backend_client(monkeypatch, fake)

    raw = b"\x89PNG\r\n\x1a\n fake image bytes"
    _ClaudeNoTrainBackend().extract_readings(raw, "image/png")

    block = fake.calls[0]["messages"][0]["content"][0]
    assert block["type"] == "image"
    assert block["source"]["type"] == "base64"
    assert block["source"]["media_type"] == "image/png"
    assert base64.standard_b64decode(block["source"]["data"]) == raw


def test_extract_readings_text_carries_text_block(monkeypatch):
    """AC-5 (text): a text media type reaches the model as a `text` block carrying the decoded text."""
    from scripts.model.client import _ClaudeNoTrainBackend

    fake = _FakeAnthropic(response_summary={"readings": _good_readings_list()})
    _patch_backend_client(monkeypatch, fake)

    raw = b"item,timepoint,source,value\nHbA1c,2026-01-15,quest-labs,5.4%"
    _ClaudeNoTrainBackend().extract_readings(raw, "text/csv")

    block = fake.calls[0]["messages"][0]["content"][0]
    assert block["type"] == "text"
    assert block["text"] == raw.decode("utf-8")  # the decoded file text reached the model


def test_extract_output_schema_is_object_rooted_for_structured_outputs():
    """The structured-output schema ROOT must be an object — the API rejects a top-level array.

    The live bug (S99 operator run): `_extract_output_schema` returned a top-level ARRAY, which the
    GA structured-outputs API rejects, so EVERY extraction 400'd → fail-closed ModelCallError →
    /upload degraded → the SPA showed "No new data landed". The mock-seam tests were blind (they
    inject a backend that returns a list, never exercising the real schema). This asserts the
    API contract directly: an object root + additionalProperties:false on every object + the
    readings array pinned to the Line Field Set. Failing-capable: revert the schema to a top-level
    array and the root-type assertion reds.
    """
    from scripts.model.client import _extract_output_schema
    from scripts.store.keying import LINE_FIELDS

    schema = _extract_output_schema()
    assert schema["type"] == "object", "structured-output schema root must be an object, not a top-level array"
    assert schema.get("additionalProperties") is False, "the object root must set additionalProperties:false"
    assert schema["required"] == ["readings"]
    arr = schema["properties"]["readings"]
    assert arr["type"] == "array", "readings must be an array of Line-Field-Set objects"
    item = arr["items"]
    assert item["type"] == "object" and item["additionalProperties"] is False
    assert set(item["required"]) == set(LINE_FIELDS), "the item object pins the Line Field Set"


def test_parse_extract_readings_unwraps_readings_object():
    """The parse reads the `readings` array off the object root the schema constrains.

    A bare top-level array (the pre-fix model shape) is rejected — failing closed — never silently
    accepted, so the parse stays aligned with the object-rooted schema.
    """
    import json

    from scripts.model.client import _parse_extract_readings

    class _Block:
        type = "text"

        def __init__(self, text):
            self.text = text

    class _Resp:
        def __init__(self, text):
            self.content = [_Block(text)]

    rows = [_good_reading("ferritin", "120")]
    assert _parse_extract_readings(_Resp(json.dumps({"readings": rows}))) == rows
    with pytest.raises(ValueError):
        _parse_extract_readings(_Resp(json.dumps(rows)))  # a bare array is the API-invalid pre-fix shape


def test_extract_readings_requests_a_generous_max_tokens(monkeypatch):
    """A real lab/biomarker panel emits dozens of readings; the output ceiling must be generous.

    The live S99 bug: max_tokens=2048 truncated the JSON readings array mid-object
    (stop_reason=max_tokens) → json.loads failed → fail-closed ModelCallError → the operator saw
    "no new data". Asserts the extract call requests the named ceiling, well above the prior 2048
    literal. Failing-capable: drop it back to a small literal and the >= floor reds.
    """
    from scripts.model.client import _ClaudeNoTrainBackend, _EXTRACT_MAX_TOKENS

    fake = _FakeAnthropic(response_summary={"readings": _good_readings_list()})
    _patch_backend_client(monkeypatch, fake)
    _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")
    assert fake.calls[0]["max_tokens"] == _EXTRACT_MAX_TOKENS
    assert _EXTRACT_MAX_TOKENS >= 8192, "a real lab panel needs a generous output ceiling"


def test_extract_readings_live_resolves_runtime_key_through_client(monkeypatch):
    """AC-4: the key is resolved at call time via `key_source.resolve` inside `_client`.

    Injects a fake `anthropic` module so the REAL `_client` runs (no `_patch_backend_client`),
    patches `key_source.resolve` to a sentinel, and asserts the SDK client constructed was handed
    THAT sentinel as its `api_key` — a call-time key, never a tracked-file or module-load read.
    """
    import sys
    import types

    from scripts.model import key_source
    from scripts.model.client import _ClaudeNoTrainBackend

    sentinel_key = "sentinel-runtime-key-xyz"
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: sentinel_key)

    fake = _FakeAnthropic(response_summary={"readings": _good_readings_list()})
    captured = {}

    def _make(api_key=None):
        captured["api_key"] = api_key
        return fake

    fake_anthropic = types.ModuleType("anthropic")
    fake_anthropic.Anthropic = _make
    monkeypatch.setitem(sys.modules, "anthropic", fake_anthropic)

    _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")

    assert captured["api_key"] == sentinel_key  # call-time key, no tracked-file read


def test_extract_readings_live_bounded_retry_then_succeed(monkeypatch):
    """AC-3a (succeed-within-bound): the Nth attempt succeeds → the call returns, invoked N times."""
    from scripts.model.client import _ClaudeNoTrainBackend

    raise_seq = [RuntimeError("transient")] * 2 + [None]  # raise twice, succeed on the third
    fake = _FakeAnthropic(response_summary={"readings": _good_readings_list()}, raise_seq=raise_seq)
    _patch_backend_client(monkeypatch, fake)

    result = _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")

    assert result == _good_readings_list()
    assert len(fake.calls) == 3  # invoked exactly the bound, succeeded on the last


def test_extract_readings_live_bounded_retry_then_fail(monkeypatch):
    """AC-3a (exhaust-the-bound): all attempts raise → `ModelCallError` after EXACTLY the bound."""
    from scripts.model.client import (
        ModelCallError,
        _ClaudeNoTrainBackend,
        _EXTRACT_MAX_ATTEMPTS,
    )

    fake = _FakeAnthropic(raise_exc=RuntimeError("always fails"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError):
        _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")

    assert len(fake.calls) == _EXTRACT_MAX_ATTEMPTS  # exactly the bound — never unbounded


@pytest.mark.parametrize(
    "fake_kwargs",
    [
        {"response_summary": None},  # failed: a null body
        {"response_summary": {}},  # empty: a non-list body
        {"response_summary": {"item": "HbA1c"}},  # malformed: a dict, not a readings list
        {"raise_exc": RuntimeError("sdk errored")},  # errored: the SDK raised
        {"raise_exc": subprocess.TimeoutExpired(cmd="model", timeout=30)},  # timed-out
    ],
    ids=["failed", "empty", "malformed", "errored", "timed-out"],
)
def test_extract_readings_live_raises_typed_on_every_failure_mode(monkeypatch, fake_kwargs):
    """AC-3 live: the live backend raises `ModelCallError` on every failure mode — 0 fabricated readings.

    Each failure mode injected at the patched SDK (a null / empty / malformed body, a raised
    exception, a timeout-style raise) makes the live `extract_readings` exhaust the bound and
    raise the typed `ModelCallError` — never returning a fabricated or partial readings payload
    (the parse helper's shape gate rejects a non-list body; the bounded retry exhausts).
    """
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    fake = _FakeAnthropic(**fake_kwargs)
    _patch_backend_client(monkeypatch, fake)

    returned = None
    try:
        returned = _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")
    except ModelCallError:
        returned = "RAISED"
    assert returned == "RAISED", "a failure mode returned a payload instead of raising"


def test_extract_readings_makes_no_live_call_without_the_sdk():
    """AC-7 (0 live spend): an UNPATCHED extract call never reaches a live API — the SDK is absent.

    With the real `anthropic` SDK absent from `.venv`, an UNPATCHED call hits the lazy
    `from anthropic import Anthropic` import inside `_client` and raises `ModuleNotFoundError`
    BEFORE any network request — the proof that no test path makes a live extract call (0 live-API
    spend), mirroring the deid/converse 0-spend pins. Skips when the SDK is installed (operator
    live mode), where the patched cases cover the fail-closed paths.
    """
    import importlib.util

    from scripts.model.client import _ClaudeNoTrainBackend

    if importlib.util.find_spec("anthropic") is not None:
        pytest.skip(
            "anthropic SDK installed (operator live mode) — the absence-based 0-live-spend guard "
            "is N/A; the patched failure-mode tests cover the fail-closed paths"
        )
    with pytest.raises(ModuleNotFoundError):
        _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 ...", "application/pdf")


# --- Cycle 3: the SEC crown-jewel probes (constant message + severed chain, 0 raw-file/key leak) --


def test_extract_readings_error_surface_carries_no_key_or_raw(monkeypatch, tmp_path):
    """AC-6 (SEC): the raised `ModelCallError` str + .args carry no synthetic key or raw-file token.

    The extract call is the first extension of the no-train lane onto the ingestion axis — whole raw
    FILES egress. Seeds a synthetic key (patches `key_source.resolve`) + a synthetic raw-file token,
    forces the failure path with a `messages.create` whose exception message EMBEDS both tokens, and
    asserts `str(exc)` and `exc.args` over the raised `ModelCallError` carry 0 occurrences of either —
    the SEC-01 constant-message lock holds. RED-capable: a variant interpolating `{exc!r}` into the
    extract message leaks the token and turns this RED (demonstrated by temporarily interpolating the
    SDK exception into the raise, observing the assertion fail, then reverting to the constant).
    """
    from scripts.guard import pii_scan
    from scripts.model import key_source
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    raw_token = "Jordan Faketestperson"  # a synthetic stand-in for raw uploaded file content
    # Built at runtime so the source carries NO key-shaped literal (the tree-wide
    # `test_no_api_key_literal_in_tracked_tree` gate flags any `sk-ant-…` literal in the PUBLIC repo).
    key_token = "synthetic-no-train-key-token-DO-NOT-LOG"
    config = tmp_path / "synthetic-identity.txt"
    config.write_text(raw_token + "\n")
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: key_token)

    fake = _FakeAnthropic(raise_exc=RuntimeError(f"sdk error on {raw_token} with {key_token}"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError) as excinfo:
        _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 raw file", "application/pdf")

    surface = str(excinfo.value) + repr(excinfo.value.args)
    assert raw_token not in surface
    assert key_token not in surface
    assert pii_scan.scan_text(str(excinfo.value), token_config=config) == 0


def test_extract_readings_error_traceback_carries_no_key_or_raw(monkeypatch, tmp_path):
    """AC-6a (SEC): the RENDERED traceback (`__cause__`/`__context__` chain) carries no key or raw token.

    `raise ... from <sdk_exc>` would attach the raw SDK exception (carrying the raw file in the request
    content block + the resolved key) as `__cause__` — which a caller's `logger.exception()` /
    `traceback.print_exc()` renders. Forces the failure path with an SDK exception EMBEDDING both
    tokens and asserts the fully-rendered traceback carries 0 occurrences of either AND
    `__cause__ is None` (the `from None` lock). RED-capable: reverting `from None` to `from <exc>`
    re-attaches the raw `__cause__` and turns this RED (demonstrated by temporarily reverting the
    raise, observing the assertion fail, then restoring `from None`).
    """
    from scripts.model import key_source
    from scripts.model.client import ModelCallError, _ClaudeNoTrainBackend

    raw_token = "Jordan Faketestperson"
    key_token = "synthetic-no-train-key-token-DO-NOT-LOG"
    monkeypatch.setattr(key_source, "resolve", lambda *a, **k: key_token)

    fake = _FakeAnthropic(raise_exc=RuntimeError(f"sdk error on {raw_token} with {key_token}"))
    _patch_backend_client(monkeypatch, fake)

    with pytest.raises(ModelCallError) as excinfo:
        _ClaudeNoTrainBackend().extract_readings(b"%PDF-1.4 raw file", "application/pdf")

    e = excinfo.value
    assert e.__cause__ is None  # the chain is severed (`from None`)
    tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    assert raw_token not in tb
    assert key_token not in tb


# --- ADR-0031-T3: the genetics genotype-fact extract mapping (PROMPT-ONLY, 0 live spend) ---
#
# T3 tunes ONE constant string — `_extract_system_prompt` — so a genetics/SNP report maps to
# DURABLE GENOTYPE FACTS in the existing Line Field Set: item=gene+rsID, timepoint=sample-date,
# source="dna-report", value=alleles; capture EVERY finding; store the FACT, not the dated
# interpretation. No schema change (the genotype fact rides the four LINE_FIELDS). The fixture
# backend echoes the scripted readings regardless of `system`, so AC-2/AC-3/AC-4 are
# non-tautological LOCKS; the genuinely RED-on-T3 probe is the AC-1 prompt structural assertion.


def _good_genotype_reading(item="MTNR1B rs10830963", value="(C;G)"):
    """A durable genotype-fact reading: item=gene+rsID, source=dna-report, value=alleles."""
    return {"item": item, "timepoint": "2019-12-13", "source": "dna-report", "value": value}


def test_extract_system_prompt_carries_genetics_genotype_fact_mapping():
    """AC-1: the extract prompt carries the genetics genotype-fact mapping directives.

    Structural token assertions over the constant system instruction (failing-capable, NOT
    exact-wording-pinned per NFR-7): the gene+rsID/sample-date/`dna-report`/alleles mapping rule,
    the capture-ALL directive, and the store-the-fact-not-the-interpretation directive. RED-first:
    the current prompt carries none of these tokens.
    """
    from scripts.model.client import _extract_system_prompt

    prompt = _extract_system_prompt()
    low = prompt.lower()
    # (a) the mapping rule — gene+rsID -> item, "dna-report" -> source, alleles -> value
    assert "rsid" in low, "the prompt must name the gene+rsID -> item mapping"
    assert "dna-report" in prompt, 'the prompt must name the literal "dna-report" source value'
    assert "allele" in low, "the prompt must name the alleles -> value mapping"
    # (b) capture-ALL — a universal quantifier co-occurring with `finding`
    assert ("every" in low or "all" in low) and "finding" in low, "the prompt must capture every finding"
    # (c) not-the-interpretation — store the durable fact, not the dated interpretation
    assert "interpretation" in low, "the prompt must store the fact, not the interpretation"


def test_extract_readings_genetics_fixture_non_tautological(monkeypatch):
    """AC-2 (NON-TAUTOLOGICAL): genetics fixture A -> readings A, a DIFFERENT fixture B -> readings B.

    Via the patched SDK, a genetics report's bytes yield the scripted genotype readings whose `item`
    carries a gene+rsID and `source == "dna-report"`; a different genetics fixture yields different
    readings (B != A). Proves the path carries the model's genotype-shaped parse, not a code
    constant. 0 live spend.
    """
    from scripts.model.client import _ClaudeNoTrainBackend

    readings_a = [_good_genotype_reading("MTNR1B rs10830963", "(C;G)")]
    fake_a = _FakeAnthropic(response_summary={"readings": readings_a})
    _patch_backend_client(monkeypatch, fake_a)
    out_a = _ClaudeNoTrainBackend().extract_readings(b"# Genetics / SNP report\nMTNR1B rs10830963 (C;G)", "text/plain")
    assert out_a == readings_a
    for reading in out_a:
        assert "rs" in reading["item"], f"genotype reading item must carry an rsID: {reading}"
        assert reading["source"] == "dna-report", f"genotype reading source must be dna-report: {reading}"

    readings_b = [_good_genotype_reading("APOE rs429358", "(T;T)")]
    fake_b = _FakeAnthropic(response_summary={"readings": readings_b})
    _patch_backend_client(monkeypatch, fake_b)
    out_b = _ClaudeNoTrainBackend().extract_readings(b"# Genetics / SNP report\nAPOE rs429358 (T;T)", "text/plain")
    assert out_b == readings_b
    assert out_a != out_b  # the parse tracks the scripted envelope — not a constant


def test_extract_readings_genetics_value_is_the_allele_not_the_interpretation(monkeypatch):
    """AC-3: the genotype reading's `value` is the allele call, never the dated interpretation.

    A genetics fixture stores `value` = the alleles "(C;G)"; the returned reading carries that allele
    call and NONE of the trait/risk interpretation narrative (the durable FACT, not the dated
    interpretation; no fabricated genotype — the value is the model's parse). Failing-capable: a
    fixture whose `value` carried the interpretation narrative reds the absence assertion.
    """
    import json

    from scripts.model.client import _ClaudeNoTrainBackend

    reading = _good_genotype_reading("MTNR1B rs10830963", "(C;G)")
    fake = _FakeAnthropic(response_summary={"readings": [reading]})
    _patch_backend_client(monkeypatch, fake)

    got = _ClaudeNoTrainBackend().extract_readings(b"MTNR1B rs10830963 (C;G)", "text/plain")[0]
    assert got["value"] == "(C;G)"  # the allele call, the durable fact
    serialized = json.dumps(got)
    for interp_token in ("risk", "increased fasting glucose"):
        assert interp_token not in got["value"], f"value carried the interpretation token: {interp_token}"
        assert interp_token not in serialized, f"reading carried the interpretation token: {interp_token}"


def test_extract_output_schema_unchanged_for_genotype_fact():
    """AC-4: the genotype fact maps onto the four LINE_FIELDS — no schema change, no second data model.

    The structured-output schema keeps its object root + readings array + the item object whose
    `properties` keys are EXACTLY the Line Field Set (no fifth genetics field bolted on).
    Failing-capable: adding a genetics property to the schema reds the keys-exactly-LINE_FIELDS
    assertion.
    """
    from scripts.model.client import _extract_output_schema
    from scripts.store.keying import LINE_FIELDS

    schema = _extract_output_schema()
    assert schema["type"] == "object"
    assert schema.get("additionalProperties") is False
    assert schema["required"] == ["readings"]
    item = schema["properties"]["readings"]["items"]
    assert item["additionalProperties"] is False
    assert set(item["properties"]) == set(LINE_FIELDS), "no genetics field bolted onto the schema"
