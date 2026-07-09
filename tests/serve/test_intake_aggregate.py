"""Unit coverage for the pre-de-id timeseries aggregation (scripts/serve/intake_aggregate.py).

The aggregation shrinks the model-based `deid_in` payload by collapsing high-cardinality
numeric wearable timeseries to compact per-stream summaries, WITHOUT touching the
PII-bearing / demographic / free-text / genetics readings that must still reach the de-id
boundary. These pin: the collapse + its stats, the pass-through of everything else, the
payload reduction, and the `AggregatingDeidClient` adapter's delegate-else-aggregate contract.
"""

import importlib
import json

import pytest

from scripts.serve.intake_aggregate import (
    aggregate_operator_state, normalize_summary, normalize_author_output, AggregatingDeidClient,
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


@pytest.mark.parametrize("bad_value", [
    ["overhead-press-restricted", "pullup-restricted"],   # the OBSERVED live shape (list)
    {"shoulder": "no-overhead"},                          # dict (BUG-940O-01)
    True,                                                 # bool (BUG-940O-01)
])
def test_normalized_output_is_consumable_by_the_real_assemble_filter(bad_value):
    """bead 940o / BUG-940O-01: the FIX must run the PRODUCTION crash path, not an inline .lower().

    The real consumer `assemble._prohibited_classes` does `(summary.get("hard-limits") or "").lower()`
    — a NON-STRING value crashes it. This pins that (a) the UN-normalized model value RAISES at the
    real consumer (normalize is load-bearing, not decorative), and (b) the normalized value is
    consumed without raising. Covers the list shape (observed) + dict/bool (BUG-940O-01)."""
    assemble = importlib.import_module("scripts.plan.assemble")
    raw = {"hard-limits": bad_value}
    with pytest.raises(AttributeError):
        assemble._prohibited_classes(raw)                 # un-normalized non-string -> the 940o crash
    # normalized -> a string -> the consumer runs without raising
    assert isinstance(assemble._prohibited_classes(normalize_summary(raw)), (set, frozenset, list, tuple))


def test_normalized_rx_classes_parse_for_the_bpmh_screen():
    """contracts-320 (safety RESCUE): a raw LIST at rx-interaction-classes makes the supplement<->Rx
    BPMH screen (`router.rx_interaction_class_set`) return an EMPTY set — a silent 'no medication
    interactions' hole. normalize coerces it to the `;`-parsed string the screen reads, so the
    operator's present Rx-interaction classes are actually seen."""
    router = importlib.import_module("scripts.plan.router")
    normalized = normalize_summary({"rx-interaction-classes": ["bleeding-risk", "cyp3a4-pgp"]})
    got = router.rx_interaction_class_set(normalized)
    assert "bleeding-risk" in got and "cyp3a4-pgp" in got, got


@pytest.mark.parametrize("n, collapses", [(19, False), (20, True)])
def test_min_count_collapse_boundary(n, collapses):
    """TC-320-02: the >=min_count collapse trigger is the feature's crux (collapse vs pass-raw).
    Exactly min_count-1 must pass through raw (a PII-bearing stream must NOT be collapsed away);
    exactly min_count must collapse. Kills the `>=`->`>` off-by-one mutation."""
    out = aggregate_operator_state(_ts("rhr", list(range(50, 50 + n))), min_count=20)
    rhr = [r for r in out if r["item"] == "rhr"]
    if collapses:
        assert len(rhr) == 1 and rhr[0].get("aggregated_from") == n
    else:
        assert len(rhr) == n and all("aggregated_from" not in r for r in rhr)


def test_summary_stats_and_recent_window_trend():
    """TC-320-03: pin median, span, and the recent_mean trailing-window slice (the material stat —
    the recent-vs-overall trend signal fed to the de-id model). A stream LONGER than recent_window
    with a flat-then-rising trend makes recent_mean differ from the overall mean."""
    values = [50] * 100 + [90] * 20   # 120 readings: flat 50, then rising 90
    out = aggregate_operator_state(_ts("rhr", values), min_count=20, recent_window=20)
    v = [r for r in out if r["item"] == "rhr"][0]["value"]
    assert v["span"] == ["2026-01-01", "2026-05-08"]              # [first, last] timepoint
    assert v["median"] == 50                                      # 100 of 120 are 50
    assert v["recent_mean"] == 90.0 and v["mean"] != v["recent_mean"]  # trailing window = the rising tail


def test_adapter_passes_fail_closed_sentinel_through():
    """TC-320-04: the adapter's fail-closed de-id-failure sentinel passthrough — a future adapter
    post-process could mangle the crown-jewel fail-closed marker; pin it at the adapter seam."""
    sentinel = {"deidentified": False, "reason": "deid-call-failed"}
    out = AggregatingDeidClient(_RecordingClient(deid_return=sentinel)).deidentify({"operator_state": []})
    assert out == sentinel and out.get("deidentified") is False


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


# --- mk0i: the AUTHOR-output boundary (the author-side of the 940o class) --------------------


def test_normalize_author_output_coerces_scalar_contract_rec_fields():
    """bead mk0i: the model author can emit a LIST/dict where `assemble` string/hashable-processes
    a scalar. Pin each coercion: claim joined; category -> None (FAIL-CLOSED, never joined);
    grounding preserves the animal/in-vitro flag token; malformed `numbers` elements dropped;
    structured/scalar fields untouched."""
    env = {"specialist": "P", "recommendations": [{
        "claim": ["do X", "do Y"], "category": ["stimulant", "other"], "grounding": ["animal", "human"],
        "source": "Smith 2024", "confidence_tier": "moderate", "reversibility": "reversible",
        "numbers": ["3 sets", {"value": "3", "units": "sets", "reference_range": "2-5"}],
    }]}
    r = normalize_author_output(env)["recommendations"][0]
    assert r["claim"] == "do X do Y"                        # SPACE-joined (SEC-02: "; " would split a limit phrase)
    assert r["category"] is None                            # fail-closed (NOT "stimulant; other" — would fail open)
    assert r["grounding"] == "animal"                       # flag token preserved (population-mismatch still fires)
    assert r["numbers"] == [{"value": "3", "units": "sets", "reference_range": "2-5"}]  # non-dict dropped
    assert r["source"] == "Smith 2024" and r["reversibility"] == "reversible"  # untouched


def test_normalize_author_output_is_noop_on_non_author_shapes():
    # the dispatch seam also routes judge / lens verdicts (different shapes, guarded downstream) —
    # normalize must pass them through unchanged, keyed on the presence of a `recommendations` list.
    for shape in ({"scores": {"quality": 8}}, {"verdict": "pass"}, {"recommendations": "not-a-list"},
                  "sentinel", ["x"], None):
        assert normalize_author_output(shape) == shape or normalize_author_output(shape) is shape


def _author_summary(hard_limits):
    """A minimal frozen-composer summary carrying an explicit `hard-limits` (self-contained tests)."""
    return {"training-age-band": "x", "hard-limits": hard_limits, "goal-domains": "s"}


def test_normalized_author_output_is_consumable_by_the_real_assemble_AND_fails_closed():
    """bead mk0i (real-consumer pin): drive the model's realistic LIST-shaped author envelope through
    the REAL `assemble()`. Self-contained (TEST-03): its OWN summary + a hard-limit whose subject the
    benign claim cannot assert, so category->None (indeterminate) is the ONLY route to the strike —
    the RED-capability cannot silently erode via the literal-claim HALT path.

    Arm 1 (RED-capable): the raw list-shaped author envelope RAISES at the real `assemble()` (the
    unprotected mk0i crash). Arm 2: the coerced envelope composes WITHOUT raising AND fails CLOSED —
    the list `category` became indeterminate so the rec's actionable content is SUPPRESSED (a joined
    category would have missed the prohibited set and fail OPEN)."""
    from scripts.plan.assemble import assemble

    summary = _author_summary("no stimulants")   # benign claim "hydrate well" cannot assert this subject
    bad_env = {"specialist": "P", "recommendations": [{
        "claim": ["hydrate well"], "category": ["stimulant", "other"], "grounding": "human",
        "source": "Smith 2024", "confidence_tier": "moderate", "reversibility": "reversible",
        "numbers": ["3 sets"],
    }]}
    with pytest.raises((AttributeError, TypeError)):
        assemble(["perf"], summary, {"perf": lambda d, s: bad_env})   # unprotected mk0i crash

    section = assemble(["perf"], summary,
                       {"perf": lambda d, s: normalize_author_output(bad_env)})["sections"][0]
    recs = section["recommendations"]
    assert len(recs) == 1                                            # composed, no crash
    assert recs[0].get("indeterminate_class_suppressed") is True     # FAIL-CLOSED (category->None->indeterminate)
    assert recs[0].get("actionable_content_struck") is True          # actionable content suppressed
    assert "indeterminate" in (recs[0].get("contradiction_disposition") or "").lower()  # the indeterminate CAUSE
    assert "numbers" not in recs[0]                                  # struck-indeterminate removed the regimen


@pytest.mark.parametrize("cat, struck", [
    ("stimulant", True),          # canonical -> struck
    ("Stimulant", True),          # SEC-01: capitalized -> canonicalized -> struck
    (" stimulant ", True),        # SEC-01: whitespace -> struck
    ("stimulant\n", True),        # SEC-01: trailing newline -> struck
    ("", True),                   # SEC-01: empty -> None -> indeterminate -> struck
    ("stimulants", False),        # RESIDUAL (documented): plural misses the frozen exact-match set
])
def test_scalar_category_canonicalized_against_the_real_assemble_halt(cat, struck):
    """SEC-01: a scalar-string `category` is canonicalized (`strip().lower() or None`) so case /
    whitespace / empty variants still hit the frozen composer's EXACT lowercase-singular
    prohibited-class set (fail-closed strike) instead of shipping ACTIONABLE (fail-open). The plural
    variant remains a documented residual (needs the frozen class-token map — tracked)."""
    from scripts.plan.assemble import assemble
    env = {"specialist": "P", "recommendations": [{
        "claim": "hydrate well", "category": cat, "grounding": "human", "source": "S 2024",
        "confidence_tier": "moderate", "reversibility": "reversible",
        "numbers": [{"value": "1", "units": "u", "reference_range": "1-2"}]}]}
    rec = assemble(["perf"], _author_summary("no stimulants"),
                   {"perf": lambda d, s: normalize_author_output(env)})["sections"][0]["recommendations"][0]
    assert bool(rec.get("actionable_content_struck")) is struck


def test_dict_grounding_preserves_population_mismatch_flag():
    """SEC-03 / TEST-02: an animal/in-vitro marker held in a DICT `grounding` value (not just a
    list/tuple element) is preserved, so the frozen composer's population-mismatch disclosure still
    fires — matching `_normalize_rec`'s docstring contract."""
    from scripts.plan.assemble import assemble
    env = {"specialist": "P", "recommendations": [{
        "claim": "consider X", "category": "training", "grounding": {"evidence": "animal"},
        "source": "S 2024", "confidence_tier": "moderate", "reversibility": "reversible",
        "numbers": [{"value": "1", "units": "u", "reference_range": "1-2"}]}]}
    assert normalize_author_output(env)["recommendations"][0]["grounding"] == "animal"
    rec = assemble(["perf"], _author_summary("none"),
                   {"perf": lambda d, s: normalize_author_output(env)})["sections"][0]["recommendations"][0]
    assert rec.get("population_mismatch_flag") is True


def test_clean_populated_author_envelope_passes_through_unchanged():
    """TEST-01: a WELL-FORMED populated author envelope is a value-preserving no-op — the normalizer
    must never silently alter a valid plan (no field coerced, no number dropped), and the real
    `assemble()` emits it ACTIONABLE (not struck)."""
    from scripts.plan.assemble import assemble
    clean = {"specialist": "P", "recommendations": [{
        "claim": "progressive overload", "category": "training", "grounding": "human",
        "source": "RCT 2024", "confidence_tier": "moderate", "reversibility": "reversible",
        "numbers": [{"value": "3", "units": "sets", "reference_range": "2-5"}]}]}
    assert normalize_author_output(clean) == clean            # verbatim (canonical fields unchanged)
    rec = assemble(["perf"], _author_summary(""),            # no hard limit -> HALT_CLEAR (not struck)
                   {"perf": lambda d, s: normalize_author_output(clean)})["sections"][0]["recommendations"][0]
    assert not rec.get("actionable_content_struck")           # a valid rec is emitted actionable
    assert rec["numbers"] == [{"value": "3", "units": "sets", "reference_range": "2-5"}]


def test_grounding_flag_tokens_mirror_the_frozen_composer_no_desync():
    """HIST-01 / QUAL-01: `_GROUNDING_FLAG_TOKENS` byte-mirrors the frozen composer's
    `GROUNDING_NEEDS_FLAG`; the change-control tripwire lives here (a test importing `assemble` does
    not trip the serve-layer 'assemble'-grep guard, which scans only scripts/serve/*.py). Fails on
    any future desync — the CI-time analogue of the codebase's module-load desync asserts."""
    from scripts.plan.assemble import GROUNDING_NEEDS_FLAG
    import scripts.serve.intake_aggregate as agg
    assert agg._GROUNDING_FLAG_TOKENS == GROUNDING_NEEDS_FLAG
