# ID-Reconcile Source — Phase-4.25 (Genetics/PGx corpus)

Scope: shared entities appearing in 2+ of section-A/B/C/D. Identifier reconciliation only — no content-quality judgment. String identity for IDs/rsIDs/PMIDs/DOIs/star-alleles; normalized-name identity for institutions.

## Summary

| Class | Shared entities scanned (in 2+ sections) | Mismatch count |
|-------|------------------------------------------|----------------|
| citations | 2 (Tandy-Connor 2018; 23andMe BRCA FDA authorization 2018) | 1 (formatting/type-tag only — see M1) |
| institutions | 8 (ACMG, CPIC, ClinGen, PharmGKB/PharmVar, FDA, gnomAD, NCCN, NSGC) | 0 |
| compound_identifiers (gene/allele/rsID) | 12 (CYP2D6, CYP2C19, CYP2C9, APOE/APOE-ε4, BRCA1, BRCA2, HLA-B*15:02, HLA-B*57:01, MTHFR, rs6025/F5, LDLR/APOB/PCSK9, CALM1–3) | 0 |
| regulatory_dates | 4 (ACMG/AMP 2015; 23andMe BRCA authorization 2018; GINA 2008; ACMG SF v3.2 2023) | 0 |
| trial_registrations | 0 (no NCT/registry IDs in corpus) | 0 |

Shared entities scanned total: 26. Substantive mismatches: 0. Formatting/metadata-only divergences flagged: 1 (M1).

## Mismatches

### M1 — Tandy-Connor 2018 type-tag divergence (formatting/metadata, NOT identifier)

- **entity_id:** Tandy-Connor S, et al. 2018, Genet Med 20(12):1515–1521, PMID 29565420, DOI 10.1038/gim.2018.38
- **sections:** A (ref [7]) and D (ref [13])
- **divergent values:**
  - All true identifier fields AGREE across sections: first author (Tandy-Connor S), year (2018), journal/volume/issue/pages (Genet Med 2018;20(12):1515–1521), PMID (29565420), DOI (10.1038/gim.2018.38) are byte-identical.
  - The ONLY divergence is the evidence **type-tag**: A tags it `[open_label]`; D tags it `[cohort]`.
- **suggested canonical:** Not an identifier-class mismatch. The type-tag is an evidence-classification field, not part of the citation identity, and is outside the ID-reconcile mandate (which checks PMID/DOI/author/year string identity). The PMID and DOI match exactly, so the two refs point at the same paper. **Recommend NO HALT on this** — flagged for the downstream content/judge gate, not for ID-reconcile. (For the record, the study is a retrospective clinical-laboratory case series of 49 confirmation samples; "open_label" vs "cohort" is a content-tagging disagreement, not an identifier conflict.)
- **justification:** Per the Phase-4.25 mandate, identifier reconciliation uses string identity on IDs/rsIDs/PMIDs/DOIs. Those all match. The type-tag is not in the enumerated identifier set (citations class checks "same PMID/DOI, same first author, same year"). Recording it as formatting-only so the verdict reflects ID integrity, not content-tag divergence.

### Notes on the other shared citation (no mismatch)

- **23andMe BRCA FDA authorization (2018):** appears as A ref [10] (FDA press announcement, March 6 2018) and D ref [3] (FDA De Novo DEN170046, 2018). These are two DISTINCT source documents describing the SAME regulatory action — a press release vs the De Novo decision summary — not the same citation rendered two ways, so there is no identifier to reconcile between them. The action date (2018) and the variant scope (three variants) agree. D names the three founder variants (185delAG + 5382insC in BRCA1; 6174delT in BRCA2); A describes them as "two in BRCA1, one in BRCA2" without naming — consistent, not conflicting. No mismatch.

### Institution-name normalization (all consistent — no mismatch)

- **ACMG:** A expands to "American College of Medical Genetics and Genomics" (with AMP, "Association for Molecular Pathology"); C and D use "American College of Medical Genetics and Genomics (ACMG)" / "ACMG". The expansion is identical wherever given; no "American College of Medical Genetics" (dropped "and Genomics") divergence. Consistent.
- **CPIC:** "Clinical Pharmacogenetics Implementation Consortium (CPIC)" in B and C; "CPIC" shorthand in D. Identical expansion. Consistent. (Note: B ref [10] renders the org name as "Clinical Pharmacogenomics Implementation Consortium" inside a single journal-title string — that is the cited article's own title text, not the section's institution naming, which is uniformly "Pharmacogenetics." Not a section-level mismatch.)
- **PharmGKB / PharmVar / ClinGen / FDA / gnomAD / NCCN / NSGC:** each canonical name used consistently where it appears in 2+ sections (PharmGKB in B; gnomAD/Genome Aggregation Database in A; FDA across A/B/D; ClinGen in A/B). No divergence.

### Compound identifier (gene/allele/rsID) cross-checks (all consistent — no mismatch)

- **HLA star-allele formatting:** C uses colon-delimited two-field form throughout — HLA-B*57:01, HLA-B*15:02, HLA-A*31:01, HLA-B*58:01. A uses "HLA-B*57:01" (same form). No legacy unspaced form (e.g., HLA-B*1502) appears in the prose, so no HLA-B*15:02-vs-HLA-B*1502 formatting split across sections. (Within-C: refs [1] and [12] in C's own bibliography render "HLA-B*5701"/"HLA-B*5801" in cited article titles — that is the journals' legacy title text, not C's prose nomenclature, and not a cross-section field.) Consistent.
- **CYP2D6 / CYP2C19 / CYP2C9:** B and C/D all use bare gene symbols and *N star-alleles (CYP2D6*4, *10, *5; CYP2C19*2/*3/*17; CYP2C9*2/*3) identically. No CYP2D6*4 vs CYP2D6*4xN type divergence across sections. Consistent.
- **APOE:** A uses "APOE"; C uses "APOE" with ε2/ε3/ε4; D uses "APOE-ε4". Same gene, same allele nomenclature (Greek ε). Consistent — "APOE-ε4" (D) and "ε4" (C) denote the same allele.
- **BRCA1 / BRCA2:** A and D both use "BRCA1"/"BRCA2" identically; both reference the same three 23andMe founder variants. Consistent.
- **rsIDs appearing in 2+ sections:** rs6025 (F5/Factor V Leiden) — only D. rs1801133 (MTHFR C677T) — only C. rs671 (ALDH2) — only C. rs4988235, rs9939609, rs762551, rs4149056, rs12777823, rs1799963 — each appears in a single section only. No rsID appears in 2+ sections, so no cross-section rsID string-identity check applies (and therefore no rsID typo split to record).
- **MTHFR:** rs1801133 / rs1801131 only in C. APOE, BRCA1/2 are the only gene symbols shared across sections, and they agree.

## Verdict

All shared identifiers (PMIDs, DOIs, first-author/year tuples, institution canonical names, gene symbols, star-alleles, rsIDs, regulatory dates) match by string/normalized-name identity across every section in which they co-occur. The single flagged divergence (M1) is an evidence-type-tag disagreement on a citation whose PMID and DOI are byte-identical across sections — outside the identifier set this gate reconciles, recorded as formatting/metadata only, not an identifier conflict.

```
verdict: PASS
```
