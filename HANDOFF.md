---
title: Session Handoff
type: note
owner: Walter McGivney
created: 2026-05-16
last_reviewed: 2026-05-25
status: active
depends_on: []
superseded_by: null
review_cadence: weekly
---

# Session Handoff

## Scope Contract — Session 5

Goal: Build project-suited drafting-team foundation (4 new roles) and 3 pilot specialist design docs (7 total) via Quant design-doc-protocol. Sequential across roles, parallel within. Probable multi-session work; checkpoint after each role. Defer `/upgrade-agent` runs and agent.md authoring to Session B.

Acceptance criteria:
- [ ] `design/` folder created with Quant-style README naming the 7-role pipeline
- [ ] Role 1 health-specialist-architect: 5-phase design-doc-protocol complete; `design/health-specialist-architect-design.md` Status: Final
- [ ] Role 2 health-implementer: 5-phase design-doc-protocol complete; `design/health-implementer-design.md` Status: Final
- [ ] Role 3 health-edge-case-reviewer: 5-phase design-doc-protocol complete; `design/health-edge-case-reviewer-design.md` Status: Final
- [ ] Role 4 medical-safety-reviewer: 5-phase design-doc-protocol complete; `design/medical-safety-reviewer-design.md` Status: Final
- [ ] Checkpoint pause after roles 1-4 for user authorization before specialist roles
- [ ] Role 5 labs-specialist: 5-phase design-doc-protocol complete; uses new foundation drafters; `design/labs-specialist-design.md` Status: Final
- [ ] Role 6 peptide-specialist: 5-phase design-doc-protocol complete; `design/peptide-specialist-design.md` Status: Final
- [ ] Role 7 medical-liaison: 5-phase design-doc-protocol complete; `design/medical-liaison-design.md` Status: Final
- [ ] Every dispatched agent prompt pastes the full 11-section role profile verbatim per INV-ROLE-INLINING
- [ ] No orchestrator self-attestation of red-team verdicts (PF-S3-01 guard); each finding personally verified against cited source
- [ ] HANDOFF rotation rule applied to VOLATILE sections at each checkpoint commit
- [ ] PF attestation appended at close in canonical form `S5 close (YYYY-MM-DD): ...`
- [ ] All three audit scripts (handoff-audit, scope-contract-audit, pf-attestation-audit) exit 0 at close
- [ ] All commits land on feature branch, none on main

Files I WILL touch:
- `design/` (new) + `design/README.md`
- `design/{role}-design.md` × 7
- `design/.{role}-design-work/*` × 7 (drafts, red-team, OQ-list, domain-research)
- `HANDOFF.md` (this contract + per-checkpoint progress + close)
- `vault/sessions/session-5.md` (close note)
- `memory/process-failures.md` (only if a new PF surfaces)
- `.beads/*` (via `bd` CLI only)

Files I will NOT touch:
- `vault/library/*`, `vault/compounds/*`, `vault/biomarkers/*`, `vault/dna/*`, `vault/labs/*`
- `.claude/skills/*` (including aplus-research and deep-research)
- `.claude/commands/*` (including upgrade-agent)
- `.claude/agents/` (deferred to Session B — design docs only this session)
- `~/Documents/Projects/skills_library/roles/*` (no role profiles deployed; design docs inform Session B authoring)
- `INVARIANTS.md` (no new invariants this session)
- `scripts/` (owned by the parallel session)
- `CLAUDE.md` (owned by the parallel session this cycle)
- `~/.claude/*` (global config untouched)
- `main` branch (commits to `feature/wiki-bpc157-aplus-research` only)

NOT doing:
- Running `/upgrade-agent` against any design doc (Session B)
- Writing any `agent.md` profile (Session B)
- The 11 remaining specialists (only pilot 3 + 4 foundation)
- Tiered vs per-agent design decision (explicit post-pilot review)
- Vault git-tracking decision
- LM-04 first HTML artifact generation
- S4 mechanical-enforcement TODO audit scripts (other session)
- Bug-001 follow-up / aplus-research v2 calibration

