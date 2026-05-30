# Phase 4.25 ID-RECONCILE — cross-section identity reconciliation

INV-RESEARCH-CROSS-SECTION-ID. Deep-mode run `supplements-landscape`, sections A–E.
Scan date 2026-05-29. Scope: SHARED ENTITIES appearing in 2+ section drafts only
(citations, compound/molecule identifiers, regulatory-event dates, numerical values,
trial registrations). Identity check only — NOT content-quality judgement. Identity
rule: string-identity for IDs/dates/registrations; normalized-form-identity for
compound names and dose/percent/n values.

Method note: a value appearing in only ONE section is OUT OF SCOPE (no cross-section
identity to reconcile) and is listed under "single-section (not scanned for mismatch)"
where it could be mistaken for shared. The post-fix grep-audit logs at the foot of each
section (OLD→NEW provenance tables) are NOT live claims and were excluded from value
extraction — only live finding bodies + bibliographies were compared.

---

## Class 1 — Citations (papers / sources cited in 2+ sections)

| Entity (citation) | Sections | Value-in-each (ref# / ID) | Mismatch? | Canonical |
|---|---|---|---|---|
| VITAL trial (Manson 2019, vitamin D3 + omega-3 primary-prevention RCT) | A (ref 12), D (named "VITAL, etc." in D1, no ref#) | A: "VITAL, n=25,871, 2000 IU/d D3, 1 g/d omega-3", NEJM, Manson JE 2019. D: "RCTs powered on hard outcomes (VITAL, etc.)" — named, no n / no ID restated | N | A's full citation (Manson JE 2019, NEJM 10.1056/NEJMoa1809944, n=25,871). D references the same trial without restating any divergent number — consistent. |
| FDA "DMHA and Phenibut" enforcement action page | B (ref 17, via Cohen PMC6583602 + the FDA notice), C (ref 6) | B: "FDA Acts on Dietary Supplements Containing DMHA and Phenibut". C: "FDA Acts on Dietary Supplements Containing DMHA and Phenibut". | N | Identical FDA page title in both. (Numbers drawn from it differ in REFERENT — see Class 4 DMHA row — not a citation-ID mismatch.) |
| FDA "FDA and Kratom" page / Import Alert 54-15 | B (ref 22), C (ref 9) | B: "FDA and Kratom (fda.gov/news-events/public-health-focus/fda-and-kratom)". C: "FDA and Kratom; Import Alert 54-15; US Marshals seize kratom supplements". | N | Same FDA source family; C adds Import Alert 54-15 + seizure (more detail), no contradicting identifier. |
| Cochrane Cerebrolysin review (Ziganshina) | E only (ref 3) | E: CD007026.pub7, PMID 37818733 | N/A | Single-section — not shared. |
| Tucker JAMA 2018 (PMC6324457) | B only (ref 16; B5 + B7 prose both inside section B) | B: PMC6324457 | N/A | Single-section (both uses are intra-B). |
| Chandrasekhar 2012 ashwagandha (PMID 23439798) | D only (ref 9) | D: PMID 23439798 / PMC3573577 | N/A | Single-section. |
| NMN metabolic meta-analysis (PMC11557618) | A only (ref 4) | A: PMC11557618 | N/A | Single-section. |
| NMN FDA NDIN correspondence (NDIN 1247/1259) | D only (ref 13) | D: NDIN 1247 SyncoZymes / 1259 Kingdomway | N/A | Single-section (see Class 3 note — C does NOT carry NMN). |

No citation cited in 2+ sections carries divergent identifiers (PMID/DOI/PMC/page-title). **0 mismatches, Class 1.**

---

## Class 2 — Compound / molecule identifiers (brand vs INN vs research-code)

| Entity | Sections | Value-in-each | Mismatch? | Canonical |
|---|---|---|---|---|
| NMN | A (A2: "NMN", "nicotinamide mononucleotide"), D (D3: "NMN", "β-nicotinamide mononucleotide"), E (n/a) | A: "NMN" / "nicotinamide mononucleotide". D: "NMN" / "β-nicotinamide mononucleotide (NMN)". | N | Normalized: β-NMN = NMN = nicotinamide mononucleotide (β-anomer is the only biologically relevant form; "β-" is a stereochemical prefix, not a different molecule). Both sections gloss the abbreviation to the full INN. Consistent. |
| KSM-66 (ashwagandha branded extract) | A (A3), D (D3) | A: "KSM-66 ... produced exclusively by Ixoreal Biomed (standardized ≥5% withanolides)". D: "KSM-66 root, ~5% withanolides". | N | KSM-66 / Ixoreal / ~5% withanolides. "≥5%" (A) and "~5%" (D) are the same standardization figure. |
| Sensoril (ashwagandha branded extract) | A (A3), D (D3) | A: "Sensoril is a Natreon-originated brand (≥10% withanolides)". D: "Sensoril dosing convention ... ~125–250 mg, reflecting higher withanolide concentration". | N | Sensoril / Natreon / ≥10% withanolides. D's "higher withanolide concentration than KSM-66" is qualitatively consistent with A's ≥10% > ≥5%. No numeric conflict (D gives no Sensoril %). |
| Ashwagandha / Withania somnifera (generic, distinct from branded extracts above) | A (A3), B (B3), D (D3), E (E3) | A/D: branded-extract context (≥5–10% withanolides). B: DILI agent "ashwagandha". E: generic root-extract trials "standardized around <0.9% withanolides". | N | Two DISTINCT entities correctly kept distinct: branded high-concentration extracts (KSM-66 ~5% / Sensoril ~10%) vs generic root-extract trials (~<0.9%). E's <0.9% is the generic-root referent, NOT the same object as the branded %. No section asserts the branded % of the generic, or vice-versa. Consistent. |
| Green tea extract / EGCG | B only (B3) | B: "green tea extract (EGCG)" | N/A | Single-section. |
| Curcumin (native / micellar / γ-cyclodextrin) | A only (A4) | A: native vs micellar vs curcumin-γ-cyclodextrin | N/A | Single-section. |
| Resveratrol | A only (A2) | A: resveratrol / SIRT1 | N/A | Single-section. |
| Creatine monohydrate | A (A1/A5), D (D2) | A: "creatine monohydrate" (lean-mass/strength + cognition). D: "creatine monohydrate" (loading-phase convention). | N | Same molecule, same name. Different outcomes discussed; identifier identical. |
| Kratom (Mitragyna speciosa / mitragynine) | B (B6), C (C3) | B: "kratom (mitragynine / 7-OH-mitragynine)". C: "kratom (Mitragyna speciosa)". | N | Same compound; B names the alkaloids, C names the species binomial. Complementary, not divergent. |
| Phenibut | B (B6), C (C5 ref via FDA DMHA/phenibut) | B: "phenibut" GABA-B agonist. C: "phenibut" (named in FDA action title). | N | Same identifier. |

**0 mismatches, Class 2.**

---

## Class 3 — Regulatory-event dates (MUST agree across sections)

| Event | Sections | Date-in-each | Mismatch? | Canonical |
|---|---|---|---|---|
| Ephedra final rule (adulterated) | C only (C3) | C: published 2004-02-11, effective 2004-04-12 | N/A | Single-section. |
| BMPEA warning letters | C only (C3) | C: 2015-04-23 (five companies) | N/A | Single-section. |
| Acacia rigidula warning letters | C only (C3) | C: 2016-03-15 (six companies) | N/A | Single-section. |
| 4-androstenedione FDA scientific memo | C only (C3) | C: 2022-03-01 | N/A | Single-section. |
| Kava FDA consumer advisory | B only (B3) | B: "2002 FDA advisory"; German 2002 ban (court-lifted 2014) | N/A | Single-section (C does not carry kava — verified by grep, 0 hits). |
| NMN NDIN timeline (Nov-2022 exclusion / Sep-29-2025 reversal / Dec-2-2025 confirmation) | D only (D3) | D: NOV 2022 / SEP 29 2025 / DEC 2 2025; 2026 status = lawful NDI | N/A | Single-section. **C3's enforcement-ingredient list does NOT include NMN** (verified: 0 NMN hits in section-C). So the NMN regulatory dates are NOT a cross-section shared entity in this corpus. |

No regulatory date appears in 2+ sections, so none can disagree. **0 mismatches, Class 3.** (Coverage note, not a mismatch: the regulatory-date load is concentrated in C, with kava-2002 isolated in B and the NMN arc isolated in D — no overlap to reconcile.)

---

## Class 4 — Numerical values appearing in 2+ sections (dose / % / n)

| Value | Sections | Value-in-each | Mismatch? | Canonical |
|---|---|---|---|---|
| Vitamin D UL = 4,000 IU/day | B (B1), D (D1) | B: "vitamin D UL is 100 mcg (4,000 IU)/day" [NIH-ODS, ref 2]. D: "the IOM place [UL] at 4,000 IU/day" [IOM 2011, ref 1]. | N | 4,000 IU/day adult UL. B attributes to NIH-ODS, D to IOM 2011 — same underlying IOM-derived figure, identical value. (D additionally cites the Endocrine Society 10,000 IU/day upper limit, which B does not mention — additive coverage, not a conflict, since it is a different body's figure explicitly labelled as such.) |
| Supplement contamination prevalence ≈ 9–15% | B5 (via ref 22/PMC13021601), B7 (ref 24) | B5: "~9–15% contamination". B7: "~9–15% ... contaminated". | N | Both intra-section B, same range, same underlying PMC13021601. Consistent. (Not a true cross-SECTION pair — both in B — but identical.) |
| "12" (DMHA context) | B5, C3 | B5: "12 supplements purchased in 2017" (product/sample count). C3: "12 DMHA warning letters" (warning-letter count). | N | NOT the same quantity — different referents (sampled products vs FDA warning letters) that share the integer 12 coincidentally. No identity to reconcile; flagged here only because the bare number could be mistaken for a shared value. |
| Withanolide standardization % | A3, D3, E3 | A: KSM-66 ≥5%, Sensoril ≥10%. D: KSM-66 ~5%. E: generic root ~<0.9%. | N | Branded KSM-66 ~5% (A≈D). Sensoril ≥10% (A only). Generic root <0.9% (E only) — different entity (see Class 2). No two sections give a DIFFERENT % for the SAME object. |
| VITAL n = 25,871; D3 dose 2000 IU/d | A (A5) | A only states n / dose; D names VITAL without restating either | N | No competing number in D → nothing to disagree with. |

No numerical value is asserted with two DIFFERENT magnitudes for the same referent in 2+ sections. **0 mismatches, Class 4.**

---

## Class 5 — Trial registrations (NCT / EudraCT / ChiCTR)

| Registration | Sections | Value | Mismatch? | Canonical |
|---|---|---|---|---|
| NCT07176325 (creatine GI/fluid loading-vs-no-load trial) | D only (D2, ref 6) | D: NCT07176325 (registration, no results) | N/A | Single-section. |

No trial registration appears in 2+ sections. **0 mismatches, Class 5.**

---

## Whole-corpus tally

- **Shared entities scanned (present in 2+ sections):** 12
  - Class 1 citations: 3 (VITAL; FDA DMHA/Phenibut page; FDA Kratom page/IA 54-15)
  - Class 2 compound identifiers: 6 (NMN; KSM-66; Sensoril; ashwagandha/Withania generic-vs-branded; creatine monohydrate; kratom; phenibut — counting the ashwagandha-family entities as the load-bearing set; NMN counted once)
  - Class 3 regulatory dates: 0 cross-section
  - Class 4 numerical values: 3 (vitamin D UL 4,000 IU; the coincidental "12"; withanolide %)
  - Class 5 trial registrations: 0 cross-section
- **Single-section entities catalogued (out of scope, not scanned for mismatch):** Cochrane Cerebrolysin, Tucker JAMA, Chandrasekhar, NMN-metabolic-meta, NMN NDIN dates, ephedra/BMPEA/Acacia/androstenedione dates, kava-2002, EGCG, curcumin forms, resveratrol, NCT07176325.
- **Mismatch count by class:** Class 1 = 0; Class 2 = 0; Class 3 = 0; Class 4 = 0; Class 5 = 0.
- **Total mismatches:** 0.

Key reconciliations that COULD have been mismatches but agree on inspection:
1. Vitamin D 4,000 IU UL (B via NIH-ODS, D via IOM 2011) — same figure, different attributing body; D's added Endocrine Society 10,000 IU is a distinct labelled figure, not a contradiction.
2. KSM-66 withanolide % — "≥5%" (A) vs "~5%" (D) normalize to the same standardization.
3. Ashwagandha withanolide % across A/D (branded ~5–10%) vs E (generic <0.9%) — correctly kept as two distinct entities; no section cross-asserts.
4. The bare integer "12" (B sample-count vs C warning-letter-count) — coincidental, different referents.
5. NMN naming (NMN / β-NMN / nicotinamide mononucleotide) normalizes to one molecule across A and D.

---

## Verdict

verdict: PASS
