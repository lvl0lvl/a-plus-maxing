"""Large-change HOLD: marker-before-exposure + tailoring-seam gate + debounce-counts-held (ADR-0040-T3).

T3 is the crown-jewel fail-closed surface: an unconfirmed materially-large swap must be NEITHER
standing NOR tailored/egressed, yet the debounce must keep COUNTING the held re-gen (it is the one
reader deliberately excluded from the pointer skip). On the large-change branch of
`plan_loop.regenerate`, T3 writes a `pending` `plan-confirm::<domain>` pointer (T1's `mark_pending`)
for EVERY promoted domain BEFORE the function returns, and excludes those held domains from the
post-promote tailoring seam's `promoted_plan`. Because T2 made `read_plan` / `horizons.window_block`
/ `tailoring.tailor` honor the pointer, the held re-gen then resolves `NO_PLAN_TODAY` end-to-end.

Every re-gen drives through the T1 front door (`plan_loop.regenerate` / `plan_loop.signal`) over a
fixture `dispatch` (`_LoopDispatch(_clean_authors())`) + a fixture de-id (`_FixedDeidClient`) + a
fixture `tailor_client` (`_EchoClient`) — 0 live-API calls, 0 real operator PII (synthetic tokens
only). Fixed dates keep the window/interval arithmetic deterministic.

  - AC-1: marker-before-exposure TEMPORAL guarantee (every `mark_pending` completed before
    `regenerate` returned; the caller's first read post-return resolves to the hold; an UNMARKED
    reading still STANDS — the window is closed by ORDER, not fail-closed resolution);
  - AC-2: the held re-gen is recorded in the raw store yet `read_plan` -> `NO_PLAN_TODAY` (not a
    walk-back to the prior confirmed plan);
  - AC-3: 0 held-plan surfacing in the 7- and 30-day `window_block`s (AR-002);
  - AC-4: `_post_promote_tailoring` receives the held domains ABSENT from its `promoted_plan`, and 0
    tailored artifact section is emitted for a held domain (HARD-AC, Decision §4);
  - AC-5: the byte-unchanged debounce COUNTS the held re-gen (no pending-over-pending storm), proven
    non-tautological by a mutation repointing `_last_regen_date` at `read_plan` (AR-003);
  - AC-6 [AMENDED 2026-07-05, 6-lens review]: the frozen-spine glob is numstat=0, `_last_regen_date`/
    `_prior_standing_plan` are byte-unchanged; the changed top-level defs are `regenerate`,
    `_change_magnitude` (materiality now filters via filter_confirmed — the HIGH fix), and
    `_post_promote_tailoring` (docstring records the T4 confirm-time caller).
"""

import ast
import functools
import subprocess
from pathlib import Path

from scripts.plan import horizons
from scripts.serve import plan_loop
from scripts.store import plan_confirm, plan_schema, store

# Loop fixtures mirrored from the existing loop component test (the recipe's convention).
from tests.serve.test_plan_loop import (
    _FixedDeidClient,
    _LoopDispatch,
    _SUSTAINED_DATES,
    _T4_PRIOR_DATE,
    _clean_authors,
    _deid_summary,
    _differing_prior,
    _new_dated_sets,
    _seed_biomarker,
    _seed_prior_standing,
    _seed_store,
)
# The tailoring artifact idioms (fixture presentation client + gitignored render seams, 0 spend).
from tests.plan.test_tailoring import _EchoClient, _gitignored_out, _synth_profile, TODAY

# A prior standing plan is seeded at `_T4_PRIOR_DATE` (2026-06-01); the re-gen writes `PLAN_DATE`
# rows, so the two never date-collide and every promoted domain replaces a differing standing plan
# -> a full 4-of-4 large change (>= LARGE_CHANGE_THRESHOLD_DOMAINS). A second-signal date sits inside
# the 7-day min-interval floor after the held re-gen.
PLAN_DATE = "2026-06-18"
WITHIN_INTERVAL_DATE = "2026-06-20"  # 2 days after PLAN_DATE (< MIN_REGEN_INTERVAL_DAYS)

_FROZEN_GLOB = (
    "scripts/plan/orchestrate.py scripts/plan/pipeline.py scripts/plan/assemble.py "
    # scripts/plan/generate_plan.py CARVED OUT — ADR-0042/0041/0046/0043 operator-signed-off (HARD) superseded plan front door; guarded by tests/plan/test_generate_plan.py + core-capability-audit.sh + per-ADR numstat probes. Architect ruling docs/adr/.pipeline/frozen-guard-reconciliation-ruling.md §2, feature/comprehensive-plan-adr.
    "scripts/plan/adjudicate.py scripts/plan/adjust.py "
    "scripts/plan/track.py scripts/plan/plan_driver.py scripts/plan/plan_orchestrator.py "
    "scripts/store/keying.py scripts/store/store.py"
).split()


