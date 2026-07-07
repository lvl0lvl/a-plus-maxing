"""The NAMED anti-implicit-activation guard (ADR-0039-T3, Cycle 2; QA-F2 / SEC-01).

The runner is disabled by default and ONLY the operator arms it. This guard preserves that premise:
no build / provision / `init_instance` step may load a runner entry. It has three arms:

  - Grep arm: the provisioning surface (`scripts/clone/init_instance.py` + any setup/build script)
    names no scheduler-install token and no `activate.enable` call — in BOTH the dotted
    `activate.enable(...)` form AND the `from ...schedule.activate import enable; enable()`
    import-and-call form (a dotted-only substring grep MISSES the second form).
  - Behavioral arm: `init_instance.run(clone_root=<scratch>)` installs 0 runner entries — a before/after
    COUNT DELTA on the DEFAULT `activate.RUNNER_LABEL` (the label init_instance WOULD arm under a real
    implicit activation) is 0 across `run()`. Polling a per-run RANDOM label instead would stay green
    even under a real implicit `enable()` on the default label (tautological — the TEST-001 fix). The
    delta is isolation-safe even if a real armed runner exists on the dev machine (before == after).
  - EXECUTED mutation-RED: injecting a REALISTIC `activate.enable()` on the DEFAULT `RUNNER_LABEL` — in
    BOTH call-forms — into a SCRATCH provision path, forced down the LAUNCHD (file) branch, raises the
    REAL ~/Library/LaunchAgents install-file DELTA on that default label above 0 and reddens the guard;
    then the default label is disabled + the installed agent file unlinked in a bulletproof teardown (a
    leaked DEFAULT-label armed agent is worse than a random-label one). A guard that stays green under
    this injection — or that reddens only via a fixture-HOME counter — is tautological. This proves (i)
    the counter reads REAL launchd state on the label init_instance would touch and (ii) the grep matches
    the import-and-call form, not only the dotted literal.

`scripts/clone/init_instance.py` is NEVER edited — the guard SCANS it; the mutation injects into a
SCRATCH copy only. The real-state arms use the REAL ~/Library/LaunchAgents (a reliable, non-hanging
home-dir read/write — never a fixture HOME, never the crontab-TCC-hanging path); an OS-capability
probe loud-skips (never a vacuity skip) only if the home dir is unwritable, and the mutation arm
additionally loud-skips if the operator's DEFAULT-label runner is already armed (it needs a disarmed
default-label baseline and must not disturb a real armed runner).
"""

import importlib.util
import textwrap
from pathlib import Path

import pytest

from scripts.clone import init_instance
from scripts.runner.schedule import activate

# The real-state test-hygiene helpers (one home, in the Cycle-1 file): the forced-launchd unique-label
# context manager with a bullet-proof disable()+file-unlink teardown, the writability probe, and the
# direct real-install read.
from tests.runner.test_activation_surface import (
    _installed_for,
    _require_launchagents_writable_or_skip,
    real_state_label,
)

# tests/runner/test_no_implicit_activation.py -> tests -> <repo root>.
REPO_ROOT = Path(__file__).resolve().parents[2]
INIT_INSTANCE_PATH = REPO_ROOT / "scripts" / "clone" / "init_instance.py"

# The provisioning surfaces the guard scans — defined ONCE (one home). A future provisioning/setup
# script is added here in one place.
_PROVISIONING_SURFACES = [INIT_INSTANCE_PATH]


def _provisioning_is_clean(paths, label):
    """The guard verdict: clean iff the scan finds 0 activation hits AND 0 real entries are armed.

    Combines the grep arm (`activate._scan_provisioning_for_activation`) with the behavioral arm
    (`activate.active_entry_count`, the SAME real-state counter `status()` uses). Goes False (guard
    RED) when a provisioning path either NAMES an activation call or has actually armed an entry.
    """
    grep_hits = activate._scan_provisioning_for_activation(paths)
    return not grep_hits and activate.active_entry_count(label) == 0


def test_grep_arm_init_instance_is_clean():
    # AC-8 (grep arm): the real tracked init_instance.py names 0 scheduler-install tokens and 0
    # activate.enable call in EITHER form -> 0 hits. Failing-capable: the mutation-RED test proves the
    # scanner hits when a call is actually present (both forms), so this 0-hit result is non-vacuous.
    hits = activate._scan_provisioning_for_activation(_PROVISIONING_SURFACES)
    assert hits == [], f"the provisioning surface names a runner-activation call/token: {hits}"


def test_behavioral_arm_init_instance_arms_nothing(tmp_path):
    # AC-8 (behavioral arm): init_instance.run(clone_root=<scratch>) installs 0 runner entries. The
    # counter polls the DEFAULT activate.RUNNER_LABEL — the label init_instance WOULD arm under a real
    # implicit enable() — as a before/after COUNT DELTA. Polling a per-run RANDOM label instead (the
    # pre-fix arm) would stay green even under a real implicit enable() on the default label, since the
    # default-label counter was never read (tautological — TEST-001). The delta is isolation-safe even
    # if a real armed runner exists on the dev machine (before == after regardless of the baseline).
    # real_state_label() forces the launchd branch + restores it; its random label is unused here — the
    # DEFAULT label is what we poll, and init_instance arms nothing so no default-label file is created.
    with real_state_label():
        before = activate.active_entry_count(activate.RUNNER_LABEL)
        init_instance.run(clone_root=tmp_path)
        after = activate.active_entry_count(activate.RUNNER_LABEL)
        assert after == before, (
            "init_instance.run changed the DEFAULT-label runner count (implicit activation on the "
            "provisioning path)"
        )
        # the guard rests GREEN over the real provisioning surface (the isolation-safe grep arm).
        assert activate._scan_provisioning_for_activation(_PROVISIONING_SURFACES) == []


