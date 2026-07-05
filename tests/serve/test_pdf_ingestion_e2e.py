"""End-to-end PDF-ingestion proof + the ADR-0031 falsification probes (ADR-0031-T6).

This is the terminal Wave-3 integration gate: a synthetic PDF upload produces an
operator-CONFIRMED LANDED reading through the SERVED `/upload` -> `/confirm-extraction`
path, with the raw PDF binary proven to stay LOCAL (the model receives extracted TEXT
only). It composes the already-built local-extract-first chain end-to-end — this task
adds NO production code:

    synthetic fixture PDF
      -> POST /upload (multipart)
      -> route.route_upload's `application/pdf` branch (ADR-0031-T4)
      -> pdf_extract.extract_text LOCAL extraction (ADR-0031-T1; STUBBED for the
         always-runs forms, REAL pdftotext for the `skipif`-gated form) — the raw
         bytes reach ONLY the local subprocess, never the model
      -> extract_chunked.extract_all chunk + aggregate + dedupe + honest-partial
         signal (ADR-0031-T2)
      -> client.extract_readings(chunk, "text/plain") (the no-train TEXT lane; MOCKED
         at the ADR-0015 ModelClient(backend=...) seam — no live API, no key, 0 spend)
      -> the /upload JSON review payload `{"readings", "partial", "notes"}` (ADR-0031-T4;
         lands 0; the F1 fold-in surfaces partial:true even when readings == [])
      -> POST /confirm-extraction `{"readings": [...]}` (Content-Type: application/json,
         the CSRF gate) -> confirm.land_confirmed -> the UNCHANGED ingest.manual_entry/
         store.append
      -> a LANDED confirmed reading, readable via store.read_all.

Two load-bearing test properties:
  (a) NON-TAUTOLOGICAL: the headline asserts the landed `store.read_all` readings TRACE to
      the fixture's confirmed `(item, value)` (the confirmed fixture subset EQUALS the
      landed readings), and a DIFFERENT fixture -> DIFFERENT landed readings — proving the
      landed data is the mock's parse, never a hardcoded constant. A failing-capable negative
      control proves the headline goes RED on the honest no-data state; it NEVER asserts
      merely "the store is non-empty".
  (b) MOCK-TESTABLE: the model client is a fixture backend injected at the ADR-0015 seam and
      the local extractor is stubbed (the always-runs forms) / runs real pdftotext (the
      skipif form) with `marker` never really run — so the run is deterministic + CI-runnable
      with no network, no key, 0 spend.

QA-2 5-vs-1 distinction (load-bearing). The CANONICAL six ADR-0031 falsification probes are
{raw-binary-egress, local-extractor-network, extend-not-rebuild, completeness/
no-silent-truncation, confirm-gate, key-never-committed}. FIVE of those six are per-test IN
this file:
  - raw-binary-egress      -> test_probe_crown_jewel_raw_binary_egress_text_lane_only
                              + test_probe_serve_and_ingest_layers_import_no_outbound_client
  - local-extractor-network-> test_probe_local_extractor_network_zero
  - extend-not-rebuild     -> test_probe_extend_not_rebuild_frozen_set_numstat_zero
  - completeness           -> test_probe_completeness_multichunk_union_deduped_lands_all
                              + test_probe_honest_partial_signal_not_silent_empty
  - confirm-gate           -> test_confirm_gate_store_empty_until_confirm
The SIXTH — key-never-committed — is NOT a per-test AC here: it is the repo-wide release gate
carried by the `block-pii-commit` / `pre-push` hooks (grep every tracked file + git history on
a fresh clone for the API-key value; threshold 0), re-run at release. This file does NOT claim
all six are per-test. The recipe additionally names a fail-closed/no-fabrication probe (NFR-4)
and the genetics non-tautology A!=B probe (AC-5) as failing-capable per-tests.

LIVE run (operator-gated, NOT a CI gate). The operator-present real-key + real-42-page-
genetics-report + real-spend run end-to-end through local-extract -> chunk -> confirm -> land
(the OS-egress-guard LIVE form of the raw-binary-egress + local-extractor-network probes) is
OQ-1, the build's final operator-present finish line — out of plan scope, NOT a `skipif`
variant collected here.
"""

import http.client
import json
import shutil
import subprocess
import threading
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest

from scripts.ingest import extract_chunked, pdf_extract
from scripts.model.client import ModelCallError, ModelClient
from scripts.serve import server as serve_server
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

BOUNDARY = "----aplusboundary7MA4YWxkTrZu0gW"

# The serve-layer outbound-client markers the crown-jewel static grep forbids (mirrors
# tests/serve/test_serve_no_egress.py::test_serve_layer_imports_no_outbound_client).
_OUTBOUND_CLIENT_MARKERS = (
    "socket.create_connection",
    "urllib.request",
    "http.client",
    "requests",
    "httpx",
)

# The byte-frozen set the EXTEND-NOT-REBUILD numstat probe binds — mirrors
# tests/serve/test_route.py::_FROZEN_ENGINE_PATHS, EXTENDED with keying.py + store.py (the
# genetics readings land via the UNCHANGED sink, never re-authoring it).
# ADR-0032-T3 sanctioned exception: scripts/plan/router.py is the NAMED additive seam for the
# de-identified `genetic-trait-classes` token (the DNA-aware planning build). The INNER engine
# modules (orchestrate/pipeline/assemble/generate_plan/adjudicate/adjust/track) stay byte-frozen;
# router.py is excluded from this frozen glob because T3 legitimately EXTENDS it. This is the
# "update the earlier E2E when a later phase changes the expected behavior" mandate, mirroring
# test_route.py::_FROZEN_ENGINE_PATHS. See docs/adr/ADR-0032 + tests/plan/test_router.py.
_FROZEN_ENGINE_PATHS = (
    "scripts/ingest/ingest.py",
    "scripts/ingest/adapter.py",
    "scripts/store/keying.py",
    "scripts/store/store.py",
    *sorted(
        str(p.relative_to(REPO_ROOT))
        for p in (REPO_ROOT / "scripts" / "plan").glob("*.py")
        if p.name not in ("router.py", "horizons.py", "tailoring.py")  # router.py (de-id summary spine) guarded by test_router_additive_only_from_fork; horizons.py is a NEW post-ADR-0032 read-layer feature module (ADR-0038-T1..T3), NOT crown-jewel spine — its invariants (single progress site, no new store stream, peptides-untracked, no fabricated deadline) are guarded by tests/plan/test_horizons.py, which catches the insertion-shaped regressions a numstat additive-guard would miss. Architect ruling, feature/dyn-loop-w2. tailoring.py (ADR-0037 care-lane tailoring) is a NEW post-ADR-0032 crown-jewel module (raw _care_profile egress + T2 safety gates), extended T1/T2/T3 so byte-freeze is impossible; it carries a DUAL risk shape with BOTH guarantors — its INSERTION-shape egress risk is guarded behaviorally by tests/plan/test_tailoring.py (T1 AC-4 static-scan; T3 AC-2/AC-3 wire-scan/artifact-only), its DELETION-shape safety-gate-removal risk by test_tailoring_additive_only_from_fork (PROSPECTIVE — vacuous until tailoring.py is on main, since a new-since-fork file reports 0 deletions vs the fork). Architect ruling, feature/dyn-loop-w5, 3rd carve-out.
    ),
)

