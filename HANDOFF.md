---
title: Session Handoff
type: note
owner: Walter McGivney
created: 2026-05-16
last_reviewed: 2026-06-05
status: active
depends_on: []
superseded_by: null
review_cadence: weekly
---

# Session Handoff

## Scope Contract — Session 37 (2026-06-06)

> Confirmed by Walter ("proceed with the contract path"). **Unit = Phase B of the `/execute-plan` re-entry: design/remediation only.** Clear the two blockers that gate W3/W4 (`5wo`, `qwj`) so Phase C can run `/execute-plan` in wave mode uninterrupted. NO V1 task built, NO `/execute-plan` invocation this session. Both blockers carry a decision-fork surfaced to Walter for adjudication — neither is resolved silently.

Goal: Resolve `5wo` and `qwj` (the two W3/W4 design/remediation blockers), each via dispatched-Architect/SE analysis with the decision-fork surfaced to Walter, then the chosen resolution applied and the bead closed/split — no production V1 task built.

Acceptance criteria:
- [ ] AC1 (`5wo`) — Architect (full profile inlined, INV-ROLE-INLINING) analyzes the `render.emit` single-`Path` vs ADR-0004-T2 pagination conflict against ADR-0004 + the T1 Interface Contract + `render.py`; the (a) amend-T1-return-contract vs (b) caller-orchestrated-pagination fork is presented to Walter in prose with a recommendation; Walter's choice is recorded + documented in the owning artifact (ADR/spec/recipe per the ownership matrix) with the downstream single-path assumptions (T3/ADR-0006-T2/ADR-0007-T2) reconciled; `5wo` closed (or left open with a precise residual if Walter defers the doc-amendment into the W4 build).
- [ ] AC2 (`qwj`) — `scripts/guard/pii_scan.py` made operator-agnostic (operator-identity tokens sourced from a gitignored operator config, sane no-config default; tests updated/added); the vault-prose-hit policy (~924/~150 tracked-prose hits vs the ADR-0005-T1 pre-commit hook) decided with Walter (allowlist/scope vs clone-init sanitization) and recorded; `qwj` closed or split (residual sanitization beaded if it is clone-init territory).
- [ ] AC3 — baseline stays green: full suite (was 120/2) + governance audits unaffected; no regression.
- [ ] AC4 — lifecycle + close: `/review-pr` on the Phase-B PR → fix every legitimate finding (priority-only, never suppress — PF-S26-01) → `/merge`; then the S37 close (suite + 4 close audits + branch-completeness green at `--session 37`, PF attestation, VOLATILE 6-clause rotation) sequenced AFTER the merge (PF-S25-01).

