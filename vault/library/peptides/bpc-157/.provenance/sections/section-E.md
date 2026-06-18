# Section E: Pharmacokinetics, Dose, Route & Formulation

> **Integrity note.** A widely-circulated "~15 min half-life for BPC-157" is *real data* but is **rat IV (n=6)**, not human. No measured human PK parameter (half-life, Cmax, AUC, bioavailability) has been published. Every numeric PK value below is animal, tagged with species + n + route. No human PK number is asserted. Practitioner doses and the Phase 2 SC dose are handled separately and never used to infer exposure.

---

## E.1 How much real human PK exists: essentially none

There is **no published measured human pharmacokinetic profile** for BPC-157. The one human trial designed to produce one — a Phase 1 oral safety/PK study of "PCO-02"/Bepecin (sponsor PharmaCotherapia d.o.o.), NCT02637284 — listed Cmax, Tmax, AUC and T1/2 as *secondary outcome measures*, but **no results are posted** and the record's current registry overall status is **"UNKNOWN"** (no results posted), with estimated completion March 2016 [1, rct] (registered; no results posted). The trial used **oral tablets, 1 mg BPC-157 per tablet**, with single doses of 1, 3, or 6 tablets (Phase 1a) and 3 tablets every 8 h for 14 days (9 mg/day; Phase 1b), enrollment ~42 healthy volunteers [1, rct] (registered; no results posted). Because no PK results are public, **no human half-life, Cmax, AUC, or oral bioavailability value can be stated. → no admissible human PK source located.**

The active Phase 2 trial (NCT07437547, sponsor Hudson Biotech) is a clinical-efficacy trial, not a PK study, and **does not disclose its subcutaneous dose** (see E.4) [2, rct] (registered; no results posted).

**`human_pk_exists = false`** — see structured return.

---

## E.2 Measured animal PK (single primary source: rat + dog)

All quantitative absorption/half-life/distribution/clearance figures below come from one formal ADME study in rats and beagle dogs [3, animal]. BPC-157 is a 15-amino-acid peptide, MW 1419 Da [3, animal].

### Half-life (elimination t½) — **animal only**
- **Rat, IV, 20 µg/kg, n=6: 15.2 min** [3, animal] — *this is the figure mis-circulated as "BPC-157's half-life"; it is rat IV.*
- Rat, IM single dose, n=6/dose: range ~7.87–29.7 min across 20/100/500 µg/kg [3, animal]
- Rat, repeated IM 100 µg/kg ×7 d, n=6: 18.5 min [3, animal]
- **Beagle dog, IV, 6 µg/kg, n=6: 5.27 ± 2.25 min** [3, animal]
- Beagle dog, IM single dose, n=6/dose: ~20.0–29.3 min [3, animal]
- Authors' summary across both species/routes: **"less than 30 min"** [3, animal].

### Absolute bioavailability (IM vs IV) — **animal only**
- **Rat IM, n=6/dose: ~14.5%–19.4%** (18.82% at 20 µg/kg; 14.49% at 100 µg/kg; 19.35% at 500 µg/kg) [3, animal]
- **Beagle dog IM, n=6/dose: ~45%–51%** (45.27%±24.85% / 47.64%±18.09% / 50.56%±27.01% at 6/30/150 µg/kg) [3, animal]
- **No oral bioavailability was measured** in this study. → no admissible source for oral %F.

### Exposure parameters (rat, IM single dose, n=6/dose) [3, animal]
| Dose (IM) | Tmax | Cmax | AUC₀–t |
|---|---|---|---|
| 20 µg/kg | 3.00 min | 12.3 ng/ml | 75.1 ng·min/ml |
| 100 µg/kg | 3.00 min | 48.9 ng/ml | 289 ng·min/ml |
| 500 µg/kg | 3.00 min | 141 ng/ml | 1930 ng·min/ml |

Rat IV (20 µg/kg, n=6): AUC₀–∞ 400 ng·min/ml; Vss 36.4 ml/kg; CL 50.1 ml/min/kg; MRT 0.727 min [3, animal].
Dog IV (6 µg/kg, n=6): AUC₀–t 76.4±30.2 ng·min/ml; Vss 243±162 ml/kg; CL 90.8±40.1 ml/min/kg; MRT 2.49±0.822 min [3, animal].
PK was **linear** across the tested doses in both species [3, animal].

### Metabolism, distribution, excretion (rat, n=6) [3, animal]
- **Metabolism:** rapid peptidase degradation; intact BPC-157 was the main plasma component at ~3 min, then degraded to small peptide fragments and ultimately amino acids (M1 = proline; at 1 h, [³H]proline = 86.65% of plasma radioactivity) [3, animal].
- **Distribution:** highest in kidney; elevated in liver, stomach wall, spleen, thymus; lower than plasma in brain, myocardium, skeletal muscle, fat [3, animal].
- **Excretion:** main routes urine and bile (urine ~16–18%, bile ~9% in bile-duct-cannulated rats) [3, animal].

