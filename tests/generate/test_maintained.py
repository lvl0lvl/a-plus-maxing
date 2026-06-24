"""Tests for the unified maintained-HTML output (ADR-0025-T1).

The maintained re-emit lifecycle (`scripts/generate/maintained.py`) RE-EMITS one
living plan artifact as new data arrives: it renders the de-identified report FIRST
(`render.emit` content path), runs the deterministic name-fill (`reinsert_out`) as
the FINAL pass, gates the name-bearing write behind a REALPATH-CONTAINMENT check
(the SEC-01 caller-precondition — the crown jewel), preserves prior content across
re-emits, folds the `track.resolve_plan_progress` plan-vs-actual view in as its OWN
section, and writes atomically (temp-then-rename).

No real operator PII enters this test tree: every identity token is the SYNTHETIC
`Janet Q Testperson` (mirroring the T0-SCANSCOPE hook fixture). The profile-source
seam (`_profile_paths`) points both the report header read and `reinsert_out` at a
fixture under `tmp_path`, never the real `vault/meta/operator-profile.md`.
"""

import datetime
import os
import subprocess
from pathlib import Path

import pytest

from scripts.generate import maintained
from scripts.plan import reinsert_out, track
from scripts.store import plan_schema, store
from vault.design.templates import report

SYNTH_NAME = "Janet Q Testperson"
SYNTH_INITIALS = "JQT"
TODAY = datetime.date(2026, 6, 24)
ON_DATE = "2026-06-24"


# --- fixtures -------------------------------------------------------------------


def _synth_profile(tmp_path):
    """Write a synthetic gitignored operator profile and return its path tuple."""
    prof = tmp_path / "operator-profile.md"
    prof.write_text(f"# Operator Profile — {SYNTH_NAME}\n", encoding="utf-8")
    return (prof,)


def _gitignored_out(tmp_path):
    """Create a git repo whose out-dir is gitignored; return (repo_root, out_dir).

    `reinsert_out` re-inserts only when `git check-ignore <target>` exits 0, so the
    out-dir must be a real gitignored path inside a git repo for the name to land.
    """
    repo = tmp_path / "repo"
    out = repo / "vault" / "artifacts" / "generated"
    out.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("vault/artifacts/generated/\n", encoding="utf-8")
    return repo, out


def _workout_plan():
    return {"exercises": [{"name": "Squat", "sets": 3, "load": "185 lb", "reps": 8}]}


def _wk_tracking(**over):
    return {"elapsed_min": 45, "volume_lb": 5000, "sets_done": {"Squat": 3}, **over}


def _seed_plan(root, domain="workout", date=ON_DATE, plan=None, specialist="personal-trainer"):
    plan_schema.record_plan(domain, plan or _workout_plan(), date, specialist, root)


# ===============================================================================
# Cycle 1: format-then-fill order + crown-jewel 0-committed-PII (AC-6, AC-5, HIGH-1)
# ===============================================================================


def test_ac6_render_runs_before_fill_name_survives(tmp_path):
    """AC-6: render.emit runs FIRST, reinsert_out is the FINAL pass; the name survives."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"

    path = maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY,
        _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    written = Path(path).read_text(encoding="utf-8")
    # The re-inserted full name SURVIVES into the emitted artifact (not clobbered by a
    # later re-render). A fill-then-render order would drop it back to initials-only.
    assert SYNTH_NAME in written, "the re-inserted name did not survive the render-then-fill order"
    assert f"Patient {SYNTH_INITIALS} ·" not in written, "initials placeholder was not filled (fill ran before render, or not at all)"


def test_ac6_order_is_render_then_fill_not_reverse(tmp_path, monkeypatch):
    """AC-6: reinsert_out is invoked AFTER the content render, over the produced HTML."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    calls = []

    real_reinsert = reinsert_out.reinsert_out

    def spy(html, target_path, **kw):
        # The content render must already be present in the HTML reinsert_out receives —
        # i.e. reinsert_out is the FINAL pass over the produced HTML, not a pre-render step.
        calls.append("reinsert")
        assert "Patient" in html, "reinsert_out ran before the content render produced the header"
        return real_reinsert(html, target_path, **kw)

    monkeypatch.setattr(maintained.reinsert_out, "reinsert_out", spy)
    maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY,
        _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    assert calls == ["reinsert"], "reinsert_out was not the single final fill pass"


