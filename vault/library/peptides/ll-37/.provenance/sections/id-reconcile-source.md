# Phase 4.25 ID-Reconcile — LL-37 (iteration 2)

## Verdict

verdict: PASS

Iteration-1 found 1 citation mismatch: the Lande et al. *Sci Rep* 2020 SLE paper
("Native/citrullinated LL37-specific T-cells help autoantibody production in SLE") was
cited with a divergent article number (Section D = 5851 vs Section G = 5847) and a
mismatched/incomplete external-ID set (D = PMID 32245990 + DOI; G = PMCID-only). That
defect is now remediated and confirmed. A full re-scan of all 5 entity classes across
sections A–G (live content only; `## Post-fix grep audit` blocks excluded per instruction)
found NO remaining mismatch and NO new divergence.

---

## Per-class findings (scanned + mismatch_count per class)

### citations — scanned 14 shared papers across 2+ sections; mismatch_count = 0

Every paper appearing in ≥2 sections was re-checked for article/PMID/DOI concordance:

- Lande 2007 (pDC self-DNA, Nature 449:564) — B[8], D[1]: PMID 17873860, DOI
  10.1038/nature06116. MATCH.
- Lande 2014 (LL-37 T-cell autoantigen, Nat Commun 5:5621) — D[4], F[9]: PMID 25470744,
  DOI 10.1038/ncomms6621. MATCH.
- Lande 2020 (SLE T-cells, Sci Rep 2020;10) — D[7], G[15]: article 5851, PMID 32245990,
  DOI 10.1038/s41598-020-62480-3. **MATCH (remediated — see resolution section).**
- Grönberg 2014 (VLU FIH, WRR 22:613) — E[1], F[1], G[4]: PMID 25041740, DOI
  10.1111/wrr.12211. MATCH.
- Mahlapuu 2021 (HEAL Phase IIb, WRR 29:938) — E[2], F[2], G[5]: PMID 34687253, DOI
  10.1111/wrr.12977, PMCID PMC9298190. MATCH (G cites PMCID subset; no conflict).
- Miranda 2023 (DFU) — E[3], C(coverage mention): PMID 37480520, DOI
  10.1007/s00403-023-02657-8. MATCH.
- Armiento 2020 (IAPP, Angew Chem 59:12837) — B[13], D[11]: PMID 32220015, DOI
  10.1002/anie.202000148. MATCH.
- Engelberg & Landau 2020 (LL-37(17-29), Nat Commun 11:3894) — B[12], D[13]: PMID
  32753597, DOI 10.1038/s41467-020-17736-x. MATCH.
- Carretero 2008 (wound healing, JID 128:223) — B[6], G[2] (+C prov note): PMID 17805349,
  DOI 10.1038/sj.jid.5701043. MATCH.
- Simonetti 2021 (MRSA wound, Antibiotics 10:1210) — C[6], G[3]: PMID 34680791, PMCID
  PMC8532939, DOI 10.3390/antibiotics10101210. MATCH.
- Dolkar 2018 (melanoma derm toxicity, J Cutan Pathol 45:539) — E[6], F[5]: PMID 29665030,
  DOI 10.1111/cup.13262. MATCH (E[6]'s earlier "Williams" byline already corrected to
  Dolkar in live content).
- "Renovation as innovation" cancer review — E[5], F[4]: PMC9445486 (E adds PMID 36081952,
  DOI 10.3389/fphar.2022.944147). MATCH.
- Pahar B (first-author shared, but DISTINCT papers): A[8] = PMC9368159, NETosis, 2022 vs
  F[10] = Vaccines 2020;8(3):517, PMID 32927756, "Immunomodulatory Role." Two different
  works, each internally consistent. NOT a cross-section ID mismatch.
- Single-section papers (Coffelt 2009 B[10]; Ji 2019 B[11]; Barlow 2011 C[4]; etc.): no
  cross-section surface, no conflict.

### institutions — scanned 5 shared entities; mismatch_count = 0

Karolinska/Gudmundsson-Agerberth originators (A 1996 paper, G 1995 paper — distinct real
works, same group); Promore Pharma/Pergamum clinical sponsor (E,F,G — Pergamum = prior
corporate name, no contradiction); Lande/Gilliet lineage (B,D,F,G); Marche+Gdańsk
(Simonetti, C,G); MD Anderson (E,F). All attributed consistently.

### compound_identifiers — scanned 5; mismatch_count = 0

