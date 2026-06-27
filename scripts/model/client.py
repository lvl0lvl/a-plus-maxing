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

    def extract_readings(self, file_content, media_type):
        """Extract structured readings from an uploaded file (the no-train extraction seam).

        The uploaded file content + its media type in, a `list` of readings out — each a `dict`
        carrying the full Line Field Set (`item`, `timepoint`, `source`, `value` per
        `keying.LINE_FIELDS`). Fail-closed: a non-`list` return, a `list` carrying a reading that
        fails `keying.is_conformant` (a missing Line-Field-Set field), or any backend failure
        (empty / errored / timed-out) raises `ModelCallError` — never a fabricated or partial
        readings payload.

        Args:
            file_content (bytes | str): The uploaded file content (bytes for a document/image
                media type, decodable bytes or str for a text media type).
            media_type (str): The file's IANA media type (e.g. "application/pdf", "image/png").

        Returns:
            (list) The extracted readings, each a Line-Field-Set `dict`.
        """
        from scripts.store.keying import is_conformant

        result = _call(self.backend.extract_readings, file_content, media_type)
        if not isinstance(result, list):
            raise ModelCallError("extract_readings: backend returned a non-list result")
        for reading in result:
            if not is_conformant(reading):
                raise ModelCallError("extract_readings: backend returned a field-short reading")
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
    except Exception:  # the model boundary: any backend error fails closed, typed
        # SEC-01: a CONSTANT message — never interpolate `{exc!r}`, which can carry raw
        # input (the backend's exception text). `from None` INTENTIONALLY SUPPRESSES the
        # `__cause__`/`__context__` chain: the original SDK exception can carry raw operator
        # PII (the request prompt) + the resolved key, which a caller's `logger.exception()` /
        # `traceback.print_exc()` would render. At this PII/key boundary the chained cause's
        # debuggability is not worth the latent raw/key leak (PUBLIC repo).
        raise ModelCallError("backend call failed") from None
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


def _converse_system_prompt():
    """Build the converse system instruction: constrain the reply/extraction JSON shape.

    A CONSTANT system instruction (no raw conversation interpolated — the turns are passed
    natively as the `messages` array, never inlined here) telling the model to respond with
    ONLY a JSON object `{"reply": str, "extraction": list}` — the assistant reply text plus a
    list of structured field proposals. The converse analogue of `_deid_prompt`'s field-set
    instruction; the shape gate is the downstream `_parse_converse_turn`.
    """
    return (
        "You are conducting one intake turn. Respond with a single JSON object and nothing "
        'else, shaped exactly as {"reply": <assistant reply text>, "extraction": [<zero or '
        "more structured field proposals>]}. The reply is the text shown to the operator; the "
        "extraction is the list of fields you inferred this turn (an empty list when none). "
        "Emit no prose outside the JSON object."
    )


def _parse_converse_turn(response):
    """Parse the model response into the `{"reply", "extraction"}` turn mapping.

    Reads the first `text` content block off the SDK envelope and decodes it as the JSON turn
    object — the assistant reply text plus a structured extraction proposal. Returns the
    parsed mapping (the raw conversation never flows through here); a non-text / non-JSON /
    wrong-shape response raises, failing closed at the retry loop to `ModelCallError`. The
    shape check mirrors the public `ModelClient.converse` validation (a dict with a truthy
    `reply` and an `extraction` key), so a truthy-but-malformed body is rejected at the
    backend, never returned as a partial turn.
    """
    import json

    text = next((b.text for b in response.content if getattr(b, "type", None) == "text"), None)
    if text is None:
        raise ValueError("converse: model response carried no text block")
    turn = json.loads(text)
    if not isinstance(turn, dict) or not turn.get("reply") or "extraction" not in turn:
        raise ValueError("converse: model response was not the {reply, extraction} shape")
    return turn


# The de-id call's bounded retry ceiling — at most this many `messages.create` attempts
# before the failure propagates to the `_call` fail-closed wrapper (never an unbounded
# retry). An in-task design constant (recipe disposition #8), named here, not a call-site
# literal, so the bound is one machine-diffable value.
_DEID_MAX_ATTEMPTS = 3

# The per-call timeout (seconds) the SDK request runs under — a bounded wait, never an
# indefinite block. Passed through `with_options(timeout=...)` at call time.
_DEID_TIMEOUT_SECONDS = 60.0

