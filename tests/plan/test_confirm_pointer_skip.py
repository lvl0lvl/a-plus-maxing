"""Standing-plan readers skip an unconfirmed reading (ADR-0040-T2, read-side pre-filter).

Every DIRECT `plan::<domain>` standing-plan reader must honor T1's `plan-confirm::`
pointer: a held (`pending`/`declined`-pointer) plan reading is dropped BEFORE the pure
resolve, so a held large re-gen resolves `NO_PLAN_TODAY` / no window block / no tailored
section — never the held plan, never a walk-back. The complete resolver set (ADR-0040
Consequences-Negative-2 completeness leak):

    AC-1  `plan_schema.read_plan`            — the single AR-007 read-side edit
    AC-2  `track.{resolve_plan_progress,record_tracking}` — covered TRANSITIVELY (0 edits)
    AC-3  `horizons.window_block`            — the AR-002 direct-scan SEPARATE falsifier
    AC-4  `tailoring.tailor` emit-gate       — the care-lane emit-gate
    AC-5  no-pointer / confirmed reading STANDS (backward-compat paired control)
    AC-6  frozen spine: WRITE-path + engine numstat=0; only plan_schema hunk = read_plan
    AC-7  `care_team_rollup.resolve_rollup` is a freshness read-model, NOT a resolver
          (pointer-agnostic paired control; care_team_rollup.py byte-unchanged)

`resolve_plan`'s date-equality body, the WRITE path, the engine, and `resolve_rollup`
stay byte-frozen — the filter is caller-side. Synthetic-only; 0 live model spend.
"""

import ast
import datetime
import json
import subprocess
from pathlib import Path

from scripts.plan import horizons, tailoring, track
from scripts.store import care_team_rollup, plan_confirm, plan_schema, store

# Repo root for the git-shell frozen-spine probe (tests/plan/<file> -> parents[2]).
REPO_ROOT = Path(__file__).resolve().parents[2]

# The ADR-0032 Validation-named WRITE-path + engine glob that must stay byte-frozen.
FROZEN_GLOB = (
    "scripts/plan/orchestrate.py", "scripts/plan/pipeline.py",
    # scripts/plan/assemble.py CARVED OUT — ADR-0041-T2 (uniform-program migration) superseded the assemble composer; behavioral guarantor tests/plan/test_assemble.py + tests/plan/test_generate_plan_uniform.py. Wave-2 frozen-guard reconciliation, Architect Option-A ruling.
    # scripts/plan/generate_plan.py CARVED OUT — ADR-0042/0041/0046/0043 operator-signed-off (HARD) superseded plan front door; guarded by tests/plan/test_generate_plan.py + core-capability-audit.sh + per-ADR numstat probes. Architect ruling docs/adr/.pipeline/frozen-guard-reconciliation-ruling.md §2, feature/comprehensive-plan-adr.
    "scripts/plan/adjudicate.py", "scripts/plan/adjust.py",
    "scripts/plan/track.py", "scripts/plan/plan_driver.py", "scripts/plan/plan_orchestrator.py",
    "scripts/store/keying.py", "scripts/store/store.py",
)

TODAY = datetime.date(2026, 6, 24)
TODAY_STR = "2026-06-24"
YESTERDAY_STR = "2026-06-23"
PRIOR_STR = "2026-06-21"  # in both the 7- and 30-day trailing windows ending 2026-06-24


def _workout_plan():
    return {"exercises": [{"name": "Squat", "sets": 5}]}


def _supp_plan():
    return {"items": [{"name": "Creatine", "dose": "5 g"}]}


def _seed_held(root, domain, plan, plan_date, specialist):
    """Record a `plan::<domain>` reading for `plan_date` and mark it `pending` (held)."""
    plan_schema.record_plan(domain, plan, plan_date, specialist, root)
    plan_confirm.mark_pending(domain, plan_date, root)


class _DetClient:
    """A deterministic presentation client (mirrors `ModelClient.converse`); 0 live spend."""

    def converse(self, messages):
        ctx = json.loads(messages[0]["content"])
        return {"reply": f"PERSONALIZED-{ctx['domain']}.", "extraction": []}


