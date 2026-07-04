"""Care-lane tailoring pass — re-present each recorded, non-held plan for the operator (ADR-0037-T1).

The pass runs on the CARE LANE, AFTER the front-door promote. For each closed-set plan domain it
applies a deterministic EMIT-GATE — emit a tailored section ONLY when a recorded `plan::<domain>`
exists for the re-gen date (a HELD domain records no plan for the date, so it is excluded WITHOUT
re-deriving the safety decision) — then re-presents that recorded plan against the operator's RAW
care-lane detail (`care_chat._care_profile`'s `health_detail`). Reading the raw detail is the
ADR-0037-named personalization egress (the care agent is the operator's own agent); the CROWN-JEWEL
constraint is on the SINK: the tailored output renders ONLY into the gitignored `maintained`
artifact through `generate.maintained.reemit_maintained` — never the de-identified store, the
de-identified dashboard, or a specialist-lane dispatch.

Fail-safe (ADR-0037 §4): a presentation-model failure (`ModelCallError` or an empty return) degrades
THAT domain to its un-tailored, safety-cleared recorded plan — the emit-gate already decided
eligibility deterministically, independent of the model call — so a model failure never drops the
domain and never bypasses the safety posture. The pass opens no store stream, defines no store key,
and adds no second name-bearing writer: its only sink is `reemit_maintained`.
"""

import datetime
import functools
import json
import re

from scripts.generate import maintained
from scripts.model.client import ModelCallError
from scripts.plan import orchestrate, router
from scripts.store import plan_schema, store

# Map each plan domain to its raw `_care_profile.health_detail` label (the operator's own free-text).
# `workout` reads the raw `training` detail; the compound + nutrition domains map by name.
_DETAIL_LABEL = {
    "workout": "training",
    "nutrition": "nutrition",
    "supplements": "supplements",
    "peptides": "peptides",
}

# The compound domains the two deterministic T2 safety mechanics apply to. The dosing-reject and the
# interaction screen both target the investigational-compound surface (supplements + peptides); the
# non-compound domains (workout, nutrition) are neither scanned nor screened. One canonical definition.
_COMPOUND_DOMAINS = ("supplements", "peptides")

# Curated dosing-vocabulary lexicon (ADR-0037 finding D / OQ-2): the unit + administration-frequency
# + route/titration KEYWORDS that denote a dose. A compound-domain TAILORED (model) section carrying
# any of these is re-presenting a prescribing instruction for an investigational compound — rejected
# (degraded to the specialist's safety-cleared recorded plan). A curated keyword set, never a model
# call. Single-letter units (`g`/`kg`/`ml`/`cc`) are matched only adjacent to a number by
# `_DOSING_NUMERIC_UNIT` to avoid firing on prose; the multi-char unit words are matched as tokens.
_DOSING_WORD_TOKENS = frozenset({
    "mg", "mcg", "ug", "µg", "iu", "milligram", "milligrams", "microgram", "micrograms",
    "daily", "nightly", "weekly", "twice", "once", "bid", "tid", "qd", "qhs", "eod",
    "subq", "subcutaneous", "subcutaneously", "intramuscular", "titrate", "titration", "taper",
})
_DOSING_NUMERIC_UNIT = re.compile(r"\d+\s*(?:mg|mcg|ug|µg|g|kg|ml|cc|iu)\b", re.IGNORECASE)
_WORD = re.compile(r"[a-zµ]+")


def _carries_dosing_token(text):
    """Whether a tailored-output string carries a dosing / route / titration token (finding D).

    A number adjacent to a mass/volume/activity unit (`250mg`, `5 g`, `100 iu`) or any curated
    dosing keyword (`mcg`, `nightly`, `subq`, `titrate`, …) present as a word token. Curated
    keyword scan — no model call.

    Args:
        text (str): The candidate tailored-section text.

    Returns:
        (bool) True when a dosing token is present.
    """
    if _DOSING_NUMERIC_UNIT.search(text):
        return True
    return any(word in _DOSING_WORD_TOKENS for word in _WORD.findall(text.lower()))


def _interaction_referral(profile, domain, plan):
    """The deterministic drug×compound interaction verdict for one compound domain (ADR-0037 §3).

    Model-INDEPENDENT: intersects the operator's present Rx-interaction classes (read from the care
    profile — a superset of `router.summarize`, carrying the de-identified `rx-interaction-classes`
    field — via `router.rx_interaction_class_set`) with the compound's declared additive-AE classes
    (`orchestrate._rx_bpmh_matched_classes` over the recorded plan's `ae_profile`), reusing the
    reconciler's rx-BPMH class basis rather than forking a parallel vocabulary. Computed off the
    store/profile, BEFORE and independent of the presentation model call. Fails CLOSED: a non-empty
    intersection ALWAYS returns a surfaced "see your doctor" referral (never a silent drop).

    Args:
        profile (dict): The operator's care profile (`_care_profile` shape).
        domain (str): The plan domain being tailored.
        plan (dict): The recorded (de-identified) plan value for the domain.

    Returns:
        (str) The referral text on a class intersection, or `""` when clean / non-compound.
    """
    if domain not in _COMPOUND_DOMAINS:
        return ""
    operator_rx_classes = router.rx_interaction_class_set(profile)
    if not operator_rx_classes:
        return ""
    ae_profile = plan.get("ae_profile") if isinstance(plan, dict) else None
    candidate = {"domain": domain, "meta": {"ae_profile": ae_profile if isinstance(ae_profile, dict) else {}}}
    matched = orchestrate._rx_bpmh_matched_classes(candidate, operator_rx_classes)
    if not matched:
        return ""
    classes = ", ".join(sorted(matched))
    return (
        f"See your doctor before continuing {domain}: a medication-interaction class ({classes}) "
        f"overlaps your current prescriptions."
    )


