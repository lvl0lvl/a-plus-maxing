"""App shell render — the four-screen left-nav SPA served at GET / (ADR-0029-T1).

`render(store_read, *, status=None, _today=None)` produces the self-contained
four-screen SPA (`Dashboard` / `Upload Documents` / `Plan` / `Chat with Team`)
ported from the operator-approved `prototype/app.html` shell. Inlines all CSS + SVG;
0 external asset references (render.emit refuses otherwise) — the prototype's lucide
CDN `<script>` is removed (icons render as inline `<svg>`, OQ-2 extract-used-icons)
and its bare-path `<img src="images/body.png">` is removed with its readiness state.

The `Dashboard` / `Plan` / `Chat with Team` screens render HONEST awaiting states —
0 fabricated operator data (ADR-0009 D2): no WHOOP recovery rings, no demo plan, no
fabricated specialist activity. Every figure the dashboard will show comes from the
operator's own data once it lands; T3+ wires the live surfaces. The `Upload Documents`
screen's document-link cards read the real ingestion load-state (the `status` injected
by `generate.run('app')`, resolved by `scripts.ingest.status`): an empty store shows
honest "Not linked" cards; after an upload they reflect the landed readings/files. The
about-you fields + the additional-documents dropzone + the plan-building chat are the
served SHELL here — T3 wires the form/chat (this task stands up the served surface only).
"""

from html import escape as _esc

from scripts.ingest import status as ingest_status
from scripts.serve.capture import (
    BODYWEIGHT_BANDS,
    EQUIPMENT_ACCESS_CLASSES,
    SEX_OPTIONS,
)

# The four left-nav screens' inline `<svg>` icons (OQ-2: only the icons the shell uses,
# rendered inline so the SPA loads no icon CDN). Ported from prototype/app.html:272-275.
_NAV_ICONS = {
    "dashboard": "<svg class='ic' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'><rect x='3' y='3' width='7' height='9' rx='1.5'/><rect x='14' y='3' width='7' height='5' rx='1.5'/><rect x='14' y='12' width='7' height='9' rx='1.5'/><rect x='3' y='16' width='7' height='5' rx='1.5'/></svg>",
    "upload": "<svg class='ic' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'><path d='M12 16V4m0 0L8 8m4-4 4 4'/><path d='M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3'/></svg>",
    "plan": "<svg class='ic' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'><path d='M5 3h11l4 4v14a0 0 0 0 1 0 0H5z'/><path d='M9 12h6M9 16h6M9 8h2'/></svg>",
    "team": "<svg class='ic' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'><path d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'/></svg>",
}

# The document-card inline `<svg>` glyphs (ported from prototype/app.html:370-373).
_DOC_ICONS = {
    "wearable": "<path d='M3 12h4l2 6 4-14 2 8h6' fill='none' stroke='currentColor' stroke-width='1.7' stroke-linejoin='round'/>",
    "labs": "<path d='M6 2h7l5 5v15H6z' fill='none' stroke='currentColor' stroke-width='1.6'/><path d='M13 2v5h5' fill='none' stroke='currentColor' stroke-width='1.6'/>",
    "medical": "<rect x='5' y='3' width='14' height='18' rx='2' fill='none' stroke='currentColor' stroke-width='1.6'/><path d='M9 8h6M9 12h6M9 16h4' stroke='currentColor' stroke-width='1.6'/>",
    "dna": "<path d='M8 3c0 5 8 6 8 9s-8 4-8 9M16 3c0 5-8 6-8 9s8 4 8 9' fill='none' stroke='currentColor' stroke-width='1.6'/>",
}


