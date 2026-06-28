"""Tests for the local PDF->text extraction module (ADR-0031-T1).

Two cycles. Cycle 1 drives the two-tier dispatch (``pdftotext`` primary, ``marker``
fallback on low text), the fail-loud raise on total failure, and the crown-jewel
0-network source-grep — all over STUBBED subprocess runners (always-run,
deterministic; ``marker_single`` is NEVER shelled, so no heavy run / model
download / network breach). Cycle 2 round-trips the REAL ``pdftotext`` binary over
hand-built synthetic NON-PII fixture PDFs behind a
``skipif shutil.which("pdftotext") is None`` gate, proving the return is the
extracted text and not a hardcoded constant.
"""

import shutil

import pytest

from scripts.ingest import pdf_extract

# The outbound-client surface markers, a test-local copy mirroring
# tests/serve/test_serve_no_egress.py:50-56 plus the model-client SDK. The
# crown-jewel grep (AC-5) reds the moment any appears in pdf_extract.py.
_OUTBOUND_CLIENT_MARKERS = (
    "socket.create_connection",
    "urllib.request",
    "http.client",
    "requests",
    "httpx",
)

# Single-token synthetic NON-PII sentinels: contiguous (no spaces, so pdftotext
# extracts each verbatim), distinct, and comfortably longer than any sane
# _LOW_TEXT_CHARS so the real-binary cases return on the cheap pdftotext tier
# (never shelling the real marker).
_X_SENTINEL = "GENOMARKERX_MTNR1B_rs10830963"
_Y_SENTINEL = "GENOMARKERY_TCF7L2_rs7903146"

_poppler_required = pytest.mark.skipif(
    shutil.which("pdftotext") is None,
    reason="pdftotext (poppler) not installed — real-binary extraction not exercisable",
)


def _make_text_pdf(text):
    """Build a minimal single-page text-layer PDF whose only text is `text`.

    Deterministic, no PII, no third-party library (reportlab/fpdf are not in the
    runtime) — pdftotext extracts `text` verbatim. Byte offsets in the xref table
    are computed from the assembled body so the file is structurally valid.

    Args:
        text (str): The latin-1-encodable synthetic text to embed.
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


# --------------------------------------------------------------------------- #
# Cycle 1 — branching / fail-loud / 0-network grep, over STUBBED runners
# --------------------------------------------------------------------------- #


def test_extract_text_low_text_invokes_marker_fallback_once(monkeypatch):
    """AC-3: pdftotext below threshold -> marker fallback fires exactly once."""
    marker_calls = []

    def fake_marker(pdf_path):
        marker_calls.append(pdf_path)
        return "MARKER_FALLBACK_TEXT_AMPLE_ENOUGH"

    monkeypatch.setattr(
        pdf_extract, "_run_pdftotext",
        lambda pdf_path: "x" * (pdf_extract._LOW_TEXT_CHARS - 1),
    )
    monkeypatch.setattr(pdf_extract, "_run_marker", fake_marker)

    result = pdf_extract.extract_text("/fake/scan.pdf")

    assert result == "MARKER_FALLBACK_TEXT_AMPLE_ENOUGH"
    assert len(marker_calls) == 1


def test_extract_text_ample_text_skips_marker_fallback(monkeypatch):
    """AC-4: pdftotext at/above threshold -> marker runner never invoked."""
    marker_calls = []

    def fake_marker(pdf_path):
        marker_calls.append(pdf_path)
        return "SHOULD_NOT_BE_RETURNED"

    ample = "y" * (pdf_extract._LOW_TEXT_CHARS + 5)
    monkeypatch.setattr(pdf_extract, "_run_pdftotext", lambda pdf_path: ample)
    monkeypatch.setattr(pdf_extract, "_run_marker", fake_marker)

    result = pdf_extract.extract_text("/fake/doc.pdf")

    assert result == ample
    assert len(marker_calls) == 0


def test_extract_text_raises_pdf_extract_error_when_both_extractors_empty(monkeypatch):
    """AC-6: both tiers yield no text -> PdfExtractError, never a silent ''."""
    monkeypatch.setattr(pdf_extract, "_run_pdftotext", lambda pdf_path: "")
    monkeypatch.setattr(pdf_extract, "_run_marker", lambda pdf_path: "")

    with pytest.raises(pdf_extract.PdfExtractError):
        pdf_extract.extract_text("/fake/empty.pdf")


def test_extract_text_absent_binary_raises_pdf_extract_error(monkeypatch):
    """RISKY-1: an absent binary (subprocess FileNotFoundError) raises the typed PdfExtractError.

    On a poppler-less clone `subprocess.run(["pdftotext", ...])` raises `FileNotFoundError`
    (an `OSError`). The "total failure -> PdfExtractError" contract must cover it so T4's
    `except PdfExtractError` catches it — an un-typed OSError would escape that tuple and drop
    the request thread. RED without the wrap: the FileNotFoundError propagates un-typed.
    """
    def fake_run(*args, **kwargs):
        raise FileNotFoundError(2, "No such file or directory", "pdftotext")

    monkeypatch.setattr(pdf_extract.subprocess, "run", fake_run)

    with pytest.raises(pdf_extract.PdfExtractError):
        pdf_extract.extract_text("/fake/report.pdf")


def test_pdf_extract_imports_no_outbound_client_or_sdk():
    """AC-5: the module references no outbound HTTP client and no model SDK."""
    src = __import__("pathlib").Path(pdf_extract.__file__).read_text()
    for marker in _OUTBOUND_CLIENT_MARKERS:
        assert marker not in src, (
            f"pdf_extract.py references an outbound client ({marker!r}) — the local "
            f"extractor must keep the raw PDF bytes on-device (0 network)"
        )
    assert "anthropic" not in src, (
        "pdf_extract.py references the anthropic SDK — the local extractor must "
        "import no model client (0 network)"
    )


# --------------------------------------------------------------------------- #
# Cycle 2 — real pdftotext round-trip + non-tautology, skipif-gated
# --------------------------------------------------------------------------- #


@_poppler_required
def test_extract_text_real_pdftotext_returns_fixture_text(tmp_path):
    """AC-1: real pdftotext returns the fixture PDF's embedded text verbatim."""
    pdf = tmp_path / "fixture_x.pdf"
    pdf.write_bytes(_make_text_pdf(_X_SENTINEL))

    result = pdf_extract.extract_text(pdf)

    assert _X_SENTINEL in result


@_poppler_required
def test_extract_text_non_tautological_distinct_fixtures(tmp_path):
    """AC-2: distinct fixtures yield distinct text — the return is not a constant."""
    x_pdf = tmp_path / "fixture_x.pdf"
    x_pdf.write_bytes(_make_text_pdf(_X_SENTINEL))
    y_pdf = tmp_path / "fixture_y.pdf"
    y_pdf.write_bytes(_make_text_pdf(_Y_SENTINEL))

    result_x = pdf_extract.extract_text(x_pdf)
    result_y = pdf_extract.extract_text(y_pdf)

    assert _X_SENTINEL in result_x
    assert _Y_SENTINEL in result_y
    assert result_y != result_x
