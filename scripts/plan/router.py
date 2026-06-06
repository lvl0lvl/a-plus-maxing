"""No-train router: plan-reasoning summary derivation + payload whitelist gate.

The one PII-touching plan-reasoning dispatch. `summarize` derives a de-identified
summary from store-read state over the closed Summary Field-Set (ADR-0006-T0
spike); `dispatch` routes that summary to the no-train lane and — the load-bearing
security behavior — RAISES on any payload field outside the closed field-set (a
WHITELIST: allow only field-set tokens, reject every field in the complement,
named-excluded raw-PII OR a novel field). The field-set constant below is the
version-controlled source-of-truth for the PII boundary (Security MEDIUM-2); the
field NAMES were supplied by the spike at build time.
"""

# Closed Summary Field-Set (ADR-0006-T0). The single definition of the allowlist
# both `summarize` and `dispatch`'s whitelist check reference — no second copy.
SUMMARY_FIELD_SET = (
    # operator-profile (de-identified)
    "training-age-band",
    "sex-for-dosing",
    "bodyweight-band",
    "equipment-access-class",
    # goals
    "goal-domains",
    "goal-targets",
    "goal-priority-order",
    # current-state (de-identified)
    "recovery-status-band",
    "active-issue-class",
    "hard-limits",
    "recent-trend-direction",
)

# Named-excluded raw-PII fields (ADR-0006-T0). Enumerates the raw-PII the
# derivation strips; the whitelist gate rejects the full out-of-field-set
# complement, of which this is the operationally-relevant subset.
EXCLUDED_RAW_PII = (
    # identity
    "legal-name",
    "date-of-birth",
    "government-id",
    # contact
    "email-address",
    "phone-number",
    "postal-address",
    "geolocation",
    # health-identifier
    "medical-record-number",
    "insurance-id",
    "provider-name",
    "raw-lab-values",
    "raw-symptom-free-text",
    "clinical-notes",
)

# Lane attributes (Constraint D1→ADR-0006: plan summaries route no-train).
NO_TRAIN_LANE = "no-train"
TRAIN_ELIGIBLE_LANE = "train-eligible"

# Raw store item -> field-set field. A field-set field backed by a raw-PII source
# item is derived from it via the band/class transformation; the rest read from a
# store item of the same name. Identity fields (legal-name, etc.) have no entry —
# they are dropped, never reaching the summary.
_RAW_TO_FIELD = {
    "date-of-birth": "training-age-band",
    "postal-address": "equipment-access-class",
    "raw-lab-values": "recent-trend-direction",
    "raw-symptom-free-text": "active-issue-class",
    "clinical-notes": "active-issue-class",
}


class Dispatch:
    """A routed plan-reasoning dispatch, carrying its lane attribute.

    Attributes:
        lane (str): The lane the dispatch was routed to (the no-train lane).
        payload (dict): The model-bound payload (field-set tokens only).
    """

    def __init__(self, lane, payload):
        self.lane = lane
        self.payload = payload


def _age_band(value):
    """Bucket a raw date-of-birth into a coarse training-age band.

    Buckets by birth-decade (minimal sensible boundaries — the spike pins the
    band SHAPE, not exact cutoffs); the raw date never appears in the token.
    """
    year = str(value)[:4]
    return f"born-{year[:3]}0s" if year.isdigit() else "age-band-unknown"


def _trend_token(value):
    """Map a raw lab/reading value to a coarse direction token (no raw value)."""
    text = str(value).lower()
    if any(w in text for w in ("rising", "up", "increase", "high", "out-of-range")):
        return "out-of-range"
    if any(w in text for w in ("falling", "down", "decrease", "low")):
        return "out-of-range"
    return "within-range"


def _issue_class(value):
    """Map raw symptom/clinical free-text to a coarse body-region issue class."""
    text = str(value).lower()
    if any(w in text for w in ("back", "spine", "lumbar")):
        return "back-region"
    if any(w in text for w in ("knee", "leg", "hip", "ankle")):
        return "lower-limb-region"
    if any(w in text for w in ("shoulder", "arm", "elbow", "wrist")):
        return "upper-limb-region"
    return "general-issue"