def _style():
    """Return the inline `<style>` — the approved Clinical Light design (prototype:3-267)."""
    return """<style>
:root{
  --ink:#101426; --ink2:#5A6178; --muted:#5A6178; --faint:#9AA1B4;
  --bg:#F5F7FB; --sheet:#fff; --line:#E7EAF3; --line2:#EEF1F7; --ctrl:#8A9099;
  --accent:#4A55E8; --accent-deep:#2E37B0; --soft:#EEF0FE; --soft-bd:#D9DCFB;
  --good:#1FB5A6; --good-bg:#E8F7F4; --watch:#E8A23B; --watch-bg:#FBF1E0; --idle:#9AA1AB;
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
.app{display:grid;grid-template-columns:248px 1fr;min-height:100vh}

/* ---------- side nav ---------- */
.nav{background:var(--sheet);border-right:1px solid var(--line);padding:22px 14px;display:flex;flex-direction:column;gap:3px;position:sticky;top:0;height:100vh;overflow:auto}
.brand{padding:4px 10px 18px;font-size:16px;font-weight:800;letter-spacing:-.01em}
.brand small{display:block;font-size:12px;font-weight:400;color:var(--muted);margin-top:2px}
.navitem{display:flex;align-items:center;gap:11px;padding:10px 12px;border-radius:9px;font-size:14px;font-weight:600;color:var(--ink2);cursor:pointer;text-decoration:none;border:none;background:none;width:100%;text-align:left}
.navitem:hover{background:var(--line2)}
.navitem.active{background:var(--soft);color:var(--accent)}
.navitem .ic{width:18px;height:18px;flex:none;color:currentColor}

/* ---------- content ---------- */
.content{padding:34px 40px;overflow:auto;max-height:100vh}
.screen{display:none;max-width:1080px;margin:0 auto}
.screen.active{display:block}
.h1{font-size:24px;font-weight:800;letter-spacing:-.01em}
.sub{font-size:14px;color:var(--ink2);margin-top:6px;line-height:1.5}
.pagehead{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:26px}
.pill{font-size:12px;font-weight:600;border-radius:999px;padding:5px 12px}
.pill.muted{background:var(--line2);color:var(--muted)}
.pill.good{background:var(--good-bg);color:var(--good)}
.pill.watch{background:var(--watch-bg);color:var(--watch)}
.card{background:var(--sheet);border:1px solid var(--line);border-radius:12px;padding:18px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.seclab{font-size:13px;font-weight:700;color:#374151;margin:22px 0 11px}
.btn{font-size:13.5px;font-weight:600;border-radius:9px;padding:11px 18px;cursor:pointer;border:1px solid transparent}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent-deep)}
.btn.ghost{background:var(--sheet);color:var(--ink2);border-color:var(--line)}
.inp{width:100%;border:1px solid var(--ctrl);border-radius:8px;padding:10px 12px;font-size:13.5px;color:var(--ink);background:var(--sheet);font-family:var(--font)}
.inp:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(37,99,235,.3)}
select.inp{cursor:pointer}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.field label{display:block;font-size:12.5px;font-weight:600;color:#374151;margin-bottom:6px}

/* awaiting / empty states (consistent across Dashboard / Plan / Chat with Team) */
.await{border:1px dashed var(--line);border-radius:11px;padding:22px;background:#FBFCFE;margin-bottom:18px}
.await .at{font-size:15px;font-weight:700;color:var(--ink)}
.await .ad{font-size:13px;color:var(--ink2);margin-top:6px;line-height:1.5}

/* document-link cards (Upload Documents — driven by the live load-state) */
.doc{display:flex;align-items:center;gap:14px;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:11px}
.doc .ic{width:24px;height:24px;flex:none;color:var(--muted)}
.doc .m{flex:1;min-width:0}
.doc .t{font-size:14px;font-weight:600}
.doc .d{font-size:12.5px;color:var(--muted);margin-top:2px}
.doc .d code{font-family:var(--mono);font-size:12px;background:var(--line2);padding:1px 6px;border-radius:5px}
.doc .st{font-size:13px;font-weight:600;flex:none;display:flex;align-items:center;gap:7px}
.doc.done{border-color:#CDEAD9;background:#FCFFFD}
.doc.done .st{color:var(--good)}
.doc .link{color:var(--accent);cursor:pointer}
.drop{border:1.5px dashed var(--ctrl);border-radius:10px;padding:20px;text-align:center;color:var(--muted);font-size:13px;cursor:pointer}
.drop:hover{border-color:var(--accent);color:var(--accent);background:var(--soft)}

/* plan-building chat composer (Upload Documents — posts each turn to /chat) */
.turns{display:flex;flex-direction:column;gap:10px;margin-bottom:14px}
.turn{border:1px solid var(--line);border-radius:10px;padding:11px 14px;font-size:13.5px;line-height:1.5;white-space:pre-wrap}
.turn.me{background:var(--soft);border-color:var(--soft-bd)}
.turn.bot{background:var(--sheet)}
.composer{display:flex;gap:10px}
.composer .inp{flex:1}
.receipt{font-size:12px;color:var(--muted);margin:2px 0 12px;min-height:1px}
</style>"""


