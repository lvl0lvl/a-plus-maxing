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

from scripts.plan import plan_orchestrator, router, safety_review, track
from scripts.plan.gate_dispatch import compose_gate_dispatch
from scripts.store import biomarker_meta, plan_confirm, plan_schema, store

# The judge role slug the loop dispatches the QUALITY gate through the unified subscription seam.
# PUBLIC + shared (bead 3ge1 concern b): the `_JudgeClient` adapter + the loop tests read this ONE
# constant instead of re-declaring a coupled "quality-judge" literal; the forward-looking
# dispatch-seam consumers (T2/T3/T4) read it too when the production dispatch is wired.
JUDGE_ROLE = "quality-judge"

# The large-change HOLD bar (ADR-0036 OQ-4 → ADR-0040 → ADR-0046 disposition #36): a re-gen that
# replaces a STRICT MAJORITY of the ACTIVE RENDERABLE set is a materially-large swap ADR-0040 HOLDS
# `pending` (it does NOT stand and is not tailored/egressed) until an explicit operator confirm. The
# strict-majority DENOMINATOR is `|renderable|` (`active & RENDERABLE_DOMAINS`, the `renderable` local),
# NOT `|active|`: the numerator (`_change_magnitude`, the promoted standing-plan replacements) draws
# only from `renderable` and caps at 4, so a `len(active)` bar is structurally unreachable for
# `|active| ≥ 8` and would fail OPEN (the hold never fires; a full renderable swap stands unconfirmed).
# The fraction reproduces the retired fixed `3` on a 4-renderable surface (3-of-4 holds, 2-of-4 does
# not) while scaling DOWN for a narrowed renderable surface. This re-base is the HARD PRECONDITION
# before the ADR-0046 activation runs live against the SCALED 15+ card ROSTER — a fixed count-of-3 is a
# MINORITY of a grown roster and must never gate it (disposition #36 resolves external ADR-0040 OQ-2).
def _is_renderable_majority(changed_count, renderable_count):
    """Whether `changed_count` is a STRICT majority of `renderable_count` (the large-change hold bar).

    The hold fires when the promoted standing-plan replacement count (`_change_magnitude`, the
    numerator, ≤ `|renderable|` ≤ 4) is a STRICT majority of the active RENDERABLE-set size
    (`|renderable|`, the denominator). Strict — `> half`, i.e. `>= renderable_count // 2 + 1` — so an
    even-sized renderable set does NOT hold at its half-point (2-of-4 does not, 3-of-4 does),
    reproducing the retired constant's 3-of-4 boundary.

    Args:
        changed_count (int): The promoted domains replacing a differing prior standing plan.
        renderable_count (int): The active RENDERABLE-set size (`len(active & RENDERABLE_DOMAINS)`).

    Returns:
        (bool) True when `changed_count` is a strict majority of `renderable_count`.
    """
    return changed_count >= renderable_count // 2 + 1


def dispatch_route_collisions(specialists=None, judge=None, lenses=None):
    """Names shared across >=2 dispatch-seam route name-spaces — empty when the disjoint precondition holds.

    The dispatch-seam routing precondition (bead 3ge1 concern b): the unified
    `dispatch(name, prompt, context)` seam routes `name` over THREE name-spaces — a
    `plan_schema.PLAN_DOMAINS` specialist (returns its author envelope), `JUDGE_ROLE` (the quality
    score map), or a `safety_review.DEFAULT_LENSES` lens (that lens's findings). A production dispatch
    can route `name` unambiguously ONLY if the three are pairwise disjoint; any name shared across two
    of them would shadow one route. This predicate returns the offending overlap (a frozenset), empty
    when the precondition holds. The module ASSERTS it holds at import (below) so the precondition is
    runtime-enforced in every deployed build, not merely test-checked; a forward-looking dispatch-seam
    consumer (T2/T3/T4) can also call it to validate custom rosters. Defaults read the live rosters.

    Args:
        specialists (iterable, optional): The plan-domain specialist names; None -> `PLAN_DOMAINS`.
        judge (str, optional): The quality-judge role slug — a SINGLE slug, NOT an iterable (it is
            wrapped as one element; passing a tuple would report a false no-collision and a list would
            raise, since the two sibling params ARE iterables — mind the asymmetry); None -> `JUDGE_ROLE`.
        lenses (iterable, optional): The safety-lens names; None -> `safety_review.DEFAULT_LENSES`.

    Returns:
        (frozenset) The names present in two or more of the three name-spaces (empty = disjoint).
    """
    specialists = set(plan_schema.PLAN_DOMAINS if specialists is None else specialists)
    judge_set = {JUDGE_ROLE if judge is None else judge}
    lenses = set(safety_review.DEFAULT_LENSES if lenses is None else lenses)
    # Pairwise intersections — the house disjointness idiom (cf. router.py / orchestrate.py `&`).
    return frozenset((specialists & judge_set) | (specialists & lenses) | (judge_set & lenses))


