"""The programmatic subscription orchestrator — the autonomous drive layer over the inner engine.

`run_orchestrated` is the programmatic runtime surface that SUPERSEDES the S68 interactive
`/generate-plan` session: it takes the raw operator plan-intake, runs it through the Wave-1
`deid_in` crown-jewel boundary, dispatches each plan-domain specialist programmatically (the
full role profile inlined verbatim per INV-ROLE-INLINING) over the de-identified summary, and
drives the existing `pipeline.run_generation` seam (compute -> reconcile -> adjudicate ->
record). It WRAPS the inner engine verbatim — it re-authors nothing in `orchestrate` /
`pipeline` / `assemble` / `generate_plan` / `adjudicate` / `router`: the plan + safety reasoning
is the dispatched specialists' / liaison's (runtime A), never invented here. This module is the
wiring + the dispatch loop + the de-id halt, and records nothing the inner engine did not.

On a `deid_in` honest-no-plan sentinel (`{"deidentified": False, ...}`) it HALTS to honest
no-plan and dispatches nothing — never a dispatch over a non-summary. It NEVER bypasses the
inner safety gate: a held additive-AE / cross-domain-conflict / Rx-BPMH finding records only
when `adjudicate` (forwarded through `run_generation`'s `adjudicator` hook) releases it.

It ALSO owns the orchestrator's control surface, so it exposes an injectable GATE-DISPATCH SEAM
(`gate_dispatch=`, default a no-op that dispatches nothing). The Wave-3 quality judge
(ADR-0023-T1) and safety review (ADR-0024-T1) wire their real post-generation gates into this
seam; ADR-0020-T2 injects a recording spy here for the outage gate-idle (0-dispatch) assertion.
This task builds ONLY the seam + its inert default, NEVER the gates. `gate_dispatch` is DISTINCT
from `run_generation`'s `gates=` per-domain safety-inputs dict (`clearance_granted` /
`red_s_lea_screen` to `compute_plan`): `gate_dispatch=` is the post-generation gate-dispatch hook
this task adds, `gates=` is the per-domain compute input this callable also forwards.

The revise loop (ADR-0022-T2) and the dispatch-cap (ADR-0022-T3) are LATER tasks and are
explicitly OUT of scope here — this module pre-builds neither.
"""

import json
from pathlib import Path

from scripts.plan import pipeline
from scripts.plan.deid_in import deid_in

# domain -> the role whose full profile the dispatch prompt inlines (INV-ROLE-INLINING). The
# plan-domain specialists live under `.claude/agents/<role>/agent.md` (verified present); a
# nonexistent path would inline empty and make the role-inlining contract vacuous, so the live
# profile is read at dispatch time and a missing one fails loud (FileNotFoundError).
_ROLE_OF_DOMAIN = {
    "workout": "personal-trainer",
    "nutrition": "nutritionist",
    "supplements": "supplement-specialist",
    "peptides": "peptide-specialist",
}

# The default plan domains an unattended run generates (all four `PLAN_DOMAINS`); a caller
# narrows via `domains=`.
DEFAULT_DOMAINS = ("workout", "nutrition", "supplements", "peptides")

# The honest no-plan reason when the de-id-IN boundary returns the sentinel: there is no
# de-identified summary, so the orchestrator halts and dispatches nothing. Mirrors the de-id
# sentinel's vocabulary (the honest-no-plan states share a shape).
DEID_HALTED = "deid-halted"

_AGENTS_ROOT = Path(".claude/agents")


def _role_profile(role):
    """Read a role's full profile verbatim from `.claude/agents/<role>/agent.md`.

    The INV-ROLE-INLINING source for the plan-domain specialists. A missing profile fails loud
    (the dispatch must inline a real profile, never an empty path that makes the contract vacuous).

    Args:
        role (str): The role slug (e.g. "personal-trainer").

    Returns:
        (str) The profile file's full text.
    """
    return (_AGENTS_ROOT / role / "agent.md").read_text(encoding="utf-8")


def _dispatch_prompt(role, summary, gates):
    """Build a specialist dispatch prompt: the full role profile + the de-identified summary.

    Inlines the role's full profile verbatim (INV-ROLE-INLINING) ahead of the de-identified
    operator summary + the active gates — the dispatch payload carries the de-identified summary
    only (0 raw-PII), since the orchestrator only ever has the `deid_in` summary, never the raw
    intake, at this point.

    Args:
        role (str): The dispatched role slug.
        summary (dict): The de-identified operator summary (the dispatch's only operator-state).
        gates (dict): The active per-domain safety inputs.

    Returns:
        (str) The dispatch prompt.
    """
    profile = _role_profile(role)
    return (
        f"{profile}\n\n"
        "## De-identified operator summary (the ONLY operator-state source — 0 raw PII)\n\n"
        f"{json.dumps(summary, default=str)}\n\n"
        "## Active gates\n\n"
        f"{json.dumps(gates, default=str)}\n"
    )


