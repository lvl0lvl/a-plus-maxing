"""Care-lane tailoring pass — placement, emit-gate, degrade-to-safe, artifact-only (ADR-0037-T1).

The tailoring pass re-presents each RECORDED, NON-HELD `plan::<domain>` against the operator's
RAW care-lane detail (`care_chat._care_profile`'s `health_detail` — the ADR-named personalization
egress) and renders the result ONLY into the gitignored `maintained` artifact through
`reemit_maintained`. This is a CROWN-JEWEL surface: the tailored (raw-reading) output must never
reach the de-identified store / dashboard / specialist path — its ONLY sink is the gitignored
maintained artifact.

Every identity token here is the SYNTHETIC `Janet Q Testperson` (mirroring the T0-SCANSCOPE hook
fixture); no real operator PII enters this test tree. The presentation model is a mock (0 live
spend); the artifact write is driven through the `_out_dir`/`_profile_paths`/`_repo_root` seams.
"""

import datetime
import json
import subprocess
from pathlib import Path

import pytest

from scripts.model.client import ModelCallError
from scripts.store import plan_schema

SYNTH_NAME = "Janet Q Testperson"
TODAY = datetime.date(2026, 6, 24)
ON_DATE = "2026-06-24"

# Raw care-lane specifics the operator entered — present in `_care_profile`'s `health_detail`,
# ABSENT from the recorded (de-identified) plan. A tailored section referencing these proves the
# pass read the raw detail (the designed personalization egress).
RAW_PEPTIDE = "BPC-157 250mcg subq nightly protocol"
RAW_SUPPLEMENT = "Creatine monohydrate 5g loading"


def _peptide_plan(compound="recorded-de-id-peptide"):
    return {"compound": compound, "dose": "250 mcg", "route": "subq"}


def _supplement_plan(name="Creatine"):
    return {"items": [{"name": name, "dose": "5 g"}]}


# --- fixtures -------------------------------------------------------------------


def _synth_profile(tmp_path):
    """Write a synthetic gitignored operator profile and return its path tuple."""
    prof = tmp_path / "operator-profile.md"
    prof.write_text(f"# Operator Profile — {SYNTH_NAME}\n", encoding="utf-8")
    return (prof,)


def _gitignored_out(tmp_path):
    """Create a git repo whose out-dir is gitignored; return (repo_root, out_dir)."""
    repo = tmp_path / "repo"
    out = repo / "vault" / "artifacts" / "generated"
    out.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("vault/artifacts/generated/\n", encoding="utf-8")
    return repo, out


def _seed_plan(root, domain, *, plan, date=ON_DATE, specialist="specialist"):
    plan_schema.record_plan(domain, plan, date, specialist, root)


def _care_profile_read(**detail):
    """A care-profile reader (the `_care_profile` shape) carrying the raw `health_detail`."""
    return lambda: {"health_detail": dict(detail)}


class _EchoClient:
    """A mock presentation client: echoes the operator's raw detail into the tailored reply.

    Mirrors `ModelClient.converse` (returns `{"reply", "extraction"}`). `raise_error` raises the
    typed `ModelCallError` (the fail-closed backend mode); `empty` returns an empty reply (the
    empty-return degrade case).
    """

    def __init__(self, *, raise_error=False, empty=False):
        self.raise_error = raise_error
        self.empty = empty
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        if self.raise_error:
            raise ModelCallError("presentation backend failed")
        ctx = json.loads(messages[0]["content"])
        if self.empty:
            return {"reply": "", "extraction": []}
        return {
            "reply": f"PERSONALIZED-{ctx['domain']}: keyed to {ctx.get('operator_detail')}.",
            "extraction": [],
        }


def _run_tailor(tmp_path, *, client, care_profile_read, seeds, plan_date=ON_DATE):
    """Seed the given `plan::<domain>` rows, run `tailor`, return (artifact_text, path)."""
    from scripts.plan import tailoring

    store_root = tmp_path / "store"
    for domain, plan in seeds.items():
        _seed_plan(store_root, domain, plan=plan, date=plan_date)
    repo, out = _gitignored_out(tmp_path)
    path = tailoring.tailor(
        store_root, client=client, care_profile_read=care_profile_read, plan_date=plan_date,
        out_dir=out, _today=TODAY, _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    return Path(path).read_text(encoding="utf-8"), Path(path)


# ===============================================================================
# Cycle 1: Placement (AC-1), Emit-gate on held domain (AC-2), Artifact-only (AC-4)
# ===============================================================================


def test_ac1_personalized_section_references_raw_detail(tmp_path):
    # AC-1: over a recorded, non-held plan::<domain> + raw care-lane detail, the maintained
    # artifact's tailored section for that domain references the operator's ACTUAL raw specifics.
    text, _ = _run_tailor(
        tmp_path,
        client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE, supplements=RAW_SUPPLEMENT),
        seeds={"peptides": _peptide_plan()},
    )
    assert "data-domain='peptides'" in text, "no tailored section emitted for the recorded domain"
    assert RAW_PEPTIDE in text, "the tailored section did not reference the operator's raw detail"


