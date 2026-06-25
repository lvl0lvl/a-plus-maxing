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

from scripts.guard import pii_scan
from scripts.model.client import ModelCallError
from scripts.plan.router import SUMMARY_FIELD_SET

# The honest no-plan reason when the de-id-IN model call fails (ADR-0020 fail-closed): the
# client raised `ModelCallError`, so there is no de-identified summary — the orchestrator
# halts to the honest no-plan state and dispatches nothing. Mirrors the VOCABULARY of
# `generate_plan.AUTHOR_CALL_FAILED`; the de-id-IN sentinel is UPSTREAM of any per-domain
# dispatch, so it carries no domain/section (Interface Contracts: the de-id-IN honest-no-plan
# shape, distinct from the per-domain author-failure record). ADR-0020-T2 reuses this same
# sentinel shape for the whole-run-outage halt (a distinct `reason`).
DEID_CALL_FAILED = "deid-call-failed"

# The honest no-plan reason when an IN-field-set summary VALUE carries raw operator PII (SEC-1):
# the key whitelist below checks field NAMES, but a faithless de-id call can pass the whitelist
# yet echo raw PII into an allowed field's VALUE. The boundary value-scans every value and fails
# closed to this sentinel on any hit — distinct from `DEID_CALL_FAILED` so a faithless-model PII
# injection is diagnosable apart from a benign outage. The orchestrator treats it identically
# (the `deidentified` discriminator is the load-bearing key).
DEID_VALUE_PII = "deid-value-pii"


def deid_in(raw_intake, client, identity_config=pii_scan.DEFAULT_IDENTITY_CONFIG):
    """De-identify the raw operator plan-intake through the injected no-train client.

    Routes the de-id call through `client.deidentify(raw_intake)` and returns the
    de-identified summary the orchestrator consumes. Uses ONLY the injected client (constructs
    no second `ModelClient`, opens no SDK path); holds the raw intake in memory and writes
    nothing to a tracked path. Fail-closed: ANY exception from the de-id call (not only
    `ModelCallError`) becomes the honest no-plan sentinel — never a fabricated or partial
    summary, never a passthrough of `raw_intake`, never a raw-bearing traceback (the exception
    TYPE name is recorded for diagnosis; its message/args — which can carry raw — are not).

    The return is a DISCRIMINATED UNION (API-02): either a SUCCESS de-identified summary
    (keyed ONLY by `router.SUMMARY_FIELD_SET`, never carrying `deidentified`) OR the honest
    no-plan sentinel `{"deidentified": False, "reason": DEID_CALL_FAILED}`. `deidentified` is a
    RESERVED key — it is never a `SUMMARY_FIELD_SET` member (enforced by the whitelist below),
    so the orchestrator (ADR-0022-T1) distinguishes success from no-plan by its ABSENCE
    (success) vs PRESENCE (no-plan). The boundary enforces the SAME positive field-set
    whitelist the persisted path (`router.dispatch`) enforces: a summary carrying any
    out-of-set field (raw PII smuggled past a non-faithful de-id call) is rejected — the
    boundary fails closed to the sentinel rather than return the contaminated dict. It
    additionally VALUE-SCANS every in-set field (SEC-1): an allowed field whose VALUE carries
    raw operator PII (identity or contact) — past the key-name whitelist — fails closed to the
    `DEID_VALUE_PII` sentinel, via the NON-TRUNCATING `pii_scan.scan_text_full` (no
    `_MAX_SCAN_TEXT_LEN` straddle hole; the capped `scan_text` gap is sc97).

    Args:
        raw_intake (dict): The raw operator plan-intake (carries raw-PII fields).
        client: An injected model client exposing `deidentify(raw_intake) -> summary` (a real
            `scripts.model.client.ModelClient`, or a `_FixedEnvelopeClient`-style mock in tests).
        identity_config (str | Path, optional): The gitignored operator-identity token file the
            value-scan loads (mirrors `router.summarize`); defaults to
            `pii_scan.DEFAULT_IDENTITY_CONFIG`. Absent → identity detection is empty but the
            value-class patterns (email / phone / postal) still run.

    Returns:
        (dict) The de-identified summary the orchestrator consumes (success), OR the honest
        no-plan sentinel `{"deidentified": False, "reason": DEID_CALL_FAILED, "error_type": ...}`
        on any de-id failure (a raise) or an out-of-field-set (contaminated) summary, OR
        `{"deidentified": False, "reason": DEID_VALUE_PII}` when an in-set field's value carries
        raw PII.
    """
    try:
        summary = client.deidentify(raw_intake)
    except Exception as exc:  # SEC-02: ANY de-id failure fails closed; type, never raw message
        return {
            "deidentified": False,
            "reason": DEID_CALL_FAILED,
            "error_type": type(exc).__name__,
        }
    # FIX 1 (WHITELIST): enforce the positive field-set the persisted path enforces. A summary
    # carrying an out-of-set field (raw PII past a non-faithful de-id) is NOT returned.
    if not isinstance(summary, dict) or not set(summary) <= set(SUMMARY_FIELD_SET):
        return {"deidentified": False, "reason": DEID_CALL_FAILED}
    # SEC-1 (VALUE-SCAN): the whitelist above checks field NAMES; this checks the VALUES. A
    # faithless de-id can pass the key whitelist yet echo raw operator PII into an allowed
    # field's value. Mirror the persisted-side value gate (`router.summarize`'s 8j6 scan) but
    # with the NON-TRUNCATING `scan_text_full` — no `_MAX_SCAN_TEXT_LEN` straddle hole (the
    # crown-jewel boundary; the capped `scan_text` gap is sc97). `str(value)` flattens a
    # non-scalar so STRING PII inside a container is caught too. Name no value (no PII echo).
    # The scan INHERITS `pii_scan`'s value-pattern recall — numeric-typed identifiers (a phone
    # /MRN/lab as a bare JSON number or a 7+-digit run) and two-line `\n`-split postal addresses
    # are residual recall gaps at this boundary, tracked for the real-PII run (beads, SEC-1).
    for value in summary.values():
        if pii_scan.scan_text_full(str(value), token_config=identity_config):
            return {"deidentified": False, "reason": DEID_VALUE_PII}
    return summary
