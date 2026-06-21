# Gate 6 — CRITIQUE (red-team) — Retatrutide research-report

Adversarial review of `vault/library/peptides/retatrutide/research-report.md` against the six required defect axes. I did not write this draft.

## Prose critique

**1. INVESTIGATIONAL discipline (the #1 axis) — HOLDS.**
The not-approved / Phase-2-only framing is enforced redundantly and correctly: YAML (`status: researching`, `evidence_tier: B`, `risk_tier: experimental`), the metadata block, the "Read this first" callout, the TL;DR, and banners at the head of §2 ("Phase 2 — investigational, not confirmed"), §3 ("DEFINING INTEGRITY FRAME … NO marketing approval"), §5, and §8. The headline −24.2% is never stated without the dual qualifier (Phase 2 + not approved) attached at every occurrence (metadata, Read-first, TL;DR, §2.1, §2.3). Crucially, the TRIUMPH Phase-3 toplines (28.3% at 12mg / TRIUMPH-1; 28.7% / TRIUMPH-4) are explicitly fenced as "sponsor TOPLINE PRESS RELEASE … not peer-reviewed … must NOT be treated as verified efficacy," bibliography tier=3, and excluded from verified numbers (§3.3, §7, provenance note). No Phase-2 or press-release figure reads as established or approved. No defect.

**2. Triple mechanism distinct from tirzepatide/semaglutide — HOLDS, correct.**
GIP + GLP-1 + glucagon (GCGR) triple agonism is stated accurately and the glucagon arm is correctly identified as the defining differentiator vs tirzepatide (dual GIP/GLP-1) and semaglutide (GLP-1-only) — §1.1, §1.4, §1.7 enumerated contrast, §2.2, TL;DR. The energy-expenditure / hepatic-fat-oxidation attribution to GCGR is honestly flagged in §1.8 as resting on mechanism review + mouse data, not a human dismantling study. The glucagon-raises-glucose hazard and the insulinotropic offset are handled correctly (§1.4, §5.2). No defect.

**3. Citation integrity (the tirzepatide lesson) — HOLDS, mechanically verified.**
I grepped every inline `[n]` token: all of [1]–[22] appear in the body (counts 4–93 each) and every one resolves to exactly one `## Bibliography` entry. All 22 bibliography entries are defined exactly once. NO dangling tokens, NO section-local collisions, NO duplicate definitions. The bib lists [4] before [3] (grouped by category, not numerically) — cosmetic ordering only, not a defect. A crosswalk table and provenance note document the A–F dedup (Jastreboff A[3]=B[1]=D[1]=F[1]/[2]→[3]; Sanyal→[5]; etc.). Spot-checks pass: ~24.2% at 48wk/12mg → Jastreboff 2023 [3] (PMID 37366315); MASH/liver-fat −86% at 48wk → Sanyal 2024 [5] (PMID 38858523). This is the clean inverse of the tirzepatide failure.

**4. Safety honesty — HOLDS.**
The glucagon heart-rate increase is grounded in the Tier-1 Jastreboff trial (dose-dependent rise + week-24 peak) and the report explicitly DROPPED the secondary SeekPeptides ~5–10 bpm magnitude (section D[5], anecdote_aggregate) as non-Tier-1 — confirmed against section-D.md line 21/63 where that vendor bpm figure existed and was correctly excluded (§5.2, §5.7, provenance note). Cutaneous hyperesthesia 7% vs 1% placebo with dose-dependent breakdown (§5.3) matches source. Transient eGFR dip → recovery/net improvement by 48wk with CIs (§5.3) matches Heerspink 2025 [12]. C-cell explicitly class-extrapolated, not measured (§5.4). No long-term, CV-outcome, or human thyroid claims are made; CV/renal hard outcomes correctly deferred to TRIUMPH-Outcomes (~2029). No defect.

**5. Regulatory — HOLDS.**
NOT approved anywhere (§6.1, enumerated FDA/EMA/other/no-marketed-product). Gray-market premature caution is appropriately strong and grounded in FDA enforcement + documented sterility failures, not overstated (§6.3, §8.2). WADA correctly NOT prohibited: 2026 Prohibited List S4.4 absence verified, and the 2026 Monitoring Program correctly limited to "Markers of Semaglutide and Tirzepatide" with the explicit note that retatrutide is not individually named and that monitoring ≠ prohibition (§6.4). FDA Fast Track correctly reported as UNVERIFIED rather than asserted (§3.4, §6.2). No defect.

**6. No Wikipedia / population annotation / tier defensibility / no contradictions — HOLDS.**
No Wikipedia source appears in the corpus or bibliography (asserted and confirmed by inspection). Every population is annotated (obesity-no-T2D Phase 2; T2D Phase 2; MASLD Phase 2a; CVD/CKD CVOT). Tier B / experimental is defensible and transparently argued in §7 (high design quality but early-phase, single-sponsor, pre-Phase-3-publication). I checked for contradictions across the eGFR ("transient decrease" vs "net improvement" — reconciled correctly as dip-then-recovery), the glucagon-glucose ("theoretical hyperglycemia" vs "HbA1c fell" — reconciled via insulinotropic offset), and the cross-class comparison (correctly flagged indirect/cross-trial, not head-to-head). No internal contradictions found.

**Minor observations (NOT defects, no action required):**
- §3.2 lists TRIUMPH-1 as "Completed" while §6.1 example uses TRIUMPH-3 as "Active, not recruiting" — these are different trials at different stages, not a contradiction.
- The 100% single-sponsor concentration is appropriately framed as a corpus-level characterization, not a formal bibliometric audit (§4.1).

## Verdict

verdict: PASS

```json
{"phase":"6","critique_agent_id":"critique-reta-i1","draft_path":"vault/library/peptides/retatrutide/research-report.md","findings":[],"additional_retrievals":[],"halt_reasons":[],"iterations":1,"verdict":"PASS"}
```
