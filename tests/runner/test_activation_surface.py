"""The operator-owned scheduler activation surface (ADR-0039-T3, Cycle 1).

`scripts/runner/schedule/activate.py` is the enable/disable/status surface the operator runs to
arm the weekly cadence tick, plus the launchd/cron templates it renders. These tests pin its ten
Cycle-1 acceptance criteria:

  - disabled by default (AC-1) + import-inert (AC-2): a fresh install arms nothing, and importing
    the surface fires 0 signal / de-id / dispatch.
  - the enable/disable/kill-switch round-trip + status (AC-3): the 0 -> 1 -> 0 active-entry count
    read from REAL scheduler state (the real `crontab -l` for a uniquely-labelled runner entry, the
    cron branch forced so the entry is a single restorable line — NEVER a fixture-HOME dir listing).
  - the templates carry 0 operator-specific path + 0 OAuth token (AC-4 / AC-10): tracked,
    operator-agnostic (ADR-0005-safe); the rendered instance is gitignored.
  - the missed-window catch-up + the debounce pair defer to the built loop (AC-5 / AC-7): the runner
    declares no second debounce; `plan_loop._should_regenerate` governs.

The REAL-STATE arms (AC-1 counter, AC-3 round-trip) read the real `crontab -l` via the forced cron
branch and FAIL LOUD (never `pytest.skip`) if no scheduler is available; every arm that calls
`enable()` runs under `forced_cron_label()` — a uniquely-labelled entry with an unconditional
try/finally teardown (`disable()` + a crontab snapshot-restore) so a crash between enable() and
disable() cannot leave a REAL armed entry. The non-real-state arms use a tmp store + fixture
dispatch/`deid_client`; 0 live spend, 0 real operator PII (synthetic tokens only).
"""

import contextlib
import importlib
import re
import shutil
import subprocess
import uuid
from pathlib import Path

import pytest

from scripts.model.client import ModelClient
from scripts.serve import plan_loop
from scripts.store import plan_schema, store

from scripts.runner import cadence_runner
from scripts.runner.schedule import activate

from tests.serve.test_plan_loop_regen import (
    _ON_DATE,
    _REGRESSING,
    _SUSTAINED_DATES,
    _SummarizeDeid,
    _TrendDispatch,
    _regen_root,
    _seed,
    _seed_biomarker,
    _seed_store,
)

# tests/runner/test_activation_surface.py -> tests -> <repo root>.
REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "scripts" / "runner" / "schedule"
PLIST_TEMPLATE = SCHEDULE_DIR / "cadence-runner.plist.template"
CRONTAB_TEMPLATE = SCHEDULE_DIR / "cadence-runner.crontab.template"


# --- real-state test hygiene (shared by both T3 test files; Security L3) -------------
#
# Every arm that calls enable() forces the reversible CRON branch (monkeypatch the launchd-
# availability probe to False) so the armed entry is a single restorable `crontab` line, never a
# registration in the operator's live launchd GUI domain, and runs under a uniquely-labelled entry
# with an UNCONDITIONAL try/finally teardown. A crash between enable() and disable() must not leave a
# REAL armed entry (an un-torn-down entry is itself the implicit activation the task forbids).


def _require_scheduler_or_fail():
    """FAIL LOUD (never skip) if no OS scheduler is available for the real-state arms.

    The close-audit FATAL-on-skip posture reads a skipped non-tautology proof as clean, so a missing
    scheduler must redden — it never `pytest.skip`s. The pinned cron branch needs `crontab`; if it is
    absent the real-state arm cannot run.
    """
    if not shutil.which("crontab") and not shutil.which("launchctl"):
        pytest.fail("no scheduler (launchctl/crontab) available — real-state arm cannot run (never skip)")
    if not shutil.which("crontab"):
        pytest.fail("crontab unavailable — the pinned cron-branch real-state arm cannot run (never skip)")


def _snapshot_crontab():
    """The current user crontab, as `(had_crontab, text)` — `(False, "")` when none is installed."""
    proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if proc.returncode != 0:
        return (False, "")
    return (True, proc.stdout)


def _restore_crontab(had, snapshot):
    """Restore the pre-test crontab exactly: rewrite the snapshot, or remove the crontab if none."""
    if had:
        subprocess.run(["crontab", "-"], input=snapshot, text=True, check=True)
    else:
        subprocess.run(["crontab", "-r"], capture_output=True, text=True)


