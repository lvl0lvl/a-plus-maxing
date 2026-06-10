"""Tests for scripts/guard/pii_scan.py — tracked-file operator-PII scanner.

`scan(tracked_files, identity_config=...) -> int` reads each file's CONTENTS and
counts operator-PII matches. The operator-AGNOSTIC patterns (two structural
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
    assert scan(_tracked(root), identity_config=cfg) == 0

    # AC-3: plant every class into a tracked file's CONTENTS in the SAME clone.
    leak = root / "README.md"
    body = leak.read_text()
    for token in PLANTS.values():
        body += token
    leak.write_text(body)
    _git(["add", "-A"], root)

    assert scan(_tracked(root), identity_config=cfg) >= 1


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

    assert scan(_tracked(root), identity_config=NO_CONFIG) >= 1


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
    assert scan(files, identity_config=cfg) >= 1
    # Same token, no config -> agnostic patterns find nothing here -> 0.
    assert scan(files, identity_config=NO_CONFIG) == 0


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

    assert scan(_tracked(root), identity_config=cfg) >= 1


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
    assert scan(files, identity_config=str(cfg)) >= 1
    # Same address, no config -> NOT detected (the generic-gmail flood is gone).
    assert scan(files, identity_config=NO_CONFIG) == 0


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

    assert scan(_tracked(root), identity_config=NO_CONFIG) >= 1


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

    assert scan(_tracked(root), identity_config=NO_CONFIG) >= 1
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
    assert scan(files, identity_config=NO_CONFIG) >= 1
    # Switch off, no config: the structural plant alone scores 0.
    assert scan(files, identity_config=NO_CONFIG, include_structural=False) == 0
    # Switch off, config present: the contact token STILL detects.
    assert scan(files, identity_config=str(cfg), include_structural=False) >= 1


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
    assert isinstance(scan(_tracked(root), identity_config=NO_CONFIG), int)


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
    assert scan(_tracked(root), identity_config=str(cfg)) >= 1


def test_identity_match_is_case_insensitive(tmp_path):
    """2x1: an operator-identity token matches case-insensitively (config-driven)."""
    root = _scratch_clone(tmp_path)
    cfg = _identity_config(tmp_path, token="Examplename")
    leak = root / "code.py"
    leak.write_text(leak.read_text() + "contact EXAMPLENAME today\n")
    _git(["add", "-A"], root)
    assert scan(_tracked(root), identity_config=cfg) >= 1


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
    assert scan_text("hello world, no pii here", identity_config=NO_CONFIG) == 0
    assert scan_text("mail me at Test.Fixture@Gmail.COM", identity_config=NO_CONFIG) >= 1  # case-insensitive too
    assert scan_text("ask Examplename first", identity_config=cfg) >= 1
    assert scan_text("ask Examplename first", identity_config=NO_CONFIG) == 0


def test_scan_text_scopes_out_structural_store_pattern():
    """scan_text targets personal-identity tokens (name/contact), NOT the file-
    structural store-line patterns (those detect a leaked store NDJSON FILE, not raw
    PII inside a scalar summary token). A bare store line carries no personal data."""
    from scripts.guard.pii_scan import scan_text

    store_line = (
        '{"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", '
        '"source": "manual", "value": 55}'
    )
    assert scan_text(store_line, identity_config=NO_CONFIG) == 0


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
    assert pii_scan.scan_text(value, identity_config=NO_CONFIG) >= 1, label


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
    assert pii_scan.scan_text(value, identity_config=NO_CONFIG) >= 1, label


def test_scan_text_detects_compatibility_homograph_email():
    """g5x AC1: an NFKC compatibility-homograph email (fullwidth @) is caught.

    A fullwidth commercial-at (U+FF20) folds to '@' under NFKC, so 'op<FF20>gmail.com'
    is the same contact and must score >=1 — reds without the NFKC fold. (Cross-script
    confusables, e.g. Cyrillic, are out of scope for the single-operator value boundary.)
    """
    homograph = "reach me op＠gmail.com"
    assert pii_scan.scan_text(homograph, identity_config=NO_CONFIG) >= 1


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
    "123 Main St\nSpringfield, IL 62704",  # canonical TWO-LINE address — out of scope (TEST-1)
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
    (a hit here fail-closes planning on legit health text). The two-line row pins the
    documented out-of-scope street-line/city-line newline split. The leading liveness
    assert proves _VALUE_COMPILED is ACTIVE, so a regression that disabled the
    patterns reds here too (not only in the positive-detection test — F-TEST1).
    """
    assert pii_scan.scan_text("x@protonmail.com", identity_config=NO_CONFIG) >= 1  # patterns live
    assert pii_scan.scan_text(value, identity_config=NO_CONFIG) == 0


def test_scan_text_postal_accepted_residual_value_final_metric():
    """nue residual pin: a value ENDING in a bare 5-digit metric after a word-state
    token ("felt ok," -> 'ok' is Oklahoma) survives the tail guard and STILL matches.

    This is the documented accepted false positive (fail-closed: the operator
    rephrases). Pinned so a future regex change that silently flips it to 0 reds
    here and forces the residual documentation in _VALUE_PII_PATTERNS to be
    re-evaluated alongside it.
    """
    assert pii_scan.scan_text("did 3 sets, felt ok, 10000", identity_config=NO_CONFIG) >= 1


def test_scan_text_caps_input_length():
    """SEC-1: scan_text bounds match cost by capping input at _MAX_SCAN_TEXT_LEN.

    The unanchored email local-part makes `findall` O(n^2); the cap bounds the worst
    case. A pass-through value is a short stated token, so PII beyond the cap is not
    scanned. Reds if the cap is removed (the trailing email would then be found).
    """
    filler = "a" * pii_scan._MAX_SCAN_TEXT_LEN
    # PII past the cap is truncated away -> not found.
    assert pii_scan.scan_text(filler + " x@protonmail.com", identity_config=NO_CONFIG) == 0
    # Control: the same email within the cap IS found.
    assert pii_scan.scan_text("x@protonmail.com " + filler, identity_config=NO_CONFIG) >= 1


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
    assert scan(_tracked(root), identity_config=NO_CONFIG) == 0
