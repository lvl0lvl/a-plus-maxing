"""Tests for the no-train router: summary derivation + payload whitelist gate.

Covers ADR-0006-T1 AC-1..AC-6 + fail-closed + the fga flat-payload pin. The
load-bearing target is AC-4: the payload-field-level WHITELIST raise must fire on
ANY out-of-field-set field — a named-excluded raw-PII field AND a novel field
absent from the named-excluded list — proving the check is "allow only field-set
tokens", not "block known-bad fields".
"""

from pathlib import Path

import pytest

from scripts.plan import router
from scripts.store import biomarker_meta


def _expected_age(iso_dob):
    """The exact integer age (as a str) for `iso_dob` relative to today's UTC date.

    Mirrors `router._age_band`'s computation so the exact-age assertion is grounded in the
    run date, not a literal that goes stale — the load-bearing non-tautology check is the
    A != B difference (a constant-return deriver reds it).
    """
    from datetime import datetime, timezone
    dob = datetime.strptime(iso_dob, "%Y-%m-%d").date()
    today = datetime.now(timezone.utc).date()
    return str(today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))


# The pinned pre-edit Summary Field-Set membership (AC-1). The OQ-5 repurpose changes
# `training-age-band`/`bodyweight-band`'s DERIVATION, never the tuple — this literal proves
# no token was added or removed (byte-identical field set).
_PINNED_FIELD_SET = (
    "training-age-band",
    "training-experience-band",
    "sex-for-dosing",
    "bodyweight-band",
    "equipment-access-class",
    "goal-domains",
    "goal-targets",
    "goal-priority-order",
    "recovery-status-band",
    "active-issue-class",
    "hard-limits",
    "recent-trend-direction",
    "rx-interaction-classes",
    "dietary-pattern-class",
    "supplement-stack-class",
    "peptide-use-class",
    "training-volume-band",
    "genetic-trait-classes",
)


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
        # equipment-access-class is now a pass-through token sourced from the demographic
        # equipment selection (ADR-0018-T1 reconciliation) — an OWN-NAME store item, not
        # the removed postal-address derivation. The value is a member of the bounded
        # equipment-access enum the Step-1 select is built from (AC-6 markup<->gate no-drift).
        {"item": "equipment-access-class", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "full-home-gym"},
        {"item": "raw-lab-values", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "lab", "value": "ALT 30; AST 28"},
        {"item": "raw-symptom-free-text", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "tweaked back in January"},
        {"item": "sex-for-dosing", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "male"},
        # OQ-5 repurpose: bodyweight-band is now DERIVED from the local `bodyweight-kg`
        # dated series (current weight + trend), never a directly-stored pass-through band.
        {"item": "bodyweight-kg", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "85.0"},
        {"item": "bodyweight-kg", "timepoint": "2026-02-01T00:00:00+00:00",
         "source": "intake", "value": "82.0"},
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
    # F15: a token VALUE derives from the supplied records (full DOB → exact age).
    assert summary["training-age-band"] == _expected_age("1986-04-12")
    # And it tracks the input: a different DOB year produces a different age.
    other = _store_read_factory([
        {"item": "date-of-birth", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "1972-08-09"},
    ])
    assert router.summarize(other)["training-age-band"] == _expected_age("1972-08-09")
    assert summary["training-age-band"] != router.summarize(other)["training-age-band"]


def _reading(value):
    """One readings-series record carrying `value` (the derivation input shape)."""
    return [{"item": "x", "timepoint": "2026-01-01T00:00:00+00:00",
             "source": "intake", "value": value}]


@pytest.mark.parametrize("iso_dob", [
    "1986-04-12",
    "1972-08-09",
    "2001-12-31",
    "  1986-04-12  ",   # surrounding whitespace is stripped before parsing
    "1900-01-01",
])
def test_age_band_exact_age_from_full_dob(iso_dob):
    """OQ-5 (AC-2): _age_band emits the EXACT integer age (years) from the full ISO DOB —
    computed dynamically relative to today's UTC date, never a born-decade band."""
    assert router._age_band(_reading(iso_dob)) == _expected_age(iso_dob.strip())


@pytest.mark.parametrize("value", [
    "not-a-date",
    "1986",          # a bare year is no longer a parseable full DOB
    "86",
    "198",
    "1986-13-40",    # out-of-range month/day — unparseable
    "3026-01-01",    # future-dated — never fabricate an age
])
def test_age_band_unparseable_or_future_is_sentinel(value):
    """OQ-5 (AC-3 fail-safe): a malformed/unparseable or future-dated DOB derives the
    `age-unknown` sentinel rather than crashing or echoing the raw value."""
    token = router._age_band(_reading(value))
    assert token == "age-unknown"
    assert value.strip() not in token  # the raw value never survives into the sentinel


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


# NOTE (ADR-0018-T1): the former `test_region_class_token_value` parametrized test is
# removed. It exercised `router._region_class`, the postal-address -> equipment-access-class
# deriver, which the reconciliation removed (the demographic equipment selection is now the
# token's one source). The function no longer exists; the test that called it is gone, not
# weakened. `equipment-access-class`'s new pass-through sourcing is covered by
# `tests/serve/test_intake_demographics.py` (the demographic round-trip) and the
# `_clean_records()` own-name fixture above (field-set completeness for the dispatch tests).


