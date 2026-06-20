# ID-RECONCILE — Phase 4.25
## Estradiol Biomarker Report — Cross-Section Entity Reconciliation

Sections scanned: A (Physiology), B (Reference Ranges), C (Measurement), D (Determinants & Clinical Significance)
Match strategy: author + year + PMID; NOT local bracket numbering.

---

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

### 1. Citations (shared across 2+ sections)

| Entity | Sections | A attribution | B attribution | C attribution | D attribution | Mismatch? |
|--------|----------|---------------|---------------|---------------|---------------|-----------|
| Frederiksen 2020 (PMID 31720688) | A [4], B [6] | "Sex-specific Estrogen Levels and Reference Intervals from Infancy to Late Adulthood Determined by LC-MS/MS"; JCEM 2020;105(3):754–768; tag: cohort; male range ~14–41 pg/mL / 50–150 pmol/L | Same title (minor case difference only); same PMID/DOI/journal; tag: cohort; same male range 50–150 pmol/L (~14–41 pg/mL) | Not cited | Not cited | **No mismatch** |
| Rosner et al. 2013 (PMID 23463657) | B [1/2], C [1] | Not cited | "Challenges to the measurement of estradiol: an Endocrine Society position statement"; JCEM 2013;98(4):1376–1387; PMID 23463657; [regulatory/mechanism_review] | Same paper, same PMID, same journal; [mechanism_review]; quantitative claims consistent (68% overestimation by direct RIA) | Not cited | **No mismatch** |
| Finkelstein 2013 (PMID 24024838) | D only | Not cited | Not cited | Not cited | "Gonadal steroids and body composition, strength, and sexual function in men"; NEJM 2013;369(11):1011–1022; PMID 24024838; [rct]; N=400 | **Single-section only — not a shared entity; no cross-section check required** |

Citation mismatch tally: **0 of 2 shared citations**.

---

### 2. Compound Identifiers

| Entity | Sections | Consistent? |
|--------|----------|-------------|
| 17β-estradiol (E2) | A, B, C, D | Yes — all four sections use "17β-estradiol" or "E2" consistently |
| CYP19A1 (aromatase) | A, D | A: "aromatase (CYP19A1)"; D: "aromatase activity, primarily in adipose, liver, and brain" — same enzyme, consistent biological framing. No identifier conflict. |
| SHBG | A, B, D | Consistent across all three sections as sex hormone-binding globulin; role described consistently. |
| Estrone (E1) / Estriol (E3) | A, B, D | All consistent: E1 = moderate potency, postmenopausal dominant; E3 = weakest, pregnancy. No conflict. |

Compound-identifier mismatch tally: **0**.

---

### 3. Institutions

| Entity | Sections | Consistent? |
|--------|----------|-------------|
| CDC Hormone Standardization (HoSt) Program | C only | Single section; no cross-section check. |
| Endocrine Society | B, C | Both cite the 2013 position statement (PMID 23463657) with consistent attribution. No conflict. |
| Mayo Clinic Laboratories | B only | Single section. |

Institution mismatch tally: **0**.

---

### 4. Regulatory Dates

| Entity | Section | Value | Cross-section? |
|--------|---------|-------|----------------|
| CDC HoSt Phase 2 launch | C | 2014 | C only — no cross-section check required. |

Regulatory-date mismatch tally: **0**.

---

### 5. Trial Registrations

No trial registration numbers (NCT IDs) cited in any section.

Trial-registration mismatch tally: **0**.

---

## Specific Entity Checks (Mandated by Prompt)

### A. Frederiksen 2020 (PMID 31720688) — A vs B
- Section A [4]: LC-MS/MS cohort, adult male ~14–41 pg/mL (50–150 pmol/L), early follicular ~20–50 pg/mL, preovulatory ~150–350 pg/mL, luteal ~60–200 pg/mL. Tag: cohort.
- Section B [6]: Same cohort (n=1838), same male range (~14–41 pg/mL / 50–150 pmol/L), no significant age-related decline ages 30–60. Tag: cohort.
- **AGREE.** Numerical values, attribution, and tag are consistent.