def _large_regen(root, *, plan_date=PLAN_DATE):
    """Seed a full 4-of-4 large change and drive one re-gen through the T1 front door; return result."""
    _seed_store(root)
    _seed_prior_standing(root, plan_schema.PLAN_DOMAINS)  # 4 differing standing plans -> large change
    return plan_loop.regenerate(
        root,
        dispatch=_LoopDispatch(_clean_authors()),
        deid_client=_FixedDeidClient(_deid_summary()),
        plan_date=plan_date,
    )


def _promoted(result):
    return [d for d, r in result["results"].items() if r.get("recorded")]


# --- AC-1: marker-before-exposure TEMPORAL guarantee (OQ-4) -------------------------


def test_marker_before_exposure_temporal(tmp_path, monkeypatch):
    # AC-1: on a large re-gen every promoted domain is marked `pending` BEFORE `regenerate` returns,
    # so no caller can ever observe the swap as standing. The guarantee is the caller-observable
    # ORDER, not a fail-closed resolver: an UNMARKED reading still stands (T2 backward-compat).
    root = tmp_path / "store"

    marked = []
    real_mark = plan_confirm.mark_pending

    def spy_mark(domain, plan_date, root_):
        marked.append((domain, plan_date))
        return real_mark(domain, plan_date, root_)

    monkeypatch.setattr(plan_confirm, "mark_pending", spy_mark)

    result = _large_regen(root)
    promoted = _promoted(result)
    assert set(promoted) == set(plan_schema.PLAN_DOMAINS), f"expected a full swap: {promoted}"

    # (a) every promoted domain marked pending exactly once, keyed on the re-gen date (held as a unit).
    assert sorted(d for d, _ in marked) == sorted(promoted), f"marker coverage: {marked}"
    assert all(pd == PLAN_DATE for _, pd in marked), f"markers not keyed on plan_date: {marked}"

    # (b) marker-before-return: on return the pending pointer EXISTS for every held domain (every
    #     mark_pending completed before regenerate returned — the happens-before guarantee).
    for domain in promoted:
        assert plan_confirm.decision_for(domain, PLAN_DATE, root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: no pending pointer on return (marker did not precede the return)"
        )

    # (c) no caller exposure: the first read a caller can do post-return resolves to the HOLD, never
    #     the swapped plan (the transient promote->marker window is closed BEFORE the return).
    for domain in promoted:
        standing = plan_schema.read_plan(domain, PLAN_DATE, root)
        assert standing["state"] == plan_schema.NO_PLAN_TODAY, f"{domain} swap stood: {standing}"
        assert standing["plan"] is None
        assert standing["plan_date"] != PLAN_DATE

    # (d) NON-fail-closed clause: an UNMARKED reading STILL stands — the prior standing plans (dated
    #     _T4_PRIOR_DATE, never marked) resolve normally. The window is closed by the marker ORDER,
    #     not by read_plan failing closed on an unmarked reading.
    for domain in plan_schema.PLAN_DOMAINS:
        prior = plan_schema.read_plan(domain, _T4_PRIOR_DATE, root)
        assert prior["state"] is None, f"{domain}: an unmarked reading did not stand (spurious hold)"
        assert prior["plan"] == _differing_prior(domain)


# --- AC-2: the held re-gen is recorded yet does NOT stand ---------------------------


def test_held_regen_recorded_but_does_not_stand(tmp_path):
    # AC-2: after the large re-gen, the frozen promote DID write the new plan (raw store), yet
    # read_plan HOLDS it -> NO_PLAN_TODAY, plan None, NOT the held date, NOT a walk-back.
    root = tmp_path / "store"
    _large_regen(root)
    for domain in plan_schema.PLAN_DOMAINS:
        rows = [r for r in store.read(f"plan::{domain}", root=root) if r["timepoint"] == PLAN_DATE]
        assert len(rows) == 1, f"{domain}: the frozen promote did not record the new plan: {rows}"

        standing = plan_schema.read_plan(domain, PLAN_DATE, root)
        assert standing["state"] == plan_schema.NO_PLAN_TODAY, f"{domain} stood the held swap: {standing}"
        assert standing["plan"] is None, f"{domain}: a held/walk-back plan surfaced: {standing['plan']}"
        assert standing["plan_date"] != PLAN_DATE, f"{domain}: the held date stood: {standing}"


