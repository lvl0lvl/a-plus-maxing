"""The automated plan-evolution loop's front-door binding (ADR-0036-T1).

`regenerate(root, *, dispatch, deid_client, plan_date=None, trigger=None)` is the loop's ONE
entry into the FULL-COMPOSITION front door. It drives `plan_orchestrator.run_orchestrated`
with a REAL composed gate producer injected, so `run_orchestrated`'s `loop_enabled` path is
taken: the run enters the ONE shared driver (`plan_driver.drive`), composes the gate verdicts
via `gate_dispatch.compose_disposition`, applies the fail-closed `safety_passed is True` surface
gate, and runs the five `orchestrate` cross-domain holds (energy bounce, additive-AE,
cross-domain-conflict, Rx-BPMH, the medical-liaison adjudication gate).

The anti-degradation guard (the load-bearing deliverable): this module reaches the screened-only
single-press plan route on 0 paths, issues 0 bare cross-domain-reconciler calls that bypass the
driver, and references the per-domain re-plan leg on 0 paths — every evolved plan runs the SAME
composed safety gate + cross-domain reconciler the first plan ran, so a re-gen after the first can
never record un-reconciled (ADR-0036 finding-A safety parity). The guard is grep-checkable: this
module names none of those legs' symbols.

The loop is a SINGLE subscription-agent dispatch: ONE `dispatch` seam answers every agent class
(each plan-domain specialist, the quality judge, each safety lens), routed by its first argument.
`regenerate` composes the gate producer over that seam via `gate_dispatch.compose_gate_dispatch`
(the quality judge wrapped as `_JudgeClient`, the safety lenses dispatched directly — they share
the `(name, prompt, context)` call shape). It records nothing itself and opens no new store stream:
the inner engine's `record_plan`/promote is the only writer, so the driver's `SAFETY_BLOCKED` /
held-result outcome flows back to the caller untouched (a faithful pass-through — the loop adds no
bypass). Reasoning is the dispatched agents' (runtime A), never invented here.

Synthetic-only until real operator data is ingested (operator-gated): the raw plan-intake is the
current operator state read from `root`; the injected `deid_client` de-identifies it at the
crown-jewel `deid_in` boundary before any specialist dispatch.
"""

import datetime
import functools

from scripts.plan import plan_orchestrator, router, track
from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.store import biomarker_meta, plan_schema, store

# The judge role slug the loop dispatches the QUALITY gate through the unified subscription seam.
_JUDGE_ROLE = "quality-judge"

# The large-change advisory threshold (ADR-0036 OQ-4) — a fixed module constant a deterministic
# test reads, NOT a runtime default. Same pinned-number convention as the T2 debounce constants
# below. A re-gen replacing AT LEAST this many existing standing plans surfaces a large-change
# ADVISORY (a visibility notice — the swap already landed; NOT a hold). At `3` with a closed
# 4-domain universe the advisory fires on a 3-of-4 majority swap or a full 4-of-4 swap.
LARGE_CHANGE_THRESHOLD_DOMAINS = 3


class _JudgeClient:
    """Adapt the unified subscription dispatch into the quality gate's `.judge(payload)` seam.

    The quality gate calls `judge_client.judge(payload)`; the loop's ONE dispatch seam answers every
    agent class, so the judge is that seam addressed by `_JUDGE_ROLE`. This is the thin adapter that
    lets `compose_gate_dispatch` bind the judge to the same subscription dispatch the specialists +
    lenses use.

    Attributes:
        dispatch (Callable): The unified subscription-agent dispatch seam.
    """

    def __init__(self, dispatch):
        self.dispatch = dispatch

    def judge(self, payload):
        """Return the per-dimension score map by dispatching the quality judge over the seam."""
        return self.dispatch(_JUDGE_ROLE, "", payload)


