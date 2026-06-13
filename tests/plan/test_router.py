"""Tests for the no-train router: summary derivation + payload whitelist gate.

Covers ADR-0006-T1 AC-1..AC-6 + fail-closed + the fga flat-payload pin. The
load-bearing target is AC-4: the payload-field-level WHITELIST raise must fire on
ANY out-of-field-set field — a named-excluded raw-PII field AND a novel field
absent from the named-excluded list — proving the check is "allow only field-set
tokens", not "block known-bad fields".
"""

import pytest

from scripts.plan import router
from scripts.store import biomarker_meta


# --- store-read fakes ----------------------------------------------------------


def _store_read_factory(records):
    """Build a fake store.read returning `records` for any item, recording calls."""
    calls = []

    def fake_read(item, *args, **kwargs):
        calls.append(item)
        return [r for r in records if r["item"] == item]

    fake_read.calls = calls
    return fake_read


def _clean_records():
    """The clean record set backing every field-set field with a PII-free token."""
    return [
        {"item": "date-of-birth", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "1986-04-12"},
        {"item": "postal-address", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "123 Main St"},
        {"item": "raw-lab-values", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "lab", "value": "ALT 30; AST 28"},
        {"item": "raw-symptom-free-text", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "tweaked back in January"},
        {"item": "sex-for-dosing", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "male"},
        {"item": "bodyweight-band", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "80-90kg"},
        {"item": "goal-domains", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "strength;recovery"},
        {"item": "goal-targets", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "return to pre-Jan-2026 loading"},
        {"item": "goal-priority-order", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "recovery>strength"},
        {"item": "recovery-status-band", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "moderate"},
        {"item": "hard-limits", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "no overhead pressing"},
    ]


def _clean_store_read():
    """A store.read whose state backs every field-set field with a clean token."""
    return _store_read_factory(_clean_records())


# --- Cycle 1: summarize --------------------------------------------------------


def test_summarize_returns_only_field_set():
    """AC-1: summary field set EQUALS the spike Summary Field-Set, no extra fields."""
    summary = router.summarize(_clean_store_read())
    assert set(summary.keys()) == set(router.SUMMARY_FIELD_SET)


def test_summarize_excludes_named_raw_pii_field():
    """AC-1: a named-excluded raw-PII field in store state is ABSENT from summary."""
    summary = router.summarize(_clean_store_read())
    for excluded in router.EXCLUDED_RAW_PII:
        assert excluded not in summary
    # date-of-birth is a concrete named-excluded field present in store state.
    assert "date-of-birth" not in summary


def test_summarize_emits_no_raw_value_in_any_token():
    """4-1: no raw input VALUE leaks into any summary token (not just the name).

    Plants a distinctive sentinel into each raw-PII source item and asserts the
    sentinel substring is absent from EVERY summary token value — the derivation
    must emit a band/class token, never the raw value. Reds if `_band_token`-style
    passthrough returns the raw value embedded in a whitelisted field.
    """
    sentinels = {
        "date-of-birth": "1986-04-12-SENTINEL",
        "postal-address": "123-SECRET-STREET",
        "raw-lab-values": "ALT-9999-SENTINEL",
        "raw-symptom-free-text": "back-SENTINEL-tweak",
        "clinical-notes": "clinical-SENTINEL-note",
    }
    records = [
        {"item": item, "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": val}
        for item, val in sentinels.items()
    ]
    # Plus clean state for the pass-through field-set fields.
    records += [
        {"item": "goal-targets", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "return to pre-Jan-2026 loading"},
    ]
    summary = router.summarize(_store_read_factory(records))
    token_blob = " ".join(str(v) for v in summary.values())
    for raw_value in sentinels.values():
        assert raw_value not in token_blob, (
            f"raw value {raw_value!r} leaked into a summary token: {summary}"
        )


def test_summarize_reads_through_store():
    """AC-5 + F15: summarize sources state via store.read AND the token data-flows.

    Asserts both call-occurrence AND that a token VALUE derives from the fake
    records — a hardcoded-return `summarize` (ignoring its input) would fail the
    data-flow leg.
    """
    store_read = _clean_store_read()
    summary = router.summarize(store_read)
    # The read callable was the state source: it was invoked.
    assert store_read.calls, "summarize did not invoke the store read model"
    # F15: a token VALUE derives from the supplied records (1986 DOB → born-1980s).
    assert summary["training-age-band"] == "born-1980s"
    # And it tracks the input: a different DOB year produces a different band.
    other = _store_read_factory([
        {"item": "date-of-birth", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "1972-08-09"},
    ])
    assert router.summarize(other)["training-age-band"] == "born-1970s"


def _reading(value):
    """One readings-series record carrying `value` (the derivation input shape)."""
    return [{"item": "x", "timepoint": "2026-01-01T00:00:00+00:00",
             "source": "intake", "value": value}]


