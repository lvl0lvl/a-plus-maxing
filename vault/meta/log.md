---
title: Wiki Operation Log
type: reference
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
last_updated: 2026-05-23
depends_on: []
superseded_by: null
review_cadence: session
permalink: a-plus-maxing/meta/log
---

# Wiki Operation Log

Append-only. One line per ingest/edit/lint/export operation.
Format: `YYYY-MM-DD | op | page | note`

Ops: `create`, `update`, `link`, `lint`, `export`, `delete`, `schema`

---

- 2026-05-23 | schema | WIKI.md | initial schema established (compounds, biomarkers, protocols, parameters, decisions)
- 2026-05-23 | create | meta/index.md | initial index seeded from existing pages
- 2026-05-23 | create | meta/contradictions.md | empty log seeded
- 2026-05-23 | create | meta/log.md | this file
- 2026-05-23 | create | compounds/_template.md | compound page template
- 2026-05-23 | create | biomarkers/_template.md | biomarker page template
- 2026-05-23 | update | meta/index.md | added compound + biomarker templates
- 2026-05-23 | create | meta/operator-profile.md | slow-changing Walter context (scaffold awaiting Jan 2026 issue characterization)
- 2026-05-23 | create | meta/current-state.md | fast-changing snapshot (biomarkers, active protocols/compounds)
- 2026-05-23 | create | meta/goals.md | goal hierarchy + hard limits + doctor-handout queue
- 2026-05-23 | create | library/peptides/_source-whitelist.md | type-tagged source whitelist with admissibility matrix
- 2026-05-23 | create | library/peptides/_triage.md | peptide class taxonomy + triage scoring rubric
- 2026-05-23 | update | meta/index.md | indexed all three meta files + peptide refs
- 2026-05-23 | move | library/peptides/_source-whitelist.md → library/_source-whitelist.md | generalized from peptide-only to all health research
- 2026-05-23 | update | library/_source-whitelist.md | retitled, domain-extension pattern documented
- 2026-05-23 | update | WIKI.md | added Agent Consumers section with 14-agent roster (peptide, endocrine, lymphatic, gi, cardio, recovery, sleep, longevity, trainer, nutrition, supplement, labs, mental-perf, medical-liaison)
- 2026-05-23 | update | meta/index.md | updated whitelist path
- 2026-05-23 | create | library/peptides/bpc-157/research-report.md | deep-mode dispatch; 10,193 words; ~80 distinct citations; Sikiric-share ~76-80% across deduplicated primaries
- 2026-05-23 | create | compounds/bpc-157.md | derived compound entry; evidence_tier C; risk_tier experimental; status researching
- 2026-05-23 | update | library/peptides/_triage.md | added BPC-157 to Done queue
- 2026-05-23 | update | meta/index.md | indexed bpc-157 research-report and compound entry
- 2026-05-23 | update | compounds/_template.md | added Non-English Literature Coverage and Prescribing-Practice Layer sections (every future compound entry gets these by default)
- 2026-05-23 | update | library/_source-whitelist.md | added Tier 2.7 (Practitioner protocols), Tier NE (Non-English literature), new `practitioner_protocol` type-tag, expanded admissibility matrix
- 2026-05-23 | create | library/peptides/bpc-157/practitioner-layer.md | supplementary dispatch — Compounding Lab AU is only dose-explicit current data sheet; Edwin Lee IV outlier; consensus subQ 250-500 µg/day 4-6 wk
- 2026-05-23 | create | library/peptides/bpc-157/non-english-layer.md | supplementary dispatch — Korean antinociception primaries (Park 2021, Jung 2022), Chinese porcine Xue 2004b + clopidogrel Wu 2020, Croatian conf abstracts (psoriasis, fistula, nephrotoxicity), Pliva patent estate; zero Russian primaries; PL 14736 Phase II UC not located in any language
- 2026-05-23 | update | library/peptides/bpc-157/research-report.md | author attribution fixed [A-11] He L 2022 ← was "Xu et al."; new §7.12 (pain/nociception), §7.13 (dermatology signal), §7.14 (porcine corroboration); §11 clopidogrel interaction; §19.5 supplementary dispatch summary
- 2026-05-23 | update | compounds/bpc-157.md | added Non-English Literature Coverage + Prescribing-Practice Layer sections; updated dose with full sourcing; added clopidogrel interaction; added 3 layer pointers in Relations
- 2026-05-24 | update | library/peptides/bpc-157/research-report.md | rebuilt deep-mode via /aplus-research --update=suspect-fabrications; prior version archived at vault/library/peptides/bpc-157/_archive/2026-05-24-suspect-fabrications/research-report.md; 20,635 words refined to 1,039 lines; 52 deduplicated primaries (post #22/#32 downgrade); 6 paired retrieval+judge dispatches (3 needed iter-2 remediation, all PASS at 99/100 deep threshold); IC-13 corpus-scoping 30/30 probes PASS, zero fabrications; FIXED canonical S2 misattribution of He L 2022 (was claimed as human PK study, is rat+beagle dog only — confirmed via PMC9794587)
- 2026-05-24 | update | compounds/bpc-157.md | rebuilt from new research-report; prior archived at vault/compounds/_archive/bpc-157-2026-05-24-suspect-fabrications.md; risk_tier remains experimental; surface FDA April 22 2026 Cat 2 removal-via-nominations-withdrawal (not safety clearance)
- 2026-05-24 | update | library/peptides/bpc-157/practitioner-layer.md | rebuilt; prior archived
- 2026-05-24 | update | library/peptides/bpc-157/non-english-layer.md | rebuilt; prior archived
- 2026-05-24 | update | meta/contradictions.md | 7 new resolved entries (C1–C7) from Phase 4.75 IC-10 + Phase 4 triangulation; 1 historical (C8 = He L 2022 species misattribution caught and corrected, supersedes the 2026-05-23 Xu/He attribution resolution which only fixed authorship not species)
- 2026-05-25 | create | .claude/skills/aplus-research/lib/gate_attest.py | canonical writer for gate-3.5/4.75/6/7.5/8.5 JSONs; mechanical resistance against PF-S3-01 (orchestrator self-attestation); 12/12 smoke tests pass (9 original + 3 BUG-001 regression tests)
- 2026-05-25 | create | .claude/hooks/enforce-role-inlining.sh | PreToolUse hook on Task tool blocking role-tagged dispatches without full 11-section profile; 8/8 smoke tests pass
- 2026-05-25 | schema | .claude/skills/aplus-research/schemas/gate-{3.5,4.75,6,7.5,8.5}.schema.json | added required `attestation_chain` field with strict structure (sha256 hex-64 regex, ISO date-times); iter max bumped 3 → 4 in gate-3.5 to accommodate path-b re-dispatch
- 2026-05-25 | create | INVARIANTS.md | initial register with 11 named invariants and mechanical-verification column; 4 audit-script TODO for S5
- 2026-05-25 | create | vault/meta/landmarks.md | landmark-agnostic register (4 active LMs); explicit `status: completed` transition prevents silent-degradation-after-landmark-passes
- 2026-05-25 | update | CLAUDE.md | session start protocol expanded (read INVARIANTS, PF log, landmarks; scope contract template with binary ACs); session close protocol expanded (mandatory PF attestation, audit scripts step, landmark window check); self-recognition flags added
- 2026-05-25 | update | HANDOFF.md | Top-3 active failure modes pointer added (volatile); S4 close written
- 2026-05-25 | update | memory/process-failures.md | PF-S3-01 entry created with recurrence_count=2 (predecessor PF-S2-01); AP-ORCH-SELF-ATTEST class identifier reserved
- 2026-05-25 | create | vault/sessions/session-3.md | retroactive S3 session note (canonical fabrication catch + PF-S3-01 origin)
- 2026-05-25 | create | vault/sessions/session-4.md | S4 mechanical resistance + path-(b) re-verification + rigor framework adoption
- 2026-05-25 | update | aplus-research SKILL.md | added Hard Rule 9 (no orchestrator self-attestation of gate verdicts); added Attestation chain section documenting gate_attest.py workflow + halt-reason table + threat model
- 2026-05-25 | rebuild | BPC-157 attestation chain | all 6 gates now carry valid attestation_chain; per-section judge scores iter-4: A=100/B=100/C=100/D=99/E=99/F=100; gate_attest.py verify-chain returns clean
- 2026-05-26 | create | vault/decisions/2026-05-26-foundation-role-agent-md-location.md | retroactive ADR for foundation-role agent.md canonical-path decision (option C: skills_library canonical + .claude/agents symlink); closes Q4 documentation gap surfaced by parallel design session
- 2026-05-27 | create | design/health-edge-case-reviewer-design.md | Pass-2 Role 3 design doc Final (887 lines, 18 sections + Appendix A); inherits Role 1 §4 OUTBOUND (8 rows) + Role 2 §4.2 OUTBOUND (5 rows); §4 MIXED tri-table directionality; 26 §13 rows (25 PROPOSED + 1 REFERENCED); 32 red-team findings (22 adversarial + 10 medical-safety v1-substitute) → 27 LEGITIMATE + 1 LEGITIMATE-MODIFIED + 2 REJECTED-with-cited-evidence + 1 DUPLICATE + 1 WITHDRAWN; PF-S3-01 5th consecutive guard held
- 2026-05-28 | update | .claude/hooks/enforce-role-inlining.sh | hook v2.5 — 9th-section operational-slot synonym set (## Modes | ## Audit Protocol | ## Task Routing) replacing literal ## Modes requirement; closes bead a-plus-maxing-hca E1 class (recurrence_count=3 → mandatory structural fix per Rigor Framework Discipline 8); smoke tests 8→11/11; INVARIANTS.md INV-ROLE-INLINING Change Log row appended for S12
- 2026-05-28 | create | design/medical-safety-reviewer-design.md | Pass-2 Role 4 (medical-safety-reviewer) design doc Final (874 lines, 18 sections + Appendix A); §4 MIXED tri-table — INBOUND from Role 1 (8 rows) + Role 2 (5 rows) + Role 3 (3 rows) = 16 INBOUND + 9 OUTBOUND (Council-Mode row 9 added at synthesis per OQ-4); 27 §13 rows (1 LIVE + 2 REFERENCED-with-PROPOSED-extension + 24 PROPOSED-only); 41 red-team findings (30 adversarial + 11 medical-safety v1-substitute) → 13 LEGITIMATE + 16 LEGITIMATE-MODIFIED + 3 REJECTED-with-cited-evidence + 3 REJECTED-WITH-ADOPTION + 3 DUPLICATE; PF-S3-01 6th consecutive guard held; closes v1-substitute software-security gap for S10/S11/S12 safety-red-team slot
- 2026-05-29 | deploy | .claude/agents/health-edge-case-reviewer/ | S14 Role 3 Session B — /upgrade-agent 8-phase pipeline deployed agent.md (191 lines / 6364 cl100k tok) + library-index.md (22 lines); net-new 0/10 baseline; 3 research artifacts validated 9/10 by separate+parallel fact-checker/judge (R3 1 remediation); Phase-6 adversarial 9 findings dispositioned; /review-pr 6 findings → 4 LEGITIMATE fixed+blind-verified + 1 DEFERRED (7is) + 1 NOT_A_BUG; sub-out QA drafter slot → health-edge-case-reviewer; PR #2 rebase-merged to main (clean per-session branch off origin/main, Option A); Session B debt 2→1; beads p47/o9y/7is filed (frozen-design-doc defects); PF-S3-01 8th consecutive guard held; PF-S13-01 + PF-S12-01 falsification windows HELD
- 2026-05-29 | deploy | .claude/agents/medical-safety-reviewer/ | S15 Role 4 Session B — /upgrade-agent 8-phase pipeline deployed agent.md (198 lines / 8021 cl100k tok) + library-index.md; net-new 0/10 baseline; 3 research artifacts validated 9/10 by separate+parallel fact-checker/judge (R3 1 remediation); Phase-6 adversarial 8 findings dispositioned; AC0 closed bead 4ej (XR-002: Role 1 §13 row 15 DEPLOY_WITH_OVERRIDE_PATH→BLOCK_WITH_OVERRIDE_PATH); sub-out safety-red-team slot → medical-safety-reviewer; /review-pr 6 findings → 2 LEGITIMATE fixed+blind-verified + 2 NOT_A_BUG + 2 beaded (dcy/1rm frozen-design-doc defects); PR #3 rebase-merged to main (clean per-session branch off origin/main, Option A); Session B debt 1→0 — FOUNDATION PIPELINE COMPLETE (4/4 roles deployed+incorporated); PF-S3-01 guard held; PF-S13-01 + PF-S12-01 falsification windows HELD (PF-S12-01 loop now closed)
