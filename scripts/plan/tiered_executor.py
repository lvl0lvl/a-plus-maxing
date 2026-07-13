"""The four-tier deterministic executor + escalation predicate (ADR-0045-T2, FAIL-CLOSED).

Reads ADR-0045-T1's compiled ``monitoring_config`` + the day's monitoring-signal observations and
routes each observed signal-event into one of four escalation tiers, **fail-closed by direction**:
an unclassifiable or multi-tier event escalates to the HIGHER tier, never guesses down. It is the
zero-slack critical-path node on the monitoring loop (``0045-T1 -> 0045-T2 -> 0045-T3``); ADR-0045-T3
(Wave 6) hosts this engine in the ADR-0039 runner.

The load-bearing property is DETERMINISM ON A NO-EVENT DAY: when no ``monitoring_signal`` crosses a
material threshold, the executor makes 0 model calls + 0 de-id-IN calls + 0 front-door re-entries —
it Tier-1 auto-applies the certified bounded adjustments deterministically and does nothing else.

The four tiers (the escalation predicate reads them in fail-closed-UP order over each observed
signal's fired rules, resolving the signal-event to the MAX implicated tier):

  - **Tier-1 (bounded in-domain deterministic)** — a certified ``TIER1_AUTO_APPLY_SAFE`` rule whose
    signal reads UNDER its ``materiality_threshold`` is auto-applied deterministically with 0 model
    calls. The *model recording* of a Tier-1 auto-apply is ADR-0045-T3's disposition #22 (Wave 6),
    not this task — the executor's Tier-1 output is the bounded-adjustment directive.
  - **Tier-2 (material in-domain)** — a certified rule whose signal reads AT/ABOVE materiality
    (certified-but-material) routes the re-plan THROUGH the composed gate + per-domain safety floor
    (``plan_orchestrator.run_orchestrated``(loop_enabled) -> ``plan_driver.drive`` ->
    ``gate_dispatch.compose_disposition`` -> the fail-closed ``safety_passed is True`` surface gate),
    the SAME composition ADR-0043-T3's Leg-1 uses — NEVER the bare ``adjust.adjust_plan`` leg
    (finding-A parity, PF-S133-02: the bare leg applies ONLY the per-domain floor and re-runs neither
    the composed gate nor the cross-domain reconciliation — the exact safety gap Tier-2 must not open).
    An UN-wired composed gate (``gate_dispatch is None``) is fail-closed-UP to a Tier-4 hold, never a
    degraded re-plan: ``run_orchestrated`` derives ``loop_enabled = gate_dispatch is not None``, so a
    ``None`` gate would drop to the LEGACY non-loop path and record an UN-composed plan (WAVE5-01).
  - **Tier-3 (cross-domain seam)** — a ``MUST_ESCALATE`` rule reaching another domain
    (``target_domain`` != own) routes to ADR-0043-T2's reconciler (``orchestrate.reconcile`` /
    the ``cross_domain_seams`` pass), 0 auto-applied at Tier-1.
  - **Tier-4 (safety-threshold)** — a safety-gate rule (``safety == "gate"``) HOLDS by the executor
    calling the EXISTING ``plan_confirm.mark_pending(domain, plan_date, root)`` DIRECTLY for the
    safety-affected domain (Ruling 1 / Option B), **magnitude-INDEPENDENT** — NOT via the
    composition's magnitude-gated ADR-0040 hold (which is SKIPPED on a blocked / sub-majority run, so
    Option A fails OPEN for exactly the safety events Tier-4 exists to close). The pending pointer
    makes ``plan_model.read_plan_version`` resolve the change NOT-standing and
    ``plan_confirm.decision_for == DECISION_PENDING`` positively — 0 auto-advance past the
    human/medical-liaison gate. A ``MUST_ESCALATE`` entry the predicate cannot positively pin to
    Tier-2/3/4-by-safety lands at Tier-4 by DEFAULT (the fail-closed-UP terminal tier, F2 / Ruling 2).

Store surface: the executor's ONLY DIRECT store write is the EXISTING ``plan_confirm.mark_pending``
on the Tier-4 / F2-default / fail-closed-hold path — a Tier-2 route's ``run_orchestrated`` writes
transitively through the frozen record spine (no new direct write here). That direct hold rides the
frozen ``plan-confirm::`` stream under keying's unchanged
``(item, timepoint, source)`` identity (battery-tested at ADR-0040/0044-T1), defines NO new store
key/stream, and calls no other ``store.append`` / ``store.correct``. Otherwise it READS the compiled
config and CALLS the composition (Tier-2) + ``orchestrate.reconcile`` (Tier-3) seams. It changes no
existing file and re-implements neither the compiler's rule grammar nor the driver's revise loop.

Observation contract (SE Ask-vs-Proceed rule 3 — same public intent, simpler internal shape, stated
in the recipe Deviation table): ``observations`` is a per-signal reading set ``{signal_name:
observed_value}`` the predicate classifies against the config's ``{signal, bound,
materiality_threshold}`` envelope; an unobserved signal is no event. ADR-0045-T3 binds the seams from
the runner context and feeds the compiled config read from the ADR-0044 model.
"""

