---
title: Phase 3 Watch List — Substrate-Unaddressed Gaps
type: phase-tracking
created: 2026-05-27
session: S10
status: active
purpose: Track 4 gaps surfaced by Phase 2 substrate-sufficiency review but NOT addressed in Pass-1 substrate. Phase 3 red-team should surface these if they are real defects in the design doc. If Phase 3 does NOT surface them, they become candidate follow-up beads.
---

# Phase 3 Watch List

After Phase 2 synthesis, the orchestrator reviewed `domain-research.md` sufficiency. Substrate cleared deep-mode rigor (13,876 words, 68 sources, iter-3 99-100/100 ACCEPT). Three gaps were resolved during synthesis from architectural reasoning. Four remain unaddressed and are watched here for Phase 3 surfacing.

## Watched gaps

### WG-1 — Specialist-Pass-1-fallback discipline
**Defect surface.** Template line 32 says "specialist design docs follow this template too, with the §3 specialist-fallback content path until their own Pass-1 lands in Pass-3." Substrate assumes implementer has a Pass-1 substrate. Reality: 14 specialists have NO Pass-1 yet. The implementer's process step 1 ("read inputs including Pass-1 deliverable") may have nothing to read for specialist authoring during Session B before Pass-3 lands.

**Surfaces in Role 2 design doc?** Implicitly via §17.2 A-4 ("14-specialist roster stable through Role 2's batch authoring") but not explicitly named.

**Expected Phase 3 finding shape.** Adversarial reviewer should flag: "Role 2 §10.1 auto-loads `domain-research.md` for the role being designed; the 14 specialists have no Pass-1 substrate; the implementer's auto-load is undefined for specialist authoring."

**If NOT surfaced** → bead F-WG1: clarify §10.1 auto-load behavior when Pass-1 substrate absent.

### WG-2 — library-index.md authoring spec for specialists
**Defect surface.** Role 1 deployed with a paired `library-index.md` (24 lines, 5 conditional refs). Spec for whether and how the implementer authors a per-specialist library-index.md is not in substrate; not in design doc; not in Role 1's §13.

**Surfaces in Role 2 design doc?** Not addressed. §8.1 mentions "library-index.md (if the architect's template variant requires it)" but does not commit either way.

**Expected Phase 3 finding shape.** Contracts/architect reviewer should flag: "Role 1 has library-index.md but Role 2 §8.1 hedges; either commit the library-index.md authoring to implementer ownership OR escalate via Architecture Question OR explicitly defer."

**If NOT surfaced** → bead F-WG2: amend §2.2 owned-items list to include library-index.md OR file an Architecture Question.

### WG-3 — aplus-research target_class enumeration per specialist
**Defect surface.** R12 covers `--mode` floor per specialist. It does NOT cover `target_class` enumeration (peptide vs supplement vs biomarker vs protocol — see aplus-research SKILL.md §1.2). Implementer's DIFFER block (§4.2 row 5) names "per-role mode floor" but the target_class enumeration is implicit.

**Surfaces in Role 2 design doc?** §13 row 12 audits mode-floor presence; no row audits target_class declaration. EC-3 covers WIKI.md row "Dispatches research on: none" but not the target_class field shape.

**Expected Phase 3 finding shape.** Adversarial/QA reviewer should flag: "§13 row 12 audits `--mode` only; SPECIALIST profiles also need a target_class declaration to invoke aplus-research correctly; either add row 12.6 or escalate."

**If NOT surfaced** → bead F-WG3: add §13 row for target_class declaration audit OR escalate via Architecture Question.

### WG-4 — Operator-profile field enumeration per specialist class
**Defect surface.** EC-6 covers operator-profile schema-drift detection (row 6.6). EC-6 does NOT specify which operator-profile fields each specialist class is expected to read. The "DIFFER set" item "Operator-profile fields read" (§4.2 INBOUND row 5 inherited from Role 1 + §10.3) is conceptual but does not enumerate per-role.

**Surfaces in Role 2 design doc?** No. Operator-profile is named as NOT-auto-loaded by implementer; field enumeration is left to specialist-authoring time.

**Expected Phase 3 finding shape.** Contracts reviewer should flag: "Role 2 §10.3 names operator-profile as specialist-not-implementer load; but does not specify the per-specialist-class field enumeration (e.g., cardiovascular-specialist reads `medications + allergies + cardiovascular_history`; sleep-coach reads `sleep_baseline + caffeine_intake`). Without enumeration, specialists may diverge silently."

**If NOT surfaced** → bead F-WG4: amend §10 with a per-specialist-class field enumeration table OR escalate via Architecture Question.

## Resolution at Phase 4

After Phase 3 red-team produces `red-team-{adversarial,safety}.md`:

1. Search both red-team outputs for findings touching WG-1, WG-2, WG-3, WG-4.
2. For each watched gap, mark `SURFACED: <finding-id>` or `NOT_SURFACED`.
3. NOT_SURFACED gaps become beads at session close per user directive.
4. SURFACED gaps fold into Phase 4 classification per PF-S3-01-guarded personal source-read.

## Reference

- Substrate sufficiency assessment was performed by orchestrator before Phase 3 dispatch.
- Three other gaps surfaced by sufficiency review were resolved during Phase 2 synthesis itself (per-specialist dispatch handoff per Insight 7; project-local placement per S9 precedent; upstream-defect escalation via EC-11). They are NOT watched here.