def _region_class(value):
    """Map a raw postal-address to a coarse presence/region class (no raw value)."""
    return "region-present" if str(value).strip() else "region-absent"


# Per-field-set-field de-identifying derivations for fields backed by a raw-PII
# source item. Each MUST emit a derived band/class token only — the raw value
# never appears in the emitted token (Finding 4-1).
_FIELD_DERIVATION = {
    "training-age-band": _age_band,
    "recent-trend-direction": _trend_token,
    "active-issue-class": _issue_class,
    "equipment-access-class": _region_class,
}

# §5b change-control tripwire (Finding 4-2): every raw source item must be a
# named-excluded raw-PII field, and the field-set must stay disjoint from the
# excluded list. A future edit that adds a raw-PII item to neither structure —
# which would then read through `summarize`'s else-branch under its own name —
# trips this at module load.
assert set(_RAW_TO_FIELD) <= set(EXCLUDED_RAW_PII)
assert set(SUMMARY_FIELD_SET).isdisjoint(set(EXCLUDED_RAW_PII))


def summarize(store_read):
    """Derive the plan-reasoning summary from store-read state.

    Reads operator state through the store read model (`store_read`, the
    `store.read` surface) and no other source, applying the spike's raw-field ->
    summary-token transformation so no named-excluded raw-PII field survives. The
    returned summary is name-addressable: a mapping from each Summary Field-Set
    field name to its de-identified token, carrying only field-set fields.

    Args:
        store_read (Callable): The store read surface (`store.read`), called per
            field-set field to source its backing state.

    Returns:
        (dict) A name-addressable summary keyed by the Summary Field-Set fields.
    """
    summary = {}
    for field in SUMMARY_FIELD_SET:
        # A raw-PII source item backs this field via the band/class map...
        source_items = [raw for raw, f in _RAW_TO_FIELD.items() if f == field]
        if source_items:
            readings = []
            for raw in source_items:
                readings.extend(store_read(raw))
            if readings:
                summary[field] = _FIELD_DERIVATION[field](readings[-1]["value"])
        else:
            # ...otherwise the field reads from a store item of its own name.
            readings = store_read(field)
            if readings:
                summary[field] = readings[-1]["value"]
    return summary


def dispatch(summary, sink=None):
    """Route a summary to the no-train lane after the payload whitelist gate.

    Fail-closed: a summary that is absent/raised, malformed, or partial (any
    field-set field whose membership cannot be affirmatively established) RAISES
    before the model send — the sink is never reached. The whitelist check then
    rejects any payload field outside the closed Summary Field-Set (named-excluded
    raw-PII OR a novel field): `set(payload) ⊆ SUMMARY_FIELD_SET` must hold.

    Args:
        summary (dict): A `summarize`-built name-addressable summary.
        sink (Callable, optional): The model sink receiving the payload. Defaults
            to a no-op sink.

    Returns:
        (Dispatch) The routed dispatch carrying the no-train lane attribute.
    """
    if not isinstance(summary, dict) or not summary:
        raise ValueError("dispatch: summary is absent or malformed (fail-closed)")

    # Fail-closed: a partial derivation (any field-set field unestablished)
    # defaults to OUT-of-set and raises — never send a partial payload.
    missing = [f for f in SUMMARY_FIELD_SET if f not in summary]
    if missing:
        raise ValueError(f"dispatch: partial summary, missing {missing} (fail-closed)")

    # The model-bound payload carries the dispatch's actual fields so the
    # whitelist check below can see (and reject) any injected out-of-set field.
    payload = dict(summary)

    # Payload-field-level WHITELIST: raise on ANY field outside the closed
    # field-set (its complement), keyed on absence from the set — not on a
    # named-excluded blacklist, not on a network call occurring.
    if not set(payload) <= set(SUMMARY_FIELD_SET):
        out_of_set = set(payload) - set(SUMMARY_FIELD_SET)
        raise ValueError(
            f"dispatch: out-of-field-set field(s) {sorted(out_of_set)} rejected"
        )

    if sink is not None:
        sink(payload)
    return Dispatch(NO_TRAIN_LANE, payload)
