"""Care-agent review-on-final-save + de-associated meds curation (ADR-0033-0035-T8).

The crown-jewel BOTH-legs egress unit coverage for `scripts/serve/care_review.py`:

- Leg 1 (clarifying review): `care_review.review` builds the DE-IDENTIFIED `router.summarize`
  profile and makes ONE `client.converse` call carrying ONLY that de-id profile — 0 full-DOB,
  0 raw drug string, 0 legal name.
- Leg 2 (meds curation): a DISTINCT, meds-only `converse` request built OUTSIDE
  `chat._model_messages`, carrying drug NAMES but 0 operator-identity token + 0 name<->med
  linkage, proposing the de-identified `rx-interaction-classes` CLASS token.

Every crown-jewel probe is a `pii_scan.scan_text_full` EXECUTION over the RECORDED request
(count 0 on the real request, > 0 on the injected-identity negative control), never a substring
grep alone — the QA-F3 W6 negative controls prove the both-legs green is non-vacuous.

Confirm-when-unsure (0 unconfirmed `rx-interaction-classes` writes), the no-key honest 0-spend
degrade, and 0 raw drug string as a planner token / in the `dispatch` payload are asserted here.

Every test injects a RECORDING mock backend at the ADR-0015 `ModelClient(backend=...)` seam and
runs `pii_scan` over in-memory request strings + a tmp store/scaffold root — 0 live `converse`
call, 0 curation call, 0 key, 0 network, 0 `key_source.resolve()`-gated call.

DEFERRED (NOT asserted here): the operator-present LIVE care-agent run — a real no-train key +
real spend, end-to-end through final-save -> de-id review -> questions-in-thread + meds
curation — is ADR-0035 OQ-1, operator-gated. This suite is the mock/fixture floor beneath it.
"""

import functools
import json
from pathlib import Path

import pytest

from scripts.model.client import ModelCallError, ModelClient
from scripts.plan import router
from scripts.guard import pii_scan
from scripts.serve import capture
from scripts.serve import care_review
from scripts.store import store

# A fake operator legal name — NEVER a real one. Written into a gitignored-shape one-regex-per-
# line token config so the W6 identity-injection negative control REDS deterministically in CI
# (where `vault/meta/operator-identity.txt` is ABSENT). None of the seeded profile values carry
# it, so the real-request leg-1/leg-2 probes read 0.
_FAKE_LEGAL_NAME = "Marlowe Fenwick"

# The conditionally-set store items that make `router.summarize` produce EVERY SUMMARY_FIELD_SET
# field (so `dispatch` does not raise partial). None carries operator PII (no fake name, no
# email/phone/postal), so the clarifying-request leg-1 probe reads 0.
_FULL_STORE = {
    "date-of-birth": "1986-04-12",
    "bodyweight-kg": "82",
    "sex-for-dosing": "male",
    "equipment-access-class": "full-home-gym",
    "goal-domains": "Workout;Nutrition",
    "goal-targets": "build strength and improve sleep",
    "goal-priority-order": "recovery then strength",
    "recovery-status-band": "moderate",
    "raw-symptom-free-text": "occasional knee soreness",
    "hard-limits": "no overhead pressing",
    "safety-screen::exercise-safety": "negative",
    "safety-screen::phq2": "negative",
    "safety-screen::apnea": "negative",
}


class _CareBackend:
    """A recording converse backend: records each request, scripts a per-leg reply.

    Records every `converse(messages)` payload into `self.calls` (the crown-jewel probe reads
    what the model call CARRIED). Distinguishes the two legs by request CONTENT (the care_review
    task marker), so the assertions stay order-independent: a `rx-interaction-curation` request
    gets a scripted class proposal (confident by default; `confident=False` drives the uncertain
    path), any other request gets a clarifying question.
    """

    def __init__(self, *, question="What is your top training priority this cycle?",
                 rx_class="cyp3a4-pgp", confident=True):
        self.question = question
        self.rx_class = rx_class
        self.confident = confident
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        if "rx-interaction-curation" in json.dumps(messages):
            return {"reply": "Please confirm these interaction classes.",
                    "extraction": [{"rx-interaction-class": self.rx_class,
                                    "confident": self.confident}]}
        return {"reply": self.question, "extraction": []}


