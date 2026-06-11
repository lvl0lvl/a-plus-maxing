"""Tests for scripts/clone/init_instance.py — the fresh-clone init step (ADR-0005-T2).

`init_instance.run(clone_root)` is the one command a new operator runs after
`git clone` to reach a fillable, PII-free local instance. Its three load-bearing
properties are DATA-ISOLATION properties, gated here as falsifiable RED targets:
(Gate A / AC-2) data entered after init lands OUTSIDE git (untracked/gitignored);
(Gate B / AC-3) the instance generates a DASHBOARD from the clone's OWN inputs
alone with 0 reads of any other operator's store (0 cross-clone paths) — the plan
half of spec crit-3 is DEFERRED (assemble.py / ADR-0006-T2 is Wave 5); (Gate C /
AC-5) `run` references no network and no cross-clone path (egress guard observes 0
outbound; 0 reads outside the clone root), PLUS the SEC-03 failing-capable case
(an injected synthetic outbound call into a `run` path flips the guard to FAIL).

Each test runs against a scratch clone (a real git repo carrying the ADR-0005-T1
`.gitignore` boundary), never the live tree. The scaffold-page path convention is
not pinned upstream, so the AC-1 test self-plants a representative `status: scaffold`
page under `vault/scaffold/` (see the recipe's scaffold-page UPSTREAM FLAG).
"""

import os
import platform
import socket
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.clone import init_instance
from scripts.clone.init_instance import run
from scripts.generate.render import emit
from scripts.guard.egress_guard import run as egress_run
from scripts.store import store
from vault.design.templates import dashboard

REPO_ROOT = Path(__file__).resolve().parents[2]

DARWIN_ONLY = pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="OS-level egress isolation binding is exercised on the host OS (Darwin here)",
)

# The scaffold-page directory this executor chose for `run` to surface (recipe
# UPSTREAM FLAG: scaffold-page path convention not pinned; recorded for the
# orchestrator to formalize). A tracked vault dir, matching the existing
# vault/meta/*.md `status: scaffold` convention.
SCAFFOLD_DIR = "vault/scaffold"


def _make_scratch_clone(tmp_path):
    """Create a scratch git clone carrying the live ADR-0005-T1 `.gitignore` boundary.

    A real git repo (so `git status --porcelain` / `git check-ignore` run against
    it), with the live `.gitignore` copied verbatim so its `vault/store/` exclusion
    is present, plus a representative `status: scaffold` page self-planted under the
    tracked scaffold dir. Returns the clone root.
    """
    clone = tmp_path / "clone"
    clone.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=clone, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=clone, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=clone, check=True)
    (clone / ".gitignore").write_text((REPO_ROOT / ".gitignore").read_text())

    scaffold = clone / SCAFFOLD_DIR
    scaffold.mkdir(parents=True)
    (scaffold / "goals.md").write_text(
        "---\ntitle: Goals\ntype: note\nstatus: scaffold\n---\n\n# Goals\n"
    )
    subprocess.run(["git", "add", "-A"], cwd=clone, check=True)
    subprocess.run(["git", "commit", "-qm", "scratch clone"], cwd=clone, check=True)
    return clone


def _reading(timepoint="2026-06-01T08:00:00+00:00", value=55, item="rhr", source="manual"):
    """Build a reading carrying every Line Field Set field."""
    return {"item": item, "timepoint": timepoint, "source": source, "value": value}


