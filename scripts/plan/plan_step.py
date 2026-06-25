"""The step-harness — the skill's per-round drive over the ONE shared driver (ADR-0028-T3).

The plan-generation skill cannot hold a live `plan_driver.drive` generator object across Agent-tool
dispatches (a generator cannot pause across the Agent tool), so the harness is the PAUSE BOUNDARY:
skill -> harness -> driver. `step(serialized_state | None, ...)` constructs/resumes the driver from
the SERIALIZED memo-cache state, advances it EXACTLY ONE yield, and returns
`(pending_request, serialized_state)`. Re-calling `step` with the prior serialized state + the
just-fulfilled envelope re-drives to the NEXT yield (or completion).

There is NO held generator object across calls — the serialized state IS the continuation. The inner
engine is a pure function of `(authors, summary, gates, cached-hook-responses)` (ADR-0028 OQ-5), so
re-constructing a FRESH `plan_driver.drive` each round and replaying the accumulated fulfilments
re-traces the SAME yields deterministically up to the next cache-miss. The state has two parts:
  - the MEMO cache: the accumulated REAUTHOR / ADJUDICATOR responses, keyed by the two documented T2
    shapes (`reauthor:(domain, constraint)` / `adjudicator:(held-domain, hold-class, finding_id)`).
    Seeding `plan_driver.drive(initial_memo=...)` with these makes the cached hooks HIT (no re-yield)
    on the re-drive.
  - the ROUNDS log: the ordered AUTHOR / GATE direct-yield fulfilments (those are NOT memo-backed —
    they are direct yields), replayed in order so the re-drive reaches the same point.

The serialization FORMAT is a lossless `json` round-trip (`json.loads(json.dumps(state)) == state`):
every memo key is the string `"<class>:<json-encoded tail>"` (colon-safe — the finding_id may itself
carry colons), and the rounds log + the final result are json-native.

The harness DRIVES — it does NOT compose a disposition (`compose_disposition` is the ONE composition
site, in `plan_driver`) and does NOT re-derive the adjudication release (`outcome == "cleared"` + the
CRITICAL / H1-H2 check stay in `orchestrate.adjudicate`). The no-fork crown jewel holds at the
harness. It is INDEPENDENTLY DRIVABLE by a fixture consumer — it takes the inner-engine seam, the
gates, the budget, and the memo-cache callables as INPUTS (never a module-scope live import), so a
fixture consumer drives it with 0 live wiring.

The harness is ALSO the PII boundary for the DERIVED yields (ADR-0028-T4): before a GATE / REAUTHOR /
ADJUDICATOR payload leaves the process to a subscription agent, `_scan_yield_payload` value-scans it
(reusing `pii_scan.scan_text_full`, the `deid_in` precedent) and fails CLOSED to the
`YIELD_PAYLOAD_PII` sentinel on a hit. The GATE scan is scoped to `payload[0]` (the assembled plan);
the AUTHOR seam is not scanned (the orchestrator holds only the de-identified summary).
"""

import json

from scripts.guard import pii_scan
from scripts.plan import plan_driver

# The two documented memo-cache key classes (the leading token of `_reauthor_key` /
# `_adjudicator_key`). The serialized memo key is `"<class>:<json-encoded tail>"`; the class token is
# how the harness routes a fulfilled REAUTHOR / ADJUDICATOR envelope back into the memo on the
# appended-envelope re-call.
_REAUTHOR_CLASS = "reauthor"
_ADJUDICATOR_CLASS = "adjudicator"
_MEMO_CLASSES = frozenset({_REAUTHOR_CLASS, _ADJUDICATOR_CLASS})

# The serialized-state field names (a named shape, not an anonymous positional dict).
_MEMO = "memo"
_ROUNDS = "rounds"
_PENDING = "pending"
_DONE = "done"
_RESULT = "result"