**Route-extrapolation flag:** these are rat/dog IV and **IM** parameters at **µg/kg** doses. They cannot be converted to human oral or human subcutaneous exposure. `[route-extrapolation]` — any inference from dog IM 45–51% %F to human SC, or from rat IV 15.2 min to human t½, is unsupported.

---

## E.3 Oral vs injectable stability (gastric-juice claim)

The claim that BPC-157 is **"stable / resistant to degradation in human gastric juice for more than 24 hours"** originates with the discovering group (Sikiric et al.) and is repeated in their reviews [4, mechanism_review]. The ADME paper similarly states BPC-157 "is resistant to hydrolysis, enzyme digestion, and even gastric juice" [3, animal]. **Caveat:** this is the originating lab's assertion / re-statement, not an independent re-measurement located here; treat the specific ">24 h" figure as an author-sourced claim, qualitatively supported but not independently replicated in the sources retrieved. BPC-157 was discovered by Sikiric and colleagues (University of Zagreb) as a fragment associated with gastric juice; it is given alone without a carrier [4, mechanism_review]. No quantitative human oral stability/degradation kinetics were located. → quantitative oral-stability PK: no admissible source.

---

## E.4 Dose / route table

Doses are segregated by evidentiary basis. **Human-trial doses are cited; practitioner doses carry no exposure claim; animal doses are species + route tagged. Cross-route inferences are flagged, not made.**

### (a) Human-trial doses — cited
| Trial | Route | Dose | n | Status / results |
|---|---|---|---|---|
| NCT02637284 (PharmaCotherapia, Ph1) [1] | **Oral** | 1 mg/tablet; single 1/3/6 mg; repeated 3 mg ×3/day (9 mg/day) ×14 d | ~42 | Registry overall status **"UNKNOWN"**; **no PK results posted** |
| NCT07437547 (Hudson Biotech, Ph2) [2] | **Subcutaneous** | **Dose NOT disclosed** (once daily ×14 d) | ~120 | Recruiting (start Feb 2026) |

### (b) Practitioner-convention doses — `[practitioner_protocol]`, NOT exposure-grounded
- Commonly cited community/clinic conventions are typically ~250–500 µg/day SC or oral, often "per injury site." **These are practitioner_protocol conventions only — no PK/efficacy basis and no admissible primary source; they are NOT derived from the trials above and must not be presented as established dosing.** Listed here solely to mark the convention space. *(No specific numeric practitioner figure is asserted as fact; flagged practitioner_protocol.)*

### (c) Animal doses — species + route tagged [3, animal]
| Species | Route | Doses tested | n |
|---|---|---|---|
| Rat | IV | 20 µg/kg | 6 |
| Rat | IM | 20 / 100 / 500 µg/kg (single); 100 µg/kg ×7 d | 6/group |
| Beagle dog | IV | 6 µg/kg | 6 |
| Beagle dog | IM | 6 / 30 / 150 µg/kg (single); 30 µg/kg ×7 d | 6/group |

The ADME authors note an interspecies **body-surface-area conversion** (e.g., ~200 µg/person/day ↔ 20 µg/kg rat / 6 µg/kg dog) [3, animal]. **`[route-extrapolation]` / `[species-extrapolation]` flag:** this allometric conversion is the authors' scaling, is IM-anchored, and does **not** establish a human oral or human SC dose. Animal IP doses commonly seen in efficacy literature (µg/kg, intraperitoneal) are likewise **not** human SC doses and are not used here.

### Reconstitution math (vendor_label — purity/dilution only)
Permitted purely as arithmetic: e.g., a 10 mg vial reconstituted with 2 ml bacteriostatic water = 5 mg/ml, so 0.1 ml = 500 µg. **This is dilution arithmetic from vendor_label, not an efficacy or exposure claim** [vendor_label]. No vendor/forum half-life or bioavailability number is reproduced.

---

## Dropped / refused claims (lack of admissible source)
- **Human half-life** — refused. The "~15 min" / "<30 min" figures are rat/dog (IV/IM), not human [3]. No human t½ exists.
- **Human Cmax / Tmax / AUC** — refused. Secondary outcomes of NCT02637284 but **no results posted** [1].
- **Human oral bioavailability (%F)** — refused. Not measured in [3] (animal IM only) and not posted in [1].
- **Phase 2 subcutaneous dose (mg/µg)** — refused/unavailable. Not disclosed in NCT07437547 record or mirror [2].
- **Quantitative oral gastric-stability kinetics** — only the originating lab's ">24 h" qualitative/author claim; no independent quantitative source [4].
- **Vendor/forum half-life numbers** — refused per integrity rule; vendor_label used for dilution arithmetic only.

