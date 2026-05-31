# Gate 4.75 — Citation Integrity Verifier (mode=standard)

Corpus: `sections/section-A.md` (photoaging/barrier topicals), `sections/section-B.md` (AGA + compounds), `sections/section-C.md` (conditions literacy + image/test validity).
Canonical type-tag enum: `rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`.
Verifier checks structural compliance only; it does not judge content quality.

## IC-1 Type-Tag Presence

Every inline `[N, tag]` (and the second cite in every `[N, tag; M, tag]` multi-cite) was extracted and its tag checked against the enum. Distinct inline tags used across the corpus: `cohort, in_vitro, mechanism_review, meta_analysis, open_label, practitioner_protocol, rct, regulatory` — all eight are enum members. Multi-tag inline form `[1, meta_analysis/regulatory]` (section-C L77): both tags enum-valid. No inline numeric cite carries an out-of-enum or missing tag.

One non-numeric inline citation ID was found: `[SA-mech, mechanism_review]` (section-A L68). The tag `mechanism_review` is enum-valid, so IC-1 (tag presence) is satisfied; the non-resolving identifier `SA-mech` is recorded under IC-10.

No type-tag presence violation detected.

## IC-2 Bibliography Type-Tag Presence

All 57 numbered bibliography entries (A: 18, B: 27, C: 12) carry a `[tag]` immediately before `(Retrieved: ...)`. Every tag is an enum member. Multi-tag entry section-C `[1] [meta_analysis / regulatory]` — both tags enum-valid (slash-joined multi-tag, acceptable). The grep for entries lacking a clean enum tag returned empty for all three files.

No bibliography type-tag violation detected.

## IC-3 Vendor-Not-Numerical

`grep -i vendor_label` returns only the type-tag legend line in section-C L4 (a definition, not a citation). There is no `vendor_label` cite anywhere in the corpus, so no `vendor_label` source grounds any numerical efficacy/AE/dose claim.

No vendor-not-numerical violation detected.

## IC-4 Anecdote-Not-Numerical

Two substantive `anecdote_aggregate` usages:
- section-C L148 (bibliography supporting list, *Actas Dermo-Sifiliográficas*): no numeric grounded. Clean.
- section-C L69: grounds dataset-composition figures — "ISIC training sets ~82% Fitzpatrick I–III; FST V/VI ~8%; as few as ~8 melanoma images for FST V." These ARE numeric, but they are dataset-composition descriptors, NOT an AE rate / dose / effect size (the prohibited class under IC-4). The cite is also explicitly bounded "off-whitelist arXiv/preprint corroboration only" and the boundary it supports does not turn on these numbers. Outside the IC-4 prohibited class; recorded as a WARNING for visibility, not a HALT.

No anecdote-grounded AE-rate/dose/effect-size claim detected (the one numeric is dataset-composition, out of prohibited class).

## IC-5 Practitioner-Protocol-Not-Efficacy

`practitioner_protocol` inline cites: section-C L15 (ROSCO [6], phenotype-based management approach + which agents are prescriber-managed — classification/management, no effect size); section-C L84 (AAAAI/EAACI IgG position — a "do not use" recommendation, no efficacy figure); section-B L104/L106 ([26] Delphi — indications/dosing/contraindications/monitoring = dose/route/cycle + risk-floor); section-B L105 ([27] — starting doses/titration/splitting = dose only). No `practitioner_protocol` cite grounds an efficacy effect-size claim; where efficacy is discussed nearby, it rests on `rct`/`meta_analysis` cites.

No practitioner-protocol-grounds-efficacy violation detected.

## IC-6 Compounding-Data-Sheet-With-Efficacy

One `compounding_data_sheet` usage: section-B L107 — `[20, rct; compounding convention is compounding_data_sheet]`. The compounding tag grounds only the formulation/availability fact ("compounded topical finasteride typically 0.1–0.25% solution/gel"); the co-located efficacy/PK ("RCT-validated P-3074 0.25% spray") is grounded by the underlying primary `[20, rct]` (Piraccini, PMID 34634163, resolved). Compounding tag does not stand alone behind an efficacy claim.

No compounding-data-sheet-grounds-efficacy-without-primary violation detected.

## IC-7 Population-Mismatch

