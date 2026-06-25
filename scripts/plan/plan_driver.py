"""The ONE shared control-inversion driver — the extracted revise-loop control flow (ADR-0026-T1).

This module owns the autonomous bounded revise loop that was inline in
`plan_orchestrator.run_orchestrated`: the scratch-store lifecycle, the `while True:`
gate->branch->re-dispatch sequencing, the `safety_passed is True` surface gate, the bounded-revise
cap, the preserved halts, and the scratch-and-promote logic. It exists in EXACTLY ONE definition
(the no-fork crown jewel) — `run_orchestrated` (API/test mode) and the ADR-0026-T3 skill
subscription mode both DRIVE this driver, neither re-hosts the loop.

`drive` is a generator-coroutine. Its drive-protocol (the shared control-inversion contract,
ADR-0028-T1 typed-request shape): the driver YIELDS a typed `Request(kind, payload)` — never a bare
tuple — with `kind` in `REQUEST_KINDS` (AUTHOR / GATE emitted at T1; REAUTHOR / ADJUDICATOR reserved
for T2). The CONSUMER switches on `kind`, fulfils the request, and `.send()`s the RAW fulfilment back:
  - AUTHOR request (`payload = (domains, summary, gates)`): the CONSUMER captures each domain's
    author envelope (via its `dispatch` seam — a fixture in tests, a real subscription agent in the
    skill) and SENDS the captured `{domain: envelope}` fragment back (`gen.send(envelopes)`).
  - GATE request (`payload = (assembled_plan, gate_producer)`): the CONSUMER dispatches the judge
    and each safety lens (via the RAW-VERDICT producer the payload carries) and SENDS the RAW
    `{judge, review}` verdicts back — NEVER a composed callable (ADR-0028 OQ-2 rejects shipping the
    skill a Python callable whose body must synchronously call agents) and NEVER a finished
    disposition. `drive` then calls `compose_disposition` over the raw verdicts (the ONE composition
    site) and applies the fail-closed `safety_passed is True` surface gate over the result — both
    stay in ONE place; the consumer builds NO disposition and re-derives nothing.
  - The driver runs the inner engine (`pipeline.run_generation`) over the captured authors against
    an ISOLATED scratch store, gates the assembled result via the yielded GATE request, and either
    (a) promotes the survivors into `root` and STOPS (accept + `safety_passed is True`), (b) re-yields
    an AUTHOR request for the REVISE-targeted domains (quality REVISE + safety passing, below
    `revise_cap`), or (c) STOPS at a terminal honest-no-plan halt (`SAFETY_BLOCKED` /
    `REVISE_EXHAUSTED` / `PROMOTE_FAILED` / `DISPATCH_CAP_EXCEEDED`).
  - The disposition the driver READS is the FIXED 3-key shape `{accept: bool, safety_passed: bool,
    revise_domains: list}` — `safety_passed is True` is the ONLY surface path; `revise_domains`
    names only run-set domains.

The driver is INDEPENDENTLY DRIVABLE by a fixture-supplied `gate_producer` + a consumer feeding
fixture envelopes, with no live client and no skill — it takes the inner-engine seam, the budget,
and the gates as inputs (never a module-scope live import). The de-id-sentinel halt + the budget
construction live in the consumer (`run_orchestrated`), BEFORE the driver is entered.

REUSE only: the driver calls `pipeline.run_generation` (the byte-frozen inner-engine seam) and
`store.append`/`store.items`/`store.read` (the unchanged store surface) — it defines no store key,
records no plan directly, and leaves the reconciler + the safety gates unchanged.
"""

import tempfile
from collections import namedtuple
from pathlib import Path

from scripts.plan import pipeline
from scripts.plan.dispatch_budget import DispatchCapExceeded
from scripts.store import store

# The typed discriminated-union drive request (ADR-0028-T1). The driver yields a `Request(kind,
# payload)` instead of a bare tuple, so every yield is exhaustively tagged with exactly one `kind`
# and the consumer switches on it (a mis-handled / omitted kind fails closed rather than
# default-allowing). T1 emits AUTHOR + GATE; REAUTHOR / ADJUDICATOR are RESERVED tokens T2 fills
# (throw/replay) — reserved here so the kind set is the stable contract downstream consumes.
AUTHOR = "AUTHOR"
GATE = "GATE"
REAUTHOR = "REAUTHOR"
ADJUDICATOR = "ADJUDICATOR"

