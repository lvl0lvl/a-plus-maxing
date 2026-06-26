---
scope: "ADR-0029: wire the operator-approved app.html SPA front-end to the already-built conversational-intake backend — the SPA becomes a tracked inline-asset render-view served at GET /, the live converse backend lands, the Upload Documents demographics+chat surface is wired to the built /upload + /chat seams, and the conversation→usable-plan slice is proven end-to-end"
adrs: [ADR-0029]
tier: 8
created: 2026-06-26
status: approved
---

# Spec: Unified Inline-Asset SPA Front-End — Realize the Intake Slice on the New Surface

## Component Overview

This spec implements ADR-0029 (Adopt the Single-File Inline-Asset SPA `app.html` as the V1 Operator Front-End, Superseding the Intake Wizard Presentation). It WIRES the operator-approved four-screen SPA (`prototype/app.html` — a persistent left-nav shell: `Dashboard` / `Upload Documents` / `Plan` / `Chat with Team`) to the already-built conversational-intake backend so the operator's REAL data can flow in through the new surface. The deliverable is the intake-first slice: the SPA becomes the GET `/` body of the existing loopback server, its off-file assets are vendored inline so `render.emit` will emit it, the live `converse` backend is implemented, and the `Upload Documents` surface (the ADR-0018 form/chat split realized as one screen) is wired to the built `/upload` capture seam and the built `/chat` egress seam. This realizes ADRs 0015-0019 on the new front-end; it does NOT re-decide them.

The backend contracts are DECIDED and largely BUILT — verified against the live tree (`main` at `b43a30c` as of 2026-06-26): the `/chat` route + `chat.dispatch_turn` per-turn dispatch (`server.py:126-252`, `chat.py` [VERIFIED]), the gate-enforced extractor (`extract.py` `extract_facts`/`persist_extraction` [VERIFIED]), the question strategy with store-grounded `domain_done` + CONCERN-1 record-only domains (`chat.plan_next_turn` [VERIFIED]), the demographic capture routing (`capture.py` — `sex-for-dosing`/`bodyweight-band`/`equipment-access-class` ∈ `WIRED_TOKENS`, the birth-year → `date-of-birth` named-excluded source, the `_BOUNDED_ENUMS` for the demographic selects [VERIFIED]), the closed `SUMMARY_FIELD_SET` already extended with the ADR-0019 chat tokens (`dietary-pattern-class`/`supplement-stack-class`/`peptide-use-class`/`training-volume-band`) and the `equipment-access-class` reconciliation already applied (`router.py:18-46,107-115,468-492` [VERIFIED]), and the live `deidentify` no-train call (`client.py:213+` [VERIFIED]). The intake wizard `vault/design/templates/intake.py` has its demographic form ACTIVATED and its rich sections are chat-affordance panels (ADR-0018-T1 was built ON the wizard surface, `intake.py` [VERIFIED]). What this spec adds is the FRONT-END PIVOT — the same already-built backend, realized on the SPA instead of the wizard — plus the one remaining backend gap (live `converse`) and the one absent integration proof (the conversation→usable-plan E2E).

Three premises the source brief carried as open are STALE against the live tree and are reconciled here (Repo-Grounding Ledger): (a) the "four orphan tokens" are no longer orphaned at the capture level — `capture.py` wires all four and the wizard form is activated; the orphan-ness is now ONLY on the SPA surface (`app.html`'s `About you` inputs carry 0 `name=`/POST, `prototype/app.html:362-366` [VERIFIED]), so the demographic work in this spec is the SPA FORM MARKUP retargeted onto the new surface, NOT re-building the capture seam; (b) the ADR-0019 chat-token extension (the brief's candidate T6) is ALREADY BUILT (the four tokens are minted, derived, and tripwire-green in `router.py` [VERIFIED]), so no token-minting task exists here; (c) the headline conversation→usable-plan E2E (`tests/plan/test_conversation_to_plan_e2e.py`) was never written (`test ! -f` returns 0 [VERIFIED]) — this spec creates it.

Upstream, the spec depends on the built loopback transport (ADR-0013), the capture/persist routing (ADR-0014), the `/chat` egress (ADR-0016), the de-identifying extractor (ADR-0017), and the de-identified `SUMMARY_FIELD_SET` (ADR-0019) — all consumed unchanged. Downstream, the served SPA becomes the standing front-end surface: the `Dashboard`/`Plan`/`Chat-with-Team` screens stay honest awaiting-states (ADR-0009 D2) until their own per-surface live-wiring lands (OQ-3, future), and the operator-present LIVE run (real key + real data + spend) is the operator-gated checkpoint AFTER this build (out of scope here). The headline capability — a real-or-fixture conversation producing a usable plan through the SPA-served path — is exercisable against MOCKS/fixtures with no live API; the LIVE converse implemented in T2 is exercised only at that operator checkpoint, never in CI.

**The crown-jewel PII boundary (NFR-1, load-bearing).** This spec changes nothing about where data crosses the de-identification boundary. The served SPA's only outbound calls are the same-origin loopback `/upload` (local capture) and the one ADR-0016 `/chat` turn (the live conversation raw, on the no-train lane); it introduces 0 new outbound class. Every persisted fact stays de-identified through the unchanged extractor + `capture` gate + `summarize` (ADR-0017). The de-id-IN boundary (`deid_in`, `client.deidentify`) and the inner plan engine (`scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py`) are byte-frozen — no task in this spec edits them (a wave-checkpoint `git diff --numstat = 0` proof, NFR-4). The served front-end carries 0 off-file asset references — the AUTHORITATIVE check is a `render.emit` run that RETURNS a path rather than RAISING (a substring grep is non-authoritative — it misses a bare-path `src`; render.py:46-53 [VERIFIED]).

### Token / Field Map (BUILT — reused unchanged; the SPA form is the missing producer)

Every token below is verified ∈ the live `SUMMARY_FIELD_SET` (`router.py:18-46` [VERIFIED]) and its capture/derivation path is BUILT. This spec's T3 supplies the SPA-surface PRODUCER (the form `name=` markup) for the demographic tokens; it adds NO new token, derivation, or gate.

