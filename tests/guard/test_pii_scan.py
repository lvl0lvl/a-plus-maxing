"""Tests for scripts/guard/pii_scan.py — tracked-file operator-PII scanner.

`scan(tracked_files, token_config=...) -> int` reads each file's CONTENTS and
counts operator-PII matches (`identity_config` is the deprecated alias — b9l).
The operator-AGNOSTIC patterns (two structural
store-line patterns) are tracked; the operator-IDENTITY and operator-CONTACT
tokens load at run time from gitignored configs (`vault/meta/operator-identity.txt`
/ `operator-contact.txt`) — contact moved from a generic tracked `@gmail.com`
pattern to the config model at 3lv (the generic pattern flooded on fixture/bead
emails, breaking clonability).
AC-2/AC-3 run the SAME scanner over the SAME controlled scratch git clone: clean
set -> 0, then a planted token per class -> >=1, with the offending path reported
via the single PII-HIT: <path> stderr channel. Identity detection is proven
config-driven (a synthetic token detected only when the config supplies it) so no
operator name lives in tracked source. AC-4 checks git check-ignore vault/store/
in both directions. A no-op scanner (always 0) must fail the plant tests.
"""

import json
import subprocess
from pathlib import Path

import pytest

from scripts.guard import pii_scan
from scripts.guard.pii_scan import scan

# A SYNTHETIC identity token (not the real operator) supplied via a tmp config,
# so the fixtures carry no operator name. Detection of this token must depend on
# the config being present (config-driven, not hardcoded).
SYNTHETIC_IDENTITY = "Testperson|Examplename"

# A SYNTHETIC contact token (3lv): contact detection is config-driven like identity
# — the trunk scan carries NO generic email pattern (it flooded on fixture/bead
# emails, breaking clonability). Tests supply this token via a tmp config line.
SYNTHETIC_CONTACT = r"test\.fixture@gmail\.com"

# One planted token per declared operator-PII class. The contact plant uses a
# synthetic gmail address; the structural health-data token is a synthetic
# {item,timepoint,source,value} store line (biomarker-independent, not real PII);
# the identity plant uses the synthetic token above.
PLANTS = {
    "identity": "patient name: Examplename\n",
    "contact": "reply-to: test.fixture@gmail.com\n",
    "health-data": (
        '{"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", '
        '"source": "manual", "value": 55}\n'
    ),
}

# A path that does not exist -> identity detection is empty (agnostic patterns
# still run). Used to prove identity detection is config-driven.
NO_CONFIG = "/nonexistent/operator-identity.txt"


def _git(args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )


def _scratch_clone(tmp_path, gitignore_store=True):
    """Build a controlled git repo with a known-clean tracked fileset.

    Args:
        tmp_path (Path): pytest tmp dir.
        gitignore_store (bool, optional): plant the `vault/store/` .gitignore
            entry (AC-4 positive) when True; omit it (AC-4 negative) when False.

    Returns:
        (Path) The scratch clone root.
    """
    root = tmp_path / "scratch"
    root.mkdir()
    _git(["init", "-q"], root)
    (root / "README.md").write_text("# project\nclean content, no operator PII\n")
    (root / "code.py").write_text("def f():\n    return 1\n")
    if gitignore_store:
        (root / ".gitignore").write_text("vault/store/\n")
    _git(["add", "-A"], root)
    return root


def _tracked(root):
    out = _git(["ls-files"], root).stdout.split("\n")
    return [str(root / p) for p in out if p.strip()]


def _identity_config(tmp_path, token=SYNTHETIC_IDENTITY):
    """Write a tmp token config (synthetic identity + contact lines); return its path.

    One regex per line, matching the production config shape. The contact line is
    included because contact detection is config-driven (3lv) — tests asserting
    all-class detection supply both token classes through this one config.
    """
    cfg = tmp_path / "operator-identity.txt"
    cfg.write_text(f"# synthetic test token\n{token}\n{SYNTHETIC_CONTACT}\n")
    return str(cfg)


def test_scan_clean_then_planted_same_clone(tmp_path):
    """AC-2 + AC-3 same scanner / same clone: 0 on clean, >=1 once planted.

    Proves the 0-on-clean result against a scanner demonstrably capable of >=1
    (QA F1+F2), against the controlled scratch fileset (not the live ls-files set).
    Identity is supplied via a tmp synthetic config.
    """
    root = _scratch_clone(tmp_path)
    cfg = _identity_config(tmp_path)
    # AC-2: clean tracked set -> 0.
    assert scan(_tracked(root), token_config=cfg) == 0

    # AC-3: plant every class into a tracked file's CONTENTS in the SAME clone.
    leak = root / "README.md"
    body = leak.read_text()
    for token in PLANTS.values():
        body += token
    leak.write_text(body)
    _git(["add", "-A"], root)

    assert scan(_tracked(root), token_config=cfg) >= 1


def test_agnostic_detection_without_config(tmp_path):
    """Agnostic (structural) patterns detect with NO config (a fresh clone).

    A planted structural store-line is caught even when the gitignored token
    configs are absent. Contact is NOT agnostic since 3lv — its config-driven
    behavior is pinned in test_contact_detection_is_config_driven.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "README.md"
    body = leak.read_text() + PLANTS["health-data"]
    leak.write_text(body)
    _git(["add", "-A"], root)

    assert scan(_tracked(root), token_config=NO_CONFIG) >= 1


def test_identity_detection_is_config_driven(tmp_path):
    """The synthetic identity token is detected only when the config supplies it.

    Plant the synthetic token's text into a tracked file. With the tmp config it
    is detected (>=1); without any config (non-existent path) that same token is
    NOT detected — proving identity detection is config-driven, not hardcoded.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "code.py"
    leak.write_text(leak.read_text() + PLANTS["identity"])
    _git(["add", "-A"], root)
    files = _tracked(root)

    cfg = _identity_config(tmp_path)
    assert scan(files, token_config=cfg) >= 1
    # Same token, no config -> agnostic patterns find nothing here -> 0.
    assert scan(files, token_config=NO_CONFIG) == 0


