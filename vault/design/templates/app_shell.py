"""Served SPA front-end (ADR-0029): the operator-approved prototype design (`app_view.html`)
rendered with the live ingestion load-state.

The design source of truth is `app_view.html` — the verbatim prototype port: inline lucide
SVG + an inlined image (render.emit-clean), honest empty-data, the wired chat composers, and
the demographic form that POSTs the four gate-bound capture tokens to `/upload`. `render`
reads that design and injects the ONE load-state-dependent surface — the Upload "Link your
documents" cards (`<!--DOC_CARDS-->`) — from the ingestion `status` (resolved by
`generate.run('app')` via `scripts.ingest.status`): an empty store shows honest "+ Link"
cards, a loaded stream shows the landed names/counts (names/counts only, never a raw reading
value or rsid). The page's lucide icons are vendored inline in `app_view.html`; the four
document-card icons are `_DOC_ICONS` below.
"""
import datetime as _datetime
import html as _html
import pathlib
import re as _re

from scripts.ingest import status as ingest_status
from scripts.plan.router import summarize

_VIEW = pathlib.Path(__file__).with_name("app_view.html")

# The four 'Link your documents' card icons (the prototype's inline SVG paths), keyed by
# document class — rendered into the load-state-aware cards that replace <!--DOC_CARDS-->.
_DOC_ICONS = {
    "wearable": '<path d="M3 12h4l2 6 4-14 2 8h6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "labs": '<path d="M6 2h7l5 5v15H6z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M13 2v5h5" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    "medical": '<rect x="5" y="3" width="14" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M9 8h6M9 12h6M9 16h4" stroke="currentColor" stroke-width="1.6"/>',
    "dna": '<path d="M8 3c0 5 8 6 8 9s-8 4-8 9M16 3c0 5-8 6-8 9s8 4 8 9" fill="none" stroke="currentColor" stroke-width="1.6"/>',
}

_LINK = "<span class='link'>+ Link</span>"
_LOADED = "<span style='color:var(--good);font-weight:600'>✓ loaded</span>"

# The 'About you' demographic store items the served form pre-fills from (each form field
# name == its store item name; `capture.persist_capture` writes each under its own name).
# `date-of-birth` is the amended full-date input and `bodyweight-kg` the amended number input
# (each pre-fills its `value=`); the two SELECT tokens pre-SELECT their saved option (ADR-0034
# retired the `bodyweight-band` select). `goal-domains` is DELIBERATELY ABSENT — it is a
# chat-only rich-section field (gathered at POST /chat), not a field on this demographic form,
# so it has no select/checkbox surface here to pre-fill.
_DEMOGRAPHIC_SELECTS = ("sex-for-dosing", "equipment-access-class")
_DEMOGRAPHIC_DOB = "date-of-birth"
_DEMOGRAPHIC_WEIGHT = "bodyweight-kg"

# The unlocked My-Info panel's editable free-text fields (ADR-0033-0035-T7), each mapped to the
# store item its saved value resolves from — the pinned capture<->form contract: the goal tokens
# write a store item of their own name; the four `_CHAT_RAW_SOURCE_FIELDS` write a `raw-*-free-text`
# raw-source item (see `scripts.serve.capture`). A field whose store item has no reading stays
# blank (no fabricated value). Distinct from `_DEMOGRAPHIC_SELECTS`: these are `value=`-injected
# text inputs, not option-pre-selected <select>s.
_MYINFO_TEXT_FIELDS = {
    "goal-domains": "goal-domains",
    "goal-targets": "goal-targets",
    "goal-priority-order": "goal-priority-order",
    "training-detail": "raw-training-detail-free-text",
    "nutrition-detail": "raw-nutrition-free-text",
    "supplement-stack": "raw-supplement-free-text",
    "peptide-stack": "raw-peptide-free-text",
}

