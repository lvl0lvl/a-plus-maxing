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

from scripts.generate import maintained
from scripts.model.client import ModelCallError
from scripts.store import plan_schema, store

# Map each plan domain to its raw `_care_profile.health_detail` label (the operator's own free-text).
# `workout` reads the raw `training` detail; the compound + nutrition domains map by name.
_DETAIL_LABEL = {
    "workout": "training",
    "nutrition": "nutrition",
    "supplements": "supplements",
    "peptides": "peptides",
}


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
    if not reply:
        raise ModelCallError("care-tailoring: backend returned an empty presentation reply")
    return reply


def tailor(root, *, client, care_profile_read, plan_date, out_dir=None,
           _today=None, _profile_paths=None, _repo_root=None, _target_override=None):
    """Emit a tailored maintained artifact for the recorded, non-held plans; return its path.

    For each `plan_schema.PLAN_DOMAINS` domain, resolves the recorded `plan::<domain>` state for
    `plan_date` (the emit-gate: a plan dated `plan_date` means recorded + non-held) and, for each
    eligible domain, re-presents it against the operator's raw care-lane detail. A presentation
    failure degrades that domain to its un-tailored recorded plan (fail-safe). Renders ALL tailored
    sections ONLY through `reemit_maintained` — opens no store stream, defines no store key.

    Args:
        root (str | Path): The store root the recorded plans are read from AND the maintained
            artifact's store surface.
        client: The presentation model client (`converse(messages) -> {"reply", ...}`).
        care_profile_read (Callable): A zero-arg reader returning the operator's full care profile
            (`care_chat._care_profile`'s shape: identity-safe demographics + raw `health_detail`).
        plan_date (str): The re-gen's YYYY-MM-DD date the emit-gate keys on.
        out_dir (Path, optional): The gitignored artifacts root forwarded to `reemit_maintained`.
        _today (datetime.date, optional): Test-only render-date seam. Defaults to `plan_date`.
        _profile_paths (tuple, optional): Test-only synthetic-identity seam.
        _repo_root (str | Path, optional): Test-only repo-root seam for the gitignore confirm.
        _target_override (str | Path, optional): Test-only artifact-target seam.

    Returns:
        (Path) The maintained artifact path written.
    """
    store_read = functools.partial(store.read, root=root)
    profile = care_profile_read() or {}
    health_detail = profile.get("health_detail") or {}

    tailored = {}
    for domain in plan_schema.PLAN_DOMAINS:
        resolved = plan_schema.resolve_plan(store_read(f"plan::{domain}"), plan_date)
        # Emit-gate: only a plan RECORDED for this re-gen date (state is None). A held domain
        # recorded nothing for the date; a domain with only a prior standing plan resolves to
        # NO_PLAN_TODAY. Both are excluded — reading the recorded state, not re-deriving safety.
        if resolved["state"] is not None:
            continue
        plan = resolved["plan"]
        detail = health_detail.get(_DETAIL_LABEL.get(domain))
        try:
            tailored[domain] = _present(client, domain, plan, detail)
        except ModelCallError:
            # Fail-safe: degrade THIS domain to its un-tailored, safety-cleared recorded plan.
            tailored[domain] = str(plan)

    render_today = _today if _today is not None else datetime.date.fromisoformat(plan_date)
    return maintained.reemit_maintained(
        root=root, tailored_sections=tailored, _out_dir=out_dir, _today=render_today,
        _profile_paths=_profile_paths, _repo_root=_repo_root, _target_override=_target_override,
    )