# --- AC-3: 0 held-plan surfacing in the horizon windows (AR-002) --------------------


def test_zero_horizon_surfacing(tmp_path):
    # AC-3: neither the 7-day nor the 30-day window_block surfaces the held plan for any held domain
    # (the prior CONFIRMED in-window block or None may return, but never the held plan_date).
    root = tmp_path / "store"
    _large_regen(root)
    for domain in plan_schema.PLAN_DOMAINS:
        for span in (7, 30):
            block = horizons.window_block(domain, root, PLAN_DATE, span)
            assert block is None or block["plan_date"] != PLAN_DATE, (
                f"{domain} span {span}: the held plan surfaced in the window block: {block}"
            )


# --- AC-5: the byte-unchanged debounce COUNTS the held re-gen (AR-003) --------------


def test_debounce_counts_held_regen(tmp_path):
    # AC-5 (preservation): the byte-unchanged _last_regen_date reads plan:: DIRECTLY via resolve_plan
    # (NOT read_plan), so it COUNTS the held re-gen -> no pending-over-pending storm. A second signal
    # inside the min-interval fires NO re-gen. (Non-tautology is proven by the mutation control below.)
    root = tmp_path / "store"
    _large_regen(root)
    _seed_biomarker(root, "hrv", [40, 50, 60], _SUSTAINED_DATES)  # sustained improving signal present
    store_read = functools.partial(store.read, root=root)

    assert plan_loop._last_regen_date(store_read, WITHIN_INTERVAL_DATE) == PLAN_DATE, (
        "the debounce did not count the held re-gen (last-re-gen != the held date)"
    )

    plan_loop.signal(
        root, trigger=plan_loop.DATA_EVENT_TRIGGER,
        dispatch=_LoopDispatch(_clean_authors()),
        deid_client=_FixedDeidClient(_deid_summary()), plan_date=WITHIN_INTERVAL_DATE,
    )
    assert _new_dated_sets(root, WITHIN_INTERVAL_DATE) == 0, (
        "a second re-gen fired inside the min-interval (the held re-gen stopped counting)"
    )


def test_debounce_mutation_repoint_at_read_plan_refires(tmp_path, monkeypatch):
    # AC-5 (mutation control — the RED for the preservation guard): repointing _last_regen_date at
    # read_plan makes the held (pending) re-gen fall out of the last-re-gen read, so the debounce
    # STOPS counting it and a second re-gen storms within the interval. A green here proves the
    # byte-unchanged direct-resolve_plan read (which ignores the pointer) is what suppresses the storm.
    root = tmp_path / "store"
    _large_regen(root)
    _seed_biomarker(root, "hrv", [40, 50, 60], _SUSTAINED_DATES)

    def _regen_date_via_read_plan(store_read, on_date):
        dates = [
            plan_schema.read_plan(d, on_date, root)["plan_date"]
            for d in plan_schema.PLAN_DOMAINS
        ]
        dates = [d for d in dates if d is not None]
        return max(dates) if dates else None

    monkeypatch.setattr(plan_loop, "_last_regen_date", _regen_date_via_read_plan)

    plan_loop.signal(
        root, trigger=plan_loop.DATA_EVENT_TRIGGER,
        dispatch=_LoopDispatch(_clean_authors()),
        deid_client=_FixedDeidClient(_deid_summary()), plan_date=WITHIN_INTERVAL_DATE,
    )
    assert _new_dated_sets(root, WITHIN_INTERVAL_DATE) == 1, (
        "under the read_plan-repoint mutation the held re-gen still counted (guard is tautological)"
    )


# --- AC-4: the tailoring seam excludes the held domains (HARD-AC, Decision §4) ------


