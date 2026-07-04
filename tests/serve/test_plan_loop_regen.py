"""Re-gen re-summarize path + crown-jewel non-egress wire-scan (ADR-0036-T3).

The T1 binding drives every re-gen through the FULL-COMPOSITION front door
(`plan_loop.regenerate` -> `plan_orchestrator.run_orchestrated` -> `plan_driver.drive`).
T3 pins the two consequences of that binding the loop must GUARANTEE on every re-entry:

  - finding B (re-summarize): `regenerate` re-reads the CURRENT store (`_read_raw_intake`
    per call) and re-enters `run_orchestrated`, so the de-id boundary re-derives
    `recent-trend-direction` from the live `biomarker::` feed on every re-gen (no stale
    summary, no `plan-track::` bridge). Because the re-derived trend differs for a
    behind-goal vs an on-track series, the summary handed to the author differs, so the
    author's disposition differs (the mutation-control pair) — AC-1/AC-2/AC-3.
  - AC-6 (held-domain persistence): clearance is re-derived by the `orchestrate` holds per
    re-gen (never inherited), so a domain held on the new data is NOT recorded.
  - finding C (crown-jewel non-egress): a raw operator identifier / raw med seeded into the
    RAW intake never reaches any specialist-lane dispatch payload on the loop path, and the
    free-text trigger carries only the DERIVED trigger label — never the raw care-chat turn
    text — AC-4/AC-5.

The de-id boundary in these tests is a summarize-backed client (`_SummarizeDeid`): its
`deidentify` returns `router.summarize` over the live store — the SUMMARY_FIELD_SET-shaped
band/class mapping a faithful de-id call emits (the shape `deid_in` whitelists). Every
dispatch / de-id / judge / lens is a mock/fixture; no test hits a live API or reads a real
key, and the tree carries 0 REAL operator PII (synthetic tokens only) — AC-7.
"""

import functools
import json
from pathlib import Path

from scripts.model.client import ModelClient
from scripts.plan import router
from scripts.plan.safety_review import DEFAULT_LENSES
from scripts.serve import care_chat, plan_loop
from scripts.store import loop_schema, plan_schema, store

from tests.plan.test_generate_plan import (
    _author,
    _nutrition_meal_rec,
    _nutrition_target_rec,
    _peptide_rec,
    _seed_store,
    _supplement_rec,
    _workout_rec,
)
from tests.plan.test_orchestrate import _SUPP_CONFLICT, _nutrition, _recon
from tests.plan.test_quality_judge import _clean_scores
from tests.serve.test_care_chat import _RecordingBackend, _seed

# The shared `plan_loop.JUDGE_ROLE` constant (bead 3ge1 concern b), not a re-declared coupled literal.
from scripts.serve.plan_loop import JUDGE_ROLE as _JUDGE_ROLE
_ON_DATE = "2026-06-18"
_SUSTAINED_DATES = ("2026-06-01", "2026-06-08", "2026-06-16")  # 3 readings, 15-day span
_REGRESSING = (60, 50, 40)  # falling hrv -> worst-wins `regressing`
_IMPROVING = (40, 50, 60)   # rising hrv -> `improving`

# Synthetic raw-PII (NEITHER is real operator PII — the tree carries synthetic tokens only).
_SYNTHETIC_NAME = "Jordan Fakename"
_SYNTHETIC_DRUG = "Zalenprax-XR 250mg"


# --- fixtures (0 live spend) --------------------------------------------------------


def _seed_biomarker(root, marker, values, dates):
    """Seed a `biomarker::<marker>` series (one reading per value/date) via the frozen writer."""
    for value, day in zip(values, dates):
        loop_schema.record_biomarker(marker, f"{day}T00:00:00+00:00", value, root)


def _regen_root(tmp_path, name, series):
    """A tmp store: operator + care-profile state, an OLD prior plan, and an hrv `series`.

    The old prior plan (2026-06-01) satisfies the 7-day min-interval; the 3-reading /
    15-day hrv series is the sustained directional signal — together the debounce gate
    passes, so a trigger drives exactly one re-gen dated `_ON_DATE`.
    """
    root = tmp_path / name
    _seed_store(root)
    _seed(root)  # care-profile fields for router.summarize / care_chat
    plan_schema.record_plan(
        "workout", {"exercises": [{"name": "Squat", "sets": 3}]},
        "2026-06-01", "personal-trainer", root,
    )
    _seed_biomarker(root, "hrv", series, _SUSTAINED_DATES)
    return root