# The first-run completeness gate (ADR-0033 Decision / OQ-2 / ST-04). The served body is
# CONDITIONAL on `_intake_complete`: the SEVEN directly-captured required `summarize` tokens
# are all CONDITIONALLY set (omitted from the summary when their source reading is absent), so
# keying on their PRESENCE naturally EXCLUDES the always-set tokens — `rx-interaction-classes`
# (filled only post-unlock by the ADR-0035 review; requiring it would deadlock the gate, ST-04)
# and the always-set derived bands. The three `safety-screen::*` answered markers are scanned
# from the flat read model directly (they are not SUMMARY_FIELD_SET members).
_REQUIRED_TOKENS = (
    "training-age-band", "sex-for-dosing", "bodyweight-band", "equipment-access-class",
    "goal-domains", "goal-targets", "goal-priority-order",
)
_REQUIRED_SAFETY_MARKERS = (
    "safety-screen::exercise-safety", "safety-screen::phq2", "safety-screen::apnea",
)
# The four platform `.screen` sections stripped from the served body when the profile is
# INCOMPLETE — markup-level absence (not a CSS hide), so 0 platform surface is reachable on
# first run. The Create-Profile `#screen-wizard`/`#screen-equipment` sections are preserved.
_PLATFORM_SCREENS = ("screen-dashboard", "screen-plan", "screen-team", "screen-profile")


def _esc(value):
    """HTML-escape a display string — a filename/source is never trusted raw into markup."""
    return _html.escape(str(value), quote=True)


def _doc_card(icon_key, title, sub, state_html):
    """One 'Link your documents' card (prototype `.doc` markup) for a document class."""
    return (f"<div class='doc'><svg class='ic' viewBox='0 0 24 24'>{_DOC_ICONS[icon_key]}</svg>"
            f"<div class='m'><div class='t'>{title}</div><div class='d'>{sub}</div></div>"
            f"<div class='st'>{state_html}</div></div>")


def _doc_cards(status):
    """The four document cards, driven by the live ingestion load-state (names/counts only).

    An unloaded class shows the honest "+ Link" affordance; a loaded class flips to a
    "✓ loaded" state naming the landed file(s) `_esc`-escaped — never a raw reading value.
    """
    we = status["wearable"]
    if we.get("loaded"):
        sub = (f"{_esc(we['source'])} · {we['count']} readings · {_esc(', '.join(we['items']))} · "
               f"{_esc(we['range'][0])} – {_esc(we['range'][1])}")
        # Generic title; the source is render-state-driven from the load-state, never a hardcode
        # (NFR-4: the operator flagged a hardcoded single source as a recurring failure class).
        wearable = _doc_card("wearable", f"Wearable export · detected: {_esc(we['source'])}", sub, _LOADED)
    else:
        wearable = _doc_card("wearable", "Wearable export", "Wearable / fitness tracker export", _LINK)

    labs = status["labs"]
    if labs.get("loaded"):
        labs_card = _doc_card("labs", "Labs &amp; bloodwork", _esc(", ".join(labs["files"])), _LOADED)
    else:
        labs_card = _doc_card("labs", "Labs &amp; bloodwork", "PDF or CSV", _LINK)

    medical = _doc_card("medical", "Medical history", "PDF, document, or paste", _LINK)

    dna = status["dna"]
    if dna.get("loaded"):
        # A dropzone 23andMe file names the file; an extracted genetics-report PDF (ADR-0031,
        # no dropzone file) names its genotype-reading count instead — never crash on files[0].
        dna_detail = (f"{_esc(dna['files'][0])} landed" if dna.get("files")
                      else f"{dna.get('count', 0)} genotypes landed")
        dna_card = _doc_card("dna", "DNA", dna_detail, _LOADED)
    else:
        dna_card = _doc_card("dna", "DNA (23andMe)", "23andMe raw .zip", _LINK)

    return f"{wearable}{labs_card}{medical}{dna_card}"


def _default_status(store_read):
    """Standalone-render status: wearable from store_read; DNA/labs unknown without their roots."""
    return {"wearable": ingest_status.wearable_status(store_read),
            "dna": {"loaded": False, "files": []},
            "labs": {"loaded": False, "files": []}}


_PLAN_LABELS = [("workout", "Workout"), ("nutrition", "Nutrition"),
                ("supplements", "Supplements"), ("peptides", "Peptides")]

# The static Plan-screen body shown when no plan is recorded for today — the honest awaiting state
# (preserved from the pre-wiring template, injected by `_plan_zone` so the no-plan case is unchanged).
_AWAITING_PLAN = (
    '<div class="card" style="margin-bottom:18px;display:flex;align-items:center;'
    "justify-content:space-between;gap:16px\">"
    "<div data-awaiting='plan'><div style=\"font-weight:700;font-size:15px\">No approved plan yet</div>"
    '<div class="sub">Once you\'ve loaded your documents and talked through your goals, generate your '
    "plan here. When you approve it, this screen shows your approved plan.</div></div>"
    '<button class="btn primary" id="plan-gen-run" style="flex:none">Generate plan &rarr;</button>'
    "</div>"
    "<div id='plan-gen-status' class='sub' role='status' style='display:none;margin-bottom:18px'></div>"
)