# The valid `kind` set (the no-fork single source of truth for both the driver's yields and the
# consumer's exhaustive switch). An unrecognized kind is NOT in this set, so the consumer's switch
# fails closed on it (Negative-1 mitigation).
REQUEST_KINDS = frozenset({AUTHOR, GATE, REAUTHOR, ADJUDICATOR})

Request = namedtuple("Request", ("kind", "payload"))
Request.__doc__ = (
    "A typed discriminated-union drive request the driver yields. `kind` is one of `REQUEST_KINDS`; "
    "`payload` is the kind-specific fulfilment input the consumer reads. AUTHOR: `(domains, summary, "
    "gates)` — the consumer dispatches each domain's specialist and sends back `{domain: envelope}`. "
    "GATE: `(assembled_plan, gate_producer)` — the consumer dispatches the judge + each lens via the "
    "RAW-VERDICT producer and sends back the raw `{judge, review}` verdicts (NOT a composed callable, "
    "NOT a disposition); `drive` composes them via `compose_disposition` (the ONE composition site) "
    "and applies the fail-closed `safety_passed is True` surface gate."
)

class _ReplayNeeded(BaseException):
    """The throw/replay-memo sentinel: a memo-cache MISS on a REAUTHOR / ADJUDICATOR hook (ADR-0028-T2).

    REAUTHOR (the energy-bounce re-author) and ADJUDICATOR (the held-finding medical-liaison) fire
    DEEP INSIDE the byte-frozen `orchestrate.generate_plans`, NOT in `drive`'s frame, so they cannot
    become direct yields like AUTHOR / GATE. The memo-cache callable `drive` forwards into
    `run_generation` raises THIS sentinel on a cache MISS; it unwinds THROUGH the frozen engine (whose
    only catch is the narrow `except ModelCallError` — no broad `except Exception`/`except BaseException`)
    up to `drive`'s replay handler, which yields the typed request, caches the dispatched envelope, and
    re-drives the pass over a FRESH scratch store.

    It subclasses `BaseException` DIRECTLY, NOT `Exception` — so neither the engine's
    `except ModelCallError` nor `drive`'s GATE-yield `except Exception: disposition = None` (the
    `_safe_gate` analogue) can swallow it into a SAFETY_BLOCKED. The non-swallowable contract rests on
    this base; re-typing it to `Exception` is an ADR-0028 HALT condition (Architect review required).

    Attributes:
        kind (str): The dispatch CLASS — `REAUTHOR` or `ADJUDICATOR` — so `drive`'s catch knows which
            typed `Request` to yield.
        key (tuple): The memo cache key the miss was raised for, so `drive` knows which cache slot the
            `.send()`'d envelope fills (`("reauthor", domain, ceiling)` /
            `("adjudicator", held_domain, hold_class, finding_id)`).
        payload: The de-identified fulfilment payload the typed request carries to the consumer.
    """

    def __init__(self, kind, key, payload):
        self.kind = kind
        self.key = key
        self.payload = payload
        super().__init__(f"replay needed: {kind} {key}")


# domain -> the role whose full profile the dispatch prompt inlines (INV-ROLE-INLINING). The SINGLE
# definition (the no-fork crown jewel) for both uses: the driver's out-of-run-set revise guard reads
# it for MEMBERSHIP (a `revise_domains` entry naming a domain not in this map — or not in the run's
# `domains` — is a malformed disposition, routed to SAFETY_BLOCKED rather than letting an unguarded
# `_ROLE_OF_DOMAIN[domain]` KeyError escape), and `plan_orchestrator._dispatch_domains` imports it for
# the role-slug VALUE lookup (`_ROLE_OF_DOMAIN[domain]` -> the profile the dispatch prompt inlines).
# The orchestrator already imports `plan_driver`, so it imports this map — no fork, no import cycle.
_ROLE_OF_DOMAIN = {
    "workout": "personal-trainer",
    "nutrition": "nutritionist",
    "supplements": "supplement-specialist",
    "peptides": "peptide-specialist",
}