from collections import defaultdict

from scripts.plan import monitoring_compiler, orchestrate, plan_orchestrator
from scripts.store import plan_confirm

# The four escalation tiers (ascending — the fail-closed-UP direction; the predicate resolves a
# multi-tier signal-event to the MAX implicated tier).
TIER_1 = 1  # bounded in-domain deterministic auto-apply (0 model calls)
TIER_2 = 2  # material in-domain re-plan THROUGH the composed gate + per-domain floor
TIER_3 = 3  # cross-domain seam -> orchestrate.reconcile
TIER_4 = 4  # safety-threshold / fail-closed-UP default -> plan_confirm.mark_pending HOLD


def _rule_of(entry):
    """The adjustment rule an ADR-0045-T1 compiled entry carries.

    The compiled entry is ``{_RULE_KEY: rule, _CLASSIFICATION_KEY: token}``; ``classification_of`` is
    the public accessor for the token, but the compiler exposes no public accessor for the rule, so
    the rule is read through the compiler's own single-sourced ``_RULE_KEY`` constant (never a
    hard-coded ``"rule"`` literal — a rename in the compiler follows here in lockstep).

    Args:
        entry (Mapping): A compiled rule entry from a ``monitoring_config`` domain's rules.

    Returns:
        (Mapping) The ``adjustment_rule`` the entry compiled.
    """
    return entry[monitoring_compiler._RULE_KEY]