def _plan_item_lines(domain, plan):
    """Render one domain's recorded plan value into a list of `<li>` strings."""
    if not isinstance(plan, dict):
        return []
    lines = []
    if domain == "workout":
        for ex in plan.get("exercises", []):
            sets, reps = ex.get("sets"), ex.get("reps")
            head = f"{sets}×{reps}" if sets and reps else (f"{sets} sets" if sets else "")
            tail = " · ".join(p for p in (head, ex.get("detail")) if p)
            suffix = f" — {_esc(tail)}" if tail else ""
            lines.append(f"<li><b>{_esc(ex.get('name', ''))}</b>{suffix}</li>")
    elif domain == "nutrition":
        m = plan.get("macros") or {}
        water = f" · water {_esc(plan['water_l'])}L" if plan.get("water_l") else ""
        lines.append(
            f"<li><b>{_esc(plan.get('calorie_goal', '?'))} kcal/day</b> — protein "
            f"{_esc(m.get('protein', '?'))}g · carbs {_esc(m.get('carbs', '?'))}g · fat "
            f"{_esc(m.get('fat', '?'))}g{water}</li>"
        )
        for meal in plan.get("meals", []):
            kcal = f" ({_esc(meal['kcal'])} kcal)" if meal.get("kcal") else ""
            contents = f" — {_esc(meal['contents'])}" if meal.get("contents") else ""
            lines.append(f"<li><b>{_esc(meal.get('name', ''))}</b>{kcal}{contents}</li>")
    elif domain == "supplements":
        for item in plan.get("items", []):
            timing = f" · {_esc(item['timing'])}" if item.get("timing") else ""
            lines.append(
                f"<li><b>{_esc(item.get('name', ''))}</b> — {_esc(item.get('dose', ''))}{timing}</li>"
            )
    elif domain == "peptides":
        route = f" · {_esc(plan['route'])}" if plan.get("route") else ""
        lines.append(
            f"<li><b>{_esc(plan.get('compound', ''))}</b> — {_esc(plan.get('dose', ''))}{route}</li>"
        )
    return lines


def _plan_zone(store_read, today):
    """Read each domain's recorded plan for `today` and render the Plan-screen body.

    `store_read` is the flat reading list `store.read_all` returns; the domain's plan readings are
    filtered out by item name and resolved with `plan_schema.resolve_plan` (the same resolution the
    dashboard plan zone uses). Renders one card per domain with a plan recorded for today; with no
    plan in any domain, returns the unchanged honest awaiting state.
    """
    from scripts.store import plan_schema

    rows = store_read if isinstance(store_read, list) else []
    cards = []
    for domain, label in _PLAN_LABELS:
        item = f"{plan_schema._PREFIX_PLAN}{domain}"
        readings = [r for r in rows if isinstance(r, dict) and r.get("item") == item]
        resolved = plan_schema.resolve_plan(readings, today)
        plan = resolved.get("plan")
        lines = _plan_item_lines(domain, plan) if plan is not None else []
        if not lines:
            continue
        specialist = resolved.get("specialist") or label
        cards.append(
            f'<div class="card" style="margin-bottom:14px">'
            f'<div style="font-weight:700;font-size:15px;margin-bottom:6px">{_esc(label)}'
            f'<span class="sub" style="font-weight:500"> · {_esc(specialist)}</span></div>'
            f'<ul style="margin:0;padding-left:18px;line-height:1.6">{"".join(lines)}</ul></div>'
        )
    if not cards:
        return _AWAITING_PLAN
    return "".join(cards)


# The human labels for the three intake safety screens whose positive referral flags surface in
# the My-Info doctor-visit display (ADR-0033-0035-T3/T10). Keyed by the pinned `referral.collate`
# screen name; the value is the de-identified display label (never the raw operator answer).
_REFERRAL_LABELS = {
    "exercise-safety": "Exercise safety — chest pain, dizziness, or breathlessness on exertion",
    "phq2": "Mood check (PHQ-2)",
    "apnea": "Possible sleep apnea",
}


