"""Tests for the doctor-visit SBAR handout template (the dvq::queue render surface).

Pins the SBAR section anatomy through the PRODUCTION path
(`generate.run("handout")` over stores seeded via the published writers), the
flagged-interactions render off the `dvq::queue` (severity-ranked, the disposition
value-domain, grade/watchlist tolerance, the honest empty-queue absence), the
honesty gates (Situation/Assessment awaiting, the regimen from the day's plans,
no clinical verdict, initials-only header), the store-adversarial battery
(cross-stream isolation, same-finding dedupe, a mutation-style proof), escaping,
and the single-file inert contract. The dvq render is mutation-proven RED: the
seeded cautions appear ONLY because the render reads the queue.
"""

import datetime
from pathlib import Path

import pytest

from scripts.generate import generate, render
from scripts.store import loop_schema, plan_confirm, plan_schema, queue_schema, store
from vault.design.templates import component_set as cs
from vault.design.templates import handout

_TODAY = datetime.date(2026, 6, 20)
_ISO = "2026-06-20"

# The header's two states: an unfilled scaffold (full name in the title, every
# field a `<...>` prompt) and a filled copy. The header must render INITIALS only.
_SCAFFOLD_PROFILE = """# Operator Profile — Walter McGivney

## Demographics
- **Age:** <years>
- **Current status:** <resolved | improving | stable | ongoing>
"""

_FILLED_PROFILE = """# Operator Profile — Walter McGivney

## Demographics
- **Age:** 44

## January 2026 health issue
- **Current status:** improving
"""


def _finding(finding_id, *, caution, axis="rx-bpmh", source_specialist="supplement-specialist",
             outcome="block-stands", non_overridable=False, band=None, **extra):
    """Build one dvq queue entry in the shape `_doctor_visit_queue_entry` writes."""
    return {
        "finding_id": finding_id, "axis": axis, "caution": caution,
        "held_domain": "supplements", "source_specialist": source_specialist,
        "outcome": outcome, "non_overridable": non_overridable,
        "composite_band": band, "harm_class": None, **extra,
    }


def _seed_findings(root):
    """Seed three adjudicated findings, out of severity order on purpose."""
    queue_schema.record_doctor_visit_queue_entry(
        _finding("ae:bpc", caution="BPC-157 experimental — no firm human safety base-rate.",
                 axis="additive-ae", source_specialist="peptide-specialist",
                 outcome="cleared-with-override", band="MEDIUM"),
        _ISO, root)
    queue_schema.record_doctor_visit_queue_entry(
        _finding("rx:warfarin", caution="Omega-3 + warfarin — additive bleeding risk; monitor.",
                 outcome="block-stands", band="HIGH"),
        _ISO, root)
    queue_schema.record_doctor_visit_queue_entry(
        _finding("rx:vitk", caution="Vitamin K + warfarin — non-overridable auto-block.",
                 outcome="block-stands", non_overridable=True, band="CRITICAL"),
        _ISO, root)


def _seed_plans(root, on_date=_ISO):
    """Seed today's supplements + experimental peptides plans."""
    plan_schema.record_plan(
        "supplements",
        {"items": [{"name": "Creatine", "dose": "5 g"}, {"name": "Omega-3", "dose": "2 g"}]},
        on_date, "supplement-specialist", root)
    plan_schema.record_plan(
        "peptides",
        {"compound": "bpc-157", "dose": "250 mcg", "route": "subq", "tags": ["experimental"]},
        on_date, "peptide-specialist", root)


def _seed_asks(root):
    """Seed one pending panel, one resolved panel, one answered watch-out."""
    loop_schema.record_pending_panel("ferritin", "2026-06-10T00:00:00+00:00", root)
    loop_schema.record_pending_panel("lipid-panel", "2026-06-01T00:00:00+00:00", root)
    loop_schema.record_panel_result("lipid-panel", "complete", "2026-06-05T00:00:00+00:00", root)