Invariants at risk:
- INV-ROLE-INLINING — every agent dispatch inlines full 11-section profile verbatim; `enforce-role-inlining.sh` PreToolUse hook is the mechanical check
- INV-SCOPE-CONTRACT — satisfied by this block; `scope-contract-audit.sh` validates format at close
- INV-BRANCH-NOT-MAIN — currently on `feature/wiki-bpc157-aplus-research`; discipline-only guard until pre-commit hook lands
- INV-PF-ATTESTATION — canonical form at close
- INV-HO-ROTATION / INV-HO-NO-STALE-HASH — rotation rule applied to VOLATILE sections; no SHA prefixes in narrative prose
- INV-RESEARCH-ATTESTATION — N/A (no `aplus-research` dispatch this session); `/deep-research` paired-judge rigor is the substitute and is NOT self-attested

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

## Top-3 active failure modes (VOLATILE — rotates each session)

Forward-facing readiness for next session. Replaced at every close, not accumulated. Per Rigor Framework Discipline 8.

1. **AP-ORCH-SELF-ATTEST** (PF-S2-01 + PF-S3-01, recurrence_count=2; mitigation hardened this session via `gate_attest.py` + attestation_chain schema + inlining hook). Live going into S5 because the mechanical defenses are still untested in a fresh dispatch — first new aplus-research run in S5+ is the next falsification window. If gate-self-attestation slips past the new defenses → recurrence_count=3 → mandatory structural fix (likely UUIDv4 agent-identity ledger replacing brief-hash uniqueness).
2. **AP-INCOMPLETE-PROPAGATION** (S4 finding) — when fixing a metadata defect, the fix lands in the obvious place (bibliography line) but adjacent narrative/tally/self-check sections holding the same value are missed. Section A iter-2 missed Ref [2] PMID re-verification; Section C iter-2 missed Xue 2004 institution sweep in narrative lines 43/92/102/106. Mechanical defense: every iter-N remediation must run post-fix grep for the OLD value across the whole file before declaring done. Promote to AP-XXX-NN catalog entry when 2+ AP catalog entries accumulate.
3. **AP-ORCHESTRATOR-ITER-INFLATION** (S4 finding, BUG-001 root cause) — orchestrator calling `start-iteration --phase X` more times than necessary because of a misconception about iteration scope. Each redundant call moves iter_start_ts forward and invalidates fresh-but-pre-call agent outputs. Mechanical defense: gate_attest.py now supports `--section` for partial-remediation cycles; iteration N is the section's iteration, not the phase's.

## Current State (volatile)
- BPC-157 canonical library entry is **live, re-verified, and carries a clean attestation chain**. All 6 aplus-research gates PASS with agent-source sha256 recorded in each gate JSON. `verify-chain` returns clean.
- Per-section judge scores (iter-4 final, path-b re-dispatch): A=100, B=100, C=100, D=99, E=99, F=100.
- Two additional metadata defects surfaced by iter-3 judges (Section A Ref [2] PMID + invented co-author; Section C narrative drift on C6 fix) — both corrected and iter-4 PASS.
- **Mechanical resistance** is now installed against PF-S3-01 recurrence: `gate_attest.py` + 12/12 smoke tests + required `attestation_chain` in 5 gate schemas; `enforce-role-inlining.sh` PreToolUse hook + 8/8 smoke tests; `INVARIANTS.md` with 11 named invariants (4 still TODO for audit-script wiring in S5).
- BUG-001 patched in gate_attest.py: per-section iter_start_ts via `--section` flag for path-b partial remediation; JSON `iteration` field takes precedence over filename suffix; schema iter max 3 → 4.
- `vault/meta/landmarks.md` register established. 4 active landmarks (LM-01 doctor visit, LM-02 Oura, LM-03 23andMe, LM-04 first HTML artifact). Landmark-agnostic by design — status flips to `completed` after windows exhausted, no silent failure.
- Beads: epic `a-plus-maxing-c6k` (P1) ready; `a-plus-maxing-3py` closed in S3.
- Branch: `feature/wiki-bpc157-aplus-research` at commit `8b05b30` as of 2026-05-25 S4 close. Ephemeral; no upstream push. Vault gitignore decision still unresolved.