| Intake surface | Captured input | Class | Persistence target (BUILT) | Consumer |
|----------------|----------------|-------|----------------------------|----------|
| SPA `Upload Documents` form — birth year | a year (`<input name=date-of-birth>`) | wired derived (`training-age-band` ← `date-of-birth` via `_age_band`, `router.py:111` [VERIFIED]) | `store.append("date-of-birth", …)` (named-excluded raw source) → `summarize` derives the band | `summarize` → `assemble` |
| SPA `Upload Documents` form — sex | bounded `<select name=sex-for-dosing>` | wired pass-through (∈ `WIRED_TOKENS`, `capture.py:61` [VERIFIED]) | `store.append("sex-for-dosing", source:"intake")` | `summarize` → `assemble` |
| SPA `Upload Documents` form — body weight range (kg-token `value=`, pounds label) | bounded `<select name=bodyweight-band>` (`value=` is the kg band token; the DISPLAY label is the pounds range) | wired pass-through band (∈ `WIRED_TOKENS`, `capture.py:62`; `_BOUNDED_ENUMS` `BODYWEIGHT_BANDS`, `capture.py:118,124` [VERIFIED]) | `store.append("bodyweight-band", …)` (de-identified kg band token, never raw lb) | `summarize` → `assemble` |
| SPA `Upload Documents` form — equipment access | bounded `<select name=equipment-access-class>` | wired pass-through (RECONCILED — postal derivation removed, `router.py:107-115,468-469` [VERIFIED]) | `store.append("equipment-access-class", …)` | `summarize` → `assemble` |
| SPA `Upload Documents` form — link documents | DNA / HealthKit / labs file | (unchanged) | `route.route_upload` → `ingest.run`/`dna.land` (byte-unchanged) | ingest seam |
| SPA `Upload Documents` chat — goals/training/nutrition/supplements/peptides | conversational turns | wired de-identified (existing `WIRED_TOKENS` + the ADR-0019 `_ALWAYS_SET_DERIVED` chat bands, `router.py:488-492` [VERIFIED]) | `client.converse` → `extract_facts` → `persist_capture` → store, `source:"intake"` | `summarize` → `assemble` |

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0029 OQ-1 | Open Question | Once the wizard presentation is superseded, is `intake.py` deleted or kept as a fallback? | **Defer** | Deleting vs retaining the superseded wizard module is a cleanup decision orthogonal to getting real data flowing. This spec supersedes `intake.py` as the SERVED front-end (T1 re-points GET `/`); the module stays on disk unused (the `intake` template stays registered and its module tests stay green). Deletion/fallback is a follow-up, out of THIS spec's scope. |
| ADR-0029 OQ-2 | Open Question | lucide vendoring mechanism — full UMD bundle inline vs extract only the used icons as inline SVG? | **Proceed (assumption)** | A build-stage choice inside T1. T1 picks extract-used-icons-as-inline-SVG (preferred — `app.html` already renders the nav/screen icons as inline `<svg>`, so only the `data-lucide` set + the CDN `<script>` need vendoring); full-bundle is acceptable only if under ADR-0004's <500KB budget. Either yields 0 off-file references. Documented as a T1 assumption. |
| ADR-0029 OQ-3 | Open Question | The as-built Dashboard/Plan screens render fabricated demo data — what does each screen render until its own live-wiring lands? | **Proceed (constraint)** | This build wires ONLY `Upload Documents`. The `Dashboard`/`Plan`/`Chat-with-Team` screens MUST render honest awaiting-states (ADR-0009 D2), NEVER fabricated demo data presented as the operator's data — an in-scope T1 acceptance criterion. The FULL per-surface live-wiring (real `dashboard.py`/plan output, the specialist-chat backend) is future work, out of THIS spec's scope; the honest-placeholder requirement is IN scope and enforced. |
| Live-tree finding (ADR-0018) | Stale premise | The brief's "four orphan tokens" — the demographic CAPTURE seam is already built (`capture.py` routes all four; the wizard form is activated). | **Proceed (reconciled)** | The orphan-ness is now ONLY on the SPA surface (`app.html`'s `About you` inputs carry 0 `name=`/POST). T3 retargets the FORM MARKUP onto the SPA and reuses the built capture seam unchanged — it does NOT rebuild capture. Recorded in the Repo-Grounding Ledger (T3). |
| Live-tree finding (ADR-0019) | Stale premise | The brief's candidate T6 (extend `SUMMARY_FIELD_SET` with chat tokens) is already built. | **Defer (already satisfied)** | The four chat tokens are minted, derived (`_dietary_pattern_class` etc.), and tripwire-green in `router.py` [VERIFIED]. No token-minting task exists in this spec; T5's E2E personalizes from the already-minted tokens. Recorded in the Repo-Grounding Ledger (T5). |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `vault/design/templates/app_shell.py` | Create | The operator-approved SPA as a TRACKED render-view module exposing `render(store_read, *, status=None, _today=None)` → the self-contained four-screen left-nav SPA HTML. All assets inline (the used lucide icons as inline SVG per OQ-2; the bare-path `images/body.png` removed). The `Dashboard`/`Plan`/`Chat-with-Team` screens render honest awaiting-states (ADR-0009 D2), 0 fabricated demo data. T3 then wires the `Upload Documents` form/chat into the same module. |
| `scripts/generate/generate.py` | Modify | Register the SPA module in `_TEMPLATES` (`generate.py:27` [VERIFIED]) under `"app"`; extend the `intake`-keyed ingestion-status injection branch (`generate.py:74-90` [VERIFIED]) so the `"app"` view's `Upload Documents` screen renders the same real `ingest.status.resolve` load-state. |
| `scripts/serve/server.py` | Modify | Re-point `_render_intake` (the GET `/` + POST re-render body source, `server.py:70-81` [VERIFIED]) from `generate.run("intake")` → `generate.run("app")`; `_LOOPBACK="127.0.0.1"` (`server.py:29`) and the route table {GET `/`, POST `/upload`, POST `/chat`} byte-unchanged. |
| `scripts/model/client.py` | Modify | Implement `_ClaudeNoTrainBackend.converse(messages)` (today a `NotImplementedError` stub, `client.py:201-206` [VERIFIED]) as the live no-train API call MIRRORING the implemented `deidentify` (`client.py:213+`): same `_client()` (lazy `anthropic` + runtime `key_source.resolve`), bounded retry-with-timeout, fail-closed `ModelCallError` (constant message, `from None`). `deidentify`/`author`/the public `ModelClient` wrappers UNCHANGED. |
| `tests/serve/test_app_shell.py` | Create | T1: the inline-asset `render.emit` probe (returns a path, not a raise) + the render.emit-RAISES negative probe; the honest-data enumeration (Dashboard/Plan/Team); the GET `/` re-point. T3 extends: the SPA demographic form `name=`/`/upload` wiring + the chat composer `/chat` wiring + the honest ingestion-state. |
| `tests/serve/test_server.py` | Modify | T1: re-point all 19 `WIZARD_TITLE` assertion sites (the constant is DEFINED once at `test_server.py:34` and asserted at 19 sites — `:189,313,347,371,398,406,424,440,459,487,519,544,632,664,716,745,781,822,852` [VERIFIED]). The SPA `<title>` is `A+ Maxing` (`prototype/app.html:2` [VERIFIED]), NOT the wizard's `A+ Maxing — Build your plan`, so EVERY one of the 19 breaks under the re-point: the generic POST-re-render thread-survival assertions re-point to a SPA served-body marker, but the wizard-PRESENTATION-specific re-render tests (the Step-6 `/generate-plan` handoff `test_post_step6_is_a_generate_plan_handoff_not_in_app_generation:833` + the capture-field re-render assertions in `test_post_capture_*:781,822`) are REWRITTEN to the SPA's behavior or RETIRED, never marker-swapped — no tautological test left asserting the dead-as-served wizard (BACKWARD-COMPAT). |
| `tests/model/test_client.py` | Modify | T2: the live-converse mock tests (the contracted `{"reply","extraction"}` shape via a fixture SDK client; fail-closed typed raise with 0 raw-turn/key leak; runtime key; 0 live spend; scoped-change proof). |
| `tests/serve/test_intake_elicitation.py` | Create | T4: the SPA-surface not-naive elicitation proof — a fresh operator is asked the gaps; the `not-discussed`/`none`/`moderate` sentinels are a GAP, never vacuous `domain_done`/`intake_complete` (PF-S87-01); failing-capable negative control. |
| `tests/plan/test_conversation_to_plan_e2e.py` | Create | T5: the headline conversation→usable-plan E2E (composing ADR-0017-T2) — a fixture conversation through the served `/chat` → a USABLE recorded plan (`recorded == True` + content-traceability), NOT the honest no-plan state; mock-tested; the live variant operator-gated. |

