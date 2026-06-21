---
source-specs: [docs/spec/adr-0013-adr-0014-spec.md]
adrs: [ADR-0013, ADR-0014, ADR-0012]
created: 2026-06-21
status: approved
total-waves: 2
critical-path-length: 6 tasks
estimated-effort: 8 task-days
---

# Build Plan: Interactive Intake Website — Loopback Upload Server + Web-Form Capture

This plan executes one spec (`docs/spec/adr-0013-adr-0014-spec.md`, tier 6, ADR-0013 + ADR-0014 + the ADR-0012 amendment) as two dependency-ordered waves: **Wave A — the upload server** (the loopback `scripts/serve/` HTTP server, the multipart reader, the Apple-Health-zip→`export.xml` extraction, the upload route into the UNCHANGED ingest seam, and the failing-capable egress proof) and **Wave B — the interactive wizard** (the Step-2..6 forms, the by-data-class capture persistence per ADR-0014, the Step-6 `/generate-plan` handoff, the design-critic pass on Steps 3-5, and the store-adversarial battery). 6 tasks total (5 in Wave A, 1 in Wave B), all software — a new `scripts/serve/` package over the existing `vault/store/` + dropzones + the markdown vault. The substrate is local Python 3.12+ + the stdlib `http.server` / `multipart` / `zipfile` (NO third-party web framework, NO database engine, NO always-on daemon); tooling is `pytest`, `rg`, `git`. The server is GLUE: it reuses `ingest.run` / `dna.land` / `status.resolve` / `intake.render` / `generate.run('intake')` / `store.append` byte-unchanged and is wrapped in the already-audited `egress_guard.run`; every script is built by SE, with QA + Security + Architect review on every wave (the design-reviewer added on Wave B), and `plan-integrity` gating the checkpoints.

## Infrastructure Prerequisites

| Prerequisite | Purpose | Verification Command |
|-------------|---------|---------------------|
| Python 3.12+ interpreter (project venv) | Every task runs `pytest` and project Python under `scripts/serve/` | `python3 --version \| grep -qE '3\.(1[2-9]\|[2-9][0-9])'` |
| `pytest` installed in the active environment | Every wave checkpoint runs `pytest` over the task's test files | `python3 -c "import pytest"` && `pytest --version` |
| `rg` (ripgrep) on PATH | Reuse / no-artifact-route / 0-extraction / 0-model-call scans (ADR-0013-T4, ADR-0013-T5, ADR-0014-T1) | `rg --version` |
| `git` on PATH with the repo initialized | `git diff --numstat` 0-shared-routine-edit proofs (ADR-0013-T3, ADR-0013-T4) | `git -C "$(git rev-parse --show-toplevel)" rev-parse --is-inside-work-tree` |
| The egress guard `scripts/guard/egress_guard.py` present + failing-capable | Wave A's 0-egress proof (ADR-0013-T5) and the loopback-bind boundary CONSUME the already-audited OS-level guard | `python3 -c "from scripts.guard.egress_guard import run; assert run(lambda: open('/dev/null').read())"` |
| The ingest seam present byte-unchanged on entry | The server is a front door over `ingest.run` / `dna.land` / the CLI source-map / `status.resolve` / `intake.render` / `generate.run` / `store.append` — all must exist | `python3 -c "from scripts.ingest import ingest, dna; from scripts.ingest import status; from scripts.generate import generate; from scripts.store import store; from scripts.plan import router"` |