def _read_raw_intake(root):
    """The current operator plan-intake the de-id boundary de-identifies (the loop re-reads live).

    The loop re-generates from the operator's CURRENT stored state, so the raw intake is that state
    read live from `root`. The crown-jewel `deid_in` boundary (inside `run_orchestrated`) de-identifies
    it through the injected `deid_client` before any specialist sees it — the loop hands the boundary
    the raw state, never a specialist.

    Args:
        root (str | Path): The store root.

    Returns:
        (dict) The raw operator plan-intake.
    """
    return {"operator_state": store.read_all(root)}


def regenerate(root, *, dispatch, deid_client, plan_date=None, trigger=None, tailor_client=None):
    """Drive the loop's re-gen through the full-composition front door and return the run result.

    Reads the current raw plan-intake for `root`, resolves `plan_date` to today's ISO date when
    `None`, composes the gate producer over the unified `dispatch` seam, and drives
    `plan_orchestrator.run_orchestrated` with that producer injected so the `loop_enabled` driver
    path is taken. Returns the `run_orchestrated` result unaltered (its recorded-survivors shape,
    or its honest-no-plan / `SAFETY_BLOCKED` shape). Never calls the screened-only route or the
    per-domain re-plan leg; never bypasses `plan_driver.drive`; records nothing itself.

    Args:
        root (str | Path): The store root the plans + the queue are recorded into.
        dispatch (Callable): The unified subscription-agent dispatch seam,
            `dispatch(name, prompt, context)` — a plan-domain name returns that domain's author
            envelope, `_JUDGE_ROLE` returns the quality score map, a safety-lens name returns that
            lens's findings. A real subscription agent in production; a fixture mock in tests.
        deid_client: The injected de-id model client for the crown-jewel `deid_in` boundary (a real
            `ModelClient`, or a fixture mock).
        plan_date (str, optional): The plans' YYYY-MM-DD date. `None` -> today's ISO date.
        trigger (str, optional): The cadence/manual trigger label (carried for the downstream
            debounce/rationale seams; not consumed here).
        tailor_client (optional): The care-lane presentation model client forwarded to the
            ADR-0037-T1 tailoring pass on the automated post-promote seam. `None` (the not-yet-wired
            production trigger site) leaves the seam a pass-through, mirroring the `signal`
            seams-unwired posture — no tailoring, 0 model spend.

    Returns:
        (dict) The `run_orchestrated` result (recorded survivors + reconciliation + dvq_entries),
        or its honest-no-plan / `SAFETY_BLOCKED` shape on a blocked/held run.

    Notes:
        Re-summarize per re-gen (ADR-0036-T3 finding B): `regenerate` re-reads the CURRENT store
        on every call (`_read_raw_intake` below) and re-enters `run_orchestrated`, so the de-id
        boundary re-derives `recent-trend-direction` from the LIVE `biomarker::` feed each re-gen
        — no stale summary is reused and the trend rides `router.summarize`, never a plan-history
        tracking-prefix bridge. Held-domain clearance is likewise re-derived by the `orchestrate` holds per re-gen
        (never inherited). Crown-jewel non-egress (finding C): the loop hands `deid_in` the raw
        intake and dispatches only the de-identified summary — a raw operator identifier / raw med
        never reaches a specialist payload, and a free-text trigger carries only its derived label.
        Pinned by `tests/serve/test_plan_loop_regen.py`.
    """
    plan_date = plan_date or datetime.date.today().isoformat()
    # Finding B: re-read the CURRENT store every re-gen so the de-id re-summarize re-derives the
    # trend from the live feed — never a cached/stale summary.
    raw_intake = _read_raw_intake(root)
    store_read = functools.partial(store.read, root=root)
    gate_producer = compose_gate_dispatch(_JudgeClient(dispatch), dispatch)
    result = plan_orchestrator.run_orchestrated(
        raw_intake, deid_client, dispatch, store_read, root,
        plan_date=plan_date, gate_dispatch=gate_producer,
    )
    # Post-promote seams (ADR-0036-T4): the re-gen rationale, the large-change ADVISORY notice, the
    # pass-through tailoring-hook seam, and the separate adherence input. Only a run that actually
    # PROMOTED has a standing plan to narrate, flag, tailor, or thread adherence into — a blocked/halt
    # run (SAFETY_BLOCKED / DEID_HALTED / cap) promoted nothing and passes straight through untouched.
    promoted = _promoted_domains(result)
    if not promoted:
        return result
    # AC-1: a non-empty plain-language what-changed rationale on every promoted re-gen.
    result["rationale"] = _compose_rationale(promoted, trigger)
    # AC-5: read adherence as a SEPARATE additional input, distinct from the trend (which the de-id
    # boundary re-derives via router.summarize). Absent adherence never blocks the trend-driven
    # re-gen — the re-gen already promoted.
    adherence = _read_adherence(root, plan_date)
    # AC-2/AC-3 (OQ-4): a re-gen that replaced at least the pinned number of existing standing plans
    # surfaces a large-change ADVISORY (a notice, not a hold). The new plan is ALREADY the standing
    # plan — the front-door promote inside `run_orchestrated` recorded it before this check runs — so
    # this only NOTES that a materially-large swap landed (changed domains + rationale) for operator
    # visibility. The true hold-until-confirm is the deferred follow-on ADR-0036-T4b. `>=` fires at 3
    # OR 4 of the 4 domains: a majority-of-domains swap is material enough to surface.
    if _change_magnitude(store_read, result, promoted, plan_date) >= LARGE_CHANGE_THRESHOLD_DOMAINS:
        from scripts.serve import confirm
        result["large_change"] = True
        result["large_change_advisory"] = confirm.confirm_large_change(
            promoted, rationale=result["rationale"])
    else:
        result["large_change"] = False
        result["large_change_advisory"] = None
    # AC-4: the post-promote tailoring-hook seam — fired exactly once per promoted re-gen with the
    # promoted plan set + the render target. ADR-0037-T1 fills it: on a threaded `tailor_client` the
    # care-lane tailoring pass runs once (else it stays a pass-through — the un-wired site).
    _post_promote_tailoring(
        {domain: result["results"][domain]["plan"] for domain in promoted},
        root, adherence=adherence, tailor_client=tailor_client, plan_date=plan_date,
    )
    return result


