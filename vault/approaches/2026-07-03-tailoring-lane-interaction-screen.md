---
name: tailoring-lane-interaction-screen
type: approach
status: abandoned
session: S105
date: 2026-07-03
supersedes: none
tags:
- tailoring
- interaction-screen
- crown-jewel
- adr-0037
permalink: a-plus-maxing/approaches/2026-07-03-tailoring-lane-interaction-screen
---

# A drug×supplement×peptide interaction screen in the care-lane tailoring pass

**What was tried:** ADR-0037 premised the tailoring pass as "the ONLY place a raw drug×supplement×peptide interaction check can run (the de-id specialists structurally cannot)." ADR-0037-T2 built it: `tailoring._interaction_referral` intersecting `router.rx_interaction_class_set(profile)` with the compound's additive-AE classes (read from the recorded plan's `ae_profile` extra), fail-closed to a "see your doctor" referral.

**Why abandoned:** RETIRED (Architect binding ruling, feature/dyn-loop-w6). Two verified facts: (1) DORMANT — `ae_profile` lives in the author candidate's `meta` (`generate_plan.py:375`), a sibling of `candidate["plan"]`; `record_plan` persists ONLY the plan value, so a production-recorded compound plan carries no `ae_profile` → the screen ALWAYS returns "" in production (it fired only on a test that hand-injected `ae_profile`, a shape production never records — a tautological fixture, PF-S105-01). (2) REDUNDANT — it uses the SAME de-identified class basis + the SAME `orchestrate._rx_bpmh_matched_classes` function as the PRIMARY reconciler BPMH screen (`orchestrate.reconcile` behavior 5), which runs at generate-time and HOLDS a matching compound → held domain records no plan → tailoring's emit-gate excludes it. The tailoring screen's would-fire set is a SUBSET of the primary's already-held set. The ADR premise was FALSE: the implementation uses the de-id class basis, not a raw check. The one divergent case (a liaison-OVERRIDE clearance) is already surfaced via the doctor-visit queue; re-warning on it is tailoring second-guessing a medical adjudication (the presentation-not-authoring violation ADR-0037's own Alternative C rejects).

**What would change the verdict:** A genuine RAW check the de-id primary structurally cannot express (a specific drug×compound pair with no shared curated class) would be a NEW ADR naming a new raw-egress computation, evaluated on its own terms — NOT a silent revival of this dormant class-intersection screen. If ADR-0034's curated `rx-interaction-classes` coverage is found materially incomplete, the fix is CURATION (strengthens the primary), not a parallel tailoring-lane lookup.

**Cross-references:**
- Architect ruling (feature/dyn-loop-w6); ADR-0037 §3 retirement amendment
- PF-S105-01 (tautological-fixture masking); bead `qiob`
- PR #282 (wave-6: screen retired, dosing-reject kept)