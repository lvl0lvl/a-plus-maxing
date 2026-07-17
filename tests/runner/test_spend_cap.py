"""Tests for the per-tester cumulative monthly spend cap (ADR-0049-T3).

`scripts.runner.spend_cap.SpendCap` maintains a cumulative monthly per-tester count in a gitignored
instance-local JSON ledger (keyed by `getpass.getuser()` + `YYYY-MM`) and fails closed — serialized,
atomic, check-then-increment — past the per-tester monthly ceiling. `SpendCapExceeded` subclasses
`dispatch_budget.DispatchCapExceeded` (C1) so a refusal surfaces honest-no-plan at
`plan_orchestrator.py:314` when the metered loop is armed, rather than crashing the run.
`metered_dispatch.build_dispatch(client, *, spend_cap=None)` gains the injectable consult-before-
dispatch seam (default-OFF — the ADR-0049-T1 D2 tests are byte-unchanged).

Every env/clock/ledger/tester crosses through an INJECTED seam: a tmp `ledger_path`, a fake `clock`,
a synthetic `tester`. No test touches the real instance ledger or a real `getpass.getuser()`, and the
tree carries 0 real operator PII.
"""

import ast
import json
import os
import stat
import subprocess
import threading
from datetime import datetime
from pathlib import Path

import pytest

from scripts.plan import dispatch_budget
from scripts.plan.dispatch_budget import DispatchBudget
from scripts.plan.plan_orchestrator import _dispatch_domains, run_orchestrated
from scripts.runner import metered_dispatch
from scripts.runner import spend_cap as spend_cap_mod
from scripts.runner.spend_cap import (
    DEFAULT_MONTHLY_CAP,
    SPEND_CAP_EXCEEDED,
    SpendCap,
    SpendCapExceeded,
)
from tests.plan.test_deid_in import _FixedDeidClient, _raw_intake
from tests.plan.test_plan_orchestrator import _deid_summary, _sustaining_authors
from tests.runner.test_metered_dispatch import (
    _CountingAuthorClient,
    _assert_clean_metered_egress,
    _drive_metered,
)

_SPEND_CAP_SOURCE = Path(__file__).resolve().parents[2] / "scripts" / "runner" / "spend_cap.py"
_TESTER = "synthetic-tester"


def _fixed_clock(date_str):
    """A clock returning a fixed `datetime` parsed from a YYYY-MM-DD string."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return lambda: dt


def _key(tester, month):
    """The ledger's flat `(tester, month)` key."""
    return f"{tester}::{month}"


# --- construction: named-constant defaults + the gitignored production path (AC-1) ----------------


