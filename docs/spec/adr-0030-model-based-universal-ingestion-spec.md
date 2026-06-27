---
scope: "ADR-0030: route an any-format browser upload through the no-train model lane to EXTRACT structured Line-Field-Set readings, surface every extracted reading to the operator for review, and land ONLY operator-confirmed readings through the UNCHANGED store.append sink — a new universal-extraction front door onto the frozen ingest engine, mock/fixture-tested at 0 live spend"
adrs: [ADR-0030]
tier: 8
created: 2026-06-27
status: approved
---

# Spec: Model-Based Universal Ingestion — Any-Format Upload Extraction via the No-Train Lane

## Component Overview

This spec implements ADR-0030 (Model-Based Universal Ingestion). Today the ingestion path reads only a closed set of wearable/DNA export shapes: the CLI's `_EXT_SOURCE` maps four extensions to named adapters and `_detect_source` raises `SystemExit` on any other extension ([`scripts/ingest/__main__.py:39,42-50`](../../../../scripts/ingest/__main__.py)), and the website router `route_upload` dispatches only the named wearable adapters plus a `.zip` content-branch, adding "NO extraction logic" by design ([`scripts/serve/route.py:58-93`](../../../../scripts/serve/route.py)). A `.pdf`, an arbitrary `.csv`/`.json`, or a photo of a report hits the `SystemExit` dead-end. This spec builds the ADR-0030 resolution: route an unrecognized-format upload through the operator's already-authorized no-train model lane to extract structured `(item, timepoint, source, value)` readings, gate every extracted value behind operator confirmation, and write confirmed readings through the unchanged `store.append` sink.

The build is a NEW FRONT DOOR onto a frozen engine, decomposed into five tasks. **T1** adds an `extract_readings` method to the no-train model client ([`scripts/model/client.py`](../../../../scripts/model/client.py)) mirroring the live `deidentify`/`converse` methods — lazy `_client()`, runtime `key_source.resolve`, bounded retry-with-timeout, fail-closed `ModelCallError` raised `from None` ([`scripts/model/client.py:251-334`](../../../../scripts/model/client.py)). **T2** extends `route_upload` so an unrecognized-format upload routes through `extract_readings` (NOT the named adapters), returning the extracted readings WITHOUT landing them. **T3** wires the server: the `POST /upload` handler surfaces extracted readings as a JSON review payload (it does not land them), and a new `POST /confirm-extraction` route lands ONLY the operator-confirmed subset through the unchanged `store.append`, mirroring `ingest.manual_entry`/`import_csv` ([`scripts/ingest/ingest.py:61-129`](../../../../scripts/ingest/ingest.py)). **T4** lands the operator-confirm UI on the SPA `Upload Documents` surface ([`vault/design/templates/app_view.html`](../../../../vault/design/templates/app_view.html)). **T5** is the headline end-to-end proof plus the ADR-0030 falsification probes as tests.

The extraction backend is the swappable no-train client (ADR-0015), so the file→model mechanism is pinned at the SDK seam and mock-tested at 0 live spend: the no-train `messages.create` call carries the file content as a native `document`/`image`/text content block (a base64 `document` source for a PDF, a base64 `image` source for an image, plain text for a text format) and a structured-output JSON schema constrains the returned readings to the Line-Field-Set shape. The existing `_FakeAnthropic` patched-SDK harness + `_patch_backend_client` seam ([`tests/model/test_client.py:405-469`](../../../../tests/model/test_client.py)) carry every extract test with no live API and no key. The OS-level egress-guard LIVE run is OQ-1 (deferred); this spec's crown-jewel probe is the structural/mock form.

**The crown-jewel PII boundary (NFR-1, load-bearing).** ADR-0030 is the FIRST extension of the no-train lane onto the ingestion axis: it broadens the operator-data-to-no-train surface from plan-path data to whole raw uploaded FILES. The bound this spec enforces is that the ONLY egress of file content is the no-train lane — 0 file bytes to any non-no-train endpoint — preserved structurally by keeping the single model-client SDK import inside `scripts/model/` (the standing `rg` guard, [`tests/model/test_client.py:158-176`](../../../../tests/model/test_client.py) + [`tests/serve/test_serve_no_egress.py:186-200`](../../../../tests/serve/test_serve_no_egress.py)) and routing the file only into the injected `client.extract_readings`. No extracted reading lands unconfirmed (the confirm-gate probe), no extraction failure fabricates a reading (the fail-closed probe), and the raw upload is never written to a tracked path (OQ-5). The frozen ingest engine + Line-Field-Set + `store.append` sink + the `scripts/plan/*` engine (including the `deid_in` de-id boundary) are byte-unchanged (NFR-4, EXTEND-NOT-REBUILD) — the extraction is a new front door, not an engine edit.

### Pinned file→model mechanism (T1 — grounded; internals-discretionary at the wire level)

| Upload class | Content block sent on the no-train `messages.create` | Grounding |
|--------------|------------------------------------------------------|-----------|
| PDF (`application/pdf`) | `{"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": <b64>}}` | Anthropic SDK native PDF document block (claude-api skill, Files/Vision; `claude-opus-4-8`) |
| Image (`image/png`, `image/jpeg`, …) | `{"type": "image", "source": {"type": "base64", "media_type": <mime>, "data": <b64>}}` | Anthropic SDK native vision image block (claude-api skill, Vision) |
| Text (CSV/JSON/TXT) | `{"type": "text", "text": <decoded file text>}` | plain text content (no base64 needed) |
| Return-shape constraint | `output_config={"format": {"type": "json_schema", "schema": <Line-Field-Set readings array>}}` | structured outputs on `claude-opus-4-8` (claude-api skill, Structured Outputs) |

The model does the structured interpretation; the file bytes egress ONLY on this one no-train `messages.create` call. The local `pdftotext`/`marker` zero-egress pre-extraction fast-path (both present locally — [VERIFIED: `/opt/homebrew/bin/pdftotext`, `~/.local/bin/marker`]) is OQ-2, explicitly OUT of this spec (a non-goal).

## Unresolved Concerns Disposition

Source: ADR-0030 Open Questions OQ-1..OQ-5, dispositioned in [`docs/spec/.pipeline/adr-0030/dispositions.md`](dispositions.md) under the operator's autonomous build directive.

