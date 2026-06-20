# Gate 6 — Phase 6 CRITIQUE (red-team) — MK-677 (Ibutamoren)

**Agent:** critique-mk677-i1 (red-team; did NOT author the draft)
**Draft:** `vault/library/peptides/mk-677/research-report.md`
**Date:** 2026-06-20

## Prose critique

I adversarially reviewed the synthesized MK-677 report against the seven mandated red-team axes. The report is unusually disciplined; I could not find any defect rising to major/critical. Findings by axis:

**1. Small-molecule-not-peptide / GHS-R1a-not-GHRH classification — CORRECT and load-bearing throughout.** The frontmatter (`class: other`), the "Read this first" block, every section's compound-class note, §1.1 ("the defining fact"), §1.4 (Gq/PLC vs GHRH-R Gs/PKA), and §6.3 all hold the small-molecule/non-peptide and ghrelin-receptor/not-GHRH distinctions. The molecular t½ (~4.7 h, ~4–6 h range) vs PD duration (~24 h) is NOT conflated anywhere; §1.5 explicitly carries the "24-hour half-life is a misquote" reconciliation, §1.7 names it as the recurring trap, and the provenance note confirms the Phase-4.25 half-life check was clean. No defect.

**2. Biomarker/lean-mass ≠ function — CORRECTLY held.** Nass 2008 (FFM +1.1 kg, 95% CI 0.7–1.5) is stated everywhere alongside the explicit "did NOT result in changes in strength or function" and "neither MK-677 nor placebo affected thigh muscle area." This dissociation is named "the spine of the section" (§2) and reinforced in TL;DR, §2.6, §3.3 (frailty → INVESTIGATIONAL, function NOT improved), §4, and §7. It never reads as a functional benefit. No defect.

**3. FAILED programs prominent + correct.** Alzheimer's (Sevigny 2008, n=563, 416 completers, IGF-1 +60.1%/+72.9%, no cognitive/functional benefit on ADAS-Cog/CIBIC-plus/ADCS-ADL/CDR-sob) and hip-fracture (Adunsky 2011, n=123 [62/61], endpoint missed + early termination, CHF ~4/62 [6.5%] vs ~1/61 [1.7%]) are both labeled **FAILED** prominently in §3.1/§3.2, the demarcation legend, §5.3, §7, and the provenance note. Verbatim conclusions are quoted accurately and match the source sections. No defect.

**4. Metabolic harm dominant + CHF honest + class risks flagged extrapolated.** §5 leads with metabolic as "the dominant safety concern" (fasting glucose, insulin sensitivity, HbA1c), grounds it in Nass/Chapman/Svensson, and §5.4 explicitly separates trial-observed AEs from theoretical class risks (malignancy/IGF-1, acromegaly-like effects flagged as extrapolation, NOT observed in the RCTs). §5.3 characterizes the CHF signal honestly and warns against extrapolating the ~6.5% rate to healthy young users. No defect.

**5. Regulatory — precise, no conflation.** Never approved (§6.1); not a lawful dietary ingredient with the two distinct exclusions and the Dec-2025 FDA warning letters to Prime Sports Nutrition (2025-12-12) and Agebox Inc. (2025-12-19) (§6.2); §6.3 states with care that MK-677 as a small molecule is NOT in the §503A peptide action / FR Doc 2026-07361 and that the two tracks are distinct (explicitly "DOES NOT apply"); WADA S2 ibutamoren named (§6.4). The §503A distinction is stated, never conflated. No defect.

**6. Citation integrity.** All 38 inline tokens [1]–[38] resolve to bibliography entries; every bibliography entry [1]–[38] is cited inline at least once (no dangling, no orphan, no gaps). No duplicate bibliography line. The crosswalk maps each per-section local token to the unified number for all 38. No Wikipedia anywhere (only the "No Wikipedia" assertion). PMIDs/DOIs present and consistent with source sections. No defect.

**7. Concentration audit / tier / population annotation.** The 75% Merck author-footprint is FLAGGED (≥70%) with both framings reported (75% author-footprint vs 37.5% strict sponsorship), denominator = 8 enumerated primaries, table consistent. evidence_tier B and risk_tier medium are defensibly argued in §7. Population annotations are carried per-study. One genuine (minor) internal inconsistency found below.

**MINOR finding — population-annotation inconsistency (Svensson 1998 age range).** The same obese-male study [9] is annotated as "aged ~19–49" in §2.2 but "aged 18–50" in §5.1. Both describe the identical Svensson cohort. This was inherited verbatim from the source sections (section-B = ~19–49; section-D = 18–50) and not reconciled during synthesis. It does not change any conclusion and is below the major threshold, but it is a real cross-section numeric inconsistency in a population annotation, which the concentration/population-consistency axis asks me to flag.

No counter-evidence, alternative-explanation, balance, or objectivity defects were located. The report is, if anything, conservative against the compound (it repeatedly refuses to read surrogates as benefit). No additional retrievals warranted.

## Verdict

verdict: PASS

```json
{"phase":"6","critique_agent_id":"critique-mk677-i1","draft_path":"vault/library/peptides/mk-677/research-report.md","findings":[{"category":"logical-inconsistency","severity":"minor","description":"Svensson 1998 [9] obese-male age range is annotated as '~19-49' in §2.2 but '18-50' in §5.1 for the identical cohort; inherited unreconciled from source sections B vs D. No effect on conclusions, but a real cross-section population-annotation inconsistency."}],"additional_retrievals":[],"halt_reasons":[],"iterations":1,"verdict":"PASS"}
```
