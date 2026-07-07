"""The operator-owned scheduler activation surface (ADR-0039-T3, Cycle 1).

`scripts/runner/schedule/activate.py` is the enable/disable/status surface the operator runs to
arm the weekly cadence tick, plus the launchd/cron templates it renders. These tests pin its ten
Cycle-1 acceptance criteria:

  - disabled by default (AC-1) + import-inert (AC-2): a fresh install arms nothing, and importing
    the surface fires 0 signal / de-id / dispatch.
  - the enable/disable/kill-switch round-trip + status (AC-3): the 0 -> 1 -> 0 active-entry count
    read from REAL scheduler state (the real `~/Library/LaunchAgents/<label>.plist` install file for a
    uniquely-labelled runner entry, the launchd branch forced — NEVER a fixture-HOME dir listing).
  - the templates carry 0 operator-specific path + 0 OAuth token (AC-4 / AC-10): tracked,
    operator-agnostic (ADR-0005-safe); the rendered instance is gitignored.
  - the missed-window catch-up + the debounce pair defer to the built loop (AC-5 / AC-7): the runner
    declares no second debounce; `plan_loop._should_regenerate` governs.

The REAL-STATE arms (AC-1 counter, AC-3 round-trip) read the real installed-agent-file presence via
the forced launchd branch (a reliable, NON-HANGING home-dir read/write — deliberately not the
crontab path, whose writes hang under TCC in a non-interactive context); every arm that calls
`enable()` runs under `real_state_label()` — a uniquely-labelled entry with an unconditional,
per-step teardown (`disable()` + a reliable filesystem unlink) so a crash between enable() and
disable() cannot leave a REAL armed agent. An OS-capability probe loud-skips (never a vacuity skip)
only if the home dir is unwritable. The non-real-state arms use a tmp store + fixture
dispatch/`deid_client`; 0 live spend, 0 real operator PII (synthetic tokens only).
"""

import ast
import contextlib
import importlib
import re
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
# Every arm that calls enable() forces the LAUNCHD (file) branch (monkeypatch the launchd-availability
# probe to True) so the real-state artifact is a plain file installed into the REAL
# ~/Library/LaunchAgents — a reversible, cross-platform, NON-HANGING real-state read/write. This is
# deliberately NOT the crontab path: crontab WRITES hang under macOS TCC in a non-interactive
# subagent / CI / fresh-clone context (a partial write there can orphan an un-removable armed entry),
# whereas a home-dir file write + presence-read + unlink always work. Each test runs under a
# uniquely-labelled entry with an UNCONDITIONAL, per-step teardown whose RELIABLE filesystem unlink
# guarantees no REAL armed agent and no rendered-plist litter survives — even if launchctl (a
# best-effort convenience that fails headless) does nothing. Real state, never a fixture HOME.

# Cached ~/Library/LaunchAgents writability: None=unprobed, True/False=result (probed once per session).
_LAUNCHAGENTS_WRITABLE = None


def _launchagents_dir():
    """The REAL per-user launchd agent dir (created if absent) — the real-state install location."""
    d = Path.home() / "Library" / "LaunchAgents"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _require_launchagents_writable_or_skip():
    """Fast probe of REAL ~/Library/LaunchAgents writability; loud `pytest.skip` if the OS denies it.

    OS-CAPABILITY SKIP vs VACUITY SKIP (the recipe's "fail-loud, never skip" reconciliation): this is
    NOT the forbidden vacuity-skip. The real-state arms install a plain file into the REAL
    ~/Library/LaunchAgents (never a fixture HOME) — a home-dir write that does NOT hit the crontab-TCC
    write-hang and never blocks pytest. In a CAPABLE env (a writable home, ~universal) the probe
    SUCCEEDS and the real-state mutation-RED STILL RUNS — the counter reads the real install-file
    presence, the guard REDs — so non-vacuity is preserved. It skips ONLY when the OS genuinely denies
    the home-dir write, a loud reasoned skip that does NOT read as a clean pass. Probed once, cached.
    """
    global _LAUNCHAGENTS_WRITABLE
    if _LAUNCHAGENTS_WRITABLE is False:
        pytest.skip("~/Library/LaunchAgents not writable (cached) — the real-state mutation-RED "
                    "requires a launchd-capable context (OS-capability skip)")
    if _LAUNCHAGENTS_WRITABLE is True:
        return
    probe = _launchagents_dir() / f"com.aplusmaxing.cadence-runner.capprobe-{uuid.uuid4().hex}.plist"
    try:
        probe.write_text("<probe/>\n", encoding="utf-8")
        ok = probe.exists()
        probe.unlink()
    except OSError:
        _LAUNCHAGENTS_WRITABLE = False
        try:
            if probe.exists():
                probe.unlink()
        except OSError:
            pass
        pytest.skip("~/Library/LaunchAgents not writable — the real-state mutation-RED requires a "
                    "launchd-capable context (OS-capability skip, NOT a vacuity skip: a capable env "
                    "runs the real mutation-RED)")
    _LAUNCHAGENTS_WRITABLE = ok
    if not ok:
        pytest.skip("~/Library/LaunchAgents write did not persist — the real-state mutation-RED "
                    "requires a launchd-capable context (OS-capability skip)")