**Wave-gated prerequisite (NOT a Wave-A entry prerequisite).** The ADR-0014 capture path consumes `router.summarize` + `pii_scan.scan` + `vault/scaffold/filled/` — those are prerequisites for **Wave B** (`ADR-0014-T1`), not Wave A. Verification once Wave B opens: `python3 -c "from scripts.plan.router import summarize, SUMMARY_FIELD_SET; from scripts.guard.pii_scan import scan; assert callable(summarize) and callable(scan)"` exits 0, and `.gitignore` carries `vault/scaffold/filled/` (`git check-ignore vault/scaffold/filled/x` exits 0 — VERIFIED present at [.gitignore:5](../../.gitignore#L5)).

## Wave Schedule

Built from the spec's Kahn topological sort (6 nodes, 0 cycles, depth = 6). The single entry point is `ADR-0013-T1` (the server skeleton); the chain runs T1 → T2 → T3 → T4 → T5 → ADR-0014-T1. Wave A bundles the five ADR-0013 transport tasks (they share the `scripts/serve/` package + the request path); Wave B is the single ADR-0014 capture task (it depends on Wave A's POST handler + guard-wrapped path). Risk ordering applied within the topological constraints: the loopback-bind boundary (T1) and the traversal-safe staging (T2) precede the route that dispatches uploads (T4); the egress proof (T5) precedes the capture write (Wave B) so the request path is proven egress-free before any operator PII is captured through it.

### Wave A: Upload Server — Loopback Bind, Multipart Staging, Apple-Zip Extraction, Route, Egress Proof

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0013-T1 | Loopback-Only HTTP Server Skeleton + `python -m scripts.serve` Entry | SE + Security review | 1-1.5 days |
| ADR-0013-T2 | Multipart Reader + Temp Staging (Traversal-Safe, Oversize-Bounded) | SE + Security review | 1-1.5 days |
| ADR-0013-T3 | Apple-Health-Zip → `export.xml` Extraction (Mirrors `dna.land`) | SE | 1 day |
| ADR-0013-T4 | Upload Route → Ingest Dispatch + Intake Re-Render (Intake-Only) | SE + Security review | 1-2 days |
| ADR-0013-T5 | Egress Guard Over the Request-Handler Dispatch (0 Outbound, Loopback-Proven) | SE + Security review | 0.5-1 day |

**Entry Criteria:**
- All Infrastructure Prerequisites pass verification (the egress guard + the ingest seam present byte-unchanged).
- `scripts/serve/` does NOT yet exist (VERIFIED absent on entry — ADR-0013 Context); a Wave-A build creating it does not collide with a prior surface.
- `plan-integrity` has grounded every Wave-A task's inputs against the LIVE tree (`stat`/`grep` `ingest.run`/`dna.land`/`_EXT_SOURCE`/`status.resolve`/`intake.render`/`generate.run`/`egress_guard.run` exist) and confirmed the dependency map is an acyclic DAG with artifact-named edges before the wave builds.

**Exit Criteria / Checkpoint:**
- `pytest tests/serve/test_server.py tests/serve/test_bind.py tests/serve/test_multipart.py tests/serve/test_apple_zip.py tests/serve/test_route.py tests/serve/test_egress.py` passes (ADR-0013-T1 crit 5, T2 crit 5, T3 crit 6, T4 crit 7, T5 crit 4).
- **Loopback-bind boundary (ADR-0013-T1 crit 1):** the structural assertion over the server's bind call finds 0 binds to `0.0.0.0`/`""`/a routable interface; a GET `/` returns 200 + the wizard HTML (crit 2); a port collision exits non-zero fail-loud + binds nothing (crit 3).
- **Traversal + oversize (ADR-0013-T2 crit 2-3):** a `../../x` filename writes ONLY inside the temp dir (`Path(staged).resolve()` within the temp root, 0 escapes); an over-ceiling body is refused with 0 residual oversize temp file; the copy is chunked (crit 4, `rg` finds the chunked loop).
- **Apple-zip extraction (ADR-0013-T3 crit 1-3):** a synthetic Apple-Health zip yields the inner `export.xml`; a pre-extracted xml passes through; a zip with no `export.xml` fails loud; the streamed copy is chunked under the byte ceiling (crit 4).
- **Route + intake-only (ADR-0013-T4 crit 1-5):** a POST of a synthetic `export.xml` lands readings via the unchanged `ingest.run` and re-renders the wizard; a synthetic DNA `.zip` lands via the unchanged `dna.land`; an Apple-Health `.zip` extracts then routes to healthkit; the source-detection REUSES `_EXT_SOURCE`/`_detect_source` (0 second extension-map in `scripts/serve/`); NO dashboard/report artifact route exists (a GET for an artifact path 404s; `rg` finds 0 artifact-serving route).
- **0-shared-routine-edit (ADR-0013-T3 crit 5; ADR-0013-T4 crit 6):** `git diff --numstat <pre-wave> -- scripts/ingest/ingest.py scripts/ingest/adapter.py scripts/ingest/scheduler.py scripts/ingest/dna.py scripts/ingest/adapters/healthkit.py` reports 0 changed lines — the server adds 0 adapter / 0 store-write / 0 extraction-in-ingest logic.
- **Failing-capable egress proof (ADR-0013-T5 crit 1-3) — the load-bearing Wave-A safety gate:** the egress guard over a REAL upload→ingest→re-render dispatch returns truthy (0 outbound calls), AND an INJECTED outbound call into the dispatch drives the guard to FAIL (falsy). A guard that does NOT flip to FAIL on the injected call is a no-go (the guard must intercept the new request code path — subprocess/async included, since the guard is OS-level). The production `server.py` request-handler dispatch is wrapped by `egress_guard.run` (`rg` finds the wrap), not merely tested under it.
- **Verifier:** QA, with Security sign-off on the PII/egress boundary (the loopback bind T1, the traversal-safe staging T2, the intake-only route T4, the failing-capable egress proof T5); Architect verifies the front-door reuse design (0-shared-routine-edit); `plan-integrity` gates the wave transition (the checkpoint Go/No-Go RAN green — executed, not reasoned).

**Wall-clock estimate:** 2 days (`ADR-0013-T4` is the longer task).

---

### Wave B: Interactive Wizard — By-Data-Class Capture, Step-6 Handoff, Design Critic, Store-Adversarial Battery

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0014-T1 | Web-Form Capture — By-Data-Class Persistence (Steps 2-6, Field-Map-Grounded) | SE + Security review | 2-2.5 days |

**Entry Criteria:**
- Wave A checkpoint passed (the POST `/upload` handler + the guard-wrapped request path are green; the egress proof is failing-capable; the shared ingest routines are byte-unchanged).
- The wave-gated Wave-B prerequisite passes: `router.summarize` + `pii_scan.scan` importable, `SUMMARY_FIELD_SET` carries every wired token, `vault/scaffold/filled/` gitignored (the by-data-class routing targets).
- `plan-integrity` has grounded ADR-0014-T1's inputs against the LIVE tree (`SUMMARY_FIELD_SET` tokens at [scripts/plan/router.py:18-36](../../scripts/plan/router.py#L18); `store.append` source-field at [scripts/store/store.py:134](../../scripts/store/store.py#L134); the `.gitignore` scaffold entry) before the wave builds.

**Exit Criteria / Checkpoint:**
- `pytest tests/serve/test_capture.py tests/serve/test_capture_store_adversarial.py` passes (ADR-0014-T1 crit 8).
- **Per-wired-field round-trip (ADR-0014-T1 crit 1):** each wired de-identified field (Step-2 `goal-domains`/`goal-targets`/`goal-priority-order`/`hard-limits`; Step-3 `recovery-status-band`; the curated `rx-interaction-classes`) → `store.read(token)` returns the reading tagged `source:"intake"` → `summarize` returns it under the token; every token asserted ∈ `SUMMARY_FIELD_SET`; 0 wired fields missing from the summary.
- **Two-surface negative-placement (ADR-0014-T1 crit 2) — the project assert-placement mandate:** record-only fields (Step-3 training detail, all Step-4 nutrition, the raw Step-5 stack) land ONLY under `vault/scaffold/filled/` AND `store.read(<any SUMMARY_FIELD_SET token>)` does NOT contain a record-only value (the negative assertion that the data is NOT in the wrong place, not only that it exists somewhere).
- **Fresh-clone PII scan (ADR-0014-T1 crit 3):** `pii_scan.scan` over the tracked tree after a full capture session returns 0 operator tokens (the ADR-0005 NFR-2 guarantee held on the capture surface).
- **`summarize`-gate-raises (ADR-0014-T1 crit 4) — asserted adversarially:** the test plants a raw-PII value into a `SUMMARY_FIELD_SET` item and asserts `summarize` RAISES (failing-capable — the gate must reject it, not merely that a clean field-set value passes).
- **Step-6 handoff (ADR-0014-T1 crit 5):** "Save & open plan generation" routes to `/generate-plan` and performs 0 in-app generation (`rg` finds 0 `assemble`/plan-generation call in `scripts/serve/`).
- **Curated-token-only `rx-interaction-classes` (ADR-0014-T1 crit 6):** the item is written ONLY from supplied de-identified class tokens; `rg` finds 0 raw-name→class lookup in `scripts/serve/` (raw drug names never cross the gate).
- **Store-adversarial battery (ADR-0014-T1 crit 7) — `docs/checklists/store-adversarial-tests.md` MANDATE:** all four categories present on the capture write path (cross-stream namespace collision, same-timepoint dedupe, dedupe-key boundary with `value` excluded, mutation test observed RED); category 4 actually ran RED under a deliberately-broken keying/dedupe, then reverted — a battery that stays green under the mutation is a no-go.
- **Design-critic pass on Steps 3-5:** the design-reviewer reviews the interactive Step-3 training / Step-4 nutrition / Step-5 supplement forms for visual consistency against the locked design (Clinical Light) + the no-sparkline rule + the honest record-only labeling; findings are addressed or beaded before merge.
- **Verifier:** QA, with Security sign-off on the capture PII boundary (crit 2, 3, 4) and the store-adversarial battery (crit 7); the design-reviewer signs off on Steps 3-5; `plan-integrity` gates the wave transition (executed Go/No-Go).

**Wall-clock estimate:** 2.5 days.

## Agent Assignment Matrix

Every build task is a software task built by SE. The five Wave-A tasks each touch the PII/egress/trust boundary (a new listening socket, a multipart write path, an upload route, the egress proof) → SE + Security review. The single Wave-B task is the first automated scaffold-writer on the PII fault line → SE + Security review, plus the design-reviewer on the interactive Steps 3-5. `plan-integrity` is a READ-ONLY verification lens (grounds inputs, gates each checkpoint) dispatched alongside the Tier-2/Tier-3 reviewers — it authors no code and does NOT deploy as an a-plus agent.

| Task ID | Agent | Rationale |
|---------|-------|-----------|
| ADR-0013-T1 | SE + Security review | The new loopback listening socket — the first network surface; Security audits the loopback-only bind + the operator-stop lifecycle. |
| ADR-0013-T2 | SE + Security review | The multipart write path — a path-traversal / oversize surface; Security audits the traversal containment + the byte ceiling. |
| ADR-0013-T3 | SE | The Apple-zip extraction mirrors the already-audited `dna.land` pattern; it adds no new egress/PII control of its own (reuses T2's temp-staging + byte ceiling) — no separate Security review (SEC-02-style de-scoping, recorded below). |
| ADR-0013-T4 | SE + Security review | The upload route + the intake-only boundary — re-crossing the artifact-delivery axis is the ADR-0013 Falsification-3 risk; Security audits the route dispatch + the no-artifact-serving assertion. |
| ADR-0013-T5 | SE + Security review | The egress proof over the request path — the PII no-egress boundary on the new surface; Security audits the failing-capable guard wrap. |
| ADR-0014-T1 | SE + Security review (+ design-reviewer) | The first automated scaffold-writer; Security audits the by-data-class routing + the fresh-clone PII scan + the `summarize`-gate-raises; the design-reviewer reviews Steps 3-5. |

**SEC-02-style Security de-scoping for `ADR-0013-T3` (documented, not silent).** `ADR-0013-T3` (the Apple-zip extraction) carries a 0-egress / byte-ceiling concern, which by the rule above would read as "SE + Security review." It is deliberately NOT assigned a separate Security review: the extraction reuses `ADR-0013-T2`'s already-Security-reviewed temp-staging + byte ceiling and mirrors the already-audited `dna.land` zip-member pattern ([scripts/ingest/dna.py:49,92](../../scripts/ingest/dna.py#L49)) — it implements no new egress/PII control. The residual (the guard's coverage of the extraction code path) is closed by the failing-capable egress proof at the Wave-A checkpoint (`ADR-0013-T5`), which wraps the WHOLE request path including the extraction, not by a per-task sign-off. Recorded here so the absence is explicit.

## Checkpoint Protocol

A checkpoint sits at each wave boundary. Each names the test command(s), the acceptance criteria verified (by task ID + criterion), the artifacts that must exist (by path), a go/no-go rule, and the verifier role. `plan-integrity` gates each transition — a wave advances only when its checkpoint Go/No-Go RAN green (executed, not reasoned).

### Wave A → Wave B Boundary

- **Tests:** `pytest tests/serve/test_server.py tests/serve/test_bind.py tests/serve/test_multipart.py tests/serve/test_apple_zip.py tests/serve/test_route.py tests/serve/test_egress.py`; `git diff --numstat <pre-wave-A> -- scripts/ingest/ingest.py scripts/ingest/adapter.py scripts/ingest/scheduler.py scripts/ingest/dna.py scripts/ingest/adapters/healthkit.py` (expect 0); `rg "dashboard|report" scripts/serve/` (expect 0 artifact-serving route).
- **Acceptance Criteria Verified:** ADR-0013-T1 1-5; ADR-0013-T2 1-5; ADR-0013-T3 1-6; ADR-0013-T4 1-7; ADR-0013-T5 1-4.
- **Artifacts Present:** `scripts/serve/__init__.py`, `scripts/serve/__main__.py`, `scripts/serve/server.py`, `scripts/serve/multipart.py`, `scripts/serve/apple_zip.py`, `scripts/serve/route.py`, and their test files.
- **Cross-task integration check (egress guard green with sockets blocked):** the egress guard over a REAL upload→ingest→re-render dispatch returns truthy (0 outbound), AND an injected outbound call drives it to FAIL — the guard is failing-capable over the new request path before any operator PII is captured through it (Wave B). The upload→ingest→re-render E2E is exercised on a synthetic `export.xml`, a synthetic Apple-Health zip, AND a synthetic DNA zip (all three land via the unchanged seam).
- **Go/No-Go:** All tests pass; the bind is loopback-only; a `../../x` filename cannot escape the temp dir; the Apple-zip extraction yields the inner xml and fails loud on a missing member; the route dispatches into the UNCHANGED `ingest.run`/`dna.land` (0 shared-routine edits); NO artifact-serving route exists; the egress guard is failing-capable over the request path. Any non-loopback bind, any temp escape, any shared-routine edit, any artifact-serving route, or a guard that does not flip to FAIL is a no-go.
- **Verifier:** QA; Security signs off on T1/T2/T4/T5 (the PII/egress boundary); Architect verifies the front-door reuse; `plan-integrity` gates the transition.

### Wave B → Done

- **Tests:** `pytest tests/serve/test_capture.py tests/serve/test_capture_store_adversarial.py`; `pii_scan.scan` over the tracked tree post-capture (expect 0 operator tokens); `rg "assemble" scripts/serve/` (expect 0 in-app generation); `rg <raw-name→class lookup> scripts/serve/` (expect 0); regression: `pytest` over the full suite.
- **Acceptance Criteria Verified:** ADR-0014-T1 1-8.
- **Artifacts Present:** `scripts/serve/capture.py`, `tests/serve/test_capture.py`, `tests/serve/test_capture_store_adversarial.py` (+ the `server.py` POST form-submit wiring).
- **Cross-task integration check (the de-identification gate, end-to-end):** a captured wired field round-trips form → `store.append(token, source:"intake")` → `summarize` returns it under the token — the plan-reasoning-over-capture path runs entirely behind the closed `SUMMARY_FIELD_SET` gate. Record-only fields are asserted NOT in any `SUMMARY_FIELD_SET` item (the negative placement).
- **Store-adversarial battery (`pka` mandate):** all four categories present on the capture write path; category 4 (mutation) observed RED under a deliberately-broken keying/dedupe, then reverted. A battery green under the mutation is a no-go.
- **Go/No-Go:** All tests pass; every wired field round-trips through the gate; record-only fields land ONLY in the gitignored scaffold (0 in any field-set item); the fresh-clone PII scan returns 0; `summarize` RAISES on raw PII in a field-set item (failing-capable); the Step-6 submit is a `/generate-plan` handoff (0 in-app generation); `rx-interaction-classes` is curated-token-only (0 raw-name lookup); the store-adversarial battery is non-tautological; the design-reviewer signed off on Steps 3-5; full-suite regression green. Any operator token in a tracked file, any record-only value in a field-set item, any raw-name→class lookup, or a `summarize` gate that does not raise is a no-go.
- **Verifier:** QA; Security signs off on the capture PII boundary + the store-adversarial battery; the design-reviewer signs off on Steps 3-5; `plan-integrity` gates the transition.

## Critical Path

A single linear chain (the spec has one entry point and one leaf):

```
ADR-0013-T1 → ADR-0013-T2 → ADR-0013-T3 → ADR-0013-T4 → ADR-0013-T5 → ADR-0014-T1
```

- **Length:** 6 tasks (5 in Wave A + 1 in Wave B).
- **Zero-slack tasks:** all 6 — the chain is linear, so every task is on the critical path and carries 0 slack. A delay on any task delays the plan.
- **No parallelism within Wave A:** although Wave A bundles five tasks, they are dependency-ordered (T1→T2→T3→T4→T5), so the wave's wall-clock is the SUM of its tasks on the critical path, not the max — the wave is a single serial spine. The 2-day Wave-A wall-clock estimate is the longest single task (`ADR-0013-T4`) for the checkpoint-barrier accounting; the serial build effort across T1-T5 is 4.5-7 task-days.
- **Total estimated effort:** ~8 task-days (Wave A 4.5-7 + Wave B 2-2.5), critical-path length 6 tasks.

## Risk Schedule

### Risk-mitigating-before-protected ordering

- **The loopback-bind boundary (`ADR-0013-T1`) precedes the upload route (`ADR-0013-T4`)** — the server is proven loopback-only before any upload is dispatched through it.
- **The traversal-safe + oversize-bounded staging (`ADR-0013-T2`) precedes the route + the Apple-zip extraction (`ADR-0013-T3`/`T4`)** — a malicious filename or an oversize body is contained before the staged file reaches the ingest seam.
- **The egress proof (`ADR-0013-T5`) precedes the capture write (`ADR-0014-T1`)** — the request path is proven failing-capable egress-free (an injected outbound call drives the guard to FAIL) BEFORE any operator PII is captured and persisted through it. This is the enforcement-first invariant on the new network surface: no PII-capturing task precedes the egress proof.

### Security-sensitive ordering

The PII/egress boundary is fully in place before any task captures operator PII: `ADR-0013-T1` (loopback bind) → `ADR-0013-T2` (traversal-safe staging) → `ADR-0013-T4` (intake-only route) → `ADR-0013-T5` (failing-capable egress proof) all land in Wave A, with Security review in the same wave; `ADR-0014-T1` (the first automated scaffold-writer) lands in Wave B strictly after the egress proof. Security review is never deferred past the implementing wave.

**SEC-02-style de-scoping — `ADR-0013-T3` carries a byte-ceiling / 0-egress concern but gets NO separate Security review (documented).** It reuses `ADR-0013-T2`'s already-reviewed temp-staging + byte ceiling and mirrors the already-audited `dna.land` zip pattern; the residual (the guard's coverage of the extraction code path) is closed by the failing-capable egress proof at `ADR-0013-T5`, which wraps the whole request path including the extraction. Recorded in the Agent Assignment Matrix preamble and here so the absence is explicit, not an oversight.

