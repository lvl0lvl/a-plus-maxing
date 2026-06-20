# ID-Reconcile Phase 4.25 — TSH Biomarker Report

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

### Citations (author + year + PMID, cross-section only)

| Entity | Sections | A value | D value | Status |
|--------|----------|---------|---------|--------|
| Garber 2012 AACE/ATA guidelines (PMID 23246686) | B[6], D[1] | Same PMID, same description | Same PMID, same description | AGREE |
| Hollowell/NHANES III (PMID 11836274) | B[2] only | — | — | Single-section; no cross-section check possible |
| Rothacker 2016 (PMID 26735261) | A[4] only | — | — | Single-section; no cross-section check possible |
| Favresse 2018 (PMID 29982406) | C[4] only | — | — | Single-section; no cross-section check possible |
| Rodondi 2010 JAMA (PMID 20858880) | D[3] only | — | — | Single-section; no cross-section check possible |
| Xing 2021 (PMID 33662155) | B[1] and B[5] | Intra-section duplicate (same paper cited twice in B) | — | Intra-section duplicate per prompt instruction — NOT a cross-section mismatch; synthesis to collapse |

**Citation mismatch count: 0**

---

### Log-Linear TSH↔fT4 Relationship (A + D)

| Claim | Section A | Section D | Status |
|-------|-----------|-----------|--------|
| Relationship type | "log-linear inverse relationship between TSH and free T4" | "TSH responds exponentially to small changes in circulating thyroid hormone" | AGREE (equivalent framing) |
| Amplification ratio | "a 1 pmol/L decrease in fT4 … two- to threefold rise in TSH" (within-range slope description; Rothacker 2016) | "a 2-fold change in free T4 produces a 100-fold shift in TSH" (aggregate amplification; Jonklaas 2014) | AGREE — complementary, not contradictory: A describes the incremental slope within the reference range; D states the cumulative amplification across a 2-fold span. Both are consistent with a log-linear model where log(TSH) is approximately linear in fT4. |
| Section C mention | "The log-linear inverse relationship between TSH and fT4 is load-bearing for interpretation" (no quantification) | — | AGREE with A and D framing |

**Log-linear relationship: no mismatch.**

---

### Reference Interval Figures (B authoritative; cross-checked against D)

