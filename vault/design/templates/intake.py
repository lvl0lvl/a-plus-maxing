"""Intake wizard render — the 6-step "Build your plan" guided flow (ADR-0004 single-file).

`render(store_read)` produces the self-contained HTML intake wizard faithful to the
`Intake v2 — Guided` design (design/a+maxing_designs.pen, frame 2vFFC): a header, a
6-step left-rail stepper, and the six step panels stacked as a static flow shell — the
foundation the interactive ingest build wires step-by-step. Inlines all CSS + SVG; 0
external asset references (render.emit refuses otherwise).

Step 1 ("Your info & documents") is LIVE: its "Link your documents" cards read the real
load-state — the wearable stream from `store_read`, the DNA/labs dropzones from the
injected `status` (built by `generate.run('intake')` via `scripts.ingest.status.resolve`)
— so the operator sees what has landed and the exact command to load what has not. The
privacy line ("parsed locally — nothing is uploaded") is kept prominent (ADR-0001).

Steps 2 + 6 are faithful to the `khCNX` (Goals & priorities) / `BRAUE` (Review & generate)
mocks. Steps 3-5 (Training / Nutrition / Supplements & peptides) are a first-pass shell
composed from the established intake vocabulary, pending the ui-designer pass in the
interactive-ingest build.
"""

from scripts.ingest import status as ingest_status

# The intake mocks (2vFFC / khCNX / BRAUE) use a neutral gray palette + a blue accent
# (distinct from the dashboard's clin-* tokens). Held here so the render matches the mock.
_INK, _INK2, _INK3 = "#111827", "#4B5563", "#6B7280"
_CANVAS, _SHEET, _LINE, _LINE2 = "#F3F4F6", "#FFFFFF", "#E5E7EB", "#F1F2F4"
_BLUE, _BLUE_DEEP, _BLUE_SOFT = "#2563EB", "#1D4ED8", "#EFF2FE"
_GREEN, _GREEN_BG = "#059669", "#ECFDF5"
_FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
_MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

_STEPS = [
    "Your info & documents", "Goals & priorities", "Training",
    "Nutrition", "Supplements & peptides", "Review & generate",
]

# Inline line-icons (no external assets) keyed per document card.
_ICONS = {
    "labs": "<path d='M6 2h7l5 5v15a0 0 0 0 1 0 0H6z' fill='none' stroke='currentColor' stroke-width='1.6'/><path d='M13 2v5h5' fill='none' stroke='currentColor' stroke-width='1.6'/>",
    "medical": "<rect x='5' y='3' width='14' height='18' rx='2' fill='none' stroke='currentColor' stroke-width='1.6'/><path d='M9 8h6M9 12h6M9 16h4' stroke='currentColor' stroke-width='1.6'/>",
    "wearable": "<path d='M3 12h4l2 6 4-14 2 8h6' fill='none' stroke='currentColor' stroke-width='1.7' stroke-linejoin='round'/>",
    "dna": "<path d='M8 3c0 5 8 6 8 9s-8 4-8 9M16 3c0 5-8 6-8 9s8 4 8 9' fill='none' stroke='currentColor' stroke-width='1.6'/>",
}