def _emit(root, tmp_path, today=_TODAY):
    """Render the handout through the production path and return its HTML."""
    return generate.run("handout", _root=root, _out_dir=tmp_path / "out", _today=today).read_text()


def _between(html, start, end):
    """Slice the markup between two unique anchors (section scoping)."""
    return html[html.index(start) + len(start):html.index(end, html.index(start))]


def _interactions(html):
    """The flagged-interactions section body (the title's `&` renders as `&amp;`)."""
    return _between(html, "flagged interactions", "Assessment —")


# --- structure -------------------------------------------------------------

def test_handout_renders_all_sbar_sections(tmp_path):
    """The five SBAR sections + header + footer render in order."""
    html = _emit(tmp_path / "store", tmp_path)
    for anchor in (
        "A+ Maxing — Doctor Visit Handout",
        "Situation — top of mind for this visit",
        "Background — current regimen",
        "Background — flagged interactions",
        "Assessment — patient-observed patterns",
        "Recommendation — questions",
        "hd-foot",
    ):
        assert anchor in html, anchor
    # SBAR order: Situation precedes the two Backgrounds precede Assessment precedes Recommendation.
    assert (html.index("Situation —") < html.index("current regimen")
            < html.index("flagged interactions") < html.index("Assessment —")
            < html.index("Recommendation —"))


# --- AC2: the flagged-interactions render off dvq::queue (mutation-proven) --

def test_flagged_interactions_render_from_dvq_queue(tmp_path):
    """Every seeded finding's caution renders — proving the render reads the queue."""
    root = tmp_path / "store"
    _seed_findings(root)
    section = _interactions(_emit(root, tmp_path))
    assert "Omega-3 + warfarin" in section
    assert "Vitamin K + warfarin" in section
    assert "BPC-157 experimental" in section
    # MUTATION proof: with NO queue entries the section renders the honest absence,
    # NOT these cautions — so their presence is caused by the dvq read.
    empty = _interactions(_emit(tmp_path / "empty", tmp_path))
    assert "No flagged interactions or contraindications on file." in empty
    assert "warfarin" not in empty


def test_finding_disposition_value_domain(tmp_path):
    """Each disposition renders its correct PALETTE chip; a None band is omitted."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("a", caution="auto", non_overridable=True, outcome="block-stands", band="CRITICAL"), _ISO, root)
    queue_schema.record_doctor_visit_queue_entry(
        _finding("b", caution="unresolved", outcome="block-stands", band="HIGH"), _ISO, root)
    queue_schema.record_doctor_visit_queue_entry(
        _finding("c", caution="cleared", outcome="cleared-with-override", band=None), _ISO, root)
    section = _interactions(_emit(root, tmp_path))
    # non-overridable -> auto-block, concern tint; block-stands -> unresolved, concern;
    # cleared-with-override -> on record, watch.
    assert "pill tint-concern'>auto-block — do not proceed" in section
    assert "pill tint-concern'>unresolved — discuss" in section
    assert "pill tint-watch'>on record — proceeding with consent" in section
    # A None composite_band renders NO band token (never a fabricated band).
    cleared_row = _between(section, "cleared", "</div>")
    assert "CRITICAL" not in cleared_row and "HIGH" not in cleared_row and "MEDIUM" not in cleared_row


def test_findings_severity_ranked(tmp_path):
    """The render preserves queue_schema's order: auto-block > block-stands > cleared."""
    root = tmp_path / "store"
    _seed_findings(root)
    section = _interactions(_emit(root, tmp_path))
    assert (section.index("Vitamin K + warfarin")        # non-overridable (tier 0)
            < section.index("Omega-3 + warfarin")        # block-stands HIGH (tier 1)
            < section.index("BPC-157 experimental"))      # cleared MEDIUM (tier 2)


