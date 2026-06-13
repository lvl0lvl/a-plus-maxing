"""Report template — the Physician Face Sheet (bead nsxy).

Renders the operator-approved face sheet per
`vault/design/physician-facesheet-v1-spec.md`: the v2 body governs section
structure, typography, and slot shapes; the signed v3 amendment block governs
every color binding. Page one is the 90-second scan layer — header + status
line, the since-your-last-review triage card, current regimen with adherence,
abnormal-first biomarkers, goals, 30-day signal aggregates, asks & agenda, and
the source-tier footer. Page two is the detail layer: the per-item readings
tables re-ordered abnormal-first, each heading carrying its source glyph and
registered ref range. `plan::`/`plan-track::` items keep their verbatim-table
routing — no KPI, no sparkline; a dict value must never reach numeric viz
(ADR-0010 D5) — and items with no numeric reading route table-only for the
same reason. The naive projection NEVER renders here (S52 operator decision).

The honesty rule (ADR-0009 D2) governs every slot: model-gated sections
(deltas/LM-01, adherence aggregates, signals/LM-02, goals) render em-dash or
digit-free awaiting copy, never an invented number; the header's age band and
issue status read the ADR-0005 filled-scaffold copy
(`vault/scaffold/filled/operator-profile.md`) when present, else the tracked
scaffold (`vault/meta/operator-profile.md`), only when those fields are
filled, and the operator renders as INITIALS only — never the full name.

All markup and colors come from `component_set` tokens (PALETTE, CHROME,
ACCENTS, SECTION_ACCENTS) with ONE exception sanctioned by the spec's v3
block: the self-reported tier's base amber `#B7791F` ships as non-text tier
chrome (glyph fills, stat-box edges) and is deliberately NOT a system token —
the v3 registration list is closed at four. Single-file zero-script
(ADR-0004): inert everything, the shared `@media print` contract inherited
and extended with the face sheet's own page rules. A template is a callable
`template(store_read) -> html_str`.
"""

import datetime
import re
from pathlib import Path

from scripts.store import biomarker_meta, plan_schema
from scripts.store.loop_schema import _TAG_PANEL, derive_watchout_questions
from vault.design.templates import component_set as cs

# Shared date/number formatting — reused from the dashboard template (the one
# other consumer) rather than re-derived: locale-independent month names, the
# `.10g` number form, and the ISO-timepoint date parse.
from vault.design.templates.dashboard import (
    _MONTH_NAMES,
    _format_number,
    _reading_date,
    _short_date,
)

# The operator-profile sources the header status line reads (age band +
# issue status when filled; initials from the title), in preference order:
# the ADR-0005-compliant filled copy (`vault/scaffold/filled/` — gitignored,
# the pinned filled-scaffold-value path) when it exists, else the tracked
# scaffold (unfilled prompts -> em-dash awaiting slots). Module constant so
# tests can point it at fixtures.
_PROFILE_PATHS = (
    Path("vault/scaffold/filled/operator-profile.md"),
    Path("vault/meta/operator-profile.md"),
)

# The self-reported tier's base amber — the v3 spec's ONE unregistered hex:
# non-text tier chrome only (glyph fills, stat-box top edges), never text
# (tier TEXT renders the registered `*-text` shades).
_SELF_REPORTED_BASE = "#B7791F"

# Source tier -> (glyph, non-text base chrome, AA text shade). Glyph SHAPES
# are distinct so monochrome print preserves the tiers (facesheet spec).
_TIER_CHROME = {
    "lab-grade": ("◆", cs.ACCENTS["training"], cs.CHROME["training-text"]),
    "consumer wearable": ("●", cs.ACCENTS["supplements"], cs.CHROME["supplements-text"]),
    "self-reported": ("○", _SELF_REPORTED_BASE, cs.CHROME["watch-text"]),
}