def _style():
    return f"""<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: {_FONT}; background: {_CANVAS}; color: {_INK};
       -webkit-font-smoothing: antialiased; padding: 40px 20px; }}
.sheet {{ max-width: 1020px; margin: 0 auto; background: {_SHEET}; border: 1px solid {_LINE};
          border-radius: 12px; overflow: hidden; }}
.head {{ display: flex; justify-content: space-between; align-items: flex-start;
         padding: 26px 32px; border-bottom: 1px solid {_LINE}; }}
.brand {{ font-size: 17px; font-weight: 700; }}
.brand .sub {{ font-size: 13px; font-weight: 400; color: {_INK3}; margin-top: 2px; }}
.stepno {{ font-size: 13px; color: {_INK3}; }}
.cols {{ display: flex; }}
.rail {{ width: 232px; flex: none; padding: 28px 20px; border-right: 1px solid {_LINE}; }}
.rstep {{ display: flex; align-items: center; gap: 11px; padding: 9px 12px; border-radius: 9px;
          font-size: 13.5px; color: {_INK3}; }}
.rstep.active {{ background: {_BLUE_SOFT}; color: {_BLUE}; font-weight: 600; }}
.rnum {{ width: 26px; height: 26px; border-radius: 50%; flex: none; display: flex;
         align-items: center; justify-content: center; font-size: 12.5px; font-weight: 600;
         background: {_LINE}; color: {_INK3}; }}
.rstep.active .rnum {{ background: {_BLUE}; color: #fff; }}
.main {{ flex: 1; min-width: 0; }}
.panel {{ padding: 30px 36px; border-bottom: 1px solid {_LINE2}; }}
.panel:last-child {{ border-bottom: none; }}
.eyebrow {{ font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
            color: {_BLUE}; margin-bottom: 9px; }}
.ptitle {{ font-size: 21px; font-weight: 700; }}
.psub {{ font-size: 14px; color: {_INK2}; margin-top: 6px; line-height: 1.5; }}
.seclab {{ font-size: 12.5px; font-weight: 700; color: #374151; margin: 22px 0 10px; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px 24px; }}
.field label {{ display: block; font-size: 12.5px; font-weight: 600; color: #374151; margin-bottom: 6px; }}
.box {{ border: 1px solid {_LINE}; border-radius: 8px; padding: 10px 12px; font-size: 13.5px;
        color: {_INK}; background: {_SHEET}; min-height: 40px; display: flex; align-items: center;
        justify-content: space-between; }}
.box.ph {{ color: {_INK3}; }}
.docs {{ display: flex; flex-direction: column; gap: 12px; margin-top: 4px; }}
.doc {{ display: flex; align-items: center; gap: 14px; border: 1px solid {_LINE};
        border-radius: 10px; padding: 14px 16px; }}
.dicon {{ width: 26px; height: 26px; flex: none; color: {_INK3}; }}
.dmain {{ flex: 1; min-width: 0; }}
.dtitle {{ font-size: 14px; font-weight: 600; }}
.dsub {{ font-size: 12.5px; color: {_INK3}; margin-top: 2px; }}
.dsub code {{ font-family: {_MONO}; font-size: 12px; color: {_INK2}; background: {_LINE2};
             padding: 1px 6px; border-radius: 5px; }}
.dstate {{ font-size: 13px; font-weight: 600; flex: none; }}
.dstate.ok {{ color: {_GREEN}; }}
.dstate.no {{ color: {_BLUE}; }}
.note {{ font-size: 12.5px; color: {_INK3}; margin-top: 16px; display: flex; align-items: center; gap: 7px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.chip {{ font-size: 12.5px; padding: 6px 12px; border-radius: 999px; border: 1px solid {_LINE};
         color: {_INK2}; }}
.chip.on {{ background: {_BLUE_SOFT}; border-color: {_BLUE_SOFT}; color: {_BLUE}; font-weight: 600; }}
.chip.ok {{ background: {_GREEN_BG}; border-color: {_GREEN_BG}; color: {_GREEN}; font-weight: 600; }}
.rows {{ display: flex; flex-direction: column; gap: 8px; }}
.rev {{ border: 1px solid {_LINE}; border-radius: 10px; padding: 14px 16px; }}
.rev h4 {{ font-size: 13.5px; font-weight: 700; margin-bottom: 6px; }}
.rev p {{ font-size: 12.5px; color: {_INK2}; line-height: 1.55; }}
.foot {{ display: flex; justify-content: space-between; align-items: center; margin-top: 26px; }}
.btn {{ font-size: 13.5px; font-weight: 600; border-radius: 9px; padding: 11px 18px; cursor: default; }}
.btn.back {{ border: 1px solid {_LINE}; color: {_INK2}; background: {_SHEET}; }}
.btn.next {{ background: {_BLUE}; color: #fff; border: 1px solid {_BLUE_DEEP}; }}
</style>"""


def _rail():
    items = []
    for i, label in enumerate(_STEPS, start=1):
        active = " active" if i == 1 else ""
        items.append(f"<div class='rstep{active}'><span class='rnum'>{i}</span>{label}</div>")
    return f"<nav class='rail'>{''.join(items)}</nav>"


def _field(label, value, placeholder=False):
    cls = "box ph" if placeholder else "box"
    return f"<div class='field'><label>{label}</label><div class='{cls}'>{value}</div></div>"


