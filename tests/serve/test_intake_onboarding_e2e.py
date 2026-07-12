"""End-to-end intake/onboarding gate + the composed ADR-0033/0034/0035 falsification probes.

The terminal Wave-7 integration proof for the intake/onboarding slice: a fresh store renders the
Create-Profile-only surface (0 platform surfaces); filling the required intake through the
PRODUCTION capture path (`build_server` over tmp roots → POST `/upload` → `capture.persist_capture`)
flips the derived store-grounded completeness gate (`app_shell._intake_complete`), unlocks, and
serves the full shell opening on the Chat-with-Team workspace / My-Info tab; a DIFFERENT filled
profile yields a DIFFERENT de-identified `router.summarize` summary (the four serve-fillable tokens
carry the captured signal, not a constant). Every raw-PII token is proven NEVER to cross to the
no-train planner (`router.dispatch(...).payload`) nor any model request, and the safety signals are
proven to route to referral (`referral.collate`) never a plan input. Driven over tmp roots with a
RECORDING mock backend injected at the ADR-0015 `ModelClient(backend=...)` seam — 0 network, 0 key,
0 live `converse`/curation spend.

This module wires NO production code. GREEN means the binding test passes against the already-built
Wave-1…6 mechanism; a RED for a real MECHANISM gap routes back to the owning task (T1 capture / T2
de-association / T3 safety+referral / T4/T5 wizard+equipment / T6 gate / T7 unlocked shell + edit
path / T8 care-review), not a fix authored here.

THE EIGHT COMPOSED FALSIFICATION PROBES (each FAILING-CAPABLE; QA-F3 RED-on-violation):
  (1) gate-bypass / hidden-until-complete (AC-1/AC-2) — REDs if a fresh/partial store serves ANY
      platform surface instead of Create-Profile-only, or if an incomplete required set / an
      unanswered safety screen UNLOCKS.
  (2) non-tautological-headline / captured-signal A≠B (AC-1) — REDs if a DIFFERENT filled profile
      yields the SAME de-id summary on all four serve-fillable tokens, or if the assertion is
      merely "a page was served".
  (3) crown-jewel PII boundary (AC-3) — REDs if a seeded raw-PII profile (legal name / full DOB /
      raw drug name / PHQ-2 free-text answer / race string) produces ≥ 1 of those raw strings in
      the `dispatch` payload OR a model request, OR if the de-associated EXACT AGE + weight + trend
      do NOT reach the planner (an over-strip).
  (4) editable-My-Info no-bypass (SEC-F1, behavioral) (AC-3) — REDs if a raw value driven THROUGH
      the My-Info edit `/upload` re-submit path crosses to the `dispatch` payload or a model request.
  (5) safety-bypass (AC-4) — REDs if a positive exercise-safety / PHQ-2 / apnea answer does NOT
      yield a `referral::<name>` flag, OR if a `safety-screen::*` / `referral::*` item is a
      `SUMMARY_FIELD_SET` token / reaches a dispatched payload.
  (6) serve-auto-classification + meds-curation de-association (AC-5) — REDs if a raw med at intake
      produces ≥ 1 `rx-interaction-classes` store write from `persist_capture`, or if an unconfirmed
      curated class persists.
  (7) extend-not-rebuild (AC-6) — REDs if `git diff --numstat <fork-point>` over the 7 frozen
      `scripts/plan/*` engine files + `scripts/store/*.py` emits ANY row, or if `router.py` is
      non-additive (the `SUMMARY_FIELD_SET` membership changed, the `dispatch` whitelist deleted, or
      deletions over the sanctioned cap).
  (8) 0-live-spend (AC-7) — REDs if the E2E makes a `key_source.resolve()`-gated live call, a live
      `converse`/curation call, or opens a non-loopback socket.

LOCK/UNLOCK DISCRIMINATOR NOTE (test-precision, verified 2026-07-01): the SPA nav marker
"Chat with Team" is NOT a lock discriminator — it survives in the left-nav sidebar in BOTH the
locked and unlocked bodies (`app_shell._lock_to_create_profile` strips the four platform `.screen`
SECTIONS, not the sidebar). The genuinely gate-varying markers are the platform screen sections +
the workspace tabs (`id="screen-team"`, `id="screen-dashboard"`, `id="screen-plan"`,
`id="screen-profile"`, `data-tab="generate"`, `data-tab="build">My Info`) — ABSENT when locked,
PRESENT when unlocked — plus `id="screen-wizard"` PRESENT (the Create-Profile surface). This is a
test-authoring precision the headline resolves; the gate mechanism itself flips correctly.

DEFERRED (NOT a CI gate): the operator-present LIVE care-agent run — a real no-train key + real
spend, end-to-end through final-save → de-id review → questions-in-thread + meds curation (the
OS-level-egress-guard LIVE form of the crown-jewel probes) — is ADR-0035 OQ-1, the operator-gated
checkpoint AFTER this build. No `@pytest.mark.skipif` variant is required — it is an operator
checkpoint, not a collected-skipped test.
"""

import functools
import http.client
import json
import subprocess
import threading
from pathlib import Path

import pytest