# Reading source tag -> tier. Only the sources that exist are mapped
# (loop_schema's biomarker writer tags "manual" = operator-entered =
# self-reported); an unmapped source renders NO tier claim — a gap is
# stated, never inferred. Lab-grade/wearable land here when those ingest
# sources exist.
_SOURCE_TIERS = {"manual": "self-reported"}

# The signals section's four 30-day aggregate slots (LM-02 gated: structure
# renders, values stay em-dash — the dashboard's designed-empty precedent).
# All four are wearable-tier streams.
_SIGNAL_SLOTS = ("Sleep avg", "HRV avg", "RHR avg", "Steps / day")

# The footer honesty line — verbatim per the facesheet spec.
_HONESTY_LINE = "every value tagged · gaps stated, never inferred · local-first · print-safe"


def _report_style():
    """Return the face sheet's own `<style>` block, built from system tokens.

    The page frame (~880px white page, 32px padding, 1px card-border edge,
    Inter), the 2px training-blue header rule, 14px section gaps, the 4x16px
    section accent bars, and the row/card/footer classes. Print-native: the
    gray app page-bg is overridden to paper, and print drops the edge and
    breaks before page two. Every color is a `component_set` token reference
    (plus the documented `_SELF_REPORTED_BASE` non-text chrome).
    """
    p, c, a = cs.PALETTE, cs.CHROME, cs.ACCENTS
    return f"""<style>
html, body {{ background: {p['paper']}; }}
.fs-page {{ max-width: 880px; margin: 24px auto; padding: 32px; background: {p['paper']}; border: 1px solid {c['card-border']}; font-family: Inter, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }}
.fs-header {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; }}
.fs-title {{ font-size: 20px; font-weight: 700; }}
.fs-caption {{ color: {p['muted']}; font-size: 12px; }}
.fs-status {{ color: {p['muted']}; font-size: 12px; margin-top: 4px; }}
.fs-head-block {{ border-bottom: 2px solid {a['training']}; padding-bottom: 12px; }}
.fs-sec {{ margin-top: 14px; }}
.fs-shead {{ display: flex; align-items: center; gap: 8px; }}
.fs-bar {{ display: inline-block; width: 4px; height: 16px; border-radius: 2px; }}
.fs-stitle {{ font-size: 13px; font-weight: 700; }}
.fs-card {{ border: 1px solid {c['card-border']}; border-radius: 8px; padding: 10px 14px; margin-top: 8px; }}
.fs-triage {{ background: {c['training-tint']}; }}
.fs-triage .fs-stitle {{ color: {c['training-text']}; }}
.fs-asks {{ background: {c['nutrition-tint']}; }}
.fs-row {{ display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; margin-top: 6px; font-size: 12px; }}
.fs-rowname {{ font-weight: 600; }}
.fs-adh {{ margin-left: auto; }}
.fs-exp {{ color: {c['watch-text']}; }}
.fs-trow {{ font-size: 12px; margin-top: 4px; }}
.fs-attn {{ background: {c['watch-tint']}; color: {c['watch-text']}; border-radius: 6px; padding: 2px 8px; }}
.fs-abrow {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; background: {c['concern-tint']}; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-size: 12px; }}
.fs-marker {{ font-size: 12px; font-weight: 700; color: {p['concern']}; }}
.fs-abrow .pill {{ margin-left: auto; }}
.fs-strip {{ background: {c['good-tint']}; color: {p['good']}; border-radius: 8px; padding: 8px 12px; margin-top: 6px; font-size: 12px; }}
.fs-siggrid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 8px; }}
.fs-sig {{ border: 1px solid {c['card-border']}; border-top: 3px solid {a['supplements']}; border-radius: 8px; padding: 8px; }}
.fs-tier {{ font-size: 11px; color: {p['muted']}; }}
.fs-sigval {{ font-size: 15px; font-weight: 700; }}
.fs-asklabel {{ font-size: 12px; font-weight: 600; }}
.fs-askrow {{ margin-top: 6px; font-size: 12px; }}
.fs-askrow .chip-b {{ margin-right: 6px; background: {p['paper']}; }}
.fs-foot {{ display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-top: 14px; padding-top: 10px; border-top: 1px solid {c['card-border']}; font-size: 11px; color: {p['muted']}; }}
.fs-page2 {{ margin-top: 24px; }}
@media print {{
  .fs-page {{ max-width: 100%; margin: 0; border: none; padding: 0; }}
  .fs-page2 {{ page-break-before: always; }}
}}
</style>"""