def _doc(key, title, subtitle, state_text, ok):
    icon = f"<svg class='dicon' viewBox='0 0 24 24'>{_ICONS[key]}</svg>"
    state_cls = "ok" if ok else "no"
    state = f"<span class='dstate {state_cls}'>{state_text}</span>"
    return (f"<div class='doc'>{icon}<div class='dmain'>"
            f"<div class='dtitle'>{title}</div><div class='dsub'>{subtitle}</div></div>{state}</div>")


def _doc_cards(status):
    """The four 'Link your documents' cards, driven by the live load-state."""
    we = status["wearable"]
    if we.get("loaded"):
        sub = (f"{we['source']} · {we['count']} readings · {', '.join(we['items'])} · "
               f"{we['range'][0]} – {we['range'][1]}")
        wearable = _doc("wearable", "Wearable export (Apple Health)", sub, "✓ loaded", True)
    else:
        wearable = _doc("wearable", "Wearable export (Apple Health)",
                        "<code>python -m scripts.ingest export.xml</code>", "Not linked", False)

    dna = status["dna"]
    if dna.get("loaded"):
        dna_card = _doc("dna", "DNA (23andMe)", f"{dna['files'][0]} landed in vault/dna/raw/",
                        "✓ loaded", True)
    else:
        dna_card = _doc("dna", "DNA (23andMe)",
                        "<code>python -m scripts.ingest 23andme.zip</code>", "Not linked", False)

    labs = status["labs"]
    if labs.get("loaded"):
        labs_card = _doc("labs", "Labs & bloodwork", f"{', '.join(labs['files'])}", "✓ loaded", True)
    else:
        labs_card = _doc("labs", "Labs & bloodwork", "PDF or CSV → vault/labs/raw/", "+ Link", False)

    medical = _doc("medical", "Medical history", "PDF, document, or paste", "+ Link", False)
    return f"<div class='docs'>{wearable}{labs_card}{medical}{dna_card}</div>"


def _panel(num, title, subtitle, body, *, note=False):
    foot = ("<div class='foot'><span class='btn back'>Back</span>"
            f"<span class='btn next'>{'Next: ' + _STEPS[num] if num < 6 else 'Generate my plan'} →</span></div>")
    note_html = ("<div class='note'>\U0001F512 Parsed locally into your store — nothing is uploaded.</div>"
                 if note else "")
    return (f"<section class='panel'><div class='eyebrow'>Step {num} of 6</div>"
            f"<div class='ptitle'>{title}</div><div class='psub'>{subtitle}</div>"
            f"{body}{note_html}{foot}</section>")


def _chips(items, on=()):
    out = []
    for it in items:
        cls = "chip ok" if it in on else "chip"
        out.append(f"<span class='{cls}'>{it}</span>")
    return f"<div class='chips'>{''.join(out)}</div>"


def _step1(status):
    about = ("<div class='seclab'>About you</div><div class='grid2'>"
             + _field("Birth year", "—", True) + _field("Sex (for dosing)", "—", True)
             + _field("Bodyweight", "—", True) + _field("Equipment access", "—", True) + "</div>")
    docs = "<div class='seclab'>Link your documents</div>" + _doc_cards(status)
    return _panel(1, "Your info &amp; documents",
                  "Start with the basics, then link any documents you have — labs, history, "
                  "wearable exports. They’re parsed locally into your store.",
                  about + docs, note=True)


def _step2():
    body = ("<div class='seclab'>Goal areas</div>"
            + _chips(["Workout", "Nutrition", "Supplements", "Peptides"], on=["Workout", "Nutrition", "Supplements"])
            + "<div class='seclab'>Targets</div><div class='rows'>"
            + "<div class='box ph'>Add a target — e.g. “add 10 lb to squat by September”</div>"
            + "<div class='box ph'>Add a target — e.g. “bring resting heart rate under 50”</div></div>"
            + "<div class='seclab'>Priority order</div>"
            + _chips(["1 · Workout", "2 · Nutrition", "3 · Supplements"]))
    return _panel(2, "Goals &amp; priorities",
                  "What should the plan optimize for, and in what order?", body)


