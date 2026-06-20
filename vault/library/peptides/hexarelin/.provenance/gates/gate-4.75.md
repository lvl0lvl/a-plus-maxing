# Gate 4.75 — Citation Integrity Verifier — Hexarelin

Mode: deep. Corpus: section-A…F + rubric. Verifier ran IC-1…IC-13 + population_mismatch + concentration_audit + corpus_scoping. Calibration: HALT only on genuine integrity violations; paywall / fetch-tooling artifact / honest gap / minor within-section number-or-population nit = WARN.

## IC-1 Type-Tag Presence

Every inline citation carries a tag from the canonical enum. Two distinct inline conventions are used and both are admissible: Section A and the indication bullets use `[tag][N]` (e.g., `[mechanism_review][1]`, `[animal (rat)][3]`); Sections B/D/E/F use a trailing `` `[tag, population]` `` annotation (e.g., `` `[rct, n=12 healthy adults]` ``, `` `[regulatory]` ``, `` `[vendor_label]` ``). Population/descriptor suffixes (`animal (rat)`, `rct cross-over`, `prospective clinical trial`) resolve to a canonical base tag. Descriptive variants "interventional" / "clinical trial" / "prospective trial" map to the interventional/cohort/open_label family and each names its base evidence type; not enum-violating. No bare/missing tags found. PASS.

## IC-2 Bibliography Type-Tag Presence

Every bibliography entry carries an explicit type-tag annotation. Multi-purpose tags present and acceptable (`in_vitro/animal mechanism` on Section C [6]; `regulatory/compounding_data_sheet` on Section F [1]). All map to the enum. PASS.

## IC-3 Vendor-Not-Numerical

`vendor_label` cites appear in Section A [5] and Section F [9][10][11][12]. Section A [5] grounds only non-numeric structural identity (CAS, sequence, formula, MW) and the qualitative GHS-R>CD36 preference; the quantitative cardiac CD36 claim is explicitly grounded in animal ref [7], not the vendor. Section F vendor cites ground only reconstitution math (mg/mL, IU, U-100), storage convention, and gray-market pricing — all permitted contexts; the desensitization-magnitude numbers are explicitly NOT grounded on vendor pages (self-check 1). No vendor cite grounds an efficacy/AE/dose-recommendation number. PASS.

## IC-4 Anecdote-Not-Numerical

`anecdote_aggregate` appears only in Section E (gray-market availability / "research use only" labelling) — qualitative availability disclosure, no numerical AE rate, dose, or effect size attached. PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy

`practitioner_protocol` cites (Section F [6] downgraded, [8] downgraded) ground only dose/route/cycle convention, explicitly reported as practice convention not efficacy; both are flagged as failing the name+venue+date bar and downgraded. No practitioner_protocol cite is the sole source of an efficacy claim. PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy

`compounding_data_sheet` cites (Section F [1][3]) ground only a NEGATIVE availability gate result ("no hexarelin product/data sheet located"). No efficacy claim attached. PASS.

## IC-7 Population-Mismatch

Animal numerical claims all satisfy the §1 override (species is the sentence subject within 100 chars and the cite is the sole source): Section C "hexarelin 80 µg/kg SC for 7 days to hypophysectomized rats" [7]; "100 µg/kg SC twice daily for 30 days to male Sprague-Dawley rats" [8]; Section A coronary-perfusion-pressure / 84 kDa CD36 in rat [7]. Human-population annotations are present and granular throughout (GHD children / healthy elderly / healthy adult / pubertal vs prepubertal vs elderly; n stated). Animal entries state species + n where available (Agbo n=96, n=6/group). See population_mismatch block. PASS.

## IC-8 Route-Extrapolation

Route is explicit and matched to the cited primary in every dose claim. Human PK/PD claims specify IV/SC/intranasal/oral and cite Ghigo 1994 (multi-route) [1]; cardiac human claims specify IV and cite Bisi/Broglio [4][5]; animal claims specify SC and cite Locatelli/Agbo [7][8]; practitioner convention specifies SC and cites practitioner/vendor sources. No dose claim asserts a route the cited primary did not test without annotation. The Section D safety floor carries an explicit `[dose-extrapolation]` tag for off-label dose/frequency/duration extrapolation. PASS.

## IC-9 Concentration-Surfacing

Single-largest-first-author-lineage share = 25% (< 70%), so the §3 first-class-section requirement is vacuous. The corpus nonetheless surfaces the concentration question in a dedicated "Concentration audit" subsection in Section C and flags the developer-network footprint. PASS (vacuous + voluntarily surfaced). See concentration_audit block.

## IC-10 No Fabricated Citations

