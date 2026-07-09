"""Unit coverage for the pre-de-id timeseries aggregation (scripts/serve/intake_aggregate.py).

The aggregation shrinks the model-based `deid_in` payload by collapsing high-cardinality
numeric wearable timeseries to compact per-stream summaries, WITHOUT touching the
PII-bearing / demographic / free-text / genetics readings that must still reach the de-id
boundary. These pin: the collapse + its stats, the pass-through of everything else, the
payload reduction, and the `AggregatingDeidClient` adapter's delegate-else-aggregate contract.
"""

import json

from scripts.serve.intake_aggregate import (
    aggregate_operator_state, normalize_summary, AggregatingDeidClient,
)


def _ts(item, values, source="healthkit"):
    # strictly-increasing timepoints (month rolls after 28 days) so "latest by date" is the
    # last-inserted reading — the aggregation sorts by timepoint, so a cycling date would make
    # "latest" the max-date reading, not the last one.
    return [{"item": item, "timepoint": f"2026-{1 + i // 28:02d}-{1 + i % 28:02d}", "source": source,
             "value": float(v)} for i, v in enumerate(values)]


def test_collapses_high_cardinality_numeric_stream_to_one_summary():
    state = _ts("rhr", list(range(50, 50 + 40)))  # 40 numeric readings
    out = aggregate_operator_state(state, min_count=20)
    rhr = [r for r in out if r["item"] == "rhr"]
    assert len(rhr) == 1, "the 40-reading rhr stream did not collapse to one summary"
    v = rhr[0]["value"]
    assert v["n"] == 40 and rhr[0]["aggregated_from"] == 40
    assert v["min"] == 50 and v["max"] == 89 and v["latest"] == 89
    assert v["mean"] == round(sum(range(50, 90)) / 40, 1)


def test_preserves_low_count_and_non_numeric_readings_verbatim():
    # demographics (low count), free-text (non-numeric), DOB — the PII-bearing set — pass through
    keep = [
        {"item": "date-of-birth", "timepoint": "2026-01-01", "source": "intake", "value": "1970-04-12"},
        {"item": "goal-targets", "timepoint": "2026-01-01", "source": "intake", "value": "longevity"},
        {"item": "raw-symptom-free-text", "timepoint": "2026-01-01", "source": "intake",
         "value": "shoulder pain, call me at 4155550199"},
    ]
    state = keep + _ts("hrv", list(range(30, 30 + 25)))  # + a collapsible stream
    out = aggregate_operator_state(state, min_count=20)
    # every PII-bearing reading survives UNCHANGED (so it still reaches the de-id boundary)
    for r in keep:
        assert r in out, f"a PII-bearing reading was dropped by aggregation: {r['item']}"
    assert sum(1 for r in out if r["item"] == "hrv") == 1  # the timeseries still collapsed


def test_aggregation_reduces_payload_size():
    state = (_ts("rhr", list(range(40, 40 + 500)))
             + [{"item": "goal-targets", "timepoint": "2026-01-01", "source": "x", "value": "longevity"}])
    before = len(json.dumps(state, default=str))
    after = len(json.dumps(aggregate_operator_state(state), default=str))
    assert after < before / 10, f"payload not reduced >=10x (before={before}, after={after})"


def test_boolean_and_mixed_value_streams_are_not_collapsed():
    # bools are not "numeric" for a metric; a mixed stream (some non-numeric) stays raw
    bools = [{"item": "flag", "timepoint": f"2026-01-{i+1:02d}", "source": "x", "value": bool(i % 2)}
             for i in range(30)]
    out = aggregate_operator_state(bools, min_count=20)
    assert sum(1 for r in out if r["item"] == "flag") == 30, "a boolean stream was wrongly collapsed"


def test_normalize_summary_coerces_lists_to_joined_strings():
    # bead 940o: the model de-id emits list-valued fields; the assemble/router.summarize
    # consumer contract is `; `-joined strings (it does hard-limits.lower()).
    summ = {
        "training-age-band": "20-plus-years",              # scalar — unchanged
        "hard-limits": ["overhead-press-restricted", "pullup-restricted"],  # list -> string
        "goal-targets": ["fitness", "longevity"],
    }
    out = normalize_summary(summ)
    assert out["training-age-band"] == "20-plus-years"
    assert out["hard-limits"] == "overhead-press-restricted; pullup-restricted"
    assert out["goal-targets"] == "fitness; longevity"
    # the coerced value survives .lower() (the exact assemble op that crashed on a list)
    assert out["hard-limits"].lower() == "overhead-press-restricted; pullup-restricted"


def test_normalize_summary_passes_fail_closed_sentinel_through():
    sentinel = {"deidentified": False, "reason": "deid-call-failed"}
    assert normalize_summary(sentinel) is sentinel


class _RecordingClient:
    def __init__(self, deid_return=None):
        self.deid_input = None
        self.authored = None
        self._deid_return = deid_return if deid_return is not None else {"training-age-band": "50-plus"}

    def deidentify(self, raw_intake):
        self.deid_input = raw_intake
        return self._deid_return

    def author(self, domain, summary):
        self.authored = (domain, summary)
        return {"specialist": "x", "recommendations": []}


def test_adapter_aggregates_deidentify_input_and_delegates_other_methods():
    inner = _RecordingClient()
    client = AggregatingDeidClient(inner, min_count=20)
    raw = {"operator_state": _ts("rhr", list(range(50, 50 + 40)))
           + [{"item": "date-of-birth", "timepoint": "2026-01-01", "source": "i", "value": "1970-04-12"}]}
    out = client.deidentify(raw)
    # inner saw the AGGREGATED input (rhr collapsed to 1), DOB preserved
    got = inner.deid_input["operator_state"]
    assert sum(1 for r in got if r["item"] == "rhr") == 1
    assert any(r["item"] == "date-of-birth" for r in got)
    assert out == {"training-age-band": "50-plus"}
    # a non-deidentify method delegates straight through to the inner client
    assert client.author("workout", {"x": 1}) == {"specialist": "x", "recommendations": []}
    assert inner.authored == ("workout", {"x": 1})


def test_adapter_normalizes_list_valued_deid_output():
    # bead 940o: the adapter coerces the model's list-valued summary output to the string
    # contract, so a downstream `assemble` string op does not crash on the live path.
    inner = _RecordingClient(deid_return={"hard-limits": ["overhead-press-restricted", "pullup-restricted"],
                                          "training-age-band": "20-plus-years"})
    out = AggregatingDeidClient(inner).deidentify({"operator_state": []})
    assert out["hard-limits"] == "overhead-press-restricted; pullup-restricted"
    assert out["training-age-band"] == "20-plus-years"
