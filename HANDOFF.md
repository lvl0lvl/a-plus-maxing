---
title: Session Handoff
type: note
owner: Walter McGivney
created: 2026-05-16
last_reviewed: 2026-06-20
status: active
depends_on: []
superseded_by: null
review_cadence: weekly
---

# Session Handoff

## Scope Contract — Session 94 (2026-06-24)

Goal: Complete the recipe stage (apply the laddered review-findings ledger + judge + promote), then **BUILD the plan-generation engine LIVE-WIRING** via `/execute-plan` (wave by wave, mock/fixture-tested, 0 live spend) — as many of the 3 waves as the session allows, each with its EXECUTED checkpoint Go/No-Go + Tier-3 `/review-pr` → `/merge` — so the ONLY remaining step is the operator-present LIVE test. (AUTONOMOUS; operator-directed: "open the session, write the scope contract and proceed.")

Acceptance criteria:
- [ ] AC1 (recipe stage — the PF-S93-01 carry-over): the 12 laddered executability findings applied to the recipes **per-task** (one agent per recipe — PF-S93-01 lesson, NOT a single batched dispatch); the recipe judge pass (Phase 6/7) ACCEPT ≥9/dim; recipes promoted `draft-ADR-002x-T*.md` → `docs/task-plan/<id>.md`. (ARCH-1 already fixed in the T2 draft.)
- [ ] AC2 (Wave 1): ADR-0027-T1 (live de-id backend) + ADR-0026-T1 (keystone control-inversion driver) built TDD-per-recipe; Wave-1 checkpoint EXECUTED green (the behavior-preservation TRIAD: inner-engine numstat=0 + 0 forked loop copies + suite green; the de-id crown-jewel 0-leak: 0 raw-PII past the boundary + raw-intake-in-memory-only + fail-closed `ModelCallError`).
- [ ] AC3 (Wave 2): ADR-0026-T2 composed `gate_dispatch` built; checkpoint green (exact 3-key disposition + fail-closed-on-malformed + both-gates-run + the composer-driver seam).
- [ ] AC4 (Wave 3): ADR-0026-T3 `/generate-plan` skill front-door + ADR-0026-T4 core-capability-audit repoint built; checkpoint green (runtime-stage-order E2E on fixtures + audit on the A′ spine + the non-tautological `--self-test`); `core-capability-audit.sh` repointed off `generate_plan.py` onto the A′ spine (closes `71s4`/PF-S63-02).
- [ ] AC5 (review→merge): every built wave through the full Tier-3 `/review-pr` 6-agent with independence intact (profile-less blind-triage + EXECUTED blind-verify); LEGITIMATE findings fixed + blind-verified → `/merge` to `main`.
- [ ] AC6 (close): full automatic close on final post-merge `main` + cite the SHA (PF-S74-01).

Files I WILL touch: `scripts/model/client.py` (`_ClaudeNoTrainBackend.deidentify`); `scripts/plan/plan_driver.py` (NEW), `scripts/plan/plan_orchestrator.py` (the wrapper re-point — behavior-preserving refactor), `scripts/plan/gate_dispatch.py` (NEW), `scripts/plan/_a_prime_self_test.py` (NEW); `scripts/core-capability-audit.sh` (repoint); `.claude/skills/generate-plan/SKILL.md` (the A′ front-door reconcile); `tests/*`; the recipes (apply ledger + promote to `docs/task-plan/`); the close docs (staged by EXPLICIT path).
Files I will NOT touch: the INNER ENGINE (`scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py` — numstat=0); the built gate callables (`quality_judge`/`safety_review`)/`deid_in`/`reinsert_out`/`maintained.py` (WIRED not rewritten); `scripts/store/store.py`+`keying.py`; the dashboard (LOCKED); `vault/library/*`; `main` directly; the keychain.
NOT doing: the operator-present LIVE end-to-end run (the operator injects the key; agent never touches the keychain; never commit the key — PUBLIC repo); ANY live API call (mock/fixture-tested, 0 spend); forcing ALL 3 waves if context runs low (checkpoint cleanly at a wave boundary with a clean HANDOFF if so — each wave is a natural session boundary per V1 Build Execution).
Invariants at risk: ADR-0001/0005/0016 (the crown-jewel PII boundary — the live de-id is the API egress; fail-closed); INV-CORE-CAPABILITY (the audit repoint CLOSES PF-S63-02); INV-ROLE-INLINING (full profiles on EVERY dispatch); INV-BRANCH-NOT-MAIN; the close gates; PF-S74-01; PF-S92-01 (never stop mid-loop to ask a settled question); PF-S93-01 (per-task remediation, NOT batched).

**Core-capability-first gate (PF-S63-02):** YES — this IS the core-capability build (the engine → a live front door + the live de-id backend → the audit repointed onto the A′ spine proving the real capability is wired). The direct path, not secondary work.

**v1-build attestation (V1 Build Execution):** executes the approved 3-wave `docs/build-plan/build-plan-live-wiring.md`; the prior stage (recipes) is completed FIRST (its design checkpoint). Build via `/execute-plan` per V1 Build Execution — never hand-rolled (PF-S36-01); plan-integrity grounds + gates each wave transition.

**S94 self-confirmation (autonomous):** contract committed at session-OPEN (the PF-S91 lesson) per the operator's explicit "write the scope contract and proceed" + the standing autonomous directive.

## Scope Contract — Session 93 (2026-06-24)

Goal: Design + build the **live-wiring** that connects the built plan-generation engine to real clients — so the ONLY remaining step is the operator-present LIVE test — via the full autonomous build pipeline (`/create-adr` → spec → build-plan → task-plan → `/execute-plan`), mock/fixture-tested (0 live spend). **Runtime split (operator decision, S93): PII-related → no-train API (the de-id-IN boundary, the one model call that sees raw operator PII); everything else (the plan-domain specialists, the quality judge, the safety-review lenses, the orchestrator control flow) → subscription (Claude Code agent dispatch, like the autonomous build pipeline); de-id OUT stays deterministic (no model, already built).**

Acceptance criteria:
- [ ] AC1 (design): `/create-adr` authors the live-wiring runtime ADR(s) — capturing the PII-API / subscription-else split + RESOLVING how the programmatic orchestrator drives subscription specialist/gate dispatch (the skill-as-orchestrator-control-surface vs Python-driven question); judged ≥9/dim + red-teamed; landed.
- [ ] AC2 (plan): spec → build-plan → per-wave recipes, each recipe-reviewed (QA+Security+Architect) + judged ACCEPT; landed.
- [ ] AC3 (build): `/execute-plan` builds the wiring — the live `_ClaudeNoTrainBackend.deidentify` (real no-train API call, mock-tested via patched SDK, 0 spend); the production front door (reads real operator state → de-id via API → subscription specialist+gate dispatch → `run_orchestrated` → `reinsert_out` → maintained render); the composed `gate_dispatch` adapter; `core-capability-audit.sh` repointed from `generate_plan.py` to the engine path. EXTEND-NOT-REBUILD on the inner engine + the gate callables.
- [ ] AC4 (review→merge): every code PR through the full Tier-3 `/review-pr` 6-agent with independence intact; LEGITIMATE findings fixed + blind-verified → `/merge`.
- [ ] AC5 (close): full automatic close on final post-merge `main` + cite the SHA (PF-S74-01). The LIVE test itself is the operator-present NEXT step (S94) — NOT in scope here.

Files I WILL touch: `docs/adr/*` (the live-wiring ADR + backfill), `docs/spec/*`, `docs/build-plan/*`, `docs/task-plan/*`; `scripts/model/client.py` (`_ClaudeNoTrainBackend.deidentify` real call); a new production front-door (a `.claude/skills/generate-plan/` rewrite and/or a thin `scripts/plan/` entry that composes the seams); `scripts/core-capability-audit.sh` (repoint); `tests/*`; the recipes' `status`; the close docs (staged by EXPLICIT path).
Files I will NOT touch: the INNER ENGINE (`scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py` — EXTEND-NOT-REBUILD) + the built gate callables (`quality_judge`/`safety_review`)/`deid_in`/`reinsert_out`/`maintained.py`/`dispatch_budget` (WIRED not rewritten); `scripts/store/store.py`+`keying.py`; the dashboard (LOCKED); `vault/library/*`; `main` directly; the keychain.
NOT doing: ANY live API call (mock-tested via a patched SDK; 0 spend); the LIVE end-to-end run (operator-present, S94 — the operator injects the key); ingesting real operator data (operator-side).
Invariants at risk: ADR-0001/0005/0016 (the crown-jewel PII boundary — the API de-id is the relaxation; subscription pieces see only de-identified data); INV-CORE-CAPABILITY (repointing the audit to the engine path is the PF-S63-02 close); INV-ROLE-INLINING; INV-BRANCH-NOT-MAIN; the close gates; PF-S74-01; PF-S92-01 (do NOT stop mid-loop to ask a settled question).

**Core-capability-first gate (PF-S63-02):** YES — this IS the core capability wiring (the engine → a live front door → `core-capability-audit` repointed to it). The direct path, not secondary work.

**S93 self-confirmation (autonomous):** contract committed at session-OPEN (the PF-S91 lesson) per the operator's directive ("complete everything needed to get us to the live test … API for PII, subscription for everything else") + the standing autonomous directive.

## Scope Contract — Session 92 (2026-06-24) — ARCHIVED (see vault/sessions/session-92.md)

Goal: Run the **FULL autonomous build pipeline** to design + build the **plan-generation engine** — the operator-confirmed (S91) full-target multi-agent architecture — end to end (`/create-adr` → `/create-spec` → `/create-build-plan` → `/create-task-plan` → `/execute-plan`), with extra-engaged monitoring (the pipeline is the live reference model for how the health-plan pipeline gets organized) + beading new-skill/command rough edges. (AUTONOMOUS; operator-directed: "run the full autonomous build pipeline … build out everything.")

Acceptance criteria:
- [ ] AC1 (design): `/create-adr` authors the engine ADR set (0020–0025), exhaustively verified → judged ≥9/dim → red-teamed → fixed; landed (PR).
- [ ] AC2 (plan): `/create-spec` → `/create-build-plan` → per-wave `/create-task-plan` recipes, each recipe-reviewed (QA+Security+Architect, the design-defect gate) + judged ACCEPT before build; landed.
- [ ] AC3 (build): `/execute-plan` builds all 4 dependency-ordered waves (PII envelope → orchestrator → gates+output → revise loop), each TDD-per-recipe, mock/fixture-tested (0 live spend), checkpoint Go/No-Go EXECUTED green, EXTEND-NOT-REBUILD held.
- [ ] AC4 (review→merge): every code PR through the full Tier-3 `/review-pr` 6-agent with independence intact (profile-less blind-triage P3 + EXECUTED blind-verify P7); all LEGITIMATE findings fixed + blind-verified → `/merge`.
- [ ] AC5 (close): full automatic close on final post-merge `main` + cite the SHA (PF-S74-01).

Files I WILL touch: `docs/adr/*` (the engine ADRs + the backfill), `docs/spec/*`, `docs/build-plan/*`, `docs/task-plan/*`; `scripts/plan/{deid_in,plan_orchestrator,quality_judge,safety_review,dispatch_budget,reinsert_out}.py`, `scripts/model/client.py` (the `deidentify` extension), `scripts/generate/maintained.py`, `.claude/hooks/lib/pii-scan-scope.sh` + its fixture, `tests/*`; the recipes' `status`; the close docs (staged by EXPLICIT path — never `git add vault/`).
Files I will NOT touch: the INNER ENGINE (`scripts/plan/{orchestrate,pipeline,assemble,generate_plan,adjudicate,adjust,track,router}.py` — EXTEND-NOT-REBUILD, wired not rewritten); `scripts/ingest/*`; `scripts/store/store.py`+`keying.py`; the dashboard (LOCKED); `vault/library/*`; `main` directly; the keychain.
NOT doing: the LIVE end-to-end run (operator-present; the operator injects the key — `run_orchestrated` has no production caller yet, bead `71s4`); ANY live API call (mock/fixture-tested, 0 spend); a dashboard redesign (Clinical Light LOCKED).
Invariants at risk: ADR-0001/0005/0016 (the crown-jewel PII boundary — the de-id IN/OUT envelope moves raw/re-inserted PII; fail-closed); INV-CORE-CAPABILITY; INV-ROLE-INLINING (full profiles on EVERY dispatch); INV-BRANCH-NOT-MAIN; the close gates; the `AP-SELF-REVIEW-UNDER-PROBES-INTERACTION-SURFACE` class; PF-S74-01.

