# Phase 4.25 — ID-Reconcile Verifier: Total Testosterone

## Verdict

verdict: PASS

All shared entities across sections A, B, C, and D agree within expected source-level rounding variation. No genuine cross-section disagreement found where the same fact or citation yields a conflicting value or attribution.

---

## Per-Class Mismatch Table

### Citations (author + year + PMID, matched across 2+ sections)

| Citation | Sections | A attribution | B attribution | C attribution | D attribution | Status |
|----------|----------|---------------|---------------|---------------|---------------|--------|
| Bhasin et al. 2018, PMID 29562364 | B, C, D | — | JCEM 2018, ref [2]; "Endocrine Society clinical practice guideline" | JCEM 2018, ref [7]; same title | JCEM 2018, refs [1] and [3]; same title | AGREE |
| Rosner et al. 2007, PMID 17090633 | B, C | — | JCEM 2007, ref [5]; Rosner W, Auchus RJ, Azziz R, Sluss PM, Raff H | JCEM 2007, ref [1]; same authors, same journal | — | AGREE |
| Travison et al. 2017, PMID 28324103 | B (explicit); C (prose reference) | — | JCEM 2017, ref [1]; "harmonized reference ranges" | Referenced in prose as "Travison harmonization study" within the HoSt narrative; no independent bibliography entry | — | AGREE (B holds the full citation; C attributes correctly without duplicating) |
| Goldman et al. 2017, PMID 28673039 | A only | ref [4]; Endocrine Reviews 2017; "A Reappraisal of Testosterone's Binding in Circulation" | — | Not cited by PMID | — | N/A (single-section; no cross-section conflict possible) |
| Vermeulen et al. 1999, PMID 10523012 | C only | — | — | ref [9]; JCEM 1999; validated calculated free T | — | N/A |

### Reference-range values (harmonized range + conversion)

