"""Tests for the Physician Face Sheet template (bead nsxy).

Pins the page-one section anatomy through the PRODUCTION path
(`generate.run("report")` over stores seeded via the published writers), the
honesty gates (digit-free awaiting copy, em-dash adherence, no fabricated
percentages, initials-only header, real in-range counts, watch chips only for
out-of-range registered markers), the page-2 abnormal-first detail layer, the
populated triage-row anatomy (helper-level — the production path renders the
first-visit copy until LM-01 lands), escaping across every new interpolated
sink, and the single-file inert contract. Colors are asserted as
`component_set` token references, never re-derived literals.
"""

import datetime
import html as html_lib
import re

import pytest

from scripts.generate import generate
from scripts.store import loop_schema, plan_schema
from vault.design.templates import component_set as cs
from vault.design.templates import report

_TODAY = datetime.date(2026, 6, 12)
_ISO = "2026-06-12"

# An unfilled operator-profile scaffold (the `<...>` prompt form the repo
# scaffold ships) and a filled counterpart — the header's two states.
_SCAFFOLD_PROFILE = """# Operator Profile — Walter

## Demographics
- **Sex:** <M | F>
- **Age:** <years>  (DOB if you want auto-update: <YYYY-MM-DD>)

## January 2026 health issue
- **Current status:** <resolved | improving | stable | ongoing>
"""

_FILLED_PROFILE = """# Operator Profile — Walter McGivney

## Demographics
- **Age:** 44

## January 2026 health issue
- **Current status:** improving
"""


def _seed_biomarkers(root):
    """Seed four markers: crp concern, rhr + vitamin-d good, hrv neutral."""
    loop_schema.record_biomarker("crp", "2026-05-12T00:00:00+00:00", 6.1, root)
    loop_schema.record_biomarker("crp", "2026-06-11T00:00:00+00:00", 7.3, root)
    loop_schema.record_biomarker("rhr", "2026-06-11T00:00:00+00:00", 52, root)
    loop_schema.record_biomarker("vitamin-d", "2026-06-11T00:00:00+00:00", 45, root)
    loop_schema.record_biomarker("hrv", "2026-06-11T00:00:00+00:00", 71, root)


def _seed_plans(root, on_date=_ISO):
    """Seed today's supplements + experimental peptides plans."""
    plan_schema.record_plan(
        "supplements",
        {"items": [
            {"name": "Creatine", "dose": "5 g"},
            {"name": "Vitamin D3", "dose": "5000 IU"},
        ]},
        on_date, "supplement-specialist", root,
    )
    plan_schema.record_plan(
        "peptides",
        {"compound": "bpc-157", "dose": "250 mcg", "route": "subq",
         "tags": ["experimental"]},
        on_date, "peptide-specialist", root,
    )


def _seed_asks(root):
    """Seed one pending panel, one resolved panel, one answered watch-out."""
    loop_schema.record_pending_panel("ferritin", "2026-06-10T00:00:00+00:00", root)
    loop_schema.record_pending_panel("lipid-panel", "2026-06-01T00:00:00+00:00", root)
    loop_schema.record_panel_result(
        "lipid-panel", "complete", "2026-06-05T00:00:00+00:00", root
    )
    loop_schema.record_watchout_answer(
        "injection_site_reaction", "none observed", "2026-06-10T00:00:00+00:00", root
    )


def _emit(root, tmp_path, today=_TODAY):
    """Render the report through the production path and return its HTML."""
    return generate.run(
        "report", _root=root, _out_dir=tmp_path / "out", _today=today
    ).read_text()


def _between(html, start, end):
    """Slice the markup between two unique anchors (section scoping)."""
    i = html.index(start)
    return html[i:html.index(end, i)]


def _text(markup):
    """Tag-strip and entity-decode markup to its rendered text."""
    return html_lib.unescape(re.sub(r"<[^>]*>", "", markup))


def _body(html):
    """Return the document body with all <style> blocks removed."""
    return re.sub(r"<style>.*?</style>", "", html, flags=re.S)


# --------------------------------------------------------------------------- #
# Section 1 — header + status line
# --------------------------------------------------------------------------- #


def test_header_prepared_date_and_blue_rule(tmp_path):
    """The header renders the seam date and the 2px training-blue rule."""
    html = _emit(tmp_path / "store", tmp_path)
    assert "A+ Maxing — Physician Face Sheet" in html
    assert "Prepared June 12, 2026" in html
    assert f"border-bottom: 2px solid {cs.ACCENTS['training']}" in html


