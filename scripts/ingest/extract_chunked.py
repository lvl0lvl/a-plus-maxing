"""Chunk + aggregate + dedupe extraction front with the honest-partial signal (ADR-0031-T2).

`extract_all(text, client)` takes already-extracted document TEXT plus an injected model client
and turns it into deduped readings WITHOUT ever handing the model a raw-binary block:

  1. Split `text` into bounded line-boundary chunks (each <= `_CHUNK_CHARS`) with `_CHUNK_OVERLAP`
     characters of carry-over between neighbours — a finding straddling a boundary lands in BOTH
     chunks (captured, then deduped), and a finding is never cut mid-line.
  2. Call the injected `client.extract_readings(chunk, "text/plain")` once per chunk — the
     crown-jewel text-only path. This module NEVER constructs a raw-binary / document block; it
     only ever hands the model a `text/plain` chunk (the raw upload bytes never reach here).
  3. Aggregate the UNION of every chunk's readings, deduped to one reading per
     `(item, timepoint, source)` identity through the UNCHANGED `keying.dedupe_key` — the same
     single-source-of-truth key the store sink uses. No second dedupe key is defined here.
  4. Return `{"readings": [...], "complete": bool, "note": str | None}` — the HONEST
     too-large/partial signal. A document splitting into more than `_MAX_CHUNKS` chunks returns
     the readings from the first `_MAX_CHUNKS` chunks with `complete=False` + a non-empty `note`,
     NEVER a silent empty list (the exact "no new data" failure this replaces).

The model client is INJECTED — this module imports no model-client SDK and no outbound network
client. A chunk-level model-call error propagates out of `extract_all` unswallowed: it is never
converted into a fabricated reading or a false `complete` (the fail-closed inheritance).
"""

from scripts.store.keying import dedupe_key, is_conformant

# Max characters per text/plain chunk handed to the model. An OQ-2 build-tunable value, named
# here as one machine-diffable constant rather than a call-site literal (NFR-7). Sized so a
# real multi-page report (e.g. a ~350 KB genetics export) splits into ~9 chunks — one model
# call each — rather than ~45, keeping a live upload to ~1-2 min and within the chunk budget;
# the compact genotype-fact output per chunk stays well under `_EXTRACT_MAX_TOKENS` (S100 live run).
_CHUNK_CHARS = 40000

# Characters of carry-over between consecutive chunks so a finding straddling a chunk boundary
# appears in both neighbours (captured, then deduped). An OQ-2 build-tunable value (NFR-7).
_CHUNK_OVERLAP = 400

# Max chunks processed before the honest-partial signal trips (`complete=False` + a `note`). An
# OQ-2 build-tunable value, named here as one machine-diffable constant (NFR-7).
_MAX_CHUNKS = 40


def extract_all(text, client, *, chunk_chars=_CHUNK_CHARS, overlap=_CHUNK_OVERLAP, max_chunks=_MAX_CHUNKS):
    """Chunk `text`, extract per chunk over the text path, and aggregate the deduped union.

    Splits the already-extracted document `text` into bounded line-boundary chunks, calls the
    injected `client.extract_readings(chunk, "text/plain")` once per chunk, and returns the union
    of every chunk's readings deduped through `keying.dedupe_key`. A document splitting into more
    than `max_chunks` chunks is processed for its first `max_chunks` chunks and reported as
    incomplete (the honest-partial signal); within budget it is reported complete.

    Args:
        text (str): The already-extracted document text.
        client: An injected model client exposing
            `extract_readings(content, media_type) -> list` (the ADR-0030 extraction surface).
        chunk_chars (int, optional): Max characters per chunk. Defaults to `_CHUNK_CHARS`.
        overlap (int, optional): Carry-over characters between chunks. Defaults to `_CHUNK_OVERLAP`.
        max_chunks (int, optional): Max chunks processed before the partial signal. Defaults to
            `_MAX_CHUNKS`.

    Returns:
        (dict) `{"readings": list, "complete": bool, "note": str | None}` — the deduped union of
        the processed chunks' readings, whether the whole document was processed, and a note
        describing the over-budget condition when it was not (else None).
    """
    chunks = _split_chunks(text, chunk_chars, overlap)
    complete = True
    note = None
    if len(chunks) > max_chunks:
        note = (
            f"document too large: {len(chunks)} chunks exceed the {max_chunks}-chunk budget; "
            f"extracted readings from the first {max_chunks} chunks only"
        )
        complete = False
        chunks = chunks[:max_chunks]

    collected = []
    for chunk in chunks:
        collected.extend(client.extract_readings(chunk, "text/plain"))

    # Dedupe the cross-chunk union to one reading per (item, timepoint, source) identity through
    # the shared keying.dedupe_key — mirroring the store sink's own collapse
    # (`list({keying.dedupe_key(r): r for r in readings}.values())`), NOT a second key. Each
    # reading is guarded by keying.is_conformant first: dedupe_key's documented precondition is a
    # conformant reading (it raises KeyError otherwise), the same shared check the confirm path
    # runs before landing. The injected client already guarantees conformance, so this guard never
    # drops a real reading — it only honors the precondition.
    readings = list({dedupe_key(r): r for r in collected if is_conformant(r)}.values())
    return {"readings": readings, "complete": complete, "note": note}


def _split_chunks(text, chunk_chars, overlap):
    """Split `text` into <= `chunk_chars` line-boundary chunks with `overlap` carry-over.

    Lines accumulate into a chunk until the next line would push it over `chunk_chars`; the chunk
    is emitted and the next chunk seeds with the trailing `overlap` characters (so a finding
    straddling the boundary lands in both neighbours). A single line longer than `chunk_chars` is
    hard-split into `(chunk_chars - overlap)`-bounded pieces — a degenerate no-newline run — so the
    carry-over seed still survives in assembly (seed + piece <= chunk_chars) and a finding
    straddling a hard-split boundary lands in both neighbours too, never silently dropped. Each
    emitted chunk is a contiguous slice of `text`.

    Args:
        text (str): The text to split.
        chunk_chars (int): Max characters per chunk.
        overlap (int): Carry-over characters seeded into each subsequent chunk.

    Returns:
        (list) The ordered chunks, each a contiguous <= `chunk_chars` slice of `text`.
    """
    if not text:
        return []

    # A degenerate no-newline run longer than chunk_chars is hard-split into pieces bounded at
    # (chunk_chars - overlap), NOT chunk_chars: the assembly seeds each non-first chunk with
    # `overlap` trailing chars, so a piece <= (chunk_chars - overlap) keeps seed + piece within
    # chunk_chars and the seed is never dropped — a reading straddling a hard-split boundary still
    # lands in both neighbours. A chunk_chars-sized piece would force the seed-drop and silently
    # lose the straddling reading while still reporting complete=True (the honest-completeness bug).
    hard_split = max(1, chunk_chars - overlap)
    segments = []
    for line in text.splitlines(keepends=True):
        if len(line) > chunk_chars:
            while len(line) > hard_split:
                segments.append(line[:hard_split])
                line = line[hard_split:]
        if line:
            segments.append(line)

    chunks = []
    current = ""
    for segment in segments:
        if current and len(current) + len(segment) > chunk_chars:
            chunks.append(current)
            current = current[-overlap:] if overlap else ""
            if len(current) + len(segment) > chunk_chars:
                current = ""  # the seed would overflow this segment — drop it (segment <= chunk_chars)
        current += segment
    if current:
        chunks.append(current)
    return chunks