def _implicated_tiers(domain, entries, material, materiality_known):
    """The escalation tiers a signal's fired rules positively implicate (fail-closed-UP).

    Over the rules targeting one observed signal: a certified ``TIER1_AUTO_APPLY_SAFE`` rule gates on
    materiality (immaterial -> Tier-1 auto-apply, material -> Tier-2 certified-but-material); a
    ``MUST_ESCALATE`` cross-domain rule -> Tier-3 and a safety-gate rule -> Tier-4 are the structural
    escalations (implicated whenever the signal reads); an in-domain un-certified ``MUST_ESCALATE``
    rule escalates on a material observation OR when materiality is INDETERMINATE (the signal carries
    no ``materiality_threshold``, so immateriality can't be positively shown — CQ-1/SEC-W5-02) and,
    positively pinning no tier, contributes the Tier-4 fail-closed-UP DEFAULT. Only a PROVABLY-immaterial
    un-certified rule (materiality known, reading below threshold) does nothing — no unsafe auto-apply.

    Args:
        domain (str): The signal's own domain (the in-domain reference for the cross-domain check).
        entries (list): The compiled rule entries targeting this signal.
        material (bool): Whether the observation reads at/above a KNOWN materiality_threshold (False
            when the threshold is absent — read with materiality_known to tell indeterminate from
            provably-immaterial).
        materiality_known (bool): Whether the signal carries a materiality_threshold at all. False ->
            materiality is INDETERMINATE (an un-certified in-domain rule then fail-closes UP, not inert).

    Returns:
        (set) The implicated tier numbers; a set (possibly empty) whose max is the routed tier.
        (set) The cross-domain target domains implicated (for the Tier-3 reconcile candidates).
    """
    tiers = set()
    cross_targets = set()
    for entry in entries:
        rule = _rule_of(entry)
        if monitoring_compiler.classification_of(entry) == monitoring_compiler.TIER1_AUTO_APPLY_SAFE:
            # certified in-domain: auto-apply when immaterial, re-plan when material.
            tiers.add(TIER_2 if material else TIER_1)
            continue
        # MUST_ESCALATE — fail-closed-UP.
        target_domain = rule.get(monitoring_compiler.RULE_TARGET_DOMAIN, domain)
        cross_domain = target_domain != domain
        safety_gate = rule.get(monitoring_compiler.RULE_SAFETY) == monitoring_compiler.SAFETY_GATE
        if safety_gate:
            tiers.add(TIER_4)  # structural safety escalation (magnitude-independent)
        if cross_domain:
            tiers.add(TIER_3)  # structural cross-domain-seam escalation
            cross_targets.add(target_domain)
        if not safety_gate and not cross_domain and (material or not materiality_known):
            # an in-domain un-certified rule (non-monotone / under-specified) pinning no tier: the
            # Tier-4 fail-closed-UP DEFAULT (F2) on a material observation OR when materiality is
            # INDETERMINATE (materiality_threshold absent -> immateriality can't be shown, so a large
            # reading must NOT go inert — CQ-1/SEC-W5-02). A PROVABLY-immaterial rule (materiality
            # known, reading below threshold) stays inert (fail-safe).
            tiers.add(TIER_4)
    return tiers, cross_targets


def _tier2_replan(domain, raw_intake, deid_client, dispatch, store_read, root, plan_date,
                  gate_dispatch, reauthor, adjudicator):
    """Route a material in-domain re-plan THROUGH the composed gate (NEVER the bare adjust leg).

    Drives ``plan_orchestrator.run_orchestrated``(loop_enabled) over the affected domain — de-id-IN ->
    dispatch -> the inner engine -> ``plan_driver.drive`` -> ``gate_dispatch.compose_disposition`` ->
    the fail-closed ``safety_passed is True`` surface gate — the SAME composition ADR-0043-T3's Leg-1
    uses. The ``gate_dispatch`` producer is the injected composed gate (the runner supplies the real
    one in ADR-0045-T3); loop_enabled is what carries the re-plan through the composition rather than
    the legacy non-loop floor.
    """
    return plan_orchestrator.run_orchestrated(
        raw_intake, deid_client, dispatch, store_read, root,
        plan_date=plan_date, domains=(domain,), gate_dispatch=gate_dispatch,
        reauthor=reauthor, adjudicator=adjudicator,
    )


def _tier3_reconcile(domain, cross_targets):
    """Route a cross-domain-seam event to ADR-0043-T2's reconciler (0 auto-applied at Tier-1).

    Hands the involved domains (the rule's own domain + its cross-domain targets) to
    ``orchestrate.reconcile`` — the ``cross_domain_seams`` reconciler decides the holds; the executor
    never auto-applies a cross-domain adjustment. The runner (ADR-0045-T3) supplies the reconciler's
    real per-domain candidates from the ADR-0044 model.
    """
    candidates = {d: {"domain": d, "plan": None} for d in ({domain} | cross_targets)}
    return orchestrate.reconcile(candidates)


def _routing(domain, signal, tier, action, effect):
    """One tier-routing record — the per-event surface (F3: escalations/rejections are OBSERVABLE)."""
    return {"domain": domain, "signal": signal, "tier": tier, "action": action, "effect": effect}