def _crontab_lines_for(label):
    """The real `crontab -l` lines carrying the runner `# <label>` marker (real-state read)."""
    had, text = _snapshot_crontab()
    if not had:
        return []
    return [ln for ln in text.splitlines() if ln.rstrip().endswith(f"# {label}")]


@contextlib.contextmanager
def forced_cron_label():
    """Yield a uniquely-labelled runner label with the CRON branch forced + a bullet-proof teardown.

    Forces `activate._launchd_available` to False (the reversible cron branch), snapshots the crontab,
    and unconditionally `disable()`s the label + restores the crontab snapshot + removes any rendered
    instance on exit — even if the body raises between enable() and teardown.
    """
    _require_scheduler_or_fail()
    saved_probe = activate._launchd_available
    activate._launchd_available = lambda: False
    label = f"com.aplusmaxing.cadence-runner.test-{uuid.uuid4().hex}"
    had, snapshot = _snapshot_crontab()
    try:
        yield label
    finally:
        try:
            activate.disable(label)
        finally:
            _restore_crontab(had, snapshot)
            rendered = activate._rendered_plist_path(label)
            if rendered.exists():
                rendered.unlink()
            activate._launchd_available = saved_probe


def _single_reading_root(tmp_path, name):
    """A store past the min-interval (old prior plan) but with a SINGLE hrv reading.

    One reading is < `SUSTAINED_WINDOW_MIN_READINGS`, so `_sustained_signal` is False and the built
    debounce holds (0 re-gens) even though the min-interval has elapsed — the AC-7 single arm.
    """
    root = tmp_path / name
    _seed_store(root)
    _seed(root)
    plan_schema.record_plan(
        "workout", {"exercises": [{"name": "Squat", "sets": 3}]},
        "2026-06-01", "personal-trainer", root,
    )
    _seed_biomarker(root, "hrv", (50,), ("2026-06-16",))
    return root


def _within_interval_root(tmp_path, name):
    """A sustained series whose last re-gen (2026-06-14) is < 7 days before `_ON_DATE` (2026-06-18).

    The min-interval arm of `_should_regenerate` holds, so a catch-up tick no-ops (`regenerated:
    False`) — the AC-5 missed-window catch-up over the built debounce.
    """
    root = tmp_path / name
    _seed_store(root)
    _seed(root)
    plan_schema.record_plan(
        "workout", {"exercises": [{"name": "Squat", "sets": 3}]},
        "2026-06-14", "personal-trainer", root,
    )
    _seed_biomarker(root, "hrv", _REGRESSING, _SUSTAINED_DATES)
    return root


# =====================================================================================
# AC-1 / AC-3 — disabled-by-default + enable/disable/kill-switch round-trip (REAL state)
# =====================================================================================


def test_disabled_by_default_fresh_install():
    # AC-1 (disabled by default; the counter reads REAL scheduler state, PF-S63-02 falsifiable):
    # with NO entry loaded for a uniquely-labelled runner label, status() reports DISABLED and the
    # active-entry counter reads 0 FROM the real `crontab -l` (not a fixture-HOME dir) BEFORE any
    # enable(). Because the label is unique-per-run, real state for it is legitimately 0 at entry.
    # Falsification down-payment: importing/constructing the surface without enable() leaves the
    # real-state count at 0 (it goes >=1 only when an entry is actually loaded — proven by AC-3).
    with forced_cron_label() as label:
        assert activate.active_entry_count(label) == 0, (
            "a fresh label had a real scheduler entry before enable() (disabled-by-default broken)"
        )
        assert activate.status(label)["state"] == "DISABLED"
        # constructing/importing the surface arms nothing — the real-state count stays 0.
        importlib.reload(activate)
        # the reload rebinds the probe module attribute; re-force the cron branch for the counter read.
        activate._launchd_available = lambda: False
        assert activate.active_entry_count(label) == 0, (
            "importing the runner surface loaded a real entry (import must arm nothing)"
        )