# The bounded revise loop's reason vocabulary (ADR-0022-T2), the same kebab-string family as
# `dispatch_budget.DISPATCH_CAP_EXCEEDED`. SAFETY_BLOCKED is the TERMINAL fail-closed halt (a
# non-positive safety disposition — `safety_passed` not boolean-True); REVISE_EXHAUSTED is the
# bounded-cap halt (a non-converging quality miss past `revise_cap`).
SAFETY_BLOCKED = "safety-blocked"
REVISE_EXHAUSTED = "revise-exhausted"

# The honest no-plan reason when promoting the surfaced pass's plan rows from the scratch store into
# `root` fails mid-write (an OSError on a `store.append`). Same kebab-string family; the promote is
# guarded so a write failure fails closed (honest no-plan, the real store NOT left partial) rather
# than escaping uncaught with a half-promoted plan set.
PROMOTE_FAILED = "promote-failed"

# The bounded revise cap default (dispositions #2: N=3 fixed at build-plan time). A named module
# constant (NOT a hard-coded literal at the loop site), mirroring
# `dispatch_budget.DEFAULT_DISPATCH_CAP`; `run_orchestrated`'s `revise_cap` keyword defaults to it
# so the bound is configurable + testable.
DEFAULT_REVISE_CAP = 3


def drive(summary, domains, store_read, root, *, plan_date, gates, gate_producer, compose=None,
          on_date=None, reauthor=None, adjudicator=None, budget=None, revise_cap=DEFAULT_REVISE_CAP,
          initial_memo=None):
    """Drive the autonomous bounded revise loop as a control-inversion generator-coroutine.

    The ONE shared revise-loop control flow (the no-fork crown jewel). Yields a dispatch-request
    `(domains, summary, gates)` for each pass the consumer must author, receives the captured author
    envelopes via `.send()`, runs the inner engine against an isolated scratch store, yields a GATE
    request carrying the assembled result + the raw-verdict producer, COMPOSES the consumer's raw
    `{judge, review}` verdicts into the 3-key disposition (the ONE composition site), and either
    promotes the survivors into `root` (accept + `safety_passed is True`), re-yields a
    revise-request, or halts to honest no-plan. The inner engine writes plan::/dvq:: as it generates,
    BEFORE the whole-plan gate runs — so each pass writes to an ISOLATED scratch store, and the
    surviving plans are PROMOTED into `root` ONLY when the gates surface them (a SAFETY_BLOCKED /
    REVISE_EXHAUSTED halt promotes nothing — the fail-closed surface).

    Args:
        summary (dict): The de-identified operator summary the dispatch authors over.
        domains (tuple): The plan domains to generate this run.
        store_read (Callable): The store read surface, instance-root pre-bound (operator state is
            read from the real root through this, never the scratch).
        root (str | Path): The real store root the surfaced plans promote into.
        plan_date (str): The plans' YYYY-MM-DD date.
        gates (dict): Per-domain safety inputs forwarded to `run_generation`.
        gate_producer (Callable): The RAW-VERDICT producer (charge-wrapped by the consumer) the GATE
            yield carries: `gate_producer(assembled_plan) -> {judge, review}`. The consumer
            dispatches the judge + each lens through it and sends the raw verdicts back; `drive`
            composes them via `compose` — the producer builds NO disposition (ADR-0028 OQ-2).
        compose (Callable, optional): The raw-verdicts -> 3-key-disposition mapping
            `compose(verdicts, assembled_plan) -> disposition` (the ONE composition site). Defaults
            to `gate_dispatch.compose_disposition` (lazily imported to avoid the
            `gate_dispatch -> safety_review -> plan_orchestrator -> plan_driver` import cycle); a
            test-injection point, never a second composition site.
        on_date (str, optional): The doctor-visit-queue collation date. Forwarded to
            `run_generation`.
        reauthor (Callable, optional): The energy-bounce re-dispatch hook. When provided, `drive`
            inverts it via THROW/REPLAY-MEMO (ADR-0028-T2): a memo-cache wrapper is forwarded into
            `run_generation` that raises the `_ReplayNeeded` sentinel on a cache MISS — `drive`
            catches it, yields a `REAUTHOR` request, caches the `.send()`'d envelope, and re-drives
            over a fresh scratch store. `None` -> no hook (the engine's no-reauthor branch).
        adjudicator (Callable, optional): The held-finding medical-liaison dispatch hook (the inner
            safety gate — never bypassed). Inverted via the SAME throw/replay-memo mechanism: a memo
            wrapper raises `_ReplayNeeded` on a cache MISS per held domain; `drive` yields one
            `ADJUDICATOR` request per held domain, caches each `.send()`'d liaison envelope, and
            re-drives. The consumer returns ONLY the raw envelope — the `outcome == "cleared"`
            release stays in `orchestrate.adjudicate` (the no-fork crown jewel). `None` -> no hook.
        budget (DispatchBudget, optional): The per-plan dispatch budget for `dispatch_count` surfacing
            (charged by the consumer on each specialist dispatch + by the charge-wrapped
            `gate_dispatch`). When `None`, `dispatch_count` is reported as `0`.
        revise_cap (int, optional): The bounded revise-loop cap. Defaults to `DEFAULT_REVISE_CAP`.
        initial_memo (dict, optional): A pre-seeded throw/replay-memo cache (ADR-0028-T3). The
            step-harness (`plan_step.step`) re-constructs the driver each round from the SERIALIZED
            memo cache and seeds the accumulated REAUTHOR / ADJUDICATOR responses here, so the
            re-drive HITS those cached keys instead of re-yielding them (the OQ-5 round-based
            replay — there is no held generator). `drive` mutates this dict in place (the harness
            reads the accumulated cache back from the same object). `None` -> the legacy
            generator-local cache (`{}` when a hook is wired, else `None`), unchanged.

    Yields:
        (Request) A typed `Request(kind, payload)` (ADR-0028-T1): an `AUTHOR` request whose payload
        is `(domains, summary, gates)` — the consumer sends back the captured `{domain: envelope}`
        authors fragment — or a `GATE` request whose payload is `(assembled_plan, gate_producer)` —
        the consumer dispatches the judge + each lens via the producer and sends back the RAW
        `{judge, review}` verdicts (`drive` composes them).

    Returns:
        (dict) On a surfaced plan, the `run_generation` result plus `dispatch_count`. On a halt, the
        honest no-plan state (`SAFETY_BLOCKED` / `REVISE_EXHAUSTED` / `PROMOTE_FAILED`). The
        dispatch-cap halt's `DispatchCapExceeded` PROPAGATES to the consumer's cap-halt handler.
    """
    if compose is None:
        # Lazy import: `gate_dispatch` pulls in `safety_review` -> `plan_orchestrator` -> this
        # module, so a module-scope import would cycle. `compose_disposition` is a pure function;
        # importing it inside the call keeps the driver independently drivable (AC-10) and module-
        # scope free of the composer (and of any live wiring).
        from scripts.plan.gate_dispatch import compose_disposition
        compose = compose_disposition
    count = (lambda: budget.count) if budget is not None else (lambda: 0)
    # The throw/replay-memo cache (ADR-0028-T2): keyed by the dispatch class + the engine's hook
    # arguments. A hook fires DEEP inside the byte-frozen engine (`reauthor("workout", {...})` /
    # `_adjudicate_with_band(safety_finding, adjudicator)`), so it cannot yield directly; the memo
    # wrapper forwarded into `run_generation` raises `_ReplayNeeded` on a cache MISS, `drive` yields
    # the typed request, caches the dispatched envelope here, and re-drives. On the replay the key is
    # cached, so the wrapper returns the envelope and the engine proceeds unchanged. The cache lives
    # for the whole `drive` invocation (one slot per distinct hook key across all passes / re-drives).
    # A harness-supplied `initial_memo` seeds the cache with the accumulated REAUTHOR / ADJUDICATOR
    # responses from prior `plan_step.step` rounds (ADR-0028-T3): the re-drive then HITS those keys
    # instead of re-yielding them, so the round-based replay is deterministic with no held generator.
    # `drive` mutates it in place — the harness reads the accumulated cache back from the same object.
    # Absent it, the legacy generator-local cache is unchanged.
    if initial_memo is not None:
        memo = initial_memo
    else:
        memo = {} if (reauthor is not None or adjudicator is not None) else None
    engine_reauthor = _memo_hook(REAUTHOR, _reauthor_key, memo) if reauthor is not None else None
    engine_adjudicator = (
        _memo_hook(ADJUDICATOR, _adjudicator_key, memo) if adjudicator is not None else None
    )
    with tempfile.TemporaryDirectory(prefix="aplus-revise-") as scratch_parent:
        revise_count = 0
        authors = yield Request(AUTHOR, (tuple(domains), summary, gates))
        result, scratch = yield from _run_with_replay(
            authors, store_read, scratch_parent, "pass-0", plan_date=plan_date, on_date=on_date,
            gates=gates, reauthor=engine_reauthor, adjudicator=engine_adjudicator, memo=memo,
        )
        while True:
            # GATE direct-yield inversion (ADR-0028-T1, OQ-2): yield a GATE request carrying the
            # assembled result + the RAW-VERDICT producer. The CONSUMER dispatches the judge + each
            # lens through the producer and `.send()`s the raw `{judge, review}` verdicts back here;
            # `drive` COMPOSES them via `compose` (the ONE composition site) and applies the surface
            # gate. The fail-closed contract is preserved verbatim (Security HIGH-1): a producer that
            # RAISES (a lens dispatch failed mid-review) is THROWN into this generator by the
            # consumer (`gen.throw`) and reads as ambiguous -> `disposition = None` -> SAFETY_BLOCKED;
            # a malformed raw verdict (non-dict / missing key) composes to a not-`True`
            # `safety_passed` (fail-closed in `compose_disposition`); `DispatchCapExceeded` is the
            # budget halt (not a gate ambiguity), re-raised to propagate to the consumer's cap-halt
            # handler. The surface gate (`safety_passed is True`) stays here, in ONE place — the
            # consumer builds NO disposition and re-derives nothing.
            try:
                verdicts = yield Request(GATE, (result, gate_producer))
                disposition = compose(verdicts, result)
            except DispatchCapExceeded:
                raise
            except Exception:
                disposition = None
            # SAFETY GATE (the only surface path is a positive boolean-True safety assertion).
            # `False` / `None` / absent / non-bool / non-dict / a raised gate -> TERMINAL
            # SAFETY_BLOCKED: never re-authored, never looped, never overridden (AC-2, R2, HIGH-1).
            if not (isinstance(disposition, dict) and disposition.get("safety_passed") is True):
                return _honest_no_plan(SAFETY_BLOCKED, dispatch_count=count())
            # QUALITY: an ACCEPT with safety passing surfaces the plan — PROMOTE the survivors from
            # the scratch store into `root` and return (AC-1, AC-4). A write OSError mid-promote
            # fails CLOSED to honest no-plan (the real store is not left surfacing a half-promoted
            # plan set) rather than escaping uncaught (SEC-01).
            if disposition.get("accept") is True:
                try:
                    _promote_plans(scratch, root)
                except OSError:
                    return _honest_no_plan(PROMOTE_FAILED, dispatch_count=count())
                return {**result, "dispatch_count": count()}
            # A quality REVISE with safety passing: bounded re-author. Halt at `revise_cap` without
            # convergence (AC-3, R1 — the count of re-dispatch passes is capped exactly).
            if revise_count >= revise_cap:
                return _honest_no_plan(REVISE_EXHAUSTED, dispatch_count=count())
            # Re-dispatch ONLY the REVISE-targeted domains (an inner non-overridably-held domain is
            # never a revise TARGET — AC-5/R3; the loop re-authors only the quality-flagged domains
            # the composed disposition names). Re-running with the SAME authors is store-idempotent
            # (identical result, no convergence), so the per-domain `authors` is REBUILT from a fresh
            # specialist dispatch (the consumer's `dispatch` seam — MF-1).
            revise_domains = disposition.get("revise_domains") or []
            # An unknown / out-of-run-set revise TARGET is a malformed disposition: route it to the
            # same TERMINAL fail-closed halt the loop already takes for a non-dict / absent-key safety
            # disposition, rather than letting an unguarded `_ROLE_OF_DOMAIN[domain]` KeyError escape
            # uncaught (BUG-01/API-02). The composed gate must only ever name a domain this run is
            # generating.
            if any(d not in _ROLE_OF_DOMAIN or d not in domains for d in revise_domains):
                return _honest_no_plan(SAFETY_BLOCKED, dispatch_count=count())
            authors.update((yield Request(AUTHOR, (tuple(revise_domains), summary, gates))))
            revise_count += 1
            result, scratch = yield from _run_with_replay(
                authors, store_read, scratch_parent, f"pass-{revise_count}", plan_date=plan_date,
                on_date=on_date, gates=gates, reauthor=engine_reauthor,
                adjudicator=engine_adjudicator, memo=memo,
            )


