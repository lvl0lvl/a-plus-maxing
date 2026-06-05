"""Shared ingestion routine: adapter import, dedupe, manual-entry/CSV fallback (ADR-0003-T1).

`run(adapter, export_file)` reads an export through the `adapter.py` contract and
writes each reading into the local store via `store.append`. `manual_entry` and
`import_csv` are the operator fallbacks for sources without a wired adapter; both
land in the SAME `vault/store/` files through the SAME `store.append` path. Dedupe
is inherited through `store.append`, which owns the single `keying.dedupe_key`
call; this module imports no keying and defines no key of its own. Because every
write flows through `store.append`, a re-run appends 0 duplicate lines and an
export mixing stored and new timepoints appends only the new-timepoint delta. The
only sink is the local store via `store.append`: no raw NDJSON write, no model
step (ADR-0001 No-Raw-Reading-To-Model Rule; ADR-0003 Risk N3 single-key + Risk
N2 inherited field-set rejection).
"""

import csv

from scripts.store import store


def _store_reading(reading, root):
    """Write one reading into its item's store file via `store.append`.

    Derives the item from the reading itself (`reading["item"]`) so the file an
    `append` writes and the `item` field it stores cannot diverge. A reading
    missing `item` raises `ValueError` — the same failure `store.append` raises
    for every other missing Line Field Set field — so the missing-field error is
    uniform across all fields. Every write goes through `store.append` (shared-key
    dedupe + field-set rejection inherited from the store), never a raw NDJSON
    write, never a second dedupe key.
    """
    if "item" not in reading:
        raise ValueError(
            f"reading missing required field(s); needs {store.keying.LINE_FIELDS}"
        )
    store.append(reading["item"], reading, root=root)


def run(adapter, export_file, root=store.DEFAULT_ROOT):
    """Import an adapter's export into the store in one invocation.

    Reads the export's readings via the adapter contract and writes each through
    `store.append`. Idempotent on the shared `(item, timepoint, source)` key: a
    re-run over already-stored readings appends 0 duplicate lines, and an export
    mixing stored and new timepoints appends only the new-timepoint delta. Writes
    only to the store; invokes no model step.

    A reading missing any Line Field Set field (including `item`) raises
    `ValueError` — the missing-field failure is uniform across all fields.

    Args:
        adapter (Adapter): A source adapter exposing `source_tag()` and
            `read_readings(export_file)` per `scripts/ingest/adapter.py`.
        export_file (str | Path): The source export the adapter reads.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.
    """
    for reading in adapter.read_readings(export_file):
        _store_reading(reading, root)


def manual_entry(item, reading, root=store.DEFAULT_ROOT):
    """Write one operator-supplied reading into the same store as adapter imports.

    The manual fallback for an item without a wired adapter. Writes through the
    same `store.append` path as `run` (same shared key, same field-set rejection,
    same per-item file); no raw write, no model step. The `item` argument must
    equal `reading["item"]`; a mismatch raises `ValueError` so the file an
    `append` writes and the `item` field it stores cannot diverge.

    Args:
        item (str): The item identifier (names the item's store file). Must equal
            `reading["item"]`.
        reading (dict): A reading carrying every Line Field Set field.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.
    """
    if "item" in reading and reading["item"] != item:
        raise ValueError(
            f"item {item!r} disagrees with reading item {reading['item']!r}"
        )
    _store_reading(reading, root)


def import_csv(path, root=store.DEFAULT_ROOT):
    """Import a CSV of readings into the store via the shared `store.append` path.

    Each CSV row is a Line-Field-Set reading (columns: item, timepoint, source,
    value); every row lands in its item's store file through `store.append` (same
    dedupe + field-set path as adapter imports). No raw write, no model step.

    `csv.DictReader` yields all-string fields, so a CSV `value` is stored as a
    string (unlike an adapter/JSON reading, which may carry a numeric value); the
    store is value-type-agnostic, and the dedupe identity is the
    `(item, timepoint, source)` tuple only, so a string vs numeric value does not
    change a reading's dedupe key.

    The whole CSV is parsed and validated before any write (all-or-nothing at the
    validation boundary), so a bad row never leaves a partial import behind. A
    header whose columns do not cover `keying.LINE_FIELDS`, a ragged row (extra
    columns, surfaced by `csv.DictReader` as a `None` key), or a row with a
    missing or empty required field each raises `ValueError` and writes nothing.

    Args:
        path (str | Path): The CSV file to import.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.
    """
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is not None and not set(
            store.keying.LINE_FIELDS
        ).issubset(reader.fieldnames):
            raise ValueError(
                f"CSV header {reader.fieldnames} does not cover "
                f"{store.keying.LINE_FIELDS}"
            )

        readings = []
        for row in reader:
            if None in row:
                raise ValueError("CSV row has more columns than the header")
            reading = dict(row)
            for field in store.keying.LINE_FIELDS:
                if not reading.get(field):
                    raise ValueError(
                        f"CSV row missing required field {field!r}: {reading!r}"
                    )
            readings.append(reading)

    for reading in readings:
        _store_reading(reading, root)
