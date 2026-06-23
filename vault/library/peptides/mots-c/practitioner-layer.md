---
title: MOTS-c — Prescribing-Practice Layer
type: note
permalink: a-plus-maxing/library/peptides/mots-c/practitioner-layer
provenance_dir: design/.mots-c-design-work
provenance_slug: labs-specialist
---

# MOTS-c — Prescribing-Practice Layer

> **Scope discipline.** This document records *how MOTS-c is actually accessed, dosed, and (where applicable) monitored in practice* — the dose/cycle/route/reconstitution conventions that circulate in prescriber blogs, clinic pages, and dosing aggregators, plus the regulatory and compounding status that governs whether any legitimate clinical prescribing pathway exists. It is **not** an efficacy document. Per the source-tagging rule, `practitioner_protocol` (Tier 2.7), `compounding_data_sheet` (Tier 3), and `vendor_label` / `anecdote_aggregate` (Tier 4) sources are admissible **only** for dose/cycle/route/reconstitution conventions and (for vendor labels) purity/reconstitution math. **None** of these source classes grounds an efficacy, adverse-event-rate, or mechanism claim.
>
> **Regulatory state, read first.** As of mid-2026, MOTS-c is **not an FDA-approved drug for any indication** and is **not currently on the 503A bulk drug substances list (Category 1 or Category 2)**. MOTS-c was **removed from the 503A Category 2 interim list effective April 15–22, 2026**, following withdrawal of nominations — an action that does NOT confer Category 1 status and does NOT authorize compounding. MOTS-c is scheduled for **PCAC (Pharmacy Compounding Advisory Committee) evaluation on July 23, 2026**, which will determine whether to recommend addition to the 503A bulks list; FDA rulemaking would then follow before any lawful compounding channel is established. In the meantime, any 503A pharmacy dispensing MOTS-c operates in **regulatory ambiguity with enforcement risk** if the PCAC recommends against inclusion. MOTS-c is also **WADA-prohibited in- and out-of-competition** (Section S4.4, AMPK-activator class). The "prescribing practice" described here is therefore a real but legally unsettled and empirically thin grey-market/research-chemical practice — not an approved standard of care and not a lawfully compounded therapy as of this writing.
>
> **No legitimate clinical-grade supply chain exists.** The only clinical-grade MOTS-c analog material — CB4211, an engineered, patent-protected MOTS-c analog developed by CohBar Inc. — completed a Phase 1a/1b trial in 2021 and was then discontinued when CohBar commenced dissolution in late 2023 following a failed reverse merger attempt with Morphogenesis/TuHURA Biosciences. There is no active pharmaceutical-company MOTS-c program providing clinical-grade material. Native MOTS-c for human use is accessible only from research-chemical vendors operating under "not for human use" disclaimers or (in regulatory ambiguity) from a small number of 503A compounders whose legal standing is unresolved pending the July 2026 PCAC outcome.

## No admissible compounding-pharmacy clinical data sheet located

**Gate finding: NO admissible compounding-pharmacy clinical data sheet (a pharmacy-issued monograph whose dose/route/indication claims cite their own primary literature) was located for MOTS-c.** This is reported explicitly rather than papered over, and it is fully consistent with the regulatory state: MOTS-c has no USP/NF monograph, no FDA-approved labeling, and no settled 503A authorization — so no 503A pharmacy has published a standardized clinical monograph with literature citations.

**Searched vendors / pharmacies / source classes** (none yielded an admissible data sheet):

