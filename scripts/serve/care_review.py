"""Care-agent review-on-final-save + de-associated meds curation (ADR-0033-0035-T8).

The SECOND named model-egress surface this ADR set adds (after T2's de-associated demographic
facts): the care-agent review fired at the intake unlock transition. It has TWO legs, BOTH
crown-jewel load-bearing (NFR-1):

1. The clarifying-review leg — `review` builds the DE-IDENTIFIED `router.summarize` profile (the
   same summary the planner consumes, 0-raw-PII by the router 8j6 gate) and makes ONE
   `client.converse` call carrying ONLY that de-id profile — 0 full-DOB, 0 raw drug string, 0
   legal name — to produce >= 1 Care-Assistant clarifying question.
2. The de-associated meds-curation leg — a DISTINCT, meds-only `converse` request built by this
   module's OWN builder (NOT `chat._model_messages`, the 0-store-content intake-turn builder): it
   carries the operator's raw drug NAMES (the record-only meds T1 routes to the gitignored
   scaffold) but 0 operator-identity token + 0 name<->med linkage, and proposes the de-identified
   `rx-interaction-classes` CLASS token. Confirm-when-unsure: an uncertain proposal writes 0
   `rx-interaction-classes` store items until the operator confirms (`confirm_curation`); only a
   confident/confirmed CLASS token — never a raw drug string — persists as the planner input.

The review REUSES the injected `ModelClient` (`client`) — it constructs no second `ModelClient`,
imports no model-client SDK, opens no outbound HTTP client. With no resolvable key
(`key_available=False`) it degrades HONESTLY: 0 model call, an honest deferred state, never a
silent empty or a fabricated question.

DEFERRED (documented, NOT run here): the operator-present LIVE care-agent run — a real no-train
key + real spend, end-to-end through final-save -> de-id review -> questions-in-thread + meds
curation — is ADR-0035 OQ-1, operator-gated. The tests exercise this module with a recording mock
backend injected at the ADR-0015 model-client backend seam, at 0 live spend.
"""

import datetime
import json
import re
from pathlib import Path

from scripts.guard import pii_scan
from scripts.model.client import ModelCallError
from scripts.plan import router
from scripts.serve.capture import DEFAULT_SCAFFOLD_ROOT
from scripts.store import store

# The record-only medication FORM field T1 routes into the gitignored operator-record scaffold
# (capture.py: deliberately absent from WIRED_TOKENS, so the untrusted raw drug free-text lands
# record-only, never the model-bound token). The curation reads the raw drug names from here.
_RX_MED_FIELD = "rx-interaction-classes"

# The leg-2 DOB fail-closed pattern (Security MEDIUM-2): `pii_scan` carries no date-of-birth
# detector, so a bare `1986-04-12` typed into the med free-text would egress undetected by the
# value-class scan alone. A drug name legitimately never contains a date, so any ISO or slashed
# date token in a med value is treated as identity and fails the curation closed (defers). The
# pattern is deliberately conservative — an ISO `YYYY-MM-DD` or a slashed `D/M/Y` / `M-D-Y`.
_DATE_LIKE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")


def review(store_read, *, client, key_available, store_root=None,
           scaffold_root=None, identity_config=None):
    """Run the care-agent review over a complete profile; return the review receipt.

    Args:
        store_read (Callable): The instance-root-bound `store.read` partial (the
            `router.summarize` caller contract) the de-id profile is derived from.
        client: The REUSED `ModelClient` (exposing `converse(messages)`); constructed by the
            caller, never here.
        key_available (bool): Whether a no-train key resolves — the `_key_available()` bool. False
            -> the honest 0-spend deferred state (no model call).
        store_root (str | Path, optional): The store root the CONFIRMED class token writes into.
        scaffold_root (str | Path, optional): The gitignored operator-record root the curation
            reads the record-only raw meds from.
        identity_config (str | Path, optional): The operator-identity token config threaded into
            `router.summarize`'s 8j6 PII gate.

    Returns:
        (dict) The review receipt: `questions` (>= 1 clarifying question on a keyed complete
        profile), `curation` (the proposed/confirmed `rx-interaction-classes` state + a confirm
        flag, or None when no med is recorded), `progress` (the "what it is doing" status the
        existing `.chat-progress`/`.bar` surface renders), and `deferred` (True with a `reason` on
        `key_available=False` or a failed model call).
    """
    if not key_available:
        return _deferred("no-train key not connected; care review deferred (0 model spend)")
    if identity_config is not None:
        summary = router.summarize(store_read, identity_config=identity_config)
    else:
        summary = router.summarize(store_read)
    try:
        reply = client.converse(_clarifying_messages(summary))
    except ModelCallError as exc:
        # Leg 1 failed before any clarifying question was produced — nothing paid-for to keep.
        # Fail-closed (NFR-2): surface honestly, mirroring chat._degraded_turn.
        return _deferred(str(exc))
    try:
        curation = _curate_meds(client, scaffold_root, store_root, identity_config)
    except ModelCallError as exc:
        # Leg 2 failed AFTER leg 1 already produced (and paid for) its clarifying question. Keep
        # the leg-1 questions and surface a deferred-curation SUB-state — never discard the paid
        # leg-1 reply by returning a total-deferred receipt with empty questions.
        curation = {
            "deferred": True,
            "reason": str(exc),
            "proposed_classes": [],
            "confirmed": False,
            "confirm_question": None,
        }
    return {
        "deferred": False,
        "questions": [reply["reply"]],
        "reply": reply["reply"],
        "curation": curation,
        # The final-save fire path: the profile IS complete (the trigger's precondition), so the
        # status reflects the true complete state the existing `_progressUpdate` surface renders.
        "progress": _progress("Reviewing your intake and preparing clarifying questions",
                              intake_complete=True),
    }