# The honest no-plan reason when a DERIVED yield payload — the GATE assembled plan / the ADJUDICATOR
# safety finding / the REAUTHOR constraint — carries raw operator PII (ADR-0028-T4). The value-scan
# at the harness boundary fails CLOSED to this sentinel BEFORE the payload leaves the process to a
# subscription agent: the first-ever scan over these engine-derived artifacts (the AUTHOR seam is
# structurally clean — the orchestrator holds only the de-identified summary). Mirrors the `deid_in`
# value-PII fail-closed return shape; name no value (no PII echo in the reason).
YIELD_PAYLOAD_PII = "yield-payload-pii"

# The private "no fulfilment supplied" sentinel for `step`'s `fulfilled_envelope` default. It is NOT
# `None`, because `None` is a LEGITIMATE, safety-critical fulfilment: a REAUTHOR returning `None` (the
# trainer cannot fuel a sustainable session — the workout is HELD) and an ADJUDICATOR returning `None`
# (the medical liaison DECLINES to clear a held finding — the safe default, the hold stands) must be
# CACHED so the re-drive HITs (exactly as the synchronous `_run_with_replay` caches every envelope
# unconditionally). Defaulting to this sentinel lets `step` route a SUPPLIED `None` into the cache
# while still skipping a re-call that supplies no fulfilment (the first call).
_UNFULFILLED = object()


