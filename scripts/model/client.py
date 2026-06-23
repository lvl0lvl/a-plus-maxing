"""The swappable no-train model client — the system's single model boundary.

`ModelClient` is a NARROW two-method surface — `converse(...)` (one intake turn) and
`author(domain, summary)` (the plan-author envelope) — over an INJECTABLE backend seam.
The backend defaults to a Claude no-train commercial-API backend (`_ClaudeNoTrainBackend`,
the only site a model-client SDK import appears); swapping the provider is a backend
injection at construction — no caller-side edit (ADR-0015 Negative-2). Every backend call
is fail-closed: a failed / empty / errored / timed-out call RAISES `ModelCallError` and
NEVER returns a fabricated or silently-partial payload (NFR-2).

The published surface is frozen here (ADR-0015-T1): `ADR-0016-T1` imports `converse`,
`ADR-0015-T3` imports `author`, `ADR-0017-T1` validates `converse`'s extraction proposal.
The SDK request/response wire detail is internal (NFR-5: interface pinned, internals
discretionary).

Two `author` conformance levels coexist: `ModelClient.author` validates the backend
envelope and RAISES on a malformed shape, while the captured-envelope adapter
(`generate_plan._FixedEnvelopeClient.author`) returns the pre-resolved envelope verbatim
(backward-compat with existing callers — the envelope was already validated when first
authored, so the adapter re-wrap fires no second model call and adds no second check).
"""


class ModelCallError(RuntimeError):
    """A model-backend call failed — failed, empty, errored, or timed out.

    Raised by both `ModelClient` methods on any backend failure mode. The client never
    returns a fabricated or partial payload on failure (the NFR-2 fail-closed contract).
    """


class ModelClient:
    """The two-method no-train model client over an injectable backend seam.

    Attributes:
        backend: The provider backend (the swap seam). A backend exposes
            `converse(messages) -> {"reply": str, "extraction": list}` and
            `author(domain, summary) -> envelope`. Defaults to the Claude no-train
            commercial-API backend.
    """

    def __init__(self, backend=None):
        self.backend = backend if backend is not None else _ClaudeNoTrainBackend()

    def converse(self, messages):
        """Run one intake turn through the backend.

        Args:
            messages (list[dict]): The conversation turns (`{"role", "content"}`).

        Returns:
            (dict) `{"reply": str, "extraction": list}` — the assistant reply text and a
            structured extraction proposal (the input `ADR-0017-T1` validates).
        """
        result = _call(self.backend.converse, messages)
        if not isinstance(result, dict) or not result.get("reply") or "extraction" not in result:
            raise ModelCallError("converse: backend returned an empty or malformed result")
        return result

    def author(self, domain, summary):
        """Author a domain's plan recommendations over a de-identified summary.

        Args:
            domain (str): The plan domain (e.g. "workout").
            summary (dict): The de-identified `router.summarize` summary mapping.

        Returns:
            (dict) The plan-author envelope `{"specialist": slug, "recommendations": [...]}`
            or the thin-library sentinel `{"thin_library": True, "specialist": slug}`.
        """
        result = _call(self.backend.author, domain, summary)
        if not isinstance(result, dict) or not _is_author_envelope(result):
            raise ModelCallError("author: backend returned an empty or malformed envelope")
        return result


def _is_author_envelope(result):
    """True when `result` is a valid author envelope or the thin-library sentinel."""
    if result.get("thin_library") is True and result.get("specialist"):
        return True
    return bool(result.get("specialist")) and isinstance(result.get("recommendations"), list)


def _call(backend_method, *args):
    """Invoke a backend method, converting any failure into `ModelCallError`.

    A raised exception (errored / timed-out) or a falsy return (failed / empty) becomes a
    typed `ModelCallError` — the fail-closed boundary. The per-method shape checks above
    catch a malformed-but-truthy payload.
    """
    try:
        result = backend_method(*args)
    except ModelCallError:
        raise
    except Exception as exc:  # the model boundary: any backend error fails closed, typed
        raise ModelCallError(f"backend call failed: {exc!r}") from exc
    if not result:
        raise ModelCallError("backend returned an empty result")
    return result


class _ClaudeNoTrainBackend:
    """The default backend: the Claude no-train commercial API.

    The ONLY model-client SDK import site in the codebase (lazily imported so the client
    module loads without the SDK or a key — the key is resolved at call time via
    `key_source.resolve`). A live call is made only when this backend is actually invoked;
    it is never exercised in tests (tests inject a fixture backend).
    """

    MODEL = "claude-opus-4-8"

    def _client(self):
        from anthropic import Anthropic  # the single SDK import, inside scripts/model/

        from scripts.model.key_source import resolve

        return Anthropic(api_key=resolve())

    def converse(self, messages):
        """One intake turn against the no-train API."""
        raise NotImplementedError(
            "live converse is wired at the Wave-B operator checkpoint; tests inject a backend"
        )

    def author(self, domain, summary):
        """Author a domain's recommendations against the no-train API."""
        raise NotImplementedError(
            "live author is wired by ADR-0015-T3; tests inject a backend"
        )
