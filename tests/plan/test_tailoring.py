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
# pass read the raw detail (the designed personalization egress). These carry a raw specific WITHOUT
# a dose/route/frequency token — the ADR-0037-T2 compound-domain dosing-reject strips dose-bearing
# tailored output, so the personalization egress is proven with a non-dosing specific.
RAW_PEPTIDE = "BPC-157 for my left Achilles tendon repair"
RAW_SUPPLEMENT = "Creatine monohydrate for post-workout recovery"

# The dose-bearing counterpart (unit + route + frequency): a compound-domain tailored section that
# re-presents THIS is prescribing an investigational compound (ADR-0037 finding D) -> rejected.
RAW_PEPTIDE_DOSING = "BPC-157 250mcg subq nightly protocol"

# The de-identified operator Rx-interaction-class field `_care_profile` carries (via `router.summarize`)
# and the T2 interaction screen intersects against a compound's declared additive-AE classes.
RX_CLASS_FIELD = "rx-interaction-classes"


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


def _care_profile_read_rx(rx_classes, **detail):
    """A care-profile reader carrying the de-identified `rx-interaction-classes` field + raw detail.

    Mirrors `_care_profile`'s superset-of-`summarize` shape: the profile carries the operator's
    present Rx-interaction classes (a `;`-joined scalar) the T2 interaction screen reads via
    `router.rx_interaction_class_set`, alongside the raw `health_detail`.
    """
    return lambda: {RX_CLASS_FIELD: rx_classes, "health_detail": dict(detail)}


class _EchoClient:
    """A mock presentation client: echoes the operator's raw detail into the tailored reply.

    Mirrors `ModelClient.converse` (returns `{"reply", "extraction"}`). `raise_error` raises the
    typed `ModelCallError` (the fail-closed backend mode); `empty` returns an empty reply (the
    empty-return degrade case).
    """

    def __init__(self, *, raise_error=False, empty=False, whitespace=False):
        self.raise_error = raise_error
        self.empty = empty
        self.whitespace = whitespace
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        if self.raise_error:
            raise ModelCallError("presentation backend failed")
        ctx = json.loads(messages[0]["content"])
        if self.empty:
            return {"reply": "", "extraction": []}
        if self.whitespace:
            return {"reply": "   \n\t ", "extraction": []}
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


def _care_tailored_body(text, domain):
    """Extract the inner text of the `care-tailored` body for `domain` (isolates it from the fold)."""
    import re

    m = re.search(
        rf"data-domain='{domain}'.*?<div class='care-tailored-body'>(.*?)</div>", text, re.S)
    return m.group(1) if m else None


def test_whitespace_reply_degrades_to_untailored_plan(tmp_path):
    # FIX 3: a whitespace-only presentation reply is empty in substance — it must degrade to the
    # recorded plan, not emit a blank tailored body. Scoped to the care-tailored body so the
    # tracking-fold's copy of the plan can't mask the assertion.
    text, _ = _run_tailor(
        tmp_path,
        client=_EchoClient(whitespace=True),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE),
        seeds={"peptides": _peptide_plan()},
    )
    body = _care_tailored_body(text, "peptides")
    assert body is not None, "no tailored section emitted for the recorded domain"
    assert body.strip(), "a whitespace-only reply emitted a blank tailored body instead of degrading"
    assert "recorded-de-id-peptide" in body, "the degrade did not render the un-tailored recorded plan"


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


# ===============================================================================
# Cycle 3: Emit-gate keys on THIS re-gen's hold set, not a store-date proxy (R-D / HIGH)
# ===============================================================================