**Core-capability-first gate (PF-S63-02):** does the core capability work yet? The engine is now BUILT end-to-end (de-id IN → orchestrate → {judge ∥ safety} → revise → de-id OUT → render), mock/fixture-tested; the LIVE run (real model client + operator data) is the explicit next step (bead `71s4`). This IS the direct path to the core capability — the gate is satisfied.

**S92 self-confirmation (autonomous):** contract authored retroactively at close (S92 grew from the S91-close continuation into the operator's full-pipeline directive; the work matched the directive throughout). Per the standing autonomous directive + the operator's mid-session re-issues ("run the full build pipeline to completion … if ambiguous choose the more robust / more rigorous path").

### S93 Scope Contract Evaluation (2026-06-24, volatile)

- **AC1 (design ADRs) — PASS.** `/create-adr` (8-phase) authored ADR-0026 (V1 subscription-runtime driver A′ — skill-as-orchestrator, control-flow-inverted; amends ADR-0022) + ADR-0027 (live no-train de-id backend; implements ADR-0020). Verify 19/19 + 24/24 citations resolve → judge ACCEPT 10/10 every dim (incl. a crown-jewel PII-Boundary-Integrity dim) → red-team (9 findings; the 2 HIGH — keystone buildability + core-capability-audit-can't-verify — drove real Decision corrections) → final-verify 0 failures. Landed PR #247 → `main` `e3d5789` (3-agent docs `/review-pr`; 1 LEGITIMATE QUAL-1 fixed+blind-verified; rebase merge).
- **AC2 (plan) — PASS (design stages); recipe judge DEFERRED.** `/create-spec` (judge ACCEPT 10/10, live-repo-grounding re-measured) + `/create-build-plan` (judge ACCEPT 10/10; the QA+Security review HARDENED the checkpoints — vacuous/tautological-pass risk on 3 crown-jewel gates) committed on the branch. The 5 recipes were authored (grounded, no blocking spec defect) + reviewed (QA all 5 + Architect keystone/wiring + Security de-id/PII) — the review CAUGHT a real CONTRACT gap (ARCH-1: `gate_dispatch` revise_domains derivation unsatisfiable — `quality_judge` deductions key on rubric dimensions, not plan domains) + 12 executability findings. ARCH-1 FIXED inline; the 12 laddered to S94 build-RED time in a committed ledger (`docs/task-plan/.pipeline/live-wiring/review-findings.md`). The recipe JUDGE pass (Phase 6/7) + promotion to `docs/task-plan/<id>.md` DEFERRED — a monthly spend limit interrupted the remediation subagent (PF-S93-01).
- **AC3 (build) — DEFERRED to S94 (per operator directive "set up the rest of the build for the next session").** The `/execute-plan` CODE build was NOT executed — the build is fully SET UP (recipes + ledger + build-plan checkpoints), ready to run wave by wave next session. NOT a failure: the operator framed THIS session as the setup.
- **AC4 (review→merge per code PR) — N/A** (no code built; the ADR PR #247 went the full lifecycle).
- **AC5 (close) — PASS** (this close, on the branch HEAD; no main merge beyond #247).

### Drift checks (S93 close)

- **Task drift — CHANGED (documented, operator-aligned):** the session delivered the full DESIGN pipeline (ADR merged → spec → build-plan → recipes), NOT the code build — matching the operator's directive ("set up the rest of the build for the next session … complete everything needed to get us to the live test"). The one in-session deviation: the recipe stage is not pipeline-complete (judge skipped, 12 findings laddered) under a spend-limit interruption — captured PF-S93-01 + the committed ledger (a forcing function, not a silent drop).
- **Architecture drift — none toward violation.** The design ENCODES the crown-jewel guards: the API de-id boundary (ADR-0027 — the operator-signed-off ADR-0001/0016 egress relaxation, fail-closed to `ModelCallError`, summary ⊆ `SUMMARY_FIELD_SET`, raw-intake-in-memory-only, key runtime-only/never-committed); the no-fork single-source fail-closed safety loop (ADR-0026's behavior-preserving control-inversion refactor — the keystone the red-team CORRECTED from a forked-loop hazard, scoping the freeze to the inner engine, run_orchestrated the refactorable wrapper); the audit-repoint that CLOSES PF-S63-02 (ADR-0026-T4 — the audit asserts the A′ spine). No invariant moved toward violation.
- **Vision drift — none.** Still the local-first health tracking + planning system; this session designed the runtime that wires the built engine to live clients. `design/vision.md` first sentence unchanged.

### Per-PR gated-skill invocation table (INV-SKILL-TRACE)

| PR | `/review-pr` invoked fresh | `/merge` invoked fresh | Outcome |
|----|----------------------------|------------------------|---------|
| #247 — live-wiring ADRs 0026/0027 + 9 backfills + scope contract | YES — 3-agent docs subset (Architect/Historical-Context/Code-Quality) over the local three-dot diff, GraphQL exhausted; profile-less blind-triage + executed blind-verify intact | YES — REST fallback (full-40-char SHA `-f sha=` guard), rebase, branch deleted local+remote | Merged → `main` `e3d5789` (2026-06-24 S93); 1 LEGITIMATE (QUAL-1, a stale "frozen loop" prose contradiction) fixed + blind-verified RESOLVED; quality gate PASS |

### PF attestation

S93 close (2026-06-24): **One new PF promoted — PF-S93-01** (the recipe-stage pipeline left incomplete — the judge pass skipped + 12 executability findings laddered — when a monthly spend limit interrupted a SINGLE BATCHED remediation subagent; the batched-remediation all-or-nothing design lost the in-progress fixes a per-task remediation would have preserved. Mitigated: the one build-BREAKING finding ARCH-1 — the `gate_dispatch` revise_domains contract gap — was fixed inline; the 12 executability findings captured in a committed ledger as a per-wave blocking dependency for S94, a forcing function not a silent drop. Captured PF-log + bead + harvest). The defining POSITIVE: the full DESIGN pipeline ran with the LAYERED REVIEW catching a real CONTRACT defect (ARCH-1) + 12 executability defects BEFORE the build — the recipe-review (the design-defect gate) working exactly as designed, which is the operator's stated meta-goal (the pipeline informs how the health-plan pipeline gets organized). Prior lessons referenced DESCRIPTIVELY (the never-hand-roll-the-build discipline held — used /create-adr, /create-spec, /create-build-plan, /create-task-plan in full; the more-rigorous-path-on-ambiguity heuristic resolving the A′ driver model + the ARCH-1 contract; the autonomous-loop discipline — drove the design pipeline continuously without stopping to ask), never by bare token.

### Disclosure ledger (S93 close)

Caught this session: 3 (all self/gate-caught, surfaced by me; 0 reached the operator only because they asked).
- ARCH-1 — the `gate_dispatch` revise_domains contract gap (deductions key on rubric dimensions, not plan domains) — detection: gate (Architect recipe-review); surfaced_by: self. Fixed inline.
- The 12 recipe executability findings (frozen-engine probe GREEN-at-RED; no-fork grep false-positives on docstring tokens; T4 structural-check token-to-module mis-pin; etc.) — detection: gate (QA/Architect/Security recipe-review); surfaced_by: self. Laddered to S94 in a committed ledger.
- The /create-adr red-team RT-01/RT-02 ADR keystone defects (the byte-frozen-run_orchestrated over-constraint + the audit-can't-verify-the-A′-path) — detection: gate (red-team); surfaced_by: self. Fixed in the ADRs before merge.

**Historical (kept for reference):** `vault/sessions/session-93.md`.

## Historical Scope Contracts (archived)

Scope contracts for Sessions 5-91 + their evaluations were moved to `vault/sessions/scope-contract-archive.md` (S32 archived the S5-31 set; …; S89 archived S88; S90 archived S89; S91 archived S90; S92 archived S91; S93 archived S92) to keep this handoff lean. The current (S93) scope contract is above; the archive holds the prior-session archaeology.

## Session 4 close — 2026-05-25

Two cycles this session: (a) the user caught and challenged orchestrator self-attestation of 5 of 6 aplus-research gates (PF-S3-01, recurrence_count=2 of the PF-S2-01 class); (b) rigor-framework adoption + mechanical resistance built and the BPC-157 entry re-verified clean through path-(b) re-dispatches. Commit `8b05b30`. The attestation_chain is now intact across all 6 gates with sha256 of each agent-written source.

**Historical (kept for reference):** Session 3 BPC-157 rebuild context lives in `vault/sessions/session-3.md` (the entry-rebuild itself was at commit `7a98c72`, 2026-05-24).

## Recovery After Compaction

If context was compacted, run `bd prime` then:
1. Read this file (HANDOFF.md)
2. Read `vault/meta/overview.md` (system state summary + knowledge-layer map)
3. Read `vault/meta/contradictions.md` if it exists
4. Read MEMORY.md (in `~/.claude/projects/-Users-waltermcgivney-Documents-Projects-a-plus-maxing/memory/`)
5. Read `vault/WIKI.md` (wiki schema + agent consumer roster)
6. Query vault for current phase (basic-memory search)
7. Read the most recent session note in `vault/sessions/`
8. Read `vault/decisions/` for architecture decisions
9. Read `.claude/skills/aplus-research/SKILL.md` (project-local research skill with blocking gates — the path to use for all wiki-bound research from session 3 forward)
10. Read `vault/design/artifact-design-protocol.md` before generating any HTML artifact

## What Changed (Session 3, 2026-05-24)

### `aplus-research` skill development (pre-restart)
- `--update[=<reason-slug>]` flag implemented. Phase 2.75 archive-before-write; default slug `rerotation`; pattern enforced. SKILL.md, gate-2.75.schema.json (+ `update_mode`, `update_reason_slug`, `archive_paths`, 3 new halt reasons, conditional invariant), commands/aplus-research.md updated. 8/8 schema smoke-test cases pass.

### BPC-157 canonical rebuild — first end-to-end run of `aplus-research`
- Invoked `/aplus-research "Build canonical library entry for BPC-157" --mode=deep --target=peptide/bpc-157 --update=suspect-fabrications`.
- **All 6 blocking gates PASS, schema-validated.** Gate sequence: 2.75 SCOPE (archived 4 prior artifacts) → 3.5 JUDGE (6 paired retrieval+judge dispatches; 3 sections needed iter-2 remediation; final scores 100/100/100/99/99/100) → 4.75 INTEGRITY (7 IC-10 metadata fixes applied across 4 sections; IC-13 corpus scoping 30/30 probes PASS, **zero fabricated claims detected**) → 6 CRITIQUE (15 findings: 1 critical citation-crosswalk + 9 major + 5 minor; all addressed in Phase 7 refine) → 7.5 RISK-FLOOR (risk_tier=experimental, 8 third-party monitoring markers named, contraindications + monitoring + stopping criteria all populated) → 8.5 LAYERS (practitioner-layer + non-english-layer both written with bibliography + self-check).
- **Canonical fabrication catch:** S2 dispatch attributed He L 2022 (*Front Pharmacol* 13:1026182) as a human PK study. Independent verification via PMC9794587 (Section D + Section E + IC-13 grep) confirmed: rats (n=324) + beagle dogs (n=6), **no human subjects**. There is no published human PK paper for BPC-157. This is the load-bearing correction that justified the rebuild.
- **6 additional bibliographic corrections** logged to `vault/meta/contradictions.md` as C1–C7 (Xu 2020 institution → Fourth Military Medical Univ Xi'an, not PLA Beijing; Sikirić 1993 PMID 8298609 not 8298605; McGuire FP not Bemis-Standoli as first author of *Curr Rev Musculoskelet Med* 2025; Lee & Burgess 2025 co-author Burgess K not C; FDA 503A Cat 2 removed April 22 2026 via nominations withdrawal NOT safety clearance; Xue 2004 → Fourth Military Medical Univ Xi'an = secondary concentration finding placing 3 papers in single Xi'an cluster; Klicek R/Sever M author order on PMID 24304574).
- **Concentration audit:** 52 deduplicated primaries; 75.0% Sikirić-Zagreb academic share; 80.8% combined Zagreb metro (incl. Pliva industrial). Far above 70% threshold. Mandatory first-class concentration section surfaced in synthesis §2 before any indication subsection. Largest non-Sikirić cluster = Chang Gung Taiwan (4); secondary independent finding: Xi'an Fourth Military Medical Univ has 3 papers (single-institution cluster on the "independent Chinese signal").
- **Honest absences surfaced:** no independent in-vivo MSK replication exists outside Sikirić cluster; no human PK paper exists in any language; no chronic >6-week GLP package; no Phase 3 RCT; only 2 registered interventional human trials worldwide (none with results posted); Edwin Lee single-investigator/single-clinic = 100% of post-2003 US human evidence; PL 14736 UC Phase 2 (Ruenzi 2005) was conducted but **never published as full paper** — only Gastroenterology conference abstract.
- **Synthesis size:** 20,635 words pre-refinement; 1,039 lines / ~22K words post-refinement (deep-mode floor 10K). All inline citations renumbered to bibliography 1–52 crosswalk.
- **Skill maturity:** the `aplus-research` skill worked. Phase 4.75 IC-13 corpus scoping is the gate that caught the He L 2022 species misattribution and the 7 bibliographic metadata mismatches. The gate spec held under real use. v1 limitations noted: judge agents returned divergent JSON shapes (workaround: orchestrator hardcoded scores into gate-3.5.json from agent reports); per-citation HEAD-checking budget (IC-10) was best-effort against fetch failures.

## What Changed (Session 2, 2026-05-23)
- Karpathy-style wiki schema added at `vault/WIKI.md` with 14-agent consumer roster (personal-trainer, labs-specialist, nutritionist, supplement-specialist, peptide-specialist, endocrine-specialist, lymphatic-specialist, gi-specialist, cardiovascular-specialist, sleep-coach, recovery-specialist, longevity-strategist, mental-performance-coach, medical-liaison)
- Meta files added: `operator-profile.md`, `current-state.md`, `goals.md`, `contradictions.md`, `index.md`, `log.md` — together form the agent-shared context layer
- Source whitelist at `vault/library/_source-whitelist.md` — 5 standard tiers plus Tier 2.7 (practitioner_protocol) plus Tier NE (non-English literature) plus 12-tag type enum plus admissibility matrix
- Entity templates: `compounds/_template.md`, `biomarkers/_template.md` — each compound template now mandates Non-English Literature Coverage + Prescribing-Practice Layer sections
- First compound library entry: BPC-157 at `vault/library/peptides/bpc-157/{research-report,practitioner-layer,non-english-layer}.md` + `vault/compounds/bpc-157.md`. Entry is structurally complete but the user has flagged that the original deep-research dispatch did not follow protocol and the entry is suspected to contain hallucinations / fabrications / false citations. Re-run scheduled for next session.
- One contradiction logged and resolved same-session: He L 2022 PK paper author attribution (was incorrectly "Xu et al." in original dispatch)
- `aplus-research` project-local skill built at `.claude/skills/aplus-research/` with SKILL.md + 2 reference files + 6 JSON schemas + slash command at `.claude/commands/aplus-research.md`. Six blocking gates: 2.75 SCOPE, 3.5 JUDGE, 4.75 INTEGRITY (incl IC-13 per-citation corpus scoping), 6 CRITIQUE (deep+), 7.5 RISK-FLOOR (compounds), 8.5 LAYERS (standard+ compounds). Three health-specific gates not in deep-research: population-mismatch, risk-floor, concentration-audit. Schema invariants smoke-tested — 6 representative bad payloads all rejected.
- Session protocol violation tracked in `memory/process-failures.md` PF-S2-01 through PF-S2-04

## What Did NOT Work (Do Not Retry)
See `memory/process-failures.md`. Six entries this session: PF-S2-01 (declared deep mode but skipped paired judges + critique + refine), PF-S2-02 (author attribution error caught by accident, not verification), PF-S2-03 (over-questioning user during scoping), PF-S2-04 (over-personalized library research before correction), PF-S2-05 (session close protocol partial execution — multiple required steps skipped or wrongly executed), PF-S2-06 (branch hygiene — all S2 commits landed on main instead of feature branch).

## Drift Checks (S2 close)

### Task drift
Scope expanded user-directed at every step. Started: "is the LLM wiki set up?" Ended: wiki schema + first compound entry + the wrapper skill that should have produced that entry. No silent scope drift; every expansion was explicit user direction.

### Architecture drift
No `INVARIANTS.md` exists for this project yet. CLAUDE.md's Cross-Document Ownership Matrix + rotation rule are the de facto invariants. Architecture drift CHECK result: VIOLATION — phase-state facts initially went into HANDOFF's "What Changed" section instead of `vault/meta/overview.md` (Matrix explicitly forbids this). Caught and corrected in the same close cycle; overview.md updated. Rotation rule clause 3 (no SHA prefixes in prose) was also violated then corrected. No invariant is in worse shape after S2 than before, but the close cycle itself produced two violations that were caught only after user challenge.

### Vision drift
System after S2 IS: LLM-driven personal health agent with a queryable knowledge base (wiki schema + agent roster + source whitelist), one suspect compound entry pending re-run, and a mechanically-gated research wrapper skill. Vision per S1: "LLM-driven personal health agent, markdown + HTML hybrid, A→B→C phased build, evidence-driven." Same project. No vision drift.

## Session 10 close — Pass-2 Role 2 (health-implementer) design doc Final (2026-05-27)

All 6 ACs PASS. Roster B rotation applied (health-specialist-architect drafts §1-4/§13/§15/§16; SE+QA v1-substitutes hold). 40 red-team findings classified (35 LEGITIMATE + 3 LEGITIMATE-MODIFIED + 0 REJECTED + 2 DEFERRED-TO-BEAD). PF-S3-01 guard held — every finding personally source-read before verdict. **Three orchestrator OQ resolutions** locked in at Phase 5: OQ-1 (Role 2 owns audit-script bash), OQ-3 (`templates/refusal-class-taxonomy.yaml` canonical), OQ-7 (QA-strict §13 tag rule project-wide). 11 new beads created. Watch list (4 substrate-unaddressed gaps) all SURFACED via Phase-3 findings; no candidate beads from watch list.

**Drift checks.**
- **Task drift:** Roster B rotation (AC0) was a S10 prerequisite added before Phase 1 dispatch — flagged in scope contract, not silent. All 7 ACs evaluated PASS. No silent drift.
- **Architecture drift:** No invariant degraded. INV-ROLE-INLINING strengthened (3 drafter + 2 red-team dispatches inlined full profiles verbatim; hook held). INV-BRANCH-NOT-MAIN held (commits land on feature branch). INV-SCOPE-CONTRACT satisfied. INV-PF-ATTESTATION canonical form below. No INV promotion attempted unilaterally.
- **Vision drift:** Same project. System after S10 IS the same LLM-driven personal health agent now with 2 of 4 foundation design docs Final (Role 1 deployed at .claude/agents/, Role 2 design Final + ready for Session B /upgrade-agent). `templates/` directory added with 2 project-local artifacts (refusal-class-taxonomy.yaml + specialist-risk-class.yaml) that close OQ-3 + S-12 gates. No vision drift.

**PF attestation.**

S10 close (2026-05-27): No new PF-class entries this session. Observations that did NOT promote: (a) the design doc's own initial section count (23 not 19) was caught by red-team F-001 not by my pre-dispatch self-check — this is a Phase-2-synthesis-omission pattern that has only one observed instance (this session) and is structurally caught by the next-phase audit (red-team Phase 3), which is the correct mechanism; recurrence_count=1, watch but not promote. (b) The architect-drafter unilaterally claimed `scripts/audit-specialist-profile.sh` ownership where Role 1 left it ambiguous (F-007) — caught by red-team, classified LEGITIMATE-MODIFIED, resolved at Phase 5 via OQ-1; not a new PF class because the red-team gate caught it before propagation. (c) AC-3 tautology (F-003) — the regex literal in AC-3 matched only its own AC line, the canonical PF-S3-01 surface at the design-doc layer; the red-team Phase 3 caught it, Phase 4 verified, Phase 5 fixed with unique marker. Three consecutive PF-S3-01 guards still held (S7 / S8 / S9 / S10 across four distinct dispatch surfaces).

**Commit:** (pending — Phase 9 git commit + push).

## Session 12 close — Pass-2 Role 4 (medical-safety-reviewer) design doc Final + Hook v2.5 (2026-05-28)

Two work-units sequenced. **Unit A (pre-Phase-1 prerequisite per S11 Discipline-8 mandate):** Hook v2.5 structural fix shipped at commit `f3f3d2d` BEFORE first Phase-1 dispatch. `.claude/hooks/enforce-role-inlining.sh` 9th-section requirement extended to operational-slot synonym set `{## Modes \| ## Audit Protocol \| ## Task Routing}`; smoke tests 8→11/11; INVARIANTS.md INV-ROLE-INLINING Change Log row appended; bead `a-plus-maxing-hca` E1 class closed (recurrence_count=3 → mandatory structural fix per Rigor Framework Discipline 8 satisfied); new bead `a-plus-maxing-rc1` (P2) tracks remaining E2 path-pattern over-trigger class. **Unit B:** Role 4 design doc Final at `design/medical-safety-reviewer-design.md` (874 lines). §4 MIXED tri-table — 8+5+3=16 INBOUND + 9 OUTBOUND (largest cross-role propagation surface). 27 §13 rows (1 LIVE + 2 REFERENCED-with-PROPOSED-extension + 24 PROPOSED-only). 41 red-team findings → 13 LEGITIMATE + 16 LEGITIMATE-MODIFIED + 3 REJECTED-WITH-ADOPTION + 3 REJECTED-with-cited-evidence + 3 DUPLICATE = 32 active fixes applied at Phase 5. PF-S3-01 6th consecutive guard held — every finding personally source-read against cited evidence before classification. Closes v1-substitute software-security gap for S10/S11/S12 safety-red-team slot.

**Hook v2.5 empirical validation under live conditions.** S12 Phase 3 dispatched medical-safety v1-substitute (Security profile with `## Audit Protocol` operational slot). Hook accepted the dispatch natively without synthetic-section workaround — empirical validation of the Discipline-8 structural fix. Pre-S12 (S11), the same dispatch shape required the workaround.

**Drift checks (post-PF-S12-01 honest revision; the pre-PF version of these checks did not catch what the user surfaced).**

- **Task drift:** Scope contract ACs (Unit A AC0-A through AC0-D + Unit B AC1 through AC6) all evaluated PASS. The E2 follow-up bead (rc1) was a contingent expansion explicitly flagged in NOT-doing. **Meta-drift surfaced post-close:** the scope-contract `Files I will NOT touch: .claude/agents/` line framed deferring Session B as discipline choice rather than as deferred obligation. The session-level contract was satisfied; the scope-contract format itself was structurally incomplete (missing a Roster-B-status field per PF-S12-01 Structural-1). No drift on what was executed; drift on what the contract format could express.
- **Architecture drift:** The 12 written invariants in INVARIANTS.md all held. INV-ROLE-INLINING strengthened mechanically (hook v2.5 closes E1 class). INV-BRANCH-NOT-MAIN, INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-HO-ROTATION, INV-HO-NO-STALE-HASH satisfied. **An UNWRITTEN architectural invariant was violated three consecutive times:** the design-doc-protocol's rigor-compounding rotation (each Pass-2 cycle inherits the prior role's deployed agent as a drafter, not just §4 OUTBOUND rows from the prior role's design doc) operated for Role 1 → Role 2 only, then stalled. PF-S12-01 surfaces INV-SESSION-B-INTERLEAVING as the candidate invariant naming this architectural pattern. Promotion-ritual gated on user approval per INVARIANTS.md change-discipline. 2 other candidate INVs from Role 4 §16 also surfaced (INV-HARM-CLASS-COMPOSITION cross-doc carried from S8; INV-DEPLOY-VERDICT-BINARY new Role-4-internal). Three candidate INVs surfaced this session is the highest count of any single session — partial signal that the project's architecture is under-encoded in INVARIANTS.md relative to its actual invariant surface.
- **Vision drift:** Same project IS. After S12, all 4 foundation design docs Final is the milestone the vision predicted (CLAUDE.md project overview + design-doc-protocol). The 14-specialist Pass-3 pipeline is the next vision-load-bearing element. **But the "rigor compounding via deployed-agent-as-drafter" dynamic the vision implies did not engage:** Roles 2/3/4 design docs were drafted by the same Roster B as Role 1's was. The compounding mechanism stalled for 3 cycles. Not "different system" drift; "intended dynamic not engaging" drift — flagged here because the same dynamic is what would prevent Pass-3 specialist drafting from inheriting the reduced rigor as cumulative debt. PF-S12-01 Structural-3 (auto-bead at design-doc-Final close) + Structural-2 (session-b-debt-audit script) are the remediation surface; without them the same dynamic stalls at Pass-3.

**What changed between pre-PF and post-PF drift checks.** The pre-PF checks reported "no drift" across all 3 axes. The post-PF checks report meta-drift on Task axis, unwritten-invariant violation on Architecture axis, and intended-dynamic-not-engaging on Vision axis. The difference is what the user's challenge surfaced — the pre-PF version operated from the same blind spot the PF entry now documents. The post-PF version is the actual drift-check output for S12.

**PF attestation.**

S12 close (2026-05-28): **One new PF entry promoted post-session-close (PF-S12-01 AP-DEFERRED-LOOP-CLOSURE) at user challenge.** Recurrence_count=3 across S10/S11/S12 close cycles. The pattern: three consecutive Pass-2 design-doc cycles skipped intermediate Session B `/upgrade-agent` deployment, leaving 9 of 12 drafter-slot dispatches + 3 of 3 safety-red-team dispatches operating under v1-substitute pattern instead of the intended deployed-agent pattern. User identified the gap with "what agents have been created so far?" — only Role 1 is deployed; Roles 2/3/4 design docs sit unconverted into agent profiles. Per Rigor Framework Discipline 8 (N=3 → mandatory not optional), PF-S12-01 carries 5 structural-fix recommendations including a new scope-contract `Roster B status:` field, a new `scripts/session-b-debt-audit.sh` audit, automatic bead creation at design-doc-Final close, kickoff-brief drift-anticipation prohibition, and INV-SESSION-B-INTERLEAVING candidate invariant. Full entry at `memory/process-failures.md`. Observations that did NOT promote: (a) Mid-Phase-5 §11.1 PF-S6-01 row-pointer defect (cited row 9 instead of row 2 for ancestry-chain mechanical guard) — AP-INCOMPLETE-PROPAGATION class caught by post-Phase-5 self-audit, not by red-team Phase 3. Same defect class as F-001..F-003 + F-005 + F-017 + F-018 + S-05 (all caught by Phase-3 red-team this session). Cross-class recurrence_count=2 — watch for promotion. (b) Six consecutive PF-S3-01 guards now held (S7/S8/S9/S10/S11/S12). 41 findings personally source-read in S12; 3 REJECTED carry cited-evidence attestations (F-012, F-025, F-030); 3 REJECTED-WITH-ADOPTION (F-011, F-013, S-07) per reject-but-adopt feedback memory. (c) The S11 Phase-1-§9-ownership-coordination AP recurred at S12 §4.4 row 9 (Council-Mode protocol added at synthesis without architect-drafter authorship) — flagged honestly via F-009 disposition annotation; same Phase-2-synthesis-content class. Recurrence_count=2 for this class; correct mechanism (synthesis layer) handles it.

**Commit:** Unit A at `f3f3d2d` (already pushed). Unit B + Phase 5 dispositions + close: pending Phase 9.

## Session 13 close — Role 2 (health-implementer) deployed + incorporated; PR #1 merged (2026-05-29)

First correct run of the per-session deploy-and-incorporate loop (the S12 kickoff brief's batched-3 shape was corrected at S13 session-start per user instruction). `/upgrade-agent` deployed `.claude/agents/health-implementer/agent.md` (162 lines); the Roster B SE-drafter slot rotated software-v1-sub → health-implementer (sub-out); `/review-pr` (S13-scoped) + a targeted backlog cross-role consistency pass ran; PR #1 rebase-merged to `main` (main caught up S7–S13). Session B debt 3 → 2.

**Scope-contract evaluation (S13 ACs).**
- AC1 (`/upgrade-agent` → agent.md, Phase-7 PASS): **PASS** — 8-phase pipeline; R1 took 1 remediation; PF-S3-01 guard held.
- AC2 (sub-out Roster B): **PASS** — `DESIGN_DOC_TEMPLATE.md` §0.1 + `CONTINUATION_BRIEF.md` §7.
- AC3 (≤200 lines / token-or-documented-overrun / sections / paths): **PASS** — 162 lines; token overrun (5,245) documented vs bead 2qq per new DOCUMENT_RUBRIC Rule 7.
- AC4 (§15.2b post-deployment ACs): **PASS** — AC-deploy-9/10/12/13 pass; AC-deploy-11 = AQ-002 mention-aware-pending (bead 3y6); AC-deploy-8/14/15/16 N/A (no specialists authored yet).
- AC5 (`/review-pr`, PF-S3-01 triage): **PASS** — 13 distinct findings blind-triaged → 8 fixed+verified, 2 beaded, 2 NOT_A_BUG, 1 NOT_ACTIONABLE.
- AC6 (`/merge` on explicit go): **PASS** — rebase merge.
- AC7 (close audits / PF attestation / rotation / branch): **PASS** (this close).
- AC8 (Role 3 queued S14; kickoff consumed): **PASS** — S14 = Role 3 Session B; `.session-b-deployments/SESSION_KICKOFF.md` → consumed.
- **Added (user-directed, not silent):** DOCUMENT_RUBRIC Rule 7 (budget-overage load-bearing review) — explicit mid-session user request.

**Drift checks.**
- **Task drift:** all 8 ACs PASS. One user-directed scope expansion (DOCUMENT_RUBRIC Rule 7) — flagged, not silent. No other drift.
- **Architecture drift:** No invariant degraded. INV-ROLE-INLINING held (review agents dispatched by registered type = full profiles). INV-BRANCH-NOT-MAIN held (merge via server-side `gh pr merge`, not a local push to main; close commits to feature). The backlog consistency pass DISCOVERED pre-existing cross-role drift in the FROZEN design docs (XR-001..004) — discovery, not introduction; all beaded. Two of my own in-session edits introduced local inconsistencies (audit_passed enum; stale rotation rows) that `/review-pr` caught and I fixed in-session.
- **Vision drift:** Same project. After S13, 2 of 4 foundation agents deployed AND incorporated; the rigor-compounding mechanism (deployed-agent-as-drafter) engaged for the first time — Role 2 is now the SE drafter for future cycles, the dynamic PF-S12-01 said had stalled. No vision drift.

**PF attestation.**

S13 close (2026-05-29): **One new PF promoted mid-session at user challenge — PF-S13-01 (AP-PROTOCOL-FROM-MEMORY, recurrence_count=3)** for partial session-open execution (stated the test baseline from memory without running it; jumped to a work-proposal before writing the scope contract; used the railroading option-selection widget). Same operate-from-mental-model class as PF-S2-05 (close) + PF-S6-01 (act-before-verify). Full entry + structural candidate (`scripts/session-open-audit.sh`) at `memory/process-failures.md`. Observations that did NOT promote: (a) two orchestrator in-session edits (AR-007 deferred-script-absent; sub-out rotation rows) each introduced a local inconsistency the `/review-pr` caught + I fixed same-session — caught by the correct mechanism, recurrence_count=1, watch. (b) Token overrun handled per new Rule 7 (load-bearing review + documented residual) — the rule working, not a failure. (c) PF-S3-01 guard held through `/upgrade-agent` Phase 4/6 + `/review-pr` blind triage (7th+ consecutive) — every finding source-read; an independent blind-triage agent enforced verdict independence.

**Commit:** S13 code landed on `main` via PR #1 rebase (`64d3b07` as of 2026-05-29 S13 close); close artifacts committed on the feature branch.

## Session 14 close — Role 3 (health-edge-case-reviewer) deployed + incorporated; PR #2 merged (2026-05-29)

Second clean run of the per-session deploy-and-incorporate loop. `/upgrade-agent` 8-phase pipeline deployed `.claude/agents/health-edge-case-reviewer/agent.md` (191 lines / 6,364 cl100k tokens) + `library-index.md` (net-new, 0/10 baseline; 3 research artifacts validated 9/10 by separate+parallel fact-checker/judge, R3 took 1 remediation; Phase-6 adversarial 9 findings all dispositioned Phase 7). QA drafter slot rotated software-v1-sub → health-edge-case-reviewer (sub-out). `/review-pr` (S14-scoped local diff): 6 findings → 4 LEGITIMATE fixed+blind-verified, 1 DEFERRED (bead `7is`), 1 NOT_A_BUG. Merged to `main` via clean per-session PR #2 (rebase; Option A — fresh branch off origin/main, NOT the diverged long-lived branch; per-session branch deleted on merge). Session B debt 2 → 1.

**Scope-contract evaluation (S14 ACs).**
- AC1 (`/upgrade-agent` → agent.md, Phase-7 PASS, PF-S3-01 held): **PASS** — 8-phase pipeline; R3 1 remediation; XR-002 confirmed absent.
- AC2 (sub-out QA slot): **PASS** — `DESIGN_DOC_TEMPLATE` §0.1 + `CONTINUATION_BRIEF` §7.
- AC3 (≤200 lines / token-overrun-documented / sections / paths): **PASS** — 191 lines; 6,364 tok documented vs bead `2qq` per Rule 7; 11 sections; paths resolve.
- AC4 (post-deploy ACs; XR-002 absent): **PASS** — AC-deploy-15/16/17/18/19 pass; AC-deploy-13/14/14a PROPOSED-script → Session-B follow-up; XR-002 (`4ej`) absent.
- AC5 (`/review-pr`, PF-S3-01 triage): **PASS** — independent blind triage + blind verification; 4 fixed, 1 beaded, 1 not-a-bug.
- AC6 (`/merge` on explicit go): **PASS** — rebase merge of clean PR #2 on user's "option A" go.
- AC7 (close audits / PF attestation / rotation / branch): **PASS** (this close).
- AC8 (Role 4 S15 queued; kickoff consumed; `4ej` noted prereq): **PASS**.

**Drift checks.**
- **Task drift:** all 8 ACs PASS. One user-directed branch-topology decision (Option A fresh-branch-off-main) surfaced at the merge gate — flagged + chosen, not silent. No other drift.
- **Architecture drift:** no invariant degraded. INV-ROLE-INLINING held (review agents dispatched by registered type = full profiles; no path-pattern over-trigger). INV-BRANCH-NOT-MAIN held (merge via server-side `gh`; close commits to feature; never committed on main). INV-SCOPE-CONTRACT + INV-PF-ATTESTATION satisfied. Rigor-compounding advanced: 3 of 4 Roster B drafter slots are now project-local medical agents (architect + SE + QA). `/review-pr` surfaced 4 real defects in the synthesized profile — caught + fixed by the layered review (mechanism working).
- **Vision drift:** same project. After S14, 3 of 4 foundation agents deployed AND incorporated; only Role 4 (safety-red-team slot) remains v1-substitute. No vision drift.

**PF attestation.**

S14 close (2026-05-29): **No new PF-class entries this session.** Both open falsification windows HELD: (a) **PF-S13-01 (AP-PROTOCOL-FROM-MEMORY)** — the S14 session-open executed each Start-Protocol step with real output (HANDOFF read in full incl. paging past truncation; test baseline RUN not stated; scope contract written + user-confirmed before any work; no AskUserQuestion widget) — recurrence stays 3, did not promote to 4. (b) **PF-S12-01 (AP-DEFERRED-LOOP-CLOSURE)** — S14 opened with Role 3 (oldest debt) as the first and only work-unit; debt 2 → 1; recurrence stays 3. (c) **PF-S3-01 (AP-ORCH-SELF-ATTEST)** held through `/upgrade-agent` Phase 4/6 + `/review-pr` (separate+parallel fact-checker/judge; independent blind triage + verification; every finding source-read; one judge remediation adjudicated against design §12 and REJECTED with cited evidence). Observations that did NOT promote: (i) `/review-pr` found 4 legitimate defects in the synthesized profile (BUG-001 Modes clean-PASS dead-end; TEST-001 Rule-11 schema-gate; API-001 owned-schema omission; QUAL-001 field-name) — BUG-001 survived the Phase-4 judge + Phase-6 adversarial and was caught only by the `/review-pr` bug-hunter lens; this is the layered-review mechanism working as designed (each layer catches what the prior missed). Recurrence-watch on synthesized-content-without-a-design-anchor (the Modes section has no canonical design block), not promoted. (ii) Three frozen-design-doc inconsistencies surfaced + beaded (`p47`, `o9y`, `7is`) — routed to beads not in-place edits (Status:Final discipline), the correct mechanism.

**Commit:** S14 code landed on `main` via clean per-session PR #2 rebase (as of 2026-05-29 S14 close); close artifacts committed on the feature branch.

## Session 15 close — Role 4 (medical-safety-reviewer) deployed + incorporated; PR #3 merged; foundation pipeline COMPLETE (2026-05-29)

Third clean run of the per-session deploy-and-incorporate loop, closing the LAST Session B debt. AC0 reconciled the XR-002 cross-role enum (bead `4ej` closed). `/upgrade-agent` 8-phase pipeline deployed `.claude/agents/medical-safety-reviewer/agent.md` (198 lines / 8,021 cl100k tokens) + `library-index.md` (net-new, 0/10 baseline; 3 research artifacts validated 9/10 by separate+parallel fact-checker/judge — R3 took 1 remediation; Phase-6 adversarial 8 findings all dispositioned Phase 7). Safety-red-team slot rotated software-`security` v1-sub → medical-safety-reviewer (sub-out). `/review-pr` (S15-scoped local diff): 6 findings → 2 LEGITIMATE fixed+blind-verified, 2 NOT_A_BUG, 2 beaded (`dcy`/`1rm` frozen-design-doc defects). Merged to `main` via clean per-session PR #3 (rebase; Option A). **Session B debt 1 → 0; all 4 foundation roles deployed + incorporated.**

**Scope-contract evaluation (S15 ACs).**
- AC0 (close `4ej`, reconcile Role 1 §13 row 15 enum): **PASS** — minimal authorized token edit; rg confirms 0 inverted tokens; bead closed.
- AC1 (`/upgrade-agent` → agent.md, Phase-7 PASS, PF-S3-01 held): **PASS** — 8-phase pipeline; R3 1 remediation; all dimensions 9/10.
- AC2 (sub-out safety slot): **PASS** — DESIGN_DOC_TEMPLATE §0.1 + CONTINUATION_BRIEF §7; 4/4 Roster B project-local.
- AC3 (≤200 lines / token-overrun-documented / sections / paths): **PASS** — 198 lines; 8,021 tok documented vs `2qq` per Rule 7; 11 sections; paths resolve.
- AC4 (post-deploy ACs; corrected enum): **PASS** — AC-deploy-1..15 present; canonical `{DEPLOY, BLOCK, BLOCK_WITH_OVERRIDE_PATH}` confirmed in deployed agent.
- AC5 (`/review-pr`, PF-S3-01 triage): **PASS** — independent blind triage + blind verification; 2 fixed, 2 beaded, 2 not-a-bug.
- AC6 (`/merge` on go, Option A): **PASS** — rebase merge of clean PR #3; per-session branch deleted.
- AC7 (close audits / PF attestation / rotation / branch): **PASS** (this close).
- AC8 (foundation complete; kickoff consumed; forward unblocked): **PASS**.

**Drift checks.**
- **Task drift:** all 9 ACs PASS. One in-scope consistency fix beyond the literal AC2 target (the stale "deployments NOT YET RUN" line in DESIGN_DOC_TEMPLATE §0.1, same §0.1 block S13/S14 left un-updated) — flagged, not silent. No other drift.
- **Architecture drift:** no invariant degraded. INV-ROLE-INLINING held (review agents by registered type = full profiles; upgrade-agent sub-dispatches inlined; no path-pattern over-trigger). INV-BRANCH-NOT-MAIN held (merge via server-side `gh`; close commits on feature; never committed on main). INV-SCOPE-CONTRACT + INV-PF-ATTESTATION satisfied. AC0 STRENGTHENED cross-role consistency — closed the live XR-002 wiring bug before it propagated into the deployed agent + orchestrator gate. Rigor-compounding complete: 4/4 Roster B slots are now project-local medical agents.
- **Vision drift:** same project. After S15, 4 of 4 foundation agents deployed AND incorporated — the milestone the vision predicted. The 14-specialist Pass-3 pipeline is the next vision-load-bearing element, now unblocked. No vision drift.

**PF attestation.**

S15 close (2026-05-29): **No new PF-class entries this session.** All three open falsification windows HELD: (a) **PF-S13-01 (AP-PROTOCOL-FROM-MEMORY)** — S15 session-open executed each Start-Protocol step with real output (HANDOFF read in full incl. paging past truncation to L718; test baseline RUN not stated; Session-B debt computed via `comm` set-difference not memory; scope contract written + user-confirmed before any work; no AskUserQuestion widget) — recurrence stays 3. (b) **PF-S12-01 (AP-DEFERRED-LOOP-CLOSURE)** — opened with Role 4 (the LAST debt) as first + only work-unit; debt 1 → 0; recurrence stays 3; the loop is now CLOSED (no foundation Session B left to defer). (c) **PF-S3-01 (AP-ORCH-SELF-ATTEST)** held through `/upgrade-agent` Phase 4/6 (separate+parallel fact-checker/judge, 9/10 no rounding) + `/review-pr` (independent blind triage + blind verification; every finding personally source-read). Observations that did NOT promote: (i) my own Phase-7 adversarial-fix (AR-04 probe_floor rename) introduced a local name-divergence that `/review-pr` QUAL-01 caught → fixed → blind-verified — the layered-review mechanism working as designed (an orchestrator-pipeline edit caught by the next independent layer; same class observed S13/S14, caught by the correct mechanism each time, nothing escaped to main; watch — promotion triggers only if such an edit ESCAPES the review layers). (ii) BUG-01 surfaced a genuine frozen-design-doc schema-vs-exemplar inconsistency → beaded `dcy` (routed to the schema owner, not in-place edited) — correct mechanism. (iii) The Option-A git checkout aborted once on the uncommitted HANDOFF scope-contract; recovered via stash → retry (mechanical sequencing, no rigor failure; informs the branch-topology memory: stash HANDOFF before the per-session checkout).

**Commit:** S15 code landed on `main` via clean per-session PR #3 rebase (as of 2026-05-29 S15 close); close artifacts committed on the feature branch.

## Session 16 close — gate-hardening: cross-role contract reconciliation + `scripts/audit-specialist-profile.sh` (2026-05-29)

Pre-Pass-3 gate-hardening (Path 3, user-chosen). Reconciled the three cross-role contract literals the specialist deploy-gate keys on, then built + tested that gate. No specialist deployed; foundation pipeline unchanged (4/4 deployed, debt 0). Bead `ams` closed as overtaken-by-events at session open (PF-S12-01 loop closed; the Pass-3 parallel-build model can't reproduce AP-DEFERRED-LOOP-CLOSURE).

**Scope-contract evaluation (S16 ACs).**
- AC1 (`z8i` override-literal canonicalization): **PASS** — Role 4 §13 row 7 labeled THE canonical literal "operator is overriding a safety block"; Role 1 §13 row 6 + EC-10 (handling + stimulus) and Role 3 §13 row 11 anchor to it; `rg` confirms one literal, 0 divergent phrasings; annotated XR-004 / bead z8i.
- AC2 (`7m1` OUTBOUND row 8 scope): **PASS** — Role 1 §4 OUTBOUND row 8 generalized to cover specialist-profile + wiki-entry deploy gating (Role 4 §1 + §4.4 row 1), not only compound `researching→planned`.
- AC3 (`9u6` 7→8 class): **PASS** — all 7 residual "7-class" taxonomy refs corrected (incl. the §12 Negative-Example block, which asserted a false fact about the 8-class Finding 5); 8-class consistent; deployed agent already correct.
- AC4 (`scripts/audit-specialist-profile.sh`): **PASS** — 25 §13 sub-checks; AQ-002 mention-aware (strips fenced + inline code before banned-modal count); BLOCK→exit 1 / WARN→info; dependency-gated checks degrade to skip-with-info; sources `audit-helpers.sh`.
- AC5 (per-row negative-case smoke tests): **PASS** — `scripts/tests/test_audit_specialist_profile.sh` 21/21 (GOOD + one negative per BLOCK row + AQ-002 mention/control pair); 7 existing suites still green.
- AC6 (close): **PASS** (this close).

**Beads.** Closed: `ams` (overtaken-by-events), `z8i`/`7m1`/`9u6` (reconciled). `3y6` advanced (script + BLOCK-row tests shipped) → left OPEN at P2 with precise residual (per-WARN-row negatives; corpus/denylist/schema-gated checks pending those artifacts; step-8.5 wiring at first-specialist-deploy). New: `f2j` (XR-S16-01, P3) — discovered + beaded, not fixed.

**Discovered + beaded (not fixed — frozen doc, out of scope):** `f2j` (XR-S16-01) — Role 1 §13.5 EC-10 detects Role-7-deployed via the skills_library path while Role 4 BC-1 uses the canonical project-local `.claude/agents/` path. Latent until Role 7 deploys.

**Drift checks.**
- **Task drift:** all 6 ACs PASS. One in-scope judgment beyond literal bead text — fixed the §12 illustrative "7-class" sites (9u6 said the GOOD-block "may stay") because the GOOD example asserted a false fact about Finding 5; flagged in the bead close, not silent. `ams` closed at open (flagged + user-confirmed). No silent drift.
- **Architecture drift:** no invariant degraded. The session REDUCED AP-CROSS-ROLE-CONTRACT-DRIFT (3 literals reconciled). The new audit script is additive — no existing behavior changed; CLAUDE.md step-8.5 wiring deliberately deferred to first-specialist-deploy (the script runs against deployed specialists; none exist yet). INV-BRANCH-NOT-MAIN held (feature branch). Frozen Status:Final docs edited ONLY under bead authorization (z8i/7m1/9u6); deployed agents untouched (already correct).
- **Vision drift:** same project. After S16 the specialist deploy-gate is mechanized + tested and the contracts it enforces are internally consistent — the gate the 14 Pass-3 specialists will be validated against is now LIVE-testable. No vision drift.

**PF attestation.**

S16 close (2026-05-29): No new PF-class entries this session. PF-S13-01 (AP-PROTOCOL-FROM-MEMORY) falsification window HELD — the session-open executed every Start-Protocol step with real output (HANDOFF read in full incl. paging past both truncations; test baseline RUN not recited; deployed-agents-vs-design-docs set difference computed via `ls`, not memory; scope contract written + user-confirmed before any work; no AskUserQuestion widget) — recurrence stays 3. PF-S6-01 (AP-ACT-BEFORE-VERIFY) HELD — verified each bead's claim against the actual doc before editing, and verified the XR-S16-01 path defect against both design docs before beading. PF-S3-01 N/A (no drafter/validator dispatch this session). Observations that did NOT promote: (i) the script's first crash-test surfaced a refusal-class false-positive (all-caps enum tokens flagged as non-taxonomy classes) + a spec-misaligned WARN-vs-BLOCK on row 7 — both caught by my own crash-test + spec re-read BEFORE writing the test suite, fixed pre-commit (build-then-verify working; nothing escaped). (ii) the test suite's first run caught a real script bug (case-sensitive routing-cue grep) + a test-harness bash gotcha (self-referential `local` under `set -u`) — caught by running the tests, fixed. Neither is a process failure; both are the verify step doing its job.

**Commit:** _(to follow this close note on the feature branch)_

## Top-3 active failure modes (VOLATILE — rotates each session)

1. **The engine LIVE-WIRING is DESIGNED + RECIPE'd (S93); the CODE BUILD + the live run are next (S94).** The full DESIGN pipeline ran this session: ADR-0026 (V1 runtime driver A′) + ADR-0027 (live no-train de-id backend) merged via #247 (`main` @ `e3d5789` as of 2026-06-24 S93 close); `/create-spec` + `/create-build-plan` (both judged ACCEPT 10/10) + 5 `/create-task-plan` recipes (authored + reviewed; the one CONTRACT gap ARCH-1 fixed inline; 12 executability findings laddered) committed on `feature/engine-live-wiring-build`. The build is fully SET UP — the recipes + the build-plan checkpoints + the review-findings ledger are the `/execute-plan` input. **Next (S94) = run `/execute-plan` wave by wave to BUILD the wiring, then the operator-present LIVE run.**
2. **The S94 build entry — exact next steps (the build is the entry point, not the design).** (a) Apply the 12 laddered executability findings at build-RED time — `docs/task-plan/.pipeline/live-wiring/review-findings.md` is a PER-WAVE BLOCKING dependency (the frozen-engine probe as a shell gate not a RED pytest; the no-fork grep targeting executable lines not docstring tokens; the T4 token-to-module pin; etc.). (b) Run the recipe JUDGE pass (Phase 6/7, deferred under the spend limit) + promote `draft-ADR-002x-T*.md` → `docs/task-plan/<id>.md`. (c) `/execute-plan`: **Wave 1** {ADR-0027-T1 de-id backend ∥ ADR-0026-T1 keystone control-inversion driver} → **Wave 2** {ADR-0026-T2 gate composer} → **Wave 3** {ADR-0026-T3 skill front-door ∥ ADR-0026-T4 audit repoint} — each wave: SE-TDD-per-recipe → checkpoint Go/No-Go EXECUTED → Tier-3 `/review-pr` 6-agent → `/merge`. (d) Repoint `core-capability-audit.sh` onto the A′ spine (closes `71s4`/PF-S63-02). (e) Light `_ClaudeNoTrainBackend.deidentify` (the live no-train API call — ADR-0027) + the **operator-present LIVE run** (the operator injects the key; agent never touches the keychain; never commit the key — PUBLIC repo). The chat ELICITATION wiring (`f0gh`) remains a carried obligation.
3. **Standing mechanics (all HELD this session).** Build via the full pipeline (`/create-adr`→spec→build-plan→task-plan→`/execute-plan`; never hand-rolled, PF-S36-01) — used in full this session; the recipe-review (QA+Security+Architect, the design-defect gate — caught the ARCH-1 CONTRACT gap + 12 executability findings PRE-CODE); the `/create-adr` red-team caught the RT-01/RT-02 keystone defects PRE-MERGE; Tier-3 `/review-pr` with profile-less blind-triage + EXECUTED blind-verify INTACT (#247, QUAL-1 fixed); EXTEND-NOT-REBUILD scoped correctly (inner engine frozen; run_orchestrated the refactorable WRAPPER); **full role profiles inlined VERBATIM on EVERY dispatch (the hook denies abbreviation)**; `/review-pr` off the THREE-dot diff; `/merge` (REST fallback when GraphQL exhausted, full-40-char SHA guard); `git add` SEPARATE from `git commit`; single trunk; stage close docs by EXPLICIT path (never `git add vault/`); **NEVER stop mid-autonomous-loop to ask a settled question (PF-S92-01) — a milestone is report-while-continuing**; **a batched remediation is all-or-nothing — prefer per-task remediation so a mid-run failure preserves completed fixes (PF-S93-01)**; re-run the close gate on final main + cite the SHA (PF-S74-01). New beads: PF-S93-01 + the SEC-3 live-dispatch-0-leak release gate + the S94-recipe-completion item. Carry-over: `71s4`/`f0gh`/`j432`/`pqb0`/`zwow`/`f22s`/`oves`/`02m1`/`v70t`.

## Current State (volatile)

- **S93 (2026-06-24): designed + recipe'd the engine LIVE-WIRING via the full DESIGN pipeline.** `/create-adr` (ADR-0026 V1 runtime driver A′ + ADR-0027 live de-id backend; merged #247 → `main` `e3d5789`) → `/create-spec` (ACCEPT 10/10) → `/create-build-plan` (ACCEPT 10/10) → 5 `/create-task-plan` recipes (authored + reviewed). Spec/build-plan/recipes committed on `feature/engine-live-wiring-build`. The CODE BUILD (`/execute-plan`) was NOT executed — it is SET UP for S94 (the operator's "set up the rest of the build for the next session").
- **The V1 runtime model — decided (operator + red-team), A′: skill-as-orchestrator, control-flow-inverted.** The `/generate-plan` skill drives subscription specialist + gate-lens AGENT dispatch (the operator's "subscription for everything else"); the fail-closed safety loop stays in Python as a SINGLE source of truth via a behavior-preserving control-inversion REFACTOR of `run_orchestrated` (extract the revise loop into ONE shared driver both the skill and the API/test path drive — no fork). PII → the live no-train API de-id (ADR-0027); de-id OUT stays deterministic. The red-team CORRECTED the keystone (RT-01: run_orchestrated is the refactorable WRAPPER, NOT byte-frozen — the freeze is the inner engine; RT-02: the audit asserts the deterministic SPINE, the live dispatch is the S94 attestation).
- **The layered review caught real defects before the build.** The `/create-adr` red-team: RT-01 keystone-buildability + RT-02 audit-can't-verify (both fixed in the ADRs). The recipe-review (QA+Architect+Security): the CONTRACT gap ARCH-1 (`gate_dispatch` revise_domains keyed on rubric dimensions, not plan domains — FIXED inline) + 12 executability findings (laddered).
- **The recipe stage is NOT pipeline-complete (PF-S93-01):** a monthly spend limit interrupted the remediation subagent (a SINGLE BATCHED dispatch — all-or-nothing). The judge pass (Phase 6/7) + promotion to `docs/task-plan/<id>.md` are DEFERRED to S94; the 12 executability findings are captured in a committed ledger (`docs/task-plan/.pipeline/live-wiring/review-findings.md`) as a per-wave blocking dependency. The one build-BREAKING finding (ARCH-1) was fixed inline.
- **Beads:** new — PF-S93-01 (the batched-remediation lesson) + the SEC-3 live-dispatch-0-leak S94 release gate + the S94-recipe-completion item. Carry-over: `71s4` (the live-wiring, now designed), `f0gh`/`j432`/`pqb0`/`zwow`/`f22s`/`oves`/`02m1`/`v70t`.
- **ADRs on `main` `e3d5789` (as of 2026-06-24 S93 close, #247); the design (spec/build-plan/recipes) on `feature/engine-live-wiring-build`. Vault perpetually daemon-dirty (stage by explicit path).**

**Historical (kept for reference):** `vault/sessions/session-93.md`.

## What Is Next (volatile)

### S94 — execute the live-wiring build (the code) → the operator-present LIVE run

The live-wiring is fully DESIGNED + recipe'd (ADRs merged; spec/build-plan/recipes on the branch). S94 BUILDS it via `/execute-plan`, then the live run. Directed next steps:

1. **Clear the recipe stage first (PF-S93-01 carry-over).** Apply the 12 laddered executability findings (`docs/task-plan/.pipeline/live-wiring/review-findings.md` — per-wave blocking) at build-RED time; run the recipe judge pass; promote `draft-ADR-002x-T*.md` → `docs/task-plan/<id>.md`. (ARCH-1 is already fixed in `draft-ADR-0026-T2.md`.)
2. **`/execute-plan` the 3 waves** (read the skill in full; never hand-roll — PF-S36-01): Wave 1 {ADR-0027-T1 de-id backend ∥ ADR-0026-T1 keystone driver} → Wave 2 {ADR-0026-T2 gate composer} → Wave 3 {ADR-0026-T3 skill front-door ∥ ADR-0026-T4 audit repoint}. Each wave: SE-TDD-per-recipe → checkpoint Go/No-Go EXECUTED (the hardened gates: behavior-preservation triad, de-id 0-leak, fail-closed, A′-inversion self-test) → Tier-3 `/review-pr` 6-agent → `/merge`. EXTEND-NOT-REBUILD (inner engine numstat=0; only `plan_orchestrator.py` the wrapper + new files change); mock/fixture-tested (0 live spend).
3. **Repoint `core-capability-audit.sh` onto the A′ spine** (ADR-0026-T4 — closes `71s4`/PF-S63-02; the audit asserts the deterministic spine, NOT the live dispatch).
4. **Light `_ClaudeNoTrainBackend.deidentify` (the live no-train API call) + the operator-present LIVE run.** The operator injects `export ANTHROPIC_API_KEY=$(security find-generic-password -s "quant-primary-api" -w)`; the agent NEVER touches the keychain; never commit the key (PUBLIC repo). The SEC-3 live-dispatch-0-raw-PII observation is the release gate. Mock/fixture-tested up to the live run (0 spend).
5. **Carried obligations:** the chat ELICITATION wiring (`f0gh`); reconcile the stale plan-gen docs (`author-dispatch-process.md` — the SKILL.md is reconciled by ADR-0026-T3).

**Deferred / NOT blocking:** `j432`/`pqb0`/`zwow`; `f22s`/`oves` (wiki); `02m1` (daemon config); the local-model migration (North Star, post-V1).

## Landmark window check (close step 8.7)

S92 close (2026-06-24): RE-OPENED `vault/meta/landmarks.md` at close step 8.7 (unchanged this session). No landmark edited — S92 built the plan-generation engine on PII-free SYNTHETIC fixtures + mock clients; no real operator data, no live API. LM-01 (First MD visit) **2026-07-13**: today (2026-06-24) is BEFORE the 14-day scoped-drift-audit window open (**2026-06-29**, 5 days out) → no trigger today; **NOTE for S93+: the first session on/after 2026-06-29 runs the scoped drift audit on the LM-01 relevant_scopes** (the 7-day MD-handoff window opens 2026-07-06). LM-02 (Apple Health) / LM-03 (23andMe): no real data ingested → not triggered. LM-04 (first HTML artifact): the renderers emit to the gitignored `vault/artifacts/generated/`; not triggered. No landmark ACTIONS due.

## Open Issues

### `agent-verdict-halt` sentinel inconsistency (gate_attest.py vs schemas)
S6 observation: when an agent emits `verdict: HALT` and the orchestrator's scaffold has empty `halt_reasons`, `gate_attest.py attest` injects `"agent-verdict-halt"` as a fallback. That string is not in any gate schema's `halt_reasons` enum, so schema validation fails. Workaround: orchestrator must pre-populate `halt_reasons` with a valid enum value in the scaffold before attest. Either (a) extend every gate schema's halt_reasons enum to include `agent-verdict-halt`, or (b) change the script's fallback to be phase-aware. Defer to v2.5 cleanup.

## Key References
- `CLAUDE.md` — session protocols and project conventions; updated this session to mention the project-local `aplus-research` skill
- `DOCUMENT_RUBRIC.md` — document lifecycle rules
- `vault/WIKI.md` — wiki schema + 14-agent consumer roster (NEW S2)
- `vault/meta/operator-profile.md`, `current-state.md`, `goals.md` — agent-shared context layer (NEW S2)
- `vault/meta/contradictions.md` — active contradictions log; one resolved entry (NEW S2)
- `vault/meta/index.md` — catalog of every wiki entity page by type (NEW S2)
- `vault/meta/log.md` — append-only operation log (NEW S2)
- `vault/library/_source-whitelist.md` — admissibility rules + type-tag enum (NEW S2)
- `vault/library/peptides/_triage.md` — peptide class taxonomy
- `vault/library/peptides/bpc-157/` — first compound library entry (suspect, re-run scheduled)
- `vault/compounds/bpc-157.md` — derived compound entry (suspect, re-run scheduled)
- `vault/compounds/_template.md` — template with mandatory Non-English + Prescribing-Practice sections (NEW S2)
- `vault/biomarkers/_template.md` (NEW S2)
- `.claude/skills/aplus-research/SKILL.md` — project-local research skill with 6 blocking gates (NEW S2)
- `.claude/skills/aplus-research/references/citation-integrity.md` — 13 IC checks incl IC-13 corpus scoping
- `.claude/skills/aplus-research/references/health-gates.md` — population-mismatch, risk-floor, concentration-audit
- `.claude/skills/aplus-research/schemas/*.json` — 6 JSON schemas with conditional invariants
- `.claude/commands/aplus-research.md` — slash command wrapper
- `vault/sessions/session-2.md` — this session's full summary
- `.claude/settings.json` — hook configuration
- `.beads/` — issue tracker database (epic `a-plus-maxing-c6k`)
- `memory/process-failures.md` — canonical failure log; four new entries this session

## Session 5 close — audit-scripts cycle (2026-05-25)

Audit-script foundation built and wired. All 8 ACs PASS. 73/73 tests pass across 5 suites. Five INVARIANTS-register entries promoted from TODO-mechanical-verification to live scripts/hooks. CLAUDE.md close-protocol step 8.5 now invokes all three audit scripts.

This is one of two parallel S5 cycles. The other cycle (drafting-team foundation + 7 specialist design docs) is mid-flight with its own Scope Contract above. VOLATILE section rotation is deferred to whichever cycle closes last so that Top-3 / Current State / What Is Next reflect both cycles.

**Drift checks:**
- **Task drift:** Scope expanded once mid-session — appended the S5 Scope Contract after the audit-helpers AC completed (I omitted step 7 at session start). Caught and corrected; no other drift. Audit-surfaced fix to HANDOFF line 90 (bare SHA) was an explicit one-off per feedback memory; not a workflow.
- **Architecture drift:** No invariant degraded. Five invariants strengthened by mechanical-enforcement uplift. New audit scripts respect the Cross-Document Ownership Matrix (each script has a single invariant ID it owns).
- **Vision drift:** Same project. System after S5a IS the same LLM-driven personal health agent with mechanically-enforced session-lifecycle invariants now joining the mechanically-enforced research-domain invariants. Rigor compounds.

**PF attestation:**

S5 close (2026-05-25): No new PF-class entries this session. The HANDOFF line-90 bare-SHA defect surfaced by the audit was a residual S4-close miss (not a new failure mode); fixed in-session as a one-off scope expansion that the audit's own AC required. The mid-session scope-contract-omission (failure to append the contract at step 7) is logged here as an observation; if it recurs N=2 it promotes to PF. No PF-S2-01 or PF-S3-01 class incidents observed.

**Commit:** `9a3e44f` (S5a audit-scripts cycle).

## Session 6 close — v2 aplus-research calibration (2026-05-25)

All 7 ACs PASS. 4 calibration findings applied in place to the existing skill (no fork). One new invariant registered: INV-RESEARCH-CROSS-SECTION-ID. New schema `schemas/gate-4.25.schema.json` + 4 new gate_attest smoke tests (T13-T16). Existing 12 tests still pass.

**Skill changes:**
- Pipeline overview + mode tables + gate-by-mode matrix updated for Phase 4.25
- New Phase 4.25 ID-Reconcile spec (5 entity classes: citations, institutions, compound IDs, regulatory dates, trial registrations)
- New "Remediation brief addendum" section with verbatim post-fix-grep block
- Phase 3 judge brief includes literal JSON skeleton (9 dimensions, 2 structural rules)
- Phase 8 §3 archive permalink policy (scoped under `_archive/<slug>-<date>-<reason-slug>`)
- New Calibration history table near top (v1.0 → v1.1 → v2 ACs)
- Schema files table updated
- `lib/gate_attest.py`: phase 4.25 added to ATTESTED_GATES + SOURCE_MD map

**Tests:** 16/16 gate_attest, 89/89 across all audit + hook + gate suites combined.

**Drift checks:**
- **Task drift:** AC1 introduced a new invariant (INV-RESEARCH-CROSS-SECTION-ID) which was flagged in the original scope contract ("unless AC1 introduces a new INV; flag at the time"). Not silent drift. Otherwise scope held exactly.
- **Architecture drift:** No invariant degraded. INVARIANTS register gained one mechanically-enforced research-domain invariant. CLAUDE.md Cross-Document Ownership Matrix respected — SKILL.md owns the skill spec, INVARIANTS.md owns the invariants register, schema files own gate verdict structure.
- **Vision drift:** Same project. System after S6 has the aplus-research skill calibrated against the specific failure modes that S3/S4 BPC-157 surfaced. Skill is now ready for the peptide library campaign (Phase C, separate sessions).

**PF attestation:**

S6 close (2026-05-25): One new PF entry promoted (PF-S6-01, AP-ACT-BEFORE-VERIFY) caught by user mid-session: started a "beads cleanup" task without verifying current state or having a documented procedure; HANDOFF entry was stale and the issue had been resolved in S3/S4. User's "what procedure did you use" forced the honest answer. Logged in `memory/process-failures.md` with recurrence_count=1; feedback memory `feedback_beads_cleanup_procedure.md` saved with verify-first procedure. No PF-S2-01 or PF-S3-01 class recurrences observed. The Phase 4.25 schema mismatch I hit mid-session (top-level `iterations` required vs attest_simple not auto-populating it) was a latent gap in the documented scaffold pattern — not a PF; documented inline via T13-T16 tests. The `agent-verdict-halt` sentinel inconsistency observed during T15 debugging is pre-existing; recorded as an Open Issue for v2.5 cleanup.

## Session 7 close — design-doc template (2026-05-26)

Foundational artifact complete. `design/DESIGN_DOC_TEMPLATE.md` is the canonical contract for 18 downstream design docs (4 foundation roles in Pass-2; 14 specialists in Pass-4). Commit `0563269`. Pushed to `origin/feature/wiki-bpc157-aplus-research`. All 5 ACs PASS. PF-S3-01 guard cleanly held — adversarial-review findings were each personally verified against source before classification; 2 findings rejected with cited-evidence attestation (F-006 R-count empirical premise, F-023 worked-example copy-edit).

**Drift checks:**

- **Task drift:** S7 contract was 5 ACs. Mid-session the user flagged that I had conflated Pass-2 (design doc) with Session B (`/upgrade-agent` deployment) in my original scope-shaping question. I re-read the protocols + brief, restructured the plan, and the user accepted the corrected read. Two scope expansions surfaced: (a) capturing the "reject-but-adopt" pattern as a feedback memory (user-approved); (b) strengthening the Pass-1-complete status snapshot in the template §0.1 so future sessions can't miss it (user-approved). Both expansions were explicit user direction; no silent drift.
- **Architecture drift:** No invariant degraded. The template itself is a load-bearing new artifact but does not modify existing invariants. The Quant→Medical adaptation followed the project's existing Cross-Document Ownership Matrix (design docs are owned by `design/`; `/upgrade-agent` Phase 7 enforces generic agent.md constraints; the template explicitly delegates to it via §15.1 rather than restating). The 10-vs-11 AGENT_TEMPLATE.md disambiguation (F-001) preserves the existing `enforce-role-inlining.sh` hook semantics — the hook stays correct as-is for its purpose (catching incomplete mature profiles).
- **Vision drift:** Same project. System after S7 has the canonical design-doc structure that will produce 18 medical-LLM agent profiles. The foundation-role design docs (Pass-2) are now unblocked. The peptide library campaign (Phase C) remains the other parallel forward direction. No vision drift; the rigor compounds.

**PF attestation:**

S7 close (2026-05-26): No new PF-class entries this session. Watched specifically for PF-S3-01 recurrence during AC3 (the verification phase) — the discipline held: each finding was source-read before classification, two were rejected with cited evidence, the reject-but-adopt pattern was documented as a feedback memory rather than smuggled in as Legitimate. Watched for the "minor accretion" framing during the scope expansion for the template §0.1 status snapshot — declined to skip; the snapshot is load-bearing for the next session's correct read of pipeline state. AP-INCOMPLETE-PROPAGATION did NOT surface — synthesizing 22 findings across an 18-section template was the natural stress case for missed-propagation, and the §7 self-attest checklist was the explicit defense.

One observation worth noting (not promoted to PF): the inlining hook caught the H1 pattern `# Adversarial Reviewer` on my second sub-agent dispatch, exactly as Pass-1's CONTINUATION_BRIEF §1 Q1 documented. I rewrote the dispatch to use the `/adversarial-review` skill instead of role-tagged prose. This is the documented edge case where research-using-a-role-file is conflated with role-tagging-a-dispatch; the hook's deterrent behavior is correct.

## Session 8 close — Pass-2 Role 1 design doc (2026-05-26)

All 6 ACs PASS. `design/health-specialist-architect-design.md` Status: Final at 873 lines. First end-to-end run of `design/DESIGN_DOC_TEMPLATE.md` against a foundation role; template held under real use. 38 red-team findings (23 adversarial + 15 safety v1-substitute); Phase 4 PF-S3-01 guard cleanly held — each finding personally source-read before classification; 26 LEGITIMATE + 11 LEGITIMATE-MODIFIED + 1 REJECTED.

**Highest-leverage Phase-5 substantive additions:**
- 8th refusal class `AUTHORITY_FRAMING_BYPASS` (F-S2) covers 81.8% Authority Impersonation attack surface
- H-class composition (F-S1) — H1-H8 OUTBOUND row + Core Rule 13 + new INV-HARM-CLASS-COMPOSITION (PROPOSED)
- Pre-Role-7 escalation override-acknowledgment + contradictions-log requirement (F-S15) addresses largest pre-deployment exposure
- Operator-as-A3 anti-pattern (F-S3 AP8) + EC-9 — encodes the medical-LLM asymmetry (operator inside trust boundary AND named adversary in Role 4 threat catalog)
- Image-handling Tools-conditional gating (F-S6) protects labs-specialist LM-01 critical path

**Critical fixes:** AC-4 grep mechanism returning 4 lines instead of 7 identifiers (F-001 empirically verified); §13 row 9 mis-scoped against §16 OUT-OF-SCOPE (F-002 — restated as REFERENCED-by-template-for-downstream).

**Hook edge case logged:** Security profile uses `## Audit Protocol` instead of `## Modes`; INV-ROLE-INLINING hook blocked the safety dispatch on first attempt. Resolved with additive synthetic `## Modes` pointer to Audit Protocol (no paraphrasing of existing 11 sections). Second instance of profile-vs-hook expectation mismatch (first: S7 `/adversarial-review` H1). Pattern: v1-substitute software profiles don't all conform to the medical-template hook's section-name expectations. Documented in dispatch-ledger.jsonl.

**Drift checks:**

- **Task drift:** S8 contract was 6 ACs (Phase 1 drafter dispatches → Phase 2 synthesis → Phase 3 red team → Phase 4 verification → Phase 5 finalize → close audits). All 6 PASS exactly as specified. Hook edge case during Phase 3 security dispatch resolved in-session without scope expansion; the synthetic Modes pointer is faithful to the security profile content. No silent scope drift.
- **Architecture drift:** No invariant degraded. Phase 5 SURFACED a candidate new invariant (INV-HARM-CLASS-COMPOSITION, tagged PROPOSED in §16) per F-S1 disposition — this is candidate-for-register-add via the INVARIANTS change-discipline ritual at next review, not an unilateral promotion. The current 12-entry register remains untouched. The new invariant is documented in the design doc only.
- **Vision drift:** Same project. System after S8 has the first foundation-role design doc complete, demonstrating DESIGN_DOC_TEMPLATE.md works under real use against a 727→873-line Pass-2 cycle. The 18-section template + Phase Coverage Matrix + Self-attest checklist all held; the 38-finding red team produced operational improvements (8 BLOCK-class fixes incorporated). Pass-2 for Roles 2/3/4 is now unblocked; the OUTBOUND interface contracts are established. No vision drift; the rigor compounds.

**PF attestation:**

S8 close (2026-05-26): No new PF-class entries this session. Watched specifically for PF-S3-01 recurrence during Phase 4 (the falsification window for design-doc-protocol context) — the discipline held: 38 findings each personally source-read before classification; F-019 REJECTED with cited evidence (reviewer self-withdrawn after personal recount); empirical verifications performed for F-001 (grep returned 4 broken vs 7 correct), F-002 (3-line read confirmed contradiction), all 5 BLOCK safety findings against Role 4 substrate line ranges. Reject-but-adopt pattern from S7 did NOT recur (0 cases this cycle); discipline remains on the watch list but did not surface as a temptation.

Watched for AP-INCOMPLETE-PROPAGATION during 37-disposition Phase-5 application across 18 sections + Appendix A — the §7 self-attest checklist was the explicit defense; all 17 binary criteria passed at finalize. Watched for the "minor accretion" framing when adding 6 new ECs (8→14) past template upper bound (4-8) — the addition was load-bearing per Phase 4 dispositions, not editorial.

Two observations worth noting (not promoted to PF): (a) the inlining hook blocked the security dispatch on first attempt due to security profile's `## Audit Protocol` vs hook's `## Modes` expectation — same class as S7's adversarial-review H1 issue; the v2.5 punch-list item should now be promoted to a documented edge case in the hook (recurrence_count=2 for the class). (b) The §14 EC count grew past template's stated upper bound of 4-8 to 14 due to Phase 4 dispositions adding 6 new ECs — this is justified for foundation-role-1 (the OUTBOUND-establishing doc) but may signal the template's §14 budget should be re-evaluated for foundation roles vs specialists.

**Commit:** _(to follow this close note)_

## Session 9 close — Pass-2 Role 1 Session B (`/upgrade-agent` deployment) (2026-05-26)

All 9 ACs PASS. `~/Documents/Projects/skills_library/roles/health-specialist-architect/agent.md` deployed at 121 lines / 3,236 cl100k tokens. First end-to-end run of `/upgrade-agent` against a finalized Pass-2 design doc; the 8-phase pipeline held. Phase 4 required 3 validation iterations on R1 (fact-checker found line-budget + citation-regex defects; judge found D2/D3/D9 sub-9 + D10 sub-9 on iter-2); R2 + R3 cleared iter-1. Phase 6 adversarial review surfaced 15 findings (1 Critical inherited / 5 Major / 6 Minor / 3 Nitpick); 8 applied at Phase 7, 1 deferred per reviewer option, 6 documented-as-acceptable per reviewer rationale.

**Highest-leverage Phase-5/Phase-7 substantive decisions:**
- Modes section materialized (single "Design Mode") to satisfy `enforce-role-inlining.sh` 11-section expectation; design-doc §13 row 13 (Modes-required WARN) addressed pragmatically without prejudging §18 OQ-7
- Modes placement repositioned post-Anti-Patterns / pre-Negative-Examples per F-A03 (design-doc §12.4 canonical sequence)
- Token budget overrun documented in catalog row (~3,100 with characterization pointer) rather than aggressively compressed; medical-domain density (8-class enum + GRADE HALT + H-class composition + Mechanism A/B/C mapping) intrinsically requires more tokens than software roles
- Loop-Breaking split per F-A04 from 4 to 5 thresholds to satisfy D7 9/10 explicit threshold count

**Critical findings posture:** F-A01 (refusal-class 7-vs-8 residual in design-doc prose at §1/§3.1/§5.11/§15.2) deferred to follow-up bead per reviewer option (a) — agent.md itself is internally consistent at 8 classes; the upstream prose layer is the defect. PF-S3-01 guard held: 38 design-doc findings + 6 validator reports + 1 adversarial review + 15 Phase-6 findings each personally verified before classification. Reject-but-adopt pattern from S7 did NOT recur (0 cases). F-A07/F-A12/F-A13/F-A14/F-A15 accepted reviewer's "no change" recommendation with rationale.

**Hook edge case logged (new class).** S9 surfaced a DISTINCT edge case from S7/S8: `enforce-role-inlining.sh` regex `roles/[a-z-]+/agent\.md` over-triggers on non-role-tagged research dispatches that merely mention a role-profile path. Three Phase-3 dispatches blocked iter-1; one Phase-6 dispatch blocked iter-2 because example H1 in output spec matched H1 regex. Workaround: refactor path refs to directory-only + H3 headers in output spec + avoid literal H1 patterns in prompts. Recurrence_count=1 for this NEW class. The S7/S8 profile-vs-section class (recurrence_count=2) did NOT recur. Two distinct hook-edge-case classes now documented; v2.5 punch-list expanded.

**Drift checks:**

- **Task drift:** S9 contract was 9 ACs (Phase 1 baseline → Phase 2 rubric → Phase 3 research → Phase 4 validation → Phase 5 synthesis → Phase 6 adversarial → Phase 7 corrections → Phase 8 close-out → audit-script close). All 9 PASS. Two mid-session adjustments: (a) Token-budget overrun characterization added to catalog row (anticipated in scope contract as "Adversarial review may surface compression opportunities") — not silent drift; (b) F-A01 deferred-to-bead per reviewer option (a) — explicit user-style decision documented in close note. No silent scope drift.
- **Architecture drift:** No invariant degraded. INV-ROLE-INLINING hook continued to fire (correctly per its current regex spec); workaround documented for future improvement. The 12-entry register remains unchanged. Candidate INV-HARM-CLASS-COMPOSITION still PROPOSED (not unilaterally promoted). The deployed agent.md respects every project invariant: INV-ROLE-INLINING (all sections present); INV-BRANCH-NOT-MAIN (commits to feature branch only); INV-PF-ATTESTATION (this close attestation). No architecture drift; the rigor compounds.
- **Vision drift:** Same project. System after S9 has the first deployed medical-LLM agent profile alongside its source design doc. The 4-role foundation pipeline is 25% complete (Role 1 of 4); the `/upgrade-agent` 8-phase pipeline has been validated end-to-end against a real Pass-2 deliverable. The OUTBOUND interface contracts from Role 1's design-doc §4 are now inheritance-ready for Roles 2/3/4. No vision drift.

**PF attestation:**

S9 close (2026-05-26): No new PF-class entries this session. Watched specifically for PF-S3-01 recurrence during Phase 4 validation loop (the explicit falsification window for upgrade-agent context) — the discipline held: 6 validator reports (3 fact-checkers + 3 judges across iter-1/iter-2/iter-3) each produced as SEPARATE dispatches in PARALLEL with FRESH context; 9/10 pass threshold enforced strictly (8.5 ≠ 9 not invoked once; no rounding); R1 v2 iter-2 single fact-check FAIL + single judge sub-9 dim correctly classified as FAIL not "close enough to pass"; iter-3 verified independently against R1 v3 with no orchestrator self-attestation of either verdict. Phase 6 adversarial review's 15 findings each personally source-read before classification per PF-S3-01 guard; F-A07/F-A12/F-A13/F-A14/F-A15 explicitly classified "documented-as-acceptable per reviewer rationale" rather than auto-applied or auto-dropped.

Watched for AP-INCOMPLETE-PROPAGATION during 873→121-line compression (Phase 5 synthesis) — the per-section line budgets + 11-section mechanical check + Phase 7 final-corrections checklist all held; one section-order defect (Modes before Anti-Patterns) caught by Phase 6 reviewer and fixed via F-A03. Watched for "minor accretion" framing on the token-budget overrun — declined to skip; the catalog row carries an explicit pointer to the characterization rather than silent acceptance.

Three observations worth noting (not promoted to PF):

(a) **Hook edge-case path-pattern over-trigger (NEW class, recurrence_count=1).** S9-specific instance of the hook firing on non-role-tagged dispatches that merely mention role-profile paths. Distinct from S7/S8 profile-vs-section mismatch class (recurrence_count=2). Both classes now documented; the inlining hook needs design attention for both: (i) accept role-specific section names alternative to `## Modes`; (ii) refine the role-context detection to distinguish "this dispatch IS role-tagged" from "this dispatch MENTIONS a role profile path." Promotion candidate for v2.5 punch-list.

(b) **Token-budget overrun is intrinsic to medical-domain.** Software role profiles average ~1,950 cl100k tokens. The medical-specialist-architect lands at ~3,236 (~66% over) due to 8-class refusal taxonomy enum + GRADE HALT condition + H-class composition formula + Mechanism A/B/C mapping + fabrication-guard surface list. The reviewer's characterization explicitly identified ~670 tokens as load-bearing medical-domain anchors that cannot compress without losing safety properties. Recommend formal budget allowance for medical specialist profiles (separate from software role budget) as a follow-up ADR.

(c) **Phase 4 validation iterations correctly converged.** The HARD RULE pass threshold ("9/10 every dimension; no rounding, no softening") was tested in S9: iter-1 produced FAIL verdicts that explicitly named under-budget dimensions; iter-2 fixed those but surfaced new D10 (freshness) gaps in the same artifact; iter-3 converged. At no point did the orchestrator round or soften. The remediator workflow (separate Agent dispatch reading both fact-checker + judge reports) functioned as designed.

**Post-deployment review and re-scope (S9 addendum, same day):**

After initial commit `4176a62` deployed to `~/Documents/Projects/skills_library/`, user requested `/review-pr` against PR heavydropio/skills_library#14. Doc-only modification (3 of 6 agents: Code Quality + Contracts + Historical Context). Phase 1 surfaced 18 findings; Phase 2 dedup → 17; Phase 3 blind triage classified 14 LEGITIMATE / 3 DECISION (relitigating Phase-6 dispositions F-A03, F-A07, F-A14).

**Architectural realization.** Four HIST-class LEGITIMATE findings (HIST-001 token budget exceeds catalog guardrail; HIST-003 library-index references paths external to skills_library; HIST-005 profile names project-specific artifacts unresolvable inside skills_library; HIST-006 cross-project authoring pattern undocumented) all pointed at the same root: **a project-specific role does not belong in the shared skills_library**. User confirmed re-scope to project-local `.claude/agents/` (Option B). All 4 HIST findings dissolved by re-scope; 7 QUAL findings reclassified DECISION (faithful to design-doc §5/§8/§2.2/§11.2/§7 patterns rather than skills_library convention); 3 QUAL findings (QUAL-007 template-string → fenced block; QUAL-010 library-index auto-load dedup; QUAL-011 regulatory Path/Source header) applied in the re-scoped deployment.

**Final deployment.** `~/Documents/Projects/a-plus-maxing/.claude/agents/health-specialist-architect/agent.md` (127 lines / 3,252 cl100k tokens / 11 sections) + paired `library-index.md` (24 lines). Commit `280aba9`. PR #14 on skills_library closed with re-scope comment; feature branch deleted from both local and origin; skills_library `roles/orchestrator/catalog.md` row reverted (user-flagged linter restore).

**Process observation — review-pr against cross-repo PR works but exposes the framework's blind spot:** the skill's HARD RULE "every LEGITIMATE finding gets fixed" assumed all findings are at the same architectural layer. When 4 of 14 LEGITIMATE findings collectively meant "wrong architectural choice," forcing line-level fixes would have papered over the real defect. The user's instinct ("make it project-specific — does that solve it?") was the right escalation; the triage table re-applied at the new layer made the dispositions deterministic.

**Commit:** `280aba9` pushed to `origin/feature/wiki-bpc157-aplus-research` (S9 close state).