class _OpenTrace:
    """Record every filesystem path the traced code reads/writes via pathlib.Path.

    `init_instance.run` and the dashboard generation touch the filesystem through
    `Path.read_text` / `Path.write_text` / `Path.open` / `Path.glob` / `Path.exists`
    (and `store.read` reads via `Path.read_text` / `Path.exists`) — NOT through
    `builtins.open` / `os.open`. So the trace patches those `Path` methods (the real
    I/O surface the code uses); a `builtins.open` patch would never fire and the
    Gate B/C assertions would pass vacuously. Each accessed path is resolved and
    compared against the clone root to prove 0 reads/writes outside it
    (Gate B 0-cross-clone-read / Gate C 0-outside-root-read property). The trace's
    own detection capability is proven by `test_open_trace_reds_on_out_of_root_read`.
    """

    _PATH_METHODS = ("read_text", "write_text", "open", "glob", "exists", "is_dir", "is_file")

    def __init__(self, monkeypatch):
        self.paths = []
        self._monkeypatch = monkeypatch

    def __enter__(self):
        trace = self
        for name in self._PATH_METHODS:
            real = getattr(Path, name)

            def traced(self, *args, __real=real, **kwargs):
                trace._record(self)
                return __real(self, *args, **kwargs)

            self._monkeypatch.setattr(Path, name, traced)
        return self

    def __exit__(self, *exc):
        return False

    def _record(self, path):
        try:
            self.paths.append(Path(path).resolve())
        except (TypeError, ValueError):
            pass  # non-path targets are not cross-clone reads

    def opens_outside(self, root):
        """Return recorded accesses that resolve outside `root` (cross-clone / off-root)."""
        root = Path(root).resolve()
        outside = []
        for p in self.paths:
            try:
                p.relative_to(root)
            except ValueError:
                outside.append(p)
        return outside


def test_open_trace_reds_on_out_of_root_read(tmp_path, monkeypatch):
    """Self-check: the read-trace REPORTS a deliberate read outside the clone root.

    Proves the trace's RED-capability (mirrors the SEC-03 clean-then-injected
    pattern). Without this, the Gate B/C `assert opens_outside == []` checks could
    pass vacuously (the original `builtins.open`/`os.open` trace never fired because
    the code reads via `Path.read_text`/`Path.exists`). A clean local read records 0
    off-root accesses; a deliberate read of a store OUTSIDE the clone root is flagged.
    """
    clone = _make_scratch_clone(tmp_path)
    run(clone)
    store_root = clone / "vault/store"

    # Sibling store OUTSIDE the clone root, carrying another operator's reading.
    sibling_store = tmp_path / "sibling-clone" / "vault/store"
    sibling_store.mkdir(parents=True)
    store.append("rhr", _reading(value=999, source="sibling"), root=sibling_store)

    # Clean direction: a local-only read records 0 off-root accesses.
    with _OpenTrace(monkeypatch) as clean:
        store.read("rhr", root=store_root)
    assert clean.opens_outside(clone) == [], "local read must not flag off-root"

    # Detection direction: an out-of-root read IS reported (trace turns red).
    with _OpenTrace(monkeypatch) as leaking:
        store.read("rhr", root=sibling_store)
    assert leaking.opens_outside(clone), "trace failed to report an out-of-root read"


# --------------------------------------------------------------------------- #
# Cycle 1 — init_instance.run + data-isolation gates (AC-1, AC-2, AC-3, AC-5)
# --------------------------------------------------------------------------- #


def test_fresh_clone_init_leaves_scaffolds_and_initialized_store(tmp_path):
    """AC-1: run() leaves empty status:scaffold pages + a readable INITIALIZED store.

    The store is in a valid initialized state: `store.read` over the local store
    returns an empty-but-well-formed read (empty reading set, NOT a missing/
    uninitialized-store error) — the test FAILS if run skips store init. The
    scaffold page is surfaced in its unfilled `status: scaffold` state, not rewritten.
    """
    clone = _make_scratch_clone(tmp_path)

    run(clone)

    # Store is initialized + readable (empty-but-well-formed), not missing.
    store_root = clone / "vault/store"
    assert store_root.is_dir(), "run did not initialize the store root"
    readings = store.read("rhr", root=store_root)
    assert readings == [], "initialized store should read empty-but-well-formed"

    # Scaffold page surfaced in its unfilled status:scaffold state, unmodified.
    scaffold_page = clone / SCAFFOLD_DIR / "goals.md"
    assert scaffold_page.exists()
    assert "status: scaffold" in scaffold_page.read_text()


