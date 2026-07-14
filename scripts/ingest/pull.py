"""Tracker-pull orchestration — fetch the wired API sources + the watched folder, then land them.

`main()` (`python -m scripts.ingest.pull`) is the NEW caller of the UNCHANGED `scheduler.run`: under
the runner store lock it builds the `exports` map — fetch each wired API-pull source (Build A: Whoop)
to a gitignored staged file via the shared OAuth/fetch layer, plus scan the Apple-Health watched
folder — then calls `scheduler.run(exports, root)`, which runs the UNCHANGED `ingest.run` -> unchanged
`store.append` per source. It is a new caller, not an edit: `scheduler.run`, `ingest.run`,
`store.append`, and the `(item, timepoint, source)` dedupe are reused byte-unchanged, so a re-run
appends 0 duplicates and correctness rests on the store key, not on the fetch window.

Apple Health has no cloud REST API, so it is not an API-pull source — an operator Shortcut drops an
Apple Health export into a gitignored watched folder (`vault/inbox/healthkit/`) and the tick ingests
the newest one through the existing, byte-unchanged `healthkit` adapter (automated PLACEMENT, zero
new adapter code; the full cumulative dump dedups to a no-op on a re-drop).

DISABLED BY DEFAULT: importing or building this module arms no scheduled entry — nothing self-arms.
The scheduled unattended cadence is armed once by the operator (the operator-gated LIVE step, the
same disabled-by-default posture the plan-loop cadence runner uses), so a build never authenticates
to a vendor on a timer without an explicit operator arm (PF-S63-02). A per-source fetch failure fails
closed for THAT source (0 readings, a loud diagnostic) but never blocks the others or the watched
folder — one expired token does not stop the Apple path.
"""

import argparse
import sys
import tempfile
from pathlib import Path

from scripts.ingest import oauth_pull, scheduler
from scripts.runner import store_lock
from scripts.store import store

# The wired API-pull sources this tick fetches, DERIVED from `oauth_pull._MANIFESTS` — the single
# source of truth for which sources have a cloud pull manifest (whoop / oura / garmin / google-health).
# Deriving it (rather than a second hardcoded tuple) closes the F2 silent-drift trap: a future
# `<source>_cloud` adapter is fetched the moment its manifest is added, and one that is wired +
# status-listed but MISSING a manifest can no longer be silently never-fetched (the cli/status/scheduler
# congruence guard `test_cli_and_status_source_sets_match_scheduler_wired_set` reds). The dict order is
# the fetch/land order. A per-source fetch failure fails closed for THAT source only (0 readings, loud).
_API_PULL_SOURCES = tuple(oauth_pull._MANIFESTS)

# The watched-folder source tags (ingested from the gitignored inbox drop, NOT the cloud API — Apple
# Health has no cloud REST API). Named so the congruence guard can assert the API-pull set is exactly
# the discovered wired set MINUS the watched-folder sources.
WATCHED_FOLDER_SOURCES = ("healthkit",)

# The gitignored Apple-Health watched folder the operator Shortcut drops exports into. The tick scans
# `<watched-root>/healthkit/` for the newest export and ingests it via the unchanged healthkit adapter.
WATCHED_ROOT_DEFAULT = Path("vault/inbox")

# The distinct scheduler label for the tracker-pull cadence — registered so the operator can arm this
# tick under its own name (pointing at `python -m scripts.ingest.pull`), separate from the plan-loop
# cadence label. Registration only: the build installs no scheduled entry (disabled by default); the
# actual arming is the operator-gated LIVE step, mirroring the daily-monitor label's deferral.
TRACKER_PULL_LABEL = "com.aplusmaxing.tracker-pull"


def _since_for(source, root):
    """Return the latest stored calendar day for `source` (the fetch delta cursor), or None.

    A bandwidth optimization only: the store's `(item, timepoint, source)` dedupe makes an over-fetch
    land 0 duplicates, so correctness does not depend on this cursor's precision. The cursor is a date
    derived from the store's timepoints — a request parameter, never store content (ADR-0001 §4).
    """
    days = [r["timepoint"][:10] for r in store.read_all(root) if r.get("source") == source]
    return max(days) if days else None


