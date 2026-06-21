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

The router adds NO extraction logic (ADR-0013 "this server still adds no extraction
logic"): an Apple-Health zip is passed AS-IS to the zip-aware healthkit adapter, which
extracts `export.xml` itself. The shared ingest routines (`ingest.py`/`adapter.py`/
`scheduler.py`/`dna.py`) are byte-unchanged by this module (ADR-0003 0-shared-routine-edit
/ ADR-0013 "new front door") — it CALLS the seam, never re-implements the import/land.
"""

import zipfile
from pathlib import Path

from scripts.ingest import dna, ingest
from scripts.ingest.__main__ import _adapter, _detect_source
from scripts.store import store

# The production DNA dropzone — the CLI's `_load_dna` default (scripts/ingest/__main__.py:120).
# The store default lives in `store.DEFAULT_ROOT`; both resolve a `None` root to the real instance.
_DEFAULT_DNA_ROOT = Path("vault/dna/raw")


def _zip_is_apple_health(zip_path):
    """Return True if the `.zip` is an Apple-Health export (carries a `*/export.xml` member).

    The content-disambiguation between the two zip shapes the browser uploads: an
    Apple-Health export nests `export.xml` under a directory member, a 23andMe export
    carries a genotype `.txt` and no `export.xml`. Skips directory entries and macOS
    `__MACOSX` resource forks, mirroring the adapter/`dna.land` member scans.

    Args:
        zip_path (str | Path): Path to the staged `.zip` upload.

    Returns:
        (bool) True for an Apple-Health-export shape, False for a 23andMe shape.
    """
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.endswith("/") or name.startswith("__MACOSX"):
                continue
            if Path(name).name == "export.xml":
                return True
    return False


def route_upload(staged_path, *, root=None, dna_root=None):
    """Route a staged upload into the unchanged ingest seam by its detected source.

    Maps the staged file to a source — reusing the CLI's `_detect_source`/`_EXT_SOURCE`,
    content-branching a `.zip` (Apple-Health-export shape -> healthkit; 23andMe shape ->
    dna) — and dispatches: a wearable source constructs the named adapter and calls the
    UNCHANGED `ingest.run(adapter, staged_path, root)` (an Apple-Health zip is passed AS-IS
    to the zip-aware healthkit adapter, which extracts `export.xml` itself); a DNA upload
    calls the UNCHANGED `dna.land(staged_path, dna_root)`. Adds no extraction, no
    store-write, no second extension->source map.

    A `None` `root`/`dna_root` resolves to the production `vault/store/` / `vault/dna/raw/`
    defaults (the operator-entry path `python -m scripts.serve`, which builds the server
    with no roots); tests pass tmp roots so the E2E never touches the real instance.

    Args:
        staged_path (str | Path): The file staged by `multipart.stage_uploads`.
        root (str | Path, optional): The store root the wearable dispatch writes.
            Defaults to `store.DEFAULT_ROOT` (`vault/store/`).
        dna_root (str | Path, optional): The DNA dropzone the DNA dispatch lands into.
            Defaults to `vault/dna/raw/`.

    Returns:
        (str) The source the upload routed to ("healthkit"/"whoop"/"oura"/"garmin"/"dna").
    """
    path = Path(staged_path)
    if path.suffix.lower() == ".zip":
        source = "healthkit" if _zip_is_apple_health(path) else "dna"
    else:
        source = _detect_source(path)

    if source == "dna":
        dna.land(path, dna_root if dna_root is not None else _DEFAULT_DNA_ROOT)
    else:
        ingest.run(_adapter(source), path, root=root if root is not None else store.DEFAULT_ROOT)
    return source
