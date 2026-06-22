"""By-data-class capture persistence (ADR-0014-T1).

`persist_capture(fields, *, root, scaffold_root, identity_config)` routes each
submitted intake form field BY ITS DATA CLASS, the load-bearing classification the
ADR-0014 PII boundary rests on:

- A wired de-identified `SUMMARY_FIELD_SET` token (`goal-domains`, `goal-targets`,
  `goal-priority-order`, `hard-limits`, `recovery-status-band`, `rx-interaction-classes`)
  -> the time-series store via the UNCHANGED `store.append`, item named EXACTLY as the
  token, tagged `source:"intake"`. The seam REUSES `store.append` — it never
  re-implements the NDJSON write/dedupe (that would fork the surface the store-adversarial
  battery protects).
- The Step-3 "train around / injury" free-text -> a `raw-symptom-free-text` store item
  (the RAW item `router.summarize` DE-IDENTIFIES into `active-issue-class`), NEVER
  `active-issue-class` directly.
- A record-only / raw value (Step-3 training detail, all Step-4 nutrition, the raw Step-5
  supplement/peptide stack) -> the gitignored `vault/scaffold/filled/` operator record,
  honestly labeled "for your record". NEVER a `SUMMARY_FIELD_SET` store item — a raw drug
  name is named-excluded PII, never `rx-interaction-classes` (which carries only curated
  de-identified class tokens).

`rx-interaction-classes` is written ONLY from the form's supplied de-identified class
tokens; there is no raw-drug-name -> class lookup in this module (the de-identification is
an operator/liaison CURATION step at the store layer per `router.py`, not serve-layer code).
The `router.summarize` 8j6 PII gate is the runtime backstop that fail-closes if raw PII
ever reaches a field-set item.
"""

import datetime
from pathlib import Path

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
    "rx-interaction-classes",
)

# The Step-3 "train around / injury" form field -> the RAW-symptom store item
# `summarize` de-identifies into `active-issue-class`. Written to the store (it is the
# derivation INPUT, a named-excluded raw-PII class), never as a field-set token.
_TRAIN_AROUND_FIELD = "train-around"
_RAW_SYMPTOM_ITEM = "raw-symptom-free-text"

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
        identity_config (str | Path, optional): Accepted for the published-surface
            contract (the boundary's identity config); the runtime PII backstop is
            `router.summarize`'s 8j6 gate, not enforced here — this seam ROUTES by data
            class so raw PII never reaches a field-set item in the first place.

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
        if name in WIRED_TOKENS:
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
