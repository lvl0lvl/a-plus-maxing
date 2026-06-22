---
scope: "ADR-0015 ADR-0016 ADR-0017 ADR-0018 ADR-0019: the conversational-intake agent — the swappable no-train model client, the /chat egress seam, the conversation→de-identified-store extractor, the demographic-form activation, and the SUMMARY_FIELD_SET extension"
adrs: [ADR-0015, ADR-0016, ADR-0017, ADR-0018, ADR-0019]
tier: 7
created: 2026-06-22
status: approved
---

# Spec: Conversational Intake Agent (Swappable Model Client + /chat + Extraction + Demographic Activation + Field-Set Extension)

## Component Overview

This spec delivers the conversational-intake agent — the build that closes the long-standing core-capability gap (PF-S63-02 / PF-S87-01 / bead `71s4`): a real conversation produces a *usable plan* through the existing assembly pipeline, not just working chat plumbing. It implements the five accepted conversational-intake ADRs as one dependency-ordered build over the live loopback server and the live plan-reasoning boundary.

The deliverable is five things, each grounded against the `feature/conversational-intake-foundation`-merged tree (`main` at `71eb853` as of 2026-06-22 S88 close): (1) **the swappable no-train model client** (ADR-0015) — the system's FIRST programmatic model boundary (a repo scan for `anthropic`/`openai`/`.messages.create`/`httpx`/`requests` over `scripts/` returns 0 today [VERIFIED]), a single module BOTH the intake conversation and the plan-author dispatch call through, defaulting to a Claude no-train commercial API and swappable at the seam, fail-closed on any failed/empty call, reading its API key at RUNTIME from an injectable source (env / macOS-keychain command) and NEVER a tracked file (the repo is PUBLIC); (2) **the `/chat` endpoint** (ADR-0016/0018) — a NEW sibling route on the unchanged `ThreadingHTTPServer(("127.0.0.1", port), ...)` (`scripts/serve/server.py:222`, `_LOOPBACK = "127.0.0.1"` at `server.py:29` [VERIFIED]) that carries one intake turn in / one turn out, making the system's first authorized outbound model call (live conversation raw, never store content); (3) **the conversation→de-identified-store extractor** (ADR-0017) — "model proposes, gate disposes": the model's extraction output passes through `capture`'s EXISTING value gates (`_bounded_value_ok` / `_value_has_pii` / by-data-class routing, `scripts/serve/capture.py:189-244` [VERIFIED]) BEFORE any `store.append`; (4) **the demographic-form activation** (ADR-0018) — the kept Step-1 "About you" layer (today four dead `_field(..., True)` placeholders outside the POSTing `capture_form`, `intake.py:258-266,408-413` [VERIFIED]) becomes working capture so the four orphan tokens `sex-for-dosing` / `bodyweight-band` / `equipment-access-class` / `training-age-band` (all `SUMMARY_FIELD_SET` members with no working input, `router.py:18-22` [VERIFIED]) get real inputs; (5) **the `SUMMARY_FIELD_SET` extension** (ADR-0019) — new de-identified nutrition/supplement/peptide/training-detail tokens, each a band/class derivation under the existing change-control tripwires (`router.py:307-313,329-349` [VERIFIED]), so the chat-extracted rich-section facts reach `compute_plan`'s domain translators (`_to_nutrition_plan` / `_to_supplements_plan` / `_to_peptides_plan`, `generate_plan.py:130-228` [VERIFIED]).

The build **reuses, never re-implements**, the live seams the data-in / data-out / intake-website waves already built. Reused byte-unchanged: `capture.persist_capture` (the de-identification gate, `capture.py:189` [VERIFIED]) and `store.append(item, reading, root)` (the NDJSON write + `(item,timepoint,source)` dedupe, `store.py:134-162` [VERIFIED]) — the extractor adds only the dialogue→facts *producer* in front of these (ADR-0017 Alternative C). Reused unchanged: `assemble`'s four safety filters + the clearance gate + the per-domain translators + `record_plan` (`generate_plan.py:60-62,94-101` [VERIFIED]) — ADR-0015 amends ONLY ADR-0006's dispatch *mechanism*, swapping the captured-envelope feed (`_author_callable`, `generate_plan.py:65-81` [VERIFIED]) for a programmatic call through the one client. Reused unchanged: `router.summarize` (the 0-raw-PII derivation boundary, `router.py:352-432` [VERIFIED]) — the question strategy reads ONLY this de-identified surface, and the plan-author summary stays summary-only. The content-upload transport (`route.route_upload` → `ingest.run`/`dna.land`, `route.py:58-93` [VERIFIED]) is byte-unchanged: the split moves the *rich sections* to chat, not the file uploads.

These five decisions form the "conversational-intake" cut of the V1 architecture, in DAG order ADR-0016 → ADR-0015 → {ADR-0017 ∥ ADR-0018} → ADR-0019. The build orders into two waves by that DAG: **Wave A** = the model client + the `/chat` transport + the extractor + the plan-author wiring (the model boundary and the conversation path — ADR-0015/0016/0017 plus the ADR-0015 plan-author re-wire); **Wave B** = the demographic-form activation + the `SUMMARY_FIELD_SET` extension (the form-side activation and the token-vocabulary widening that lets the chat-extracted rich facts reach the planner — ADR-0018/0019). The headline acceptance — a real-or-fixture conversation producing a usable plan end-to-end — is exercisable against MOCKS/fixtures with no live API (the model client is swapped for a fixture at the seam); the LIVE end-to-end run (real conversation → real plan) is gated on the runtime keychain API key, an operator-run check, not a CI gate.

**The crown-jewel PII boundary (NFR-1, load-bearing).** Exactly three data classes cross exactly these boundaries (ADR-0016/0017 §4 of the design): the **live conversation (raw)** MAY egress raw — but ONLY on the one `/chat` model call, on the no-train lane (ADR-0016); the **de-identified context** for the next ask (token names, bands/classes, booleans) MAY egress de-identified; the **persisted fact** crosses to the plan model only as a de-identified `SUMMARY_FIELD_SET` band/class through the unchanged `router.summarize` path. Nothing raw is EVER committed: the raw transcript is transient (in-memory for the live session), any residue lands ONLY on a gitignored surface (`vault/scaffold/filled/`, `vault/store/` are gitignored, `.gitignore:4-5` [VERIFIED]), and the registered `block-pii-commit.sh` PreToolUse hook + the `pre-push-pii-scan.sh` backstop deny a committed filled-value path. The 0-shared-routine-edit invariant (ADR-0003-T2 — `scripts/ingest/ingest.py`/`adapter.py`/`scheduler.py` byte-unchanged) and the store-adversarial-test battery (`docs/checklists/store-adversarial-tests.md`) apply to any `scripts/store/` surface this build touches.

### Token / Field Map (grounded against the closed `SUMMARY_FIELD_SET`)

Every "wired de-identified" token below is verified ∈ `SUMMARY_FIELD_SET` at `router.py:18-36` [VERIFIED]. The map fixes WHICH structure each new ADR-0019 token joins (the design §3.2 integration contract); the exact token vocabulary + band/class cuts are an in-scope spec decision pinned in `ADR-0019-T1` per the named criteria, NOT a deferral.

| Intake surface | Captured input | Class | Persistence target | Consumer |
|----------------|----------------|-------|--------------------|----------|
| Form Step-1 — demographics | birth year | wired derived (`training-age-band` ← `date-of-birth` via `_age_band`, `router.py:80,192`) | `store.append("date-of-birth", …)` (named-excluded raw source) → `summarize` derives the band | `summarize` → `assemble` |
| Form Step-1 — demographics | sex | wired pass-through (`sex-for-dosing`) | `store.append("sex-for-dosing", source:"intake")` | `summarize` → `assemble` |
| Form Step-1 — demographics | bodyweight | wired pass-through derived band (`bodyweight-band`) | `store.append("bodyweight-band", …)` (de-identified band, never raw kg) | `summarize` → `assemble` |
| Form Step-1 — demographics | equipment access | wired pass-through (`equipment-access-class`) — distinct from the `postal-address`→`equipment-access-class` derivation already mapped at `router.py:81`; ADR-0018-T1 must reconcile (see ADR-0018-T1 AC) | `store.append` per the reconciled wiring | `summarize` → `assemble` |
| Form Step-1 — uploads | DNA / HealthKit / labs | (unchanged) | `route.route_upload` → `ingest.run`/`dna.land` (byte-unchanged) | ingest seam |
| Chat — goals | goal-domains, goal-targets, goal-priority-order, hard-limits | wired de-identified (existing `WIRED_TOKENS`, `capture.py:50-56`) | extractor → `persist_capture` → `store.append`, `source:"intake"` | `summarize` → `assemble` |
| Chat — training (detail) | recovery-status-band | wired de-identified (existing) | extractor → `persist_capture` → store | `summarize` → `assemble` |
| Chat — training (around) | train-around / injury free-text | wired derived (`active-issue-class` ← `raw-symptom-free-text`, `capture.py:69-70`, `router.py:83`) | extractor → `persist_capture` → `store.append("raw-symptom-free-text")` (named-excluded raw source) | `summarize` derives the class |
| Chat — training (volume/detail) | split / weekly-volume / modality | **NEW ADR-0019 raw-backed-derived** band/class tokens (kind-2; chat-sourced, distinct from demographic `training-age-band`) | extractor → `persist_capture` → store (raw source named-excluded) → `summarize` derives the band | `summarize` → `_to_workout_plan` meta / roster |
| Chat — nutrition | dietary pattern / allergens / meals | **NEW ADR-0019 raw-backed-derived** band/class tokens (kind-2) | extractor → `persist_capture` → store → `summarize` derives | `summarize` → `_to_nutrition_plan` |
| Chat — supplements | supplement stack | **NEW ADR-0019 raw-backed-derived** class tokens (kind-2) | extractor → `persist_capture` → store → `summarize` derives | `summarize` → `_to_supplements_plan` |
| Chat — peptides | peptide stack | **NEW ADR-0019 raw-backed-derived** class token (kind-2) | extractor → `persist_capture` → store → `summarize` derives | `summarize` → `_to_peptides_plan` |
| Chat — Rx-interaction | medications named in dialogue | record-only (`rx-interaction-classes` is a curated-untrusted kind-3 token, DELIBERATELY absent from `WIRED_TOKENS`, `capture.py:57-64`) | `persist_capture` routes record-only → gitignored scaffold | none (model-bound item fed only by the deferred liaison curation surface, ADR-0014 OQ-2) |

