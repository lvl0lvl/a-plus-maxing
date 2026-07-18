"""Front-door authoring reads the assembled record, not the router.summarize band (ADR-0050-T1).

`_do_generate_plan` (the POST /generate-plan front door) must author EVERY domain — the candidate
renderable pass AND the Leg-2 rich-domain synthesize pass — against
`context_assembler.assemble_context(store_read)`'s identity-stripped FULL record, not the coarse
`router.summarize` band. The spy `self.client` records each `(domain, summary_arg)` so the tests
partition the captured author calls by renderable-membership and pin the enriched free-text at BOTH
author sites (anti-vacuity: the Leg-2 partition is HARD-asserted non-empty, so a fixture that later
drops the rich domain REDs here instead of passing the EVERY-call universal vacuously).

Everything is SYNTHETIC — a scratch tmp store, a spy author (0 live API, 0 key, 0 spend), env
untouched. Author counts are DERIVED from the seeded store's active set, never observed-then-hardcoded.
"""

import datetime
import functools
import io
import json
import subprocess
from email.message import Message
from pathlib import Path

from scripts.plan import context_assembler, router
from scripts.plan.assemble import PROGRAM_KEY
from scripts.serve import plan_loop
from scripts.serve import server as serve_server
from scripts.store import keying, plan_schema, store

from tests.store.test_plan_model import _training_program

REPO_ROOT = Path(__file__).resolve().parents[2]

# The ADR-0032 frozen-six freeze base (AC-5) — the recipe's rollback anchor, a permanent main
# ancestor, so its numstat vs the working tree equals this task's diff on the frozen set (empty).
_FROZEN_SIX_BASE = "3ab1c3abb6c995fbaaadcb179735759e4a61d73d"
_FROZEN_SIX = (
    "scripts/store/store.py", "scripts/store/keying.py", "scripts/plan/pipeline.py",
    "scripts/plan/adjudicate.py", "scripts/plan/adjust.py", "scripts/plan/router.py",
)

# The three raw health-substance free-text classes assemble_context carries UNCOLLAPSED and
# router.summarize does NOT (it collapses/drops them) — the enriched-record-vs-band discriminator.
_FREE_TEXT_KEYS = (
    "raw-training-detail-free-text",
    "raw-symptom-free-text",
    "raw-supplement-free-text",
)


class _SpyAuthorClient:
    """A spy no-train author: records each (domain, summary_arg), returns a per-domain envelope."""

    def __init__(self, envelopes):
        self._envelopes = envelopes
        self.calls = []  # list[(domain, summary_arg)]

    def author(self, domain, summary):
        self.calls.append((domain, summary))
        return self._envelopes[domain]


def _rec(claim, category, source, payload):
    """A complete HALT-clearing universal recommendation (the assemble survival contract)."""
    return {
        "claim": claim, "source": source, "confidence_tier": "established",
        "reversibility": "fully reversible on discontinuation", "category": category,
        "payload": payload,
    }


def _envelopes():
    """Per-domain author envelopes: four RECORDING renderable domains + one rich (sleep) domain.

    The renderable set is disjoint compounds (creatine / BPC-157) so the frozen orchestrate records
    the active renderables (any(recorded) True -> Leg 2 fires); sleep carries a conformant DOMAIN
    PROGRAM the Leg-2 synthesize folds. Envelopes for every renderable + sleep are present so the
    spy never KeyErrors on whichever subset the seed activates.
    """
    return {
        "workout": {"specialist": "personal-trainer", "recommendations": [
            _rec("rebuild a movement base with goblet squats", "training",
                 "ACSM resistance-training guidelines 2024",
                 {"name": "Goblet squat", "sets": 3, "reps": "8-12", "detail": "controlled tempo"})]},
        "nutrition": {"specialist": "nutritionist", "recommendations": [
            _rec("set energy and protein at maintenance to support recovery", "nutrition",
                 "ISSN position stand on protein and exercise 2017",
                 {"calorie_goal": 2600, "macros": {"protein": 190, "carbs": 250, "fat": 80}})]},
        "supplements": {"specialist": "supplement-specialist", "recommendations": [
            _rec("supplement creatine to close a documented gap", "supplementation",
                 "Examine.com creatine monograph 2024",
                 {"name": "Creatine monohydrate", "dose": "5 g", "timing": "daily"})]},
        "peptides": {"specialist": "peptide-specialist", "recommendations": [
            _rec("run bpc-157 for localized tissue support", "peptide-therapy",
                 "vault/library/peptides/bpc-157 research-report 2026",
                 {"compound": "BPC-157", "dose": "250 mcg", "route": "subcutaneous"})]},
        "sleep": {"specialist": "sleep-specialist", "recommendations": [{
            "claim": "consolidate sleep with a fixed wake time", "category": "sleep",
            "source": "vault/library sleep-hygiene review 2026", "confidence_tier": "established",
            "reversibility": "fully reversible on discontinuation", "payload": {},
            PROGRAM_KEY: _training_program(),
        }]},
    }