Checked: 2 inline `in_vitro`/`animal`-class numeric cites + 1 rat-data claim.
- section-B L66 (rat embryofetal teratogenicity, `[9, regulatory]`): carries `[population-mismatch: rat]` in the same sentence. Claim is categorical (hypospadias, reduced anogenital distance), flagged anyway. Compliant.
- section-B L95 (GHK-Cu, `[25, in_vitro]`): numeric "picomolar–nanomolar concentrations" + cell/ex-vivo proliferation claims; carries `[population-mismatch: human ex-vivo follicle / cultured cells]` in the same sentence, and the species ("human ex-vivo / cultured cells") is the explicit subject within the clause. Compliant on both grounds.

No `animal` inline cite exists outside the rat-flagged regulatory line. The sole `in_vitro` numeric cite is flagged. Section-A self-check confirms no animal/in-vitro source grounds a number there (vitamin-C collagen and SA comedolysis are tagged mechanistic, non-numeric; Fisher MMP data are in-vivo human skin). Section-C distribution-mismatch (Esteva curated-vs-consumer, ISIC tone imbalance) is narratively flagged though not an animal/in-vitro species case.

Checked: 3 candidate claims. Misses: 0. No unflagged population-mismatch detected.

## IC-8 Route-Extrapolation

Route/concentration extrapolation flags present and correctly placed:
- section-B L29: `[route-extrapolation]` on antihypertensive-dose-oral-minoxidil pericardial-effusion warning vs LDOM, and oral-vs-topical minoxidil safety. Source route (oral antihypertensive, multi-mg–tens-of-mg) is stated; flagged.
- section-B L72: `[route-extrapolation]` on the 5 mg-prostate/older-men PCPT framing vs 1 mg AGA indication. Flagged.
- section-B L76: `[route-extrapolation]` on topical finasteride lowering-but-not-eliminating systemic DHT (topical vs oral route). Flagged.
- section-B L107: oral 1 mg-AGA vs 5 mg-prostate finasteride and compounded-topical 0.1–0.25% vs RCT P-3074 0.25% — route/concentration divergences stated in-line as "Divergence" with the underlying RCT (`[20, rct]`/`[13, rct]`) cited; concentration is matched to the trial's formulated %.

Section-A self-check states no efficacy number is extrapolated across route/concentration; all efficacy figures are reported at the formulated topical % the cited trial used (verified against the body — e.g., 8% glycolic/lactic A[14], 5% niacinamide A[11b], 5% ascorbic A[13] all match the cited-trial concentrations). No topical-vs-oral or in-vitro-conc-vs-formulated-% number is imported unflagged.

No route-extrapolation miss detected. No route-unverifiable cases.

## IC-9 Concentration-Surfacing

Distinct primaries across the whole corpus: 57 numbered bibliography entries (bibliographies are section-scoped; numbering resets per section, and no PMID/DOI spans two sections — see IC-10). Largest lab/group/industry-sponsor cluster of distinct primaries:
- Voorhees / U-Michigan dermatology group: 2 (A[1] Weiss, A[7] Fisher)
- Green / Nambour-cohort group (QIMR): 2 (A[8] Hughes, A[9] Green)
- Olsen EA: 2 (B[3] minoxidil RCT, B[12] dutasteride RCT)
- Procter & Gamble (industry sponsor): 1 (A[11b] Bissett niacinamide)

Largest cluster = 2 distinct primaries. Computed single-cluster share = 2 / 57 ≈ **3.5%** (tie among Voorhees, Green/Nambour, Olsen). This is far below the 70% threshold; no first-class dominance section is required. The only industry-sponsor concentration (P&G, niacinamide) is already surfaced in-corpus with an explicit single-sponsor dominance caveat and a certainty downgrade (section-A L56, A.4 table).

Computed concentration share: ~3.5% (largest cluster name: Voorhees-Michigan / Green-Nambour / Olsen, each 2 primaries). Below 70% — no buried-dominance violation.

## IC-10 No Fabricated Citations / Cross-Section ID Reconciliation

Inline-to-bibliography resolution: every numeric inline ID resolves to a defined bibliography entry in its own section — A body uses 1,2,4,5,6,7,8,9,10,11,11b,12,13,14,14b,15,16,16b (all defined); B body uses 1–27 (all defined); C body uses 1–12 (all defined). One non-numeric inline ID, `[SA-mech, mechanism_review]` (section-A L68), does NOT resolve to any bibliography entry — recorded as WARNING (see verdict). It grounds a non-numeric textbook mechanistic statement ("salicylic-acid comedolysis is concentration-dependent"); the numeric SA claim on the same line is grounded by the resolvable `[15, rct]` (Boutli, PMID 14708455). Not a load-bearing value, so not a HALT under standard-mode rules.

