"""Local NDJSON store: per-item append/read over the gitignored store root.

One NDJSON file per item under the store root (ADR-0002-T0 File Granularity).
`append` validates and idempotently writes one line; `read` scans the item file
and returns readings ordered by timepoint. Local file I/O only — no network,
login, or model step (ADR-0001 D1->D2).
"""

import json
from pathlib import Path

from scripts.store import keying

DEFAULT_ROOT = Path("vault/store")


def _item_path(item, root):
    return Path(root) / f"{item}.ndjson"


def _read_lines(path):
    """Parse an item file into a list of reading dicts (empty if absent)."""
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


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
    existing = {keying.dedupe_key(r) for r in _read_lines(path)}
    if keying.dedupe_key(reading) in existing:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(reading) + "\n")


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
