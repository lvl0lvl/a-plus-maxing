"""Fresh-clone init step (ADR-0005-T2) — the git-clone -> fillable instance entry.

`run(clone_root)` is the one command a new operator runs after `git clone` to
reach a fillable, PII-free local instance. It initializes the local NDJSON store
under the gitignored `vault/store/` root through the ADR-0002-T1 store API and
surfaces the empty `status: scaffold` pages in their unfilled state — it seeds no
reading and rewrites no scaffold. Every read and write stays under the clone root:
no path outside it, no other clone's store, no network. Data entered after init
lands untracked via the ADR-0005-T1 `.gitignore` boundary, so a clone carries no
operator data (the accepted no-VC-backup trade-off — see docs/clone-init.md).

This is a THIN LEAF entry point (ADR-0005-T2 has 0 outgoing dependency edges); it
CONSUMES the store (`store.read` / `vault/store/` root), and at Wave 4 the dashboard
generation runs through the ADR-0004-T1 `render.emit`. It publishes no new shared
signature.
"""

from pathlib import Path

from scripts.store import store

# Tracked vault dir the `status: scaffold` pages live in (the same status:scaffold
# convention as vault/meta/*.md). The concrete path is not pinned upstream
# (recipe scaffold-page UPSTREAM FLAG); recorded here for the orchestrator to
# formalize across .gitignore / spec / the AC-1 test.
SCAFFOLD_DIR = "vault/scaffold"

# Store root relative to the clone root — the gitignored boundary entered data
# lands under (ADR-0005-T1 `.gitignore` excludes `vault/store/`).
STORE_SUBDIR = store.DEFAULT_ROOT


def _resolve_clone_root(clone_root):
    """Resolve the clone root, failing fast/visibly if it does not exist.

    Args:
        clone_root (str | Path): The clone root to initialize.

    Returns:
        (Path) The resolved clone root.

    Raises:
        FileNotFoundError: The clone root does not exist (no out-of-root fallback).
    """
    root = Path(clone_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"clone root does not exist: {root}")
    return root


def _init_store(clone_root):
    """Initialize the local store root so `store.read` returns an empty-but-well-formed read.

    Creates the gitignored `vault/store/` directory under the clone root. No reading
    is seeded; a subsequent `store.read` over the local store returns an empty
    reading set, not a missing-store error.
    """
    (clone_root / STORE_SUBDIR).mkdir(parents=True, exist_ok=True)


def _surface_scaffolds(clone_root):
    """Surface the empty `status: scaffold` pages in their unfilled state.

    Returns the scaffold pages present under the tracked scaffold dir without
    filling or rewriting them. A clone ships these pages tracked; init does not
    create or modify them.

    Returns:
        (list) The scaffold-page Paths surfaced (empty when none are present).
    """
    scaffold = clone_root / SCAFFOLD_DIR
    if not scaffold.is_dir():
        return []
    return sorted(p for p in scaffold.glob("*.md") if p.is_file())


def run(clone_root=Path(".")):
    """Initialize a fresh clone into a fillable, PII-free local instance.

    Initializes the local store (0 operator readings, readable empty-but-well-formed)
    and surfaces the empty `status: scaffold` pages, staying entirely within the
    clone root (0 cross-clone path, 0 network). Entered data lands untracked via the
    ADR-0005-T1 `.gitignore` boundary.

    Args:
        clone_root (str | Path, optional): The clone root to initialize. Defaults to
            the current directory (the cloned repo root in production).

    Returns:
        (list) The scaffold-page Paths surfaced.

    Raises:
        FileNotFoundError: The clone root does not exist.
    """
    root = _resolve_clone_root(clone_root)
    _init_store(root)
    return _surface_scaffolds(root)