def test_header_unfilled_profile_renders_em_dash_slots(tmp_path, monkeypatch):
    """An unfilled scaffold renders em-dash awaiting slots, never a guess."""
    profile = tmp_path / "profile.md"
    profile.write_text(_SCAFFOLD_PROFILE)
    monkeypatch.setattr(report, "_PROFILE_PATH", profile)
    html = _emit(tmp_path / "store", tmp_path)
    assert "Patient W · age band — · issue status — · last review — · next visit —" in html


def test_header_filled_profile_initials_and_band_only(tmp_path, monkeypatch):
    """A filled profile renders initials + decade band — NEVER the name or age.

    The PII gate: the operator's full name must not reach a render in any
    form, and the exact age renders only as its decade band.
    """
    profile = tmp_path / "profile.md"
    profile.write_text(_FILLED_PROFILE)
    monkeypatch.setattr(report, "_PROFILE_PATH", profile)
    html = _emit(tmp_path / "store", tmp_path)
    assert "Patient WM · age band 40s · issue status improving" in html
    assert "Walter" not in html, "the operator name must never render"
    assert "McGivney" not in html, "the operator name must never render"
    assert not re.search(r"\b44\b", _body(html)), "the exact age must not render"


def test_header_missing_profile_renders_awaiting(tmp_path, monkeypatch):
    """A missing profile file renders the awaiting slots, not a crash."""
    monkeypatch.setattr(report, "_PROFILE_PATH", tmp_path / "absent.md")
    html = _emit(tmp_path / "store", tmp_path)
    assert "Patient — · age band — · issue status —" in html


# --------------------------------------------------------------------------- #
# Section 2 — since your last review (triage)
# --------------------------------------------------------------------------- #


def test_triage_renders_first_visit_copy_on_training_tint(tmp_path):
    """The production path renders the first-visit copy (the LM-01 awaiting
    state) inside the training-tint card with the training-text title."""
    html = _emit(tmp_path / "store", tmp_path)
    card = _between(html, "fs-card fs-triage", "Current regimen")
    assert "No prior review — full baseline below" in card
    assert f".fs-triage {{ background: {cs.CHROME['training-tint']}; }}" in html
    assert f".fs-triage .fs-stitle {{ color: {cs.CHROME['training-text']}; }}" in html
    copy = _text(_between(card, "No prior review", "</div>"))
    assert not re.search(r"\d", copy), "the awaiting copy must be digit-free"


def test_triage_row_populated_anatomy():
    """The populated delta-row helper: improving = good with ▲/▼, attention =
    the measured watch pair with ●, neutral = ink; unknown kind KeyErrors.

    Pinned at helper level: the production path renders the first-visit copy
    until LM-01 visit anchoring lands.
    """
    up = report._triage_row("CRP falling toward range", "improving", rising=True)
    down = report._triage_row("LDL down", "improving", rising=False)
    assert "▲" in up and "▼" in down
    assert f"color:{cs.PALETTE['good']}" in up

    attention = report._triage_row("bpc-157 started — experimental", "attention")
    assert "●" in attention
    assert "fs-attn" in attention, (
        "attention rows ride the measured watch pair (watch-text on the "
        "card's training-tint computes < 4.5)"
    )

    neutral = report._triage_row("No change in sleep", "neutral")
    assert "fs-attn" not in neutral and "color:" not in neutral

    with pytest.raises(KeyError):
        report._triage_row("x", "bogus-kind")


# --------------------------------------------------------------------------- #
# Section 3 — current regimen with adherence
# --------------------------------------------------------------------------- #


def test_regimen_rows_from_todays_plans(tmp_path):
    """Today's plan items render as regimen rows with the plan-date `since`
    and an em-dash adherence slot per row — never a fabricated percent."""
    root = tmp_path / "store"
    _seed_plans(root)
    html = _emit(root, tmp_path)
    section = _between(html, "Current regimen — with adherence", "Biomarkers —")
    assert "Creatine — 5 g" in section
    assert "Vitamin D3 — 5000 IU" in section
    assert "bpc-157 · 250 mcg · subq" in section
    assert section.count("since Jun 12") == 3
    assert section.count("adherence —") == 3
    assert "%" not in _body(html), "no fabricated adherence percentage anywhere"


