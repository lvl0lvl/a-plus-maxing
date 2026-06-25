"""Tests for the model-backed de-id-IN boundary (ADR-0020-T1) — the crown-jewel egress gate.

`scripts.plan.deid_in.deid_in(raw_intake, client)` is the SOLE de-id-IN on the plan path:
raw operator plan-intake in, the de-identified summary the orchestrator consumes out, routed
through the INJECTED `ModelClient.deidentify` on its no-train backend, fail-closed to the
honest no-plan state on any model failure (never a leak, never a passthrough of raw). These
tests pin the five acceptance criteria:

  - AC-1: `deid_in` returns the de-identified summary via the injected client's `deidentify`,
    and uses ONLY the injected client — it constructs no second `ModelClient` (a
    `ModelClient.__init__` spy confirms 0 self-constructed clients) and the de-id call is the
    EXACT injected object (sentinel-client identity);
  - AC-2: a mock client whose `deidentify` raises `ModelCallError` → `deid_in` returns the
    honest no-plan sentinel (`DEID_CALL_FAILED`), never a fabricated/partial summary, never a
    raw passthrough; the error path scans 0 raw-PII;
  - AC-3: the persisted-side `router.summarize` path is unchanged — a `summarize`-derived
    summary scans 0 raw-PII (the byte-unchanged assertion is the recipe's `git diff` gate);
  - AC-5: the boundary writes nothing to a tracked path (a filesystem-write spy records 0
    writes during the call);
  - Risk R3 (crown-jewel leak probe): a seeded SYNTHETIC raw-PII token (a synthetic legal
    name + a synthetic lab value, never real operator PII) → `pii_scan.scan_text` over the
    EMITTED summary returns 0; a `deid_in` that echoed `raw_intake` turns this RED.

Every client is a mock/`_FixedEnvelopeClient`-style fixture; no test hits a live API or reads
a real key, and the test tree carries 0 real operator PII (synthetic tokens only).
"""

import json

import pytest

from scripts.guard import pii_scan
from scripts.model.client import ModelCallError, ModelClient
from scripts.plan import router
from scripts.plan.deid_in import DEID_CALL_FAILED, DEID_VALUE_PII, deid_in


# --- synthetic fixtures (0 real operator PII) ----------------------------------

# A synthetic legal name + a synthetic lab value seeded into the raw intake. NEITHER is real
# operator PII — the test tree carries synthetic tokens only. The leak probe's identity-token
# config (written to tmp) matches these so `scan_text` would catch a passthrough.
SYNTHETIC_NAME = "Jordan Faketestperson"
SYNTHETIC_LAB = "ALT 412 U/L"


def _raw_intake():
    """A raw operator plan-intake carrying synthetic raw-PII (name + lab value)."""
    return {
        "legal-name": SYNTHETIC_NAME,
        "raw-lab-values": SYNTHETIC_LAB,
        "goal-text": "I want to get stronger and recover from a recent injury.",
    }


def _deid_summary_fixture():
    """The de-identified summary the mock `deidentify` emits — band/class tokens only.

    Shaped from `router.SUMMARY_FIELD_SET`: carries NONE of the synthetic raw-PII tokens
    (no legal name, no raw lab value) — exactly what a real de-id call would emit.
    """
    return {
        "training-age-band": "10-15y",
        "sex-for-dosing": "male",
        "bodyweight-band": "80-90kg",
        "goal-domains": ["workout"],
        "active-issue-class": "musculoskeletal-recovery",
        "recovery-status-band": "moderate",
    }


class _FixedDeidClient:
    """A client adapter that returns a fixed, pre-captured de-identified summary.

    Mirrors `generate_plan._FixedEnvelopeClient` (the captured-envelope adapter) for the
    de-id seam: `deidentify(raw_intake)` returns the captured summary (or raises a captured
    Exception). It RECORDS the call so the test can assert the de-id call routed through THIS
    exact injected object (the no-second-client half of AC-1).

    Attributes:
        deid_output: The captured de-identified summary to return (or an Exception to raise).
    """

    def __init__(self, deid_output):
        self.deid_output = deid_output
        self.calls = []

    def deidentify(self, raw_intake):
        self.calls.append(raw_intake)
        if isinstance(self.deid_output, Exception):
            raise self.deid_output
        return self.deid_output