def _clean_authors():
    """A clean four-domain author set (disjoint compounds -> no additive-AE hold; all record)."""
    return {
        "workout": _recon(_author(_workout_rec("Goblet squat", 3)), energy_cost_kcal=500),
        "nutrition": _nutrition(
            _nutrition_target_rec(), _nutrition_meal_rec("Breakfast", kcal=600),
            energy_budget={"sustains": True, "sustainable_training_kcal": 700},
        ),
        "supplements": _author(_supplement_rec("Creatine", "5 g"), specialist="supplement-specialist"),
        "peptides": _author(_peptide_rec("BPC-157", "250 mcg", "subq"), specialist="peptide-specialist"),
    }


class _SummarizeDeid:
    """A de-id client whose `deidentify` returns `router.summarize` over the LIVE store.

    The faithful fixture for `deid_in`: the SUMMARY_FIELD_SET-shaped band/class mapping a real
    de-id call emits, re-derived from the current store on every call — so a re-gen re-reading
    the store re-derives `recent-trend-direction` from the live `biomarker::` feed.
    """

    def __init__(self, root):
        self.root = root

    def deidentify(self, raw_intake):
        return router.summarize(functools.partial(store.read, root=self.root))


class _LeakDeid:
    """The inject-key guard: a FAITHLESS de-id that echoes the raw name into an in-set VALUE.

    `active-issue-class` is a SUMMARY_FIELD_SET key, so `deid_in`'s key whitelist passes it; the
    synthetic name is not in the default identity config, so the value-scan passes too — the name
    reaches the dispatch. Proves the wire-scan is FAILING-CAPABLE (it goes RED when raw PII
    actually reaches a specialist payload), so `test_crown_jewel_non_egress_wire_scan`'s
    0-hit assertion tests something, not a tautology.
    """

    def __init__(self, root):
        self.root = root

    def deidentify(self, raw_intake):
        summary = router.summarize(functools.partial(store.read, root=self.root))
        summary["active-issue-class"] = _SYNTHETIC_NAME
        return summary


class _TrendDispatch:
    """The unified subscription dispatch: records every call; the workout author reads the trend.

    Routes specialist / judge / lens by the first arg (the loop's ONE seam). The workout author's
    disposition is a deterministic function of the de-identified `recent-trend-direction` the loop
    handed it: `regressing` -> the DE-LOAD branch, else MAINTAIN — so a run's disposition reflects
    the trend the loop re-derived (the mutation control). `held=True` makes supplements declare a
    cross-domain conflict (no adjudicator -> supplements is HELD, records nothing).

    Attributes:
        held (bool): Whether supplements declares a cross-domain conflict (-> held).
        calls (list): Every `{name, prompt, context}` dispatched (specialist + judge + lens).
        workout_disposition (str | None): `de-load` / `maintain` from the last workout dispatch.
    """

    def __init__(self, *, held=False):
        self.held = held
        self.calls = []
        self.workout_disposition = None

    def __call__(self, name, prompt, context):
        self.calls.append({"name": name, "prompt": prompt, "context": context})
        if name == _JUDGE_ROLE:
            return _clean_scores()
        if name in DEFAULT_LENSES:
            return []
        authors = _clean_authors()
        if self.held:
            authors["supplements"] = _recon(
                _author(_supplement_rec("Fish oil", "2 g"), specialist="supplement-specialist"),
                conflicts=_SUPP_CONFLICT,
            )
        if name == "workout":
            self.workout_disposition = (
                "de-load" if context.get("recent-trend-direction") == "regressing" else "maintain"
            )
        return authors[name]

    def spec_calls(self):
        """The specialist-lane dispatch calls (the four PLAN_DOMAINS), judge/lens excluded."""
        return [c for c in self.calls if c["name"] in plan_schema.PLAN_DOMAINS]


def _plan_rows_on(root, domain, on_date):
    """The `plan::<domain>` rows dated `on_date` under `root`."""
    return [r for r in store.read(f"plan::{domain}", root=root) if r["timepoint"] == on_date]


# =====================================================================================
# Cycle 1 — re-summarize: finding-B trend, mutation control, held-domain persistence ---
# =====================================================================================