def _reauthor_key(domain, constraint):
    """The memo key for an energy-bounce re-author hook call (`reauthor(domain, constraint)`).

    The engine calls `reauthor("workout", {"sustainable_training_kcal": ceiling})`
    ([orchestrate.py:550]); the key distills the dispatch class + the de-identified constraint into a
    hashable slot. `constraint` is the bounce directive's de-identified ceiling dict — no raw PII.

    Args:
        domain (str): The bounced domain (always `"workout"` in V1).
        constraint (dict): The sustainable-energy ceiling (`{"sustainable_training_kcal": int}`).

    Returns:
        (tuple) The cache key `("reauthor", domain, ceiling)`.
    """
    return ("reauthor", domain, constraint.get("sustainable_training_kcal"))


def _adjudicator_key(safety_finding):
    """The memo key for a held-finding adjudicator hook call (`adjudicator(safety_finding)`).

    The engine calls `_adjudicate_with_band(safety_finding, adjudicator)` once per held domain
    ([orchestrate.py:578,595,613]); each held finding carries a distinct `finding_id` (distilled at
    [orchestrate.py:222,255,301]), so `(held_domain, source, finding_id)` is a distinct slot per held
    domain — one replay round, one `ADJUDICATOR` yield, per held domain.

    Args:
        safety_finding (dict): The held finding routed to the liaison (`finding_id`, `source`,
            `held_domain`).

    Returns:
        (tuple) The cache key `("adjudicator", held_domain, source, finding_id)`.
    """
    return (
        "adjudicator", safety_finding.get("held_domain"), safety_finding.get("source"),
        safety_finding.get("finding_id"),
    )


