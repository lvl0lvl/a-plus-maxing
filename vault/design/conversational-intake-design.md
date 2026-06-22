---
title: Conversational Intake — interface-contract design (ADR-0015–0019 → S89 build spec)
type: design
status: draft
owner: walter
created: 2026-06-22
last_reviewed: 2026-06-22
review_cadence: phase
permalink: a-plus-maxing/design/conversational-intake-design
---

# Conversational Intake — Interface-Contract Design

**What this is.** The interface-contract layer that bridges the accepted conversational-intake ADR set (ADR-0015–0019) to the S89 implementation spec. It fixes the load-bearing boundaries — the question-strategy surface, the chat transport, the dialogue→de-identified-facts extraction, and the PII data-flow — as testable contracts (signatures, preconditions, postconditions, error cases) WITHOUT pinning their internals. It does NOT specify prompts, the exact new ADR-0019 token vocabulary, the model SDK calls, or retry/backoff mechanics — those are deferred to the spec by the ADRs (ADR-0015 OQ-2/OQ-3, ADR-0019 OQ-1/OQ-2) and are restated in §6 Out of Scope.

**Grounding.** Every contract below is grounded against the live tree on `feature/conversational-intake-foundation` as of 2026-06-22, not against the ADR prose alone: the loopback server `scripts/serve/{server.py,route.py,__main__.py}`, the capture gate `scripts/serve/capture.py`, the router boundary `scripts/plan/router.py`, the plan-author caller `scripts/plan/generate_plan.py`, and the store `scripts/store/store.py`. Baseline confirmed: zero model-client import anywhere in `scripts/` (`rg` for `anthropic`/`openai`/`.messages.create`/`httpx`/`requests` → none); the only `do_POST` is `/upload`. The two model-touching paths ADR-0015 names: the intake conversation (a NEW seam, §2) and the plan-author dispatch, whose production seam is `generate_plan._author_callable`'s captured-envelope feed (`generate_plan.py:65-81`), reached via `compute_plan` → `assemble` (§5). NOTE (design-review H-1): `router.dispatch(summary, sink=None)` is NOT a production seam — it has no production caller (`rg '\bdispatch\b'` over `scripts/` finds only its definition); its `sink` is exercised only by tests, and ADR-0015 does not require wiring it.

**Naming.** New module paths in this doc are illustrative placement (`scripts/serve/`, `scripts/model/`); the spec fixes exact filenames. What is load-bearing here is the SHAPE of each boundary and what crosses it, not the file it lives in.

---

## 0. Boundary map (the four new seams + the two they reuse)

```
            ┌─────────────────────── loopback server (ADR-0013/0018) ──────────────────────┐
            │  GET /            POST /upload (unchanged)        POST /chat  (NEW — §2)        │
            │   form-only          file→ingest seam               turn in → turn out          │
            └──────────────────────────────────┬───────────────────────────────────────────┘
                                                │ one turn
                          ┌─────────────────────▼──────────────────────┐
                          │ question-strategy component (§1)            │  reads: de-id store summary
                          │  reads store summary → decides next ask     │  emits: next-turn intent (de-id)
                          └─────────────────────┬──────────────────────┘
                                                │ context (de-identified) + raw operator turn
                       ┌────────────────────────▼─────────────────────────┐
                       │ model client (§ADR-0015, the ONE model boundary)  │  ← the ONLY raw egress (ADR-0016)
                       │  default no-train Claude; swappable at the seam   │
                       └────────────────────────┬─────────────────────────┘
                                                │ model turn (assistant text + structured extraction proposal)
                       ┌────────────────────────▼─────────────────────────┐
                       │ extraction component (§3)  "model proposes"       │
                       └────────────────────────┬─────────────────────────┘
                                                │ candidate facts {field-name → raw-ish value}
                       ┌────────────────────────▼─────────────────────────┐
                       │ capture.persist_capture (UNCHANGED gate)  "gate disposes"          │
                       │  _bounded_value_ok / _value_has_pii / by-data-class routing        │
                       └──────────┬───────────────────────────────────┬──────────────────────┘
                          de-identified token                  raw / record-only
                          → store.append (SUMMARY_FIELD_SET)    → vault/scaffold/filled/ (gitignored)
                                                                       │
                          router.summarize: per-PATH de-id — pass-through tokens backstopped by the
                          8j6 scan; DERIVED tokens de-id'd by the derivation's coarseness ONLY (no 8j6
                          scan on that path — §3.2 / C-1)
```

Two seams are REUSED byte-unchanged and must not be re-implemented: `capture.persist_capture` (the gate) and `store.append` (the write).

