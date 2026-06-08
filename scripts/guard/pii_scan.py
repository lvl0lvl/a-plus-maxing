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
import unicodedata
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
# spans lines); the contact pattern is single-line either way. The contact pattern
# matches case-INSENSITIVELY (2x1): a non-canonical-case email (Op.User@Gmail.COM)
# is the same contact and must score a hit, not pass. The structural store-line
# patterns stay DOTALL-only (store keys are canonical lowercase JSON).
_CONTACT_COMPILED = re.compile(AGNOSTIC_PATTERNS["contact"], re.DOTALL | re.IGNORECASE)
_STRUCTURAL_COMPILED = [
    re.compile(p, re.DOTALL) for name, p in AGNOSTIC_PATTERNS.items() if name != "contact"
]
_COMPILED_AGNOSTIC = [_CONTACT_COMPILED] + _STRUCTURAL_COMPILED

# Value-boundary PII patterns (bead g5x): the FULL EXCLUDED_RAW_PII contact classes
# the router names — generic email (ANY domain, so @gmail.com / @googlemail.com / a
# non-gmail provider all hit), phone (E.164 + NANP), and a conservative US street
# address. Applied by `scan_text` (the runtime VALUE boundary feeding
# `router.summarize`) ONLY — NOT by `scan`. The trunk-wide commit scanner stays
# gmail-conservative on purpose: a generic-email / phone / postal pattern run across
# the whole tracked tree floods on docs + test fixtures, breaking clonability (the
# operator-specific commit-hook redesign is bead 3lv). Each entry point therefore
# carries its own pattern set; the identity loader is shared.
#
# Phone patterns anchor on `(?<!\d)`/`(?!\d)` and a digit-count floor so ISO
# timestamps (`08:00:00+00:00`) and bare numeric runs do not register. Postal
# requires >=1 street-NAME word between the number and the suffix (so "10 St John's
# Wort" — St as Saint — does not match) and matches the suffix CASE-SENSITIVELY in
# Title-case (so lowercase common words like "way"/"st"/"dr" in free text do not
# trip it; real addresses are conventionally capitalised).
_VALUE_PII_PATTERNS = {
    "email": (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.IGNORECASE),
    "phone-e164": (r"(?<!\d)\+\d{8,15}(?!\d)", 0),
    "phone-separated": (
        r"(?<!\d)(?:\+?\d{1,3}[\s.\-])?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)",
        0,
    ),
    "postal-us": (
        r"(?<!\d)\d{1,6}\s+(?:[A-Za-z0-9.'\-]+\s+){1,4}"
        r"(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Ln|Lane|Dr|Drive|Ct|Court"
        r"|Way|Pl|Place|Ter|Terrace|Cir|Circle|Hwy|Highway|Pkwy|Parkway)\b",
        0,
    ),
}
_VALUE_COMPILED = [re.compile(pat, flags) for pat, flags in _VALUE_PII_PATTERNS.values()]

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
            # Case-INSENSITIVE (2x1): an operator name matches in any casing.
            patterns.append(re.compile(token, re.DOTALL | re.IGNORECASE))
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


def scan_text(text, identity_config=DEFAULT_IDENTITY_CONFIG):
    """Count operator-PII matches in a single in-memory string.

    The value-level counterpart to `scan` (which reads file CONTENTS for the
    file-distribution boundary). Applies the operator-IDENTITY tokens + the full
    EXCLUDED_RAW_PII value classes — generic email (any domain), phone (E.164 +
    NANP), and a conservative US street address (bead g5x) — and NOT the structural
    store-line patterns (those detect a leaked store NDJSON FILE, not personal data
    inside a scalar token). Used by the router summary boundary (bead 8j6) to
    fail-closed on raw PII in a pass-through field value.

    The text is NFKC-folded first, so compatibility homographs (e.g. a fullwidth
    `＠`) normalise to their canonical form before matching. Cross-script confusables
    (e.g. a Cyrillic lookalike) are out of scope for this single-operator value
    boundary. The widened classes are deliberately NOT applied by `scan` — see the
    `_VALUE_PII_PATTERNS` note for why the trunk scanner stays gmail-conservative.

    Args:
        text (str): The value to scan.
        identity_config (str | Path, optional): The gitignored operator-identity
            token file; absent -> identity detection is empty (the value patterns
            still run).

    Returns:
        (int) Total operator-PII (value-class + identity) matches in `text`.
    """
    normalized = unicodedata.normalize("NFKC", text)
    patterns = _VALUE_COMPILED + _load_identity_patterns(identity_config)
    return sum(len(pattern.findall(normalized)) for pattern in patterns)


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