def step(serialized_state, *, fulfilled_envelope=_UNFULFILLED, summary=None, domains=None, store_read=None,
         root=None, plan_date=None, gates=None, gate_producer=None, compose=None, on_date=None,
         reauthor=None, adjudicator=None, budget=None, revise_cap=plan_driver.DEFAULT_REVISE_CAP,
         identity_config=pii_scan.DEFAULT_IDENTITY_CONFIG):
    """Advance the shared driver EXACTLY one yield from the serialized state; return the next request.

    The per-round drive entry (the skill's pause boundary). Re-constructs a FRESH `plan_driver.drive`
    from the serialized memo-cache state + the ordered AUTHOR / GATE rounds log, seeds the driver's
    memo with the accumulated REAUTHOR / ADJUDICATOR responses (so those cached hooks HIT rather than
    re-yield), replays the rounds log for each direct AUTHOR / GATE yield, and STOPS at the FIRST
    yield the accumulated state does not already answer — returning it as `pending_request`. The
    just-`fulfilled_envelope` from the prior call's pending request is appended into the right slot
    (the memo for a REAUTHOR / ADJUDICATOR fulfilment, the rounds log for an AUTHOR / GATE one) before
    the re-drive. On completion the driver's final result is captured into the state and
    `pending_request` is `None`.

    The harness composes nothing and re-derives nothing — it DRIVES the one shared driver (the
    no-fork crown jewel). The driver inputs (the inner-engine seam, the gates, the budget, the
    memo-cache callables) are passed as arguments each call, never a module-scope live import.

    Args:
        serialized_state (dict | None): The prior round's serialized state. `None` on the FIRST call
            (a fresh run — the memo + rounds log start empty).
        fulfilled_envelope: The envelope the consumer dispatched for the prior pending request.
            Defaults to the `_UNFULFILLED` sentinel (no fulfilment supplied — the first call). A
            SUPPLIED fulfilment — INCLUDING a legitimate `None` (a REAUTHOR that declines to fuel a
            sustainable session, an ADJUDICATOR that declines to clear a held finding — the safe
            defaults) — is routed into the memo (REAUTHOR / ADJUDICATOR) or the rounds log (AUTHOR /
            GATE) by the prior pending request's recorded `kind`. A supplied `None` is cached exactly
            as the synchronous `_run_with_replay` caches it, so the re-drive HITs (no re-yield) and
            the engine proceeds to the held / declined terminal state rather than re-firing forever.
        summary (dict): The de-identified operator summary (forwarded to `drive`).
        domains (tuple): The plan domains to generate (forwarded to `drive`).
        store_read (Callable): The store read surface, instance-root pre-bound.
        root (str | Path): The real store root the surfaced plans promote into.
        plan_date (str): The plans' YYYY-MM-DD date.
        gates (dict): Per-domain safety inputs forwarded to `run_generation`.
        gate_producer (Callable): The RAW-VERDICT producer the GATE yield carries.
        compose (Callable, optional): The raw-verdicts -> disposition mapping forwarded to `drive`.
        on_date (str, optional): The doctor-visit-queue collation date.
        reauthor (Callable, optional): The energy-bounce re-dispatch hook (forwarded to `drive`).
        adjudicator (Callable, optional): The held-finding liaison hook (forwarded to `drive`).
        budget (DispatchBudget, optional): The per-plan dispatch budget.
        revise_cap (int, optional): The bounded revise-loop cap.
        identity_config (str | Path, optional): The gitignored operator-identity token file the
            boundary value-scan loads (the same `deid_in` precedent default). Passed as an INPUT
            (never a module-scope live read) so the scan stays fixture-drivable.

    Returns:
        (Request | None) The next pending typed `Request(kind, payload)` the consumer must fulfil, or
        `None` when the run completed (or the boundary value-scan failed closed on a derived payload
        carrying raw PII — the run's result is then the `YIELD_PAYLOAD_PII` sentinel).
        (dict) The re-serialized state (the continuation) — pass it to the next `step` call.
    """
    state = _fresh_state() if serialized_state is None else serialized_state
    if state.get(_DONE):
        return None, state

    # Route the just-fulfilled envelope into the right slot per the PRIOR pending request's kind.
    # The envelope is json-normalized BEFORE it enters the state, so the serialized state stays a
    # lossless `json` round-trip by construction (a fixture envelope may carry tuples — e.g. a
    # `lenses` tuple — which json renders as a list; normalizing here makes the state's bytes the
    # canonical json form, and the re-drive runs over that form identically).
    pending = state.get(_PENDING)
    if pending is not None and fulfilled_envelope is not _UNFULFILLED:
        if pending["kind"] == plan_driver.GATE and isinstance(fulfilled_envelope, BaseException):
            # The GATE producer RAISED (a safety-lens dispatch failed mid-review). A BaseException is
            # not json-serializable, so it cannot enter the lossless rounds log; record the json-safe
            # raised-GATE MARKER instead — `_send_round` reconstructs it into a fail-closed `gen.throw`
            # on the re-drive, so the round-based path reproduces the synchronous SAFETY_BLOCKED-on-
            # gate-raise (`drive`'s GATE-yield `except Exception: disposition = None`), exactly as the
            # synchronous consumer's `driver.throw(gate_error)` does.
            state[_ROUNDS] = state[_ROUNDS] + [dict(_GATE_RAISED)]
        else:
            normalized = _json_native(fulfilled_envelope)
            if pending["kind"] in (plan_driver.REAUTHOR, plan_driver.ADJUDICATOR):
                state[_MEMO][pending["key"]] = normalized
            else:
                state[_ROUNDS] = state[_ROUNDS] + [normalized]

    # Re-construct a FRESH driver seeded with the accumulated memo (the cached REAUTHOR / ADJUDICATOR
    # responses HIT instead of re-yielding), replay the AUTHOR / GATE rounds log, and advance to the
    # FIRST yield the accumulated state does not already answer — the no-held-generator re-drive.
    request, done, result = _drive_to_next(
        memo=_deserialize_memo(state[_MEMO]), rounds=state[_ROUNDS], summary=summary, domains=domains,
        store_read=store_read, root=root, plan_date=plan_date, gates=gates,
        gate_producer=gate_producer, compose=compose, on_date=on_date, reauthor=reauthor,
        adjudicator=adjudicator, budget=budget, revise_cap=revise_cap,
    )

    if done:
        state[_PENDING] = None
        state[_DONE] = True
        state[_RESULT] = _json_native(result)
        return None, state

    # CROWN-JEWEL value-scan (ADR-0028-T4): before the DERIVED yield payload leaves the process to a
    # subscription agent, scan it for raw operator PII. The GATE assembled plan / the ADJUDICATOR
    # safety finding / the REAUTHOR constraint are DERIVED from the engine — their PII-freeness is
    # transitive-but-unverified (the AUTHOR seam is structurally clean). On a hit the payload FAILS
    # CLOSED — it does NOT leave the process: the harness halts to the fail-closed sentinel rather
    # than returning the pending request onward (mirrors the `deid_in` fail-closed return; no PII echo).
    if _scan_yield_payload(request, identity_config):
        state[_PENDING] = None
        state[_DONE] = True
        state[_RESULT] = {"deidentified": False, "reason": YIELD_PAYLOAD_PII}
        return None, state

    state[_PENDING] = {"kind": request.kind, "key": _serialize_key(request_key(request))}
    return request, state