def _present(client, domain, plan, detail):
    """Re-present one domain's recorded plan against the operator's raw detail; return the text.

    Mirrors the care turn's single-call model boundary (`converse`), fail-closed: a failed / empty
    backend return raises `ModelCallError`, which the caller degrades to the un-tailored plan.

    Args:
        client: A presentation model client exposing `converse(messages) -> {"reply", ...}`.
        domain (str): The plan domain being re-presented.
        plan: The recorded (de-identified) plan value for the domain.
        detail: The operator's raw care-lane detail for the domain, or None.

    Returns:
        (str) The tailored per-domain section text.

    Raises:
        ModelCallError: The backend failed or returned an empty reply.
    """
    context = {"task": "care-tailoring", "domain": domain, "plan": plan, "operator_detail": detail}
    messages = [
        {"role": "user", "content": json.dumps(context, sort_keys=True)},
        {"role": "user", "content": "Re-present this domain's plan personalized to the operator."},
    ]
    result = client.converse(messages)
    reply = result.get("reply") if isinstance(result, dict) else None
    if not reply or not reply.strip():
        raise ModelCallError("care-tailoring: backend returned an empty presentation reply")
    return reply


def tailor(root, *, client, care_profile_read, plan_date, promoted=None, out_dir=None,
           _today=None, _profile_paths=None, _repo_root=None, _target_override=None):
    """Emit a tailored maintained artifact for the recorded, non-held plans; return its path.

    For each `plan_schema.PLAN_DOMAINS` domain, applies the emit-gate — the domain must be in THIS
    re-gen's `promoted` (recorded-and-not-held) set AND resolve to a plan dated `plan_date` — then
    re-presents each eligible domain against the operator's raw care-lane detail. A presentation
    failure degrades that domain to its un-tailored recorded plan (fail-safe). Renders ALL tailored
    sections ONLY through `reemit_maintained` — opens no store stream, defines no store key.

    Args:
        root (str | Path): The store root the recorded plans are read from AND the maintained
            artifact's store surface.
        client: The presentation model client (`converse(messages) -> {"reply", ...}`).
        care_profile_read (Callable): A zero-arg reader returning the operator's full care profile
            (`care_chat._care_profile`'s shape: identity-safe demographics + raw `health_detail`).
        plan_date (str): The re-gen's YYYY-MM-DD date the emit-gate keys on.
        promoted (set | dict, optional): THIS re-gen's recorded-and-not-held domain set (Risk R-D).
            A domain absent from it is excluded even when its store row is dated `plan_date` — the
            store-date read alone is a proxy that breaks on a same-date re-record. None (back-compat)
            keys the gate on the store-date read only.
        out_dir (Path, optional): The gitignored artifacts root forwarded to `reemit_maintained`.
        _today (datetime.date, optional): Test-only render-date seam. Defaults to `plan_date`.
        _profile_paths (tuple, optional): Test-only synthetic-identity seam.
        _repo_root (str | Path, optional): Test-only repo-root seam for the gitignore confirm.
        _target_override (str | Path, optional): Test-only artifact-target seam.

    Returns:
        (Path) The maintained artifact path written.
    """
    plan_date = plan_date or datetime.date.today().isoformat()
    store_read = functools.partial(store.read, root=root)
    profile = care_profile_read() or {}
    health_detail = profile.get("health_detail") or {}

    tailored = {}
    for domain in plan_schema.PLAN_DOMAINS:
        # Emit-gate part 1 (Risk R-D): the domain must be in THIS re-gen's recorded-and-not-held
        # set. A held domain is absent — excluded before the store read, so a stale same-date store
        # row from a prior run can never shadow-tailor a domain the safety composition just held.
        if promoted is not None and domain not in promoted:
            continue
        resolved = plan_schema.resolve_plan(store_read(f"plan::{domain}"), plan_date)
        # Emit-gate part 2: only a plan RECORDED for this re-gen date (state is None). A held domain
        # recorded nothing for the date; a domain with only a prior standing plan resolves to
        # NO_PLAN_TODAY. Both are excluded — reading the recorded state, not re-deriving safety.
        if resolved["state"] is not None:
            continue
        plan = resolved["plan"]
        detail = health_detail.get(_DETAIL_LABEL.get(domain))
        # Deterministic interaction screen (ADR-0037 §3/§4): computed off the store/profile, BEFORE
        # and INDEPENDENT of the presentation call, so a failed/empty presentation can neither change
        # the verdict nor suppress a fired referral (fail-closed). Separate from the presentation.
        referral = _interaction_referral(profile, domain, plan)
        try:
            tailored[domain] = _present(client, domain, plan, detail)
        except ModelCallError:
            # Fail-safe: degrade THIS domain to its un-tailored, safety-cleared recorded plan.
            tailored[domain] = str(plan)
        else:
            # Dosing-token reject (ADR-0037 finding D): a compound-domain TAILORED (model) section
            # must not re-present a dose/route/titration for an investigational compound. On a hit,
            # REJECT — degrade through the SAME un-tailored recorded-plan branch as a model failure.
            if domain in _COMPOUND_DOMAINS and _carries_dosing_token(tailored[domain]):
                tailored[domain] = str(plan)
        # Fail-closed: the referral surfaces regardless of presentation outcome (tailored, degraded,
        # or dosing-rejected) — a match always yields a surfaced referral.
        if referral:
            tailored[domain] = f"{referral}\n\n{tailored[domain]}"

    render_today = _today if _today is not None else datetime.date.fromisoformat(plan_date)
    return maintained.reemit_maintained(
        root=root, tailored_sections=tailored, _out_dir=out_dir, _today=render_today,
        _profile_paths=_profile_paths, _repo_root=_repo_root, _target_override=_target_override,
    )