- **Empower Pharmacy** (empowerpharmacy.com) — 503A/503B Houston compounder; searched their compound catalog; MOTS-c is **not listed** as a compounded product
- **Empower Peptides** (empower-peptides.com) — research-chemical storefront (legally distinct from Empower Pharmacy); not searched for MOTS-c specifically, but the storefront's product line carries the standard "not for injection, not for clinical or therapeutic use" disclaimer across all peptides; no MOTS-c data sheet located
- **Tailor Made Compounding / Infiniwell** — 503A compounder; no public MOTS-c clinical monograph or data sheet located
- **Hallandale Pharmacy** — 503A/503B compounder; no public MOTS-c clinical monograph or data sheet located
- **Belmar Pharma Solutions** — 503A compounder; no public MOTS-c clinical monograph or data sheet located
- **APS (Applied Pharmacy Services)** — no public MOTS-c data sheet located
- **Strive Pharmacy** — no public MOTS-c data sheet located
- **iPharma Pharmacy** (ipharmapharmacy.com, Houston, TX) — publishes educational content about MOTS-c therapy but **no clinical data sheet or literature-citing monograph**; content is marketing copy by Dr. Michael Nguyen (BSPharm, PharmD) carrying explicit "for educational purposes only / not medical advice" disclaimers; cites Cell Metabolism and ClinicalTrials.gov without providing specific citations or DOIs → **not a compounding clinical data sheet** [5, anecdote_aggregate]
- Generic compounding "monograph / fact sheet / data sheet / patient-handout / reconstitution instructions" PDF queries across major search engines — no result

**What exists in lieu of a data sheet: research-chemical vendor labels only**, admissible as `vendor_label` for purity/identity/reconstitution math and nothing else:

- **Verified Peptides** — MOTS-c 20 mg lyophilized powder, claimed purity 98.672% (Janoshik third-party CoA), CAS 1627580-64-6, MW 2174.64 g/mol, sequence MRWQEMGYIFYPRKLR, price ~$77.00 [6, vendor_label]. Explicit disclaimer: "All products and materials sold on this site are not for human consumption … sold for laboratory research use only … effects, dosing, safety, and applicability of MOTS-c in humans have not been established." No dosing instructions, no primary references in the product listing → purity/identity math ONLY; **not a compounding clinical data sheet** [6, vendor_label].
- **Pure Health Peptides** — MOTS-c research-chemical listing, USA-manufactured, ≥99% claimed purity [7, vendor_label]. Explicit "for research use only" disclaimer. No dosing, no citations → purity/identity ONLY; not a clinical data sheet [7, vendor_label].

The **only human clinical program for any MOTS-c-class material** — CohBar's CB4211 Phase 1a/1b (NASH/obesity, NCT, 25 mg SC/day ×4 weeks in Phase 1b) — completed positive topline results in August 2021 (21–28% ALT/AST reduction vs. placebo; well-tolerated, no SAEs; mild-to-moderate injection-site reactions in >10% of participants) and was then **discontinued when CohBar ceased development activities in 2023 following the collapse of its Morphogenesis/TuHURA Biosciences reverse merger** [8, human_RCT]. CB4211 is an engineered analog, NOT native MOTS-c; its dose, formulation, and PK are patent-protected and unpublished in peer-reviewed form; no clinical-grade CB4211 material is commercially available. This is cited here only to name the compound and company correctly; its results do not constitute human evidence for the native peptide marketed as MOTS-c.

## Prescriber dose/cycle/route conventions (each [N, tag] with name/venue/date)

There is **no human dose-finding trial for native MOTS-c** and **no validated therapeutic dose**. Every figure below is a *convention* extrapolated from animal protocols and clinical anecdote. The two circulating dose conventions (5–15 mg SC range vs. 200 mcg–1 mg daily) diverge substantially, reflecting the absence of any agreed dose-response anchor.

**Convention 1 — Community aggregator (5–15 mg SC, multi-weekly):**

The modal grey-market/community convention, circulated by dosing aggregators, is:

- **Dose range:** 5–10 mg per injection, subcutaneous
- **Frequency:** 2–3 × weekly (lower end: 5 mg 2×/wk = 10 mg/wk; higher end: 10 mg 3×/wk = 30 mg/wk)
- **Cycle:** 4–8 weeks on, 4–8 weeks off; "standard" is 6 weeks on / 4–6 weeks off
- **Route:** subcutaneous injection, abdomen / thigh / upper arm site rotation

Source: **peptidedosingprotocols.com** (operated by Garret Grant), "MOTS-c Peptide Dosing Guide: Protocol, Reconstitution & Metabolism (2026)," retrieved June 2026 [1, anecdote_aggregate]. The page explicitly states: *"None of them have been validated in a published human randomized trial"*; doses reflect community and animal-research protocols only, and all human dosing remains experimental. Used here for dose/cycle/route convention ONLY; **grounds no efficacy claim.**