def test_default_ceiling_and_ledger_are_named_module_defaults(tmp_path):
    """The constructor defaults bind the NAMED module-level ceiling + the gitignored production path."""
    cap = SpendCap(ledger_path=tmp_path / "ledger.json", tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    assert cap._ceiling == DEFAULT_MONTHLY_CAP
    default_cap = SpendCap(tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    assert default_cap._ledger_path == spend_cap_mod._DEFAULT_LEDGER_PATH


def test_ac1_production_default_ledger_is_gitignored():
    """AC-1: the production default ledger path is the repo-root `.spend-cap-ledger.json` + gitignored."""
    repo_root = Path(__file__).resolve().parents[2]
    assert spend_cap_mod._DEFAULT_LEDGER_PATH == repo_root / ".spend-cap-ledger.json"
    result = subprocess.run(
        ["git", "check-ignore", ".spend-cap-ledger.json"], cwd=repo_root, capture_output=True
    )
    assert result.returncode == 0, "the production ledger path is not gitignored (`.gitignore` line missing)"


def test_ac1_ledger_created_owner_only(tmp_path):
    """AC-1: the ledger is created owner-only 0o600 (a world-readable ledger REDs, umask-0 precedent)."""
    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=5, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    old_umask = os.umask(0)  # most permissive -> a plain open('w') would show group/world bits
    try:
        cap.charge()
    finally:
        os.umask(old_umask)
    assert ledger.exists()
    mode = stat.S_IMODE(os.stat(ledger).st_mode)
    assert mode == 0o600, f"expected 0600, got {oct(mode)}"
    assert not (mode & 0o077), "group/world bits are set on the ledger"


# --- SpendCapExceeded propagation contract (C1 / AR-3) -------------------------------------------


def test_spend_cap_exceeded_subclasses_dispatch_cap_exceeded_with_distinct_reason():
    """C1/AR-3/F2: SpendCapExceeded IS-A DispatchCapExceeded, distinct reason, `.cap` = the real ceiling."""
    exc = SpendCapExceeded(7, 64)
    assert isinstance(exc, dispatch_budget.DispatchCapExceeded)  # caught at plan_orchestrator:314
    assert exc.reason == SPEND_CAP_EXCEEDED  # NOT clobbered to DISPATCH_CAP_EXCEEDED by the parent __init__
    assert exc.count == 7  # the persisted current count
    assert exc.cap == 64  # the real ceiling — honors the parent's `.cap (int)` contract (LSP, F2)


# --- AC-2: cap enforcement + fail-closed persist, check-then-increment ----------------------------


def test_ac2_cap_enforcement_and_check_then_increment_persist(tmp_path):
    """AC-2/C2: past the ceiling `charge` raises; the persisted count == ceiling (NOT ceiling+1)."""
    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=3, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    key = _key(_TESTER, "2026-07")

    assert cap.charge() == 1
    assert cap.charge() == 2
    assert cap.charge() == 3  # at the ceiling
    with pytest.raises(SpendCapExceeded) as exc:
        cap.charge()  # 3 + 1 > 3 -> refuse WITHOUT writing
    assert exc.value.count == 3, "the halt carries the persisted current (ceiling), not ceiling+1"
    assert exc.value.cap == 3, "the halt carries the real ceiling in `.cap` (F2)"
    # persist assertion (MF-1): the ledger re-read is the ceiling, NOT ceiling+1 (drops the persist-
    # then-check mutant, whose re-read would show 4).
    assert json.loads(ledger.read_text())[key] == 3
    # idempotent refusal: a second past-ceiling charge also raises and the ledger never exceeds ceiling.
    with pytest.raises(SpendCapExceeded):
        cap.charge()
    assert json.loads(ledger.read_text())[key] == 3


# --- AC-2b: refusal E2E via the PRODUCTION consumer run_orchestrated (Arch F1/F2) -----------------


def test_ac2b_run_orchestrated_surfaces_honest_no_plan_at_ceiling(tmp_path):
    """AC-2b: run_orchestrated with a cap at the ceiling surfaces honest-no-plan, NOT a crash."""
    from tests.plan.test_generate_plan import _seed_store

    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=1, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    cap.charge()  # count 1 == ceiling; the run's first dispatch charge must refuse

    client = _CountingAuthorClient(_sustaining_authors())
    dispatch = metered_dispatch.build_dispatch(client, spend_cap=cap)
    store_read = _seed_store(tmp_path)

    out = run_orchestrated(
        _raw_intake(), _FixedDeidClient(_deid_summary()), dispatch, store_read, tmp_path,
        plan_date="2026-07-16", domains=("workout", "nutrition"),
    )
    # the SpendCapExceeded (a DispatchCapExceeded subclass) was caught at :314 -> honest no-plan
    assert out.get("reason") == SPEND_CAP_EXCEEDED
    assert out.get("results") == {}, "a plan recorded past the monthly ceiling"
    # fail-closed BEFORE the outbound metered author call was issued
    assert client.author_call_count == 0, "the metered author was invoked past the spend cap"


# --- AC-3: monthly rollover (injected clock) -----------------------------------------------------


def test_ac3_monthly_rollover(tmp_path):
    """AC-3: a prior-month entry does not count against the current month (month-keyed ledger)."""
    ledger = tmp_path / "ledger.json"
    holder = {"dt": datetime(2026, 7, 16)}
    cap = SpendCap(ledger_path=ledger, ceiling=1, tester=_TESTER, clock=lambda: holder["dt"])

    cap.charge()  # July: count 1 == ceiling
    with pytest.raises(SpendCapExceeded):
        cap.charge()  # July refuses
    holder["dt"] = datetime(2026, 8, 1)  # roll to August
    # falsifier: a mutant keying the ledger without the month would carry July's count into August
    # and this charge would raise -> RED.
    assert cap.charge() == 1, "the new month did not start fresh (ledger not month-keyed)"


# --- AC-4: per-tester isolation + composition with the per-run DispatchBudget ---------------------


def test_ac4_per_tester_isolation(tmp_path):
    """AC-4: tester-A at the ceiling does NOT refuse tester-B (per-tester ledger keying)."""
    ledger = tmp_path / "ledger.json"
    clock = _fixed_clock("2026-07-16")
    cap_a = SpendCap(ledger_path=ledger, ceiling=1, tester="tester-a", clock=clock)
    cap_b = SpendCap(ledger_path=ledger, ceiling=1, tester="tester-b", clock=clock)

    cap_a.charge()  # A at the ceiling
    with pytest.raises(SpendCapExceeded):
        cap_a.charge()
    assert cap_b.charge() == 1, "tester-A's ceiling refused tester-B"


def test_ac4_composition_monthly_ceiling_trips_first(tmp_path):
    """AC-4: monthly-ceiling < per-run-cap -> SpendCapExceeded fires at the closure's consult."""
    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=1, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    client = _CountingAuthorClient(_sustaining_authors())
    dispatch = metered_dispatch.build_dispatch(client, spend_cap=cap)
    with pytest.raises(SpendCapExceeded):
        _dispatch_domains(("workout", "nutrition"), _deid_summary(), {}, dispatch, DispatchBudget(cap=100))


def test_ac4_composition_per_run_cap_trips_first(tmp_path):
    """AC-4: per-run-cap < monthly-ceiling -> DispatchCapExceeded fires FIRST (`:380` before `:382`)."""
    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=100, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    client = _CountingAuthorClient(_sustaining_authors())
    dispatch = metered_dispatch.build_dispatch(client, spend_cap=cap)
    with pytest.raises(dispatch_budget.DispatchCapExceeded) as exc:
        _dispatch_domains(("workout", "nutrition"), _deid_summary(), {}, dispatch, DispatchBudget(cap=1))
    # the per-run cap fired (budget.charge at :380), NOT the monthly spend cap (the :382 closure)
    assert not isinstance(exc.value, SpendCapExceeded)
    assert exc.value.reason == dispatch_budget.DISPATCH_CAP_EXCEEDED


# --- AC-4b: the charge is serialized (Security H1) -----------------------------------------------


def test_ac4b_concurrent_charge_exactly_one_succeeds(tmp_path):
    """AC-4b: N>=8 concurrent charges against ceiling=1 -> EXACTLY ONE succeeds (the lock is load-bearing)."""
    ledger = tmp_path / "ledger.json"
    n = 8
    barrier = threading.Barrier(n)
    fixed = datetime(2026, 7, 16)

    def clock():
        # AR-1 determinism: align every thread at the ledger-read (BEFORE the charge lock) so the
        # lock-free mutant reads the pre-write ledger in every thread (its lost-update window widens
        # to certainty), while the locked GREEN still serializes past this point.
        barrier.wait()
        return fixed

    cap = SpendCap(ledger_path=ledger, ceiling=1, tester=_TESTER, clock=clock)
    successes = []
    refusals = []
    guard = threading.Lock()

    def worker():
        try:
            cap.charge()
            with guard:
                successes.append(1)
        except SpendCapExceeded:
            with guard:
                refusals.append(1)

    threads = [threading.Thread(target=worker) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # the load-bearing assertion: assert on the success-count (a lost-update RMW may still leave
    # count==1, so "exactly one succeeds" is what reliably REDs the lock-free mutant).
    assert len(successes) == 1, f"expected exactly one success, got {len(successes)}"
    assert len(refusals) == n - 1
    assert json.loads(ledger.read_text())[_key(_TESTER, "2026-07")] == 1


# --- AC-4c: corrupt / torn ledger fail-closed (Security M2) --------------------------------------


def test_ac4c_corrupt_ledger_fails_closed(tmp_path):
    """AC-4c: a present-but-corrupt (non-JSON / non-dict) ledger -> fail CLOSED (raise, count=0)."""
    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=5, tester=_TESTER, clock=_fixed_clock("2026-07-16"))

    ledger.write_text("not valid json {{{")  # unreadable
    with pytest.raises(SpendCapExceeded) as exc:
        cap.charge()
    assert exc.value.count == 0
    assert exc.value.reason == SPEND_CAP_EXCEEDED

    ledger.write_text("[1, 2, 3]")  # valid JSON, non-dict
    with pytest.raises(SpendCapExceeded) as exc:
        cap.charge()
    assert exc.value.count == 0

    # FIX-2 (QA S1): an OSError on read (a directory in the ledger slot) is caught by the read-arm and
    # fails CLOSED — narrowing the `except (OSError, ValueError)` to just ValueError REDs this.
    as_dir = tmp_path / "as_dir"
    as_dir.mkdir()
    cap_dir = SpendCap(ledger_path=as_dir, ceiling=5, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    with pytest.raises(SpendCapExceeded) as exc:
        cap_dir.charge()
    assert exc.value.count == 0
    assert exc.value.cap == 5  # the fail-closed raise carries the real ceiling (F2)


@pytest.mark.parametrize("bad_value", [-1000000, -1, "abc", None, [1, 2], True])
def test_ac4c_value_corrupt_ledger_fails_closed(tmp_path, bad_value):
    """FIX-1/C3: a valid dict whose stored count is corrupt (negative / non-int / bool) fails CLOSED."""
    ledger = tmp_path / "ledger.json"
    key = _key(_TESTER, "2026-07")
    ledger.write_text(json.dumps({key: bad_value}))
    cap = SpendCap(ledger_path=ledger, ceiling=5, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    # a negative value would BYPASS the ceiling (fail-OPEN); a non-int would TypeError past the :314
    # catch — both fail CLOSED as a SpendCapExceeded instead.
    with pytest.raises(SpendCapExceeded) as exc:
        cap.charge()
    assert exc.value.count == 0
    assert exc.value.cap == 5
    # a fail-closed refusal never writes — the corrupt ledger is left untouched
    assert json.loads(ledger.read_text()) == {key: bad_value}


def test_ac4c_torn_write_leaves_prior_count(tmp_path, monkeypatch):
    """AC-4c: a persist failure at the atomic swap leaves the PRIOR count intact (atomic-write is load-bearing)."""
    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=10, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    key = _key(_TESTER, "2026-07")

    cap.charge()  # 1
    cap.charge()  # 2
    assert json.loads(ledger.read_text())[key] == 2

    def _raise_replace(*args, **kwargs):
        raise OSError("simulated crash at the atomic rename")

    monkeypatch.setattr(os, "replace", _raise_replace)
    try:
        cap.charge()  # the atomic swap fails; a bare-open mutant would have already overwritten in place
    except OSError:
        pass
    # the atomic write's temp is not os.replace'd on the failure -> the live ledger keeps the prior
    # count. A bare-`open('w')` mutant writes in place (no os.replace) -> the re-read shows 3 -> RED.
    assert json.loads(ledger.read_text())[key] == 2, "a persist failure corrupted/advanced the ledger"


# --- AC-5: the D2 wire-scan stays green with a cap injected + a spend_cap-scoped no-store AST check


def test_ac5_d2_scan_stays_green_with_cap_injected(tmp_path, monkeypatch):
    """AC-5: driving the metered dispatch WITH a cap injected keeps 0 store read + 0 outbound field."""
    ledger = tmp_path / "ledger.json"
    cap = SpendCap(ledger_path=ledger, ceiling=100, tester=_TESTER, clock=_fixed_clock("2026-07-16"))
    recorder, store_spy = _drive_metered(
        lambda c: metered_dispatch.build_dispatch(c, spend_cap=cap), _deid_summary(), monkeypatch
    )
    _assert_clean_metered_egress(recorder, store_spy)  # 0 raw-PII, 0 store-content, <= allowlist, 0 store reads


def test_ac5_structural_no_scripts_store_import():
    """AC-5/MF-2: spend_cap's imports reference no scripts.store symbol (a planted import would RED)."""
    tree = ast.parse(_SPEND_CAP_SOURCE.read_text(encoding="utf-8"))
    package_parts = ["scripts", "runner"]  # spend_cap.py's containing package
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                imported.append(node.module or "")
            else:
                anchor = package_parts[: max(0, len(package_parts) - (node.level - 1))]
                if node.module:
                    imported.append(".".join(anchor + [node.module]))
                else:
                    imported += [".".join(anchor + [alias.name]) for alias in node.names]
    store_imports = [m for m in imported if m == "scripts.store" or m.startswith("scripts.store.")]
    assert store_imports == [], f"spend_cap must import no scripts.store symbol: {store_imports}"


# --- AC-6: frozen-six untouched ------------------------------------------------------------------


def test_ac6_frozen_six_numstat_empty():
    """AC-6: the six byte-frozen ADR-0032 files are untouched vs the fork point (numstat empty)."""
    repo_root = Path(__file__).resolve().parents[2]
    frozen_six = [
        "scripts/store/store.py",
        "scripts/store/keying.py",
        "scripts/plan/pipeline.py",
        "scripts/plan/adjudicate.py",
        "scripts/plan/adjust.py",
        "scripts/plan/router.py",
    ]
    result = subprocess.run(
        ["git", "diff", "--numstat", "3ab1c3abb6c995fbaaadcb179735759e4a61d73d", "--", *frozen_six],
        cwd=repo_root, capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "", f"a frozen-six file was modified: {result.stdout!r}"