def _promoted_domains(result):
    """The domains this re-gen actually promoted (recorded a new plan for)."""
    return [domain for domain, r in (result.get("results") or {}).items() if r.get("recorded")]


def _compose_rationale(promoted, trigger):
    """A non-empty plain-language sentence describing what this re-gen changed (AC-1).

    Composed inline on the re-gen path (no helper module, no store key): names the trigger that
    fired the re-gen and the domains whose plan it refreshed. The plan REASONING stays the
    specialists' (runtime A) — this is a factual what-changed summary over the promoted set.

    Args:
        promoted (list): The domains this re-gen recorded a new plan for.
        trigger (str | None): The cadence/manual trigger label; None -> "scheduled".

    Returns:
        (str) A non-empty what-changed sentence.
    """
    kind = trigger or "scheduled"
    return f"Re-generated the plan ({kind} trigger); refreshed: {', '.join(sorted(promoted))}."


def _prior_standing_plan(readings, plan_date):
    """The plan value of the latest standing plan dated strictly BEFORE `plan_date`, or None."""
    prior_dates = [r["timepoint"] for r in readings if r["timepoint"] < plan_date]
    if not prior_dates:
        return None
    return plan_schema.resolve_plan(readings, max(prior_dates))["plan"]


def _change_magnitude(store_read, result, promoted, plan_date):
    """How many existing standing plans this re-gen replaces with different content (OQ-4 proxy).

    For each promoted domain, compares the newly-promoted plan against the domain's prior standing
    plan (the latest plan dated before `plan_date`). A domain with no prior standing plan is an
    establish, not a swap-over-standing, so it does not count; a domain whose new plan matches its
    prior standing plan is unchanged. The magnitude is the count of standing plans being replaced —
    breadth of change across domains, the materiality proxy the large-change advisory reads.

    Args:
        store_read (Callable): The instance-root-bound `store.read`.
        result (dict): The `run_orchestrated` result (its `results` carries each domain's new plan).
        promoted (list): The domains this re-gen promoted.
        plan_date (str): The re-gen's YYYY-MM-DD date.

    Returns:
        (int) The count of promoted domains whose prior standing plan is being replaced.
    """
    changed = 0
    for domain in promoted:
        prior = _prior_standing_plan(store_read(f"plan::{domain}"), plan_date)
        if prior is not None and result["results"][domain]["plan"] != prior:
            changed += 1
    return changed


