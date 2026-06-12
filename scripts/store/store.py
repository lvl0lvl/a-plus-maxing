"""Local NDJSON store: per-item append/read over the gitignored store root.

One NDJSON file per item under the store root (ADR-0002-T0 File Granularity).
`append` validates and idempotently writes one line; `read` scans the item file
and returns readings ordered by timepoint; `items`/`read_all` publish the
cross-item surface (sorted item enumeration, flat item-then-timepoint-ordered
read model) so no consumer enumerates the on-disk layout itself. Local file
I/O only — no network, login, or model step (ADR-0001 D1->D2).
"""

import json
import os
import sys
import tempfile
from pathlib import Path

from scripts.store import keying

DEFAULT_ROOT = Path("vault/store")


def _item_path(item, root):
    # SEC: an untrusted ingestion `item` (CSV row / manual entry) must not escape
    # the gitignored store root. Reject any item whose resolved store path is not a
    # direct child of the root ("../x", absolute paths, "a/b" all escape; "" maps to
    # root/.ndjson which stays inside the root, so it is allowed, not an escape).
    base = Path(root).resolve()
    target = (base / f"{item}.ndjson").resolve()
    if target.parent != base:
        raise ValueError(f"unsafe item {item!r}: store path escapes the root")
    return target


def _read_lines(path):
    """Parse an item file into its well-formed, conformant reading dicts.

    Returns an empty list if the file is absent. A line is kept only if it is
    valid JSON, a `dict`, and carries every Line Field Set field
    (`keying.is_conformant`). Every other line — torn/partial JSON, a non-dict
    JSON value, or a dict missing a required field — is skipped, not raised on,
    and emits one `STORE-SKIP: <path>:<1-based-line-number>` warning to stderr.
    That channel is the store's corruption-detection signal (it parallels
    `pii_scan`'s `PII-HIT:` channel) and a consumer may depend on its format.
    Filtering here means both `read` (sort by timepoint) and `append` (dedupe)
    only ever see conformant dict readings.

    Args:
        path (Path): The item's `.ndjson` file.

    Returns:
        (list) The file's well-formed, conformant reading dicts, in file order.
    """
    if not path.exists():
        return []
    readings = []
    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            print(f"STORE-SKIP: {path}:{lineno}", file=sys.stderr)
            continue
        if not isinstance(obj, dict) or not keying.is_conformant(obj):
            print(f"STORE-SKIP: {path}:{lineno}", file=sys.stderr)
            continue
        readings.append(obj)
    return readings


def append(item, reading, root=DEFAULT_ROOT):
    """Append one reading to its item file by rewriting the file atomically.

    Rewrites the item file as its well-formed prior lines plus the new line
    (write temp sibling -> fsync -> `os.replace`). Idempotent on the dedupe
    identity: re-appending a reading with the same `(item, timepoint, source)`
    is a no-op. Self-heals: pre-existing malformed or non-conformant lines are
    dropped on write (`_read_lines` filters them). Prior lines' logical content
    is preserved, but their exact on-disk byte form is not guaranteed stable
    across appends (they are re-serialized).

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

    # Write the full file to a temp sibling, then os.replace. os.replace is atomic
    # on POSIX, so a reader never sees a torn line — it sees either the complete old
    # file or the complete new one. fsync before the replace makes the new bytes
    # durable on disk first, so a crash after the rename cannot expose empty/short
    # content. Self-heals: malformed lines were already dropped by _read_lines.
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f"{path.name}.", suffix=".tmp")
    try:
        # os.fdopen takes ownership of fd; close fd directly only if it raises first.
        try:
            fh = os.fdopen(fd, "w")
        except BaseException:
            os.close(fd)
            raise
        with fh:
            fh.write("".join(lines))
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        # Broader than Exception on purpose: an interrupt (e.g. KeyboardInterrupt)
        # mid-write must still unlink the orphan temp so no stray sibling is left.
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def read(item, root=DEFAULT_ROOT):
    """Return the item's well-formed, conformant readings ordered by timepoint.

    Returns only lines that are valid JSON, a `dict`, and carry every Line Field
    Set field. Malformed or non-conformant lines are skipped (not raised on) and
    each emits one `STORE-SKIP: <path>:<1-based-line-number>` line on stderr, so
    the returned list may be a proper subset of the readings ever appended if the
    file was corrupted. The ordering is lexicographic on the `timepoint` string
    and assumes the spike's UTC-offset producer obligation; a non-UTC-offset
    timepoint would sort wrong.

    Args:
        item (str): The item identifier.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (list) The item's well-formed readings, sorted by their `timepoint` field.
    """
    readings = _read_lines(_item_path(item, root))
    return sorted(readings, key=lambda r: r["timepoint"])


def items(root=DEFAULT_ROOT):
    """Return the sorted item identifiers stored under the store root.

    Owns the one-`.ndjson`-file-per-item layout knowledge (ADR-0002-T0 File
    Granularity): an item is stored iff its `.ndjson` file exists under the
    root. A missing or empty root yields an empty list.

    Args:
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (list) The stored item identifiers, sorted lexicographically.
    """
    return sorted(p.stem for p in Path(root).glob("*.ndjson"))


def read_all(root=DEFAULT_ROOT):
    """Return every stored item's readings as one flat cross-item list.

    Concatenates `read(item, root=root)` over `items(root)`: the outer order
    is item-name lexicographic, the order within an item is `read`'s timepoint
    sort. Delegates through `read`, so malformed-line skipping behaves exactly
    as a per-item read (one `STORE-SKIP:` stderr line per skipped line).

    Args:
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (list) The flat list of reading dicts across every stored item.
    """
    readings = []
    for item in items(root):
        readings.extend(read(item, root=root))
    return readings