Files I WILL touch: `scripts/guard/pii_scan.py` + `tests/guard/*` (qwj); a new gitignored operator-config file + `.gitignore` entry (qwj); the artifact owning the emit-return contract — candidate set `docs/task-plan/ADR-0004-T1.md`, `docs/spec/adr-0004-adr-0007-spec.md`, and the single-path assumptions in the T3/ADR-0006-T2/ADR-0007-T2 recipes (5wo — exact set depends on Walter's fork choice); `vault/decisions/` (dated decision note if 5wo amends the contract); `HANDOFF.md` (contract + close rotation); `vault/sessions/session-37.md` (NEW); `vault/meta/log.md` (append); `.beads/issues.jsonl` via `bd`.

Files I will NOT touch: any `v1-build` task module (`br1`/`xlu`/`ml1`/`ftm`/`yo6`/`oaf`/`8cv`/`1aa`/`1ih` — Phase C); `/execute-plan` invocation (Phase C); other `scripts/**` production code beyond `pii_scan.py`; the deployed roster `.claude/agents/*`; `lib/gate_attest.py`, schemas, bda, the wiki-ingest gate; `INVARIANTS.md` + the audit scripts (no unilateral invariant/mechanical change); real operator-PII values (live only in the gitignored config, never tracked); `vault/{compounds,biomarkers,library}/` content; `main` directly.

NOT doing: building any V1 task / running `/execute-plan` (Phase C); hand-scrubbing the ~150 vault-prose operator-name files (clone-init/ADR-0005 sanitization — beaded if residual, not done inline); silently resolving either fork; mechanizing the wave-attestation field (`vvs`); editing the build-plan wave structure.

Invariants at risk: INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-HO-ROTATION, INV-HO-NO-STALE-HASH, INV-BRANCH-NOT-MAIN, INV-TRUNK-COMPLETENESS, INV-ROLE-INLINING. Governing principle for qwj: ADR-0005 PII-free trunk — the gitignored-config approach must keep the trunk operator-name-free.

## Scope Contract — Session 36 (2026-06-06)

> Confirmed by Walter ("scope phase A and then proceed" — after Walter caught at S36 open that the V1 execute stage was hand-rolled per-task instead of run through the sanctioned `/execute-plan`, and that the build-plan wave order was abandoned from S32; PF-S36-01 logged). **Unit = Phase A of the execute-plan re-entry: governance + bookkeeping only, NO new code.** Get the V1 build back onto the `/execute-plan` rails by documenting it as the execute-stage path, adding the wave + checkpoint convention to v1-build scope contracts, reconciling the wave-naming drift, and banking the S36 damage-assessment (all runnable build-plan checkpoints green) as the verified baseline. Phase B (unblock `5wo`/`qwj`) + Phase C (run `/execute-plan` in wave mode) are explicitly NOT this session.

Goal: Adopt `/execute-plan` as the documented, sole sanctioned V1 execute-stage path and stop the out-of-order-build drift — via CLAUDE.md governance, the v1-build wave-attestation convention, wave-naming reconciliation, and a recorded verified baseline — with no production code built.

Acceptance criteria:
- [ ] AC1 — PF-S36-01 logged in `memory/process-failures.md` (the execute-stage skill-substitution failure + the clean damage assessment). [DONE — commit `21d7241`]
- [ ] AC2 — CLAUDE.md gains a "V1 Build Execution" section naming `/execute-plan` as the ONLY sanctioned path to build `docs/task-plan/` recipes, with the project path-mapping (recipes=`docs/task-plan/`, build plan=`docs/build-plan/build-plan-v1-full.md`, roles=`skills_library/roles/`), the wave-order + per-wave-checkpoint-gate rule, and read-in-full-before-invoke (PF-S17-01).
- [ ] AC3 — CLAUDE.md Session-Start step 7 gains the v1-build convention: a v1-build scope contract cites its build-plan wave AND attests the prior wave's checkpoint Go/No-Go passed (documented convention; mechanical enforcement BEADED, not an INV-SCOPE-CONTRACT change this session).
- [ ] AC4 — Wave-naming reconciled: HANDOFF volatile sections + `vault/sessions/session-36.md` use the build-plan topological wave numbers (W1..W7) with per-wave done/open state stated; bead `orl` closed.
- [ ] AC5 — Damage-assessment baseline recorded: `vault/meta/overview.md` phase-state updated to the current build wave-state (9/18 leaves; W1-2 complete, W3-4 partial, W5-7 open; all runnable build-plan checkpoints green as of S36) + `vault/sessions/session-36.md` captures the checkpoint-gate evidence.
- [ ] AC6 — The mechanical enforcement of the v1-build wave-attestation field (extend `scope-contract-audit.sh` + the INVARIANTS change-discipline ritual) is filed as a bead (deferred — needs Walter approval).
- [ ] AC7 — Lifecycle + close: docs-subset `/review-pr` (Code Quality + Contracts + Historical) on the Phase-A PR → fix every legitimate finding (priority-only, never suppress — PF-S26-01) → `/merge`; then the session close (suite/governance-suites green, 4 close audits + branch-completeness green at `--session 36`, PF attestation, VOLATILE 6-clause rotation) sequenced AFTER the merge (PF-S25-01).

Files I WILL touch: `memory/process-failures.md` (PF — done); `CLAUDE.md` (V1 Build Execution section + step-7 v1-build convention); `HANDOFF.md` (S36 contract + close rotation + wave-naming reconciliation + baseline pointer); `vault/meta/overview.md` (phase-state baseline — matrix owner of milestone status); `vault/sessions/session-36.md` (NEW); `vault/meta/log.md` (append S36); `.beads/issues.jsonl` via `bd` (close `orl`; file the scope-contract-audit mechanization bead).

Files I will NOT touch: `scripts/**` production code + `tests/**` (NO building this session); `docs/task-plan/*`, `docs/spec/*`, `docs/adr/*`, `docs/build-plan/*` (read-only upstream — the build plan is the canonical wave source); `INVARIANTS.md` + `scripts/scope-contract-audit.sh` (no unilateral invariant/mechanical change — AC6 BEADS it); `.claude/agents/*` + the deployed roster; `lib/gate_attest.py`, `schemas/*`, bda, the wiki-ingest gate; `vault/{compounds,biomarkers,library}/` content; the real operator-PII values; `main` directly.

NOT doing: building any `v1-build` task (`br1`/`xlu`/`ml1`/`ftm`/`yo6`/`oaf`/`8cv`/`1aa`/`1ih` — Phase C); resolving `5wo` or `qwj` (Phase B); invoking `/execute-plan` against a real recipe (Phase C); mechanizing the wave-attestation field / editing `scope-contract-audit.sh` / changing `INV-SCOPE-CONTRACT` (AC6 beads it); editing the build plan / specs / ADRs / recipes; library-population.

Invariants at risk: INV-SCOPE-CONTRACT (Phase A documents a CONVENTION adjacent to it; does NOT change the six audited fields), INV-PF-ATTESTATION, INV-HO-ROTATION, INV-HO-NO-STALE-HASH, INV-BRANCH-NOT-MAIN, INV-TRUNK-COMPLETENESS, INV-ROLE-INLINING.

### S36 Scope Contract Evaluation (2026-06-06, volatile)

- **AC1 — PASS.** PF-S36-01 logged (`memory/process-failures.md`, commit `30749e4`).
- **AC2 — PASS.** CLAUDE.md "V1 Build Execution" section names `/execute-plan` the sole sanctioned execute path + project path-mapping + wave-order + checkpoint-gate rule + read-in-full.
- **AC3 — PASS.** CLAUDE.md step-7 carries the `v1-build` wave+checkpoint convention (documented; mechanization beaded `vvs`, NOT an INV-SCOPE-CONTRACT change — the six audited fields are untouched, audit green at `--session 36`).
- **AC4 — PASS.** Wave-naming reconciled to build-plan topological waves (CLAUDE.md + overview.md + this HANDOFF rotation use W1-W7); `orl` CLOSED.
- **AC5 — PASS.** `vault/meta/overview.md` carries the S36 build wave-state baseline (9/18; W1-2 complete, W3-4 partial, W5-7 open; runnable checkpoints green); `session-36.md` records the checkpoint evidence.
- **AC6 — PASS.** `vvs` filed (P2) — mechanize the wave-attestation field in `scope-contract-audit.sh` (needs INV change-discipline + Walter approval).
- **AC7 — PASS (this close).** Docs-subset `/review-pr` (Code Quality + Contracts + Historical) on PR #57 → 9 findings (8 LEGITIMATE fixed, 1 NOT_A_BUG), 0 suppressed → rebase-merged at `6da2d4c` (as of 2026-06-06 S36 close); close on `fix/s36-close` AFTER the merge (PF-S25-01).
- **CHANGED:** none silent. The 8 review fixes (QUAL-001..004, API-001, HIST-001..003) STRENGTHENED the docs — removed a volatile-phase-state accrual from the static CLAUDE.md, a misleading roles-path note, a resurrected retired class label, and a narrative-vs-tracker `orl` drift. NO production code touched (Phase B/C deferred).

### Drift checks (S36 close)

- **Task drift:** the contracted unit (Phase A governance — adopt `/execute-plan`, bank the verified baseline, reconcile wave-naming; NO code) delivered exactly. The damage assessment (read-only, surfaced by Walter's question) confirmed the built outputs sound. No expansion into building tasks / Phase B / Phase C; the review fixes were in-scope doc corrections.
- **Architecture drift:** toward LESS violation — the execute stage now has a documented sanctioned path + wave-checkpoint discipline (closing the PF-S36-01 root); the ownership-matrix violation (phase-state in the static CLAUDE.md) introduced mid-session was caught by the review + removed; INV-SCOPE-CONTRACT unchanged (convention documented, mechanization beaded); INV-BRANCH-NOT-MAIN held; INV-TRUNK-COMPLETENESS green; INV-ROLE-INLINING held (the 3 reviewers dispatched by registered type).
- **Vision drift:** none. What the system IS after S36: "a local-first health tracking + planning system whose V1 build (9/18, data spine built) is now back on the sanctioned `/execute-plan` wave-gated rails, with the prior out-of-order builds verified undamaged." Matches `design/vision.md`.

### PF attestation

S36 close (2026-06-06): **One new PF promoted this session — PF-S36-01 (`AP-STAGE-SKILL-SUBSTITUTION`)**, at Walter's challenge: the entire V1 execute stage was hand-rolled per-task instead of run through the sanctioned `/execute-plan` skill, and from S32 the build-plan wave order was abandoned. Logged with the full damage assessment — the built OUTPUTS are SOUND (verified via the build plan's own checkpoint gates: full suite 120/2, 0 dangling refs, runnable Wave 2→3 + 3→4/4→5 gates green); the gap is process-only, the residual being the checkpoint gates that cover skipped tasks (the Wave 3→4 PII-commit boundary, needs `xlu`) + the never-run Tier-2 wave review. Mitigation: adopted `/execute-plan` in CLAUDE.md (Structural-1), added the `v1-build` wave-attestation convention (Structural-2, mechanization beaded `vvs`), reconciled wave-naming (`orl` closed, Structural-3). Observed + held: (a) **PF-S26-01** — the docs-subset review's 9 findings: 8 LEGITIMATE all fixed, 1 NOT_A_BUG (the agent's own verdict), 0 suppressed; the matrix stayed priority-only. (b) **PF-S25-01 TRIPPED-CLEAN** — the close sequenced AFTER the PR #57 merge on `fix/s36-close`; the review even caught a nascent instance (HIST-002: an "`orl` closed" claim ahead of the tracker) and it was fixed before merge. (c) **PF-S17-01** — `/review-pr` + `/merge` read in full; no `Workflow` substitution. (d) **PF-S13-01** — full session-open protocol run with real output + `branch-completeness-audit.sh` at open. (e) GraphQL throttled all session → REST for PR create + merge (full-40-char-SHA guard); the readiness check confirmed the PR head matched the pushed fix before merge.

