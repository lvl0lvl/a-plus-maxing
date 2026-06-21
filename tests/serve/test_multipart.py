"""Multipart reader + temp-staging tests (ADR-0013-T2).

Covers the traversal-safe, oversize-bounded upload staging that `ADR-0013-T4`'s
POST handler consumes. AC-1: a file part streams to a path under a server-owned
temp dir. AC-2 / Risk Confirmation-3: a `../../x` / `..\\..\\x` / absolute
`/etc/x` filename stages ONLY inside the temp dir (the traversal target never
materializes). AC-3 / Risk `07f6`: an over-ceiling body is refused before the
full body is written and leaves 0 residual oversize temp file. AC-4: the staging
copy is chunked (no single-shot full-body read).
"""

import io
from pathlib import Path

from scripts.serve.multipart import UploadTooLarge, stage_uploads

REPO_ROOT = Path(__file__).resolve().parents[2]

BOUNDARY = "----aplusboundary7MA4YWxkTrZu0gW"


def _multipart_body(parts):
    """Build a multipart/form-data body from `parts`.

    Args:
        parts (list): Each item is a dict with `name`, optional `filename`, and
            `body` (bytes). A `filename` makes it a file part; absence makes it a
            plain form field.

    Returns:
        (bytes) The encoded multipart body with the module-level BOUNDARY.
    """
    out = bytearray()
    for part in parts:
        out += f"--{BOUNDARY}\r\n".encode()
        disp = f'Content-Disposition: form-data; name="{part["name"]}"'
        if "filename" in part:
            disp += f'; filename="{part["filename"]}"'
        out += (disp + "\r\n\r\n").encode()
        body = part["body"]
        out += body if isinstance(body, bytes) else body.encode()
        out += b"\r\n"
    out += f"--{BOUNDARY}--\r\n".encode()
    return bytes(out)


def _content_type():
    """Return the multipart content-type header value with the test boundary."""
    return f"multipart/form-data; boundary={BOUNDARY}"


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 stage under temp root; AC-2 traversal containment
# --------------------------------------------------------------------------- #


def test_file_part_streams_under_temp_root(tmp_path):
    """AC-1: a file part is streamed to a path inside the server-owned temp root.

    Stages a single file part and asserts the returned staged path exists and
    `Path(staged).resolve()` is within the temp root — the upload lands under
    the server-chosen temp dir, never elsewhere.
    """
    body = _multipart_body([{"name": "export", "filename": "export.zip", "body": b"PK\x03\x04 payload"}])
    result = stage_uploads(_content_type(), io.BytesIO(body), tmp_path)

    staged = result["files"][0]["path"]
    assert Path(staged).exists(), "staged file does not exist"
    assert Path(staged).resolve().is_relative_to(tmp_path.resolve()), (
        f"staged path {staged} escaped the temp root {tmp_path}"
    )
    assert Path(staged).read_bytes() == b"PK\x03\x04 payload", "staged content mismatch"


def test_traversal_filenames_stay_inside_temp_root(tmp_path):
    """AC-2 / Risk Confirmation-3: traversal/absolute filenames stage inside temp.

    Uploads parts with `../../x`, `..\\..\\x`, and absolute `/etc/x` filenames.
    Each staged path must still resolve within the temp root, and the traversal
    target (a sibling of the temp root named `x`, or `/etc/x`) must not exist.
    Proves the client filename contributes only a basename.
    """
    escape_target = tmp_path.parent / "x"
    etc_target = Path("/etc/x")
    assert not escape_target.exists(), "fixture precondition: sibling x must not pre-exist"

    for client_name in ("../../x", "..\\..\\x", "/etc/x"):
        body = _multipart_body([{"name": "f", "filename": client_name, "body": b"traversal-attempt"}])
        result = stage_uploads(_content_type(), io.BytesIO(body), tmp_path)
        staged = Path(result["files"][0]["path"])
        assert staged.resolve().is_relative_to(tmp_path.resolve()), (
            f"filename {client_name!r} escaped the temp root: staged at {staged}"
        )

    assert not escape_target.exists(), "traversal escaped: ../../x wrote a sibling of the temp root"
    assert not etc_target.exists(), "traversal escaped: absolute /etc/x was written"