def test_postal_address_no_longer_derives_equipment_access_class():
    """ADR-0018-T1: postal-address is removed as the equipment-access-class source.

    The reconciliation pins ONE source for `equipment-access-class` — the demographic
    equipment selection (a pass-through token). The former `postal-address` derivation is
    gone: `postal-address` is no longer in `_RAW_TO_FIELD`, `equipment-access-class` is no
    longer in `_FIELD_DERIVATION`, and `_region_class` is removed. `postal-address` STAYS a
    named-excluded raw-PII class (the boundary promise is unchanged).

    Failing-capable: re-adding `postal-address -> equipment-access-class` to `_RAW_TO_FIELD`
    (the double-source the AC reconciles) reds this.
    """
    assert "postal-address" not in router._RAW_TO_FIELD, (
        "postal-address still maps in _RAW_TO_FIELD — the equipment double-source is back"
    )
    assert "equipment-access-class" not in router._FIELD_DERIVATION, (
        "equipment-access-class is still a derived field — it must be a pass-through token"
    )
    assert not hasattr(router, "_region_class"), (
        "_region_class still exists — the postal-address deriver was not removed"
    )
    # The boundary promise is unchanged: postal-address stays named-excluded raw PII.
    assert "postal-address" in router.EXCLUDED_RAW_PII, (
        "postal-address was wrongly dropped from EXCLUDED_RAW_PII"
    )


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
    # `equipment-access-class` is a still-pass-through token (read under its own name);
    # `bodyweight-band` is no longer pass-through (OQ-5 derives it from `bodyweight-kg`).
    store_read = _store_read_factory([
        {"item": "equipment-access-class", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": 80},
        {"item": "recovery-status-band", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": None},
    ])
    summary = router.summarize(store_read)
    assert summary["equipment-access-class"] == 80
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
    # yduw (FINDING-1, crown-jewel): a full DOB typed into a pass-through field.
    # Security EXECUTED this at the T9 review — it crossed VERBATIM to the no-train
    # dispatch + the clarifying model request, because scan_text had no date detector.
    # This row RED'd on the pre-yduw code and lands WITH the pii_scan DOB detector.
    ("goal-targets", "reach peak by birthday 1986-03-14", "1986-03-14",
     "DOB in pass-through (yduw)"),
    # 6hts: a canonical TWO-LINE mailing address (street line \n city/ZIP line) in a
    # pass-through field — caught by the [\s\S] street->ZIP span.
    ("hard-limits", "mail me at 123 Main St\nSpringfield, IL 62704", "123 Main St",
     "two-line postal (6hts)"),
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
    assert summary["training-age-band"] == _expected_age("1986-04-12")  # clone DOB, not the 1955 plant
    assert summary["goal-targets"] == "return to pre-Jan-2026 loading"
    # ...nothing was read from DEFAULT_ROOT (the planted sentinels never surface)...
    assert "DEFAULT-ROOT-SENTINEL" not in str(summary)
    # ...and the crown jewel holds: neither full-DOB string (the clone's OR the 1955 plant)
    # crosses — only the de-associated exact age does.
    assert "1955-01-01" not in str(summary)
    assert "1986-04-12" not in str(summary)
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
    assert router._recent_trend_direction(_store_read_factory(
        _stream_series("biomarker::fasting-glucose", 90, 200))) == "regressing"


def test_recent_trend_in_range_marker_staying_in_range_is_flat():
    """Decision §2: an in-range marker moving but staying in range -> flat.

    fasting-glucose 90 -> 95 are both inside (70, 99): distance-to-range stays
    0, so the trend is the no-change `flat` (the in-range polarity branch
    through the feed reduction, distinct from the trivial equal-value case).
    """
    assert router._recent_trend_direction(_store_read_factory(
        _stream_series("biomarker::fasting-glucose", 90, 95))) == "flat"


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


# --- smei: in-range feed markers must carry a reference_range ---


def test_smei_in_range_feed_markers_all_carry_a_range():
    """smei: every in-range-polarity feed marker carries a reference_range.

    `biomarker_meta.trend` judges an in-range marker by distance-to-range, so an
    in-range feed marker with no range yields None -> `_trend_token` raises ->
    the WHOLE plan summary fail-closes. Pins the invariant the load-time tripwire
    guards; RED if a future registry edit adds an in-range feed marker with no
    range.
    """
    for stream in router._POLARITY_FEED:
        meta = biomarker_meta.get(stream)
        if meta["good_direction"] == "in-range":
            assert meta["reference_range"] is not None, stream


def test_smei_in_range_without_range_trips_load_assert():
    """smei: an in-range feed marker with no range trips the load-time tripwire.

    Fail-capable: inject an in-range marker with reference_range=None into the
    registry and reload router; the smei tripwire must raise AssertionError. A
    removed/weakened assert lets the reload succeed and turns this RED. The
    finally clause restores the real registry and reloads a clean router for the
    rest of the suite.
    """
    import importlib

    original = biomarker_meta.METADATA
    try:
        biomarker_meta.METADATA = {
            **original,
            "smei-probe": {
                "units": "x",
                "reference_range": None,
                "good_direction": "in-range",
            },
        }
        with pytest.raises(AssertionError):
            importlib.reload(router)
    finally:
        biomarker_meta.METADATA = original
        importlib.reload(router)


# --- rxbp: the supplement<->Rx BPMH PII boundary (de-identified Rx classes) -----


def _rx_records(rx_classes_value=None, **extra):
    """Clean field-set records, optionally seeding the curated `rx-interaction-classes` item.

    `extra` injects additional raw store items (e.g. a raw `medication-list`) for the adversarial
    leak tests.
    """
    records = _clean_records()
    if rx_classes_value is not None:
        records.append({"item": "rx-interaction-classes", "timepoint": "2026-01-01T00:00:00+00:00",
                        "source": "intake", "value": rx_classes_value})
    for item, val in extra.items():
        records.append({"item": item, "timepoint": "2026-01-01T00:00:00+00:00",
                        "source": "intake", "value": val})
    return records


def test_rx_interaction_classes_always_set_empty_default():
    """No-meds operator: the field is ALWAYS present and defaults to the empty token.

    Mirrors `recent-trend-direction`'s always-set contract — a no-medication operator must NOT
    trip dispatch's partial-summary raise. Reds if the field is set only `if readings`.
    """
    summary = router.summarize(_clean_store_read())  # no rx-interaction-classes item seeded
    assert summary["rx-interaction-classes"] == ""
    assert set(summary.keys()) == set(router.SUMMARY_FIELD_SET)  # field present, summary complete


def test_rx_interaction_classes_passes_curated_tokens():
    """The curated de-identified class tokens cross the boundary, normalized (sorted/lower/dedup)."""
    summary = router.summarize(_store_read_factory(
        _rx_records("CYP3A4-pgp; bleeding-risk; bleeding-risk")
    ))
    assert summary["rx-interaction-classes"] == "bleeding-risk;cyp3a4-pgp"  # deduped + sorted + lowered


def test_summarize_drops_raw_medication_list_never_leaks():
    """ADVERSARIAL PII (AC1): a raw `medication-list` free-text never survives `summarize`.

    The raw medication free-text (drug names + a prescriber note) is a named-excluded raw-PII class
    with NO derivation — `summarize` never reads it. Only the operator/liaison-curated
    `rx-interaction-classes` tokens cross. Reds if a future wiring routes the raw item into the
    summary (e.g. backing the field off `medication-list`): the planted raw substrings would appear.
    """
    raw_meds = "warfarin 5mg nightly; atorvastatin 40mg — Dr-SENTINEL-Smith"
    summary = router.summarize(_store_read_factory(
        _rx_records("anticoagulant;bleeding-risk", **{"medication-list": raw_meds})
    ))
    token_blob = " ".join(str(v) for v in summary.values())
    for leaked in ("warfarin", "atorvastatin", "Dr-SENTINEL-Smith", "5mg"):
        assert leaked not in token_blob, f"raw medication substring {leaked!r} leaked: {summary}"
    # the curated class tokens DID cross (the de-identified surface is what the BPMH screen reads).
    assert summary["rx-interaction-classes"] == "anticoagulant;bleeding-risk"
    assert "medication-list" not in summary  # the raw item is never a summary field


def test_rx_interaction_classes_8j6_pii_backstop_raises():
    """The 8j6 pass-through PII gate is the runtime backstop on the curated value (mutation-proof).

    The class tokens are de-identified BY the curation contract, but that contract is unenforced
    upstream — so a mis-curated value carrying raw operator PII (a prescriber phone) RAISES at the
    boundary rather than crossing. Reds if the 8j6 scan is removed from the deriver: the PII would
    pass through and this expected raise would not fire.
    """
    with pytest.raises(ValueError) as exc:
        router.summarize(_store_read_factory(
            _rx_records("anticoagulant; call +14155550123")
        ))
    assert "rx-interaction-classes" in str(exc.value)
    assert "fail-closed" in str(exc.value)
    assert "+14155550123" not in str(exc.value)  # names the field, never echoes the PII value


def test_medication_list_rejected_by_dispatch_whitelist():
    """AC1 belt: the raw `medication-list` is named-excluded, so the dispatch whitelist rejects it.

    Proves the boundary is allow-only-field-set, not block-known-bad: even if a raw medication field
    were injected into a payload, `dispatch` raises before any send.
    """
    summary = router.summarize(_clean_store_read())
    summary["medication-list"] = "warfarin 5mg"  # inject the raw raw-PII field
    with pytest.raises(ValueError) as exc:
        router.dispatch(summary)
    assert "medication-list" in str(exc.value)


@pytest.mark.parametrize("value,expected", [
    ("bleeding-risk;cyp3a4-pgp", {"bleeding-risk", "cyp3a4-pgp"}),
    ("  Bleeding-Risk ; ANTICOAGULANT ", {"bleeding-risk", "anticoagulant"}),
    ("", set()),
    (";;", set()),
])
def test_rx_interaction_class_set_parses(value, expected):
    """The orchestrator's parser normalizes the `;`-joined scalar into a token set."""
    assert router.rx_interaction_class_set({"rx-interaction-classes": value}) == expected


def test_rx_interaction_class_set_absent_field_is_empty():
    """A summary predating the field (or a non-str value) yields the empty set — no Rx surface."""
    assert router.rx_interaction_class_set({}) == set()
    assert router.rx_interaction_class_set({"rx-interaction-classes": None}) == set()


def test_rx_interaction_classes_8j6_backstop_scans_past_scan_text_cap():
    """SEC-1 regression: the 8j6 backstop scans PER TOKEN, not the truncated whole value.

    pii_scan.scan_text truncates its input at _MAX_SCAN_TEXT_LEN; a `;`-joined class list can
    legitimately exceed it. A whole-value scan elides PII past the cap — a real de-identification-
    boundary leak. The per-token scan keeps every scanned unit short, so trailing PII in a long
    curated value still RAISES. Reds if the deriver reverts to scanning the whole `;`-joined value.
    """
    long_value = ";".join(["bleeding-risk"] * 400) + "; contact dr.smith@example.com"
    assert len(long_value) > 4096  # past the scan_text cap — a whole-value scan would elide the tail
    with pytest.raises(ValueError) as exc:
        router.summarize(_store_read_factory(_rx_records(long_value)))
    assert "rx-interaction-classes" in str(exc.value)
    assert "dr.smith@example.com" not in str(exc.value)  # names the field, never echoes the PII


# =========================================================================== #
# ADR-0019-T1 — de-identified chat-sourced nutrition/supplement/peptide/training
# tokens. Each is kind-2 raw-backed-derived: a named-excluded raw source + a
# `_RAW_TO_FIELD` entry + a `_FIELD_DERIVATION` coarse band/class. THE CRITICAL AC
# (AC-2) is the per-token output-scan COARSENESS PROOF — an INDEPENDENT scan of the
# emitted token, NOT the 8j6 gate (which does NOT run on the raw-backed-derived
# path: router.summarize's derived branch runs no `scan_text`). De-identification
# is the DERIVATION's coarseness; the output scan is its proof.
# =========================================================================== #

# The four (raw source -> derived token -> consuming domain) the task mints. The
# raw sources are named-excluded; the derived tokens are SUMMARY_FIELD_SET members.
_CHAT_TOKENS = (
    # (raw source store item, derived field-set token, consuming domain)
    ("raw-nutrition-free-text", "dietary-pattern-class", "nutrition"),
    ("raw-supplement-free-text", "supplement-stack-class", "supplements"),
    ("raw-peptide-free-text", "peptide-use-class", "peptides"),
    ("raw-training-detail-free-text", "training-volume-band", "workout"),
)

# A crafted raw value per source carrying a distinctive identifiable substring. The
# output scan asserts NONE of these substrings survives into the emitted coarse token
# (non-reversibility). Realistic representative input (PF-S90-01): a real dietary
# free-text, a real supplement stack, a real peptide stack, a real training split.
_CRAFTED_RAW = {
    "raw-nutrition-free-text":
        "mostly chicken rice and broccoli, allergic to SHELLFISH-SENTINEL, 5 meals a day",
    "raw-supplement-free-text":
        "creatine 5g, whey PROTEINBRAND-SENTINEL, vitamin D 4000IU nightly",
    "raw-peptide-free-text":
        "BPC-157 250mcg SENTINEL-COMPOUND twice daily subcutaneous",
    "raw-training-detail-free-text":
        "PPL 6x/week, 22 SENTINEL-SETS per session, heavy barbell squats",
}


def _chat_records(raw_source, value):
    """One readings-series record for a chat raw source item carrying `value`."""
    return [{"item": raw_source, "timepoint": "2026-01-01T00:00:00+00:00",
             "source": "intake", "value": value}]


def test_chat_tokens_are_field_set_members():
    """AC-1/AC-3: each new derived token is a SUMMARY_FIELD_SET member."""
    for _raw, token, _domain in _CHAT_TOKENS:
        assert token in router.SUMMARY_FIELD_SET, token


def test_chat_raw_sources_are_named_excluded():
    """AC-3: each new raw source is a named-excluded raw-PII class (never a token)."""
    for raw, token, _domain in _CHAT_TOKENS:
        assert raw in router.EXCLUDED_RAW_PII, raw
        assert raw not in router.SUMMARY_FIELD_SET, raw
        # raw -> token mapping registered.
        assert router._RAW_TO_FIELD.get(raw) == token, raw


def test_chat_tokens_have_a_registered_derivation():
    """AC-1/AC-3: each new token has a `_FIELD_DERIVATION` coarse band/class function."""
    for _raw, token, _domain in _CHAT_TOKENS:
        assert token in router._FIELD_DERIVATION, token
        assert callable(router._FIELD_DERIVATION[token]), token


@pytest.mark.parametrize("raw_source, token, domain", _CHAT_TOKENS)
def test_chat_token_coarseness_output_scan(raw_source, token, domain):
    """AC-2 (THE CRITICAL coarseness proof): a crafted raw value at a chat source emits
    a coarse band/class carrying 0 of that raw value (non-reversibility).

    The 8j6 `summarize` PII gate does NOT run on this raw-backed-derived path
    (router.summarize's derived branch at the `_RAW_TO_FIELD` source lookup runs no
    `scan_text` — only the pass-through else-branch gates). So a new token's
    de-identification is NOT the 8j6 gate; it is the DERIVATION's COARSENESS, and THIS
    independent output scan — not the gate — is the de-identification proof. We seed a
    distinctive identifiable substring at the named-excluded source and assert it is
    ABSENT from the emitted token (the token is the coarse class only).
    """
    crafted = _CRAFTED_RAW[raw_source]
    summary = router.summarize(_store_read_factory(_chat_records(raw_source, crafted)))
    emitted = str(summary[token])
    # The emitted token is the coarse band/class — the raw sentinel never appears.
    for fragment in crafted.split():
        if fragment.isupper() and "SENTINEL" in fragment:
            assert fragment not in emitted, (
                f"raw value fragment {fragment!r} leaked into the {token!r} token: {emitted!r}"
            )
    # Belt: the whole crafted raw string never appears verbatim either.
    assert crafted not in emitted, f"raw value leaked verbatim into {token!r}: {emitted!r}"


def test_chat_token_coarseness_negative_control_is_failing_capable():
    """AC-2 negative control (LOAD-BEARING): a TOO-FINE derivation (passing the raw value
    through) makes the per-token output scan FAIL; the real coarse band passes.

    Proves the coarseness scan is failing-capable, not a constant-true assertion. We
    temporarily install a too-fine `dietary-pattern-class` deriver that returns the raw
    value verbatim, confirm the output scan now finds the sentinel (the scan WOULD red),
    then revert to the real coarse band and confirm the sentinel is gone (the scan
    passes). This is the proof the whole task's load-bearing gate is failing-capable.
    """
    raw_source, token = "raw-nutrition-free-text", "dietary-pattern-class"
    crafted = _CRAFTED_RAW[raw_source]
    real_deriver = router._FIELD_DERIVATION[token]
    try:
        # TOO-FINE: pass the raw value straight through (no de-identification).
        router._FIELD_DERIVATION[token] = lambda readings: str(readings[-1]["value"])
        leaky = router.summarize(_store_read_factory(_chat_records(raw_source, crafted)))
        # Under the too-fine deriver the sentinel DOES appear — the scan is failing-capable.
        assert "SHELLFISH-SENTINEL" in str(leaky[token]), (
            "the too-fine deriver should leak the raw value — the negative control is broken"
        )
    finally:
        router._FIELD_DERIVATION[token] = real_deriver
    # Reverted to the coarse band: the sentinel is gone (the scan passes).
    clean = router.summarize(_store_read_factory(_chat_records(raw_source, crafted)))
    assert "SHELLFISH-SENTINEL" not in str(clean[token])


def _capturing_client(captured):
    """A model client whose `author(domain, summary)` records the summary it is handed."""
    class _Client:
        def author(self, domain, summary):
            captured[domain] = dict(summary)
            return {"specialist": "test", "recommendations": []}
    return _Client()


@pytest.mark.parametrize("raw_source, token, domain", _CHAT_TOKENS)
def test_chat_token_reaches_its_domain_author(raw_source, token, domain, tmp_path):
    """AC-1 (round-trip to the translator; Risk PF-S87-01): a chat raw input -> its
    named-excluded source item -> `summarize` derives the band -> the token is in the
    summary the domain's author (the translator's consumer) reasons over.

    `compute_plan(domain, ...)` builds the summary via `router.summarize` and hands it to
    the domain author (`client.author(domain, summary)`). The token reaching that summary
    for the consuming domain is the round-trip-to-translator (the translators consume the
    author's recommendations reasoned over this summary). A capturing client records the
    summary so we assert the token is present AND carries the derived coarse band.
    """
    from functools import partial

    from scripts.plan import generate_plan
    from scripts.store import store

    store.append(
        raw_source,
        {"item": raw_source, "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": _CRAFTED_RAW[raw_source]},
        root=tmp_path,
    )
    captured = {}
    generate_plan.compute_plan(
        domain,
        store_read=partial(store.read, root=tmp_path),
        client=_capturing_client(captured),
    )
    assert domain in captured, f"the {domain!r} author was never handed a summary"
    assert token in captured[domain], (
        f"the {token!r} token never reached the {domain!r} author's summary"
    )
    # The token carries the DERIVED coarse band, not the raw value.
    assert "SENTINEL" not in str(captured[domain][token])


def test_chat_tokens_tripwires_green_on_clean_import():
    """AC-3: the change-control tripwires hold with the extended set (clean import).

    A fresh `import scripts.plan.router` runs the module-load asserts:
    `set(_RAW_TO_FIELD) <= EXCLUDED_RAW_PII` + `SUMMARY_FIELD_SET.isdisjoint(EXCLUDED_RAW_PII)`.
    A clean reload not raising proves every new token is placed in the correct structure.
    """
    import importlib
    importlib.reload(router)  # re-runs the load-time tripwires; raises if any is red
    # And explicitly: the new tokens are disjoint from the excluded set, the raw sources
    # are subsumed by it.
    assert set(router._RAW_TO_FIELD) <= set(router.EXCLUDED_RAW_PII)
    assert set(router.SUMMARY_FIELD_SET).isdisjoint(set(router.EXCLUDED_RAW_PII))


def test_training_volume_band_distinct_from_training_age_band():
    """AC-4: the chat-sourced `training-volume-band` is DISTINCT from the demographic
    `training-age-band` — distinct field-set members, distinct sources, distinct derivers.
    """
    assert "training-volume-band" in router.SUMMARY_FIELD_SET
    assert "training-age-band" in router.SUMMARY_FIELD_SET
    assert "training-volume-band" != "training-age-band"
    # Distinct sources: training-volume-band from the chat free-text, training-age-band
    # from the demographic date-of-birth.
    assert router._RAW_TO_FIELD.get("raw-training-detail-free-text") == "training-volume-band"
    assert router._RAW_TO_FIELD.get("date-of-birth") == "training-age-band"
    # Distinct derivers.
    assert (router._FIELD_DERIVATION["training-volume-band"]
            is not router._FIELD_DERIVATION["training-age-band"])


# =========================================================================== #
# Wave-B /review-pr fixes — the 4 chat-deriver correctness bugs + the BUG-1
# absent-source HONESTY sentinel. Each test asserts the POST-FIX behavior and is
# failing-capable against the pre-fix code (the old no-signal-default-on-absent,
# the single-digit frequency regex, the len<=1 separators-only false positive, the
# plant-pattern-masks-allergy ordering, the garbled malformed-year band).
# =========================================================================== #


# (deriver, the no-signal default for a PRESENT-but-unspecific value). Only the dietary +
# training derivers have an unspecific-present no-signal default; the supplement/peptide
# derivers are binary presence (any present non-none text reads as presence), so a present
# unspecific value reads as presence, not the no-signal default — covered separately.
_UNSPECIFIC_PRESENT_DERIVERS = (
    (router._dietary_pattern_class, "general-diet"),
    (router._training_volume_band, "moderate"),
)


@pytest.mark.parametrize("raw_source, token, _domain", _CHAT_TOKENS)
def test_chat_deriver_absent_source_emits_distinct_sentinel(raw_source, token, _domain):
    """BUG-1 + TEST-1/TEST-4: an ABSENT source (empty store_read) emits the DISTINCT
    `not-discussed` sentinel, NOT the no-signal default.

    A fresh operator with no chat data must NOT emit a token token-indistinguishable from
    a CONFIRMED answer (`none`/`general-diet`/`moderate`). The sentinel makes the data
    honest: "not elicited" (`not-discussed`) is distinguishable from "confirmed none".
    The sentinel is still a value, so the always-set contract holds (no partial-summary
    raise). Failing-capable: the pre-fix absent branch returned the no-signal default,
    which != `not-discussed`.
    """
    summary = router.summarize(_store_read_factory([]))  # nothing stored for any source
    assert summary[token] == "not-discussed", (
        f"{token!r} on an absent source emitted {summary[token]!r}, not the sentinel"
    )
    # The token is still PRESENT (always-set contract): the new tokens never drop out of
    # the summary even when no chat source exists (so they do not contribute to a
    # partial-summary raise — they are in `_ALWAYS_SET_DERIVED`).
    assert token in summary
    assert token in router._ALWAYS_SET_DERIVED


def test_chat_absent_source_distinct_from_confirmed_none_for_presence_tokens():
    """BUG-1: for the supplement/peptide presence tokens, ABSENT (-> sentinel) is
    token-distinguishable from a CONFIRMED-none ('none' typed) -> `none`.

    The whole point of the sentinel: `<deriver>([]) != <deriver>([{value:'none'}])`. A
    fresh operator (absent) reads `not-discussed`; an operator who typed "none" reads the
    confirmed `none`. Failing-capable: the pre-fix absent branch returned `none`, making
    the two indistinguishable.
    """
    confirmed_none = [{"item": "x", "timepoint": "2026-01-01T00:00:00+00:00",
                       "source": "intake", "value": "none"}]
    for deriver in (router._supplement_stack_class, router._peptide_use_class):
        assert deriver([]) == "not-discussed"
        assert deriver(confirmed_none) == "none"
        assert deriver([]) != deriver(confirmed_none), (
            f"{deriver.__name__}: absent must be distinguishable from confirmed-none"
        )


@pytest.mark.parametrize("deriver, confirmed_default", _UNSPECIFIC_PRESENT_DERIVERS)
def test_chat_deriver_no_signal_default_reserved_for_present_source(deriver, confirmed_default):
    """BUG-1: the no-signal default (`general-diet`/`moderate`) is RESERVED for a PRESENT
    source that resolves to no specific signal — never emitted on an absent source.

    Absent -> the sentinel; a present value that matches no specific bucket -> the
    no-signal default. Pins the two-state distinction so a future edit cannot collapse
    absent back onto the default.
    """
    assert deriver([]) == "not-discussed"
    # A present-but-unspecific value resolves to the confirmed no-signal default.
    unspecific = [{"item": "x", "timepoint": "2026-01-01T00:00:00+00:00",
                   "source": "intake", "value": "nothing in particular xyz"}]
    assert deriver(unspecific) == confirmed_default


def test_chat_tokens_sentinel_keeps_summary_complete_and_dispatchable():
    """BUG-1 always-set: with a COMPLETE clean store but NO chat sources, the 4 chat
    tokens are the `not-discussed` sentinel AND the full summary still dispatches.

    Proves the sentinel keeps the always-set contract: a no-chat-data operator gets the
    sentinel for each chat token, the summary is complete (every field-set field present),
    and `dispatch` does NOT trip the partial-summary raise.
    """
    summary = router.summarize(_clean_store_read())  # clean pass-through state, no chat sources
    for _raw, token, _domain in _CHAT_TOKENS:
        assert summary[token] == "not-discussed", token
    assert set(summary.keys()) == set(router.SUMMARY_FIELD_SET)  # complete, no field omitted
    result = router.dispatch(summary)  # must NOT raise partial-summary
    assert result.lane == router.NO_TRAIN_LANE
    for _raw, token, _domain in _CHAT_TOKENS:
        assert result.payload[token] == "not-discussed"


# --- TEST-2: per-deriver bucket-branch unit tests (mirror _age_band/_issue_class) ----


@pytest.mark.parametrize("value, expected", [
    # BUG-5 precedence: allergy/restriction is checked FIRST (never masked by a plant pattern).
    ("vegetarian but allergic to nuts", "restricted"),
    ("pescatarian gluten-free", "restricted"),
    ("eat everything but allergic to shellfish", "restricted"),
    ("keto bulk", "restricted"),
    ("carnivore", "restricted"),
    ("vegan", "plant-based"),
    ("wholly plant based diet", "plant-based"),
    ("vegetarian, no meat", "plant-forward"),
    ("plant-forward mostly", "plant-forward"),
    ("eat everything, omnivore", "omnivore"),
    ("chicken rice and beef", "omnivore"),
    ("nothing in particular", "general-diet"),  # present, no bucket -> no-signal default
])
def test_dietary_pattern_class_token_value(value, expected):
    """BUG-5 + TEST-2: _dietary_pattern_class maps free-text to the correct coarse class,
    with the allergy/restriction signal taking precedence over plant patterns."""
    assert router._dietary_pattern_class(_reading(value)) == expected


@pytest.mark.parametrize("value, expected", [
    ("none", "none"),
    ("no", "none"),
    ("n/a", "none"),
    (";;;", "none"),                         # BUG-4: separators-only -> none (not single)
    (",,", "none"),                          # BUG-4
    ("creatine 5g", "single-supplement"),
    ("creatine; whey; vitamin d", "multi-supplement"),
    ("creatine, omega-3, magnesium", "multi-supplement"),
])
def test_supplement_stack_class_token_value(value, expected):
    """BUG-4 + TEST-2: _supplement_stack_class maps free-text to the correct presence/
    breadth class; a separators-only value resolves to `none`, never a false single."""
    assert router._supplement_stack_class(_reading(value)) == expected


@pytest.mark.parametrize("value, expected", [
    ("none", "none"),
    ("no", "none"),
    (";;;", "none"),                         # BUG-4: separators-only -> none (not in-use)
    (",,", "none"),                          # BUG-4
    ("bpc-157 250mcg", "peptide-in-use"),
    ("tb-500; ipamorelin", "peptide-in-use"),
])
def test_peptide_use_class_token_value(value, expected):
    """BUG-4 + TEST-2: _peptide_use_class maps free-text to the correct binary presence
    class; a separators-only value resolves to `none`, never a false peptide-in-use."""
    assert router._peptide_use_class(_reading(value)) == expected


@pytest.mark.parametrize("value, expected", [
    ("twice a week", "low"),
    ("2x", "low"),
    ("minimal", "low"),
    ("3x/week", "moderate"),
    ("4 sessions per week", "moderate"),
    ("5 days", "high"),
    ("6x/week", "high"),
    ("daily", "high"),
    # BUG-3: double-digit counts must NOT collapse to the moderate no-signal default.
    ("10x", "high"),
    ("12 sessions", "high"),
    ("4-5x", "high"),                        # range -> the unit-adjacent digit (5) -> high
    ("15 sets", "moderate"),                 # "sets" is not a frequency unit — not misread
    ("5 days and 2x", "low"),                # contextual/last frequency (2x) wins over max()
    ("nothing specific", "moderate"),        # present, no count -> no-signal middle
])
def test_training_volume_band_token_value(value, expected):
    """BUG-3 + TEST-2: _training_volume_band maps free-text to the correct weekly-volume
    band; double-digit counts band correctly and a stray set count is not misread as
    frequency."""
    assert router._training_volume_band(_reading(value)) == expected


# The module-load tripwires (router.py:312-313) verbatim. The mis-placement tests below
# re-run these EXACT assertions against a deliberately mis-placed structure, proving the
# tripwire is the thing that reds — `importlib.reload` rebuilds router's module literals
# from source, so an in-place dict mutation cannot survive a reload to trip it (unlike the
# smei test, which mutates the SEPARATE biomarker_meta module the load assert reads). A
# subprocess that mutates BEFORE the load assert runs is the faithful "module-load" proof.

_MISPLACEMENT_SUBPROCESS = """
import sys
# Inject the mis-placement into router's source-of-truth constants AFTER the import-time
# asserts already ran clean, then re-execute the EXACT load-time tripwire to prove a
# mis-placed token reds it. {mutation}
from scripts.plan import router
{mutation}
assert set(router._RAW_TO_FIELD) <= set(router.EXCLUDED_RAW_PII)
assert set(router.SUMMARY_FIELD_SET).isdisjoint(set(router.EXCLUDED_RAW_PII))
print("tripwire-did-not-red")
"""


def _run_misplacement_subprocess(mutation):
    """Run the load-time tripwire against a mis-placed structure in a fresh interpreter.

    Returns the subprocess result; a faithful tripwire reds with a non-zero exit and an
    AssertionError in stderr (never prints `tripwire-did-not-red`).
    """
    import subprocess
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    return subprocess.run(
        [sys.executable, "-c", _MISPLACEMENT_SUBPROCESS.format(mutation=mutation)],
        cwd=repo_root, capture_output=True, text=True,
    )


def test_chat_token_misplacement_raw_source_not_excluded_reds_at_load():
    """AC-5 (Risk Negative-2): a raw source mapped in `_RAW_TO_FIELD` but NOT in
    `EXCLUDED_RAW_PII` reds the load-time tripwire (AssertionError).

    Fail-capable: add a raw source the excluded list does not name, then re-run the EXACT
    `set(_RAW_TO_FIELD) <= EXCLUDED_RAW_PII` tripwire — it raises AssertionError. A token
    whose raw source escapes the excluded list reads through `summarize`'s else-branch
    under its raw name — the leak this tripwire catches.
    """
    result = _run_misplacement_subprocess(
        'router._RAW_TO_FIELD["unlisted-raw-source"] = "dietary-pattern-class"'
    )
    assert result.returncode != 0, (
        f"the mis-placement tripwire did not red; stdout={result.stdout!r}"
    )
    assert "AssertionError" in result.stderr
    assert "tripwire-did-not-red" not in result.stdout


def test_chat_token_misplacement_token_in_excluded_reds_at_load():
    """AC-5 (Risk Negative-2): a token placed in BOTH the field-set and the excluded list
    reds the disjointness tripwire at module load.

    Fail-capable: also name a derived token in `EXCLUDED_RAW_PII` (so the field-set and
    excluded list overlap), then re-run the EXACT
    `SUMMARY_FIELD_SET.isdisjoint(EXCLUDED_RAW_PII)` tripwire — it raises AssertionError.
    """
    result = _run_misplacement_subprocess(
        'router.EXCLUDED_RAW_PII = router.EXCLUDED_RAW_PII + ("dietary-pattern-class",)'
    )
    assert result.returncode != 0, (
        f"the mis-placement tripwire did not red; stdout={result.stdout!r}"
    )
    assert "AssertionError" in result.stderr
    assert "tripwire-did-not-red" not in result.stdout


# =========================================================================== #
# ADR-0032-T3 — the additive de-identified `genetic-trait-classes` token + the
# local deriver. The planner consumes ONLY the coarse trait-class token; the raw
# rsID+allele genotype NEVER crosses to the no-train lane (the crown jewel, NFR-1).
# The deriver mirrors `_rx_interaction_classes_token` and calls T2's matcher
# (`scripts.genetics.match.match_genotypes`). Mock/fixture-tested, 0 live spend.
# =========================================================================== #


def _write_genetics_page(library_root, gene, rsid, findings, slug=None):
    """Write a fixture genetics page in the pinned T1<->T2 format (mirrors test_match)."""
    slug = slug or f"{gene.replace('/', '-').lower()}-{rsid}"
    lines = [
        "---",
        f"title: {gene} {rsid}",
        "type: genetics",
        f"gene: {gene}",
        f"rsid: {rsid}",
        "evidence_tier: B",
        "last_verified: 2026-06-29",
        "provenance_dir: design/genetics-fixture",
        "provenance_slug: genetics-fixture",
        "---",
        "",
        f"# {gene} {rsid}",
        "",
        "## Genotype Findings",
    ]
    for genotype, trait_class, prose in findings:
        lines.append(f"- {genotype}: {trait_class} — {prose} [1]")
    page = Path(library_root) / f"{slug}.md"
    page.write_text("\n".join(lines) + "\n")
    return page


def _dna_store_read(gene, rsid, genotype):
    """A store.read seeded with ONE operator `dna-report` genotype reading for a variant."""
    return _store_read_factory([
        {"item": f"{gene} {rsid}", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "dna-report", "value": genotype},
    ])


def test_genetic_trait_classes_in_field_set():
    """AC-1: `genetic-trait-classes` is a SUMMARY_FIELD_SET member + the tripwire holds.

    The module-load `isdisjoint(EXCLUDED_RAW_PII)` tripwire ran at import (else this
    module failed to collect); re-affirm the additive member did not break it. RED-first
    today: the member is absent.
    """
    assert "genetic-trait-classes" in router.SUMMARY_FIELD_SET
    assert set(router.SUMMARY_FIELD_SET).isdisjoint(set(router.EXCLUDED_RAW_PII))


def test_genetic_trait_classes_token_non_tautological(tmp_path):
    """AC-2: the token IS the matched finding (A != B), not a plumbed constant. 0 spend.

    A fixture page maps the operator's LOCAL allele to a coarse trait class; genotype A
    and genotype B map to DIFFERENT classes, so a constant-return deriver reds (out_a ==
    out_b). Cross-checks T2's per-genotype lookup.
    """
    _write_genetics_page(tmp_path, "CYP1A2", "rs762551", [
        ("(A;A)", "fast-caffeine-metabolism", "fast metabolizer"),
        ("(C;C)", "slow-caffeine-metabolism", "slow metabolizer"),
    ])
    out_a = router.summarize(
        _dna_store_read("CYP1A2", "rs762551", "(A;A)"),
        genetics_library_root=tmp_path,
    )["genetic-trait-classes"]
    out_b = router.summarize(
        _dna_store_read("CYP1A2", "rs762551", "(C;C)"),
        genetics_library_root=tmp_path,
    )["genetic-trait-classes"]
    assert out_a == "fast-caffeine-metabolism"
    assert out_b == "slow-caffeine-metabolism"
    assert out_b != out_a


def test_genetic_trait_classes_token_joined_sorted_deduped(tmp_path):
    """AC-2 contract: multiple matches -> a `;`-joined, SORTED, deduped coarse scalar."""
    _write_genetics_page(tmp_path, "CYP1A2", "rs762551", [("(A;A)", "zeta-class", "z")])
    _write_genetics_page(tmp_path, "ACTN3", "rs1815739", [("(C;C)", "alpha-class", "a")])
    store_read = _store_read_factory([
        {"item": "CYP1A2 rs762551", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "dna-report", "value": "(A;A)"},
        {"item": "ACTN3 rs1815739", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "dna-report", "value": "(C;C)"},
    ])
    token = router.summarize(store_read, genetics_library_root=tmp_path)["genetic-trait-classes"]
    assert token == "alpha-class;zeta-class"  # sorted + ;-joined


def test_genetic_trait_classes_carries_no_raw_genotype_fail_closed(tmp_path):
    """AC-3 CROWN JEWEL: the token carries 0 raw genotypes; a raw-genotype-bearing
    trait-class token makes `summarize` RAISE (fail-closed) rather than leak it.

    FAILING-CAPABLE: a deriver that passes the raw genotype through reds both halves —
    the absence assertion (a) AND the fail-closed raise (b).
    """
    import re

    # (a) a normal match's token carries no rsID and no allele-call pattern.
    _write_genetics_page(tmp_path, "CYP1A2", "rs762551", [
        ("(A;A)", "fast-caffeine-metabolism", "fast"),
    ])
    token = router.summarize(
        _dna_store_read("CYP1A2", "rs762551", "(A;A)"),
        genetics_library_root=tmp_path,
    )["genetic-trait-classes"]
    assert not re.search(r"rs\d+", token)
    assert not re.search(r"\([ACGTDI]+;[ACGTDI]+\)", token)

    # (b) a page whose finding embeds a raw genotype IN the trait-class token ->
    #     summarize RAISES (fail-closed), naming the field, never echoing the genotype.
    leak_root = tmp_path / "leak"
    leak_root.mkdir()
    _write_genetics_page(leak_root, "CYP1A2", "rs762551", [
        ("(A;A)", "carrier-of-rs762551", "a leaky trait-class carrying an rsID"),
    ])
    with pytest.raises(ValueError) as exc:
        router.summarize(
            _dna_store_read("CYP1A2", "rs762551", "(A;A)"),
            genetics_library_root=leak_root,
        )
    assert "genetic-trait-classes" in str(exc.value)
    assert "fail-closed" in str(exc.value)
    assert "rs762551" not in str(exc.value)  # names the field, never echoes the genotype


def test_genetic_trait_classes_carries_no_raw_allele_call_fail_closed(tmp_path):
    """AC-3 CROWN JEWEL (allele-call half): a trait-class token carrying an `(X;Y)`
    allele-call makes `summarize` RAISE, never echoing the genotype."""
    _write_genetics_page(tmp_path, "CYP1A2", "rs762551", [
        ("(A;A)", "metabolizer-(A;A)", "a leaky trait-class carrying an allele call"),
    ])
    with pytest.raises(ValueError) as exc:
        router.summarize(
            _dna_store_read("CYP1A2", "rs762551", "(A;A)"),
            genetics_library_root=tmp_path,
        )
    assert "genetic-trait-classes" in str(exc.value)
    assert "fail-closed" in str(exc.value)
    assert "(A;A)" not in str(exc.value)


def test_genetic_trait_classes_pii_scan_branch_fail_closed(tmp_path):
    """QA-1 CROWN JEWEL (pii_scan half): a trait-class token embedding a structural
    value-class token (an email) makes `summarize` RAISE via the deriver's `pii_scan`
    backstop — the third fail-closed trigger, distinct from `rs\\d+` and `(allele;allele)`.

    The two sibling tests cover the `rs\\d+` and `(allele;allele)` triggers; NONE exercises
    the `pii_scan.scan_text(tok, ...)` condition, so a surgical removal of JUST that
    condition would pass them all. An email (`operator@example.com`) trips ONLY `pii_scan`
    (it matches neither raw-genotype pattern), so removing the `pii_scan` condition reds
    THIS test — pinning the crown-jewel's third branch. Uses the REAL store (store.append
    to a tmp root + the real `store.read`), consistent with the AC-10 production path.
    """
    from functools import partial

    from scripts.store import store

    # REAL store: append the operator's CYP1A2 genotype to a tmp store root.
    store_root = tmp_path / "store"
    store.append(
        "CYP1A2 rs762551",
        {"item": "CYP1A2 rs762551", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "dna-report", "value": "(A;A)"},
        root=store_root,
    )
    store_read = partial(store.read, root=store_root)

    # A fixture page whose trait-class TOKEN field embeds a structural value-class token
    # (an email) — trips the deriver's pii_scan backstop, not the genotype patterns.
    lib = tmp_path / "genetics"
    lib.mkdir()
    _write_genetics_page(lib, "CYP1A2", "rs762551", [
        ("(A;A)", "metabolizer-operator@example.com", "a leaky trait-class carrying contact PII"),
    ])
    with pytest.raises(ValueError) as exc:
        router.summarize(store_read, genetics_library_root=lib)
    assert "genetic-trait-classes" in str(exc.value)        # names the field
    assert "fail-closed" in str(exc.value)
    assert "operator@example.com" not in str(exc.value)     # never echoes the value


def test_genetic_trait_classes_always_set_empty_on_no_dna(tmp_path):
    """AC-4 ALWAYS-SET: a no-DNA `store_read` -> "" AND dispatch does NOT partial-raise."""
    summary = router.summarize(_clean_store_read(), genetics_library_root=tmp_path)
    assert summary["genetic-trait-classes"] == ""
    assert set(summary.keys()) == set(router.SUMMARY_FIELD_SET)  # field present, complete
    router.dispatch(summary)  # must not raise a partial-summary error


def test_dispatch_whitelists_genetic_trait_classes_rejects_raw_genotype(tmp_path):
    """AC-5: dispatch ADMITS `genetic-trait-classes` (now a field-set member); a
    raw-genotype field name is REJECTED by the same `set(payload) <= field-set` whitelist."""
    summary = router.summarize(_clean_store_read(), genetics_library_root=tmp_path)
    assert "genetic-trait-classes" in summary
    router.dispatch(summary)  # the new field rides through the whitelist — no raise
    summary["MTNR1B rs10830963"] = "(C;G)"  # a raw-genotype field name, out-of-set
    with pytest.raises(ValueError) as exc:
        router.dispatch(summary)
    assert "MTNR1B rs10830963" in str(exc.value)


def test_summarize_no_arg_production_path_is_dna_aware(tmp_path, monkeypatch):
    """AC-10 FIX-1/CQ-1: `None` resolves to the real default; the frozen no-arg
    production `summarize(store_read)` call is DNA-aware WITHOUT a caller edit.

    Exercises the REAL store (not a fake `store_read`): the genotype is `store.append`-ed
    to a tmp root, and `summarize` is handed the SAME bound `store.read` shape the frozen
    production callers use — `functools.partial(store.read, root=...)` (generate_plan.py:356
    / orchestrate.py:537). With the real store, the production no-arg path runs T2's matcher
    over the WHOLE curated set, reading each derived item key through `store._item_path`'s
    direct-child safety check — so a `/`-bearing curated gene (BUG-1) would crash this path
    mid-iteration. The prior fake-`store_read` build MASKED that path-escape (PF-S99-01 /
    PF-S101-01: the AC-10 integration criterion must exercise the real store path it claims
    to verify, not a stand-in that never reaches `_item_path`).

    Monkeypatches the module-level default library root to a fixture library, calls the
    no-arg signature, and asserts a NON-EMPTY token tracing to the fixture page. The
    negative control (matching page absent from that same default-resolved library -> "")
    DISTINGUISHES "wired to the real default, no match" from "feature disabled": an inert
    `None`->`""`-always build reds the non-empty assertion (the always-set AC-4 passes
    identically either way and cannot catch it).
    """
    from functools import partial

    from scripts.store import store

    # REAL store: append the operator's CYP1A2 genotype to a tmp store root.
    store_root = tmp_path / "store"
    store.append(
        "CYP1A2 rs762551",
        {"item": "CYP1A2 rs762551", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "dna-report", "value": "(A;A)"},
        root=store_root,
    )
    store_read = partial(store.read, root=store_root)  # the frozen production call shape

    lib = tmp_path / "genetics"
    lib.mkdir()
    _write_genetics_page(lib, "CYP1A2", "rs762551", [
        ("(A;A)", "fast-caffeine-metabolism", "fast"),
    ])
    monkeypatch.setattr(router, "GENETICS_LIBRARY_DEFAULT_ROOT", lib)
    # NO genetics_library_root passed — the frozen production signature, over the REAL store.
    token = router.summarize(store_read)["genetic-trait-classes"]
    assert token == "fast-caffeine-metabolism"  # non-empty, traces to the fixture page

    # Negative control: same REAL store + default-resolved library, matching page ABSENT -> "".
    empty_lib = tmp_path / "genetics-empty"
    empty_lib.mkdir()
    monkeypatch.setattr(router, "GENETICS_LIBRARY_DEFAULT_ROOT", empty_lib)
    assert router.summarize(store_read)["genetic-trait-classes"] == ""


# =========================================================================== #
# ADR-0033-0035-T2 — OQ-5 actual-age + actual-weight de-association (REPURPOSE).
# `training-age-band` now carries the EXACT AGE (from the local full date-of-birth);
# `bodyweight-band` now carries the CURRENT WEIGHT + TREND (from the local bodyweight-kg
# series). The full DOB + the raw per-day weight history NEVER cross to the no-train
# planner (the crown jewel, NFR-1). Mock/fixture-tested, 0 live spend.
# =========================================================================== #


def _weight_series(values):
    """A `bodyweight-kg` dated series store_read over the given per-day values (chronological)."""
    return _store_read_factory([
        {"item": "bodyweight-kg", "timepoint": f"2026-{i + 1:02d}-01T00:00:00+00:00",
         "source": "intake", "value": v}
        for i, v in enumerate(values)
    ])


def test_summary_field_set_byte_identical_after_repurpose():
    """AC-1: the repurpose changes DERIVATION, not the field set — the tuple is byte-identical.

    A clean reimport re-runs the module-load tripwires (they must hold with the additive
    `bodyweight-kg` member); the tuple equals the pinned pre-edit membership, proving no
    token was added or removed.
    """
    import importlib
    importlib.reload(router)  # re-runs the load-time tripwires; raises if any red
    assert router.SUMMARY_FIELD_SET == _PINNED_FIELD_SET


def test_training_age_band_is_exact_age_non_tautological():
    """AC-2: training-age-band is the EXACT integer age; a different birth-year DOB yields a
    different age (a constant-return deriver reds age_a == age_b)."""
    dob_a, dob_b = "1986-04-12", "1972-08-09"
    age_a = router.summarize(_store_read_factory([
        {"item": "date-of-birth", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": dob_a},
    ]))["training-age-band"]
    age_b = router.summarize(_store_read_factory([
        {"item": "date-of-birth", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": dob_b},
    ]))["training-age-band"]
    assert age_a == _expected_age(dob_a)
    assert age_b == _expected_age(dob_b)
    assert age_a != age_b  # non-tautological: different DOB year -> different age


def test_training_age_band_carries_no_full_dob_crown_jewel(monkeypatch):
    """AC-3 CROWN JEWEL (SEC-F2 + QA-F3): the full DOB never reaches the summary.

    PRIMARY (format-agnostic): the token is the integer age; the seeded full-DOB string is
    absent from the serialized summary in any format; `pii_scan.scan_text` over the summary
    returns 0. NEGATIVE CONTROL (QA-F3, prove-it-can-RED at THIS wave): stub the training-age
    deriver to echo the raw DOB and confirm the seeded-substring scan goes RED — the probe is
    non-vacuous.
    """
    import re

    from scripts.guard import pii_scan

    dob = "1986-03-12"
    store_read = _store_read_factory([
        {"item": "date-of-birth", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": dob},
    ])
    summary = router.summarize(store_read)
    assert summary["training-age-band"] == _expected_age(dob)
    # PRIMARY, format-agnostic: no rendering of the seeded full DOB survives.
    for fragment in (dob, "1986/03/12", "03/12/1986", "March 12 1986"):
        assert fragment not in str(summary), fragment
    # SUPPLEMENTARY (does NOT stand alone): the enumerated MM/DD / month-day regex is absent.
    assert not re.search(r"\b\d{4}[-/]\d{2}[-/]\d{2}\b", str(summary))
    # pii_scan over the serialized summary returns 0 identity/value hits (SEC-F2).
    assert pii_scan.scan_text(str(summary)) == 0
    # NEGATIVE CONTROL: stub the deriver to leak the raw DOB -> the substring scan RED.
    monkeypatch.setitem(router._FIELD_DERIVATION, "training-age-band",
                        lambda readings: str(readings[-1]["value"]))
    leaked = router.summarize(store_read)
    assert dob in str(leaked)  # the leak IS present under the stub — the probe can RED


def test_bodyweight_band_is_current_weight_plus_trend_non_tautological():
    """AC-4: bodyweight-band carries the CURRENT weight + a coarse trend; a down-trending
    series yields a distinct trend from a flat one (a constant return reds down != flat)."""
    down = router.summarize(_weight_series(["85.0", "84.0", "83.0", "82.0"]))["bodyweight-band"]
    flat = router.summarize(_weight_series(["80.0", "80.0"]))["bodyweight-band"]
    assert down != flat  # non-tautological
    assert "down" in down and "flat" in flat
    assert "82" in down  # the current weight traces to the LATEST reading


def test_bodyweight_series_stays_local_crown_jewel(monkeypatch):
    """AC-5 CROWN JEWEL (QA-F3): only the current weight crosses; the per-day history stays
    local, and `dispatch` rejects a raw bodyweight-kg payload field.

    NEGATIVE CONTROL: stub the deriver to echo the raw series and confirm the seeded-substring
    scan goes RED — the probe is non-vacuous at THIS wave.
    """
    series = ["85.0", "84.0", "83.0", "82.0"]
    store_read = _weight_series(series)
    summary = router.summarize(store_read)
    # Only the current (82) crosses; the non-current per-day history is absent.
    for historical in ("85.0", "84.0", "83.0"):
        assert historical not in str(summary), historical
    # dispatch rejects a raw bodyweight-kg payload field (the out-of-field-set whitelist).
    complete = router.summarize(_clean_store_read())
    complete["bodyweight-kg"] = "82.0"
    with pytest.raises(ValueError) as exc:
        router.dispatch(complete)
    assert "bodyweight-kg" in str(exc.value)
    # NEGATIVE CONTROL: stub the deriver to leak the raw series -> the substring scan RED.
    monkeypatch.setitem(router._FIELD_DERIVATION, "bodyweight-band",
                        lambda readings: str([r["value"] for r in readings]))
    leaked = router.summarize(store_read)
    assert "85.0" in str(leaked)  # the leak IS present under the stub — the probe can RED


def test_age_and_weight_conditional_omitted_when_absent():
    """AC-6: training-age-band + bodyweight-band stay CONDITIONAL (omitted when their source
    is absent, not in `_ALWAYS_SET_DERIVED`); a complete summary still dispatches.

    RED-first (weight half): a directly-stored `bodyweight-band` item is now IGNORED (the
    source is `bodyweight-kg`); with no `bodyweight-kg` reading the token is OMITTED — today's
    pass-through would include it.
    """
    assert "training-age-band" not in router._ALWAYS_SET_DERIVED
    assert "bodyweight-band" not in router._ALWAYS_SET_DERIVED
    # No date-of-birth, no bodyweight-kg, but a STALE directly-stored bodyweight-band item.
    store_read = _store_read_factory([
        {"item": "bodyweight-band", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "80-90kg"},
        {"item": "sex-for-dosing", "timepoint": "2026-01-01T00:00:00+00:00",
         "source": "intake", "value": "male"},
    ])
    summary = router.summarize(store_read)
    assert "training-age-band" not in summary
    assert "bodyweight-band" not in summary  # RED today: pass-through would include the stale item
    # A complete clean summary (both sources present) dispatches without a partial raise.
    router.dispatch(router.summarize(_clean_store_read()))


def test_experience_band_bands_years_and_defaults_to_sentinel():
    """`_experience_band` bands stated years and emits the shared no-signal sentinel when absent.

    Bands the latest numeric years into the coarse experience class the planner reads; a fresh
    operator (no reading) or a non-numeric value emits `_NOT_DISCUSSED` — the same ALWAYS-SET
    sentinel the other always-set derivers use, so `training-experience-band`'s membership never
    trips dispatch's partial-summary raise.
    """
    band = lambda y: router._experience_band([{"value": str(y)}])
    assert band(0.5) == "novice"
    assert band(2) == "early-intermediate"
    assert band(4) == "intermediate"
    assert band(8) == "advanced"
    assert band(25) == "veteran"
    # no reading / non-numeric -> the shared always-set sentinel (never a fabricated band)
    assert router._experience_band([]) == router._NOT_DISCUSSED
    assert router._experience_band([{"value": "lots"}]) == router._NOT_DISCUSSED
    # it is a registered ALWAYS-SET derived field (present for a fresh operator)
    assert "training-experience-band" in router._ALWAYS_SET_DERIVED
    assert "training-experience-band" in router.SUMMARY_FIELD_SET
