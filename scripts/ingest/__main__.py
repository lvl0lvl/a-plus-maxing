"""Operator-facing ingestion CLI — load one export into your local instance.

`python -m scripts.ingest <path> [--source NAME]` loads a single operator data export,
locally and model-free:
- a wearable export (Apple Health `export.xml`, a Whoop sqlite, ...) -> the
  `vault/store/` time-series store via the UNCHANGED `ingest.run` (the adapter is
  auto-detected from the file extension, or named with `--source`);
- a DNA export (a 23andMe `.zip` or raw `.txt`) -> the gitignored `vault/dna/raw/`
  dropzone via `dna.land`.

It reads no stdin, opens no server, and makes no network call (ADR-0001 D1): the only
sink is the local store / the local dropzone — nothing is uploaded. The adapter set +
the store-write path are UNCHANGED (ADR-0003-T2); this is a thin operator entry over
them, parallel to the unattended `scheduler.run`.
"""

import argparse
import importlib
import sys
from pathlib import Path

from scripts.ingest import dna, ingest
from scripts.store import store

# Wearable source -> (adapter module, adapter class). The scheduler auto-discovers
# adapters for the unattended run; this operator CLI uses an explicit name map so
# `--source` is a closed choice set (kept congruent with the discovered wired set by
# test_cli_and_status_source_sets_match_scheduler_wired_set). DNA is handled separately (not a
# time-series adapter). whoop/oura/garmin map to the legacy file-drop parsers (their native manual
# export shapes); google-health is cloud-only (no native file), so its manual load reads a staged
# `{item, timepoint, value}` pull JSON via the cloud adapter.
_ADAPTERS = {
    "healthkit": ("scripts.ingest.adapters.healthkit", "HealthKitAdapter"),
    "whoop": ("scripts.ingest.adapters.whoop", "WhoopAdapter"),
    "oura": ("scripts.ingest.adapters.oura", "OuraAdapter"),
    "garmin": ("scripts.ingest.adapters.garmin", "GarminAdapter"),
    "google-health": ("scripts.ingest.adapters.google_health_cloud", "GoogleHealthCloudAdapter"),
}
_SOURCES = sorted([*_ADAPTERS, "dna"])

# Auto-detect the source from the file extension for the unambiguous cases (the two the
# operator actually uses: Apple Health `.xml`, DNA `.zip`). Ambiguous extensions
# (`.json` = oura|garmin, a raw `.txt`) require an explicit `--source`.
_EXT_SOURCE = {".xml": "healthkit", ".zip": "dna", ".sqlite": "whoop", ".db": "whoop"}


def _detect_source(path):
    """Infer the source from the file extension, or exit asking for `--source`."""
    source = _EXT_SOURCE.get(path.suffix.lower())
    if source is None:
        raise SystemExit(
            f"cannot infer the source of {path.name} from its extension; "
            f"pass --source (one of: {', '.join(_SOURCES)})"
        )
    return source


def _adapter(source):
    """Construct the named wearable adapter."""
    module_name, class_name = _ADAPTERS[source]
    return getattr(importlib.import_module(module_name), class_name)()


def _date_range(timepoints):
    """Return the (earliest, latest) calendar day across the timepoints' date prefixes."""
    days = sorted(t[:10] for t in timepoints)
    return (days[0], days[-1]) if days else ("", "")


def _load_wearable(source, path, root):
    """Run the named wearable adapter over `path`; report the per-item delta + day range."""
    adapter = _adapter(source)
    tag = adapter.source_tag()
    before = sum(1 for r in store.read_all(root) if r.get("source") == tag)
    ingest.run(adapter, path, root=root)
    after = [r for r in store.read_all(root) if r.get("source") == tag]

    print(f"Loaded {source} from {path.name} — {len(after) - before} new reading(s) "
          "into your local store.")
    by_item = {}
    for reading in after:
        by_item.setdefault(reading["item"], []).append(reading["timepoint"])
    for item in sorted(by_item):
        lo, hi = _date_range(by_item[item])
        span = f"{lo} .. {hi}" if lo != hi else lo
        print(f"  {item:<14}{len(by_item[item]):>7} reading(s)   {span}")
    print("Parsed locally into your store — nothing was uploaded.")


def _load_dna(path, dna_root):
    """Land the DNA export in the gitignored dropzone; report the variant count only."""
    result = dna.land(path, dna_root)
    print(f"Landed DNA export {result['name']} — {result['variants']} variant(s) "
          f"into {dna_root} (gitignored).")
    print("Parsed locally — nothing was uploaded. Clinical-variant analysis is a "
          "separate, later step.")


def main(argv=None):
    """Load one export into the local instance and return 0; a failure exits non-zero.

    Args:
        argv (list, optional): Argument vector; defaults to `sys.argv[1:]`.

    Returns:
        (int) 0 on success.
    """
    parser = argparse.ArgumentParser(
        prog="python -m scripts.ingest",
        description="Load one operator data export into your local instance (no upload, no model).",
    )
    parser.add_argument("path", help="the export file (Apple Health export.xml, a DNA .zip, ...)")
    parser.add_argument("--source", choices=_SOURCES, default=None,
                        help="force the source; otherwise inferred from the file extension")
    parser.add_argument("--root", default=None, help="store root (default: vault/store/)")
    parser.add_argument("--dna-root", default=None, help="DNA dropzone (default: vault/dna/raw/)")
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"no such file: {path}")
    source = args.source or _detect_source(path)

    if source == "dna":
        dna_root = Path(args.dna_root) if args.dna_root else Path("vault/dna/raw")
        _load_dna(path, dna_root)
    else:
        root = args.root if args.root is not None else store.DEFAULT_ROOT
        _load_wearable(source, path, root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
