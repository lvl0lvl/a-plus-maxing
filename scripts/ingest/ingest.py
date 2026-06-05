"""Shared ingestion routine: adapter import, dedupe, manual-entry/CSV fallback (ADR-0003-T1).

`run(adapter, export_file)` reads an export through the `adapter.py` contract and
writes each reading into the local store via `store.append`. `manual_entry` and
`import_csv` are the operator fallbacks for sources without a wired adapter; both
land in the SAME `vault/store/` files through the SAME `store.append` path. The
dedupe key is the single shared `keying.dedupe_key` (no second key here), so a
re-run appends 0 duplicate lines and an export mixing stored and new timepoints
appends only the new-timepoint delta. The only sink is the local store via
`store.append`: no raw NDJSON write, no model step (ADR-0001 No-Raw-Reading-To-
Model Rule; ADR-0003 Risk N3 single-key + Risk N2 inherited field-set rejection).
"""

import csv

from scripts.store import store


def _store_reading(item, reading, root):
    """Write one reading into its item's store file via `store.append`.

    The single internal write path `run` / `manual_entry` / `import_csv` share:
    every write goes through `store.append` (shared-key dedupe + field-set
    rejection inherited from the store), never a raw NDJSON write, never a second
    dedupe key.
    """
    store.append(item, reading, root=root)


def run(adapter, export_file, root=store.DEFAULT_ROOT):
    """Import an adapter's export into the store in one invocation.

    Reads the export's readings via the adapter contract and writes each through
    `store.append`. Idempotent on the shared `(item, timepoint, source)` key: a
    re-run over already-stored readings appends 0 duplicate lines, and an export
    mixing stored and new timepoints appends only the new-timepoint delta. Writes
    only to the store; invokes no model step.

    Args:
        adapter (Adapter): A source adapter exposing `source_tag()` and
            `read_readings(export_file)` per `scripts/ingest/adapter.py`.
        export_file (str | Path): The source export the adapter reads.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.
    """
    for reading in adapter.read_readings(export_file):
        _store_reading(reading["item"], reading, root)


def manual_entry(item, reading, root=store.DEFAULT_ROOT):
    """Write one operator-supplied reading into the same store as adapter imports.

    The manual fallback for an item without a wired adapter. Writes through the
    same `store.append` path as `run` (same shared key, same field-set rejection,
    same per-item file); no raw write, no model step.

    Args:
        item (str): The item identifier (names the item's store file).
        reading (dict): A reading carrying every Line Field Set field.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.
    """
    _store_reading(item, reading, root)


def import_csv(path, root=store.DEFAULT_ROOT):
    """Import a CSV of readings into the store via the shared `store.append` path.

    Each CSV row is a Line-Field-Set reading (columns: item, timepoint, source,
    value); every row lands in its item's store file through `store.append` (same
    dedupe + field-set path as adapter imports). No raw write, no model step.

    Args:
        path (str | Path): The CSV file to import.
        root (str | Path, optional): Store root. Defaults to `vault/store/`.
    """
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            reading = dict(row)
            _store_reading(reading["item"], reading, root)