def test_regimen_experimental_row_watch_text_disclosure(tmp_path):
    """An `experimental` tag renders the row detail in watch-text plus the
    disclosure note; an untagged plan renders neither."""
    root = tmp_path / "store"
    _seed_plans(root)
    html = _emit(root, tmp_path)
    section = _between(html, "Current regimen — with adherence", "Biomarkers —")
    assert "<span class='fs-rowname fs-exp'>bpc-157 · 250 mcg · subq</span>" in section
    assert "experimental — disclosure attached" in section
    assert f".fs-exp {{ color: {cs.CHROME['watch-text']}; }}" in html

    plain_root = tmp_path / "plain"
    plan_schema.record_plan(
        "peptides",
        {"compound": "bpc-157", "dose": "250 mcg", "route": "subq"},
        _ISO, "peptide-specialist", plain_root,
    )
    plain = _between(
        _emit(plain_root, tmp_path / "plain-out"),
        "Current regimen — with adherence", "Biomarkers —",
    )
    assert "fs-exp" not in plain
    assert "disclosure attached" not in plain


def test_regimen_awaiting_when_no_plan_today(tmp_path):
    """A plan dated another day renders the digit-free awaiting line, no rows."""
    root = tmp_path / "store"
    _seed_plans(root, on_date="2026-06-10")
    html = _emit(root, tmp_path)
    section = _between(html, "Current regimen — with adherence", "Biomarkers —")
    assert "fs-row'" not in section
    assert "No supplement or peptide plan recorded for today" in section
    awaiting = re.search(r"<div class='awaiting'>(.*?)</div>", section, re.S).group(1)
    assert not re.search(r"\d", _text(awaiting))


# --------------------------------------------------------------------------- #
# Section 4 — biomarkers: abnormal rows + the in-range strip
# --------------------------------------------------------------------------- #


def test_abnormal_row_anatomy_real_data(tmp_path):
    """The out-of-range row renders name in concern, the self-reported glyph,
    the real value/ref/delta/window/drawn detail, and the watch chip."""
    root = tmp_path / "store"
    _seed_biomarkers(root)
    html = _emit(root, tmp_path)
    row = _between(html, "<div class='fs-abrow'>", "</div>")
    assert "<span class='fs-marker'>CRP</span>" in row
    assert f".fs-marker {{ font-size: 12px; font-weight: 700; color: {cs.PALETTE['concern']}; }}" in html
    assert f"<span style='color:{report._SELF_REPORTED_BASE}'>○</span>" in row
    assert "7.3 mg/L · ref 0 – 3 · +1.2/30d · drawn Jun 11" in row
    assert "<span class='pill tint-watch'>watch</span>" in row
    assert f".fs-abrow {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; background: {cs.CHROME['concern-tint']};" in html


def test_watch_chip_only_for_out_of_range_markers(tmp_path):
    """Exactly one watch chip per out-of-range registered marker — in-range
    and unregistered (neutral) markers render none."""
    root = tmp_path / "store"
    _seed_biomarkers(root)
    html = _emit(root, tmp_path)
    assert html.count("pill tint-watch") == 1, (
        "one chip for the one concern marker; good/neutral markers get none"
    )

    clean_root = tmp_path / "clean"
    loop_schema.record_biomarker("rhr", "2026-06-11T00:00:00+00:00", 52, clean_root)
    clean = _emit(clean_root, tmp_path / "clean-out")
    assert "pill tint-watch" not in clean
    assert "fs-abrow" not in _body(clean)


def test_in_range_strip_count_is_real(tmp_path):
    """The collapse strip carries the REAL good count: neutral (no registered
    range) markers are never counted in range."""
    root = tmp_path / "store"
    _seed_biomarkers(root)  # rhr + vitamin-d good, crp concern, hrv neutral
    html = _emit(root, tmp_path)
    assert "✓ 2 markers in range — full table with sparklines on page 2" in html

    one_root = tmp_path / "one"
    loop_schema.record_biomarker("rhr", "2026-06-11T00:00:00+00:00", 52, one_root)
    one = _emit(one_root, tmp_path / "one-out")
    assert "✓ 1 marker in range — full table with sparklines on page 2" in one


def test_no_biomarkers_renders_awaiting_line(tmp_path):
    """An empty biomarker layer renders one digit-free awaiting line — no
    abnormal rows, no strip, no invented zero."""
    root = tmp_path / "store"
    _seed_plans(root)
    html = _emit(root, tmp_path)
    section = _between(html, "Biomarkers — out of range or trending", "Goals &amp; trajectory")
    assert "No biomarker readings on file yet." in section
    assert "fs-abrow" not in section and "fs-strip" not in section
    awaiting = re.search(r"<div class='awaiting'>(.*?)</div>", section, re.S).group(1)
    assert not re.search(r"\d", _text(awaiting))


# --------------------------------------------------------------------------- #
# Sections 5 + 6 — goals and signal aggregates (gated awaiting states)
# --------------------------------------------------------------------------- #


