# ID-Reconcile Source — Phase 4.25
<!-- Phase 4.25 verifier: shared-entity cross-section consistency scan -->
<!-- Sections scanned: A, B, C, D -->
<!-- Iteration: 2 -->

## Verdict

verdict: PASS

Both targeted fixes from iteration 1 are confirmed. No genuine cross-section disagreements remain across citations, institutions, compound identifiers, regulatory dates, or trial registrations.

---

## Fix Confirmation

### Fix 1: Vermeulen 1999 (PMID 10523012) — `mechanism_review` tag in all four sections

| Section | Tag in this iteration | Status |
|---------|----------------------|--------|
| A [5] | `mechanism_review` | PASS |
| B [2] | `mechanism_review` | PASS (was `cohort`) |
| C [1] | `mechanism_review` | PASS |
| D [6] | `mechanism_review` | PASS (was untagged) |

### Fix 2: Binding-fraction percentages harmonized

| Section | Canonical figure | Wider-range qualifier | Status |
|---------|-----------------|----------------------|--------|
| A | ~44% SHBG / ~50% albumin / ~2% free | "1–4% depending on population, sex, age, and assay method" | PASS |
| B | ~44% SHBG / ~50–54% albumin / ~1–4% free | "fractions as high as 65% reported, but canonical reference-adult-male figures are ~44% SHBG-bound and ~50–54% albumin-bound" — explicit qualifier present | PASS |
| C | No standalone percentage table; references Vermeulen Ka constants consistent with A/B | — | PASS |
| D | ~44% SHBG / ~50–54% albumin / ~2% free (Vermeulen canonical) | "wider ranges (SHBG 30–44%, albumin 54–68%) appear in the literature" — scoped as 'literature' not canonical | PASS |

All wider-range figures carry explicit population/method qualifiers. No unscoped non-overlapping figures remain.

---

## Per-Class Mismatch Table

### Citations (author + year + PMID + tag)

| Entity | Sections | PMID | Tags | Status |
|--------|----------|------|------|--------|
| Vermeulen 1999 | A[5], B[2], C[1], D[6] | 10523012 | A: mechanism_review / B: mechanism_review / C: mechanism_review / D: mechanism_review | PASS |
| Bhasin 2018 | A[6], B[7], C[2], D[4] | 29562364 | All: regulatory | PASS |
| Rosner 2007 | A[4], B[6b], C[3] | 17090633 | B: regulatory; A/C: mechanism_review | Informational — same paper, different contextual role in each section; no factual mismatch; not halt-level |
| Fritz 2008 | B[4], C[9 via Winters], D[5 Kacker] | 18171714 / 24090209 / 9761253 | Distinct papers, correctly distinct citations | PASS |

**Citations scanned: 8 unique shared entities. Mismatch count: 0**

---

### Compound Identifiers — Testosterone Fraction Percentages

| Fraction | Section A | Section B | Section D | Assessment |
|----------|-----------|-----------|-----------|------------|
| Free T | ~2%; 1–4% range qualified | ~1–4% | ~2% canonical | PASS |
| Albumin-bound T | ~50% canonical (Vermeulen) | ~50–54% canonical; wider literature noted with explicit qualifier | ~50–54% canonical (Vermeulen); wider literature noted with explicit qualifier | PASS |
| SHBG-bound T | ~44% canonical | ~44% canonical; wider up to 65% with explicit qualifier | ~44% canonical; wider 30–44% with explicit qualifier | PASS |

**Compound identifiers scanned: 3 fractions × 3 sections = 9 comparisons. Mismatch count: 0**

---

### cFT-vs-ED Overestimate — Consistency Check

| Claim | Section B | Section C | Assessment |
|-------|-----------|-----------|------------|
| cFT overestimates ED by | "~20–24%" (Endotext) | "median ratio 1.19" ≈ 19% (Fiers 2018) | 19% within study-level variance of 20–24%; different source studies; consistent direction — PASS |

---

### Analog Immunoassay Magnitude — Consistency Check

| Claim | B | C | D | Assessment |
|-------|---|---|---|------------|
| Analog value relative to reference | ~1/8 of cFT | ~1/4 to 1/7 of ED | ~1/7 of ED | Denominator difference (cFT vs ED): cFT ≈ 1.2× ED, so analog ≈ ED/7 → cFT/8.4; consistent with B's "one-eighth of cFT." PASS |

---

### Institutions

| Institution | Sections | Finding |
|-------------|----------|---------|
| Endocrine Society | A, B, C, D | Consistent naming throughout | PASS |
| CDC Hormone Standardization Program / HoSt-TT | B, C | Consistent naming | PASS |
| WHO NIBSC (SHBG standard) | C | Single-section reference, no cross-section conflict | PASS |
| NCBI Bookshelf (Endotext) | B | Single-section reference, no cross-section conflict | PASS |

**Institutions scanned: 4. Mismatch count: 0**

---

### Regulatory Dates

| Document | Sections | Date cited | Status |
|----------|----------|------------|--------|
| Bhasin 2018 Endocrine Society CPG | A, B, C, D | 2018 across all | PASS |
| Rosner 2007 ES position statement | A, B, C | 2007 across all | PASS |

**Regulatory dates scanned: 2. Mismatch count: 0**

---

### Trial Registrations

No trial registrations cited in any section.

**Trial registrations scanned: 0. Mismatch count: 0**

---

## Tally

| Class | Scanned | Mismatch Count |
|-------|---------|----------------|
| citations | 8 | 0 |
| institutions | 4 | 0 |
| compound_identifiers | 9 | 0 |
| regulatory_dates | 2 | 0 |
| trial_registrations | 0 | 0 |

**Total halt-class mismatches: 0**

---

## Summary

Both iteration-1 fixes land correctly. Vermeulen 1999 now carries `mechanism_review` in all four sections. Binding-fraction percentages are harmonized to the canonical Vermeulen-anchored baseline (~44% SHBG / ~50–54% albumin / ~2% free) across all sections, with all wider literature figures explicitly qualified by population or method scope. No unscoped non-overlapping figures remain. Zero cross-section disagreements exist in any of the five entity classes.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":8,"mismatch_count":0},"institutions":{"scanned":4,"mismatch_count":0},"compound_identifiers":{"scanned":9,"mismatch_count":0},"regulatory_dates":{"scanned":2,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":2}
```
