# Phase 4.25 ID-Reconcile — GHK-Cu (iteration 2)

## Verdict

verdict: PASS

Both prior cross-section issues are remediated and now consistent across all affected sections. A full re-scan of all 5 entity classes across sections A–G found zero remaining and zero new cross-section mismatches.

## Per-class findings (scanned + mismatch_count per class; table of any remaining mismatch)

| Entity class | Scanned (distinct cross-section entities) | Mismatch count | Notes |
|---|---|---|---|
| citations | 12 | 0 | Maquart 1988 (now 3169264 in B/C/G); Mulder 1994 (17147644 + RCT design in E/F/G); Maquart 1993 (8227353 in B/C); Siméon 2000, Campbell 2012, Hong 2010, OBM 2021, CIR 2018, Pickart 2012/2015/2018 — all PMID/DOI/design consistent where co-cited |
| institutions | 6 | 0 | Reims/Maquart group; Skin Biology (Pickart/Margolina/Vasquez-Soltero); ProCyte (Patt/Trachy/Duncan); Koch/Stanford; CIR panel; Hudson Biotech — described consistently across sections |
| compound_identifiers | 7 | 0 | MW 340.38, CID 73587, C14H24N6O4 (peptide), C14H22CuN6O4 (complex), CAS 49557-75-7 (peptide), CAS 89030-95-5 (complex); copper constants 16.44/16.2/8.68 (overall) vs 12.62 (pH-7.4 conditional) — explicitly NOT conflated; concentration split (CIR <10 ppm / vendor 0.05–2% / practitioner 1–3%) kept distinct |
| regulatory_dates | 5 | 0 | FDA 503A April 2026, PCAC Feb 2027, WADA 2026 Prohibited List, CIR 2018, Cu RDA/UL — localized in Section F (CIR also in G, consistent); internally consistent |
| trial_registrations | 1 | 0 | NCT07437586 (Hudson Biotech Phase 2) — single value, consistent across E's claim/table/bib |

No remaining-mismatch table is needed (all counts 0).

### Detail on the no-mismatch determinations

- **Citations.** Maquart 1988 FEBS paper: PMID **3169264** in B[4], C[1], G[7] — now unanimous (G corrected from 3049153). Mulder 1994: PMID **17147644** + "multicenter randomized evaluator-blinded vehicle-controlled RCT" in E[5], F[16]+Claim 9, G[13] — unanimous; closure figures 98.5%/60.8% and infection 7% vs 34% match across E/F/G. Maquart 1993 = 8227353 in B/C (off-by-one already fixed in C). All other co-cited papers (Siméon 2000, Campbell 2012, Hong 2010, OBM Genetics 2021, CIR 2018, the Pickart 2012/2015/2018 reviews) agree on PMID/DOI/PMC across the sections that carry them.
- **Compound identifiers.** CAS assignment is unambiguous wherever both numbers appear (A claims 1/4 + bib [6]/[7]; F line 5): 49557-75-7 = free peptide, 89030-95-5 = copper complex. F's substance line correctly labels which CAS is which, matching A. MW 340.38 and CID 73587 appear only in Section A — no cross-section disagreement possible; values correct. Copper-binding constants are explicitly distinguished as different quantities in both A (claim 6) and B (claim 1): 16.44/16.2/8.68 = Pickart-review overall stability constants; 12.62 = tier-1 pH-7.4 conditional (A only, explicitly firewalled). MW / copper-constant / CAS are not conflated anywhere.
- **Concentration split.** Three distinct, correctly-attributed concentration regimes — CIR regulatory `<10 ppm` (F + G, identical), vendor cosmetic-active formulation `~0.05–2%` (F, vendor TDS [7]) / `~0.05–1%` (G, supplier [4]) (different vendor sources, overlapping, both flagged vendor-only — not a contradiction), and practitioner topical-dosing convention `1–3% by weight` (G, practitioner_protocol [15]). Different entity types, kept separated, not conflated.
- **Institutions.** No institution is named two different ways across sections. Skin Biology (Bellevue WA), ProCyte (Patt/Trachy/Duncan), the Reims group, and the Pickart/Margolina/Vasquez-Soltero authorship triad are spelled and described consistently in every section that carries them.
- **Regulatory dates / trial registrations.** All date-bearing regulatory specifics (FDA 503A April 2026, PCAC Feb 2027, WADA 2026 Prohibited List) live solely in Section F; CIR 2018 appears in F and G with identical year/DOI/`<10 ppm`/cosmetic-only scope. The Category 1-vs-2 wording variance on F's [10]-source note is the already-disclosed secondary-tracker sequencing discrepancy flagged in F's own body, not a cross-section conflict. NCT07437586 appears only in Section E with one consistent phase/status/sponsor/n/start-date across its claim text, table, and bibliography.

## Resolution confirmation (the 2 prior items)

1. **Maquart 1988 FEBS PMID — RESOLVED.** PMID is now consistently **3169264** in B[4], C[1], and G[7]. Section G previously carried the wrong **3049153** (which resolves to an unrelated strictosidine-synthase paper); G's live bib [7] (line 62) now reads 3169264, and 3049153 survives only inside G's qualified OLD→NEW audit note (permitted, not live content). The prior 2-of-3 consensus (B, C) + DOI/vol agreement is now a unanimous 3-of-3.

2. **Mulder 1994 design — RESOLVED.** All of E, F, G now describe PMID **17147644** as a **multicenter, randomized, evaluator-blinded, vehicle-controlled RCT** (lamin Gel, diabetic neuropathic foot ulcers, 98.5% vs 60.8% closure, infection 7% vs 34%). Section F previously called it an open-label 0.03/0.3/3% dose-finding study; F Claim 9 was corrected and a new tier-1 bib entry [16] added, with the retired "open-label dose-finding / 0.03%, 0.3% and 3% / ~15 days" phrasings surviving only inside F's qualified audit note (permitted). No fabricated alternate PMID. F[16] explicitly notes consistency with Section E [5] and Section G [13].

## Structured verdict

```json
{"phase":"4.25","entity_classes":{"citations":{"scanned":12,"mismatch_count":0,"mismatches":[]},"institutions":{"scanned":6,"mismatch_count":0,"mismatches":[]},"compound_identifiers":{"scanned":7,"mismatch_count":0,"mismatches":[]},"regulatory_dates":{"scanned":5,"mismatch_count":0,"mismatches":[]},"trial_registrations":{"scanned":1,"mismatch_count":0,"mismatches":[]}},"iterations":2,"halt_reasons":[]}
```
