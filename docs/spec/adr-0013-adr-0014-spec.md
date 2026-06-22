---
scope: "ADR-0013 ADR-0014 (+ ADR-0012 amendment): interactive intake website — loopback upload server + web-form capture"
adrs: [ADR-0013, ADR-0014, ADR-0012]
tier: 6
created: 2026-06-21
status: approved
---

# Spec: Interactive Intake Website (Loopback Upload Server + Web-Form Capture)

## Component Overview

This spec delivers the interactive intake website: an operator-started, ephemeral, loopback-only HTTP server (`python -m scripts.serve`) that serves the existing intake wizard and receives browser uploads, routing each into the UNCHANGED ingestion seam (ADR-0013), plus the web-form capture path that persists the wizard's Step-2..6 input by data class — de-identified `SUMMARY_FIELD_SET`-token fields to the local store, raw/rich context to the gitignored `vault/scaffold/filled/` (ADR-0014). The Apple Health export **zip** is accepted by the **healthkit adapter itself** (`scripts/ingest/adapters/healthkit.py`), which extracts its `export.xml` member, mirroring `dna.land`'s zip-member extraction (the ADR-0012 2026-06-21 amendment, which the ADR-0013 `complements ADR-0012` edge confirms lives in the ingest/adapter layer); the server routes the uploaded file (zip or xml) into `ingest.run` via that now-zip-aware adapter and adds no extraction logic. The deliverable is a new `scripts/serve/` package plus the form-handler wiring — a stdlib `http.server` bound to `127.0.0.1` only, a `multipart` reader that streams each upload to a server-chosen temp path, a route that content-disambiguates a `.zip` (Apple-Health-export shape → healthkit adapter; 23andMe shape → `dna.land`) and dispatches the upload into `ingest.run` / `dna.land`, and a re-render via `generate.run('intake')`. There is no third-party web framework, no database engine, and no always-on daemon: the process is operator-started and exits when stopped.

