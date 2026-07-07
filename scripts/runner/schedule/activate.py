"""The operator-owned scheduler activation surface for the weekly cadence runner (ADR-0039-T3).

`enable()` / `disable()` / `status()` are the surface the operator runs to arm, kill, and inspect the
weekly `python -m scripts.runner.cadence_runner` tick (ADR-0039-T1's driver). The runner ships
DISABLED BY DEFAULT: a fresh install loads no scheduler entry, and importing this module arms nothing
(0 `signal` / de-id / dispatch on import — every effect lives inside a function, none at module scope).
No build / provision / `init_instance` step ever calls `enable()`; the operator arms it explicitly (the
NAMED anti-implicit-activation guard, ADR-0039-T3 AC-8, preserves that premise).

`enable()` renders the launchd plist from `cadence-runner.plist.template` — substituting `{{PYTHON}}`
= `sys.executable`, `{{REPO_ROOT}}` = the runtime-derived repo root, `{{LABEL}}` = the runner label —
into a GITIGNORED `*.rendered.plist`, then installs it: launchd (`launchctl load` a `~/Library/
LaunchAgents` agent) when available, else the reversible `crontab` fallback line. It renders NO
operator-specific path into any tracked file and NO `CLAUDE_CODE_OAUTH_TOKEN` into the plist — the
runner PROCESS keychain-reads the OAuth token at runtime (ADR-0039-T2), never a launchd
`EnvironmentVariables` value (SEC-02). The templates are operator-agnostic (placeholder-only), so they
are ADR-0005-safe to track.

The runner adds NO second debounce: the missed-window policy is catch-up-on-next-wake, deferring to
the BUILT `plan_loop._should_regenerate` (a catch-up tick within `MIN_REGEN_INTERVAL_DAYS` no-ops).
This module re-declares no loop constant and imports no loop internals — its whole import surface is
the standard library.

`active_entry_count()` (and `status()`, which wraps it) reads the REAL scheduler state on the branch
`enable()` installs to — the installed `~/Library/LaunchAgents/<label>.plist` file presence when
launchd is available, else the `crontab -l` marker line — never a fixture-HOME dir listing. The
launchd read is a plain filesystem check (reliable, never hangs; the file is the persistent install
launchd loads at login), and every crontab/launchctl subprocess is timeout-bounded so a TCC-blocked
write fails fast rather than hanging. The same real-state counter is reused by the AC-8
anti-implicit-activation guard, so a fresh label reads 0 and an armed label reads >=1 off REAL state.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

# The single runner-label home — reused by enable/disable/status + the templates' {{LABEL}} slot.
RUNNER_LABEL = "com.aplusmaxing.cadence-runner"

# This surface's directory — the templates live here and the rendered *.rendered.plist is written here.
SCHEDULE_DIR = Path(__file__).resolve().parent
PLIST_TEMPLATE = SCHEDULE_DIR / "cadence-runner.plist.template"
CRONTAB_TEMPLATE = SCHEDULE_DIR / "cadence-runner.crontab.template"

# Every crontab/launchctl subprocess is bounded so a TCC-blocked write (a non-interactive
# subagent / CI / fresh-clone context where `crontab -` waits on a Full-Disk-Access prompt that
# never appears) raises `subprocess.TimeoutExpired` FAST (fail-loud) instead of hanging the process
# — a hang is strictly worse than a fast error (no signal + blocks the mandatory baseline/close gate).
_SCHED_TIMEOUT_S = 10


def _repo_root():
    """The runtime-derived repo root: scripts/runner/schedule/activate.py -> ... -> repo root."""
    return Path(__file__).resolve().parents[3]


def _launchd_available():
    """Whether the launchd primary path is usable (a darwin host with `launchctl` on PATH).

    The activation-branch selector: True -> the launchd `StartCalendarInterval` agent; False -> the
    reversible `crontab` fallback line. `active_entry_count` reads launchd registrations only when
    this is True, so a single call site governs both which branch `enable()` installs and where the
    counter reads real state.
    """
    return sys.platform == "darwin" and shutil.which("launchctl") is not None


def _rendered_plist_path(label):
    """The gitignored rendered-instance plist path for a label (matches `*.rendered.plist`)."""
    return SCHEDULE_DIR / f"{label}.rendered.plist"


def _launchagents_dir():
    """The operator's per-user launchd agent directory."""
    return Path.home() / "Library" / "LaunchAgents"


def _installed_plist_path(label):
    """The installed launchd agent path for a label."""
    return _launchagents_dir() / f"{label}.plist"


def _crontab_marker(label):
    """The trailing comment marker that scopes a crontab line to a runner label."""
    return f"# {label}"


def _render(template_text, *, python, repo_root, label):
    """Substitute the `{{PYTHON}}` / `{{REPO_ROOT}}` / `{{LABEL}}` placeholders in a template."""
    return (template_text.replace("{{PYTHON}}", python)
            .replace("{{REPO_ROOT}}", repo_root)
            .replace("{{LABEL}}", label))