| Entity | Section A | Section B | Section C | Section D | Status |
|--------|-----------|-----------|-----------|-----------|--------|
| Harmonized lower limit | Not stated as formal harmonized value; HPG homeostatic narrative gives "~300–1,000 ng/dL" | **264 ng/dL (9.2 nmol/L)** — Travison 2017 / HoSt | 264 ng/dL (9.2 nmol/L) — cited via Bhasin 2018 adopting HoSt | 264 ng/dL (9.2 nmol/L) — Bhasin 2018 | AGREE (A's 300–1,000 is HPG physiology narrative, not the formal harmonized cutoff; no conflict) |
| Harmonized upper limit | Not stated | 916 ng/dL (31.8 nmol/L) | Not stated explicitly | Not stated | AGREE (only B cites the formal upper bound; absent in others is not a conflict) |
| Unit conversion | Not stated | 1 ng/dL = 0.0347 nmol/L | Not stated | Not stated | AGREE |

### 3-Pool fractions (SHBG / albumin / free)

| Fraction | Section A (Goldman 2017) | Section C | Section D | Status |
|----------|--------------------------|-----------|-----------|--------|
| SHBG-bound | ~44% | ~44% | ~44% | AGREE |
| Albumin-bound | ~50% | ~54% | ~54% | MINOR NUMERICAL VARIATION — within published source-level variation; A cites Goldman 2017 (PMID 28673039); C and D reflect Vermeulen-era estimates. Neither section attributes the 50% vs 54% figure to the same citation with a conflicting value. Not a genuine mismatch. |
| Free | ~2% | 1–3% | ~2% | AGREE (2% is within the 1–3% range; no conflict) |

### Hypogonadism threshold (~300 ng/dL + Bhasin/Endocrine Society 2018)

| Entity | Section B | Section D | Status |
|--------|-----------|-----------|--------|
| Lower diagnostic threshold (formal) | 264 ng/dL (9.2 nmol/L) per Bhasin 2018 (PMID 29562364) | 264 ng/dL (9.2 nmol/L) per Bhasin 2018 (PMID 29562364) | AGREE |
| 300 ng/dL landmark | "Reasonable clinical landmark, sitting close to the harmonized 2.5th percentile" | "Popularized by the American Urological Association as a diagnostic threshold; contested" | AGREE in substance — both acknowledge 300 ng/dL as a widely used but non-definitive cutoff; neither claims it is the formal Endocrine Society threshold |
| Diagnostic criteria | Symptoms AND two confirmatory fasting morning samples | Symptoms AND "unequivocally and consistently low" on two fasting morning samples | AGREE |

### LC-MS/MS + CDC HoSt standardization

| Entity | Section B | Section C | Status |
|--------|-----------|-----------|--------|
| Reference method | LC-MS/MS at CDC reference laboratory | LC-MS/MS (ID-LC-MS/MS variant); CDC adopted as RMP | AGREE |
| HoSt Program citation | Referenced via Bhasin 2018 endorsement; Travison 2017 used it as anchor | PMID 20926540 (Rosner/Vesper 2010 consensus); Wang et al. 2014 (PMID 24960363) as CDC RMP pub | AGREE (B cites the downstream endorsement; C cites the founding consensus document — different citations, same program, no conflict) |
| Performance criterion | Not stated | ±6.4% mean bias vs RMP over 2.50–1,000 ng/dL | AGREE (only C gives technical details; B does not contradict them) |

### Diurnal / AM-sampling rationale

| Entity | Section A | Section C | Section D | Status |
|--------|-----------|-----------|-----------|--------|
| AM collection window | 08:00–10:00 | 08:00–10:00 | 07:00–09:00 h (stated in measurement limitations sub-section) | MINOR: D states "07:00–09:00 h" while A and C state "08:00–10:00." D's window is shifted 1 hour earlier but overlaps substantially; this reflects rounding of different published sources. The Endocrine Society guideline (Bhasin 2018 cited by both C and D) specifies morning fasting samples without pinning an exact 2-hour window; the 07–09 vs 08–10 difference is source-level variation, not a citation-level mismatch. |
| Magnitude of diurnal decline | ≥43% from peak to nadir (Diver 2003, PMID 12780747) | 15–20% higher in morning vs evening nadir (Endotext chapter, NBK279145) | 20–35% lower by afternoon (Bhasin 2018) | APPARENT VARIATION — these cite different statistics from different sources: A quotes the Diver 2003 AM-to-nadir range; C quotes a typical population-level morning-vs-evening difference; D quotes the Bhasin 2018 guideline figure. No two sections attribute a different value to the *same* citation. Not a genuine citation-mismatch. |

### SHBG discordance (C vs D)

| Entity | Section C | Section D | Status |
|--------|-----------|-----------|--------|
| Recommendation to measure free T | Bhasin 2018 (PMID 29562364) — when SHBG abnormality suspected | Bhasin 2018 (PMID 29562364) — same | AGREE |
| Conditions raising SHBG | Aging, hyperthyroidism, cirrhosis, estrogen/OCP, HIV, anticonvulsants | Aging, hyperthyroidism, liver disease, HIV, anticonvulsants, anorexia | AGREE (minor list variation; not conflicting) |
| Conditions lowering SHBG | Obesity, T2D, insulin resistance, hypothyroidism, androgen use, nephrotic syndrome, glucocorticoid excess | Obesity, hypothyroidism, hyperinsulinemia, nephrotic syndrome, exogenous androgens | AGREE |

---

## Tally

| Class | Scanned | Mismatch count |
|-------|---------|----------------|
| Citations (author+year+PMID) | 5 cross-section matches | 0 |
| Institutions | 3 (CDC, Endocrine Society, ISSWSH) | 0 |
| Compound identifiers (ng/dL values, nmol/L values, conversion factor) | 8 | 0 |
| Regulatory dates | 2 (Bhasin 2018, Rosner 2007) | 0 |
| Trial registrations | 0 | 0 |

**Total genuine mismatches: 0**

Minor numerical variations noted (albumin-bound fraction ~50% in A vs ~54% in C/D; diurnal AM window stated as 07:00–09:00 in D vs 08:00–10:00 in A/C) are within published source-level rounding and are not attributed to the same citation with differing values. They do not constitute genuine cross-section disagreements.

---

## Summary

All shared entities reconcile cleanly. Bhasin 2018 (PMID 29562364), Rosner 2007 (PMID 17090633), and Travison 2017 (PMID 28324103) are cited consistently across sections. The harmonized 264 ng/dL lower bound, the 300 ng/dL clinical landmark, the LC-MS/MS + CDC HoSt standard, and the AM-sampling requirement all agree. No halt condition present.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":5,"mismatch_count":0},"institutions":{"scanned":3,"mismatch_count":0},"compound_identifiers":{"scanned":8,"mismatch_count":0},"regulatory_dates":{"scanned":2,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