@pytest.mark.parametrize("value, expected", [
    ("1986-04-12", "born-1980s"),
    ("1972-08-09", "born-1970s"),
    ("2001-12-31", "born-2000s"),
    ("not-a-date", "age-band-unknown"),
])
def test_age_band_token_value(value, expected):
    """F17: _age_band emits the correct birth-decade band (exact token value)."""
    assert router._age_band(_reading(value)) == expected


@pytest.mark.parametrize("value, expected", [
    ("tweaked my back", "back-region"),
    ("lumbar spine ache", "back-region"),
    ("sore knee", "lower-limb-region"),
    ("hip flexor strain", "lower-limb-region"),
    ("shoulder impingement", "upper-limb-region"),
    ("general fatigue", "general-issue"),
])
def test_issue_class_token_value(value, expected):
    """F17: _issue_class maps free-text to the correct body-region class."""
    assert router._issue_class(_reading(value)) == expected


@pytest.mark.parametrize("value, expected", [
    ("123 Main St", "region-present"),
    ("   ", "region-absent"),
    ("", "region-absent"),
])
def test_region_class_token_value(value, expected):
    """F17: _region_class maps an address to presence/region class."""
    assert router._region_class(_reading(value)) == expected


def test_trend_token_flat_on_no_change():
    """F17/F3: equal latest-vs-prior → `flat` (a determinable no-change)."""
    series = _reading("10") + [{"item": "x", "timepoint": "2026-02-01T00:00:00+00:00",
                                "source": "lab", "value": "10"}]
    assert router._trend_token(series) == "flat"


@pytest.mark.parametrize("series_values", [
    [],            # no readings
    ["10"],        # single reading — insufficient series
    [None, None],  # missing data — must NOT be a false affirmative
    ["x", "y"],    # non-numeric — no determinable direction
])
def test_trend_token_flat_on_insufficient_or_missing(series_values):
    """F3: insufficient/missing series → `flat`, never a false `improving`."""
    series = [{"item": "x", "timepoint": f"2026-0{i + 1}-01T00:00:00+00:00",
               "source": "lab", "value": v} for i, v in enumerate(series_values)]
    token = router._trend_token(series) if series else router._trend_token(
        [{"item": "x", "timepoint": "2026-01-01T00:00:00+00:00",
          "source": "lab", "value": "10"}])
    # The empty-series case is unreachable via summarize (guarded by `if readings`),
    # so exercise the single-reading insufficient case for it.
    assert token == "flat"
    assert token != "improving"


def test_trend_token_uses_spike_vocabulary_only():
    """F3: every _trend_token output is in the closed spike vocabulary."""
    assert set(router.TREND_DIRECTIONS) == {"improving", "flat", "regressing"}
    # The old wrong vocabulary is gone.
    series = _reading("10") + [{"item": "x", "timepoint": "2026-02-01T00:00:00+00:00",
                                "source": "lab", "value": "10"}]
    assert router._trend_token(series) in router.TREND_DIRECTIONS


def test_trend_token_raises_on_unlabellable_directional_change():
    """F3 blocked-gap: a real numeric change with unknown polarity RAISES.

    improving vs regressing needs per-item good-direction polarity, absent from the
    Line Field Set. Rather than fabricate or erase the change, the derivation
    raises — surfacing the spec/metadata gap at the boundary (fail-closed).
    """
    series = _reading("10") + [{"item": "x", "timepoint": "2026-02-01T00:00:00+00:00",
                                "source": "lab", "value": "20"}]
    with pytest.raises(ValueError) as exc:
        router._trend_token(series)
    assert "polarity" in str(exc.value)


def test_trend_token_raises_on_cross_item_series():
    """F8: the two compared numeric readings must come from ONE item.

    A series mixing items (an alt reading then an hrv reading) has no
    single-marker trend; resolving polarity from the last reading's item would
    label the alt-vs-hrv movement `improving`. Fail-closed: raise naming both
    items — never the values.
    """
    series = [
        {"item": "alt", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "lab", "value": 30},
        {"item": "hrv", "timepoint": "2026-02-01T00:00:00+00:00",
         "source": "lab", "value": 50},
    ]
    with pytest.raises(ValueError) as exc:
        router._trend_token(series)
    message = str(exc.value)
    assert "alt" in message and "hrv" in message
    assert "30" not in message and "50" not in message