def _render_plist(label):
    """Render the launchd plist for a label into its gitignored `*.rendered.plist` and return the path.

    Renders regardless of the install branch, so the rendered instance exists for inspection even on
    the cron fallback path.
    """
    text = _render(PLIST_TEMPLATE.read_text(encoding="utf-8"),
                   python=sys.executable, repo_root=str(_repo_root()), label=label)
    rendered = _rendered_plist_path(label)
    rendered.write_text(text, encoding="utf-8")
    return rendered


def _render_crontab_line(label):
    """The single cron entry line for a label, rendered from the crontab template (comments dropped)."""
    text = _render(CRONTAB_TEMPLATE.read_text(encoding="utf-8"),
                   python=sys.executable, repo_root=str(_repo_root()), label=label)
    marker = _crontab_marker(label)
    for line in text.splitlines():
        if line.rstrip().endswith(marker) and not line.lstrip().startswith("#"):
            return line
    raise RuntimeError("crontab template carries no cron entry line for the label")


def _read_crontab():
    """The current user crontab as `(had_crontab, text)` — `(False, "")` when none is installed."""
    proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=_SCHED_TIMEOUT_S)
    if proc.returncode != 0:
        return (False, "")
    return (True, proc.stdout)


def _write_crontab(text):
    """Install `text` as the user crontab (a `crontab -` write). Callers decide empty-vs-remove."""
    subprocess.run(["crontab", "-"], input=text if text.endswith("\n") else text + "\n",
                   text=True, check=True, timeout=_SCHED_TIMEOUT_S)


def _remove_crontab():
    """Remove the user crontab entirely (`crontab -r`) — only when nothing else remains."""
    subprocess.run(["crontab", "-r"], capture_output=True, text=True, timeout=_SCHED_TIMEOUT_S)


def _install_cron(label):
    """Append the label's cron line to the user crontab; idempotent (no duplicate line)."""
    had, text = _read_crontab()
    lines = text.splitlines() if had else []
    marker = _crontab_marker(label)
    if any(line.rstrip().endswith(marker) for line in lines):
        return
    lines.append(_render_crontab_line(label))
    _write_crontab("\n".join(lines) + "\n")


def _remove_cron(label):
    """Strip the label's cron line from the user crontab; idempotent (no-op when absent).

    Preserves ALL residual content: when any non-runner line remains (INCLUDING comments and blank
    lines) the crontab is rebuilt from the kept lines via `crontab -`; `crontab -r` (wiping the whole
    crontab) is used ONLY when the runner line was genuinely the sole line — so the kill-switch never
    nukes an operator's unrelated crontab entries (Security LOW-2).
    """
    had, text = _read_crontab()
    if not had:
        return
    marker = _crontab_marker(label)
    lines = text.splitlines()
    kept = [line for line in lines if not line.rstrip().endswith(marker)]
    if len(kept) == len(lines):
        return  # the runner line was not present — idempotent no-op
    if kept:
        _write_crontab("\n".join(kept) + "\n")
    else:
        _remove_crontab()


def _launchctl(args):
    """Best-effort `launchctl <args>` — timeout-bounded; a headless / absent launchctl is non-fatal.

    The `~/Library/LaunchAgents/<label>.plist` FILE is the authoritative install (launchd loads it at
    login); `launchctl load`/`unload` is a best-effort IMMEDIATE-(de)activation convenience whose
    failure in a headless / no-GUI / non-darwin context (rc != 0, `TimeoutExpired`, or a missing
    binary) must NOT fail `enable()`/`disable()` — the file write/unlink is the real state. Motivation
    stated per the no-defensive-programming policy: the install is the file, launchctl is a convenience.
    """
    try:
        subprocess.run(["launchctl", *args], capture_output=True, text=True, timeout=_SCHED_TIMEOUT_S)
    except (subprocess.SubprocessError, OSError):
        pass


def _install_launchd(label, rendered):
    """Install the rendered plist as a `~/Library/LaunchAgents` agent (file = authoritative install)."""
    installed = _installed_plist_path(label)
    installed.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(rendered, installed)
    _launchctl(["load", str(installed)])


def _remove_launchd(label):
    """Remove the label's installed launchd agent file; idempotent (no-op when absent)."""
    installed = _installed_plist_path(label)
    if installed.exists():
        _launchctl(["unload", str(installed)])
        installed.unlink()


def _crontab_entry_count(label):
    """The count of REAL `crontab -l` lines carrying the label's marker."""
    had, text = _read_crontab()
    if not had:
        return 0
    marker = _crontab_marker(label)
    return sum(1 for line in text.splitlines() if line.rstrip().endswith(marker))