def test_tracked_source_carries_no_operator_identity(tmp_path):
    """Shareability guard: the tracked scanner source holds no operator name.

    Regression guard that keeps the trunk shareable — the operator-identity
    literal must live only in the gitignored config, never in tracked source.
    """
    src = open(pii_scan.__file__, encoding="utf-8").read()
    config = Path(pii_scan.__file__).resolve().parents[2] / "vault" / "meta" / "operator-identity.txt"
    if not config.exists():
        pytest.skip("no operator-identity config on this instance")
    tokens = [
        piece
        for line in config.read_text().splitlines()
        if line.strip() and not line.startswith("#")
        for piece in line.strip().split("|")
    ]
    assert tokens, "operator-identity config is empty"
    for token in tokens:
        assert token not in src


@pytest.mark.parametrize("pii_class", sorted(PLANTS))
def test_scan_hits_each_pii_class(tmp_path, pii_class):
    """AC-3 class completeness (Security HIGH-2): >=1 for a token per class.

    Each declared class (identity, contact, health-data) planted alone into a
    tracked file's CONTENTS must produce >=1 — a single-token scanner fails this.
    Identity AND contact tokens are supplied via the synthetic tmp config (contact
    is config-driven since 3lv); health-data detects agnostically.
    """
    root = _scratch_clone(tmp_path)
    cfg = _identity_config(tmp_path)
    leak = root / "code.py"
    leak.write_text(leak.read_text() + PLANTS[pii_class])
    _git(["add", "-A"], root)

    assert scan(_tracked(root), token_config=cfg) >= 1


def test_agnostic_set_pins_structural_and_tokens_are_config_sourced(tmp_path):
    """Tracked AGNOSTIC set is the two structural patterns ONLY; tokens are config-sourced.

    The scanner exposes its agnostic patterns as a module-level structure; this
    asserts the exact spike regexes for the two structural store-line patterns,
    and that neither the operator-identity nor the operator-contact tokens are in
    that tracked set (each is sourced from its own gitignored config — bead 3lv:
    the generic `@gmail.com` contact pattern was REMOVED from the trunk-wide set
    because it floods on synthetic fixture/bead emails, breaking clonability).
    """
    declared_agnostic = {
        "health-data-item-then-tp": (
            r'("item"|"value")[\s\S]{0,400}?"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'
        ),
        "health-data-tp-then-item": (
            r'"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}[\s\S]{0,400}?("item"|"value")'
        ),
    }
    assert set(pii_scan.AGNOSTIC_PATTERNS) == set(declared_agnostic)
    assert pii_scan.AGNOSTIC_PATTERNS == declared_agnostic
    # Identity AND contact are config-sourced, not part of the tracked pattern set.
    assert "identity" not in pii_scan.AGNOSTIC_PATTERNS
    assert "contact" not in pii_scan.AGNOSTIC_PATTERNS
    assert pii_scan.DEFAULT_IDENTITY_CONFIG.name == "operator-identity.txt"
    assert pii_scan.DEFAULT_CONTACT_CONFIG.name == "operator-contact.txt"


def test_contact_detection_is_config_driven(tmp_path):
    """3lv: the operator contact is detected only when a config supplies it.

    Plant a synthetic gmail address in a tracked file. With a contact config
    carrying that token it is detected (>=1); with no config that same address is
    NOT detected (==0) — proving contact detection is operator-specific and
    config-driven, mirroring the identity model. The ==0 leg is the clonability
    fix: a fresh clone (no config) no longer floods on fixture/bead emails.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "code.py"
    leak.write_text(leak.read_text() + PLANTS["contact"])
    _git(["add", "-A"], root)
    files = _tracked(root)

    cfg = tmp_path / "operator-contact.txt"
    cfg.write_text("# synthetic test contact\n" + SYNTHETIC_CONTACT + "\n")
    assert scan(files, token_config=str(cfg)) >= 1
    # Same address, no config -> NOT detected (the generic-gmail flood is gone).
    assert scan(files, token_config=NO_CONFIG) == 0


def test_scan_detects_multiline_pretty_printed_reading(tmp_path):
    """SEC-02: a pretty-printed (multi-line) leaked store reading is detected.

    The re.DOTALL fix must catch a `json.dumps(reading, indent=2)` reading whose
    fields span newlines — a single-line scanner would miss it. Agnostic patterns
    catch this with no identity config.
    """
    root = _scratch_clone(tmp_path)
    reading = {
        "item": "rhr",
        "timepoint": "2026-06-01T08:00:00+00:00",
        "source": "manual",
        "value": 55,
    }
    leak = root / "README.md"
    leak.write_text(leak.read_text() + "\n" + json.dumps(reading, indent=2) + "\n")
    _git(["add", "-A"], root)

    assert scan(_tracked(root), token_config=NO_CONFIG) >= 1


def test_scan_names_offending_file_on_stderr(tmp_path, capfd):
    """AC-3 offending-file channel (Security MED): PII-HIT: <path> on stderr.

    The single pinned channel the ADR-0005-T1 hook reads — not the return value,
    not a second channel. Uses the structural (agnostic) plant since contact is
    config-driven (3lv).
    """
    root = _scratch_clone(tmp_path)
    leak = root / "README.md"
    leak.write_text(leak.read_text() + PLANTS["health-data"])
    _git(["add", "-A"], root)
    offending = str(leak)

    assert scan(_tracked(root), token_config=NO_CONFIG) >= 1
    captured = capfd.readouterr()
    assert f"PII-HIT: {offending}" in captured.err


def test_scan_structural_switch(tmp_path):
    """dv3: include_structural=False drops ONLY the structural patterns.

    The commit/pre-push hooks scan known-fixture paths (tests/) with the switch
    off — fixtures embed synthetic reading-shaped literals by construction. The
    config-driven tokens MUST still run with the switch off (a real operator
    token in a fixture file is a leak); reds if the switch silently disables the
    token scan too, or if the default stops applying the structural patterns.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "code.py"
    leak.write_text(leak.read_text() + PLANTS["health-data"] + PLANTS["contact"])
    _git(["add", "-A"], root)
    files = _tracked(root)
    cfg = tmp_path / "operator-contact.txt"
    cfg.write_text(SYNTHETIC_CONTACT + "\n")

    # Default: structural plant detected even with no token config.
    assert scan(files, token_config=NO_CONFIG) >= 1
    # Switch off, no config: the structural plant alone scores 0.
    assert scan(files, token_config=NO_CONFIG, include_structural=False) == 0
    # Switch off, config present: the contact token STILL detects.
    assert scan(files, token_config=str(cfg), include_structural=False) >= 1