def _scan_yield_payload(request, identity_config):
    """Value-scan a DERIVED yield payload before it leaves the process; return the raw-PII hit count.

    The crown-jewel value-scan (ADR-0028-T4) over the DERIVED GATE / ADJUDICATOR / REAUTHOR yield
    payloads — the first-ever scan over these engine-derived artifacts. It REUSES
    `pii_scan.scan_text_full` (the same value-scan utility the `deid_in` boundary uses, the precedent
    shape) over the `str(payload)`-flattened payload, so STRING PII inside a non-scalar container is
    caught too. The AUTHOR seam is NOT scanned: its payload is the de-identified summary the
    orchestrator already holds (structurally clean), so an AUTHOR request returns 0.

    GATE scope: the GATE payload is `(assembled_plan, gate_producer)` — the scan is scoped to
    `payload[0]` (the assembled plan, the actual derived-PII surface). `payload[1]` is the
    `gate_producer` CALLABLE (it `str()`s to an inert `<function ...>` repr); it is scoped out
    EXPLICITLY so a future producer that closes over operator-derived data is not silently scanned
    around, and so the scan targets the assembled plan rather than a callable repr. REAUTHOR /
    ADJUDICATOR: the payload IS the derived artifact (the constraint / the safety finding) — scan it
    whole.

    Args:
        request (Request): The pending typed `Request(kind, payload)` about to leave the process.
        identity_config (str | Path): The gitignored operator-identity token file the scan loads.

    Returns:
        (int) The count of raw-PII matches in the derived payload (0 on a clean payload, and 0 for an
        AUTHOR request — the structurally-clean seam).
    """
    if request.kind == plan_driver.GATE:
        scanned = request.payload[0]
    elif request.kind in (plan_driver.REAUTHOR, plan_driver.ADJUDICATOR):
        scanned = request.payload
    else:
        return 0
    return pii_scan.scan_text_full(str(scanned), token_config=identity_config)


def _drive_to_next(*, memo, rounds, summary, domains, store_read, root, plan_date, gates,
                   gate_producer, compose, on_date, reauthor, adjudicator, budget, revise_cap):
    """Re-construct the driver, replay the rounds log, and advance to the next un-answered yield.

    The OQ-5 round-based replay: a FRESH `plan_driver.drive` is seeded with the accumulated memo, then
    walked one yield at a time. Each direct AUTHOR / GATE yield is fulfilled from the ordered `rounds`
    log (a GATE round recorded as the raised-GATE marker is reconstructed into a fail-closed
    `gen.throw` — see `_send_round`). When the rounds log is exhausted (a NEW AUTHOR / GATE yield) or a
    NOT-yet-cached REAUTHOR / ADJUDICATOR yield appears (a cache-miss the seeded memo did not answer),
    that yield is the next pending request. If the driver completes during the replay, its result is
    returned.

    Returns:
        (Request | None) The next un-answered pending request, or `None` on completion.
        (bool) Whether the driver completed.
        (dict | None) The driver's final result on completion.
    """
    gen = plan_driver.drive(
        summary, domains, store_read, root, plan_date=plan_date, gates=gates,
        gate_producer=gate_producer, compose=compose, on_date=on_date, reauthor=reauthor,
        adjudicator=adjudicator, budget=budget, revise_cap=revise_cap, initial_memo=memo,
    )
    replay = iter(rounds)
    try:
        request = next(gen)
        while True:
            if request.kind in (plan_driver.AUTHOR, plan_driver.GATE):
                envelope = next(replay, _UNANSWERED)
                if envelope is _UNANSWERED:
                    return request, False, None  # the rounds log is exhausted — a NEW direct yield
                request = _send_round(gen, request, envelope)
            else:
                # a REAUTHOR / ADJUDICATOR yield: the seeded memo did not answer it -> a NEW cache-miss
                return request, False, None
    except StopIteration as done:
        return None, True, done.value