def _identity_config(tmp_path):
    """Write a gitignored-style identity-token config matching the synthetic PII tokens.

    One regex token per line (the `pii_scan._load_token_patterns` format). The probe scans
    the EMITTED summary against THIS config: a passthrough of `raw_intake` would carry the
    synthetic name/lab and register a hit; a clean de-identified summary registers 0.
    """
    config = tmp_path / "synthetic-identity.txt"
    config.write_text(SYNTHETIC_NAME + "\n" + SYNTHETIC_LAB + "\n")
    return config


# --- AC-1: boundary contract + no-train-backend / no-second-client -------------


def test_deid_in_returns_summary_via_injected_client():
    """AC-1: `deid_in` returns the de-identified summary the injected `deidentify` emits."""
    summary = _deid_summary_fixture()
    client = _FixedDeidClient(summary)

    result = deid_in(_raw_intake(), client)

    assert result == summary
    # the de-id call routed through the EXACT injected client object (its `deidentify` fired)
    assert client.calls == [_raw_intake()]


def test_deid_in_constructs_no_second_client(monkeypatch):
    """AC-1 (no-train guarantee, no-second-client half): `deid_in` builds 0 new clients.

    A `ModelClient.__init__` spy confirms `deid_in` instantiates no `ModelClient` of its own
    — it uses ONLY the injected client. A `deid_in` that constructed its own client (and thus
    a live no-train backend) turns this RED.
    """
    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)

    client = _FixedDeidClient(_deid_summary_fixture())
    deid_in(_raw_intake(), client)

    assert instantiations == [], "deid_in constructed a second ModelClient (must use only the injected one)"


def test_deid_in_routes_through_no_train_backend():
    """AC-1 (no-train guarantee, no-train-backend half): the de-id call runs on the no-train backend.

    A `ModelClient` over the default `_ClaudeNoTrainBackend` is the injected client; `deid_in`
    routing the de-id call through it (rather than a self-constructed training-eligible client)
    means the no-train backend is the call site. A fixture backend stands in for the live no-train
    method (whose live call is `NotImplementedError` until the operator checkpoint) so 0 live spend.
    """
    from tests.model.test_client import _FixtureBackend

    summary = _deid_summary_fixture()
    injected = ModelClient(backend=_FixtureBackend(deidentify_result=summary))

    result = deid_in(_raw_intake(), injected)

    assert result == summary
    # the injected client is a real ModelClient (the no-train surface) — not a self-built one
    assert isinstance(injected, ModelClient)


# --- AC-5: 0 writes to a tracked path ------------------------------------------