def test_check_ignore_positive_when_entry_present(tmp_path):
    """AC-4 positive: git check-ignore vault/store/ exits 0 when entry present."""
    root = _scratch_clone(tmp_path, gitignore_store=True)
    assert pii_scan.store_is_gitignored(root) is True


def test_check_ignore_negative_when_entry_absent(tmp_path):
    """AC-4 negative (QA F3): no entry -> reports non-ignored / FAIL (falsifiable)."""
    root = _scratch_clone(tmp_path, gitignore_store=False)
    assert pii_scan.store_is_gitignored(root) is False


def test_scan_empty_list_returns_zero_int():
    """SEC-01(a) (QA F5): scan([]) == 0 and the return is an int."""
    result = scan([])
    assert result == 0
    assert isinstance(result, int)


def test_scan_returns_int_on_nonempty(tmp_path):
    """SEC-01(a): the -> int return-type shape holds on a real set too."""
    root = _scratch_clone(tmp_path)
    assert isinstance(scan(_tracked(root), token_config=NO_CONFIG), int)


def test_scan_contact_is_case_insensitive(tmp_path):
    """2x1: a non-canonical-case contact (Test.Fixture@Gmail.COM) is detected (>=1).

    An upper/mixed-case email is the same contact and must score a hit, not pass.
    Contact is config-driven since 3lv, so the token comes from the synthetic
    config; the config loader compiles every token IGNORECASE, which this pins
    (reds if the loader drops the flag).
    """
    root = _scratch_clone(tmp_path)
    cfg = tmp_path / "operator-contact.txt"
    cfg.write_text(SYNTHETIC_CONTACT + "\n")
    leak = root / "README.md"
    leak.write_text(leak.read_text() + "reply-to: Test.Fixture@Gmail.COM\n")
    _git(["add", "-A"], root)
    assert scan(_tracked(root), token_config=str(cfg)) >= 1


def test_identity_match_is_case_insensitive(tmp_path):
    """2x1: an operator-identity token matches case-insensitively (config-driven)."""
    root = _scratch_clone(tmp_path)
    cfg = _identity_config(tmp_path, token="Examplename")
    leak = root / "code.py"
    leak.write_text(leak.read_text() + "contact EXAMPLENAME today\n")
    _git(["add", "-A"], root)
    assert scan(_tracked(root), token_config=cfg) >= 1


def test_scan_text_counts_contact_and_identity(tmp_path):
    """scan_text (8j6 helper): counts contact + identity tokens in an in-memory string.

    The value-level counterpart to `scan` (which reads file CONTENTS). Contact is
    agnostic; identity is config-driven (the same token is undetected with no config).
    """
    from scripts.guard.pii_scan import scan_text

    cfg = _identity_config(tmp_path)  # synthetic 'Testperson|Examplename'
    # Pin the agnostic assertions to NO_CONFIG so they do not bind to the real
    # gitignored operator-identity file (present on dev, absent on a fresh clone):
    # contact detection is config-independent (TEST-1).
    assert scan_text("hello world, no pii here", token_config=NO_CONFIG) == 0
    assert scan_text("mail me at Test.Fixture@Gmail.COM", token_config=NO_CONFIG) >= 1  # case-insensitive too
    assert scan_text("ask Examplename first", token_config=cfg) >= 1
    assert scan_text("ask Examplename first", token_config=NO_CONFIG) == 0


def test_scan_text_scopes_out_structural_store_pattern():
    """scan_text targets personal-identity tokens (name/contact), NOT the file-
    structural store-line patterns (those detect a leaked store NDJSON FILE, not raw
    PII inside a scalar summary token). A bare store line carries no personal data.

    Also pins the dob-iso / dob-numeric-year-first T-ONLY timestamp exclusion
    (bh-316-1 / SEC-DEID-02): a T-separated store timepoint is scoped out of the DOB
    class, but a SPACE- or NEWLINE-separated date+time is a human DOB signal and DOES
    catch. The full-ISO-DATETIME DOB ("1986-03-14T00:00:00") is byte-identical to a
    store timepoint and is the same accepted scope-out (compensated upstream by
    age-banding); a regression that widened the exclusion back to [T\\s] would red the
    space/newline asserts below."""
    from scripts.guard.pii_scan import scan_text

    store_line = (
        '{"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", '
        '"source": "manual", "value": 55}'
    )
    # include_dob=True exercises the opt-in DOB class so the T-exclusion is tested WITH
    # the date class active (default off would make these trivially 0 — a tautology).
    assert scan_text(store_line, token_config=NO_CONFIG, include_dob=True) == 0
    # T-separated date+time (store shape / date-picker) is scoped out; …
    assert scan_text("1986-03-14T00:00:00", token_config=NO_CONFIG, include_dob=True) == 0
    # … but a SPACE- or NEWLINE-separated date+time is a DOB signal and catches.
    assert scan_text("1986-03-14 08:00", token_config=NO_CONFIG, include_dob=True) >= 1
    assert scan_text("dob 1986-03-14\nsession at 08:00", token_config=NO_CONFIG, include_dob=True) >= 1


# --- g5x: widen scan_text to the full EXCLUDED_RAW_PII value classes ------------
# scan_text is the runtime VALUE boundary feeding router.summarize. Before g5x it
# matched only the @gmail.com contact + identity tokens, so a non-gmail email /
# phone / postal address typed into a free-text pass-through field scored 0 and
# leaked to both sinks. These reds the gmail-only scan_text; greens once the value
# boundary covers the full contact classes. NO_CONFIG so they bind to the agnostic
# value patterns, not the gitignored operator-identity file.

@pytest.mark.parametrize("value, label", [
    ("reach me at op.user@protonmail.com", "non-gmail email"),
    ("mail op.user@googlemail.com", "googlemail"),
    ("OP.USER@PROTONMAIL.COM", "email case-insensitive"),
    ("call +1 415 555 0199", "phone E.164 spaced"),
    ("call +14155550199 now", "phone E.164 contiguous"),
    ("ring (415) 555-0199", "phone NANP parens"),
    ("ring 415-555-0199", "phone NANP dashes"),
    ("ring 415.555.0199", "phone NANP dots"),
])
def test_scan_text_detects_value_pii_classes(value, label):
    """g5x AC1: scan_text catches each tractable EXCLUDED_RAW_PII contact class.

    Each class (generic/non-gmail email, googlemail, phone E.164/NANP) typed into a
    free-text value scores >=1 — reds on the gmail-only scan_text. Postal has its own
    precise ZIP/state-anchored detector (bead nue; tests below).
    """
    assert pii_scan.scan_text(value, token_config=NO_CONFIG) >= 1, label


