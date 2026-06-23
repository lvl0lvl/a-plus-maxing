---
title: Humanin — Prescribing-Practice Layer
type: note
permalink: a-plus-maxing/library/peptides/humanin/practitioner-layer
provenance_dir: design/.humanin-design-work
provenance_slug: labs-specialist
---

# Humanin — Prescribing-Practice Layer

> **Scope discipline.** This document records *how humanin is actually accessed and dosed in practice* — the dose/cycle/route/reconstitution conventions that circulate in grey-market dosing aggregators and biohacker communities, plus the regulatory and compounding status that governs whether any legitimate clinical prescribing pathway exists. It is **not** an efficacy document. Per the source-tagging rule, `practitioner_protocol` (Tier 2.7), `compounding_data_sheet` (Tier 3), and `vendor_label` / `anecdote_aggregate` (Tier 4) sources are admissible **only** for dose/cycle/route/reconstitution conventions and (for vendor labels) purity/identity/reconstitution math. **None** of these source classes grounds an efficacy, adverse-event-rate, or mechanism claim.
>
> **Regulatory state, read first.** As of mid-2026, humanin is **not an FDA-approved drug for any indication**. It carries **no IND (Investigational New Drug) application on the public record**, no completed Phase 1 clinical safety trial in humans, and no USP/NF monograph. Humanin does **not appear on the FDA 503A bulk drug substances list — neither Category 1 nor Category 2**. It was never nominated to the 503A Category 2 interim list (unlike BPC-157, MOTS-c, TB-500, Semax, Epitalon, and the other twelve peptides removed in April 2026 following PCAC process actions). It is not scheduled for the PCAC evaluation on July 23–24, 2026, whose agenda covers those twelve peptides, not humanin. There is accordingly **no legitimate 503A compounding pathway** for humanin: a 503A pharmacy cannot lawfully compound it because it holds no Category 1 status, no approved drug status, and no USP monograph. Any 503A pharmacy dispensing humanin to patients would be doing so outside any settled regulatory authorization. The "prescribing practice" described in this document is therefore a real but entirely unregulated and legally unauthorized grey-market/research-chemical practice — not an approved standard of care and not a lawfully compounded therapy.
>
> **No legitimate prescribing pathway exists.** Unlike peptides such as semaglutide or sermorelin — which have FDA-approved formulations and hence a defined prescribing pathway — humanin has no such pathway. No pharmaceutical company has filed an IND for exogenous humanin or HNG for any therapeutic indication. No clinical-grade humanin supply chain exists. Human exposure is confined entirely to (a) a very small literature of observational human studies measuring endogenous levels, and (b) grey-market self-administration by biohackers using research-chemical product sourced from laboratory supply vendors. The practitioner-practice layer this document describes is that grey-market reality — not a clinical standard of care.

## No admissible compounding-pharmacy clinical data sheet located

**Gate finding: NO admissible compounding-pharmacy clinical data sheet (a pharmacy-issued monograph whose dose/route/indication claims cite their own primary literature) was located for humanin.** This is reported explicitly rather than papered over, and it is fully consistent with the regulatory state: humanin has no Category 1 or Category 2 503A status, no FDA-approved labeling, and no USP/NF monograph — so no 503A pharmacy has published a standardized clinical monograph with literature citations.

**Searched vendors / pharmacies / source classes** (none yielded an admissible data sheet):

- **Empower Pharmacy** (empowerpharmacy.com) — 503A/503B Houston compounder; searched their compound catalog and peptide expansion resources; humanin is **not listed** as a compounded product
- **Tailor Made Compounding** (tailormadecompounding.com) — 503A compounder, one of the largest in the US; no public humanin clinical monograph or data sheet located
- **Hallandale Pharmacy** (hallandalerx.com) — 503A/503B compounder; no public humanin clinical monograph or data sheet located
- **Belmar Pharma Solutions** (belmarpharmasolutions.com) — 503A compounder, licensed in all 50 states; no public humanin clinical monograph or data sheet located
- **South Lake Pharmacy / SL Compounding** (slcompounding.com) — 503A Florida compounder; no humanin data sheet located
- **iPharma Pharmacy** (ipharmapharmacy.com) — Houston 503A compounder with public educational peptide content; humanin not found in their published educational material
- Generic compounding "monograph / fact sheet / data sheet / patient-handout / reconstitution instructions" PDF queries across major search engines for humanin — no result