The server is **glue, not a new ingestion path**. It reuses, byte-unchanged, the shared seam the data-in / data-out waves already built — `ingest.run(adapter, export_file, root)` ([scripts/ingest/ingest.py:39](../../scripts/ingest/ingest.py#L39) [VERIFIED]), the adapter contract `adapter.py`, and `scheduler.py` (the 0-shared-routine-edit invariant names exactly these three; ADR-0003-T2) — plus `dna.land(source_file, dna_root)` ([scripts/ingest/dna.py:71](../../scripts/ingest/dna.py#L71) [VERIFIED]), the CLI's source-detection map `_EXT_SOURCE` + `_detect_source` ([scripts/ingest/__main__.py:39,42](../../scripts/ingest/__main__.py#L39) [VERIFIED]), `status.resolve` / `status.wearable_status` ([scripts/ingest/status.py:51,17](../../scripts/ingest/status.py#L17) [VERIFIED]), `intake.render(store_read, *, status, _today)` ([vault/design/templates/intake.py:263](../../vault/design/templates/intake.py#L263) [VERIFIED]) re-rendered through `generate.run('intake')` ([scripts/generate/generate.py:34](../../scripts/generate/generate.py#L34) [VERIFIED]), and `store.append(item, reading, root)` for the form-capture persistence ([scripts/store/store.py:134](../../scripts/store/store.py#L134) [VERIFIED]). The Apple-Health-zip→`export.xml` extraction is the ONE adapter change: it lives in the healthkit ADAPTER (`scripts/ingest/adapters/healthkit.py`), NOT a serve-layer module and NOT the shared routine — `healthkit.py` is an adapter, which ADR-0003-T2's 0-shared-routine-edit invariant explicitly permits to change (the invariant protects `ingest.py`/`adapter.py`/`scheduler.py`, never the adapters), so an Apple Health zip is ingestable from BOTH `python -m scripts.ingest` and the web upload. The capture path routes only through `router.summarize`'s closed `SUMMARY_FIELD_SET` de-identification gate ([scripts/plan/router.py:18-36,352](../../scripts/plan/router.py#L18) [VERIFIED]) — a captured de-identified field is written to a store item named for its token, tagged `source: "intake"`, and reaches a specialist only via that gate. The new network surface is proven egress-free under the already-audited OS-level egress guard `egress_guard.run(operation)` ([scripts/guard/egress_guard.py:82](../../scripts/guard/egress_guard.py#L82) [VERIFIED]) by TEST (the guard forks a child that `os._exit`s and returns only a bool, so it cannot wrap a request that must return a re-rendered response — it is the test harness, not a per-request production wrapper); the production server is egress-free by construction (it makes no outbound calls).

These two decisions are the "intake-website" cut of the V1 architecture. ADR-0013 fixes the TRANSPORT (the loopback server + the upload route); ADR-0014 fixes the DATA-WRITE path (the form-capture persistence by data class). They are distinct, non-circular decisions — the server hosts the forms ADR-0014 persists, and ADR-0014's write path is consumed only through the server's POST handler — so the build orders Wave A (the upload server, the more-foundational transport) before Wave B (the interactive wizard forms that depend on the server existing). The ADR-0012 amendment is folded into Wave A: the Apple-Health-zip extraction is the input-format handling the upload route needs, and it mirrors `dna.land`'s existing `_genotype_member` / `zipfile.is_zipfile` pattern ([scripts/ingest/dna.py:49,92](../../scripts/ingest/dna.py#L49) [VERIFIED]).

The intake wizard's read-only Step 1 ("Your info & documents") is already LIVE — its load-state cards render the real store + dropzone state via `status.resolve` ([vault/design/templates/intake.py:1-12,263](../../vault/design/templates/intake.py) [VERIFIED]). Steps 2-6 are a "static flow shell" ([vault/design/templates/intake.py:5](../../vault/design/templates/intake.py#L5) [VERIFIED]): this spec makes them interactive and persisting. The field-map is grounded against the closed `SUMMARY_FIELD_SET` and against the wizard's current placeholder fields, and is the load-bearing input to ADR-0014's by-data-class routing (the Field Map subsection below).

**Field-map convention.** A captured field is one of three classes: (1) a **wired de-identified** field whose token is in `SUMMARY_FIELD_SET` — written to a store item under its token name with `source: "intake"`, reaching the plan through `summarize`; (2) a **record-only** field with no de-identified consumer today (most of Step 3 training, all of Step 4 nutrition, the raw Step-5 stack) — captured to the gitignored `vault/scaffold/filled/` and NEVER into a `SUMMARY_FIELD_SET` item; (3) a **curated** field (`rx-interaction-classes`) whose de-identified class tokens are emitted from the raw Step-5 stack by an operator/liaison curation step, never raw drug names ([scripts/plan/router.py:113-176](../../scripts/plan/router.py#L113) [VERIFIED]).

### Field Map (grounded against the closed `SUMMARY_FIELD_SET`)

| Wizard step | Captured input | Class | Persistence target | Consumer |
|-------------|----------------|-------|--------------------|----------|
| Step 2 — Goals & priorities | goal-domains, goal-targets, goal-priority-order | wired de-identified | store item per token, `source:"intake"` | `summarize` → `assemble` |
| Step 2 — Goals & priorities | **hard-limits** (ADD: the fail-closed HALT-filter input, ABSENT from the mock) | wired de-identified | store item `hard-limits`, `source:"intake"` | `summarize` → `assemble` HALT |
| Step 3 — Training | training experience, sessions/week, session length, style/split, current main lifts, train-around | record-only (no wired consumer) | `vault/scaffold/filled/` (honestly labeled) | profile record (no plan flow) |
| Step 3 — Training | **recovery-status-band** (ADD; derivable de-identified band) | wired de-identified | store item `recovery-status-band`, `source:"intake"` | `summarize` → `assemble` |
| Step 4 — Nutrition | dietary pattern, meals/day, allergies, foods-to-avoid | record-only (NO wired consumer) | `vault/scaffold/filled/` (honestly labeled) | none (OQ-1 future field-set extension) |
| Step 5 — Supplements & peptides | raw supplement names + doses, raw peptide names + doses, hoped-to-address | record-only (NO wired consumer) | `vault/scaffold/filled/` (honestly labeled) | none (raw drug names NEVER cross the gate) |
| Step 5 — Supplements & peptides | the supplement↔Rx interaction FORM field (operator-typed text, untrusted) | record-only (Wave-B FIX-A) | `vault/scaffold/filled/` (honestly labeled) | none — the model-bound `rx-interaction-classes` store item is fed ONLY by the curation surface deferred to ADR-0014 OQ-2, NEVER this serve-layer field |
| Step 6 — Review & generate | (handoff only) "Save & open plan generation" → `/generate-plan` | n/a | n/a (NOT in-app generate) | `/generate-plan` |

`SUMMARY_FIELD_SET` membership of every "wired de-identified" token above is verified at [scripts/plan/router.py:18-36](../../scripts/plan/router.py#L18) [VERIFIED] (`goal-domains`, `goal-targets`, `goal-priority-order`, `hard-limits`, `recovery-status-band` all present). The `rx-interaction-classes` store item remains a `SUMMARY_FIELD_SET` member (router.py:35) but the capture FORM field is NOT wired to it (Wave-B FIX-A — record-only); the item is fed by the curation surface deferred to ADR-0014 OQ-2. The raw Step-5 stack names are named-excluded raw PII ([scripts/plan/router.py:41-62,104-176](../../scripts/plan/router.py#L41) [VERIFIED]); the curation surface for `rx-interaction-classes` is operator/liaison-emitted (ADR-0014 OQ-2), not a code lookup of raw names.

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0013 OQ-2 | Open Question | Default port `scripts.serve` binds on `127.0.0.1`, and the collision behavior when that port is in use | Proceed | An implementation detail of startup, not a boundary decision. The spike-free build fixes a default port and a collision behavior (fail-loud with a stated alternate-port instruction) in `ADR-0013-T1`; the loopback-only / ephemeral / egress-free decision is unchanged by the number. No task gates on the specific port. |
| ADR-0013 OQ-1 | Open Question (PRD NG-4 wording) | Update PRD NG-4 to record the artifact-vs-ingest axis carve-out | Defer | Out of scope for this code build — a PRD documentation follow-up owned in the ADR (target 2026-06-30). The carve-out is recorded in ADR-0013; the server's intake-only / no-artifact-serving invariant is enforced in `ADR-0013-T4` regardless of the PRD text. Recorded as a doc-coherence interface point, not specced here. |
| ADR-0014 OQ-1 | Open Question | The de-identified token forms for nutrition + the supplement/peptide stack, and the PII-boundary review they require | Defer | Out of scope: until a future ADR-0006-T0 PII-boundary decision adds those tokens to `SUMMARY_FIELD_SET`, Steps 4-5 are captured to the gitignored scaffold as record-only and do NOT flow into the plan. Wave B's capture path persists them honestly labeled record-only; it adds 0 `SUMMARY_FIELD_SET` tokens ([scripts/plan/router.py:18-36](../../scripts/plan/router.py#L18) [VERIFIED]). Safe to defer: the record-only path is complete without the tokens; the plan simply has no nutrition/supplement section until they land. |
| ADR-0014 OQ-2 | Open Question | The curation surface for `rx-interaction-classes` (how the operator/liaison emits de-identified class tokens, never raw drug names, and where that step lives) | Proceed (record-only this build) | The Step-5 stack capture lands raw names ONLY in the gitignored scaffold; the `rx-interaction-classes` store item is written from the operator/liaison-curated class tokens, not derived in code from raw names ([scripts/plan/router.py:137-176](../../scripts/plan/router.py#L137) [VERIFIED]). This build captures the raw stack record-only and writes `rx-interaction-classes` ONLY when curated class tokens are supplied (the form surfaces a class-token field, not a drug-name→class code path). The curation mechanism beyond that field is the deferred OQ-2; no code lookup of raw names is built. |
| ADR-0012 amendment (2026-06-21) | Decision (input format) | The Apple Health upload accepts the export zip and extracts `export.xml` itself, mirroring `dna.land`; extraction lives in the ingest/adapter layer | In scope (Wave A) | Built in `ADR-0013-T3`: the **healthkit adapter** (`scripts/ingest/adapters/healthkit.py`) is extended to accept a zip — its `read_readings` detects a zip, extracts the single `*/export.xml` member (the `zipfile.is_zipfile` branch + member-locate + streamed copy, mirroring `_genotype_member` / `land` at [scripts/ingest/dna.py:49,92-99](../../scripts/ingest/dna.py#L49) [VERIFIED]), then runs its existing `iterparse` streamed read. The server (`ADR-0013-T4`) routes the uploaded zip into `ingest.run` via that now-zip-aware adapter and adds NO extraction logic — matching the ADR-0013 `complements ADR-0012` edge ("the zip-member extraction lives in the ingest/adapter layer per that amendment, so this server still adds no extraction logic") and the ADR-0012 amendment ("the adapter accepting a zip"). An Apple Health zip is therefore ingestable from BOTH `python -m scripts.ingest` and the web upload. The decompression-size ceiling (bead `07f6`) is operator-owned (local self-DoS, no egress) and tracked, not resolved here. |
| Egress guard proof | Constraint (ADR-0013 / ADR-0001) | The new network surface is proven egress-free (sockets blocked) by TEST; the production server is egress-free by construction | In scope (Wave A) | `ADR-0013-T5` is the egress **TEST**: it builds a fixture upload request, runs the handler's upload→ingest→re-render dispatch over a `tmp_path` store inside a zero-arg closure, passes that closure to `egress_guard.run`, and asserts truthy (sockets blocked; the store-write side-effects persist on disk so the assertion is meaningful). The guard FORKS a child that `os._exit`s and returns only a bool ([scripts/guard/egress_guard.py:82,102-119](../../scripts/guard/egress_guard.py#L82) [VERIFIED]), so it CANNOT wrap the production request (the re-rendered response produced in the child never returns to the parent handler) — it is the test harness, not a per-request production wrapper. The production server is egress-free BY CONSTRUCTION (it makes no outbound calls — proven additionally by a grep test that `scripts/serve/` imports no `socket.create_connection`/`urllib`/http client). The loopback bind is a static assertion over the server's bind call. The guard is OS-level and already audited at `ADR-0001-T1`; this build CONSUMES it as the test harness, adding no new egress control. |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/serve/__init__.py` | Create | Package marker for the loopback intake server. |
| `scripts/serve/__main__.py` | Create | `python -m scripts.serve` entry: bind `127.0.0.1` only, start the server under the egress guard, operator-stop on signal/exit; fail-loud on a non-loopback bind or a port collision. |
| `scripts/serve/server.py` | Create | The stdlib `http.server` handler: GET `/` serves the wizard (re-rendered via `generate.run('intake')`); POST `/upload` reads the multipart body, stages to temp, dispatches into `ingest.run` / `dna.land` (the healthkit adapter accepts the zip directly), re-renders. Loopback-origin rejection. |
| `scripts/serve/multipart.py` | Create | A stdlib multipart/form-data reader that streams each uploaded part to a server-chosen temp path (bounded copy with a byte ceiling), sanitizing the client filename so a `../` traversal cannot escape the temp dir. |
| `scripts/ingest/adapters/healthkit.py` | Modify | Extend `read_readings` to accept an Apple Health export `.zip`: detect a zip (`zipfile.is_zipfile`), extract the single `*/export.xml` member (mirroring `dna.land`'s `_genotype_member`/zip-copy at [scripts/ingest/dna.py:49,92-99](../../scripts/ingest/dna.py#L49)), then run the existing `iterparse` streamed read. A pre-extracted `export.xml` reads as today. This is the ONE adapter change; `ingest.py`/`adapter.py`/`scheduler.py` stay byte-unchanged (ADR-0003-T2 protects the shared routine, not the adapters). |
| `scripts/serve/route.py` | Create | The upload-routing seam: map a staged upload to a source (reusing the CLI's `_EXT_SOURCE` / `_detect_source` logic, content-disambiguating a `.zip`: Apple-Health-export shape → healthkit; 23andMe shape → dna) and dispatch into `ingest.run` (wearable; the healthkit adapter accepts the zip) or `dna.land` (DNA); never edits the shared ingest/adapter/scheduler routines. |
| `scripts/serve/capture.py` | Create | The web-form capture-persistence path (ADR-0014): route each captured field by data class — wired de-identified → `store.append(token, reading, source:"intake")`; record-only → `vault/scaffold/filled/`; curated `rx-interaction-classes` → store item from supplied class tokens. Classifies every field against `SUMMARY_FIELD_SET` before writing. |
| `tests/serve/test_server.py` | Create | GET `/` serves the wizard, POST `/upload` happy path (export.xml → ingest → re-render), loopback-origin rejection, intake-only (no artifact-serving route). |
| `tests/serve/test_bind.py` | Create | Structural assertion: the server binds `127.0.0.1` and never `0.0.0.0`/`""`; port-collision fail-loud behavior. |
| `tests/serve/test_multipart.py` | Create | Multipart streaming to temp; path-traversal filename (`../../x`) writes only inside the temp dir; oversize-upload byte-ceiling enforcement. |
| `tests/ingest/test_adapters.py` | Modify | Add the zip-aware healthkit tests: `read_readings` on a synthetic Apple-Health zip yields the SAME readings as on the extracted `export.xml`; a non-zip / non-xml fails loud. (Extends the existing adapter suite that carries the 0-shared-routine-edit `numstat` gate for `ingest.py`/`adapter.py`.) |
| `tests/serve/test_route.py` | Create | A staged Apple-Health `.zip` (or `export.xml`) routes into `ingest.run` via the zip-aware healthkit adapter; a staged 23andMe DNA `.zip` routes into `dna.land`; the shared `ingest.py`/`adapter.py`/`scheduler.py` are byte-unchanged (`git diff --numstat` = 0; healthkit.py is expected to change). |
| `tests/serve/test_serve_no_egress.py` | Create | The egress TEST: a fixture upload request's upload→ingest→re-render dispatch, run over a `tmp_path` store inside a zero-arg closure passed to `egress_guard.run`, observes 0 outbound calls (truthy; store-write side-effects persist on disk); injecting a synthetic outbound call drives the guard to FAIL (failing-capable); a grep test asserts `scripts/serve/` imports no `socket.create_connection`/`urllib`/http client (production egress-free by construction). |
| `tests/serve/test_capture.py` | Create | Per-wired-field round-trip (capture → `store.read` returns the token item tagged `source:"intake"` → `summarize` returns it); record-only fields land ONLY under `vault/scaffold/filled/`; a fresh-clone PII scan returns 0 operator tokens in tracked files; raw PII into a `SUMMARY_FIELD_SET` item is rejected by `summarize`. |
| `tests/serve/test_capture_store_adversarial.py` | Create | The store-adversarial battery for the capture write path (cross-stream collision, same-timepoint dedupe, dedupe-key boundary, mutation) per `docs/checklists/store-adversarial-tests.md`. |

## Tasks

### ADR-0013-T1: Loopback-Only HTTP Server Skeleton + `python -m scripts.serve` Entry

**Status:** TODO
**ADR Source:** ADR-0013, Decision (operator-started, ephemeral, loopback-only `python -m scripts.serve`, binds `127.0.0.1` only, operator-started/-stopped, not a daemon); ADR-0013, Validation Approach (Confirmation 1: bind is `127.0.0.1` never `0.0.0.0`/`""`; Falsification 1: a non-loopback bind halts release); ADR-0013, Open Questions (OQ-2: default port + collision behavior)
**Files to create/modify:**
- `scripts/serve/__init__.py` -- package marker
- `scripts/serve/__main__.py` -- `python -m scripts.serve` entry: loopback bind, operator-start/-stop, fail-loud on a non-loopback bind / port collision
- `scripts/serve/server.py` -- the `http.server` request-handler skeleton (GET `/` route stub returning the wizard; the POST route lands in `ADR-0013-T4`)
- `tests/serve/test_server.py` -- GET `/` serves the wizard HTML
- `tests/serve/test_bind.py` -- bind is `127.0.0.1`, never `0.0.0.0`/`""`; port-collision fail-loud

**Acceptance Criteria:**
1. `python -m scripts.serve` (invoked in-process via its `main`) constructs the server bound to `127.0.0.1` and a fixed default port; a structural assertion over the bind call finds 0 binds to `0.0.0.0`, `""`, or any routable interface (ADR-0013 Confirmation 1).
2. A GET `/` against the running handler returns HTTP 200 and a body that IS the intake wizard HTML (the `generate.run('intake')` / `intake.render` output — the test asserts the wizard's title string is present), not a directory listing or a generic page.
3. When the default port is already bound, `python -m scripts.serve` exits non-zero with a fail-loud message naming the collision and the alternate-port instruction (ADR-0013 OQ-2 collision behavior), and binds nothing — verified by pre-binding the port and asserting the non-zero exit + the stated message.
4. The server reads no stdin and is operator-stopped (a stop signal / context exit shuts the listener cleanly), verified by starting and stopping it in-process with stdin closed.
5. `pytest tests/serve/test_server.py tests/serve/test_bind.py` passes.

**Risk Mitigations:** ADR-0013 Negative-1 (a listening socket is a new local leak surface; must be loopback-bound by test) — criterion 1 is the structural loopback-bind assertion that fails on any non-loopback bind. ADR-0013 Negative-3 (an operator who walks away holds an open port) — criterion 4 enforces the clean operator-stop lifecycle (not a daemon).
**Dependencies:** None (entry point for this spec). Blocks: ADR-0013-T2, ADR-0013-T4.

---

### ADR-0013-T2: Multipart Reader + Temp Staging (Traversal-Safe, Oversize-Bounded)

**Status:** TODO
**ADR Source:** ADR-0013, Decision (parses uploads locally, writes only to existing local store/dropzones); ADR-0013, Validation Approach (Confirmation 3: a client-supplied `filename=../../x` is written only inside the server-chosen temp path); ADR-0012 amendment, Consequence (the `07f6` decompression-size concern — a streamed copy with a byte ceiling)
**Files to create/modify:**
- `scripts/serve/multipart.py` -- stream each multipart/form-data part to a server-chosen temp path; sanitize the client filename; bounded copy with a byte ceiling
- `tests/serve/test_multipart.py` -- streaming to temp; `../../x` writes only inside the temp dir; oversize byte-ceiling enforcement

**Acceptance Criteria:**
1. A multipart/form-data body carrying one file part is streamed to a server-chosen path UNDER a server-owned temp directory, and `multipart`'s returned staged path resolves to a location inside that temp dir (`Path(staged).resolve()` is within the temp root), verified by uploading a body and asserting the staged file exists inside the temp root.
2. A client filename of `../../x` (or `..\\..\\x`, or an absolute `/etc/x`) lands ONLY inside the server-chosen temp directory — `Path(staged).resolve()` is still within the temp root and 0 files are written outside it (ADR-0013 Confirmation 3), verified by asserting the resolved staged path is within the temp root and the traversal target path does not exist.
3. An upload whose body exceeds the configured byte ceiling is refused (raises / truncates-and-raises) before the full body is written, and the partial temp file is removed — verified by uploading an over-ceiling body and asserting the refusal + 0 residual oversize temp file (the `07f6` self-DoS mitigation surface).
4. The reader streams (does not read the whole body into memory at once): the staging copy is chunked with the byte ceiling applied per-chunk, verified by `rg` finding the chunked-copy loop (0 single-shot full-body reads of the file part).
5. `pytest tests/serve/test_multipart.py` passes.

**Risk Mitigations:** ADR-0013 Confirmation 3 / Negative-1 (a path-traversal filename must not escape the temp path) — criterion 2 is the traversal-containment assertion. ADR-0012 amendment `07f6` (an unbounded copy can OOM / amplify) — criteria 3, 4 put a byte ceiling on the streamed copy.
**Dependencies:** ADR-0013-T1 (the server the reader stages uploads for). Blocks: ADR-0013-T3, ADR-0013-T4.

---

### ADR-0013-T3: Zip-Aware Healthkit Adapter — `read_readings` Accepts an Apple Health Zip (Mirrors `dna.land`)

**Status:** TODO
**ADR Source:** ADR-0012, Amendment 2026-06-21 (the Apple Health ingest path accepts the export zip and extracts `export.xml` itself — "a small helper in the ingest path, or the adapter accepting a zip" — mirroring `dna.land`'s zip-member extraction; the streamed `iterparse` read is unchanged); ADR-0013, Related Decisions (ADR-0012 `complements`: "the zip-member extraction lives in the ingest/adapter layer per that amendment, so this server still adds no extraction logic"); ADR-0003-T2 0-shared-routine-edit invariant (it protects `ingest.py`/`adapter.py`/`scheduler.py` — NOT the adapters, which it explicitly permits to change)
**Files to create/modify:**
- `scripts/ingest/adapters/healthkit.py` -- extend `read_readings(self, export_file)` ([scripts/ingest/adapters/healthkit.py:67-83](../../scripts/ingest/adapters/healthkit.py#L67)) to detect a zip (`zipfile.is_zipfile`), extract the single `*/export.xml` member (mirroring `_genotype_member` + the `land` zip-copy at [scripts/ingest/dna.py:49,92-99](../../scripts/ingest/dna.py#L49)), then run the existing `iterparse` streamed read over the extracted xml; a non-zip `export.xml` reads as today
- `tests/ingest/test_adapters.py` -- `read_readings` on a synthetic Apple-Health zip yields the SAME readings as on the extracted `export.xml`; a non-zip / non-xml fails loud (extends the existing adapter suite)

**Acceptance Criteria:**
1. `read_readings` on a synthetic Apple Health export `.zip` (a single `*/export.xml` member + noise members) yields the SAME readings as `read_readings` on the extracted `export.xml`, verified by building both fixtures and asserting equal reading lists — the adapter detects the zip (`zipfile.is_zipfile`), locates the `*/export.xml` member, streams it out (the same member-locate → `zf.open` stream-copy shape `dna.land` uses at [scripts/ingest/dna.py:92-99](../../scripts/ingest/dna.py#L92) [VERIFIED]), then runs its existing `iterparse` read.
2. A non-zip raw `export.xml` reads exactly as today (the existing `iterparse` path), verified by the existing healthkit fixture still yielding its readings unchanged (the `dna.land` raw-`.txt` passthrough analog).
3. A zip with NO `*/export.xml` member, and a non-zip non-xml file, each fail loud (raise a stated error), never silently importing nothing — verified by feeding both and asserting the raise (the `_genotype_member` fail-loud analog at [scripts/ingest/dna.py:67](../../scripts/ingest/dna.py#L67) [VERIFIED] + the existing fail-loud-on-malformed posture).
4. The inner-xml extraction is a streamed copy (the extracted xml can be hundreds of MB; the copy mirrors `dna.land`'s `shutil.copyfileobj` stream-copy at [scripts/ingest/dna.py:96-97](../../scripts/ingest/dna.py#L96), not a single-shot read), verified by `rg` finding the streamed copy in `healthkit.py` (0 single-shot full-member `.read()` of the member). The decompression-size ceiling (bead `07f6`) extends to this path and is tracked, not resolved here.
5. The SHARED routine is byte-unchanged — `ingest.py`, `adapter.py`, and `scheduler.py` carry 0 changed lines, verified by `git diff --numstat <pre-task> -- scripts/ingest/ingest.py scripts/ingest/adapter.py scripts/ingest/scheduler.py` reporting 0 (ADR-0003-T2: the 0-shared-routine-edit invariant protects these three; `healthkit.py` is an ADAPTER and is EXPECTED to change — it is NOT in the numstat set).
6. An Apple Health zip ingests via BOTH the CLI (`python -m scripts.ingest <zip> --source healthkit`) and (later, `ADR-0013-T4`) the server — verified by the CLI path landing the zip's inner readings in a temp store (the dual-entry-point ingestability the adapter-layer location delivers; a serve-layer extraction would leave the CLI needing a manual unzip).
7. `pytest tests/ingest/test_adapters.py` passes.

**Risk Mitigations:** ADR-0012 amendment (a browser-uploaded Apple Health zip cannot reach `ingest.run` without the extraction) — criteria 1-3 build the zip-awareness in the adapter, mirroring `dna.land`. ADR-0012 `07f6` (the hundreds-of-MB extracted xml) — criterion 4 streams the copy. ADR-0003-T2 0-shared-routine-edit invariant — criterion 5 keeps `ingest.py`/`adapter.py`/`scheduler.py` byte-unchanged (the adapter is correctly NOT in that set). Dual-entry-point ingestability — criterion 6.
**Dependencies:** None new beyond the live healthkit adapter + `dna.land` precedent (both present). Blocks: ADR-0013-T4.

---

### ADR-0013-T4: Upload Route → Ingest Dispatch + Intake Re-Render (Intake-Only)

**Status:** TODO
**ADR Source:** ADR-0013, Decision (POST uploads route into the existing `ingest.run` / `dna.land` seam; re-render the wizard; serves NO generated artifact live — intake-only); ADR-0013, Validation Approach (Falsification 3: serving a generated artifact re-crosses the artifact-delivery axis ADR-0004/NG-4 prohibit); ADR-0003 0-shared-routine-edit invariant
**Files to create/modify:**
- `scripts/serve/route.py` -- map a staged upload to a source (reuse `_EXT_SOURCE` / `_detect_source`, content-disambiguating a `.zip`: Apple-Health-export shape → healthkit; 23andMe shape → dna) and dispatch into `ingest.run` (wearable; the zip-aware healthkit adapter from `ADR-0013-T3` accepts the zip directly) or `dna.land` (DNA); the route does NOT extract
- `scripts/serve/server.py` -- wire the POST `/upload` handler: stage (T2) → route (this task) → re-render via `generate.run('intake')`
- `tests/serve/test_server.py` -- POST `/upload` happy path (export.xml → ingest → re-render); loopback-origin rejection; intake-only (no artifact-serving route)
- `tests/serve/test_route.py` -- a staged `export.xml` routes into `ingest.run` (healthkit); a staged DNA `.zip` routes into `dna.land`; the shared routines byte-unchanged

**Acceptance Criteria:**
1. A POST `/upload` of a synthetic `export.xml` lands its readings in the store via the UNCHANGED `ingest.run(adapter, export_file, root)` ([scripts/ingest/ingest.py:39](../../scripts/ingest/ingest.py#L39) [VERIFIED]) and the response re-renders the wizard reflecting the new load-state (the re-rendered wizard's wearable card shows the loaded count) — verified by `store.read` returning the imported readings AND the response body carrying the updated wizard.
2. A POST `/upload` of a synthetic DNA `.zip` lands it in the gitignored DNA dropzone via the UNCHANGED `dna.land(source_file, dna_root)` ([scripts/ingest/dna.py:71](../../scripts/ingest/dna.py#L71) [VERIFIED]) — verified by the landed file appearing under the dna_root and the response re-rendering the wizard.
3. A POST `/upload` of an Apple Health `.zip` routes the zip (NOT a pre-extracted xml) into `ingest.run` via the zip-aware `healthkit` adapter (`ADR-0013-T3`), which extracts `export.xml` internally — verified by `store.read` returning the healthkit-mapped readings from the zip's inner xml. The route adds NO extraction logic.
4. The source-detection logic REUSES the CLI's `_EXT_SOURCE` / `_detect_source` mapping ([scripts/ingest/__main__.py:39,42](../../scripts/ingest/__main__.py#L39) [VERIFIED]) — `route.py` references that map / function rather than re-deriving the extension→source rules, verified by `rg` finding the import / call (0 second extension-map definitions in `scripts/serve/`). NOTE: an Apple-Health zip routes to `healthkit` (whose adapter accepts the zip), distinct from the CLI's `.zip → dna` default — `route.py` branches a zip on its content (Apple-Health-export shape → healthkit; 23andMe shape → dna), the one extension the website disambiguates by content.
5. The server serves NO generated artifact (dashboard/report) live — there is 0 route returning a dashboard/report artifact; only GET `/` (wizard) and POST `/upload` (ingest + re-render) exist (ADR-0013 Falsification 3) — verified by asserting a GET for a dashboard/report path returns 404 (no artifact route) and `rg` finds 0 `dashboard`/`report` artifact-serving route in `scripts/serve/`.
6. The shared ingest routines are byte-unchanged BY THIS TASK: `git diff --numstat <pre-task> -- scripts/ingest/ingest.py scripts/ingest/adapter.py scripts/ingest/scheduler.py scripts/ingest/dna.py` reports 0 changed lines (the route is a new front door, adds 0 adapter / 0 store-write / 0 extraction logic — ADR-0013, ADR-0003 invariant). NOTE: `healthkit.py` is deliberately NOT in this set — it is an adapter that changed in `ADR-0013-T3` to accept the zip; the route adds nothing to it.
7. `pytest tests/serve/test_server.py tests/serve/test_route.py` passes.

**Risk Mitigations:** ADR-0013 Falsification 3 (re-crossing onto the artifact-delivery axis) — criterion 5 asserts intake-only (no dashboard/report route). ADR-0003 0-shared-routine-edit / ADR-0013 "new front door" — criterion 6 holds the shared routines byte-unchanged. ADR-0013 Decision (reuse, not re-implement) — criterion 4 reuses the CLI source-detection.
**Dependencies:** ADR-0013-T1 (the server skeleton + POST route), ADR-0013-T2 (the staged upload), ADR-0013-T3 (the Apple-zip extraction). Blocks: ADR-0013-T5, ADR-0014-T1.

---

### ADR-0013-T5: Egress TEST Over the Request-Handler Dispatch (0 Outbound, Egress-Free by Construction)

**Status:** TODO
**ADR Source:** ADR-0013, Decision (zero outbound network calls); ADR-0013, Validation Approach (Confirmation 2: the upload→ingest→re-render path makes 0 outbound calls under the egress guard with sockets blocked; Falsification 2: ≥1 outbound connection halts release); ADR-0001 "0 outbound calls carrying store content"
**Files to create/modify:**
- `tests/serve/test_serve_no_egress.py` -- the egress TEST: build a fixture upload request, run the handler's upload→ingest→re-render dispatch over a `tmp_path` store inside a zero-arg closure, pass the closure to `egress_guard.run` ([scripts/guard/egress_guard.py:82](../../scripts/guard/egress_guard.py#L82) [VERIFIED]) and assert truthy (sockets blocked; store-write side-effects persist on disk so the assertion is meaningful); an injected outbound call drives the guard to FAIL (failing-capable); a grep test asserts `scripts/serve/` imports no outbound HTTP client (production egress-free by construction)

**Why this is a TEST, not a production wrapper.** `egress_guard.run` FORKS a child that applies the OS sandbox, runs the operation, and `os._exit`s with a status code — `run` returns only a bool to the parent ([scripts/guard/egress_guard.py:102-119](../../scripts/guard/egress_guard.py#L102) [VERIFIED]). The re-rendered HTML response produced INSIDE the child therefore never returns to the parent request handler, so the guard CANNOT wrap the production request (which must return a response). The guard is the test harness; the production server is egress-free by construction (it makes no outbound calls).

**Acceptance Criteria:**
1. A fixture upload request's upload→ingest→re-render dispatch (a POST `/upload` of a synthetic `export.xml`, run over a `tmp_path` store) wrapped in ONE zero-arg closure passed to `egress_guard.run` returns truthy (0 outbound network calls observed across the whole dispatch) (ADR-0013 Confirmation 2) — the closure runs the production handler's dispatch path, not a no-op, and the store-write side-effects persist on disk (asserted) so the truthy result is meaningful, not vacuous.
2. Injecting a synthetic outbound call into the dispatch closure drives `egress_guard.run` to return falsy (FAIL) — the guard is failing-capable over the request code path (subprocess/async-spawned calls included, since the guard is OS-level) (ADR-0013 Falsification 2) — verified by wrapping a dispatch that makes one outbound call and asserting the falsy result.
3. The PRODUCTION server is egress-free by construction — `rg` over `scripts/serve/` finds 0 outbound HTTP clients (`socket.create_connection`, `urllib.request`, `http.client`, `requests`, `httpx`), verified by the grep test asserting 0 hits. (The guard is NOT wrapped around the production request handler — it cannot be, per "Why this is a TEST"; the re-render re-reads the disk store in the PARENT after the test-guarded ingest.)
4. `pytest tests/serve/test_serve_no_egress.py` passes.

**Risk Mitigations:** ADR-0013 Negative-1 (the new listening socket is a leak surface; must be proven egress-free by test) — criteria 1-2 are the failing-capable 0-egress proof over the request dispatch, run as a test. ADR-0001 "0 outbound calls carrying store content" — criterion 3 realizes that boundary on the server surface (egress-free by construction, grep-proven).
**Dependencies:** ADR-0013-T4 (the request dispatch the egress test exercises). Blocks: (Wave B's capture path runs the same egress-free dispatch).

---

### ADR-0014-T1: Web-Form Capture — By-Data-Class Persistence (Steps 2-6, Field-Map-Grounded)

**Status:** TODO
**ADR Source:** ADR-0014, Decision (captured input persisted by data class: de-identified `SUMMARY_FIELD_SET`-token fields to the store via `store.append` tagged `source:"intake"`; raw/rich to gitignored `vault/scaffold/filled/`; raw PII never into a `SUMMARY_FIELD_SET` item; reaches specialists only via `router.summarize`); ADR-0014, Validation Approach (Confirmation 1: round-trip per wired field; Confirmation 2: raw input lands ONLY under gitignored paths; Falsification 1: raw PII in a field-set item must raise)
**Files to create/modify:**
- `scripts/serve/capture.py` -- route each captured field by data class per the Field Map: wired de-identified → `store.append(token, reading, source:"intake")`; record-only → `vault/scaffold/filled/`; curated `rx-interaction-classes` → store item from supplied class tokens. Classify every field against `SUMMARY_FIELD_SET` before writing.
- `scripts/serve/server.py` -- wire the POST form-submit handler (Steps 2-6 + the Step-6 `/generate-plan` handoff) to `capture.py`
- `tests/serve/test_capture.py` -- per-wired-field round-trip; record-only fields land ONLY under `vault/scaffold/filled/`; fresh-clone PII scan returns 0 tracked tokens; raw PII into a field-set item rejected by `summarize`
- `tests/serve/test_capture_store_adversarial.py` -- the store-adversarial battery for the capture write path

**Acceptance Criteria:**
1. Each WIRED de-identified field (Step-2 `goal-domains`/`goal-targets`/`goal-priority-order`/`hard-limits`; Step-3 `recovery-status-band`; the curated `rx-interaction-classes`) captured through the form is written to a store item named EXACTLY its `SUMMARY_FIELD_SET` token, tagged `source:"intake"`, and `summarize` returns it under the token name — verified by a round-trip test PER wired field: capture → `store.read(token)` returns the reading tagged `source:"intake"` → `summarize(store_read)` returns it under the token (ADR-0014 Confirmation 1; 0 wired fields missing from the summary). Every token is asserted ∈ `SUMMARY_FIELD_SET` ([scripts/plan/router.py:18-36](../../scripts/plan/router.py#L18) [VERIFIED]).
2. RECORD-ONLY fields (Step-3 training detail, all Step-4 nutrition, the raw Step-5 supplement/peptide names) land ONLY under `vault/scaffold/filled/` and NEVER into a `SUMMARY_FIELD_SET` store item — verified by capturing them and asserting (a) the gitignored scaffold file holds them AND (b) `store.read(<any SUMMARY_FIELD_SET token>)` does NOT contain a record-only value (the negative-placement assertion). The capture surface labels them honestly as record/future-use only.
3. A fresh-clone tracked-file PII scan returns 0 operator tokens in any tracked file after a full capture session — verified by running `pii_scan.scan` over the tracked tree post-capture and asserting 0 hits (ADR-0014 Confirmation 2; identical to ADR-0005 NFR-2).
4. Writing raw PII into a `SUMMARY_FIELD_SET` store item is rejected — `summarize`'s PII gate raises on a raw-PII value in a field-set item — verified by attempting a raw value into a field-set token and asserting the raise (ADR-0014 Falsification 1; [scripts/plan/router.py:352,470](../../scripts/plan/router.py#L352) [VERIFIED]).
5. The Step-6 "Save & open plan generation" submit is a HANDOFF to `/generate-plan` (NOT an in-app generate) — the handler performs 0 in-app plan generation and routes to the `/generate-plan` entry, verified by asserting the submit triggers the handoff and `rg` finds 0 `assemble`/plan-generation call in `scripts/serve/`.
6. The curated `rx-interaction-classes` store item is written ONLY from supplied de-identified class tokens, never derived in code from raw drug names — verified by `rg` finding 0 raw-name→class lookup in `scripts/serve/` and the capture writing `rx-interaction-classes` only when class tokens are supplied (ADR-0014 OQ-2; [scripts/plan/router.py:137-176](../../scripts/plan/router.py#L137) [VERIFIED]).
7. The capture write path satisfies the store-adversarial battery (`docs/checklists/store-adversarial-tests.md`): cross-stream namespace collision (a capture read for token X never returns token Y's value), same-timepoint dedupe (two distinct captures at one timepoint both persist; an identical re-capture is idempotent), dedupe-key boundary (the `(item, timepoint, source)` identity, value excluded), and a mutation test that goes RED when the keying/dedupe is deliberately broken — verified by `tests/serve/test_capture_store_adversarial.py` covering all four, category 4 observed RED.
8. `pytest tests/serve/test_capture.py tests/serve/test_capture_store_adversarial.py` passes.

**Risk Mitigations:** ADR-0014 Negative-1 (the first automated scaffold-writer; a capture bug could mis-route raw PII) — criteria 2, 3, 4 are the two-surface + fresh-clone-scan + `summarize`-gate-raises defense. ADR-0014 Negative-2 (nutrition + supplement stack have no de-identified consumer) — criterion 2 captures them record-only, 0 `SUMMARY_FIELD_SET` flow. ADR-0014 Negative-3 (per-field classification discipline) — criterion 1 asserts every wired token ∈ `SUMMARY_FIELD_SET`. Store-surface mandate (`pka`) — criterion 7 is the adversarial battery.
**Dependencies:** ADR-0013-T4 (the server's POST handler the form submits to), ADR-0013-T5 (the egress-free request dispatch — proven by test — the capture write runs through). Store substrate (`store.append`, `keying.py`, `router.summarize`, `pii_scan.scan`) is a prior-wave prerequisite (verified present).

---

## Dependency Map

```
ADR-0013-T1 --> ADR-0013-T2   (the server the multipart reader stages uploads for)
ADR-0013-T1 --> ADR-0013-T4   (the server skeleton the POST route wires into)
ADR-0013-T2 --> ADR-0013-T3   (the temp-staging + byte ceiling the Apple-zip extraction reuses)
ADR-0013-T2 --> ADR-0013-T4   (the staged upload the route dispatches)
ADR-0013-T3 --> ADR-0013-T4   (the Apple-zip extraction the route calls before healthkit routing)
ADR-0013-T4 --> ADR-0013-T5   (the request dispatch the egress test exercises)
ADR-0013-T4 --> ADR-0014-T1   (the POST handler the capture form submits to)
ADR-0013-T5 --> ADR-0014-T1   (the egress-free request dispatch — proven by test — the capture write runs through)
```

Entry points (no dependencies in this spec): ADR-0013-T1

Topological order (Kahn parallel groups):
1. **Group 1 (entry point):** ADR-0013-T1
2. **Group 2:** ADR-0013-T2 (after ADR-0013-T1)
3. **Group 3:** ADR-0013-T3 (after ADR-0013-T2)
4. **Group 4:** ADR-0013-T4 (after ADR-0013-T1, ADR-0013-T2, ADR-0013-T3)
5. **Group 5:** ADR-0013-T5 (after ADR-0013-T4)
6. **Group 6:** ADR-0014-T1 (after ADR-0013-T4, ADR-0013-T5)

Critical path: ADR-0013-T1 → ADR-0013-T2 → ADR-0013-T3 → ADR-0013-T4 → ADR-0013-T5 → ADR-0014-T1

No cycles (6 groups, every edge points from an earlier group to a later group; Kahn drains all 6 nodes).

**Wave grouping for the build plan:** Wave A = {ADR-0013-T1..T5} (the upload server, the more-foundational transport + the zip-aware healthkit adapter + the egress proof). Wave B = {ADR-0014-T1} (the interactive wizard forms + the capture persistence + the store-adversarial battery, depending on Wave A's POST handler + egress-free dispatch).

## Test Strategy

### Unit Tests
- **Scope:** `scripts/serve/__main__.py`, `scripts/serve/server.py`, `scripts/serve/multipart.py`, `scripts/serve/route.py`, `scripts/serve/capture.py`, and the zip-aware extension of `scripts/ingest/adapters/healthkit.py`.
- **Approach:** `pytest` against the in-process handler (no live socket needed for most cases — construct the handler and call its method, or run it on an ephemeral loopback port in a fixture); a temp `vault/store/` + temp dropzone roots; synthetic `export.xml` / Apple-Health-zip / DNA-zip fixtures; a temp `vault/scaffold/filled/` root for the capture tests; planted-token fixtures for the PII scan.
- **Criteria covered:** ADR-0013-T1 1-5; ADR-0013-T2 1-5; ADR-0013-T3 1-7; ADR-0013-T4 1-7; ADR-0013-T5 1-4; ADR-0014-T1 1-8.

### Integration Tests
- **Scope:** the cross-task paths — (a) the full upload→stage→ingest (zip-aware healthkit adapter)→re-render request path; (b) the egress TEST running the request dispatch inside `egress_guard.run` (sockets blocked) + the grep proof that `scripts/serve/` is egress-free by construction; (c) the capture round-trip (form → store item → `summarize`); (d) the fresh-clone tracked-file PII scan after a capture session; (e) the `git diff --numstat` 0-shared-routine-edit proofs on `ingest.py`/`adapter.py`/`scheduler.py` (ADR-0013-T3 crit 5, ADR-0013-T4 crit 6).
- **Approach:** run the server on an ephemeral loopback port in a fixture, POST synthetic uploads, assert store/dropzone state + the re-rendered wizard; run the egress guard over the same dispatch; run `pii_scan.scan` / `git diff --numstat` against a scratch worktree.
- **Criteria covered:** ADR-0013-T4 1-3, 6; ADR-0013-T5 1-2; ADR-0014-T1 1-3.

### Risk-Specific Tests
- **ADR-0013 Negative-1 (new socket leak surface):** the loopback-bind structural assertion (ADR-0013-T1 crit 1) + the failing-capable egress guard (ADR-0013-T5 crit 2) + the traversal-containment assertion (ADR-0013-T2 crit 2).
- **ADR-0013 Falsification 3 (re-crossing the artifact-delivery axis):** the intake-only assertion — no dashboard/report route, GET for an artifact path 404s (ADR-0013-T4 crit 5).
- **ADR-0012 amendment `07f6` (decompression-size self-DoS):** the byte-ceiling streamed copy (ADR-0013-T2 crit 3-4, ADR-0013-T3 crit 4).
- **ADR-0003 0-shared-routine-edit:** `git diff --numstat` = 0 on `ingest.py`/`adapter.py`/`scheduler.py` (the SHARED routine; ADR-0013-T3 crit 5, ADR-0013-T4 crit 6). `dna.py` is also unedited by both tasks. `healthkit.py` is an adapter EXPECTED to change in ADR-0013-T3 (accepting the zip) — it is deliberately NOT in the numstat=0 set, per ADR-0003-T2 (the invariant protects the shared routine, not the adapters).
- **ADR-0014 Negative-1 (first automated scaffold-writer, mis-routed raw PII):** the two-surface negative-placement (ADR-0014-T1 crit 2) + the fresh-clone PII scan (crit 3) + the `summarize`-gate-raises (crit 4).
- **ADR-0014 store-surface mandate (`pka`):** the store-adversarial battery on the capture write path (ADR-0014-T1 crit 7).

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section (each cites ADR-0013/0014/0012 Decision + Validation Approach lines).
- [x] Every ADR ID in the `adrs` frontmatter has at least one task (ADR-0013: T1-T5; ADR-0014: T1; ADR-0012 amendment: ADR-0013-T3).
- [x] All ADR IDs resolve to actual ADR files on disk (ADR-0012/0013/0014 in `docs/adr/`).

### Acceptance Criteria Quality
- [x] Every task has ≥1 acceptance criterion (each has 4-8).
- [x] All criteria are binary — each cites a command, an HTTP status, a file/section condition, a `git diff --numstat`, an `rg` count, or a guard truthy/falsy result.
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient".

### File Manifest Integrity
- [x] Every task has a file manifest; every file in any task block appears in the top-level File Manifest and vice versa.
- [x] No task lists a directory instead of a specific file.
- [x] Every source file has a corresponding test file (`server.py`→`test_server.py`/`test_route.py`/`test_serve_no_egress.py`; `__main__.py`/bind→`test_bind.py`; `multipart.py`→`test_multipart.py`; the zip-aware `healthkit.py` change→`tests/ingest/test_adapters.py`; `route.py`→`test_route.py`; `capture.py`→`test_capture.py`/`test_capture_store_adversarial.py`; `__init__.py` is a package marker, no test).

### Dependency Map Integrity
- [x] No cycles (Kahn drains all 6 nodes; 6 ordered groups).
- [x] Every task ID in a Dependencies field appears as a node; every edge corresponds to a Dependencies entry; the entry point (ADR-0013-T1) has "None".

### Constraint Propagation
- [x] Loopback-only (ADR-0013 → ADR-0013-T1 crit 1); 0-egress proven by test + egress-free by construction (ADR-0001/0013 → ADR-0013-T5 crit 1-3); uploads land only in gitignored paths (ADR-0013/0014 → ADR-0013-T2 crit 2, ADR-0014-T1 crit 2-3); 0-shared-routine-edit on `ingest.py`/`adapter.py`/`scheduler.py`, the adapter (`healthkit.py`) excluded (ADR-0003 → ADR-0013-T3 crit 5, ADR-0013-T4 crit 6); intake-only / no artifact-serving (ADR-0004/NG-4 → ADR-0013-T4 crit 5); the de-identification gate (ADR-0001/0014 → ADR-0014-T1 crit 1, 4).

### Unresolved Concerns
- [x] Disposition section present (6 rows). ADR-0013 OQ-1/OQ-2, ADR-0014 OQ-1/OQ-2, the ADR-0012 amendment, the egress-guard wrap each dispositioned (Proceed / Defer / In scope).
- [x] Defer dispositions justify why deferral is safe (NG-4 wording is a doc follow-up; nutrition/supplement tokens are record-only-complete without the field-set extension).

### Risk Coverage
- [x] Risk Mitigations field on every task; every in-scope ADR negative consequence covered (ADR-0013 N1→T1+T2+T5, N3→T1; ADR-0014 N1→T1, N2→T1, N3→T1; ADR-0012 `07f6`→T2+T3; the artifact-axis falsification→T4).

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status).
- [x] No placeholder text ("TBD", "TODO: fill in", "...").