def test_emit_gate_keys_on_promoted_holdset_not_store_date(tmp_path):
    # Risk R-D (crown jewel): a same-date re-record can leave a HELD domain's prior-run plan dated
    # THIS plan_date in the store. The store-date proxy (resolve_plan state is None) would then EMIT
    # a tailored section for a domain THIS re-gen HELD — a shadow-prescribe. The emit-gate must key
    # on the promoted (recorded-and-not-held THIS re-gen) set: a domain absent from `promoted` gets
    # 0 tailored sections even though its store row is dated plan_date.
    from scripts.plan import tailoring

    store_root = tmp_path / "store"
    # BOTH domains carry a plan dated plan_date (the store-date proxy would emit both).
    _seed_plan(store_root, "peptides", plan=_peptide_plan(), date=ON_DATE)
    _seed_plan(store_root, "supplements", plan=_supplement_plan(), date=ON_DATE)
    repo, out = _gitignored_out(tmp_path)
    # THIS re-gen HELD peptides (adverse data) and promoted only supplements.
    path = tailoring.tailor(
        store_root, client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE, supplements=RAW_SUPPLEMENT),
        plan_date=ON_DATE, promoted={"supplements"},
        out_dir=out, _today=TODAY, _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    text = Path(path).read_text(encoding="utf-8")
    assert "data-domain='peptides'" not in text, (
        "a domain HELD this re-gen (absent from `promoted`) was shadow-tailored around the safety "
        "composition on the strength of its stale same-date store row"
    )
    assert "data-domain='supplements'" in text, "the promoted domain failed to tailor"


# ===============================================================================
# Cycle 4: real loop->_care_profile->artifact wiring (Integration-Verification Mandate)
# ===============================================================================


def _seed_raw_detail(root, item, value, date=ON_DATE):
    """Seed a raw care-lane free-text store row `_care_profile` reads into `health_detail`."""
    from scripts.store import store

    store.append(item, {"item": item, "timepoint": f"{date}T00:00:00+00:00",
                        "source": "intake", "value": value}, root=root)


def test_post_promote_real_wiring_personalizes_artifact(tmp_path):
    # Integration-Verification Mandate: the AC-5 tests monkeypatch tailoring.tailor, so the real
    # _post_promote_tailoring -> tailoring.tailor -> care_chat._care_profile -> reemit_maintained path
    # never runs. Drive it end-to-end with NO monkeypatch of tailor and a REAL seeded store; assert a
    # personalized section (keyed to the operator's raw detail) lands in the gitignored artifact.
    from scripts.serve import plan_loop

    store_root = tmp_path / "store"
    _seed_plan(store_root, "peptides", plan=_peptide_plan(), date=ON_DATE)
    _seed_raw_detail(store_root, "raw-peptide-free-text", RAW_PEPTIDE)
    repo, out = _gitignored_out(tmp_path)
    seams = {"out_dir": out, "_today": TODAY,
             "_profile_paths": _synth_profile(tmp_path), "_repo_root": repo}
    plan_loop._post_promote_tailoring(
        {"peptides": _peptide_plan()}, store_root, plan_date=ON_DATE,
        tailor_client=_EchoClient(), _tailor_seams=seams,
    )
    text = (out / "maintained.html").read_text(encoding="utf-8")
    assert "data-domain='peptides'" in text, "the real wiring emitted no tailored section"
    assert RAW_PEPTIDE in text, (
        "the real care_profile_read did not thread the operator's raw detail into the artifact"
    )


def test_post_promote_partial_degrade_per_domain(tmp_path):
    # The "degrade THIS domain only" claim: with two promoted domains and a client that fails for B
    # only, A is personalized AND B is un-tailored (its recorded plan) in the SAME artifact.
    from scripts.serve import plan_loop

    class _PerDomainClient:
        def converse(self, messages):
            ctx = json.loads(messages[0]["content"])
            if ctx["domain"] == "supplements":
                raise ModelCallError("supplements presentation backend failed")
            return {"reply": f"PERSONALIZED-{ctx['domain']}: keyed to {ctx.get('operator_detail')}.",
                    "extraction": []}

    store_root = tmp_path / "store"
    _seed_plan(store_root, "peptides", plan=_peptide_plan(), date=ON_DATE)
    _seed_plan(store_root, "supplements", plan=_supplement_plan(), date=ON_DATE)
    _seed_raw_detail(store_root, "raw-peptide-free-text", RAW_PEPTIDE)
    _seed_raw_detail(store_root, "raw-supplement-free-text", RAW_SUPPLEMENT)
    repo, out = _gitignored_out(tmp_path)
    seams = {"out_dir": out, "_today": TODAY,
             "_profile_paths": _synth_profile(tmp_path), "_repo_root": repo}
    plan_loop._post_promote_tailoring(
        {"peptides": _peptide_plan(), "supplements": _supplement_plan()}, store_root,
        plan_date=ON_DATE, tailor_client=_PerDomainClient(), _tailor_seams=seams,
    )
    text = (out / "maintained.html").read_text(encoding="utf-8")
    assert "PERSONALIZED-peptides" in text, "domain A did not personalize"
    assert "PERSONALIZED-supplements" not in text, "domain B emitted tailored content despite failing"
    assert "Creatine" in text, "domain B did not degrade to its un-tailored recorded plan"