def _referral_zone(store_read):
    """Render the intake safety-screen referral flags for the My-Info doctor-visit display.

    The T3 production consumer of `referral.collate` (which had no caller until T10): each positive
    `referral::<screen>` flag written at capture becomes a doctor-visit line naming the screen (the
    de-identified human label, NEVER the raw answer); with 0 flags the section shows an honest
    "nothing flagged" state. The flags are never a plan input — this is a read-only display over the
    de-identified positivity signals, mirroring `referral.collate`'s caller contract.

    Args:
        store_read (list): The flat cross-item reading list (`store.read_all` shape); adapted into
            the per-item callable `referral.collate` expects.

    Returns:
        (str) The doctor-visit referral markup (a flagged list, or the honest no-referral note).
    """
    from scripts.serve import referral

    rows = store_read if isinstance(store_read, list) else []
    flagged = referral.collate(
        lambda item: [r for r in rows if isinstance(r, dict) and r.get("item") == item]
    )
    if not flagged:
        return ("<div class='note'>Nothing from your intake screens was flagged for your "
                "doctor visit.</div>")
    items = "".join(f"<li>{_esc(_REFERRAL_LABELS.get(screen, screen))}</li>" for screen in flagged)
    return (f"<div class='note'>These intake answers are flagged to raise with your doctor — "
            f"they never enter your plan.</div>"
            f"<ul style='margin:8px 0 0;padding-left:18px;line-height:1.6'>{items}</ul>")


def _latest_values(store_read, names):
    """The latest-by-timepoint stored value for each of `names`, from the flat store read.

    `store_read` is the flat reading list `store.read_all` returns (item-then-timepoint
    ordered). For each requested item this keeps the reading with the greatest `timepoint`
    (ties resolve to the last seen, mirroring the store's last-in-file resolution). An item
    with no reading is simply absent from the result — no fabricated default.

    Args:
        store_read (list): The flat cross-item reading list.
        names (tuple): The item names to resolve a latest value for.

    Returns:
        (dict) Item name -> its latest stored value, only for items that have a reading.
    """
    latest = {}
    rows = store_read if isinstance(store_read, list) else []
    for r in rows:
        if not isinstance(r, dict) or r.get("item") not in names:
            continue
        timepoint = r.get("timepoint", "")
        prior = latest.get(r["item"])
        if prior is None or timepoint >= prior[0]:
            latest[r["item"]] = (timepoint, r.get("value"))
    return {item: value for item, (_tp, value) in latest.items()}


def _prefill_form(html, store_read):
    """Pre-fill the 'About you' demographic form from the operator's saved store values.

    Reads the latest saved reading per demographic item and re-renders the existing static
    form markup with the matching <select> option pre-SELECTED and the amended full-date
    birthdate + `bodyweight-kg` number inputs' `value=` pre-filled, so the operator does not
    re-type data the store already holds. A field with no saved reading stays blank/default
    (no fabricated value). When any demographic is pre-filled, a '✓ Saved — edit to update'
    banner is injected as the form's first child so the operator sees they were remembered.
    The saved classes are de-identified; the birthdate/weight are the operator's own values
    rendered back over the local loopback (no egress).

    Args:
        html (str): The rendered SPA HTML (post DOC_CARDS/PLAN_ZONE substitution).
        store_read (list): The flat cross-item reading list driving the pre-fill.

    Returns:
        (str) The HTML with the demographic form pre-filled, or unchanged when nothing saved.
    """
    saved = _latest_values(store_read, (_DEMOGRAPHIC_DOB, _DEMOGRAPHIC_WEIGHT, *_DEMOGRAPHIC_SELECTS))
    rich = _latest_values(store_read, tuple(set(_MYINFO_TEXT_FIELDS.values())))
    if not saved and not rich:
        return html  # nothing saved — honest blank/default form, no banner

    for name in _DEMOGRAPHIC_SELECTS:
        value = saved.get(name)
        if value is None:
            continue
        option = f"<option value='{_esc(value)}'>"
        html = html.replace(option, f"<option value='{_esc(value)}' selected>", 1)

    # The unlocked My-Info panel's free-text fields (T7): inject each field's latest saved value
    # from its mapped store item. A field with no saved reading stays blank (honest-data).
    for field, item in _MYINFO_TEXT_FIELDS.items():
        value = rich.get(item)
        if value is None:
            continue
        html = html.replace(f"name='{field}'>", f"name='{field}' value='{_esc(value)}'>", 1)

    dob = saved.get(_DEMOGRAPHIC_DOB)
    if dob is not None:
        html = html.replace(
            "id='date-of-birth' name='date-of-birth'>",
            f"id='date-of-birth' name='date-of-birth' value='{_esc(dob)}'>",
            1,
        )

    weight = saved.get(_DEMOGRAPHIC_WEIGHT)
    if weight is not None:
        # The store is canonical kg; the operator's unit is pounds. Convert kg -> lb for the
        # My-Info display AND select the lbs unit, so the number and its label agree — the bug
        # was the kg value shown under the default 'lbs' label (e.g. "108 lbs" for a 108 kg /
        # 238 lb operator). A faithful conversion, never a fabricated value; a non-numeric value
        # falls back to as-is under kg (no conversion).
        try:
            display = str(round(float(weight) / 0.453592))
            unit_opt = "<option value='lbs'>lbs</option>"
            html = html.replace(unit_opt, "<option value='lbs' selected>lbs</option>", 1)
        except (ValueError, TypeError):
            display = _esc(weight)
        html = html.replace(
            "name='bodyweight-kg' placeholder=\"Weight\"",
            f"name='bodyweight-kg' value='{display}' placeholder=\"Weight\"",
            1,
        )

    if not saved:
        return html  # only rich free-text prefilled — no demographic banner (unchanged semantics)
    banner = ("<div class='upload-status' data-prefill='saved'>"
              "<span style='color:var(--good);font-weight:600'>✓ Saved — edit to update</span></div>")
    return html.replace(
        "<form action='/upload' method='post'>",
        f"<form action='/upload' method='post'>{banner}",
        1,
    )