- 37-aa sequence LLGDFFRKSKEKIGKEFKRIVQRIKDFLRNLVPRTES — A(claim 4), G(§3): character-for-
  character identical. MATCH.
- MW ~4493 Da / 4.49 kDa — A(claim 6), C(prov note ≈4493 Da). MATCH.
- Net charge +6 — A(claim 5: +6, note +5.9 at pH 7.4), B(cationic), G. MATCH (the +5.9 is
  A's self-noted methodological variant, not a cross-section conflict).
- 37-residue length — consistent throughout (A,B,C,F,G).
- hCAP18 residue numbering — A "134–170" (numbers from full pre-pro-protein incl. 30-aa
  signal peptide) vs G "hCAP-18(104–140)" (numbers from mature protein after signal
  cleavage; offset ≈30). Both span exactly 37 residues; both are valid literature
  conventions. Soft note only, NOT scored as a mismatch (consistent with iteration-1).

### regulatory_dates — scanned 4; mismatch_count = 0

FDA 503A Cat-2 removal (FR Doc 2026-07361, published 2026-04-16; effective ~Apr 22–23,
2026) and the PCAC timeline (LL-37 NOT on the July 23–24, 2026 PCAC; deferred to "before
end of February 2027") live in Section F and are internally consistent. Section G's
regulatory statements ("no approved exogenous LL-37 product," "Phase IIb failed on full
population") are fully concordant. No divergent regulatory date across sections.

### trial_registrations — scanned 3; mismatch_count = 0

- NCT02225366 (melanoma, MD Anderson) — E[4], F[3]. MATCH.
- EudraCT 2018-000536-10 (HEAL Phase IIb) — E[2], F[2]; both note no NCT located. MATCH.
- NCT04098562 (Miranda DFU) — E[3] + E table (C references same trial by PMID 37480520).
  CONSISTENT.

---

## Resolution confirmation (the Lande 2020 item)

RESOLVED — verified across both live-content locations:

- section-D [7]: "*Sci Rep* 2020;**10:5851**. DOI: **10.1038/s41598-020-62480-3**. PMID:
  **32245990**."
- section-G [15]: "*Sci Rep* 2020;**10:5851**. DOI:**10.1038/s41598-020-62480-3**. PMID:
  **32245990**. PMCID:PMC7125190."

The two sections now carry an identical and mutually consistent identifier triple:
article **5851** / PMID **32245990** / DOI **10.1038/s41598-020-62480-3**. The remediation
fixed both prior defects from iteration-1: (a) G's wrong article number "5847" is corrected
to 5851, and (b) G now carries the full PMID + DOI rather than a PMCID-only reference. The
"5847" token survives ONLY inside section-G's `## Post-fix grep audit` block documenting the
OLD→NEW fix — which is excluded from live-content checks — and appears nowhere in any live
citation. Resolution confirmed; no regression introduced.

---

## Additional re-confirmations requested

- **MW 4493 / charge +6 / 37-aa:** CONFIRMED consistent (A↔C MW; A net charge +6; sequence
  character-identical A↔G).
- **FDA Cat-2 removal ~Apr 2026 + LL-37 deferred off the Jul-2026 PCAC:** CONFIRMED (Section
  F, internally consistent; concordant with G; no cross-section conflict).
- **Mahlapuu Phase IIb NEGATIVE on primary endpoint:** CONFIRMED concordant across E
  (closure 26.5/24.7/25.3%, ns), F ("well tolerated"; no positive primary claimed), and G
  ("failed its primary efficacy endpoint on the full population"). All three agree; only the
  post-hoc ≥10 cm² subgroup is positive, correctly flagged.
- **Dual-nature B↔D consistency:** CONFIRMED. Anti-amyloid IAPP/Aβ (Armiento B[13]/D[11];
  Bhattacharjya D[12]) and self-assembly-as-helical-fibrils-not-cross-α (Engelberg
  B[12]/D[13]) align; FPRL1/TLR4 pro-tumor framing in B (ovarian, lung) is a strict subset
  of D's and F's bidirectional cancer accounting — no section asserts the opposite direction
  for any tissue. Direction agrees everywhere.

---

## Structured verdict

```json
{"phase":"4.25","entity_classes":{"citations":{"scanned":14,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":5,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":5,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":4,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":3,"mismatch_count":0,"mismatches":[]}},"iterations":2,"halt_reasons":[]}
```

PASS condition met (all 5 entity classes mismatch_count = 0). The single iteration-1 defect
(Lande 2020 SLE citation) is resolved with no new divergence introduced.