def _memo_hook(kind, key_of, memo):
    """Build the memo-cache wrapper the engine calls in place of the raw REAUTHOR / ADJUDICATOR hook.

    The wrapper forwarded into `run_generation` (so the byte-frozen engine stays unchanged — it still
    calls a plain callable). On a cache HIT it returns the cached envelope (the engine proceeds
    unchanged); on a cache MISS it raises the `_ReplayNeeded` sentinel carrying the dispatch class +
    the key — the sentinel unwinds THROUGH the engine to `drive`'s replay handler. The wrapper itself
    NEVER dispatches and NEVER charges — the consumer dispatches the real hook (charge-wrapped) when
    `drive` yields the typed request, so the charge accrues once per cache MISS only (ADR-0028-T2).

    Args:
        kind (str): The dispatch class (`REAUTHOR` / `ADJUDICATOR`).
        key_of (Callable): The hook-args -> memo-key distiller (`_reauthor_key` / `_adjudicator_key`).
        memo (dict): The shared throw/replay-memo cache.

    Returns:
        (Callable) The engine-facing memo wrapper, same call signature as the raw hook.
    """
    def wrapper(*args):
        key = key_of(*args)
        if key in memo:
            return memo[key]
        raise _ReplayNeeded(kind, key, args)

    return wrapper


