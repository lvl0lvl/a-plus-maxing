"""Tracked-file operator-PII scanner (ADR-0001-T0 selected token set).

`scan(tracked_files) -> int` reads each supplied file's CONTENTS and returns the
total count of operator-PII matches across the spike's declared token set. When
the count is >=1, each offending file is named via the single pinned channel — a
`PII-HIT: <path>` line on stderr — which the ADR-0005-T1 pre-commit hook reads.
The `tracked_files` list is the caller's current staged/tracked set captured at
invocation; `scan` does not re-enumerate (the hook passes its own `--staged`
set, closing the add-after-enumeration TOCTOU window).

Deviation from the spike's literal scan command (implementation mechanism only):
the spike names `git ls-files -z | xargs -0 rg ...`; this host's `rg` is a shell-
function shim `xargs` cannot exec (that pipeline returns exit 127 here), and the
published surface is `scan(list[str]) -> int`. The patterns are re-expressed as
Python `re` applied to each file's CONTENTS — same patterns, same contents-search
semantics, portable. The selected token set and contents-search are unchanged.
"""

import re
import subprocess
import sys

# The spike's declared operator-PII token set, one entry per declared class
# (identity, contact, and the two field-order structural store-line patterns).
# Exposed so a test can assert the implemented set EQUALS the declared set.
TOKEN_PATTERNS = {
    "identity": r"Walter|McGivney",
    "contact": r"[A-Za-z0-9._%+-]+@gmail\.com",
    "health-data-item-then-tp": (
        r'("item"|"value").*"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'
    ),
    "health-data-tp-then-item": (
        r'"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}.*("item"|"value")'
    ),
}

_COMPILED = [re.compile(p) for p in TOKEN_PATTERNS.values()]


def scan(tracked_files):
    """Count operator-PII matches across the contents of the supplied files.

    Args:
        tracked_files (iterable[str]): Paths to scan (the caller's current
            staged/tracked set; not re-enumerated here).

    Returns:
        (int) Total number of operator-PII matches across the files' contents.
        Each file with >=1 match is named on stderr as `PII-HIT: <path>`.
    """
    total = 0
    for path in tracked_files:
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except (FileNotFoundError, IsADirectoryError):
            continue
        hits = sum(len(pattern.findall(text)) for pattern in _COMPILED)
        if hits:
            total += hits
            print(f"PII-HIT: {path}", file=sys.stderr)
    return total


def store_is_gitignored(repo_root):
    """Report whether `vault/store/` is gitignored in the given repo.

    Args:
        repo_root (str | Path): A git repo root to check.

    Returns:
        (bool) True when `git check-ignore vault/store/` exits 0 (entry present),
        False when it does not (AC-4: falsifiable in both directions).
    """
    return (
        subprocess.run(
            ["git", "check-ignore", "vault/store/"],
            cwd=repo_root,
            capture_output=True,
        ).returncode
        == 0
    )