def _intake_complete(store_read):
    """Whether the first-run profile is complete enough to unlock the platform surfaces.

    A pure function of the store-derived state, re-read each render — NOT a stored boolean, a
    turn-count, or a model flag, and explicitly NOT `chat.plan_next_turn(...).intake_complete`
    (which is vacuously True at zero domain coverage). `store_read` is the FLAT reading list
    `store.read_all` returns; it is ADAPTED into the per-item callable `summarize` contracts (a
    closure filtering the flat list by item name). True iff all seven required tokens are PRESENT
    keys in the summary AND the three safety-screen answered markers are in the flat list. Does
    NOT require `rx-interaction-classes` or any always-set token, and does NOT swallow
    `summarize`'s fail-closed `ValueError` (fail-loud at the boundary).
    """
    rows = store_read if isinstance(store_read, list) else []
    summary = summarize(lambda item: [r for r in rows if isinstance(r, dict) and r.get("item") == item])
    if not all(token in summary for token in _REQUIRED_TOKENS):
        return False
    present = {r.get("item") for r in rows if isinstance(r, dict)}
    return all(marker in present for marker in _REQUIRED_SAFETY_MARKERS)


def _mark_screen_active(html, screen_id):
    """Mark ONE `.screen` section active server-side (the first render decides the open surface)."""
    return html.replace(
        f'<section class="screen" id="{screen_id}">',
        f'<section class="screen active" id="{screen_id}">',
        1,
    )


def _lock_to_create_profile(html):
    """The INCOMPLETE-profile body: strip the four platform `.screen` sections and open the wizard.

    Removes the dashboard/plan/team/profile sections at the markup level (their `id="screen-*"` and
    the `data-tab="generate"` tab go with them), leaving the Create-Profile `#screen-wizard`/
    `#screen-equipment` surface, and marks the wizard active so first run opens on it.
    """
    for screen_id in _PLATFORM_SCREENS:
        html = _re.sub(
            rf'<section class="screen" id="{screen_id}">.*?</section>',
            "", html, count=1, flags=_re.DOTALL,
        )
    return _mark_screen_active(html, "screen-wizard")


# The wizard fields the Create-Profile flow can pre-fill from an already-populated store, so an
# operator who ingested data in a prior session (DNA/wearable/partial demographics) does NOT re-type
# what the store already holds. Keyed by the store item; the wizard input carries the same name.
_WIZARD_PREFILL_ITEMS = ("date-of-birth", "sex-for-dosing", "equipment-access-class", "goal-domains",
                         "raw-training-experience")


