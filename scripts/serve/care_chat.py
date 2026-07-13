"""Profile-aware Care Assistant conversation (the continuous post-unlock care chat).

Distinct from `chat.dispatch_turn` (the PRE-unlock intake elicitation). This is the POST-unlock care
conversation, and it is the operator's OWN private agent: it re-reads the operator's FULL profile
server-side each turn (`_care_profile`) — the operator's actual peptide / supplement / diet / training
/ injury detail, plus demographics / goals / genetics — so it reasons over the real specifics, not
coarse bands. The care-review clarifying questions are the conversation's opening turns, carried back
in `conversation`, so a reply continues them instead of restarting.

Privacy boundary (operator-directed): the de-identification line is the care -> SPECIALIST / plan
hand-off (`router.dispatch`), NOT the operator -> care-agent link. The care agent is private, so it
sees the operator's real health detail; only PURE IDENTITY stays stripped (legal name, exact DOB,
contact, address) — `_care_profile` is built on `router.summarize`, which is identity-safe by
construction (disjoint from the named-excluded identity PII), then enriched with the raw health
free-text. The one `converse` call carries this profile + the live conversation (the operator's own
words, already the no-train egress class) + the current turn. The profile is SERVER-derived each turn
(the client never supplies it), so a client cannot inject a forged profile. The plan/specialist path
(`summarize` -> `dispatch`) stays de-identified — unchanged.

Store-write: the care agent WRITES the facts the operator states back to the store through the EXACT
SAME gated path the intake chat uses — `extract.persist_extraction` -> `capture.persist_capture` — so a
model-proposed fact is de-identified BY DATA CLASS by the gate (a raw value under a wired token routes
record-only; the free-text PII scan backstops), NEVER a new store path or a new egress. The model
PROPOSES, the gate DISPOSES; the receipt reports what ACTUALLY LANDED. The extraction coverage/quality
is the model's job (runtime, the same as the intake extractor); this module supplies the gated wiring.
"""

import functools
import json
import logging

from scripts.model.client import ModelCallError
from scripts.plan import router
from scripts.plan.context_assembler import assemble_context
from scripts.serve import extract
from scripts.store import store

# The field tokens the care turn's structured `extraction` may use (mapped to a plain-language
# description + allowed values). Supplied in the CONTEXT so the model knows WHICH facts to capture and
# in what shape; `capture.persist_capture` re-validates every one server-side (a bounded value out of
# its enum, or a raw value under a wired token, routes record-only — the model only PROPOSES). These
# are the capture FORM-FIELD names `persist_capture` routes by. `recovery-status-band` is the field
# the plan pipeline currently blocks on.
_EXTRACTABLE_FIELDS = {
    "recovery-status-band": "the operator's current recovery/readiness — EXACTLY one of: low, moderate, high",
    "training-experience": "years of training experience (a whole number)",
    "goal-priority-order": "the operator's stated ordering of goal priorities (free text)",
    "goal-targets": "the operator's stated goal/outcome targets (free text)",
    "hard-limits": "hard limits or things to strictly avoid (free text)",
    "nutrition-detail": "diet / nutrition specifics the operator states (free text)",
    "supplement-stack": "supplements + doses the operator states (free text)",
    "peptide-stack": "peptides + doses the operator states (free text)",
    "training-detail": "training split / days / volume specifics (free text)",
    "train-around": "injuries or issues to train around (free text)",
}

# A standing context note so the agent knows the conversation is durable (it was answering "I can't
# save" — false: the system auto-persists every turn to the conversation vault and restores it on
# reload, so the earlier turns it sees ARE the full, permanent history).
_PERSISTENCE_NOTE = (
    "This conversation is automatically saved and restored when the operator reloads — the earlier "
    "turns you are shown are the full, durable history, so never tell the operator you cannot save it."
)

# The orchestration system-prompt block (mirrors `_PERSISTENCE_NOTE`): supplied in the CONTEXT when an
# assembled record + a non-empty active set are present, so the care agent knows it is the Orchestrator
# — it DECOMPOSES the operator's goals + assembled state into one brief per active specialist. The
# `briefs` list carries exactly one brief per active domain, each with that specialist's FULL assembled
# record (the operator's uncollapsed health detail, NOT a coarse band) + the operator's goals.
_ORCHESTRATION_NOTE = (
    "You are the Orchestrator. Decompose the operator's stated goals and assembled state into one brief "
    "per active specialist: the `briefs` list below carries exactly one brief per active domain, each "
    "with that specialist's full assembled record (the operator's uncollapsed health detail) and the "
    "operator's goals. Reason per-specialist from each brief's full record; never collapse it to a "
    "coarse band."
)


