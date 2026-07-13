"""Tests for the on-demand + unattended (cron) generation entry point (ADR-0004-T3).

`generate.run(artifact_name)` is a THIN entry point over the ADR-0004-T1
`render.emit`. It assembles the cross-item store read model, selects a template
by name, and drives ONE `render.emit` invocation that writes the self-contained
artifact, returning the path. The same code path serves both the interactive
(on-demand) invocation and the unattended/cron invocation — there is no daemon
and no served surface.

The load-bearing gates here are falsifiable by construction:
- AC-3 (NG-4): listening sockets are counted ACROSS the process tree of the REAL
  cron surface (`python -m scripts.generate.generate` driven as a subprocess under
  a listen-recording sitecustomize shim), asserted == 0. Positive controls run the
  SAME mechanism over a subprocess that listens, a subprocess whose os.fork() child
  listens, and a subprocess that spawns a fresh interpreter that listens — each
  asserted > 0 — so the observer is proven to discriminate 0-from-nonzero for every
  child-process breach shape (not just same-interpreter). A negative control asserts 0.
- AC-5: `render.emit` is SPIED (wrapping the real one); both entry modes must
  drive exactly ONE shared emit invocation per run. Structural identity of the
  two modes' artifacts is a CORROBORATING secondary check only.
"""

import datetime
import os
import re
import subprocess
import sys
import unittest.mock
from pathlib import Path

import pytest

from scripts.generate import generate, render
from scripts.store import plan_model, store
from vault.design.templates import dashboard, report

# The canonical periodized comprehensive version (PF-S131-01) — imported, not
# re-authored, so this regression pins the exact shipped plan-model:: shape.
from tests.store.test_plan_model import _comprehensive_version

REPO_ROOT = Path(__file__).resolve().parents[2]