**Token-kind discipline (ADR-0019 §3.2, non-negotiable).** Every new ADR-0019 token is **kind-2 (raw-backed-derived)**: a raw input lands in a named-excluded store item and `summarize` derives the band/class via `_RAW_TO_FIELD` → `_FIELD_DERIVATION` (`router.py:80-85,301-305`). On this path **there is NO 8j6 per-value PII scan** — `router.py:406-412` runs the derivation with no `scan_text` call; the 8j6 raise runs only on the pass-through `else` path (`router.py:416-430`). So a new token's de-identification MUST be proven by its derivation's COARSENESS via an independent per-token output scan (ADR-0019-T1 AC), NOT by the 8j6 gate. A new token added to NEITHER `SUMMARY_FIELD_SET` NOR a derivation reads through `summarize`'s else-branch under its own raw name — exactly the leak the module-load tripwires red on (`router.py:312-313`).

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0015 OQ-1 | Open Question | Claude no-train default vs a non-Claude provider behind the same seam | Proceed | The seam makes the provider non-binding (swappable); the build records a Claude no-train API as the DEFAULT and keeps the swap a one-module edit. A later non-Claude preference changes only the default, not the single-boundary architecture. `ADR-0015-T1` builds the seam swap-clean (criterion: swapping the provider edits ≤1 file outside the client). |
| ADR-0015 OQ-2 | Open Question | The exact boundary contract the swap seam exposes (the minimal cross-provider interface) | Proceed | The build FIXES the two-method shape the two callers need — a conversation-turn call and a structured-author call — as the client's public interface (`ADR-0015-T1` AC), without pinning the internal SDK request/response. That shape is the load-bearing swap surface; the wire detail is implementer discretion (NFR-5). |
| ADR-0015 OQ-3 | Open Question | The EXACT retry/backoff + degrade-vs-surface mechanics per consumer | Proceed | The fail-closed PRINCIPLE is decided (no fabricated/partial plan or extraction on a failed call). The build fixes a concrete, testable mechanic per consumer in `ADR-0015-T2`/`ADR-0015-T3`/`ADR-0017-T1` (intake: surface-error + degrade-to-form, no store write; plan-author: honest no-plan state). The exact retry COUNT/backoff curve is tuning the spec sets a default for and a follow-up may revise; the no-fabricated-result contract holds regardless. |
| ADR-0016 OQ-1 | Open Question | The precise no-train retention window for raw conversation | Defer | A vendor-policy fact (the ~30-day no-train profile, window UNVERIFIED) that quantifies the accepted bounded-retention exposure but does not change any build interface; the decision (B accepts bounded retention) stands. Tracked as a doc/policy follow-up owned in ADR-0016; no task gates on the exact window. |
| ADR-0016 OQ-2 / ADR-0017 OQ-2 | Open Question | The exact local-residue handling for the raw transcript (in-memory-only vs gitignored-scaffold-for-replay vs discard-after-extraction) | Proceed (in-memory + per-turn-discard this build) | The egress/retention posture is settled by ADR-0016 (transient for the live session; off-device = the no-train bounded window; nothing raw committed). This build pins **per-turn extraction + in-memory transcript discarded after each turn's extraction** (CONCERN-2 decided below), so no raw transcript is held to session end and no scaffold replay file is written for the transcript itself. `ADR-0016-T1`'s tests assert no raw transcript reaches any tracked OR gitignored-persistent surface beyond the live request; the `block-pii-commit`/pre-push backstop guards the residual. |
| ADR-0017 OQ-1 / ADR-0014 OQ-1 | Open Question | Which de-identified tokens must be minted for chat nutrition/supplement/peptide/training-detail | In scope (Wave B) | This is exactly what `ADR-0019-T1` decides — ADR-0019 IS the resolution of the deferred ADR-0014/0017 OQ-1. The exact vocabulary + cuts are pinned at spec/build time under the named coarseness + tripwire criteria, NOT deferred. |
| ADR-0018 OQ-1 | Open Question | Which exact demographic field fills which orphan token + each token's derivation | In scope (Wave B) | `ADR-0018-T1` fixes the field→token wiring (birth year → `training-age-band` via `_age_band`; sex → `sex-for-dosing`; bodyweight → `bodyweight-band`; equipment → `equipment-access-class`) and reconciles the existing `postal-address`→`equipment-access-class` derivation collision (AC below). |
| ADR-0018 OQ-2 | Open Question | The form-vs-chat classification rule for a borderline (partly-objective, partly-interplay) input | Proceed | The build applies the design's rule: an input that is a bounded selection or a file upload → form; an input whose value is the rich-section interplay → chat (`ADR-0018-T1` keeps the form to demographics + uploads only, 0 rich-section form fields — the falsifiable confirmation criterion). A genuinely borderline future input re-opens the topology decision (ADR-0018 review trigger); none in THIS build is borderline. |
| ADR-0019 OQ-2 | Open Question | All-at-once vs phased per-domain field-set extension | Proceed (all-at-once this build) | Phased is a valid sequencing option (ADR-0019 Alternative C) but leaves un-minted domains in the PF-S87-01 gap longer and spreads change-control churn. This build mints all four domains in one reviewed batch (`ADR-0019-T1`), and `ADR-0017-T2`'s CONCERN-1 criterion makes the divergence-window contract hold even so (a token-not-yet-minted domain reports record-only, never `domain_done`) — so a later phased token is safe regardless. |
| Design CONCERN-1 | Contract gap (§1.3 ↔ §3.2) | A chat-covered domain whose ADR-0019 token is not yet minted must route record-only AND must not let the question loop terminate thinking it is "done" | In scope (Wave A) | `ADR-0017-T2` builds the question-strategy `domain_done` as STORE-grounded + explicit-decline (never turn-count / model say-so), and a chat-covered domain with no `SUMMARY_FIELD_SET` token reports "captured-for-record, not-planned", never `domain_done` — the explicit PF-S87-01 anti-gap criterion. |
| Design CONCERN-2 | Contract gap (§2 ↔ §3) | Extraction cadence — per-turn vs end-of-session — is unfixed by any ADR | In scope, DECIDED per-turn (Wave A) | The build fixes **per-turn extraction**: the extractor runs on each `/chat` turn so (a) `summarize`'s `missing_fields` gap-set is live each turn and (b) the raw transcript residency is short (a turn, not a session). `ADR-0016-T1`'s `/chat` response returns the per-turn capture receipt; `ADR-0017-T1`'s extractor is invoked per turn. |
| Design CONCERN-3 | Coherence (§3.1 free-text residual) | The documented `_value_has_pii` free-text residual (a clinical diagnosis typed into a goals field is not caught) now applies to model-emitted free-text | Proceed (no NEW gap; bound the AC) | The same accepted V1 residual (`capture.py:88-95`), correctly inherited. The build's extraction AC must NOT claim the gate catches clinical PHI in a free-text token (that would be a tautological/false test); it asserts the gate catches identity/contact PII (email/phone/postal/identity tokens) and the residual stands for both form and extractor. |
| Design H-2 | Wiring gap (High) | `identity_config` is dropped at today's `/upload` `persist_capture` call site (`server.py:158-160` calls it WITHOUT `identity_config`), so operator-IDENTITY PII detection is empty | In scope (Wave A) | A factory-to-component wiring gap of exactly the class the project mandates warn about. `ADR-0017-T1` REQUIRES threading the instance `identity_config` into BOTH the new `/chat` capture call AND the existing `/upload` call site (the same gate, same instance) — a wiring acceptance criterion, not a deferral. |
| Design H-1 | Coherence (corrected) | The plan-author model seam is `generate_plan._author_callable`'s captured-envelope feed, NOT `router.dispatch` (`dispatch` has 0 production callers) | In scope (Wave A) | `ADR-0015-T3` wires the ONE client into `_author_callable`'s envelope production; `router.dispatch` is left unwired (ADR-0015 does not require wiring it). The build does NOT introduce a second model call at `dispatch`. |

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/model/__init__.py` | Create | Package marker for the one model boundary. |
| `scripts/model/client.py` | Create | The swappable no-train model client (ADR-0015): the SINGLE programmatic model boundary, a two-method public interface (`converse(...)` for an intake turn, `author(domain, summary)` for the plan-author envelope), default = a Claude no-train commercial API, swappable at the seam; fail-closed on a failed/empty/errored/timed-out call. Reads the API key at RUNTIME from an injectable key source (env var / a keychain-fetch command), NEVER a tracked file. |
| `scripts/model/key_source.py` | Create | The injectable runtime key source: resolves the no-train API key from an env var or a macOS-keychain `security find-generic-password` command at call time; raises fail-loud if absent. Never reads/writes a tracked file; the key never lands in the repo. |
| `scripts/serve/chat.py` | Create | The `/chat` turn handler logic (the question-strategy + extractor + capture wiring for one turn), kept out of `server.py`'s HTTP plumbing: `plan_next_turn` (the de-identified gap-set strategy), the per-turn dispatch (strategy → client.converse → extractor → `persist_capture` → receipt), and the fail-closed degraded turn. |
| `scripts/serve/extract.py` | Create | The conversation→facts extractor (ADR-0017): `extract_facts(model_extraction_output, turn_text) -> ExtractionResult{candidate_facts, declined_domains, dropped}`; validates the model proposal (never trusts it), routes the well-formed `candidate_facts` UNCHANGED to `capture.persist_capture` (the gate). Adds NO `store.append` path of its own. |
| `scripts/serve/server.py` | Modify | Add the POST `/chat` sibling route (route table → {GET `/`, POST `/upload`, POST `/chat`}); the bind literal `_LOOPBACK` is byte-unchanged. Thread the instance `identity_config` into the `/chat` capture call AND the existing `/upload` `persist_capture` call (the H-2 wiring fix). |
| `scripts/serve/capture.py` | Modify | Extend `WIRED_TOKENS` / `_BOUNDED_ENUMS` / `_FREE_TEXT_TOKENS` ONLY as the new ADR-0019 kind-2 tokens and the Step-1 demographic tokens require (the load-time `WIRED_TOKENS ⊆ SUMMARY_FIELD_SET` tripwire at `capture.py:152` stays green); `persist_capture`'s routing/gate logic is otherwise unchanged. |
| `scripts/plan/router.py` | Modify | Extend `SUMMARY_FIELD_SET` with the new ADR-0019 nutrition/supplement/peptide/training-detail tokens and the Step-1 demographic-derived tokens; add each new raw-backed-derived token's `_RAW_TO_FIELD` entry + `_FIELD_DERIVATION` band/class function; keep the module-load disjointness tripwires green (`router.py:307-313,329-349`). |
| `scripts/plan/generate_plan.py` | Modify | Re-wire `_author_callable` so the plan-author envelope is produced by a programmatic call through `scripts/model/client.py` (the ADR-0015 H-1 seam) — `assemble`'s filters, the clearance gate, the translators, and `record_plan` UNCHANGED; fail-closed to the honest no-plan state on a failed author call. |
| `vault/design/templates/intake.py` | Modify | Activate Step-1: convert the four dead `_field(..., True)` demographic placeholders (`intake.py:258-266`) into real POSTing form inputs inside `capture_form` (`intake.py:408-413`); add the chat surface affordance (a `/chat` panel) replacing the rich-section Steps 3-5 wizard fields. Build the demographic `<select>`/inputs from the same constants the capture gate validates against (no markup↔gate drift). |
| `scripts/model/keychain-setup.md` | Create | Operator runbook: how to store the no-train API key in the macOS keychain so `key_source.py` fetches it at runtime (NOT a secret, a doc). |
| `tests/model/test_client.py` | Create | The client is the single model import point; both consumers route through it; fail-closed on a failed/empty call (a fixture/mock client, no live API); the swap edits ≤1 file outside the client. |
| `tests/model/test_key_source.py` | Create | The key source resolves from env / keychain-command at runtime; absent key fails loud; no tracked file is read; a grep test asserts no API key literal in the tracked tree. |
| `tests/serve/test_chat.py` | Create | `/chat` is a loopback sibling route (one turn in/out); the ONE outbound call carries live conversation + de-identified context and nothing else; a failed model call returns a degraded turn (no fabricated turn/fact, no store write) and never kills the thread; the per-turn capture receipt reports what landed. |
| `tests/serve/test_extract.py` | Create | The extractor reaches the store ONLY via `persist_capture`'s gate; a model-emitted raw value under a token name routes record-only/rejected; a non-dict / unparseable proposal yields `candidate_facts={}` + `dropped`, writes nothing, never raises into the thread; the partial/garbled case (M-3) keeps well-formed facts + lists dropped + the receipt reports what landed. |
| `tests/serve/test_chat_no_egress.py` | Create | The `/chat` turn dispatch over a mock client makes 0 outbound calls beyond the one client call; a `rg` test asserts `scripts/serve/` imports no outbound HTTP client of its own (the only model egress is via `scripts/model/`); the de-identified-context-only assertion (no store content, no other operator's transcript in the model payload). |
| `tests/serve/test_question_strategy.py` | Create | `plan_next_turn` reads ONLY the de-identified `summarize` summary (instance-bound `store_read`); `domain_done` is store-grounded + explicit-decline (never turn-count/model say-so); a token-not-yet-minted chat-covered domain reports record-only, never `domain_done` (CONCERN-1); malformed control inputs raise (fail-loud). |
| `tests/serve/test_capture.py` | Modify | Extend the per-wired-field round-trip to the new demographic + ADR-0019 tokens (capture → `store.read(token)` → `summarize` returns it); record-only fields land ONLY under `vault/scaffold/filled/`; the H-2 `identity_config` threading round-trip (an operator-identity token in a free-text value routes record-only WITH `identity_config` threaded). |
| `tests/serve/test_capture_store_adversarial.py` | Modify | Extend the store-adversarial battery to the new token write paths (cross-stream collision, same-timepoint dedupe, dedupe-key boundary, mutation observed RED) per `docs/checklists/store-adversarial-tests.md`. |
| `tests/plan/test_router.py` | Modify | Per-new-token: the derived token is a de-identified band/class (a crafted raw value seeded at the source item → 0 raw value in the emitted token — the INDEPENDENT per-token output scan, NOT the 8j6 gate); the module-load disjointness tripwires stay green with the extended set. |
| `tests/plan/test_generate_plan.py` | Modify | The plan-author envelope is produced via the model client (a mock/fixture client at the seam); `core-capability-audit.sh --self-test` shape passes with the programmatic author path; a failed author call yields the honest no-plan state, never a fabricated/degraded plan. |
| `tests/serve/test_intake_demographics.py` | Create | Step-1 demographics POST and persist; the four orphan tokens (`sex-for-dosing`/`bodyweight-band`/`equipment-access-class`/`training-age-band`) each derive from a real input (0 orphans, against today's 4); the form carries 0 rich-section fields (rich sections are chat-only); a content upload still routes through `route_upload`, not chat. |
| `tests/plan/test_conversation_to_plan_e2e.py` | Create | The HEADLINE end-to-end (PF-S87-01): a fixture conversation (mock client) → `/chat` turns → `persist_capture` → `summarize` → `generate_plan`/`compute_plan` → a USABLE rendered plan covering the chat-sourced rich domains; testable with NO live API; a docstring-noted live-API-gated variant (real conversation → real plan) gated on the runtime keychain key. |

## Tasks

### ADR-0015-T1: The Swappable No-Train Model Client + Runtime Key Source (Single Model Boundary)

**Status:** TODO
**ADR Source:** ADR-0015, Decision (one swappable no-train model client as the single programmatic model boundary; default Claude no-train; swappable at the seam); ADR-0015, Consequences "Fail-closed on a failed model call"; ADR-0015, Validation Approach (Confirmation: single import point, both paths route through it; Falsification: a model call outside the client seam, >1 caller-side edit to swap the provider); ADR-0015 OQ-1/OQ-2 (default provider + boundary-contract shape — pinned here)
**Files to create/modify:**
- `scripts/model/__init__.py` -- package marker
- `scripts/model/client.py` -- the client: a two-method public interface `converse(...)` (an intake turn) + `author(domain, summary)` (the plan-author envelope), default Claude no-train, swappable at the seam; fail-closed on a failed/empty/errored/timed-out call
- `scripts/model/key_source.py` -- the injectable runtime key source (env var / macOS-keychain `security find-generic-password` command); fail-loud on an absent key; reads/writes NO tracked file
- `scripts/model/keychain-setup.md` -- the operator runbook for storing the key in the keychain
- `tests/model/test_client.py`, `tests/model/test_key_source.py`

**Acceptance Criteria:**
1. The client is the SINGLE model import point: an `rg` over `scripts/` for any model-client import (`anthropic`/`openai`/`.messages.create`/`httpx`/`requests`) finds them ONLY inside `scripts/model/`, against today's baseline of 0 anywhere (`rg` over `scripts/` returns 0 [VERIFIED]) — verified by the grep test asserting 0 model-client imports outside `scripts/model/`.
2. The client exposes EXACTLY the two-method boundary both callers need — `converse(...)` (one intake turn → assistant text + a structured extraction proposal) and `author(domain, summary)` (→ the plan-author envelope `{"specialist": slug, "recommendations": [...]}` or the thin-library sentinel `assemble` consumes, `generate_plan.py:37` [VERIFIED]) — verified by constructing the client with a fixture/mock backend and asserting both methods return their contracted shape (no live API).
3. The provider is swappable at the seam: swapping the default Claude no-train backend for an alternate edits ≤1 file outside the client module (ADR-0015 Falsification: >1 caller-side edit = ossified) — verified by a test that constructs the client with an injected alternate backend (the seam parameter) and exercises both methods, asserting 0 edits to either caller (`scripts/serve/chat.py`, `scripts/plan/generate_plan.py`) are needed to swap.
4. A failed / empty / errored / timed-out model call FAILS CLOSED: the client raises a typed failure (never returns a fabricated or silently-partial result) — verified by injecting each failure mode into the mock backend and asserting the typed raise, and asserting the method NEVER returns a partial/fabricated payload (ADR-0015 Falsification: ≥1 fabricated/partial result = breach).
5. The API key is fetched at RUNTIME from the injectable key source — `key_source.resolve()` reads an env var or runs the keychain-fetch command at call time; an absent key raises fail-loud naming how to set it; NO tracked file holds the key — verified by `tests/model/test_key_source.py` (resolves from a set env var; raises on an unset one; reads no tracked file) AND a grep test asserting 0 API-key literal in the tracked tree.
6. `pytest tests/model/test_client.py tests/model/test_key_source.py` passes (no live API — the backend is a fixture/mock).

**Risk Mitigations:** ADR-0015 Negative-2 (the swap seam ossifies if shaped to one provider) — criterion 3 caps the swap at ≤1 file. ADR-0015 Negative-1 (first hard commercial-API dependency) — criteria 2,3 keep the boundary swap-ready. ADR-0015 fail-closed contract — criterion 4. Public-repo key leak (MEMORY: no operator PII / secret in tracked text) — criterion 5 keeps the key out of the repo.
**Dependencies:** None (entry point — the model boundary every other model-touching task routes through). Blocks: ADR-0015-T2, ADR-0015-T3, ADR-0016-T1, ADR-0017-T1.

---

### ADR-0015-T2: Question Strategy — De-Identified Store-Grounded Gap-Set (Hybrid, CONCERN-1)

**Status:** TODO
**ADR Source:** ADR-0018, Decision (the conversational agent owns the rich sections); design §1 (the hybrid: code owns the de-identified gap-set + `domain_done`/`intake_complete`, the model owns phrasing within the gap set); design CONCERN-1 (a token-not-yet-minted domain reports record-only, never `domain_done`); ADR-0015 fail-closed (the strategy reads only the de-identified surface)
**Files to create/modify:**
- `scripts/serve/chat.py` -- `plan_next_turn(summary, covered_domains, declined_domains) -> TurnIntent{target_domain, missing_fields, domain_done, intake_complete}` (the strategy half; the per-turn dispatch lands in ADR-0016-T1)
- `tests/serve/test_question_strategy.py`

**Acceptance Criteria:**
1. `plan_next_turn` reads operator-capture state ONLY through the de-identified `router.summarize(store_read)` surface (`router.py:352` [VERIFIED]) — never the raw transcript, never the gitignored scaffold; the `store_read` is the instance-root-bound reader (`functools.partial(store.read, root=instance_root)`, the `summarize` caller contract, `router.py:366-380` [VERIFIED]) — verified by `rg` finding 0 raw-transcript / scaffold read in the strategy AND a test that a non-instance-bound reader is rejected or the call site binds the root.
2. `domain_done` is STORE-grounded + explicit-decline: a domain is done when every `SUMMARY_FIELD_SET` token mapped to it is PRESENT in `summary` OR the operator declined it — verified by a test that a domain with a missing token is NOT done (even after N turns) and a declined domain IS done; a test asserts `domain_done` does NOT rest on turn count or model say-so (the PF-S87-01 anti-gap).
3. CONCERN-1: a chat-covered domain whose ADR-0019 token is NOT yet minted (an empty `missing_fields` for a not-planner-feeding domain) reports "captured-for-record, not-planned" and is NEVER reported `domain_done` vacuously — verified by a test with a chat-covered domain absent from `SUMMARY_FIELD_SET` asserting the record-only state, not `domain_done`.
4. `TurnIntent` carries NO raw operator string — only token NAMES, domain names, and booleans (`missing_fields ⊆ SUMMARY_FIELD_SET`) — verified by a test asserting the returned intent's values are token/domain names + booleans, 0 raw turn text.
5. Malformed control inputs raise fail-loud: a `target_domain`/`covered_domains`/`declined_domains` member outside the chat-covered set, a `declined_domains ⊄ covered_domains`, or a non-dict `summary` raises (never silently corrupts loop termination) — verified per case.
6. `pytest tests/serve/test_question_strategy.py` passes.

**Risk Mitigations:** Design §1.2 (a silently-dropped decline leaves a domain re-asked forever; turn-count "done" leaves a domain silently un-captured) — criteria 2,5. CONCERN-1 / PF-S87-01 (rich capture that never feeds the plan) — criterion 3. ADR-0016 raw-egress bound (the control surface must be de-identified) — criteria 1,4.
**Dependencies:** ADR-0015-T1 (reads `router.summarize`; no model call in the strategy itself, but it lives in `chat.py` alongside the client-driven dispatch). Blocks: ADR-0016-T1.

---

### ADR-0015-T3: Wire the Plan-Author Dispatch Through the One Client (H-1, Honest No-Plan on Failure)

**Status:** TODO
**ADR Source:** ADR-0015, Decision (the plan-author dispatch is the SECOND consumer; both route through the one client); ADR-0015, Consequences (amends ADR-0006's dispatch MECHANISM only — `assemble`'s filters / clearance gate / translators / `record_plan` UNCHANGED); ADR-0015, Validation Approach (Confirmation: the wired `author → assemble → record_plan → render` self-test passes with the programmatic author path; Falsification: the `_author_callable` captured-data feed persists; a failed author call yields a fabricated plan); design H-1 (the production seam is `_author_callable`, NOT `router.dispatch`)
**Files to create/modify:**
- `scripts/plan/generate_plan.py` -- replace `_author_callable`'s captured-envelope-verbatim return (`generate_plan.py:65-81` [VERIFIED]) with a call through `scripts/model/client.py`'s `author(domain, summary)`; `assemble` (`generate_plan.py:61`), the clearance gate, the four filters, the translators, and `record_plan` UNCHANGED
- `tests/plan/test_generate_plan.py` -- the programmatic author path; honest no-plan on a failed author call

**Acceptance Criteria:**
1. The plan-author envelope is produced by a call through the ONE model client (`scripts/model/client.py`'s `author`), NOT the captured-envelope-verbatim feed — verified by a test with a mock client at the seam asserting `compute_plan`/`generate_plan` reach the client's `author` (and `rg` finds the captured-data `_author_callable` verbatim-return is gone / re-wired), against the live `_author_callable` baseline (`generate_plan.py:65-81` [VERIFIED]).
2. `assemble`'s four safety filters, the clearance gate, the per-domain translators, and `record_plan` are UNCHANGED — verified by `git diff` showing 0 changed lines in `assemble.py` / `plan_schema.record_plan` and the existing `assemble`/clearance/translator tests passing unchanged.
3. The author call carries the de-identified `router.summarize` summary, NOT raw operator data (this path stays summary-only — it is NOT the `/chat` raw-egress carve-out) — verified by a test asserting the payload to the client's `author` is a `summarize`-built de-identified summary (0 raw operator PII).
4. A FAILED author model call yields the honest no-plan state — `compute_plan`/`generate_plan` record NOTHING on a failed author call (the existing coverage-gap / payload-less no-plan path, `generate_plan.py:338-344` [VERIFIED]), NEVER a fabricated or degraded plan — verified by injecting a client failure and asserting `recorded == False` + the honest reason, with 0 fabricated plan written.
5. The wired-path self-test shape passes with the programmatic author path: the `core-capability-audit.sh --self-test` behavioral check (`generate_plan.py:393-467` [VERIFIED]) passes with the author output produced BY the client (a deterministic mock at the seam, no live agent dispatch) — verified by the self-test green with the mock-client author path.
6. `pytest tests/plan/test_generate_plan.py` passes.

**Risk Mitigations:** ADR-0015 Negative-4 (wiring the dispatch programmatically changes ADR-0006's mechanism — must not change the filter architecture) — criterion 2. ADR-0015 fail-closed (a failed author call must not fabricate a plan) — criterion 4. ADR-0015 Falsification (the captured-data feed persisting = core-capability gap not closed) — criteria 1,5. design H-1 (the correct seam) — criterion 1 targets `_author_callable`, not `dispatch`.
**Dependencies:** ADR-0015-T1 (the client `author` method). Blocks: ADR-0019-T2 (the end-to-end plan run rides this wired author path).

---

### ADR-0016-T1: The `/chat` Egress Seam — One Turn In / One Turn Out, Fail-Closed, Per-Turn Extraction

**Status:** TODO
**ADR Source:** ADR-0016, Decision (the live intake conversation may egress raw to the no-train lane; only the live conversation, nothing else); ADR-0018, amends ADR-0013 (the chat is a NEW sibling route on the loopback server); ADR-0016, Validation Approach (Confirmation: the only raw egress is the live conversation on the no-train lane; Falsification: any raw egress OTHER than the live conversation); ADR-0015 OQ-3 fail-closed (a failed call returns a degraded turn, no fabricated turn/fact, no store write); design §2 (loopback-bound, single-egress-class, fail-closed turn, thread survival); design CONCERN-2 (per-turn extraction, DECIDED)
**Files to create/modify:**
- `scripts/serve/server.py` -- add the POST `/chat` route (route table → {GET `/`, POST `/upload`, POST `/chat`}); the `_LOOPBACK` bind literal byte-unchanged (`server.py:29,222` [VERIFIED]); the `/chat` body shape is implementer discretion (NFR-5)
- `scripts/serve/chat.py` -- the per-turn dispatch: `plan_next_turn` (ADR-0015-T2) → `client.converse` → `extract_facts` (ADR-0017-T1) → `persist_capture` → return the per-turn receipt; the fail-closed degraded turn
- `tests/serve/test_chat.py`, `tests/serve/test_chat_no_egress.py`

**Acceptance Criteria:**
1. `/chat` is a sibling route on the SAME `ThreadingHTTPServer(("127.0.0.1", port), ...)` (`server.py:222`, `_LOOPBACK = "127.0.0.1"` at `server.py:29` [VERIFIED]) — it introduces NO new bind; `_LOOPBACK` is byte-unchanged — verified by a structural assertion the bind literal is untouched (0 binds to `0.0.0.0`/`""`) AND a test that `/chat` is served by the loopback server (the route table is {GET `/`, POST `/upload`, POST `/chat`}).
2. ONE turn in / one turn out: a POST `/chat` carrying a raw operator turn returns the assistant reply text + the per-turn capture receipt (the `persist_capture` `{"store":[...], "scaffold":[...]}` shape, `capture.py:244` [VERIFIED]) + the intake-progress state — verified by a turn round-trip with a mock client asserting all three response parts.
3. The ONE outbound network call `/chat` makes is the model call through `scripts/model/client.py` on the no-train lane, carrying the live conversation (raw) + the §1 de-identified context and NOTHING else — verified by `tests/serve/test_chat_no_egress.py`: over a mock client the dispatch makes 0 outbound calls of its own (`rg` finds 0 outbound HTTP client imported in `scripts/serve/`), AND the model payload carries 0 store content / 0 other operator's transcript (the de-identified-context-only assertion). (ADR-0016 Falsification: any raw egress other than the live conversation = release-blocking.)
4. Per-turn extraction (CONCERN-2): the extractor runs on EACH `/chat` turn so `summarize`'s gap-set is live each turn and the raw transcript residency is one turn — verified by a two-turn test asserting turn-1's landed facts are visible to turn-2's `missing_fields`, and the transcript is not held to session end (no session-spanning raw transcript surface).
5. Fail-closed turn (ADR-0015 OQ-3): a failed / timed-out / rate-limited / empty model call returns a turn that surfaces the failure + degrades toward the demographic form, and MUST NOT (a) fabricate an assistant reply, (b) fabricate an extracted fact, or (c) write anything to the store on that turn — verified by injecting each failure mode and asserting the degraded turn + 0 store write + 0 fabricated fact.
6. Thread survival: a malformed `/chat` body or a model-client exception MUST NOT kill the request thread — it returns a degraded turn (mirroring `/upload`'s catch-and-re-render posture, `server.py:161-173` [VERIFIED]) — verified by posting a malformed body and asserting a degraded response, not a dropped connection.
7. `pytest tests/serve/test_chat.py tests/serve/test_chat_no_egress.py` passes.

**Risk Mitigations:** ADR-0016 Negative (raw conversation egresses — the bound must hold) — criterion 3 (single egress class). ADR-0013 Negative-1 (the listening socket — must stay loopback) — criterion 1. ADR-0015 fail-closed — criteria 5,6. design CONCERN-2 (cadence) — criterion 4 (per-turn, short transcript residency).
**Dependencies:** ADR-0015-T1 (the client `converse`), ADR-0015-T2 (the strategy), ADR-0017-T1 (the extractor + the capture wiring). Blocks: ADR-0017-T2.

---

### ADR-0017-T1: The Conversation→De-Identified-Store Extractor (Model Proposes, Gate Disposes; M-3; H-2 Wiring)

**Status:** TODO
**ADR Source:** ADR-0017, Decision (chat-extracted facts written through the SAME two-surface gate-enforced routing as the form; de-identification enforced at the extraction boundary by the deterministic `capture` value gates BEFORE any `store.append`; model proposes, gate disposes); ADR-0017, Validation Approach (Confirmation: every chat-extracted fact passes the gate before `store.append`; no model-emitted fact reaches a `SUMMARY_FIELD_SET` item without the gate; Falsification: any chat-extracted raw PII in a `SUMMARY_FIELD_SET` item, any gate-bypass route); design §3.1 (the `extract_facts` contract, malformed-input + partial/garbled M-3 cases); design H-2 (`identity_config` threading); design CONCERN-3 (the free-text residual)
**Files to create/modify:**
- `scripts/serve/extract.py` -- `extract_facts(model_extraction_output, turn_text) -> ExtractionResult{candidate_facts: dict, declined_domains: set, dropped: list}`; validates the model proposal, routes `candidate_facts` UNCHANGED to `capture.persist_capture`; adds NO `store.append` of its own
- `scripts/serve/server.py` -- thread the instance `identity_config` into the `/chat` capture `persist_capture` call AND the existing `/upload` `persist_capture` call (`server.py:158-160` calls it WITHOUT `identity_config` today [VERIFIED] — the H-2 fix)
- `tests/serve/test_extract.py`, `tests/serve/test_capture.py` (Modify — the `identity_config` round-trip)

**Acceptance Criteria:**
1. EVERY chat-extracted fact reaches the store ONLY via `persist_capture`'s gate (`_bounded_value_ok` / `_value_has_pii` / by-data-class routing, `capture.py:189-244` [VERIFIED]) — there is NO extraction→`store.append` path bypassing the gate — verified by `rg` finding 0 `store.append` in `scripts/serve/extract.py` AND a test that the extractor's only store path is through `persist_capture` (ADR-0017 Confirmation).
2. A model-emitted value carrying raw PII under a token name routes record-only or is rejected, NEVER silently into a `SUMMARY_FIELD_SET` item — verified by feeding a crafted extraction proposal with a raw value (email/phone/postal) under a wired token name and asserting it lands in the gitignored scaffold (record-only), NOT in the token's store item (ADR-0017 Falsification). NOTE per CONCERN-3: the test asserts the gate catches identity/contact PII (email/phone/postal/identity tokens); it does NOT claim the gate catches a clinical diagnosis typed into a free-text token (the accepted V1 residual, `capture.py:88-95` [VERIFIED]) — a "gate de-identifies all PHI" assertion would be a tautological/false test and is excluded.
3. Malformed-input (M-2): a non-dict `model_extraction_output`, or a proposal `extract_facts` cannot parse, yields `ExtractionResult{candidate_facts={}, dropped=[<unparseable field names>]}`, writes NOTHING, does NOT raise into the request thread, and does NOT fabricate a fact — verified per malformed case.
4. Partial/garbled (M-3): when the model returns SOME well-formed and some malformed facts, the well-formed go in `candidate_facts` (each routed INDEPENDENTLY through the gate — `persist_capture` is per-field) and the rest in `dropped`; the turn receipt reports what ACTUALLY LANDED (the `persist_capture` `{"store":[...], "scaffold":[...]}` receipt) PLUS `dropped`, so the next-turn `missing_fields` is computed against what the STORE holds, not what the model claimed — verified by a mixed proposal asserting the landed facts are captured, the dropped ones are listed, and the receipt drives the gap-set against landed-only.
5. H-2 wiring: the `/chat` capture call AND the existing `/upload` `persist_capture` call BOTH thread the instance `identity_config` (e.g. `<instance_root>/vault/meta/operator-identity.txt`, `pii_scan.DEFAULT_IDENTITY_CONFIG` at `pii_scan.py:149` [VERIFIED]) — verified by `rg` finding `identity_config=` at BOTH call sites (closing the `server.py:158-160` omission [VERIFIED]) AND a `test_capture.py` round-trip: an operator-identity token in a free-text value routes record-only WITH `identity_config` threaded (vs the empty-detection baseline without it).
6. A failed model EXTRACTION call yields ZERO candidate facts and writes nothing (never a fabricated/guessed fact); an empty `candidate_facts` from a SUCCESSFUL call (a turn that captured nothing yet) is a valid distinct outcome, not a failure — verified by distinguishing the two cases in tests.
7. `pytest tests/serve/test_extract.py tests/serve/test_capture.py` passes.

**Risk Mitigations:** ADR-0017 Negative-1 (the extractor is the first model-output-trusting surface; a mis-classified fact could route raw detail toward a token) — criteria 1,2 (gate-at-write + record-only routing). design M-2/M-3 (malformed + partial extraction) — criteria 3,4. design H-2 (empty operator-identity detection at today's call site) — criterion 5. ADR-0015 fail-closed — criterion 6. CONCERN-3 (no tautological PHI claim) — criterion 2's NOTE.
**Dependencies:** ADR-0015-T1 (the client's extraction-proposal output the extractor validates). Blocks: ADR-0016-T1, ADR-0017-T2.

---

### ADR-0017-T2: End-to-End Conversation → Usable Plan (PF-S87-01 Headline) + CONCERN-1 Loop-Termination

**Status:** TODO
**ADR Source:** ADR-0017, Decision (the persisted side stays de-identified, the planner's input contract unchanged); ADR-0019, Validation Approach (Confirmation: every chat-extracted fact reaches the roster); design §8 (the build must satisfy all fixed contracts); PF-S87-01 (rich capture that never feeds the plan is the gap the whole set exists to close); ADR-0015 Confirmation (a plan generated headless through the wired path)
**Files to create/modify:**
- `tests/plan/test_conversation_to_plan_e2e.py` -- the headline end-to-end over a fixture conversation (mock client); the live-API-gated variant noted
- (no production file — this task is the integration proof binding ADR-0015-T3 + ADR-0016-T1 + ADR-0017-T1 + the Wave-B tokens; it gates the wave transition)

**Acceptance Criteria:**
1. HEADLINE (PF-S87-01): a fixture conversation (a mock client returning scripted turns + extraction proposals) driven through `/chat` turns → `persist_capture` → `summarize` → `generate_plan`/`compute_plan` (ADR-0015-T3's wired author path) produces a USABLE rendered plan covering the chat-sourced rich domains (≥1 domain plan recorded + rendered from chat-extracted facts) — verified by the E2E asserting a recorded, rendered plan whose content traces to the fixture conversation's facts, NOT the honest no-plan state.
2. The E2E is testable with NO live API — the model client is a fixture/mock at the ADR-0015 seam; the run is deterministic and CI-runnable — verified by the test passing under `.venv/bin/python -m pytest` with no network.
3. The LIVE end-to-end run (real conversation → real plan via the runtime keychain key) is documented as an operator-run gated check (a docstring-noted variant), NOT a CI gate — verified by the test file carrying the live-gated variant note + the `keychain-setup.md` reference; the CI run uses the mock.
4. CONCERN-1 loop-termination at the integration level: a fixture conversation covering a domain whose token is NOT minted terminates the question loop reporting that domain record-only (captured-for-record, not-planned), NEVER `intake_complete` with a silent gap — verified by an E2E variant with an unminted chat domain asserting the record-only termination state (the PF-S87-01 anti-gap, end to end).
5. The persisted side stays de-identified after the conversation: a post-conversation store scan + `summarize` output finds 0 raw operator PII (ADR-0017 Confirmation, `router.py:352-432` [VERIFIED]) — verified by the E2E running `pii_scan` over the post-conversation store and asserting 0 raw-PII hits.
6. `pytest tests/plan/test_conversation_to_plan_e2e.py` passes.

**Risk Mitigations:** PF-S87-01 (a feature reviewed for plumbing but not for whether the capture produces a usable plan) — criterion 1 is the usable-plan proof, criterion 4 the anti-gap. ADR-0017 Falsification (raw PII in the persisted side) — criterion 5. ADR-0015 fail-closed end-to-end — the wired author path's honest no-plan is exercised in ADR-0015-T3 and ridden here.
**Dependencies:** ADR-0015-T3 (the wired author path), ADR-0016-T1 (the `/chat` dispatch), ADR-0017-T1 (the extractor), ADR-0018-T1 + ADR-0019-T1 (the demographic + rich-domain tokens the plan personalizes from). Blocks: none (the wave-closing integration gate).

---

### ADR-0018-T1: Demographic-Form Activation — The Four Orphan Tokens Get Real Inputs (Form Stays Objective-Only)

**Status:** TODO
**ADR Source:** ADR-0018, Decision (the structured form keeps ONLY demographics + content uploads as working capture; the rich sections move to chat; the Step-1 demographic layer is retained and ACTIVATED); ADR-0018, Validation Approach (Confirmation: the form captures only objective inputs, 0 rich-section fields; the four orphan tokens each derive from a real demographic input, 0 orphans against today's 4; Falsification: a rich-section form field persisting a rich fact, a demographic token still orphaned, a content upload routed through chat); ADR-0018 OQ-1 (the field→token wiring — pinned here)
**Files to create/modify:**
- `vault/design/templates/intake.py` -- activate Step-1: convert the four dead `_field(..., True)` placeholders (`intake.py:258-266` [VERIFIED]) into real POSTing inputs inside `capture_form` (`intake.py:408-413` [VERIFIED]); add the `/chat` panel affordance replacing the rich-section Steps 3-5 fields; build the demographic `<select>`/inputs from the same constants the capture gate validates against
- `scripts/serve/capture.py` -- wire the four demographic fields into the capture routing: birth year → `date-of-birth` (named-excluded raw source → `summarize` derives `training-age-band` via `_age_band`, `router.py:81,192`); sex → `sex-for-dosing` (pass-through wired token); bodyweight → `bodyweight-band` (a de-identified band, never raw kg); equipment → `equipment-access-class` (reconciled with the existing `postal-address`→`equipment-access-class` map, `router.py:81` — see AC 5); extend `WIRED_TOKENS`/`_BOUNDED_ENUMS` as needed (the `WIRED_TOKENS ⊆ SUMMARY_FIELD_SET` tripwire at `capture.py:152` stays green)
- `scripts/plan/router.py` -- add/reconcile the demographic-token derivations (`sex-for-dosing`/`bodyweight-band` and the `equipment-access-class` source reconciliation); keep the disjointness tripwires green (`router.py:307-313`)
- `tests/serve/test_intake_demographics.py`

**Acceptance Criteria:**
1. The four previously-orphan tokens (`sex-for-dosing`/`bodyweight-band`/`equipment-access-class`/`training-age-band`, all `SUMMARY_FIELD_SET` members with no working input today, `router.py:18-22` [VERIFIED]) EACH derive from a real Step-1 demographic input — verified by a POST of the Step-1 form asserting each token resolves through `summarize` from the submitted demographic value (0 orphan tokens, against today's baseline of 4; ADR-0018 Confirmation).
2. Each demographic token is de-identified: `training-age-band` is a born-decade band (`_age_band`, `router.py:192-199` [VERIFIED], raw DOB never in the token); `bodyweight-band` is a coarse weight band (never raw kg); `sex-for-dosing` / `equipment-access-class` carry only their de-identified class — verified by a per-token output scan (a crafted raw value at the source → 0 raw value in the emitted token).
3. The `equipment-access-class` source collision is RECONCILED: `router.py:81` already maps `postal-address` → `equipment-access-class`, but ADR-0018 wires the demographic equipment selection to it — the build pins ONE source for the token (the demographic equipment selection, with the `postal-address` derivation either removed or kept as a distinct documented fallback) and the module-load disjointness tripwires stay green — verified by a test asserting `equipment-access-class` derives from the demographic input + a clean module load (no double-source ambiguity; `router.py:307-313` [VERIFIED]).
4. The form captures ONLY objective inputs: after activation the POSTing `capture_form`'s field names are demographics + content-upload affordances only, with 0 rich-section fields (no goals/training/nutrition/supplement/peptide form field — those are chat-only) — verified by enumerating the form's POSTed field names against the demographic + upload set (0 rich-section fields; ADR-0018 Confirmation + Falsification).
5. A content upload (DNA/HealthKit/labs) still routes through the unchanged `route.route_upload` → `ingest.run`/`dna.land` seam (`route.py:58-93` [VERIFIED]), NOT chat — verified by a file upload landing via `route_upload` (0 file uploads through `/chat`; ADR-0018 Falsification).
6. The demographic markup is built from the same constants the capture gate validates against (no markup↔gate drift, mirroring the existing `RECOVERY_STATUS_BANDS`/`GOAL_DOMAINS` pattern, `capture.py:80-85` [VERIFIED]) — verified by `rg` confirming the `<select>`/input options reference the gate's enum constants.
7. `pytest tests/serve/test_intake_demographics.py tests/serve/test_capture.py` passes.

**Risk Mitigations:** ADR-0018 Negative-3 (the kept demographic layer is dead today; the split is half-delivered if the orphans stay orphaned) — criteria 1,2. ADR-0018 Negative-1 (a misclassified input on the wrong surface) — criteria 4,5 (form objective-only). ADR-0018 Falsification (rich field on the form / orphaned token / upload through chat) — criteria 1,4,5. The `equipment-access-class` double-source defect — criterion 3.
**Dependencies:** ADR-0016-T1 (the `/chat` panel the form links to). Blocks: ADR-0017-T2 (the plan personalizes from these tokens), ADR-0019-T1 (shares the `router.py` token-extension surface).

---

### ADR-0019-T1: Extend `SUMMARY_FIELD_SET` with De-Identified Chat-Sourced Tokens (Per-Token Coarseness Proof; Tripwires Green)

**Status:** TODO
**ADR Source:** ADR-0019, Decision (extend the closed `SUMMARY_FIELD_SET` with de-identified nutrition/supplement/peptide/training-detail tokens, each a band/class derivation under the change-control tripwire discipline; the exact vocabulary fixed at spec stage); ADR-0019, Validation Approach (Confirmation: each new fact appears in `summarize` as a de-identified token AND reaches the roster; every new token is a band/class proven by a per-token output scan — NOT the 8j6 gate, which does not run on the derived path; the change-control tripwires stay green; Falsification: a new token carrying raw PII, a fact never reaching the planner, a red tripwire); design §3.2 (the new tokens are kind-2 raw-backed-derived; the derivation-coarseness proof is REQUIRED per token, not the 8j6 gate)
**Files to create/modify:**
- `scripts/plan/router.py` -- extend `SUMMARY_FIELD_SET` (`router.py:18-36` [VERIFIED]) with the new nutrition/supplement/peptide/training-detail tokens (the exact vocabulary + band/class cuts pinned here); add each new token's `_RAW_TO_FIELD` entry (`router.py:80-85`) + its `_FIELD_DERIVATION` band/class function (`router.py:301-305`); name-exclude each raw source item in `EXCLUDED_RAW_PII` (`router.py:41-66`); keep the module-load disjointness tripwires green (`router.py:312-313,329-349`)
- `scripts/serve/capture.py` -- wire the new tokens' raw-source capture into the routing (each raw input → its named-excluded store item, never the band token directly; mirroring the `train-around` → `raw-symptom-free-text` pattern, `capture.py:230-234` [VERIFIED])
- `tests/plan/test_router.py` -- the per-token coarseness + tripwire tests
- `tests/serve/test_capture_store_adversarial.py` (Modify — the new write paths' store-adversarial battery)

**Acceptance Criteria:**
1. Each new chat-sourced nutrition/supplement/peptide/training-detail fact appears in the `summarize` summary as a de-identified token AND reaches its domain translator — verified by a round-trip test PER new token: the raw input → its named-excluded store item → `summarize` derives the band/class → the token is read by `summarize` and consumed by `_to_nutrition_plan` / `_to_supplements_plan` / `_to_peptides_plan` / the workout meta (`generate_plan.py:130-228` [VERIFIED]); 0 new tokens missing from the summary (ADR-0019 Confirmation).
2. Every new token is de-identified — a band/class, never raw — PROVEN by an INDEPENDENT per-token output scan, NOT the 8j6 gate: a crafted raw value seeded at the token's source store item, asserting the EMITTED token carries 0 of that raw value (non-reversibility) — verified per new token (ADR-0019 Confirmation + Falsification). The test docstring states explicitly that the 8j6 `summarize` gate does NOT run on the raw-backed-derived path (`router.py:406-412` runs no `scan_text` [VERIFIED]), so this output scan — not the gate — is the de-identification proof (design §3.2 / C-1).
3. The change-control tripwires stay GREEN with the extended set: the module-load asserts `set(_RAW_TO_FIELD) ⊆ EXCLUDED_RAW_PII` and `SUMMARY_FIELD_SET.isdisjoint(EXCLUDED_RAW_PII)` (`router.py:312-313` [VERIFIED]) and the `WIRED_TOKENS ⊆ SUMMARY_FIELD_SET` assert (`capture.py:152` [VERIFIED]) pass with every new token placed in the correct structure — verified by a clean module import (0 tripwire reds; ADR-0019 Falsification: a red tripwire is a release blocker).
4. The new tokens are the CHAT-SOURCED training-VOLUME/detail family, DISTINCT from ADR-0018's demographic `training-age-band` (a `date-of-birth` derivation) — the two "training" families do not overlap — verified by a test asserting the new training-detail token(s) and `training-age-band` are distinct `SUMMARY_FIELD_SET` members with distinct sources (ADR-0019 Decision disambiguation).
5. A new token added to NEITHER the field-set NOR a derivation (the leak path that reads through `summarize`'s else-branch under its own raw name) is caught at module load — verified by a mutation test that deliberately mis-places a token and observes the tripwire RED, then reverts.
6. The new tokens' store write paths satisfy the store-adversarial battery (`docs/checklists/store-adversarial-tests.md`): cross-stream collision (a read for new-token X never returns Y's value), same-timepoint dedupe, dedupe-key boundary (`(item,timepoint,source)`, value excluded), and a mutation observed RED — verified by `tests/serve/test_capture_store_adversarial.py` covering all four, category 4 RED.
7. `pytest tests/plan/test_router.py tests/serve/test_capture_store_adversarial.py` passes.

**Risk Mitigations:** ADR-0019 Negative-1 (a mis-derivation could leak more granularity than intended — a too-fine band reconstructs raw detail; the 8j6 gate does NOT cover this path) — criterion 2 (the per-token output scan is the real mitigation). ADR-0019 Negative-2 (each token needs a tripwire kept correct) — criteria 3,5. PF-S87-01 (a fact never reaching the planner) — criterion 1. Store-surface mandate (`pka`) — criterion 6.
**Dependencies:** ADR-0018-T1 (shares the `router.py`/`capture.py` token-extension surface; built after the demographic tokens land to avoid a `router.py` merge collision). Blocks: ADR-0017-T2 (the plan personalizes the rich domains from these tokens).

---

## Dependency Map

```
ADR-0015-T1 --> ADR-0015-T2   (the strategy lives in chat.py alongside the client dispatch)
ADR-0015-T1 --> ADR-0015-T3   (the client's author() method the plan-author seam calls)
ADR-0015-T1 --> ADR-0016-T1   (the client's converse() the /chat turn calls)
ADR-0015-T1 --> ADR-0017-T1   (the client's extraction-proposal output the extractor validates)
ADR-0015-T2 --> ADR-0016-T1   (the gap-set strategy the /chat dispatch drives)
ADR-0017-T1 --> ADR-0016-T1   (the extractor + capture wiring the /chat dispatch calls per turn)
ADR-0016-T1 --> ADR-0017-T2   (the /chat dispatch the end-to-end conversation drives)
ADR-0015-T3 --> ADR-0017-T2   (the wired programmatic author path the plan run rides)
ADR-0017-T1 --> ADR-0017-T2   (the extractor the end-to-end conversation runs through)
ADR-0016-T1 --> ADR-0018-T1   (the /chat panel the activated form links to)
ADR-0018-T1 --> ADR-0019-T1   (shares the router.py/capture.py token-extension surface; serialized to avoid a merge collision)
ADR-0018-T1 --> ADR-0017-T2   (the plan personalizes from the demographic tokens)
ADR-0019-T1 --> ADR-0017-T2   (the plan personalizes the rich domains from the new tokens)
```

Entry point (no dependencies in this spec): ADR-0015-T1

Topological order (Kahn parallel groups):
1. **Group 1 (entry point):** ADR-0015-T1
2. **Group 2:** ADR-0015-T2, ADR-0015-T3, ADR-0017-T1 (all after ADR-0015-T1)
3. **Group 3:** ADR-0016-T1 (after ADR-0015-T1, ADR-0015-T2, ADR-0017-T1)
4. **Group 4:** ADR-0018-T1 (after ADR-0016-T1)
5. **Group 5:** ADR-0019-T1 (after ADR-0018-T1)
6. **Group 6:** ADR-0017-T2 (after ADR-0016-T1, ADR-0015-T3, ADR-0017-T1, ADR-0018-T1, ADR-0019-T1)

Critical path: ADR-0015-T1 → ADR-0017-T1 → ADR-0016-T1 → ADR-0018-T1 → ADR-0019-T1 → ADR-0017-T2

No cycles (6 groups, every edge points from an earlier group to a later group; Kahn drains all 7 nodes).

**Wave grouping for the build plan:** Wave A = {ADR-0015-T1, ADR-0015-T2, ADR-0015-T3, ADR-0016-T1, ADR-0017-T1} (the model boundary + the `/chat` transport + the extractor + the plan-author re-wire — the conversation path). Wave B = {ADR-0018-T1, ADR-0019-T1, ADR-0017-T2} (the demographic activation + the field-set extension + the end-to-end usable-plan proof — the form-side activation and the token vocabulary that lets the chat-extracted rich facts reach the planner; ADR-0017-T2 is the wave-closing integration gate that needs both waves' tokens). The per-wave checkpoint Go/No-Go: Wave A's is the `/chat` no-egress + fail-closed + extractor-gate proofs; Wave B's is the PF-S87-01 end-to-end usable-plan proof (ADR-0017-T2) + the per-token coarseness scans + the green tripwires.

## Test Strategy

### Unit Tests
- **Scope:** `scripts/model/client.py`, `scripts/model/key_source.py`, `scripts/serve/chat.py` (the strategy `plan_next_turn`), `scripts/serve/extract.py`, and the extended derivations in `scripts/plan/router.py` + `scripts/serve/capture.py`.
- **Approach:** `pytest` against a FIXTURE/MOCK model client at the ADR-0015 seam (no live API — the headline capability is exercised against mocks); a temp `vault/store/` + temp `scaffold_root`; an injected `key_source` (a set env var) for the key tests; planted-token fixtures for the PII scans; the `summarize`/`store_read` instance-bound reader for the strategy.
- **Criteria covered:** ADR-0015-T1 1-6; ADR-0015-T2 1-6; ADR-0015-T3 1-6; ADR-0016-T1 (the per-turn dispatch units) 2,4,5,6; ADR-0017-T1 1-7; ADR-0018-T1 1-7; ADR-0019-T1 1-7.

### Integration Tests
- **Scope:** the cross-task paths — (a) the full `/chat` turn dispatch (strategy → mock client.converse → extractor → `persist_capture` → receipt → re-render) on an ephemeral loopback port; (b) the `/chat` no-egress proof (0 outbound calls beyond the one mock client call + the `rg`-proven no-HTTP-client-in-`scripts/serve/`); (c) the plan-author wired path (mock client `author` → `assemble` → `record_plan` → render); (d) the HEADLINE conversation→usable-plan end-to-end (ADR-0017-T2); (e) the H-2 `identity_config` threading at both `/chat` and `/upload`; (f) the post-conversation tracked-file + store PII scans.
- **Approach:** run the server on an ephemeral loopback port in a fixture, POST synthetic `/chat` turns over a scripted mock client, assert store/scaffold state + the re-rendered wizard + the recorded plan; run `pii_scan` over the post-conversation store + tracked tree; assert the de-identified-context-only model payload.
- **Criteria covered:** ADR-0016-T1 1,3,7; ADR-0017-T1 1,2,4,5; ADR-0017-T2 1-6; ADR-0018-T1 1,4,5; ADR-0015-T3 5.

### Risk-Specific Tests
- **ADR-0016 raw-egress bound (the crown-jewel PII boundary, NFR-1):** the single-egress-class assertion — the `/chat` model call carries live conversation + de-identified context and nothing else, no store content / no other operator's transcript (ADR-0016-T1 crit 3); the post-conversation store/tracked-file PII scan = 0 (ADR-0017-T2 crit 5).
- **ADR-0015 fail-closed (NFR-2):** the typed-raise on a failed/empty model call (ADR-0015-T1 crit 4); the degraded `/chat` turn with 0 store write / 0 fabricated fact (ADR-0016-T1 crit 5); the honest no-plan state on a failed author call (ADR-0015-T3 crit 4).
- **ADR-0019 per-token de-identification (the 8j6 gate does NOT cover the derived path):** the INDEPENDENT per-token output scan — a crafted raw value at the source → 0 raw value in the emitted token (ADR-0019-T1 crit 2); the green disjointness tripwires (crit 3) + the mis-placement mutation RED (crit 5).
- **PF-S87-01 (rich capture that never reaches the planner):** the headline conversation→usable-plan end-to-end (ADR-0017-T2 crit 1) + the CONCERN-1 token-not-yet-minted record-only loop-termination (ADR-0017-T2 crit 4, ADR-0015-T2 crit 3).
- **Store-surface mandate (`pka`):** the store-adversarial battery on the new token write paths (ADR-0019-T1 crit 6).
- **Public-repo secret leak (MEMORY):** the runtime key source reads no tracked file + the grep test for 0 key literal in the tracked tree (ADR-0015-T1 crit 5).
- **ADR-0003-T2 0-shared-routine-edit:** `git diff --numstat` = 0 on `scripts/ingest/ingest.py`/`adapter.py`/`scheduler.py` across the whole spec (no task touches them; the content-upload seam is byte-unchanged) — a wave-checkpoint assertion.

## NFRs (cross-cutting, each falsifiable, each tied to an ADR)

- **NFR-1 (crown-jewel PII boundary — ADR-0016/0017).** Exactly three data classes cross exactly the boundaries the Component Overview fixes: live conversation MAY egress raw ONLY on the one `/chat` model call (no-train lane); de-identified context MAY egress de-identified; persisted facts cross to the plan model only as de-identified `SUMMARY_FIELD_SET` band/class through the unchanged `summarize`. Nothing raw is EVER committed (the transcript is transient, residue gitignored-only, the `block-pii-commit`/pre-push backstop guards a committed value). *Falsified if* any outbound call carries a raw persisted fact / raw store read / another operator's transcript, OR a fresh-clone tracked-file scan finds raw conversation or operator PII. (ADR-0016-T1 crit 3, ADR-0017-T2 crit 5.)
- **NFR-2 (fail-closed on model failure — ADR-0015).** A failed / empty / errored / timed-out model call NEVER yields a fabricated or silently-partial plan or extraction — the client raises typed, the `/chat` turn degrades (no store write, no fabricated fact), the plan-author falls to the honest no-plan state. *Falsified if* ≥1 fabricated/partial result reaches the store, the planner, or the operator as if complete. (ADR-0015-T1 crit 4, ADR-0016-T1 crit 5, ADR-0015-T3 crit 4.)
- **NFR-3 (runtime key, never tracked — MEMORY / public repo).** The no-train API key is resolved at RUNTIME from an injectable source (env / keychain command); no tracked file holds it. *Falsified if* a grep finds an API-key literal in the tracked tree or `key_source` reads a tracked file. (ADR-0015-T1 crit 5.)
- **NFR-4 (0-shared-routine-edit + store-adversarial battery — ADR-0003/`pka`).** `scripts/ingest/ingest.py`/`adapter.py`/`scheduler.py` byte-unchanged across the spec; any `scripts/store/` write path satisfies `docs/checklists/store-adversarial-tests.md`. *Falsified if* `git diff --numstat` ≠ 0 on the three shared routines, or a new store write path lacks the four adversarial categories with category 4 RED. (wave checkpoint, ADR-0019-T1 crit 6.)
- **NFR-5 (interface-pinned, internals-discretionary).** The build PINS the model-client public interface (`converse`/`author`), the gate-routing contract (extractor → `persist_capture` → `store.append`), the per-token coarseness-proof requirement, the `/chat` boundary (loopback, one-turn-in/out, single-egress-class), and every acceptance criterion. It does NOT pin the model SDK request/response, the prompt/system-prompt text, the `/chat` HTTP wire format, or the exact retry/backoff curve — implementer discretion per the ADRs (ADR-0015 OQ-2/OQ-3, design §6).

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section (each cites ADR-0015/0016/0017/0018/0019 Decision + Validation Approach + the design-doc concern/flag it carries).
- [x] Every ADR ID in the `adrs` frontmatter has at least one task (ADR-0015: T1-T3; ADR-0016: T1; ADR-0017: T1-T2; ADR-0018: T1; ADR-0019: T1).
- [x] All ADR IDs resolve to actual ADR files on disk (ADR-0015–0019 in `docs/adr/` [VERIFIED]).

### Acceptance Criteria Quality
- [x] Every task has ≥1 acceptance criterion (each has 6-7).
- [x] All criteria are binary — each cites a command, a `pytest` target, an `rg`/grep count, a `git diff --numstat`, a typed-raise, a per-token output scan, or a store/tracked-file PII-scan count.
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient".

### File Manifest Integrity
- [x] Every task has a file manifest; every file in any task block appears in the top-level File Manifest and vice versa.
- [x] No task lists a directory instead of a specific file.
- [x] Every source file has a corresponding test file (`client.py`/`key_source.py`→`test_client.py`/`test_key_source.py`; `chat.py`→`test_chat.py`/`test_chat_no_egress.py`/`test_question_strategy.py`; `extract.py`→`test_extract.py`; the `router.py`/`capture.py` extensions→`test_router.py`/`test_capture.py`/`test_capture_store_adversarial.py`; the `generate_plan.py` re-wire→`test_generate_plan.py`; the `intake.py` activation→`test_intake_demographics.py`; the end-to-end→`test_conversation_to_plan_e2e.py`; `__init__.py`/`keychain-setup.md` are a marker/doc, no test).

### Dependency Map Integrity
- [x] No cycles (Kahn drains all 7 nodes; 6 ordered groups).
- [x] Every task ID in a Dependencies field appears as a node; every edge corresponds to a Dependencies entry; the entry point (ADR-0015-T1) has "None".

### Constraint Propagation
- [x] Single model boundary + fail-closed (ADR-0015 → ADR-0015-T1 crit 1,4); both paths through the one client (ADR-0015 → ADR-0015-T3 crit 1, ADR-0016-T1 crit 3); raw-egress bound to the live conversation (ADR-0016 → ADR-0016-T1 crit 3); de-identified persistence via the gate (ADR-0017 → ADR-0017-T1 crit 1,2); per-token coarseness, not the 8j6 gate (ADR-0019 → ADR-0019-T1 crit 2); the four orphan tokens activated (ADR-0018 → ADR-0018-T1 crit 1); the H-2 `identity_config` wiring (design → ADR-0017-T1 crit 5); CONCERN-1 record-only loop-termination (design → ADR-0015-T2 crit 3, ADR-0017-T2 crit 4); CONCERN-2 per-turn extraction (design → ADR-0016-T1 crit 4); M-3 partial/garbled (design → ADR-0017-T1 crit 4); CONCERN-3 no tautological PHI claim (design → ADR-0017-T1 crit 2 NOTE).
- [x] The crown-jewel PII boundary (NFR-1) is carried as both an NFR and per-task criteria (ADR-0016-T1 crit 3, ADR-0017-T2 crit 5).

### Unresolved Concerns
- [x] Disposition section present (15 rows). ADR-0015 OQ-1/OQ-2/OQ-3, ADR-0016 OQ-1/OQ-2, ADR-0017 OQ-1/OQ-2, ADR-0018 OQ-1/OQ-2, ADR-0019 OQ-2, and the six design flags (CONCERN-1/2/3, H-1, H-2) each dispositioned (Proceed / Defer / In scope).
- [x] Defer dispositions justify why deferral is safe (the no-train retention window is a vendor-policy fact gating no interface).

### Risk Coverage
- [x] Risk Mitigations field on every task; every in-scope ADR negative consequence covered (ADR-0015 N1/N2/N4 + fail-closed; ADR-0016 raw-egress; ADR-0017 N1 + M-2/M-3; ADR-0018 N1/N3; ADR-0019 N1/N2 + the store mandate).

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status).
- [x] No placeholder text ("TBD", "TODO: fill in", "...").
- [x] The headline capability (PF-S87-01: conversation → usable plan) is a named end-to-end task (ADR-0017-T2) testable against mocks, with the live-API run gated on the runtime keychain key.