def _identity_config(tmp_path):
    """Write a gitignored-shape one-regex-per-line identity token config (the fake legal name)."""
    path = tmp_path / "operator-identity.txt"
    path.write_text(_FAKE_LEGAL_NAME + "\n")
    return path


def _seed_full(store_root):
    """Seed the store so `summarize` produces every SUMMARY_FIELD_SET field (dispatch-complete)."""
    for item, value in _FULL_STORE.items():
        store.append(item, {"item": item, "timepoint": "2026-06-01T00:00:00+00:00",
                            "source": "intake", "value": value}, root=store_root)


def _reader(store_root):
    """The instance-root-bound `store.read` partial `summarize`'s caller contract requires."""
    return functools.partial(store.read, root=store_root)


def _seed_scaffold_med(store_root, scaffold_root, value="atorvastatin 20mg"):
    """Route a raw med through T1's record-only capture so the curation has a drug to de-associate."""
    capture.persist_capture({"rx-interaction-classes": value},
                            root=store_root, scaffold_root=scaffold_root)


# --------------------------------------------------------------------------- #
# Cycle 1 — the clarifying-review leg + the crown-jewel leg-1 probe + the QA-F3
#   W6 negative control + the no-key honest degrade (AC-1, AC-2 leg-1, AC-5)
# --------------------------------------------------------------------------- #


def test_review_fires_and_produces_clarifying_question(tmp_path):
    """AC-1: a keyed review over a complete profile makes EXACTLY ONE clarifying converse + >= 1 Q."""
    store_root = tmp_path / "store"
    _seed_full(store_root)
    backend = _CareBackend()
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=tmp_path / "scaffold",
        identity_config=_identity_config(tmp_path),
    )
    assert result["deferred"] is False, "a keyed complete-profile review must not defer"
    assert len(result["questions"]) >= 1, "the review produced no clarifying question"
    assert len(backend.calls) == 1, (
        f"expected EXACTLY ONE clarifying converse (no scaffold med), got {len(backend.calls)}"
    )


def test_clarifying_request_carries_only_deid_profile(tmp_path):
    """AC-2 leg 1: the clarifying converse carries ONLY the de-id summarize profile — 0 identity."""
    store_root = tmp_path / "store"
    _seed_full(store_root)
    idcfg = _identity_config(tmp_path)
    backend = _CareBackend()
    care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=idcfg,
    )
    request_text = json.dumps(backend.calls[0])
    assert pii_scan.scan_text_full(request_text, token_config=idcfg) == 0, (
        "the clarifying converse request carried operator PII (crown-jewel leg-1 breach)"
    )
    # A seeded-substring scan for the load-bearing raw classes (belt-and-braces over the pii_scan
    # execution): no legal name, no full DOB, no raw drug string in the de-id profile request.
    assert _FAKE_LEGAL_NAME not in request_text, "a legal name crossed into the clarifying request"
    assert "1986-04-12" not in request_text, "a full DOB crossed into the clarifying request"
    assert "atorvastatin" not in request_text, "a raw drug string crossed into the clarifying request"


def test_injected_identity_reds_the_clarifying_probe(tmp_path):
    """AC-2 W6 negative control (leg 1): an injected identity token REDS the clarifying probe."""
    store_root = tmp_path / "store"
    _seed_full(store_root)
    idcfg = _identity_config(tmp_path)
    summary = router.summarize(_reader(store_root), identity_config=idcfg)
    poisoned = dict(summary)
    poisoned["goal-targets"] = f"{_FAKE_LEGAL_NAME} wants to add 20kg to the squat"
    request_text = json.dumps(care_review._clarifying_messages(poisoned))
    assert pii_scan.scan_text_full(request_text, token_config=idcfg) > 0, (
        "the leg-1 probe could not count an injected identity token — it is vacuous"
    )


