# Judge — Live-Wiring Spec — Iteration 1

**Spec:** `docs/spec/.pipeline/live-wiring/draft-spec.md`
**Judge:** fresh context; no prior scores, no author brief seen.
**Re-measure base:** `main @ e3d5789`, branch `feature/engine-live-wiring-build` (matches the spec's declared base).
**AUTO-FAIL scan result:** NONE fired. (Details under each dimension; the dimension-11 four-probe re-measurement found no Create-on-existing, no Modify-on-absent, no stale premise, no phantom input, no duplicate enforcer.)

**VERDICT: ACCEPT (every dimension ≥ 9/10).**

---

## Independent dimension-11 re-measurement (run FIRST, not taken from the author's Ledger)

All probes run with Read/Grep/Glob/read-only Bash, no network.

### Manifest action-truth (`stat` every row)
- **7 Create rows — all ABSENT on disk (correct):** `scripts/plan/plan_driver.py`, `scripts/plan/gate_dispatch.py`, `scripts/plan/_a_prime_self_test.py`, `tests/plan/test_plan_driver.py`, `tests/plan/test_gate_dispatch.py`, `tests/plan/test_generate_plan_skill_glue.py`, `tests/plan/test_a_prime_self_test.py`.
- **5 Modify rows — all PRESENT on disk (correct):** `scripts/model/client.py`, `tests/model/test_client.py`, `scripts/plan/plan_orchestrator.py`, `.claude/skills/generate-plan/SKILL.md`, `scripts/core-capability-audit.sh`.
- **No Create-on-existing / Modify-on-absent mismatch.**

### Load-bearing premise freshness (re-confirmed against the live files, not the ADR prose)
- `_ClaudeNoTrainBackend.deidentify` IS a `NotImplementedError` stub — `client.py:156-160` CONFIRMED ("live deidentify is wired at the Wave-B operator checkpoint; tests inject a backend").
- `MODEL = "claude-opus-4-8"` — `client.py:135` CONFIRMED.
- Lazy `from anthropic import Anthropic` + `key_source.resolve()` in `_client()` — `client.py:137-142` CONFIRMED. `key_source.resolve` def at `key_source.py:64` CONFIRMED.
- `ModelClient.deidentify` wrapper with `isinstance(result, dict)` → `ModelCallError` — `client.py:92-95` CONFIRMED; `_call` fail-closed wrapper `client.py:105-123` CONFIRMED (constant message, no `{exc!r}` interpolation — SEC-01).
- Inline revise loop IN `run_orchestrated`'s `while True:` — `plan_orchestrator.py:260-300` CONFIRMED, with every cited sub-line exact: `safety_passed is True` gate at `:265`; accept → `_promote_plans` at `:271-276`; `revise_cap` halt at `:279-280`; `revise_domains` re-dispatch + out-of-run-set guard at `:286-294`; de-id sentinel halt at `:229-231`; `dispatch_cap` halt at `:301-305`. The 3 disposition keys (`accept`/`safety_passed`/`revise_domains`) ARE consumed inline at `:265`/`:271`/`:286`. CONFIRMED.
- `quality_judge(assembled_plan, judge_client)` returns `{"verdict": ACCEPT|REVISE, "dimensions": {...}, "deductions": [...]}` — `quality_judge.py:206-253` CONFIRMED (the spec's `-> {verdict}` is the load-bearing key; dimensions/deductions are also present).
- `review_plan(assembled_plan, dispatch, *, lenses=DEFAULT_LENSES)` returns `{"findings": ..., "passed": bool, "lenses": ...}` — `safety_review.py:110-169` CONFIRMED; `DEFAULT_LENSES` ≥2 enforced (`len(lenses) < 2` raises ValueError at `:147-151`).
- `router.SUMMARY_FIELD_SET` exists — `router.py:20` CONFIRMED; `deid_in` imports it and enforces the ⊆ whitelist + `DEID_CALL_FAILED` sentinel — `deid_in.py:18,27,42-65` CONFIRMED.
- `core-capability-audit.sh` CALLER pin IS `$REPO_ROOT/scripts/plan/generate_plan.py` — `core-capability-audit.sh:47` CONFIRMED; the behavioral check invokes `scripts.plan.generate_plan --self-test` at `:68` CONFIRMED. `generate_plan._self_test` at `generate_plan.py:454` CONFIRMED (the analogue the A′ self-test is modeled on).
- Inner-engine 8 modules all present (`orchestrate`/`pipeline`/`assemble`/`generate_plan`/`adjudicate`/`adjust`/`track`/`router`) — CONFIRMED.
- The 7 specialist + lens agents (`personal-trainer`/`nutritionist`/`supplement-specialist`/`peptide-specialist` + `medical-safety-reviewer`/`health-edge-case-reviewer`/`medical-liaison`) all present under `.claude/agents/` — CONFIRMED.
- `reinsert_out(html, target_path, ...)` at `reinsert_out.py:88` — CONFIRMED.
- **Test baseline `1611 passed, 2 skipped`** — RE-RAN `.venv/bin/python -m pytest -q` → `1611 passed, 2 skipped in 23.82s`. CONFIRMED exactly.

### Non-duplication probes (the auto-fail surface)
- **NO existing shared driver:** `rg 'class PlanDriver|def drive|shared_driver|plan_driver' scripts/plan/` → NONE FOUND. `rg 'yield .*dispatch|\.send\(' scripts/plan/` → NONE FOUND. The inline loop is the one being extracted, not forked. CONFIRMED — not a duplicate enforcer.
- **NO existing `gate_dispatch` COMPOSER:** `rg 'gate_dispatch' scripts/` shows the token ONLY as (a) the `run_orchestrated` seam PARAMETER (`plan_orchestrator.py:137,168-221,261`), (b) the inert `_noop_gate_dispatch` default at `:308`, (c) the `_safe_gate` wrapper at `:373-391`, and (d) docstring references in `quality_judge.py`/`safety_review.py`/`dispatch_budget.py`. There is NO built composer module/function. CONFIRMED — not a duplicate enforcer.
- **`run_orchestrated` has no production caller:** `rg run_orchestrated scripts/` → only its own def + docstring mentions in `quality_judge.py`/`dispatch_budget.py`/`plan_orchestrator.py`; no front door composes it over live clients. CONFIRMED (matches ADR-0026 Context).

### One thing the author's Ledger got imprecise (NOT an auto-fail)
The ledger (ADR-0026-T3 RGC-3 row, and the Validation Checklist's "no phantom inputs" line) cites the maintained-render input as **`reemit_maintained` ([maintained.py:245])**. Re-measurement: the symbol `reemit_maintained` DOES exist and IS at **line 245** — but in **`scripts/generate/maintained.py`**, not `scripts/plan/maintained.py` (there is no `scripts/plan/maintained.py`). The cited symbol + line are correct; only the *directory* is elided in the bare-filename citation. Because `reemit_maintained` is a *declared input the skill calls* (not a Manifest action path) and the symbol resolves at the cited line, this is a citation-precision nit, not a phantom input and not an action mismatch. It is noted under Dimension 1/11 as the single sub-10 deduction; it does not gate ACCEPT.
*(Caveat for the next reader: the basic-memory daemon rewrites `vault/**` frontmatter on sync and during this session it momentarily perturbed `scripts/generate/maintained.py` grep output mid-read — the symbol is definitively present per the stable `grep -n '^def '` enumeration: `reemit_maintained` at `:245`.)*

---

## Per-dimension scores

### 1. Traceability — 9/10
Every task carries a non-empty **ADR Source** citing a specific ADR section: ADR-0027-T1 → ADR-0027 Decision+Rationale+Validation + dispositions #5/#7/#8; ADR-0026-T1 → ADR-0026 Decision+Rationale+Consequences + OQ-1 + Validation probes; T2 → ADR-0026 Decision + Validation criterion #2 + OQ-2; T3 → ADR-0026 Decision + Consequences-Neutral; T4 → ADR-0026 Validation criterion #4 + OQ-4 + dispositions #4 + INV-CORE-CAPABILITY/PF-S63-02. Both ADR IDs in frontmatter have ≥1 task (ADR-0026 → T1/T2/T3/T4; ADR-0027 → T1). Both ADR files resolve on disk. Every AC traces to an ADR Validation approach / consequence (e.g. ADR-0026-T1 AC-2/3/4 ↔ ADR-0026 forked-loop / behavior-preservation / injected-safety-not-True falsification criteria; ADR-0027-T1 AC-4/8 ↔ ADR-0027 fail-closed-on-error / raw-PII-leak probes). No task has an empty ADR Source → no auto-fail.
**Deduction (−1):** the ADR-0026-T3 ADR-Source-traced input `reemit_maintained` is cited with a bare-filename path that resolves to the wrong directory (`scripts/generate/maintained.py`, not `scripts/plan/`). **Fix:** in the File Manifest row + the ADR-0026-T3 file-list bullet + the ledger RGC-3 cell, write `scripts/generate/maintained.py:245` (full path). **Projected after fix: 10/10.**

### 2. Task Granularity — 10/10
Five tasks, each a coherent 1–3-day unit. ADR-0027-T1 (one backend method + its test battery) ≈ 1–2 d. ADR-0026-T1 (the keystone extract + re-point + driver unit tests) is the largest but is a single bounded refactor under the 1611-test oracle — ≤3 d, not a mini-project (it is one cohesive control-inversion, not multiple features). T2 (one composer + tests), T3 (one skill reconcile + glue test), T4 (one audit repoint + self-test + test) each ≈ 1–2 d. No task is <4 h (each carries ≥6 ACs across a source file + a test file) and none exceeds the 5-day ceiling. No single-function-trivial task; no mini-project. No auto-fail. **Verification statement:** I read each task's file-list + AC set and confirmed each is one source artifact + its test, sized 1–3 days, none sub-4-hour or over-5-day.

### 3. Acceptance Criteria Quality — 10/10
Every AC is binary and testable against a named function/command/count/threshold. Samples: ADR-0027-T1 AC-3 "count of out-of-set keys = 0"; AC-6 "raises `ModelCallError` after exactly the bounded number of attempts (asserted by counting the fake's invocations)"; AC-8 "count of raw-PII tokens past the boundary = 0". ADR-0026-T1 AC-1 "`git diff --numstat` shows 0 changed lines on every inner-engine module"; AC-3 "`pytest -q` reports `1611 passed, 2 skipped`"; AC-2 grep "finds EXACTLY 1 definition … and 0 duplicated copies". ADR-0026-T2 AC-1 "`set(disposition.keys()) == {"accept","safety_passed","revise_domains"}`". ADR-0026-T4 AC-1 "grep … finding 0 references to `generate_plan.py` as the CALLER and ≥1 to the A′ spine module". No subjective term ("performs well", "clean", "robust", "appropriate") appears in any AC. No auto-fail. **Verification statement:** I read all 39 ACs across the 5 tasks; each names a command/function/count/present-absent check with a 0-threshold or the pinned 1611 baseline; 0 subjective predicates.

### 4. File Manifest Completeness — 10/10
The top-level Manifest lists all 12 files (5 Modify + 7 Create) each with a purpose. Cross-check: every file named in a task's file-list appears in the top-level Manifest (client.py/test_client.py → ADR-0027-T1; plan_driver.py/plan_orchestrator.py/test_plan_driver.py → ADR-0026-T1; gate_dispatch.py/test_gate_dispatch.py → ADR-0026-T2; SKILL.md/test_generate_plan_skill_glue.py → ADR-0026-T3; core-capability-audit.sh/_a_prime_self_test.py/test_a_prime_self_test.py → ADR-0026-T4). Conversely every Manifest file appears in ≥1 task block. No task lists a directory. No file in a task block is missing from the top-level Manifest → no auto-fail. **Verification statement:** I matched each of the 12 Manifest rows to its task block and each task file-list entry back to the Manifest; the sets are identical.

### 5. Dependency Accuracy — 10/10
The Dependency Map edges are: ADR-0026-T1→T2, T1→T3, T2→T3, ADR-0027-T1→T3, T1→T4, T2→T4. Each matches a Dependencies field in the corresponding task block (T2 deps T1; T3 deps T1+T2+ADR-0027-T1; T4 deps T1+T2). The two entry points (ADR-0027-T1, ADR-0026-T1) carry "None (entry point)". The build-vs-runtime divergence is correctly modeled: ADR-0026-T1 is build-independent of ADR-0027-T1 (it drives via the fixture `dispatch` seam) even though de-id IN is the first *runtime* stage — I confirmed `run_orchestrated` already supports a fixture `dispatch`/`gate_dispatch` so the extract needs no live backend. Topological sort yields 3 parallel groups, all edges forward; **no cycle** → no auto-fail. **Verification statement:** I traced every Map edge to a Dependencies entry and every Dependencies entry to a Map edge; ran Kahn ordering by hand — acyclic, 3 groups.

### 6. Constraint Preservation — 10/10
ADR constraints land in downstream ACs: ADR-0001 (summaries-not-raw) → ADR-0027-T1 AC-3/AC-8 + ADR-0026-T3 AC-2 (every dispatch payload carries the de-identified summary only). ADR-0005 (no committed PII/key) → ADR-0027-T1 AC-7 (raw-intake-in-memory-only) + the key-via-`key_source.resolve` (never tracked) + the `block-pii-commit`/`pre-push` backstop. ADR-0016 (raw egress bounded to the no-train lane) → ADR-0027-T1 key-contract assumption (Risk Mitigations). The no-fork single-source-of-truth constraint → ADR-0026-T1 AC-2 + ADR-0026-T3 AC-3. The fixed 3-key disposition (ADR-0026 OQ-2 NOTE) → ADR-0026-T2 AC-1. INV-CORE-CAPABILITY/PF-S63-02 → ADR-0026-T4 AC-3/4. INV-CRITICAL-NON-OVERRIDABLE (the `safety_passed is True`-only surface) → ADR-0026-T1 AC-4/8 + ADR-0026-T2 AC-4. No constrained task ignores an upstream constraint → no auto-fail. **Verification statement:** I walked each in-scope ADR constraint (ADR-0001/0005/0016 + the no-fork + the fixed-key + the core-capability invariant) to its enforcing AC; each is present.

### 7. Test Strategy Coverage — 10/10
Three subsections (Unit, Integration, Risk-Specific) each name concrete tests. Unit covers every task's source via patched-SDK / fixture-`dispatch` / fixture-judge+review (criteria ADR-0027-T1 1-9, ADR-0026-T1 1-11, T2 1-7, T3 1-6, T4 1-8). Integration drives the runtime-stage-order E2E (de-id IN → driver → composed gate → revise → promote → render) and explicitly exercises a file created by one task consumed by another (T1's driver → T2's disposition → T4's self-test). Risk-Specific seeds each adversarial condition (synthetic raw-PII token, injected SDK exception, out-of-set field, `safety_passed` not-True disposition, malformed composite, non-converging revise, over-cap tally, out-of-run-set revise) and asserts the 0-threshold / fail-closed outcome. The store-adversarial battery is correctly handled: no NEW `scripts/store/` write is added (the only store write, `_promote_plans → store.append`, is MOVED-not-modified by the T1 extract and re-proven by AC-3's 1611-test green re-run) — this satisfies CLAUDE.md's store-surface rule. Every AC maps to ≥1 Test Strategy category → no untested criterion → no auto-fail. **Verification statement:** I cross-checked the "Criteria covered" lines against the full AC inventory; all 39 ACs are claimed in ≥1 category, and the store-surface exception is sound (MOVED-not-modified, re-proven by the suite).

### 8. Unresolved Concerns Handling — 10/10
Eight items (ADR-0026 OQ-1…4, ADR-0027 OQ-1…4) each carry a disposition: 6 Proceed (each tied to an in-task design decision / assumption / HARD AC — e.g. ADR-0027 OQ-3 → ADR-0027-T1 AC-7; ADR-0026 OQ-4 → ADR-0026-T4 ACs) and 2 Defer (ADR-0026 OQ-3 subscription ceiling; ADR-0027 OQ-2 retention window — both operator/operational, post-build, with written justification + "No task"). 0 Block (none needed). No undispositioned item → no auto-fail. Each Proceed names where it is resolved; each Defer states why it does not block the mock-tested build. **Verification statement:** I matched all 8 ADR open questions to a disposition row; each Proceed cites its resolving AC/assumption and each Defer its justification.

### 9. Component Overview Clarity — 10/10
The Overview is ~5 paragraphs (well over 50 words). It states WHAT (wire the two live-wiring ADRs — the live de-id backend + the A′ shared-driver), WHY (turn the mock-tested S92 engine LIVE without forking the fail-closed loop), and HOW-IT-FITS (the dependency tiers vs the runtime stage order, the EXTEND-NOT-REBUILD inner-engine freeze, the resolved tensions ADR-0027↔0001/0005 and ADR-0026's no-fork). A reader unfamiliar with the work can locate the five deliverables, the crown-jewel 0-leak obligation, and the build-vs-runtime divergence. Not missing, not under 50 words → no auto-fail. **Verification statement:** I read the Overview; it answers what/why/how-it-fits with the load-bearing EXTEND-NOT-REBUILD and runtime-vs-dependency distinctions made explicit.

### 10. Downstream Readiness — 10/10
Frontmatter carries all required fields (`scope`, `adrs`, `tier`, `created`, `status`). All required sections present in exemplar order: Component Overview, Unresolved Concerns Disposition, File Manifest, Tasks (each with Status/ADR Source/Files/Acceptance Criteria/Risk Mitigations/Dependencies — the 7 required task fields), Dependency Map (with topological ordering + numbered parallel groups), Test Strategy (3 subsections), Repo-Grounding Ledger, Validation Checklist. Task IDs follow `ADR-{NNN}-T{M}`. No placeholder text ("TBD"/"TODO: fill in"/"..."). The Dependency Map maps to build-plan waves explicitly. Parseable by build-planning → no missing required section/field → no auto-fail. **Verification statement:** I confirmed the 5 frontmatter fields, the 7 task fields on all 5 tasks, the `ADR-NNN-TM` ID format, the 3 Test-Strategy subsections, and a numbered topological order — all present.

### 11. Live-Repo Grounding — 9/10
INDEPENDENTLY re-measured (above), NOT taken from the author's Ledger. Every Manifest action matches disk (7 Create absent / 5 Modify present). Every load-bearing premise is currently true (the de-id stub, the inline loop with every sub-line exact, the gate-callable return shapes, `SUMMARY_FIELD_SET`, the audit CALLER pin, the 8 inner-engine modules, the 7 agents, the 1611-test baseline re-run green). Both non-duplication claims hold: NO existing shared driver, NO existing `gate_dispatch` composer — so the two Create artifacts that would be the auto-fail surface are genuinely new. No stale premise, no Create-on-existing / Modify-on-absent, no duplicate enforcer → no auto-fail.
**Deduction (−1):** ONE cited input is path-imprecise — `reemit_maintained` is cited as `[maintained.py:245]` but resolves to `scripts/generate/maintained.py:245`, not the implied `scripts/plan/`. The symbol AND line are correct (so it is NOT a phantom input and NOT an action mismatch — it is a *declared call-input*, not a Manifest path), but a build agent reading the bare filename could look in the wrong directory. **Fix:** write the full path `scripts/generate/maintained.py:245` in the ADR-0026-T3 file-list bullet, the SKILL.md Manifest-row prose, and the ledger RGC-3 cell. **Projected after fix: 10/10.**

---

## Summary

| # | Dimension | Score |
|---|-----------|-------|
| 1 | Traceability | 9 |
| 2 | Task Granularity | 10 |
| 3 | Acceptance Criteria Quality | 10 |
| 4 | File Manifest Completeness | 10 |
| 5 | Dependency Accuracy | 10 |
| 6 | Constraint Preservation | 10 |
| 7 | Test Strategy Coverage | 10 |
| 8 | Unresolved Concerns Handling | 10 |
| 9 | Component Overview Clarity | 10 |
| 10 | Downstream Readiness | 10 |
| 11 | Live-Repo Grounding | 9 |

**AUTO-FAIL: none fired.**
**VERDICT: ACCEPT** — every dimension ≥ 9/10. The spec is grounded, traceable, testable, and downstream-ready.

**Non-blocking polish (the only sub-10 items, both the same root cause — a single bare-filename citation):**
1. Replace the bare `maintained.py:245` citation with the full path `scripts/generate/maintained.py:245` in three places (ADR-0026-T3 file-list bullet, the SKILL.md Manifest-row prose, the ledger RGC-3 cell + the Validation-Checklist "no phantom inputs" line). This clears both the Dim-1 and Dim-11 deductions and takes the spec to a clean 10×11. It is not a phantom input (the symbol + line are correct) and does not block ACCEPT.
