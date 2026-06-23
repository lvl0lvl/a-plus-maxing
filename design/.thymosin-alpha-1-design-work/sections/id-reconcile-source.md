## Verdict

verdict: PASS

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "iterations": 2,
  "entity_classes": {
    "citations": {
      "scanned": 34,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 8,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 12,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 10,
      "mismatch_count": 0,
      "mismatches": []
    },
    "trial_registrations": {
      "scanned": 8,
      "mismatch_count": 0,
      "mismatches": []
    }
  },
  "halt_reasons": []
}
```

---

## Per-Class Prose Tables

### 1. Citations (scanned: 34 shared-entity appearances; mismatch_count: 0)

| PMID | Sections | Tag | Tier | Consistency |
|------|----------|-----|------|-------------|
| 10607256 (Mutchnick 1999) | B [2], E [7] | rct | 2 | MATCH — author list, journal, DOI, tag, tier identical |
| 23327199 (ETASS 2013) | B [7], C [6], D [4], E [9] | rct | 1 | MATCH — full author string, Critical Care, PMID, tag, tier identical across all 4 sections |
| 27633969 (Liu 2016 BMC) | C [8], D [5] | meta_analysis | 1 | MATCH — author list, journal, DOI, tag, tier identical |
| 39814420 (TESTS 2025) | B [8], C [7], E [10] | rct | 1 | MATCH — full author string, BMJ DOI, tag, tier identical |
| 22178096 (Carraro 2012) | B [6], C [4] | open_label | 2 | MATCH — both tag open_label tier 2; Iter-1 fix confirmed |
| 11381492 (Ancell 2001) | C (self-check + inline), D [3] + D line 140 | mechanism_review | 2 | MATCH — PMID, journal, DOI, tag, tier consistent |

**ETASS p-value:** B states p=0.062 unadjusted / p=0.049 log-rank; D states P=0.049 log-rank — correctly scoped to the log-rank analysis, consistent.

**TESTS n-count:** B says n=1,089 mITT; C and E say 1,106 (total enrolled). Both are factually correct for their respective population labels — B explicitly tags "mITT," C/E refer to total enrolled. Not a mismatch; properly scoped.

---

### 2. Institutions / Concentration (scanned: 8 named research groups; mismatch_count: 0)

| Group | Sections | Funding disclosure | Consistency |
|-------|----------|-------------------|-------------|
| Goldstein / GWU | A, E | NCI/NIH academic | MATCH |
| Garaci / Tor Vergata Rome | A, C, E | Italian foundations / ERC | MATCH |
| Wu / Sun Yat-sen (ETASS) | B, C, D, E | Guangdong academic/government only (no SciClone) | MATCH — Iter-1 fix confirmed; B now states Guangdong Natural Science Foundation + Guangdong Medical Scientific Research Foundation; no SciClone attribution; E explicitly separates ETASS from TESTS |
| Wu / Sun Yat-sen (TESTS) | B, C, E | SciClone co-funded | MATCH |

---

### 3. Compound Identifiers (scanned: 12 instances; mismatch_count: 0)

| Entity | Sections | Value | Consistency |
|--------|----------|-------|-------------|
| Peptide length | A, D, E | 28 amino acids | MATCH |
| N-terminal modification | A, D | N-terminal acetyl on serine | MATCH |
| MW | A | ~3108 Da | Stated only in A; consistent with ZADAXIN standard reference cited |
| INN | A, D | thymalfasin | MATCH |
| Brand | A, B, C, D, E | Zadaxin (SciClone Pharmaceuticals) | MATCH |
| Route | B, C, D | Subcutaneous (SC) injection only | MATCH |
| Standard dose | B, C, D | 1.6 mg SC | MATCH |
| Reconstitution | D | 1 mL sterile water -> 1.6 mg/mL | Only in D; no contradiction elsewhere |

---

### 4. Regulatory Dates / Facts (scanned: 10 instances; mismatch_count: 0)

| Fact | Sections | Value | Consistency |
|------|----------|-------|-------------|
| Country approval count | A, B, C, D, E | >35 countries / over 35 countries | MATCH — Iter-1 fix confirmed; B's former ~30 is gone; all sections use ">35" or "over 35" |
| FDA non-approval | B, C, D | Not FDA-approved for any indication | MATCH |
| FDA orphan designations | C, D | Melanoma + HCC (per Ancell 2001 PMID 11381492; hedged "not primary-fetchable") | MATCH — Iter-1 fix confirmed; both sections cite same indications and same PMID with same hedge |
| PCAC vote date | D | December 4, 2024 | Only in D; no contradiction elsewhere |
| 503A compounding status | D, E | Not legally compoundable under 503A as of current date | MATCH |
| WADA status — Ta1 | D | Not explicitly named on 2026 prohibited list | Only in D; E does not contradict |

---

### 5. Trial Registrations / Facts (scanned: 8 trial facts; mismatch_count: 0)

| Trial | Sections | Key facts | Consistency |
|-------|----------|-----------|-------------|
| Chien 1998 CHB RCT | B | n=~98; 26-week arm 40.6% response | Only in B; no contradiction |
| ETASS (PMID 23327199) | B, C, D, E | n=361; single-blind; 6 Chinese hospitals; Guangdong academic funding | MATCH across all 4 sections |
| TESTS (PMID 39814420) | B, C, E | mITT n=1,089 (B) / total 1,106 (C, E); double-blind; 22 centers; HR 0.99; p=0.93 | No mismatch — n-count difference is mITT vs total enrolled, explicitly labeled |
| Carraro 2012 (PMID 22178096) | B, C | open_label; tier 2; hemodialysis; H1N1 vaccine | MATCH — both tag open_label tier 2; Iter-1 fix confirmed |
| Gravenstein 1989 RCT | C | n=90 elderly men 65-99y; double-blind | Only in C; no contradiction |
| NCT06821100 | C | COVID-19 booster trial ongoing; adults >=60 | Only in C; no contradiction |

---

## Iter-1 Fix Verification

| Fix | Status |
|-----|--------|
| ETASS funding -> Guangdong academic/government (no SciClone) | CONFIRMED RESOLVED — B line 43 states Guangdong Natural Science Foundation + Guangdong Medical Scientific Research Foundation; no SciClone attribution; E section 7 independently separates ETASS (no commercial sponsor) from TESTS (SciClone co-funded) |
| Carraro 2012 -> open_label tier 2 in BOTH B and C | CONFIRMED RESOLVED — B [6] tag: open_label tier 2; C [4] tag: open_label tier 2 |
| Country count -> ">35 countries" everywhere | CONFIRMED RESOLVED — A ("more than 35"), B (">35"), C ("over 35"), D ("> 35"), E ("35+") — all consistent >=35 formulations |
| FDA orphan designations -> melanoma + HCC in BOTH C and D (PMID 11381492) | CONFIRMED RESOLVED — C line 39 names melanoma + HCC with PMID 11381492; D line 140 names melanoma + HCC with PMID 11381492; same hedge in both |

---

*Gate written 2026-06-20. Scan covers all 5 sections (A-E) across all 5 entity classes. No new mismatches detected. All 4 Iter-1 fixes verified resolved.*
