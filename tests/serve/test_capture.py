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
import subprocess
import sys
from pathlib import Path

from scripts.guard import pii_scan
from scripts.plan.router import SUMMARY_FIELD_SET, summarize
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
    ("nutrition-detail", "raw-nutrition-free-text", "dietary-pattern-class",
     "vegan, allergic to SHELLFISH-XYZ, 5 small meals", "SHELLFISH-XYZ", "plant-based"),
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
