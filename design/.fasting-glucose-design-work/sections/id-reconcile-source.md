# Phase 4.25 — ID Reconcile: Fasting Glucose (Shared-Entity Cross-Section Check)

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

No mismatches found across any class. Tables below record what was examined.

### Citations (papers cited in 2+ sections)

Each section maintains an independent bibliography numbered from [1]. Cross-section matching was performed on author + year + PMID/DOI.

| Entity (author + year) | Sections | Agreement |
|---|---|---|
| ADA Standards of Care 2025 (doi:10.2337/dc25-S002) | B[1], C[5] (cited as 2024 ed in C) | **See note below** |
| WHO/IDF 2006 definition report (ISBN 9241594934) | B[2], D (referenced by name only, no separate citation) | Consistent — same document, same year, same framing |
| Diabetes Prevention Program / DPPOS (Knowler 2009, Lancet, PMC3135022) | D[5] only (sole section citing the DPP paper directly) | Not multiply cited across sections — no cross-section conflict |

**ADA Standards of Care — edition note (B vs C):**
- Section B cites the **2025** ADA Standards (doi:10.2337/dc25-S002, PMC12690183) as its primary diagnostic authority.
- Section C cites the **2024** ADA Standards (PMC9810477, doi unspecified) as [5] for the fasting definition and diagnostic confirmation requirement.
- These are **two different annual editions of the same document**, not two conflicting descriptions of the same paper. Section C's use of the 2024 edition reflects the laboratory-guideline layer (2024 was current when C was authored or the 2024 edition carries the specific lab language cited). The diagnostic thresholds themselves (FPG ≥126 mg/dL for diabetes; 100–125 mg/dL IFG) are **identical** in both editions and are consistently stated in both sections. This is a same-series edition split, not a citation mismatch. **No conflict.**

All other citations are section-local (not repeated across sections with potentially conflicting descriptions).

---

### Institutions

Shared named bodies appearing in 2+ sections, checked for consistent naming/expansion.

| Institution | Sections | Form used | Agreement |
|---|---|---|---|
| ADA (American Diabetes Association) | A, B, C, D | "ADA" / "American Diabetes Association" | Consistent |
| WHO (World Health Organization) | A, B, C, D | "WHO" / "World Health Organization" | Consistent |
| IDF (International Diabetes Federation) | B, C | "IDF" / "International Diabetes Federation" | Consistent |
| IFCC | C | Section-local only | N/A |
| NGSP | C | Section-local only | N/A |
| EFLM | C | Section-local only | N/A |

No naming conflicts. All multi-section institutions are consistently abbreviated and expanded.

---

### Compound Identifiers

Shared molecules, indices, and formulae appearing in 2+ sections.

| Entity | Sections | Values stated | Agreement |
|---|---|---|---|
| mg/dL ↔ mmol/L conversion factor | A, B, C | A: "1 mmol/L = 18.0 mg/dL"; B: "divide mg/dL by 18.0 to obtain mmol/L (more precisely, multiply by 0.0555)"; C: implicit (uses both units, no explicit factor stated) | **Consistent** — all use 18.0; B's parenthetical 0.0555 = 1/18.018, the precise molecular weight factor, is not contradictory (it is the more exact expression) |
| HOMA-IR formula | D only | D[D.5]: HOMA-IR = (fasting insulin [µIU/mL] × fasting glucose [mmol/L]) / 22.5 (or ÷ 405 when glucose in mg/dL) | Section-local only; no cross-section conflict |
| GCK (glucokinase gene) | A (implicit via glucokinase enzyme), D | A describes glucokinase as "GK" or "glucokinase" in the enzymatic context; D uses "GCK" as the gene symbol for MODY2. These are the same gene/enzyme; naming is appropriate to context (gene symbol vs. enzyme name) — no conflict | Consistent |
| GLUT3 / GLUT4 / GLUT1 | A only | Section-local | N/A |
| PEPCK / G6Pase | A, D | A: "PEPCK" and "glucose-6-phosphatase"; D: "PEPCK" and "G6Pase" / "glucose-6-phosphatase" | Consistent — same pathway elements, same directionality (gluconeogenic rate-limiters) |
| PI3K-Akt / FOXO1 | A, D | A: "PI3K-Akt pathway … phosphorylate and inactivate FOXO1 … PEPCK and G6Pase"; D: "insulin … inhibiting the gluconeogenic transcription factor FOXO1 and reducing the expression of G6Pase and PEPCK" | **Consistent** — mechanism and directionality agree |