def _nav():
    """The left-nav shell: brand + the four screen buttons (inline `<svg>` icons)."""
    buttons = "".join(
        f"<button class='navitem' data-screen='{screen}'>{_NAV_ICONS[screen]}{label}</button>"
        for screen, label in (
            ("dashboard", "Dashboard"), ("upload", "Upload Documents"),
            ("plan", "Plan"), ("team", "Chat with Team"),
        )
    )
    return ("<nav class='nav'>"
            "<div class='brand'>A+ Maxing<small>Your health, planned</small></div>"
            f"{buttons}</nav>")


def _awaiting(screen, title, detail):
    """A consistent honest awaiting/empty state, tagged `data-awaiting=<screen>`.

    The same markup on every awaiting screen (Dashboard / Plan / Chat with Team) so the
    honest-data invariant reads as ONE state, not three ad-hoc strings (ADR-0009 D2).
    """
    return (f"<div class='await' data-awaiting='{screen}'>"
            f"<div class='at'>{title}</div><div class='ad'>{detail}</div></div>")


def _dashboard():
    head = ("<div class='pagehead'><div><div class='h1'>Dashboard</div>"
            "<div class='sub'>Your readiness, trends, calendar, and today's plan appear here "
            "once your data is loaded and your plan is generated. Every figure shown comes from "
            "your own data and cites its source — nothing here is filled with sample numbers.</div></div></div>")
    body = _awaiting("dashboard", "No data yet",
                     "Load your documents on the Upload Documents screen, then generate your "
                     "plan. Until then this stays empty — no estimated or example readings are shown.")
    return f"<section class='screen' id='screen-dashboard'>{head}{body}</section>"


def _doc_card(icon_key, title, sub, state_html, *, done=False):
    cls = "doc done" if done else "doc"
    return (f"<div class='{cls}'><svg class='ic' viewBox='0 0 24 24'>{_DOC_ICONS[icon_key]}</svg>"
            f"<div class='m'><div class='t'>{title}</div><div class='d'>{sub}</div></div>"
            f"<div class='st'>{state_html}</div></div>")