def _readings_by_item(store_read):
    """Group the store read model's readings into per-item reading lists."""
    by_item = {}
    for reading in store_read:
        by_item.setdefault(reading["item"], []).append(reading)
    return by_item


def _read_profile():
    """Parse the operator profile's header-relevant fields.

    Reads the FIRST existing `_PROFILE_PATHS` entry: the gitignored filled
    copy under `vault/scaffold/filled/` (ADR-0005's pinned filled-scaffold
    path) wins over the tracked scaffold. Returns initials (from the profile
    title — never the full name), the age BAND (decade, e.g. `40s`, derived
    from a filled Age field — the exact age never renders), and the
    January-issue status (a filled Current status field). An unfilled
    scaffold prompt (`<...>`) reads None, and no profile file at all reads
    all-None — the header renders its em-dash awaiting slots either way
    (ADR-0009 D2 honest absence; a fresh clone still generates).

    Returns:
        (dict) Keys `initials`, `age_band`, `issue_status`; None = unfilled.
    """
    fields = {"initials": None, "age_band": None, "issue_status": None}
    path = next((p for p in _PROFILE_PATHS if p.exists()), None)
    if path is None:
        return fields
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^# Operator Profile — (.+)$", text, re.M)
    if title:
        initials = "".join(
            word[0].upper() for word in title.group(1).split() if word[0].isalpha()
        )
        fields["initials"] = initials or None
    age = re.search(r"^- \*\*Age:\*\* (.+)$", text, re.M)
    if age:
        years = re.match(r"(\d+)", age.group(1).strip())
        # Plausible-age bound: a DOB-shaped value ("1982-03-15" -> 1982) or a
        # zero is not an age in years — render the em-dash, never a fabricated
        # band like "1980s" (ADR-0009 D2).
        if years and 0 < int(years.group(1)) < 120:
            fields["age_band"] = f"{int(years.group(1)) // 10 * 10}s"
    status = re.search(r"^- \*\*Current status:\*\* (.+)$", text, re.M)
    if status:
        value = status.group(1).strip()
        if value and not value.startswith("<"):
            fields["issue_status"] = value
    return fields


def _long_date(day):
    """Format a date in the face sheet's long form, e.g. `June 12, 2026`."""
    return f"{_MONTH_NAMES[day.month - 1]} {day.day}, {day.year}"


def _tier_markup(tier, with_word=False):
    """Render a tier's glyph span in its base chrome, plus a trailing space.

    Args:
        tier (str): A `_TIER_CHROME` key.
        with_word (bool, optional): Append the tier word in its AA `*-text`
            shade (the page-2 captions and the footer legend form).

    Returns:
        (str) The assembled tier markup.
    """
    glyph, base, text = _TIER_CHROME[tier]
    markup = f"<span style='color:{base}'>{glyph}</span> "
    if with_word:
        markup += f"<span style='color:{text}'>{tier}</span>"
    return markup


def _section(title, bar_hex, body_html, card_class=None):
    """Return one face-sheet section: 4x16 accent bar + 13px/700 title + body.

    Args:
        title (str): The section heading text (escaped).
        bar_hex (str): The accent-bar token hex (chrome, never data state).
        body_html (str): The assembled section body, included verbatim.
        card_class (str, optional): Wrap header+body in a tinted `.fs-card`
            of this class (the triage / asks cards).

    Returns:
        (str) The assembled `.fs-sec` markup.
    """
    head = (
        f"<div class='fs-shead'><span class='fs-bar' style='background:{bar_hex}'></span>"
        f"<span class='fs-stitle'>{cs._escape(str(title))}</span></div>"
    )
    if card_class is not None:
        return f"<div class='fs-sec'><div class='fs-card {card_class}'>{head}{body_html}</div></div>"
    return f"<div class='fs-sec'>{head}{body_html}</div>"


