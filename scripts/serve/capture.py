"""By-data-class capture persistence (ADR-0014-T1).

`persist_capture(fields, *, root, scaffold_root, identity_config)` routes each
submitted intake form field BY ITS DATA CLASS, the load-bearing classification the
ADR-0014 PII boundary rests on:

- A wired de-identified `SUMMARY_FIELD_SET` token (`goal-domains`, `goal-targets`,
  `goal-priority-order`, `hard-limits`, `recovery-status-band`)
  -> the time-series store via the UNCHANGED `store.append`, item named EXACTLY as the
  token, tagged `source:"intake"`. The seam REUSES `store.append` — it never
  re-implements the NDJSON write/dedupe (that would fork the surface the store-adversarial
  battery protects). `rx-interaction-classes` is a SUMMARY_FIELD_SET token but is NOT
  wired here (Wave-B FIX-A): its model-bound form is liaison-curated, so the untrusted
  form field routes record-only instead (see the WIRED_TOKENS note below).
- The Step-3 "train around / injury" free-text -> a `raw-symptom-free-text` store item
  (the RAW item `router.summarize` DE-IDENTIFIES into `active-issue-class`), NEVER
  `active-issue-class` directly.
- A record-only / raw value (Step-3 training detail, all Step-4 nutrition, the raw Step-5
  supplement/peptide stack, the Step-5 rx-interaction text) -> the gitignored
  `vault/scaffold/filled/` operator record, honestly labeled "for your record". NEVER a
  `SUMMARY_FIELD_SET` store item — a raw drug name is named-excluded PII, never the
  model-bound `rx-interaction-classes` item (which carries only curated de-identified
  class tokens).

There is no raw-drug-name -> class lookup in this module: de-identification is an
operator/liaison CURATION step at the store layer per `router.py`, not serve-layer code,
and the untrusted rx form field is captured record-only (Wave-B FIX-A) rather than wired
into the model-bound item. The `router.summarize` 8j6 PII gate is the runtime backstop
that fail-closes if raw PII ever reaches a field-set item.
"""

import datetime
from pathlib import Path

from scripts.guard import pii_scan
from scripts.plan.router import SUMMARY_FIELD_SET
from scripts.store import store

# The default gitignored operator-record root (ADR-0005 forward convention). A record-only
# value writes under here; it is NEVER added to git (`block-pii-commit` denies a staged
# value, and the prefix is in `.gitignore`). Tests pass a tmp `scaffold_root` instead.
DEFAULT_SCAFFOLD_ROOT = Path("vault/scaffold/filled")

# The de-identified wired tokens the capture form writes to the store, each keyed by the
# FORM FIELD NAME the markup submits. The value is the SUMMARY_FIELD_SET token the store
# item is named for (here identical to the field name — the pass-through tokens read from
# a store item of their own name). The load-time tripwire below pins every token into the
# field set, mirroring router.py's disjointness asserts: a wired token dropped from the
# field set trips at import, never silently writes a novel store item.
WIRED_TOKENS = (
    "goal-domains",
    "goal-targets",
    "goal-priority-order",
    "hard-limits",
    "recovery-status-band",
)
# `rx-interaction-classes` is DELIBERATELY ABSENT from the wired set (Wave-B FIX-A).
# Its store item IS a SUMMARY_FIELD_SET member, but the model-bound token may carry
# only liaison-CURATED de-identified class tokens. The capture FORM field collects
# operator-typed text the server cannot trust to be de-identified (a raw drug name +
# dose would route verbatim into the model-bound item, and the `pii_scan` value gate
# does not catch drug names). So the form field routes RECORD-ONLY to the gitignored
# scaffold; the curation surface that emits real class tokens is the beaded ADR-0014
# OQ-2 future consumer, not this serve-layer seam.

# The Step-3 "train around / injury" form field -> the RAW-symptom store item
# `summarize` de-identifies into `active-issue-class`. Written to the store (it is the
# derivation INPUT, a named-excluded raw-PII class), never as a field-set token.
_TRAIN_AROUND_FIELD = "train-around"
_RAW_SYMPTOM_ITEM = "raw-symptom-free-text"

