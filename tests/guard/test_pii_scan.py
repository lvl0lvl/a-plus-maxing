"""Tests for scripts/guard/pii_scan.py — tracked-file operator-PII scanner.

`scan(tracked_files) -> int` reads each file's CONTENTS and counts operator-PII
matches across the spike's declared token set (identity, contact, structural
store-line). AC-2/AC-3 run the SAME scanner over the SAME controlled scratch git
clone: clean set -> 0, then a planted token per class -> >=1, with the offending
path reported via the single PII-HIT: <path> stderr channel. AC-4 checks
git check-ignore vault/store/ in both directions (entry present -> 0, absent ->
fail). A no-op scanner (always 0) must fail the plant tests.
"""

import subprocess

import pytest

from scripts.guard import pii_scan
from scripts.guard.pii_scan import scan

# One planted token per declared operator-PII class. The structural health-data
# token is a real {item,timepoint,source,value} store line (biomarker-independent).
PLANTS = {
    "identity": 'patient name: Walter McGivney\n',
    "contact": 'reply-to: operator@example.com\n',
    "health-data": (
        '{"item": "rhr", "timepoint": "2026-06-01T08:00:00+00:00", '
        '"source": "manual", "value": 55}\n'
    ),
}


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


def test_scan_clean_then_planted_same_clone(tmp_path):
    """AC-2 + AC-3 same scanner / same clone: 0 on clean, >=1 once planted.

    Proves the 0-on-clean result against a scanner demonstrably capable of >=1
    (QA F1+F2), against the controlled scratch fileset (not the live ls-files set).
    """
    root = _scratch_clone(tmp_path)
    # AC-2: clean tracked set -> 0.
    assert scan(_tracked(root)) == 0

    # AC-3: plant every class into a tracked file's CONTENTS in the SAME clone.
    leak = root / "README.md"
    body = leak.read_text()
    for token in PLANTS.values():
        body += token
    leak.write_text(body)
    _git(["add", "-A"], root)

    assert scan(_tracked(root)) >= 1


@pytest.mark.parametrize("pii_class", sorted(PLANTS))
def test_scan_hits_each_pii_class(tmp_path, pii_class):
    """AC-3 class completeness (Security HIGH-2): >=1 for a token per class.

    Each declared class (identity, contact, health-data) planted alone into a
    tracked file's CONTENTS must produce >=1 — a single-token scanner fails this.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "code.py"
    leak.write_text(leak.read_text() + PLANTS[pii_class])
    _git(["add", "-A"], root)

    assert scan(_tracked(root)) >= 1


def test_implemented_token_set_equals_declared(tmp_path):
    """Token set EQUALS the spike's declared set (not a subset).

    The scanner exposes its patterns as a module-level structure; this asserts
    one pattern per declared class and the exact spike regexes, so the scanner
    cannot ship a narrower set than the spike fixed.
    """
    declared = {
        "identity": r"Walter|McGivney",
        "contact": r"[A-Za-z0-9._%+-]+@gmail\.com",
        "health-data-item-then-tp": (
            r'("item"|"value").*"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'
        ),
        "health-data-tp-then-item": (
            r'"timepoint"\s*:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}.*("item"|"value")'
        ),
    }
    assert set(pii_scan.TOKEN_PATTERNS) == set(declared)
    assert pii_scan.TOKEN_PATTERNS == declared


def test_scan_names_offending_file_on_stderr(tmp_path, capfd):
    """AC-3 offending-file channel (Security MED): PII-HIT: <path> on stderr.

    The single pinned channel the ADR-0005-T1 hook reads — not the return value,
    not a second channel.
    """
    root = _scratch_clone(tmp_path)
    leak = root / "README.md"
    leak.write_text(leak.read_text() + PLANTS["identity"])
    _git(["add", "-A"], root)
    offending = str(leak)

    assert scan(_tracked(root)) >= 1
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
    assert isinstance(scan(_tracked(root)), int)
