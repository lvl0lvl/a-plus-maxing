# ID-Reconcile Phase 4.25 — ALT Biomarker Report

## Verdict

verdict: PASS

---

## Entity Class Scan

### 1. Citations (author + year + PMID, cross-section matches)

| Citation | Sections | A details | Other section details | Agreement? |
|---|---|---|---|---|
| Kim WR et al. 2008, PMID 18366115 | A + D | A[1]: Hepatology 2008;47(4):1363-1370, PMID 18366115, DOI 10.1002/hep.22109 | D[5]: same title, same journal/year/volume/pages, same PMID 18366115 | AGREE |
| Schumann G et al. 2002, PMID 12241021 | A + C | A[3]: Clin Chem Lab Med 2002;40(7):718-724, PMID 12241021 | C[1]: same journal/year/volume/pages, same PMID 12241021; minor formatting difference (A: "Franck PFH", C: "Franck PF") — non-substantive author-name abbreviation variant | AGREE (trivial name abbreviation only) |
| Cohen JA, Kaplan MM 1979, PMID 520102 | A + D | A[7]: Dig Dis Sci 1979;24(11):835-838, PMID 520102 | D[6]: same author pair, same journal/year/volume/pages, same PMID 520102 | AGREE |
| Prati D et al. 2002, PMID 12093239 | B only (A cross-reference by content) | B[3]: Ann Intern Med 2002;137(1):1-10, PMID 12093239 | D cross-references "Section B: Reference Ranges" for ULN discussion but does not independently cite Prati — not a cross-section citation disagreement | N/A (single citation locus) |

**Citations scanned: 3 shared (Kim 2008, Schumann 2002, Cohen/Kaplan 1979). Mismatches: 0.**

---

### 2. Compound / Enzyme Identifiers

| Identifier | Sections mentioning | Agreement? |
|---|---|---|
| ALT = alanine aminotransferase (EC 2.6.1.2) | A (explicit EC number) | Only A states EC number; B/C/D use the name — no conflict |
| AST = aspartate aminotransferase (EC 2.6.1.1) | A (explicit) | Consistent across all sections |
| PLP / P5P / pyridoxal-5'-phosphate | A, C, D | A: "PLP-dependent enzyme", "pyridoxal-5'-phosphate"; C: "P5P (also called PLP or vitamin B6 coenzyme)"; D: "pyridoxal-5-phosphate (vitamin B6)" — all refer to same entity, consistent nomenclature |
| Units: U/L | B, C, D | B: "U/L (units per liter), synonymous with IU/L"; C: "units per liter (U/L), where 1 U = ..."; D uses U/L throughout | AGREE |
| ALT1 (GPT1) cytosolic; ALT2 (GPT2) mitochondrial | A only | Not contradicted elsewhere |
| NADH at 340 nm | C only | Not contradicted elsewhere |

**Compound identifiers scanned: 5 shared. Mismatches: 0.**

---

### 3. Liver-Specificity / Injury-Not-Function Framing (A ↔ D)

- **Section A** (Release Mechanism): "ALT measures **hepatocellular injury** (disruption of the hepatocyte plasma membrane), not **hepatic synthetic function**"; "a liver can be inflamed and leaking ALT while its synthetic capacity ... remains intact, and conversely, end-stage cirrhosis ... may show a paradoxically low or falling ALT despite severe functional impairment."
- **Section D** (Limitations): "ALT reflects hepatocellular **injury**, not hepatic **function** — synthetic capacity (albumin, INR, bilirubin) is the independent complement." Also: "'Burnt-out' cirrhosis — where end-stage fibrotic replacement has eliminated most viable hepatocytes — can present with normal or even low ALT because there is insufficient functional hepatocellular mass left to release the enzyme."

**Assessment: Fully consistent. Both sections independently articulate the same injury-not-function distinction and the same paradox of low ALT in end-stage cirrhosis. AGREE.**

---

### 4. Conventional ULN + Lower Healthy Threshold (Prati 30/19) — B authoritative

- **Section B (authoritative)**: Prati 2002 — "updated healthy ULN thresholds of **30 U/L for men and 19 U/L for women**." ACG 2017 guideline endorses "**29–33 IU/L for males and 19–25 IU/L for females**."
- **Section D**: Does not cite Prati figures independently. States "the conventional ULN is population-derived and widely agreed to be too high, particularly for women and metabolically healthy lean individuals (cross-reference Section B: Reference Ranges)." Explicitly defers to Section B for ULN figures.

**Assessment: D explicitly cross-references B and does not independently assert figures — no conflict. AGREE.**

---

### 5. De Ritis Ratio (A intro ↔ D evidence)

| Claim | Section A | Section B | Section D |
|---|---|---|---|
| Origin | "first described by Fernando De Ritis in 1957" | Mentioned in passing (AST/ALT ratio context) | "first described in 1957" [D5 Kim 2008] |
| ALD pattern | "ratio characteristically exceeds 2:1" | "AST:ALT >2 in ~90% of cases" in ALD | "AST:ALT ratio above 2.0 predicted ... alcoholic liver disease" (Cohen & Kaplan 1979) [D6] |
| MASLD pattern | "In most acute hepatocellular insults ... ALT exceeds or equals AST (De Ritis ratio ≤ 1)" | "In early MASLD ... ALT often exceeds AST ... De Ritis ratio ... typically <1" | "Ratio <1 → MASLD and acute viral hepatitis" |
| Mechanism (ALD) | "mitochondrial injury is prominent and hepatic pyridoxine depletion preferentially suppresses ALT synthesis" | "alcohol-mediated depletion of pyridoxal phosphate (needed for ALT synthesis)" | "alcohol depletes pyridoxal-5-phosphate (vitamin B6), a cofactor for ALT synthesis more than for AST, selectively suppressing ALT" |

