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

from scripts.ingest import status as ingest_status

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
    if not saved:
        return html  # nothing saved — honest blank/default form, no banner

    for name in _DEMOGRAPHIC_SELECTS:
        value = saved.get(name)
        if value is None:
            continue
        option = f"<option value='{_esc(value)}'>"
        html = html.replace(option, f"<option value='{_esc(value)}' selected>", 1)

    dob = saved.get(_DEMOGRAPHIC_DOB)
    if dob is not None:
        html = html.replace(
            "id='date-of-birth' name='date-of-birth'>",
            f"id='date-of-birth' name='date-of-birth' value='{_esc(dob)}'>",
            1,
        )

    weight = saved.get(_DEMOGRAPHIC_WEIGHT)
    if weight is not None:
        html = html.replace(
            "name='bodyweight-kg' placeholder=\"Weight\"",
            f"name='bodyweight-kg' value='{_esc(weight)}' placeholder=\"Weight\"",
            1,
        )

    banner = ("<div class='upload-status' data-prefill='saved'>"
              "<span style='color:var(--good);font-weight:600'>✓ Saved — edit to update</span></div>")
    return html.replace(
        "<form action='/upload' method='post'>",
        f"<form action='/upload' method='post'>{banner}",
        1,
    )


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
    )
    return _prefill_form(html, store_read)
