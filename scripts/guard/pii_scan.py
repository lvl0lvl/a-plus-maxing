"""Tracked-file operator-PII scanner (ADR-0001-T0 selected token set).

`scan(tracked_files) -> int` reads each supplied file's CONTENTS and returns the
total count of operator-PII matches. When the count is >=1, each offending file
is named via the single pinned channel — a `PII-HIT: <path>` line on stderr —
which the ADR-0005-T1 pre-commit hook reads. The `tracked_files` list is the
caller's current staged/tracked set captured at invocation; `scan` does not
re-enumerate (the hook passes its own `--staged` set, closing the
add-after-enumeration TOCTOU window).

Operator-identity tokens (the operator's name) load at run time from the
GITIGNORED `vault/meta/operator-identity.txt`, so this tracked scanner carries
NO operator PII and the trunk is shareable. A fresh clone has no such file, so
identity detection is simply empty there while the operator-AGNOSTIC patterns
still run. The operator-agnostic set is the generic `@gmail.com` contact pattern
plus the two structural `{item, timepoint, source, value}` store-line patterns;
none of those carry personal data.

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
from pathlib import Path

# Operator-AGNOSTIC patterns (no personal data): the generic contact pattern and
# the two field-order structural store-line patterns. Tracked, exposed so a test
# can pin the tracked set to the spike's agnostic patterns.
AGNOSTIC_PATTERNS = {
    "contact": r"[A-Za-z0-9._%+-]+@gmail\.com",
    "health-data-item-then-tp": (
        r'("item"|"value")[\s\S]{0,400}?"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'
    ),
    "health-data-tp-then-item": (
        r'"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}[\s\S]{0,400}?("item"|"value")'
    ),
}

# Structural store-line patterns match across newlines (a pretty-printed reading
# spans lines); the contact pattern is single-line either way.
_COMPILED_AGNOSTIC = [re.compile(p, re.DOTALL) for p in AGNOSTIC_PATTERNS.values()]

# Operator-identity tokens load from this GITIGNORED file (one regex per line);
# absent on a fresh clone -> empty identity set. Keeps operator PII out of tracked
# source.
DEFAULT_IDENTITY_CONFIG = Path("vault/meta/operator-identity.txt")


def _load_identity_patterns(config_path):
    """Compile the operator-identity regexes from the gitignored config.

    Args:
        config_path (str | Path): Path to the identity config; one regex token
            per non-blank, non-`#`-comment line.

    Returns:
        (list[re.Pattern]) One compiled pattern per token line, or `[]` when the
        file is absent (a fresh clone carries no identity tokens).
    """
    path = Path(config_path)
    if not path.exists():
        return []
    patterns = []
    for line in path.read_text(encoding="utf-8").splitlines():
        token = line.strip()
        if token and not token.startswith("#"):
            patterns.append(re.compile(token, re.DOTALL))
    return patterns


def scan(tracked_files, identity_config=DEFAULT_IDENTITY_CONFIG):
    """Count operator-PII matches across the contents of the supplied files.

    Args:
        tracked_files (iterable[str]): Paths to scan (the caller's current
            staged/tracked set; not re-enumerated here).
        identity_config (str | Path, optional): Path to the gitignored
            operator-identity token file; absent -> identity detection is empty.

    Returns:
        (int) Total number of operator-PII matches across the files' contents.
        Each file with >=1 match is named on stderr as `PII-HIT: <path>`.
    """
    patterns = _COMPILED_AGNOSTIC + _load_identity_patterns(identity_config)
    total = 0
    for path in tracked_files:
        try:
            with open(path, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        hits = sum(len(pattern.findall(text)) for pattern in patterns)
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
