# ID-Reconcile Phase 4.25 — Serum Sodium

## Verdict

verdict: PASS

---

## Per-Class Mismatch Table

| Entity class | Instances scanned | Mismatches | Notes |
|---|---|---|---|
| Citations (author+year+PMID) | 8 shared-across-section citations examined | 0 | Spasovski 2014 (PMID 24569125) appears in B+D: PMID, DOI, journal, year, pages agree; tier tag differs (1 vs 2) — metadata inconsistency only, not a citation-identity mismatch. Hillier 1999 (PMID 10225241) cited only in B; Adrogué-Madias 2000 PMIDs 10816188 + 10824078 cited only in A — no cross-section conflict possible. |
| Institution names | 0 shared institution identifiers | 0 | No institution names asserted across multiple sections. |
| Compound / biomarker identifiers | 5 shared entities checked (see detail below) | 0 | All agree (see below). |
| Regulatory dates | 0 cross-section regulatory dates | 0 | No regulatory dates shared across sections. |
| Trial registrations | 0 | 0 | No trial registrations cited in any section. |

**Tally: 0 genuine cross-section mismatches.**

---

## Entity-Level Detail

### Reference interval (A + B + D)
- Section A: 135–145 mmol/L (opening paragraph + Clinical Summary)
- Section B: 135–145 mmol/L (Reference Interval table)
- Section D: <135 for hyponatremia, >145 for hypernatremia — consistent
- **Result: AGREE**

### Water-balance-not-salt concept (A + D)
- Section A: "[Na⁺] is a measure of water balance, not of total-body sodium content or dietary salt intake" — the Edelman ratio identity is stated explicitly
- Section D: "Serum sodium ([Na⁺]) is a concentration, not a measure of total-body sodium — it reflects the ratio of sodium to total body water"
- **Result: AGREE — identical conceptual content**

### Pseudohyponatremia mechanism (B + C + D)
- Section B: indirect ISE dilutes sample, assumes 93% water; artifact arises with severe hypertriglyceridemia (>10–15 mmol/L) or hyperproteinemia; confirmed by direct ISE (blood-gas analyzer). Mechanism correctly identified as the dilution assumption failure.
- Section C: same mechanism — "electrolyte exclusion effect"; indirect ISE assumes 0.93 kg/L plasma water; direct ISE is immune; quantified at ~1 mmol/L per 10 mmol/L increment in total lipids. Consistent with B.
- Section D: attributes the artifact to "indirect flame photometry" and states "modern ion-selective electrode methods largely eliminate this artefact." Flame photometry is historically accurate (pseudohyponatremia was first described as a flame artifact, and flame also dilutes), and D's "largely eliminate" could be read as referring to direct ISE eliminating it. However, D's framing is imprecise relative to B+C's explicit teaching that indirect ISE (the dominant modern platform) shares the same vulnerability. **This is a framing imprecision, not a cross-section citation or identifier mismatch.** It does not meet halt criteria.
- **Result: AGREE on mechanism identity (electrolyte exclusion / dilution assumption); framing imprecision in D noted but not a halt trigger**

### Glucose correction factor (B + D)
- Section B: presents BOTH Katz 1973 (+1.6 mmol/L per 100 mg/dL) and Hillier 1999 (+2.4 mmol/L per 100 mg/dL, PMID 10225241); explicitly states Hillier is "now generally preferred."
- Section D: states "corrected sodium rises approximately 1.6 mmol/L for every 5.6 mmol/L increment in glucose above the normal range" — this is the Katz factor only; Hillier is not cited or mentioned.
- Assessment: D presents only one of two legitimate correction factors (the older, less preferred one). D does not contradict the Hillier value — it simply omits it. Per the task brief, flag only if "a section states a DIFFERENT single value contradicting another." D's 1.6 value is a real, published correction factor and is not numerically inconsistent with B's citation of it; D's omission of the 2.4 Hillier factor is a content gap, not a cross-section entity contradiction.
- **Result: OMISSION only (Hillier factor absent from D) — not a halt-level citation or identifier mismatch**