# A unique sentinel distinguishing an exhausted rounds log from a legitimately-`None` fulfilment.
_UNANSWERED = object()

# The json-safe MARKER recorded in the rounds log for a GATE round whose producer RAISED (a safety
# lens failed mid-review). A raised producer is a BaseException — NOT json-serializable, so it cannot
# enter the lossless rounds log directly; the marker stands in for it, and `_send_round` reconstructs
# it into a `gen.throw` of `_GateProducerRaised` on the re-drive, reproducing the synchronous
# SAFETY_BLOCKED-on-gate-raise (`drive`'s GATE-yield `except Exception: disposition = None`). A clean
# raw verdict is `{judge, review}` — never this shape, so the marker is unambiguous.
_GATE_RAISED = {"__gate_raised__": True}


class _GateProducerRaised(Exception):
    """The fail-closed sentinel `_send_round` throws into the driver for a recorded GATE-producer raise.

    A plain `Exception` (NOT a `BaseException`): the driver's GATE-yield fail-closed wrap
    (`except Exception: disposition = None`) MUST catch it -> SAFETY_BLOCKED, mirroring the synchronous
    consumer's `driver.throw(gate_error)`. (`_ReplayNeeded` is the BaseException that must NOT be
    caught; this one is its opposite — it must be, so the raised GATE fails closed to no plan.)
    """


def _send_round(gen, request, envelope):
    """Send a replayed AUTHOR / GATE round envelope back into the driver and return the next yield.

    A GATE envelope is the raw verdicts (or a producer-call result); the harness does NOT compose it
    — it `.send()`s it back verbatim (`drive` composes via `compose_disposition`, the ONE site). A
    GATE round recorded as the raised-GATE MARKER (`_GATE_RAISED` — the producer raised mid-review, a
    safety lens failed) is reconstructed into a `gen.throw` of the `_GateProducerRaised` fail-closed
    sentinel: the driver's GATE-yield `except Exception: disposition = None` catches it ->
    SAFETY_BLOCKED, reproducing the synchronous consumer's `driver.throw(gate_error)` fail-closed wrap
    (the surface gate stays in `drive`). AUTHOR rounds — and clean GATE verdicts — are always `.send()`'d.
    """
    if (request.kind == plan_driver.GATE and isinstance(envelope, dict)
            and envelope.get("__gate_raised__") is True):
        return gen.throw(_GateProducerRaised("a GATE producer raised mid-review — fail closed"))
    return gen.send(envelope)


def request_key(request):
    """Compute the memo key for a REAUTHOR / ADJUDICATOR request (the routing slot), or `None`.

    The driver's REAUTHOR / ADJUDICATOR `Request.payload` carries the de-identified hook args; the
    memo key is `plan_driver._reauthor_key(*payload)` / `_adjudicator_key(*payload)` — the SAME
    distiller the driver's memo wrapper uses, so the harness routes the fulfilled envelope into the
    exact slot the re-drive's cache HIT reads. Each AUTHOR / GATE request is a direct yield (no memo
    key) and returns `None`.

    Args:
        request (Request): A yielded typed `Request(kind, payload)`.

    Returns:
        (tuple | None) The memo cache key, or `None` for an AUTHOR / GATE request.
    """
    if request.kind == plan_driver.REAUTHOR:
        return plan_driver._reauthor_key(*request.payload)
    if request.kind == plan_driver.ADJUDICATOR:
        return plan_driver._adjudicator_key(*request.payload)
    return None