# ===============================================================================
# Cycle 5: Dosing-token reject on a compound-domain tailored section (ADR-0037 finding D, AC-1)
# ===============================================================================


def test_dosing_token_in_compound_tailoring_rejects_to_untailored_plan(tmp_path):
    # AC-1 POSITIVE control: a compound-domain (peptides) tailored section whose model output carries
    # a dose/route/frequency token (echoed from a dose-bearing raw detail) is REJECTED — the domain
    # degrades to its un-tailored recorded plan. Count of compound-domain TAILORED (model) sections
    # carrying a dosing token == 0: the model marker is gone, the recorded plan is rendered instead.
    text, _ = _run_tailor(
        tmp_path,
        client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE_DOSING),
        seeds={"peptides": _peptide_plan()},
    )
    body = _care_tailored_body(text, "peptides")
    assert body is not None, "no tailored section emitted for the recorded compound domain"
    assert "PERSONALIZED-peptides" not in body, (
        "a compound tailored section carrying a dosing token was NOT rejected (shadow-prescribe)"
    )
    assert RAW_PEPTIDE_DOSING not in body, "the dose-bearing tailored output was not stripped"
    assert "recorded-de-id-peptide" in body, "the reject did not degrade to the un-tailored plan"


def test_no_dosing_token_in_compound_tailoring_is_retained(tmp_path):
    # AC-1 NEGATIVE control: a compound-domain tailored section WITHOUT a dosing token is KEPT — the
    # reject is falsifiable, not blanket compound-domain suppression.
    text, _ = _run_tailor(
        tmp_path,
        client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=RAW_PEPTIDE),
        seeds={"peptides": _peptide_plan()},
    )
    body = _care_tailored_body(text, "peptides")
    assert "PERSONALIZED-peptides" in body, "a non-dosing compound tailored section was suppressed"
    assert RAW_PEPTIDE in body, "the non-dosing raw specific was not personalized into the section"


def test_dosing_token_reject_scoped_to_compound_domains(tmp_path):
    # AC-1 scope: a NON-compound domain (workout) tailored section carrying a dosing-like token is NOT
    # scanned/rejected — the reject is compound-domain-only (supplements / peptides).
    text, _ = _run_tailor(
        tmp_path,
        client=_EchoClient(),
        care_profile_read=_care_profile_read(training="deadlift 100kg 5x5 daily"),
        seeds={"workout": {"exercises": [{"name": "deadlift", "sets": 5}]}},
    )
    body = _care_tailored_body(text, "workout")
    assert body is not None, "no tailored section emitted for the workout domain"
    assert "PERSONALIZED-workout" in body, "a non-compound domain was wrongly dosing-rejected"


# Findings 2/3 — dosing-token detector quality. RED cases: dose/frequency notation the prior lexicon
# let through (`2x/day`, `q12h`, `2 tablets`, `b.i.d.`, `units`, `grams`, `per day`). Each MUST be
# detected as a dosing token, or a compound tailored section could shadow-prescribe.
@pytest.mark.parametrize("dosing_text", [
    "inject 2x/day this week", "run it 3x/week", "250mcg/day protocol", "dose q12h as needed",
    "every 8 hours for pain", "take 2 units", "5 grams post-workout", "add 1 gram",
    "once per day", "swallow 2 tablets", "3 caps with food", "b.i.d. dosing",
])
def test_dosing_detector_catches_frequency_and_form_bypasses(dosing_text):
    from scripts.plan.tailoring import _carries_dosing_token

    assert _carries_dosing_token(dosing_text), (
        f"a dose/frequency notation bypassed the dosing detector: {dosing_text!r}"
    )