def _route_domain(domain, domain_config, observations, raw_intake, deid_client, dispatch,
                  store_read, root, plan_date, gate_dispatch, reauthor, adjudicator):
    """Route ONE domain's observed signal-events to tiers; a bad SIGNAL fail-closes only itself.

    Builds the domain's ``{signal_name: signal}`` index (a NAMELESS monitored signal is skipped,
    mirroring the compiler's ``.get()`` tolerance — WAVE5-02) and the per-signal fired-rule groups,
    then routes each OBSERVED signal-event. Two per-signal fail-closes, each surfaced (F3) and never a
    silent drop / bare exception / un-composed re-plan: a non-numeric (un-interpretable) reading and a
    Tier-2 route whose composed gate is UN-wired (``gate_dispatch is None``) each fail-closed-UP to a
    Tier-4 hold for THAT signal. Returns the domain's tier-routing records.
    """
    routings = []
    signals = {}
    for signal in domain_config[monitoring_compiler.DOMAIN_SIGNALS]:
        name = signal.get(monitoring_compiler.SIGNAL_NAME)
        if name is None:
            continue  # a nameless monitored signal is no event — skip (mirror the compiler's .get())
        signals[name] = signal
    entries_by_signal = defaultdict(list)
    for entry in domain_config[monitoring_compiler.DOMAIN_RULES]:
        entries_by_signal[_rule_of(entry).get(monitoring_compiler.RULE_TARGET_SIGNAL)].append(entry)

    for signal_name, entries in entries_by_signal.items():
        if signal_name not in observations:
            continue  # the signal was not observed today -> no event
        observation = observations[signal_name]
        signal = signals.get(signal_name)
        materiality = (
            signal.get(monitoring_compiler.SIGNAL_MATERIALITY) if isinstance(signal, dict) else None
        )
        if not isinstance(observation, (int, float)):
            # WAVE5-02: an un-interpretable (non-numeric) reading cannot be classified against
            # materiality — fail-closed-UP to a Tier-4 hold for THIS signal (never a bare TypeError
            # on the `>=` below, never a silent drop), so a later signal/domain still processes.
            plan_confirm.mark_pending(domain, plan_date, root)
            routings.append(_routing(domain, signal_name, TIER_4, "hold-uninterpretable-reading", None))
            continue
        material = materiality is not None and observation >= materiality

        tiers, cross_targets = _implicated_tiers(domain, entries, material, materiality is not None)
        if not tiers:
            continue  # nothing implicated (a provably-immaterial un-certified rule does nothing)
        tier = max(tiers)  # fail-closed-UP: resolve a multi-tier event to the HIGHER tier

        if tier == TIER_1:
            routings.append(_routing(domain, signal_name, TIER_1, "auto-apply", None))
        elif tier == TIER_2:
            if gate_dispatch is None:
                # WAVE5-01: the composed gate IS the Tier-2 safety surface. A re-plan with
                # gate_dispatch=None drops to run_orchestrated's LEGACY non-loop path, which records
                # a plan WITHOUT the driver / composed gate / fail-closed `safety_passed` surface — a
                # fail-OPEN. Refuse the degraded re-plan; fail-closed-UP to a Tier-4 hold instead. The
                # guard also guarantees "replan-through-composition" is emitted ONLY when the composed
                # loop genuinely runs (loop_enabled = gate_dispatch is not None).
                plan_confirm.mark_pending(domain, plan_date, root)
                routings.append(_routing(domain, signal_name, TIER_4, "hold-composed-gate-unwired", None))
            else:
                result = _tier2_replan(
                    domain, raw_intake, deid_client, dispatch, store_read, root, plan_date,
                    gate_dispatch, reauthor, adjudicator,
                )
                routings.append(_routing(domain, signal_name, TIER_2, "replan-through-composition", result))
        elif tier == TIER_3:
            report = _tier3_reconcile(domain, cross_targets)
            routings.append(_routing(domain, signal_name, TIER_3, "reconcile", report))
        else:  # TIER_4 — the safety-threshold hold + the F2 fail-closed-UP default
            plan_confirm.mark_pending(domain, plan_date, root)
            routings.append(_routing(domain, signal_name, TIER_4, "hold-pending-human-gate", None))
    return routings