def test_trend_reaches_regen_via_summarize(tmp_path):
    # AC-1 (finding B): a re-gen re-summarizes the CURRENT store, so the dispatched summary carries
    # the re-derived `recent-trend-direction` from the live `biomarker::` feed — and the trend rides
    # `router.summarize`, never a `plan-track::` bridge.
    root = _regen_root(tmp_path, "trend", _REGRESSING)

    # (a) the carrying path: summarize derives the trend from the biomarker feed; a store-read spy
    # over the derivation records 0 `plan-track::` reads (the trend is not carried by the tracking prefix).
    trend_expected = router._recent_trend_direction(functools.partial(store.read, root=root))
    assert trend_expected == "regressing", f"the seeded series did not derive regressing: {trend_expected}"
    reads = []

    def _spy_read(item):
        reads.append(item)
        return store.read(item, root=root)

    router.summarize(_spy_read)
    assert not any(i.startswith("plan-track::") for i in reads), (
        f"the trend derivation read a plan-track:: item (bridge, not the biomarker feed): {reads}"
    )

    # (b) fire the loop through the serve-layer debounced entry; the dispatched summary carries it.
    dispatch = _TrendDispatch()
    plan_loop.signal(root, trigger=plan_loop.FREE_TEXT_TRIGGER, dispatch=dispatch,
                     deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    spec = dispatch.spec_calls()
    assert spec, "no specialist dispatch fired (the loop did not re-gen)"
    summary = spec[0]["context"]
    assert summary.get("recent-trend-direction") == "regressing", (
        f"the re-derived trend did not reach the dispatched summary: {summary.get('recent-trend-direction')}"
    )
    assert set(summary) <= set(router.SUMMARY_FIELD_SET), (
        f"the dispatched summary carried an out-of-field-set key: {set(summary) - set(router.SUMMARY_FIELD_SET)}"
    )
    # (c) the loop module carries the trend through NO `plan-track::` bridge.
    assert "plan-track" not in Path("scripts/serve/plan_loop.py").read_text(), (
        "plan_loop.py references plan-track:: (the trend must ride router.summarize, not a track bridge)"
    )


def test_stale_summary_would_miss_the_trend(tmp_path):
    # AC-1 (failing-capable proof): a de-id that does NOT re-summarize the current store — the fixed
    # `_deid_summary()` fixture, which carries no `recent-trend-direction` — hands the author NO trend.
    # Proves `test_trend_reaches_regen_via_summarize`'s trend assertion is not a tautology: it reds when
    # the re-summarize does not happen.
    from tests.plan.test_plan_orchestrator import _deid_summary

    assert "recent-trend-direction" not in _deid_summary(), (
        "the fixed fixture unexpectedly carries a trend — the failing-capable proof is void"
    )
    root = _regen_root(tmp_path, "stale", _REGRESSING)

    class _FixedDeid:
        def deidentify(self, raw_intake):
            return _deid_summary()

    dispatch = _TrendDispatch()
    plan_loop.signal(root, trigger=plan_loop.FREE_TEXT_TRIGGER, dispatch=dispatch,
                     deid_client=_FixedDeid(), plan_date=_ON_DATE)
    spec = dispatch.spec_calls()
    assert spec, "no specialist dispatch fired"
    # a NON-re-summarizing de-id leaves the trend absent — the exact RED the AC-1 assertion guards against
    assert spec[0]["context"].get("recent-trend-direction") is None, (
        "the fixed (non-re-summarizing) de-id somehow carried the trend — the AC-1 guard would be vacuous"
    )


def test_behind_trend_de_loads(tmp_path):
    # AC-2 (mutation control, behind -> de-load): a series trending BEHIND goal (regressing) makes the
    # re-gen express the de-load branch for the affected domain (the author read the re-derived trend).
    root = _regen_root(tmp_path, "behind", _REGRESSING)
    dispatch = _TrendDispatch()
    plan_loop.signal(root, trigger=plan_loop.FREE_TEXT_TRIGGER, dispatch=dispatch,
                     deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert dispatch.workout_disposition == "de-load", (
        f"a behind-goal (regressing) trend did not de-load: {dispatch.workout_disposition}"
    )


def test_mutation_control_pair_differs(tmp_path):
    # AC-3 (mutation control, the falsifiable PAIR): an on-track/ahead series (improving) does NOT
    # de-load, and the behind vs on-track dispositions are NOT equal — proving the re-gen reads the
    # re-derived trend (a rule that ignored the trend would return the same disposition for both).
    behind = _regen_root(tmp_path, "pair-behind", _REGRESSING)
    ahead = _regen_root(tmp_path, "pair-ahead", _IMPROVING)
    d_behind, d_ahead = _TrendDispatch(), _TrendDispatch()
    plan_loop.signal(behind, trigger=plan_loop.FREE_TEXT_TRIGGER, dispatch=d_behind,
                     deid_client=_SummarizeDeid(behind), plan_date=_ON_DATE)
    plan_loop.signal(ahead, trigger=plan_loop.FREE_TEXT_TRIGGER, dispatch=d_ahead,
                     deid_client=_SummarizeDeid(ahead), plan_date=_ON_DATE)
    assert d_ahead.workout_disposition == "maintain", (
        f"an on-track (improving) trend expressed the de-load branch: {d_ahead.workout_disposition}"
    )
    assert d_behind.workout_disposition != d_ahead.workout_disposition, (
        "the behind and on-track dispositions are equal — the re-gen is not reading the re-derived trend"
    )


def test_held_domain_persists_on_regen(tmp_path):
    # AC-6 (held-domain persistence): a domain HELD by the new-data composition (a cross-domain
    # conflict, no adjudicator -> recorded: False) is NOT recorded on the re-gen — clearance is
    # re-derived per re-gen, never inherited. A non-held survivor still records (the pass ran).
    root = _regen_root(tmp_path, "held", _IMPROVING)
    dispatch = _TrendDispatch(held=True)
    result = plan_loop.signal(root, trigger=plan_loop.FREE_TEXT_TRIGGER, dispatch=dispatch,
                              deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    # 0 silently un-held still-unsafe domains: the held supplements domain records NOTHING
    assert _plan_rows_on(root, "supplements", _ON_DATE) == [], (
        "the held supplements domain was recorded on the re-gen (a hold was inherited/bypassed)"
    )
    assert result["results"]["supplements"]["recorded"] is False
    # positive control: a non-held survivor DID record (else the held assertion is vacuous)
    assert len(_plan_rows_on(root, "peptides", _ON_DATE)) == 1, (
        "no survivor recorded — the held-domain assertion would be vacuous"
    )


# =====================================================================================
# Cycle 2 — crown-jewel non-egress wire-scan (finding C) ------------------------------
# =====================================================================================


def _seed_raw_pii(root):
    """Seed synthetic raw PII into the RAW intake: a legal name + a raw med free-text string.

    `legal-name` is not a SUMMARY_FIELD_SET field (summarize never reads it); the raw drug rides a
    named-excluded raw source (`raw-peptide-free-text`) summarize collapses to a coarse class. Both
    live in `store.read_all` — the raw intake the loop de-identifies — so their ABSENCE from the
    dispatch is load-bearing (the loop read a store that HELD them).
    """
    store.append("legal-name", {"item": "legal-name", "timepoint": "2026-06-01T00:00:00+00:00",
                                "source": "intake", "value": _SYNTHETIC_NAME}, root=root)
    store.append("raw-peptide-free-text",
                 {"item": "raw-peptide-free-text", "timepoint": "2026-06-01T00:00:00+00:00",
                  "source": "intake", "value": f"{_SYNTHETIC_DRUG}, BPC-157 250mcg"}, root=root)


def test_crown_jewel_non_egress_wire_scan(tmp_path):
    # AC-4 (crown-jewel non-egress): raw operator PII seeded into the RAW intake reaches NO
    # specialist-lane dispatch payload on the loop path, fired through the free-text (care-chat)
    # trigger. A NEGATIVE assertion over the dumped wire — count of raw-PII hits == 0.
    root = _regen_root(tmp_path, "crown", _REGRESSING)
    _seed_raw_pii(root)

    # the seed genuinely lives in the raw intake the loop reads (so its absence in the wire is real)
    raw_intake = json.dumps(store.read_all(root))
    assert _SYNTHETIC_NAME in raw_intake and _SYNTHETIC_DRUG in raw_intake, (
        "the synthetic raw PII was not seeded into the raw intake — the wire-scan would be vacuous"
    )

    dispatch = _TrendDispatch()
    care_chat.respond("my hrv keeps dropping and I feel wiped out", [], client=_RecordingBackend(),
                      store_root=root, loop_dispatch=dispatch, loop_deid_client=_SummarizeDeid(root))
    spec = dispatch.spec_calls()
    assert spec, "no specialist dispatch fired through the care-chat trigger (the loop did not re-gen)"
    wire = json.dumps(dispatch.calls)

    # the crown-jewel negative assertion: 0 raw-PII hits in ANY dispatch payload
    assert _SYNTHETIC_NAME not in wire, "the raw legal name reached a specialist dispatch payload (de-id breach)"
    assert _SYNTHETIC_DRUG not in wire, "the raw med name reached a specialist dispatch payload (de-id breach)"
    # positive control: the wire genuinely carries dispatched de-id content (not an empty pass)
    assert '"recent-trend-direction": "regressing"' in wire, (
        "the dispatched wire carried no de-identified summary content — the 0-hit scan is vacuous"
    )


def test_wire_scan_reds_when_pii_reaches_the_dispatch(tmp_path):
    # AC-4 (failing-capable / the inject-key guard): a FAITHLESS de-id that echoes the raw name into
    # an in-set field VALUE (`_LeakDeid`) passes `deid_in`'s whitelist + default value-scan, so the
    # name REACHES the dispatch — and the wire-scan assertion goes RED. Proves
    # `test_crown_jewel_non_egress_wire_scan` tests something (the boundary blocks a real leak).
    root = _regen_root(tmp_path, "leak", _REGRESSING)
    _seed_raw_pii(root)
    dispatch = _TrendDispatch()
    care_chat.respond("my hrv keeps dropping", [], client=_RecordingBackend(), store_root=root,
                      loop_dispatch=dispatch, loop_deid_client=_LeakDeid(root))
    assert dispatch.spec_calls(), "the leak de-id produced no dispatch (the guard is void)"
    wire = json.dumps(dispatch.calls)
    assert _SYNTHETIC_NAME in wire, (
        "a de-id that echoed the raw name into an in-set value did NOT surface in the wire — the "
        "wire-scan would not catch a real leak (tautology)"
    )


def test_free_text_payload_is_derived_tokens_only(tmp_path):
    # AC-5 (raw free-text cannot reach the dispatch): the free-text trigger's dispatch payload carries
    # ONLY de-identified summary tokens (keys ⊆ SUMMARY_FIELD_SET) and 0 raw care-chat turn strings —
    # the notify carries the DERIVED trigger label, never the raw turn text (finding-C).
    root = _regen_root(tmp_path, "derived", _REGRESSING)
    _seed_raw_pii(root)
    turn = "my hrv keeps dropping and I take Zalenprax every morning"
    dispatch = _TrendDispatch()
    care_chat.respond(turn, [], client=_RecordingBackend(), store_root=root,
                      loop_dispatch=dispatch, loop_deid_client=_SummarizeDeid(root))
    spec = dispatch.spec_calls()
    assert spec, "no specialist dispatch fired"
    for call in spec:
        assert set(call["context"]) <= set(router.SUMMARY_FIELD_SET), (
            f"a dispatch payload carried an out-of-field-set key: "
            f"{set(call['context']) - set(router.SUMMARY_FIELD_SET)}"
        )
    wire = json.dumps(dispatch.calls)
    assert turn not in wire, "the raw care-chat turn text reached a specialist dispatch payload (finding-C)"


def test_regen_suite_makes_no_live_backend_call(tmp_path, monkeypatch):
    # AC-7: the re-gen loop runs over injected mocks only — it constructs no `ModelClient` (and thus
    # no live no-train backend). A `ModelClient.__init__` spy confirms 0 self-constructed clients on
    # the loop path (0 live spend).
    instantiations = []
    real_init = ModelClient.__init__

    def spy_init(self, *args, **kwargs):
        instantiations.append(self)
        return real_init(self, *args, **kwargs)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)

    root = _regen_root(tmp_path, "no-live", _REGRESSING)
    dispatch = _TrendDispatch()
    plan_loop.signal(root, trigger=plan_loop.FREE_TEXT_TRIGGER, dispatch=dispatch,
                     deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert dispatch.spec_calls(), "no dispatch fired"
    assert instantiations == [], "the re-gen path constructed a ModelClient (must use only injected mocks)"
