"""Local NDJSON store: per-item append/read over the gitignored store root.

One NDJSON file per item under the store root (ADR-0002-T0 File Granularity).
`append` validates and idempotently writes one line; `correct` appends a
SUPERSEDING line for an already-stored (item, timepoint, source) — the bead-1vi
explicit correction primitive, never an in-place mutation; `read` scans the
item file, resolves each (item, timepoint, source) identity to its
last-appended line (latest-wins), and returns readings ordered by timepoint;
`items`/`read_all` publish the cross-item surface (sorted item enumeration,
flat item-then-timepoint-ordered read model) so no consumer enumerates the
on-disk layout itself. Local file I/O only — no network, login, or model step
(ADR-0001 D1->D2).
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


def _write_atomic(path, readings):
    """Rewrite the item file as `readings`, one JSON line each, atomically.

    Write the full file to a temp sibling, then os.replace. os.replace is atomic
    on POSIX, so a reader never sees a torn line — it sees either the complete old
    file or the complete new one. fsync before the replace makes the new bytes
    durable on disk first, so a crash after the rename cannot expose empty/short
    content. Prior lines' logical content is preserved, but their exact on-disk
    byte form is not guaranteed stable across writes (they are re-serialized).

    Args:
        path (Path): The item's `.ndjson` file.
        readings (tuple | list): The conformant reading dicts to write, in order.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(r) + "\n" for r in readings]

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


def _resolve_latest(readings):
    """Collapse same-dedupe-key readings to the last one in file (append) order.

    The bead-1vi latest-wins read basis: a correction appends a superseding
    line for an already-stored `(item, timepoint, source)` (see `correct`), so
    among lines sharing that identity the LAST in file order — append order —
    is the current value; the same most-recent-wins resolution basis
    `loop_schema.read_panel` follows. Each surviving reading keeps its
    first-appearance position, so the relative order of distinct identities is
    unchanged.

    Args:
        readings (list): Conformant reading dicts in file order.

    Returns:
        (list) One reading per `(item, timepoint, source)` identity.
    """
    return list({keying.dedupe_key(r): r for r in readings}.values())


def append(item, reading, root=DEFAULT_ROOT):
    """Append one reading to its item file by rewriting the file atomically.

    Rewrites the item file as its well-formed prior lines plus the new line
    (write temp sibling -> fsync -> `os.replace`). Idempotent on the dedupe
    identity: re-appending a reading with the same `(item, timepoint, source)`
    is a no-op — value included or not, so the normal ingest path NEVER
    overrides a stored value (an intended value correction is an explicit
    `correct` call). Self-heals: pre-existing malformed or non-conformant lines
    are dropped on write (`_read_lines` filters them).

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
    _write_atomic(path, (*well_formed, reading))


def correct(item, reading, root=DEFAULT_ROOT):
    """Append a superseding value for an already-stored (item, timepoint, source).

    The bead-1vi explicit correction primitive: where `append` drops a re-entry
    whose dedupe identity is already stored, `correct` appends it as a new line
    DESPITE the dedupe, and `read` resolves the identity to this last-appended
    line (latest-wins). The prior line stays in the file untouched — the audit
    trail is append-only per ADR-0002, never mutated or deleted. Correcting an
    identity to the value it already resolves to is an idempotent no-op (a
    re-run appends 0 duplicate lines). An identity with no stored line raises:
    a correction targets an existing reading, so a mistyped item / timepoint /
    source fails loud instead of silently creating a new series point.

    Args:
        item (str): The item identifier (names the item's `.ndjson` file).
        reading (dict): The superseding reading, carrying every Line Field Set
            field; its `(item, timepoint, source)` must already be stored.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Raises:
        ValueError: The reading is missing a required Line Field Set field, or
            no stored reading carries its `(item, timepoint, source)` identity.
    """
    if not keying.is_conformant(reading):
        raise ValueError(
            f"reading missing required field(s); needs {keying.LINE_FIELDS}"
        )

    path = _item_path(item, root)
    well_formed = _read_lines(path)
    current = {keying.dedupe_key(r): r for r in well_formed}
    key = keying.dedupe_key(reading)
    if key not in current:
        raise ValueError(f"no stored reading with identity {key!r} to correct")
    if current[key]["value"] == reading["value"]:
        return
    _write_atomic(path, (*well_formed, reading))


def read(item, root=DEFAULT_ROOT):
    """Return the item's latest-wins-resolved readings ordered by timepoint.

    Returns only lines that are valid JSON, a `dict`, and carry every Line Field
    Set field. Malformed or non-conformant lines are skipped (not raised on) and
    each emits one `STORE-SKIP: <path>:<1-based-line-number>` line on stderr, so
    the returned list may be a proper subset of the readings ever appended if the
    file was corrupted. Lines sharing an `(item, timepoint, source)` identity
    are resolved to the LAST in file (append) order — a `correct` superseding
    append wins over the line it corrects (`_resolve_latest`), so every store
    consumer reads corrected values through this one surface. The ordering is
    lexicographic on the `timepoint` string and assumes the spike's UTC-offset
    producer obligation; a non-UTC-offset timepoint would sort wrong. A
    directory named `<item>.ndjson` under the root raises `IsADirectoryError` —
    fail-fast at the storage boundary, not guarded.

    Args:
        item (str): The item identifier.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (list) The item's resolved readings, sorted by their `timepoint` field.
    """
    readings = _resolve_latest(_read_lines(_item_path(item, root)))
    return sorted(readings, key=lambda r: r["timepoint"])


def items(root=DEFAULT_ROOT):
    """Return the sorted item identifiers stored under the store root.

    Owns the one-`.ndjson`-file-per-item layout knowledge (ADR-0002-T0 File
    Granularity): enumeration is by NAME only — every direct child named
    `*.ndjson` is an item slug, deliberately unfiltered by file-kind, so a
    directory named `*.ndjson` is enumerated too and `read` of its slug raises
    `IsADirectoryError` (the fail-fast storage-boundary contract). A missing or
    empty root yields an empty list.

    Args:
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (list) The stored item identifiers, sorted lexicographically.
    """
    # Exact inverse of _item_path's f"{item}.ndjson" naming: a literal suffix
    # strip, not p.stem — the dotfile `.ndjson` (the documented-allowed empty
    # item) is suffix-less to pathlib, so its stem would be a phantom slug.
    return sorted(p.name[: -len(".ndjson")] for p in Path(root).glob("*.ndjson"))


def read_all(root=DEFAULT_ROOT):
    """Return every stored item's readings as one flat cross-item list.

    Concatenates `read(item, root=root)` over `items(root)`: the outer order
    is item-name lexicographic, the order within an item is `read`'s timepoint
    sort. Delegates through `read`, so malformed-line skipping AND the
    latest-wins identity resolution behave exactly as a per-item read (one
    `STORE-SKIP:` stderr line per skipped line; one reading per identity). A
    directory named `*.ndjson` under the root raises `IsADirectoryError` out of
    its `read` — fail-fast at the storage boundary, not guarded.

    Args:
        root (str | Path, optional): Store root. Defaults to `vault/store/`.

    Returns:
        (list) The flat list of reading dicts across every stored item.
    """
    readings = []
    for item in items(root):
        readings.extend(read(item, root=root))
    return readings
