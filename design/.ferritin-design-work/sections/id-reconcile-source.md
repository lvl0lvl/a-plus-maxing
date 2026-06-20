# ID-RECONCILE — Phase 4.25 — Serum Ferritin

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

| Entity Class | Instances Scanned | Cross-Section Mismatches | Notes |
|---|---|---|---|
| Citations (author+year+PMID) | 6 shared-cite candidates checked | 0 | Ueda/Takasawa 2018 (PMID 30150549) in B+D: consistent. Cancado 2025 (PMID 39941219) in A+B: consistent. BSG Snook 2021 (PMID 34497146) in B+D: consistent. |
| Institutions / guideline bodies | 5 (WHO, BSG, ESC, KDIGO, AGA) | 0 | WHO 2020 guideline cited consistently in B and C (different aspects: clinical threshold vs. calibration standard — complementary, not conflicting). |
| Compound / biomarker identifiers | 5 (ng/mL=µg/L equivalence, 1 ng/mL≈8–10 mg stores, <15 cutoff, <30 cutoff, TSAT thresholds) | 0 | See per-entity notes below. |
| Regulatory dates | 2 (WHO IS 19/118 = 2022; BSG 2021) | 0 | Consistent across sections. |
| Trial registrations | 0 | 0 | No trial registrations cited in any section. |

**Total genuine cross-section mismatches: 0**

---

## Per-Entity Detail

### 1. 1 ng/mL ≈ 8–10 mg storage iron
- **Section A** [9, PMID 39941219]: stated explicitly — "approximately 1 ng/mL (= 1 µg/L) of serum ferritin ≈ 8–10 mg of storage iron in healthy adults."
- **Section B**: does not cite this conversion. No conflict — absence is not contradiction.
- **Verdict: no mismatch.**

### 2. Iron-deficiency cutoffs: <15 ng/mL and <30 ng/mL
- **Section A** [9]: <15 ng/mL = absent iron stores.
- **Section B** [4, Guyatt 1992, PMID 1487761]: <15 ng/mL, specificity ~99%, sensitivity ~59%. <30 ng/mL as contemporary threshold (BSG 2021, WHO 2020).
- **Section D** [1, Truong 2024, PMID from Lancet Haematol]: "below 15–30 ng/mL is the single most specific laboratory test."
- All three sections agree: <15 is the classical high-specificity anchor; <30 is the preferred contemporary operational cutoff. Direction and hierarchy are consistent.
- **Verdict: no mismatch.**

### 3. Acute-phase reactant / IL-6 / hepcidin physiology — ferritin RISES in inflammation
- **Section A**: IL-1β, IL-6, TNF-α → NF-κB → ferritin transcription upregulated; IL-6 → JAK2-STAT3 → hepcidin → ferroportin degradation → iron sequestration.
- **Section B** [8, Ueda 2018, PMID 30150549]: IL-1β and TNF-α via NF-κB; hepcidin chronically elevated in chronic disease, diverting iron into macrophages and hepatocytes.
- **Section C**: IL-6, TNF-α, IL-1β upregulate ferritin transcription (acute-phase response named as confound).
- **Section D** [4, Ueda 2018, PMID 30150549]: IL-6 and TNF-α directly upregulate hepatic ferritin synthesis; hepcidin sequesters iron in macrophages and hepatocytes.
- All four sections consistently name the same cytokines (IL-6, TNF-α, IL-1β) and the same direction (ferritin rises). A and D share the same mechanistic depth on hepcidin; B and C corroborate. No directional or factual divergence.
- **Verdict: no mismatch.**

### 4. Functional vs. absolute iron deficiency (B + D)
- **Section B** [9, ESC 2021, PMID 34447992]: two-tier schema — absolute deficiency at ferritin <100 ng/mL; functional deficiency at ferritin 100–299 ng/mL + TSAT <20%.
- **Section D** [4, Ueda 2018, PMID 30150549]: functional iron deficiency = normal/elevated total stores but iron sequestered by hepcidin, unavailable for erythropoiesis; CKD functional deficiency TSAT <20% with ferritin possibly >100–200 ng/mL; CHF ~50% affected by TSAT-based criteria even with non-low ferritin.
- Both sections agree on the concept, mechanism (hepcidin-mediated sequestration), and the TSAT <20% threshold as the functional marker. B provides the specific ESC numeric schema; D applies the same logic across CKD/CHF/IBD. Consistent.
- **Verdict: no mismatch.**