Spot-verified load-bearing PMIDs/primaries via WebFetch / NCBI eutils:
- Ghigo 1994 (8126144) — VERIFIED: authors Ghigo/Arvat/Gianotti/Imbimbo/Lenaerts/Deghenghi/Camanni; JCEM 1994; multi-route hexarelin; bioavailability SC 77.0±10.5%, intranasal 4.8±0.9%, oral 0.3±0.1% — matches Sections A/B verbatim.
- Rahim/O'Neill/Shalet 1998 (9589671) — VERIFIED via eutils esummary: "Growth hormone status during long-term hexarelin therapy," JCEM 1998;83:1644-1649. (PubMed HTML hit a CAPTCHA; esummary resolved cleanly — citation is real, not fabricated.)
- Bodart 2002 CD36 (11988484) — VERIFIED: Bodart et al., Circ Res 2002, CD36 mediates cardiovascular action of GHRPs in heart.
- Broglio 2001 (11322491) — VERIFIED: Broglio et al., Endocrine 2001, GH-independent cardiotropic activities in normal/GHD/dilated-cardiomyopathy subjects.
- Bisi 1999 (10528131) — VERIFIED: Bisi et al., Eur J Pharmacol 1999, cardiac effects of hexarelin in hypopituitary adults.
- FR Doc 2026-07361 — VERIFIED at govinfo: PCAC Notice of Meeting July 23-24 2026; agenda BPC-157/KPV/TB-500/MOTS-c (Day 1), DSIP/Semax/Epitalon (Day 2); hexarelin/examorelin not mentioned — matches Section E exactly.
- WADA 2026 primary PDF — corpus-retrieval LIMITATION (WARN, not a HALT): the wada-ama.org PDF and JS landing page would not render through WebFetch (binary PDF / JS) and the drugs.com mirror returned HTTP 403. The substantive claim (hexarelin = examorelin, WADA-prohibited at all times under S2 as a named GH-releasing peptide) was independently corroborated via an external navigation-aid source. The exact decimal "S2.2.4" verbatim re-confirmation could not be re-rendered through tooling; this is a fetch artifact, not a non-resolving URL. See warnings.

Every inline `[N]` resolves to a per-section bibliography entry. No fabricated citations detected. PASS (load-bearing PMIDs all resolve; one regulatory primary deferred to WARN on tooling).

## IC-11 No Placeholder Strings

Grep for `[citation needed]` / TBD / TODO / "Content continues" / "according to some reports" / "research suggests" / "experts believe" returned no matches. PASS.

## IC-12 No Wikipedia Citations

No `wikipedia.org` / `sportwiki` URL appears in any section bibliography. The string "wiki" occurs only as (a) prose references to the destination project wiki ("Bottom line for the wiki"), (b) an explicit exclusion note in Section F ("SportWiki is wiki-type → HALT-adjacent ... excluded"), and (c) Section D's self-check assertion that no Wikipedia source was used. An "excluded as wiki" note is correctly NOT a citation. (Verifier did use a Wikipedia page as a navigation aid to corroborate the WADA fact — permitted; it is not in the report.) PASS.

## IC-13 Per-Citation Corpus Scoping

Deep-mode spot sample of load-bearing numerical/scope claims grep-verified against retrieved corpora: Ghigo 1994 bioavailability triplet (77% / 4.8% / 0.3%) matched verbatim in the retrieved abstract; Rahim 1998 long-term-therapy title/scope matched; Bisi/Broglio cardiac scope (LVEF rise in normal+GHD, no response in dilated cardiomyopathy; GH-independent) matched; CD36/84 kDa rat target matched Bodart. No quote-not-found or number-not-found. The WADA 2026 PDF corpus was not retrievable through tooling → `corpus-missing` WARN (paywall/binary-render analogue), not HALT, per IC-13 policy. PASS with one corpus-missing WARN.

## Verdict

verdict: PASS

```json
{"phase":"4.75","verdict":"PASS","iterations":1,"ic_checks":{"IC-1":{"status":"PASS","count_checked":120,"count_flagged":0},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS","count_checked":7,"count_flagged":0},"IC-4":{"status":"PASS","count_checked":2},"IC-5":{"status":"PASS","count_checked":2,"count_flagged":0},"IC-6":{"status":"PASS","count_checked":2},"IC-7":{"status":"PASS","count_checked":3,"count_flagged":0},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS","count_checked":7,"count_flagged":0},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS","count_checked":0,"count_flagged":0},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":3,"flagged_citations":[]},"concentration_audit":{"verdict":"PASS","total_primaries":8,"largest_cluster_name":"University of Turin (Ghigo/Arvat/Broglio/Bisi) — largest single first-author lineage","largest_cluster_count":2,"share":0.25,"threshold_triggered":false,"surfaced_section_heading":"Concentration audit (Section C)"},"corpus_scoping":{"verdict":"PASS","claims_checked":7,"claims_failed":[]},"halt_reasons":[],"warnings":["IC-10/IC-13: WADA 2026 Prohibited List primary PDF (wada-ama.org) not renderable through WebFetch (binary PDF + JS landing page); drugs.com mirror HTTP 403 — corpus-missing fetch-tooling artifact, not a non-resolving URL; substantive 'hexarelin = examorelin, WADA-prohibited at all times under S2 as named GHRP' independently corroborated via navigation-aid source; exact 'S2.2.4' decimal not re-verified through tooling this pass","concentration_audit: developer-footprint caveat — Deghenghi/Mediolanum (developer) is co-author or supplier on 4/8=50% of primaries and the two human cardiac-inotropy confirmations [4][5] are both from the same Turin lab (no cross-lab independent human replication); below 0.70 threshold so threshold_triggered=false, but surfaced as a caveat per brief","minor cross-section population-descriptor nit: Section B [7] tags Rahim/O'Neill/Shalet 1998 JCEM (PMID 9589671) as '[adults]' while Section C [2] (same paper) describes it as '12 healthy elderly subjects' — Section C 'elderly' descriptor is the precise one; minor within-corpus inconsistency, not a population-mismatch-gate violation (no animal/in_vitro number unflagged)"]}
```