def _header_block(today):
    """Render the header: title, prepared date, and the initials status line.

    The status line carries operator INITIALS only; age band + issue status
    render from the profile when filled, em-dash otherwise; last review +
    next visit stay em-dash until LM-01 visit anchoring lands.
    """
    profile = _read_profile()
    prepared = _long_date(today)
    status_line = (
        f"Patient {profile['initials'] or '—'}"
        f" · age band {profile['age_band'] or '—'}"
        f" · issue status {profile['issue_status'] or '—'}"
        " · last review — · next visit —"
    )
    return (
        "<div class='fs-head-block'>"
        "<div class='fs-header'>"
        "<div class='fs-title'>A+ Maxing — Physician Face Sheet</div>"
        f"<div class='fs-caption'>Prepared {cs._escape(prepared)}</div>"
        "</div>"
        f"<div class='fs-status'>{cs._escape(status_line)}</div>"
        "</div>"
    )


def _triage_row(text, kind, rising=True):
    """Render one since-your-last-review delta row (the populated anatomy).

    Built ahead of LM-01 visit anchoring — the production path renders the
    first-visit copy until deltas are derivable. Direction-colored per the v3
    bindings: improving = PALETTE good with ▲/▼, attention = watch-text with
    ●, neutral = ink. Attention rows ride the measured watch-tint ground:
    watch-text directly on the card's training-tint computes 4.31 (< the 4.5
    AA floor, measured at build), so the watch pair carries the row.

    Args:
        text (str): The delta-row text (escaped).
        kind (str): "improving", "attention", or "neutral"; anything else
            KeyErrors (fail-loud, matching `pill`/`_series_color`).
        rising (bool, optional): Improving rows' arrow direction (▲/▼).

    Returns:
        (str) The assembled `.fs-trow` markup.
    """
    if kind == "improving":
        arrow = "▲" if rising else "▼"
        return (
            f"<div class='fs-trow' style='color:{cs.PALETTE['good']}'>"
            f"{arrow} {cs._escape(str(text))}</div>"
        )
    if kind == "attention":
        return f"<div class='fs-trow fs-attn'>● {cs._escape(str(text))}</div>"
    if kind == "neutral":
        return f"<div class='fs-trow'>{cs._escape(str(text))}</div>"
    raise KeyError(kind)


def _triage_section():
    """Render section 2 — the triage card, in its awaiting/first-visit state.

    Until LM-01 visit anchoring lands the card renders the first-visit copy,
    which is literally true in both the first-visit and model-not-landed
    conditions (facesheet spec) — `_triage_row` holds the populated anatomy.
    """
    body = "<div class='fs-trow'>No prior review — full baseline below</div>"
    return _section(
        "Since your last review", cs.ACCENTS["training"], body,
        card_class="fs-triage",
    )


def _since_text(readings, match):
    """Derive a regimen row's `since` from the item's EARLIEST stored plan.

    Scans the domain's stored plan readings in `store.read` (timepoint) order
    for the first whose plan value `match`es the rendered item — the item has
    been part of the regimen since that plan's date, not merely since today's
    re-recording. An unparseable earliest timepoint renders `since —` (honest
    absence, never an invented date).
    """
    earliest = next(r for r in readings if match(r["value"]))
    day = _reading_date(earliest["timepoint"])
    return f"since {_short_date(day)}" if day is not None else "since —"


