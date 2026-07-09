"""Deterministic pre-de-id aggregation of high-cardinality operator timeseries.

The model-based `deid_in` boundary (ADR-0020, the `run_orchestrated` path) sends the raw
operator intake to the no-train de-id model. The operator's wearable timeseries
(RHR/HRV/SpO2/resp-rate) can be thousands of readings spanning years — on a real intake
that is ~131K tokens of raw points the model would have to crunch into a trend, on the
most expensive model (Opus), on every re-generation.

`aggregate_operator_state` collapses each high-cardinality NUMERIC timeseries stream to ONE
compact per-stream summary (count, span, latest, mean/median, range, recent-window mean) so
the de-id model receives biomarker STATS, not raw readings — cutting the de-id payload
~10-100x. It touches ONLY high-cardinality numeric streams; demographics, goals, free-text,
date-of-birth, safety screens, and genetics pass through UNCHANGED, so every PII-bearing
field still reaches the de-id boundary and gets de-identified. The aggregation runs
IN-PROCESS on the raw data before any egress, so it does not weaken the crown-jewel de-id
OUTPUT scan — it only reduces the INPUT the no-train model sees.

`AggregatingDeidClient` is the thin adapter that applies it at the injectable `deid_client`
seam (`plan_loop.signal(..., deid_client=...)`) — the frozen `_read_raw_intake` /
`run_orchestrated` engine is untouched (EXTEND-NOT-REBUILD).
"""

from collections import defaultdict
from statistics import mean, median

# A stream is collapsed only when it has at least this many readings AND every value is
# numeric — the wearable-timeseries shape. Demographics / goals / free-text / DOB / genetics
# (all low-count or non-numeric) fall below this and pass through verbatim.
DEFAULT_MIN_COUNT = 20
# The trailing window (most-recent N readings) summarised separately so the de-id model can
# still read a recent-vs-overall trend from the compact summary.
DEFAULT_RECENT_WINDOW = 90


def aggregate_operator_state(operator_state, *, min_count=DEFAULT_MIN_COUNT,
                             recent_window=DEFAULT_RECENT_WINDOW):
    """Collapse high-cardinality numeric timeseries streams to one summary reading each.

    Args:
        operator_state (list): The raw operator readings (`{item, timepoint, source, value}`).
        min_count (int, optional): The per-stream reading count at/above which a numeric
            stream is collapsed. Below it, readings pass through unchanged.
        recent_window (int, optional): The trailing-window size for the `recent_mean` stat.

    Returns:
        (list) The operator state with high-cardinality numeric streams collapsed; all other
        readings (and any non-dict entries) preserved in first-seen order.
    """
    by_item = defaultdict(list)
    order = []
    for r in operator_state:
        if not isinstance(r, dict) or "item" not in r:
            order.append(("raw", r))
            continue
        item = r["item"]
        if item not in by_item:
            order.append(("item", item))
        by_item[item].append(r)

    out = []
    for kind, key in order:
        if kind == "raw":
            out.append(key)
            continue
        readings = by_item[key]
        nums = [r["value"] for r in readings if isinstance(r.get("value"), (int, float))
                and not isinstance(r.get("value"), bool)]
        if len(readings) >= min_count and len(nums) == len(readings):
            dated = sorted(readings, key=lambda r: str(r.get("timepoint", "")))
            recent = [r["value"] for r in dated[-recent_window:]]
            out.append({
                "item": key,
                "timepoint": dated[-1].get("timepoint"),
                "source": readings[0].get("source"),
                "aggregated_from": len(readings),
                "value": {
                    "n": len(nums),
                    "span": [dated[0].get("timepoint"), dated[-1].get("timepoint")],
                    "latest": dated[-1]["value"],
                    "mean": round(mean(nums), 1),
                    "median": round(median(nums), 1),
                    "min": min(nums),
                    "max": max(nums),
                    "recent_mean": round(mean(recent), 1),
                },
            })
        else:
            out.extend(readings)
    return out