| Figure | Section B | Section D | Status |
|--------|-----------|-----------|--------|
| Standard adult upper limit | ~4.0–4.5 mIU/L | SCH defined as TSH 4.5–9.9 mIU/L (implies upper normal ≤4.5) | AGREE |
| Overt hypothyroidism threshold | often >10 mIU/L | >10 mIU/L | AGREE |
| Suppressed TSH (overt hyperthyroidism) | <0.1 mIU/L | <0.1 mIU/L | AGREE |
| Subclinical hyperthyroidism Grade 1 | TSH 0.1–0.39 mIU/L (B table) | suppressed TSH + normal fT4/fT3 (D, no grade breakdown) | AGREE (no conflict; D does not contradict B's grading) |
| Age-related upper limit shift | 97.5th pctile = 3.56 mIU/L (age 20–29) → 7.49 mIU/L (age ≥80), Surks & Hollowell 2007 | "TSH levels of 5–8 mIU/L are common in healthy octogenarians" | AGREE (D's prose range is consistent with B's 7.49 mIU/L 97.5th-pctile figure) |

**Reference interval mismatch count: 0**

---

### Subclinical Disease Framing (B + D)

| Concept | Section B | Section D | Status |
|---------|-----------|-----------|--------|
| SCH definition | TSH above upper reference limit + normal fT4, HPT axis intact, not during acute illness/post-op | TSH mildly elevated (4.5–9.9 mIU/L) + fT4 within reference range | AGREE |
| SCH spontaneous reversion | ~60% of mild SCH cases revert within 5 years (B, from Jasim 2021 IJEM) | watchful waiting in >70 years with TSH 5–10 mIU/L (D, TRUST trial) | AGREE (consistent clinical framing) |
| TSH ≥10 mIU/L as stronger treatment trigger | B implies by referencing mild SCH controversy (4.5–9.9 range) | D explicitly: "TSH ≥10 mIU/L … stronger treatment trigger … approximately doubled CHD risk" | AGREE |

**Subclinical disease framing mismatch count: 0**

---

### Institutions

| Institution | Sections | Description consistency | Status |
|-------------|----------|------------------------|--------|
| ATA (American Thyroid Association) | B (2011 and 2017 pregnancy guidelines), D (via AACE/ATA 2012 guidelines) | Consistently named; distinct guideline versions referenced appropriately | AGREE |
| NACB (National Academy of Clinical Biochemistry) | B[3] only | 2003 guidelines recommending upper limit ~2.5 mIU/L | Single-section; no cross-check needed |
| IFCC C-STFT (Committee for Standardization of Thyroid Function Tests) | C only | Between-assay biases up to ~39%; harmonization ongoing | Single-section; no cross-check needed |
| Thyroid Studies Collaboration | D (Rodondi 2010; Collet 2012; Blum 2015) | Consistently attributed | Single-section; no conflict |

**Institution-name mismatch count: 0**

---

### Compound / Biomarker Identifiers

| Identifier | Sections | Status |
|------------|----------|--------|
| TSH units: mIU/L ≡ µIU/mL | B (explicit equivalence statement) | Single-section authoritative; A, C, D all use mIU/L consistently | AGREE |
| TSH molecular weight ~28 kDa | A only | Single-section |
| Biotin interference threshold ≥20–50 µg/L on Roche platforms | C only | Single-section |

**Compound identifier mismatch count: 0**

---

### Regulatory Dates / Guideline Years

| Document | Section | Year | Status |
|----------|---------|------|--------|
| NACB lab practice guidelines | B | 2003 | Single-section |
| AACE/ATA hypothyroidism guidelines | B[6], D[1] | 2012 (both cite same paper, same year) | AGREE |
| ATA pregnancy guidelines — first version cited | B | 2011 | Single-section (2011 guidelines superseded by 2017) |
| ATA pregnancy guidelines — current | B[9] | 2017 (Alexander, Pearce et al.) | Single-section |
| ATA hypothyroidism treatment guidelines | D[2] | 2014 (Jonklaas et al.) | Single-section |
| ATA hyperthyroidism guidelines | B[10] | 2016 (Ross et al.) | Single-section |

**Regulatory date mismatch count: 0**

---

### Trial Registrations

No trial registrations cited in any section. TRUST trial (Stott 2017 NEJM, PMID 28402245) cited in D only — no registration number appears in any section.

**Trial registration mismatch count: 0**

---

### Notes on Near-Misses (Not HALTs)

1. **Pulsatile burst count and amplitude:** A cites Brabant 1990 (PMID 2105332) — ~10–12 bursts/24h, amplitude ~0.6 mIU/L per pulse. C cites van der Spoel 2021 (PMID 33716972) — ~13 bursts/24h, pulse mass ~0.90 mU/L. Different source studies, different cohort estimates of a biologically variable parameter; not the same citation with conflicting values. Synthesis should note the range spans both estimates. NOT a HALT.

2. **Nocturnal TSH peak timing:** A (Brabant 1990) states peak "between 21:00 and 02:00." C (van der Spoel 2021) states peak "between 02:00–04:00 h." Different underlying studies with overlapping but distinct windows reflecting genuine literature variability. The attributions differ (different PMIDs), so this is not a citation-mismatch. Synthesis should present the range (21:00–04:00) as the nocturnal surge window. NOT a HALT.

3. **Xing 2021 intra-section duplicate:** B[1] and B[5] are the same paper (PMID 33662155). Per prompt instructions, this is a known intra-section duplicate for synthesis to collapse. NOT treated as a cross-section mismatch. NOT a HALT.

---

## Tally

| Class | Scanned | Mismatches |
|-------|---------|-----------|
| Citations (cross-section) | 6 shared or potentially shared entities examined | 0 |
| Institutions | 4 | 0 |
| Compound identifiers | 3 | 0 |
| Regulatory dates | 6 | 0 |
| Trial registrations | 0 (none present) | 0 |
| **TOTAL** | **19** | **0** |

---

## Machine-Parseable Record

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":6,"mismatch_count":0},"institutions":{"scanned":4,"mismatch_count":0},"compound_identifiers":{"scanned":3,"mismatch_count":0},"regulatory_dates":{"scanned":6,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```

---

## Summary

All shared entities across sections A, B, C, and D are consistent. The log-linear TSH↔fT4 amplification framing is complementary across A and D (A gives the incremental within-range slope; D gives the 2-fold→100-fold aggregate amplification), not contradictory. Reference interval figures, subclinical disease framing, institutional names, guideline years, and the AACE/ATA 2012 citation (PMID 23246686) all agree across sections. Two near-misses (pulsatile parameter estimates; nocturnal peak timing window) reflect different source studies with different PMIDs and do not constitute citation mismatches. The intra-section Xing 2021 duplicate (B[1]/B[5]) is flagged for synthesis collapse per prompt instructions and does not affect cross-section verdict.
