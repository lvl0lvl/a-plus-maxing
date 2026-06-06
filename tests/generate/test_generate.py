"""Tests for the on-demand + unattended (cron) generation entry point (ADR-0004-T3).

`generate.run(artifact_name)` is a THIN entry point over the ADR-0004-T1
`render.emit`. It assembles the cross-item store read model, selects a template
by name, and drives ONE `render.emit` invocation that writes the self-contained
artifact, returning the path. The same code path serves both the interactive
(on-demand) invocation and the unattended/cron invocation — there is no daemon
and no served surface.

The load-bearing gates here are falsifiable by construction:
- AC-3 (NG-4): a listen-counter is measured over the REAL `generate.run` call
  (asserted == 0) AND over a deliberate bind+listen probe (asserted > 0), so the
  observer is proven to discriminate 0-from-nonzero (no blind-observer pass).
- AC-5: `render.emit` is SPIED (wrapping the real one); both entry modes must
  drive exactly ONE shared emit invocation per run. Structural identity of the
  two modes' artifacts is a CORROBORATING secondary check only.
"""

import socket
import subprocess
import sys
import unittest.mock
from pathlib import Path

import pytest

from scripts.generate import generate, render
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]


def _seed_store(root):
    """Seed a tmp store root with two items via the published store.append writer.

    Two items, so the cross-item read model assembled by `generate.run` spans more
    than one `.ndjson` file — exercising the enumeration helper over a real layout.
    """
    readings = [
        {"item": "rhr", "timepoint": "2026-05-01T00:00:00+00:00", "source": "whoop", "value": 52},
        {"item": "rhr", "timepoint": "2026-05-02T00:00:00+00:00", "source": "whoop", "value": 49},
        {"item": "hrv", "timepoint": "2026-05-01T00:00:00+00:00", "source": "whoop", "value": 71},
        {"item": "hrv", "timepoint": "2026-05-02T00:00:00+00:00", "source": "whoop", "value": 88},
    ]
    for reading in readings:
        store.append(reading["item"], reading, root=root)


# --------------------------------------------------------------------------- #
# Cycle 1 — entry point: on-demand write+exit (AC-1), unattended stdin-closed
# (AC-2), NG-4 0-listening-socket (AC-3), single render path (AC-5)
# --------------------------------------------------------------------------- #


def test_run_writes_file_and_returns_existing_path(tmp_path):
    """AC-1: run('dashboard') returns a Path that EXISTS on disk after the call."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    path = generate.run("dashboard", _root=root, _out_dir=out)

    assert isinstance(path, Path)
    assert path.exists()
    assert path.is_file()


def test_main_exits_zero(tmp_path, capsys):
    """AC-1: main(['dashboard']) returns exit code 0 and prints the produced path."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    code = generate.main(["dashboard", "--root", str(root), "--out-dir", str(out)])

    assert code == 0
    printed = capsys.readouterr().out.strip()
    assert printed
    assert Path(printed).exists()


def test_unknown_artifact_name_raises(tmp_path):
    """AC-1 boundary: an unknown artifact_name fails fast (no silent empty file)."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    with pytest.raises(Exception):
        generate.run("not-a-real-template", _root=root, _out_dir=out)


def test_run_never_prompts_for_input(tmp_path):
    """AC-2: run never reads operator input — builtins.input is called 0 times."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    def forbidden_input(*a, **k):
        raise AssertionError("generate.run must never prompt for operator input")

    with unittest.mock.patch("builtins.input", forbidden_input):
        path = generate.run("dashboard", _root=root, _out_dir=out)
    assert path.exists()


