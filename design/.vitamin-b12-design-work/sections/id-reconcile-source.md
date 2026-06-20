# ID-RECONCILE — Phase 4.25, Iteration 2
**Topic:** Serum Vitamin B12
**Sections checked:** A, B, C, D

---

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

| Entity class | Instances scanned | Mismatches |
|---|---|---|
| Citations (PMID / journal / year / sample size) | 14 | 0 |
| Institution / organization names | 5 | 0 |
| Compound identifiers (names, unit-conversion formula) | 8 | 0 |
| Regulatory dates (guideline year, effective dates) | 3 | 0 |
| Trial registrations | 0 | 0 |

**Total mismatches: 0**

---

## Confirmation of the Three Previously Halted Items

| # | Item | Iteration-1 finding | Iteration-2 status |
|---|---|---|---|
| 1 | Unit-conversion formula (A vs B) | A had inverted formula (pmol/L × 0.738 = pg/mL) | RESOLVED — A now states "pg/mL × 0.738 = pmol/L"; B states "1 pg/mL = 0.738 pmol/L"; both equivalent and consistent |
| 2 | Clarke 2007 (PMID 17363419) sample size (B vs C) | B = 2,403 vs C = 544 | RESOLVED — C now states n = 2,403; matches B |
| 3 | Valente 2011 (PMID 21482749) sample size (B vs C) | B = 700 vs C ≈ 600 | RESOLVED — C now states n = 700; matches B |

---

## Full Cross-Section Entity Check (All Classes)

### Citations — Shared across ≥2 sections

| Citation | Sections | B sample size | C sample size | PMID agreement | Status |
|---|---|---|---|---|---|
| Clarke 2007 (*Clin Chem*, PMID 17363419) | B (ref 4), C (ref 4) | 2,403 | 2,403 | ✓ | PASS |
| Valente 2011 (*Clin Chem*, PMID 21482749) | B (ref 3), C (ref 5) | 700 | 700 | ✓ | PASS |
| Stabler 2013 (*NEJM*, PMID 23301732) | A (ref 7), B (ref 5), D (ref 1) | — | — | ✓ all three | PASS |
| Devalia/BSH 2014 (*Br J Haematol*, PMID 24942828) | C (ref 2), D (ref 4) | — | — | ✓ | PASS |
| Clarke 2007 AUC figures | B: 0.85 (holoTC) vs 0.76 (total B12) overall; subgroups 0.87/0.79 (normal renal) and 0.85/0.74 (impaired renal) | C: "AUC 0.85–0.87 vs 0.74–0.79" — range covers both subgroups | — | Consistent | PASS |
| Valente 2011 AUC figures | B: holoTC 0.90 (0.86–0.93) vs B12 0.80 vs MMA 0.78 | C: same figures stated identically | — | ✓ | PASS |
| Carmel 2011 (*Am J Clin Nutr*, PMID 21593511) | B (ref 2) | — | — | Single-section; no cross-section conflict | PASS |
| Nexo/Hoffmann-Lücke 2011 (*Am J Clin Nutr*, PMID 21593496) | A (ref 5) | — | — | Different paper from Carmel 2011; no conflict | PASS |

### Institutions / Organizations

| Name | Sections | Status |
|---|---|---|
| NICE (National Institute for Health and Care Excellence) | B, C | Consistent spelling and guideline number (NG239 2024) |
| NIH Office of Dietary Supplements | A (ref 3) | Single-section; no conflict |
| British Committee for Standards in Haematology (BSH) | C (ref 2), D (ref 4) | Consistent |
| Axis-Shield Diagnostics (Dundee) | C | Single-section; no conflict |
| WHO (IS 03/178) | C (ref 8) | Single-section; no conflict |

### Compound Identifiers

