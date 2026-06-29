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

from html import escape as _esc

from scripts.ingest import status as ingest_status
from scripts.serve.capture import (
    BODYWEIGHT_BANDS,
    EQUIPMENT_ACCESS_CLASSES,
    SEX_OPTIONS,
)

# The intake mocks (2vFFC / khCNX / BRAUE) use a neutral gray palette + a blue accent
# (distinct from the dashboard's clin-* tokens). Held here so the render matches the mock.
_INK, _INK2, _INK3 = "#111827", "#4B5563", "#6B7280"
_CANVAS, _SHEET, _LINE, _LINE2 = "#F3F4F6", "#FFFFFF", "#E5E7EB", "#F1F2F4"
# Control-boundary border (Wave-B FIX-F): #8A9099 on white is 3.22:1, clearing the WCAG
# 1.4.11 3:1 control-boundary bar (#E5E7EB on white is only 1.24:1). Used for the input/
# select/textarea resting border so a control's edge is perceivable.
_CTRL_BORDER = "#8A9099"
# Focus ring (Wave-B FIX-F): a visible on-theme blue ring for WCAG 2.4.7 / 1.4.11, since
# the resting->focus 1px border swap alone is not a sufficient focus indicator.
_FOCUS_RING = "rgba(37, 99, 235, 0.35)"  # the _BLUE accent at 35% — a 3px soft ring
_BLUE, _BLUE_DEEP, _BLUE_SOFT = "#2563EB", "#1D4ED8", "#EFF2FE"
_GREEN = "#059669"
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
.rows {{ display: flex; flex-direction: column; gap: 8px; }}
.rev {{ border: 1px solid {_LINE}; border-radius: 10px; padding: 14px 16px; }}
.rev h4 {{ font-size: 13.5px; font-weight: 700; margin-bottom: 6px; }}
.rev p {{ font-size: 12.5px; color: {_INK2}; line-height: 1.55; }}
.foot {{ display: flex; justify-content: space-between; align-items: center; margin-top: 26px; }}
.btn {{ font-size: 13.5px; font-weight: 600; border-radius: 9px; padding: 11px 18px; cursor: pointer; }}
.btn.back {{ border: 1px solid {_LINE}; color: {_INK2}; background: {_SHEET}; }}
.btn.next {{ background: {_BLUE}; color: #fff; border: 1px solid {_BLUE_DEEP}; }}
/* Interactive capture controls — the input/select/textarea control vocabulary (ADR-0014-T1). */
.inp, textarea.inp, select.inp {{ width: 100%; border: 1px solid {_CTRL_BORDER}; border-radius: 8px;
        padding: 10px 12px; font-size: 13.5px; color: {_INK}; background: {_SHEET};
        font-family: {_FONT}; }}
textarea.inp {{ min-height: 44px; resize: vertical; line-height: 1.45; }}
/* Focus: a visible blue ring (WCAG 2.4.7 / 1.4.11) — not the border swap alone. */
.inp:focus, textarea.inp:focus, select.inp:focus {{ outline: none; border-color: {_BLUE};
        box-shadow: 0 0 0 3px {_FOCUS_RING}; }}
.handoff {{ border: 1px solid {_BLUE_SOFT}; background: {_BLUE_SOFT}; border-radius: 10px;
        padding: 16px 18px; margin-top: 18px; }}
.handoff h4 {{ font-size: 13.5px; font-weight: 700; color: {_BLUE_DEEP}; margin-bottom: 6px; }}
.handoff p {{ font-size: 12.5px; color: {_INK2}; line-height: 1.55; }}
.handoff code {{ font-family: {_MONO}; font-size: 12px; color: {_BLUE_DEEP}; background: {_SHEET};
        padding: 1px 6px; border-radius: 5px; }}
</style>"""


def _rail():
    items = []
    for i, label in enumerate(_STEPS, start=1):
        active = " active" if i == 1 else ""
        items.append(f"<div class='rstep{active}'><span class='rnum'>{i}</span>{label}</div>")
    return f"<nav class='rail'>{''.join(items)}</nav>"


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
        # The values are store-derived, but escape on the way into HTML regardless — item/source
        # strings flow from adapter data, and the filename strings below flow from the operator's
        # own filesystem (a `<`/`&` in a name must not break or inject into the page).
        sub = (f"{_esc(we['source'])} · {we['count']} readings · {_esc(', '.join(we['items']))} · "
               f"{_esc(we['range'][0])} – {_esc(we['range'][1])}")
        wearable = _doc("wearable", "Wearable export (Apple Health)", sub, "✓ loaded", True)
    else:
        wearable = _doc("wearable", "Wearable export (Apple Health)",
                        "<code>python -m scripts.ingest export.xml</code>", "Not linked", False)

    dna = status["dna"]
    if dna.get("loaded"):
        # A dropzone 23andMe file names the file; an extracted genetics-report PDF (ADR-0031,
        # no dropzone file) names its genotype-reading count instead — never crash on files[0].
        detail = (f"{_esc(dna['files'][0])} landed in vault/dna/raw/" if dna.get("files")
                  else f"{dna.get('count', 0)} genotypes landed")
        dna_card = _doc("dna", "DNA (23andMe)", detail, "✓ loaded", True)
    else:
        dna_card = _doc("dna", "DNA (23andMe)",
                        "<code>python -m scripts.ingest 23andme.zip</code>", "Not linked", False)

    labs = status["labs"]
    if labs.get("loaded"):
        labs_card = _doc("labs", "Labs & bloodwork", _esc(", ".join(labs["files"])), "✓ loaded", True)
    else:
        labs_card = _doc("labs", "Labs & bloodwork", "PDF or CSV → vault/labs/raw/", "+ Link", False)

    medical = _doc("medical", "Medical history", "PDF, document, or paste", "+ Link", False)
    return f"<div class='docs'>{wearable}{labs_card}{medical}{dna_card}</div>"


def _panel(num, title, subtitle, body, *, note=False, submit=False):
    if submit:
        # The Step-6 submit: a real POST submit carrying `step=6` so the handler routes
        # the captured fields and re-renders the wizard's `/generate-plan` handoff state.
        foot = ("<div class='foot'><span class='btn back'>Back</span>"
                "<button class='btn next' type='submit' name='step' value='6'>"
                "Save &amp; open plan generation →</button></div>")
    else:
        foot = ("<div class='foot'><span class='btn back'>Back</span>"
                f"<span class='btn next'>Next: {_STEPS[num]} →</span></div>")
    note_html = ("<div class='note'>\U0001F512 Parsed locally into your store — nothing is uploaded.</div>"
                 if note else "")
    return (f"<section class='panel'><div class='eyebrow'>Step {num} of 6</div>"
            f"<div class='ptitle'>{title}</div><div class='psub'>{subtitle}</div>"
            f"{body}{note_html}{foot}</section>")


def _text_field(label, name, placeholder=""):
    """A labeled single-line text input bound to the capture field `name`."""
    return (f"<div class='field'><label for='{name}'>{label}</label>"
            f"<input class='inp' type='text' id='{name}' name='{name}' "
            f"placeholder='{_esc(placeholder)}'></div>")


def _select_field(label, name, options):
    """A labeled select bound to the capture field `name` (first option is the prompt)."""
    opts = "".join(f"<option value='{_esc(v)}'>{_esc(t)}</option>" for v, t in options)
    return (f"<div class='field'><label for='{name}'>{label}</label>"
            f"<select class='inp' id='{name}' name='{name}'>{opts}</select></div>")


# Step-1 demographic select option labels (display text only; the option VALUES are the
# capture gate constants — `SEX_OPTIONS`/`BODYWEIGHT_BANDS`/`EQUIPMENT_ACCESS_CLASSES` — so
# the markup and the server-side `_BOUNDED_ENUMS` gate cannot drift, AC-6). Mirrors the
# Wave-A RECOVERY_STATUS_BANDS option-label pattern.
_SEX_LABELS = {"male": "Male", "female": "Female"}
_EQUIPMENT_LABELS = {
    "full-home-gym": "Full home gym", "commercial-gym": "Commercial gym",
    "minimal-equipment": "Minimal equipment", "bodyweight-only": "Bodyweight only",
}


def _step1(status):
    # The four demographic placeholders are now REAL POSTing inputs (ADR-0018-T1). Birth
    # year writes the `date-of-birth` raw source the capture seam de-identifies into
    # `training-age-band` (never the raw year in the token). Sex / bodyweight band /
    # equipment access are bounded `<select>`s whose option VALUES are the capture gate
    # constants (AC-6 no-drift) — the bodyweight band is a coarse range, never raw kg.
    about = ("<div class='seclab'>About you</div><div class='grid2'>"
             + _text_field("Birth year", "date-of-birth", "e.g. 1986")
             + _select_field("Sex (for dosing)", "sex-for-dosing",
                             [("", "Select…")] + [(v, _SEX_LABELS[v]) for v in SEX_OPTIONS])
             + _select_field("Bodyweight band", "bodyweight-band",
                             [("", "Select a range…")] + [(b, b) for b in BODYWEIGHT_BANDS])
             + _select_field("Equipment access", "equipment-access-class",
                             [("", "Select…")] + [(v, _EQUIPMENT_LABELS[v]) for v in EQUIPMENT_ACCESS_CLASSES])
             + "</div>")
    docs = "<div class='seclab'>Link your documents</div>" + _doc_cards(status)
    return _panel(1, "Your info &amp; documents",
                  "Start with the basics, then link any documents you have — labs, history, "
                  "wearable exports. They’re parsed locally into your store.",
                  about + docs, note=True)


def _chat_panel(num, title, subtitle, blurb):
    """A rich-section panel whose detail is gathered in conversation, not a form field.

    ADR-0018-T1 makes the form OBJECTIVE-ONLY: the rich sections (goals, training,
    nutrition, supplements & peptides) are CHAT-only — gathered by the Wave-A
    conversational intake at the POST `/chat` route, not as form fields. Each rich-section
    panel keeps its stepper place but carries 0 capture `name=` inputs; its body is a thin
    affordance pointing the operator to the chat. Reuses the locked Clinical Light theme
    (`.handoff` panel) — no new design.
    """
    body = ("<div class='handoff'><h4>" + title + "</h4>"
            "<p>" + blurb + " This is gathered in conversation — open the chat to talk it "
            "through. Nothing here is a form field; the rich detail is captured by the "
            "intake conversation at <code>/chat</code>.</p></div>")
    return _panel(num, title, subtitle, body)


def _step2():
    return _chat_panel(2, "Goals &amp; priorities",
                       "What should the plan optimize for, and in what order?",
                       "Your goals, targets, priority order, and hard limits.")


def _step3():
    return _chat_panel(3, "Training",
                       "How you train now, so the workout plan meets you where you are.",
                       "Your training experience, schedule, style, and anything to train around.")


def _step4():
    return _chat_panel(4, "Nutrition",
                       "Dietary pattern and constraints, so nutrition fits how you actually eat.",
                       "Your dietary pattern, meal structure, allergies, and food preferences.")


def _step5():
    return _chat_panel(5, "Supplements &amp; peptides",
                       "Your current stack; interaction screening runs later, in plan generation.",
                       "Your current supplement and peptide stack, and medications to screen against.")


def _step6():
    # The HANDOFF state: a readiness summary + the instruction to run `/generate-plan`
    # (the agent path). The server performs 0 in-app generation; this step routes the
    # operator to the generate leg, never renders a plan.
    body = ("<div class='rows'>"
            + "<div class='rev'><h4>Workout</h4><p>Generated by the personal-trainer specialist when "
              "you run plan generation. Every recommendation cites a source; coverage gaps are "
              "disclosed, not filled with a fabricated protocol.</p></div>"
            + "<div class='rev'><h4>Nutrition</h4><p>Targets and structure aligned to your goals + "
              "training load.</p></div>"
            + "<div class='rev'><h4>Supplements &amp; peptides</h4><p>Screened for additive-AE and "
              "Rx interactions; anything flagged routes to the medical-liaison gate.</p></div></div>"
            + "<div class='handoff'><h4>Ready to generate your plan</h4>"
              "<p>Your inputs are saved locally. Plan generation runs as the next step — "
              "run <code>/generate-plan</code> to have the specialists build your plan from a "
              "de-identified summary. Nothing is generated in this app; nothing is final until "
              "you say so.</p></div>")
    return _panel(6, "Review &amp; generate",
                  "Review your inputs, then generate your plan. Nothing is final until you say so.",
                  body, submit=True)


def _default_status(store_read):
    """Standalone-render status: wearable from store_read; DNA/labs unknown without their roots."""
    return {"wearable": ingest_status.wearable_status(store_read),
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
    # The form is OBJECTIVE-ONLY (ADR-0018-T1): Step-1's activated demographic inputs +
    # the content-upload affordances are the ONLY capture fields it POSTs to `/upload`
    # (multipart, so `stage_uploads` parses them into `staged["fields"]`). Step-1 is now
    # INSIDE the form so its demographic inputs submit. The rich sections (Steps 2-5) are
    # CHAT-only `/chat` affordance panels (0 form fields). The Step-6 submit carries
    # `step=6` and routes the `/generate-plan` handoff re-render.
    capture_form = (
        "<form method='post' action='/upload' enctype='multipart/form-data'>"
        + _step1(status) + _step2() + _step3() + _step4() + _step5() + _step6()
        + "</form>"
    )
    body = capture_form
    return (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>A+ Maxing — Build your plan</title>{_style()}</head>"
            f"<body><div class='sheet'>{head}<div class='cols'>{_rail()}<div class='main'>{body}</div></div></div></body></html>")