def _regimen_rows(plan_readings, resolved_supplements, resolved_peptides):
    """Render the regimen rows from the day's resolved plans.

    Supplements rows render `name — dose`; the peptides row renders
    `compound · dose · route`, with an "experimental" tag switching the row
    detail to watch-text plus the disclosure note. `since` is the date of the
    EARLIEST stored plan whose value carries the same item (supplements: an
    items[].name match; peptides: the compound match) — `_since_text`. The
    adherence column stays an honest em-dash per row: the 30-day adherence
    aggregate model does not exist, and a fabricated % is a claim.
    """
    adherence = "<span class='fs-adh caption'>adherence —</span>"
    rows = []
    if resolved_supplements["state"] is None:
        for entry in resolved_supplements["plan"]["items"]:
            since = _since_text(
                plan_readings["supplements"],
                lambda v, name=entry["name"]: any(
                    i["name"] == name for i in v["items"]
                ),
            )
            rows.append(
                "<div class='fs-row'>"
                f"<span class='fs-rowname'>{cs._escape(entry['name'])} — {cs._escape(entry['dose'])}</span>"
                f"<span class='caption'>{cs._escape(since)}</span>"
                f"{adherence}</div>"
            )
    if resolved_peptides["state"] is None:
        plan = resolved_peptides["plan"]
        detail = f"{plan['compound']} · {plan['dose']} · {plan['route']}"
        since = _since_text(
            plan_readings["peptides"],
            lambda v: v["compound"] == plan["compound"],
        )
        if "experimental" in plan.get("tags", ()):
            name = (
                f"<span class='fs-rowname fs-exp'>{cs._escape(detail)}</span>"
                "<span class='fs-exp'>experimental — disclosure attached</span>"
            )
        else:
            name = f"<span class='fs-rowname'>{cs._escape(detail)}</span>"
        rows.append(
            f"<div class='fs-row'>{name}"
            f"<span class='caption'>{cs._escape(since)}</span>"
            f"{adherence}</div>"
        )
    return "".join(rows)


def _regimen_section(plan_readings, today):
    """Render section 3 — current regimen with adherence, from today's plans."""
    on_date = today.isoformat()
    supplements = plan_schema.resolve_plan(plan_readings.get("supplements", []), on_date)
    peptides = plan_schema.resolve_plan(plan_readings.get("peptides", []), on_date)
    body = _regimen_rows(plan_readings, supplements, peptides)
    if not body:
        body = cs.awaiting(
            "No supplement or peptide plan recorded for today — "
            "the regimen renders from the day's plan."
        )
    return _section(
        "Current regimen — with adherence", cs.ACCENTS["supplements"], body
    )


def _tier_glyph(source):
    """Render a reading source's tier glyph (non-text chrome), or ''.

    Only mapped sources render a glyph — an unmapped source states no tier.
    """
    tier = _SOURCE_TIERS.get(source)
    if tier is None:
        return ""
    return _tier_markup(tier)


def _numeric_readings(readings):
    """Split readings into the numeric-coercible subset and its float values."""
    numeric_readings, numeric = [], []
    for reading in readings:
        number = biomarker_meta.to_number(reading["value"])
        if number is not None:
            numeric_readings.append(reading)
            numeric.append(number)
    return numeric_readings, numeric


def _abnormal_detail(item, readings):
    """Compose an abnormal row's detail text from real store data.

    `value · ref <low> – <high> · <signed delta>/<window> · drawn <date>` —
    each segment renders only when its data exists: the delta needs two
    numeric readings, the window needs both their dates parseable, the drawn
    date needs the latest timepoint parseable. Never a fabricated segment.
    """
    meta = biomarker_meta.get(item)
    latest = readings[-1]["value"]
    low, high = meta["reference_range"]
    parts = [
        f"{latest} {meta['units']}",
        f"ref {_format_number(low)} – {_format_number(high)}",
    ]
    numeric_readings, numeric = _numeric_readings(readings)
    if len(numeric) >= 2:
        delta = numeric[-1] - numeric[-2]
        sign = "+" if delta > 0 else ""
        delta_text = f"{sign}{_format_number(delta)}"
        last_day = _reading_date(numeric_readings[-1]["timepoint"])
        prev_day = _reading_date(numeric_readings[-2]["timepoint"])
        if last_day is not None and prev_day is not None:
            delta_text += f"/{(last_day - prev_day).days}d"
        parts.append(delta_text)
    drawn = _reading_date(readings[-1]["timepoint"])
    if drawn is not None:
        parts.append(f"drawn {_short_date(drawn)}")
    return " · ".join(parts)