def test_large_regen_gates_held_from_tailoring_seam(tmp_path, monkeypatch):
    # AC-4: a large re-gen calls _post_promote_tailoring with the held domains ABSENT from its
    # promoted_plan (spy the argument), and the maintained artifact carries NO tailored section for a
    # held domain. Falsification: before the gate the seam receives the FULL promoted set (held
    # present) -> the spy sees held domains -> RED. A fixture _EchoClient + gitignored render seams
    # forward the SAME call regenerate makes (0 live spend); on a full hold the held set = the whole
    # promoted set, so the gated promoted_plan is empty.
    root = tmp_path / "store"
    repo, out = _gitignored_out(tmp_path)
    seams = {"out_dir": out, "_today": TODAY,
             "_profile_paths": _synth_profile(tmp_path), "_repo_root": repo}

    seen = []
    real_seam = plan_loop._post_promote_tailoring

    def spy_seam(promoted_plan, render_target, **kwargs):
        seen.append(set(promoted_plan))
        kwargs.pop("tailor_client", None)
        kwargs.pop("_tailor_seams", None)
        return real_seam(promoted_plan, render_target,
                         tailor_client=_EchoClient(), _tailor_seams=seams, **kwargs)

    monkeypatch.setattr(plan_loop, "_post_promote_tailoring", spy_seam)

    _large_regen(root)  # full 4-of-4 large change -> every promoted domain is held

    # (a) the seam fired once with EVERY held domain absent from promoted_plan (a full hold -> {}).
    assert seen == [set()], f"held domains reached the tailoring seam's promoted_plan: {seen}"
    # (b) end-to-end: 0 tailored artifact section for any held domain.
    art = out / "maintained.html"
    text = art.read_text(encoding="utf-8") if art.exists() else ""
    for domain in plan_schema.PLAN_DOMAINS:
        assert f"data-domain='{domain}'" not in text, f"held {domain} was shadow-tailored/egressed"


# --- FIX 1 (6-lens review, HIGH) + FIX 6 (OQ-6 supersede): materiality vs the last STANDING plan --

POST_INTERVAL_DATE = "2026-06-26"  # 8 days after PLAN_DATE (> MIN_REGEN_INTERVAL_DAYS)


def test_regen_re_deriving_held_content_is_held_again(tmp_path):
    # FIX 1 (HIGH): a held large re-gen (never confirmed) must NOT be the materiality baseline.
    # Setup: 4 differing prior standing plans @ _T4_PRIOR_DATE stand (no pointer); a large re-gen @
    # PLAN_DATE is HELD (every domain pending, never confirmed). A fresh re-gen @ POST_INTERVAL_DATE
    # re-derives the SAME content the held re-gen produced. Because _change_magnitude filters the prior
    # readings through filter_confirmed, the held PLAN_DATE reading is dropped and materiality is
    # measured vs the STANDING _T4_PRIOR_DATE plan (still differing) -> material -> HELD AGAIN.
    # MUTATION-PROOF: revert _change_magnitude to read raw and _prior_standing_plan picks the held
    # PLAN_DATE reading; the re-derived content reads 0 change, falls below threshold, and STANDS
    # unheld -> the asserts below go RED.
    root = tmp_path / "store"
    _large_regen(root)  # 4 differing priors stand; the PLAN_DATE re-gen is held (all domains pending)
    for domain in plan_schema.PLAN_DOMAINS:
        assert plan_confirm.decision_for(domain, PLAN_DATE, root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: precondition failed — the PLAN_DATE re-gen is not held"
        )

    # A fresh re-gen re-derives the SAME content (same _clean_authors) at a later date, via the T1
    # front door directly (regenerate never debounces; the debounce is signal's, tested separately).
    result = plan_loop.regenerate(
        root,
        dispatch=_LoopDispatch(_clean_authors()),
        deid_client=_FixedDeidClient(_deid_summary()),
        plan_date=POST_INTERVAL_DATE,
    )
    assert set(_promoted(result)) == set(plan_schema.PLAN_DOMAINS), f"the re-gen did not promote: {result}"

    # The re-derived re-gen is HELD AGAIN — materiality read the STANDING prior, not the never-confirmed one.
    for domain in plan_schema.PLAN_DOMAINS:
        assert plan_confirm.decision_for(domain, POST_INTERVAL_DATE, root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: the re-derived re-gen was not held (materiality read the never-confirmed baseline)"
        )
        standing = plan_schema.read_plan(domain, POST_INTERVAL_DATE, root)
        assert standing["state"] == plan_schema.NO_PLAN_TODAY, f"{domain}: a never-confirmed re-gen stood: {standing}"
        assert standing["plan"] is None, f"{domain}: a held/walk-back plan surfaced: {standing['plan']}"