# The converse call's bounded retry ceiling — at most this many `messages.create` attempts
# before the failure propagates to the fail-closed raise (never an unbounded retry). The
# converse analogue of `_DEID_MAX_ATTEMPTS`, named here so the bound is one machine-diffable
# value, not a call-site literal.
_CONVERSE_MAX_ATTEMPTS = 3

# The per-call timeout (seconds) the converse SDK request runs under — a bounded wait, never
# an indefinite block. Passed through `with_options(timeout=...)` at call time.
_CONVERSE_TIMEOUT_SECONDS = 60.0

# The extract call's bounded retry ceiling — at most this many `messages.create` attempts before
# the failure propagates to the fail-closed raise (never an unbounded retry). The extract
# analogue of `_DEID_MAX_ATTEMPTS`, named here so the bound is one machine-diffable value, not a
# call-site literal.
_EXTRACT_MAX_ATTEMPTS = 3

# The per-call timeout (seconds) the extract SDK request runs under — a bounded wait, never an
# indefinite block. Passed through `with_options(timeout=...)` at call time.
_EXTRACT_TIMEOUT_SECONDS = 60.0


def _extract_system_prompt():
    """Build the extract system instruction: constrain the returned readings to the Line Field Set.

    A CONSTANT system instruction (no raw file content interpolated — the file is passed natively
    as the user-turn content block, never inlined here) telling the model to respond with ONLY a
    JSON array of readings whose keys are drawn from `keying.LINE_FIELDS`. The extract analogue of
    `_deid_prompt`'s field-set instruction; the shape gate is the downstream `_parse_extract_readings`.
    """
    from scripts.store.keying import LINE_FIELDS

    field_roster = ", ".join(LINE_FIELDS)
    return (
        "You extract structured readings from the uploaded file content. Respond with a single "
        "JSON array and nothing else. Each array element is a reading object whose keys are exactly "
        f"this Line Field Set: {field_roster}. Emit no prose outside the JSON array."
    )


def _extract_content_block(file_content, media_type):
    """Build the media-typed content block carrying the uploaded file for the model.

    The pinned file→model mechanism: a base64 `document` source for "application/pdf", a base64
    `image` source for an image media type, a `text` block for a text media type. A single
    media-type dispatch — the load-bearing egress surface that carries the raw file to the model.
    """
    import base64

    if media_type == "application/pdf":
        return {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": base64.standard_b64encode(file_content).decode("utf-8"),
            },
        }
    if media_type.startswith("image/"):
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": base64.standard_b64encode(file_content).decode("utf-8"),
            },
        }
    text = file_content.decode("utf-8") if isinstance(file_content, (bytes, bytearray)) else file_content
    return {"type": "text", "text": text}


def _extract_output_schema():
    """Build the `output_config.format` json_schema constraining the readings to the Line Field Set.

    A top-level array of Line-Field-Set objects, derived from `keying.LINE_FIELDS` (the single
    source of truth, not a hand-retyped roster). Structured outputs require `additionalProperties:
    false` on objects; the internal field ordering is implementer discretion (NFR-7).
    """
    from scripts.store.keying import LINE_FIELDS

    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {field: {"type": "string"} for field in LINE_FIELDS},
            "required": list(LINE_FIELDS),
            "additionalProperties": False,
        },
    }


