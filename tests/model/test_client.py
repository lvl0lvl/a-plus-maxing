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


def test_no_train_backend_deidentify_is_not_invoked_in_tests():
    """The default no-train backend's `deidentify` is `NotImplementedError`, never live.

    Mirrors the `converse`/`author` stubs: the live de-id call is wired at the operator
    checkpoint. Calling it raises `NotImplementedError` (lit at the checkpoint) — the proof
    that no test path makes a live de-id call (0 live-API spend).
    """
    from scripts.model.client import _ClaudeNoTrainBackend

    with pytest.raises(NotImplementedError):
        _ClaudeNoTrainBackend().deidentify({"legal-name": "Jordan Tester"})


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
