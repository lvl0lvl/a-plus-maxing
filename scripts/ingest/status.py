"""Ingestion load-state resolver — what has landed in the local instance, for the intake screen.

`resolve(store_read, *, dna_root, labs_root)` computes the per-source load-state the intake
screen's "Link your documents" cards render: which sources have landed (wearable readings in
the time-series store; a DNA / labs file in the gitignored dropzone) with counts + day ranges.
Pure over its inputs (the store read model + the dropzone roots) — no model, no network. It
surfaces COUNTS only, never reading values or genotype content.
"""

from pathlib import Path

# The wearable sources whose readings land in the time-series store (the DNA/labs dropzones
# are separate gitignored landing dirs, not the store).
_WEARABLE_SOURCES = ("healthkit", "whoop", "oura", "garmin")


def _wearable(store_read):
    """Load-state of the wearable stream: loaded?, total readings, items, day range, source."""
    rows = [r for r in store_read if r.get("source") in _WEARABLE_SOURCES]
    if not rows:
        return {"loaded": False}
    days = sorted(r["timepoint"][:10] for r in rows)
    return {
        "loaded": True,
        "count": len(rows),
        "items": sorted({r["item"] for r in rows}),
        "range": (days[0], days[-1]),
        "source": rows[0]["source"],
    }


def _dropzone(root, suffixes):
    """Load-state of a file dropzone: loaded? + the landed file names (no content read)."""
    path = Path(root)
    if not path.exists():
        return {"loaded": False, "files": []}
    files = sorted(f.name for f in path.iterdir() if f.is_file() and f.suffix.lower() in suffixes)
    return {"loaded": bool(files), "files": files}


def resolve(store_read, *, dna_root, labs_root):
    """Return the per-source ingestion load-state for the intake screen.

    Args:
        store_read (list): The store read model (reading dicts).
        dna_root (str | Path): The DNA dropzone (production: `vault/dna/raw/`).
        labs_root (str | Path): The labs dropzone (production: `vault/labs/raw/`).

    Returns:
        (dict) `{"wearable": {...}, "dna": {...}, "labs": {...}}` — load-state + counts only.
    """
    return {
        "wearable": _wearable(store_read),
        "dna": _dropzone(dna_root, {".txt"}),
        "labs": _dropzone(labs_root, {".pdf", ".csv", ".txt", ".json"}),
    }
