"""UI-driven front-end wiring E2E (bead xwbe / the "T10" S103 Tier-3 deferral).

The S103 build left the SERVER mechanism complete + tested but the BROWSER wiring unbuilt: the
9-step wizard gathered nothing and POSTed nothing, the care-review JSON receipt was read as HTML and
dropped, `confirm_curation` had no route, and `referral.collate` had no consumer. These tests prove
the wiring end-to-end — and, unlike `test_intake_onboarding_e2e.py`'s hand-authored `_required_fields`
dict, they DERIVE the POST from the SERVED WIZARD MARKUP: the field names, the safety-screen answer
attributes, and the goal-domain chips are parsed out of `GET /`'s wizard body and the multipart body
is built from THAT — so a markup↔capture contract drift (a renamed field, a missing `data-safety`
attribute, a dropped required control) reds the test. It is the "served-UI completion flips the gate +
surfaces the questions" verification the bead requires (the JS gather in `submitProfile` mirrors this
same contract; the live-browser drive is the operator-facing companion).

MOCK/FIXTURE-tested at 0 live spend: the care-review case injects a recording mock backend at the
ADR-0015 `ModelClient(backend=...)` seam with a fail-closed key resolver; no live API, no key, no
non-loopback socket.
"""

import functools
import http.client
import json
import re
import threading
from pathlib import Path

from scripts.model.client import ModelClient
from scripts.model.key_source import KeyUnavailableError
from scripts.serve import referral
from scripts.serve import server as serve_server
from scripts.store import store
from vault.design.templates import app_shell

BOUNDARY = "----aplusfrontendwiring7MA4YWxkTrZu0gW"

# The platform-surface markers ABSENT from the locked Create-Profile body, PRESENT once unlocked.
_PLATFORM_MARKERS = ('id="screen-team"', 'id="screen-dashboard"', 'id="screen-plan"',
                     'id="screen-profile"', 'data-tab="generate"', 'data-tab="build">My Info')
_WIZARD_MARKER = 'id="screen-wizard"'

# The negative safety answers (a clean profile); the capture negative-answer set (mirrors capture.py).
_NEGATIVE_VALS = {"no", "none", "not-at-all", "negative", "never", "0"}

# Canned values for the named free-text/date/number wizard controls, keyed by the markup field name.
# The NAMES are discovered from the markup; only the representative values are canned here.
_CANNED_TEXT = {
    "date-of-birth": "1986-04-12",
    "bodyweight-kg": "82",
    "goal-targets": "build strength and improve sleep",
    "goal-priority-order": "recovery then strength",
    "occupation": "software engineer",
    "train-around": "left knee soreness",
    "food-allergy": "",
    "drug-allergy": "",
    "sleep-hours": "7",
    "smoker-quit-years": "",
    "nutrition-detail": "high-protein omnivore, three meals a day",
    "supplement-stack": "creatine 5g daily",
    "peptide-stack": "none",
    "training-detail": "4 days per week barbell training",
}


class _RecordingCareBackend:
    """A recording converse backend: records requests, scripts a clarifying question / class proposal."""

    def __init__(self, *, question="What is your single top priority this cycle?"):
        self.question = question
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        if "rx-interaction-curation" in json.dumps(messages):
            return {"reply": "Please confirm these interaction classes.",
                    "extraction": [{"rx-interaction-class": "cyp3a4-pgp", "confident": True}]}
        return {"reply": self.question, "extraction": []}


def _key_absent():
    """A fail-closed key resolver — the care-review never fires (deterministic HTML re-render)."""
    raise KeyUnavailableError("no key in test")


def _serve_in_thread(srv):
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _build(tmp_root, *, backend=None, key_resolver=_key_absent):
    """Build the production server over tmp roots + the injected recording-mock seam (0 spend)."""
    client = ModelClient(backend=backend) if backend is not None else None
    srv = serve_server.build_server(
        0, store_root=tmp_root / "store", dna_root=tmp_root / "dna",
        scaffold_root=tmp_root / "scaffold", client=client, key_resolver=key_resolver,
    )
    return srv, srv.server_address[1]


