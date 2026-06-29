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

import re
from datetime import datetime, timezone
from pathlib import Path

from scripts.genetics import match
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
    # chat-sourced rich-domain (de-identified, ADR-0019-T1) — coarse band/class tokens
    # derived from the chat-extracted free-text, never the raw food/stack/split text.
    # Each is kind-2 raw-backed-derived (a named-excluded raw source + a derivation);
    # `training-volume-band` (chat-sourced weekly volume) is DISTINCT from the
    # demographic `training-age-band` (date-of-birth born-decade band).
    "dietary-pattern-class",
    "supplement-stack-class",
    "peptide-use-class",
    "training-volume-band",
    # genetics (de-identified, ADR-0032-T3) — the COARSE genetic-trait CLASSES the
    # operator's curated genotypes resolve to against the local library; the raw
    # rsID+allele genotype NEVER crosses to the no-train planner (the crown jewel,
    # NFR-1). Match-derived (T2's `match_genotypes`), not raw-PII-backed — its own
    # dedicated `summarize` branch, NOT a `_RAW_TO_FIELD`/`_ALWAYS_SET_DERIVED` member.
    "genetic-trait-classes",
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
    # chat-sourced rich-domain raw free-text (ADR-0019-T1). The operator's raw nutrition
    # / supplement / peptide / training-detail prose — named-excluded raw-PII classes that
    # `summarize` DERIVES into the coarse `dietary-pattern-class` / `supplement-stack-class`
    # / `peptide-use-class` / `training-volume-band` tokens (the raw text never crosses the
    # boundary). Named here so the disjointness tripwire pins them out of the field-set and
    # the dispatch whitelist rejects any raw source that reached a payload.
    "raw-nutrition-free-text",
    "raw-supplement-free-text",
    "raw-peptide-free-text",
    "raw-training-detail-free-text",
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
# `equipment-access-class` is NOT here (ADR-0018-T1 reconciliation): the demographic
# equipment selection (a Step-1 bounded select) is its ONE authoritative source — a
# pass-through `WIRED_TOKENS` token read under its own name. The former
# `postal-address -> equipment-access-class` inference (a coarse region-presence proxy)
# is removed; `postal-address` stays a named-excluded raw-PII class in EXCLUDED_RAW_PII,
# just no longer a derivation source.
_RAW_TO_FIELD = {
    "date-of-birth": "training-age-band",
    "raw-symptom-free-text": "active-issue-class",
    "clinical-notes": "active-issue-class",
    # chat-sourced rich-domain raw free-text -> coarse band/class (ADR-0019-T1).
    "raw-nutrition-free-text": "dietary-pattern-class",
    "raw-supplement-free-text": "supplement-stack-class",
    "raw-peptide-free-text": "peptide-use-class",
    "raw-training-detail-free-text": "training-volume-band",
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

# The de-identified genetics field (ADR-0032-T3): the COARSE genetic-trait CLASSES the
# operator's curated genotypes resolve to. The raw rsID+allele genotype is NEVER read
# into the token — the deriver collects each match's `trait_class` only (the crown
# jewel, NFR-1). Resolution (genotype -> trait class) is T2's LOCAL library lookup
# (`scripts.genetics.match`), never a model call.
GENETIC_TRAIT_CLASS_FIELD = "genetic-trait-classes"

# The `None`->real-default genetics library root (FIX-1/CQ-1). Mirrors
# `store.DEFAULT_ROOT = Path("vault/store")`: a `summarize(store_read)` with NO
# `genetics_library_root` resolves to the REAL `vault/library/genetics/`, so the frozen
# no-arg production callers (`generate_plan.py`/`orchestrate.py`/`chat.py`) are DNA-aware
# WITHOUT a caller edit. `None` resolves HERE, to the live library — it does NOT disable
# the feature.
GENETICS_LIBRARY_DEFAULT_ROOT = Path("vault/library/genetics")

# Crown-jewel backstop (NFR-1): a coarse trait-class token must carry NO raw genotype.
# A curated finding is contracted to a coarse class, but that contract is unenforced
# upstream — a token matching an rsID (`rs\d+`) or an allele-call (`(allele;allele)`)
# makes the deriver fail-closed rather than leak the genotype to the no-train planner.
_RAW_GENOTYPE_PATTERNS = (
    re.compile(r"rs\d+"),
    re.compile(r"\([ACGTDI]+;[ACGTDI]+\)"),
)


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


def _genetic_trait_classes_token(store_read, genetics_library_root, identity_config):
    """Derive the de-identified `genetic-trait-classes` token from matched library findings.

    Calls T2's `match.match_genotypes` against the resolved local genetics library,
    collects each match's COARSE `trait_class`, and emits a deterministic `;`-joined
    scalar (sorted, deduped). ALWAYS set (no DNA / no resolved match -> the empty token
    `""`), mirroring `_rx_interaction_classes_token` so a no-DNA operator never trips
    `dispatch`'s partial-summary raise. The raw rsID+allele genotype NEVER enters the
    token — only the coarse trait class crosses to the no-train planner (the crown
    jewel, NFR-1).

    `genetics_library_root` of `None` resolves to the module-level
    `GENETICS_LIBRARY_DEFAULT_ROOT` (the REAL `vault/library/genetics/`), so the frozen
    no-arg `summarize(store_read)` callers are DNA-aware in production WITHOUT a caller
    edit (FIX-1/CQ-1) — `None` does NOT disable the feature.

    Per-token fail-closed backstop (the crown jewel): a curated finding is contracted to
    a coarse trait class, never a raw genotype, but that contract is unenforced upstream.
    A collected token matching a raw-genotype pattern (`rs\\d+` or `(allele;allele)`) OR
    carrying operator PII (`pii_scan.scan_text`) RAISES at the boundary rather than
    crossing it. Names the field, never the value (no genotype/PII echo).

    Args:
        store_read (Callable): The per-item store read surface (`store.read`),
            pre-bound to the instance root by the caller (the T2 matcher's contract).
        genetics_library_root (str | Path | None): The `vault/library/genetics/` root;
            `None` resolves to the real `GENETICS_LIBRARY_DEFAULT_ROOT`.
        identity_config (str | Path): The operator-identity token config passed to the
            8j6 PII scan (the value `summarize` resolves for the boundary).

    Returns:
        (str) The coarse `;`-joined, sorted, deduped trait-class scalar, or `""` when no
        curated variant resolves.

    Raises:
        ValueError: When a collected trait-class token carries a raw genotype or operator
            PII (fail-closed) — surfaced at the boundary, never leaked downstream.
    """
    library_root = (
        genetics_library_root
        if genetics_library_root is not None
        else GENETICS_LIBRARY_DEFAULT_ROOT
    )
    matches = match.match_genotypes(store_read, library_root=library_root)
    tokens = sorted({m["trait_class"] for m in matches})
    for tok in tokens:
        if any(p.search(tok) for p in _RAW_GENOTYPE_PATTERNS) or pii_scan.scan_text(
            tok, token_config=identity_config
        ):
            raise ValueError(
                f"summarize: {GENETIC_TRAIT_CLASS_FIELD!r} carries a raw genotype or raw "
                f"operator PII; the coarse-trait-class-by-curation assumption is violated "
                f"(fail-closed)"
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


# BUG-1 sentinel (Wave-B review): the DISTINCT "source absent — not elicited" token for
# the 4 chat-sourced always-set derivers. Kept separate from each deriver's no-signal
# default (`general-diet`/`none`/`moderate`), which means "there IS source data and it
# says so". `not-discussed` (absent) is token-distinguishable from `none` (confirmed-none)
# — a fresh operator with no chat data reads as "not elicited", never "confirmed no
# peptides". Still a value, so the always-set contract holds (dispatch's partial-summary
# raise does not trip).
_NOT_DISCUSSED = "not-discussed"


def _age_band(readings):
    """Bucket a raw date-of-birth into a coarse training-age band.

    Buckets by birth-decade (minimal sensible boundaries — the spike pins the
    band SHAPE, not exact cutoffs); the raw date never appears in the token.
    Requires EXACTLY 4 digits after stripping surrounding whitespace and a year
    inside a sane range (1900..the current UTC year) — a malformed value ('86',
    '198', a future year, a non-numeric string) bands `age-band-unknown` rather
    than fabricating a born-decade.
    """
    raw = str(readings[-1]["value"]).strip()
    year = raw[:4]
    if len(year) != 4 or not year.isdigit():
        return "age-band-unknown"
    if not 1900 <= int(year) <= datetime.now(timezone.utc).year:
        return "age-band-unknown"
    return f"born-{year[:3]}0s"


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


def _dietary_pattern_class(readings):
    """Map raw nutrition free-text to a coarse dietary-pattern class (ADR-0019-T1).

    Emits a coarse diet class only — the raw food/allergen text never appears in the
    token (the per-token output scan, AC-2, proves this). Mirrors `_issue_class`'s
    keyword-bucketing coarseness: the class is a pattern bucket, not the raw meal log.
    An ABSENT readings series (no chat-extracted nutrition yet) -> the `not-discussed`
    sentinel (BUG-1: distinguishable from a confirmed pattern). A PRESENT value with no
    matched pattern -> the `general-diet` no-signal default.

    Precedence (BUG-5): the allergy/restriction keyword set is checked FIRST, before the
    plant-pattern buckets, so a mixed "pattern + allergy" value ('vegetarian but allergic
    to nuts') bands `restricted` consistently with the omnivore-with-allergy case
    ('eat everything but allergic to shellfish') — the allergy signal is never masked by
    a leading plant pattern. Single coarse class only (no second allergen token — that is
    a vocabulary change out of scope).
    """
    if not readings:
        return _NOT_DISCUSSED
    text = str(readings[-1]["value"]).lower()
    if any(w in text for w in ("keto", "carnivore", "elimination", "allergic", "allergy",
                               "intolerant", "restricted", "gluten-free")):
        return "restricted"
    if any(w in text for w in ("vegan", "plant-based", "plant based", "wholly plant")):
        return "plant-based"
    if any(w in text for w in ("vegetarian", "plant-forward", "plant forward", "pescatarian")):
        return "plant-forward"
    if any(w in text for w in ("meat", "chicken", "beef", "fish", "omnivore", "everything")):
        return "omnivore"
    return "general-diet"


def _supplement_stack_class(readings):
    """Map raw supplement free-text to a coarse stack-presence class (ADR-0019-T1).

    Emits a coarse presence/category class only — raw product names and doses never
    appear in the token (AC-2). The cut is presence + rough breadth (one vs several),
    never the itemized stack. An ABSENT series -> the `not-discussed` sentinel (BUG-1:
    distinguishable from a confirmed-none). A PRESENT empty / no-supplement / separators-
    only value (the operator typed something that resolves to nothing) -> the confirmed
    `none`.
    """
    if not readings:
        return _NOT_DISCUSSED
    text = str(readings[-1]["value"]).strip().lower()
    if not text or text in ("none", "no", "n/a", "na"):
        return "none"
    # Count distinct comma/semicolon/newline-separated items as a rough breadth signal.
    # BUG-4: filter the empties FIRST so a separators-only value (';;;', ',,') resolves to
    # 0 parts -> `none`, never a false single-supplement off a len<=1 empty list.
    parts = [p.strip() for p in text.replace(";", ",").replace("\n", ",").split(",") if p.strip()]
    if not parts:
        return "none"
    return "multi-supplement" if len(parts) > 1 else "single-supplement"


def _peptide_use_class(readings):
    """Map raw peptide free-text to a coarse use/presence class (ADR-0019-T1).

    Emits a coarse use/presence class only — raw compound names and doses never appear
    in the token (AC-2). The cut is binary presence (the peptide axis is high-sensitivity:
    presence, not the itemized compounds). An ABSENT series -> the `not-discussed` sentinel
    (BUG-1: distinguishable from a confirmed-none — a fresh operator never reads as
    "confirmed no peptides"). A PRESENT empty / no-peptide / separators-only value -> the
    confirmed `none`.
    """
    if not readings:
        return _NOT_DISCUSSED
    text = str(readings[-1]["value"]).strip().lower()
    if not text or text in ("none", "no", "n/a", "na"):
        return "none"
    # BUG-4: a separators-only value (';;;', ',,') is PRESENT-but-empty -> confirmed `none`,
    # not a false `peptide-in-use`. Strip the separators and re-check for residual content.
    parts = [p.strip() for p in text.replace(";", ",").replace("\n", ",").split(",") if p.strip()]
    if not parts:
        return "none"
    return "peptide-in-use"


def _training_volume_band(readings):
    """Map raw training-detail free-text to a coarse weekly-volume band (ADR-0019-T1).

    Emits a coarse weekly-volume band only — raw set counts / the itemized split never
    appear in the token (AC-2). DISTINCT from `_age_band`'s `training-age-band` (a
    demographic born-decade band): this is a chat-sourced training-VOLUME band. Bands by
    weekly session frequency parsed loosely from the free-text (`low`/`moderate`/`high`).
    An ABSENT series (no chat-extracted training detail yet) -> the `not-discussed`
    sentinel (BUG-1). A PRESENT value with no determinable count -> the `moderate`
    no-signal middle.

    BUG-3: the frequency capture is one-or-two digits (not a single digit), so a
    double-digit count ('10x', '12 sessions') bands `high` instead of being misread.
    Parsed counts are clamped to 1..14 (a sane weekly-session range). When two unrelated
    numbers appear ('5 days and 2x'), the CONTEXTUAL/last frequency match wins over
    `max()` of unrelated integers. A range like '4-5x' captures the digit adjacent to the
    unit ('5' -> high).
    """
    import re

    if not readings:
        return _NOT_DISCUSSED
    text = str(readings[-1]["value"]).lower()
    # All frequency matches across both unit patterns, in text order; the LAST wins (the
    # contextual per-week count), not max() of unrelated integers.
    matches = sorted(
        re.finditer(r"\b(\d{1,2})\s*(?:x|days?|sessions?|/week|per week)", text),
        key=lambda m: m.start(),
    )
    sessions = max(1, min(14, int(matches[-1].group(1)))) if matches else None
    if sessions is None:
        if any(w in text for w in ("twice", "2x", "minimal", "light")):
            return "low"
        if any(w in text for w in ("daily", "every day", "two-a-day", "high volume")):
            return "high"
        return "moderate"
    if sessions <= 2:
        return "low"
    if sessions >= 5:
        return "high"
    return "moderate"


# Per-field-set-field de-identifying derivations for fields backed by a raw-PII
# source item. Each takes the readings SERIES and MUST emit a derived band/class
# token only — the raw value never appears in the emitted token (Finding 4-1).
# `equipment-access-class` is no longer here (ADR-0018-T1): it is now a pass-through
# token sourced from the demographic equipment selection, not a postal-address derivation.
_FIELD_DERIVATION = {
    "training-age-band": _age_band,
    "active-issue-class": _issue_class,
    # chat-sourced rich-domain coarse band/class derivers (ADR-0019-T1).
    "dietary-pattern-class": _dietary_pattern_class,
    "supplement-stack-class": _supplement_stack_class,
    "peptide-use-class": _peptide_use_class,
    "training-volume-band": _training_volume_band,
}

# Derived tokens that are ALWAYS set (ADR-0019-T1): a fresh operator with no chat-extracted
# source yet gets the deriver's no-signal default, so these never trip dispatch's
# partial-summary raise — mirroring `recent-trend-direction` (the no-signal `flat`) and
# `rx-interaction-classes` (the empty `""`). The OTHER raw-PII-backed derived fields
# (`training-age-band`, `active-issue-class`) stay conditionally set — they are omitted when
# their source is absent (the demographic intake always seeds `date-of-birth`; a
# never-injured operator legitimately has no `active-issue-class`). Their derivers index
# `readings[-1]` and are only reached when `if readings` holds.
_ALWAYS_SET_DERIVED = (
    "dietary-pattern-class",
    "supplement-stack-class",
    "peptide-use-class",
    "training-volume-band",
)

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


def summarize(store_read, identity_config=pii_scan.DEFAULT_IDENTITY_CONFIG,
              genetics_library_root=None):
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
        genetics_library_root (str | Path, optional): The `vault/library/genetics/`
            root the `genetic-trait-classes` deriver resolves the operator's curated
            genotypes against (ADR-0032-T3). `None` (the default the three frozen
            callers pass) resolves to the module-level `GENETICS_LIBRARY_DEFAULT_ROOT`
            (the REAL library), so the no-arg production call is DNA-aware WITHOUT a
            caller edit — `None` does NOT disable the feature (FIX-1/CQ-1).

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
        if field == GENETIC_TRAIT_CLASS_FIELD:
            # ADR-0032-T3: coarse genetic trait classes from T2's LOCAL matcher.
            # ALWAYS set (no DNA / no match -> the empty token `""`), so a no-DNA
            # operator never trips dispatch's partial-summary raise. `genetics_library_root`
            # of None resolves to the real GENETICS_LIBRARY_DEFAULT_ROOT (FIX-1/CQ-1 —
            # the no-arg production call is DNA-aware without a caller edit). The raw
            # rsID+allele genotype NEVER enters the token (the crown jewel); the deriver
            # fail-closes on a raw-genotype-bearing token.
            summary[field] = _genetic_trait_classes_token(
                store_read, genetics_library_root, identity_config
            )
            continue
        if field in _ALWAYS_SET_DERIVED:
            # chat-sourced rich-domain bands (ADR-0019-T1): ALWAYS set — a fresh operator
            # with no chat-extracted source yet gets the deriver's no-signal default (the
            # coarse `none`/`general-diet`/`moderate`), so the new tokens never trip
            # dispatch's partial-summary raise (mirroring recent-trend-direction / rxbp).
            readings = []
            for raw in (r for r, f in _RAW_TO_FIELD.items() if f == field):
                readings.extend(store_read(raw))
            summary[field] = _FIELD_DERIVATION[field](readings)
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