@pytest.mark.parametrize("value, label", [
    ("ship to 123 main st, springfield il 62704", "lowercase street+state+ZIP (the nue canonical)"),
    ("123 Main St, Springfield IL 62704", "Title-case street+state+ZIP"),
    ("MAIL TO 123 MAIN ST SPRINGFIELD IL 62704", "uppercase, no commas"),
    ("456 oak avenue, columbus oh 43004-1234", "full suffix word + ZIP+4"),
    ("789 elm rd 62704", "street-suffix + ZIP, no state token"),
    ("100 acacia, springfield il 62704", "state+ZIP, no recognizable street suffix"),
    ("100 maple, fort wayne in 46802", "word-state token 'in' (Indiana) — TEST-2"),
    ("po box 123, springfield il 62704", "PO Box, comma after box number — TEST-3"),
    ("po box 123 springfield il 62704", "PO Box, no comma — TEST-3"),
    ("ship to 123 main st, springfield il\n62704", "\\s+ separator bridges the newline — TEST-1"),
])
def test_scan_text_detects_postal_address(value, label):
    """nue AC1: a full street address in a free-text value scores >=1, ANY case.

    The detector is anchored on the strong co-signal the bead specifies — a US ZIP
    5(-4) preceded by street-number+words plus a street-suffix token OR a 2-letter
    state token — so it is case-INSENSITIVE (case is the wrong discriminator,
    PR#78 BUG-1/HIST-1) without flooding on Title-case training text. Reds on the
    postal-less scan_text. The TEST-2/TEST-3/TEST-1 rows pin the word-state token,
    both PO Box comma forms (the \\s*,?\\s+ lead-in), and the newline-crossing \\s+
    separator (fail-closed widening).
    """
    assert pii_scan.scan_text(value, token_config=NO_CONFIG) >= 1, label


@pytest.mark.parametrize("value, label", [
    ("ship to 27 portland st, dartmouth ns b2y 1a1", "lowercase Canadian postal (spaced)"),
    ("27 Portland St, Dartmouth NS B2Y 1A1", "Title-case Canadian postal (spaced)"),
    ("MAIL TO 27 PORTLAND ST DARTMOUTH NS B2Y1A1", "uppercase, no inner space"),
    ("near halifax ns b3h 4r2", "bare Canadian postal in free text"),
    ("the code is k1a0b1 for ottawa", "Canadian postal, no space, mid-text"),
])
def test_scan_text_detects_canadian_postal(value, label):
    """nue-CA: a Canadian postal code (A1A 1A1 / A1A1A1) in a free-text value scores >=1.

    The operator is in Nova Scotia, Canada — directly in-population. The US-ZIP-anchored
    postal detectors miss `B2Y 1A1`, so a Canadian street address typed into a goals field
    scored 0 and leaked. The additive `[A-Za-z]\\d[A-Za-z]\\s?\\d[A-Za-z]\\d` pattern is the
    high-confidence token; case-insensitive, optional inner space. Reds on the
    US-ZIP-only `_VALUE_PII_PATTERNS`.
    """
    assert pii_scan.scan_text(value, token_config=NO_CONFIG) >= 1, label


@pytest.mark.parametrize("value", [
    "did 3x5 at b2y rpe 8",                 # 'b2y' fragment, not the full 6-char postal
    "set 1a1 to failure",                   # '1a1' fragment alone — no letter-digit-letter lead
    "ns province check-in",                 # bare province abbrev — deliberately not added
    "macro split 40 30 30 today",           # numeric run, no letter-digit-letter-digit-letter-digit
    "zone 2 for a1 b2 c3 intervals",        # spaced letter-digit pairs, not a contiguous postal
])
def test_scan_text_canadian_postal_negative_controls(value):
    """nue-CA: health free-text near-misses do NOT trip the Canadian postal pattern (== 0).

    Pins the false-positive boundary: a 3-char postal fragment, a bare province token, and
    rep/macro/interval numerics with stray letters must not register. The leading liveness
    assert proves the value patterns are ACTIVE so a regression that disabled them reds here
    too.
    """
    assert pii_scan.scan_text("b2y 1a1 from dartmouth", token_config=NO_CONFIG) >= 1  # pattern live
    assert pii_scan.scan_text(value, token_config=NO_CONFIG) == 0


def test_scan_text_full_detects_canadian_postal():
    """nue-CA: scan_text_full (the capture-path scanner) also catches a Canadian postal.

    `capture._value_has_pii` calls `scan_text_full`; this pins that the additive pattern is
    in `_VALUE_COMPILED` (shared by both entry points), so a Canadian postal anywhere in a
    full-length value is caught on the capture path.
    """
    assert pii_scan.scan_text_full(
        "train at the new place, mail me at 27 Portland St, Dartmouth NS B2Y 1A1",
        token_config=NO_CONFIG,
    ) >= 1


def test_scan_text_detects_compatibility_homograph_email():
    """g5x AC1: an NFKC compatibility-homograph email (fullwidth @) is caught.

    A fullwidth commercial-at (U+FF20) folds to '@' under NFKC, so 'op<FF20>gmail.com'
    is the same contact and must score >=1 — reds without the NFKC fold. (Cross-script
    confusables, e.g. Cyrillic, are out of scope for the single-operator value boundary.)
    """
    homograph = "reach me op＠gmail.com"
    assert pii_scan.scan_text(homograph, token_config=NO_CONFIG) >= 1


