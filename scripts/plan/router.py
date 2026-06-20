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
    # BPMH (de-identified) — the operator's present Rx-interaction CLASSES only,
    # never the raw medication names (rxbp; the supplement<->Rx BPMH axis).
    "rx-interaction-classes",
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
    # The operator's raw medication free-text (drug names + prescriber/pharmacy
    # notes). NEVER read by `summarize` (no `_RAW_TO_FIELD`/`_FIELD_DERIVATION`
    # entry — it is dropped, never derived); the de-identified Rx-interaction
    # CLASS tokens cross the boundary instead, curated in the store under
    # `rx-interaction-classes` (rxbp). Named here so the `dispatch` whitelist
    # rejects it should it ever reach a payload, and so the disjointness tripwire
    # below pins it out of the Summary Field-Set.
    "medication-list",
)

# Lane attributes (Constraint D1→ADR-0006: plan summaries route no-train).
NO_TRAIN_LANE = "no-train"
TRAIN_ELIGIBLE_LANE = "train-eligible"

# Raw store item -> field-set field. A field-set field backed by a raw-PII source
# item is derived from it via the band/class transformation; the rest read from a
# store item of the same name. Identity fields (legal-name, etc.) have no entry —
# they are dropped, never reaching the summary. `recent-trend-direction` is NOT
# here: it is registry-derived (juc, 2026-06-12 decision) from the `biomarker::`
# polarity feed, not from any raw-PII item — see `_recent_trend_direction`.
# `raw-lab-values` stays a named-excluded raw-PII class (the boundary promise) but
# is no longer derivation plumbing.
_RAW_TO_FIELD = {
    "date-of-birth": "training-age-band",
    "postal-address": "equipment-access-class",
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

# The de-identified BPMH field (rxbp): the operator's present Rx-interaction CLASS
# tokens, curated in the store as a `;`-joined scalar (the same canonical AE-class
# vocabulary the compound authors declare — `bleeding-risk`, `cyp3a4-pgp`, … — so a
# supplement's declared `additive_classes` can be matched against the operator's
# medication interaction surface). De-identification (drug name -> interaction class)
# is an operator/liaison CURATION step at the store layer, NOT a code lookup: no
# pharmacology DB enters this module, and an incomplete drug map can never produce a
# false-clean. The raw `medication-list` (drug free-text) is named-excluded and never
# read; only these curated class tokens cross the boundary.
RX_INTERACTION_CLASS_FIELD = "rx-interaction-classes"


def rx_interaction_class_set(summary):
    """The normalized set of operator Rx-interaction-class tokens from a summary.

    Parses the `rx-interaction-classes` field (a `;`-joined scalar, possibly empty)
    into a lowercased/stripped token set for the orchestrator's BPMH screen. An
    absent field (a summary that predates the field) or the empty no-meds token
    yields the empty set — no Rx surface, no hold.

    Args:
        summary (dict): A `summarize`-built summary.

    Returns:
        (set) The normalized Rx-interaction-class tokens (possibly empty).
    """
    raw = summary.get(RX_INTERACTION_CLASS_FIELD, "")
    if not isinstance(raw, str):
        return set()
    return {tok.strip().lower() for tok in raw.split(";") if tok.strip()}


def _rx_interaction_classes_token(store_read, identity_config):
    """Derive the de-identified `rx-interaction-classes` token from curated store state.

    Reads the operator/liaison-curated `rx-interaction-classes` store item — a
    de-identified list of Rx-interaction-class tokens, NOT raw drug names — and emits
    a deterministic `;`-joined scalar (sorted, deduped, lowercased). ALWAYS set (no
    curated item, or an empty value, yields the empty no-meds token `""`), mirroring
    `recent-trend-direction`'s always-set contract so a no-medication operator never
    trips `dispatch`'s partial-summary raise.

    The 8j6 pass-through PII gate is the runtime backstop: the class tokens are
    de-identified by the curation contract, but that contract is unenforced upstream,
    so a mis-curated token carrying raw operator PII (a prescriber email/phone, an
    address) RAISES at the boundary rather than crossing it. The scan runs PER TOKEN,
    not over the whole `;`-joined value: `pii_scan.scan_text` truncates its input at
    `_MAX_SCAN_TEXT_LEN`, so a whole-value scan would elide PII once this list field
    grows past the cap (SEC-1) — scanning each short class token keeps every scanned
    unit inside the window. Names the field, never the value (no PII echo).

    Args:
        store_read (Callable): The store read surface, called for the curated
            `rx-interaction-classes` item.
        identity_config (str | Path): The operator-identity token config passed to
            the 8j6 PII scan (the value `summarize` resolves for the boundary).

    Returns:
        (str) The de-identified `;`-joined Rx-interaction-class scalar (sorted, deduped,
        lowercased), or `""` when no medication is curated.
    """
    readings = store_read(RX_INTERACTION_CLASS_FIELD)
    if not readings:
        return ""
    value = str(readings[-1]["value"])
    tokens = sorted({tok.strip().lower() for tok in value.split(";") if tok.strip()})
    for tok in tokens:
        if pii_scan.scan_text(tok, token_config=identity_config):
            raise ValueError(
                f"summarize: {RX_INTERACTION_CLASS_FIELD!r} carries raw operator PII; the "
                f"de-identified-class-tokens-by-curation assumption is violated (fail-closed)"
            )
    return ";".join(tokens)

# The juc registry-driven recent-trend-direction feed (2026-06-12 decision §1):
# every registered-polarity marker (non-None `good_direction`), read under the
# `biomarker::` namespace only. Version-controlled VIA the registry — never
# hand-retyped, never store-enumerated, never goal-filtered. A `good_direction`
# edit re-shapes this feed AND the dashboard chips (dual-surface; registry
# polarity edits carry a review note from the juc decision forward). Daily-cadence
# streams (rhr/hrv/sleep-hours) are included for v1 per the adopted sub-call.
_POLARITY_FEED = tuple(
    f"biomarker::{marker}"
    for marker, meta in biomarker_meta.METADATA.items()
    if meta["good_direction"] is not None
)


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

    Reused by `_recent_trend_direction` as the per-stream deriver over the juc
    registry-polarity feed (2026-06-12 decision): each feed stream is a single
    registered-polarity marker, so the cross-item raise cannot trip and the
    registry resolves the polarity through `biomarker_meta.trend` (rising ALT
    regresses; rising HDL improves). The cross-item and unknown-polarity raises
    remain as fail-closed safety nets — a determinable directional change with
    unknown polarity surfaces at the boundary rather than fabricate a
    value-judgment. `flat` is emitted for genuine no-change, for an
    insufficient/missing series (the no-signal token — missing data is NEVER a
    false `improving`), and — since ADR-0008 — for an in-range-polarity marker
    whose movement keeps the same distance-to-range (the value moved, the
    judgment did not).
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


def _recent_trend_direction(store_read):
    """Derive `recent-trend-direction` by worst-wins over the polarity feed.

    juc decision §2 (2026-06-12): each registered-polarity `biomarker::` stream
    (`_POLARITY_FEED`) contributes its own trend — its last two numeric readings
    via `_trend_token` over that one stream's series, so each stream's
    cross-item/unknown-polarity fail-closed raises still guard it. The per-stream
    trends reduce WORST-WINS: any `regressing` wins; else any `improving`; else
    `flat`. A stream with an insufficient/missing series yields `flat`
    (`_trend_token`'s no-signal token), which is the worst-wins floor — so a feed
    with no lab signal at all reduces to `flat` (decision §4: the operator-fresh
    state emits the no-signal `flat`, never a partial-summary block). The output
    is one of the closed `TREND_DIRECTIONS` (juc tripwire below).

    Args:
        store_read (Callable): The store read surface, called per feed stream.
            Caller-bound to the instance root exactly as `summarize` documents.

    Returns:
        (str) `improving`, `flat`, or `regressing`.
    """
    trends = [_trend_token(store_read(stream)) for stream in _POLARITY_FEED]
    if "regressing" in trends:
        return "regressing"
    if "improving" in trends:
        return "improving"
    return "flat"


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

# juc change-control tripwire (2026-06-12 decision §3): the registry-driven
# recent-trend-direction feed is EXACTLY the registered-polarity marker set read
# under `biomarker::` — every source resolves to a registered marker with a
# non-None good_direction, so a hand-edited off-registry source trips this; no
# feed source is a Summary Field-Set field (the feed produces the derived token,
# it is not itself a field) and none joins the named-excluded raw-PII set (the
# streams are derivation inputs, never raw-PII classes — resolving the second half
# of S51 sub-question (c)); and the worst-wins reduction's outputs are pinned to
# the locked TREND_DIRECTIONS vocabulary. `_TREND_REDUCTION_OUTPUTS` is that
# declared output set, kept distinct from the unordered vocabulary `TREND_DIRECTIONS`
# because it is ORDERED by worst-wins precedence (regressing > improving > flat,
# mirroring the reduction's return order); a future change to the reduction's outputs
# that drifts off this set reds the final assert below.
_TREND_REDUCTION_OUTPUTS = ("regressing", "improving", "flat")
assert all(
    (_m := biomarker_meta.get(_s)) is not None and _m["good_direction"] is not None
    for _s in _POLARITY_FEED
)
assert set(_POLARITY_FEED).isdisjoint(SUMMARY_FIELD_SET)
assert set(_POLARITY_FEED).isdisjoint(EXCLUDED_RAW_PII)
assert set(_TREND_REDUCTION_OUTPUTS) <= set(TREND_DIRECTIONS)

# smei validity pin (juc decision cross-system note): every "in-range"-polarity
# feed marker MUST carry a reference_range. `biomarker_meta.trend` judges an
# in-range marker by distance-to-range, so an in-range marker with no range
# returns None -> `_trend_token` hits its unknown-polarity raise -> the WHOLE
# plan summary fail-closes. ("up"/"down" markers judge by rising/falling and
# need no range — e.g. hrv/sleep-hours.) Pinned at load so a future registry
# edit (an in-range marker added without a range, or a range nulled) trips here,
# not silently at the operator's runtime.
assert all(
    biomarker_meta.get(_s)["reference_range"] is not None
    for _s in _POLARITY_FEED
    if biomarker_meta.get(_s)["good_direction"] == "in-range"
)


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
        if field == "recent-trend-direction":
            # juc: registry-driven worst-wins over the `biomarker::` polarity feed
            # — neither a raw-PII-backed field nor a store item of its own name.
            # ALWAYS set (zero feed signal -> the no-signal `flat`, decision §4),
            # so a fresh operator never trips dispatch's partial-summary raise.
            summary[field] = _recent_trend_direction(store_read)
            continue
        if field == RX_INTERACTION_CLASS_FIELD:
            # rxbp: de-identified Rx-interaction-class tokens, curated in the store.
            # ALWAYS set (no meds -> the empty token `""`), so a no-medication
            # operator never trips dispatch's partial-summary raise. The 8j6 PII
            # backstop scans the curated value inside the deriver.
            summary[field] = _rx_interaction_classes_token(store_read, identity_config)
            continue
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
