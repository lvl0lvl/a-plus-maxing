# ID-RECONCILE — Phase 4.25
## Free T3 Biomarker Report — Cross-Section Entity Verification

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

### 1. Unit Conversion (pg/mL ↔ pmol/L ×1.536)

| Sections | Claim | Agreement |
|----------|-------|-----------|
| A (line 27) | "pg/mL × 1.536 = pmol/L" | — |
| B (line 11) | "×1.536: 1 pg/mL = 1.536 pmol/L (MW T3 = 650.97 g/mol)" | MATCH |
| C | Does not state conversion factor explicitly | N/A |
| D | Does not state conversion factor explicitly | N/A |

Result: A and B agree. No mismatch.

---

### 2. Reference Interval (B authoritative: 2.3–4.2 pg/mL / 3.5–6.5 pmol/L)

| Sections | Claim | Note |
|----------|-------|------|
| A (line 27) | 2.3–4.2 pg/mL (3.5–6.5 pmol/L) | Matches B exactly |
| B (line 5) | 2.3–4.2 pg/mL (3.5–6.5 pmol/L) | Authoritative |
| C (line 5) | "roughly 2–6 pmol/L (~1.3–3.9 pg/mL)" | Describes analytical/detection range, not the euthyroid reference interval; different claim, not contradictory |
| D (line 62) | "~2–6 pg/mL / 3.1–9.2 pmol/L" | Describes circulating concentration range across populations, not the conventional reference interval; math is internally consistent (2×1.536=3.07; 6×1.536=9.22); different claim, not contradictory |

Result: A and B share the same claim (conventional adult reference interval) and agree perfectly. C and D are making different, broader statements about the circulating concentration range — not the same claim as A/B, so no cross-section contradiction.

---

### 3. Deiodinase Physiology + Active-Hormone Framing (A primary; B, C, D in NTI context)

| Entity | A | B | C | D | Agreement |
|--------|---|---|---|---|-----------|
| D1: peripheral T4→T3 conversion, liver/kidney, dominant source of circulating T3 | Yes | Yes (in NTI context) | Yes (in NTI context) | Yes — "~80% of circulating T3 from T4" (circulating fraction, not total production) | CONSISTENT |
| D2: activating, predominantly intracellular, brain/pituitary | Yes | Not stated in NTI section | Not stated | Implied | CONSISTENT |
| D3: inactivating, upregulated in illness, T3→T2 + T4→rT3 | Yes | Yes | Yes | Yes | CONSISTENT |
| T4 as prohormone / T3 as active form | Yes | Yes (implicit) | Yes (implicit) | Yes | CONSISTENT |

Note on D1 percentage: Section A states ~83% of total T3 production is peripheral; Section D states D1 "normally supplies ~80% of circulating T3." These refer to different denominators (total daily production vs. the circulating fraction specifically) and are not contradictory.

---

### 4. T3-Toxicosis Diagnostic Role (B + D)

| Claim | B | D | Agreement |
|-------|---|---|-----------|
| Pattern: isolated fT3 elevation, normal fT4, suppressed TSH | Yes | Yes | MATCH |
| Occurs in early Graves' disease | Yes | Yes | MATCH |
| Occurs in autonomously functioning toxic nodules | Yes | Yes | MATCH |
| ATA guidelines citation | Ross et al. 2016, PMID 27521067 | Ross et al. 2016, PMID 27521067 | MATCH |
| Total T3 preferred over free T3 in practice | Yes (from ATA note) | Yes | MATCH |
| Prevalence figure | ~5% of all thyrotoxicosis (B) | 5–46% of autonomously functioning nodules (D) | DIFFERENT POPULATIONS — not contradictory |

Result: No mismatch. The prevalence figures in B and D refer to different populations (all thyrotoxicosis vs. toxic nodule subset) and are compatible.

---

### 5. NTI / Low-T3 Syndrome Mechanism (B, C, D)