# HIST1 / PF-S63-02: router.py is excluded from the byte-frozen set above because
# ADR-0032-T3 legitimately EXTENDS it — but a WHOLESALE exclusion would let a future
# NON-ADDITIVE rewrite of router.py's existing ~600 lines (the de-id summary spine, a
# crown-jewel gate) pass CI silently. The additive-only guard below names that failure
# class and still protects router.py: DELETIONS are capped at the sanctioned ADR-0032-T3
# count (the `summarize` signature reflow + the removed redundant function-local
# `import re`, QUAL1 = 2), while INSERTIONS stay unbounded.
_ROUTER_ADDITIVE_PATH = "scripts/plan/router.py"
# ADR-0033-0035-T2 / ADR-0034 OQ-5: the sanctioned _age_band born-decade→exact-age deriver-body
# repurpose deletes 14 lines; the de-id spine (SUMMARY_FIELD_SET tuple + dispatch whitelist +
# tripwires) is byte-frozen — verified by AC-7's scoped-diff. Re-calibrated 2→14 (as it was 2
# for ADR-0032-T3), keeping the tight tripwire against a non-additive spine rewrite.
_ROUTER_SANCTIONED_DELETIONS = 14

# Synthetic fixture readings — distinct items/timepoints/values so the latest-wins
# (item, timepoint, source) store identity never collapses two, and so fixture A and B yield
# provably DIFFERENT landed sets (the non-constant proof). Each carries the full
# keying.LINE_FIELDS set so confirm.land_confirmed's all-or-nothing conformance check passes.
READINGS_A = (
    {"item": "ferritin", "timepoint": "2026-05-01", "source": "labreport", "value": "120"},
    {"item": "vitamin_d", "timepoint": "2026-05-01", "source": "labreport", "value": "44"},
)
READINGS_B = (
    {"item": "glucose_fasting", "timepoint": "2026-05-02", "source": "labreport", "value": "92"},
    {"item": "hdl", "timepoint": "2026-05-02", "source": "labreport", "value": "58"},
)

# Genetics genotype-fact fixtures (the AC-5 / T3 cross-check): item = gene + rsID,
# source = "dna-report", value = the allele call — the durable fact, not the interpretation.
GENETICS_A = (
    {"item": "MTNR1B rs10830963", "timepoint": "2026-04-01", "source": "dna-report", "value": "(C;G)"},
    {"item": "TCF7L2 rs7903146", "timepoint": "2026-04-01", "source": "dna-report", "value": "(C;T)"},
)
GENETICS_B = (
    {"item": "APOE rs429358", "timepoint": "2026-04-02", "source": "dna-report", "value": "(T;T)"},
)

# Synthetic extracted-text the stubbed local extractor returns for the always-runs forms — it
# carries NO raw-binary token (the raw token lives only in the PDF binary, never the text).
_EXTRACTED_TEXT_A = "Ferritin 120 ng/mL on 2026-05-01\nVitamin D 44 ng/mL on 2026-05-01\n"

# A base reading every chunk's mock returns in the completeness probe, so no chunk ever returns
# [] (which fail-closes the lane); it appears in every chunk yet lands ONCE (the dedupe proof).
_BASE_READING = {"item": "panel_header", "timepoint": "2026-04-01", "source": "labreport", "value": "1"}


# --------------------------------------------------------------------------- #
# Fixture backends + the synthetic-PDF builder + the served-E2E helpers
# --------------------------------------------------------------------------- #


class _FixtureBackend:
    """A mock extract backend: records every call, returns scripted readings.

    Injected at the ADR-0015 `ModelClient(backend=...)` seam so the E2E exercises the REAL
    served /upload -> PDF local-extract branch -> chunk -> /confirm-extraction -> land path
    with only the model backend mocked (no live API, no key). `extract_calls` records every
    `(content, media_type)` so the crown-jewel probe can prove the model lane received only
    text/plain and never the raw bytes.

    Attributes:
        readings (tuple): The scripted Line-Field-Set readings each call returns.
        extract_calls (list): The recorded `(content, media_type)` of every call.
    """

    def __init__(self, readings):
        self.readings = readings
        self.extract_calls = []

    def extract_readings(self, file_content, media_type):
        self.extract_calls.append((file_content, media_type))
        return [dict(r) for r in self.readings]


class _MarkerBackend:
    """A content-driven mock: returns a base reading plus one reading per marker in the chunk.

    The completeness probe needs a DISTINCT reading per chunk to prove the cross-chunk union
    lands deduped. Each chunk yields `_BASE_READING` (so no chunk ever returns [] -> the lane
    never fail-closes) plus a distinct reading for every marker present in that chunk. The base
    appears in every chunk but lands once (0 duplicate); every marker lands (0 dropped).

    Attributes:
        markers (list): The per-section marker tokens.
        extract_calls (list): The recorded `(content, media_type)` of every call.
    """

    def __init__(self, markers):
        self.markers = markers
        self.extract_calls = []

    def extract_readings(self, file_content, media_type):
        self.extract_calls.append((file_content, media_type))
        text = file_content if isinstance(file_content, str) else str(file_content)
        out = [dict(_BASE_READING)]
        for marker in self.markers:
            if marker in text:
                out.append(_marker_reading(marker))
        return out


class _RaisingBackend:
    """A mock extract backend that fail-closes every chunk call with `ModelCallError`."""

    def __init__(self):
        self.extract_calls = []

    def extract_readings(self, file_content, media_type):
        self.extract_calls.append((file_content, media_type))
        raise ModelCallError("synthetic chunk extraction failure")