## Tasks

### ADR-0029-T1: Port `app.html` into a Tracked Inline-Asset Render-View + Re-point GET `/` + Honest Awaiting-States

**Status:** TODO
**ADR Source:** ADR-0029, Decision (adopt the SPA, served as the GET `/` body, lucide + every asset vendored inline, superseding the wizard presentation); ADR-0029, Consequences Negative-1 (every off-file reference must be inlined before serving) + Neutral (GET `/` body source re-point; Dashboard/Plan stay visibly-placeholder); ADR-0029, Validation Approach (Inline-asset: a `render.emit` run RETURNS a written path rather than raising — the AUTHORITATIVE check; Loopback transport: GET `/` body is the SPA, bind unchanged); OQ-2 (lucide vendoring), OQ-3 (honest awaiting-states)
**Files to create/modify:**
- `vault/design/templates/app_shell.py` -- Create: the SPA render-view module (inline assets; honest awaiting-states for Dashboard/Plan/Team)
- `scripts/generate/generate.py` -- Modify: register `"app"` in `_TEMPLATES`; extend the ingestion-status injection to the `"app"` view
- `scripts/serve/server.py` -- Modify: re-point `_render_intake` → `generate.run("app")`; bind + route table unchanged
- `tests/serve/test_app_shell.py` -- Create
- `tests/serve/test_server.py` -- Modify: re-point the served-body assertions