@pytest.mark.parametrize("value, label", [
    ("reach peak by birthday 1986-03-14", "ISO DOB in a goals field (the yduw T9 vector)"),
    ("dob 03/14/1986", "US slash MM/DD/YYYY"),
    ("born 14.03.1986", "dotted DD.MM.YYYY"),
    ("1986/03/14 birthdate", "ISO-order slash year-first"),
    ("born March 14, 1986", "month-name Month DD, YYYY"),
    ("b-day 14 Mar 2001", "day + abbreviated month + year"),
    ("dob jan 1st 1990", "month + ordinal day + year"),
    # SEC-DEID-01: 2-digit-year DOB, CO-SIGNAL-anchored on a DOB cue word.
    ("born 3/14/86", "2-digit-year DOB with 'born' cue"),
    ("reach peak by birthday 3/14/86", "2-digit-year DOB in a goals field, 'birthday' cue"),
    ("dob 03/14/86", "2-digit-year DOB, 'dob' cue"),
    ("b-day 14.03.86", "2-digit-year DOB, 'b-day' cue, dotted"),
    # bh-316-3: non-padded dash year-first (dob-iso needs leading zeros; year-first now has dash).
    ("1986-3-14 birthdate", "dash year-first, non-padded"),
    ("born 1986-1-5", "dash year-first, single-digit month AND day"),
    # bh-316-1 / SEC-DEID-02: a DOB carrying a same-line or next-line clock time still catches
    # (the T-only store exclusion no longer swallows a space/newline-separated date+time).
    ("1986-03-14 08:00 recorded", "DOB + same-line HH:MM"),
    ("dob 1986-03-14\n08:00 session", "DOB on a line above an HH:MM line"),
    # SEC-DEID-04: en-dash / em-dash separators fold to ASCII before matching.
    ("born 1986–03–14", "ISO DOB with en-dash separators"),
    ("dob 1986—03—14", "ISO DOB with em-dash separators"),
])
def test_scan_text_detects_dob_date(value, label):
    """yduw: a FULL calendar date (day+month+year) in a pass-through value scores >=1.

    Security EXECUTED this leak at the T9 review — a DOB typed into goal-targets crossed
    VERBATIM to the no-train dispatch + the clarifying model request because scan_text
    had no date detector. Reds on the pre-yduw _VALUE_PII_PATTERNS. The extended rows
    pin the T9-review residual closures (SEC-DEID-01 2-digit cued, bh-316-1/-3 time-suffix
    + dash year-first, SEC-DEID-04 unicode dash). include_dob=True: the DOB class is
    opt-in (default off) so it never alters the frozen-engine scans; the DOB tests
    exercise it explicitly (free-text production callers opt in — capture / summarize
    8j6 / care_review, per the _VALUE_PII_PATTERNS note).
    """
    assert pii_scan.scan_text(value, token_config=NO_CONFIG, include_dob=True) >= 1, label


@pytest.mark.parametrize("value", [
    "return to pre-Jan-2026 loading",        # month+year partial, no day — deliberately out
    "plan for august 2026",                  # month+year, no day
    "born in 1986",                          # bare year — too low-signal (floods)
    "target 10000 steps or 12500 calories",  # 5-digit metric runs
    "BP 120 over 80",
    "sleep 7-8 hours",
    "wake at 08:00:00",                      # time, no date
    "3 sets x 12 reps at rpe 8",
    # SEC-DEID-01 flood corpus: macro splits / set schemes / rep drops are shape-identical
    # to a 2-digit date but carry NO 4-digit year and NO DOB cue -> dob-cued-2digit stays off.
    "macros 40/30/30",                       # macro split — no year, no cue
    "bench 5/3/1 wave",                      # Wendler 5/3/1 set scheme — no year, no cue
    "squat 12/10/8 drop set",                # rep-drop set — no year, no cue
    "zone 2/3/4 intervals",                  # zone scheme — no year, no cue
    "born to run a 5k",                      # DOB cue word but NO date run — cue alone must not fire
    "march 14 birthday",                     # month-name + cue but NO year — partial
    "dob 03/14",                             # numeric + cue but only 2 components (no year)
])
def test_scan_text_dob_negative_controls(value):
    """yduw / SEC-DEID-01: partial dates, health numerics, and training vocab do NOT
    trip the date class (== 0).

    Pins the fail-closed boundary's precision: a MONTH-YEAR partial, a bare year, a
    time, metric runs, and — the SEC-DEID-01 flood vectors — macro splits ("40/30/30"),
    set schemes ("5/3/1"), rep drops ("12/10/8"), and a bare DOB CUE word without a date
    run must not register; only a FULL date (or a cue NEXT TO a 2-digit date) does. The
    leading liveness assert proves the date class is ACTIVE so a regression that disabled
    it — or that weakened the 4-digit-year / cue anchor and flooded on training vocab —
    reds here too.
    """
    assert pii_scan.scan_text("dob 1986-03-14", token_config=NO_CONFIG, include_dob=True) >= 1  # class live
    assert pii_scan.scan_text(value, token_config=NO_CONFIG, include_dob=True) == 0


@pytest.mark.parametrize("value, label", [
    ("ssn 123-45-6789 on file", "dashed SSN"),
    ("123 Main St\nSpringfield, IL 62704", "canonical two-line mailing address (6hts)"),
    ("mail 456 Oak Avenue\nColumbus, OH 43004-1234", "two-line, full suffix + ZIP+4"),
])
def test_scan_text_detects_ssn_and_two_line_postal(value, label):
    """6hts: a dashed SSN + a canonical TWO-LINE mailing address score >=1.

    The SSN 3-2-4 dashed token is unambiguous PII with no flood cost. The two-line
    address is caught by the [\\s\\S] street->ZIP span (still co-signal-anchored on
    street-number + suffix ... ZIP). Reds on the pre-6hts _VALUE_PII_PATTERNS. NOTE: a
    BARE contiguous digit run (a phone/MRN as one number) stays out by design — a
    flood-avoidance residual pinned in test_scan_text_value_boundary_negative_controls.
    """
    assert pii_scan.scan_text(value, token_config=NO_CONFIG) >= 1, label


