# Gate 4.25 — ID-Reconcile Report
## Semax Deep Research — Cross-Section Shared-Entity Consistency

**Run date:** 2026-06-22
**Iteration:** 1
**Sections scanned:** A, B, C, D, E
**Shared PMIDs pre-checked (design-TAG):** 18 — 0 mismatches (pre-confirmed)

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
      "scanned": 18,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 5,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 4,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 4,
      "mismatch_count": 0,
      "mismatches": []
    },
    "trial_registrations": {
      "scanned": 0,
      "mismatch_count": 0,
      "mismatches": []
    }
  },
  "halt_reasons": []
}
```

---

## Per-Class Detail

### Citations — 18 shared PMIDs scanned; 9 genuine divergences found and fixed inline

All divergences were resolved by editing the section files. Counts in the JSON above reflect post-fix state (mismatch_count = 0).

| PMID | Canonical (eutils) | Diverging section(s) | Field wrong | Fix applied |
|---|---|---|---|---|
| 35456550 | Pharmaceutics 2022;14(4):716; DOI …/pharmaceutics14040716 | Section E | Article number 795, DOI suffix 795 | Fixed → 716 / …716 |
| 32580520 | Genes (Basel) 2020;11(6):681; DOI …/genes11060681 | Section C | Issue 7, article 808 | Fixed → issue 6, article 681 |
| 32580520 | Genes (Basel) 2020;11(6):681; DOI …/genes11060681 | Section E | Article 684, DOI suffix 684 | Fixed → article 681, DOI …681 |
| 39442746 | Eur J Pharmacol 2024;984:177068 | Section A | Volume 985 | Fixed → 984 |
| 39442746 | Eur J Pharmacol 2024;984:177068 | Section C | Volume 985, article 177086 | Fixed → vol 984, article 177068 |
| 39442746 | Eur J Pharmacol 2024;984:177068 | Section D | Volume 985, article 177096 | Fixed → vol 984, article 177068 |
| 41479572 | Acta Naturae 2025;17(4):110–120 | Section D | 17(1):65–77 | Fixed → 17(4):110–120 |
| 36083821 | Vopr Kurortol… 2022;99(4 Vyp. 2):72–77 | Section B | 99(4):5–12 | Fixed → 99(4 Vyp. 2):72–77 |
| 36083821 | Vopr Kurortol… 2022;99(4 Vyp. 2):72–77 | Section D | 99(2):32–39 | Fixed → 99(4 Vyp. 2):72–77 |
| 11517472 | Zh Nevrol… 1997;97(6):26–34 | Section B | 26–28 | Fixed → 26–34 |
| 15678666 | Vestn Oftalmol 2004;120(6):25–27 | Section B | 120(6):39–42 | Fixed → 120(6):25–27 |
| 15678666 | Vestn Oftalmol 2004;120(6):25–27 | Section D | 120(5):36–40 | Fixed → 120(6):25–27 |

**PMIDs with no divergence across sections (consistent at all sites):**
29798983 (Gusev 2018), 16635254 (Dolotov 2006a J Neurochem), 16996037 (Dolotov 2006b Brain Res), 19633950 (Dmitrieva 2010), 11517472 author/year/journal (pages fixed above), 15792140 (Gusev 2005).

---

### Institutions — 5 entity instances scanned; 0 mismatches

| Entity | Sections | Consistent? |
|---|---|---|
| IMG-RAS (Institute of Molecular Genetics, Russian Academy of Sciences) | A, B, C, E | Yes |
| Zakusov Research Institute of Pharmacology | C, E | Yes |
| Peptogen (IMG-RAS spinout) | C, E | Yes |
| Pirogov Russian National Research Medical University | C, D, E | Yes |
| NRC Kurchatov Institute (successor to Zakusov) | C, E | Yes |

---

### Compound Identifiers — 4 entity instances scanned; 0 mismatches

| Claim | Sections checked | Consistent? |
|---|---|---|
| Semax sequence = Met-Glu-His-Phe-Pro-Gly-Pro (MEHFPGP) | A, B, C, D, E | Yes |
| Parent Semax = H-MEHFPGP-OH (free N-term, free C-term) | A, B | Yes |
| N-Acetyl-Semax-Amidate = Ac-MEHFPGP-NH₂ (modified, distinct entity) | A, B, D, E | Yes |
| Non-corticotropic / no steroidogenic activity | A, B, C, D | Yes |

---

### Regulatory Dates — 4 entity instances scanned; 0 mismatches

All facts below are author-reported via Deigin et al. 2022 (PMID 35456550) and flagged as such in sections D and E, not sourced to primary registry documents.

| Claim | Sections | Consistent? |
|---|---|---|
| Russia-registered: 0.1% and 1% intranasal forms | A, D, E | Yes |
| ЖНВЛП (Vital and Essential Drugs) listing | A, D, E | Yes (all note it; D correctly flags the year as not independently verifiable; E cites December 2011 decree as author-reported) |
| NOT FDA/EMA approved | B, D, E | Yes |
| WADA S0 reasoned-inference (not a named ban; requires ADO/WADA adjudication) | D | Single section; consistent with E's framing of NASA as unapproved |

---

### Concentration Figures — Two figures, different denominators, NOT contradictory

| Section | Figure | Denominator stated? | Denominator scope |
|---|---|---|---|
| C (§C.5.1 and §C.7) | ~90–95% IMG-RAS/Zakusov-lineage | Yes — "mechanistic (BDNF-induction, neuroprotection transcriptomics, cognitive preclinical) literature" | Full preclinical mechanism corpus (16 studies reviewed) |
| E (§E.1 self-check) | ~78–89% (7/9 IMG-RAS; 8/9 with Zakusov) | Yes — "9 verifiable English-language peer-reviewed publications enumerated" | The 9-study English-language table in §E.1 specifically |

These are different denominators applied honestly to different corpus slices. Section C's ~90–95% figure covers all preclinical mechanism work (a broader set including Russian-language and non-enumerated papers); Section E's 78–89% covers only the 9 enumerated English-language studies listed in §E.1's table. Neither denominator is ambiguous; no clarifying edit required.

---

### Trial Registrations — 0 scanned

No clinical trial registration numbers appear in any section. The absence is correctly noted across sections (all studies predate or lack ClinicalTrials.gov registration).

---

## Summary of edits made to section files

- **section-A.md:** 1 edit — PMID 39442746 volume corrected (985 → 984)
- **section-B.md:** 3 edits — PMID 11517472 pages (26–28 → 26–34); PMID 36083821 issue/pages (99(4):5–12 → 99(4 Vyp. 2):72–77); PMID 15678666 pages (120(6):39–42 → 120(6):25–27)
- **section-C.md:** 2 edits — PMID 32580520 issue/article (11(7):808 → 11(6):681); PMID 39442746 volume/article (985:177086 → 984:177068)
- **section-D.md:** 3 edits — PMID 39442746 volume/article (985:177096 → 984:177068); PMID 41479572 vol/issue/pages (17(1):65–77 → 17(4):110–120); PMID 36083821 issue/pages (99(2):32–39 → 99(4 Vyp. 2):72–77); PMID 15678666 issue/pages (120(5):36–40 → 120(6):25–27)
- **section-E.md:** 2 edits — PMID 35456550 article/DOI (795/…795 → 716/…716); PMID 32580520 article/DOI (684/…684 → 681/…681)

All mismatches resolved inline. No residual divergence. Verdict: PASS.