# Negative controls: benign prose whose bare frequency adverbs (`once`/`daily`/`weekly`/`taper`)
# tripped the prior lexicon. Each MUST NOT be flagged — the detector targets dose notation, not copy.
@pytest.mark.parametrize("benign_text", [
    "take this once your tendon heals", "fits your daily routine", "a weekly check-in call",
    "ease back as you taper off training", "BPC-157 for your left Achilles tendon repair",
    "review your progress every week this month",
])
def test_dosing_detector_ignores_benign_frequency_adverbs(benign_text):
    from scripts.plan.tailoring import _carries_dosing_token

    assert not _carries_dosing_token(benign_text), (
        f"benign prose false-fired the dosing detector: {benign_text!r}"
    )


# ===============================================================================
# Cycle 6: The drug×compound interaction gate lives at the RECONCILER, not the tailoring lane
# (ADR-0037 §3 RETIRED — Architect binding ruling). The record-path production contract.
# ===============================================================================

# A curated Rx-interaction class the operator's medication surface carries AND a compound declares.
KNOWN_RX_CLASS = "bleeding-risk"


def test_recorded_compound_plan_carries_no_ae_profile_no_tailoring_referral(tmp_path):
    # NON-TAUTOLOGICAL record-path contract: a compound plan produced through the PRODUCTION translate
    # path (compute_plan -> record_plan) carries NO `ae_profile` — that field lives in the candidate
    # `meta`, a sibling record_plan never writes — so tailoring emits NO "see your doctor" referral for
    # it EVEN WHEN the operator's rx-interaction-classes intersect the compound's declared additive-AE
    # classes. This encodes the true production behavior: the drug×compound interaction gate is the
    # RECONCILER's primary BPMH screen (tests/plan/test_orchestrate.py), NOT the tailoring lane. The
    # test FAILS if anyone re-homes an ae_profile-reading interaction screen into the tailoring lane
    # (the retired §3), or makes the record path persist ae_profile to feed such a screen.
    from scripts.plan import tailoring
    from scripts.plan.generate_plan import compute_plan
    from scripts.store import store
    from tests.plan.test_generate_plan import _author, _peptide_rec, _seed_store

    store_root = tmp_path / "store"
    store_read = _seed_store(store_root)
    envelope = {
        **_author(_peptide_rec("BPC-157", "250 mcg", "subcutaneous"),
                  specialist="peptide-specialist"),
        "reconciliation": {"ae_profile": {"additive_classes": [KNOWN_RX_CLASS]}},
    }
    candidate = compute_plan("peptides", envelope, store_read)
    # the compound genuinely DECLARES the interacting class — it rides in the candidate meta ...
    assert candidate["meta"]["ae_profile"]["additive_classes"] == [KNOWN_RX_CLASS], (
        "the author's declared additive-AE class did not reach the candidate meta"
    )
    plan_schema.record_plan(
        "peptides", candidate["plan"], ON_DATE, candidate["specialist"], store_root)
    # ... but the production record path persists ONLY the plan payload — no ae_profile lands, so the
    # dormant §3 screen (reading `plan.get("ae_profile")`) could never fire in production.
    recorded = plan_schema.resolve_plan(
        store.read("plan::peptides", root=store_root), ON_DATE)["plan"]
    assert "ae_profile" not in recorded, (
        "the record path persisted ae_profile — the retired §3 screen's dormancy premise broke"
    )

    repo, out = _gitignored_out(tmp_path)
    path = tailoring.tailor(
        store_root, client=_EchoClient(),
        care_profile_read=_care_profile_read_rx(KNOWN_RX_CLASS, peptides=RAW_PEPTIDE),
        plan_date=ON_DATE, promoted={"peptides"},
        out_dir=out, _today=TODAY, _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    body = _care_tailored_body(Path(path).read_text(encoding="utf-8"), "peptides")
    assert body is not None, "no tailored section emitted for the recorded compound domain"
    assert "see your doctor" not in body.lower(), (
        "a tailoring-lane interaction referral fired on a production-recorded compound plan — the "
        "retired §3 screen was re-homed into the tailoring lane"
    )


# ===============================================================================
# Cycle 7 (ADR-0037-T3): load-time SUMMARY_FIELD_SET-disjointness tripwire (AC-1)
# ===============================================================================

# Re-run the EXACT load-time disjointness assert in a fresh interpreter AFTER mutating the
# field set, to prove a tailoring section key masquerading as a summary field reds it. Mirrors
# tests/plan/test_router.py's `_MISPLACEMENT_SUBPROCESS` change-control idiom.
_TRIPWIRE_SUBPROCESS = """
import sys
from scripts.plan import router, tailoring
{mutation}
assert set(tailoring._TAILORING_SECTION_KEYS).isdisjoint(set(router.SUMMARY_FIELD_SET))
print("tripwire-did-not-red")
"""


def _run_tripwire_subprocess(mutation):
    """Run the load-time disjointness tripwire against a mutated field set in a fresh interpreter.

    Returns the subprocess result; a faithful tripwire reds with a non-zero exit and an
    AssertionError in stderr (never prints `tripwire-did-not-red`).
    """
    import subprocess
    import sys

    repo_root = Path(__file__).resolve().parents[2]
    return subprocess.run(
        [sys.executable, "-c", _TRIPWIRE_SUBPROCESS.format(mutation=mutation)],
        cwd=repo_root, capture_output=True, text=True,
    )


def test_tailoring_section_keys_disjoint_from_summary_field_set():
    # AC-1 (no-raise half): the module imported (its load-time tripwire ran clean), the tailoring
    # section keys ARE the domains the pass emits at the reemit_maintained boundary (tied to the
    # emitted set, not a hand-spelled copy), and they are disjoint from router.SUMMARY_FIELD_SET —
    # so no tailoring key can cross the de-id boundary as a `summarize`/`dispatch` planner token.
    from scripts.plan import router, tailoring

    assert set(tailoring._TAILORING_SECTION_KEYS) == set(plan_schema.PLAN_DOMAINS)
    assert set(tailoring._TAILORING_SECTION_KEYS).isdisjoint(set(router.SUMMARY_FIELD_SET))


def test_tailoring_key_in_summary_field_set_reds_at_load():
    # AC-1 (raise half): a tailoring section key placed INTO SUMMARY_FIELD_SET reds the load-time
    # disjointness tripwire. Fail-capable — inject a REAL tailoring key into the field set, then
    # re-run the EXACT tripwire expression; it raises AssertionError (never prints the sentinel).
    result = _run_tripwire_subprocess(
        "router.SUMMARY_FIELD_SET = router.SUMMARY_FIELD_SET + "
        "(sorted(tailoring._TAILORING_SECTION_KEYS)[0],)"
    )
    assert result.returncode != 0, (
        f"the disjointness tripwire did not red; stdout={result.stdout!r}"
    )
    assert "AssertionError" in result.stderr
    assert "tripwire-did-not-red" not in result.stdout


# ===============================================================================
# Cycle 8 (ADR-0037-T3): crown-jewel wire-scan — 0 tailoring/raw content reaches
# the de-id store streams OR the de-id dashboard render (AC-2, finding E), and the
# tailored sections land ONLY in the gitignored artifact (AC-3).
# ===============================================================================

# A distinctive synthetic raw care-lane detail the tailoring path READS (fed via `health_detail`,
# never persisted to the de-id store) — carrying a raw drug specific + the operator's legal name.
# The wire-scan proves NEITHER reaches the store or the de-id dashboard. Deliberately dose-free so
# the T2 compound-domain dosing-reject retains it (the artifact IS the positive control).
WIRE_RAW_DETAIL = f"BPC-157 left-Achilles rehab for {SYNTH_NAME}"

# The rendered tailoring-content markers `reemit_maintained` emits for a tailored section
# (`scripts/generate/maintained._tailored_sections_html`). Their presence in a de-id surface
# would BE the leak this wire-scan forbids.
_TAILORING_CONTENT_MARKERS = ("care-tailored", "data-domain=", "PERSONALIZED-")


def _tailoring_content_hits(payload):
    """Count raw-PII (legal name + raw detail) + rendered-tailoring-content occurrences."""
    hits = payload.count(SYNTH_NAME) + payload.count(WIRE_RAW_DETAIL)
    hits += sum(payload.count(marker) for marker in _TAILORING_CONTENT_MARKERS)
    return hits


def _run_wire_scan_tailor(tmp_path):
    """Seed a de-id plan + a biomarker, run the FULL tailoring path; return (artifact_text, store_root)."""
    from scripts.plan import tailoring
    from scripts.store import loop_schema

    store_root = tmp_path / "store"
    _seed_plan(store_root, "peptides", plan=_peptide_plan(), date=ON_DATE)
    loop_schema.record_biomarker("ferritin", "2026-06-01T00:00:00+00:00", 52, root=store_root)
    repo, out = _gitignored_out(tmp_path)
    path = tailoring.tailor(
        store_root, client=_EchoClient(),
        care_profile_read=_care_profile_read(peptides=WIRE_RAW_DETAIL),
        plan_date=ON_DATE, out_dir=out, _today=TODAY,
        _profile_paths=_synth_profile(tmp_path), _repo_root=repo,
    )
    return Path(path).read_text(encoding="utf-8"), store_root


def _deid_surfaces(store_root, tmp_path):
    """Dump the two de-id surfaces the tailored output must never reach: the store streams
    (`store.read_all`) + the de-id dashboard render (`render_views` over the seeded biomarker)."""
    from scripts.generate import render_views
    from scripts.store import store

    store_dump = json.dumps(store.read_all(store_root))
    pages = render_views.render_views(
        store_root, biomarkers=("ferritin",), _out_dir=tmp_path / "dash")
    dashboard_dump = "\n".join(p.read_text(encoding="utf-8") for p in pages)
    return store_dump, dashboard_dump


def test_ac2_wire_scan_no_tailoring_or_raw_content_in_deid_surfaces(tmp_path):
    # AC-2 CROWN JEWEL: after the FULL tailoring path (incl. the T2 dosing-reject), 0 raw-PII
    # (legal name + raw drug specific) AND 0 rendered-tailoring-content markers reach EITHER the
    # de-id store streams OR the de-id dashboard render. The tailored (raw-reading) output's ONLY
    # sink is the gitignored maintained artifact.
    from scripts.store import store

    artifact_text, store_root = _run_wire_scan_tailor(tmp_path)
    # positive control: the content IS in the gitignored artifact (the test seeded real content).
    assert _tailoring_content_hits(artifact_text) > 0, "the tailoring path emitted no content to scan"

    store_dump, dashboard_dump = _deid_surfaces(store_root, tmp_path)
    assert _tailoring_content_hits(store_dump) == 0, "tailoring/raw content leaked into a de-id store stream"
    assert _tailoring_content_hits(dashboard_dump) == 0, "tailoring/raw content leaked into the de-id dashboard"

    # finding E: no `plan-tailor::` (or any tailoring-owned) store stream was opened.
    assert not any("tailor" in item for item in store.items(store_root)), (
        "the tailoring pass opened a store stream (finding E — no raw store stream)"
    )

    # NON-TAUTOLOGY guard: injecting a tailoring marker into a de-id payload REDs the probe.
    assert _tailoring_content_hits(store_dump + "<section class='care-tailored'>") > 0, (
        "the wire-scan probe cannot detect injected tailoring content (tautological)"
    )
    assert _tailoring_content_hits(dashboard_dump + WIRE_RAW_DETAIL) > 0


def test_ac3_tailored_sections_only_in_gitignored_artifact(tmp_path):
    # AC-3: the tailored sections appear in the gitignored maintained artifact (>=1) and in 0
    # tracked/committed render (the de-id dashboard payload).
    artifact_text, store_root = _run_wire_scan_tailor(tmp_path)
    assert artifact_text.count("data-domain='peptides'") >= 1, "no tailored section in the artifact"
    _, dashboard_dump = _deid_surfaces(store_root, tmp_path)
    assert dashboard_dump.count("data-domain") == 0, "a tailored section reached the de-id dashboard"
    assert dashboard_dump.count("care-tailored") == 0, "a tailored section class reached the de-id dashboard"


# ===============================================================================
# Cycle 9 (ADR-0037-T3): ADR-0001 egress amendment (AC-4) + the reinserted-name
# pre-ship commit/push PII scan (AC-5).
# ===============================================================================


def test_ac4_adr0001_records_tailoring_egress_carveout():
    # AC-4: ADR-0001's egress list carries the ADR-0037 tailoring presentation carve-out entry
    # AND the `amended-by` edge (finding F — named egress).
    import re

    doc = Path("docs/adr/ADR-0001-pii-trust-boundary-no-train-routing.md").read_text(encoding="utf-8")
    m = re.search(r"ADR-0037[^\n|]*\|\s*amended-by\s*\|([^\n]*)", doc)
    assert m, "ADR-0001 has no `amended-by` Related-Decisions row for ADR-0037"
    row = m.group(1).lower()
    assert "tailoring" in row, "the ADR-0037 row does not name the tailoring egress carve-out"
    assert "gitignored" in row or "maintained artifact" in row, (
        "the ADR-0037 row does not scope the tailored output to the gitignored maintained artifact"
    )


def _synth_identity_config(tmp_path):
    """A gitignored SYNTHETIC operator-identity token file (`first|last`), the shape pii_scan loads."""
    cfg = tmp_path / "operator-identity.txt"
    cfg.write_text("Janet|Testperson\n", encoding="utf-8")
    return cfg


def test_ac5_reinserted_name_artifact_denied_by_pii_scan(tmp_path):
    # AC-5 pre-ship (OQ-3 / RT-01): a maintained artifact carrying the REINSERTED operator NAME
    # under vault/artifacts/generated/ is DENIED by the commit/push PII scan (`scan_scoped` over
    # the data-bearing prefix + the identity tokens — the artifact path passed as `data_bearing`
    # mirrors the hook's DATA_BEARING_PREFIXES classification of vault/artifacts/generated/).
    # Paired control: a de-identified (initials-only) artifact under the SAME prefix PASSES. A scan
    # that denies both or neither fails the gate.
    from scripts.guard import pii_scan

    # produce the REAL name-bearing artifact through the tailoring path (reinsert_out re-inserts
    # the synthetic full name onto the confirmable-gitignored target).
    name_text, _ = _run_wire_scan_tailor(tmp_path)
    assert SYNTH_NAME in name_text, "the tailoring path did not re-insert the operator name (feature broken)"
    name_art = tmp_path / "repo" / "vault" / "artifacts" / "generated" / "maintained.html"
    assert name_art.exists()

    # a de-identified counterpart under the SAME prefix (initials only — the reinserted name stripped).
    clean_art = name_art.parent / "maintained-clean.html"
    clean_art.write_text(name_text.replace(SYNTH_NAME, "Patient JQT"), encoding="utf-8")

    identity_cfg = _synth_identity_config(tmp_path)
    contact_cfg = tmp_path / "operator-contact.txt"  # empty synthetic contact config (no tokens)
    contact_cfg.write_text("", encoding="utf-8")

    denied = pii_scan.scan_scoped([str(name_art)], [str(name_art)],
                                  contact_config=contact_cfg, identity_config=identity_cfg)
    passed = pii_scan.scan_scoped([str(clean_art)], [str(clean_art)],
                                  contact_config=contact_cfg, identity_config=identity_cfg)
    assert denied > 0, "the reinserted-name artifact was NOT denied (scan-scope hole over the artifact prefix)"
    assert passed == 0, "the de-identified artifact was wrongly denied (over-block)"
