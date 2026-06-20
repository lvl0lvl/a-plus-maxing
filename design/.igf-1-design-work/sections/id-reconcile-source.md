# Phase 4.25 — ID-Reconcile Verifier: IGF-1

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

### Citations (shared across 2+ sections)

| Citation | Sections | Author/Year/PMID Consistent? | Tag Consistent? | Notes |
|----------|----------|------------------------------|-----------------|-------|
| Katznelson 2014 — Acromegaly CPG | A [5], B [4], D [1] | YES — DOI 10.1210/jc.2014-2700 matches all three; PMID 25356808 present in B+D but **absent from A's bibliography entry** | YES — [regulatory] in all | PMID omission in A is bibliographic incompleteness; DOI uniquely identifies same paper; not a contradiction |
| Molitch 2011 — Adult GHD CPG | B [5], D [2] | YES — PMID 21602453, volume/issue/pages identical | YES — [regulatory] in both | Full agreement |

**Cross-section citation mismatch count: 0** (the Katznelson PMID gap in A is an omission, not a conflict — same DOI resolves to same record)

### Shared Entities — Agreement Check

| Entity Class | Claim in Source Section | Claim in Cross-Section | Agreement? |
|---|---|---|---|
| GH/IGF-1 axis framing | A: GHRH→GH→IGF-1; JAK2/STAT5b; negative feedback at hypothalamus + pituitary | B/C/D: all reference GH/IGF-1 axis consistently without introducing alternative mechanistic claims | AGREE |
| Age-dependence / age-SDS mandatory | A: "all clinical interpretation requires comparison to age- and sex-matched reference ranges" [Katznelson 2014] | B: central organizing principle; SDS >+2 = elevated; "presenting a single adult reference range is clinically misleading" | C: "serial monitoring must use the same assay and its own matched age-sex reference population" | D §D.7: "Age-SDS is mandatory"; 100 ng/mL example | AGREE — all four sections consistent and mutually reinforcing |
| IGF-1 half-life (ternary complex) | A: "approximately 15 hours" (ternary complex); also states "12–15 hours" for ternary complex in IGFBP section | C §Pre-Analytics: "approximately 12–15 hours when bound in the ternary complex" [Skjaerbaek 2000] | AGREE — A's "approximately 15 hours" rounds to the upper end of C's "12–15 hours" range; same cited mechanism, not a contradiction |
| No clinically significant diurnal variation | A: "IGF-1 serum concentrations exhibit no meaningful diurnal variation" [Al-Samerria 2021] | C: "total serum IGF-1 shows no clinically significant circadian variation" [Skjaerbaek 2000] | AGREE — consistent claim, independent supporting citations |
| IGFBP binding fractions | A: <1% free; >98% IGFBP-bound; IGFBP-3 accounts for 75–90%; 150 kDa ternary complex | C: "More than 90% of circulating IGF-1 travels as part of a ternary complex" | AGREE — C's 90% ternary-complex figure is a subset of A's >98% total-bound figure; remainder bound to other IGFBPs (IGFBP-1, IGFBP-2); no conflict |
| IGFBP interference / assay dissociation | A: binding proteins extend half-life and create circulating reservoir | C: IGFBP interference blocks antibody epitopes; acid-ethanol + IGF-II excess dissociation strategies | AGREE — A covers biology; C covers assay consequence; complementary, not contradictory |
| Acromegaly first-line screen | B [4, Katznelson 2014]: "Elevated IGF-1 is the recommended first-line biochemical screening test for acromegaly"; SDS >+2 threshold | D [1, Katznelson 2014]: "recommends measuring serum IGF-1 — age-adjusted — as the initial screen"; normalisation as primary treatment target | AGREE — same guideline, consistent characterisation, same PMID 25356808 |
| Low IGF-1 not specific to GHD | B: "a subnormal IGF-1 is supportive evidence, but confirmation requires dynamic GH stimulation testing" [Molitch 2011] | D §D.2: "low IGF-1 is not specific to GHD" [Molitch 2011]; lists malnutrition, liver disease, diabetes, hypothyroidism, oral oestrogen, aging, systemic illness | AGREE — consistent interpretive caveat, same guideline citation, same PMID 21602453 |
| Units ng/mL = µg/L | A: "ng/mL (equivalent to µg/L)" | B: "1 ng/mL = 1 µg/L"; document uses ng/mL throughout | D: ng/mL throughout | AGREE |

### Institutions

| Institution | Sections | Consistent? |
|---|---|---|
| Endocrine Society (issuing body for both CPGs) | A, B, D | AGREE |

**Institution-name mismatch count: 0**

### Compound Identifiers

| Identifier | Sections | Consistent? |
|---|---|---|
| IGF-1 / Insulin-like growth factor 1 / somatomedin C | A, B, C, D | AGREE |
| IGFBP-3 / insulin-like growth factor binding protein-3 | A, C, D | AGREE |
| ALS / acid-labile subunit | A, C | AGREE |
| WHO IS 02/254 (IGF-1 WHO International Standard) | C only | N/A (single section) |

**Compound-identifier mismatch count: 0**

### Regulatory Dates

| Date/Milestone | Sections | Consistent? |
|---|---|---|
| Katznelson 2014 CPG publication year | A, B, D | AGREE — all cite 2014 |
| Molitch 2011 CPG publication year | B, D | AGREE — both cite 2011 |

**Regulatory-date mismatch count: 0**

### Trial Registrations

No trial registration numbers appear in any of the four sections.

**Trial-registration mismatch count: 0**

---

## Tally

| Class | Scanned | Mismatches |
|---|---|---|
| Citations | 2 shared (Katznelson 2014 × 3 sections; Molitch 2011 × 2 sections) | 0 |
| Institutions | 1 | 0 |
| Compound identifiers | 4 | 0 |
| Regulatory dates | 2 | 0 |
| Trial registrations | 0 | 0 |

**Total mismatches: 0. Verdict: PASS.**

One bibliographic incompleteness noted (Section A citation [5] omits PMID 25356808 for Katznelson 2014; DOI 10.1210/jc.2014-2700 is present and resolves unambiguously). This is a metadata gap in one section's bibliography, not a cross-section disagreement.

---

## Machine-Readable Block

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":2,"mismatch_count":0},"institutions":{"scanned":1,"mismatch_count":0},"compound_identifiers":{"scanned":4,"mismatch_count":0},"regulatory_dates":{"scanned":2,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
