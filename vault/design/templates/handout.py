"""Handout template — the doctor-visit SBAR handout (the dvq::queue render surface).

Renders the medical-liaison's doctor-visit queue — the plan-generation pipeline's
adjudicated safety findings (additive-AE, cross-domain-conflict, and supplement-Rx
BPMH outcomes, each cleared-with-override or block-stands) — as the one-page SBAR
handout the operator brings to the MD visit (medical-liaison design §9.4). The
section structure is SBAR: Situation / Background (regimen + flagged interactions)
/ Assessment / Recommendation. It renders NO clinical verdict — the flagged-
interactions list surfaces dispositions + source attribution, and the
Recommendation is questions/requests only (never a prescription or START/STOP).

The render is a data-out PII boundary (ADR-0004-T1): it reads operator data ONLY
from the `store_read` argument. The flagged-interactions section resolves the
`dvq::queue` items IN `store_read` through the PURE `queue_schema.
resolve_doctor_visit_queue` (NOT `read_doctor_visit_queue`, which reads the store
root) — keeping the boundary, the same severity ordering (non-overridable auto-
block > block-stands > cleared, then band), and the §9.4 render precondition: the
optional liaison `grade`/`watchlist` annotations are TOLERATED absent (the data
layer guarantees the tier baseline; the render degrades to it).

The honesty rule (ADR-0009 D2) governs every slot: the model-gated SBAR sections
(Situation visit-priorities, Assessment observations, the Rx-medication BPMH
reconciliation) render em-dash awaiting copy, never an invented entry; the regimen
renders from the day's `plan::supplements`/`plan::peptides`, the Recommendation
from pending `panel::` draws + unanswered watch-out questions. The operator renders
as INITIALS only — never the full name. All markup + colors come from
`component_set` tokens (the shared `read_profile`/`long_date`/`tier_legend` and the
PALETTE-tinted pills for data state); single-file zero-script (ADR-0004), the
shared `@media print` contract extended with the page's own print rules. A template
is a module exposing `render(store_read) -> html_str`.
"""

import datetime
from pathlib import Path

from scripts.store import biomarker_meta, plan_schema, queue_schema
from scripts.store.loop_schema import derive_watchout_questions, panel_pending
from vault.design.templates import component_set as cs

# The header profile sources, same preference order as the face sheet: the
# ADR-0005 filled copy (gitignored) wins over the tracked scaffold; the header
# reads INITIALS only. Module constant so tests can point it at fixtures.
_PROFILE_PATHS = (
    Path("vault/scaffold/filled/operator-profile.md"),
    Path("vault/meta/operator-profile.md"),
)

# The doctor-visit-queue stream id (queue_schema owns the stream; the render
# resolves the item's readings out of store_read through the pure resolver, so it
# never reads the store root — the data-out PII boundary).
_DVQ_ITEM = "dvq::queue"

# The footer honesty line — verbatim, shared with the face sheet.
_HONESTY_LINE = "every value tagged · gaps stated, never inferred · local-first · print-safe"

# The non-prescribing disclaimer: this artifact states no diagnosis or prescription
# (medical-liaison renders no clinical verdict; §9.4 Recommendation is questions only).
_NO_VERDICT_LINE = "Questions & requests only — this sheet states no diagnosis or prescription."

# Axis -> the human-readable provenance phrase for a finding's source line.
_AXIS_LABEL = {
    "additive-ae": "additive-AE",
    "cross-domain-conflict": "cross-domain conflict",
    "rx-bpmh": "supplement–Rx (BPMH)",
}