def _abnormal_row(item, readings):
    """Render one out-of-range biomarker row on the concern tint.

    Marker name in PALETTE concern, the source-tier glyph (honest — only for
    a mapped source), the real-data detail, and the watch chip on the
    measured watch pair — the chip renders ONLY here, for out-of-range
    registered markers.
    """
    return (
        "<div class='fs-abrow'>"
        f"<span class='fs-marker'>{cs._escape(biomarker_meta.display_name(item))}</span>"
        f"{_tier_glyph(readings[-1]['source'])}"
        f"<span>{cs._escape(_abnormal_detail(item, readings))}</span>"
        f"{cs.pill('watch', 'watch')}"
        "</div>"
    )


def _biomarker_section(biomarkers):
    """Render section 4 — biomarkers out of range, then the in-range strip.

    Abnormal-first: every `state_for == "concern"` item renders an abnormal
    row (name-sorted); the in-range collapse strip carries the REAL count of
    `good` items. No abnormals -> no abnormal rows (the strip still renders
    honestly); no biomarker streams at all -> one muted awaiting line.

    Args:
        biomarkers (dict): item -> readings for the biomarker-shaped streams.
    """
    if not biomarkers:
        body = cs.awaiting("No biomarker readings on file yet.")
    else:
        states = {
            item: cs.state_for(item, readings[-1]["value"])
            for item, readings in biomarkers.items()
        }
        rows = [
            _abnormal_row(item, biomarkers[item])
            for item in sorted(biomarkers)
            if states[item] == "concern"
        ]
        in_range = sum(1 for state in states.values() if state == "good")
        plural = "marker" if in_range == 1 else "markers"
        strip = (
            f"<div class='fs-strip'>✓ {in_range} {plural} in range — "
            "full table with sparklines on page 2</div>"
        )
        body = "".join(rows) + strip
    return _section(
        "Biomarkers — out of range or trending",
        cs.SECTION_ACCENTS["biomarkers"],
        body,
    )


def _goals_section():
    """Render section 5 — goals & trajectory (awaiting: no goal model yet)."""
    return _section(
        "Goals & trajectory",
        cs.SECTION_ACCENTS["goals"],
        cs.awaiting("No goals on file — the goal model is pending."),
    )


def _signals_section():
    """Render section 6 — patient-generated signal aggregates (LM-02 gated).

    The dashboard's designed-empty precedent: the four stat boxes render
    their structure — wearable-tier top edge, tier glyph + label row, em-dash
    value — with no invented number and no direction arrow.
    """
    boxes = "".join(
        "<div class='fs-sig'>"
        f"<div class='fs-tier'>{_tier_markup('consumer wearable')}consumer wearable</div>"
        "<div class='fs-sigval'>—</div>"
        f"<div class='caption'>{cs._escape(label)}</div>"
        "</div>"
        for label in _SIGNAL_SLOTS
    )
    caption = (
        "<div class='caption'>Thirty-day aggregates arrive with the first "
        "wearable baseline window.</div>"
    )
    return _section(
        "Patient-generated signals — 30-day aggregates",
        cs.ACCENTS["sleep"],
        f"<div class='fs-siggrid'>{boxes}</div>{caption}",
    )


def _pending_panels(panels):
    """Return the panel items still pending, by source provenance.

    Mirrors `loop_schema.read_panel`'s resolution over the read model: the
    pending marker is the only reading written under the plan-recommendation
    tag, so a panel is pending iff NO reading carries another source.
    """
    return [
        item
        for item, readings in sorted(panels.items())
        if all(r["source"] == _TAG_PANEL for r in readings)
    ]