### Store-surface mandate (`pka`)

`ADR-0014-T1` writes to `scripts/store/` (the capture-persistence path through `store.append`), so it MUST satisfy `docs/checklists/store-adversarial-tests.md` — checked at the SE Tier-1 self-check AND in the Tier-2 QA dispatch (the dispatch prompt cites the checklist; QA verifies all four categories are present and non-tautological, category 4 ran RED). This is a hard gate at the Wave B → Done checkpoint.

## Three-Tier Review

Per the project's V1 Build Execution: each wave runs Tier-1 (SE self-check against the recipe verification checklist) → Tier-2 (whole-wave-diff review: QA always; Security + Architect always for this build given the PII/egress/trust boundary; the design-reviewer on Wave B for Steps 3-5; `plan-integrity` gates the checkpoint) → Tier-3 (`/review-pr` 6-agent) before merge. No tier is skippable. `plan-integrity` grounds every task's inputs against the LIVE tree before the wave builds and gates each wave transition on the executed checkpoint Go/No-Go.

## Feedback Protocol

| Issue Type | Action | Blocks Plan? |
|-----------|--------|-------------|
| Spec defect (untestable criterion) | Flag for spec revision with the task ID + criterion number; log in `docs/build-plan/.pipeline/deviations.md` | Yes — a checkpoint cannot verify an untestable criterion |
| Missing dependency discovered | Add the edge to the wave schedule, re-run the Kahn sort, re-validate ordering; log for spec revision | No — the plan self-corrects |
| A shared ingest routine WOULD need an edit to route the upload | HALT — the server is glue (ADR-0013 / ADR-0003 0-shared-routine-edit); escalate before editing `ingest.py`/`adapter.py`/`scheduler.py`/`dna.py` | Yes — a shared-routine edit breaks the front-door invariant |
| A captured field has no clear data class | HALT — classify against `SUMMARY_FIELD_SET` / `EXCLUDED_RAW_PII` before persisting (ADR-0014 discipline); escalate an ambiguous field | Yes — an unclassified field could land raw PII on the wrong surface |
| Scope change needed | Halt, write resume state, escalate to the user | Yes — plan scope is fixed at 6 tasks |
| A new network route beyond GET `/` + POST `/upload` + the form submit is proposed | Re-open ADR-0013 against the artifact-delivery boundary (ADR-0004 / NG-4) before adding it | Yes — an artifact-serving route re-crosses the prohibited axis |