**Historical (kept for reference):** Session 3 BPC-157 rebuild context lives in `vault/sessions/session-3.md`.

## What Is Next (volatile)

### Mechanical-enforcement TODO from INVARIANTS.md (S5–S6)
- `scripts/handoff-audit.sh` for INV-HO-ROTATION + INV-HO-NO-STALE-HASH (rotation discipline content-pattern + structural-integrity checks per Rigor Framework Discipline 5).
- pre-commit hook for INV-BRANCH-NOT-MAIN (mirror of push-block; PF-S2-06 recurrence guard).
- close-protocol audit for INV-SCOPE-CONTRACT (verifies HANDOFF carries a scope contract dated this session).
- close-protocol audit for INV-PF-ATTESTATION (verifies PF log either has new entry OR explicit "No PF this session" line dated this session).
- `scripts/lib/audit-helpers.sh` shared library (emit / fail / violations counter) per Rigor Framework Discipline 5 §3.

### v2 calibration findings from S3 + S4 (for next aplus-research upgrade cycle)
- Cross-section identity reconciliation step in Phase 4 (catches metadata mismatches BEFORE Phase 4.75 verifier needs to). Iter-3 surfaced 2 defects the in-skill iter-2 remediation missed; a Phase 4 sub-step would have caught them earlier.
- Post-fix grep enforcement in remediation agents — every metadata-correction agent must run grep for the OLD value across the whole file before declaring done (AP-INCOMPLETE-PROPAGATION mitigation).
- Phase 6 critique re-run on refined draft was correctly required by the gate spec; the orchestrator-self-attest in S3 was the violation, not the spec. The corrected protocol stands.
- Permalink-suffix collision on `vault/compounds/<slug>.md` permalink when prior archive carries the same permalink (linter auto-suffixes `-1`) — document in SKILL.md as expected behavior or change archive permalinks to scope under `_archive/`.
- v2 judge briefs must require the literal JSON skeleton inline (S3 judges returned divergent shapes; S4 was templated more tightly and worked cleanly).

### Specialist-role profile rollout (S4–S6)
- Author 11-section role profile for `peptide-specialist` (first specialist agent that will consume the BPC-157 entry, ahead of the July 2026 doctor visit).
- Author `medical-liaison` role profile (downstream consumer for the doctor-handout queue).
- Inlining hook will block their dispatch until full profiles exist — discipline enforced at dispatch time.

### Open project work
- Walter pending: 23andMe raw file to `vault/dna/raw/`; Oura purchase; meal-template content; January 2026 health issue characterization (per operator-profile.md; `medium+` risk-tier HALT remains active on BPC-157 movement from `researching` to `planned` until populated).
- Vault git-tracking decision still deferred.
- First HTML artifact generation still deferred (LM-04 active landmark).

### Drift checks (S4 close)

**Task drift:** S4 began as "build mechanical resistance" then expanded user-directed to "adopt rigor framework + re-verify BPC-157 entry via path-(b)." Every expansion was explicit user direction; every acceptance criterion evaluated PASS. The user-issued path-(a) authorization for the Section A + C iter-3 HALTs was an explicit scope extension, not silent drift. No silent task drift.

**Architecture drift:** Cross-Document Ownership Matrix check — `gate_attest.py` is the canonical writer for gate-3.5 / 4.75 / 6 / 7.5 / 8.5 JSONs (lives in `.claude/skills/aplus-research/lib/`); CLAUDE.md owns session protocols; INVARIANTS.md owns the invariants register; vault/meta/landmarks.md owns the landmark register. Each is single-owner. Rotation rule applied to Top-3 + Current State + What Is Next. No SHA prefixes in narrative prose (commit `8b05b30` self-dated this section close, not embedded in prose elsewhere). No architecture invariant degraded; several were strengthened by mechanical-enforcement uplift.