def test_unattended_stdin_closed_exits_zero(tmp_path):
    """AC-2: an unattended run with stdin CLOSED completes and exits 0 (never blocks).

    Drives the real cron-/operator-invocable surface as a subprocess
    (`python -m scripts.generate.generate`) with stdin redirected from /dev/null,
    so a run that blocked on stdin would hang (caught by the timeout) and a run
    that prompted would fail. Points the subprocess at a seeded tmp store via
    --root/--out-dir so it never touches the real gitignored store/artifacts dir.
    """
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    proc = subprocess.run(
        [sys.executable, "-m", "scripts.generate.generate",
         "dashboard", "--root", str(root), "--out-dir", str(out)],
        cwd=str(REPO_ROOT),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
    printed = proc.stdout.strip().splitlines()[-1]
    assert Path(printed).exists()


def _count_listens(observed):
    """Run `observed` (zero-arg) while counting socket bind-to-listen calls in it.

    Monkeypatches socket.socket.listen and .bind to increment a shared counter for
    the duration of the observed call, then restores. Returns the count of
    bind/listen operations attributable to the call. The same mechanism is run
    over both the real `generate.run` (expect 0) and a deliberate bind+listen
    probe (expect > 0), so the observer is proven to discriminate.

    Returns:
        (int) The number of bind/listen operations observed during the call.
    """
    counter = {"n": 0}
    real_listen = socket.socket.listen
    real_bind = socket.socket.bind

    def counting_listen(self, *a, **k):
        counter["n"] += 1
        return real_listen(self, *a, **k)

    def counting_bind(self, *a, **k):
        counter["n"] += 1
        return real_bind(self, *a, **k)

    with unittest.mock.patch.object(socket.socket, "listen", counting_listen), \
            unittest.mock.patch.object(socket.socket, "bind", counting_bind):
        observed()
    return counter["n"]


def test_run_binds_zero_listening_sockets(tmp_path):
    """AC-3 (NG-4): 0 sockets bound-to-listen across the real generate.run call.

    POSITIVE CONTROL: the SAME observation mechanism over a deliberate bind+listen
    probe must report NON-ZERO, proving the observer discriminates 0-from-nonzero.
    The gate fails if the positive control is not non-zero (a blind/mis-wired
    observer would report 0 for both and pass vacuously).
    """
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    def run_generate():
        generate.run("dashboard", _root=root, _out_dir=out)

    def bind_and_listen_probe():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", 0))
            s.listen(1)
        finally:
            s.close()

    # Positive control first: the observer must SEE a bind+listen.
    control_count = _count_listens(bind_and_listen_probe)
    assert control_count > 0, (
        "positive control observed 0 bind/listen — the observer is blind, so the "
        "== 0 assertion below would be a vacuous pass"
    )

    # The real generate.run path must bind 0 listening sockets (no server/daemon).
    run_count = _count_listens(run_generate)
    assert run_count == 0, f"generate.run bound {run_count} sockets to listen (NG-4 breach)"


def test_both_modes_drive_one_shared_render_emit(tmp_path):
    """AC-5: on-demand + cron both drive exactly ONE shared render.emit per run.

    SPY on render.emit (wrapping the real one) so it still produces the file while
    counting calls. Each mode must produce exactly one emit invocation; both modes
    route through the SAME render.emit. The emit-spy is the load-bearing proof —
    structural identity of the two artifacts is asserted only as a CORROBORATING
    secondary check (two independent render paths could coincidentally match).
    """
    root = tmp_path / "store"
    _seed_store(root)

    # On-demand mode: a direct generate.run call.
    with unittest.mock.patch("scripts.generate.render.emit", wraps=render.emit) as spy_ondemand:
        on_demand = generate.run("dashboard", _root=root, _out_dir=tmp_path / "on-demand")
    assert spy_ondemand.call_count == 1, (
        f"on-demand drove {spy_ondemand.call_count} render.emit calls, expected 1"
    )

    # Cron mode: the same entry invoked through main() (the cron-invocable surface).
    with unittest.mock.patch("scripts.generate.render.emit", wraps=render.emit) as spy_cron:
        code = generate.main(
            ["dashboard", "--root", str(root), "--out-dir", str(tmp_path / "cron")]
        )
    assert code == 0
    assert spy_cron.call_count == 1, (
        f"cron drove {spy_cron.call_count} render.emit calls, expected 1"
    )

    # Both spies wrapped the SAME render.emit object (one render path, not two).
    assert spy_ondemand._mock_wraps is spy_cron._mock_wraps is render.emit

    # CORROBORATING secondary check only: same store state -> structurally identical
    # artifacts (both modes produced the dashboard from the same seeded store).
    cron_path = tmp_path / "cron" / on_demand.name
    assert on_demand.read_text() == cron_path.read_text()


# --------------------------------------------------------------------------- #
# Cycle 2 — the produced file opens offline with 0 outbound (AC-4)
# --------------------------------------------------------------------------- #

import re  # noqa: E402

# A src=/href=/url() target that resolves off the file is anything that is neither
# a same-document #fragment nor an inline data: URI.
_REF_RE = re.compile(
    r"""(?:src|href)\s*=\s*['"]([^'"]*)['"]|url\(\s*['"]?([^'")]*)['"]?\s*\)""", re.I
)


def _asset_refs(html):
    """Return every src/href/url() target in the file, keeping inline data: URIs.

    Drops same-document #fragment hrefs (no asset). data: URIs are kept so the
    offline-open walk has a real asset to resolve in-process.
    """
    out = []
    for m in _REF_RE.finditer(html):
        target = (m.group(1) or m.group(2) or "").strip()
        if not target or target.startswith("#"):
            continue
        out.append(target)
    return out


@pytest.mark.parametrize("artifact_name", ["dashboard", "report"])
def test_produced_file_opens_offline_zero_outbound(tmp_path, artifact_name):
    """AC-4: opening the PRODUCED file under the egress guard observes 0 outbound.

    Renders the artifact via generate.run, then opens the file generate.run
    actually produced (via the returned path) under the OS egress guard, walking
    and resolving EVERY asset reference. The self-contained ADR-0004-T1 artifact
    carries only inline assets, so the captured outbound count stays 0 — asserted
    over the real produced file, not "the file opens".
    """
    import urllib.request

    from scripts.guard.egress_guard import run as egress_run

    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    produced = generate.run(artifact_name, _root=root, _out_dir=out)
    assert produced.exists()

    def open_and_walk_assets():
        html = produced.read_text()
        for target in _asset_refs(html):
            # A data: URI resolves in-process; an off-host URL would attempt a
            # socket connect here, which the OS egress guard would surface as a fail.
            with urllib.request.urlopen(target) as resp:
                resp.read()

    assert egress_run(open_and_walk_assets), (
        f"opening the produced {artifact_name} file observed outbound network"
    )