def test_enable_disable_roundtrip_status():
    # AC-3 (enable/disable/kill-switch round-trip + status; the 0 -> 1 -> 0 counter reads REAL state):
    # enable() (forced cron) writes EXACTLY 1 restorable crontab line for the label; status() reports
    # ENABLED with the counter reading 1 FROM the real `crontab -l`; disable() (the kill-switch)
    # removes it, post-disable count == 0 and status() DISABLED. The 0 -> 1 -> 0 round-trip over the
    # REAL counter IS the evidence it reflects REAL registrations, not a constant — the property AC-8's
    # mutation-RED depends on. Teardown (context manager) unconditionally disables + restores.
    with forced_cron_label() as label:
        assert activate.active_entry_count(label) == 0
        activate.enable(label)
        assert activate.active_entry_count(label) == 1, (
            "enable() did not register exactly 1 real entry for the label"
        )
        assert activate.status(label)["state"] == "ENABLED"
        # corroborate directly against the REAL crontab (the counter is not a constant / fixture read).
        assert len(_crontab_lines_for(label)) == 1, "the label's line is not in the real crontab"
        # idempotent: a second enable() does not add a duplicate line.
        activate.enable(label)
        assert activate.active_entry_count(label) == 1, "enable() is not idempotent (duplicate entry)"
        activate.disable(label)
        assert activate.active_entry_count(label) == 0, "disable() (kill-switch) did not remove the entry"
        assert activate.status(label)["state"] == "DISABLED"
        assert _crontab_lines_for(label) == [], "the label's line survived disable() in the real crontab"
        # disable() is idempotent — disabling an already-disabled label is a no-op.
        activate.disable(label)
        assert activate.active_entry_count(label) == 0


# =====================================================================================
# AC-2 — building/importing the surface fires 0 signal / de-id / dispatch --------------
# =====================================================================================


def test_import_is_inert(monkeypatch):
    # AC-2: importing scripts.runner.schedule.activate + constructing the surface WITHOUT enable()/run()
    # fires 0 plan_loop.signal, 0 de-id (0 self-constructed ModelClient), 0 dispatch — building the
    # activation surface arms nothing. (activate imports neither plan_loop nor ModelClient; the spies
    # make that failing-capable — a module that fired signal/de-id on import would redden.)
    signal_calls = []
    monkeypatch.setattr(plan_loop, "signal", lambda *a, **k: signal_calls.append((a, k)))
    client_inits = []
    real_init = ModelClient.__init__

    def spy_init(self, *a, **k):
        client_inits.append(self)
        return real_init(self, *a, **k)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)
    importlib.reload(importlib.import_module("scripts.runner.schedule.activate"))
    assert signal_calls == [], "importing activate fired plan_loop.signal"
    assert client_inits == [], "importing activate constructed a ModelClient (de-id)"


# =====================================================================================
# AC-4 — the templates carry 0 operator-specific path; the rendered instance is gitignored
# =====================================================================================


def _string_values(plist_text):
    """The `<string>...</string>` element values of a plist (the rendered-target strings)."""
    return re.findall(r"<string>(.*?)</string>", plist_text, flags=re.DOTALL)


def test_plist_template_zero_operator_path():
    # AC-4 (plist template 0 operator-specific path; Negative-5): the tracked template carries no
    # absolute operator path (no /Users/, no /home/) — only the {{PYTHON}}/{{REPO_ROOT}}/{{LABEL}}
    # placeholders. Failing-capable: a template with a literal /Users/walter/... path reddens this.
    text = PLIST_TEMPLATE.read_text(encoding="utf-8")
    assert "/Users/" not in text, "the plist template carries a hardcoded /Users/ operator path (Negative-5)"
    assert "/home/" not in text, "the plist template carries a hardcoded /home/ operator path (Negative-5)"
    absolute = [v for v in _string_values(text) if v.startswith("/")]
    assert absolute == [], f"the plist template carries non-placeholder absolute paths: {absolute}"
    for placeholder in ("{{PYTHON}}", "{{REPO_ROOT}}", "{{LABEL}}"):
        assert placeholder in text, f"the plist template is missing the {placeholder} placeholder"