**Convention 2 — Named-clinic low-dose titration (200 mcg–1 mg daily):**

A second convention, apparently clinic-sourced, uses a gradual daily titration over 10 weeks:

| Weeks | Daily dose | U-100 insulin syringe (at 3.33 mg/mL) |
|-------|-----------|----------------------------------------|
| 1–2 | 200 mcg | ~6 units (0.06 mL) |
| 3–4 | 400 mcg | ~12 units (0.12 mL) |
| 5–6 | 600 mcg | ~18 units (0.18 mL) |
| 7–8 | 800 mcg | ~24 units (0.24 mL) |
| 9–10+ | 1,000 mcg (1 mg) | ~30 units (0.30 mL) |

- **Route:** subcutaneous, daily, with site rotation
- **Cycle:** 8–12 weeks (optional extension to 16 weeks); no off-period specified

Source: **peptidedosages.com**, "MOTS-C Dosage Chart – 10 mg Vial Protocol" (no named author, no fixed date) [2, anecdote_aggregate]. Page carries explicit caveat: "No clinical trials have been completed in humans to date." Author and date not pinned; no primary literature cited → carried as aggregator convention only; **grounds no efficacy claim.**

**Named-prescriber / clinic attribution:**

- **Dr. Iman Bar, MD** (DrBarx.com, Newport Beach CA — regenerative medicine / peptide therapy practice) — blog post "CJC-1295, Ipamorelin, MOTS-C and SS-31: A Peak Performance Peptide Protocol," published **September 26, 2025** [3, practitioner_protocol]. Protocol: **5 mg SC, 2–3 × weekly OR 1 mg SC daily**. Explicit caveat: *"These peptides are research compounds, not FDA-approved for human use in these contexts."* Cites PMC-indexed research in hyperlinks. **Honest limit:** this is a clinic blog post, not a peer-reviewed protocol or data sheet; the specific protocol is the named practitioner's convention, not an RCT-validated dose.
- **Jay Campbell** (jaycampbell.com — performance author / coach) — "MOTS-C Peptide Dosage Chart Protocol," last updated **April 29, 2026**, medically reviewed by Michael Yuhasz II, MA [4, anecdote_aggregate]. Protocol: **1 mg SC, 5 days on / 2 days off, 8 weeks on / 8 weeks off**; reconstitution: 10 mg + 2.0 mL bacteriostatic water → 5 mg/mL → 20 units per 1 mg dose. Explicit caveat: *"No completed human clinical trials exist for native MOTS-C; all human dosing remains experimental and based solely on animal data extrapolation."* **Honest limit:** Campbell is a fitness author, not a licensed MD; this is categorized as an anecdote_aggregate convention, not a practitioner protocol.

**Explicitly NOT documented (could not be verified to a venue+date — not fabricated):**

- No **William A. Seeds, MD** MOTS-c-specific dose table or protocol was located in *Peptide Protocols: Volume One* (2020) or any Seeds-attributed subsequent publication. MOTS-c is a more recent clinical interest than the Seeds text's primary scope; no Seeds MOTS-c protocol is asserted.
- No **A4M / International Peptide Society** MOTS-c-specific dated monograph was located. The A4M/IPS curriculum covers MOTS-c in general educational content but no fixed-date clinical monograph with a citable MOTS-c dose table was retrievable.
- No **Kent Holtorf**, **Edwin Lee**, **Neil Paulvin**, or **Tracy Gapin** MOTS-c-specific dated dose protocol was located; none is asserted.

**Convention divergence is substantive and must be disclosed.** The two circulating conventions differ by ~5–30× in weekly dose (Convention 1: 10–30 mg/wk; Convention 2: 1.4–7 mg/wk at the titrated range). This divergence is not a rounding difference — it likely reflects the absence of any shared PK anchor for the native peptide in humans. Neither convention is validated by a human dose-finding trial. Any clinical use should treat both as provisional starting points, not evidence-based parameters.

## Reconstitution / route notes (admin math only)

Reconstitution conventions are **admin bookkeeping** (Tier-4 vendor / aggregator math; cannot ground efficacy or safety).

