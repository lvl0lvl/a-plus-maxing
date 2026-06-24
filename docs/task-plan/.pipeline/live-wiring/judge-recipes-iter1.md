---
artifact: judge-recipes-iter1
pipeline: live-wiring
spec: docs/spec/live-wiring-spec.md
build-plan: docs/build-plan/build-plan-live-wiring.md
judge: fresh (unseen authoring + remediation)
bar: ACCEPT iff ALL 10 dimensions >= 9/10
checkout: feature/engine-live-wiring-build @ 58de39d
date: 2026-06-24
---

# Judge — Live-Wiring Implementation Recipes (iter-1, bounded judge pass)

Five recipes under `docs/task-plan/.pipeline/live-wiring/`. Each scored 0-10 on the 10-dimension
recipe rubric; ACCEPT requires ALL dimensions >= 9. AUTO-FAIL checked first on every recipe.

The load-bearing remediated gates were spot-verified READ-ONLY against the live tree (not the recipe
prose): every Create target ABSENT, every Modify target PRESENT, and each non-trivial gate confirmed
RED-able-as-written against the real source shapes. **No recipe carries a vacuous / non-RED-able gate
the remediation missed.** Findings below.

## Live-tree spot-verification ledger (what was checked against source)

| Claim under test | Source checked | Verdict |
|---|---|---|
| All 8 Create targets absent | `ls` / `test -e` | PASS — all absent |
| All 6 Modify targets present | `ls` / `test -e` | PASS — all present |
| **T1** `_call` SEC-01 constant message (`SEC-4` lock is "lock existing", RED-able by `{exc!r}` variant) | `client.py:105-123` — `raise ModelCallError("backend call failed") from exc`, no interpolation | PASS — non-vacuous; the lock targets a real control |
| **T1** `MODEL = "claude-opus-4-8"` attr (AC-2 swap) + `deidentify` `NotImplementedError` stub | `client.py:135,158-160` | PASS |
| **T1** AC-7 tmp-tree rglob (not write-spy) is the right surface | live method writes nothing; AC-7 is a PIN + MUTATION-RED — correctly framed as the RED-bearer | PASS — the mutation variant is the non-vacuous lock, not the clean case |
| **T1** `ModelClient.deidentify` `isinstance(result,dict)` + `deid_in` `<= SUMMARY_FIELD_SET` + `DEID_CALL_FAILED` downstream gates | `client.py:92-95`, `deid_in.py:27,71-72` | PASS — the fail-closed ACs assert real downstream gates |
| **T1(KEYSTONE)** bare `safety_passed is True` survives in COMMENTS at :211/:378 (no-fork false-positive surface) | `plan_orchestrator.py` — bare token at :211 (comment), :378 (docstring); + :76 comment | PASS — the executable-not-token grep is REQUIRED and correctly specified |
| **T1** executable form appears EXACTLY once | `disposition.get("safety_passed") is True` at :265 only; `while True:` at :260 only | PASS — grep RED-able only on a real 2nd copy |
| **T1** ARCH-2: exactly 3 `disposition.get(...)` reads, no `disposition.get("n")` | :265 `safety_passed`, :271 `accept`, :286 `revise_domains`; 0 `disposition.get("n")` / `disposition[` | PASS — the "confirmed absent" reconciliation is accurate |
| **T1** extract-boundary line cites (252 scratch / 260 while / 265 gate / 271 accept / 273 promote / 286 revise / 301 cap) | `plan_orchestrator.py` sed-confirmed | PASS |
| **T2** `revise_domains` derivation: deductions key on rubric DIMENSIONS not plan DOMAINS — domain must come from sections, NOT the deduction | `quality_judge.py:50` (`DIMENSIONS`), `:107-121` `_empty_domain_deductions` returns `{"dimension","reason"}` only; domain is inside the `reason` string, NOT a structured field; `:245-253` verdict shape | **PASS — this is the crux; the remediation is CORRECT.** A deduction->domain map would be a bug; the recipe mandates re-walking `results[domain]["section"]["domain"]` |
| **T2** `results[domain]["section"]["domain"]` is real | `quality_judge.py:177-184` `_plan_sections` walks `results[domain]["section"]`; `assemble.py:99` sets `"domain": domain` | PASS — the localization field exists |
| **T2** `review_plan(...,*,lenses=DEFAULT_LENSES)->{findings,passed,lenses}`, `DEFAULT_LENSES`=3, `<2` raises | `safety_review.py:43,110,147` | PASS — both-gates / >=2-lens AC grounded |
| **T2** intersect with run-set `domains` (out-of-run-set guard at :286-294) | `plan_orchestrator.py:292-294` guards `d not in _ROLE_OF_DOMAIN or d not in domains` -> SAFETY_BLOCKED | PASS — AC-6 `<= run-set` targets the live guard |
| **T3** `router.summarize` at SKILL.md:48 (de-id-IN) AND :61 (operator-state-source) — phase-scoped, not whole-file | `SKILL.md:48,61`; `deid_in.py:10-11` confirms `router.summarize` SURVIVES as persisted-side gate | PASS — phase-scoped grep is correct; a whole-file-absent count would be WRONG |
| **T3** `_dispatch_prompt` is a FLAT STRING with `json.dumps(summary)` embedded (serialize-whole-payload is load-bearing) | `plan_orchestrator.py:110-133` — returns f-string with `json.dumps(summary, default=str)` inline | PASS — a dict/list recursion alone WOULD miss the in-string case; the single-serialize method is justified |
| **T4** current audit: CALLER=`generate_plan.py`:47, structural `assemble(`:54 + `record_plan(`:56, behavioral `generate_plan --self-test`:68 with `>/dev/null 2>&1` | `core-capability-audit.sh` confirmed | PASS — exit-code-only consumption (QA-3) is real; the repoint targets are grounded |
| **T4** `safety_passed` bare token survives in `plan_orchestrator.py` comments ~:76/211/378 (per-module comment-strip needed) | confirmed :76,:211,:378 | PASS |
| **T4** drop `record_plan(` is correct (A' promotes via `_promote_plans`->`store.append`, never `record_plan(`) | live loop :273 `_promote_plans`; no `record_plan(` on the A' path | PASS |
| **T4** negative-test stub cases A/B/B2/C/D + `CORE_CAP_CALLER`/`CORE_CAP_SKIP_BEHAVIORAL` | `test_core_capability_audit.sh:29-58` — exactly those 5 cases | PASS — the QA-6 rewrite enumeration matches the live stubs; correctly flagged as REQUIRED file #4 (Deviations table) |
| **T4** `generate_plan._self_test` model exists | `generate_plan.py:454`, `--self-test` CLI :541-556 | PASS |
| **T2/T1 fixtures** `_FixedJudgeClient`/`_clean_scores`/`_RecordingLensDispatch`/`_RecordingDispatch`/`_FixedDeidClient`/`_deid_summary`/`_sustaining_authors` | confirmed in the cited test files | PASS |
| **T3** `reinsert_out`:88 / `reemit_maintained`:245 / `ModelClient.deidentify`:78 | confirmed | PASS |

---

## ADR-0027-T1 — Live No-Train De-Id Backend

AUTO-FAIL scan: none triggered (prerequisites + verification commands present; no ADR/research loaded;
risk pre-check present and gated before impl; every AC -> a verification step; RED-before-GREEN with
REGRESSION on every cycle; the method fills a FROZEN seam — Interface Contracts correctly states it
SATISFIES rather than CREATES a contract; rollback = entry-state revert + Do-NOT list; manifest =
`client.py` + `test_client.py`, no creep; no placeholder/TBD).

| # | Dimension | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Entry State Completeness | 10 | 5 prerequisites incl. SDK-absent + seam-present grep commands; entry state explicitly doubles as rollback target. |
| 2 | Context Minimalism | 10 | Reads only `client.py`/`test_client.py`/`router.py`/`deid_in.py`/`key_source.py`; explicit Do-NOT-load list (ADRs, inner engine, sibling recipes, vault). |
| 3 | Risk Pre-Check | 10 | Four risks (N1/N4/N3/SEC-4) each gated to a live test before impl; placeholder-test guard stated. |
| 4 | AC Coverage | 10 | All 9 ACs + SEC-4 -> named tests in the Verification Checklist. |
| 5 | TDD Discipline | 9 | RED-before-GREEN + REGRESSION on every cycle; `/write-tests` with specific criteria. Cycles 3-4 are PIN-EXISTING-BEHAVIOR (clean case GREEN-on-oracle), and the recipe correctly relocates the RED obligation onto the MUTATION/LEAK variant — a legitimate, well-justified TDD shape for a 0-leak pin, not a GREEN-before-RED violation. |
| 6 | Interface Contract Clarity | 10 | Frozen-seam: no new contract; correctly documents the downstream summary-subset + sentinel contract it SATISFIES. |
| 7 | Change Description Quality | 10 | What+why per cycle, no literal code, sufficient to implement (model-id-from-attr, bounded-retry constant, in-memory-only). |
| 8 | Rollback Protocol | 10 | Stash/checkout/flag/escalate + explicit Do-NOT (no silent skip, no weakening the leak probe). |
| 9 | Scope Discipline | 10 | Exactly the manifest two files; EXTEND-NOT-REBUILD numstat gate on router/deid_in/key_source. |
| 10 | Downstream Readiness | 10 | Concrete paths/commands/named tests; patched-SDK construction note removes ambiguity. |

**Min dimension: 9. Verdict: ACCEPT.** (Cosmetic, non-blocking: the context cite `_good_deidentify_fixture [:90]` is the live `_good_deid_summary_fixture()` at :89 — a name/line drift in a read-pointer, not an executable gate; the worker reads the file. Not a fix-list item.)

---

## ADR-0026-T1 — Shared Control-Inversion Driver Extraction (KEYSTONE)

AUTO-FAIL scan: none triggered. The no-fork probe (the most error-prone gate) is the load-bearing
remediation and is verified RED-able-as-written: it greps EXECUTABLE control flow (`while True:` header
+ the `disposition.get("safety_passed") is True` expression on a non-comment line), explicitly NOT the
bare token that survives in comments at :211/:378 — confirmed against live source. The frozen-engine
gate is correctly demoted from a RED-first pytest to a standing SHELL gate (`<wave-base>` =
`git merge-base`, unresolvable inside pytest) — a correct fix, not a skipped criterion.

| # | Dimension | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Entry State Completeness | 10 | Baseline + inner-engine-present + inline-loop/seam/store-write greps; rollback target stated. |
| 2 | Context Minimalism | 10 | Reads wrapper + `pipeline.py` signature + the two oracle test suites; Do-NOT-load list (incl. the inner engine save for pipeline's signature). |
| 3 | Risk Pre-Check | 10 | Six risks (N2/fork/safety-not-True/frozen-engine/store-keying) each gated; the fork + frozen-engine gates carry the QA-1/QA-2 corrections. |
| 4 | AC Coverage | 10 | AC-1..11 + QA-2 golden-line -> named tests; ARCH-2 disposition-read preservation enumerated against live grep. |
| 5 | TDD Discipline | 10 | 5 cycles RED->GREEN->REFACTOR->REGRESSION; the golden-line capture is correctly sequenced BEFORE GREEN (a runtime re-capture would be tautological — QA-3 explicitly addressed). |
| 6 | Interface Contract Clarity | 10 | CREATES the `plan_driver` drive-protocol: yielded-request + `.send()` envelope + FIXED 3-key disposition read + change-control (Architect review). The keystone consumed interface is fully specified. |
| 7 | Change Description Quality | 10 | Extract-by-structure boundary named by line; helper-home decision left to the worker with the no-fork grep as oracle; no literal code. |
| 8 | Rollback Protocol | 10 | Stash/checkout/flag/escalate + Do-NOT (no weakening fork / safety-not-True / behavior-preservation probes). |
| 9 | Scope Discipline | 10 | `plan_driver.py` + `plan_orchestrator.py` + test + the committed golden fixture — all in manifest; inner-engine numstat=0 gate. |
| 10 | Downstream Readiness | 10 | Concrete; the executable-not-token grep, the merge-base shell gate, and the static golden oracle remove the three ambiguities a naive author would hit. |

**Min dimension: 10. Verdict: ACCEPT.** The disposition-read enumeration's "`disposition.get("n")`
reconciliation" was verified accurate (0 such reads live) — a correct closure of a phantom read, not a
gap.

---

## ADR-0026-T2 — Composed `gate_dispatch` Adapter

AUTO-FAIL scan: none triggered. The crux remediation — the `revise_domains` derivation rule — was
verified against `quality_judge.py`: deductions carry `{"dimension","reason"}` ONLY, the `dimension`
is a RUBRIC dimension (followability/coherence/internal-consistency/completeness), and the plan domain
lives inside the `reason` STRING, never a structured field. The recipe's rule (re-walk
`results[domain]["section"]["domain"]` for structural deductions; all-run-set fallback for
dimension-level deductions; intersect with run-set) is the ONLY correct derivation and is buildable
without editing any gate module. AC-2 is non-tautological (asserts the derivation rule via two
distinct fixtures, not a fixed list).

| # | Dimension | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Entry State Completeness | 10 | T1-complete prerequisite + gate-callables grep; rollback = Wave-1 checkpoint HEAD. |
| 2 | Context Minimalism | 10 | Reads the two gate modules + the driver's disposition contract + the two mock fixtures; Do-NOT-load list. |
| 3 | Risk Pre-Check | 10 | Malformed-composite / 3-key / >=2-lens risks each gated to a test. |
| 4 | AC Coverage | 10 | AC-1..7 + the QA-4 T1<->T2 seam assertion -> named tests. |
| 5 | TDD Discipline | 10 | 3 cycles RED->GREEN->REFACTOR->REGRESSION; fail-closed RED-capability stated (default-True variant -> RED). |
| 6 | Interface Contract Clarity | 10 | The composer's 3-key OUTPUT contract fully specified incl. the derivation rule + fail-closed `safety_passed` + change-control. |
| 7 | Change Description Quality | 10 | The derivation rule is spelled out with the exact source field (`section.get("domain")` per `quality_judge._empty_domain_deductions`), no literal code, dimension-vs-domain trap explicitly called out. |
| 8 | Rollback Protocol | 10 | Stash/checkout/flag/escalate + Do-NOT (no malformed-composite surfacing `safety_passed: True`). |
| 9 | Scope Discipline | 10 | `gate_dispatch.py` + test only; numstat=0 on inner engine + both gate modules. |
| 10 | Downstream Readiness | 10 | The QA-4 seam test (real composer -> real driver) at Wave 2 moves the shape-mismatch catch upstream; concrete throughout. |

**Min dimension: 10. Verdict: ACCEPT.** The single most-likely-to-be-wrong gate (deduction->domain
conflation) is explicitly AVOIDED — the remediation is correct, not merely present.

---

## ADR-0026-T3 — `/generate-plan` Skill Front-Door

AUTO-FAIL scan: none triggered. The 0-raw-PII scan remediation — serialize the FULL payload string
(`json.dumps(payload, default=str)`) rather than dict/list-recurse — is verified load-bearing:
`_dispatch_prompt` returns a flat f-string with `json.dumps(summary)` embedded, so a recursion alone
WOULD miss an in-string raw token. The phase-scoped `router.summarize` prose-grep is correct (the
token legitimately survives elsewhere as the persisted-side store-read gate, per `deid_in.py:10-11`) —
a whole-file-absent count would be a false gate. The no-fork-at-skill grep reuses the verified
executable-not-token fix.

| # | Dimension | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Entry State Completeness | 10 | T1/T2/T-de-id complete + agent-roster grep; rollback = Wave-2 checkpoint HEAD. |
| 2 | Context Minimalism | 10 | Reads SKILL.md + driver + client + gate_dispatch + reinsert_out/maintained + `_dispatch_prompt` shape; Do-NOT-load list. |
| 3 | Risk Pre-Check | 10 | 0-raw-PII / skill-fork / deterministic-substitute risks each gated. |
| 4 | AC Coverage | 10 | AC-1..6 -> named tests; SEC-6 residual (live-agent 0-PII) EXPLICITLY deferred to S94, not silently dropped. |
| 5 | TDD Discipline | 9 | 3 cycles RED->GREEN->REGRESSION; the 0-PII clean case is a PIN with the RED relocated onto the in-string-raw-token variant (justified for a structural-hold property), and the prose-grep ACs are genuine RED-first against the unreconciled SKILL.md. |
| 6 | Interface Contract Clarity | 10 | Correctly states it CREATES no new interface — CONSUMES the T1 protocol + T2 composer + T-de-id seam; documents the dispatch protocol as a USE. |
| 7 | Change Description Quality | 10 | Both `router.summarize` refs (:48 + :61) named with the exact reconciliation + the disambiguation sentence; no literal code in SKILL.md. |
| 8 | Rollback Protocol | 10 | Stash/checkout/flag/escalate + Do-NOT (no weakening the full-payload scan or the no-fork grep). |
| 9 | Scope Discipline | 10 | SKILL.md (prose) + glue test only; numstat=0 on inner engine; "no production Python added" stated. |
| 10 | Downstream Readiness | 10 | The single-serialize method is pinned (not an "OR recursion" ambiguity); the phase-scoped grep removes the false-absent trap. |

**Min dimension: 9. Verdict: ACCEPT.**

---

## ADR-0026-T4 — Core-Capability-Audit Repoint + A′-Inversion `--self-test`

AUTO-FAIL scan: none triggered. Three load-bearing remediations verified: (1) the structural grep is
PINNED per-module — `$CALLER`=`plan_driver.py` hosts the disposition gate, `RUN_GEN_HOST`=
`plan_orchestrator.py` hosts `pipeline.run_generation` — matching the real two-module A′ spine; (2) the
self-test drives the REAL `gate_dispatch` composer (ARCH-4) over fixture judge/review, so `depends-on
ADR-0026-T2` is a real edge and the inversion comes from the composer's fail-closed surface, not a
hand-shaped disposition; (3) the audit-exits-nonzero-on-broken-spine gate (QA-3) is present and targets
the verified exit-code-only consumption (`>/dev/null 2>&1` at :68) — the self-test signals via NON-ZERO
EXIT, not a printed message. The negative-test rewrite (cases A/B/B2/C/D) matches the live stubs and is
correctly flagged as a REQUIRED 4th file in a Deviations table.

| # | Dimension | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Entry State Completeness | 10 | T1/T2 complete + audit-scaffold + negative-test-present grep; rollback = Wave-2 checkpoint HEAD. |
| 2 | Context Minimalism | 10 | Reads audit + `generate_plan._self_test` model + driver + composer + audit-helpers + the negative-test stubs; Do-NOT-load list. |
| 3 | Risk Pre-Check | 10 | PF-S63-02 tautology / exit-code-chain / F-008 fail-closed risks each gated. |
| 4 | AC Coverage | 10 | AC-1..8 + QA-3 exit-code chain + QA-6 negative-test rewrite -> named tests/cases. |
| 5 | TDD Discipline | 10 | 4 cycles RED->GREEN->REGRESSION; the broken-spine RED is the non-tautology proof; the negative-test-still-RED is gated. |
| 6 | Interface Contract Clarity | 10 | The `--self-test` exit-code contract is defined+consumed within the task (both sides in-manifest); correctly not a cross-task interface. |
| 7 | Change Description Quality | 10 | Per-module grep targets named with host modules + comment-strip rationale; `record_plan(`-drop justified; no literal code. |
| 8 | Rollback Protocol | 10 | Stash/checkout/flag/escalate + Do-NOT (no tautological guard, no print-then-exit-0). |
| 9 | Scope Discipline | 10 | 3 manifest files + the negative-test (REQUIRED, in a Deviations table per scope-discipline) — the cross-doc-ownership-correct way to flag the 4th file. |
| 10 | Downstream Readiness | 10 | The QA-5 per-module pin + QA-6 case-by-case rewrite enumeration remove every ambiguity an author would hit on the two-module spine. |

**Min dimension: 10. Verdict: ACCEPT.**

---

## Summary

| Recipe | Wave | Min dim | Verdict |
|--------|------|---------|---------|
| ADR-0027-T1 (live de-id backend) | 1 | 9 | **ACCEPT** |
| ADR-0026-T1 (KEYSTONE shared driver) | 1 | 10 | **ACCEPT** |
| ADR-0026-T2 (composed gate_dispatch) | 2 | 10 | **ACCEPT** |
| ADR-0026-T3 (/generate-plan front-door) | 3 | 9 | **ACCEPT** |
| ADR-0026-T4 (audit repoint + A′ self-test) | 3 | 10 | **ACCEPT** |

**All 5 recipes ACCEPT (every dimension >= 9). No REVISE. No fix list.**

Every load-bearing remediated gate was verified RED-able-as-written against the live tree:
- T1 frozen-engine probe is a SHELL gate (merge-base, not a RED pytest) + the no-fork grep targets the
  executable `disposition.get("safety_passed") is True` expression, NOT the bare token surviving in
  comments at :211/:378.
- T2 `revise_domains` derivation re-walks `results[domain]["section"]["domain"]` with an all-run-set
  fallback — it does NOT conflate the deduction's rubric-dimension with a plan domain (verified: the
  deduction carries `{"dimension","reason"}` only; domain is inside the reason string).
- T3 0-raw-PII scan serializes the full payload string (load-bearing because `_dispatch_prompt` embeds
  `json.dumps(summary)` in a flat f-string a recursion would miss); the `router.summarize` prose-grep
  is phase-scoped (the token legitimately survives as the persisted-side store-read gate).
- T4 structural grep is pinned per-module (`$CALLER`=plan_driver.py, RUN_GEN_HOST=plan_orchestrator.py),
  the self-test drives the real composer, and the audit-exits-nonzero-on-broken-spine gate is present
  against the verified exit-code-only (`>/dev/null 2>&1`) consumption.

One cosmetic, non-blocking note (not promoted to a fix because it is a read-pointer, not an executable
gate): T1's context-load cite `_good_deidentify_fixture [:90]` is the live `_good_deid_summary_fixture()`
at :89 — a name/line drift in a "files to read" pointer; the worker reads the file, so it does not
introduce executable ambiguity.