No compound identifier mismatches.

---

### Regulatory Dates

Guideline years cited in 2+ sections.

| Entity | Sections | Year stated | Agreement |
|---|---|---|---|
| ADA Standards of Care | B (2025), C (2024) | See citation note above — these are genuinely different annual editions; the diagnostic thresholds they carry are identical across sections | **No conflict** |
| WHO/IDF consultation report | B (2006), D (referenced by year in text: "WHO definition 6.1–6.9 mmol/L") | Both sections consistent on 2006 and on the 6.1 mmol/L IFG lower bound | **Consistent** |
| ADA IFG lower-bound history (1997 → 2003 change) | B only | Section-local | N/A |

No regulatory date mismatches.

---

### Trial Registrations

Named trials cited in 2+ sections, checked for consistent results.

| Trial | Sections | Result as stated | Agreement |
|---|---|---|---|
| DPP (Diabetes Prevention Program) | B (named in context of ADA IFG threshold rationale), D[5] (Knowler 2009, specific results) | B names the DPP threshold alignment as rationale for the 2003 ADA IFG change (no numerical result); D gives: lifestyle 58% reduction, metformin 31% reduction in 3-year diabetes incidence; DPPOS 10-year: 34% lifestyle, 18% metformin sustained | B does not state results, only mentions the DPP framing — no numerical conflict |
| PIONEER 2 | D only (Rosenstock 2019, n=816 T2DM, oral semaglutide 14 mg HbA1c −1.4% vs empagliflozin −0.9% at 26 weeks) | Section-local | N/A |
| UKPDS | D only (secondary failure rate: 54% required insulin over 6 years to maintain FPG < 5.9 mmol/L) | Section-local | N/A |

No trial registration mismatches.

---

## Whole-Corpus Tally

| Class | Shared entities examined | Mismatches |
|---|---|---|
| Citations | 2 (ADA SoC series [B/C]; WHO/IDF 2006 [B/D]) | 0 |
| Institutions | 4 (ADA, WHO, IDF, + NGSP/IFCC/EFLM section-local) | 0 |
| Compound identifiers | 5 (conversion factor, HOMA-IR, GCK, PEPCK/G6Pase, FOXO1 axis) | 0 |
| Regulatory dates | 2 (ADA SoC year, WHO/IDF 2006) | 0 |
| Trial registrations | 1 (DPP cross-referenced B↔D) | 0 |
| **Total** | **14** | **0** |

---

## Key Cross-Section Invariants Verified

1. **ADA diabetes threshold:** ≥126 mg/dL / ≥7.0 mmol/L — stated identically in A (deferred to B), B (authoritative), C, and D. **Consistent.**
2. **ADA IFG lower bound:** 100 mg/dL / 5.6 mmol/L — stated in B (authoritative), C (100–125 mg/dL), D (5.6–6.9 mmol/L). **Consistent.**
3. **WHO IFG lower bound:** 110 mg/dL / 6.1 mmol/L — stated in B (authoritative), D ("WHO definition 6.1–6.9 mmol/L"). **Consistent.**
4. **18.0 mg/dL per mmol/L conversion:** A and B both use 18.0; B adds the exact 0.0555 factor (not contradictory). **Consistent.**
5. **HOMA-IR formula:** mmol/L version (÷22.5) and mg/dL version (÷405) both stated in D; not repeated in other sections. **No cross-section conflict.**
6. **8-hour fasting definition:** stated in A ("minimum 8-hour period"), B ("at least 8 hours"), C ("at least 8 hours"). **Consistent.**
7. **Plasma ~10–15% higher than whole blood:** stated in A, confirmed in C. **Consistent.**

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":2,"mismatch_count":0},"institutions":{"scanned":4,"mismatch_count":0},"compound_identifiers":{"scanned":5,"mismatch_count":0},"regulatory_dates":{"scanned":2,"mismatch_count":0},"trial_registrations":{"scanned":1,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