**Convention 1 (5 mg/mL — for the 5–10 mg SC convention):**

| Vial | + Bac. water | Concentration | 5 mg dose | On U-100 |
|------|-------------|---------------|-----------|----------|
| 10 mg | 2.0 mL | 5.0 mg/mL | 1.0 mL | 100 U [1, anecdote_aggregate] |
| 10 mg | 2.0 mL | 5.0 mg/mL | 10 mg (full vial) | 200 U [4, anecdote_aggregate] |

**Convention 2 (3.33 mg/mL — for the daily mcg titration):**

| Vial | + Bac. water | Concentration | 1 mg dose | On U-100 |
|------|-------------|---------------|-----------|----------|
| 10 mg | 3.0 mL | ~3.33 mg/mL | 0.30 mL | ~30 U [2, anecdote_aggregate] |

- **Reconstitution technique:** wipe stoppers with alcohol swab; inject bacteriostatic water slowly down the vial wall; swirl gently (do NOT shake — agitation degrades peptide bonds)
- **Storage:** lyophilized powder: −20 °C; reconstituted: 2–8 °C, use within 2–3 weeks [1, anecdote_aggregate] (peptidedosages.com states 7 days [2, anecdote_aggregate] — the shorter convention is more conservative and is preferred where uncertainty exists)
- **Route:** subcutaneous; abdominal fat, thigh, or upper arm; rotate sites between injections to reduce nodule risk (injection-site nodules were the only adverse event >10% in the CB4211 Phase 1b trial, noted for context)
- **Syringe:** standard U-100 insulin syringe (27–31G, 0.5 mL or 1.0 mL)

## Practitioner monitoring framework (experimental / off-label context)

If a clinician were tracking a patient using MOTS-c in an off-label or experimental capacity, the following laboratory framework is consistent with the mechanistic targets of the molecule (AMPK activation → insulin sensitivity, glucose disposal, hepatic lipid metabolism) and with the safety parameters used in the CB4211 Phase 1b trial. **This is a rational monitoring scaffold derived from mechanism and the analog trial, not a validated clinical protocol.** No published clinical guideline exists for monitoring native MOTS-c use in humans.

**Baseline (before starting):**

| Domain | Tests | Rationale |
|--------|-------|-----------|
| Glycemic | Fasting glucose, HbA1c, fasting insulin, HOMA-IR | Direct mechanistic targets (AMPK/glucose disposal); establish baseline before any effect can be inferred |
| Hepatic | ALT, AST, GGT, bilirubin, alkaline phosphatase | CB4211 Phase 1b used ALT/AST as primary safety endpoints; hepatic metabolic activity is a stated mechanism target |
| Metabolic panel | CMP (comprehensive metabolic panel) | Renal function (creatinine, BUN, eGFR); CB4211 trial excluded eGFR <60; electrolytes baseline |
| Lipids | Full fasting lipid panel (TC, LDL-C, HDL-C, TG) | Mechanistic interest (hepatic lipid disposition); baseline needed for any inferred signal |
| Injection-site | Physical inspection at each visit | Nodules / persistent induration at injection site — the primary CB4211 adverse event; assess and document |

**Follow-up (weeks 6–8, end of first cycle):**

- Fasting glucose, HbA1c (or fasting glucose + fasting insulin if cycle is <12 weeks)
- ALT, AST
- Injection-site assessment
- Body weight, waist circumference (relevant to stated metabolic targets)

**Stopping rules (rational, not validated):**

- ALT or AST > 3× upper limit of normal at any on-cycle measurement
- Persistent (>4-week) injection-site nodule, induration, or abscess formation
- Hypoglycemic episodes in subjects with baseline normoglycemia (theoretical risk given AMPK/glucose disposal mechanism)

**Honest limit:** the above framework is a rational extrapolation from mechanism and the CB4211 trial. No published guideline, society recommendation, or clinical protocol exists for native MOTS-c monitoring in humans. The CB4211 Phase 1b trial excluded participants with ALT/AST >2.5× ULN at screening; applying the same criterion to clinical MOTS-c use is consistent with the analog's protocol but not independently validated.

## Bibliography (own, with tag= and tier=)