def test_include_dob_false_drops_only_the_dob_class():
    """yduw/contracts-1: include_dob=False (the public-page / derived-content opt-out)
    removes ONLY the DOB class — every base contact/identifier class still fires.

    The public-page (research_query, wiki-ingest-lint) and derived-artifact (plan_step
    GATE) scanners pass include_dob=False so a citation/schedule date is not a DOB leak.
    This must NOT weaken the boundary for the other classes. Pins both directions: a
    value carrying email+phone+postal+SSN+DOB keeps all four base classes under False and
    gains the DOB class under True; a pure-DOB value scores 0 under False and >=1 under
    True (so the toggle controls the DOB class and nothing else)."""
    v = ("born 1986-03-14 ssn 123-45-6789 reach op@x.com or "
         "+14155550199 addr 12 Oak Ave Springfield IL 62704")
    on = pii_scan.scan_text(v, token_config=NO_CONFIG, include_dob=True)
    off = pii_scan.scan_text(v, token_config=NO_CONFIG, include_dob=False)
    assert off >= 4, f"base classes (email/phone/postal/ssn) must all fire under False, got {off}"
    assert on > off, "the DOB class must add matches under include_dob=True"
    # The toggle controls ONLY the DOB class: a pure-DOB value is 0 off / >=1 on.
    assert pii_scan.scan_text("born 1986-03-14", token_config=NO_CONFIG, include_dob=False) == 0
    assert pii_scan.scan_text("born 1986-03-14", token_config=NO_CONFIG, include_dob=True) >= 1


@pytest.mark.parametrize("value, label", [
    ("call me at 4155550199", "10-digit contiguous phone"),
    ("phone 14155550199 now", "11-digit with country code"),
    ("mrn 0084721399 on file", "10-digit MRN"),
    ("ssn 123456789", "9-digit no-separator SSN"),
    ("account 123456789012", "12-digit account"),
])
def test_scan_operator_value_catches_bare_digit_run(value, label):
    """6hts (operator-signed-off): a bare CONTIGUOUS >=9-digit run (phone/MRN/no-separator
    SSN/account) that the separator-anchored phone/SSN patterns miss is caught at the
    free-text operator-value boundary. Reds without the digitrun-long class / include_digit_run.
    """
    assert pii_scan.scan_operator_value(value, token_config=NO_CONFIG, full=True) >= 1, label


@pytest.mark.parametrize("value", [
    "target 100000 steps",            # 6-digit metric
    "1234567 lifetime steps",         # 7-digit metric (the ceiling of a realistic metric)
    "walked 5 km in 65000 steps",     # 5-digit
    "40/30/30 macros",                # separated, not contiguous
    "BP 120 over 80",
    "3 sets x 12 reps at rpe 8",
])
def test_digit_run_floor_flood_safe(value):
    """6hts: the >=9-digit floor does NOT trip on legit health metrics (<=7 digits).

    Verified flood-safe threshold. The leading liveness assert proves the digit-run class
    is ACTIVE, so a regression that disabled it OR lowered the floor into metric range reds
    here too."""
    assert pii_scan.scan_operator_value("call 4155550199", token_config=NO_CONFIG, full=True) >= 1  # class live
    assert pii_scan.scan_operator_value(value, token_config=NO_CONFIG, full=True) == 0


def test_scan_public_content_excludes_dob_and_digit_run_keeps_base():
    """contracts-2: scan_public_content applies ONLY the base contact/identifier classes —
    a research/schedule DATE or numeric citation is NOT flagged (the contracts-1 regression
    class), but a real email/phone/postal/SSN leaking into a public page STILL is."""
    # DOB + digit-run must NOT trip on public/derived content
    assert pii_scan.scan_public_content(
        "retest by 2026-09-01, born 3/14/86, ref 4155550199 in the study",
        token_config=NO_CONFIG, full=True) == 0
    # base classes still fire (a real leak onto a public page)
    assert pii_scan.scan_public_content(
        "contact op.user@protonmail.com", token_config=NO_CONFIG, full=True) >= 1


def test_digit_run_is_opt_in_off_for_frozen_default():
    """6hts / EXTEND-NOT-REBUILD: the bare-digit-run class is OPT-IN — the low-level
    scan_text_full default (what the byte-frozen plan_step/deid_in callers use) does NOT
    apply it, so a long number in a derived plan does not fail-close the frozen gate
    (the contracts-1 regression class, avoided by construction)."""
    v = "aim for 1000000000 lifetime steps by 2026"
    assert pii_scan.scan_text_full(v, token_config=NO_CONFIG) == 0                       # frozen default: OFF
    assert pii_scan.scan_operator_value(v, token_config=NO_CONFIG, full=True) >= 1       # operator-value: ON


def test_email_pattern_is_length_bounded_no_redos():
    """SEC-DEID-05: the email local-part/domain are length-bounded so the unanchored `+`
    cannot backtrack O(n^2) on a long no-@ blob in the uncapped scan_text_full. Structural
    guard (a timing assert would flake): the RFC-64 local-part bound must be present, and
    real emails still match."""
    email_src = pii_scan._VALUE_PII_PATTERNS["email"][0]
    assert "{1,64}" in email_src, "the email local-part length bound (ReDoS guard) was removed"
    for e in ("op.user@protonmail.com", "A@B.CO", "x_y+z@mail.example.org"):
        assert pii_scan.scan_text_full(e, token_config=NO_CONFIG) >= 1, e


@pytest.mark.parametrize("value", [
    "train at 5 Star Gym Way",             # Title-case gym name, not a street (BUG-1)
    "30 min Dr Patel followup",            # 'Dr' as Doctor honorific, not Drive (BUG-1)
    "1 Rep Max St progression",            # 'St' Title-cased in training text (BUG-1)
    "run 5 miles at zone 2",
    "weight 185 lbs this week",
    "3 sets of 10 reps",
    "BP 120 over 80",
    "sleep 7-8 hours",
    "call 4155550199",                     # bare contiguous 10-digit — out of scope (numeric-ID flood)
    "return to pre-Jan-2026 loading",      # the clean goal-targets baseline value
    "4 vial lot 90210",                    # number+words+5-digit with no suffix/state co-signal (nue)
    "10 St John's Wort daily",             # 'St' as Saint + a number, no ZIP (nue)
    "5 Star Gym Way every morning",        # street-suffix word but no ZIP anywhere (nue)
    "walked 5 km in 10000 steps",          # word-state 'in' + metric, tail guard kills it (BUG-1)
    "target 10000 steps or 12500 calories",  # word-state 'or' + two ZIP-shaped metrics (BUG-1)
    "12 week plan from dr patel: 10000 steps/day",  # 'dr' honorific as street-suffix lead (BUG-2)
    "10 sets in 90210 zone",               # word-state 'in' + 5-digit mid-value (HIST-1)
    "walked 5 miles today\nthen logged 62704 steps",  # cross-line, no street-number+suffix co-signal (F12)
])
def test_scan_text_value_boundary_negative_controls(value):
    """g5x AC2 + nue: health free-text does NOT trip the value patterns (== 0).

    Pins the false-positive boundary: Title-cased gym/training text (which a
    case-sensitive postal regex would have wrongly raised on — PR#78 BUG-1),
    rep/distance/weight/BP numerics, bare contiguous phone digits (numeric-ID flood —
    F-TEST2 honest boundary), and date fragments must not register as PII. The nue
    rows pin the postal detector's co-signal anchoring: a bare 5-digit number, a
    Saint/honorific 'St'/'Dr', or a suffix-shaped word WITHOUT a ZIP must not match.
    The BUG-1/BUG-2/HIST-1 rows pin the (?!\\s*\\w) tail guard: a ZIP-shaped metric
    followed by more words must not match even with a word-state/honorific co-signal
    (a hit here fail-closes planning on legit health text). The cross-line row pins
    that the widened [\\s\\S] two-line-postal span (bead 6hts) still requires the
    street-number + suffix co-signal — a ZIP-shaped metric on a later line without
    that lead-in must NOT match (the two-line ADDRESS itself is a positive control in
    test_scan_text_detects_ssn_and_two_line_postal). The leading liveness assert proves
    _VALUE_COMPILED is ACTIVE, so a regression that disabled the patterns reds here too
    (not only in the positive-detection test — F-TEST1).
    """
    assert pii_scan.scan_text("x@protonmail.com", token_config=NO_CONFIG) >= 1  # patterns live
    assert pii_scan.scan_text(value, token_config=NO_CONFIG) == 0