def test_form_fields_returned_alongside_files(tmp_path):
    """AC-1 surface: non-file form fields are returned alongside staged files.

    The published surface returns the form fields plus the staged file paths so
    the route can read both. A plain field (no filename) lands in `fields`, the
    file part in `files`.
    """
    body = _multipart_body(
        [
            {"name": "kind", "body": "apple-health"},
            {"name": "export", "filename": "export.zip", "body": b"PK payload"},
        ]
    )
    result = stage_uploads(_content_type(), io.BytesIO(body), tmp_path)

    assert result["fields"].get("kind") == "apple-health", "form field not returned"
    assert len(result["files"]) == 1, "expected exactly one staged file"


# --------------------------------------------------------------------------- #
# Cycle 2 — AC-3 byte ceiling refusal; AC-4 chunked copy
# --------------------------------------------------------------------------- #


def test_over_ceiling_body_refused_before_full_write(tmp_path, monkeypatch):
    """AC-3 / Risk `07f6`: an over-ceiling file part is refused, 0 residual file.

    Drives the ceiling via a small injected `MAX_UPLOAD_BYTES` (test seam) so the
    refusal is proved WITHOUT a 512 MiB in-memory fixture (the prior fixture flaked
    under memory pressure). A body modestly above the injected ceiling must raise
    UploadTooLarge before the full body is written, and the partial temp file is
    removed — no residual oversize temp file remains. Failing-capable: remove the
    ceiling and the over-ceiling body stages instead of raising.
    """
    import scripts.serve.multipart as multipart

    monkeypatch.setattr(multipart, "MAX_UPLOAD_BYTES", 4096)
    oversize = b"A" * (4096 + 2048)  # over the injected ceiling, tiny in RAM
    body = _multipart_body([{"name": "export", "filename": "big.zip", "body": oversize}])

    raised = False
    try:
        stage_uploads(_content_type(), io.BytesIO(body), tmp_path)
    except UploadTooLarge:
        raised = True
    assert raised, "over-ceiling body was NOT refused (the byte ceiling is missing)"

    residual = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert residual == [], f"partial oversize temp file left behind: {residual}"


def test_at_ceiling_body_is_accepted(tmp_path, monkeypatch):
    """AC-3 boundary: a body at exactly the ceiling is accepted (refusal is for OVER).

    A part whose body is exactly MAX_UPLOAD_BYTES must stage successfully — the
    ceiling refuses strictly-greater, not equal, so the boundary is not off-by-one.
    Drives the ceiling via a small injected `MAX_UPLOAD_BYTES` (test seam) so the
    boundary is proved WITHOUT a 512 MiB in-memory fixture.
    """
    import scripts.serve.multipart as multipart

    monkeypatch.setattr(multipart, "MAX_UPLOAD_BYTES", 4096)
    at_ceiling = b"B" * 4096
    body = _multipart_body([{"name": "export", "filename": "atlimit.zip", "body": at_ceiling}])
    result = stage_uploads(_content_type(), io.BytesIO(body), tmp_path)
    staged = Path(result["files"][0]["path"])
    assert staged.exists() and staged.stat().st_size == 4096, "at-ceiling body not staged whole"


def test_copy_is_chunked_not_single_shot():
    """AC-4: the staging copy is chunked — no single-shot full-body part read.

    Greps `scripts/serve/multipart.py` for the chunked-copy loop and asserts no
    unbounded `.read()` (read of the whole part into memory). The ceiling can only
    fire before full materialization if the copy reads in bounded chunks.
    """
    src = (REPO_ROOT / "scripts" / "serve" / "multipart.py").read_text()
    assert "shutil.copyfileobj" in src or "CHUNK" in src, "no chunked-copy loop found"
    assert ".read()" not in src, "a single-shot full-body .read() defeats the byte ceiling"
