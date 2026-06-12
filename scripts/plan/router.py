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

from scripts.guard import pii_scan
from scripts.store import biomarker_meta

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


# Closed `recent-trend-direction` vocabulary (ADR-0006-T0 spike lines 32-33).
TREND_DIRECTIONS = ("improving", "flat", "regressing")


def _age_band(readings):
    """Bucket a raw date-of-birth into a coarse training-age band.

    Buckets by birth-decade (minimal sensible boundaries — the spike pins the
    band SHAPE, not exact cutoffs); the raw date never appears in the token.
    """
    year = str(readings[-1]["value"])[:4]
    return f"born-{year[:3]}0s" if year.isdigit() else "age-band-unknown"


def _trend_token(readings):
    """Derive a `recent-trend-direction` token from the readings SERIES.

    The spike (lines 32-33) locks the closed vocabulary `improving`/`flat`/
    `regressing` — a direction over time, derived from the latest vs prior
    NUMERIC reading, never a single value or a range-membership. The two
    compared readings must come from ONE item: a series mixing items carries
    no single-marker trend, so a cross-item comparison RAISES naming both
    items (fail-closed — never the values).

    The per-marker good-direction gap is closable per marker via
    `scripts/store/biomarker_meta.py` (ADR-0008 D4): a registered-polarity
    marker's directional change resolves to `improving`/`regressing` through
    the registry (rising ALT regresses; rising HDL improves). An UNREGISTERED
    marker — including the generic `raw-lab-values` stream, unregistered by
    design — keeps the fail-closed raise: a determinable directional change
    with unknown polarity surfaces at the boundary rather than fabricate a
    value-judgment. Per-marker lab trends for the summary are the Track-2
    residual (`juc`). `flat` is emitted for genuine no-change, for an
    insufficient/missing series (the no-signal token — missing data is NEVER
    a false `improving`), and — since ADR-0008 — for an in-range-polarity
    marker whose movement keeps the same distance-to-range (the value moved,
    the judgment did not).
    """
    pairs = [
        (r["item"], n)
        for r in readings
        if (n := biomarker_meta.to_number(r["value"])) is not None
    ]
    if len(pairs) < 2:
        return "flat"  # insufficient series / missing data — no false affirmative
    (prev_item, prev), (last_item, last) = pairs[-2], pairs[-1]
    if prev_item != last_item:
        raise ValueError(
            f"recent-trend-direction: the two compared numeric readings come "
            f"from different items ({prev_item!r} vs {last_item!r}) — a "
            f"cross-item comparison is not a marker trend (fail-closed)"
        )
    if last == prev:
        return "flat"  # genuine no-change
    direction = biomarker_meta.trend(last_item, prev, last)
    if direction is not None:
        return direction
    raise ValueError(
        "recent-trend-direction: a directional change is not faithfully "
        "labellable improving/regressing for a marker with no registered "
        "good-direction polarity (scripts/store/biomarker_meta.py) — "
        "fail-closed on the unregistered marker"
    )


def _issue_class(readings):
    """Map raw symptom/clinical free-text to a coarse body-region issue class."""
    text = str(readings[-1]["value"]).lower()
    if any(w in text for w in ("back", "spine", "lumbar")):
        return "back-region"
    if any(w in text for w in ("knee", "leg", "hip", "ankle")):
        return "lower-limb-region"
    if any(w in text for w in ("shoulder", "arm", "elbow", "wrist")):
        return "upper-limb-region"
    return "general-issue"


def _region_class(readings):
    """Map a raw postal-address to a coarse presence/region class (no raw value)."""
    return "region-present" if str(readings[-1]["value"]).strip() else "region-absent"


# Per-field-set-field de-identifying derivations for fields backed by a raw-PII
# source item. Each takes the readings SERIES and MUST emit a derived band/class
# token only — the raw value never appears in the emitted token (Finding 4-1).
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