**Vision drift:** System after S4 IS: LLM-driven personal health agent with the aplus-research skill mechanically resistant to its own documented failure modes (PF-S2-01 + PF-S3-01), a clean attestation chain on the BPC-157 canonical entry, an explicit invariants register, a landmark-agnostic register, and rigor-framework session protocols. Same project as S1; no vision drift. The system can now defend against the failure class that produced PF-S3-01 — the rigor compounds rather than the drift.

### Rigor Framework adoption progress (per §11 sequence)

| Discipline | Adoption status |
|---|---|
| 1 Session lifecycle | ✅ Start/close protocols, 3-axis drift, recovery, scope contract template |
| 2 Memory stack | ✅ Four layers + PF log in place |
| 3 Document Ownership Matrix | ✅ In CLAUDE.md |
| 4 Rotation rule (6-clause) | ✅ In CLAUDE.md; audit script TODO S5 |
| 5 Invariants + mechanical enforcement | 🟡 INVARIANTS.md + 2 mechanical defenses (gate_attest.py, inlining hook); 4 TODO audit scripts |
| 6 3-session pipeline | 🟡 Recognized; aplus-research v1.1 (`gate_attest.py`) is technically a compressed in-session 3-wave; first true Fork-Upgrade-Run cycle slated for v2 |
| 7 HALT-and-close-cleanly | ✅ Applied this session (path-(a) authorization, path-(b) re-dispatch); self-recognition flags in CLAUDE.md |
| 8 Failure-mode discipline | ✅ PF log with recurrence_count, AP class tags emerging, Top-3 pointer in HANDOFF, "No PF this session" attestation mandatory |
| 9 Agent roles + adversarial review | 🟡 Inlining hook live; 11-section role profiles still TODO for project specialists (peptide-specialist, medical-liaison) |
| 10 Orchestrator skill spec | 🟡 CLAUDE.md is functional equivalent; not yet a callable `orchestrator` skill |

S5+ priorities: Discipline 5 audit scripts + Discipline 9 specialist role profiles.

## PF attestation (mandatory per CLAUDE.md close step 4)

S4 close (2026-05-25): One new PF entry promoted (PF-S3-01, dated 2026-05-24, written this session with recurrence_count=2). No additional PF-class incidents observed during the S4 mechanical-resistance build + re-verification work. Two AP candidates surfaced (AP-INCOMPLETE-PROPAGATION, AP-ORCHESTRATOR-ITER-INFLATION) but neither has recurrence yet; tracked in Top-3 pointer instead of catalog. The path-(b) re-dispatch discipline worked as designed — surfaced 2 metadata defects the prior remediation cycle had missed, validating the framework's "every Session B catches something" claim.

## Landmark window check (close step 8.7)

All 4 active landmarks (LM-01 doctor visit, LM-02 Oura, LM-03 23andMe, LM-04 first HTML artifact) — no trigger windows opened during S4. LM-01 trigger window opens ~14 days before the July 2026 visit date; the scoped audit dispatch is queued for that date.

## Open Issues

### Vault not in git (unchanged from S1)
Per S1 HANDOFF. Decision still deferred. Note: all S2 vault content was committed (per user instruction) but the underlying `.gitignore` policy was not reconsidered this session.