def _asks_section(panels, plan_readings, answered_watchouts, today):
    """Render section 7 — asks & agenda on the nutrition-tint card.

    `Order today:` renders one bordered chip per pending `panel::` draw (real
    provenance-resolved state); `Patient questions:` derives from the active
    peptide protocol's watch-out questions that have no stored answer yet.
    Either line renders a muted none-state when empty.
    """
    pending = _pending_panels(panels)
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
        question_line = (
            "<span class='caption'>none queued — watch-outs raise questions "
            "here when a protocol is active</span>"
        )
    body = (
        f"<div class='fs-askrow'><span class='fs-asklabel'>Order today:</span> {chips}</div>"
        f"<div class='fs-askrow'><span class='fs-asklabel'>Patient questions:</span> {question_line}</div>"
    )
    return _section(
        "Asks & agenda", cs.ACCENTS["nutrition"], body, card_class="fs-asks"
    )


def _footer(today):
    """Render the footer: the colored source-tier legend + the honesty line."""
    legend = " · ".join(
        _tier_markup(tier, with_word=True) for tier in _TIER_CHROME
    )
    generated = _long_date(today)
    return (
        "<div class='fs-foot'>"
        f"<span>{legend}</span>"
        f"<span>{_HONESTY_LINE} · generated {cs._escape(generated)}</span>"
        "</div>"
    )


