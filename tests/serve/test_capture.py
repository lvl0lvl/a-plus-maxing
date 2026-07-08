"""By-data-class capture seam tests (ADR-0014-T1).

`scripts/serve/capture.py`'s `persist_capture` routes each submitted form field by
its data class (the recipe's Grounded Field Map): a de-identified `SUMMARY_FIELD_SET`
token -> the store via the UNCHANGED `store.append` tagged `source:"intake"`; a
raw/record-only value -> the gitignored `vault/scaffold/filled/` operator record;
never a raw value into a field-set store item.

Cycle 1 — AC-1 per-wired-field round-trip (each wired token -> `store.read` tagged
`source:"intake"` -> `summarize` returns it under the token), AC-6 curated-token-only
`rx-interaction-classes`, and the Risk Negative-1 setup (a Step-3 "train around"
capture writes a `raw-symptom-free-text` item that `summarize` DERIVES into
`active-issue-class`, never the raw text).

Cycle 3 — the PII-boundary proofs: the fresh-clone tracked-tree scan returns 0
operator tokens after a full capture session, `summarize` RAISES on a raw-PII value
planted into a field-set item, and `block-pii-commit` would DENY a staged filled
scaffold. Each gate carries its negative control proving it is failing-capable.
"""

import functools
import importlib
import subprocess
import sys
from pathlib import Path

from scripts.guard import pii_scan
from scripts.plan.router import SUMMARY_FIELD_SET, dispatch, summarize
from scripts.serve import capture
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# An identity config that is ABSENT on disk: identity-token detection is empty (the
# operator's real name/contact are not in the tree), while the value-class patterns
# (any-domain email, phone, postal) still run — exactly the fresh-clone posture.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"


def _bound(root):
    """The instance-bound store_read `summarize` requires (recipe caller contract)."""
    return functools.partial(store.read, root=root)


def _summary(root):
    """Run `summarize` over a tmp instance with an absent identity config."""
    return summarize(_bound(root), identity_config=_ABSENT_IDENTITY)


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 per-wired-field round-trip
# --------------------------------------------------------------------------- #

# The de-identified wired tokens this task captures, each with a synthetic value
# that is a valid de-identified token (no raw PII) and is distinctive enough that a
# cross-stream leak would be detectable.
# `rx-interaction-classes` is NOT here (Wave-B FIX-A): the untrusted form field routes
# record-only, never into the model-bound store item — see the FIX-A tests below.
_WIRED_VALUES = {
    "goal-domains": "Workout;Nutrition",  # in the FIX-B chip enum (Workout/Nutrition/…)
    "goal-targets": "add 10 lb to squat by september",
    "goal-priority-order": "1-strength;2-recovery;3-longevity",
    "hard-limits": "no overhead pressing; one rest day minimum",
    "recovery-status-band": "moderate",
}


def test_every_wired_token_is_in_the_field_set():
    """AC-1: every token the capture seam writes to the store is a SUMMARY_FIELD_SET member.

    Grounds the capture seam's wired-token set against the LIVE allowlist — a token
    the seam would write that is NOT in the field set is a bug (it would write a
    novel store item `summarize`/`dispatch` reject). The module's load-time tripwire
    enforces the same; this pins it from the test side.
    """
    for token in _WIRED_VALUES:
        assert token in SUMMARY_FIELD_SET, f"{token!r} is not a SUMMARY_FIELD_SET token"
    assert set(capture.WIRED_TOKENS) <= set(SUMMARY_FIELD_SET), (
        "capture.WIRED_TOKENS carries a token absent from SUMMARY_FIELD_SET"
    )


def test_wired_field_round_trips_store_then_summarize(tmp_path):
    """AC-1: each wired field -> store item (source:"intake") -> summarize under its token.

    For each wired de-identified token, persist a synthetic value into a tmp store
    root via the capture seam, assert `store.read(token)` returns the reading tagged
    `source:"intake"` with the captured value, and assert `summarize` returns that
    value under the token name. Asserts 0 wired fields are missing from the summary.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        dict(_WIRED_VALUES), root=store_root, scaffold_root=scaffold_root,
        identity_config=_ABSENT_IDENTITY,
    )

    summary = _summary(store_root)
    for token, value in _WIRED_VALUES.items():
        readings = store.read(token, root=store_root)
        assert len(readings) == 1, f"{token!r} did not land exactly one reading"
        assert readings[0]["source"] == "intake", f"{token!r} not tagged source:intake"
        assert readings[0]["value"] == value, f"{token!r} stored the wrong value"
        assert summary.get(token) == value, f"summarize did not return {token!r} under its token"

    missing = [t for t in _WIRED_VALUES if summary.get(t) != _WIRED_VALUES[t]]
    assert not missing, f"wired fields missing from the summary: {missing}"


def test_wired_token_value_is_a_utc_offset_timepoint(tmp_path):
    """AC-1: the capture write carries a UTC-offset timepoint (store sort correctness).

    The store's `read` sorts lexicographically on `timepoint` and assumes the
    producer wrote a UTC-offset string. A capture write that omitted the offset
    would sort wrong against other producers; assert the offset is present.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"goal-domains": "Workout"}, root=store_root, scaffold_root=tmp_path / "scaffold",
        identity_config=_ABSENT_IDENTITY,
    )
    tp = store.read("goal-domains", root=store_root)[0]["timepoint"]
    assert tp.endswith("+00:00") or "+" in tp[10:] or tp[10:].count("-") >= 1, (
        f"timepoint {tp!r} is not a UTC-offset string"
    )


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-6 curated-token-only rx-interaction-classes (Risk Falsification rx)
# --------------------------------------------------------------------------- #


def test_rx_form_field_never_writes_the_model_bound_store_item(tmp_path):
    """AC-6 (Wave-B FIX-A): the rx FORM field never writes the `rx-interaction-classes` store item.

    Even a value that LOOKS like clean class tokens (`bleeding-risk;cyp3a4-pgp`) from the
    untrusted form field must NOT reach the model-bound store item — the server cannot
    distinguish it from a raw drug name. The field is captured record-only; the model-bound
    item is fed only by the liaison curation path (the beaded ADR-0014 OQ-2 surface).
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"rx-interaction-classes": "bleeding-risk;cyp3a4-pgp"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("rx-interaction-classes", root=store_root) == [], (
        "the rx form field wrote the model-bound store item (must route record-only)"
    )


def test_serve_layer_has_no_raw_drug_to_class_lookup():
    """AC-6 / Risk Falsification rx: scripts/serve/ carries 0 raw-drug-name->class map.

    The de-identification (drug name -> interaction class) is a CURATION step at the
    store layer per router.py, NEVER a code lookup in the serve layer. Assert no
    pharmacology map (a dict literal keyed on a raw drug name mapping to a class
    token) enters scripts/serve/. Reds if such a lookup is added.
    """
    serve_dir = REPO_ROOT / "scripts" / "serve"
    # A raw-drug-name -> interaction-class lookup would name common drugs as keys.
    raw_drug_markers = ("warfarin", "aspirin", "ibuprofen", "metformin", "statin", "ssri")
    for py in serve_dir.glob("*.py"):
        src = py.read_text().lower()
        for marker in raw_drug_markers:
            assert marker not in src, (
                f"{py.name} references a raw drug name {marker!r} — a raw-name->class "
                f"lookup must not enter the serve layer (de-id is a store-layer curation)"
            )


def test_raw_drug_name_in_supplement_stack_never_reaches_a_field_set_item(tmp_path):
    """AC-6 (Wave-B FIX-A): a raw drug name in the raw stack never reaches a field-set item.

    A raw supplement/drug name (Step-5 raw stack) is a record-only field -> the
    gitignored scaffold, NEVER any `SUMMARY_FIELD_SET` store item. With the rx form
    field now also record-only (FIX-A), the `rx-interaction-classes` model-bound item
    is never written by capture at all — assert it stays empty and no field-set item
    carries the drug name.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {
            "rx-interaction-classes": "bleeding-risk",
            "supplement-stack": "warfarin 5mg; fish oil 2g",  # record-only raw stack
        },
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("rx-interaction-classes", root=store_root) == [], (
        "the rx form field wrote the model-bound store item (must route record-only)"
    )
    for token in SUMMARY_FIELD_SET:
        for reading in store.read(token, root=store_root):
            assert "warfarin" not in str(reading["value"]), (
                f"a raw drug name leaked into the {token!r} field-set store item"
            )


# --------------------------------------------------------------------------- #
# Cycle 1 — Risk Negative-1 setup: active-issue-class indirection
# --------------------------------------------------------------------------- #