def _marker_reading(marker):
    """Return the distinct conformant reading a section marker maps to."""
    return {"item": f"snp_{marker}", "timepoint": "2026-04-01", "source": "labreport", "value": marker}


def _make_text_pdf(text):
    """Build a minimal single-page text-layer PDF whose only page text is `text`.

    Deterministic, no PII, no third-party library — pdftotext extracts `text` verbatim. Mirrors
    T1's `tests/ingest/test_pdf_extract.py::_make_text_pdf` (the hand-built synthetic fixture).

    Args:
        text (str): The latin-1-encodable synthetic page text to embed.
    """
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    content = ("BT /F1 12 Tf 72 700 Td (" + escaped + ") Tj ET").encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += (str(index) + " 0 obj\n").encode() + obj + b"\nendobj\n"
    xref_offset = len(pdf)
    count = len(objects) + 1
    pdf += ("xref\n0 " + str(count) + "\n").encode()
    pdf += b"0000000000 65535 f \n"
    for offset in offsets:
        pdf += (("%010d" % offset) + " 00000 n \n").encode()
    pdf += (
        "trailer\n<< /Size " + str(count) + " /Root 1 0 R >>\nstartxref\n"
        + str(xref_offset) + "\n%%EOF\n"
    ).encode()
    return bytes(pdf)


def _pdf_bytes(token=None, page_text="SYNTHETIC GENETICS REPORT no-PII"):
    """Return synthetic `report.pdf` bytes; with `token`, seed it into the raw binary only.

    The page text never carries the token (so a real pdftotext extraction is token-free); the
    token, when given, is appended into the raw PDF binary AFTER `%%EOF`, where it survives only
    in the binary structure — the seed the crown-jewel / OQ-3 probes prove reaches no model call
    and no sink (the local extractor is stubbed in those probes, so the bytes are read only by
    the staged-temp -> stub path).
    """
    pdf = _make_text_pdf(page_text)
    if token:
        pdf = pdf + b"\n%% RAWBINARYONLY " + token.encode() + b"\n"
    return pdf


def _multichunk_text(markers):
    """Build extracted text that splits into >= len(markers) chunks, one marker per section.

    Each marker heads a section whose filler body is ~`extract_chunked._CHUNK_CHARS`, so two full
    sections never fit in one chunk and `len(markers)` markers yield >= `len(markers)` chunks (with
    headroom under `_MAX_CHUNKS`, so the upload reports `partial: false`). Sized RELATIVE to the
    imported `extract_chunked._CHUNK_CHARS` (NFR-7) — never a hardcoded char count, so the fixtures
    survive any OQ-2 retuning of the chunk constants.
    """
    filler = "filler line text. " * (extract_chunked._CHUNK_CHARS // len("filler line text. "))
    return "".join(marker + "\n" + filler + "\n" for marker in markers)


def _over_budget_text():
    """Build extracted text that splits into > extract_chunked._MAX_CHUNKS chunks (partial).

    Each section's body exceeds `extract_chunked._CHUNK_CHARS`, so `_MAX_CHUNKS + 1` sections force
    the split past the `_MAX_CHUNKS` budget and the honest-partial signal trips. Sized RELATIVE to
    the imported constants (NFR-7) — never a hardcoded char count.
    """
    body = "x" * (extract_chunked._CHUNK_CHARS + 1)
    return "".join(
        "section" + str(i) + "\n" + body + "\n" for i in range(extract_chunked._MAX_CHUNKS + 1)
    )


def _raw_token():
    """Return a per-run-unique raw-binary token (NOT a tracked literal).

    Generated at runtime so it appears in NO tracked file by construction — the residue scan
    for this token is a true 0-hit guard, not a self-match against this test's source.
    """
    return f"APLUS_E2E_RAWTOKEN_{uuid.uuid4().hex}"


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


@contextmanager
def _running_server(root_base, backend):
    """Yield the loopback port of a running server over tmp roots + the mock client.

    Binds an EPHEMERAL loopback port (`build_server(0)`) over tmp store/dna/scaffold roots under
    `root_base` and a `ModelClient` over `backend`, so the E2E never touches the real vault and
    never makes a live API call. Shuts the listener down cleanly on exit.
    """
    srv = serve_server.build_server(
        0,
        store_root=root_base / "store",
        dna_root=root_base / "dna",
        scaffold_root=root_base / "scaffold",
        client=ModelClient(backend=backend),
    )
    _serve_in_thread(srv)
    try:
        yield srv.server_address[1]
    finally:
        srv.shutdown()
        srv.server_close()


def _multipart_upload(filename, payload):
    """Build a single-file multipart/form-data body for the `export` field."""
    out = bytearray()
    out += f"--{BOUNDARY}\r\n".encode()
    out += (f'Content-Disposition: form-data; name="export"; filename="{filename}"\r\n\r\n').encode()
    out += payload
    out += b"\r\n"
    out += f"--{BOUNDARY}--\r\n".encode()
    return bytes(out)


def _post_upload(port, filename, payload):
    """POST a multipart file to `/upload`; return (status, base_content_type, parsed-or-raw body).

    The body is the parsed JSON review payload when the response is application/json (a PDF
    upload that surfaced readings or the honest-partial signal), else the raw HTML text (the
    honest no-data / fail-closed re-render). Returning the content-type lets a caller distinguish
    the two without guessing.
    """
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = _multipart_upload(filename, payload)
    conn.request(
        "POST", "/upload", body=body,
        headers={"Content-Type": f"multipart/form-data; boundary={BOUNDARY}"},
    )
    resp = conn.getresponse()
    ctype = (resp.getheader("Content-Type") or "").split(";", 1)[0].strip().lower()
    text = resp.read().decode("utf-8")
    conn.close()
    if ctype == "application/json":
        return resp.status, ctype, json.loads(text)
    return resp.status, ctype, text


def _post_confirm(port, readings):
    """POST the operator-confirmed subset to `/confirm-extraction`; return (status, parsed body).

    Sends `{"readings": [...]}` with `Content-Type: application/json` — the CSRF gate the route
    requires (a text/plain POST is rejected 415 before the body is parsed).
    """
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = json.dumps({"readings": readings}).encode("utf-8")
    conn.request(
        "POST", "/confirm-extraction", body=body,
        headers={"Content-Type": "application/json"},
    )
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, json.loads(text)


def _tuples(readings):
    """Order-independent set of (item, timepoint, source, value) tuples — the BARE landed readings.

    Excludes the additive `biomarker::` trend-feed mirror `confirm.land_confirmed` writes for a
    registered-polarity marker (the dead-feed fix): that mirror is a derived trend copy of a
    confirmed reading, not a distinct confirmed reading, so it is filtered from this equality.
    """
    return {
        (r["item"], r["timepoint"], r["source"], r["value"])
        for r in readings if not r["item"].startswith("biomarker::")
    }


def _offered_readings(ctype, body):
    """Return the readings the /upload response offered for review (empty for the no-data state)."""
    if ctype == "application/json" and isinstance(body, dict):
        return body.get("readings", [])
    return []


def _gitignore_dropzones():
    """Return the raw-data dropzone prefixes from .gitignore (the residue-scan exemption set).

    Reads the block under the "raw personal data dropzones" comment — the `vault/...` prefixes
    git ignores — so the exemption is derived from .gitignore, never a hardcoded path list.
    """
    lines = (REPO_ROOT / ".gitignore").read_text().splitlines()
    prefixes = []
    collecting = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            collecting = "raw personal data dropzones" in stripped
            continue
        if collecting and stripped.startswith("vault/"):
            prefixes.append(stripped)
    return prefixes


def _is_gitignored(prefix):
    """Return True if `prefix` is genuinely git-ignored (the exemption is real, not assumed)."""
    probe = prefix.rstrip("/") + "/probe"
    result = subprocess.run(["git", "check-ignore", "-q", probe], cwd=REPO_ROOT)
    return result.returncode == 0


# --------------------------------------------------------------------------- #
# Cycle 1 — the headline non-tautological land + negative control + confirm-gate + mock-tested
#   AC-1, AC-2, AC-6 (confirm-gate), AC-8
# --------------------------------------------------------------------------- #


def test_headline_pdf_local_extract_chunk_confirm_lands_traced_reading(tmp_path, monkeypatch):
    """AC-1 (headline, NON-TAUTOLOGICAL): a synthetic PDF -> /upload PDF local-extract ->
    /confirm-extraction lands a reading that TRACES to the fixture.

    The always-runs, pdf_extract-STUBBED form: the local extractor returns synthetic TEXT (no
    raw-binary token); the mock backend at the ADR-0015 seam returns scripted Line-Field-Set
    readings. The landed `store.read_all` readings EQUAL the confirmed fixture subset (the
    fixture's `(item, value)` appear in the store) and the confirm receipt RECORDS the land —
    never merely "the store is non-empty". Woven AC-6 confirm-gate: the store is empty
    immediately after /upload and BEFORE /confirm-extraction.
    """
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes(_raw_token()))
        assert status == 200
        assert ctype == "application/json", "a PDF upload surfaces a JSON review payload"
        offered = body["readings"]
        assert _tuples(offered) == _tuples(READINGS_A)
        # AC-6 confirm-gate: nothing has landed before the confirm POST.
        assert store.read_all(tmp_path / "store") == []

        cstatus, cbody = _post_confirm(port, offered)
        assert cstatus == 200
        # recorded == True: the confirm receipt lists the landed item tokens.
        assert set(cbody["landed"]) == {r["item"] for r in READINGS_A}

        landed = store.read_all(tmp_path / "store")
    # Content-traceable: the landed readings EQUAL the confirmed fixture subset.
    assert _tuples(landed) == _tuples(READINGS_A)
    assert {(r["item"], r["value"]) for r in landed if not r["item"].startswith("biomarker::")} == {
        (r["item"], r["value"]) for r in READINGS_A}
    # The raw PDF stayed local: the model lane received only text/plain chunks.
    assert backend.extract_calls
    assert all(mt == "text/plain" for _c, mt in backend.extract_calls)