def test_grade_watchlist_tolerated_absent_and_rendered_present(tmp_path):
    """A finding with no grade renders cleanly; a finding with a grade shows its chip."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("no-grade", caution="ungraded finding", band="HIGH"), _ISO, root)
    queue_schema.record_doctor_visit_queue_entry(
        _finding("graded", caution="graded finding", band="HIGH", grade="moderate"), _ISO, root)
    section = _interactions(_emit(root, tmp_path))
    assert "ungraded finding" in section          # no KeyError, renders without a grade
    assert "GRADE moderate" in section            # the optional liaison annotation, when present


def test_finding_source_attribution(tmp_path):
    """Each finding names its source specialist + axis + real band (the §9.4 provenance)."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("x", caution="c", axis="rx-bpmh", source_specialist="supplement-specialist", band="HIGH"),
        _ISO, root)
    section = _interactions(_emit(root, tmp_path))
    assert "via supplement-specialist · supplement–Rx (BPMH) · HIGH" in section


def test_caution_absent_renders_em_dash_not_none(tmp_path):
    """A finding with no caution renders an em-dash, never the literal 'None'."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        {"finding_id": "nc", "axis": "rx-bpmh", "held_domain": "supplements",
         "source_specialist": "supplement-specialist", "outcome": "block-stands",
         "non_overridable": False, "composite_band": "HIGH"},   # no 'caution' key
        _ISO, root)
    row = _between(_interactions(_emit(root, tmp_path)), "class='hd-find'", "</div>")
    assert ">None<" not in row
    assert "<span>—</span>" in row


def test_unknown_composite_band_is_omitted(tmp_path):
    """A band outside the data layer's known set is not displayed as a real band."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("ub", caution="finding with a garbage band", band="WOBBLE"), _ISO, root)
    section = _interactions(_emit(root, tmp_path))
    assert "finding with a garbage band" in section   # the finding still renders
    assert "WOBBLE" not in section                     # ...but the unknown band is omitted


def test_unknown_outcome_surfaces_not_downgrades(tmp_path):
    """An unrecognized outcome surfaces for discussion (concern), never as consent."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("uo", caution="finding with an unknown outcome",
                 outcome="deferred-pending-labs", band="HIGH"), _ISO, root)
    section = _interactions(_emit(root, tmp_path))
    assert "pill tint-concern'>disposition unverified — discuss" in section
    assert "on record — proceeding with consent" not in section


def test_empty_queue_states_absence_not_safety(tmp_path):
    """An empty queue states 'none on file' — never the unstated claim 'you are safe'."""
    section = _interactions(_emit(tmp_path / "store", tmp_path))
    assert "No flagged interactions or contraindications on file." in section
    assert "Findings appear here when the plan pipeline adjudicates a safety concern." in section
    # states absence, never an affirmative all-clear / "you are safe" reassurance.
    assert "all clear" not in section.lower()
    assert "you are safe" not in section.lower()


# --- AC3: regimen + recommendation + honesty gates -------------------------

def test_regimen_renders_from_plans(tmp_path):
    """Supplements + the experimental peptide render from the day's plans."""
    root = tmp_path / "store"
    _seed_plans(root)
    html = _emit(root, tmp_path)
    regimen = _between(html, "current regimen", "flagged interactions")
    assert "Creatine — 5 g" in regimen
    assert "Omega-3 — 2 g" in regimen
    assert "bpc-157 · 250 mcg · subq" in regimen
    assert "experimental — disclosure attached" in regimen
    # The Rx-BPMH reconciliation is an honest awaiting sub-line.
    assert "Prescription medications reconcile here when the medication-reconciliation (BPMH) intake lands." in regimen


def test_regimen_awaiting_when_no_plan_today(tmp_path):
    """No plan dated today -> the honest awaiting line, never an invented regimen."""
    regimen = _between(_emit(tmp_path / "store", tmp_path), "current regimen", "flagged interactions")
    assert "No supplement or peptide plan recorded for today." in regimen


