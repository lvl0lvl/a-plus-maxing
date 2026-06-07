"""Tests for the no-train router: summary derivation + payload whitelist gate.

Covers ADR-0006-T1 AC-1..AC-6 + fail-closed + the fga flat-payload pin. The
load-bearing target is AC-4: the payload-field-level WHITELIST raise must fire on
ANY out-of-field-set field — a named-excluded raw-PII field AND a novel field
absent from the named-excluded list — proving the check is "allow only field-set
tokens", not "block known-bad fields".
"""

import pytest

from scripts.plan import router


# --- store-read fakes ----------------------------------------------------------


def _store_read_factory(records):
    """Build a fake store.read returning `records` for any item, recording calls."""
    calls = []

    def fake_read(item, *args, **kwargs):
        calls.append(item)
        return [r for r in records if r["item"] == item]

    fake_read.calls = calls
    return fake_read


def _clean_store_read():
    """A store.read whose state backs every field-set field with a clean token."""
    records = [
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
    return _store_read_factory(records)


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
    assert not sink_calls, "the scalar gate must raise before the model send"
    assert "op.user@gmail.com" not in str(exc.value)


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