def _weight_display(summary):
    """A human-readable weight in BOTH units from the de-id `bodyweight-band` kg value (or None).

    The de-id summary carries `bodyweight-band` = `"<kg>;<trend>"` (the canonical kilograms + trend);
    the operator may think in pounds, so the care context presents BOTH (`"238 lb (108 kg)"`) — no new
    raw data (the kg is already in the band). Lets the assistant talk weight in the operator's unit
    even when their explicit preference was captured before it was stored.
    """
    band = summary.get("bodyweight-band")
    if not band:
        return None
    try:
        kg = float(str(band).split(";")[0].strip())
    except (ValueError, TypeError):
        return None
    return f"{round(kg / 0.453592)} lb ({round(kg)} kg)"


def _weight_unit_preference(scaffold_root):
    """The operator's chosen weight unit ('pounds'/'kilograms') from the latest capture, or None.

    Read from the record-only scaffold `bodyweight-unit` (a display preference, not PII — `lbs`/`kg`),
    so the assistant LEADS with the operator's unit. None when unrecorded (older intake); the context
    then still carries both units via `_weight_display`, so the assistant is never kg-only.
    """
    from pathlib import Path

    from scripts.serve.capture import DEFAULT_SCAFFOLD_ROOT

    root = Path(scaffold_root) if scaffold_root is not None else DEFAULT_SCAFFOLD_ROOT
    if not root.exists():
        return None
    captures = sorted(root.glob("capture-*.json"))
    if not captures:
        return None
    try:
        data = json.loads(captures[-1].read_text())
    except (OSError, ValueError):
        return None
    unit = data.get("bodyweight-unit") if isinstance(data, dict) else None
    return {"lbs": "pounds", "kg": "kilograms"}.get(unit)


def _age_display(summary):
    """The operator's CHRONOLOGICAL age from the (legacy-misnamed) `training-age-band` token, or None.

    `training-age-band` holds the exact chronological age in years derived from the operator's birth
    year — NOT lifting experience, despite the token name. The name misled the assistant into asking
    whether 55 was age or training years; presenting it clearly as the operator's age removes that.
    """
    band = summary.get("training-age-band")
    if band is None:
        return None
    age = str(band).split(";")[0].strip()
    return f"{age} years" if age else None


# The operator's raw intake health free-text, mapped to a clear care-facing label. These are the
# named-excluded raw sources `summarize` collapses to coarse bands FOR THE SPECIALIST hand-off; the
# care agent is the operator's OWN agent, so it reads the SPECIFICS the operator entered — the
# peptides, supplement, diet, training, and injury detail — not the vague bands.
_CARE_HEALTH_DETAIL = {
    "nutrition": "raw-nutrition-free-text",
    "supplements": "raw-supplement-free-text",
    "peptides": "raw-peptide-free-text",
    "training": "raw-training-detail-free-text",
    "injuries": "raw-symptom-free-text",
}