def _seed(root):
    """Seed a PII-free operator state that activates sleep (rich) + recording renderables.

    `goal-domains` projects the card-domain slugs; the three raw health-substance free-text classes
    are what `assemble_context` carries UNCOLLAPSED. Values are synthetic health text — NO genotype
    pattern, NO operator-identity token — so the assembler value gate passes (else it fail-closes).
    """
    fields = {
        "goal-domains": "workout nutrition sleep",
        "goal-targets": "return to pre-Jan-2026 loading",
        "goal-priority-order": "recovery>strength",
        "recovery-status-band": "moderate",
        "hard-limits": "no overhead pressing",
        "raw-training-detail-free-text": "upper/lower split three days a week, moderate accessory volume",
        "raw-symptom-free-text": "left shoulder impingement, overhead pressing limited",
        "raw-supplement-free-text": "creatine monohydrate five grams daily, magnesium glycinate at night",
    }
    for item, value in fields.items():
        store.append(
            item,
            {f: None for f in keying.LINE_FIELDS}
            | {"item": item, "timepoint": "2026-07-13", "source": "intake", "value": value},
            root=root,
        )
    return functools.partial(store.read, root=root)


def _drive_generate_plan_inproc(store_root, spy):
    """Drive `_do_generate_plan` in-process (no socket); mirror _drive_confirm_plan_change_inproc.

    Every response path reads `requestline`/`request_version` via _write_json -> send_response, so
    they are NOT optional; `client` + a resolving `key_resolver` make the no-key guard pass.
    """
    bound = type("BoundIntakeRequestHandler", (serve_server.IntakeRequestHandler,),
                 {"store_root": store_root})
    handler = bound.__new__(bound)
    handler.path = "/generate-plan"
    handler.command = "POST"
    handler.requestline = "POST /generate-plan HTTP/1.1"
    handler.request_version = "HTTP/1.1"
    headers = Message()
    headers["Content-Type"] = "application/json"
    handler.headers = headers
    handler.rfile = io.BytesIO(b"{}")
    handler.wfile = io.BytesIO()
    handler.client = spy
    handler.key_resolver = (lambda: object())  # _key_available() truthy, no live key resolved
    handler._do_generate_plan()
    return handler.wfile.getvalue()


def _run(tmp_path):
    """Seed, drive the front door with a spy, return the harness bundle the ACs pin."""
    root = tmp_path / "store"
    store_read = _seed(root)
    spy = _SpyAuthorClient(_envelopes())
    _drive_generate_plan_inproc(root, spy)
    summary = router.summarize(store_read)
    active = plan_loop.active_plan_domains(summary)
    renderable = set(plan_schema.RENDERABLE_DOMAINS)
    renderable_active = sorted(active & renderable)
    rich_active = sorted(active - renderable)
    candidate_calls = [(d, s) for (d, s) in spy.calls if d in renderable]
    leg2_calls = [(d, s) for (d, s) in spy.calls if d not in renderable]
    return {
        "spy": spy, "store_read": store_read,
        "renderable_active": renderable_active, "rich_active": rich_active,
        "candidate_calls": candidate_calls, "leg2_calls": leg2_calls,
    }


def _free_text_count(summary_arg):
    """How many of the three assemble_context free-text classes the author input carries."""
    return sum(1 for k in _FREE_TEXT_KEYS if k in summary_arg)


def test_every_author_call_carries_the_assembled_free_text(tmp_path):
    # AC-1: EVERY captured author call (candidate @832 + Leg-2 @862) receives assemble_context's
    # record -> >=3 free-text fields. RED against the pre-repoint server.py (both sites author the
    # router.summarize band, which lacks the free-text keys).
    h = _run(tmp_path)
    assert h["spy"].calls, "no author call was captured (the front door never authored)"
    for domain, summary_arg in h["spy"].calls:
        assert _free_text_count(summary_arg) >= 3, (
            f"{domain}: the author input carries {_free_text_count(summary_arg)} free-text field(s) "
            f"(<3) — it is the router.summarize band, not the assembled record"
        )


def test_leg2_rich_partition_nonempty_and_carries_free_text(tmp_path):
    # AC-1 anti-vacuity (QA MUST-FIX): the Leg-2 partition (domain NOT in RENDERABLE_DOMAINS) is
    # HARD-asserted NON-EMPTY (proves @862 actually fired) AND carries >=3 free-text fields
    # SPECIFICALLY — so the EVERY-call universal is not vacuously true over candidate calls only.
    # A later fixture edit dropping the rich domain then REDs here rather than passing vacuously.
    h = _run(tmp_path)
    assert h["leg2_calls"], (
        "the Leg-2 rich author partition (domain NOT in RENDERABLE_DOMAINS) is EMPTY — @862 never "
        "fired; the AC-1 EVERY-call universal would be vacuously true over candidate calls alone"
    )
    for domain, summary_arg in h["leg2_calls"]:
        assert _free_text_count(summary_arg) >= 3, (
            f"Leg-2 {domain}: the @862 rich author received the band, not the assembled record"
        )