def _step3():
    body = ("<div class='grid2'>" + _field("Training experience", "—", True)
            + _field("Sessions per week", "—", True) + _field("Session length", "—", True)
            + _field("Preferred style / split", "—", True) + "</div>"
            + "<div class='seclab'>Current main lifts (optional)</div><div class='grid2'>"
            + _field("Squat", "—", True) + _field("Bench", "—", True)
            + _field("Deadlift", "—", True) + _field("Overhead press", "—", True) + "</div>"
            + "<div class='seclab'>Train around</div>"
            + _chips(["Lower-back caution", "Shoulder", "Knee", "+ add"]))
    return _panel(3, "Training",
                  "How you train now, so the workout plan meets you where you are.", body)


def _step4():
    body = ("<div class='grid2'>" + _field("Dietary pattern", "—", True)
            + _field("Meals per day", "—", True) + "</div>"
            + "<div class='seclab'>Allergies &amp; intolerances</div>"
            + _chips(["Dairy", "Gluten", "Shellfish", "Nuts", "+ add"])
            + "<div class='seclab'>Foods to avoid / preferences</div>"
            + "<div class='rows'><div class='box ph'>Add a preference — e.g. “no pork”, “high protein”</div></div>")
    return _panel(4, "Nutrition",
                  "Dietary pattern and constraints, so nutrition fits how you actually eat.", body)


def _step5():
    body = ("<div class='seclab'>Current supplement stack</div><div class='rows'>"
            + "<div class='box ph'>Add a supplement — name &amp; dose (e.g. “creatine monohydrate · 5 g”)</div>"
            + "<div class='box ph'>Add a supplement — name &amp; dose</div></div>"
            + "<div class='seclab'>Peptides (current or considered)</div><div class='rows'>"
            + "<div class='box ph'>Add a peptide — name &amp; dose</div></div>"
            + "<div class='seclab'>What are you hoping to address?</div>"
            + _chips(["Recovery", "Sleep", "Longevity", "Body composition", "+ add"]))
    return _panel(5, "Supplements &amp; peptides",
                  "Your current stack — so interactions are screened before anything is recommended.", body)


def _step6():
    body = ("<div class='rows'>"
            + "<div class='rev'><h4>Workout</h4><p>Generated from your inputs by the personal-trainer "
              "specialist. Every recommendation cites a source; coverage gaps are disclosed, not "
              "filled with a fabricated protocol.</p></div>"
            + "<div class='rev'><h4>Nutrition</h4><p>Targets and structure aligned to your goals + "
              "training load.</p></div>"
            + "<div class='rev'><h4>Supplements &amp; peptides</h4><p>Screened for additive-AE and "
              "Rx interactions; anything flagged routes to the medical-liaison gate.</p></div></div>"
            + "<div class='note'>Generated locally; only a de-identified summary reaches the model.</div>")
    return _panel(6, "Review &amp; generate",
                  "Review your inputs, then generate your plan. Nothing is final until you say so.", body)


def _default_status(store_read):
    """Standalone-render status: wearable from store_read; DNA/labs unknown without their roots."""
    return {"wearable": ingest_status._wearable(store_read),
            "dna": {"loaded": False, "files": []},
            "labs": {"loaded": False, "files": []}}


def render(store_read, *, status=None, _today=None):
    """Return the self-contained 6-step intake wizard HTML for the current load-state.

    Args:
        store_read (list): The store read model (reading dicts) — drives Step 1's wearable card.
        status (dict, optional): The full ingestion load-state from `ingest.status.resolve`
            (wearable + dna + labs), injected by `generate.run('intake')`. Defaults to a
            store-only status (DNA/labs shown as not-linked) so the template renders standalone.
        _today (date, optional): Accepted for render-engine seam parity; unused here.

    Returns:
        (str) The full HTML document.
    """
    status = status if status is not None else _default_status(store_read)
    head = ("<div class='head'><div class='brand'>A+ Maxing<div class='sub'>Build your plan</div></div>"
            "<div class='stepno'>6 steps</div></div>")
    body = (_step1(status) + _step2() + _step3() + _step4() + _step5() + _step6())
    return (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>A+ Maxing — Build your plan</title>{_style()}</head>"
            f"<body><div class='sheet'>{head}<div class='cols'>{_rail()}<div class='main'>{body}</div></div></div></body></html>")