**The plan-author model seam (corrected per design review H-1).** ADR-0015's SECOND consumer is the plan-author dispatch. Its production seam is NOT `router.dispatch` — `dispatch` has NO production caller (`rg '\bdispatch\b'` over `scripts/` finds only its definition at `router.py:435`; `generate_plan.compute_plan` and the cross-domain `orchestrate.py` both call `router.summarize` → `assemble` and never `dispatch`). The actual production seam is `generate_plan._author_callable`, which today returns the captured agent envelope verbatim (`generate_plan.py:65-81`); ADR-0015 makes THAT envelope-production a programmatic call through the one client (§5). `router.dispatch` is currently unwired and ADR-0015 does NOT require wiring it. Everything else in §1–§3 is new.

---

## 1. The question strategy

**Role.** Decide, before each chat turn, what the intake agent should ask next, by reading what the de-identified store already holds and what the field-set still wants — so the dialogue is targeted (it does not re-ask captured ground) yet flexible (it follows the operator's words), and it can declare a domain "done."

### 1.1 What it reads (precondition surface)

The strategy reads operator-capture state ONLY through the existing de-identified read surface — never the raw transcript, never the gitignored scaffold:

- `router.summarize(store_read)` → the name-addressable de-identified summary keyed by `SUMMARY_FIELD_SET` (`scripts/plan/router.py:352`). A field PRESENT with a value = captured; a field ABSENT from the returned dict = not yet captured (`summarize` omits a field whose backing store item has no readings — the `if readings:` guard at `router.py:411` for the derived path and `router.py:416` for the pass-through path).
- `store_read` MUST be the instance-root-bound reader (`functools.partial(store.read, root=instance_root)`), the same caller contract `summarize`/`compute_plan` document (`generate_plan.py:290-292`). **Breaks if** an unbound `store.read` is passed: it silently reads `vault/store/` under the cwd, so the strategy reasons over the wrong instance and re-asks already-captured fields. The spec MUST bind the root at the call site.

### 1.2 Contract

```
plan_next_turn(summary: dict, covered_domains: set[str], declined_domains: set[str]) -> TurnIntent

  TurnIntent (de-identified — NEVER carries a raw operator value):
    {
      "target_domain": str,        # a chat-covered rich domain (goals/training/nutrition/supplements/peptides)
      "missing_fields": list[str], # SUMMARY_FIELD_SET tokens still ABSENT for target_domain
      "domain_done": bool,         # this domain's targeted fields are all captured OR operator declined
      "intake_complete": bool,     # every chat-covered domain is domain_done
    }
```

The third argument is `declined_domains` (a de-identified `set[str]` of chat-covered domain NAMES the operator declined in dialogue), NOT a turn transcript. This is deliberate (design-review M-2): the strategy's input surface is de-identified by construction, so it carries token names, domain names, and booleans — never raw turn text. The decline SIGNAL is extracted from the dialogue by §3's extractor (the model produces it, the extractor surfaces it as a domain name); the strategy receives only the de-identified name. **Breaks if** the spec threads a raw turn transcript into this argument: that re-introduces raw operator text into the control surface §1.1 forbids — the decline must arrive as a domain-name set, not as the words that expressed it.

- **Preconditions:** `summary` is a `summarize`-built dict (de-identified by construction); `covered_domains ⊆` the chat-covered rich domains ADR-0018 assigns to chat; `declined_domains ⊆ covered_domains` and carries domain NAMES only (no raw text — a de-id precondition the caller MUST satisfy).
- **Postconditions:** `target_domain` is `domain_done=False` if any exists, else `intake_complete=True`. `missing_fields ⊆ SUMMARY_FIELD_SET`. The returned `TurnIntent` carries no raw operator string — only token NAMES and booleans. (The model turns the intent into a question; the question text is the model's, §2/§6.)
- **Error cases:**
  - An empty `summary` (`{}`, a fresh operator) is valid input, not an error — every domain reads as not-started, the first turn opens cold.
  - A `target_domain` not in the chat-covered set is a programming error → raise (fail-loud), never silently ask about a form-owned domain.
  - A `covered_domains` or `declined_domains` member outside the chat-covered set, or a `declined_domains ⊄ covered_domains`, is a malformed input → raise (fail-loud); the strategy never silently ignores a malformed control input (it would corrupt loop termination — a silently-dropped decline leaves a domain re-asked forever).
  - A `summary` that is not a dict → raise (fail-loud); the strategy reads ONLY a `summarize`-built mapping, never an arbitrary object.
- **"Done" semantics:** a domain is `domain_done` when (a) every `SUMMARY_FIELD_SET` token mapped to that domain is PRESENT in `summary`, OR (b) the operator declined the domain in dialogue. Branch (b)'s evidence is a model-extracted decline signal; **breaks if** the spec lets "done" rest on turn count or model say-so without checking the store — `domain_done` is a function of the STORE state plus an explicit decline, not of dialogue length. (This keeps the loop from terminating with a domain silently un-captured — the PF-S87-01 failure class.)

### 1.3 Alternatives (genuinely open — pick one with a breaks-if)

| | A. Fully model-driven from a domain checklist | B. Structured question bank | C. **Hybrid: deterministic gap-set, model-phrased ask** |
|---|---|---|---|
| Who picks the next field | the model, given the checklist + transcript | a fixed decision tree in code | code computes `missing_fields` from the store; model phrases & sequences the ask within that set |
| Re-ask risk | high — model must track "already captured" itself | low | low — `missing_fields` is derived from the store each turn |
| Conversational flexibility | high | low (rigid, reproduces the form's lossiness ADR-0018 rejects) | high within the gap set |
| De-id of the control surface | weak — the control logic sees the raw transcript | strong | strong — the gap-set computation reads only the de-id summary |

**Decision: C (hybrid).** Code owns the de-identified gap-set (`missing_fields` from `summarize`) and `domain_done`/`intake_complete`; the model owns phrasing, follow-up depth, and ordering WITHIN the gap set. This keeps the loop-termination and re-ask guarantees deterministic (a store-grounded `domain_done`, §1.2) while keeping ADR-0018's conversational fidelity (the model phrases freely). It rejects A because a model that self-tracks coverage re-creates the very "did this actually get captured" gap (PF-S87-01) the pivot exists to close; it rejects B because a fixed tree is the rigid form ADR-0018 supersedes, in a chat shell (the same defect ADR-0016 Alternative C names).

**Breaks if:** a future chat-covered domain has NO `SUMMARY_FIELD_SET` token (the ADR-0019 vocabulary has not yet minted it). Then `missing_fields` is empty for that domain and the gap-set computation reports `domain_done` vacuously even though nothing was captured to the planner. Mitigation contract: the strategy MUST treat a domain whose tokens are not-yet-minted as **record-only / not-planner-feeding** and surface that state (the ADR-0019 OQ-2 phased-rollout reality), NOT as `domain_done`. Until ADR-0019's tokens land for a domain, the strategy may still converse and the extractor still records to scaffold, but the strategy reports that domain as "captured-for-record, not-planned," never "done." (Assumption: the chat-covered domain set and the minted-token set can diverge during a phased ADR-0019 rollout — they will; this contract is what keeps the divergence honest.)

---

## 2. The chat transport

**Role.** A new sibling route on the existing loopback server (ADR-0013/0018) that carries one intake turn in and one intake turn out. It is the surface that performs the system's first outbound model call (ADR-0016's one authorized egress class).

### 2.1 Contract (the boundary the route promises — NOT its HTTP framing)

```
POST /chat   (sibling to the unchanged GET / and POST /upload; route table becomes {GET /, POST /upload, POST /chat})

  Request boundary (one turn in):
    - the operator's raw turn text (the live conversation — ADR-0016 permits this raw)
    - an opaque session/turn handle (so the server can hold the in-memory transcript for the live session)
  Response boundary (one turn out):
    - the assistant's reply text (the model's next question/acknowledgement)
    - the per-turn capture receipt: which SUMMARY_FIELD_SET tokens this turn landed in the store, which routed record-only
      (the same {"store": [...], "scaffold": [...]} shape persist_capture already returns — capture.py:244)
    - the intake-progress state (TurnIntent's intake_complete / per-domain done — §1)
```

- **Loopback-bound (precondition, structural):** the route is served by the SAME `ThreadingHTTPServer((_LOOPBACK, port), ...)` (`server.py:222`, `_LOOPBACK = "127.0.0.1"`, `server.py:29`). It introduces NO new bind. **Breaks if** the chat handler is moved off this server or the bind literal is touched — ADR-0013's "first network surface, off-machine-unreachable by construction" criterion and the `branch-completeness`/structural assertions rest on the single `_LOOPBACK` site.
- **Egress contract (postcondition, load-bearing — ADR-0016):** the ONE outbound network call `/chat` makes is the model call through the §ADR-0015 client, on the no-train lane, carrying the live conversation (raw) plus the §1 de-identified context. It carries NO store content beyond that de-identified context, and NO content of any OTHER operator's. ADR-0013 was validated as "0 outbound calls carrying store content"; this route owns the single new egress class ADR-0016 authorizes and nothing wider. **Breaks if** `/chat` sends the gitignored scaffold residue, a raw store read, or a prior operator's transcript — that widens the carve-out past ADR-0016's conversation-only bound (a release-blocking falsification, ADR-0016 §Falsification).
- **Failure contract (error case — ADR-0015 OQ-3 fail-closed):** when the model call fails / times out / is rate-limited / returns empty, `/chat` returns a turn that surfaces the failure to the operator and degrades toward the demographic form (ADR-0015 Consequences "degrade-to-form / surfaced error for intake"). It MUST NOT (a) fabricate an assistant reply, (b) fabricate an extracted fact, or (c) write anything to the store on that turn. The exact retry count / backoff / when-to-degrade-vs-surface is ADR-0015 OQ-3, deferred to spec (§6) — but "no fabricated turn, no store write on failure" is fixed here.
- **Request-thread survival (error case, mirrors the live server):** a malformed `/chat` body, or a model-client exception, MUST NOT kill the request thread — the existing `/upload` handler already catches its input-error set and re-renders rather than dropping (`server.py:161-173`); `/chat` adopts the same posture (return a degraded turn, never a stack-trace drop).
- **Concurrency posture (design-review L-2 — the server is `ThreadingHTTPServer`, each request a thread, `server.py:222`):** two `/chat` turns for the SAME session arriving concurrently (a double-submit / a retried turn) must not corrupt capture. The store is safe at the file level — `store.append` is atomic per item and dedupes on `(item, timepoint, source)` (`store.py:160`), so a double-captured fact is idempotent, not a torn file. The residual risk is two turns reading the same pre-write `summary` and both computing the same `missing_fields` (a re-asked or double-asked field), which is benign (the gap-set self-corrects on the next turn once the write lands). The CONTRACT: per-session single-flight is NOT required for correctness; last-writer-wins is acceptable because the gate + store dedupe make double-capture idempotent. The spec MAY add single-flight per session handle for UX, but it is not a safety requirement.

### 2.2 Out of scope here (implementer discretion / spec)

The HTTP framing (JSON body shape, content-type, status codes, streaming vs. whole-response, the session-handle representation, the in-memory transcript structure) is implementation discretion (Core Rule 4). What this section fixes is loopback-binding, the one-turn-in/one-turn-out boundary, the single-egress-class promise, and the fail-closed turn — not the wire format.

---

## 3. The extraction mechanism

**Role.** Turn the dialogue into the de-identified field-set facts the planner reads, with de-identification enforced by the EXISTING deterministic gate, never by the model — "model proposes, gate disposes" (ADR-0017).

### 3.1 Contract

```
extract_facts(model_extraction_output: dict, turn_text: str) -> ExtractionResult

  model_extraction_output: the model's structured extraction proposal for THIS turn
                           (its shape is the model-client's contract, ADR-0015 OQ-2 / §6;
                            extract_facts validates it, never trusts it blindly)
  turn_text:               the operator's raw turn (used only to attribute/validate the
                           proposal; NEVER written to the store)

  ExtractionResult:
    {
      "candidate_facts": dict {form-field-name: value},  # the SHAPE persist_capture consumes
                                                         # (persist_capture(fields, ...), capture.py:189)
      "declined_domains": set[str],   # chat-covered domains the operator declined this turn (→ §1)
      "dropped": list[str],           # field names the model proposed that extract_facts could NOT
                                      # parse into a well-formed candidate (the partial/garbled set)
    }
```

The `candidate_facts` are then handed UNCHANGED to the existing gate:

```
capture.persist_capture(candidate_facts, root=<instance store>, scaffold_root=<gitignored>,
                        identity_config=<instance operator-identity config — see H-2 below>)
   → for each field:
       _bounded_value_ok(name, value) fails  → record-only (scaffold)          (capture.py:216)
       name in _FREE_TEXT_TOKENS and _value_has_pii(value)  → record-only      (capture.py:221)
       name in WIRED_TOKENS  → store.append under the token name, source:"intake"   (capture.py:226-229)
       name == "train-around" → raw-symptom store item (summarize de-identifies → active-issue-class)
       else → record-only (scaffold)                                            (capture.py:235-239)
```

- **Precondition:** `model_extraction_output` is a dict (the model-client's proposal shape, ADR-0015 OQ-2). `extract_facts` VALIDATES it — a non-dict, or a proposal whose fields it cannot parse into a well-formed `{field-name: value}`, is handled by the malformed-input error case below, never assumed well-formed. `candidate_facts` KEYS are capture field names (the wired tokens, `train-around`, or any field — an unknown key routes record-only by the gate's else-branch, which is correct/safe). The extractor is NOT permitted to call `store.append` itself.
- **Postcondition (the load-bearing one — ADR-0017):** EVERY chat-extracted fact reaches the store ONLY via `persist_capture`'s gate. There is no extraction→`store.append` path that bypasses `_bounded_value_ok`/`_value_has_pii`/by-data-class routing. A model-emitted value carrying raw PII under a token name routes record-only or is rejected — never silently into a `SUMMARY_FIELD_SET` item.
  - **The de-identification backstop is PER-PATH, not universal (design-review C-1 — read this exactly).** For a **pass-through** token (a field reading from a store item of its own name) the `router.summarize` 8j6 `scan_text` raise (`router.py:425`, the `else` branch) IS the per-value runtime backstop — a raw value there fail-closes at the boundary. For a **raw-backed DERIVED** token (the `source_items`/`_FIELD_DERIVATION` branch, `router.py:406-412`) there is **NO per-value PII scan at all** — the 8j6 raise does not run on that path; de-identification rests ENTIRELY on the derivation function being coarse (`_age_band`/`_issue_class`/`_region_class` discard the raw value, but cannot raise on embedded raw PII). So the spec MUST NOT rely on the 8j6 gate to catch a leaky derived token; that proof is the derivation's coarseness, verified per token (§3.2).
- **Malformed-input error case (design-review M-2):** a `model_extraction_output` that is not a dict, or a proposal `extract_facts` cannot parse, yields an `ExtractionResult` with `candidate_facts={}`, `dropped=[<the unparseable field names>]`, and writes nothing — it does NOT raise into the request thread (the §2 thread-survival contract) and does NOT fabricate a fact.
- **Partial / garbled extraction (design-review M-3):** when the model returns SOME well-formed facts and some malformed ones, `extract_facts` keeps the well-formed in `candidate_facts` and lists the rest in `dropped`. Each kept fact routes INDEPENDENTLY through the gate (already true — `persist_capture` routes per field). The turn receipt (§2 response) MUST report what actually LANDED (the `persist_capture` `{"store":[...], "scaffold":[...]}` receipt) plus `dropped`, so §1's next-turn `missing_fields` is computed against what the STORE holds, not what the model claimed. A partially-garbled turn is therefore neither silently full-captured nor discarded: it captures what landed and re-asks (via the live gap-set) what did not.
- **Failure contract (error case — ADR-0015 OQ-3 fail-closed):** a failed / errored model extraction CALL yields ZERO candidate facts and writes nothing — never a fabricated or guessed fact. An empty `candidate_facts` from a SUCCESSFUL call (a turn that captured nothing yet) is a valid, common outcome and is distinct from a model-CALL failure (the §2 failure contract owns the operator-facing degrade); neither writes a fabricated fact.

**H-2 — `identity_config` is dropped at today's production call site (design-review High; verified).** The live `/upload` handler calls `capture.persist_capture(fields, root=store_root, scaffold_root=scaffold_root)` — WITHOUT `identity_config` (`server.py:158-160`). With `identity_config=None`, `_value_has_pii` → `pii_scan.scan_text_full(value)` runs only the GENERIC value patterns (email / phone / postal); operator-IDENTITY-token detection (the operator's specific name, etc., unless it matches a generic pattern) is empty (`summarize`'s own docstring documents this silent-empty behavior, `router.py:373-380`). This is a factory-to-component wiring gap of exactly the class the project's integration mandates warn about. **Contract (a wiring acceptance criterion for the S89 build):** the `/chat` capture call MUST thread the instance `identity_config` (e.g. `<instance_root>/vault/meta/operator-identity.txt`) into `persist_capture`, AND the build MUST close the same omission at the existing `/upload` call site (it is the same gate, same instance). Until that wiring lands, operator-SPECIFIC identity detection is ABSENT on the capture path and the gate catches only generic-format PII — invariant 2 (§4) is scoped accordingly. The design does NOT accept `identity_config=None` as the production posture; it requires the wiring.

### 3.2 The de-identification-derivation contract for new ADR-0019 tokens

ADR-0019 mints new de-identified nutrition/supplement/peptide/training-detail tokens. This design fixes HOW they integrate with the gate WITHOUT pinning the vocabulary (ADR-0019 OQ-1, §6):

- A new token is one of three kinds, mirroring the patterns in `router.py` + `capture.py`:
  1. **Pass-through de-identified token** (like `goal-domains`, `recovery-status-band`): the value is already a band/class when it reaches the store; it is wired into `capture.WIRED_TOKENS` and (if bounded) `capture._BOUNDED_ENUMS`. Its PII backstop IS the `summarize` 8j6 `scan_text` raise — this path (a field reading from a store item of its own name) is the `else` branch where the raise runs (`router.py:416-430`).
  2. **Raw-backed derived token** (like `training-age-band` ← `date-of-birth`, `active-issue-class` ← `raw-symptom-free-text`): the RAW input lands in a named-excluded store item, and `summarize` derives the band/class via `_RAW_TO_FIELD` → `_FIELD_DERIVATION` (`router.py:80,301`). The raw never appears in the token. **There is NO 8j6 per-value scan on this path** (design-review C-1): `router.py:406-412` runs the derivation with no `scan_text` call. De-identification here is the derivation's COARSENESS alone — the change-control tripwires only guarantee the raw SOURCE is named-excluded, not that the derived VALUE is PII-free. **Every new ADR-0019 nutrition/supplement/peptide/training-detail token is this kind** (raw-backed-derived), so the 8j6 backstop does NOT cover them.
  3. **Curated, untrusted-input token** (like `rx-interaction-classes`, `capture.py:57-64` Wave-B FIX-A): a field-set member that is pass-through in SHAPE but whose form/extractor input cannot be trusted to be de-identified, so it is DELIBERATELY absent from `WIRED_TOKENS` — the untrusted input routes record-only and the model-bound token is curated at the store layer (a liaison curation surface), never written straight from the extractor. **Breaks if** the spec wires an extractor directly into a curation-only token: a new pass-through-SHAPED token whose extractor input is untrusted MUST follow kind 3 (record-only + store-layer curation), NOT kind 1.
- **Change-control tripwire honoring (precondition, non-negotiable):** every new token MUST satisfy the existing module-load asserts — `set(_RAW_TO_FIELD) ⊆ EXCLUDED_RAW_PII` and `SUMMARY_FIELD_SET ∩ EXCLUDED_RAW_PII == ∅` (`router.py:312-313`), and the `capture.WIRED_TOKENS ⊆ SUMMARY_FIELD_SET` assert (`capture.py:152`). A token added to NEITHER the field-set NOR a derivation reads through `summarize`'s else-branch under its own raw name — exactly the leak the tripwires red on at import. **Breaks if** a token is added to the field-set but its raw source is not named-excluded, or a bounded token skips `_BOUNDED_ENUMS` — the spec MUST place each new token into the correct structure and the build MUST keep the asserts green (ADR-0019 §Falsification: a red tripwire is a release blocker). Note (C-1): these asserts pin the raw SOURCE as named-excluded; they do NOT prove the derived OUTPUT is PII-free — that is the separate per-token coarseness proof below.
- **Derivation coarseness proof (precondition for every new kind-2 token — design-review C-1, REQUIRED, not deferred to a gate):** because no per-value scan runs on the derived path, each new derived token's de-identification MUST be proven by its DERIVATION being coarse. The spec acceptance criterion (per new derived token): an INDEPENDENT per-token output scan in the token's tests — a crafted raw value seeded at the token's source store item, asserting the EMITTED token carries 0 of that raw value (non-reversibility). This is the real mitigation; it does NOT defer to the 8j6 backstop (which never runs here). **Breaks if** a band is cut too fine (e.g. a dietary band that reconstructs a specific raw dietary fact) — ADR-0019 OQ-1 flags band granularity as itself a PII-boundary review item; the spec sets the cuts, but the per-token output scan is what catches a too-fine cut.

### 3.3 Alternatives (settled by ADR-0017 — recorded, not re-opened)

ADR-0017 already adjudicated: (A) let the model write the store directly — rejected (trusts the model to self-de-identify, moves the boundary off the deterministic gate); (B) extract-to-raw-intermediate then de-identify — rejected (a new PII-at-rest surface); (C) reuse `persist_capture` unchanged — adopted AS the substrate, plus the new dialogue→facts producer in front. This design implements C: the extractor is the new producer; `persist_capture` and `store.append` are unchanged. No alternative is re-opened here.

---

## 4. The PII handling flow (the crown-jewel boundary — load-bearing)

State it explicitly. There are exactly three data classes and they cross exactly these boundaries:

| Data class | May it egress to the model? | Where may it persist? | Committed to git, ever? |
|---|---|---|---|
| **Live conversation (raw operator turn)** | YES — raw, no-train lane, the live `/chat` model call ONLY (ADR-0016) | transient for the live session (in-memory); any residue ONLY on gitignored surfaces (ADR-0005/0016) | NEVER |
| **De-identified context for the next ask (§1 TurnIntent + de-id summary)** | YES — de-identified (token names, bands/classes) | derived on the fly from the store; not separately persisted | n/a (de-identified) |
| **Persisted fact (chat-extracted)** | only as a de-identified `SUMMARY_FIELD_SET` band/class through the EXISTING plan-reasoning egress (`router.summarize` → the plan-author model call, §5; unchanged) | `store.append` (de-identified token) OR `vault/scaffold/filled/` (raw/record-only, gitignored) | the store + scaffold are gitignored; NEVER a tracked page |

**The four invariants this flow holds (each falsifiable, each tied to an ADR):**

1. **Only the live conversation crosses raw.** The single raw-egress call is `/chat`'s model call (§2). Every OTHER model-bound path — the plan-author dispatch (§5), the plan-reasoning summary — carries de-identified summaries only, unchanged (ADR-0016 Decision; `router.summarize` untouched, `router.py:352`). *Falsified if* any outbound call carries a raw persisted fact, a raw store read, or another operator's transcript.

2. **Every persisted fact is de-identified — by a PER-PATH mechanism (design-review C-1).** The extractor writes only through the gate (§3); a de-identified band/class reaches the store, raw routes record-only to the gitignored scaffold. The de-identification backstop differs by token kind: a **pass-through** token is backstopped by the `summarize` 8j6 `scan_text` raise (`router.py:425`, the `else` branch); a **raw-backed DERIVED** token (every new ADR-0019 token) has NO 8j6 scan on its path (`router.py:406-412`) — its de-identification is the derivation's coarseness, proven by a per-token output scan (§3.2). The 8j6 gate is NOT a universal "raises if a raw value ever reaches a token" guarantee. The capture-path `_value_has_pii` catches GENERIC-format PII (email/phone/postal); operator-SPECIFIC identity detection runs only when `identity_config` is threaded (H-2 — required by the §3.1 wiring criterion, absent at today's call site). *Falsified if* a post-conversation store scan finds raw operator PII in a `SUMMARY_FIELD_SET` item (ADR-0017 §Falsification) — caught for pass-through tokens at the 8j6 boundary, for derived tokens by the per-token coarseness test.

3. **The raw transcript is transient + never committed.** The transcript lives in memory for the live session; any residue lands only on gitignored surfaces (`vault/scaffold/filled/`, `vault/store/`). The registered `block-pii-commit.sh` PreToolUse hook + the `pre-push-pii-scan.sh` backstop deny a committed filled-value path. *Falsified if* a fresh-clone scan of tracked files finds raw conversation or operator-PII tokens (ADR-0005/0016 §Falsification — release-blocking, history cannot be cleanly scrubbed). **Note:** the EXACT local-residue handling (in-memory only vs. gitignored-scaffold-for-replay vs. discard-after-extraction) is ADR-0016 OQ-2 / ADR-0017 OQ-2, deferred to spec (§6). What is fixed here: whatever the residue mechanism, it lands ONLY on a gitignored surface and the commit/push hooks are the backstop.

4. **Fail-closed on model-call failure.** A failed model call writes nothing and fabricates nothing (§2 + §3 failure contracts; ADR-0015 OQ-3). *Falsified if* a failed/empty/timed-out call yields a fabricated assistant turn, a fabricated extracted fact, or a store write (ADR-0015 §Falsification).

**Assumption (breaks-if):** the no-train provider's no-train + retention terms hold (the ~30-day no-train profile ADR-0001/0016 record, window UNVERIFIED — ADR-0016 OQ-1). **Breaks if** raw conversation becomes training-eligible or its retention window grows — then ADR-0016's relaxation is re-opened and the raw-egress carve-out closes (ADR-0016 §Review-triggers / Dissent).

---

## 5. The plan-author dispatch becomes programmatic (ADR-0015's second consumer)

This is the OTHER model-touching path ADR-0015 names; the design fixes its boundary so the build does not scatter a second model call.

- **Today:** `generate_plan._author_callable(author_output)` returns a captured agent envelope verbatim; its `specialist(domain, summary)` ignores `(domain, summary)` (`generate_plan.py:65-81`). The model is reached only by an out-of-process interactive agent dispatch — the core-capability gap (PF-S63-02 / `71s4`).
- **Contract after wiring:** the captured-envelope feed is replaced by a call through the ONE §ADR-0015 model client — the client produces the author envelope `{"specialist": slug, "recommendations": [...]}` (or the thin-library sentinel) that `assemble` then filters. `assemble`'s four safety filters, the clearance gate, the per-domain translators, and `record_plan` are UNCHANGED (ADR-0015 amends ADR-0006's dispatch MECHANISM only). The author call carries the de-identified `router.summarize` summary, NOT raw operator data — this path stays summary-only (it is NOT the §2 raw-egress carve-out).
- **Failure contract (ADR-0015 OQ-3 fail-closed):** a failed author model call yields the honest no-plan state (`compute_plan`/`generate_plan` already record nothing on a coverage-gap / payload-less section — `generate_plan.py:338-344`), NEVER a fabricated or degraded plan. The mechanical proof stays `core-capability-audit.sh --self-test` (`generate_plan.py:393`), which must pass with the author output produced BY the client rather than fed as captured data (ADR-0015 §Confirmation).
- **Single-boundary contract:** both §2 (intake conversation) and §5 (plan-author) reach the model ONLY through the one client. **Breaks if** the build inlines an SDK call at either site — ADR-0015 §Falsification: ≥1 model-client import outside the client module fails the single-boundary decision; >1 caller-side edit to swap the provider means the seam ossified.