| Mechanism element | B | C | D | Agreement |
|-------------------|---|---|---|-----------|
| D1 downregulation | Yes | Yes | Yes | MATCH |
| D3 upregulation | Yes | Yes | Yes | MATCH |
| rT3 elevation | Yes (implied) | Yes, with caveat: "may be normal or reduced in some NTIS" (Fliers 2021) | Yes | CONSISTENT — C's caveat refines, does not contradict B/D |
| TSH: normal or mildly suppressed (not elevated) | Yes | Yes (normal or slightly suppressed) | Yes (inappropriately normal or mildly suppressed) | MATCH |
| Not primary thyroid disease | Yes | Yes | Yes | MATCH |

Result: No mismatch. The Fliers/Boelen 2021 nuance in C (rT3 not universally elevated) is a refinement, not a contradiction with B or D.

---

### 6. Favresse et al. (PMID 29982406) — Interferences Review

| Section | Citation present | Citation form |
|---------|-----------------|---------------|
| A | No | — |
| B | No | — |
| C | Yes — Favresse J et al. *Endocr Rev.* 2018;39(5):830–850. PMID: 29982406 | Correctly attributed |
| D | No | — |

Result: Cited in C only. Cannot assess cross-section mismatch. Single-section citation — no conflict possible.

---

### 7. ATA Guidelines Citations (Shared across B and D)

| Guideline | B citation | D citation | Agreement |
|-----------|-----------|-----------|-----------|
| 2016 ATA Hyperthyroidism Guidelines | Ross DS et al., *Thyroid* 2016;26(10):1343–1421. PMID: 27521067 | Ross DS et al., *Thyroid* 2016;26(10):1343–1421. PMID: 27521067 | EXACT MATCH |
| 2014 ATA Hypothyroidism Guidelines | Jonklaas J, Bianco AC et al., *Thyroid* 2014;24(12):1670–1751. PMID: 25266247 | Jonklaas J, Bianco AC et al., *Thyroid* 2014;24(12):1670–1751. PMID: 25266247 | EXACT MATCH |

Result: No mismatch.

---

### 8. Welsh & Soldin (cited in C only)

Cited in C as: Welsh KJ, Soldin SJ. *Eur J Endocrinol.* 2016;175(6):R255–R263. PMID: 27737898. Not cited in A, B, or D. Single-section; no cross-section mismatch possible.

---

### 9. Bianco et al. 2019 Review (cited in A; Bianco as author in D)

Section A [1]: Bianco AC et al. *Endocr Rev.* 2019;40(4):1000–1047. PMID: 31033998. Cited in A only as the mechanism review.
Section D [2]: Bianco AC appears as co-author on the Jonklaas 2014 ATA guidelines, a different paper. No citation conflict.

---

## Mismatch Tally

| Entity class | Items scanned | Mismatches |
|--------------|--------------|-----------|
| Citations (author + year + PMID across 2+ sections) | 3 (ATA 2016, ATA 2014, conversion ×1.536) | 0 |
| Institutions (ATA, Endocrine Society) | 2 | 0 |
| Compound identifiers (T3 MW, unit conversions) | 1 | 0 |
| Regulatory dates (guideline years) | 2 | 0 |
| Trial registrations | 0 | 0 |
| **TOTAL** | **8** | **0** |

---

## Summary

All shared entities in 2+ sections agree. The conventional reference interval (2.3–4.2 pg/mL / 3.5–6.5 pmol/L) is stated identically in A and B. The ×1.536 conversion factor is consistent between A and B. All cross-cited ATA guideline papers (PMID 27521067, PMID 25266247) carry identical author, year, journal, volume, and PMID across every section that cites them. Deiodinase physiology, T3-toxicosis framing, and NTI/low-T3 mechanism are internally consistent across all four sections — minor differences in numeric scope (e.g., D1's "~80% of circulating T3" vs. A's "~83% of total T3 production") refer to different denominators and are compatible. No halt conditions met.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":3,"mismatch_count":0},"institutions":{"scanned":2,"mismatch_count":0},"compound_identifiers":{"scanned":1,"mismatch_count":0},"regulatory_dates":{"scanned":2,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