def test_entered_data_lands_untracked(tmp_path):
    """AC-2 / Gate A: a reading entered after run() is untracked AND gitignored.

    Falsifiable: a clone-init that wrote the reading to a tracked path, or under a
    clone lacking the ADR-0005-T1 boundary, makes this red. BOTH halves are
    asserted — `git status --porcelain` does NOT list the file AND `git check-ignore`
    exits 0 — the porcelain half is not droppable.
    """
    clone = _make_scratch_clone(tmp_path)
    run(clone)

    store_root = clone / "vault/store"
    store.append("rhr", _reading(), root=store_root)
    new_file = store_root / "rhr.ndjson"
    assert new_file.exists()

    rel = new_file.relative_to(clone)
    porcelain = subprocess.run(
        ["git", "status", "--porcelain"], cwd=clone, capture_output=True, text=True, check=True
    ).stdout
    assert str(rel) not in porcelain, f"entered data appeared in git status: {porcelain!r}"

    check = subprocess.run(["git", "check-ignore", str(rel)], cwd=clone)
    assert check.returncode == 0, "entered store file is not gitignored"


def test_generate_dashboard_from_local_inputs_only_zero_cross_clone_reads(tmp_path, monkeypatch):
    """AC-3 / Gate B: dashboard renders from local inputs alone, 0 cross-clone reads.

    A sibling-clone store is planted OUTSIDE the clone root with operator data. The
    dashboard generation runs over the LOCAL (empty, initialized) store via
    render.emit, and the open-trace shows 0 opens of any path outside the clone root
    (in particular 0 opens under the sibling clone). Falsifiable: a generation that
    opened the sibling store, or any off-root path, makes this red.

    DEFERRED (recipe Deviation #2): the plan-generation-independence half of spec
    crit-3 — assemble.py (ADR-0006-T2) is Wave 5 and does not exist at Wave 4.
    """
    clone = _make_scratch_clone(tmp_path)
    run(clone)

    # A sibling clone OUTSIDE the clone root, carrying another operator's readings.
    sibling = tmp_path / "sibling-clone"
    sibling_store = sibling / "vault/store"
    sibling_store.mkdir(parents=True)
    # 98765 never collides with style-block tokens (the pill radius is 999px).
    store.append("rhr", _reading(value=98765, source="sibling"), root=sibling_store)

    store_root = clone / "vault/store"
    out_dir = clone / "vault/artifacts/generated"

    with _OpenTrace(monkeypatch) as trace:
        local_read = store.read("rhr", root=store_root)
        path = emit(dashboard, local_read, _out_dir=out_dir)

    assert path.exists(), "dashboard did not render from local inputs"
    html = path.read_text()
    assert "Health Dashboard" in html, "dashboard rendered from local inputs"
    assert "98765" not in html, "dashboard leaked the sibling clone's value"

    outside = trace.opens_outside(clone)
    assert outside == [], f"generation read paths outside the clone root: {outside}"


@DARWIN_ONLY
def test_run_zero_egress_and_zero_reads_outside_clone_root(tmp_path, monkeypatch):
    """AC-5 / Gate C: run() makes 0 outbound calls AND 0 reads outside the clone root.

    The egress guard over a run() closure is truthy (0 outbound, incl. subprocess),
    AND the open-trace over run() shows 0 opens outside the clone root.
    """
    clone = _make_scratch_clone(tmp_path)

    assert egress_run(lambda: run(clone)), "clean run() must be egress-clean (truthy)"

    clone2 = _make_scratch_clone(tmp_path / "second")
    with _OpenTrace(monkeypatch) as trace:
        run(clone2)
    outside = trace.opens_outside(clone2)
    assert outside == [], f"run() read paths outside the clone root: {outside}"


