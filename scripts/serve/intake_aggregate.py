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
    """Coerce a model-de-id summary's list-valued fields to `; `-joined strings.

    The no-train de-id MODEL (`deid_in` via `ModelClient`) emits multi-value SUMMARY_FIELD_SET
    fields as LISTS (e.g. `hard-limits: [...]`), but the deterministic `router.summarize` — the
    shape the downstream frozen plan-composition layer / translators consume — emits `; `-joined STRINGS and
    string-processes them (`(summary.get("hard-limits") or "").lower()`). A raw list crashes
    that consumer (`'list' object has no attribute 'lower'`, bead 940o — surfaced at the first
    LIVE run; the mock tests used string-shaped fixtures). This coerces list values to the
    string contract. The fail-closed sentinel (`{"deidentified": False}`) passes through
    unchanged; `deid_in`'s key-whitelist has already validated the KEYS.
    """
    if not isinstance(summary, dict) or summary.get("deidentified") is False:
        return summary
    return {k: ("; ".join(str(x) for x in v) if isinstance(v, list) else v)
            for k, v in summary.items()}


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
        # inner client. `_inner`/`_min_count`/`_recent_window` exist on self, so they never
        # reach here (no recursion).
        return getattr(self._inner, name)