def test_no_key_degrades_honestly_zero_spend(tmp_path):
    """AC-5: a keyless review makes 0 model calls and returns an HONEST deferred state."""
    store_root = tmp_path / "store"
    _seed_full(store_root)
    backend = _CareBackend()
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=False,
        store_root=store_root, scaffold_root=tmp_path / "scaffold",
        identity_config=_identity_config(tmp_path),
    )
    assert backend.calls == [], "a keyless review made a model call (0-spend breach)"
    assert result["deferred"] is True and result.get("reason"), "the keyless degrade is not honest"
    assert result["questions"] == [], "the keyless degrade fabricated a question"


# --------------------------------------------------------------------------- #
# Cycle 2 — the distinct de-associated meds-curation request + the crown-jewel
#   leg-2 probe + confirm-when-unsure (AC-2 leg-2, AC-3, AC-4)
# --------------------------------------------------------------------------- #


def test_meds_curation_is_a_distinct_request_outside_model_messages(tmp_path):
    """AC-3: the curation is a SEPARATE request built OUTSIDE chat._model_messages."""
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _seed_scaffold_med(store_root, scaffold_root)
    backend = _CareBackend()
    care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=_identity_config(tmp_path),
    )
    curation_calls = [c for c in backend.calls if "rx-interaction-curation" in json.dumps(c)]
    assert len(curation_calls) == 1, "the curation is not a single distinct meds-only request"
    curation_text = json.dumps(curation_calls[0])
    # NOT a `_model_messages` output: it carries the drug-name curation content, never the
    # `_deidentified_view` token/domain-names JSON (target_domain / missing_fields keys).
    assert "target_domain" not in curation_text and "missing_fields" not in curation_text, (
        "the curation request has the `_model_messages` `_deidentified_view` shape"
    )
    assert "atorvastatin" in curation_text, "the curation request carries no drug name"
    # Source assert: care_review never CALLS the chat intake-turn builder nor imports chat (a
    # prose docstring reference to the name is fine — the breach is a call / an import).
    src = (Path(care_review.__file__)).read_text()
    assert "_model_messages(" not in src, "care_review calls chat._model_messages for the curation"
    assert "serve.chat" not in src and "serve import chat" not in src, "care_review imports chat"


def test_curation_request_carries_drug_names_zero_identity(tmp_path):
    """AC-2 leg 2: the curation carries drug NAMES but 0 operator-identity + 0 name<->med linkage."""
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _seed_scaffold_med(store_root, scaffold_root)
    idcfg = _identity_config(tmp_path)
    backend = _CareBackend()
    care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=idcfg,
    )
    curation_text = json.dumps(
        [c for c in backend.calls if "rx-interaction-curation" in json.dumps(c)][0]
    )
    assert "atorvastatin" in curation_text, "the drug name did not reach the curation request"
    assert pii_scan.scan_text_full(curation_text, token_config=idcfg) == 0, (
        "the curation request carried operator identity (crown-jewel leg-2 breach)"
    )
    assert _FAKE_LEGAL_NAME not in curation_text, "a legal name crossed into the curation request"


def test_injected_identity_reds_the_curation_probe(tmp_path):
    """AC-2 W6 negative control (leg 2): an injected identity token REDS the curation probe."""
    idcfg = _identity_config(tmp_path)
    request_text = json.dumps(
        care_review._curation_messages(["atorvastatin 20mg", _FAKE_LEGAL_NAME])
    )
    assert pii_scan.scan_text_full(request_text, token_config=idcfg) > 0, (
        "the leg-2 probe could not count an injected identity token — it is vacuous"
    )