def test_mutation_red_guard_catches_injected_activation(tmp_path):
    # AC-8 (EXECUTED mutation-RED — the BLOCKING QA MUST-FIX; mirrors T4 AC-7(d)): inject a REALISTIC
    # activate.enable() on the DEFAULT activate.RUNNER_LABEL — the label init_instance WOULD arm under a
    # real implicit activation (TEST-001) — in BOTH the dotted and the bare import-and-call forms into a
    # SCRATCH provision path, force it down the LAUNCHD (file) branch, and EXECUTE it — confirming (a)
    # the grep arm matches BOTH forms, (b) the behavioral counter catches the arming via a >0 DELTA on
    # the SAME default label the behavioral arm polls, read FROM the real ~/Library/LaunchAgents install
    # file (NOT a fixture-HOME), and (c) the guard rests RED. Then the default label is disabled + the
    # installed agent file unlinked in a bulletproof finally (a crash between the injected enable() and
    # teardown must not leave a REAL armed DEFAULT-label agent — worse than a random-label one).
    #
    # OS-CAPABILITY / OS-STATE SKIP vs VACUITY SKIP: a fast writability probe loud-skips only when the OS
    # denies the home-dir write, and an armed-default-label probe loud-skips only when the operator
    # already has the DEFAULT-label runner armed (the delta needs a disarmed baseline and must not
    # disturb a real armed runner). Neither is a clean pass; in a capable, disarmed env this RUNS the
    # real mutation-RED (real install-file delta >0, guard RED). It NEVER hangs (no crontab-TCC write).
    _require_launchagents_writable_or_skip()
    label = activate.RUNNER_LABEL
    if activate._installed_plist_path(label).exists():
        pytest.skip(
            "the operator has the DEFAULT-label runner armed; the mutation-RED needs a disarmed "
            "default-label baseline and must not disturb a real armed runner (OS-state skip)"
        )
    saved_probe = activate._launchd_available
    activate._launchd_available = lambda: True
    try:
        before = activate.active_entry_count(label)
        assert before == 0, "the DEFAULT-label runner was armed at mutation-RED entry (baseline not disarmed)"

        # baseline: the guard is GREEN over the REAL tracked init_instance.py (the isolation-safe grep arm).
        assert activate._scan_provisioning_for_activation(_PROVISIONING_SURFACES) == [], (
            "the guard was not green over the real provisioning surface at baseline"
        )

        # a SCRATCH provision path that (wrongly) arms the runner on the DEFAULT label, in BOTH call-forms.
        scratch = tmp_path / "provision_mutated.py"
        scratch.write_text(textwrap.dedent("""\
            \"\"\"SCRATCH provisioning path that WRONGLY arms the runner (AC-8 mutation injection).\"\"\"
            import scripts.runner.schedule.activate as activate
            from scripts.runner.schedule.activate import enable

            def run():
                activate.enable()   # dotted activate.enable(...) form, DEFAULT RUNNER_LABEL
                enable()            # bare `from ...import enable; enable()` form, DEFAULT label
        """), encoding="utf-8")

        # (a) grep arm matches BOTH forms.
        hits = activate._scan_provisioning_for_activation([scratch])
        dotted = [h for h in hits if "activate.enable(" in h[2]]
        bare = [h for h in hits if h[2].strip().startswith("enable(")]
        assert dotted, f"the grep arm missed the dotted activate.enable(...) form: {hits}"
        assert bare, f"the grep arm missed the bare `from ...import enable; enable()` form: {hits}"

        # (b) EXECUTE the injected enable() -> a REAL ~/Library/LaunchAgents install file (launchd forced).
        spec = importlib.util.spec_from_file_location("aplus_scratch_provision_mutated", scratch)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.run()

        # the behavioral counter catches the arming via a >0 DELTA on the DEFAULT label, read FROM the
        # real install file (the scratch-HOME tautology killer) — the SAME label the behavioral arm polls.
        after = activate.active_entry_count(label)
        assert after > before, (
            "the injected enable() did not raise the DEFAULT-label real-state count (delta not caught)"
        )
        assert _installed_for(label), "the injected entry is not in the REAL ~/Library/LaunchAgents (fixture-HOME read?)"

        # (c) the guard rests RED over the mutated scratch path.
        assert not _provisioning_is_clean([scratch], label), (
            "the guard stayed GREEN under an injected activate.enable() — it is tautological (QA-F2)"
        )
    finally:
        # bulletproof teardown: disable() the DEFAULT label, then unlink both artifacts (each step
        # independent so a failing disable() never skips the RELIABLE filesystem unlink), then restore
        # the launchd probe. A leaked DEFAULT-label armed agent is worse than a random-label one.
        try:
            activate.disable(label)
        except Exception:
            pass
        for artifact in (activate._installed_plist_path(label), activate._rendered_plist_path(label)):
            try:
                if artifact.exists():
                    artifact.unlink()
            except OSError:
                pass
        activate._launchd_available = saved_probe

    # after teardown, NO real armed agent for the DEFAULT label survives.
    assert not _installed_for(label), "a REAL armed launchd agent survived teardown (implicit activation)"