def test_goals_awaiting_digit_free(tmp_path):
    """No goal model -> one digit-free awaiting line under the goals bar."""
    html = _emit(tmp_path / "store", tmp_path)
    assert f"background:{cs.SECTION_ACCENTS['goals']}" in html
    section = _between(html, "Goals &amp; trajectory", "Patient-generated signals")
    awaiting = re.search(r"<div class='awaiting'>(.*?)</div>", section, re.S).group(1)
    assert "No goals on file" in awaiting
    assert not re.search(r"\d", _text(awaiting))


def test_signals_structure_with_em_dash_values(tmp_path):
    """The LM-02-gated stat boxes render structure (wearable tier edge + glyph
    + label) with em-dash values, no direction arrows, digit-free caption."""
    html = _emit(tmp_path / "store", tmp_path)
    section = _between(html, "Patient-generated signals", "Asks &amp; agenda")
    assert section.count("<div class='fs-sigval'>—</div>") == 4
    assert section.count("consumer wearable") == 4
    assert "▲" not in section and "▼" not in section, "no invented direction"
    assert f"border-top: 3px solid {cs.ACCENTS['supplements']}" in html
    caption = _between(section, "Thirty-day aggregates", "</div>")
    assert not re.search(r"\d", _text(caption))


# --------------------------------------------------------------------------- #
# Section 7 — asks & agenda
# --------------------------------------------------------------------------- #


def test_asks_pending_chips_provenance_resolved(tmp_path):
    """`Order today:` chips render ONLY provenance-pending panels: the
    resolved panel renders no chip even though its pending marker persists."""
    root = tmp_path / "store"
    _seed_asks(root)
    html = _emit(root, tmp_path)
    section = _between(html, "Asks &amp; agenda", "fs-foot")
    order = _between(section, "Order today:", "Patient questions:")
    assert "<span class='chip-b'>Ferritin</span>" in order
    assert "Lipid Panel" not in order, "a landed result is not a pending draw"


def test_asks_questions_derived_minus_answered(tmp_path):
    """`Patient questions:` carries the active protocol's watch-out questions
    that have no stored answer; answered questions drop off the line."""
    root = tmp_path / "store"
    _seed_plans(root)
    _seed_asks(root)
    html = _emit(root, tmp_path)
    questions = _between(html, "Patient questions:", "</div>")
    assert "Appetite Change" in questions
    assert "Injection Site Reaction" not in questions, (
        "an answered watch-out is no longer an open question"
    )


def test_asks_none_states_when_empty(tmp_path):
    """No pending draws and no active protocol render muted none-states."""
    html = _emit(tmp_path / "store", tmp_path)
    section = _between(html, "Asks &amp; agenda", "fs-foot")
    assert "none pending" in section
    assert "none queued" in section
    assert f".fs-asks {{ background: {cs.CHROME['nutrition-tint']}; }}" in html


# --------------------------------------------------------------------------- #
# Footer — source-tier legend + honesty line
# --------------------------------------------------------------------------- #


def test_footer_tier_legend_and_honesty_line(tmp_path):
    """The legend renders glyphs in the base triple, tier WORDS in the *-text
    triple, the honesty line verbatim, and the generation date."""
    html = _emit(tmp_path / "store", tmp_path)
    foot = _between(html, "<div class='fs-foot'>", "fs-page2")
    for glyph, base, text, word in (
        ("◆", cs.ACCENTS["training"], cs.CHROME["training-text"], "lab-grade"),
        ("●", cs.ACCENTS["supplements"], cs.CHROME["supplements-text"], "consumer wearable"),
        ("○", report._SELF_REPORTED_BASE, cs.CHROME["watch-text"], "self-reported"),
    ):
        assert f"<span style='color:{base}'>{glyph}</span>" in foot
        assert f"<span style='color:{text}'>{word}</span>" in foot
    assert (
        "every value tagged · gaps stated, never inferred · local-first · print-safe"
        in foot
    )
    assert "generated June 12, 2026" in foot


# --------------------------------------------------------------------------- #
# Page 2 — abnormal-first detail layer
# --------------------------------------------------------------------------- #


def test_page2_abnormal_first_ordering(tmp_path):
    """Page-2 sections order concern items first, then the rest by item."""
    root = tmp_path / "store"
    _seed_biomarkers(root)
    _seed_plans(root)
    html = _emit(root, tmp_path)
    page2 = html[html.index("fs-page2"):]
    order = re.findall(r"<h2>([^<]*)</h2>", page2)
    decoded = [html_lib.unescape(h) for h in order]
    assert decoded[0] == "biomarker::crp", "the concern item leads page 2"
    assert set(decoded[1:]) == {
        "biomarker::hrv", "biomarker::rhr", "biomarker::vitamin-d",
        "plan::peptides", "plan::supplements",
    }
    assert decoded[1:] == sorted(decoded[1:]), "non-abnormal items stay item-sorted"