def test_ac5_name_bearing_artifact_under_gitignored_dir_hooks_deny(tmp_path):
    """AC-5 crown jewel: a name-bearing maintained render staged/pushed is DENIED by both hooks."""
    # Build an isolated temp git repo carrying a SYNTHETIC identity token (no real PII),
    # mirroring the T0-SCANSCOPE hook fixture. The maintained writer is the producer; the
    # hooks are the egress authority that 0 real-PII reaches any committed/pushed file.
    real_root = Path(__file__).resolve().parents[2]  # the live checkout: the pii_scan policy ships here
    commit_hook = real_root / ".claude" / "hooks" / "block-pii-commit.sh"
    push_hook = real_root / ".claude" / "hooks" / "pre-push-pii-scan.sh"

    repo = tmp_path / "repo"
    (repo / "vault" / "artifacts" / "generated").mkdir(parents=True)
    (repo / "vault" / "meta").mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    subprocess.run(["git", "checkout", "-q", "-b", "feat"], cwd=repo, check=True)
    (repo / ".gitignore").write_text(
        "vault/artifacts/generated/\nvault/meta/operator-identity.txt\nvault/meta/operator-contact.txt\n",
        encoding="utf-8",
    )
    (repo / "vault" / "meta" / "operator-identity.txt").write_text(f"{SYNTH_NAME}\n", encoding="utf-8")
    bd_stub = tmp_path / "bd.sh"
    bd_stub.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    bd_stub.chmod(0o755)
    subprocess.run(["git", "add", ".gitignore"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=repo, check=True)

    art = repo / "vault" / "artifacts" / "generated" / "plan.html"
    art.write_text(f"<html><body><h1>Plan for {SYNTH_NAME}</h1></body></html>\n", encoding="utf-8")

    # commit-time: force-stage (the dropzone is gitignored) then invoke block-pii-commit.sh
    subprocess.run(["git", "add", "-f", "vault/artifacts/generated/plan.html"], cwd=repo, check=True)
    import json
    commit_input = json.dumps({"tool_input": {"command": "git commit -m wip"}})
    proc = subprocess.run(
        ["bash", str(commit_hook)],
        input=commit_input, capture_output=True, text=True, cwd=repo,
        env={**os.environ,
             "BLOCK_PII_COMMIT_PROJECT_ROOT": str(repo),
             "BLOCK_PII_COMMIT_PII_SCAN_ROOT": str(real_root),
             "BLOCK_PII_COMMIT_BD_CMD": str(bd_stub)},
    )
    assert '"permissionDecision":"deny"' in proc.stdout, f"commit hook did not DENY the name-bearing artifact: {proc.stdout}"
    assert "vault/artifacts/generated/plan.html" in proc.stdout

    # push-time: commit the artifact, then invoke pre-push-pii-scan.sh over the push range
    subprocess.run(["git", "add", "-f", "vault/artifacts/generated/plan.html"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "name-bearing"], cwd=repo, check=True)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    push_input = f"refs/heads/feat {sha} refs/heads/feat {'0' * 40}\n"
    pproc = subprocess.run(
        ["bash", str(push_hook)],
        input=push_input, capture_output=True, text=True, cwd=repo,
        env={**os.environ, "PRE_PUSH_PII_SCAN_ROOT": str(real_root)},
    )
    assert pproc.returncode == 1, f"push hook did not DENY the name-bearing artifact (rc={pproc.returncode}): {pproc.stderr}"
    assert "vault/artifacts/generated/plan.html" in pproc.stderr


def test_ac5_writes_only_under_gitignored_out_dir(tmp_path):
    """AC-5: the name-bearing artifact lands ONLY under the gitignored out-dir."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    path = maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY,
        _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    resolved = os.path.realpath(path)
    assert resolved.startswith(os.path.realpath(out) + os.sep), "artifact wrote outside the gitignored out-dir"
    assert SYNTH_NAME in Path(path).read_text(encoding="utf-8")


# --- HIGH-1: crown-jewel symlink/traversal/non-contained containment (fail-closed) ----


def test_high1_refuses_symlink_escape_to_tracked_path(tmp_path):
    """HIGH-1: a symlink under the gitignored dir pointing at a TRACKED path is REFUSED.

    git check-ignore exits 0 on the symlink's lexical name (under the gitignored prefix),
    but os.path.realpath escapes to a tracked path — the name-bearing HTML would write
    THROUGH the symlink into a tracked file. The realpath-containment guard must refuse.
    """
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    # A TRACKED destination outside the gitignored dir.
    tracked = repo / "tracked.html"
    tracked_dir = tracked.parent
    # Plant the symlink-escape under the gitignored out-dir: its lexical name is under the
    # gitignored prefix, but its realpath target is the tracked file above.
    escape = out / "escape.html"
    escape.symlink_to(tracked)

    with pytest.raises(Exception) as exc:
        maintained.reemit_maintained(
            root=store_root, _out_dir=out, _today=TODAY,
            _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
            _target_override=escape,
        )
    assert "contain" in str(exc.value).lower() or "realpath" in str(exc.value).lower() or "refus" in str(exc.value).lower()
    # NEGATIVE assertion (E2E placement): 0 name-bearing artifacts at the tracked target.
    assert not tracked.exists() or SYNTH_NAME not in tracked.read_text(encoding="utf-8"), \
        "the name-bearing artifact wrote THROUGH the symlink into a tracked file"


def test_high1_refuses_dotdot_traversal_destination(tmp_path):
    """HIGH-1: a `..`-traversal destination escaping the gitignored root is REFUSED."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    traversal = out / ".." / ".." / "tracked.html"  # resolves OUTSIDE out/
    with pytest.raises(Exception):
        maintained.reemit_maintained(
            root=store_root, _out_dir=out, _today=TODAY,
            _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
            _target_override=traversal,
        )
    landed = (out / ".." / ".." / "tracked.html").resolve()
    assert not landed.exists(), "a `..`-traversal write was not refused"


def test_high1_refuses_non_contained_absolute_path(tmp_path):
    """HIGH-1: any non-contained absolute path outside the realpath root is REFUSED."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    outside = tmp_path / "outside.html"
    with pytest.raises(Exception):
        maintained.reemit_maintained(
            root=store_root, _out_dir=out, _today=TODAY,
            _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
            _target_override=outside,
        )
    assert not outside.exists(), "a non-contained absolute-path write was not refused"


def test_test02_equal_path_containment_branch_is_allowed(tmp_path):
    """TEST-02: the `real_target == real_root` branch of `_assert_contained` is ALLOWED (no raise).

    The containment check refuses only a target whose realpath is NEITHER the root NOR strictly
    under it. The degenerate equal-path case (`target` resolves to exactly `out_dir`) is the
    documented ALLOW branch — it must NOT raise. Pinned directly on `_assert_contained` so the
    branch has explicit coverage (it was previously exercised by no test).
    """
    repo, out = _gitignored_out(tmp_path)
    # target == out_dir: realpaths are equal -> the allow branch (no raise)
    maintained._assert_contained(out, out)


def test_sec01_refuses_symlinked_out_dir_root(tmp_path):
    """SEC-01: a SYMLINKED out_dir root is REFUSED independently of the target-containment check.

    A symlinked out_dir would let the realpath-containment check adopt the symlink's TARGET as the
    root and sanction a write outside the real gitignored tree (the `git check-ignore` /
    gitignored-prefix contract is on the lexical name, not the symlink target). `_assert_contained`
    must reject the symlinked root before resolving it. (A legitimate out-dir whose ANCESTOR is a
    symlink — macOS `/var`->`/private/var` — is unaffected: only the out_dir's own final component
    is checked, which `_gitignored_out`'s real dir is.)
    """
    repo, real_out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    # plant a symlink whose final component IS a symlink pointing at the real gitignored out-dir
    linked_out = repo / "vault" / "artifacts" / "linked_generated"
    linked_out.symlink_to(real_out)

    with pytest.raises(ValueError, match="symlink"):
        maintained.reemit_maintained(
            root=store_root, _out_dir=linked_out, _today=TODAY,
            _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
        )


# ===============================================================================
# Cycle 2: re-emit preserves prior content + folds tracking (AC-1, AC-3, AC-4)
# ===============================================================================


def _PRESERVED_OPEN():
    return "<div class='maintained-preserved'>"


def test_ac1_reemit_preserves_prior_annotation(tmp_path):
    """AC-1: a re-emit on a new data point preserves prior annotations (lost entries = 0)."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    profile = _synth_profile(tmp_path)
    target = out / "maintained.html"

    # First emit, then inject a prior annotation into the preserved container.
    maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
    )
    first = target.read_text(encoding="utf-8")
    annotation = "<p class='annot'>operator note: felt strong on squats</p>"
    injected = first.replace(_PRESERVED_OPEN(), _PRESERVED_OPEN() + annotation, 1)
    target.write_text(injected, encoding="utf-8")

    # A NEW data point arrives: record a plan so the re-emit content differs.
    _seed_plan(store_root)
    maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
    )
    reemitted = target.read_text(encoding="utf-8")
    # The prior annotation SURVIVES (a stateless regenerate would have dropped it).
    assert annotation in reemitted, "the prior annotation was lost across the re-emit (stateless regenerate)"
    # The new data point is present too.
    assert "Squat" in reemitted, "the new data point did not appear in the re-emit"