@DARWIN_ONLY
def test_injected_outbound_call_flips_egress_guard_to_fail(tmp_path, monkeypatch):
    """AC-5 SEC-03 failing-capable: an outbound call inside a run() path -> guard FAIL.

    Injects a synthetic outbound socket connect into a `run` code path (the
    scaffold-surfacing step) and asserts egress_guard.run returns falsy — proving
    the guard intercepts THIS new code path, not merely that a clean run makes 0
    calls. Requires network so the deny is attributed to the sandbox, not an
    offline host (mirrors the egress_guard suite's _require_network discipline).
    """
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3).close()
    except OSError:
        pytest.skip("no network — egress deny not exercisable")

    clone = _make_scratch_clone(tmp_path)

    real_surface = init_instance._surface_scaffolds

    def egressing_surface(clone_root):
        result = real_surface(clone_root)
        socket.create_connection(("1.1.1.1", 53), timeout=3)
        return result

    monkeypatch.setattr(init_instance, "_surface_scaffolds", egressing_surface)

    assert not egress_run(lambda: run(clone)), (
        "injected outbound call in a run() path must flip the guard to FAIL"
    )


def test_run_raises_when_clone_root_unresolvable(tmp_path):
    """run fails fast/visibly at the boundary when the clone root does not exist.

    Fail fast rather than silently reading an out-of-root fallback (recipe GREEN
    boundary note). A non-existent clone root raises.
    """
    with pytest.raises((FileNotFoundError, ValueError)):
        run(tmp_path / "does-not-exist")


# --------------------------------------------------------------------------- #
# Cycle 2 — operator-facing clone README (AC-4) — Non-Code Artifact
# --------------------------------------------------------------------------- #

CLONE_README = REPO_ROOT / "docs/clone-init.md"


def test_clone_readme_exists():
    """AC-4: docs/clone-init.md exists."""
    assert CLONE_README.exists(), "docs/clone-init.md is missing"


def test_clone_readme_has_clone_to_fillable_section():
    """AC-4: README has the 'From git clone to a fillable instance' section."""
    assert "## From git clone to a fillable instance" in CLONE_README.read_text()


def test_clone_readme_states_concrete_init_command():
    """AC-4: README gives the concrete init command that runs init_instance.run."""
    text = CLONE_README.read_text()
    assert "init_instance" in text and "run" in text, "no concrete init command"


def test_clone_readme_states_no_version_control_backup():
    """AC-4: README states entered data is excluded from version control.

    The no-VC-backup consequence (the operator keeps a separate local backup) —
    the accepted ADR-0005 trade-off the spec Risk Mitigations field names.
    """
    text = CLONE_README.read_text().lower()
    assert "version control" in text or "version-control" in text
    assert "backup" in text


# --- dv3: pre-push PII backstop install ------------------------------------------


def _seed_pre_push_src(clone):
    """Copy the live tracked pre-push hook source into the scratch clone."""
    src = clone / init_instance.PRE_PUSH_HOOK_SRC
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text((REPO_ROOT / init_instance.PRE_PUSH_HOOK_SRC).read_text())
    return src


def test_init_installs_pre_push_pii_backstop(tmp_path):
    """dv3: run() installs the tracked pre-push hook into .git/hooks, executable.

    Without the install, a clone's only PII gate is the agent-session PreToolUse
    hook — a human-terminal/IDE push path would be wholly ungated. Reds if run()
    drops the install step.
    """
    clone = _make_scratch_clone(tmp_path)
    _seed_pre_push_src(clone)
    run(clone)
    dest = clone / ".git" / "hooks" / "pre-push"
    assert dest.is_file()
    assert "pre-push-pii-scan.sh" in dest.read_text()
    assert os.access(dest, os.X_OK)


