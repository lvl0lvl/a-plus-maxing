"""Multipart/form-data reader + traversal-safe, oversize-bounded temp staging (ADR-0013-T2).

`stage_uploads(content_type, body_stream, temp_root)` parses a multipart/form-data
request body and streams each uploaded FILE part to a server-chosen path UNDER
`temp_root`, deriving the staged filename from ONLY the basename of the client
filename (`Path(name).name`) so a `../` traversal cannot escape the temp dir
(ADR-0013 Confirmation-3). The body is read from the stream in bounded chunks; a
file part exceeding `MAX_UPLOAD_BYTES` is refused (the partial temp file removed)
BEFORE its full body materializes — the ADR-0012 `07f6` self-DoS mitigation. The
chunked copy mirrors `dna.land`'s streamed shape (scripts/ingest/dna.py:96-98).

This PUBLISHES the staging surface `ADR-0013-T4`'s POST handler consumes: the
returned staged path ALWAYS resolves within `temp_root`; the client filename
contributes only a basename. Downstream tasks must not use the raw client
filename or remove the ceiling without Architect + Security review.
"""

from pathlib import Path

# The per-file-part byte ceiling. A part body strictly exceeding this is refused
# before the full body is written (ADR-0012 `07f6`: an unbounded copy can OOM /
# amplify; the Apple export can be hundreds of MB). 512 MiB covers a large
# Apple-Health zip with headroom while bounding a single upload.
MAX_UPLOAD_BYTES = 512 * 1024 * 1024

# The streamed-copy chunk size. The body is consumed in chunks of this size so the
# ceiling fires mid-stream and an over-ceiling part never fully materializes.
CHUNK_SIZE = 64 * 1024


class UploadTooLarge(Exception):
    """Raised when a file part exceeds MAX_UPLOAD_BYTES (the partial file is removed)."""


def _parse_boundary(content_type):
    """Extract the boundary token from a multipart/form-data content-type header.

    Args:
        content_type (str): The request content-type header value.

    Returns:
        (bytes) The boundary delimiter bytes (without the leading `--`).
    """
    if "boundary=" not in (content_type or ""):
        raise ValueError("content-type is not multipart/form-data with a boundary")
    boundary = content_type.split("boundary=", 1)[1].strip()
    if boundary.startswith('"') and boundary.endswith('"'):
        boundary = boundary[1:-1]
    if not boundary:
        raise ValueError("multipart boundary is empty")
    return boundary.encode("latin-1")


def _parse_disposition(raw_headers):
    """Parse a part's Content-Disposition params from its raw header block.

    Args:
        raw_headers (bytes): The part header block (before the blank line).

    Returns:
        (dict) The `name` and optional `filename` params.
    """
    params = {}
    for line in raw_headers.split(b"\r\n"):
        text = line.decode("latin-1")
        if text.lower().startswith("content-disposition:"):
            for token in text.split(";")[1:]:
                token = token.strip()
                if "=" in token:
                    key, value = token.split("=", 1)
                    params[key.strip().lower()] = value.strip().strip('"')
    return params


def _safe_name(client_filename):
    """Derive a traversal-safe staged basename from the client filename.

    Takes ONLY `Path(client_filename).name` so no directory component (POSIX or
    Windows) survives, then strips a leftover-traversal name. The single
    sanitization site keeps the traversal-containment criterion meaningful.

    Args:
        client_filename (str): The untrusted client-supplied filename.

    Returns:
        (str) A basename with no directory components and no bare-traversal name.
    """
    # Normalize Windows separators so Path on POSIX still strips a `..\\..\\x` head.
    name = Path(client_filename.replace("\\", "/")).name
    if name in ("", ".", ".."):
        name = "upload"
    return name