| # | Item | Disposition | Rationale / Where it lands |
|---|------|-------------|----------------------------|
| OQ-1 | The operator-present LIVE run (real key + real file + real spend) end-to-end | **Defer** | Operator-gated downstream checkpoint, not a build task. The build is mock/fixture-tested at 0 live spend; the OS-egress-guard LIVE form of the crown-jewel probe is the deferred live run. Recorded as a non-goal. |
| OQ-2 | Tier-1 deterministic format-family detectors + local `pdftotext`/`marker` zero-egress fast-path | **Defer** | Alternative A's salvageable zero-egress component; ships independently of this decision. OUT of this spec's scope (a non-goal / future fast-path ahead of the model). |
| OQ-3 | The build spec→task→execute mechanics (model→extraction call, confirm UI, retry/backoff/timeout) | **Proceed** | THIS spec resolves OQ-3 — it IS the build decomposition (T1 mechanics, T3 confirm route, T4 confirm UI). The operator-confirm-before-land + no-train-lane-only contracts hold regardless of mechanics. |
| OQ-4 | Precise no-train retention window for raw uploaded files | **Defer** | Operational/operator-owned (target 2026-06-30); does not change the decision (it accepts bounded retention, the same no-train profile as the de-id summary/conversation). Out of build scope. |
| OQ-5 | Local-residue handling of the raw uploaded file during the extraction call | **Proceed** | Load-bearing for ADR-0005 (a tracked raw-file residue breaches the PII-free trunk). The spec PINS: the raw upload is held in memory / the gitignored OS-temp `staged_path` only (`server.py` stages under `tempfile.TemporaryDirectory()`, [`scripts/serve/server.py:175-178`](../../../../scripts/serve/server.py)), discarded after extraction, NEVER a tracked write — backstopped by the `block-pii-commit`/`pre-push` hooks. A build acceptance criterion (T2 crit 5, T5 crit 6). |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/model/client.py` | Modify | T1: add `ModelClient.extract_readings(file_content, media_type)` (public validation: returns a list of Line-Field-Set readings, else `ModelCallError`) + `_ClaudeNoTrainBackend.extract_readings` (the live no-train call mirroring `deidentify`/`converse`: lazy `_client()`, runtime key, bounded retry-with-timeout, constant-message `ModelCallError from None`) + the `_extract_*` prompt/parse helpers + the `_EXTRACT_MAX_ATTEMPTS`/`_EXTRACT_TIMEOUT_SECONDS` bound constants. `converse`/`deidentify`/`author`/the existing `ModelClient` wrappers byte-unchanged. |
| `tests/model/test_client.py` | Modify | T1: the patched-SDK `extract_readings` mock tests (reuse `_FakeAnthropic`/`_patch_backend_client`): the fixture-readings round-trip + non-tautological negative control (different fixture → different readings); fail-closed typed-raise on every failure mode with 0 fabricated readings; runtime key via `key_source.resolve` inside `_client`; 0 live spend (absent SDK → `ModuleNotFoundError`); SEC no raw-file/key on the `str`/`.args`/traceback surface; the file→model document/image/text content-block mechanism; scoped-change proof. |
| `scripts/serve/route.py` | Modify | T2: extend `route_upload` with a `client=None` param and an unrecognized-format branch — when `_detect_source` would `SystemExit`, route the staged file through `client.extract_readings` (the no-train lane), reading the file from the gitignored staged path only and discarding it after the call. Return a discriminated result (a landed-source string for the named-adapter/dna path; the extracted-readings-awaiting-confirm payload for the extraction path). Adds NO store write and NO second extension→source map. |
| `tests/serve/test_route.py` | Modify | T2: the universal-extraction route test (unrecognized format → `extract_readings`, named/dna formats unchanged); the crown-jewel structural file-egress probe (the file reaches only the injected `client.extract_readings`; `scripts/serve/` imports 0 outbound client); the no-auto-land assertion (0 `store.append` over the extraction path); the OQ-5 no-tracked-write assertion; the EXTEND-NOT-REBUILD numstat probe over the frozen set. |
| `scripts/serve/server.py` | Modify | T3: the `POST /upload` handler routes `route_upload`'s discriminated result — a landed source re-renders as today; an extraction result is surfaced as a JSON review payload (mirroring `/chat`'s `_write_json`), NOT landed. Add a `POST /confirm-extraction` route that lands ONLY the operator-confirmed subset through `confirm.land_confirmed` (→ the unchanged `store.append`); add `/confirm-extraction` to the route table; thread the instance `client` into `route_upload`. Catch-and-degrade thread survival preserved. |
| `scripts/serve/confirm.py` | Create | T3: `land_confirmed(readings, *, root)` — validate each operator-confirmed reading carries the full Line-Field-Set and land it through the UNCHANGED `ingest.manual_entry`/`store.append` (the existing operator store path the confirm→land step mirrors). Makes NO model call and NO direct NDJSON write; a reading missing a Line-Field-Set field is rejected (lands nothing). The ONLY landing path for extracted readings. |
| `tests/serve/test_extract_confirm.py` | Create | T3: the confirm-gate probe (store empty before confirm; readings land only after `POST /confirm-extraction`); the no-unconfirmed-land negative control (an `/upload` extraction surfaces readings but writes 0 to the store); the confirm→land round-trip through `store.append`; a malformed/partial confirmed reading lands nothing; thread-survival on a malformed confirm body. |
| `vault/design/templates/app_view.html` | Modify | T4: the operator-confirm UI on the `Upload Documents` surface — an unrecognized-format upload posts to `/upload`, renders the returned extracted readings in a review panel (each reading with its `(item, timepoint, source, value)` + a confirm/reject control), and posts the operator-confirmed subset to `/confirm-extraction`; an honest empty/awaiting state when nothing is extracted (ADR-0009 D2, no fabricated readings shown). The inline JS reuses the existing `fetch` upload posture ([`vault/design/templates/app_view.html:738,761`](../../../../vault/design/templates/app_view.html)). |
| `tests/serve/test_app_shell.py` | Modify | T4: the rendered SPA carries the confirm-review markup + the inline JS that posts to `/upload` then `/confirm-extraction`; 0 fabricated extracted readings shown in the empty state; the confirm control posts only the operator-selected subset. |
| `tests/serve/test_universal_ingestion_e2e.py` | Create | T5: the headline E2E (synthetic fixture file → `route_upload` extract via the mock backend → surfaced readings → `POST /confirm-extraction` → `store.append`), the non-tautological headline assertion (the landed readings trace to the FIXTURE's extracted values, not a constant; failing-capable negative control), and the four ADR-0030 falsification probes composed end-to-end (crown-jewel file-egress, confirm-gate, fail-closed, OQ-5 residue) + the EXTEND-NOT-REBUILD numstat checkpoint. |

## Tasks

### ADR-0030-T1: The No-Train `extract_readings` Method (Mirror `deidentify`/`converse`; Fail-Closed; Runtime Key; Mock-Tested)

**Status:** TODO
**ADR Source:** ADR-0030, Decision (route the raw upload through the no-train model lane to extract structured `(item, timepoint, source, value)` readings; the extraction backend is the swappable ADR-0015 no-train client); ADR-0030, Validation Approach — Confirmation (extraction is mock-testable at 0 live spend: a patched SDK / injected fake backend returns a canned extraction; each extracted reading carries the full Line-Field-Set) + Backend swappability (the extraction model resolves from the ADR-0015 seam); ADR-0030, Falsification — Fail-closed-on-error (an extraction failure/timeout/malformed response raises `ModelCallError` and 0 fabricated readings are offered) + Key-never-committed scan
**Files to create/modify:**
- `scripts/model/client.py` -- Modify: add `ModelClient.extract_readings` + `_ClaudeNoTrainBackend.extract_readings` + `_extract_*` helpers + bound constants
- `tests/model/test_client.py` -- Modify: the patched-SDK `extract_readings` mock tests

**Acceptance Criteria:**
1. `ModelClient.extract_readings(file_content, media_type)` is implemented and returns a `list` of readings, each a `dict` carrying every Line-Field-Set field (`item`, `timepoint`, `source`, `value` per `keying.LINE_FIELDS`, [`scripts/store/keying.py:11`](../../../../scripts/store/keying.py)) — verified by a test with a `_FixtureBackend`/patched-SDK fixture (no live API) asserting the returned value is a `list` whose every reading's keys ⊇ the Line-Field-Set.
1a. Public fail-closed validation (the `converse`-mirror, [`scripts/model/client.py:47-60`](../../../../scripts/model/client.py)): a non-`list` return raises `ModelCallError`, AND a returned `list` carrying a reading that is missing any Line-Field-Set field raises `ModelCallError` — verified by two separate fixtures (a non-list body; a list with one field-short reading) each asserting `pytest.raises(ModelCallError)`.
2. NON-TAUTOLOGICAL (fixture-driven, not a constant): the extract returns the FIXTURE's readings — verified by a test where fixture A yields readings A and a DIFFERENT fixture B yields readings B (B ≠ A), proving the method returns the model's parse, not a hardcoded constant.
3. Fail-closed-on-error: a failed / empty / malformed / errored / timed-out extraction raises `ModelCallError` and returns 0 fabricated readings — verified by parametrizing each failure mode at the patched SDK (`None`, `{}`, a non-list body, a `RuntimeError`, a `TimeoutExpired`) and asserting `pytest.raises(ModelCallError)` with no readings returned (the `_call`/parse fail-closed boundary, [`scripts/model/client.py:105-126`](../../../../scripts/model/client.py)).
3a. Bounded retry: `_ClaudeNoTrainBackend.extract_readings` invokes `messages.create` at most `_EXTRACT_MAX_ATTEMPTS` times before the fail-closed raise — verified by a raise-on-every-attempt fixture asserting `len(fake.calls) == _EXTRACT_MAX_ATTEMPTS` (the `_DEID_MAX_ATTEMPTS` mirror, [`scripts/model/client.py:216,317`](../../../../scripts/model/client.py)).
4. Runtime key, never a tracked file: `_ClaudeNoTrainBackend.extract_readings` resolves the key at call time via `key_source.resolve()` inside `_client()` (the same path `deidentify` uses, [`scripts/model/client.py:244-249`](../../../../scripts/model/client.py)) — verified by a fake-`anthropic`-module test asserting the SDK client was handed the `key_source.resolve` sentinel as `api_key` (call-time key, no tracked-file read).
5. File→model mechanism: the no-train `messages.create` carries the file content as the media-typed content block per the pinned mechanism table — a `document` base64 source for `application/pdf`, an `image` base64 source for an image media type, a `text` block for a text media type — verified by a patched-SDK test asserting the captured `messages.create` kwargs carry the file content in the expected block shape for each media class (the raw file reaches the model prompt, as the deid prompt-carries-raw test does, [`tests/model/test_client.py:475-493`](../../../../tests/model/test_client.py)).
6. SEC constant-message (no raw-file/key on the `str`/`.args` surface): the raised `ModelCallError` carries a CONSTANT message — verified by forcing the failure path with an SDK exception EMBEDDING a synthetic raw-file token + a synthetic key token and asserting `str(exc)` and `repr(exc.args)` carry 0 occurrences of either (the SEC-01 constant-message lock, [`tests/model/test_client.py:601-633,1000-1029`](../../../../tests/model/test_client.py)).
6a. SEC severed chain (no raw-file/key on the rendered traceback): the raise is `from None` — verified, under the same embedded-token failure path, by asserting `exc.__cause__ is None` AND the fully-rendered `traceback.format_exception(...)` carries 0 occurrences of the raw-file or key token (the `from None` lock the deid/converse traceback tests pin, [`tests/model/test_client.py:635-663,1032-1060`](../../../../tests/model/test_client.py)).
7. 0 live spend: with the real `anthropic` SDK absent from `.venv`, an UNPATCHED `extract_readings` call raises `ModuleNotFoundError` BEFORE any network request — verified by an absence-gated test (`skipif` when the SDK is installed), mirroring the deid/converse 0-spend pins ([`tests/model/test_client.py:296-316,939-957`](../../../../tests/model/test_client.py)).
8. Scoped change: `git diff scripts/model/client.py` shows the only NEW method bodies are `ModelClient.extract_readings` + `_ClaudeNoTrainBackend.extract_readings` + the `_extract_*` helpers + the bound constants; `converse`, `deidentify`, `author`, every other `ModelClient.*` wrapper, and `_client` are byte-unchanged — verified by the diff touching only the added extract surface.
9. `.venv/bin/python -m pytest tests/model/test_client.py` passes.

**Risk Mitigations:** ADR-0030 Negative (the file-egress class must be proven no-train-lane-only) — crit 4,5,6 (runtime key, content-block on the one no-train call, constant fail-closed message, 0 raw/key leak). ADR-0030 fidelity-ceiling (a misread is caught later, never fabricated) — crit 3 (fail-closed, 0 fabricated readings). Public-repo key/PII leak (MEMORY) — crit 4,6,7. Non-tautological extraction — crit 2 (fixture-driven negative control).
**Dependencies:** None (entry point).

---

### ADR-0030-T2: Universal-Extraction Front Door — `route_upload` Routes an Unrecognized Format Through `extract_readings` (Not the Named Adapters; Readings Do NOT Auto-Land; OQ-5 Residue)

**Status:** TODO
**ADR Source:** ADR-0030, Decision (route a browser-uploaded file of ANY format through the no-train model lane to extract; the existing router "adds no extraction logic" is the front door this extends, ADR-0013); ADR-0030, Consequences Positive (the `.pdf`/arbitrary-CSV/JSON `SystemExit` dead-end closes); ADR-0030, Falsification — File-egress probe (the ONLY egress of file content is the no-train lane; 0 file bytes to any non-no-train endpoint) + Confirm-gate (0 model-extracted readings land in the store without an operator-confirm step); ADR-0030 OQ-5 (local-residue handling — held in memory / the gitignored staged path, discarded after extraction)
**Files to create/modify:**
- `scripts/serve/route.py` -- Modify: the `client=None` param + the unrecognized-format `extract_readings` branch + the discriminated return
- `tests/serve/test_route.py` -- Modify: the universal-route test + the crown-jewel structural probe + no-auto-land + OQ-5 + the EXTEND-NOT-REBUILD numstat probe

**Acceptance Criteria:**
1. An unrecognized-format upload (a `.pdf` / an arbitrary `.json` / an `.png` the named-adapter map does not cover) routes through `client.extract_readings`, NOT a named adapter or `dna.land` — verified by a test passing a `.pdf` staged file + a mock client recording its `extract_readings` calls, asserting `client.extract_readings` was called once with the file content and `ingest.run`/`dna.land` were not.
2. NO regression on the recognized formats: a recognized wearable extension still routes to `ingest.run(_adapter(source), …)` and a DNA `.zip`/`.txt` still routes to `dna.land`, with `client.extract_readings` NOT called — verified by re-running the existing recognized-format route assertions with the mock client injected and asserting `extract_readings` call count is 0 on those paths.
3. The extraction path does NOT auto-land: `route_upload` over an unrecognized format makes 0 `store.append` calls and 0 `dna.land` calls — it RETURNS the extracted readings (the awaiting-confirm payload), the store is empty afterward — verified by asserting `store.read_all(tmp_root) == []` after the extraction route and the return value carries the fixture's readings.
4. CROWN-JEWEL file-egress (the file reaches only the no-train lane): the file content reaches ONLY the injected `client.extract_readings` — verified by the mock client recording that it received the file bytes AND asserting no other recorded sink (`ingest.run` / `dna.land` / `store.append`) received them. (The OS-level egress-guard LIVE form is OQ-1, deferred.)
4a. CROWN-JEWEL structural guards (no outbound surface added): `route.py` imports no SDK and calls only `client.extract_readings` — verified by the standing `scripts/serve/` 0-outbound-client grep returning 0 ([`tests/serve/test_serve_no_egress.py:186-200`](../../../../tests/serve/test_serve_no_egress.py)) AND the single-model-client-import `rg` returning 0 ([`tests/model/test_client.py:158-176`](../../../../tests/model/test_client.py)).
5. OQ-5 no tracked write of the raw file: the extraction path reads the file ONLY from the gitignored staged path and writes the raw file to NO tracked path — verified by a test asserting that after the extraction route, no file under the repo's tracked tree (outside the gitignored `vault/store|dna/raw|labs/raw|scaffold/filled` prefixes, [`.gitignore:2-5`](../../../../.gitignore)) carries the synthetic raw-file token, and the staged temp file is discarded after the call.
6. EXTEND-NOT-REBUILD: `git diff --numstat <fork-point> --` over the frozen set — `scripts/ingest/ingest.py`, `scripts/ingest/adapter.py`, every `scripts/plan/*.py` (including the `deid_in.py` de-id boundary) — emits 0 rows — verified by a numstat test mirroring [`tests/serve/test_route.py:188-204`](../../../../tests/serve/test_route.py), extended with the `scripts/plan/*` paths.
7. `.venv/bin/python -m pytest tests/serve/test_route.py` passes.

**Risk Mitigations:** ADR-0030 crown-jewel egress (0 file bytes to any non-no-train endpoint) — crit 4. ADR-0030 confirm-gate precondition (no auto-land) — crit 3. ADR-0030 OQ-5 (no tracked raw-file residue) — crit 5. ADR-0030 0-shared-routine-edit / EXTEND-NOT-REBUILD (frozen engine) — crit 6. No regression on the wired adapters — crit 2.
**Dependencies:** ADR-0030-T1 (the `extract_readings` method `route_upload` dispatches to — T2 calls the surface T1 builds).

---

### ADR-0030-T3: Operator-Confirm-Before-Land — `/upload` Surfaces Extracted Readings, `POST /confirm-extraction` Lands Only the Confirmed Subset via the Unchanged `store.append`

**Status:** TODO
**ADR Source:** ADR-0030, Decision (require the operator to confirm EVERY extracted value before anything lands; write confirmed readings through the UNCHANGED `store.append` sink); ADR-0030, Consequences Positive (confirmed readings land through the unchanged single sink in the Line-Field-Set shape — no second sink, no second dedupe key) + (the operator-confirm gate keeps the store honest — no unconfirmed, possibly-misread reading becomes the operator's data); ADR-0030, Falsification — Confirm-gate probe (0 model-extracted readings land without an operator-confirm step; assert the store is empty before confirm, readings land only after); ADR-0030 constrains ADR-0009 (honest-data: no auto-landed model-extracted reading)
**Files to create/modify:**
- `scripts/serve/server.py` -- Modify: the `/upload` discriminated-result handling + the `POST /confirm-extraction` route + the route table + threading `self.client` into `route_upload`
- `scripts/serve/confirm.py` -- Create: `land_confirmed(readings, *, root)` over the unchanged `ingest.manual_entry`/`store.append`
- `tests/serve/test_extract_confirm.py` -- Create: the confirm-gate probe + no-unconfirmed-land + the confirm→land round-trip + malformed-reading rejection + thread survival

**Acceptance Criteria:**
1. CONFIRM-GATE probe (store empty before confirm): a `POST /upload` of an unrecognized-format file surfaces the extracted readings as a JSON review payload AND lands 0 of them — verified by asserting the store is empty (`store.read_all(store_root) == []`) immediately after the `/upload` response, and the response body carries the extracted readings for review.
2. Land only on confirm: a subsequent `POST /confirm-extraction` carrying the operator-confirmed subset lands EXACTLY that subset through `confirm.land_confirmed` → the unchanged `store.append` — verified by asserting each confirmed reading is readable from the store after the confirm POST AND a reading the operator did NOT confirm is absent from the store.
3. `confirm.land_confirmed` uses ONLY the unchanged sink: it lands each reading through `ingest.manual_entry`/`store.append` ([`scripts/ingest/ingest.py:36,61-80`](../../../../scripts/ingest/ingest.py)), makes 0 model call, and adds 0 direct NDJSON write and 0 second dedupe key — verified by a test that `confirm.py` imports no model client and references no keying/dedupe of its own, and a re-confirm of the same readings appends 0 duplicate lines (dedupe inherited from `store.append`).
4. A malformed/partial confirmed reading lands nothing: a confirmed reading missing a Line-Field-Set field is rejected (`ValueError` surfaced as a degraded confirm response) and 0 readings land from that request — verified by a confirm POST with an incomplete reading asserting `store.read_all == []` afterward (the uniform missing-field rejection, [`scripts/ingest/ingest.py:32-36`](../../../../scripts/ingest/ingest.py)).
5. Thread survival: a malformed `/confirm-extraction` body (non-JSON / wrong shape) is answered with a degraded JSON response and never drops the request thread or fabricates a landed reading — verified by a malformed-body POST asserting a non-2xx JSON response with 0 store writes (mirroring `/chat`'s catch-and-degrade, [`scripts/serve/server.py:243-267`](../../../../scripts/serve/server.py)).
6. The route table gains exactly `POST /confirm-extraction`: the `_LOOPBACK="127.0.0.1"` bind is byte-unchanged and the route table is `{GET /, GET /settings/key, POST /upload, POST /chat, POST /settings/key, POST /confirm-extraction}` (0 new bind/port, 0 outbound class) — verified by a served-handler test asserting `/confirm-extraction` is handled and an unknown POST still 404s, and the `scripts/serve/` 0-outbound-client grep still returns 0.
7. `.venv/bin/python -m pytest tests/serve/test_extract_confirm.py tests/serve/test_server.py` passes.

**Risk Mitigations:** ADR-0030 confirm-gate (no reading lands unconfirmed) — crit 1,2. ADR-0030 0-engine-edit / single-sink (confirmed readings land the established way, no second sink/key) — crit 3. ADR-0009 honest-data (no auto-landed reading) — crit 1. ADR-0030 fidelity-ceiling (a malformed reading lands nothing) — crit 4. Thread survival — crit 5. PII-boundary single-egress (0 new outbound class) — crit 6.
**Dependencies:** ADR-0030-T2 (the `route_upload` discriminated extraction result the `/upload` handler surfaces; the confirm route lands what T2's front door extracted).

---

### ADR-0030-T4: The SPA Operator-Confirm UI — Review Extracted Readings on `Upload Documents`, Confirm→Land (Honest Empty State; No Fabricated Readings)

**Status:** TODO
**ADR Source:** ADR-0030, Decision (the operator confirms every extracted value before anything lands) + ADR-0030 tensions-with ADR-0029 (uploads originate from the SPA `Upload Documents` screen); ADR-0030, Consequences Negative (the fidelity ceiling shifts review onto the operator — many confirmations per upload); ADR-0009 D2 honest-data (no invented number / sample content presented as data)
**Files to create/modify:**
- `vault/design/templates/app_view.html` -- Modify: the confirm-review panel on `Upload Documents` + the inline JS posting `/upload` then `/confirm-extraction`
- `tests/serve/test_app_shell.py` -- Modify: the rendered-SPA confirm-UI assertions

**Acceptance Criteria:**
1. The rendered SPA `Upload Documents` surface carries a review panel that, on an unrecognized-format upload, renders each extracted reading's `(item, timepoint, source, value)` with a per-reading confirm/reject control — verified by a test parsing the rendered SPA HTML asserting the review-panel markup + the per-reading confirm control are present (against today's `Upload Documents` surface, [`vault/design/templates/app_view.html:431,468-478`](../../../../vault/design/templates/app_view.html)).
2. The inline JS posts the upload to `/upload`, reads the returned extracted-readings payload, and posts the operator-confirmed subset to `/confirm-extraction` — verified by an `rg`/structural test over the rendered SPA asserting a `fetch('/upload'`-then-`fetch('/confirm-extraction'` flow exists in the inline JS (extending the existing `fetch('/upload'` posture, [`vault/design/templates/app_view.html:738,761`](../../../../vault/design/templates/app_view.html)).
3. HONEST empty state (ADR-0009 D2): when nothing is extracted, the review panel renders an awaiting/empty state with 0 fabricated readings — verified by rendering with an empty/absent extraction and asserting no placeholder `(item, timepoint, source, value)` row is shown as the operator's data.
4. Confirm posts only the selected subset: the confirm action sends ONLY the operator-confirmed readings (a rejected reading is omitted from the `/confirm-extraction` body) — verified by a structural test asserting the confirm handler collects the selected/confirmed rows, not the full extracted set.
5. The served SPA still passes the inline-asset render gate: `generate.run("app")` RETURNS a written path (does not raise the off-file-asset `ValueError`, [`scripts/generate/generate.py:75-91`](../../../../scripts/generate/generate.py)) — verified by a test asserting the returned path exists (the confirm UI adds no off-file asset reference).
6. `.venv/bin/python -m pytest tests/serve/test_app_shell.py` passes.

**Risk Mitigations:** ADR-0030 confirm-before-land realized on the operator surface — crit 1,2,4. ADR-0030 Negative (operator review burden) — crit 1 (per-reading confirm control). ADR-0009 D2 honest-data (no fabricated readings shown) — crit 3. ADR-0029 inline-asset gate (no off-file reference) — crit 5.
**Dependencies:** ADR-0030-T3 (the `/upload` review payload + the `/confirm-extraction` route the SPA UI consumes).

---

### ADR-0030-T5: End-to-End Universal Ingestion + the ADR-0030 Falsification Probes as Tests (Non-Tautological; Mock-Tested; 0 Live Spend)

**Status:** TODO
**ADR Source:** ADR-0030, Validation Approach — Confirmation (a reading reaches `store.append` ONLY after the operator-confirm step; the extraction call runs on the no-train lane only; new front door, 0 engine edit) + the four Falsification probes (file-egress, confirm-gate, fail-closed, key-never-committed); ADR-0030, Decision (the full author→extract→confirm→land path); the honest ceiling (a DNA report PDF yields stated findings, not raw genotype — a non-AC note)
**Files to create/modify:**
- `tests/serve/test_universal_ingestion_e2e.py` -- Create (absent today [VERIFIED `test ! -e` returns 0]): the headline E2E + the composed falsification probes; no new production code (binds the built mechanism)

**Acceptance Criteria:**
1. HEADLINE (non-tautological): a synthetic fixture file (a CSV/JSON/PDF-shaped fixture) driven through `route_upload` extract (mock backend at the ADR-0015 seam returning scripted Line-Field-Set readings) → surfaced → `POST /confirm-extraction` → `store.append` lands the confirmed readings, AND the landed store readings TRACE to the FIXTURE's extracted values (a specific fixture `(item, value)` appears in the store), NOT a constant — verified by the E2E asserting the landed readings equal the confirmed fixture subset, NEVER merely "the store is non-empty".
2. Failing-capable negative control: the SAME pipeline with an extraction returning NO usable readings (or with the operator confirming none) lands 0 readings (the honest no-data state) — verified by the negative-control case, proving crit 1 distinguishes a landed reading from the no-data state.
3. CROWN-JEWEL file-egress probe (structural/mock): across the full E2E the file content reaches ONLY the mock `extract_readings` (the no-train lane) — verified by the mock recording the file content AND the `scripts/serve/` 0-outbound-client grep + the single-model-client-import `rg` both returning 0 over the E2E path. (The OS-egress-guard LIVE run is OQ-1, deferred.)
4. CONFIRM-GATE probe: the store is empty after `/upload` and before `/confirm-extraction`; ≥1 reading lands only after the confirm POST — verified by asserting `store.read_all == []` pre-confirm and the confirmed subset present post-confirm.
5. FAIL-CLOSED probe: an extraction failure/timeout/malformed response injected at the mock seam raises `ModelCallError` upstream and surfaces 0 fabricated readings for confirmation (nothing lands) — verified by the failure-injection case asserting the store stays empty and no readings payload is offered.
6. OQ-5 residue probe: across the E2E, no tracked file (outside the gitignored dropzone prefixes) carries the synthetic raw-file token; the staged temp file is discarded after extraction — verified by the post-E2E tracked-tree scan returning 0.
7. EXTEND-NOT-REBUILD checkpoint: `git diff --numstat <fork-point> --` over `scripts/ingest/ingest.py` + `scripts/ingest/adapter.py` + every `scripts/plan/*.py` (including `deid_in.py`) emits 0 rows — verified by the numstat assertion.
8. 0 live spend: the E2E injects the mock backend at the ADR-0015 seam and makes 0 `key_source.resolve()`-gated live call; deterministic + CI-runnable with no network and no key — verified by the suite passing under `.venv/bin/python -m pytest` + a mock-injection assertion.
9. `.venv/bin/python -m pytest tests/serve/test_universal_ingestion_e2e.py` passes.

**Non-AC note (the honest ceiling, ADR-0030 Rationale).** A DNA *report* PDF yields the lab's STATED findings, not the raw genotype table `dna.land` validates — extraction recovers the readings a document states, not data it does not carry. The E2E fixtures encode stated-findings shapes; this is documented in the test module docstring, not asserted as a build criterion (it is a coverage ceiling, not a falsifiable threshold).

**Risk Mitigations:** ADR-0030 the four Falsification probes (file-egress / confirm-gate / fail-closed / OQ-5) — crit 3,4,5,6. ADR-0030 PF-class non-tautological headline (a feature plumbed but not proven to land a usable confirmed reading) — crit 1 (trace-to-fixture), crit 2 (failing-capable). EXTEND-NOT-REBUILD (frozen engine) — crit 7. Live-API coupling — crit 8 (mock-tested CI; the live run is OQ-1, operator-gated).
**Dependencies:** ADR-0030-T3 (the full backend author→extract→surface→confirm→land path the E2E exercises; the E2E drives the served `/upload`+`/confirm-extraction` routes directly, NOT T4's SPA markup).

---

## Dependency Map

```
ADR-0030-T1 --> ADR-0030-T2   (T2's front door dispatches to the extract method T1 builds)
ADR-0030-T2 --> ADR-0030-T3   (T3's /upload handler surfaces, and /confirm-extraction lands, what T2's route_upload extracts)
ADR-0030-T3 --> ADR-0030-T4   (T4's SPA UI consumes the /upload review payload + the /confirm-extraction route T3 builds)
ADR-0030-T3 --> ADR-0030-T5   (T5's headline E2E exercises the full backend upload->extract->confirm->land path T3 completes, driving the routes directly, NOT T4's markup)
```

Entry points (no inbound edges): **ADR-0030-T1**

Topological order (Kahn parallel groups):
1. **Group 1 (entry point):** ADR-0030-T1 (the no-train `extract_readings` method)
2. **Group 2:** ADR-0030-T2 (the universal-extraction front door — after T1)
3. **Group 3:** ADR-0030-T3 (the confirm-before-land server route — after T2)
4. **Group 4:** ADR-0030-T4, ADR-0030-T5 (parallel — both after T3; T4 wires the SPA confirm UI, T5 proves the backend E2E via the routes directly; T4 and T5 share no file)

Critical path: **ADR-0030-T1 → ADR-0030-T2 → ADR-0030-T3 → ADR-0030-T5** (length-4; T4 is length-4 off T3 in parallel with T5, not lengthening the path).

No cycles (Kahn drains all 5 nodes; 4 ordered groups; every edge points from an earlier group to a later group). T4 and T5 in Group 4 share no dependency edge.

**Wave-checkpoint Go/No-Go (the universal-ingestion gate):** the no-train `extract_readings` is fail-closed + mock-tested at 0 live spend (T1), an unrecognized-format upload routes through `extract_readings` not the named adapters and does NOT auto-land (T2), the `/upload` surface lands 0 readings before `/confirm-extraction` and the confirmed subset lands via the unchanged `store.append` (T3), the SPA confirm UI reviews extracted readings honestly (T4), the headline E2E lands the fixture's confirmed readings non-tautologically (T5), AND **the four ADR-0030 falsification probes are GREEN** (crown-jewel file-egress structural, confirm-gate, fail-closed, OQ-5 residue), AND the frozen surfaces are byte-unchanged: `git diff --numstat <fork-point> -- scripts/ingest/ingest.py scripts/ingest/adapter.py scripts/plan/*.py` reports 0 rows (NFR-4, the EXTEND-NOT-REBUILD checkpoint probe).

## Test Strategy

### Unit Tests
- **Scope:** `scripts/model/client.py` (the `extract_readings` method + backend, mocked at the SDK seam), `scripts/serve/route.py` (the `route_upload` extract branch + discriminated return), `scripts/serve/confirm.py` (the `land_confirmed` validate+land), `vault/design/templates/app_view.html` (the rendered confirm-review markup + inline JS).
- **Approach:** `pytest` with the `_FakeAnthropic` patched-SDK + `_patch_backend_client` seam ([`tests/model/test_client.py:405-469`](../../../../tests/model/test_client.py)) for `extract_readings` (no live API, no key); a `_FixtureBackend`-style mock client injected into `route_upload`/the server for the routing + confirm tests; a temp store root so no test touches the real instance; an `rg`/parse over the rendered SPA HTML for the confirm UI.
- **Criteria covered:** T1 crit 1-9 (incl. 1a, 3a, 6a); T2 crit 1-3,5; T3 crit 3,4; T4 crit 1-6.

### Integration Tests
- **Scope:** the cross-seam paths — (a) `route_upload` extract over an unrecognized format with the mock client (T2); (b) the served `POST /upload` surfaces readings + `POST /confirm-extraction` lands the confirmed subset (T3); (c) the headline E2E: synthetic fixture file → `/upload` extract → surfaced → `/confirm-extraction` → `store.append` (T5).
- **Approach:** instantiate the production `IntakeRequestHandler` over tmp roots + an injected mock backend (the `test_serve_no_egress` `_build_post_handler` pattern, [`tests/serve/test_serve_no_egress.py:92-114`](../../../../tests/serve/test_serve_no_egress.py)); POST synthetic multipart/JSON bodies; assert the store/scaffold state and the JSON review/confirm receipts.
- **Criteria covered:** T2 crit 1,2,4,4a,6,7; T3 crit 1,2,5,6,7; T5 crit 1,2,4,8,9.

### Risk-Specific Tests
- **CROWN-JEWEL file-egress (ADR-0030, the load-bearing probe):** the file content reaches ONLY the injected `client.extract_readings`; `scripts/serve/` imports 0 outbound client ([`tests/serve/test_serve_no_egress.py:186-200`](../../../../tests/serve/test_serve_no_egress.py)) and the single-model-client-import `rg` returns 0 ([`tests/model/test_client.py:158-176`](../../../../tests/model/test_client.py)) (T2 crit 4,4a, T5 crit 3). Structural/mock at build stage; the OS-egress-guard LIVE run is OQ-1.
- **CONFIRM-GATE (ADR-0030):** the store is empty after `/upload` and before `/confirm-extraction`; readings land only after the confirm POST (T3 crit 1,2; T5 crit 4).
- **FAIL-CLOSED (ADR-0030):** an extraction failure/timeout/malformed response raises `ModelCallError` and offers 0 fabricated readings (T1 crit 3,3a,6,6a; T5 crit 5).
- **OQ-5 LOCAL-RESIDUE (ADR-0005):** no tracked file carries the raw-upload token; the staged temp file is discarded (T2 crit 5; T5 crit 6).
- **EXTEND-NOT-REBUILD numstat (NFR-4):** `git diff --numstat <fork-point>` = 0 on `scripts/ingest/{ingest,adapter}.py` + `scripts/plan/*.py` (incl. `deid_in.py`) — the wave-checkpoint probe (T2 crit 6, T5 crit 7), extending the existing [`tests/serve/test_route.py:188-204`](../../../../tests/serve/test_route.py) pattern.
- **NON-TAUTOLOGICAL extract + E2E:** the extract returns the fixture's readings (different fixture → different readings, T1 crit 2); the E2E lands the fixture's confirmed values with a failing-capable negative control (T5 crit 1,2).
- **Public-repo key/PII leak (MEMORY):** the runtime key reads no tracked file + 0 key/raw leak on the fail-closed surface (T1 crit 4,6,6a,7).

## NFRs (cross-cutting, each falsifiable, each tied to ADR-0030)

- **NFR-1 (crown-jewel PII boundary — ADR-0030 file-egress class).** The ONLY egress of file content is the no-train lane; 0 file bytes reach any non-no-train endpoint. The single model-client SDK import stays inside `scripts/model/`; the file reaches only the injected `client.extract_readings`. *Falsified if* the file content reaches any sink other than `client.extract_readings`, OR `scripts/serve/` imports an outbound client, OR a model-client SDK import appears outside `scripts/model/`. **Verification:** T2 crit 4,4a, T5 crit 3 (structural/mock); the OS-egress-guard LIVE run is OQ-1 (deferred).
- **NFR-2 (operator-confirm-before-land — ADR-0030 confirm-gate).** No model-extracted reading lands in `store.append` without an operator-confirm step; the store is empty before confirm. *Falsified if* ≥1 extracted reading is in the store before `POST /confirm-extraction`. **Verification:** T2 crit 3, T3 crit 1,2, T5 crit 4.
- **NFR-3 (fail-closed, no fabricated reading — ADR-0030 fail-closed + ADR-0009 honest-data).** An extraction failure/timeout/malformed response raises `ModelCallError` and offers 0 fabricated readings; a malformed confirmed reading lands nothing. *Falsified if* a failed/partial extraction surfaces ≥1 fabricated reading, OR an incomplete confirmed reading lands. **Verification:** T1 crit 3,3a,6,6a, T3 crit 4, T5 crit 5.
- **NFR-4 (extend-not-rebuild — the frozen ingest engine + Line-Field-Set + `store.append` + the `scripts/plan/*` engine).** `scripts/ingest/ingest.py`, `scripts/ingest/adapter.py`, and every `scripts/plan/*.py` (including the `deid_in` de-id boundary) are byte-frozen; the extraction is a new front door, not an engine edit. *Falsified if* `git diff --numstat <fork-point>` ≠ 0 on those files. **Verification:** T2 crit 6, T5 crit 7 (the wave-checkpoint numstat probe). (Note: the brief named `scripts/serve/deid_in.py`; the de-id boundary's real path is `scripts/plan/deid_in.py` — `scripts/serve/deid_in.py` does not exist. The real path is the frozen one.)
- **NFR-5 (OQ-5 no tracked raw-file residue — ADR-0005).** The raw uploaded file is held in memory / the gitignored OS-temp staged path only and discarded after extraction; it is never written to a tracked path. *Falsified if* a tracked file (outside the gitignored dropzone prefixes) carries the raw-upload content after extraction. **Verification:** T2 crit 5, T5 crit 6 (backstopped by `block-pii-commit`/`pre-push`).
- **NFR-6 (0 live spend — mock/fixture-tested).** Every acceptance criterion is satisfiable with a MOCK no-train backend injected at the ADR-0015 seam + synthetic fixture files; no test makes a live API call or reads a real key. *Falsified if* any build test makes a `key_source.resolve()`-gated live call. **Verification:** T1 crit 7, T5 crit 8 (the absence-of-SDK 0-spend pins).
- **NFR-7 (interface-pinned, internals-discretionary).** The build PINS the `ModelClient.extract_readings(file_content, media_type) -> list[Line-Field-Set readings]` contract, the file→model content-block mechanism (document/image/text), the `route_upload` discriminated return, the `POST /confirm-extraction` route + JSON shape, and every acceptance criterion. It does NOT pin the exact SDK request JSON, the structured-output schema's internal field ordering, the confirm UI's exact CSS/JS, or the retry/backoff constants' values — implementer discretion.

## Amended-Criterion → Enforcing AC (ADR-0030 §amends)

ADR-0030 (on acceptance) amends the falsification criteria of four governing ADRs to authorize the ONE ingestion-extraction egress class on the no-train lane (ADR-0030 Consequences — Amendment declaration / Related Decisions). Each scoped criterion maps to the build AC that enforces the bound — so a future build that breaks an amended bound reds a specific AC:

| Amended ADR (ADR-0030 §amends) | Scoped falsification criterion | Enforcing build AC |
|---|---|---|
| **ADR-0001** | the ingestion clause's model-independence (Decision L24) is scoped to authorize this one extraction-egress class on the no-train lane | the crown-jewel file-egress bound — 0 file bytes to any non-no-train endpoint (NFR-1): **T2 crit 4,4a**, **T5 crit 3** |
| **ADR-0003** | falsification #3 ("halt ingestion if it sends ≥1 raw reading to the model") is scoped — the no-train extraction call is the authorized, operator-confirmed exception; confirmed readings still land via the unchanged sink | the operator-confirm gate (**T3 crit 1,2**, **T5 crit 4**) + the 0-shared-routine-edit / EXTEND-NOT-REBUILD numstat (**T2 crit 6**, **T5 crit 7**) |
| **ADR-0013** | the upload-server "exactly ONE outbound class" falsification is scoped to admit a SECOND authorized upload-server outbound class — the extraction call on the no-train lane | the single-egress-class structural probe — `route.py` imports no SDK, the only outbound is `client.extract_readings`, `scripts/serve/` carries 0 outbound client (**T2 crit 4a**, **T3 crit 6**) |
| **ADR-0029** | the SPA "≥1 outbound class beyond the `/chat` turn → block adoption" falsification is scoped to admit the upload-extraction egress (same no-train lane) | the SPA's only browser outbound are the same-origin `/upload` + `/confirm-extraction` (loopback); the extraction egress is the SERVER's no-train call (**T4 crit 2**, **T3 crit 6**) |

## Repo-Grounding Ledger

| Task | RGC-1 (manifest action vs disk) | RGC-2 (premise freshness) | RGC-3 (cited-input existence + declared shape) | RGC-4 (capability non-duplication) | Disposition |
|------|---------------------------------|---------------------------|-----------------------------------------------|-----------------------------------|-------------|
| T1 | pass — `client.py`/`test_client.py` Modify=present [VERIFIED] | pass — `deidentify`/`converse` are LIVE-implemented (`client.py:251-334` [VERIFIED]); `author` is the `NotImplementedError` stub (`client.py:291-295`); there is NO `extract_readings` method today (the new surface) | pass — the `_client`/`key_source.resolve`/bounded-retry/`ModelCallError from None` mirror present; `_FakeAnthropic`/`_patch_backend_client`/`_summary_envelope_text` patched-SDK harness present (`test_client.py:405-469` [VERIFIED]); `keying.LINE_FIELDS` present (`keying.py:11`); the no-train document/image/structured-output content blocks grounded against the claude-api skill (`claude-opus-4-8`) | pass — distinct from the existing `scripts/serve/extract.py` / `extract_facts` (the ADR-0017 conversation-PROPOSAL validator that routes model-emitted facts through `capture.persist_capture`, `extract.py:58-147` [VERIFIED]): the proposed file→model Line-Field-Set extraction is a NEW method on the MODEL CLIENT (`scripts/model/client.py`), a different layer and capability — file-content→structured-readings on the no-train lane, NOT serve-layer conversation-fact validation — so NOT a duplicate. To avoid the literal name collision with the `scripts/serve/extract.py` module + its `extract_facts`, the new method is named `extract_readings` (not bare `extract`); the single SDK import stays inside `scripts/model/` | Grounded |
| T2 | pass — `route.py`/`test_route.py` Modify=present [VERIFIED] | stale→actual — `route_upload` dispatches ONLY named adapters + the `.zip` content-branch and `_detect_source` `SystemExit`s on an unrecognized extension (`route.py:58-93`, `__main__.py:42-50` [VERIFIED]); the universal-extraction branch is absent today | pass — `_detect_source`/`_EXT_SOURCE` reuse present (`route.py:25,87`); `store.read_all` present; `.gitignore` dropzone prefixes present (`.gitignore:2-5`); the `test_shared_ingest_routines_byte_unchanged` numstat pattern present (`test_route.py:188-204`); the `scripts/serve/` 0-outbound grep present (`test_serve_no_egress.py:186-200`) | pass — the extract branch is a NEW front door on the existing router; it CALLS `client.extract_readings`, adds no second extension map, no store write | Grounded |
| T3 | pass — `server.py` Modify=present; `confirm.py`/`test_extract_confirm.py` Create=absent [VERIFIED] | stale→actual — the route table is `{GET /, GET /settings/key, POST /upload, POST /chat, POST /settings/key}` and carries NO `/confirm-extraction`, no extraction surface (`server.py:129-147` [VERIFIED]); `route_upload` is called WITHOUT a client today (`server.py:180`) | pass — the `/chat` `_write_json` + catch-and-degrade pattern present (`server.py:243-268`); `ingest.manual_entry`/`import_csv`/`store.append` present (`ingest.py:36,61-129`); the `build_server` `client` class-attr seam present (`server.py:118,241,398-415`) | pass — distinct from the existing `capture.persist_capture` (the model-proposes-gate-disposes sink for CONVERSATION facts, `capture.py:230-300` [VERIFIED]): `confirm.land_confirmed` is the SAME disposes-after-gate pattern but for FILE-extracted readings — a CALLER of the UNCHANGED `store.append`/`ingest.manual_entry` sink, NOT a second sink and NOT a second gate (the operator-confirm IS the gate). Adds no second dedupe key; the `/upload` handler is extended, not rebuilt | Grounded |
| T4 | pass — `app_view.html`/`test_app_shell.py` Modify=present [VERIFIED] | stale→actual — `Upload Documents` is the `#screen-team` workspace right column with a `<form action='/upload'>` + a `fetch('/upload'` flow (`app_view.html:431,468,738,761` [VERIFIED]); there is NO confirm-review panel / `/confirm-extraction` post today | pass — the `Upload Documents` form + doc-cards + the inline-JS `fetch('/upload'` upload posture present; `generate.run('app')` inline-asset gate present (`generate.py:75-91`, `render.emit` off-file guard) | pass — the confirm UI is NEW markup on the existing surface; it reuses the `fetch` upload posture, adds no off-file asset | Grounded |
| T5 | pass — `test_universal_ingestion_e2e.py` Create=absent [VERIFIED `test ! -e` returns 0] | pass — the mock-client seam (`ModelClient(backend=...)`, `client.py:44`), the served-handler `_build_post_handler` test pattern (`test_serve_no_egress.py:92-114`), and the numstat fork-point pattern (`test_route.py:195-204`) are all present and byte-unchanged | pass — `store.read_all`/`store.append` present; the 0-outbound grep + single-import `rg` present; the `.gitignore` dropzone prefixes present for the OQ-5 scan | pass — the E2E is the absent headline proof; it binds the built mechanism, adds 0 production code | Grounded |

**Ledger notes.**
- **`extract.py` naming-collision decision (T1 RGC-4).** A serve-layer module `scripts/serve/extract.py` with an `extract_facts`/`persist_extraction` capability already exists (the ADR-0017 conversation-proposal validator, [`scripts/serve/extract.py:58-147`](../../../../scripts/serve/extract.py)). It is a DIFFERENT layer (serve) and a DIFFERENT capability (validating model-emitted conversation facts into `capture.persist_capture`) from this spec's NEW model-client method (file content → structured Line-Field-Set readings on the no-train lane). To keep the two unambiguous and avoid the literal module/function name clash, the new model-client method is named **`extract_readings`** (on `scripts/model/client.py`), NOT bare `extract`. T1's manifest/criteria use `extract_readings` throughout.
- **`confirm.land_confirmed` is a caller, not a sink (T3 RGC-4).** `confirm.land_confirmed` mirrors the existing `capture.persist_capture` disposes-after-gate pattern but lands FILE-extracted readings; it CALLS the unchanged `store.append`/`ingest.manual_entry` sink (no second sink, no second dedupe key, no second gate — the operator-confirm IS the gate).

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR-0030 section (Decision / Consequences / Validation Approach — Confirmation+Falsification / Open Questions / constrains-edge).
- [x] Every ADR ID in the `adrs` frontmatter (ADR-0030) has at least one task (T1-T5 all cite ADR-0030).
- [x] All ADR IDs resolve to actual ADR files on disk (`docs/adr/ADR-0030-model-based-universal-ingestion.md` [VERIFIED]).

### Acceptance Criteria Quality
- [x] Every task has ≥1 acceptance criterion (T1 has 12 — 1,1a,2,3,3a,4,5,6,6a,7,8,9; T2 has 8 — 1,2,3,4,4a,5,6,7; T3 has 7; T4 has 6; T5 has 9).
- [x] All criteria are binary — each cites a `pytest` target, an `rg`/grep count, a mock call-count, a `store.read_all` assertion, a `git diff --numstat`, a tracked-tree scan count, or a render-path return.
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient".

### File Manifest Integrity
- [x] Every task has a file manifest; every file in any task block appears in the top-level File Manifest and vice versa.
- [x] No task lists a directory instead of a specific file (the frozen-set globs are numstat probe targets in criteria, not manifest entries).
- [x] Every source file has a corresponding test file (`client.py`→`test_client.py`; `route.py`→`test_route.py`; `server.py`/`confirm.py`→`test_extract_confirm.py`; `app_view.html`→`test_app_shell.py`; the E2E→`test_universal_ingestion_e2e.py`).

### Dependency Map Integrity
- [x] No cycles (Kahn drains all 5 nodes; 4 ordered groups).
- [x] Every task ID in a Dependencies field appears as a node; every edge corresponds to a Dependencies entry; the entry point (T1) has "None (entry point)".
- [x] No phantom dependency — T2→T1 (T2 calls the method T1 builds), T3→T2 (T3 surfaces/lands what T2 extracts), T4→T3 (T4 consumes T3's payload+route), T5→T3 (T5 exercises T3's full backend path); each edge names the artifact/surface that flows.
- [x] No missing dependency — file-level: T2 (`route.py`) calls T1's `client.extract_readings`; T3 (`server.py`) calls T2's `route_upload` return + creates `confirm.py`; T4 (`app_view.html`) consumes T3's routes; T5 drives T3's routes — every implicit edge is declared.

### Constraint Propagation
- [x] CROWN-JEWEL file-egress (0 file bytes to a non-no-train endpoint) carried as NFR-1 + T2 crit 4 + T5 crit 3.
- [x] CONFIRM-GATE (0 readings land unconfirmed) carried as NFR-2 + T2 crit 3 + T3 crit 1,2 + T5 crit 4.
- [x] FAIL-CLOSED (0 fabricated readings) carried as NFR-3 + T1 crit 3,3a,6 + T3 crit 4 + T5 crit 5.
- [x] EXTEND-NOT-REBUILD (frozen engine numstat) carried as NFR-4 + the wave-checkpoint probe + T2 crit 6 + T5 crit 7.
- [x] OQ-5 LOCAL-RESIDUE (no tracked raw-file write) carried as NFR-5 + T2 crit 5 + T5 crit 6.
- [x] 0 LIVE SPEND carried as NFR-6 + T1 crit 7 + T5 crit 8.

### Unresolved Concerns
- [x] Disposition section present (5 rows): OQ-1 Defer, OQ-2 Defer, OQ-3 Proceed, OQ-4 Defer, OQ-5 Proceed — matching `dispositions.md`.
- [x] Defer dispositions justify why deferral is safe (OQ-1 operator-gated live run; OQ-2 independent fast-path; OQ-4 operational, decision-invariant).
- [x] Proceed dispositions land as build criteria (OQ-3 = the whole decomposition; OQ-5 = T2 crit 5 / T5 crit 6).

### Risk Coverage
- [x] Risk Mitigations field on every task; every ADR-0030 negative consequence covered (the first-ingestion-axis egress class → NFR-1/the egress probes; the standing verification burden → the four falsification probes as tests; the fidelity ceiling → confirm-before-land + fail-closed; the operator-review burden → T4's per-reading confirm; the network dependency → mock-tested, the live run is OQ-1).
- [x] The four ADR-0030 §amends scoped criteria (ADR-0001/0003/0013/0029) each map to an enforcing build AC in the Amended-Criterion → Enforcing AC table.

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category.
- [x] Risk-specific tests exist for the crown-jewel file-egress probe, the confirm-gate probe, fail-closed, OQ-5 residue, the EXTEND-NOT-REBUILD numstat, and the non-tautological extract+E2E.

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status).
- [x] No placeholder text ("TBD", "TODO: fill in", "...").
- [x] The headline capability (universal any-format ingestion through extract→confirm→land) is a named end-to-end task (T5) testable against mocks at 0 live spend, with the LIVE run gated on OQ-1 (operator-present, real key + real file + real spend).

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists in the current worktree (`client.py`/`test_client.py`/`route.py`/`test_route.py`/`server.py`/`app_view.html`/`test_app_shell.py` [VERIFIED present]).
- [x] Every File Manifest `Create` row names a path that does NOT already exist (`confirm.py`/`test_extract_confirm.py`/`test_universal_ingestion_e2e.py` — all absent [VERIFIED]).
- [x] Every ADR premise a task relies on was re-verified against the current repo; stale-against-build premises (no `extract_readings` method, no extraction branch in `route_upload`, no `/confirm-extraction` route, no confirm UI) are recorded in the Repo-Grounding Ledger with the actual state.
- [x] Every cited input a task parses/reads declares its structural assumption AND the live file satisfies it (the `_FakeAnthropic` harness, the `_detect_source`/`_EXT_SOURCE` reuse, the `_write_json`/catch-and-degrade pattern, the `store.append`/`manual_entry` sink, the `fetch('/upload'` posture, the numstat fork-point pattern, the 0-outbound grep — all re-grepped).
- [x] No task proposes a new artifact that duplicates an existing capability (`extract_readings` is a new method on the existing client; the front door reuses `_detect_source` + `client.extract_readings`; `confirm.py` lands through the unchanged `store.append`; the confirm UI reuses the `fetch` upload posture).
- [x] Repo-Grounding Ledger present, one row per task, each with a disposition.
- [x] Manifest-path correction recorded: the brief's `scripts/serve/deid_in.py` does not exist; the de-id boundary's real path `scripts/plan/deid_in.py` is the frozen-set member (NFR-4 note).