def _scan_watched_folder(watched_root):
    """Return the newest Apple-Health export in `<watched_root>/healthkit/`, or None when empty.

    Selects the most recently modified `.xml`/`.zip` export the operator Shortcut dropped. Re-ingesting
    the same (full cumulative) export is a safe no-op via the healthkit daily-mean dedupe, so returning
    an already-seen file is harmless.

    Args:
        watched_root (str | Path): The watched-folder root (its `healthkit/` child is scanned).

    Returns:
        (Path | None) The newest export path, or None when the folder is absent or empty.
    """
    healthkit_dir = Path(watched_root) / "healthkit"
    if not healthkit_dir.is_dir():
        return None
    exports = [p for p in healthkit_dir.iterdir()
               if p.is_file() and p.suffix.lower() in (".xml", ".zip")]
    if not exports:
        return None
    return max(exports, key=lambda p: p.stat().st_mtime)


def main(argv=None):
    """Run one tracker-pull tick (fetch the API sources + the watched folder) and land it; return 0.

    Acquires the runner store lock over the tick's read-modify-write; a busy tick defers (returns 0
    without fetching or writing, catching up on the next tick). For each wired API-pull source it
    fetches the delta to a staged file (a fail-closed fetch error for one source is logged loudly and
    skipped, never aborting the tick), adds the watched-folder Apple export, and calls the UNCHANGED
    `scheduler.run`.

    Args:
        argv (list, optional): Argument vector; defaults to `sys.argv[1:]`.

    Returns:
        (int) 0 — the tick completed (or deferred on a busy lock).
    """
    parser = argparse.ArgumentParser(
        prog="python -m scripts.ingest.pull",
        description="Pull the wired tracker sources + the watched folder into your local store "
                    "(no upload of store content, no model step).",
    )
    parser.add_argument("--root", default=None, help="store root (default: vault/store/)")
    parser.add_argument("--watched-root", default=None,
                        help="Apple-Health watched-folder root (default: vault/inbox/)")
    args = parser.parse_args(argv)

    root = args.root if args.root is not None else store.DEFAULT_ROOT
    watched_root = Path(args.watched_root) if args.watched_root else WATCHED_ROOT_DEFAULT

    with store_lock.cadence_lock(root) as acquired:
        if not acquired:
            print("tracker-pull: another tick holds the store lock; deferring to the next tick",
                  file=sys.stderr)
            return 0
        exports = {}
        with tempfile.TemporaryDirectory(prefix="tracker-pull-") as staged_dir:
            for source in _API_PULL_SOURCES:
                try:
                    staged = oauth_pull.fetch(source, since=_since_for(source, root),
                                              staged_dir=staged_dir)
                    exports[source] = staged
                except oauth_pull.TrackerPullError as exc:
                    # Fail-closed for THIS source (0 readings), loud, and decoupled: an expired token
                    # for one source never blocks the others or the watched folder.
                    print(f"tracker-pull: {source} fetch failed, skipping this tick ({exc})",
                          file=sys.stderr)
            watched = _scan_watched_folder(watched_root)
            if watched is not None:
                exports[WATCHED_FOLDER_SOURCES[0]] = watched
            # Land each source in its OWN try/except (M1): a malformed/partial export for one source
            # (e.g. a truncated watched Apple export raising ET.ParseError) must never crash the tick
            # or drop the OTHER sources' already-fetched readings. A per-source `scheduler.run({tag:
            # path})` call is equivalent to the single batched call for the ADR-0003-T3 delta/dedup —
            # the store `(item, day, source)` key owns dedup, not the batching — so isolating the land
            # does not change what is stored. A land failure is logged loud and skipped, exactly as the
            # fetch loop above isolates a per-source fetch failure; the tick then returns normally.
            for tag, path in exports.items():
                try:
                    scheduler.run({tag: path}, root=root)
                except Exception as exc:
                    print(f"tracker-pull: {tag} land failed, skipping this tick ({exc})",
                          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