# Runtime-enforce the dispatch-seam routing precondition at import (house pattern, cf. router.py's
# module-level disjointness asserts): the three route name-spaces MUST be pairwise disjoint or the
# unified `dispatch(name, ...)` seam cannot route unambiguously. A collision fails loud at import in
# every deployed build — stronger than a test-only check.
assert not dispatch_route_collisions(), (
    "dispatch-seam route name-spaces (PLAN_DOMAINS / JUDGE_ROLE / safety_review.DEFAULT_LENSES) "
    f"must be pairwise disjoint; collisions: {dispatch_route_collisions()}")


class _JudgeClient:
    """Adapt the unified subscription dispatch into the quality gate's `.judge(payload)` seam.

    The quality gate calls `judge_client.judge(payload)`; the loop's ONE dispatch seam answers every
    agent class, so the judge is that seam addressed by `JUDGE_ROLE`. This is the thin adapter that
    lets `compose_gate_dispatch` bind the judge to the same subscription dispatch the specialists +
    lenses use.

    Attributes:
        dispatch (Callable): The unified subscription-agent dispatch seam.
    """

    def __init__(self, dispatch):
        self.dispatch = dispatch

    def judge(self, payload):
        """Return the per-dimension score map by dispatching the quality judge over the seam."""
        return self.dispatch(JUDGE_ROLE, "", payload)


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


# Summary fields whose PRESENCE signals activity in a specific card domain (RULING 2). The coarse
# chat-sourced rich-domain band tokens (ADR-0019-T1) are CLASS values, not domain slugs — so their
# PRESENCE in the de-id summary maps to the corresponding card domain (a stated diet -> nutrition,
# a supplement stack -> supplements, a peptide-use band -> peptides, a training-volume band ->
# workout). Goal / issue / genetic-trait fields carry card slugs directly (filtered).
_FIELD_PRESENCE_DOMAIN = {
    "dietary-pattern-class": "nutrition",
    "supplement-stack-class": "supplements",
    "peptide-use-class": "peptides",
    "training-volume-band": "workout",
}

# Band-field values that signal NO active use (so they do NOT activate their domain): the documented
# `router` absent sentinel (`not-discussed`) and a confirmed-none. A real coarse class value ("omnivore",
# a supplement-stack class, …) DOES activate its domain.
_INACTIVE_BAND_VALUES = frozenset({router._NOT_DISCUSSED, "none", ""})


def _surface_tokens(value):
    """Tokenize a de-id summary field value (str or iterable) into candidate card-domain slugs."""
    if value is None:
        return []
    if isinstance(value, str):
        return value.replace(",", " ").split()
    if isinstance(value, (list, tuple, set)):
        return [str(token) for token in value]
    return []


def derive_operator_surface(summary):
    """Project the ALREADY-de-identified summary into the `activation` surface (RULING 2, crown-jewel).

    The front-door helper `active_domains` had no surface constructor — this is it. It PROJECTS the
    post-de-id summary (`router.summarize` / `deid_in` output) into the four `activation` channels
    (`goals` / `data` / `mentions` / `lab_or_trait_touches`), each an iterable of card-domain slugs:
    `goals` from `goal-domains`, `mentions` from the coarse rich-domain band-field PRESENCE + a card
    slug named in `active-issue-class`, `lab_or_trait_touches` from the coarse `genetic-trait-classes`
    tokens. It originates NO new operator-state source — a pure projection of what the assembled /
    de-identified context already holds.

    DE-ID-SAFE by construction (the LOAD-BEARING crown-jewel boundary): it consumes the post-de-id
    `summary` ONLY (never the raw intake), and every channel value is FILTERED to
    `activation.CARD_DOMAINS ∪ activation.CROSS_CUTTING_INPUTS` (card slugs / coarse tokens only) — so
    a raw operator identifier, a raw med free-text, or a raw genotype structurally cannot enter the
    surface (ADR-0032 genetics crown jewel: only the coarse de-id trait-CLASS token can touch
    `lab_or_trait_touches`, never a raw allele).

    Args:
        summary (Mapping): The post-de-id operator summary (`router.SUMMARY_FIELD_SET` fields).

    Returns:
        (dict) The `_SURFACE_CHANNELS` mapping `activation.active_domains` consumes.
    """
    from scripts.plan import activation

    known = set(activation.CARD_DOMAINS) | set(activation.CROSS_CUTTING_INPUTS)
    goals = {slug for slug in _surface_tokens(summary.get("goal-domains")) if slug in known}
    mentions = {slug for slug in _surface_tokens(summary.get("active-issue-class")) if slug in known}
    mentions |= {
        domain for field, domain in _FIELD_PRESENCE_DOMAIN.items()
        if str(summary.get(field) or "").strip().lower() not in _INACTIVE_BAND_VALUES
    }
    traits = {slug for slug in _surface_tokens(summary.get("genetic-trait-classes")) if slug in known}
    # `data` (tracked-stream presence) is not a summary field — the goals/mentions channels carry the
    # activation signal here; the deriver stays a pure summary projection (no store read).
    return {
        "goals": sorted(goals), "data": [],
        "mentions": sorted(mentions), "lab_or_trait_touches": sorted(traits),
    }


