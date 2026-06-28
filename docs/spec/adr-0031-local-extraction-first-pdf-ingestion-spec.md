---
scope: "ADR-0031: extract an unrecognized-format PDF upload to TEXT LOCALLY first (pdftotext primary, marker fallback) — 0 network — then send only the extracted TEXT (never the raw document block) to the no-train model for structuring over the existing text content-block path, CHUNKED so the structured output never truncates and every finding is captured, aggregated + deduped through the UNCHANGED keying / store.append sink, with genetics findings captured as DURABLE GENOTYPE FACTS (item=gene+rsID, timepoint=sample-date, source=dna-report, value=alleles); a NEW local-extract front module onto the frozen engine, mock/fixture-tested at 0 live spend"
adrs: [ADR-0031]
tier: 9
created: 2026-06-28
status: approved
---

# Spec: Local-Extraction-First PDF Ingestion + Genetics Genotype-Fact Capture

## Component Overview

This spec implements ADR-0031, which AMENDS the now-live ADR-0030 file→model mechanism. Today an unrecognized-format upload routes through the no-train model as a raw base64 `document` content block: `route._extract_unrecognized` reads `path.read_bytes()` and hands the raw binary + a derived media type to `client.extract_readings` ([`scripts/serve/route.py:143-145`](../../../../scripts/serve/route.py)), whose backend base64-encodes a PDF into a `{"type":"document",...}` block for the no-train call ([`scripts/model/client.py:303-320`](../../../../scripts/model/client.py)). Two S99 operator-present live-run failures made that the wrong default for a dense file: the structured-output schema was top-level-array-rooted (every call 400'd — fixed `0ee9a5d`, now object-rooted [`scripts/model/client.py:334-360`](../../../../scripts/model/client.py)), then a real multi-page report truncated the JSON output at `max_tokens=2048` (raised to `_EXTRACT_MAX_TOKENS=16384`, `e7461ab`, now [`scripts/model/client.py:279`](../../../../scripts/model/client.py)). The residual that commit named — a 42-page genetics/SNP report that still truncates at 16384 — is a format-fit limit, not a ceiling to keep raising. **The two foundation fixes are committed (`0ee9a5d` + `e7461ab`); this spec builds ON them.**

The build is a NEW LOCAL-EXTRACT FRONT MODULE onto the frozen engine, decomposed into six tasks. **T1** adds a local PDF→text extraction module (`scripts/ingest/pdf_extract.py`, NEW): `pdftotext` (poppler) primary as a local subprocess, `marker`/`marker_single` fallback when `pdftotext` yields no/low text — both deterministic local subprocesses making zero network calls, returning the extracted text. **T2** adds the chunk-and-aggregate module (`scripts/ingest/extract_chunked.py`, NEW): split the extracted text into bounded chunks, call `client.extract_readings(chunk, "text/plain")` per chunk (the existing TEXT content-block path, never a `document` block), aggregate + dedupe the per-chunk readings through the UNCHANGED `keying.dedupe_key`/`is_conformant`, and surface an HONEST partial/too-large signal — never a silent "no new data". **T3** maps genetics findings to durable GENOTYPE FACTS via the extract system prompt (`scripts/model/client.py._extract_system_prompt`): item=gene+rsID, timepoint=genome sample date, source=`dna-report`, value=alleles, capturing ALL findings (not a "noteworthy" subset), storing the fact and NOT the report's dated interpretation. **T4** wires the front step into `route._extract_unrecognized` — a PDF is local-extracted to text FIRST, then chunk-structured (the raw binary stays local) — and surfaces the honest signal through the server `/upload` review payload. **T5** lands the operator-visible partial-extraction note on the SPA review panel (no silent "no new data"). **T6** is the headline end-to-end proof plus the six ADR-0031 falsification probes as tests.

The structuring backend is the swappable no-train client (ADR-0015), so the model call is mock-tested at 0 live spend at the same `_FakeAnthropic`/`_patch_backend_client` seam ADR-0030 uses ([`tests/model/test_client.py`](../../../../tests/model/test_client.py)). The local extractors run a real `pdftotext` on a synthetic fixture PDF where poppler is present (a `skipif`-gated, deterministic, 0-spend, 0-network local run) and STUB the heavy `marker` subprocess — never a real heavy marker run ([VERIFIED: poppler 26.02.0 at `/opt/homebrew/bin/pdftotext`; `~/.local/bin/marker_single` → marker-pdf]). The OS-level egress-guard LIVE run is OQ-1 (deferred); this spec's crown-jewel probe is the structural/mock form.

**The crown-jewel PII boundary (NFR-1, load-bearing).** ADR-0031 is a FURTHER move toward ADR-0001's crown-jewel ideal: where ADR-0030 sent the whole raw PDF binary off-device as a `document` block, ADR-0031 keeps the raw binary LOCAL (it reaches only the `pdftotext`/`marker` subprocess) and sends only the scopeable extracted TEXT across the SAME authorized no-train lane (ADR-0016 / ADR-0027). The bound this spec enforces for a PDF upload is: **0 raw-binary bytes egress to ANY endpoint (including the no-train lane — the lane receives extracted TEXT only), AND 0 text bytes to any non-no-train endpoint, AND 0 network calls from the local extractor subprocess.** The frozen ingest engine + Line-Field-Set + `keying`/`store.append` sink + `scripts/plan/*` engine are byte-unchanged (NFR-3, EXTEND-NOT-REBUILD) — the local-extract step is a new front module, not an engine edit. Genetics readings land via the UNCHANGED sink (no second data model, ADR-0031 non-goal). No extracted reading lands unconfirmed (the inherited confirm-gate), no extraction failure fabricates a reading (fail-closed), no dense document drops findings silently (honest completeness).

### Pinned local-extract-first mechanism (T1–T4 — grounded; tuning values discretionary)

| Upload class | Mechanism | Grounding |
|--------------|-----------|-----------|
| PDF (`application/pdf`) — unrecognized format | `pdf_extract.extract_text(path)` → `pdftotext` subprocess; on no/low text → `marker_single` subprocess (stubbed in tests). Then `extract_chunked.extract_all(text, client)`: chunk → `client.extract_readings(chunk, "text/plain")` per chunk → aggregate + dedupe via `keying`. **Raw binary never reaches the model; only `text/plain` chunks do.** | poppler `pdftotext` + marker-pdf present [VERIFIED]; the existing `text` content-block path [`client.py:330-331`](../../../../scripts/model/client.py); `keying.dedupe_key`/`is_conformant` [`keying.py:19,35`](../../../../scripts/store/keying.py) |
| Non-PDF unrecognized format (image / arbitrary text) | UNCHANGED ADR-0030 path: raw content → `client.extract_readings(file_content, media_type)` (image vision block / text block) | [`route.py:143-145`](../../../../scripts/serve/route.py), [`client.py:321-331`](../../../../scripts/model/client.py) — ADR-0031 is PDF-scoped; the image/text paths are out of scope, byte-unchanged |
| Genetics genotype fact (a genetics-report PDF) | The extract system prompt instructs: per SNP finding, `item`=gene+rsID, `timepoint`=genome sample date, `source`=`dna-report`, `value`=alleles; capture ALL findings; store the fact, NOT the interpretation. **No schema change** — `_extract_output_schema` already constrains each reading to `LINE_FIELDS`. | [`client.py:282-300`](../../../../scripts/model/client.py) (`_extract_system_prompt`), [`client.py:334-360`](../../../../scripts/model/client.py) (`_extract_output_schema` over `LINE_FIELDS`) |
| Honest completeness signal | `extract_chunked.extract_all` returns `{"readings": [...], "complete": bool, "note": str|None}`; the route propagates it; the server `/upload` review payload carries `partial`/`notes`; the SPA renders the note. A document too dense to complete surfaces a partial/too-large signal — never a silent "no new data". | the prior live failure (commit `e7461ab` message) the honest signal replaces |

The exact chunk size + overlap, the `max_chunks` too-large ceiling, and the `marker`-trigger low-text threshold are pinned at build as named constants (OQ-2); the completeness + dedupe + fallback contracts hold regardless of the exact values (NFR-7).

## Unresolved Concerns Disposition

Source: ADR-0031 Open Questions OQ-1..OQ-4. Dispositioned under the operator's autonomous build directive (the scope calls flow from the ADR + the build brief; none is a new operator-owned decision).

| # | Item | Disposition | Rationale / Where it lands |
|---|------|-------------|----------------------------|
| OQ-1 | The operator-present LIVE run (real key + the real genetics report + real spend) end-to-end through local-extract → chunk → structure → confirm → land. | **Defer** | Operator-gated downstream checkpoint, not a build task. The build is mock/fixture-tested at 0 live spend; the OS-egress-guard LIVE form of the crown-jewel + local-extractor-network probes is the deferred live run. Recorded as a non-goal. |
| OQ-2 | The exact chunk size + overlap, the `max_chunks` too-large ceiling, and the `marker`-trigger low-text threshold. | **Proceed** | Pinned at build as named constants — `_CHUNK_CHARS` / `_CHUNK_OVERLAP` / `_MAX_CHUNKS` (T2) and `_LOW_TEXT_CHARS` (T1). The completeness (no cross-boundary loss via overlap), dedupe (no duplicate via `keying`), honest-partial, and marker-fallback contracts hold regardless of the exact values; the values are NFR-7 implementer-discretionary within the pinned contract. |
| OQ-3 | Local-residue handling of the extracted TEXT during the structuring call — memory-only, or written to the gitignored staged path. | **Proceed** | Load-bearing for ADR-0005 (a tracked text residue breaches the PII-free trunk). The spec PINS: both the raw binary and the extracted text are held in memory / the gitignored OS-temp staged path only (the existing `route_upload` staged path under `tempfile.TemporaryDirectory()`), discarded after extraction, NEVER a tracked write — backstopped by the `block-pii-commit`/`pre-push` hooks. A build acceptance criterion (T4 crit 6, T6 residue probe). |
| OQ-4 | The precise no-train retention window for the extracted text at this call. | **Defer** | Operational/operator-owned (target 2026-06-30); does not change the decision (it accepts bounded retention, the same no-train profile as the de-id summary/conversation, and the payload is strictly SMALLER than ADR-0030's raw binary). Out of build scope. |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/ingest/pdf_extract.py` | Create | T1: `extract_text(pdf_path) -> str` — `pdftotext` subprocess primary; on no/low text (`< _LOW_TEXT_CHARS`) the `marker_single` subprocess fallback; a typed `PdfExtractError` on total failure (no silent ""). Local subprocesses, 0 network, 0 SDK import. The `_LOW_TEXT_CHARS` threshold (OQ-2) is a named constant. |
| `tests/ingest/test_pdf_extract.py` | Create | T1: the real-`pdftotext` round-trip on a synthetic fixture PDF (`skipif` poppler absent) + a different-fixture non-tautology; the stubbed-subprocess low-text→marker-fallback + ample-text→no-fallback branching; the 0-outbound-client/0-SDK grep; the fail-loud-on-total-failure raise. |
| `scripts/ingest/extract_chunked.py` | Create | T2: `extract_all(text, client, *, chunk_chars=_CHUNK_CHARS, overlap=_CHUNK_OVERLAP, max_chunks=_MAX_CHUNKS) -> dict` — split text into ≤`chunk_chars` line-boundary chunks with `overlap`, call `client.extract_readings(chunk, "text/plain")` per chunk, aggregate + dedupe via the UNCHANGED `keying.dedupe_key`/`is_conformant`, return `{"readings": [...], "complete": bool, "note": str|None}` (the honest partial/too-large signal). Imports `keying` (REUSED, no second key); imports no SDK (injected client). The `_CHUNK_*` constants (OQ-2) are named. |
| `tests/ingest/test_extract_chunked.py` | Create | T2: single-chunk round-trip; the crown-jewel text-path (every call media_type `"text/plain"`); the non-tautological N-chunk union aggregation; the cross-overlap dedupe via `keying`; the honest too-large signal (`complete=False`+note over budget, `complete=True`/`note=None` within budget); the `ModelCallError` fail-closed propagation; the reuse-keying-no-second-key grep. |
| `scripts/model/client.py` | Modify | T3: extend `_extract_system_prompt` with the genetics genotype-fact mapping instruction (item=gene+rsID, timepoint=sample-date, source=`dna-report`, value=alleles; capture ALL findings; store the fact, NOT the interpretation). NO schema change (`_extract_output_schema` already constrains to `LINE_FIELDS`). `extract_readings`, `_extract_content_block`, `_extract_output_schema`, `deidentify`, `converse`, `author` byte-unchanged. |
| `tests/model/test_client.py` | Modify | T3: the `_extract_system_prompt()` genetics-mapping structural assertions (the gene+rsID/sample-date/`dna-report`/alleles rule + the capture-ALL + the not-the-interpretation directives); the non-tautological genetics-readings flow through the fixture backend (genetics fixture A → readings A, fixture B → readings B≠A); the value-is-the-allele-not-the-interpretation fixture; the scoped-change diff (only `_extract_system_prompt` touched). |
| `scripts/serve/route.py` | Modify | T4: in `_extract_unrecognized`, branch on `media_type == "application/pdf"` — local-extract via `pdf_extract.extract_text(path)` then `extract_chunked.extract_all(text, client)`, returning `{"extracted_readings": readings, "extraction_complete": bool, "extraction_note": note}`. A non-PDF unrecognized format keeps the UNCHANGED raw-content `client.extract_readings(file_content, media_type)` path. The raw PDF bytes reach ONLY the local extractor; the model client receives only `text/plain`. Imports no outbound client / SDK. |
| `tests/serve/test_route.py` | Modify | T4: the PDF text-path routing (pdf_extract + extract_chunked called, the raw-bytes document path not); the crown-jewel raw-binary-egress structural probe (model receives `text/plain`, the seeded raw-binary token reaches no model call); the non-PDF-unchanged regression; the honest-signal-in-return assertion; the no-auto-land; the OQ-3/OQ-5 residue scan; the EXTEND-NOT-REBUILD numstat over the frozen set + `keying.py` + `store.py`. |
| `scripts/serve/server.py` | Modify | T4: the `/upload` handler collects `extraction_complete`/`extraction_note` across staged files and surfaces them in the JSON review payload — `{"readings": extracted, "partial": <any incomplete>, "notes": [...]}` — so the honest partial/too-large signal reaches the operator. A complete extraction keeps `partial: false`. The route table, the `_LOOPBACK` bind, and the 0-outbound-client posture are byte-unchanged. |
| `tests/serve/test_server.py` | Modify | T4: the `/upload` partial-signal surfacing (an over-budget extraction → `partial: true` + notes in the payload; a complete extraction → `partial: false`); the route-table-unchanged + 0-outbound-client re-assertion. |
| `vault/design/templates/app_view.html` | Modify | T5: the review panel renders a visible partial-extraction note when the `/upload` payload carries `partial: true` + `notes`; the inline JS displays both the readings AND the note (never the silent empty/"no new data" state on a partial). Reuses the existing `#review-panel`/`showReview` posture ([`app_view.html:485-487,745`](../../../../vault/design/templates/app_view.html)); adds no off-file asset. |
| `tests/serve/test_app_shell.py` | Modify | T5: the rendered-SPA partial-note markup + the inline-JS `partial`/`notes` branch; the honest empty-vs-partial distinction (a partial response shows readings + note, a truly-empty extraction shows the awaiting state); the inline-asset render-gate pass. |
| `tests/serve/test_pdf_ingestion_e2e.py` | Create | T6: the headline E2E (synthetic fixture PDF → `route_upload` PDF local-extract → chunk → mock structure → surfaced → `POST /confirm-extraction` → `store.append`), the non-tautological trace-to-fixture headline + failing-capable negative control, the genetics genotype-fact land, and the six ADR-0031 falsification probes (raw-binary-egress, local-extractor-network, extend-not-rebuild, completeness/no-silent-truncation, confirm-gate, key-never-committed) composed end-to-end. No new production code. |

## Tasks

### ADR-0031-T1: Local PDF→Text Extraction Module — `pdftotext` Primary, `marker` Fallback, 0 Network, Fail-Loud

**Status:** TODO
**ADR Source:** ADR-0031, Decision (extract the text LOCALLY before any model call; local extraction is two-tier — `pdftotext` deterministic primary, `marker`/`marker_single` fallback invoked only when `pdftotext` yields no/low text; both deterministic local subprocesses making zero network calls); ADR-0031, Rationale — coverage (`pdftotext` fast default, `marker` only on the low-text trigger); ADR-0031, Falsification — Local-extractor-network probe (0 network calls from the local extractor); ADR-0031 OQ-2 (the `marker`-trigger low-text threshold pinned at build)
**Files to create/modify:**
- `scripts/ingest/pdf_extract.py` -- Create: `extract_text` + the `pdftotext`/`marker` subprocess helpers + `_LOW_TEXT_CHARS`
- `tests/ingest/test_pdf_extract.py` -- Create: the real-`pdftotext`+stubbed-`marker` tests

**Acceptance Criteria:**
1. `extract_text(pdf_path) -> str` returns the PDF's text via `pdftotext` — verified by a test running the real `pdftotext` on a synthetic fixture PDF (no PII) whose known text (e.g. `"MTNR1B rs10830963 (C;G)"`) appears verbatim in the return, `skipif shutil.which("pdftotext") is None` (a clone without poppler stays green; mirrors the SDK-absent skip posture).
2. NON-TAUTOLOGICAL (fixture-driven, not a constant): a fixture PDF carrying text X returns X and a DIFFERENT fixture carrying text Y returns Y (Y ≠ X) — verified by the two skipif-gated real-`pdftotext` cases, proving the return is the extracted text, not a hardcoded string.
3. Low-text → `marker` fallback: with `pdftotext` STUBBED to return `< _LOW_TEXT_CHARS` characters, `extract_text` invokes the `marker_single` fallback exactly once and returns the marker text — verified with BOTH subprocess calls stubbed (no real heavy marker run, no model download), asserting the marker stub's call count is 1.
4. Ample-text → no fallback: with `pdftotext` STUBBED to return `>= _LOW_TEXT_CHARS` characters, the `marker` fallback is NOT invoked — verified by asserting the marker stub's call count is 0 (the cheap path's no-heavy-cost contract).
5. CROWN-JEWEL local-extractor 0-network by construction: `scripts/ingest/pdf_extract.py` imports/uses no outbound HTTP client (the `_OUTBOUND_CLIENT_MARKERS` set — `socket.create_connection`, `urllib.request`, `http.client`, `requests`, `httpx`) and no model-client SDK (`anthropic`) — verified by a source-grep test returning 0. (The OS-egress-guard LIVE 0-network probe is OQ-1, deferred.)
6. Fail-loud on total failure: a PDF yielding no text from `pdftotext` AND no text from the `marker` fallback raises a typed `PdfExtractError` — verified by stubbing both to return `""` and asserting `pytest.raises(PdfExtractError)`, so the caller never mistakes an extraction failure for an empty document (the honest-data no-silent-empty contract).
7. `.venv/bin/python -m pytest tests/ingest/test_pdf_extract.py` passes.

**Risk Mitigations:** ADR-0031 crown-jewel local-extractor-network (0 network from the extractor) — crit 5 (structural; the LIVE OS-egress-guard form is OQ-1). ADR-0031 honest-data (no silent empty on extraction failure) — crit 6. Non-tautological extraction — crit 2. The heavy-`marker` cost paid only on the low-text trigger — crit 3,4. The `marker`-stub discipline (never a real heavy run / model download in tests) — crit 3.
**Dependencies:** None (entry point).

---

### ADR-0031-T2: Chunk + Aggregate + Dedupe Extraction with the Honest-Partial Signal — Text-Path Only, Reuses `keying`

**Status:** TODO
**ADR Source:** ADR-0031, Decision (send only the extracted TEXT over the existing `text` content-block path — never the raw `document` block — chunking large text so the structured OUTPUT never truncates and every finding is captured, aggregating + deduping through the UNCHANGED `keying.is_conformant`/`store.append` sink); ADR-0031, Validation — Chunk-and-aggregate completeness (the UNION of all parts' readings, deduped; 0 findings dropped across boundaries, 0 duplicates from overlap) + Completeness/no-silent-truncation (a too-large document surfaces an HONEST partial/too-large signal, never a silent "no new data"); ADR-0031 OQ-2 (chunk size + overlap + the too-large ceiling pinned at build)
**Files to create/modify:**
- `scripts/ingest/extract_chunked.py` -- Create: `extract_all` + the chunker + `_CHUNK_CHARS`/`_CHUNK_OVERLAP`/`_MAX_CHUNKS`
- `tests/ingest/test_extract_chunked.py` -- Create: the mock-client chunk/aggregate/dedupe/signal tests

**Acceptance Criteria:**
1. Single-chunk round-trip: text fitting one chunk drives exactly one `client.extract_readings(text, "text/plain")` call and returns `{"readings": <the mock's conformant readings>, "complete": True, "note": None}` — verified with a recording mock client.
2. CROWN-JEWEL text-path: EVERY `client.extract_readings` call `extract_all` makes carries media_type `"text/plain"` (never `"application/pdf"`); no raw-binary content reaches the client — verified by the mock recording every call's `media_type`.
3. NON-TAUTOLOGICAL N-chunk aggregation (no cross-boundary loss): a text large enough to split into N ≥ 3 chunks, with the mock returning a DISTINCT reading per chunk, yields an aggregate `readings` that is the UNION of all N (a reading produced only by chunk 3 IS present), `len == N` after dedupe — verified by asserting each chunk's distinct reading is in the result (fails if any chunk's findings are dropped).
4. Cross-overlap dedupe via the SHARED key: when two chunks return readings sharing an `(item, timepoint, source)` identity (the overlap region), the aggregate carries that reading ONCE — verified using `keying.dedupe_key` (0 duplicates), proving the dedupe reuses the shared key, not a second one.
5. HONEST too-large signal (no silent drop), NON-TAUTOLOGICAL: a text whose chunk count exceeds `_MAX_CHUNKS` returns `complete=False` + a non-empty `note` AND still returns the readings it DID extract (never a silent empty / "no new data"); a within-budget text returns `complete=True`, `note=None` — verified by an over-budget fixture (`complete is False`, `note` truthy) and a within-budget fixture (`complete is True`, `note is None`), so the signal trips ONLY when over budget.
6. Fail-closed propagation: a `ModelCallError` raised by `client.extract_readings` on a chunk propagates out of `extract_all` (it is not swallowed into a fabricated reading or a false `complete`) — verified by a mock raising on a chunk asserting `pytest.raises(ModelCallError)` and 0 readings returned.
7. Reuses `keying`, no second key: `scripts/ingest/extract_chunked.py` imports `keying.dedupe_key`/`is_conformant` and defines no dedupe identity of its own, and imports no model-client SDK — verified by a source-grep/import test.
8. `.venv/bin/python -m pytest tests/ingest/test_extract_chunked.py` passes.

**Risk Mitigations:** ADR-0031 completeness / no-silent-truncation (the exact prior "no new data" failure) — crit 3,5. ADR-0031 crown-jewel text-only egress — crit 2. ADR-0031 fail-closed (no fabricated reading) — crit 6. ADR-0031 single-sink / 0-shared-routine-edit (no second dedupe key) — crit 4,7. Non-tautological aggregation + signal — crit 3,5.
**Dependencies:** None (entry point — operates on text + an injected client; mock-tested in isolation).

---

### ADR-0031-T3: Genetics Genotype-Fact Extraction Mapping — Capture-All, Fact-Not-Interpretation, Prompt-Only

**Status:** TODO
**ADR Source:** ADR-0031, Decision (capture genetics findings as DURABLE GENOTYPE FACTS — item=gene+rsID, timepoint=genome sample date, source=`dna-report`, value=alleles; ALL SNP findings, not a "Noteworthy" subset; the report's dated interpretation is NOT stored as truth); ADR-0031, Rationale (the fact/interpretation separation maps genetics INTO the existing Line-Field-Set store, no second data model); ADR-0031 constrains-edge ADR-0009 (honest data — the durable genotype fact, re-derived from current evidence at plan time)
**Files to create/modify:**
- `scripts/model/client.py` -- Modify: extend `_extract_system_prompt` with the genetics genotype-fact instruction
- `tests/model/test_client.py` -- Modify: the genetics-mapping structural + non-tautological fixture assertions

**Acceptance Criteria:**
1. The genetics genotype-fact mapping rule is present in `_extract_system_prompt()`: the returned instruction string carries the gene+rsID→`item`, sample-date→`timepoint`, `dna-report`→`source`, alleles→`value` mapping AND a "capture ALL/every finding" directive AND a "do NOT store the report's interpretation" directive — verified by structural substring/token assertions on `_extract_system_prompt()`.
2. NON-TAUTOLOGICAL genetics-readings flow: with the fixture backend returning genetics-shaped readings, a genetics fixture A yields readings whose `item` carries a gene+rsID and `source == "dna-report"`, and a DIFFERENT genetics fixture B yields DIFFERENT genotype readings (B ≠ A) — verified through the `_FakeAnthropic`/`_patch_backend_client` harness at 0 live spend, proving the path carries the model's parse, not a code constant. (The model's actual adherence to the prompt is the LIVE run, OQ-1.)
3. Fact-not-interpretation: a genetics fixture's reading carries `value` = the allele call (e.g. `"(C;G)"`), NOT the trait/interpretation narrative — verified by a fixture asserting `value` is the alleles and the interpretation string is absent from the reading (no fabricated genotype — the value is the parse, not invented).
4. Scoped change: `git diff scripts/model/client.py` shows the only changed body is `_extract_system_prompt`; `extract_readings`, `_extract_content_block`, `_extract_output_schema` (NO schema change — `LINE_FIELDS` already fits the genotype fact), `deidentify`, `converse`, `author` are byte-unchanged — verified by the diff touching only `_extract_system_prompt`.
5. 0 live spend: every T3 test runs against a direct `_extract_system_prompt()` call or the fixture backend; no test makes a `key_source.resolve()`-gated live call — verified (mirrors the deid/extract 0-spend pins).
6. `.venv/bin/python -m pytest tests/model/test_client.py` passes.

**Risk Mitigations:** ADR-0031 honest-data (the durable genotype FACT, not the dated interpretation) — crit 1,3. ADR-0031 no-fabricated-genotype (the value is the model's parse, proven by the fixture non-tautology + the fail-closed contract inherited from `extract_readings`) — crit 2,3. ADR-0031 0-shared-routine-edit / single store (no second data model — `LINE_FIELDS` reused, no schema change) — crit 4. Scoped change (no collateral edit to the de-id/converse/author/extract surfaces) — crit 4.
**Dependencies:** None (entry point — edits the existing extract prompt; independent of T1/T2).

---

### ADR-0031-T4: Wire the Local-Extract-First Front Step into `route._extract_unrecognized` + Surface the Honest Signal

**Status:** TODO
**ADR Source:** ADR-0031, Decision (for an unrecognized-format PDF, extract the text LOCALLY before any model call, then send only the extracted TEXT to the no-train model — never the raw `document` block; the raw binary stays on the device); ADR-0031, Consequences Positive (strictly less egress — the raw PDF binary never leaves the device; new front step, 0 engine edit); ADR-0031, Falsification — Raw-binary-egress probe (0 raw-binary bytes egress to ANY endpoint) + Extend-not-rebuild (`git diff --numstat` = 0 on the frozen set) + Completeness/no-silent-truncation (the honest partial/too-large signal reaches the operator) + Confirm-gate (0 readings auto-land); ADR-0031 OQ-3 (the extracted-text + raw-binary residue handling)
**Files to create/modify:**
- `scripts/serve/route.py` -- Modify: the `_extract_unrecognized` PDF branch (local-extract → chunk) + the honest-signal return
- `tests/serve/test_route.py` -- Modify: the PDF text-path + crown-jewel + no-regression + signal + residue + numstat probes
- `scripts/serve/server.py` -- Modify: surface `partial`/`notes` in the `/upload` review payload
- `tests/serve/test_server.py` -- Modify: the partial-signal surfacing + route-table-unchanged re-assertion

**Acceptance Criteria:**
1. PDF local-extract-first routing: a `.pdf` unrecognized upload routes through `pdf_extract.extract_text(path)` then `extract_chunked.extract_all(text, client)` (the local-extract-first text path), NOT the raw-bytes `client.extract_readings(file_content, "application/pdf")` document path — verified by a test passing a `.pdf` staged file with `pdf_extract`/`extract_chunked` recorded (both called) and the raw-bytes document path NOT exercised.
2. CROWN-JEWEL raw-binary-egress (the load-bearing probe): for the PDF path the model client receives ONLY `text/plain` content (via `extract_chunked`); the raw PDF bytes (a seeded binary-only token NOT present in the extracted text) reach ONLY the local extractor and appear in NO `client.extract_readings` call — verified by a mock client recording every call's `(content, media_type)` asserting every `media_type == "text/plain"` AND the seeded raw-binary token is absent from every call's content. (The OS-egress-guard LIVE form is OQ-1, deferred.)
3. Non-PDF unchanged (no regression): a non-PDF unrecognized format (an `.png` / arbitrary text) still routes through the UNCHANGED `client.extract_readings(file_content, media_type)` (the ADR-0030 image/text path), with `pdf_extract.extract_text` NOT called — verified by asserting `pdf_extract` call count 0 on a non-PDF unrecognized upload, and the recognized wearable/DNA formats route as today.
4. Honest signal surfaced (non-tautological): when `extract_chunked` returns `complete=False`, the route's return carries `extraction_complete=False` + the note, AND the server `/upload` JSON review payload carries `partial: true` + the note(s); a complete extraction yields `partial: false` with `notes` empty — verified by a stubbed over-budget extraction asserting the payload's `partial`/`notes`, and a complete extraction asserting `partial: false`.
5. No auto-land (inherited confirm-gate): the PDF extraction path makes 0 `store.append` / 0 `dna.land` calls and `store.read_all(root) == []` after `/upload`; the readings are RETURNED for the operator-confirm step — verified.
6. OQ-3 / OQ-5 residue: neither the raw PDF binary nor the extracted text is written to any TRACKED path (outside the gitignored staged/dropzone prefixes, [`.gitignore:2-5`](../../../../.gitignore)); the staged temp file is discarded after extraction — verified by a post-route tracked-tree scan for a seeded token returning 0.
7. EXTEND-NOT-REBUILD: `git diff --numstat <fork-point> --` over `scripts/ingest/ingest.py` + `scripts/ingest/adapter.py` + every `scripts/plan/*.py` + `scripts/store/keying.py` + `scripts/store/store.py` emits 0 rows — verified by a numstat test extending the existing `_FROZEN_ENGINE_PATHS` pattern ([`tests/serve/test_route.py:386-413`](../../../../tests/serve/test_route.py)) with `keying.py` + `store.py` (the genetics readings land via the unchanged sink — `store.append` byte-frozen).
8. CROWN-JEWEL structural (no outbound surface added): `scripts/serve/` imports 0 outbound client (the standing grep, [`tests/serve/test_serve_no_egress.py:186-205`](../../../../tests/serve/test_serve_no_egress.py)) and the single-model-client-import `rg` returns 0; the new `scripts/ingest/pdf_extract.py` + `scripts/ingest/extract_chunked.py` import 0 outbound client / SDK — verified by the greps.
9. `.venv/bin/python -m pytest tests/serve/test_route.py tests/serve/test_server.py` passes.

**Risk Mitigations:** ADR-0031 crown-jewel raw-binary-egress (0 raw bytes to any endpoint; the model gets text only) — crit 2,8. ADR-0031 honest-completeness (the partial/too-large signal reaches the operator) — crit 4. ADR-0031 confirm-gate precondition (no auto-land) — crit 5. ADR-0031 OQ-3/OQ-5 (no tracked raw/text residue) — crit 6. ADR-0031 EXTEND-NOT-REBUILD (frozen engine + keying + store.append) — crit 7. No regression on the wired adapters / image-text path — crit 3.
**Dependencies:** ADR-0031-T1 (the `pdf_extract.extract_text` the route calls), ADR-0031-T2 (the `extract_chunked.extract_all` the route calls).

---

### ADR-0031-T5: SPA Honest-Partial Note on the Review Panel — No Silent "No New Data"

**Status:** TODO
**ADR Source:** ADR-0031, Decision (honest completeness — a too-large/garbled document surfaces a partial/too-large signal, NEVER a silent "no new data"); ADR-0031, Falsification — Completeness/no-silent-truncation (0 findings silently dropped with no operator-visible signal); ADR-0009 D2 honest-data (no invented data; the operator sees the true state)
**Files to create/modify:**
- `vault/design/templates/app_view.html` -- Modify: the partial-extraction note on the review panel + the inline-JS `partial`/`notes` branch
- `tests/serve/test_app_shell.py` -- Modify: the rendered-SPA partial-note assertions

**Acceptance Criteria:**
1. The rendered SPA review panel carries markup for a partial-extraction note (an element that displays the `notes` when the `/upload` payload's `partial` is true) — verified by parsing the rendered SPA HTML for the note element on the `Upload Documents`/review surface ([`app_view.html:485-487`](../../../../vault/design/templates/app_view.html)).
2. The inline JS, on a `/upload` response with `partial: true`, displays the note(s) in the review panel ALONGSIDE the extracted readings — verified by an `rg`/structural test over the rendered SPA asserting a `partial`/`notes` branch exists in the `showReview`/upload-response flow ([`app_view.html:745,773`](../../../../vault/design/templates/app_view.html)).
3. HONEST empty-vs-partial distinction (no false "no new data"): a `partial: true` response WITH readings renders BOTH the readings AND the note; a truly-empty extraction (no readings, not partial) renders the honest awaiting state — verified by asserting the two states render distinctly (a partial extraction is never collapsed into the empty/awaiting state).
4. The served SPA still passes the inline-asset render gate: `generate.run("app")` RETURNS a written path (does not raise the off-file-asset `ValueError`) — verified by a test asserting the returned path exists (the note adds no off-file asset reference).
5. `.venv/bin/python -m pytest tests/serve/test_app_shell.py` passes.

**Risk Mitigations:** ADR-0031 honest-completeness realized on the operator surface (the partial signal is operator-visible) — crit 1,2,3. ADR-0009 D2 honest-data (no false "no new data" on a partial extraction) — crit 3. ADR-0029 inline-asset gate (no off-file reference) — crit 4.
**Dependencies:** ADR-0031-T4 (the server `/upload` `partial`/`notes` payload shape the SPA consumes).

---

### ADR-0031-T6: End-to-End PDF Ingestion + the ADR-0031 Falsification Probes as Tests (Non-Tautological; Mock-Tested; 0 Live Spend)

**Status:** TODO
**ADR Source:** ADR-0031, Validation Approach — Confirmation (local-extraction-first testable at 0 live spend: a fixture PDF through `pdftotext` + the model-structuring mock; the model receives a `text` block never a `document` block; each reading carries the full Line-Field-Set) + Chunk-and-aggregate completeness + Genetics genotype-fact mapping + New-front-step-0-engine-edit; ADR-0031, Falsification (all six probes: raw-binary-egress, local-extractor-network, extend-not-rebuild, completeness/no-silent-truncation, confirm-gate, key-never-committed); ADR-0031, Decision (the full local-extract → chunk → structure → confirm → land path)
**Files to create/modify:**
- `tests/serve/test_pdf_ingestion_e2e.py` -- Create (absent today [VERIFIED `test ! -e` returns 0]): the headline E2E + the composed falsification probes; no new production code (binds the built mechanism)

**Acceptance Criteria:**
1. HEADLINE (non-tautological): a synthetic fixture PDF driven through `route_upload` (PDF → `pdf_extract` local-extract → `extract_chunked` → mock backend at the ADR-0015 seam returning scripted Line-Field-Set readings) → surfaced → `POST /confirm-extraction` → `store.append` lands the confirmed readings, AND the landed store readings TRACE to the FIXTURE's extracted values (a specific `(item, value)` appears in the store), NOT a constant — verified, NEVER merely "the store is non-empty". The full path runs real `pdftotext` where present (`skipif` poppler absent) AND a `pdf_extract`-stubbed form (always runs) so the chunk→structure→confirm→land path is exercised everywhere.
2. Failing-capable negative control: the SAME pipeline with the mock returning NO usable readings (or the operator confirming none) lands 0 readings (the honest no-data state) — verified, proving crit 1 distinguishes a landed reading from the no-data state.
3. CROWN-JEWEL raw-binary-egress (structural/mock): across the E2E the model client receives ONLY `text/plain` chunk content; the raw PDF bytes (a seeded binary token absent from the text) reach only the local extractor and appear in NO model call; `scripts/serve/` + the new ingest modules carry 0 outbound client — verified. (The OS-egress-guard LIVE run is OQ-1, deferred.)
4. COMPLETENESS / no-silent-truncation: a multi-chunk fixture lands ALL N chunks' readings (aggregated + deduped, 0 dropped, 0 duplicate) after confirm; an over-budget fixture surfaces `partial: true` + a note in the `/upload` payload (the honest signal reaches the operator), NEVER a silent empty / "no new data" — verified by both cases.
5. GENETICS genotype-fact (non-tautological): a genetics fixture (mock backend returning genotype-shaped readings) lands readings with `item`=gene+rsID, `timepoint`=sample-date, `source`=`dna-report`, `value`=alleles after confirm, and a DIFFERENT genetics fixture lands DIFFERENT genotype readings; `_extract_system_prompt()` carries the genetics mapping rule (cross-checks T3) — verified.
6. CONFIRM-GATE + LOCAL-EXTRACTOR-NETWORK: the store is empty after `/upload` and before `/confirm-extraction` (≥1 reading lands only after the confirm POST); the local extractor modules import 0 outbound client and `marker` is stubbed (no real heavy run / model download) — verified.
7. EXTEND-NOT-REBUILD checkpoint: `git diff --numstat <fork-point> --` over `scripts/ingest/ingest.py` + `scripts/ingest/adapter.py` + every `scripts/plan/*.py` + `scripts/store/keying.py` + `scripts/store/store.py` emits 0 rows — verified by the numstat assertion.
8. 0 LIVE SPEND: the E2E injects the mock backend at the ADR-0015 seam + synthetic fixtures and makes 0 `key_source.resolve()`-gated live call; deterministic + CI-runnable with no network and no key — verified by the suite passing under `.venv/bin/python -m pytest` + a mock-injection assertion.
9. `.venv/bin/python -m pytest tests/serve/test_pdf_ingestion_e2e.py` passes.

**Non-AC note (the LIVE run, ADR-0031 OQ-1).** The operator-present LIVE run — real key + the real 42-page genetics/SNP report + real spend + the OS-level egress-guard forms of the raw-binary-egress and local-extractor-network probes — is operator-gated, NOT a build criterion. It is documented in the test-module docstring, not asserted here. The key-never-committed scan (grep every tracked file + git history on a fresh clone for the API-key value; threshold 0) is a repo-wide release gate carried by the `block-pii-commit`/`pre-push` hooks, re-run at release, not a per-test AC.

**Risk Mitigations:** ADR-0031 the six Falsification probes (raw-binary-egress / local-extractor-network / extend-not-rebuild / completeness / confirm-gate / key-never-committed) — crit 3,4,6,7 + the release-gate note. ADR-0031 non-tautological headline (a feature plumbed but not proven to land a usable confirmed reading) — crit 1 (trace-to-fixture), crit 2 (failing-capable). Genetics genotype-fact end-to-end — crit 5. Live-API coupling — crit 8 (mock-tested CI; the live run is OQ-1).
**Dependencies:** ADR-0031-T4 (the wired local-extract route + the server `/upload`+`/confirm-extraction` path the E2E exercises directly), ADR-0031-T3 (the genetics genotype-fact prompt the E2E cross-checks).

---

## Dependency Map

```
ADR-0031-T1 --> ADR-0031-T4   (route._extract_unrecognized calls pdf_extract.extract_text — T1's module)
ADR-0031-T2 --> ADR-0031-T4   (route._extract_unrecognized calls extract_chunked.extract_all — T2's module)
ADR-0031-T4 --> ADR-0031-T5   (the SPA partial-note consumes T4's server /upload partial/notes payload)
ADR-0031-T4 --> ADR-0031-T6   (the E2E exercises T4's wired local-extract route + the confirm path directly, NOT T5's SPA markup)
ADR-0031-T3 --> ADR-0031-T6   (the E2E cross-checks T3's genetics genotype-fact prompt + lands genotype readings)
```

Entry points (no inbound edges): **ADR-0031-T1, ADR-0031-T2, ADR-0031-T3** (parallel — T1/T2 are independent local modules; T3 is an independent prompt edit).

Topological order (Kahn parallel groups):
1. **Group 1 (entry points, parallel):** ADR-0031-T1 (local text extraction), ADR-0031-T2 (chunk + aggregate + signal), ADR-0031-T3 (genetics genotype-fact prompt)
2. **Group 2:** ADR-0031-T4 (wire the front step into the route + surface the signal — after T1 + T2)
3. **Group 3 (parallel):** ADR-0031-T5 (SPA partial-note — after T4), ADR-0031-T6 (E2E + falsification probes — after T4 + T3)

Critical path: **ADR-0031-T1 (or T2) → ADR-0031-T4 → ADR-0031-T6** (length-3). T3 → T6 is length-2 (off the critical path); T5 is length-3 off T4 in parallel with T6, not lengthening the path.

No cycles (Kahn drains all 6 nodes: remove T1/T2/T3 with 0 inbound → T4's inbound from T1+T2 is satisfied → remove T4 → T5's inbound from T4 and T6's inbound from T4+T3 are satisfied → remove T5, T6; every edge points from an earlier group to a later group). T5 and T6 in Group 3 share no file (T5: `app_view.html`/`test_app_shell.py`; T6: `test_pdf_ingestion_e2e.py`).

**Wave-checkpoint Go/No-Go (the local-extraction-first gate):** the local extractor runs `pdftotext` primary + the `marker` fallback at 0 network with a fail-loud total-failure raise (T1), the chunk-and-aggregate path lands the UNION of all chunks deduped via the unchanged `keying` and surfaces an honest partial/too-large signal (T2), the genetics genotype-fact prompt captures the durable fact not the interpretation (T3), an unrecognized-format PDF routes through local-extract-first so the model receives `text/plain` not a `document` block and the readings do NOT auto-land (T4), the SPA surfaces the partial signal honestly (T5), the headline E2E lands the fixture's confirmed readings non-tautologically (T6), AND **the six ADR-0031 falsification probes are GREEN** (raw-binary-egress structural, local-extractor-network structural, extend-not-rebuild numstat, completeness/no-silent-truncation, confirm-gate, key-never-committed release scan), AND the frozen surfaces are byte-unchanged: `git diff --numstat <fork-point> -- scripts/ingest/ingest.py scripts/ingest/adapter.py scripts/plan/*.py scripts/store/keying.py scripts/store/store.py` reports 0 rows (NFR-3).

## Test Strategy

### Unit Tests
- **Scope:** `scripts/ingest/pdf_extract.py` (the `pdftotext`/`marker` two-tier + fail-loud, real-`pdftotext`-on-fixture + stubbed-subprocess), `scripts/ingest/extract_chunked.py` (the chunk/aggregate/dedupe/signal over a mock client), `scripts/model/client.py` (the `_extract_system_prompt` genetics mapping + the fixture-backend non-tautology), `vault/design/templates/app_view.html` (the rendered partial-note markup + inline JS).
- **Approach:** `pytest` with a synthetic fixture PDF (no PII) for the real-`pdftotext` run (`skipif shutil.which("pdftotext") is None`); STUBBED `pdftotext`/`marker` subprocesses for the branching + fallback logic (never a real heavy marker run / model download); a recording mock client injected into `extract_chunked` for the chunk/aggregate/dedupe/signal tests; the `_FakeAnthropic`/`_patch_backend_client` patched-SDK seam for the genetics fixture-backend tests (no live API, no key); an `rg`/parse over the rendered SPA HTML for the partial-note.
- **Criteria covered:** T1 crit 1-7; T2 crit 1-8; T3 crit 1-6; T5 crit 1-4.

### Integration Tests
- **Scope:** the cross-seam paths — (a) `route._extract_unrecognized` over a `.pdf` with `pdf_extract`+`extract_chunked` (T4); (b) the served `POST /upload` surfacing `partial`/`notes` (T4); (c) the headline E2E: synthetic fixture PDF → `/upload` local-extract → chunk → mock structure → surfaced → `/confirm-extraction` → `store.append` (T6).
- **Approach:** instantiate the production `IntakeRequestHandler` over tmp roots + an injected mock backend (the `test_serve_no_egress` `_build_post_handler` pattern); POST synthetic multipart/JSON bodies; assert the store state + the JSON review/confirm receipts; run real `pdftotext` where present + a `pdf_extract`-stubbed form everywhere.
- **Criteria covered:** T4 crit 1,3,4,5,9; T6 crit 1,2,4,5,8,9.

### Risk-Specific Tests
- **CROWN-JEWEL raw-binary-egress (ADR-0031, the load-bearing probe):** for a PDF the model client receives ONLY `text/plain`; the seeded raw-binary token reaches no model call; `scripts/serve/` + the new ingest modules carry 0 outbound client (T2 crit 2; T4 crit 2,8; T6 crit 3). Structural/mock at build; the OS-egress-guard LIVE run is OQ-1.
- **LOCAL-EXTRACTOR-NETWORK (ADR-0031):** `pdf_extract`/`extract_chunked` import 0 outbound client / SDK; `marker` stubbed (no real run / model download) (T1 crit 5; T2 crit 7; T6 crit 6). Structural at build; the OS-egress-guard LIVE 0-network form is OQ-1.
- **COMPLETENESS / no-silent-truncation (ADR-0031):** the N-chunk union aggregates deduped (0 dropped, 0 dup) and the over-budget honest signal reaches the operator, never a silent "no new data" (T2 crit 3,4,5; T4 crit 4; T5 crit 1,2,3; T6 crit 4).
- **EXTEND-NOT-REBUILD numstat (NFR-3):** `git diff --numstat <fork-point>` = 0 on `scripts/ingest/{ingest,adapter}.py` + `scripts/plan/*.py` + `scripts/store/keying.py` + `scripts/store/store.py` — the wave-checkpoint probe (T4 crit 7; T6 crit 7), extending the existing `_FROZEN_ENGINE_PATHS` pattern.
- **CONFIRM-GATE (inherited from ADR-0030):** the store is empty after `/upload`, readings land only after `/confirm-extraction` (T4 crit 5; T6 crit 6).
- **FAIL-CLOSED / no fabrication (ADR-0031 + ADR-0009):** a total extraction failure raises (T1 crit 6); a chunk `ModelCallError` propagates with 0 fabricated readings (T2 crit 6); the genotype value is the parse, not invented (T3 crit 2,3).
- **OQ-3 / OQ-5 LOCAL-RESIDUE (ADR-0005):** no tracked file carries the raw-binary OR the extracted-text token; the staged temp file is discarded (T4 crit 6; T6 residue scan).
- **GENETICS genotype-fact (non-tautological):** the durable fact (item=gene+rsID, source=`dna-report`, value=alleles) lands; a different genetics fixture lands different genotype readings (T3 crit 2,3; T6 crit 5).
- **Public-repo key/PII leak (MEMORY):** the key-never-committed scan (threshold 0 API-key hits) is the repo-wide release gate carried by the `block-pii-commit`/`pre-push` hooks (T6 release-gate note).

## NFRs (cross-cutting, each falsifiable, each tied to ADR-0031)

- **NFR-1 (crown-jewel PII boundary — ADR-0031 raw-binary-egress + local-extractor-network).** For a PDF, 0 raw-binary bytes egress to ANY endpoint (the model receives extracted TEXT only); 0 text bytes to any non-no-train endpoint; 0 network calls from the local extractor. The raw binary reaches only the local `pdftotext`/`marker` subprocess; the model client receives only `text/plain`; the single model-client SDK import stays inside `scripts/model/`. *Falsified if* the model client receives a `document` block for a local-extracted PDF, OR the raw-binary token reaches any model call, OR `scripts/serve/`/the new ingest modules import an outbound client, OR an SDK import appears outside `scripts/model/`. **Verification:** T2 crit 2; T4 crit 2,8; T6 crit 3,6 (structural/mock); the OS-egress-guard LIVE run is OQ-1 (deferred).
- **NFR-2 (honest data + completeness — ADR-0031 + ADR-0009).** Confirm-before-land is unchanged (no auto-land); a too-large/garbled document surfaces an operator-visible partial/too-large signal, NEVER a silent "no new data"; the genetics path stores the durable genotype FACT (not the dated interpretation); no fabricated genotypes; no silent truncation. *Falsified if* a partial extraction lands a silent subset with no operator-visible signal, OR a reading auto-lands before confirm, OR the genetics value stores the interpretation instead of the alleles, OR a failed extraction fabricates a reading. **Verification:** T2 crit 5,6; T3 crit 1,3; T4 crit 4,5; T5 crit 1,2,3; T6 crit 1,2,4,5.
- **NFR-3 (extend-not-rebuild — the frozen ingest engine + Line-Field-Set + `keying`/`store.append` + the `scripts/plan/*` engine).** `scripts/ingest/ingest.py`, `scripts/ingest/adapter.py`, every `scripts/plan/*.py`, `scripts/store/keying.py`, and `scripts/store/store.py` (the `store.append` sink) are byte-frozen; the local-extract step is a NEW front module (`scripts/ingest/pdf_extract.py` + `scripts/ingest/extract_chunked.py`), not an engine edit; genetics readings land via the unchanged sink. *Falsified if* `git diff --numstat <fork-point>` ≠ 0 on those files. **Verification:** T4 crit 7; T6 crit 7 (the wave-checkpoint numstat probe).
- **NFR-4 (fail-closed, no fabricated reading — ADR-0031 + ADR-0009).** A total local-extraction failure raises `PdfExtractError`; a chunk-level `ModelCallError` propagates with 0 fabricated readings; a malformed reading lands nothing (inherited from `confirm.land_confirmed`/`extract_readings`). *Falsified if* an extraction failure surfaces ≥1 fabricated reading or a false `complete`. **Verification:** T1 crit 6; T2 crit 6; T3 crit 2,3.
- **NFR-5 (0 live spend — mock/fixture-tested).** Every acceptance criterion is satisfiable with a MOCK no-train backend injected at the ADR-0015 seam + synthetic fixtures + a real `pdftotext` (`skipif`-gated) + a STUBBED `marker`; no test makes a live API call, reads a real key, or runs a real heavy `marker` / model download. *Falsified if* any build test makes a `key_source.resolve()`-gated live call or shells a real `marker` run. **Verification:** T1 crit 1(skip),3,4; T3 crit 5; T6 crit 8.
- **NFR-6 (OQ-3 no tracked residue — ADR-0005).** Both the raw uploaded binary and the extracted text are held in memory / the gitignored OS-temp staged path only and discarded after extraction; neither is written to a tracked path. *Falsified if* a tracked file (outside the gitignored dropzone prefixes) carries the raw-binary or extracted-text content after extraction. **Verification:** T4 crit 6; T6 residue scan (backstopped by `block-pii-commit`/`pre-push`).
- **NFR-7 (interface-pinned, internals-discretionary).** The build PINS the `pdf_extract.extract_text(pdf_path) -> str` contract, the `extract_chunked.extract_all(text, client) -> {"readings", "complete", "note"}` contract, the route's PDF text-path + the honest-signal return shape, the server `/upload` `partial`/`notes` payload keys, the genetics genotype-fact mapping rule, and every acceptance criterion. It does NOT pin the exact `_CHUNK_CHARS`/`_CHUNK_OVERLAP`/`_MAX_CHUNKS`/`_LOW_TEXT_CHARS` values (OQ-2, build-time tunable within the pinned contracts), the `pdftotext`/`marker` CLI flags, the chunk-split algorithm internals, or the SPA note's exact CSS/JS — implementer discretion.

## Amended-Criterion → Enforcing AC (ADR-0031 §amends ADR-0030)

ADR-0031 AMENDS ADR-0030's pinned file→model mechanism for an unrecognized-format PDF (ADR-0031 Decision / Related Decisions — the `depends-on (+ amends)` edge to ADR-0030). Each amended ADR-0030 criterion maps to the ADR-0031 build AC that enforces the new bound — so a future build that reverts to the raw-document-block default reds a specific AC:

| Amended ADR-0030 criterion | Scoped change (ADR-0031) | Enforcing build AC |
|---|---|---|
| ADR-0030's pinned file→model mechanism — a PDF egresses as a base64 `document` content block ([`client.py:303-320`](../../../../scripts/model/client.py)) | For an unrecognized-format PDF the raw `document` block is REPLACED by local-text-extraction-first → only `text/plain` to the model, chunked; the raw binary stays local | **T4 crit 1,2** (PDF routes through local-extract; the model receives `text/plain` not the document block), **T2 crit 2**, **T6 crit 3** |
| ADR-0030's single-call completeness (one `document` block bounded by one call's `max_tokens` output) | Replaced by chunk-and-aggregate so a dense document lands ALL its findings, deduped, with an honest partial/too-large signal | **T2 crit 3,5**, **T4 crit 4**, **T6 crit 4** |
| ADR-0001 / ADR-0016 egress class (the raw `document` block on the no-train lane) | TIGHTENED — the raw binary no longer egresses; only scopeable extracted text crosses the same no-train lane (strictly LESS egress) | NFR-1, **T4 crit 2,8**, **T6 crit 3** |

## Repo-Grounding Ledger

| Task | RGC-1 (manifest action vs disk) | RGC-2 (premise freshness) | RGC-3 (cited-input existence + declared shape) | RGC-4 (capability non-duplication) | Disposition |
|------|---------------------------------|---------------------------|-----------------------------------------------|-----------------------------------|-------------|
| T1 | pass — `pdf_extract.py`/`test_pdf_extract.py` Create=absent [VERIFIED `test ! -e` returns 0] | pass — `pdftotext` is present + local ([VERIFIED: poppler 26.02.0 at `/opt/homebrew/bin/pdftotext`]); `marker_single` is present ([VERIFIED: `~/.local/bin/marker_single` → marker-pdf]); both are local subprocesses (the ADR's two-tier premise holds) | pass — `subprocess` + `pathlib` stdlib; the `_OUTBOUND_CLIENT_MARKERS` grep set present ([`tests/serve/test_serve_no_egress.py:50-56`](../../../../tests/serve/test_serve_no_egress.py)); the SDK-absent `skipif` posture present (the deid/extract 0-spend pins); `scripts/ingest/adapters/whoop.py` already uses `subprocess` (subprocess in `scripts/ingest/` is precedented) | pass — no existing pdf-text extractor (grep for `pdftotext`/`marker_single`/`def extract_text` in `scripts/` returned 0); a NEW local-extraction front module, not a duplicate of the deterministic adapters | Grounded |
| T2 | pass — `extract_chunked.py`/`test_extract_chunked.py` Create=absent [VERIFIED] | pass — `client.extract_readings(file_content, media_type)` is LIVE ([`client.py:97-126,488-531`](../../../../scripts/model/client.py)); the `text` content block exists for a text media type ([`client.py:330-331`](../../../../scripts/model/client.py)); `_EXTRACT_MAX_TOKENS=16384` ([`client.py:279`](../../../../scripts/model/client.py)); `keying.dedupe_key`/`is_conformant` present ([`keying.py:19,35`](../../../../scripts/store/keying.py)) | pass — `keying.dedupe_key`/`is_conformant` (the shared key, REUSED) present; `ModelCallError` present ([`client.py:25-30`](../../../../scripts/model/client.py)); the injected-client pattern (`route_upload(..., client=...)`) present ([`route.py:68`](../../../../scripts/serve/route.py)) | pass — no existing chunk/aggregate module (grep returned 0); it CALLS `client.extract_readings` (injected) + REUSES `keying`, defining no second key — not a duplicate | Grounded |
| T3 | pass — `client.py`/`test_client.py` Modify=present [VERIFIED] | pass — `_extract_system_prompt` exists + already instructs the Line-Field-Set shape ([`client.py:282-300`](../../../../scripts/model/client.py)); `_extract_output_schema` already constrains each reading to `LINE_FIELDS` ([`client.py:334-360`](../../../../scripts/model/client.py)) — so the genotype fact (item/timepoint/source/value) needs NO schema change; the `_FakeAnthropic`/`_patch_backend_client` harness present | pass — `LINE_FIELDS` present ([`keying.py:11`](../../../../scripts/store/keying.py)); the genotype fact maps onto the existing 4 fields exactly; the fixture-backend non-tautology pattern present (the ADR-0030-T1 extract tests) | pass — extends the EXISTING extract prompt; adds no second prompt, no second data model (genetics maps INTO `LINE_FIELDS`, ADR-0031 non-goal #3); the existing `dna.land` 23andMe path is untouched ([`dna.py`](../../../../scripts/ingest/dna.py)) | Grounded |
| T4 | pass — `route.py`/`server.py`/`test_route.py`/`test_server.py` Modify=present [VERIFIED] | stale→actual — `_extract_unrecognized` currently reads `path.read_bytes()` + sends raw bytes to `client.extract_readings` ([`route.py:143-145`](../../../../scripts/serve/route.py)); the local-extract-first PDF branch is absent today; the `/upload` handler reads `result["extracted_readings"]` + writes `{"readings": extracted}` with NO `partial`/`notes` ([`server.py:206,247`](../../../../scripts/serve/server.py)) | pass — the `route_upload(..., client=...)` injected-client seam ([`route.py:68`](../../../../scripts/serve/route.py)); the `_FROZEN_ENGINE_PATHS` numstat pattern present ([`tests/serve/test_route.py:386-413`](../../../../tests/serve/test_route.py)); the `scripts/serve/` 0-outbound grep present ([`tests/serve/test_serve_no_egress.py:186-205`](../../../../tests/serve/test_serve_no_egress.py)); `.gitignore` dropzone prefixes present ([`.gitignore:2-5`](../../../../.gitignore)); `store.read_all` present | pass — extends the existing `_extract_unrecognized` seam (a PDF sub-branch) + the existing `/upload` payload (adds `partial`/`notes`); adds no second router, no store write — the no-auto-land contract is preserved | Grounded |
| T5 | pass — `app_view.html`/`test_app_shell.py` Modify=present [VERIFIED] | stale→actual — the `#review-panel` renders `extracted_readings` + an honest `data-awaiting='extraction'` empty state via `showReview` ([`app_view.html:485-487,745,773`](../../../../vault/design/templates/app_view.html)); there is NO partial-extraction note today | pass — the `#review-panel`/`#review-list`/`showReview` + the `fetch('/upload')`→`/confirm-extraction` flow present; the `generate.run("app")` inline-asset gate present | pass — the partial-note is NEW markup on the existing review panel; it reuses the `showReview`/upload-response posture, adds no off-file asset | Grounded |
| T6 | pass — `test_pdf_ingestion_e2e.py` Create=absent [VERIFIED `test ! -e` returns 0] | pass — the mock-client seam (`ModelClient(backend=...)`, [`client.py:44`](../../../../scripts/model/client.py)), the served-handler `_build_post_handler` pattern, the `_FROZEN_ENGINE_PATHS` numstat fork-point pattern, `confirm.land_confirmed` (the unchanged confirm→land sink, [`confirm.py:22-59`](../../../../scripts/serve/confirm.py)) all present + byte-unchanged | pass — `store.read_all`/`store.append`, the 0-outbound grep + single-import `rg`, the `.gitignore` dropzone prefixes (the OQ-3 residue scan) all present; `_extract_system_prompt` present (the T3 cross-check) | pass — the E2E is the absent headline proof; it binds the built mechanism, adds 0 production code | Grounded |

**Ledger notes.**
- **Module placement (T1/T2 RGC-4).** The two new modules live in `scripts/ingest/` (the local-extraction front), NOT `scripts/serve/`: `pdf_extract.py` (a file→text local-subprocess concern) and `extract_chunked.py` (a pure `(text, injected client) → readings` orchestration). The serve no-egress guard scans `scripts/serve/*.py` for outbound HTTP clients ([`test_serve_no_egress.py:50-56,186-205`](../../../../tests/serve/test_serve_no_egress.py)) — placing the subprocess-shelling extractor in `scripts/ingest/` keeps the serve layer subprocess-free, and the frozen-set numstat freezes only `ingest.py`/`adapter.py` (specific files), so a NEW file in `scripts/ingest/` is allowed. `route.py` imports both as it already imports `from scripts.ingest import dna, ingest`.
- **No schema change for genetics (T3 RGC-2).** `_extract_output_schema` already constrains each reading to `LINE_FIELDS` (item/timepoint/source/value) — the genotype fact maps onto those four fields exactly (item=gene+rsID, timepoint=sample-date, source=`dna-report`, value=alleles), so T3 is a PROMPT-only edit; no second data model, honoring ADR-0031 non-goal #3.
- **Frozen-set extension (T4/T6 RGC-3).** The ADR-0031 numstat probe extends the existing `_FROZEN_ENGINE_PATHS` (`ingest.py` + `adapter.py` + `scripts/plan/*.py`) with `scripts/store/keying.py` + `scripts/store/store.py` to also freeze `store.append`, matching the ADR's "0 edits to `store.append`" falsification.

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR-0031 section (Decision / Rationale / Consequences / Validation — Confirmation+Falsification / Open Questions / constrains-edge).
- [x] Every ADR ID in the `adrs` frontmatter (ADR-0031) has at least one task (T1-T6 all cite ADR-0031).
- [x] All ADR IDs resolve to actual ADR files on disk (`docs/adr/ADR-0031-local-extraction-first-pdf-ingestion.md` [VERIFIED]).

### Acceptance Criteria Quality
- [x] Every task has ≥1 acceptance criterion (T1 has 7; T2 has 8; T3 has 6; T4 has 9; T5 has 5; T6 has 9).
- [x] All criteria are binary — each cites a `pytest` target, a mock call-count, an `rg`/grep count, a `store.read_all` assertion, a `git diff --numstat`, a tracked-tree scan count, a `pytest.raises`, or a render-path return.
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient".

### File Manifest Integrity
- [x] Every task has a file manifest; every file in any task block appears in the top-level File Manifest and vice versa.
- [x] No task lists a directory instead of a specific file (the frozen-set globs are numstat probe targets in criteria, not manifest entries).
- [x] Every source file has a corresponding test file (`pdf_extract.py`→`test_pdf_extract.py`; `extract_chunked.py`→`test_extract_chunked.py`; `client.py`→`test_client.py`; `route.py`→`test_route.py`; `server.py`→`test_server.py`; `app_view.html`→`test_app_shell.py`; the E2E→`test_pdf_ingestion_e2e.py`).

### Dependency Map Integrity
- [x] No cycles (Kahn drains all 6 nodes; 3 ordered groups).
- [x] Every task ID in a Dependencies field appears as a node; every edge corresponds to a Dependencies entry; the entry points (T1, T2, T3) have "None (entry point)".
- [x] No phantom dependency — T4→T1 (route calls `pdf_extract.extract_text`), T4→T2 (route calls `extract_chunked.extract_all`), T5→T4 (SPA consumes the server `partial`/`notes` payload), T6→T4 (E2E drives the wired route+confirm path), T6→T3 (E2E cross-checks the genetics prompt); each edge names the artifact/surface that flows.
- [x] No missing dependency — file-level: T4 (`route.py`) imports T1's + T2's modules; T5 (`app_view.html`) consumes T4's payload; T6 drives T4's routes + cross-checks T3's prompt; every implicit edge is declared.

### Constraint Propagation
- [x] CROWN-JEWEL raw-binary-egress (0 raw bytes to any endpoint; model gets text only) carried as NFR-1 + T2 crit 2 + T4 crit 2,8 + T6 crit 3.
- [x] LOCAL-EXTRACTOR-NETWORK (0 network from the extractor) carried as NFR-1 + T1 crit 5 + T2 crit 7 + T6 crit 6.
- [x] HONEST DATA + COMPLETENESS (confirm-before-land; partial signal not silent "no new data"; genotype fact not interpretation) carried as NFR-2 + T2 crit 5,6 + T3 crit 1,3 + T4 crit 4,5 + T5 crit 1,2,3 + T6 crit 1,2,4,5.
- [x] EXTEND-NOT-REBUILD (frozen engine + keying + store.append numstat) carried as NFR-3 + the wave-checkpoint probe + T4 crit 7 + T6 crit 7.
- [x] FAIL-CLOSED (no fabricated reading / genotype) carried as NFR-4 + T1 crit 6 + T2 crit 6 + T3 crit 2,3.
- [x] OQ-3 LOCAL-RESIDUE (no tracked raw/text residue) carried as NFR-6 + T4 crit 6 + T6 residue scan.
- [x] 0 LIVE SPEND carried as NFR-5 + T1 crit 1(skip),3,4 + T3 crit 5 + T6 crit 8.

### Unresolved Concerns
- [x] Disposition section present (4 rows): OQ-1 Defer, OQ-2 Proceed, OQ-3 Proceed, OQ-4 Defer.
- [x] Defer dispositions justify why deferral is safe (OQ-1 operator-gated live run; OQ-4 operational, decision-invariant, smaller payload).
- [x] Proceed dispositions land as build criteria (OQ-2 = the `_CHUNK_*`/`_LOW_TEXT_CHARS` build-time constants in T1/T2; OQ-3 = T4 crit 6 / T6 residue scan).

### Risk Coverage
- [x] Risk Mitigations field on every task; every ADR-0031 negative consequence covered (the poppler/marker provisioning cost → the `marker`-stub + `skipif`-poppler discipline; the chunking latency/multiple calls → mock-tested, the live cost is OQ-1; `pdftotext` layout loss → the `marker` low-text fallback (T1); the genotype-in-one-`value` mapping → the `LINE_FIELDS` reuse (T3); the `marker` ~GB weight → paid only on the low-text trigger (T1 crit 3,4)).
- [x] The three ADR-0031 §amends scoped criteria (the document-block mechanism, single-call completeness, the egress class) each map to an enforcing build AC in the Amended-Criterion → Enforcing AC table.

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category.
- [x] Risk-specific tests exist for the crown-jewel raw-binary-egress, the local-extractor-network probe, completeness/no-silent-truncation, the extend-not-rebuild numstat, the confirm-gate, fail-closed, OQ-3 residue, and the genetics genotype-fact.

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status).
- [x] No placeholder text ("TBD", "TODO: fill in", "...").
- [x] The headline capability (local-extraction-first PDF ingestion through extract→chunk→structure→confirm→land) is a named end-to-end task (T6) testable against mocks + a fixture PDF at 0 live spend, with the LIVE run gated on OQ-1 (operator-present, real key + the real genetics report + real spend).

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists in the current worktree (`client.py`/`test_client.py`/`route.py`/`test_route.py`/`server.py`/`test_server.py`/`app_view.html`/`test_app_shell.py` [VERIFIED present]).
- [x] Every File Manifest `Create` row names a path that does NOT already exist (`pdf_extract.py`/`test_pdf_extract.py`/`extract_chunked.py`/`test_extract_chunked.py`/`test_pdf_ingestion_e2e.py` — all absent [VERIFIED]).
- [x] Every ADR premise a task relies on was re-verified against the current repo; stale-against-build premises (the raw-bytes `_extract_unrecognized`, the no-`partial`/`notes` `/upload` payload, the no-partial-note review panel) are recorded in the Repo-Grounding Ledger with the actual state.
- [x] Every cited input a task parses/reads declares its structural assumption AND the live file satisfies it (the `pdftotext`/`marker_single` binaries, the `client.extract_readings` text path + `_EXTRACT_MAX_TOKENS`, the `keying.dedupe_key`/`is_conformant` shared key, the `_extract_system_prompt`/`_extract_output_schema` over `LINE_FIELDS`, the `route_upload(client=...)` seam, the `_FROZEN_ENGINE_PATHS` numstat pattern, the `#review-panel`/`showReview` posture, the `confirm.land_confirmed` sink — all re-read/re-grepped).
- [x] No task proposes a new artifact that duplicates an existing capability (`pdf_extract`/`extract_chunked` are new local-extraction modules with no existing equivalent; the genetics mapping extends the existing extract prompt; the readings land via the unchanged `confirm.land_confirmed`/`store.append` sink).
- [x] Repo-Grounding Ledger present, one row per task, each with a disposition.
- [x] Module-placement + no-schema-change + frozen-set-extension decisions recorded in the Ledger notes.