def _seed_store(root):
    """Seed a tmp store root with two items via the published store.append writer.

    Two items, so the cross-item read model assembled by `generate.run` spans more
    than one `.ndjson` file — exercising `store.read_all` over a real layout.
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
    """AC-1 boundary: an unknown artifact_name fails fast with the documented KeyError."""
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    with pytest.raises(KeyError, match="unknown artifact"):
        generate.run("not-a-real-template", _root=root, _out_dir=out)


def test_main_unknown_artifact_exits_2(tmp_path):
    """AC-1 boundary: the cron surface rejects an unknown artifact via argparse exit 2.

    `main` resolves artifact_name through argparse `choices=`, which rejects an
    unknown name with SystemExit(2) BEFORE `run`'s KeyError — the operator/cron
    rejection path, distinct from `run`'s documented KeyError (covered above).
    """
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    with pytest.raises(SystemExit) as exc:
        generate.main(["not-a-real-template", "--root", str(root), "--out-dir", str(out)])
    assert exc.value.code == 2


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


# A sitecustomize shim that wraps socket.socket.LISTEN (the listening-socket
# operation — a bind-only UDP socket is NOT a listening socket, so bind is NOT
# counted: F2 counter semantics) to append the calling pid to $LISTEN_LOG. Because
# it is a sitecustomize on PYTHONPATH, the interpreter auto-imports it at startup
# in the observed process AND in any FRESH-INTERPRETER subprocess it spawns (which
# inherits PYTHONPATH); os.fork() children inherit the already-patched class. So a
# listen anywhere in the process tree — same interpreter, fork child, or spawned
# new interpreter — is recorded, spanning the process boundary the previous
# parent-only class patch could not (F1).
_LISTEN_SHIM = (
    "import os, socket\n"
    "_log = os.environ.get('LISTEN_LOG')\n"
    "if _log:\n"
    "    _real = socket.socket.listen\n"
    "    def _counting(self, *a, **k):\n"
    "        with open(_log, 'a') as fh:\n"
    "            fh.write(str(os.getpid()) + '\\n')\n"
    "        return _real(self, *a, **k)\n"
    "    socket.socket.listen = _counting\n"
)


def _count_listens_across_processes(tmp_path, argv_tail):
    """Run `python <argv_tail>` as a subprocess and count listens anywhere in its tree.

    Installs the `_LISTEN_SHIM` sitecustomize on PYTHONPATH and points LISTEN_LOG at
    a fresh log file, then runs the interpreter with `argv_tail` (a `-m`/`-c`
    invocation). The shim records every `socket.socket.listen` in the observed
    process, in any os.fork() child (inherited patched class), and in any spawned
    fresh interpreter (which re-imports the sitecustomize via inherited PYTHONPATH).

    Args:
        tmp_path (Path): A unique tmp dir for this observation's shim + log.
        argv_tail (list): The interpreter argument tail after `sys.executable`
            (e.g. `["-m", "scripts.generate.generate", ...]` or `["-c", "..."]`).

    Returns:
        (int) The number of `socket.socket.listen` calls recorded across the tree.
    """
    obs_dir = tmp_path / f"obs-{abs(hash(tuple(argv_tail)))}"
    obs_dir.mkdir()
    (obs_dir / "sitecustomize.py").write_text(_LISTEN_SHIM)
    log = obs_dir / "listens.log"

    env = dict(os.environ)
    env["PYTHONPATH"] = str(obs_dir) + os.pathsep + env.get("PYTHONPATH", "")
    env["LISTEN_LOG"] = str(log)

    proc = subprocess.run(
        [sys.executable, *argv_tail],
        cwd=str(REPO_ROOT),
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"observed subprocess failed: stderr={proc.stderr!r}"
    return len(log.read_text().splitlines()) if log.exists() else 0


def test_run_binds_zero_listening_sockets(tmp_path):
    """AC-3 (NG-4): 0 listening sockets opened anywhere in the real generate.run tree.

    Drives the REAL cron surface `python -m scripts.generate.generate` as a
    subprocess under a listen-recording sitecustomize shim and asserts 0 listening
    sockets were opened anywhere in its process tree (no server/daemon).

    POSITIVE CONTROLS (close the blind-observer tautology ACROSS the process
    boundary — the prior same-interpreter control could not): the SAME mechanism
    over (a) a subprocess that itself listens, (b) a subprocess whose os.fork()
    CHILD listens, and (c) a subprocess that spawns a FRESH INTERPRETER that
    listens must each report NON-ZERO — proving the observer discriminates
    0-from-nonzero for every child-process shape the NG-4 breach could take. A
    NEGATIVE control (a subprocess that opens no listening socket) must report 0,
    so the observer is not stuck-on.
    """
    root = tmp_path / "store"
    out = tmp_path / "out"
    _seed_store(root)

    listen_body = (
        "import socket\n"
        "s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
        "s.bind(('127.0.0.1',0)); s.listen(1); s.close()\n"
    )
    fork_child_listen = (
        "import os, socket\n"
        "pid=os.fork()\n"
        "if pid==0:\n"
        "    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
        "    s.bind(('127.0.0.1',0)); s.listen(1); s.close()\n"
        "    os._exit(0)\n"
        "os.waitpid(pid,0)\n"
    )
    spawned_interp_listen = (
        "import subprocess, sys\n"
        f"subprocess.run([sys.executable,'-c',{listen_body!r}], check=True)\n"
    )

    # Positive control (a): the observed subprocess itself opens a listening socket.
    same = _count_listens_across_processes(tmp_path, ["-c", listen_body])
    assert same > 0, "positive control (same-interpreter listen) observed 0 — blind observer"

    # Positive control (b): an os.fork() CHILD of the observed subprocess listens.
    forked = _count_listens_across_processes(tmp_path, ["-c", fork_child_listen])
    assert forked > 0, "positive control (os.fork child listen) observed 0 — blind across fork"

    # Positive control (c): a FRESH-INTERPRETER subprocess grandchild listens.
    spawned = _count_listens_across_processes(tmp_path, ["-c", spawned_interp_listen])
    assert spawned > 0, "positive control (fresh-interpreter listen) observed 0 — blind across spawn"

    # Negative control: a subprocess that opens no listening socket reports 0.
    none = _count_listens_across_processes(tmp_path, ["-c", "x=1\n"])
    assert none == 0, f"negative control reported {none} — observer is stuck-on, not discriminating"

    # The REAL generate.run cron surface must open 0 listening sockets in its tree.
    run_count = _count_listens_across_processes(
        tmp_path,
        ["-m", "scripts.generate.generate", "dashboard",
         "--root", str(root), "--out-dir", str(out)],
    )
    assert run_count == 0, f"generate.run opened {run_count} listening sockets (NG-4 breach)"


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

    # Both modes route through the ONE module path "scripts.generate.render.emit"
    # — patched here with wraps=render.emit — so a single render path is guaranteed
    # by construction (the patch target is the only emit symbol generate.run resolves).
    assert spy_ondemand.call_count == spy_cron.call_count == 1

    # CORROBORATING secondary check only: same store state -> structurally identical
    # artifacts (both modes produced the dashboard from the same seeded store).
    cron_path = tmp_path / "cron" / on_demand.name
    assert on_demand.read_text() == cron_path.read_text()


# --------------------------------------------------------------------------- #
# Cycle 2 — the produced file opens offline with 0 outbound (AC-4)
# --------------------------------------------------------------------------- #

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


def test_offline_open_walk_detects_off_host_ref(tmp_path):
    """AC-4 POSITIVE CONTROL: the SAME walk over an OFF-HOST ref is observed FALSY.

    The real dashboard/report carry ZERO off-host asset refs, so the urlopen walk
    in the AC-4 test never attempts an outbound connect — `egress_run` would return
    truthy over a no-op closure even if the guard were blind. This control runs the
    identical open_and_walk_assets mechanism over a synthetic file carrying one
    off-host ref and asserts `egress_run` returns FALSY, proving the walk+guard
    actually detect outbound before the AC-4 test asserts truthy for the real file.
    """
    import urllib.request

    from scripts.guard.egress_guard import run as egress_run

    # An off-host ref (closed local port) that resolves OFF the file: the walk must
    # attempt a socket connect, which the egress guard surfaces as a fail.
    synthetic = tmp_path / "off-host.html"
    synthetic.write_text("<img src='http://127.0.0.1:9/x'>")

    def open_and_walk_assets():
        html = synthetic.read_text()
        refs = _asset_refs(html)
        assert refs, "control fixture must carry an off-host ref for a meaningful walk"
        for target in refs:
            with urllib.request.urlopen(target) as resp:
                resp.read()

    assert not egress_run(open_and_walk_assets), (
        "walking an off-host ref returned truthy — the walk/guard is blind, so the "
        "AC-4 truthy assertion over the real file would be a vacuous pass"
    )


def test_empty_store_succeeds_and_writes_file(tmp_path):
    """An empty/nonexistent store yields an empty-data artifact, not a crash.

    `generate.run` over a store root with no `.ndjson` files assembles an empty
    read model and still drives one render.emit, writing a file. Pins the
    empty-store contract (zero readings -> empty-data artifact, run succeeds).
    """
    empty_root = tmp_path / "nonexistent-store"  # never created -> no item files
    out = tmp_path / "out"

    path = generate.run("dashboard", _root=empty_root, _out_dir=out)

    assert path.exists()
    assert path.is_file()


# --------------------------------------------------------------------------- #
# Regression (Wave-4 Tier-2): the comprehensive `plan-model::` stream must route
# through EVERY renderer without raising. 0043-T3 Leg-2 made `plan-model::` a live
# store stream; report.py:702 gained the skip but dashboard.py missed it, so any
# store holding a comprehensive plan crashed the dashboard render with the
# 'unrouted stream prefix' KeyError. The report co-edit was unguarded — this test
# guards BOTH surfaces so neither skip can be silently removed.
# --------------------------------------------------------------------------- #


def test_plan_model_stream_does_not_crash_renderers(tmp_path):
    """A store holding a comprehensive plan-model:: version renders on every surface.

    RED capability: reverting the dashboard.py plan-model:: skip re-raises the
    'unrouted stream prefix' KeyError on the dashboard entry point AND render fn;
    removing the report.py:702 skip re-raises it on the report entry point AND
    render fn. Either regression fails this test.
    """
    root = tmp_path / "store"
    out = tmp_path / "out"
    on_date = "2026-07-13"
    plan_model.record_plan_version(_comprehensive_version(date=on_date), root)
    today = datetime.date.fromisoformat(on_date)
    store_read = store.read_all(root)

    # Both entry points route plan-model:: without raising and write an artifact.
    for artifact in ("dashboard", "report"):
        path = generate.run(artifact, _root=root, _out_dir=out, _today=today)
        assert path.exists() and path.is_file()

    # The render fns route plan-model:: directly (not only via generate.run).
    assert dashboard.render(store_read, _today=today, _root=root)
    assert report.render(store_read, _today=today, _root=root)