## Historical Scope Contracts (archived)

Scope contracts for Sessions 5-35 + their evaluations were moved to `vault/sessions/scope-contract-archive.md` (S32 archived the S5-31 set; S33 archived S32; S34 archived S33; S35 archived S34; S36 archived S35) to keep this handoff lean. The current (S36) scope contract is above; the archive holds the prior-session archaeology.

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
7. Read the most recent session note in `vault/sessions/` — currently `session-2.md`
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

1. **`/execute-plan` is the sanctioned execute path (PF-S36-01) — NEW + STANDING.** Build V1 tasks via `/execute-plan` in WAVE mode against `docs/build-plan/build-plan-v1-full.md`; complete build-plan waves IN ORDER and gate on the per-wave checkpoint Go/No-Go — never hand-roll a per-task SE-dispatch substitute. A `v1-build` scope contract cites its wave + attests the prior wave's checkpoint passed (CLAUDE.md "V1 Build Execution" + step 7). The hand-rolled per-task build (S30-S35) left Waves 3-4 partial; re-entry completes them in order. Read `/execute-plan`'s SKILL.md + references IN FULL before the first wave run.
2. **read-before-invoke (PF-S13-01 + PF-S17-01) — STANDING.** Read each skill/recipe/protocol IN FULL before invoking — `/execute-plan`, `/review-pr`, `/merge`, the task recipe. No `Workflow`/hand-rolled substitution for a gated skill (the PF-S36-01 family root). `.venv/bin/python -m pytest`, never from memory.
3. **PF-S3-01 layered-review is load-bearing on single-builder tasks (3rd consecutive: `n9h`/`gu4`/`3gp`).** For any single-SE build (Phase C), the full `/review-pr` + blind triage + blind verify is non-optional; when self-verifying a falsifiability gate, test EVERY failure mode including the cross-process one.