def test_ac3_tracking_folds_as_section_not_separate_file(tmp_path):
    """AC-3: the plan-vs-actual view folds in as a SECTION, not a separate file."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    profile = _synth_profile(tmp_path)

    _seed_plan(store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)

    path = maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
    )
    html = Path(path).read_text(encoding="utf-8")
    # The folded plan-vs-actual section is present IN the maintained artifact.
    assert "maintained-tracking" in html, "the tracking section did not fold into the maintained artifact"
    assert "Plan vs actual" in html
    assert "5200" in html, "the resolved tracking value did not render in the folded section"
    # NEGATIVE assertion (E2E placement): no separate one-off tracking artifact was emitted.
    other = [p for p in out.iterdir() if p.is_file() and p.name != "maintained.html"]
    assert other == [], f"the tracking surface emitted a separate file instead of folding in: {other}"


def test_ac3_fold_reads_resolve_plan_progress_directly(tmp_path, monkeypatch):
    """AC-3: the fold reads via track.resolve_plan_progress (the store-surface read), not a re-derived join."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    profile = _synth_profile(tmp_path)
    _seed_plan(store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)

    calls = []
    real = track.resolve_plan_progress

    def spy(domain, on_date, root):
        calls.append(domain)
        return real(domain, on_date, root)

    monkeypatch.setattr(maintained.track, "resolve_plan_progress", spy)
    maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
    )
    assert "workout" in calls, "the fold did not call track.resolve_plan_progress directly"