def result_of(serialized_state):
    """Read the driver's final result from a terminal serialized state.

    Returns:
        (dict | None) The promoted/halt result captured when the driver completed, or `None` if the
        run has not completed.
    """
    return serialized_state.get(_RESULT)


def memo_of(serialized_state):
    """Read the serialized memo-cache sub-dict (string keys -> envelopes) from a serialized state.

    Returns:
        (dict) The memo cache, keyed by the documented `"<class>:<tail>"` string shapes.
    """
    return serialized_state.get(_MEMO, {})


def key_class(serialized_key):
    """Return the memo-key class token (`reauthor` / `adjudicator`) of a serialized string key.

    Returns:
        (str) The class token (the substring before the first `:`).
    """
    return serialized_key.split(":", 1)[0]


def parse_key(serialized_key):
    """Parse a serialized memo key into its class token + its tail tuple.

    The serialized key is `"<class>:<json-encoded tail list>"` — colon-safe (the json-encoded tail
    is parsed as a unit, so a finding_id carrying colons round-trips).

    Args:
        serialized_key (str): A serialized memo-cache key.

    Returns:
        (str) The class token (`reauthor` / `adjudicator`).
        (list) The tail components (REAUTHOR: `[domain, constraint]`; ADJUDICATOR:
        `[held-domain, hold-class, finding_id]`).
    """
    cls, encoded_tail = serialized_key.split(":", 1)
    return cls, json.loads(encoded_tail)


def _fresh_state():
    """Build the empty serialized state for a fresh run (no memo, no rounds, nothing pending)."""
    return {_MEMO: {}, _ROUNDS: [], _PENDING: None, _DONE: False, _RESULT: None}


def _json_native(obj):
    """Normalize an envelope / result to its canonical json-native form (tuples -> lists).

    A fixture envelope (or the driver's final result) may carry tuples — a `lenses` tuple, a nested
    author fragment — which json renders as a list. Round-tripping through json here makes the value
    the canonical json form BEFORE it enters the serialized state, so the state stays a lossless
    `json` round-trip (`json.loads(json.dumps(state)) == state`) by construction, and the re-drive
    runs over that canonical form identically each round.

    Args:
        obj: A json-serializable envelope or driver result.

    Returns:
        The same value in its canonical json-native form (tuples become lists).
    """
    return json.loads(json.dumps(obj))


def _serialize_key(key_tuple):
    """Serialize a memo key tuple into the lossless `"<class>:<json-encoded tail>"` string form.

    The driver's memo keys are tuples (`("reauthor", domain, ceiling)` /
    `("adjudicator", held_domain, source, finding_id)`); json cannot key a dict by a tuple, so the
    key is `class + ":" + json.dumps(tail)`. The json-encoded tail is colon-safe and round-trips
    losslessly (a finding_id carrying colons survives). `None` (an AUTHOR / GATE request, no key)
    passes through unchanged.

    Args:
        key_tuple (tuple | None): The driver memo key, or `None` for a direct-yield request.

    Returns:
        (str | None) The serialized string key, or `None`.
    """
    if key_tuple is None:
        return None
    cls = key_tuple[0]
    tail = list(key_tuple[1:])
    return f"{cls}:{json.dumps(tail)}"


def _deserialize_memo(serialized_memo):
    """Rebuild the driver's tuple-keyed memo from the serialized string-keyed memo.

    The inverse of `_serialize_key` over the whole memo: each `"<class>:<json-encoded tail>"` string
    key becomes the `(class, *tail)` tuple the driver's memo wrapper looks up, so the re-drive's
    cache HITs the accumulated REAUTHOR / ADJUDICATOR responses.

    Args:
        serialized_memo (dict): The serialized memo (string keys -> envelopes).

    Returns:
        (dict) The driver-shaped memo (tuple keys -> envelopes).
    """
    memo = {}
    for serialized_key, envelope in serialized_memo.items():
        cls, tail = parse_key(serialized_key)
        memo[(cls, *tail)] = envelope
    return memo
