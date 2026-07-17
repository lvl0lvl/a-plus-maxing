"""The metered specialist-author dispatch seam — the metered-lane analog of subscription_dispatch (ADR-0049-T1).

`build_dispatch(client)` adapts an injected metered-lane model client into the
`dispatch(name, prompt, context) -> author envelope` seam (`plan_orchestrator._dispatch_domains`). It
serves ONLY the SPECIALIST name-space: it routes the call through the client's `.author(name, context)`
— authenticating on the shared `a-plus-maxing-api-key` metered lane (`key_source.resolve` through
`_ClaudeNoTrainBackend`) — and `ModelClient.author` ALWAYS returns a plan-author envelope, never a
`quality-judge` per-dimension score-map nor a safety-lens findings-list. So this factory is NOT wired
as the live `loop_dispatch`: the built loop's `dispatch(name, ...)` seam is a THREE-name-space
aggregate (a specialist / `plan_loop.JUDGE_ROLE` / a `safety_review.DEFAULT_LENSES` lens — `plan_loop`
asserts the three are pairwise disjoint), and the judge/lens name-spaces need a metered gate-dispatch
surface that does not exist yet (bead: metered loop_dispatch needs a judge/lens surface). It reads no
store, de-identifies nothing, and re-hosts no loop logic: the already-de-identified `context` (the
summary) is the ONLY operator-state that crosses (the de-id-IN happens INSIDE the loop, upstream).

Gate-blindness (a bounded asymmetry — recorded, not "fixed"): the pre-built role-inlined `prompt` (the
subscription lane's subprocess input — the role profile + the summary + the `## Active gates` block,
`plan_orchestrator._dispatch_prompt`) is DISCARDED here; `ModelClient.author` builds its own metered
prompt from `(domain, summary)`, so the metered author never sees the `## Active gates` block — it is
gate-blind. This is SOUND today: gates are forwarded independently to the deterministic composer
(`run_generation`, `plan_orchestrator.py`), so gate enforcement is downstream + author-independent,
and the live loop path OMITS `run_orchestrated(gates=...)` (it defaults all-conservative), so no real
gates flow to either author and the divergence is dormant. It BREAKS IF a future task populates
`run_orchestrated`'s `gates=` on the loop path: the subscription author would see them, the metered
author silently would not — an author-visible-safety-context divergence to reconcile then.

The module imports NO `scripts.store` symbol (mirror `subscription_dispatch`'s import set): the
adapter closure captures only `client` — no store handle, no `raw_intake` handle — the structural half
of the 0-store-read guarantee (the module-level spy + mutant in the D2 wire-scan is the
non-tautological backstop). Module import fires 0 side effects (0 dispatch, 0 key resolve, 0 model
call) — importing the seam arms nothing.
"""

from scripts.serve.intake_aggregate import normalize_author_output


def build_dispatch(client, *, spend_cap=None):
    """Adapt a metered-lane model client into the built loop's unified dispatch seam.

    Returns the `dispatch(name, prompt, context) -> author envelope` seam
    (`plan_orchestrator._dispatch_domains`): each specialist / judge / lens call is routed through
    `client.author(name, context)` on the shared-key metered lane, and a specialist AUTHOR envelope's
    scalar-contract recommendation fields are normalized to the frozen composer's shape
    (`normalize_author_output`, bead mk0i — a list/dict-valued rec field otherwise crashes the frozen
    `assemble` mid-run; idempotent here since `ModelClient.author` already normalizes at its boundary,
    applied for mirror parity + to cover a non-`ModelClient` recording client, and a no-op on the
    judge/lens verdict shapes). The pre-built `prompt` is DISCARDED (gate-blindness, see the module
    docstring): only the de-identified `context` crosses. Reads no store, de-identifies nothing,
    re-hosts no loop logic.

    When a `spend_cap` is injected (ADR-0049-T3), the dispatch closure consults it (`spend_cap.charge()`)
    BEFORE each outbound `client.author(...)` — a `spend_cap.SpendCapExceeded` (a
    `dispatch_budget.DispatchCapExceeded` subclass) then propagates fail-closed and the outbound metered
    call is never issued. `spend_cap=None` (the default) issues NO consult, so the ADR-0049-T1 D2 tests
    are byte-for-byte unchanged. This adds 0 outbound field and 0 `scripts.store` read (the cap reads
    its own ledger). The metered loop is NOT armed in production today; the arming task (bead
    `a-plus-maxing-23xr`) MUST inject a real cap here — the `run_orchestrated` cap-halt catch
    (`plan_orchestrator.py:314`) is already satisfied because `SpendCapExceeded` subclasses
    `DispatchCapExceeded`, so a monthly-cap refusal surfaces honest-no-plan rather than crashing.

    Args:
        client: The metered-lane model client, `client.author(name, context) -> envelope` (a real
            `ModelClient` in production authenticating via the shared `a-plus-maxing-api-key`; a
            fixture recording client in tests).
        spend_cap (SpendCap, optional): The injectable per-tester monthly spend cap
            (`scripts.runner.spend_cap.SpendCap`), consulted argless before each dispatch. Default
            `None` -> no consult (the backward-compatible D2 path).

    Returns:
        (Callable) The `dispatch(name, prompt, context)` seam the built loop consumes.
    """
    def dispatch(name, prompt, context):
        # Consult the injected monthly spend cap BEFORE the outbound call so a refusal fail-closes
        # before the metered author is invoked (the SpendCapExceeded propagates to the run's cap-halt
        # handler). Default-OFF (`spend_cap is None`) keeps the D2 path byte-unchanged.
        if spend_cap is not None:
            spend_cap.charge()
        # The metered author builds its own prompt from (name, context); the pre-built role-inlined
        # `prompt` is DISCARDED (gate-blindness, module docstring). Normalize the model AUTHOR
        # envelope's scalar rec fields to the frozen `assemble` shape UPSTREAM of run_orchestrated
        # (bead mk0i); a no-op on judge/lens verdicts.
        return normalize_author_output(client.author(name, context))

    return dispatch
