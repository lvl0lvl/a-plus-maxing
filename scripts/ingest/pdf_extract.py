"""Local PDF->text extraction, on-device only (ADR-0031-T1).

The device-side front step that turns an uploaded PDF into TEXT entirely on the
machine, so the crown-jewel raw PDF binary never leaves the device: the bytes
reach ONLY the local `pdftotext`/`marker` subprocess. ADR-0030 sent the whole raw
PDF off-device as a base64 `document` block; ADR-0031 extracts the text here first
and sends only text downstream.

Two tiers behind one public call:

1. `extract_text(pdf_path) -> str` runs `pdftotext` (poppler) as a deterministic
   local subprocess — text-layer extraction, 0 network — as the cheap primary
   tier. When that yields fewer than `_LOW_TEXT_CHARS` non-whitespace characters
   (the scanned / no-text-layer case) it falls back to the `marker_single`
   (marker-pdf) local subprocess exactly once and returns that text.
2. On TOTAL failure (both tiers yield no usable text) it raises `PdfExtractError`
   — it NEVER returns a silent `""`, so the caller can never mistake an extraction
   failure for a genuinely empty document (the honest-data, no-silent-empty
   contract, NFR-2/NFR-4).

The module imports NO outbound HTTP client and NO model-client SDK — the raw PDF
bytes reach only the local subprocess; 0 network from the extractor (the
crown-jewel local-extractor-network property, NFR-1). It is the first
subprocess-shelling module under `scripts/ingest/`; `subprocess` is stdlib, so no
in-tree precedent is needed. T4 (Wave 2) wires this into `route._extract_unrecognized`;
this task builds only the standalone extractor (EXTEND-NOT-REBUILD, NFR-3).
"""

import subprocess
import tempfile
from pathlib import Path

# OQ-2: the named low-text threshold (non-whitespace chars). A pdftotext return
# below this signals no/low text layer (scanned PDF) and triggers the marker
# fallback. The two-tier contract holds regardless of the exact value (NFR-7);
# this is one machine-diffable constant, not a call-site literal.
_LOW_TEXT_CHARS = 16

# Constant failure message — no raw path / file-content interpolation, the same
# no-leak posture as the model boundary's fail-closed raises.
_EXTRACT_FAILED_MSG = (
    "PDF text extraction failed: both pdftotext and marker yielded no usable text"
)


class PdfExtractError(Exception):
    """Raised when both extraction tiers yield no usable text (total failure)."""


def _run_pdftotext(pdf_path):
    """Shell `pdftotext` to extract the PDF's text layer to stdout (0 network).

    Passes argv as a list (no `shell=True`, no string interpolation of the path)
    and captures stdout. A PDF with no text layer yields little/no text here; the
    low-text decision and the fail-loud raise live in `extract_text`, so this
    runner returns whatever text the binary produced.

    Args:
        pdf_path (str | Path): Path to the staged PDF.
    """
    completed = subprocess.run(
        ["pdftotext", str(Path(pdf_path)), "-"],
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _run_marker(pdf_path):
    """Shell `marker_single` to extract the PDF to markdown text (0 network).

    The heavy fallback tier, paid only on the low-text trigger. Writes markdown to
    a temp output dir, then reads and joins the produced `.md` file(s). Passes argv
    as a list (no `shell=True`). In tests this runner is ALWAYS stubbed — never
    shelled — so no real heavy run / model download / network occurs there.

    Args:
        pdf_path (str | Path): Path to the staged PDF.
    """
    with tempfile.TemporaryDirectory() as out_dir:
        subprocess.run(
            ["marker_single", str(Path(pdf_path)), "--output_dir", out_dir],
            capture_output=True,
            text=True,
        )
        markdown = [md.read_text() for md in sorted(Path(out_dir).glob("**/*.md"))]
    return "\n".join(markdown)


def extract_text(pdf_path):
    """Extract a PDF's text on-device — pdftotext primary, marker fallback, fail-loud.

    Runs `pdftotext`; if it returns at least `_LOW_TEXT_CHARS` non-whitespace
    characters, returns that text. Otherwise runs `marker_single` exactly once and
    returns its text if non-empty. If both tiers yield no usable text, raises
    `PdfExtractError` — never a silent `""`. The raw PDF bytes reach only the local
    subprocess; 0 network.

    Args:
        pdf_path (str | Path): Path to the staged PDF.

    Returns:
        (str) The extracted text.
    """
    try:
        text = _run_pdftotext(pdf_path)
        if len(text.strip()) >= _LOW_TEXT_CHARS:
            return text
        text = _run_marker(pdf_path)
    except OSError as exc:
        # An absent binary makes subprocess.run raise FileNotFoundError (an OSError);
        # wrap it into the typed PdfExtractError so total failure is actually total.
        raise PdfExtractError(_EXTRACT_FAILED_MSG) from exc
    if text.strip():
        return text
    raise PdfExtractError(_EXTRACT_FAILED_MSG)