## Validation Checklist

### Wave Integrity
- [x] Every task appears in exactly one wave — 6 tasks across 2 waves (5 + 1), 0 duplicates, 0 omissions, verified against the Kahn sort.
- [x] No task is scheduled before its dependency's wave — Wave B's single task depends only on Wave A tasks; within Wave A the serial spine T1→T2→T3→T4→T5 is respected.
- [x] Topological ordering respected — the wave schedule is the Kahn result of the 6-node graph.

### Checkpoint Quality
- [x] Every wave boundary has ≥1 verifiable exit criterion — both boundaries name `pytest`/`git diff --numstat`/`rg`/`pii_scan.scan` commands.
- [x] Every checkpoint names specific test commands (not "run tests").
- [x] Every checkpoint identifies a verifier role — QA + Security + (Wave B) design-reviewer + `plan-integrity`.

### Agent Assignment
- [x] Every spec task appears in the Agent Assignment Matrix — all 6 listed.
- [x] No implementation task assigned to a review-only role — `plan-integrity` is READ-ONLY (grounds + gates, authors no code); every script task is SE-primary.
- [x] Security-sensitive tasks have Security review — T1/T2/T4/T5 + ADR-0014-T1 carry "SE + Security review"; T3's de-scoping is documented.

### Critical Path
- [x] Critical path is the actual longest chain — the linear T1→…→ADR-0014-T1 spine; all 6 tasks zero-slack.