# Server-side enumerated value sets for the bounded wired fields (Wave-B FIX-B). The
# markup enforces these client-side (a `<select>` / a fixed chip set), but a crafted
# POST can write any string into the token — so the server re-validates here BEFORE
# `store.append`. `intake.py` builds its `<select>`/chips from these same constants so
# the markup and this gate cannot drift. An out-of-set value is routed RECORD-ONLY to
# the gitignored scaffold (never garbage into the model-bound token). Matching is
# case-insensitive on the stripped value; `goal-domains` is a `;`-joined multi-value,
# so EVERY token must be in the enum for the whole value to be accepted.
RECOVERY_STATUS_BANDS = ("low", "moderate", "high")
GOAL_DOMAINS = ("Workout", "Nutrition", "Supplements", "Peptides")
_BOUNDED_ENUMS = {
    "recovery-status-band": ({b.lower() for b in RECOVERY_STATUS_BANDS}, False),
    "goal-domains": ({d.lower() for d in GOAL_DOMAINS}, True),
}


# The free-text wired tokens (operator-typed prose, not a bounded enum). Their full
# value is PII-scanned on the capture path before it is written to the model-bound
# token (Wave-B FIX-C): `pii_scan.scan_text` caps a single call at 4096 chars, so a
# value longer than that could carry PII past the cap that the single 8j6 gate misses.
# Accepted V1 residual: an operator deliberately typing a diagnosis into a goals field
# is NOT caught here — the field is FOR de-identified goal text, the model path is
# no-train, and a clinical-PHI detector is out of scope. The UI field carries guidance.
_FREE_TEXT_TOKENS = ("goal-targets", "hard-limits", "goal-priority-order")


def _value_has_pii(value, identity_config):
    """Whether a free-text value carries operator PII anywhere in its FULL length.

    `pii_scan.scan_text` caps at `_MAX_SCAN_TEXT_LEN`, so a long value could hide PII
    past the cap. The earlier fix windowed the value into overlapping ≤cap chunks, but
    two value-PII patterns — `email` (unbounded local/domain) and `postal-street-zip`
    (unbounded street-name word) — have no finite maximum match span, so NO fixed
    overlap can provably contain every match in some window: a long postal straddling
    a window step boundary is seen whole by neither window and leaks past the gate.
    Instead this scans the value in a SINGLE non-truncating pass via
    `pii_scan.scan_text_full`, which has no window boundaries to straddle. Scoped to the
    capture path — it does NOT change `scan_text`'s own default cap (which has other
    callers); the capture-path values are bounded operator form fields.

    Args:
        value (str): The free-text field value to scan in full.
        identity_config (str | Path | None): The operator-identity token config passed
            to `scan_text_full`; None falls through to its default.

    Returns:
        (bool) True when the full value scans positive for operator PII.
    """
    if identity_config is None:
        return pii_scan.scan_text_full(value) > 0
    return pii_scan.scan_text_full(value, token_config=identity_config) > 0


def _bounded_value_ok(name, value):
    """Whether a bounded field's value is within its server-side enum (Wave-B FIX-B).

    Args:
        name (str): The wired field name (only `_BOUNDED_ENUMS` members are bounded).
        value (str): The submitted value (a scalar; `goal-domains` is `;`-joined).

    Returns:
        (bool) True when `name` is unbounded, or every token of `value` is in the enum.
        A `goal-domains` with any out-of-set token, a separators-only `goal-domains`
        (no in-enum token at all), or a `recovery-status-band` not in the band set, is
        False (-> routed record-only).
    """
    enum = _BOUNDED_ENUMS.get(name)
    if enum is None:
        return True  # not a bounded field — no enum to check
    allowed, multi = enum
    raw_tokens = value.split(";") if multi else [value]
    # A separators-only value (";;;") filters to an EMPTY list — `all()` over nothing is
    # vacuously True, which would write garbage into the model-bound token. Require at
    # least one non-empty token, AND every one of them in the enum.
    tokens = [tok.strip().lower() for tok in raw_tokens if tok.strip()]
    return bool(tokens) and all(tok in allowed for tok in tokens)

# Load-time tripwire (mirrors router.py's change-control asserts): every wired token must
# be a SUMMARY_FIELD_SET member. A field-set edit that drops a wired token reds this at
# import — the operator never reaches a runtime that writes a novel item the consumer rejects.
assert set(WIRED_TOKENS) <= set(SUMMARY_FIELD_SET), (
    "capture.WIRED_TOKENS carries a token absent from router.SUMMARY_FIELD_SET — "
    "the field map is stale (re-ground per the ADR-0014 review trigger)"
)