---

## 6. Out of scope (deferred to the S89 spec — do NOT pin here)

These are deliberately deferred by the ADRs; this design does not specify them:

- **Prompts / system prompts / question phrasing** — the model owns phrasing within §1's gap set (Core Rule 4/6).
- **The exact ADR-0019 token vocabulary + band/class cuts** (ADR-0019 OQ-1) — §3.2 fixes the INTEGRATION contract (which structure each token joins, the tripwire asserts, "coarse enough not to reconstruct"); the spec mints the actual tokens and cuts.
- **Phased vs. all-at-once ADR-0019 rollout** (ADR-0019 OQ-2) — a build-sequencing choice; §1.3's breaks-if makes the divergence safe either way.
- **Model SDK calls / provider auth / the client's request-response shape** (ADR-0015 OQ-2) — the client's internal contract; this design fixes only that ONE client exists and both paths route through it (§5).
- **Retry policy / backoff / exact degrade-vs-surface thresholds** (ADR-0015 OQ-3) — §2/§3/§5 fix the fail-closed PRINCIPLE (no fabricated turn/fact/write on failure); the mechanics are the spec's.
- **Local-residue handling for the raw transcript** (ADR-0016 OQ-2 / ADR-0017 OQ-2) — §4 invariant 3 fixes "gitignored-only + hook backstop"; the in-memory-vs-scaffold-vs-discard choice is the spec's.
- **`/chat` HTTP wire format** (§2.2) — JSON body, status codes, streaming, session-handle representation: implementer discretion.
- **The form-vs-chat classification rule for a borderline input** (ADR-0018 OQ-2) and **the exact demographic-field→orphan-token wiring** (ADR-0018 OQ-1) — spec-stage.