def confirm_curation(class_tokens, *, store_root=None, identity_config=None):
    """Persist the operator-CONFIRMED `rx-interaction-classes` class tokens (the confirm write).

    The follow-up to an uncertain curation: only after the operator confirms does the de-identified
    class token persist as the planner input. Names/de-dupes/normalizes the class tokens and writes
    the single `;`-joined scalar through the UNCHANGED `store.append`.

    Crown-jewel value gate (symmetric with the auto-persist `_curate_meds` path): `rx-interaction-classes`
    is a model-bound `SUMMARY_FIELD_SET` token whose only downstream backstop is `summarize`'s 8j6
    `pii_scan.scan_text`, which carries NO date detector. So this confirm write-back runs the SAME
    `_med_value_has_identity` gate (`pii_scan.scan_text_full` + the `_DATE_LIKE` DOB backstop) that
    `_curate_meds` runs before any value crosses: if ANY submitted token carries operator identity/contact
    or a DOB-shaped date, the WHOLE batch defers (persists nothing) — fail-closed, no leaky prefix. This
    matters because `confirm_curation` is network-reachable (POST `/confirm-curation`): the legitimate UI
    only ever posts the model's de-identified class proposals, but a crafted loopback POST must not land a
    raw DOB the planner would then consume.

    Args:
        class_tokens (iterable[str]): The confirmed de-identified interaction-class tokens.
        store_root (str | Path, optional): The store root to write into.
        identity_config (str | Path, optional): The operator-identity token config threaded into the
            value gate (the same seam the route passes `self.identity_config` through); None falls
            through to `pii_scan`'s default (the `_DATE_LIKE` DOB backstop applies regardless).

    Returns:
        (dict) `{"confirmed": [tokens]}` on success; `{"confirmed": [], "deferred": True, "reason": ...}`
        when a token carried identity/DOB (nothing persists) or when there is nothing to persist.
    """
    raw = [str(tok) for tok in class_tokens if tok and str(tok).strip()]
    if any(_med_value_has_identity(tok, identity_config) for tok in raw):
        # Fail-closed (mirrors _curate_meds): 0 persist, an honest deferred state — never a leaky prefix.
        return {"confirmed": [], "deferred": True,
                "reason": ("a confirmed interaction class carried personal details (a name, date of "
                           "birth, email, phone, or address); nothing was recorded")}
    tokens = _normalize_classes(class_tokens)
    if not tokens:
        return {"confirmed": []}
    _persist_classes(tokens, store_root)
    return {"confirmed": tokens}


def _clarifying_messages(summary):
    """Build the clarifying-review converse request from the de-id summary ONLY (leg 1).

    A care_review-LOCAL builder — NOT `chat._model_messages` (the 0-store-content intake-turn
    builder). Carries ONLY the de-identified `summarize` profile, 0 raw scaffold content.
    """
    context = {"task": "care-clarifying-review", "profile": summary}
    return [{"role": "user", "content": json.dumps(context, sort_keys=True)}]


def _curation_messages(medications):
    """Build the DISTINCT meds-curation converse request from drug NAMES only (leg 2).

    A care_review-LOCAL builder (NOT `chat._model_messages`). Carries the operator's raw drug
    names to classify — and NOTHING else: no operator-identity token, no name<->med linkage (the
    caller reads only the record-only med field, never the operator's other fields).
    """
    context = {"task": "rx-interaction-curation", "medications": sorted(medications)}
    return [{"role": "user", "content": json.dumps(context, sort_keys=True)}]