def normalize_summary(summary):
    """Coerce a model-de-id summary's non-string field values to the string consumer contract.

    The no-train de-id MODEL (`deid_in` via `ModelClient`) emits multi-value SUMMARY_FIELD_SET
    fields as LISTS (observed at the first LIVE run) — and, being a non-deterministic model on
    the crown-jewel path, could emit a dict/scalar too. The downstream frozen plan-composition
    layer / translators expect STRING values and string-process them (the hard-limit filter does
    `(...).lower()`); ANY non-string value crashes that consumer (`'list'/'dict'/'bool' object
    has no attribute 'lower'`, bead 940o — the mock tests used string-shaped fixtures so the
    crash reached the first live run). This coerces EVERY value to a string: a list joins with
    `; ` (which every current SUMMARY_FIELD_SET consumer parses equivalently — they all strip
    tokens — though NOT byte-identical to `router.summarize`, which joins rx-/genetic-trait
    tokens with `;`); any other non-string (dict/int/float/bool) is `str()`-ed (so a falsy 0
    is not silently dropped by a downstream `(x or "")`).

    `normalize_summary` runs INSIDE the de-id client, so `deid_in`'s own key-whitelist + PII
    value-scan run on THIS return (downstream, not before). The fail-closed sentinel
    (`{"deidentified": False}`) and any non-dict input pass through unchanged — the sentinel
    branch is forward-defense for a de-id backend that RETURNS the sentinel rather than raising
    (`deid_in`'s discriminated-union contract permits it, though the current `ModelClient` raises).

    Args:
        summary (dict): The de-id model output — SUMMARY_FIELD_SET-keyed (list / scalar / string
            values), or the fail-closed sentinel.

    Returns:
        (dict) The summary with every field value coerced to a string (a list `; `-joined, any
        other non-string `str()`-ed); the sentinel and non-dict inputs returned unchanged.
    """
    if not isinstance(summary, dict) or summary.get("deidentified") is False:
        return summary
    return {
        k: (v if isinstance(v, str)
            else "; ".join(str(x) for x in v) if isinstance(v, list)
            else str(v))
        for k, v in summary.items()
    }


# The population-mismatch grounding tokens the frozen plan composer flags on (mirrors
# its `GROUNDING_NEEDS_FLAG`). A non-scalar `grounding` that CONTAINS one is coerced TO it, so
# the mismatch disclosure still fires (fail-toward-flagging) rather than being silently missed.
_GROUNDING_FLAG_TOKENS = ("animal", "in-vitro")


def _normalize_rec(rec):
    """Coerce one recommendation's scalar-contract fields to the frozen plan-composer contract.

    The frozen plan composer string/hashable-processes specific rec fields; a model author emitting a
    LIST/dict there crashes it (the 940o class at the author-output boundary, bead mk0i):
      - `claim` -> `.lower()`  (crashes on a non-string): joined to a string (descriptive text).
      - `category` -> `category in prohibited_classes` (crashes on an unhashable list): a non-scalar
        class is set to None, which routes into the frozen composer's FAIL-CLOSED indeterminate path
        (suppress the actionable content) — NEVER joined, because a joined class would miss the
        prohibited-class set and fail OPEN (an unsafe plan).
      - `grounding` -> `in GROUNDING_NEEDS_FLAG`: a non-scalar preserves an animal/in-vitro marker so
        the population-mismatch flag still fires.
      - `numbers` -> `_is_complete` iterates and calls `number.get(...)` (crashes on a non-dict
        element): filtered to dict-only elements (a malformed number is dropped; a rec left without
        actionable numbers is safe — it renders without dosing, never crashes).
    Every other field (source / confidence_tier / reversibility — presence-checked; `cross_domain` —
    a bool) is left untouched. A non-dict rec passes through unchanged.
    """
    if not isinstance(rec, dict):
        return rec
    out = dict(rec)
    claim = out.get("claim")
    if claim is not None and not isinstance(claim, str):
        out["claim"] = "; ".join(str(x) for x in claim) if isinstance(claim, list) else str(claim)
    category = out.get("category")
    if category is not None and not isinstance(category, str):
        out["category"] = None  # fail-closed -> INDETERMINATE suppress; NEVER join (would fail open)
    grounding = out.get("grounding")
    if grounding is not None and not isinstance(grounding, str):
        marker = next((t for t in _GROUNDING_FLAG_TOKENS
                       if isinstance(grounding, (list, tuple)) and t in grounding), None)
        out["grounding"] = marker or (
            "; ".join(str(x) for x in grounding) if isinstance(grounding, list) else str(grounding))
    if "numbers" in out:
        nums = out["numbers"]
        out["numbers"] = [n for n in nums if isinstance(n, dict)] if isinstance(nums, list) else []
    return out