def _parse_extract_readings(response):
    """Parse the model response into the readings list.

    Reads the first `text` content block off the SDK envelope and decodes it as the JSON readings
    array — the model's Line-Field-Set readings. Returns the parsed list verbatim (the raw file
    never flows through here); a non-text / non-JSON / non-list response raises, failing closed at
    the retry loop to `ModelCallError`. Mirrors `_parse_deid_summary`'s posture (first text block →
    `json.loads`), with a list shape gate instead of a dict gate.
    """
    import json

    text = next((b.text for b in response.content if getattr(b, "type", None) == "text"), None)
    if text is None:
        raise ValueError("extract_readings: model response carried no text block")
    readings = json.loads(text)
    if not isinstance(readings, list):
        raise ValueError("extract_readings: model response was not a JSON array")
    return readings


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
        """Run one intake turn against the no-train API (the live converse call).

        Sends the conversation `messages` to the `MODEL` no-train API under a bounded
        retry-with-timeout loop and returns the model's parsed turn — `{"reply", "extraction"}`,
        the assistant reply text plus a structured extraction proposal. A constant `system`
        instruction constrains the shape; the raw conversation is held in memory only (the
        local arg plus the request) and is written to no path. On bound exhaustion the raw SDK
        exception is suppressed and a constant-message `ModelCallError` is raised — never a
        fabricated or partial turn (the downstream `ModelClient.converse` validation is the
        outer net).

        Args:
            messages (list[dict]): The conversation turns (`{"role", "content"}`).

        Returns:
            (dict) The parsed turn `{"reply": str, "extraction": list}`.
        """
        client = self._client()
        system = _converse_system_prompt()
        for _ in range(_CONVERSE_MAX_ATTEMPTS):
            try:
                response = client.with_options(timeout=_CONVERSE_TIMEOUT_SECONDS).messages.create(
                    model=self.MODEL,
                    max_tokens=2048,
                    system=system,
                    messages=messages,
                )
                return _parse_converse_turn(response)
            except Exception:  # bounded: try again until the attempt ceiling
                pass
        # SEC-01: a CONSTANT message — never interpolate the SDK exception (it can carry the
        # raw conversation or the resolved key). `from None` INTENTIONALLY SUPPRESSES the
        # `__cause__`/`__context__` chain: the raw SDK exception carries the raw conversation
        # (the request) + the resolved key, which a caller's `logger.exception()` /
        # `traceback.print_exc()` would render. At this PII/key boundary the chained cause's
        # debuggability is not worth the latent raw/key leak (PUBLIC repo).
        # Raised at the backend boundary so the raw SDK exception never escapes `converse`.
        raise ModelCallError("converse call failed") from None

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
        # raw intake or the resolved key). `from None` INTENTIONALLY SUPPRESSES the
        # `__cause__`/`__context__` chain: `last_exc` is the raw SDK exception carrying the raw
        # intake (the request prompt) + the resolved key, which a caller's `logger.exception()` /
        # `traceback.print_exc()` would render. At this PII/key boundary the chained cause's
        # debuggability is not worth the latent raw/key leak (PUBLIC repo).
        # Raised at the backend boundary so the raw SDK exception never escapes `deidentify`.
        raise ModelCallError("deidentify call failed") from None

    def extract_readings(self, file_content, media_type):
        """Extract readings from an uploaded file against the no-train API (the live extract call).

        Sends the file to the `MODEL` no-train API as the pinned media-typed content block (a base64
        `document` source for "application/pdf", a base64 `image` source for an image media type, a
        `text` block for a text media type) under a bounded retry-with-timeout loop, with an
        `output_config.format` json_schema constraining the returned readings to the Line Field Set,
        and returns the model's parsed readings list — never the raw file. The raw file is held in
        memory only (the local arg + the request); it is written to no path. The returned list is the
        parse of the model response, not a passthrough; the downstream `ModelClient.extract_readings`
        `isinstance(list)` + per-reading `is_conformant` checks fail it closed on a malformed shape.

        Args:
            file_content (bytes | str): The uploaded file content (bytes for a document/image media
                type, decodable bytes or str for a text media type).
            media_type (str): The file's IANA media type (e.g. "application/pdf", "image/png").

        Returns:
            (list) The extracted readings, each a Line-Field-Set `dict`.
        """
        client = self._client()
        system = _extract_system_prompt()
        content_block = _extract_content_block(file_content, media_type)
        schema = _extract_output_schema()
        for _ in range(_EXTRACT_MAX_ATTEMPTS):
            try:
                response = client.with_options(timeout=_EXTRACT_TIMEOUT_SECONDS).messages.create(
                    model=self.MODEL,
                    max_tokens=2048,
                    system=system,
                    messages=[{"role": "user", "content": [content_block]}],
                    output_config={"format": {"type": "json_schema", "schema": schema}},
                )
                return _parse_extract_readings(response)
            except Exception:  # bounded: try again until the attempt ceiling
                pass
        # SEC-01: a CONSTANT message — never interpolate the SDK exception (it can carry the raw
        # file bytes or the resolved key). `from None` INTENTIONALLY SUPPRESSES the
        # `__cause__`/`__context__` chain: the raw SDK exception carries the raw file (the request
        # content block) + the resolved key, which a caller's `logger.exception()` /
        # `traceback.print_exc()` would render. At this PII/key boundary the chained cause's
        # debuggability is not worth the latent raw/key leak (PUBLIC repo).
        # Raised at the backend boundary so the raw SDK exception never escapes `extract_readings`.
        raise ModelCallError("extract_readings call failed") from None