def _doc_cards(status):
    """The four 'Link your documents' cards, driven by the live load-state.

    Reads the same ingestion-status contract `scripts.ingest.status` resolves for the
    intake wizard — an empty store shows honest "Not linked" cards; a loaded stream
    shows the landed count/filename (counts-only, never a raw reading value or rsid).
    """
    we = status["wearable"]
    if we.get("loaded"):
        sub = (f"{_esc(we['source'])} · {we['count']} readings · {_esc(', '.join(we['items']))} · "
               f"{_esc(we['range'][0])} – {_esc(we['range'][1])}")
        wearable = _doc_card("wearable", "Wearable export (Apple Health)", sub, "✓ loaded", done=True)
    else:
        wearable = _doc_card("wearable", "Wearable export (Apple Health)",
                             "<code>python -m scripts.ingest export.xml</code>",
                             "<span class='link'>+ Link</span>")

    labs = status["labs"]
    if labs.get("loaded"):
        labs_card = _doc_card("labs", "Labs &amp; bloodwork", _esc(", ".join(labs["files"])),
                              "✓ loaded", done=True)
    else:
        labs_card = _doc_card("labs", "Labs &amp; bloodwork", "PDF or CSV → vault/labs/raw/",
                              "<span class='link'>+ Link</span>")

    medical = _doc_card("medical", "Medical history", "PDF, document, or paste",
                        "<span class='link'>+ Link</span>")

    dna = status["dna"]
    if dna.get("loaded"):
        dna_card = _doc_card("dna", "DNA (23andMe)", f"{_esc(dna['files'][0])} landed in vault/dna/raw/",
                             "✓ loaded", done=True)
    else:
        dna_card = _doc_card("dna", "DNA (23andMe)", "<code>python -m scripts.ingest 23andme.zip</code>",
                             "<span class='link'>+ Link</span>")
    return f"{wearable}{labs_card}{medical}{dna_card}"


# Step-1 demographic <select> option labels (display text only). The option VALUES are the
# capture gate constants (SEX_OPTIONS / BODYWEIGHT_BANDS / EQUIPMENT_ACCESS_CLASSES) so the
# markup and the server-side `_BOUNDED_ENUMS` gate cannot drift (AC-2). For `bodyweight-band`
# the value is the kg gate token (so `persist_capture` validates) while the label is the
# pounds range (so the operator reads pounds) — the raw lb is a DISPLAY LABEL, never POSTed.
_SEX_LABELS = {"male": "Male", "female": "Female"}
_EQUIPMENT_LABELS = {
    "full-home-gym": "Full home gym", "commercial-gym": "Commercial gym",
    "minimal-equipment": "Minimal equipment", "bodyweight-only": "Bodyweight only",
}
_BODYWEIGHT_LB_LABELS = {
    "under-60kg": "Under 132 lb", "60-70kg": "132–154 lb", "70-80kg": "154–176 lb",
    "80-90kg": "176–198 lb", "90-100kg": "198–220 lb", "over-100kg": "Over 220 lb",
}


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


def _about_fields():
    """The objective-only 'About you' demographic inputs — the four gate-bound capture name=.

    Birth year writes the named-excluded `date-of-birth` raw source the capture seam
    de-identifies into `training-age-band` (never the raw year in a token). Sex / bodyweight
    band / equipment access are bounded `<select>`s whose option VALUES are the capture gate
    constants (AC-2 no-drift); the bodyweight band is a coarse kg range, never raw kg/lb.
    """
    return ("<div class='seclab' style='margin-top:0'>About you</div><div class='grid2'>"
            + _text_field("Birth year", "date-of-birth", "e.g. 1986")
            + _select_field("Sex (for dosing)", "sex-for-dosing",
                            [("", "Select…")] + [(v, _SEX_LABELS[v]) for v in SEX_OPTIONS])
            + _select_field("Body weight range", "bodyweight-band",
                            [("", "Select a range…")] + [(b, _BODYWEIGHT_LB_LABELS[b]) for b in BODYWEIGHT_BANDS])
            + _select_field("Equipment access", "equipment-access-class",
                            [("", "Select…")] + [(v, _EQUIPMENT_LABELS[v]) for v in EQUIPMENT_ACCESS_CLASSES])
            + "</div>")