def _marker_series(item, prev, latest):
    """A two-reading series for `item` carrying the prev/latest values."""
    return [
        {"item": item, "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "lab", "value": prev},
        {"item": item, "timepoint": "2026-02-01T00:00:00+00:00",
         "source": "lab", "value": latest},
    ]


def test_trend_token_registered_up_marker_rising_improves():
    """ADR-0008 D4: a registered "up" marker rising resolves to improving (hrv)."""
    assert router._trend_token(_marker_series("hrv", 50, 60)) == "improving"


def test_trend_token_registered_down_marker_rising_regresses():
    """ADR-0008 D4: a registered "down" marker rising resolves to regressing (alt)."""
    assert router._trend_token(_marker_series("alt", 30, 50)) == "regressing"


def test_trend_token_resolves_prefixed_item_name():
    """ADR-0008 D4: the `biomarker::`-prefixed item name resolves the polarity too."""
    assert router._trend_token(
        _marker_series("biomarker::hrv", 50, 60)
    ) == "improving"


# --- Cycle 2: dispatch ---------------------------------------------------------


def test_dispatch_routes_no_train_lane():
    """AC-2: dispatch routes to the NO-TRAIN lane, not the default/train lane."""
    summary = router.summarize(_clean_store_read())
    result = router.dispatch(summary)
    assert result.lane == router.NO_TRAIN_LANE
    assert result.lane != router.TRAIN_ELIGIBLE_LANE


def test_dispatch_payload_subset_of_field_set():
    """AC-3: model-bound payload field set is a SUBSET of the Summary Field-Set."""
    captured = {}

    def sink(payload):
        captured["payload"] = payload

    summary = router.summarize(_clean_store_read())
    router.dispatch(summary, sink=sink)
    assert "payload" in captured, "model sink was never reached on a clean dispatch"
    assert set(captured["payload"].keys()) <= set(router.SUMMARY_FIELD_SET)


def test_dispatch_clean_path_zero_non_model_egress():
    """AC-3 complement: egress_guard observes 0 store-content egress (non-model path)."""
    from scripts.guard.egress_guard import run

    summary = router.summarize(_clean_store_read())
    # SEC-03: assert the clean path first, so it reds for the right reason.
    assert run(lambda: router.dispatch(summary, sink=lambda p: None))


def test_dispatch_injected_non_model_egress_flips_guard_to_fail():
    """4-3 SEC-03 failing-capable: an outbound call on a dispatch side path -> FAIL.

    Asserts the CLEAN direction truthy FIRST, then injects a synthetic outbound
    call on a non-model side path within the same guarded closure and asserts the
    guard returns falsy — proving the egress complement is failing-capable for the
    router, not merely that a clean dispatch makes 0 calls. Requires network so the
    deny is attributed to the sandbox, not an offline host (mirrors the clone /
    egress_guard suites' precheck discipline).
    """
    import socket

    from scripts.guard.egress_guard import run

    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3).close()
    except OSError:
        pytest.skip("no network — egress deny not exercisable")

    summary = router.summarize(_clean_store_read())
    # Clean direction first: a plain dispatch closure observes 0 egress.
    assert run(lambda: router.dispatch(summary, sink=lambda p: None))

    def dispatch_with_side_egress():
        router.dispatch(summary, sink=lambda p: None)
        socket.create_connection(("1.1.1.1", 53), timeout=3)

    assert not run(dispatch_with_side_egress), (
        "an outbound call on a dispatch side path must flip the guard to FAIL"
    )


def test_dispatch_clean_control_does_not_raise():
    """AC-4 control: a payload of only field-set tokens does NOT raise."""
    summary = router.summarize(_clean_store_read())
    # Control passes (does not raise) — the falsifying baseline for the raise tests.
    router.dispatch(summary, sink=lambda p: None)


def test_dispatch_raises_on_named_excluded_field():
    """AC-4 (i): dispatch RAISES on a NAMED-EXCLUDED raw-PII field, naming it."""
    summary = router.summarize(_clean_store_read())
    summary["email-address"] = "a@b.com"  # named-excluded contact-class field
    with pytest.raises(Exception) as exc:
        router.dispatch(summary, sink=lambda p: None)
    assert "email-address" in str(exc.value)


def test_dispatch_raises_on_novel_out_of_field_set_field():
    """AC-4 (ii) — falsifying whitelist target: a NOVEL out-of-set field RAISES.

    A field absent from BOTH the field-set AND the named-excluded list. A blacklist
    impl (block named-excluded only) PASSES (i) but FAILS this. The whitelist must
    raise because the field is not a field-set member.
    """
    novel = "favorite-color"
    assert novel not in router.SUMMARY_FIELD_SET
    assert novel not in router.EXCLUDED_RAW_PII
    summary = router.summarize(_clean_store_read())
    summary[novel] = "blue"
    with pytest.raises(Exception) as exc:
        router.dispatch(summary, sink=lambda p: None)
    assert novel in str(exc.value)


def test_dispatch_raise_is_field_set_membership_not_call_occurrence():
    """AC-4: the raise fires BEFORE the sink — on field membership, not a call."""
    summary = router.summarize(_clean_store_read())
    summary["phone-number"] = "555-1234"
    sink_calls = []
    with pytest.raises(Exception):
        router.dispatch(summary, sink=lambda p: sink_calls.append(p))
    assert not sink_calls, "raise must precede the model send (not a call-occurrence)"


