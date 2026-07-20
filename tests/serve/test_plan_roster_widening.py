"""ADR-0052-T3: end-to-end composition gate — the always-on ten author into `plan-model::`.

Drives the REAL POST /generate-plan front door with a fixture client returning conformant envelopes
for all ten always-on domains (four thin renderable + six `domain_program`-valid rich §5-§10), and
asserts the composed `plan-model::` version records >=10 authored programs (the COUNT the rich render
will lay out, NOT the rendered card count) while `RENDERABLE_DOMAINS` stays four (the widening is
AUTHORING, not RENDERING). An empty-state surface authors no §11-§13 program (no progressive
fabrication). $0 — fixture/spy client + synthetic store, no live SDK call, no spend.
"""
import datetime
import subprocess
from pathlib import Path

from scripts.model import client
from scripts.plan import activation
from scripts.store import plan_model, plan_schema
from tests.serve.test_orchestrator_synthesize import _rich_author
from tests.serve.test_server import (
    _MockAuthorClient,
    _domain_envelopes,
    _post_generate_plan,
    _seed_summary_store,
    _serve_in_thread,
    _server_with_author,
)

_ALWAYS_ON_TEN = frozenset({
    "workout", "nutrition", "peptides", "supplements", "endocrine",
    "cardiovascular", "recovery", "sleep", "longevity", "mental-performance",
})
_RICH_SIX = ("endocrine", "cardiovascular", "recovery", "sleep", "longevity", "mental-performance")
_PROGRESSIVE_THREE = ("dermatology", "gi", "lymphatic")
_FROZEN_ANCHOR = "3ab1c3abb6c995fbaaadcb179735759e4a61d73d"
_FROZEN_SIX_PLUS_TRACK = (
    "scripts/store/store.py", "scripts/store/keying.py", "scripts/plan/pipeline.py",
    "scripts/plan/adjudicate.py", "scripts/plan/adjust.py", "scripts/plan/router.py",
    "scripts/plan/track.py",
)


def _ten_domain_envelopes():
    """The four thin renderable envelopes + six `domain_program`-valid rich §5-§10 envelopes.

    The thin four drive Leg-1 (`orchestrate.generate_plans` -> the `plan::` validators); the six rich
    drive Leg-2 (`care_chat.synthesize` -> `_author_rich` -> `domain_program.validate`), so every
    floored always-on domain authors and folds into the composed `plan-model::` version.
    """
    envelopes = dict(_domain_envelopes())
    for domain in _RICH_SIX:
        envelopes[domain] = _rich_author(domain)
    return envelopes


class _ContractGroundedClient(_MockAuthorClient):
    """A spy client that GROUNDS every author call through the REAL `_author_system_prompt`.

    `_MockAuthorClient` returns a pre-built envelope WITHOUT building the prompt, so a mock alone
    bypasses `_contract_section` — the composition count would discriminate on T2's floor but NOT on
    T1's `_AUTHOR_CONTRACT_SECTION` map (a §5-§10 domain would still record from the canned envelope
    even if T1 never mapped it). Calling `client._author_system_prompt(domain)` FIRST reproduces the
    real front-door coupling: an UN-mapped domain raises `ValueError` (T1's guard), which the server's
    `_author_rich` `except`->None drops — so the >=10 composition count genuinely requires BOTH T1 (the
    map resolves §5-§10) and T2 (the floor seats them in `active`). The canned envelope keeps it $0
    (no live model call); only the pure-string prompt build runs.
    """

    def author(self, domain, summary):
        client._author_system_prompt(domain)  # exercises T1's _contract_section; ValueError if unmapped
        return super().author(domain, summary)


def _git_numstat(anchor, paths):
    repo = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
    ).stdout.strip()
    return subprocess.run(
        ["git", "diff", "--numstat", anchor, "--", *paths],
        capture_output=True, text=True, cwd=repo, check=True,
    ).stdout.strip()


