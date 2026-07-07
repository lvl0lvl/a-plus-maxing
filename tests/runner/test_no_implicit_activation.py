"""The NAMED anti-implicit-activation guard (ADR-0039-T3, Cycle 2; QA-F2 / SEC-01).

The runner is disabled by default and ONLY the operator arms it. This guard preserves that premise:
no build / provision / `init_instance` step may load a runner entry. It has three arms:

  - Grep arm: the provisioning surface (`scripts/clone/init_instance.py` + any setup/build script)
    names no scheduler-install token and no `activate.enable` call — in BOTH the dotted
    `activate.enable(...)` form AND the `from ...schedule.activate import enable; enable()`
    import-and-call form (a dotted-only substring grep MISSES the second form).
  - Behavioral arm: `init_instance.run(clone_root=<scratch>)` installs 0 runner entries — the
    active-entry counter (REUSED from `activate.status()`'s REAL-state counter) reads 0 after `run()`.
  - EXECUTED mutation-RED: injecting a REALISTIC `activate.enable()` — in BOTH call-forms — into a
    SCRATCH provision path, forced down the LAUNCHD (file) branch, drives the REAL
    ~/Library/LaunchAgents install-file counter to >=1 and reddens the guard; then it is reverted +
    the installed agent file unlinked in an unconditional teardown. A guard that stays green under this
    injection — or that reddens only via a fixture-HOME counter — is tautological. This proves (i) the
    counter reads REAL launchd state and (ii) the grep matches the import-and-call form, not only the
    dotted literal.

`scripts/clone/init_instance.py` is NEVER edited — the guard SCANS it; the mutation injects into a
SCRATCH copy only. The real-state arms use the REAL ~/Library/LaunchAgents (a reliable, non-hanging
home-dir read/write — never a fixture HOME, never the crontab-TCC-hanging path); an OS-capability
probe loud-skips (never a vacuity skip) only if the home dir is unwritable.
"""

import importlib.util
import textwrap
from pathlib import Path

from scripts.clone import init_instance
from scripts.runner.schedule import activate

# The real-state test-hygiene helpers (one home, in the Cycle-1 file): the forced-launchd unique-label
# context manager with a bullet-proof disable()+file-unlink teardown, and the direct real-install read.
from tests.runner.test_activation_surface import _installed_for, real_state_label

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
    # AC-8 (behavioral arm): init_instance.run(clone_root=<scratch>) installs 0 runner entries — the
    # active-entry counter (the SAME real-state counter AC-1/AC-3 exercised) reads 0 for a fresh label
    # after run(). Forced launchd + unconditional teardown; the real init_instance.py is NEVER edited.
    with real_state_label() as label:
        assert activate.active_entry_count(label) == 0
        init_instance.run(clone_root=tmp_path)
        assert activate.active_entry_count(label) == 0, (
            "init_instance.run armed a runner entry (implicit activation on the provisioning path)"
        )
        # the guard rests GREEN over the real provisioning surface.
        assert _provisioning_is_clean(_PROVISIONING_SURFACES, label)


def test_mutation_red_guard_catches_injected_activation(tmp_path):
    # AC-8 (EXECUTED mutation-RED — the BLOCKING QA MUST-FIX; mirrors T4 AC-7(d)): inject a REALISTIC
    # activate.enable() in BOTH the dotted and the bare import-and-call forms into a SCRATCH provision
    # path, force it down the LAUNCHD (file) branch (real_state_label monkeypatches the launchd probe
    # True), and EXECUTE it — confirming (a) the grep arm matches BOTH forms, (b) the behavioral counter
    # reports >=1 FROM the real ~/Library/LaunchAgents install file (NOT a fixture-HOME), and (c) the
    # guard rests RED. Then the injected label is disabled + the installed agent file unlinked in the
    # real_state_label finally (a crash between the injected enable() and teardown must not leave a REAL
    # armed agent).
    #
    # OS-CAPABILITY SKIP vs VACUITY SKIP: real_state_label gates on a fast writability probe
    # (`_require_launchagents_writable_or_skip`). In a CAPABLE env (writable home, ~universal) this test
    # RUNS the real mutation-RED (real install-file counter >=1, guard RED) — non-vacuity preserved.
    # Only when the OS genuinely denies the home-dir write does it loud-skip with a documented reason —
    # NOT a clean pass, and distinct from a vacuity skip. It NEVER hangs (no crontab-TCC write path).
    with real_state_label() as label:
        # baseline: the guard is GREEN over the REAL tracked init_instance.py.
        assert _provisioning_is_clean(_PROVISIONING_SURFACES, label), (
            "the guard was not green over the real provisioning surface at baseline"
        )

        # a SCRATCH provision path that (wrongly) arms the runner, in BOTH call-forms.
        scratch = tmp_path / "provision_mutated.py"
        scratch.write_text(textwrap.dedent(f"""\
            \"\"\"SCRATCH provisioning path that WRONGLY arms the runner (AC-8 mutation injection).\"\"\"
            import scripts.runner.schedule.activate as activate
            from scripts.runner.schedule.activate import enable

            def run():
                activate.enable({label!r})   # dotted activate.enable(...) form
                enable({label!r})            # bare `from ...import enable; enable()` form
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

        # the behavioral counter reads >=1 FROM the real install file (the scratch-HOME tautology killer).
        assert activate.active_entry_count(label) >= 1, (
            "the injected enable() did not register a REAL scheduler entry (counter not reading real state)"
        )
        assert _installed_for(label), "the injected entry is not in the REAL ~/Library/LaunchAgents (fixture-HOME read?)"

        # (c) the guard rests RED over the mutated scratch path.
        assert not _provisioning_is_clean([scratch], label), (
            "the guard stayed GREEN under an injected activate.enable() — it is tautological (QA-F2)"
        )

    # after the unconditional teardown, NO real armed agent for the injected label survives.
    assert not _installed_for(label), "a REAL armed launchd agent survived teardown (implicit activation)"
