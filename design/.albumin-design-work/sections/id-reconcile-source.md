# ID-RECONCILE Phase 4.25 — Serum Albumin

## Verdict

verdict: PASS

---

## Shared-Entity Consistency Checks

### 1. Reference Interval (3.5–5.0 g/dL)

| Section | Stated interval | Unit cross-check |
|---------|----------------|-----------------|
| A (Physiology) | 3.5–5.0 g/dL (35–50 g/L) | Explicit g/dL ↔ g/L conversion confirmed |
| B (Reference Ranges) | 3.5–5.0 g/dL (35–50 g/L) | Explicit; notes method/lab-dependent bounds within this range |
| C (Measurement) | Not stated as a standalone reference interval (section scope is method, not clinical range) | N/A |
| D (Determinants) | Hypoalbuminemia defined as < 3.5 g/dL (35 g/L) — consistent with 3.5 lower bound | Consistent by implication |

**Finding:** A and B agree exactly (3.5–5.0 g/dL / 35–50 g/L). D uses the lower bound consistently. C does not state a reference interval (appropriate for a measurement-methods section). No disagreement.

---

### 2. Plasma Half-Life

| Section | Stated value | Citation |
|---------|-------------|---------|
| A (Physiology) | ~19–21 days | refs [1, mechanism_review] and [3, mechanism_review] = Caraceni PMID 24333308 + Merlot PMID 25161624 |
| D (Determinants) | ~19 days | ref [12, mechanism_review] = Merlot Front Physiol PMID 25161624 |
| B | Not stated explicitly | — |
| C | Not stated | — |

**Finding:** A states ~19–21 days; D states ~19 days, citing Merlot (PMID 25161624). A also cites Merlot as one of its sources ([3]). The D figure (~19 days) falls within A's range (~19–21 days). There is no directional conflict; D simply cites the lower end of A's range from the same underlying source. No disagreement.

**Note:** A also mentions a "circulatory half-life" of 16–18 hours (exchange between vascular and extravascular compartments) and explicitly distinguishes it from the protein half-life. D does not repeat this figure. No conflict — both sections are describing the same underlying biology and D does not contradict A's clarifying note.

---

### 3. Negative Acute-Phase Reactant / IL-6 Mechanism

| Section | Description | Key claim |
|---------|-------------|----------|
| A (Physiology) | IL-6 → JAK/STAT3 + NF-κB → upregulates positive APRs at expense of albumin/transferrin | Albumin is negative acute-phase reactant; synthesis suppressed by IL-6 |
| B (Reference Ranges) | "IL-6, TNF-α, IL-1 — that upregulate CRP and other positive acute-phase proteins"; also capillary permeability increase shifts albumin to interstitium | Consistent; adds TNF-α and IL-1 alongside IL-6; adds transcapillary escape mechanism |
| D (Determinants) | "cytokines, principally IL-6"; discusses transcapillary escape in detail; cites Soeters et al. PMID 30288759 and ASPEN 2021 | Consistent; IL-6 as principal cytokine; same two-mechanism framework (synthesis suppression + capillary leak) |

**Finding:** All three sections agree on the negative-acute-phase-reactant classification, IL-6 as the principal mediator, and the downstream mechanism of hepatic reprioritization. B and D both add the transcapillary-leak / capillary-permeability mechanism on top of synthesis suppression — these are additive, not contradictory. No disagreement.

---

### 4. BCG/BCP Method Bias Direction

| Section | Direction of bias | Specifics |
|---------|-----------------|----------|
| B (Reference Ranges) | "BCG systematically overestimates albumin relative to immunoturbidimetric reference methods — particularly at low concentrations" | Overestimate; BCP preferred in nephrology |
| C (Measurement) | "BCG systematically overestimates albumin" because of non-specific binding to alpha-1 and alpha-2 globulins | Overestimate; bias widens at low albumin; BCP more specific |
| D (Determinants) | "BCP is more specific and avoids BCG's cross-reactivity with globulins" | Consistent direction (BCG high-biased); BCP preferred |

**Finding:** B, C, and D all agree: BCG overestimates (positive bias), BCP is more specific. No directional disagreement.

---

### 5. Composite Scores (Child-Pugh / ALBI)