def test_no_raw_drug_string_as_planner_token_or_in_dispatch(tmp_path):
    """AC-2: a CONFIRMED curation persists the de-id CLASS token — 0 raw drug as token / in dispatch."""
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _seed_scaffold_med(store_root, scaffold_root)
    idcfg = _identity_config(tmp_path)
    backend = _CareBackend(confident=True)
    care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=idcfg,
    )
    readings = store.read("rx-interaction-classes", root=store_root)
    assert readings, "a confident curation did not persist the rx-interaction-classes token"
    token_value = str(readings[-1]["value"])
    assert token_value == "cyp3a4-pgp", f"unexpected persisted class token {token_value!r}"
    assert "atorvastatin" not in token_value, "a raw drug string persisted as the planner token"
    payload = router.dispatch(router.summarize(_reader(store_root), identity_config=idcfg)).payload
    assert "atorvastatin" not in json.dumps(payload), "a raw drug string reached the dispatch payload"
    assert payload["rx-interaction-classes"] == "cyp3a4-pgp"


def test_curation_defers_fail_closed_on_identity_in_med_value(tmp_path):
    """AC-2 leg 2 (adversarial): identity + a bare DOB typed INTO the med free-text NEVER egresses.

    The leg-2 crown-jewel de-association contract: `capture` routes the raw med free-text
    record-only UNSCANNED, so an operator who types a name / DOB / email into the medication list
    must NOT have it serialized into the curation `converse` request. Mirrors leg-1's FAIL-CLOSED
    8j6 posture (`router.summarize` RAISES on a PII pass-through; it never partial-strips): the
    curation DEFERS with 0 `converse` call rather than send a leaky de-identified request.
    RED-capable: the pre-fix `_curate_meds` (no value gate) egresses the poisoned value verbatim —
    `pii_scan.scan_text_full` over the recorded curation request counts the name + email (> 0) and
    the curation request is present in `backend.calls`; this test reds it.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    idcfg = _identity_config(tmp_path)
    poisoned = (f"atorvastatin 20mg prescribed to {_FAKE_LEGAL_NAME}, DOB 1986-04-12, "
                "jane.doe@example.com")
    capture.persist_capture({"rx-interaction-classes": poisoned, "favorite-color": "blue"},
                            root=store_root, scaffold_root=scaffold_root)
    backend = _CareBackend()
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=idcfg,
    )
    # 0 curation converse call — the poisoned med value never egressed.
    curation_calls = [c for c in backend.calls if "rx-interaction-curation" in json.dumps(c)]
    assert curation_calls == [], "the poisoned med value egressed a curation request (leg-2 breach)"
    # No recorded request (clarifying included) carries the identity / DOB / email.
    for call in backend.calls:
        text = json.dumps(call)
        assert pii_scan.scan_text_full(text, token_config=idcfg) == 0, "operator PII reached a request"
        assert _FAKE_LEGAL_NAME not in text and "1986-04-12" not in text and "jane.doe@example.com" not in text
    # The curation deferred honestly (an honest reason) and wrote 0 rx-interaction-classes token.
    assert result["curation"]["deferred"] is True and result["curation"].get("reason"), (
        "the poisoned-med curation did not defer honestly"
    )
    assert store.read("rx-interaction-classes", root=store_root) == [], "a poisoned curation wrote a token"
    # Leg 1 still delivered its clarifying questions (only the curation deferred).
    assert result["questions"], "leg 1 was suppressed by the leg-2 fail-closed gate"


def test_clean_med_value_still_curates_after_the_gate(tmp_path):
    """The leg-2 gate fires ONLY on a PII/date hit — a clean med value still curates normally."""
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _seed_scaffold_med(store_root, scaffold_root, value="atorvastatin 20mg, metformin 500mg")
    backend = _CareBackend(confident=True)
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=_identity_config(tmp_path),
    )
    assert result["curation"]["confirmed"] is True, "a clean med value did not curate normally"
    assert store.read("rx-interaction-classes", root=store_root), "the clean curation persisted no token"


def test_confirm_when_unsure_writes_zero_unconfirmed_class(tmp_path):
    """AC-4: an uncertain classification surfaces a confirm question + writes 0 until confirmed."""
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _seed_scaffold_med(store_root, scaffold_root)
    backend = _CareBackend(confident=False)
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=_identity_config(tmp_path),
    )
    assert result["curation"]["confirmed"] is False, "an uncertain classification was auto-applied"
    assert result["curation"]["confirm_question"], "no confirm question surfaced for the uncertain class"
    assert store.read("rx-interaction-classes", root=store_root) == [], (
        "an unconfirmed rx-interaction-classes token was written (auto-apply false-clean)"
    )
    # Only a CONFIRMED token persists — the planner input is the confirmed class only.
    care_review.confirm_curation(["cyp3a4-pgp"], store_root=store_root)
    confirmed = store.read("rx-interaction-classes", root=store_root)
    assert confirmed and confirmed[-1]["value"] == "cyp3a4-pgp", "the confirmed token did not persist"


# --------------------------------------------------------------------------- #
# Tier-3 FIX-2 — the curation reads the LATEST capture only, not the union of all
# history (bounds spend + recovers from a prior dated med's permanent-defer trap).
# --------------------------------------------------------------------------- #


def _write_capture(scaffold_root, stamp, value):
    """Write one record-only `capture-<stamp>.json` med file with an explicit ordering stamp."""
    root = Path(scaffold_root)
    root.mkdir(parents=True, exist_ok=True)
    (root / f"capture-{stamp}.json").write_text(
        json.dumps({"rx-interaction-classes": value}) + "\n"
    )


def test_curation_reads_latest_capture_only_not_the_union(tmp_path):
    """FIX-2: a superseding capture REPLACES the prior meds — the curation never unions history.

    Two record-only captures land in the scaffold (an OLD `atorvastatin`, a NEWER `metformin`).
    The review re-fires on every complete-profile save, so unioning would re-classify the whole
    history each time (repeated spend + duplicate store writes). The curation must carry ONLY the
    latest capture's meds.

    RED-capable: the pre-fix `_scaffold_meds` globbed ALL captures and unioned them — the
    curation request would carry BOTH drug names, reddening the `atorvastatin`-absent assertion.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _write_capture(scaffold_root, "2026-06-01T00-00-00", "atorvastatin 20mg")
    _write_capture(scaffold_root, "2026-06-02T00-00-00", "metformin 500mg")
    backend = _CareBackend(confident=True)
    care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=_identity_config(tmp_path),
    )
    curation_text = json.dumps(
        [c for c in backend.calls if "rx-interaction-curation" in json.dumps(c)][0]
    )
    assert "metformin" in curation_text, "the latest capture's med did not reach the curation"
    assert "atorvastatin" not in curation_text, (
        "an OLD capture's med reached the curation — the curation unioned history (spend + drop)"
    )