---

## Bibliography
- **[1]** PharmaCotherapia d.o.o. *Phase I, Pilot Study in Healthy Volunteers, to Assess the Safety and Pharmacokinetics of PCO-02* (Bepecin / BPC-157, oral). NCT02637284. ClinicalTrials.gov. Registered 2015; est. completion Mar 2016; no results posted. URL: https://clinicaltrials.gov/study/NCT02637284 — id: NCT02637284 — type: rct — (registered; no results posted; human, oral, ~42 healthy volunteers; no PK results).
- **[2]** Hudson Biotech. *A Randomized, Double-Blind, Placebo-Controlled Phase 2 Trial of Pentadecapeptide BPC 157 for Accelerated Repair of Acute Grade II Hamstring Strain (MRI-confirmed)* (subcutaneous). NCT07437547. ClinicalTrials.gov. Start 2 Feb 2026; recruiting. URL: https://clinicaltrials.gov/study/NCT07437547 — id: NCT07437547 — type: rct — (registered; no results posted; human, subcutaneous, ~120; dose not disclosed).
- **[3]** He L, et al. *Pharmacokinetics, distribution, metabolism, and excretion of body-protective compound 157, a potential drug for treating various wounds, in rats and dogs.* Frontiers in Pharmacology. 2022 Dec 14;13:1026182. URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9794587/ — id: PMC9794587 / doi:10.3389/fphar.2022.1026182 — type: animal — (species: Sprague-Dawley rats and beagle dogs; n=6 per dose group per route; IV + IM).
- **[4]** Sikiric P, Hahm K-B, Boban Blagaic A, et al. *Stable Gastric Pentadecapeptide BPC 157, Robert's Stomach Cytoprotection/Adaptive Cytoprotection/Organoprotection, and Selye's Stress Coping Response: Progress, Achievements, and the Future.* Gut and Liver. 2020 Mar 15;14(2):153–167 (pub. online 2019). URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7096228/ — id: PMC7096228 — type: mechanism_review — (gastric-juice stability claim, discovery/origin; no animal n — review).

---

## Post-fix grep audit

Remediation (judge-E, type_tag_discipline): three non-enum type-tags were remapped to the canonical enum — `registered-trial`→`rct` (NCT02637284, NCT07437547; inline note "registered; no results posted" added, and no efficacy number rests on either), `peer-reviewed-animal`→`animal` (He L 2022 rat/dog ADME), `primary-author-review`→`mechanism_review` (Sikiric 2020 originating-lab review). PK substance, route/species flags, and dropped-claims unchanged.

**Grep 1 — non-enum tags must be zero:**
```
$ grep -inE 'registered-trial|peer-reviewed-animal|primary-author-review' section-E.md
(no output — 0 hits; exit code 1)
```

**Grep 2 — all inline `[N, tag]` tags now in the canonical enum:** every inline tag resolves to one of `rct` ([1], [2]), `animal` ([3]), or `mechanism_review` ([4]) — all members of the canonical enum (`rct, meta_analysis, cohort, open_label, animal, in_vitro, mechanism_review, regulatory, compounding_data_sheet, vendor_label, practitioner_protocol, anecdote_aggregate`).

**Confirmation:** no non-enum type-tag remains in section-E.md (inline citations or bibliography).

---

### Post-fix grep audit (iter-4.25, ID-reconcile remediation)

**Fix 1 — NCT02637284 registry overall-status (4.25 hard mismatch B vs E).** Source of truth: WebFetch of `https://clinicaltrials.gov/api/v2/studies/NCT02637284` (v2 API) on 2026-06-18 → `overallStatus` = **"UNKNOWN"** (verbatim), `hasResults` = false. Section E previously stated `"Active, not recruiting"`.

- OLD (E.1 prose): `the record's last known status is "Active, not recruiting"` → NEW: `the record's current registry overall status is "UNKNOWN" (no results posted)`.
- OLD (E.4 dose table): `Active-not-recruiting; no PK results posted` → NEW: `Registry overall status "UNKNOWN"; no PK results posted`.

Residual check — `grep -inE 'active,? not recruiting' section-E.md` → **0 hits** (exit 1). `grep -inE 'UNKNOWN' section-E.md` → hits at L9 (E.1 prose) and L67 (dose table), both the corrected verbatim API status. Disposition: both correct; status now matches the API and Section B verbatim ("UNKNOWN" + "no results posted").

**Cross-section consistency (NCT02637284 status, B vs E): CONSISTENT.** Both B (prose L9, bib L33, summary L49) and E (prose L9, table L67) use the verbatim API string **"UNKNOWN"** plus "no results posted." No "Active, not recruiting" residual in either file.