def _table(readings):
    """Return a comparison table (timepoint, source, value) for one item's readings.

    All three cells coerce through `str` — a raw-appended non-string timepoint
    or source must render its text, never crash the whole sheet.
    """
    rows = "".join(
        "<tr>"
        f"<td>{cs._escape(str(r['timepoint']))}</td>"
        f"<td>{cs._escape(str(r['source']))}</td>"
        f"<td>{cs._escape(str(r['value']))}</td>"
        "</tr>"
        for r in readings
    )
    return (
        "<table><caption class='caption'>readings</caption>"
        "<thead><tr><th>timepoint</th><th>source</th><th>value</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _item_caption(item, readings):
    """Render a page-2 item heading's tier glyph + ref range caption, or ''.

    The tier renders only for a mapped source (glyph in base chrome, tier
    word in its `*-text` shade); the ref range only where registered. Neither
    -> no caption line.
    """
    parts = []
    tier = _SOURCE_TIERS.get(readings[-1]["source"])
    if tier is not None:
        parts.append(_tier_markup(tier, with_word=True))
    meta = biomarker_meta.get(item)
    if meta is not None and meta["reference_range"] is not None:
        low, high = meta["reference_range"]
        parts.append(
            cs._escape(
                f"ref {_format_number(low)} – {_format_number(high)} {meta['units']}"
            )
        )
    if not parts:
        return ""
    return f"<div class='caption'>{' · '.join(parts)}</div>"


def _item_section(item, readings):
    """Render one page-2 per-item section.

    `plan::`/`plan-track::` items keep the verbatim heading + readings table
    (ADR-0010 D5 — no KPI, no sparkline). A stream with numeric readings
    renders the full anatomy: heading, tier/ref caption, latest-value KPI,
    polyline sparkline over ONLY the numeric values (state judged from the
    RAW latest reading — the page-1 abnormal gate's basis), and the table. A
    stream with NO numeric reading routes table-only — a string must never
    reach numeric viz.
    """
    if item.startswith(("plan::", "plan-track::")):
        return (
            "<section>"
            f"<h2>{cs._escape(item)}</h2>"
            f"{_table(readings)}"
            "</section>"
        )
    caption = _item_caption(item, readings)
    _numeric_reads, numeric = _numeric_readings(readings)
    if not numeric:
        return (
            "<section>"
            f"<h2>{cs._escape(item)}</h2>"
            f"{caption}{_table(readings)}"
            "</section>"
        )
    # ONE state basis sheet-wide: the RAW latest value — the same basis as the
    # page-1 abnormal gate and the page-2 ordering key. A stream whose latest
    # reading is non-numeric claims NO current concern anywhere; the sparkline
    # still plots the numeric history, tinted neutral.
    state = cs.state_for(item, readings[-1]["value"])
    return (
        "<section>"
        f"<h2>{cs._escape(item)}</h2>"
        f"{caption}"
        f"{cs.kpi(biomarker_meta.display_name(item), readings[-1]['value'])}"
        f"{cs.sparkline(numeric, state)}"
        f"{_table(readings)}"
        "</section>"
    )


def _detail_page(by_item):
    """Render page 2 — every item's readings, abnormal items first.

    Ordering: `state_for == "concern"` items first, then everything else,
    each group item-sorted (deterministic; clinical grouping awaits a model —
    never alphabetical-as-clinical-claim, the order is stated by the
    heading).
    """
    ordered = sorted(
        by_item,
        key=lambda item: (
            0 if cs.state_for(item, by_item[item][-1]["value"]) == "concern" else 1,
            item,
        ),
    )
    sections = "".join(_item_section(item, by_item[item]) for item in ordered)
    head = (
        "<div class='fs-shead'>"
        f"<span class='fs-bar' style='background:{cs.SECTION_ACCENTS['biomarkers']}'></span>"
        "<span class='fs-stitle'>Page 2 — full readings, abnormal first</span></div>"
    )
    return f"<div class='fs-page2'>{head}{sections}</div>"


def render(store_read, _today=None):
    """Assemble the Physician Face Sheet HTML from the shared component set.

    Args:
        store_read (list): The store read model passed through by render.emit.
        _today (datetime.date, optional): Test-only date seam (the prepared
            date, plan resolution, and footer); defaults to the current date.

    Returns:
        (str) The assembled face-sheet HTML (single document, inline styling,
        zero scripts).

    Raises:
        KeyError: An item carries a `::` prefix outside the routed stream
            types, or an unknown plan:: domain suffix (fail-loud; the
            dashboard's ADR-0008 D3 contract, mirrored).
    """
    today = _today if _today is not None else datetime.date.today()
    by_item = _readings_by_item(store_read)
    plan_readings, panels, biomarkers = {}, {}, {}
    answered_watchouts = set()
    for item, readings in by_item.items():
        if item.startswith("biomarker::"):
            biomarkers[item] = readings
        elif item.startswith("plan::"):
            domain = item[len("plan::"):]
            if domain not in plan_schema.PLAN_DOMAINS:
                raise KeyError(
                    f"unrouted plan:: domain {domain!r}: routing for a new "
                    f"stream type is added deliberately, never by silent fallthrough"
                )
            # Only the regimen/asks consumers' domains; workout/nutrition
            # plans render page-2 verbatim only (via by_item).
            if domain in ("supplements", "peptides"):
                plan_readings[domain] = readings
        elif item.startswith("plan-track::"):
            pass  # page-2 verbatim table only
        elif item.startswith("panel::"):
            panels[item] = readings
        elif item.startswith("watch-out::"):
            answered_watchouts.add(item[len("watch-out::"):])
        elif item.startswith("feedback::"):
            pass  # page-2 table only
        elif "::" in item:
            prefix = item.split("::", 1)[0] + "::"
            raise KeyError(
                f"unrouted stream prefix {prefix!r}: routing for a new stream "
                f"type is added deliberately, never by silent fallthrough"
            )
        else:
            biomarkers[item] = readings
    body = (
        "<div class='fs-page'>"
        f"{_header_block(today)}"
        f"{_triage_section()}"
        f"{_regimen_section(plan_readings, today)}"
        f"{_biomarker_section(biomarkers)}"
        f"{_goals_section()}"
        f"{_signals_section()}"
        f"{_asks_section(panels, plan_readings, answered_watchouts, today)}"
        f"{_footer(today)}"
        f"{_detail_page(by_item)}"
        "</div>"
    )
    return (
        "<!doctype html><html lang='en'>"
        f"{cs.head('A+ Maxing — Physician Face Sheet', _report_style())}"
        f"<body>{body}</body></html>"
    )