class _BoundaryStream:
    """Incremental multipart reader over a body stream — never reads the body whole.

    Consumes `body_stream` in CHUNK_SIZE chunks into a sliding buffer, yielding
    each part's headers, then streaming the part body up to the next boundary so
    the byte ceiling can fire before an over-ceiling part fully materializes.

    Attributes:
        stream (BinaryIO): The request body stream.
        delimiter (bytes): The boundary delimiter `--<boundary>`.
    """

    def __init__(self, body_stream, boundary):
        self.stream = body_stream
        self.delimiter = b"--" + boundary
        self._buf = b""
        self._eof = False

    def _fill(self):
        """Pull one chunk into the buffer; return False at end of stream."""
        if self._eof:
            return False
        chunk = self.stream.read(CHUNK_SIZE)
        if not chunk:
            self._eof = True
            return False
        self._buf += chunk
        return True

    def _read_until(self, marker):
        """Stream-read until `marker` is in the buffer; return the index or raise."""
        while marker not in self._buf:
            if not self._fill():
                raise ValueError(f"malformed multipart body: missing {marker!r}")
        return self._buf.index(marker)

    def parts(self):
        """Yield `(params, body_iter)` per part; body_iter streams the part bytes.

        Each part's body is yielded as a chunk iterator bounded by the next
        boundary delimiter — the caller pulls chunks, so an over-ceiling body is
        never accumulated here.
        """
        # Skip the preamble up to (not including) the first delimiter; the loop
        # then consumes each delimiter and decides part-vs-close uniformly.
        first = self._read_until(self.delimiter)
        self._buf = self._buf[first:]

        while True:
            # At each iteration the buffer starts with the delimiter `--<boundary>`.
            # Consume it, then the two bytes after it decide part vs. close.
            self._buf = self._buf[len(self.delimiter) :]
            while len(self._buf) < 2 and self._fill():
                pass
            if self._buf[:2] == b"--":  # closing delimiter `--<boundary>--`
                return
            # Another part: consume the CRLF, then read the header block.
            self._buf = self._buf.lstrip(b"\r\n")
            sep = self._read_until(b"\r\n\r\n")
            raw_headers = self._buf[:sep]
            self._buf = self._buf[sep + 4 :]
            params = _parse_disposition(raw_headers)
            yield params, self._iter_body()

    def _iter_body(self):
        """Yield the current part's body chunks up to the next boundary delimiter."""
        # The part body is terminated by `\r\n--<boundary>`.
        terminator = b"\r\n" + self.delimiter
        while True:
            idx = self._buf.find(terminator)
            if idx != -1:
                yield self._buf[:idx]
                # Leave the delimiter (minus the leading CRLF) in the buffer.
                self._buf = self._buf[idx + 2 :]
                return
            # Boundary not yet in buffer: flush all but a safe tail (could straddle).
            keep = len(terminator)
            if len(self._buf) > keep:
                emit = self._buf[:-keep]
                self._buf = self._buf[-keep:]
                if emit:
                    yield emit
            if not self._fill():
                raise ValueError("malformed multipart body: unterminated part")


def _stage_file(body_iter, dest):
    """Stream a part body iterator to `dest`, enforcing the byte ceiling.

    Writes the part body chunk-by-chunk (the streamed shape `dna.land` uses) while
    tracking the running byte count; a body strictly exceeding MAX_UPLOAD_BYTES is
    refused — the partial temp file is removed and UploadTooLarge raised — before
    the full body is written.

    Args:
        body_iter (Iterator): The part body chunk iterator.
        dest (Path): The staged destination path under the temp root.
    """
    seen = 0
    with open(dest, "wb") as out:
        for chunk in body_iter:
            seen += len(chunk)
            if seen > MAX_UPLOAD_BYTES:
                out.close()
                dest.unlink(missing_ok=True)
                raise UploadTooLarge(
                    f"upload exceeds the {MAX_UPLOAD_BYTES}-byte ceiling (refused before full write)"
                )
            out.write(chunk)


def stage_uploads(content_type, body_stream, temp_root):
    """Parse a multipart/form-data body and stage each file part under `temp_root`.

    Streams each uploaded FILE part to a sanitized path under `temp_root` (the
    client filename contributes only a basename), applies the per-part byte
    ceiling (an over-ceiling part is refused before its full body is written),
    and returns the staged file paths plus the plain form fields. The staged path
    ALWAYS resolves within `temp_root` — the published invariant `ADR-0013-T4`
    relies on. PUBLISHED CONTRACT (frozen): consumed by `ADR-0013-T4`.

    Args:
        content_type (str): The request content-type header (carries the boundary).
        body_stream (BinaryIO): A binary stream of the full request body.
        temp_root (str | Path): The server-chosen temp dir all parts stage under.

    Returns:
        (dict) `{"files": [{"name": str, "filename": str, "path": Path}, ...],
            "fields": {name: value}}` — the staged file parts and the plain fields.
    """
    boundary = _parse_boundary(content_type)
    temp_root = Path(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)

    reader = _BoundaryStream(body_stream, boundary)
    files = []
    fields = {}
    for params, body_iter in reader.parts():
        name = params.get("name", "")
        if "filename" in params:
            dest = temp_root / _safe_name(params["filename"])
            _stage_file(body_iter, dest)
            files.append({"name": name, "filename": params["filename"], "path": dest})
        else:
            value = b"".join(body_iter)
            fields[name] = value.decode("utf-8", errors="replace")
    return {"files": files, "fields": fields}