def normalize_author_output(envelope):
    """Coerce a model AUTHOR envelope's recommendation fields to the frozen plan-composer contract.

    The specialist author is a non-deterministic no-train MODEL; like the de-id model (bead 940o,
    `normalize_summary`), it can emit a LIST/dict where the frozen composer expects a scalar,
    crashing the frozen composer mid-run (bead mk0i, the author-side of the same class). Applied at the
    injectable dispatch seam (`subscription_dispatch.build_dispatch`), UPSTREAM of the frozen
    `run_orchestrated` plan composer — the frozen spine is untouched.

    A no-op on any shape that is NOT an author envelope (a dict carrying a `recommendations` list):
    the same dispatch seam also routes judge / lens verdicts, whose shapes differ and are guarded
    downstream (`gate_dispatch`), so they pass through unchanged.

    Args:
        envelope: The dispatch return — an author envelope `{specialist, recommendations: [...]}`,
            or a judge/lens verdict, or any other shape.

    Returns:
        The author envelope with each recommendation's scalar-contract fields coerced (see
        `_normalize_rec`); any non-author shape returned unchanged.
    """
    if not isinstance(envelope, dict) or not isinstance(envelope.get("recommendations"), list):
        return envelope
    out = dict(envelope)
    out["recommendations"] = [_normalize_rec(r) for r in envelope["recommendations"]]
    return out


class AggregatingDeidClient:
    """A de-id client adapter that (1) aggregates the raw intake's high-cardinality timeseries
    (in-process, deterministically) BEFORE delegating the de-id model call to the inner
    client, so the no-train model receives biomarker summaries instead of thousands of raw
    readings, and (2) normalises the model's de-id OUTPUT to the string-valued shape the
    downstream frozen plan-composition layer / translators expect (bead 940o). Every other client method delegates
    to the inner client unchanged."""

    def __init__(self, inner, *, min_count=DEFAULT_MIN_COUNT, recent_window=DEFAULT_RECENT_WINDOW):
        self._inner = inner
        self._min_count = min_count
        self._recent_window = recent_window

    def deidentify(self, raw_intake):
        """De-identify the intake — collapse its high-cardinality timeseries first, then
        normalise the de-id output's list-valued fields to the string consumer contract."""
        if isinstance(raw_intake, dict) and isinstance(raw_intake.get("operator_state"), list):
            raw_intake = {
                **raw_intake,
                "operator_state": aggregate_operator_state(
                    raw_intake["operator_state"],
                    min_count=self._min_count, recent_window=self._recent_window,
                ),
            }
        return normalize_summary(self._inner.deidentify(raw_intake))

    def __getattr__(self, name):
        # Delegate every non-deidentify method (converse / author / extract_readings) to the
        # inner client. `_inner`/`_min_count`/`_recent_window` exist on self, so they never reach
        # here. A dunder probe (copy/pickle asking for `__deepcopy__`/`__getstate__`) on a
        # half-built instance would hit `__getattr__('_inner')` before __init__ set it — raise
        # cleanly for dunders instead of recursing into a RecursionError.
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(self._inner, name)
