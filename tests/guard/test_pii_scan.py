"""Tests for scripts/guard/pii_scan.py — tracked-file operator-PII scanner.

`scan(tracked_files, identity_config=...) -> int` reads each file's CONTENTS and
counts operator-PII matches. The operator-AGNOSTIC patterns (generic `@gmail.com`
contact + two structural store-line patterns) are tracked; the operator-IDENTITY
tokens load at run time from the gitignored `vault/meta/operator-identity.txt`.
AC-2/AC-3 run the SAME scanner over the SAME controlled scratch git clone: clean
set -> 0, then a planted token per class -> >=1, with the offending path reported
via the single PII-HIT: <path> stderr channel. Identity detection is proven
config-driven (a synthetic token detected only when the config supplies it) so no
operator name lives in tracked source. AC-4 checks git check-ignore vault/store/
in both directions. A no-op scanner (always 0) must fail the plant tests.
"""

import json
import subprocess

import pytest

from scripts.guard import pii_scan
from scripts.guard.pii_scan import scan

# A SYNTHETIC identity token (not the real operator) supplied via a tmp config,
# so the fixtures carry no operator name. Detection of this token must depend on
# the config being present (config-driven, not hardcoded).
SYNTHETIC_IDENTITY = "Testperson|Examplename"

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
    """Write a tmp identity config holding one synthetic token; return its path."""
    cfg = tmp_path / "operator-identity.txt"
    cfg.write_text(f"# synthetic test token\n{token}\n")
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
    """Agnostic patterns detect with NO identity config (non-existent path).

    A planted structural store-line and a generic `@gmail.com` contact are caught
    even when the gitignored identity config is absent (a fresh clone).
    """
    root = _scratch_clone(tmp_path)
    leak = root / "README.md"
    body = leak.read_text() + PLANTS["contact"] + PLANTS["health-data"]
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
    assert "Walter" not in src
    assert "McGivney" not in src


@pytest.mark.parametrize("pii_class", sorted(PLANTS))
def test_scan_hits_each_pii_class(tmp_path, pii_class):
    """AC-3 class completeness (Security HIGH-2): >=1 for a token per class.

    Each declared class (identity, contact, health-data) planted alone into a
    tracked file's CONTENTS must produce >=1 — a single-token scanner fails this.
    Identity is supplied via the synthetic tmp config.
    """
    root = _scratch_clone(tmp_path)
    cfg = _identity_config(tmp_path)
    leak = root / "code.py"
    leak.write_text(leak.read_text() + PLANTS[pii_class])
    _git(["add", "-A"], root)

    assert scan(_tracked(root), identity_config=cfg) >= 1


def test_agnostic_set_pins_spike_and_identity_is_config_sourced(tmp_path):
    """Tracked AGNOSTIC set EQUALS the spike's agnostic patterns; identity is not.

    The scanner exposes its agnostic patterns as a module-level structure; this
    asserts the exact spike regexes for contact + the two structural store-line
    patterns, and that no operator-identity literal is in that tracked set (it is
    sourced from the gitignored config instead).
    """
    declared_agnostic = {
        "contact": r"[A-Za-z0-9._%+-]+@gmail\.com",
        "health-data-item-then-tp": (
            r'("item"|"value")[\s\S]{0,400}?"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'
        ),
        "health-data-tp-then-item": (
            r'"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}[\s\S]{0,400}?("item"|"value")'
        ),
    }
    assert set(pii_scan.AGNOSTIC_PATTERNS) == set(declared_agnostic)
    assert pii_scan.AGNOSTIC_PATTERNS == declared_agnostic
    # Identity is config-sourced, not part of the tracked pattern set.
    assert "identity" not in pii_scan.AGNOSTIC_PATTERNS
    assert pii_scan.DEFAULT_IDENTITY_CONFIG.name == "operator-identity.txt"


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
    not a second channel.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "README.md"
    leak.write_text(leak.read_text() + PLANTS["contact"])
    _git(["add", "-A"], root)
    offending = str(leak)

    assert scan(_tracked(root), identity_config=NO_CONFIG) >= 1
    captured = capfd.readouterr()
    assert f"PII-HIT: {offending}" in captured.err


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
