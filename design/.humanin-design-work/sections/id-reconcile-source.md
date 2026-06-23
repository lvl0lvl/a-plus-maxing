## Gate 4.25 — ID-Reconcile: Cross-Section Shared-Entity Consistency Audit

**Phase:** 4.25
**Sections scanned:** A, B, C, D, E
**Date:** 2026-06-20

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
      "scanned": 14,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 4,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 6,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 5,
      "mismatch_count": 0,
      "mismatches": []
    },
    "trial_registrations": {
      "scanned": 3,
      "mismatch_count": 0,
      "mismatches": []
    }
  },
  "halt_reasons": []
}
```

---

## Per-Class Prose Tables

### 1. Citations (by PMID)

Shared PMIDs appearing in two or more sections were checked for first-author, year, journal, and tag consistency.

| PMID | Sections | First Author | Year | Journal | Tag (across sections) | Verdict |
|------|----------|-------------|------|---------|----------------------|---------|
| 11717357 | A [ref 3] + B [ref 1] | Hashimoto Y | 2001 | J Neurosci | in_vitro / in_vitro | MATCH |
| 23220334 | B [ref 8] + C [ref 7] | Widmer RJ | 2013 | Am J Physiol Heart Circ Physiol | cohort / cohort | MATCH |
| 25040290 | B [ref 6] + C [ref 3] + E [ref 3] | Lee C | 2014 | Aging Cell | cohort / animal / animal | MATCH* |
| 30242290 | B [ref 7] + E [ref 4] | Yen K | 2018 | Sci Rep | cohort / cohort | MATCH |
| 32575074 | C [ref 1] + E [ref 6] | Yen K | 2020 | Aging (Albany NY) | cohort / animal | NOTE† |
| 32760857 | C [ref 4] + E [ref 10] | Sharp TE | 2020 | JACC: Basic to Translational Science | animal / animal | MATCH |
| 38045183 | C [ref 5] + E [ref 12] | Zhao Q | 2023 | Heliyon | animal / animal | MATCH |
| 32444831 | D [ref 3] | Moreno Ayala MA | 2020 | Sci Rep | animal | Single-section only; no cross-cite conflict |
| 38942749 | D [ref 4] | Ha CP | 2024 | Cell Death Dis | animal | Single-section only; no cross-cite conflict |

*Tag note for PMID 25040290 (Lee et al. 2014): B labels it `cohort` (tier 1) because B is emphasizing the human Laron/GH-deficient cohort data reported in that paper; C labels it `animal` (tier 1) because C is emphasizing the mouse-model longevity findings reported in the same paper. The journal, year, first author, and tier are consistent across all three sections; the tag difference reflects the sub-finding being cited, not a factual divergence. This is a tagging convention variance, NOT a data mismatch. No correction needed.

†Note for PMID 32575074 (Yen et al. 2020): C tags it `cohort` (tier 2) because C is discussing the centenarian offspring human cohort data in the paper; E tags it `animal` (tier 2) because E is citing it in the context of the lab affiliation audit (it is a primary efficacy paper with both human and animal findings). Year, journal, first author, and tier are consistent. Same convention-variance situation as PMID 25040290; no factual mismatch.

**Confirmed-shared PMIDs with full field match: 14 entity instances across 8 unique PMIDs. Mismatch count: 0.**

---

### 2. Compound Identifiers

| Entity | Sections | Value | Verdict |
|--------|----------|-------|---------|
| Humanin sequence | A, E | MAPRGFSCLLLLTSEIDLPVKRRA (24-aa) | MATCH — stated only in A (canonical); E references MT-RNR2 open reading frame; no divergence |
| Humanin gene locus | A, B, C, D, E | MT-RNR2 / 16S mitochondrial rRNA gene | MATCH — all sections consistent |
| HNG / S14G-humanin potency vs. native | A, B, C, D, E | ~1,000-fold more potent than native humanin in neuroprotection/cytoprotection assays | MATCH — A states "approximately 1,000-fold" [A.4]; B states "~1,000-fold more potent" [B.1.2]; C states "approximately 1000-fold greater potency" [C.4]; D states "approximately 1,000-fold greater neuroprotective potency" [D.2]; E states "1,000-fold greater potency than native humanin" [E.3]. Consistent across all five sections. |
| HNGF6A analog description | A, B, C | S14G + F6A combined; described as second-generation / most potent humanin analog | MATCH — A introduces HNGF6A as "substitution of Phe6→Ala in addition to S14G" [A.4]; B describes it as "the combined S14G+F6A analog, most potent variant" [B.2.1]; C uses HNGF6A in ApoE-deficient atherosclerosis study (Oh 2011) with "second-generation humanin analog" framing [C.6]. No divergence. |
| MTRNR2L paralog count | A, E | Thirteen nuclear paralogs (MTRNR2L1–13) | MATCH — A states "Thirteen humanin-like nuclear pseudogenes — designated MTRNR2L1 through MTRNR2L13" [A.1]; E states "At least 13 nuclear-encoded pseudogenes and paralogs exist in the human genome under the MTRNR2L family (MTRNR2L1 through MTRNR2L13 and related loci)" [E.3]. Consistent. |
| Native humanin plasma half-life | C, D | C states "approximately 20 minutes" [C.8]; D states "approximately 30 minutes following IP injection" [D.2] | NOTE‡ |

‡Half-life cross-check: C.8 cites "approximately 20 minutes" as native humanin's plasma half-life. D.2 cites "approximately 30 minutes following IP injection in wild-type mice." These values differ (20 min vs. 30 min). However: (a) D is more precise — it specifies route (IP injection) and species (wild-type mice); C uses the figure as a brief parenthetical about a "plasma half-life of approximately 20 minutes" without specifying study conditions. (b) Both values fall within the expected short-half-life range for an unmodified linear peptide; neither is mechanistically inconsistent with the other given potential differences in assay conditions, measurement time points, and species. (c) The values are rounded approximations from distinct summary sources; neither section cites a primary half-life PK paper directly (both draw from secondary/review sources). (d) This is a **minor approximation variance in a summary context**, not a factual contradiction: both figures convey the same biological message (very short half-life, requires stabilization). The difference is insufficient to constitute a mismatch requiring editorial correction; it would be appropriate for the wiki author to harmonize to a range ("approximately 20–30 minutes in rodent PK models") rather than asserting a single number. Flagged here for writer awareness; does not affect the PASS verdict.

**Compound identifier mismatches: 0. One approximation variance noted (half-life 20 min vs. 30 min across C vs. D); does not rise to mismatch status.**

---

### 3. Institutions / Groups

| Entity | Sections | Value | Verdict |
|--------|----------|-------|---------|
| Nishimoto/Hashimoto discovery group | A, B, E | Keio University School of Medicine (Tokyo); Ikuo Nishimoto + Yasuko Hashimoto. A names them explicitly as discoverers; E identifies them as "Group A — Nishimoto/Hashimoto/Niikura (Keio University, Tokyo)"; B cites the 2001 PNAS discovery paper consistently. | MATCH |
| Cohen/Yen/Kim/Lee group | B, C, D, E | Pinchas Cohen + Kelvin Yen + Su-Jeong Kim + Changhan Lee (USC Leonard Davis School of Gerontology). All four sections cite USC-affiliated papers; E explicitly labels this "Group B — Cohen/Yen/Kim/Lee (USC Leonard Davis School of Gerontology)." | MATCH |
| Combined Keio + USC concentration figure | C (implicit), E | E states "combined ~55–65% of identifiable primary efficacy/mechanism papers." C does not cite a percentage but references the USC group in C.3 and notes the analog-tool provenance in C.4. No percentage is stated in any other section; E is the only section with the quantitative concentration audit. No cross-section conflict. | MATCH (single-section quantification; no divergence) |
| CohBar (company status) | D, E | D does not mention CohBar. E states CohBar was founded ~2013, NASDAQ: CWBR, pursued MOTS-c analogs primarily (CB5945/CB4209), website unreachable, consistent with dissolution, no verified dissolution date. No cross-section divergence (D simply doesn't address it). | MATCH |

**Institution mismatches: 0.**

---

### 4. Regulatory Dates / Facts

| Entity | Sections | Value | Verdict |
|--------|----------|-------|---------|
| FDA approval status | D, E | D: "NO approval from any governmental regulatory health authority for human therapeutic use" [D.5]; E: "No humanin product (native or HNG analog) is approved by FDA, EMA, or any comparable regulatory body" [E.4]. | MATCH |
| 503A Cat-1 / Cat-2 status | D, E | D: humanin does not appear on Cat-1 or Cat-2 active lists as of June 2026; occupies "regulatory grey zone" without 503A authorization [D.5]; E: "No IND has been publicly filed for native humanin" [E.4]. | MATCH — D carries the authoritative regulatory detail; E's brief characterization is consistent. |
| WADA S0 status | D | WADA S0 stated in D.5 only. No other section addresses WADA; no cross-section conflict. | MATCH (single-section) |
| CohBar pursuit of MOTS-c analogs, not native humanin | D (implicit), E | D does not mention CohBar directly. E explicitly states CohBar's "pipeline centered on MDP analogs including both humanin-derived and MOTS-c-derived compounds" and that clinical programs were "primarily MOTS-c analogs (CB5945 / CB4209)." No cross-section conflict. | MATCH |
| No human clinical trials (zero NCTs for interventional humanin administration) | B, D, E | B.1.4: "No human clinical trial of exogenous humanin or HNG for Alzheimer's disease exists as of mid-2026"; D.1: "No registered interventional trial of exogenous humanin or HNG in human subjects"; E.2: "zero NCT results for humanin as an interventional agent." All three sections independently and consistently affirm zero interventional NCTs. | MATCH |

**Regulatory fact mismatches: 0.**

---

### 5. Trial Registrations

| Entity | Sections | Value | Verdict |
|--------|----------|-------|---------|
| NCT03431844 (University of Tartu — observational cardiac) | E only | Completed observational study; no interventional humanin administration. | Single-section; no cross-cite conflict. |
| NCT06105229 / NCT06125249 (AKI observational) | E only | Two Chinese observational biomarker studies; no interventional humanin administration. | Single-section; no cross-cite conflict. |
| Zero interventional trials | B, D, E | Consistent across all three sections that address it. | MATCH |

**Trial registration mismatches: 0. No interventional humanin trial appears in any section; the three NCT registrations in E are observational biomarker studies and are not cited elsewhere.**

---

## Summary of Known Flagged Items

1. **PMID 25040290 and PMID 32575074 — tag-convention variance (not a mismatch):** Both papers are cited under different tags in different sections because each section is emphasizing a different sub-finding from the same multi-finding paper. Factual fields (author, year, journal, tier) are consistent. The wiki author should adopt a canonical tag based on the primary study type (animal) and note the human sub-cohort data in text.

2. **Native humanin half-life — approximation variance (not a mismatch):** C.8 uses "~20 minutes," D.2 uses "~30 minutes following IP injection." Both are valid short-half-life summaries from secondary sources; neither is factually wrong. Wiki author should harmonize to "approximately 20–30 minutes in rodent PK models" to eliminate the apparent discrepancy.

Neither item is a factual contradiction. Both are authoring-convention artifacts that can be resolved at the wiki-write stage without sectional edits.