def test_ac4_atomic_reemit_leaves_no_partial_state(tmp_path):
    """AC-4: an injected mid-write failure leaves the prior-good artifact, never a partial."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    profile = _synth_profile(tmp_path)
    target = out / "maintained.html"

    # First good emit.
    maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
    )
    good = target.read_text(encoding="utf-8")
    assert SYNTH_NAME in good

    # Inject a mid-write failure on the re-emit: the artifact must remain the prior-good one.
    _seed_plan(store_root)
    with pytest.raises(RuntimeError):
        maintained.reemit_maintained(
            root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
            _fail_after_render=True,
        )
    after = target.read_text(encoding="utf-8")
    assert after == good, "an interrupted re-emit left a partial/divergent artifact (not the prior-good one)"
    # No stray temp sibling left behind.
    leftovers = [p.name for p in out.iterdir() if p.name.startswith("maintained.html.") and p.name.endswith(".tmp")]
    assert leftovers == [], f"a stray temp artifact was left after the failure: {leftovers}"


# --- TEST-01: the profile-paths override leaks no global side-effect (the finally restore) ---


def test_render_report_restores_profile_paths_no_global_leak(tmp_path):
    """TEST-01: a `_profile_paths` re-emit leaves `report._PROFILE_PATHS` unchanged afterward.

    `_render_report` overrides the module constant ONLY across its render and restores it in a
    finally — so a process-shared `report._PROFILE_PATHS` does NOT leak the synthetic test profile
    into other suites. Pins the finally restore: the constant is its pre-call value afterward.
    """
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    before = report._PROFILE_PATHS

    maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY,
        _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )

    assert report._PROFILE_PATHS == before, "the profile-paths override leaked a global side-effect"


def test_render_report_restores_profile_paths_even_when_render_raises(tmp_path, monkeypatch):
    """TEST-01 (the finally pin): the constant is restored even when `report.render` RAISES.

    Forces `report.render` to raise mid-render; the override must still be unwound by the finally.
    REDs if `_render_report`'s finally body is replaced with `pass` (the constant would stay
    pointed at the synthetic profile, leaking into every later suite sharing the process).
    """
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    before = report._PROFILE_PATHS

    def boom(*args, **kwargs):
        raise RuntimeError("injected render failure")

    monkeypatch.setattr(maintained.report, "render", boom)

    with pytest.raises(RuntimeError, match="injected render failure"):
        maintained.reemit_maintained(
            root=store_root, _out_dir=out, _today=TODAY,
            _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
        )

    assert report._PROFILE_PATHS == before, \
        "the profile-paths override was NOT restored when render raised (the finally is broken)"


# ===============================================================================
# Cycle 3: store-adversarial battery (bead `pka`) — AC-7
# The four required docs/checklists/store-adversarial-tests.md categories over the
# maintained.py store paths (track.resolve_plan_progress read + track.record_tracking write).
# ===============================================================================


def _nutrition_plan():
    return {
        "calorie_goal": 2800,
        "macros": {"protein": 180, "carbs": 300, "fat": 80},
        "meals": [{"name": "Breakfast", "contents": "eggs, oats", "kcal": 650}],
    }


def _render_fold_html(tmp_path, store_root, on_date=ON_DATE):
    """Re-emit the maintained artifact and return its folded HTML (the fold-under-test)."""
    out = tmp_path / f"x{on_date}" / "repo" / "vault" / "artifacts" / "generated"
    out.mkdir(parents=True)
    repo = tmp_path / f"x{on_date}" / "repo"
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("vault/artifacts/generated/\n", encoding="utf-8")
    return maintained.reemit_maintained(
        root=store_root, _out_dir=out,
        _today=datetime.date.fromisoformat(on_date),
        _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    ).read_text(encoding="utf-8")


def test_ac7_cross_stream_collision_domain_x_never_returns_y(tmp_path):
    """AC-7 cat-1: a domain-X fold never renders domain-Y's tracking (cross-stream isolation)."""
    store_root = tmp_path / "store"
    # workout plan+tracking with a SENTINEL value; nutrition plan+tracking with a DIFFERENT sentinel.
    _seed_plan(store_root, domain="workout", plan={"exercises": [{"name": "Squat", "sets": 3}]})
    _seed_plan(store_root, domain="nutrition", specialist="nutritionist", plan=_nutrition_plan())
    track.record_tracking("workout", _wk_tracking(volume_lb=7777), ON_DATE, store_root)
    track.record_tracking("nutrition", {"food_kcal": 9999}, ON_DATE, store_root)

    wk = track.resolve_plan_progress("workout", ON_DATE, store_root)
    nut = track.resolve_plan_progress("nutrition", ON_DATE, store_root)
    # The workout read carries ONLY workout's tracking value, never nutrition's.
    assert wk["tracking"]["volume_lb"] == 7777
    assert "food_kcal" not in wk["tracking"], "workout fold cross-read nutrition's tracking (stream collision)"
    assert nut["tracking"]["food_kcal"] == 9999
    assert "volume_lb" not in nut["tracking"], "nutrition fold cross-read workout's tracking (stream collision)"
    # And in the rendered fold: workout's value renders against workout, not nutrition.
    html = _render_fold_html(tmp_path, store_root)
    assert "7777" in html and "9999" in html