def test_held_supplements_plan_absent_from_regimen(tmp_path):
    """A HELD (pending-pointer) supplements plan does NOT render in the SBAR regimen; a
    co-seeded non-held peptides plan still renders (the render-side confirm filter drops only
    the held domain). RED before the fix (bead a-plus-maxing-zsre): the handout resolves raw
    `plan::` readings without `plan_confirm.filter_confirmed`, so the held plan leaks in as
    the standing 'current regimen'."""
    root = tmp_path / "store"
    plan_schema.record_plan(
        "supplements", {"items": [{"name": "Creatine", "dose": "5 g"}]},
        _ISO, "supplement-specialist", root)
    plan_confirm.mark_pending("supplements", _ISO, root)
    plan_schema.record_plan(
        "peptides", {"compound": "bpc-157", "dose": "250 mcg", "route": "subq"},
        _ISO, "peptide-specialist", root)

    regimen = _between(_emit(root, tmp_path), "current regimen", "flagged interactions")
    assert "Creatine" not in regimen, "a HELD supplements plan leaked into the regimen"
    assert "bpc-157 · 250 mcg · subq" in regimen, "the non-held peptides plan must still render"


def test_non_experimental_peptide_has_no_disclosure_note(tmp_path):
    """A peptide without the experimental tag renders the row but no disclosure note."""
    root = tmp_path / "store"
    plan_schema.record_plan(
        "peptides", {"compound": "tb-500", "dose": "2 mg", "route": "subq", "tags": []},
        _ISO, "peptide-specialist", root)
    regimen = _between(_emit(root, tmp_path), "current regimen", "flagged interactions")
    assert "tb-500 · 2 mg · subq" in regimen
    assert "experimental — disclosure attached" not in regimen


def test_footer_renders_tier_legend_and_honesty(tmp_path):
    """The footer carries the source-tier legend words + the honesty + no-record lines."""
    foot = _between(_emit(tmp_path / "store", tmp_path), "hd-foot", "</body>")
    assert "lab-grade" in foot and "consumer wearable" in foot and "self-reported" in foot
    assert "every value tagged · gaps stated, never inferred" in foot
    assert "not a medical record" in foot


def test_recommendation_questions_and_requests_only(tmp_path):
    """Recommendation renders requests + questions only, behind the no-verdict disclaimer."""
    root = tmp_path / "store"
    _seed_plans(root)
    _seed_asks(root)
    html = _emit(root, tmp_path)
    rec = _between(html, "Recommendation — questions", "hd-foot")
    assert "this sheet states no diagnosis or prescription" in rec
    assert "Requests — order today:" in rec
    assert "Ferritin" in rec or "ferritin" in rec.lower()   # the pending panel chip
    assert "Questions:" in rec
    # the derived watch-out questions render by display name (bpc-157's protocol)
    assert "Injection Site Reaction" in rec and "Appetite Change" in rec


def test_recommendation_answered_watchout_is_filtered(tmp_path):
    """An answered watch-out drops from the Questions queue; unanswered ones remain."""
    root = tmp_path / "store"
    _seed_plans(root)
    loop_schema.record_watchout_answer(
        "appetite_change", "no change", "2026-06-10T00:00:00+00:00", root)
    rec = _between(_emit(root, tmp_path), "Recommendation — questions", "hd-foot")
    assert "Appetite Change" not in rec            # answered -> filtered out
    assert "Injection Site Reaction" in rec        # unanswered -> still queued


def test_recommendation_empty_states(tmp_path):
    """No pending panels + no active protocol -> both honest none-states render."""
    rec = _between(handout.render([], _today=_TODAY), "Recommendation — questions", "hd-foot")
    assert "none pending" in rec
    assert "none queued" in rec