def _wizard_prefill_script(store_read):
    """Emit a `window.__aplusSaved` script with the store values the wizard can pre-fill (client-side).

    The locked Create-Profile wizard is NOT server-side pre-filled (its inputs are static markup); the
    client reads this blob on load and populates the matching wizard fields when there is no in-progress
    draft, so an operator who already has demographics/goals in the store re-enters only what is genuinely
    missing. The values are the operator's own (a local DOB, de-identified class tokens) rendered back over
    loopback — the same posture as `_prefill_form`. `</` is escaped so a value can never break the tag.
    """
    import json

    rows = store_read if isinstance(store_read, list) else []
    saved = _latest_values(rows, _WIZARD_PREFILL_ITEMS)
    # The store item is `raw-training-experience` (named-excluded raw source), but the wizard input
    # is `name='training-experience'`; the client fills by input name, so re-key it to match.
    if "raw-training-experience" in saved:
        saved["training-experience"] = saved.pop("raw-training-experience")
    blob = json.dumps(saved).replace("</", "<\\/")
    return f"<script>window.__aplusSaved={blob};</script>"


def _welcome_back_banner(store_read):
    """A wizard banner for a RETURNING operator: names what's restored + what's genuinely still needed.

    When the store already holds demographics/goals (a prior session), a returning operator lands on a
    mostly-blank Step 1 (a year-only birthdate cannot populate the date input; there is no stored weight)
    and reasonably reads it as "nothing came back". This banner states plainly what was restored (sex /
    equipment / goals / birth year — the store DOES have them) and what still needs entering (body weight,
    goal targets/priority, the safety screens — the required tokens the store lacks). Empty for a fresh
    operator (nothing saved). Derived from the store, names/flags only — never a raw value.
    """
    rows = store_read if isinstance(store_read, list) else []
    saved = _latest_values(rows, _WIZARD_PREFILL_ITEMS)
    if not saved:
        return ""  # a fresh operator — no returning-operator banner
    names = {"sex-for-dosing": "sex", "equipment-access-class": "equipment access", "goal-domains": "goals"}
    restored = [names[k] for k in ("sex-for-dosing", "equipment-access-class", "goal-domains") if saved.get(k)]
    dob = saved.get("date-of-birth")
    if dob:
        restored.append("birth year" if _re.fullmatch(r"\d{4}", str(dob)) else "birthdate")
    summary = summarize(lambda item: [r for r in rows if isinstance(r, dict) and r.get("item") == item])
    present = {r.get("item") for r in rows if isinstance(r, dict)}
    need = []
    if "bodyweight-band" not in summary:
        need.append("body weight")
    if "goal-targets" not in summary:
        need.append("goal targets")
    if "goal-priority-order" not in summary:
        need.append("goal priority order")
    if not all(m in present for m in _REQUIRED_SAFETY_MARKERS):
        need.append("the safety screens")
    parts = []
    if restored:
        parts.append(f"<b>Restored from your saved data:</b> {_esc(', '.join(restored))}.")
    if need:
        parts.append(f"<b>Still needed:</b> {_esc(', '.join(need))} — the rest is already on file.")
    return ("<div class='card' style='margin:0 0 16px;background:var(--good-bg);border-color:var(--good)'>"
            f"<div style='font-size:13px;line-height:1.55'>Welcome back — {' '.join(parts)}</div></div>")


def _wizard_loaded_note(status, store_read):
    """A Documents-step note naming the data already loaded, so the wizard does not look empty.

    An operator who ingested DNA/wearable/labs in a prior session should SEE that the app holds it —
    not a wall of empty "+ Link" cards. Reports names/counts only (never a raw reading value), from the
    live load-state + the genotype-reading count in the store. Empty string when nothing is loaded.
    """
    rows = store_read if isinstance(store_read, list) else []
    parts = []
    dna = status.get("dna", {}) if isinstance(status, dict) else {}
    genotype_ct = sum(1 for r in rows if isinstance(r, dict)
                      and _re.search(r"\brs\d|\bi\d{6}", str(r.get("item", ""))))
    if genotype_ct:
        parts.append(f"{genotype_ct} genotypes")
    elif dna.get("loaded"):
        parts.append("DNA")
    if status.get("wearable", {}).get("loaded") if isinstance(status, dict) else False:
        parts.append("wearable data")
    if status.get("labs", {}).get("loaded") if isinstance(status, dict) else False:
        parts.append("labs")
    if not parts:
        return ""
    return ("<div class='note' style='margin-bottom:11px'>"
            f"<b>✓ Already loaded:</b> {_esc(', '.join(parts))}. You don't need to re-add these — "
            "link any additional documents below, or manage them later in My Info.</div>")