def _read_adherence(root, on_date):
    """Read each tracked domain's plan-vs-actual progress as a SEPARATE adherence input (AC-5).

    Threads `track.resolve_plan_progress` into the re-gen as an additional input DISTINCT from the
    `recent-trend-direction` trend (which the de-id boundary re-derives via `router.summarize`, not a
    plan-history bridge). A pure READ of the existing plan/tracking streams — it defines no store key
    and appends nothing (ADR-0038 no-new-stream). Absent adherence is a value, not a block: a domain
    with no tracking snapshot reads `has_tracking=False`, and because the trend already arrives via
    `router.summarize`, the trend-driven re-gen ran unblocked regardless (OQ-5).

    Args:
        root (str | Path): The store root.
        on_date (str): The re-gen's YYYY-MM-DD date.

    Returns:
        (dict) domain -> the `resolve_plan_progress` plan-vs-actual view for each tracked domain.
    """
    return {domain: track.resolve_plan_progress(domain, on_date, root)
            for domain in plan_schema.TRACKED_DOMAINS}


def _post_promote_tailoring(promoted_plan, render_target, *, adherence=None,
                            tailor_client=None, plan_date=None):
    """Post-promote tailoring-hook seam — runs the ADR-0037-T1 care-lane tailoring pass once.

    Fired EXACTLY ONCE per promoted re-gen, AFTER the front-door promote, with the promoted plan set
    plus the render target (`generate.maintained.reemit_maintained`'s root) — plus the separate
    adherence input as a keyword extra. When a `tailor_client` is threaded it dispatches the care-lane
    tailoring pass (`tailoring.tailor`) once — the pass reads the operator's RAW `_care_profile`
    detail and renders the tailored sections ONLY into the gitignored maintained artifact. Absent the
    client (the not-yet-wired production trigger site) it stays a PASS-THROUGH, mirroring `signal`'s
    seams-unwired posture — 0 tailoring, 0 model spend. Change-control (build-plan multi-agent flag):
    the call shape (promoted plan + render target, once per re-gen) is a cross-task contract — a
    later edit changing it triggers an Architect contract-update notice.

    Args:
        promoted_plan (dict): domain -> the promoted plan value for each promoted domain.
        render_target (str | Path): The `reemit_maintained` root/artifact target.
        adherence (dict, optional): The separate plan-vs-actual adherence input (AC-5).
        tailor_client (optional): The care-lane presentation model client. None -> pass-through.
        plan_date (str, optional): The re-gen's YYYY-MM-DD date the tailoring emit-gate keys on.
    """
    if tailor_client is None:
        return None
    from scripts.plan import tailoring
    from scripts.serve import care_chat

    care_profile_read = functools.partial(
        care_chat._care_profile, functools.partial(store.read, root=render_target))
    tailoring.tailor(render_target, client=tailor_client,
                     care_profile_read=care_profile_read, plan_date=plan_date)
    return None


# --- ADR-0036-T2: the shared debounce gate + three-trigger convergence ----------------
#
# The three real trigger surfaces — a wearable/lab `biomarker::` write-event (route.py /
# confirm.py), the weekly cadence tick, and a care-chat free-text capture (care_chat.py) —
# converge on the ONE debounced entry `signal`, so no trigger reaches `regenerate` un-debounced.
# A whole-plan front-door re-gen is materially more expensive than a per-domain patch
# (ADR-0036 Consequences-Negative-1), so a re-gen fires only when the pinned min-interval has
# elapsed AND the `biomarker::` window carries a sustained directional signal. Every trigger kind —
# the free-text one included — is bound by the SAME 7-day min-interval floor; the derived date-only
# state cannot represent a finer per-trigger (sub-day) free-text clock without a new store stream,
# which ADR-0038 forbids, so the free-text trigger carries no independent sub-day bound. The debounce
# state introduces ZERO new store stream (OQ-5): the
# last-re-gen date is DERIVED from the dated `plan::` history via `plan_schema.resolve_plan`, and
# the window is a query over the existing `biomarker::` series via the router trend feed — no
# `loop::`/`debounce::`/`regen-marker::` item, no `store.append` of a marker.