def _scaffold_record(scaffold_root):
    """Merge the operator's record-only scaffold captures into one `{field: latest value}` dict.

    The gitignored scaffold holds record-only intake data the operator entered — MEDICATIONS
    (`rx-interaction-classes`, deliberately routed record-only because raw drug names are never
    de-identified for the specialist path), plus sleep, alcohol, smoker status, equipment detail,
    race, occupation. NONE of it is pure identity (legal name / exact DOB / contact / address route
    to the named-excluded store, not here), so the operator's OWN private care agent reads it. The
    latest non-empty value wins per field across captures.
    """
    import json
    from pathlib import Path

    from scripts.serve.capture import DEFAULT_SCAFFOLD_ROOT

    root = Path(scaffold_root) if scaffold_root is not None else DEFAULT_SCAFFOLD_ROOT
    if not root.exists():
        return {}
    merged = {}
    for path in sorted(root.glob("capture-*.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            for key, value in data.items():
                if value:
                    merged[key] = value
    return merged


def _care_profile(store_read, *, scaffold_root=None, identity_config=None):
    """The FULL care-facing profile: the identity-safe summary PLUS the operator's raw health detail.

    The de-identification boundary is the care -> SPECIALIST / plan hand-off (`router.dispatch`), NOT
    the operator -> care-agent link. The care agent is the operator's OWN private agent, so it reads
    the operator's ACTUAL detail — the peptide / supplement / diet / training / injury free-text they
    entered at intake — instead of the coarse specialist-facing bands. Built ON TOP of
    `router.summarize`, which is identity-safe BY CONSTRUCTION (its output is disjoint from the
    named-excluded identity PII — legal name, exact DOB, contact, address never appear; only the
    derived age / weight / sex / equipment / goals / genetics / rx-classes do), then ENRICHED with the
    raw health free-text under `health_detail`. So the agent sees the operator's real specifics while
    pure identity stays stripped, and the specialist/plan path stays de-identified.
    """
    if identity_config is not None:
        profile = dict(router.summarize(store_read, identity_config=identity_config))
    else:
        profile = dict(router.summarize(store_read))
    detail = {}
    for label, item in _CARE_HEALTH_DETAIL.items():
        rows = store_read(item)
        if rows and rows[-1].get("value"):
            detail[label] = rows[-1]["value"]
    if detail:
        profile["health_detail"] = detail
    # Record-only scaffold data (medications + sleep/alcohol/smoker/equipment/race/occupation): the
    # operator's OWN agent reads it — none of it is pure identity. Medications get an explicit label so
    # the agent treats them as meds, not the (empty) de-identified `rx-interaction-classes` summary
    # token; the rest is surfaced under `record` as additional profile context.
    record = _scaffold_record(scaffold_root)
    meds = record.pop("rx-interaction-classes", None)
    if meds:
        profile.setdefault("health_detail", {})["medications"] = meds
    if record:
        profile["record"] = record
    return profile


def _derive_goals(record):
    """Project the operator's stated-goal fields out of the assembled record (NOT re-collapsed).

    The `goal-*` fields already present in the ADR-0042 assembled record (`goal-domains`,
    `goal-priority-order`, `goal-targets`) — surfaced whole for the specialist, never re-summarized.
    Empty when the record carries no stated goal.

    Args:
        record (dict): The `assemble_context` assembled record.

    Returns:
        (dict) The `goal-*` subset of `record`.
    """
    return {key: value for key, value in record.items() if key.startswith("goal")}


def decompose(goals, assembled_state, active_domains):
    """Decompose the operator's goals + assembled state into one per-specialist brief per active domain.

    The brief-builder seam of the care-agent Orchestrator: for EACH active domain, emit exactly one
    brief carrying (a) the domain identity, (b) the FULL ADR-0042 `assembled_state` record — carried
    WHOLE, never sliced and never re-collapsed to a coarse `router.summarize` band (the per-specialist
    slice is deferred), and (c) the operator's goals. A PURE function of its three inputs — it does NOT
    read the store, compute the active set (no second activation gate), or call the model. The active
    set is INJECTED (its source is wired at the front door by ADR-0043-T3 + ADR-0046-T1).

    Args:
        goals: The operator's stated goals (in `respond`, derived from the record's stated-goal fields).
        assembled_state (dict): The ADR-0042 `assemble_context` record — the identity-stripped FULL
            record each brief carries whole.
        active_domains: The injected active-specialist set (a collection of domain identifiers).

    Returns:
        (list) One `brief` per active domain — `len == len(active_domains)`, 0 un-briefed, 0
        duplicates. Each `brief` is `{"domain", "assembled_state", "goals"}`.
    """
    return [
        {"domain": domain, "assembled_state": assembled_state, "goals": goals}
        for domain in active_domains
    ]


def _care_messages(profile, conversation, turn_text, *, weight_display=None, weight_pref=None,
                   age_display=None, goals=None, assembled_state=None, active_domains=None):
    """Build the care converse payload: the operator's FULL profile + conversation + turn (+ orchestration).

    Mirrors `chat._model_messages`'s API-valid shape (every entry role ∈ {user, assistant}, string
    content) but the index-0 context is the operator's FULL care profile (`_care_profile`: the
    identity-safe demographics/goals/genetics + the raw `health_detail`) — so the Care Assistant
    reasons over the operator's actual specifics, not coarse bands. The optional `weight_display` (both
    units) + `weight_pref` (the operator's chosen unit) are added so the assistant talks weight in the
    operator's unit, not kg-only. When an `assembled_state` record + a non-empty `active_domains` set
    are supplied, the orchestration decompose→brief system prompt + the per-specialist `briefs` list are
    LAYERED ON ADDITIVELY (the care agent becomes the Orchestrator) — the reply-only conversational
    context is preserved, so an existing caller with no active set is unaffected. A malformed
    conversation entry (not a `{role, content}` dict) is SKIPPED, never char-splatted into the payload.
    """
    context = {
        "task": "care-conversation",
        "profile": profile,
        "extractable_fields": _EXTRACTABLE_FIELDS,
        "notes": _PERSISTENCE_NOTE,
    }
    if weight_display:
        context["operator_weight"] = weight_display
    if weight_pref:
        context["operator_weight_unit"] = weight_pref
    if age_display:
        context["operator_age"] = age_display
        # The profile token `training-age-band` is a LEGACY NAME that holds chronological age, not
        # lifting experience — state it so the assistant does not re-ask age-vs-training-years.
        context["profile_glossary"] = {
            "training-age-band": "the operator's chronological age in years (NOT training experience)"
        }
    # Orchestration layer (ADDITIVE): when an assembled record + a non-empty active set are supplied,
    # LAYER ON the decompose→brief system prompt + one brief per active specialist. An absent/empty
    # active set adds neither key, so the payload is byte-equivalent to the reply-only conversational
    # turn — the existing agent (and every existing conversational test) is unaffected.
    if assembled_state is not None and active_domains:
        context["orchestration"] = _ORCHESTRATION_NOTE
        context["briefs"] = decompose(goals, assembled_state, active_domains)
    messages = [{"role": "user", "content": json.dumps(context, sort_keys=True)}]
    if isinstance(conversation, list):
        for turn in conversation:
            if isinstance(turn, dict) and "role" in turn and "content" in turn:
                messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": turn_text})
    return messages


def respond(turn_text, conversation, *, client, store_root=None, scaffold_root=None, identity_config=None,
            loop_dispatch=None, loop_deid_client=None, active_domains=None):
    """Run one Care Assistant conversation turn over the operator's FULL profile; reply + gated capture.

    Re-reads the operator's full care profile server-side (`_care_profile`: identity-safe demographics /
    goals / genetics + the raw health detail; server-authoritative — the client never supplies it),
    builds the converse payload (profile context + conversation + turn),
    makes the ONE no-train model call, and returns `{"reply", "receipt"}`. The care agent WRITES the
    facts it extracted from the operator's turn through the SAME gate the intake chat uses
    (`extract.persist_extraction` -> `capture.persist_capture`): a proposed fact is de-identified by its
    data class, a raw value under a wired token routes record-only, and the receipt reports what actually
    landed. Fail-closed on a failed/empty call (`ModelCallError`) -> an honest degraded reply with an
    empty receipt, 0 fabrication, 0 store write.

    Args:
        turn_text (str): The operator's raw turn this round.
        conversation (list): The prior live conversation turns (`{"role", "content"}`), incl. the
            care-review opening questions the client carried back.
        client: A model client exposing `converse(messages) -> {"reply", "extraction"}` that raises
            `ModelCallError` on a failed/empty call (the one no-train model boundary).
        store_root (str | Path, optional): The instance store root the de-id profile is read from AND
            the gate appends wired tokens into.
        scaffold_root (str | Path, optional): The gitignored operator-record root the gate writes
            record-only values under.
        identity_config (str | Path, optional): The instance operator-identity token config threaded
            into `router.summarize`'s 8j6 PII gate AND the capture gate's free-text PII scan.
        active_domains (optional): The INJECTED active-specialist set. When non-empty, `respond`
            assembles the ADR-0042 record + derives the operator's goals and threads the orchestration
            decompose→brief context into `_care_messages` (one brief per active specialist). Absent or
            empty -> the reply-only conversational turn, unchanged. The SOURCE
            (`activation.active_domains`) is wired at the front door by ADR-0043-T3/0046; this task
            only ACCEPTS the injected value, it does not compute it.

    Returns:
        (dict) `{"reply": <assistant reply>, "receipt": {"store", "scaffold", "dropped"}}`, or the
        fail-closed `{"reply": None, "receipt": empty, "degraded": True, "reason": ...}` on a failure.
    """
    store_read = functools.partial(store.read, root=store_root) if store_root is not None else store.read
    profile = _care_profile(store_read, scaffold_root=scaffold_root, identity_config=identity_config)
    # Orchestration inputs (additive): ONLY when an active set is INJECTED do we assemble the ADR-0042
    # record + derive the operator's goals — no needless assembler call / model-cost on a plain
    # conversational turn with no active set. The assembled record is identity-stripped + genetics-carved
    # BY CONSTRUCTION (the ADR-0042 seam, mirroring `_care_profile`'s identity_config handling).
    goals = assembled_state = None
    if active_domains:
        if identity_config is not None:
            assembled_state = assemble_context(store_read, identity_config=identity_config)
        else:
            assembled_state = assemble_context(store_read)
        goals = _derive_goals(assembled_state)
    messages = _care_messages(
        profile, conversation, turn_text,
        weight_display=_weight_display(profile),
        weight_pref=_weight_unit_preference(scaffold_root),
        age_display=_age_display(profile),
        goals=goals, assembled_state=assembled_state, active_domains=active_domains,
    )
    try:
        result = client.converse(messages)
    except ModelCallError as exc:
        return {"reply": None, "receipt": {"store": [], "scaffold": [], "dropped": []},
                "degraded": True, "reason": str(exc)}
    # Store-write through the SAME gate the intake chat uses: the care agent's proposed facts route
    # through `capture.persist_capture` (de-identify by data class), never a direct/second store path.
    receipt = extract.persist_extraction(
        result.get("extraction"), turn_text, root=store_root,
        scaffold_root=scaffold_root, identity_config=identity_config,
    )
    # A free-text capture completion: notify the plan loop's ONE debounced entry (ADR-0036-T2). Fires
    # only on this non-degraded branch (skipped on the fail-closed `ModelCallError` degrade above).
    # The notify carries only the derived trigger label — never the raw `turn_text` (the finding-C
    # boundary; the debounce reads DERIVED store state). Loop seams threaded by the caller; production
    # server->site threading is ADR-0036-T4. Additive — the `{"reply", "receipt"}` return is unchanged.
    from scripts.serve import plan_loop
    try:
        plan_loop.signal(store_root, trigger=plan_loop.FREE_TEXT_TRIGGER,
                         dispatch=loop_dispatch, deid_client=loop_deid_client)
    except Exception:
        # Fail-open: the loop notify is additive — a derivation/re-gen raise must never break the
        # primary care-chat reply (the capture already persisted; the `{"reply", "receipt"}` return
        # is the contract).
        logging.exception("plan-loop signal failed after care-chat capture (additive; reply unaffected)")
    return {"reply": result.get("reply"), "receipt": receipt}


def collect(collected, store_read):
    """Collect the dispatched specialists' DOMAIN PROGRAMs and reconcile through the ONE path (T2).

    The care-agent Orchestrator's collect step (ADR-0043-T2), placed AFTER + DISJOINT from the T1
    decompose region. Gathers the collected dispatched-specialist candidates — each a
    `compute_plan`-shaped result carrying its DOMAIN PROGRAM (with `cross_domain_seams`) under the
    plan's `PROGRAM_KEY`, plus the source `meta` (the additive-AE / conflict / energy triggers) and
    `reason` (the RED-S/LEA clinical-routing reason) — into the `{domain: candidate}` shape
    `orchestrate.reconcile` consumes, and routes them through the ONE `orchestrate.reconcile` path
    (reached via a function-level import mirroring the lazy `plan_loop` import in `respond`, cycle-free
    — `scripts.plan.orchestrate` never imports this module).

    SEC-W3-03 (BLOCKING; fail-OPEN otherwise): the shaped candidates PRESERVE every always-on
    safety-floor trigger the source carries — the additive-AE / conflict `meta.ae_profile` and the
    RED-S/LEA `reason`, NOT only the `domain_program` — AND the collect DERIVES + threads
    `operator_rx_classes` from the store exactly as `generate_plans` does
    (`router.rx_interaction_class_set(router.summarize(store_read))`). Shaping only the program (dropping
    `meta`/`reason`, defaulting `operator_rx_classes` to the empty set) makes all three floors DEAD on
    the care_chat path — the exact fail-OPEN this preservation closes.

    The collect step does NOT dispatch specialists, compute the active set, or synthesize the integrated
    plan (that is ADR-0043-T3). The dispatch SOURCE of `collected` is wired at the front door by
    ADR-0043-T3 / ADR-0046-T1; this task only ACCEPTS the injected value.

    Args:
        collected: An iterable of collected specialist candidates — each a mapping carrying `domain`,
            the candidate `plan` (with the DOMAIN PROGRAM under `PROGRAM_KEY`), the source `meta`, and
            the `reason`.
        store_read (Callable): The instance-root-bound store read surface; the operator's present
            Rx-interaction classes are derived from it (de-identified) for the BPMH floor.

    Returns:
        (dict) The `orchestrate.reconcile` result — `report` (incl. the uniform `seams`), `holds`,
        `conflict_held`, `rx_bpmh_held`.
    """
    from scripts.plan import orchestrate

    # 61cy — FAIL LOUD on a duplicate domain rather than the silent last-wins dict-comprehension: a
    # duplicate would silently drop a trigger-bearing candidate (its `meta`/`reason` safety-floor
    # trigger), a fail-OPEN. Now that ADR-0043-T3 wires the seam-emitting dispatch source that COULD
    # emit two candidates for one domain, the collision must surface, not be swallowed.
    candidates = {}
    for item in collected:
        domain = item["domain"]
        if domain in candidates:
            raise ValueError(
                f"care_chat.collect: duplicate domain {domain!r} in the collected specialists — a "
                f"duplicate silently drops a trigger-bearing candidate (61cy fail-loud)"
            )
        candidates[domain] = {
            "domain": domain,
            "specialist": item.get("specialist"),
            "plan": item.get("plan"),
            "meta": item.get("meta") or {},  # PRESERVE the additive-AE / conflict / energy triggers
            "reason": item.get("reason"),     # PRESERVE the RED-S/LEA clinical-routing reason
            "section": item.get("section"),
        }
    operator_rx_classes = router.rx_interaction_class_set(router.summarize(store_read))
    return orchestrate.reconcile(candidates, operator_rx_classes=operator_rx_classes)


def _program_for_renderable(domain, plan):
    """The domain's seven-field DOMAIN PROGRAM for the comprehensive version, from Leg 1's plan.

    Uses the author-emitted program (`PROGRAM_KEY`) when the surviving rec carried one, else LIFTs a
    transitional program from the recorded renderable plan (prescription = the plan, kind + the
    conformant transitional floors) via `generate_plan._lift_program` — so EVERY promoted renderable
    domain contributes a `domain_program.validate`-conformant program, none is silently dropped.
    """
    from scripts.plan import generate_plan
    from scripts.plan.assemble import PROGRAM_KEY

    if isinstance(plan, dict) and plan.get(PROGRAM_KEY) is not None:
        return dict(plan[PROGRAM_KEY])
    payload = {k: v for k, v in plan.items() if k != PROGRAM_KEY} if isinstance(plan, dict) else plan
    return generate_plan._lift_program({"payload": payload}, domain)


def _rich_program_from_envelope(envelope):
    """The first embedded seven-field DOMAIN PROGRAM (`PROGRAM_KEY`) in a rich-domain author envelope."""
    from scripts.plan.assemble import PROGRAM_KEY

    for rec in (envelope or {}).get("recommendations", []):
        program = rec.get(PROGRAM_KEY)
        if program is not None:
            return dict(program)
    return None


def _compose_version(programs, on_date):
    """Compose ONE comprehensive plan version from the gate-cleared per-domain DOMAIN PROGRAMs.

    Satisfies `plan_model.validate_plan_version`: >=1 domain program, a non-empty integrated
    narrative, >=1 dated milestone, and a non-empty monitoring config (`compile_config` returns a
    non-empty config over the non-empty `programs` map — `synthesize` returns None before reaching
    here when there is no program, so the empty case never arrives).
    """
    from scripts.plan import monitoring_compiler
    from scripts.store import plan_model

    monitoring_config = monitoring_compiler.compile_config(programs)
    return {
        plan_model.VERSION_DATE: on_date,
        plan_model.DOMAIN_PROGRAMS: dict(programs),
        plan_model.NARRATIVE: (
            "Integrated comprehensive plan across " + ", ".join(sorted(programs)) + "."
        ),
        plan_model.MILESTONES: [
            {"date": on_date, "label": "plan established", "metric": "adherence + first re-test"},
        ],
        plan_model.MONITORING_CONFIG: monitoring_config,
    }


def synthesize(active, run_result, author_rich, store_read, *, on_date, root):
    """Leg 2 (ADR-0043-T3, OPTION 2): compose ONE comprehensive plan version and record it.

    The care-agent synthesize step, placed AFTER + DISJOINT from the T1 decompose / T2 collect
    regions. Runs ONLY after Leg 1's composed gate surfaced a PASS (the caller invokes it after its
    pass-guard) — so a SAFETY_BLOCKED run never reaches here (the prior comprehensive version stands,
    0 partial write, AC-BP). Composes ONE integrated version from the gate-cleared programs Leg 1
    surfaced (the renderable domains it promoted) PLUS any rich domain active in the surface (authored
    via `author_rich`, reconciled through `collect`'s always-on floors, folded in when not held), and
    records it via `plan_model.record_plan_version` — the ADDITIVE comprehensive record ON TOP of
    Leg 1's KEPT thin per-domain write.

    Args:
        active (Iterable[str]): The active card-emitting domains for this run (the surface's active
            set); rich members beyond `plan_schema.RENDERABLE_DOMAINS` are authored + folded here.
        run_result (dict): Leg 1's result (`results` maps each domain to its record — a promoted
            renderable domain carries a recorded `plan`).
        author_rich (Callable): `author_rich(domain) -> author envelope | None` — dispatches a rich
            specialist (the unified subscription seam in `regenerate`, the no-train client in the
            server twin). 0 live spend in tests (a fixture seam).
        store_read (Callable): The instance-root-bound store read surface (the always-on-floor
            `operator_rx_classes` is derived from it inside `collect`).
        on_date (str): The version's YYYY-MM-DD date.
        root (str | Path): The store root the comprehensive version records into.

    Returns:
        (dict | None) The recorded comprehensive version, or None when there is no program to compose.
    """
    from scripts.plan import domain_program
    from scripts.plan.assemble import PROGRAM_KEY
    from scripts.store import plan_model, plan_schema

    programs = {}
    for domain, record in (run_result.get("results") or {}).items():
        if record.get("recorded") and record.get("plan") is not None:
            program = _program_for_renderable(domain, record["plan"])
            if program is not None:
                programs[domain] = program

    rich = sorted(set(active) - set(plan_schema.RENDERABLE_DOMAINS))
    if rich:
        candidates = []
        for domain in rich:
            envelope = author_rich(domain)
            program = _rich_program_from_envelope(envelope)
            candidates.append({
                "domain": domain, "specialist": (envelope or {}).get("specialist"),
                "plan": {PROGRAM_KEY: program} if program is not None else None,
                "meta": {}, "reason": None, "section": None,
            })
        outcome = collect(candidates, store_read)  # the always-on floors (SEC-W3-03 preserved)
        held = (set(outcome["holds"]) | set(outcome["conflict_held"])
                | set(outcome["rx_bpmh_held"]))
        for candidate in candidates:
            program = (candidate["plan"] or {}).get(PROGRAM_KEY)
            if candidate["domain"] in held or program is None:
                continue
            # W4-02: validate before folding — a non-conformant rich program is DROPPED (mirror
            # generate_plan._lift_program), never folded to crash the downstream composer
            # (monitoring_compiler.compile_config reads program[MONITORING_SIGNALS]).
            try:
                domain_program.validate(program)
            except domain_program.DomainProgramError:
                continue
            # HCR-01: deep-strip `load` from the rich prescription before folding, so no un-cleared
            # load reaches stored comprehensive state (ADR-0015/BUG-01). Clearance is not plumbed to
            # the rich path -> strip UNCONDITIONALLY (a rich domain's RENDERABLE_IDENTITY is None, so
            # project_renderable just deep-strips + passes through), matching the renderable translators.
            program = dict(program)
            program[domain_program.PRESCRIPTION] = domain_program.project_renderable(
                program.get(domain_program.PRESCRIPTION), candidate["domain"], strip_load=True)
            programs[candidate["domain"]] = program

    if not programs:
        return None
    version = _compose_version(programs, on_date)
    plan_model.record_plan_version(version, root)
    return version