**Acceptance Criteria:**
1. AUTHORITATIVE inline-asset: `generate.run("app")` (driving `render.emit` over `app_shell.render`) RETURNS a written `Path` that exists and does NOT raise `ValueError` — the served SPA carries 0 asset references `_is_external` flags (`render.py:46-53,113` [VERIFIED]) — verified by a test asserting the returned path exists; a substring grep is NOT substituted for this run.
2. Inline-asset NEGATIVE probe (failing-capable, checkpoint AC): re-introducing ONE off-file reference into the assembled SPA (e.g. a `<script src="https://unpkg.com/...">` or a bare-path `<img src="x.png">`) makes `render.emit` RAISE `ValueError` and write nothing — verified by a test that injects an off-file ref and asserts the raise (proving the gate is the real `render.emit` probe, not a grep).
3. lucide vendored inline (OQ-2): the served SPA loads NO `unpkg.com`/CDN lucide `<script>` (the `prototype/app.html:411` [VERIFIED] CDN load is gone) and renders its icons as inline `<svg>` — verified by `rg 'unpkg|lucide@|<script[^>]*src="http'` over the rendered SPA returning 0.
4. body.png removed/inlined: the bare-path `<img src="images/body.png">` (`prototype/app.html:292` [VERIFIED]) is NOT in the served SPA (removed with the Readiness awaiting-state, or inlined as a `data:` URI) — verified by `rg 'images/body.png'` over the rendered SPA returning 0.
5. HONEST-DATA (OQ-3 / ADR-0009 D2): the served `Dashboard`, `Plan`, and `Chat with Team` screens present 0 fabricated operator data — verified by enumerating the rendered screens and asserting the fabricated set is ABSENT (no "Synced from WHOOP", the `84`% RECOVERY ring, `7.8` SLEEP, `68 ms`/`49 bpm`/`183 lb`, `2,650 kcal`, `BPC-157 · 250mcg`, "Upper Push — Hypertrophy" presented as the operator's readings/plan; `prototype/app.html:290,295-296,300-301,323-325,342-345` [VERIFIED]); each renders an awaiting/empty state.
6. RE-POINT (loopback transport): GET `/` on the loopback server returns HTTP 200 + the SPA body (the four-screen nav shell {Dashboard, Upload Documents, Plan, Chat with Team}), NOT the wizard — verified by a served-handler test asserting the GET `/` body carries the SPA nav markers and not the wizard `<title>`; `_LOOPBACK="127.0.0.1"` (`server.py:29` [VERIFIED]) byte-unchanged and the route table is {GET `/`, POST `/upload`, POST `/chat`} (0 new bind/port).
7. BACKWARD-COMPAT (no tautological dead-wizard test): `tests/serve/test_server.py`'s 19 `WIZARD_TITLE` assertion sites are resolved against the SPA in TWO classes — (a) the generic POST-re-render thread-survival assertions are re-pointed to a SPA served-body marker (the SPA `<title>A+ Maxing` / the nav-shell markers, `prototype/app.html:2` [VERIFIED], NOT the wizard `A+ Maxing — Build your plan`); (b) the wizard-PRESENTATION-specific re-render tests — the Step-6 `/generate-plan` handoff `test_post_step6_is_a_generate_plan_handoff_not_in_app_generation` (`test_server.py:833`, which POSTs `step:"6"`, a wizard-only submit the SPA does not have) and the capture-field re-render assertions in `test_post_capture_*` (`test_server.py:781,822`) — are REWRITTEN to the SPA's actual capture behavior or RETIRED, NEVER given a marker swap (a marker-swapped dead-wizard test is the tautological test this criterion forbids). The intake-wizard MODULE tests (`tests/generate/test_intake.py`) stay green (intake.py retained, OQ-1) — verified by `rg -c "WIZARD_TITLE" tests/serve/test_server.py` returning 0 (constant + every assertion removed or re-pointed), the named Step-6/capture-re-render tests REMOVED or asserting SPA behavior (no `step:"6"`/`WIZARD_TITLE` body assertion), AND `.venv/bin/python -m pytest tests/serve/test_server.py tests/generate/test_intake.py` green.
8. `.venv/bin/python -m pytest tests/serve/test_app_shell.py tests/serve/test_server.py` passes.

**Risk Mitigations:** ADR-0029 Negative-1 (off-file references block serving) — crit 1,2,3,4 (the `render.emit` probe + negative probe). ADR-0029 Neutral + OQ-3 + the ADR-0009 D1/D2 collision (fabricated demo presented as data) — crit 5 (honest awaiting-states). ADR-0029 Neutral (body-source re-point) + ADR-0013 transport posture — crit 6 (loopback/route unchanged). BACKWARD-COMPAT (no tautological dead-wizard test) — crit 7.
**Dependencies:** None (entry point).

---

### ADR-0029-T2: Implement the Live `converse` Backend (Mirror the Live `deidentify`; Fail-Closed; Runtime Key; Mock-Tested)

**Status:** TODO
**ADR Source:** ADR-0029, Decision (the SPA's `Chat with Team`/intake surface relies on ADR-0016's one-turn `/chat` egress; the backend it consumes is unchanged) + ADR-0029 depends-on ADR-0016 (the `/chat` one-turn egress as the only outbound class); ADR-0016, Decision (the live intake conversation may egress raw to the no-train lane); ADR-0015 fail-closed (a failed model call never fabricates a turn); MEMORY (no operator PII / API key in tracked text — PUBLIC repo)
**Files to create/modify:**
- `scripts/model/client.py` -- Modify: implement `_ClaudeNoTrainBackend.converse(messages)` mirroring `deidentify`
- `tests/model/test_client.py` -- Modify: the live-converse mock tests

**Acceptance Criteria:**
1. `_ClaudeNoTrainBackend.converse(messages)` is implemented (the `NotImplementedError` raise at `client.py:201-206` [VERIFIED] is gone) and returns `{"reply": str, "extraction": list}` — verified by a test with a FIXTURE/MOCK SDK client (injected, no live API) asserting the contracted shape passes the public `ModelClient.converse` validation (`client.py:46-58` [VERIFIED]).
2. Runtime key, never a tracked file: `converse` resolves the API key at call time via `key_source.resolve()` inside `_client()` (the same path `deidentify` uses, `client.py:194-199` [VERIFIED]); NO tracked file holds the key — verified by a grep test asserting 0 API-key literal in the tracked tree AND that `converse` reads the key only through `key_source.resolve` (no tracked-file read).
3. Fail-closed (SEC-01): a failed / empty / errored / timed-out live converse raises `ModelCallError` with a CONSTANT message + `from None` (the `deidentify` pattern, `client.py:213+` [VERIFIED]) — never interpolating the SDK exception (which can carry the raw turn or the resolved key) — verified by injecting each failure mode into the mock SDK client and asserting the typed raise with 0 raw-turn/key substring in the message.
4. Mock-tested, 0 live spend: the converse tests inject a backend/SDK-client fixture at the seam; the live `_ClaudeNoTrainBackend.converse` SDK call is NEVER exercised in CI (mirroring `deidentify`'s "never exercised in tests", `client.py:186-189` [VERIFIED]) — verified by the test suite passing under `.venv/bin/python -m pytest` with no network and no key.
5. Scoped change: `git diff scripts/model/client.py` shows the ONLY changed method body is `_ClaudeNoTrainBackend.converse`; `deidentify`, `author`, every `ModelClient.*` wrapper, and `_client` are byte-unchanged — verified by the diff touching only the converse method.
6. `.venv/bin/python -m pytest tests/model/test_client.py` passes.

**Risk Mitigations:** Public-repo key/PII leak (MEMORY) — crit 2,3 (runtime key, constant fail-closed message, no key/turn leak). ADR-0029 PII-boundary-unchanged (no new outbound class) — crit 5 (converse joins the existing no-train lane, adds no class). ADR-0015 fail-closed (no fabricated turn) — crit 3.
**Dependencies:** None (entry point).

---

### ADR-0029-T3: Wire the SPA `Upload Documents` Surface — Demographic Form → `/upload` + Chat Composer → `/chat` + Honest Ingestion-State

**Status:** TODO
**ADR Source:** ADR-0029, Decision (`Upload Documents` realizing the form/chat split is the first surface wired) + ADR-0029 depends-on ADR-0018 (the screen realizes the form/chat split), ADR-0014 (the capture/persist routing consumed unchanged), ADR-0016 (the one-turn `/chat`); ADR-0029, Validation Approach (Split preserved: the served SPA contains BOTH an objective demographics+uploads form AND a conversational surface); OQ-3 (the `Upload Documents` ingestion-state is honest)
**Files to create/modify:**
- `vault/design/templates/app_shell.py` -- Modify (created by T1): give the demographic inputs real `name=` + a `/upload` form; wire the `Upload Documents` chat composer to `/chat`; render the real ingestion-state
- `tests/serve/test_app_shell.py` -- Modify (created by T1): the SPA form/chat wiring assertions

**Acceptance Criteria:**
1. The SPA `Upload Documents` "About you" form POSTs EXACTLY the four demographic `name=` fields — `date-of-birth`, `sex-for-dosing`, `bodyweight-band`, `equipment-access-class` — to the loopback `/upload` route (the built capture seam) — verified by a test parsing the rendered SPA's form asserting the four `name=` attributes target `action="/upload"` (against today's `app.html` demographic inputs carrying 0 `name=`, `prototype/app.html:362-366` [VERIFIED]).
2. The demographic `<select>` `<option value=...>` tokens are BUILT FROM the capture gate's enum constants (`SEX_OPTIONS`/`BODYWEIGHT_BANDS`/`EQUIPMENT_ACCESS_CLASSES`, `capture.py:117-119`; lowercased into `_BOUNDED_ENUMS` at `:123-125` [VERIFIED]) — 0 hardcoded `value=` list that is not the gate constant (no markup↔gate drift). For `bodyweight-band` the `value=` is the kg gate token (so capture still validates) and the DISPLAY LABEL is the pounds range (so the operator reads pounds): the select is EXACTLY the 6-band 1:1 map `under-60kg`→"Under 132 lb", `60-70kg`→"132–154 lb", `70-80kg`→"154–176 lb", `80-90kg`→"176–198 lb", `90-100kg`→"198–220 lb", `over-100kg`→"Over 220 lb" (kg→lb at 2.2046, rounded to the band boundary) — 6 options, NOT the prototype's 7 pound-ranges (`prototype/app.html:365` [VERIFIED], the 7-vs-6 cardinality mismatch removed). Verified by an `rg`/import test asserting the `<option value=...>` set equals `BODYWEIGHT_BANDS` (the 6 kg tokens) AND each option's label text is its pinned pounds range.
3. The four demographic fields round-trip through the BUILT capture seam: a POST of the SPA form to `/upload` lands each token via the unchanged `persist_capture` (`capture.py:230-300` [VERIFIED]) — `sex-for-dosing`/`bodyweight-band`/`equipment-access-class` as `WIRED_TOKENS` pass-throughs, birth-year → the named-excluded `date-of-birth` source → `summarize` derives `training-age-band` — verified by a round-trip test asserting each of the four tokens resolves through `summarize` from the submitted value (0 orphan tokens on the SPA surface, against today's 4).
4. The `Upload Documents` chat composer is wired to `/chat`: the rendered SPA carries a `fetch("/chat"` (or equivalent same-origin XHR) in its inline JS that sends the turn and renders the returned turn-list + per-turn receipt (the `chat.dispatch_turn` JSON receipt shape `{"reply","receipt","progress","degraded"}`, `server.py:205-252` [VERIFIED]) — verified by a structural test asserting the SPA's inline JS posts to `/chat` and renders the receipt (against today's dead `Send →` composer with 0 fetch — the `chatHTML` template's `.composer`, `prototype/app.html:467`, mounted for the upload screen at `:387`+`:473` [VERIFIED]).
5. HONEST ingestion-state: the `Upload Documents` document-cards + ingestion statusbar render the real injected `status` load-state — 0 fabricated ingestion counts (no "12,480 readings", "✓ ingested", "2 of 4 categories" presented as the operator's data, `prototype/app.html:370,379` [VERIFIED]) — verified by rendering with an EMPTY store/status and asserting the document-cards show not-linked/awaiting states (0 fabricated counts).
6. Form objective-only + single egress class: the SPA `Upload Documents` form carries 0 rich-section `name=` fields (no goal/training/nutrition/supplement/peptide form field — those are the chat-only surface); the SPA's only outbound calls are same-origin `/upload` + `/chat` (0 new outbound class beyond the ADR-0016 turn) — verified by enumerating the form's `name=` set (demographics + uploads only) AND `rg` over the rendered SPA finding 0 fetch/XHR to a non-loopback URL.
7. `.venv/bin/python -m pytest tests/serve/test_app_shell.py tests/serve/test_intake_demographics.py` passes.

**Risk Mitigations:** ADR-0029 Confirmation (Split preserved: the SPA carries BOTH the objective form AND the conversational surface) — crit 1,4,6. ADR-0018 split realized on the new surface — crit 1,2,3,6. markup↔gate drift — crit 2. ADR-0029 PII-boundary (single egress class) — crit 6. ADR-0009 D2 honest-data (`Upload Documents`) — crit 5.
**Dependencies:** ADR-0029-T1 (the SPA tracked render-view module this task wires — T3 modifies the file T1 creates).

---

### ADR-0029-T4: Not-Naive Intake Elicitation on the SPA Surface (Sentinel Bands = Gap; Fresh Operator Asked; Never Vacuous `intake_complete`)

**Status:** TODO
**ADR Source:** ADR-0029, Decision (`Upload Documents` realizes the form/chat split — the conversational surface must actually elicit the rich sections); PF-S87-01 (rich capture that vacuously reads "done" is the gap the conversational-intake set exists to close); design CONCERN-1 (a chat-covered domain whose token is not planner-feeding reports record-only, never `domain_done` vacuously); ADR-0016 (the control surface stays de-identified)
**Files to create/modify:**
- `tests/serve/test_intake_elicitation.py` -- Create: the SPA-surface elicitation proof (rides the built `chat.plan_next_turn`/`dispatch_turn` + the served `/chat` route; no new production code)

**Acceptance Criteria:**
1. A FRESH operator (empty store → the de-identified `summarize` with the chat tokens at their `not-discussed`/no-signal sentinel, `router.py:_ALWAYS_SET_DERIVED:488-492` [VERIFIED]) drives the served `/chat` and is ASKED the genuine gaps — `plan_next_turn` returns a non-empty `missing_fields`/`target_domain` for the goals/training domains with absent tokens — verified by a fresh-store `/chat` turn asserting the intent surfaces the gap (the operator is asked, not skipped).
2. SENTINEL = GAP (the PF-S87-01 trap): the always-set chat tokens (`dietary-pattern-class`/`supplement-stack-class`/`peptide-use-class`/`training-volume-band`) at their `not-discussed`/`none`/`moderate` sentinel are NEVER read as "captured" to vacuously satisfy `domain_done` — the nutrition/supplements/peptides domains report RECORD-ONLY (captured-for-record, not-planned; `chat._DOMAIN_TOKENS` empty-tuple, `chat.py:39-56` [VERIFIED]), never `domain_done` from the sentinel — verified by a test that a fresh all-sentinel summary yields the record-only state for those domains, not `domain_done`.
3. NEVER vacuous `intake_complete`: with a genuine gap still open, the elicitation loop NEVER reports `intake_complete` True — verified by a fresh-operator drive asserting `intake_complete` is False while any goals/training gap is open and the record-only domains have not been surfaced.
4. Failing-capable negative control: a summary with the genuine gaps FILLED + the record-only domains surfaced/declined reports `intake_complete` True — verified by the complementary case, proving crit 3 distinguishes complete from incomplete (not constant-False).
5. De-identified control surface: `plan_next_turn` reads ONLY the de-identified `summarize` mapping (0 raw transcript / scaffold read in the strategy, `chat.py:125-216` [VERIFIED]); the returned `TurnIntent` carries 0 raw operator string (token/domain names + booleans only) — verified by asserting the intent's values are token/domain names + booleans.
6. `.venv/bin/python -m pytest tests/serve/test_intake_elicitation.py` passes.

**Risk Mitigations:** PF-S87-01 (rich capture that vacuously reads done) — crit 2,3 (sentinel=gap, never vacuous complete). design CONCERN-1 (record-only, never vacuous `domain_done`) — crit 2. ADR-0029 PII-boundary (the control surface stays de-identified) — crit 5. Non-tautological elicitation proof — crit 4 (failing-capable).
**Dependencies:** ADR-0029-T1 (the served SPA surface this elicitation runs on). T4 rides the BUILT `chat.plan_next_turn`/`dispatch_turn` + the already-served `/chat` route (route table unchanged) — it does NOT consume T3's SPA chat-composer fetch markup (the test POSTs to `/chat` directly), so the honest precondition is only that the SPA surface is served (T1), not that the composer is wired (T3).

---

### ADR-0029-T5: End-to-End Conversation → Usable Plan Through the SPA-Served Path (Compose ADR-0017-T2; Non-Tautological; Mock-Tested)

**Status:** TODO
**ADR Source:** ADR-0029, Decision (the SPA's `Plan` screen surfaces the planner reading the de-identified `SUMMARY_FIELD_SET`; the intake slice's purpose is that real data flows in and produces a plan) + ADR-0029 depends-on ADR-0017 (de-identified persistence) and ADR-0019 (the field set the plan personalizes from); PF-S87-01 (the headline: a real-or-fixture conversation produces a USABLE plan, not just working plumbing); ADR-0017-T2 (the composed recipe — `recorded == True` + content-traceability, the non-tautological headline)
**Files to create/modify:**
- `tests/plan/test_conversation_to_plan_e2e.py` -- Create (absent today, `test ! -f` returns 0 [VERIFIED]): the headline E2E; no new production code (binds the already-built mechanism)

**Acceptance Criteria:**
1. HEADLINE (non-tautological): a fixture conversation (a mock backend at the client seam returning scripted `converse` turns + extraction proposals carrying chat-sourced rich-domain facts, AND a scripted `author` envelope) driven through the served `/chat` → `persist_capture` → `summarize` → `generate_plan`/`compute_plan` produces a USABLE plan — `recorded == True` (`generate_plan.py` [VERIFIED]), ≥1 domain plan recorded, AND the plan CONTENT traces to a specific fact the fixture conversation supplied (a de-identified value appears in the rendered plan), NOT the honest no-plan state — verified by the E2E asserting `recorded == True` AND content-traceability, NEVER merely "a plan object is non-None".
2. Failing-capable negative control: the SAME pipeline driven with a fixture supplying NO usable facts (an empty/declined conversation) observes the HONEST NO-PLAN state (`recorded == False`) — verified by the negative-control case, proving crit 1 distinguishes a usable plan from the no-plan state.
3. Mock-tested, no live API: the E2E injects the mock backend at the ADR-0015 seam and makes 0 live `key_source.resolve()`-gated call; deterministic + CI-runnable with no network and no key — verified by the test passing under `.venv/bin/python -m pytest` + a mock-injection assertion. (T2's live converse is NOT exercised here — the seam is mocked.)
4. LIVE variant operator-gated: the test file carries a docstring-noted LIVE variant (real conversation → real plan via the runtime keychain key) as a `@pytest.mark.skipif`-on-absent-key, referencing `scripts/model/keychain-setup.md`, explicitly NOT a CI gate — verified by the live variant collecting + skipping without the key.
5. The persisted side stays de-identified after the conversation: a post-conversation `pii_scan` over the store + the `summarize` output finds 0 raw operator PII (seed an identifiable raw value in a `/chat` turn; assert it does not survive into a token or the summary) — verified by the post-conversation PII scan returning 0.
6. `.venv/bin/python -m pytest tests/plan/test_conversation_to_plan_e2e.py` passes.

**Risk Mitigations:** PF-S87-01 (a feature plumbed but not proven to produce a usable plan) — crit 1 (usable-plan proof), crit 2 (failing-capable). ADR-0017 Falsification (raw PII in the persisted side) — crit 5. ADR-0029 PII-boundary — crit 5. Live-API coupling — crit 3,4 (mock-tested CI, live operator-gated).
**Dependencies:** ADR-0029-T3 (the SPA-realized `/chat` → plan slice this proves end-to-end).

---

## Dependency Map

```
ADR-0029-T1 --> ADR-0029-T3   (T3 modifies the SPA render-view module T1 creates; the form/chat is wired into the served surface T1 stood up)
ADR-0029-T1 --> ADR-0029-T4   (T4 validates elicitation on the served SPA surface T1 stands up; it rides the BUILT /chat route + chat.plan_next_turn/dispatch_turn, NOT T3's composer markup)
ADR-0029-T3 --> ADR-0029-T5   (T5 is the headline usable-plan proof for the SPA-realized /chat → plan slice)
```

`ADR-0029-T2` has no in-spec edges (it edits `scripts/model/client.py` only; its consumer is the operator-present LIVE run, out of scope — every in-spec test mocks the model backend at the seam).

Entry points (no inbound edges): **ADR-0029-T1**, **ADR-0029-T2**

Topological order (Kahn parallel groups):
1. **Group 1 (entry points):** ADR-0029-T1, ADR-0029-T2 (independent — T1 stands up the served SPA shell; T2 implements the live converse backend)
2. **Group 2:** ADR-0029-T3, ADR-0029-T4 (both after T1 — parallel; T3 wires the `Upload Documents` form/chat into the served surface, T4 proves the elicitation on that served surface via the BUILT `/chat` route; T3 and T4 share no file)
3. **Group 3:** ADR-0029-T5 (after T3 — the headline usable-plan proof for the slice T3 realizes)

Critical path: **ADR-0029-T1 → ADR-0029-T3 → ADR-0029-T5** (length-3; T4 is length-2 off T1, not on the critical path).

No cycles (3 groups; every edge points from an earlier group to a later group; Kahn drains all 5 nodes). T2 is a standalone entry point in Group 1.

**Wave-checkpoint Go/No-Go (the front-end serving gate):** the SPA serves with 0 off-file references (T1 crit 1 — the AUTHORITATIVE `render.emit`-returns-a-path probe + the T1 crit 2 render.emit-RAISES negative probe), the served Dashboard/Plan/Team present 0 fabricated data (T1 crit 5), the `Upload Documents` form/chat round-trips through the built `/upload`+`/chat` seams (T3), the elicitation is not-naive (T4), the conversation produces a usable plan (T5 — the PF-S87-01 headline), AND the frozen surfaces are byte-unchanged: `git diff --numstat <pre-spec> -- scripts/plan/orchestrate.py scripts/plan/pipeline.py scripts/plan/assemble.py scripts/plan/generate_plan.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/track.py scripts/plan/router.py scripts/plan/deid_in.py` reports 0 (NFR-4, the EXTEND-NOT-REBUILD checkpoint probe).

## Test Strategy

### Unit Tests
- **Scope:** `vault/design/templates/app_shell.py` (the SPA render output — assets, honest-data, form/chat markup), `scripts/generate/generate.py` (the `"app"` registration + status seam), `scripts/serve/server.py` (the GET `/` re-point), `scripts/model/client.py` (the live `converse` backend, mocked).
- **Approach:** `pytest` against the rendered SPA HTML string (parse the form/screens, enumerate `name=`, `rg` the asset/fetch surface) + a FIXTURE/MOCK SDK client injected at the ADR-0015 seam (no live API, no key) for the converse tests; a temp store/scaffold root + the `ingest.status.resolve` seam for the honest-state render.
- **Criteria covered:** ADR-0029-T1 crit 1-8; ADR-0029-T2 crit 1-6; ADR-0029-T3 crit 1,2,4,5,6.

### Integration Tests
- **Scope:** the cross-seam paths — (a) GET `/` served-body is the SPA over the loopback handler (T1); (b) the SPA demographic form POST `/upload` → `persist_capture` → `summarize` round-trip (T3, reusing the built `test_intake_demographics` capture assertions); (c) the served `/chat` per-turn dispatch driven fresh — the elicitation gap-set + record-only domains (T4); (d) the HEADLINE conversation→usable-plan E2E through the served `/chat` → `summarize` → `generate_plan` (T5).
- **Approach:** run the server on an ephemeral loopback port in a fixture; POST the SPA form to `/upload` and synthetic `/chat` turns over a scripted mock client; assert the store/scaffold state, the `summarize` output, and the recorded plan.
- **Criteria covered:** ADR-0029-T1 crit 6,7; ADR-0029-T3 crit 1,3,7; ADR-0029-T4 crit 1-6; ADR-0029-T5 crit 1-6.

### Risk-Specific Tests
- **INLINE-ASSET (ADR-0029 Negative-1, the AUTHORITATIVE check):** the `render.emit`-RETURNS-a-path probe (T1 crit 1) + the render.emit-RAISES negative probe on a re-introduced off-file reference (T1 crit 2) — a substring grep is non-authoritative and is NOT substituted.
- **HONEST-DATA (OQ-3 / ADR-0009 D2):** the served Dashboard/Plan/Team carry 0 fabricated operator data (T1 crit 5); the `Upload Documents` ingestion-state is the real load-state (T3 crit 5).
- **CROWN-JEWEL PII 0-LEAK (NFR-1):** the SPA introduces 0 new outbound class — its only fetches are same-origin `/upload` + `/chat` (T3 crit 6); the live converse fails closed with 0 raw-turn/key leak (T2 crit 3); the post-conversation store + `summarize` carry 0 raw operator PII (T5 crit 5); the existing `tests/serve/test_chat_no_egress.py` + `tests/serve/test_serve_no_egress.py` cover the backend single-egress-class (unchanged).
- **FROZEN-ENGINE numstat (NFR-4, EXTEND-NOT-REBUILD):** `git diff --numstat <pre-spec>` = 0 on `scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py` + `deid_in.py` — a wave-checkpoint probe (no task edits them; T2 edits only `converse` in `client.py`, T2 crit 5).
- **PF-S87-01 NON-TAUTOLOGICAL E2E:** the headline asserts `recorded == True` + content-traceability, never "a plan object is non-None" (T5 crit 1); the failing-capable negative control proves it distinguishes the no-plan state (T5 crit 2); the not-naive elicitation never vacuously completes (T4 crit 2,3,4).
- **Public-repo key leak (MEMORY):** the runtime key source reads no tracked file + 0 key literal in the tracked tree (T2 crit 2).
- **BACKWARD-COMPAT:** the wizard→SPA served-body assertions are re-pointed; the wizard MODULE tests stay green (T1 crit 7); no tautological test asserts the dead-as-served wizard.

## NFRs (cross-cutting, each falsifiable, each tied to ADR-0029)

- **NFR-1 (crown-jewel PII boundary — ADR-0029 PII-boundary-unchanged / ADR-0016/0017).** The served front-end's only outbound class is the ADR-0016 `/chat` one-turn egress (raw live conversation, no-train lane); `/upload` is local loopback; every persisted fact stays de-identified via the unchanged extractor + gate + `summarize`. *Falsified if* the SPA introduces ≥1 outbound class beyond `/chat`, or ≥1 post-conversation store write / `summarize` field is not de-identified. (T2 crit 3, T3 crit 6, T5 crit 5.)
- **NFR-2 (inline-asset / 0 external request — ADR-0029 Negative-1).** The served SPA carries 0 off-file asset references; the AUTHORITATIVE check is `render.emit` RETURNING a path rather than RAISING. *Falsified if* `render.emit` raises on the assembled SPA, or the served HTML carries any `http(s)://`/`//`/bare-path asset reference. (T1 crit 1,2,3,4.)
- **NFR-3 (honest data — ADR-0029 OQ-3 / ADR-0009 D2).** The served Dashboard/Plan/Chat-with-Team present 0 fabricated demo data as the operator's data; `Upload Documents` is the only live-wired surface and its ingestion-state is the real load-state. *Falsified if* any non-intake screen presents a fabricated metric/plan as the operator's data, or the `Upload Documents` cards show fabricated ingestion counts. (T1 crit 5, T3 crit 5.)
- **NFR-4 (extend-not-rebuild — the frozen engine + de-id boundary).** The inner plan engine `scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py` + the `deid_in` de-id-IN boundary are byte-frozen across the spec; the only model-client change is `converse`. *Falsified if* `git diff --numstat <pre-spec>` ≠ 0 on those 9 files, or `client.py` changes a method other than `converse`. (T2 crit 5; the wave-checkpoint numstat probe.)
- **NFR-5 (loopback transport unchanged — ADR-0029 depends-on ADR-0013).** The SPA is served as the GET `/` body of the existing `127.0.0.1` loopback server with 0 new serving process/port; only the rendered body changes. *Falsified if* a new bind (other than 127.0.0.1) or a new serving process/port is introduced, or the route table changes from {GET `/`, POST `/upload`, POST `/chat`}. (T1 crit 6.)
- **NFR-6 (interface-pinned, internals-discretionary).** The build PINS the served-view registration contract (`generate.run("app")` over a `render(store_read,...)` module), the AUTHORITATIVE inline-asset check (a `render.emit` run), the demographic `name=`→token wiring (reusing the built capture seam), the `/chat` receipt shape, and every acceptance criterion. It does NOT pin the SPA's exact CSS/JS, the lucide-vendoring mechanism (OQ-2 — extract-used-icons preferred), the `/chat` fetch wire format, or the converse SDK request/response — implementer discretion.

## Repo-Grounding Ledger

| Task | RGC-1 (manifest action vs disk) | RGC-2 (premise freshness) | RGC-3 (cited-input existence + declared shape) | RGC-4 (capability non-duplication) | Disposition |
|------|---------------------------------|---------------------------|-----------------------------------------------|-----------------------------------|-------------|
| T1 | pass — `app_shell.py`/`test_app_shell.py` Create=absent; `generate.py`/`server.py`/`test_server.py` Modify=present | stale→actual — `render.emit` raises on off-file AND `server._render_intake` hardcodes `generate.run("intake")` STILL TRUE (`server.py:81` [VERIFIED]); `_TEMPLATES` registry confirmed (`generate.py:27`) | pass — `prototype/app.html` cited refs present (lucide `:411`, body.png `:292`, demo data `:290,295-296,300-301,323-325,342-345`, SPA `<title>A+ Maxing` `:2`); `test_server.py` `WIZARD_TITLE` present — constant def `:34` + 19 assertion sites (`:189,313,…,852`), all break under the re-point (SPA title ≠ wizard title) | pass — the SPA view is the ADR-0029 supersession of the wizard view, not a duplicate; the `intake` template is RETAINED (OQ-1) | Grounded |
| T2 | pass — `client.py`/`test_client.py` Modify=present | pass — `_ClaudeNoTrainBackend.converse` is a `NotImplementedError` stub (`client.py:201-206` [VERIFIED]); `deidentify` is implemented live (`client.py:213+`) | pass — the `deidentify` mirror (`_client`/`key_source.resolve`/bounded retry/`ModelCallError`+`from None`) present; the public `ModelClient.converse` validation present (`client.py:46-58`) | pass — `converse` is the existing stub method, not a new capability; the only SDK import stays inside `scripts/model/` | Grounded |
| T3 | pass — `app_shell.py`/`test_app_shell.py` created by T1; `test_intake_demographics.py` Modify=present | stale→actual — the demographic CAPTURE seam is BUILT (`capture.py` routes all four; `WIRED_TOKENS:61-63`, `_DOB_FIELD:84`, `_BOUNDED_ENUMS:123-125` [VERIFIED]); the wizard form is already activated. The orphan-ness is ONLY on the SPA surface (`app.html:362-366` inputs carry 0 `name=`) | pass — `SEX_OPTIONS`/`BODYWEIGHT_BANDS`/`EQUIPMENT_ACCESS_CLASSES` enum constants present; the `/chat` route + `dispatch_turn` receipt shape `{"reply","receipt","progress","degraded"}` present (`server.py:205-252`); the dead `Send →` composer present (`app.html:467`, the `chatHTML` template; upload-screen mount `:387`+`:473`) | pass — the demographic capture + `/chat` dispatch are REUSED unchanged, not duplicated; T3 adds only the SPA-surface producer markup | Stale-Premise-Reconciled |
| T4 | pass — `test_intake_elicitation.py` Create=absent | pass — `chat.plan_next_turn` record-only/`domain_done` + `_DOMAIN_TOKENS` empty-tuple record-only domains BUILT (`chat.py:39-216` [VERIFIED]); `_ALWAYS_SET_DERIVED` sentinel BUILT (`router.py:488-492`) | pass — the de-identified `summarize` control surface present; the served `/chat` dispatch present | pass — the elicitation backend is REUSED; the test is the absent SPA-surface proof, not a duplicate | Grounded |
| T5 | pass — `test_conversation_to_plan_e2e.py` Create=absent (`test ! -f` returns 0 [VERIFIED]) | stale→actual — the ADR-0019 chat tokens are MINTED + derived + tripwire-green (`router.py:43-46,112-115,474-492` [VERIFIED]) — the ADR-0017-T2 "needs both waves' tokens" premise is SATISFIED, so the brief's candidate T6 is NOT needed; `generate_plan`/`compute_plan`/`record_plan`/`summarize`/`pii_scan` present byte-unchanged | pass — the mock-client seam (`ModelClient(backend=...)`, `client.py:44` [VERIFIED]) present; `keychain-setup.md` present for the live-variant reference | pass — the E2E is the absent headline proof; it binds the built mechanism, adds 0 production code | Stale-Premise-Reconciled |

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR-0029 section (Decision / Consequences / Validation Approach / depends-on edge + OQ).
- [x] Every ADR ID in the `adrs` frontmatter (ADR-0029) has at least one task (T1-T5 all cite ADR-0029).
- [x] All ADR IDs resolve to actual ADR files on disk (`docs/adr/ADR-0029-unified-spa-front-end-shell.md` [VERIFIED]).

### Acceptance Criteria Quality
- [x] Every task has ≥1 acceptance criterion (each has 6-8).
- [x] All criteria are binary — each cites a `pytest` target, an `rg`/grep count, a `render.emit` return/raise, a `git diff`, a round-trip assertion, or a PII-scan count.
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient".

### File Manifest Integrity
- [x] Every task has a file manifest; every file in any task block appears in the top-level File Manifest and vice versa.
- [x] No task lists a directory instead of a specific file.
- [x] Every source file has a corresponding test file (`app_shell.py`→`test_app_shell.py`; the `generate.py`/`server.py` re-point→`test_app_shell.py`/`test_server.py`; `client.py` converse→`test_client.py`; the elicitation→`test_intake_elicitation.py`; the E2E→`test_conversation_to_plan_e2e.py`).

### Dependency Map Integrity
- [x] No cycles (Kahn drains all 5 nodes; 3 ordered groups; T2 a standalone Group-1 entry point).
- [x] Every task ID in a Dependencies field appears as a node; every edge corresponds to a Dependencies entry; the entry points (T1, T2) have "None (entry point)".
- [x] No phantom dependency — T3→T1 (T3 edits the file T1 creates), T4→T1 (T4 validates elicitation on the served surface T1 stands up, riding the BUILT `/chat` route + `chat.plan_next_turn`/`dispatch_turn`, NOT T3's composer markup), T5→T3 (T5 proves the slice T3 realizes); each edge names the artifact/surface that flows.

### Constraint Propagation
- [x] CROWN-JEWEL PII 0-leak carried as NFR-1 + per-task criteria (T2 crit 3, T3 crit 6, T5 crit 5).
- [x] INLINE-ASSET (AUTHORITATIVE `render.emit` probe, not a grep) carried as NFR-2 + T1 crit 1,2.
- [x] HONEST-DATA (ADR-0009 D2) carried as NFR-3 + T1 crit 5, T3 crit 5.
- [x] EXTEND-NOT-REBUILD (frozen engine numstat) carried as NFR-4 + the wave-checkpoint probe + T2 crit 5.
- [x] LOOPBACK transport unchanged carried as NFR-5 + T1 crit 6.

### Unresolved Concerns
- [x] Disposition section present (5 rows): OQ-1 Defer, OQ-2 Proceed-assumption, OQ-3 Proceed-constraint, + the two live-tree stale-premise reconciliations (ADR-0018 capture-built, ADR-0019 tokens-built).
- [x] Defer dispositions justify why deferral is safe (intake.py deletion is orthogonal cleanup; the ADR-0019 token work is already satisfied).

### Risk Coverage
- [x] Risk Mitigations field on every task; every ADR-0029 negative consequence covered (Negative-1 off-file refs → T1; Negative-2 maintenance surface → bounded by the single inline-asset module; Negative-3 wizard-recipe retarget → T3 realizes the split on the SPA; the Neutral fabricated-demo collision → T1 honest-data).

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category.
- [x] Risk-specific tests exist for the inline-asset probe, honest-data, PII 0-leak, frozen-engine numstat, and the non-tautological E2E.

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status).
- [x] No placeholder text ("TBD", "TODO: fill in", "...").
- [x] The headline capability (PF-S87-01: conversation → usable plan through the SPA-served path) is a named end-to-end task (T5) testable against mocks, with the live-API run gated on the runtime keychain key.

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists in the current worktree (`generate.py`/`server.py`/`client.py`/`test_server.py`/`test_client.py`/`test_intake_demographics.py` [VERIFIED]); the `app_shell.py` Modify in T3 is created by T1 in dependency order.
- [x] Every File Manifest `Create` row names a path that does NOT already exist (`app_shell.py`/`test_app_shell.py`/`test_intake_elicitation.py`/`test_conversation_to_plan_e2e.py` — all absent [VERIFIED]).
- [x] Every ADR premise a task relies on was re-verified against the current repo; stale premises (the "orphan tokens", the candidate T6 token-extension) are recorded in the Repo-Grounding Ledger with the actual state.
- [x] Every cited input a task parses/reads declares its structural assumption AND the live file satisfies it (the app.html cited lines, the gate enum constants, the `/chat` receipt shape, the `_TEMPLATES` registry — all re-grepped).
- [x] No task proposes a new artifact that duplicates an existing capability (the SPA view supersedes the wizard view per ADR-0029; the capture/`/chat`/token surfaces are reused, not rebuilt).
- [x] Repo-Grounding Ledger present, one row per task, each with a disposition.