def test_dispatch_raise_message_names_key_not_value():
    """4-3-LOW: the rejection message carries the field NAME but NOT its value.

    Reds if a future debug-edit appends the offending field's value to the error.
    """
    summary = router.summarize(_clean_store_read())
    secret_value = "PHONE-VALUE-SENTINEL-555"
    summary["phone-number"] = secret_value
    with pytest.raises(Exception) as exc:
        router.dispatch(summary, sink=lambda p: None)
    message = str(exc.value)
    assert "phone-number" in message
    assert secret_value not in message


def test_dispatch_fail_closed_on_raising_summarize():
    """Fail-closed: a summarize that raised → dispatch RAISES, sink un-called."""
    sink_calls = []
    with pytest.raises(Exception):
        router.dispatch(None, sink=lambda p: sink_calls.append(p))
    assert not sink_calls, "dispatch must not send on a failed/absent summary"


def test_dispatch_fail_closed_on_partial_summary():
    """Fail-closed: a malformed/partial summary → dispatch RAISES, sink un-called."""
    partial = {"goal-targets": "x"}  # missing the rest of the field-set
    sink_calls = []
    with pytest.raises(Exception):
        router.dispatch(partial, sink=lambda p: sink_calls.append(p))
    assert not sink_calls, "dispatch must not send a partial-derivation payload"


def test_dispatch_payload_is_flat_scalar(  # fga: N/A-FLAT pin
):
    """fga pin: every model-bound payload value is a scalar (non-container).

    Pins the V1 flat-payload assumption: if a future change introduces a nested
    container under a field-set key, this test turns RED — flagging that the
    shallow `set(payload.fields) ⊆ field_set` whitelist no longer suffices and
    recursion (bead fga) becomes load-bearing.
    """
    captured = {}
    summary = router.summarize(_clean_store_read())
    router.dispatch(summary, sink=lambda p: captured.update({"p": p}))
    for value in captured["p"].values():
        assert not isinstance(value, (dict, list, tuple, set))


def test_dispatch_raises_on_nonscalar_payload_value():
    """fga runtime gate: a container value under an allowlisted field RAISES.

    The shallow field-set whitelist checks NAMES; a raw-PII field smuggled inside a
    nested container under an allowlisted key would pass that name check. The runtime
    scalar gate rejects any non-scalar payload value — a runtime guarantee, not only
    the test-only flat-payload pin. Names the field, never the value; fires before the
    model send.
    """
    summary = router.summarize(_clean_store_read())
    summary["goal-domains"] = ["strength", {"smuggled": "op.user@gmail.com"}]
    sink_calls = []
    with pytest.raises(ValueError) as exc:
        router.dispatch(summary, sink=lambda p: sink_calls.append(p))
    assert "goal-domains" in str(exc.value)
    # Pin that the raise came from the fga scalar gate (not some other check that
    # happens to fire on goal-domains) — reds if the scalar gate is removed (TEST-3).
    assert "non-scalar" in str(exc.value)
    assert not sink_calls, "the scalar gate must raise before the model send"
    assert "op.user@gmail.com" not in str(exc.value)


def test_dispatch_raises_on_bytes_payload_value():
    """fga allowlist (SEC-2): a bytes value (a non-scalar opaque type NOT in the old
    dict/list/tuple/set blacklist) is rejected by the positive scalar allowlist.

    Reds on the old blacklist gate (bytes passed); green on the allowlist (None or
    str/int/float/bool permitted, everything else rejected).
    """
    summary = router.summarize(_clean_store_read())
    summary["goal-targets"] = b"op.user@gmail.com"
    sink_calls = []
    with pytest.raises(ValueError) as exc:
        router.dispatch(summary, sink=lambda p: sink_calls.append(p))
    assert "goal-targets" in str(exc.value)
    assert "non-scalar" in str(exc.value)
    assert not sink_calls


def test_dispatch_allows_none_and_numeric_scalar_values():
    """fga allowlist (SEC-2): None and numeric scalars are permitted (not rejected).

    The positive allowlist must not over-reject legitimate scalar payload values.
    """
    summary = router.summarize(_clean_store_read())
    summary["bodyweight-band"] = 85          # int scalar
    summary["recovery-status-band"] = None    # None permitted
    captured = {}
    router.dispatch(summary, sink=lambda p: captured.update({"p": p}))
    assert captured["p"]["bodyweight-band"] == 85
    assert captured["p"]["recovery-status-band"] is None


# --- 8j6: in-summary pass-through PII value-gate --------------------------------


def test_summarize_raises_on_raw_pii_in_passthrough_field():
    """8j6 fail-closed: raw operator PII in a pass-through field -> summarize RAISES.

    The 7 non-derived field-set fields are read VERBATIM (else-branch). A contact
    token (@gmail.com) typed into a free-text pass-through field (goal-targets) must
    be caught at the summary boundary — the defined 0-raw-PII trust boundary — never
    reaching the model (via dispatch) or the render (via assemble). Names the field,
    not the value (no PII echo in the error).
    """
    # Control: the all-clean baseline does NOT raise (the falsifying baseline).
    router.summarize(_clean_store_read())

    leaky = _store_read_factory([
        {"item": "goal-targets", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "ping me: op.user@gmail.com"},
    ])
    with pytest.raises(ValueError) as exc:
        router.summarize(leaky)
    assert "goal-targets" in str(exc.value)
    assert "op.user@gmail.com" not in str(exc.value)