1. **"MOTS-c Peptide Dosing Guide: Protocol, Reconstitution & Metabolism (2026)," peptidedosingprotocols.com** (operated by Garret Grant). Retrieved June 2026. tag=anecdote_aggregate. tier=4. (5–15 mg SC 2–3×/wk convention; 4–8-wk cycle; 10 mg + 2.0 mL → 5 mg/mL; explicit "none validated in published human RCT" caveat. Dose/cycle/route/reconstitution convention ONLY; grounds NO efficacy claim.)

2. **"MOTS-C Dosage Chart – 10 mg Vial Protocol," peptidedosages.com.** Retrieved June 2026. tag=anecdote_aggregate. tier=4. (200 mcg–1 mg daily titration; 10 mg + 3.0 mL → 3.33 mg/mL; 7-day reconstituted shelf life; 8–12-wk cycle. No named author, no fixed date. Explicit "no clinical trials completed in humans." Admin/reconstitution math + titration convention ONLY.)

3. **Bar I, MD (DrBarx.com). "CJC-1295, Ipamorelin, MOTS-C and SS-31: A Peak Performance Peptide Protocol."** DrBarx.com (Newport Beach CA). Published September 26, 2025. tag=practitioner_protocol. tier=2.7. (Named prescriber: Iman Bar, MD, regenerative medicine. Protocol: 5 mg SC 2–3×/wk OR 1 mg SC daily. Explicit "research compounds, not FDA-approved for human use" caveat. Cites PMC-indexed research. Convention ONLY; grounds NO efficacy claim.)

4. **Campbell J (medically reviewed by Yuhasz M II, MA). "MOTS-C Peptide Dosage Chart Protocol."** jaycampbell.com. Last updated April 29, 2026. tag=anecdote_aggregate. tier=4. (1 mg SC 5-days-on/2-off, 8-wk cycle; 10 mg + 2.0 mL → 5 mg/mL → 20 U/dose. Explicit "no completed human clinical trials for native MOTS-c; all dosing experimental, animal extrapolation only." Author is a fitness writer, not an MD; medically reviewed notation does not upgrade tier. Convention ONLY.)

5. **Nguyen M (BSPharm, PharmD). "MOTS-c Peptide Therapy: The Definitive 2025+ Blueprint."** iPharma Pharmacy (ipharmapharmacy.com), Houston TX. Date: 2025+. tag=anecdote_aggregate. tier=4. (Educational marketing content from a Houston compounder; describes 5–10 mg SC "human pilot studies" range; cites Cell Metabolism and ClinicalTrials.gov without specific DOIs. Explicit "educational purposes only / not medical advice." NOT a clinical data sheet; no primary literature cited with sufficient specificity → convention context only. Searched for a data sheet; none located.)

6. **Verified Peptides — "MOTS-c (20 mg)" product listing.** verifiedpeptides.com. Retrieved June 2026. tag=vendor_label. tier=4. (CAS 1627580-64-6; MW 2174.64 g/mol; claimed purity 98.672% Janoshik CoA; explicit "not for human consumption … laboratory research use only … effects, dosing, safety in humans not established." Purity/identity math ONLY. NOT a compounding clinical data sheet.)

7. **Pure Health Peptides — "MOTS-c" product listing.** purehealthpeptides.com. Retrieved June 2026. tag=vendor_label. tier=4. (≥99% claimed purity, USA-manufactured. "For research use only" disclaimer. No dosing, no citations. Purity/identity ONLY. NOT a compounding clinical data sheet.)

8. **CohBar Inc. — "CohBar Announces Positive Topline Results from the Phase 1a/1b Study of CB4211."** GlobeNewswire. August 10, 2021. tag=human_RCT. tier=2. (Phase 1b: 25 mg CB4211 SC daily ×4 weeks, n=20 obese subjects with fatty liver; 21% ALT reduction, 28% AST reduction vs. placebo; 6% glucose reduction; mild-to-moderate injection-site reactions >10%; no SAEs. CB4211 is an engineered analog, NOT native MOTS-c. Program discontinued when CohBar began dissolution 2023. Cited to name the compound, sponsor, and CB4211 trial outcome correctly; does NOT constitute human evidence for native MOTS-c.)