def _run_with_replay(authors, store_read, scratch_parent, pass_label, *, plan_date, on_date, gates,
                     reauthor, adjudicator, memo):
    """Run one pass through the inner engine, inverting any REAUTHOR / ADJUDICATOR hook via replay.

    The throw/replay-memo driver for a single pass (ADR-0028-T2). Runs `pipeline.run_generation`
    against a FRESH scratch store; if a memo-cache MISS raises `_ReplayNeeded` deep inside the
    byte-frozen engine, catch it, YIELD the typed `Request(kind, payload)`, cache the consumer's
    `.send()`'d envelope under the sentinel's key, and RE-DRIVE the pass over a NEW scratch dir (the
    engine re-runs against clean scratch — never double-writing the discarded one). The re-drive
    loops until `run_generation` completes without a sentinel (every fired hook now cached); the LAST,
    completed scratch holds the promotable rows and is returned for `_promote_plans`. With no hooks
    (`memo is None`) it is the plain single `run_generation` call (the legacy path, unchanged).

    Args:
        authors (dict): The captured author envelopes for this pass.
        store_read (Callable): The store read surface (the real root, pre-bound).
        scratch_parent (str | Path): The per-`drive` scratch parent dir.
        pass_label (str): The pass's scratch-dir stem (`pass-0` / `pass-{n}`).
        plan_date (str): The plans' date.
        on_date (str | None): The doctor-visit-queue collation date.
        gates (dict): Per-domain safety inputs.
        reauthor (Callable | None): The engine-facing memo `reauthor` wrapper (or `None`).
        adjudicator (Callable | None): The engine-facing memo `adjudicator` wrapper (or `None`).
        memo (dict | None): The shared throw/replay-memo cache (`None` when no hook is wired).

    Yields:
        (Request) A `REAUTHOR` / `ADJUDICATOR` typed request per cache MISS, fulfilled by the
        consumer's `.send()` of the dispatched envelope.

    Returns:
        (dict) The completed `run_generation` result.
        (Path) The scratch dir the completed result wrote into (the promote source).
    """
    attempt = 0
    while True:
        scratch = Path(scratch_parent) / (pass_label if attempt == 0 else f"{pass_label}-replay-{attempt}")
        try:
            result = pipeline.run_generation(
                authors, store_read, scratch, plan_date=plan_date, on_date=on_date, gates=gates,
                reauthor=reauthor, adjudicator=adjudicator,
            )
        except _ReplayNeeded as need:
            # A memo MISS fired deep in the engine: yield the typed request, cache the consumer's
            # dispatched envelope under the sentinel's key, and re-drive over a fresh scratch dir.
            envelope = yield Request(need.kind, need.payload)
            memo[need.key] = envelope
            attempt += 1
            continue
        return result, scratch


