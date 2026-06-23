# Phase 4.25 — ID-Reconcile Gate
**Compound:** Cerebrolysin | **Date:** 2026-06-22 | **Iterations:** 1

---

## Verdict

verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "iterations": 1,
  "entity_classes": {
    "citations": {
      "scanned": 7,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 3,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 1,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 4,
      "mismatch_count": 0,
      "mismatches": []
    },
    "trial_registrations": {
      "scanned": 5,
      "mismatch_count": 0,
      "mismatches": []
    }
  },
  "halt_reasons": []
}
```

---

## Per-Class Prose Tables

### Citations (shared PMIDs scanned = 7)

| PMID | Sections | Author/Year/Journal | Tag consistency | Author-integrity flag | Status |
|------|----------|--------------------|-----------------|-----------------------|--------|
| 22282884 (CASTA / Heiss 2012, Stroke) | B[1], C[12] | Consistent | `rct` both | n/a | PASS |
| 22514792 (Masliah 2012, Drugs Today) | A[8], C[2] | Consistent | `mechanism_review` both ✓ | **FIXED** — flag now in A[8]; was absent | PASS (fixed) |
| 26564102 (CARS / Muresanu 2016, Stroke) | B[2], C[11], E[1] | Consistent | `rct` all | n/a | PASS |
| 29248999 (Bornstein 2018, Neurol Sci) | C[10], E[3] | Consistent | `meta_analysis` both | n/a | PASS |
| 31710397 (VaD Cochrane / Cui 2019) | B[9], C[9], E[7] | Consistent | `meta_analysis` all | n/a | PASS |
| 37818733 (Cochrane 2023 / Ziganshina) | A[2], B[3], C[8], D[8], E[6] | Consistent | `meta_analysis` all | n/a | PASS |
| 38737662 (Seidl & Aigner 2024, J Med Life) | A[7], D[5] | Consistent | **FIXED** — A corrected from `mechanism_review` → `in_vitro`; D was already `in_vitro` | n/a | PASS (fixed) |

**eutils verification (PMID 38737662):** PubMed publication type = "Journal Article; Comparative Study." This is a primary analytical composition comparison, not a review. `in_vitro` is the correct design tag. Section D had the correct tag; Section A has been corrected.

**eutils verification (PMID 22514792):** PubMed publication type = "Journal Article; Review." `mechanism_review` is the correct tag in both A and C. Tag inconsistency: none. Integrity-flag inconsistency: resolved.

### Institutions (scanned = 3)

| Institution | Sections present | Consistent? |
|-------------|-----------------|-------------|
| Ever Neuro Pharma GmbH, Unterach, Austria | A, D, E | YES — named consistently; "formerly EBEWE" noted where relevant |
| NIH ORI (misconduct determination, Sept 2024) | C, E | YES — same date/scope in both sections |
| Paracelsus Medical University, Salzburg (Seidl & Aigner affiliation) | D[5] only | n/a — appears in one section only; no conflict |

### Compound Identifiers (scanned = 1 — Cerebrolysin preparation characteristics)

| Attribute | Section A | Section C | Section D | Section E | Status |
|-----------|-----------|-----------|-----------|-----------|--------|
| Source organism | porcine brain cortex | porcine brain | porcine brain tissue | porcine brain | Consistent ✓ |
| Preparation method | enzymatic proteolysis | enzymatic hydrolysis | enzymatic hydrolysis | enzymatic hydrolysis | Consistent ✓ |
| MW cutoff | <10 kDa | below 10,000 Da | <10 kDa | — | Consistent ✓ |
| Gross composition ratio | 85% AA / 15% peptides | **FIXED** → 85%/15% | 85%/15% (implied via Seidl ref) | — | PASS (fixed) |
| BDNF/GDNF/NGF/CNTF absent | confirmed [4, in_vitro] | confirmed [1] | — | — | Consistent ✓ |
| "Mimicry-not-delivery" framing | explicit A.4.1 | explicit C.1 | — | — | Consistent ✓ |
| Manufacturer | Ever Neuro Pharma GmbH | — | Ever Neuro Pharma GmbH | Ever Neuro Pharma GmbH | Consistent ✓ |
| Route | IV/IM | — | IV/IM | IV/IM | Consistent ✓ |

### Regulatory/Efficacy Facts (scanned = 4)

| Fact | Sections | Consistent? |
|------|----------|-------------|
| CASTA null-on-primary (Heiss 2012, PMID 22282884) | B, C | YES — both state primary endpoint null; post-hoc subgroup consistent |
| Cochrane 2023 non-fatal SAE signal RR 2.39 (95% CI 1.10–5.23) | B[3], C[8], D[8], E[6] | YES — exact figure consistent across all sections |
| Approved ~50 countries, not FDA/EMA-central | A[A.1], D[D.1], E[E.2] | YES — consistent framing; EMA national vs. centralized distinction consistent |
| Masliah NIH ORI finding: Sept 2024, 132 papers, 8 Cerebrolysin-specific | C[4], E[16] | YES — consistent |
| Rockenstein retractions: PMID 25047000 (Dec 2025), PMID 26611895 (Mar 2025) | C[6,7], E[16] | YES — consistent retraction dates and bases |
| Manufacturer-associated share ~60–70% | E[E.1.2] | Appears in E only — no conflict with other sections |
| VaD Cochrane all-outcomes very-low-certainty | B[9], C[9] | YES — consistent |

### Trial Registrations (scanned = 5)

| Trial | Registration | Sections | Consistent? |
|-------|-------------|----------|-------------|
| CASTA | ClinicalTrials.gov (not explicitly cited in sections) | B, C | n/a — both cite PMID 22282884 consistently |
| CARS | ClinicalTrials.gov NCT01406860 (not explicitly cited) | B, C, E | n/a — all cite PMID 26564102 consistently |
| CAPTAIN I | NCT01606111 | B[10], E[2] | Consistent — B cites PMID 31494820; E cites NCT |
| CAPTAIN II | NCT01606111 (same program) | B[11] | Consistent |
| CEREHETIS | NCT not cited | D[9], C | Consistent — both reference Kalinin post-hoc |

---

## Summary of Fixes Applied

1. **Section A [7] — PMID 38737662 tag:** `mechanism_review` → `in_vitro` (eutils-verified: Comparative Study / Journal Article, not a review). Tier updated 3 → 2. PMC ID added.
2. **Section A [8] — PMID 22514792 Masliah flag:** Author-integrity annotation added to bibliography entry matching Section C. Inline provisional caveats added to A.4.1, A.4.3, A.4.4, and A.4.5 table.
3. **Section C — Composition ratio:** "75% / 25%" corrected to "85% / 15%" with note on the Hartbauer variant, matching Sections A and D.

All three fixes were genuine divergences (not per-section intentional differences). No unresolvable divergences remain. Verdict: PASS.