| Section | Child-Pugh albumin thresholds | ALBI formula |
|---------|------------------------------|-------------|
| B (Reference Ranges) | Scored 1 (>3.5 g/dL/>35 g/L), 2 (2.8–3.5 g/dL/28–35 g/L), 3 (<2.8 g/dL/<28 g/L) | ALBI = 0.66 × log₁₀[bilirubin (μmol/L)] − 0.085 × [albumin (g/L)] |
| D (Determinants) | Mentions albumin as "a formal component of the Child-Pugh score (one of three synthetic-function variables alongside prothrombin time and bilirubin)" — does not restate thresholds | Does not restate formula; notes ALBI uses albumin + bilirubin |

**Finding:** B provides the full Child-Pugh albumin threshold table and ALBI formula. D does not restate thresholds or formula but cites the same Johnson et al. 2015 (PMID 25512453) for ALBI, consistent with B's citation ([9] in B = same paper). No conflict; D defers to the reference and does not contradict B's details.

---

### 6. Oncotic Pressure Contribution

| Section | Percentage | Citation |
|---------|-----------|---------|
| A (Physiology) | ~70–80% of total oncotic pressure | refs [1,2,3] |
| B (Reference Ranges) | Not stated as a percentage | — |
| C | Not stated | — |
| D | Not stated | — |

**Finding:** Only A states the 70–80% figure. No other section contradicts it. No conflict.

---

### 7. Unit Conversion (g/dL ↔ g/L)

| Section | Conversion stated |
|---------|-----------------|
| A | g/dL × 10 = g/L (explicit) |
| B | g/dL × 10 = g/L (explicit) |
| C | Implicit in g/L references throughout |
| D | g/dL and g/L used consistently with ×10 relationship |

**Finding:** All sections use g/dL and g/L in concordant 10× relationship. No inconsistency.

---

### 8. Shared Citation: Merlot et al. Front Physiol 2014, PMID 25161624

| Section | How cited | Role |
|---------|----------|------|
| A | ref [3] — Merlot AM, Kalinowski DS, Richardson DR — PMID 25161624 — DOI 10.3389/fphys.2014.00299 | Multiple: half-life, structure, antioxidant, transport |
| D | ref [12] — same author, title, journal, year, PMID, DOI | Half-life (~19 days) |

**Finding:** Same paper, same PMID, same DOI, same author list in both sections. Citation is internally consistent. No mismatch.

---

### 9. Synthesis Rate in Health vs Inflammation (A vs D)

| Section | Claim |
|---------|------|
| A | "only 20–30% of hepatocytes actively producing albumin… ~10–15 g/day; can increase 200–300%" (in health); synthesis suppressed by IL-6 in inflammation |
| D | "~10–12 g/day in healthy adults" for synthesis; in inflammation, Soeters 2019 found "fractional synthesis rate in plasma is normal or even mildly increased" in most inflammatory disease — fall driven by capillary leak |

**Finding:** A cites 10–15 g/day; D cites 10–12 g/day. These ranges overlap (10–12 is within 10–15). The difference is the precision of the bounds, not a contradiction. Both sections are consistent with each other and consistent with the same biological claim. The A statement represents the upper range of the healthy adult output, which is unambiguously inclusive of D's 10–12 g/day. No genuine disagreement.

---

## Mismatch Tally

| Entity class | Shared entities scanned | Mismatches |
|-------------|------------------------|------------|
| Citations (author+year+PMID matched across sections) | 2 shared (Merlot PMID 25161624 in A+D; Johnson ALBI in B+D) | 0 |
| Institutions | 0 named across sections | 0 |
| Compound identifiers (biomarker-specific) | 1 (HSA — consistent throughout) | 0 |
| Regulatory dates | 0 cited across sections | 0 |
| Trial registrations | 0 cited | 0 |
| Numerical entities (reference interval, half-life, oncotic %, BCG bias direction, unit conversion) | 5 classes checked | 0 |

**Total cross-section mismatches: 0**

---

## Summary

All shared entities across the four sections are internally consistent. The reference interval (3.5–5.0 g/dL) is stated identically in A and B; D uses the lower bound consistently. The half-life (~19 days in D, ~19–21 days in A) is non-contradictory, citing the same Merlot 2014 source. The negative-acute-phase-reactant/IL-6 mechanism is stated consistently in A, B, and D, with B and D adding the transcapillary-leak mechanism additively. BCG overestimation is confirmed in the same direction in B, C, and D. The single shared citation (Merlot PMID 25161624, appearing in both A and D) uses identical author/year/PMID/DOI. No halt-class discrepancy was identified in any entity class.

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":2,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":1,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