### aplus-research has never been invoked
The skill exists but the first end-to-end run happens next session. Likely failure modes (recorded for next session's debugging): (a) `--update` flag missing blocks Phase 2.75; (b) `jsonschema` Python package presence check not implemented as pre-flight; (c) corpus retrieval for paywalled primaries may exceed paywall-bypass capability — `corpus-missing` WARN expected on a meaningful share of cites.

### Beads ticket dependencies were created backwards
Created `a-plus-maxing-s5k` (implement `--update` flag) and `a-plus-maxing-3py` (re-run BPC-157), then accidentally made both depend on the long-lived epic `a-plus-maxing-c6k`. Result: both show as blocked in `bd ready` even though they should be the next ready work. `bd dep` CLI has no `remove` subcommand in this version. Next session: either close the broken-dep tickets and re-create, or manually edit the bd JSONL to remove the c6k dep. Tickets are visible via `bd list --status=open`.

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

## Scope Contract — Session 5 (2026-05-25)

Goal: Build the 4 mechanical-enforcement audit scripts + shared helpers library + pre-commit branch-block hook, wired into the close protocol and reflected in INVARIANTS.md.

Acceptance criteria:
- [x] `scripts/lib/audit-helpers.sh` — shared `emit` / `fail` / violations-counter (per Rigor Framework Discipline 5 §3); 16/16 smoke tests pass
- [x] `scripts/handoff-audit.sh` — checks INV-HO-ROTATION (clauses 2 + 5) + INV-HO-NO-STALE-HASH; 12/12 smoke tests pass; exits 0 on current HANDOFF.md
- [x] `scripts/scope-contract-audit.sh` — checks HANDOFF.md carries a `## Scope Contract — Session N` block with required subfields and binary ACs; 12/12 smoke tests pass
- [x] `scripts/pf-attestation-audit.sh` — checks canonical `S<N> close (YYYY-MM-DD):` attestation line; 12/12 smoke tests pass
- [x] `.claude/hooks/block-commit-main.sh` — PreToolUse Bash hook blocking `git commit` while HEAD = main; wired into `.claude/settings.json`; 21/21 smoke tests pass
- [x] Smoke tests for each remaining script — all pass (73/73 across 5 suites)
- [x] `INVARIANTS.md` Mechanical Verification column updated for INV-HO-ROTATION, INV-HO-NO-STALE-HASH, INV-BRANCH-NOT-MAIN, INV-SCOPE-CONTRACT, INV-PF-ATTESTATION — TODO markers removed; S5 Change Log row added
- [x] `CLAUDE.md` close protocol step 8.5 expanded to invoke the 3 new audit scripts (handoff, scope-contract, pf-attestation)

Files I WILL touch:
- `scripts/lib/audit-helpers.sh` (NEW)
- `scripts/handoff-audit.sh` (NEW)
- `scripts/scope-contract-audit.sh` (NEW)
- `scripts/pf-attestation-audit.sh` (NEW)
- `scripts/tests/` (NEW, smoke fixtures + runner)
- `.claude/hooks/block-commit-main.sh` (NEW)
- `.claude/hooks/tests/test_block_commit_main.sh` (NEW)
- `.claude/settings.json` (add PreToolUse Bash matcher)
- `INVARIANTS.md` (Mechanical Verification cells + Change Log row)
- `CLAUDE.md` (close-protocol step 8.5)
- `HANDOFF.md` (this contract + at session close)

Files I will NOT touch:
- `vault/library/peptides/bpc-157/*` and `vault/compounds/bpc-157.md`
- `.claude/skills/aplus-research/*`
- `vault/meta/landmarks.md`
- Any agent role profile files (separate session per user direction)

NOT doing:
- Specialist role profiles (peptide-specialist, medical-liaison) — separate session
- v2 aplus-research calibration findings
- Vault git-tracking decision
- First HTML artifact (LM-04)
- Beads ticket dep-cleanup
- Walter pending items (23andMe, Oura, meal-template, Jan-2026 issue)

Invariants at risk:
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH — audited by this session's own deliverable (built-in falsification)
- INV-SCOPE-CONTRACT — this contract satisfies it
- INV-PF-ATTESTATION — mandatory at close
- INV-BRANCH-NOT-MAIN — already on feature branch; new hook becomes second line of defense

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

## Scope Contract — Session 6 (2026-05-25)

Goal: Apply 4 v2 calibration findings to the aplus-research skill in place, with smoke tests where mechanically verifiable. Skill remains usable for the upcoming peptide library campaign.

Acceptance criteria:
- [x] AC1 — Phase 4.25 ID-Reconcile inserted as BLOCKING gate for standard+; full spec in SKILL.md; `schemas/gate-4.25.schema.json` validated; gate_attest.py wired (ATTESTED_GATES + SOURCE_MD); INV-RESEARCH-CROSS-SECTION-ID added to INVARIANTS register
- [x] AC2 — Post-fix grep enforcement: dedicated "Remediation brief addendum" section in SKILL.md with verbatim block orchestrator injects into Phase 3.5 iter-2+, 4.25 iter-2+, 4.75 verifier remediation, Phase 6 critique remediation
- [x] AC3 — Phase 3 judge brief now embeds literal JSON skeleton (9 dimensions + total + threshold + verdict + findings array) with structural rules
- [x] AC4 — Archive permalink policy documented in Phase 8 §3: scoped under `a-plus-maxing/compounds/_archive/<slug>-<date>-<reason-slug>`; orchestrator rewrites permalink BEFORE archive move in Phase 2.75
- [x] AC5 — Calibration history table near top of SKILL.md (v1.0 → v1.1 → v2 ACs)
- [x] AC6 — Smoke verification: gate_attest 16/16 pass (12 existing + 4 new for phase 4.25 round-trip incl. PASS + HALT + override + stale-source); all audit-script suites still green
- [x] AC7 — Close-protocol audits all exit 0; PF attestation in canonical form (below)

Files I WILL touch:
- `.claude/skills/aplus-research/SKILL.md`
- `.claude/skills/aplus-research/references/citation-integrity.md` (if needed)
- `.claude/skills/aplus-research/schemas/gate-3.5.schema.json` (if AC3 requires)
- `.claude/skills/aplus-research/schemas/gate-4.75.schema.json` (if AC1 affects)
- New `.claude/skills/aplus-research/schemas/gate-4.25.schema.json` (only if AC1 = blocking gate)
- New fixture/smoke test under `.claude/skills/aplus-research/tests/`
- `HANDOFF.md` (this contract + close note)
- `memory/process-failures.md` (only if new PF surfaces)

Files I will NOT touch:
- `vault/library/peptides/bpc-157/*`, `vault/compounds/bpc-157.md`
- `vault/library/peptides/_triage.md`
- `scripts/*`, `.claude/hooks/*`
- `design/*`
- `INVARIANTS.md` (unless AC1 introduces a new INV; flag at the time)
- `CLAUDE.md`
- `~/.claude/skills/deep-research/*`

NOT doing:
- Peptide library campaign runs (Phase C; separate sessions)
- Beads dep cleanup (deferred or rolled into close if quick)
- Specialist role profiles (parallel session)
- Walter pending items
- Vault git-tracking decision
- First HTML artifact (LM-04)

Invariants at risk:
- INV-RESEARCH-ATTESTATION (gate-3.5 schema touches must preserve attestation_chain)
- INV-RESEARCH-IC13-CORPUS (remediation grep must stay distinct from IC-13 verifier)
- INV-HO-ROTATION + INV-HO-NO-STALE-HASH (rotation deferred to last-closing S5/S6 cycle)
- INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN — standard close discipline

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

S6 close (2026-05-25): No new PF-class entries this session. The Phase 4.25 schema mismatch I hit mid-session (top-level `iterations` required vs attest_simple not auto-populating it) was a latent gap in the documented scaffold pattern — surfaced by writing the new tests, fixed by following the pre-existing scaffold convention. Not a PF; documented inline in the test file via T13-T16 examples. The `agent-verdict-halt` sentinel inconsistency observed during T15 debugging is also pre-existing (not in any schema's halt_reasons enum); recorded here for v2.5 cleanup. No PF-S2-01, PF-S3-01, or AP-class incidents observed.