def test_clean_latest_capture_recovers_from_a_prior_dated_med_defer(tmp_path):
    """FIX-2: a clean LATEST capture curates normally even after a prior DATED med (recovery).

    A dated med (`atorvastatin since 2020-01-15`) trips `_DATE_LIKE` and defers the curation. Under
    the pre-fix union `_scaffold_meds`, EVERY future review re-read that old dated file and deferred
    forever (no recovery). Reading the LATEST capture only lets a later clean capture curate.

    RED-capable: the pre-fix union carries the dated OLD value into `_med_value_has_identity`, which
    defers — reddening the `confirmed`/persisted assertions.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _write_capture(scaffold_root, "2026-06-01T00-00-00", "atorvastatin since 2020-01-15")
    _write_capture(scaffold_root, "2026-06-02T00-00-00", "atorvastatin 20mg")
    backend = _CareBackend(confident=True)
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=_identity_config(tmp_path),
    )
    assert result["curation"]["confirmed"] is True, (
        "a clean latest capture did not recover from a prior dated med's defer trap"
    )
    assert store.read("rx-interaction-classes", root=store_root), "the recovered curation persisted no token"


# --------------------------------------------------------------------------- #
# Tier-3 FIX-3 — a leg-2 curation failure preserves the already-paid-for leg-1
# clarifying questions (never discards them via a total-deferred receipt).
# --------------------------------------------------------------------------- #


class _Leg2FailBackend:
    """A backend that answers leg-1 (clarifying) but RAISES ModelCallError on leg-2 (curation)."""

    def __init__(self):
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        if "rx-interaction-curation" in json.dumps(messages):
            raise ModelCallError("curation backend unavailable")
        return {"reply": "What is your top training priority this cycle?", "extraction": []}


def test_leg2_failure_preserves_leg1_questions_with_deferred_curation(tmp_path):
    """FIX-3: leg-1 succeeds + leg-2 raises -> keep the leg-1 questions AND a deferred curation.

    The pre-fix `review` ran both legs inside ONE try/except, so a leg-2 `ModelCallError` returned
    `_deferred(...)` with `questions: []` — discarding the already-paid-for leg-1 clarifying reply.
    The receipt must carry the leg-1 questions and a deferred-curation sub-state instead.

    RED-capable: the pre-fix single-try `review` returns an empty-questions total-deferred receipt
    — reddening the non-empty-questions + not-total-deferred assertions.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    _seed_scaffold_med(store_root, scaffold_root, value="atorvastatin 20mg")
    backend = _Leg2FailBackend()
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=_identity_config(tmp_path),
    )
    # The paid-for leg-1 question survives (the whole review is NOT total-deferred).
    assert result["deferred"] is False, "a leg-2 failure wrongly total-deferred the whole review"
    assert result["questions"], "the leg-1 clarifying questions were discarded on a leg-2 failure"
    # The curation carries a deferred sub-state with an honest reason.
    assert result["curation"]["deferred"] is True and result["curation"].get("reason"), (
        "a leg-2 failure did not surface a deferred-curation sub-state"
    )
    # No rx-interaction-classes token was written by the failed curation.
    assert store.read("rx-interaction-classes", root=store_root) == [], (
        "a failed leg-2 curation wrote a class token"
    )
    # The curation converse call WAS attempted (proving leg-1 ran first and the failure is leg-2).
    assert any("rx-interaction-curation" in json.dumps(c) for c in backend.calls), (
        "the curation leg was never attempted — the test does not exercise the leg-2 failure path"
    )