def test_band_lacks_free_text_keys_nontautology_anchor(tmp_path):
    # AC-2 in-test anchor: the router.summarize band does NOT carry the three free-text keys (and the
    # assembled record DOES). This proves the AC-1 assertion genuinely DISTINGUISHES the enriched
    # record from the band — reverting either author site back to the band REDs AC-1, non-tautologically.
    h = _run(tmp_path)
    band = router.summarize(h["store_read"])  # the same one-arg band the pre-repoint code authored
    assert _free_text_count(band) == 0, (
        f"the band already carries free-text keys {sorted(band)} — the AC-1 assertion would pass "
        f"against the band too (tautological)"
    )
    assembled = context_assembler.assemble_context(h["store_read"])
    assert _free_text_count(assembled) >= 3, "the assembled record must carry the discriminating keys"


def test_candidate_selection_still_reads_the_band(tmp_path):
    # AC-3: active-domain selection is UNCHANGED by the repoint — the candidate partition's domain
    # set equals the band-derived active ∩ RENDERABLE_DOMAINS (selection reads the band, @815-817
    # left intact), even though the author INPUT is now the enriched record.
    h = _run(tmp_path)
    candidate_domains = sorted({d for (d, _s) in h["candidate_calls"]})
    band_selection = sorted(
        plan_loop.active_plan_domains(router.summarize(h["store_read"]))
        & set(plan_schema.RENDERABLE_DOMAINS)
    )
    assert candidate_domains == band_selection, (candidate_domains, band_selection)


def test_no_new_author_call_concrete_derived_count(tmp_path):
    # AC-4: the repoint adds NO new model call. len(spy.calls) == renderable-active + rich-active, a
    # count DERIVED from the seeded store's active set (the two partitions cover `active` disjointly),
    # NOT observed-then-hardcoded. A double-author (e.g. re-authoring per site) would RED this.
    h = _run(tmp_path)
    expected = len(h["renderable_active"]) + len(h["rich_active"])
    assert len(h["spy"].calls) == expected, (
        f"{len(h['spy'].calls)} author calls != {expected} "
        f"(renderable_active {h['renderable_active']} + rich_active {h['rich_active']})"
    )


def test_frozen_six_stays_byte_frozen(tmp_path):
    # AC-5: the ADR-0032 frozen six stay byte-frozen — the numstat vs the freeze base is empty.
    out = subprocess.run(
        ["git", "diff", "--numstat", _FROZEN_SIX_BASE, "--", *_FROZEN_SIX],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    assert out.strip() == "", f"a frozen-six file changed vs {_FROZEN_SIX_BASE}: {out}"


def test_module_is_zero_spend_no_live_client(tmp_path):
    # AC-6 ($0): the module constructs NO live client and carries no real operator-identity literal —
    # the drive runs on a spy, no network, no key. Needles are concatenated at runtime so they never
    # self-match this assertion's own source text. The spy-driven front door authored end-to-end.
    src = Path(__file__).read_text(encoding="utf-8")
    assert ("Model" + "Client(") not in src, "no live ModelClient may be constructed"
    assert ("wmcgiv" + "ney") not in src, "no real operator identity literal"
    assert ("@gmail" + ".com") not in src, "no real operator email literal"
    h = _run(tmp_path)
    assert h["spy"].calls, "the spy-driven front door made no author call"


def test_front_door_fail_closes_before_any_author_call(tmp_path):
    # SAFETY: the @823 assemble_context(store_read) runs BEFORE the author loop, so a raw genotype
    # smuggled into an allowlisted health-substance free-text field fail-closes the WHOLE run into
    # the @876 degrade envelope — with NO operator PII reaching the no-train author. router.summarize
    # (@815) neither carries nor scans raw-symptom-free-text, so assemble_context is the gate that
    # trips. Seed the active PII-free state, then overwrite the symptom text with a genotype.
    root = tmp_path / "store"
    _seed(root)
    store.append(
        "raw-symptom-free-text",
        {f: None for f in keying.LINE_FIELDS}
        | {"item": "raw-symptom-free-text", "timepoint": "2026-07-14", "source": "intake",
           "value": "left shoulder pain; MTHFR rs1801133 = (C;T) flagged in report"},
        root=root,
    )
    spy = _SpyAuthorClient(_envelopes())
    raw = _drive_generate_plan_inproc(root, spy)
    body = json.loads(raw.split(b"\r\n\r\n", 1)[1].decode("utf-8"))
    # (a) the whole-run fail-closed degrade envelope (server.py:881-882).
    assert body["degraded"] is True, body
    assert body["reason"] == "could not generate plan", body
    assert body["plan_html"] is None, body
    # (b) LOAD-BEARING: the fail-closed raise fired BEFORE any author call, so NO operator PII
    # reached the model client — the spy captured zero author calls. REDs if @823 moves past the loop.
    assert spy.calls == [], f"an author call fired despite the fail-close: {spy.calls}"
    # (c) nothing was recorded — every plan domain resolves to NO_PLAN for today.
    today = datetime.date.today().isoformat()
    for domain in plan_schema.PLAN_DOMAINS:
        resolved = plan_schema.read_plan(domain, today, root)
        assert resolved["plan"] is None, (domain, resolved)
