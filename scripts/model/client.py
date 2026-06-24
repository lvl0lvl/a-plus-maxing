"""The swappable no-train model client — the system's single model boundary.

`ModelClient` is a NARROW three-method surface — `converse(...)` (one intake turn),
`author(domain, summary)` (the plan-author envelope), and `deidentify(raw_intake)` (the
de-id-IN seam: raw plan-intake → de-identified summary, ADR-0020) — over an INJECTABLE
backend seam. The backend defaults to a Claude no-train commercial-API backend
(`_ClaudeNoTrainBackend`, the only site a model-client SDK import appears); swapping the
provider is a backend injection at construction — no caller-side edit (ADR-0015 Negative-2).
Every backend call is fail-closed: a failed / empty / errored / timed-out call RAISES
`ModelCallError` and NEVER returns a fabricated or silently-partial payload (NFR-2).

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
    """The three-method no-train model client over an injectable backend seam.

    Attributes:
        backend: The provider backend (the swap seam). A backend exposes
            `converse(messages) -> {"reply": str, "extraction": list}`,
            `author(domain, summary) -> envelope`, and
            `deidentify(raw_intake) -> de_identified_summary`. Defaults to the Claude
            no-train commercial-API backend.
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

    def deidentify(self, raw_intake):
        """De-identify a raw operator plan-intake into the de-identified summary (de-id IN).

        The de-id-IN seam (ADR-0020): raw plan-intake PII in, the de-identified summary the
        plan pipeline consumes out — the `router.summarize`-shaped band/class mapping, never
        raw PII. Fail-closed: an empty / malformed (non-mapping) result raises `ModelCallError`,
        never a fabricated or partial summary.

        Args:
            raw_intake (dict): The raw operator plan-intake (carries raw-PII fields).

        Returns:
            (dict) The de-identified summary mapping the orchestrator consumes.
        """
        result = _call(self.backend.deidentify, raw_intake)
        if not isinstance(result, dict):
            raise ModelCallError("deidentify: backend returned an empty or malformed summary")
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
        # SEC-01: a CONSTANT message — never interpolate `{exc!r}`, which can carry raw
        # input (the backend's exception text). The chained `from exc` keeps the original
        # in the traceback frame for debugging; the `str(ModelCallError)` surface stays raw-free.
        raise ModelCallError("backend call failed") from exc
    if not result:
        raise ModelCallError("backend returned an empty result")
    return result


def _deid_prompt(raw_intake):
    """Build the de-id-IN prompt: inline the raw intake, instruct a field-set summary.

    The model is given the raw intake (which carries PII) and told to emit ONLY a
    de-identified band/class summary whose keys are drawn from `router.SUMMARY_FIELD_SET`
    — no raw PII, no novel fields. A read of the existing whitelist for the field roster,
    not a second copy. The subset check is NOT done here; it is `deid_in`'s downstream gate.
    """
    import json

    from scripts.plan.router import SUMMARY_FIELD_SET

    field_roster = ", ".join(SUMMARY_FIELD_SET)
    return (
        "De-identify the raw operator plan-intake below into a JSON summary object whose "
        "keys are drawn ONLY from this field set: "
        f"{field_roster}. "
        "Emit de-identified band/class tokens only — never a raw legal name, raw lab value, "
        "address, or any other raw PII, and never a key outside the field set. "
        "Respond with the JSON object and nothing else.\n\n"
        f"Raw intake:\n{json.dumps(raw_intake)}"
    )


def _parse_deid_summary(response):
    """Parse the model response into the de-identified summary mapping.

    Reads the first `text` content block off the SDK envelope and decodes it as the JSON
    summary object — the model's `SUMMARY_FIELD_SET`-shaped band/class mapping. Returns the
    parsed mapping verbatim (the raw intake never flows through here); a non-text / non-JSON
    / non-mapping response raises, failing closed at the `_call` boundary to `ModelCallError`.
    """
    import json

    text = next((b.text for b in response.content if getattr(b, "type", None) == "text"), None)
    if text is None:
        raise ValueError("deidentify: model response carried no text block")
    summary = json.loads(text)
    if not isinstance(summary, dict):
        raise ValueError("deidentify: model response was not a JSON object")
    return summary


# The de-id call's bounded retry ceiling — at most this many `messages.create` attempts
# before the failure propagates to the `_call` fail-closed wrapper (never an unbounded
# retry). An in-task design constant (recipe disposition #8), named here, not a call-site
# literal, so the bound is one machine-diffable value.
_DEID_MAX_ATTEMPTS = 3

# The per-call timeout (seconds) the SDK request runs under — a bounded wait, never an
# indefinite block. Passed through `with_options(timeout=...)` at call time.
_DEID_TIMEOUT_SECONDS = 60.0


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

    def deidentify(self, raw_intake):
        """De-identify a raw plan-intake against the no-train API (the live de-id-IN call).

        Sends the raw intake to the `MODEL` no-train API under a bounded retry-with-timeout
        loop and returns the model's parsed de-identified summary — a `SUMMARY_FIELD_SET`-
        shaped band/class mapping, never the raw intake. The raw intake is held in memory
        only (the local arg + the prompt string); it is written to no path. The returned
        mapping is the parse of the model response, not a passthrough of the raw input; the
        downstream `ModelClient.deidentify` `isinstance(dict)` check + `deid_in`'s
        `⊆ SUMMARY_FIELD_SET` whitelist fail it closed if the model emits an out-of-set field.

        Args:
            raw_intake (dict): The raw operator plan-intake (carries raw-PII fields).

        Returns:
            (dict) The de-identified summary mapping (`SUMMARY_FIELD_SET`-keyed).
        """
        client = self._client()
        prompt = _deid_prompt(raw_intake)
        last_exc = None
        for _ in range(_DEID_MAX_ATTEMPTS):
            try:
                response = client.with_options(timeout=_DEID_TIMEOUT_SECONDS).messages.create(
                    model=self.MODEL,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )
                return _parse_deid_summary(response)
            except Exception as exc:  # bounded: try again until the attempt ceiling
                last_exc = exc
        # SEC-01: a CONSTANT message — never interpolate the SDK exception (it can carry the
        # raw intake or the resolved key). The chained `from last_exc` keeps the original in
        # the traceback frame for debugging; the `str(ModelCallError)` surface stays raw-free.
        # Raised at the backend boundary so the raw SDK exception never escapes `deidentify`.
        raise ModelCallError("deidentify call failed") from last_exc