Cross-section reconciliation: no PMID or DOI appears in more than one section (verified by per-PMID file membership). Bibliographies are disjoint and section-scoped, so there is no shared-entity author/year/value to disagree on. No cross-section identifier disagreement possible or found.

Fabrication spot-check (15 of the most load-bearing identifiers fetched against NCBI eutils): PMIDs 3336176 (Weiss 1988), 8552187 (Fisher 1996), 23732711 (Hughes 2013), 10475183 (Green 1999), 9777765 (Kaufman 1998), 17110217 (Olsen 2006), 20605255 (Eun 2010), 11050579 (Price 2000), 30206635 (Lee 2019), 34634163 (Piraccini 2022), 39565602 (Akiska Delphi), 32041693 (Freeman 2020), 28117445 (Esteva 2017), 38300170 (Reynolds 2024), 18492135 (Bissett 2004) — all 15 resolve and match the bibliography on title + first author + year. Minor non-load-bearing nuance: B[26] Akiska Delphi is listed by NCBI as a 2025 epub vs "2024" in the doc — publication-date nuance, not a fabrication, not behind any numeric claim. Section-internal post-fix audits (A[15] Boutli, B[18] Lucia, B[12] Olsen identifier correction) are consistent with the resolved records.

No fabricated/unresolvable citation on a load-bearing value, and no cross-section identifier disagreement, detected.

## IC-11 No Placeholder Strings

`grep -inE 'citation needed|TBD|TODO|Content continues|according to some reports|research suggests|experts believe'` across all three files: exit 1, zero matches. The `## Post-fix grep audit` and `## Self-check` sections describe prior remediation and confirm placeholder-absence; these are provenance, not placeholders (per instructions, not flagged).

No placeholder string detected.

## IC-12 No Wikipedia Citations

`grep -i wikipedia` returns only three self-check assertion lines (section-A L137, section-B L172, section-C L157) stating Wikipedia is NOT cited. No `wikipedia.org` URL or citation appears in any bibliography.

No Wikipedia citation detected.

## IC-13 Per-Citation Corpus Scoping

`SKIP-mode` (standard mode). The Phase-3.5 paired judges already grep-verified load-bearing numerics against fetched records; per-citation corpus scoping is not re-run here.

SKIP-mode recorded.

## Population-Mismatch

3 candidate animal/in-vitro/species claims checked corpus-wide; all 3 carry an in-sentence flag (`[population-mismatch: rat]` B L66; `[population-mismatch: human ex-vivo follicle / cultured cells]` B L95, where species is also the explicit subject). No `animal`/`in_vitro` numeric claim is missing its mismatch flag. Misses: 0.

## Concentration-Audit

Distinct primaries (corpus): 57. Largest single lab/group/industry-sponsor cluster: 2 distinct primaries (three-way tie: Voorhees-Michigan A[1]+A[7]; Green-Nambour A[8]+A[9]; Olsen EA B[3]+B[12]). Share ≈ 3.5%, below the 70% dominance threshold. P&G is the only industry sponsor cluster (1 primary, A[11b]) and is already flagged with a certainty downgrade. No buried-dominance violation; no first-class dominance section required.

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings:
  - "IC-10: inline identifier [SA-mech] (section-A L68) does not resolve to a bibliography entry; tag is enum-valid and it grounds a non-numeric textbook mechanism claim (the co-located numeric is grounded by resolvable [15, rct]), so non-load-bearing -> WARNING not HALT"
  - "IC-4: anecdote_aggregate cite (section-C L69) grounds dataset-composition numerics (~82% FST I-III, ~8% FST V/VI, ~8 melanoma images FST V); these are corpus-composition descriptors, not an AE-rate/dose/effect-size (IC-4 prohibited class), and are marked off-whitelist corroboration -> WARNING not HALT"
  - "IC-10: B[26] Akiska LDOM Delphi shown as 2025 epub by NCBI vs '2024' in bibliography; publication-date nuance, not behind any numeric claim -> WARNING"
```