def active_plan_domains(summary):
    """The active card-emitting domains for the front door (RULING 2 + the renderable-core floor).

    `activation.active_domains(derive_operator_surface(summary))`, FLOORED at the renderable core four
    when the surface carries NO renderable-domain signal — the baseline plan (backward-compatible with
    the pre-growth always-four behavior). Progressive activation ADDS a rich domain when the surface
    signals it, and NARROWS the renderable subset only when the surface explicitly signals a proper
    renderable subset (AC-4 / AC-S2). The result never zeroes out an existing operator's plan.
    """
    from scripts.plan import activation

    active = set(activation.active_domains(derive_operator_surface(summary)))
    if not (active & set(plan_schema.RENDERABLE_DOMAINS)):
        active |= set(plan_schema.RENDERABLE_DOMAINS)
    return active


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
            envelope, `JUDGE_ROLE` returns the quality score map, a safety-lens name returns that
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
    # Leg 1 (OPTION 2 — the ADR-0028 composed safety gate PRESERVED, WRAPPED not retired): derive the
    # de-id-safe operator surface and NARROW the dispatched set to active ∩ the renderable roster; the
    # composed gate_dispatch is STILL injected so run_orchestrated's loop_enabled path (drive ->
    # compose_disposition -> the fail-closed safety_passed gate -> the five holds -> thin promote) runs
    # unchanged. `domains=` is an already-accepted run_orchestrated param — plan_orchestrator is NOT
    # edited. A rich domain active in the surface is folded in by Leg 2 (it never traverses the thin
    # renderable-validator path).
    summary = router.summarize(store_read)
    active = active_plan_domains(summary)
    renderable = tuple(sorted(active & set(plan_schema.RENDERABLE_DOMAINS)))
    gate_producer = compose_gate_dispatch(_JudgeClient(dispatch), dispatch)
    result = plan_orchestrator.run_orchestrated(
        raw_intake, deid_client, dispatch, store_read, root,
        plan_date=plan_date, domains=renderable, gate_dispatch=gate_producer,
    )
    # Post-promote seams (ADR-0036-T4): the re-gen rationale, the large-change ADVISORY notice, the
    # pass-through tailoring-hook seam, and the separate adherence input. Only a run that actually
    # PROMOTED has a standing plan to narrate, flag, tailor, or thread adherence into — a blocked/halt
    # run (SAFETY_BLOCKED / DEID_HALTED / cap) promoted nothing and passes straight through untouched.
    promoted = _promoted_domains(result)
    if not promoted:
        return result
    # AC-1: a non-empty plain-language what-changed rationale on every promoted re-gen. Computed
    # AHEAD of Leg 2 because the large-change advisory below reads it.
    result["rationale"] = _compose_rationale(promoted, trigger)
    # AC-5: read adherence as a SEPARATE additional input, distinct from the trend (which the de-id
    # boundary re-derives via router.summarize). Absent adherence never blocks the trend-driven
    # re-gen — the re-gen already promoted.
    adherence = _read_adherence(root, plan_date)
    # AC-2/AC-3 (OQ-4 → ADR-0040), W4-01: apply the materially-large HOLD BEFORE Leg 2. The hold
    # concerns the thin swap Leg 1 already RECORDED by the front-door promote inside `run_orchestrated`;
    # it does NOT depend on Leg 2, so running it first makes it fire REGARDLESS of Leg 2's outcome — a
    # Leg-2 raise can no longer skip it and leave a materially-large thin swap standing UNCONFIRMED
    # (the partial-write hole in AC-BP). The hold branch marks every promoted domain `pending` before
    # this function returns, so the read-side skip (T2) resolves it `NO_PLAN_TODAY` until an explicit
    # operator confirm; the `large_change_advisory` dict is the confirm-PROMPT payload (not a
    # swap-already-landed notice). Materiality is measured against the last STANDING (confirmed /
    # no-pointer) plan — `_change_magnitude` filters the prior readings through `filter_confirmed`, so a
    # never-confirmed held re-gen is not the baseline. The hold fires when the swap is a STRICT
    # MAJORITY of the active RENDERABLE set (`_is_renderable_majority` over `len(renderable)`, the
    # `renderable` local bound above) — a majority-of-renderable swap is material enough to hold.
    if _is_renderable_majority(
        _change_magnitude(store_read, result, promoted, plan_date, root), len(renderable)
    ):
        # ADR-0040 hold: the whole materially-large swap is held as a unit (OQ-3). Write a `pending`
        # pointer for EVERY promoted domain (not just the content-changed subset) BEFORE this function
        # returns, so a single-process caller can never observe the swap as standing — T2's readers
        # (read_plan / window_block / tailoring) then drop the held reading (NO_PLAN_TODAY end-to-end).
        for domain in promoted:
            plan_confirm.mark_pending(domain, plan_date, root)
        held = set(promoted)
        from scripts.serve import confirm
        result["large_change"] = True
        result["large_change_advisory"] = confirm.confirm_large_change(
            promoted, rationale=result["rationale"])
    else:
        held = set()
        result["large_change"] = False
        result["large_change_advisory"] = None
    # Leg 2 (OPTION 2 — ADDITIVE, gated by the pass): the `if not promoted` guard above IS the
    # SAFETY_BLOCKED boundary (on a block, promoted is empty and regenerate returned untouched — no
    # synthesis, no comprehensive record, the prior version stands, 0 partial write, AC-BP). Reaching
    # here ⟺ Leg 1's composed gate SURFACED a pass, so the care-agent synthesize step composes ONE
    # comprehensive plan version from the gate-cleared programs Leg 1 surfaced PLUS any active rich
    # domain (authored via the dispatch seam over the de-id summary, reconciled through the always-on
    # floors) and records it via plan_model.record_plan_version — ON TOP of Leg 1's KEPT thin write.
    # W4-01: the rich-author dispatch is ISOLATED (try/except -> None) so a transient rich dispatch
    # error degrades that domain to honest no-plan (Leg 1 stands), never propagating out of the loop —
    # mirroring the server twin's `_author_rich` (server.py).
    from scripts.serve import care_chat

    def _author_rich(domain):
        try:
            return dispatch(domain, "", summary)
        except Exception:
            return None

    care_chat.synthesize(
        active, result, _author_rich, store_read, on_date=plan_date, root=root,
    )
    # AC-4: the post-promote tailoring-hook seam — fired exactly once per promoted re-gen with the
    # promoted plan set + the render target. ADR-0037-T1 fills it: on a threaded `tailor_client` the
    # care-lane tailoring pass runs once (else it stays a pass-through — the un-wired site).
    # ADR-0040 deferred-tailoring seam: a HELD domain is excluded from the seam's promoted_plan so it
    # is never tailored/egressed during the hold (on a full large-change hold this narrows to {}). A
    # below-threshold re-gen has an empty held set, so the full promoted set reaches the seam unchanged.
    # T4's confirm fires the deferred tailoring once for the now-confirmed domain.
    _post_promote_tailoring(
        {domain: result["results"][domain]["plan"] for domain in promoted if domain not in held},
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


def _change_magnitude(store_read, result, promoted, plan_date, root):
    """How many existing STANDING plans this re-gen replaces with different content (OQ-4 proxy).

    For each promoted domain, compares the newly-promoted plan against the domain's prior STANDING
    plan (the latest CONFIRMED / no-pointer plan dated before `plan_date`). The prior readings are
    pre-filtered through `plan_confirm.filter_confirmed`, so a never-confirmed HELD re-gen (a
    `pending` pointer) is NOT the materiality baseline — without this a held large swap that a later
    re-gen re-derives identically would read 0 change and stand unheld (6-lens review, HIGH). A
    domain with no prior standing plan is an establish, not a swap-over-standing, so it does not
    count; a domain whose new plan matches its prior standing plan is unchanged. The magnitude is the
    count of standing plans being replaced — breadth of change across domains, the materiality proxy
    the large-change hold reads.

    Args:
        store_read (Callable): The instance-root-bound `store.read`.
        result (dict): The `run_orchestrated` result (its `results` carries each domain's new plan).
        promoted (list): The domains this re-gen promoted.
        plan_date (str): The re-gen's YYYY-MM-DD date.
        root (str | Path): The store root, forwarded to `filter_confirmed` for the pointer lookup.

    Returns:
        (int) The count of promoted domains whose prior standing plan is being replaced.
    """
    changed = 0
    for domain in promoted:
        confirmed = plan_confirm.filter_confirmed(store_read(f"plan::{domain}"), domain, root)
        prior = _prior_standing_plan(confirmed, plan_date)
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
                            tailor_client=None, plan_date=None, _tailor_seams=None):
    """Post-promote tailoring-hook seam — runs the ADR-0037-T1 care-lane tailoring pass once.

    Fired per RELEASE of a promoted plan, AFTER the front-door promote, with the plan set to render
    plus the render target (`generate.maintained.reemit_maintained`'s root) — plus the separate
    adherence input as a keyword extra. TWO callers fire it (ADR-0040-T4): (1) `regenerate` once per
    re-gen AT re-gen time, over the promoted-and-NOT-held domains (a held domain is excluded so it is
    never tailored/egressed during the hold); (2) `confirm.confirm_plan_change` once per operator
    confirm, over the UNION of every currently-confirmed held domain for that `plan_date` (the deferred
    tailoring the hold withheld, fired on the pending->confirmed transition). When a `tailor_client` is
    threaded it dispatches the care-lane tailoring pass (`tailoring.tailor`) once — the pass reads the
    operator's RAW `_care_profile` detail and renders the tailored sections ONLY into the gitignored
    maintained artifact. Absent the client (the not-yet-wired production trigger site) it stays a
    PASS-THROUGH, mirroring `signal`'s seams-unwired posture — 0 tailoring, 0 model spend.
    Change-control (build-plan multi-agent flag): the call shape (plan set + render target) is a
    cross-task contract — a later edit changing it triggers an Architect contract-update notice.

    Args:
        promoted_plan (dict): domain -> the promoted plan value for each promoted domain.
        render_target (str | Path): The `reemit_maintained` root/artifact target.
        adherence (dict, optional): The separate plan-vs-actual adherence input (AC-5).
        tailor_client (optional): The care-lane presentation model client. None -> pass-through.
        plan_date (str, optional): The re-gen's YYYY-MM-DD date the tailoring emit-gate keys on.
        _tailor_seams (dict, optional): Test-only seams forwarded to `tailoring.tailor` (the
            gitignored `out_dir` / synthetic-identity / repo-root artifact seams). None in production.
    """
    if tailor_client is None:
        return None
    from scripts.plan import tailoring
    from scripts.serve import care_chat

    care_profile_read = functools.partial(
        care_chat._care_profile, functools.partial(store.read, root=render_target))
    # Risk R-D: pass the promoted (recorded-and-not-held THIS re-gen) domain set so the tailoring
    # emit-gate keys on the current hold set, not a stale same-date store row.
    tailoring.tailor(render_target, client=tailor_client,
                     care_profile_read=care_profile_read, plan_date=plan_date,
                     promoted=set(promoted_plan), **(_tailor_seams or {}))
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
    """The latest on-file re-gen date across BOTH the thin `plan::` rows and the comprehensive stream.

    Dual-source resolver (RULING 1 consequence). OPTION 2 KEEPS Leg 1's thin `plan::<domain>` write,
    so a re-gen promoting >=1 renderable domain advances the marker via `plan::` (read across the
    RENDERABLE roster — the only domains that ever carry a thin row). It ALSO reads the comprehensive
    `plan-model::` version stream (`plan_model.resolve_comprehensive`) so a renderable-LESS (all-rich)
    comprehensive re-gen — which writes NO thin row — still advances the `MIN_REGEN_INTERVAL_DAYS`
    debounce floor; a `plan::`-only marker would starve on such a re-gen and every subsequent trigger
    would re-fire (debounce thrash). Zero on-file re-gens resolve to None.
    """
    from scripts.store import plan_model

    dates = []
    for domain in plan_schema.RENDERABLE_DOMAINS:
        resolved = plan_schema.resolve_plan(store_read(f"plan::{domain}"), on_date)
        if resolved["plan_date"] is not None:
            dates.append(resolved["plan_date"])
    comprehensive = plan_model.resolve_comprehensive(store_read(plan_model._PREFIX_MODEL), on_date)
    if comprehensive["plan_date"] is not None:
        dates.append(comprehensive["plan_date"])
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