def _handout_style():
    """Return the handout's own `<style>` block, built from `component_set` tokens.

    The base component CSS (`.pill`/`.tint-*`/`.chip-b`/`.awaiting`/`.caption`) is
    inherited from `cs.head`'s shared block; this adds only the page frame (~880px
    white page, the 2px training-blue header rule, the section accent bars, the
    finding rows, and the footer) and a print rule dropping the page chrome.
    """
    p, c, a = cs.PALETTE, cs.CHROME, cs.ACCENTS
    return f"""<style>
html, body {{ background: {p['paper']}; }}
.hd-page {{ max-width: 880px; margin: 24px auto; padding: 32px; background: {p['paper']}; border: 1px solid {c['card-border']}; font-family: Inter, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; color: {p['ink']}; }}
.hd-header {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; }}
.hd-title {{ font-size: 20px; font-weight: 700; }}
.hd-caption {{ color: {p['muted']}; font-size: 12px; }}
.hd-status {{ color: {p['muted']}; font-size: 12px; margin-top: 4px; }}
.hd-head-block {{ border-bottom: 2px solid {a['training']}; padding-bottom: 12px; }}
.hd-sec {{ margin-top: 14px; }}
.hd-shead {{ display: flex; align-items: center; gap: 8px; }}
.hd-bar {{ display: inline-block; width: 4px; height: 16px; border-radius: 2px; }}
.hd-stitle {{ font-size: 13px; font-weight: 700; }}
.hd-sub {{ color: {p['muted']}; font-size: 12px; margin-top: 4px; }}
.hd-row {{ display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; margin-top: 6px; font-size: 12px; }}
.hd-rowname {{ font-weight: 600; }}
.hd-find {{ display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; border: 1px solid {c['card-border']}; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-size: 12px; }}
.hd-findsrc {{ color: {p['muted']}; }}
.hd-foot {{ display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-top: 14px; padding-top: 10px; border-top: 1px solid {c['card-border']}; font-size: 11px; color: {p['muted']}; }}
@media print {{
  .hd-page {{ max-width: 100%; margin: 0; border: none; padding: 0; }}
}}
</style>"""


def _section(title, bar_hex, body_html):
    """Return one SBAR section: a 4x16 accent bar + 13px/700 title + body.

    Args:
        title (str): The section heading text (escaped).
        bar_hex (str): The accent-bar token hex (chrome, never data state).
        body_html (str): The assembled section body, included verbatim.

    Returns:
        (str) The assembled `.hd-sec` markup.
    """
    head = (
        f"<div class='hd-shead'><span class='hd-bar' style='background:{bar_hex}'></span>"
        f"<span class='hd-stitle'>{cs._escape(str(title))}</span></div>"
    )
    return f"<div class='hd-sec'>{head}{body_html}</div>"


def _header_block(today):
    """Render the header: title, prepared date, and the initials status line.

    The status line carries operator INITIALS only; age band + issue status render
    from the profile when filled, em-dash otherwise (`cs.read_profile`).
    """
    profile = cs.read_profile(_PROFILE_PATHS)
    prepared = cs.long_date(today)
    status_line = (
        f"Patient {profile['initials'] or '—'}"
        f" · age band {profile['age_band'] or '—'}"
        f" · issue status {profile['issue_status'] or '—'}"
    )
    return (
        "<div class='hd-head-block'>"
        "<div class='hd-header'>"
        "<div class='hd-title'>A+ Maxing — Doctor Visit Handout</div>"
        f"<div class='hd-caption'>Prepared {cs._escape(prepared)}</div>"
        "</div>"
        f"<div class='hd-status'>{cs._escape(status_line)}</div>"
        "</div>"
    )


def _situation_section():
    """Render section 1 — Situation (awaiting: visit priorities are operator-authored)."""
    return _section(
        "Situation — top of mind for this visit",
        cs.ACCENTS["training"],
        cs.awaiting(
            "Visit priorities are operator-authored — set the top-of-mind list at visit prep."
        ),
    )


def _regimen_section(plan_readings, today):
    """Render section 2a — current regimen, from the day's supplement/peptide plans.

    `name — dose` per supplement; `compound · dose · route` for the peptide, with
    an experimental tag adding the disclosure note. The Rx-medication rows are an
    honest awaiting sub-line: no medication-reconciliation (BPMH) intake stream
    exists, so a fabricated Rx row would be a claim.
    """
    on_date = today.isoformat()
    rows = []
    supplements = plan_schema.resolve_plan(plan_readings.get("supplements", []), on_date)
    if supplements["state"] is None:
        for entry in supplements["plan"]["items"]:
            rows.append(
                "<div class='hd-row'><span class='hd-rowname'>"
                f"{cs._escape(entry['name'])} — {cs._escape(entry['dose'])}</span></div>"
            )
    peptides = plan_schema.resolve_plan(plan_readings.get("peptides", []), on_date)
    if peptides["state"] is None:
        plan = peptides["plan"]
        detail = f"{plan['compound']} · {plan['dose']} · {plan['route']}"
        note = ""
        if "experimental" in plan.get("tags", ()):
            note = "<span class='caption'>experimental — disclosure attached</span>"
        rows.append(
            "<div class='hd-row'><span class='hd-rowname'>"
            f"{cs._escape(detail)}</span>{note}</div>"
        )
    body = "".join(rows) or cs.awaiting(
        "No supplement or peptide plan recorded for today."
    )
    body += (
        "<div class='hd-sub'>Prescription medications reconcile here when the "
        "medication-reconciliation (BPMH) intake lands.</div>"
    )
    return _section(
        "Background — current regimen (self-reported)", cs.ACCENTS["supplements"], body
    )


