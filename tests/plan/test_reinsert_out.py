"""Tests for the deterministic PII re-insertion OUT pass (ADR-0021-T1) — the crown jewel.

`scripts.plan.reinsert_out.reinsert_out(html, target_path)` is the deterministic, model-free
OUT re-insertion: produced HTML in, a STRING out (the artifact content) carrying the real
operator full name when `target_path` is confirmable-gitignored, else the initials-only `html`
unchanged (fail-closed). It does NOT write — the CALLER (ADR-0025-T1) owns the write to the
SAME path it `git check-ignore`-confirmed. These tests pin the five acceptance criteria:

  - AC-1: a confirmable-gitignored target RETURNS a string whose header shows the operator's
    FULL NAME (read from the gitignored source), not initials (return-string contract; the
    module writes nothing);
  - AC-2: the SAME call with a TRACKED target suppresses re-insertion and returns the
    initials-only string (the fail-closed default), AND the high-entropy full-name token is
    ABSENT from that output (the name did not leak onto the tracked target);
  - AC-3 (Risk — single egress class): the module imports NOTHING from `scripts.model` —
    asserted on the module's IMPORT SET (its namespace), never a substring grep;
  - AC-4 (Risk — ADR-0005): after a re-inserting render, `pii_scan.scan` over a synthetic
    `vault/store/` and the tracked set returns 0 real-PII hits — the store and every tracked
    render stay de-identified (the OUT pass writes nothing);
  - Symlinked / path-divergent target (MEDIUM-1): a symlink under a gitignored prefix pointing
    OUT to a tracked location — the return-string contract holds (no write occurs), so a
    symlink cannot redirect a write to an escaped path.

Every fixture is SYNTHETIC (0 real operator PII in the test tree). The full-name oracle is a
high-entropy token (`Zxqvarn Wolthrip`) with zero overlap with the template HTML boilerplate,
so the AC-1-bytes-contain and AC-2-name-absent assertions cannot false-pass or false-fail.
"""

import importlib
import subprocess

from scripts.guard import pii_scan
from scripts.plan import reinsert_out as reinsert_out_mod
from scripts.plan.reinsert_out import reinsert_out


# --- synthetic fixtures (0 real operator PII) ----------------------------------

# The full-name oracle: high-entropy, zero overlap with the template HTML boilerplate
# (NOT "Test Operator" — that collides with the literal "Operator"/"Patient" in template text
# and would make the bytes-contain / name-absent assertions false-pass/false-fail). The initials
# the de-identified render carries for this name are "ZW".
SYNTHETIC_FULL_NAME = "Zxqvarn Wolthrip"
SYNTHETIC_INITIALS = "ZW"

# A produced-HTML fixture carrying the initials placeholder, in the handout header shape
# (`Patient <initials>`). It carries the word "Operator"/"Patient" boilerplate but NOT the
# high-entropy full-name token — verified by the guard below.
PRODUCED_HTML = (
    "<html><body><div class='hd-head-block'><div class='hd-status'>"
    f"Patient {SYNTHETIC_INITIALS} · age band 40s · issue status recovering"
    "</div></div></body></html>"
)

assert SYNTHETIC_FULL_NAME not in PRODUCED_HTML, (
    "fixture invariant: the full-name oracle must not appear in the produced HTML before "
    "re-insertion, else the AC-1/AC-2 presence/absence assertions are vacuous"
)


def _write_synthetic_profile(tmp_path):
    """Write a synthetic gitignored identity profile and return its Path.

    Mirrors the real source shape: a `# Operator Profile — <synthetic full name>` title line
    `read_profile` / the re-insertion read the name from. NEVER the real filled profile.
    """
    profile = tmp_path / "operator-profile.md"
    profile.write_text(
        f"# Operator Profile — {SYNTHETIC_FULL_NAME}\n\n"
        "- **Age:** 44\n- **Current status:** recovering\n",
        encoding="utf-8",
    )
    return profile


def _init_repo_with_gitignore(tmp_path):
    """Init a temp git repo gitignoring `vault/artifacts/generated/`; return its root Path.

    Gives a real `git check-ignore` surface so the gitignored / tracked verdicts the gate
    keys on are genuine, not stubbed.
    """
    repo = tmp_path / "repo"
    (repo / "vault" / "artifacts" / "generated").mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("vault/artifacts/generated/\n", encoding="utf-8")
    return repo