def test_ac7_store_level_both_distinct_same_day_persist(tmp_path):
    """AC-7 cat-2(a): two DISTINCT same-day snapshots BOTH persist at the store; identical re-entry adds 0."""
    store_root = tmp_path / "store"
    _seed_plan(store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5000), ON_DATE, store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5000), ON_DATE, store_root)  # identical -> no-op
    assert len(store.read("plan-track::workout", root=store_root)) == 1, "identical re-entry was not idempotent"
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)  # distinct -> persists
    assert len(store.read("plan-track::workout", root=store_root)) == 2, \
        "a distinct same-day snapshot was silently dropped at the store (the S41 safety-surface escape)"


def test_ac7_fold_level_latest_wins_and_idempotent(tmp_path):
    """AC-7 cat-2(b): the fold renders the LATEST-wins snapshot (not both); identical re-entry is a no-op."""
    store_root = tmp_path / "store"
    _seed_plan(store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5000), ON_DATE, store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)  # latest

    prog = track.resolve_plan_progress("workout", ON_DATE, store_root)
    assert prog["tracking"]["volume_lb"] == 5200, "the fold read did not return the latest-wins snapshot"

    html = _render_fold_html(tmp_path, store_root)
    assert "5200" in html, "the fold did not render the latest-wins snapshot"
    assert "5000" not in html.split("maintained-tracking", 1)[1], \
        "the fold rendered a stale (non-latest) snapshot, or a merged both-snapshots view"

    # An identical re-entry of the latest is an idempotent no-op (no third store line).
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)
    assert len(store.read("plan-track::workout", root=store_root)) == 2