def test_scan_text_postal_accepted_residual_value_final_metric():
    """nue residual pin: a value ENDING in a bare 5-digit metric after a word-state
    token ("felt ok," -> 'ok' is Oklahoma) survives the tail guard and STILL matches.

    This is the documented accepted false positive (fail-closed: the operator
    rephrases). Pinned so a future regex change that silently flips it to 0 reds
    here and forces the residual documentation in _VALUE_PII_PATTERNS to be
    re-evaluated alongside it.
    """
    assert pii_scan.scan_text("did 3 sets, felt ok, 10000", token_config=NO_CONFIG) >= 1


def test_scan_text_caps_input_length():
    """SEC-1: scan_text bounds match cost by capping input at _MAX_SCAN_TEXT_LEN.

    The unanchored email local-part makes `findall` O(n^2); the cap bounds the worst
    case. A pass-through value is a short stated token, so PII beyond the cap is not
    scanned. Reds if the cap is removed (the trailing email would then be found).
    """
    filler = "a" * pii_scan._MAX_SCAN_TEXT_LEN
    # PII past the cap is truncated away -> not found.
    assert pii_scan.scan_text(filler + " x@protonmail.com", token_config=NO_CONFIG) == 0
    # Control: the same email within the cap IS found.
    assert pii_scan.scan_text("x@protonmail.com " + filler, token_config=NO_CONFIG) >= 1


def test_scan_accepts_deprecated_identity_config_alias(tmp_path):
    """b9l: `scan(identity_config=...)` still detects AND emits DeprecationWarning.

    The ADR-0005-T1 recipe pins the published `scan` surface under change control;
    the alias keeps the pre-b9l kwarg working. Reds if the alias is dropped
    (TypeError) or its DeprecationWarning is removed without Architect review.
    """
    root = _scratch_clone(tmp_path)
    cfg = _identity_config(tmp_path)
    leak = root / "code.py"
    leak.write_text(leak.read_text() + PLANTS["identity"])
    _git(["add", "-A"], root)
    with pytest.warns(DeprecationWarning):
        assert scan(_tracked(root), identity_config=cfg) >= 1


def test_scan_text_accepts_deprecated_identity_config_alias(tmp_path):
    """b9l: `scan_text(identity_config=...)` detects AND warns, mirroring scan."""
    cfg = _identity_config(tmp_path)
    with pytest.warns(DeprecationWarning):
        assert pii_scan.scan_text("ask Examplename first", identity_config=cfg) >= 1


def test_both_token_kwargs_raise_typeerror(tmp_path):
    """PR#100 F2: `token_config` + `identity_config` together raise TypeError.

    The pre-fix alias-wins resolution silently discarded the caller's
    `token_config`, masking a caller bug. Both functions refuse the pair. Reds
    if either function resolves the conflict silently again.
    """
    root = _scratch_clone(tmp_path)
    cfg = _identity_config(tmp_path)
    with pytest.raises(TypeError, match="not both"):
        scan(_tracked(root), token_config=cfg, identity_config=cfg)
    with pytest.raises(TypeError, match="not both"):
        pii_scan.scan_text("ask Examplename first", token_config=cfg,
                           identity_config=cfg)