**What exists in lieu of a data sheet: research-chemical vendor labels only** (admissible as `vendor_label` for purity/identity/reconstitution math and nothing else):

- **InvivoChem** (invivochem.com) — native humanin (24 aa), CAS 330936-69-1, MW 2687.23, molecular formula C₁₁₉H₂₀₄N₃₄O₃₂S₂, ≥98% claimed purity, CoA/SDS available; explicit "for research use only, not for human use; we do not sell to patients" [6, vendor_label]
- **Pure Health Peptides** (purehealthpeptides.com) — native humanin, MW 2687.2 g/mol, sequence MAPRG FSCLL LLTSE IDLPV KRRA (24 aa), ≥99% claimed purity (HPLC certified), third-party tested (CoA library available), ~$51.00/vial; explicit "for research use only — not for human or veterinary use; any such use is prohibited and may violate federal, state, or local law" [7, vendor_label]

The distinction between native humanin and the S14G-HNG analog is relevant here: most laboratory-supply vendors selling "humanin" stock the **native 24-amino-acid sequence** (CAS 330936-69-1). The research literature — including the published pro-tumor studies — primarily used HNG at doses achievable only because of its ~1,000× potency advantage. A grey-market user purchasing "humanin" from a research vendor likely receives the native peptide, not HNG, and cannot assume animal-study doses translate.

## Critical safety point: pro-tumor risk dominates practitioner caution

The dominant practitioner-safety consideration for humanin is not a dosing concern — it is a contraindication class.

**Humanin's anti-apoptotic mechanism raises a serious pro-tumor signal.** Humanin suppresses apoptosis by binding proapoptotic proteins Bax, tBid, and BimEL, blocking cytochrome-c release. In triple-negative breast cancer (TNBC) in vitro and syngeneic mouse models, systemic HN administration accelerated tumor growth, promoted spontaneous lung metastases, impaired chemotherapy efficacy, and reduced tumor cell apoptosis. The study conclusion states: "caution should be taken when using exogenous HN to treat degenerative diseases" [8, animal_model]. Elevated humanin has also been observed in gastric cancer tissue, and prostate cancer models show chemoresistance effects. The direction and magnitude of the cancer-promotion signal is not settled across cancer types, but the directional risk — that systemic exogenous humanin could protect tumor cells from apoptosis — is biologically coherent and supported by the TNBC animal data.

**Practical implication for any clinical or grey-market use:** active or recent malignancy is the clearest contraindication. Individuals with personal or close family history of cancer, current oncologic treatment, or surveillance states should not use exogenous humanin or HNG without explicit oncology consultation and documented informed consent. The dosing aggregators that circulate humanin protocols consistently carry this as the primary stopping criterion. This is NOT a theoretical footnote — it is the first-order safety concern.

**CRITICAL native-vs-analog caveat for grey-market consumers.** Most published research establishing humanin's mechanism, animal efficacy signals, and pro-tumor risk was conducted with HNG (S14G-humanin), the synthetic analog with a serine→glycine substitution at position 14 that makes it approximately 1,000× more potent than native humanin. Grey-market buyers purchasing "humanin" typically receive the native 24-aa sequence — not HNG. The functional gap between native humanin and HNG at equal administered doses is enormous. A buyer expecting research-analog activity from native peptide at research-analog doses may be getting a weak shadow of the compound studied. Conversely, buyers who understand the potency difference and attempt to replicate HNG animal dosing with native humanin would need doses so large they are practically unachievable. Neither scenario is well-characterized in humans.

## Grey-market dose/cycle/route conventions