# --- AC-1: confirmable-gitignored target -> full name in the returned string ---


def test_gitignored_target_shows_full_name(tmp_path):
    """AC-1: a gitignored target returns a string whose header shows the FULL NAME, not initials."""
    repo = _init_repo_with_gitignore(tmp_path)
    profile = _write_synthetic_profile(tmp_path)
    target = repo / "vault" / "artifacts" / "generated" / "plan.html"

    out = reinsert_out(PRODUCED_HTML, target, _profile_paths=(profile,), _repo_root=repo)

    assert SYNTHETIC_FULL_NAME in out, "the re-inserted render must carry the full name"
    assert f"Patient {SYNTHETIC_INITIALS}" not in out, "the initials placeholder must be replaced"


def test_gitignored_target_writes_nothing(tmp_path):
    """AC-1 (return-string contract): the module returns a string and writes NO artifact."""
    repo = _init_repo_with_gitignore(tmp_path)
    profile = _write_synthetic_profile(tmp_path)
    target = repo / "vault" / "artifacts" / "generated" / "plan.html"

    out = reinsert_out(PRODUCED_HTML, target, _profile_paths=(profile,), _repo_root=repo)

    assert isinstance(out, str)
    assert not target.exists(), "the OUT pass must not write the target — the caller writes"


# --- AC-2: tracked target -> fail-closed to initials-only, name absent ----------


def test_tracked_target_initials_only(tmp_path):
    """AC-2: a TRACKED target suppresses re-insertion and returns the initials-only string."""
    repo = _init_repo_with_gitignore(tmp_path)
    profile = _write_synthetic_profile(tmp_path)
    tracked_target = repo / "vault" / "report.html"  # not under the gitignored dropzone

    out = reinsert_out(PRODUCED_HTML, tracked_target, _profile_paths=(profile,), _repo_root=repo)

    assert out == PRODUCED_HTML, "fail-closed: the tracked target returns the html unchanged"
    assert SYNTHETIC_FULL_NAME not in out, "the full name must NOT leak onto a tracked target"


def test_absent_profile_source_initials_only(tmp_path):
    """AC-2 (fail-closed): an absent gitignored identity source -> no re-insertion, name absent."""
    repo = _init_repo_with_gitignore(tmp_path)
    absent = tmp_path / "does-not-exist.md"
    target = repo / "vault" / "artifacts" / "generated" / "plan.html"

    out = reinsert_out(PRODUCED_HTML, target, _profile_paths=(absent,), _repo_root=repo)

    assert out == PRODUCED_HTML, "no profile source -> no re-insertion (fail-closed)"
    assert SYNTHETIC_FULL_NAME not in out


# --- AC-3: no model import on the OUT path (import-set assertion, not a grep) ---


def test_no_model_import():
    """AC-3: the module's namespace resolves NO symbol to `scripts.model.*` (single egress class)."""
    mod = importlib.reload(reinsert_out_mod)
    leaked = []
    for name in dir(mod):
        value = getattr(mod, name)
        module_name = getattr(value, "__module__", None)
        if isinstance(module_name, str) and module_name.startswith("scripts.model"):
            leaked.append(name)
        # a bound module object imported directly (import scripts.model as x)
        mod_dunder = getattr(value, "__name__", None)
        if isinstance(mod_dunder, str) and mod_dunder.startswith("scripts.model"):
            leaked.append(name)
    assert leaked == [], f"reinsert_out must import nothing from scripts.model; leaked: {leaked}"


# --- AC-4: store + tracked set stay de-identified after a re-inserting render ---