def test_summarize_pii_gate_is_config_driven_identity(tmp_path):
    """8j6: the gate catches the IDENTITY class too (config-driven), not only contact.

    An operator-identity token in a pass-through value RAISES when the identity
    config supplies it, and does NOT raise without the config (proving the gate is
    config-driven, mirroring pii_scan's identity model).
    """
    cfg = tmp_path / "operator-identity.txt"
    cfg.write_text("# synthetic\nExamplename\n")
    leaky = [
        {"item": "hard-limits", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "ask Examplename before changes"},
    ]
    with pytest.raises(ValueError) as exc:
        router.summarize(_store_read_factory(leaky), identity_config=str(cfg))
    assert "hard-limits" in str(exc.value)
    # Same token, no config -> not detected -> no raise (config-driven).
    router.summarize(_store_read_factory(leaky), identity_config="/nonexistent/x.txt")


def test_summarize_passthrough_accepts_clean_non_str_values():
    """8j6 boundary (TEST-2): a clean non-str pass-through value (int/None) flows
    through verbatim.

    str(80)/str(None) carry no PII, so the gate passes them; pins the
    pass-through-of-non-str contract so a future change that coerced or rejected
    non-str values would be caught.
    """
    store_read = _store_read_factory([
        {"item": "bodyweight-band", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": 80},
        {"item": "recovery-status-band", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": None},
    ])
    summary = router.summarize(store_read)
    assert summary["bodyweight-band"] == 80
    assert summary["recovery-status-band"] is None


def test_summarize_raises_on_container_value_with_embedded_pii():
    """8j6 (TEST-2): a container pass-through value with embedded contact PII RAISES
    at summarize.

    str(list) keeps a whole-token contact in one element visible to scan_text, so the
    8j6 gate catches it at the summary boundary BEFORE dispatch's fga scalar gate
    would reject the container shape — pinning the 8j6/fga interaction.
    """
    leaky = _store_read_factory([
        {"item": "goal-priority-order", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": ["recovery", "email op.user@gmail.com"]},
    ])
    with pytest.raises(ValueError) as exc:
        router.summarize(leaky)
    assert "goal-priority-order" in str(exc.value)


def test_summarize_multi_pii_field_raises_naming_first_in_field_set_order():
    """8j6 (TEST-2): with multiple PII-bearing pass-through fields, the raise names the
    FIRST in SUMMARY_FIELD_SET order (goal-targets precedes hard-limits) — pinning the
    first-raise contract so a reorder/batched-report refactor is caught.
    """
    leaky = _store_read_factory([
        {"item": "goal-targets", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "reach me op.user@gmail.com"},
        {"item": "hard-limits", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "ask coach@gmail.com"},
    ])
    with pytest.raises(ValueError) as exc:
        router.summarize(leaky)
    msg = str(exc.value)
    assert "goal-targets" in msg            # first in SUMMARY_FIELD_SET order
    assert "hard-limits" not in msg         # short-circuits on the first hit


def test_summarize_does_not_gate_derived_fields():
    """8j6 boundary (TEST-4): the gate covers PASS-THROUGH fields only. A derived field
    whose raw source carries contact PII still emits a clean band/class token and does
    NOT raise — the derivation strips the raw value; the gate is on the else-branch
    only. Pins the derived/pass-through branch boundary against silent relocation.
    """
    store_read = _store_read_factory([
        {"item": "raw-symptom-free-text", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "tweaked back; email me op.user@gmail.com"},
    ])
    summary = router.summarize(store_read)
    # active-issue-class is DERIVED from raw-symptom-free-text -> band/class token.
    assert summary["active-issue-class"] == "back-region"
    assert "op.user@gmail.com" not in str(summary)


# --- g5x: widened value boundary blocks the full EXCLUDED_RAW_PII contact classes ---
# Before g5x the summarize gate (scan_text) caught only @gmail.com + identity, so a
# non-gmail email / phone / postal in a free-text pass-through field reached BOTH the
# model sink (dispatch) and the render sink (assemble), which both consume summarize's
# output. summarize is the single upstream boundary: raising there blocks both sinks.

@pytest.mark.parametrize("field, value, secret, label", [
    ("goal-targets", "ping me at op.user@protonmail.com", "op.user@protonmail.com",
     "non-gmail email"),
    ("hard-limits", "ask op.user@googlemail.com first", "op.user@googlemail.com",
     "googlemail"),
    ("goal-targets", "call me +1 415 555 0199 anytime", "415 555 0199", "phone"),
    ("hard-limits", "deliveries to 123 main st, springfield il 62704",
     "123 main st", "postal (nue)"),
])
def test_summarize_raises_on_widened_pii_class_in_passthrough(field, value, secret, label):
    """g5x AC1 + nue: each tractable EXCLUDED_RAW_PII contact class in a pass-through
    RAISES.

    Reds on the gmail-only scan_text (a non-gmail email / phone / postal scored 0 and
    flowed through). The raise names the field, never echoes the value (no PII leak in
    the error). Asserted at the summarize boundary — the single 0-raw-PII boundary
    upstream of BOTH dispatch (model) and assemble (render). The postal row binds the
    nue precise (ZIP/state-anchored, case-insensitive) detector to this boundary.
    """
    # Control: the all-clean baseline does NOT raise (the falsifying baseline).
    router.summarize(_clean_store_read())

    leaky = _store_read_factory([
        {"item": field, "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": value},
    ])
    with pytest.raises(ValueError) as exc:
        router.summarize(leaky)
    assert field in str(exc.value), label
    assert secret not in str(exc.value)


def test_widened_pii_blocks_model_sink_both_paths():
    """g5x AC1 (both sinks): a non-gmail email in a pass-through field never reaches the
    model sink. Built on a COMPLETE clean read with ONLY goal-targets poisoned, so absent
    the widening summarize would COMPLETE and dispatch WOULD send — making this
    failing-capable (the sink IS called on the gmail-only scan_text). The widened gate
    raises at the summarize boundary, upstream of BOTH dispatch (model) and assemble
    (render); the `goal-targets` in the message pins the raise as the PII gate, not the
    partial-summary fail-closed.
    """
    records = _clean_records()
    for record in records:
        if record["item"] == "goal-targets":
            record["value"] = "reach me x@protonmail.com"
    sink_calls = []
    with pytest.raises(ValueError) as exc:
        # The model path: summarize feeds dispatch; the raise precedes any send.
        router.dispatch(
            router.summarize(_store_read_factory(records)),
            sink=lambda p: sink_calls.append(p),
        )
    assert "goal-targets" in str(exc.value)  # the PII gate, not the partial-summary guard
    assert not sink_calls, "widened-PII value must not reach the model sink"


# --- e3b: the caller-binds-clone-root store.read convention ----------------------


def test_summarize_with_root_bound_partial_reads_only_the_clone_store(tmp_path, monkeypatch):
    """e3b: summarize over a caller-bound store.read partial reads ONLY the clone.

    Pins the caller-binds-clone-root convention (S51 adjudication, option b):
    `summarize` keeps its bare `store_read` callable signature and the CALLER
    pre-binds the instance root (`functools.partial(store.read, root=...)`),
    mirroring `generate.run`'s call-site binding (`store.read_all(root)`).
    Mirrors the init_instance Gate B/C clone-isolation shape: DEFAULT_ROOT is
    planted with sentinel state that WOULD surface in the summary if read (a
    1955 DOB + a sentinel goal token). RED-proven: handing summarize the
    unbound `store.read` (the e3b divergence) reads the DEFAULT_ROOT sentinels
    and fails the clone-data assertions.
    """
    from functools import partial

    from scripts.store import store

    # DEFAULT_ROOT is relative (vault/store); chdir sandboxes it under tmp_path.
    monkeypatch.chdir(tmp_path)
    default_sentinels = [
        {"item": "date-of-birth", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "1955-01-01"},
        {"item": "goal-targets", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "DEFAULT-ROOT-SENTINEL"},
    ]
    for record in default_sentinels:
        store.append(record["item"], record, root=store.DEFAULT_ROOT)

    # The clone instance store, every field-set field backed with distinct state.
    clone_root = tmp_path / "clone" / "vault" / "store"
    for record in _clean_records():
        store.append(record["item"], record, root=clone_root)

    summary = router.summarize(partial(store.read, root=clone_root))

    # The summary reflects ONLY the clone's data...
    assert summary["training-age-band"] == "born-1980s"  # clone DOB, not the 1955 plant
    assert summary["goal-targets"] == "return to pre-Jan-2026 loading"
    # ...nothing was read from DEFAULT_ROOT (the planted sentinels never surface)...
    assert "DEFAULT-ROOT-SENTINEL" not in str(summary)
    assert "born-1950s" not in str(summary)
    # ...and the clone store backs the FULL field set (no partial-read fallback).
    assert set(summary.keys()) == set(router.SUMMARY_FIELD_SET)


def test_summarize_clone_missing_item_never_falls_back_to_default_root(tmp_path, monkeypatch):
    """e3b sibling: a clone-missing item is OMITTED, never DEFAULT_ROOT-filled.

    Closes the hole the full-clone sibling leaves open: a per-item fallback
    mutant in `summarize` (empty bound read -> unbound `store.read(item)`)
    PASSES that test, because its clone backs every field-set field and the
    fallback never fires. Here the clone store is `_clean_records()` MINUS the
    `hard-limits` record (`hard-limits` is a pass-through field — in
    `SUMMARY_FIELD_SET`, not in `_RAW_TO_FIELD`) while DEFAULT_ROOT plants a
    `hard-limits` sentinel: a faithful `summarize` OMITS the field; the mutant
    surfaces the sentinel and reds the absence assertions. The partial summary
    then trips `dispatch`'s fail-closed refusal, which names the missing field
    — wrong-instance data never silently completes a model-bound payload.
    """
    from functools import partial

    from scripts.store import store

    # DEFAULT_ROOT is relative (vault/store); chdir sandboxes it under tmp_path.
    monkeypatch.chdir(tmp_path)
    store.append(
        "hard-limits",
        {"item": "hard-limits", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "DEFAULT-ROOT-HARD-LIMIT"},
        root=store.DEFAULT_ROOT,
    )

    # The clone instance store, every field-set field EXCEPT hard-limits.
    clone_root = tmp_path / "clone" / "vault" / "store"
    for record in _clean_records():
        if record["item"] != "hard-limits":
            store.append(record["item"], record, root=clone_root)

    summary = router.summarize(partial(store.read, root=clone_root))

    # The clone-missing field is absent — not filled from DEFAULT_ROOT...
    assert "hard-limits" not in summary
    assert "DEFAULT-ROOT-HARD-LIMIT" not in str(summary)
    # ...and the partial summary trips the fail-closed dispatch refusal by name.
    with pytest.raises(ValueError, match="hard-limits"):
        router.dispatch(summary)


# --- juc: registry-driven worst-wins recent-trend-direction (2026-06-12) --------


def _stream_series(stream, prev, latest):
    """A two-reading series for a `biomarker::` feed stream (prev then latest)."""
    return [
        {"item": stream, "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "lab", "value": prev},
        {"item": stream, "timepoint": "2026-02-01T00:00:00+00:00",
         "source": "lab", "value": latest},
    ]


def test_polarity_feed_is_registry_driven():
    """Decision §1: the feed is EXACTLY the registered-polarity markers, biomarker::.

    Non-tautological membership: registered-polarity markers IN; polarity-less
    markers OUT; every source under the biomarker:: namespace. A hand-typed feed
    that dropped a polarity marker or added a polarity-less one reds here.
    """
    feed = set(router._POLARITY_FEED)
    # Every registered-polarity marker is present (incl. the v1 daily-cadence set).
    for marker in ("ferritin", "vitamin-d", "crp", "alt", "hdl", "ldl",
                   "fasting-glucose", "rhr", "hrv", "sleep-hours"):
        assert f"biomarker::{marker}" in feed, marker
    # Every polarity-less marker is absent (good_direction is None).
    for marker in ("bodyweight", "est-1rm", "steps"):
        assert f"biomarker::{marker}" not in feed, marker
    # Every source is biomarker::-namespaced and resolves to a registered marker.
    for stream in feed:
        assert stream.startswith("biomarker::")
        meta = biomarker_meta.get(stream)
        assert meta is not None and meta["good_direction"] is not None


def test_recent_trend_worst_wins_regressing_dominates():
    """Decision §2: any regressing stream wins over improving + flat streams."""
    store_read = _store_read_factory(
        _stream_series("biomarker::alt", 30, 50)       # down marker rising -> regressing
        + _stream_series("biomarker::hdl", 40, 60)     # up marker rising  -> improving
        + _stream_series("biomarker::crp", 1, 1)       # no change         -> flat
    )
    assert router._recent_trend_direction(store_read) == "regressing"


def test_recent_trend_improving_when_no_regressing():
    """Decision §2: any improving wins when no stream regresses (improving > flat)."""
    store_read = _store_read_factory(
        _stream_series("biomarker::hdl", 40, 60)       # improving
        + _stream_series("biomarker::crp", 1, 1)       # flat
    )
    assert router._recent_trend_direction(store_read) == "improving"


def test_recent_trend_flat_when_all_streams_flat():
    """Decision §2: with only flat streams, the reduction is flat."""
    store_read = _store_read_factory(
        _stream_series("biomarker::crp", 1, 1)
        + _stream_series("biomarker::ferritin", 100, 100)
    )
    assert router._recent_trend_direction(store_read) == "flat"


def test_recent_trend_zero_stream_is_flat():
    """Decision §4: no feed signal at all reduces to the no-signal `flat`."""
    empty = _store_read_factory([])  # no readings for any stream
    assert router._recent_trend_direction(empty) == "flat"


def test_recent_trend_insufficient_stream_contributes_no_false_signal():
    """Decision §2/§4: a <2-reading stream yields no affirmative trend.

    A single-reading stream alone -> flat (never a fabricated improving); the
    same single-reading stream alongside one regressing stream -> regressing
    (the insufficient stream is the worst-wins floor, not a vote).
    """
    one_reading = [{"item": "biomarker::hdl", "timepoint": "2026-01-01T00:00:00+00:00",
                    "source": "lab", "value": 50}]
    assert router._recent_trend_direction(_store_read_factory(one_reading)) == "flat"
    assert router._recent_trend_direction(_store_read_factory(
        one_reading + _stream_series("biomarker::alt", 30, 50)
    )) == "regressing"


def test_recent_trend_resolves_polarity_per_stream_via_registry():
    """Decision §2: each stream's trend is its own registry polarity.

    A rising down-marker (alt) regresses; a rising up-marker (hdl) improves;
    a rising in-range marker moving out of range (fasting-glucose) regresses.
    Each asserted in isolation (only that stream has data).
    """
    assert router._recent_trend_direction(
        _store_read_factory(_stream_series("biomarker::alt", 30, 50))) == "regressing"
    assert router._recent_trend_direction(
        _store_read_factory(_stream_series("biomarker::hdl", 40, 60))) == "improving"
    assert router._recent_trend_direction(
        _store_read_factory(_stream_series("biomarker::hrv", 50, 60))) == "improving"


def test_recent_trend_output_pinned_to_trend_directions():
    """Decision §3: every reduction output is in the closed TREND_DIRECTIONS vocab.

    Pins the function's actual outputs to the locked vocabulary (the load-time
    assert pins the declared `_TREND_REDUCTION_OUTPUTS`; this ties the function to
    it). Reds if a future edit returns an off-vocabulary token like 'rising'.
    """
    assert set(router._TREND_REDUCTION_OUTPUTS) <= set(router.TREND_DIRECTIONS)
    for records in (
        [],
        _stream_series("biomarker::alt", 30, 50),
        _stream_series("biomarker::hdl", 40, 60),
        _stream_series("biomarker::crp", 1, 1),
    ):
        out = router._recent_trend_direction(_store_read_factory(records))
        assert out in router.TREND_DIRECTIONS
        assert out in router._TREND_REDUCTION_OUTPUTS


def test_recent_trend_boundary_disposition_decision_3():
    """Decision §3: raw-lab-values is de-plumbed but stays the boundary promise.

    The raw-lab-values -> recent-trend-direction mapping is REMOVED from
    _RAW_TO_FIELD; raw-lab-values REMAINS in EXCLUDED_RAW_PII; the biomarker::
    feed streams do NOT join EXCLUDED_RAW_PII and are not field-set fields.
    """
    assert "raw-lab-values" not in router._RAW_TO_FIELD
    assert "raw-lab-values" in router.EXCLUDED_RAW_PII
    assert set(router._POLARITY_FEED).isdisjoint(router.EXCLUDED_RAW_PII)
    assert set(router._POLARITY_FEED).isdisjoint(router.SUMMARY_FIELD_SET)
    # recent-trend-direction is no longer a raw-PII-derived field.
    assert "recent-trend-direction" not in router._FIELD_DERIVATION
    assert "recent-trend-direction" not in router._RAW_TO_FIELD.values()


def test_summarize_recent_trend_from_biomarker_feed_worst_wins():
    """End-to-end: summarize derives recent-trend-direction worst-wins from the feed.

    A complete clean state PLUS one regressing biomarker stream -> the summary's
    recent-trend-direction is `regressing`, and the full summary dispatches.
    """
    records = _clean_records() + _stream_series("biomarker::alt", 30, 50)
    summary = router.summarize(_store_read_factory(records))
    assert summary["recent-trend-direction"] == "regressing"
    # The whole summary still dispatches (the field is a clean scalar token).
    result = router.dispatch(summary)
    assert result.payload["recent-trend-direction"] == "regressing"


def test_summarize_recent_trend_present_and_flat_with_no_lab_data():
    """Decision §4 at the summarize boundary: a fresh operator gets `flat`, not partial.

    The clean state has NO biomarker:: streams. recent-trend-direction must be
    PRESENT and `flat` (the no-signal token) — NOT omitted. Failing-capable: a
    revert to the old `if readings`-gated population would omit the field, and the
    dispatch below would raise the partial-summary refusal instead of routing.
    """
    summary = router.summarize(_clean_store_read())
    assert summary["recent-trend-direction"] == "flat"
    result = router.dispatch(summary)  # must NOT raise partial
    assert result.lane == router.NO_TRAIN_LANE
    assert result.payload["recent-trend-direction"] == "flat"


def test_summarize_reads_feed_through_injected_store_read():
    """e3b: the feed streams are read via the INJECTED store_read, not a global.

    Asserts the biomarker:: feed streams appear in the fake read's recorded calls
    — so `_recent_trend_direction` honors the caller-bound clone-root partial that
    `summarize` documents (the feed reads ride the same bound surface, bead e3b).
    """
    store_read = _clean_store_read()
    router.summarize(store_read)
    for stream in router._POLARITY_FEED:
        assert stream in store_read.calls, stream