def test_deid_in_writes_nothing_to_a_tracked_path(monkeypatch):
    """AC-5: the boundary performs 0 filesystem writes during the call (raw stays in-memory).

    A write-spy patches every filesystem-write surface (`Path.write_text` / `Path.open` in a
    write mode / `builtins.open` in a write mode). `deid_in` is a pure in-memory call-through,
    so it records 0 writes — a boundary that persisted raw to a tracked path turns this RED.
    """
    from pathlib import Path

    writes = []

    real_write_text = Path.write_text
    real_path_open = Path.open
    real_builtin_open = open

    def spy_write_text(self, *args, **kwargs):
        writes.append(str(self))
        return real_write_text(self, *args, **kwargs)

    def spy_path_open(self, *args, **kwargs):
        mode = (args[0] if args else kwargs.get("mode", "r"))
        if any(m in mode for m in ("w", "a", "x", "+")):
            writes.append(str(self))
        return real_path_open(self, *args, **kwargs)

    def spy_builtin_open(file, *args, **kwargs):
        mode = (args[0] if args else kwargs.get("mode", "r"))
        if any(m in mode for m in ("w", "a", "x", "+")):
            writes.append(str(file))
        return real_builtin_open(file, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", spy_write_text)
    monkeypatch.setattr(Path, "open", spy_path_open)
    monkeypatch.setattr("builtins.open", spy_builtin_open)

    client = _FixedDeidClient(_deid_summary_fixture())
    deid_in(_raw_intake(), client)

    assert writes == [], f"deid_in wrote to the filesystem (must be 0 writes): {writes}"


# --- Risk R3 (crown-jewel): raw-PII leak probe over the EMITTED summary ----------


def test_emitted_summary_carries_no_raw_pii(tmp_path):
    """Risk R3 (crown-jewel): `pii_scan.scan_text` over the emitted summary returns 0.

    Seeds the synthetic raw-PII (name + lab) into the raw intake; the mock `deidentify`
    returns a de-identified fixture (carrying NONE of those tokens). The probe scans the
    EMITTED summary against an identity config matching the synthetic tokens — a clean
    de-identified summary scans 0. A `deid_in` that echoed `raw_intake` instead of the
    `deidentify` output would carry the synthetic name/lab and turn this RED.
    """
    config = _identity_config(tmp_path)
    client = _FixedDeidClient(_deid_summary_fixture())

    emitted = deid_in(_raw_intake(), client)
    emitted_text = json.dumps(emitted)

    assert pii_scan.scan_text(emitted_text, token_config=config) == 0


def test_leak_probe_reds_on_a_passthrough_boundary(tmp_path):
    """Negative control (failing-capable proof): the raw echo WOULD leak; `deid_in` blocks it.

    Constructs the exact passthrough failure the crown-jewel probe must catch: a `deidentify`
    that echoes the RAW intake. Scanning that echoed output DIRECTLY against the synthetic
    identity config registers >0 hits — proving `test_emitted_summary_carries_no_raw_pii` is
    failing-capable (it tests something, not a tautology). Since FIX 1's whitelist, routing the
    same echo THROUGH `deid_in` no longer leaks: the raw intake carries out-of-`SUMMARY_FIELD_SET`
    fields (`legal-name`, `raw-lab-values`), so the boundary rejects it to the sentinel — proven
    here by scanning the actual `deid_in` output and getting 0 (the boundary's positive value).
    """
    config = _identity_config(tmp_path)
    raw = _raw_intake()
    passthrough_client = _FixedDeidClient(raw)  # echoes raw — the leak the boundary must prevent

    # the raw echo itself WOULD leak (the probe is failing-capable, not a tautology)
    assert pii_scan.scan_text(json.dumps(raw), token_config=config) > 0
    # but the real boundary rejects the out-of-field-set echo -> the sentinel, 0 leak (FIX 1)
    blocked = deid_in(raw, passthrough_client)
    assert pii_scan.scan_text(json.dumps(blocked), token_config=config) == 0
    assert blocked["deidentified"] is False


# --- AC-2: fail-closed on ModelCallError ---------------------------------------


def test_deid_in_fail_closed_returns_honest_no_plan_sentinel():
    """AC-2: a `deidentify` that raises `ModelCallError` → the honest no-plan sentinel.

    Never a fabricated/partial summary, never a passthrough of the raw intake. The returned
    value is `{"deidentified": False, "reason": DEID_CALL_FAILED}` — the orchestrator treats a
    falsy/`deidentified: False` summary as "no de-identified summary → halt, dispatch nothing".
    """
    failing_client = _FixedDeidClient(ModelCallError("backend de-id call failed"))

    result = deid_in(_raw_intake(), failing_client)

    # the raise-path sentinel: the discriminator + reason are load-bearing; the raise path
    # also carries error_type (FIX 3, the exception class name — never its raw-bearing message).
    assert result["deidentified"] is False
    assert result["reason"] == DEID_CALL_FAILED
    assert result["error_type"] == "ModelCallError"
    assert DEID_CALL_FAILED == "deid-call-failed"


def test_deid_in_fail_closed_leaks_no_raw_pii(tmp_path):
    """AC-2 (the 0-leak-on-error half): the error-path return scans 0 raw-PII.

    Seeds the synthetic raw-PII into the raw intake, forces a `ModelCallError`, and asserts the
    serialized sentinel carries NONE of the synthetic name/lab tokens (the error path leaks
    nothing). A `deid_in` that returned the raw intake on error would carry the synthetic tokens
    and turn this RED — see `test_deid_in_error_path_is_failing_capable` for the explicit proof.
    """
    config = _identity_config(tmp_path)
    failing_client = _FixedDeidClient(ModelCallError("backend de-id call failed"))

    result = deid_in(_raw_intake(), failing_client)
    serialized = json.dumps(result)

    assert pii_scan.scan_text(serialized, token_config=config) == 0


def test_deid_in_error_path_is_failing_capable(tmp_path):
    """Negative control (failing-capable proof): a raw-passthrough-on-error WOULD leak.

    Constructs the exact broken error boundary the fail-closed contract must prevent: on a
    `ModelCallError`, return the RAW intake instead of the sentinel. Scanning that against the
    synthetic identity config registers >0 hits — proving `test_deid_in_fail_closed_leaks_no_raw_pii`
    is failing-capable (the assertion tests something, not a tautology), and that the ACTUAL
    `deid_in` (which returns the sentinel) is the safe one.
    """
    config = _identity_config(tmp_path)
    raw = _raw_intake()

    # the broken behavior the fail-closed branch replaces: raw-on-error passthrough
    def broken_deid_in_on_error(raw_intake, client):
        try:
            return client.deidentify(raw_intake)
        except ModelCallError:
            return raw_intake  # the leak the real boundary must NOT do

    failing_client = _FixedDeidClient(ModelCallError("backend de-id call failed"))
    leaked = broken_deid_in_on_error(raw, failing_client)

    assert pii_scan.scan_text(json.dumps(leaked), token_config=config) > 0
    # and the REAL deid_in does NOT leak on the same error
    safe = deid_in(raw, failing_client)
    assert pii_scan.scan_text(json.dumps(safe), token_config=config) == 0


# --- AC-3: the persisted-side `router.summarize` path is unchanged --------------


def test_persisted_side_summarize_scans_clean():
    """AC-3: the persisted-side `router.summarize`-derived summary scans 0 raw-PII.

    `deid_in` SUPERSEDES `summarize` as the de-id-IN on the plan path but `summarize` survives
    UNCHANGED as the persisted-side de-id; this asserts that path still produces a 0-raw-PII
    summary (the byte-unchanged half is the recipe's `git diff --numstat router.py` = 0 gate).
    Reuses the established clean-store-read fixture from `test_router`.
    """
    from tests.plan.test_router import _clean_store_read

    summary = router.summarize(_clean_store_read())
    summary_text = json.dumps(summary, default=str)

    assert pii_scan.scan_text(summary_text) == 0
    # the de-id gate is intact: only field-set fields, no named-excluded raw-PII field present
    assert set(summary.keys()) == set(router.SUMMARY_FIELD_SET)


# --- AC-4: 0 live-API calls (mock clients only) --------------------------------


def test_default_no_train_backend_makes_no_live_call_and_fails_closed():
    """AC-4: a default `ModelClient` makes 0 live de-id calls — it fails closed, not a real summary.

    The default `_ClaudeNoTrainBackend.deidentify` is `NotImplementedError` until the operator
    checkpoint; `_call` wraps that into `ModelCallError`, so `deid_in` over a default client
    returns the honest no-plan sentinel — NEVER a real de-identified summary (no live API call,
    0 spend). This proves the live backend is never successfully exercised in tests: a default
    client yields the fail-closed sentinel, not a model-authored payload. Every other `deid_in`
    test injects a fixture/mock client, so 0 live-API spend across the suite.
    """
    live_client = ModelClient()  # default _ClaudeNoTrainBackend (live method unimplemented)

    result = deid_in(_raw_intake(), live_client)

    # the default backend's NotImplementedError -> ModelCallError -> the raise-path sentinel
    # (with error_type, FIX 3); a real summary would carry no `deidentified` discriminator.
    assert result["deidentified"] is False, (
        "a default no-train client must fail closed (no live de-id call), not return a summary"
    )
    assert result["reason"] == DEID_CALL_FAILED


# --- FIX 1 (WHITELIST): the de-id-IN boundary enforces the positive field-set whitelist ----


def _contaminated_summary():
    """A de-id result carrying band-tokens PLUS a raw-PII field (the contamination case).

    A faithful de-id summary carries ONLY `router.SUMMARY_FIELD_SET` fields; this one smuggles
    in an out-of-set raw-PII field (`legal-name` + `raw-lab-values`) alongside valid band
    tokens. The de-id-IN boundary's whitelist must reject the whole dict (not return it).
    """
    return {
        "sex-for-dosing": "male",
        "legal-name": SYNTHETIC_NAME,
        "raw-lab-values": SYNTHETIC_LAB,
    }


def test_deid_in_rejects_out_of_field_set_contaminated_summary(tmp_path):
    """FIX 1 (WHITELIST): a de-id summary with an out-of-set raw-PII field → the sentinel.

    The de-id-IN boundary enforces the SAME positive field-set whitelist the persisted path
    (`router.dispatch`) enforces: `set(summary) <= set(router.SUMMARY_FIELD_SET)`. A summary
    carrying an out-of-set field (raw PII smuggled past a non-faithful de-id call) is NOT
    returned — `deid_in` fails closed to the honest no-plan sentinel, and the result scans 0
    raw-PII. A `deid_in` that returned the contaminated dict turns this RED.
    """
    config = _identity_config(tmp_path)
    client = _FixedDeidClient(_contaminated_summary())

    result = deid_in(_raw_intake(), client)

    assert result == {"deidentified": False, "reason": DEID_CALL_FAILED}
    assert pii_scan.scan_text(json.dumps(result), token_config=config) == 0


def test_deid_in_whitelist_passes_a_clean_in_set_summary():
    """FIX 1: a faithful summary (only `SUMMARY_FIELD_SET` fields) passes the whitelist.

    Proves the whitelist is a subset gate, not a fixed-shape gate — a clean de-identified
    summary carrying only field-set fields is returned verbatim (the success leg).
    """
    summary = _deid_summary_fixture()
    assert set(summary) <= set(router.SUMMARY_FIELD_SET)
    client = _FixedDeidClient(summary)

    assert deid_in(_raw_intake(), client) == summary


# --- SEC-1 (VALUE-SCAN): the key whitelist checks NAMES; this checks in-set VALUES for raw PII --


def _value_pii_summary(pii_value):
    """A summary whose KEYS are all in `SUMMARY_FIELD_SET` but ONE value carries raw PII.

    The key-name whitelist passes (`active-issue-class` is a field-set field); the
    contamination is in the VALUE — the exact gap the key-name-only whitelist misses (a
    faithless de-id echoing raw PII into an allowed field's value).
    """
    summary = _deid_summary_fixture()
    summary["active-issue-class"] = pii_value
    return summary


def test_deid_in_rejects_in_set_value_carrying_identity_pii(tmp_path):
    """SEC-1: an in-set key whose VALUE carries the operator's name → the value-PII sentinel.

    The key whitelist passes (`active-issue-class` is a `SUMMARY_FIELD_SET` field), but the
    value is the synthetic operator NAME. The value-level scan (identity-token config) catches
    it and `deid_in` fails closed to `{deidentified: False, reason: DEID_VALUE_PII}`; the result
    scans 0 raw-PII. A `deid_in` WITHOUT the value scan returns the contaminated summary — RED
    (the returned dict carries the name; the discriminator + scan assertions both fail).
    """
    config = _identity_config(tmp_path)
    client = _FixedDeidClient(_value_pii_summary(SYNTHETIC_NAME))

    result = deid_in(_raw_intake(), client, identity_config=config)

    assert result == {"deidentified": False, "reason": DEID_VALUE_PII}
    assert pii_scan.scan_text_full(json.dumps(result), token_config=config) == 0


def test_deid_in_rejects_in_set_value_carrying_contact_pii(tmp_path):
    """SEC-1: an in-set value carrying value-CLASS PII (email) → the sentinel, no config needed.

    The value-class patterns (email / phone / postal) run WITHOUT an identity-token config, so a
    contact-PII leak into an allowed field's value is caught even when the operator-identity file
    is absent — proving the value scan is not solely identity-token-dependent.
    """
    client = _FixedDeidClient(
        _value_pii_summary("reach me at jordan.fake@test-clinic.example.org")
    )

    result = deid_in(_raw_intake(), client, identity_config=tmp_path / "absent.txt")

    assert result["deidentified"] is False
    assert result["reason"] == DEID_VALUE_PII


def test_deid_in_value_scan_catches_pii_past_the_scan_text_cap(tmp_path):
    """SEC-1 (sc97): the value scan is NON-TRUNCATING — PII past `_MAX_SCAN_TEXT_LEN` is caught.

    The capped `scan_text` leaves a straddle hole at a value boundary; `deid_in` uses
    `scan_text_full`. A value whose raw-PII (the operator name) sits AFTER a long benign prefix
    (longer than the `scan_text` cap) must still fail closed — a `deid_in` that used the capped
    `scan_text` would return the contaminated summary (RED).
    """
    config = _identity_config(tmp_path)
    cap = pii_scan._MAX_SCAN_TEXT_LEN
    long_value = ("recovery " * ((cap // 9) + 200)) + SYNTHETIC_NAME
    assert len(long_value) > cap
    client = _FixedDeidClient(_value_pii_summary(long_value))

    result = deid_in(_raw_intake(), client, identity_config=config)

    assert result == {"deidentified": False, "reason": DEID_VALUE_PII}


def test_deid_in_value_scan_passes_a_clean_summary(tmp_path):
    """SEC-1: a clean band/class summary passes the value scan (the success leg is preserved).

    Proves the value scan does not false-positive on the legitimate band/class tokens — a clean
    de-identified summary is still returned verbatim with the scan in place.
    """
    config = _identity_config(tmp_path)
    summary = _deid_summary_fixture()
    client = _FixedDeidClient(summary)

    assert deid_in(_raw_intake(), client, identity_config=config) == summary


# --- FIX 2 (TEST-01): a REAL ModelClient(backend=_FixtureBackend(...)) wired into deid_in ----


def test_deid_in_with_real_client_malformed_backend_fails_closed(tmp_path):
    """FIX 2 (TEST-01): a REAL `ModelClient` over a malformed-result backend → the sentinel.

    Wires a real `ModelClient(backend=_FixtureBackend(deidentify_result="not-a-mapping"))`
    into `deid_in` (not a pre-built `ModelCallError`): the real client's shape-check RAISES
    `ModelCallError` on the non-mapping result, and `deid_in`'s except lands it on the honest
    no-plan sentinel. Proves the real client's raise composes with `deid_in` (the seam, end
    to end), scanning 0 raw-PII.
    """
    from tests.model.test_client import _FixtureBackend

    config = _identity_config(tmp_path)
    real_client = ModelClient(backend=_FixtureBackend(deidentify_result="not-a-mapping"))

    result = deid_in(_raw_intake(), real_client)

    # the real client's shape-check raised ModelCallError -> the raise-path sentinel
    # (carrying error_type, FIX 3); the discriminator + reason are the load-bearing keys.
    assert result["deidentified"] is False
    assert result["reason"] == DEID_CALL_FAILED
    assert result["error_type"] == "ModelCallError"
    assert pii_scan.scan_text(json.dumps(result), token_config=config) == 0


def test_deid_in_with_real_client_contaminated_backend_fails_closed(tmp_path):
    """FIX 2 (TEST-01, composes with FIX 1): a REAL client over a contaminated backend result.

    The backend returns a band-tokens-PLUS-raw-field mapping (truthy + a valid `dict`, so the
    real client's shape-check passes it through); `deid_in`'s WHITELIST then catches the
    out-of-set raw-PII field and fails closed to the sentinel. Proves FIX 1 and FIX 2 compose:
    the real client lands the dict, the de-id-IN whitelist rejects it.
    """
    from tests.model.test_client import _FixtureBackend

    config = _identity_config(tmp_path)
    real_client = ModelClient(
        backend=_FixtureBackend(deidentify_result=_contaminated_summary())
    )

    result = deid_in(_raw_intake(), real_client)

    assert result == {"deidentified": False, "reason": DEID_CALL_FAILED}
    assert pii_scan.scan_text(json.dumps(result), token_config=config) == 0


# --- FIX 3 (SEC-02): ANY exception from the de-id call fails closed (not only ModelCallError) -


def test_deid_in_fails_closed_on_non_model_call_error(tmp_path):
    """FIX 3 (SEC-02): a `deidentify` raising a NON-`ModelCallError` exception → the sentinel.

    A `ValueError` whose message embeds the RAW intake (`ValueError(f"bad {raw}")`) is the
    leak-via-traceback case the broadened except must catch: `deid_in` returns the honest
    no-plan sentinel, and the serialized sentinel scans 0 raw-PII — the raw in the exception
    message does NOT escape. A `deid_in` that caught only `ModelCallError` would let this
    propagate (raw in the traceback) and turn this RED.
    """
    config = _identity_config(tmp_path)
    raw = _raw_intake()

    class _RaisingValueErrorClient:
        def deidentify(self, raw_intake):
            raise ValueError(f"bad {raw_intake}")  # raw embedded in the message

    result = deid_in(raw, _RaisingValueErrorClient())

    assert result["deidentified"] is False
    assert result["reason"] == DEID_CALL_FAILED
    assert pii_scan.scan_text(json.dumps(result), token_config=config) == 0


def test_deid_in_records_exception_type_not_message(tmp_path):
    """FIX 3 (SEC-02): the sentinel records the exception TYPE name, never its message.

    To keep a genuine bug diagnosable WITHOUT leaking raw, the broadened except records
    `error_type` (the exception class name) — never the message/repr/args (which can carry
    raw). Asserts `error_type == "ValueError"` AND the sentinel still scans 0 raw-PII even
    though the raised message embedded the synthetic name/lab.
    """
    config = _identity_config(tmp_path)
    raw = _raw_intake()

    class _RaisingValueErrorClient:
        def deidentify(self, raw_intake):
            raise ValueError(f"bad {SYNTHETIC_NAME} {SYNTHETIC_LAB}")

    result = deid_in(raw, _RaisingValueErrorClient())

    assert result["error_type"] == "ValueError"
    assert pii_scan.scan_text(json.dumps(result), token_config=config) == 0