def _honest_no_plan(reason, *, dispatch_count, deidentified=True, **extra):
    """The shared honest-no-plan return shape for every halt path (0 plans surfaced).

    The single shape the de-id-sentinel, dispatch-cap, safety-blocked, and revise-exhausted halts
    all return — `{"deidentified", "reason", "results": {}, "dvq_entries": [], "dispatch_count"}` —
    so the divergent halt builders share one definition. `extra` carries a path-specific field (the
    de-id sentinel's `deid`).

    Args:
        reason (str): The halt reason token (a kebab-string from the reason vocabulary).
        dispatch_count (int): The aggregate dispatch count reached at the halt.
        deidentified (bool, optional): The de-id state — False only on the de-id-sentinel halt.

    Returns:
        (dict) The honest no-plan state.
    """
    return {
        "deidentified": deidentified,
        "reason": reason,
        "results": {},
        "dvq_entries": [],
        "dispatch_count": dispatch_count,
        **extra,
    }


def _promote_plans(scratch_root, root):
    """Promote the surfaced pass's `plan::` / `dvq::` rows from the scratch store into `root`.

    The autonomous loop drives the inner engine against an ISOLATED scratch store each pass (the
    inner engine writes plan rows as it generates, BEFORE the whole-plan gate runs), so a blocked
    plan never touches the rendered `root`. When the gates SURFACE a plan, its survivors are promoted
    here: each `plan::` / `dvq::` row the inner engine wrote into `scratch_root` is appended to
    `root` through the SAME `store.append` surface (inheriting the store-keying `(item, timepoint,
    source)` dedupe — a re-promoted identical row is idempotent). The operator state already lives in
    `root`; only the inner engine's generated plan / queue streams promote.

    EVERY read completes BEFORE any write: the `(item, reading)` pairs are collected from the scratch
    store first, then appended into `root`. And the affected `root` item files are snapshotted (their
    prior on-disk bytes, or absence) before the first append, so a write OSError mid-append RESTORES
    each touched file to its pre-promote state before re-raising — the real store is never left with
    a half-promoted plan set (the caller's guard then routes the re-raise to a `PROMOTE_FAILED`
    honest no-plan halt). SEC-01.

    Args:
        scratch_root (str | Path): The surfaced pass's scratch store root.
        root (str | Path): The real store root the surfaced plans promote into.
    """
    pairs = []
    for item in store.items(scratch_root):
        if not (item.startswith("plan::") or item.startswith("dvq::")):
            continue
        for reading in store.read(item, root=scratch_root):
            pairs.append((item, reading))

    # Snapshot the pre-promote on-disk state of every item file this promote will touch, so a
    # mid-append OSError can roll the real store back to where it was (no half-promoted set).
    affected = {store._item_path(item, root) for item, _ in pairs}
    snapshot = {p: (p.read_bytes() if p.exists() else None) for p in affected}
    try:
        for item, reading in pairs:
            store.append(item, reading, root=root)
    except OSError:
        for path, prior in snapshot.items():
            if prior is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(prior)
        raise