@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="poppler/pdftotext not installed")
def test_headline_real_pdftotext_pdf_upload_lands_traced_reading(tmp_path):
    """AC-1 (real-pdftotext form): a real fixture PDF flows through the REAL local subprocess.

    Builds a synthetic single-page text-layer PDF (no PII), drives it through the REAL
    `pdf_extract.extract_text` (NOT stubbed) -> chunk -> the mock backend -> confirm -> land.
    The page text genuinely reaching the mock as a text/plain chunk proves the local subprocess
    ran; the landed readings trace to the fixture subset.
    """
    page_text = "Ferritin reading 120 ng/mL sample 2026-05-01 cohort fixture"
    pdf = _make_text_pdf(page_text)
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", pdf)
        assert status == 200 and ctype == "application/json"
        _post_confirm(port, body["readings"])
        landed = store.read_all(tmp_path / "store")
    assert _tuples(landed) == _tuples(READINGS_A)
    assert backend.extract_calls
    assert all(mt == "text/plain" for _c, mt in backend.extract_calls)
    # The chunk the mock received is the real pdftotext output (carries the page text) — the
    # local subprocess genuinely extracted the text (not a constant / not stubbed).
    received = " ".join(str(c) for c, _mt in backend.extract_calls)
    assert "Ferritin" in received, "real pdftotext did not feed the extracted text to the chunker"


def test_different_fixture_yields_different_landed_readings(tmp_path, monkeypatch):
    """AC-1 (non-constant): a DIFFERENT fixture -> DIFFERENT landed readings (B != A).

    Proves the landed readings are the mock's parse of the fixture, not a hardcoded constant —
    a constant mechanism would land the same readings for both fixtures.
    """
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)

    backend_a = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path / "a", backend_a) as port:
        _status, _ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        _post_confirm(port, body["readings"])
        landed_a = store.read_all(tmp_path / "a" / "store")

    backend_b = _FixtureBackend(READINGS_B)
    with _running_server(tmp_path / "b", backend_b) as port:
        _status, _ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        _post_confirm(port, body["readings"])
        landed_b = store.read_all(tmp_path / "b" / "store")

    assert _tuples(landed_a) == _tuples(READINGS_A)
    assert _tuples(landed_b) == _tuples(READINGS_B)
    assert _tuples(landed_a) != _tuples(landed_b), "landed readings must track the fixture, not a constant"