def run_orchestrated(raw_intake, deid_client, dispatch, store_read, root, *, plan_date,
                     domains=DEFAULT_DOMAINS, on_date=None, gates=None, gate_dispatch=None,
                     reauthor=None, adjudicator=None):
    """Drive the autonomous GENERATE pass: de-id IN -> dispatch specialists -> the inner engine.

    The programmatic runtime surface (runtime A): (1) calls `deid_in(raw_intake, deid_client)`
    for the de-identified summary; (2) HALTS to honest no-plan with 0 dispatches when `deid_in`
    returns the `{"deidentified": False}` sentinel — never a dispatch over a non-summary;
    (3) otherwise, for each requested domain, builds a dispatch prompt inlining the domain's full
    role profile verbatim (INV-ROLE-INLINING) over the de-identified summary + the active gates,
    issues it through the injected `dispatch` seam, and captures each author envelope into
    `authors`; (4) drives `pipeline.run_generation(authors, ...)` and returns its result. The
    inner engine records the survivors via `record_plan`; the orchestrator records nothing
    directly, opens no new store stream, and never bypasses the inner safety gate (a held finding
    records only when `adjudicate` — forwarded through `adjudicator` — releases it).

    Args:
        raw_intake (dict): The raw operator plan-intake (carries raw-PII fields).
        deid_client: The injected de-id model client (a real `ModelClient`, or a fixture mock).
        dispatch (Callable): The programmatic specialist-dispatch seam,
            `dispatch(domain, prompt, summary) -> author envelope`. A real agent dispatch in
            production; a fixture-author mock in tests (so the orchestrator runs with 0 live spend).
        store_read (Callable): The store read surface, instance-root pre-bound.
        root (str | Path): The store root the plans + the queue are recorded into.
        plan_date (str): The plans' YYYY-MM-DD date.
        domains (tuple, optional): The plan domains to generate. Defaults to all four
            `PLAN_DOMAINS`.
        on_date (str, optional): The doctor-visit-queue collation date. Forwarded to
            `run_generation` (defaults there to `plan_date`).
        gates (dict, optional): Per-domain safety inputs (`clearance_granted`, `red_s_lea_screen`)
            forwarded to `run_generation` (the per-domain `compute_plan` input). DISTINCT from
            `gate_dispatch`. Defaults to all-conservative.
        gate_dispatch (Callable, optional): The injectable GATE-DISPATCH SEAM — the Wave-3 /
            ADR-0020-T2 attachment point. Default `None` -> a no-op that dispatches nothing; this
            task builds ONLY the seam + its inert default, never the gates (those are Wave-3).
            ADR-0023-T1 / ADR-0024-T1 wire real post-generation gates here; ADR-0020-T2 injects a
            recording spy here for the outage gate-idle (0-dispatch) assertion. DISTINCT from
            `gates=`.
        reauthor (Callable, optional): The energy-bounce re-dispatch hook, forwarded to
            `run_generation` verbatim.
        adjudicator (Callable, optional): The held-finding medical-liaison dispatch hook,
            forwarded to `run_generation` verbatim (the inner safety gate — never bypassed).

    Returns:
        (dict) On a successful run, the `run_generation` result (`results`, `reconciliation`,
        `reauthored`, `adjudication`, `conflict_adjudications`, `rx_bpmh_adjudications`,
        `dvq_entries`). On the de-id sentinel halt, the honest no-plan state
        `{"deidentified": False, "reason": DEID_HALTED, "results": {}, "dvq_entries": [],
        "deid": <the sentinel>}` — 0 dispatches issued, `run_generation` never called.
    """
    gates = gates or {}
    # The seam is HELD here (the control-surface hook ADR-0023-T1 / ADR-0024-T1 wire real gates
    # into, ADR-0020-T2 spies). Its DEFAULT is a no-op that dispatches nothing — this task builds
    # the seam only, never the gates, so a normal run issues 0 gate dispatches (AC-7).
    gate_dispatch = gate_dispatch if gate_dispatch is not None else _noop_gate_dispatch

    summary = deid_in(raw_intake, deid_client)
    # Honest no-plan halt: the de-id boundary returned the sentinel ({"deidentified": False}), so
    # there is no de-identified summary. Dispatch nothing, call no inner engine, return honest
    # no-plan — never a dispatch over a non-summary (the spec CORE CHANGE).
    if summary.get("deidentified") is False:
        return {
            "deidentified": False,
            "reason": DEID_HALTED,
            "results": {},
            "dvq_entries": [],
            "deid": summary,
        }

    # Dispatch each domain's specialist (full profile inlined) over the de-identified summary
    # through the injected seam, capturing each author envelope. The orchestrator originates no
    # plan content — the envelope is the specialist's (runtime A).
    authors = {}
    for domain in domains:
        role = _ROLE_OF_DOMAIN[domain]
        prompt = _dispatch_prompt(role, summary, gates)
        authors[domain] = dispatch(domain, prompt, summary)

    # Drive the inner engine verbatim. It records the survivors via `record_plan`; the
    # orchestrator records nothing directly and opens no new store stream. The safety gate
    # (the `adjudicator` hook) is forwarded, never bypassed.
    return pipeline.run_generation(
        authors, store_read, root, plan_date=plan_date, on_date=on_date, gates=gates,
        reauthor=reauthor, adjudicator=adjudicator,
    )


def _noop_gate_dispatch(*args, **kwargs):
    """The inert default gate-dispatch seam: dispatches nothing.

    The post-generation gate-dispatch hook's no-op default (AC-7). A normal run with the default
    issues 0 gate dispatches — the seam is the attachment point ADR-0023-T1 / ADR-0024-T1 wire
    real judge / safety-review gates into and ADR-0020-T2 spies for the outage gate-idle
    assertion. This task builds the seam + this inert default ONLY, never the gates.
    """
    return None