def _launchd_entry_count(label):
    """1 when the runner is installed as a launchd agent, else 0.

    Reads the REAL install-location file presence (`~/Library/LaunchAgents/<label>.plist`) — the
    persistent "armed" state launchd loads at login — NOT `launchctl list` (which needs an immediate
    load that fails in a headless context) and NOT a fixture-HOME dir listing. A plain filesystem read:
    reliable, never hangs.
    """
    return 1 if _installed_plist_path(label).exists() else 0


def active_entry_count(label=RUNNER_LABEL):
    """The count of REAL scheduler registrations for the runner label, on the ACTIVE branch.

    Reads real state on the branch `enable()` installs to — the launchd install-file presence when
    launchd is available, else the `crontab -l` marker lines — never a fixture-HOME dir listing. A
    fresh label reads 0; an `enable()`d label reads >=1. The single resolution path reused by
    `status()` and the AC-8 anti-implicit-activation guard.

    Args:
        label (str, optional): The runner label to count registrations for.

    Returns:
        (int) The number of real scheduler entries registered for the label.
    """
    if _launchd_available():
        return _launchd_entry_count(label)
    return _crontab_entry_count(label)


def status(label=RUNNER_LABEL):
    """Report ENABLED/DISABLED for the runner label by reading REAL scheduler registration.

    Args:
        label (str, optional): The runner label to inspect.

    Returns:
        (dict) `{"state": "ENABLED" | "DISABLED", "active_entries": int, "label": str}` — `state` is
        ENABLED iff the real-state active-entry count is > 0.
    """
    count = active_entry_count(label)
    return {"state": "ENABLED" if count > 0 else "DISABLED", "active_entries": count, "label": label}


# The anti-implicit-activation guard scanner (ADR-0039-T3 AC-8): the tokens/symbols a provisioning
# surface must NOT name. `enable` is matched in BOTH the dotted `activate.enable(...)` form AND the
# `from ...schedule.activate import enable; enable()` import-and-call form — a dotted-only substring
# grep MISSES the second form.
_ACTIVATION_TOKENS = ("launchctl", "StartCalendarInterval", "crontab", ".rendered.plist")
_IMPORT_ENABLE_RE = re.compile(r"from\s+[\w.]*schedule\.activate\s+import\s+[^\n]*\benable\b")
_DOTTED_ENABLE_RE = re.compile(r"\bactivate\.enable\s*\(")
_BARE_ENABLE_RE = re.compile(r"(?<![.\w])enable\s*\(")


def _scan_provisioning_for_activation(paths):
    """Scan provisioning source files for any runner-activation token or `activate.enable` call.

    Matches the scheduler-install tokens plus an `activate.enable` call in BOTH the dotted
    `activate.enable(...)` form and the `from ...schedule.activate import enable; enable()`
    import-and-call form. An EMPTY result means the surface arms no runner entry; the reused
    real-state `active_entry_count` supplies the guard's behavioral arm.

    Args:
        paths (list): The provisioning-source file paths to scan.

    Returns:
        (list) One `(path, lineno, line)` tuple per activation hit; empty when the surface is clean.
    """
    hits = []
    for path in paths:
        text = Path(path).read_text(encoding="utf-8")
        imports_enable = bool(_IMPORT_ENABLE_RE.search(text))
        for lineno, line in enumerate(text.splitlines(), start=1):
            if any(token in line for token in _ACTIVATION_TOKENS):
                hits.append((str(path), lineno, line.strip()))
            elif _DOTTED_ENABLE_RE.search(line):
                hits.append((str(path), lineno, line.strip()))
            elif imports_enable and _BARE_ENABLE_RE.search(line):
                hits.append((str(path), lineno, line.strip()))
    return hits


def enable(label=RUNNER_LABEL):
    """Arm the weekly cadence tick for the runner label; render the plist + install the schedule.

    Renders the launchd plist into its gitignored `*.rendered.plist` (0 operator path, 0 OAuth token),
    then installs the schedule via launchd when available, else the reversible `crontab` fallback.
    Idempotent — enabling an already-armed label adds no duplicate entry.

    Args:
        label (str, optional): The runner label to arm.

    Returns:
        (Path) The rendered instance plist path.
    """
    rendered = _render_plist(label)
    if _launchd_available():
        _install_launchd(label, rendered)
    else:
        _install_cron(label)
    return rendered


def disable(label=RUNNER_LABEL):
    """The kill-switch: disarm the runner label on the ACTIVE branch + remove the rendered instance.

    Symmetric with `enable()`: removes the label's launchd agent file when launchd is available, else
    strips its `crontab` line (the residual-safe `_remove_cron`), then removes the rendered instance
    plist. Idempotent — disabling an already-disabled label is a no-op.

    Args:
        label (str, optional): The runner label to disarm.
    """
    if _launchd_available():
        _remove_launchd(label)
    else:
        _remove_cron(label)
    rendered = _rendered_plist_path(label)
    if rendered.exists():
        rendered.unlink()