---

## 7. Contract concerns / ADR-gap flags (raised, not papered over)

Three flags for the orchestrator. None blocks the design; each is a coherence gap the spec must close.

**CONCERN-1 (gap, §1.3 ↔ §3.2 — the divergence window is real and un-owned by a single ADR).** ADR-0018 puts a domain in chat; ADR-0019 mints that domain's tokens — and ADR-0019 OQ-2 explicitly allows a PHASED rollout where they land at different times. During that window a chat-covered domain has NO planner-feeding token. Neither ADR-0018 nor ADR-0019 names WHO reports that a domain is "captured-for-record, not-planned" so the §1 loop does not terminate with a silent gap (the PF-S87-01 failure class the whole set exists to close). §1.3's breaks-if assigns that to the question-strategy component. The spec should make this explicit in an acceptance criterion: a chat-covered, token-not-yet-minted domain reports record-only, never `domain_done`.

**CONCERN-2 (gap, §2 ↔ §3 — no ADR fixes the per-turn vs. end-of-session extraction cadence).** The ADRs fix THAT extraction goes through the gate (ADR-0017) but not WHEN — does the extractor run on every `/chat` turn, or once at session end? This is load-bearing for two contracts: §1's `missing_fields` is only accurate if the store is updated as the conversation progresses (per-turn extraction), and §4 invariant 3's "transient transcript" is cheaper if facts are gate-persisted per turn rather than holding the whole raw transcript to the end. This design ASSUMES per-turn extraction (it makes the gap-set live and shortens raw-transcript residency) and §2's response contract returns a per-turn capture receipt consistent with that. The spec should confirm per-turn extraction or justify end-of-session and re-derive §1's freshness contract. Flagging rather than silently picking — it changes the §1/§4 contracts. **Within the per-turn assumption, the partial/garbled extraction case (design-review M-3) is the sharp edge:** a turn that yields some well-formed and some unparseable facts must compute §1's next-turn `missing_fields` against what ACTUALLY landed in the store (the `persist_capture` receipt), not what the model proposed — §3.1's `ExtractionResult.dropped` + the turn receipt fix this, so a half-captured turn re-asks (via the live gap-set) exactly the fields that did not land, never silently counting a dropped fact as captured.