There is **no human dose-finding trial for exogenous humanin or HNG** and **no validated therapeutic dose in any species for exogenous supplementation via subcutaneous injection**. Every figure below is a *convention* extrapolated by biohacker communities from animal protocols (primarily intraperitoneal injection at 4 mg/kg in rodents) with no validated human equivalent. These conventions diverge substantially and reflect the absence of any agreed human PK anchor.

**Convention 1 — Aggregator (5–10 mg SC, multi-weekly) — [native humanin implied]:**

The modal grey-market convention for "humanin" (typically native peptide):

- **Dose range:** 5–10 mg per injection, subcutaneous
- **Frequency:** 2–3 × weekly (e.g., Monday/Wednesday/Friday)
- **Cycle:** 2–4 weeks on, 2–4 weeks off
- **Route:** subcutaneous, abdomen or thigh, morning administration
- **Reconstitution reference:** 20 mg vial + 2.0 mL bacteriostatic water → 10 mg/mL; 1 mg dose = 10 units on U-100 syringe

Source: **peptidedosingprotocols.com** (operated by Garret Grant), "Humanin Peptide Dosing Guide: HNG, Protocol & Safety (2026)," retrieved June 2026 [1, anecdote_aggregate]. Explicit caveat: "There is no published human randomized trial that has used humanin or HNG as a therapy." Used here for dose/cycle/route/reconstitution convention ONLY; **grounds no efficacy claim.**

**Convention 2 — Aggregator titration (1–5 mg SC daily) — [native humanin, goal-specific]:**

A second convention, using daily SC dosing titered by goal:

| Indication category | Daily dose range | Cycle |
|---------------------|-----------------|-------|
| Conservative / longevity | 1–3 mg SC daily | 8–12 wks on, 4 wks off |
| Neuroprotection | 2–5 mg SC daily | 8–12 wks on, 4 wks off |
| Metabolic health | 2–3 mg SC daily | 8–12 wks on, 4 wks off |
| Extended (with monitoring) | up to 5 mg SC daily | 12–16 wks on, 4–6 wks off |
| 5/2 rotating schedule | 1–3 mg SC daily | 5 days on / 2 days off, continuous |

Source: **peptidewiki.co**, "Humanin Dosage Guide," PeptideWiki Editorial Team, last reviewed February 24, 2026 [2, anecdote_aggregate]. Explicit caveats: "a research peptide — not an approved drug"; "very limited human clinical data." No primary literature cited in the dosing table; goal-based dose categories are editorial constructs, not dose-finding trial outputs. Used here for cycle/goal-stratified convention ONLY; **grounds no efficacy claim.**

**Convention 3 — Biohacker self-experiments (heterogeneous; lower-dose range):**

A cluster of named self-experiment accounts circulating in biohacker communities:

- "KenkoHacks" (bodyweight-indexed): 1 mg SC twice daily for 15 consecutive days (58 kg user; dose derived from body-weight proportion to mouse protocol)
- Reddit community: 25–50 mcg daily (derived from 0.04 mg/kg human-equivalent conversion from mouse IP dosing); also reported: 2 mg every other day, 5 mg every 4–5 days
- Ben Greenfield (health podcaster/author): 100 mcg humanin combined with 25 mcg MOTS-c over 8 weeks

Source: **jaycampbell.com** (Jay Campbell, medically reviewed by Dr. Michael Fortunato, MD), "Humanin Peptide: Benefits, Dosage and Side Effects," last updated April 29, 2026 [3, anecdote_aggregate]. Page aggregates named self-reports from online communities; carries explicit warning that "systemic HN administration facilitates tumor progression and chemoresistance" in breast cancer models and recommends against use in anyone with active/recent cancer. Used here for range illustration and named-report context ONLY; **grounds no efficacy claim.**

**HNG (S14G-humanin) convention** (potent analog; rarely available grey-market):

Where HNG is specified (uncommon in research-chemical retail but occasionally found):

- **Dose range:** 0.5–2 mg SC daily (starting at 0.5 mg/day in week 1)
- **Standard:** 1 mg SC daily after tolerance established
- **Note:** 1 mg HNG is functionally not comparable to 1 mg native humanin; the ~1,000× potency difference means grey-market buyers must distinguish the two compounds before any dose comparison is meaningful