def test_negative_control_no_usable_readings_lands_nothing(tmp_path, monkeypatch):
    """AC-2 (failing-capable negative control): no usable reading -> 0 land.

    Drives the SAME pipeline in two honest-no-data sub-cases, proving AC-1's land assertion goes
    RED when there is no usable reading (it is NOT a constant-pass):
      (a) the operator confirms NONE of the surfaced readings -> 0 land.
      (b) the mock returns [] (a blank extraction). An empty mock return raises nothing:
          `extract_all` returns `{readings: [], complete: True}` and the route reports
          `extraction_complete: True`, so the server's `if extracted or partial:` is False
          (extracted == [] AND not partial) and it falls through to the honest no-data HTML
          re-render (a NON-JSON response) — 0 fabricated readings offered, store stays empty.
    Both confirm `store.read_all == []`.
    """
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)

    # (a) confirm none -> 0 land.
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path / "a", backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200 and ctype == "application/json"
        assert body["readings"], "readings were surfaced for review"
        cstatus, cbody = _post_confirm(port, [])
        assert cstatus == 200
        assert cbody["landed"] == []
        assert store.read_all(tmp_path / "a" / "store") == []

    # (b) blank extraction -> honest no-data re-render, NOT a fabricated reading.
    empty_backend = _FixtureBackend(())
    with _running_server(tmp_path / "b", empty_backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200
        assert ctype != "application/json", (
            "a blank extraction must surface the no-data re-render, NOT a review payload"
        )
        assert _offered_readings(ctype, body) == [], "a blank extraction offers no fabricated reading"
        assert store.read_all(tmp_path / "b" / "store") == []
    assert empty_backend.extract_calls, "the extract lane was exercised (not a silent no-op)"


def test_confirm_gate_store_empty_until_confirm(tmp_path, monkeypatch):
    """AC-6 (confirm-gate): a model-extracted reading lands ONLY after the confirm POST.

    The /upload response carries the readings for review and lands 0; the store is empty if the
    confirm step is bypassed; a reading is readable from the store ONLY after /confirm-extraction.
    """
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200 and ctype == "application/json"
        assert body["readings"], "the /upload body carries the extracted readings for review"
        # Confirm bypassed -> 0 land.
        assert store.read_all(tmp_path / "store") == []

        _post_confirm(port, body["readings"])
        # filter the additive biomarker:: trend-feed mirror (a registered marker mirrors on confirm).
        bare = [r for r in store.read_all(tmp_path / "store") if not r["item"].startswith("biomarker::")]
        assert len(bare) == len(READINGS_A)


def test_mock_tested_no_live_key_resolution_zero_spend(tmp_path, monkeypatch):
    """AC-8: the E2E runs over the mock seam with 0 live key-gated calls (no network, no key).

    Spies `key_source.resolve` (the live backend's only key gate); the full upload -> confirm ->
    land E2E lands the fixture readings via the mock, and the spy records 0 calls — the live lane
    is never touched. Proves the run is deterministic + CI-runnable with no key / 0 spend.
    """
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)
    calls = []

    def _spy_resolve(*args, **kwargs):
        calls.append((args, kwargs))
        return "FAKE-KEY-NEVER-USED"

    monkeypatch.setattr("scripts.model.key_source.resolve", _spy_resolve)

    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        _status, _ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        _post_confirm(port, body["readings"])
        landed = store.read_all(tmp_path / "store")

    assert _tuples(landed) == _tuples(READINGS_A), "the extract lane ran via the mock"
    assert backend.extract_calls, "the mock backend actually received the extracted text"
    assert calls == [], "no live key resolution occurred (0 live spend)"


# --------------------------------------------------------------------------- #
# Cycle 2 — the composed falsification probes
#   AC-3 (crown-jewel raw-binary-egress), AC-4 (completeness), AC-5 (genetics),
#   AC-6 (local-extractor-network), NFR-4 (fail-closed), NFR-6 (OQ-3 residue)
# --------------------------------------------------------------------------- #


def test_probe_crown_jewel_raw_binary_egress_text_lane_only(tmp_path, monkeypatch):
    """AC-3 (CROWN-JEWEL, mock-recording): the raw PDF binary reaches ONLY the local extractor.

    The stub models the local extractor — it returns clean TEXT (no raw token); the seeded
    raw-binary token lives only in the PDF binary (the staged temp), absent from the extracted
    text. Across the full E2E: every model call carries `media_type == "text/plain"` (never
    application/pdf / a document block); the raw token reaches NO model call's content AND no
    other sink (store/dna/scaffold tmp roots); the landed readings carry only the structured
    `(item, value)`, never the raw bytes.
    """
    token = _raw_token()
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes(token))
        assert status == 200 and ctype == "application/json"
        _post_confirm(port, body["readings"])

    assert backend.extract_calls, "the model lane never received the extracted text"
    # Every model call carried text/plain — the raw application/pdf document path was never taken.
    assert all(mt == "text/plain" for _c, mt in backend.extract_calls)
    # The seeded raw-binary token reached NO model call content.
    received = "".join(str(c) for c, _mt in backend.extract_calls)
    assert token not in received, "the raw-binary token reached a model call (crown-jewel breach)"

    # No OTHER sink received the raw token (the tmp instance roots carry none).
    for root in (tmp_path / "store", tmp_path / "dna", tmp_path / "scaffold"):
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file():
                assert token not in p.read_text(errors="ignore"), f"{p} carries the raw-binary token"

    # The landed readings carry only the structured (item, value), never the raw bytes.
    landed = store.read_all(tmp_path / "store")
    assert _tuples(landed) == _tuples(READINGS_A)
    assert all(token not in str(r) for r in landed)