def _disposition(entry):
    """Return (chip label, PALETTE pill tint) for a finding's MD disposition.

    The disposition is the finding's CURRENT state for the doctor; the colour is a
    PALETTE data state (via the pill tint), NEVER accent chrome. The three tiers
    mirror `queue_schema._severity_rank` exactly (one contract, not a second
    judgment): a non-overridable auto-block and an unresolved block-stands are both
    open concerns (concern); a cleared-with-override is on record, the operator
    proceeding with informed consent (watch).
    """
    if bool(entry.get("non_overridable")):
        return "auto-block — do not proceed", "concern"
    if entry.get("outcome") == "block-stands":
        return "unresolved — discuss", "concern"
    return "on record — proceeding with consent", "watch"


def _finding_source(entry):
    """Render a finding's muted source/provenance line: who says it + the axis + band.

    Names which source raised the finding (`source_specialist`) and how (the axis),
    plus the real composite band when an adjudicator set one (`None` only when none
    ran — omitted, never a fabricated band). The optional liaison GRADE rides a
    bordered chip when present (§9.4 render precondition: tolerate it absent).
    """
    bits = []
    if entry.get("source_specialist"):
        bits.append(f"via {entry['source_specialist']}")
    if entry.get("axis"):
        bits.append(_AXIS_LABEL.get(entry["axis"], entry["axis"]))
    if entry.get("composite_band"):
        bits.append(entry["composite_band"])
    src = (
        f"<span class='hd-findsrc'>{cs._escape(' · '.join(bits))}</span>" if bits else ""
    )
    grade = entry.get("grade")
    grade_chip = cs.chip_b(f"GRADE {grade}") if grade else ""
    return f"{src}{grade_chip}"


def _finding_row(entry):
    """Render one flagged-interaction row: disposition chip + caution + source line.

    No clinical verdict — the chip states the finding's disposition (a fact about
    the adjudication), the caution is the finding's verbatim source-attributed
    text, and the source line names provenance. The data layer already severity-
    ranked the findings, so the rows render in MD-priority order as received.
    """
    label, tint = _disposition(entry)
    return (
        "<div class='hd-find'>"
        f"{cs.pill(label, tint)}"
        f"<span>{cs._escape(str(entry.get('caution', '')))}</span>"
        f"{_finding_source(entry)}"
        "</div>"
    )


def _interactions_section(findings):
    """Render section 2b — flagged interactions, severity-ranked (the dvq::queue core).

    Each adjudicated finding renders a row; an empty queue renders an honest
    absence (no flagged findings ON FILE — never the unstated claim "you are
    safe"), with the note that findings appear here when the pipeline adjudicates
    a safety concern.

    Args:
        findings (list): The severity-ranked queue entries from
            `queue_schema.resolve_doctor_visit_queue` (possibly empty).
    """
    if not findings:
        body = (
            "<div class='hd-row'>No flagged interactions or contraindications on file.</div>"
            "<div class='hd-sub'>Findings appear here when the plan pipeline "
            "adjudicates a safety concern.</div>"
        )
    else:
        body = "".join(_finding_row(entry) for entry in findings)
    return _section(
        "Background — flagged interactions & contraindications",
        cs.SECTION_ACCENTS["biomarkers"],
        body,
    )


def _assessment_section():
    """Render section 3 — Assessment, the not-a-diagnosis label + awaiting state.

    Patient-observed patterns are operator-authored; until that intake exists the
    section renders the label and an honest awaiting line (no invented pattern).
    """
    body = (
        f"{cs.pill('patient observation — not a diagnosis', 'neutral')}"
        f"{cs.awaiting('Patient-observed patterns are operator-authored — none on file.')}"
    )
    return _section("Assessment — patient-observed patterns", cs.ACCENTS["sleep"], body)