def test_store_and_tracked_stay_deidentified(tmp_path):
    """AC-4: after a re-inserting render, `pii_scan.scan` over store + the tracked set = 0 hits."""
    repo = _init_repo_with_gitignore(tmp_path)
    profile = _write_synthetic_profile(tmp_path)
    target = repo / "vault" / "artifacts" / "generated" / "plan.html"

    # The re-inserting render returns the name-bearing string (held in memory; never written).
    out = reinsert_out(PRODUCED_HTML, target, _profile_paths=(profile,), _repo_root=repo)
    assert SYNTHETIC_FULL_NAME in out

    # A synthetic gitignored store + a synthetic tracked render — both de-identified by
    # construction (initials-only; the name lives only in the in-memory `out`). An identity
    # config matching the synthetic name so a leak WOULD be caught.
    identity = tmp_path / "operator-identity.txt"
    identity.write_text("Zxqvarn|Wolthrip\n", encoding="utf-8")

    store_file = tmp_path / "store-line.txt"
    store_file.write_text("training-age-band: 10-15y\nsex-for-dosing: male\n", encoding="utf-8")
    tracked_render = tmp_path / "tracked-report.html"
    tracked_render.write_text(PRODUCED_HTML, encoding="utf-8")  # initials-only, no name

    hits = pii_scan.scan(
        [str(store_file), str(tracked_render)],
        token_config=identity,
        include_structural=False,
    )
    assert hits == 0, "the persisted store and the tracked render must stay de-identified"


# --- SEC-02: a short initials token must not mis-substitute a longer placeholder ---


def test_single_word_name_does_not_mangle_longer_placeholder(tmp_path):
    """SEC-02: a 1-char initials token (single-word name) leaves a longer `Patient XW` intact.

    A single-word operator name (`Zephyr`) derives the 1-char initials `Z`. The produced HTML
    carries a LONGER `Patient ZW ·` placeholder. An unanchored `Patient Z` -> `Patient Zephyr`
    replace clobbers the `Patient ZW` token into `Patient ZephyrW` (RED on the old code); the
    word-boundary anchor refuses the within-token partial, leaving `Patient ZW` intact (GREEN).
    """
    repo = _init_repo_with_gitignore(tmp_path)
    profile = tmp_path / "operator-profile.md"
    profile.write_text("# Operator Profile — Zephyr\n", encoding="utf-8")
    target = repo / "vault" / "artifacts" / "generated" / "plan.html"

    html = (
        "<html><body><div class='hd-status'>"
        "Patient ZW · age band 40s · issue status recovering"
        "</div></body></html>"
    )

    out = reinsert_out(html, target, _profile_paths=(profile,), _repo_root=repo)

    # the longer `Patient ZW` placeholder is NOT mangled by the 1-char `Z` substitution
    assert "Patient ZW ·" in out, "the longer placeholder must survive the short-initials replace"
    assert "ZephyrW" not in out, "the short initials must not partially clobber the longer token"


# --- MEDIUM-1: symlinked / path-divergent target -------------------------------


def test_symlinked_target_return_string_contract(tmp_path):
    """MEDIUM-1: a symlink under a gitignored prefix pointing OUT — the contract holds, no write.

    The module does NOT write, so a symlink cannot redirect a write to an escaped realpath. The
    gate decision is governed by `git check-ignore` on the SUPPLIED path; the test pins that the
    return-string contract holds (a string out, the link target untouched) — making the
    divergence explicit. If a later revision adds a write, this probe must be extended to assert
    a realpath-resolution check.
    """
    repo = _init_repo_with_gitignore(tmp_path)
    profile = _write_synthetic_profile(tmp_path)

    # A real file OUTSIDE the gitignored dropzone (a tracked-shaped escape target).
    escape = repo / "vault" / "escape-tracked.html"
    escape.write_text("ESCAPE-TARGET-ORIGINAL\n", encoding="utf-8")

    # A symlink UNDER the gitignored prefix (so its own path `git check-ignore`s gitignored)
    # pointing OUT to the tracked escape file.
    link = repo / "vault" / "artifacts" / "generated" / "plan.html"
    link.symlink_to(escape)

    out = reinsert_out(PRODUCED_HTML, link, _profile_paths=(profile,), _repo_root=repo)

    assert isinstance(out, str), "a string is returned for a symlinked target"
    # The module writes NOTHING — the escape target is untouched (a write through the symlink
    # would have clobbered it).
    assert escape.read_text(encoding="utf-8") == "ESCAPE-TARGET-ORIGINAL\n", (
        "no write occurs, so the symlink cannot redirect a write to the escaped realpath"
    )