def test_ac2_held_domain_gets_no_tailored_section(tmp_path):
    # AC-2 / Risk R-D: a HELD domain (no recorded plan::<domain> for the date — recorded:False)
    # gets 0 tailored sections; a co-present non-held domain still tailors. The emit-gate reads the
    # RECORDED state (resolve_plan), never re-derives the safety decision.
    text, _ = _run_tailor(
        tmp_path,
        client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE, supplements=RAW_SUPPLEMENT),
        seeds={"peptides": _peptide_plan()},  # supplements HELD -> not recorded
    )
    assert "data-domain='peptides'" in text, "the non-held domain failed to tailor"
    assert "data-domain='supplements'" not in text, (
        "a HELD (not-recorded) domain was shadow-tailored around the safety gate"
    )


def test_ac2_domain_held_this_regen_despite_prior_standing_plan(tmp_path):
    # AC-2 edge: a domain HELD this re-gen but carrying a PRIOR standing plan (an earlier date)
    # must still get 0 tailored sections — the gate keys on a plan dated THIS plan_date, not on the
    # mere existence of any historical plan.
    from scripts.plan import tailoring

    store_root = tmp_path / "store"
    _seed_plan(store_root, "peptides", plan=_peptide_plan("old"), date="2026-06-10")  # prior only
    repo, out = _gitignored_out(tmp_path)
    path = tailoring.tailor(
        store_root, client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE), plan_date=ON_DATE,
        out_dir=out, _today=TODAY, _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    text = Path(path).read_text(encoding="utf-8")
    assert "data-domain='peptides'" not in text, (
        "a domain held THIS re-gen (only a prior standing plan) was tailored"
    )


def test_ac4_no_store_writer_renders_only_through_reemit(tmp_path):
    # AC-4 / Risk R-egress: the pass opens no store stream / no second name-bearing writer — it
    # writes ONLY through reemit_maintained. Static scan of the module source.
    src = Path("scripts/plan/tailoring.py").read_text(encoding="utf-8")
    assert "store.append" not in src, "the tailoring pass appends to the store (a second stream)"
    assert "_write_atomic" not in src, "the tailoring pass opens its own writer"
    assert "reemit_maintained" in src, "the tailoring pass does not render through reemit_maintained"
    # no NEW store-key stream prefix is defined in the module (reading plan:: is a read, not a def)
    assert "_PREFIX" not in src, "the tailoring pass defines a store-key prefix (a new stream)"


def test_ac4_tailored_content_lands_only_in_gitignored_artifact(tmp_path):
    # AC-4: the tailored section appears in the maintained artifact under the gitignored out-dir
    # (driven via the _out_dir seam), never a store stream. The store carries only the plan:: row.
    from scripts.store import store

    text, path = _run_tailor(
        tmp_path,
        client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE),
        seeds={"peptides": _peptide_plan()},
    )
    assert "vault/artifacts/generated" in str(path), "artifact not under the gitignored out-dir"
    assert RAW_PEPTIDE in text
    # the raw detail is NOWHERE in the store — the tailored egress is artifact-only
    store_root = tmp_path / "store"
    rows = store.read("plan::peptides", root=store_root)
    assert all(RAW_PEPTIDE not in json.dumps(r) for r in rows), (
        "the raw care detail leaked into the de-identified plan store"
    )


# ===============================================================================
# Cycle 2: Degrade-to-safe (AC-3), automated-path invocation (AC-5), idempotency (AC-6)
# ===============================================================================


@pytest.mark.parametrize("bad_client", [_EchoClient(raise_error=True), _EchoClient(empty=True)])
def test_ac3_presentation_failure_degrades_to_untailored_plan(tmp_path, bad_client):
    # AC-3 / Risk R-§4: an injected ModelCallError / empty return degrades THAT domain to its
    # un-tailored, safety-cleared recorded plan — the run does not crash. The emit-gate already
    # decided eligibility deterministically, independent of the model call.
    text, path = _run_tailor(
        tmp_path,
        client=bad_client,
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE),
        seeds={"peptides": _peptide_plan()},
    )
    # the section is still emitted (never dropped) — but with the UN-TAILORED recorded plan
    assert "data-domain='peptides'" in text, "degrade dropped the domain instead of un-tailoring it"
    assert "recorded-de-id-peptide" in text, "the un-tailored recorded plan was not rendered"
    assert "PERSONALIZED-peptides" not in text, "a failed presentation still emitted tailored content"
    assert path.exists(), "the run crashed / produced no artifact on a presentation failure"