def test_ac7_dedupe_key_boundary_item_timepoint_source_value_excluded(tmp_path):
    """AC-7 cat-3: dedupe identity is (item, timepoint, source); value EXCLUDED; each field's contribution."""
    from scripts.store import keying
    assert keying.DEDUPE_FIELDS == ("item", "timepoint", "source"), "the dedupe identity changed"
    assert "value" not in keying.DEDUPE_FIELDS, "value must be EXCLUDED from the dedupe identity"

    store_root = tmp_path / "store"
    _seed_plan(store_root)
    # Same (item, timepoint) + same content-derived source + DIFFERENT value collides? No —
    # record_tracking's source is CONTENT-tagged, so a different value is a different source -> persists.
    track.record_tracking("workout", _wk_tracking(volume_lb=100), ON_DATE, store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=200), ON_DATE, store_root)  # different content -> new source
    assert len(store.read("plan-track::workout", root=store_root)) == 2, "differing content (source) did not persist"

    # A DIFFERENT timepoint (single field differing) does NOT collide -> a distinct line.
    _seed_plan(store_root, date="2026-06-25")
    track.record_tracking("workout", _wk_tracking(volume_lb=100), "2026-06-25", store_root)
    assert len(store.read("plan-track::workout", root=store_root)) == 3, "a differing timepoint collided"
    # A DIFFERENT item (domain) does NOT collide -> a separate stream.
    _seed_plan(store_root, domain="nutrition", specialist="nutritionist", plan=_nutrition_plan())
    track.record_tracking("nutrition", {"food_kcal": 100}, ON_DATE, store_root)
    assert len(store.read("plan-track::nutrition", root=store_root)) == 1, "a differing item collided across streams"


def test_ac7_mutation_observed_red_then_reverted(tmp_path, monkeypatch):
    """AC-7 cat-4: a deliberate keying mutation makes a battery assertion go RED (non-tautological).

    Mutate the store dedupe identity to DROP `source` (collapse the key to `(item, timepoint)`).
    Under the mutation two DISTINCT same-day snapshots — which the store-level-both-persist
    guarantee requires to BOTH persist (their content-tagged sources keep them distinct) — now
    collide on the source-less key and the second silently overwrites the first (the S41
    dropped-entry safety-surface escape). Observed RED here, then reverted by monkeypatch
    teardown (test_ac7_store_level_both_distinct_same_day_persist re-proves GREEN with the real
    key) — proving the battery is not green-by-construction.
    """
    from scripts.store import store as store_mod

    store_root = tmp_path / "store"
    _seed_plan(store_root)

    # MUTATION: drop `source` from the dedupe identity (the stream/content distinguisher).
    monkeypatch.setattr(
        store_mod.keying, "dedupe_key",
        lambda reading: (reading["item"], reading["timepoint"]),  # source EXCLUDED -> distinct snapshots collide
    )
    track.record_tracking("workout", _wk_tracking(volume_lb=5000), ON_DATE, store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)  # DISTINCT content
    persisted = len(store.read("plan-track::workout", root=store_root))
    # The store-level-both-persist invariant the battery rests on goes RED: under the mutation the
    # two distinct same-day snapshots collapse to 1 (a dropped entry), not 2.
    assert persisted == 1, (
        "EXPECTED the source-dropped key to collapse two distinct snapshots to 1 (the mutation must bite); "
        f"got {persisted} — the mutation did not change the store's keying"
    )
    # monkeypatch auto-reverts on teardown; the real (item, timepoint, source) key restores both-persist.