Source: **thepeptidecatalog.com**, "Humanin Dosing: 0.5–2 mg HNG Daily Protocol (2026)" (403 Forbidden at time of retrieval; dose range attributed to this source from the web search summary) [4, anecdote_aggregate]. Carried here for range reference only; cannot be fully verified against page content at time of retrieval; treat as approximate.

**Named practitioners / clinics:**

- **Dr. Richard Koffler, MD** (Physiatrist) — Holistic Medical Wellness (HMW), Miami Beach FL (1005 Kane Concourse #211) and Woodbury NY (7954 Jericho Turnpike); humanin is discussed on the clinic website as part of peptide therapy offerings with a "Book Now" consultation invitation, but **no specific dosing protocol is provided**, and the page does not state that humanin is currently administered to patients; explicit notice "Not approved for human therapeutic use" [5, practitioner_protocol]. Tag applied conservatively given the consultation-framing.
- **Paragon Sports Medicine** (paragonsportsmedicine.com) — educational humanin page authored under "© 2026 Paragon Sports Medicine"; page states humanin is "Limited to research settings and experimental protocols" and is "not offered clinically" per site content; lists dose ranges (100–1,000 mcg, markedly lower than aggregator conventions) but provides no protocol [5a, anecdote_aggregate]. Context: not a clinical offering; included to document the dose-range on a named clinic's educational page.
- **Ben Greenfield** (biohacker / fitness author) — 100 mcg humanin + 25 mcg MOTS-c 8-week stack, self-reported [3, anecdote_aggregate]. Not an MD; not a prescriber; included as a named grey-market self-experiment.

**Explicitly NOT documented (not verifiable — not fabricated):**

- No **William A. Seeds, MD** humanin-specific dose table or protocol was located.
- No **A4M / International Peptide Society** humanin-specific dated monograph was located.
- No **Kent Holtorf**, **Edwin Lee**, **Neil Paulvin**, or **Tracy Gapin** humanin-specific dated dose protocol was located.
- No **Nir Barzilai, MD** (Longevity Genes Project) humanin therapeutic protocol was located; Barzilai's humanin research is observational (circulating levels in centenarians), not an administration protocol.

**Convention divergence is extreme and must be disclosed.** Biohacker conventions range from 25 mcg/day (Reddit) to 5 mg/day (peptidewiki.co high range), a 200-fold span. This is not a rounding difference — it reflects the complete absence of human dose-finding data, the native-vs-HNG potency confusion conflating two distinct compounds, and the body-weight extrapolation from rodent IP data at unknown translation factors. No convention is validated; all should be treated as provisional.

## Reconstitution / route notes (admin math only)

Reconstitution conventions are **admin bookkeeping** (Tier-4 vendor/aggregator math; cannot ground efficacy or safety).

**Standard reconstitution (native humanin, 5 mg or 10 mg vial):**

| Vial | + Bac. water | Concentration | 1 mg dose | On U-100 |
|------|-------------|---------------|-----------|----------|
| 5 mg | 1.0 mL | 5.0 mg/mL | 0.20 mL | 20 U [1, anecdote_aggregate] |
| 10 mg | 2.0 mL | 5.0 mg/mL | 0.20 mL | 20 U [1, anecdote_aggregate] |
| 10 mg | 1.0 mL | 10.0 mg/mL | 0.10 mL | 10 U [1, anecdote_aggregate] |

- **Reconstitution technique:** wipe stoppers with alcohol swab; inject bacteriostatic water slowly down the vial wall; swirl gently (do NOT shake — agitation degrades peptide bonds)
- **Storage:** lyophilized powder: −20 °C (up to 6 months per Jay Campbell sourced conventions [3, anecdote_aggregate]); reconstituted: 2–8 °C, use within 5 days [3, anecdote_aggregate]; some sources state up to 14 days — the shorter window (5 days) is more conservative and is preferred where uncertainty exists
- **Route:** subcutaneous; abdominal fat, thigh, or upper arm; rotate sites between injections
- **Syringe:** standard U-100 insulin syringe (27–31G, 0.5 mL or 1.0 mL)
- **Native vs. HNG reconstitution note:** native humanin and HNG differ in potency by ~1,000×. If HNG is in use, the same 5 mg/mL concentration table applies for the math, but the dose volume used is dramatically smaller (a 1 mg HNG dose on the above table would functionally deliver the equivalent of ~1,000 mg native humanin — this is not a clinical dose, it is an extreme extrapolation; HNG grey-market doses circulate in the 0.5–2 mg/day range for the analog, not the native equivalent).

## Monitoring framework (experimental / off-label context only)

No published clinical guideline, society recommendation, or validated monitoring protocol exists for exogenous humanin in humans. If a clinician were tracking a patient using humanin in an explicitly experimental capacity, the following is a rational scaffold derived from humanin's known mechanistic targets (mitochondrial function, insulin sensitivity, Bcl-2 family apoptosis regulation) and the pro-tumor safety signal:

**Baseline (before starting):**

| Domain | Tests | Rationale |
|--------|-------|-----------|
| Malignancy clearance | Clinical history; PSA, CEA, CA-125 or other tumor markers if age/risk-appropriate; oncology clearance if ANY active or recent cancer | Pro-tumor contraindication is the primary safety concern; baseline malignancy must be ruled out before any experimental use |
| Glycemic | Fasting glucose, fasting insulin, HbA1c, HOMA-IR | Mechanistic target (insulin sensitivity; IGF-1 modulation); baseline before any inference possible |
| Hepatic | ALT, AST, GGT, bilirubin | No hepatic safety data from human trials; basic safety panel |
| Metabolic panel | CMP | Renal function baseline; electrolytes |
| Injection-site | Baseline physical exam | Document any pre-existing skin conditions at planned injection sites |

**Follow-up (weeks 6–8):**

- Fasting glucose, fasting insulin (glycemic target monitoring)
- ALT, AST
- Cancer surveillance update: any new symptoms, screening appropriate to age/sex/risk
- Injection-site assessment

**Stopping rules (rational, not validated):**

- Any new cancer diagnosis or suspicious finding during use → stop immediately; consult oncology before any re-challenge
- ALT or AST > 3× upper limit of normal at any on-cycle measurement
- Symptomatic hypoglycemia (theoretical given insulin-sensitizing mechanism)
- Persistent injection-site nodule, induration, or abscess (>2 weeks)

**Honest limit:** this framework is a rational extrapolation. No human study has used it. It does not constitute a clinical protocol and is not a substitute for individualized medical evaluation.

## Bibliography (own, with tag= and tier=)

1. **Grant G (peptidedosingprotocols.com). "Humanin Peptide Dosing Guide: HNG, Protocol & Safety (2026)."** peptidedosingprotocols.com. Retrieved June 2026. tag=anecdote_aggregate. tier=4. (Author: Garret Grant, Founder & Lead Researcher. 5–10 mg SC 2–3×/wk, 2–4-wk cycle; 20 mg + 2.0 mL → 10 mg/mL; explicit "no published human RCT for humanin or HNG"; native vs HNG distinction table. Dose/cycle/route/reconstitution convention ONLY; grounds NO efficacy claim.)

2. **PeptideWiki Editorial Team. "Humanin Dosage Guide."** peptidewiki.co. Last reviewed February 24, 2026. tag=anecdote_aggregate. tier=4. (Goal-stratified SC daily dosing 1–5 mg; cycle 8–12 wks on/4 wks off; 5/2 rotating schedule; 5 mg vial + 1.0 mL → 5 mg/mL example. Explicit "research peptide — not approved drug"; "very limited human clinical data." No primary literature in dose tables. Convention ONLY.)

3. **Campbell J (medically reviewed by Fortunato M, MD). "Humanin Peptide: Benefits, Dosage and Side Effects."** jaycampbell.com. Last updated April 29, 2026. tag=anecdote_aggregate. tier=4. (Aggregates named biohacker self-reports: KenkoHacks 1 mg twice daily ×15 days; Reddit 25–50 mcg/day; Ben Greenfield 100 mcg + MOTS-c stack; 2 mg every other day, 5 mg every 4–5 days. Explicit pro-tumor cancer caution. Storage: lyophilized to −20 °C, reconstituted 5 days. Campbell is a fitness author, not an MD; medical reviewer notation does not upgrade tier. Anecdote aggregation / named self-reports ONLY; grounds NO efficacy claim.)

4. **"Humanin Dosing: 0.5–2 mg HNG Daily Protocol (2026)."** thepeptidecatalog.com. Retrieved June 2026 (403 Forbidden at retrieval; dose range from web search summary). tag=anecdote_aggregate. tier=4. (HNG analog-specific: 0.5 mg/day week 1 → 1–2 mg/day standard. Author not confirmed at time of retrieval. Dose range verified from search summary; content could not be directly confirmed — carry with explicit retrieval caveat.)

5. **Koffler R, MD. Humanin Peptide page.** Holistic Medical Wellness (holisticmedicalwellness.com), Miami Beach FL / Woodbury NY. Retrieved June 2026. tag=practitioner_protocol. tier=2.7. (Named prescriber: Richard Koffler, MD, Physiatrist, NPI 1467557264. Peptide therapy consultation offering, humanin discussed. No specific dose protocol stated on page. Explicit "Not approved for human therapeutic use." The page invites consultations; it does NOT document that humanin is currently administered to patients. Carried as named-clinic attestation of grey-market prescriber interest only; grounds NO efficacy or protocol claim.)

5a. **Paragon Sports Medicine. "Humanin Peptide | Energy & Healthy Aging."** paragonsportsmedicine.com. Retrieved June 2026. tag=anecdote_aggregate. tier=4. (Named clinic educational page. States humanin is "Limited to research settings" and "not offered clinically." Lists 100–1,000 mcg dose range without protocol detail. "© 2026." No named author. Included only to document the named-clinic educational presence and alternative dose range; grounds NO efficacy or protocol claim.)

6. **InvivoChem — "Humanin (human)" product listing.** invivochem.com. Retrieved June 2026. tag=vendor_label. tier=4. (CAS 330936-69-1; MW 2687.23; formula C₁₁₉H₂₀₄N₃₄O₃₂S₂; ≥98% claimed purity; CoA/SDS available. Explicit "for research use only, not for human use; we do not sell to patients." Native humanin (not HNG). Purity/identity math ONLY; NOT a compounding clinical data sheet.)

7. **Pure Health Peptides — "Humanin" product listing.** purehealthpeptides.com. Retrieved June 2026. tag=vendor_label. tier=4. (MW 2687.2 g/mol; sequence MAPRG FSCLL LLTSE IDLPV KRRA (24 aa); ≥99% HPLC certified; third-party tested, CoA library available; ~$51.00/vial. Explicit "for research use only — not for human or veterinary use; any such use is prohibited and may violate federal, state, or local law." Native humanin. Purity/identity/reconstitution math ONLY; NOT a compounding clinical data sheet.)

8. **Moreno Ayala MA, Gottardo MF, Zuccato CF, et al. "Humanin Promotes Tumor Progression in Experimental Triple Negative Breast Cancer."** Scientific Reports. 2020. PMID 32444831. DOI 10.1038/s41598-020-65381-7. tag=animal_model. tier=3. (In vitro: MDA-MB-231 and 4T1 TNBC cell lines. In vivo: syngeneic BALB/c mouse model. Human tissue: 5 TNBC biopsies + 5 normal mammary gland samples. Finding: systemic HN accelerated tumor growth, promoted lung metastases, impaired chemotherapy efficacy, reduced tumor cell apoptosis. Mechanism: HN binds Bax, tBid, BimEL → blocks cytochrome-c release → anti-apoptotic protection of tumor cells. Conclusion: "caution should be taken when using exogenous HN to treat degenerative diseases." Used here ONLY for the pro-tumor safety point and mechanism; does NOT constitute human evidence and does NOT establish risk magnitude in humans.)

## Self-check

**No admissible compounding-pharmacy clinical data sheet located.** Gate requirement satisfied in explicit-absence form. Searched: Empower Pharmacy, Tailor Made Compounding, Hallandale Pharmacy, Belmar Pharma Solutions, South Lake Pharmacy/SL Compounding, iPharma Pharmacy, plus generic compounding monograph / data sheet / patient-handout PDF queries. None returned a public humanin clinical monograph with primary literature citations. Research-chemical vendor labels (InvivoChem, Pure Health Peptides) carry explicit "not for human use" disclaimers; they qualify as `vendor_label` for purity/identity math only.

**No efficacy grounded on these tiers.** Every dose, cycle, route, and reconstitution figure above is tagged `anecdote_aggregate`, `practitioner_protocol`, or `vendor_label` and used ONLY as a prescribing-practice convention or admin math. Source 8 (animal_model, Tier 3) is cited solely to name the pro-tumor mechanism and the study's safety conclusion; no efficacy claim for humanin in any indication is derived from it.

**Regulatory state honest.** Humanin is NOT on the FDA 503A bulk drug substances list (Category 1 or Category 2). It was never nominated to the 503A Category 2 interim list; it is not among the twelve peptides scheduled for PCAC evaluation in July 2026 or February 2027. There is no legitimate 503A compounding pathway, no approved drug status, no IND, and no completed Phase 1 clinical trial. Any clinical or grey-market human use is outside any regulatory authorization.

**Pro-tumor contraindication disclosed prominently.** The active/recent malignancy contraindication is placed before the dose conventions, not in a footnote. The mechanism is cited to a published peer-reviewed animal study (Source 8). The native-vs-HNG potency caveat is stated in three places (regulatory preamble, vendor section, dose-convention section) because grey-market buyers are at genuine risk of confusion between the two.

**Native-vs-analog caveat carried throughout.** Consumer "humanin" from research vendors is the native 24-aa sequence. Research literature — including the pro-tumor data — used HNG at far higher per-milligram efficacy. Buyers may get the weak native peptide while expecting analog-class activity. This divergence is documented, not papered over.

**Named-prescriber conventions disclosed honestly.** [5] = Dr. Richard Koffler, MD / Holistic Medical Wellness / Miami Beach FL + Woodbury NY — name + NPI + venue confirmed; no specific protocol on their page; consultation framing noted. [5a] = Paragon Sports Medicine — named clinic, not currently offering clinically; educational-page only. Jay Campbell [3] = fitness author, not MD; medical reviewer Dr. Michael Fortunato, MD noted but does not upgrade tier. Seeds, A4M, IPS, Holtorf, Lee, Paulvin, Gapin, Barzilai humanin-specific protocols: **searched, not verifiable to venue+date, not fabricated.**

**Convention divergence extreme and disclosed.** 25 mcg/day to 5 mg/day = 200-fold range. Documented explicitly; not papered over.

**Off-whitelist sources check.** No Cureus, Hindawi, Ivyspring, wjgnet, Dove, Spandidos, or AME sources cited in this document.

**Source 4 retrieval caveat.** thepeptidecatalog.com/articles/humanin-dosing-guide returned HTTP 403 at time of retrieval. The HNG dose range (0.5–2 mg/day) is sourced from the web search result summary, not direct page access. Carried with explicit caveat. If the page becomes accessible, a direct-read verification is the recommended follow-up.

**Gaps / residual limits.**
- *Not resolved:* No human PK data for native humanin or HNG at any SC dose; translation from animal IP dosing is entirely unvalidated.
- *Not resolved:* Grey-market HNG availability is limited; most buyers receive native humanin, but vendor catalogues are not systematically surveyed and product availability shifts.
- *Not fabricated:* No clinic currently documented as offering humanin via a formal prescription protocol (as distinct from educational content or consultation framing).
- *Pro-tumor signal scope:* The Moreno Ayala 2020 TNBC study is the most specific published animal model; gastric and prostate cancer signals are mentioned in the research literature but the mechanistic direction is not fully consistent across tumor types. The TNBC data is the strongest single signal and is the appropriate anchor for the contraindication.