def test_composition_records_ten_authored_into_plan_model(tmp_path):
    # AC-1/AC-2 (placement, not existence): a generation over the floored always-on ten records >=10
    # authored programs in the composed `plan-model::` version, the six §5-§10 rich each present by
    # domain key. RED before T1+T2: the six §5-§10 either are not in `active` (no T2 floor) or
    # `_author_rich`->None (no T1 map), so the composed version carries <=4 programs.
    _seed_summary_store(tmp_path / "store")  # signal-less summary -> T2 floors to the always-on ten
    srv, port = _server_with_author(tmp_path, _ContractGroundedClient(_ten_domain_envelopes()))
    _serve_in_thread(srv)
    try:
        status, _body = _post_generate_plan(port)
        assert status == 200, f"POST /generate-plan returned {status}, expected 200"
        today = datetime.date.today().isoformat()
        resolved = plan_model.read_plan_version(today, tmp_path / "store")
        assert resolved["state"] is None, (
            f"the plan-model:: comprehensive version did not stand for today (state={resolved['state']!r})")
        programs = resolved["version"][plan_model.DOMAIN_PROGRAMS]
        assert len(programs) >= 10, f"fewer than ten authored programs in plan-model:: : {sorted(programs)}"
        for domain in _RICH_SIX:
            assert domain in programs, (
                f"the always-on rich domain {domain!r} did not author into plan-model:: : {sorted(programs)}")
    finally:
        srv.shutdown()
        srv.server_close()


def test_render_stays_four_renderable_domains():
    # AC-3: the widening is AUTHORING, not RENDERING — RENDERABLE_DOMAINS stays the original four
    # (RT-009). Asserting the render shows >=10 cards would be the WRONG test and FAIL by design.
    assert len(plan_schema.RENDERABLE_DOMAINS) == 4
    assert set(plan_schema.RENDERABLE_DOMAINS) == {"workout", "nutrition", "supplements", "peptides"}


def test_floor_set_equals_authorable_set():
    # AC-4: the floor set == the authorable set == the always-on ten, so no floored always-on domain
    # silently `_author_rich`->None and no authorable domain is left off the floor.
    assert set(activation.ALWAYS_ON_DOMAINS) == set(client._AUTHOR_CONTRACT_SECTION) == _ALWAYS_ON_TEN


def test_empty_state_authors_no_progressive_program(tmp_path):
    # AC-5: an empty-state surface (no dermatology / GI / lymphatic signal) authors NO §11-§13 program
    # — the floor never fabricates a progressive card. RED if a §11-§13 slug were added to ALWAYS_ON.
    _seed_summary_store(tmp_path / "store")  # no skin / gut / lymphatic signal
    srv, port = _server_with_author(tmp_path, _ContractGroundedClient(_ten_domain_envelopes()))
    _serve_in_thread(srv)
    try:
        status, _body = _post_generate_plan(port)
        assert status == 200
        today = datetime.date.today().isoformat()
        programs = plan_model.read_plan_version(today, tmp_path / "store")["version"][plan_model.DOMAIN_PROGRAMS]
        for domain in _PROGRESSIVE_THREE:
            assert domain not in programs, (
                f"a progressive §11-§13 domain {domain!r} was fabricated on an empty-state surface: {sorted(programs)}")
    finally:
        srv.shutdown()
        srv.server_close()


def test_frozen_surface_and_no_synthesize_leg_edit():
    # AC-6: the composition used the ALREADY-WIRED synthesize leg + T1/T2 — no frozen surface changed
    # and server.py / care_chat.py are byte-unchanged vs main (the Stale-Premise-Reconciliation held).
    assert _git_numstat(_FROZEN_ANCHOR, _FROZEN_SIX_PLUS_TRACK) == "", "the frozen ADR-0032 surface changed"
    assert _git_numstat("main", ("scripts/serve/server.py", "scripts/serve/care_chat.py")) == "", (
        "server.py / care_chat.py changed vs main — the no-edit reconciliation was violated")