def test_crontab_template_placeholder_only():
    # AC-4 (crontab fallback template placeholder-only): the tracked crontab template carries no
    # absolute operator path and only the {{PYTHON}}/{{REPO_ROOT}}/{{LABEL}} placeholders.
    text = CRONTAB_TEMPLATE.read_text(encoding="utf-8")
    assert "/Users/" not in text, "the crontab template carries a hardcoded /Users/ operator path"
    assert "/home/" not in text, "the crontab template carries a hardcoded /home/ operator path"
    for placeholder in ("{{PYTHON}}", "{{REPO_ROOT}}", "{{LABEL}}"):
        assert placeholder in text, f"the crontab template is missing the {placeholder} placeholder"


def test_rendered_instance_plist_is_gitignored():
    # AC-4 (rendered instance gitignored): enable() renders the plist to a gitignored path; the
    # rendered *.rendered.plist is untracked (git check-ignore returns it). Failing-capable: a rendered
    # path not covered by .gitignore reddens (git check-ignore returns nonzero / empty).
    with forced_cron_label() as label:
        activate.enable(label)
        rendered = activate._rendered_plist_path(label)
        assert rendered.exists(), "enable() did not render an instance plist"
        rel = rendered.relative_to(REPO_ROOT)
        out = subprocess.run(
            ["git", "check-ignore", str(rel)], capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert out.returncode == 0 and out.stdout.strip(), (
            f"the rendered instance plist is not gitignored: {rel} (git check-ignore returned nothing)"
        )


# =====================================================================================
# AC-10 — the OAuth token is NEVER rendered into the plist (SEC-02) --------------------
# =====================================================================================

# The token-VALUE pattern (a `sk-ant-oat` prefix + the token-char class). Assembled from fragments so
# no verbatim token literal is written into the tree (a tracked literal would self-match the repo's
# tree-wide token scan). The pattern is the same shape a real OAuth token value carries.
_OAT_PREFIX = "sk-" + "ant-" + "oat"
_TOKEN_VALUE_RE = re.compile(re.escape(_OAT_PREFIX) + r"[A-Za-z0-9_-]+")
_TOKEN_ENV_LITERAL = "CLAUDE_CODE_OAUTH_TOKEN"


def test_oauth_token_never_in_plist_template():
    # AC-10 (SEC-02): the plist TEMPLATE carries neither the CLAUDE_CODE_OAUTH_TOKEN env-var literal nor
    # a token-VALUE. Positive control (scan non-vacuity): a runtime-assembled token-shaped probe MATCHES
    # the pattern, proving the 0-hit result over the real template is a real 0, not a broken pattern.
    probe = _OAT_PREFIX + uuid.uuid4().hex  # runtime-assembled, never a tracked literal
    assert _TOKEN_VALUE_RE.search(probe), "the AC-10 token pattern is inert (positive control failed)"
    text = PLIST_TEMPLATE.read_text(encoding="utf-8")
    assert _TOKEN_ENV_LITERAL not in text, "the plist template names CLAUDE_CODE_OAUTH_TOKEN (SEC-02)"
    assert not _TOKEN_VALUE_RE.search(text), "the plist template carries an OAuth token value (SEC-02)"


def test_oauth_token_never_in_rendered_plist():
    # AC-10 (SEC-02): the RENDERED instance plist (produced by enable()) carries neither the env-var
    # literal nor a token value — the token is keychain-read by the runner PROCESS at runtime (T2),
    # never injected as a launchd EnvironmentVariables value. Failing-capable: rendering the token into
    # EnvironmentVariables would redden both plist scans while the positive control stays green.
    probe = _OAT_PREFIX + uuid.uuid4().hex
    assert _TOKEN_VALUE_RE.search(probe), "the AC-10 token pattern is inert (positive control failed)"
    with forced_cron_label() as label:
        activate.enable(label)
        rendered = activate._rendered_plist_path(label).read_text(encoding="utf-8")
        assert _TOKEN_ENV_LITERAL not in rendered, "the rendered plist names CLAUDE_CODE_OAUTH_TOKEN (SEC-02)"
        assert not _TOKEN_VALUE_RE.search(rendered), "the rendered plist carries an OAuth token value (SEC-02)"


# =====================================================================================
# AC-5 / AC-6 / AC-7 — the runner defers to the BUILT debounce (no second debounce) ----
# =====================================================================================


def test_missed_window_catchup_honors_built_debounce(tmp_path):
    # AC-5 (missed-window catch-up honors the built debounce): the plist template sets
    # StartCalendarInterval; a catch-up tick fired WITHIN MIN_REGEN_INTERVAL_DAYS of the last completed
    # re-gen produces 0 new plans — driving plan_loop.signal (through T1's cadence_runner.run) over a
    # store whose _last_regen_date is < 7 days prior returns regenerated: False. The within-interval
    # no-op path DOES carry a `regenerated: False` key (distinct from AC-7's gate-pass path). The runner
    # adds NO second debounce — the built plan_loop._should_regenerate governs.
    assert "StartCalendarInterval" in PLIST_TEMPLATE.read_text(encoding="utf-8"), (
        "the plist template does not set StartCalendarInterval (the weekly cadence)"
    )
    root = _within_interval_root(tmp_path, "catchup")
    session = _TrendDispatch()
    result = cadence_runner.run(root, dispatch_factory=lambda: session,
                                deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert result["regenerated"] is False, (
        f"a catch-up tick within the min-interval re-generated (built debounce not honored): {result}"
    )
    assert session.spec_calls() == [], "a within-interval catch-up dispatched a specialist (0 new plans expected)"


def test_activation_gate_disabled_zero_signals(monkeypatch):
    # AC-6 (activation gate — disabled -> 0 re-gens): with the schedule DISABLED (no entry loaded) the
    # runner tick is never invoked -> plan_loop.signal call-count == 0. NOTE (SUBSUMED): a unit test
    # cannot make the OS launchd/cron fire and there is no "disabled -> run() returns early" gate, so
    # this is a STATED INVARIANT (the scheduler drives nothing while no entry is loaded), NOT the
    # disabled-by-default falsification — that is the AC-1 + AC-3 real-state counter round-trip.
    signal_calls = []
    monkeypatch.setattr(plan_loop, "signal", lambda *a, **k: signal_calls.append((a, k)))
    with forced_cron_label() as label:
        assert activate.status(label)["state"] == "DISABLED"
        # over a multi-week synthetic window with no entry loaded, nothing fires the tick.
        for _week in range(6):
            assert activate.active_entry_count(label) == 0, "an entry was armed while the schedule is disabled"
    assert signal_calls == [], "plan_loop.signal fired while the schedule was disabled"


def test_built_debounce_pair_once_enabled(tmp_path, monkeypatch):
    # AC-7 (built debounce pair holds once enabled): a single new reading IN-window -> 0 re-gens; a
    # sustained signal past MIN_REGEN_INTERVAL_DAYS -> EXACTLY 1 re-gen. Measured by a concrete re-gen
    # COUNT (a spy on plan_loop.regenerate), NOT result["regenerated"] (the gate-pass path returns
    # regenerate(...)'s result, which carries NO `regenerated` key). The runner adds no second debounce
    # — the pair maps to (0, 1) via the built plan_loop._should_regenerate.
    regen_calls = []
    real_regen = plan_loop.regenerate

    def spy(*a, **k):
        regen_calls.append((a, k))
        return real_regen(*a, **k)

    monkeypatch.setattr(plan_loop, "regenerate", spy)

    # single new reading IN-window (not sustained) -> the debounce holds -> 0 re-gens.
    single_root = _single_reading_root(tmp_path, "single")
    single_session = _TrendDispatch()
    cadence_runner.run(single_root, dispatch_factory=lambda: single_session,
                       deid_client=_SummarizeDeid(single_root), plan_date=_ON_DATE)
    assert len(regen_calls) == 0, f"a single in-window reading re-generated (want 0): {len(regen_calls)}"
    assert single_session.spec_calls() == [], "a single in-window reading dispatched a specialist"

    # sustained signal past the min-interval -> EXACTLY 1 re-gen.
    regen_calls.clear()
    sustained_root = _regen_root(tmp_path, "sustained", _REGRESSING)
    sustained_session = _TrendDispatch()
    cadence_runner.run(sustained_root, dispatch_factory=lambda: sustained_session,
                       deid_client=_SummarizeDeid(sustained_root), plan_date=_ON_DATE)
    assert len(regen_calls) == 1, f"a sustained signal did not re-gen exactly once (want 1): {len(regen_calls)}"
    assert sustained_session.spec_calls(), "the sustained re-gen dispatched no specialist (corroboration)"