def _installed_for(label):
    """Whether the REAL launchd install file for a label is present (the real-state read)."""
    return activate._installed_plist_path(label).exists()


@contextlib.contextmanager
def real_state_label():
    """Yield a uniquely-labelled runner label with the LAUNCHD (file) branch forced + bulletproof teardown.

    Forces `activate._launchd_available` -> True so enable() installs a plain file into the REAL
    ~/Library/LaunchAgents (reversible, non-hanging, cross-platform real-state — NOT a fixture HOME and
    NOT the crontab-TCC-hanging path); a writability probe loud-skips only if the OS denies the
    home-dir write (so `pytest -q` never hangs). Each teardown step is INDEPENDENT so a failing
    disable() never skips the RELIABLE filesystem unlink of the installed agent file + the rendered
    instance — no REAL armed agent and no rendered-plist litter survives.
    """
    _require_launchagents_writable_or_skip()
    saved_probe = activate._launchd_available
    activate._launchd_available = lambda: True
    label = f"com.aplusmaxing.cadence-runner.test-{uuid.uuid4().hex}"
    try:
        yield label
    finally:
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
    # active-entry counter reads 0 FROM the real ~/Library/LaunchAgents install-file presence (not a
    # fixture-HOME dir) BEFORE any enable(). Because the label is unique-per-run, real state for it is
    # legitimately 0 at entry. Falsification down-payment: importing/constructing the surface without
    # enable() leaves the real-state count at 0 (it goes >=1 only when an entry is actually installed —
    # proven by AC-3).
    with real_state_label() as label:
        assert activate.active_entry_count(label) == 0, (
            "a fresh label had a real scheduler entry before enable() (disabled-by-default broken)"
        )
        assert activate.status(label)["state"] == "DISABLED"
        # constructing/importing the surface arms nothing — the real-state count stays 0.
        importlib.reload(activate)
        # the reload rebinds the probe module attribute; re-force the launchd branch for the counter read.
        activate._launchd_available = lambda: True
        assert activate.active_entry_count(label) == 0, (
            "importing the runner surface loaded a real entry (import must arm nothing)"
        )


def test_enable_disable_roundtrip_status():
    # AC-3 (enable/disable/kill-switch round-trip + status; the 0 -> 1 -> 0 counter reads REAL state):
    # enable() (forced launchd) installs EXACTLY 1 real ~/Library/LaunchAgents agent file for the
    # label; status() reports ENABLED with the counter reading 1 FROM that real install-file presence;
    # disable() (the kill-switch) removes it, post-disable count == 0 and status() DISABLED. The
    # 0 -> 1 -> 0 round-trip over the REAL counter IS the evidence it reflects REAL registrations, not a
    # constant — the property AC-8's mutation-RED depends on. Teardown unconditionally disables + unlinks.
    with real_state_label() as label:
        assert activate.active_entry_count(label) == 0
        activate.enable(label)
        assert activate.active_entry_count(label) == 1, (
            "enable() did not register exactly 1 real entry for the label"
        )
        assert activate.status(label)["state"] == "ENABLED"
        # corroborate directly against the REAL install file (the counter is not a constant / fixture read).
        assert _installed_for(label), "the label's agent file is not in the real ~/Library/LaunchAgents"
        # idempotent: a second enable() does not add a duplicate entry.
        activate.enable(label)
        assert activate.active_entry_count(label) == 1, "enable() is not idempotent (duplicate entry)"
        activate.disable(label)
        assert activate.active_entry_count(label) == 0, "disable() (kill-switch) did not remove the entry"
        assert activate.status(label)["state"] == "DISABLED"
        assert not _installed_for(label), "the label's agent file survived disable() in ~/Library/LaunchAgents"
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
    with real_state_label() as label:
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
    with real_state_label() as label:
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
    with real_state_label() as label:
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