def _curate_meds(client, scaffold_root, store_root, identity_config):
    """The de-associated meds-curation leg: propose the de-id class token, confirm-when-unsure.

    Returns None when no medication is recorded (no curation request is made). Otherwise it FIRST
    runs the leg-2 value-level identity gate — the analogue of leg-1's `router.summarize` 8j6 gate
    (Security HIGH-1 / QA MUST-FIX): `capture` routes the raw med free-text record-only UNSCANNED,
    so a med value carrying operator identity/contact (`pii_scan.scan_text_full`) OR a date-looking
    token (a DOB `pii_scan` cannot detect) must NOT egress. Mirroring leg-1's FAIL-CLOSED posture
    (`summarize` RAISES; it never partial-strips — a partial strip is the leaky de-id the crown
    jewel refuses), the curation DEFERS with 0 `converse` call rather than send a leaky request.
    Only when EVERY med value is clean does it make the DISTINCT curation `converse` call over the
    drug names and read the class proposal: a confident proposal persists the de-identified class
    token; an uncertain one writes 0 and surfaces a confirm question (confirm-when-unsure).
    """
    medications = _scaffold_meds(scaffold_root)
    if not medications:
        return None
    if any(_med_value_has_identity(value, identity_config) for value in medications):
        # Fail-closed: 0 curation converse call, an honest deferred state (no partial strip).
        return {
            "deferred": True,
            "reason": ("remove personal details (a name, date of birth, email, phone, or "
                       "address) from your medication list before I can classify it"),
            "proposed_classes": [],
            "confirmed": False,
            "confirm_question": None,
        }
    result = client.converse(_curation_messages(medications))
    proposals = [p for p in (result.get("extraction") or []) if isinstance(p, dict)]
    proposed = _normalize_classes(
        str(p.get("rx-interaction-class", "")) for p in proposals
    )
    all_confident = bool(proposals) and all(p.get("confident") for p in proposals)
    if all_confident and proposed:
        _persist_classes(proposed, store_root)
        return {"proposed_classes": proposed, "confirmed": True, "confirm_question": None}
    return {
        "proposed_classes": proposed,
        "confirmed": False,
        "confirm_question": _confirm_question(proposed),
    }


def _scaffold_meds(scaffold_root):
    """Read the record-only raw drug names from the LATEST operator-record capture (T1).

    Each capture writes one `capture-<stamp>.json` `{field: value}` file; the record-only med
    field is `rx-interaction-classes` (the raw drug free-text). Reads ONLY the LATEST capture's
    med field (the newest by the timestamp-sorted name) — never the union of all history: the
    review re-fires on every complete-profile save, so a union would re-classify the whole
    history each time (repeated spend + duplicate store writes) AND trap the curation forever if
    one HISTORICAL value carried a date the `_DATE_LIKE` gate defers on. Latest-only bounds spend
    to the current med state and lets a later clean capture recover from a prior dated one. Reads
    ONLY the med field — never the operator's other captured fields — so the curation request
    cannot carry operator identity.
    """
    root = Path(scaffold_root) if scaffold_root is not None else DEFAULT_SCAFFOLD_ROOT
    if not root.exists():
        return []
    captures = sorted(root.glob("capture-*.json"))
    if not captures:
        return []
    try:
        data = json.loads(captures[-1].read_text())
    except (OSError, ValueError):
        return []
    if not isinstance(data, dict):
        return []
    value = data.get(_RX_MED_FIELD)
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _med_value_has_identity(value, identity_config):
    """Whether a raw med value carries operator identity/contact (pii_scan) or a DOB-like date.

    The leg-2 fail-closed value gate. Runs the full-length `pii_scan.scan_text_full` (operator
    identity + the tractable value-classes — any-domain email, phone, US/CA postal) over the med
    free-text, PLUS the `_DATE_LIKE` DOB backstop (`pii_scan` has no date detector). True on any
    hit — the caller defers the curation rather than egress a leaky de-identified request.
    """
    if identity_config is not None:
        hits = pii_scan.scan_text_full(value, token_config=identity_config)
    else:
        hits = pii_scan.scan_text_full(value)
    return hits > 0 or bool(_DATE_LIKE.search(value))


def _normalize_classes(tokens):
    """Sort, dedupe, lowercase, and drop-empty a set of interaction-class tokens."""
    return sorted({tok.strip().lower() for tok in tokens if tok and tok.strip()})


def _persist_classes(class_tokens, store_root):
    """Write the de-identified `rx-interaction-classes` scalar via the UNCHANGED store.append."""
    token = ";".join(_normalize_classes(class_tokens))
    if not token:
        return
    root = store_root if store_root is not None else store.DEFAULT_ROOT
    reading = {
        "item": router.RX_INTERACTION_CLASS_FIELD,
        "timepoint": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "care-review",
        "value": token,
    }
    store.append(router.RX_INTERACTION_CLASS_FIELD, reading, root=root)


def _confirm_question(proposed):
    """The confirm-when-unsure question surfaced for an uncertain classification (0 auto-write)."""
    if proposed:
        return (
            "I could not classify your medications with confidence. Please confirm whether these "
            f"interaction classes apply before I record them: {', '.join(proposed)}."
        )
    return (
        "I could not classify your medications with confidence. Please confirm your medication "
        "interaction classes before I record them."
    )


def _deferred(reason):
    """The honest deferred state: 0 model call, 0 fabricated question, an explicit reason."""
    return {
        "deferred": True,
        "reason": reason,
        "questions": [],
        "curation": None,
        "progress": _progress("Care review deferred — no model call made"),
    }


def _progress(status, intake_complete=False):
    """The 'what it is doing' status the existing `.chat-progress`/`.bar` + `_progressUpdate` surface renders.

    `intake_complete` reflects the TRUE profile-completeness state (QA SHOULD-FIX): the final-save
    fire path passes True (the trigger only fires on a complete profile), so `_progressUpdate`
    renders the ready-to-generate state rather than a stale "still building" one; the deferred
    (no-key / failed-call) states keep it False.
    """
    return {"status": status, "intake_complete": intake_complete, "target_domain": None}
