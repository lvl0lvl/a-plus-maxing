## Verdict

verdict: PASS

All cross-section entity mismatches identified below are tier-rating divergences (the same paper receiving different tier integers in different sections) or a tag-label divergence for one citation — none affect author lists, year, journal, volume, issue, pages, or DOI. The factual metadata for all 11 shared PMIDs is byte-identical across sections that cite them. No compound-identifier, institutional-name, or regulatory-docket factual divergence was found. The gate passes with documented tier-annotation notes for downstream wiki canonicalization.

```json
{
  "phase": "4.25",
  "verdict": "PASS",
  "iterations": 1,
  "entity_classes": {
    "citations": {
      "scanned": 12,
      "mismatch_count": 0,
      "mismatches": []
    },
    "institutions": {
      "scanned": 3,
      "mismatch_count": 0,
      "mismatches": []
    },
    "compound_identifiers": {
      "scanned": 4,
      "mismatch_count": 0,
      "mismatches": []
    },
    "regulatory_dates": {
      "scanned": 5,
      "mismatch_count": 0,
      "mismatches": []
    },
    "trial_registrations": {
      "scanned": 1,
      "mismatch_count": 0,
      "mismatches": []
    }
  },
  "halt_reasons": []
}
```

---

## Per-class prose tables

### 1. Citations (PMIDs) — 12 scanned, 0 metadata mismatches

The 11 shared PMIDs listed in scope were scanned across all sections that cite them. Factual metadata (authors, year, journal, vol/issue, pages, DOI) is consistent. Tier annotations and, in two cases, the evidence-type tag differ between sections — these are section-local interpretive classifications, not factual metadata divergences. They are documented below as notes for wiki synthesis (not halt-class mismatches per the gate definition, which targets author/year/journal/vol/issue/pages).

| PMID | Sections citing | Authors (verified identical) | Year | Journal | Metadata consistent? | Tier divergence (note only) | Tag divergence (note only) |
|------|-----------------|------------------------------|------|---------|---------------------|---------------------------|--------------------------|
| 12374906 | A, C | Khavinson VKh | 2002 | Neuro Endocrinol Lett | YES | A=tier 2; C=tier 3 | None |
| 12937682 | A, B, D | Khavinson VKh, Bondarev IE, Butyugov AA | 2003 | Bull Exp Biol Med | YES | All tier 3 | None |
| 14501183 | B, E | Anisimov VN et al. (9 authors) | 2003 | Biogerontology | YES | All tier 2 | None |
| 14523363 | A, B, C, D, E | Khavinson VKh, Morozov VG | 2003 | Neuro Endocrinol Lett | YES | A=tier 2; B/C/D/E=tier 3 | A/B/D/E=open_label; C=cohort |
| 14647006 | A, E | Khavinson VKh et al. (7 authors) | 2003 | Neuro Endocrinol Lett | YES | A=tier 3; E=tier 2 | None |
| 17969590 | A, C | Korkushko OV et al. (8 authors) | 2007 | Adv Gerontol | YES | All tier 3 | None |
| 22451889 | B, D | Korkushko OV, Khavinson VKh, Shatilo VB, Antonyk-Sheglova IA | 2011 | Bull Exp Biol Med | YES | All tier 3 | B=rct; D=open_label |
| 32019204 | A, E | Khavinson V et al. (8 authors) | 2020 | Molecules | YES | A=tier 3; E=tier 2 | None |
| 35413689 | A, C | Yue X et al. (11 authors) | 2022 | Aging (Albany NY) | YES | All tier 2 | None |
| 40141333 | C, D, E | Araj SK et al. (4 authors) | 2025 | Int J Mol Sci | YES | All tier 2 | None |
| 40493162 | C, E | Gatta M et al. (11 authors) | 2025 | Stem Cell Rev Rep | YES | All tier 2 | None |
| 40908429 | A, B, C, D, E | Al-Dulaimi S, Thomas R, Matta S, Roberts T | 2025 | Biogerontology | YES | A/B/D/E=tier 2; C=tier 1 | None |

**Tier-annotation notes (for wiki synthesis, not halt-class):**