@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="poppler/pdftotext not installed")
def test_probe_crown_jewel_real_pdftotext_raw_binary_egress_text_lane_only(tmp_path):
    """AC-3 (CROWN-JEWEL, REAL-pdftotext, NON-VACUOUS): the raw PDF binary reaches ONLY the
    local extractor — driven through the REAL pdftotext subprocess, not the stub.

    The stubbed crown-jewel variant returns a CONSTANT text, so the seeded raw-binary token can
    never enter the pipeline BY CONSTRUCTION (its three token-tracing legs give 0 independent
    coverage). This variant feeds a REAL token-bearing PDF (the token appended AFTER `%%EOF`, where
    a real pdftotext extraction never picks it up) through the REAL `pdf_extract.extract_text` ->
    chunk -> the recording mock backend -> confirm. Real extraction actually PROCESSES the
    token-bearing bytes, so the token-absence assertions are non-vacuous: the seeded token reaches
    NEITHER any model call's content, NOR any tmp sink, NOR any landed reading, while the real page
    text DOES reach the text/plain model lane (proving the local subprocess ran). 0 live spend
    (recording mock at the ADR-0015 seam); marker never run.
    """
    token = _raw_token()
    pdf = _pdf_bytes(token, page_text="Ferritin 120 ng/mL sample 2026-05-01 cohort fixture")
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", pdf)
        assert status == 200 and ctype == "application/json"
        _post_confirm(port, body["readings"])

    assert backend.extract_calls, "the model lane never received the extracted text"
    # Every model call carried text/plain — the raw application/pdf document path was never taken.
    assert all(mt == "text/plain" for _c, mt in backend.extract_calls)
    received = "".join(str(c) for c, _mt in backend.extract_calls)
    # The REAL pdftotext output reached the model lane (the local subprocess genuinely ran) — this
    # is what makes the absence assertion below non-vacuous (a stub could not feed the page text).
    assert "Ferritin" in received, "real pdftotext did not feed the extracted text to the chunker"
    # NON-VACUOUS: the seeded raw-binary token was PROCESSED by real extraction yet reached NO
    # model call content (the crown-jewel text-only boundary held on real-extracted bytes).
    assert token not in received, "the raw-binary token reached a model call (crown-jewel breach)"

    # No OTHER sink received the raw token (the tmp instance roots carry none).
    for root in (tmp_path / "store", tmp_path / "dna", tmp_path / "scaffold"):
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file():
                assert token not in p.read_text(errors="ignore"), f"{p} carries the raw-binary token"

    # The landed readings carry only the structured (item, value), never the raw bytes.
    landed = store.read_all(tmp_path / "store")
    assert _tuples(landed) == _tuples(READINGS_A)
    assert all(token not in str(r) for r in landed)


def test_probe_serve_and_ingest_layers_import_no_outbound_client():
    """AC-3 (static): the serve layer + the new local-extractor modules carry 0 outbound client.

    `scripts/serve/*.py` AND the new `scripts/ingest/{pdf_extract,extract_chunked}.py` reference
    no outbound HTTP client (`_OUTBOUND_CLIENT_MARKERS`); the two ingest modules import no
    `anthropic` SDK; and the single model-client import lives ONLY under `scripts/model/`.
    Mirrors test_serve_no_egress + test_client's single-import seam, EXTENDED to the new modules.
    """
    targets = list((REPO_ROOT / "scripts" / "serve").glob("*.py")) + [
        REPO_ROOT / "scripts" / "ingest" / "pdf_extract.py",
        REPO_ROOT / "scripts" / "ingest" / "extract_chunked.py",
    ]
    for py in targets:
        src = py.read_text()
        for marker in _OUTBOUND_CLIENT_MARKERS:
            assert marker not in src, (
                f"{py.name} references an outbound client ({marker!r}) — must be egress-free"
            )
    for mod in ("pdf_extract.py", "extract_chunked.py"):
        assert "anthropic" not in (REPO_ROOT / "scripts" / "ingest" / mod).read_text(), (
            f"{mod} imports the model-client SDK — the local extractor must carry no SDK"
        )
    result = subprocess.run(
        [
            "rg", "-n",
            r"anthropic|openai|\.messages\.create|httpx|requests",
            "scripts/", "--glob", "!scripts/model/**",
        ],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 1, (
        "model-client import leaked outside scripts/model/:\n" + result.stdout
    )


def test_probe_local_extractor_network_zero(tmp_path, monkeypatch):
    """AC-6 (local-extractor-network): the local extractor opens 0 sockets, runs no heavy marker.

    Structural (always runs): `pdf_extract.py` + `extract_chunked.py` import no outbound HTTP
    client and no `anthropic` SDK — 0 network by construction. Behavioural (skipif pdftotext):
    a text-layer PDF never triggers the heavy `marker` fallback, so no real heavy run / model
    download occurs (the OS-egress-guard LIVE 0-socket form is OQ-1, deferred).
    """
    for mod in ("pdf_extract.py", "extract_chunked.py"):
        src = (REPO_ROOT / "scripts" / "ingest" / mod).read_text()
        for marker in _OUTBOUND_CLIENT_MARKERS:
            assert marker not in src, f"{mod} references an outbound client ({marker!r})"
        assert "anthropic" not in src, f"{mod} imports the model-client SDK"

    if shutil.which("pdftotext") is not None:
        marker_calls = []
        monkeypatch.setattr(
            pdf_extract, "_run_marker",
            lambda pdf_path: marker_calls.append(pdf_path) or "",
        )
        pdf = tmp_path / "text_layer.pdf"
        pdf.write_bytes(_make_text_pdf("Ample text layer present here sample 2026-04-01"))
        text = pdf_extract.extract_text(pdf)
        assert "Ample" in text, "pdftotext did not extract the text layer"
        assert marker_calls == [], "the heavy marker tier ran on a text-layer PDF (0 real run violated)"


def test_probe_completeness_multichunk_union_deduped_lands_all(tmp_path, monkeypatch):
    """AC-4 (completeness): a multi-chunk PDF lands ALL chunks' readings, deduped, after confirm.

    Stubs the local extractor to return text that splits into >= 3 chunks, one marker per
    section. The content-driven mock returns a base reading every chunk (so no chunk fail-closes)
    plus a distinct reading per marker present. After confirm the store holds the UNION deduped:
    every marker's reading (0 dropped) and the base reading ONCE (it appeared in every chunk but
    lands once — 0 duplicate). The within-budget upload surfaces `partial: false`.
    """
    markers = [f"SNPMARK{i}" for i in range(5)]
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _multichunk_text(markers))
    backend = _MarkerBackend(markers)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200 and ctype == "application/json"
        assert body["partial"] is False, "a within-budget document is complete (not partial)"
        _post_confirm(port, body["readings"])
        landed = store.read_all(tmp_path / "store")

    assert len(backend.extract_calls) >= 3, "the document was not multi-chunk"
    expected = {
        (_BASE_READING["item"], _BASE_READING["timepoint"], _BASE_READING["source"], _BASE_READING["value"]),
        *(
            (r["item"], r["timepoint"], r["source"], r["value"])
            for r in (_marker_reading(m) for m in markers)
        ),
    }
    assert _tuples(landed) == expected, "the cross-chunk union did not land complete + deduped"
    # 0 dropped (all markers + base) AND 0 duplicate (base appeared in every chunk, lands once).
    assert len(landed) == len(markers) + 1