### Risk Ordering
- [x] Risk-mitigating tasks precede the tasks they protect — loopback bind (T1) before the route (T4); traversal-safe staging (T2) before extraction/route (T3/T4); the egress proof (T5) before the capture write (Wave B).
- [x] Security ordering correct — the PII/egress boundary is fully in place before any task captures operator PII (T5 before ADR-0014-T1); Security review in the implementing wave.
- [x] The store-surface mandate (`pka`) gates ADR-0014-T1 at Tier-1 + Tier-2.

### Spec Traceability
- [x] Every spec task appears in the wave schedule — ADR-0013-T1..T5 + ADR-0014-T1 all scheduled.
- [x] No task in the plan is absent from the source spec — all 6 plan task IDs are spec task IDs.
- [x] `source-specs` frontmatter lists the consumed spec (`docs/spec/adr-0013-adr-0014-spec.md`).

### Infrastructure
- [x] Every prerequisite has a verification command — the egress guard + the ingest seam carry an importable-assertion command; the Wave-B-gated `router.summarize`/`pii_scan.scan`/scaffold prerequisite is gated to Wave B entry (not Wave A).
- [x] Wave A tasks do not depend on unlisted prerequisites — Wave A consumes the ingest seam + the egress guard (both listed); the capture-path prerequisites are explicitly Wave-B-gated.

### Feedback Protocol
- [x] Feedback protocol section present; covers spec defect, missing dep, the shared-routine-edit HALT, the unclassified-field HALT, scope change, and the new-route artifact-axis re-open.