- **PMID 12374906** (Khavinson 2002 review, Neuro Endocrinol Lett): A assigns tier 2; C assigns tier 3 with note "Khavinson-authored; Khavinson-edited journal." C's rationale is the stronger argument; suggested canonical: tier 3.
- **PMID 14523363** (Khavinson & Morozov 2003): A assigns tier 2; B/C/D/E assign tier 3. B/C/D/E reasoning (Khavinson-institute authored, non-randomized design, Russian-translated venue) is the stronger argument; suggested canonical: tier 3. C also assigns tag "cohort" while A/B/D/E use "open_label"; B explicitly notes PubMed lists it as RCT but corrects to open_label; suggested canonical tag: open_label (B's explicit rationale).
- **PMID 14647006** (Khavinson et al. 2003 chromatin paper, Neuro Endocrinol Lett): A assigns tier 3; E assigns tier 2. A's rationale (Khavinson-led, Russian journal, no independent replication) favors tier 3; suggested canonical: tier 3.
- **PMID 22451889** (Korkushko et al. 2011, Bull Exp Biol Med): B tags as "rct" (mirroring PubMed pub-type, with explicit caveats); D tags as "open_label." B's self-check notes the tag is the PubMed-indexed claim; D's "open_label" reflects the editorial judgment that the randomization claim is unaudited. For wiki synthesis, "rct" with an explicit caveat note (per B's handling) is the more defensible canonical choice, as it preserves the primary source's claimed design while flagging the audit limitation.
- **PMID 32019204** (Khavinson et al. 2020, Molecules): A assigns tier 3; E assigns tier 2. A flags MDPI open-access concern and Khavinson lead authorship, favoring tier 3; suggested canonical: tier 3.
- **PMID 40908429** (Al-Dulaimi et al. 2025, Biogerontology): A/B/D/E=tier 2; C=tier 1. The Biogerontology journal is a solid specialty venue but not a top-tier journal; sections assigning tier 2 are the majority and the more conservative assignment. Suggested canonical: tier 2.

---

### 2. Compound identifiers — 4 scanned, 0 mismatches

| Entity | Fact | Consistent across sections? | Note |
|--------|------|-----------------------------|------|
| Epitalon sequence | Ala-Glu-Asp-Gly (AEDG) | YES — A, C, D all use identical sequence | |
| Molecular weight | ~390 Da / ~390.35 Da | YES — A uses "~390.35 Da"; D uses "~390 Da" (rounded); no divergence in scientific meaning | |
| Epithalamin vs. Epitalon distinction | Crude bovine pineal extract vs. synthetic AEDG tetrapeptide | YES — maintained consistently across A, B, C, D, E | |
| CAS numbers | 307297-39-8 (free peptide), 307297-40-1 (acetate) | Section A only (identity section); not duplicated in other sections; no conflict | |

---

### 3. Institutions / groups / concentration — 3 scanned, 0 mismatches

| Entity | Fact | Sections | Consistent? |
|--------|------|----------|-------------|
| Khavinson's institute name | "St. Petersburg Institute of Bioregulation and Gerontology" | A, B, C, D, E | YES — exact name identical across all sections |
| Anisimov affiliation | N.N. Petrov Research Institute of Oncology / N.N. Petrov National Medical Research Center of Oncology | B (long form), C (abbreviated mention), E (full name) | YES — same institution, slightly different name forms (both accurate); no factual conflict |
| ≥80% concentration figure | "estimated ≥80%" of primary papers from Khavinson/direct collaborators | B (implied), C (states "vast majority"), E (states "≥80%" with enumerated derivation) | YES — the quantified figure is in E (the section dedicated to concentration audit); B/C use qualitative language consistent with E's finding; no divergence |

---

### 4. Regulatory dates / facts — 5 scanned, 0 cross-section mismatches

| Entity | Fact | Sections | Consistent? | Note |
|--------|------|----------|-------------|------|
| FDA Cat-2 removal date | April 15, 2026 (effective) / April 16, 2026 (Federal Register publication) | D (para: "April 15"; bib [11]: "April 15"; bib [12]: "April 16"), E (para: "April 15"; bib [16]: "April 16") | YES — the April 15/16 split is the difference between the effective date and the FR publication date; both sections handle this the same way | |
| Federal Register citation | 91 Fed. Reg. 20465, Docket FDA-2025-N-6895 | D [12], E [16] | YES — identical | |
| PCAC date | D bullet: "July 24, 2026"; D para: "July 23–24, 2026"; D bib [12]: "July 23–24, 2026"; E para: "July 24, 2026"; E bib [16]: "July 23–24, 2026" | D, E | EFFECTIVELY CONSISTENT — the two-day meeting is July 23–24; some prose references cite only July 24 (the second day or the epitalon-specific agenda item per Boesen Snow Law source). The bib entries in both D and E correctly state "July 23–24, 2026" citing the Federal Register. The prose abbreviation to "July 24" is a simplification within both sections but not a cross-section divergence (both D and E do it). | |
| WADA S0 | Epitalon not individually named; captured by S0 Non-Approved Substances clause | D only (E does not separately address WADA) | YES — no conflict | |
| Russian MoH authorization | Epithalamin only (not synthetic Epitalon AEDG) | D, E | YES — both sections correctly scope the Russian registration to Epithalamin; both note synthetic Epitalon has no equivalent separate registration | |

---

### 5. Trial registrations — 1 scanned, 0 mismatches

| Entity | Fact | Sections | Consistent? |
|--------|------|----------|-------------|
| FDA-2025-N-6895 (regulatory docket) | Docket for 503A Category 2 removal + PCAC review | D [12], E [16] | YES — docket number, title, and scope are identical across both bibliography entries |

No human trial registrations (ClinicalTrials.gov NCT numbers) exist for Epitalon in any section; all sections that address this explicitly note the absence. The FDA docket is the only registration-class entity present.

---

## Summary

All 12 shared-PMID bibliography entries have byte-identical factual metadata (authors, year, journal, vol/issue, pages, DOI) across every section citing them. The six tier-annotation divergences and one tag divergence (open_label vs. cohort for PMID 14523363; rct vs. open_label for PMID 22451889) are section-local interpretive classifications that do not constitute factual mismatches under the gate definition — they are noted with suggested canonicals for wiki synthesis. Compound identity, institutional names, concentration figure, and regulatory docket facts are consistent across all sections.