def test_probe_honest_partial_signal_not_silent_empty(tmp_path, monkeypatch):
    """AC-4 (no-silent-truncation): an over-budget PDF surfaces an honest partial signal.

    Three non-tautological cases prove the signal trips ONLY when over budget, and never as a
    silent "no new data":
      - within-budget -> `partial: false`, `notes: []`.
      - over-budget   -> `partial: true` + a non-empty note (readings non-empty).
      - F1 edge       -> `partial: true` + a non-empty note even when `readings == []`.

    The F1 edge cannot arise from the real chunker (each chunk's empty return fail-closes the
    lane), so it is the server's defensive guard against the prior "no new data" failure; it is
    exercised by forcing the route->server seam shape — stubbing `extract_chunked.extract_all` to
    the empty+incomplete result (a test stub of a NON-frozen module, not a production edit).
    """
    # within-budget -> partial: false.
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)
    with _running_server(tmp_path / "wb", _FixtureBackend(READINGS_A)) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200 and ctype == "application/json"
        assert body["partial"] is False
        assert body["notes"] == []

    # over-budget -> partial: true + non-empty note (readings non-empty).
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _over_budget_text())
    with _running_server(tmp_path / "ob", _FixtureBackend(READINGS_A)) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200 and ctype == "application/json"
        assert body["partial"] is True
        assert body["notes"] and body["notes"][0], "the honest over-budget note must reach the operator"

    # F1: partial: true even when readings == [] (no silent collapse to the "no new data" re-render).
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: "irrelevant text")
    monkeypatch.setattr(
        extract_chunked, "extract_all",
        lambda text, client, **kwargs: {
            "readings": [], "complete": False, "note": "document too large: nothing in budget",
        },
    )
    with _running_server(tmp_path / "f1", _FixtureBackend(READINGS_A)) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200 and ctype == "application/json", (
            "F1: an over-budget empty extraction must NOT collapse to the silent no-data re-render"
        )
        assert body["readings"] == []
        assert body["partial"] is True
        assert body["notes"] and body["notes"][0]


def test_probe_non_tautological_genetics_fixture_a_genotypes_neq_b(tmp_path, monkeypatch):
    """AC-5 (genetics genotype-fact, NON-TAUTOLOGICAL): a genetics PDF lands genotype readings.

    A genetics fixture lands genotype-shaped readings after confirm — each carrying a gene+rsID
    `item`, `source == "dna-report"`, and an allele `value` — and a DIFFERENT genetics fixture
    lands DIFFERENT genotype readings (B != A), proving the durable genotype fact is the fixture's
    parse, not a constant.
    """
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: "GENOME SNP REPORT no-PII\n")

    backend_a = _FixtureBackend(GENETICS_A)
    with _running_server(tmp_path / "a", backend_a) as port:
        _status, _ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        _post_confirm(port, body["readings"])
        landed_a = store.read_all(tmp_path / "a" / "store")

    backend_b = _FixtureBackend(GENETICS_B)
    with _running_server(tmp_path / "b", backend_b) as port:
        _status, _ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        _post_confirm(port, body["readings"])
        landed_b = store.read_all(tmp_path / "b" / "store")

    assert _tuples(landed_a) == _tuples(GENETICS_A)
    assert _tuples(landed_b) == _tuples(GENETICS_B)
    assert _tuples(landed_a) != _tuples(landed_b), "genetics A genotypes must differ from B"
    # The genotype-fact shape: gene+rsID item, dna-report source, allele-call value.
    for reading in landed_a:
        assert reading["source"] == "dna-report"
        assert "rs" in reading["item"] and " " in reading["item"], "item is not gene+rsID"
        assert "(" in reading["value"] and ")" in reading["value"], "value is not an allele call"


def test_genetics_extract_prompt_carries_mapping_rule():
    """AC-5 (T3 cross-check): the extract system prompt carries the genetics genotype-fact rule.

    Consumes the rule's PRESENCE (not its exact text): `_extract_system_prompt()` carries the
    `dna-report` source token plus the allele/rsID mapping tokens (the T3 -> T6 edge).
    """
    from scripts.model.client import _extract_system_prompt

    prompt = _extract_system_prompt()
    assert "dna-report" in prompt, "the genetics source mapping is absent from the extract prompt"
    low = prompt.lower()
    assert "allele" in low and "rsid" in low, "the genotype allele/rsID mapping is absent"


def test_probe_fail_closed_extraction_failure_lands_no_fabricated_genotype(tmp_path, monkeypatch):
    """NFR-4 (fail-closed / no-fabrication): a failed extraction fabricates nothing.

    Two failure injections, each driven through the served /upload surface:
      (a) `pdf_extract.extract_text` raises `PdfExtractError` (a total local-extract failure).
      (b) the mock chunk backend raises `ModelCallError` (a chunk model-call failure).
    Each surfaces HTTP 200 (the request thread survived), NO JSON readings payload, and
    `store.read_all == []` — 0 fabricated genotypes, nothing lands.
    """
    # (a) total local-extract failure.
    def _raise_extract(path):
        raise pdf_extract.PdfExtractError("synthetic total extraction failure")

    monkeypatch.setattr(pdf_extract, "extract_text", _raise_extract)
    with _running_server(tmp_path / "a", _FixtureBackend(GENETICS_A)) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200, "the request thread survived (degrade, not drop)"
        assert ctype != "application/json", "a failed extraction offers no JSON readings payload"
        assert _offered_readings(ctype, body) == []
        assert store.read_all(tmp_path / "a" / "store") == []

    # (b) chunk model-call failure.
    monkeypatch.setattr(pdf_extract, "extract_text", lambda path: _EXTRACTED_TEXT_A)
    raising = _RaisingBackend()
    with _running_server(tmp_path / "b", raising) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes())
        assert status == 200
        assert ctype != "application/json"
        assert _offered_readings(ctype, body) == []
        assert store.read_all(tmp_path / "b" / "store") == []
    assert raising.extract_calls, "the chunk extraction was actually attempted (the model lane failed)"


