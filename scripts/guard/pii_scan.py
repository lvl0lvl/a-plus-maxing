"""Tracked-file operator-PII scanner (ADR-0001-T0 selected token set).

`scan(tracked_files) -> int` reads each supplied file's CONTENTS and returns the
total count of operator-PII matches. When the count is >=1, each offending file
is named via the single pinned channel — a `PII-HIT: <path>` line on stderr —
which the ADR-0005-T1 pre-commit hook reads. The `tracked_files` list is the
caller's current staged/tracked set captured at invocation; `scan` does not
re-enumerate (the hook passes its own `--staged` set, closing the
add-after-enumeration TOCTOU window).

Operator-identity tokens (the operator's name) and operator-contact tokens (the
operator's real email/handles) load at run time from GITIGNORED configs
(`vault/meta/operator-identity.txt` / `operator-contact.txt`), so this tracked
scanner carries NO operator PII and the trunk is shareable. A fresh clone has no
such files, so token detection is simply empty there while the operator-AGNOSTIC
patterns still run. The operator-agnostic set is the two structural
`{item, timepoint, source, value}` store-line patterns; neither carries personal
data. Contact moved OUT of the agnostic set at 3lv: a generic `@gmail.com`
pattern run trunk-wide flags the scanner's own synthetic test fixtures and bead
example emails (14 false hits on a routine staged set), so the operator's REAL
contact is detected config-driven instead — present on the operator instance,
absent (and therefore silent) on a clone.

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

# Operator-AGNOSTIC patterns (no personal data): the two field-order structural
# store-line patterns. Tracked, exposed so a test can pin the tracked set to the
# spike's structural patterns. Contact is NOT here (3lv): the operator's contact
# is a config-driven token (DEFAULT_CONTACT_CONFIG below), loaded by whichever
# caller wants contact coverage — the commit hook's trunk-wide scope passes it.
AGNOSTIC_PATTERNS = {
    "health-data-item-then-tp": (
        r'("item"|"value")[\s\S]{0,400}?"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'
    ),
    "health-data-tp-then-item": (
        r'"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}[\s\S]{0,400}?("item"|"value")'
    ),
}

# Structural store-line patterns match across newlines (a pretty-printed reading
# spans lines) and stay DOTALL-only (store keys are canonical lowercase JSON).
_COMPILED_AGNOSTIC = [re.compile(p, re.DOTALL) for p in AGNOSTIC_PATTERNS.values()]

# Value-boundary PII patterns (bead g5x): the EXCLUDED_RAW_PII contact classes the
# router names that are tractable for a free-text value scan — generic dotted-domain
# email (ANY provider, so @gmail.com / @googlemail.com / a non-gmail provider all
# hit) and phone (E.164 + NANP). Applied by `scan_text` (the runtime VALUE boundary
# feeding `router.summarize`) ONLY — NOT by `scan`. The trunk-wide commit scanner
# stays gmail-conservative on purpose: a generic-email / phone pattern run across the
# whole tracked tree floods on docs + test fixtures, breaking clonability (the
# operator-specific commit-hook redesign is bead 3lv). Each entry point therefore
# carries its own pattern set; the identity loader is shared.
#
# Shape note: this dict is name -> (pattern, flags) so each entry's flags travel with
# it (email is IGNORECASE; phone is not). AGNOSTIC_PATTERNS above is name -> string
# with flags applied at its compile site — a deliberate shape difference. The `email`
# value pattern is generic any-domain ON PURPOSE: at the VALUE boundary any email in
# a free-text field is a leak risk, so the value scan needs no contact config (3lv).
#
# Phone patterns anchor on `(?<!\d)`/`(?!\d)` and a digit-count floor so ISO
# timestamps (`08:00:00+00:00`) and bare numeric runs do not register; the separated
# form requires separators so a contiguous numeric ID does not match.
#
# POSTAL address (bead nue) is detected at this boundary by a PRECISE detector
# anchored on the strong co-signal PR#78 BUG-1/HIST-1 demanded: a US ZIP 5(-4)
# preceded by a street-number lead-in plus EITHER a street-suffix token OR a
# 2-letter state token, with the ZIP value-final or punctuation-followed (the
# (?!\s*\w) tail guard keeps metric continuations like "10000 steps" out).
# Span semantics: the suffix->ZIP span and the state pattern's middle span are
# line-confined ([^\n]), but every \s+ separator crosses newlines — which only
# widens the catch (fail-closed direction). Case-INSENSITIVE (case is the wrong
# discriminator — "123 MAIN ST" and "123 main st" are the same address), yet
# "Dr Patel followup" / "5 Star Gym Way" / "1 Rep Max St progression" cannot
# match: no ZIP. A bare 5-digit number cannot match either: no street lead-in +
# co-signal. Honest residuals, deliberate on a fail-closed PII boundary:
# (i) a value ENDING in a bare 5-digit metric after a word-state token ("did 3
# sets, felt ok, 10000") still false-positives — fail-closed, the operator
# rephrases; (ii) the tail guard makes a ZIP followed by a bare word ("62704
# usa") an accepted recall miss; (iii) the canonical TWO-LINE mailing address
# ("123 Main St\nSpringfield, IL 62704") is NOT detected — the street-line/
# city-line newline split is out of scope (extension tracked in a bead).
# Spelled-out state names ("illinois") and ZIP-less street lines are NOT
# matched (the ZIP is the co-signal that keeps the detector off legitimate
# training text). Structured `postal-address` store data is already stripped
# via the router's _RAW_TO_FIELD derivation, so this covers the free-text-typed
# residual. Out of scope here: cross-script (Cyrillic) homographs, TLD-less
# local addresses (name@localhost), and bare contiguous phone digits (which
# flood on numeric IDs) — single-operator accidental-leakage threat model.
_ZIP = r"\d{5}(?:-\d{4})?"
_STREET_SUFFIX = (
    r"st|street|ave|avenue|rd|road|blvd|boulevard|dr|drive|ln|lane|way|ct|court|"
    r"pl|place|ter|terrace|cir|circle|hwy|highway|pkwy|parkway"
)
_US_STATE = (
    r"al|ak|az|ar|ca|co|ct|de|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|mn|ms|mo|"
    r"mt|ne|nv|nh|nj|nm|ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|va|wa|wv|wi|wy|dc"
)
_VALUE_PII_PATTERNS = {
    "email": (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.IGNORECASE),
    "phone-e164": (r"(?<!\d)\+\d{8,15}(?!\d)", 0),
    "phone-separated": (
        r"(?<!\d)(?:\+?\d{1,3}[\s.\-])?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)",
        0,
    ),
    # street-number (optional comma) + 1-5 words + street-suffix token ... ZIP;
    # the suffix->ZIP span is line-confined, the ZIP tail-guarded.
    "postal-street-zip": (
        rf"(?<!\d)\d{{1,5}}\s*,?\s+(?:[\w'’.#-]+\s+){{1,5}}(?:{_STREET_SUFFIX})\b\.?"
        rf"[^\n]{{0,48}}?(?<!\d){_ZIP}(?!\s*\w)",
        re.IGNORECASE,
    ),
    # street-number lead-in ... 2-letter state token, then the tail-guarded ZIP
    # (catches suffix-less street names: "100 acacia, springfield il 62704").
    "postal-state-zip": (
        rf"(?<!\d)\d{{1,5}}\s*,?\s+[^\n]{{2,60}}?\b(?:{_US_STATE})\s*,?\s+"
        # The (?<!\d) before the ZIP is inert here (the mandatory \s+ precedes
        # it) — kept as parallelism with postal-street-zip, where it IS
        # load-bearing, and as insurance against a future separator edit.
        rf"(?<!\d){_ZIP}(?!\s*\w)",
        re.IGNORECASE,
    ),
}
_VALUE_COMPILED = [re.compile(pat, flags) for pat, flags in _VALUE_PII_PATTERNS.values()]

# scan_text caps its input before matching: the unanchored email local-part makes
# `findall` O(n^2) on a long string (a measured multi-second hang on a pasted blob),
# and router.summarize feeds operator-pasted field values in with no upstream cap. A
# pass-through field value is a short de-identified stated token, so a generous cap
# bounds the worst case without affecting any legitimate value (PR#78 SEC-1 — a
# motivated availability control on the PII boundary).
_MAX_SCAN_TEXT_LEN = 4096

# Operator-identity tokens load from this GITIGNORED file (one regex per line);
# absent on a fresh clone -> empty identity set. Keeps operator PII out of tracked
# source.
DEFAULT_IDENTITY_CONFIG = Path("vault/meta/operator-identity.txt")

# Operator-contact tokens (real email/handles) load from this GITIGNORED file,
# same one-regex-per-line shape and the same loader (3lv). Separate from the
# identity config because the two carry different SCOPES at the commit hook: the
# contact is denied TRUNK-WIDE (it has no legitimate tracked use — provenance
# prose uses the operator's name, never the email), while the name is denied only
# on data-bearing paths (it IS accepted provenance in governance/session prose).
DEFAULT_CONTACT_CONFIG = Path("vault/meta/operator-contact.txt")


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


def scan(tracked_files, identity_config=DEFAULT_IDENTITY_CONFIG, include_structural=True):
    """Count operator-PII matches across the contents of the supplied files.

    Args:
        tracked_files (iterable[str]): Paths to scan (the caller's current
            staged/tracked set; not re-enumerated here).
        identity_config (str | Path, optional): Path to a gitignored token file
            (identity or contact); absent -> token detection is empty.
        include_structural (bool, optional): Apply the agnostic structural
            store-line patterns. Callers scanning known-fixture paths (test
            suites whose fixtures embed synthetic reading-shaped literals by
            construction) pass False so only the config-driven tokens run there
            (bead dv3 — the structural net over fixtures is pure false positive).

    Returns:
        (int) Total number of operator-PII matches across the files' contents.
        Each file with >=1 match is named on stderr as `PII-HIT: <path>`.
    """
    structural = _COMPILED_AGNOSTIC if include_structural else []
    patterns = structural + _load_identity_patterns(identity_config)
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
    file-distribution boundary). Applies the operator-IDENTITY tokens + the tractable
    EXCLUDED_RAW_PII value classes — generic dotted-domain email (any provider),
    phone (E.164 + NANP) (bead g5x), and US postal address via the precise
    ZIP/state-anchored detector (bead nue) — and NOT the structural store-line
    patterns (those detect a leaked store NDJSON FILE, not personal data inside a
    scalar token). Used by the router summary boundary (bead 8j6) to fail-closed on
    raw PII in a pass-through field value.

    The text is NFKC-folded first, so compatibility homographs (e.g. a fullwidth
    `＠`) normalise to their canonical form before matching, then capped at
    `_MAX_SCAN_TEXT_LEN` to bound match cost. Out of scope for this single-operator
    value boundary (see the `_VALUE_PII_PATTERNS` note): ZIP-less postal fragments,
    two-line/multi-line addresses (the street line + city line split across
    newlines), cross-script (Cyrillic) confusables, TLD-less local addresses
    (`name@localhost`), and bare contiguous phone digits. The value classes are
    deliberately NOT applied by `scan` — the trunk scanner stays gmail-conservative.

    Args:
        text (str): The value to scan.
        identity_config (str | Path, optional): The gitignored operator-identity
            token file; absent -> identity detection is empty (the value patterns
            still run).

    Returns:
        (int) Total operator-PII (value-class + identity) matches in `text`.
    """
    normalized = unicodedata.normalize("NFKC", text)[:_MAX_SCAN_TEXT_LEN]
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