def test_post_interval_regen_supersedes_pending_pointer(tmp_path):
    # FIX 6 (OQ-6, spec T3 AC-5 final clause): a re-gen that CLEARS the min-interval over a still-
    # `pending` domain SUPERSEDES the prior pending pointer with a FRESH mark_pending at the new date.
    # Two _large_regen calls > MIN_REGEN_INTERVAL_DAYS apart; the domains are still pending from the
    # first (never confirmed). The new-date pointer is a fresh PENDING and the new-date re-gen holds;
    # the prior pending pointer is untouched (proving a fresh mark at the new date, not a reuse).
    root = tmp_path / "store"
    _large_regen(root)  # first held re-gen @ PLAN_DATE
    assert (plan_loop._date_of(POST_INTERVAL_DATE) - plan_loop._date_of(PLAN_DATE)).days > \
        plan_loop.MIN_REGEN_INTERVAL_DAYS, "POST_INTERVAL_DATE must clear the min-interval"

    _large_regen(root, plan_date=POST_INTERVAL_DATE)  # second held re-gen; domains still pending from the first

    for domain in plan_schema.PLAN_DOMAINS:
        assert plan_confirm.decision_for(domain, POST_INTERVAL_DATE, root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: no fresh pending pointer at the superseding date (OQ-6 supersede)"
        )
        assert plan_confirm.decision_for(domain, PLAN_DATE, root) == plan_confirm.DECISION_PENDING, (
            f"{domain}: the prior pending pointer changed (supersede must be a fresh mark at the new date)"
        )
        standing = plan_schema.read_plan(domain, POST_INTERVAL_DATE, root)
        assert standing["state"] == plan_schema.NO_PLAN_TODAY, f"{domain}: the superseding re-gen stood: {standing}"
        assert standing["plan"] is None


# --- AC-6: frozen-spine numstat=0 + only `regenerate` changed -----------------------


def _repo_root():
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
    ).stdout.strip()


def _top_defs(text):
    """name -> exact source segment for every top-level def/class in a module's text."""
    tree = ast.parse(text)
    return {
        node.name: ast.get_source_segment(text, node)
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }


# The pre-ADR-0040-hold plan_loop.py baseline: the parent of the first ADR-0040-hold commit
# (`d8f10921` "hold large-change re-gen until confirm"), before the hold layer modified
# regenerate / _change_magnitude / _post_promote_tailoring. The non-vacuity "these defs DID
# change" guard pins against this FIXED pre-change SHA, not origin/main — once the ADR-0040
# build merged, origin/main caught up to the changed defs so `!= origin` self-invalidated
# (bead 2deg). Mirrors test_generate_plan.py's PRE_TASK_HEAD pattern.
PRE_TASK_HEAD = "300de2f1cd57e700194de0e20114a844299eab31"


def test_frozen_spine_and_only_regenerate_changed():
    # AC-6: the ADR-0032 write-path+engine glob is byte-frozen (numstat=0), and the ONLY top-level
    # def in plan_loop.py that changed vs origin/main is `regenerate` — so _last_regen_date /
    # _prior_standing_plan / _change_magnitude / _post_promote_tailoring are all byte-unchanged.
    repo = _repo_root()
    numstat = subprocess.run(
        ["git", "diff", "--numstat", "origin/main", "--", *_FROZEN_GLOB],
        capture_output=True, text=True, cwd=repo, check=True,
    ).stdout.strip()
    assert numstat == "", f"the frozen spine changed (numstat): {numstat!r}"

    current = _top_defs(Path(repo, "scripts/serve/plan_loop.py").read_text(encoding="utf-8"))
    origin = _top_defs(subprocess.run(
        ["git", "show", "origin/main:scripts/serve/plan_loop.py"],
        capture_output=True, text=True, cwd=repo, check=True,
    ).stdout)

    # [AMENDED 2026-07-05, 6-lens review] `regenerate` (the hold layer), `_change_magnitude` (the
    # materiality baseline now filters via filter_confirmed — the HIGH fix + its `root` call-site
    # change), and `_post_promote_tailoring` (docstring records the T4 confirm-time second caller) are
    # the ONLY changed defs. `_last_regen_date` (the debounce) and `_prior_standing_plan` stay
    # byte-unchanged.
    changed_defs = ("regenerate", "_change_magnitude", "_post_promote_tailoring")
    for name, src in origin.items():
        if name in changed_defs:
            continue
        assert current.get(name) == src, f"{name} changed vs origin/main (must be byte-unchanged)"
    for helper in ("_last_regen_date", "_prior_standing_plan"):
        assert current[helper] == origin[helper], f"{helper} is not byte-unchanged"
    # sanity (not vacuous): each changed def DID change vs the pinned PRE-ADR-0040 baseline,
    # NOT origin/main — origin caught up once the ADR-0040 build merged, so `!= origin` reads
    # empty and self-invalidates (bead 2deg). `.get` tolerates a def absent at the baseline
    # (would read as "changed").
    pretask = _top_defs(subprocess.run(
        ["git", "show", f"{PRE_TASK_HEAD}:scripts/serve/plan_loop.py"],
        capture_output=True, text=True, cwd=repo, check=True,
    ).stdout)
    for name in changed_defs:
        assert current[name] != pretask.get(name), \
            f"{name} did not change vs the pre-ADR-0040 baseline (fix not applied)"