### B. Conversion factor ×3.671
- Section B only states the factor explicitly: "pg/mL × 3.671 = pmol/L" (MW 272 g/mol). No other section cites a conflicting factor. All pmol/L values in A and C are mathematically consistent with this factor (e.g., A: 20 pg/mL → 73 pmol/L; 150 pg/mL → 550 pmol/L; 200 pg/mL → 734 pmol/L — all match Section B's conversion table).
- **AGREE.**

### C. Aromatase/CYP19A1 + E2/E1/E3 framing — A vs D
- Section A: CYP19A1 in ovary (two-cell model), adipose, bone, brain, liver, skin. Male peripheral contribution ~85%.
- Section D: ">80% of circulating E2 in men derives from aromatase activity, primarily in adipose, liver, and brain." Slight numeric approximation (~80% vs ~85%) but both drawn from narrative prose, not from a shared cited statistic — no citation-attribution conflict.
- **AGREE within acceptable approximation tolerance; not a citation mismatch.**

### D. Immunoassay inaccuracy + LC-MS/MS — B vs C
- Section B: "Direct immunoassays have a limit of quantitation of 30–100 pg/mL — above most male, prepubertal, and postmenopausal concentrations. Results in these populations from direct immunoassays are unreliable. LC-MS/MS is the current gold standard." [Rosner 2013, PMID 23463657]
- Section C: "direct RIAs (without extraction) overestimated by 68%"; LC-MS/MS reference standard; immunoassays "break down precisely where accurate measurement matters most: in men, postmenopausal women, children, and patients monitored on aromatase-inhibitor therapy." [Rosner 2013, PMID 23463657; Stanczyk 2010, PMID 20332268]
- Section D (Limitations #2): Cross-references Measurement section; same conclusion. No numerical conflict.
- **AGREE.**

### E. Male-E2-matters framing — A vs D
- Section A: E2 required for spermatogenesis, libido, fat distribution, bone (threshold ~20 pg/mL / 73 pmol/L). [Cooke 2017, PMID 28539434]
- Section D: Fat mass accumulation tracks E2 deficiency; libido/erectile function partly estradiol-dependent; bone loss with AI-driven E2 suppression. [Finkelstein 2013, PMID 24024838; Ettinger 1998, PMID 9661589]
- **AGREE** — consistent mechanistic framing, no conflicting claims.

### F. Cycle-phase values — A vs B vs C vs D
- All four sections give broadly consistent follicular-phase nadir values (~20–80 pg/mL range depending on whether quoting a typical midpoint or a full population interval), preovulatory peak (150–500 pg/mL depending on context), and luteal range (40–260 pg/mL). Variation reflects different reporting conventions (typical value vs. 2.5–97.5th percentile interval vs. clinical monitoring targets) and different source papers (Frederiksen 2020 vs. Verdonk 2019), not an underlying factual conflict.
- **AGREE — no citation-level disagreement.**

---

## Mismatch Tally Summary

| Class | Scanned (shared entities) | Mismatches |
|-------|--------------------------|------------|
| Citations | 2 | 0 |
| Institutions | 1 (shared: Endocrine Society) | 0 |
| Compound identifiers | 4 | 0 |
| Regulatory dates | 0 shared | 0 |
| Trial registrations | 0 | 0 |

---

## Machine-Readable JSON

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":2,"mismatch_count":0},"institutions":{"scanned":1,"mismatch_count":0},"compound_identifiers":{"scanned":4,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```

---

## Summary

All shared entities across two or more sections agree: Frederiksen 2020 (PMID 31720688) is consistently attributed as a cohort-tagged LC-MS/MS reference study with identical male E2 ranges in both A and B; the Rosner 2013 Endocrine Society position statement (PMID 23463657) is cited consistently in B and C with aligned quantitative claims; the ×3.671 conversion factor is internally consistent across all pmol/L values in all sections; and the immunoassay-inaccuracy, LC-MS/MS preference, and male-E2-matters framings are coherent across B, C, and D. No genuine cross-section disagreements were found.