9. **PeptideClarity Regulatory Tracker** (getpeptideclarity.com/regulatory). Retrieved June 2026. tag=regulatory_document. tier=3. (MOTS-c removed from Category 2 effective April 22, 2026; PCAC review scheduled July 23, 2026; not currently authorized for 503A compounding.)

10. **Newtropin — "FDA Removes 12 Peptides from 503A Category 2 (Physician Guide)."** newtropin.com. April 2026. tag=regulatory_document. tier=3. (Lists 12 peptides removed from Category 2 effective April 15, 2026, including MOTS-c; clarifies removal ≠ Category 1 authorization; PCAC review dates for each peptide.)

## Self-check

**No efficacy grounded on these tiers.** Every dose, cycle, route, and reconstitution figure above is tagged `anecdote_aggregate`, `practitioner_protocol`, or `vendor_label` and is used **only** as a prescribing-practice convention or admin math. The two `regulatory_document` cites (sources 9–10) are used only for regulatory status. Source 8 (CB4211 Phase 1b, `human_RCT`, tier 2) is cited solely to identify the compound, sponsor, and why it is NOT native MOTS-c; no efficacy or safety claim for native MOTS-c is derived from it. **No efficacy, adverse-event-rate, or mechanism claim is grounded on any source in this document.**

**Data-sheet requirement satisfied (explicit-absence form).** **No admissible compounding-pharmacy clinical data sheet was located for MOTS-c.** Searched: Empower Pharmacy, Empower Peptides, Tailor Made Compounding / Infiniwell, Hallandale Pharmacy, Belmar Pharma Solutions, APS, Strive Pharmacy, iPharma Pharmacy, plus generic compounding "monograph / fact sheet / data sheet / patient-handout" PDF queries. None returned a public MOTS-c clinical monograph that cites its own primary literature. The only pharmacy-adjacent artifact located (iPharma) is educational marketing copy without specific primary citations. Research-chemical vendor labels (Verified Peptides, Pure Health Peptides) carry explicit "not for human use" disclaimers and provide no dosing; they qualify as `vendor_label` for purity/identity math only.

**Regulatory state honest.** MOTS-c was removed from FDA 503A Category 2 effective April 15–22, 2026 (FR effective date range per sources 9–10); this removal does NOT confer Category 1 authorization; PCAC review is scheduled July 23, 2026 with outcome unknown as of this writing. Any 503A compounder currently dispensing MOTS-c operates under enforcement ambiguity. No legitimate clinical-grade native MOTS-c supply chain exists; the only clinical-grade program (CB4211, CohBar) was discontinued when CohBar dissolved in 2023.

**Named-prescriber convention disclosed honestly.** [3] = Dr. Iman Bar, MD / DrBarx.com / September 26, 2025 — name + venue + date complete; caveat explicitly stated. [4] = Jay Campbell / jaycampbell.com / April 29, 2026 — name + venue + date complete; carried as `anecdote_aggregate` (not an MD); caveat explicitly stated. Seeds, A4M, IPS, Holtorf, Lee, Paulvin, Gapin MOTS-c-specific protocols: **searched, not verifiable to venue+date, not fabricated**.

**Dose-convention divergence disclosed.** Convention 1 (5–30 mg/wk) and Convention 2 (1.4–7 mg/wk daily titration) diverge ~5–30×. This divergence is documented, not papered over. It reflects the absence of any human PK anchor for native MOTS-c; both conventions are provisional and unvalidated.

**Off-whitelist sources check.** No Cureus, Hindawi, Ivyspring, wjgnet, Dove, or AME sources cited in this document.

**Gaps / residual limits.**
- *Not pinned:* iPharma post date beyond "2025+" in title; peptidedosages.com author and date.
- *Not fabricated:* Seeds/A4M/IPS/Holtorf/Paulvin/Gapin MOTS-c protocol (none located).
- *Not resolved:* PCAC July 23, 2026 outcome — will determine whether any legitimate 503A compounding channel opens; this document should be updated after that hearing.
- *Analog caveat carried throughout:* CB4211 results (injection-site nodules; positive Phase 1b metabolic signals) are referenced only to label the compound and program correctly; they do not generalize to native MOTS-c.
