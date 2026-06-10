"""Curated per-marker biomarker metadata registry (ADR-0008 D1).

The single metadata layer the render (component_set/dashboard) and plan (router)
surfaces consult for per-marker semantics: units, reference range, and
good-direction polarity. The registry values are general-adult population
reference values — operator-agnostic reference data per ADR-0005, not operator
PII. The v1 ranges are not sex- or lab-specific (ADR-0008 accepted limitation).
An unknown marker resolves to None everywhere (honest absence, never a
fabricated range).
"""

# marker -> {units, reference_range (low, high) | None, good_direction}.
# good_direction: "up" (rising improves), "down" (falling improves), "in-range"
# (movement toward the reference range improves), or None (no polarity).
METADATA = {
    "ferritin":        {"units": "ng/mL",  "reference_range": (30.0, 400.0), "good_direction": "in-range"},
    "vitamin-d":       {"units": "ng/mL",  "reference_range": (30.0, 100.0), "good_direction": "in-range"},
    "crp":             {"units": "mg/L",   "reference_range": (0.0, 3.0),    "good_direction": "down"},
    "alt":             {"units": "U/L",    "reference_range": (7.0, 56.0),   "good_direction": "down"},
    "hdl":             {"units": "mg/dL",  "reference_range": (40.0, 100.0), "good_direction": "up"},
    "ldl":             {"units": "mg/dL",  "reference_range": (0.0, 100.0),  "good_direction": "down"},
    "fasting-glucose": {"units": "mg/dL",  "reference_range": (70.0, 99.0),  "good_direction": "in-range"},
    "rhr":             {"units": "bpm",    "reference_range": (40.0, 100.0), "good_direction": "down"},
    "hrv":             {"units": "ms",     "reference_range": None,           "good_direction": "up"},
}

# The per-stream item-id prefixes the accessors tolerate (loop_schema namespaces).
_PREFIXES = ("biomarker::", "panel::", "watch-out::")

# Marker-name words rendered as acronyms (upper-cased) by display_name.
_ACRONYMS = frozenset({"hrv", "rhr", "crp", "alt", "hdl", "ldl"})


def _strip_prefix(item):
    """Return `item` with its stream prefix removed, if it carries one."""
    for prefix in _PREFIXES:
        if item.startswith(prefix):
            return item[len(prefix):]
    return item


def _to_number(value):
    """Parse `value` to a float, or None if it is missing/non-numeric."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get(item):
    """Look up a marker's metadata entry, tolerating the stream prefix.

    Args:
        item (str): The marker name, with or without a stream prefix
            (`biomarker::ferritin` and `ferritin` both resolve).

    Returns:
        (dict | None) The METADATA entry, or None for an unregistered marker.
    """
    return METADATA.get(_strip_prefix(item).lower())


def display_name(item):
    """Derive a clean display label from a store item id.

    Strips the stream prefix, splits on `-`/`_`, and title-cases each word —
    except acronym words (hrv, rhr, ...), which upper-case. So
    `biomarker::ferritin` -> `Ferritin`, `hrv` -> `HRV`, and
    `watch-out::injection_site_reaction` -> `Injection Site Reaction`.

    Args:
        item (str): The store item id, with or without a stream prefix.

    Returns:
        (str) The clean display label.
    """
    words = _strip_prefix(item).replace("_", "-").split("-")
    return " ".join(
        w.upper() if w.lower() in _ACRONYMS else w.title() for w in words
    )


def state_for(item, value):
    """Judge a marker value against its registered reference range.

    A numeric value inside the registered range (inclusive bounds) reads
    "good"; outside reads "concern". A non-numeric value, an unregistered
    marker, or a marker with no registered range reads None (neutral — no
    judgment possible). Never returns "watch": that state is reserved for
    future explicit nearing-boundary rules (ADR-0008 D1).

    Args:
        item (str): The marker name, with or without a stream prefix.
        value: The latest value to judge.

    Returns:
        (str | None) "good", "concern", or None.
    """
    number = _to_number(value)
    if number is None:
        return None
    meta = get(item)
    if meta is None or meta["reference_range"] is None:
        return None
    low, high = meta["reference_range"]
    return "good" if low <= number <= high else "concern"


def trend(item, prev, latest):
    """Label a marker's prev->latest movement via its good-direction polarity.

    Equal values read "flat". An "up" polarity reads rising as "improving" and
    falling as "regressing"; "down" is the inverse. An "in-range" polarity
    judges by distance-to-range `d(v) = max(low - v, v - high, 0.0)`: d
    shrinking reads "improving", growing "regressing", equal "flat" — and with
    no registered range reads None. A non-numeric value or an unregistered /
    polarity-less marker reads None.

    Args:
        item (str): The marker name, with or without a stream prefix.
        prev: The prior value.
        latest: The latest value.

    Returns:
        (str | None) "improving", "flat", "regressing", or None.
    """
    p, l = _to_number(prev), _to_number(latest)
    if p is None or l is None:
        return None
    meta = get(item)
    if meta is None or meta["good_direction"] is None:
        return None
    if meta["good_direction"] == "in-range":
        if meta["reference_range"] is None:
            return None
        low, high = meta["reference_range"]
        p = max(low - p, p - high, 0.0)
        l = max(low - l, l - high, 0.0)
        return "flat" if l == p else ("improving" if l < p else "regressing")
    if l == p:
        return "flat"
    rising = l > p
    if meta["good_direction"] == "up":
        return "improving" if rising else "regressing"
    return "regressing" if rising else "improving"