def test_init_does_not_clobber_foreign_pre_push_hook(tmp_path):
    """dv3: an operator's own pre-push hook (no sentinel) is preserved, not overwritten."""
    clone = _make_scratch_clone(tmp_path)
    _seed_pre_push_src(clone)
    foreign = clone / ".git" / "hooks" / "pre-push"
    foreign_body = "#!/bin/sh\n# operator-owned hook\nexit 0\n"
    foreign.write_text(foreign_body)
    run(clone)
    assert foreign.read_text() == foreign_body


def test_init_does_not_clobber_wrapper_that_calls_backstop_by_name(tmp_path):
    """dv3 (BUG-4): a wrapper hook that CALLS the backstop by name (but lacks the
    sentinel) is preserved — a substring-anywhere match would have clobbered it."""
    clone = _make_scratch_clone(tmp_path)
    _seed_pre_push_src(clone)
    dest = clone / ".git" / "hooks" / "pre-push"
    wrapper = "#!/bin/sh\n./my-lint.sh && exec .claude/hooks/pre-push-pii-scan.sh \"$@\"\n"
    dest.write_text(wrapper)
    run(clone)
    assert dest.read_text() == wrapper


def test_init_preserves_binary_pre_push_hook_without_crashing(tmp_path):
    """dv3 (BUG-3): a binary/non-UTF8 existing hook is preserved and run() does not raise."""
    clone = _make_scratch_clone(tmp_path)
    _seed_pre_push_src(clone)
    dest = clone / ".git" / "hooks" / "pre-push"
    dest.write_bytes(b"\x7fELF\x02\x01\x01\x00\xff\xfe\x00\x01binary-hook")
    pages = run(clone)  # must not raise UnicodeDecodeError
    assert dest.read_bytes().startswith(b"\x7fELF")
    assert pages


def test_init_refreshes_previously_installed_backstop(tmp_path):
    """dv3: a sentinel-carrying (ours) pre-push hook is refreshed on re-init."""
    clone = _make_scratch_clone(tmp_path)
    _seed_pre_push_src(clone)
    dest = clone / ".git" / "hooks" / "pre-push"
    dest.write_text("#!/bin/bash\n" + init_instance._PRE_PUSH_SENTINEL + "\n# stale prior install\n")
    run(clone)
    assert "fail-closed" in dest.read_text()  # current source body, not the stale stub


def test_init_replaces_symlink_dest_not_its_target(tmp_path):
    """dv3 (BUG-4 symlink): a sentinel-carrying symlink dest is REPLACED — its target
    is not written through."""
    clone = _make_scratch_clone(tmp_path)
    _seed_pre_push_src(clone)
    target = clone / "operator-script.sh"
    target.write_text("#!/bin/bash\n" + init_instance._PRE_PUSH_SENTINEL + "\noperator content\n")
    dest = clone / ".git" / "hooks" / "pre-push"
    dest.symlink_to(target)
    run(clone)
    assert dest.is_symlink() is False                # link replaced, not followed
    assert "operator content" in target.read_text()  # target intact


def test_init_preserves_dangling_symlink_pre_push(tmp_path):
    """dv3 (BUG-4 dangling-link edge): a broken symlink at pre-push is not written
    THROUGH to its missing target — it is preserved (not ours, cannot confirm)."""
    clone = _make_scratch_clone(tmp_path)
    _seed_pre_push_src(clone)
    dest = clone / ".git" / "hooks" / "pre-push"
    dest.symlink_to(clone / "nonexistent-target.sh")
    pages = run(clone)  # must not raise, must not create the target
    assert dest.is_symlink() is True
    assert (clone / "nonexistent-target.sh").exists() is False
    assert pages


def test_init_without_hook_source_still_runs(tmp_path):
    """dv3: a clone missing the tracked hook source initializes normally (skip, not raise)."""
    clone = _make_scratch_clone(tmp_path)
    pages = run(clone)
    assert (clone / ".git" / "hooks" / "pre-push").exists() is False
    assert pages  # the scaffold surface still works