def _now():
    """The UTC-offset timepoint a store reading carries (the store's producer obligation)."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _reading(item, value):
    """Build a conformant store reading for a captured value, tagged source:"intake"."""
    return {"item": item, "timepoint": _now(), "source": "intake", "value": value}


def _write_scaffold(scaffold_root, fields):
    """Write the record-only fields to the gitignored operator record.

    Writes ONE JSON file per capture under `scaffold_root` (created on first write —
    this task is the first producer of the ADR-0005 forward convention). The record-only
    values legitimately live here (gitignored + `block-pii-commit`-guarded); they NEVER
    reach a `store.append`.

    Args:
        scaffold_root (Path): The gitignored operator-record root.
        fields (dict): The record-only field name -> value pairs.
    """
    import json

    root = Path(scaffold_root)
    root.mkdir(parents=True, exist_ok=True)
    # A per-capture file named by the capture timepoint (collision-safe, append-only record).
    stamp = _now().replace(":", "-")
    (root / f"capture-{stamp}.json").write_text(json.dumps(fields, indent=2) + "\n")


def persist_capture(fields, *, root=None, scaffold_root=None, identity_config=None):
    """Route and persist each submitted intake field by its data class.

    Args:
        fields (dict): The submitted form fields (name -> value), as parsed into
            `stage_uploads`'s `fields` dict.
        root (str | Path, optional): The store root the wired tokens append into.
            Defaults to `store.DEFAULT_ROOT` (`vault/store/`).
        scaffold_root (str | Path, optional): The gitignored operator-record root the
            record-only values write under. Defaults to `vault/scaffold/filled/`.
        identity_config (str | Path, optional): The operator-identity token config for
            the free-text full-value PII scan (Wave-B FIX-C); threaded into
            `pii_scan.scan_text`. The seam ROUTES by data class so raw PII never reaches
            a field-set item; `router.summarize`'s 8j6 gate remains the runtime backstop.

    Returns:
        (dict) The routing outcome: `{"store": [tokens written], "scaffold": [field
        names recorded]}` — a thin receipt the handler can re-render against.
    """
    store_root = root if root is not None else store.DEFAULT_ROOT
    scaffold = scaffold_root if scaffold_root is not None else DEFAULT_SCAFFOLD_ROOT

    written_tokens = []
    record_only = {}
    for name, value in fields.items():
        if value is None or (isinstance(value, str) and not value.strip()):
            continue  # an unfilled field carries nothing to route
        if name in WIRED_TOKENS and not _bounded_value_ok(name, value):
            # A crafted out-of-enum value for a bounded field (recovery-status-band /
            # goal-domains) — do NOT write garbage into the model-bound token. Route it
            # record-only to the gitignored scaffold (Wave-B FIX-B).
            record_only[name] = value
        elif name in _FREE_TEXT_TOKENS and _value_has_pii(value, identity_config):
            # A free-text wired token whose FULL value carries operator PII (caught past
            # scan_text's 4096-char cap, Wave-B FIX-C) — route it record-only, never into
            # the model-bound token where PII past the single 8j6 gate's cap would evade.
            record_only[name] = value
        elif name in WIRED_TOKENS:
            # A wired de-identified token -> the store under its own name, source:"intake".
            store.append(name, _reading(name, value), root=store_root)
            written_tokens.append(name)
        elif name == _TRAIN_AROUND_FIELD:
            # The "train around" free-text -> the RAW-symptom item summarize de-identifies
            # into active-issue-class. NEVER active-issue-class directly.
            store.append(_RAW_SYMPTOM_ITEM, _reading(_RAW_SYMPTOM_ITEM, value), root=store_root)
            written_tokens.append(_RAW_SYMPTOM_ITEM)
        else:
            # Everything else is record-only: it has no de-identified field-set consumer
            # today (Step-3 training detail, all Step-4 nutrition, the raw Step-5 stack).
            # -> the gitignored scaffold, honestly labeled. NEVER a field-set store item.
            record_only[name] = value

    if record_only:
        _write_scaffold(scaffold, record_only)

    return {"store": written_tokens, "scaffold": sorted(record_only)}