# --------------------------------------------------------------------------- #
# Tier-3 FIX-4 — the `_DATE_LIKE` DOB backstop, ISOLATED (a bare DOB in a med value
# with NO name/email/phone still defers). The compound-poison test never lets
# `_DATE_LIKE` determine the outcome; this does.
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("dated, clean", [
    # 2-digit-year forms: pii_scan is 4-digit-year-anchored (flood-safe against macro
    # splits like "40/30/30"), so it reads 0 on these — the defer is attributable to
    # care_review's local _DATE_LIKE ALONE, the isolation this test exists for. (pii_scan
    # NOW catches 4-digit/ISO DOBs itself via bead yduw — a defense-in-depth overlap — so
    # _DATE_LIKE's independent contribution is exactly these 2-digit-year formats.)
    ("atorvastatin 20mg 4/12/86", "atorvastatin 20mg"),      # slashed 2-digit year
    ("metformin 4-12-86", "metformin 500mg"),                # dashed 2-digit year
])
def test_bare_dob_in_med_value_defers_isolating_date_like(dated, clean, tmp_path):
    """FIX-4: a DATE-ONLY med value (no name/email/phone) defers the curation — `_DATE_LIKE` alone.

    The existing fail-closed test uses a COMPOUND poison (name+email+DOB) where name+email already
    trip `pii_scan` `hits > 0`, so `_DATE_LIKE` never determines the outcome. This seeds a med value
    whose ONLY identity signal is a 2-digit-year date — a format pii_scan's 4-digit-year-anchored
    detector leaves to `_DATE_LIKE` (`pii_scan.scan_text_full` reads 0, proven below), so the defer
    is attributable to `_DATE_LIKE` alone. Parametrized over the slashed + dashed branches.

    RED-capable: drop the `or bool(_DATE_LIKE.search(value))` clause and the dated value scans 0,
    the curation proceeds (a converse call + a class-token write) — reddening BOTH assertions. The
    companion clean value (no date) proves the date is the SOLE trigger: it curates normally.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    _seed_full(store_root)
    idcfg = _identity_config(tmp_path)
    # Pre-condition: the dated value's ONLY identity signal is the date (pii_scan reads 0).
    assert pii_scan.scan_text_full(dated, token_config=idcfg) == 0, (
        f"the dated med {dated!r} carries a pii_scan hit — _DATE_LIKE is not the sole trigger"
    )
    _seed_scaffold_med(store_root, scaffold_root, value=dated)
    backend = _CareBackend(confident=True)
    result = care_review.review(
        _reader(store_root), client=ModelClient(backend=backend), key_available=True,
        store_root=store_root, scaffold_root=scaffold_root, identity_config=idcfg,
    )
    # The date alone deferred the curation: 0 curation converse call, 0 class-token write.
    assert [c for c in backend.calls if "rx-interaction-curation" in json.dumps(c)] == [], (
        f"a bare-DOB med value {dated!r} egressed a curation request (_DATE_LIKE did not defer)"
    )
    assert result["curation"]["deferred"] is True, "the bare-DOB med value did not defer the curation"
    assert store.read("rx-interaction-classes", root=store_root) == [], (
        "a bare-DOB med value wrote a class token (must defer)"
    )

    # Companion: the SAME med value WITHOUT the date curates normally (date is the sole trigger).
    clean_store = tmp_path / "clean-store"
    clean_scaffold = tmp_path / "clean-scaffold"
    _seed_full(clean_store)
    _seed_scaffold_med(clean_store, clean_scaffold, value=clean)
    clean_backend = _CareBackend(confident=True)
    clean_result = care_review.review(
        _reader(clean_store), client=ModelClient(backend=clean_backend), key_available=True,
        store_root=clean_store, scaffold_root=clean_scaffold, identity_config=idcfg,
    )
    assert clean_result["curation"]["confirmed"] is True, (
        f"the clean med {clean!r} (no date) did not curate — date is not the sole trigger"
    )
    assert any("rx-interaction-curation" in json.dumps(c) for c in clean_backend.calls), (
        "the clean companion made no curation call"
    )


def test_confirm_question_with_no_proposed_classes_does_not_ask_to_confirm_nothing():
    """When the model proposed 0 classes, the message does NOT ask the operator to 'confirm classes'.

    A confirm-when-unsure prompt with an EMPTY proposed set previously read "Please confirm your
    medication interaction classes before I record them" while showing nothing — the operator saw a
    confirm prompt with nothing to confirm. The empty-proposed message must instead state honestly that
    nothing was recorded, with no imperative to confirm a non-existent class list.
    """
    from scripts.serve import care_review
    msg = care_review._confirm_question([])
    assert "Please confirm your medication interaction classes" not in msg, (
        "the empty-proposed message still asks the operator to confirm classes that do not exist"
    )
    assert "not recorded anything" in msg or "nothing" in msg.lower(), (
        "the empty-proposed message does not honestly state that nothing was recorded"
    )
    # the non-empty case still asks to confirm the actual proposed classes.
    with_classes = care_review._confirm_question(["androgen", "cyp3a4"])
    assert "androgen" in with_classes and "cyp3a4" in with_classes, "the proposed classes are not surfaced to confirm"