def test_ac7_mutation_revert_restores_green(tmp_path):
    """AC-7 cat-4 (revert proof): with the real keying, both distinct same-day snapshots persist again."""
    store_root = tmp_path / "store"
    _seed_plan(store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5000), ON_DATE, store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)  # DISTINCT content
    assert len(store.read("plan-track::workout", root=store_root)) == 2, \
        "the real (item, timepoint, source) key did not keep both distinct same-day snapshots (mutation not reverted)"


# ===============================================================================
# Cycle 4: single-file portability budget — AC-2
# ===============================================================================


def test_ac2_artifact_is_single_offline_file_under_500kb(tmp_path):
    """AC-2: each re-emit is one self-contained offline file, 0 external requests, < 500000 bytes."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    profile = _synth_profile(tmp_path)
    _seed_plan(store_root)
    track.record_tracking("workout", _wk_tracking(volume_lb=5200), ON_DATE, store_root)

    path = maintained.reemit_maintained(
        root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
    )
    # Single self-contained file: it IS one file, written, and present.
    assert Path(path).is_file()
    # < 500KB ceiling (ADR-0004 portability budget, inherited via render.emit).
    size = Path(path).stat().st_size
    assert size < 500000, f"the maintained artifact exceeded the <500KB budget: {size} bytes"
    # 0 external asset references: render.emit raises on any external ref, so a clean emit means
    # 0 off-file references. Re-scan the produced artifact to assert 0 external references survive.
    from scripts.generate.render import _external_references
    refs = _external_references(Path(path).read_text(encoding="utf-8"))
    assert refs == [], f"the maintained artifact carries external asset references: {refs}"


def test_ac2_external_reference_makes_emit_raise(tmp_path, monkeypatch):
    """AC-2: an external asset reference makes the render raise (0 file written) — budget enforced by render.emit."""
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    profile = _synth_profile(tmp_path)
    target = out / "maintained.html"

    # Inject an external <img src> into the assembled HTML: render.emit must raise (the budget gate).
    real_assemble = maintained._assemble_maintained

    def poisoned(*a, **k):
        return real_assemble(*a, **k).replace(
            "</body>", "<img src='https://evil.example/x.png'></body>", 1
        )

    monkeypatch.setattr(maintained, "_assemble_maintained", poisoned)
    with pytest.raises(ValueError, match="external asset reference"):
        maintained.reemit_maintained(
            root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
        )
    # 0 file written when the budget is violated.
    assert not target.exists(), "a network-dependent artifact was written despite the external reference"
    # BUG-03: the temp staging dir is auto-cleaned even when render.emit raises mid-render.
    staging = [p.name for p in out.iterdir() if p.name.startswith(".staging")]
    assert staging == [], f"a staging dir accreted after a render-budget raise: {staging}"


# --- BUG-03: the temp staging dir does not accrete across re-emits ---------------


def test_bug03_staging_dir_does_not_accrete_across_reemits(tmp_path):
    """BUG-03: each re-emit's staging dir is auto-cleaned — the out-dir holds only the artifact.

    The old fixed `out_dir/.staging` was created but never removed (only the staged FILE was
    unlinked), so the directory accreted. The temp-staging-dir fix leaves 0 `.staging*` entries.
    """
    repo, out = _gitignored_out(tmp_path)
    store_root = tmp_path / "store"
    profile = _synth_profile(tmp_path)

    for _ in range(3):
        _seed_plan(store_root)
        maintained.reemit_maintained(
            root=store_root, _out_dir=out, _today=TODAY, _profile_paths=profile, _repo_root=repo,
        )

    entries = sorted(p.name for p in out.iterdir())
    assert entries == ["maintained.html"], f"the out-dir accreted non-artifact entries: {entries}"
    staging = [n for n in entries if n.startswith(".staging")]
    assert staging == [], f"a staging dir accreted across re-emits: {staging}"
