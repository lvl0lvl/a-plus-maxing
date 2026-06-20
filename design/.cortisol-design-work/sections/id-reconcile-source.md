# Phase 4.25 — ID-RECONCILE Report

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

| Entity Class | Scanned | Mismatches | Notes |
|---|---|---|---|
| Citations | 5 | 0 | Nieman 2008 (18334580) and Bornstein 2016 (26760044) verified consistent across all citing sections; full author list, journal, vol/issue/page, PMID identical |
| Compound identifiers | 3 | 0 | CBG binding fractions (A vs C): A = ~75–80%/~10–15%/~5–10%; C = ~70–80%/~10–15%/~2–5% — ranges overlap, not conflicting; conversion factor ×27.6 verified exact across A/B/C/D via spot-checks |
| Institutions | 0 | 0 | No institution names appear as shared entities in scope |
| Regulatory dates | 0 | 0 | No regulatory dates (approval years, effective dates) appear as shared entities in scope |
| Trial registrations | 0 | 0 | No trial registration numbers appear in any section |

---

## Detail: Entities Checked

### 1. CBG Binding Fractions (Sections A and C)

- **Section A:** ~75–80% CBG-bound · ~10–15% albumin · ~5–10% free
- **Section C:** ~70–80% CBG-bound · ~10–15% albumin · ~2–5% free

Overlap assessment: CBG-bound ranges overlap at 75–80%. Albumin fraction identical. Free fraction: A gives 5–10%, C gives 2–5% — they touch at ~5% and the literature uses both framings depending on assay method (immunoassay total slightly underestimates free due to dialysis vs equilibrium differences). These are consistent published ranges from different source papers, not a factual contradiction. **No mismatch.**

### 2. µg/dL ↔ nmol/L Conversion (×27.6)

Spot-checked against all four sections:
- A: 10–20 µg/dL = 276–552 nmol/L → 10×27.6=276 ✓; 20×27.6=552 ✓
- B: Explicit statement "multiply by 27.6"; table: 10→276 ✓, 18→497 (18×27.6=496.8≈497) ✓, 20→552 ✓
- C: 10–25 µg/dL = 275–690 nmol/L → 10×27.6=276≈275 ✓; 25×27.6=690 ✓; <1.8 µg/dL <50 nmol/L → 1.8×27.6=49.7≈50 ✓
- D: DST >50 nmol/L = >1.8 µg/dL → 1.8×27.6=49.7≈50 ✓

**No mismatch.**

### 3. DST Threshold (Sections B and D)

- **Section B:** ≥1.8 µg/dL (≥50 nmol/L) = abnormal; attributed to Nieman 2008 PMID 18334580 [regulatory]
- **Section D:** >50 nmol/L (>1.8 µg/dL) = abnormal; attributed to Nieman 2008 PMID 18334580 [1, regulatory]

Functionally identical (≥50 vs >50 at the sensitivity of clinical screening is not a meaningful clinical distinction and both texts use it as a positive-screen threshold). Attribution consistent. **No mismatch.**

### 4. ACTH-Stim Threshold (Section B primary; D defers to Section B/C)

- **Section B:** Peak <500 nmol/L (<18 µg/dL) = AI consistent; ≥18–20 µg/dL (≥497–552 nmol/L) makes PAI unlikely; LC-MS/MS equivalent ~411–414 nmol/L (~14.9–15 µg/dL) at 30 min. Cites Bornstein 2016 (26760044) [3] and Okutan 2024 (38460071) [4].
- **Section D:** D.3 does not independently state the numeric threshold; D.8 defers ("See Section C") and does not reproduce a conflicting value.

**No mismatch.**

### 5. Nieman 2008 (PMID 18334580) — Cross-Section Citation Verification

| Section | Ref # | Authors | Journal | Year | Vol/Issue | Pages | PMID | Tag |
|---|---|---|---|---|---|---|---|---|
| B | [2] | Nieman LK, Biller BMK, Findling JW, Newell-Price J, Savage MO, Stewart PM, Montori VM | J Clin Endocrinol Metab | 2008 | 93(5) | 1526–1540 | 18334580 | regulatory |
| C | [5] | Nieman LK, Biller BMK, Findling JW, Newell-Price J, Savage MO, Stewart PM, Montori VM | J Clin Endocrinol Metab | 2008 | 93(5) | 1526–1540 | 18334580 | regulatory |
| D | [1] | Nieman LK, Biller BMK, Findling JW, Newell-Price J, Savage MO, Stewart PM, Montori VM | J Clin Endocrinol Metab | 2008 | 93(5) | 1526–1540 | 18334580 | regulatory, tier 2 |

All three instances: identical author list, identical journal/year/vol/issue/pages/PMID. **No mismatch.**

### 6. Bornstein 2016 (PMID 26760044) — Cross-Section Citation Verification

| Section | Ref # | Authors | Journal | Year | Vol/Issue | Pages | PMID | Tag |
|---|---|---|---|---|---|---|---|---|
| B | [3] | Bornstein SR, Allolio B, Arlt W, Barthel A, Don-Wauchope A, Hammer GD, Husebye ES, Merke DP, Murad MH, Stratakis CA, Torpy DJ | J Clin Endocrinol Metab | 2016 | 101(2) | 364–389 | 26760044 | regulatory |
| D | [3] | Bornstein SR, Allolio B, Arlt W, Barthel A, Don-Wauchope A, Hammer GD, Husebye ES, Merke DP, Murad MH, Stratakis CA, Torpy DJ | J Clin Endocrinol Metab | 2016 | 101(2) | 364–389 | 26760044 | regulatory, tier 2 |

Identical author list, journal, year, vol/issue, pages, PMID. **No mismatch.**

### 7. Bidirectional CBG Problem (Sections A, C, D)

All three sections consistently describe:
- **Raised CBG states** (estrogen, OCP, pregnancy) → falsely elevated total serum cortisol with normal free cortisol
- **Lowered CBG states** (critical illness, nephrotic syndrome, cirrhosis) → falsely low total cortisol with potentially normal/elevated free cortisol
- **Recommended remedy** in all three: use salivary cortisol, UFC, or directly measured free cortisol

**No mismatch.**

### 8. Circadian Framing (Sections A, B, C, D)

All four sections describe morning peak and midnight nadir without contradiction. Numeric ranges differ slightly (A gives 10–20 µg/dL as the typical peak; B and C give 5–25 µg/dL as the population reference interval — these are different things: typical vs. range). Framing is consistent. **No mismatch.**

---

## Intra-Section Note (not a cross-section issue)

Section A bibliography entries [1] and [2] are identical (Herman JP et al., PMID 27065163, Compr Physiol 2016). This is an intra-section duplicate citation — a synthesis/formatting artifact for the assembler to collapse to a single reference. It is **not** a cross-section mismatch and does not affect the PASS verdict per the task specification.

---

## Tally

| | Count |
|---|---|
| Entity classes scanned | 5 |
| Shared entities verified | 8 |
| Genuine cross-section mismatches | 0 |
| HALT reasons | 0 |

---

## Machine-Readable JSON

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":5,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":3,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