from scripts.guard import pii_scan
from scripts.model.client import ModelClient
from scripts.model.key_source import KeyUnavailableError
from scripts.plan import router
from scripts.serve import care_review
from scripts.serve import referral
from scripts.serve import server as serve_server
from scripts.store import store
from vault.design.templates import app_shell

REPO_ROOT = Path(__file__).resolve().parents[2]

BOUNDARY = "----aplusintakeonboarding7MA4YWxkTrZu0gW"

# The platform-surface markers ABSENT from the locked Create-Profile body and PRESENT once the gate
# unlocks (verified 2026-07-01). NOT "Chat with Team" — that survives the left-nav in both states.
_PLATFORM_MARKERS = (
    'id="screen-team"',
    'id="screen-dashboard"',
    'id="screen-plan"',
    'id="screen-profile"',
    'data-tab="generate"',
    'data-tab="build">My Info',
)
# The Create-Profile surface marker (present in BOTH states — the wizard is the locked body).
_WIZARD_MARKER = 'id="screen-wizard"'
# The default-active unlocked workspace (opens-on-Chat-with-Team / My-Info tab default-active).
_SCREEN_TEAM_ACTIVE = 'class="screen active" id="screen-team"'

# A fake operator legal name (NEVER a real one), written into a gitignored-shape one-regex-per-line
# identity token config so the crown-jewel identity negative control REDs deterministically in CI.
_FAKE_LEGAL_NAME = "Marlowe Fenwick"
# A distinctive race/ethnonym string seeded into a record-only field — value-class direct-substring
# proof (a rare token that never collides with a derived plan class).
_RACE_STRING = "Melungeon"
# A raw PHQ-2 free-text answer — capture writes only the de-identified `positive`/`negative` marker,
# so the raw answer must appear NOWHERE downstream.
_PHQ2_RAW_ANSWER = "felt hopeless nearly every day for weeks"