def _wizard_doc_cards(status, store_read):
    """The Documents-step cards rendered load-state-aware: a class already in the store shows '✓ loaded'.

    The wizard's four document cards were STATIC '+ Link' markup that contradicted the 'Already loaded'
    note above them (a returning operator with 117 genotypes still saw every card as empty '+ Link').
    This renders them from the live load-state — wearable and DNA (by genotype count) and labs flip to
    '✓ loaded'; an unloaded class keeps the '+ Link' affordance the wizard uploader wires. Names/counts
    only, never a raw reading value (mirrors `_doc_cards`).
    """
    rows = store_read if isinstance(store_read, list) else []
    genotype_ct = sum(1 for r in rows if isinstance(r, dict)
                      and _re.search(r"\brs\d|\bi\d{6}", str(r.get("item", ""))))
    we = status.get("wearable", {}) if isinstance(status, dict) else {}
    labs = status.get("labs", {}) if isinstance(status, dict) else {}
    wearable = _doc_card(
        "wearable", "Wearable export",
        "Activity, sleep &amp; vitals — loaded" if we.get("loaded") else "Activity, sleep &amp; vitals — parsed locally",
        _LOADED if we.get("loaded") else _LINK)
    labs_card = _doc_card(
        "labs", "Labs &amp; bloodwork",
        _esc(", ".join(labs["files"])) if labs.get("files") else ("loaded" if labs.get("loaded") else "PDF or CSV of a recent panel"),
        _LOADED if labs.get("loaded") else _LINK)
    medical = _doc_card("medical", "Medical history", "Visit summaries, prior plans, records", _LINK)
    dna = _doc_card(
        "dna", "DNA",
        f"{genotype_ct} genotypes loaded" if genotype_ct else "23andMe or AncestryDNA raw export",
        _LOADED if genotype_ct else _LINK)
    return wearable + labs_card + medical + dna


def render(store_read=None, *, status=None, _today=None):
    """Return the inline-asset SPA shell HTML with the Upload doc-cards at the live load-state.

    The design is `app_view.html` (passes render.emit's off-file guard); three surfaces are
    injected: the four 'Link your documents' cards (`<!--DOC_CARDS-->`, rendered from `status`),
    the Plan-screen body (`<!--PLAN_ZONE-->`, the domains' recorded plans for today resolved from
    `store_read`, else the honest awaiting state), and the 'About you' demographic form pre-filled
    from the operator's latest saved readings (`_prefill_form`). No fabricated data — an empty
    store shows honest "+ Link" cards, the no-plan awaiting state, and a blank/default form.

    Args:
        store_read (list, optional): The store read model; drives the wearable card's
            load-state when `status` is not injected. None renders the empty state.
        status (dict, optional): The full ingestion load-state (wearable/dna/labs), injected
            by `generate.run('app')`. None falls back to a store-only default.
        _today (date, optional): The render date driving the Plan screen's plan-for-today
            resolution (`_plan_zone`); defaults to today's date.

    Returns:
        (str) The full self-contained SPA HTML document.
    """
    if store_read is None:
        store_read = []
    status = status if status is not None else _default_status(store_read)
    today = (_today or _datetime.date.today()).isoformat()
    html = (
        _VIEW.read_text(encoding="utf-8")
        .replace("<!--DOC_CARDS-->", _doc_cards(status))
        .replace("<!--PLAN_ZONE-->", _plan_zone(store_read, today))
        .replace("<!--REFERRAL_ZONE-->", _referral_zone(store_read))
        .replace("<!--SAVED_PROFILE-->", _wizard_prefill_script(store_read))
        .replace("<!--WIZARD_LOADED_NOTE-->", _wizard_loaded_note(status, store_read))
        .replace("<!--WELCOME_BACK-->", _welcome_back_banner(store_read))
        .replace("<!--WIZARD_DOC_CARDS-->", _wizard_doc_cards(status, store_read))
    )
    html = _prefill_form(html, store_read)
    if _intake_complete(store_read):
        return _mark_screen_active(html, "screen-team")
    return _lock_to_create_profile(html)