**CONCERN-3 (coherence, §3.1 — the documented free-text residual now applies to model output).** `capture._value_has_pii` does NOT catch a clinical diagnosis deliberately typed into a free-text goals field (the accepted V1 residual, `capture.py:88-95`; the model path is no-train, a clinical-PHI detector is out of scope). ADR-0017 §Consequences-Negative correctly notes this residual "now applies to model-emitted free-text too." This is not a NEW gap — it is the SAME residual, correctly inherited — but the spec's extraction acceptance criteria must not claim the gate catches clinical PHI in a free-text token; it catches identity/contact PII (email/phone/postal/identity tokens), and the residual stands for both the form and the extractor. A test asserting "the gate de-identifies all PHI in free text" would be a tautological/false test (it would encode behavior the gate does not have).

---

## 8. Summary of fixed contracts (the build must satisfy all)

1. Question strategy reads ONLY the de-identified `summarize` summary (instance-bound `store_read`); emits a de-identified `TurnIntent`; `domain_done` is store-grounded + explicit-decline, never turn-count or model say-so; a token-not-yet-minted domain reports record-only, never done.
2. `/chat` is a sibling route on the unchanged `127.0.0.1` server; one turn in / one turn out; its ONE outbound call is the no-train model call carrying live conversation (raw) + de-identified context and nothing else; a failed call returns a degraded turn (no fabricated turn/fact, no store write) and never kills the thread.
3. The extractor emits `candidate_facts` in `persist_capture`'s field shape and reaches the store ONLY through the unchanged gate (`_bounded_value_ok`/`_value_has_pii`/by-data-class → `store.append`); new ADR-0019 tokens join the correct router structure (pass-through / raw-backed-derived / curated-untrusted) and keep every module-load tripwire green; each new DERIVED token carries a per-token output-scan coarseness proof (the 8j6 gate does NOT cover the derived path — C-1); the `/chat` capture call threads the instance `identity_config` (H-2); a failed extraction writes nothing, a partial extraction re-asks what did not land (M-3).
4. Three data classes cross exactly as §4's table fixes: live conversation raw (one call only), de-identified context, de-identified persisted facts (de-id PER-PATH — 8j6 backstop for pass-through, derivation coarseness for derived); nothing raw is committed; fail-closed holds on model failure.
5. Both model paths route through the ONE ADR-0015 client: the intake conversation (the NEW `/chat` seam) and the plan-author dispatch (whose production seam is `_author_callable`'s captured-envelope feed, NOT `router.dispatch` — H-1). The plan-author path stays summary-only and fails closed to the honest no-plan state.
