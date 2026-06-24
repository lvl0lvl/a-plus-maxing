"""The deterministic PII re-insertion OUT pass (ADR-0021-T1) — the crown jewel.

`reinsert_out(html, target_path)` is the deterministic, model-free OUT re-insertion: it takes
the produced (de-identified, initials-only) render HTML and the path the render is destined for,
and RETURNS the render with the real operator full name re-inserted over the initials placeholder
— but ONLY when `target_path` is confirmable-gitignored. It RETURNS A STRING; it does NOT write
the artifact. The CALLER (ADR-0025-T1) owns the write to the SAME path it `git check-ignore`-
confirmed. `target_path` is the path the re-insertion is gated ON (the confirm), not a path this
module writes to — keeping the OUT pass write-free, so the persisted store and every tracked
render trivially stay de-identified.

Fail-closed default: when the target is NOT confirmable-gitignored (`git check-ignore` non-zero),
or the gitignored identity source is absent, NO re-insertion is performed — the initials-only
`html` is returned unchanged (the ADR-0021 fail-closed-to-initials decision). Deterministic and
model-free on either branch: NO `scripts.model` symbol is imported and no model client is
constructed (the single-egress-class invariant — no real PII to any model on the OUT path).

The in-process `git check-ignore` confirm is best-effort defense-in-depth, NOT the fail-closed
authority — the confirm and the caller's subsequent write are non-atomic (a TOCTOU window). The
authority that no name-bearing tracked file ever commits is the commit/push PII hooks
(`block-pii-commit.sh` + `pre-push-pii-scan.sh`, the ADR-0021-T0-SCANSCOPE coverage over
`vault/artifacts/generated/`), which scan the staged/pushed set at the egress boundary.

The full name is read DIRECTLY from the gitignored profile source (the
`^# Operator Profile — (.+)$` title) — the SAME source `component_set.read_profile` reads, but
the full name the title holds, not the initials `read_profile` derives from it.

Published surface (consumed by ADR-0025-T1): `reinsert_out(html, target_path) -> str`.
"""

import re
import subprocess
from pathlib import Path

# The gitignored profile sources, same preference order as the face sheet / handout header: the
# ADR-0005 filled copy (gitignored) wins over the tracked scaffold. The title line carries the
# FULL NAME (`read_profile` derives initials from it; this pass reads the full name). Module
# constant so the caller / tests can point it at fixtures.
DEFAULT_PROFILE_PATHS = (
    Path("vault/scaffold/filled/operator-profile.md"),
    Path("vault/meta/operator-profile.md"),
)

# The profile title carrying the operator's full name (same regex `read_profile` parses).
_TITLE_RE = re.compile(r"^# Operator Profile — (.+)$", re.M)


def _read_full_name(profile_paths):
    """Return the operator full name from the first existing profile title, or None.

    Reads the FIRST existing `profile_paths` entry (the caller orders them: the gitignored
    filled copy first, then the tracked scaffold) and returns the full name the
    `^# Operator Profile — (.+)$` title holds. Absent profile, or no title, returns None — the
    fail-closed signal (no re-insertion).
    """
    path = next((p for p in profile_paths if p.exists()), None)
    if path is None:
        return None
    title = _TITLE_RE.search(path.read_text(encoding="utf-8"))
    if not title:
        return None
    name = title.group(1).strip()
    return name or None


def _initials_of(full_name):
    """Derive the initials `read_profile` renders from a full name (the placeholder to replace)."""
    return "".join(word[0].upper() for word in full_name.split() if word[0].isalpha())


def _target_is_gitignored(target_path, repo_root):
    """True when `git check-ignore <target_path>` exits 0 (the per-target gitignored confirm).

    The same `git check-ignore` mechanism `pii_scan.store_is_gitignored` wraps, generalized from
    the fixed `vault/store/` to the supplied target. Best-effort defense-in-depth (the confirm
    and the caller's write are non-atomic); the fail-closed authority is the commit/push hooks.
    """
    return (
        subprocess.run(
            ["git", "check-ignore", str(target_path)],
            cwd=repo_root,
            capture_output=True,
        ).returncode
        == 0
    )


def reinsert_out(html, target_path, *, _profile_paths=DEFAULT_PROFILE_PATHS, _repo_root=None):
    """Re-insert the operator full name into `html` when `target_path` is confirmable-gitignored.

    Deterministic, model-free. RETURNS the render as a STRING; writes NOTHING (the caller owns
    the write to the same path it `git check-ignore`-confirmed). When `target_path` is
    confirmable-gitignored AND the gitignored identity source holds a full name, the
    `Patient <initials>` placeholder is substituted with the full name and the name-bearing
    string is returned. Otherwise (target not gitignored, or no profile source) the initials-only
    `html` is returned unchanged — the fail-closed default.

    Args:
        html (str): The produced (de-identified, initials-only) render HTML.
        target_path (str | Path): The path the render is destined for — the gate input the
            re-insertion is confirmed against (`git check-ignore`), NOT a path this module writes.
        _profile_paths (tuple, optional): Gitignored profile sources in preference order — a
            test/caller seam; defaults to the engine-owned `DEFAULT_PROFILE_PATHS`.
        _repo_root (str | Path, optional): The repo root the `git check-ignore` confirm runs in;
            defaults to the current working directory (the trunk).

    Returns:
        (str) The name-bearing render when the target is confirmable-gitignored and a full name
        is available, else the initials-only `html` unchanged (fail-closed).
    """
    if not _target_is_gitignored(target_path, _repo_root):
        return html
    full_name = _read_full_name(_profile_paths)
    if full_name is None:
        return html
    initials = _initials_of(full_name)
    if not initials:
        return html
    return html.replace(f"Patient {initials}", f"Patient {full_name}")