def _recommendation_section(panels, plan_readings, answered_watchouts, today):
    """Render section 4 — Recommendation: questions & requests only (no verdict).

    `Requests — order today:` renders one bordered chip per pending `panel::` draw
    (real provenance-resolved state, `panel_pending`); `Questions:` derives from
    the active peptide protocol's watch-out questions with no stored answer yet.
    Either line renders a muted none-state when empty. No prescription, no
    START/STOP — the explicit no-verdict disclaimer leads the section.
    """
    pending = [
        item for item, readings in sorted(panels.items()) if panel_pending(readings)
    ]
    chips = (
        "".join(cs.chip_b(biomarker_meta.display_name(item)) for item in pending)
        or "<span class='caption'>none pending</span>"
    )
    questions = []
    peptides = plan_schema.resolve_plan(
        plan_readings.get("peptides", []), today.isoformat()
    )
    if peptides["state"] is None:
        derived = derive_watchout_questions([peptides["plan"]["compound"]])
        questions = sorted(q for q in derived if q not in answered_watchouts)
    if questions:
        question_line = cs._escape(
            " · ".join(biomarker_meta.display_name(q) for q in questions)
        )
    else:
        question_line = "<span class='caption'>none queued</span>"
    body = (
        f"<div class='hd-sub'>{cs._escape(_NO_VERDICT_LINE)}</div>"
        f"<div class='hd-row'><span class='hd-rowname'>Requests — order today:</span> {chips}</div>"
        f"<div class='hd-row'><span class='hd-rowname'>Questions:</span> {question_line}</div>"
    )
    return _section("Recommendation — questions & requests", cs.ACCENTS["nutrition"], body)


def _footer(today):
    """Render the footer: the colored source-tier legend + the honesty/no-verdict line."""
    return (
        "<div class='hd-foot'>"
        f"<span>{cs.tier_legend()}</span>"
        f"<span>{cs._escape(_HONESTY_LINE)} · renders no clinical verdict · "
        f"not a medical record · generated {cs._escape(cs.long_date(today))}</span>"
        "</div>"
    )


def render(store_read, _today=None):
    """Assemble the doctor-visit SBAR handout HTML from the shared component set.

    Reads operator data ONLY from `store_read`: the flagged-interactions section
    resolves the `dvq::queue` readings in `store_read` through the pure
    `queue_schema.resolve_doctor_visit_queue` (severity-ranked, grade/watchlist-
    tolerant); the regimen reads the day's `plan::supplements`/`plan::peptides`;
    the recommendation reads pending `panel::` draws + unanswered `watch-out::`
    questions. Streams this focused artifact does not surface are ignored (it
    renders the five SBAR sections, not the whole store).

    Args:
        store_read (list): The store read model passed through by render.emit.
        _today (datetime.date, optional): Test-only date seam (prepared date,
            plan resolution, footer); defaults to the current date.

    Returns:
        (str) The assembled handout HTML (single document, inline styling, zero
        scripts).
    """
    today = _today if _today is not None else datetime.date.today()
    by_item = {}
    for reading in store_read:
        by_item.setdefault(reading["item"], []).append(reading)
    plan_readings, panels = {}, {}
    answered_watchouts = set()
    for item, readings in by_item.items():
        if item.startswith("plan::"):
            domain = item[len("plan::"):]
            if domain in ("supplements", "peptides"):
                plan_readings[domain] = readings
        elif item.startswith("panel::"):
            panels[item] = readings
        elif item.startswith("watch-out::"):
            answered_watchouts.add(item[len("watch-out::"):])
    findings = queue_schema.resolve_doctor_visit_queue(by_item.get(_DVQ_ITEM, []))
    body = (
        "<div class='hd-page'>"
        f"{_header_block(today)}"
        f"{_situation_section()}"
        f"{_regimen_section(plan_readings, today)}"
        f"{_interactions_section(findings)}"
        f"{_assessment_section()}"
        f"{_recommendation_section(panels, plan_readings, answered_watchouts, today)}"
        f"{_footer(today)}"
        "</div>"
    )
    return (
        "<!doctype html><html lang='en'>"
        f"{cs.head('A+ Maxing — Doctor Visit Handout', _handout_style())}"
        f"<body>{body}</body></html>"
    )