def execute_monitoring_day(config, observations, raw_intake, deid_client, dispatch, store_read, root,
                           *, plan_date, gate_dispatch=None, reauthor=None, adjudicator=None):
    """Classify the day's observed signals against the compiled config and route each to a tier.

    Iterates each domain's compiled rules grouped by target signal; for each OBSERVED signal it reads
    the observation's materiality against the signal envelope, computes the implicated tiers over the
    signal's fired rules (fail-closed-UP), and routes the signal-event to the MAX implicated tier —
    Tier-1 auto-apply (0 model calls), Tier-2 re-plan through the composition, Tier-3
    ``orchestrate.reconcile``, or Tier-4 ``plan_confirm.mark_pending`` HOLD. An observed signal whose
    fired rules pin no tier (e.g. a provably-immaterial un-certified rule) is inert (no routing). Each
    domain is processed in ISOLATION: a domain-level fault fail-closes THAT domain to a Tier-4 hold and
    never aborts a later domain's safety hold (WAVE5-02). The executor's ONLY DIRECT store write is the
    Tier-4 / F2-default / fail-closed ``mark_pending`` (the existing ``plan-confirm::`` sink; no new
    key/stream) — a Tier-2 route's ``run_orchestrated`` writes transitively through the frozen record
    spine.

    Args:
        config (Mapping): The ADR-0045-T1 compiled ``monitoring_config`` (``{domain: {DOMAIN_RULES,
            DOMAIN_SIGNALS}}``) the executor READS — never re-runs the compiler's rule grammar.
        observations (Mapping): The day's per-signal readings ``{signal_name: observed_value}``.
        raw_intake (dict): The raw operator plan-intake a Tier-2 re-plan de-identifies through
            ``run_orchestrated`` (forwarded verbatim; the de-id-IN crown-jewel boundary owns it).
        deid_client: The injected de-id model client a Tier-2 re-plan routes the de-id-IN call through.
        dispatch (Callable): The programmatic specialist-dispatch seam a Tier-2 re-plan consumes.
        store_read (Callable): The store read surface, instance-root pre-bound (forwarded to a Tier-2
            re-plan).
        root (str | Path): The store root the Tier-4 ``mark_pending`` hold records into.
        plan_date (str): The day's YYYY-MM-DD date (the re-plan date + the Tier-4 pointer timepoint).
        gate_dispatch (Callable, optional): The composed RAW-VERDICT producer injected into a Tier-2
            re-plan's ``run_orchestrated`` (loop_enabled) — the runner supplies the real composed gate
            in ADR-0045-T3. Default ``None``.
        reauthor (Callable, optional): The energy-bounce re-dispatch hook forwarded to a Tier-2 re-plan.
        adjudicator (Callable, optional): The held-finding medical-liaison hook forwarded to a Tier-2
            re-plan (the inner safety gate — never bypassed).

    Returns:
        (dict) ``{"routings": [<per-event tier-routing record>, ...]}`` — each record is
        ``{domain, signal, tier, action, effect}``; the ``tier`` is the resolved escalation tier and
        the record's PRESENCE is the event's surfaced disposition (F3).
    """
    routings = []
    for domain, domain_config in config.items():
        try:
            domain_routings = _route_domain(
                domain, domain_config, observations, raw_intake, deid_client, dispatch,
                store_read, root, plan_date, gate_dispatch, reauthor, adjudicator,
            )
        except Exception:
            # WAVE5-02 per-domain isolation: an UNANTICIPATED domain-level fault (a malformation no
            # signal-level guard caught) fail-closes THIS domain to a Tier-4 hold and is SURFACED
            # (F3) — it must never propagate and abort a LATER domain's safety hold. The broad catch
            # is a deliberate fail-closed backstop for a health-safety loop, not a swallowed error.
            plan_confirm.mark_pending(domain, plan_date, root)
            routings.append(_routing(domain, None, TIER_4, "hold-domain-fault", None))
        else:
            routings.extend(domain_routings)

    return {"routings": routings}