def test_situation_and_assessment_are_honest_awaiting(tmp_path):
    """Situation + Assessment render awaiting copy (operator-authored, not invented)."""
    html = _emit(tmp_path / "store", tmp_path)
    situation = _between(html, "Situation — top of mind for this visit", "Background — current regimen")
    assert "awaiting" in situation and "operator-authored" in situation
    assessment = _between(html, "Assessment — patient-observed patterns", "Recommendation —")
    assert "patient observation — not a diagnosis" in assessment
    assert "awaiting" in assessment


def test_sheet_adds_no_prescriptive_verdict_of_its_own(tmp_path):
    """The sheet's OWN copy is non-prescribing.

    The disclaimers render, AND — given neutral source cautions (the seeded
    findings carry none) — no STOP/START/prescribe/discontinue verb appears
    anywhere. Cautions are verbatim source text, so this proves the sheet itself
    adds no clinical verdict (the negative assertion QA found missing).
    """
    root = tmp_path / "store"
    _seed_findings(root)   # neutral cautions — no prescription verbs
    _seed_plans(root)
    html = _emit(root, tmp_path)
    assert "states no diagnosis or prescription" in html
    assert "renders no clinical verdict" in html
    low = html.lower()
    for verb in ("stop ", "start ", "prescribe", "discontinue"):
        assert verb not in low, verb


# --- PII: initials only ----------------------------------------------------

def test_header_initials_only_never_full_name(tmp_path, monkeypatch):
    """A filled profile renders INITIALS only — the full name never reaches the page."""
    profile = tmp_path / "filled.md"
    profile.write_text(_FILLED_PROFILE, encoding="utf-8")
    monkeypatch.setattr(handout, "_PROFILE_PATHS", (profile,))
    html = handout.render([], _today=_TODAY)
    assert "Patient WM" in html              # initials of "Walter McGivney"
    assert "age band 40s" in html
    assert "issue status improving" in html
    assert "Walter" not in html and "McGivney" not in html


def test_header_em_dash_when_profile_absent(tmp_path, monkeypatch):
    """No profile file -> every header field renders its em-dash awaiting slot."""
    monkeypatch.setattr(handout, "_PROFILE_PATHS", (tmp_path / "absent.md",))
    html = handout.render([], _today=_TODAY)
    assert "Patient — · age band — · issue status —" in html


def test_unfilled_scaffold_renders_initials_only(tmp_path, monkeypatch):
    """An unfilled scaffold still renders only the title initials, fields em-dash."""
    profile = tmp_path / "scaffold.md"
    profile.write_text(_SCAFFOLD_PROFILE, encoding="utf-8")
    monkeypatch.setattr(handout, "_PROFILE_PATHS", (profile,))
    html = handout.render([], _today=_TODAY)
    assert "Patient WM · age band — · issue status —" in html
    assert "McGivney" not in html


# --- AC4 wiring + ADR-0004 single-file -------------------------------------

def test_generate_run_handout_emits_named_file(tmp_path):
    """generate.run('handout') is wired and writes handout.html via the _today seam."""
    path = generate.run("handout", _root=tmp_path / "store", _out_dir=tmp_path / "out", _today=_TODAY)
    assert path.name == "handout.html"
    assert "Doctor Visit Handout" in path.read_text()


def test_single_file_no_external_asset_references(tmp_path):
    """The handout inlines everything — zero external asset references (ADR-0004)."""
    root = tmp_path / "store"
    _seed_findings(root)
    _seed_plans(root)
    html = _emit(root, tmp_path)
    assert render._external_references(html) == []