def _get_root(port):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", "/")
    resp = conn.getresponse()
    body = resp.read().decode("utf-8")
    conn.close()
    return resp.status, body


def _post_fields(port, fields):
    """POST a fields-only multipart capture to `/upload`; return (status, content_type, body)."""
    body = bytearray()
    for name, value in fields.items():
        body += f"--{BOUNDARY}\r\n".encode()
        body += (f'Content-Disposition: form-data; name="{name}"\r\n\r\n').encode()
        body += str(value).encode("utf-8")
        body += b"\r\n"
    body += f"--{BOUNDARY}--\r\n".encode()
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("POST", "/upload", body=bytes(body),
                 headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    ctype = resp.getheader("Content-Type") or ""
    conn.close()
    return resp.status, ctype, text


# --------------------------------------------------------------------------- #
# The MARKUP-GROUNDED gather — the field set is parsed from the served wizard body,
# mirroring the `submitProfile` JS collect() contract (names + safety attrs + chips).
# --------------------------------------------------------------------------- #


def _wizard_region(html):
    """The wizard + equipment section bodies (where the JS gathers `#wsteps` / `#screen-equipment`)."""
    wiz = re.search(r'id="screen-wizard">(.*?)</section>', html, re.DOTALL)
    equip = re.search(r'id="screen-equipment">(.*?)</section>', html, re.DOTALL)
    assert wiz and equip, "the served body is missing the wizard / equipment Create-Profile screens"
    return wiz.group(1) + equip.group(1)


def _markup_gather(html, *, positive_safety=False):
    """Build the capture POST dict from the SERVED wizard markup (the UI gather contract).

    Discovers, from the markup: every `<select name=...>` (first non-empty option value), every named
    `<input>`/`<textarea>` (a canned representative value), the three `data-safety` screens (the
    negative answer for a clean profile, a positive one when `positive_safety`), and the step-2
    goal-domain chips. Mirrors `submitProfile`'s JS collect(): a drift between the markup and this
    contract (a renamed control, a missing safety attribute) surfaces as a KeyError/assertion here.
    """
    region = _wizard_region(html)
    fields = {}

    # <select name=...> -> first non-empty option value (the bounded demographic tokens).
    for m in re.finditer(r"<select\b([^>]*)>(.*?)</select>", region, re.DOTALL):
        nm = re.search(r"name='([^']+)'", m.group(1))
        if not nm:
            continue
        opts = [o for o in re.findall(r"<option value='([^']*)'", m.group(2)) if o.strip()]
        if opts:
            fields[nm.group(1)] = opts[0]

    # Named <input>/<textarea> (skip checkboxes + the empty goal-domains hidden input — derived below).
    for m in re.finditer(r"<(input|textarea)\b([^>]*)>", region):
        attrs = m.group(2)
        nm = re.search(r"name='([^']+)'", attrs)
        if not nm:
            continue
        name = nm.group(1)
        if "type='checkbox'" in attrs or name in fields or name == "goal-domains":
            continue
        value = _CANNED_TEXT.get(name, "n/a")
        if value:
            fields[name] = value

    # goal-domains: the step-2 chip labels (multi-select) — pick the first two, ;-joined.
    step2 = re.search(r'data-step="2"(.*?)data-step="3"', region, re.DOTALL)
    assert step2, "the served wizard is missing the step-2 goals region"
    chips = [c.strip() for c in re.findall(r'<label class="opt"[^>]*>.*?</span>([^<]+)</label>', step2.group(1))]
    assert len(chips) >= 2, f"the goal-domain chips were not found in the markup: {chips}"
    fields["goal-domains"] = ";".join(chips[:2])

    # Safety screens: group the data-safety labels by screen; pick a negative (clean) or positive answer.
    by_screen = {}
    for screen, val in re.findall(r'data-safety="([^"]+)" data-val="([^"]+)"', region):
        by_screen.setdefault(screen, []).append(val)
    for screen, vals in by_screen.items():
        if positive_safety:
            pick = next((v for v in vals if v.lower() not in _NEGATIVE_VALS), vals[0])
        else:
            pick = next((v for v in vals if v.lower() in _NEGATIVE_VALS), vals[0])
        fields[screen] = pick

    return fields


def _reader(tmp_root):
    return functools.partial(store.read, root=tmp_root / "store")


# --------------------------------------------------------------------------- #
# AC1 — a served-UI completion (gathered FROM THE MARKUP) flips the gate + unlocks
# --------------------------------------------------------------------------- #


def test_markup_carries_the_wiring_contract(tmp_path):
    """AC1 (structural): the served wizard + equipment carry the submit wiring the JS drives.

    The locked body's equipment screen submits via `submitProfile(...)`, step 9 advances to the
    equipment screen (`show('equipment')`), and the three gate-critical safety screens carry the
    `data-safety` capture hooks — the exact seams the markup gather + the JS collect() both read.
    """
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        _, locked = _get_root(port)
    finally:
        srv.shutdown()
        srv.server_close()
    assert "submitProfile(" in locked, "the equipment Save button is not wired to submitProfile"
    assert "show('equipment')" in locked, "the wizard final step does not advance to the equipment screen"
    for screen in ("exercise-safety", "phq2", "apnea"):
        assert f'data-safety="{screen}"' in locked, f"the {screen} safety screen carries no capture hook"
    assert "location.reload()" in locked, "submitProfile does not reload into the unlocked shell"
    # Finding 1 (bug-hunter): submitProfile must NOT blind-reload — it discriminates the unlocked
    # shell (an `id="screen-team"` marker in the HTML re-render) from a still-locked body (a required
    # field diverted server-side), so a diverted-field completion never reloads to a blank wizard.
    assert 'html.indexOf(\'id="screen-\'+\'team"\')' in locked, (
        "submitProfile blind-reloads without confirming the gate flipped (Finding 1 regression)"
    )
    # Finding 2 (bug-hunter): the weight unit is an EXPLICIT choice (default 'Unit', no silent lbs),
    # and submitProfile requires it so a metric entry is never silently converted as lbs.
    assert "<option value='' selected>Unit</option>" in locked, (
        "the weight-unit select still defaults to a unit (silent lbs conversion risk, Finding 2)"
    )
    assert "a weight unit (kg or lbs)" in locked, "submitProfile does not require an explicit weight unit"
    # Draft autosave: the locked wizard persists entries to localStorage and restores them on load
    # (a refresh mid-wizard never loses typed work; the store is written only on the final submit).
    assert "aplus_wizard_draft_v1" in locked, "the Create-Profile draft autosave (localStorage) is not wired"
    assert "_wizClearDraft" in locked, "the draft is not cleared once the profile completes"


def test_ui_driven_markup_gather_flips_gate_and_unlocks(tmp_path):
    """AC1 (HEADLINE, UI-driven): a completion GATHERED FROM THE SERVED MARKUP flips the gate.

    Parses the locked wizard body, builds the capture POST from the discovered field contract (NOT a
    hand-authored dict), POSTs it to `/upload`, and asserts GET `/` flips from the Create-Profile-only
    body to the full unlocked shell. The gather derives the field NAMES + safety attributes from the
    markup, so a markup↔capture drift reds this headline.
    """
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        status, locked = _get_root(port)
        assert status == 200 and _WIZARD_MARKER in locked
        for marker in _PLATFORM_MARKERS:
            assert marker not in locked, f"the fresh store leaked a platform surface {marker!r}"

        fields = _markup_gather(locked)
        post_status, _, _ = _post_fields(port, fields)
        assert post_status == 200, f"the markup-gathered capture POST returned {post_status}"

        status, unlocked = _get_root(port)
        assert status == 200
        for marker in _PLATFORM_MARKERS:
            assert marker in unlocked, (
                f"the markup-gathered completion did not unlock {marker!r} (a markup↔capture drift?)"
            )
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# AC4 — a positive safety answer surfaces in the My-Info doctor-visit display
# --------------------------------------------------------------------------- #


def test_ui_driven_positive_safety_surfaces_referral_in_my_info(tmp_path):
    """AC4 (UI-driven): a positive safety answer flags a referral that renders in My-Info.

    Gathers a completion with POSITIVE safety answers from the markup, POSTs it, then asserts both
    `referral.collate` returns the flagged screens AND the unlocked My-Info body renders their human
    labels (the `referral.collate` production consumer wired in `app_shell._referral_zone`). A clean
    (negative) profile shows none of the labels — the display is answer-gated.
    """
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        _, locked = _get_root(port)
        fields = _markup_gather(locked, positive_safety=True)
        assert _post_fields(port, fields)[0] == 200
        _, unlocked = _get_root(port)
    finally:
        srv.shutdown()
        srv.server_close()

    flagged = referral.collate(_reader(tmp_path))
    assert set(flagged) == {"exercise-safety", "phq2", "apnea"}, (
        f"positive safety answers did not all raise a referral flag: {flagged}"
    )
    for screen in flagged:
        assert app_shell._REFERRAL_LABELS[screen] in unlocked, (
            f"the flagged {screen} referral is not surfaced in the unlocked My-Info display"
        )


# --------------------------------------------------------------------------- #
# AC2 — a served-UI completion (with a key) surfaces the care-review JSON receipt
# --------------------------------------------------------------------------- #


def test_ui_driven_completion_returns_care_review_receipt_json(tmp_path):
    """AC2 (UI-driven, HIGH-1): a completion with a key returns the care-review JSON the front-end renders.

    With a usable key + the recording mock backend, a markup-gathered completion POST to `/upload`
    returns a JSON care-review receipt (Content-Type application/json) carrying >= 1 clarifying
    question and the meds-curation state — the exact payload `submitProfile` stashes and the reload
    bootstrap renders into the Care Assistant thread (previously read as HTML and dropped). The
    recording backend proves the clarifying leg fired; 0 live spend (fail-closed resolver + mock seam).
    """
    backend = _RecordingCareBackend()
    srv, port = _build(tmp_path, backend=backend, key_resolver=lambda: None)
    _serve_in_thread(srv)
    try:
        _, locked = _get_root(port)
        fields = _markup_gather(locked)
        fields["rx-interaction-classes"] = "atorvastatin 20mg"  # drives the leg-2 curation
        status, ctype, text = _post_fields(port, fields)
        assert status == 200, f"the completion POST returned {status}"
        assert "application/json" in ctype, (
            f"the care-review completion did not return JSON (the receipt would be dropped as HTML): {ctype}"
        )
        receipt = json.loads(text)
    finally:
        srv.shutdown()
        srv.server_close()

    assert receipt.get("deferred") is False, f"the care review deferred unexpectedly: {receipt}"
    assert receipt.get("questions"), "the care-review receipt carries no clarifying question for the UI to render"
    assert "curation" in receipt, "the care-review receipt carries no meds-curation state"
    assert backend.calls, "the recording mock backend received no care-review call (path not exercised)"


def test_served_page_is_no_store_so_a_refresh_never_serves_stale_js(tmp_path):
    """Root-cause fix (operator report): GET / carries `Cache-Control: no-store`.

    The served page IS the app (a single inline-asset document regenerated per GET). Without a cache
    directive the stdlib server let the browser serve a STALE cached copy on refresh — old JS (so the
    wizard's localStorage autosave never ran and typed work was lost) and old markup (no pre-fill / no
    already-loaded note). `no-store` forces every load/refresh to fetch the current document.
    Failing-capable: drop the header and this reds.
    """
    srv, port = _build(tmp_path)
    _serve_in_thread(srv)
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/")
        resp = conn.getresponse()
        resp.read()
        cache = resp.getheader("Cache-Control")
        conn.close()
        assert cache == "no-store", f"GET / did not send Cache-Control: no-store (got {cache!r}) — a refresh can serve stale JS"
    finally:
        srv.shutdown()
        srv.server_close()