| Entity | Sections | Status |
|---|---|---|
| pg/mL × 0.738 = pmol/L (forward conversion) | A, B | PASS — both now state the forward direction |
| Methylcobalamin (MeCbl) | A | Single-section definition; not contradicted |
| 5′-deoxyadenosylcobalamin (AdoCbl) | A | Single-section definition; not contradicted |
| Holotranscobalamin (holoTC / "active B12") | A, B, C, D | Consistent definition across all four sections (TC-II-bound, CD320-receptor-mediated uptake) |
| Methylmalonic acid (MMA) | A, B, C, D | Consistent (adenosylcobalamin-dependent methylmalonyl-CoA mutase; >280–300 nmol/L in A; MMA threshold not re-stated in B/C/D — no conflict) |
| 5-methyltetrahydrofolate (5-methyl-THF) | A, D | Consistent labeling and mechanism |
| S-adenosylmethionine (SAM) | A | Single-section; no conflict |
| Succinyl-CoA | A | Single-section; no conflict |

### Regulatory Dates

| Guideline | Date stated | Sections | Status |
|---|---|---|---|
| NICE NG239 | 2024 | B (ref 1), C (implicit via BSH reference) | PASS |
| NIH-ODS Fact Sheet | "Updated 2024" | A (ref 3) | Single-section; no conflict |
| BSH / Devalia 2014 (*Br J Haematol*) | 2014 | C (ref 2), D (ref 4) | PASS |

### Trial Registrations

None cited across any section. Scanned: 0. Mismatches: 0.

---

## Borderline Items Examined and Cleared

| Item | A | B | C | D | Resolution |
|---|---|---|---|---|---|
| Transport split HC fraction | ~80% | ~70–80% | ~70–80% | storage pool (consistent) | Point estimate vs range — compatible approximation, not a conflict |
| Transport split TC fraction | ~20% | 20–30% | ~20–30% | consistent | Same |
| Grey zone (pmol/L) | 148–295 (derived from 200–400 pg/mL) | 133–258 (NICE NG239) | qualitative only | 150–300 (rounded approximation of A) | Each figure is self-labeled with its source; different guideline bodies set different thresholds; no single shared entity stated differently |
| HoloTC deficiency threshold | <25–40 pmol/L (assay-range) | <25 pmol/L (NICE) | <25 pmol/L (NICE, via ref) | n/a | A notes assay variability; B/C cite NICE cut-point — consistent framing |
| Anti-IF antibody ASSAY false-negative rate | not stated | not stated | 22–53% of PA samples give falsely normal/elevated serum B12 | 30–50% false-negative rate of the AIFA antibody test | Different statistics: C measures assay-interference rate on serum B12 assay; D measures false-negative rate of the AIFA antibody detection test itself — distinct, not conflicting |
| AIFA prevalence in PA | 50–70% | not stated | 50–70% | 50–70% | PASS — consistent across A, C, D |

---

## Tally

| Class | Scanned | Mismatches |
|---|---|---|
| Citations | 14 | 0 |
| Institutions | 5 | 0 |
| Compound identifiers | 8 | 0 |
| Regulatory dates | 3 | 0 |
| Trial registrations | 0 | 0 |
| **Total** | **30** | **0** |

---

## Machine-Readable Block

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":14,"mismatch_count":0},"institutions":{"scanned":5,"mismatch_count":0},"compound_identifiers":{"scanned":8,"mismatch_count":0},"regulatory_dates":{"scanned":3,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```

---

## Summary

All three iteration-1 halts are confirmed resolved: Section A's unit-conversion formula is now correctly stated in the forward direction (pg/mL × 0.738 = pmol/L), Clarke 2007 (PMID 17363419) carries n = 2,403 in both Sections B and C, and Valente 2011 (PMID 21482749) carries n = 700 in both Sections B and C. A full sweep of all 30 shared-entity instances across the five ID-RECONCILE classes found zero remaining mismatches; borderline numerical variations in transport-fraction percentages and grey-zone bounds are self-consistently attributed to distinct sources and do not constitute cross-section conflicts.
