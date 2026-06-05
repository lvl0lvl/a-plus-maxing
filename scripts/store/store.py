"""Local NDJSON store: per-item append/read over the gitignored store root.

One NDJSON file per item under the store root (ADR-0002-T0 File Granularity).
`append` validates and idempotently writes one line; `read` scans the item file
and returns readings ordered by timepoint. Local file I/O only — no network,
login, or model step (ADR-0001 D1->D2).
"""

import json
import os
import sys
import tempfile
from pathlib import Path

from scripts.store import keying

DEFAULT_ROOT = Path("vault/store")


def _item_path(item, root):
    return Path(root) / f"{item}.ndjson"


def _read_lines(path):
    """Parse an item file into a list of well-formed reading dicts (empty if absent).

    A malformed (torn/partial) line is skipped, not raised on: each skip emits one
    `STORE-SKIP: <path>:<1-based-line-number>` warning to stderr so a downstream
    consumer can detect dropped lines. The rest of the file still parses.
    """
    if not path.exists():
        return []
    readings = []
    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            readings.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"STORE-SKIP: {path}:{lineno}", file=sys.stderr)
    return readings


def append(item, reading, root=DEFAULT_ROOT):
    """Append one NDJSON line for a reading to its item file, idempotently.

    Args:
        item (str): The item identifier (names the item's `.ndjson` file).
        reading (dict): A reading carrying every Line Field Set field.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Raises:
        ValueError: The reading is missing a required Line Field Set field.
    """
    if not keying.is_conformant(reading):
        raise ValueError(
            f"reading missing required field(s); needs {keying.LINE_FIELDS}"
        )

    path = _item_path(item, root)
    well_formed = _read_lines(path)
    if keying.dedupe_key(reading) in {keying.dedupe_key(r) for r in well_formed}:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(r) + "\n" for r in (*well_formed, reading)]

    # Write the full file to a temp sibling, then os.replace — atomic on POSIX, so
    # a crash leaves either the complete old file or the complete new one, never a
    # torn line. This also self-heals: malformed lines were dropped by _read_lines.
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f"{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write("".join(lines))
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def read(item, root=DEFAULT_ROOT):
    """Return the item's readings ordered ascending by timepoint.

    The ordering is lexicographic on the `timepoint` string and assumes the
    spike's UTC-offset producer obligation; a non-UTC-offset timepoint would
    sort wrong.

    Args:
        item (str): The item identifier.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (list) The item's readings, sorted by their `timepoint` field.
    """
    readings = _read_lines(_item_path(item, root))
    return sorted(readings, key=lambda r: r["timepoint"])