### 5. WHO / standardization story (B + C)
- **Section B** [6, WHO 2020]: clinical threshold guidance — <30 ng/mL standard; <70 ng/mL when inflammation present.
- **Section C** [5, Fox 2022, PMID 34939377]: calibration standards — IS 80/602, IS 80/578 (1985), IS 94/572 (1997), IS 19/118 (2022 current). IS 19/118 is recombinant L-chain ferritin, 10.5 µg/ampoule, 12 laboratories in 9 countries.
- These sections address orthogonal aspects of the WHO's role (clinical thresholds vs. metrological standards). No contradiction; complementary.
- **Verdict: no mismatch.**

### 6. Hemochromatosis / TSAT >45% (B + D)
- **Section B**: notes hemochromatosis in the elevated ferritin differential; does not state a specific TSAT cutoff for hemochromatosis workup (TSAT <20% is cited only for functional deficiency).
- **Section D** [7, Allen 2008, PMID 18199861]: TSAT >45% is "the earliest and most sensitive marker of iron excess" and gates the hemochromatosis diagnostic algorithm (fasting TSAT >45% → HFE genotyping).
- B does not contradict D; B simply does not state the hemochromatosis-specific TSAT threshold. D fills that gap. There is no conflicting TSAT value for hemochromatosis anywhere in the four sections.
- **Verdict: no mismatch.**

### 7. Units: ng/mL = µg/L
- **Section A**: "1 ng/mL (= 1 µg/L)" — explicit equivalence.
- **Section B**: "ng/mL, numerically identical to µg/L."
- **Section C**: uses both notations. Note: one line reads "86,028 µg/L (86 µg/mL)" — this appears to be an internal parenthetical shorthand for "86 µg/mL ≈ 86,000 ng/mL ≈ 86,028 µg/L" where the µg/mL parenthetical is erroneous (should be ng/mL or µg/L), but this is a within-C notational issue, not a cross-section disagreement on the ng/mL = µg/L equivalence.
- **Section D**: ng/mL throughout.
- **Verdict: no mismatch across sections.**

### 8. Shared citations — full cross-section audit
| Citation | Sections | PMID Consistent | Data Consistent |
|---|---|---|---|
| Ueda N, Takasawa K 2018, *Nutrients* | B[8], D[4] | 30150549 = 30150549 ✓ | Hepcidin/ferritin/CKD: consistent ✓ |
| Cancado RD et al. 2025, *Diagnostics* | A[9], B[7] | 39941219 = 39941219 ✓ | Both cite as mechanism_review; usage consistent ✓ |
| BSG Snook J et al. 2021, *Gut* | B[5], D[2] | 34497146 = 34497146 ✓ | BSG 2021 guidelines cited for same content ✓ |

---

## Tally

- Entity classes scanned: 5
- Total cross-section mismatches: 0
- halt_reasons: none

---

## Machine-Readable JSON

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":6,"mismatch_count":0},"institutions":{"scanned":5,"mismatch_count":0},"compound_identifiers":{"scanned":5,"mismatch_count":0},"regulatory_dates":{"scanned":2,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```

---

## Summary

All shared entities across the four sections are internally consistent: the <15 / <30 ng/mL iron-deficiency cutoffs, the IL-6/TNF-α/IL-1β → NF-κB → ferritin (rises) mechanism and its hepcidin arm, the functional vs. absolute iron deficiency distinction (TSAT <20% as the functional marker), the ng/mL = µg/L unit equivalence, and the three shared citations (Ueda 2018, Cancado 2025, BSG Snook 2021) all agree across sections. No genuine cross-section disagreement was found.
