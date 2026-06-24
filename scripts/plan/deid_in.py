"""The model-backed de-id-IN boundary — the crown-jewel egress gate (ADR-0020-T1).

`deid_in(raw_intake, client)` is the SOLE de-id-IN on the plan path: it takes the raw operator
plan-intake and an INJECTED `ModelClient`, routes the de-id call through `client.deidentify`
(on the no-train backend), and returns the de-identified summary the orchestrator consumes —
the `router.SUMMARY_FIELD_SET`-shaped band/class mapping the inner engine already consumes from
`router.summarize`. It uses ONLY the injected client (constructs no second `ModelClient`, opens
no SDK path) and holds the raw intake in memory — it writes nothing to a tracked path.

This boundary SUPERSEDES `router.summarize` as the sole de-id-IN on the plan path;
`router.summarize` SURVIVES UNCHANGED as the persisted-side de-id (the store-read gate). On a
`ModelCallError` the boundary is fail-closed: it returns the honest no-plan sentinel below,
never a fabricated/partial summary and never a passthrough of the raw intake (NFR-2 / the
crown-jewel containment contract).
"""

from scripts.model.client import ModelCallError

# The honest no-plan reason when the de-id-IN model call fails (ADR-0020 fail-closed): the
# client raised `ModelCallError`, so there is no de-identified summary — the orchestrator
# halts to the honest no-plan state and dispatches nothing. Mirrors the VOCABULARY of
# `generate_plan.AUTHOR_CALL_FAILED`; the de-id-IN sentinel is UPSTREAM of any per-domain
# dispatch, so it carries no domain/section (Interface Contracts: the de-id-IN honest-no-plan
# shape, distinct from the per-domain author-failure record). ADR-0020-T2 reuses this same
# sentinel shape for the whole-run-outage halt (a distinct `reason`).
DEID_CALL_FAILED = "deid-call-failed"


def deid_in(raw_intake, client):
    """De-identify the raw operator plan-intake through the injected no-train client.

    Routes the de-id call through `client.deidentify(raw_intake)` and returns the
    de-identified summary the orchestrator consumes. Uses ONLY the injected client (constructs
    no second `ModelClient`, opens no SDK path); holds the raw intake in memory and writes
    nothing to a tracked path. Fail-closed: a raised `ModelCallError` becomes the honest
    no-plan sentinel `{"deidentified": False, "reason": DEID_CALL_FAILED}` — never a fabricated
    or partial summary, never a passthrough of `raw_intake`.

    Args:
        raw_intake (dict): The raw operator plan-intake (carries raw-PII fields).
        client: An injected model client exposing `deidentify(raw_intake) -> summary` (a real
            `scripts.model.client.ModelClient`, or a `_FixedEnvelopeClient`-style mock in tests).

    Returns:
        (dict) The de-identified summary the orchestrator consumes, OR the honest no-plan
        sentinel `{"deidentified": False, "reason": DEID_CALL_FAILED}` on a `ModelCallError`.
    """
    try:
        return client.deidentify(raw_intake)
    except ModelCallError:
        return {"deidentified": False, "reason": DEID_CALL_FAILED}
