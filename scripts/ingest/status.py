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


def wearable_status(store_read):
    """Load-state of the wearable stream: loaded?, total readings, items, day range, source.

    The public wearable-only resolver — `resolve` uses it for the full status, and the intake
    template's standalone render path consumes it directly (so it does not reach a private helper).

    Args:
        store_read (list): The store read model (reading dicts).

    Returns:
        (dict) `{"loaded": bool}` plus, when loaded, `count`/`items`/`range`/`source`.
    """
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


def dna_status(store_read, dna_root):
    """Load-state of DNA: a 23andMe file in the dropzone OR extracted genotype readings in the store.

    The dropzone scan recognizes a 23andMe `.txt` raw export only (the `{".txt"}` suffix filter); a
    `.zip` export arrives via a different path (the `python -m scripts.ingest 23andme.zip` unpack),
    not this dropzone listing. A genetics-report PDF instead lands as `source == "dna-report"`
    genotype readings in the store (ADR-0031 local extraction). Either counts as DNA loaded — `count`
    is the genotype-reading count when present, else the dropzone is returned unchanged. Surfaces
    counts only, never a genotype value.

    Args:
        store_read (list): The store read model (reading dicts).
        dna_root (str | Path): The DNA dropzone (production: `vault/dna/raw/`).

    Returns:
        (dict) `{"loaded": bool, "files": [...]}` plus `count` when genotype readings are present.
    """
    drop = _dropzone(dna_root, {".txt"})
    genotypes = [r for r in store_read if r.get("source") == "dna-report"]
    if genotypes:
        return {"loaded": True, "files": drop["files"], "count": len(genotypes)}
    return drop


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
        "wearable": wearable_status(store_read),
        "dna": dna_status(store_read, dna_root),
        "labs": _dropzone(labs_root, {".pdf", ".csv", ".txt", ".json"}),
    }