# The trigger labels the three surfaces pass into the single debounced entry.
CADENCE_TRIGGER = "cadence"
DATA_EVENT_TRIGGER = "biomarker-write"
FREE_TEXT_TRIGGER = "free-text"

# Pinned debounce parameters (ADR-0036 OQ-1) — fixed module constants, not runtime defaults.
# The weekly floor between ANY two re-gens (aligns with the weekly cadence trigger, bounds the
# whole-plan re-gen cost, Consequences-Negative-1); derived from the dated `plan::` history.
MIN_REGEN_INTERVAL_DAYS = 7
# The sustained window's minimum readings — REUSES the existing honest-absence n>=3 guardrail
# (`biomarker_meta.PROJECTION_MIN_TIMEPOINTS`), one constant with one home, never a second literal.
SUSTAINED_WINDOW_MIN_READINGS = biomarker_meta.PROJECTION_MIN_TIMEPOINTS
# The >= n readings must span at least this many days to count as sustained (not a same-day cluster).
SUSTAINED_WINDOW_SPAN_DAYS = 7
# The directional-consistency bar: a qualifying stream's per-stream registered-polarity trend
# (`router._trend_token`) must be one of these — a real directional signal, not `flat`.
SUSTAINED_TREND_DIRECTIONS = ("improving", "regressing")


def _date_of(timepoint):
    """The calendar date of a store timepoint (a date-only or a full-ISO string)."""
    return datetime.date.fromisoformat(str(timepoint).split("T", 1)[0])


def _last_regen_date(store_read, on_date):
    """The latest on-file `plan::` date across `PLAN_DOMAINS` — the derived last-re-gen date, or None.

    Reads each domain's `plan::<domain>` series through `plan_schema.resolve_plan` (the dated read):
    a domain with a plan resolves to its plan date, the max of which is the last time ANY plan was
    generated. Zero on-file plans resolve to None (no prior re-gen to debounce against).
    """
    dates = []
    for domain in plan_schema.PLAN_DOMAINS:
        resolved = plan_schema.resolve_plan(store_read(f"plan::{domain}"), on_date)
        if resolved["plan_date"] is not None:
            dates.append(resolved["plan_date"])
    return max(dates) if dates else None


def _sustained_signal(store_read):
    """Whether a SINGLE `biomarker::` stream carries a sustained directional signal.

    Both conjuncts are tied to the SAME stream over its SAME recent window (the trailing
    `SUSTAINED_WINDOW_MIN_READINGS` readings): a stream qualifies only when, over that recent window,
    it (a) carries >= `SUSTAINED_WINDOW_MIN_READINGS` distinct timepoints spanning >=
    `SUSTAINED_WINDOW_SPAN_DAYS` (a sustained series, never a single reading, a same-day cluster, or an
    ancient anchor + a recent pair) AND (b) shows a directional trend (`router._trend_token` over that
    one stream is one of `SUSTAINED_TREND_DIRECTIONS`, not `flat`). Worst-wins reduces over the
    per-stream verdicts — the gate fires only when some ONE stream satisfies BOTH over its own recent
    window, so a directional blip in one stream can never borrow a flat long series in another (the
    cross-stream false-fire). A single new reading fails (a) — the debounce holds.
    """
    for stream in router._POLARITY_FEED:
        readings = store_read(stream)
        dates = sorted({_date_of(r["timepoint"]) for r in readings})
        if len(dates) < SUSTAINED_WINDOW_MIN_READINGS:
            continue
        recent = dates[-SUSTAINED_WINDOW_MIN_READINGS:]
        if (recent[-1] - recent[0]).days < SUSTAINED_WINDOW_SPAN_DAYS:
            continue
        if router._trend_token(readings) in SUSTAINED_TREND_DIRECTIONS:
            return True
    return False