def _upload(status):
    head = ("<div class='pagehead'><div><div class='h1'>Upload Documents</div>"
            "<div class='sub'>Start with the basics, then link any documents you have — labs, "
            "history, wearable exports. They're parsed locally into your store; nothing is uploaded.</div></div></div>")
    docs = "<div class='seclab'>Link your documents</div>" + _doc_cards(status)
    additional = ("<div class='seclab'>Additional documents</div>"
                  "<div class='drop'>Drop any other files here, or click to browse — anything relevant "
                  "(prior plans, imaging reports, notes). Parsed locally into your store.</div>")
    submit = ("<div style='display:flex;justify-content:flex-end;margin-top:18px'>"
              "<button class='btn primary' type='submit'>Save your info →</button></div>")
    # The form is OBJECTIVE-ONLY (ADR-0018 form/chat split): the four demographic inputs +
    # the content-upload affordances POST (multipart) to the BUILT `/upload` capture seam.
    # The rich sections (goals/training/nutrition/supplements/peptides) are the chat surface
    # below — 0 rich-section form field here.
    form = ("<form method='post' action='/upload' enctype='multipart/form-data'>"
            f"{_about_fields()}{docs}{additional}{submit}</form>")
    card = f"<div class='card' style='margin-bottom:22px'>{form}</div>"
    return f"<section class='screen' id='screen-upload'>{head}{card}{_build_plan_chat()}</section>"


def _build_plan_chat():
    """The plan-building chat composer — the conversational surface that fetches POST `/chat`.

    The rich detail (goals/training/nutrition/supplements/peptides) is gathered here in
    conversation, not as form fields (the ADR-0018 split). Each turn POSTs to the BUILT
    `/chat` route (the inline JS in `_script`); the assistant reply mounts into the
    `#chat-turns` list and the per-turn `{store,scaffold,dropped}` receipt + degraded state
    render into `#chat-receipt`. Same-origin only — the one outbound class is the ADR-0016
    `/chat` turn.
    """
    intro = ("<div class='seclab' style='font-size:15px'>Build your plan</div>"
             "<div class='sub' style='margin:-4px 0 12px'>Talk it through with your Care Assistant — "
             "goals, training, nutrition, supplements, peptides. It captures the rich detail your "
             "documents can't.</div>")
    turns = "<div class='turns' id='chat-turns'></div>"
    receipt = "<div class='receipt' id='chat-receipt'></div>"
    composer = ("<div class='composer'>"
                "<input class='inp' id='chat-input' "
                "placeholder='Tell your Care Assistant about your goals…'>"
                "<button class='btn primary' type='button' id='chat-send'>Send →</button></div>")
    return f"{intro}<div class='card'>{turns}{receipt}{composer}</div>"


def _plan():
    head = ("<div class='pagehead'><div><div class='h1'>Plan</div>"
            "<div class='sub'>Your plan is generated from a de-identified summary, every "
            "recommendation cites a source, and nothing is final until you approve it.</div></div>"
            "<span class='pill watch'>Draft · not yet approved</span></div>")
    card = ("<div class='card' style='margin-bottom:18px;display:flex;align-items:center;"
            "justify-content:space-between;gap:16px'><div><div style='font-weight:700;font-size:15px'>"
            "No approved plan yet</div><div class='sub'>Once you've loaded your documents and talked "
            "through your goals, generate your plan here. When you approve it, this screen shows your "
            "approved plan.</div></div><button class='btn primary' style='flex:none'>Generate plan →</button></div>")
    awaiting = _awaiting("plan", "Specialist contributions appear on plan run",
                         "Each specialist's recommendations — attributed and evidence-graded — populate "
                         "here when you generate your plan. No specialist output is shown until then.")
    return f"<section class='screen' id='screen-plan'>{head}{card}{awaiting}</section>"


def _team():
    head = ("<div class='pagehead'><div><div class='h1'>Chat with Team</div>"
            "<div class='sub'>Talk to your Care Assistant, or pick any specialist to go deeper. "
            "Each one cites its sources and stays in its lane.</div></div></div>")
    awaiting = _awaiting("team", "Your care team chat opens once your plan is set up",
                         "Load your documents and build your plan, then talk to your Care Assistant "
                         "here and switch to any specialist. No conversation is shown until then.")
    return f"<section class='screen' id='screen-team'>{head}{awaiting}</section>"