**Assessment: All three sections agree — ALD gives ratio >2, MASLD/acute hepatitis gives ratio <1. Mechanistic explanation is consistent (mitochondrial AST release + PLP depletion suppressing ALT in ALD). AGREE.**

---

### 6. IFCC / P5P Measurement (C ↔ A cross-check)

- **Section A**: "ALT is a PLP-dependent enzyme ... clinical states of vitamin B6 depletion ... can suppress measured serum ALT and AST values even in the presence of significant hepatocellular injury" [A3 = Schumann 2002 IFCC, same PMID as C[1]].
- **Section C**: Full IFCC reference procedure detail. Specifies P5P supplementation is required; documents that non-P5P assays underestimate ALT. Cites Schumann 2002 (PMID 12241021) as C[1].
- **Section D**: "ALT requires pyridoxal-5-phosphate as a cofactor; deficiency suppresses enzyme activity, causing artifactual under-reading of true hepatocellular injury. This is a recognized mechanism in hemodialysis patients."

**Assessment: All three sections consistently describe P5P/PLP dependence and the suppression effect in deficiency. The IFCC citation (Schumann 2002, PMID 12241021) appears in both A and C with matching identifiers. AGREE.**

---

### 7. ×ULN Bands (B ↔ D)

| Band | Section B | Section D |
|---|---|---|
| Mild (<5× ULN) | "<5× ULN: MASLD, alcohol (mild), DILI, thyroid, celiac, chronic viral hepatitis" | "<5× ULN" named as "mild-to-moderate chronic elevation"; same differential (MASLD, ALD, chronic viral hepatitis, DILI, thyroid, celiac) |
| Moderate (5–15× ULN) | "5–15× ULN: acute viral hepatitis A/B/C/E, DILI, autoimmune hepatitis" | Not separately labeled; D uses ">10–25× ULN" for the severe band |
| Marked (>15× ULN) | ">15× ULN: ischemic hepatopathy, toxic hepatitis; >10,000 U/L almost exclusively ischemic or toxic" | ">10–25× ULN: acute viral hepatitis up to 100× ULN, ischemic hepatitis ≥20× ULN, acetaminophen overdose >100× ULN" |

**Assessment:** The band labels differ slightly in how the moderate/severe boundary is drawn (B uses 5–15× / >15×; D uses <5× / >10–25× without a separate moderate category), but this is an organizational difference in how the sections are structured, not a factual contradiction — the underlying diagnostic categories and the claim that ischemic hepatopathy produces the highest elevations are consistent. The DILI ≥3× ULN trigger and Hy's Law (ALT ≥3× ULN + bilirubin ≥2× ULN) appear in both B (implicitly, through the mild band description) and D (explicitly). **No factual disagreement. AGREE.**

---

### 8. Regulatory Dates / Guideline Years

| Document | Section | Year cited |
|---|---|---|
| ACG Clinical Guideline (Kwo, Cohen, Lim) | B | 2017; PMID 27995906 |
| AASLD HBV Guidance (Terrault et al.) | B | 2018; PMID 29405329 |
| IFCC Part 4 reference procedure (Schumann) | A, C | 2002; PMID 12241021 |
| Cohen & Kaplan De Ritis paper | A, D | 1979; PMID 520102 |

No regulatory document year is cited differently across sections.

**Regulatory dates scanned: 4. Mismatches: 0.**

---

### 9. Trial / Study Registrations

No clinical trial registration numbers (NCT, ISRCTN, EudraCT) appear in any section. Not applicable.

**Trial registrations scanned: 0. Mismatches: 0.**

---

## Mismatch Tally

| Entity Class | Scanned | Genuine mismatches |
|---|---|---|
| Citations (author + year + PMID) | 3 shared | 0 |
| Institutions / guideline bodies | 4 (ACG, AASLD, IFCC, JCTLM) | 0 |
| Compound identifiers (ALT, AST, PLP/P5P, units) | 5 | 0 |
| Regulatory dates / guideline years | 4 | 0 |
| Trial registrations | 0 | 0 |

**Total mismatches: 0. Verdict: PASS.**

---

## Summary

All shared entities across sections A, B, C, and D are in agreement. The three cross-section citations (Kim 2008 PMID 18366115; Schumann 2002 PMID 12241021; Cohen & Kaplan 1979 PMID 520102) carry consistent author lists, journal details, and PMIDs. The injury-not-function framing, De Ritis ratio directionality (ALD >2, MASLD <1), Prati 30/19 U/L figures, PLP/P5P dependence, and ×ULN band differentials are factually consistent across sections. The sole surface-level variation (Schumann author "Franck PFH" in A vs "Franck PF" in C) is a non-substantive name-abbreviation difference, not a citation identity mismatch.

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":3,"mismatch_count":0},"institutions":{"scanned":4,"mismatch_count":0},"compound_identifiers":{"scanned":5,"mismatch_count":0},"regulatory_dates":{"scanned":4,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