def _module_func_sources(source):
    """Map each top-level function name to its exact source segment (AC-6 hunk probe)."""
    tree = ast.parse(source)
    return {
        node.name: ast.get_source_segment(source, node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


# ===============================================================================
# Cycle 1: read_plan skip + transitive track.py coverage + backward-compat + freshness
# ===============================================================================


def test_read_plan_skips_held_not_walkback(tmp_path):
    # AC-1: a held (pending-pointer) reading dated today resolves NO_PLAN_TODAY (plan None,
    # plan_date != today) — excluded from the max(timepoint); a prior-dated plan does NOT
    # walk back to "today". The skip is caller-side: a direct resolve_plan still stands the
    # held plan (resolve_plan's body is byte-unchanged, the filter runs in read_plan).
    root = tmp_path
    plan_schema.record_plan("workout", _workout_plan(), YESTERDAY_STR, "coach", root)
    _seed_held(root, "workout", _workout_plan(), TODAY_STR, "coach")

    resolved = plan_schema.read_plan("workout", TODAY_STR, root)
    assert resolved["state"] == plan_schema.NO_PLAN_TODAY
    assert resolved["plan"] is None
    assert resolved["plan_date"] != TODAY_STR
    assert resolved["plan_date"] == YESTERDAY_STR  # latest ON FILE, no walk-back to today

    held = [r for r in store.read("plan::workout", root=root) if r["timepoint"] == TODAY_STR][0]
    direct = plan_schema.resolve_plan([held], TODAY_STR)
    assert direct["state"] is None and direct["plan"] == held["value"]


def test_track_transitive_skip_no_edit(tmp_path):
    # AC-2: track.py reaches the plan ONLY through read_plan, so read_plan's skip covers it
    # with 0 edits to track.py — resolve_plan_progress reports has_plan False and
    # record_tracking returns no-plan-to-track against a held plan.
    root = tmp_path
    _seed_held(root, "workout", _workout_plan(), TODAY_STR, "coach")

    progress = track.resolve_plan_progress("workout", TODAY_STR, root)
    assert progress["has_plan"] is False

    result = track.record_tracking("workout", {"sets_done": {"Squat": 3}}, TODAY_STR, root)
    assert result["state"] == track.NO_PLAN_TO_TRACK


def test_no_pointer_reading_stands(tmp_path):
    # AC-5 (backward-compat, paired control with AC-1): a no-pointer reading — and a
    # confirmed-pointer reading — resolve EXACTLY as pre-ADR (state None, plan present). If
    # the GREEN edit over-filters (drops a no-pointer reading), this goes red.
    root_np = tmp_path / "np"
    plan_schema.record_plan("workout", _workout_plan(), TODAY_STR, "coach", root_np)
    r_np = plan_schema.read_plan("workout", TODAY_STR, root_np)
    assert r_np["state"] is None and r_np["plan"] is not None

    root_c = tmp_path / "c"
    plan_schema.record_plan("workout", _workout_plan(), TODAY_STR, "coach", root_c)
    plan_confirm.mark_pending("workout", TODAY_STR, root_c)
    plan_confirm.set_decision("workout", TODAY_STR, plan_confirm.DECISION_CONFIRMED, root_c)
    r_c = plan_schema.read_plan("workout", TODAY_STR, root_c)
    assert r_c["state"] is None and r_c["plan"] is not None


def test_resolve_rollup_freshness_pointer_agnostic(tmp_path):
    # AC-7 (freshness paired control): resolve_rollup is a Zone-5 freshness read-model, NOT a
    # standing-plan resolver — it does NOT consult the pointer. A held (pending-pointer)
    # plan::workout dated today yields the SAME {state, days} for personal-trainer as a
    # no-pointer reading. If someone wrongly made the freshness reader pointer-aware, the
    # pointer-present == pointer-absent assertion goes red.
    root_held = tmp_path / "held"
    plan_schema.record_plan("workout", _workout_plan(), TODAY_STR, "coach", root_held)
    plan_confirm.mark_pending("workout", TODAY_STR, root_held)

    root_plain = tmp_path / "plain"
    plan_schema.record_plan("workout", _workout_plan(), TODAY_STR, "coach", root_plain)

    held_rollup = care_team_rollup.resolve_rollup(store.read_all(root_held), TODAY)
    plain_rollup = care_team_rollup.resolve_rollup(store.read_all(root_plain), TODAY)

    assert held_rollup["personal-trainer"]["state"] == "current"
    assert held_rollup["personal-trainer"] == plain_rollup["personal-trainer"]


# ===============================================================================
# Cycle 2: the other two direct plan:: readers — window_block (AR-002) + tailor emit-gate
# ===============================================================================


def test_window_block_skips_held_week_and_month(tmp_path):
    # AC-3 (AR-002, LOAD-BEARING, SEPARATE falsifier): window_block reads plan::<domain>
    # DIRECTLY and never calls resolve_plan/read_plan, so a read_plan-only fix leaves it
    # leaking. A held reading dated today (the max-timepoint in BOTH windows) must NEVER be
    # the block — the prior confirmed / no-pointer in-window reading is.
    root = tmp_path
    plan_schema.record_plan("workout", _workout_plan(), PRIOR_STR, "coach", root)
    _seed_held(root, "workout", _workout_plan(), TODAY_STR, "coach")

    week = horizons.window_block("workout", root, TODAY_STR, 7)
    month = horizons.window_block("workout", root, TODAY_STR, 30)
    assert week is not None and week["plan_date"] == PRIOR_STR
    assert month is not None and month["plan_date"] == PRIOR_STR


def test_tailor_emit_gate_skips_held(tmp_path, monkeypatch):
    # AC-4: tailor's emit-gate emits 0 tailored section for a held (pending-pointer) domain
    # even when it is in `promoted` (belt-and-suspenders with T3's seam gate); a co-present
    # non-held domain still tailors. The full emit-gate (promoted check -> filter_confirmed ->
    # resolve_plan state -> _present dispatch) runs as production; only the terminal render
    # sink is captured, so the assertion is on the emit-gate decision, not the HTML render.
    # Deterministic client -> 0 live spend.
    store_root = tmp_path / "store"
    _seed_held(store_root, "supplements", _supp_plan(), TODAY_STR, "supplement-specialist")
    plan_schema.record_plan("workout", _workout_plan(), TODAY_STR, "personal-trainer", store_root)

    captured = {}

    def _capture_reemit(*, root=None, tailored_sections=None, **kwargs):
        captured["sections"] = tailored_sections
        return Path(root)

    monkeypatch.setattr(tailoring.maintained, "reemit_maintained", _capture_reemit)

    tailoring.tailor(
        store_root, client=_DetClient(), care_profile_read=lambda: {"health_detail": {}},
        plan_date=TODAY_STR, promoted={"workout", "supplements"},
    )
    assert "workout" in captured["sections"], "the non-held domain failed to tailor"
    assert "supplements" not in captured["sections"], (
        "a HELD (pending-pointer) domain was tailored around the confirm gate"
    )


# ===============================================================================
# Cycle 3: frozen-spine guard — numstat=0 + plan_schema.py read_plan-only hunk (AC-6)
# ===============================================================================


def test_frozen_spine_numstat_and_read_plan_only_hunk():
    # AC-6 (AR-007): the ADR-0032 WRITE-path + engine glob is byte-frozen (0 changed lines vs
    # origin/main), care_team_rollup.py is byte-unchanged (pairs with AC-7), and the ONLY
    # plan_schema.py hunk is read_plan's pre-filter — the record-spine SURVIVORS correct_plan,
    # record_plan_tracking (which carry every store.append/store.correct caller line) are
    # byte-identical to the origin/main baseline. resolve_plan + record_plan are SANCTIONED-
    # SUPERSEDED by ADR-0044-T1 (plan-model record spine, scripts.store.plan_model), behavioral
    # guarantor tests/store/test_plan_model.py — carved from this freeze below.
    diff = subprocess.run(
        ["git", "diff", "--numstat", "origin/main", "--", *FROZEN_GLOB],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert diff.stdout.strip() == "", f"frozen WRITE-path/engine changed:\n{diff.stdout}"

    rollup = subprocess.run(
        ["git", "diff", "--numstat", "origin/main", "--", "scripts/store/care_team_rollup.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    assert rollup.stdout.strip() == "", f"care_team_rollup.py changed:\n{rollup.stdout}"

    baseline = subprocess.run(
        ["git", "show", "origin/main:scripts/store/plan_schema.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    current = (REPO_ROOT / "scripts/store/plan_schema.py").read_text(encoding="utf-8")
    base_funcs = _module_func_sources(baseline)
    cur_funcs = _module_func_sources(current)
    # resolve_plan + record_plan CARVED OUT — ADR-0044-T1 record-spine supersession (plan-model
    # record spine); behavioral guarantor tests/store/test_plan_model.py. Wave-2 frozen-guard
    # reconciliation, Architect Option-A ruling.
    for name in ("correct_plan", "record_plan_tracking"):
        assert base_funcs[name] == cur_funcs[name], (
            f"frozen plan_schema function {name!r} changed — only read_plan's hunk + the "
            "ADR-0044-T1 record-spine supersession are sanctioned"
        )