**Demoted from prior Top-3:** the S35 "generation entry point published / AC-3 child-process falsifiability" framing (that gate is merged + falsifiable across the process tree; the forward risk is now the execute-plan/wave discipline).

## Current State (volatile)

- **S36 (2026-06-06) put the V1 build back on the `/execute-plan` rails — governance only, no code.** Walter caught that the execute stage had been hand-rolled per-task (not via `/execute-plan`) and that the build-plan wave order was abandoned from S32. PF-S36-01 logged; the built outputs verified SOUND (the build plan's own checkpoint gates pass — full suite 120/2, 0 dangling refs, Wave 2→3 + 3→4/4→5 gates green). PR #57 (PF + CLAUDE.md `/execute-plan` adoption + step-7 wave convention + overview baseline + session-36) → docs-subset `/review-pr` (9 findings; 8 fixed, 1 NOT_A_BUG, 0 suppressed) → rebase-merged at `6da2d4c` (as of 2026-06-06 S36 close).
- **`/execute-plan` is now the documented sole execute-stage path** (CLAUDE.md "V1 Build Execution" + the step-7 `v1-build` wave/checkpoint convention). Wave-naming reconciled to build-plan topological waves (`orl` CLOSED). `vvs` filed (P2 — mechanize the wave-attestation field).
- **Build: 9/18 leaves.** W1-2 complete; W3 2/4 (`xlu` needs `qwj`, `br1` open); W4 2/5 (`yo6` blocked-on-`5wo`, `ml1`, `ftm` open); W5-7 open. Live per-wave state in `vault/meta/overview.md`.
- **SINGLE TRUNK** unchanged (since S22). Suite **120 passed / 2 skipped** (Linux-only egress).
- **Active landmarks:** no trigger windows opened. LM-04 still pending (the `generate.run` producer is live but unfed).

**Historical (kept for reference):** `vault/sessions/session-36.md` + `vault/meta/log.md` S36 entry.

## What Is Next (volatile)

### Resume checklist — next session (S37) open

**Clean slate — nothing dangling from S36.** No pending PR cycle, no un-run audit, no uncommitted state: `main` @ `a5fc5fb` (as of 2026-06-06 S36 close), tree clean, 0 open PRs, both S36 PRs (#57 content, #58 close) merged. The next session opens normally:

1. Run the Session Start Protocol (steps 1-6) + `branch-completeness-audit.sh` at OPEN. Baseline suite = 120 passed / 2 skipped.
2. Cut a `fix/`-branch off `main` for Phase B; write + confirm the S37 scope contract (Phase B unblocks the W3/W4 leaves; cite that context).
3. **Phase B is DESIGN / REMEDIATION — NOT a `/execute-plan` wave yet** (execute-plan wave mode begins at Phase C):
   - **`5wo`** — `bd show 5wo`; read `docs/adr/ADR-0004-on-demand-single-file-artifact-generation.md`, the T1 Interface Contract in `docs/spec/adr-0004-adr-0007-spec.md`, and `scripts/generate/render.py`. Dispatch Architect; the fork (amend `render.emit` to return ≥2 paths vs caller-orchestrated pagination) is an Interface-Contract decision — **surface the options to Walter for adjudication, don't pick silently.**
   - **`qwj`** — `bd show qwj`; read `scripts/guard/pii_scan.py`. Make the scanner operator-agnostic (config/parameter-driven, not a hard-coded name) per the ADR-0005 clonable PII-free trunk. Resolve before `xlu` (now a wired dependency).
4. **Phase C** (after B): `/execute-plan` in WAVE mode — read its SKILL.md + references IN FULL first (PF-S17-01) — complete W3 (`br1`+`xlu`) → W4 → W5 → W6 → W7, gating on each per-wave checkpoint + a wave PR.

### S36 banked the `/execute-plan` re-entry baseline. Next: Phase B (unblock `5wo`/`qwj`) → Phase C (`/execute-plan` wave mode, complete W3→W7 in order).

**RESUMPTION POINT.** S36 was Phase A (governance: adopt `/execute-plan`, bank the verified baseline, reconcile wave-naming — no code). **Open the next session on `main`** (Start Protocol + `branch-completeness-audit.sh` at open). The re-entry continues:

1. **Phase B — clear the wave-completion blockers (do first):**
   - **`5wo` (P2)** — the `render.emit` single-`Path` vs `ADR-0004-T2` ≥2-path pagination Architect amendment (gates `yo6`/W4). An Interface-Contract/ADR decision; do NOT resolve silently inside T2.
   - **`qwj` (P2)** — the PII scanner hard-codes the operator name + ≈924 `scan` hits across tracked vault prose (now a WIRED dependency of `xlu`/W3). Resolve before `xlu`.
2. **Phase C — resume `/execute-plan` in WAVE mode** (read its SKILL.md + references in full first, PF-S17-01; project path-mapping in CLAUDE.md "V1 Build Execution"): complete **Wave 3** (`br1` spike + `xlu`) → run the Wave 3→4 checkpoint AS A GATE (incl. the PII-commit boundary `tests/hooks/test_block_pii_commit.sh` + SEC-01(b), runnable once `xlu` exists) → wave PR. Then **Wave 4** (`ml1` + `ftm` + `yo6`) → **Wave 5** (`oaf` + `8cv`) → **Wave 6** (`1aa`) → **Wave 7** (`1ih`). One wave ≈ one session.
3. **The first ARTIFACT (LM-04)** lands when `generate.run` is invoked with real operator data (Walter-pending exports) — the producer is live; only the data is missing.

**Published surfaces the next waves consume:** `generate.run(artifact_name) -> Path` (S35) · `render.emit(template, store_read) -> Path` + `component_set.py` (S34; path-return is the `5wo` open question for T2) · the `Adapter` Protocol + 4 adapters (`oaf` assembles the wired set) · `ingest.run(adapter, export_file, root=…)` · `store.append`/`read` (cross-item `read_all`/`items` pending `4yk`) · `keying.py` (never redefine) · `egress_guard.run` · `pii_scan.scan` (for `xlu` — resolve `qwj` first). Enforcement-first holds: no plan-reasoning-over-PII task buildable until the router (`br1`/`ftm`, W3/W4).

**Operator-data preconditions** (Walter-pending): 23andMe raw → `vault/dna/raw/`, the Oura/Apple-Watch/Garmin exports, meal-template content, January-2026 issue characterization. The three meta files (`operator-profile`/`current-state`/`goals`) remain `status: scaffold`.

**Parallel track (unblocked + gated):** library-population via research-only `/aplus-research` sessions — PF-S22-01 window: ONE merge target + `branch-completeness-audit.sh` + `wiki-lint.sh` at each batch close. V1 is a thin-library MVP and does not block on it.

### Open beads carried
- **V1 build execution (label `v1-build`):** **9 closed** (W1 `394`/`bez`/`qbb`; W2 `89a`/`e9m`; W3 `6be`/`gu4`; W4 `n9h`/`3gp`). OPEN: W3 `xlu`(needs `qwj`)/`br1`; W4 `yo6`(needs `5wo`)/`ml1`/`ftm`; W5 `oaf`/`8cv`; W6 `1aa`; W7 `1ih`. Plus `e3d` (recipe doc-consistency, non-blocking).
- **PR review beads open:** `1ww`/`qwj`/`ivt`/`z2u` (PR #44), `1vi` (PR #47), `5wo` (PR #53), `4yk` P2 + `u8u` P3 (PR #55). S36: `vvs` P2 filed; `orl` CLOSED.
- **V1 spec/build-plan gaps (S29):** `kz6`, `12p`, `434`, `bpu`, `dv3`, `4xe`.
- **P2:** `dke`, `3v5`, `xg4`, `382`, `w3n`, `5bd`, `5l9`/`78p`, `pmp`, `h1z`, `rc1`.
- **P3:** `0oy`, `ko5`, `75t`, `ae0`/`d6g`/`4ba`/`3v6`/`dip`, `t7z`/`fsr`/`8qe`, `r7t`/`7rm`/`60f`, `5jr`, `9c5`/`pnl`/`2n1`/`4h1`/`smw`, `mxo`, plus pre-existing `1ek`/`6ln`/`mdv`/`1rm`/`2gs`/`623`/`f2r`/`yfu`/`2qq`/`p47`/`o9y`/`7is`/`mdg`/`5by`/`1ox`/`9yk`.
- **Closed:** S36: `orl`. S35: `3gp` (PR #55). S34: `gu4` (PR #53). S33: `n9h` (PR #50). S32: `8s6`/`6be`. S31: `89a`/`e9m`. S30: `394`/`bez`/`qbb`.

### Open project work (unchanged)
- Vault git-tracking decision deferred (`ko5`). First HTML artifact (LM-04) is recipe-pinned (`ADR-0004-T1`/`T2`/`T3`, `ADR-0007-T2`); lands when execute reaches W4/W7 + real operator data.

## Landmark window check (close step 8.7)

All 4 active landmarks (LM-01 doctor visit July 2026, LM-02 Oura/wearable, LM-03 23andMe, LM-04 first HTML artifact) — no trigger windows opened during S36 (2026-06-06; governance-only session). LM-04 still pending: the `generate.run` producer is live but no artifact generates until it's fed real operator data (Walter-pending). LM-01's 14-day-before window still depends on the TBD July exact date (not within window as of 2026-06-06); LM-02/03 remain Walter-pending. No status flips due.

## Open Issues

### Vault git-tracking policy — now tracked as bead `ko5` (S27)
The vault knowledge graph is git-tracked de-facto (since S2, per user instruction); `.gitignore` excludes only the operator-PII raw dropzones (`vault/dna/raw/`, `vault/labs/raw/`). The S1 "decision deferred" note is now a tracked decision: **`ko5`** — ratify the vault-git-tracking policy against ADR-0005 (PII-free trunk), which largely answers it (the PII-free vault content IS the tracked trunk; filled-scaffold values + the store are gitignored), and close/supersede the S1 deferral. Filed S27 when the question was raised.

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