def summarize(store_read, identity_config=pii_scan.DEFAULT_IDENTITY_CONFIG):
    """Derive the plan-reasoning summary from store-read state.

    Reads operator state through the store read model (`store_read`, the
    `store.read` surface) and no other source, applying the spike's raw-field ->
    summary-token transformation so no named-excluded raw-PII field survives. The
    returned summary is name-addressable: a mapping from each Summary Field-Set
    field name to its de-identified token, carrying only field-set fields.

    Args:
        store_read (Callable): The store read surface (`store.read`), called per
            field-set field to source its backing state. Caller contract (bead
            e3b, S51 adjudication): pre-bind the instance root before passing —
            e.g. `functools.partial(store.read, root=instance_root)` — mirroring
            `generate.run`'s call-site binding (`store.read_all(root)`). An
            unbound `store.read` reads `store.DEFAULT_ROOT` (`vault/store/`
            under the cwd), not the caller's instance — silently; no error is
            raised at this boundary, the misread surfaces only as
            wrong-instance summary data.
        identity_config (str | Path, optional): The gitignored operator-identity
            token file for the pass-through PII gate (bead 8j6); absent -> identity
            detection is empty (the value-boundary patterns — any-domain email,
            phone, postal — still run via scan_text). When the caller's cwd
            diverges from the instance root (the same scenario requiring the
            bound `store_read` partial), `identity_config` MUST also be passed
            instance-bound (e.g. `<instance_root>/vault/meta/operator-identity.txt`),
            because the default resolves under the cwd and an ABSENT file
            silently empties identity-token detection
            (`pii_scan._load_token_patterns` returns `[]`).

    Returns:
        (dict) A name-addressable summary keyed by the Summary Field-Set fields.

    Raises:
        ValueError: When a pass-through field value carries raw operator PII (the
            8j6 fail-closed gate) — surfaced at the boundary, never leaked downstream.
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
                summary[field] = _FIELD_DERIVATION[field](readings)
        else:
            # ...otherwise the field reads from a store item of its own name.
            readings = store_read(field)
            if readings:
                value = readings[-1]["value"]
                # 8j6 fail-closed: a pass-through field is contracted as a de-identified
                # STATED TOKEN (PII-free by store schema). That assumption is unenforced
                # upstream, so enforce it HERE — the summary IS the 0-raw-PII boundary.
                # Raw PII (operator identity / contact) in the value cannot be faithfully
                # passed through; surface the gap at the boundary rather than leak it to
                # the model (via dispatch) or the render (via assemble). Names the field,
                # never the value (no PII echo).
                if pii_scan.scan_text(str(value), token_config=identity_config):
                    raise ValueError(
                        f"summarize: pass-through field {field!r} carries raw operator "
                        f"PII; the PII-free-by-store-schema assumption is violated "
                        f"(fail-closed)"
                    )
                summary[field] = value
    return summary


def dispatch(summary, sink=None):
    """Route a summary to the no-train lane after the payload whitelist gate.

    Fail-closed: a summary that is absent/raised, malformed, or partial (any
    field-set field whose membership cannot be affirmatively established) RAISES
    before the model send — the sink is never reached. The whitelist check then
    rejects any payload field outside the closed Summary Field-Set (named-excluded
    raw-PII OR a novel field): `set(payload) ⊆ SUMMARY_FIELD_SET` must hold. A
    non-scalar payload value (a container under an allowlisted key) likewise RAISES
    before the send (fga) — payload values must be scalar (None or str/int/float/bool).

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

    # fga (SEC-2) runtime scalar gate: the field-set whitelist checks NAMES; this
    # checks VALUE SHAPE. The payload is scalar-by-derivation, but a future nested-
    # summary change could smuggle a raw-PII field inside a container under an
    # allowlisted key, past the shallow name check. Fail-closed via a positive
    # ALLOWLIST of scalar types (None or str/int/float/bool): reject anything else —
    # closing bytes/bytearray/frozenset/memoryview and any future opaque type, not
    # only the four enumerated containers. A runtime guarantee, not only the
    # test-only flat-payload pin. Names the field, never the value.
    nonscalar = sorted(
        field for field, value in payload.items()
        if value is not None and not isinstance(value, (str, int, float, bool))
    )
    if nonscalar:
        raise ValueError(
            f"dispatch: non-scalar payload value(s) {nonscalar} rejected (fga)"
        )

    if sink is not None:
        sink(payload)
    return Dispatch(NO_TRAIN_LANE, payload)