def _script():
    """Inline JS: hash-routing across the four screens + the Upload chat composer.

    The chat composer POSTs each turn to the same-origin `/chat` route (the ONLY outbound
    class — the ADR-0016 one-turn lane), mounts the assistant reply into `#chat-turns`, and
    renders the per-turn `{reply, receipt, progress, degraded}` receipt + the fail-closed
    degraded state into `#chat-receipt`. All inline — 0 off-file `<script src>` (the
    `render.emit` inline-asset guard); 0 non-loopback fetch (the single-egress-class boundary).
    """
    return ("<script>"
            "function show(s){"
            "document.querySelectorAll('.screen').forEach(e=>e.classList.remove('active'));"
            "(document.getElementById('screen-'+s)||document.getElementById('screen-dashboard')).classList.add('active');"
            "document.querySelectorAll('.navitem').forEach(n=>n.classList.toggle('active',n.dataset.screen===s));"
            "document.querySelector('.content').scrollTop=0;}"
            "document.querySelectorAll('.navitem').forEach(n=>n.addEventListener('click',()=>location.hash=n.dataset.screen));"
            "window.addEventListener('hashchange',()=>show((location.hash||'#dashboard').slice(1)));"
            "show((location.hash||'#dashboard').slice(1));"
            # --- Upload chat composer: POST each turn to /chat, render reply + receipt ---
            "var conv=[];"
            "function addTurn(role,text){"
            "var t=document.createElement('div');"
            "t.className='turn '+(role==='user'?'me':'bot');"
            "t.textContent=text;"
            "document.getElementById('chat-turns').appendChild(t);}"
            "function renderReceipt(data){"
            "var el=document.getElementById('chat-receipt');"
            "if(data.degraded){el.textContent='The assistant is unavailable — your inputs are saved; "
            "continue with the form above.';return;}"
            "var parts=[];"
            "var w=(data.receipt&&data.receipt.store)?data.receipt.store.length:0;"
            "if(w){parts.push('Captured '+w+' detail(s) this turn.');}"
            "if(data.progress&&data.progress.intake_complete){parts.push('Intake complete.');}"
            "el.textContent=parts.join(' ');}"
            "var send=document.getElementById('chat-send'),input=document.getElementById('chat-input');"
            "if(send){send.addEventListener('click',function(){"
            "var text=input.value.trim();if(!text){return;}"
            "addTurn('user',text);input.value='';conv.push({role:'user',content:text});"
            "fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},"
            "body:JSON.stringify({turn:text,conversation:conv})})"
            ".then(function(res){return res.json();})"
            ".then(function(data){"
            "if(data.reply){addTurn('assistant',data.reply);conv.push({role:'assistant',content:data.reply});}"
            "renderReceipt(data);})"
            ".catch(function(){renderReceipt({degraded:true});});});}"
            "</script>")


def _default_status(store_read):
    """Standalone-render status: wearable from store_read; DNA/labs unknown without their roots."""
    return {"wearable": ingest_status.wearable_status(store_read),
            "dna": {"loaded": False, "files": []},
            "labs": {"loaded": False, "files": []}}


def render(store_read, *, status=None, _today=None):
    """Return the self-contained four-screen app-shell SPA HTML for the load-state.

    Args:
        store_read (list): The store read model (reading dicts) — drives the Upload
            screen's wearable card load-state.
        status (dict, optional): The full ingestion load-state from `ingest.status.resolve`
            (wearable + dna + labs), injected by `generate.run('app')`. Defaults to a
            store-only status (DNA/labs shown not-linked) so the template renders standalone.
        _today (date, optional): Accepted for render-engine seam parity; unused here.

    Returns:
        (str) The full HTML document (inline CSS + inline SVG, 0 external asset references).
    """
    status = status if status is not None else _default_status(store_read)
    content = _dashboard() + _upload(status) + _plan() + _team()
    return (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>A+ Maxing</title>{_style()}</head>"
            f"<body><div class='app'>{_nav()}<div class='content'>{content}</div></div>{_script()}</body></html>")