def test_ac6_idempotent_per_plan_date(tmp_path):
    # AC-6 / Risk R-idem: firing the pass twice for the same (plan, date) produces 0 duplicate /
    # stale tailored sections (the tailored block renders in the FRESH body, outside the preserved
    # container, so a re-emit replaces rather than accretes it).
    from scripts.plan import tailoring

    store_root = tmp_path / "store"
    _seed_plan(store_root, "peptides", plan=_peptide_plan(), date=ON_DATE)
    repo, out = _gitignored_out(tmp_path)
    prof = _synth_profile(tmp_path)
    kwargs = dict(client=_EchoClient(), care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE),
                  plan_date=ON_DATE, out_dir=out, _today=TODAY, _profile_paths=prof, _repo_root=repo)
    tailoring.tailor(store_root, **kwargs)
    path = tailoring.tailor(store_root, **kwargs)  # second fire, same (plan, date)
    text = Path(path).read_text(encoding="utf-8")
    assert text.count("data-domain='peptides'") == 1, (
        f"re-firing accreted duplicate tailored sections: {text.count(chr(39)+'data-domain'+chr(39))}"
    )


def test_ac5_seam_unwired_is_passthrough_no_tailoring(tmp_path, monkeypatch):
    # AC-5 (unwired guard): with NO tailor_client threaded (the not-yet-wired production trigger
    # site), the post-promote seam stays a pass-through — tailoring.tailor is NOT called (0 live
    # model spend on the un-wired path). Mirrors plan_loop.signal's `seams-unwired` posture.
    from scripts.plan import tailoring
    from scripts.serve import plan_loop

    calls = []
    monkeypatch.setattr(tailoring, "tailor", lambda *a, **k: calls.append(1))
    plan_loop._post_promote_tailoring({"peptides": _peptide_plan()}, tmp_path / "store",
                                      plan_date=ON_DATE)
    assert calls == [], "the un-wired seam invoked the tailoring pass"


def test_ac5_wired_seam_fires_tailoring_once(tmp_path, monkeypatch):
    # AC-5: when the tailor_client is threaded, the post-promote seam fires the tailoring pass
    # EXACTLY ONCE, forwarding the render target (the reemit_maintained root) and plan_date.
    from scripts.plan import tailoring
    from scripts.serve import plan_loop

    calls = []
    monkeypatch.setattr(tailoring, "tailor", lambda *a, **k: calls.append((a, k)) or (tmp_path / "m"))
    render_target = tmp_path / "store"
    plan_loop._post_promote_tailoring({"peptides": _peptide_plan()}, render_target,
                                      plan_date=ON_DATE, tailor_client=object())
    assert len(calls) == 1, f"the wired seam fired {len(calls)} times, expected once"
    (args, kwargs) = calls[0]
    assert args[0] == render_target, "the seam did not forward the render target as the store root"
    assert kwargs.get("plan_date") == ON_DATE, "the seam did not forward plan_date"


def test_ac5_automated_regen_fires_tailoring_once(tmp_path, monkeypatch):
    # AC-5 (integration): firing the automated front door (regenerate — the cadence/biomarker path,
    # NO care-chat turn) runs the tailoring pass exactly once AFTER the promote. Drives the real
    # composed front door over fixtures (0 live spend), with the tailoring pass stubbed to count.
    from scripts.plan import tailoring
    from scripts.serve import plan_loop
    from tests.plan.test_deid_in import _FixedDeidClient
    from tests.plan.test_generate_plan import _seed_store
    from tests.plan.test_plan_orchestrator import _deid_summary
    from tests.serve.test_plan_loop import _LoopDispatch, _clean_authors

    store_root = tmp_path / "store"
    _seed_store(store_root)
    calls = []
    monkeypatch.setattr(tailoring, "tailor", lambda *a, **k: calls.append((a, k)) or (tmp_path / "m"))

    today = datetime.date.today().isoformat()
    result = plan_loop.regenerate(
        store_root, dispatch=_LoopDispatch(_clean_authors()),
        deid_client=_FixedDeidClient(_deid_summary()), plan_date=today,
        trigger=plan_loop.DATA_EVENT_TRIGGER, tailor_client=object(),
    )
    promoted = [d for d, r in result["results"].items() if r.get("recorded")]
    assert promoted, "the re-gen promoted nothing — the AC-5 precondition (a promote) did not hold"
    assert len(calls) == 1, f"the automated re-gen fired tailoring {len(calls)} times, expected once"