def test_train_around_writes_raw_symptom_item_summarize_derives_issue_class(tmp_path):
    """Risk Negative-1: a Step-3 'train around' capture -> raw-symptom item -> derived class.

    The "train around / injury" input writes a `raw-symptom-free-text` store item
    (NOT `active-issue-class` directly). `summarize` then DERIVES `active-issue-class`
    from it as a de-identified body-region class — the raw text never appears under
    the field-set token.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"train-around": "tweaked my lower back deadlifting last week"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # The raw item is written under raw-symptom-free-text, NOT active-issue-class.
    assert store.read("raw-symptom-free-text", root=store_root), "train-around did not write the raw-symptom item"
    assert store.read("active-issue-class", root=store_root) == [], (
        "train-around wrongly wrote active-issue-class directly (must be derived, not stored)"
    )
    summary = _summary(store_root)
    assert summary.get("active-issue-class") == "back-region", (
        "summarize did not derive active-issue-class from the raw-symptom item"
    )
    # The raw free-text never appears under the field-set token.
    assert "deadlifting" not in str(summary.get("active-issue-class", ""))


# --------------------------------------------------------------------------- #
# Wave-B Tier-2 FIX-A — the rx field is captured record-only, never model-bound
# --------------------------------------------------------------------------- #


def test_rx_field_drug_name_lands_in_scaffold_never_a_field_set_item(tmp_path):
    """FIX-A: a raw drug name in the rx field -> the gitignored scaffold, NEVER the store/summary.

    The Step-5 `rx-interaction-classes` FORM field collects operator-typed text the
    server cannot trust to be de-identified class tokens — a raw drug name ("warfarin
    5mg") would route verbatim into the `rx-interaction-classes` field-set store item,
    which `summarize` sends to the model, and the `pii_scan` value gate does NOT catch
    drug names. So the capture seam routes that field to the gitignored scaffold
    record-only (the curation surface that emits real de-identified class tokens is the
    beaded ADR-0014 OQ-2 future consumer). Assert the drug name lands in the scaffold,
    and appears in NO SUMMARY_FIELD_SET store item and NOT in the summary.

    Failing-capable: re-add `rx-interaction-classes` to `capture.WIRED_TOKENS` and the
    drug name reaches the store item + summary, reddening both negative assertions.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {"rx-interaction-classes": "warfarin 5mg; metformin 500mg"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )

    # Positive: the captured rx text landed in the gitignored scaffold record.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "warfarin" in scaffold_text, "the rx field value did not land in the gitignored scaffold"

    # Negative (load-bearing): the drug name is in NO field-set store item.
    for token in SUMMARY_FIELD_SET:
        for reading in store.read(token, root=store_root):
            assert "warfarin" not in str(reading["value"]), (
                f"a raw drug name reached the {token!r} field-set store item (model-bound)"
            )
    # Negative (load-bearing): the drug name never reaches the summary the model sees.
    summary = _summary(store_root)
    assert "warfarin" not in str(summary.get("rx-interaction-classes", "")), (
        "a raw drug name reached the rx-interaction-classes summary value (model-bound)"
    )
    assert "warfarin" not in str(summary), "a raw drug name reached the model-bound summary"


def test_out_of_enum_recovery_band_routes_record_only_not_the_token(tmp_path):
    """FIX-B: a crafted out-of-set recovery-status-band -> scaffold, NEVER the token.

    `recovery-status-band` is a bounded `<select>` (low/moderate/high), enforced only
    client-side. A crafted POST writing `extreme` must NOT land in the model-bound token
    — the server re-validates against the enum and routes the out-of-set value
    record-only to the gitignored scaffold.

    Failing-capable: drop the bounded-value check and `extreme` lands in the token store
    item, reddening the negative assertion.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {"recovery-status-band": "extreme"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("recovery-status-band", root=store_root) == [], (
        "an out-of-enum recovery-status-band reached the model-bound token store item"
    )
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "extreme" in scaffold_text, "the out-of-enum value did not land record-only in the scaffold"
    # A valid band still lands in the token (the gate is selective, not a blanket block).
    capture.persist_capture(
        {"recovery-status-band": "moderate"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    band = store.read("recovery-status-band", root=store_root)
    assert band and band[0]["value"] == "moderate", "a valid recovery band did not land in the token"


def test_out_of_enum_goal_domains_routes_record_only_not_the_token(tmp_path):
    """FIX-B: a crafted out-of-set goal-domains token -> scaffold, NEVER the token.

    `goal-domains` is a fixed chip set (Workout/Nutrition/Supplements/Peptides). A
    crafted POST whose `;`-joined value carries an out-of-set token (`Workout;Hacking`)
    must NOT land in the model-bound token — the server validates EVERY token against
    the enum and routes the whole out-of-set value record-only.

    Failing-capable: drop the bounded-value check and `Hacking` lands in the token.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {"goal-domains": "Workout;Hacking"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("goal-domains", root=store_root) == [], (
        "an out-of-enum goal-domains value reached the model-bound token store item"
    )
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "Hacking" in scaffold_text, "the out-of-enum goal-domains did not land record-only"
    # A wholly in-enum multi-value still lands in the token.
    capture.persist_capture(
        {"goal-domains": "Workout;Nutrition"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    gd = store.read("goal-domains", root=store_root)
    assert gd and gd[0]["value"] == "Workout;Nutrition", "an in-enum goal-domains did not land in the token"


def test_separators_only_goal_domains_routes_record_only_not_the_token(tmp_path):
    """FIX (F3): a separators-only goal-domains value routes record-only, never the token.

    `_bounded_value_ok` split a `;`-joined value and required every NON-EMPTY token to be
    in the enum — but a separators-only value (`";;;"`) filters to an EMPTY token list, so
    `all()` over nothing was vacuously True and `";;;"` was written verbatim into the
    model-bound goal-domains token. An empty token list is INVALID; the value routes
    record-only to the gitignored scaffold.

    Failing-capable: under the old vacuous-true `all(... if tok.strip())`, `";;;"` lands in
    the token store item, reddening the negative assertion.
    """
    assert capture._bounded_value_ok("goal-domains", ";;;") is False, (
        "a separators-only goal-domains value was accepted (vacuous all() over empty tokens)"
    )
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {"goal-domains": ";;;"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("goal-domains", root=store_root) == [], (
        "a separators-only goal-domains value reached the model-bound token store item"
    )
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert ";;;" in scaffold_text, "the separators-only value did not route record-only"
    # A whitespace-padded separators-only value is likewise rejected by the gate.
    assert capture._bounded_value_ok("goal-domains", " ; ; ") is False, (
        "a whitespace-padded separators-only goal-domains value was accepted"
    )


def test_rx_interaction_classes_is_not_a_wired_capture_token():
    """FIX-A: the capture seam does NOT wire `rx-interaction-classes` to the store.

    The form field carries operator-typed text, not trusted curated class tokens, so it
    is captured record-only — it must NOT be in `WIRED_TOKENS`. (The store item of that
    name is still a SUMMARY_FIELD_SET member fed by the liaison curation path, unchanged.)
    """
    assert "rx-interaction-classes" not in capture.WIRED_TOKENS, (
        "the rx form field must route record-only, not into the model-bound store item"
    )


# --------------------------------------------------------------------------- #
# Wave-B Tier-2 FIX-C — full-value PII scan on free-text wired tokens
# --------------------------------------------------------------------------- #


def test_free_text_token_pii_past_the_4096_cap_routes_record_only(tmp_path):
    """FIX-C: PII past `scan_text`'s 4096-char cap is caught on the capture path.

    `pii_scan.scan_text` caps its input at 4096 chars, so an email planted PAST the cap
    in a free-text wired token (`goal-targets`/`hard-limits`) would evade the single-call
    8j6 gate and land in the model-bound token. The capture path scans the FULL value, so
    PII anywhere in it is caught and the value routes record-only to the gitignored
    scaffold, never the token.

    Failing-capable: a single capped `scan_text(value)` returns 0 for this input (the
    email is past 4096), so reverting the full-value scan lets the value reach the token,
    reddening the negative assertion.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    # A long clean lead-in PAST 4096 chars, then an email — the email is beyond the cap.
    padded = ("add 10 lb to my squat. " * 250) + " reach me at operator@example.com"
    assert len(padded) > 4096, "the fixture must place the email past the 4096-char cap"
    # Pre-condition: a single capped scan MISSES the past-cap email (the evasion).
    assert pii_scan.scan_text(padded, token_config=_ABSENT_IDENTITY) == 0, (
        "the capped single scan unexpectedly caught the past-cap email — fixture invalid"
    )

    capture.persist_capture(
        {"goal-targets": padded},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Negative (load-bearing): the PII value never reached the model-bound token.
    assert store.read("goal-targets", root=store_root) == [], (
        "a free-text value carrying past-cap PII reached the model-bound goal-targets token"
    )
    # Positive: it landed record-only in the gitignored scaffold instead.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "operator@example.com" in scaffold_text, "the PII free-text value did not route record-only"

    # The gate is selective: a clean free-text value still lands in the token.
    capture.persist_capture(
        {"hard-limits": "no overhead pressing"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    hl = store.read("hard-limits", root=store_root)
    assert hl and hl[0]["value"] == "no overhead pressing", "a clean free-text value did not land in the token"


def test_canadian_postal_in_free_text_token_routes_record_only(tmp_path):
    """nue-CA: a Canadian postal typed into a free-text wired token routes record-only.

    The operator is in Nova Scotia. A Canadian street address (`B2Y 1A1`) typed into a
    free-text goals field must NOT reach the model-bound `goal-priority-order` token (a
    raw-PII egress on the crown-jewel boundary) — it routes record-only to the gitignored
    scaffold instead. Failing-capable: without the Canadian postal pattern the value scans
    0 and lands in the token, reddening the negative assertion.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    value = "prioritize squat first, ship gear to 27 Portland St, Dartmouth NS B2Y 1A1"
    # Pre-condition: the full-value scan catches the Canadian postal (the gate's trigger).
    assert pii_scan.scan_text_full(value, token_config=_ABSENT_IDENTITY) >= 1, (
        "the Canadian postal was not detected by scan_text_full — fixture/pattern invalid"
    )

    capture.persist_capture(
        {"goal-priority-order": value},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Negative (load-bearing): the Canadian-postal value never reached the model-bound token.
    assert store.read("goal-priority-order", root=store_root) == [], (
        "a free-text value carrying a Canadian postal reached the model-bound token"
    )
    for token in SUMMARY_FIELD_SET:
        readings = store.read(token, root=store_root)
        assert all("B2Y" not in str(r.get("value")) for r in readings), (
            f"the Canadian postal leaked into the {token!r} field-set store item"
        )
    # Positive: it landed record-only in the gitignored scaffold instead.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "B2Y 1A1" in scaffold_text, "the Canadian-postal value did not route record-only"


def test_dob_in_free_text_token_routes_record_only(tmp_path):
    """yduw: a full DOB typed into a free-text wired token routes record-only.

    Security EXECUTED the leak at the T9 review — a DOB in `goal-targets` crossed to the
    no-train dispatch because pii_scan had no date detector. With the yduw fix,
    `scan_text_full` catches the DOB at capture, so it must NOT reach the model-bound
    `goal-targets` token — it routes record-only to the gitignored scaffold instead.
    Failing-capable: without the date detector the value scans 0 and lands in the token.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    value = "reach peak by birthday 1986-03-14"
    # Pre-condition: the full-value scan catches the DOB (the capture gate's trigger).
    # include_dob=True mirrors capture._value_has_pii's opt-in (the DOB class is opt-in,
    # default off, so the byte-frozen engine scans stay unaffected — see the pii_scan note).
    assert pii_scan.scan_text_full(value, token_config=_ABSENT_IDENTITY, include_dob=True) >= 1, (
        "the DOB was not detected by scan_text_full — fixture/pattern invalid"
    )

    capture.persist_capture(
        {"goal-targets": value},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Negative (load-bearing): the DOB value never reached the model-bound token.
    assert store.read("goal-targets", root=store_root) == [], (
        "a free-text value carrying a full DOB reached the model-bound goal-targets token"
    )
    for token in SUMMARY_FIELD_SET:
        readings = store.read(token, root=store_root)
        assert all("1986-03-14" not in str(r.get("value")) for r in readings), (
            f"the DOB leaked into the {token!r} field-set store item"
        )
    # Positive: it landed record-only in the gitignored scaffold instead.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "1986-03-14" in scaffold_text, "the DOB value did not route record-only"


# A PII token whose match span EXCEEDS the old `overlap=64`, so positioned across the
# old window step boundary (~char 4032) it was seen WHOLE by neither overlapping window
# and leaked. A 79-char postal (span > 64) and an email — both real `scan_text_full`
# hits (proven below) — are the straddle probes.
_STRADDLE_POSTAL = "12345 Northwest Industrial Distribution Center Boulevard, Springfield, IL 62704."
_STRADDLE_EMAIL = "reach me at operator.fieldtest@example.com."
# The OLD window geometry the straddle targets: window length 4096, step 4096-64=4032,
# so the boundary the old code stepped past sits at char 4032.
_OLD_WINDOW = 4096
_OLD_STEP = _OLD_WINDOW - 64


def _straddle_value(token, boundary):
    """A >4096-char free-text value with `token` centred on `boundary` (clean padding).

    The padding is digit-free, sentence-terminated prose so it forms no spurious PII
    match and ends cleanly before `token`; the trailing prose follows the token's own
    terminating `.` so the postal ZIP tail-guard is satisfied.
    """
    unit = "add weight to my squat slowly. "  # 31 chars, no digits, ends '. '
    start = boundary - len(token) // 2
    prefix = (unit * (start // len(unit) + 1))[:start]
    return prefix + token + " " + unit * 300


def test_free_text_pii_straddling_the_old_window_boundary_routes_record_only(tmp_path):
    """FIX-C straddle: PII across the old window step boundary routes record-only.

    The earlier FIX-C past-cap test planted PII only at the very END of the value (wholly
    inside the final window), so `overlap` was never exercised — mutating it to 0 left the
    capture tests green. This sweeps a long postal AND an email across a band of offsets
    around the old step boundary (char 4032) inside a >4096-char value, asserting at EVERY
    offset the value routes record-only (absent from the store token, present in the
    gitignored scaffold). Under the old `overlap=64` windowing a postal of span > 64 sat
    in the dead zone between the two windows and leaked; the single non-truncating scan
    has no boundary to straddle.

    Failing-capable: pre-condition asserts each probe is a real `scan_text_full` hit; the
    fix is proven RED by reverting `_value_has_pii` to the `overlap=64` windowing.
    """
    for probe, marker in ((_STRADDLE_POSTAL, "62704"), (_STRADDLE_EMAIL, "operator.fieldtest@example.com")):
        # Pre-condition: the probe IS a real full-value PII hit (else the test proves nothing).
        assert pii_scan.scan_text_full(probe, token_config=_ABSENT_IDENTITY) >= 1, (
            f"straddle probe {probe!r} is not a value-PII hit — fixture invalid"
        )
        # Sweep the band of boundary offsets that straddle the old [4032, 4096] dead zone.
        for boundary in range(_OLD_STEP - 40, _OLD_WINDOW + 8):
            value = _straddle_value(probe, boundary)
            assert len(value) > 4096, "the straddle fixture must exceed the 4096-char cap"
            store_root = tmp_path / f"store-{marker[:6]}-{boundary}"
            scaffold_root = tmp_path / f"scaffold-{marker[:6]}-{boundary}"
            capture.persist_capture(
                {"goal-targets": value},
                root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
            )
            # Negative (load-bearing): the PII value never reached the model-bound token.
            assert store.read("goal-targets", root=store_root) == [], (
                f"PII probe {marker!r} at boundary offset {boundary} reached the model-bound "
                f"goal-targets token (straddle leak)"
            )
            # Positive: it landed record-only in the gitignored scaffold instead.
            scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
            assert marker in scaffold_text, (
                f"PII probe {marker!r} at boundary offset {boundary} did not route record-only"
            )


# --------------------------------------------------------------------------- #
# Cycle 3 — AC-2 two-surface negative placement (record-only -> scaffold ONLY)
# --------------------------------------------------------------------------- #


def test_record_only_field_lands_in_scaffold_not_in_any_field_set_item(tmp_path):
    """AC-2 / Risk Negative-2: a record-only value lands ONLY under the scaffold root.

    A field with no de-identified field-set consumer (an arbitrary record-only field) and
    the FIX-A record-only `rx-interaction-classes` form field are record-only — they land
    under the gitignored scaffold root and NOT under any SUMMARY_FIELD_SET store item (the
    project assert-placement mandate: assert NOT in the wrong place). (NOTE ADR-0019-T1:
    the former `supplement-stack` example here is now a WIRED raw source — it writes the
    `raw-supplement-free-text` named-excluded store item, no longer record-only — so this
    test uses genuinely-record-only fields to keep proving the scaffold-routing path.)
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    record_only = {
        "favorite-color": "mediterranean-ish, high protein",
        "rx-interaction-classes": "creatine monohydrate 5g",
    }
    capture.persist_capture(
        record_only, root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )

    # Positive: the record-only values are present somewhere under the scaffold root.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "mediterranean" in scaffold_text, "the favorite-color record-only value did not land in the scaffold"
    assert "creatine" in scaffold_text, "the rx record-only value did not land in the scaffold"

    # Negative (the load-bearing assertion): NO SUMMARY_FIELD_SET store item carries a
    # record-only value. Iterate EVERY field-set token.
    for token in SUMMARY_FIELD_SET:
        for reading in store.read(token, root=store_root):
            v = str(reading["value"])
            assert "mediterranean" not in v and "creatine" not in v, (
                f"a record-only value leaked into the {token!r} field-set store item"
            )


# --------------------------------------------------------------------------- #
# Cycle 3 — AC-3 fresh-clone PII scan + AC-4 summarize-gate-raises
# --------------------------------------------------------------------------- #


_ABSENT_CONTACT = "vault/meta/__no_such_contact_config__.txt"


def test_full_capture_session_leaves_tracked_tree_pii_free(tmp_path):
    """AC-3 / Risk Negative-1: after a full capture session, the TRACKED tree carries 0 PII.

    Run a full synthetic Steps-2..5 capture against tmp roots (the values include a
    distinctive record-only string), then run the SINGLE-SOURCED scan policy
    `pii_scan.scan_scoped` — the exact policy the `block-pii-commit` hook + the
    pre-push backstop run — over the git-tracked file set in the fresh-clone posture
    (no operator identity/contact configs, no data-bearing paths). The captured
    values live ONLY under the gitignored store + scaffold, so the tracked tree
    carries 0 operator tokens.

    (`scan_scoped`, not raw `scan`: the trunk scanner applies the structural
    store-line patterns ONLY to non-fixture paths — `tests/` fixtures embed synthetic
    reading-shaped literals by construction, the documented known-fixture partition,
    so a raw whole-tree structural scan floods on them. `scan_scoped` is the policy
    that holds the clonability guarantee this AC asserts.)

    Failing-capable per the planted-leak control below: a real operator token written
    into a tracked path IS caught.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {
            **_WIRED_VALUES,
            "dietary-pattern": "high protein",
            "supplement-stack": "creatine monohydrate 5g",
            "train-around": "lower back caution",
        },
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    hits = pii_scan.scan_scoped(
        tracked, [], contact_config=_ABSENT_CONTACT, identity_config=_ABSENT_IDENTITY,
    )
    assert hits == 0, f"the tracked tree carries {hits} operator-PII hit(s) after a capture session"

    # Sanity: the capture DID write under the gitignored roots (the values live there).
    assert store.read("goal-domains", root=store_root), "the capture wrote nothing to the tmp store"
    assert list(scaffold_root.rglob("*")), "the capture wrote nothing to the tmp scaffold"

    # NEGATIVE CONTROL (failing-capable): plant a real operator-contact token into a
    # tracked-path-shaped file and confirm the SAME scan policy catches it — proving
    # the 0-hit result above is a real clean, not a constant-zero scan.
    leak = tmp_path / "leaked-tracked.md"
    leak.write_text("reach the operator at operator@example.com")
    contact_cfg = tmp_path / "contact.txt"
    contact_cfg.write_text(r"operator@example\.com")
    planted = pii_scan.scan_scoped(
        [str(leak)], [], contact_config=str(contact_cfg), identity_config=_ABSENT_IDENTITY,
    )
    assert planted >= 1, "the scan policy did not catch a planted operator-contact leak (not failing-capable)"


def test_summarize_raises_on_raw_pii_planted_in_field_set_item(tmp_path):
    """AC-4 / Risk Negative-1: summarize RAISES on raw PII in a field-set item (adversarial).

    Plant a raw-PII value (an email) into a pass-through SUMMARY_FIELD_SET store item
    via `store.append` (simulating a capture bug that mis-routed raw text into a
    field-set item). `summarize` must RAISE ValueError (the 8j6 fail-closed gate) —
    the runtime backstop the boundary depends on.

    Failing-capable per the negative control below.
    """
    store_root = tmp_path / "store"
    # NEGATIVE CONTROL: a CLEAN field-set value does NOT raise (the gate is selective).
    capture.persist_capture(
        {"goal-targets": "add 10 lb to squat"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    _summary(store_root)  # must not raise on the clean value

    # Now plant raw PII into a field-set item (a mis-routed capture bug, simulated).
    import datetime
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    store.append(
        "hard-limits",
        {"item": "hard-limits", "timepoint": ts, "source": "intake",
         "value": "contact me at operator@example.com"},
        root=store_root,
    )
    try:
        _summary(store_root)
    except ValueError:
        pass  # expected — the gate raised on the planted PII
    else:
        raise AssertionError("summarize did NOT raise on raw PII planted in a field-set item")


def test_block_pii_commit_denies_a_staged_filled_scaffold(tmp_path):
    """AC-3-deny: block-pii-commit would DENY a staged vault/scaffold/filled/ value.

    Stage a filled-scaffold value under `vault/scaffold/filled/` in a throwaway git
    repo (so the real tree is untouched), then invoke the hook with a `git commit`
    command and assert the deny verdict. Honors the commit-sequencing rule: the
    staging `git add` runs as its OWN command, separate from the asserted commit.
    """
    import json
    import os

    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    # The scaffold prefix the hook denies on (single-sourced in pii-scan-scope.sh).
    scaffold_file = repo / "vault" / "scaffold" / "filled" / "operator-record.json"
    scaffold_file.parent.mkdir(parents=True)
    scaffold_file.write_text('{"dietary-pattern": "high protein"}\n')
    # Stage as its OWN command (the sequencing rule).
    subprocess.run(["git", "add", "vault/scaffold/filled/operator-record.json"], cwd=repo, check=True)

    hook = REPO_ROOT / ".claude" / "hooks" / "block-pii-commit.sh"
    hook_input = json.dumps({
        "tool_input": {"command": "git commit -m 'add record'"},
        "cwd": str(repo),
    })
    env = dict(os.environ, BLOCK_PII_COMMIT_PROJECT_ROOT=str(repo))
    proc = subprocess.run(
        ["bash", str(hook)], input=hook_input, cwd=repo, env=env,
        capture_output=True, text=True,
    )
    assert '"permissionDecision":"deny"' in proc.stdout, (
        f"block-pii-commit did not DENY a staged filled scaffold; stdout={proc.stdout!r} stderr={proc.stderr!r}"
    )


# --------------------------------------------------------------------------- #
# ADR-0017-T1 H-2 — instance identity_config threading (AC-5)
# --------------------------------------------------------------------------- #


def test_identity_config_round_trip_changes_detection(tmp_path):
    """AC-5/H-2: an operator-identity token routes record-only WITH identity_config, lands WITHOUT it.

    The H-2 gap is empty operator-identity detection when the capture call DROPS
    `identity_config` (the today's `/upload` omission). This round-trip proves the
    threading is NOT a no-op: a free-text value carrying the operator's name routes
    record-only WHEN an instance `identity_config` listing that name is threaded, and
    lands in the model-bound token WHEN it is the empty/absent baseline (no identity
    detection). Same value, same gate — only the threaded config differs.

    Failing-capable: drop `identity_config` at the call (the baseline) and the name
    reaches the model-bound token, reddening the record-only assertion.
    """
    # An instance identity config listing the operator name token (one regex per line).
    identity_cfg = tmp_path / "operator-identity.txt"
    identity_cfg.write_text("Walter McGivney\n")
    value = "add 10 lb to squat; ask Walter McGivney before changing the program"

    # WITH the instance config threaded: the name is detected -> record-only to scaffold.
    store_with = tmp_path / "store-with"
    scaffold_with = tmp_path / "scaffold-with"
    capture.persist_capture(
        {"goal-targets": value},
        root=store_with, scaffold_root=scaffold_with, identity_config=str(identity_cfg),
    )
    assert store.read("goal-targets", root=store_with) == [], (
        "an operator-identity value reached the model-bound token WITH identity_config threaded"
    )
    scaffold_text = "".join(p.read_text() for p in scaffold_with.rglob("*") if p.is_file())
    assert "McGivney" in scaffold_text, "the identity value did not route record-only WITH the config"

    # WITHOUT it (the empty-detection baseline): identity detection is empty, so the
    # value lands in the model-bound token — the exact H-2 gap. This is the no-op
    # baseline the threading changes.
    store_without = tmp_path / "store-without"
    capture.persist_capture(
        {"goal-targets": value},
        root=store_without, scaffold_root=tmp_path / "scaffold-without",
        identity_config=_ABSENT_IDENTITY,
    )
    landed = store.read("goal-targets", root=store_without)
    assert landed and "McGivney" in landed[0]["value"], (
        "the empty-detection baseline did not land the value — the round-trip proves nothing"
    )


def test_upload_call_site_threads_identity_config():
    """AC-5/H-2: the existing /upload persist_capture call threads `identity_config=`.

    The H-2 factory-to-component wiring gap was the `/upload` handler calling
    `persist_capture` WITHOUT `identity_config` (server.py:158-159), silently disabling
    operator-identity detection at that capture call site. This asserts the call now
    passes `identity_config=` — closing the omission. Reds if the parameter is dropped.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "server.py").read_text()
    # The /upload persist_capture call must thread identity_config — the H-2 fix.
    import re as _re
    call = _re.search(r"capture\.persist_capture\((.*?)\)", src, _re.DOTALL)
    assert call is not None, "the /upload persist_capture call was not found in server.py"
    assert "identity_config=" in call.group(1), (
        "the /upload persist_capture call drops identity_config — the H-2 gap (empty "
        "identity detection) is still open"
    )


def test_identity_config_seam_threads_to_every_capture_call_site():
    """AC-5/H-2: the instance identity_config seam exists for every capture call site.

    The H-2 invariant is that EVERY capture call site threads the instance
    `identity_config` through the SAME class-attr seam as `store_root`/`scaffold_root`,
    so operator-identity PII detection is non-empty at all of them. This task closes the
    `/upload` site and pins the seam (`build_server(..., identity_config=...)` -> the
    handler class attr -> the call) so `ADR-0016-T1`'s `/chat` capture call threads
    `self.identity_config` the same way (the generic-seam form: the mechanism is wired
    here, the `/chat` call site lands with the dispatch).

    Reds if the seam is removed (no `identity_config` kwarg on `build_server`, or the
    handler does not read `self.identity_config` into the call).
    """
    import inspect

    from scripts.serve import server as serve_server

    # The build_server seam carries identity_config (same shape as store/scaffold roots).
    params = inspect.signature(serve_server.build_server).parameters
    assert "identity_config" in params, (
        "build_server lacks the identity_config seam — the /chat call cannot thread it"
    )
    src = (REPO_ROOT / "scripts" / "serve" / "server.py").read_text()
    # The handler exposes the class-attr seam and reads it into the capture call.
    assert "identity_config = None" in src, "the handler lacks the identity_config class-attr seam"
    assert "self.identity_config" in src, (
        "the handler does not thread self.identity_config into a capture call — the "
        "instance config is not wired through the seam"
    )


# --------------------------------------------------------------------------- #
# ADR-0019-T1 — the chat-sourced rich-domain raw-source capture round-trip.
# Each new chat field writes its NAMED-EXCLUDED raw source store item (NOT the band
# token), which `summarize` then DERIVES into the coarse band/class — mirroring the
# `train-around -> raw-symptom-free-text -> active-issue-class` special-case.
# --------------------------------------------------------------------------- #

# (chat form field, named-excluded raw source, derived band token, a realistic raw value,
#  a distinctive raw fragment, the expected coarse band).
_CHAT_CAPTURE_CASES = [
    # BUG-5 (Wave-B review): "allergic" makes this `restricted` — the allergy/restriction
    # signal takes precedence over the leading plant pattern (the masked-allergy fix). The
    # value is unchanged (a realistic mixed pattern+allergy input); the band is corrected.
    ("nutrition-detail", "raw-nutrition-free-text", "dietary-pattern-class",
     "vegan, allergic to SHELLFISH-XYZ, 5 small meals", "SHELLFISH-XYZ", "restricted"),
    ("supplement-stack", "raw-supplement-free-text", "supplement-stack-class",
     "creatine 5g, whey BRAND-XYZ, omega-3", "BRAND-XYZ", "multi-supplement"),
    ("peptide-stack", "raw-peptide-free-text", "peptide-use-class",
     "BPC-157 250mcg COMPOUND-XYZ subcutaneous", "COMPOUND-XYZ", "peptide-in-use"),
    ("training-detail", "raw-training-detail-free-text", "training-volume-band",
     "PPL 6x/week, 22 SETS-XYZ per session", "SETS-XYZ", "high"),
]


import pytest


@pytest.mark.parametrize("field, raw_source, token, value, fragment, band", _CHAT_CAPTURE_CASES)
def test_chat_field_writes_raw_source_summarize_derives_band(
    field, raw_source, token, value, fragment, band, tmp_path,
):
    """ADR-0019-T1: a chat rich-domain capture -> its named-excluded raw source -> the
    derived coarse band, never the band token directly.

    Each new chat field (`nutrition-detail` / `supplement-stack` / `peptide-stack` /
    `training-detail`) writes its NAMED-EXCLUDED raw source store item (mirroring
    `train-around -> raw-symptom-free-text`), NOT the band token. `summarize` then
    DERIVES the coarse band/class from that raw source — closing the capture -> store ->
    summarize loop. The raw free-text never appears under the field-set token (AC-2).
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {field: value},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # The raw item is written under the named-excluded raw source, NOT the band token.
    assert store.read(raw_source, root=store_root), (
        f"{field!r} did not write the {raw_source!r} raw source item"
    )
    assert store.read(token, root=store_root) == [], (
        f"{field!r} wrongly wrote the {token!r} band token directly (must be derived)"
    )
    summary = _summary(store_root)
    assert summary.get(token) == band, (
        f"summarize did not derive the {token!r} band from the {raw_source!r} raw source"
    )
    # The raw free-text fragment never appears under the field-set token.
    assert fragment not in str(summary.get(token, "")), (
        f"raw fragment {fragment!r} leaked into the {token!r} token"
    )


@pytest.mark.parametrize("bad_dob", ["not-a-date", "1986", "3026-01-01", "1986-13-40"])
def test_malformed_dob_through_capture_seam_is_age_unknown(bad_dob, tmp_path):
    """OQ-5 (TEST-3): a malformed/unparseable or future-dated full DOB through the capture
    seam derives the `age-unknown` sentinel, with the raw string nowhere in the token.

    The Step-1 birth-date field writes the RAW `date-of-birth` store item; `summarize`
    de-identifies it via `_age_band` (repurposed to the exact-age deriver). A value that is
    not a parseable past ISO date must derive `age-unknown` rather than crash or echo the raw
    value. Failing-capable: an echoing deriver leaks the raw string into the token.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"date-of-birth": bad_dob},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # The raw value landed in the named-excluded raw source, never the token directly.
    assert store.read("date-of-birth", root=store_root), "the birth-date field wrote no raw source"
    assert store.read("training-age-band", root=store_root) == [], (
        "the birth-date field wrongly wrote training-age-band directly (must be derived)"
    )
    summary = _summary(store_root)
    assert summary.get("training-age-band") == "age-unknown", (
        f"a malformed DOB {bad_dob!r} did not derive the age-unknown sentinel"
    )
    # The raw malformed string appears nowhere in the emitted token.
    assert bad_dob not in str(summary.get("training-age-band", "")), (
        f"the raw DOB string {bad_dob!r} leaked into the training-age-band token"
    )


def test_bodyweight_band_de_wired_weight_routes_to_kg_series(tmp_path):
    """AC-8 (OQ-5): `bodyweight-band` is DE-WIRED; a captured weight routes to the local
    `bodyweight-kg` series, and 0 `bodyweight-band` store item is written.

    The band-consumer de-wire (bead `rod1`): `bodyweight-band` is out of `WIRED_TOKENS` +
    `_BOUNDED_ENUMS`, but the `BODYWEIGHT_BANDS` constant is RETAINED (still imported by the
    non-served legacy `intake.py`; full deletion is bead `rod1`). A captured `bodyweight-kg`
    number writes a `bodyweight-kg` reading (the named-excluded local series) via the
    UNCHANGED `store.append`; `import scripts.serve.capture` raises no AssertionError (the
    `WIRED_TOKENS <= SUMMARY_FIELD_SET` tripwire holds after the removal).
    """
    assert "bodyweight-band" not in capture.WIRED_TOKENS
    assert "bodyweight-band" not in capture._BOUNDED_ENUMS
    # The de-wire-not-delete disposition: the constant is retained (legacy intake.py importer).
    assert hasattr(capture, "BODYWEIGHT_BANDS")

    store_root = tmp_path / "store"
    capture.persist_capture(
        {"bodyweight-kg": "82.0"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # The weight number wrote the named-excluded local `bodyweight-kg` series...
    kg = store.read("bodyweight-kg", root=store_root)
    assert kg and kg[-1]["value"] == "82.0", "the weight number did not write the bodyweight-kg series"
    # ...and 0 `bodyweight-band` store item (the de-wired token is never written directly).
    assert store.read("bodyweight-band", root=store_root) == [], (
        "a bodyweight-band store item was written (the token must be derived, not stored)"
    )
    # The load-time tripwire holds after the removal (no AssertionError at import).
    importlib.reload(capture)


def test_weight_capture_round_trips_to_bodyweight_band_token(tmp_path):
    """AC-9 round-trip (cross-checks Cycle 1): a captured weight -> the local `bodyweight-kg`
    series -> `summarize` derives the current-weight+trend `bodyweight-band` token.

    Proves the capture->`bodyweight-kg`->deriver round-trip end-to-end over a tmp store.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"bodyweight-kg": "82.0"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    token = _summary(store_root).get("bodyweight-band")
    assert token is not None, "summarize did not derive bodyweight-band from the bodyweight-kg series"
    assert "82" in token, f"the current weight did not trace into the derived token: {token!r}"
    # It is the DERIVED current-weight+trend scalar, not a coarse WIRED enum band.
    assert token not in capture.BODYWEIGHT_BANDS, "bodyweight-band is a coarse WIRED band (de-wire incomplete)"


def test_full_dob_captures_to_local_date_of_birth_item(tmp_path):
    """OQ-5: a full ISO DOB captures to the named-excluded local `date-of-birth` item (pins
    the raw source survives the amendment), and 0 `training-age-band` is written directly."""
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"date-of-birth": "1986-04-12"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    dob = store.read("date-of-birth", root=store_root)
    assert dob and dob[-1]["value"] == "1986-04-12", "the full DOB did not write the date-of-birth item"
    assert store.read("training-age-band", root=store_root) == [], (
        "training-age-band was written directly (must be derived from the date-of-birth source)"
    )


def test_chat_fields_are_not_wired_tokens(tmp_path):
    """ADR-0019-T1: the band tokens are NOT WIRED_TOKENS (they are derived, not pass-through).

    The new BAND tokens are read by `summarize` from their raw source — they are NOT
    written own-name like a pass-through wired token. The `WIRED_TOKENS <= SUMMARY_FIELD_SET`
    tripwire stays green because WIRED_TOKENS is unchanged. Asserts the four band tokens are
    absent from WIRED_TOKENS and the four raw sources are not field-set tokens.
    """
    for _field, raw_source, token, _v, _f, _b in _CHAT_CAPTURE_CASES:
        assert token not in capture.WIRED_TOKENS, token
        assert raw_source not in SUMMARY_FIELD_SET, raw_source


# --------------------------------------------------------------------------- #
# ADR-0033-0035-T1 — the comprehensive intake field->destination contract.
# T1 PINS the 9-step contract over the EXISTING capture routing (ADR-0014/0018/0019):
# the four rich-domain fields carry REAL signal (not the absent-source default), the
# OQ-1 select VALUE resolves to its deriver bucket, raw meds + sensitive fields route
# record-only, and an edited re-capture re-runs the SAME raw-source path. The routing
# pre-exists; each test pins it, failing-capable by its named mutation.
# --------------------------------------------------------------------------- #

# (field, bucket-keyword value, derived token, the deriver's no-signal default, expected).
_T1_REAL_SIGNAL_CASES = [
    ("nutrition-detail", "vegan", "dietary-pattern-class", "general-diet", "plant-based"),
    ("supplement-stack", "creatine, whey", "supplement-stack-class", "none", "multi-supplement"),
    ("peptide-stack", "BPC-157", "peptide-use-class", "none", "peptide-in-use"),
    ("training-detail", "5 days/week", "training-volume-band", "moderate", "high"),
]


@pytest.mark.parametrize("field, value, token, no_signal_default, expected", _T1_REAL_SIGNAL_CASES)
def test_rich_domain_field_carries_real_signal_vs_not_discussed_default(
    field, value, token, no_signal_default, expected, tmp_path,
):
    """AC-1: a rich-domain capture lands REAL signal; a fresh store reads not-discussed.

    A fresh store (no capture) reads the `not-discussed` absent-source sentinel for the
    always-set token; after a bucket-keyword capture the token derives its real bucket
    (not `not-discussed`, not the deriver's no-signal default) — the real-signal contrast
    the existing round-trip test omits.

    Failing-capable: drop the field's key from `capture._CHAT_RAW_SOURCE_FIELDS` and it
    routes record-only, the token stays `not-discussed`, reddening the non-default assert.
    """
    store_root = tmp_path / "store"
    # The real-signal CONTRAST: a fresh store reads the absent-source sentinel.
    assert _summary(store_root).get(token) == "not-discussed", (
        f"a fresh store did not read {token!r} as the not-discussed sentinel"
    )
    capture.persist_capture(
        {field: value},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    derived = _summary(store_root).get(token)
    assert derived == expected, (
        f"{field!r}={value!r} derived {derived!r}, not the expected {expected!r}"
    )
    assert derived not in ("not-discussed", no_signal_default), (
        f"{token!r} carried the no-signal value {derived!r}, not real signal"
    )


# (field, submitted select VALUE, derived token, expected bucket) — the OQ-1 pin. The
# select OPTION VALUE (not the display text) carries the deriver keyword; the
# `"5 days/week"`->high row encodes the crux that a "5 or more days" display must submit
# a digit-adjacent-unit VALUE (a `"5 or more days"` literal derives `moderate`, not high).
_T1_OQ1_VALUE_BUCKET_CASES = [
    ("nutrition-detail", "vegan", "dietary-pattern-class", "plant-based"),
    ("nutrition-detail", "keto", "dietary-pattern-class", "restricted"),
    ("training-detail", "5 days/week", "training-volume-band", "high"),
    ("training-detail", "2x", "training-volume-band", "low"),
    ("supplement-stack", "none", "supplement-stack-class", "none"),
    ("supplement-stack", "creatine, whey", "supplement-stack-class", "multi-supplement"),
    ("peptide-stack", "none", "peptide-use-class", "none"),
    ("peptide-stack", "BPC-157", "peptide-use-class", "peptide-in-use"),
]


@pytest.mark.parametrize("field, value, token, expected_bucket", _T1_OQ1_VALUE_BUCKET_CASES)
def test_oq1_select_value_resolves_to_expected_deriver_bucket(
    field, value, token, expected_bucket, tmp_path,
):
    """AC-2 (OQ-1): a bounded select VALUE resolves to its expected deriver bucket.

    The pinned T1<->T4 format coupling: the select OPTION VALUE carries a deriver-matching
    keyword through `persist_capture`->`summarize`. Each row's bucket is real signal (a
    determinate class, never the `not-discussed` absent-source sentinel).

    Failing-capable: a deriver-keyword change or a `_RAW_TO_FIELD` repoint reds the row.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {field: value},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    derived = _summary(store_root).get(token)
    assert derived == expected_bucket, (
        f"{field!r}={value!r} resolved to {derived!r}, not the expected {expected_bucket!r}"
    )
    assert derived != "not-discussed", (
        f"{token!r} read the absent-source default, not the submitted select value"
    )


def test_comprehensive_capture_records_raw_meds_zero_rx_class_writes(tmp_path):
    """AC-3: a comprehensive 9-step submission records raw meds, writes 0 rx-class tokens.

    The crown-jewel negative at comprehensive-roster scale: a full submission (goals +
    demographics + the four rich-domain fields + a raw `rx-interaction-classes` med field)
    writes 0 `rx-interaction-classes` store items; the raw drug name lands record-only in
    the gitignored scaffold and in NO field-set item, while the rich-domain tokens still
    derive real signal.

    Failing-capable: re-add `rx-interaction-classes` to `capture.WIRED_TOKENS` and the raw
    drug name reaches the model-bound store item, reddening the empty-read assert.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    fields = {
        "goal-domains": "Workout;Nutrition",
        "recovery-status-band": "moderate",
        "sex-for-dosing": "male",
        "bodyweight-kg": "82.0",
        "equipment-access-class": "full-home-gym",
        "nutrition-detail": "vegan",
        "supplement-stack": "creatine, whey",
        "peptide-stack": "BPC-157",
        "training-detail": "5 days/week",
        "rx-interaction-classes": "warfarin 5mg; metformin 500mg",
    }
    capture.persist_capture(
        fields, root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Crown jewel: 0 rx-interaction-classes store writes from persist_capture.
    assert store.read("rx-interaction-classes", root=store_root) == [], (
        "the rx form field wrote the model-bound store item (must route record-only)"
    )
    # The raw drug name landed in the gitignored scaffold receipt.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "warfarin" in scaffold_text, "the raw med field did not land in the gitignored scaffold"
    # Negative (load-bearing): the drug name is in NO field-set store item.
    for token in SUMMARY_FIELD_SET:
        for reading in store.read(token, root=store_root):
            assert "warfarin" not in str(reading["value"]), (
                f"a raw drug name reached the {token!r} field-set store item"
            )
    # Real signal coexists with record-only meds: the four rich-domain tokens derive non-default.
    summary = _summary(store_root)
    assert summary.get("dietary-pattern-class") == "plant-based"
    assert summary.get("supplement-stack-class") == "multi-supplement"
    assert summary.get("peptide-use-class") == "peptide-in-use"
    assert summary.get("training-volume-band") == "high"


def test_sensitive_fields_route_record_only_no_cannabis(tmp_path):
    """AC-4: race/occupation/sleep/stress/smoker/alcohol record-only; NO cannabis routing.

    Each sensitive field routes to the gitignored scaffold receipt and writes 0 field-set
    store tokens. A probe `cannabis` field lands record-only like any unrecognized field —
    the contract carries NO cannabis-specific routing key/token in `capture.py`.

    Failing-capable: wire any sensitive field into `capture.WIRED_TOKENS` and its value
    reaches a field-set store item, reddening the 0-store-token assertion.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    sensitive = {
        "race": "RACE-XYZ",
        "ethnicity": "ETHNICITY-XYZ",
        "occupation": "OCCUPATION-XYZ",
        "sleep": "SLEEP-XYZ 6 hours",
        "stress": "STRESS-XYZ high",
        "smoker": "SMOKER-XYZ never",
        "alcohol": "ALCOHOL-XYZ weekly",
        "cannabis": "CANNABIS-XYZ probe",
    }
    receipt = capture.persist_capture(
        sensitive, root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Each sensitive (and the probe) field name is recorded in the scaffold receipt.
    for name in sensitive:
        assert name in receipt["scaffold"], f"{name!r} did not route record-only to the scaffold"
    # Negative (load-bearing): no sensitive value reaches ANY field-set store item.
    markers = ("RACE-XYZ", "ETHNICITY-XYZ", "OCCUPATION-XYZ", "SLEEP-XYZ", "STRESS-XYZ",
               "SMOKER-XYZ", "ALCOHOL-XYZ", "CANNABIS-XYZ")
    for token in SUMMARY_FIELD_SET:
        for reading in store.read(token, root=store_root):
            v = str(reading["value"])
            for marker in markers:
                assert marker not in v, f"a sensitive value {marker!r} leaked into {token!r}"
    # Negative (the no-cannabis contract): no cannabis-specific routing key/token exists.
    assert "cannabis" not in capture.WIRED_TOKENS
    assert "cannabis" not in capture._CHAT_RAW_SOURCE_FIELDS
    assert "cannabis" not in capture._BOUNDED_ENUMS
    capture_src = (REPO_ROOT / "scripts" / "serve" / "capture.py").read_text().lower()
    assert "cannabis" not in capture_src, "a cannabis-specific key/token entered capture.py"


def test_editable_re_capture_re_runs_same_path_no_direct_band_write(tmp_path):
    """AC-5: an edited re-capture re-runs the raw-source path; the band is never written direct.

    An edited rich-domain field re-submitted through `persist_capture` re-routes through its
    raw-source item (append-only), `summarize` re-derives from the latest reading, and the
    band token is never written directly (0 new write surface).

    Failing-capable: a direct-band-write path would land a `dietary-pattern-class` store
    item, reddening the 0-direct-write assertion.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {"nutrition-detail": "omnivore"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    capture.persist_capture(
        {"nutrition-detail": "vegan"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Both readings landed in the raw source (append-only), edited value last.
    readings = store.read("raw-nutrition-free-text", root=store_root)
    assert len(readings) == 2, f"re-capture did not append (got {len(readings)} readings)"
    assert readings[-1]["value"] == "vegan", "the edited re-capture is not the latest reading"
    # summarize re-derives from the latest (edited) reading.
    assert _summary(store_root).get("dietary-pattern-class") == "plant-based", (
        "summarize did not re-derive from the edited latest reading"
    )
    # The band token is NEVER written directly (0 new write surface).
    assert store.read("dietary-pattern-class", root=store_root) == [], (
        "the band token was written directly (must be derived, not stored)"
    )


# --------------------------------------------------------------------------- #
# ADR-0033-0035-T3 — Cycle 1: the safety-signal routing region. Each of the three
# safety screens (exercise-safety / PHQ-2 / apnea) writes a `safety-screen::<screen>`
# answered marker REGARDLESS of the answer (the gate's presence signal) + a
# `referral::<screen>` flag on a POSITIVE answer ONLY (the safety-bypass falsification);
# food/drug allergies route to the existing `hard-limits` token, never
# `rx-interaction-classes`. All fixture-driven over a tmp store root; 0 live spend.
# --------------------------------------------------------------------------- #

# (form field name, screen name, a POSITIVE answer value, a NEGATIVE answer value). The
# field/answer values are the pinned T3<->T4 contract; a POSITIVE answer raises the
# referral flag, a NEGATIVE writes only the answered marker.
_SAFETY_SCREEN_CASES = [
    ("exercise-safety", "exercise-safety", "chest-pain", "none"),
    ("phq2", "phq2", "nearly-every-day", "not-at-all"),
    ("apnea", "apnea", "yes", "no"),
]


@pytest.mark.parametrize("field, screen, positive, negative", _SAFETY_SCREEN_CASES)
def test_safety_screens_write_answered_markers(field, screen, positive, negative, tmp_path):
    """AC-1: each safety screen writes its `safety-screen::<screen>` answered marker
    REGARDLESS of the answer value (the gate's presence signal).

    Failing-capable: with the safety region absent the field falls to the record-only
    `else`, no marker is written, and `store.read(<marker>)` is empty.
    """
    for value in (positive, negative):
        store_root = tmp_path / f"store-{screen}-{value}"
        capture.persist_capture(
            {field: value}, root=store_root, scaffold_root=tmp_path / "scaffold",
            identity_config=_ABSENT_IDENTITY,
        )
        assert store.read(f"safety-screen::{screen}", root=store_root), (
            f"{field!r}={value!r} did not write the safety-screen::{screen} answered marker"
        )


@pytest.mark.parametrize("field, screen, positive, negative", _SAFETY_SCREEN_CASES)
def test_positive_safety_answer_writes_referral_flag(field, screen, positive, negative, tmp_path):
    """AC-2 positive: a POSITIVE safety answer writes a `referral::<screen>` flag.

    Failing-capable: a no-op route (never writes the flag) reds this positive case.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {field: positive}, root=store_root, scaffold_root=tmp_path / "scaffold",
        identity_config=_ABSENT_IDENTITY,
    )
    assert store.read(f"referral::{screen}", root=store_root), (
        f"a positive {field!r} answer did not write the referral::{screen} flag"
    )


@pytest.mark.parametrize("field, screen, positive, negative", _SAFETY_SCREEN_CASES)
def test_negative_safety_answer_writes_no_referral_flag(field, screen, positive, negative, tmp_path):
    """AC-2 negative: a NEGATIVE safety answer writes NO referral flag (only the marker).

    Failing-capable: an always-write route reds this negative case — the flag trips ONLY
    on a positive answer.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {field: negative}, root=store_root, scaffold_root=tmp_path / "scaffold",
        identity_config=_ABSENT_IDENTITY,
    )
    assert store.read(f"referral::{screen}", root=store_root) == [], (
        f"a negative {field!r} answer wrongly wrote the referral::{screen} flag"
    )
    # The answered marker IS still written (the presence signal, regardless of answer).
    assert store.read(f"safety-screen::{screen}", root=store_root), (
        f"a negative {field!r} answer did not write the safety-screen::{screen} marker"
    )


def test_safety_marker_value_is_deidentified_not_raw_answer(tmp_path):
    """AC-1/crown-jewel: the marker stores a de-identified positivity signal, never the
    raw free-text answer (no raw PHQ-2/symptom text reaches a `safety-screen::*` item).

    Failing-capable: a route echoing the raw answer into the marker leaks the raw token.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "chest-pain-climbing-stairs-XYZ"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    marker = store.read("safety-screen::exercise-safety", root=store_root)
    assert marker and marker[-1]["value"] in ("positive", "negative"), (
        "the safety marker did not store a de-identified positivity signal"
    )
    assert "XYZ" not in str(marker[-1]["value"]), "the raw answer leaked into the marker value"


def _rendered_allergy_field_names():
    """Extract the allergy input `name=`s from the ACTUAL rendered wizard markup.

    Grounds the capture contract against the served design (`app_shell.render`) rather than
    hard-coded field names — a future markup rename (e.g. back to `drug-allergies`) reds the
    placement assertion below, catching the capture<->form contract break at its source.
    """
    import re

    from vault.design.templates import app_shell

    html = app_shell.render()
    return re.findall(
        r"<label>[^<]*[Aa]llerg[^<]*</label>\s*<input[^>]*\bname=['\"]([^'\"]+)['\"]", html,
    )


def test_allergies_route_to_hard_limits(tmp_path):
    """AC-4: the rendered allergy fields route to the existing `hard-limits` token.

    De-tautologized (Tier-3 FIX-1): asserts PLACEMENT against the ACTUAL rendered wizard
    field names — every allergy input the served markup emits must be a `_ALLERGY_FIELDS`
    member (else the capture branch never sees it and the value silently falls record-only,
    the drug-allergy hard-contraindication never reaching the planner). Then round-trips
    those SAME field names through the capture seam into `hard-limits`.

    Failing-capable: rename an allergy input in the markup (or drop a field name from
    `_ALLERGY_FIELDS`) and the membership assertion reds; with the allergy region absent
    the round-trip fields fall to record-only and `hard-limits` carries neither value.
    """
    rendered = _rendered_allergy_field_names()
    assert rendered, "no allergy inputs found in the rendered wizard markup"
    for name in rendered:
        assert name in capture._ALLERGY_FIELDS, (
            f"the rendered allergy input {name!r} is not a _ALLERGY_FIELDS member — the "
            f"capture<->form contract is broken (it would fall record-only, never hard-limits)"
        )
    # Both allergy classes are wired (a rename that dropped one would shrink this set).
    assert set(rendered) == set(capture._ALLERGY_FIELDS), (
        f"rendered allergy fields {sorted(rendered)} != _ALLERGY_FIELDS "
        f"{sorted(capture._ALLERGY_FIELDS)}"
    )

    store_root = tmp_path / "store"
    capture.persist_capture(
        {"food-allergy": "shellfish", "drug-allergy": "penicillin"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    values = " ".join(str(r["value"]) for r in store.read("hard-limits", root=store_root))
    assert "shellfish" in values, "the food allergy did not route to hard-limits"
    assert "penicillin" in values, "the drug allergy did not route to hard-limits"


def test_pii_bearing_allergy_value_diverts_record_only(tmp_path):
    """FIX-1 (Security): a PII-bearing allergy value diverts record-only, never `hard-limits`.

    The allergy branch writes the model-bound `hard-limits` token, but — unlike every sibling
    free-text token — it was UNSCANNED. An allergy value carrying operator contact PII (an
    email) must be caught by the SAME uncapped `_value_has_pii` gate and routed record-only
    to the gitignored scaffold, never reaching the model-bound `hard-limits` token.

    Failing-capable: drop the `_value_has_pii` check in the allergy branch and the email
    lands in the `hard-limits` store item, reddening the empty-read assertion.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {"drug-allergy": "penicillin — reaction notes, reach me at operator@example.com"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    # Negative (load-bearing): the PII-bearing allergy never reached the model-bound token.
    assert store.read("hard-limits", root=store_root) == [], (
        "a PII-bearing allergy value reached the model-bound hard-limits token"
    )
    # Positive: it landed record-only in the gitignored scaffold instead.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "operator@example.com" in scaffold_text, "the PII allergy value did not route record-only"

    # The gate is selective: a clean allergy value still lands in hard-limits.
    capture.persist_capture(
        {"food-allergy": "shellfish"},
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    hl = " ".join(str(r["value"]) for r in store.read("hard-limits", root=store_root))
    assert "shellfish" in hl, "a clean allergy value did not land in hard-limits"


def test_drug_allergy_not_in_rx_interaction_classes(tmp_path):
    """AC-4: a drug allergy never routes into the liaison-curated `rx-interaction-classes`.

    A drug allergy is a hard contraindication (-> `hard-limits`), not a drug-interaction
    class. Failing-capable: a mis-route into `rx-interaction-classes` reds the empty read.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"drug-allergy": "penicillin"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("rx-interaction-classes", root=store_root) == [], (
        "a drug allergy wrongly routed into the model-bound rx-interaction-classes token"
    )
    # It DID land in hard-limits (the pinned route).
    values = " ".join(str(r["value"]) for r in store.read("hard-limits", root=store_root))
    assert "penicillin" in values, "the drug allergy did not route to hard-limits"


def test_positive_exercise_safety_records_contraindication_marker_and_referral(tmp_path):
    """AC-5: a POSITIVE exercise-safety answer records BOTH the
    `safety-screen::exercise-safety` contraindication marker (recorded so the deferred
    clinician-clearance-grant path can gate on it) AND the `referral::exercise-safety` flag.

    Failing-capable: no marker / no flag reds each assertion.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "chest-pain"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    marker = store.read("safety-screen::exercise-safety", root=store_root)
    assert marker and marker[-1]["value"] == "positive", (
        "the exercise-safety contraindication marker was not recorded"
    )
    assert store.read("referral::exercise-safety", root=store_root), (
        "the exercise-safety referral flag was not written on a positive answer"
    )


# --- ADR-0033-0035-T3 STORE-ADVERSARIAL battery (pka, docs/checklists/store-adversarial-tests.md).
# The safety-marker / referral-flag / hard-limits writes land in scripts/store/ via the
# UNCHANGED store.append, so the four required categories apply to T3's new streams. ---


def test_safety_streams_do_not_cross_read(tmp_path):
    """STORE-ADVERSARIAL #1 (cross-stream namespace isolation): a read for one safety
    marker / referral flag / hard-limits never returns another stream's value.

    A positive exercise-safety + negative phq2/apnea + a food allergy captured together:
    the exercise-safety flag is present, phq2/apnea flags are absent, and the allergy is
    in `hard-limits` and in NO safety-screen/referral stream (the S41 fabricated-cross-read
    pattern). Failing-capable: a shared bare item name would cross-read.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "chest-pain", "phq2": "not-at-all", "apnea": "no",
         "food-allergy": "shellfish"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("referral::exercise-safety", root=store_root), "positive es did not flag"
    assert store.read("referral::phq2", root=store_root) == [], "negative phq2 wrongly flagged"
    assert store.read("referral::apnea", root=store_root) == [], "negative apnea wrongly flagged"
    hard_limits = " ".join(str(r["value"]) for r in store.read("hard-limits", root=store_root))
    assert "shellfish" in hard_limits, "the allergy did not land in hard-limits"
    for stream in ("safety-screen::exercise-safety", "referral::exercise-safety",
                   "safety-screen::phq2", "safety-screen::apnea"):
        vals = " ".join(str(r["value"]) for r in store.read(stream, root=store_root))
        assert "shellfish" not in vals, f"the allergy cross-contaminated {stream!r}"


def test_safety_marker_same_timepoint_dedupe_and_distinct_screens_both_persist(tmp_path):
    """STORE-ADVERSARIAL #2/#3 (same-key dedupe boundary / distinct-stream no-drop): a
    second write at an existing `(item, timepoint, source)` is dropped (value excluded from
    the dedupe key), but two DISTINCT screen markers sharing a timepoint BOTH persist — the
    exact S41 same-timepoint contraindication-drop this checklist exists to prevent.

    Failing-capable: widen the dedupe key to include `value` and the same-key re-write
    persists (len == 2); drop the `::`-namespaced item distinctness and the distinct-screen
    marker is clobbered.
    """
    import datetime

    store_root = tmp_path / "store"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Same item + timepoint + source, DIFFERENT value -> second dropped (dedupe excludes value).
    store.append("safety-screen::apnea",
                 {"item": "safety-screen::apnea", "timepoint": ts, "source": "intake", "value": "negative"},
                 root=store_root)
    store.append("safety-screen::apnea",
                 {"item": "safety-screen::apnea", "timepoint": ts, "source": "intake", "value": "positive"},
                 root=store_root)
    apnea = store.read("safety-screen::apnea", root=store_root)
    assert len(apnea) == 1, "a same-key re-write was not deduped (dedupe key must exclude value)"
    assert apnea[0]["value"] == "negative", "the dedupe dropped the FIRST write, not the second"
    # A DISTINCT screen marker at the SAME timepoint -> BOTH persist (distinct `::` items).
    store.append("safety-screen::exercise-safety",
                 {"item": "safety-screen::exercise-safety", "timepoint": ts, "source": "intake", "value": "positive"},
                 root=store_root)
    assert store.read("safety-screen::exercise-safety", root=store_root), (
        "a distinct screen marker sharing a timepoint was dropped (the S41 contraindication-drop)"
    )
    assert store.read("safety-screen::apnea", root=store_root), "the apnea marker was clobbered"


def test_safety_markers_use_namespaced_prefix_not_bare_names(tmp_path):
    """STORE-ADVERSARIAL #4 (mutation / cross-stream namespacing): the markers write under
    the `safety-screen::` / `referral::` namespace, never a bare token that could collide
    with a field-set stream.

    Failing-capable (mutation): drop the `safety-screen::`/`referral::` prefix and a bare
    un-namespaced item is written, reddening the bare-read + prefix assertions.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "chest-pain"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    assert store.read("safety-screen::exercise-safety", root=store_root)
    assert store.read("referral::exercise-safety", root=store_root)
    # No bare un-namespaced safety item was written (the prefix keeps them field-set-disjoint).
    assert store.read("exercise-safety", root=store_root) == [], (
        "a bare un-namespaced safety item was written (the :: namespace prevents collision)"
    )
    for item in store.items(root=store_root):
        assert item.startswith("safety-screen::") or item.startswith("referral::"), (
            f"a non-namespaced safety item {item!r} was written"
        )


# --------------------------------------------------------------------------- #
# ADR-0033-0035-T3 — Cycle 2: the crown-jewel never-a-plan-input probe. No
# `safety-screen::*` / `referral::*` marker is a SUMMARY_FIELD_SET member, so summarize
# never reads them AND dispatch's whitelist rejects one injected into a payload. By guard
# EXECUTION over the FROZEN summarize/dispatch, not a substring grep.
# --------------------------------------------------------------------------- #


def test_safety_markers_absent_from_summarize(tmp_path):
    """AC-3 crown-jewel: no `safety-screen::*` / `referral::*` key appears in `summarize`
    output — the markers are not SUMMARY_FIELD_SET members, so summarize's
    `for field in SUMMARY_FIELD_SET` loop structurally never reads them.

    RED-capable: reds if a marker were ever made a SUMMARY_FIELD_SET member (a future
    field-set regression).
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"exercise-safety": "chest-pain", "phq2": "nearly-every-day", "apnea": "yes"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # The markers + a flag ARE in the store (the probe is over real capture output)...
    assert store.read("safety-screen::exercise-safety", root=store_root)
    assert store.read("referral::exercise-safety", root=store_root)
    # ...but NONE reaches the plan summary.
    summary = _summary(store_root)
    leaked = [k for k in summary if k.startswith("safety-screen::") or k.startswith("referral::")]
    assert not leaked, f"a safety marker reached the plan summary: {leaked}"


def test_dispatch_rejects_injected_safety_screen_field():
    """AC-3 crown-jewel: `dispatch` RAISES the out-of-field-set ValueError on a payload
    carrying an injected `safety-screen::*` field (the whitelist rejects the complement).

    RED-capable: reds if the marker were whitelisted into SUMMARY_FIELD_SET.
    """
    complete = {field: "" for field in SUMMARY_FIELD_SET}
    dispatch(complete)  # negative control: a complete valid summary does NOT raise
    injected = dict(complete)
    injected["safety-screen::exercise-safety"] = "positive"
    with pytest.raises(ValueError, match="out-of-field-set"):
        dispatch(injected)


def test_training_experience_routes_raw_local_band_crosses(tmp_path):
    """The wizard training-experience number writes the RAW local source, never the band token.

    Crown-jewel (NFR-1): the operator's exact years land under the named-excluded
    `raw-training-experience` local item (shown in My-Info); the coarse `training-experience-band`
    the planner reads is DERIVED by `summarize`, never written by capture directly. Failing-capable:
    if capture wrote the band token directly, the `== []` band-absent assertion reds.
    """
    import functools

    from scripts.plan import router
    from scripts.serve import capture
    from scripts.store import store

    receipt = capture.persist_capture({"training-experience": "25"}, root=tmp_path,
                                       scaffold_root=tmp_path / "sc")
    # the raw source landed local; the band token was NOT written directly
    assert [r["value"] for r in store.read("raw-training-experience", root=tmp_path)] == ["25"]
    assert store.read("training-experience-band", root=tmp_path) == [], "capture wrote the band token directly (crown-jewel breach)"
    assert "raw-training-experience" in receipt["store"]
    # only the DERIVED band crosses; the raw number never enters the summary
    summary = router.summarize(functools.partial(store.read, root=tmp_path))
    assert summary["training-experience-band"] == "veteran"
    assert "25" not in str(summary.get("training-experience-band")), "the exact number leaked into the crossing token"
    # the raw source is named-excluded (the dispatch whitelist would reject it)
    assert "raw-training-experience" in router.EXCLUDED_RAW_PII
    assert "raw-training-experience" not in router.SUMMARY_FIELD_SET
