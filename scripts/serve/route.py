"""Upload-routing seam — map a browser-staged file into the unchanged ingest seam (ADR-0013-T4).

`route_upload(staged_path, *, root, dna_root)` is the website's front-door router: it
maps a file already staged by `multipart.stage_uploads` (ADR-0013-T2) to a source and
dispatches it into the UNCHANGED `ingest.run` (wearable) / `dna.land` (DNA) seam. The
source-detection REUSES the CLI's `_EXT_SOURCE` / `_detect_source`
(scripts/ingest/__main__.py:39,42) — it defines NO second extension->source map. The one
disambiguation the website adds over the CLI is the `.zip` content-branch: the CLI maps
`.zip -> dna`, but the browser uploads BOTH an Apple-Health export zip (whose adapter,
ADR-0013-T3, accepts the zip) and a 23andMe zip, so a `.zip` is branched on its CONTENT —
an Apple-Health-export shape (`*/export.xml` inside) routes to healthkit; a 23andMe shape
routes to dna.

A recognized format adds NO extraction logic (ADR-0013 "this server still adds no
extraction logic"): an Apple-Health zip is passed AS-IS to the zip-aware healthkit adapter,
which extracts `export.xml` itself. The shared ingest routines (`ingest.py`/`adapter.py`/
`scheduler.py`/`dna.py`) — and the byte-frozen plan engine — are unchanged by this module
(ADR-0003 0-shared-routine-edit / ADR-0030 NFR-4) — it CALLS the seam, never re-implements
the import/land.

ADR-0030-T2 adds ONE front-door branch: an UNRECOGNIZED extension (one `_detect_source`
cannot map) routes through the injected no-train extract lane — `client.extract_readings`
(ADR-0030-T1) over the staged file read from the gitignored staged path only — and RETURNS
the extracted readings as the awaiting-confirm payload (they do NOT auto-land; the operator
confirm step lands the confirmed subset). The file content reaches ONLY the injected client;
this module imports no outbound client / SDK. With no client injected the unrecognized-format
SystemExit is preserved (today's no-client contract byte-unchanged).
"""

import mimetypes
import zipfile
from pathlib import Path

from scripts.ingest import dna, ingest
from scripts.ingest.__main__ import _adapter, _detect_source
from scripts.ingest.adapters.healthkit import _export_xml_member
from scripts.store import store

# The production DNA dropzone — the CLI's `_load_dna` default (scripts/ingest/__main__.py:120).
# The store default lives in `store.DEFAULT_ROOT`; both resolve a `None` root to the real instance.
_DEFAULT_DNA_ROOT = Path("vault/dna/raw")


def _zip_is_apple_health(zip_path):
    """Return True if the `.zip` is an Apple-Health export (carries a `*/export.xml` member).

    The content-disambiguation between the two zip shapes the browser uploads: an
    Apple-Health export nests `export.xml` under a directory member, a 23andMe export
    carries a genotype `.txt` and no `export.xml`. DELEGATES the member scan to the
    healthkit adapter's `_export_xml_member` so the "what makes a zip Apple-Health" rule
    lives in ONE place (the adapter that extracts it) — a True here means the same scan
    the adapter then runs will succeed.

    Args:
        zip_path (str | Path): Path to the staged `.zip` upload.

    Returns:
        (bool) True for an Apple-Health-export shape, False for a 23andMe shape.
    """
    with zipfile.ZipFile(zip_path) as zf:
        try:
            _export_xml_member(zf)
        except ValueError:
            return False
        return True


def route_upload(staged_path, *, client=None, root=None, dna_root=None):
    """Route a staged upload — a recognized format lands; an unrecognized format extracts.

    A RECOGNIZED format maps to a source — reusing the CLI's `_detect_source`/`_EXT_SOURCE`,
    content-branching a `.zip` (Apple-Health-export shape -> healthkit; 23andMe shape -> dna)
    — and dispatches into the UNCHANGED seam: a wearable source calls
    `ingest.run(adapter, staged_path, root)` (an Apple-Health zip is passed AS-IS to the
    zip-aware healthkit adapter, which extracts `export.xml` itself); a DNA upload calls
    `dna.land(staged_path, dna_root)`. That arm RETURNS the routed source string (today's
    contract) — no extraction, no store-write beyond the seam, no second extension->source map.

    An UNRECOGNIZED extension (one `_detect_source` cannot map) WITH an injected `client`
    routes the staged file through the no-train extract lane — `client.extract_readings`
    (ADR-0030-T1) over the file content read from the gitignored staged path only — and
    RETURNS the extracted readings as the awaiting-confirm payload (a `dict`, distinguishable
    from the recognized arm's source string). That arm makes 0 `store.append` / `dna.land`
    call: the readings do NOT auto-land (the operator confirm step lands the confirmed subset).
    With NO client injected the unrecognized-format `_detect_source` SystemExit is PRESERVED.

    A `None` `root`/`dna_root` resolves to the production `vault/store/` / `vault/dna/raw/`
    defaults (the operator-entry path `python -m scripts.serve`, which builds the server
    with no roots); tests pass tmp roots so the E2E never touches the real instance.

    Args:
        staged_path (str | Path): The file staged by `multipart.stage_uploads`.
        client (ModelClient, optional): The injected no-train model client exposing
            `extract_readings`. When None, an unrecognized format preserves the SystemExit.
        root (str | Path, optional): The store root the wearable dispatch writes.
            Defaults to `store.DEFAULT_ROOT` (`vault/store/`).
        dna_root (str | Path, optional): The DNA dropzone the DNA dispatch lands into.
            Defaults to `vault/dna/raw/`.

    Returns:
        (str) The source a recognized upload routed to ("healthkit"/"whoop"/"oura"/"garmin"/
        "dna"), OR (dict) `{"extracted_readings": list}` — the awaiting-confirm payload an
        unrecognized-format extraction routed to.
    """
    path = Path(staged_path)
    if path.suffix.lower() == ".zip":
        source = "healthkit" if _zip_is_apple_health(path) else "dna"
    else:
        try:
            source = _detect_source(path)
        except SystemExit:
            # No named adapter covers this extension. With a client injected, route the
            # staged file through the no-train extract lane (ADR-0030-T2); with no client,
            # preserve today's `_detect_source` SystemExit contract (byte-unchanged).
            if client is None:
                raise
            return _extract_unrecognized(path, client)

    if source == "dna":
        dna.land(path, dna_root if dna_root is not None else _DEFAULT_DNA_ROOT)
    else:
        ingest.run(_adapter(source), path, root=root if root is not None else store.DEFAULT_ROOT)
    return source


def _extract_unrecognized(path, client):
    """Route an unrecognized-format staged file through the no-train extract lane (ADR-0030-T2).

    Reads the staged file content from the gitignored staged path ONLY, derives the media type
    from its extension, and calls the injected `client.extract_readings(file_content, media_type)`.
    The extracted readings are RETURNED as the awaiting-confirm payload — they are NOT written to
    the store / DNA dropzone (the operator confirm step lands the confirmed subset). The file
    content reaches ONLY the injected client; nothing is written to any tracked path (OQ-5).

    Args:
        path (Path): The gitignored staged-upload path.
        client (ModelClient): The injected no-train model client exposing `extract_readings`.

    Returns:
        (dict) `{"extracted_readings": list}` — the awaiting-confirm payload, distinguishable
        from the recognized-format arm's source string.
    """
    file_content = path.read_bytes()
    media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {"extracted_readings": client.extract_readings(file_content, media_type)}