### ODS correction limits (B + D)
- Section B (citing Spasovski 2014 PMID 24569125 + Bastos/Rocha 2023 PMID 37523718): general limit ≤10–12 mmol/L/24h and ≤18 mmol/L/48h; high-risk: 4–6 mmol/L/24h, ceiling 8 mmol/L/24h.
- Section D (citing Spasovski 2014 PMID 24569125 + Sterns 1986 PMID 3713747): "≤6–8 mmol/L per 24 hours (the 2014 European guideline uses 8 mmol/L/24h as the ceiling)." Also cites Sterns 1986: >12 mmol/L/day threshold.
- Both B and D cite the same Spasovski 2014 source (PMID, DOI, journal agree). The characterization differs slightly (B distinguishes general vs. high-risk tiers; D presents 8 mmol/L as the overall ceiling), but both are citing the same underlying document and not contradicting its content. Hypernatremia correction: both B and D agree on 10–12 mmol/L/24h.
- **Result: AGREE on source identity; presentation granularity differs (general vs. high-risk tier distinction) — not a citation-entity mismatch**

### SIADH (B + D)
- Section B: urine Na ≥20–30 mmol/L as the SIADH branch point
- Section D: urine Na typically >40 mmol/L in SIADH diagnostic criteria
- Assessment: Both are citing clinical thresholds, not named citations with PMID. The Spasovski 2014 guideline (shared cite) uses ≥30 mmol/L; some sources use >40. This is a within-topic threshold difference in non-citation clinical criteria. Does not constitute a citation-identity or compound-identifier mismatch.
- **Result: Threshold range difference in clinical criteria — not a halt-level entity mismatch**

### Units mmol/L = mEq/L (A + B + C + D)
- All four sections treat mmol/L and mEq/L as numerically identical for sodium.
- Section B states this explicitly: "numerically identical to milliequivalents per litre (mEq/L) because sodium is monovalent."
- **Result: AGREE across all four sections**

### Spasovski et al. 2014 citation (B + D — shared PMID 24569125)
- Section B: PMID 24569125, DOI 10.1530/EJE-13-1020, Eur J Endocrinol, 2014;170(3):G1–G47 — tier: 1
- Section D: PMID 24569125, DOI 10.1530/EJE-13-1020, Eur J Endocrinol, 2014;170(3):G1–47 — tier: 2
- PMID, DOI, journal, year, volume, issue, pages: **AGREE**. Tier tag differs (1 vs. 2) — internal metadata inconsistency only.
- **Result: Citation identity AGREES; tier inconsistency is a metadata note, not a halt trigger**

---

## Summary

No halt-level cross-section disagreements found. All shared citation identities (author+year+PMID) agree. Shared physiological entities (reference interval, water-balance concept, ODS correction ceiling sources, units) agree across sections. Three sub-halt observations for editorial note: (1) D's pseudohyponatremia framing attributes the artifact primarily to flame photometry and implies modern ISE "largely eliminates" it, which understates indirect ISE's shared vulnerability per B+C; (2) D presents only the Katz 1.6 glucose correction factor, omitting Hillier 2.4 that B explicitly flags as currently preferred; (3) Spasovski 2014 is tagged tier-1 in B and tier-2 in D. None of these constitute entity-class mismatches under the defined halt criteria.

---

```json
{"phase":"4.25","verdict":"PASS","entity_classes":{"citations":{"scanned":8,"mismatch_count":0},"institutions":{"scanned":0,"mismatch_count":0},"compound_identifiers":{"scanned":5,"mismatch_count":0},"regulatory_dates":{"scanned":0,"mismatch_count":0},"trial_registrations":{"scanned":0,"mismatch_count":0}},"halt_reasons":[],"iterations":1}
```