def test_escaping_across_interpolated_sinks(tmp_path):
    """A finding's caution + source + grade carrying markup are escaped, never raw."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("inj", caution="<script>alert('x')</script> & more",
                 source_specialist="<b>spoof</b>", band="HIGH", grade="<i>g</i>"),
        _ISO, root)
    section = _interactions(_emit(root, tmp_path))
    assert "<script>" not in section
    assert "&lt;script&gt;" in section
    assert "<b>spoof</b>" not in section
    assert "<i>g</i>" not in section              # the grade chip sink is escaped too
    assert "&lt;i&gt;g&lt;/i&gt;" in section


# --- AC5: store-surface adversarial battery --------------------------------

def test_adversarial_cross_stream_isolation(tmp_path):
    """The findings come ONLY from dvq::queue; no other stream cross-reads into it.

    A biomarker reading and a supplements plan sharing the collation date must
    never surface as a flagged finding (the S41 read_panel cross-stream class).
    The plan content still routes — to the regimen section, not the findings.
    """
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("only", caution="the only flagged finding", band="HIGH"), _ISO, root)
    loop_schema.record_biomarker("crp", "2026-06-20T00:00:00+00:00", 7.3, root)
    _seed_plans(root)
    html = _emit(root, tmp_path)
    section = _interactions(html)
    assert "the only flagged finding" in section
    # exactly one finding row (count the row class, not the `hd-findsrc` substring);
    # no biomarker or plan stream cross-read into the queue resolution.
    assert section.count("class='hd-find'") == 1
    assert "crp" not in section and "7.3" not in section
    assert "Creatine" not in section                  # the plan is the regimen, never a finding
    assert "Creatine — 5 g" in html                   # ...and it DID route, to the regimen section


def test_adversarial_same_finding_dedupe_latest_wins(tmp_path):
    """Re-collating one finding on a later date supersedes it — ONE row, latest disposition."""
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("f1", caution="warfarin interaction", outcome="block-stands", band="HIGH"),
        "2026-06-19", root)
    queue_schema.record_doctor_visit_queue_entry(
        _finding("f1", caution="warfarin interaction", outcome="cleared-with-override", band="HIGH"),
        "2026-06-20", root)
    section = _interactions(_emit(root, tmp_path))
    assert section.count("class='hd-find'") == 1                  # not two rows for one finding
    assert "on record — proceeding with consent" in section       # the LATEST disposition
    assert "unresolved — discuss" not in section                  # the superseded one is gone


def test_adversarial_idempotent_same_date_norecord(tmp_path):
    """The identical finding recorded twice on the SAME date is an idempotent no-op — ONE row."""
    root = tmp_path / "store"
    entry = _finding("dup", caution="warfarin interaction", outcome="block-stands", band="HIGH")
    queue_schema.record_doctor_visit_queue_entry(entry, _ISO, root)
    queue_schema.record_doctor_visit_queue_entry(entry, _ISO, root)   # identical, same date
    section = _interactions(_emit(root, tmp_path))
    assert section.count("class='hd-find'") == 1
    assert section.count("warfarin interaction") == 1


def test_adversarial_mutation_findings_required(tmp_path):
    """Mutation proof: the section's content is caused by the dvq read, not the frame.

    With the queue populated the caution renders; with it empty the SAME render
    yields the honest absence instead — so the assertion fails if the render ever
    stops reading the queue (the page frame alone cannot produce the caution).
    """
    root = tmp_path / "store"
    queue_schema.record_doctor_visit_queue_entry(
        _finding("m", caution="distinctive-mutation-caution", band="HIGH"), _ISO, root)
    populated = _interactions(_emit(root, tmp_path))
    empty = _interactions(_emit(tmp_path / "empty", tmp_path))
    assert "distinctive-mutation-caution" in populated
    assert "distinctive-mutation-caution" not in empty
    assert "No flagged interactions" in empty and "No flagged interactions" not in populated


# --- backward-compat: report + dashboard unchanged -------------------------

@pytest.mark.parametrize("artifact", ["dashboard", "report"])
def test_sibling_artifacts_still_render(tmp_path, artifact):
    """Adding the handout target leaves the dashboard + report render paths intact."""
    path = generate.run(artifact, _root=tmp_path / "store", _out_dir=tmp_path / "out", _today=_TODAY)
    assert path.name == f"{artifact}.html"
    assert render._external_references(path.read_text()) == []