def _should_regenerate(store_read, *, on_date):
    """Whether the shared debounce gate passes — pure over the derived read state.

    True only when the min-interval has elapsed since the derived last-re-gen date AND the
    `biomarker::` window carries a sustained directional signal. The gate is trigger-agnostic: every
    trigger kind (the free-text one included) is bound by the SAME 7-day min-interval floor — the
    derived date-only state cannot express a finer sub-day free-text clock without a new store stream
    (ADR-0038 forbids one), so there is no independent free-text bound. Reads state — never writes.
    """
    last = _last_regen_date(store_read, on_date)
    if last is not None:
        elapsed_days = (_date_of(on_date) - _date_of(last)).days
        if elapsed_days < MIN_REGEN_INTERVAL_DAYS:
            return False
    return _sustained_signal(store_read)


def signal(root, *, trigger, dispatch=None, deid_client=None, plan_date=None, tailor_client=None):
    """The ONE debounced entry every trigger kind calls; re-generate only when the gate passes.

    Runs the shared debounce predicate over DERIVED state (last-re-gen date from the dated `plan::`
    history; sustained-signal window over the `biomarker::` series). On pass it invokes T1's
    `regenerate(...)` exactly once and returns its re-gen receipt — it NEVER bypasses `regenerate`
    (the T1 front-door binding stays the sole path to the driver) and NEVER writes a store record.
    On a cadence trigger with no window signal it returns a hold+prompt payload (a `log_prompt` flag,
    0 new plans). On a debounced drop (inside window / inside min interval) it returns a no-op receipt
    with 0 new plans. The production server->trigger-site threading
    of the loop `dispatch`/`deid_client` seams is ADR-0036-T4; absent seams, a gate-pass is a no-op
    (`seams-unwired`) rather than a bare re-gen — the trigger sites notify additively either way.

    Args:
        root (str | Path): The store root the derived state is read from and the re-gen records into.
        trigger (str): The trigger label — `CADENCE_TRIGGER`, `DATA_EVENT_TRIGGER`, or
            `FREE_TEXT_TRIGGER`.
        dispatch (Callable, optional): The unified subscription-agent dispatch seam forwarded to
            `regenerate` on a gate-pass. None at a not-yet-wired production trigger site.
        deid_client (optional): The de-id model client forwarded to `regenerate`. None as above.
        plan_date (str, optional): The plans' YYYY-MM-DD date. None -> today's ISO date.
        tailor_client (optional): The care-lane presentation model client forwarded to `regenerate`
            for the ADR-0037-T1 post-promote tailoring pass. None at a not-yet-wired trigger site.

    Returns:
        (dict) The `regenerate` result on a gate-pass with seams present, else a no-op / hold+prompt
        receipt: `{"regenerated": bool, "log_prompt": bool, "trigger": str, "reason": str}`.
    """
    plan_date = plan_date or datetime.date.today().isoformat()
    root = root if root is not None else store.DEFAULT_ROOT
    store_read = functools.partial(store.read, root=root)
    if _should_regenerate(store_read, on_date=plan_date):
        if dispatch is not None and deid_client is not None:
            return regenerate(root, dispatch=dispatch, deid_client=deid_client,
                              plan_date=plan_date, trigger=trigger, tailor_client=tailor_client)
        return {"regenerated": False, "log_prompt": False, "trigger": trigger,
                "reason": "seams-unwired"}
    if trigger == CADENCE_TRIGGER and not _sustained_signal(store_read):
        return {"regenerated": False, "log_prompt": True, "trigger": trigger,
                "reason": "absent-signal-hold"}
    return {"regenerated": False, "log_prompt": False, "trigger": trigger, "reason": "debounced"}