def test_trunk_scan_stays_gmail_conservative(tmp_path):
    """g5x AC2: the trunk-wide `scan` is NOT widened — clonability is preserved.

    The widened value classes (non-gmail email / phone / postal) are scoped to the
    value boundary (scan_text) only. The trunk commit-scanner `scan` must still ignore
    them (its gmail-only contact choice keeps a fresh clone from flooding on docs/test
    fixtures — see bead 3lv). Reds if a future edit widens `scan` to the value classes.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "code.py"
    # Only the WIDENED value classes — no @gmail.com, no structural store line, no identity.
    leak.write_text(
        leak.read_text()
        + "contact x@protonmail.com\n"
        + "phone +1 415 555 0199\n"
        + "ship to 123 main st, springfield il 62704\n"
    )
    _git(["add", "-A"], root)
    assert scan(_tracked(root), token_config=NO_CONFIG) == 0


# --- SEC-02 / aque: CLAUDE_CODE_OAUTH_TOKEN secret detection -------------------
# The OAuth token literal is assembled at RUNTIME so this tracked test file carries
# no matchable `sk-ant-oat`+alnum literal — the tree-wide token scan (and, once this
# feature lands, `scan` itself) greps ALL tracked files, prose + tests included, so a
# naive literal here would self-trip the very scanner under test (PF-S112-01). The
# in-source fragments (`"sk-"`, `"ant-"`, `"oat"`) never form a contiguous
# `sk-ant-oat`+alnum, so neither the pattern under test nor the ADR-0039 T2 tree scan
# matches this file.
_OAUTH_PREFIX = "sk-" + "ant-" + "oat"


def _synthetic_oauth_token():
    """A synthetic (non-real) token of the `sk-ant-oat<alnum>` shape, runtime-built."""
    return _OAUTH_PREFIX + "01" + "A9b8C7d6" * 5


# The no-train API-key prefix (bead SEC-01): the SEPARATE `a-plus-maxing-api-key`
# keychain item the ModelClient reads — same runtime fragment-assembly so this file
# carries no matchable `sk-ant-api`+alnum literal (the very trap this bead's own text
# tripped; PF-S112-01).
_API_PREFIX = "sk-" + "ant-" + "api"


def _synthetic_api_key():
    """A synthetic (non-real) key of the `sk-ant-api<alnum>` shape, runtime-built."""
    return _API_PREFIX + "03" + "F4e5D6c7" * 5


def test_oauth_token_secret_blocked_trunk_wide(tmp_path):
    """SEC-02 (aque): a leaked CLAUDE_CODE_OAUTH_TOKEN is BLOCKED trunk-wide by `scan`.

    `pii_scan` is the SINGLE policy the block-pii-commit + pre-push-pii-scan hooks run,
    but it had NO secret/credential detection — a `sk-ant-oat...` token in a tracked
    file passed both hooks clean (only the ADR-0039-T2 pytest-time tree scan, a
    backstop over already-tracked files, caught it — missing new-file commits,
    `--no-verify`, and human-terminal commits). The token is operator-AGNOSTIC (a
    credential shape, not operator data), so `scan` must detect it with NO token config
    AND even in the fixture scope (`include_structural=False`) — a leaked token in a
    `tests/` fixture is still a leak. RED before the pattern is added; mutation-RED if
    `_COMPILED_SECRET` is later removed from `scan`.
    """
    root = _scratch_clone(tmp_path)
    # AC: clean tracked set -> the secret class adds 0 (non-vacuous baseline).
    assert scan(_tracked(root), token_config=NO_CONFIG) == 0

    leak = root / "code.py"
    leak.write_text(leak.read_text() + f"OAUTH_TOKEN = {_synthetic_oauth_token()!r}\n")
    _git(["add", "-A"], root)

    # Detected with NO identity config (agnostic secret pattern)...
    assert scan(_tracked(root), token_config=NO_CONFIG) >= 1
    # ...AND in the fixture scope (structural off) — a token in tests/ is a leak.
    assert scan(_tracked(root), token_config=NO_CONFIG, include_structural=False) >= 1


def test_api_key_secret_blocked_trunk_wide(tmp_path):
    """SEC-01 (sibling of aque): a leaked no-train API key (`sk-ant-api…`) is BLOCKED
    trunk-wide by `scan`, exactly as the OAuth token. The api-prefixed key is the
    SEPARATE `a-plus-maxing-api-key` keychain item — a live METERED-SPEND credential —
    so an accidental commit into this PUBLIC repo is a spend-leak (the same threat model
    aque closed for the OAuth token). Detected with NO token config AND in the fixture
    scope (`include_structural=False`). RED before the sibling pattern is added;
    mutation-RED if its `SECRET_PATTERNS` entry is removed.
    """
    root = _scratch_clone(tmp_path)
    assert scan(_tracked(root), token_config=NO_CONFIG) == 0

    leak = root / "code.py"
    leak.write_text(leak.read_text() + f"API_KEY = {_synthetic_api_key()!r}\n")
    _git(["add", "-A"], root)

    assert scan(_tracked(root), token_config=NO_CONFIG) >= 1
    assert scan(_tracked(root), token_config=NO_CONFIG, include_structural=False) >= 1


def test_secret_patterns_anchored_not_overbroad(tmp_path):
    """The secret patterns are anchored to the `sk-ant-oat` (OAuth) and `sk-ant-api`
    (no-train API key) prefixes — a DIFFERENT `sk-ant-` shape, or EITHER bare prefix
    with no trailing alnum, does NOT match, so the trunk scanner does not flood on
    incidental `sk-ant-` mentions in docs (clonability preserved; the same conservatism
    as the gmail-only contact choice). Reds if a future edit broadens either pattern to
    bare `sk-ant-`.

    Leads with an F-TEST1 liveness assert (mirrors the sibling negative-control tests):
    a real token of EACH covered class detects, so the `== 0` near-miss assertions below
    cannot go vacuously green under a regression that disables the secret patterns.
    """
    # F-TEST1 liveness: BOTH covered classes detect (else the `== 0` below is vacuous).
    live = tmp_path / "live.txt"
    live.write_text(f"O = {_synthetic_oauth_token()!r}\nA = {_synthetic_api_key()!r}\n")
    assert scan([str(live)], token_config=NO_CONFIG) >= 2  # both patterns live

    root = _scratch_clone(tmp_path)
    leak = root / "README.md"
    other = ("sk-" + "ant-") + "zzz9-" + "notarealprefix"  # a sk-ant- shape, neither oat nor api
    bare_oat = _OAUTH_PREFIX                                # oat prefix, no trailing alnum
    bare_api = _API_PREFIX                                  # api prefix, no trailing alnum
    leak.write_text(
        leak.read_text() + f"mentions {other} and {bare_oat} and {bare_api} only\n"
    )
    _git(["add", "-A"], root)

    assert scan(_tracked(root), token_config=NO_CONFIG) == 0


def test_scan_scoped_blocks_oauth_token_in_fixture_path(tmp_path):
    """`scan_scoped` (the single policy both hooks run) blocks an OAuth token even on a
    `tests/`-prefixed fixture path — where the structural net is intentionally OFF
    (bead dv3), the secret pattern must still fire (a token in a fixture is a leak).
    """
    root = _scratch_clone(tmp_path)
    fixture = root / "tests"
    fixture.mkdir()
    (fixture / "conftest_fixture.py").write_text(
        f"TOKEN = {_synthetic_oauth_token()!r}\n"
    )
    _git(["add", "-A"], root)
    changed = _tracked(root)
    # scan_scoped keys the fixture partition on the "tests/" prefix of the REPO-relative
    # path; _tracked returns absolute paths, so pass repo-relative here.
    rel = [str(Path(p).relative_to(root)) for p in changed]
    import os
    cwd = os.getcwd()
    try:
        os.chdir(root)
        assert pii_scan.scan_scoped(rel, [], contact_config=NO_CONFIG,
                                    identity_config=NO_CONFIG) >= 1
    finally:
        os.chdir(cwd)