def test_oq3_no_raw_or_text_residue_in_tracked_tree(tmp_path, monkeypatch):
    """NFR-6 (OQ-3 residue): no tracked file carries the raw-binary OR extracted-text token.

    Drives the full E2E with a per-run-unique raw-binary token (in the PDF bytes) AND an
    extracted-text token (in the stubbed extractor's output), then scans every TRACKED file
    (`git ls-files`, which respects .gitignore) for BOTH -> 0 hits. The dropzone exemption set
    is read from .gitignore and confirmed genuinely ignored, so a future dropzone change cannot
    silently weaken the scan. The tmp instance roots carry neither token (the raw upload + the
    extracted text lived only in memory / the discarded OS-temp staged path).
    """
    raw_token = _raw_token()
    text_token = f"APLUS_E2E_TEXTTOKEN_{uuid.uuid4().hex}"
    monkeypatch.setattr(
        pdf_extract, "extract_text",
        lambda path: f"Ferritin 120 ng/mL {text_token} sample 2026-05-01\n",
    )
    backend = _FixtureBackend(READINGS_A)
    with _running_server(tmp_path, backend) as port:
        status, ctype, body = _post_upload(port, "report.pdf", _pdf_bytes(raw_token))
        assert status == 200 and ctype == "application/json"
        _post_confirm(port, body["readings"])

    dropzones = _gitignore_dropzones()
    assert dropzones, "the .gitignore dropzone exemption set is non-empty"
    for prefix in dropzones:
        assert _is_gitignored(prefix), f"dropzone {prefix} is no longer git-ignored — exemption weakened"

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True
    ).stdout.splitlines()
    for token in (raw_token, text_token):
        hits = []
        for rel in tracked:
            if not rel:
                continue
            path = REPO_ROOT / rel
            try:
                if token in path.read_text(errors="ignore"):
                    hits.append(rel)
            except OSError:
                continue
        assert hits == [], f"a token leaked into tracked files: {hits}"

    for root in (tmp_path / "store", tmp_path / "dna", tmp_path / "scaffold"):
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file():
                content = p.read_text(errors="ignore")
                assert raw_token not in content and text_token not in content, f"{p} carries a token"


# --------------------------------------------------------------------------- #
# Cycle 3 — EXTEND-NOT-REBUILD (AC-7)
# --------------------------------------------------------------------------- #


def test_probe_extend_not_rebuild_frozen_set_numstat_zero():
    """AC-7 (EXTEND-NOT-REBUILD): the byte-frozen engine + sink set is unchanged from the fork.

    `git diff --numstat <fork-point> -- <frozen set>` emits 0 rows over the EXTENDED frozen set
    (scripts/ingest/{ingest,adapter}.py + every scripts/plan/*.py + scripts/store/{keying,store}.py)
    — T6 is a Create-only test binding the existing spine. Mirrors
    test_route.py::test_frozen_engine_byte_unchanged; failing-capable: a transient edit to any
    frozen file emits a row.
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    rows = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", *_FROZEN_ENGINE_PATHS],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    changed = [line for line in rows.splitlines() if line.strip()]
    assert changed == [], f"a frozen engine/plan file was edited (EXTEND-NOT-REBUILD broken): {changed}"


def test_router_additive_only_from_fork():
    """HIST1 / PF-S63-02: scripts/plan/router.py changed ADDITIVELY ONLY from the fork.

    router.py is the sanctioned ADR-0032-T3 additive seam, so it is NOT byte-frozen — but
    a NON-ADDITIVE rewrite of its existing engine logic (more deleted lines than the
    sanctioned change) is the crown-jewel-spine regression this guard catches. Falsifiable:
    deleting any existing non-sanctioned line pushes the deletion count over the threshold
    and REDs this test. INSERTIONS are unbounded (additive extension is allowed).
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    fields = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", _ROUTER_ADDITIVE_PATH],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    # numstat row: "<insertions>\t<deletions>\t<path>"; absent row -> unchanged -> 0 deletions.
    deletions = int(fields[1]) if fields else 0
    assert deletions <= _ROUTER_SANCTIONED_DELETIONS, (
        f"router.py deleted {deletions} lines (> {_ROUTER_SANCTIONED_DELETIONS} sanctioned) "
        f"— a NON-ADDITIVE rewrite of the de-id summary spine (PF-S63-02 guard-loosening)"
    )


# HIST1 / PF-S63-02: tailoring.py (ADR-0037 care-lane tailoring) is excluded from the
# byte-frozen set above because it is a NEW post-ADR-0032 crown-jewel module extended across
# T1/T2/T3 — but a WHOLESALE exclusion would let a future NON-ADDITIVE rewrite that DELETES a
# T2 safety gate pass CI silently. The additive-only guard below names that failure class:
# DELETIONS are capped at 0, while INSERTIONS stay unbounded. It is PROSPECTIVE — a
# new-since-fork file reports 0 deletions vs the fork, so the guard is vacuous until tailoring.py
# is on main; within-branch protection is tests/plan/test_tailoring.py's behavioral gates' job.
_TAILORING_ADDITIVE_PATH = "scripts/plan/tailoring.py"
# ADR-0040-T2 (sanctioned): the tailor emit-gate wraps its `resolve_plan(store_read(...))` in
# `plan_confirm.filter_confirmed(...)` so a held domain is skipped — a modify-to-ADD-a-gate edit
# (import line + the resolve line) that numstat scores as 2 deletions. Verified safety-adding, not
# gate-removing; the deletion cap is raised to the exact sanctioned count. A larger non-additive
# rewrite (>2 deletions) still reds. Behavioral protection is tests/plan/test_tailoring.py's job.
_TAILORING_SANCTIONED_DELETIONS = 2


def test_tailoring_additive_only_from_fork():
    """HIST1 / PF-S63-02: scripts/plan/tailoring.py changed ADDITIVELY ONLY from the fork.

    PROSPECTIVE guard: tailoring.py is new-since-fork, so it reports 0 deletions vs the fork
    and this test is vacuous until tailoring.py lands on main. Once on main, a NON-ADDITIVE
    rewrite that DELETES a T2 safety gate pushes the deletion count over 0 and REDs this test.
    Within-branch, the INSERTION-shape egress risk is the job of tests/plan/test_tailoring.py's
    behavioral gates (T1 AC-4 static-scan; T3 AC-2/AC-3 wire-scan/artifact-only). INSERTIONS
    are unbounded (additive extension is allowed).
    """
    fork_point = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    fields = subprocess.run(
        ["git", "diff", "--numstat", fork_point, "--", _TAILORING_ADDITIVE_PATH],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    # numstat row: "<insertions>\t<deletions>\t<path>"; absent row -> unchanged -> 0 deletions.
    deletions = int(fields[1]) if fields else 0
    assert deletions <= _TAILORING_SANCTIONED_DELETIONS, (
        f"tailoring.py deleted {deletions} lines (> {_TAILORING_SANCTIONED_DELETIONS} sanctioned) "
        f"— a NON-ADDITIVE rewrite removing a T2 safety gate (PF-S63-02 guard-loosening)"
    )