# =====================================================================================
# Tier-2 review fixes — safe kill-switch (Security LOW-2) + timeout-bounded subprocesses -
# =====================================================================================
#
# The cron-branch kill-switch is exercised here as a PURE-LOGIC test over monkeypatched crontab I/O
# (no real crontab subprocess — crontab writes hang under TCC in a non-interactive context, so a real
# crontab test is neither reliable nor safe). The launchd-branch kill-switch is covered by AC-3's real
# 0 -> 1 -> 0 round-trip.


def _fake_crontab_io(monkeypatch, text):
    """Monkeypatch activate's crontab I/O over an in-memory crontab; return the mutable state dict."""
    state = {"text": text, "removed_all": False}
    monkeypatch.setattr(activate, "_read_crontab", lambda: (True, state["text"]))
    monkeypatch.setattr(activate, "_write_crontab", lambda t: state.__setitem__("text", t))
    monkeypatch.setattr(activate, "_remove_crontab", lambda: state.update(text="", removed_all=True))
    return state


def test_kill_switch_preserves_residual_crontab_content(monkeypatch):
    # Security LOW-2: disable()'s cron-branch kill-switch must NOT wipe residual crontab content
    # (comments / other jobs) when it strips the runner line — it rebuilds from the kept lines.
    label = "com.aplusmaxing.cadence-runner.test-resid"
    state = _fake_crontab_io(
        monkeypatch,
        f"# operator comment\n0 5 * * * other-job\n0 3 * * 1 run  # {label}\n",
    )
    activate._remove_cron(label)
    assert not state["removed_all"], "the kill-switch wiped the WHOLE crontab despite residual content (LOW-2)"
    assert "# operator comment" in state["text"], "the kill-switch nuked an operator comment line"
    assert "0 5 * * * other-job" in state["text"], "the kill-switch nuked an unrelated cron job"
    assert label not in state["text"], "the kill-switch did not strip the runner line"


def test_kill_switch_preserves_blank_only_residual(monkeypatch):
    # Security LOW-2 (the exact bug): when the ONLY residual is a blank line, the kill-switch must NOT
    # `crontab -r` the whole crontab — it rebuilds from the kept (blank) line, preserving the crontab.
    label = "com.aplusmaxing.cadence-runner.test-blank"
    state = _fake_crontab_io(monkeypatch, f"\n0 3 * * 1 run  # {label}\n")
    activate._remove_cron(label)
    assert not state["removed_all"], "the kill-switch `crontab -r`'d on a blank-only residual (LOW-2)"
    assert label not in state["text"], "the kill-switch did not strip the runner line"


def test_kill_switch_removes_crontab_when_runner_was_sole_line(monkeypatch):
    # The `crontab -r` path is used ONLY when the runner line was genuinely the sole line.
    label = "com.aplusmaxing.cadence-runner.test-sole"
    state = _fake_crontab_io(monkeypatch, f"0 3 * * 1 run  # {label}\n")
    activate._remove_cron(label)
    assert state["removed_all"], "the kill-switch did not `crontab -r` when the runner line was the sole line"


def test_all_scheduler_subprocesses_are_timeout_bounded():
    # Defect-1a: every crontab/launchctl subprocess.run in activate.py carries a timeout= keyword so a
    # TCC-blocked write fails FAST (never hangs `pytest -q`). AST-level assertion (robust to nested
    # parens); failing-capable (dropping a timeout= keyword reddens it).
    tree = ast.parse(Path(activate.__file__).read_text(encoding="utf-8"))
    sched_calls = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "run" and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"):
            continue
        if not (node.args and isinstance(node.args[0], ast.List) and node.args[0].elts
                and isinstance(node.args[0].elts[0], ast.Constant)
                and node.args[0].elts[0].value in ("crontab", "launchctl")):
            continue
        cmd = node.args[0].elts[0].value
        sched_calls.append(cmd)
        assert "timeout" in {kw.arg for kw in node.keywords}, (
            f"subprocess.run(['{cmd}', ...]) lacks a timeout= keyword (hang risk)"
        )
    assert sched_calls, "no scheduler subprocess.run calls found in activate.py (the test is vacuous)"