def test_page2_heading_caption_glyph_and_ref_range(tmp_path):
    """A manual-sourced registered item's heading caption carries the
    self-reported tier (glyph in base chrome, word in watch-text) + range."""
    root = tmp_path / "store"
    _seed_biomarkers(root)
    html = _emit(root, tmp_path)
    section = _between(html, "<h2>biomarker::crp</h2>", "</section>")
    assert f"<span style='color:{report._SELF_REPORTED_BASE}'>○</span>" in section
    assert f"<span style='color:{cs.CHROME['watch-text']}'>self-reported</span>" in section
    assert "ref 0 – 3 mg/L" in section


def test_page2_unknown_source_states_no_tier(tmp_path):
    """An unmapped reading source renders NO tier claim — gaps stated, never
    inferred. Seeded via the raw store reading shape (legacy direct append)."""
    from scripts.store import store

    root = tmp_path / "store"
    store.append(
        "biomarker::crp",
        {"item": "biomarker::crp", "timepoint": "2026-06-11T00:00:00+00:00",
         "source": "whoop", "value": 7.3},
        root=root,
    )
    html = _emit(root, tmp_path)
    section = _between(html, "<h2>biomarker::crp</h2>", "</section>")
    assert "self-reported" not in section
    assert "○" not in section.split("<table>")[0]


def test_page2_string_stream_routes_table_only(tmp_path):
    """A stream with no numeric reading (watch-out answers) renders heading +
    table ONLY — a string must never reach the sparkline/KPI path."""
    root = tmp_path / "store"
    _seed_asks(root)
    html = _emit(root, tmp_path)
    section = _between(html, "<h2>watch-out::injection_site_reaction</h2>", "</section>")
    assert "<table>" in section
    assert "<svg" not in section
    assert "class='kpi'" not in section
    assert "none observed" in section


# --------------------------------------------------------------------------- #
# Escaping — adversarial content through every new interpolated sink
# --------------------------------------------------------------------------- #


def test_adversarial_content_escapes_through_new_sections(tmp_path, monkeypatch):
    """HTML-special content through the regimen rows, panel chips, watch-out
    tables, and the profile status line renders escaped: entities present,
    no raw tag anywhere."""
    evil = 'a&w "<b>x'
    root = tmp_path / "store"
    plan_schema.record_plan(
        "supplements",
        {"items": [{"name": evil, "dose": f'5 "g" {evil}'}]},
        _ISO, "supplement-specialist", root,
    )
    plan_schema.record_plan(
        "peptides",
        {"compound": evil, "dose": evil, "route": evil, "tags": ["experimental"]},
        _ISO, "peptide-specialist", root,
    )
    loop_schema.record_pending_panel(evil, "2026-06-10T00:00:00+00:00", root)
    loop_schema.record_watchout_answer("evil_q", f"ans {evil}", "2026-06-10T00:00:00+00:00", root)
    profile = tmp_path / "profile.md"
    profile.write_text(
        "# Operator Profile — <Evil> Walter\n"
        "- **Age:** 44\n"
        "- **Current status:** improving <b>now\n"
    )
    monkeypatch.setattr(report, "_PROFILE_PATH", profile)

    html = _emit(root, tmp_path)
    assert "&amp;" in html, "the ampersand must render entity-escaped"
    assert "&lt;b&gt;" in html or "&lt;B&gt;" in html
    assert "<b>" not in html and "<B>" not in html, "raw markup reached the sheet"
    assert "&lt;Evil&gt;" not in html and "<Evil>" not in html, (
        "the profile name renders as initials only — never the raw title text"
    )
    assert "improving &lt;b&gt;now" in html, "the status value renders escaped"


# --------------------------------------------------------------------------- #
# Single-file inert + print contract
# --------------------------------------------------------------------------- #


def test_facesheet_inert_and_print_native(tmp_path):
    """Zero scripts, zero hrefs/srcs, zero form controls; the shared @media
    print block is inherited and the face sheet adds its own page rules."""
    root = tmp_path / "store"
    _seed_biomarkers(root)
    _seed_plans(root)
    html = _emit(root, tmp_path)
    assert "<script" not in html
    assert "href=" not in html and "src=" not in html
    assert "<input" not in html and "<a " not in html
    assert "@media print" in html
    assert ".fs-page2 { page-break-before: always; }" in html
    assert ".fs-page { max-width: 100%; margin: 0; border: none; padding: 0; }" in html
