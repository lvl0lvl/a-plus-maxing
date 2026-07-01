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

from scripts.model.client import ModelClient
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