# The pinned `router.SUMMARY_FIELD_SET` membership (17 members, verified 2026-07-01). AC-6 asserts
# this tuple is byte-identical — a membership change is the crown-jewel-spine regression the guard
# catches. (The recipe prose said "18 members"; the live tuple is 17 — the mechanism is pinned here.)
_PINNED_SUMMARY_FIELD_SET = (
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

# The 7 byte-frozen inner-engine plan files (EXTEND-NOT-REBUILD; router.py is EXCLUDED — it is T2's
# sanctioned additive seam, guarded separately by the router scoped-additive probe below).
_FROZEN_ENGINE_PATHS = (
    # scripts/plan/orchestrate.py CARVED OUT — ADR-0043-T2 (reconcile via cross_domain_seams) superseded the orchestrator; behavioral guarantor tests/serve/test_orchestrator_reconcile.py. Wave-3 frozen-guard reconciliation (F-011), Architect Option-A ruling.
    "scripts/plan/pipeline.py",
    # scripts/plan/assemble.py CARVED OUT — ADR-0041-T2 (uniform-program migration) superseded the assemble composer; behavioral guarantor tests/plan/test_assemble.py + tests/plan/test_generate_plan_uniform.py. Wave-2 frozen-guard reconciliation, Architect Option-A ruling.
    # scripts/plan/generate_plan.py CARVED OUT — ADR-0042/0041/0046/0043 operator-signed-off (HARD, ADR Phase-1 gate) superseded plan front door; guarded behaviorally by tests/plan/test_generate_plan.py + core-capability-audit.sh + the per-ADR numstat probes (NOT this byte-guard). Architect ruling docs/adr/.pipeline/frozen-guard-reconciliation-ruling.md §2, feature/comprehensive-plan-adr.
    "scripts/plan/adjudicate.py",
    "scripts/plan/adjust.py",
    # scripts/plan/track.py CARVED OUT — ADR-0044-T2 (mixed-history reader re-point of resolve_plan_progress) superseded track.py; behavioral guarantor tests/store/test_plan_model_reader.py + tests/plan/test_track.py. Wave-3 frozen-guard reconciliation (F-011), Architect Option-A ruling.
)
_ROUTER_ADDITIVE_PATH = "scripts/plan/router.py"
# The ADR-0033-0035-T2 sanctioned deletion cap (mirroring `test_route.py::_ROUTER_SANCTIONED_DELETIONS`).
_ROUTER_SANCTIONED_DELETIONS = 14


# --------------------------------------------------------------------------- #
# Harness — the production `build_server` over tmp roots + the recording mock seam
# --------------------------------------------------------------------------- #


class _RecordingCareBackend:
    """A recording converse backend: records every request, scripts a per-leg reply.

    Records each `converse(messages)` payload into `self.calls` (the crown-jewel probe reads what
    the model call CARRIED). Distinguishes the two care-review legs by request CONTENT (the
    care_review task marker), so assertions stay order-independent: an `rx-interaction-curation`
    request gets a scripted class proposal (confident by default; `confident=False` drives the
    uncertain path), any other request gets a clarifying question.
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

    def clarifying_calls(self):
        """The recorded clarifying-review requests (NOT the leg-2 meds curation)."""
        return [c for c in self.calls if "rx-interaction-curation" not in json.dumps(c)]

    def curation_calls(self):
        """The recorded leg-2 meds-curation requests (the sanctioned drug-name egress class)."""
        return [c for c in self.calls if "rx-interaction-curation" in json.dumps(c)]


def _key_absent():
    """A key_resolver that fails-closed — care-review never fires (deterministic HTML re-render)."""
    raise KeyUnavailableError("no key in test")


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _build(tmp_root, *, backend=None, key_resolver=_key_absent, identity_config=None):
    """Build the production server over tmp roots + the injected recording-mock seam.

    Injects the mock backend at the ADR-0015 `ModelClient(backend=...)` seam. `key_resolver`
    defaults to the fail-closed `_key_absent` (care-review off — the headline drives GET `/`, not
    the review); the crown-jewel path passes `key_resolver=lambda: None` to fire the review at 0
    live `key_source.resolve()` calls.
    """
    client = ModelClient(backend=backend) if backend is not None else None
    srv = serve_server.build_server(
        0, store_root=tmp_root / "store", dna_root=tmp_root / "dna",
        scaffold_root=tmp_root / "scaffold", client=client,
        key_resolver=key_resolver,
        identity_config=str(identity_config) if identity_config is not None else None,
    )
    return srv, srv.server_address[1]


def _field_part(name, value):
    """Build one multipart NON-FILE form-field part (staged in `fields` → `persist_capture`)."""
    out = bytearray()
    out += f"--{BOUNDARY}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="{name}"\r\n\r\n').encode()
    out += str(value).encode("utf-8")
    out += b"\r\n"
    return bytes(out)


def _multipart_fields(fields):
    """Build a fields-only multipart/form-data body (no files)."""
    body = bytearray()
    for name, value in fields.items():
        body += _field_part(name, value)
    body += f"--{BOUNDARY}--\r\n".encode()
    return bytes(body)


def _post_fields(port, fields):
    """POST a fields-only multipart capture to `/upload`; return (status, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/upload", body=_multipart_fields(fields),
                 headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, text


def _get_root(port):
    """GET `/` on the running server; return the served body (the gate-conditional shell)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", "/")
    resp = conn.getresponse()
    body = resp.read().decode("utf-8")
    conn.close()
    return resp.status, body


def _reader(tmp_root):
    """The instance-root-bound `store.read` partial `summarize`/`collate`'s caller contract needs."""
    return functools.partial(store.read, root=tmp_root / "store")


# The required intake filled through the PRODUCTION capture path — the FORM FIELD names (the T4↔T1
# contract), NOT the store-item names: `date-of-birth`/`bodyweight-kg` write the named-excluded raw
# source (derived to `training-age-band`/`bodyweight-band`); `train-around` writes the raw-symptom
# source (→ `active-issue-class`); the safety FORM fields are `exercise-safety`/`phq2`/`apnea` (the
# capture writes the `safety-screen::<screen>` store-item marker). This set is dispatch-complete.
def _required_fields(**overrides):
    """The dispatch-complete required intake as a capture form-field dict (override any field)."""
    fields = {
        "date-of-birth": "1986-04-12",
        "bodyweight-kg": "82",
        "sex-for-dosing": "male",
        "equipment-access-class": "full-home-gym",
        "goal-domains": "Workout;Nutrition",
        "goal-targets": "build strength and improve sleep",
        "goal-priority-order": "recovery then strength",
        "recovery-status-band": "moderate",
        "train-around": "occasional knee soreness",
        "hard-limits": "no overhead pressing",
        "exercise-safety": "no",
        "phq2": "no",
        "apnea": "no",
    }
    fields.update(overrides)
    return fields


def _identity_config(tmp_root):
    """Write a gitignored-shape one-regex-per-line identity token config (the fake legal name)."""
    tmp_root.mkdir(parents=True, exist_ok=True)
    path = tmp_root / "operator-identity.txt"
    path.write_text(_FAKE_LEGAL_NAME + "\n")
    return path


# --------------------------------------------------------------------------- #
# Cycle 1 — the headline lock→unlock + A≠B captured-signal + negative controls + 0-spend
# --------------------------------------------------------------------------- #


def test_headline_fresh_store_locked_then_required_intake_unlocks_full_shell(tmp_path):
    """AC-1 (HEADLINE, non-tautological): fresh store → Create-Profile-only; required intake → full shell.

    A fresh tmp store serves the LOCKED Create-Profile body — every platform-surface marker ABSENT
    (0 platform surface reachable), the wizard PRESENT. Filling the required intake via the
    PRODUCTION capture POST(s) to `/upload` flips the derived store-grounded gate: GET `/` now serves
    the full shell — every platform marker PRESENT, the Chat-with-Team workspace default-active
    (opens-on-My-Info). NEVER asserts merely "a page was served"; the transition itself is the proof
    (the AC-2 negative control proves it distinguishes a real unlock from the locked state).
    """
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        # Fresh store → LOCKED Create-Profile-only (0 platform surfaces).
        status, locked = _get_root(port)
        assert status == 200
        assert _WIZARD_MARKER in locked, "the fresh store did not serve the Create-Profile wizard"
        for marker in _PLATFORM_MARKERS:
            assert marker not in locked, (
                f"a fresh store leaked a platform surface {marker!r} (gate-bypass — hidden-until-complete broken)"
            )

        # Fill the required intake through the PRODUCTION capture path.
        post_status, _ = _post_fields(port, _required_fields())
        assert post_status == 200, f"the required-intake capture POST returned {post_status}"

        # The gate flipped → the full shell, opening on the Chat-with-Team / My-Info workspace.
        status, unlocked = _get_root(port)
        assert status == 200
        for marker in _PLATFORM_MARKERS:
            assert marker in unlocked, (
                f"the completed intake did not unlock the platform surface {marker!r} (gate never flipped)"
            )
        assert _SCREEN_TEAM_ACTIVE in unlocked, (
            "the unlocked shell did not open on the Chat-with-Team workspace / My-Info tab"
        )
    finally:
        srv.shutdown()
        srv.server_close()


def test_headline_different_profile_yields_different_de_id_summary(tmp_path):
    """AC-1 (captured-signal, A≠B): a DIFFERENT filled profile → a DIFFERENT de-id summary.

    Fills profile A and a DIFFERENT profile B (distinct nutrition/supplement/peptide/training
    free-text) through the PRODUCTION capture path over two tmp stores; `router.summarize` over each
    differs on ≥ 1 of the four serve-fillable tokens — proving the served de-id summary carries the
    CAPTURED SIGNAL, not a hardcoded constant. REDs if the two summaries are identical on all four
    (the feature is plumbed but the signal does not flow).
    """
    profile_a = _required_fields(
        **{"nutrition-detail": "strict vegan plant-based diet",
           "supplement-stack": "creatine 5g daily",
           "peptide-stack": "none",
           "training-detail": "5 days per week heavy barbell lifting"})
    profile_b = _required_fields(
        **{"nutrition-detail": "high-protein carnivore",
           "supplement-stack": "none",
           "peptide-stack": "BPC-157 250mcg daily",
           "training-detail": "2 days per week light activity"})

    root_a, root_b = tmp_path / "A", tmp_path / "B"
    for root, profile in ((root_a, profile_a), (root_b, profile_b)):
        srv, port = _build(root)
        _serve_in_thread(srv)
        try:
            assert _post_fields(port, profile)[0] == 200
        finally:
            srv.shutdown()
            srv.server_close()

    summary_a = router.summarize(_reader(root_a))
    summary_b = router.summarize(_reader(root_b))
    serve_fillable = ("dietary-pattern-class", "supplement-stack-class",
                      "peptide-use-class", "training-volume-band")
    differing = [t for t in serve_fillable if summary_a.get(t) != summary_b.get(t)]
    assert differing, (
        "a DIFFERENT filled profile yielded the SAME de-id summary on all four serve-fillable "
        f"tokens (constant summary — captured signal does not flow): A={summary_a}, B={summary_b}"
    )


def test_negative_control_required_set_incomplete_stays_locked(tmp_path):
    """AC-2 (failing-capable negative control): the required set incomplete STAYS locked.

    Fills every required token EXCEPT `goal-priority-order` → GET `/` STAYS Create-Profile-only (0
    platform surfaces). Proves AC-1's unlock assertion goes RED when the required set is absent — the
    headline is not a constant-pass.
    """
    fields = _required_fields()
    del fields["goal-priority-order"]
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        assert _post_fields(port, fields)[0] == 200
        status, body = _get_root(port)
        assert status == 200
        assert _WIZARD_MARKER in body, "the incomplete profile did not stay on the Create-Profile wizard"
        for marker in _PLATFORM_MARKERS:
            assert marker not in body, (
                f"an incomplete required set UNLOCKED platform surface {marker!r} (gate-bypass)"
            )
    finally:
        srv.shutdown()
        srv.server_close()


def test_negative_control_safety_screen_unanswered_stays_locked(tmp_path):
    """AC-2 (failing-capable negative control): a safety screen unanswered STAYS locked.

    Fills every required token but leaves the PHQ-2 safety screen UNANSWERED (no `phq2` field, so no
    `safety-screen::phq2` marker) → GET `/` STAYS locked. Proves the gate requires the three answered
    safety markers, not only the demographic tokens.
    """
    fields = _required_fields()
    del fields["phq2"]
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        assert _post_fields(port, fields)[0] == 200
        status, body = _get_root(port)
        assert status == 200
        assert _WIZARD_MARKER in body, "the unanswered-safety profile did not stay on the wizard"
        for marker in _PLATFORM_MARKERS:
            assert marker not in body, (
                f"an unanswered safety screen UNLOCKED platform surface {marker!r} (safety-gate-bypass)"
            )
    finally:
        srv.shutdown()
        srv.server_close()


def test_zero_live_spend_mock_seam_no_key_no_converse_no_curation(tmp_path, monkeypatch):
    """AC-7 (mock-tested, 0 live spend): the full intake→unlock→care-review runs at 0 key-gated calls.

    Spies `key_source.resolve` (the live backend's ONLY key gate); the full intake → unlock →
    care-review E2E runs via the recording mock backend + the injected `key_resolver`, and the spy
    records 0 calls (the live lane is never touched). Asserts the test source injects the mock at the
    ADR-0015 seam (`"ModelClient(backend=" in src`). Proves the run is deterministic + CI-runnable
    with no key / 0 spend. (The LIVE run — real key + real spend — is ADR-0035 OQ-1, out of CI.)
    """
    calls = []

    def _spy_resolve(*args, **kwargs):
        calls.append((args, kwargs))
        return "FAKE-KEY-NEVER-USED"

    monkeypatch.setattr("scripts.model.key_source.resolve", _spy_resolve)

    backend = _RecordingCareBackend()
    idcfg = _identity_config(tmp_path / "meta")
    srv, port = _build(tmp_path, backend=backend, key_resolver=lambda: None, identity_config=idcfg)
    _serve_in_thread(srv)
    try:
        status, _ = _post_fields(port, _required_fields(**{"rx-interaction-classes": "atorvastatin 20mg"}))
        assert status == 200
    finally:
        srv.shutdown()
        srv.server_close()

    assert backend.calls, "the recording mock backend received no care-review call (path not exercised)"
    assert calls == [], "a live `key_source.resolve()`-gated call occurred (0-live-spend breach)"
    src = Path(__file__).read_text()
    assert "ModelClient(backend=" in src, "the E2E does not inject the mock at the ADR-0015 seam"


# --------------------------------------------------------------------------- #
# Cycle 2 — crown-jewel PII boundary + SEC-F1 behavioral edit-path + safety + curation
# --------------------------------------------------------------------------- #


def _drive_intake_and_care_review(tmp_path, *, fields, backend, identity_config):
    """POST a dispatch-complete intake through the server, firing the care-review; return the backend.

    Runs the FULL production path (capture → store → the T6 gate → the T8 final-save care-review over
    the injected recording mock). The recording backend records the clarifying `converse` + the
    distinct leg-2 curation request the crown-jewel scans.
    """
    srv, port = _build(tmp_path, backend=backend, key_resolver=lambda: None, identity_config=identity_config)
    _serve_in_thread(srv)
    try:
        status, _ = _post_fields(port, fields)
        assert status == 200, f"the intake capture POST returned {status}"
    finally:
        srv.shutdown()
        srv.server_close()
    return backend


def test_probe_crown_jewel_raw_pii_profile_zero_crossing_dispatch_and_model_requests(tmp_path):
    """AC-3 (CROWN-JEWEL, load-bearing): a seeded raw-PII profile → 0 raw crossing; de-id facts present.

    Seeds a known raw-PII profile through the PRODUCTION capture POST — a legal name + race string
    (record-only), a full DOB `1986-03-14` (→ `training-age-band`, the exact age, never the DOB
    string), a raw drug `atorvastatin` (record-only meds → the leg-2 curation), a PHQ-2 free-text
    answer (dropped — capture keeps only the de-identified marker). Builds
    `dispatch(summarize(store_read)).payload` AND captures every recorded model request, then asserts:

    - The operator IDENTITY (legal name, race string) — `pii_scan.scan_text_full(..., token_config=
      fixture) == 0` over the payload + EVERY request INCLUDING the curation (non-vacuous: the
      negative control below poisons a copy and counts > 0), plus direct-substring absence.
    - The full DOB `1986-03-14` + the PHQ-2 raw answer — 0 in the payload + EVERY request.
    - The raw drug `atorvastatin` — 0 in the `dispatch` payload AND 0 in the clarifying (non-curation)
      requests (the no-train PLANNER boundary sees only the `rx-interaction-classes` CLASS token). It
      LEGITIMATELY MAY appear in the leg-2 meds-curation request (the sanctioned ADR-0035 named
      egress class: drug names only, 0 identity) — so the drug-name assertion is SCOPED to the
      planner boundary + the non-curation requests, NOT reddened on the curation.
    - The planner DOES receive the de-associated EXACT AGE (an integer ≈ 40, not the DOB string) +
      the current weight + trend (`bodyweight-band` PRESENT + NON-EMPTY) — the expected facts, not an
      over-strip.

    ≥ 1 raw crossing reds the boundary; an absent expected fact reds the over-strip.
    """
    idcfg = _identity_config(tmp_path / "meta")
    fields = _required_fields(
        **{"date-of-birth": "1986-03-14",
           "rx-interaction-classes": "atorvastatin 20mg",
           "phq2": _PHQ2_RAW_ANSWER,
           # A record-only field carrying the operator's legal name + race string (never a wired
           # token — a wired token would trip summarize's fail-closed 8j6 gate). It lands in the
           # gitignored scaffold; the crown jewel proves it never crosses to the planner / a request.
           "medical-history-note": f"{_FAKE_LEGAL_NAME}; {_RACE_STRING}"})
    backend = _drive_intake_and_care_review(tmp_path, fields=fields, backend=_RecordingCareBackend(),
                                            identity_config=idcfg)
    assert backend.clarifying_calls(), "the clarifying-review leg did not fire"
    assert backend.curation_calls(), "the leg-2 curation did not fire (the drug-name egress is untested)"

    payload = router.dispatch(router.summarize(_reader(tmp_path), identity_config=idcfg)).payload
    payload_text = json.dumps(payload)
    all_requests_text = json.dumps(backend.calls)
    non_curation_text = json.dumps(backend.clarifying_calls())

    # (a) operator IDENTITY: 0 in the payload + EVERY request (incl. curation).
    for surface_name, surface_text in (("dispatch payload", payload_text),
                                       ("all model requests", all_requests_text)):
        assert pii_scan.scan_text_full(surface_text, token_config=idcfg) == 0, (
            f"operator identity crossed into the {surface_name} (crown-jewel breach)"
        )
        assert _FAKE_LEGAL_NAME not in surface_text, f"a legal name crossed into the {surface_name}"
        assert _RACE_STRING not in surface_text, f"a race string crossed into the {surface_name}"
    # Non-vacuous: the scanner CAN count the identity token (the negative control).
    assert pii_scan.scan_text_full(payload_text + " " + _FAKE_LEGAL_NAME, token_config=idcfg) > 0, (
        "the identity probe could not count an injected identity token — it is vacuous"
    )

    # (b) the full DOB + the PHQ-2 raw answer: 0 in the payload + EVERY request. BOUNDARY NOTE: the
    #     full DOB is captured (as the named-excluded `date-of-birth` source) then DERIVED to the age
    #     — so its absence here guards the DISPATCH/de-id boundary. The PHQ-2 raw answer, by contrast,
    #     is DROPPED at capture (the safety region persists only the de-identified `safety-screen::phq2`
    #     / `referral::phq2` markers — the raw free-text is retained in NEITHER the store nor the
    #     scaffold), so its absence here guards the CAPTURE-RETENTION boundary (it can never reach the
    #     dispatch boundary because it never persists); this sub-assertion reds a capture-retention
    #     regression, not a dispatch-boundary one.
    for surface_name, surface_text in (("dispatch payload", payload_text),
                                       ("all model requests", all_requests_text)):
        assert "1986-03-14" not in surface_text, f"the full DOB crossed into the {surface_name}"
        assert _PHQ2_RAW_ANSWER not in surface_text, f"the PHQ-2 raw answer crossed into the {surface_name}"

    # (c) the raw drug: 0 in the dispatch payload + the clarifying (non-curation) requests; the leg-2
    #     curation MAY legitimately carry it (the sanctioned ADR-0035 drug-name egress class).
    assert "atorvastatin" not in payload_text, "a raw drug name crossed into the no-train dispatch payload"
    assert "atorvastatin" not in non_curation_text, (
        "a raw drug name crossed into the clarifying (planner-boundary) request"
    )

    # (d) the de-associated facts ARE present (not an over-strip): the EXACT integer age + the weight+trend.
    assert payload.get("training-age-band"), "the de-associated exact age is absent (over-strip)"
    assert str(payload["training-age-band"]).isdigit(), (
        f"training-age-band is not the de-associated integer age: {payload['training-age-band']!r}"
    )
    assert "1986-03-14" not in str(payload["training-age-band"]), "training-age-band leaked the full DOB"
    assert payload.get("bodyweight-band"), "the de-associated current weight+trend is absent (over-strip)"


def test_probe_sec_f1_my_info_edit_path_zero_raw_crossing_behavioral(tmp_path):
    """AC-3 / SEC-F1 (behavioral): a raw value driven THROUGH the My-Info edit `/upload` re-submit → 0 crossing.

    After the initial intake unlocks, drives a CHANGED full DOB `1990-07-22` THROUGH the My-Info edit
    form's `/upload` re-submit path (the same capture POST, T7's editable Demographics field — NOT the
    initial intake); re-builds `dispatch(summarize(store_read)).payload` + captures the re-fired model
    requests; asserts the changed full-DOB appears in the re-built payload + EVERY re-fired request 0
    times — the editable-My-Info no-bypass property proven BEHAVIORALLY end-to-end (the
    Security-reviewed companion to T7's W5 STRUCTURAL grep).

    VECTOR NOTE (T7 markup, verified 2026-07-01): the My-Info edit form exposes an EDITABLE
    Demographics `date-of-birth` field but renders Medications as a READ-ONLY note routing to
    Chat-with-Team (no editable meds field in My-Info). So the behavioral edit-path proof uses the
    CHANGED-full-DOB vector (which genuinely exercises T7's edit `/upload` seam), NOT a new-raw-drug
    vector (not exercisable through the My-Info edit form — that egress belongs to the T8 care-review
    curation seam, covered by the AC-3 crown-jewel + AC-5).
    """
    idcfg = _identity_config(tmp_path / "meta")
    # Initial intake unlocks; the initial DOB `1986-04-12` derives age 40.
    backend = _RecordingCareBackend()
    srv, port = _build(tmp_path, backend=backend, key_resolver=lambda: None, identity_config=idcfg)
    _serve_in_thread(srv)
    try:
        assert _post_fields(port, _required_fields(**{"date-of-birth": "1986-04-12"}))[0] == 200
        # Snapshot the de-associated age BEFORE the edit so the post-edit assertion below can prove
        # the edit was APPLIED, not silently no-op'd (locking out the vacuity the `.isdigit()`-only
        # check allowed — a no-op edit leaves the initial digit age in place and would pass).
        age_before = router.summarize(_reader(tmp_path), identity_config=idcfg)["training-age-band"]
        backend.calls.clear()  # isolate the re-fired requests from the initial intake's.
        # Drive the CHANGED full DOB `1990-07-22` (age 35) through the My-Info edit `/upload` re-submit.
        assert _post_fields(port, {"date-of-birth": "1990-07-22"})[0] == 200
    finally:
        srv.shutdown()
        srv.server_close()

    payload = router.dispatch(router.summarize(_reader(tmp_path), identity_config=idcfg)).payload
    payload_text = json.dumps(payload)
    refired_text = json.dumps(backend.calls)

    assert "1990-07-22" not in payload_text, (
        "the My-Info edit changed-DOB crossed into the no-train dispatch payload (SEC-F1 behavioral breach)"
    )
    assert "1990-07-22" not in refired_text, (
        "the My-Info edit changed-DOB crossed into a re-fired model request (SEC-F1 behavioral breach)"
    )
    # NON-VACUITY LOCK: the edit ACTUALLY took effect — the re-derived age CHANGED (40 → 35). Without
    # this, a no-op-edit regression (the `/upload` DOB edit silently dropped) would leave the initial
    # age in place and the changed-DOB "0-crossing" above would pass VACUOUSLY (the value was never
    # captured, so of course it never crosses). Asserting the age changed proves the raw DOB genuinely
    # flowed THROUGH the edit → capture → de-id path, so the 0-crossing is a real no-bypass proof.
    age_after = str(payload.get("training-age-band", ""))
    assert age_after.isdigit(), "the My-Info edit did not re-derive the de-associated age through the capture path"
    assert age_after != str(age_before), (
        f"the My-Info DOB edit did NOT re-derive the age ({age_before!r} unchanged) — the edit no-op'd, "
        f"so the changed-DOB 0-crossing above is VACUOUS (a no-bypass regression could hide here)"
    )
    assert age_after == "35", f"the 1990-07-22 edit derived age {age_after!r}, expected 35"


def test_probe_safety_positive_answer_referral_flag_never_a_plan_input(tmp_path):
    """AC-4 (SAFETY → REFERRAL, never a plan input): a positive answer flags referral; never a plan token.

    A POSITIVE exercise-safety (chest pain) + elevated PHQ-2 + positive apnea answer at intake →
    `referral.collate(store_read)` returns the `referral::<screen>` flags; a NEGATIVE answer set →
    NO flag (so the flag trips ONLY on a positive answer — the safety-bypass falsification). AND no
    `safety-screen::*` / `referral::*` item is a `SUMMARY_FIELD_SET` member: it is absent from
    `summarize`, and `dispatch` RAISES the out-of-field-set error if a `safety-screen::*` field is
    injected into a payload.
    """
    root_pos, root_neg = tmp_path / "pos", tmp_path / "neg"
    positive = _required_fields(**{"exercise-safety": "chest pain on exertion",
                                   "phq2": "yes, several days a week", "apnea": "yes"})
    for root, fields in ((root_pos, positive), (root_neg, _required_fields())):
        srv, port = _build(root)
        _serve_in_thread(srv)
        try:
            assert _post_fields(port, fields)[0] == 200
        finally:
            srv.shutdown()
            srv.server_close()

    # A positive answer → a referral flag per screen; a negative answer set → none.
    assert referral.collate(_reader(root_pos)) == ["exercise-safety", "phq2", "apnea"], (
        "a positive safety answer did not raise its referral flag (safety-bypass)"
    )
    assert referral.collate(_reader(root_neg)) == [], (
        "a negative safety answer set raised a referral flag (the flag is not answer-gated)"
    )

    # No safety marker is a plan input: absent from summarize, and dispatch rejects it if injected.
    summary = router.summarize(_reader(root_pos))
    for key in summary:
        assert not key.startswith("safety-screen::") and not key.startswith("referral::"), (
            f"a safety/referral marker {key!r} is a SUMMARY_FIELD_SET token (never-a-plan-input broken)"
        )
    poisoned = dict(summary)
    poisoned["safety-screen::phq2"] = "yes"
    with pytest.raises(ValueError):
        router.dispatch(poisoned)


def test_probe_serve_auto_classification_and_meds_curation_confirm_when_unsure(tmp_path):
    """AC-5 (serve-auto-classification + meds curation): 0 auto-classify at capture; confirm-when-unsure.

    Two legs:
    - Record-only: a raw med captured at intake → 0 `rx-interaction-classes` store writes from
      `persist_capture` (the record-only routing — the rejected ADR-0034 Alternative A); the raw med
      lands in the gitignored scaffold, NOT the model-bound token.
    - Confirm-when-unsure: the care-agent curation (mock, UNCERTAIN) surfaces the de-identified class
      token confirm-when-unsure and writes 0 `rx-interaction-classes` until the operator confirms (the
      rejected ADR-0035 Alternative C); only the CONFIRMED token then persists as a planner input.
    """
    # Leg 1 — record-only at capture (an incomplete profile so the care-review does not fire):
    root_ro = tmp_path / "ro"
    srv, port = _build(root_ro)  # _key_absent → care-review off
    _serve_in_thread(srv)
    try:
        assert _post_fields(port, {"rx-interaction-classes": "atorvastatin 20mg, metformin 500mg"})[0] == 200
    finally:
        srv.shutdown()
        srv.server_close()
    assert store.read("rx-interaction-classes", root=root_ro / "store") == [], (
        "a raw med auto-classified into the rx-interaction-classes store item at capture (serve-auto-classification)"
    )
    scaffold_text = "".join(p.read_text() for p in (root_ro / "scaffold").rglob("*") if p.is_file())
    assert "atorvastatin" in scaffold_text, "the raw med did not land record-only in the scaffold"

    # Leg 2 — confirm-when-unsure: an UNCERTAIN curation writes 0 until confirmed.
    root_cu = tmp_path / "cu"
    idcfg = _identity_config(tmp_path / "meta")
    backend = _drive_intake_and_care_review(
        root_cu, fields=_required_fields(**{"rx-interaction-classes": "atorvastatin 20mg"}),
        backend=_RecordingCareBackend(confident=False), identity_config=idcfg)
    assert backend.curation_calls(), "the uncertain-curation leg did not fire"
    assert store.read("rx-interaction-classes", root=root_cu / "store") == [], (
        "an UNCONFIRMED curated class persisted (confirm-when-unsure broken — the ADR-0035 Alt-C reject)"
    )
    # Only a CONFIRMED token persists as the planner input.
    care_review.confirm_curation(["cyp3a4-pgp"], store_root=root_cu / "store")
    confirmed = store.read("rx-interaction-classes", root=root_cu / "store")
    assert confirmed and confirmed[-1]["value"] == "cyp3a4-pgp", "the confirmed class token did not persist"
    payload = router.dispatch(router.summarize(_reader(root_cu), identity_config=idcfg)).payload
    assert payload["rx-interaction-classes"] == "cyp3a4-pgp", "the confirmed class is not the planner input"
    assert "atorvastatin" not in json.dumps(payload), "a raw drug string reached the dispatch payload"


# --------------------------------------------------------------------------- #
# Cycle 3 — EXTEND-NOT-REBUILD (frozen numstat + router scoped-additive)
# --------------------------------------------------------------------------- #


def _fork_point():
    """The dynamic fork-point (`git merge-base HEAD origin/main`) — never hardcoded."""
    return subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()


def test_probe_extend_not_rebuild_frozen_set_numstat_zero():
    """AC-6 (EXTEND-NOT-REBUILD): the 7 frozen plan-engine files + the frozen store spine — numstat 0.

    `git diff --numstat <fork-point> --` over the 7 byte-frozen `scripts/plan/*` engine files
    (orchestrate/pipeline/assemble/generate_plan/adjudicate/adjust/track) + the authoritative frozen
    store spine (`scripts/store/keying.py` + `scripts/store/store.py`, ADR-0032:107) emits 0 rows —
    the intake/onboarding slice RIDES the unchanged inner engine + store, it re-authors none.
    Falsifiable: a transient edit to any frozen file emits a row. Mirrors
    `tests/serve/test_route.py::test_frozen_engine_byte_unchanged`.

    Reconciled for ADR-0040 (large-change hold): the former whole-`scripts/store/*.py` glob is
    narrowed to the authoritative frozen store spine — it over-reached ADR-0032:107 and forbade the
    ADR-0040-sanctioned additive store surface (`scripts/store/plan_confirm.py`, the bounded
    `plan-confirm::` stream OQ-1 amending ADR-0038; and `read_plan`'s AR-007 read-side skip in
    `plan_schema.py`). keying.py + store.py stay byte-frozen.
    """
    store_paths = ("scripts/store/keying.py", "scripts/store/store.py")
    frozen = (*_FROZEN_ENGINE_PATHS, *store_paths)
    rows = subprocess.run(
        ["git", "diff", "--numstat", _fork_point(), "--", *frozen],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    changed = [line for line in rows.splitlines() if line.strip()]
    assert changed == [], f"a frozen plan-engine / store file was edited (EXTEND-NOT-REBUILD broken): {changed}"


def test_probe_router_scoped_additive_field_set_and_dispatch_byte_unchanged():
    """AC-6 (router scoped-additive): SUMMARY_FIELD_SET byte-identical + dispatch whitelist present + deletions capped.

    `router.py` is the sanctioned ADR-0032-T3 / T2 additive seam (NOT byte-frozen), but a NON-ADDITIVE
    rewrite of the de-id summary spine is the crown-jewel-spine regression this guard catches:
    - `router.SUMMARY_FIELD_SET` tuple membership is byte-identical to the pinned set.
    - The `dispatch` payload whitelist line `set(payload) <= set(SUMMARY_FIELD_SET)` is present unchanged.
    - `git diff --numstat <fork-point> -- router.py` deletions ≤ the T2-sanctioned cap (INSERTIONS
      unbounded, DELETIONS capped). Mirrors `test_route.py::test_router_additive_only_from_fork`.
    """
    assert router.SUMMARY_FIELD_SET == _PINNED_SUMMARY_FIELD_SET, (
        "router.SUMMARY_FIELD_SET membership changed (a non-additive de-id-spine rewrite)"
    )
    router_src = (REPO_ROOT / _ROUTER_ADDITIVE_PATH).read_text()
    assert "set(payload) <= set(SUMMARY_FIELD_SET)" in router_src, (
        "the dispatch payload whitelist line was deleted/altered (the crown-jewel gate)"
    )
    fields = subprocess.run(
        ["git", "diff", "--numstat", _fork_point(), "--", _ROUTER_ADDITIVE_PATH],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    deletions = int(fields[1]) if fields else 0
    assert deletions <= _ROUTER_SANCTIONED_DELETIONS, (
        f"router.py deleted {deletions} lines (> {_ROUTER_SANCTIONED_DELETIONS} sanctioned) — a "
        f"NON-ADDITIVE rewrite of the de-id summary spine (PF-S63-02 guard-loosening)"
    )
